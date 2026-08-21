# DCLM Transition-Object Spectrum Comparison Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Extract eight frozen all-layer activation objects from one 2,048-token DCLM forward, compute common-contract centered covariance spectra, render per-object and aggregate comparisons, and archive a registered object-sensitivity verdict.

**Architecture:** A focused experiment package separates pure object construction, pure spectrum metrics, model extraction, and deterministic rendering. The model forward stores only the raw block input and Attention write needed to derive all objects, while a native MLP pre-hook supplies an identity guard. Raw outputs live under the worker run root; canonical Summary/Detailed and curated figures live beside the Protocol.

**Tech Stack:** Python 3.10, PyTorch, Transformers, NumPy, Matplotlib, pytest, one H100.

## Global Constraints

- Use exactly the frozen Qwen3-8B model and first 2,048 `uint32` tokens of the named DCLM shard.
- Preserve all eight registered objects, all 35 adjacent transitions, and all 36 same-layer states/updates.
- Center over token rows; use float32 sample-space Gram eigenspectra; normalize eigenvalues by trace.
- Plot rank 1--2,048 with log y-axis `[1e-12, 1]` and identical coordinates.
- Do not change the Protocol, train, use labels, commit, push, publish, sync, or infer functionality.

---

### Task 1: Pure Object And Spectrum Contracts

**Files:**
- Create: `Projects/from-attention-to-search/XingyuD/MoE_Routing_Experiments/active/a15_08_04_e01_dclm_transition_object_spectrum_comparison/core.py`
- Create: `Projects/from-attention-to-search/XingyuD/MoE_Routing_Experiments/active/a15_08_04_e01_dclm_transition_object_spectrum_comparison/tests/test_core.py`

**Interfaces:**
- `build_objects(h, a, norm_fns) -> dict[str, list[Tensor]]`
- `covariance_spectrum(matrix) -> SpectrumMetrics`
- `paired_contrast(rows, left, right) -> dict[str, float]`

- [ ] Write synthetic failing tests for all eight formulas, layer counts, centering rank cap, normalized monotone spectrum, low-rank recovery, constant rejection, and contrast metrics.
- [ ] Run the focused test and verify failure because `core.py` is absent.
- [ ] Implement only the tested pure functions and dataclass.
- [ ] Re-run focused tests and require all pass.

### Task 2: Frozen DCLM Extraction And Identity Guards

**Files:**
- Create: `Projects/from-attention-to-search/XingyuD/MoE_Routing_Experiments/active/a15_08_04_e01_dclm_transition_object_spectrum_comparison/extract.py`
- Create: `Projects/from-attention-to-search/XingyuD/MoE_Routing_Experiments/active/a15_08_04_e01_dclm_transition_object_spectrum_comparison/tests/test_extraction_contract.py`

**Interfaces:**
- `load_token_slice(path, offset, count) -> Tensor`
- `capture_activations(model, input_ids) -> CaptureResult`
- writes `activations.pt`, `preflight.json`, and `extraction_manifest.json`.

- [ ] Write failing tests for exact uint32 slice loading, SHA identity, and hook-coverage/reconstruction guard helpers.
- [ ] Run focused tests and verify the missing implementation failure.
- [ ] Implement local model loading, all-token hooks, replay smoke, activation storage, and manifests.
- [ ] Run all package tests.
- [ ] Execute 128-token smoke; require 36 layers, native-$Z$ and $Z=X+U$ relative error below `1e-5`, and exact replay.
- [ ] Execute the frozen 2,048-token extraction only after smoke passes.

### Task 3: All Spectra, Metrics, And Registered Verdict

**Files:**
- Create: `Projects/from-attention-to-search/XingyuD/MoE_Routing_Experiments/active/a15_08_04_e01_dclm_transition_object_spectrum_comparison/analyze.py`

**Interfaces:**
- consumes `activations.pt` and extraction manifest.
- writes `arrays/spectra.npz`, `tables/spectrum_metrics.csv`, `tables/paired_contrasts.csv`, and `verdict.json`.

- [ ] Add a tiny synthetic analysis smoke to tests that verifies schemas and the registered verdict mapper.
- [ ] Implement sequential GPU/CPU spectrum computation without retaining derived full matrices.
- [ ] Run full analysis and assert 283 curves, finite traces, monotone spectra, normalized sums, exact condition/layer coverage, and one typed verdict.

### Task 4: Per-Object And Aggregate Figures

**Files:**
- Create: `Projects/from-attention-to-search/XingyuD/MoE_Routing_Experiments/active/a15_08_04_e01_dclm_transition_object_spectrum_comparison/render.py`
- Create: `Projects/from-attention-to-search/XingyuD/MoE_Routing_Experiments/active/a15_08_04_e01_dclm_transition_object_spectrum_comparison/tests/test_render_contract.py`

**Interfaces:**
- consumes `spectra.npz` and metric tables.
- writes eight PNG/PDF condition figures, `all_objects_common_axes_grid`, `all_objects_layer_median_comparison`, and `r80_by_layer_and_object`.

- [ ] Write a failing render-contract test for filenames, shared axis constants, and all-layer series counts.
- [ ] Implement deterministic rendering with a layer colorbar and no curve selection.
- [ ] Run render tests and full renderer.
- [ ] Visually inspect every central PNG and verify shared coordinates, labels, no clipping, and all curves.

### Task 5: Evidence Records And Final Verification

**Files:**
- Create: `Projects/from-attention-to-search/main/experiments/A15/15_08_target_conditioned_layer_innovation/A15_08_04_E01_dclm_transition_object_spectrum_comparison/summary.md`
- Create: `Projects/from-attention-to-search/main/experiments/A15/15_08_target_conditioned_layer_innovation/A15_08_04_E01_dclm_transition_object_spectrum_comparison/detailed.md`
- Modify: the A15_08_04 Anchor Sections 7--8 only after eligible evidence exists.

**Interfaces:**
- consumes Protocol, manifests, tables, verdict, and audited figures.
- produces canonical result reading path and artifact map.

- [ ] Read the result-lineage and detailed-record references before writing results.
- [ ] Audit Protocol conformance and record any deviations before interpretation.
- [ ] Copy only decision-bearing figures/tables to the canonical result directory.
- [ ] Write conclusion-first Summary and complete Detailed evidence ledger.
- [ ] Update Anchor Sections 7--8 with the direct result and bounded next decision.
- [ ] Run full tests, Python compilation, artifact hashes, count/schema checks, link checks, and visual audit.
- [ ] Do not commit; report local artifacts and ask the researcher for the closed-book result interpretation.

