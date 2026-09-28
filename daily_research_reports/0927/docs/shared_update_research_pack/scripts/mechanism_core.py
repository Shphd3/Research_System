"""Framework-independent experiment math with a supplied frozen Torch tail.

This module does NOT load S7, claim source compatibility, submit jobs, or fit SAE.
The native adapter and all preflight gates in protocol.md remain required.
"""
from __future__ import annotations
from typing import Callable
import numpy as np
import torch
import torch.nn.functional as F

Tensor = torch.Tensor
Tail = Callable[[Tensor], Tensor]

def source_gradient(W: Tensor, b: Tensor, C: Tensor, y: Tensor, tail: Tail,
                    microbatch: int = 32) -> Tensor:
    if (W.ndim != 2 or C.ndim != 2 or C.shape[1] != W.shape[1]
            or len(C) != len(y) or len(C) == 0 or microbatch < 1):
        raise ValueError('Invalid source shapes.')
    dW = torch.zeros_like(W, requires_grad=True)
    accumulated = torch.zeros_like(W)
    # Every chunk contributes its SUM divided by the same total sample count.
    for start in range(0,len(C),microbatch):
        ix=slice(start,start+microbatch)
        logits=tail(C[ix] @ (W.detach()+dW).T + b)
        if logits.ndim != 2 or logits.shape[1] != 2:
            raise ValueError('Tail must return [N,2] conditional logits.')
        loss=F.cross_entropy(logits.double(),y[ix],reduction='sum')/len(C)
        accumulated += torch.autograd.grad(loss,dW)[0].detach()
    if not torch.isfinite(accumulated).all() or accumulated.norm() < 1e-8:
        raise ValueError('Non-finite or degenerate source gradient; do not drop this branch.')
    return accumulated

def normalized_delta(W: Tensor, G: Tensor, eps: float) -> Tensor:
    if eps <= 0 or W.norm() <= 0 or G.norm() < 1e-8:
        raise ValueError('Invalid step scale.')
    return (-eps*W.detach().norm()*G/G.norm()).detach()

def measure(W: Tensor, b: Tensor, C: Tensor, y: Tensor, dW: Tensor,
            tail: Tail, Q: Tensor | None=None, microbatch: int=32) -> dict[str,np.ndarray]:
    if (C.ndim != 2 or W.ndim != 2 or C.shape[1] != W.shape[1]
            or dW.shape != W.shape or len(C) != len(y) or len(C) == 0 or microbatch < 1):
        raise ValueError('Invalid readout shapes or microbatch size.')
    arrays={k:[] for k in ('baseline','after','I','I1','C_S','C_perp','a0','da','e',
                            'logits0','logits1')}
    gb=torch.zeros_like(W)
    for start in range(0,len(C),microbatch):
        ix=slice(start,start+microbatch)
        cb=C[ix]
        a0=(cb @ W.detach().T+b).detach().requires_grad_(True)
        logits0=tail(a0)
        loss0=F.cross_entropy(logits0.double(),y[ix],reduction='none')
        # SUM gives one loss derivative per independent row. Average once below.
        e=torch.autograd.grad(loss0.sum(),a0)[0].detach()
        da=cb @ dW.T
        with torch.no_grad():
            logits1=tail(a0.detach()+da)
            loss1=F.cross_entropy(logits1.double(),y[ix],reduction='none')
        i1=(e.double()*da.double()).sum(-1)
        if Q is None:
            cs=torch.zeros_like(i1)
        else:
            cs=((e.double()@Q.double())*(da.double()@Q.double())).sum(-1)
        vals={'baseline':loss0.detach(),'after':loss1,'I':loss1-loss0.detach(),
              'I1':i1,'C_S':cs,'C_perp':i1-cs,'a0':a0.detach(),'da':da,'e':e,
              'logits0':logits0.detach(),'logits1':logits1.detach()}
        for k,v in vals.items(): arrays[k].append(v.cpu().numpy())
        gb += e.T @ cb / len(C)
    out={k:np.concatenate(v,axis=0) for k,v in arrays.items()}
    from_g=float((gb.double()*dW.double()).sum())
    from_a=float(out['I1'].mean())
    if abs(from_g-from_a)>max(1e-7,1e-4*abs(from_a)):
        raise AssertionError('Gradient/representation closure failed. Check reductions.')
    out['I1_from_gradient']=np.array(from_g)
    out['R']=out['I']-out['I1']
    return out

def orthonormal_span(D: Tensor, relative_tol: float=1e-6) -> Tensor:
    if D.ndim != 2 or D.shape[1] == 0:
        raise ValueError('Non-empty decoder-column matrix required.')
    u,s,_=torch.linalg.svd(D.double(),full_matrices=False)
    if s[0] <= 0: raise ValueError('Zero decoder span.')
    return u[:,s>relative_tol*s[0]]

def shared_atom_selection(zA: np.ndarray,zB: np.ndarray,k:int=32) -> np.ndarray:
    # Caller must concatenate structural splits only, across both rho values.
    if zA.ndim!=2 or zB.ndim!=2 or zA.shape[1]!=zB.shape[1]:
        raise ValueError('SAE coordinate identity mismatch.')
    pa=(zA>0).mean(0); pb=(zB>0).mean(0); score=np.minimum(pa,pb)
    ids=np.arange(len(score)); order=np.lexsort((ids,-score))
    return order[score[order]>0][:k]
