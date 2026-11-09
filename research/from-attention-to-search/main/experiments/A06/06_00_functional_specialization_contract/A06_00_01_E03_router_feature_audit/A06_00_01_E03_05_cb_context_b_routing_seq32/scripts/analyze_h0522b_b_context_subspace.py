#!/usr/bin/env python3
"""Post-hoc B-context geometry/subspace analysis for H0522b."""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
from collections import Counter, defaultdict
from pathlib import Path

os.environ.setdefault("PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION", "python")
os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib")

import torch
from torch.nn import functional as F

from run_h0521b_seq32_contiguous_ab import MoETinyTransformer, load_json, project_root, resolve_output, write_csv, write_json
from run_h0522b_cb_context_b_routing_seq32 import B_CONTEXT_ROLES, SOURCE_ROLES, generate_dataset


DIRECTION_NAMES = ["B_identity", "AB_context", "CB_context", "AB_vs_CB"]
PAIR_NAMES = [
    ("B_in_B_only", "B_in_AB"),
    ("B_in_B_only", "B_in_CB"),
    ("B_in_AB", "B_in_CB"),
]


def load_model(cfg: dict, run_dir: Path, seed: int, device: torch.device) -> MoETinyTransformer:
    model = MoETinyTransformer(int(cfg["data"]["vocab_size"]), cfg["model"]).to(device)
    ckpt_path = run_dir / "moe_top1_no_lb" / f"seed_{seed}" / "model.pt"
    ckpt = torch.load(ckpt_path, map_location=device)
    model.load_state_dict(ckpt["model_state"])
    model.eval()
    return model


def cosine(a: torch.Tensor, b: torch.Tensor) -> float:
    if float(a.norm()) == 0.0 or float(b.norm()) == 0.0:
        return math.nan
    return float(F.cosine_similarity(a, b, dim=0).item())


def projection_score(v: torch.Tensor, basis: torch.Tensor) -> float:
    if float(v.norm()) == 0.0 or basis.numel() == 0:
        return math.nan
    coeff = basis @ v
    return float((coeff.pow(2).sum() / v.pow(2).sum()).item())


def collect_seed_records(model: MoETinyTransformer, data, cfg: dict, device: torch.device, seed: int) -> list[dict]:
    rows: list[dict] = []
    batch_size = int(cfg["evaluation"]["batch_size"])
    with torch.no_grad():
        for start in range(0, data.x.shape[0], batch_size):
            x = data.x[start : start + batch_size].to(device)
            classes = data.classes[start : start + batch_size]
            motif_positions = data.motif_positions[start : start + batch_size]
            records = data.source_records[start : start + batch_size]
            _, info = model(x, return_acts=True)
            reps = info["ffn_input"].detach().cpu()
            experts = info["expert_idx"].detach().cpu()
            router_logits = info["router_logits"].detach().cpu()
            for local_i, cls in enumerate(classes):
                for rec in records[local_i]:
                    pos = int(rec["position"])
                    rows.append(
                        {
                            "seed": seed,
                            "class": cls,
                            "motif_position": motif_positions[local_i],
                            "source_position": pos,
                            "source_identity": str(rec["source_identity"]),
                            "source_role": str(rec["source_role"]),
                            "expert": int(experts[local_i, pos].item()),
                            "hidden": reps[local_i, pos].clone(),
                            "router_logits": router_logits[local_i, pos].clone(),
                        }
                    )
    return rows


def mean_hidden(rows: list[dict], predicate) -> torch.Tensor:
    xs = [row["hidden"] for row in rows if predicate(row)]
    if not xs:
        raise ValueError("empty mean_hidden selection")
    return torch.stack(xs).mean(dim=0)


def role_counter(rows: list[dict], role: str) -> Counter[int]:
    c: Counter[int] = Counter()
    for row in rows:
        if row["source_role"] == role:
            c[int(row["expert"])] += 1
    return c


def dominant_expert(rows: list[dict], role: str) -> int:
    c = role_counter(rows, role)
    return int(c.most_common(1)[0][0]) if c else -1


def analyze_seed(seed: int, cfg: dict, run_dir: Path, device: torch.device) -> dict[str, list[dict]]:
    model = load_model(cfg, run_dir, seed, device)
    eval_data = generate_dataset(cfg, seed, "eval", int(cfg["data"]["eval_samples_per_class"]))
    rows = collect_seed_records(model, eval_data, cfg, device, seed)

    role_means = {role: mean_hidden(rows, lambda r, role=role: r["source_role"] == role) for role in B_CONTEXT_ROLES}
    background_mean = mean_hidden(rows, lambda r: r["source_identity"] == "background")
    all_b_mean = mean_hidden(rows, lambda r: r["source_role"] in B_CONTEXT_ROLES)
    directions = {
        "B_identity": all_b_mean - background_mean,
        "AB_context": role_means["B_in_AB"] - role_means["B_in_B_only"],
        "CB_context": role_means["B_in_CB"] - role_means["B_in_B_only"],
        "AB_vs_CB": role_means["B_in_AB"] - role_means["B_in_CB"],
    }

    centroid_rows = []
    for left, right in PAIR_NAMES:
        centroid_rows.append(
            {
                "seed": seed,
                "left": left,
                "right": right,
                "centroid_cosine": cosine(role_means[left], role_means[right]),
                "centroid_l2_distance": float((role_means[left] - role_means[right]).norm().item()),
                "left_dominant_expert": dominant_expert(rows, left),
                "right_dominant_expert": dominant_expert(rows, right),
            }
        )

    router_w = model.moe.router.weight.detach().cpu()
    boundary_rows = []
    for left, right in PAIR_NAMES:
        direction = role_means[right] - role_means[left]
        left_dom = dominant_expert(rows, left)
        right_dom = dominant_expert(rows, right)
        dom_boundary = router_w[right_dom] - router_w[left_dom] if left_dom >= 0 and right_dom >= 0 else torch.zeros_like(direction)
        vals = []
        for i in range(router_w.shape[0]):
            for j in range(router_w.shape[0]):
                if i == j:
                    continue
                vals.append(abs(cosine(direction, router_w[j] - router_w[i])))
        boundary_rows.append(
            {
                "seed": seed,
                "comparison": f"{left}_to_{right}",
                "left_dominant_expert": left_dom,
                "right_dominant_expert": right_dom,
                "same_dominant_expert": int(left_dom == right_dom),
                "dominant_boundary_cosine": cosine(direction, dom_boundary) if left_dom != right_dom else math.nan,
                "dominant_boundary_logit_delta": float(torch.dot(dom_boundary, direction).item()) if left_dom != right_dom else math.nan,
                "max_abs_any_boundary_cosine": max(vals) if vals else math.nan,
                "direction_norm": float(direction.norm().item()),
            }
        )

    subspace_rows = []
    num_experts = int(cfg["model"]["num_experts"])
    for expert in range(num_experts):
        hs = [row["hidden"] for row in rows if int(row["expert"]) == expert]
        if len(hs) < 4:
            continue
        x = torch.stack(hs)
        x = x - x.mean(dim=0, keepdim=True)
        _, _, vh = torch.linalg.svd(x, full_matrices=False)
        for rank in [1, 2, 4, 8]:
            basis = vh[: min(rank, vh.shape[0])]
            for name in DIRECTION_NAMES:
                subspace_rows.append(
                    {
                        "seed": seed,
                        "expert": expert,
                        "rank": rank,
                        "direction": name,
                        "projection_score": projection_score(directions[name], basis),
                        "num_tokens_in_expert": len(hs),
                    }
                )

    direction_rows = [
        {
            "seed": seed,
            "direction": name,
            "norm": float(vec.norm().item()),
            "cos_to_B_identity": cosine(vec, directions["B_identity"]),
        }
        for name, vec in directions.items()
    ]

    compact_rows = []
    for role in B_CONTEXT_ROLES:
        c = role_counter(rows, role)
        total = sum(c.values())
        for expert in range(int(cfg["model"]["num_experts"])):
            compact_rows.append(
                {
                    "seed": seed,
                    "source_role": role,
                    "expert": expert,
                    "fraction": c[expert] / total if total else 0.0,
                    "count": c[expert],
                }
            )

    return {
        "centroid": centroid_rows,
        "boundary": boundary_rows,
        "subspace": subspace_rows,
        "directions": direction_rows,
        "b_context_matrix": compact_rows,
    }


def plot_outputs(out_dir: Path, fig_dir: Path, cfg: dict) -> None:
    import matplotlib.pyplot as plt

    fig_dir.mkdir(parents=True, exist_ok=True)
    seeds = [int(s) for s in cfg["seeds"]]
    experts = list(range(int(cfg["model"]["num_experts"])))

    def read_rows(name: str) -> list[dict]:
        with (out_dir / name).open("r", encoding="utf-8") as f:
            return list(csv.DictReader(f))

    subspace = read_rows("b_context_expert_subspace_projection_by_seed.csv")
    fig, axes = plt.subplots(1, len(seeds), figsize=(13.5, 3.4), sharey=True)
    for ax, seed in zip(axes, seeds):
        mat = torch.zeros(len(DIRECTION_NAMES), len(experts))
        for row in subspace:
            if int(row["seed"]) == seed and int(row["rank"]) == 4:
                mat[DIRECTION_NAMES.index(row["direction"]), int(row["expert"])] = float(row["projection_score"])
        im = ax.imshow(mat.numpy(), cmap="viridis", vmin=0, vmax=1, aspect="auto")
        ax.set_title(str(seed), fontsize=10)
        ax.set_xticks(range(len(experts)), [f"E{i}" for i in experts])
        ax.set_yticks(range(len(DIRECTION_NAMES)), DIRECTION_NAMES if ax is axes[0] else [])
        for i in range(mat.shape[0]):
            for j in range(mat.shape[1]):
                val = float(mat[i, j])
                ax.text(j, i, f"{val:.2f}", ha="center", va="center", fontsize=7, color="white" if val > 0.5 else "black")
    fig.suptitle("B-context direction projection onto expert top-4 subspaces", fontsize=12)
    fig.subplots_adjust(right=0.93, left=0.11, top=0.78, bottom=0.18, wspace=0.12)
    cbar_ax = fig.add_axes([0.945, 0.18, 0.012, 0.60])
    fig.colorbar(im, cax=cbar_ax, label="projection score")
    fig.savefig(fig_dir / "b_context_expert_subspace_projection_rank4_by_seed.png", dpi=200)
    plt.close(fig)

    centroid = read_rows("b_context_centroid_cosine_by_seed.csv")
    labels = B_CONTEXT_ROLES
    fig, axes = plt.subplots(1, len(seeds), figsize=(12.5, 3.2), sharey=True)
    for ax, seed in zip(axes, seeds):
        mat = torch.eye(len(labels))
        for row in centroid:
            if int(row["seed"]) == seed:
                i = labels.index(row["left"])
                j = labels.index(row["right"])
                mat[i, j] = mat[j, i] = float(row["centroid_cosine"])
        im = ax.imshow(mat.numpy(), cmap="magma", vmin=0, vmax=1, aspect="auto")
        ax.set_title(str(seed), fontsize=10)
        ax.set_xticks(range(len(labels)), ["B-only", "AB", "CB"], rotation=30, ha="right")
        ax.set_yticks(range(len(labels)), ["B-only", "AB", "CB"] if ax is axes[0] else [])
        for i in range(mat.shape[0]):
            for j in range(mat.shape[1]):
                val = float(mat[i, j])
                ax.text(j, i, f"{val:.2f}", ha="center", va="center", fontsize=8, color="white" if val < 0.55 else "black")
    fig.suptitle("B-context hidden centroid cosine by seed", fontsize=12)
    fig.subplots_adjust(right=0.93, left=0.10, top=0.78, bottom=0.22, wspace=0.15)
    cbar_ax = fig.add_axes([0.945, 0.22, 0.012, 0.56])
    fig.colorbar(im, cax=cbar_ax, label="cosine")
    fig.savefig(fig_dir / "b_context_centroid_cosine_by_seed.png", dpi=200)
    plt.close(fig)

    boundary = read_rows("b_context_router_boundary_alignment_by_seed.csv")
    comparisons = [f"{a}_to_{b}" for a, b in PAIR_NAMES]
    fig, ax = plt.subplots(figsize=(8.8, 3.2))
    mat = torch.zeros(len(seeds), len(comparisons))
    for si, seed in enumerate(seeds):
        for ci, comp in enumerate(comparisons):
            row = next(r for r in boundary if int(r["seed"]) == seed and r["comparison"] == comp)
            val = row["dominant_boundary_cosine"]
            mat[si, ci] = float(val) if val not in ("", "nan") and val == val else math.nan
    im = ax.imshow(mat.numpy(), cmap="coolwarm", vmin=-1, vmax=1, aspect="auto")
    ax.set_yticks(range(len(seeds)), [str(s) for s in seeds])
    ax.set_xticks(range(len(comparisons)), ["B-only->AB", "B-only->CB", "AB->CB"], rotation=25, ha="right")
    ax.set_title("Dominant router-boundary alignment for B-context splits")
    for i in range(mat.shape[0]):
        for j in range(mat.shape[1]):
            val = float(mat[i, j])
            text = "same" if math.isnan(val) else f"{val:.2f}"
            ax.text(j, i, text, ha="center", va="center", fontsize=8)
    fig.colorbar(im, ax=ax, label="cosine")
    fig.tight_layout()
    fig.savefig(fig_dir / "b_context_router_boundary_alignment_by_seed.png", dpi=200)
    plt.close(fig)


def run(args: argparse.Namespace) -> None:
    cfg = load_json(args.config)
    root = project_root()
    base_run_dir = resolve_output(root, cfg["output"]["result_dir"], args.base_run_name)
    out_dir = resolve_output(root, "active/synthetic_data_understanding/results/h0522b_cb_context_subspace_analysis", args.run_name)
    fig_dir = resolve_output(root, "active/synthetic_data_understanding/figures/h0522b_cb_context_subspace_analysis", args.run_name)
    out_dir.mkdir(parents=True, exist_ok=True)
    fig_dir.mkdir(parents=True, exist_ok=True)
    write_json(out_dir / "resolved_config.json", cfg)

    all_rows: dict[str, list[dict]] = defaultdict(list)
    seeds = [int(s) for s in cfg["seeds"]]
    device_count = torch.cuda.device_count() if torch.cuda.is_available() else 0
    for i, seed in enumerate(seeds):
        device = torch.device(f"cuda:{i % device_count}" if device_count else "cpu")
        print(f"analyze seed={seed} device={device}", flush=True)
        rows = analyze_seed(seed, cfg, base_run_dir, device)
        for key, value in rows.items():
            all_rows[key].extend(value)

    write_csv(out_dir / "b_context_centroid_cosine_by_seed.csv", all_rows["centroid"])
    write_csv(out_dir / "b_context_router_boundary_alignment_by_seed.csv", all_rows["boundary"])
    write_csv(out_dir / "b_context_expert_subspace_projection_by_seed.csv", all_rows["subspace"])
    write_csv(out_dir / "b_context_direction_norms_by_seed.csv", all_rows["directions"])
    write_csv(out_dir / "b_context_routing_matrix_by_seed.csv", all_rows["b_context_matrix"])
    plot_outputs(out_dir, fig_dir, cfg)
    summary = {
        "run_name": args.run_name,
        "base_run_name": args.base_run_name,
        "result_dir": str(out_dir),
        "figure_dir": str(fig_dir),
        "outputs": [
            "b_context_centroid_cosine_by_seed.csv",
            "b_context_router_boundary_alignment_by_seed.csv",
            "b_context_expert_subspace_projection_by_seed.csv",
        ],
    }
    write_json(out_dir / "run_summary.json", summary)
    print(json.dumps(summary, indent=2), flush=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--base-run-name", required=True)
    parser.add_argument("--run-name", required=True)
    args = parser.parse_args()
    run(args)


if __name__ == "__main__":
    main()
