#!/usr/bin/env python3
"""A07_05 controlled common-update interference diagnostic.

The experiment asks whether a common-example gradient step causally increases
rare/conflict loss more than norm-matched controls from the same checkpoint.
It intentionally tests the update mechanism only; it is not a MoE utility run.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple

import numpy as np

os.environ.setdefault("PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION", "python")

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.nn.utils import parameters_to_vector, vector_to_parameters


COMMON_GROUPS = (0, 2)
RARE_GROUPS = (1, 3)


@dataclass
class Split:
    x: torch.Tensor
    y: torch.Tensor
    group: torch.Tensor
    parent: torch.Tensor
    rare: torch.Tensor
    position: torch.Tensor
    nuisance: torch.Tensor


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--config", required=True)
    p.add_argument("--run-name", required=True)
    p.add_argument("--run-stage", choices=["smoke", "full"], default="full")
    p.add_argument("--seeds", default="")
    p.add_argument("--shard-index", type=int, default=0)
    p.add_argument("--num-shards", type=int, default=1)
    p.add_argument("--aggregate-only", action="store_true")
    p.add_argument("--device", default="cpu")
    return p.parse_args()


def load_config(path: str) -> Dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def seed_list(cfg: Dict, override: str) -> List[int]:
    if override:
        return [int(x.strip()) for x in override.split(",") if x.strip()]
    return [int(x) for x in cfg["seeds"]]


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def rows_to_csv(path: Path, rows: Sequence[Dict]) -> None:
    ensure_dir(path.parent)
    if not rows:
        return
    fields: List[str] = []
    for row in rows:
        for key in row.keys():
            if key not in fields:
                fields.append(key)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def read_csvs(paths: Iterable[Path]) -> List[Dict]:
    rows: List[Dict] = []
    for path in paths:
        if not path.exists():
            continue
        with open(path, newline="", encoding="utf-8") as f:
            rows.extend(list(csv.DictReader(f)))
    return rows


def unit_vectors(rng: np.random.Generator, count: int, dim: int) -> np.ndarray:
    x = rng.normal(size=(count, dim))
    x /= np.linalg.norm(x, axis=1, keepdims=True) + 1e-12
    return x


def make_split(cfg: Dict, seed: int, stage: str, split: str, device: torch.device) -> Split:
    data = cfg["data"]
    rng = np.random.default_rng(seed + (0 if split == "train" else 100000))
    dim = int(data["input_dim"])
    if stage == "smoke":
        common_n = int(data["smoke_train_common_per_group"] if split == "train" else data["smoke_eval_per_group"])
        rare_n = int(data["smoke_train_rare_per_group"] if split == "train" else data["smoke_eval_per_group"])
    else:
        common_n = int(data["train_common_per_group"] if split == "train" else data["eval_per_group"])
        rare_n = int(data["train_rare_per_group"] if split == "train" else data["eval_per_group"])

    common_vec = unit_vectors(np.random.default_rng(seed + 11), 1, dim)[0]
    parent_vec = unit_vectors(np.random.default_rng(seed + 12), 2, dim)
    rare_vec = unit_vectors(np.random.default_rng(seed + 13), 2, dim)
    group_vec = unit_vectors(np.random.default_rng(seed + 14), 4, dim)
    nuisance_vec = unit_vectors(np.random.default_rng(seed + 15), 4, dim)
    position_vec = unit_vectors(np.random.default_rng(seed + 16), 4, dim)

    xs: List[np.ndarray] = []
    ys: List[int] = []
    groups: List[int] = []
    parents: List[int] = []
    rares: List[int] = []
    positions: List[int] = []
    nuisances: List[int] = []
    for group in range(4):
        parent = group // 2
        rare = group % 2
        n = rare_n if rare else common_n
        for _ in range(n):
            pos = int(rng.integers(0, 4))
            nui = int(rng.integers(0, 4))
            x = (
                float(data["global_common_strength"]) * common_vec
                + float(data["parent_strength"]) * parent_vec[parent]
                + float(data["group_marker_strength"]) * group_vec[group]
                + float(data["nuisance_strength"]) * nuisance_vec[nui]
                + float(data["position_strength"]) * position_vec[pos]
                + rng.normal(scale=float(data["noise_std"]), size=dim)
            )
            if rare:
                x = x + float(data["rare_marker_strength"]) * rare_vec[parent]
            else:
                x = x + float(data["common_marker_strength"]) * group_vec[group]
            xs.append(x.astype(np.float32))
            ys.append(group)
            groups.append(group)
            parents.append(parent)
            rares.append(rare)
            positions.append(pos)
            nuisances.append(nui)

    order = np.arange(len(xs))
    rng.shuffle(order)
    return Split(
        x=torch.tensor(np.stack(xs)[order], dtype=torch.float32, device=device),
        y=torch.tensor(np.asarray(ys, dtype=np.int64)[order], dtype=torch.long, device=device),
        group=torch.tensor(np.asarray(groups, dtype=np.int64)[order], dtype=torch.long, device=device),
        parent=torch.tensor(np.asarray(parents, dtype=np.int64)[order], dtype=torch.long, device=device),
        rare=torch.tensor(np.asarray(rares, dtype=np.int64)[order], dtype=torch.long, device=device),
        position=torch.tensor(np.asarray(positions, dtype=np.int64)[order], dtype=torch.long, device=device),
        nuisance=torch.tensor(np.asarray(nuisances, dtype=np.int64)[order], dtype=torch.long, device=device),
    )


def make_unrelated_split(cfg: Dict, seed: int, stage: str, device: torch.device) -> Tuple[torch.Tensor, torch.Tensor]:
    data = cfg["data"]
    rng = np.random.default_rng(seed + 300000)
    dim = int(data["input_dim"])
    n = int(data["smoke_unrelated_train"] if stage == "smoke" else data["unrelated_train"])
    nuisance_vec = unit_vectors(np.random.default_rng(seed + 31), 8, dim)
    xs: List[np.ndarray] = []
    ys: List[int] = []
    for i in range(n):
        nui = int(rng.integers(0, 8))
        x = (
            float(data["unrelated_strength"]) * nuisance_vec[nui]
            + rng.normal(scale=float(data["unrelated_noise_std"]), size=dim)
        )
        xs.append(x.astype(np.float32))
        ys.append(i % 4)
    order = np.arange(n)
    rng.shuffle(order)
    return (
        torch.tensor(np.stack(xs)[order], dtype=torch.float32, device=device),
        torch.tensor(np.asarray(ys, dtype=np.int64)[order], dtype=torch.long, device=device),
    )


class ProbeMLP(nn.Module):
    def __init__(self, input_dim: int, hidden_dim: int, output_dim: int, dropout: float):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.Tanh(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim, output_dim),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.net(x)


def make_model(cfg: Dict, device: torch.device) -> ProbeMLP:
    return ProbeMLP(
        int(cfg["data"]["input_dim"]),
        int(cfg["model"]["hidden_dim"]),
        4,
        float(cfg["model"]["dropout"]),
    ).to(device)


def batch_indices(n: int, batch_size: int, device: torch.device) -> torch.Tensor:
    return torch.randint(0, n, (batch_size,), device=device)


def train_common_warmup(cfg: Dict, model: nn.Module, train: Split, stage: str) -> List[Dict]:
    training = cfg["training"]
    steps = int(training["smoke_warmup_steps"] if stage == "smoke" else training["warmup_steps"])
    batch_size = int(training["batch_size"])
    opt = torch.optim.AdamW(
        model.parameters(),
        lr=float(training["lr"]),
        weight_decay=float(training["weight_decay"]),
    )
    common_mask = train.rare == 0
    x_common = train.x[common_mask]
    y_common = train.y[common_mask]
    trace: List[Dict] = []
    for step in range(steps):
        idx = batch_indices(x_common.shape[0], batch_size, x_common.device)
        logits = model(x_common[idx])
        loss = F.cross_entropy(logits, y_common[idx])
        opt.zero_grad(set_to_none=True)
        loss.backward()
        opt.step()
        if step in (0, steps - 1):
            trace.append({"warmup_step": step, "common_train_loss": float(loss.detach().item())})
    return trace


@torch.no_grad()
def eval_metrics(model: nn.Module, split: Split) -> Dict:
    model.eval()
    logits = model(split.x)
    loss = F.cross_entropy(logits, split.y, reduction="none")
    pred = logits.argmax(dim=-1)
    out: Dict[str, float] = {
        "total_loss": float(loss.mean().item()),
        "total_acc": float((pred == split.y).float().mean().item()),
    }
    for name, groups in [("common", COMMON_GROUPS), ("rare", RARE_GROUPS)]:
        mask = torch.zeros_like(split.rare, dtype=torch.bool)
        for group in groups:
            mask = mask | (split.group == group)
        out[f"{name}_loss"] = float(loss[mask].mean().item())
        out[f"{name}_acc"] = float((pred[mask] == split.y[mask]).float().mean().item())
    for group in range(4):
        mask = split.group == group
        out[f"group_{group}_loss"] = float(loss[mask].mean().item())
        out[f"group_{group}_acc"] = float((pred[mask] == split.y[mask]).float().mean().item())
    return out


def grad_vector(model: nn.Module, x: torch.Tensor, y: torch.Tensor, batch_size: int) -> Tuple[torch.Tensor, float]:
    params = [p for p in model.parameters() if p.requires_grad]
    total = x.shape[0]
    accum = [torch.zeros_like(p, memory_format=torch.preserve_format) for p in params]
    loss_sum = 0.0
    for start in range(0, total, batch_size):
        stop = min(start + batch_size, total)
        logits = model(x[start:stop])
        loss = F.cross_entropy(logits, y[start:stop], reduction="sum")
        grads = torch.autograd.grad(loss, params, retain_graph=False, create_graph=False)
        for i, g in enumerate(grads):
            accum[i] += g.detach()
        loss_sum += float(loss.detach().item())
    flat_grad = torch.cat([(g / max(total, 1)).reshape(-1) for g in accum])
    return -flat_grad, loss_sum / max(total, 1)


def norm_match(direction: torch.Tensor, target_norm: float, eps: float = 1e-12) -> torch.Tensor:
    return direction * (target_norm / float(direction.norm().clamp_min(eps).item()))


def basis_from_vectors(vectors: Sequence[torch.Tensor], threshold: float) -> torch.Tensor:
    mat = torch.stack([v.detach() for v in vectors], dim=1)
    mat = mat - mat.mean(dim=0, keepdim=True) * 0.0
    if mat.numel() == 0:
        return torch.empty((0, 0), device=vectors[0].device)
    u, s, _vh = torch.linalg.svd(mat, full_matrices=False)
    if s.numel() == 0:
        return torch.empty((mat.shape[0], 0), device=mat.device)
    keep = s > (float(s.max().item()) * threshold)
    if not bool(keep.any()):
        keep[0] = True
    return u[:, keep]


def projection_fraction(direction: torch.Tensor, basis: torch.Tensor) -> float:
    if basis.numel() == 0:
        return 0.0
    proj = basis @ (basis.T @ direction)
    return float((proj.norm().pow(2) / direction.norm().clamp_min(1e-12).pow(2)).item())


def projector_overlap(basis_a: torch.Tensor, basis_b: torch.Tensor) -> float:
    if basis_a.numel() == 0 or basis_b.numel() == 0:
        return 0.0
    denom = max(min(basis_a.shape[1], basis_b.shape[1]), 1)
    return float(((basis_a.T @ basis_b).pow(2).sum() / denom).item())


def mask_for_groups(group: torch.Tensor, groups: Sequence[int]) -> torch.Tensor:
    mask = torch.zeros_like(group, dtype=torch.bool)
    for item in groups:
        mask = mask | (group == item)
    return mask


def split_half_mask(base_mask: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
    idx = base_mask.nonzero(as_tuple=False).flatten()
    half = idx.numel() // 2
    mask_a = torch.zeros_like(base_mask, dtype=torch.bool)
    mask_b = torch.zeros_like(base_mask, dtype=torch.bool)
    mask_a[idx[:half]] = True
    mask_b[idx[half:]] = True
    return mask_a, mask_b


def apply_and_eval(
    model: nn.Module,
    base_vec: torch.Tensor,
    direction: torch.Tensor,
    step_scale: float,
    eval_split: Split,
) -> Dict:
    vector_to_parameters(base_vec + step_scale * direction, model.parameters())
    metrics = eval_metrics(model, eval_split)
    vector_to_parameters(base_vec, model.parameters())
    return metrics


def run_seed(cfg: Dict, seed: int, stage: str, device: torch.device) -> Dict[str, List[Dict]]:
    torch.manual_seed(seed)
    np.random.seed(seed)
    random.seed(seed)

    train = make_split(cfg, seed, stage, "train", device)
    eval_split = make_split(cfg, seed, stage, "eval", device)
    unrelated_x, unrelated_y = make_unrelated_split(cfg, seed, stage, device)

    model = make_model(cfg, device)
    trace_rows = train_common_warmup(cfg, model, train, stage)
    model.eval()

    eval_batch_size = int(cfg["training"]["eval_batch_size"])
    common_mask = train.rare == 0
    rare_mask = train.rare == 1
    baseline = eval_metrics(model, eval_split)
    common_update, common_train_loss = grad_vector(model, train.x[common_mask], train.y[common_mask], eval_batch_size)
    rare_update, rare_train_loss = grad_vector(model, train.x[rare_mask], train.y[rare_mask], eval_batch_size)
    unrelated_update, unrelated_train_loss = grad_vector(model, unrelated_x, unrelated_y, eval_batch_size)

    common_group_updates: List[torch.Tensor] = []
    common_group_updates_a: List[torch.Tensor] = []
    common_group_updates_b: List[torch.Tensor] = []
    projection_rows: List[Dict] = []
    for group in COMMON_GROUPS:
        g_mask = train.group == group
        update, train_loss = grad_vector(model, train.x[g_mask], train.y[g_mask], eval_batch_size)
        common_group_updates.append(update)
        mask_a, mask_b = split_half_mask(g_mask)
        update_a, _ = grad_vector(model, train.x[mask_a], train.y[mask_a], eval_batch_size)
        update_b, _ = grad_vector(model, train.x[mask_b], train.y[mask_b], eval_batch_size)
        common_group_updates_a.append(update_a)
        common_group_updates_b.append(update_b)
        projection_rows.append(
            {
                "seed": seed,
                "row_type": "common_group_update",
                "group": group,
                "update_norm": float(update.norm().item()),
                "train_loss": train_loss,
            }
        )

    basis = basis_from_vectors(common_group_updates, float(cfg["projection"]["svd_threshold"]))
    basis_a = basis_from_vectors(common_group_updates_a, float(cfg["projection"]["svd_threshold"]))
    basis_b = basis_from_vectors(common_group_updates_b, float(cfg["projection"]["svd_threshold"]))
    stability = projector_overlap(basis_a, basis_b)
    rare_fraction_values: List[float] = []
    for group in RARE_GROUPS:
        g_mask = train.group == group
        update, train_loss = grad_vector(model, train.x[g_mask], train.y[g_mask], eval_batch_size)
        frac = projection_fraction(update, basis)
        rare_fraction_values.append(frac)
        projection_rows.append(
            {
                "seed": seed,
                "row_type": "rare_group_projection",
                "group": group,
                "rare_common_update_fraction": frac,
                "update_norm": float(update.norm().item()),
                "train_loss": train_loss,
                "projector_rank": int(basis.shape[1]),
                "projector_stability": stability,
            }
        )

    common_norm = float(common_update.norm().item())
    gen = torch.Generator(device=device)
    gen.manual_seed(seed + 900000)
    random_update = torch.randn(common_update.shape, generator=gen, device=device)

    directions = {
        "common_update": common_update,
        "unrelated_update": unrelated_update,
        "random_update": random_update,
        "rare_update_sanity": rare_update,
    }
    step_scale = float(cfg["perturbation"]["step_scale"])
    base_vec = parameters_to_vector([p.detach() for p in model.parameters()]).detach()
    perturbation_rows: List[Dict] = []
    group_rows: List[Dict] = []
    for name, direction in directions.items():
        matched = norm_match(direction, common_norm)
        after = apply_and_eval(model, base_vec, matched, step_scale, eval_split)
        row = {
            "seed": seed,
            "perturbation": name,
            "step_scale": step_scale,
            "direction_norm_raw": float(direction.norm().item()),
            "direction_norm_applied": float(matched.norm().item()),
            "baseline_common_loss": baseline["common_loss"],
            "baseline_rare_loss": baseline["rare_loss"],
            "after_common_loss": after["common_loss"],
            "after_rare_loss": after["rare_loss"],
            "common_loss_delta": after["common_loss"] - baseline["common_loss"],
            "rare_loss_delta": after["rare_loss"] - baseline["rare_loss"],
            "baseline_common_acc": baseline["common_acc"],
            "baseline_rare_acc": baseline["rare_acc"],
            "after_common_acc": after["common_acc"],
            "after_rare_acc": after["rare_acc"],
            "common_acc_delta": after["common_acc"] - baseline["common_acc"],
            "rare_acc_delta": after["rare_acc"] - baseline["rare_acc"],
        }
        perturbation_rows.append(row)
        for group in range(4):
            group_rows.append(
                {
                    "seed": seed,
                    "perturbation": name,
                    "group": group,
                    "baseline_group_loss": baseline[f"group_{group}_loss"],
                    "after_group_loss": after[f"group_{group}_loss"],
                    "group_loss_delta": after[f"group_{group}_loss"] - baseline[f"group_{group}_loss"],
                    "baseline_group_acc": baseline[f"group_{group}_acc"],
                    "after_group_acc": after[f"group_{group}_acc"],
                    "group_acc_delta": after[f"group_{group}_acc"] - baseline[f"group_{group}_acc"],
                }
            )

    rare_delta = {r["perturbation"]: r["rare_loss_delta"] for r in perturbation_rows}
    common_delta = {r["perturbation"]: r["common_loss_delta"] for r in perturbation_rows}
    stage_rows = [
        {
            "seed": seed,
            "stage": stage,
            "baseline_common_loss": baseline["common_loss"],
            "baseline_rare_loss": baseline["rare_loss"],
            "baseline_rare_common_loss_gap": baseline["rare_loss"] - baseline["common_loss"],
            "baseline_common_acc": baseline["common_acc"],
            "baseline_rare_acc": baseline["rare_acc"],
            "common_update_train_loss": common_train_loss,
            "rare_update_train_loss": rare_train_loss,
            "unrelated_update_train_loss": unrelated_train_loss,
            "common_update_norm": common_norm,
            "rare_update_norm": float(rare_update.norm().item()),
            "unrelated_update_norm": float(unrelated_update.norm().item()),
            "projector_rank": int(basis.shape[1]),
            "projector_stability": stability,
            "rare_common_update_fraction": float(np.mean(rare_fraction_values)),
            "common_to_rare_loss_effect_vs_random": rare_delta["common_update"] - rare_delta["random_update"],
            "common_to_rare_loss_effect_vs_unrelated": rare_delta["common_update"] - rare_delta["unrelated_update"],
            "common_to_rare_loss_effect": rare_delta["common_update"] - max(
                rare_delta["random_update"], rare_delta["unrelated_update"]
            ),
            "common_update_rare_loss_delta": rare_delta["common_update"],
            "random_update_rare_loss_delta": rare_delta["random_update"],
            "unrelated_update_rare_loss_delta": rare_delta["unrelated_update"],
            "rare_update_sanity_rare_loss_delta": rare_delta["rare_update_sanity"],
            "common_update_common_loss_delta": common_delta["common_update"],
        }
    ]
    for row in trace_rows:
        row["seed"] = seed
        row["stage"] = stage

    return {
        "stage": stage_rows,
        "warmup_trace": trace_rows,
        "perturbation": perturbation_rows,
        "projection": projection_rows,
        "group_loss": group_rows,
    }


def mean_rows(rows: Sequence[Dict], keys: Sequence[str], values: Sequence[str]) -> List[Dict]:
    buckets: Dict[Tuple, List[Dict]] = {}
    for row in rows:
        buckets.setdefault(tuple(row[k] for k in keys), []).append(row)
    out: List[Dict] = []
    for key, vals in sorted(buckets.items()):
        item = {k: v for k, v in zip(keys, key)}
        for value in values:
            arr = np.asarray([float(v[value]) for v in vals if v.get(value, "") != ""], dtype=float)
            if arr.size == 0:
                continue
            item[value] = float(arr.mean())
            item[f"{value}_std"] = float(arr.std(ddof=0))
        item["n"] = len(vals)
        out.append(item)
    return out


def write_json(path: Path, item: Dict) -> None:
    ensure_dir(path.parent)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(item, f, indent=2)


def plot_tables(curated_dir: Path, run_dir: Path, perturb_summary: List[Dict], projection_summary: List[Dict]) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    order = ["common_update", "random_update", "unrelated_update", "rare_update_sanity"]
    by_name = {r["perturbation"]: r for r in perturb_summary}
    xs = [x for x in order if x in by_name]
    vals = [float(by_name[x]["rare_loss_delta"]) for x in xs]
    errs = [float(by_name[x].get("rare_loss_delta_std", 0.0)) for x in xs]
    colors = ["#d95f02", "#7570b3", "#1b9e77", "#66a61e"][: len(xs)]
    fig, ax = plt.subplots(figsize=(6.2, 3.6))
    ax.axhline(0.0, color="#444444", linewidth=0.8)
    ax.bar(xs, vals, yerr=errs, color=colors, alpha=0.85)
    ax.set_ylabel("rare loss delta")
    ax.set_title("A07_05 one-step perturbation effect")
    ax.tick_params(axis="x", rotation=20)
    fig.tight_layout()
    ensure_dir(curated_dir / "figures")
    ensure_dir(run_dir / "figures")
    fig.savefig(curated_dir / "figures" / "rare_loss_effect.png", dpi=180)
    fig.savefig(run_dir / "figures" / "rare_loss_effect.png", dpi=180)
    plt.close(fig)

    rare_rows = [r for r in projection_summary if r.get("row_type") == "rare_group_projection"]
    names = [f"group {int(r['group'])}" for r in rare_rows]
    vals = [float(r["rare_common_update_fraction"]) for r in rare_rows]
    errs = [float(r.get("rare_common_update_fraction_std", 0.0)) for r in rare_rows]
    fig, ax = plt.subplots(figsize=(5.6, 3.4))
    ax.bar(names, vals, yerr=errs, color="#4e79a7", alpha=0.85)
    ax.set_ylim(0.0, min(1.0, max(vals + [0.1]) * 1.25))
    ax.set_ylabel("fraction of rare update in common subspace")
    ax.set_title("A07_05 rare update projection")
    fig.tight_layout()
    fig.savefig(curated_dir / "figures" / "projection_fraction.png", dpi=180)
    fig.savefig(run_dir / "figures" / "projection_fraction.png", dpi=180)
    plt.close(fig)


def aggregate(cfg: Dict, run_dir: Path) -> None:
    shard_dir = run_dir / "shards"
    all_rows = {
        key: read_csvs(sorted(shard_dir.glob(f"*__{key}.csv")))
        for key in ["stage", "warmup_trace", "perturbation", "projection", "group_loss"]
    }
    ensure_dir(run_dir / "tables")
    for key, rows in all_rows.items():
        rows_to_csv(run_dir / "tables" / f"{key}_by_seed.csv", rows)

    stage_summary = mean_rows(
        all_rows["stage"],
        ["stage"],
        [
            "baseline_common_loss",
            "baseline_rare_loss",
            "baseline_rare_common_loss_gap",
            "baseline_common_acc",
            "baseline_rare_acc",
            "common_update_norm",
            "rare_update_norm",
            "unrelated_update_norm",
            "projector_rank",
            "projector_stability",
            "rare_common_update_fraction",
            "common_to_rare_loss_effect_vs_random",
            "common_to_rare_loss_effect_vs_unrelated",
            "common_to_rare_loss_effect",
            "common_update_rare_loss_delta",
            "random_update_rare_loss_delta",
            "unrelated_update_rare_loss_delta",
            "rare_update_sanity_rare_loss_delta",
            "common_update_common_loss_delta",
        ],
    )
    perturb_summary = mean_rows(
        all_rows["perturbation"],
        ["perturbation"],
        [
            "direction_norm_raw",
            "direction_norm_applied",
            "baseline_common_loss",
            "baseline_rare_loss",
            "after_common_loss",
            "after_rare_loss",
            "common_loss_delta",
            "rare_loss_delta",
            "common_acc_delta",
            "rare_acc_delta",
        ],
    )
    projection_summary = mean_rows(
        all_rows["projection"],
        ["row_type", "group"],
        ["rare_common_update_fraction", "update_norm", "train_loss", "projector_rank", "projector_stability"],
    )
    group_summary = mean_rows(
        all_rows["group_loss"],
        ["perturbation", "group"],
        ["baseline_group_loss", "after_group_loss", "group_loss_delta", "group_acc_delta"],
    )
    rows_to_csv(run_dir / "tables" / "stage_summary.csv", stage_summary)
    rows_to_csv(run_dir / "tables" / "perturbation_summary.csv", perturb_summary)
    rows_to_csv(run_dir / "tables" / "projection_summary.csv", projection_summary)
    rows_to_csv(run_dir / "tables" / "group_loss_delta_summary.csv", group_summary)

    thresholds = cfg["thresholds"]
    stage = stage_summary[0] if stage_summary else {}
    decision = {
        "run_name": run_dir.name,
        "n_seeds": int(stage.get("n", 0)) if stage else 0,
        "common_to_rare_loss_effect": float(stage.get("common_to_rare_loss_effect", 0.0)) if stage else 0.0,
        "common_update_rare_loss_delta": float(stage.get("common_update_rare_loss_delta", 0.0)) if stage else 0.0,
        "rare_update_sanity_rare_loss_delta": float(stage.get("rare_update_sanity_rare_loss_delta", 0.0)) if stage else 0.0,
        "rare_common_update_fraction": float(stage.get("rare_common_update_fraction", 0.0)) if stage else 0.0,
        "projector_stability": float(stage.get("projector_stability", 0.0)) if stage else 0.0,
        "baseline_rare_common_loss_gap": float(stage.get("baseline_rare_common_loss_gap", 0.0)) if stage else 0.0,
    }
    decision["passes_common_harm"] = bool(
        decision["common_update_rare_loss_delta"] > float(thresholds["common_rare_delta_min"])
        and decision["common_to_rare_loss_effect"] > float(thresholds["effect_margin_min"])
    )
    decision["passes_projection_guard"] = bool(
        decision["rare_common_update_fraction"] > float(thresholds["rare_projection_fraction_min"])
        and decision["projector_stability"] > float(thresholds["projector_stability_min"])
    )
    decision["passes_rare_sanity"] = bool(
        decision["rare_update_sanity_rare_loss_delta"] <= float(thresholds["rare_update_sanity_max_delta"])
    )
    decision["passes_underlearning_guard"] = bool(
        decision["baseline_rare_common_loss_gap"] > float(thresholds["rare_underlearning_gap_min"])
    )
    decision["anchor_decision"] = (
        "supported"
        if decision["passes_common_harm"]
        and decision["passes_projection_guard"]
        and decision["passes_rare_sanity"]
        and decision["passes_underlearning_guard"]
        else "weakened_or_insufficient"
    )
    rows_to_csv(run_dir / "tables" / "decision_summary.csv", [decision])
    write_json(run_dir / "decision_summary.json", decision)

    curated_dir = Path(cfg["output"]["research_experiment_dir"])
    ensure_dir(curated_dir / "tables")
    ensure_dir(curated_dir / "figures")
    for name in [
        "stage_by_seed.csv",
        "perturbation_by_seed.csv",
        "projection_by_seed.csv",
        "group_loss_by_seed.csv",
        "stage_summary.csv",
        "perturbation_summary.csv",
        "projection_summary.csv",
        "group_loss_delta_summary.csv",
        "decision_summary.csv",
    ]:
        src = run_dir / "tables" / name
        if src.exists():
            dst = curated_dir / "tables" / name
            dst.write_bytes(src.read_bytes())
    plot_tables(curated_dir, run_dir, perturb_summary, projection_summary)

    manifest = {
        "run_name": run_dir.name,
        "result_dir": str(run_dir),
        "curated_dir": str(curated_dir),
        "config": cfg,
        "seeds": sorted({int(r["seed"]) for r in all_rows["stage"]}),
        "decision": decision,
        "note": "Controlled common-update perturbation diagnostic; no real-data utility claim.",
    }
    write_json(run_dir / "run_manifest.json", manifest)
    write_json(curated_dir / "run_manifest.json", manifest)


def resolve_device(device_arg: str) -> torch.device:
    if device_arg.startswith("cuda") and torch.cuda.is_available():
        return torch.device(device_arg)
    return torch.device("cpu")


def main() -> None:
    args = parse_args()
    cfg = load_config(args.config)
    root = Path(__file__).resolve().parents[1]
    result_base = root.parents[1] / cfg["output"]["result_dir"]
    run_dir = result_base / args.run_name
    ensure_dir(run_dir / "shards")

    if args.aggregate_only:
        aggregate(cfg, run_dir)
        print(f"aggregated {args.run_name} -> {run_dir}")
        return

    device = resolve_device(args.device)
    seeds = seed_list(cfg, args.seeds)
    my_seeds = [s for i, s in enumerate(seeds) if i % args.num_shards == args.shard_index]
    for seed in my_seeds:
        result = run_seed(cfg, seed, args.run_stage, device)
        for key, rows in result.items():
            rows_to_csv(run_dir / "shards" / f"seed_{seed}__{key}.csv", rows)
        print(f"completed seed={seed} stage={args.run_stage} device={device} shard={args.shard_index}/{args.num_shards}")


if __name__ == "__main__":
    main()
