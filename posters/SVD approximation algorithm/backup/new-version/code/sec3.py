#!/usr/bin/env python3
import os, io, math, zipfile, argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import torch


# ----------------------------
# Load activation from zipped torch.save
# ----------------------------
def extract_tensor(obj):
    if torch.is_tensor(obj):
        return obj.detach().cpu().numpy()
    if isinstance(obj, np.ndarray):
        return obj
    if isinstance(obj, dict):
        for v in obj.values():
            if torch.is_tensor(v):
                return v.detach().cpu().numpy()
            if isinstance(v, np.ndarray):
                return v
    if isinstance(obj, (list, tuple)):
        for v in obj:
            out = extract_tensor(v)
            if isinstance(out, np.ndarray):
                return out
    raise RuntimeError("Could not extract numeric tensor from torch.load output.")

def load_activation_from_zip(zip_path: str) -> np.ndarray:
    with zipfile.ZipFile(zip_path, "r") as zf:
        names = zf.namelist()
        if len(names) != 1:
            raise RuntimeError(f"Expected exactly one member in zip, got {names}")
        member = names[0]
        payload = zf.read(member)
    obj = torch.load(io.BytesIO(payload), map_location="cpu")
    A = extract_tensor(obj)
    return np.asarray(A)

def to_token_matrix(A: np.ndarray) -> np.ndarray:
    if A.ndim != 3:
        raise ValueError(f"Expected [B,L,H], got {A.shape}")
    B, L, H = A.shape
    return A.reshape(B * L, H)


# ----------------------------
# Metrics (all energy-based, no explicit HxH projector needed)
# ----------------------------
def frob_norm_sq(X: np.ndarray) -> float:
    return float(np.sum(X * X))

def spike_energy(X: np.ndarray, Vk: np.ndarray) -> float:
    """
    Vk: (k,H) with orthonormal rows (top-k right singular vectors).
    For projector Pk = Vk^T Vk, spike part is XPk.
    Frobenius energy: ||X Pk||_F^2 = ||X Vk^T||_F^2.
    """
    Y = X @ Vk.T  # (N,k)
    return float(np.sum(Y * Y))

def mean_in_spike_fraction(mu: np.ndarray, Vk: np.ndarray) -> float:
    """
    Fraction of mean energy captured by spike subspace span(Vk):
      ||Proj(mu)||^2 / ||mu||^2  with Proj(mu)=Vk^T(Vk mu)
    Using orthonormal rows: ||Vk mu||^2 / ||mu||^2.
    """
    mu2 = float(mu @ mu) + 1e-12
    proj2 = float((Vk @ mu) @ (Vk @ mu))
    return proj2 / mu2

def residual_energy_topk_svd(sigmas: np.ndarray, k: int) -> float:
    """
    Residual energy fraction after removing top-k SVD components:
      sum_{i>k} sigma_i^2 / sum_i sigma_i^2
    """
    s2 = sigmas * sigmas
    total = float(np.sum(s2)) + 1e-12
    kept = float(np.sum(s2[:k]))
    return 1.0 - kept / total


# ----------------------------
# Plot helpers (no custom colors)
# ----------------------------
def save_curve(x, y, outpath, title, xlabel, ylabel, xlog=False):
    os.makedirs(os.path.dirname(outpath), exist_ok=True)
    plt.figure()
    plt.plot(x, y)
    if xlog:
        plt.xscale("log")
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.tight_layout()
    plt.savefig(outpath, dpi=200)
    plt.close()

def save_two_curves(x, y1, y2, labels, outpath, title, xlabel, ylabel, xlog=False):
    os.makedirs(os.path.dirname(outpath), exist_ok=True)
    plt.figure()
    plt.plot(x, y1, label=labels[0])
    plt.plot(x, y2, label=labels[1])
    if xlog:
        plt.xscale("log")
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    plt.tight_layout()
    plt.savefig(outpath, dpi=200)
    plt.close()


# ----------------------------
# Main
# ----------------------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--zip", type=str, required=True, help="Path to activation zip")
    ap.add_argument("--outdir", type=str, default="figures")
    ap.add_argument("--kmax", type=int, default=512, help="Max k to evaluate")
    ap.add_argument("--k_list", type=str, default="1,5,10,41,62,205,512",
                    help="Comma-separated k values for summary table")
    ap.add_argument("--dtype", type=str, default="float64", choices=["float32","float64"])
    args = ap.parse_args()

    # Load & reshape
    A = load_activation_from_zip(args.zip)
    X = to_token_matrix(A)
    X = X.astype(np.float64 if args.dtype == "float64" else np.float32)
    N, H = X.shape
    print(f"[INFO] Loaded X shape={X.shape} (N={N}, H={H}) dtype={X.dtype}")

    # Compute mean and mean-removed matrix
    mu = X.mean(axis=0)
    X_mu = np.ones((N, 1), dtype=X.dtype) @ mu[None, :]
    X_avg = X - X_mu

    # Full SVD once
    print("[INFO] Computing full SVD of X (this may take time)...")
    U, S, Vt = np.linalg.svd(X, full_matrices=False)  # Vt: (H,H)
    print("[INFO] SVD done. Top sigmas:", S[:10])

    # Total energies
    Ex = frob_norm_sq(X)
    Ex_avg = frob_norm_sq(X_avg)

    # Evaluate across k=1..kmax (or up to H)
    kmax = min(args.kmax, H)
    ks = np.arange(1, kmax + 1)

    spike_reduction = np.empty(kmax, dtype=np.float64)
    tail_ratio = np.empty(kmax, dtype=np.float64)
    mean_in_spike = np.empty(kmax, dtype=np.float64)
    svd_residual = np.empty(kmax, dtype=np.float64)

    for k in range(1, kmax + 1):
        Vk = Vt[:k, :]  # (k,H)

        Espike = spike_energy(X, Vk)
        Espike_avg = spike_energy(X_avg, Vk)

        Etail = Ex - Espike
        Etail_avg = Ex_avg - Espike_avg

        spike_reduction[k-1] = 1.0 - (Espike_avg / (Espike + 1e-12))
        tail_ratio[k-1] = (Etail_avg / (Etail + 1e-12))
        mean_in_spike[k-1] = mean_in_spike_fraction(mu, Vk)
        svd_residual[k-1] = residual_energy_topk_svd(S, k)

    # Save figures
    out_spike = os.path.join(args.outdir, "avg_spike_reduction_vs_k.png")
    out_tail  = os.path.join(args.outdir, "avg_tail_preservation_vs_k.png")
    out_mean  = os.path.join(args.outdir, "avg_mean_in_spike_vs_k.png")
    out_resid = os.path.join(args.outdir, "avg_residual_energy_comparison.png")

    save_curve(
        ks, spike_reduction, out_spike,
        title="Spike energy reduction by averaging vs spike-subspace size",
        xlabel="Spike subspace size k",
        ylabel=r"$1 - \|X_{\mathrm{avg}}P_k\|_F^2 / \|XP_k\|_F^2$",
        xlog=True,
    )

    save_curve(
        ks, tail_ratio, out_tail,
        title="Tail energy preservation under averaging vs spike-subspace size",
        xlabel="Spike subspace size k",
        ylabel=r"$\|X_{\mathrm{avg}}(I-P_k)\|_F^2 / \|X(I-P_k)\|_F^2$",
        xlog=True,
    )

    save_curve(
        ks, mean_in_spike, out_mean,
        title="Mean captured by spike subspace",
        xlabel="Spike subspace size k",
        ylabel=r"$\|\mathrm{Proj}_k(\mu)\|_2^2 / \|\mu\|_2^2$",
        xlog=True,
    )

    # Residual energy: averaging vs SVD
    avg_residual = np.full_like(ks, fill_value=(Ex_avg / (Ex + 1e-12)), dtype=np.float64)
    save_two_curves(
        ks, avg_residual, svd_residual,
        labels=["Averaging (mean removal)", "Top-k SVD removal"],
        outpath=out_resid,
        title="Residual energy fraction: averaging vs top-k SVD removal",
        xlabel="k (log scale)",
        ylabel=r"$\|X_{\mathrm{res}}\|_F^2 / \|X\|_F^2$",
        xlog=True,
    )

    print("[INFO] Saved figures:")
    print(" ", out_spike)
    print(" ", out_tail)
    print(" ", out_mean)
    print(" ", out_resid)

    # Summary table at selected k
    k_list = [int(x.strip()) for x in args.k_list.split(",") if x.strip()]
    k_list = [k for k in k_list if 1 <= k <= kmax]
    rows = []
    for k in k_list:
        rows.append({
            "k": k,
            "mean_in_spike": float(mean_in_spike[k-1]),
            "spike_reduction": float(spike_reduction[k-1]),
            "tail_ratio": float(tail_ratio[k-1]),
            "avg_residual_energy": float(Ex_avg / (Ex + 1e-12)),
            "svd_residual_energy": float(svd_residual[k-1]),
        })
    df = pd.DataFrame(rows)
    csv_path = os.path.join(args.outdir, "avg_vs_svd_summary.csv")
    df.to_csv(csv_path, index=False)
    print("\n=== Summary table (saved to CSV) ===")
    print(df.to_string(index=False))
    print("[INFO] Saved:", csv_path)


if __name__ == "__main__":
    main()
