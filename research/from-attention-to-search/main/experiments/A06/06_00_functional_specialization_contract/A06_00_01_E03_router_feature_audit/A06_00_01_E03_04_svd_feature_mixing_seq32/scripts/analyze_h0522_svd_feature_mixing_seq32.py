#!/usr/bin/env python3
"""Post-training SVD feature-mixing analysis for H0522."""

from __future__ import annotations

import argparse
import csv
import importlib.util
import json
import math
import os
import random
import sys
from collections import Counter, defaultdict
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib")
os.environ.setdefault("PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION", "python")

import matplotlib.pyplot as plt
import torch
import torch.nn.functional as F


CLASS_ORDER = ["background", "A_only", "B_only", "AB_composite"]
FEATURES = ["v_A", "v_B", "v_AB_raw", "v_AB_int"]
RANKS = [1, 2, 4, 8, 16]


def write_json(path: Path, data: dict | list) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def write_csv(path: Path, rows: list[dict], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_h0521b_runner(repo_root: Path):
    script = (
        repo_root
        / "XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/scripts/run_h0521b_seq32_contiguous_ab.py"
    )
    spec = importlib.util.spec_from_file_location("h0521b_runner", script)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load runner from {script}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def background_tokens(cfg: dict) -> list[int]:
    start = int(cfg["data"].get("background_token_start", 10))
    return list(range(start, int(cfg["data"]["vocab_size"])))


def generate_fixed_eval(cfg: dict, seed: int, n_per_class: int, motif_position: int):
    rng = random.Random(seed + 2026052201)
    seq_len = int(cfg["data"]["seq_len"])
    if motif_position < 0 or motif_position >= seq_len - 1:
        raise ValueError("motif_position must allow a two-token motif")
    token_cfg = cfg["data"]["tokens"]
    token_a = int(token_cfg["A"])
    token_b = int(token_cfg["B"])
    y_a = int(token_cfg["y_A"])
    y_b = int(token_cfg["y_B"])
    y_ab = int(token_cfg["y_AB"])
    bg = background_tokens(cfg)

    rows: list[tuple[list[int], int, str]] = []

    def bg_seq() -> list[int]:
        return [rng.choice(bg) for _ in range(seq_len)]

    for _ in range(n_per_class):
        seq = bg_seq()
        rows.append((seq, rng.choice(bg), "background"))

    for _ in range(n_per_class):
        seq = bg_seq()
        seq[motif_position] = token_a
        seq[motif_position + 1] = rng.choice(bg)
        rows.append((seq, y_a, "A_only"))

    for _ in range(n_per_class):
        seq = bg_seq()
        seq[motif_position] = rng.choice(bg)
        seq[motif_position + 1] = token_b
        rows.append((seq, y_b, "B_only"))

    for _ in range(n_per_class):
        seq = bg_seq()
        seq[motif_position] = token_a
        seq[motif_position + 1] = token_b
        rows.append((seq, y_ab, "AB_composite"))

    rng.shuffle(rows)
    x = torch.tensor([r[0] for r in rows], dtype=torch.long)
    y = torch.tensor([r[1] for r in rows], dtype=torch.long)
    classes = [r[2] for r in rows]
    return x, y, classes


def load_model(runner, cfg: dict, ckpt: Path, device: torch.device):
    model = runner.make_model("moe_top1_no_lb", cfg, device)
    payload = torch.load(ckpt, map_location=device)
    state = payload["model_state"] if "model_state" in payload else payload
    model.load_state_dict(state)
    model.eval()
    return model


def normalized_mutual_info(labels: list[str], experts: list[int]) -> float:
    n = len(labels)
    if n == 0:
        return 0.0
    label_counts = Counter(labels)
    expert_counts = Counter(experts)
    joint = Counter(zip(labels, experts))
    mi = 0.0
    for (label, expert), count in joint.items():
        pxy = count / n
        px = label_counts[label] / n
        py = expert_counts[expert] / n
        mi += pxy * math.log(max(pxy / max(px * py, 1e-12), 1e-12))
    hx = -sum((count / n) * math.log(count / n) for count in label_counts.values())
    hy = -sum((count / n) * math.log(count / n) for count in expert_counts.values())
    return 2 * mi / (hx + hy) if hx + hy > 0 else 0.0


def collect_prediction_records(model, x, y, classes, cfg: dict, device: torch.device):
    batch_size = int(cfg["evaluation"]["batch_size"])
    hidden_rows: list[torch.Tensor] = []
    expert_rows: list[torch.Tensor] = []
    router_rows: list[torch.Tensor] = []
    loss_rows: list[torch.Tensor] = []
    pred_rows: list[torch.Tensor] = []
    with torch.no_grad():
        for start in range(0, x.shape[0], batch_size):
            xb = x[start : start + batch_size].to(device)
            yb = y[start : start + batch_size].to(device)
            logits, info = model(xb, return_acts=True)
            final_logits = logits[:, -1, :]
            hidden_rows.append(info["ffn_input"][:, -1, :].detach().cpu())
            expert_rows.append(info["expert_idx"][:, -1].detach().cpu())
            router_rows.append(info["router_probs"][:, -1, :].detach().cpu())
            loss_rows.append(F.cross_entropy(final_logits, yb, reduction="none").detach().cpu())
            pred_rows.append(torch.argmax(final_logits, dim=-1).detach().cpu())
    hidden = torch.cat(hidden_rows, dim=0)
    experts = torch.cat(expert_rows, dim=0)
    router_probs = torch.cat(router_rows, dim=0)
    losses = torch.cat(loss_rows, dim=0)
    preds = torch.cat(pred_rows, dim=0)
    correct = preds == y.cpu()
    return {
        "hidden": hidden,
        "experts": experts,
        "router_probs": router_probs,
        "losses": losses,
        "preds": preds,
        "correct": correct,
        "classes": classes,
    }


def class_metrics(seed: int, collected: dict) -> list[dict]:
    rows = []
    losses = collected["losses"]
    correct = collected["correct"]
    classes = collected["classes"]
    for cls in CLASS_ORDER:
        idx = [i for i, c in enumerate(classes) if c == cls]
        rows.append(
            {
                "seed": seed,
                "class": cls,
                "count": len(idx),
                "mean_ce": float(losses[idx].mean().item()),
                "accuracy": float(correct[idx].float().mean().item()),
            }
        )
    return rows


def routing_rows(seed: int, collected: dict, num_experts: int) -> tuple[list[dict], list[dict]]:
    classes = collected["classes"]
    experts = collected["experts"].tolist()
    rows = []
    deep = []
    for cls in CLASS_ORDER:
        vals = [e for e, c in zip(experts, classes) if c == cls]
        total = len(vals)
        counts = Counter(vals)
        for e in range(num_experts):
            rows.append(
                {
                    "seed": seed,
                    "class": cls,
                    "expert": e,
                    "count": counts[e],
                    "fraction": counts[e] / total if total else 0.0,
                }
            )
        dom_e, dom_n = counts.most_common(1)[0]
        deep.append(
            {
                "seed": seed,
                "class": cls,
                "dominant_expert": dom_e,
                "dominant_fraction": dom_n / total if total else 0.0,
            }
        )
    deep.append(
        {
            "seed": seed,
            "class": "ALL",
            "dominant_expert": -1,
            "dominant_fraction": normalized_mutual_info(classes, experts),
            "metric": "class_expert_nmi",
        }
    )
    return rows, deep


def feature_directions(seed: int, collected: dict) -> tuple[dict[str, torch.Tensor], list[dict]]:
    h = collected["hidden"]
    classes = collected["classes"]
    return feature_directions_from_labels(seed, h, classes, prefix="")


def feature_directions_from_labels(seed: int, h: torch.Tensor, classes: list[str], prefix: str) -> tuple[dict[str, torch.Tensor], list[dict]]:
    means = {}
    rows = []
    for cls in CLASS_ORDER:
        idx = torch.tensor([i for i, c in enumerate(classes) if c == cls], dtype=torch.long)
        means[cls] = h[idx].mean(dim=0)
    dirs = {
        f"{prefix}v_A": means["A_only"] - means["background"],
        f"{prefix}v_B": means["B_only"] - means["background"],
        f"{prefix}v_AB_raw": means["AB_composite"] - means["background"],
        f"{prefix}v_AB_int": means["AB_composite"] - means["A_only"] - means["B_only"] + means["background"],
    }
    for name, vec in dirs.items():
        rows.append({"seed": seed, "feature": name, "norm": float(vec.norm().item())})
    cos_ab = F.cosine_similarity(dirs[f"{prefix}v_AB_raw"], dirs[f"{prefix}v_A"] + dirs[f"{prefix}v_B"], dim=0)
    rows.append({"seed": seed, "feature": f"{prefix}cos(v_AB_raw,v_A+v_B)", "norm": float(cos_ab.item())})
    return dirs, rows


def permuted_feature_directions(seed: int, collected: dict) -> tuple[dict[str, torch.Tensor], list[dict]]:
    permuted = list(collected["classes"])
    random.Random(seed + 9931).shuffle(permuted)
    return feature_directions_from_labels(seed, collected["hidden"], permuted, prefix="perm_")


def svd_basis(matrix: torch.Tensor, max_rank: int) -> torch.Tensor | None:
    if matrix.shape[0] < 2:
        return None
    centered = matrix.float() - matrix.float().mean(dim=0, keepdim=True)
    _, _, vh = torch.linalg.svd(centered, full_matrices=False)
    return vh[: min(max_rank, vh.shape[0])].T.contiguous()


def projection_score(vec: torch.Tensor, basis: torch.Tensor, rank: int) -> float:
    norm = vec.float().norm()
    if norm.item() < 1e-9 or basis is None or basis.shape[1] == 0:
        return math.nan
    unit = vec.float() / norm
    sub = basis[:, : min(rank, basis.shape[1])]
    return float((sub.T @ unit).pow(2).sum().item())


def svd_projection_rows(seed: int, collected: dict, dirs: dict[str, torch.Tensor], num_experts: int) -> list[dict]:
    h = collected["hidden"]
    experts = collected["experts"]
    rows = []
    max_rank = max(RANKS)

    global_basis = svd_basis(h, max_rank)
    for feature, vec in dirs.items():
        for rank in RANKS:
            rows.append(
                {
                    "seed": seed,
                    "bucket": "global",
                    "expert": -1,
                    "count": int(h.shape[0]),
                    "feature": feature,
                    "rank": rank,
                    "projection_score": projection_score(vec, global_basis, rank),
                }
            )

    rng = torch.Generator().manual_seed(seed + 771)
    for expert in range(num_experts):
        idx = torch.nonzero(experts == expert, as_tuple=False).flatten()
        basis = svd_basis(h[idx], max_rank) if idx.numel() >= 2 else None
        random_idx = torch.randperm(h.shape[0], generator=rng)[: idx.numel()]
        random_basis = svd_basis(h[random_idx], max_rank) if random_idx.numel() >= 2 else None
        for bucket, cur_basis in [("expert", basis), ("random_matched", random_basis)]:
            for feature, vec in dirs.items():
                for rank in RANKS:
                    rows.append(
                        {
                            "seed": seed,
                            "bucket": bucket,
                            "expert": expert,
                            "count": int(idx.numel()),
                            "feature": feature,
                            "rank": rank,
                            "projection_score": projection_score(vec, cur_basis, rank),
                        }
                    )
    return rows


def ablation_rows(seed: int, model, x, y, classes, base_losses: torch.Tensor, cfg: dict, device: torch.device, num_experts: int) -> list[dict]:
    batch_size = int(cfg["evaluation"]["batch_size"])
    rows = []
    for expert in range(num_experts):
        losses = []
        with torch.no_grad():
            for start in range(0, x.shape[0], batch_size):
                xb = x[start : start + batch_size].to(device)
                yb = y[start : start + batch_size].to(device)
                logits, _ = model(xb, return_acts=True, ablate_expert=expert)
                losses.append(F.cross_entropy(logits[:, -1, :], yb, reduction="none").detach().cpu())
        masked = torch.cat(losses, dim=0)
        delta = masked - base_losses
        for cls in CLASS_ORDER:
            idx = torch.tensor([i for i, c in enumerate(classes) if c == cls], dtype=torch.long)
            rows.append(
                {
                    "seed": seed,
                    "expert": expert,
                    "class": cls,
                    "base_ce": float(base_losses[idx].mean().item()),
                    "masked_ce": float(masked[idx].mean().item()),
                    "delta_ce": float(delta[idx].mean().item()),
                }
            )
    return rows


def ab_expert_rows(seed: int, routing_deep: list[dict], projection_rows_all: list[dict], ablation_all: list[dict]) -> list[dict]:
    ab_route = next(r for r in routing_deep if r["class"] == "AB_composite")
    ab_expert = int(ab_route["dominant_expert"])
    rows = []
    for rank in [4, 8, 16]:
        item = {
            "seed": seed,
            "ab_dominant_expert": ab_expert,
            "ab_dominant_fraction": float(ab_route["dominant_fraction"]),
            "rank": rank,
        }
        for feature in ["v_A", "v_B", "v_AB_int"]:
            vals = [
                r
                for r in projection_rows_all
                if r["seed"] == seed
                and r["bucket"] == "expert"
                and int(r["expert"]) == ab_expert
                and r["feature"] == feature
                and int(r["rank"]) == rank
            ]
            item[f"proj_{feature}"] = vals[0]["projection_score"] if vals else math.nan
        for cls in CLASS_ORDER:
            vals = [r for r in ablation_all if r["seed"] == seed and int(r["expert"]) == ab_expert and r["class"] == cls]
            item[f"delta_ce_{cls}"] = vals[0]["delta_ce"] if vals else math.nan
        rows.append(item)
    return rows


def heatmap_by_seed(rows: list[dict], out: Path, value: str, row_key: str, title: str, seeds: list[int], num_experts: int) -> None:
    labels = CLASS_ORDER
    fig, axes = plt.subplots(1, len(seeds), figsize=(4.8 * len(seeds), 3.8), squeeze=False, constrained_layout=True)
    for ax, seed in zip(axes[0], seeds):
        mat = torch.zeros(len(labels), num_experts)
        for r in rows:
            if int(r["seed"]) == seed:
                mat[labels.index(r[row_key]), int(r["expert"])] = float(r[value])
        im = ax.imshow(mat.numpy(), vmin=0, vmax=1, cmap="viridis")
        ax.set_title(f"seed {seed}")
        ax.set_xticks(range(num_experts), [f"E{i}" for i in range(num_experts)])
        ax.set_yticks(range(len(labels)), labels)
        for i in range(len(labels)):
            for j in range(num_experts):
                ax.text(j, i, f"{mat[i, j]:.2f}", ha="center", va="center", color="white" if mat[i, j] < 0.55 else "black", fontsize=8)
    fig.suptitle(title)
    fig.colorbar(im, ax=axes.ravel().tolist(), shrink=0.8)
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=180, bbox_inches="tight")
    plt.close(fig)


def plot_ab_projection(rows: list[dict], out: Path, seeds: list[int]) -> None:
    fig, axes = plt.subplots(1, len(seeds), figsize=(4.4 * len(seeds), 3.4), squeeze=False, constrained_layout=True)
    features = ["proj_v_A", "proj_v_B", "proj_v_AB_int"]
    colors = {"proj_v_A": "#1f77b4", "proj_v_B": "#ff7f0e", "proj_v_AB_int": "#2ca02c"}
    for ax, seed in zip(axes[0], seeds):
        cur = [r for r in rows if int(r["seed"]) == seed]
        ranks = sorted({int(r["rank"]) for r in cur})
        for f in features:
            vals = [next(r for r in cur if int(r["rank"]) == rank)[f] for rank in ranks]
            ax.plot(ranks, vals, marker="o", label=f.replace("proj_", ""), color=colors[f])
        expert = int(cur[0]["ab_dominant_expert"]) if cur else -1
        frac = float(cur[0]["ab_dominant_fraction"]) if cur else math.nan
        ax.set_title(f"seed {seed}: AB dom E{expert} ({frac:.2f})")
        ax.set_xlabel("SVD rank r")
        ax.set_ylim(0, 1.02)
        ax.grid(True, alpha=0.25)
    axes[0][0].set_ylabel("ProjectionScore")
    axes[0][0].legend(loc="lower right")
    fig.suptitle("AB-dominant expert: feature direction projection")
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=180, bbox_inches="tight")
    plt.close(fig)


def plot_projection_vs_baseline(projection_rows: list[dict], ab_rows: list[dict], out: Path, seeds: list[int]) -> None:
    fig, axes = plt.subplots(1, len(seeds), figsize=(4.8 * len(seeds), 3.6), squeeze=False, constrained_layout=True)
    features = ["v_A", "v_B", "v_AB_int"]
    buckets = ["expert", "random_matched", "global"]
    colors = {"expert": "#1f77b4", "random_matched": "#ff7f0e", "global": "#2ca02c"}
    width = 0.24
    for ax, seed in zip(axes[0], seeds):
        cur_ab = [r for r in ab_rows if int(r["seed"]) == seed and int(r["rank"]) == 4][0]
        expert = int(cur_ab["ab_dominant_expert"])
        xs = list(range(len(features)))
        for b_i, bucket in enumerate(buckets):
            vals = []
            for feat in features:
                expert_id = expert if bucket != "global" else -1
                match = [
                    r
                    for r in projection_rows
                    if int(r["seed"]) == seed
                    and r["bucket"] == bucket
                    and int(r["expert"]) == expert_id
                    and r["feature"] == feat
                    and int(r["rank"]) == 4
                ][0]
                vals.append(float(match["projection_score"]))
            offsets = [x + (b_i - 1) * width for x in xs]
            ax.bar(offsets, vals, width=width, label=bucket, color=colors[bucket])
        ax.set_xticks(xs, features)
        ax.set_ylim(0, 1.05)
        ax.set_title(f"seed {seed}: AB dom E{expert}")
        ax.grid(axis="y", alpha=0.25)
    axes[0][0].set_ylabel("ProjectionScore at rank 4")
    axes[0][0].legend(loc="lower right")
    fig.suptitle("AB-dominant expert vs baselines")
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=180, bbox_inches="tight")
    plt.close(fig)


def plot_ab_ablation(rows: list[dict], out: Path, seeds: list[int]) -> None:
    fig, axes = plt.subplots(1, len(seeds), figsize=(4.4 * len(seeds), 3.4), squeeze=False, constrained_layout=True)
    for ax, seed in zip(axes[0], seeds):
        cur = [r for r in rows if int(r["seed"]) == seed and int(r["rank"]) == 4]
        vals = [float(cur[0][f"delta_ce_{cls}"]) for cls in CLASS_ORDER]
        ax.bar(CLASS_ORDER, vals, color=["#777777", "#1f77b4", "#ff7f0e", "#2ca02c"])
        expert = int(cur[0]["ab_dominant_expert"])
        ax.set_title(f"seed {seed}: mask E{expert}")
        ax.tick_params(axis="x", rotation=35)
        ax.axhline(0.0, color="black", linewidth=0.8)
        ax.grid(axis="y", alpha=0.25)
    axes[0][0].set_ylabel("Delta CE")
    fig.suptitle("Mask AB-dominant expert: class-wise loss change")
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=180, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n-eval-per-class", type=int, default=4096)
    parser.add_argument("--motif-position", type=int, default=15)
    parser.add_argument("--run-root", type=Path, default=None)
    parser.add_argument("--h0521b-run", type=Path, default=None)
    args = parser.parse_args()

    script_path = Path(__file__).resolve()
    exp_dir = script_path.parents[1]
    from_attention_root = script_path.parents[6]
    project_root = from_attention_root / "XingyuD"
    h0521b_run = args.h0521b_run or (
        project_root
        / "Attention_Search_Experiments/active/synthetic_data_understanding/results/h0521b_seq32_contiguous_ab/h0521b_seq32_contiguous_ab_4gpu_20260521"
    )
    cfg = read_json(h0521b_run / "resolved_config.json")
    runner = load_h0521b_runner(from_attention_root)
    seeds = [int(s) for s in cfg["seeds"]]
    num_experts = int(cfg["model"]["num_experts"])

    device_count = torch.cuda.device_count()
    devices = [torch.device(f"cuda:{i}") for i in range(device_count)] if device_count else [torch.device("cpu")]
    print(f"Using devices: {[str(d) for d in devices]}")

    table_dir = exp_dir / "tables"
    figure_dir = exp_dir / "figures"
    all_class_rows = []
    all_routing_rows = []
    all_routing_deep = []
    all_norm_rows = []
    all_projection_rows = []
    all_ablation_rows = []
    all_ab_rows = []

    for seed_i, seed in enumerate(seeds):
        device = devices[seed_i % len(devices)]
        ckpt = h0521b_run / "moe_top1_no_lb" / f"seed_{seed}" / "model.pt"
        print(f"Analyzing seed={seed} on {device}: {ckpt}", flush=True)
        torch.manual_seed(seed)
        model = load_model(runner, cfg, ckpt, device)
        x, y, classes = generate_fixed_eval(cfg, seed, args.n_eval_per_class, args.motif_position)
        collected = collect_prediction_records(model, x, y, classes, cfg, device)
        class_rows = class_metrics(seed, collected)
        routing, routing_deep = routing_rows(seed, collected, num_experts)
        dirs, norm_rows = feature_directions(seed, collected)
        perm_dirs, perm_norm_rows = permuted_feature_directions(seed, collected)
        projection_rows = svd_projection_rows(seed, collected, {**dirs, **perm_dirs}, num_experts)
        ablation = ablation_rows(seed, model, x, y, classes, collected["losses"], cfg, device, num_experts)
        ab_rows = ab_expert_rows(seed, routing_deep, projection_rows, ablation)
        all_class_rows.extend(class_rows)
        all_routing_rows.extend(routing)
        all_routing_deep.extend(routing_deep)
        all_norm_rows.extend(norm_rows)
        all_norm_rows.extend(perm_norm_rows)
        all_projection_rows.extend(projection_rows)
        all_ablation_rows.extend(ablation)
        all_ab_rows.extend(ab_rows)

    write_csv(table_dir / "class_metrics.csv", all_class_rows)
    write_csv(table_dir / "routing_prediction_by_seed.csv", all_routing_rows)
    write_csv(table_dir / "routing_prediction_summary_by_seed.csv", all_routing_deep)
    write_csv(table_dir / "feature_direction_norms.csv", all_norm_rows)
    write_csv(table_dir / "svd_projection_scores.csv", all_projection_rows)
    write_csv(table_dir / "expert_ablation_delta_loss.csv", all_ablation_rows)
    write_csv(table_dir / "ab_expert_deep_dive.csv", all_ab_rows)

    heatmap_by_seed(
        all_routing_rows,
        figure_dir / "routing_prediction_by_seed.png",
        "fraction",
        "class",
        "Prediction-position routing P(expert | class)",
        seeds,
        num_experts,
    )
    plot_ab_projection(all_ab_rows, figure_dir / "ab_expert_projection_by_seed.png", seeds)
    plot_projection_vs_baseline(
        all_projection_rows,
        all_ab_rows,
        figure_dir / "ab_expert_projection_vs_baselines_rank4_by_seed.png",
        seeds,
    )
    plot_ab_ablation(all_ab_rows, figure_dir / "ab_expert_ablation_delta_loss_by_seed.png", seeds)

    run_summary = {
        "experiment": "H0522_svd_feature_mixing_seq32",
        "h0521b_run": str(h0521b_run),
        "seeds": seeds,
        "n_eval_per_class": args.n_eval_per_class,
        "motif_position": args.motif_position,
        "devices": [str(d) for d in devices],
        "tables": str(table_dir),
        "figures": str(figure_dir),
    }
    write_json(exp_dir / "run_summary.json", run_summary)
    print(json.dumps(run_summary, indent=2), flush=True)


if __name__ == "__main__":
    main()
