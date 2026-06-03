from __future__ import annotations

import csv
import math
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from run_known_good import entropy, forward, nmi_from_counts


ROOT = Path(__file__).resolve().parent
FIG_DIR = ROOT / "figures" / "no_router_prior"
TABLE_DIR = ROOT / "tables" / "no_router_prior"
NOTE_DIR = ROOT / "notes" / "no_router_prior"


def init_params(seed: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed)

    # Keep favorable expert initialization exactly as in the known-good run.
    experts = np.array(
        [
            [[0.80, 0.00], [0.00, 0.10]],
            [[0.10, 0.00], [0.00, 0.80]],
        ],
        dtype=np.float64,
    )
    experts += rng.normal(scale=0.015, size=experts.shape)

    # Remove router diagonal prior. Start near zero with only tiny random
    # symmetry-breaking noise.
    router_w = rng.normal(scale=0.015, size=(2, 2))
    router_b = rng.normal(scale=0.005, size=(2,))
    return experts, router_w, router_b


def evaluate(
    seed: int,
    step: int,
    experts: np.ndarray,
    router_w: np.ndarray,
    router_b: np.ndarray,
) -> dict[str, float | int | str]:
    xs = [np.array([1.0, 0.0]), np.array([0.0, 1.0])]
    heatmap = []
    losses = []
    top1 = []

    for x in xs:
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

    if top1[0] != top1[1]:
        pattern = "separated"
    else:
        pattern = "collapsed"

    return {
        "condition": "no_router_prior",
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


def train_seed(seed: int, steps: int = 200, lr: float = 0.08) -> list[dict[str, float | int | str]]:
    experts, router_w, router_b = init_params(seed)
    xs = [np.array([1.0, 0.0]), np.array([0.0, 1.0])]
    checkpoints = {0, 10, 50, 100, 200}
    rows: list[dict[str, float | int | str]] = []

    for step in range(steps + 1):
        if step in checkpoints:
            rows.append(evaluate(seed, step, experts, router_w, router_b))

        if step == steps:
            break

        grad_experts = np.zeros_like(experts)
        grad_w = np.zeros_like(router_w)
        grad_b = np.zeros_like(router_b)

        for x in xs:
            _, probs, expert_out, y_hat = forward(x, experts, router_w, router_b)
            err = y_hat - x

            for e in range(2):
                grad_experts[e] += probs[e] * np.outer(err, x)

            grad_probs = np.array([float(err @ expert_out[e]) for e in range(2)])
            centered = grad_probs - float(probs @ grad_probs)
            grad_logits = probs * centered
            grad_w += np.outer(grad_logits, x)
            grad_b += grad_logits

        scale = 1.0 / len(xs)
        experts -= lr * grad_experts * scale
        router_w -= lr * grad_w * scale
        router_b -= lr * grad_b * scale

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
    ax.set_title(f"no prior seed {row['seed']} step {row['step']}")

    for i in range(2):
        for j in range(2):
            ax.text(j, i, f"{heatmap[i, j]:.2f}", ha="center", va="center")

    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    fig.tight_layout()
    fig.savefig(FIG_DIR / f"heatmap_seed{row['seed']}_step{row['step']}.png", dpi=160)
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

        fig.suptitle(f"no router prior seed {seed}")
        fig.tight_layout()
        fig.savefig(FIG_DIR / f"trajectory_seed{seed}.png", dpi=160)
        plt.close(fig)


def main() -> None:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    TABLE_DIR.mkdir(parents=True, exist_ok=True)
    NOTE_DIR.mkdir(parents=True, exist_ok=True)

    all_rows: list[dict[str, float | int | str]] = []
    for seed in [0, 1, 2]:
        all_rows.extend(train_seed(seed))

    fieldnames = [
        "condition",
        "seed",
        "step",
        "p_e0_given_A",
        "p_e1_given_A",
        "p_e0_given_B",
        "p_e1_given_B",
        "mean_route_margin",
        "nmi",
        "assignment_accuracy",
        "mean_entropy",
        "max_expert_usage",
        "loss",
        "pattern",
    ]

    with (TABLE_DIR / "metrics_by_checkpoint.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_rows)

    final_rows = [r for r in all_rows if int(r["step"]) == 200]
    with (TABLE_DIR / "seed_checkpoint_summary.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(final_rows)

    for row in all_rows:
        if int(row["step"]) in {0, 50, 200}:
            save_heatmap(row)
    save_trajectory(all_rows)

    with (NOTE_DIR / "run_observations.md").open("w", encoding="utf-8") as f:
        f.write("# No Router Prior Run Observations\n\n")
        f.write("Second round: same known-good setup, but remove mild router diagonal prior. Expert advantage initialization and balanced feature frequency are kept.\n\n")
        f.write("Final checkpoint summary:\n\n")
        for row in final_rows:
            f.write(
                f"- seed {row['seed']}: pattern={row['pattern']}, "
                f"margin={row['mean_route_margin']:.4f}, "
                f"NMI={row['nmi']:.4f}, "
                f"accuracy={row['assignment_accuracy']:.4f}, "
                f"entropy={row['mean_entropy']:.4f}, "
                f"max_usage={row['max_expert_usage']:.4f}, "
                f"loss={row['loss']:.6f}\n"
            )

    print("Wrote no-router-prior artifacts to:")
    print(FIG_DIR)
    print(TABLE_DIR)
    print(NOTE_DIR)


if __name__ == "__main__":
    main()
