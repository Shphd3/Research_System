#!/usr/bin/env python3
"""Linear CKA for aligned, already extracted representation matrices.

Requirements: Python >= 3.10 and NumPy.
Run: python cka_reference.py --self-test
     python cka_reference.py x.npz y.npz --out pair.json

Each NPZ contains `features` (n x d) and unique Unicode/byte-string
`sample_ids` (n). Both files must contain exactly the same ID set.
This program does NOT verify the model site, text hashes, source groups,
training history, or metadata contracts. It does NOT test model quality.

The U-corrected estimator normalizes U-centered Gram matrices. Correcting
the underlying HSIC estimates does not make the resulting ratio unbiased.
It can be negative; it is never clipped to [0, 1].

Methods: Kornblith et al. (2019), Similarity of Neural Network
Representations Revisited, and its authors' public CKA reference notebook.
Implementation below is expressed directly from the mathematical formulas.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys
import tempfile
from typing import Any

import numpy as np


class DegenerateRepresentationError(ValueError):
    """CKA is undefined for this representation or estimator."""


def _center_and_scale(x: np.ndarray, name: str) -> np.ndarray:
    arr = np.asarray(x)
    if arr.ndim != 2 or min(arr.shape) == 0:
        raise ValueError(f"{name} must be a nonempty [samples, features] matrix")
    if arr.dtype.kind not in "fiu":
        raise TypeError(f"{name} must have real numeric dtype")
    arr = arr.astype(np.float64, copy=True)
    if not np.isfinite(arr).all():
        raise ValueError(f"{name} contains NaN or infinity")
    # A uniform positive scale is CKA-invariant. Scale before centering to
    # avoid overflow, then rescale centered values for stable Gram products.
    scale = float(np.max(np.abs(arr)))
    if scale == 0.0:
        raise DegenerateRepresentationError(f"{name} is all zero")
    arr /= scale
    if np.all(arr == arr[0:1, :]):
        raise DegenerateRepresentationError(f"{name} has no variation across samples")
    arr -= arr.mean(axis=0, keepdims=True)
    scale = float(np.max(np.abs(arr)))
    if scale == 0.0:
        raise DegenerateRepresentationError(f"{name} is constant after centering")
    arr /= scale
    return arr


def _center_gram(gram: np.ndarray, corrected: bool) -> np.ndarray:
    n = gram.shape[0]
    if corrected:
        if n < 4:
            raise ValueError("U-corrected CKA requires at least four samples")
        g = gram.copy()
        np.fill_diagonal(g, 0.0)
        row_sum = g.sum(axis=1, keepdims=True)
        total = float(row_sum.sum())
        g -= row_sum / (n - 2)
        g -= row_sum.T / (n - 2)
        g += total / ((n - 1) * (n - 2))
        np.fill_diagonal(g, 0.0)
        return g
    row_mean = gram.mean(axis=1, keepdims=True)
    return gram - row_mean - row_mean.T + float(gram.mean())


def _normalized_inner_product(k: np.ndarray, l: np.ndarray) -> float:
    kn = float(np.linalg.norm(k, ord="fro"))
    ln = float(np.linalg.norm(l, ord="fro"))
    if not np.isfinite(kn + ln) or kn == 0.0 or ln == 0.0:
        raise DegenerateRepresentationError("Centered Gram norm is zero or non-finite")
    score = float(np.sum((k / kn) * (l / ln)))
    if not np.isfinite(score):
        raise FloatingPointError("Non-finite CKA value")
    return score


def linear_cka(x: np.ndarray, y: np.ndarray, corrected: bool = False) -> float:
    """Calculate linear CKA; rows must refer to the same ordered samples.

    Uses O(n^2) memory, appropriate for the plan's finite audit panels.
    `corrected=True` uses U-centered kernels, not an unbiased final ratio.
    Degenerate kernels raise an exception rather than returning a fake zero.
    """
    xc = _center_and_scale(x, "X")
    yc = _center_and_scale(y, "Y")
    n = xc.shape[0]
    if n != yc.shape[0]:
        raise ValueError("X and Y must have the same number of samples")
    if n < (4 if corrected else 2):
        raise ValueError("Too few samples for the selected estimator")
    gx, gy = xc @ xc.T, yc @ yc.T
    k, l = _center_gram(gx, corrected), _center_gram(gy, corrected)
    # U-centering may annihilate a nonconstant but uninformative kernel,
    # e.g. a scalar multiple of the identity. Detect numerical residue.
    tol = 100.0 * np.finfo(np.float64).eps
    for g, centered in ((gx, k), (gy, l)):
        if np.linalg.norm(centered, "fro") <= tol * np.linalg.norm(g, "fro"):
            raise DegenerateRepresentationError("Centered kernel is numerically degenerate")
    return _normalized_inner_product(k, l)


def _load_npz(path: Path) -> tuple[np.ndarray, list[str]]:
    with np.load(path, allow_pickle=False) as data:
        missing = {"features", "sample_ids"} - set(data.files)
        if missing:
            raise ValueError(f"{path}: missing NPZ keys: {sorted(missing)}")
        features = np.asarray(data["features"])
        ids = np.asarray(data["sample_ids"])
    if features.ndim != 2 or ids.ndim != 1 or len(ids) != features.shape[0]:
        raise ValueError(f"{path}: inconsistent feature/ID dimensions")
    if ids.dtype.kind not in "US":
        raise TypeError(f"{path}: sample_ids must be strings; object arrays are not accepted")
    names = [v.decode("utf-8") if isinstance(v, bytes) else str(v) for v in ids.tolist()]
    if any(not name for name in names) or len(set(names)) != len(names):
        raise ValueError(f"{path}: sample IDs must be nonempty and unique")
    return features, names


def align_npz(x_path: Path, y_path: Path) -> tuple[np.ndarray, np.ndarray, dict[str, Any]]:
    x, xi = _load_npz(x_path)
    y, yi = _load_npz(y_path)
    if set(xi) != set(yi):
        raise ValueError("ID sets differ; refusing to silently intersect the datasets")
    lookup = {name: i for i, name in enumerate(yi)}
    order = [lookup[name] for name in xi]
    ordered_bytes = json.dumps(xi, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    return x, y[order], {
        "y_rows_reordered": xi != yi,
        "ordered_sample_ids_sha256": hashlib.sha256(ordered_bytes).hexdigest(),
        "n_samples": len(xi),
        "x_features": int(x.shape[1]),
        "y_features": int(y.shape[1]),
    }


def self_test() -> dict[str, Any]:
    rng = np.random.default_rng(20260920)
    x = rng.normal(size=(96, 13))
    y = rng.normal(size=(96, 9))
    q, _ = np.linalg.qr(rng.normal(size=(13, 13)))
    transformed = 2.0 * x @ q + rng.normal(size=(1, 13))
    permutation = rng.permutation(len(x))
    checks: dict[str, bool] = {}
    for corrected in (False, True):
        tag = "u" if corrected else "biased"
        np.testing.assert_allclose(linear_cka(x, x, corrected), 1.0, atol=1e-10)
        checks[f"self_{tag}"] = True
        np.testing.assert_allclose(linear_cka(x, transformed, corrected), 1.0, atol=1e-10)
        checks[f"orthogonal_scale_translation_{tag}"] = True
        np.testing.assert_allclose(linear_cka(x, y, corrected),
                                   linear_cka(x[permutation], y[permutation], corrected), atol=1e-10)
        checks[f"shared_row_permutation_{tag}"] = True
    xc, yc = x - x.mean(axis=0), y - y.mean(axis=0)
    feature_score = float(np.linalg.norm(xc.T @ yc, "fro") ** 2 /
                          (np.linalg.norm(xc.T @ xc, "fro") * np.linalg.norm(yc.T @ yc, "fro")))
    np.testing.assert_allclose(linear_cka(x, y), feature_score, atol=1e-10)
    checks["feature_gram_formula_agreement"] = True
    try:
        linear_cka(np.ones_like(x), y)
    except DegenerateRepresentationError:
        checks["constant_matrix_rejected"] = True
    else:
        raise AssertionError("A constant matrix must be rejected")
    try:
        linear_cka(np.eye(8), np.eye(8), corrected=True)
    except DegenerateRepresentationError:
        checks["degenerate_u_kernel_rejected"] = True
    else:
        raise AssertionError("U-centered identity kernel must be rejected")
    with tempfile.TemporaryDirectory() as tmp:
        px, py = Path(tmp) / "x.npz", Path(tmp) / "y.npz"
        ids = np.array([f"sample_{i:04d}" for i in range(len(x))])
        np.savez(px, features=x, sample_ids=ids)
        np.savez(py, features=y[permutation], sample_ids=ids[permutation])
        ax, ay, meta = align_npz(px, py)
        np.testing.assert_array_equal(ax, x)
        np.testing.assert_array_equal(ay, y)
        assert meta["y_rows_reordered"]
        checks["sample_ids_realign"] = True
        np.savez(py, features=y[:-1], sample_ids=ids[:-1])
        try:
            align_npz(px, py)
        except ValueError:
            checks["different_id_sets_rejected"] = True
        else:
            raise AssertionError("Different ID sets must be rejected")
    random_x = rng.normal(size=(48, 2048))
    random_y = rng.normal(size=(48, 1536))
    independent_demo = {
        "n": 48, "dx": 2048, "dy": 1536,
        "cka_linear_biased": linear_cka(random_x, random_y),
        "cka_linear_u": linear_cka(random_x, random_y, corrected=True),
        "scope": "Independent synthetic Gaussian matrices, NOT language-model results",
    }
    return {"status": "PASS", "checks": checks, "independent_high_dimensional_demo": independent_demo,
            "numpy_version": np.__version__}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("x", nargs="?", type=Path)
    parser.add_argument("y", nargs="?", type=Path)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    try:
        if args.self_test:
            if args.x or args.y:
                raise ValueError("--self-test does not accept input files")
            result = self_test()
        else:
            if args.x is None or args.y is None:
                parser.error("Provide two NPZ files, or use --self-test")
            x, y, meta = align_npz(args.x, args.y)
            result = {"status": "OK", **meta, "estimators": {},
                      "scope": "Description of the aligned matrices, not semantic or capability quality",
                      "metadata_contract": "Upstream site, content hashes and data versions must be verified"}
            for name, corrected in (("cka_linear_biased", False), ("cka_linear_u", True)):
                try:
                    value = linear_cka(x, y, corrected)
                    result["estimators"][name] = {"value": value, "status": "OK"}
                except DegenerateRepresentationError as exc:
                    result["estimators"][name] = {"value": None, "status": "undefined", "reason": str(exc)}
        text = json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False)
        if args.out:
            args.out.parent.mkdir(parents=True, exist_ok=True)
            with args.out.open("x", encoding="utf-8") as stream:
                stream.write(text + "\n")
        print(text)
        return 0
    except (OSError, ValueError, TypeError, FloatingPointError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
