from __future__ import annotations

import csv
from pathlib import Path

import matplotlib.pyplot as plt
import torch
import torch.nn.functional as F


ROOT = Path(__file__).resolve().parent
FIG_DIR = ROOT / "figures" / "ntp_style"
TABLE_DIR = ROOT / "tables" / "ntp_style"
NOTE_DIR = ROOT / "notes" / "ntp_style"

FEATURES = torch.eye(2, dtype=torch.float32)
TARGETS = torch.tensor([0, 1], dtype=torch.long)


def nmi_from_counts(counts: torch.Tensor) -> float:
    total = counts.sum().item()
    if total == 0:
        return 0.0
    joint = counts / total
    row = joint.sum(dim=1, keepdim=True)
    col = joint.sum(dim=0, keepdim=True)

    mi = 0.0
    for i in range(2):
        for j in range(2):
            if joint[i, j] > 0 and row[i, 0] > 0 and col[0, j] > 0:
                mi += (joint[i, j] * torch.log(joint[i, j] / (row[i, 0] * col[0, j]))).item()

    h_row = -(row[row > 0] * torch.log(row[row > 0])).sum().item()
    h_col = -(col[col > 0] * torch.log(col[col > 0])).sum().item()
    if h_row + h_col == 0:
        return 0.0
    return 2.0 * mi / (h_row + h_col)


class Top1NTPModel(torch.nn.Module):
    def __init__(self, condition: str, seed: int):
        super().__init__()
        torch.manual_seed(seed)

        self.condition = condition
        self.router = torch.nn.Linear(2, 2)
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
            self.router.bias.copy_(0.005 * torch.randn_like(self.router.bias))

    def forward_one(self, h: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor, int, torch.Tensor]:
        router_logits = self.router(h)
        probs = torch.softmax(router_logits, dim=-1)
        top1 = int(torch.argmax(probs).item())
        selected_gate = probs[top1]
        expert_out = self.experts[top1](h)
        moe_out = selected_gate * expert_out
        vocab_logits = self.lm_head(moe_out)
        return vocab_logits, probs, top1, selected_gate


def evaluate(model: Top1NTPModel, condition: str, seed: int, step: int) -> dict[str, float | int | str]:
    model.eval()
    probs_by_feature = []
    top1_assignments = []
    selected_gates = []
    losses = []
    correct = []

    with torch.no_grad():
        for i, h in enumerate(FEATURES):
            logits, probs, top1, selected_gate = model.forward_one(h)
            loss = F.cross_entropy(logits.unsqueeze(0), TARGETS[i].unsqueeze(0))
            pred = int(torch.argmax(logits).item())
            probs_by_feature.append(probs.detach())
            top1_assignments.append(top1)
            selected_gates.append(float(selected_gate.item()))
            losses.append(float(loss.item()))
            correct.append(1.0 if pred == int(TARGETS[i].item()) else 0.0)

    heatmap = torch.stack(probs_by_feature)
    counts = torch.zeros((2, 2), dtype=torch.float32)
    for feature_id, expert_id in enumerate(top1_assignments):
        counts[feature_id, expert_id] += 1.0

    direct_acc = 0.5 * ((top1_assignments[0] == 0) + (top1_assignments[1] == 1))
    swapped_acc = 0.5 * ((top1_assignments[0] == 1) + (top1_assignments[1] == 0))
    assignment_accuracy = max(direct_acc, swapped_acc)

    row_margin_a = abs(float(heatmap[0, 0] - heatmap[0, 1]))
    row_margin_b = abs(float(heatmap[1, 0] - heatmap[1, 1]))
    mean_route_margin = 0.5 * (row_margin_a + row_margin_b)
    max_usage = float(heatmap.mean(dim=0).max().item())
    mean_entropy = float((-(heatmap.clamp_min(1e-12) * heatmap.clamp_min(1e-12).log()).sum(dim=1)).mean().item())
    pattern = "separated" if top1_assignments[0] != top1_assignments[1] else "collapsed"

    return {
        "condition": condition,
        "seed": seed,
        "step": step,
        "top1_A": top1_assignments[0],
        "top1_B": top1_assignments[1],
        "p_e0_given_A": float(heatmap[0, 0].item()),
        "p_e1_given_A": float(heatmap[0, 1].item()),
        "p_e0_given_B": float(heatmap[1, 0].item()),
        "p_e1_given_B": float(heatmap[1, 1].item()),
        "mean_selected_gate": sum(selected_gates) / len(selected_gates),
        "mean_route_margin": mean_route_margin,
        "nmi": nmi_from_counts(counts),
        "assignment_accuracy": float(assignment_accuracy),
        "mean_entropy": mean_entropy,
        "max_expert_usage": max_usage,
        "ce_loss": sum(losses) / len(losses),
        "per_feature_accuracy": sum(correct) / len(correct),
        "pattern": pattern,
    }


def train_condition(condition: str, seeds: list[int], steps: int = 300, lr: float = 0.05) -> list[dict[str, float | int | str]]:
    checkpoints = {0, 10, 50, 100, 200, 300}
    rows: list[dict[str, float | int | str]] = []

    for seed in seeds:
        model = Top1NTPModel(condition, seed)
        optimizer = torch.optim.Adam(model.parameters(), lr=lr)

        for step in range(steps + 1):
            if step in checkpoints:
                rows.append(evaluate(model, condition, seed, step))

            if step == steps:
                break

            model.train()
            optimizer.zero_grad()
            losses = []
            for i, h in enumerate(FEATURES):
                logits, _, _, _ = model.forward_one(h)
                losses.append(F.cross_entropy(logits.unsqueeze(0), TARGETS[i].unsqueeze(0)))
            loss = torch.stack(losses).mean()
            loss.backward()
            optimizer.step()

    return rows


def write_csv(path: Path, rows: list[dict[str, float | int | str]]) -> None:
    if not rows:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def save_heatmap(row: dict[str, float | int | str]) -> None:
    condition_dir = FIG_DIR / str(row["condition"])
    condition_dir.mkdir(parents=True, exist_ok=True)
    heatmap = torch.tensor(
        [
            [row["p_e0_given_A"], row["p_e1_given_A"]],
            [row["p_e0_given_B"], row["p_e1_given_B"]],
        ],
        dtype=torch.float32,
    )
    fig, ax = plt.subplots(figsize=(3.2, 2.8))
    im = ax.imshow(heatmap.numpy(), vmin=0, vmax=1, cmap="Blues")
    ax.set_xticks([0, 1], labels=["E0", "E1"])
    ax.set_yticks([0, 1], labels=["A_ctx", "B_ctx"])
    ax.set_title(f"{row['condition']} seed {row['seed']} step {row['step']}")
    for i in range(2):
        for j in range(2):
            ax.text(j, i, f"{float(heatmap[i, j]):.2f}", ha="center", va="center")
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    fig.tight_layout()
    fig.savefig(condition_dir / f"heatmap_seed{row['seed']}_step{row['step']}.png", dpi=160)
    plt.close(fig)


def save_trajectory(condition: str, rows: list[dict[str, float | int | str]]) -> None:
    condition_dir = FIG_DIR / condition
    condition_dir.mkdir(parents=True, exist_ok=True)

    for seed in sorted({int(r["seed"]) for r in rows}):
        seed_rows = [r for r in rows if int(r["seed"]) == seed]
        steps = [int(r["step"]) for r in seed_rows]
        margins = [float(r["mean_route_margin"]) for r in seed_rows]
        losses = [float(r["ce_loss"]) for r in seed_rows]
        accs = [float(r["per_feature_accuracy"]) for r in seed_rows]

        fig, axes = plt.subplots(1, 3, figsize=(9.6, 2.8))
        axes[0].plot(steps, margins, marker="o")
        axes[0].set_title("route margin")
        axes[0].set_xlabel("step")
        axes[0].set_ylim(0, 1)
        axes[1].plot(steps, losses, marker="o")
        axes[1].set_title("CE loss")
        axes[1].set_xlabel("step")
        axes[2].plot(steps, accs, marker="o")
        axes[2].set_title("next-token acc")
        axes[2].set_xlabel("step")
        axes[2].set_ylim(0, 1.05)
        fig.suptitle(f"{condition} seed {seed}")
        fig.tight_layout()
        fig.savefig(condition_dir / f"trajectory_seed{seed}.png", dpi=160)
        plt.close(fig)


def write_observations(condition: str, final_rows: list[dict[str, float | int | str]]) -> None:
    condition_dir = NOTE_DIR / condition
    condition_dir.mkdir(parents=True, exist_ok=True)
    separated = sum(1 for r in final_rows if r["pattern"] == "separated")
    mean_nmi = sum(float(r["nmi"]) for r in final_rows) / len(final_rows)
    mean_loss = sum(float(r["ce_loss"]) for r in final_rows) / len(final_rows)
    mean_acc = sum(float(r["per_feature_accuracy"]) for r in final_rows) / len(final_rows)

    with (condition_dir / "run_observations.md").open("w", encoding="utf-8") as f:
        f.write(f"# {condition} Observations\n\n")
        f.write("NTP-style top-1 sparse audit with fixed orthogonal hidden states.\n\n")
        f.write(f"Separated final top-1 routing: {separated}/{len(final_rows)} seeds.\n")
        f.write(f"Mean final NMI: {mean_nmi:.4f}.\n")
        f.write(f"Mean final CE loss: {mean_loss:.6f}.\n")
        f.write(f"Mean final per-feature accuracy: {mean_acc:.4f}.\n\n")
        for row in final_rows:
            f.write(
                f"- seed {row['seed']}: pattern={row['pattern']}, "
                f"top1_A={row['top1_A']}, top1_B={row['top1_B']}, "
                f"margin={float(row['mean_route_margin']):.4f}, "
                f"NMI={float(row['nmi']):.4f}, "
                f"route_acc={float(row['assignment_accuracy']):.4f}, "
                f"CE={float(row['ce_loss']):.6f}, "
                f"token_acc={float(row['per_feature_accuracy']):.4f}\n"
            )


def main() -> None:
    conditions = [
        "ntp_known_good",
        "ntp_no_router_prior",
        "ntp_no_prior_no_expert_advantage",
    ]
    seeds = [0, 1, 2]

    all_rows: list[dict[str, float | int | str]] = []
    final_summary: list[dict[str, float | int | str]] = []

    for condition in conditions:
        rows = train_condition(condition, seeds)
        all_rows.extend(rows)
        final_rows = [r for r in rows if int(r["step"]) == 300]
        final_summary.extend(final_rows)
        write_csv(TABLE_DIR / condition / "metrics_by_checkpoint.csv", rows)
        write_csv(TABLE_DIR / condition / "seed_checkpoint_summary.csv", final_rows)
        write_observations(condition, final_rows)
        for row in rows:
            if int(row["step"]) in {0, 100, 300}:
                save_heatmap(row)
        save_trajectory(condition, rows)

    write_csv(TABLE_DIR / "all_conditions_by_checkpoint.csv", all_rows)
    write_csv(TABLE_DIR / "all_conditions_final_summary.csv", final_summary)

    print("Wrote NTP-style top-1 audit artifacts to:")
    print(TABLE_DIR)
    print(FIG_DIR)
    print(NOTE_DIR)


if __name__ == "__main__":
    main()
