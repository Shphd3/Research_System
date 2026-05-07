#!/usr/bin/env python3
import os
import argparse
import numpy as np
import torch
import pandas as pd
import matplotlib.pyplot as plt


def load_pt_matrix(path: str) -> np.ndarray:
    t = torch.load(path, map_location="cpu")
    if not torch.is_tensor(t):
        raise TypeError(f"Expected torch.Tensor in {path}, got {type(t)}")
    X = t.detach().cpu().numpy().astype(np.float64)
    if X.ndim != 2:
        raise ValueError(f"Expected 2D tensor [N,H], got {X.shape}")
    return X


def mean_noise_ratio(X: np.ndarray) -> dict:
    """
    Compute:
      mu = mean over rows
      mu_norm = ||mu||_2
      sigma2 = E||x||^2 (mean over rows of squared norm)
      noise_level = sqrt(sigma2 / N)
      R = mu_norm / noise_level
    """
    N, H = X.shape
    mu = X.mean(axis=0)
    mu_norm = float(np.linalg.norm(mu))

    row_sq = np.sum(X * X, axis=1)
    sigma2 = float(np.mean(row_sq))
    noise_level = float(np.sqrt(sigma2 / N))

    R = mu_norm / (noise_level + 1e-30)

    return {
        "N": N,
        "H": H,
        "mu_norm": mu_norm,
        "noise_level": noise_level,
        "R": R,
        "mu_mean": float(np.mean(mu)),
        "mu_std": float(np.std(mu)),
        "mu_abs_median": float(np.median(np.abs(mu))),
        "mu_abs_p99": float(np.percentile(np.abs(mu), 99)),
        "mu_abs_max": float(np.max(np.abs(mu))),
        "mu_pos_frac": float(np.mean(mu > 0)),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base_dir", default=".", help="directory containing *.pt files")
    ap.add_argument("--outdir", default="./sec2_1_figures")
    ap.add_argument("--runs", nargs="+", required=True,
                    help="Each run: name,activation_file,grad_output_file")
    args = ap.parse_args()

    os.makedirs(args.outdir, exist_ok=True)

    rows = []
    for spec in args.runs:
        # spec format: name,act.pt,grad.pt
        parts = spec.split(",")
        if len(parts) != 3:
            raise ValueError(f"Bad run spec: {spec}. Use name,activation.pt,grad_output.pt")
        name, act_f, grad_f = parts
        act_path = os.path.join(args.base_dir, act_f)
        grad_path = os.path.join(args.base_dir, grad_f)

        X = load_pt_matrix(act_path)
        D = load_pt_matrix(grad_path)

        rX = mean_noise_ratio(X)
        rD = mean_noise_ratio(D)

        rows.append({
            "run": name,
            "type": "activation",
            **rX
        })
        rows.append({
            "run": name,
            "type": "grad_output",
            **rD
        })

        print(f"[INFO] {name}: R_x={rX['R']:.3f}, R_delta={rD['R']:.3f}")

    df = pd.DataFrame(rows)
    out_csv = os.path.join(args.outdir, "sec2_1_mean_significance.csv")
    df.to_csv(out_csv, index=False)
    print(f"[INFO] Saved CSV: {out_csv}")

    # Bar plot of R values
    pivot = df.pivot(index="run", columns="type", values="R").reset_index()

    plt.figure(figsize=(9, 4))
    x = np.arange(len(pivot))
    w = 0.38
    plt.bar(x - w/2, pivot["activation"], width=w, label="Activation $R_x$")
    plt.bar(x + w/2, pivot["grad_output"], width=w, label="Grad output $R_\\delta$")

    plt.xticks(x, pivot["run"], rotation=20, ha="right")
    plt.ylabel(r"$R = \|\mu\| / \sqrt{\mathbb{E}\|x\|^2/N}$")
    plt.title("Noise-normalized mean magnitude (Activation vs Grad Output)")
    plt.grid(True, axis="y", ls="--", alpha=0.3)
    plt.legend()
    plt.tight_layout()

    out_png = os.path.join(args.outdir, "sec2_1_R_bar.png")
    plt.savefig(out_png, dpi=200)
    plt.close()
    print(f"[INFO] Saved figure: {out_png}")


if __name__ == "__main__":
    main()
