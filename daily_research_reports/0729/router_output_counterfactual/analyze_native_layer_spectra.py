#!/usr/bin/env python3
"""Descriptive native-output spectrum audit for the two frozen MoE models.

This appendix reuses the exact held-out token split from the approved
counterfactual experiment.  It reconstructs each layer's native sparse-expert
output (selected expert output times the native top-1 weight), centers the
token-by-feature matrix, and saves its complete normalized covariance spectrum.

The two checkpoints differ in both centering and load-balance training, so the
cross-model comparison is descriptive and must not be read causally.
"""

from __future__ import annotations

import argparse
import gc
import hashlib
import json
import math
import os
import platform
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd
import torch
import torch.nn.functional as F

from run_experiment import MODEL_SPECS, build_token_split, capture_states, load_model
import run_probe


EXPERIMENT_DIR = Path(__file__).resolve().parent
RESULTS_DIR = EXPERIMENT_DIR / "results/native_layer_spectra"
LOCAL_TOKENIZER = Path("/mnt/bucket/MoE_Router/configs")


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
    parser.add_argument("--layers", type=int, nargs="*", default=None, help="One-based layers")
    parser.add_argument("--smoke", action="store_true")
    return parser.parse_args()


def compute_native_routes(
    model_key: str,
    mlp: torch.nn.Module,
    routing_input: torch.Tensor,
    device: str,
    chunk_tokens: int,
) -> Tuple[torch.Tensor, torch.Tensor]:
    hidden_size = routing_input.shape[-1]
    checkpoint_center = getattr(
        mlp,
        "router_running_mean",
        torch.zeros(hidden_size, dtype=torch.float32, device=device),
    ).detach().float().to(device)
    if MODEL_SPECS[model_key]["native_center"] == "checkpoint_running":
        native_center = checkpoint_center
    else:
        native_center = torch.zeros_like(checkpoint_center)

    labels: List[torch.Tensor] = []
    weights: List[torch.Tensor] = []
    with torch.inference_mode():
        for start in range(0, routing_input.shape[0], chunk_tokens):
            value = routing_input[start : start + chunk_tokens].to(device=device, dtype=torch.bfloat16)
            logits = mlp.gate(value - native_center.to(dtype=value.dtype))
            probability = F.softmax(logits, dim=-1, dtype=torch.float32)
            weight, label = probability.max(dim=-1)
            labels.append(label.cpu())
            weights.append(weight.to(dtype=torch.bfloat16).cpu())
    return torch.cat(labels).long(), torch.cat(weights).to(dtype=torch.bfloat16)


def compute_native_sparse(
    mlp: torch.nn.Module,
    expert_input: torch.Tensor,
    labels: torch.Tensor,
    weights: torch.Tensor,
    device: str,
    chunk_tokens: int,
) -> torch.Tensor:
    sparse = torch.zeros_like(expert_input, dtype=torch.bfloat16, device="cpu")
    with torch.inference_mode():
        for expert_id, expert in enumerate(mlp.experts):
            positions = torch.where(labels == expert_id)[0]
            for start in range(0, positions.numel(), chunk_tokens):
                current_positions = positions[start : start + chunk_tokens]
                hidden = expert_input[current_positions].to(device=device, dtype=torch.bfloat16)
                output = expert(hidden)
                output = output * weights[current_positions].to(device=device, dtype=output.dtype)[:, None]
                if not torch.isfinite(output).all():
                    raise RuntimeError(f"Non-finite native output for expert {expert_id}")
                sparse[current_positions] = output.to(device="cpu", dtype=torch.bfloat16)
    return sparse


def spectrum_stats(output: torch.Tensor, device: str) -> Tuple[np.ndarray, Dict[str, float]]:
    value = output.to(device=device, dtype=torch.float32)
    value = value - value.mean(dim=0, keepdim=True)
    covariance = value.T @ value / max(value.shape[0] - 1, 1)
    eigenvalues = torch.linalg.eigvalsh(covariance).flip(0).clamp_min(0)
    total = eigenvalues.sum().clamp_min(1e-20)
    probability = eigenvalues / total
    nonzero = probability[probability > 0]
    effective_rank = torch.exp(-(nonzero * nonzero.log()).sum())
    cumulative = probability.cumsum(dim=0)
    rank90 = torch.searchsorted(cumulative, torch.tensor(0.90, device=device)).item() + 1
    probability_np = probability.cpu().numpy()

    def top_energy(k: int) -> float:
        return float(probability[:k].sum().item())

    stats = {
        "effective_rank": float(effective_rank.item()),
        "rank90": int(rank90),
        "top1_energy": top_energy(1),
        "top8_energy": top_energy(8),
        "top32_energy": top_energy(32),
        "stable_rank": float((1.0 / probability[0].clamp_min(1e-20)).item()),
        "total_centered_variance": float(total.item()),
        "output_mean_norm": float(output.float().mean(dim=0).norm().item()),
        "output_rms_norm": float(torch.sqrt(output.float().square().sum(dim=1).mean()).item()),
    }
    del value, covariance, eigenvalues, probability
    torch.cuda.empty_cache()
    return probability_np, stats


def token_sha256(tokens: torch.Tensor) -> str:
    array = tokens.detach().cpu().numpy().astype(np.int64, copy=False)
    return hashlib.sha256(array.tobytes(order="C")).hexdigest()


def main() -> None:
    args = parse_args()
    if args.smoke:
        args.calibration_docs = min(args.calibration_docs, 4)
        args.evaluation_docs = min(args.evaluation_docs, 4)
        args.batch_size = min(args.batch_size, 2)
        if args.layers is None:
            args.layers = [1]

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    if not (LOCAL_TOKENIZER / "tokenizer.json").is_file():
        raise FileNotFoundError(LOCAL_TOKENIZER / "tokenizer.json")
    # Avoid network-dependent tokenizer resolution while preserving the exact
    # tokenizer files used by the MoE workspace.
    run_probe.TOKENIZER_NAME = str(LOCAL_TOKENIZER)
    split = build_token_split(args)
    model, config = load_model(MODEL_SPECS[args.model]["model_dir"], args.checkpoint_step, args.device)
    expert_inputs, routing_inputs, _, final_output = capture_states(
        model,
        split.evaluation,
        args.batch_size,
        args.device,
        capture_blocks=False,
    )
    del final_output

    if args.layers is None:
        layer_indices = list(range(config.num_hidden_layers))
    else:
        layer_indices = [layer - 1 for layer in args.layers]
    if any(layer < 0 or layer >= config.num_hidden_layers for layer in layer_indices):
        raise ValueError(f"Invalid layer list: {args.layers}")

    summary_rows: List[Dict[str, object]] = []
    spectrum_rows: List[Dict[str, object]] = []
    for layer_index in layer_indices:
        mlp = model.model.layers[layer_index].mlp
        labels, weights = compute_native_routes(
            args.model,
            mlp,
            routing_inputs[layer_index],
            args.device,
            args.expert_batch_tokens,
        )
        sparse = compute_native_sparse(
            mlp,
            expert_inputs[layer_index],
            labels,
            weights,
            args.device,
            args.expert_batch_tokens,
        )
        probability, stats = spectrum_stats(sparse, args.device)
        counts = np.bincount(labels.numpy(), minlength=config.num_experts)
        row = {
            "model": args.model,
            "layer": layer_index + 1,
            "n_tokens": int(labels.numel()),
            "load_min": int(counts.min()),
            "load_max": int(counts.max()),
            **stats,
        }
        summary_rows.append(row)
        spectrum_rows.extend(
            {
                "model": args.model,
                "layer": layer_index + 1,
                "spectral_rank": rank + 1,
                "normalized_energy": float(energy),
            }
            for rank, energy in enumerate(probability)
        )
        print(json.dumps(row, sort_keys=True), flush=True)
        del labels, weights, sparse, probability
        gc.collect()
        torch.cuda.empty_cache()

    suffix = "_smoke" if args.smoke else ""
    pd.DataFrame(summary_rows).sort_values("layer").to_csv(
        RESULTS_DIR / f"{args.model}_summary{suffix}.csv", index=False
    )
    pd.DataFrame(spectrum_rows).sort_values(["layer", "spectral_rank"]).to_csv(
        RESULTS_DIR / f"{args.model}_spectrum{suffix}.csv", index=False
    )
    manifest = {
        "analysis": "native_layer_spectra",
        "model": args.model,
        "model_dir": str(MODEL_SPECS[args.model]["model_dir"]),
        "checkpoint_step": args.checkpoint_step,
        "matrix": "centered native sparse MoE output: native top-1 weight times selected expert output",
        "normalization": "covariance eigenvalues divided by their sum",
        "layers": [layer + 1 for layer in layer_indices],
        "evaluation_shape": list(split.evaluation.shape),
        "evaluation_token_sha256": token_sha256(split.evaluation),
        "args": vars(args),
        "environment": {
            "python": platform.python_version(),
            "torch": torch.__version__,
            "cuda_visible_devices": os.environ.get("CUDA_VISIBLE_DEVICES"),
            "device_name": torch.cuda.get_device_name(torch.device(args.device)),
        },
        "claim_boundary": "Descriptive checkpoint comparison only; the two models differ in both centering and load-balance training.",
    }
    (RESULTS_DIR / f"{args.model}_manifest{suffix}.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n"
    )


if __name__ == "__main__":
    main()
