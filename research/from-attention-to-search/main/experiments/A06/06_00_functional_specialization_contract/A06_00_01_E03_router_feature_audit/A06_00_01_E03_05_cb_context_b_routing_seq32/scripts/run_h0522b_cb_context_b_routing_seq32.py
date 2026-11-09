#!/usr/bin/env python3
"""Run H0522b seq_len=32 CB-context B source-token routing diagnostic."""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import random
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from multiprocessing import get_context

os.environ.setdefault("PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION", "python")
os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib")

import torch
from torch.nn import functional as F

from run_h0521b_seq32_contiguous_ab import (
    MoETinyTransformer,
    SeqDataset,
    add_background_source_records,
    aggregate_mean,
    background_tokens,
    load_json,
    normalized_mutual_info,
    project_root,
    resolve_output,
    train_one_model,
    write_csv,
    write_json,
)


CLASS_NAMES = ["A_only", "B_only", "AB_composite", "CB_composite", "background"]
SOURCE_IDENTITIES = ["A", "B", "C", "background"]
SOURCE_ROLES = [
    "A_in_A_only",
    "A_in_AB",
    "C_in_CB",
    "B_in_B_only",
    "B_in_AB",
    "B_in_CB",
    "background_neighbor_A_only",
    "background_neighbor_B_only",
    "background_only",
]
B_CONTEXT_ROLES = ["B_in_B_only", "B_in_AB", "B_in_CB"]


@dataclass
class EvalBundle:
    x: torch.Tensor
    y: torch.Tensor
    classes: list[str]
    motif_positions: list[int]
    source_records: list[list[dict]]


def generate_dataset(cfg: dict, seed: int, split: str, samples_per_class: int) -> EvalBundle:
    rng = random.Random(seed + (0 if split == "train" else 1000003))
    seq_len = int(cfg["data"]["seq_len"])
    bg_tokens = background_tokens(cfg)
    token_cfg = cfg["data"]["tokens"]
    token_a = int(token_cfg["A"])
    token_b = int(token_cfg["B"])
    token_c = int(token_cfg["C"])
    target_a = int(token_cfg["y_A"])
    target_b = int(token_cfg["y_B"])
    target_ab = int(token_cfg["y_AB"])
    target_cb = int(token_cfg["y_CB"])
    bg_source_count = int(cfg["evaluation"].get("source_background_positions_per_sample", 2))
    rows: list[tuple[list[int], int, str, int, list[dict]]] = []
    legal_positions = list(range(seq_len - 1))

    def background_sequence() -> list[int]:
        return [rng.choice(bg_tokens) for _ in range(seq_len)]

    def add_sample(cls: str, motif: list[int], target: int, source_roles: list[tuple[int, str, str]]) -> None:
        p = rng.choice(legal_positions)
        seq = background_sequence()
        seq[p : p + 2] = motif
        records: list[dict] = []
        for offset, identity, role in source_roles:
            pos = p + offset
            records.append(
                {
                    "position": pos,
                    "source_identity": identity,
                    "source_role": role,
                    "is_motif_token": 1,
                }
            )
        add_background_source_records(records, rng, seq_len, {p, p + 1}, bg_source_count)
        rows.append((seq, target, cls, p, records))

    for _ in range(samples_per_class):
        r = rng.choice(bg_tokens)
        add_sample("A_only", [token_a, r], target_a, [(0, "A", "A_in_A_only"), (1, "background", "background_neighbor_A_only")])
    for _ in range(samples_per_class):
        r = rng.choice(bg_tokens)
        add_sample("B_only", [r, token_b], target_b, [(0, "background", "background_neighbor_B_only"), (1, "B", "B_in_B_only")])
    for _ in range(samples_per_class):
        add_sample("AB_composite", [token_a, token_b], target_ab, [(0, "A", "A_in_AB"), (1, "B", "B_in_AB")])
    for _ in range(samples_per_class):
        add_sample("CB_composite", [token_c, token_b], target_cb, [(0, "C", "C_in_CB"), (1, "B", "B_in_CB")])
    for _ in range(samples_per_class):
        seq = background_sequence()
        y = rng.choice(bg_tokens)
        records: list[dict] = []
        add_background_source_records(records, rng, seq_len, set(), bg_source_count)
        rows.append((seq, y, "background", -1, records))

    rng.shuffle(rows)
    return EvalBundle(
        x=torch.tensor([row[0] for row in rows], dtype=torch.long),
        y=torch.tensor([row[1] for row in rows], dtype=torch.long),
        classes=[row[2] for row in rows],
        motif_positions=[row[3] for row in rows],
        source_records=[row[4] for row in rows],
    )


def evaluate_class_metrics(model: MoETinyTransformer, data: EvalBundle, cfg: dict, device: torch.device, seed: int) -> list[dict]:
    losses: dict[str, list[float]] = defaultdict(list)
    correct: Counter[str] = Counter()
    counts: Counter[str] = Counter()
    batch_size = int(cfg["evaluation"]["batch_size"])
    model.eval()
    with torch.no_grad():
        for start in range(0, data.x.shape[0], batch_size):
            x = data.x[start : start + batch_size].to(device)
            y = data.y[start : start + batch_size].to(device)
            classes = data.classes[start : start + batch_size]
            logits, _ = model(x)
            logits = logits[:, -1, :]
            loss = F.cross_entropy(logits, y, reduction="none")
            pred = torch.argmax(logits, dim=-1)
            for i, cls in enumerate(classes):
                losses[cls].append(float(loss[i].detach().cpu()))
                correct[cls] += int(pred[i].item() == int(y[i].item()))
                counts[cls] += 1
    return [
        {
            "seed": seed,
            "model": "moe_top1_no_lb",
            "class": cls,
            "count": counts[cls],
            "mean_ce": sum(losses[cls]) / len(losses[cls]) if losses[cls] else math.nan,
            "accuracy": correct[cls] / counts[cls] if counts[cls] else math.nan,
        }
        for cls in CLASS_NAMES
    ]


def cosine_from_counters(a: Counter[int], b: Counter[int], num_experts: int) -> float:
    va = torch.tensor([a[i] for i in range(num_experts)], dtype=torch.float)
    vb = torch.tensor([b[i] for i in range(num_experts)], dtype=torch.float)
    if float(va.norm()) == 0.0 or float(vb.norm()) == 0.0:
        return math.nan
    return float(F.cosine_similarity(va, vb, dim=0).item())


def collect_moe_diagnostics(model: MoETinyTransformer, data: EvalBundle, cfg: dict, device: torch.device, seed: int) -> dict[str, list[dict]]:
    num_experts = int(cfg["model"]["num_experts"])
    batch_size = int(cfg["evaluation"]["batch_size"])
    role_counts: dict[str, Counter[int]] = defaultdict(Counter)
    identity_counts: dict[str, Counter[int]] = defaultdict(Counter)
    source_role_labels: list[str] = []
    source_identity_labels: list[str] = []
    source_experts: list[int] = []
    source_rows: list[dict] = []
    model.eval()
    with torch.no_grad():
        for start in range(0, data.x.shape[0], batch_size):
            x = data.x[start : start + batch_size].to(device)
            classes = data.classes[start : start + batch_size]
            motif_positions = data.motif_positions[start : start + batch_size]
            source_records = data.source_records[start : start + batch_size]
            _, info = model(x, return_acts=True)
            experts_by_pos = info["expert_idx"].detach().cpu()
            probs_by_pos = info["router_probs"].detach().cpu()
            for local_i, cls in enumerate(classes):
                for record in source_records[local_i]:
                    pos = int(record["position"])
                    expert = int(experts_by_pos[local_i, pos].item())
                    probs = probs_by_pos[local_i, pos]
                    top2 = torch.topk(probs, k=min(2, num_experts)).values
                    margin = float((top2[0] - top2[1]).item()) if top2.numel() > 1 else 0.0
                    role = str(record["source_role"])
                    identity = str(record["source_identity"])
                    role_counts[role][expert] += 1
                    identity_counts[identity][expert] += 1
                    source_role_labels.append(role)
                    source_identity_labels.append(identity)
                    source_experts.append(expert)
                    source_rows.append(
                        {
                            "seed": seed,
                            "class": cls,
                            "motif_position": motif_positions[local_i],
                            "source_position": pos,
                            "source_identity": identity,
                            "source_role": role,
                            "is_motif_token": int(record["is_motif_token"]),
                            "expert": expert,
                            "router_margin": margin,
                        }
                    )

    def matrix_rows(group_name: str, counts: dict, groups: list[str]) -> list[dict]:
        rows = []
        for group in groups:
            total = sum(counts[group].values())
            for expert in range(num_experts):
                rows.append(
                    {
                        "seed": seed,
                        group_name: group,
                        "expert": expert,
                        "count": counts[group][expert],
                        "fraction": counts[group][expert] / total if total else 0.0,
                    }
                )
        return rows

    dominant = {}
    dominant_fraction = {}
    for role in SOURCE_ROLES:
        total = sum(role_counts[role].values())
        if total == 0:
            dominant[role] = -1
            dominant_fraction[role] = math.nan
        else:
            expert, count = role_counts[role].most_common(1)[0]
            dominant[role] = int(expert)
            dominant_fraction[role] = count / total

    b_context_rows = []
    for left, right in [("B_in_B_only", "B_in_AB"), ("B_in_B_only", "B_in_CB"), ("B_in_AB", "B_in_CB")]:
        b_context_rows.append(
            {
                "seed": seed,
                "comparison": f"{left}_vs_{right}",
                "same_dominant_expert": int(dominant[left] == dominant[right]),
                "left_dominant_expert": dominant[left],
                "right_dominant_expert": dominant[right],
                "routing_distribution_cosine": cosine_from_counters(role_counts[left], role_counts[right], num_experts),
            }
        )

    rule_summary = {
        "seed": seed,
        "role_nmi": normalized_mutual_info(source_role_labels, source_experts),
        "identity_nmi": normalized_mutual_info(source_identity_labels, source_experts),
        "B_in_B_only_dominant_expert": dominant["B_in_B_only"],
        "B_in_AB_dominant_expert": dominant["B_in_AB"],
        "B_in_CB_dominant_expert": dominant["B_in_CB"],
        "B_same_Bonly_AB": int(dominant["B_in_B_only"] == dominant["B_in_AB"]),
        "B_same_Bonly_CB": int(dominant["B_in_B_only"] == dominant["B_in_CB"]),
        "B_same_AB_CB": int(dominant["B_in_AB"] == dominant["B_in_CB"]),
        "B_all_three_same": int(dominant["B_in_B_only"] == dominant["B_in_AB"] == dominant["B_in_CB"]),
        **{f"{role}_dominant_fraction": dominant_fraction[role] for role in B_CONTEXT_ROLES},
    }
    return {
        "source_token_rows": source_rows,
        "source_role_matrix": matrix_rows("source_role", role_counts, SOURCE_ROLES),
        "source_identity_matrix": matrix_rows("source_identity", identity_counts, SOURCE_IDENTITIES),
        "seed_rule_summary": [rule_summary],
        "b_context_similarity": b_context_rows,
    }


def plot_outputs(out_dir: Path, fig_dir: Path, cfg: dict) -> None:
    try:
        import matplotlib.pyplot as plt
    except Exception as exc:
        print(f"matplotlib unavailable: {exc}", flush=True)
        return

    def read_csv(path: Path) -> list[dict]:
        with path.open("r", encoding="utf-8") as f:
            return list(csv.DictReader(f))

    fig_dir.mkdir(parents=True, exist_ok=True)
    num_experts = int(cfg["model"]["num_experts"])
    role_rows = read_csv(out_dir / "source_role_matrix_by_seed.csv")
    seeds = [int(s) for s in cfg["seeds"]]

    matrix = torch.zeros(len(seeds) * len(SOURCE_ROLES), num_experts)
    ylabels = []
    for si, seed in enumerate(seeds):
        for ri, role in enumerate(SOURCE_ROLES):
            ylabels.append(f"{seed}:{role}")
            for row in role_rows:
                if int(row["seed"]) == seed and row["source_role"] == role:
                    matrix[si * len(SOURCE_ROLES) + ri, int(row["expert"])] = float(row["fraction"])
    plt.figure(figsize=(7.2, max(6.0, 0.28 * len(ylabels))))
    plt.imshow(matrix.numpy(), cmap="magma", vmin=0, vmax=1, aspect="auto")
    plt.xticks(range(num_experts), [f"E{i}" for i in range(num_experts)])
    plt.yticks(range(len(ylabels)), ylabels, fontsize=7)
    plt.colorbar(label="fraction")
    plt.title("H0522b source-role routing by seed")
    for i in range(matrix.shape[0]):
        for j in range(num_experts):
            val = float(matrix[i, j])
            if val >= 0.15:
                plt.text(j, i, f"{val:.2f}", ha="center", va="center", fontsize=6, color="white" if val > 0.5 else "black")
    plt.tight_layout()
    plt.savefig(fig_dir / "source_role_routing_matrix_by_seed_row.png", dpi=180)
    plt.close()

    b_matrix = torch.zeros(len(seeds) * len(B_CONTEXT_ROLES), num_experts)
    b_labels = []
    for si, seed in enumerate(seeds):
        for ri, role in enumerate(B_CONTEXT_ROLES):
            b_labels.append(f"{seed}:{role}")
            for row in role_rows:
                if int(row["seed"]) == seed and row["source_role"] == role:
                    b_matrix[si * len(B_CONTEXT_ROLES) + ri, int(row["expert"])] = float(row["fraction"])
    plt.figure(figsize=(6.8, max(4.2, 0.35 * len(b_labels))))
    plt.imshow(b_matrix.numpy(), cmap="viridis", vmin=0, vmax=1, aspect="auto")
    plt.xticks(range(num_experts), [f"E{i}" for i in range(num_experts)])
    plt.yticks(range(len(b_labels)), b_labels, fontsize=8)
    plt.colorbar(label="fraction")
    plt.title("B source-token routing across contexts by seed")
    for i in range(b_matrix.shape[0]):
        for j in range(num_experts):
            val = float(b_matrix[i, j])
            plt.text(j, i, f"{val:.2f}", ha="center", va="center", fontsize=7, color="white" if val > 0.5 else "black")
    plt.tight_layout()
    plt.savefig(fig_dir / "b_context_routing_by_seed_row.png", dpi=180)
    plt.close()


def worker(seed: int, cfg: dict, out_dir: str, run_stage: str, device_id: int | None) -> None:
    device = torch.device(f"cuda:{device_id}" if device_id is not None and torch.cuda.is_available() else "cpu")
    root_out = Path(out_dir)
    train_data = generate_dataset(cfg, seed, "train", int(cfg["data"]["train_samples_per_class"]))
    eval_data = generate_dataset(cfg, seed, "eval", int(cfg["data"]["eval_samples_per_class"]))
    model = train_one_model("moe_top1_no_lb", cfg, train_data, seed, device, root_out, run_stage)
    write_csv(root_out / f"class_metrics_seed_{seed}.csv", evaluate_class_metrics(model, eval_data, cfg, device, seed))
    diag = collect_moe_diagnostics(model, eval_data, cfg, device, seed)
    for key, rows in diag.items():
        write_csv(root_out / f"{key}_seed_{seed}.csv", rows)


def read_csv_rows(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def run_task(args: argparse.Namespace) -> None:
    cfg = load_json(args.config)
    if args.run_stage == "smoke":
        cfg = json.loads(json.dumps(cfg))
        cfg["seeds"] = cfg["seeds"][:1]
        cfg["data"]["train_samples_per_class"] = min(512, int(cfg["data"]["train_samples_per_class"]))
        cfg["data"]["eval_samples_per_class"] = min(256, int(cfg["data"]["eval_samples_per_class"]))
        cfg["training"]["steps"] = int(cfg["training"]["smoke_steps"])
    root = project_root()
    out_dir = resolve_output(root, cfg["output"]["result_dir"], args.run_name)
    fig_dir = resolve_output(root, cfg["output"]["figure_dir"], args.run_name)
    out_dir.mkdir(parents=True, exist_ok=True)
    fig_dir.mkdir(parents=True, exist_ok=True)
    write_json(out_dir / "resolved_config.json", cfg)
    write_json(
        out_dir / "dataset_manifest.json",
        {
            "class_names": CLASS_NAMES,
            "source_identities": SOURCE_IDENTITIES,
            "source_roles": SOURCE_ROLES,
            "b_context_roles": B_CONTEXT_ROLES,
            "motif_policy": "contiguous two-token motif at uniformly sampled positions; compare B in r-B, A-B, C-B.",
        },
    )

    seeds = [int(seed) for seed in cfg["seeds"]]
    device_count = torch.cuda.device_count() if torch.cuda.is_available() else 0
    print(f"RUN_NAME={args.run_name} RUN_STAGE={args.run_stage} CUDA={torch.cuda.is_available()} CUDA_DEVICE_COUNT={device_count}", flush=True)

    if args.parallel and len(seeds) > 1 and device_count > 1:
        ctx = get_context("spawn")
        procs = []
        for i, seed in enumerate(seeds):
            p = ctx.Process(target=worker, args=(seed, cfg, str(out_dir), args.run_stage, i % min(device_count, 2)))
            p.start()
            procs.append(p)
        for p in procs:
            p.join()
            if p.exitcode != 0:
                raise RuntimeError(f"worker failed with exit code {p.exitcode}")
    else:
        for i, seed in enumerate(seeds):
            worker(seed, cfg, str(out_dir), args.run_stage, i % device_count if device_count else None)

    class_rows: list[dict] = []
    diagnostics: dict[str, list[dict]] = defaultdict(list)
    for seed in seeds:
        class_rows.extend(read_csv_rows(out_dir / f"class_metrics_seed_{seed}.csv"))
        for key in ["source_token_rows", "source_role_matrix", "source_identity_matrix", "seed_rule_summary", "b_context_similarity"]:
            diagnostics[key].extend(read_csv_rows(out_dir / f"{key}_seed_{seed}.csv"))

    write_csv(out_dir / "class_metrics_by_seed.csv", class_rows)
    write_csv(out_dir / "class_metrics.csv", aggregate_mean(class_rows, ["model", "class"], ["mean_ce", "accuracy"]))
    for key, rows in diagnostics.items():
        write_csv(out_dir / f"{key}_by_seed.csv", rows)
    write_csv(out_dir / "source_role_routing_matrix.csv", aggregate_mean(diagnostics["source_role_matrix"], ["source_role", "expert"], ["fraction"]))
    write_csv(out_dir / "source_identity_routing_matrix.csv", aggregate_mean(diagnostics["source_identity_matrix"], ["source_identity", "expert"], ["fraction"]))

    rule_rows = diagnostics["seed_rule_summary"]
    intersection_rows = []
    for field in ["B_same_Bonly_AB", "B_same_Bonly_CB", "B_same_AB_CB", "B_all_three_same"]:
        vals = [int(row[field]) for row in rule_rows]
        intersection_rows.append({"rule": field, "hold_count": sum(vals), "num_seeds": len(vals), "hold_fraction": sum(vals) / len(vals)})
    write_csv(out_dir / "cross_seed_b_context_intersection.csv", intersection_rows)
    plot_outputs(out_dir, fig_dir, cfg)

    summary = {
        "run_name": args.run_name,
        "stage": args.stage,
        "run_stage": args.run_stage,
        "variant": args.variant,
        "result_dir": str(out_dir),
        "figure_dir": str(fig_dir),
        "seeds": seeds,
        "primary_metric": "B source-token routing distribution across B-only, AB, and CB contexts per seed",
    }
    write_json(out_dir / "run_summary.json", summary)
    print(json.dumps(summary, indent=2), flush=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--stage", default="h0522b_cb_context_b_routing_seq32")
    parser.add_argument("--run-name", required=True)
    parser.add_argument("--variant", default="cb_context_b_source_routing")
    parser.add_argument("--run-stage", choices=["smoke", "full"], default="full")
    parser.add_argument("--parallel", action="store_true")
    args = parser.parse_args()
    run_task(args)


if __name__ == "__main__":
    main()
