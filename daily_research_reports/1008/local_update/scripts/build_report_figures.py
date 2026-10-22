"""Render four report-ready figures from selected frozen small tables.

Only figure formatting changes. No model, forward pass, bootstrap, training,
GPU or source table mutation. Interpretation belongs in report prose.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.colors import TwoSlopeNorm
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
EVI = ROOT / "evidence"
OUT = ROOT / "figures" / "report"
DOMAINS = ["computer_science", "mathematics", "physics", "biology"]
LABELS = ["计算机科学", "数学", "物理", "生物"]
TABLES = ["controlled_cells.csv", "controlled_rule_interaction.csv",
          "natural_cells_main16.csv", "sae_activation_pattern_distances.csv",
          "gradient_geometry_vs_loss.csv"]


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def matrix(frame, row, col, value, rows, cols):
    tab = frame.pivot(index=row, columns=col, values=value)
    assert tab.index.is_unique and tab.columns.is_unique
    result = tab.loc[rows, cols].to_numpy(dtype=float)
    assert np.all(np.isfinite(result))
    return result


def heat(ax, values, x, y, title, *, norm, cmap="RdBu_r", fmt=".3f", diagonal=False):
    shown = np.ma.array(values, mask=np.eye(len(values), dtype=bool)) if diagonal else values
    cm = plt.get_cmap(cmap).copy()
    cm.set_bad("#F0F2F4")
    im = ax.imshow(shown, norm=norm, cmap=cm, aspect="equal")
    ax.set_xticks(range(len(x)), x)
    ax.set_yticks(range(len(y)), y)
    ax.set_title(title, loc="left", pad=14, fontsize=12.5, fontweight="medium")
    ax.set_xticks(np.arange(-.5, len(x), 1), minor=True)
    ax.set_yticks(np.arange(-.5, len(y), 1), minor=True)
    ax.grid(which="minor", color="white", linewidth=1.6)
    ax.tick_params(which="minor", bottom=False, left=False)
    ax.tick_params(axis="both", length=0, pad=8)
    for i in range(values.shape[0]):
        for j in range(values.shape[1]):
            if diagonal and i == j:
                ax.text(j, i, "—", ha="center", va="center", color="#89919B", fontsize=12)
                continue
            rgb = cm(norm(values[i, j]))[:3]
            lum = .2126 * rgb[0] + .7152 * rgb[1] + .0722 * rgb[2]
            ax.text(j, i, format(values[i, j], fmt), ha="center", va="center",
                    color="white" if lum < .49 else "#182430", fontsize=12)
    for spine in ax.spines.values():
        spine.set_visible(False)
    return im


def bar(fig, im, ax, label, **kwargs):
    cb = fig.colorbar(im, ax=ax, fraction=.044, pad=.035, shrink=.86, **kwargs)
    cb.set_label(label, labelpad=8)
    cb.outline.set_linewidth(.6)
    cb.ax.tick_params(length=3, width=.6)
    return cb


def save(fig, name):
    for suffix in ["png", "svg"]:
        fig.savefig(OUT / f"{name}.{suffix}", dpi=300, bbox_inches="tight",
                    facecolor="white", metadata={"Creator": "1008 report figure renderer"})
    plt.close(fig)


def controlled():
    cells = pd.read_csv(EVI / "controlled_cells.csv")
    interaction = pd.read_csv(EVI / "controlled_rule_interaction.csv")
    assert len(cells) == 8 and len(interaction) == 2
    fig, axes = plt.subplots(1, 2, figsize=(10.4, 4.8), layout="constrained")
    for ax, eps, title in [(axes[0], 1e-4, "(a) 相对参数步长 ε＝10⁻⁴")]:
        sub = cells[np.isclose(cells.relative_parameter_step, eps)]
        v = matrix(sub, "signal_direction_inner_product", "answer_rule",
                   "mean_finite_loss_delta_nat", [.1, .8], ["same", "flip"]) * 1000
        assert np.all(v < 0)
        im = heat(ax, v, ["保持类别对应", "对调类别对应"], ["0.1", "0.8"], title,
                  norm=TwoSlopeNorm(vmin=-7, vcenter=0, vmax=7), fmt=".4f")
        ax.set_xlabel("B的正确类别对应")
        ax.set_ylabel("信号方向内积 ρ")
    bar(fig, im, axes[0], "平均 I（10⁻³ nat／目标）")
    sub = interaction.set_index("relative_parameter_step").loc[[1e-4, 5e-5]]
    y = sub.interaction_M_nat.to_numpy() * 1e4
    errors = np.vstack([y - sub.interval95_low_nat.to_numpy() * 1e4,
                        sub.interval95_high_nat.to_numpy() * 1e4 - y])
    axes[1].errorbar([0, 1], y, yerr=errors, fmt="o", markersize=6,
                     color="#245A81", ecolor="#245A81", capsize=5, linewidth=1.4,
                     label="均值及95%区间")
    axes[1].axhline(0, color="#777F87", linewidth=.8)
    axes[1].set_xticks([0, 1], ["10⁻⁴", "5×10⁻⁵"])
    axes[1].set_xlim(-.5, 1.5)
    axes[1].set_ylim(-.05, 1.95)
    axes[1].set_title("(b) 交互量 M", loc="left", pad=14, fontsize=12.5)
    axes[1].set_xlabel("相对参数步长 ε")
    axes[1].set_ylabel("M（10⁻⁴ nat／目标）")
    axes[1].legend(frameon=False, loc="upper right", fontsize=9)
    axes[1].grid(axis="y", alpha=.15, linewidth=.6)
    save(fig, "conclusion01_controlled")


def natural():
    frame = pd.read_csv(EVI / "natural_cells_main16.csv")
    assert len(frame) == 16 and set(frame.step) == {"full_step"}
    mean = matrix(frame, "source", "target", "mean_delta_loss", DOMAINS, DOMAINS) * 1000
    adverse = matrix(frame, "source", "target", "event_adverse_fraction_gt_1e_5", DOMAINS, DOMAINS) * 100
    assert np.all(mean < 0) and np.all((adverse > 43) & (adverse < 54))
    fig, axes = plt.subplots(1, 2, figsize=(11.5, 5.1), layout="constrained")
    im = heat(axes[0], mean, LABELS, LABELS, "(a) 平均有限损失变化",
              norm=TwoSlopeNorm(vmin=-2.05, vcenter=0, vmax=2.05))
    bar(fig, im, axes[0], "I（10⁻³ nat／目标）")
    im = heat(axes[1], adverse, LABELS, LABELS, "(b) 增损位置比例（I＞10⁻⁵ nat）",
              norm=plt.Normalize(0, 60), cmap="YlOrRd", fmt=".2f")
    bar(fig, im, axes[1], "比例（%）")
    for ax in axes:
        ax.set_xlabel("接收域 B")
        ax.set_ylabel("来源域 A")
    save(fig, "conclusion02_natural")


def sae():
    frame = pd.read_csv(EVI / "sae_activation_pattern_distances.csv")
    frame = frame[frame["mode"] == "frequency"]
    assert len(frame) == 16
    v = 1 - matrix(frame, "fit_domain", "readout_domain", "cosine", DOMAINS, DOMAINS)
    fig, ax = plt.subplots(figsize=(6.2, 5.1), layout="constrained")
    im = heat(ax, v, LABELS, LABELS, "SAE领域激活差异",
              norm=plt.Normalize(0, .4), cmap="Blues", fmt=".3f")
    ax.set_xlabel("readout领域")
    ax.set_ylabel("fit领域")
    bar(fig, im, ax, "差异（1−余弦相似度）")
    save(fig, "conclusion02_sae_domains")


def geometry():
    frame = pd.read_csv(EVI / "gradient_geometry_vs_loss.csv")
    assert len(frame) == 16
    fig, axes = plt.subplots(1, 2, figsize=(11.5, 5.1), layout="constrained")
    for ax, field, title, unit in zip(axes,
          ["gradient_cosine", "finite_response_pearson"],
          ["(a) 来源平均梯度的方向余弦", "(b) 有限损失变化的相关"],
          ["Frobenius余弦", "Pearson相关系数"]):
        v = matrix(frame, "source_i", "source_j", field, DOMAINS, DOMAINS)
        assert np.allclose(v, v.T, atol=1e-14)
        im = heat(ax, v, LABELS, LABELS, title,
                  norm=TwoSlopeNorm(vmin=-1, vcenter=0, vmax=1), diagonal=True)
        bar(fig, im, ax, unit)
        ax.set_xlabel("来源域")
        ax.set_ylabel("来源域")
    save(fig, "conclusion03_geometry_response")


def main(font):
    OUT.mkdir(parents=True, exist_ok=True)
    font_manager.fontManager.addfont(str(font))
    font_name = font_manager.FontProperties(fname=str(font)).get_name()
    plt.rcParams.update({"font.family": [font_name, "DejaVu Sans"],
                         "font.size": 10.5, "axes.unicode_minus": False,
                         "axes.linewidth": .8, "axes.spines.top": False,
                         "axes.spines.right": False, "svg.fonttype": "path",
                         "savefig.facecolor": "white"})
    inputs = {str(EVI / name): sha(EVI / name) for name in TABLES}
    controlled()
    natural()
    sae()
    geometry()
    for path, expected in inputs.items():
        assert sha(path) == expected, path
    meta = {"created_at_utc": datetime.now(timezone.utc).isoformat(),
            "kind": "report-ready rendering of existing selected tables; no new measurement",
            "input_sha256": inputs, "script_sha256": sha(__file__),
            "font": {"path": str(font), "sha256": sha(font), "in_repository": False,
                     "source": "https://raw.githubusercontent.com/notofonts/noto-cjk/main/Sans/OTF/SimplifiedChinese/NotoSansCJKsc-Regular.otf"},
            "policy": "No explanatory findings, causal claims or long footers inside figures; panel titles, axes, units, legends and numbers only.",
            "row_scope": {"controlled": "12 fixed direction families; existing paired bootstrap intervals unchanged",
                          "natural": "16 source/receiver cells; 1024 receiver records, 16 positions each; original threshold 1e-5 retained",
                          "sae": "existing domain activation result; frequency mode, all 30000 atoms; fit/readout domain axes; not source/receiver loss axes",
                          "gradient": "four source averages; two SOURCE axes; same 16384 receiver positions; self-pairs masked for display"},
            "new_statistics": False,
            "sae_source": {
                "path": "/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A17/17_12_domain_update_geometry/20260930/evidence/activation_pattern_distances.csv",
                "sha256": inputs[str(EVI / "sae_activation_pattern_distances.csv")],
                "transformation": "frequency mode only; plotted difference = 1 - existing cosine; no new estimation",
                "boundary": "fit/readout activation panel differs from source/receiver finite-update panel; no pairwise prediction claim"
            },
            "outputs": [{"path": str(p.relative_to(ROOT)), "sha256": sha(p), "bytes": p.stat().st_size}
                        for p in sorted(OUT.glob("conclusion*"))]}
    (EVI / "report_figures_provenance.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"figures": len(list(OUT.glob("*.png"))), "outputs": len(meta["outputs"]),
                      "sources_unchanged": True}, ensure_ascii=False))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--font", type=Path, required=True)
    main(parser.parse_args().font)
