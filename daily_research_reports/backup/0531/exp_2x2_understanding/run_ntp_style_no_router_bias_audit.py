from __future__ import annotations

import csv
from pathlib import Path

import matplotlib.pyplot as plt
import torch
import torch.nn.functional as F

from run_ntp_style_top1_audit import FEATURES, TARGETS, nmi_from_counts


ROOT = Path(__file__).resolve().parent
TABLE_DIR = ROOT / "tables" / "ntp_style_no_router_bias"
FIG_DIR = ROOT / "figures" / "ntp_style_no_router_bias"
NOTE_PATH = ROOT / "notes" / "ntp_style_no_router_bias_audit.md"

CONDITIONS = [
    "ntp_known_good",
    "ntp_no_router_prior",
    "ntp_no_prior_no_expert_advantage",
]
SEEDS = list(range(10))
CHECKPOINTS = {0, 10, 50, 100, 200, 300}


class NoBiasTop1NTPModel(torch.nn.Module):
    def __init__(self, condition: str, seed: int):
        super().__init__()
        torch.manual_seed(seed)

        self.condition = condition
        self.router = torch.nn.Linear(2, 2, bias=False)
        self.experts = torch.nn.ModuleList([torch.nn.Linear(2, 2), torch.nn.Linear(2, 2)])
        self.lm_head = torch.nn.Linear(2, 2)
        self.reset_parameters(condition)

    def reset_parameters(self, condition: str) -> None:
        with torch.no_grad():
            self.lm_head.weight.copy_(torch.eye(2))
            self.lm_head.bias.zero_()

            if condition in {"ntp_known_good", "ntp_no_router_prior"}:
                expert_weights = [
                    torch.tensor([[0.80, 0.00], [0.00, 0.10]], dtype=torch.float32),
                    torch.tensor([[0.10, 0.00], [0.00, 0.80]], dtype=torch.float32),
                ]
            elif condition == "ntp_no_prior_no_expert_advantage":
                expert_weights = [
                    torch.tensor([[0.45, 0.00], [0.00, 0.45]], dtype=torch.float32),
                    torch.tensor([[0.45, 0.00], [0.00, 0.45]], dtype=torch.float32),
                ]
            else:
                raise ValueError(f"unknown condition: {condition}")

            for expert, weight in zip(self.experts, expert_weights):
                expert.weight.copy_(weight + 0.015 * torch.randn_like(weight))
                expert.bias.copy_(0.005 * torch.randn_like(expert.bias))

            if condition == "ntp_known_good":
                prior = torch.tensor([[0.30, -0.30], [-0.30, 0.30]], dtype=torch.float32)
                self.router.weight.copy_(prior + 0.015 * torch.randn_like(prior))
            else:
                self.router.weight.copy_(0.015 * torch.randn_like(self.router.weight))

    def forward_one(self, h: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor, int, torch.Tensor]:
        router_logits = self.router(h)
        probs = torch.softmax(router_logits, dim=-1)
        top1 = int(torch.argmax(probs).item())
        selected_gate = probs[top1]
        expert_out = self.experts[top1](h)
        moe_out = selected_gate * expert_out
        vocab_logits = self.lm_head(moe_out)
        return vocab_logits, probs, top1, selected_gate


def forced_ce(model: NoBiasTop1NTPModel, feature_id: int, expert_id: int) -> float:
    h = FEATURES[feature_id]
    target = TARGETS[feature_id].unsqueeze(0)
    with torch.no_grad():
        expert_out = model.experts[expert_id](h)
        logits = model.lm_head(expert_out)
        ce = F.cross_entropy(logits.unsqueeze(0), target)
    return float(ce.item())


def evaluate(
    model: NoBiasTop1NTPModel,
    condition: str,
    seed: int,
    step: int,
    update_norm_e0: float,
    update_norm_e1: float,
) -> dict[str, float | int | str]:
    model.eval()
    logits = torch.stack(
        [
            model.router(FEATURES[0]).detach(),
            model.router(FEATURES[1]).detach(),
        ]
    )
    probs = torch.softmax(logits, dim=-1)
    top1_a = int(torch.argmax(probs[0]).item())
    top1_b = int(torch.argmax(probs[1]).item())

    counts = torch.zeros((2, 2), dtype=torch.float32)
    counts[0, top1_a] += 1.0
    counts[1, top1_b] += 1.0

    ce_a_e0 = forced_ce(model, 0, 0)
    ce_a_e1 = forced_ce(model, 0, 1)
    ce_b_e0 = forced_ce(model, 1, 0)
    ce_b_e1 = forced_ce(model, 1, 1)

    with torch.no_grad():
        losses = []
        correct = []
        for i, h in enumerate(FEATURES):
            vocab_logits, _, _, _ = model.forward_one(h)
            losses.append(float(F.cross_entropy(vocab_logits.unsqueeze(0), TARGETS[i].unsqueeze(0)).item()))
            correct.append(1.0 if int(torch.argmax(vocab_logits).item()) == int(TARGETS[i]) else 0.0)

    return {
        "condition": condition,
        "seed": seed,
        "step": step,
        "top1_A": top1_a,
        "top1_B": top1_b,
        "initial_or_current_pattern": "split" if top1_a != top1_b else "collapsed",
        "NMI": nmi_from_counts(counts),
        "logit_A_E0": float(logits[0, 0]),
        "logit_A_E1": float(logits[0, 1]),
        "logit_B_E0": float(logits[1, 0]),
        "logit_B_E1": float(logits[1, 1]),
        "delta_A_E1_minus_E0": float(logits[0, 1] - logits[0, 0]),
        "delta_B_E1_minus_E0": float(logits[1, 1] - logits[1, 0]),
        "p_A_E0": float(probs[0, 0]),
        "p_A_E1": float(probs[0, 1]),
        "p_B_E0": float(probs[1, 0]),
        "p_B_E1": float(probs[1, 1]),
        "selected_gate_A": float(probs[0, top1_a]),
        "selected_gate_B": float(probs[1, top1_b]),
        "CE_A_E0": ce_a_e0,
        "CE_A_E1": ce_a_e1,
        "CE_B_E0": ce_b_e0,
        "CE_B_E1": ce_b_e1,
        "CE_A_selected_minus_unselected": (ce_a_e0 - ce_a_e1) if top1_a == 0 else (ce_a_e1 - ce_a_e0),
        "CE_B_selected_minus_unselected": (ce_b_e0 - ce_b_e1) if top1_b == 0 else (ce_b_e1 - ce_b_e0),
        "update_norm_E0": update_norm_e0,
        "update_norm_E1": update_norm_e1,
        "ce_loss": sum(losses) / len(losses),
        "token_acc": sum(correct) / len(correct),
    }


def train_step(model: NoBiasTop1NTPModel, optimizer: torch.optim.Optimizer) -> tuple[float, float]:
    before_e0 = torch.cat([p.detach().flatten().clone() for p in model.experts[0].parameters()])
    before_e1 = torch.cat([p.detach().flatten().clone() for p in model.experts[1].parameters()])

    optimizer.zero_grad(set_to_none=True)
    losses = []
    for i, h in enumerate(FEATURES):
        logits, _, _, _ = model.forward_one(h)
        losses.append(F.cross_entropy(logits.unsqueeze(0), TARGETS[i].unsqueeze(0)))
    loss = torch.stack(losses).mean()
    loss.backward()
    optimizer.step()

    after_e0 = torch.cat([p.detach().flatten().clone() for p in model.experts[0].parameters()])
    after_e1 = torch.cat([p.detach().flatten().clone() for p in model.experts[1].parameters()])
    return float(torch.norm(after_e0 - before_e0).item()), float(torch.norm(after_e1 - before_e1).item())


def run() -> tuple[list[dict[str, float | int | str]], list[dict[str, float | int | str]]]:
    by_checkpoint: list[dict[str, float | int | str]] = []
    initial_rows: list[dict[str, float | int | str]] = []

    for condition in CONDITIONS:
        for seed in SEEDS:
            model = NoBiasTop1NTPModel(condition, seed)
            optimizer = torch.optim.Adam(model.parameters(), lr=0.05)
            update_norm_e0 = 0.0
            update_norm_e1 = 0.0
            initial_top1: tuple[int, int] | None = None

            for step in range(301):
                if step in CHECKPOINTS:
                    row = evaluate(model, condition, seed, step, update_norm_e0, update_norm_e1)
                    if initial_top1 is None:
                        initial_top1 = (int(row["top1_A"]), int(row["top1_B"]))
                        initial_rows.append({k: row[k] for k in row if k not in {"ce_loss", "token_acc"}})
                    row["top1_stable_from_step0"] = int(
                        int(row["top1_A"]) == initial_top1[0]
                        and int(row["top1_B"]) == initial_top1[1]
                    )
                    by_checkpoint.append(row)

                if step == 300:
                    break
                update_norm_e0, update_norm_e1 = train_step(model, optimizer)
    return by_checkpoint, initial_rows


def write_csv(path: Path, rows: list[dict[str, float | int | str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def save_figures(rows: list[dict[str, float | int | str]]) -> None:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    final_rows = [r for r in rows if int(r["step"]) == 300]
    fig, axes = plt.subplots(1, 3, figsize=(13, 3.6))

    for condition in CONDITIONS:
        cond_rows = [r for r in final_rows if r["condition"] == condition]
        seeds = [int(r["seed"]) for r in cond_rows]
        axes[0].plot(seeds, [float(r["NMI"]) for r in cond_rows], marker="o", label=condition)
        axes[1].plot(seeds, [float(r["token_acc"]) for r in cond_rows], marker="o", label=condition)
        axes[2].plot(seeds, [float(r["selected_gate_A"]) for r in cond_rows], marker="o", label=f"{condition} A")
        axes[2].plot(seeds, [float(r["selected_gate_B"]) for r in cond_rows], marker="x", linestyle="--", label=f"{condition} B")

    axes[0].set_title("final NMI by seed")
    axes[1].set_title("final token accuracy by seed")
    axes[2].set_title("final selected gate by seed")
    for ax in axes:
        ax.set_xlabel("seed")
        ax.grid(alpha=0.25)
        ax.legend(fontsize=6)
    fig.tight_layout()
    fig.savefig(FIG_DIR / "summary_by_seed.png", dpi=180)
    plt.close(fig)

    for condition in CONDITIONS:
        cond_rows = [r for r in rows if r["condition"] == condition]
        fig, axes = plt.subplots(1, 3, figsize=(13, 3.6))
        for seed in SEEDS:
            seed_rows = [r for r in cond_rows if int(r["seed"]) == seed]
            steps = [int(r["step"]) for r in seed_rows]
            axes[0].plot(steps, [float(r["NMI"]) for r in seed_rows], marker="o", label=f"s{seed}")
            axes[1].plot(steps, [float(r["selected_gate_A"]) for r in seed_rows], marker="o", label=f"s{seed} A")
            axes[1].plot(steps, [float(r["selected_gate_B"]) for r in seed_rows], marker="x", linestyle="--", label=f"s{seed} B")
            axes[2].plot(steps, [float(r["CE_A_selected_minus_unselected"]) for r in seed_rows], marker="o", label=f"s{seed} A")
            axes[2].plot(steps, [float(r["CE_B_selected_minus_unselected"]) for r in seed_rows], marker="x", linestyle="--", label=f"s{seed} B")
        axes[0].set_title("NMI trajectory")
        axes[1].set_title("selected gate trajectory")
        axes[2].set_title("CE selected - unselected")
        axes[2].axhline(0.0, color="black", linewidth=1)
        for ax in axes:
            ax.set_xlabel("step")
            ax.grid(alpha=0.25)
            ax.legend(fontsize=5, ncol=2)
        fig.suptitle(condition)
        fig.tight_layout()
        fig.savefig(FIG_DIR / f"{condition}_trajectory.png", dpi=180)
        plt.close(fig)


def write_note(rows: list[dict[str, float | int | str]]) -> None:
    NOTE_PATH.parent.mkdir(parents=True, exist_ok=True)
    final_rows = [r for r in rows if int(r["step"]) == 300]
    initial_rows = [r for r in rows if int(r["step"]) == 0]
    with NOTE_PATH.open("w", encoding="utf-8") as f:
        f.write("# NTP-Style No Router Bias Audit\n\n")
        f.write("Router uses Linear(2, 2, bias=False). Other settings are unchanged.\n\n")
        for condition in CONDITIONS:
            init = [r for r in initial_rows if r["condition"] == condition]
            final = [r for r in final_rows if r["condition"] == condition]
            init_split = sum(1 for r in init if r["initial_or_current_pattern"] == "split")
            final_split = sum(1 for r in final if r["initial_or_current_pattern"] == "split")
            mean_nmi = sum(float(r["NMI"]) for r in final) / len(final)
            mean_acc = sum(float(r["token_acc"]) for r in final) / len(final)
            f.write(
                f"- {condition}: initial split {init_split}/{len(init)}, "
                f"final split {final_split}/{len(final)}, "
                f"mean final NMI {mean_nmi:.3f}, mean token acc {mean_acc:.3f}\n"
            )
        f.write("\nSeed details:\n\n")
        for condition in CONDITIONS:
            f.write(f"## {condition}\n\n")
            for row in final:
                pass
            for row in [r for r in final_rows if r["condition"] == condition]:
                f.write(
                    f"- seed {row['seed']}: top1=({row['top1_A']},{row['top1_B']}), "
                    f"NMI={float(row['NMI']):.1f}, token_acc={float(row['token_acc']):.1f}, "
                    f"gate=({float(row['selected_gate_A']):.3f},{float(row['selected_gate_B']):.3f})\n"
                )


def main() -> None:
    rows, initial_rows = run()
    write_csv(TABLE_DIR / "by_checkpoint.csv", rows)
    write_csv(TABLE_DIR / "initial_router.csv", initial_rows)
    write_csv(TABLE_DIR / "final_summary.csv", [r for r in rows if int(r["step"]) == 300])
    save_figures(rows)
    write_note(rows)
    print("Wrote no-router-bias audit artifacts:")
    print(TABLE_DIR)
    print(FIG_DIR)
    print(NOTE_PATH)


if __name__ == "__main__":
    main()
