#!/usr/bin/env python3
"""Audit whether step-0 top-k concentration is driven by frequent token ids."""

from __future__ import annotations

import argparse
import csv
import importlib.util
import json
import math
from collections import Counter
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import numpy as np
import torch


EXP_DIR = Path(__file__).resolve().parents[1]
RUNNER_PATH = EXP_DIR / "scripts" / "run_real_text_common_logit_audit.py"


def load_runner():
    spec = importlib.util.spec_from_file_location("real_text_common_logit_runner", RUNNER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load runner from {RUNNER_PATH}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def gini_from_counts(counts: torch.Tensor) -> float:
    counts = counts.float()
    if counts.sum() <= 0:
        return 0.0
    n = float(counts.numel())
    sorted_counts = torch.sort(counts).values
    weights = 2 * torch.arange(1, counts.numel() + 1, device=counts.device).float() - n - 1
    return float((weights * sorted_counts).sum().item() / (n * sorted_counts.sum().item()))


def metrics_from_counts(counts: torch.Tensor, total: int, num_experts: int) -> dict[str, Any]:
    if total <= 0:
        return {
            "max_selection_share": 0.0,
            "top2_selection_share": 0.0,
            "top4_selection_share": 0.0,
            "active_experts": 0,
            "active_experts_ratio": 0.0,
            "routing_entropy": 0.0,
            "effective_experts": 0.0,
            "gini_load": 0.0,
            "counts_json": "[]",
            "shares_json": "[]",
        }
    p = counts.float() / float(total)
    nz = p[p > 0]
    entropy = float((-(nz * torch.log(nz)).sum() / math.log(num_experts)).item()) if len(nz) else 0.0
    sorted_p = torch.sort(p, descending=True).values
    return {
        "max_selection_share": float(sorted_p[0].item()),
        "top2_selection_share": float(sorted_p[: min(2, num_experts)].sum().item()),
        "top4_selection_share": float(sorted_p[: min(4, num_experts)].sum().item()),
        "active_experts": int((counts > 0).sum().item()),
        "active_experts_ratio": float((counts > 0).float().mean().item()),
        "routing_entropy": entropy,
        "effective_experts": float(num_experts**entropy),
        "gini_load": gini_from_counts(counts),
        "counts_json": json.dumps([int(x) for x in counts.cpu().tolist()]),
        "shares_json": json.dumps([round(float(x), 8) for x in p.cpu().tolist()]),
    }


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    seen = set()
    for row in rows:
        for key in row:
            if key not in seen:
                fields.append(key)
                seen.add(key)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-path", default="/data/share/109_cache_dir/hf_data/dclm_bin")
    parser.add_argument("--output-dir", default=str(EXP_DIR / "quick_topk_token_frequency_audit_full8192"))
    parser.add_argument("--num-sequences", type=int, default=8192)
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--num-experts", type=int, default=8)
    parser.add_argument("--seeds", default="0,1,2")
    parser.add_argument("--topks", default="1,2,4")
    parser.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    args = parser.parse_args()

    runner = load_runner()
    run_args = SimpleNamespace(
        vocab_size=151936,
        hidden_size=512,
        num_layers=6,
        num_heads=8,
        num_key_value_heads=4,
        expert_hidden_dim=2048,
        initializer_range=0.02,
        audit_batch_size=args.batch_size,
    )
    device = torch.device(args.device)
    dataset = runner.PackedBinDataset(Path(args.data_path))
    sample_indices = list(range(args.num_sequences))
    seeds = [int(x) for x in args.seeds.split(",") if x.strip()]
    topks = [int(x) for x in args.topks.split(",") if x.strip()]
    out_dir = Path(args.output_dir)

    token_counter: Counter[int] = Counter()
    for start in range(0, len(sample_indices), args.batch_size):
        x, _ = dataset.batch(sample_indices[start : start + args.batch_size], torch.device("cpu"))
        token_counter.update(int(v) for v in x.reshape(-1).tolist())

    total_tokens = args.num_sequences * 256
    top_ids = {
        "top10_ids": {tok for tok, _ in token_counter.most_common(10)},
        "top50_ids": {tok for tok, _ in token_counter.most_common(50)},
        "top200_ids": {tok for tok, _ in token_counter.most_common(200)},
    }
    group_names = ["all", "top10_ids", "top50_ids", "top200_ids", "not_top10", "not_top50", "not_top200"]

    rows: list[dict[str, Any]] = []
    for seed in seeds:
        model = runner.make_model(args.num_experts, seed, run_args, device)
        model.eval()
        cap = runner.GateCapture(model)
        layers = [idx for idx, _, _ in runner.iter_gate_modules(model)]
        counts = {
            (layer, k, group): torch.zeros(args.num_experts, dtype=torch.long, device=device)
            for layer in layers
            for k in topks
            for group in group_names
        }
        token_counts = {(layer, group): 0 for layer in layers for group in group_names}

        with torch.no_grad():
            for start in range(0, len(sample_indices), args.batch_size):
                batch_idx = sample_indices[start : start + args.batch_size]
                x, _ = dataset.batch(batch_idx, device)
                flat_x = x.reshape(-1)
                masks = {
                    "all": torch.ones_like(flat_x, dtype=torch.bool),
                    "top10_ids": torch.zeros_like(flat_x, dtype=torch.bool),
                    "top50_ids": torch.zeros_like(flat_x, dtype=torch.bool),
                    "top200_ids": torch.zeros_like(flat_x, dtype=torch.bool),
                    "not_top10": torch.ones_like(flat_x, dtype=torch.bool),
                    "not_top50": torch.ones_like(flat_x, dtype=torch.bool),
                    "not_top200": torch.ones_like(flat_x, dtype=torch.bool),
                }
                for group, ids in top_ids.items():
                    if ids:
                        id_tensor = torch.tensor(sorted(ids), device=device, dtype=flat_x.dtype)
                        m = (flat_x[:, None] == id_tensor[None, :]).any(dim=1)
                    else:
                        m = torch.zeros_like(flat_x, dtype=torch.bool)
                    masks[group] = m
                    masks["not_" + group.replace("_ids", "")] = ~m

                cap.clear()
                _ = model.model(input_ids=x, use_cache=False)
                for layer_idx, (_h, logits) in cap.records.items():
                    lf = logits.float()
                    for group, mask in masks.items():
                        n_tok = int(mask.sum().item())
                        token_counts[(layer_idx, group)] += n_tok
                    for k in topks:
                        top_idx_all = torch.topk(lf, k=k, dim=-1).indices
                        for group, mask in masks.items():
                            if not mask.any():
                                continue
                            top_idx = top_idx_all[mask].reshape(-1)
                            counts[(layer_idx, k, group)] += torch.bincount(top_idx, minlength=args.num_experts)

        cap.close()
        for layer in layers:
            for k in topks:
                for group in group_names:
                    n_tok = token_counts[(layer, group)]
                    total = n_tok * k
                    row = {
                        "model_seed": seed,
                        "layer": layer,
                        "num_experts": args.num_experts,
                        "top_k_readout": k,
                        "group": group,
                        "token_count": n_tok,
                        "selection_count": total,
                        "token_fraction": n_tok / max(total_tokens, 1),
                        "uniform_share": 1.0 / args.num_experts,
                    }
                    row.update(metrics_from_counts(counts[(layer, k, group)], total, args.num_experts))
                    rows.append(row)
        del model
        if torch.cuda.is_available():
            torch.cuda.empty_cache()

    write_csv(out_dir / "topk_by_token_frequency_metrics.csv", rows)
    token_summary = {
        "num_sequences": args.num_sequences,
        "total_tokens": total_tokens,
        "unique_token_ids": len(token_counter),
        "top_tokens": token_counter.most_common(30),
        "top10_fraction": sum(c for _, c in token_counter.most_common(10)) / total_tokens,
        "top50_fraction": sum(c for _, c in token_counter.most_common(50)) / total_tokens,
        "top200_fraction": sum(c for _, c in token_counter.most_common(200)) / total_tokens,
    }
    summary: dict[str, Any] = {"token_summary": token_summary, "by_group_topk": {}}
    for group in group_names:
        summary["by_group_topk"][group] = {}
        for k in topks:
            sub = [r for r in rows if r["group"] == group and r["top_k_readout"] == k and r["token_count"] > 0]
            summary["by_group_topk"][group][str(k)] = {
                "token_fraction_mean": float(np.mean([r["token_fraction"] for r in sub])),
                "max_selection_share_mean": float(np.mean([r["max_selection_share"] for r in sub])),
                "max_selection_share_max": float(np.max([r["max_selection_share"] for r in sub])),
                "top2_selection_share_mean": float(np.mean([r["top2_selection_share"] for r in sub])),
                "top4_selection_share_mean": float(np.mean([r["top4_selection_share"] for r in sub])),
                "effective_experts_mean": float(np.mean([r["effective_experts"] for r in sub])),
                "gini_load_mean": float(np.mean([r["gini_load"] for r in sub])),
            }
    (out_dir / "topk_by_token_frequency_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
