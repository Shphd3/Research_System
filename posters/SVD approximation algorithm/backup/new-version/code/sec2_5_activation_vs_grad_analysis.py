import torch
import numpy as np
import matplotlib.pyplot as plt
import argparse
import os

# ----------------------------
# Utilities
# ----------------------------

def load_pt(path):
    x = torch.load(path, map_location="cpu")
    if isinstance(x, (list, tuple)):
        x = x[0]
    return x.detach().cpu().numpy().astype(np.float64)


def compute_mean_spike_tail(X, spike_frac=0.01):
    """
    Decompose X into:
      M      = 1 μ^T
      Spike  = projection onto top-k singular vectors (centered)
      Tail   = remainder
    """

    N, H = X.shape

    # Mean
    mu = X.mean(axis=0)
    M = np.outer(np.ones(N), mu)

    # Centered
    Xc = X - M

    # SVD on centered matrix
    U, s, Vt = np.linalg.svd(Xc, full_matrices=False)
    k = max(1, int(H * spike_frac))
    Vk = Vt[:k].T

    X_spike = Xc @ Vk @ Vk.T
    X_tail  = Xc - X_spike

    return M, X_spike, X_tail


def frob_energy(X):
    return np.sum(X * X)


def outlier_contribution(X, M, Spike, Tail, top_frac=0.001, sample_entries=2_000_000, seed=0):
    """
    For top |X| entries, compute squared contribution shares.
    """

    rng = np.random.default_rng(seed)

    N, H = X.shape
    total_entries = N * H

    # sample entries for efficiency
    idx = rng.integers(0, total_entries, size=sample_entries)
    rows = idx // H
    cols = idx % H

    raw_vals = np.abs(X[rows, cols])

    threshold = np.quantile(raw_vals, 1 - top_frac)

    mask = raw_vals >= threshold
    rows = rows[mask]
    cols = cols[mask]

    # squared shares
    x2 = X[rows, cols]**2
    m2 = M[rows, cols]**2
    s2 = Spike[rows, cols]**2
    t2 = Tail[rows, cols]**2

    total = x2 + 1e-30

    return {
        "mean_share":  m2 / total,
        "spike_share": s2 / total,
        "tail_share":  t2 / total,
    }


# ----------------------------
# Plot 1: Global Energy
# ----------------------------

def plot_energy_bar(act_stats, grad_stats, outdir):

    labels = ["Mean", "Spike", "Tail"]

    fig, axs = plt.subplots(1, 2, figsize=(10, 4))

    # Activation
    axs[0].bar(labels, act_stats)
    axs[0].set_title("Activation energy fraction")
    axs[0].set_ylabel("Fraction of total Frobenius energy")

    # Grad
    axs[1].bar(labels, grad_stats)
    axs[1].set_title("Grad_output energy fraction")

    plt.tight_layout()
    plt.savefig(os.path.join(outdir, "energy_decomposition.png"), dpi=300)
    plt.close()


# ----------------------------
# Plot 2: Outlier Histogram
# ----------------------------

def plot_outlier_hist(act_out, grad_out, outdir):

    fig, axs = plt.subplots(1, 2, figsize=(12, 4))

    bins = np.linspace(0, 1, 50)

    # Activation
    axs[0].hist(act_out["mean_share"], bins=bins, alpha=0.5, label="Mean")
    axs[0].hist(act_out["spike_share"], bins=bins, alpha=0.5, label="Spike")
    axs[0].hist(act_out["tail_share"], bins=bins, alpha=0.5, label="Tail")
    axs[0].set_title("Activation outlier contribution")
    axs[0].set_xlabel("Squared contribution share")
    axs[0].legend()

    # Grad_output
    axs[1].hist(grad_out["mean_share"], bins=bins, alpha=0.5, label="Mean")
    axs[1].hist(grad_out["spike_share"], bins=bins, alpha=0.5, label="Spike")
    axs[1].hist(grad_out["tail_share"], bins=bins, alpha=0.5, label="Tail")
    axs[1].set_title("Grad_output outlier contribution")
    axs[1].set_xlabel("Squared contribution share")
    axs[1].legend()

    plt.tight_layout()
    plt.savefig(os.path.join(outdir, "outlier_contribution_hist.png"), dpi=300)
    plt.close()


# ----------------------------
# Main
# ----------------------------

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--activation", required=True)
    parser.add_argument("--grad_output", required=True)
    parser.add_argument("--outdir", default="./figures_sec2_5")
    parser.add_argument("--spike_frac", type=float, default=0.01)
    parser.add_argument("--top_frac", type=float, default=0.001)
    args = parser.parse_args()

    os.makedirs(args.outdir, exist_ok=True)

    print("[INFO] Loading matrices...")
    X_act  = load_pt(args.activation)
    X_grad = load_pt(args.grad_output)

    print("[INFO] Decomposing activation...")
    M_a, S_a, T_a = compute_mean_spike_tail(X_act, args.spike_frac)

    print("[INFO] Decomposing grad_output...")
    M_g, S_g, T_g = compute_mean_spike_tail(X_grad, args.spike_frac)

    # Global energy fractions
    Ea = frob_energy(X_act)
    Eg = frob_energy(X_grad)

    act_stats = [
        frob_energy(M_a) / Ea,
        frob_energy(S_a) / Ea,
        frob_energy(T_a) / Ea,
    ]

    grad_stats = [
        frob_energy(M_g) / Eg,
        frob_energy(S_g) / Eg,
        frob_energy(T_g) / Eg,
    ]

    plot_energy_bar(act_stats, grad_stats, args.outdir)

    print("[INFO] Computing outlier contributions...")
    act_out  = outlier_contribution(X_act,  M_a, S_a, T_a, args.top_frac)
    grad_out = outlier_contribution(X_grad, M_g, S_g, T_g, args.top_frac)

    plot_outlier_hist(act_out, grad_out, args.outdir)

    print("[DONE] Figures saved to:", args.outdir)


if __name__ == "__main__":
    main()
