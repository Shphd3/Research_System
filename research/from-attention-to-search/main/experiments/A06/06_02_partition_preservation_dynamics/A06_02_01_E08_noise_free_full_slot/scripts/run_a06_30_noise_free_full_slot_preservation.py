#!/usr/bin/env python3
"""Run A06_30 no-background full-slot preservation audit."""

from __future__ import annotations

import argparse
import csv
import importlib.util
import json
import math
import os
import time
from dataclasses import dataclass
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib")
os.environ.setdefault("PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION", "python")

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import torch
from torch.nn import functional as F


EXPERIMENT_ID = "A06_02_01_E08_noise_free_full_slot"
REPO_ROOT = Path(__file__).resolve().parents[7]
BASE_RUNNER = (
    REPO_ROOT
    / "Projects"
    / "from-attention-to-search"
    / "main"
    / "experiments"
    / "A06"
    / "A06_02_02_E03_transformer_common_rare"
    / "scripts"
    / "run_a06_24_synthetic_common_rare_transformer_moe.py"
)


def load_base_module():
    spec = importlib.util.spec_from_file_location("a06_24_base", BASE_RUNNER)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import base runner at {BASE_RUNNER}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


base = load_base_module()


@dataclass
class FullSlotBatch:
    x: torch.Tensor
    feature: torch.Tensor
    route_pos: torch.Tensor


def parse_int_list(text: str) -> list[int]:
    return [int(part) for part in str(text).replace(",", " ").split() if part.strip()]


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    keys = sorted({k for row in rows for k in row.keys()})
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict]:
    if not path.exists() or path.stat().st_size == 0:
        return []
    with path.open("r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def clone_state(model) -> dict[str, torch.Tensor]:
    return {k: v.detach().cpu().clone() for k, v in model.state_dict().items()}


def load_state(model, state: dict[str, torch.Tensor], device: torch.device) -> None:
    model.load_state_dict({k: v.to(device) for k, v in state.items()})


def make_model(args: argparse.Namespace, seed: int, device: torch.device):
    base.set_seed(seed)
    vocab_size = int(args.num_neutral_tokens) + int(args.num_features)
    model = base.TinyTransformerMoE(
        vocab_size=vocab_size,
        d_model=int(args.d_model),
        num_heads=int(args.num_heads),
        d_ff=int(args.d_ff),
        num_experts=int(args.num_experts),
    )
    return model.to(device)


def generate_full_slot_batch(args: argparse.Namespace, n: int, seed: int, balanced: bool) -> FullSlotBatch:
    gen = torch.Generator().manual_seed(int(seed))
    num_features = int(args.num_features)
    if balanced:
        feature = torch.arange(n, dtype=torch.long) % num_features
        feature = feature[torch.randperm(n, generator=gen)]
    else:
        feature = torch.randint(0, num_features, (n,), generator=gen)
    token = int(args.num_neutral_tokens) + feature
    x = token.view(-1, 1).expand(n, int(args.seq_len)).clone()
    route_pos = torch.full((n,), int(args.seq_len) - 2, dtype=torch.long)
    return FullSlotBatch(x=x, feature=feature, route_pos=route_pos)


def route_slice(x: torch.Tensor, route_pos: torch.Tensor) -> torch.Tensor:
    return x[torch.arange(x.shape[0], device=x.device), route_pos.to(x.device)]


def full_lm_loss(logits: torch.Tensor, x: torch.Tensor) -> torch.Tensor:
    pred = logits[:, :-1, :].reshape(-1, logits.shape[-1])
    labels = x[:, 1:].reshape(-1)
    return F.cross_entropy(pred, labels)


def equal_norm_rows(rows: torch.Tensor, scale: float) -> torch.Tensor:
    centered = rows.float() - rows.float().mean(dim=0, keepdim=True)
    return centered / centered.norm(dim=1, keepdim=True).clamp_min(1e-8) * float(scale)


def set_router_rows(model, rows: torch.Tensor, scale: float) -> None:
    with torch.no_grad():
        model.moe.router.weight.copy_(equal_norm_rows(rows, scale).to(model.moe.router.weight.device))


@torch.no_grad()
def collect_hidden(model, batch: FullSlotBatch, args: argparse.Namespace, device: torch.device) -> torch.Tensor:
    model.eval()
    parts = []
    for start in range(0, batch.x.shape[0], int(args.eval_batch_size)):
        x = batch.x[start : start + int(args.eval_batch_size)].to(device)
        h = model.router_states(x).detach().cpu()
        parts.append(h)
    return torch.cat(parts, dim=0)


def centers_by_feature(states: torch.Tensor, feature: torch.Tensor, num_features: int) -> torch.Tensor:
    centers = []
    for f in range(num_features):
        mask = feature == f
        if bool(mask.any()):
            centers.append(states[mask].mean(dim=0))
        else:
            centers.append(states.mean(dim=0))
    return torch.stack(centers, dim=0)


def build_centers(model, calib: FullSlotBatch, args: argparse.Namespace, device: torch.device) -> dict[str, torch.Tensor | None]:
    h = collect_hidden(model, calib, args, device)
    n, seq_len, d = h.shape
    feature = calib.feature.detach().cpu()
    all_h = h.reshape(n * seq_len, d)
    all_feature = feature.repeat_interleave(seq_len)
    pred_h = h[:, :-1, :].reshape(n * (seq_len - 1), d)
    pred_feature = feature.repeat_interleave(seq_len - 1)
    last_h = h[:, int(args.seq_len) - 2, :]
    return {
        "random": None,
        "oracle_allpos": centers_by_feature(all_h, all_feature, int(args.num_features)),
        "oracle_predpos": centers_by_feature(pred_h, pred_feature, int(args.num_features)),
        "oracle_lastpred": centers_by_feature(last_h, feature, int(args.num_features)),
    }


def best_feature_mapping(feature: torch.Tensor, assign: torch.Tensor, num_features: int, num_experts: int) -> dict[int, int]:
    return base.best_feature_mapping(feature.detach().cpu(), assign.detach().cpu(), num_features, num_experts)


def margin_from_mapping(scores: torch.Tensor, feature: torch.Tensor, mapping: dict[int, int]) -> torch.Tensor:
    feature_cpu = feature.detach().cpu()
    scores_cpu = scores.detach().cpu().float()
    target = torch.tensor([mapping[int(f)] for f in feature_cpu.tolist()], dtype=torch.long)
    target_scores = scores_cpu[torch.arange(scores_cpu.shape[0]), target]
    masked = scores_cpu.clone()
    masked[torch.arange(scores_cpu.shape[0]), target] = -1e9
    return target_scores - masked.max(dim=1).values


def p05(values: torch.Tensor) -> float:
    if int(values.numel()) == 0:
        return float("nan")
    vals = torch.sort(values.detach().cpu().float()).values
    idx = max(0, min(int(vals.numel()) - 1, int(math.floor(0.05 * max(0, int(vals.numel()) - 1)))))
    return float(vals[idx].item())


@torch.no_grad()
def collect_scores(model, batch: FullSlotBatch, args: argparse.Namespace, device: torch.device):
    model.eval()
    score_all = []
    assign_all = []
    score_pred = []
    assign_pred = []
    score_last = []
    assign_last = []
    loss_sum = 0.0
    correct = 0
    count = 0
    for start in range(0, batch.x.shape[0], int(args.eval_batch_size)):
        x = batch.x[start : start + int(args.eval_batch_size)].to(device)
        logits, info = model(x, common_vec=None)
        scores = info["route_scores"].detach().cpu()
        assign = scores.argmax(dim=-1)
        score_all.append(scores.reshape(-1, scores.shape[-1]))
        assign_all.append(assign.reshape(-1))
        score_pred.append(scores[:, :-1, :].reshape(-1, scores.shape[-1]))
        assign_pred.append(assign[:, :-1].reshape(-1))
        score_last.append(scores[:, int(args.seq_len) - 2, :].detach().cpu())
        assign_last.append(assign[:, int(args.seq_len) - 2].detach().cpu())
        pred = logits[:, :-1, :].reshape(-1, logits.shape[-1])
        labels = x[:, 1:].reshape(-1)
        loss_sum += float(F.cross_entropy(pred, labels, reduction="sum").detach().cpu().item())
        correct += int((pred.argmax(dim=-1) == labels).sum().detach().cpu().item())
        count += int(labels.numel())
    return {
        "scores_all": torch.cat(score_all, dim=0),
        "assign_all": torch.cat(assign_all, dim=0),
        "scores_pred": torch.cat(score_pred, dim=0),
        "assign_pred": torch.cat(assign_pred, dim=0),
        "scores_last": torch.cat(score_last, dim=0),
        "assign_last": torch.cat(assign_last, dim=0),
        "loss": loss_sum / max(1, count),
        "next_token_accuracy": correct / max(1, count),
    }


def eval_model(
    model,
    batch: FullSlotBatch,
    args: argparse.Namespace,
    device: torch.device,
    condition: str,
    seed: int,
    checkpoint: int,
    mapping: dict[int, int] | None,
    step0_margin: torch.Tensor | None,
) -> tuple[dict, dict[int, int], torch.Tensor]:
    out = collect_scores(model, batch, args, device)
    num_features = int(args.num_features)
    num_experts = int(args.num_experts)
    feature_seq = batch.feature.detach().cpu()
    feature_all = feature_seq.repeat_interleave(int(args.seq_len))
    feature_pred = feature_seq.repeat_interleave(int(args.seq_len) - 1)
    if mapping is None:
        mapping = best_feature_mapping(feature_all, out["assign_all"], num_features, num_experts)
    matched_all = torch.tensor([mapping[int(f)] for f in feature_all.tolist()], dtype=torch.long)
    margin_all = margin_from_mapping(out["scores_all"], feature_all, mapping)
    margin_pred = margin_from_mapping(out["scores_pred"], feature_pred, mapping)
    margin_last = margin_from_mapping(out["scores_last"], feature_seq, mapping)
    if step0_margin is not None:
        eligible = step0_margin.detach().cpu() > 0
        sign_flip = float((margin_all[eligible] <= 0).float().mean().item()) if bool(eligible.any()) else float("nan")
    else:
        sign_flip = 0.0
    row = {
        "experiment_id": EXPERIMENT_ID,
        "condition": condition,
        "seed": seed,
        "checkpoint": checkpoint,
        "eval_sequences": int(feature_seq.numel()),
        "eval_tokens_all": int(feature_all.numel()),
        "loss": out["loss"],
        "next_token_accuracy": out["next_token_accuracy"],
        "allpos_feature_NMI": base.nmi(feature_all, out["assign_all"]),
        "predpos_feature_NMI": base.nmi(feature_pred, out["assign_pred"]),
        "lastpred_feature_NMI": base.nmi(feature_seq, out["assign_last"]),
        "matched_preserve_fraction": float((out["assign_all"] == matched_all).float().mean().item()),
        "margin_mean": float(margin_all.mean().item()),
        "margin_p05": p05(margin_all),
        "pred_margin_p05": p05(margin_pred),
        "last_margin_p05": p05(margin_last),
        "positive_margin_frac": float((margin_all > 0).float().mean().item()),
        "sign_flip_rate": sign_flip,
        **base.load_metrics(out["assign_all"], num_experts),
    }
    for f, e in mapping.items():
        row[f"map_feature_{f}_expert"] = e
    return row, mapping, margin_all


def train_condition(
    args: argparse.Namespace,
    condition: str,
    centers: torch.Tensor | None,
    base_state: dict[str, torch.Tensor],
    eval_batch: FullSlotBatch,
    seed: int,
    device: torch.device,
) -> list[dict]:
    model = make_model(args, seed + 10000, device)
    load_state(model, base_state, device)
    if centers is not None:
        set_router_rows(model, centers, float(args.router_init_scale))
    optimizer = torch.optim.AdamW(model.parameters(), lr=float(args.lr), weight_decay=float(args.weight_decay))
    checkpoints = sorted(set([0] + parse_int_list(args.checkpoints)))
    rows = []
    mapping = None
    step0_margin = None
    row, mapping, step0_margin = eval_model(model, eval_batch, args, device, condition, seed, 0, None, None)
    rows.append(row)
    checkpoint_set = set(checkpoints)
    for step in range(1, int(args.train_steps) + 1):
        model.train()
        batch = generate_full_slot_batch(args, int(args.train_batch_size), seed + 700000 + step, balanced=False)
        x = batch.x.to(device)
        logits, _info = model(x, common_vec=None)
        loss = full_lm_loss(logits, x)
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), float(args.grad_clip))
        optimizer.step()
        if step in checkpoint_set:
            row, _mapping, _margin = eval_model(model, eval_batch, args, device, condition, seed, step, mapping, step0_margin)
            rows.append(row)
    return rows


def run_cell(args: argparse.Namespace, seed: int, device: torch.device) -> tuple[list[dict], list[dict]]:
    calib = generate_full_slot_batch(args, int(args.calib_samples), seed + 101, balanced=True)
    eval_batch = generate_full_slot_batch(args, int(args.eval_samples), seed + 202, balanced=True)
    base_model = make_model(args, seed + 3001, device)
    base_state = clone_state(base_model)
    centers = build_centers(base_model, calib, args, device)
    data_rows = []
    for split, batch in [("calib", calib), ("eval", eval_batch)]:
        feature_counts = torch.bincount(batch.feature, minlength=int(args.num_features)).float()
        row = {
            "experiment_id": EXPERIMENT_ID,
            "seed": seed,
            "split": split,
            "sample_count": int(batch.feature.numel()),
            "seq_len": int(args.seq_len),
            "background_token_count": 0,
        }
        for f in range(int(args.num_features)):
            row[f"feature{f}_fraction"] = float((feature_counts[f] / feature_counts.sum().clamp_min(1.0)).item())
        data_rows.append(row)
    train_rows = []
    for condition, center in centers.items():
        train_rows.extend(train_condition(args, condition, center, base_state, eval_batch, seed, device))
    return data_rows, train_rows


def aggregate_rows(rows: list[dict], keys: list[str], metrics: list[str]) -> list[dict]:
    groups: dict[tuple, list[dict]] = {}
    for row in rows:
        groups.setdefault(tuple(row.get(k, "") for k in keys), []).append(row)
    out = []
    for group_key, group_rows in sorted(groups.items()):
        base_row = {k: group_key[i] for i, k in enumerate(keys)}
        base_row["n"] = len(group_rows)
        for metric in metrics:
            vals = []
            for row in group_rows:
                try:
                    val = float(row.get(metric, "nan"))
                except (TypeError, ValueError):
                    val = float("nan")
                if not math.isnan(val):
                    vals.append(val)
            base_row[f"{metric}_mean"] = float(np.mean(vals)) if vals else float("nan")
            base_row[f"{metric}_std"] = float(np.std(vals)) if vals else float("nan")
            base_row[f"{metric}_min"] = float(np.min(vals)) if vals else float("nan")
            base_row[f"{metric}_max"] = float(np.max(vals)) if vals else float("nan")
        out.append(base_row)
    return out


def plot_trajectory(rows: list[dict], metric: str, title: str, path: Path) -> None:
    conditions = sorted({str(r["condition"]) for r in rows})
    plt.figure(figsize=(8.5, 5.0))
    for condition in conditions:
        cond_rows = sorted([r for r in rows if str(r["condition"]) == condition], key=lambda r: int(r["checkpoint"]))
        xs = [int(r["checkpoint"]) for r in cond_rows]
        ys = [float(r[f"{metric}_mean"]) for r in cond_rows]
        plt.plot(xs, ys, marker="o", linewidth=1.6, label=condition)
    plt.xlabel("checkpoint")
    plt.ylabel(metric)
    plt.title(title)
    plt.legend(fontsize=8)
    plt.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(path, dpi=180)
    plt.close()


def plot_final_bar(rows: list[dict], metric: str, title: str, path: Path) -> None:
    conditions = [str(r["condition"]) for r in rows]
    vals = [float(r[f"{metric}_mean"]) for r in rows]
    plt.figure(figsize=(8.0, 4.6))
    plt.bar(range(len(conditions)), vals, color="#4C78A8")
    plt.xticks(range(len(conditions)), conditions, rotation=25, ha="right")
    plt.ylabel(metric)
    plt.title(title)
    plt.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(path, dpi=180)
    plt.close()


def summarize_and_plot(output_dir: Path, args: argparse.Namespace, run_name: str) -> dict:
    partial_dir = output_dir / "partials" / run_name
    data_rows: list[dict] = []
    train_rows: list[dict] = []
    for path in sorted(partial_dir.glob("data_audit_rank*.csv")):
        data_rows.extend(read_csv(path))
    for path in sorted(partial_dir.glob("training_trajectory_rank*.csv")):
        train_rows.extend(read_csv(path))
    table_dir = output_dir / "tables"
    fig_dir = output_dir / "figures"
    write_csv(table_dir / "data_audit.csv", data_rows)
    write_csv(table_dir / "training_trajectory.csv", train_rows)
    metrics = [
        "allpos_feature_NMI",
        "predpos_feature_NMI",
        "lastpred_feature_NMI",
        "matched_preserve_fraction",
        "margin_mean",
        "margin_p05",
        "pred_margin_p05",
        "last_margin_p05",
        "positive_margin_frac",
        "sign_flip_rate",
        "max_load",
        "effective_experts",
        "next_token_accuracy",
        "loss",
    ]
    trajectory = aggregate_rows(train_rows, ["condition", "checkpoint"], metrics)
    final_step = max(int(r["checkpoint"]) for r in train_rows) if train_rows else 0
    reinit = aggregate_rows([r for r in train_rows if int(r["checkpoint"]) == 0], ["condition"], metrics)
    final = aggregate_rows([r for r in train_rows if int(r["checkpoint"]) == final_step], ["condition"], metrics)
    write_csv(table_dir / "condition_trajectory_aggregate.csv", trajectory)
    write_csv(table_dir / "condition_aggregate_reinit.csv", reinit)
    write_csv(table_dir / "condition_aggregate_final.csv", final)
    if trajectory:
        plot_trajectory(trajectory, "allpos_feature_NMI", "All-position feature NMI trajectory", fig_dir / "allpos_feature_nmi_trajectory.png")
        plot_trajectory(trajectory, "margin_p05", "All-position margin p05 trajectory", fig_dir / "margin_p05_trajectory.png")
        plot_trajectory(trajectory, "next_token_accuracy", "Next-token accuracy trajectory", fig_dir / "next_token_accuracy_trajectory.png")
    if final:
        plot_final_bar(final, "allpos_feature_NMI", "Final all-position feature NMI", fig_dir / "final_allpos_feature_nmi.png")
        plot_final_bar(final, "margin_p05", "Final all-position margin p05", fig_dir / "final_margin_p05.png")

    def find(rows: list[dict], condition: str, metric: str) -> float:
        for row in rows:
            if str(row.get("condition")) == condition:
                return float(row.get(f"{metric}_mean", "nan"))
        return float("nan")

    key = {
        "completed_seeds": len({int(r["seed"]) for r in train_rows}) if train_rows else 0,
        "completed_training_rows": len(train_rows),
        "final_step": final_step,
        "oracle_allpos_step0_nmi": find(reinit, "oracle_allpos", "allpos_feature_NMI"),
        "oracle_allpos_step0_margin_p05": find(reinit, "oracle_allpos", "margin_p05"),
        "oracle_allpos_final_nmi": find(final, "oracle_allpos", "allpos_feature_NMI"),
        "oracle_allpos_final_margin_p05": find(final, "oracle_allpos", "margin_p05"),
        "oracle_predpos_final_nmi": find(final, "oracle_predpos", "allpos_feature_NMI"),
        "oracle_predpos_final_margin_p05": find(final, "oracle_predpos", "margin_p05"),
        "oracle_lastpred_final_nmi": find(final, "oracle_lastpred", "allpos_feature_NMI"),
        "oracle_lastpred_final_margin_p05": find(final, "oracle_lastpred", "margin_p05"),
        "random_final_nmi": find(final, "random", "allpos_feature_NMI"),
        "random_final_margin_p05": find(final, "random", "margin_p05"),
    }
    verdict = "insufficient"
    if key["completed_seeds"] >= int(args.expected_seeds):
        ideal_margins = [
            key["oracle_allpos_final_margin_p05"],
            key["oracle_predpos_final_margin_p05"],
            key["oracle_lastpred_final_margin_p05"],
        ]
        ideal_nmis = [
            key["oracle_allpos_final_nmi"],
            key["oracle_predpos_final_nmi"],
            key["oracle_lastpred_final_nmi"],
        ]
        if min(ideal_margins) > 0.0 and min(ideal_nmis) >= 0.95:
            verdict = "supports_background_noise_hypothesis"
        else:
            verdict = "weakens_background_noise_sufficiency"
    summary = {
        "experiment_id": EXPERIMENT_ID,
        "run_name": run_name,
        "run_stage": args.run_stage,
        "verdict": verdict,
        "key_metrics": key,
        "config": vars(args),
        "generated_at_unix": time.time(),
        "tables": {
            "data_audit": str(table_dir / "data_audit.csv"),
            "training_trajectory": str(table_dir / "training_trajectory.csv"),
            "condition_trajectory_aggregate": str(table_dir / "condition_trajectory_aggregate.csv"),
            "condition_aggregate_reinit": str(table_dir / "condition_aggregate_reinit.csv"),
            "condition_aggregate_final": str(table_dir / "condition_aggregate_final.csv"),
        },
        "figures": {
            "allpos_feature_nmi_trajectory": str(fig_dir / "allpos_feature_nmi_trajectory.png"),
            "margin_p05_trajectory": str(fig_dir / "margin_p05_trajectory.png"),
            "next_token_accuracy_trajectory": str(fig_dir / "next_token_accuracy_trajectory.png"),
            "final_allpos_feature_nmi": str(fig_dir / "final_allpos_feature_nmi.png"),
            "final_margin_p05": str(fig_dir / "final_margin_p05.png"),
        },
    }
    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-stage", choices=["smoke", "full"], default="full")
    parser.add_argument("--run-name", default=f"{EXPERIMENT_ID}_{int(time.time())}")
    parser.add_argument("--output-dir", default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument("--seeds", default="0 1 2 3 4 5 6 7")
    parser.add_argument("--expected-seeds", type=int, default=8)
    parser.add_argument("--seq-len", type=int, default=32)
    parser.add_argument("--num-features", type=int, default=4)
    parser.add_argument("--num-experts", type=int, default=4)
    parser.add_argument("--num-neutral-tokens", type=int, default=32)
    parser.add_argument("--d-model", type=int, default=64)
    parser.add_argument("--num-heads", type=int, default=4)
    parser.add_argument("--d-ff", type=int, default=128)
    parser.add_argument("--calib-samples", type=int, default=2048)
    parser.add_argument("--eval-samples", type=int, default=2048)
    parser.add_argument("--train-batch-size", type=int, default=256)
    parser.add_argument("--eval-batch-size", type=int, default=512)
    parser.add_argument("--train-steps", type=int, default=2000)
    parser.add_argument("--checkpoints", default="160 500 1000 2000")
    parser.add_argument("--lr", type=float, default=2e-3)
    parser.add_argument("--weight-decay", type=float, default=1e-4)
    parser.add_argument("--grad-clip", type=float, default=1.0)
    parser.add_argument("--router-init-scale", type=float, default=1.5)
    args = parser.parse_args()

    if args.run_stage == "smoke":
        args.seeds = "0"
        args.expected_seeds = 1
        args.calib_samples = min(args.calib_samples, 512)
        args.eval_samples = min(args.eval_samples, 512)
        args.train_steps = min(args.train_steps, 20)
        args.checkpoints = "5 20"

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    output_dir = Path(args.output_dir).resolve()
    run_name = args.run_name
    partial_dir = output_dir / "partials" / run_name
    partial_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "figures").mkdir(parents=True, exist_ok=True)
    (output_dir / "run_config.json").write_text(json.dumps(vars(args), indent=2), encoding="utf-8")

    print(json.dumps({"event": "start", "device": str(device), "run_stage": args.run_stage, "run_name": run_name}), flush=True)
    data_rows: list[dict] = []
    train_rows: list[dict] = []
    for seed in parse_int_list(args.seeds):
        cell_data, cell_train = run_cell(args, seed, device)
        data_rows.extend(cell_data)
        train_rows.extend(cell_train)
        print(json.dumps({"event": "cell_done", "seed": seed}), flush=True)
    write_csv(partial_dir / "data_audit_rank0.csv", data_rows)
    write_csv(partial_dir / "training_trajectory_rank0.csv", train_rows)
    summary = summarize_and_plot(output_dir, args, run_name)
    print(json.dumps({"event": "summary", "summary": summary}, indent=2), flush=True)


if __name__ == "__main__":
    main()

