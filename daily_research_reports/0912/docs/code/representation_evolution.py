"""Fixed-panel drift and cross-readout audit. All axes must use identical sample IDs.
Use 2x2 H(time) x SAE(time), plus group swaps, rather than equating latent index IDs.
"""
import argparse,json
from pathlib import Path
import numpy as np
import torch
from .feature_statistics import sparse_codes,group_scores
from model import Qwen3SAEForCausalLM

def relation_matrix(x,max_n=4096):
    x=np.asarray(x,dtype=np.float64)
    if x.ndim!=2 or len(x)>max_n:raise ValueError("Expected [N,D] with N <= 4096; explicitly subsample a FIXED panel")
    u=x/np.linalg.norm(x,axis=1,keepdims=True).clip(1e-12)
    return u@u.T

def relation_drift(x,y):
    if len(x)!=len(y):raise ValueError("Mismatched sample count")
    a,b=relation_matrix(x),relation_matrix(y)
    keep=~np.eye(len(a),dtype=bool)
    return float(np.sqrt(np.mean((a[keep]-b[keep])**2))) if len(a)>1 else 0.0

def variance_decomposition(x,weights):
    """W+B=T for a COMPLETE nonnegative soft partition, using one metric/weighting.
    Never silently renormalize incomplete SAE coverage into a complete partition.
    """
    x=np.asarray(x,dtype=np.float64);q=np.asarray(weights,dtype=np.float64)
    if q.ndim!=2 or len(q)!=len(x) or np.any(q<0) or not np.allclose(q.sum(1),1,atol=1e-7):
        raise ValueError("Need a complete per-token partition; append unassigned category explicitly")
    mu=x.mean(0);mass=q.sum(0);use=mass>0
    centers=(q[:,use].T@x)/mass[use,None]
    within=sum(float((q[:,g,None]*(x-centers[j])**2).sum()) for j,g in enumerate(np.flatnonzero(use)))/len(x)
    between=float((mass[use,None]*(centers-mu)**2).sum())/len(x)
    total=float(((x-mu)**2).sum())/len(x)
    if not np.isclose(within+between,total,atol=1e-8,rtol=1e-7):raise ArithmeticError("Variance identity failed")
    return {"W":within,"B":between,"T":total,"B_over_T":between/total if total else None}

@torch.inference_mode()
def read_with(h,sae,group_ids=None,batch_size=256):
    sae.eval()
    chunks=[]
    for a in range(0,len(h),batch_size):
        x=torch.tensor(h[a:a+batch_size],dtype=sae.decoder.dtype,device=sae.decoder.device)
        idx,val=sae.encode(x)
        z=sparse_codes(idx.cpu().numpy(),val.float().cpu().numpy(),sae.width)
        chunks.append(z.toarray() if group_ids is None else group_scores(z,group_ids)[0])
    return np.concatenate(chunks)

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--early-activations",required=True);p.add_argument("--late-activations",required=True)
    p.add_argument("--early-checkpoint",required=True);p.add_argument("--late-checkpoint",required=True)
    p.add_argument("--early-groups");p.add_argument("--late-groups");p.add_argument("--output",required=True)
    a=p.parse_args()
    with np.load(a.early_activations,allow_pickle=False) as f:early=dict(f)
    with np.load(a.late_activations,allow_pickle=False) as f:late=dict(f)
    if not np.array_equal(early["sample_ids"],late["sample_ids"]):raise ValueError("Panel identity/order mismatch")
    s0=Qwen3SAEForCausalLM.from_checkpoint(a.early_checkpoint).sae
    s1=Qwen3SAEForCausalLM.from_checkpoint(a.late_checkpoint).sae
    if s0 is None or s1 is None:raise ValueError("Both checkpoints require SAE observers")
    views={f"H{t}_E{e}":read_with(h,s) for t,h in enumerate([early["h"],late["h"]]) for e,s in enumerate([s0,s1])}
    result={"native_h_relation_drift":relation_drift(early["h"],late["h"]),
            "H_change_fixed_E0":relation_drift(views["H0_E0"],views["H1_E0"]),
            "E_change_fixed_H0":relation_drift(views["H0_E0"],views["H0_E1"]),
            "E_change_fixed_H1":relation_drift(views["H1_E0"],views["H1_E1"]),
            "joint_change":relation_drift(views["H0_E0"],views["H1_E1"]),
            "warning":"These are replacement contrasts, NOT additive percentages or semantic accuracy."}
    if bool(a.early_groups)!=bool(a.late_groups):raise ValueError("Supply BOTH group maps or neither")
    if a.early_groups:
        g0=np.load(a.early_groups,allow_pickle=False)["group_ids"];g1=np.load(a.late_groups,allow_pickle=False)["group_ids"]
        if s0.width!=s1.width:raise ValueError("Group-map swaps require same width AND continued latent identity")
        # Only valid for continued SAE parameters, not independently permuted/fitted dictionaries.
        q={f"H{t}_E{e}_G{g}":read_with(h,s,groups) for t,h in enumerate([early["h"],late["h"]])
           for e,s in enumerate([s0,s1]) for g,groups in enumerate([g0,g1])}
        result["group_views"]={k:relation_drift(q["H0_E0_G0"],v) for k,v in q.items()}
        result["group_swap_boundary"]="Only continued neuron indexing; independent dictionaries require calibration alignment first."
    Path(a.output).write_text(json.dumps(result,indent=2),encoding="utf-8")
if __name__=="__main__":main()
