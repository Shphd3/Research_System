"""Deterministic tensor-task construction; no access to losses or gradients."""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import argparse, hashlib, json
import numpy as np

@dataclass(frozen=True)
class Geometry:
    c0: np.ndarray
    Q: np.ndarray
    sigma: float
    beta: float = 0.25

    def validate(self) -> None:
        if self.c0.ndim != 1 or self.Q.shape != (self.c0.size, 16):
            raise ValueError('Expected c0[d] and Q[d,16].')
        if not np.isfinite(self.c0).all() or not np.isfinite(self.Q).all():
            raise ValueError('Non-finite geometry.')
        n = np.linalg.norm(self.c0)
        if n <= 1e-8 or self.sigma <= 1e-8 or self.beta < 0:
            raise ValueError('Degenerate baseline, amplitude or nuisance scale.')
        if np.linalg.norm(self.Q.T @ self.Q - np.eye(16)) >= 1e-5:
            raise ValueError('Q is not orthonormal.')
        if np.linalg.norm(self.Q.T @ self.c0) / n >= 1e-5:
            raise ValueError('Q is not perpendicular to c0.')

def signed_qr(a: np.ndarray) -> np.ndarray:
    q, r = np.linalg.qr(a)
    signs = np.where(np.diag(r) < 0, -1.0, 1.0)
    return q * signs[None, :]

def calibrate(C: np.ndarray, tie_keys=None) -> tuple[Geometry, int]:
    """C contains native positions only; selection is label/loss blind."""
    C = np.asarray(C, dtype=np.float64)
    if C.ndim != 2 or min(C.shape) < 17 or not np.isfinite(C).all():
        raise ValueError('Insufficient or invalid native calibration positions.')
    distances = np.sum((C - C.mean(0)) ** 2, axis=1)
    tied = np.flatnonzero(distances == distances.min())
    if tie_keys is not None:
        if len(tie_keys) != len(C):
            raise ValueError('Reference tie-key count mismatch.')
        ref = int(min(tied, key=lambda index: tie_keys[index]))
    else:
        ref = int(tied[0])
    c0 = C[ref].copy()
    n2 = float(c0 @ c0)
    if n2 <= 1e-16:
        raise ValueError('Zero reference: protocol amendment required.')
    V = C - c0
    V -= np.outer(V @ c0 / n2, c0)
    V -= V.mean(0)
    _, s, vt = np.linalg.svd(V, full_matrices=False)
    if len(s) < 16 or s[15] <= 1e-8:
        raise ValueError('Calibration rank below 16.')
    raw = vt[:16].T
    raw -= np.outer(c0, c0 @ raw / n2)
    Q = signed_qr(raw)
    sigma = 0.25 * float(np.median(np.std((C - c0) @ Q, axis=0, ddof=0)))
    geometry = Geometry(c0, Q, sigma)
    geometry.validate()
    return geometry, ref

def directions(geometry: Geometry, family: int, rho: float) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    geometry.validate()
    if not 0 <= rho < 1:
        raise ValueError('Require 0 <= rho < 1: avoid indistinguishable contradictory tasks.')
    rng = np.random.default_rng(np.random.SeedSequence([20260927, int(family), 99]))
    F = geometry.Q @ signed_qr(rng.normal(size=(16, 16)))
    va = np.sqrt(rho) * F[:, 0] + np.sqrt(1-rho) * F[:, 1]
    vb = np.sqrt(rho) * F[:, 0] + np.sqrt(1-rho) * F[:, 2]
    assert abs(float(va @ vb) - rho) < 1e-6
    return va, vb, F[:, 3:]

def generate(geometry: Geometry, family: int, rho: float, split: int,
             repeat: int, n_pairs: int, group: str) -> dict[str, np.ndarray]:
    if group not in ('A', 'B') or n_pairs < 1:
        raise ValueError('Invalid group or sample count.')
    va, vb, nuisance = directions(geometry, family, rho)
    rng = np.random.default_rng(np.random.SeedSequence([20260927, family, split, repeat]))
    xi = rng.normal(size=(n_pairs, 13)) / np.sqrt(13.0)
    t = np.tile(np.array([-1.0, 1.0]), n_pairs)
    vector = va if group == 'A' else vb
    C = geometry.c0 + geometry.sigma * (
        t[:, None] * vector[None, :] + geometry.beta * np.repeat(xi @ nuisance.T, 2, axis=0)
    )
    return {'c': C.astype(np.float32), 't': t.astype(np.int64),
            'pair_id': np.repeat(np.arange(n_pairs), 2), 'xi': xi,
            'y_same': ((t + 1)/2).astype(np.int64),
            'y_flip': ((1 - t)/2).astype(np.int64)}

def witness(geometry: Geometry, family: int, rho: float, rule: int,
            a_plus: np.ndarray, a_minus: np.ndarray, bias: np.ndarray) -> np.ndarray:
    if rule not in (-1, 1):
        raise ValueError('rule must be +/-1.')
    va, vb, _ = directions(geometry, family, rho)
    w = (va + rule*vb)/(1 + rule*rho)
    mid, diff = (a_plus+a_minus)/2, (a_plus-a_minus)/2
    return np.outer(mid-bias, geometry.c0)/(geometry.c0 @ geometry.c0) + np.outer(diff/geometry.sigma, w)

def digest(a: np.ndarray) -> str:
    return hashlib.sha256(np.ascontiguousarray(a).tobytes()).hexdigest()

if __name__ == '__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--basis', type=Path, required=True)
    p.add_argument('--out', type=Path, required=True)
    p.add_argument('--family', type=int, default=21001)
    p.add_argument('--rho', type=float, default=0.8)
    p.add_argument('--pairs', type=int, default=256)
    a=p.parse_args()
    if a.out.exists():
        raise FileExistsError(a.out)
    z=np.load(a.basis, allow_pickle=False)
    g=Geometry(z['c0'], z['Q'], float(z['sigma']), float(z['beta']) if 'beta' in z else 0.25)
    b=generate(g,a.family,a.rho,40,0,a.pairs,'B')
    a.out.parent.mkdir(parents=True,exist_ok=True)
    np.savez_compressed(a.out, **b)
    print(json.dumps({'path':str(a.out),'c_sha256':digest(b['c']), 'records':len(b['c'])}))
