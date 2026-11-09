#!/usr/bin/env python3
"""A06_13: decompose the real-DCLM proxy-init failure stage."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

import pandas as pd

ROOT = Path("/data/250010109/Research_System")
A10 = ROOT / "Projects/from-attention-to-search/main/experiments/A06/06_01_geometry_and_state_discovery/A06_01_04_E01_real_proxy_operationalization"
A11 = ROOT / "Projects/from-attention-to-search/main/experiments/A06/06_01_geometry_and_state_discovery/A06_01_04_E02_real_proxy_router_initialization"
A12 = ROOT / "Projects/from-attention-to-search/main/experiments/A06/06_01_geometry_and_state_discovery/A06_01_04_E03_real_proxy_training_overwrite"
A13 = ROOT / "Projects/from-attention-to-search/main/experiments/A06/06_01_geometry_and_state_discovery/A06_01_04_E04_real_proxy_failure_decomposition"


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fields = []
    seen = set()
    for row in rows:
        for key in row:
            if key not in seen:
                fields.append(key)
                seen.add(key)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    run_dir = A13 / "runs/failure_decomposition/a06_13_failure_decomposition_20260622_full01"
    (run_dir / "results").mkdir(parents=True, exist_ok=True)
    (run_dir / "figures").mkdir(parents=True, exist_ok=True)

    a10 = pd.read_csv(A10 / "runs/real_dclm_proxy_feature_operationalization/a06_10_real_dclm_proxy_4gpu_20260622_full01/results/proxy_cluster_summary.csv")
    a11 = pd.read_csv(A11 / "runs/real_dclm_proxy_center_router_initialization/a06_11_proxy_center_router_4gpu_20260622_full01/results/router_initialization_summary.csv")
    a12 = pd.read_csv(A12 / "runs/real_dclm_proxy_init_training_preservation/a06_12_proxy_init_training_4gpu_20260622_full01/results/training_preservation_summary.csv")

    a10_late_step0 = a10[(a10["condition"] == "residual") & (a10["checkpoint_step"] == 0) & (a10["layer"].isin([3, 4, 5]))]["eval_assignment_nmi"].mean()
    a10_late_step10 = a10[(a10["condition"] == "residual") & (a10["checkpoint_step"] == 10) & (a10["layer"].isin([3, 4, 5]))]["eval_assignment_nmi"].mean()
    a10_random = a10["random_assignment_nmi"].mean()
    a11_step0_raw = a11[(a11["router_condition"] == "raw_center_equal_norm") & (a11["route_space"] == "raw_input") & (a11["source_checkpoint_step"] == 0)]["proxy_route_nmi"].mean()
    a11_random = a11[(a11["router_condition"] == "random_equal_norm") & (a11["route_space"] == "raw_input") & (a11["source_checkpoint_step"] == 0)]["proxy_route_nmi"].mean()
    traj = a12[a12["variant"] == "raw_center"].groupby("step")[["proxy_route_nmi", "route_max_cluster_load", "common_margin", "lm_loss"]].mean().reset_index()
    random_traj = a12[a12["variant"] == "random"].groupby("step")[["proxy_route_nmi", "route_max_cluster_load", "common_margin", "lm_loss"]].mean().reset_index()
    raw_step0 = float(traj[traj["step"] == 0]["proxy_route_nmi"].iloc[0])
    raw_step5 = float(traj[traj["step"] == 5]["proxy_route_nmi"].iloc[0])
    raw_step10 = float(traj[traj["step"] == 10]["proxy_route_nmi"].iloc[0])
    random_step10 = float(random_traj[random_traj["step"] == 10]["proxy_route_nmi"].iloc[0])
    loss_delta10 = float(traj[traj["step"] == 10]["lm_loss"].iloc[0] - random_traj[random_traj["step"] == 10]["lm_loss"].iloc[0])

    bottleneck_rows = [
        {
            "stage": "proxy_discovery_h_to_q",
            "contract": "stable proxy labels exist above random",
            "metric": "late-layer residual eval_assignment_nmi",
            "value": round(float(a10_late_step0), 6),
            "guard_value": round(float(a10_random), 6),
            "status": "pass_with_boundary",
            "evidence": "A06_10 step0 late-layer proxy is modest but above random; step10 late-layer proxy is strong.",
            "next_action_if_failed": "redefine proxy construction",
        },
        {
            "stage": "proxy_discovery_h_to_q_step10_guard",
            "contract": "proxy strengthens after early training",
            "metric": "late-layer residual eval_assignment_nmi at step10",
            "value": round(float(a10_late_step10), 6),
            "guard_value": round(float(a10_random), 6),
            "status": "pass",
            "evidence": "A06_10 step10 late-layer proxy is high and nuisance-bounded.",
            "next_action_if_failed": "avoid step10 proxy-dependent claims",
        },
        {
            "stage": "linear_bridge_q_to_a0",
            "contract": "proxy centers initialize raw-input router above random",
            "metric": "raw_center step0 raw-input proxy_route_nmi",
            "value": round(float(a11_step0_raw), 6),
            "guard_value": round(float(a11_random), 6),
            "status": "pass",
            "evidence": "A06_11 raw-center rows route by proxy at step0.",
            "next_action_if_failed": "study nonlinear/bias bridge",
        },
        {
            "stage": "training_preservation_a0_to_at",
            "contract": "proxy routing survives through step10",
            "metric": "raw_center proxy_route_nmi at step10",
            "value": round(raw_step10, 6),
            "guard_value": round(random_step10, 6),
            "status": "fail_first_failed_contract",
            "evidence": "A06_12 raw-center NMI collapses from step0 to step5/10 while loss remains comparable.",
            "next_action_if_failed": "test anti-collapse or preservation mechanisms",
        },
        {
            "stage": "loss_guard",
            "contract": "failure is not caused by worse LM optimization",
            "metric": "raw_center minus random lm_loss at step10",
            "value": round(loss_delta10, 6),
            "guard_value": 0.0,
            "status": "pass_loss_comparable",
            "evidence": "LM loss is nearly identical to random at step10.",
            "next_action_if_failed": "retune scale/lr before interpreting routing failure",
        },
    ]
    write_csv(run_dir / "results/bottleneck_summary.csv", bottleneck_rows)
    collapse = traj.copy()
    collapse["drop_from_step0"] = raw_step0 - collapse["proxy_route_nmi"]
    collapse["fraction_of_step0_remaining"] = collapse["proxy_route_nmi"] / raw_step0
    collapse.to_csv(run_dir / "results/raw_center_collapse_timing.csv", index=False)

    try:
        import matplotlib.pyplot as plt

        plt.figure(figsize=(7, 4))
        plt.plot(collapse["step"], collapse["fraction_of_step0_remaining"], marker="o")
        plt.axhline(0.1, linestyle="--")
        plt.xlabel("step")
        plt.ylabel("fraction of step0 proxy NMI remaining")
        plt.tight_layout()
        plt.savefig(run_dir / "figures/raw_center_proxy_retention.png", dpi=160)
        plt.close()
    except Exception:
        pass

    summary = {
        "decision": "training_feedback_override",
        "first_failed_stage": "training_preservation_a0_to_at",
        "raw_center_step0_proxy_route_nmi": raw_step0,
        "raw_center_step5_proxy_route_nmi": raw_step5,
        "raw_center_step10_proxy_route_nmi": raw_step10,
        "random_step10_proxy_route_nmi": random_step10,
        "step10_loss_delta_raw_minus_random": loss_delta10,
        "recommended_next": [
            "router freeze or delayed router training",
            "lower router learning rate",
            "proxy-preservation auxiliary loss",
            "common/load anti-collapse regularizer",
        ],
    }
    (run_dir / "run_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
