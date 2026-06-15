from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle


OUT = Path(__file__).resolve().parent / "figures"
OUT.mkdir(parents=True, exist_ok=True)

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 12,
    "axes.titlesize": 18,
    "axes.labelsize": 12,
    "figure.dpi": 160,
})


COL = {
    "ink": "#17202a",
    "muted": "#6b7280",
    "blue": "#2563eb",
    "cyan": "#0891b2",
    "green": "#16a34a",
    "orange": "#ea580c",
    "red": "#dc2626",
    "purple": "#7c3aed",
    "gray": "#e5e7eb",
    "light": "#f8fafc",
}


def clean(ax):
    ax.set_xticks([])
    ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)


def box(ax, xy, w, h, title, body="", fc="#ffffff", ec="#1f2937", lw=1.4):
    patch = FancyBboxPatch(
        xy, w, h,
        boxstyle="round,pad=0.02,rounding_size=0.025",
        linewidth=lw, edgecolor=ec, facecolor=fc,
    )
    ax.add_patch(patch)
    ax.text(xy[0] + w / 2, xy[1] + h * 0.63, title,
            ha="center", va="center", color=COL["ink"], weight="bold", fontsize=13)
    if body:
        ax.text(xy[0] + w / 2, xy[1] + h * 0.30, body,
                ha="center", va="center", color=COL["muted"], fontsize=10, linespacing=1.25)
    return patch


def arrow(ax, start, end, color="#374151", lw=1.8):
    arr = FancyArrowPatch(start, end, arrowstyle="-|>", mutation_scale=16,
                          linewidth=lw, color=color, shrinkA=5, shrinkB=5)
    ax.add_patch(arr)


def save(fig, name):
    fig.savefig(OUT / name, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def background_gap():
    fig, ax = plt.subplots(figsize=(13.2, 7.2))
    clean(ax)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.text(0.03, 0.94, "Why study sparse MoE gating?", fontsize=22, weight="bold", color=COL["ink"])
    ax.text(0.03, 0.885,
            "Sparse MoE scales parameters, but top-1 routing decides which experts actually learn.",
            fontsize=12, color=COL["muted"])

    box(ax, (0.04, 0.55), 0.24, 0.22, "MoE promise",
        "More parameters\nnear-constant token compute",
        fc="#eff6ff", ec=COL["blue"])
    box(ax, (0.38, 0.55), 0.24, 0.22, "Router bottleneck",
        "Top-1 gate sends each token\nto one expert",
        fc="#ecfeff", ec=COL["cyan"])
    box(ax, (0.72, 0.55), 0.24, 0.22, "Failure mode",
        "Early bias can create\nexpert underuse",
        fc="#fff7ed", ec=COL["orange"])

    arrow(ax, (0.29, 0.66), (0.37, 0.66), COL["muted"])
    arrow(ax, (0.63, 0.66), (0.71, 0.66), COL["muted"])

    box(ax, (0.18, 0.17), 0.64, 0.21, "Research gap",
        "Load balance tells how many tokens each expert receives.\n"
        "It does not tell whether routing is driven by useful feature differences\n"
        "or by common hidden components amplified during early training.",
        fc=COL["light"], ec="#111827", lw=1.6)
    arrow(ax, (0.84, 0.54), (0.62, 0.39), COL["orange"], lw=2.0)
    save(fig, "s02_background_gap_diagram.png")


def evidence_storyline():
    fig, ax = plt.subplots(figsize=(13.2, 7.2))
    clean(ax)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.text(0.03, 0.94, "Storyline: from audit to mechanism", fontsize=22, weight="bold", color=COL["ink"])

    items = [
        ("1. Consistency is not enough", "High route consistency can hide collapse", COL["red"]),
        ("2. Specialization is reachable", "Slot-aware init enters a better basin", COL["green"]),
        ("3. Common-logit bias", "$w_e^T c$ acts as expert-specific bias", COL["blue"]),
        ("4. Real-text update", "Step-0 bias exists; step-10 amplification dominates", COL["orange"]),
        ("5. Next mechanism", "Common-filtered initialization + anti-lock-in routing", COL["purple"]),
    ]
    ys = [0.78, 0.66, 0.54, 0.42, 0.30]
    for i, ((title, body, color), y) in enumerate(zip(items, ys)):
        ax.add_patch(Rectangle((0.08, y - 0.035), 0.055, 0.07, facecolor=color, edgecolor=color))
        ax.text(0.1075, y, str(i + 1), color="white", ha="center", va="center", fontsize=14, weight="bold")
        box(ax, (0.16, y - 0.045), 0.72, 0.09, title, body,
            fc="#ffffff", ec=color, lw=1.4)
        if i < len(ys) - 1:
            arrow(ax, (0.1075, y - 0.04), (0.1075, ys[i + 1] + 0.04), color=COL["muted"], lw=1.4)

    box(ax, (0.18, 0.08), 0.64, 0.13, "Talk thesis",
        "The project is now a mechanism audit: early route concentration is not only a load issue,\n"
        "but a router-input geometry and early-training feedback problem.",
        fc="#f9fafb", ec="#111827", lw=1.5)
    save(fig, "s03_storyline_ladder.png")


def common_logit_model():
    fig, ax = plt.subplots(figsize=(13.2, 7.2))
    clean(ax)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.text(0.03, 0.94, "Mechanism: common component becomes expert-specific bias",
            fontsize=21, weight="bold", color=COL["ink"])

    box(ax, (0.06, 0.62), 0.20, 0.18, "Router input", "$h_i = c + r_i$", fc="#eff6ff", ec=COL["blue"])
    box(ax, (0.40, 0.62), 0.20, 0.18, "Gate score", "$z_{i,e}=w_e^T h_i$", fc="#ecfeff", ec=COL["cyan"])
    box(ax, (0.74, 0.62), 0.20, 0.18, "Top-1 route", "$e_i=argmax_e z_{i,e}$", fc="#fff7ed", ec=COL["orange"])
    arrow(ax, (0.27, 0.71), (0.39, 0.71), COL["muted"])
    arrow(ax, (0.61, 0.71), (0.73, 0.71), COL["muted"])

    ax.text(0.08, 0.45, "$z_{i,e}=w_e^T c + w_e^T r_i$",
            fontsize=28, color=COL["ink"])
    ax.text(0.12, 0.38, "common score", fontsize=12, color=COL["blue"], weight="bold")
    ax.text(0.40, 0.38, "residual / feature score", fontsize=12, color=COL["green"], weight="bold")

    box(ax, (0.08, 0.17), 0.38, 0.17, "Why it biases top-1",
        "$w_e^T c$ does not depend on token feature,\n"
        "but differs across experts.",
        fc="#fef2f2", ec=COL["red"])
    box(ax, (0.54, 0.17), 0.38, 0.17, "Design implication",
        "Equalize, filter, or isolate common directions\n"
        "before residual feature dispatch.",
        fc="#f5f3ff", ec=COL["purple"])
    save(fig, "s06_common_logit_model.png")


def position_source_simple():
    labels = ["baseline", "zero routed\nposition", "zero all\npositions", "random feature\nposition"]
    max_load = [0.62, 0.345, 0.345, 0.40]
    common_ratio = [0.51, 0.045, 0.035, 0.082]

    fig, ax = plt.subplots(figsize=(13.2, 7.2))
    x = range(len(labels))
    width = 0.35
    ax.bar([i - width/2 for i in x], max_load, width, label="step-0 max load", color=COL["blue"])
    ax.bar([i + width/2 for i in x], common_ratio, width, label="common ratio", color=COL["orange"])
    ax.axhline(0.25, color=COL["muted"], linestyle="--", linewidth=1.2, label="balanced load for 4 experts")
    ax.set_ylim(0, 0.72)
    ax.set_xticks(list(x))
    ax.set_xticklabels(labels)
    ax.set_ylabel("Value")
    ax.set_title("Position/source ablation: common offset is causal but not sufficient")
    ax.legend(loc="upper right", frameon=True)
    ax.grid(axis="y", alpha=0.25)
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)
    ax.text(0.02, 0.67,
            "Zeroing the routed position reduces common ratio and step-0 load,\n"
            "but later slot specialization still needs a better routing mechanism.",
            transform=ax.transAxes, fontsize=11, color=COL["muted"], va="top")
    save(fig, "s08_position_source_simplified.png")


def freeze_split_bar():
    labels = ["normal", "freeze\ngate", "freeze\nexperts", "freeze\nprefix before L5"]
    common_delta = [1.2760, 0.5354, 0.1919, 0.0278]
    load_delta = [0.7334, 0.7314, 0.7183, 0.0660]

    fig, ax = plt.subplots(figsize=(13.2, 7.2))
    x = range(len(labels))
    width = 0.36
    ax.bar([i - width/2 for i in x], common_delta, width, label="common-margin delta", color=COL["purple"])
    ax.bar([i + width/2 for i in x], load_delta, width, label="raw max-load delta", color=COL["orange"])
    ax.set_xticks(list(x))
    ax.set_xticklabels(labels)
    ax.set_ylabel("Step 0 -> 10 change, layer 5")
    ax.set_title("Freeze split: raw concentration and common-margin spike are related, not identical")
    ax.legend(loc="upper right", frameon=True)
    ax.grid(axis="y", alpha=0.25)
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)
    ax.text(0.02, 0.92,
            "Fixed gate can still concentrate raw top-1 load.\n"
            "Full common-margin spike needs hidden-producing path + gate-hidden interaction.",
            transform=ax.transAxes, fontsize=11, color=COL["muted"], va="top")
    save(fig, "s11_freeze_split_key_numbers.png")


def next_mechanism():
    fig, ax = plt.subplots(figsize=(13.2, 7.2))
    clean(ax)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.text(0.03, 0.94, "Next mechanism hypothesis: common-filtered, coupling-preserving routing",
            fontsize=20, weight="bold", color=COL["ink"])

    box(ax, (0.04, 0.58), 0.20, 0.18, "Estimate common\nsubspace", "$C$ from router inputs", fc="#eef2ff", ec=COL["purple"])
    box(ax, (0.30, 0.58), 0.20, 0.18, "Filter token\ninput", "$r=(I-P_C)h$", fc="#ecfeff", ec=COL["cyan"])
    box(ax, (0.56, 0.58), 0.20, 0.18, "Preserve\ncoupling", "router-expert\nresidual geometry", fc="#f0fdf4", ec=COL["green"])
    box(ax, (0.82, 0.58), 0.14, 0.18, "Initialize\nrouter", "residual-aware\nscores", fc="#fff7ed", ec=COL["orange"])
    arrow(ax, (0.25, 0.67), (0.29, 0.67), COL["muted"])
    arrow(ax, (0.51, 0.67), (0.55, 0.67), COL["muted"])
    arrow(ax, (0.77, 0.67), (0.81, 0.67), COL["muted"])

    box(ax, (0.10, 0.19), 0.36, 0.20, "What it should reduce",
        "early common-margin amplification\nand gate-hidden interaction",
        fc="#fef2f2", ec=COL["red"])
    box(ax, (0.54, 0.19), 0.36, 0.20, "What it must preserve",
        "task loss, effective experts,\nand useful router-expert coupling",
        fc="#f9fafb", ec="#111827")
    save(fig, "s12_next_mechanism_hypothesis.png")


if __name__ == "__main__":
    background_gap()
    evidence_storyline()
    common_logit_model()
    position_source_simple()
    freeze_split_bar()
    next_mechanism()
