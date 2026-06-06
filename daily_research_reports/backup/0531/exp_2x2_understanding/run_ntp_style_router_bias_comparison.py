from __future__ import annotations

import csv
from pathlib import Path

import torch
import torch.nn.functional as F

from run_ntp_style_no_router_bias_audit import NoBiasTop1NTPModel
from run_ntp_style_top1_audit import FEATURES, TARGETS, Top1NTPModel, nmi_from_counts


ROOT = Path(__file__).resolve().parent
TABLE_PATH = ROOT / "tables" / "ntp_style_router_bias_comparison.csv"
NOTE_PATH = ROOT / "notes" / "ntp_style_router_bias_comparison.md"

CONDITIONS = [
    "ntp_known_good",
    "ntp_no_router_prior",
    "ntp_no_prior_no_expert_advantage",
]
SEEDS = list(range(10))


def eval_model(model: torch.nn.Module) -> dict[str, float | int | str]:
    probs = []
    top1 = []
    losses = []
    correct = []
    with torch.no_grad():
        for i, h in enumerate(FEATURES):
            logits, p, expert_id, _ = model.forward_one(h)
            probs.append(p)
            top1.append(expert_id)
            losses.append(float(F.cross_entropy(logits.unsqueeze(0), TARGETS[i].unsqueeze(0)).item()))
            correct.append(1.0 if int(torch.argmax(logits).item()) == int(TARGETS[i]) else 0.0)
    counts = torch.zeros((2, 2), dtype=torch.float32)
    counts[0, top1[0]] += 1.0
    counts[1, top1[1]] += 1.0
    return {
        "top1_A": top1[0],
        "top1_B": top1[1],
        "pattern": "split" if top1[0] != top1[1] else "collapsed",
        "NMI": nmi_from_counts(counts),
        "selected_gate_A": float(probs[0][top1[0]]),
        "selected_gate_B": float(probs[1][top1[1]]),
        "ce_loss": sum(losses) / len(losses),
        "token_acc": sum(correct) / len(correct),
    }


def train_to_final(model: torch.nn.Module) -> None:
    optimizer = torch.optim.Adam(model.parameters(), lr=0.05)
    for _ in range(300):
        optimizer.zero_grad(set_to_none=True)
        losses = []
        for i, h in enumerate(FEATURES):
            logits, _, _, _ = model.forward_one(h)
            losses.append(F.cross_entropy(logits.unsqueeze(0), TARGETS[i].unsqueeze(0)))
        torch.stack(losses).mean().backward()
        optimizer.step()


def run() -> list[dict[str, float | int | str]]:
    rows: list[dict[str, float | int | str]] = []
    for bias_mode, cls in [("with_bias", Top1NTPModel), ("no_bias", NoBiasTop1NTPModel)]:
        for condition in CONDITIONS:
            for seed in SEEDS:
                model = cls(condition, seed)
                initial = eval_model(model)
                train_to_final(model)
                final = eval_model(model)
                rows.append(
                    {
                        "bias_mode": bias_mode,
                        "condition": condition,
                        "seed": seed,
                        "initial_top1_A": initial["top1_A"],
                        "initial_top1_B": initial["top1_B"],
                        "initial_pattern": initial["pattern"],
                        "initial_NMI": initial["NMI"],
                        "final_top1_A": final["top1_A"],
                        "final_top1_B": final["top1_B"],
                        "final_pattern": final["pattern"],
                        "final_NMI": final["NMI"],
                        "final_selected_gate_A": final["selected_gate_A"],
                        "final_selected_gate_B": final["selected_gate_B"],
                        "final_ce_loss": final["ce_loss"],
                        "final_token_acc": final["token_acc"],
                    }
                )
    return rows


def write_outputs(rows: list[dict[str, float | int | str]]) -> None:
    TABLE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with TABLE_PATH.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    NOTE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with NOTE_PATH.open("w", encoding="utf-8") as f:
        f.write("# Router Bias Comparison\n\n")
        f.write("Same conditions, seeds 0-9, 300 training steps.\n\n")
        for bias_mode in ["with_bias", "no_bias"]:
            f.write(f"## {bias_mode}\n\n")
            for condition in CONDITIONS:
                subset = [
                    r for r in rows if r["bias_mode"] == bias_mode and r["condition"] == condition
                ]
                init_split = sum(1 for r in subset if r["initial_pattern"] == "split")
                final_split = sum(1 for r in subset if r["final_pattern"] == "split")
                mean_nmi = sum(float(r["final_NMI"]) for r in subset) / len(subset)
                f.write(
                    f"- {condition}: initial split {init_split}/10, "
                    f"final split {final_split}/10, mean final NMI {mean_nmi:.3f}\n"
                )
            f.write("\n")


def main() -> None:
    rows = run()
    write_outputs(rows)
    print(NOTE_PATH.read_text(encoding="utf-8"))
    print("CSV:", TABLE_PATH)


if __name__ == "__main__":
    main()
