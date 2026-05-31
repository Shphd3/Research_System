from __future__ import annotations

import csv
import math
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from run_known_good import entropy, nmi_from_counts


ROOT = Path(__file__).resolve().parent
FIG_DIR = ROOT / "figures" / "top1_sparse"
TABLE_DIR = ROOT / "tables" / "top1_sparse"
NOTE_DIR = ROOT / "notes" / "top1_sparse"

FEATURES = [np.array([1.0, 0.0]), np.array([0.0, 1.0])]


def softmax(z: np.ndarray) -> np.ndarray:
    z = z - np.max(z)
    exp_z = np.exp(z)
    return exp_z / np.sum(exp_z)


def init_expert_advantage(rng: np.random.Generator) -> np.ndarray:
    experts = np.array(
        [
            [[0.80, 0.00], [0.00, 0.10]],
            [[0.10, 0.00], [0.00, 0.80]],
        ],
        dtype=np.float64,
    )
    return experts + rng.normal(scale=0.015, size=experts.shape)


def init_no_expert_advantage(rng: np.random.Generator) -> np.ndarray:
    base = np.array([[0.45, 0.00], [0.00, 0.45]], dtype=np.float64)
    experts = np.stack([base.copy(), base.copy()])
    return experts + rng.normal(scale=0.015, size=experts.shape)


def init_params(condition: str, seed: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed)

    if condition in {"top1_known_good", "top1_no_router_prior"}:
        experts = init_expert_advantage(rng)
    elif condition == "top1_no_prior_no_expert_advantage":
        experts = init_no_expert_advantage(rng)
    else:
        raise ValueError(f"unknown condition: {condition}")

    if condition == "top1_known_good":
        router_w = np.array([[0.30, -0.30], [-0.30, 0.30]], dtype=np.float64)
        router_w += rng.normal(scale=0.015, size=router_w.shape)
    else:
        router_w = rng.normal(scale=0.015, size=(2, 2))

    router_b = rng.normal(scale=0.005, size=(2,))
    return experts, router_w, router_b


def forward_top1_sparse(
    x: np.ndarray, experts: np.ndarray, router_w: np.ndarray, router_b: np.ndarray
) -> tuple[np.ndarray, np.ndarray, int, np.ndarray, np.ndarray]:
    logits = router_w @ x + router_b
    probs = softmax(logits)
    top1 = int(np.argmax(probs))
    selected_prob = probs[top1]
    expert_out = np.stack([experts[0] @ x, experts[1] @ x])

    # Sparse top-1 forward: only the selected expert contributes. Router still
    # receives gradient through selected_prob.
    y_hat = selected_prob * expert_out[top1]
    return logits, probs, top1, expert_out, y_hat


def evaluate(
    condition: str,
    seed: int,
    step: int,
    experts: np.ndarray,
    router_w: np.ndarray,
    router_b: np.ndarray,
) -> dict[str, float | int | str]:
    heatmap = []
    selected_gates = []
    losses = []
    top1_assignments = []

    for x in FEATURES:
        _, probs, top1, _, y_hat = forward_top1_sparse(x, experts, router_w, router_b)
        heatmap.append(probs)
        selected_gates.append(float(probs[top1]))
        losses.append(0.5 * float(np.sum((y_hat - x) ** 2)))
        top1_assignments.append(top1)

    heatmap_arr = np.array(heatmap)
    counts = np.zeros((2, 2), dtype=np.float64)
    for feature_id, expert_id in enumerate(top1_assignments):
        counts[feature_id, expert_id] += 1.0

    direct_acc = 0.5 * ((top1_assignments[0] == 0) + (top1_assignments[1] == 1))
    swapped_acc = 0.5 * ((top1_assignments[0] == 1) + (top1_assignments[1] == 0))
    assignment_accuracy = max(direct_acc, swapped_acc)

    row_margin_a = abs(float(heatmap_arr[0, 0] - heatmap_arr[0, 1]))
    row_margin_b = abs(float(heatmap_arr[1, 0] - heatmap_arr[1, 1]))
    mean_margin = 0.5 * (row_margin_a + row_margin_b)
    usage = np.mean(heatmap_arr, axis=0)
    max_usage = float(np.max(usage))
    mean_entropy = 0.5 * (entropy(heatmap_arr[0]) + entropy(heatmap_arr[1]))
    pattern = "separated" if top1_assignments[0] != top1_assignments[1] else "collapsed"

    return {
        "condition": condition,
        "seed": seed,
        "step": step,
        "top1_A": top1_assignments[0],
        "top1_B": top1_assignments[1],
        "p_e0_given_A": float(heatmap_arr[0, 0]),
        "p_e1_given_A": float(heatmap_arr[0, 1]),
        "p_e0_given_B": float(heatmap_arr[1, 0]),
        "p_e1_given_B": float(heatmap_arr[1, 1]),
        "mean_selected_gate": float(np.mean(selected_gates)),
        "mean_route_margin": mean_margin,
        "nmi": nmi_from_counts(counts),
        "assignment_accuracy": float(assignment_accuracy),
        "mean_entropy": mean_entropy,
        "max_expert_usage": max_usage,
        "loss": float(np.mean(losses)),
        "pattern": pattern,
    }


def train_condition(
    condition: str, seeds: list[int], steps: int = 200, lr: float = 0.08
) -> list[dict[str, float | int | str]]:
    checkpoints = {0, 10, 50, 100, 200}
    rows: list[dict[str, float | int | str]] = []

    for seed in seeds:
        experts, router_w, router_b = init_params(condition, seed)

        for step in range(steps + 1):
            if step in checkpoints:
                rows.append(evaluate(condition, seed, step, experts, router_w, router_b))

            if step == steps:
                break

            grad_experts = np.zeros_like(experts)
            grad_w = np.zeros_like(router_w)
            grad_b = np.zeros_like(router_b)

            for x in FEATURES:
                _, probs, top1, expert_out, y_hat = forward_top1_sparse(
                    x, experts, router_w, router_b
                )
                err = y_hat - x
                selected_prob = probs[top1]

                grad_experts[top1] += selected_prob * np.outer(err, x)

                grad_selected_prob = float(err @ expert_out[top1])
                grad_logits = np.zeros(2, dtype=np.float64)
                for j in range(2):
                    indicator = 1.0 if j == top1 else 0.0
                    grad_logits[j] = grad_selected_prob * selected_prob * (indicator - probs[j])

                grad_w += np.outer(grad_logits, x)
                grad_b += grad_logits

            scale = 1.0 / len(FEATURES)
            experts -= lr * grad_experts * scale
            router_w -= lr * grad_w * scale
            router_b -= lr * grad_b * scale

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
    condition = str(row["condition"])
    condition_dir = FIG_DIR / condition
    condition_dir.mkdir(parents=True, exist_ok=True)

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
    ax.set_title(f"{condition} seed {row['seed']} step {row['step']}")
    for i in range(2):
        for j in range(2):
            ax.text(j, i, f"{heatmap[i, j]:.2f}", ha="center", va="center")
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
        losses = [float(r["loss"]) for r in seed_rows]
        gates = [float(r["mean_selected_gate"]) for r in seed_rows]

        fig, axes = plt.subplots(1, 3, figsize=(9.6, 2.8))
        axes[0].plot(steps, margins, marker="o")
        axes[0].set_title("route margin")
        axes[0].set_xlabel("step")
        axes[0].set_ylim(0, 1)
        axes[1].plot(steps, gates, marker="o")
        axes[1].set_title("selected gate")
        axes[1].set_xlabel("step")
        axes[1].set_ylim(0, 1)
        axes[2].plot(steps, losses, marker="o")
        axes[2].set_title("loss")
        axes[2].set_xlabel("step")
        fig.suptitle(f"{condition} seed {seed}")
        fig.tight_layout()
        fig.savefig(condition_dir / f"trajectory_seed{seed}.png", dpi=160)
        plt.close(fig)


def write_observations(condition: str, final_rows: list[dict[str, float | int | str]]) -> None:
    condition_dir = NOTE_DIR / condition
    condition_dir.mkdir(parents=True, exist_ok=True)
    separated = sum(1 for r in final_rows if r["pattern"] == "separated")
    margins = [float(r["mean_route_margin"]) for r in final_rows]
    nmis = [float(r["nmi"]) for r in final_rows]

    with (condition_dir / "run_observations.md").open("w", encoding="utf-8") as f:
        f.write(f"# {condition} Observations\n\n")
        f.write("Top-1 sparse forward; router gradient through selected softmax gate.\n\n")
        f.write(f"Separated final top-1 routing: {separated}/{len(final_rows)} seeds.\n")
        f.write(f"Mean final route margin: {np.mean(margins):.4f}.\n")
        f.write(f"Mean final NMI: {np.mean(nmis):.4f}.\n\n")
        for row in final_rows:
            f.write(
                f"- seed {row['seed']}: pattern={row['pattern']}, "
                f"top1_A={row['top1_A']}, top1_B={row['top1_B']}, "
                f"margin={float(row['mean_route_margin']):.4f}, "
                f"NMI={float(row['nmi']):.4f}, "
                f"accuracy={float(row['assignment_accuracy']):.4f}, "
                f"selected_gate={float(row['mean_selected_gate']):.4f}, "
                f"loss={float(row['loss']):.6f}\n"
            )


def main() -> None:
    conditions = [
        "top1_known_good",
        "top1_no_router_prior",
        "top1_no_prior_no_expert_advantage",
    ]
    seeds = [0, 1, 2]

    all_rows: list[dict[str, float | int | str]] = []
    summary_rows: list[dict[str, float | int | str]] = []

    for condition in conditions:
        rows = train_condition(condition, seeds=seeds)
        all_rows.extend(rows)
        final_rows = [r for r in rows if int(r["step"]) == 200]
        summary_rows.extend(final_rows)

        write_csv(TABLE_DIR / condition / "metrics_by_checkpoint.csv", rows)
        write_csv(TABLE_DIR / condition / "seed_checkpoint_summary.csv", final_rows)
        write_observations(condition, final_rows)

        for row in rows:
            if int(row["step"]) in {0, 50, 200}:
                save_heatmap(row)
        save_trajectory(condition, rows)

    write_csv(TABLE_DIR / "all_conditions_by_checkpoint.csv", all_rows)
    write_csv(TABLE_DIR / "all_conditions_final_summary.csv", summary_rows)

    print("Wrote top1 sparse proxy artifacts to:")
    print(TABLE_DIR)
    print(FIG_DIR)
    print(NOTE_DIR)


if __name__ == "__main__":
    main()
