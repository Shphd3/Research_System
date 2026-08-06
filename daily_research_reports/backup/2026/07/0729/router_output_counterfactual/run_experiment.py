#!/usr/bin/env python3
"""Frozen within-model route-output counterfactual audit.

The treatment changes only the selected sparse-expert identity at one layer.
The native per-token top-1 softmax weight, exact expert loads, shared expert,
input state, model parameters, and every other layer are held fixed.
"""

from __future__ import annotations

import argparse
import gc
import json
import math
import os
import platform
import sys
import types
from pathlib import Path
from typing import Dict, List, Sequence, Tuple

import numpy as np
import pandas as pd
import torch
import torch.nn.functional as F


EXPERIMENT_DIR = Path(__file__).resolve().parent
RESULTS_DIR = EXPERIMENT_DIR / "results"
PRIOR_PROBE_DIR = EXPERIMENT_DIR.parent.parent / "0728/router_layer_band_probe"
if str(PRIOR_PROBE_DIR) not in sys.path:
    sys.path.insert(0, str(PRIOR_PROBE_DIR))

from run_probe import MODEL_SPECS, build_token_split, load_model  # noqa: E402


THRESHOLDS = {
    "center_flip_min": 0.20,
    "shuffle_flip_min": 0.50,
    "shuffle_sparse_cka_max": 0.99,
    "noop_kl_max": 1e-6,
    "noop_abs_nll_delta_max": 1e-6,
    "support_median_r_max": 0.25,
    "support_median_flip_adjusted_r_max": 0.50,
    "support_median_flip_only_cka_min": 0.90,
    "support_median_spectrum_ratio_max": 0.25,
    "support_median_angle_ratio_max": 0.25,
    "support_median_kl_ratio_max": 0.25,
    "support_abs_nll_delta_max": 0.01,
    "reject_median_r_min": 0.75,
    "reject_median_flip_only_cka_max": 0.50,
    "reject_median_kl_ratio_min": 0.75,
    "reject_abs_nll_delta_min": 0.02,
    "min_eligible_layers": 8,
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", choices=["lb", "decommon"], required=True)
    parser.add_argument("--device", default="cuda:0")
    parser.add_argument("--checkpoint-step", type=int, default=40000)
    parser.add_argument("--calibration-docs", type=int, default=32)
    parser.add_argument("--evaluation-docs", type=int, default=64)
    parser.add_argument("--max-length", type=int, default=256)
    parser.add_argument("--candidate-pool", type=int, default=512)
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--expert-batch-tokens", type=int, default=2048)
    parser.add_argument("--logit-batch-docs", type=int, default=1)
    parser.add_argument("--layers", type=int, nargs="*", default=None, help="One-based layers")
    parser.add_argument("--smoke", action="store_true")
    return parser.parse_args()


def capture_states(
    model: torch.nn.Module,
    token_ids: torch.Tensor,
    batch_size: int,
    device: str,
    capture_blocks: bool,
) -> Tuple[List[torch.Tensor], List[torch.Tensor], List[torch.Tensor], torch.Tensor]:
    num_layers = len(model.model.layers)
    expert_inputs: List[List[torch.Tensor]] = [[] for _ in range(num_layers)]
    routing_inputs: List[List[torch.Tensor]] = [[] for _ in range(num_layers)]
    block_outputs: List[List[torch.Tensor]] = [[] for _ in range(num_layers)]
    final_outputs: List[torch.Tensor] = []
    hooks = []

    def make_pre_hook(layer_index: int):
        def hook(_module, args):
            expert_value = args[0].detach().reshape(-1, args[0].shape[-1])
            # These checkpoints use gating_reference='oracle': the Router sees
            # the attention-branch output passed as args[1], while the sparse
            # experts consume args[0].  Preserve both objects explicitly.
            route_arg = args[1] if len(args) > 1 and torch.is_tensor(args[1]) else args[0]
            route_value = route_arg.detach().reshape(-1, route_arg.shape[-1])
            expert_inputs[layer_index].append(expert_value.to(device="cpu", dtype=torch.bfloat16))
            routing_inputs[layer_index].append(route_value.to(device="cpu", dtype=torch.bfloat16))

        return hook

    def make_block_hook(layer_index: int):
        def hook(_module, _args, output):
            value = output[0] if isinstance(output, tuple) else output
            block_outputs[layer_index].append(
                value.detach().reshape(-1, value.shape[-1]).to(device="cpu", dtype=torch.bfloat16)
            )

        return hook

    for layer_index, layer in enumerate(model.model.layers):
        hooks.append(layer.mlp.register_forward_pre_hook(make_pre_hook(layer_index)))
        if capture_blocks:
            hooks.append(layer.register_forward_hook(make_block_hook(layer_index)))

    try:
        with torch.inference_mode():
            for start in range(0, token_ids.shape[0], batch_size):
                batch = token_ids[start : start + batch_size].to(device, non_blocking=True)
                output = model.model(
                    input_ids=batch,
                    use_cache=False,
                    output_attentions=False,
                    output_hidden_states=False,
                    output_expert_labels=False,
                )
                final_outputs.append(
                    output.last_hidden_state.detach().reshape(-1, output.last_hidden_state.shape[-1]).to(
                        device="cpu", dtype=torch.bfloat16
                    )
                )
    finally:
        for handle in hooks:
            handle.remove()

    expert_values = [torch.cat(chunks, dim=0) for chunks in expert_inputs]
    routing_values = [torch.cat(chunks, dim=0) for chunks in routing_inputs]
    if capture_blocks:
        blocks = [torch.cat(chunks, dim=0) for chunks in block_outputs]
    else:
        blocks = [torch.empty(0, dtype=torch.bfloat16) for _ in range(num_layers)]
    return expert_values, routing_values, blocks, torch.cat(final_outputs, dim=0)


def compute_routes(
    model_key: str,
    mlp: torch.nn.Module,
    calibration_input: torch.Tensor,
    evaluation_input: torch.Tensor,
    device: str,
    seed: int,
    route_chunk_tokens: int,
) -> Dict[str, torch.Tensor | float | bool]:
    calibration_center = calibration_input.float().mean(dim=0).to(device)
    checkpoint_center = getattr(mlp, "router_running_mean", torch.zeros_like(calibration_center)).detach().float().to(device)
    native_center = checkpoint_center if MODEL_SPECS[model_key]["native_center"] == "checkpoint_running" else torch.zeros_like(calibration_center)

    all_native_labels: List[torch.Tensor] = []
    all_native_weights: List[torch.Tensor] = []
    all_center_scores: List[torch.Tensor] = []
    with torch.inference_mode():
        for start in range(0, evaluation_input.shape[0], route_chunk_tokens):
            x = evaluation_input[start : start + route_chunk_tokens].to(device=device, dtype=torch.bfloat16)
            native_center_local = native_center.to(dtype=x.dtype)
            calibration_center_local = calibration_center.to(dtype=x.dtype)
            native_logits = mlp.gate(x - native_center_local)
            native_probs = F.softmax(native_logits, dim=-1, dtype=torch.float32)
            native_weights, native_labels = native_probs.max(dim=-1)
            centered_scores = mlp.gate(x - calibration_center_local)
            all_native_labels.append(native_labels.cpu())
            all_native_weights.append(native_weights.to(dtype=torch.bfloat16).cpu())
            all_center_scores.append(centered_scores.cpu())

    native_labels = torch.cat(all_native_labels).long()
    native_weights = torch.cat(all_native_weights).to(dtype=torch.bfloat16)
    center_scores = torch.cat(all_center_scores).float().numpy()
    quotas = np.bincount(native_labels.numpy(), minlength=mlp.num_experts)
    raw_center_labels = center_scores.argmax(axis=1).astype(np.int64)
    center_labels = exact_quota_assignment(center_scores, quotas)

    generator = torch.Generator(device="cpu").manual_seed(seed)
    shuffle_labels = native_labels[torch.randperm(native_labels.numel(), generator=generator)]

    native_counts = np.bincount(native_labels.numpy(), minlength=mlp.num_experts)
    center_counts = np.bincount(center_labels, minlength=mlp.num_experts)
    shuffle_counts = np.bincount(shuffle_labels.numpy(), minlength=mlp.num_experts)
    load_exact = bool(np.array_equal(native_counts, center_counts) and np.array_equal(native_counts, shuffle_counts))

    return {
        "native_labels": native_labels,
        "native_weights": native_weights,
        "center_labels": torch.from_numpy(center_labels).long(),
        "shuffle_labels": shuffle_labels.long(),
        "raw_center_flip": float(np.mean(raw_center_labels != native_labels.numpy())),
        "center_flip": float(np.mean(center_labels != native_labels.numpy())),
        "shuffle_flip": float(np.mean(shuffle_labels.numpy() != native_labels.numpy())),
        "quota_repair_fraction": float(np.mean(center_labels != raw_center_labels)),
        "load_exact": load_exact,
        "native_counts": torch.from_numpy(native_counts),
        "calibration_center_norm": float(calibration_center.norm().item()),
        "checkpoint_center_norm": float(checkpoint_center.norm().item()),
    }


def exact_quota_assignment(scores: np.ndarray, quotas: np.ndarray) -> np.ndarray:
    """Deterministic greedy minimum-penalty repair of centered argmax labels."""
    labels = scores.argmax(axis=1).astype(np.int64)
    counts = np.bincount(labels, minlength=scores.shape[1]).astype(np.int64)
    quotas = np.asarray(quotas, dtype=np.int64)
    if counts.sum() != quotas.sum():
        raise ValueError("Quota total does not match token count")

    rounds = 0
    while not np.array_equal(counts, quotas):
        rounds += 1
        if rounds > scores.shape[1] * 2:
            raise RuntimeError(f"Quota repair did not converge: counts={counts}, quotas={quotas}")
        over = counts > quotas
        under_ids = np.flatnonzero(counts < quotas)
        token_ids = np.flatnonzero(over[labels])
        if token_ids.size == 0 or under_ids.size == 0:
            raise RuntimeError("Quota repair reached an inconsistent state")

        assigned_scores = scores[token_ids, labels[token_ids]][:, None]
        penalties = assigned_scores - scores[np.ix_(token_ids, under_ids)]
        order = np.argsort(penalties, axis=None, kind="mergesort")
        moved = 0
        n_targets = under_ids.size
        for flat_index in order:
            token_pos = int(flat_index // n_targets)
            target_pos = int(flat_index % n_targets)
            token = int(token_ids[token_pos])
            source = int(labels[token])
            target = int(under_ids[target_pos])
            if counts[source] <= quotas[source] or counts[target] >= quotas[target]:
                continue
            labels[token] = target
            counts[source] -= 1
            counts[target] += 1
            moved += 1
            if np.array_equal(counts, quotas):
                break
        if moved == 0:
            raise RuntimeError("Quota repair made no progress")

    return labels


def audit_all_experts(
    mlp: torch.nn.Module,
    hidden: torch.Tensor,
    device: str,
    chunk_size: int,
) -> Tuple[bool, List[float]]:
    n_tokens = hidden.shape[0]
    finite = True
    norm_sums = [0.0 for _ in range(mlp.num_experts)]
    with torch.inference_mode():
        for start in range(0, n_tokens, chunk_size):
            end = min(start + chunk_size, n_tokens)
            x = hidden[start:end].to(device=device, dtype=torch.bfloat16)
            for expert_id, expert in enumerate(mlp.experts):
                output = expert(x)
                finite = finite and bool(torch.isfinite(output).all().item())
                norm_sums[expert_id] += float(torch.linalg.vector_norm(output.float(), dim=-1).sum().item())
    return finite, [value / n_tokens for value in norm_sums]


def run_forced_layer(
    model: torch.nn.Module,
    token_ids: torch.Tensor,
    layer_index: int,
    forced_labels: torch.Tensor,
    native_weights: torch.Tensor,
    batch_size: int,
    device: str,
) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
    mlp = model.model.layers[layer_index].mlp
    state = {"offset": 0}
    sparse_outputs: List[torch.Tensor] = []
    shared_outputs: List[torch.Tensor] = []
    target_blocks: List[torch.Tensor] = []
    final_outputs: List[torch.Tensor] = []

    def forced_forward(self, hidden_states, gating_reference=None, global_step=None):
        del gating_reference, global_step
        batch_size_local, sequence_length, hidden_size = hidden_states.shape
        n_tokens = batch_size_local * sequence_length
        start = int(state["offset"])
        end = start + n_tokens
        flat_hidden = hidden_states.reshape(-1, hidden_size)
        selected_flat = forced_labels[start:end].to(device=hidden_states.device)
        selected = selected_flat.view(-1, 1)
        weights = native_weights[start:end].to(device=hidden_states.device, dtype=hidden_states.dtype)
        sparse = torch.zeros_like(flat_hidden)
        for expert_id, expert in enumerate(self.experts):
            token_positions = torch.where(selected_flat == expert_id)[0]
            current_state = flat_hidden[token_positions]
            current_output = expert(current_state) * weights[token_positions, None]
            sparse.index_add_(0, token_positions, current_output.to(dtype=hidden_states.dtype))
        shared = self.shared_expert(hidden_states).reshape(-1, hidden_size)
        sparse_outputs.append(sparse.detach().to(device="cpu", dtype=torch.bfloat16))
        shared_outputs.append(shared.detach().to(device="cpu", dtype=torch.bfloat16))
        value = (sparse + shared).reshape_as(hidden_states)
        zero = hidden_states.new_zeros(())
        return value, (selected, zero, zero, zero)

    def block_hook(_module, _args, output):
        value = output[0] if isinstance(output, tuple) else output
        target_blocks.append(
            value.detach().reshape(-1, value.shape[-1]).to(device="cpu", dtype=torch.bfloat16)
        )

    had_instance_forward = "forward" in mlp.__dict__
    previous_instance_forward = mlp.__dict__.get("forward")
    mlp.forward = types.MethodType(forced_forward, mlp)
    hook = model.model.layers[layer_index].register_forward_hook(block_hook)
    try:
        with torch.inference_mode():
            seq_len = token_ids.shape[1]
            for doc_start in range(0, token_ids.shape[0], batch_size):
                state["offset"] = doc_start * seq_len
                batch = token_ids[doc_start : doc_start + batch_size].to(device, non_blocking=True)
                output = model.model(
                    input_ids=batch,
                    use_cache=False,
                    output_attentions=False,
                    output_hidden_states=False,
                    output_expert_labels=False,
                )
                final_outputs.append(
                    output.last_hidden_state.detach().reshape(-1, output.last_hidden_state.shape[-1]).to(
                        device="cpu", dtype=torch.bfloat16
                    )
                )
    finally:
        hook.remove()
        if had_instance_forward:
            mlp.forward = previous_instance_forward
        else:
            del mlp.forward

    return (
        torch.cat(sparse_outputs, dim=0),
        torch.cat(shared_outputs, dim=0),
        torch.cat(target_blocks, dim=0),
        torch.cat(final_outputs, dim=0),
    )


def linear_cka(x: torch.Tensor, y: torch.Tensor, device: str) -> float:
    xg = x.to(device=device, dtype=torch.float32)
    yg = y.to(device=device, dtype=torch.float32)
    xg = xg - xg.mean(dim=0, keepdim=True)
    yg = yg - yg.mean(dim=0, keepdim=True)
    cross = xg.T @ yg
    xx = xg.T @ xg
    yy = yg.T @ yg
    numerator = cross.square().sum()
    denominator = torch.sqrt(xx.square().sum() * yy.square().sum()).clamp_min(1e-20)
    return float((numerator / denominator).item())


def token_metrics(x: torch.Tensor, y: torch.Tensor, device: str) -> Tuple[float, float]:
    xg = x.to(device=device, dtype=torch.float32)
    yg = y.to(device=device, dtype=torch.float32)
    cosine = F.cosine_similarity(xg, yg, dim=-1, eps=1e-12).mean()
    frobenius = torch.linalg.vector_norm(xg - yg) / torch.linalg.vector_norm(xg).clamp_min(1e-12)
    return float(cosine.item()), float(frobenius.item())


def spectral_stats(y: torch.Tensor, device: str, top_r: int = 32) -> Dict[str, object]:
    value = y.to(device=device, dtype=torch.float32)
    value = value - value.mean(dim=0, keepdim=True)
    covariance = value.T @ value / max(value.shape[0] - 1, 1)
    eigenvalues, eigenvectors = torch.linalg.eigh(covariance)
    order = torch.argsort(eigenvalues, descending=True)
    eigenvalues = eigenvalues[order].clamp_min(0)
    eigenvectors = eigenvectors[:, order]
    probability = eigenvalues / eigenvalues.sum().clamp_min(1e-20)
    nonzero = probability[probability > 0]
    effective_rank = torch.exp(-(nonzero * nonzero.log()).sum())
    cumulative = torch.cumsum(probability, dim=0)
    rank90 = int(torch.searchsorted(cumulative, torch.tensor(0.90, device=device)).item() + 1)
    return {
        "probability": probability.cpu(),
        "basis": eigenvectors[:, :top_r].cpu(),
        "effective_rank": float(effective_rank.item()),
        "rank90": rank90,
    }


def compare_spectra(native: Dict[str, object], other: Dict[str, object], device: str) -> Dict[str, float]:
    p = native["probability"].to(device=device, dtype=torch.float32)
    q = other["probability"].to(device=device, dtype=torch.float32)
    spectrum_tv = 0.5 * torch.abs(p - q).sum()
    v0 = native["basis"].to(device=device, dtype=torch.float32)
    v1 = other["basis"].to(device=device, dtype=torch.float32)
    singular = torch.linalg.svdvals(v0.T @ v1).clamp(0, 1)
    angles = torch.rad2deg(torch.arccos(singular))
    return {
        "spectrum_tv": float(spectrum_tv.item()),
        "effective_rank_delta": float(abs(other["effective_rank"] - native["effective_rank"])),
        "rank90_delta": float(abs(other["rank90"] - native["rank90"])),
        "principal_angle_mean_deg": float(angles.mean().item()),
        "principal_angle_max_deg": float(angles.max().item()),
    }


def logit_metrics(
    model: torch.nn.Module,
    native_hidden: torch.Tensor,
    other_hidden: torch.Tensor,
    token_ids: torch.Tensor,
    docs_per_chunk: int,
    device: str,
) -> Dict[str, float]:
    num_docs, seq_len = token_ids.shape
    hidden_size = native_hidden.shape[-1]
    native_3d = native_hidden.view(num_docs, seq_len, hidden_size)
    other_3d = other_hidden.view(num_docs, seq_len, hidden_size)
    native_nll_sum = 0.0
    other_nll_sum = 0.0
    kl_sum = 0.0
    count = 0
    with torch.inference_mode():
        for start in range(0, num_docs, docs_per_chunk):
            end = min(start + docs_per_chunk, num_docs)
            h0 = native_3d[start:end, :-1].to(device=device, dtype=torch.bfloat16)
            h1 = other_3d[start:end, :-1].to(device=device, dtype=torch.bfloat16)
            targets = token_ids[start:end, 1:].to(device)
            logits0 = model.lm_head(h0)
            logits1 = model.lm_head(h1)
            flat_targets = targets.reshape(-1)
            flat0 = logits0.reshape(-1, logits0.shape[-1]).float()
            flat1 = logits1.reshape(-1, logits1.shape[-1]).float()
            native_nll_sum += float(F.cross_entropy(flat0, flat_targets, reduction="sum").item())
            other_nll_sum += float(F.cross_entropy(flat1, flat_targets, reduction="sum").item())
            logp0 = F.log_softmax(flat0, dim=-1)
            logp1 = F.log_softmax(flat1, dim=-1)
            kl_sum += float(F.kl_div(logp1, logp0, log_target=True, reduction="sum").item())
            count += int(flat_targets.numel())
            del h0, h1, logits0, logits1, flat0, flat1, logp0, logp1
    native_nll = native_nll_sum / count
    other_nll = other_nll_sum / count
    return {
        "native_nll": native_nll,
        "other_nll": other_nll,
        "nll_delta": other_nll - native_nll,
        "logit_kl": kl_sum / count,
    }


def safe_ratio(numerator: float, denominator: float, eps: float = 1e-12) -> float:
    if abs(denominator) <= eps:
        return float("nan")
    return float(numerator / denominator)


def analyze_layer(
    model_key: str,
    model: torch.nn.Module,
    layer_index: int,
    calibration_routing_input: torch.Tensor,
    evaluation_routing_input: torch.Tensor,
    evaluation_expert_input: torch.Tensor,
    native_block: torch.Tensor,
    native_final: torch.Tensor,
    evaluation_tokens: torch.Tensor,
    args: argparse.Namespace,
) -> Dict[str, object]:
    mlp = model.model.layers[layer_index].mlp
    seed = 20260729 + 100 * (["lb", "decommon"].index(model_key)) + layer_index
    routes = compute_routes(
        model_key,
        mlp,
        calibration_routing_input,
        evaluation_routing_input,
        args.device,
        seed,
        args.batch_size * evaluation_tokens.shape[1],
    )
    expert_bank_finite, expert_output_mean_norms = audit_all_experts(
        mlp, evaluation_expert_input, args.device, args.expert_batch_tokens
    )

    native_sparse, native_shared, noop_block, noop_final = run_forced_layer(
        model,
        evaluation_tokens,
        layer_index,
        routes["native_labels"],
        routes["native_weights"],
        args.batch_size,
        args.device,
    )
    center_sparse, center_shared, center_block, center_final = run_forced_layer(
        model,
        evaluation_tokens,
        layer_index,
        routes["center_labels"],
        routes["native_weights"],
        args.batch_size,
        args.device,
    )
    shuffle_sparse, shuffle_shared, shuffle_block, shuffle_final = run_forced_layer(
        model,
        evaluation_tokens,
        layer_index,
        routes["shuffle_labels"],
        routes["native_weights"],
        args.batch_size,
        args.device,
    )

    center_cka = linear_cka(native_sparse, center_sparse, args.device)
    shuffle_cka = linear_cka(native_sparse, shuffle_sparse, args.device)
    center_mask = routes["center_labels"] != routes["native_labels"]
    flip_only_cka = linear_cka(native_sparse[center_mask], center_sparse[center_mask], args.device)
    center_cosine, center_frobenius = token_metrics(native_sparse, center_sparse, args.device)
    shuffle_cosine, shuffle_frobenius = token_metrics(native_sparse, shuffle_sparse, args.device)

    r_value = safe_ratio(1.0 - center_cka, 1.0 - shuffle_cka)
    flip_ratio = safe_ratio(routes["center_flip"], routes["shuffle_flip"])
    flip_adjusted_r = safe_ratio(r_value, flip_ratio)

    native_spectrum = spectral_stats(native_sparse, args.device)
    center_spectrum = spectral_stats(center_sparse, args.device)
    shuffle_spectrum = spectral_stats(shuffle_sparse, args.device)
    center_spectral = compare_spectra(native_spectrum, center_spectrum, args.device)
    shuffle_spectral = compare_spectra(native_spectrum, shuffle_spectrum, args.device)

    noop_function = logit_metrics(
        model, native_final, noop_final, evaluation_tokens, args.logit_batch_docs, args.device
    )
    center_function = logit_metrics(
        model, native_final, center_final, evaluation_tokens, args.logit_batch_docs, args.device
    )
    shuffle_function = logit_metrics(
        model, native_final, shuffle_final, evaluation_tokens, args.logit_batch_docs, args.device
    )

    row: Dict[str, object] = {
        "model": model_key,
        "layer": layer_index + 1,
        "n_tokens": int(evaluation_routing_input.shape[0]),
        "seed": seed,
        "raw_center_flip_rate": routes["raw_center_flip"],
        "center_flip_rate": routes["center_flip"],
        "shuffle_flip_rate": routes["shuffle_flip"],
        "quota_repair_fraction": routes["quota_repair_fraction"],
        "load_exact": routes["load_exact"],
        "native_loads": json.dumps(routes["native_counts"].tolist()),
        "calibration_center_norm": routes["calibration_center_norm"],
        "checkpoint_center_norm": routes["checkpoint_center_norm"],
        "expert_bank_all_finite": expert_bank_finite,
        "expert_output_mean_norms": json.dumps(expert_output_mean_norms),
        "sparse_cka_center": center_cka,
        "sparse_cka_shuffle": shuffle_cka,
        "sparse_cka_center_flip_only": flip_only_cka,
        "r_value": r_value,
        "flip_rate_ratio_center_over_shuffle": flip_ratio,
        "flip_adjusted_r": flip_adjusted_r,
        "sparse_token_cosine_center": center_cosine,
        "sparse_token_cosine_shuffle": shuffle_cosine,
        "sparse_frobenius_center": center_frobenius,
        "sparse_frobenius_shuffle": shuffle_frobenius,
        "sparse_frobenius_ratio": safe_ratio(center_frobenius, shuffle_frobenius),
        "native_effective_rank": native_spectrum["effective_rank"],
        "center_effective_rank": center_spectrum["effective_rank"],
        "shuffle_effective_rank": shuffle_spectrum["effective_rank"],
        "native_rank90": native_spectrum["rank90"],
        "center_rank90": center_spectrum["rank90"],
        "shuffle_rank90": shuffle_spectrum["rank90"],
        "spectrum_tv_center": center_spectral["spectrum_tv"],
        "spectrum_tv_shuffle": shuffle_spectral["spectrum_tv"],
        "spectrum_tv_ratio": safe_ratio(center_spectral["spectrum_tv"], shuffle_spectral["spectrum_tv"]),
        "effective_rank_delta_center": center_spectral["effective_rank_delta"],
        "effective_rank_delta_shuffle": shuffle_spectral["effective_rank_delta"],
        "effective_rank_delta_ratio": safe_ratio(
            center_spectral["effective_rank_delta"], shuffle_spectral["effective_rank_delta"]
        ),
        "rank90_delta_center": center_spectral["rank90_delta"],
        "rank90_delta_shuffle": shuffle_spectral["rank90_delta"],
        "principal_angle_mean_center_deg": center_spectral["principal_angle_mean_deg"],
        "principal_angle_mean_shuffle_deg": shuffle_spectral["principal_angle_mean_deg"],
        "principal_angle_mean_ratio": safe_ratio(
            center_spectral["principal_angle_mean_deg"], shuffle_spectral["principal_angle_mean_deg"]
        ),
        "principal_angle_max_center_deg": center_spectral["principal_angle_max_deg"],
        "principal_angle_max_shuffle_deg": shuffle_spectral["principal_angle_max_deg"],
        "block_cka_noop": linear_cka(native_block, noop_block, args.device),
        "block_cka_center": linear_cka(native_block, center_block, args.device),
        "block_cka_shuffle": linear_cka(native_block, shuffle_block, args.device),
        "final_hidden_cka_noop": linear_cka(native_final, noop_final, args.device),
        "final_hidden_cka_center": linear_cka(native_final, center_final, args.device),
        "final_hidden_cka_shuffle": linear_cka(native_final, shuffle_final, args.device),
        "native_nll": center_function["native_nll"],
        "noop_nll_delta": noop_function["nll_delta"],
        "center_nll_delta": center_function["nll_delta"],
        "shuffle_nll_delta": shuffle_function["nll_delta"],
        "noop_logit_kl": noop_function["logit_kl"],
        "center_logit_kl": center_function["logit_kl"],
        "shuffle_logit_kl": shuffle_function["logit_kl"],
        "logit_kl_ratio": safe_ratio(center_function["logit_kl"], shuffle_function["logit_kl"]),
        "shared_invariance_max_abs": float(
            max(
                (native_shared.float() - center_shared.float()).abs().max().item(),
                (native_shared.float() - shuffle_shared.float()).abs().max().item(),
            )
        ),
    }
    row["noop_pass"] = bool(
        row["noop_logit_kl"] <= THRESHOLDS["noop_kl_max"]
        and abs(row["noop_nll_delta"]) <= THRESHOLDS["noop_abs_nll_delta_max"]
    )
    row["eligible"] = bool(
        routes["load_exact"]
        and expert_bank_finite
        and row["shared_invariance_max_abs"] == 0.0
        and row["noop_pass"]
        and routes["center_flip"] >= THRESHOLDS["center_flip_min"]
        and routes["shuffle_flip"] >= THRESHOLDS["shuffle_flip_min"]
        and shuffle_cka < THRESHOLDS["shuffle_sparse_cka_max"]
    )

    del native_sparse, center_sparse, shuffle_sparse
    del native_shared, center_shared, shuffle_shared
    del noop_block, noop_final, center_block, center_final, shuffle_block, shuffle_final
    gc.collect()
    torch.cuda.empty_cache()
    return row


def model_verdict(frame: pd.DataFrame) -> Dict[str, object]:
    eligible = frame[frame.eligible.astype(bool)].copy()
    result: Dict[str, object] = {
        "eligible_layers": int(len(eligible)),
        "total_layers": int(len(frame)),
        "eligible_layer_ids": eligible.layer.astype(int).tolist(),
    }
    if len(eligible) < THRESHOLDS["min_eligible_layers"]:
        result.update({"verdict": "insufficient", "reason": "fewer than eight eligible layers"})
        return result

    medians = {
        "median_r": float(eligible.r_value.median()),
        "median_flip_adjusted_r": float(eligible.flip_adjusted_r.median()),
        "median_flip_only_cka": float(eligible.sparse_cka_center_flip_only.median()),
        "median_spectrum_ratio": float(eligible.spectrum_tv_ratio.median()),
        "median_angle_ratio": float(eligible.principal_angle_mean_ratio.median()),
        "median_kl_ratio": float(eligible.logit_kl_ratio.median()),
        "max_abs_center_nll_delta": float(eligible.center_nll_delta.abs().max()),
    }
    result.update(medians)
    support = bool(
        medians["median_r"] <= THRESHOLDS["support_median_r_max"]
        and medians["median_flip_adjusted_r"] <= THRESHOLDS["support_median_flip_adjusted_r_max"]
        and medians["median_flip_only_cka"] >= THRESHOLDS["support_median_flip_only_cka_min"]
        and medians["median_spectrum_ratio"] <= THRESHOLDS["support_median_spectrum_ratio_max"]
        and medians["median_angle_ratio"] <= THRESHOLDS["support_median_angle_ratio_max"]
        and medians["median_kl_ratio"] <= THRESHOLDS["support_median_kl_ratio_max"]
        and medians["max_abs_center_nll_delta"] <= THRESHOLDS["support_abs_nll_delta_max"]
    )
    reject = bool(
        medians["median_r"] >= THRESHOLDS["reject_median_r_min"]
        or medians["median_flip_only_cka"] <= THRESHOLDS["reject_median_flip_only_cka_max"]
        or medians["median_kl_ratio"] >= THRESHOLDS["reject_median_kl_ratio_min"]
        or medians["max_abs_center_nll_delta"] >= THRESHOLDS["reject_abs_nll_delta_min"]
    )
    if support:
        result.update({"verdict": "support_h0", "reason": "all preregistered equivalence clauses passed"})
    elif reject:
        result.update({"verdict": "reject_h0", "reason": "at least one preregistered rejection clause fired"})
    else:
        result.update({"verdict": "insufficient", "reason": "eligible but between support and rejection regions"})
    return result


def main() -> None:
    args = parse_args()
    if args.smoke:
        args.calibration_docs = min(args.calibration_docs, 4)
        args.evaluation_docs = min(args.evaluation_docs, 4)
        args.batch_size = min(args.batch_size, 2)
        if args.layers is None:
            args.layers = [1]

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    split = build_token_split(args)
    model, config = load_model(MODEL_SPECS[args.model]["model_dir"], args.checkpoint_step, args.device)
    calibration_expert_inputs, calibration_routing_inputs, _, _ = capture_states(
        model, split.calibration, args.batch_size, args.device, capture_blocks=False
    )
    evaluation_expert_inputs, evaluation_routing_inputs, native_blocks, native_final = capture_states(
        model, split.evaluation, args.batch_size, args.device, capture_blocks=True
    )

    if args.layers is None:
        layer_indices = list(range(config.num_hidden_layers))
    else:
        layer_indices = [value - 1 for value in args.layers]
    if any(index < 0 or index >= config.num_hidden_layers for index in layer_indices):
        raise ValueError(f"Invalid layer list: {args.layers}")

    suffix = "_smoke" if args.smoke else ""
    output_csv = RESULTS_DIR / f"{args.model}_layer_metrics{suffix}.csv"
    rows: List[Dict[str, object]] = []
    for layer_index in layer_indices:
        row = analyze_layer(
            args.model,
            model,
            layer_index,
            calibration_routing_inputs[layer_index],
            evaluation_routing_inputs[layer_index],
            evaluation_expert_inputs[layer_index],
            native_blocks[layer_index],
            native_final,
            split.evaluation,
            args,
        )
        rows.append(row)
        pd.DataFrame(rows).sort_values("layer").to_csv(output_csv, index=False)
        print(
            json.dumps(
                {
                    "model": args.model,
                    "layer": layer_index + 1,
                    "center_flip": row["center_flip_rate"],
                    "r": row["r_value"],
                    "flip_cka": row["sparse_cka_center_flip_only"],
                    "kl_ratio": row["logit_kl_ratio"],
                    "nll_delta": row["center_nll_delta"],
                    "eligible": row["eligible"],
                },
                sort_keys=True,
            ),
            flush=True,
        )

    frame = pd.DataFrame(rows).sort_values("layer")
    verdict = model_verdict(frame)
    result_json = RESULTS_DIR / f"{args.model}_verdict{suffix}.json"
    result_json.write_text(json.dumps(verdict, indent=2, sort_keys=True) + "\n")
    manifest = {
        "experiment": "router_output_counterfactual",
        "model": args.model,
        "model_dir": str(MODEL_SPECS[args.model]["model_dir"]),
        "checkpoint_step": args.checkpoint_step,
        "architecture": {
            "layers": config.num_hidden_layers,
            "hidden_size": config.hidden_size,
            "experts": config.num_experts,
            "top_k": config.num_experts_per_tok,
            "norm_topk_prob": config.norm_topk_prob,
            "gating_reference": getattr(config, "gating_reference", None),
            "shared_expert_present": model.model.layers[0].mlp.shared_expert is not None,
        },
        "data": {
            "calibration_shape": list(split.calibration.shape),
            "evaluation_shape": list(split.evaluation.shape),
            "source_manifest": str(PRIOR_PROBE_DIR / "results/data_manifest.json"),
            "document_records": split.records,
        },
        "layers": [value + 1 for value in layer_indices],
        "thresholds": THRESHOLDS,
        "args": vars(args),
        "environment": {
            "python": platform.python_version(),
            "torch": torch.__version__,
            "cuda_visible_devices": os.environ.get("CUDA_VISIBLE_DEVICES"),
            "device_name": torch.cuda.get_device_name(torch.device(args.device)),
        },
        "verdict": verdict,
    }
    (RESULTS_DIR / f"{args.model}_manifest{suffix}.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n"
    )
    print(json.dumps(verdict, indent=2, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
