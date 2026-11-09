#!/usr/bin/env python3
"""Run H0522 seq_len=32 router factor audit stages 1-5."""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import random
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path

os.environ.setdefault("PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION", "python")
os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib")

import torch
from torch import nn
from torch.nn import functional as F

from run_h0521b_seq32_contiguous_ab import (
    CLASS_NAMES,
    MoETinyTransformer,
    Top1MoEFFN,
    background_tokens,
    cluster_purity,
    final_logits,
    generate_dataset,
    load_json,
    normalized_mutual_info,
    project_root,
    resolve_output,
    write_csv,
    write_json,
)


FACTOR_FIELDS = [
    "token_identity",
    "token_id",
    "source_position",
    "left_token_identity",
    "source_role",
    "sample_class",
    "rule_label",
    "target_id",
    "background_vs_signal",
]


@dataclass
class AuditBundle:
    records: list[dict]
    hidden: torch.Tensor
    logits: torch.Tensor
    experts: list[int]


@dataclass
class DisentangledDataset:
    x: torch.Tensor
    y: torch.Tensor
    rule_labels: list[str]
    first_identity: list[str]
    second_identity: list[str]
    second_family: list[str]
    motif_positions: list[int]


def read_csv(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def factor_value(row: dict, field: str) -> str:
    return str(row.get(field, "NA"))


def entropy(vals: list[int]) -> float:
    n = len(vals)
    if n == 0:
        return 0.0
    counts = Counter(vals)
    return -sum((c / n) * math.log(c / n) for c in counts.values())


def conditional_entropy(labels: list[str], experts: list[int]) -> float:
    n = len(labels)
    groups: dict[str, list[int]] = defaultdict(list)
    for label, expert in zip(labels, experts):
        groups[label].append(expert)
    return sum((len(vals) / n) * entropy(vals) for vals in groups.values()) if n else 0.0


def majority_accuracy(labels: list[str], experts: list[int]) -> float:
    if not labels:
        return 0.0
    table: dict[str, Counter[int]] = defaultdict(Counter)
    for label, expert in zip(labels, experts):
        table[label][expert] += 1
    correct = 0
    for label, expert in zip(labels, experts):
        pred = table[label].most_common(1)[0][0]
        correct += int(pred == expert)
    return correct / len(labels)


def one_hot_r2(labels: list[str], y: torch.Tensor) -> float:
    if y.numel() == 0:
        return 0.0
    unique = sorted(set(labels))
    idx = {label: i for i, label in enumerate(unique)}
    x = torch.zeros(len(labels), len(unique) + 1, dtype=torch.float64)
    x[:, 0] = 1.0
    for i, label in enumerate(labels):
        x[i, idx[label] + 1] = 1.0
    y64 = y.to(torch.float64)
    coef = torch.linalg.lstsq(x, y64).solution
    pred = x @ coef
    sse = torch.sum((y64 - pred) ** 2).item()
    centered = y64 - y64.mean(dim=0, keepdim=True)
    sst = torch.sum(centered ** 2).item()
    return 1.0 - sse / sst if sst > 1e-12 else 0.0


def token_identity(token_id: int, cfg: dict) -> str:
    tokens = cfg["data"]["tokens"]
    if token_id == int(tokens["A"]):
        return "A"
    if token_id == int(tokens["B"]):
        return "B"
    return "background"


def left_token_identity(seq: torch.Tensor, pos: int, cfg: dict) -> str:
    if pos <= 0:
        return "BOS"
    return token_identity(int(seq[pos - 1].item()), cfg)


def load_h0521b_model(seed: int, cfg: dict, run_dir: Path, device: torch.device) -> MoETinyTransformer:
    model = MoETinyTransformer(int(cfg["data"]["vocab_size"]), cfg["model"]).to(device)
    ckpt_path = run_dir / "moe_top1_no_lb" / f"seed_{seed}" / "model.pt"
    ckpt = torch.load(ckpt_path, map_location=device)
    model.load_state_dict(ckpt["model_state"])
    model.eval()
    return model


def collect_audit_bundle(model: MoETinyTransformer, data, cfg: dict, seed: int, device: torch.device) -> AuditBundle:
    records: list[dict] = []
    hidden_rows: list[torch.Tensor] = []
    logit_rows: list[torch.Tensor] = []
    experts: list[int] = []
    batch_size = int(cfg["evaluation"]["batch_size"])
    model.eval()
    with torch.no_grad():
        for start in range(0, data.x.shape[0], batch_size):
            x = data.x[start : start + batch_size].to(device)
            y = data.y[start : start + batch_size]
            classes = data.classes[start : start + batch_size]
            motif_positions = data.motif_positions[start : start + batch_size]
            source_records = data.source_records[start : start + batch_size]
            _, info = model(x, return_acts=True)
            router_logits = info["router_logits"].detach().cpu()
            expert_idx = info["expert_idx"].detach().cpu()
            ffn_input = info["ffn_input"].detach().cpu()
            x_cpu = x.detach().cpu()
            for local_i, cls in enumerate(classes):
                for rec in source_records[local_i]:
                    pos = int(rec["position"])
                    tok = int(x_cpu[local_i, pos].item())
                    row = {
                        "run_id": "h0521b_existing",
                        "seed": seed,
                        "sample_id": start + local_i,
                        "sample_class": cls,
                        "position": pos,
                        "source_position": pos,
                        "token_id": tok,
                        "token_identity": str(rec["source_identity"]),
                        "token_role": str(rec["source_role"]),
                        "source_role": str(rec["source_role"]),
                        "left_token_id": int(x_cpu[local_i, pos - 1].item()) if pos > 0 else -1,
                        "left_token_identity": left_token_identity(x_cpu[local_i], pos, cfg),
                        "right_token_id_if_available": int(x_cpu[local_i, pos + 1].item()) if pos + 1 < x_cpu.shape[1] else -1,
                        "target_id": int(y[local_i].item()),
                        "rule_label": cls,
                        "background_vs_signal": "signal" if int(rec["is_motif_token"]) else "background",
                        "motif_position": int(motif_positions[local_i]),
                        "expert_id": int(expert_idx[local_i, pos].item()),
                    }
                    for e, val in enumerate(router_logits[local_i, pos].tolist()):
                        row[f"router_logit_{e}"] = val
                    records.append(row)
                    hidden_rows.append(ffn_input[local_i, pos].clone())
                    logit_rows.append(router_logits[local_i, pos].clone())
                    experts.append(row["expert_id"])
    return AuditBundle(records, torch.stack(hidden_rows), torch.stack(logit_rows), experts)


def factor_metrics(bundle: AuditBundle, seed: int) -> list[dict]:
    rows = []
    for factor in FACTOR_FIELDS:
        labels = [factor_value(row, factor) for row in bundle.records]
        rows.append(
            {
                "seed": seed,
                "factor": factor,
                "nmi": normalized_mutual_info(labels, bundle.experts),
                "conditional_entropy": conditional_entropy(labels, bundle.experts),
                "majority_expert_accuracy": majority_accuracy(labels, bundle.experts),
                "router_logit_r2": one_hot_r2(labels, bundle.logits),
                "num_levels": len(set(labels)),
                "num_records": len(labels),
            }
        )
    return rows


def component_metrics(bundle: AuditBundle, model: MoETinyTransformer, seed: int) -> list[dict]:
    rows = []
    global_mean = bundle.hidden.mean(dim=0, keepdim=True)
    w = model.moe.router.weight.detach().cpu()
    b = model.moe.router.bias.detach().cpu()
    natural = torch.argmax(bundle.logits, dim=-1)
    for factor in FACTOR_FIELDS:
        labels = [factor_value(row, factor) for row in bundle.records]
        means: dict[str, torch.Tensor] = {}
        for label in sorted(set(labels)):
            idx = torch.tensor([i for i, x in enumerate(labels) if x == label], dtype=torch.long)
            means[label] = bundle.hidden[idx].mean(dim=0, keepdim=True)
        comp = torch.cat([means[label] - global_mean for label in labels], dim=0)
        removed_logits = (bundle.hidden - comp) @ w.T + b
        comp_logits = comp @ w.T
        flipped = torch.argmax(removed_logits, dim=-1) != natural
        rows.append(
            {
                "seed": seed,
                "component": factor,
                "flip_rate": float(flipped.float().mean().item()),
                "component_logit_r2": one_hot_r2(labels, bundle.logits),
                "component_logit_norm_mean": float(comp_logits.norm(dim=-1).mean().item()),
                "num_records": len(labels),
            }
        )
    return rows


def evaluate_force_route(model: MoETinyTransformer, data, cfg: dict, device: torch.device, seed: int, prefix: str) -> list[dict]:
    batch_size = int(cfg["evaluation"]["batch_size"])
    num_experts = int(cfg["model"]["num_experts"])
    losses: dict[tuple[str, str], list[float]] = defaultdict(list)
    model.eval()
    with torch.no_grad():
        for mode in ["natural"] + [f"force_E{e}" for e in range(num_experts)] + [f"ablate_E{e}" for e in range(num_experts)]:
            for start in range(0, data.x.shape[0], batch_size):
                x = data.x[start : start + batch_size].to(device)
                y = data.y[start : start + batch_size].to(device)
                classes = data.classes[start : start + batch_size]
                kwargs = {}
                if mode.startswith("force_E"):
                    kwargs["force_expert"] = int(mode.split("E")[1])
                if mode.startswith("ablate_E"):
                    kwargs["ablate_expert"] = int(mode.split("E")[1])
                logits, _ = model_final_logits(model, x, **kwargs)
                ce = F.cross_entropy(logits, y, reduction="none")
                for i, cls in enumerate(classes):
                    losses[(mode, cls)].append(float(ce[i].detach().cpu()))
    natural = {cls: sum(losses[("natural", cls)]) / len(losses[("natural", cls)]) for cls in CLASS_NAMES}
    rows = []
    for (mode, cls), vals in losses.items():
        mean_ce = sum(vals) / len(vals)
        rows.append(
            {
                "seed": seed,
                "stage": prefix,
                "mode": mode,
                "class": cls,
                "mean_ce": mean_ce,
                "delta_ce_vs_natural": mean_ce - natural[cls],
            }
        )
    return rows


def model_final_logits(model: nn.Module, x: torch.Tensor, **kwargs):
    out = model(x, **kwargs)
    if isinstance(out, tuple):
        logits, info = out
    else:
        logits, info = out, {}
    return logits[:, -1, :], info


class StressMoETinyTransformer(nn.Module):
    def __init__(self, vocab_size: int, cfg: dict, residual_scale: float) -> None:
        super().__init__()
        seq_len = int(cfg["seq_len"])
        d_model = int(cfg["d_model"])
        self.residual_scale = float(residual_scale)
        self.token_emb = nn.Embedding(vocab_size, d_model)
        self.pos_emb = nn.Embedding(seq_len, d_model)
        self.attn = nn.MultiheadAttention(d_model, int(cfg["n_heads"]), batch_first=True, dropout=float(cfg["dropout"]))
        self.ln1 = nn.LayerNorm(d_model)
        self.moe = Top1MoEFFN(d_model, int(cfg["ffn_dim"]), int(cfg["num_experts"]), float(cfg["dropout"]))
        self.ln2 = nn.LayerNorm(d_model)
        self.dropout = nn.Dropout(float(cfg["dropout"]))
        self.lm_head = nn.Linear(d_model, vocab_size)

    def forward(self, idx, return_acts: bool = False, force_expert: int | None = None, ablate_expert: int | None = None):
        bsz, width = idx.shape
        pos = torch.arange(width, device=idx.device).unsqueeze(0).expand(bsz, width)
        x = self.token_emb(idx) + self.pos_emb(pos)
        mask = torch.triu(torch.ones(width, width, device=idx.device, dtype=torch.bool), diagonal=1)
        attn_out, _ = self.attn(x, x, x, attn_mask=mask, need_weights=False)
        x = self.ln1(x + self.dropout(attn_out))
        moe_input = x
        moe_out, info = self.moe(x, force_expert=force_expert, ablate_expert=ablate_expert)
        hidden = self.ln2(self.residual_scale * x + self.dropout(moe_out))
        logits = self.lm_head(hidden)
        if return_acts:
            info["ffn_input"] = moe_input
            info["hidden"] = hidden
        return logits, info


def train_stress_model(cfg: dict, train_data, seed: int, device: torch.device, residual_scale: float, run_stage: str):
    torch.manual_seed(seed + 7001)
    random.seed(seed + 7001)
    model = StressMoETinyTransformer(int(cfg["data"]["vocab_size"]), cfg["model"], residual_scale).to(device)
    train_cfg = cfg["stage4_stress"]
    steps = int(train_cfg["smoke_steps"] if run_stage == "smoke" else train_cfg["steps"])
    batch_size = int(train_cfg["batch_size"])
    opt = torch.optim.AdamW(model.parameters(), lr=float(train_cfg["lr"]), weight_decay=float(train_cfg["weight_decay"]))
    rng = random.Random(seed + 88)
    indices = list(range(train_data.x.shape[0]))
    model.train()
    for step in range(1, steps + 1):
        batch_idx = [indices[rng.randrange(len(indices))] for _ in range(batch_size)]
        x = train_data.x[batch_idx].to(device)
        y = train_data.y[batch_idx].to(device)
        logits, _ = model_final_logits(model, x)
        loss = F.cross_entropy(logits, y)
        opt.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), float(train_cfg["grad_clip"]))
        opt.step()
        if step == 1 or step % int(train_cfg["log_every"]) == 0 or step == steps:
            print(f"stage4 residual_scale={residual_scale} seed={seed} step={step} loss={float(loss.detach().cpu()):.4f}", flush=True)
    return model


def make_disentangled_dataset(cfg: dict, seed: int, split: str, samples_per_rule: int) -> DisentangledDataset:
    rng = random.Random(seed + (0 if split == "train" else 1000003))
    dcfg = cfg["stage5_disentangled"]
    seq_len = int(dcfg["seq_len"])
    vocab_size = int(dcfg["vocab_size"])
    n = int(dcfg["num_identity_pairs"])
    a_tokens = list(range(11, 11 + n))
    b_tokens = list(range(31, 31 + n))
    c_tokens = list(range(51, 51 + n))
    y0, y1 = 3, 4
    reserved = set(a_tokens + b_tokens + c_tokens + [y0, y1])
    bg_tokens = [i for i in range(80, vocab_size) if i not in reserved]
    rows = []
    rules = ["R_B_family", "R_C_family"]
    for rule in rules:
        for _ in range(samples_per_rule):
            i = rng.randrange(n)
            a = a_tokens[i]
            second = b_tokens[i] if rule == "R_B_family" else c_tokens[i]
            second_family = "B_family" if rule == "R_B_family" else "C_family"
            target = y0 if ((i % 2 == 0) == (rule == "R_B_family")) else y1
            p = rng.randrange(seq_len - 1)
            seq = [rng.choice(bg_tokens) for _ in range(seq_len)]
            seq[p : p + 2] = [a, second]
            rows.append((seq, target, rule, f"A{i}", f"{second_family}_{i}", second_family, p))
    rng.shuffle(rows)
    return DisentangledDataset(
        x=torch.tensor([r[0] for r in rows], dtype=torch.long),
        y=torch.tensor([r[1] for r in rows], dtype=torch.long),
        rule_labels=[r[2] for r in rows],
        first_identity=[r[3] for r in rows],
        second_identity=[r[4] for r in rows],
        second_family=[r[5] for r in rows],
        motif_positions=[r[6] for r in rows],
    )


def train_disentangled_model(cfg: dict, train_data: DisentangledDataset, seed: int, device: torch.device, run_stage: str):
    dcfg = cfg["stage5_disentangled"]
    model_cfg = {
        "seq_len": int(dcfg["seq_len"]),
        "d_model": 128,
        "n_heads": 4,
        "ffn_dim": 256,
        "num_experts": 4,
        "dropout": 0.0,
    }
    model = MoETinyTransformer(int(dcfg["vocab_size"]), model_cfg).to(device)
    torch.manual_seed(seed + 9001)
    rng = random.Random(seed + 9001)
    steps = int(dcfg["smoke_steps"] if run_stage == "smoke" else dcfg["steps"])
    opt = torch.optim.AdamW(model.parameters(), lr=float(dcfg["lr"]), weight_decay=float(dcfg["weight_decay"]))
    indices = list(range(train_data.x.shape[0]))
    model.train()
    for step in range(1, steps + 1):
        batch_idx = [indices[rng.randrange(len(indices))] for _ in range(int(dcfg["batch_size"]))]
        x = train_data.x[batch_idx].to(device)
        y = train_data.y[batch_idx].to(device)
        logits, _ = final_logits(model, x)
        loss = F.cross_entropy(logits, y)
        opt.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), float(dcfg["grad_clip"]))
        opt.step()
        if step == 1 or step % int(dcfg["log_every"]) == 0 or step == steps:
            print(f"stage5 seed={seed} step={step} loss={float(loss.detach().cpu()):.4f}", flush=True)
    return model, model_cfg


def eval_disentangled(model: MoETinyTransformer, data: DisentangledDataset, model_cfg: dict, seed: int, device: torch.device) -> tuple[list[dict], list[dict]]:
    batch_size = 384
    rows = []
    correct = 0
    counts = 0
    model.eval()
    with torch.no_grad():
        for start in range(0, data.x.shape[0], batch_size):
            x = data.x[start : start + batch_size].to(device)
            y = data.y[start : start + batch_size].to(device)
            logits, info = model(x, return_acts=True)
            final = logits[:, -1, :]
            pred = torch.argmax(final, dim=-1)
            correct += int((pred == y).sum().item())
            counts += y.numel()
            pred_expert = info["expert_idx"][:, -1].detach().cpu().tolist()
            for i, expert in enumerate(pred_expert):
                j = start + i
                rows.append(
                    {
                        "seed": seed,
                        "sample_id": j,
                        "rule_label": data.rule_labels[j],
                        "first_identity": data.first_identity[j],
                        "second_identity": data.second_identity[j],
                        "second_family": data.second_family[j],
                        "target_id": int(data.y[j].item()),
                        "motif_position": int(data.motif_positions[j]),
                        "expert_id": int(expert),
                    }
                )
    factors = ["rule_label", "first_identity", "second_identity", "second_family", "target_id", "motif_position"]
    experts = [int(r["expert_id"]) for r in rows]
    metric_rows = []
    for factor in factors:
        labels = [str(r[factor]) for r in rows]
        metric_rows.append(
            {
                "seed": seed,
                "factor": factor,
                "nmi": normalized_mutual_info(labels, experts),
                "majority_expert_accuracy": majority_accuracy(labels, experts),
                "conditional_entropy": conditional_entropy(labels, experts),
                "eval_accuracy": correct / counts if counts else 0.0,
                "num_records": len(rows),
            }
        )
    nmi = {r["factor"]: float(r["nmi"]) for r in metric_rows}
    metric_rows.append(
        {
            "seed": seed,
            "factor": "rule_minus_first_identity",
            "nmi": nmi.get("rule_label", 0.0) - nmi.get("first_identity", 0.0),
            "majority_expert_accuracy": "",
            "conditional_entropy": "",
            "eval_accuracy": correct / counts if counts else 0.0,
            "num_records": len(rows),
        }
    )
    return rows, metric_rows


def plot_bar(rows: list[dict], fig_dir: Path, filename: str, value: str, title: str, group_field: str = "factor") -> None:
    try:
        import matplotlib.pyplot as plt
    except Exception as exc:
        print(f"matplotlib unavailable: {exc}", flush=True)
        return
    seeds = sorted({str(r["seed"]) for r in rows}, key=int)
    groups = sorted({str(r[group_field]) for r in rows})
    fig, axes = plt.subplots(1, len(seeds), figsize=(4.2 * len(seeds), 4), squeeze=False, constrained_layout=True)
    for ax, seed in zip(axes[0], seeds):
        vals = []
        for group in groups:
            match = [r for r in rows if str(r["seed"]) == seed and str(r[group_field]) == group]
            vals.append(float(match[0][value]) if match and match[0][value] != "" else 0.0)
        ax.bar(range(len(groups)), vals)
        ax.set_title(f"seed {seed}")
        ax.set_xticks(range(len(groups)))
        ax.set_xticklabels(groups, rotation=45, ha="right", fontsize=8)
        ax.set_ylim(0, max(1.0, max(vals) * 1.1 if vals else 1.0))
    fig.suptitle(title)
    fig_dir.mkdir(parents=True, exist_ok=True)
    fig.savefig(fig_dir / filename, dpi=180)
    plt.close(fig)


def plot_heatmap(rows: list[dict], fig_dir: Path, filename: str, title: str) -> None:
    try:
        import matplotlib.pyplot as plt
    except Exception:
        return
    seeds = sorted({str(r["seed"]) for r in rows}, key=int)
    classes = CLASS_NAMES
    modes = sorted({str(r["mode"]) for r in rows if str(r["mode"]) != "natural"})
    fig, axes = plt.subplots(1, len(seeds), figsize=(4.5 * len(seeds), 4.2), squeeze=False, constrained_layout=True)
    last = None
    for ax, seed in zip(axes[0], seeds):
        mat = torch.zeros(len(classes), len(modes))
        for r in rows:
            if str(r["seed"]) == seed and str(r["mode"]) in modes:
                mat[classes.index(r["class"]), modes.index(r["mode"])] = float(r["delta_ce_vs_natural"])
        last = ax.imshow(mat.numpy(), cmap="coolwarm", aspect="auto")
        ax.set_title(f"seed {seed}")
        ax.set_xticks(range(len(modes)))
        ax.set_xticklabels(modes, rotation=45, ha="right", fontsize=7)
        ax.set_yticks(range(len(classes)))
        ax.set_yticklabels(classes if ax is axes[0][0] else [""] * len(classes), fontsize=8)
    if last is not None:
        fig.colorbar(last, ax=axes[0].tolist(), shrink=0.75, label="Delta CE")
    fig.suptitle(title)
    fig_dir.mkdir(parents=True, exist_ok=True)
    fig.savefig(fig_dir / filename, dpi=180)
    plt.close(fig)


def run(args: argparse.Namespace) -> None:
    cfg = load_json(args.config)
    if args.run_stage == "smoke":
        cfg = json.loads(json.dumps(cfg))
        cfg["seeds"] = cfg["seeds"][:1]
        cfg["audit"]["max_eval_samples_per_class"] = 128
        cfg["stage4_stress"]["train_samples_per_class"] = 256
        cfg["stage4_stress"]["eval_samples_per_class"] = 128
        cfg["stage5_disentangled"]["train_samples_per_rule"] = 256
        cfg["stage5_disentangled"]["eval_samples_per_rule"] = 128

    root = project_root()
    out_dir = resolve_output(root, cfg["output"]["result_dir"], args.run_name)
    fig_dir = resolve_output(root, cfg["output"]["figure_dir"], args.run_name)
    out_dir.mkdir(parents=True, exist_ok=True)
    fig_dir.mkdir(parents=True, exist_ok=True)
    write_json(out_dir / "resolved_config.json", cfg)

    base_cfg_path = root / cfg["base_h0521b"]["config_path"]
    base_cfg = load_json(base_cfg_path)
    base_run_dir = root / cfg["base_h0521b"]["run_dir"]
    eval_data = generate_dataset(base_cfg, int(base_cfg["seed"]), "eval", int(cfg["audit"]["max_eval_samples_per_class"]))
    train_data = generate_dataset(base_cfg, int(base_cfg["seed"]), "train", int(cfg["stage4_stress"]["train_samples_per_class"]))
    stress_eval = generate_dataset(base_cfg, int(base_cfg["seed"]), "eval", int(cfg["stage4_stress"]["eval_samples_per_class"]))

    use_cuda = torch.cuda.is_available()
    device_count = torch.cuda.device_count() if use_cuda else 0
    print(f"RUN_NAME={args.run_name} RUN_STAGE={args.run_stage} CUDA={use_cuda} CUDA_DEVICE_COUNT={device_count}", flush=True)
    seeds = [int(seed) for seed in cfg["seeds"]]

    factor_rows: list[dict] = []
    component_rows: list[dict] = []
    force_rows: list[dict] = []
    record_rows: list[dict] = []
    stress_force_rows: list[dict] = []
    disentangled_rows: list[dict] = []
    disentangled_metric_rows: list[dict] = []

    for idx, seed in enumerate(seeds):
        device = torch.device(f"cuda:{idx % device_count}" if device_count else "cpu")
        model = load_h0521b_model(seed, base_cfg, base_run_dir, device)
        bundle = collect_audit_bundle(model, eval_data, base_cfg, seed, device)
        record_rows.extend(bundle.records)
        factor_rows.extend(factor_metrics(bundle, seed))
        component_rows.extend(component_metrics(bundle, model, seed))
        force_rows.extend(evaluate_force_route(model, eval_data, base_cfg, device, seed, "existing_h0521b"))

        if cfg["stage4_stress"].get("enabled", True):
            for residual_scale in cfg["stage4_stress"]["residual_scales"]:
                stress_model = train_stress_model(cfg | {"data": base_cfg["data"], "model": base_cfg["model"]}, train_data, seed, device, float(residual_scale), args.run_stage)
                rows = evaluate_force_route(stress_model, stress_eval, base_cfg, device, seed, f"stress_residual_{residual_scale}")
                for row in rows:
                    row["residual_scale"] = residual_scale
                stress_force_rows.extend(rows)

        if cfg["stage5_disentangled"].get("enabled", True):
            dcfg = cfg["stage5_disentangled"]
            samples_train = int(dcfg["smoke_samples_per_rule"] if args.run_stage == "smoke" else dcfg["train_samples_per_rule"])
            samples_eval = int(dcfg["smoke_samples_per_rule"] if args.run_stage == "smoke" else dcfg["eval_samples_per_rule"])
            dtrain = make_disentangled_dataset(cfg, seed, "train", samples_train)
            deval = make_disentangled_dataset(cfg, seed, "eval", samples_eval)
            dmodel, dmodel_cfg = train_disentangled_model(cfg, dtrain, seed, device, args.run_stage)
            rows, metrics = eval_disentangled(dmodel, deval, dmodel_cfg, seed, device)
            disentangled_rows.extend(rows)
            disentangled_metric_rows.extend(metrics)

    write_csv(out_dir / "stage1_factor_records.csv", record_rows)
    write_csv(out_dir / "stage1_factor_metrics.csv", factor_rows)
    write_csv(out_dir / "stage2_component_metrics.csv", component_rows)
    write_csv(out_dir / "stage3_force_route_delta_ce.csv", force_rows)
    write_csv(out_dir / "stage4_stress_force_route_delta_ce.csv", stress_force_rows)
    write_csv(out_dir / "stage5_disentangled_records.csv", disentangled_rows)
    write_csv(out_dir / "stage5_disentangled_metrics.csv", disentangled_metric_rows)

    plot_bar(factor_rows, fig_dir, "stage1_factor_nmi_by_seed.png", "nmi", "Stage 1: NMI(factor, expert_id)")
    plot_bar(factor_rows, fig_dir, "stage1_factor_logit_r2_by_seed.png", "router_logit_r2", "Stage 1: router-logit R2 by factor")
    plot_bar(component_rows, fig_dir, "stage2_component_flip_rate_by_seed.png", "flip_rate", "Stage 2: route flip rate after component removal", "component")
    plot_heatmap(force_rows, fig_dir, "stage3_force_route_delta_ce.png", "Stage 3: forced routing Delta CE")
    plot_heatmap(stress_force_rows, fig_dir, "stage4_stress_force_route_delta_ce.png", "Stage 4: stress variant forced routing Delta CE")
    plot_bar(disentangled_metric_rows, fig_dir, "stage5_disentangled_nmi_by_seed.png", "nmi", "Stage 5: factor NMI on disentangled task")

    summary = {
        "run_name": args.run_name,
        "stage": args.stage,
        "variant": args.variant,
        "run_stage": args.run_stage,
        "result_dir": str(out_dir),
        "figure_dir": str(fig_dir),
        "seeds": seeds,
        "stages": ["stage1_factor_audit", "stage2_component_decomposition", "stage3_route_override", "stage4_expert_path_stress", "stage5_disentangled_task"],
    }
    write_json(out_dir / "run_summary.json", summary)
    print(json.dumps(summary, indent=2), flush=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--stage", default="h0522_router_factor_audit_seq32")
    parser.add_argument("--run-name", required=True)
    parser.add_argument("--variant", default="all_stages_seq32")
    parser.add_argument("--run-stage", choices=["smoke", "full"], default="full")
    run(parser.parse_args())


if __name__ == "__main__":
    main()
