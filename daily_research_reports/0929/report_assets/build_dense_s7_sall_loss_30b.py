#!/usr/bin/env python3
"""Build an exact token-aligned Dense/S7/SALL LM-loss comparison at 30B.

Only globally token-normalized language-model loss is compared. Total losses
are intentionally excluded because the three objectives contain different SAE
terms and coefficients.
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager
from matplotlib.font_manager import FontProperties
from matplotlib.ticker import MultipleLocator


RESEARCH = Path("/data/250010109/Research_System")
EXPERIMENTS = Path("/data/250010109/MoE_Router/experiments")
SCRIPT = RESEARCH / "daily_research_reports/0929/report_assets/build_dense_s7_sall_loss_30b.py"
OUT = RESEARCH / "daily_research_reports/0929/figures/training_loss_30b"
TABLES = RESEARCH / "daily_research_reports/0929/tables/training_loss_30b"
FONT_PATH = RESEARCH / "daily_research_reports/0921/report_assets/fonts/NotoSansCJKsc-Regular.otf"

END = 30_000_000_000
LOCAL_START = 28_000_000_000
SMOOTH = 100_000_000
GRID = 25_000_000


@dataclass(frozen=True)
class Source:
    path: Path
    ceiling: int | None = None


@dataclass(frozen=True)
class Model:
    key: str
    label: str
    short: str
    color: str
    linestyle: str
    marker: str
    objective: str
    comparability: str
    sources: tuple[Source, ...]


MODELS = (
    Model(
        key="dense",
        label="Dense（原生主干）",
        short="Dense",
        color="#222222",
        linestyle="--",
        marker="o",
        objective="L_LM",
        comparability="Reference four-lane sample order preserved across the eight-rank continuation.",
        sources=(
            Source(EXPERIMENTS / "20260913_dense_baseline_pretraining/runs/full_10b_8x5090_20260913T102944Z/metrics.jsonl", 10_000_000_000),
            Source(EXPERIMENTS / "20260913_dense_baseline_pretraining/runs/full_50b_continue_from_10b_8x5090_r2_20260915T131706Z/metrics.jsonl", 22_018_691_584),
            Source(EXPERIMENTS / "20260928_dense_sall_8x5090_continue/runs/dense_baseline_continue_from_22p018691584b_8x5090/metrics.jsonl"),
        ),
    ),
    Model(
        key="s7",
        label="S7（末层 Attention 旁路，λrec=0.1）",
        short="S7 λrec=0.1",
        color="#7B2CBF",
        linestyle="-",
        marker="s",
        objective="L_LM + 0.1 L_rec + (1/32) L_AuxK",
        comparability="Native four-rank reference sample order; strictest matched sidecar comparison is S7 versus Dense.",
        sources=(
            Source(EXPERIMENTS / "20260920_s7_lambda0p1_from_scratch_4h100/runs/S7_lambda0p1_from_scratch_4h100/metrics.jsonl"),
        ),
    ),
    Model(
        key="sall",
        label="SALL（8层 Attention 旁路，λrec=1）",
        short="SALL 8-sidecar",
        color="#009E73",
        linestyle="-.",
        marker="^",
        objective="L_LM + 1.0 L_rec + (1/32) L_AuxK",
        comparability="Same data manifest and global token batch, but the initial eight-rank segment used a different per-update sample order.",
        sources=(
            Source(EXPERIMENTS / "20260916_attention_output_sidecar_multisite_50b/runs/formal50b_all_layers_8xh100_spot/metrics.jsonl", 9_174_381_056),
            Source(EXPERIMENTS / "20260918_attention_output_sidecar_all8_4h100_resume/runs/formal50b_all8_unit_weight_4h100_mbs16_resume/metrics.jsonl", 23_000_000_000),
            Source(EXPERIMENTS / "20260928_dense_sall_8x5090_continue/runs/sall_unit_weight_continue_from_23b_8x5090/metrics.jsonl"),
        ),
    ),
)


@dataclass
class Loaded:
    tokens: np.ndarray
    losses: np.ndarray
    counts: np.ndarray
    starts: np.ndarray
    weighted_prefix: np.ndarray
    covered_prefix: np.ndarray
    source_metadata: list[dict[str, object]]

    def integral(self, x: float, weighted: bool) -> float:
        if x <= 0:
            return 0.0
        prefix = self.weighted_prefix if weighted else self.covered_prefix
        index = int(np.searchsorted(self.tokens, x, side="right"))
        result = float(prefix[index])
        if index < len(self.tokens) and x > self.starts[index]:
            span = min(float(x), float(self.tokens[index])) - float(self.starts[index])
            if span > 0:
                result += span * (float(self.losses[index]) if weighted else 1.0)
        return result

    def mean(self, start: int, stop: int) -> float:
        if not (0 <= start < stop <= int(self.tokens[-1])):
            raise ValueError(f"window outside observed range: {start:,}--{stop:,}")
        numerator = self.integral(stop, True) - self.integral(start, True)
        denominator = self.integral(stop, False) - self.integral(start, False)
        if abs(denominator - (stop - start)) > 1.0:
            raise RuntimeError(
                f"coverage gap in {start:,}--{stop:,}: covered={denominator:,.0f}"
            )
        return numerator / denominator


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def parse_source(source: Source) -> tuple[dict[int, tuple[float, int]], dict[str, object]]:
    payload = source.path.read_bytes()
    points: dict[int, tuple[float, int]] = {}
    parsed = malformed = 0
    raw_last = 0
    for line in payload.splitlines():
        try:
            row = json.loads(line)
            token = int(row["actual_lm_tokens"])
            loss = float(row["lm_loss"])
            count = int(row["lm_tokens"])
        except (json.JSONDecodeError, UnicodeDecodeError, KeyError, TypeError, ValueError):
            malformed += 1
            continue
        parsed += 1
        raw_last = max(raw_last, token)
        if token <= 0 or count <= 0 or not math.isfinite(loss):
            continue
        if source.ceiling is not None and token > source.ceiling:
            continue
        points[token] = (loss, count)
    stat = source.path.stat()
    return points, {
        "path": str(source.path),
        "source_ceiling_tokens": source.ceiling,
        "sha256_of_read_snapshot": sha256_bytes(payload),
        "snapshot_bytes": len(payload),
        "filesystem_size_after_read": stat.st_size,
        "filesystem_mtime_utc_after_read": datetime.fromtimestamp(stat.st_mtime, timezone.utc).isoformat(),
        "parsed_rows": parsed,
        "malformed_rows": malformed,
        "used_rows": len(points),
        "raw_last_token": raw_last,
        "used_last_token": max(points) if points else None,
    }


def load_model(model: Model) -> Loaded:
    merged: dict[int, tuple[float, int]] = {}
    metadata: list[dict[str, object]] = []
    for source in model.sources:
        points, meta = parse_source(source)
        merged.update(points)
        metadata.append(meta)
    tokens = np.asarray(sorted(merged), dtype=np.int64)
    losses = np.asarray([merged[int(t)][0] for t in tokens], dtype=np.float64)
    counts = np.asarray([merged[int(t)][1] for t in tokens], dtype=np.int64)
    starts = tokens - counts
    if int(starts[0]) != 0:
        raise RuntimeError(f"{model.key}: trajectory does not start at token zero")
    gaps = starts[1:] - tokens[:-1]
    if np.any(gaps != 0):
        bad = np.flatnonzero(gaps != 0)[:10]
        raise RuntimeError(
            f"{model.key}: non-contiguous intervals at {bad.tolist()}, gaps={gaps[bad].tolist()}"
        )
    if int(tokens[-1]) < END:
        raise RuntimeError(f"{model.key}: endpoint {int(tokens[-1]):,} is below 30B")
    weighted_prefix = np.concatenate([[0.0], np.cumsum(losses * counts, dtype=np.float64)])
    covered_prefix = np.concatenate([[0.0], np.cumsum(counts, dtype=np.float64)])
    return Loaded(tokens, losses, counts, starts, weighted_prefix, covered_prefix, metadata)


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def configure_plot() -> FontProperties:
    font_manager.fontManager.addfont(str(FONT_PATH))
    font = FontProperties(fname=str(FONT_PATH))
    plt.rcParams.update({
        "font.family": font.get_name(),
        "axes.unicode_minus": False,
        "font.size": 10.8,
        "axes.titlesize": 12.6,
        "axes.labelsize": 11.3,
        "axes.spines.top": False,
        "axes.spines.right": False,
    })
    return font


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    TABLES.mkdir(parents=True, exist_ok=True)
    font = configure_plot()
    loaded = {model.key: load_model(model) for model in MODELS}

    windows = (
        ("28B-30B", 28_000_000_000, END),
        ("29B-30B", 29_000_000_000, END),
        ("29.9B-30B", 29_900_000_000, END),
    )
    summary_rows: list[dict[str, object]] = []
    for window_name, start, stop in windows:
        values = {model.key: loaded[model.key].mean(start, stop) for model in MODELS}
        for model in MODELS:
            value = values[model.key]
            summary_rows.append({
                "window": window_name,
                "start_tokens": start,
                "stop_tokens": stop,
                "model_key": model.key,
                "model_label": model.label,
                "mean_lm_loss": f"{value:.12f}",
                "delta_vs_dense_millinats": f"{1000 * (value - values['dense']):.9f}",
                "delta_vs_sall_millinats": f"{1000 * (value - values['sall']):.9f}",
            })
    write_csv(TABLES / "local_window_summary.csv", summary_rows)

    block_rows: list[dict[str, object]] = []
    for index, start in enumerate(range(LOCAL_START, END, SMOOTH), start=1):
        stop = start + SMOOTH
        values = {model.key: loaded[model.key].mean(start, stop) for model in MODELS}
        for model in MODELS:
            block_rows.append({
                "block_index": index,
                "start_tokens": start,
                "stop_tokens": stop,
                "model_key": model.key,
                "mean_lm_loss": f"{values[model.key]:.12f}",
                "delta_vs_dense_millinats": f"{1000 * (values[model.key] - values['dense']):.9f}",
                "delta_vs_sall_millinats": f"{1000 * (values[model.key] - values['sall']):.9f}",
            })
    write_csv(TABLES / "local_100m_blocks_28b_30b.csv", block_rows)

    grid = np.arange(SMOOTH, END + 1, GRID, dtype=np.int64)
    grid = np.unique(np.append(grid, END))
    curves: dict[str, np.ndarray] = {}
    curve_rows: list[dict[str, object]] = []
    for model in MODELS:
        values = np.asarray([loaded[model.key].mean(int(t - SMOOTH), int(t)) for t in grid])
        curves[model.key] = values
        for token, value in zip(grid, values):
            curve_rows.append({
                "tokens": int(token),
                "billions": f"{token / 1e9:.6f}",
                "model_key": model.key,
                "trailing_100m_lm_loss": f"{value:.12f}",
            })
    write_csv(TABLES / "curve_grid_25m_trailing_100m.csv", curve_rows)

    fig, axes = plt.subplots(2, 2, figsize=(15.2, 10.4), constrained_layout=True)
    ax_full, ax_zoom, ax_delta, ax_bar = axes.ravel()
    for model in MODELS:
        x = grid / 1e9
        ax_full.plot(x, curves[model.key], color=model.color, linestyle=model.linestyle,
                     linewidth=2.25, label=model.short)
        mask = grid >= 27_000_000_000
        ax_zoom.plot(x[mask], curves[model.key][mask], color=model.color,
                     linestyle=model.linestyle, linewidth=2.55, label=model.short)

    ax_full.set_title("A  0–30B：100M 词元尾随平均训练 LM loss", loc="left", fontproperties=font)
    ax_full.set_xlabel("累计有效预测词元（B）", fontproperties=font)
    ax_full.set_ylabel("训练 $L_{LM}$（nats / valid token）", fontproperties=font)
    ax_full.set_xlim(0, 30)
    ax_full.set_ylim(bottom=3.1, top=min(6.0, max(v[0] for v in curves.values()) + 0.2))
    ax_full.xaxis.set_major_locator(MultipleLocator(5))
    ax_full.grid(alpha=0.2)
    ax_full.legend(frameon=False, prop=font)

    ax_zoom.set_title("B  27–30B 局部放大（同一平滑口径）", loc="left", fontproperties=font)
    ax_zoom.set_xlabel("累计有效预测词元（B）", fontproperties=font)
    ax_zoom.set_ylabel("训练 $L_{LM}$", fontproperties=font)
    ax_zoom.set_xlim(27, 30)
    local_values = np.concatenate([v[grid >= 27_000_000_000] for v in curves.values()])
    padding = max(0.004, 0.08 * (float(local_values.max()) - float(local_values.min())))
    ax_zoom.set_ylim(float(local_values.min()) - padding, float(local_values.max()) + padding)
    ax_zoom.xaxis.set_major_locator(MultipleLocator(0.5))
    ax_zoom.grid(alpha=0.22)

    centers = np.arange(LOCAL_START + SMOOTH / 2, END, SMOOTH) / 1e9
    block_map: dict[str, np.ndarray] = {}
    for model in MODELS:
        rows = [r for r in block_rows if r["model_key"] == model.key]
        values = np.asarray([float(r["delta_vs_dense_millinats"]) for r in rows])
        block_map[model.key] = values
        ax_delta.plot(centers, values, color=model.color, linestyle=model.linestyle,
                      marker=model.marker, markersize=4.2, linewidth=2.1, label=model.short)
    ax_delta.axhline(0, color="#777777", linewidth=1.1)
    ax_delta.set_title("C  28–30B：非重叠 100M 区块相对 Dense", loc="left", fontproperties=font)
    ax_delta.set_xlabel("100M 区块中心（B）", fontproperties=font)
    ax_delta.set_ylabel("$\Delta L_{LM}$ vs Dense（millinats）", fontproperties=font)
    ax_delta.set_xlim(28, 30)
    ax_delta.xaxis.set_major_locator(MultipleLocator(0.5))
    ax_delta.grid(alpha=0.22)

    mean_28_30 = {model.key: loaded[model.key].mean(LOCAL_START, END) for model in MODELS}
    order = sorted(MODELS, key=lambda m: mean_28_30[m.key])
    bars = ax_bar.bar(
        np.arange(len(order)), [mean_28_30[m.key] for m in order],
        color=[m.color for m in order], alpha=0.88, width=0.66,
    )
    dense_value = mean_28_30["dense"]
    lower = min(mean_28_30.values()) - 0.004
    upper = max(mean_28_30.values()) + 0.003
    ax_bar.set_ylim(lower, upper)
    ax_bar.set_xticks(np.arange(len(order)), [m.short for m in order], fontproperties=font)
    ax_bar.set_ylabel("28–30B 精确词元加权 $L_{LM}$", fontproperties=font)
    ax_bar.set_title("D  28–30B 原始逐更新 loss 的精确均值", loc="left", fontproperties=font)
    ax_bar.grid(axis="y", alpha=0.2)
    for bar, model in zip(bars, order):
        value = mean_28_30[model.key]
        delta = 1000 * (value - dense_value)
        ax_bar.text(bar.get_x() + bar.get_width()/2, value + 0.00035,
                    f"{value:.6f}\n{delta:+.3f} mnat vs Dense",
                    ha="center", va="bottom", fontsize=9.5, fontproperties=font)

    fig.suptitle(
        "Dense、S7 λrec=0.1 与 SALL：截至精确 30B 的训练语言损失比较\n"
        "仅比较全局词元归一化 $L_{LM}$；不同 SAE 辅助目标的 total loss 不可横比",
        fontsize=16, fontproperties=font,
    )
    png = OUT / "training_lm_loss_dense_s7_sall_to_30b.png"
    pdf = OUT / "training_lm_loss_dense_s7_sall_to_30b.pdf"
    fig.savefig(png, dpi=220, bbox_inches="tight")
    fig.savefig(pdf, bbox_inches="tight")
    plt.close(fig)

    stability = {}
    for key in ("s7", "sall"):
        values = block_map[key]
        stability[key] = {
            "blocks_below_dense": int(np.sum(values < 0)),
            "block_count": int(len(values)),
            "minimum_delta_vs_dense_millinats": float(values.min()),
            "maximum_delta_vs_dense_millinats": float(values.max()),
            "mean_delta_vs_dense_millinats": float(values.mean()),
        }
    s7_vs_sall = np.asarray([
        float(r["delta_vs_sall_millinats"])
        for r in block_rows if r["model_key"] == "s7"
    ])
    stability["s7_vs_sall"] = {
        "blocks_s7_below_sall": int(np.sum(s7_vs_sall < 0)),
        "block_count": int(len(s7_vs_sall)),
        "minimum_s7_minus_sall_millinats": float(s7_vs_sall.min()),
        "maximum_s7_minus_sall_millinats": float(s7_vs_sall.max()),
        "mean_s7_minus_sall_millinats": float(s7_vs_sall.mean()),
    }
    manifest = {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "program": str(SCRIPT),
        "comparison_endpoint_tokens": END,
        "local_window_tokens": [LOCAL_START, END],
        "primary_metric": "globally token-weighted training lm_loss in natural-log units per valid prediction token",
        "excluded_metric": "total_loss is not comparable because the objectives and SAE coefficients differ",
        "display_smoothing": {"method": "exact trailing token-weighted arithmetic mean", "window_tokens": SMOOTH},
        "claim_boundary": "Single-seed training-loss evidence. It does not establish held-out quality, semantics, or a causal average effect. SALL is descriptive because its initial sampler order differs.",
        "models": {
            model.key: {
                "label": model.label,
                "objective": model.objective,
                "comparability": model.comparability,
                "observed_last_token_in_snapshot": int(loaded[model.key].tokens[-1]),
                "sources": loaded[model.key].source_metadata,
            } for model in MODELS
        },
        "local_window_summary": summary_rows,
        "local_100m_stability": stability,
        "outputs": {
            "figure_png": str(png), "figure_pdf": str(pdf),
            "window_summary_csv": str(TABLES / "local_window_summary.csv"),
            "block_csv": str(TABLES / "local_100m_blocks_28b_30b.csv"),
            "curve_csv": str(TABLES / "curve_grid_25m_trailing_100m.csv"),
        },
    }
    (TABLES / "comparison_manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps({
        "figure": str(png),
        "observed_endpoints": {key: int(value.tokens[-1]) for key, value in loaded.items()},
        "mean_28b_30b": mean_28_30,
        "stability": stability,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
