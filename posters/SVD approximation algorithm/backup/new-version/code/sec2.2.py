#!/usr/bin/env python3
import os, io, math, zipfile, argparse
import numpy as np
import matplotlib.pyplot as plt
import torch


# ---------- Load activation from zipped torch.save ----------
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


# ---------- Core metrics ----------
def cumulative_energy(sigmas: np.ndarray) -> np.ndarray:
    # "Spectral energy" is sigma_k^2. Total energy sum sigma^2 = ||X||_F^2.
    s2 = sigmas * sigmas
    return np.cumsum(s2) / (np.sum(s2) + 1e-12)

def energy_at_top_percent(sigmas: np.ndarray, p: float) -> tuple[int, float]:
    r = len(sigmas)
    k = max(1, int(math.ceil(p * r)))
    E = cumulative_energy(sigmas)
    return k, float(E[k - 1])

def k_for_energy(sigmas: np.ndarray, target: float) -> int:
    E = cumulative_energy(sigmas)
    return int(np.searchsorted(E, target) + 1)


# ---------- Plot helpers ----------
def save_spectrum_plot(sigmas: np.ndarray, outpath: str, kmax: int):
    os.makedirs(os.path.dirname(outpath), exist_ok=True)
    kmax = min(kmax, len(sigmas))
    x = np.arange(1, kmax + 1)
    y = sigmas[:kmax]

    plt.figure()
    plt.plot(x, y)
    plt.yscale("log")
    plt.xlabel("Singular component index $k$")
    plt.ylabel(r"Singular value $\sigma_k$ (log scale)")
    plt.title("Spike--tail spectrum of activations")
    plt.tight_layout()
    plt.savefig(outpath, dpi=200)
    plt.close()

def save_cum_energy_plot(
    sigmas: np.ndarray,
    outpath: str,
    kmax: int,
    energy_targets: list[float],
    spike_percents: list[float],
):
    """
    Plots CDF(k) = sum_{i<=k} sigma_i^2 / sum_i sigma_i^2,
    and annotates:
      - horizontal lines at target energies
      - vertical lines at the corresponding k (computed)
      - optional markers for top-p% energy fractions
    """
    os.makedirs(os.path.dirname(outpath), exist_ok=True)

    r = len(sigmas)
    E_full = cumulative_energy(sigmas)

    # Ensure the plot includes all annotated ks
    ks_targets = [(t, k_for_energy(sigmas, t)) for t in energy_targets]
    ks_spike = [(p, max(1, int(math.ceil(p * r)))) for p in spike_percents]
    need_k = max([k for (_, k) in ks_targets] + [k for (_, k) in ks_spike] + [1])
    kmax = int(max(kmax, need_k))
    kmax = min(kmax, r)

    x = np.arange(1, kmax + 1)
    E = E_full[:kmax]

    plt.figure()
    plt.plot(x, E, label="CDF of spectral energy")

    # Horizontal + vertical lines for target energies
    for t, k in ks_targets:
        if k <= kmax:
            plt.axhline(y=t, linestyle="--", linewidth=1)
            plt.axvline(x=k, linestyle="--", linewidth=1)
            # annotate near the intersection
            plt.text(
                k,
                min(0.99, t + 0.02),
                f"{int(t*100)}% @ k={k}",
                fontsize=9,
                rotation=0,
                ha="left",
                va="bottom",
            )

    # Markers for top-p% spike mass
    for p, k in ks_spike:
        if k <= kmax:
            val = float(E_full[k - 1])
            plt.scatter([k], [val], s=20)
            plt.text(
                k,
                max(0.02, val - 0.06),
                f"top {p*100:.1f}% (k={k}): {val:.3f}",
                fontsize=9,
                ha="left",
                va="top",
            )

    plt.xlabel("Singular component index $k$")
    plt.ylabel("Cumulative energy fraction  " + r"$\sum_{i\leq k}\sigma_i^2 / \sum_i \sigma_i^2$")
    plt.ylim(0.0, 1.01)
    plt.title("Cumulative spectral energy")
    plt.tight_layout()
    plt.savefig(outpath, dpi=200)
    plt.close()


# ---------- Main ----------
def parse_float_list(s: str) -> list[float]:
    if s.strip() == "":
        return []
    return [float(x.strip()) for x in s.split(",") if x.strip()]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--zip", type=str, required=True, help="Path to activation zip")
    ap.add_argument("--outdir", type=str, default="figures")
    ap.add_argument("--kmax_plot", type=int, default=1024, help="Base number of components to plot (may be increased for annotations)")
    ap.add_argument("--energy_targets", type=str, default="0.5,0.8,0.9,0.95",
                    help="Comma-separated energy thresholds to annotate on CDF plot")
    ap.add_argument("--spike_percents", type=str, default="0.01,0.015,0.05",
                    help="Comma-separated top-p% (as fractions) to annotate on CDF plot (e.g., 0.01=1%)")
    args = ap.parse_args()

    energy_targets = parse_float_list(args.energy_targets)
    spike_percents = parse_float_list(args.spike_percents)

    # Load & reshape
    A = load_activation_from_zip(args.zip).astype(np.float64)
    B, L, H = A.shape
    X = to_token_matrix(A)
    N = X.shape[0]
    print(f"[INFO] Loaded A shape={A.shape}, flattened X shape={X.shape} (N={N}, H={H})")

    # SVD
    print("[INFO] Computing full SVD of X ...")
    U, S, Vt = np.linalg.svd(X, full_matrices=False)
    r = len(S)
    print(f"[INFO] SVD done. r={r}. Top singular values: {S[:10]}")

    # Quantitative summaries
    print("\n=== Spike--tail summary (energy = sigma^2, total = ||X||_F^2) ===")
    for p in spike_percents:
        k, Ek = energy_at_top_percent(S, p)
        print(f"Top {p*100:.1f}% (k={k}) energy fraction: {Ek:.6f}")

    for t in energy_targets:
        k = k_for_energy(S, t)
        print(f"k for {int(t*100)}% energy: {k}")

    # Save figures
    out_spectrum = os.path.join(args.outdir, "spectrum_spike_tail.png")
    out_cum = os.path.join(args.outdir, "spectrum_cum_energy.png")
    save_spectrum_plot(S, out_spectrum, kmax=min(args.kmax_plot, r))
    save_cum_energy_plot(
        S,
        out_cum,
        kmax=min(args.kmax_plot, r),
        energy_targets=energy_targets,
        spike_percents=spike_percents,
    )
    print(f"\n[INFO] Saved figures:\n  {out_spectrum}\n  {out_cum}")

if __name__ == "__main__":
    main()
