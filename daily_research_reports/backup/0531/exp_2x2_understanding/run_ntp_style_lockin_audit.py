from __future__ import annotations

import csv
from pathlib import Path

import matplotlib.pyplot as plt
import torch
import torch.nn.functional as F

from run_ntp_style_top1_audit import FEATURES, TARGETS, Top1NTPModel, nmi_from_counts


ROOT = Path(__file__).resolve().parent
TABLE_PATH = ROOT / "tables" / "ntp_style_lockin_audit.csv"
FIG_PATH = ROOT / "figures" / "ntp_style_lockin_audit.png"
NOTE_PATH = ROOT / "notes" / "ntp_style_lockin_audit.md"

CONDITIONS = ["ntp_no_router_prior", "ntp_no_prior_no_expert_advantage"]
SEEDS = [0, 1, 2]
CHECKPOINTS = {0, 10, 50, 100, 200, 300}


def selected_feature_ce(model: Top1NTPModel, feature_id: int, expert_id: int) -> float:
    h = FEATURES[feature_id]
    target = TARGETS[feature_id].unsqueeze(0)
    with torch.no_grad():
        expert_out = model.experts[expert_id](h)
        logits = model.lm_head(expert_out)
        ce = F.cross_entropy(logits.unsqueeze(0), target)
    return float(ce.item())


def route_state(model: Top1NTPModel) -> dict[str, float | int]:
    probs_by_feature = []
    top1 = []
    selected = []
    for h in FEATURES:
        with torch.no_grad():
            _, probs, expert_id, selected_gate = model.forward_one(h)
        probs_by_feature.append(probs.detach())
        top1.append(expert_id)
        selected.append(float(selected_gate.item()))

    counts = torch.zeros((2, 2), dtype=torch.float32)
    for feature_id, expert_id in enumerate(top1):
        counts[feature_id, expert_id] += 1.0
    usage_e0 = float((top1[0] == 0) + (top1[1] == 0)) / 2.0
    usage_e1 = 1.0 - usage_e0

    return {
        "top1_A": top1[0],
        "top1_B": top1[1],
        "NMI": nmi_from_counts(counts),
        "selected_gate_A": selected[0],
        "selected_gate_B": selected[1],
        "expert_usage_E0": usage_e0,
        "expert_usage_E1": usage_e1,
    }


def router_grad_norm(model: Top1NTPModel) -> float:
    model.zero_grad(set_to_none=True)
    losses = []
    for i, h in enumerate(FEATURES):
        logits, _, _, _ = model.forward_one(h)
        losses.append(F.cross_entropy(logits.unsqueeze(0), TARGETS[i].unsqueeze(0)))
    loss = torch.stack(losses).mean()
    loss.backward()
    norm_sq = 0.0
    for p in model.router.parameters():
        if p.grad is not None:
            norm_sq += float(torch.sum(p.grad.detach() ** 2).item())
    model.zero_grad(set_to_none=True)
    return norm_sq**0.5


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


def audit_row(
    condition: str,
    seed: int,
    step: int,
    model: Top1NTPModel,
    update_norm_e0: float,
    update_norm_e1: float,
) -> dict[str, float | int | str]:
    state = route_state(model)
    top1_a = int(state["top1_A"])
    top1_b = int(state["top1_B"])

    ce_a_e0 = selected_feature_ce(model, 0, 0)
    ce_a_e1 = selected_feature_ce(model, 0, 1)
    ce_b_e0 = selected_feature_ce(model, 1, 0)
    ce_b_e1 = selected_feature_ce(model, 1, 1)

    return {
        "condition": condition,
        "seed": seed,
        "step": step,
        "top1_A": top1_a,
        "top1_B": top1_b,
        "NMI": state["NMI"],
        "selected_gate_A": state["selected_gate_A"],
        "selected_gate_B": state["selected_gate_B"],
        "expert_usage_E0": state["expert_usage_E0"],
        "expert_usage_E1": state["expert_usage_E1"],
        "update_norm_E0": update_norm_e0,
        "update_norm_E1": update_norm_e1,
        "router_grad_norm": router_grad_norm(model),
        "CE_A_E0": ce_a_e0,
        "CE_A_E1": ce_a_e1,
        "CE_B_E0": ce_b_e0,
        "CE_B_E1": ce_b_e1,
        "interpretation_tag": "pending",
    }


def tag_seed(rows: list[dict[str, float | int | str]]) -> str:
    by_step = {int(r["step"]): r for r in rows}
    early = by_step.get(0) or by_step.get(10)
    final = by_step[max(by_step)]
    early_collapsed = int(early["top1_A"]) == int(early["top1_B"])
    final_collapsed = int(final["top1_A"]) == int(final["top1_B"])
    final_nmi = float(final["NMI"])
    final_conf = 0.5 * (float(final["selected_gate_A"]) + float(final["selected_gate_B"]))

    if early_collapsed and final_collapsed and final_nmi == 0.0 and final_conf > 0.9:
        return "early_lock_in"
    if (not early_collapsed) and final_collapsed:
        return "optimization_drift"
    if final_collapsed and final_nmi == 0.0:
        return "task_shortcut"
    if (not final_collapsed) and final_nmi == 1.0:
        return "success_control"
    return "insufficient_evidence"


def run_audit() -> list[dict[str, float | int | str]]:
    rows: list[dict[str, float | int | str]] = []
    for condition in CONDITIONS:
        for seed in SEEDS:
            model = Top1NTPModel(condition, seed)
            optimizer = torch.optim.Adam(model.parameters(), lr=0.05)
            seed_rows: list[dict[str, float | int | str]] = []
            update_norm_e0 = 0.0
            update_norm_e1 = 0.0

            for step in range(301):
                if step in CHECKPOINTS:
                    seed_rows.append(
                        audit_row(condition, seed, step, model, update_norm_e0, update_norm_e1)
                    )
                if step == 300:
                    break
                update_norm_e0, update_norm_e1 = train_step(model, optimizer)

            tag = tag_seed(seed_rows)
            for row in seed_rows:
                row["interpretation_tag"] = tag
            rows.extend(seed_rows)
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
    ax_nmi, ax_gate, ax_usage, ax_ce = axes.flatten()

    for condition in CONDITIONS:
        for seed in SEEDS:
            seed_rows = [
                r for r in rows if r["condition"] == condition and int(r["seed"]) == seed
            ]
            steps = [int(r["step"]) for r in seed_rows]
            label = f"{condition.replace('ntp_', '')}/s{seed}"
            ax_nmi.plot(steps, [float(r["NMI"]) for r in seed_rows], marker="o", label=label)
            ax_gate.plot(
                steps,
                [float(r["selected_gate_A"]) for r in seed_rows],
                marker="o",
                linestyle="-",
                label=f"{label} A",
            )
            ax_gate.plot(
                steps,
                [float(r["selected_gate_B"]) for r in seed_rows],
                marker="x",
                linestyle="--",
                label=f"{label} B",
            )
            ax_usage.plot(
                steps,
                [float(r["expert_usage_E0"]) for r in seed_rows],
                marker="o",
                linestyle="-",
                label=f"{label} E0",
            )
            ax_usage.plot(
                steps,
                [float(r["expert_usage_E1"]) for r in seed_rows],
                marker="x",
                linestyle="--",
                label=f"{label} E1",
            )

            gaps_a = []
            gaps_b = []
            for r in seed_rows:
                top1_a = int(r["top1_A"])
                top1_b = int(r["top1_B"])
                ce_a_selected = float(r[f"CE_A_E{top1_a}"])
                ce_a_unselected = float(r[f"CE_A_E{1 - top1_a}"])
                ce_b_selected = float(r[f"CE_B_E{top1_b}"])
                ce_b_unselected = float(r[f"CE_B_E{1 - top1_b}"])
                gaps_a.append(ce_a_selected - ce_a_unselected)
                gaps_b.append(ce_b_selected - ce_b_unselected)
            ax_ce.plot(steps, gaps_a, marker="o", linestyle="-", label=f"{label} A")
            ax_ce.plot(steps, gaps_b, marker="x", linestyle="--", label=f"{label} B")

    ax_nmi.set_title("NMI over checkpoints")
    ax_nmi.set_ylim(-0.05, 1.05)
    ax_gate.set_title("selected gate over checkpoints")
    ax_gate.set_ylim(0.45, 1.02)
    ax_usage.set_title("top-1 expert usage")
    ax_usage.set_ylim(-0.05, 1.05)
    ax_ce.set_title("CE selected - unselected")
    ax_ce.axhline(0.0, color="black", linewidth=1)

    for ax in axes.flatten():
        ax.set_xlabel("step")
        ax.grid(alpha=0.25)

    ax_nmi.legend(fontsize=6)
    ax_gate.legend(fontsize=5, ncol=2)
    ax_usage.legend(fontsize=5, ncol=2)
    ax_ce.legend(fontsize=5, ncol=2)
    fig.tight_layout()
    fig.savefig(FIG_PATH, dpi=180)
    plt.close(fig)


def write_note(rows: list[dict[str, float | int | str]]) -> None:
    NOTE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with NOTE_PATH.open("w", encoding="utf-8") as f:
        f.write("# NTP-Style Lock-In Audit\n\n")
        f.write("Scope: existing NTP-style top-1 runs only: no-router-prior and no-prior/no-expert-advantage.\n\n")
        f.write("Main result:\n\n")
        for condition in CONDITIONS:
            for seed in SEEDS:
                seed_rows = [
                    r for r in rows if r["condition"] == condition and int(r["seed"]) == seed
                ]
                first = seed_rows[0]
                final = seed_rows[-1]
                f.write(
                    f"- {condition} seed {seed}: "
                    f"step0=({first['top1_A']},{first['top1_B']}), "
                    f"step300=({final['top1_A']},{final['top1_B']}), "
                    f"NMI_final={float(final['NMI']):.1f}, "
                    f"gate_A_final={float(final['selected_gate_A']):.3f}, "
                    f"gate_B_final={float(final['selected_gate_B']):.3f}, "
                    f"tag={final['interpretation_tag']}\n"
                )


def main() -> None:
    rows = run_audit()
    write_csv(rows)
    save_figure(rows)
    write_note(rows)
    print("Wrote lock-in audit artifacts:")
    print(TABLE_PATH)
    print(FIG_PATH)
    print(NOTE_PATH)


if __name__ == "__main__":
    main()
