from __future__ import annotations

import csv
from pathlib import Path

import matplotlib.pyplot as plt
import torch
import torch.nn.functional as F

from run_ntp_style_top1_audit import FEATURES, TARGETS, Top1NTPModel, nmi_from_counts


ROOT = Path(__file__).resolve().parent
TABLE_PATH = ROOT / "tables" / "ntp_style_success_dynamics_audit.csv"
FIG_PATH = ROOT / "figures" / "ntp_style_success_dynamics_audit.png"
NOTE_PATH = ROOT / "notes" / "ntp_style_success_dynamics_audit.md"

CONDITIONS = ["ntp_no_router_prior", "ntp_no_prior_no_expert_advantage"]
SEEDS = [2]
CHECKPOINTS = {0, 10, 50, 100, 200, 300}


def forced_ce(model: Top1NTPModel, feature_id: int, expert_id: int) -> float:
    h = FEATURES[feature_id]
    target = TARGETS[feature_id].unsqueeze(0)
    with torch.no_grad():
        expert_out = model.experts[expert_id](h)
        logits = model.lm_head(expert_out)
        ce = F.cross_entropy(logits.unsqueeze(0), target)
    return float(ce.item())


def route_metrics(model: Top1NTPModel) -> dict[str, float | int]:
    with torch.no_grad():
        logits_a = model.router(FEATURES[0])
        logits_b = model.router(FEATURES[1])
        probs_a = torch.softmax(logits_a, dim=-1)
        probs_b = torch.softmax(logits_b, dim=-1)
        top1_a = int(torch.argmax(probs_a).item())
        top1_b = int(torch.argmax(probs_b).item())

    counts = torch.zeros((2, 2), dtype=torch.float32)
    counts[0, top1_a] += 1.0
    counts[1, top1_b] += 1.0

    selected_gate_a = float(probs_a[top1_a].item())
    selected_gate_b = float(probs_b[top1_b].item())
    selected_logit_margin_a = float((logits_a[top1_a] - logits_a[1 - top1_a]).item())
    selected_logit_margin_b = float((logits_b[top1_b] - logits_b[1 - top1_b]).item())

    ce_a_e0 = forced_ce(model, 0, 0)
    ce_a_e1 = forced_ce(model, 0, 1)
    ce_b_e0 = forced_ce(model, 1, 0)
    ce_b_e1 = forced_ce(model, 1, 1)

    return {
        "top1_A": top1_a,
        "top1_B": top1_b,
        "NMI": nmi_from_counts(counts),
        "logit_A_E0": float(logits_a[0].item()),
        "logit_A_E1": float(logits_a[1].item()),
        "logit_B_E0": float(logits_b[0].item()),
        "logit_B_E1": float(logits_b[1].item()),
        "p_A_E0": float(probs_a[0].item()),
        "p_A_E1": float(probs_a[1].item()),
        "p_B_E0": float(probs_b[0].item()),
        "p_B_E1": float(probs_b[1].item()),
        "selected_gate_A": selected_gate_a,
        "selected_gate_B": selected_gate_b,
        "selected_logit_margin_A": selected_logit_margin_a,
        "selected_logit_margin_B": selected_logit_margin_b,
        "CE_A_E0": ce_a_e0,
        "CE_A_E1": ce_a_e1,
        "CE_B_E0": ce_b_e0,
        "CE_B_E1": ce_b_e1,
        "CE_A_selected": ce_a_e0 if top1_a == 0 else ce_a_e1,
        "CE_A_unselected": ce_a_e1 if top1_a == 0 else ce_a_e0,
        "CE_B_selected": ce_b_e0 if top1_b == 0 else ce_b_e1,
        "CE_B_unselected": ce_b_e1 if top1_b == 0 else ce_b_e0,
    }


def train_step(model: Top1NTPModel, optimizer: torch.optim.Optimizer) -> tuple[float, float]:
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


def run_audit() -> list[dict[str, float | int | str]]:
    rows: list[dict[str, float | int | str]] = []
    for condition in CONDITIONS:
        for seed in SEEDS:
            model = Top1NTPModel(condition, seed)
            optimizer = torch.optim.Adam(model.parameters(), lr=0.05)
            update_norm_e0 = 0.0
            update_norm_e1 = 0.0
            initial_top1: tuple[int, int] | None = None

            for step in range(301):
                if step in CHECKPOINTS:
                    metrics = route_metrics(model)
                    if initial_top1 is None:
                        initial_top1 = (int(metrics["top1_A"]), int(metrics["top1_B"]))
                    top1_stable = (
                        int(metrics["top1_A"]) == initial_top1[0]
                        and int(metrics["top1_B"]) == initial_top1[1]
                    )
                    rows.append(
                        {
                            "condition": condition,
                            "seed": seed,
                            "step": step,
                            **metrics,
                            "CE_gap_A_selected_minus_unselected": float(metrics["CE_A_selected"])
                            - float(metrics["CE_A_unselected"]),
                            "CE_gap_B_selected_minus_unselected": float(metrics["CE_B_selected"])
                            - float(metrics["CE_B_unselected"]),
                            "update_norm_E0": update_norm_e0,
                            "update_norm_E1": update_norm_e1,
                            "top1_stable_from_step0": int(top1_stable),
                        }
                    )

                if step == 300:
                    break
                update_norm_e0, update_norm_e1 = train_step(model, optimizer)
    return rows


def write_csv(rows: list[dict[str, float | int | str]]) -> None:
    TABLE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with TABLE_PATH.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def save_figure(rows: list[dict[str, float | int | str]]) -> None:
    FIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    ax_margin, ax_prob, ax_ce, ax_update = axes.flatten()

    for condition in CONDITIONS:
        seed_rows = [r for r in rows if r["condition"] == condition]
        steps = [int(r["step"]) for r in seed_rows]
        label = condition.replace("ntp_", "")

        ax_margin.plot(
            steps,
            [float(r["selected_logit_margin_A"]) for r in seed_rows],
            marker="o",
            label=f"{label} A",
        )
        ax_margin.plot(
            steps,
            [float(r["selected_logit_margin_B"]) for r in seed_rows],
            marker="x",
            linestyle="--",
            label=f"{label} B",
        )
        ax_prob.plot(
            steps,
            [float(r["selected_gate_A"]) for r in seed_rows],
            marker="o",
            label=f"{label} A",
        )
        ax_prob.plot(
            steps,
            [float(r["selected_gate_B"]) for r in seed_rows],
            marker="x",
            linestyle="--",
            label=f"{label} B",
        )
        ax_ce.plot(
            steps,
            [float(r["CE_gap_A_selected_minus_unselected"]) for r in seed_rows],
            marker="o",
            label=f"{label} A",
        )
        ax_ce.plot(
            steps,
            [float(r["CE_gap_B_selected_minus_unselected"]) for r in seed_rows],
            marker="x",
            linestyle="--",
            label=f"{label} B",
        )
        ax_update.plot(
            steps,
            [float(r["update_norm_E0"]) for r in seed_rows],
            marker="o",
            label=f"{label} E0",
        )
        ax_update.plot(
            steps,
            [float(r["update_norm_E1"]) for r in seed_rows],
            marker="x",
            linestyle="--",
            label=f"{label} E1",
        )

    ax_margin.set_title("selected logit margin")
    ax_prob.set_title("selected gate probability")
    ax_ce.set_title("CE selected - unselected")
    ax_update.set_title("expert update norm")
    ax_ce.axhline(0.0, color="black", linewidth=1)
    ax_margin.axhline(0.0, color="black", linewidth=1)

    for ax in axes.flatten():
        ax.set_xlabel("step")
        ax.grid(alpha=0.25)
        ax.legend(fontsize=7)

    fig.tight_layout()
    fig.savefig(FIG_PATH, dpi=180)
    plt.close(fig)


def write_note(rows: list[dict[str, float | int | str]]) -> None:
    NOTE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with NOTE_PATH.open("w", encoding="utf-8") as f:
        f.write("# NTP-Style Success Dynamics Audit\n\n")
        f.write("Scope: success seed 2 for no-router-prior and no-prior/no-expert-advantage.\n\n")
        for condition in CONDITIONS:
            seed_rows = [r for r in rows if r["condition"] == condition]
            first = seed_rows[0]
            final = seed_rows[-1]
            f.write(
                f"- {condition}: "
                f"top1 step0=({first['top1_A']},{first['top1_B']}), "
                f"top1 step300=({final['top1_A']},{final['top1_B']}), "
                f"NMI_final={float(final['NMI']):.1f}, "
                f"gate_final=({float(final['selected_gate_A']):.3f}, "
                f"{float(final['selected_gate_B']):.3f}), "
                f"CE_gap_final=({float(final['CE_gap_A_selected_minus_unselected']):.3f}, "
                f"{float(final['CE_gap_B_selected_minus_unselected']):.3f}), "
                f"stable={int(final['top1_stable_from_step0'])}\n"
            )


def main() -> None:
    rows = run_audit()
    write_csv(rows)
    save_figure(rows)
    write_note(rows)
    print("Wrote success dynamics audit artifacts:")
    print(TABLE_PATH)
    print(FIG_PATH)
    print(NOTE_PATH)


if __name__ == "__main__":
    main()
