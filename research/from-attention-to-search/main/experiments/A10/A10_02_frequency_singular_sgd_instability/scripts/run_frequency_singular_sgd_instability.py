#!/usr/bin/env python3
import argparse
import json
import math
import os
import random
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.nn.functional as F


IGNORE_INDEX = -100


@dataclass(frozen=True)
class Condition:
    name: str
    optimizer: str
    lr_key: str
    label_smoothing: float = 0.0
    row_clip: bool = False
    row_norm: bool = False
    spectral_clip: bool = False


CONDITIONS = [
    Condition("adamw_ce", "adamw", "adam_lr"),
    Condition("sgd_safe_ce", "sgd", "safe_lr"),
    Condition("sgd_high_ce", "sgd", "high_lr"),
    Condition("sgd_high_row_clip", "sgd", "high_lr", row_clip=True),
    Condition("sgd_high_row_norm", "sgd", "high_lr", row_norm=True),
    Condition("sgd_high_label_smoothing", "sgd", "high_lr", label_smoothing=0.10),
    Condition("sgd_high_spectral_clip", "sgd", "high_lr", spectral_clip=True),
]


class TinyCausalLM(nn.Module):
    def __init__(self, input_vocab_size: int, output_vocab_size: int, max_len: int, d_model: int):
        super().__init__()
        self.token_emb = nn.Embedding(input_vocab_size, d_model)
        self.pos_emb = nn.Parameter(torch.randn(max_len, d_model) * 0.02)
        self.attn = nn.MultiheadAttention(d_model, num_heads=1, batch_first=True, dropout=0.0)
        self.ln1 = nn.LayerNorm(d_model)
        self.ff = nn.Sequential(
            nn.Linear(d_model, 2 * d_model),
            nn.GELU(),
            nn.Linear(2 * d_model, d_model),
        )
        self.ln2 = nn.LayerNorm(d_model)
        self.lm_head = nn.Linear(d_model, output_vocab_size)

    def forward(self, input_ids: torch.Tensor, return_hidden: bool = False):
        _, seq_len = input_ids.shape
        x = self.token_emb(input_ids) + self.pos_emb[:seq_len]
        mask = torch.triu(
            torch.full((seq_len, seq_len), float("-inf"), device=input_ids.device),
            diagonal=1,
        )
        attn_out, _ = self.attn(x, x, x, attn_mask=mask, need_weights=False)
        h = self.ln1(x + attn_out)
        h = self.ln2(h + self.ff(h))
        logits = self.lm_head(h)
        if return_hidden:
            return logits, h
        return logits


def parse_seed_list(seed_text: str):
    return [int(x.strip()) for x in seed_text.split(",") if x.strip()]


def set_seed(seed: int):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)


def zipf_depth_probs(max_depth: int, exponent: float, device: torch.device):
    depths = torch.arange(1, max_depth + 1, device=device, dtype=torch.float32)
    weights = 1.0 / torch.pow(depths, exponent)
    return weights / weights.sum()


def target_frequencies_from_depth_probs(probs: torch.Tensor):
    freqs = []
    for token_idx in range(probs.numel()):
        freqs.append(probs[token_idx:].sum().item())
    arr = np.asarray(freqs, dtype=np.float64)
    return arr / arr.sum()


def generate_batch(batch_size: int, probs: torch.Tensor, args, device: torch.device):
    max_depth = args.max_depth
    max_len = max_depth + 1
    pad_id = max_depth
    bos_id = max_depth + 1
    levels = torch.multinomial(probs, batch_size, replacement=True) + 1
    input_ids = torch.full((batch_size, max_len), pad_id, dtype=torch.long, device=device)
    labels = torch.full((batch_size, max_len), IGNORE_INDEX, dtype=torch.long, device=device)
    input_ids[:, 0] = bos_id
    base_tokens = torch.arange(max_depth, dtype=torch.long, device=device)
    for idx, level in enumerate(levels.tolist()):
        input_ids[idx, 1 : level + 1] = base_tokens[:level]
        labels[idx, :level] = base_tokens[:level]
    return input_ids, labels


def make_eval_set(args, probs: torch.Tensor, device: torch.device):
    return generate_batch(args.eval_size, probs, args, device)


def ce_loss(logits: torch.Tensor, labels: torch.Tensor, label_smoothing: float = 0.0):
    return F.cross_entropy(
        logits.reshape(-1, logits.shape[-1]),
        labels.reshape(-1),
        ignore_index=IGNORE_INDEX,
        label_smoothing=label_smoothing,
    )


def loss_and_accuracy(logits: torch.Tensor, labels: torch.Tensor):
    vocab = logits.shape[-1]
    flat_logits = logits.reshape(-1, vocab)
    flat_labels = labels.reshape(-1)
    valid = flat_labels != IGNORE_INDEX
    per_token = F.cross_entropy(flat_logits, flat_labels, ignore_index=IGNORE_INDEX, reduction="none")
    preds = flat_logits.argmax(dim=-1)
    out = {}
    groups = {
        "all": valid,
        "common": valid & (flat_labels <= 1),
        "rare": valid & (flat_labels >= 4),
    }
    for name, mask in groups.items():
        count = int(mask.sum().item())
        if count == 0:
            out[f"{name}_loss"] = float("nan")
            out[f"{name}_accuracy"] = float("nan")
        else:
            out[f"{name}_loss"] = float(per_token[mask].mean().item())
            out[f"{name}_accuracy"] = float((preds[mask] == flat_labels[mask]).float().mean().item())
    return out


def spearman_corr(x: np.ndarray, y: np.ndarray):
    if np.allclose(x, x[0]) or np.allclose(y, y[0]):
        return float("nan")
    rx = pd.Series(x).rank(method="average").to_numpy()
    ry = pd.Series(y).rank(method="average").to_numpy()
    return float(np.corrcoef(rx, ry)[0, 1])


def effective_rank(s: torch.Tensor):
    energy = s.square()
    total = energy.sum()
    if total <= 0:
        return float("nan")
    p = energy / total
    entropy = -(p * torch.log(p + 1e-12)).sum()
    return float(torch.exp(entropy).item())


def output_svd(model: TinyCausalLM):
    weight = model.lm_head.weight.detach().float()
    u, s, vh = torch.linalg.svd(weight, full_matrices=False)
    energy = s.square()
    top_k = min(2, s.numel())
    top_energy = float((energy[:top_k].sum() / (energy.sum() + 1e-12)).item())
    return s, vh, top_energy


def extra_feature_metrics(model: TinyCausalLM, args, device: torch.device, vh: torch.Tensor):
    max_depth = args.max_depth
    max_len = max_depth + 1
    pad_id = max_depth
    bos_id = max_depth + 1
    ids = torch.full((1, max_len), pad_id, dtype=torch.long, device=device)
    ids[0, 0] = bos_id
    ids[0, 1:] = torch.arange(max_depth, dtype=torch.long, device=device)
    with torch.no_grad():
        _, h = model(ids, return_hidden=True)
    contexts = h[0, :max_depth, :].float()
    extras = contexts[1:] - contexts[:-1]
    if extras.numel() == 0:
        return {"extra_erank": float("nan"), "extra_top2_mass": float("nan")}
    s_extra = torch.linalg.svdvals(extras)
    erank = effective_rank(s_extra)
    vtop = vh[: min(2, vh.shape[0])].T
    extras_norm = extras / (extras.norm(dim=1, keepdim=True) + 1e-12)
    top_mass = (extras_norm @ vtop).square().sum(dim=1).mean()
    return {"extra_erank": erank, "extra_top2_mass": float(top_mass.item())}


def grad_profile(model: TinyCausalLM, grad_w: torch.Tensor, token_freq: np.ndarray):
    s, vh, top_energy = output_svd(model)
    vtop = vh[: min(2, vh.shape[0])].T.to(grad_w.device)
    grad_float = grad_w.detach().float()
    top_band = (grad_float @ vtop).square().sum() / (grad_float.square().sum() + 1e-12)
    row_norms = grad_float.norm(dim=1).detach().cpu().numpy()
    return {
        "top_singular_value": float(s[0].item()),
        "top2_energy_fraction": top_energy,
        "top_band_grad_mass": float(top_band.item()),
        "token_grad_imbalance": float(row_norms.max() / (row_norms.mean() + 1e-12)),
        "token_grad_concentration": float(row_norms.max() / (row_norms.sum() + 1e-12)),
        "freq_grad_spearman": spearman_corr(token_freq, row_norms),
    }


def evaluate_profile(model: TinyCausalLM, eval_ids: torch.Tensor, eval_labels: torch.Tensor, args, device):
    with torch.no_grad():
        logits, _ = model(eval_ids, return_hidden=True)
        metrics = loss_and_accuracy(logits, eval_labels)
    s, vh, top_energy = output_svd(model)
    metrics.update(
        {
            "top_singular_value": float(s[0].item()),
            "top2_energy_fraction": top_energy,
        }
    )
    metrics.update(extra_feature_metrics(model, args, device, vh))
    return metrics


def apply_output_row_transform(model: TinyCausalLM, condition: Condition, args):
    grad = model.lm_head.weight.grad
    if grad is None:
        return
    if condition.row_clip:
        norms = grad.norm(dim=1, keepdim=True)
        target = norms.median().clamp_min(1e-12) * args.row_clip_mult
        scale = torch.clamp(target / (norms + 1e-12), max=1.0)
        grad.mul_(scale)
        if model.lm_head.bias is not None and model.lm_head.bias.grad is not None:
            model.lm_head.bias.grad.mul_(scale.squeeze(1))
    if condition.row_norm:
        norms = grad.norm(dim=1, keepdim=True)
        target = norms.mean().clamp_min(1e-12)
        scale = target / (norms + 1e-12)
        grad.mul_(scale)
        if model.lm_head.bias is not None and model.lm_head.bias.grad is not None:
            model.lm_head.bias.grad.mul_(torch.clamp(scale.squeeze(1), max=10.0))


def apply_spectral_clip(model: TinyCausalLM, cap: float):
    with torch.no_grad():
        weight = model.lm_head.weight.data.float()
        u, s, vh = torch.linalg.svd(weight, full_matrices=False)
        clipped = torch.clamp(s, max=cap)
        new_weight = (u * clipped.unsqueeze(0)) @ vh
        model.lm_head.weight.data.copy_(new_weight.to(model.lm_head.weight.dtype))


def make_optimizer(model: TinyCausalLM, condition: Condition, lr: float, args):
    if condition.optimizer == "adamw":
        return torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=args.weight_decay)
    if condition.optimizer == "sgd":
        return torch.optim.SGD(model.parameters(), lr=lr, momentum=0.0)
    raise ValueError(f"unknown optimizer {condition.optimizer}")


def should_mark_unstable(eval_metrics, init_metrics, current_top_sv, init_top_sv):
    if not math.isfinite(eval_metrics["all_loss"]):
        return True
    if eval_metrics["all_loss"] > init_metrics["all_loss"] * 6.0:
        return True
    if current_top_sv > max(init_top_sv * 18.0, init_top_sv + 12.0):
        return True
    return False


def run_one(seed: int, condition: Condition, args, device: torch.device, out_run_dir: Path):
    set_seed(seed)
    probs = zipf_depth_probs(args.max_depth, args.zipf_exponent, device)
    token_freq = target_frequencies_from_depth_probs(probs)
    eval_ids, eval_labels = make_eval_set(args, probs, device)
    model = TinyCausalLM(
        input_vocab_size=args.max_depth + 2,
        output_vocab_size=args.max_depth,
        max_len=args.max_depth + 1,
        d_model=args.d_model,
    ).to(device)
    lr = getattr(args, condition.lr_key)
    optimizer = make_optimizer(model, condition, lr, args)
    init_metrics = evaluate_profile(model, eval_ids, eval_labels, args, device)
    init_top_sv = init_metrics["top_singular_value"]
    step_records = []
    unstable_step = None
    last_grad_metrics = {}

    step_records.append(
        {
            "seed": seed,
            "condition": condition.name,
            "step": 0,
            "lr": lr,
            "stable_so_far": True,
            "instability_step": np.nan,
            **init_metrics,
        }
    )

    for step in range(1, args.steps + 1):
        model.train()
        input_ids, labels = generate_batch(args.batch_size, probs, args, device)
        optimizer.zero_grad(set_to_none=True)
        logits = model(input_ids)
        loss = ce_loss(logits, labels, condition.label_smoothing)
        if not torch.isfinite(loss):
            unstable_step = step
            break
        loss.backward()
        apply_output_row_transform(model, condition, args)
        grad_w = model.lm_head.weight.grad.detach().clone()
        last_grad_metrics = grad_profile(model, grad_w, token_freq)
        optimizer.step()
        if condition.spectral_clip:
            apply_spectral_clip(model, args.spectral_cap)

        should_log = step <= 5 or step % args.log_every == 0 or step == args.steps
        if should_log:
            model.eval()
            eval_metrics = evaluate_profile(model, eval_ids, eval_labels, args, device)
            eval_metrics.update(last_grad_metrics)
            stable_now = unstable_step is None
            if unstable_step is None and should_mark_unstable(
                eval_metrics,
                init_metrics,
                eval_metrics["top_singular_value"],
                init_top_sv,
            ):
                unstable_step = step
                stable_now = False
            step_records.append(
                {
                    "seed": seed,
                    "condition": condition.name,
                    "step": step,
                    "lr": lr,
                    "stable_so_far": stable_now,
                    "instability_step": unstable_step if unstable_step is not None else np.nan,
                    **eval_metrics,
                }
            )
            if unstable_step is not None and args.stop_on_instability:
                break

    final_metrics = step_records[-1].copy()
    final_metrics["seed"] = seed
    final_metrics["condition"] = condition.name
    final_metrics["lr"] = lr
    final_metrics["completed_steps"] = int(final_metrics["step"])
    final_metrics["stable"] = unstable_step is None
    final_metrics["instability_step"] = unstable_step if unstable_step is not None else np.nan
    final_metrics["initial_eval_loss"] = init_metrics["all_loss"]
    final_metrics["top_sv_growth"] = final_metrics["top_singular_value"] / (init_top_sv + 1e-12)
    final_metrics["common_acc_gain"] = final_metrics["common_accuracy"] - init_metrics["common_accuracy"]
    final_metrics["rare_acc_gain"] = final_metrics["rare_accuracy"] - init_metrics["rare_accuracy"]

    seed_dir = out_run_dir / f"{condition.name}_seed{seed}"
    seed_dir.mkdir(parents=True, exist_ok=True)
    with open(seed_dir / "final_metrics.json", "w", encoding="utf-8") as f:
        json.dump(final_metrics, f, indent=2, sort_keys=True)

    return step_records, final_metrics


def aggregate_tables(step_df: pd.DataFrame, final_df: pd.DataFrame):
    early = step_df[(step_df["step"] > 0) & (step_df["step"] <= 25)]
    early_agg = (
        early.groupby("condition")
        .agg(
            early_freq_grad_spearman=("freq_grad_spearman", "median"),
            early_top_band_grad_mass=("top_band_grad_mass", "median"),
            early_token_grad_concentration=("token_grad_concentration", "median"),
        )
        .reset_index()
    )
    summary = (
        final_df.groupby("condition")
        .agg(
            stable_rate=("stable", "mean"),
            mean_instability_step=("instability_step", "mean"),
            final_eval_loss_mean=("all_loss", "mean"),
            final_eval_loss_std=("all_loss", "std"),
            final_common_acc_mean=("common_accuracy", "mean"),
            final_rare_acc_mean=("rare_accuracy", "mean"),
            top_sv_growth_mean=("top_sv_growth", "mean"),
            top2_energy_fraction_mean=("top2_energy_fraction", "mean"),
            top_band_grad_mass_mean=("top_band_grad_mass", "mean"),
            token_grad_concentration_mean=("token_grad_concentration", "mean"),
            freq_grad_spearman_median=("freq_grad_spearman", "median"),
            extra_erank_mean=("extra_erank", "mean"),
            extra_top2_mass_mean=("extra_top2_mass", "mean"),
        )
        .reset_index()
    )
    return summary.merge(early_agg, on="condition", how="left")


def plot_temporal(step_df: pd.DataFrame, fig_dir: Path):
    selected = ["adamw_ce", "sgd_safe_ce", "sgd_high_ce", "sgd_high_spectral_clip"]
    metrics = [
        ("common_accuracy", "common accuracy"),
        ("rare_accuracy", "rare accuracy"),
        ("top_singular_value", "top singular value"),
        ("all_loss", "eval loss"),
    ]
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    for ax, (metric, title) in zip(axes.ravel(), metrics):
        for condition in selected:
            df = step_df[step_df["condition"] == condition]
            if df.empty:
                continue
            g = df.groupby("step")[metric].mean()
            ax.plot(g.index, g.values, label=condition)
        ax.set_title(title)
        ax.set_xlabel("step")
        ax.grid(alpha=0.25)
    axes[0, 0].legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(fig_dir / "temporal_profile.png", dpi=180)
    plt.close(fig)


def plot_stability(summary: pd.DataFrame, fig_dir: Path):
    fig, ax1 = plt.subplots(figsize=(12, 5))
    order = summary.sort_values("condition")["condition"].tolist()
    x = np.arange(len(order))
    stable = summary.set_index("condition").loc[order]["stable_rate"]
    loss = summary.set_index("condition").loc[order]["final_eval_loss_mean"]
    ax1.bar(x - 0.2, stable, width=0.4, label="stable rate")
    ax1.set_ylim(0, 1.05)
    ax1.set_ylabel("stable rate")
    ax2 = ax1.twinx()
    ax2.bar(x + 0.2, loss, width=0.4, color="tab:orange", label="final eval loss")
    ax2.set_ylabel("final eval loss")
    ax1.set_xticks(x)
    ax1.set_xticklabels(order, rotation=35, ha="right")
    ax1.set_title("Stability and final loss by condition")
    fig.tight_layout()
    fig.savefig(fig_dir / "stability_by_condition.png", dpi=180)
    plt.close(fig)


def plot_spectral(step_df: pd.DataFrame, fig_dir: Path):
    selected = [
        "adamw_ce",
        "sgd_safe_ce",
        "sgd_high_ce",
        "sgd_high_row_clip",
        "sgd_high_row_norm",
        "sgd_high_spectral_clip",
    ]
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
    for condition in selected:
        df = step_df[step_df["condition"] == condition]
        if df.empty:
            continue
        g = df.groupby("step")["top_band_grad_mass"].mean()
        axes[0].plot(g.index, g.values, label=condition)
        c = df.groupby("step")["token_grad_concentration"].mean()
        axes[1].plot(c.index, c.values, label=condition)
    axes[0].set_title("Top spectral-band gradient mass")
    axes[1].set_title("Token-gradient concentration")
    for ax in axes:
        ax.set_xlabel("step")
        ax.grid(alpha=0.25)
    axes[0].legend(fontsize=7)
    fig.tight_layout()
    fig.savefig(fig_dir / "spectral_localization.png", dpi=180)
    plt.close(fig)


def plot_extra(step_df: pd.DataFrame, fig_dir: Path):
    selected = ["adamw_ce", "sgd_safe_ce", "sgd_high_ce", "sgd_high_spectral_clip"]
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
    for condition in selected:
        df = step_df[step_df["condition"] == condition]
        if df.empty:
            continue
        g = df.groupby("step")["extra_erank"].mean()
        axes[0].plot(g.index, g.values, label=condition)
        m = df.groupby("step")["extra_top2_mass"].mean()
        axes[1].plot(m.index, m.values, label=condition)
    axes[0].set_title("Extra-feature effective rank")
    axes[1].set_title("Extra-feature top-2 mass")
    for ax in axes:
        ax.set_xlabel("step")
        ax.grid(alpha=0.25)
    axes[0].legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(fig_dir / "extra_feature_geometry.png", dpi=180)
    plt.close(fig)


def write_run_manifest(args, out_dir: Path, run_name: str, device: torch.device):
    manifest = {
        "run_name": run_name,
        "created": datetime.utcnow().isoformat() + "Z",
        "device": str(device),
        "args": vars(args),
        "conditions": [condition.__dict__ for condition in CONDITIONS],
    }
    with open(out_dir / "run_manifest.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, sort_keys=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", default=".")
    parser.add_argument("--run-name", default=None)
    parser.add_argument("--seeds", default="0,1,2")
    parser.add_argument("--conditions", default="all")
    parser.add_argument("--steps", type=int, default=240)
    parser.add_argument("--batch-size", type=int, default=192)
    parser.add_argument("--eval-size", type=int, default=2048)
    parser.add_argument("--d-model", type=int, default=32)
    parser.add_argument("--max-depth", type=int, default=7)
    parser.add_argument("--zipf-exponent", type=float, default=1.55)
    parser.add_argument("--adam-lr", type=float, default=0.006)
    parser.add_argument("--safe-lr", type=float, default=0.25)
    parser.add_argument("--high-lr", type=float, default=2.0)
    parser.add_argument("--weight-decay", type=float, default=0.0)
    parser.add_argument("--row-clip-mult", type=float, default=1.5)
    parser.add_argument("--spectral-cap", type=float, default=3.0)
    parser.add_argument("--log-every", type=int, default=5)
    parser.add_argument("--device", default="auto")
    parser.add_argument("--stop-on-instability", action="store_true")
    args = parser.parse_args()

    if args.device == "auto":
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    else:
        device = torch.device(args.device)
    run_name = args.run_name or f"a10_02_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
    exp_dir = Path(args.output_dir).resolve()
    run_dir = exp_dir / "runs" / run_name
    fig_dir = exp_dir / "figures"
    table_dir = exp_dir / "tables"
    run_dir.mkdir(parents=True, exist_ok=True)
    fig_dir.mkdir(parents=True, exist_ok=True)
    table_dir.mkdir(parents=True, exist_ok=True)
    write_run_manifest(args, run_dir, run_name, device)

    selected = CONDITIONS
    if args.conditions != "all":
        names = {name.strip() for name in args.conditions.split(",") if name.strip()}
        selected = [condition for condition in CONDITIONS if condition.name in names]
    seeds = parse_seed_list(args.seeds)

    all_steps = []
    all_finals = []
    for condition in selected:
        for seed in seeds:
            steps, final = run_one(seed, condition, args, device, run_dir)
            all_steps.extend(steps)
            all_finals.append(final)
            print(
                json.dumps(
                    {
                        "condition": condition.name,
                        "seed": seed,
                        "stable": final["stable"],
                        "instability_step": final["instability_step"],
                        "final_loss": final["all_loss"],
                        "common_acc": final["common_accuracy"],
                        "rare_acc": final["rare_accuracy"],
                        "top_sv_growth": final["top_sv_growth"],
                    },
                    sort_keys=True,
                ),
                flush=True,
            )

    step_df = pd.DataFrame(all_steps)
    final_df = pd.DataFrame(all_finals)
    summary = aggregate_tables(step_df, final_df)
    step_df.to_csv(table_dir / "step_metrics.csv", index=False)
    final_df.to_csv(table_dir / "final_by_seed.csv", index=False)
    summary.to_csv(table_dir / "condition_summary.csv", index=False)
    step_df.to_csv(run_dir / "step_metrics.csv", index=False)
    final_df.to_csv(run_dir / "final_by_seed.csv", index=False)
    summary.to_csv(run_dir / "condition_summary.csv", index=False)

    plot_temporal(step_df, fig_dir)
    plot_stability(summary, fig_dir)
    plot_spectral(step_df, fig_dir)
    plot_extra(step_df, fig_dir)

    with open(run_dir / "result_paths.json", "w", encoding="utf-8") as f:
        json.dump(
            {
                "step_metrics": str(table_dir / "step_metrics.csv"),
                "final_by_seed": str(table_dir / "final_by_seed.csv"),
                "condition_summary": str(table_dir / "condition_summary.csv"),
                "figures": {
                    "temporal_profile": str(fig_dir / "temporal_profile.png"),
                    "stability_by_condition": str(fig_dir / "stability_by_condition.png"),
                    "spectral_localization": str(fig_dir / "spectral_localization.png"),
                    "extra_feature_geometry": str(fig_dir / "extra_feature_geometry.png"),
                },
            },
            f,
            indent=2,
            sort_keys=True,
        )
    print(f"completed run_dir={run_dir}")


if __name__ == "__main__":
    main()
