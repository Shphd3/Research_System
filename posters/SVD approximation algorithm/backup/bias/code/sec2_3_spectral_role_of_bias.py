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


def svd_full(X: np.ndarray):
    # returns singular values and right singular vectors V (H x r)
    U, s, Vt = np.linalg.svd(X, full_matrices=False)
    V = Vt.T
    return s, V


def proj_energy_fraction(X: np.ndarray, V: np.ndarray) -> float:
    """
    Fraction of Frobenius energy captured by projecting X onto span(V):
      ||X V V^T||_F^2 / ||X||_F^2
    """
    Xp = X @ V @ V.T
    num = np.sum(Xp * Xp)
    den = np.sum(X * X) + 1e-30
    return float(num / den)


def projector_distance(V1: np.ndarray, V2: np.ndarray) -> float:
    """
    Frobenius norm of difference between projectors:
      ||V1V1^T - V2V2^T||_F
    """
    P1 = V1 @ V1.T
    P2 = V2 @ V2.T
    return float(np.linalg.norm(P1 - P2, ord="fro"))


def principal_angles(V1: np.ndarray, V2: np.ndarray):
    """
    Principal angles between subspaces span(V1) and span(V2).
    Return cosines (singular values of V1^T V2) and angles in degrees.
    """
    M = V1.T @ V2
    sig = np.linalg.svd(M, compute_uv=False)
    sig = np.clip(sig, 0.0, 1.0)
    ang = np.arccos(sig) * 180.0 / np.pi
    return sig, ang


def save_spectrum_plot(s_raw, s_cent, k, outpath, title):
    m = min(len(s_raw), len(s_cent))
    ks = np.arange(1, m + 1)

    plt.figure(figsize=(6.5, 4))
    plt.loglog(ks, s_raw[:m], label="Raw $X$", linewidth=2)
    plt.loglog(ks, s_cent[:m], label="Centered $X_c$", linewidth=2)
    plt.axvline(k, linestyle="--", linewidth=1.5)
    plt.xlabel("Singular index $k$ (log)")
    plt.ylabel("Singular value $\\sigma_k$ (log)")
    plt.title(title)
    plt.grid(True, which="both", ls="--", alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(outpath, dpi=200)
    plt.close()


def save_cum_energy_plot(s_raw, s_cent, outpath, title):
    e_raw = s_raw * s_raw
    e_cent = s_cent * s_cent

    c_raw = np.cumsum(e_raw) / (np.sum(e_raw) + 1e-30)
    c_cent = np.cumsum(e_cent) / (np.sum(e_cent) + 1e-30)

    ks = np.arange(1, len(s_raw) + 1)

    plt.figure(figsize=(6.5, 4))
    plt.semilogx(ks, c_raw, label="Raw $X$", linewidth=2)
    plt.semilogx(ks, c_cent, label="Centered $X_c$", linewidth=2)
    plt.xlabel("Singular index $k$ (log)")
    plt.ylabel("Cumulative energy fraction")
    plt.title(title)
    plt.grid(True, which="both", ls="--", alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(outpath, dpi=200)
    plt.close()


def run_one(name: str, X: np.ndarray, spike_frac: float, outdir: str):
    N, H = X.shape
    mu = X.mean(axis=0, keepdims=True)
    Xc = X - mu

    k = max(1, int(np.ceil(spike_frac * H)))

    # SVDs
    s_raw, V_raw = svd_full(X)
    s_cent, V_cent = svd_full(Xc)

    V_raw_k = V_raw[:, :k]
    V_cent_k = V_cent[:, :k]

    # 2.3-A: spike energy fractions
    spike_frac_raw_in_rawbasis = proj_energy_fraction(X, V_raw_k)
    spike_frac_cent_in_rawbasis = proj_energy_fraction(Xc, V_raw_k)

    # How much of raw spike energy is removed by mean-centering (in raw spike basis)?
    # This answers: how much of the spike energy is attributable to the mean component.
    spike_energy_reduction = 1.0 - (spike_frac_cent_in_rawbasis / (spike_frac_raw_in_rawbasis + 1e-30))

    # Also report global mean energy fraction in raw X
    mean_energy_frac = float(np.sum(mu * mu) * N / (np.sum(X * X) + 1e-30))
    # (since ||M||_F^2 = N||mu||^2)

    # 2.3-C: subspace similarity raw spike vs centered spike
    proj_dist = projector_distance(V_raw_k, V_cent_k)
    cosines, angles = principal_angles(V_raw_k, V_cent_k)
    min_cos = float(np.min(cosines))
    mean_cos = float(np.mean(cosines))
    max_angle = float(np.max(angles))

    # Plots (2.3-B)
    save_spectrum_plot(
        s_raw, s_cent, k,
        os.path.join(outdir, f"{name}_spectrum_raw_vs_centered.png"),
        title=f"{name}: singular spectrum (raw vs centered)"
    )
    save_cum_energy_plot(
        s_raw, s_cent,
        os.path.join(outdir, f"{name}_cum_energy_raw_vs_centered.png"),
        title=f"{name}: cumulative spectral energy"
    )

    # Return summary row
    row = {
        "run": name,
        "N": N,
        "H": H,
        "k_spike": k,
        "mean_energy_frac_raw": mean_energy_frac,
        "spike_energy_frac_raw_basis_rawX": spike_frac_raw_in_rawbasis,
        "spike_energy_frac_raw_basis_centeredX": spike_frac_cent_in_rawbasis,
        "spike_energy_reduction_by_centering": spike_energy_reduction,
        "proj_dist_Pk_raw_vs_centered": proj_dist,
        "principal_cos_min": min_cos,
        "principal_cos_mean": mean_cos,
        "principal_angle_max_deg": max_angle,
        "sigma1_raw": float(s_raw[0]),
        "sigma1_centered": float(s_cent[0]),
        "sigma_k_raw": float(s_raw[k-1]),
        "sigma_k_centered": float(s_cent[k-1]),
    }
    return row


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base_dir", default=".")
    ap.add_argument("--outdir", default="./sec2_3_out")
    ap.add_argument("--spike_frac", type=float, default=0.01)
    ap.add_argument("--runs", nargs="+", required=True,
                    help="Each run: name,file.pt (activation only here)")
    args = ap.parse_args()

    os.makedirs(args.outdir, exist_ok=True)
    figdir = os.path.join(args.outdir, "figures")
    os.makedirs(figdir, exist_ok=True)

    rows = []
    for spec in args.runs:
        parts = spec.split(",")
        if len(parts) != 2:
            raise ValueError(f"Bad run spec: {spec}. Use name,file.pt")
        name, f = parts
        path = os.path.join(args.base_dir, f)
        X = load_pt_matrix(path)
        print(f"[INFO] Running {name} on {f} shape={X.shape}")
        row = run_one(name, X, args.spike_frac, figdir)
        rows.append(row)

    out_csv = os.path.join(args.outdir, "sec2_3_spectral_role_summary.csv")
    with open(out_csv, "w", newline="") as fp:
        w = csv.DictWriter(fp, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    print(f"[INFO] Saved CSV: {out_csv}")
    print(f"[INFO] Saved figures: {figdir}/<run>_spectrum_raw_vs_centered.png and <run>_cum_energy_raw_vs_centered.png")


if __name__ == "__main__":
    main()
