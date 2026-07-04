#!/usr/bin/env python3
"""Generate paper-facing LaTeX tables from completed V2 metrics."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from src.registry import EXPERIMENTS, ROOT


def esc(value: object) -> str:
    text = str(value)
    for old, new in [
        ("\\", "\\textbackslash{}"),
        ("_", "\\_"),
        ("%", "\\%"),
        ("&", "\\&"),
        ("#", "\\#"),
    ]:
        text = text.replace(old, new)
    return text


def fmt(value: object, digits: int = 3) -> str:
    try:
        val = float(value)
    except (TypeError, ValueError):
        return esc(value)
    if np.isnan(val):
        return "--"
    return f"{val:.{digits}f}"


def table_env(label: str, caption: str, cols: str, header: list[str], rows: list[list[object]]) -> str:
    lines = [
        "\\begin{table}[t]",
        "\\centering",
        f"\\caption{{{caption}}}",
        f"\\label{{{label}}}",
        f"\\begin{{tabular}}{{{cols}}}",
        "\\toprule",
        " & ".join(header) + " \\\\",
        "\\midrule",
    ]
    for row in rows:
        lines.append(" & ".join(str(item) for item in row) + " \\\\")
    lines.extend(["\\bottomrule", "\\end{tabular}", "\\end{table}", ""])
    return "\n".join(lines)


def read(exp_id: str) -> pd.DataFrame:
    path = ROOT / EXPERIMENTS[exp_id].metrics_csv
    if not path.exists():
        raise SystemExit(f"Missing metrics file: {path}")
    df = pd.read_csv(path)
    if "run_mode" in df.columns and not (df["run_mode"] == "full").all():
        raise SystemExit(f"{path} contains non-full rows. Re-run without --quick.")
    return df


def write(exp_id: str, text: str) -> None:
    path = ROOT / EXPERIMENTS[exp_id].table_tex
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def e1() -> None:
    df = read("E1")
    sub = df[(df["d"] == 64) & (df["E"] == 8) & (df["n_cal"] == df["n_cal"].max())]
    agg = sub.groupby(["dataset", "method_label"], as_index=False).agg(
        cal_loadcv=("cal_loadcv", "mean"),
        holdout_loadcv=("holdout_loadcv", "mean"),
        max_abs_error=("holdout_max_abs_error", "mean"),
        margin=("holdout_margin_p05", "mean"),
    )
    rows = [
        [esc(r.dataset), esc(r.method_label), fmt(r.cal_loadcv), fmt(r.holdout_loadcv), fmt(r.max_abs_error), fmt(r.margin)]
        for r in agg.itertuples()
    ]
    write(
        "E1",
        table_env(
            "tab:e1_static_dispatch",
            "Static uniform dispatch on the main full-run setting ($d=64$, $E=8$, largest calibration size).",
            "llrrrr",
            ["Data", "Method", "Cal LoadCV $\\downarrow$", "Holdout LoadCV $\\downarrow$", "Max error $\\downarrow$", "Margin p05 $\\uparrow$"],
            rows,
        ),
    )


def e2() -> None:
    df = read("E2")
    sub = df[(df["d"] == df["d"].max()) & (df["E"] == 8)]
    agg = sub.groupby(["dataset", "method_label"], as_index=False).agg(
        cov=("cov_condition", "mean"),
        rank=("effective_rank", "mean"),
        load=("holdout_loadcv", "mean"),
        err=("holdout_max_abs_error", "mean"),
    )
    rows = [
        [esc(r.dataset), fmt(r.cov, 2), fmt(r.rank, 1), esc(r.method_label), fmt(r.load), fmt(r.err)]
        for r in agg.itertuples()
    ]
    write(
        "E2",
        table_env(
            "tab:e2_non_spherical",
            "Spectrally flat but non-spherical features. Covariance flatness alone does not force prototype-router balance.",
            "lrrlrr",
            ["Data", "Cond. $\\downarrow$", "Eff. rank $\\uparrow$", "Method", "LoadCV $\\downarrow$", "Max error $\\downarrow$"],
            rows,
        ),
    )


def e3() -> None:
    df = read("E3")
    agg = df.groupby(["expert_init", "method_label"], as_index=False).agg(
        spread=("prototype_spread", "mean"),
        align=("cell_proto_alignment", "mean"),
        load=("holdout_loadcv", "mean"),
        margin=("holdout_margin_p05", "mean"),
    )
    keep = agg[agg["method_label"].isin(["Expert-SVD top-1", "MPI one-step top-1", "SPR-Expert", "SPR-Expert-MPI", "SPR-Local"])]
    rows = [
        [esc(r.expert_init), esc(r.method_label), fmt(r.spread), fmt(r.align), fmt(r.load), fmt(r.margin)]
        for r in keep.itertuples()
    ]
    write(
        "E3",
        table_env(
            "tab:e3_expert_guided",
            "Expert-weight-guided routing. Expert prototypes improve alignment, while quantile thresholds control mass.",
            "llrrrr",
            ["Expert init", "Router", "Proto spread $\\uparrow$", "Alignment $\\uparrow$", "LoadCV $\\downarrow$", "Margin p05 $\\uparrow$"],
            rows,
        ),
    )


def e4() -> None:
    df = read("E4")
    sub = df[df["regime"] == "medium"]
    agg = sub.groupby("method_label", as_index=False).agg(
        load=("holdout_loadcv", "mean"),
        nmi=("route_feature_nmi", "mean"),
        purity=("feature_purity", "mean"),
        var=("within_cell_var", "mean"),
        margin=("holdout_margin_p05", "mean"),
    )
    rows = [[esc(r.method_label), fmt(r.load), fmt(r.nmi), fmt(r.purity), fmt(r.var), fmt(r.margin)] for r in agg.itertuples()]
    write(
        "E4",
        table_env(
            "tab:e4_feature_partition",
            "Feature partition quality on evaluation-only latent classes.",
            "lrrrrr",
            ["Method", "LoadCV $\\downarrow$", "NMI $\\uparrow$", "Purity $\\uparrow$", "Within-var. $\\downarrow$", "Margin p05 $\\uparrow$"],
            rows,
        ),
    )


def e5() -> None:
    df = read("E5")
    final = df[df["epoch"] == df["epoch"].max()]
    agg = final.groupby("method_label", as_index=False).agg(
        val=("val_loss", "mean"),
        load=("holdout_loadcv", "mean"),
        nmi=("route_feature_nmi", "mean"),
        flip=("route_flip_rate", "mean"),
        margin=("holdout_margin_p05", "mean"),
        spec=("specialization_score", "mean"),
    )
    rows = [[esc(r.method_label), fmt(r.val), fmt(r.load), fmt(r.nmi), fmt(r.flip), fmt(r.margin), fmt(r.spec)] for r in agg.itertuples()]
    write(
        "E5",
        table_env(
            "tab:e5_training_dynamics",
            "Controlled hard-routing expert training at the final epoch.",
            "lrrrrrr",
            ["Router", "Val MSE $\\downarrow$", "LoadCV $\\downarrow$", "NMI $\\uparrow$", "Flip $\\downarrow$", "Margin p05 $\\uparrow$", "Spec. $\\uparrow$"],
            rows,
        ),
    )


def e6() -> None:
    df = read("E6")
    agg = df.groupby(["ablation", "setting"], as_index=False).agg(
        load=("holdout_loadcv", "mean"),
        nmi=("route_feature_nmi", "mean"),
        margin=("holdout_margin_p05", "mean"),
        err=("holdout_max_abs_error", "mean"),
    )
    rows = [[esc(r.ablation), esc(r.setting), fmt(r.load), fmt(r.nmi), fmt(r.margin), fmt(r.err)] for r in agg.itertuples()]
    write(
        "E6",
        table_env(
            "tab:e6_ablations",
            "Ablations and boundary checks.",
            "llrrrr",
            ["Ablation", "Setting", "LoadCV $\\downarrow$", "NMI $\\uparrow$", "Margin p05 $\\uparrow$", "Max error $\\downarrow$"],
            rows,
        ),
    )


def main() -> None:
    for fn in (e1, e2, e3, e4, e5, e6):
        fn()
    print("Wrote paper tables:")
    for spec in EXPERIMENTS.values():
        print(f"- {spec.table_tex}")


if __name__ == "__main__":
    main()
