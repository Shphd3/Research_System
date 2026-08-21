# Shared Functional Subspace Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Measure pairwise overlap among eight task-specific supervised low-rank input subspaces and test whether one shared subspace preserves their held-out task gains, including any dimension increase relative to independent subspaces.

**Architecture:** Leave the frozen E03 code, cached activations, task states, and existing confirmation artifacts unchanged. Add a self-contained analysis extension that extracts task-specific RRR coefficient subspaces, builds an equal-task-weight shared projector by truncated SVD of normalized task coefficient maps, refits only the projected correction heads with the existing TRAIN/DEVELOPMENT ridge procedure, and evaluates the frozen curve on the already-opened confirmation split.

**Tech Stack:** Python 3.12, NumPy, PyTorch, pandas, matplotlib, pytest.

**Spec:** `/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_08_target_conditioned_layer_innovation/A15_08_06_E03_aligned_hierarchical_taxonomy_replication/protocol_cn.md`

## Global Constraints

- Reuse Qwen3-8B block 24/28 cached standardized `X` and `R_U`; do not rerun model extraction.
- Preserve the existing eight domains, 8-way centered targets, five-fold OOF base logits, ridge grid, TRAIN/DEVELOPMENT split, and confirmation rows.
- Learn every projector and correction head without confirmation labels; confirmation is evaluation only.
- Do not modify frozen source snapshots or existing result files.
- Main overlap metric is normalized projection overlap `||Q_i^T Q_j||_F^2 / min(r_i, r_j)` in `[0, 1]`; because the observed off-diagonal values are below `0.02`, the heatmap masks the trivial unit diagonal and zooms the shared off-diagonal scale while printing every exact value.
- Main local heatmap uses requested RRR rank 8 because this is the first frozen independent rank that preserves at least 90% functionality for every task; layer 24 and layer 28 are separate panels.
- Shared rank grid is `{1, 2, 4, 8, 16, 32, 56, 64}`.
- Shared projector uses equal task weight: normalize each task RRR coefficient map to unit Frobenius norm, concatenate the eight maps, and take its left singular vectors.
- Report both mean-domain and worst-domain 80%/90% functionality crossings; never infer an intrinsic representation rank.

---

### Task 1: Tested Subspace Algebra

**Files:**
- Create: `/data/250010109/MoE_Router/experiments/20260819_a15_08_06_e03_aligned_hierarchical_taxonomy_replication/shared_functional_subspace_v1/shared_subspace_core.py`
- Create: `/data/250010109/MoE_Router/experiments/20260819_a15_08_06_e03_aligned_hierarchical_taxonomy_replication/shared_functional_subspace_v1/tests/test_shared_subspace_core.py`

**Interfaces:**
- Consumes: dense coefficient matrices shaped `[hidden, outputs]`.
- Produces: `coefficient_basis(coefficient, rank)`, `projection_overlap(a, b)`, and `shared_basis(coefficients, max_rank)`.

- [ ] **Step 1: Write failing tests** using hand-constructed identical, orthogonal, and partially overlapping coordinate subspaces; assert overlaps `1`, `0`, and `0.5`, and assert that the shared SVD basis reconstructs the union of two orthogonal rank-one maps at rank two.
- [ ] **Step 2: Run tests and verify RED** with `pytest -q shared_functional_subspace_v1/tests/test_shared_subspace_core.py`; expected failure is missing `shared_subspace_core`.
- [ ] **Step 3: Implement the minimal algebra** with float64 SVD, deterministic sign canonicalization, input validation, equal-task Frobenius normalization, and orthonormality checks.
- [ ] **Step 4: Run tests and verify GREEN** with the same pytest command; expected `4 passed`.

### Task 2: Frozen-Data Shared Functional Evaluation

**Files:**
- Create: `/data/250010109/MoE_Router/experiments/20260819_a15_08_06_e03_aligned_hierarchical_taxonomy_replication/shared_functional_subspace_v1/run_shared_analysis.py`
- Create: `/data/250010109/MoE_Router/experiments/20260819_a15_08_06_e03_aligned_hierarchical_taxonomy_replication/shared_functional_subspace_v1/tests/test_shared_analysis.py`
- Read only: frozen preconfirmation task states, TRAIN/DEVELOPMENT residual arrays, confirmation residual arrays, and metadata files.

**Interfaces:**
- Consumes: original task `.pt` states plus cached standardized arrays.
- Produces: `shared_subspace_result.json`, `task_subspace_overlap.csv`, `shared_functional_curves.csv`, and per-row gain archives.

- [ ] **Step 1: Write failing integration tests** on a synthetic two-task fixture; verify no test labels enter projector construction, shared rank two matches two orthogonal task spaces, and rank one fails the all-task 90% criterion.
- [ ] **Step 2: Run tests and verify RED** with `pytest -q shared_functional_subspace_v1/tests/test_shared_analysis.py`; expected failure is missing analysis functions.
- [ ] **Step 3: Implement frozen-data loading and target reconstruction** by importing the existing snapshot's `oof_predictions`, `select_spectral_ridge`, `prepare_affine_spectral`, `predict_affine`, `stratified_fold_ids`, constants, and metadata loader.
- [ ] **Step 4: Implement local overlap extraction** from rank-8 RRR coefficient maps for the two layers and save all pairwise values with the Haar expectation `rank / 4096`.
- [ ] **Step 5: Implement shared projector construction and refitting** for every frozen rank; fit task-specific correction heads on TRAIN and select ridge lambda on DEVELOPMENT only.
- [ ] **Step 6: Implement confirmation evaluation and bootstrap** using the existing base states and cached confirmation arrays; save per-domain gain, full-gain retention, mean retention, worst-domain retention, and 80%/90% crossings.
- [ ] **Step 7: Run both test files** and expect all tests to pass.
- [ ] **Step 8: Run the real analysis** into a new immutable output directory `runs/shared-functional-20260820T_shared_r1` and verify all 16 layer-domain tasks and all eight ranks are present.

### Task 3: Figures and Research Handoff

**Files:**
- Create: `/data/250010109/MoE_Router/experiments/20260819_a15_08_06_e03_aligned_hierarchical_taxonomy_replication/shared_functional_subspace_v1/render_shared_analysis.py`
- Create: `/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_08_target_conditioned_layer_innovation/A15_08_06_E03_aligned_hierarchical_taxonomy_replication/figures/figure_9_task_subspace_overlap_heatmap.png`
- Create: `/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_08_target_conditioned_layer_innovation/A15_08_06_E03_aligned_hierarchical_taxonomy_replication/figures/figure_10_shared_vs_independent_functional_dimension.png`
- Create: `/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_08_target_conditioned_layer_innovation/A15_08_06_E03_aligned_hierarchical_taxonomy_replication/tables/task_subspace_overlap.csv`
- Create: `/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_08_target_conditioned_layer_innovation/A15_08_06_E03_aligned_hierarchical_taxonomy_replication/tables/shared_functional_curves.csv`
- Create: `/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_08_target_conditioned_layer_innovation/A15_08_06_E03_aligned_hierarchical_taxonomy_replication/shared_subspace_analysis.md`

**Interfaces:**
- Consumes: Task 2 JSON/CSV outputs.
- Produces: two publication-ready figures and a concise Chinese interpretation led by overlap and shared-dimension findings.

- [ ] **Step 1: Implement the heatmap** as two panels for block 24 and 28, numeric annotations, identical domain order, masked unit diagonal, a shared off-diagonal color scale, and a caption stating rank 4, the full metric range `[0, 1]`, and the Haar baseline.
- [ ] **Step 2: Implement the dimension figure** with projected dimension on a log2 x-axis and full-gain retention on the y-axis; show independent-RRR mean, shared mean, shared worst-domain, and horizontal 0.8/0.9 lines for each layer.
- [ ] **Step 3: Render outputs and inspect both PNGs** for readable axes, labels, annotations, and no clipping.
- [ ] **Step 4: Write the handoff** with the exact overlap mean/range, independent and shared crossings, dimension inflation, claim boundary, and links to figures/tables.
- [ ] **Step 5: Run final verification**: pytest, result schema/count audit, numerical orthonormality/overlap bounds, source-input SHA256 receipt, CSV-to-JSON equality, and PNG decode checks.
