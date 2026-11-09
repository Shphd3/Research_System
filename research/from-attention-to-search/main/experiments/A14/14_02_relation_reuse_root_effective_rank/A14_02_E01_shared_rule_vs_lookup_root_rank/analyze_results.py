#!/usr/bin/env python3
"""Create the curated A14_02_E01 result table and capability-aware figure."""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from pathlib import Path
from statistics import mean, stdev

import matplotlib.pyplot as plt


CONDITION_ORDER = [
    "shared_unique",
    "lookup_unique",
    "shared_repeat_duplicate",
    "shared_repeat_diverse",
    "lookup_k1_repeat_diverse",
    "lookup_k4_repeat_diverse",
    "lookup_repeat_diverse",
]

DISPLAY_NAMES = {
    "shared_unique": "Shared\nF=1",
    "lookup_unique": "Lookup K=16\nF=1",
    "shared_repeat_duplicate": "Shared\nF=8 duplicate",
    "shared_repeat_diverse": "Shared\nF=8 diverse",
    "lookup_k1_repeat_diverse": "Lookup K=1\nF=8 diverse",
    "lookup_k4_repeat_diverse": "Lookup K=4\nF=8 diverse",
    "lookup_repeat_diverse": "Lookup K=16\nF=8 diverse",
}


def parse_bool(value: str) -> bool:
    return value.strip().lower() == "true"


def read_rows(path: Path) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    with path.open(newline="", encoding="utf-8") as handle:
        for raw in csv.DictReader(handle):
            row: dict[str, object] = dict(raw)
            row["seed"] = int(raw["seed"])
            row["capability_pass"] = parse_bool(raw["capability_pass"])
            for key in [
                "train_answer_accuracy",
                "calibration_answer_accuracy",
                "calibration_answer_ce",
                "test_answer_accuracy",
                "test_answer_ce",
                "composition_answer_accuracy",
                "semantic_consistency",
                "post_functional_rank",
                "pre_functional_rank",
                "post_pca_functional_rank",
                "post_pca_entropy_effective_rank",
                "post_pca_energy_rank_95",
                "post_random_pass_fraction",
                "post_shuffle_accuracy_drop",
                "post_shuffle_delta_ce",
                "post_full_replay_abs_ce_delta",
            ]:
                value = raw.get(key, "")
                row[key] = float(value) if value not in {"", None} else None
            rows.append(row)
    return rows


def safe_mean(values: list[float]) -> float | None:
    return mean(values) if values else None


def safe_sd(values: list[float]) -> float | None:
    return stdev(values) if len(values) > 1 else (0.0 if values else None)


def fmt(value: float | None) -> str:
    return "" if value is None else f"{value:.6f}"


def build_summary(
    rows: list[dict[str, object]], output_dir: Path
) -> dict[str, dict[str, object]]:
    grouped: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        grouped[str(row["condition"])].append(row)

    summaries: dict[str, dict[str, object]] = {}
    for condition in CONDITION_ORDER:
        condition_rows = grouped[condition]
        passing = [row for row in condition_rows if bool(row["capability_pass"])]

        def values(key: str, source: list[dict[str, object]]) -> list[float]:
            return [
                float(row[key])
                for row in source
                if row.get(key) is not None
            ]

        summaries[condition] = {
            "condition": condition,
            "seeds": len(condition_rows),
            "capability_passes": len(passing),
            "train_accuracy_mean": safe_mean(
                values("train_answer_accuracy", condition_rows)
            ),
            "test_accuracy_mean_all": safe_mean(
                values("test_answer_accuracy", condition_rows)
            ),
            "test_ce_mean_all": safe_mean(values("test_answer_ce", condition_rows)),
            "test_accuracy_mean_passing": safe_mean(
                values("test_answer_accuracy", passing)
            ),
            "test_ce_mean_passing": safe_mean(values("test_answer_ce", passing)),
            "post_functional_rank_mean_passing": safe_mean(
                values("post_functional_rank", passing)
            ),
            "post_functional_rank_sd_passing": safe_sd(
                values("post_functional_rank", passing)
            ),
            "pre_functional_rank_mean_passing": safe_mean(
                values("pre_functional_rank", passing)
            ),
            "pca_functional_rank_mean_passing": safe_mean(
                values("post_pca_functional_rank", passing)
            ),
            "entropy_effective_rank_mean_passing": safe_mean(
                values("post_pca_entropy_effective_rank", passing)
            ),
            "r95_mean_passing": safe_mean(
                values("post_pca_energy_rank_95", passing)
            ),
            "semantic_consistency_mean_all": safe_mean(
                values("semantic_consistency", condition_rows)
            ),
            "composition_accuracy_mean_passing": safe_mean(
                values("composition_answer_accuracy", passing)
            ),
            "random_subspace_pass_fraction_mean_passing": safe_mean(
                values("post_random_pass_fraction", passing)
            ),
            "shuffle_accuracy_drop_mean_passing": safe_mean(
                values("post_shuffle_accuracy_drop", passing)
            ),
            "shuffle_ce_increase_mean_passing": safe_mean(
                values("post_shuffle_delta_ce", passing)
            ),
            "full_replay_abs_ce_delta_max_passing": max(
                values("post_full_replay_abs_ce_delta", passing), default=None
            ),
        }

    columns = list(next(iter(summaries.values())).keys())
    with (output_dir / "condition_summary.csv").open(
        "w", newline="", encoding="utf-8"
    ) as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        for condition in CONDITION_ORDER:
            writer.writerow(
                {
                    key: fmt(value) if isinstance(value, float) else value
                    for key, value in summaries[condition].items()
                }
            )

    shared = {
        int(row["seed"]): row
        for row in grouped["shared_repeat_diverse"]
        if bool(row["capability_pass"])
    }
    lookup = {
        int(row["seed"]): row
        for row in grouped["lookup_repeat_diverse"]
        if bool(row["capability_pass"])
    }
    with (output_dir / "passing_shared_lookup_pairs.csv").open(
        "w", newline="", encoding="utf-8"
    ) as handle:
        columns = [
            "seed",
            "shared_post_functional_rank",
            "lookup_post_functional_rank",
            "lookup_minus_shared_rank",
            "shared_test_accuracy",
            "lookup_test_accuracy",
            "shared_composition_accuracy",
        ]
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        for seed in sorted(set(shared) & set(lookup)):
            writer.writerow(
                {
                    "seed": seed,
                    "shared_post_functional_rank": int(
                        float(shared[seed]["post_functional_rank"])
                    ),
                    "lookup_post_functional_rank": int(
                        float(lookup[seed]["post_functional_rank"])
                    ),
                    "lookup_minus_shared_rank": int(
                        float(lookup[seed]["post_functional_rank"])
                        - float(shared[seed]["post_functional_rank"])
                    ),
                    "shared_test_accuracy": fmt(
                        float(shared[seed]["test_answer_accuracy"])
                    ),
                    "lookup_test_accuracy": fmt(
                        float(lookup[seed]["test_answer_accuracy"])
                    ),
                    "shared_composition_accuracy": fmt(
                        float(shared[seed]["composition_answer_accuracy"])
                    ),
                }
            )

    return summaries


def build_figure(
    rows: list[dict[str, object]],
    summaries: dict[str, dict[str, object]],
    output_dir: Path,
) -> None:
    grouped: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        grouped[str(row["condition"])].append(row)

    plt.style.use("seaborn-v0_8-whitegrid")
    figure, axes = plt.subplots(1, 2, figsize=(14.5, 5.3))

    x = list(range(len(CONDITION_ORDER)))
    for index, condition in enumerate(CONDITION_ORDER):
        accuracies = [
            float(row["test_answer_accuracy"]) for row in grouped[condition]
        ]
        axes[0].scatter(
            [index] * len(accuracies),
            accuracies,
            color="#2b6cb0",
            alpha=0.8,
            s=34,
            zorder=3,
        )
        axes[0].plot(
            [index - 0.22, index + 0.22],
            [mean(accuracies), mean(accuracies)],
            color="#1a365d",
            linewidth=2.3,
            zorder=4,
        )
    axes[0].axhline(
        0.95,
        color="#c53030",
        linestyle="--",
        linewidth=1.5,
        label="Capability gate = 0.95",
    )
    axes[0].set_xticks(x, [DISPLAY_NAMES[name] for name in CONDITION_ORDER])
    axes[0].set_ylim(-0.03, 1.05)
    axes[0].set_ylabel("Held-out answer accuracy")
    axes[0].set_title("A. Capability must be established before rank")
    axes[0].legend(loc="lower right", frameon=True)

    valid_conditions = [
        "shared_repeat_diverse",
        "lookup_k1_repeat_diverse",
        "lookup_k4_repeat_diverse",
        "lookup_repeat_diverse",
    ]
    valid_x = list(range(len(valid_conditions)))
    for index, condition in enumerate(valid_conditions):
        ranks = [
            float(row["post_functional_rank"])
            for row in grouped[condition]
            if bool(row["capability_pass"])
        ]
        axes[1].scatter(
            [index] * len(ranks),
            ranks,
            color="#2f855a",
            alpha=0.85,
            s=42,
            zorder=3,
        )
        axes[1].plot(
            [index - 0.20, index + 0.20],
            [mean(ranks), mean(ranks)],
            color="#22543d",
            linewidth=2.5,
            zorder=4,
        )
        axes[1].text(
            index,
            mean(ranks) + 0.45,
            f"mean {mean(ranks):.2f}\n{len(ranks)}/5 pass",
            ha="center",
            va="bottom",
            fontsize=9,
        )
    axes[1].set_xticks(
        valid_x, [DISPLAY_NAMES[name] for name in valid_conditions]
    )
    axes[1].set_ylim(7.5, 15.5)
    axes[1].set_ylabel("Post-norm task-functional ROOT rank (directions)")
    axes[1].set_title("B. Rank only among capability-passing runs")

    figure.suptitle(
        "A14_02_E01: context diversity enables capability; lookup rule count raises functional rank",
        fontsize=13,
        y=1.02,
    )
    figure.tight_layout()
    figure.savefig(
        output_dir / "capability_and_functional_rank.png",
        dpi=220,
        bbox_inches="tight",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("result_csv", type=Path)
    parser.add_argument("--output-dir", type=Path, default=Path("."))
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    rows = read_rows(args.result_csv)
    summaries = build_summary(rows, args.output_dir)
    build_figure(rows, summaries, args.output_dir)


if __name__ == "__main__":
    main()
