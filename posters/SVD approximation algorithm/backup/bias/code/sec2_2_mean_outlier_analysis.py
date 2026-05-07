#!/usr/bin/env python3
import argparse
import numpy as np
import torch
import os
import matplotlib.pyplot as plt


def load_matrix(path):
    t = torch.load(path, map_location="cpu")
    X = t.detach().cpu().numpy().astype(np.float64)
    return X


def decompose_activation(X, spike_frac=0.01):
    N, H = X.shape

    mu = X.mean(axis=0)
    M = np.ones((N,1)) @ mu[None,:]

    Xc = X - M

    U, s, Vt = np.linalg.svd(Xc, full_matrices=False)
    k = max(1, int(spike_frac * H))
    Vk = Vt[:k].T

    X_spike = Xc @ Vk @ Vk.T
    X_tail = Xc - X_spike

    return M, X_spike, X_tail


def outlier_analysis(X, M, S, T, sample_entries=2000000, top_frac=0.001, seed=0):
    rng = np.random.default_rng(seed)
    N, H = X.shape

    idx_i = rng.integers(0, N, size=sample_entries)
    idx_j = rng.integers(0, H, size=sample_entries)

    vals = np.abs(X[idx_i, idx_j])
    threshold = np.quantile(vals, 1 - top_frac)

    mask = vals >= threshold

    Xo = X[idx_i[mask], idx_j[mask]]
    Mo = M[idx_i[mask], idx_j[mask]]
    So = S[idx_i[mask], idx_j[mask]]
    To = T[idx_i[mask], idx_j[mask]]

    denom = Xo**2 + 1e-30

    pM = Mo**2 / denom
    pS = So**2 / denom
    pT = To**2 / denom

    return pM, pS, pT


def plot_hist(pM, pS, pT, outdir, name):
    plt.figure(figsize=(7,5))
    bins = np.linspace(0,1,50)
    plt.hist(pM, bins=bins, alpha=0.5, label="Mean")
    plt.hist(pS, bins=bins, alpha=0.5, label="Spike")
    plt.hist(pT, bins=bins, alpha=0.5, label="Tail")
    plt.xlabel("Squared Contribution Share")
    plt.ylabel("Frequency")
    plt.legend()
    plt.title("Outlier Contribution Decomposition")
    plt.tight_layout()
    plt.savefig(os.path.join(outdir, f"{name}_outlier_hist.png"), dpi=200)
    plt.close()


def summarize(pM, pS, pT):
    def stats(x):
        return {
            "mean": float(np.mean(x)),
            "median": float(np.median(x)),
            "p90": float(np.percentile(x,90)),
        }
    return {
        "Mean": stats(pM),
        "Spike": stats(pS),
        "Tail": stats(pT),
        "Dominant_mean": float(np.mean((pM > pS) & (pM > pT))),
        "Dominant_spike": float(np.mean((pS > pM) & (pS > pT))),
        "Dominant_tail": float(np.mean((pT > pM) & (pT > pS))),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--outdir", default="./sec2_2_figures")
    parser.add_argument("--spike_frac", type=float, default=0.01)
    parser.add_argument("--sample_entries", type=int, default=2000000)
    parser.add_argument("--top_frac", type=float, default=0.001)
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args()

    os.makedirs(args.outdir, exist_ok=True)

    X = load_matrix(args.input)

    M, S, T = decompose_activation(X, args.spike_frac)
    pM, pS, pT = outlier_analysis(X, M, S, T,
                                  args.sample_entries,
                                  args.top_frac,
                                  args.seed)

    stats = summarize(pM, pS, pT)

    print("\n=== Outlier Contribution Statistics ===")
    for k,v in stats.items():
        print(k, v)

    plot_hist(pM, pS, pT, args.outdir,
              os.path.basename(args.input))


if __name__ == "__main__":
    main()
