from __future__ import annotations

import csv
import math
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from run_known_good import entropy, forward, nmi_from_counts
from run_no_prior_no_expert_advantage import init_params as init_no_advantage


ROOT = Path(__file__).resolve().parent

DIAG_TABLE_DIR = ROOT / "tables" / "diagnostics"
DIAG_NOTE_DIR = ROOT / "notes" / "diagnostics"

RAND_FIG_DIR = ROOT / "figures" / "random_far_experts"
RAND_TABLE_DIR = ROOT / "tables" / "random_far_experts"
RAND_NOTE_DIR = ROOT / "notes" / "random_far_experts"

FEATURES = [np.array([1.0, 0.0]), np.array([0.0, 1.0])]


def init_random_far_experts(seed: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed)

    # No hand-coded feature advantage. The experts are random matrices, but we
    # require them to be numerically far apart so the router can receive
    # differential expert-output signals if the loss makes those signals useful.
    for _ in range(100):
        experts = rng.normal(scale=0.85, size=(2, 2, 2))
        if np.linalg.norm(experts[0] - experts[1]) >= 1.5:
            break

    # No router diagonal prior.
    router_w = rng.normal(scale=0.015, size=(2, 2))
    router_b = rng.normal(scale=0.005, size=(2,))
    return experts, router_w, router_b


def route_metrics(
    condition: str,
    seed: int,
    step: int,
    experts: np.ndarray,
    router_w: np.ndarray,
    router_b: np.ndarray,
) -> dict[str, float | int | str]:
    heatmap = []
    losses = []
    top1 = []

    for x in FEATURES:
        _, probs, _, y_hat = forward(x, experts, router_w, router_b)
        heatmap.append(probs)
        losses.append(0.5 * float(np.sum((y_hat - x) ** 2)))
        top1.append(int(np.argmax(probs)))

    heatmap_arr = np.array(heatmap)
    counts = np.zeros((2, 2), dtype=np.float64)
    for feature_id, expert_id in enumerate(top1):
        counts[feature_id, expert_id] += 1.0

    direct_acc = 0.5 * ((top1[0] == 0) + (top1[1] == 1))
    swapped_acc = 0.5 * ((top1[0] == 1) + (top1[1] == 0))
    assignment_accuracy = max(direct_acc, swapped_acc)

    row_margin_a = abs(float(heatmap_arr[0, 0] - heatmap_arr[0, 1]))
    row_margin_b = abs(float(heatmap_arr[1, 0] - heatmap_arr[1, 1]))
    mean_margin = 0.5 * (row_margin_a + row_margin_b)
    usage = np.mean(heatmap_arr, axis=0)
    max_usage = float(np.max(usage))
    mean_entropy = 0.5 * (entropy(heatmap_arr[0]) + entropy(heatmap_arr[1]))
    pattern = "separated" if top1[0] != top1[1] else "collapsed"

    return {
        "condition": condition,
        "seed": seed,
        "step": step,
        "p_e0_given_A": float(heatmap_arr[0, 0]),
        "p_e1_given_A": float(heatmap_arr[0, 1]),
        "p_e0_given_B": float(heatmap_arr[1, 0]),
        "p_e1_given_B": float(heatmap_arr[1, 1]),
        "mean_route_margin": mean_margin,
        "nmi": nmi_from_counts(counts),
        "assignment_accuracy": float(assignment_accuracy),
        "mean_entropy": mean_entropy,
        "max_expert_usage": max_usage,
        "loss": float(np.mean(losses)),
        "pattern": pattern,
    }


def gradient_metrics(
    condition: str,
    seed: int,
    step: int,
    experts: np.ndarray,
    router_w: np.ndarray,
    router_b: np.ndarray,
) -> dict[str, float | int | str]:
    grad_w = np.zeros_like(router_w)
    grad_b = np.zeros_like(router_b)
    expert_output_gaps = []
    grad_logit_norms = []
    losses = []

    for x in FEATURES:
        _, probs, expert_out, y_hat = forward(x, experts, router_w, router_b)
        err = y_hat - x
        losses.append(0.5 * float(np.sum(err**2)))
        expert_output_gaps.append(float(np.linalg.norm(expert_out[0] - expert_out[1])))

        grad_probs = np.array([float(err @ expert_out[e]) for e in range(2)])
        centered = grad_probs - float(probs @ grad_probs)
        grad_logits = probs * centered
        grad_logit_norms.append(float(np.linalg.norm(grad_logits)))
        grad_w += np.outer(grad_logits, x)
        grad_b += grad_logits

    scale = 1.0 / len(FEATURES)
    grad_w *= scale
    grad_b *= scale

    return {
        "condition": condition,
        "seed": seed,
        "step": step,
        "expert_gap_A": expert_output_gaps[0],
        "expert_gap_B": expert_output_gaps[1],
        "mean_expert_output_gap": float(np.mean(expert_output_gaps)),
        "router_grad_w_norm": float(np.linalg.norm(grad_w)),
        "router_grad_b_norm": float(np.linalg.norm(grad_b)),
        "mean_grad_logit_norm": float(np.mean(grad_logit_norms)),
        "loss": float(np.mean(losses)),
    }


def train_condition(
    condition: str,
    init_fn,
    seeds: list[int],
    steps: int = 200,
    lr: float = 0.08,
) -> tuple[list[dict[str, float | int | str]], list[dict[str, float | int | str]]]:
    checkpoints = {0, 10, 50, 100, 200}
    metric_rows: list[dict[str, float | int | str]] = []
    grad_rows: list[dict[str, float | int | str]] = []

    for seed in seeds:
        experts, router_w, router_b = init_fn(seed)

        for step in range(steps + 1):
            if step in checkpoints:
                metric_rows.append(route_metrics(condition, seed, step, experts, router_w, router_b))
                grad_rows.append(gradient_metrics(condition, seed, step, experts, router_w, router_b))

            if step == steps:
                break

            grad_experts = np.zeros_like(experts)
            grad_w = np.zeros_like(router_w)
            grad_b = np.zeros_like(router_b)

            for x in FEATURES:
                _, probs, expert_out, y_hat = forward(x, experts, router_w, router_b)
                err = y_hat - x

                for e in range(2):
                    grad_experts[e] += probs[e] * np.outer(err, x)

                grad_probs = np.array([float(err @ expert_out[e]) for e in range(2)])
                centered = grad_probs - float(probs @ grad_probs)
                grad_logits = probs * centered
                grad_w += np.outer(grad_logits, x)
                grad_b += grad_logits

            scale = 1.0 / len(FEATURES)
            experts -= lr * grad_experts * scale
            router_w -= lr * grad_w * scale
            router_b -= lr * grad_b * scale

    return metric_rows, grad_rows


def write_csv(path: Path, rows: list[dict[str, float | int | str]]) -> None:
    if not rows:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def initial_utility_preferences(
    condition: str,
    init_fn,
    seeds: list[int],
) -> list[dict[str, float | int | str]]:
    rows: list[dict[str, float | int | str]] = []
    for seed in seeds:
        experts, _, _ = init_fn(seed)
        losses = []
        for x in FEATURES:
            feature_losses = []
            for e in range(2):
                y = experts[e] @ x
                feature_losses.append(0.5 * float(np.sum((y - x) ** 2)))
            losses.append(feature_losses)

        best_a = int(np.argmin(losses[0]))
        best_b = int(np.argmin(losses[1]))
        preference_pattern = "crossed" if best_a != best_b else "shared"
        rows.append(
            {
                "condition": condition,
                "seed": seed,
                "loss_A_E0": losses[0][0],
                "loss_A_E1": losses[0][1],
                "loss_B_E0": losses[1][0],
                "loss_B_E1": losses[1][1],
                "best_expert_A": best_a,
                "best_expert_B": best_b,
                "preference_pattern": preference_pattern,
            }
        )
    return rows


def save_heatmap(row: dict[str, float | int | str]) -> None:
    heatmap = np.array(
        [
            [row["p_e0_given_A"], row["p_e1_given_A"]],
            [row["p_e0_given_B"], row["p_e1_given_B"]],
        ],
        dtype=np.float64,
    )
    fig, ax = plt.subplots(figsize=(3.2, 2.8))
    im = ax.imshow(heatmap, vmin=0, vmax=1, cmap="Blues")
    ax.set_xticks([0, 1], labels=["E0", "E1"])
    ax.set_yticks([0, 1], labels=["Feature A", "Feature B"])
    ax.set_title(f"random far seed {row['seed']} step {row['step']}")
    for i in range(2):
        for j in range(2):
            ax.text(j, i, f"{heatmap[i, j]:.2f}", ha="center", va="center")
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    fig.tight_layout()
    fig.savefig(RAND_FIG_DIR / f"heatmap_seed{row['seed']}_step{row['step']}.png", dpi=160)
    plt.close(fig)


def save_trajectory(rows: list[dict[str, float | int | str]]) -> None:
    for seed in sorted({int(r["seed"]) for r in rows}):
        seed_rows = [r for r in rows if int(r["seed"]) == seed]
        steps = [int(r["step"]) for r in seed_rows]
        margins = [float(r["mean_route_margin"]) for r in seed_rows]
        losses = [float(r["loss"]) for r in seed_rows]
        entropy_values = [float(r["mean_entropy"]) for r in seed_rows]

        fig, axes = plt.subplots(1, 3, figsize=(9.6, 2.8))
        axes[0].plot(steps, margins, marker="o")
        axes[0].set_title("route margin")
        axes[0].set_xlabel("step")
        axes[0].set_ylim(0, 1)
        axes[1].plot(steps, entropy_values, marker="o")
        axes[1].set_title("mean entropy")
        axes[1].set_xlabel("step")
        axes[1].set_ylim(0, math.log(2) + 0.05)
        axes[2].plot(steps, losses, marker="o")
        axes[2].set_title("loss")
        axes[2].set_xlabel("step")
        fig.suptitle(f"random far experts seed {seed}")
        fig.tight_layout()
        fig.savefig(RAND_FIG_DIR / f"trajectory_seed{seed}.png", dpi=160)
        plt.close(fig)


def summarize_random_far(
    final_metric_rows: list[dict[str, float | int | str]],
    final_grad_rows: list[dict[str, float | int | str]],
    utility_rows: list[dict[str, float | int | str]],
) -> None:
    RAND_NOTE_DIR.mkdir(parents=True, exist_ok=True)
    grad_by_seed = {int(r["seed"]): r for r in final_grad_rows}
    utility_by_seed = {int(r["seed"]): r for r in utility_rows}
    separated = sum(1 for r in final_metric_rows if r["pattern"] == "separated")
    total = len(final_metric_rows)
    margins = [float(r["mean_route_margin"]) for r in final_metric_rows]
    nmis = [float(r["nmi"]) for r in final_metric_rows]
    crossed = sum(1 for r in utility_rows if r["preference_pattern"] == "crossed")

    with (RAND_NOTE_DIR / "run_observations.md").open("w", encoding="utf-8") as f:
        f.write("# Random Far Experts Run Observations\n\n")
        f.write("Condition: no router prior; experts are random matrices with large initial distance, not hand-coded feature-specific advantages.\n\n")
        f.write(f"Separated final top-1 routing: {separated}/{total} seeds.\n")
        f.write(f"Crossed initial expert utility preference: {crossed}/{total} seeds.\n")
        f.write(f"Mean final route margin: {np.mean(margins):.4f}.\n")
        f.write(f"Mean final NMI: {np.mean(nmis):.4f}.\n\n")
        f.write("Final checkpoint summary:\n\n")
        for row in final_metric_rows:
            seed = int(row["seed"])
            grad = grad_by_seed[seed]
            utility = utility_by_seed[seed]
            f.write(
                f"- seed {seed}: pattern={row['pattern']}, "
                f"initial_utility={utility['preference_pattern']}, "
                f"margin={float(row['mean_route_margin']):.4f}, "
                f"NMI={float(row['nmi']):.4f}, "
                f"accuracy={float(row['assignment_accuracy']):.4f}, "
                f"entropy={float(row['mean_entropy']):.4f}, "
                f"loss={float(row['loss']):.6f}, "
                f"expert_gap={float(grad['mean_expert_output_gap']):.4f}, "
                f"router_grad_w_norm={float(grad['router_grad_w_norm']):.6f}\n"
            )


def summarize_diagnostic(rows: list[dict[str, float | int | str]]) -> None:
    DIAG_NOTE_DIR.mkdir(parents=True, exist_ok=True)
    final_rows = [r for r in rows if int(r["step"]) == 200]
    init_rows = [r for r in rows if int(r["step"]) == 0]
    with (DIAG_NOTE_DIR / "router_signal_no_prior_no_advantage.md").open("w", encoding="utf-8") as f:
        f.write("# Router Signal Diagnostic\n\n")
        f.write("Condition: no router prior and no feature-specific expert advantage.\n\n")
        f.write("Initial checkpoint:\n\n")
        for row in init_rows:
            f.write(
                f"- seed {row['seed']}: expert_gap={float(row['mean_expert_output_gap']):.4f}, "
                f"router_grad_w_norm={float(row['router_grad_w_norm']):.6f}, "
                f"mean_grad_logit_norm={float(row['mean_grad_logit_norm']):.6f}, "
                f"loss={float(row['loss']):.6f}\n"
            )
        f.write("\nFinal checkpoint:\n\n")
        for row in final_rows:
            f.write(
                f"- seed {row['seed']}: expert_gap={float(row['mean_expert_output_gap']):.4f}, "
                f"router_grad_w_norm={float(row['router_grad_w_norm']):.6f}, "
                f"mean_grad_logit_norm={float(row['mean_grad_logit_norm']):.6f}, "
                f"loss={float(row['loss']):.6f}\n"
            )


def main() -> None:
    DIAG_TABLE_DIR.mkdir(parents=True, exist_ok=True)
    RAND_TABLE_DIR.mkdir(parents=True, exist_ok=True)
    RAND_FIG_DIR.mkdir(parents=True, exist_ok=True)

    _, no_adv_grad_rows = train_condition(
        "no_prior_no_expert_advantage",
        init_no_advantage,
        seeds=[0, 1, 2],
    )
    write_csv(DIAG_TABLE_DIR / "router_signal_no_prior_no_advantage.csv", no_adv_grad_rows)
    summarize_diagnostic(no_adv_grad_rows)

    random_metric_rows, random_grad_rows = train_condition(
        "random_far_experts",
        init_random_far_experts,
        seeds=list(range(10)),
    )
    random_utility_rows = initial_utility_preferences(
        "random_far_experts",
        init_random_far_experts,
        seeds=list(range(10)),
    )
    write_csv(RAND_TABLE_DIR / "metrics_by_checkpoint.csv", random_metric_rows)
    write_csv(RAND_TABLE_DIR / "diagnostics_by_checkpoint.csv", random_grad_rows)
    write_csv(RAND_TABLE_DIR / "initial_utility_preferences.csv", random_utility_rows)
    final_metric_rows = [r for r in random_metric_rows if int(r["step"]) == 200]
    final_grad_rows = [r for r in random_grad_rows if int(r["step"]) == 200]
    write_csv(RAND_TABLE_DIR / "seed_checkpoint_summary.csv", final_metric_rows)
    summarize_random_far(final_metric_rows, final_grad_rows, random_utility_rows)

    for row in random_metric_rows:
        if int(row["step"]) in {0, 50, 200}:
            save_heatmap(row)
    save_trajectory(random_metric_rows)

    print("Wrote router-signal diagnostic artifacts to:")
    print(DIAG_TABLE_DIR)
    print(DIAG_NOTE_DIR)
    print("Wrote random-far-experts artifacts to:")
    print(RAND_TABLE_DIR)
    print(RAND_FIG_DIR)
    print(RAND_NOTE_DIR)


if __name__ == "__main__":
    main()
