#!/usr/bin/env python3
import os, io, math, zipfile, argparse
import numpy as np
import matplotlib.pyplot as plt
import torch


# =========================
# Load activation
# =========================
def extract_tensor(obj):
    if torch.is_tensor(obj):
        return obj.detach().cpu().numpy()
    if isinstance(obj, np.ndarray):
        return obj
    if isinstance(obj, dict):
        for v in obj.values():
            out = extract_tensor(v)
            if isinstance(out, np.ndarray):
                return out
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


# =========================
# Mean estimators
# =========================
def mean_batch(b: np.ndarray) -> np.ndarray:
    return b.mean(axis=0)

def mean_single_sequence(a: np.ndarray, seq_idx: int = 0) -> np.ndarray:
    return a[seq_idx].mean(axis=0)

def mean_sampled_tokens(a: np.ndarray, samples_per_seq: int, seed: int = 0) -> np.ndarray:
    rng = np.random.default_rng(seed)
    B, L, H = a.shape
    samples = []
    for bb in range(B):
        idx = rng.choice(L, size=min(samples_per_seq, L), replace=False)
        samples.append(a[bb, idx, :])
    S = np.concatenate(samples, axis=0)  # (B*s, H)
    return S.mean(axis=0)


# =========================
# Alignment computation
# =========================
def alignment_curve(U: np.ndarray, Vt: np.ndarray, mu: np.ndarray) -> np.ndarray:
    """
    alpha_k = | <1 mu^T, sigma_k u_k v_k^T>_F | / (||1 mu^T||_F ||sigma_k u_k v_k^T||_F)
            = |(1^T u_k)(mu^T v_k)| / (sqrt(N) ||mu||)
    """
    N = U.shape[0]
    mu = mu.astype(np.float64, copy=False)
    mu_norm = np.linalg.norm(mu) + 1e-12

    ones = np.ones((N,), dtype=np.float64)
    u_sums = U.T @ ones             # (r,)
    mu_dot_v = Vt @ mu              # (r,)

    alpha = np.abs(u_sums * mu_dot_v) / (math.sqrt(N) * mu_norm)
    return alpha

def alignment_cdf(alpha: np.ndarray) -> np.ndarray:
    mass = float(np.sum(alpha)) + 1e-12
    return np.cumsum(alpha) / mass

def proj_mu_fraction(Vt: np.ndarray, mu: np.ndarray, k: int) -> float:
    mu = mu.astype(np.float64, copy=False)
    mu_norm2 = float(mu @ mu) + 1e-12
    Vk = Vt[:k, :]                  # (k,H)
    proj2 = float((Vk @ mu) @ (Vk @ mu))
    return proj2 / mu_norm2


# =========================
# Plot helpers
# =========================
def save_alignment_png(alpha: np.ndarray, outpath: str, title: str, kmax: int, k_spike: int = None):
    os.makedirs(os.path.dirname(outpath), exist_ok=True)
    kmax = min(kmax, len(alpha))
    x = np.arange(1, kmax + 1)
    y = alpha[:kmax]

    plt.figure()
    plt.plot(x, y)
    plt.xscale("log")
    plt.grid(True, which="both", linestyle="--", linewidth=0.5, alpha=0.5)
    if k_spike is not None and k_spike <= kmax:
        plt.axvline(k_spike, linestyle="--", linewidth=1)
        plt.text(k_spike, max(y)*0.8, f"1% k={k_spike}", fontsize=9, ha="left", va="center")
    plt.xlabel("Singular component index $k$ (log scale)")
    plt.ylabel(r"$|\cos(\mathrm{ColMean}_{\mu}(b),\, \sigma_k u_k v_k^\top)|$")
    plt.title(title)
    plt.tight_layout()
    plt.savefig(outpath, dpi=200)
    plt.close()

def save_cdf_png(cdf: np.ndarray, outpath: str, title: str, kmax: int, k_spike: int = None):
    os.makedirs(os.path.dirname(outpath), exist_ok=True)
    kmax = min(kmax, len(cdf))
    x = np.arange(1, kmax + 1)
    y = cdf[:kmax]

    plt.figure()
    plt.plot(x, y)
    plt.xscale("log")
    plt.ylim(0.0, 1.01)
    plt.grid(True, which="both", linestyle="--", linewidth=0.5, alpha=0.5)
    if k_spike is not None and k_spike <= kmax:
        plt.axvline(k_spike, linestyle="--", linewidth=1)
        plt.text(k_spike, 0.9, f"1% k={k_spike}", fontsize=9, ha="left", va="center")
    plt.xlabel("Singular component index $k$ (log scale)")
    plt.ylabel("Cumulative alignment mass")
    plt.title(title)
    plt.tight_layout()
    plt.savefig(outpath, dpi=200)
    plt.close()

def save_three_cdf_png(cdf1, cdf2, cdf3, labels, outpath, title, kmax, k_spike=None):
    os.makedirs(os.path.dirname(outpath), exist_ok=True)
    kmax = min(kmax, len(cdf1), len(cdf2), len(cdf3))
    x = np.arange(1, kmax + 1)

    plt.figure()
    plt.plot(x, cdf1[:kmax], label=labels[0])
    plt.plot(x, cdf2[:kmax], label=labels[1])
    plt.plot(x, cdf3[:kmax], label=labels[2])
    plt.xscale("log")
    plt.ylim(0.0, 1.01)
    plt.grid(True, which="both", linestyle="--", linewidth=0.5, alpha=0.5)
    if k_spike is not None and k_spike <= kmax:
        plt.axvline(k_spike, linestyle="--", linewidth=1)
        plt.text(k_spike, 0.15, f"1% k={k_spike}", fontsize=9, ha="left", va="center")
    plt.xlabel("Singular component index $k$ (log scale)")
    plt.ylabel("Cumulative alignment mass")
    plt.title(title)
    plt.legend()
    plt.tight_layout()
    plt.savefig(outpath, dpi=200)
    plt.close()


# =========================
# Main
# =========================
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--zip", type=str, required=True)
    ap.add_argument("--outdir", type=str, default="figures")
    ap.add_argument("--seq_idx", type=int, default=0)
    ap.add_argument("--samples_per_seq", type=int, default=64)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--kmax_plot", type=int, default=512)
    ap.add_argument("--do_shuffle_baseline", action="store_true",
                    help="Optional control: shuffle tokens and recompute batch-mean alignment/CDF")
    args = ap.parse_args()

    os.makedirs(args.outdir, exist_ok=True)
    rng = np.random.default_rng(args.seed)

    # Load activation a: [B,L,H]
    a = load_activation_from_zip(args.zip).astype(np.float64)
    B, L, H = a.shape
    b = to_token_matrix(a)  # (N,H)
    N = b.shape[0]
    print(f"[INFO] Loaded a shape={a.shape}, b shape={b.shape} (N={N}, H={H})")

    # Compute SVD once
    print("[INFO] Computing full SVD of b ...")
    U, S, Vt = np.linalg.svd(b, full_matrices=False)
    r = len(S)
    print(f"[INFO] SVD done. r={r}. Top sigmas: {S[:10]}")

    k1pct = max(1, int(math.ceil(0.01 * r)))  # 1% spike marker
    print(f"[INFO] 1% spike index k={k1pct}")

    # Means
    mu_batch = mean_batch(b)
    mu_single = mean_single_sequence(a, seq_idx=args.seq_idx)
    mu_sampled = mean_sampled_tokens(a, samples_per_seq=args.samples_per_seq, seed=args.seed)

    # Alignment curves
    alpha_batch = alignment_curve(U, Vt, mu_batch)
    alpha_sampled = alignment_curve(U, Vt, mu_sampled)
    alpha_single = alignment_curve(U, Vt, mu_single)

    # CDFs
    cdf_batch = alignment_cdf(alpha_batch)
    cdf_sampled = alignment_cdf(alpha_sampled)
    cdf_single = alignment_cdf(alpha_single)

    # Print key scalar summaries
    print("\n=== Mean-in-spike-subspace (right-subspace projection) ===")
    for k in [1, 5, 10, k1pct]:
        print(f"Proj_k(mu_batch) fraction: k={k:<4d}: {proj_mu_fraction(Vt, mu_batch, k):.6f}")

    def mass_in_head(alpha, k):
        return float(np.sum(alpha[:k]) / (np.sum(alpha) + 1e-12))

    print("\n=== Alignment mass concentration ===")
    print(f"Batch mean:   mass in top 1%  (k={k1pct}): {mass_in_head(alpha_batch, k1pct):.6f}")
    print(f"Sampled mean: mass in top 1%  (k={k1pct}): {mass_in_head(alpha_sampled, k1pct):.6f}")
    print(f"Single mean:  mass in top 1%  (k={k1pct}): {mass_in_head(alpha_single, k1pct):.6f}")

    # Save alignment plots
    save_alignment_png(alpha_batch,   os.path.join(args.outdir, "col_batch.png"),
                       "Alignment with ColMean (batch mean estimator)", args.kmax_plot, k_spike=k1pct)
    save_alignment_png(alpha_sampled, os.path.join(args.outdir, "col_sampled.png"),
                       f"Alignment with ColMean (sampled tokens, {args.samples_per_seq}/seq)", args.kmax_plot, k_spike=k1pct)
    save_alignment_png(alpha_single,  os.path.join(args.outdir, "col_single.png"),
                       f"Alignment with ColMean (single-sequence mean, seq={args.seq_idx})", args.kmax_plot, k_spike=k1pct)

    # Save CDF plots (per method)
    save_cdf_png(cdf_batch,   os.path.join(args.outdir, "col_batch_cdf.png"),
                 "CDF of ColMean alignment (batch mean)", args.kmax_plot, k_spike=k1pct)
    save_cdf_png(cdf_sampled, os.path.join(args.outdir, "col_sampled_cdf.png"),
                 "CDF of ColMean alignment (sampled tokens)", args.kmax_plot, k_spike=k1pct)
    save_cdf_png(cdf_single,  os.path.join(args.outdir, "col_single_cdf.png"),
                 "CDF of ColMean alignment (single sequence)", args.kmax_plot, k_spike=k1pct)

    # Save one combined CDF plot (compact for paper)
    save_three_cdf_png(
        cdf_batch, cdf_sampled, cdf_single,
        labels=["Batch mean", "Sampled tokens", "Single sequence"],
        outpath=os.path.join(args.outdir, "colmean_alignment_cdf_three_methods.png"),
        title="CDF of ColMean alignment mass under different mean estimators",
        kmax=args.kmax_plot,
        k_spike=k1pct
    )

    # Optional shuffle baseline
    if args.do_shuffle_baseline:
        print("\n[INFO] Running shuffle-baseline control ...")
        perm = rng.permutation(N)
        b_shuf = b[perm, :]
        U2, S2, Vt2 = np.linalg.svd(b_shuf, full_matrices=False)
        mu_shuf = mean_batch(b_shuf)
        alpha_shuf = alignment_curve(U2, Vt2, mu_shuf)
        cdf_shuf = alignment_cdf(alpha_shuf)
        save_alignment_png(alpha_shuf, os.path.join(args.outdir, "col_batch_shuffled.png"),
                           "Alignment with ColMean (batch mean, shuffled tokens)", args.kmax_plot, k_spike=k1pct)
        save_cdf_png(cdf_shuf, os.path.join(args.outdir, "col_batch_shuffled_cdf.png"),
                     "CDF of ColMean alignment (batch mean, shuffled tokens)", args.kmax_plot, k_spike=k1pct)
        print("[INFO] Saved shuffle-baseline figures.")

    print("\n[INFO] Saved figures in:", args.outdir)


if __name__ == "__main__":
    main()
