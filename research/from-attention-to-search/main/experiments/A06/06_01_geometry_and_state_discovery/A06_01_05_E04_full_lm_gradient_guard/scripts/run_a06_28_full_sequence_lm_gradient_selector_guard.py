#!/usr/bin/env python3
"""Run A06_28 full-sequence LM gradient selector guard."""

from __future__ import annotations

import argparse
import csv
import importlib.util
import json
import math
import os
import time
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib")
os.environ.setdefault("PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION", "python")

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import torch
from torch.nn import functional as F


EXPERIMENT_ID = "A06_01_05_E04_full_lm_gradient_guard"
BASE_RUNNER = (
    Path(__file__).resolve().parents[2]
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


def parse_int_list(text: str) -> list[int]:
    return base.parse_int_list(text)


def normalize_rows(rows: torch.Tensor, scale: float) -> torch.Tensor:
    return rows / rows.norm(dim=1, keepdim=True).clamp_min(1e-8) * float(scale)


def project_out(rows: torch.Tensor, direction: torch.Tensor) -> torch.Tensor:
    c = direction.float()
    c = c / c.norm().clamp_min(1e-8)
    return rows.float() - (rows.float() @ c).unsqueeze(1) * c.unsqueeze(0)


def orthogonalize_rows(rows: torch.Tensor) -> torch.Tensor:
    q, _r = torch.linalg.qr(rows.float().T, mode="reduced")
    return q.T.contiguous()


def set_router_rows(model, rows: torch.Tensor, scale: float) -> None:
    with torch.no_grad():
        model.moe.router.weight.copy_(normalize_rows(rows, scale).to(model.moe.router.weight.device))


def route_slice(x: torch.Tensor, route_pos: torch.Tensor) -> torch.Tensor:
    return base.route_slice(x, route_pos)


def generate_uniform_batch(args: argparse.Namespace, n: int, slot_len: int, seed: int):
    batch = base.generate_batch(args, n, slot_len, seed, balanced=True)
    return batch


def clone_state(model) -> dict[str, torch.Tensor]:
    return {k: v.detach().cpu().clone() for k, v in model.state_dict().items()}


def load_state(model, state: dict[str, torch.Tensor], device: torch.device) -> None:
    model.load_state_dict({k: v.to(device) for k, v in state.items()})


def make_model(args: argparse.Namespace, seed: int, device: torch.device):
    return base.make_model(args, seed, device)


def compute_loss(
    args: argparse.Namespace,
    logits: torch.Tensor,
    batch,
    x: torch.Tensor,
    route_pos: torch.Tensor,
    target: torch.Tensor,
    loss_mode: str,
) -> torch.Tensor:
    if loss_mode == "route_ce":
        return F.cross_entropy(route_slice(logits, route_pos), target)
    if loss_mode == "full_lm":
        pred = logits[:, :-1, :].reshape(-1, logits.shape[-1])
        labels = x[:, 1:].reshape(-1)
        return F.cross_entropy(pred, labels)
    if loss_mode == "route_excluded_lm":
        pred = logits[:, :-1, :]
        labels = x[:, 1:]
        positions = torch.arange(x.shape[1] - 1, device=x.device).view(1, -1)
        keep = positions != route_pos.view(-1, 1)
        return F.cross_entropy(pred[keep], labels[keep])
    raise ValueError(f"unknown loss_mode={loss_mode}")


def train_warmup_states(
    args: argparse.Namespace,
    seed: int,
    slot_len: int,
    device: torch.device,
    loss_mode: str,
) -> dict[int, dict[str, torch.Tensor]]:
    warm_steps = sorted(set(parse_int_list(args.warmup_steps)))
    max_warm = max(warm_steps)
    model = make_model(args, seed + 25000, device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=float(args.lr), weight_decay=float(args.weight_decay))
    states: dict[int, dict[str, torch.Tensor]] = {}
    if 0 in warm_steps:
        states[0] = clone_state(model)
    for step in range(1, max_warm + 1):
        model.train()
        batch = generate_uniform_batch(args, int(args.train_batch_size), slot_len, seed + 500000 + step)
        x = batch.x.to(device)
        rp = batch.route_pos.to(device)
        target = batch.target.to(device)
        logits, _info = model(x, common_vec=None)
        loss = compute_loss(args, logits, batch, x, rp, target, loss_mode)
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), float(args.grad_clip))
        optimizer.step()
        if step in warm_steps:
            states[step] = clone_state(model)
    return states


@torch.no_grad()
def collect_route_scores(model, batch, args, device: torch.device):
    model.eval()
    score_parts = []
    route_parts = []
    loss_sum = 0.0
    correct = 0
    count = 0
    for start in range(0, batch.x.shape[0], int(args.eval_batch_size)):
        x = batch.x[start : start + int(args.eval_batch_size)].to(device)
        rp = batch.route_pos[start : start + x.shape[0]].to(device)
        target = batch.target[start : start + x.shape[0]].to(device)
        logits, info = model(x, common_vec=None)
        route_logits = route_slice(logits, rp)
        scores = route_slice(info["route_scores"], rp)
        assign = scores.argmax(dim=-1)
        loss_sum += float(F.cross_entropy(route_logits, target, reduction="sum").detach().cpu().item())
        correct += int((route_logits.argmax(dim=-1) == target).sum().detach().cpu().item())
        count += int(x.shape[0])
        score_parts.append(scores.detach().cpu())
        route_parts.append(assign.detach().cpu())
    return torch.cat(score_parts, dim=0), torch.cat(route_parts, dim=0), loss_sum / max(1, count), correct / max(1, count)


def margin_from_mapping(scores: torch.Tensor, feature: torch.Tensor, mapping: dict[int, int]) -> torch.Tensor:
    target = torch.tensor([mapping[int(f)] for f in feature.detach().cpu().tolist()], dtype=torch.long)
    scores_cpu = scores.detach().cpu().float()
    target_scores = scores_cpu[torch.arange(scores_cpu.shape[0]), target]
    masked = scores_cpu.clone()
    masked[torch.arange(scores_cpu.shape[0]), target] = -1e9
    return target_scores - masked.max(dim=1).values


def p05(values: torch.Tensor) -> float:
    if int(values.numel()) == 0:
        return float("nan")
    sorted_values = torch.sort(values.detach().cpu().float()).values
    idx = max(0, min(int(sorted_values.numel()) - 1, int(math.floor(0.05 * max(0, int(sorted_values.numel()) - 1)))))
    return float(sorted_values[idx].item())


def evaluate_model(
    model,
    batch,
    args: argparse.Namespace,
    device: torch.device,
    condition: str,
    seed: int,
    slot_len: int,
    warmup_step: int,
    method: str,
    loss_mode: str,
    checkpoint: int,
    mapping: dict[int, int] | None,
    step0_margin: torch.Tensor | None,
) -> tuple[dict, dict[int, int], torch.Tensor]:
    scores, assign, loss, acc = collect_route_scores(model, batch, args, device)
    feature = batch.feature.detach().cpu()
    slot_start = batch.slot_start.detach().cpu()
    if mapping is None:
        mapping = base.best_feature_mapping(feature, assign, int(args.num_features), int(args.num_experts))
    matched = torch.tensor([mapping[int(f)] for f in feature.tolist()], dtype=torch.long)
    margin = margin_from_mapping(scores, feature, mapping)
    if step0_margin is not None:
        eligible = step0_margin.detach().cpu() > 0
        sign_flip = float((margin[eligible] <= 0).float().mean().item()) if bool(eligible.any()) else float("nan")
    else:
        sign_flip = 0.0
    row = {
        "experiment_id": EXPERIMENT_ID,
        "condition": condition,
        "method": method,
        "loss_mode": loss_mode,
        "warmup_step": warmup_step,
        "seed": seed,
        "slot_len": slot_len,
        "checkpoint": checkpoint,
        "eval_count": int(feature.numel()),
        "loss": loss,
        "target_accuracy": acc,
        "feature_NMI": base.nmi(feature, assign),
        "matched_preserve_fraction": float((assign == matched).float().mean().item()),
        "margin_mean": float(margin.mean().item()),
        "margin_p05": p05(margin),
        "positive_margin_frac": float((margin > 0).float().mean().item()),
        "sign_flip_rate": sign_flip,
        "slot_start_NMI": base.nmi(slot_start, assign),
        **base.load_metrics(assign, int(args.num_experts)),
    }
    for f, e in mapping.items():
        row[f"map_feature_{f}_expert"] = e
    return row, mapping, margin


def expert_svd_rows(model, align_to_router: bool = True) -> torch.Tensor:
    rows = []
    router_rows = model.moe.router.weight.detach().cpu().float()
    for e, expert in enumerate(model.moe.experts):
        first = expert[0].weight.detach().cpu().float()
        _u, _s, vh = torch.linalg.svd(first, full_matrices=False)
        v = vh[0].clone()
        if align_to_router and float(torch.dot(v, router_rows[e])) < 0:
            v = -v
        rows.append(v)
    return torch.stack(rows, dim=0)


def oracle_centers(route_states: torch.Tensor, feature: torch.Tensor, num_features: int) -> torch.Tensor:
    return base.oracle_centers(route_states, feature, num_features)


def flatten_position_meta(batch, args: argparse.Namespace) -> dict[str, torch.Tensor]:
    n, seq_len = batch.x.shape
    pos = torch.arange(seq_len, dtype=torch.long).view(1, seq_len).expand(n, seq_len)
    route_pos = batch.route_pos.view(-1, 1).expand(n, seq_len)
    slot_start = batch.slot_start.view(-1, 1).expand(n, seq_len)
    slot_end = route_pos
    target_pos = route_pos + 1
    return {
        "feature": batch.feature.repeat_interleave(seq_len),
        "slot_start": batch.slot_start.repeat_interleave(seq_len),
        "position": pos.reshape(-1),
        "route_mask": (pos == route_pos).reshape(-1),
        "slot_mask": ((pos >= slot_start) & (pos <= slot_end)).reshape(-1),
        "target_mask": (pos == target_pos).reshape(-1),
        "seq_len": torch.tensor(seq_len, dtype=torch.long),
    }


def forward_with_grad_tensors(model, x: torch.Tensor):
    emb = model.embed(x)
    emb.retain_grad()
    t = x.shape[1]
    mask = torch.triu(torch.ones(t, t, dtype=torch.bool, device=x.device), diagonal=1)
    attn_out, _ = model.attn(emb, emb, emb, attn_mask=mask, need_weights=False)
    h = model.ln1(emb + attn_out)
    h.retain_grad()
    moe_out, scores, route = model.moe(h, h)
    y = model.ln2(h + moe_out)
    logits = model.lm_head(y)
    return logits, {"hidden": h, "embedding": emb, "route_scores": scores, "route": route}


def collect_gradient_signals(model, batch, args: argparse.Namespace, device: torch.device, loss_mode: str) -> dict[str, torch.Tensor]:
    model.eval()
    h_parts = []
    h_grad_parts = []
    emb_grad_parts = []
    loss_sum = 0.0
    count = 0
    for start in range(0, batch.x.shape[0], int(args.grad_batch_size)):
        x = batch.x[start : start + int(args.grad_batch_size)].to(device)
        rp = batch.route_pos[start : start + x.shape[0]].to(device)
        target = batch.target[start : start + x.shape[0]].to(device)
        model.zero_grad(set_to_none=True)
        logits, info = forward_with_grad_tensors(model, x)
        if loss_mode == "route_ce":
            loss = F.cross_entropy(route_slice(logits, rp), target, reduction="sum")
        elif loss_mode == "full_lm":
            pred = logits[:, :-1, :].reshape(-1, logits.shape[-1])
            labels = x[:, 1:].reshape(-1)
            loss = F.cross_entropy(pred, labels, reduction="sum")
        elif loss_mode == "route_excluded_lm":
            pred = logits[:, :-1, :]
            labels = x[:, 1:]
            positions = torch.arange(x.shape[1] - 1, device=x.device).view(1, -1)
            keep = positions != rp.view(-1, 1)
            loss = F.cross_entropy(pred[keep], labels[keep], reduction="sum")
        else:
            raise ValueError(f"unknown loss_mode={loss_mode}")
        loss.backward()
        h = info["hidden"]
        emb = info["embedding"]
        h_parts.append(h.detach().cpu())
        h_grad_parts.append(h.grad.detach().cpu())
        emb_grad_parts.append(emb.grad.detach().cpu())
        loss_sum += float(loss.detach().cpu().item())
        count += int(x.shape[0])
    model.zero_grad(set_to_none=True)
    h_all = torch.cat(h_parts, dim=0)
    h_grad = torch.cat(h_grad_parts, dim=0)
    emb_grad = torch.cat(emb_grad_parts, dim=0)
    return {
        "hidden": h_all.reshape(-1, h_all.shape[-1]),
        "h_grad": h_grad.reshape(-1, h_grad.shape[-1]),
        "emb_grad": emb_grad.reshape(-1, emb_grad.shape[-1]),
        "h_grad_score": h_grad.pow(2).sum(dim=-1).reshape(-1),
        "emb_grad_score": emb_grad.pow(2).sum(dim=-1).reshape(-1),
        "loss": torch.tensor(loss_sum / max(1, count), dtype=torch.float),
    }


def topk_indices_per_sample(flat_scores: torch.Tensor, n: int, seq_len: int, topk: int) -> torch.Tensor:
    scores = flat_scores.view(n, seq_len)
    k = max(1, min(int(topk), seq_len))
    idx = torch.topk(scores, k=k, dim=1).indices
    offsets = torch.arange(n, dtype=torch.long).view(-1, 1) * seq_len
    return (idx + offsets).reshape(-1)


def selector_diag(
    args: argparse.Namespace,
    method: str,
    score: torch.Tensor | None,
    selected_idx: torch.Tensor | None,
    meta: dict[str, torch.Tensor],
) -> dict:
    row = {
        "selector_method": method,
        "selection_count": int(selected_idx.numel()) if selected_idx is not None else 0,
        "selection_route_frac": float("nan"),
        "selection_slot_frac": float("nan"),
        "selection_target_frac": float("nan"),
        "top1_route_frac": float("nan"),
        "top1_slot_frac": float("nan"),
        "top1_target_frac": float("nan"),
        "score_route_share": float("nan"),
        "score_slot_share": float("nan"),
        "score_target_share": float("nan"),
    }
    if selected_idx is not None and int(selected_idx.numel()) > 0:
        row["selection_route_frac"] = float(meta["route_mask"][selected_idx].float().mean().item())
        row["selection_slot_frac"] = float(meta["slot_mask"][selected_idx].float().mean().item())
        row["selection_target_frac"] = float(meta["target_mask"][selected_idx].float().mean().item())
    if score is not None and int(score.numel()) > 0:
        n = int(meta["feature"].numel()) // int(meta["seq_len"].item())
        seq_len = int(meta["seq_len"].item())
        top1 = topk_indices_per_sample(score, n, seq_len, 1)
        row["top1_route_frac"] = float(meta["route_mask"][top1].float().mean().item())
        row["top1_slot_frac"] = float(meta["slot_mask"][top1].float().mean().item())
        row["top1_target_frac"] = float(meta["target_mask"][top1].float().mean().item())
        total = float(score.clamp_min(0).sum().item())
        if total > 0:
            row["score_route_share"] = float(score[meta["route_mask"]].clamp_min(0).sum().item() / total)
            row["score_slot_share"] = float(score[meta["slot_mask"]].clamp_min(0).sum().item() / total)
            row["score_target_share"] = float(score[meta["target_mask"]].clamp_min(0).sum().item() / total)
    return row


def weighted_kmeans(
    x: torch.Tensor,
    weights: torch.Tensor,
    k: int,
    seed: int,
    n_init: int,
    max_iter: int,
    device: torch.device,
) -> torch.Tensor:
    x_dev = x.float().to(device)
    w_dev = weights.float().clamp_min(0).to(device)
    if float(w_dev.sum().detach().cpu().item()) <= 1e-12:
        w_dev = torch.ones_like(w_dev)
    w_dev = w_dev / w_dev.mean().clamp_min(1e-12)
    n = x_dev.shape[0]
    best_centers = None
    best_obj = float("inf")
    prob = (w_dev / w_dev.sum().clamp_min(1e-12)).detach().cpu()
    for init in range(n_init):
        gen = torch.Generator(device="cpu").manual_seed(seed + 1009 * init)
        idx = torch.multinomial(prob, k, replacement=False, generator=gen).to(device)
        centers = x_dev[idx].clone()
        prev_assign = None
        for _ in range(max_iter):
            dist = torch.cdist(x_dev, centers)
            assign = dist.argmin(dim=1)
            if prev_assign is not None and torch.equal(assign, prev_assign):
                break
            prev_assign = assign
            new_centers = []
            for j in range(k):
                mask = assign == j
                if bool(mask.any()):
                    ww = w_dev[mask].view(-1, 1)
                    new_centers.append((x_dev[mask] * ww).sum(dim=0) / ww.sum().clamp_min(1e-12))
                else:
                    new_centers.append(x_dev[torch.randint(0, n, (1,), device=device)].squeeze(0))
            centers = torch.stack(new_centers, dim=0)
        min_dist = torch.cdist(x_dev, centers).min(dim=1).values
        obj = float((min_dist * w_dev).sum().detach().cpu().item() / w_dev.sum().detach().cpu().item())
        if obj < best_obj:
            best_obj = obj
            best_centers = centers.detach().cpu()
    return best_centers.float()


def hidden_rows_from_projected_kmeans(
    hidden_centered: torch.Tensor,
    basis: torch.Tensor,
    k: int,
    seed: int,
    n_init: int,
    max_iter: int,
    device: torch.device,
) -> torch.Tensor:
    x = hidden_centered.float()
    b = basis.float()
    projected = x @ b
    centers_proj = base.kmeans(projected, k, seed, n_init, max_iter, device)
    assign = torch.cdist(projected.to(device), centers_proj.to(device)).argmin(dim=1).detach().cpu()
    rows = []
    for j in range(k):
        mask = assign == j
        rows.append(x[mask].mean(dim=0) if bool(mask.any()) else x.mean(dim=0))
    return torch.stack(rows, dim=0)


def fisher_basis(grad: torch.Tensor, dim: int) -> torch.Tensor:
    g = grad.float()
    nz = g.norm(dim=1) > 1e-12
    if bool(nz.any()):
        g = g[nz]
    cov = (g.T @ g) / max(1, g.shape[0])
    eigvals, eigvecs = torch.linalg.eigh(cov)
    order = torch.argsort(eigvals, descending=True)
    return eigvecs[:, order[: max(1, min(int(dim), eigvecs.shape[1]))]].contiguous()


def rows_from_gradient_direction(
    hidden_centered: torch.Tensor,
    grad: torch.Tensor,
    selected_idx: torch.Tensor,
    args: argparse.Namespace,
    seed: int,
    device: torch.device,
) -> torch.Tensor:
    selected_grad = grad[selected_idx].float()
    selected_hidden = hidden_centered[selected_idx].float()
    selected_grad = selected_grad / selected_grad.norm(dim=1, keepdim=True).clamp_min(1e-8)
    grad_centers = base.kmeans(
        selected_grad,
        int(args.num_experts),
        seed,
        int(args.kmeans_n_init),
        int(args.kmeans_max_iter),
        device,
    )
    assign = torch.cdist(selected_grad.to(device), grad_centers.to(device)).argmin(dim=1).detach().cpu()
    rows = []
    for j in range(int(args.num_experts)):
        mask = assign == j
        rows.append(selected_hidden[mask].mean(dim=0) if bool(mask.any()) else selected_hidden.mean(dim=0))
    return torch.stack(rows, dim=0)


def build_rows_for_warmup(
    args: argparse.Namespace,
    warm_model,
    calib,
    seed: int,
    device: torch.device,
    loss_mode: str,
) -> tuple[dict[str, torch.Tensor | None], dict[str, dict]]:
    states = base.collect_states(warm_model, calib, device, int(args.eval_batch_size))
    all_h = states["all"]
    route_h = states["route"]
    common_all = all_h.mean(dim=0)
    common_route = route_h.mean(dim=0)
    meta = flatten_position_meta(calib, args)
    grad = collect_gradient_signals(warm_model, calib, args, device, loss_mode)
    h_grad_score = grad["h_grad_score"]
    emb_grad_score = grad["emb_grad_score"]
    n = int(calib.x.shape[0])
    seq_len = int(calib.x.shape[1])
    all_rows = base.kmeans(
        all_h - common_all,
        int(args.num_experts),
        seed + 7001,
        int(args.kmeans_n_init),
        int(args.kmeans_max_iter),
        device,
    )
    route_rows = base.kmeans(
        route_h - common_route,
        int(args.num_experts),
        seed + 7101,
        int(args.kmeans_n_init),
        int(args.kmeans_max_iter),
        device,
    )
    oracle_rows = oracle_centers(route_h, calib.feature, int(args.num_features)) - common_route
    rows: dict[str, torch.Tensor | None] = {
        "no_reinit": None,
        "allpos_centered": all_rows,
        "route_centered": route_rows,
        "oracle_centered": oracle_rows,
    }
    selection_diag = {}
    for idx, topk in enumerate(parse_int_list(args.selector_topks)):
        h_top_idx = topk_indices_per_sample(h_grad_score, n, seq_len, topk)
        emb_top_idx = topk_indices_per_sample(emb_grad_score, n, seq_len, topk)
        for prefix, score, grad_tensor, selected_idx, offset in [
            ("grad_h", h_grad_score, grad["h_grad"], h_top_idx, 10000 + idx * 100),
            ("grad_emb", emb_grad_score, grad["emb_grad"], emb_top_idx, 20000 + idx * 100),
        ]:
            selected = all_h[selected_idx]
            selected_centered = selected - selected.mean(dim=0)
            top_method = f"{prefix}_top{topk}_centered"
            direction_method = f"{prefix}_direction_top{topk}_centered"
            rows[top_method] = base.kmeans(
                selected_centered,
                int(args.num_experts),
                seed + offset + 1,
                int(args.kmeans_n_init),
                int(args.kmeans_max_iter),
                device,
            )
            rows[direction_method] = rows_from_gradient_direction(
                all_h - common_all,
                grad_tensor,
                selected_idx,
                args,
                seed + offset + 2,
                device,
            )
            selection_diag[top_method] = selector_diag(args, top_method, score, selected_idx, meta)
            selection_diag[direction_method] = selector_diag(args, direction_method, score, selected_idx, meta)
    reference = {
        "common_all": common_all,
        "common_route": common_route,
        "route_feature_centers": oracle_centers(route_h, calib.feature, int(args.num_features)),
        "current_router_rows": warm_model.moe.router.weight.detach().cpu().float(),
        "selection_diag": selection_diag,
        "grad_loss": float(grad["loss"].item()),
        "loss_mode": loss_mode,
    }
    return rows, reference


def cosine_matrix(a: torch.Tensor, b: torch.Tensor) -> torch.Tensor:
    aa = a.float() / a.float().norm(dim=1, keepdim=True).clamp_min(1e-8)
    bb = b.float() / b.float().norm(dim=1, keepdim=True).clamp_min(1e-8)
    return aa @ bb.T


def diagnostics_for_rows(
    args: argparse.Namespace,
    rows: torch.Tensor,
    reference: dict,
    condition: str,
    method: str,
    warmup_step: int,
    seed: int,
    slot_len: int,
) -> dict:
    rows = normalize_rows(rows.detach().cpu().float(), 1.0)
    n = rows.shape[0]
    pair = cosine_matrix(rows, rows).abs()
    off = pair[~torch.eye(n, dtype=torch.bool)]
    common = reference["common_route"].float().view(1, -1)
    common_cos = cosine_matrix(rows, common).abs().view(-1)
    feature_centers = reference["route_feature_centers"].float()
    feat_cos = cosine_matrix(rows, feature_centers).abs()
    current_cos = cosine_matrix(rows, reference["current_router_rows"].float()).abs()
    center_scores = feature_centers @ rows.T
    center_assign = center_scores.argmax(dim=1)
    center_feature = torch.arange(int(args.num_features), dtype=torch.long)
    center_mapping = base.best_feature_mapping(center_feature, center_assign, int(args.num_features), int(args.num_experts))
    center_margin = margin_from_mapping(center_scores, center_feature, center_mapping)
    return {
        "experiment_id": EXPERIMENT_ID,
        "condition": condition,
        "method": method,
        "warmup_step": warmup_step,
        "seed": seed,
        "slot_len": slot_len,
        "row_pair_abs_cos_mean": float(off.mean().item()) if int(off.numel()) else float("nan"),
        "row_pair_abs_cos_max": float(off.max().item()) if int(off.numel()) else float("nan"),
        "common_abs_cos_mean": float(common_cos.mean().item()),
        "common_abs_cos_max": float(common_cos.max().item()),
        "feature_center_abs_cos_best_mean": float(feat_cos.max(dim=0).values.mean().item()),
        "feature_center_abs_cos_best_min": float(feat_cos.max(dim=0).values.min().item()),
        "current_router_abs_cos_diag_mean": float(torch.diag(current_cos).mean().item()),
        "center_margin_mean": float(center_margin.mean().item()),
        "center_margin_p05": p05(center_margin),
    }


def init_condition_model(
    args: argparse.Namespace,
    base_state: dict[str, torch.Tensor],
    rows: torch.Tensor | None,
    seed: int,
    device: torch.device,
):
    model = make_model(args, seed, device)
    load_state(model, base_state, device)
    if rows is not None:
        set_router_rows(model, rows, float(args.router_init_scale))
    return model


def train_after_reinit(
    args: argparse.Namespace,
    condition: str,
    method: str,
    warmup_step: int,
    loss_mode: str,
    model,
    eval_batch,
    seed: int,
    slot_len: int,
    device: torch.device,
) -> list[dict]:
    optimizer = torch.optim.AdamW(model.parameters(), lr=float(args.lr), weight_decay=float(args.weight_decay))
    checkpoints = sorted(set([0] + parse_int_list(args.checkpoints)))
    checkpoint_set = set(checkpoints)
    rows = []
    mapping = None
    step0_margin = None
    row, mapping, step0_margin = evaluate_model(
        model, eval_batch, args, device, condition, seed, slot_len, warmup_step, method, loss_mode, 0, None, None
    )
    rows.append(row)
    for step in range(1, int(args.train_steps) + 1):
        model.train()
        batch = generate_uniform_batch(args, int(args.train_batch_size), slot_len, seed + 800000 + warmup_step * 1000 + step)
        x = batch.x.to(device)
        rp = batch.route_pos.to(device)
        target = batch.target.to(device)
        logits, _info = model(x, common_vec=None)
        loss = compute_loss(args, logits, batch, x, rp, target, loss_mode)
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), float(args.grad_clip))
        optimizer.step()
        if step in checkpoint_set:
            row, _mapping, _margin = evaluate_model(
                model,
                eval_batch,
                args,
                device,
                condition,
                seed,
                slot_len,
                warmup_step,
                method,
                loss_mode,
                step,
                mapping,
                step0_margin,
            )
            rows.append(row)
    return rows


def run_cell(args: argparse.Namespace, seed: int, slot_len: int, device: torch.device) -> tuple[list[dict], list[dict], list[dict]]:
    calib = generate_uniform_batch(args, int(args.calib_samples), slot_len, seed + 101)
    eval_batch = generate_uniform_batch(args, int(args.eval_samples), slot_len, seed + 202)
    data_rows = [
        {
            "experiment_id": EXPERIMENT_ID,
            "split": "calib",
            "seed": seed,
            "slot_len": slot_len,
            "sample_count": int(calib.feature.numel()),
            "feature0_fraction": float((calib.feature == 0).float().mean().item()),
            "feature1_fraction": float((calib.feature == 1).float().mean().item()),
            "feature2_fraction": float((calib.feature == 2).float().mean().item()),
            "feature3_fraction": float((calib.feature == 3).float().mean().item()),
            "slot_start_unique": int(torch.unique(calib.slot_start).numel()),
        },
        {
            "experiment_id": EXPERIMENT_ID,
            "split": "eval",
            "seed": seed,
            "slot_len": slot_len,
            "sample_count": int(eval_batch.feature.numel()),
            "feature0_fraction": float((eval_batch.feature == 0).float().mean().item()),
            "feature1_fraction": float((eval_batch.feature == 1).float().mean().item()),
            "feature2_fraction": float((eval_batch.feature == 2).float().mean().item()),
            "feature3_fraction": float((eval_batch.feature == 3).float().mean().item()),
            "slot_start_unique": int(torch.unique(eval_batch.slot_start).numel()),
        },
    ]
    train_rows: list[dict] = []
    diag_rows: list[dict] = []
    methods = [m for m in str(args.methods).replace(",", " ").split() if m.strip()]
    loss_modes = [m for m in str(args.loss_modes).replace(",", " ").split() if m.strip()]
    for loss_mode in loss_modes:
        warm_states = train_warmup_states(args, seed, slot_len, device, loss_mode)
        for warmup_step in sorted(warm_states):
            warm_model = make_model(args, seed + 25000, device)
            load_state(warm_model, warm_states[warmup_step], device)
            row_map, reference = build_rows_for_warmup(args, warm_model, calib, seed + warmup_step * 97, device, loss_mode)
            for method in methods:
                if method not in row_map:
                    raise ValueError(f"unknown method {method}; available={sorted(row_map)}")
                rows = row_map[method]
                condition = f"{loss_mode}_w{warmup_step}_{method}"
                if rows is not None:
                    diag = diagnostics_for_rows(args, rows, reference, condition, method, warmup_step, seed, slot_len)
                    diag.update(reference.get("selection_diag", {}).get(method, {}))
                    diag["grad_loss"] = reference.get("grad_loss", float("nan"))
                    diag["loss_mode"] = loss_mode
                    diag_rows.append(diag)
                else:
                    diag = diagnostics_for_rows(
                        args,
                        reference["current_router_rows"],
                        reference,
                        condition,
                        method,
                        warmup_step,
                        seed,
                        slot_len,
                    )
                    diag["grad_loss"] = reference.get("grad_loss", float("nan"))
                    diag["loss_mode"] = loss_mode
                    diag_rows.append(diag)
                model = init_condition_model(args, warm_states[warmup_step], rows, seed + 61000 + warmup_step, device)
                train_rows.extend(
                    train_after_reinit(args, condition, method, warmup_step, loss_mode, model, eval_batch, seed, slot_len, device)
                )
    return data_rows, diag_rows, train_rows


def aggregate_rows(rows: list[dict], keys: list[str], metrics: list[str]) -> list[dict]:
    groups: dict[tuple, list[dict]] = {}
    for row in rows:
        group_key = tuple(row.get(k, "") for k in keys)
        groups.setdefault(group_key, []).append(row)
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


def plot_metric_by_method_warm(rows: list[dict], metric: str, title: str, path: Path) -> None:
    methods = sorted({str(r["method"]) for r in rows})
    warmups = sorted({int(r["warmup_step"]) for r in rows})
    width = 0.8 / max(1, len(methods))
    xs = np.arange(len(warmups))
    plt.figure(figsize=(10.5, 5.2))
    for idx, method in enumerate(methods):
        vals = []
        for warm in warmups:
            found = [
                float(r[f"{metric}_mean"])
                for r in rows
                if str(r["method"]) == method and int(r["warmup_step"]) == warm and f"{metric}_mean" in r
            ]
            vals.append(float(np.mean(found)) if found else float("nan"))
        plt.bar(xs + (idx - (len(methods) - 1) / 2) * width, vals, width=width, label=method)
    plt.xticks(xs, [str(w) for w in warmups])
    plt.xlabel("warmup steps")
    plt.ylabel(metric)
    plt.title(title)
    plt.legend(fontsize=7, ncol=2)
    plt.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(path, dpi=180)
    plt.close()


def plot_trajectory(rows: list[dict], metric: str, title: str, path: Path, keep_methods: set[str]) -> None:
    conds = sorted({str(r["condition"]) for r in rows if str(r.get("method")) in keep_methods})
    plt.figure(figsize=(10.5, 5.4))
    for cond in conds:
        cond_rows = sorted([r for r in rows if str(r["condition"]) == cond], key=lambda r: int(r["checkpoint"]))
        xs = [int(r["checkpoint"]) for r in cond_rows]
        ys = [float(r[f"{metric}_mean"]) for r in cond_rows]
        plt.plot(xs, ys, marker="o", linewidth=1.4, label=cond)
    plt.xlabel("post-reinit checkpoint")
    plt.ylabel(metric)
    plt.title(title)
    plt.legend(fontsize=7, ncol=2)
    plt.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(path, dpi=180)
    plt.close()


def summarize_and_plot(output_dir: Path, args: argparse.Namespace, run_name: str) -> dict:
    partial_dir = output_dir / "partials" / run_name
    data_rows: list[dict] = []
    diag_rows: list[dict] = []
    train_rows: list[dict] = []
    for path in sorted(partial_dir.glob("data_audit_rank*.csv")):
        data_rows.extend(read_csv(path))
    for path in sorted(partial_dir.glob("selector_diagnostics_rank*.csv")):
        diag_rows.extend(read_csv(path))
    for path in sorted(partial_dir.glob("training_trajectory_rank*.csv")):
        train_rows.extend(read_csv(path))
    table_dir = output_dir / "tables"
    fig_dir = output_dir / "figures"
    write_csv(table_dir / "data_audit.csv", data_rows)
    write_csv(table_dir / "selector_diagnostics.csv", diag_rows)
    write_csv(table_dir / "training_trajectory.csv", train_rows)
    metrics = [
        "feature_NMI",
        "matched_preserve_fraction",
        "margin_mean",
        "margin_p05",
        "positive_margin_frac",
        "sign_flip_rate",
        "slot_start_NMI",
        "max_load",
        "effective_experts",
        "target_accuracy",
        "loss",
    ]
    diag_metrics = [
        "row_pair_abs_cos_mean",
        "row_pair_abs_cos_max",
        "common_abs_cos_mean",
        "common_abs_cos_max",
        "feature_center_abs_cos_best_mean",
        "feature_center_abs_cos_best_min",
        "current_router_abs_cos_diag_mean",
        "center_margin_mean",
        "center_margin_p05",
        "selection_count",
        "selection_route_frac",
        "selection_slot_frac",
        "selection_target_frac",
        "top1_route_frac",
        "top1_slot_frac",
        "top1_target_frac",
        "score_route_share",
        "score_slot_share",
        "score_target_share",
        "grad_loss",
    ]
    condition_trajectory = aggregate_rows(train_rows, ["loss_mode", "condition", "method", "warmup_step", "checkpoint"], metrics)
    final_step = max(int(r["checkpoint"]) for r in train_rows) if train_rows else 0
    reinit_rows = [r for r in train_rows if int(r["checkpoint"]) == 0]
    final_rows = [r for r in train_rows if int(r["checkpoint"]) == final_step]
    condition_reinit = aggregate_rows(reinit_rows, ["loss_mode", "condition", "method", "warmup_step"], metrics)
    condition_final = aggregate_rows(final_rows, ["loss_mode", "condition", "method", "warmup_step"], metrics)
    diag_agg = aggregate_rows(diag_rows, ["loss_mode", "condition", "method", "warmup_step"], diag_metrics)
    write_csv(table_dir / "condition_trajectory_aggregate.csv", condition_trajectory)
    write_csv(table_dir / "condition_aggregate_reinit.csv", condition_reinit)
    write_csv(table_dir / "condition_aggregate_final.csv", condition_final)
    write_csv(table_dir / "selector_diagnostics_aggregate.csv", diag_agg)
    if condition_reinit:
        for loss_mode in sorted({str(r["loss_mode"]) for r in condition_reinit}):
            subset = [r for r in condition_reinit if str(r["loss_mode"]) == loss_mode]
            plot_metric_by_method_warm(subset, "feature_NMI", f"{loss_mode}: immediate feature NMI after router reinit", fig_dir / f"{loss_mode}_reinit_feature_nmi_by_method_warmup.png")
            plot_metric_by_method_warm(subset, "margin_p05", f"{loss_mode}: immediate margin p05 after router reinit", fig_dir / f"{loss_mode}_reinit_margin_p05_by_method_warmup.png")
    if condition_final:
        for loss_mode in sorted({str(r["loss_mode"]) for r in condition_final}):
            subset = [r for r in condition_final if str(r["loss_mode"]) == loss_mode]
            plot_metric_by_method_warm(subset, "feature_NMI", f"{loss_mode}: final feature NMI after post-reinit training", fig_dir / f"{loss_mode}_final_feature_nmi_by_method_warmup.png")
            plot_metric_by_method_warm(subset, "margin_p05", f"{loss_mode}: final margin p05 after post-reinit training", fig_dir / f"{loss_mode}_final_margin_p05_by_method_warmup.png")
    if condition_trajectory:
        keep = {
            "allpos_centered",
            "route_centered",
            "grad_h_topk_centered",
            "grad_h_direction_centered",
            "fisher_h_topdim_centered",
            "grad_emb_topk_centered",
            "grad_emb_direction_centered",
        }
        plot_trajectory(condition_trajectory, "feature_NMI", "Feature NMI trajectory for central methods", fig_dir / "feature_nmi_trajectory_central_methods.png", keep)
    if diag_agg:
        plot_metric_by_method_warm(diag_agg, "common_abs_cos_mean", "Source row common alignment", fig_dir / "diagnostic_common_alignment_by_method_warmup.png")
        plot_metric_by_method_warm(diag_agg, "row_pair_abs_cos_mean", "Source row pairwise cosine", fig_dir / "diagnostic_row_similarity_by_method_warmup.png")
        plot_metric_by_method_warm(diag_agg, "feature_center_abs_cos_best_mean", "Source row best feature-center cosine", fig_dir / "diagnostic_feature_center_alignment_by_method_warmup.png")
        plot_metric_by_method_warm(diag_agg, "top1_route_frac", "Selector top-1 route-position fraction", fig_dir / "diagnostic_top1_route_frac_by_method_warmup.png")

    def find(rows: list[dict], loss_mode: str, method: str, warmup_step: int, metric: str) -> float:
        for row in rows:
            if (
                str(row.get("loss_mode")) == loss_mode
                and str(row.get("method")) == method
                and int(row.get("warmup_step", -1)) == warmup_step
            ):
                return float(row.get(f"{metric}_mean", "nan"))
        return float("nan")

    key = {
        "completed_cells": len({(r["seed"], r["slot_len"]) for r in train_rows}),
        "completed_training_rows": len(train_rows),
        "final_step": final_step,
        "route_w40_grad_emb_top1_reinit_feature_nmi": find(condition_reinit, "route_ce", "grad_emb_top1_centered", 40, "feature_NMI"),
        "route_w40_grad_emb_top1_reinit_margin_p05": find(condition_reinit, "route_ce", "grad_emb_top1_centered", 40, "margin_p05"),
        "full_lm_w40_allpos_reinit_feature_nmi": find(condition_reinit, "full_lm", "allpos_centered", 40, "feature_NMI"),
        "full_lm_w40_grad_emb_top1_reinit_feature_nmi": find(condition_reinit, "full_lm", "grad_emb_top1_centered", 40, "feature_NMI"),
        "full_lm_w40_grad_emb_top4_reinit_feature_nmi": find(condition_reinit, "full_lm", "grad_emb_top4_centered", 40, "feature_NMI"),
        "full_lm_w40_grad_emb_top8_reinit_feature_nmi": find(condition_reinit, "full_lm", "grad_emb_top8_centered", 40, "feature_NMI"),
        "full_lm_w40_grad_emb_top1_reinit_margin_p05": find(condition_reinit, "full_lm", "grad_emb_top1_centered", 40, "margin_p05"),
        "full_lm_w40_grad_emb_top4_reinit_margin_p05": find(condition_reinit, "full_lm", "grad_emb_top4_centered", 40, "margin_p05"),
        "full_lm_w40_grad_emb_top8_reinit_margin_p05": find(condition_reinit, "full_lm", "grad_emb_top8_centered", 40, "margin_p05"),
        "full_lm_w40_grad_emb_top4_final_feature_nmi": find(condition_final, "full_lm", "grad_emb_top4_centered", 40, "feature_NMI"),
        "max_slot_start_nmi_reinit": max([float(r.get("slot_start_NMI_mean", "nan")) for r in condition_reinit] or [float("nan")]),
    }
    route_ref = find(condition_reinit, "full_lm", "route_centered", 40, "feature_NMI")
    allpos_best = key["full_lm_w40_allpos_reinit_feature_nmi"]
    grad_best = max(
        key["full_lm_w40_grad_emb_top1_reinit_feature_nmi"],
        key["full_lm_w40_grad_emb_top4_reinit_feature_nmi"],
        key["full_lm_w40_grad_emb_top8_reinit_feature_nmi"],
    )
    grad_margin_best = max(
        key["full_lm_w40_grad_emb_top1_reinit_margin_p05"],
        key["full_lm_w40_grad_emb_top4_reinit_margin_p05"],
        key["full_lm_w40_grad_emb_top8_reinit_margin_p05"],
    )
    if not math.isnan(route_ref) and grad_best >= route_ref - 0.05 and grad_margin_best > 0:
        verdict = "gradient_selector_candidate_supported"
    elif not math.isnan(route_ref) and grad_best > allpos_best + 0.05:
        verdict = "gradient_signal_improves_but_margin_guard_failed"
    elif not math.isnan(route_ref):
        verdict = "gradient_selector_not_supported"
    else:
        verdict = "insufficient"
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
            "selector_diagnostics": str(table_dir / "selector_diagnostics.csv"),
            "condition_aggregate_reinit": str(table_dir / "condition_aggregate_reinit.csv"),
            "condition_aggregate_final": str(table_dir / "condition_aggregate_final.csv"),
            "selector_diagnostics_aggregate": str(table_dir / "selector_diagnostics_aggregate.csv"),
        },
        "figures": {
            "reinit_feature_nmi": str(fig_dir / "reinit_feature_nmi_by_method_warmup.png"),
            "reinit_margin_p05": str(fig_dir / "reinit_margin_p05_by_method_warmup.png"),
            "final_feature_nmi": str(fig_dir / "final_feature_nmi_by_method_warmup.png"),
            "final_margin_p05": str(fig_dir / "final_margin_p05_by_method_warmup.png"),
            "feature_nmi_trajectory": str(fig_dir / "feature_nmi_trajectory_central_methods.png"),
            "diagnostic_common_alignment": str(fig_dir / "diagnostic_common_alignment_by_method_warmup.png"),
            "diagnostic_row_similarity": str(fig_dir / "diagnostic_row_similarity_by_method_warmup.png"),
            "diagnostic_feature_alignment": str(fig_dir / "diagnostic_feature_center_alignment_by_method_warmup.png"),
            "diagnostic_top1_route_frac": str(fig_dir / "diagnostic_top1_route_frac_by_method_warmup.png"),
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
    parser.add_argument("--slot-lengths", default="1 2 4 8")
    parser.add_argument("--warmup-steps", default="0 10 40")
    parser.add_argument("--loss-modes", default="route_ce full_lm")
    parser.add_argument(
        "--methods",
        default=(
            "no_reinit allpos_centered route_centered oracle_centered "
            "grad_h_top1_centered grad_h_direction_top1_centered grad_h_top4_centered grad_h_direction_top4_centered "
            "grad_emb_top1_centered grad_emb_direction_top1_centered grad_emb_top4_centered grad_emb_direction_top4_centered "
            "grad_emb_top8_centered grad_emb_direction_top8_centered"
        ),
    )
    parser.add_argument("--seq-len", type=int, default=32)
    parser.add_argument("--slot-starts", default="2 10 18")
    parser.add_argument("--num-features", type=int, default=4)
    parser.add_argument("--num-experts", type=int, default=4)
    parser.add_argument("--num-neutral-tokens", type=int, default=32)
    parser.add_argument("--common-prob", type=float, default=0.25)
    parser.add_argument("--d-model", type=int, default=64)
    parser.add_argument("--num-heads", type=int, default=4)
    parser.add_argument("--d-ff", type=int, default=128)
    parser.add_argument("--calib-samples", type=int, default=2048)
    parser.add_argument("--eval-samples", type=int, default=2048)
    parser.add_argument("--train-batch-size", type=int, default=256)
    parser.add_argument("--eval-batch-size", type=int, default=512)
    parser.add_argument("--train-steps", type=int, default=160)
    parser.add_argument("--checkpoints", default="0 10 40 80 160")
    parser.add_argument("--lr", type=float, default=2e-3)
    parser.add_argument("--weight-decay", type=float, default=1e-4)
    parser.add_argument("--grad-clip", type=float, default=1.0)
    parser.add_argument("--router-init-scale", type=float, default=1.5)
    parser.add_argument("--kmeans-n-init", type=int, default=4)
    parser.add_argument("--kmeans-max-iter", type=int, default=40)
    parser.add_argument("--grad-batch-size", type=int, default=256)
    parser.add_argument("--selector-topk", type=int, default=1)
    parser.add_argument("--selector-topks", default="1 4 8")
    parser.add_argument("--fisher-dim", type=int, default=8)
    args = parser.parse_args()

    if args.run_stage == "smoke":
        args.seeds = "0"
        args.slot_lengths = "1"
        args.warmup_steps = "0 10"
        args.loss_modes = "route_ce full_lm"
        args.train_steps = 20
        args.checkpoints = "0 5 20"
        args.calib_samples = 512
        args.eval_samples = 512
        args.methods = (
            "no_reinit allpos_centered route_centered oracle_centered "
            "grad_h_top1_centered grad_h_direction_top1_centered "
            "grad_emb_top1_centered grad_emb_direction_top1_centered grad_emb_top4_centered grad_emb_direction_top4_centered"
        )
        args.selector_topks = "1 4"

    output_dir = Path(args.output_dir)
    rank, local_rank, world_size = base.local_rank_world()
    dist_enabled = base.init_dist_if_needed(world_size)
    if torch.cuda.is_available():
        device = torch.device(f"cuda:{local_rank % torch.cuda.device_count()}")
        torch.cuda.set_device(device)
    else:
        device = torch.device("cpu")
    seeds = parse_int_list(args.seeds)
    slot_lengths = parse_int_list(args.slot_lengths)
    tasks = [(seed, slot_len) for seed in seeds for slot_len in slot_lengths]
    my_tasks = [task for i, task in enumerate(tasks) if i % world_size == rank]
    partial_dir = output_dir / "partials" / args.run_name
    partial_dir.mkdir(parents=True, exist_ok=True)
    print(
        json.dumps(
            {
                "event": "start",
                "rank": rank,
                "world_size": world_size,
                "device": str(device),
                "run_stage": args.run_stage,
                "run_name": args.run_name,
                "tasks": my_tasks,
            }
        ),
        flush=True,
    )
    all_data: list[dict] = []
    all_diag: list[dict] = []
    all_train: list[dict] = []
    for seed, slot_len in my_tasks:
        data_rows, diag_rows, train_rows = run_cell(args, seed, slot_len, device)
        all_data.extend(data_rows)
        all_diag.extend(diag_rows)
        all_train.extend(train_rows)
        print(json.dumps({"event": "cell_done", "rank": rank, "seed": seed, "slot_len": slot_len}), flush=True)
    write_csv(partial_dir / f"data_audit_rank{rank}.csv", all_data)
    write_csv(partial_dir / f"selector_diagnostics_rank{rank}.csv", all_diag)
    write_csv(partial_dir / f"training_trajectory_rank{rank}.csv", all_train)
    base.dist_barrier(dist_enabled)
    if rank == 0:
        summary = summarize_and_plot(output_dir, args, args.run_name)
        print(json.dumps({"event": "summary", "summary": summary}, indent=2), flush=True)
    base.dist_barrier(dist_enabled)


if __name__ == "__main__":
    main()
