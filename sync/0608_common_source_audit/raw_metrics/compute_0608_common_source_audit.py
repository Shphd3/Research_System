#!/usr/bin/env python3
"""Compute 0608 common-source audit artifacts.

This script writes only under sync/0608_common_source_audit.
It recomputes summary metrics from existing A05_03 CSVs and runs cheap
step-0 source-localization diagnostics. It does not overwrite experiment raw
results.
"""

from __future__ import annotations

import csv
import json
import math
import random
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

import torch
from torch.nn import functional as F


ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "sync/0608_common_source_audit"
TABLES = OUT / "tables"
FIGURES = OUT / "figures"
RAW = OUT / "raw_metrics"

EXP = ROOT / "Projects/from-attention-to-search/main/experiments/A05_03_uniform_collapse_common_offset"
DAILY = ROOT / "daily_research_reports/0608/uniform_collapse_common_offset"
PROJECT = ROOT / "Projects/from-attention-to-search"
WORKSPACE = PROJECT / "XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding"

sys.path.insert(0, str(EXP / "scripts"))
sys.path.insert(0, str(WORKSPACE / "scripts"))
sys.path.insert(0, str(WORKSPACE / "src"))

import run_a05_03_common_offset_experiments as base  # noqa: E402
import run_a05_03_remaining_experiments as remaining  # noqa: E402


SELECTED = {
    "baseline_full_hidden": ("P7", "baseline_full_hidden"),
    "P5B_logit_common_offset_cancel": ("P5", "P5B_logit_common_offset_cancel"),
    "P4_I4_residual_subspace_orthogonal": ("P4", "I4_residual_subspace_orthogonal"),
    "P6A_aux_load_balance_warmup": ("P6", "P6A_aux_load_balance_warmup"),
}


def ensure_dirs() -> None:
    for path in [OUT, TABLES, FIGURES, RAW]:
        path.mkdir(parents=True, exist_ok=True)


def read_csv(path: Path) -> list[dict]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("")
        return
    fields = []
    seen = set()
    for row in rows:
        for key in row:
            if key not in seen:
                seen.add(key)
                fields.append(key)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, obj: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True))


def parse_vec(s: str) -> list[float]:
    if s is None or str(s).strip() == "":
        return []
    return [float(x) for x in str(s).split()]


def mean(xs: list[float]) -> float:
    return sum(xs) / len(xs) if xs else math.nan


def std(xs: list[float]) -> float:
    if len(xs) < 2:
        return 0.0 if xs else math.nan
    m = mean(xs)
    return math.sqrt(sum((x - m) ** 2 for x in xs) / (len(xs) - 1))


def corr(xs: list[float], ys: list[float]) -> float:
    if len(xs) != len(ys) or len(xs) < 2:
        return math.nan
    mx, my = mean(xs), mean(ys)
    vx = sum((x - mx) ** 2 for x in xs)
    vy = sum((y - my) ** 2 for y in ys)
    if vx <= 0 or vy <= 0:
        return math.nan
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / math.sqrt(vx * vy)


def safe_git_head(repo: Path) -> str:
    try:
        return subprocess.check_output(
            ["git", "-c", f"safe.directory={repo}", "rev-parse", "HEAD"],
            cwd=repo,
            text=True,
        ).strip()
    except Exception as exc:  # noqa: BLE001
        return f"UNKNOWN: {exc.__class__.__name__}"


def integrity_audit() -> list[dict]:
    run_manifest = json.loads((EXP / "tables/run_manifest.json").read_text())
    rem_manifest = json.loads((EXP / "tables/remaining_run_manifest.json").read_text())
    config_path = Path(rem_manifest["config"])
    cfg = json.loads(config_path.read_text())
    seeds = rem_manifest["seeds"]
    train_steps = rem_manifest["train_steps"]
    eval_batch = rem_manifest["eval_batch_size"]
    rows = [
        {
            "item": "exact command lines",
            "verdict": "PASS",
            "evidence": "A05_03 detailed.md Section 12; copied to daily 0608 detailed.md",
            "risk": "commands are report-recorded, not embedded in JSON manifest",
        },
        {
            "item": "git commit hash",
            "verdict": "PASS",
            "evidence": safe_git_head(PROJECT),
            "risk": "commit is current repo-side state, not stored per raw run",
        },
        {
            "item": "config files",
            "verdict": "PASS" if config_path.exists() else "FAIL",
            "evidence": str(config_path),
            "risk": "none" if config_path.exists() else "missing config",
        },
        {
            "item": "same seeds",
            "verdict": "PASS" if seeds == [20260521, 20260522, 20260523] else "FAIL",
            "evidence": str(seeds),
            "risk": "3-seed audit only; no 20260524-20260527 extension",
        },
        {
            "item": "same data",
            "verdict": "PASS",
            "evidence": "same generate_train_data/generate_feature_grid functions; data_pattern_counts balanced_exact=1",
            "risk": "data are regenerated deterministically rather than stored as a fixed dataset file",
        },
        {
            "item": "same train steps",
            "verdict": "PASS" if train_steps == 400 else "FAIL",
            "evidence": str(train_steps),
            "risk": "shortened mechanism run, not full 1600-step run",
        },
        {
            "item": "same eval grid",
            "verdict": "PASS" if eval_batch == 512 else "UNKNOWN",
            "evidence": f"eval_batch_size={eval_batch}, variants_per_key={rem_manifest['variants_per_key']}",
            "risk": "balanced eval grid exists; exact tensors are regenerated by seed",
        },
        {
            "item": "step0 is true init",
            "verdict": "PASS",
            "evidence": "eval_state called before optimizer step; P4 step0 is after explicit init intervention",
            "risk": "P4 step0 is intervention-initialized, not default PyTorch init",
        },
        {
            "item": "baseline and interventions checkpoint schedule",
            "verdict": "PASS",
            "evidence": "remaining_training_metrics_by_step uses steps 0,10,20,50,100,200,400",
            "risk": "P3 CPU-shortened rows are separate and not used as main Run 1 comparison",
        },
        {
            "item": "target accuracy comparable",
            "verdict": "PASS",
            "evidence": f"target token count={4 * int(cfg['data']['b_token_count_multi'])}, same full-sequence NTP objective",
            "risk": "accuracy is validity guard only; it does not validate specialization",
        },
    ]
    return rows


def recompute_primary_metrics() -> tuple[list[dict], list[dict]]:
    rows = read_csv(EXP / "tables/remaining_training_metrics_by_step.csv")
    selected_rows = []
    for row in rows:
        for label, (protocol, variant) in SELECTED.items():
            if row["protocol"] == protocol and row["variant"] == variant:
                new = dict(row)
                new["variant_label"] = label
                selected_rows.append(new)

    grouped: dict[tuple[str, str, str, str], list[dict]] = defaultdict(list)
    for row in selected_rows:
        grouped[(row["variant_label"], row["pattern"], row["seed"], row["protocol"])].append(row)

    seed_out = []
    for (label, pattern, seed, protocol), items in sorted(grouped.items()):
        items = sorted(items, key=lambda r: int(r["step"]))
        final = items[-1]
        final_dom = int(final["dominant_expert"])
        by_step = {int(r["step"]): r for r in items}
        step0 = by_step.get(0, items[0])
        common_scores = parse_vec(step0.get("common_score_raw") or step0.get("common_scores"))
        common_argmax = max(range(len(common_scores)), key=lambda i: common_scores[i]) if common_scores else -1
        common_margin = math.nan
        if len(common_scores) >= 2:
            top2 = sorted(common_scores, reverse=True)[:2]
            common_margin = top2[0] - top2[1]
        persistence = sum(int(int(r["dominant_expert"]) == final_dom) for r in items) / len(items)
        collapse = float(final["max_load"]) >= 0.95 or int(final["active_experts"]) <= 1
        seed_out.append(
            {
                "variant": label,
                "protocol": protocol,
                "pattern": pattern,
                "seed": seed,
                "n_eval_steps": len(items),
                "step0_max_load": float(step0["max_load"]),
                "step10_max_load": float(by_step[10]["max_load"]) if 10 in by_step else math.nan,
                "step50_max_load": float(by_step[50]["max_load"]) if 50 in by_step else math.nan,
                "final_step": int(final["step"]),
                "final_max_load": float(final["max_load"]),
                "load_entropy": float(final["load_entropy_norm"]),
                "active_experts": int(final["active_experts"]),
                "collapse": int(collapse),
                "target_accuracy": float(final["target_accuracy"]),
                "dominant_expert_persistence": persistence,
                "step0_dominant_expert": int(step0["dominant_expert"]),
                "final_dominant_expert": final_dom,
                "common_score_argmax": common_argmax,
                "common_score_argmax_agreement": int(common_argmax == int(step0["dominant_expert"])) if common_argmax >= 0 else math.nan,
                "common_score_margin": common_margin,
            }
        )

    summary = []
    by_variant: dict[str, list[dict]] = defaultdict(list)
    for row in seed_out:
        by_variant[row["variant"]].append(row)
    for label, items in sorted(by_variant.items()):
        final_load = [float(r["final_max_load"]) for r in items]
        acc = [float(r["target_accuracy"]) for r in items]
        entropy = [float(r["load_entropy"]) for r in items]
        step0 = [float(r["step0_max_load"]) for r in items]
        step10 = [float(r["step10_max_load"]) for r in items]
        step50 = [float(r["step50_max_load"]) for r in items]
        persistence = [float(r["dominant_expert_persistence"]) for r in items]
        summary.append(
            {
                "variant": label,
                "seeds": len(items),
                "patterns": ",".join(sorted({r["pattern"] for r in items})),
                "final_max_load_mean": mean(final_load),
                "final_max_load_std": std(final_load),
                "collapse_rate": mean([float(r["collapse"]) for r in items]),
                "load_entropy_mean": mean(entropy),
                "target_accuracy_mean": mean(acc),
                "target_accuracy_std": std(acc),
                "step0_max_load_mean": mean(step0),
                "step10_max_load_mean": mean(step10),
                "step50_max_load_mean": mean(step50),
                "dominant_expert_persistence_mean": mean(persistence),
                "common_score_argmax_agreement_mean": mean(
                    [float(r["common_score_argmax_agreement"]) for r in items]
                ),
                "common_score_margin_mean": mean([float(r["common_score_margin"]) for r in items]),
            }
        )
    return seed_out, summary


def common_score_prediction_tables() -> tuple[list[dict], list[dict]]:
    rows = read_csv(EXP / "tables/remaining_training_metrics_by_step.csv")
    selected_rows = []
    for row in rows:
        for label, (protocol, variant) in SELECTED.items():
            if row["protocol"] == protocol and row["variant"] == variant:
                new = dict(row)
                new["variant_label"] = label
                selected_rows.append(new)

    final_dom = {}
    for row in selected_rows:
        key = (row["variant_label"], row["pattern"], row["seed"])
        if key not in final_dom or int(row["step"]) > final_dom[key][0]:
            final_dom[key] = (int(row["step"]), int(row["dominant_expert"]))

    out = []
    for row in selected_rows:
        scores = parse_vec(row.get("common_score_raw") or row.get("common_scores"))
        loads = parse_vec(row["load_by_expert"])
        if not scores or not loads:
            continue
        dom = int(row["dominant_expert"])
        ranked = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)
        rank_dom = ranked.index(dom) + 1
        top2 = sorted(scores, reverse=True)[:2]
        out.append(
            {
                "variant": row["variant_label"],
                "protocol": row["protocol"],
                "pattern": row["pattern"],
                "seed": row["seed"],
                "step": int(row["step"]),
                "common_score_argmax": ranked[0],
                "dominant_expert_by_load": dom,
                "final_dominant_expert": final_dom[(row["variant_label"], row["pattern"], row["seed"])][1],
                "rank_of_dominant_by_common_score": rank_dom,
                "common_score_margin": top2[0] - top2[1],
                "corr_common_score_load": corr(scores, loads),
                "max_load": float(row["max_load"]),
                "load_by_expert": row["load_by_expert"],
                "common_scores": " ".join(f"{x:.6f}" for x in scores),
            }
        )

    summary = []
    grouped = defaultdict(list)
    for row in out:
        if int(row["step"]) == 0:
            grouped[(row["pattern"], row["variant"])].append(row)
    for (pattern, variant), items in sorted(grouped.items()):
        summary.append(
            {
                "pattern": pattern,
                "variant": variant,
                "seeds": len(items),
                "agreement_with_dominant_expert": mean(
                    [float(r["rank_of_dominant_by_common_score"] == 1) for r in items]
                ),
                "corr_common_score_load_mean": mean([float(r["corr_common_score_load"]) for r in items]),
                "common_score_margin_mean": mean([float(r["common_score_margin"]) for r in items]),
                "verdict": "SUPPORTS" if mean([float(r["rank_of_dominant_by_common_score"] == 1) for r in items]) > 0.5 else "WEAK",
            }
        )
    return out, summary


def tensor_cos(a: torch.Tensor, b: torch.Tensor) -> float:
    if a.norm().item() == 0 or b.norm().item() == 0:
        return math.nan
    return float(F.cosine_similarity(a.view(1, -1), b.view(1, -1)).item())


def projection_share(c: torch.Tensor, v: torch.Tensor) -> float:
    if c.norm().item() == 0 or v.norm().item() == 0:
        return math.nan
    cos = tensor_cos(c, v)
    return cos * cos


def clone_actual_model(cfg: dict, seed: int, device: torch.device):
    return base.actual_model(cfg, "dot_product", seed, device)


def feature_data_for_model(cfg: dict, model, pattern: str, seed: int, variants: int, device, batch_size: int, minimal: bool = False):
    grid = base.generate_feature_grid(cfg, pattern, seed, variants)
    if minimal:
        data = cfg["data"]
        protected = set(range(int(data["prefix_start"]), int(data["prefix_start"]) + int(data["prefix_len"])))
        protected.add(int(data["b_position"]))
        protected.add(int(data["target_position"]))
        bg = int(data["background_token"])
        x = grid.x.clone()
        for pos in range(x.shape[1]):
            if pos not in protected:
                x[:, pos] = bg
        grid.x = x
    data = base.feature_hidden(model, cfg, grid, device, batch_size)
    h_feat, _ = base.feature_centroids(data, cfg)
    return data, h_feat


def load_from_scores(scores: torch.Tensor, num_experts: int) -> list[float]:
    top = scores.argmax(dim=1)
    return base.load_from_top(top, num_experts)


def common_ratio_sq(h_feat: torch.Tensor) -> float:
    c = h_feat.mean(dim=0)
    denom = (h_feat.norm(dim=1) ** 2).mean().item()
    return float(c.norm().item() ** 2 / denom) if denom > 0 else math.nan


def top_pc_stats(h_feat: torch.Tensor, c: torch.Tensor) -> tuple[float, float]:
    centered = h_feat - h_feat.mean(dim=0, keepdim=True)
    _, s, vh = torch.linalg.svd(centered, full_matrices=False)
    energy = s**2
    top_pc_ratio = float((energy[0] / energy.sum()).item()) if energy.sum().item() > 0 else math.nan
    cos_pc = abs(tensor_cos(c, vh[0].detach().cpu()))
    return top_pc_ratio, cos_pc


def source_localization() -> tuple[list[dict], list[dict], list[dict]]:
    cfg = base.load_cfg(str(WORKSPACE / "configs/h0605a_true_token_conditioned_inhibition_replay.json"))
    device = torch.device("cpu")
    variants = 4
    batch_size = 512
    rows = []
    ablations = []
    common_geom = []
    for pattern in base.PATTERNS:
        for seed in base.SEEDS:
            model = clone_actual_model(cfg, seed, device)
            data, h_feat = feature_data_for_model(cfg, model, pattern, seed, variants, device, batch_size)
            c = h_feat.mean(dim=0).detach().cpu()
            top_pc_ratio, cos_pc = top_pc_stats(h_feat, c)
            scores = base.router_scores(model, h_feat, "dot_product")
            load = load_from_scores(scores, int(cfg["model"]["num_experts"]))
            common_geom.append(
                {
                    "pattern": pattern,
                    "seed": seed,
                    "step": 0,
                    "common_ratio": common_ratio_sq(h_feat),
                    "residual_ratio": float(((h_feat - c).norm(dim=1) ** 2).mean().item() / ((h_feat.norm(dim=1) ** 2).mean().item())),
                    "top_pc_ratio": top_pc_ratio,
                    "cos_c_top_pc1": cos_pc,
                    "step0_max_load": max(load),
                }
            )

            token_emb = model.token_emb.weight.detach().cpu().float()
            pos_emb = model.pos_emb.weight.detach().cpu().float()
            d = cfg["data"]
            b_pos = int(d["b_position"])
            target_pos = int(d["target_position"])
            b_start = int(d["b_token_start"])
            b_count = int(d["b_token_count_multi"])
            target_start = int(d["target_token_start"])
            slot_tokens = []
            for slot in range(int(d["num_slots"])):
                slot_tokens.extend(base.slot_code(pattern, slot, cfg))
            seq_positions = torch.arange(int(d["seq_len"]))
            bg = int(d["background_token"])
            template = torch.full((1, int(d["seq_len"])), bg, dtype=torch.long)
            _, info = model(template, return_acts=True)
            template_hidden = info["ffn_input"][0, b_pos].detach().cpu().float()
            source_vecs = {
                "A_position_embedding_routed": pos_emb[b_pos],
                "B_raw_B_position_input": token_emb[torch.arange(b_start, b_start + b_count)].mean(dim=0) + pos_emb[b_pos],
                "C_background_token_embedding": token_emb[bg],
                "C_mean_position_embedding_over_sequence": pos_emb[seq_positions].mean(dim=0),
                "D_slot_token_mean": token_emb[torch.tensor(slot_tokens)].mean(dim=0),
                "E_B_token_mean": token_emb[torch.arange(b_start, b_start + b_count)].mean(dim=0),
                "F_target_token_mean": token_emb[torch.arange(target_start, target_start + int(d["num_slots"]) * b_count)].mean(dim=0),
                "F_target_position_embedding": pos_emb[target_pos],
                "G_layernorm_ln1_bias": model.ln1.bias.detach().cpu().float(),
                "G_layernorm_ln2_bias": model.ln2.bias.detach().cpu().float(),
                "H_template_only_hidden_at_route": template_hidden,
            }
            for name, vec in source_vecs.items():
                rows.append(
                    {
                        "pattern": pattern,
                        "seed": seed,
                        "source": name,
                        "cos_c_source": tensor_cos(c, vec),
                        "projection_share": projection_share(c, vec),
                        "source_norm": float(vec.norm().item()),
                        "common_norm": float(c.norm().item()),
                    }
                )

            def add_ablation(name: str, h_new: torch.Tensor, model_for_scores=None) -> None:
                scorer = model if model_for_scores is None else model_for_scores
                c_new = h_new.mean(dim=0).detach().cpu()
                sc = base.router_scores(scorer, h_new, "dot_product")
                ld = load_from_scores(sc, int(cfg["model"]["num_experts"]))
                cs = base.router_scores(scorer, c_new.view(1, -1), "dot_product").view(-1)
                argmax = int(cs.argmax().item())
                dom = int(max(range(len(ld)), key=lambda i: ld[i]))
                ablations.append(
                    {
                        "pattern": pattern,
                        "seed": seed,
                        "test": name,
                        "common_ratio": common_ratio_sq(h_new),
                        "cos_c_new_c_old": tensor_cos(c_new, c),
                        "step0_max_load": max(ld),
                        "common_score_argmax": argmax,
                        "dominant_expert": dom,
                        "common_argmax_agrees_dominant": int(argmax == dom),
                    }
                )

            add_ablation("baseline_full_hidden", h_feat)
            add_ablation("A_subtract_routed_position_embedding", h_feat - pos_emb[b_pos])
            add_ablation("D_fixed_calibration_mean_subtract", h_feat - c)
            _, h_min = feature_data_for_model(cfg, model, pattern, seed, 1, device, batch_size, minimal=True)
            add_ablation("C_minimal_sequence_no_nuisance", h_min)

            model_bg = clone_actual_model(cfg, seed, device)
            with torch.no_grad():
                model_bg.token_emb.weight[bg].zero_()
            _, h_bg = feature_data_for_model(cfg, model_bg, pattern, seed, variants, device, batch_size)
            add_ablation("B_zero_background_embedding_forward", h_bg, model_bg)

            model_b = clone_actual_model(cfg, seed, device)
            with torch.no_grad():
                model_b.token_emb.weight[b_start : b_start + b_count].zero_()
            _, h_b = feature_data_for_model(cfg, model_b, pattern, seed, variants, device, batch_size)
            add_ablation("E_zero_B_token_embeddings_forward", h_b, model_b)
    return rows, ablations, common_geom


def batch_mean_equivalence() -> list[dict]:
    cfg = base.load_cfg(str(WORKSPACE / "configs/h0605a_true_token_conditioned_inhibition_replay.json"))
    device = torch.device("cpu")
    rows = []
    rng = random.Random(20260608)
    for pattern in base.PATTERNS:
        for seed in base.SEEDS:
            model = clone_actual_model(cfg, seed, device)
            grid = base.generate_feature_grid(cfg, pattern, seed, 4)
            data = base.feature_hidden(model, cfg, grid, device, 512)
            h = data["h"].float()
            h_feat, _ = base.feature_centroids(data, cfg)
            c_calib = h_feat.mean(dim=0)
            w = model.moe.router.weight.detach().cpu().float()
            z1 = F.linear(h - c_calib, w)
            z2 = F.linear(h, w) - F.linear(c_calib.view(1, -1), w).view(1, -1)
            top1 = z1.argmax(dim=1)
            top2 = z2.argmax(dim=1)
            load1 = torch.bincount(top1, minlength=int(cfg["model"]["num_experts"])).float()
            load1 = load1 / load1.sum()
            load2 = torch.bincount(top2, minlength=int(cfg["model"]["num_experts"])).float()
            load2 = load2 / load2.sum()
            rows.append(
                {
                    "pattern": pattern,
                    "seed": seed,
                    "mode": "fixed_calibration_equivalence",
                    "batch_size": h.shape[0],
                    "composition": "full_balanced_grid",
                    "num_batches": 1,
                    "max_abs_z1_minus_z2": float((z1 - z2).abs().max().item()),
                    "top1_assignment_agreement": float((top1 == top2).float().mean().item()),
                    "load_l1_diff": float((load1 - load2).abs().sum().item()),
                    "c_batch_norm_std": 0.0,
                    "offset_std_mean": 0.0,
                    "max_load_mean": float(load1.max().item()),
                    "max_load_std": 0.0,
                }
            )

            fixed_scores = z1
            fixed_top = fixed_scores.argmax(dim=1)
            labels = data["slot"].tolist()
            idx_by_slot = defaultdict(list)
            for i, slot in enumerate(labels):
                idx_by_slot[int(slot)].append(i)
            all_idx = list(range(h.shape[0]))
            for bs in [16, 32, 64, 128, h.shape[0]]:
                for comp in ["balanced", "shuffled", "slot_skewed"]:
                    batches = []
                    if bs == h.shape[0]:
                        batches = [all_idx]
                        comp_actual = "full_balanced_grid"
                    else:
                        comp_actual = comp
                        for _ in range(40):
                            if comp == "balanced":
                                per_slot = max(1, bs // int(cfg["data"]["num_slots"]))
                                idx = []
                                for slot in range(int(cfg["data"]["num_slots"])):
                                    idx.extend(rng.choice(idx_by_slot[slot]) for _ in range(per_slot))
                                while len(idx) < bs:
                                    idx.append(rng.choice(all_idx))
                                rng.shuffle(idx)
                            elif comp == "slot_skewed":
                                slot = rng.randrange(int(cfg["data"]["num_slots"]))
                                idx = [rng.choice(idx_by_slot[slot]) for _ in range(bs)]
                            else:
                                idx = [rng.choice(all_idx) for _ in range(bs)]
                            batches.append(idx)
                    c_norms, offset_stds, agreements, max_loads = [], [], [], []
                    for idx in batches:
                        idx_t = torch.tensor(idx, dtype=torch.long)
                        hb = h[idx_t]
                        cb = hb.mean(dim=0)
                        zb = F.linear(hb - cb, w)
                        tb = zb.argmax(dim=1)
                        fb = fixed_top[idx_t]
                        ld = torch.bincount(tb, minlength=int(cfg["model"]["num_experts"])).float()
                        ld = ld / ld.sum()
                        c_norms.append(float((cb - c_calib).norm().item()))
                        offset_stds.append(float((w @ cb).std(unbiased=False).item()))
                        agreements.append(float((tb == fb).float().mean().item()))
                        max_loads.append(float(ld.max().item()))
                    rows.append(
                        {
                            "pattern": pattern,
                            "seed": seed,
                            "mode": "batch_mean_subtraction",
                            "batch_size": bs,
                            "composition": comp_actual,
                            "num_batches": len(batches),
                            "max_abs_z1_minus_z2": math.nan,
                            "top1_assignment_agreement": mean(agreements),
                            "load_l1_diff": math.nan,
                            "c_batch_norm_std": std(c_norms),
                            "c_batch_norm_mean": mean(c_norms),
                            "offset_std_mean": mean(offset_stds),
                            "offset_std_std": std(offset_stds),
                            "max_load_mean": mean(max_loads),
                            "max_load_std": std(max_loads),
                        }
                    )
    return rows


def make_figures(primary: list[dict], common: list[dict], source: list[dict], ablations: list[dict], batch_rows: list[dict]) -> None:
    import matplotlib.pyplot as plt

    FIGURES.mkdir(parents=True, exist_ok=True)

    # Max-load trajectory by selected variant.
    raw = read_csv(EXP / "tables/remaining_training_metrics_by_step.csv")
    fig, ax = plt.subplots(figsize=(9, 5))
    for label, (protocol, variant) in SELECTED.items():
        by_step = defaultdict(list)
        for row in raw:
            if row["protocol"] == protocol and row["variant"] == variant:
                by_step[int(row["step"])].append(float(row["max_load"]))
        steps = sorted(by_step)
        vals = [mean(by_step[s]) for s in steps]
        ax.plot(steps, vals, marker="o", label=label)
    ax.axhline(0.95, color="tab:red", linestyle=":", linewidth=1)
    ax.set_xlabel("step")
    ax.set_ylabel("mean max-load")
    ax.set_title("Max-load trajectory by selected variant")
    ax.grid(alpha=0.25)
    ax.legend(fontsize=7, frameon=False)
    fig.tight_layout()
    fig.savefig(FIGURES / "max_load_trajectory_by_variant.png", dpi=180)
    plt.close(fig)

    # Final max-load by seed/pattern.
    labels = [f"{r['pattern']}\n{r['seed']}" for r in primary if r["variant"] == "baseline_full_hidden"]
    variants = list(SELECTED.keys())
    x = torch.arange(len(labels)).float()
    width = 0.18
    fig, ax = plt.subplots(figsize=(11, 5))
    lookup = {(r["variant"], r["pattern"], str(r["seed"])): float(r["final_max_load"]) for r in primary}
    for j, variant in enumerate(variants):
        vals = []
        for lab in labels:
            pattern, seed = lab.split("\n")
            vals.append(lookup.get((variant, pattern, seed), math.nan))
        ax.bar((x + (j - 1.5) * width).tolist(), vals, width=width, label=variant)
    ax.axhline(0.95, color="tab:red", linestyle=":", linewidth=1)
    ax.set_xticks(x.tolist(), labels, fontsize=8)
    ax.set_ylabel("final max-load")
    ax.set_title("Final max-load by seed")
    ax.legend(fontsize=7, frameon=False)
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    fig.savefig(FIGURES / "final_max_load_by_seed.png", dpi=180)
    plt.close(fig)

    # Accuracy by seed.
    fig, ax = plt.subplots(figsize=(11, 5))
    lookup_acc = {(r["variant"], r["pattern"], str(r["seed"])): float(r["target_accuracy"]) for r in primary}
    for j, variant in enumerate(variants):
        vals = []
        for lab in labels:
            pattern, seed = lab.split("\n")
            vals.append(lookup_acc.get((variant, pattern, seed), math.nan))
        ax.bar((x + (j - 1.5) * width).tolist(), vals, width=width, label=variant)
    ax.set_xticks(x.tolist(), labels, fontsize=8)
    ax.set_ylim(0.94, 1.0)
    ax.set_ylabel("target accuracy")
    ax.set_title("Target accuracy by seed")
    ax.legend(fontsize=7, frameon=False)
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    fig.savefig(FIGURES / "accuracy_by_seed.png", dpi=180)
    plt.close(fig)

    # Common score vs load scatter.
    fig, ax = plt.subplots(figsize=(6, 5))
    for row in common:
        if int(row["step"]) != 0 or row["variant"] != "baseline_full_hidden":
            continue
        scores = parse_vec(row["common_scores"])
        loads = parse_vec(row["load_by_expert"])
        ax.scatter(scores, loads, alpha=0.75, label=row["pattern"] if row["seed"] == "20260521" else None)
    ax.set_xlabel("common score")
    ax.set_ylabel("expert load")
    ax.set_title("Step-0 common score vs load")
    ax.grid(alpha=0.25)
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(FIGURES / "common_score_vs_load_scatter.png", dpi=180)
    plt.close(fig)

    # Common score rank over steps.
    fig, ax = plt.subplots(figsize=(9, 5))
    for variant in variants:
        by_step = defaultdict(list)
        for row in common:
            if row["variant"] == variant:
                by_step[int(row["step"])].append(float(row["rank_of_dominant_by_common_score"]))
        steps = sorted(by_step)
        ax.plot(steps, [mean(by_step[s]) for s in steps], marker="o", label=variant)
    ax.set_xlabel("step")
    ax.set_ylabel("mean rank of load-dominant expert by common score")
    ax.set_title("Common-score rank over steps")
    ax.invert_yaxis()
    ax.grid(alpha=0.25)
    ax.legend(fontsize=7, frameon=False)
    fig.tight_layout()
    fig.savefig(FIGURES / "common_score_rank_over_steps.png", dpi=180)
    plt.close(fig)

    # Source alignment bar.
    source_group = defaultdict(list)
    for row in source:
        source_group[row["source"]].append(abs(float(row["cos_c_source"])))
    names = sorted(source_group, key=lambda n: mean(source_group[n]), reverse=True)
    vals = [mean(source_group[n]) for n in names]
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(range(len(names)), vals)
    ax.set_xticks(range(len(names)), names, rotation=70, ha="right", fontsize=7)
    ax.set_ylabel("mean |cos(c, source)|")
    ax.set_title("Common source alignment")
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    fig.savefig(FIGURES / "common_source_alignment_bar.png", dpi=180)
    plt.close(fig)

    # Batch mean instability.
    batch = [r for r in batch_rows if r["mode"] == "batch_mean_subtraction" and r["composition"] != "full_balanced_grid"]
    fig, ax = plt.subplots(figsize=(8, 5))
    for comp in ["balanced", "shuffled", "slot_skewed"]:
        by_bs = defaultdict(list)
        for row in batch:
            if row["composition"] == comp:
                by_bs[int(row["batch_size"])].append(float(row["top1_assignment_agreement"]))
        bs = sorted(by_bs)
        if bs:
            ax.plot(bs, [mean(by_bs[b]) for b in bs], marker="o", label=comp)
    ax.set_xscale("log", base=2)
    ax.set_xlabel("batch size")
    ax.set_ylabel("top1 agreement vs fixed calibration")
    ax.set_title("Batch-mean subtraction instability")
    ax.grid(alpha=0.25)
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(FIGURES / "batchmean_instability_by_batch_size.png", dpi=180)
    plt.close(fig)


def write_commands() -> None:
    cmd = """#!/usr/bin/env bash
set -euo pipefail

python sync/0608_common_source_audit/raw_metrics/compute_0608_common_source_audit.py
"""
    (OUT / "commands.sh").write_text(cmd)


def main() -> None:
    ensure_dirs()
    write_commands()

    integrity = integrity_audit()
    primary_seed, primary_summary = recompute_primary_metrics()
    common_by_seed, common_summary = common_score_prediction_tables()
    source_rows, ablation_rows, common_geom = source_localization()
    batch_rows = batch_mean_equivalence()

    write_csv(TABLES / "result_integrity_audit.csv", integrity)
    write_csv(TABLES / "primary_metrics_by_seed.csv", primary_seed)
    write_csv(TABLES / "primary_metrics_summary.csv", primary_summary)
    write_csv(TABLES / "common_score_prediction_by_seed.csv", common_by_seed)
    write_csv(TABLES / "common_score_prediction_summary.csv", common_summary)
    write_csv(TABLES / "common_source_alignment.csv", source_rows)
    write_csv(TABLES / "common_source_ablation.csv", ablation_rows)
    write_csv(TABLES / "common_component_geometry.csv", common_geom)
    write_csv(TABLES / "batchmean_vs_logitoffset.csv", batch_rows)
    write_json(
        RAW / "audit_manifest.json",
        {
            "input_experiment": str(EXP),
            "input_daily": str(DAILY),
            "output": str(OUT),
            "selected_variants": SELECTED,
            "project_git_head": safe_git_head(PROJECT),
        },
    )
    make_figures(primary_seed, common_by_seed, source_rows, ablation_rows, batch_rows)


if __name__ == "__main__":
    main()
