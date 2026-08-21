# Scheme A Common-Spectrum Curves And 0817 Meeting Report Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Render the already-frozen blockwise residual-update energy as full 4,096-direction normalized curves in both common parameter bases, then write an 0817 Chinese meeting report that teaches the functional result, the linear-residualization boundary, and how to judge the geometry independently.

**Architecture:** Reuse `arrays/spectral_profiles.npz`; do not rerun the model, residualizer, PCA, or confirmation evaluation. Add pure normalization/smoothing helpers and a deterministic renderer to experiment two's finalizer, regenerate its manifest, mirror the new evidence into the curated experiment directory, and place a report-facing copy under `daily_research_reports/0817`.

**Tech Stack:** Python 3.10, NumPy, Matplotlib, pytest, Markdown.

## Global Constraints

- Use CONFIRMATION direction energies already frozen for blocks 2--36.
- Plot exactly blocks `[2, 6, 10, 14, 18, 24, 25, 28, 32, 36]`.
- Use two panels: Mean Response and Rank Consensus.
- Compute directionwise variance first, then normalize within each layer: `p_lj=e_lj/sum_j(e_lj)`.
- Plot variance density `4096*p_lj` on a logarithmic y-axis.
- Use a centered 129-rank arithmetic moving average for display only.
- Treat the new figure as post-hoc descriptive shape evidence; it cannot change the registered functional, depth, basis-sensitivity, or low-rank verdicts.
- Do not train a model, reopen selection, change experiment tables, commit, push, or publish externally.

---

### Task 1: Add Tested Common-Spectrum Curve Helpers

**Files:**
- Modify: `Projects/from-attention-to-search/XingyuD/MoE_Routing_Experiments/active/a15_08_03_e01_function_admitted_update_spectral_rank_analysis/finalize.py`
- Test: `Projects/from-attention-to-search/XingyuD/MoE_Routing_Experiments/active/a15_08_03_e01_function_admitted_update_spectral_rank_analysis/tests/test_spectral_curve_rendering.py`

**Interfaces:**
- Consumes: one-dimensional nonnegative direction energy arrays of length 4,096.
- Produces: `normalized_variance_density(values: np.ndarray) -> np.ndarray` and `smooth_curve(values: np.ndarray, width: int) -> np.ndarray`.

- [x] Write failing tests that require density to sum to 4,096, preserve a uniform spectrum at density one, reject zero total energy, and use truncated centered windows at curve endpoints.
- [x] Run `python -m pytest -q tests/test_spectral_curve_rendering.py` and verify the helpers are missing.
- [x] Implement the two pure helpers without changing any registered estimator.
- [x] Re-run the focused test and the complete seven-test experiment-two suite.

### Task 2: Render And Archive Scheme A

**Files:**
- Modify: `Projects/from-attention-to-search/XingyuD/MoE_Routing_Experiments/active/a15_08_03_e01_function_admitted_update_spectral_rank_analysis/finalize.py`
- Create: raw-run `figures/common_basis_normalized_variance_curves_selected_layers.{png,pdf}`
- Create: raw-run `common_basis_curve_receipt.json`
- Modify: raw-run and curated `summary.md`, `detailed.md`, and artifact manifests.

**Interfaces:**
- Consumes: `mean_response_direction_energy[35,3,4096]`, `rank_consensus_direction_energy[35,3,4096]`, layer order, and split order from `spectral_profiles.npz`.
- Produces: a two-panel log-density figure and a receipt recording source array, split, selected layers, normalization, smoothing, and claim boundary.

- [x] Add a deterministic two-panel renderer using the approved layers and CONFIRMATION split.
- [x] Highlight blocks 24 and 28 as function-admitted and block 25 as unresolved without changing their numeric curves.
- [x] Add one concise curve-shape paragraph to experiment two's generated detailed report and a figure-availability bullet to its summary.
- [x] Run `python finalize.py`, visually inspect the PNG, and verify both bases, all ten layers, log scale, labels, and readable legend.
- [x] Mirror summary, detailed report, figures, receipt, and manifest into the curated experiment directory.

### Task 3: Write The 0817 Teaching-Oriented Meeting Report

**Files:**
- Create: `daily_research_reports/0817/docs/sync.md`
- Create: `daily_research_reports/0817/figures/common_basis_normalized_variance_curves_selected_layers.{png,pdf}`

**Interfaces:**
- Consumes: experiment-one primary table, experiment-two verdicts, the new common-spectrum figure, and existing 0816 report.
- Produces: one Chinese report usable for self-study and a five-minute oral presentation.

- [x] Explain the three experiment-one levels: 25/35 positive raw gains, 17/35 positive matched point estimates, and only blocks 24/28 simultaneously confirmed.
- [x] Explain why `X -> R_U` linear unpredictability does not imply `R_U -> Y` linear unreadability, using one algebraic and one plain-language example.
- [x] State the valid limitation that linear residualization does not remove nonlinear predictability from `X`.
- [x] Define the new curve as common-basis directionwise variance density, not an `R_U` singular-value curve.
- [x] Teach how to judge function, depth trend, spectral relocation, stable representation rank, and functional compression as five separate questions.
- [x] Add a five-minute plain-language script, likely questions, safe answers, blockers, and next-step options.

### Task 4: Final Verification

**Files:**
- Verify all files above; no new scientific estimator files.

**Interfaces:**
- Consumes: generated code, raw artifacts, curated mirror, and report.
- Produces: fresh evidence that code, files, claims, and mirrors are consistent.

- [x] Run both experiment test suites and Python compilation.
- [x] Verify the raw artifact manifest byte sizes and SHA-256 hashes.
- [x] Verify raw and curated summaries, detailed reports, new figures, receipt, and manifest are byte-identical.
- [x] Validate the new figure dimensions/non-empty files and visually inspect it.
- [x] Check the 0817 report for stale `NOT RUN` language, broken local links, missing numeric claims, placeholders, and trailing whitespace.
