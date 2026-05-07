#!/usr/bin/env python3
import os
import argparse
import numpy as np
import torch
import matplotlib.pyplot as plt
import csv


def load_pt_matrix(path: str) -> np.ndarray:
    t = torch.load(path, map_location="cpu")
    if not torch.is_tensor(t):
        raise TypeError(f"Expected torch.Tensor in {path}, got {type(t)}")
    X = t.detach().cpu().numpy().astype(np.float64)
    if X.ndim != 2:
        raise ValueError(f"Expected 2D tensor [N,H], got {X.shape}")
    return X


def weight_grad(Delta: np.ndarray, X: np.ndarray) -> np.ndarray:
    # G = Δ^T X / N
    N = X.shape[0]
    return (Delta.T @ X) / float(N)


def spectrum_summary(A: np.ndarray, spike_frac: float = 0.01):
    s = np.linalg.svd(A, full_matrices=False, compute_uv=False)
    e = s * s
    total = float(np.sum(e) + 1e-30)
    cum = np.cumsum(e) / total

    r = len(s)
    k_spike = max(1, int(np.ceil(spike_frac * r)))

    def k_for(p):
        return int(np.searchsorted(cum, p) + 1)

    return {
        "rank": r,
        "k_spike": k_spike,
        "top1": float(s[0]),
        "top5": [float(x) for x in s[:5]],
        "energy_top_spike": float(cum[k_spike - 1]),
        "k50": k_for(0.5),
        "k80": k_for(0.8),
        "k90": k_for(0.9),
        "k95": k_for(0.95),
        "s": s,
        "cum": cum,
    }


def save_spectrum_plot(s_raw, s_cent, k_spike, outpath, title):
    m = min(len(s_raw), len(s_cent))
    ks = np.arange(1, m + 1)

    plt.figure(figsize=(6.5, 4))
    plt.loglog(ks, s_raw[:m], label="Raw $G$", linewidth=2)
    plt.loglog(ks, s_cent[:m], label="Centered $G_c$", linewidth=2)
    plt.axvline(k_spike, linestyle="--", linewidth=1.5)
    plt.xlabel("Singular index $k$ (log)")
    plt.ylabel("Singular value $\\sigma_k$ (log)")
    plt.title(title)
    plt.grid(True, which="both", ls="--", alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(outpath, dpi=200)
    plt.close()


def save_cum_energy_plot(c_raw, c_cent, outpath, title):
    m = min(len(c_raw), len(c_cent))
    ks = np.arange(1, m + 1)

    plt.figure(figsize=(6.5, 4))
    plt.semilogx(ks, c_raw[:m], label="Raw $G$", linewidth=2)
    plt.semilogx(ks, c_cent[:m], label="Centered $G_c$", linewidth=2)
    plt.xlabel("Singular index $k$ (log)")
    plt.ylabel("Cumulative energy fraction")
    plt.title(title)
    plt.grid(True, which="both", ls="--", alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(outpath, dpi=200)
    plt.close()


def run_one(run_name, act_path, grad_path, outdir, spike_frac):
    X = load_pt_matrix(act_path)
    D = load_pt_matrix(grad_path)
    N, Din = X.shape
    N2, Dout = D.shape
    if N2 != N:
        raise ValueError(f"N mismatch: X {X.shape}, Delta {D.shape}")

    # raw gradient matrix
    G_raw = weight_grad(D, X)

    # mean-centered activation gradient matrix
    mu = X.mean(axis=0, keepdims=True)
    Xc = X - mu
    G_cent = weight_grad(D, Xc)

    # summaries
    s_raw = spectrum_summary(G_raw, spike_frac=spike_frac)
    s_cent = spectrum_summary(G_cent, spike_frac=spike_frac)

    # plots
    k_spike = s_raw["k_spike"]  # use raw definition for vertical line
    save_spectrum_plot(
        s_raw["s"], s_cent["s"], k_spike,
        os.path.join(outdir, f"{run_name}_G_spectrum_raw_vs_centered.png"),
        title=f"{run_name}: $G$ spectrum (raw vs centered)"
    )
    save_cum_energy_plot(
        s_raw["cum"], s_cent["cum"],
        os.path.join(outdir, f"{run_name}_G_cum_energy_raw_vs_centered.png"),
        title=f"{run_name}: $G$ cumulative energy"
    )

    # key comparison scalars
    row = {
        "run": run_name,
        "N": N,
        "Din": Din,
        "Dout": Dout,
        "spike_frac": spike_frac,
        "k_spike": k_spike,

        "raw_top1": s_raw["top1"],
        "cent_top1": s_cent["top1"],

        "raw_energy_top_spike": s_raw["energy_top_spike"],
        "cent_energy_top_spike": s_cent["energy_top_spike"],

        "raw_k50": s_raw["k50"],
        "cent_k50": s_cent["k50"],
        "raw_k90": s_raw["k90"],
        "cent_k90": s_cent["k90"],
    }

    return row


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--outdir", default="./sec2_4A_out")
    ap.add_argument("--spike_frac", type=float, default=0.01)
    ap.add_argument("--runs", nargs="+", required=True,
                    help="Each run: name,activation.pt,grad_output.pt")
    args = ap.parse_args()

    os.makedirs(args.outdir, exist_ok=True)

    rows = []
    for spec in args.runs:
        parts = spec.split(",")
        if len(parts) != 3:
            raise ValueError(f"Bad run spec: {spec}. Use name,activation.pt,grad_output.pt")
        run_name, act_path, grad_path = parts
        print(f"[INFO] Running {run_name} ...")
        row = run_one(run_name, act_path, grad_path, args.outdir, args.spike_frac)
        rows.append(row)

    out_csv = os.path.join(args.outdir, "sec2_4A_gradient_spectrum_summary.csv")
    with open(out_csv, "w", newline="") as fp:
        w = csv.DictWriter(fp, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    print(f"[INFO] Saved CSV: {out_csv}")
    print(f"[INFO] Saved figures: {args.outdir}/*_G_spectrum_raw_vs_centered.png and *_G_cum_energy_raw_vs_centered.png")


if __name__ == "__main__":
    main()
