"""Render the two existing held-out comparisons used in the 28 November meeting."""
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter

ROOT = Path(__file__).resolve().parents[3]
RUNS = Path("/data/250010109/MoE_Router/experiments")
FIGURES = ROOT / "research/small-model-moe/main/explore/1128_feature_grouping/figures"
ROUTING = RUNS / "1126_sae_feature_clusters/night_overlap/table3_routing.csv"
ORACLE = RUNS / "1127_qwen_hd4_oracle/runs/formal/Qwen-HD4-Oracle"
METRICS = [("overall", "Overall", "o", "#233e5b"),
           ("rare", "Rare target word", "D", "#a4481d"),
           ("sae_low", "Low-frequency SAE", "s", "#207563")]
BUDGETS = (500_000_000, 1_000_000_000, 3_000_000_000)


def read_rows(path):
    with path.open(newline="") as source:
        return list(csv.DictReader(source))


def main():
    FIGURES.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({"pdf.fonttype": 42, "font.size": 10, "axes.spines.top": False,
                         "axes.spines.right": False, "axes.axisbelow": True})
    fig, (coverage, loss) = plt.subplots(1, 2, figsize=(9.1, 3.95),
                                         gridspec_kw={"width_ratios": [0.9, 1.3]})
    fig.subplots_adjust(left=0.085, right=0.985, bottom=0.22, top=0.77, wspace=0.36)
    checks = []
    hidden = {r["policy"]: r for r in read_rows(ROUTING)
              if r["group"] == "hier" and r["task"] == "hidden_lowfreq"}
    for index, (policy, color) in enumerate([("one_parent", "#aab6c4"), ("free", "#406b80")]):
        row = hidden[policy]
        assert (int(row["docs"]), int(row["eligible"])) == (1009, 15309)
        value = float(row["top2"])
        coverage.bar(index, value, width=0.55, color=color)
        coverage.text(index, value + 0.014, f"{value:.2%}", ha="center")
        checks.append(("A", policy, "", value, "", "", "fraction", str(ROUTING)))
    coverage.set(xticks=(0, 1), xticklabels=("Same parent", "Any parent"),
                 ylabel="Hidden low-frequency energy covered", ylim=(0, 0.55))
    coverage.yaxis.set_major_formatter(PercentFormatter(1, decimals=0))
    coverage.set_title("A   Access to two leaves", loc="left", pad=12, weight="bold")
    for index, budget in enumerate(BUDGETS):
        source = ORACLE / f"paired_{budget}.csv"
        row = next(r for r in read_rows(source) if r["model"] == "A0")
        assert row["status"] == "measured"
        for slot, (key, label, marker, color) in enumerate(METRICS):
            delta, low, high = (float(row[f"{key}_{suffix}"]) for suffix in ("delta", "lo", "hi"))
            assert low <= delta <= high
            loss.errorbar(index + 0.16 * (slot - 1), delta,
                          yerr=[[delta - low], [high - delta]], fmt=marker, color=color,
                          markersize=5.2, capsize=3, label=label if index == 0 else None)
            checks.append(("B", label, budget, delta, low, high, "nat", str(source)))
    loss.axhline(0, lw=1, ls="--", color="#666")
    loss.set(xticks=range(3), xticklabels=("0.5B", "1B", "3B"), xlim=(-0.5, 2.5),
             ylim=(-0.124, 0.015), xlabel="Training tokens", ylabel="Held-out NLL change (nats)")
    loss.set_title("B   Deep Qwen oracle minus A0", loc="left", pad=12, weight="bold")
    handles, labels = loss.get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper right", bbox_to_anchor=(0.99, 0.99),
               ncol=3, frameon=False, fontsize=9, columnspacing=1.2)
    for ax in (coverage, loss):
        ax.grid(axis="y", alpha=0.18)
    for ext in ("pdf", "png"):
        fig.savefig(FIGURES / f"feature_grouping.{ext}", dpi=300)
    plt.close(fig)
    with (FIGURES / "numeric_check.csv").open("w", newline="") as out:
        table = csv.writer(out)
        table.writerow(("panel", "condition", "training_tokens", "value", "lo95", "hi95", "unit", "source"))
        table.writerows(checks)


if __name__ == "__main__":
    main()
