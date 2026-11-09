#!/usr/bin/env python3
"""Audit sorted expert-load rank distributions by token-frequency groups."""

from __future__ import annotations

import argparse
import csv
import importlib.util
import json
import math
from collections import defaultdict
from pathlib import Path
from typing import Any

import numpy as np
import torch


RESEARCH_ROOT = Path("/data/250010109/Research_System")
EXP_DIR = RESEARCH_ROOT / "Projects/from-attention-to-search/main/experiments/A06/06_01_geometry_and_state_discovery/A06_01_01_E01_common_filtered_spectrum"
RUNNER = EXP_DIR / "scripts/run_common_filtered_expert_spectrum_init.py"


def load_runner():
    spec = importlib.util.spec_from_file_location("a06_01_runner", RUNNER)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load runner from {RUNNER}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


runner = load_runner()
base = runner.base


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


def count_token_frequencies(dataset: Any, sample_indices: list[int], vocab_size: int, batch_size: int) -> torch.Tensor:
    counts = torch.zeros(vocab_size, dtype=torch.long)
    cpu = torch.device("cpu")
    for start in range(0, len(sample_indices), batch_size):
        batch_idx = sample_indices[start : start + batch_size]
        x, _ = dataset.batch(batch_idx, cpu)
        counts += torch.bincount(x.reshape(-1), minlength=vocab_size).long()
    return counts


def build_freq_masks(freq_counts: torch.Tensor, fracs: list[float]) -> tuple[dict[str, torch.Tensor], list[dict[str, Any]]]:
    observed = torch.nonzero(freq_counts > 0, as_tuple=False).flatten()
    sorted_obs = observed[torch.argsort(freq_counts[observed], descending=True)]
    masks: dict[str, torch.Tensor] = {}
    rows: list[dict[str, Any]] = []
    total = int(freq_counts.sum().item())
    for frac in fracs:
        k = max(1, int(math.ceil(float(frac) * int(observed.numel()))))
        ids = sorted_obs[:k]
        mask = torch.zeros_like(freq_counts, dtype=torch.bool)
        mask[ids] = True
        label = f"top_{str(frac).replace('.', 'p')}_observed_types"
        masks[label] = mask
        rows.append(
            {
                "frequency_group": label,
                "definition": f"top {frac:.4g} fraction of token types observed in init split",
                "observed_token_types": int(observed.numel()),
                "selected_token_types": int(ids.numel()),
                "selected_token_mass": int(freq_counts[ids].sum().item()),
                "selected_token_fraction": float(freq_counts[ids].sum().item() / max(total, 1)),
            }
        )
    return masks, rows


def load_metrics_from_counts(counts: torch.Tensor) -> dict[str, float | int | str]:
    counts = counts.float()
    total = counts.sum().clamp_min(1.0)
    p = counts / total
    nz = p[p > 0]
    entropy_raw = -(nz * torch.log(nz)).sum() if nz.numel() else torch.tensor(0.0)
    sorted_counts = torch.sort(counts, descending=True).values
    sorted_loads = sorted_counts / total
    return {
        "token_count": int(counts.sum().item()),
        "max_load": float(p.max().item()),
        "effective_experts": float(torch.exp(entropy_raw).item()),
        "active_experts": int((counts > 0).sum().item()),
        "counts_json": json.dumps([int(x) for x in counts.long().tolist()]),
        "rank_loads_json": json.dumps([float(x) for x in sorted_loads.tolist()]),
    }


def audit_counts(
    model: torch.nn.Module,
    dataset: Any,
    audit_indices: list[int],
    args: argparse.Namespace,
    device: torch.device,
    high_masks_cpu: dict[str, torch.Tensor],
) -> dict[tuple[int, str], torch.Tensor]:
    layers = [idx for idx, _, _ in base.iter_gate_modules(model)]
    if args.layers:
        layers = [idx for idx in layers if idx in set(args.layers)]
    counts = {(layer, "all_tokens"): torch.zeros(args.num_experts, dtype=torch.long) for layer in layers}
    for layer in layers:
        for label in high_masks_cpu:
            counts[(layer, f"high_freq_{label}")] = torch.zeros(args.num_experts, dtype=torch.long)
            counts[(layer, f"without_high_freq_{label}")] = torch.zeros(args.num_experts, dtype=torch.long)

    high_masks_gpu = {k: v.to(device=device) for k, v in high_masks_cpu.items()}
    model.eval()
    cap = base.GateCapture(model)
    with torch.no_grad():
        for start in range(0, len(audit_indices), args.token_audit_batch_size):
            batch_idx = audit_indices[start : start + args.token_audit_batch_size]
            x, _ = dataset.batch(batch_idx, device)
            token_flat = x.reshape(-1)
            cap.clear()
            _ = model.model(input_ids=x, use_cache=False)
            for layer_idx, _mlp, _gate in base.iter_gate_modules(model):
                if layer_idx not in layers:
                    continue
                _h, logits = cap.records[layer_idx]
                routes = torch.argmax(logits.float(), dim=-1)
                counts[(layer_idx, "all_tokens")] += torch.bincount(routes.detach().cpu(), minlength=args.num_experts).long()
                for label, mask_vocab in high_masks_gpu.items():
                    high = mask_vocab[token_flat]
                    if high.any():
                        counts[(layer_idx, f"high_freq_{label}")] += torch.bincount(
                            routes[high].detach().cpu(), minlength=args.num_experts
                        ).long()
                    low = ~high
                    if low.any():
                        counts[(layer_idx, f"without_high_freq_{label}")] += torch.bincount(
                            routes[low].detach().cpu(), minlength=args.num_experts
                        ).long()
    cap.close()
    return counts


def make_rank_rows(summary_rows: list[dict[str, Any]], num_experts: int) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in summary_rows:
        rank_loads = json.loads(str(row["rank_loads_json"]))
        for idx in range(num_experts):
            out = {
                "variant": row["variant"],
                "model_seed": row["model_seed"],
                "step": row["step"],
                "layer": row["layer"],
                "token_group": row["token_group"],
                "route_rank": idx + 1,
                "load_fraction": rank_loads[idx],
                "load_percent": 100.0 * rank_loads[idx],
            }
            rows.append(out)
    return rows


def aggregate_rank_rows(rank_rows: list[dict[str, Any]], late_layers: set[int]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    grouped: dict[tuple[Any, ...], list[float]] = defaultdict(list)
    for row in rank_rows:
        if int(row["layer"]) not in late_layers:
            continue
        key = (row["variant"], row["step"], row["token_group"], row["route_rank"])
        grouped[key].append(float(row["load_fraction"]))
    out: list[dict[str, Any]] = []
    for (variant, step, token_group, route_rank), values in sorted(grouped.items()):
        arr = np.asarray(values, dtype=float)
        out.append(
            {
                "variant": variant,
                "step": int(step),
                "layer_group": "late_layers_3_5",
                "token_group": token_group,
                "route_rank": int(route_rank),
                "load_fraction_mean": float(arr.mean()),
                "load_fraction_std": float(arr.std(ddof=0)),
                "load_percent_mean": float(100.0 * arr.mean()),
                "n": int(arr.size),
            }
        )

    by_key = {(r["variant"], r["token_group"], r["route_rank"], r["step"]): r for r in out}
    deltas: list[dict[str, Any]] = []
    for r in out:
        if int(r["step"]) != 10:
            continue
        base_r = by_key.get((r["variant"], r["token_group"], r["route_rank"], 0))
        if base_r is None:
            continue
        delta = float(r["load_fraction_mean"]) - float(base_r["load_fraction_mean"])
        deltas.append(
            {
                "variant": r["variant"],
                "token_group": r["token_group"],
                "route_rank": int(r["route_rank"]),
                "step10_minus_step0_load_fraction": delta,
                "step10_minus_step0_load_percent": 100.0 * delta,
            }
        )
    return out, deltas


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", type=Path, default=EXP_DIR / "runs/common_filtered_expert_spectrum_init/a06_01_common_filtered_expert_spectrum_init_4gpu_20260614_full01")
    parser.add_argument("--output-dir", type=Path, default=EXP_DIR)
    parser.add_argument("--steps", type=int, nargs="+", default=[0, 10])
    parser.add_argument("--layers", type=int, nargs="*", default=None)
    parser.add_argument("--audit-num-sequences", type=int, default=None)
    parser.add_argument("--init-num-sequences", type=int, default=None)
    parser.add_argument("--token-audit-batch-size", type=int, default=64)
    parser.add_argument("--frequency-count-batch-size", type=int, default=256)
    parser.add_argument("--top-type-fracs", type=float, nargs="+", default=[0.01, 0.05])
    parser.add_argument("--device", default="cuda:0")
    parser.add_argument("--variants", nargs="*", default=None)
    parser.add_argument("--seeds", type=int, nargs="*", default=None)
    args = parser.parse_args()

    cli = {
        "run_dir": args.run_dir,
        "output_dir": args.output_dir,
        "steps": args.steps,
        "layers": args.layers,
        "audit_num_sequences": args.audit_num_sequences,
        "init_num_sequences": args.init_num_sequences,
        "token_audit_batch_size": args.token_audit_batch_size,
        "frequency_count_batch_size": args.frequency_count_batch_size,
        "top_type_fracs": args.top_type_fracs,
        "device": args.device,
        "variants": args.variants,
        "seeds": args.seeds,
    }
    with (args.run_dir / "config/run_config.json").open(encoding="utf-8") as f:
        cfg = json.load(f)
    for key, value in cfg.items():
        setattr(args, key, value)
    for key, value in cli.items():
        setattr(args, key, value)
    args.audit_num_sequences = int(args.audit_num_sequences or cfg["audit_num_sequences"])
    args.init_num_sequences = int(args.init_num_sequences or cfg["init_num_sequences"])
    args.variants = args.variants or cfg["variants"]
    args.seeds = args.seeds or cfg["model_seeds"]

    device = torch.device(args.device if torch.cuda.is_available() and str(args.device).startswith("cuda") else "cpu")
    dataset = base.PackedBinDataset(Path(cfg["data_path"]))
    init_indices = list(range(args.init_num_sequences))
    audit_indices = list(range(args.init_num_sequences, args.init_num_sequences + args.audit_num_sequences))

    freq_counts = count_token_frequencies(dataset, init_indices, args.vocab_size, args.frequency_count_batch_size)
    high_masks, freq_rows = build_freq_masks(freq_counts, args.top_type_fracs)

    summary_rows: list[dict[str, Any]] = []
    for variant in args.variants:
        for seed in args.seeds:
            for step in args.steps:
                ckpt = args.run_dir / "checkpoints" / f"{variant}_seed{seed}_step{step}.pt"
                if not ckpt.exists():
                    raise FileNotFoundError(ckpt)
                model = base.make_model(args.num_experts, int(seed), args, device)
                state = torch.load(ckpt, map_location=device)
                model.load_state_dict(state["model_state_dict"])
                group_counts = audit_counts(model, dataset, audit_indices, args, device, high_masks)
                for (layer, group), counts in sorted(group_counts.items()):
                    row = {
                        "variant": variant,
                        "model_seed": int(seed),
                        "step": int(step),
                        "layer": int(layer),
                        "token_group": group,
                    }
                    row.update(load_metrics_from_counts(counts))
                    summary_rows.append(row)
                del model
                if torch.cuda.is_available():
                    torch.cuda.empty_cache()

    rank_rows = make_rank_rows(summary_rows, int(args.num_experts))
    rank_late_rows, rank_delta_rows = aggregate_rank_rows(rank_rows, late_layers={3, 4, 5})

    out = args.output_dir / "tables/token_frequency_routing"
    write_csv(out / "frequency_group_definition_rank_audit.csv", freq_rows)
    write_csv(out / "step0_step10_frequency_group_route_summary.csv", summary_rows)
    write_csv(out / "step0_step10_frequency_group_rank_distribution.csv", rank_rows)
    write_csv(out / "step0_step10_late_layer_rank_distribution_summary.csv", rank_late_rows)
    write_csv(out / "step10_minus_step0_late_layer_rank_distribution_delta.csv", rank_delta_rows)
    with (out / "rank_audit_run_summary.json").open("w", encoding="utf-8") as f:
        json.dump(
            {
                "run_dir": str(args.run_dir),
                "audit_num_sequences": args.audit_num_sequences,
                "init_num_sequences": args.init_num_sequences,
                "variants": args.variants,
                "seeds": args.seeds,
                "steps": args.steps,
                "layers": args.layers,
                "top_type_fracs": args.top_type_fracs,
                "summary_rows": len(summary_rows),
                "rank_rows": len(rank_rows),
                "rank_late_rows": len(rank_late_rows),
                "rank_delta_rows": len(rank_delta_rows),
            },
            f,
            indent=2,
            sort_keys=True,
        )
    print(f"wrote token-frequency rank routing audit to {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
