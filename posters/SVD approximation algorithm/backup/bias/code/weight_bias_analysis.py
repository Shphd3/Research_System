#!/usr/bin/env python3
import argparse
import numpy as np
import torch
import pandas as pd

def load_pt(path: str) -> np.ndarray:
    t = torch.load(path, map_location="cpu")
    if not torch.is_tensor(t):
        raise TypeError(f"Expected torch.Tensor in {path}, got {type(t)}")
    W = t.detach().cpu().numpy().astype(np.float64)
    if W.ndim != 2:
        raise ValueError(f"Expected 2D weight, got {W.shape}")
    return W

def frob2(A: np.ndarray) -> float:
    return float(np.sum(A*A))

def stats_vec(v: np.ndarray, name: str) -> dict:
    av = np.abs(v)
    return {
        f"{name}_l2": float(np.linalg.norm(v)),
        f"{name}_abs_median": float(np.median(av)),
        f"{name}_abs_p90": float(np.percentile(av, 90)),
        f"{name}_abs_p99": float(np.percentile(av, 99)),
        f"{name}_abs_max": float(np.max(av)),
        f"{name}_pos_frac": float(np.mean(v > 0)),
    }

def analyze(W: np.ndarray) -> dict:
    dout, din = W.shape
    Ew = frob2(W)

    # Column-mean (mean over rows / outputs)
    mu_col = W.mean(axis=0)              # (din,)
    W_col = np.ones((dout,1)) @ mu_col[None,:]
    rho_col = frob2(W_col) / (Ew + 1e-30)

    # Row-mean (mean over columns / inputs)
    mu_row = W.mean(axis=1)              # (dout,)
    W_row = mu_row[:,None] @ np.ones((1,din))
    rho_row = frob2(W_row) / (Ew + 1e-30)

    # Centered versions (remove mean components)
    Wc_col = W - W_col
    Wc_row = W - W_row

    # “Noise-normalized” style ratios for mean vectors:
    # compare ||mu|| to typical entry scale / sqrt(n)
    # For mu_col: average over dout samples per column
    entry_rms = np.sqrt(Ew / (dout*din))
    noise_col = entry_rms / np.sqrt(dout)
    noise_row = entry_rms / np.sqrt(din)

    R_col = float(np.linalg.norm(mu_col) / (np.sqrt(din) * noise_col + 1e-30))
    R_row = float(np.linalg.norm(mu_row) / (np.sqrt(dout) * noise_row + 1e-30))

    out = {
        "dout": dout,
        "din": din,
        "W_rms": float(entry_rms),
        "rho_colmean_energy": float(rho_col),
        "rho_rowmean_energy": float(rho_row),
        "R_colmean": R_col,
        "R_rowmean": R_row,
        "Wc_col_rms": float(np.sqrt(frob2(Wc_col)/(dout*din))),
        "Wc_row_rms": float(np.sqrt(frob2(Wc_row)/(dout*din))),
    }
    out.update(stats_vec(mu_col, "mu_col"))
    out.update(stats_vec(mu_row, "mu_row"))
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--files", nargs="+", required=True)
    ap.add_argument("--out_csv", default="weight_bias_summary.csv")
    args = ap.parse_args()

    rows = []
    for f in args.files:
        W = load_pt(f)
        r = analyze(W)
        r["file"] = f
        rows.append(r)
        print(f"[INFO] {f}: rho_col={r['rho_colmean_energy']:.4f}, rho_row={r['rho_rowmean_energy']:.4f}, "
              f"R_col={r['R_colmean']:.2f}, R_row={r['R_rowmean']:.2f}")

    df = pd.DataFrame(rows)
    df.to_csv(args.out_csv, index=False)
    print(f"[INFO] Saved CSV: {args.out_csv}")

if __name__ == "__main__":
    main()
