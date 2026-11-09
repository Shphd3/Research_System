#!/usr/bin/env python3
"""Rank sweep for saved real-DCLM feedback logit artifacts."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def nmi(a: np.ndarray, b: np.ndarray) -> float:
    from sklearn.metrics import normalized_mutual_info_score

    return float(normalized_mutual_info_score(a, b))


def top_eigvecs_sym(matrix: np.ndarray, k: int) -> np.ndarray:
    sym = 0.5 * (matrix + matrix.T)
    vals, vecs = np.linalg.eigh(sym)
    order = np.argsort(vals)[::-1]
    return vecs[:, order[:k]]


def projector(u: np.ndarray) -> np.ndarray:
    return u @ u.T


def random_basis(seed: int, d: int, k: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    q, _ = np.linalg.qr(rng.normal(size=(d, k)))
    return q[:, :k]


def route_nmi(logits: np.ndarray, labels: np.ndarray) -> float:
    return nmi(labels.astype(np.int64), np.argmax(logits, axis=1).astype(np.int64))


def parse_artifact(path: Path) -> tuple[int, int, int]:
    # .../seed_0/step_00005/layer_4_gate_logits.npz
    seed = int(path.parents[1].name.split("_")[1])
    step = int(path.parent.name.split("_")[1])
    layer = int(path.stem.split("_")[1])
    return seed, step, layer


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--ranks", type=int, nargs="+", default=[1, 2, 3, 4, 5, 6, 7])
    parser.add_argument("--min-full-drop", type=float, default=0.05)
    args = parser.parse_args()

    artifact_root = args.run_dir / "artifacts/gate_logits"
    files = sorted(artifact_root.glob("seed_*/step_*/layer_*_gate_logits.npz"))
    grouped: dict[tuple[int, int], dict[int, Path]] = {}
    for path in files:
        seed, step, layer = parse_artifact(path)
        grouped.setdefault((seed, layer), {})[step] = path

    rows: list[dict[str, object]] = []
    for (seed, layer), by_step in sorted(grouped.items()):
        if 0 not in by_step:
            continue
        base = np.load(by_step[0])
        z0 = base["logits"].astype(np.float32)
        labels = base["proxy_labels"].astype(np.int64)
        nmi0 = route_nmi(z0, labels)
        for step, path in sorted(by_step.items()):
            if step == 0:
                continue
            cur = np.load(path)
            zt = cur["logits"].astype(np.float32)
            dz = zt - z0
            nmi_full = route_nmi(zt, labels)
            full_drop = nmi0 - nmi_full
            denom_valid = full_drop >= args.min_full_drop
            denom = full_drop if denom_valid else 1.0
            for rank in args.ranks:
                rank_eff = min(rank, dz.shape[1])
                basis = top_eigvecs_sym((dz.T @ dz) / dz.shape[0], rank_eff)
                p = projector(basis)
                rand = random_basis(seed=900_000 + seed * 1009 + layer * 53 + step * 7 + rank, d=dz.shape[1], k=rank_eff)
                p_rand = projector(rand)
                z_fb = z0 + dz @ p
                z_res = z0 + dz - dz @ p
                z_rand_fb = z0 + dz @ p_rand
                z_rand_res = z0 + dz - dz @ p_rand
                rows.append(
                    {
                        "seed": seed,
                        "layer": layer,
                        "step": step,
                        "rank": rank_eff,
                        "step0_proxy_nmi": nmi0,
                        "full_proxy_nmi": nmi_full,
                        "full_nmi_drop": full_drop,
                        "denominator_valid": denom_valid,
                        "feedback_only_proxy_nmi": route_nmi(z_fb, labels),
                        "residual_only_proxy_nmi": route_nmi(z_res, labels),
                        "random_feedback_only_proxy_nmi": route_nmi(z_rand_fb, labels),
                        "random_residual_only_proxy_nmi": route_nmi(z_rand_res, labels),
                    }
                )

    for row in rows:
        denom = float(row["full_nmi_drop"]) if bool(row["denominator_valid"]) else 1.0
        row["drop_explained"] = (float(row["step0_proxy_nmi"]) - float(row["feedback_only_proxy_nmi"])) / denom
        row["removal_rescue"] = (float(row["residual_only_proxy_nmi"]) - float(row["full_proxy_nmi"])) / denom
        row["random_drop_explained"] = (float(row["step0_proxy_nmi"]) - float(row["random_feedback_only_proxy_nmi"])) / denom
        row["random_removal_rescue"] = (float(row["random_residual_only_proxy_nmi"]) - float(row["full_proxy_nmi"])) / denom

    valid = [row for row in rows if bool(row["denominator_valid"])]
    summary_rows: list[dict[str, object]] = []
    for rank in sorted({int(row["rank"]) for row in valid}):
        rr = [row for row in valid if int(row["rank"]) == rank]
        out: dict[str, object] = {"rank": rank, "valid_cells": len(rr)}
        for metric in ["drop_explained", "removal_rescue", "random_drop_explained", "random_removal_rescue"]:
            vals = np.array([float(row[metric]) for row in rr])
            out[f"{metric}_mean"] = float(vals.mean())
            out[f"{metric}_std"] = float(vals.std(ddof=1)) if vals.size > 1 else 0.0
        out["pass"] = (
            len(rr) >= 3
            and float(out["drop_explained_mean"]) >= 0.5
            and float(out["removal_rescue_mean"]) >= 0.5
            and float(out["drop_explained_mean"]) >= float(out["random_drop_explained_mean"]) + 0.2
            and float(out["removal_rescue_mean"]) >= float(out["random_removal_rescue_mean"]) + 0.2
        )
        summary_rows.append(out)

    write_csv(args.run_dir / "tables/real_feedback_logit_rank_sweep_scores.csv", rows)
    write_csv(args.run_dir / "tables/real_feedback_logit_rank_sweep_summary.csv", summary_rows)
    with (args.run_dir / "tables/real_feedback_logit_rank_sweep_summary.json").open("w", encoding="utf-8") as f:
        json.dump({"summary": summary_rows}, f, indent=2)

    if summary_rows:
        ranks = [int(row["rank"]) for row in summary_rows]
        explain = [float(row["drop_explained_mean"]) for row in summary_rows]
        rescue = [float(row["removal_rescue_mean"]) for row in summary_rows]
        random_explain = [float(row["random_drop_explained_mean"]) for row in summary_rows]
        plt.figure(figsize=(8, 4.5))
        plt.plot(ranks, explain, marker="o", label="feedback explain")
        plt.plot(ranks, rescue, marker="o", label="feedback removal rescue")
        plt.plot(ranks, random_explain, marker="o", label="random explain")
        plt.axhline(0.5, color="black", linestyle="--", linewidth=0.8)
        plt.xlabel("feedback logit rank")
        plt.ylabel("fraction of full NMI drop")
        plt.title("Real-DCLM feedback logit rank sweep")
        plt.legend(fontsize=8)
        plt.tight_layout()
        fig_dir = args.run_dir / "figures"
        fig_dir.mkdir(parents=True, exist_ok=True)
        plt.savefig(fig_dir / "real_feedback_logit_rank_sweep.png", dpi=170)
        plt.close()

    print(json.dumps({"run_dir": str(args.run_dir), "summary": summary_rows}, indent=2))


if __name__ == "__main__":
    main()
