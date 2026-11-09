#!/usr/bin/env python3
"""A06_01 common-filtered expert-spectrum router initialization experiment."""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import importlib.util
import json
import math
import os
import random
import socket
from contextlib import contextmanager
from pathlib import Path
from types import MethodType
from typing import Any

os.environ.setdefault("PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION", "python")
os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib")

import numpy as np
import torch
import torch.distributed as dist
import torch.nn.functional as F

RESEARCH_ROOT = Path("/data/250010109/Research_System")
EXP_DIR = RESEARCH_ROOT / "Projects/from-attention-to-search/main/experiments/A06/06_01_geometry_and_state_discovery/A06_01_01_E01_common_filtered_spectrum"
BASE_RUNNER = (
    RESEARCH_ROOT
    / "Projects/from-attention-to-search/main/experiments/A06/06_01_geometry_and_state_discovery/A06_01_01_E03_freeze_split_common_stability/scripts/run_freeze_split_common_stability.py"
)
MOE_ROOT = Path("/data/250010109/MoE_Router")


def load_base_runner():
    spec = importlib.util.spec_from_file_location("a06_02_base_runner", BASE_RUNNER)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load base runner from {BASE_RUNNER}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


base = load_base_runner()


def enhanced_load_metrics(routes: torch.Tensor, num_experts: int) -> dict[str, float]:
    counts = torch.bincount(routes.reshape(-1), minlength=num_experts).float()
    total = counts.sum().clamp_min(1.0)
    p = counts / total
    nz = p[p > 0]
    entropy_raw = -(nz * torch.log(nz)).sum() if nz.numel() else torch.tensor(0.0)
    entropy = entropy_raw / math.log(num_experts)
    sorted_counts = torch.sort(counts).values
    n = float(num_experts)
    gini_weights = 2 * torch.arange(1, num_experts + 1, device=counts.device).float() - n - 1
    gini = (gini_weights * sorted_counts).sum() / (n * sorted_counts.sum().clamp_min(1.0))
    return {
        "max_load": float(p.max().item()),
        "routing_entropy": float(entropy.item()),
        "effective_experts": float(torch.exp(entropy_raw).item()),
        "active_experts": int((counts > 0).sum().item()),
        "active_experts_ratio": float((counts > 0).float().mean().item()),
        "gini_load": float(gini.item()),
    }


base.load_metrics = enhanced_load_metrics


def now_slug() -> str:
    return dt.datetime.now().strftime("%Y%m%d_%H%M%S")


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True, default=str), encoding="utf-8")


def append_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, sort_keys=True, default=str) + "\n")


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    out: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                out.append(json.loads(line))
    return out


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fields: list[str] = []
    seen: set[str] = set()
    for row in rows:
        for key in row:
            if key not in seen:
                fields.append(key)
                seen.add(key)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def setup_dist() -> tuple[int, int, int]:
    return base.setup_dist()


def barrier() -> None:
    return base.barrier()


def parse_variant_name(variant: str) -> str:
    return variant.strip()


def orthonormalize(mat: torch.Tensor, max_cols: int | None = None) -> torch.Tensor:
    if mat.numel() == 0:
        return mat
    if max_cols is not None:
        mat = mat[:, :max_cols]
    q, _ = torch.linalg.qr(mat, mode="reduced")
    return q


def project_off_subspace(rows: torch.Tensor, basis: torch.Tensor) -> torch.Tensor:
    if basis.numel() == 0:
        return rows
    return rows - (rows @ basis) @ basis.t()


def normalize_rows(rows: torch.Tensor, target_norm: float, fallback: torch.Tensor | None = None) -> torch.Tensor:
    out = rows.clone()
    norms = out.norm(dim=1, keepdim=True)
    bad = norms.squeeze(1) < 1e-8
    if bad.any() and fallback is not None:
        out[bad] = fallback[bad]
        norms = out.norm(dim=1, keepdim=True)
    out = out / norms.clamp_min(1e-8) * float(target_norm)
    return out


def capture_layer_stats(
    model: torch.nn.Module,
    dataset: Any,
    sample_indices: list[int],
    layer_idx: int,
    args: argparse.Namespace,
    device: torch.device,
) -> dict[str, torch.Tensor | int]:
    model.eval()
    cap = base.GateCapture(model)
    d = args.hidden_size
    sum_h = torch.zeros(d, device=device)
    second = torch.zeros(d, d, device=device)
    sampled: list[torch.Tensor] = []
    sample_count = 0
    count = 0
    with torch.no_grad():
        for start in range(0, len(sample_indices), args.audit_batch_size):
            batch_idx = sample_indices[start : start + args.audit_batch_size]
            x, _ = dataset.batch(batch_idx, device)
            cap.clear()
            _ = model.model(input_ids=x, use_cache=False)
            h, _logits = cap.records[layer_idx]
            hf = h.detach().float()
            sum_h += hf.sum(dim=0)
            second += hf.t() @ hf
            count += hf.shape[0]
            if sample_count < args.max_init_tokens_per_layer:
                take = min(args.max_init_tokens_per_layer - sample_count, hf.shape[0])
                sampled.append(hf[:take].detach().cpu())
                sample_count += take
    cap.close()
    mean = sum_h / max(count, 1)
    cov = second / max(count, 1) - torch.outer(mean, mean)
    h_sample = torch.cat(sampled, dim=0).to(device=device, dtype=torch.float32) if sampled else torch.empty(0, d, device=device)
    return {"mean": mean, "cov": cov, "sample": h_sample, "count": count}


def common_basis(mean: torch.Tensor, cov: torch.Tensor, rank: int) -> torch.Tensor:
    cols: list[torch.Tensor] = []
    if mean.norm() > 1e-8:
        cols.append(mean / mean.norm().clamp_min(1e-8))
    if rank > len(cols):
        evals, evecs = torch.linalg.eigh(cov.float())
        order = torch.argsort(evals, descending=True)
        take = min(rank - len(cols), evecs.shape[1])
        cols.append(evecs[:, order[:take]])
    if not cols:
        return torch.empty(mean.numel(), 0, device=mean.device)
    mat = torch.column_stack([c if c.ndim == 1 else c[:, j] for c in cols for j in range(c.shape[1] if c.ndim > 1 else 1)])
    return orthonormalize(mat, rank)


def expert_energy_subspaces(mlp: torch.nn.Module, k: int) -> tuple[torch.Tensor, torch.Tensor]:
    bases = []
    vals = []
    for expert in mlp.experts:
        wg = expert.gate_proj.weight.detach().float()
        wu = expert.up_proj.weight.detach().float()
        g = wg.t() @ wg + wu.t() @ wu
        evals, evecs = torch.linalg.eigh(g)
        order = torch.argsort(evals, descending=True)[:k]
        bases.append(evecs[:, order])
        vals.append(evals[order].clamp_min(0.0).sqrt())
    return torch.stack(bases, dim=0), torch.stack(vals, dim=0)


def q_raw_from_spectrum(bases: torch.Tensor, sigmas: torch.Tensor, mean: torch.Tensor) -> torch.Tensor:
    rows = []
    for e in range(bases.shape[0]):
        vecs = bases[e]
        weights = sigmas[e]
        signs = torch.sign(mean.view(1, -1) @ vecs).view(-1)
        signs[signs == 0] = 1.0
        q = (vecs * (weights * signs).view(1, -1)).sum(dim=1)
        rows.append(q)
    return torch.stack(rows, dim=0)


def residual_pca_rows(residuals: torch.Tensor, num_experts: int) -> torch.Tensor:
    if residuals.shape[0] < 2:
        return torch.randn(num_experts, residuals.shape[1], device=residuals.device)
    centered = residuals - residuals.mean(dim=0, keepdim=True)
    cov = centered.t() @ centered / max(centered.shape[0] - 1, 1)
    evals, evecs = torch.linalg.eigh(cov.float())
    order = torch.argsort(evals, descending=True)
    vecs = evecs[:, order[:num_experts]].t()
    if vecs.shape[0] < num_experts:
        extra = torch.randn(num_experts - vecs.shape[0], residuals.shape[1], device=residuals.device)
        vecs = torch.cat([vecs, extra], dim=0)
    return vecs


def spectrum_scores(tokens: torch.Tensor, bases: torch.Tensor) -> torch.Tensor:
    scores = []
    for e in range(bases.shape[0]):
        proj = tokens @ bases[e]
        scores.append((proj * proj).sum(dim=1))
    return torch.stack(scores, dim=1)


def init_one_layer(
    model: torch.nn.Module,
    dataset: Any,
    init_indices: list[int],
    variant: str,
    layer_idx: int,
    args: argparse.Namespace,
    device: torch.device,
    seed: int,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    mlp = model.model.layers[layer_idx].mlp
    gate = mlp.gate
    target_norm = float(gate.weight.detach().float().norm(dim=1).mean().item())
    stats = capture_layer_stats(model, dataset, init_indices, layer_idx, args, device)
    mean = stats["mean"]
    cov = stats["cov"]
    h_sample = stats["sample"]
    basis_c = common_basis(mean, cov, args.common_rank_init)
    residuals = project_off_subspace(h_sample, basis_c)
    k = min(args.spectrum_k, args.hidden_size)
    bases, sigmas = expert_energy_subspaces(mlp, k)
    q_raw = q_raw_from_spectrum(bases, sigmas, mean)
    q_res = project_off_subspace(q_raw, basis_c)

    random_w = gate.weight.detach().float().clone()
    if variant == "V0_random_init":
        rows = random_w
    elif variant == "V1_common_orthogonal_random_init":
        rows = project_off_subspace(random_w, basis_c)
    elif variant == "V2_representation_residual_init":
        rows = residual_pca_rows(residuals, args.num_experts)
    elif variant == "V3_raw_spectrum_linear_init":
        rows = q_raw
    elif variant == "V4_common_filtered_spectrum_linear_init":
        rows = q_res
    elif variant == "V5_hybrid_spectrum_to_linear_init":
        scores = spectrum_scores(residuals, bases)
        assign = torch.argmax(scores, dim=1)
        rows_l = []
        for e in range(args.num_experts):
            mask = assign == e
            rows_l.append(residuals[mask].mean(dim=0) if mask.any() else q_res[e])
        rows = torch.stack(rows_l, dim=0)
    else:
        raise ValueError(f"Unknown variant: {variant}")

    fallback = q_res if variant != "V0_random_init" else random_w
    rows = normalize_rows(rows, target_norm, fallback=fallback)
    with torch.no_grad():
        gate.weight.copy_(rows.to(device=device, dtype=gate.weight.dtype))

    overlap_rows: list[dict[str, Any]] = []
    assign_rows: list[dict[str, Any]] = []
    for e in range(args.num_experts):
        s = bases[e]
        overlap_c = float((s.t() @ basis_c).pow(2).sum().item() / max(1, min(s.shape[1], basis_c.shape[1])))
        inter = []
        for f in range(args.num_experts):
            if f == e:
                continue
            inter.append(float((s.t() @ bases[f]).pow(2).sum().item() / max(1, s.shape[1])))
        overlap_rows.append(
            {
                "variant": variant,
                "model_seed": seed,
                "layer": layer_idx,
                "expert": e,
                "spectrum_k": k,
                "common_rank": args.common_rank_init,
                "overlap_with_C": overlap_c,
                "inter_expert_overlap_mean": float(np.mean(inter)) if inter else 0.0,
                "row_norm": float(rows[e].norm().item()),
                "w_dot_c": float((rows[e] @ mean).item()),
            }
        )
    if h_sample.numel() > 0:
        raw_scores = spectrum_scores(h_sample, bases)
        res_scores = spectrum_scores(residuals, bases)
        raw_assign = torch.argmax(raw_scores, dim=1)
        res_assign = torch.argmax(res_scores, dim=1)
        linear_assign = torch.argmax(h_sample @ rows.t(), dim=1)
        for name, assign in [("raw_oracle", raw_assign), ("residual_oracle", res_assign), ("linear_init", linear_assign)]:
            counts = torch.bincount(assign.cpu(), minlength=args.num_experts)
            lm = base.load_metrics(assign.cpu(), args.num_experts)
            assign_rows.append(
                {
                    "variant": variant,
                    "model_seed": seed,
                    "layer": layer_idx,
                    "assignment_type": name,
                    "sample_tokens": int(assign.numel()),
                    "counts_json": json.dumps([int(x) for x in counts.tolist()]),
                    **{f"assign_{k2}": v for k2, v in lm.items()},
                }
            )
        assign_rows.append(
            {
                "variant": variant,
                "model_seed": seed,
                "layer": layer_idx,
                "assignment_type": "agreement",
                "sample_tokens": int(res_assign.numel()),
                "raw_vs_residual_top1_agreement": float((raw_assign == res_assign).float().mean().item()),
                "residual_oracle_to_linear_agreement": float((res_assign == linear_assign).float().mean().item()),
            }
        )
    return overlap_rows, assign_rows


def apply_router_initialization(
    model: torch.nn.Module,
    dataset: Any,
    init_indices: list[int],
    variant: str,
    args: argparse.Namespace,
    device: torch.device,
    seed: int,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    overlap_rows: list[dict[str, Any]] = []
    assign_rows: list[dict[str, Any]] = []
    for layer_idx, _, _ in base.iter_gate_modules(model):
        rows_a, rows_b = init_one_layer(model, dataset, init_indices, variant, layer_idx, args, device, seed)
        overlap_rows.extend(rows_a)
        assign_rows.extend(rows_b)
    return overlap_rows, assign_rows


def train_variant(
    variant: str,
    seed: int,
    dataset: Any,
    init_indices: list[int],
    audit_indices: list[int],
    train_indices: list[int],
    args: argparse.Namespace,
    device: torch.device,
    run_dir: Path,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    model = base.make_model(args.num_experts, seed, args, device)
    overlap_rows, assign_rows = apply_router_initialization(model, dataset, init_indices, variant, args, device, seed)
    params = [p for p in model.parameters() if p.requires_grad]
    opt = torch.optim.AdamW(params, lr=args.learning_rate, weight_decay=0.0)
    rows: list[dict[str, Any]] = []
    grad_rows: list[dict[str, Any]] = []
    ckpt_rows: list[dict[str, Any]] = []
    last_loss = None
    ckpts = set(args.checkpoints)
    train_ptr = 0
    for step in range(0, args.max_train_steps + 1):
        if step in ckpts:
            r, _, _ = base.audit_model(
                model,
                dataset,
                audit_indices[: args.trajectory_audit_num_sequences],
                args,
                device,
                seed,
                args.num_experts,
                step,
                collect_sample=False,
            )
            model_path, gate_path = base.save_checkpoint(model, run_dir / "checkpoints", variant, seed, step, args)
            for row in r:
                row["variant"] = variant
                row["lm_loss"] = last_loss
                rows.append(row)
            ckpt_rows.append(
                {
                    "variant": variant,
                    "model_seed": seed,
                    "step": step,
                    "model_checkpoint": str(model_path.relative_to(run_dir)),
                    "gate_checkpoint": str(gate_path.relative_to(run_dir)),
                    "lm_loss": last_loss,
                }
            )
        if step == args.max_train_steps:
            break
        if train_ptr + args.train_batch_size > len(train_indices):
            random.Random(seed + step).shuffle(train_indices)
            train_ptr = 0
        batch_idx = train_indices[train_ptr : train_ptr + args.train_batch_size]
        train_ptr += args.train_batch_size
        x, y = dataset.batch(batch_idx, device)
        model.train()
        opt.zero_grad(set_to_none=True)
        out = model(input_ids=x, use_cache=False)
        loss = F.cross_entropy(out.logits.reshape(-1, out.logits.shape[-1]), y.reshape(-1))
        loss.backward()
        norms = base.grad_group_norm(model)
        if step + 1 in ckpts or step < args.gradient_log_first_steps:
            grad_rows.append({"variant": variant, "model_seed": seed, "after_backward_step": step, **norms})
        torch.nn.utils.clip_grad_norm_(params, 1.0)
        opt.step()
        last_loss = float(loss.detach().item())
    del model
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    return rows, grad_rows, ckpt_rows, overlap_rows, assign_rows


@contextmanager
def force_layer_expert(model: torch.nn.Module, layer_idx: int, expert_idx: int):
    mlp = model.model.layers[layer_idx].mlp
    original_forward = mlp.forward

    def forced_forward(self, hidden_states, gating_reference=None):
        if gating_reference is None:
            gating_reference = hidden_states
        shared = self.shared_expert(hidden_states)
        bsz, seq_len, hidden_dim = hidden_states.shape
        _, _, gating_dim = gating_reference.shape
        flat = hidden_states.reshape(-1, hidden_dim)
        out = self.experts[expert_idx](flat).reshape(bsz, seq_len, gating_dim)
        selected = torch.full((bsz * seq_len, 1), expert_idx, dtype=torch.long, device=hidden_states.device)
        return out + shared, selected

    mlp.forward = MethodType(forced_forward, mlp)
    try:
        yield
    finally:
        mlp.forward = original_forward


def mean_loss(model: torch.nn.Module, dataset: Any, indices: list[int], args: argparse.Namespace, device: torch.device) -> float:
    total = 0.0
    n = 0
    with torch.no_grad():
        for start in range(0, len(indices), args.audit_batch_size):
            batch_idx = indices[start : start + args.audit_batch_size]
            x, y = dataset.batch(batch_idx, device)
            out = model(input_ids=x, use_cache=False)
            loss = F.cross_entropy(out.logits.reshape(-1, out.logits.shape[-1]), y.reshape(-1), reduction="sum")
            total += float(loss.item())
            n += int(y.numel())
    return total / max(n, 1)


def rankdata(values: list[float]) -> np.ndarray:
    arr = np.asarray(values, dtype=float)
    order = np.argsort(arr)
    ranks = np.empty_like(arr, dtype=float)
    ranks[order] = np.arange(len(arr), dtype=float)
    return ranks


def spearman(x: list[float], y: list[float]) -> float:
    if len(x) < 2 or len(x) != len(y):
        return float("nan")
    rx = rankdata(x)
    ry = rankdata(y)
    if float(rx.std()) == 0.0 or float(ry.std()) == 0.0:
        return float("nan")
    return float(np.corrcoef(rx, ry)[0, 1])


def utility_rows_for_seed(
    variant: str,
    seed: int,
    dataset: Any,
    utility_indices: list[int],
    args: argparse.Namespace,
    device: torch.device,
    run_dir: Path,
) -> list[dict[str, Any]]:
    if variant not in set(args.utility_variants):
        return []
    rows: list[dict[str, Any]] = []
    model = base.make_model(args.num_experts, seed, args, device)
    for step in args.utility_steps:
        ckpt = run_dir / "checkpoints" / f"{variant}_seed{seed}_step{step}.pt"
        if not ckpt.exists():
            continue
        state = torch.load(ckpt, map_location=device)
        model.load_state_dict(state["model_state_dict"])
        model.eval()
        for layer_idx, _, _ in base.iter_gate_modules(model):
            if layer_idx not in set(args.utility_layers):
                continue
            stats = capture_layer_stats(model, dataset, utility_indices, layer_idx, args, device)
            mean = stats["mean"]
            cov = stats["cov"]
            h_sample = stats["sample"]
            basis_c = common_basis(mean, cov, args.common_rank_init)
            residuals = project_off_subspace(h_sample, basis_c)
            bases, _sigmas = expert_energy_subspaces(model.model.layers[layer_idx].mlp, min(args.spectrum_k, args.hidden_size))
            raw_mean_scores = spectrum_scores(h_sample, bases).mean(dim=0).detach().cpu().tolist()
            res_mean_scores = spectrum_scores(residuals, bases).mean(dim=0).detach().cpu().tolist()
            utilities = []
            for expert_idx in range(args.num_experts):
                with force_layer_expert(model, layer_idx, expert_idx):
                    loss = mean_loss(model, dataset, utility_indices, args, device)
                utilities.append(-loss)
            rows.append(
                {
                    "variant": variant,
                    "model_seed": seed,
                    "step": step,
                    "layer": layer_idx,
                    "utility_num_sequences": len(utility_indices),
                    "spearman_raw_score_utility": spearman(raw_mean_scores, utilities),
                    "spearman_res_score_utility": spearman(res_mean_scores, utilities),
                    "top1_raw_matches_utility": int(np.argmax(raw_mean_scores) == np.argmax(utilities)),
                    "top1_res_matches_utility": int(np.argmax(res_mean_scores) == np.argmax(utilities)),
                    "raw_scores_json": json.dumps([round(float(x), 8) for x in raw_mean_scores]),
                    "res_scores_json": json.dumps([round(float(x), 8) for x in res_mean_scores]),
                    "utilities_json": json.dumps([round(float(x), 8) for x in utilities]),
                }
            )
    del model
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    return rows


def variant_summary(traj: list[dict[str, Any]], replay_frac: list[dict[str, Any]], utility: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    variants = sorted({str(r["variant"]) for r in traj})
    for variant in variants:
        rows0 = [r for r in traj if str(r["variant"]) == variant and int(r["step"]) == 0 and int(r["layer"]) in {3, 4, 5}]
        rows10 = [r for r in traj if str(r["variant"]) == variant and int(r["step"]) == 10 and int(r["layer"]) in {3, 4, 5}]
        rows300 = [r for r in traj if str(r["variant"]) == variant and int(r["step"]) == 300 and int(r["layer"]) in {3, 4, 5}]
        frac = [r for r in replay_frac if str(r["variant"]) == variant and int(r["layer"]) in {3, 4, 5}]
        util = [r for r in utility if str(r["variant"]) == variant and int(r["layer"]) in {3, 4, 5}]
        def mean_val(rows: list[dict[str, Any]], key: str) -> float | None:
            vals = [float(r[key]) for r in rows if r.get(key) not in {None, ""}]
            return float(np.mean(vals)) if vals else None
        out.append(
            {
                "variant": variant,
                "late_layers_step0_common_margin": mean_val(rows0, "common_margin"),
                "late_layers_step10_common_margin": mean_val(rows10, "common_margin"),
                "late_layers_step10_raw_max_load": mean_val(rows10, "raw_max_load"),
                "late_layers_step10_effective_experts": mean_val(rows10, "raw_effective_experts"),
                "late_layers_step300_lm_loss": mean_val(rows300, "lm_loss"),
                "late_layers_A_actual": mean_val(frac, "A_actual"),
                "late_layers_A_interaction": mean_val(frac, "A_interaction"),
                "late_layers_spearman_res_utility": mean_val(util, "spearman_res_score_utility"),
            }
        )
    return out


def make_figures(run_dir: Path) -> None:
    try:
        import matplotlib.pyplot as plt
        import pandas as pd
    except Exception:
        return
    fig_dir = run_dir / "figures"
    fig_dir.mkdir(parents=True, exist_ok=True)
    traj_path = run_dir / "results/trajectory_metrics.csv"
    frac_path = run_dir / "results/replay_fraction_summary.csv"
    if traj_path.exists() and traj_path.stat().st_size > 0:
        df = pd.read_csv(traj_path)
        late = df[(df["step"] == 10) & (df["layer"].isin([3, 4, 5]))].groupby("variant").agg(
            common_margin=("common_margin", "mean"),
            raw_max_load=("raw_max_load", "mean"),
        ).reset_index()
        for metric, fname in [
            ("common_margin", "step10_common_margin_by_variant.png"),
            ("raw_max_load", "step10_raw_max_load_by_variant.png"),
        ]:
            plt.figure(figsize=(9, 4))
            plt.bar(late["variant"], late[metric])
            plt.xticks(rotation=35, ha="right")
            plt.ylabel(metric)
            plt.tight_layout()
            plt.savefig(fig_dir / fname, dpi=160)
            plt.close()
    if frac_path.exists() and frac_path.stat().st_size > 0:
        df = pd.read_csv(frac_path)
        late = df[df["layer"].isin([3, 4, 5])].groupby("variant")["A_interaction"].mean().reset_index()
        plt.figure(figsize=(9, 4))
        plt.bar(late["variant"], late["A_interaction"])
        plt.xticks(rotation=35, ha="right")
        plt.ylabel("A_interaction")
        plt.tight_layout()
        plt.savefig(fig_dir / "replay_A_interaction_by_variant.png", dpi=160)
        plt.close()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-name", default=f"a06_01_common_filtered_expert_spectrum_router_initialization_4gpu_{now_slug()}")
    parser.add_argument("--output-dir", type=Path, default=EXP_DIR)
    parser.add_argument("--data-path", type=Path, default=Path("/data/share/109_cache_dir/hf_data/dclm_bin"))
    parser.add_argument("--hidden-size", type=int, default=512)
    parser.add_argument("--num-layers", type=int, default=6)
    parser.add_argument("--num-heads", type=int, default=8)
    parser.add_argument("--num-key-value-heads", type=int, default=4)
    parser.add_argument("--expert-hidden-dim", type=int, default=2048)
    parser.add_argument("--num-experts", type=int, default=8)
    parser.add_argument("--vocab-size", type=int, default=151936)
    parser.add_argument("--initializer-range", type=float, default=0.02)
    parser.add_argument("--init-num-sequences", type=int, default=8192)
    parser.add_argument("--audit-num-sequences", type=int, default=8192)
    parser.add_argument("--trajectory-audit-num-sequences", type=int, default=8192)
    parser.add_argument("--train-num-sequences", type=int, default=32768)
    parser.add_argument("--audit-batch-size", type=int, default=8)
    parser.add_argument("--train-batch-size", type=int, default=2)
    parser.add_argument("--max-init-tokens-per-layer", type=int, default=65536)
    parser.add_argument("--max-analyzed-tokens-per-layer", type=int, default=1024)
    parser.add_argument("--model-seeds", type=int, nargs="+", default=[0, 1, 2])
    parser.add_argument(
        "--variants",
        nargs="+",
        default=[
            "V0_random_init",
            "V1_common_orthogonal_random_init",
            "V2_representation_residual_init",
            "V3_raw_spectrum_linear_init",
            "V4_common_filtered_spectrum_linear_init",
            "V5_hybrid_spectrum_to_linear_init",
        ],
    )
    parser.add_argument("--audit-layers", type=int, nargs="*", default=None)
    parser.add_argument("--max-train-steps", type=int, default=300)
    parser.add_argument("--checkpoints", type=int, nargs="+", default=[0, 1, 2, 3, 5, 10, 20, 50, 100, 200, 300])
    parser.add_argument("--learning-rate", type=float, default=3e-4)
    parser.add_argument("--gradient-log-first-steps", type=int, default=5)
    parser.add_argument("--common-rank-init", type=int, default=8)
    parser.add_argument("--spectrum-k", type=int, default=6)
    parser.add_argument("--utility-num-sequences", type=int, default=64)
    parser.add_argument("--utility-steps", type=int, nargs="+", default=[0, 10])
    parser.add_argument("--utility-layers", type=int, nargs="+", default=[3, 4, 5])
    parser.add_argument("--utility-variants", nargs="+", default=["V0_random_init", "V3_raw_spectrum_linear_init", "V4_common_filtered_spectrum_linear_init", "V5_hybrid_spectrum_to_linear_init"])
    args = parser.parse_args()

    rank, world, local_rank = setup_dist()
    device = torch.device(f"cuda:{local_rank}" if torch.cuda.is_available() else "cpu")
    torch.backends.cuda.matmul.allow_tf32 = True
    torch.backends.cudnn.allow_tf32 = True

    run_dir = args.output_dir / "runs/common_filtered_expert_spectrum_init" / args.run_name
    partial_dir = run_dir / "partials"
    for d in ["config", "logs", "results", "figures", "notes", "partials", "checkpoints"]:
        (run_dir / d).mkdir(parents=True, exist_ok=True)

    if rank == 0:
        write_json(run_dir / "config/run_config.json", vars(args))
        write_json(
            run_dir / "config/source_manifest.json",
            {
                "timestamp": dt.datetime.now().isoformat(),
                "machine": socket.gethostname(),
                "moe_root": str(MOE_ROOT),
                "runner": str(Path(__file__).resolve()),
                "runner_sha256": sha256_file(Path(__file__).resolve()),
                "base_runner": str(BASE_RUNNER),
                "base_runner_sha256": sha256_file(BASE_RUNNER),
                "model_files": {
                    "myqwen.py": sha256_file(MOE_ROOT / "src/model/qwen3_moe/myqwen.py"),
                    "qwen3config.py": sha256_file(MOE_ROOT / "src/model/qwen3_moe/qwen3config.py"),
                    "train_qwen3_moe.py": sha256_file(MOE_ROOT / "train_qwen3_moe.py"),
                },
                "data_path": str(args.data_path),
            },
        )
    barrier()

    dataset = base.PackedBinDataset(args.data_path)
    init_indices = list(range(args.init_num_sequences))
    audit_indices = list(range(args.init_num_sequences, args.init_num_sequences + args.audit_num_sequences))
    utility_indices = audit_indices[: args.utility_num_sequences]
    train_indices_base = list(
        range(
            args.init_num_sequences + args.audit_num_sequences,
            args.init_num_sequences + args.audit_num_sequences + args.train_num_sequences,
        )
    )
    if rank == 0:
        append_jsonl(run_dir / "config/init_manifest_preview.jsonl", [dataset.manifest_row(i, "init") for i in init_indices[:64]])
        append_jsonl(run_dir / "config/audit_manifest_preview.jsonl", [dataset.manifest_row(i, "audit") for i in audit_indices[:64]])
        append_jsonl(run_dir / "config/train_manifest_preview.jsonl", [dataset.manifest_row(i, "train") for i in train_indices_base[:64]])
    barrier()

    tasks = [(parse_variant_name(v), seed) for v in args.variants for seed in args.model_seeds]
    for task_idx, (variant, seed) in enumerate(tasks):
        if task_idx % world != rank:
            continue
        print(f"[rank{rank}] train start variant={variant} seed={seed}", flush=True)
        train_indices = train_indices_base[:]
        random.Random(seed + 1701).shuffle(train_indices)
        traj, grads, ckpts, overlap, assign = train_variant(
            variant, seed, dataset, init_indices, audit_indices, train_indices, args, device, run_dir
        )
        append_jsonl(partial_dir / f"trajectory_rank{rank}.jsonl", traj)
        append_jsonl(partial_dir / f"gradients_rank{rank}.jsonl", grads)
        append_jsonl(partial_dir / f"checkpoints_rank{rank}.jsonl", ckpts)
        append_jsonl(partial_dir / f"spectrum_overlap_rank{rank}.jsonl", overlap)
        append_jsonl(partial_dir / f"oracle_assignment_rank{rank}.jsonl", assign)
        print(f"[rank{rank}] train done variant={variant} seed={seed} trajectory_rows={len(traj)}", flush=True)
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
    barrier()

    replay_tasks = tasks
    for task_idx, (variant, seed) in enumerate(replay_tasks):
        if task_idx % world != rank:
            continue
        print(f"[rank{rank}] replay start variant={variant} seed={seed}", flush=True)
        rows = base.replay_metrics_for_seed(variant, seed, dataset, audit_indices, args, device, run_dir)
        append_jsonl(partial_dir / f"replay_rank{rank}.jsonl", rows)
        print(f"[rank{rank}] replay done variant={variant} seed={seed} rows={len(rows)}", flush=True)
    barrier()

    for task_idx, (variant, seed) in enumerate(tasks):
        if task_idx % world != rank:
            continue
        print(f"[rank{rank}] utility start variant={variant} seed={seed}", flush=True)
        rows = utility_rows_for_seed(variant, seed, dataset, utility_indices, args, device, run_dir)
        append_jsonl(partial_dir / f"utility_rank{rank}.jsonl", rows)
        print(f"[rank{rank}] utility done variant={variant} seed={seed} rows={len(rows)}", flush=True)
    barrier()

    if rank == 0:
        traj: list[dict[str, Any]] = []
        grads: list[dict[str, Any]] = []
        ckpts: list[dict[str, Any]] = []
        replay: list[dict[str, Any]] = []
        overlap: list[dict[str, Any]] = []
        assign: list[dict[str, Any]] = []
        utility: list[dict[str, Any]] = []
        for p in sorted(partial_dir.glob("trajectory_rank*.jsonl")):
            traj.extend(read_jsonl(p))
        for p in sorted(partial_dir.glob("gradients_rank*.jsonl")):
            grads.extend(read_jsonl(p))
        for p in sorted(partial_dir.glob("checkpoints_rank*.jsonl")):
            ckpts.extend(read_jsonl(p))
        for p in sorted(partial_dir.glob("replay_rank*.jsonl")):
            replay.extend(read_jsonl(p))
        for p in sorted(partial_dir.glob("spectrum_overlap_rank*.jsonl")):
            overlap.extend(read_jsonl(p))
        for p in sorted(partial_dir.glob("oracle_assignment_rank*.jsonl")):
            assign.extend(read_jsonl(p))
        for p in sorted(partial_dir.glob("utility_rank*.jsonl")):
            utility.extend(read_jsonl(p))
        fractions = base.replay_fraction_summary(replay)
        summary = variant_summary(traj, fractions, utility)
        write_csv(run_dir / "results/trajectory_metrics.csv", traj)
        write_csv(run_dir / "results/gradient_metrics.csv", grads)
        write_csv(run_dir / "results/checkpoint_manifest.csv", ckpts)
        write_csv(run_dir / "results/replay_metrics.csv", replay)
        write_csv(run_dir / "results/replay_fraction_summary.csv", fractions)
        write_csv(run_dir / "results/spectrum_common_overlap.csv", overlap)
        write_csv(run_dir / "results/oracle_spectrum_assignment.csv", assign)
        write_csv(run_dir / "results/forced_utility_correlation.csv", utility)
        write_csv(run_dir / "results/variant_summary.csv", summary)
        write_json(
            run_dir / "run_summary.json",
            {
                "run_name": args.run_name,
                "trajectory_rows": len(traj),
                "gradient_rows": len(grads),
                "checkpoint_rows": len(ckpts),
                "replay_rows": len(replay),
                "fraction_rows": len(fractions),
                "spectrum_overlap_rows": len(overlap),
                "oracle_assignment_rows": len(assign),
                "forced_utility_rows": len(utility),
                "variant_summary_rows": len(summary),
                "completed_at": dt.datetime.now().isoformat(),
            },
        )
        make_figures(run_dir)
    barrier()
    if dist.is_available() and dist.is_initialized():
        dist.destroy_process_group()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
