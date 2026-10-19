#!/usr/bin/env python3
"""Render longer-window Dense/S7/SALL LM-loss views through exact 30B."""

from __future__ import annotations

import csv
import json
from datetime import datetime, timezone

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MultipleLocator

import build_dense_s7_sall_loss_30b as base


START = 20_000_000_000
END = 30_000_000_000
GRID = 25_000_000
DISPLAY_WINDOWS = (500_000_000, 2_000_000_000)
SUMMARY_WINDOWS = (
    ("20B-30B", 20_000_000_000),
    ("25B-30B", 25_000_000_000),
    ("28B-30B", 28_000_000_000),
    ("29B-30B", 29_000_000_000),
)


def main() -> None:
    font = base.configure_plot()
    base.OUT.mkdir(parents=True, exist_ok=True)
    base.TABLES.mkdir(parents=True, exist_ok=True)
    loaded = {model.key: base.load_model(model) for model in base.MODELS}

    summary_rows: list[dict[str, object]] = []
    for label, start in SUMMARY_WINDOWS:
        values = {key: data.mean(start, END) for key, data in loaded.items()}
        for model in base.MODELS:
            value = values[model.key]
            summary_rows.append({
                "window": label,
                "start_tokens": start,
                "stop_tokens": END,
                "window_billions": (END - start) / 1e9,
                "model_key": model.key,
                "mean_lm_loss": f"{value:.12f}",
                "delta_vs_dense_millinats": f"{1000 * (value - values['dense']):.9f}",
                "delta_vs_sall_millinats": f"{1000 * (value - values['sall']):.9f}",
            })
    summary_path = base.TABLES / "long_endpoint_windows_to_30b.csv"
    with summary_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(summary_rows[0]))
        writer.writeheader()
        writer.writerows(summary_rows)

    fig, axes = plt.subplots(2, 2, figsize=(15.3, 10.0), constrained_layout=True)
    for column, window in enumerate(DISPLAY_WINDOWS):
        grid = np.arange(max(START, window), END + 1, GRID, dtype=np.int64)
        grid = np.unique(np.append(grid, END))
        curves: dict[str, np.ndarray] = {}
        for model in base.MODELS:
            curves[model.key] = np.asarray([
                loaded[model.key].mean(int(token - window), int(token)) for token in grid
            ])

        ax_abs = axes[0, column]
        ax_delta = axes[1, column]
        for model in base.MODELS:
            x = grid / 1e9
            ax_abs.plot(x, curves[model.key], color=model.color,
                        linestyle=model.linestyle, linewidth=2.5, label=model.short)
            delta = 1000 * (curves[model.key] - curves["dense"])
            ax_delta.plot(x, delta, color=model.color, linestyle=model.linestyle,
                          linewidth=2.35, label=model.short)
        title_window = f"{window / 1e9:g}B"
        ax_abs.set_title(f"{'AB'[column]}  {title_window} 词元尾随平均 $L_{{LM}}$", loc="left", fontproperties=font)
        ax_abs.set_xlim(20, 30)
        ax_abs.xaxis.set_major_locator(MultipleLocator(1))
        ax_abs.set_xlabel("累计有效预测词元（B）", fontproperties=font)
        ax_abs.set_ylabel("训练 $L_{LM}$", fontproperties=font)
        ax_abs.grid(alpha=0.22)
        if column == 0:
            ax_abs.legend(frameon=False, prop=font)

        ax_delta.axhline(0, color="#777777", linewidth=1.0)
        ax_delta.set_title(f"{'CD'[column]}  {title_window} 窗口相对 Dense", loc="left", fontproperties=font)
        ax_delta.set_xlim(20, 30)
        ax_delta.xaxis.set_major_locator(MultipleLocator(1))
        ax_delta.set_xlabel("累计有效预测词元（B）", fontproperties=font)
        ax_delta.set_ylabel("$\Delta L_{LM}$ vs Dense（millinats）", fontproperties=font)
        ax_delta.grid(alpha=0.22)

    # Rewrite the curve table with correctly aligned deltas after all model curves exist.
    curve_rows: list[dict[str, object]] = []
    for window in DISPLAY_WINDOWS:
        grid = np.arange(max(START, window), END + 1, GRID, dtype=np.int64)
        grid = np.unique(np.append(grid, END))
        curves = {
            model.key: np.asarray([
                loaded[model.key].mean(int(token - window), int(token)) for token in grid
            ]) for model in base.MODELS
        }
        for model in base.MODELS:
            for index, (token, value) in enumerate(zip(grid, curves[model.key])):
                curve_rows.append({
                    "window_tokens": window,
                    "tokens": int(token),
                    "model_key": model.key,
                    "trailing_mean_lm_loss": f"{value:.12f}",
                    "delta_vs_dense_millinats": f"{1000 * (value - curves['dense'][index]):.9f}",
                })
    curve_path = base.TABLES / "long_window_curve_grid_25m.csv"
    with curve_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(curve_rows[0]))
        writer.writeheader()
        writer.writerows(curve_rows)

    fig.suptitle(
        "Dense、S7 λrec=0.1 与 SALL：拉长信息窗口后的 20–30B 训练损失\n"
        "左：500M 尾随窗口；右：2B 尾随窗口；仅比较全局词元归一化 $L_{LM}$",
        fontsize=16, fontproperties=font,
    )
    png = base.OUT / "training_lm_loss_dense_s7_sall_long_windows_to_30b.png"
    pdf = base.OUT / "training_lm_loss_dense_s7_sall_long_windows_to_30b.pdf"
    fig.savefig(png, dpi=220, bbox_inches="tight")
    fig.savefig(pdf, bbox_inches="tight")
    plt.close(fig)

    manifest = {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "comparison_endpoint_tokens": END,
        "display_range_tokens": [START, END],
        "display_trailing_windows_tokens": list(DISPLAY_WINDOWS),
        "summary_windows": summary_rows,
        "observed_endpoints": {key: int(data.tokens[-1]) for key, data in loaded.items()},
        "primary_metric": "globally token-weighted training lm_loss",
        "boundary": "Single-seed training loss only; SALL initial sample order differs from the strict Dense/S7 pairing.",
        "outputs": {"figure_png": str(png), "figure_pdf": str(pdf),
                    "summary_csv": str(summary_path), "curve_csv": str(curve_path)},
    }
    (base.TABLES / "long_window_manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps({"figure": str(png), "summary": summary_rows}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
