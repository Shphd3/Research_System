import argparse
import csv
from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


CONDITIONS = (
    "normalized_directions",
    "gaussian_scaled",
    "norm_controlled_gaussian",
)


def parse_int_list(text):
    return [int(part.strip()) for part in text.split(",") if part.strip()]


def unit_random_inputs(rng, batch_size, dim):
    x = rng.standard_normal((batch_size, dim), dtype=np.float64)
    x /= np.linalg.norm(x, axis=1, keepdims=True)
    return x


def row_norm_cv(weights):
    norms = np.linalg.norm(weights, axis=1)
    return float(np.std(norms) / np.mean(norms))


def max_abs_direction_corr(unit_rows):
    corr = np.abs(unit_rows @ unit_rows.T)
    np.fill_diagonal(corr, 0.0)
    return float(np.max(corr))


def top1_counts_for_conditions(rng, weights_by_condition, dim, total_tokens, batch_size):
    counts = {
        condition: np.zeros(weights.shape[0], dtype=np.int64)
        for condition, weights in weights_by_condition.items()
    }
    remaining = total_tokens
    while remaining > 0:
        current = min(batch_size, remaining)
        x = unit_random_inputs(rng, current, dim)
        for condition, weights in weights_by_condition.items():
            winners = np.argmax(x @ weights.T, axis=1)
            counts[condition] += np.bincount(winners, minlength=weights.shape[0])
        remaining -= current
    return counts


def imbalance(prob, experts):
    return float(experts * np.max(np.abs(prob - 1.0 / experts)))


def mean_std(values):
    arr = np.asarray(values, dtype=np.float64)
    if arr.size == 0:
        return "", ""
    if arr.size == 1:
        return float(arr[0]), 0.0
    return float(np.mean(arr)), float(np.std(arr, ddof=1))


def write_csv(path, rows, fieldnames):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def aggregate_results(rows):
    group_fields = ("dim", "experts", "condition", "observed_tokens")
    metric_fields = (
        "true_cell_imbalance",
        "observed_load_error",
        "sampling_error",
        "row_norm_cv",
        "max_abs_direction_corr",
    )
    groups = defaultdict(list)
    for row in rows:
        key = tuple(row[field] for field in group_fields)
        groups[key].append(row)

    aggregate_rows = []
    for key in sorted(groups):
        grouped = groups[key]
        out = dict(zip(group_fields, key))
        out["n_rows"] = len(grouped)
        for metric in metric_fields:
            mean, std = mean_std([float(row[metric]) for row in grouped])
            out[f"{metric}_mean"] = mean
            out[f"{metric}_std"] = std
        aggregate_rows.append(out)
    return aggregate_rows


def paired_delta_rows(true_rows):
    by_key = {}
    for row in true_rows:
        key = (row["dim"], row["experts"], row["seed"], row["condition"])
        by_key[key] = row

    rows = []
    for dim, experts, seed, condition in sorted(by_key):
        if condition != "gaussian_scaled":
            continue
        gaussian = by_key[(dim, experts, seed, "gaussian_scaled")]
        controlled = by_key[(dim, experts, seed, "norm_controlled_gaussian")]
        normalized = by_key[(dim, experts, seed, "normalized_directions")]
        rows.append(
            {
                "dim": dim,
                "experts": experts,
                "seed": seed,
                "gaussian_true_cell_imbalance": gaussian["true_cell_imbalance"],
                "norm_controlled_true_cell_imbalance": controlled["true_cell_imbalance"],
                "normalized_true_cell_imbalance": normalized["true_cell_imbalance"],
                "delta_gaussian_minus_norm_controlled": float(gaussian["true_cell_imbalance"])
                - float(controlled["true_cell_imbalance"]),
                "gaussian_row_norm_cv": gaussian["row_norm_cv"],
                "norm_controlled_row_norm_cv": controlled["row_norm_cv"],
                "max_abs_direction_corr": gaussian["max_abs_direction_corr"],
            }
        )
    return rows


def plot_true_cell_imbalance(aggregate_rows, figure_path):
    figure_path.parent.mkdir(parents=True, exist_ok=True)
    experts_values = sorted({int(row["experts"]) for row in aggregate_rows})
    fig, axes = plt.subplots(1, len(experts_values), figsize=(6 * len(experts_values), 4), sharey=True)
    if len(experts_values) == 1:
        axes = [axes]

    for ax, experts in zip(axes, experts_values):
        for condition in CONDITIONS:
            rows = [
                row
                for row in aggregate_rows
                if int(row["experts"]) == experts
                and row["condition"] == condition
                and int(row["observed_tokens"]) == max(int(r["observed_tokens"]) for r in aggregate_rows)
            ]
            rows = sorted(rows, key=lambda r: int(r["dim"]))
            ax.plot(
                [int(row["dim"]) for row in rows],
                [float(row["true_cell_imbalance_mean"]) for row in rows],
                marker="o",
                label=condition,
            )
        ax.set_xscale("log", base=2)
        ax.set_xlabel("dimension")
        ax.set_title(f"m={experts}")
        ax.grid(True, alpha=0.3)

    axes[0].set_ylabel("true cell imbalance")
    axes[-1].legend(loc="best", fontsize=8)
    fig.suptitle("True cell imbalance by gate condition")
    fig.tight_layout()
    fig.savefig(figure_path, dpi=180)
    plt.close(fig)


def plot_sampling_error(aggregate_rows, figure_path):
    figure_path.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(7, 4))
    for condition in CONDITIONS:
        by_tokens = defaultdict(list)
        for row in aggregate_rows:
            if row["condition"] == condition:
                by_tokens[int(row["observed_tokens"])].append(float(row["sampling_error_mean"]))
        xs = sorted(by_tokens)
        ys = [float(np.mean(by_tokens[x])) for x in xs]
        ax.plot(xs, ys, marker="o", label=condition)
    ax.set_xscale("log", base=2)
    ax.set_xlabel("observed tokens")
    ax.set_ylabel("sampling error")
    ax.set_title("Finite-token sampling error shrinks with token count")
    ax.grid(True, alpha=0.3)
    ax.legend(loc="best", fontsize=8)
    fig.tight_layout()
    fig.savefig(figure_path, dpi=180)
    plt.close(fig)


def run(args):
    out_dir = Path(args.out_dir)
    tables_dir = out_dir / "tables"
    figures_dir = out_dir / "figures"

    dims = parse_int_list(args.dims)
    experts_values = parse_int_list(args.experts)
    observed_tokens_values = parse_int_list(args.observed_tokens)
    seeds = list(range(args.seeds))

    result_rows = []
    true_rows = []

    for dim in dims:
        for experts in experts_values:
            for seed in seeds:
                rng = np.random.default_rng(args.seed_base + seed + 1009 * dim + 9176 * experts)
                gaussian = rng.standard_normal((experts, dim), dtype=np.float64)
                norms = np.linalg.norm(gaussian, axis=1, keepdims=True)
                directions = gaussian / norms
                common_norm = float(np.mean(norms))

                weights_by_condition = {
                    "normalized_directions": directions,
                    "gaussian_scaled": gaussian,
                    "norm_controlled_gaussian": directions * common_norm,
                }
                row_norm_cv_by_condition = {
                    condition: row_norm_cv(weights)
                    for condition, weights in weights_by_condition.items()
                }
                max_corr = max_abs_direction_corr(directions)

                true_counts = top1_counts_for_conditions(
                    rng,
                    weights_by_condition,
                    dim,
                    args.true_mc,
                    args.batch_size,
                )
                true_probs = {
                    condition: counts / float(args.true_mc)
                    for condition, counts in true_counts.items()
                }
                true_imbalances = {
                    condition: imbalance(prob, experts)
                    for condition, prob in true_probs.items()
                }

                for condition in CONDITIONS:
                    true_rows.append(
                        {
                            "dim": dim,
                            "experts": experts,
                            "seed": seed,
                            "condition": condition,
                            "true_cell_imbalance": true_imbalances[condition],
                            "row_norm_cv": row_norm_cv_by_condition[condition],
                            "max_abs_direction_corr": max_corr,
                        }
                    )

                for observed_tokens in observed_tokens_values:
                    for observed_rep in range(args.observed_reps):
                        observed_counts = top1_counts_for_conditions(
                            rng,
                            weights_by_condition,
                            dim,
                            observed_tokens,
                            args.batch_size,
                        )
                        for condition in CONDITIONS:
                            p_true = true_probs[condition]
                            p_hat = observed_counts[condition] / float(observed_tokens)
                            result_rows.append(
                                {
                                    "dim": dim,
                                    "experts": experts,
                                    "seed": seed,
                                    "observed_rep": observed_rep,
                                    "condition": condition,
                                    "observed_tokens": observed_tokens,
                                    "true_mc_tokens": args.true_mc,
                                    "true_cell_imbalance": true_imbalances[condition],
                                    "observed_load_error": imbalance(p_hat, experts),
                                    "sampling_error": imbalance(p_hat - p_true + 1.0 / experts, experts),
                                    "row_norm_cv": row_norm_cv_by_condition[condition],
                                    "max_abs_direction_corr": max_corr,
                                }
                            )
                print(f"finished dim={dim} experts={experts} seed={seed}", flush=True)

    aggregate_rows = aggregate_results(result_rows)
    paired_rows = paired_delta_rows(true_rows)

    result_fields = [
        "dim",
        "experts",
        "seed",
        "observed_rep",
        "condition",
        "observed_tokens",
        "true_mc_tokens",
        "true_cell_imbalance",
        "observed_load_error",
        "sampling_error",
        "row_norm_cv",
        "max_abs_direction_corr",
    ]
    aggregate_fields = [
        "dim",
        "experts",
        "condition",
        "observed_tokens",
        "n_rows",
        "true_cell_imbalance_mean",
        "true_cell_imbalance_std",
        "observed_load_error_mean",
        "observed_load_error_std",
        "sampling_error_mean",
        "sampling_error_std",
        "row_norm_cv_mean",
        "row_norm_cv_std",
        "max_abs_direction_corr_mean",
        "max_abs_direction_corr_std",
    ]
    paired_fields = [
        "dim",
        "experts",
        "seed",
        "gaussian_true_cell_imbalance",
        "norm_controlled_true_cell_imbalance",
        "normalized_true_cell_imbalance",
        "delta_gaussian_minus_norm_controlled",
        "gaussian_row_norm_cv",
        "norm_controlled_row_norm_cv",
        "max_abs_direction_corr",
    ]

    write_csv(tables_dir / "results.csv", result_rows, result_fields)
    write_csv(tables_dir / "aggregate_by_condition.csv", aggregate_rows, aggregate_fields)
    write_csv(tables_dir / "paired_gaussian_vs_norm_controlled.csv", paired_rows, paired_fields)

    plot_true_cell_imbalance(
        aggregate_rows,
        figures_dir / "true_cell_imbalance_by_condition.png",
    )
    plot_sampling_error(
        aggregate_rows,
        figures_dir / "sampling_error_by_tokens.png",
    )

    print(f"wrote {tables_dir / 'results.csv'}")
    print(f"wrote {tables_dir / 'aggregate_by_condition.csv'}")
    print(f"wrote {tables_dir / 'paired_gaussian_vs_norm_controlled.csv'}")
    print(f"wrote {figures_dir / 'true_cell_imbalance_by_condition.png'}")
    print(f"wrote {figures_dir / 'sampling_error_by_tokens.png'}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-dir", default=".")
    parser.add_argument("--dims", default="32,128,512")
    parser.add_argument("--experts", default="8,32")
    parser.add_argument("--seeds", type=int, default=8)
    parser.add_argument("--true-mc", type=int, default=50000)
    parser.add_argument("--observed-tokens", default="4096,32768")
    parser.add_argument("--observed-reps", type=int, default=3)
    parser.add_argument("--batch-size", type=int, default=5000)
    parser.add_argument("--seed-base", type=int, default=60320)
    args = parser.parse_args()
    run(args)


if __name__ == "__main__":
    main()
