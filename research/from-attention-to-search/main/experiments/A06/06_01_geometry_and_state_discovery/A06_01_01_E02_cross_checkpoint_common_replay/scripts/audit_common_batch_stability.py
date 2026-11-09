#!/usr/bin/env python3
"""Audit cross-batch stability of router-input common components.

This is a post-hoc audit over existing checkpoints. It does not train or update
the model. For each checkpoint, it computes the router-input mean vector c on
multiple disjoint DCLM splits and compares c direction, Wc winner, and Wc
margin across splits and across two independent sample sets.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path
from typing import Any

import torch
import torch.nn.functional as F

from run_cross_checkpoint_replay import (
    GateCapture,
    PackedBinDataset,
    iter_gate_modules,
    make_model,
    top_margin,
)


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


def load_run_args(run_dir: Path) -> argparse.Namespace:
    cfg = json.loads((run_dir / "config/run_config.json").read_text(encoding="utf-8"))
    return argparse.Namespace(**cfg)


def split_indices(start_index: int, num_splits: int, seqs_per_split: int) -> dict[int, list[int]]:
    out: dict[int, list[int]] = {}
    cursor = start_index
    for split in range(num_splits):
        out[split] = list(range(cursor, cursor + seqs_per_split))
        cursor += seqs_per_split
    return out


def compute_split_common(
    model,
    dataset: PackedBinDataset,
    split_map: dict[tuple[str, int], list[int]],
    args: argparse.Namespace,
    device: torch.device,
) -> tuple[dict[tuple[str, int, int], torch.Tensor], dict[tuple[str, int, int], int]]:
    model.eval()
    cap = GateCapture(model)
    layer_ids = [idx for idx, _, _ in iter_gate_modules(model)]
    sums = {
        (set_name, split_id, layer): torch.zeros(args.hidden_size, device=device)
        for set_name, split_id in split_map
        for layer in layer_ids
    }
    counts = {(set_name, split_id, layer): 0 for set_name, split_id in split_map for layer in layer_ids}

    with torch.no_grad():
        for set_name, split_id in sorted(split_map):
            indices = split_map[(set_name, split_id)]
            for start in range(0, len(indices), args.audit_batch_size):
                batch_idx = indices[start : start + args.audit_batch_size]
                x, _ = dataset.batch(batch_idx, device)
                cap.clear()
                _ = model.model(input_ids=x, use_cache=False)
                for layer, (h, _logits) in cap.records.items():
                    key = (set_name, split_id, layer)
                    if key not in sums:
                        continue
                    hf = h.detach().float()
                    sums[key] += hf.sum(dim=0)
                    counts[key] += hf.shape[0]
    cap.close()

    common = {k: sums[k] / max(counts[k], 1) for k in sums}
    return common, counts


def mean_vec(vectors: list[torch.Tensor]) -> torch.Tensor:
    return torch.stack(vectors, dim=0).mean(dim=0)


def safe_cos(a: torch.Tensor, b: torch.Tensor) -> float:
    return float(F.cosine_similarity(a.view(1, -1), b.view(1, -1), dim=-1).item())


def pairwise_stats(values: list[float]) -> dict[str, float]:
    if not values:
        return {"mean": float("nan"), "min": float("nan"), "median": float("nan")}
    vals = sorted(values)
    mid = len(vals) // 2
    median = vals[mid] if len(vals) % 2 else 0.5 * (vals[mid - 1] + vals[mid])
    return {"mean": sum(vals) / len(vals), "min": vals[0], "median": median}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--steps", type=int, nargs="+", default=[0, 10, 300])
    parser.add_argument("--seeds", type=int, nargs="+", default=[0, 1, 2])
    parser.add_argument("--num-splits", type=int, default=8)
    parser.add_argument("--seqs-per-split", type=int, default=128)
    parser.add_argument("--primary-start", type=int, default=0)
    parser.add_argument("--secondary-start", type=int, default=50000)
    parser.add_argument("--audit-batch-size", type=int, default=16)
    parser.add_argument("--device", default="cuda:0")
    args_cli = parser.parse_args()

    run_dir = args_cli.run_dir
    run_args = load_run_args(run_dir)
    run_args.audit_batch_size = args_cli.audit_batch_size
    dataset = PackedBinDataset(Path(run_args.data_path))
    device = torch.device(args_cli.device if torch.cuda.is_available() else "cpu")

    primary = split_indices(args_cli.primary_start, args_cli.num_splits, args_cli.seqs_per_split)
    secondary = split_indices(args_cli.secondary_start, args_cli.num_splits, args_cli.seqs_per_split)
    split_map = {("primary", k): v for k, v in primary.items()}
    split_map.update({("secondary", k): v for k, v in secondary.items()})

    split_rows: list[dict[str, Any]] = []
    summary_rows: list[dict[str, Any]] = []
    set_compare_rows: list[dict[str, Any]] = []
    checkpoint_rows: list[dict[str, Any]] = []
    common_store: dict[tuple[int, int, str, int, int], torch.Tensor] = {}
    global_store: dict[tuple[int, int, str, int], torch.Tensor] = {}

    for seed in args_cli.seeds:
        model = make_model(run_args.num_experts, seed, run_args, device)
        for step in args_cli.steps:
            ckpt_path = run_dir / "checkpoints" / f"normal_seed{seed}_step{step}.pt"
            state = torch.load(ckpt_path, map_location=device)
            model.load_state_dict(state["model_state_dict"])
            common, counts = compute_split_common(model, dataset, split_map, run_args, device)
            gates = {layer: gate.weight.detach().float().to(device) for layer, _, gate in iter_gate_modules(model)}
            layers = sorted(gates)

            for set_name in ["primary", "secondary"]:
                for layer in layers:
                    vectors = [common[(set_name, split_id, layer)] for split_id in range(args_cli.num_splits)]
                    c_global = mean_vec(vectors)
                    global_store[(seed, step, set_name, layer)] = c_global.detach().cpu()
                    w = gates[layer]
                    global_logits = w @ c_global
                    global_winner = int(torch.argmax(global_logits).item())
                    global_margin = float(top_margin(global_logits.view(1, -1)).item())

                    cos_vals = []
                    same_winner_vals = []
                    margin_vals = []
                    norm_vals = []
                    for split_id, c in enumerate(vectors):
                        common_store[(seed, step, set_name, split_id, layer)] = c.detach().cpu()
                        logits = w @ c
                        winner = int(torch.argmax(logits).item())
                        margin = float(top_margin(logits.view(1, -1)).item())
                        cos_to_global = safe_cos(c, c_global)
                        cos_vals.append(cos_to_global)
                        same_winner_vals.append(float(winner == global_winner))
                        margin_vals.append(margin)
                        norm_vals.append(float(c.norm().item()))
                        split_rows.append(
                            {
                                "model_seed": seed,
                                "step": step,
                                "set_name": set_name,
                                "split_id": split_id,
                                "layer": layer,
                                "token_count": counts[(set_name, split_id, layer)],
                                "c_norm": float(c.norm().item()),
                                "cos_to_set_global": cos_to_global,
                                "common_margin": margin,
                                "common_winner": winner,
                                "set_global_margin": global_margin,
                                "set_global_winner": global_winner,
                                "winner_matches_set_global": int(winner == global_winner),
                            }
                        )

                    pair_cos = []
                    pair_same_winner = []
                    winners = []
                    for i in range(args_cli.num_splits):
                        ci = vectors[i]
                        wi = int(torch.argmax(w @ ci).item())
                        winners.append(wi)
                        for j in range(i + 1, args_cli.num_splits):
                            cj = vectors[j]
                            wj = int(torch.argmax(w @ cj).item())
                            pair_cos.append(safe_cos(ci, cj))
                            pair_same_winner.append(float(wi == wj))
                    pair = pairwise_stats(pair_cos)
                    margin_mean = sum(margin_vals) / len(margin_vals)
                    margin_std = math.sqrt(sum((x - margin_mean) ** 2 for x in margin_vals) / len(margin_vals))
                    norm_mean = sum(norm_vals) / len(norm_vals)
                    norm_std = math.sqrt(sum((x - norm_mean) ** 2 for x in norm_vals) / len(norm_vals))
                    summary_rows.append(
                        {
                            "model_seed": seed,
                            "step": step,
                            "set_name": set_name,
                            "layer": layer,
                            "num_splits": args_cli.num_splits,
                            "seqs_per_split": args_cli.seqs_per_split,
                            "tokens_per_split": args_cli.seqs_per_split * 256,
                            "cos_to_global_mean": sum(cos_vals) / len(cos_vals),
                            "cos_to_global_min": min(cos_vals),
                            "pairwise_cos_mean": pair["mean"],
                            "pairwise_cos_min": pair["min"],
                            "pairwise_cos_median": pair["median"],
                            "winner_match_global_rate": sum(same_winner_vals) / len(same_winner_vals),
                            "pairwise_same_winner_rate": sum(pair_same_winner) / len(pair_same_winner),
                            "unique_common_winners": len(set(winners)),
                            "margin_mean": margin_mean,
                            "margin_std": margin_std,
                            "margin_cv": margin_std / max(abs(margin_mean), 1e-8),
                            "norm_mean": norm_mean,
                            "norm_std": norm_std,
                            "norm_cv": norm_std / max(abs(norm_mean), 1e-8),
                        }
                    )

            for layer in layers:
                cp = global_store[(seed, step, "primary", layer)]
                cs = global_store[(seed, step, "secondary", layer)]
                w = gates[layer]
                lp = w @ cp.to(device)
                ls = w @ cs.to(device)
                wp = int(torch.argmax(lp).item())
                ws = int(torch.argmax(ls).item())
                mp = float(top_margin(lp.view(1, -1)).item())
                ms = float(top_margin(ls.view(1, -1)).item())
                set_compare_rows.append(
                    {
                        "model_seed": seed,
                        "step": step,
                        "layer": layer,
                        "primary_secondary_cos": safe_cos(cp.to(device), cs.to(device)),
                        "primary_winner": wp,
                        "secondary_winner": ws,
                        "winner_agree": int(wp == ws),
                        "primary_margin": mp,
                        "secondary_margin": ms,
                        "margin_abs_diff": abs(mp - ms),
                        "primary_norm": float(cp.norm().item()),
                        "secondary_norm": float(cs.norm().item()),
                        "norm_abs_diff": abs(float(cp.norm().item()) - float(cs.norm().item())),
                    }
                )
        del model
        if torch.cuda.is_available():
            torch.cuda.empty_cache()

    for seed in args_cli.seeds:
        for set_name in ["primary", "secondary"]:
            for layer in range(run_args.num_layers):
                if (seed, 0, set_name, layer) not in global_store:
                    continue
                c0 = global_store[(seed, 0, set_name, layer)]
                for step in args_cli.steps:
                    c = global_store[(seed, step, set_name, layer)]
                    checkpoint_rows.append(
                        {
                            "model_seed": seed,
                            "set_name": set_name,
                            "layer": layer,
                            "reference_step": 0,
                            "step": step,
                            "cos_to_step0": safe_cos(c.to(device), c0.to(device)),
                        }
                    )

    out_dir = run_dir / "results"
    write_csv(out_dir / "common_batch_stability_split.csv", split_rows)
    write_csv(out_dir / "common_batch_stability_summary.csv", summary_rows)
    write_csv(out_dir / "common_batch_stability_set_compare.csv", set_compare_rows)
    write_csv(out_dir / "common_checkpoint_stability.csv", checkpoint_rows)
    print(json.dumps(
        {
            "split_rows": len(split_rows),
            "summary_rows": len(summary_rows),
            "set_compare_rows": len(set_compare_rows),
            "checkpoint_rows": len(checkpoint_rows),
            "output_dir": str(out_dir),
        },
        indent=2,
    ))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
