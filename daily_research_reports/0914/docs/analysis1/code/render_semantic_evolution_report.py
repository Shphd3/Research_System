#!/usr/bin/env python3
"""Render the curated four-part analysis1 report from immutable run outputs."""

from __future__ import annotations

import csv
import hashlib
import json
import shutil
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from dense_sae.analysis.semantic_evolution import (
    build_triplets,
    cache_to_csr,
    dense_margin,
    grouped_ci,
    load_panel,
    sparse_margin,
)


EXEC_ROOT = Path("/data/250010109/MoE_Router/experiments/20260912_dense_sae_pretraining")
RUN = EXEC_ROOT / "analysis_runs/analysis1_20260913/full"
CONFIG = EXEC_ROOT / "configs/semantic_evolution_analysis1.json"
HERE = Path(__file__).resolve().parents[1]
FIGURES = HERE / "figures"
TABLES = HERE / "tables"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(16 * 1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def read_csv(name: str):
    with (RUN / "tables" / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows):
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def audit_and_derive():
    cfg = json.loads(CONFIG.read_text())
    receipt = json.loads((RUN / "analysis_receipt.json").read_text())
    terminal = json.loads((RUN / "terminal_receipt.json").read_text())
    assert receipt["status"] == "PASS" and receipt["samples"] == 864
    assert terminal["exit_code"] == 0 and terminal["optimizer_updates"] == 0
    rows = load_panel(Path(cfg["panel_path"]), cfg["panel_sha256"])
    sample_ids = np.asarray([row["sample_id"] for row in rows])
    caches = {}
    for slug in cfg["checkpoint_slugs"]:
        cache_path = RUN / "caches" / f"{slug}.npz"
        cache = np.load(cache_path)
        assert np.array_equal(cache["sample_ids"], sample_ids)
        assert cache["h"].shape == (864, 1024) and cache["h_hat"].shape == (864, 1024)
        assert cache["z_indices"].shape == (864, 32)
        assert all(np.isfinite(cache[key]).all() for key in ("h", "h_hat", "z_values", "decoder_norms"))
        meta = json.loads(cache_path.with_suffix(".json").read_text())
        assert meta["cache_sha256"] == sha256(cache_path) and meta["optimizer_updates"] == 0
        caches[slug] = cache
    qwen = np.load(RUN / "caches/qwen3_0p6b.npz")
    assert np.array_equal(qwen["sample_ids"], sample_ids)
    assert qwen["h"].shape == (864, 1024) and np.isfinite(qwen["h"]).all()

    triples = build_triplets(rows)
    endpoint_rows = []
    early, late = caches["0p5b"], caches["10b"]
    for rep, fn in (("h", dense_margin), ("h_hat", dense_margin), ("c", sparse_margin)):
        x0 = cache_to_csr(early) if rep == "c" else early[rep]
        x1 = cache_to_csr(late) if rep == "c" else late[rep]
        for relation, relation_triples in triples.items():
            values = fn(x1, relation_triples) - fn(x0, relation_triples)
            mean, low, high, fact_blocks = grouped_ci(values, relation_triples)
            endpoint_rows.append({
                "representation": rep, "relation": relation,
                "delta_10b_minus_0p5b": mean, "paired_ci95_low": low,
                "paired_ci95_high": high, "fact_blocks": fact_blocks,
                "analysis_status": "POST_HOC_CONFORMANCE_AUDIT",
            })
    write_csv(TABLES / "semantic_endpoint_paired_deltas.csv", endpoint_rows)

    manifest = {
        "run_job": "pt-lok5c11y",
        "run_status": "SUCCEEDED",
        "analysis_receipt_sha256": sha256(RUN / "analysis_receipt.json"),
        "terminal_receipt_sha256": sha256(RUN / "terminal_receipt.json"),
        "config_sha256": sha256(CONFIG),
        "panel_sha256": cfg["panel_sha256"],
        "verified_checkpoint_caches": cfg["checkpoint_slugs"],
        "verified_samples_per_cache": 864,
        "optimizer_updates": 0,
        "paired_delta_table_status": "post-hoc audit of a computation named in the plan but absent from the run output",
        "eligibility": "BOUNDED_EXPLORATORY_ONLY",
    }
    (TABLES / "semantic_result_source_manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return cfg, read_csv("relation_margins.csv"), read_csv("readout_accuracy.csv"), read_csv("cross_reader_quality.csv"), endpoint_rows


def hypothesis_figure(labels):
    x = np.arange(len(labels))
    fig, axes = plt.subplots(1, 3, figsize=(14, 4.2))
    for name, y in {
        "coarse domain": [.25, .38, .55, .69, .82],
        "subdomain": [.18, .29, .43, .58, .72],
        "same fact / paraphrase": [.08, .17, .30, .47, .64],
    }.items():
        axes[0].plot(x, y, marker="o", label=name)
    axes[0].set_title("Stronger visual expectation")
    axes[0].set_ylabel("Qualitative relation strength")
    axes[0].legend(frameon=False, fontsize=8)
    for name, y in {"h": [.48, .57, .67, .76, .84], "h_hat": [.43, .52, .62, .71, .79], "sparse c": [.38, .47, .57, .66, .74]}.items():
        axes[1].plot(x, y, marker="o", label=name)
    axes[1].set_title("Expected readable signal")
    axes[1].set_ylabel("Qualitative held-out readability")
    axes[1].legend(frameon=False, fontsize=8)
    expected = np.asarray([[.20, .45], [.42, .16]])
    im = axes[2].imshow(expected, cmap="viridis_r", vmin=0, vmax=.5)
    axes[2].set_xticks([0, 1], ["h@0.5B", "h@10B"])
    axes[2].set_yticks([0, 1], ["SAE@0.5B", "SAE@10B"])
    axes[2].set_title("Expected reader specificity")
    for i in range(2):
        for j in range(2): axes[2].text(j, i, f"{expected[i,j]:.2f}", ha="center", va="center")
    fig.colorbar(im, ax=axes[2], fraction=.046, label="Illustrative error")
    for ax in axes[:2]:
        ax.set_xticks(x, labels); ax.set_xlabel("Training tokens"); ax.grid(alpha=.2)
    fig.suptitle("WORKING HYPOTHESIS — deterministic illustration, not measured data", fontweight="bold")
    fig.tight_layout()
    fig.savefig(FIGURES / "semantic_hypothesis.png", dpi=180)
    plt.close(fig)


def observed_figure(labels, relation_rows, readout_rows, cross_rows):
    x = np.arange(len(labels)); slugs = ["0p5b", "1b", "3b", "5b", "10b"]
    fig, axes = plt.subplots(2, 2, figsize=(14, 9))
    ax = axes[0, 0]
    for relation in ("coarse", "fine", "fact"):
        rr = [r for r in relation_rows if r["representation"] == "h" and r["relation"] == relation and r["checkpoint_slug"] in slugs]
        y = np.asarray([float(r["mean_margin"]) for r in rr]); lo = np.asarray([float(r["ci95_low"]) for r in rr]); hi = np.asarray([float(r["ci95_high"]) for r in rr])
        ax.plot(x, y, marker="o", label=relation); ax.fill_between(x, lo, hi, alpha=.12)
    ax.axhline(0, color="black", linewidth=.8); ax.set_title("Measured relation margins in pre-SAE h")
    ax.set_ylabel("cos(a,p) - cos(a,n)"); ax.legend(frameon=False)

    ax = axes[0, 1]
    for rep in ("h", "h_hat_adapted", "h_to_h_hat_frozen", "c"):
        rr = [r for r in readout_rows if r["target"] == "leaf" and r["representation"] == rep and r["checkpoint_slug"] in slugs]
        ax.plot(x, [float(r["test_balanced_accuracy"]) for r in rr], marker="o", label=rep)
    lexical = next(float(r["test_balanced_accuracy"]) for r in readout_rows if r["checkpoint_slug"] == "tfidf" and r["target"] == "leaf")
    ax.axhline(lexical, color="black", linestyle="--", label="char TF-IDF")
    ax.set_ylim(.72, 1.01); ax.set_title("Held-out-fact leaf readout")
    ax.set_ylabel("Balanced accuracy"); ax.legend(frameon=False, fontsize=8)

    endpoint = [r for r in cross_rows if r["reader"] in {"0p5b", "10b"} and r["target"] in {"0p5b", "10b"}]
    matrix = np.asarray([[next(float(r["normalized_mse"]) for r in endpoint if r["reader"] == reader and r["target"] == target) for target in ("0p5b", "10b")] for reader in ("0p5b", "10b")])
    ax = axes[1, 0]; im = ax.imshow(matrix, cmap="magma")
    ax.set_xticks([0, 1], ["h@0.5B", "h@10B"]); ax.set_yticks([0, 1], ["SAE@0.5B", "SAE@10B"])
    for i in range(2):
        for j in range(2): ax.text(j, i, f"{matrix[i,j]:.3f}", ha="center", va="center", color="white" if matrix[i,j] > matrix.mean() else "black")
    ax.set_title("Measured cross-reader normalized MSE"); fig.colorbar(im, ax=ax, fraction=.046)

    ax = axes[1, 1]
    qwen = [r for r in relation_rows if r["checkpoint_slug"] == "qwen3_0p6b"]
    late = [r for r in relation_rows if r["checkpoint_slug"] == "10b" and r["representation"] == "h"]
    width = .36; positions = np.arange(3)
    ax.bar(positions - width/2, [float(next(r["mean_margin"] for r in late if r["relation"] == rel)) for rel in ("coarse", "fine", "fact")], width, label="Our h@10B")
    ax.bar(positions + width/2, [float(next(r["mean_margin"] for r in qwen if r["relation"] == rel)) for rel in ("coarse", "fine", "fact")], width, label="Qwen endpoint")
    ax.axhline(0, color="black", linewidth=.8); ax.set_xticks(positions, ["coarse", "fine", "fact"])
    ax.set_title("Endpoint sanity reference (unmatched)"); ax.set_ylabel("Relation margin"); ax.legend(frameon=False)

    for ax in axes.flat[:2]: ax.set_xticks(x, labels); ax.set_xlabel("Training tokens"); ax.grid(alpha=.18)
    fig.suptitle("Observed checkpoint-only results — fixed candidate panel", fontweight="bold")
    fig.tight_layout(); fig.savefig(FIGURES / "semantic_observed.png", dpi=180); plt.close(fig)


def difference_figure(labels, relation_rows, readout_rows, cross_rows, endpoint_rows):
    fig, axes = plt.subplots(2, 2, figsize=(14, 9)); x = np.arange(len(labels)); slugs = ["0p5b", "1b", "3b", "5b", "10b"]
    ax = axes[0, 0]
    order = [(rep, rel) for rep in ("h", "h_hat", "c") for rel in ("coarse", "fine", "fact")]
    means = np.asarray([next(r["delta_10b_minus_0p5b"] for r in endpoint_rows if (r["representation"], r["relation"]) == item) for item in order])
    low = np.asarray([next(r["paired_ci95_low"] for r in endpoint_rows if (r["representation"], r["relation"]) == item) for item in order])
    high = np.asarray([next(r["paired_ci95_high"] for r in endpoint_rows if (r["representation"], r["relation"]) == item) for item in order])
    ax.errorbar(np.arange(9), means, yerr=[means-low, high-means], fmt="o", capsize=3)
    ax.axhline(0, color="black", linewidth=.8); ax.set_xticks(np.arange(9), [f"{a}\n{b}" for a,b in order], rotation=25)
    ax.set_title("Paired endpoint change: 10B - 0.5B"); ax.set_ylabel("Margin change (95% fact-block CI)")

    ax = axes[0, 1]
    rr = [r for r in relation_rows if r["representation"] == "h" and r["relation"] == "coarse" and r["checkpoint_slug"] in slugs]
    actual = np.asarray([float(r["mean_margin"]) for r in rr]); illustrative = np.linspace(actual[0], actual[-1], 5)
    ax.plot(x, illustrative, "--", color="gray", label="simple monotonic expectation")
    ax.plot(x, actual, marker="o", label="observed h coarse")
    ax.set_title("Trajectory shape differs from the simple picture"); ax.set_ylabel("Coarse relation margin"); ax.legend(frameon=False)

    ax = axes[1, 0]
    reps = ("h", "h_hat_adapted", "h_to_h_hat_frozen", "c")
    lexical = next(float(r["test_balanced_accuracy"]) for r in readout_rows if r["checkpoint_slug"] == "tfidf" and r["target"] == "leaf")
    for rep in reps:
        rr = [r for r in readout_rows if r["target"] == "leaf" and r["representation"] == rep and r["checkpoint_slug"] in slugs]
        ax.plot(x, [float(r["test_balanced_accuracy"])-lexical for r in rr], marker="o", label=rep)
    ax.axhline(0, color="black", linewidth=.8); ax.set_title("Model readout above the lexical control")
    ax.set_ylabel("Leaf balanced-accuracy difference"); ax.legend(frameon=False, fontsize=8)

    ax = axes[1, 1]
    values = {f"{r['reader']}->{r['target']}": float(r["normalized_mse"]) for r in cross_rows}
    names = ["0.5->0.5", "0.5->10", "10->0.5", "10->10"]
    vals = [values["0p5b->0p5b"], values["0p5b->10b"], values["10b->0p5b"], values["10b->10b"]]
    ax.bar(np.arange(4), vals, color=["#2ca02c", "#d62728", "#d62728", "#2ca02c"])
    ax.set_xticks(np.arange(4), names); ax.set_title("Matched versus cross-checkpoint SAE readers")
    ax.set_ylabel("Normalized MSE (lower is better)")

    for ax in (axes[0,1], axes[1,0]): ax.set_xticks(x, labels); ax.set_xlabel("Training tokens"); ax.grid(alpha=.18)
    fig.suptitle("Expected–observed differences and validity warnings", fontweight="bold")
    fig.tight_layout(); fig.savefig(FIGURES / "semantic_difference.png", dpi=180); plt.close(fig)


def copy_curated_sources():
    for name in ("relation_margins.png", "readout_accuracy.png", "cross_reader_quality.png", "pca_h_0p5b.png", "pca_h_3b.png", "pca_h_10b.png", "tsne_h_0p5b.png", "tsne_h_10b.png"):
        shutil.copy2(RUN / "figures" / name, FIGURES / f"semantic_raw_{name}")
    for name in ("relation_margins.csv", "readout_accuracy.csv", "cross_reader_quality.csv"):
        shutil.copy2(RUN / "tables" / name, TABLES / f"semantic_raw_{name}")


def finalize_manifest():
    path = TABLES / "semantic_result_source_manifest.json"
    manifest = json.loads(path.read_text())
    artifacts = []
    for folder, pattern in ((FIGURES, "semantic_*.png"), (TABLES, "semantic_*.csv")):
        for artifact in sorted(folder.glob(pattern)):
            artifacts.append({
                "path": str(artifact.relative_to(HERE)),
                "sha256": sha256(artifact),
                "size_bytes": artifact.stat().st_size,
            })
    manifest["curated_artifacts"] = artifacts
    path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main():
    FIGURES.mkdir(parents=True, exist_ok=True); TABLES.mkdir(parents=True, exist_ok=True)
    cfg, relation_rows, readout_rows, cross_rows, endpoint_rows = audit_and_derive()
    hypothesis_figure(cfg["checkpoint_labels"])
    observed_figure(cfg["checkpoint_labels"], relation_rows, readout_rows, cross_rows)
    difference_figure(cfg["checkpoint_labels"], relation_rows, readout_rows, cross_rows, endpoint_rows)
    copy_curated_sources()
    finalize_manifest()
    print(json.dumps({"status": "PASS", "figures": 3, "paired_delta_rows": len(endpoint_rows)}, sort_keys=True))


if __name__ == "__main__":
    main()
