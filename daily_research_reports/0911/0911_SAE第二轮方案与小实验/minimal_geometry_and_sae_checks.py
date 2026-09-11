"""Auditable toy checks, NOT measurements from the user's language-model run.

1. Four fixed records: geometry changes while a two-group partition stays fixed.
2. A common orthogonal rotation preserves cosine relations.
3. Renaming dictionary components preserves their relational geometry.
4. Train a six-atom, top-2 auxiliary autoencoder for 25 updates, with/without
   detaching its input from a three-dimensional upstream linear model.

Dependencies: numpy, scikit-learn, torch, threadpoolctl.
Run: python minimal_geometry_and_sae_checks.py --output-dir results
No plots, remote execution, network requests, or repository modifications.
"""
from __future__ import annotations
import argparse
import csv
import json
from pathlib import Path
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import fowlkes_mallows_score, adjusted_rand_score
from threadpoolctl import threadpool_limits


def unit(x: np.ndarray) -> np.ndarray:
    norms = np.linalg.norm(x, axis=1, keepdims=True)
    if np.any(norms <= 1e-12):
        raise ValueError('Cannot normalize zero rows.')
    return x / norms


def geometry(h: np.ndarray, labels: np.ndarray) -> dict:
    u = unit(h)
    mu = u.mean(axis=0)
    w, b = 0.0, 0.0
    for k in np.unique(labels):
        rows = u[labels == k]
        mk = rows.mean(axis=0)
        mass = len(rows) / len(u)
        w += mass * np.square(rows - mk).sum(axis=1).mean()
        b += mass * np.square(mk - mu).sum()
    identity_residual = abs(w + b - (1.0 - mu @ mu))
    assert identity_residual < 1e-12
    return {'W':float(w), 'B':float(b), 'B_over_W':float(b/w),
            'mean_norm_squared':float(mu @ mu),
            'identity_residual':float(identity_residual)}


def run_gradient_check(detach_input: bool) -> dict:
    import torch
    torch.set_num_threads(1)
    torch.manual_seed(17)
    dtype = torch.float64
    x = torch.tensor([[4., -2., -1.], [4., -2., 1.],
                      [4., 2., -1.], [4., 2., 1.]], dtype=dtype)
    x = x / x.norm(dim=1, keepdim=True)
    theta = torch.nn.Parameter(torch.eye(3, dtype=dtype))
    encoder = torch.nn.Parameter(torch.randn(6, 3, dtype=dtype) * 0.3)
    decoder = torch.nn.Parameter(torch.randn(3, 6, dtype=dtype) * 0.3)
    optimizer = torch.optim.SGD([theta, encoder, decoder], lr=0.05)
    h0 = (x @ theta.T).detach().clone()
    sae0 = torch.cat([encoder.detach().reshape(-1), decoder.detach().reshape(-1)]).clone()

    def forward():
        h = x @ theta.T
        observed = h.detach() if detach_input else h
        positive = torch.relu(observed @ encoder.T)
        values, ids = positive.topk(2, dim=1)
        z = torch.zeros_like(positive).scatter(1, ids, values)
        reconstructed = z @ decoder.T
        loss = (reconstructed - observed).square().mean()
        return loss, h

    initial_loss = float(forward()[0].detach())
    first_main_grad = None
    for step in range(25):
        optimizer.zero_grad(set_to_none=True)
        loss, _ = forward()
        loss.backward()
        if step == 0:
            first_main_grad = 0.0 if theta.grad is None else float(theta.grad.norm())
        optimizer.step()
    final_loss, h_end = forward()
    delta_h = float((h_end.detach() - h0).square().mean().sqrt())
    sae_end = torch.cat([encoder.detach().reshape(-1), decoder.detach().reshape(-1)])
    if detach_input:
        assert delta_h == 0.0
    else:
        assert delta_h > 0.0
    assert float((sae_end-sae0).norm()) > 0.0
    return {'mode':'observe_only' if detach_input else 'joint_reconstruction',
            'detach_input':detach_input, 'updates':25, 'initial_loss':initial_loss,
            'final_loss':float(final_loss.detach()),
            'initial_upstream_gradient_norm':first_main_grad,
            'rms_change_in_h':delta_h,
            'sae_parameter_change':float((sae_end-sae0).norm()),
            'note':'No task loss is used; this isolates reconstruction-gradient connectivity.'}


def run(output_dir: str | Path) -> dict:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    labels = np.array([0,0,1,1])
    y = np.array([-1.,-1.,1.,1.])
    eps = np.array([-1.,1.,-1.,1.])
    h0 = np.column_stack([np.full(4,4.0), 2.0*y, eps])
    h1 = np.column_stack([np.full(4,3.8), 2.08*y, eps])
    u0, u1 = unit(h0), unit(h1)
    m0, m1 = geometry(h0,labels), geometry(h1,labels)
    off_diagonal = ~np.eye(4,dtype=bool)
    r_all = float(np.abs(u0@u0.T-u1@u1.T).mean())
    r_off = float(np.abs(u0@u0.T-u1@u1.T)[off_diagonal].mean())
    with threadpool_limits(limits=1):
        c0 = KMeans(n_clusters=2,n_init=20,random_state=17).fit_predict(u0)
        c1 = KMeans(n_clusters=2,n_init=20,random_state=17).fit_predict(u1)
    partition_fm = float(fowlkes_mallows_score(c0,c1))
    assert partition_fm == 1.0
    assert adjusted_rand_score(labels,c0) == 1.0
    assert adjusted_rand_score(labels,c1) == 1.0
    # A deterministic common rotation, applied to every sample.
    rng = np.random.default_rng(17)
    q, _ = np.linalg.qr(rng.normal(size=(3,3)))
    rotated = u0@q
    r_rotation = float(np.abs(rotated@rotated.T-u0@u0.T).mean())
    assert r_rotation < 1e-12
    # Raw component-index mismatch vs permutation-invariant relations.
    code = np.array([[0.8,0.1,0.1],[0.7,0.2,0.1],
                     [0.1,0.7,0.2],[0.1,0.1,0.8]])
    permuted = code[:,[2,0,1]]
    raw_code_mse = float(np.square(code-permuted).mean())
    relabel_relation_error = float(np.abs(unit(code)@unit(code).T -
                                         unit(permuted)@unit(permuted).T).max())
    assert relabel_relation_error < 1e-12
    report = {
        'warning':'Constructed four-point geometry plus a tiny autograd/optimization check; not LLM evidence.',
        'geometry':{'start':m0,'end':m1,
                    'relative_change':{k:float(m1[k]/m0[k]-1) for k in ['W','B','B_over_W']},
                    'R_mean_abs_all_pairs':r_all,'R_mean_abs_off_diagonal':r_off,
                    'partition_FM':partition_fm,
                    'known_sign_classifier_accuracy_start':float(np.mean((u0[:,1]>0)==labels)),
                    'known_sign_classifier_accuracy_end':float(np.mean((u1[:,1]>0)==labels))},
        'common_rotation_R':r_rotation,
        'component_renaming':{'raw_code_mse':raw_code_mse,
                             'max_relation_difference':relabel_relation_error},
        'gradient_checks':[run_gradient_check(True),run_gradient_check(False)]}
    (out/'toy_results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    np.savez(out/'toy_arrays.npz',h0=h0,h1=h1,labels=labels,rotation=q)
    with (out/'geometry_results.csv').open('w',newline='',encoding='utf-8') as f:
        wr=csv.DictWriter(f,fieldnames=['state',*m0.keys()]);wr.writeheader()
        wr.writerow({'state':'start',**m0});wr.writerow({'state':'end',**m1})
    return report

if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir',type=Path,default=Path('toy_results'))
    args=parser.parse_args()
    print(json.dumps(run(args.output_dir),ensure_ascii=False,indent=2))
