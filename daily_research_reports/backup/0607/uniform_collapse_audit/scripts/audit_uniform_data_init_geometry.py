#!/usr/bin/env python3
"""Code/data/init audit for H0605a uniform feature collapse."""

from __future__ import annotations

import csv
import hashlib
import json
import math
import random
import sys
from collections import Counter, defaultdict
from pathlib import Path

import torch
from torch.nn import functional as F


RESEARCH_ROOT = Path(__file__).resolve().parents[4]
WORKSPACE = (
    RESEARCH_ROOT
    / "Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding"
)
OUT_DIR = RESEARCH_ROOT / "daily_research_reports/0607/uniform_collapse_audit"
TABLE_DIR = OUT_DIR / "tables"
FIG_DIR = OUT_DIR / "figures"

sys.path.insert(0, str(WORKSPACE / "scripts"))
sys.path.insert(0, str(WORKSPACE / "src"))

import run_h0605a_true_token_conditioned_inhibition_replay as runner  # noqa: E402


CONDITIONS = ["R0-dot", "R1-dot", "R0-cos", "R1-cos", "S0-dot", "S1-dot", "S0-cos", "S1-cos"]
FOCUS_CONDITIONS = ["R0-dot", "R1-dot", "R0-cos", "R1-cos", "S1-cos"]
SEEDS = [20260521, 20260522, 20260523]
MODE = "multi_b_primary"


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("")
        return
    fieldnames = list(rows[0].keys())
    seen = set(fieldnames)
    for row in rows[1:]:
        for key in row:
            if key not in seen:
                fieldnames.append(key)
                seen.add(key)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, obj: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True))


def load_cfg() -> dict:
    return json.loads((WORKSPACE / "configs/h0605a_true_token_conditioned_inhibition_replay.json").read_text())


def sha_tensor(t: torch.Tensor) -> str:
    arr = t.detach().cpu().contiguous().numpy().tobytes()
    return hashlib.sha256(arr).hexdigest()[:16]


def entropy_from_counts(vals: list[int]) -> float:
    total = float(sum(vals))
    if total <= 0:
        return math.nan
    ent = 0.0
    for v in vals:
        if v > 0:
            p = v / total
            ent -= p * math.log(p)
    return ent


def norm_entropy(vals: list[int]) -> float:
    if len(vals) <= 1:
        return 1.0
    return entropy_from_counts(vals) / math.log(len(vals))


def count_summary(counter: Counter, expected_keys: list, name: str) -> dict:
    counts = [int(counter.get(k, 0)) for k in expected_keys]
    total = sum(counts)
    expected = total / max(1, len(expected_keys))
    max_abs = max((abs(c - expected) for c in counts), default=0.0)
    max_rel = max_abs / expected if expected else math.nan
    chi2 = sum(((c - expected) ** 2) / expected for c in counts) if expected else math.nan
    return {
        f"{name}_num_keys": len(expected_keys),
        f"{name}_total": total,
        f"{name}_expected": expected,
        f"{name}_min": min(counts) if counts else 0,
        f"{name}_max": max(counts) if counts else 0,
        f"{name}_min_max_ratio": (min(counts) / max(counts)) if counts and max(counts) else math.nan,
        f"{name}_max_abs_dev": max_abs,
        f"{name}_max_rel_dev": max_rel,
        f"{name}_chi2": chi2,
        f"{name}_entropy_norm": norm_entropy(counts),
    }


def actual_model_for_condition(cfg: dict, condition: str, seed: int, device: torch.device):
    """Match train_condition_seed semantics: an audit model is created before the real model."""
    random.seed(seed)
    torch.manual_seed(seed + 1009)
    audit_model = runner.make_condition_model(condition, cfg, device)
    del audit_model
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    model = runner.make_condition_model(condition, cfg, device)
    cond = runner.parse_true_token_condition(condition)
    init_meta = {"router_init_type": "pytorch_default_random"}
    if cond.router_init:
        meta = runner.init_router_from_slot_centroids(model, cfg, condition, MODE, seed, device)
        init_meta.update(meta)
        init_meta["router_init_type"] = "slot_centroid_overwrite"
    model.eval()
    return model, init_meta


def audit_data(cfg: dict) -> tuple[list[dict], list[dict], list[dict]]:
    rows = []
    first_rows = []
    batch_rows = []
    data_cfg = cfg["data"]
    num_slots = int(data_cfg["num_slots"])
    b_count = int(data_cfg["b_token_count_multi"])
    train_samples = int(data_cfg["train_samples_per_slot"])
    batch_size = int(cfg["training"]["batch_size"])
    steps = int(cfg["training"]["steps"])

    for condition in ["R0-dot", "S1-cos"]:
        for seed in SEEDS:
            train = runner.generate_slot_data(cfg, condition, MODE, "train", train_samples, seed)
            slots = train.slot.tolist()
            bs = train.b_idx.tolist()
            targets = train.target.tolist()
            slot_counter = Counter(slots)
            b_counter = Counter(bs)
            pair_counter = Counter(zip(slots, bs))
            target_counter = Counter(targets)
            order_slot_same = sum(1 for a, b in zip(slots, slots[1:]) if a == b) / max(1, len(slots) - 1)
            order_b_same = sum(1 for a, b in zip(bs, bs[1:]) if a == b) / max(1, len(bs) - 1)
            row = {
                "condition": condition,
                "seed": seed,
                "split": "train_fixed_dataset",
                "num_rows": int(train.x.shape[0]),
                "x_hash": sha_tensor(train.x[: min(4096, train.x.shape[0])]),
                "first100_hash": sha_tensor(train.x[:100]),
                "adjacent_slot_equal_fraction": order_slot_same,
                "adjacent_b_equal_fraction": order_b_same,
            }
            row.update(count_summary(slot_counter, list(range(num_slots)), "slot"))
            row.update(count_summary(b_counter, list(range(b_count)), "b"))
            row.update(count_summary(pair_counter, [(s, b) for s in range(num_slots) for b in range(b_count)], "slot_b"))
            row.update(count_summary(target_counter, [runner.target_token(s, b, cfg) for s in range(num_slots) for b in range(b_count)], "target"))
            rows.append(row)
            for idx in range(min(100, train.x.shape[0])):
                first_rows.append(
                    {
                        "condition": condition,
                        "seed": seed,
                        "row_idx": idx,
                        "slot": int(train.slot[idx].item()),
                        "b_idx": int(train.b_idx[idx].item()),
                        "target": int(train.target[idx].item()),
                        "tokens": " ".join(str(v) for v in train.x[idx].tolist()),
                    }
                )

            rng = random.Random(seed + 17)
            indices = list(range(train.x.shape[0]))
            sampled_slots = []
            sampled_bs = []
            for step in range(1, steps + 1):
                batch_idx = [indices[rng.randrange(len(indices))] for _ in range(batch_size)]
                s_batch = [slots[i] for i in batch_idx]
                b_batch = [bs[i] for i in batch_idx]
                sampled_slots.extend(s_batch)
                sampled_bs.extend(b_batch)
                if step <= 20 or step in {100, 800, 1600}:
                    batch_rows.append(
                        {
                            "condition": condition,
                            "seed": seed,
                            "step": step,
                            "slot_entropy_norm": norm_entropy([Counter(s_batch).get(s, 0) for s in range(num_slots)]),
                            "b_entropy_norm": norm_entropy([Counter(b_batch).get(b, 0) for b in range(b_count)]),
                            "slot_min": min(Counter(s_batch).values()),
                            "slot_max": max(Counter(s_batch).values()),
                            "unique_b": len(set(b_batch)),
                        }
                    )
            sampled_slot_counter = Counter(sampled_slots)
            sampled_b_counter = Counter(sampled_bs)
            sampled_pair_counter = Counter(zip(sampled_slots, sampled_bs))
            row = {
                "condition": condition,
                "seed": seed,
                "split": "training_sampled_with_replacement",
                "num_rows": len(sampled_slots),
                "x_hash": "",
                "first100_hash": "",
                "adjacent_slot_equal_fraction": sum(1 for a, b in zip(sampled_slots, sampled_slots[1:]) if a == b) / max(1, len(sampled_slots) - 1),
                "adjacent_b_equal_fraction": sum(1 for a, b in zip(sampled_bs, sampled_bs[1:]) if a == b) / max(1, len(sampled_bs) - 1),
            }
            row.update(count_summary(sampled_slot_counter, list(range(num_slots)), "slot"))
            row.update(count_summary(sampled_b_counter, list(range(b_count)), "b"))
            row.update(count_summary(sampled_pair_counter, [(s, b) for s in range(num_slots) for b in range(b_count)], "slot_b"))
            rows.append(row)

            feature_eval = runner.generate_feature_variant_data(cfg, condition, MODE, seed)
            fs = feature_eval.slot.tolist()
            fb = feature_eval.b_idx.tolist()
            fv = feature_eval.variant.tolist()
            row = {
                "condition": condition,
                "seed": seed,
                "split": "feature_variant_eval",
                "num_rows": int(feature_eval.x.shape[0]),
                "x_hash": sha_tensor(feature_eval.x[: min(4096, feature_eval.x.shape[0])]),
                "first100_hash": sha_tensor(feature_eval.x[:100]),
                "adjacent_slot_equal_fraction": sum(1 for a, b in zip(fs, fs[1:]) if a == b) / max(1, len(fs) - 1),
                "adjacent_b_equal_fraction": sum(1 for a, b in zip(fb, fb[1:]) if a == b) / max(1, len(fb) - 1),
            }
            row.update(count_summary(Counter(fs), list(range(num_slots)), "slot"))
            row.update(count_summary(Counter(fb), list(range(b_count)), "b"))
            row.update(count_summary(Counter(zip(fs, fb)), [(s, b) for s in range(num_slots) for b in range(b_count)], "slot_b"))
            row.update(count_summary(Counter(zip(fs, fb, fv)), [(s, b, v) for s in range(num_slots) for b in range(b_count) for v in range(int(cfg["feature_key_eval"]["variants_per_key"]))], "slot_b_variant"))
            rows.append(row)
    return rows, first_rows, batch_rows


def param_row(name: str, tensor: torch.Tensor, bias_exists: bool | None = None) -> dict:
    t = tensor.detach().cpu().float().flatten()
    return {
        "parameter": name,
        "shape": "x".join(str(v) for v in tensor.shape),
        "mean": float(t.mean().item()),
        "std": float(t.std(unbiased=False).item()),
        "min": float(t.min().item()),
        "max": float(t.max().item()),
        "norm": float(t.norm().item()),
        "bias_exists": "" if bias_exists is None else int(bias_exists),
    }


def router_pairwise(w: torch.Tensor) -> tuple[float, float, float]:
    wn = F.normalize(w.detach().cpu().float(), p=2, dim=1)
    mat = wn @ wn.T
    vals = [float(mat[i, j].item()) for i in range(mat.shape[0]) for j in range(mat.shape[1]) if i != j]
    return min(vals), sum(vals) / len(vals), max(vals)


def audit_initialization_and_geometry(cfg: dict, device: torch.device) -> tuple[list[dict], list[dict], list[dict], list[dict], list[dict], list[dict]]:
    init_rows = []
    geom_rows = []
    decomp_rows = []
    feature_rows = []
    mc_rows = []
    source_rows = []
    data_cfg = cfg["data"]
    b_pos = int(data_cfg["b_position"])
    batch_size = int(cfg["evaluation"]["batch_size"])
    num_experts = int(cfg["model"]["num_experts"])
    b_count = int(data_cfg["b_token_count_multi"])
    num_slots = int(data_cfg["num_slots"])
    variants_per_key = int(cfg["feature_key_eval"]["variants_per_key"])

    for condition in CONDITIONS:
        for seed in SEEDS:
            model, init_meta = actual_model_for_condition(cfg, condition, seed, device)
            cond = runner.parse_true_token_condition(condition)
            w = model.moe.router.weight.detach().cpu().float()
            pair_min, pair_mean, pair_max = router_pairwise(w)
            row_base = {
                "condition": condition,
                "seed": seed,
                "router_init_type": init_meta["router_init_type"],
                "router_metric": str(model.moe.router_metric),
                "router_temperature": float(model.moe.router_temperature),
                "router_bias_exists": int(model.moe.router.bias is not None),
                "router_weight_shape": "x".join(str(v) for v in w.shape),
                "router_row_norms": " ".join(f"{v:.6f}" for v in w.norm(dim=1).tolist()),
                "router_pairwise_cos_min": pair_min,
                "router_pairwise_cos_mean": pair_mean,
                "router_pairwise_cos_max": pair_max,
                "router_weight_hash": sha_tensor(w),
                "slot_init_centroid_norm_mean": init_meta.get("centroid_norm_mean", ""),
            }
            init_rows.append({**row_base, **param_row("router.weight", model.moe.router.weight, model.moe.router.bias is not None)})
            init_rows.append({**row_base, **param_row("token_emb.weight", model.token_emb.weight)})
            init_rows.append({**row_base, **param_row("pos_emb.weight", model.pos_emb.weight)})
            init_rows.append({**row_base, **param_row("lm_head.weight", model.lm_head.weight, model.lm_head.bias is not None)})

            if condition not in FOCUS_CONDITIONS:
                continue

            feature_eval = runner.generate_feature_variant_data(cfg, condition, MODE, seed)
            hs = []
            slots = []
            bs = []
            routes = []
            logits_all = []
            model.eval()
            with torch.no_grad():
                for start in range(0, feature_eval.x.shape[0], batch_size):
                    x = feature_eval.x[start : start + batch_size].to(device)
                    _, info = model(x, return_acts=True)
                    h = info["ffn_input"][:, b_pos, :].detach().cpu().float()
                    hs.append(h)
                    routes.append(info["expert_idx"][:, b_pos].detach().cpu())
                    logits_all.append(info["router_logits"][:, b_pos, :].detach().cpu().float())
                    slots.append(feature_eval.slot[start : start + batch_size].detach().cpu())
                    bs.append(feature_eval.b_idx[start : start + batch_size].detach().cpu())
            h_all = torch.cat(hs, dim=0)
            route_all = torch.cat(routes, dim=0)
            logits_all_t = torch.cat(logits_all, dim=0)
            slot_all = torch.cat(slots, dim=0)
            b_all = torch.cat(bs, dim=0)

            # Exact feature centroids f=(slot,b).
            centroids = []
            feature_keys = []
            route_counts = torch.zeros(num_slots, b_count, num_experts)
            for s in range(num_slots):
                for b in range(b_count):
                    mask = (slot_all == s) & (b_all == b)
                    centroids.append(h_all[mask].mean(dim=0))
                    feature_keys.append((s, b))
                    for e in range(num_experts):
                        route_counts[s, b, e] = (route_all[mask] == e).sum()
            h_feat = torch.stack(centroids)
            c = h_feat.mean(dim=0)
            residual = h_feat - c
            c_norm = float(c.norm().item())
            h_norm_mean = float(h_feat.norm(dim=1).mean().item())
            residual_norm_mean = float(residual.norm(dim=1).mean().item())
            common_ratio = c_norm / h_norm_mean if h_norm_mean else math.nan
            centered = h_feat - h_feat.mean(dim=0, keepdim=True)
            sv = torch.linalg.svdvals(centered)
            energy = sv.square()
            pc1_frac = float((energy[0] / energy.sum()).item()) if energy.sum() > 0 else math.nan
            feat_cos = F.normalize(h_feat, p=2, dim=1) @ F.normalize(h_feat, p=2, dim=1).T
            res_cos = F.normalize(residual, p=2, dim=1) @ F.normalize(residual, p=2, dim=1).T
            offdiag = ~torch.eye(h_feat.shape[0], dtype=torch.bool)
            observed_counts = torch.bincount(route_all, minlength=num_experts).float()
            observed_load = observed_counts / observed_counts.sum()
            observed_max = float(observed_load.max().item())

            # Router scores on feature centroids.
            with torch.no_grad():
                full_scores = model.moe.router_logits(h_feat.to(device)).detach().cpu().float()
                if str(model.moe.router_metric) == "dot_product":
                    residual_scores = F.linear(residual, w)
                    common_scores = (w @ c).tolist()
                else:
                    residual_scores = float(model.moe.router_temperature) * (
                        F.normalize(residual, p=2, dim=1, eps=float(model.moe.router_eps))
                        @ F.normalize(w, p=2, dim=1, eps=float(model.moe.router_eps)).T
                    )
                    common_scores = (
                        F.normalize(c.unsqueeze(0), p=2, dim=1, eps=float(model.moe.router_eps))
                        @ F.normalize(w, p=2, dim=1, eps=float(model.moe.router_eps)).T
                    ).squeeze(0).tolist()
            full_top = full_scores.argmax(dim=1)
            residual_top = residual_scores.argmax(dim=1)
            full_load = torch.bincount(full_top, minlength=num_experts).float() / h_feat.shape[0]
            residual_load = torch.bincount(residual_top, minlength=num_experts).float() / h_feat.shape[0]
            top2 = torch.topk(full_scores, 2, dim=1).values
            margin = top2[:, 0] - top2[:, 1]

            geom_rows.append(
                {
                    "condition": condition,
                    "seed": seed,
                    "router_init_type": init_meta["router_init_type"],
                    "num_exact_features": h_feat.shape[0],
                    "variants_per_feature": variants_per_key,
                    "common_norm": c_norm,
                    "feature_norm_mean": h_norm_mean,
                    "residual_norm_mean": residual_norm_mean,
                    "common_ratio": common_ratio,
                    "pc1_energy_fraction_after_mean_centering": pc1_frac,
                    "feature_pairwise_cos_mean": float(feat_cos[offdiag].mean().item()),
                    "feature_pairwise_cos_min": float(feat_cos[offdiag].min().item()),
                    "feature_pairwise_cos_max": float(feat_cos[offdiag].max().item()),
                    "residual_pairwise_cos_mean": float(res_cos[offdiag].mean().item()),
                    "residual_pairwise_cos_min": float(res_cos[offdiag].min().item()),
                    "residual_pairwise_cos_max": float(res_cos[offdiag].max().item()),
                    "observed_sample_route_loads": " ".join(f"{v:.6f}" for v in observed_load.tolist()),
                    "observed_sample_max_load": observed_max,
                    "feature_centroid_full_loads": " ".join(f"{v:.6f}" for v in full_load.tolist()),
                    "feature_centroid_full_max_load": float(full_load.max().item()),
                    "feature_centroid_residual_loads": " ".join(f"{v:.6f}" for v in residual_load.tolist()),
                    "feature_centroid_residual_max_load": float(residual_load.max().item()),
                    "mean_top1_margin": float(margin.mean().item()),
                    "common_scores_by_expert": " ".join(f"{v:.6f}" for v in common_scores),
                    "common_score_argmax": int(torch.tensor(common_scores).argmax().item()),
                }
            )
            # Interpret the hidden common direction by comparing it to input/template sources.
            c_unit = F.normalize(c.unsqueeze(0), p=2, dim=1).squeeze(0)
            token_emb = model.token_emb.weight.detach().cpu().float()
            pos_emb = model.pos_emb.weight.detach().cpu().float()
            bg = int(data_cfg["background_token"])
            b_start = int(data_cfg["b_token_start"])
            b_tokens = torch.arange(b_start, b_start + b_count)
            slot_tokens = []
            for s in range(num_slots):
                slot_tokens.extend(runner.slot_code(condition, s, cfg))
            vectors = {
                "b_position_embedding": pos_emb[b_pos],
                "b_token_embedding_mean": token_emb[b_tokens].mean(dim=0),
                "b_position_plus_b_mean": pos_emb[b_pos] + token_emb[b_tokens].mean(dim=0),
                "background_token_embedding": token_emb[bg],
                "prefix_position_embedding_mean": pos_emb[:b_pos].mean(dim=0),
                "slot_code_token_embedding_mean": token_emb[torch.tensor(slot_tokens)].mean(dim=0),
            }
            raw_b = []
            for _, b in feature_keys:
                raw_b.append(token_emb[b_start + b] + pos_emb[b_pos])
            raw_b = torch.stack(raw_b)
            raw_c = raw_b.mean(dim=0)
            raw_res = raw_b - raw_c
            source_rows.append(
                {
                    "condition": condition,
                    "seed": seed,
                    "source": "raw_b_position_input",
                    "cosine_to_hidden_common": float((F.normalize(raw_c.unsqueeze(0), p=2, dim=1).squeeze(0) * c_unit).sum().item()),
                    "source_norm": float(raw_c.norm().item()),
                    "raw_common_ratio": float(raw_c.norm().item() / raw_b.norm(dim=1).mean().item()),
                    "raw_residual_norm_mean": float(raw_res.norm(dim=1).mean().item()),
                }
            )
            for name, vec in vectors.items():
                source_rows.append(
                    {
                        "condition": condition,
                        "seed": seed,
                        "source": name,
                        "cosine_to_hidden_common": float((F.normalize(vec.unsqueeze(0), p=2, dim=1).squeeze(0) * c_unit).sum().item()),
                        "source_norm": float(vec.norm().item()),
                        "raw_common_ratio": "",
                        "raw_residual_norm_mean": "",
                    }
                )
            for e in range(num_experts):
                decomp_rows.append(
                    {
                        "condition": condition,
                        "seed": seed,
                        "expert": e,
                        "common_score": float(common_scores[e]),
                        "full_feature_load": float(full_load[e].item()),
                        "residual_feature_load": float(residual_load[e].item()),
                        "sample_route_load": float(observed_load[e].item()),
                        "router_norm": float(w[e].norm().item()),
                    }
                )
            for (s, b), top_full, top_res, m in zip(feature_keys, full_top.tolist(), residual_top.tolist(), margin.tolist()):
                if b < 8:
                    feature_rows.append(
                        {
                            "condition": condition,
                            "seed": seed,
                            "slot": s,
                            "b_idx": b,
                            "top_full_expert": int(top_full),
                            "top_residual_expert": int(top_res),
                            "top1_margin": float(m),
                        }
                    )

            # Monte Carlo isotropic random geometry baseline for feature count.
            trials = 5000
            g = torch.Generator().manual_seed(seed + 991)
            rand_scores = torch.randn(trials, h_feat.shape[0], num_experts, generator=g)
            rand_top = rand_scores.argmax(dim=2)
            rand_counts = torch.stack([(rand_top == e).sum(dim=1) for e in range(num_experts)], dim=1).float()
            rand_max = (rand_counts / h_feat.shape[0]).max(dim=1).values
            mc_rows.append(
                {
                    "condition": condition,
                    "seed": seed,
                    "num_trials": trials,
                    "num_features": h_feat.shape[0],
                    "observed_feature_full_max_load": float(full_load.max().item()),
                    "observed_feature_residual_max_load": float(residual_load.max().item()),
                    "random_baseline_max_load_mean": float(rand_max.mean().item()),
                    "random_baseline_max_load_p95": float(torch.quantile(rand_max, 0.95).item()),
                    "random_baseline_max_load_p99": float(torch.quantile(rand_max, 0.99).item()),
                    "p_random_ge_observed_full": float((rand_max >= float(full_load.max().item())).float().mean().item()),
                    "p_random_ge_observed_residual": float((rand_max >= float(residual_load.max().item())).float().mean().item()),
                }
            )
    return init_rows, geom_rows, decomp_rows, feature_rows, mc_rows, source_rows


def audit_early_gradients(cfg: dict, device: torch.device) -> list[dict]:
    rows = []
    targets = [("R0-dot", 20260522), ("R1-dot", 20260522), ("S1-cos", 20260522), ("S1-cos", 20260523)]
    b_pos = int(cfg["data"]["b_position"])
    batch_size = int(cfg["training"]["batch_size"])
    for condition, seed in targets:
        model, init_meta = actual_model_for_condition(cfg, condition, seed, device)
        train_data = runner.generate_slot_data(cfg, condition, MODE, "train", int(cfg["data"]["train_samples_per_slot"]), seed)
        opt = torch.optim.AdamW(model.parameters(), lr=float(cfg["training"]["lr"]), weight_decay=float(cfg["training"]["weight_decay"]))
        rng = random.Random(seed + 17)
        indices = list(range(train_data.x.shape[0]))
        w0 = model.moe.router.weight.detach().cpu().float().clone()
        model.train()
        for step in range(0, 11):
            batch_idx = [indices[rng.randrange(len(indices))] for _ in range(batch_size)]
            x = train_data.x[batch_idx].to(device)
            if step == 0:
                with torch.no_grad():
                    _, info = model(x, return_acts=True)
                    expert = info["expert_idx"][:, b_pos].detach().cpu()
                    counts = torch.bincount(expert, minlength=int(cfg["model"]["num_experts"])).float()
                    load = counts / counts.sum()
                    rows.append(
                        {
                            "condition": condition,
                            "seed": seed,
                            "router_init_type": init_meta["router_init_type"],
                            "step": 0,
                            "phase": "before_update",
                            "load_by_expert": " ".join(f"{v:.6f}" for v in load.tolist()),
                            "max_load": float(load.max().item()),
                            "dominant_expert": int(load.argmax().item()),
                            "router_grad_norm_by_row": "",
                            "router_delta_by_row": " ".join("0.000000" for _ in range(int(cfg["model"]["num_experts"]))),
                            "dominant_grad_norm": "",
                        }
                    )
                continue
            logits, info = model(x, return_acts=True)
            loss = runner.full_ntp_loss(logits, x)
            cond = runner.parse_true_token_condition(condition)
            if cond.token_inhibition:
                inh, _ = runner.true_token_conditioned_inhibition_loss(
                    model,
                    info["ffn_input"][:, b_pos, :],
                    info["expert_idx"][:, b_pos],
                    info["router_logits"][:, b_pos, :],
                    cfg,
                )
                loss = loss + float(cfg["true_token_inhibition"]["loss_weight"]) * inh
            opt.zero_grad(set_to_none=True)
            loss.backward()
            grad = model.moe.router.weight.grad.detach().cpu().float()
            expert = info["expert_idx"][:, b_pos].detach().cpu()
            counts = torch.bincount(expert, minlength=int(cfg["model"]["num_experts"])).float()
            load = counts / counts.sum()
            grad_norm = grad.norm(dim=1)
            torch.nn.utils.clip_grad_norm_(model.parameters(), float(cfg["training"]["grad_clip"]))
            opt.step()
            delta = (model.moe.router.weight.detach().cpu().float() - w0).norm(dim=1)
            dom = int(load.argmax().item())
            rows.append(
                {
                    "condition": condition,
                    "seed": seed,
                    "router_init_type": init_meta["router_init_type"],
                    "step": step,
                    "phase": "after_update",
                    "load_by_expert": " ".join(f"{v:.6f}" for v in load.tolist()),
                    "max_load": float(load.max().item()),
                    "dominant_expert": dom,
                    "router_grad_norm_by_row": " ".join(f"{v:.6f}" for v in grad_norm.tolist()),
                    "router_delta_by_row": " ".join(f"{v:.6f}" for v in delta.tolist()),
                    "dominant_grad_norm": float(grad_norm[dom].item()),
                }
            )
    return rows


def plot_outputs() -> None:
    import matplotlib.pyplot as plt

    def read_csv(path: Path) -> list[dict]:
        with path.open(newline="") as f:
            return list(csv.DictReader(f))

    geom = read_csv(TABLE_DIR / "step0_hidden_common_geometry.csv")
    decomp = read_csv(TABLE_DIR / "router_score_decomposition.csv")
    grad = read_csv(TABLE_DIR / "early_gradient_self_reinforcement.csv")

    # Step-0 full vs residual max load.
    fig, ax = plt.subplots(figsize=(10, 5))
    labels = []
    full = []
    resid = []
    for r in geom:
        if r["seed"] == "20260522":
            labels.append(r["condition"])
            full.append(float(r["feature_centroid_full_max_load"]))
            resid.append(float(r["feature_centroid_residual_max_load"]))
    x = torch.arange(len(labels)).float()
    ax.bar((x - 0.18).tolist(), full, width=0.36, label="full hidden")
    ax.bar((x + 0.18).tolist(), resid, width=0.36, label="residual after subtracting mean")
    ax.axhline(0.25, color="#444444", linewidth=0.8, linestyle="--", label="balanced 4 experts")
    ax.set_xticks(x.tolist(), labels, rotation=25, ha="right")
    ax.set_ylabel("max feature load")
    ax.set_title("Step-0 feature load: full hidden vs residual-only routing, seed 20260522")
    ax.legend(frameon=False)
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    fig.savefig(FIG_DIR / "step0_full_vs_residual_load_seed20260522.png", dpi=180)
    plt.close(fig)

    # Common score and load by expert for S1-cos 20260522 and R0-dot 20260522.
    fig, axes = plt.subplots(1, 2, figsize=(10, 4), sharey=False)
    for ax, condition in zip(axes, ["R0-dot", "S1-cos"]):
        rows = [r for r in decomp if r["condition"] == condition and r["seed"] == "20260522"]
        experts = [int(r["expert"]) for r in rows]
        common = [float(r["common_score"]) for r in rows]
        load = [float(r["full_feature_load"]) for r in rows]
        ax2 = ax.twinx()
        ax.bar([e - 0.15 for e in experts], common, width=0.3, color="#386cb0", label="common score")
        ax2.bar([e + 0.15 for e in experts], load, width=0.3, color="#fdb462", label="full feature load")
        ax.set_title(f"{condition} seed 20260522")
        ax.set_xlabel("expert")
        ax.set_ylabel("common score")
        ax2.set_ylabel("feature load")
        ax.set_xticks(experts)
    fig.suptitle("Common-direction score aligns with dominant route expert")
    fig.tight_layout()
    fig.savefig(FIG_DIR / "common_score_vs_load_examples.png", dpi=180)
    plt.close(fig)

    # Early gradient/load self-reinforcement.
    fig, axes = plt.subplots(2, 2, figsize=(11, 7), sharex=True, sharey=True)
    for ax, key in zip(axes.flat, [("R0-dot", "20260522"), ("R1-dot", "20260522"), ("S1-cos", "20260522"), ("S1-cos", "20260523")]):
        rows = [r for r in grad if r["condition"] == key[0] and r["seed"] == key[1]]
        ax.plot([int(r["step"]) for r in rows], [float(r["max_load"]) for r in rows], marker="o", label="max load")
        dom_grad = [float(r["dominant_grad_norm"]) if r["dominant_grad_norm"] else 0.0 for r in rows]
        if max(dom_grad) > 0:
            scale = max(dom_grad)
            ax.plot([int(r["step"]) for r in rows], [v / scale for v in dom_grad], marker="x", linestyle="--", label="dominant grad norm, normalized")
        ax.set_title(f"{key[0]} seed {key[1]}")
        ax.grid(alpha=0.25)
    axes[0, 0].legend(frameon=False, fontsize=8)
    for ax in axes[-1, :]:
        ax.set_xlabel("training step")
    for ax in axes[:, 0]:
        ax.set_ylabel("value")
    fig.suptitle("Early selected-expert self-reinforcement check")
    fig.tight_layout()
    fig.savefig(FIG_DIR / "early_gradient_self_reinforcement.png", dpi=180)
    plt.close(fig)


def main() -> None:
    TABLE_DIR.mkdir(parents=True, exist_ok=True)
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    cfg = load_cfg()
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    data_rows, first_rows, batch_rows = audit_data(cfg)
    write_csv(TABLE_DIR / "data_uniformity_counts.csv", data_rows)
    write_csv(TABLE_DIR / "first_100_samples.csv", first_rows)
    write_csv(TABLE_DIR / "batch_order_entropy.csv", batch_rows)

    init_rows, geom_rows, decomp_rows, feature_rows, mc_rows, source_rows = audit_initialization_and_geometry(cfg, device)
    write_csv(TABLE_DIR / "initialization_parameter_stats.csv", init_rows)
    write_csv(TABLE_DIR / "step0_hidden_common_geometry.csv", geom_rows)
    write_csv(TABLE_DIR / "router_score_decomposition.csv", decomp_rows)
    write_csv(TABLE_DIR / "feature_top1_examples_first8_b.csv", feature_rows)
    write_csv(TABLE_DIR / "random_geometry_baseline.csv", mc_rows)
    write_csv(TABLE_DIR / "common_direction_source_alignment.csv", source_rows)

    grad_rows = audit_early_gradients(cfg, device)
    write_csv(TABLE_DIR / "early_gradient_self_reinforcement.csv", grad_rows)

    write_json(
        TABLE_DIR / "audit_manifest.json",
        {
            "workspace": str(WORKSPACE),
            "config": str(WORKSPACE / "configs/h0605a_true_token_conditioned_inhibition_replay.json"),
            "conditions": CONDITIONS,
            "focus_conditions": FOCUS_CONDITIONS,
            "seeds": SEEDS,
            "device": str(device),
            "notes": "S* conditions overwrite PyTorch random router weights with slot-centroid initialization; R* conditions keep PyTorch default random router weights.",
        },
    )
    plot_outputs()


if __name__ == "__main__":
    main()
