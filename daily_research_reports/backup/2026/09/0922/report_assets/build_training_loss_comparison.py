#!/usr/bin/env python3
"""Build the token-aligned LM-loss comparison requested on 2026-09-22.

The historical set is defined operationally as the three trajectories whose
metric ledgers reach at least 22B valid prediction tokens: Dense, the 0912
main-path SAE bottleneck (M2), and the original all-layer Attention sidecar
(SALL).  The fourth trajectory is the fresh-from-scratch S7 lambda_rec=0.1 run.

Only globally normalized language-model loss is compared across models.
Total objective values are intentionally not compared because the models have
different auxiliary terms and coefficients.
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
from matplotlib.lines import Line2D
from matplotlib.ticker import MultipleLocator


RESEARCH = Path("/data/250010109/Research_System")
EXPERIMENTS = Path("/data/250010109/MoE_Router/experiments")
SCRIPT = RESEARCH / "daily_research_reports/0922/report_assets/build_training_loss_comparison.py"
OUT = RESEARCH / "daily_research_reports/0922/figures/sae_training_loss_comparison"
TABLES = RESEARCH / "daily_research_reports/0922/tables/sae_training_loss_comparison"
FONT_PATH = RESEARCH / "daily_research_reports/0921/report_assets/fonts/NotoSansCJKsc-Regular.otf"

HISTORICAL_CAP = 22_000_000_000
SMOOTH_TOKENS = 100_000_000
LATEST_WINDOW = 2_000_000_000
GRID_STEP = 25_000_000
SALL_SOURCE_CHECKPOINT = 9_174_381_056


@dataclass(frozen=True)
class Source:
    path: Path
    ceiling: int | None = None


@dataclass(frozen=True)
class Model:
    key: str
    label: str
    short_label: str
    color: str
    linestyle: str
    linewidth: float
    objective: str
    architecture: str
    token_order_note: str
    sources: tuple[Source, ...]


MODELS = (
    Model(
        key="dense",
        label="Dense（原生主干）",
        short_label="Dense",
        color="#222222",
        linestyle="--",
        linewidth=2.3,
        objective="L_LM",
        architecture="8-layer Dense LM; no SAE",
        token_order_note="Reference 4-rank sample order preserved by the 8-rank comparison sampler.",
        sources=(
            Source(
                EXPERIMENTS
                / "20260913_dense_baseline_pretraining/runs/full_10b_8x5090_20260913T102944Z/metrics.jsonl",
                10_000_000_000,
            ),
            Source(
                EXPERIMENTS
                / "20260913_dense_baseline_pretraining/runs/full_50b_continue_from_10b_8x5090_r2_20260915T131706Z/metrics.jsonl"
            ),
        ),
    ),
    Model(
        key="m2",
        label="M2（末层 MLP 前串联 SAE，λ=1）",
        short_label="M2 main-path",
        color="#D55E00",
        linestyle="-.",
        linewidth=2.45,
        objective="L_LM + 1.0 L_rec",
        architecture="Final-block post-norm2 Top-K SAE reconstruction replaces the MLP input; detached reconstruction target pass.",
        token_order_note="Native 4-rank reference sample order.",
        sources=(
            Source(
                EXPERIMENTS
                / "20260912_dense_sae_pretraining/runs/full_50b_bottleneck8_202609121130/metrics.jsonl"
            ),
        ),
    ),
    Model(
        key="sall",
        label="SALL（8层 Attention 旁路，λ=1）",
        short_label="SALL 8-sidecar",
        color="#009E73",
        linestyle="-",
        linewidth=2.65,
        objective="L_LM + 1.0 L_rec + (1/32) L_AuxK",
        architecture="Eight raw-Attention-output SAE sidecars; reconstructions do not enter the LM forward path.",
        token_order_note="Same manifest and global tokens/update, but the initial 8-rank sampler does not preserve the 4-rank per-update sample order.",
        sources=(
            Source(
                EXPERIMENTS
                / "20260916_attention_output_sidecar_multisite_50b/runs/formal50b_all_layers_8xh100_spot/metrics.jsonl",
                SALL_SOURCE_CHECKPOINT,
            ),
            Source(
                EXPERIMENTS
                / "20260918_attention_output_sidecar_all8_4h100_resume/runs/formal50b_all8_unit_weight_4h100_mbs16_resume/metrics.jsonl"
            ),
        ),
    ),
    Model(
        key="s7_lambda0p1",
        label="S7（第8层 Attention 旁路，λ=0.1，fresh）",
        short_label="S7 fresh λ=0.1",
        color="#7B2CBF",
        linestyle="-",
        linewidth=3.15,
        objective="L_LM + 0.1 L_rec + (1/32) L_AuxK",
        architecture="One raw-Attention-output SAE sidecar at zero-based block 7; reconstruction does not enter the LM forward path.",
        token_order_note="Native 4-rank reference sample order; fresh seed-17 trajectory.",
        sources=(
            Source(
                EXPERIMENTS
                / "20260920_s7_lambda0p1_from_scratch_4h100/runs/S7_lambda0p1_from_scratch_4h100/metrics.jsonl"
            ),
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
        """Integral of piecewise-constant loss or coverage from token zero to x."""
        if x <= 0:
            return 0.0
        values = self.weighted_prefix if weighted else self.covered_prefix
        idx = int(np.searchsorted(self.tokens, x, side="right"))
        result = float(values[idx])
        if idx < len(self.tokens) and x > self.starts[idx]:
            span = min(float(x), float(self.tokens[idx])) - float(self.starts[idx])
            if span > 0:
                result += span * (float(self.losses[idx]) if weighted else 1.0)
        return result

    def mean(self, start: int, stop: int) -> float:
        if not (0 <= start < stop <= int(self.tokens[-1])):
            raise ValueError(f"window outside observed range: {start:,}--{stop:,}")
        numerator = self.integral(stop, True) - self.integral(start, True)
        denominator = self.integral(stop, False) - self.integral(start, False)
        requested = stop - start
        if abs(denominator - requested) > 1.0:
            raise RuntimeError(
                f"metric coverage gap: requested={requested:,}, covered={denominator:,.0f}"
            )
        return numerator / denominator

    def trailing(self, window: int) -> np.ndarray:
        result = np.full(self.losses.shape, np.nan, dtype=np.float64)
        valid = self.tokens >= window
        for i in np.flatnonzero(valid):
            result[i] = self.mean(int(self.tokens[i] - window), int(self.tokens[i]))
        return result


def parse_source(source: Source) -> tuple[dict[int, tuple[float, int]], dict[str, object]]:
    if not source.path.is_file():
        raise FileNotFoundError(source.path)
    payload = source.path.read_bytes()
    digest = hashlib.sha256(payload).hexdigest()
    points: dict[int, tuple[float, int]] = {}
    parsed = 0
    malformed = 0
    finite = 0
    raw_max = 0
    for raw_line in payload.splitlines():
        try:
            row = json.loads(raw_line)
            token = int(row["actual_lm_tokens"])
            loss = float(row["lm_loss"])
            count = int(row["lm_tokens"])
        except (json.JSONDecodeError, UnicodeDecodeError, KeyError, TypeError, ValueError):
            malformed += 1
            continue
        parsed += 1
        raw_max = max(raw_max, token)
        if token <= 0 or count <= 0 or not math.isfinite(loss):
            continue
        finite += 1
        if source.ceiling is not None and token > source.ceiling:
            continue
        points[token] = (loss, count)
    stat = source.path.stat()
    metadata = {
        "path": str(source.path),
        "sha256_of_read_snapshot": digest,
        "snapshot_bytes": len(payload),
        "filesystem_size_after_read": stat.st_size,
        "filesystem_mtime_utc_after_read": datetime.fromtimestamp(
            stat.st_mtime, timezone.utc
        ).isoformat(),
        "source_ceiling_tokens": source.ceiling,
        "parsed_rows": parsed,
        "finite_rows": finite,
        "used_rows": len(points),
        "malformed_rows": malformed,
        "raw_last_token": raw_max,
        "used_last_token": max(points) if points else None,
    }
    return points, metadata


def load_model(model: Model) -> Loaded:
    merged: dict[int, tuple[float, int]] = {}
    metadata: list[dict[str, object]] = []
    for source in model.sources:
        points, source_meta = parse_source(source)
        merged.update(points)  # later continuation is authoritative
        metadata.append(source_meta)
    if not merged:
        raise RuntimeError(f"no usable metrics for {model.key}")
    tokens = np.asarray(sorted(merged), dtype=np.int64)
    losses = np.asarray([merged[int(token)][0] for token in tokens], dtype=np.float64)
    counts = np.asarray([merged[int(token)][1] for token in tokens], dtype=np.int64)
    starts = tokens - counts
    if int(starts[0]) != 0:
        raise RuntimeError(f"{model.key}: first interval does not start at zero")
    gaps = starts[1:] - tokens[:-1]
    if np.any(gaps != 0):
        bad = np.flatnonzero(gaps != 0)[:5]
        raise RuntimeError(
            f"{model.key}: non-contiguous metric intervals at indices {bad.tolist()}, "
            f"gaps={gaps[bad].tolist()}"
        )
    weighted_prefix = np.concatenate(
        [np.asarray([0.0]), np.cumsum(losses * counts, dtype=np.float64)]
    )
    covered_prefix = np.concatenate(
        [np.asarray([0.0]), np.cumsum(counts, dtype=np.float64)]
    )
    return Loaded(tokens, losses, counts, starts, weighted_prefix, covered_prefix, metadata)


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def configure_plot() -> FontProperties:
    if not FONT_PATH.is_file():
        raise FileNotFoundError(FONT_PATH)
    font_manager.fontManager.addfont(str(FONT_PATH))
    font = FontProperties(fname=str(FONT_PATH))
    plt.rcParams.update(
        {
            "font.family": font.get_name(),
            "axes.unicode_minus": False,
            "font.size": 11.2,
            "axes.titlesize": 13.0,
            "axes.labelsize": 11.8,
            "axes.spines.top": False,
            "axes.spines.right": False,
        }
    )
    return font


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    TABLES.mkdir(parents=True, exist_ok=True)
    font = configure_plot()
    loaded = {model.key: load_model(model) for model in MODELS}
    fresh_end = int(loaded["s7_lambda0p1"].tokens[-1])
    common_end = min(HISTORICAL_CAP, *(int(data.tokens[-1]) for data in loaded.values()))
    if common_end != min(HISTORICAL_CAP, fresh_end):
        raise RuntimeError("an unexpected historical source limits the common endpoint")
    latest_start = common_end - LATEST_WINDOW
    if latest_start < 0:
        raise RuntimeError("fresh S7 has not reached the registered latest-window width")

    smooth = {key: data.trailing(SMOOTH_TOKENS) for key, data in loaded.items()}

    # Exact raw token-weighted summaries. Smoothing is display-only.
    summary_rows: list[dict[str, object]] = []
    dense_latest = loaded["dense"].mean(latest_start, common_end)
    dense_1b = loaded["dense"].mean(common_end - 1_000_000_000, common_end)
    dense_100m = loaded["dense"].mean(common_end - 100_000_000, common_end)
    for model in MODELS:
        data = loaded[model.key]
        latest = data.mean(latest_start, common_end)
        latest_1b = data.mean(common_end - 1_000_000_000, common_end)
        endpoint_100m = data.mean(common_end - 100_000_000, common_end)
        summary_rows.append(
            {
                "model_key": model.key,
                "model_label": model.label,
                "observed_last_token": int(data.tokens[-1]),
                "common_endpoint_tokens": common_end,
                "latest_2b_start_tokens": latest_start,
                "mean_lm_loss_latest_2b": f"{latest:.12f}",
                "delta_vs_dense_latest_2b_millinats": f"{1000 * (latest - dense_latest):.9f}",
                "relative_vs_dense_latest_2b_percent": f"{100 * (latest / dense_latest - 1):.9f}",
                "mean_lm_loss_latest_1b": f"{latest_1b:.12f}",
                "delta_vs_dense_latest_1b_millinats": f"{1000 * (latest_1b - dense_1b):.9f}",
                "mean_lm_loss_endpoint_100m": f"{endpoint_100m:.12f}",
                "delta_vs_dense_endpoint_100m_millinats": f"{1000 * (endpoint_100m - dense_100m):.9f}",
                "objective": model.objective,
                "architecture": model.architecture,
                "token_order_note": model.token_order_note,
            }
        )
    summary_rows.sort(key=lambda row: float(row["mean_lm_loss_latest_2b"]))
    summary_csv = TABLES / "latest_common_endpoint_summary.csv"
    write_csv(summary_csv, list(summary_rows[0]), summary_rows)

    # Non-overlapping 100M blocks in the final common 2B. These are a
    # descriptive stability check, not an inferential confidence interval.
    block_rows: list[dict[str, object]] = []
    for block_index in range(LATEST_WINDOW // SMOOTH_TOKENS):
        start = latest_start + block_index * SMOOTH_TOKENS
        stop = start + SMOOTH_TOKENS
        dense_value = loaded["dense"].mean(start, stop)
        for model in MODELS:
            value = loaded[model.key].mean(start, stop)
            block_rows.append(
                {
                    "block_index": block_index + 1,
                    "start_tokens": start,
                    "stop_tokens": stop,
                    "model_key": model.key,
                    "mean_lm_loss": f"{value:.12f}",
                    "delta_vs_dense_millinats": f"{1000 * (value - dense_value):.9f}",
                }
            )
    blocks_csv = TABLES / "latest_2b_nonoverlap_100m_blocks.csv"
    write_csv(blocks_csv, list(block_rows[0]), block_rows)

    # Exact 100M trailing means at fixed landmarks, including historical-only 22B.
    landmarks = [5_000_000_000, 10_000_000_000, 15_000_000_000, 17_000_000_000]
    if common_end not in landmarks:
        landmarks.append(common_end)
    landmarks.append(HISTORICAL_CAP)
    landmark_rows: list[dict[str, object]] = []
    for endpoint in sorted(set(landmarks)):
        dense_value = loaded["dense"].mean(endpoint - SMOOTH_TOKENS, endpoint)
        for model in MODELS:
            data = loaded[model.key]
            available = int(data.tokens[-1]) >= endpoint
            value = data.mean(endpoint - SMOOTH_TOKENS, endpoint) if available else None
            landmark_rows.append(
                {
                    "endpoint_tokens": endpoint,
                    "window_tokens": SMOOTH_TOKENS,
                    "model_key": model.key,
                    "available": available,
                    "mean_lm_loss": "" if value is None else f"{value:.12f}",
                    "delta_vs_dense_millinats": ""
                    if value is None
                    else f"{1000 * (value - dense_value):.9f}",
                }
            )
    landmarks_csv = TABLES / "landmark_trailing_100m_means.csv"
    write_csv(landmarks_csv, list(landmark_rows[0]), landmark_rows)

    # Historical-only exact 22B table.
    dense_22b = loaded["dense"].mean(HISTORICAL_CAP - LATEST_WINDOW, HISTORICAL_CAP)
    historical_22b_rows: list[dict[str, object]] = []
    for model in MODELS:
        data = loaded[model.key]
        if int(data.tokens[-1]) < HISTORICAL_CAP:
            continue
        value = data.mean(HISTORICAL_CAP - LATEST_WINDOW, HISTORICAL_CAP)
        historical_22b_rows.append(
            {
                "model_key": model.key,
                "model_label": model.label,
                "range_start_tokens": HISTORICAL_CAP - LATEST_WINDOW,
                "range_stop_tokens": HISTORICAL_CAP,
                "mean_lm_loss": f"{value:.12f}",
                "delta_vs_dense_millinats": f"{1000 * (value - dense_22b):.9f}",
            }
        )
    historical_22b_rows.sort(key=lambda row: float(row["mean_lm_loss"]))
    historical_22b_csv = TABLES / "historical_only_22b_summary.csv"
    write_csv(historical_22b_csv, list(historical_22b_rows[0]), historical_22b_rows)

    # Compact grid behind the delta panel.
    grid = np.arange(500_000_000, HISTORICAL_CAP + 1, GRID_STEP, dtype=np.int64)
    curve_rows: list[dict[str, object]] = []
    for endpoint in grid:
        dense_value = loaded["dense"].mean(int(endpoint - SMOOTH_TOKENS), int(endpoint))
        for model in MODELS:
            data = loaded[model.key]
            if int(data.tokens[-1]) < endpoint:
                continue
            value = data.mean(int(endpoint - SMOOTH_TOKENS), int(endpoint))
            curve_rows.append(
                {
                    "endpoint_tokens": int(endpoint),
                    "window_tokens": SMOOTH_TOKENS,
                    "model_key": model.key,
                    "trailing_mean_lm_loss": f"{value:.12f}",
                    "delta_vs_dense_millinats": f"{1000 * (value - dense_value):.9f}",
                }
            )
    curve_csv = TABLES / "curve_grid_25m_trailing_100m.csv"
    write_csv(curve_csv, list(curve_rows[0]), curve_rows)

    # Main four-panel figure.
    fig, axes = plt.subplots(2, 2, figsize=(18.5, 11.5), constrained_layout=False)
    fig.subplots_adjust(left=0.07, right=0.985, bottom=0.11, top=0.83, wspace=0.23, hspace=0.31)
    ax_full, ax_zoom, ax_delta, ax_rank = axes.ravel()

    def draw_smoothed(axis: plt.Axes, start: int, stop: int) -> None:
        visible: list[np.ndarray] = []
        for model in MODELS:
            data = loaded[model.key]
            values = smooth[model.key]
            mask = np.isfinite(values) & (data.tokens >= start) & (data.tokens <= stop)
            indices = np.flatnonzero(mask)
            if not len(indices):
                continue
            # Keep vector output and rendering compact without changing values.
            stride = max(1, len(indices) // 3500)
            indices = indices[::stride]
            last_eligible = np.flatnonzero(mask)[-1]
            if indices[-1] != last_eligible:
                indices = np.append(indices, last_eligible)
            axis.plot(
                data.tokens[indices] / 1e9,
                values[indices],
                color=model.color,
                linestyle=model.linestyle,
                linewidth=model.linewidth,
                alpha=0.96,
            )
            visible.append(values[mask])
        if visible:
            merged = np.concatenate(visible)
            low, high = np.quantile(merged, [0.002, 0.998])
            pad = max(0.006, 0.07 * float(high - low))
            axis.set_ylim(float(low - pad), float(high + pad))
        axis.set_xlim(start / 1e9, stop / 1e9)
        axis.set_xlabel("累计有效预测词元（B）", fontproperties=font)
        axis.set_ylabel("训练 LM loss（nat / 有效目标）", fontproperties=font)
        axis.grid(True, color="#D8D8D8", linewidth=0.7, alpha=0.72)

    draw_smoothed(ax_full, 500_000_000, HISTORICAL_CAP)
    ax_full.set_title("A｜完整可观测轨迹：历史模型到 22B，fresh S7 到当前点", fontproperties=font)
    if common_end < HISTORICAL_CAP:
        ax_full.axvspan(common_end / 1e9, 22.0, color="#7B2CBF", alpha=0.055)
        ax_full.axvline(common_end / 1e9, color="#7B2CBF", linestyle=":", linewidth=1.2)
        ax_full.text(
            common_end / 1e9 + 0.12,
            ax_full.get_ylim()[1] - 0.08 * np.ptp(ax_full.get_ylim()),
            "fresh S7 尚无数据\n（不外推）",
            color="#69408A",
            va="top",
            fontproperties=font,
        )
    ax_full.xaxis.set_major_locator(MultipleLocator(2.0))

    zoom_start = 10_000_000_000
    draw_smoothed(ax_zoom, zoom_start, common_end)
    ax_zoom.set_title(
        f"B｜共同区间放大：10B–{common_end / 1e9:.3f}B",
        fontproperties=font,
    )
    ax_zoom.axvline(common_end / 1e9, color="#777777", linestyle=":", linewidth=1.0)
    ax_zoom.xaxis.set_major_locator(MultipleLocator(1.0))

    delta_grid = np.arange(2_000_000_000, common_end + 1, GRID_STEP, dtype=np.int64)
    dense_delta_values = np.asarray(
        [loaded["dense"].mean(int(x - SMOOTH_TOKENS), int(x)) for x in delta_grid]
    )
    for model in MODELS:
        values = np.asarray(
            [loaded[model.key].mean(int(x - SMOOTH_TOKENS), int(x)) for x in delta_grid]
        )
        ax_delta.plot(
            delta_grid / 1e9,
            1000 * (values - dense_delta_values),
            color=model.color,
            linestyle=model.linestyle,
            linewidth=model.linewidth,
            alpha=0.96,
        )
    ax_delta.axhline(0, color="#555555", linewidth=1.0, alpha=0.8)
    ax_delta.set_xlim(2.0, common_end / 1e9)
    ax_delta.set_xlabel("累计有效预测词元（B）", fontproperties=font)
    ax_delta.set_ylabel("相对 Dense 的 LM loss（millinat）", fontproperties=font)
    ax_delta.set_title("C｜100M 词元滑窗差值；低于 0 表示优于 Dense", fontproperties=font)
    ax_delta.grid(True, color="#D8D8D8", linewidth=0.7, alpha=0.72)
    ax_delta.xaxis.set_major_locator(MultipleLocator(2.0))

    latest_values = {
        model.key: loaded[model.key].mean(latest_start, common_end) for model in MODELS
    }
    ranking = sorted(MODELS, key=lambda model: latest_values[model.key])
    positions = np.arange(len(ranking))
    bars = ax_rank.barh(
        positions,
        [latest_values[model.key] for model in ranking],
        color=[model.color for model in ranking],
        alpha=0.88,
        height=0.64,
    )
    ax_rank.set_yticks(positions, [model.short_label for model in ranking], fontproperties=font)
    ax_rank.invert_yaxis()
    ax_rank.set_xlabel("最后共同 2B 的原始 LM loss 均值", fontproperties=font)
    ax_rank.set_title("D｜当前共同预算的精确排序（非平滑均值）", fontproperties=font)
    ax_rank.grid(True, axis="x", color="#D8D8D8", linewidth=0.7, alpha=0.72)
    values = np.asarray([latest_values[model.key] for model in ranking])
    pad = max(0.0015, 0.22 * float(values.max() - values.min()))
    ax_rank.set_xlim(float(values.min() - pad), float(values.max() + 2.3 * pad))
    for bar, model in zip(bars, ranking):
        value = latest_values[model.key]
        delta = 1000 * (value - dense_latest)
        ax_rank.text(
            value + 0.00025,
            bar.get_y() + bar.get_height() / 2,
            f"{value:.6f}  ({delta:+.3f} mnat)",
            va="center",
            fontsize=10.2,
            fontproperties=font,
        )

    handles = [
        Line2D(
            [0],
            [0],
            color=model.color,
            linestyle=model.linestyle,
            linewidth=model.linewidth,
            label=model.label,
        )
        for model in MODELS
    ]
    fig.suptitle(
        "训练语言损失比较：约 22B 的历史模型 + fresh S7 λ=0.1",
        fontsize=18.5,
        fontweight="semibold",
        fontproperties=font,
    )
    fig.legend(
        handles=handles,
        loc="upper center",
        bbox_to_anchor=(0.5, 0.91),
        ncol=2,
        frameon=False,
        handlelength=3.4,
        prop=font,
    )
    fig.text(
        0.5,
        0.025,
        "曲线为精确 100M 词元尾随均值；D 为原始逐更新 loss 的词元加权均值。只比较 L_LM，不比较构成不同的 total loss。",
        ha="center",
        color="#555555",
        fontproperties=font,
    )
    png = OUT / "training_lm_loss_22b_models_plus_fresh_s7.png"
    pdf = OUT / "training_lm_loss_22b_models_plus_fresh_s7.pdf"
    fig.savefig(png, dpi=260, bbox_inches="tight", facecolor="white")
    fig.savefig(pdf, bbox_inches="tight", facecolor="white")
    plt.close(fig)

    # Descriptive latest-window stability summary.
    stability: dict[str, dict[str, float | int]] = {}
    for model in MODELS:
        deltas = np.asarray(
            [
                float(row["delta_vs_dense_millinats"])
                for row in block_rows
                if row["model_key"] == model.key
            ]
        )
        stability[model.key] = {
            "nonoverlap_100m_block_count": int(len(deltas)),
            "blocks_below_dense": int(np.sum(deltas < 0)),
            "minimum_delta_vs_dense_millinats": float(np.min(deltas)),
            "maximum_delta_vs_dense_millinats": float(np.max(deltas)),
            "mean_delta_vs_dense_millinats": float(np.mean(deltas)),
        }

    manifest = {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "program": str(SCRIPT),
        "comparison_set_definition": (
            "Dense, M2 main-path bottleneck, and SALL are the three historical telemetry "
            "trajectories that reach at least 22B valid prediction tokens; fresh S7 lambda_rec=0.1 is added."
        ),
        "primary_metric": "globally normalized training lm_loss in nats per valid prediction target",
        "excluded_metric": (
            "total_loss is not cross-model comparable because objectives and coefficients differ"
        ),
        "display_smoothing": {
            "method": "exact trailing token-weighted arithmetic mean",
            "window_tokens": SMOOTH_TOKENS,
        },
        "current_common_endpoint_tokens": common_end,
        "current_common_endpoint_billions": common_end / 1e9,
        "fresh_s7_snapshot_endpoint_tokens": fresh_end,
        "fresh_s7_has_22b_observation": fresh_end >= HISTORICAL_CAP,
        "latest_window_tokens": [latest_start, common_end],
        "historical_comparison_endpoint_tokens": HISTORICAL_CAP,
        "outputs": {
            "figure_png": str(png),
            "figure_pdf": str(pdf),
            "latest_summary_csv": str(summary_csv),
            "latest_blocks_csv": str(blocks_csv),
            "landmarks_csv": str(landmarks_csv),
            "historical_22b_csv": str(historical_22b_csv),
            "curve_grid_csv": str(curve_csv),
        },
        "models": {
            model.key: {
                "label": model.label,
                "objective": model.objective,
                "architecture": model.architecture,
                "token_order_note": model.token_order_note,
                "first_observed_token": int(loaded[model.key].tokens[0]),
                "last_observed_token": int(loaded[model.key].tokens[-1]),
                "usable_rows": int(len(loaded[model.key].tokens)),
                "sources": loaded[model.key].source_metadata,
            }
            for model in MODELS
        },
        "latest_common_endpoint_summary": summary_rows,
        "historical_only_22b_summary": historical_22b_rows,
        "latest_2b_stability": stability,
        "eligibility": {
            "shared": (
                "seed 17, sequence length 2048, data manifest SHA-256 "
                "8a91bdbb0eb537bd80612015b99f178ca1cbb54a2fa7cf8442ab1eae7f0a2f2d, "
                "262144 valid prediction tokens/update, LM optimizer LR/betas/weight decay/warmup"
            ),
            "strictest_pair": (
                "Fresh S7 versus Dense: same reference sample order, global batch, LM path at initialization, "
                "and token schedule; changed training objective is the S7 sidecar regularization."
            ),
            "sall_deviation": (
                "SALL's initial 8-rank sampler changes the per-update sample order relative to the 4-rank reference."
            ),
            "m2_deviation": (
                "M2 changes the inference/main path because the MLP consumes the SAE reconstruction."
            ),
        },
        "claim_boundary": (
            "Single-seed training-loss evidence only. It does not establish held-out quality, semantic quality, "
            "or a causal average treatment effect. Fresh S7 has no 22B observation in this snapshot when "
            "fresh_s7_has_22b_observation is false."
        ),
    }
    manifest_path = TABLES / "comparison_manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    for path in (
        png,
        pdf,
        summary_csv,
        blocks_csv,
        landmarks_csv,
        historical_22b_csv,
        curve_csv,
        manifest_path,
    ):
        print(path)
    print(f"COMMON_ENDPOINT={common_end}")


if __name__ == "__main__":
    main()
