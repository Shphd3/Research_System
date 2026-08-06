from __future__ import annotations

import csv
from pathlib import Path

import torch

from run_ntp_style_top1_audit import FEATURES, Top1NTPModel


ROOT = Path(__file__).resolve().parent
TABLE_PATH = ROOT / "tables" / "ntp_style_initial_router_audit.csv"
NOTE_PATH = ROOT / "notes" / "ntp_style_initial_router_audit.md"

CONDITIONS = ["ntp_no_router_prior", "ntp_no_prior_no_expert_advantage"]
SEEDS = [0, 1, 2]


def audit_rows() -> list[dict[str, float | int | str]]:
    rows: list[dict[str, float | int | str]] = []
    for condition in CONDITIONS:
        for seed in SEEDS:
            model = Top1NTPModel(condition, seed)
            weight = model.router.weight.detach()
            bias = model.router.bias.detach()
            logits = torch.stack(
                [
                    model.router(FEATURES[0]).detach(),
                    model.router(FEATURES[1]).detach(),
                ]
            )
            probs = torch.softmax(logits, dim=-1)
            delta = logits[:, 1] - logits[:, 0]
            top1 = torch.argmax(probs, dim=-1)
            rows.append(
                {
                    "condition": condition,
                    "seed": seed,
                    "W_E0_A": float(weight[0, 0]),
                    "W_E0_B": float(weight[0, 1]),
                    "W_E1_A": float(weight[1, 0]),
                    "W_E1_B": float(weight[1, 1]),
                    "b_E0": float(bias[0]),
                    "b_E1": float(bias[1]),
                    "logit_A_E0": float(logits[0, 0]),
                    "logit_A_E1": float(logits[0, 1]),
                    "logit_B_E0": float(logits[1, 0]),
                    "logit_B_E1": float(logits[1, 1]),
                    "p_A_E0": float(probs[0, 0]),
                    "p_A_E1": float(probs[0, 1]),
                    "p_B_E0": float(probs[1, 0]),
                    "p_B_E1": float(probs[1, 1]),
                    "delta_A_E1_minus_E0": float(delta[0]),
                    "delta_B_E1_minus_E0": float(delta[1]),
                    "top1_A": int(top1[0]),
                    "top1_B": int(top1[1]),
                    "initial_pattern": "split" if int(top1[0]) != int(top1[1]) else "collapsed",
                }
            )
    return rows


def write_csv(rows: list[dict[str, float | int | str]]) -> None:
    TABLE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with TABLE_PATH.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_note(rows: list[dict[str, float | int | str]]) -> None:
    NOTE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with NOTE_PATH.open("w", encoding="utf-8") as f:
        f.write("# NTP-Style Initial Router Audit\n\n")
        f.write(
            "For h_A=e1 and h_B=e2, logits are the corresponding router "
            "matrix column plus bias.\n\n"
        )
        for row in rows:
            f.write(f"## {row['condition']} seed {row['seed']}\n\n")
            f.write("```text\n")
            f.write(
                "W = [[{:.6f}, {:.6f}],\n"
                "     [{:.6f}, {:.6f}]]\n".format(
                    row["W_E0_A"],
                    row["W_E0_B"],
                    row["W_E1_A"],
                    row["W_E1_B"],
                )
            )
            f.write("b = [{:.6f}, {:.6f}]\n".format(row["b_E0"], row["b_E1"]))
            f.write(
                "logits A=[{:.6f}, {:.6f}], B=[{:.6f}, {:.6f}]\n".format(
                    row["logit_A_E0"],
                    row["logit_A_E1"],
                    row["logit_B_E0"],
                    row["logit_B_E1"],
                )
            )
            f.write(
                "probs  A=[{:.6f}, {:.6f}], B=[{:.6f}, {:.6f}]\n".format(
                    row["p_A_E0"],
                    row["p_A_E1"],
                    row["p_B_E0"],
                    row["p_B_E1"],
                )
            )
            f.write(
                "delta(E1-E0) A={:.6f}, B={:.6f}; top1=({}, {}); pattern={}\n".format(
                    row["delta_A_E1_minus_E0"],
                    row["delta_B_E1_minus_E0"],
                    row["top1_A"],
                    row["top1_B"],
                    row["initial_pattern"],
                )
            )
            f.write("```\n\n")


def main() -> None:
    rows = audit_rows()
    write_csv(rows)
    write_note(rows)
    print(NOTE_PATH.read_text(encoding="utf-8"))
    print("CSV:", TABLE_PATH)


if __name__ == "__main__":
    main()
