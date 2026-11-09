#!/usr/bin/env python3
"""Audit step-0 routing by empirical token frequency groups."""

from __future__ import annotations

import argparse
import csv
import importlib.util
import json
import math
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


def load_metrics_from_counts(counts: torch.Tensor) -> dict[str, float | int]:
    counts = counts.float()
    total = counts.sum().clamp_min(1.0)
    p = counts / total
    nz = p[p > 0]
    entropy_raw = -(nz * torch.log(nz)).sum() if nz.numel() else torch.tensor(0.0)
    entropy = entropy_raw / math.log(len(counts))
    sorted_counts = torch.sort(counts).values
    n = float(len(counts))
    gini_weights = 2 * torch.arange(1, len(counts) + 1, device=counts.device).float() - n - 1
    gini = (gini_weights * sorted_counts).sum() / (n * sorted_counts.sum().clamp_min(1.0))
    return {
        "token_count": int(counts.sum().item()),
        "max_load": float(p.max().item()),
        "effective_experts": float(torch.exp(entropy_raw).item()),
        "routing_entropy": float(entropy.item()),
        "active_experts": int((counts > 0).sum().item()),
        "gini_load": float(gini.item()),
        "counts_json": json.dumps([int(x) for x in counts.long().tolist()]),
    }


def count_token_frequencies(dataset: Any, sample_indices: list[int], vocab_size: int, batch_size: int) -> torch.Tensor:
    counts = torch.zeros(vocab_size, dtype=torch.long)
    cpu = torch.device("cpu")
    for start in range(0, len(sample_indices), batch_size):
        batch_idx = sample_indices[start : start + batch_size]
        x, _ = dataset.batch(batch_idx, cpu)
        counts += torch.bincount(x.reshape(-1), minlength=vocab_size).long()
    return counts


def build_freq_masks(freq_counts: torch.Tensor, fracs: list[float], top_token_count: int) -> tuple[dict[str, torch.Tensor], list[dict[str, Any]], torch.Tensor]:
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
    top_ids = sorted_obs[:top_token_count]
    for rank, token_id in enumerate(top_ids.tolist(), start=1):
        rows.append(
            {
                "frequency_group": "top_token",
                "rank": rank,
                "token_id": int(token_id),
                "init_count": int(freq_counts[token_id].item()),
                "init_frequency": float(freq_counts[token_id].item() / max(total, 1)),
            }
        )
    return masks, rows, top_ids


def audit_variant_seed(
    model: torch.nn.Module,
    dataset: Any,
    audit_indices: list[int],
    args: argparse.Namespace,
    device: torch.device,
    high_masks_cpu: dict[str, torch.Tensor],
    top_ids: torch.Tensor,
) -> tuple[dict[tuple[int, str], torch.Tensor], dict[int, torch.Tensor], dict[int, int]]:
    layers = [idx for idx, _, _ in base.iter_gate_modules(model)]
    group_counts = {(layer, "all_tokens"): torch.zeros(args.num_experts, dtype=torch.long) for layer in layers}
    for layer in layers:
        for label in high_masks_cpu:
            group_counts[(layer, f"high_freq_{label}")] = torch.zeros(args.num_experts, dtype=torch.long)
            group_counts[(layer, f"without_high_freq_{label}")] = torch.zeros(args.num_experts, dtype=torch.long)
    top_lookup = torch.full((args.vocab_size,), -1, dtype=torch.long)
    top_lookup[top_ids.long()] = torch.arange(top_ids.numel(), dtype=torch.long)
    top_counts = {layer: torch.zeros(top_ids.numel(), args.num_experts, dtype=torch.long) for layer in layers}
    top_token_totals = {int(t.item()): 0 for t in top_ids}

    model.eval()
    cap = base.GateCapture(model)
    high_masks_gpu = {k: v.to(device=device) for k, v in high_masks_cpu.items()}
    top_lookup_gpu = top_lookup.to(device=device)
    with torch.no_grad():
        for start in range(0, len(audit_indices), args.token_audit_batch_size):
            batch_idx = audit_indices[start : start + args.token_audit_batch_size]
            x, _ = dataset.batch(batch_idx, device)
            token_flat = x.reshape(-1)
            top_idx = top_lookup_gpu[token_flat]
            top_present = top_idx >= 0
            if top_present.any():
                present_ids, present_counts = torch.unique(token_flat[top_present].detach().cpu(), return_counts=True)
                for tid, cnt in zip(present_ids.tolist(), present_counts.tolist()):
                    if tid in top_token_totals:
                        top_token_totals[tid] += int(cnt)
            cap.clear()
            _ = model.model(input_ids=x, use_cache=False)
            for layer_idx, _mlp, _gate in base.iter_gate_modules(model):
                _h, logits = cap.records[layer_idx]
                routes = torch.argmax(logits.float(), dim=-1)
                group_counts[(layer_idx, "all_tokens")] += torch.bincount(routes.detach().cpu(), minlength=args.num_experts).long()
                for label, mask_vocab in high_masks_gpu.items():
                    high = mask_vocab[token_flat]
                    if high.any():
                        group_counts[(layer_idx, f"high_freq_{label}")] += torch.bincount(routes[high].detach().cpu(), minlength=args.num_experts).long()
                    low = ~high
                    if low.any():
                        group_counts[(layer_idx, f"without_high_freq_{label}")] += torch.bincount(routes[low].detach().cpu(), minlength=args.num_experts).long()
                if top_present.any():
                    comp = top_idx[top_present] * args.num_experts + routes[top_present]
                    binc = torch.bincount(comp.detach().cpu(), minlength=top_ids.numel() * args.num_experts)
                    top_counts[layer_idx] += binc.reshape(top_ids.numel(), args.num_experts).long()
    cap.close()
    return group_counts, top_counts, top_token_totals


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", type=Path, default=EXP_DIR / "runs/common_filtered_expert_spectrum_init/a06_01_common_filtered_expert_spectrum_init_4gpu_20260614_full01")
    parser.add_argument("--output-dir", type=Path, default=EXP_DIR)
    parser.add_argument("--audit-num-sequences", type=int, default=None)
    parser.add_argument("--init-num-sequences", type=int, default=None)
    parser.add_argument("--token-audit-batch-size", type=int, default=64)
    parser.add_argument("--frequency-count-batch-size", type=int, default=256)
    parser.add_argument("--top-type-fracs", type=float, nargs="+", default=[0.01, 0.05])
    parser.add_argument("--top-token-count", type=int, default=64)
    parser.add_argument("--device", default="cuda:0")
    parser.add_argument("--variants", nargs="*", default=None)
    parser.add_argument("--seeds", type=int, nargs="*", default=None)
    args = parser.parse_args()

    cli_audit_num_sequences = args.audit_num_sequences
    cli_init_num_sequences = args.init_num_sequences
    cli_variants = args.variants
    cli_seeds = args.seeds
    cli_run_dir = args.run_dir
    cli_output_dir = args.output_dir
    cli_token_audit_batch_size = args.token_audit_batch_size
    cli_frequency_count_batch_size = args.frequency_count_batch_size
    cli_top_type_fracs = args.top_type_fracs
    cli_top_token_count = args.top_token_count
    cli_device = args.device

    with (args.run_dir / "config/run_config.json").open(encoding="utf-8") as f:
        cfg = json.load(f)
    for key, value in cfg.items():
        setattr(args, key, value)
    args.run_dir = Path(cli_run_dir)
    args.output_dir = Path(cli_output_dir)
    args.audit_num_sequences = int(cli_audit_num_sequences or cfg["audit_num_sequences"])
    args.init_num_sequences = int(cli_init_num_sequences or cfg["init_num_sequences"])
    args.variants = cli_variants or cfg["variants"]
    args.seeds = cli_seeds or cfg["model_seeds"]
    args.token_audit_batch_size = cli_token_audit_batch_size
    args.frequency_count_batch_size = cli_frequency_count_batch_size
    args.top_type_fracs = cli_top_type_fracs
    args.top_token_count = cli_top_token_count
    args.device = cli_device

    device = torch.device(args.device if torch.cuda.is_available() and str(args.device).startswith("cuda") else "cpu")
    dataset = base.PackedBinDataset(Path(cfg["data_path"]))
    init_indices = list(range(args.init_num_sequences))
    audit_indices = list(range(args.init_num_sequences, args.init_num_sequences + args.audit_num_sequences))

    freq_counts = count_token_frequencies(dataset, init_indices, args.vocab_size, args.frequency_count_batch_size)
    high_masks, freq_rows, top_ids = build_freq_masks(freq_counts, args.top_type_fracs, args.top_token_count)

    group_rows: list[dict[str, Any]] = []
    top_rows: list[dict[str, Any]] = []
    for variant in args.variants:
        for seed in args.seeds:
            ckpt = args.run_dir / "checkpoints" / f"{variant}_seed{seed}_step0.pt"
            if not ckpt.exists():
                raise FileNotFoundError(ckpt)
            model = base.make_model(args.num_experts, int(seed), args, device)
            state = torch.load(ckpt, map_location=device)
            model.load_state_dict(state["model_state_dict"])
            group_counts, top_counts, top_token_totals = audit_variant_seed(
                model, dataset, audit_indices, args, device, high_masks, top_ids
            )
            for (layer, group), counts in sorted(group_counts.items()):
                row = {
                    "variant": variant,
                    "model_seed": int(seed),
                    "step": 0,
                    "layer": int(layer),
                    "token_group": group,
                }
                row.update(load_metrics_from_counts(counts))
                group_rows.append(row)
            for layer, mat in sorted(top_counts.items()):
                for idx, token_id in enumerate(top_ids.tolist()):
                    counts = mat[idx]
                    metrics = load_metrics_from_counts(counts)
                    top_rows.append(
                        {
                            "variant": variant,
                            "model_seed": int(seed),
                            "step": 0,
                            "layer": int(layer),
                            "token_id": int(token_id),
                            "init_frequency_rank": int(idx + 1),
                            "init_count": int(freq_counts[token_id].item()),
                            "audit_count": int(top_token_totals.get(int(token_id), 0)),
                            "winner_expert": int(torch.argmax(counts).item()) if counts.sum() > 0 else -1,
                            **metrics,
                        }
                    )
            del model
            if torch.cuda.is_available():
                torch.cuda.empty_cache()

    out = args.output_dir / "tables/token_frequency_routing"
    write_csv(out / "frequency_group_definition.csv", freq_rows)
    write_csv(out / "step0_frequency_group_route_summary.csv", group_rows)
    write_csv(out / "step0_top_token_route_distribution.csv", top_rows)
    with (out / "run_summary.json").open("w", encoding="utf-8") as f:
        json.dump(
            {
                "run_dir": str(args.run_dir),
                "audit_num_sequences": args.audit_num_sequences,
                "init_num_sequences": args.init_num_sequences,
                "variants": args.variants,
                "seeds": args.seeds,
                "top_type_fracs": args.top_type_fracs,
                "top_token_count": args.top_token_count,
                "group_rows": len(group_rows),
                "top_token_rows": len(top_rows),
                "definition_rows": len(freq_rows),
            },
            f,
            indent=2,
            sort_keys=True,
        )
    print(f"wrote token-frequency routing audit to {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
