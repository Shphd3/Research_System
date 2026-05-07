#!/usr/bin/env python3
"""
Section 2.4 experiments (revised): Long tail is high-dimensional and semantically incoherent.

Main goals:
  (A) Per-token compressibility in the tail eigenbasis (effective support size).
  (B) Incoherence in coefficient space:
      compare cosine similarity of tail-basis coefficients for
        - within-sequence nearby tokens
        - within-sequence far-apart tokens
        - across-sequence tokens

Optional (off by default):
  (C) Support overlap (Jaccard) of dominant tail supports (diagnostic only).
"""

import os, io, math, zipfile, argparse
import numpy as np
import matplotlib.pyplot as plt
import torch


# ----------------------------
# Load activation from your zipped torch.save
# ----------------------------
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


# ----------------------------
# Tail projection and coefficients
# ----------------------------
def project_out_spike(X: np.ndarray, Vt_spike: np.ndarray) -> np.ndarray:
    """
    X: (M,H) tokens
    Vt_spike: (k_s, H) rows are spike right singular vectors v_k^T
    Return X_tail = X - (X V_spike^T) V_spike
    """
    coeff = X @ Vt_spike.T           # (M, k_s)
    X_spike = coeff @ Vt_spike       # (M, H)
    return X - X_spike

def tail_coefficients(X_tail: np.ndarray, Vt_tail: np.ndarray) -> np.ndarray:
    """
    c = X_tail V_tail^T
    X_tail: (M,H), Vt_tail: (H_tail,H) -> (M,H_tail)
    """
    return X_tail @ Vt_tail.T


# ----------------------------
# Effective support / compressibility
# ----------------------------
def effective_support_by_energy(c: np.ndarray, frac: float) -> int:
    e = c * c
    total = float(e.sum()) + 1e-12
    idx = np.argsort(e)[::-1]
    csum = np.cumsum(e[idx]) / total
    k = int(np.searchsorted(csum, frac) + 1)
    return k

def save_support_hist(k90, k95, outpath):
    os.makedirs(os.path.dirname(outpath), exist_ok=True)
    plt.figure()
    plt.hist(k90, bins=50, alpha=0.7, label="k@90% energy")
    plt.hist(k95, bins=50, alpha=0.7, label="k@95% energy")
    plt.xlabel("Effective support size in tail eigenbasis")
    plt.ylabel("Count")
    plt.title("Per-token semantic compressibility (tail basis)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(outpath, dpi=200)
    plt.close()


# ----------------------------
# Coefficient cosine similarity (main incoherence test)
# ----------------------------
def sample_cosines(Cs_norm, seq_ids, pos_ids, npairs, rng, mode, far_gap=256):
    """
    mode:
      - "across": different sequences
      - "within_near": same sequence, |pos_i - pos_j| <= far_gap//8 (default heuristic)
      - "within_far": same sequence, |pos_i - pos_j| >= far_gap
    """
    M = Cs_norm.shape[0]
    out = []

    # helper for drawing pairs until we have enough
    attempts = 0
    target = npairs
    while len(out) < target and attempts < target * 30:
        i = int(rng.integers(0, M))
        j = int(rng.integers(0, M))
        if i == j:
            attempts += 1
            continue

        same_seq = (seq_ids[i] == seq_ids[j])
        dist = abs(int(pos_ids[i]) - int(pos_ids[j]))

        ok = False
        if mode == "across":
            ok = not same_seq
        elif mode == "within_near":
            ok = same_seq and dist <= max(1, far_gap // 8)
        elif mode == "within_far":
            ok = same_seq and dist >= far_gap
        else:
            raise ValueError("unknown mode")

        if ok:
            out.append(float(np.dot(Cs_norm[i], Cs_norm[j])))

        attempts += 1

    return np.asarray(out, dtype=np.float64)


def save_cosine_hist(within_near, within_far, across, outpath):
    os.makedirs(os.path.dirname(outpath), exist_ok=True)
    plt.figure()
    plt.hist(within_near, bins=60, alpha=0.6, label="Within-seq (near)")
    plt.hist(within_far, bins=60, alpha=0.6, label="Within-seq (far)")
    plt.hist(across, bins=60, alpha=0.6, label="Across-seq")
    plt.xlabel("Cosine similarity in tail coefficient space")
    plt.ylabel("Count")
    plt.title("Semantic incoherence in tail basis (coefficient cosine)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(outpath, dpi=200)
    plt.close()


def summarize_vec(x, name):
    return {
        "name": name,
        "n": int(len(x)),
        "mean": float(np.mean(x)) if len(x) else float("nan"),
        "std": float(np.std(x)) if len(x) else float("nan"),
        "p10": float(np.percentile(x, 10)) if len(x) else float("nan"),
        "p50": float(np.percentile(x, 50)) if len(x) else float("nan"),
        "p90": float(np.percentile(x, 90)) if len(x) else float("nan"),
    }


# ----------------------------
# Optional: Support overlap (diagnostic)
# ----------------------------
def support_set(c: np.ndarray, k: int) -> np.ndarray:
    e = c * c
    idx = np.argsort(e)[::-1][:k]
    return np.sort(idx)

def jaccard(a: np.ndarray, b: np.ndarray) -> float:
    i = j = inter = 0
    while i < len(a) and j < len(b):
        if a[i] == b[j]:
            inter += 1; i += 1; j += 1
        elif a[i] < b[j]:
            i += 1
        else:
            j += 1
    union = len(a) + len(b) - inter
    return float(inter / union) if union > 0 else 0.0

def save_overlap_hist(within, across, outpath):
    os.makedirs(os.path.dirname(outpath), exist_ok=True)
    plt.figure()
    plt.hist(within, bins=50, alpha=0.7, label="Within-seq")
    plt.hist(across, bins=50, alpha=0.7, label="Across-seq")
    plt.xlabel("Jaccard overlap of dominant tail supports")
    plt.ylabel("Count")
    plt.title("Support overlap in tail basis (diagnostic only)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(outpath, dpi=200)
    plt.close()


# ----------------------------
# Main
# ----------------------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--zip", type=str, required=True)
    ap.add_argument("--outdir", type=str, default="figures")
    ap.add_argument("--ks", type=int, default=41, help="Spike rank k_s")
    ap.add_argument("--nsample_tokens", type=int, default=2000)
    ap.add_argument("--npairs", type=int, default=20000)
    ap.add_argument("--energy_frac_support", type=float, default=0.90,
                    help="Energy fraction defining support set (diagnostic)")
    ap.add_argument("--far_gap", type=int, default=256,
                    help="Within-seq far distance threshold (in token positions)")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--do_support_overlap", action="store_true",
                    help="Also compute Jaccard support overlap (diagnostic)")
    args = ap.parse_args()

    rng = np.random.default_rng(args.seed)

    # Load a and flatten
    a = load_activation_from_zip(args.zip).astype(np.float64)  # [B,L,H]
    B, L, H = a.shape
    b = to_token_matrix(a)  # (N,H)
    N = b.shape[0]
    print(f"[INFO] Loaded a shape={a.shape}, b shape={b.shape} (N={N}, H={H})")

    # Full SVD for tail eigenbasis
    print("[INFO] Computing full SVD of b (this may take time)...")
    U, S, Vt = np.linalg.svd(b, full_matrices=False)
    print("[INFO] SVD done. Top sigmas:", S[:10])

    ks = min(args.ks, H-1)
    print(f"[INFO] Using spike rank k_s={ks} (tail dim={H-ks})")

    Vt_spike = Vt[:ks, :]      # (ks,H)
    Vt_tail  = Vt[ks:, :]      # (H-ks,H)

    # Sample tokens for tail analysis
    idx_tokens = rng.choice(N, size=min(args.nsample_tokens, N), replace=False)
    Xs = b[idx_tokens, :]  # (M,H)
    M = Xs.shape[0]
    print(f"[INFO] Sampled M={M} tokens for tail-basis analysis")

    # Map sampled token indices -> (seq, pos)
    seq_ids = idx_tokens // L
    pos_ids = idx_tokens % L

    # Project out spike and compute tail coefficients
    Xs_tail = project_out_spike(Xs, Vt_spike)          # (M,H)
    Cs = tail_coefficients(Xs_tail, Vt_tail)           # (M,H-ks)

    # -------------------------
    # Exp 2.4-A: per-token compressibility
    # -------------------------
    k90 = np.empty(M, dtype=np.int32)
    k95 = np.empty(M, dtype=np.int32)

    for i in range(M):
        c = Cs[i]
        k90[i] = effective_support_by_energy(c, 0.90)
        k95[i] = effective_support_by_energy(c, 0.95)

    def summarize_int(arr, name):
        return {
            "name": name,
            "mean": float(np.mean(arr)),
            "median": float(np.median(arr)),
            "p90": float(np.percentile(arr, 90)),
            "p99": float(np.percentile(arr, 99)),
            "max": float(np.max(arr)),
        }

    print("\n=== Per-token compressibility in tail eigenbasis ===")
    print(summarize_int(k90, "k@90% energy"))
    print(summarize_int(k95, "k@95% energy"))
    print(f"[INFO] Tail basis dimension = {H-ks}")

    out_support = os.path.join(args.outdir, "tail_effective_support.png")
    save_support_hist(k90, k95, out_support)
    print("[INFO] Saved:", out_support)

    # -------------------------
    # Exp 2.4-B (revised main): coefficient-space incoherence
    # -------------------------
    Cs_norm = Cs / (np.linalg.norm(Cs, axis=1, keepdims=True) + 1e-12)

    within_near = sample_cosines(Cs_norm, seq_ids, pos_ids, args.npairs, rng,
                                 mode="within_near", far_gap=args.far_gap)
    within_far  = sample_cosines(Cs_norm, seq_ids, pos_ids, args.npairs, rng,
                                 mode="within_far", far_gap=args.far_gap)
    across      = sample_cosines(Cs_norm, seq_ids, pos_ids, args.npairs, rng,
                                 mode="across", far_gap=args.far_gap)

    print("\n=== Tail coefficient cosine similarity (tail eigenbasis) ===")
    print(summarize_vec(within_near, "Within-seq (near)"))
    print(summarize_vec(within_far,  "Within-seq (far)"))
    print(summarize_vec(across,      "Across-seq"))

    out_cos = os.path.join(args.outdir, "tail_coeff_cosine.png")
    save_cosine_hist(within_near, within_far, across, out_cos)
    print("[INFO] Saved:", out_cos)

    # -------------------------
    # Optional diagnostic: support overlap (Jaccard)
    # -------------------------
    if args.do_support_overlap:
        supports = []
        for i in range(M):
            c = Cs[i]
            k_sup = effective_support_by_energy(c, args.energy_frac_support)
            supports.append(support_set(c, k_sup))

        within_overlaps = []
        across_overlaps = []

        for _ in range(args.npairs):
            i = int(rng.integers(0, M))
            j = int(rng.integers(0, M))
            if i == j:
                continue
            if seq_ids[i] == seq_ids[j]:
                within_overlaps.append(jaccard(supports[i], supports[j]))
            else:
                across_overlaps.append(jaccard(supports[i], supports[j]))

        within_overlaps = np.asarray(within_overlaps)
        across_overlaps = np.asarray(across_overlaps)

        print("\n=== Diagnostic: support overlap (Jaccard) ===")
        print(summarize_vec(within_overlaps, "Within-seq Jaccard"))
        print(summarize_vec(across_overlaps, "Across-seq Jaccard"))

        out_overlap = os.path.join(args.outdir, "tail_overlap_jaccard.png")
        save_overlap_hist(within_overlaps, across_overlaps, out_overlap)
        print("[INFO] Saved:", out_overlap)

    print("\n[DONE] Section 2.4 outputs:")
    print("  - tail_effective_support.png  (per-token semantic compressibility)")
    print("  - tail_coeff_cosine.png       (main: coefficient-space incoherence)")
    if args.do_support_overlap:
        print("  - tail_overlap_jaccard.png    (diagnostic only)")
    print(f"Use ks={ks}, far_gap={args.far_gap}, npairs={args.npairs}.")


if __name__ == "__main__":
    main()
