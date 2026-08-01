#!/usr/bin/env python3
"""Paired layer/band probe for the canonical LB and decommon MoE checkpoints.

The probe is deliberately diagnostic.  It measures whether the partition made by
the frozen linear routers is visible in fixed, layerwise covariance bands.  It
does not treat expert utility as a target and does not train a new router.
"""

from __future__ import annotations

import argparse
import gc
import hashlib
import io
import json
import math
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple

import numpy as np
import pandas as pd
import torch
import torch.nn.functional as F
import zstandard as zstd
from scipy.stats import spearmanr
from sklearn.metrics import normalized_mutual_info_score
from transformers import AutoTokenizer, __version__ as transformers_version


EXPERIMENT_DIR = Path(__file__).resolve().parent
MOE_ROOT = Path("/mnt/bucket/MoE_Router")
DATA_FILE = Path(
    "/mnt/bucket/109_cache_dir/hf_data/dclm_eval_holdout/"
    "global-shard_02_of_10/local-shard_0_of_10/"
    "shard_00000000_processed.jsonl.zst"
)
RESULTS_DIR = EXPERIMENT_DIR / "results"
TOKENIZER_NAME = "Qwen/Qwen2.5-0.5B"
EXPECTED_DATA_SHA256 = "4c5ce60258943051758148653c448bb57724af7592cc9d3e9c053cc6f9e10323"


MODEL_SPECS = {
    "lb": {
        "display_name": "LB",
        "model_dir": MOE_ROOT
        / "outputs/qwen_moe_runs/output_moe/"
        "qwen3-moe-H768-linear_nocenter_lb001_8gpu-center_off-gate_off-acp_off-lb_0.01-linear",
        "native_center": "raw",
    },
    "decommon": {
        "display_name": "decommon",
        "model_dir": MOE_ROOT
        / "outputs/qwen_moe_runs/output_moe/"
        "qwen3-moe-H768--linear_running_center_8gpu_gbs768-center_running-gate_off-acp_off-lb_0-linear",
        "native_center": "checkpoint_running",
    },
}


@dataclass
class TokenSplit:
    calibration: torch.Tensor
    evaluation: torch.Tensor
    records: List[dict]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoint-step", type=int, default=40000)
    parser.add_argument("--calibration-docs", type=int, default=32)
    parser.add_argument("--evaluation-docs", type=int, default=64)
    parser.add_argument("--max-length", type=int, default=256)
    parser.add_argument("--batch-size", type=int, default=4)
    parser.add_argument("--band-width", type=int, default=64)
    parser.add_argument("--random-controls", type=int, default=4)
    parser.add_argument("--candidate-pool", type=int, default=512)
    parser.add_argument("--device", default="cuda:0")
    parser.add_argument("--models", nargs="+", choices=sorted(MODEL_SPECS), default=sorted(MODEL_SPECS))
    parser.add_argument("--smoke", action="store_true")
    return parser.parse_args()


def sha256_file(path: Path, chunk_size: int = 8 << 20) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while True:
            chunk = handle.read(chunk_size)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def iter_jsonl_zst(path: Path) -> Iterable[Tuple[int, dict]]:
    with path.open("rb") as raw:
        reader = zstd.ZstdDecompressor().stream_reader(raw)
        with io.TextIOWrapper(reader, encoding="utf-8") as text_stream:
            for line_number, line in enumerate(text_stream):
                try:
                    yield line_number, json.loads(line)
                except json.JSONDecodeError:
                    continue


def build_token_split(args: argparse.Namespace) -> TokenSplit:
    if not DATA_FILE.is_file():
        raise FileNotFoundError(DATA_FILE)
    actual_hash = sha256_file(DATA_FILE)
    if actual_hash != EXPECTED_DATA_SHA256:
        raise RuntimeError(f"DCLM shard checksum mismatch: {actual_hash}")

    tokenizer = AutoTokenizer.from_pretrained(TOKENIZER_NAME, trust_remote_code=True)
    needed = args.calibration_docs + args.evaluation_docs
    candidate_pool = max(args.candidate_pool, needed)
    candidates: List[Tuple[str, List[int], dict]] = []

    for line_number, item in iter_jsonl_zst(DATA_FILE):
        text = item.get("text", "")
        if not isinstance(text, str) or not text.strip():
            continue
        token_ids = tokenizer.encode(text, add_special_tokens=False)
        if len(token_ids) < args.max_length:
            continue
        stable_source = f"{item.get('url', '')}\n{text[:512]}".encode("utf-8", errors="replace")
        document_hash = hashlib.sha256(stable_source).hexdigest()
        max_start = len(token_ids) - args.max_length
        start = int(document_hash[:16], 16) % (max_start + 1)
        selected = token_ids[start : start + args.max_length]
        candidates.append(
            (
                document_hash,
                selected,
                {
                    "line_number": line_number,
                    "document_sha256": document_hash,
                    "url_sha256": hashlib.sha256(str(item.get("url", "")).encode()).hexdigest(),
                    "source_token_count": len(token_ids),
                    "slice_start": start,
                    "slice_length": args.max_length,
                },
            )
        )
        if len(candidates) >= candidate_pool:
            break

    if len(candidates) < needed:
        raise RuntimeError(f"Only found {len(candidates)} qualifying documents, need {needed}")
    candidates.sort(key=lambda row: row[0])
    chosen = candidates[:needed]

    records: List[dict] = []
    tensors: List[torch.Tensor] = []
    for position, (_, token_ids, record) in enumerate(chosen):
        split = "calibration" if position < args.calibration_docs else "evaluation"
        records.append({"split": split, **record})
        tensors.append(torch.tensor(token_ids, dtype=torch.long))

    calibration = torch.stack(tensors[: args.calibration_docs])
    evaluation = torch.stack(tensors[args.calibration_docs :])
    return TokenSplit(calibration=calibration, evaluation=evaluation, records=records)


def load_model(model_dir: Path, checkpoint_step: int, device: str):
    if str(MOE_ROOT) not in sys.path:
        sys.path.insert(0, str(MOE_ROOT))
    import router_eval.eval_utils as eval_utils

    # These are trusted, locally produced DeepSpeed checkpoints.  PyTorch 2.5's
    # restricted unpickler rejects their client-state metadata, so use the
    # explicit legacy loader while retaining mmap and CPU placement.
    eval_utils._load_checkpoint_state_dict = lambda path: torch.load(
        path, map_location="cpu", weights_only=False, mmap=True
    )
    model, config = eval_utils.load_moe_model(
        str(model_dir), device=device, checkpoint_step=checkpoint_step
    )
    if (config.num_hidden_layers, config.hidden_size, config.num_experts, config.num_experts_per_tok) != (
        12,
        768,
        8,
        1,
    ):
        raise AssertionError(
            "Unexpected checkpoint architecture: "
            f"L={config.num_hidden_layers}, H={config.hidden_size}, "
            f"E={config.num_experts}, K={config.num_experts_per_tok}"
        )
    model.eval()
    model.to(device=device, dtype=torch.bfloat16)
    return model, config


def extract_router_inputs(
    model: torch.nn.Module,
    token_ids: torch.Tensor,
    batch_size: int,
    device: str,
) -> List[torch.Tensor]:
    num_layers = len(model.model.layers)
    chunks: List[List[torch.Tensor]] = [[] for _ in range(num_layers)]
    hooks = []

    def make_hook(layer_index: int):
        def hook(_module, args):
            hidden = args[0].detach().reshape(-1, args[0].shape[-1])
            chunks[layer_index].append(hidden.to(device="cpu", dtype=torch.float16))

        return hook

    for layer_index, layer in enumerate(model.model.layers):
        hooks.append(layer.mlp.register_forward_pre_hook(make_hook(layer_index)))

    try:
        with torch.inference_mode():
            for start in range(0, token_ids.shape[0], batch_size):
                batch = token_ids[start : start + batch_size].to(device, non_blocking=True)
                model.model(
                    input_ids=batch,
                    use_cache=False,
                    output_attentions=False,
                    output_hidden_states=False,
                    output_expert_labels=False,
                )
    finally:
        for handle in hooks:
            handle.remove()

    return [torch.cat(layer_chunks, dim=0) for layer_chunks in chunks]


def route_metrics(logits: torch.Tensor, num_experts: int) -> Tuple[np.ndarray, dict]:
    top2 = torch.topk(logits.float(), k=2, dim=-1)
    labels = top2.indices[:, 0].cpu().numpy().astype(np.int64)
    counts = np.bincount(labels, minlength=num_experts).astype(np.float64)
    shares = counts / max(counts.sum(), 1.0)
    nonzero = shares[shares > 0]
    entropy = float(-(nonzero * np.log(nonzero)).sum())
    normalized_entropy = entropy / math.log(num_experts)
    per_token_scale = logits.float().std(dim=-1, unbiased=False).clamp_min(1e-8)
    normalized_margin = ((top2.values[:, 0] - top2.values[:, 1]) / per_token_scale).cpu().numpy()
    metrics = {
        "n_tokens": int(labels.size),
        "load_cv": float(shares.std(ddof=0) / (shares.mean() + 1e-12)),
        "normalized_entropy": normalized_entropy,
        "effective_experts": float(math.exp(entropy)),
        "max_share": float(shares.max()),
        "min_share": float(shares.min()),
        "normalized_margin_mean": float(normalized_margin.mean()),
        "normalized_margin_p05": float(np.quantile(normalized_margin, 0.05)),
        **{f"expert_{idx}_share": float(value) for idx, value in enumerate(shares)},
    }
    return labels, metrics


def eta_squared_scalar(values: np.ndarray, labels: np.ndarray, num_classes: int) -> float:
    values = np.asarray(values, dtype=np.float64)
    overall = values.mean()
    total = np.square(values - overall).sum()
    if total <= 1e-18:
        return 0.0
    between = 0.0
    for expert in range(num_classes):
        group = values[labels == expert]
        if group.size:
            between += group.size * float((group.mean() - overall) ** 2)
    return float(between / total)


def eta_squared_features(features: np.ndarray, labels: np.ndarray, num_classes: int) -> float:
    features = np.asarray(features, dtype=np.float64)
    overall = features.mean(axis=0, keepdims=True)
    total = np.square(features - overall).sum()
    if total <= 1e-18:
        return 0.0
    between = 0.0
    for expert in range(num_classes):
        group = features[labels == expert]
        if group.size:
            delta = group.mean(axis=0, keepdims=True) - overall
            between += group.shape[0] * float(np.square(delta).sum())
    return float(between / total)


def quantile_bins(values: np.ndarray, num_bins: int = 16) -> np.ndarray:
    values = np.asarray(values)
    order = np.argsort(values, kind="mergesort")
    bins = np.empty(values.size, dtype=np.int64)
    bins[order] = np.minimum((np.arange(values.size) * num_bins) // max(values.size, 1), num_bins - 1)
    return bins


def energy_label_nmi(values: np.ndarray, labels: np.ndarray) -> float:
    return float(normalized_mutual_info_score(labels, quantile_bins(values)))


def categorical_concentration(labels: np.ndarray, num_classes: int) -> dict:
    shares = np.bincount(labels, minlength=num_classes).astype(np.float64)
    shares /= max(shares.sum(), 1.0)
    nonzero = shares[shares > 0]
    entropy = float(-(nonzero * np.log(nonzero)).sum())
    return {
        "max_share": float(shares.max()),
        "normalized_entropy": float(entropy / math.log(num_classes)),
        "effective_categories": float(math.exp(entropy)),
    }


def compute_basis(centered_calibration: torch.Tensor, device: str) -> Tuple[torch.Tensor, torch.Tensor]:
    x = centered_calibration.to(device=device, dtype=torch.float32)
    covariance = x.T @ x / max(x.shape[0] - 1, 1)
    eigenvalues, eigenvectors = torch.linalg.eigh(covariance)
    order = torch.argsort(eigenvalues, descending=True)
    return eigenvalues[order].clamp_min(0).cpu(), eigenvectors[:, order].cpu()


def random_orthogonal_basis(hidden_size: int, seed: int, device: str) -> torch.Tensor:
    generator = torch.Generator(device="cpu").manual_seed(seed)
    gaussian = torch.randn(hidden_size, hidden_size, generator=generator, dtype=torch.float32)
    q, _ = torch.linalg.qr(gaussian)
    return q.to(device)


def analyze_model(
    model_key: str,
    model: torch.nn.Module,
    calibration_features: Sequence[torch.Tensor],
    evaluation_features: Sequence[torch.Tensor],
    args: argparse.Namespace,
) -> Tuple[List[dict], List[dict], List[dict], List[dict]]:
    num_layers = len(calibration_features)
    hidden_size = calibration_features[0].shape[-1]
    num_experts = model.config.num_experts
    if hidden_size % args.band_width:
        raise ValueError(f"band width {args.band_width} must divide hidden size {hidden_size}")
    num_bands = hidden_size // args.band_width

    calibration_means = [layer.float().mean(dim=0) for layer in calibration_features]
    bases: List[torch.Tensor] = []
    eigenvalues: List[torch.Tensor] = []
    for layer_index in range(num_layers):
        values, vectors = compute_basis(
            calibration_features[layer_index].float() - calibration_means[layer_index], args.device
        )
        eigenvalues.append(values)
        bases.append(vectors)

    route_rows: List[dict] = []
    band_rows: List[dict] = []
    energy_router_rows: List[dict] = []
    center_rows: List[dict] = []

    for layer_index in range(num_layers):
        mlp = model.model.layers[layer_index].mlp
        gate_weight = mlp.gate.weight.detach().float().to(args.device)
        x_cal_raw = calibration_features[layer_index].to(args.device, dtype=torch.float32)
        x_eval_raw = evaluation_features[layer_index].to(args.device, dtype=torch.float32)
        calibration_mean = calibration_means[layer_index].to(args.device)
        checkpoint_center = getattr(mlp, "router_running_mean", torch.zeros(hidden_size)).detach().float().to(args.device)

        center_rows.append(
            {
                "model": model_key,
                "layer": layer_index + 1,
                "calibration_center_norm": float(calibration_mean.norm().item()),
                "checkpoint_center_norm": float(checkpoint_center.norm().item()),
                "center_delta_norm": float((calibration_mean - checkpoint_center).norm().item()),
                "center_cosine": float(
                    F.cosine_similarity(calibration_mean[None], checkpoint_center[None], dim=-1, eps=1e-12).item()
                ),
            }
        )

        if MODEL_SPECS[model_key]["native_center"] == "checkpoint_running":
            native_center = checkpoint_center
        else:
            native_center = torch.zeros_like(calibration_mean)

        view_centers = {
            "native": native_center,
            "frozen_center": calibration_mean,
        }
        route_labels_cal: Dict[str, np.ndarray] = {}
        route_labels_eval: Dict[str, np.ndarray] = {}

        for view, center in view_centers.items():
            cal_logits = F.linear(x_cal_raw - center, gate_weight)
            eval_logits = F.linear(x_eval_raw - center, gate_weight)
            cal_labels, _ = route_metrics(cal_logits, num_experts)
            eval_labels, metrics = route_metrics(eval_logits, num_experts)
            route_labels_cal[view] = cal_labels
            route_labels_eval[view] = eval_labels
            route_rows.append(
                {
                    "model": model_key,
                    "layer": layer_index + 1,
                    "view": view,
                    **metrics,
                }
            )

        native_labels = route_labels_eval["native"]
        frozen_labels = route_labels_eval["frozen_center"]
        agreement = float(np.mean(native_labels == frozen_labels))
        for row in route_rows[-2:]:
            row["native_frozen_agreement"] = agreement
            row["native_frozen_switch_rate"] = 1.0 - agreement

        x_cal = x_cal_raw - calibration_mean
        x_eval = x_eval_raw - calibration_mean
        basis = bases[layer_index].to(args.device)
        z_cal = x_cal @ basis
        z_eval = x_eval @ basis
        total_eval_energy = z_eval.square().sum(dim=1).mean().item()

        wrong_basis = bases[(layer_index + 1) % num_layers].to(args.device)
        z_wrong = x_eval @ wrong_basis

        random_metrics: Dict[Tuple[str, int], List[Tuple[float, float]]] = {
            (view, band): [] for view in view_centers for band in range(num_bands)
        }
        for control_index in range(args.random_controls):
            random_basis = random_orthogonal_basis(
                hidden_size,
                seed=20260729 + 1000 * layer_index + control_index,
                device=args.device,
            )
            z_random = x_eval @ random_basis
            for band in range(num_bands):
                start = band * args.band_width
                end = start + args.band_width
                random_band = z_random[:, start:end]
                random_energy = random_band.square().sum(dim=1).cpu().numpy()
                random_features = random_band.cpu().numpy()
                for view, labels in route_labels_eval.items():
                    random_metrics[(view, band)].append(
                        (
                            eta_squared_features(random_features, labels, num_experts),
                            eta_squared_scalar(random_energy, labels, num_experts),
                        )
                    )

        energy_cal_columns: List[np.ndarray] = []
        energy_eval_columns: List[np.ndarray] = []
        total_spectral_variance = float(eigenvalues[layer_index].sum().item())
        cumulative_variance = torch.cumsum(eigenvalues[layer_index], dim=0)

        for band in range(num_bands):
            start = band * args.band_width
            end = start + args.band_width
            cal_band = z_cal[:, start:end]
            eval_band = z_eval[:, start:end]
            wrong_band = z_wrong[:, start:end]
            cal_energy = cal_band.square().sum(dim=1).cpu().numpy()
            eval_energy = eval_band.square().sum(dim=1).cpu().numpy()
            wrong_energy = wrong_band.square().sum(dim=1).cpu().numpy()
            eval_features_np = eval_band.cpu().numpy()
            energy_cal_columns.append(cal_energy)
            energy_eval_columns.append(eval_energy)

            band_variance = float(eigenvalues[layer_index][start:end].sum().item())
            random_array_by_view = {
                view: np.asarray(random_metrics[(view, band)], dtype=np.float64) for view in view_centers
            }
            for view, labels in route_labels_eval.items():
                random_values = random_array_by_view[view]
                feature_eta2 = eta_squared_features(eval_features_np, labels, num_experts)
                energy_eta2 = eta_squared_scalar(eval_energy, labels, num_experts)
                band_rows.append(
                    {
                        "model": model_key,
                        "layer": layer_index + 1,
                        "view": view,
                        "band": band + 1,
                        "rank_start": start + 1,
                        "rank_end": end,
                        "band_dim": args.band_width,
                        "explained_variance_fraction": band_variance / max(total_spectral_variance, 1e-12),
                        "cumulative_variance_end": float(cumulative_variance[end - 1].item())
                        / max(total_spectral_variance, 1e-12),
                        "energy_fraction": float(eval_energy.mean() / max(total_eval_energy, 1e-12)),
                        "energy_per_dimension": float(eval_energy.mean() / args.band_width),
                        "energy_mean_over_std": float(eval_energy.mean() / (eval_energy.std() + 1e-12)),
                        "feature_eta2": feature_eta2,
                        "energy_eta2": energy_eta2,
                        "energy_quantile_nmi": energy_label_nmi(eval_energy, labels),
                        "wrong_layer_energy_eta2": eta_squared_scalar(wrong_energy, labels, num_experts),
                        "random_feature_eta2_mean": float(random_values[:, 0].mean()),
                        "random_feature_eta2_std": float(random_values[:, 0].std(ddof=0)),
                        "random_energy_eta2_mean": float(random_values[:, 1].mean()),
                        "random_energy_eta2_std": float(random_values[:, 1].std(ddof=0)),
                        "feature_eta2_minus_random": feature_eta2 - float(random_values[:, 0].mean()),
                        "energy_eta2_minus_random": energy_eta2 - float(random_values[:, 1].mean()),
                    }
                )

        energy_cal_matrix = np.stack(energy_cal_columns, axis=1)
        energy_eval_matrix = np.stack(energy_eval_columns, axis=1)
        energy_mean = energy_cal_matrix.mean(axis=0, keepdims=True)
        energy_std = energy_cal_matrix.std(axis=0, keepdims=True) + 1e-12
        standardized_energy = (energy_eval_matrix - energy_mean) / energy_std
        raw_winners = energy_eval_matrix.argmax(axis=1)
        standardized_winners = standardized_energy.argmax(axis=1)

        for view, labels in route_labels_eval.items():
            raw_concentration = categorical_concentration(raw_winners, num_bands)
            standardized_concentration = categorical_concentration(standardized_winners, num_bands)
            energy_router_rows.append(
                {
                    "model": model_key,
                    "layer": layer_index + 1,
                    "view": view,
                    "raw_band_winner_nmi_with_route": float(normalized_mutual_info_score(labels, raw_winners)),
                    "standardized_band_winner_nmi_with_route": float(
                        normalized_mutual_info_score(labels, standardized_winners)
                    ),
                    **{f"raw_{key}": value for key, value in raw_concentration.items()},
                    **{f"standardized_{key}": value for key, value in standardized_concentration.items()},
                }
            )

        del x_cal_raw, x_eval_raw, x_cal, x_eval, z_cal, z_eval, z_wrong, basis, wrong_basis
        torch.cuda.empty_cache()

    return route_rows, band_rows, energy_router_rows, center_rows


def build_layer_summary(route_df: pd.DataFrame, band_df: pd.DataFrame) -> pd.DataFrame:
    rows: List[dict] = []
    for (model, layer, view), group in band_df.groupby(["model", "layer", "view"], sort=True):
        group = group.sort_values("band")
        route_row = route_df[
            (route_df.model == model) & (route_df.layer == layer) & (route_df.view == view)
        ].iloc[0]
        rho_energy, p_energy = spearmanr(group.band, group.energy_eta2)
        rho_feature, p_feature = spearmanr(group.band, group.feature_eta2)
        peak = group.loc[group.energy_eta2.idxmax()]
        head = group[group.band <= 3]
        middle = group[(group.band >= 4) & (group.band <= 8)]
        tail = group[group.band >= 9]
        rows.append(
            {
                "model": model,
                "layer": int(layer),
                "view": view,
                "load_cv": route_row.load_cv,
                "normalized_entropy": route_row.normalized_entropy,
                "effective_experts": route_row.effective_experts,
                "max_share": route_row.max_share,
                "normalized_margin_mean": route_row.normalized_margin_mean,
                "native_frozen_agreement": route_row.native_frozen_agreement,
                "energy_eta2_head_mean": head.energy_eta2.mean(),
                "energy_eta2_middle_mean": middle.energy_eta2.mean(),
                "energy_eta2_tail_mean": tail.energy_eta2.mean(),
                "energy_eta2_minus_random_head_mean": head.energy_eta2_minus_random.mean(),
                "energy_eta2_minus_random_middle_mean": middle.energy_eta2_minus_random.mean(),
                "energy_eta2_minus_random_tail_mean": tail.energy_eta2_minus_random.mean(),
                "band_depth_energy_eta2_spearman_rho": float(rho_energy),
                "band_depth_energy_eta2_spearman_p": float(p_energy),
                "band_depth_feature_eta2_spearman_rho": float(rho_feature),
                "band_depth_feature_eta2_spearman_p": float(p_feature),
                "peak_energy_band": int(peak.band),
                "peak_energy_rank_start": int(peak.rank_start),
                "peak_energy_rank_end": int(peak.rank_end),
                "peak_energy_eta2": float(peak.energy_eta2),
                "peak_energy_eta2_minus_random": float(peak.energy_eta2_minus_random),
            }
        )
    return pd.DataFrame(rows)


def write_manifest(args: argparse.Namespace, split: TokenSplit) -> None:
    manifest = {
        "experiment": "router_layer_band_probe",
        "transformers_version": transformers_version,
        "torch_version": torch.__version__,
        "checkpoint_step": args.checkpoint_step,
        "models": {
            key: {
                "model_dir": str(MODEL_SPECS[key]["model_dir"]),
                "checkpoint": str(
                    MODEL_SPECS[key]["model_dir"]
                    / f"checkpoints/checkpoint-{args.checkpoint_step}/mp_rank_00_model_states.pt"
                ),
                "native_center": MODEL_SPECS[key]["native_center"],
            }
            for key in args.models
        },
        "training_data_verified_from_logs": "/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10",
        "heldout_data": {
            "dataset_repo": "mlfoundations/dclm-baseline-1.0",
            "repo_path": "global-shard_02_of_10/local-shard_0_of_10/shard_00000000_processed.jsonl.zst",
            "local_path": str(DATA_FILE),
            "sha256": sha256_file(DATA_FILE),
            "training_global_shard": "global-shard_01_of_10",
            "evaluation_global_shard": "global-shard_02_of_10",
            "strictly_disjoint_top_level_shard": True,
        },
        "tokenizer": TOKENIZER_NAME,
        "calibration_shape": list(split.calibration.shape),
        "evaluation_shape": list(split.evaluation.shape),
        "band_width": args.band_width,
        "random_controls": args.random_controls,
        "routing_views": {
            "native": "LB uses raw h; decommon uses the checkpoint running center frozen in eval mode",
            "frozen_center": "both gates are read out offline on h minus an independent calibration mean; no redispatch",
        },
        "document_records": split.records,
    }
    (RESULTS_DIR / "data_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def main() -> None:
    args = parse_args()
    if args.smoke:
        args.calibration_docs = min(args.calibration_docs, 4)
        args.evaluation_docs = min(args.evaluation_docs, 4)
        args.max_length = min(args.max_length, 64)
        args.random_controls = min(args.random_controls, 1)
        args.candidate_pool = max(args.calibration_docs + args.evaluation_docs, 16)
    if not transformers_version.startswith("4.51."):
        raise RuntimeError(
            f"This checkpoint code requires transformers 4.51.x, found {transformers_version}. "
            "Run with the pinned overlay described in README.md."
        )
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    split = build_token_split(args)
    write_manifest(args, split)

    all_route_rows: List[dict] = []
    all_band_rows: List[dict] = []
    all_energy_router_rows: List[dict] = []
    all_center_rows: List[dict] = []

    combined_tokens = torch.cat([split.calibration, split.evaluation], dim=0)
    calibration_tokens = split.calibration.shape[0] * split.calibration.shape[1]

    for model_key in args.models:
        print(f"[probe] loading {model_key}", flush=True)
        model, _ = load_model(MODEL_SPECS[model_key]["model_dir"], args.checkpoint_step, args.device)
        print(f"[probe] extracting layer inputs for {model_key}", flush=True)
        features = extract_router_inputs(model, combined_tokens, args.batch_size, args.device)
        calibration_features = [layer[:calibration_tokens] for layer in features]
        evaluation_features = [layer[calibration_tokens:] for layer in features]
        print(f"[probe] analyzing bands for {model_key}", flush=True)
        route_rows, band_rows, energy_router_rows, center_rows = analyze_model(
            model_key,
            model,
            calibration_features,
            evaluation_features,
            args,
        )
        all_route_rows.extend(route_rows)
        all_band_rows.extend(band_rows)
        all_energy_router_rows.extend(energy_router_rows)
        all_center_rows.extend(center_rows)
        del model, features, calibration_features, evaluation_features
        gc.collect()
        torch.cuda.empty_cache()

    route_df = pd.DataFrame(all_route_rows).sort_values(["model", "view", "layer"])
    band_df = pd.DataFrame(all_band_rows).sort_values(["model", "view", "layer", "band"])
    energy_router_df = pd.DataFrame(all_energy_router_rows).sort_values(["model", "view", "layer"])
    center_df = pd.DataFrame(all_center_rows).sort_values(["model", "layer"])
    layer_summary_df = build_layer_summary(route_df, band_df).sort_values(["model", "view", "layer"])

    suffix = "_smoke" if args.smoke else ""
    route_df.to_csv(RESULTS_DIR / f"route_concentration{suffix}.csv", index=False)
    band_df.to_csv(RESULTS_DIR / f"band_separability{suffix}.csv", index=False)
    energy_router_df.to_csv(RESULTS_DIR / f"energy_router_summary{suffix}.csv", index=False)
    center_df.to_csv(RESULTS_DIR / f"center_comparison{suffix}.csv", index=False)
    layer_summary_df.to_csv(RESULTS_DIR / f"layer_summary{suffix}.csv", index=False)
    print(f"[probe] wrote results to {RESULTS_DIR}", flush=True)


if __name__ == "__main__":
    main()
