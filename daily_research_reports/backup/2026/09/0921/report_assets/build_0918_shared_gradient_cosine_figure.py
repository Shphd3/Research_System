"""Replot frozen shared-parameter gradient direction measurements for the meeting.

This is a presentation-only redraw.  It performs no model loading, fitting,
training, or new statistical test.
"""

import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
import numpy as np


HERE = Path(__file__).resolve().parents[1]
REPORTS = HERE.parent
CHECKPOINT_CSV = REPORTS / "0918" / "tables" / "shared_parameter_gradient_checkpoint_summary.csv"
OUT = HERE / "figures" / "gradient_0918"
FONT_PATH = HERE / "report_assets" / "fonts" / "NotoSansCJKsc-Regular.otf"
MODELS = ("S7", "S37", "SALL")
TOKENS_B = (0.0, 0.5, 1.0, 3.0, 5.0, 10.0)
COLORS = {"S7": "#0072B2", "S37": "#CC79A7", "SALL": "#009E73"}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def float_fields(row, fields):
    return {field: float(row[field]) for field in fields}


def fmt_token(value: float) -> str:
    return str(int(value)) if value.is_integer() else str(value)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    assert FONT_PATH.is_file(), f"missing Chinese display font: {FONT_PATH}"

    with CHECKPOINT_CSV.open(newline="") as handle:
        checkpoint_rows = list(csv.DictReader(handle))
    trajectory = []
    required_checkpoint = (
        "tokens_b",
        "rho_mean",
        "cosine_mean",
        "cosine_std",
        "angle_degrees_mean",
        "isotropic_abs_cosine_q975_normal_mean",
    )
    for row in checkpoint_rows:
        if row["parameter_group"] != "all_shared_parameters" or row["model"] not in MODELS:
            continue
        values = float_fields(row, required_checkpoint)
        trajectory.append({"model": row["model"], "batches": int(row["batches"]), **values})

    assert len(trajectory) == len(MODELS) * len(TOKENS_B), "expected 18 shared-parameter checkpoints"
    for model in MODELS:
        model_tokens = tuple(sorted(row["tokens_b"] for row in trajectory if row["model"] == model))
        assert model_tokens == TOKENS_B, (model, model_tokens)
        assert {row["batches"] for row in trajectory if row["model"] == model} == {4}

    random_bounds = {row["isotropic_abs_cosine_q975_normal_mean"] for row in trajectory}
    assert len(random_bounds) == 1, "random calibration must be identical across plotted rows"
    random_bound = random_bounds.pop()

    font_manager.fontManager.addfont(str(FONT_PATH))
    cjk_font_name = font_manager.FontProperties(fname=str(FONT_PATH)).get_name()
    plt.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": [cjk_font_name, "DejaVu Sans"],
            "axes.unicode_minus": False,
            "svg.fonttype": "none",
        }
    )
    fig, ax = plt.subplots(figsize=(13.5, 6.35), layout="constrained", facecolor="white")

    ax.axhspan(-random_bound, random_bound, color="#a6a6a6", alpha=0.42, zorder=0)
    ax.axhline(0, color="#4b5563", lw=0.9, zorder=1)
    for model in MODELS:
        rows = sorted((row for row in trajectory if row["model"] == model), key=lambda row: row["tokens_b"])
        xs = np.array([row["tokens_b"] for row in rows])
        ys = np.array([row["cosine_mean"] for row in rows])
        yerr = np.array([row["cosine_std"] for row in rows])
        ax.errorbar(
            xs,
            ys,
            yerr=yerr,
            fmt="o-",
            color=COLORS[model],
            ecolor=COLORS[model],
            elinewidth=1.05,
            capsize=3.2,
            markersize=6.5,
            lw=2.2,
            alpha=0.92,
            label=model,
            zorder=3,
        )

    ax.set_xlim(-0.2, 10.9)
    ax.set_ylim(-0.075, 0.065)
    ax.set_xticks(TOKENS_B, [fmt_token(value) for value in TOKENS_B])
    ax.set_xlabel("累计训练 token（B）", fontsize=11)
    ax.set_ylabel(r"$\cos(g_{\rm LM}, g_{\rm rec})$", fontsize=12)
    ax.grid(axis="y", color="#cbd5e1", alpha=0.55, lw=0.75)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(title="SAE 放置", frameon=False, loc="lower right", ncol=3, fontsize=10, title_fontsize=10)
    ax.text(
        0.02,
        0.04,
        f"灰带：各向同性随机方向的中心 95% 区间\n[$-{random_bound:.3e}$, $+{random_bound:.3e}$]",
        transform=ax.transAxes,
        fontsize=9.3,
        color="#374151",
        va="bottom",
        bbox={"boxstyle": "round,pad=0.35", "facecolor": "white", "edgecolor": "#9ca3af", "alpha": 0.94},
    )
    ax.set_title("共享主干参数上的梯度方向轨迹", loc="left", fontsize=13, weight="bold", pad=10)

    fig.suptitle("SAE 梯度与 LM 梯度低对齐，但并非随机方向", x=0.01, ha="left", fontsize=17, weight="bold")
    outputs = []
    for suffix in ("png", "svg"):
        path = OUT / f"01_shared_gradient_cosine_trajectory.{suffix}"
        fig.savefig(path, dpi=220, bbox_inches="tight", facecolor="white")
        outputs.append(path)
    plt.close(fig)

    manifest = {
        "status": "PASS",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "scope": "Presentation-only redraw of frozen 0918 gradient CSVs; no model inference, fitting, training, or new statistical test.",
        "script": str(Path(__file__).resolve()),
        "script_sha256": sha256(Path(__file__).resolve()),
        "inputs": {
            str(CHECKPOINT_CSV): {"sha256": sha256(CHECKPOINT_CSV)},
        },
        "rendering_font": {
            "path": str(FONT_PATH),
            "sha256": sha256(FONT_PATH),
            "source": "https://github.com/notofonts/noto-cjk/blob/main/Sans/OTF/SimplifiedChinese/NotoSansCJKsc-Regular.otf",
        },
        "outputs": [{"path": str(path), "sha256": sha256(path)} for path in outputs],
        "filter": {"parameter_group": "all_shared_parameters", "models": list(MODELS), "tokens_b": list(TOKENS_B)},
        "random_band": {
            "lower": -random_bound,
            "upper": random_bound,
            "source_column": "isotropic_abs_cosine_q975_normal_mean",
            "meaning": "Central 95% interval of signed cosine under the isotropic random-direction calibration.",
        },
        "trajectory": trajectory,
        "limitations": [
            "Each trajectory point aggregates four fixed batches; its standard deviation is not a confidence interval or a seed-to-seed estimate.",
            "The measurement concerns gradients on all shared parameters. It does not by itself establish the direction of the net optimizer update, semantic behavior, or a causal benefit of SAE regularization.",
            "The grey band is a supplied isotropic random-direction calibration; it is not an across-run performance baseline.",
        ],
    }
    (OUT / "figure_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"outputs": [str(path) for path in outputs], "random_band": [-random_bound, random_bound]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
