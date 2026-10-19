#!/usr/bin/env python3
"""Synthetic qualification of the exact low-rank covariance calculation.

No model checkpoint, cached representation or empirical spectrum is read here.
"""
import json
from pathlib import Path

import numpy as np


def spectrum(z, decoder):
    zc = z - z.mean(axis=0, keepdims=True)
    s = zc.T @ zc / (len(z) - 1)
    ev, q = np.linalg.eigh(s)
    if ev.min() < -1e-12:
        raise AssertionError("unexpected non-PSD activation covariance")
    sr = (q * np.sqrt(np.maximum(ev, 0))) @ q.T
    k = sr @ (decoder @ decoder.T) @ sr
    k = (k + k.T) / 2
    return np.linalg.eigvalsh(k)[::-1]


def main():
    rng = np.random.default_rng(20261016)
    n, m, hidden = 113, 14, 37
    z = rng.lognormal(size=(n, m)) * (rng.random((n, m)) < .2)
    decoder = rng.normal(size=(m, hidden))
    h = z @ decoder
    full = np.linalg.eigvalsh(np.cov(h, rowvar=False, ddof=1))[::-1]
    reduced = spectrum(z, decoder)
    max_abs = float(np.max(np.abs(full[:m] - reduced)))
    assert np.allclose(full[:m], reduced, rtol=1e-11, atol=1e-10)
    assert np.max(np.abs(full[m:])) < 1e-10
    constant = rng.normal(size=(hidden,))
    assert np.allclose(np.cov(h + constant, rowvar=False), np.cov(h, rowvar=False), atol=1e-10)
    scaled = spectrum(z, 7.25 * decoder)
    assert np.allclose(scaled, 7.25**2 * reduced, atol=1e-8)
    assert np.allclose(scaled / scaled.sum(), reduced / reduced.sum(), atol=1e-12)
    permuted = np.column_stack([z[rng.permutation(n), i] for i in range(m)])
    assert np.array_equal(np.sort(permuted, axis=0), np.sort(z, axis=0))
    zero = spectrum(np.zeros_like(z), decoder)
    assert np.array_equal(zero, np.zeros(m))
    zero_ratio = None if float(zero.sum()) == 0.0 else float(zero[0] / zero.sum())
    assert zero_ratio is None
    p, q = .01, .5
    upper = float(np.sqrt(p * (1-q) / (q * (1-p))))
    assert np.isclose(upper, .10050378152592121)
    receipt = {
        "status": "PASS_SYNTHETIC_MATHEMATICS_ONLY",
        "seed": 20261016,
        "shape": {"positions": n, "features": m, "hidden": hidden},
        "full_vs_reduced_eigenvalue_max_abs": max_abs,
        "verified": ["exact covariance low-rank identity", "constant covariance cancellation",
                     "model scalar normalization restores lambda scale",
                     "normalized spectrum scale invariance", "independent column shuffle preserves every value",
                     "zero total variance remains unestimable", "phi upper-bound numerical example"],
        "phi_p01_q50_upper": upper,
        "boundary": "Synthetic qualification is not an empirical result or mechanism confirmation."
    }
    dest = Path(__file__).with_name("math_qualification.json")
    dest.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(receipt, ensure_ascii=False))


if __name__ == "__main__":
    main()
