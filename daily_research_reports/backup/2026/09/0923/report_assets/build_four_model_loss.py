#!/usr/bin/env python3
"""Plot four observed LM-loss trajectories on the common 0–21B token range."""
from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
from datetime import datetime, timezone
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

RESEARCH = Path("/data/250010109/Research_System")
EXPERIMENTS = Path("/data/250010109/MoE_Router/experiments")
HERE = RESEARCH / "daily_research_reports/0923"
SOURCE_SCRIPT = RESEARCH / "daily_research_reports/0922/report_assets/build_training_loss_comparison.py"
FIG = HERE / "figures/sae_four_model_lm_loss_21b.png"
TABLE = HERE / "tables/sae_four_model_lm_loss_21b.csv"
MANIFEST = HERE / "report_assets/sae_four_model_lm_loss_21b_manifest.json"
END = 21_000_000_000
GRID = 25_000_000
WINDOW = 100_000_000
FORK = 15_465_567_744


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    spec = importlib.util.spec_from_file_location("loss_source", SOURCE_SCRIPT)
    assert spec and spec.loader
    import sys
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    by_key = {m.key: m for m in module.MODELS}
    reweighted = module.Model(
        key="s7_reweighted", label="S7", short_label="S7",
        color="#D55E00", linestyle="-.", linewidth=2.5,
        objective="L_LM + λ L_rec + (1/32) L_AuxK; λ changes from 1 to 0.1",
        architecture="Final raw-Attention SAE sidecar; continuation fork at 15.465567744B.",
        token_order_note="A forked training history; microbatch and CE chunking changed.",
        sources=(
            module.Source(EXPERIMENTS /
                "20260916_attention_output_sidecar_last_50b/runs/formal50b_last_attention_4h100/metrics.jsonl",
                FORK),
            module.Source(EXPERIMENTS /
                "20260917_attention_output_sidecar_last_reweighted_resume/runs/formal50b_last_attention_lambda0p1_mbs16_fork_4h100/metrics.jsonl"),
        ),
    )
    from dataclasses import replace
    fresh = replace(by_key["s7_lambda0p1"], label="Fresh S7", short_label="Fresh S7")
    sall = replace(by_key["sall"], label="SALL", short_label="SALL")
    models = (by_key["dense"], reweighted, fresh, sall)
    loaded = {m.key: module.load_model(m) for m in models}
    assert all(int(x.tokens[-1]) >= END for x in loaded.values())
    ticks = np.arange(WINDOW, END + 1, GRID, dtype=np.int64)
    curves = {m.key: np.array([loaded[m.key].mean(int(t - WINDOW), int(t)) for t in ticks])
              for m in models}
    summary = {m.key: {"label": m.short_label,
        "window_19_21b_mean": loaded[m.key].mean(19_000_000_000, END),
        "at_15b_trailing100m": loaded[m.key].mean(15_000_000_000 - WINDOW, 15_000_000_000),
        "at_17b_trailing100m": loaded[m.key].mean(17_000_000_000 - WINDOW, 17_000_000_000),
        "last_observed_tokens": int(loaded[m.key].tokens[-1]),
        "sources": loaded[m.key].source_metadata} for m in models}
    TABLE.parent.mkdir(parents=True, exist_ok=True)
    with TABLE.open("w", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(["model", "lm_loss_19_21b_token_weighted", "trailing100m_at15b",
                         "trailing100m_at17b", "last_observed_valid_tokens"])
        for m in models:
            s = summary[m.key]
            writer.writerow([m.short_label, f"{s['window_19_21b_mean']:.9f}",
                             f"{s['at_15b_trailing100m']:.9f}",
                             f"{s['at_17b_trailing100m']:.9f}", s["last_observed_tokens"]])
    FIG.parent.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({"font.size": 10, "axes.spines.top": False,
                         "axes.spines.right": False})
    fig, axes = plt.subplots(1, 2, figsize=(12.5, 4.6), gridspec_kw={"width_ratios": [1.35, 1]})
    for m in models:
        x = ticks / 1e9
        y = curves[m.key]
        axes[0].plot(x, y, label=m.short_label, color=m.color,
                     linestyle=m.linestyle, lw=m.linewidth)
        if m.key != "dense":
            recent = x >= 14
            delta = curves["dense"] - y
            axes[1].plot(x[recent], delta[recent],
                         label=m.short_label,
                         color=m.color, linestyle=m.linestyle, lw=m.linewidth)
    for ax in axes:
        ax.set_xlabel("Cumulative valid prediction tokens (B)")
        ax.axvline(15, color="#999999", lw=.8, alpha=.5)
        ax.axvline(17, color="#999999", lw=.8, alpha=.5)
        ax.grid(alpha=.2, axis="y")
    axes[0].set_ylabel("LM loss, trailing 100M-token mean")
    axes[1].set_ylabel("Dense loss − model loss")
    axes[1].set_title("Positive means lower loss than Dense", fontsize=10)
    axes[1].axhline(0, color="#222222", lw=1, alpha=.75)
    axes[0].set_xlim(0, 21)
    axes[1].set_xlim(14, 21)
    delta_arrays = [curves["dense"] - curves[m.key] for m in models if m.key != "dense"]
    local_values = np.concatenate([v[ticks >= 14_000_000_000] for v in delta_arrays])
    bound = max(.005, float(np.quantile(np.abs(local_values), .995)) * 1.15)
    axes[1].set_ylim(-bound, bound)
    axes[0].legend(frameon=False, loc="upper right")
    fig.suptitle("LM loss trajectory and local reduction relative to Dense", weight="bold")
    fig.text(.5, .015, "Descriptive training telemetry; SALL sample order and S7 fork history are not strictly matched.",
             ha="center", fontsize=8, color="#555555")
    fig.tight_layout(rect=[0, .04, 1, .94])
    fig.savefig(FIG, dpi=180)
    plt.close(fig)
    manifest = {"created_at_utc": datetime.now(timezone.utc).isoformat(),
                "figure": str(FIG), "figure_sha256": sha(FIG),
                "table": str(TABLE), "table_sha256": sha(TABLE),
                "source_script": str(SOURCE_SCRIPT), "source_script_sha256": sha(SOURCE_SCRIPT),
                "common_end_valid_tokens": END, "smoothing_window_valid_tokens": WINDOW,
                "comparison_window_valid_tokens": [19_000_000_000, END],
                "reweighted_fork_valid_tokens": FORK, "models": summary,
                "claim_boundary": "Training LM loss on observed tokens only; not throughput, held-out quality, or isolated causal effects."}
    MANIFEST.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    print(json.dumps({k: v["window_19_21b_mean"] for k, v in summary.items()}, sort_keys=True))


if __name__ == "__main__":
    main()
