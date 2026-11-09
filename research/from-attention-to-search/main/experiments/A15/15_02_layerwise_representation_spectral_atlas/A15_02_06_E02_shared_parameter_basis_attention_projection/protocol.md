---
experiment_id: A15_02_06_E02_shared_parameter_basis_attention_projection
anchor_id: 15_02_06_mlp_parameter_geometry_and_semantic_location
status: RESULT_COMPLETE_BASIS_SENSITIVE_AI_DRAFT_AWAITING_HUMAN_CONFIRMATION
canonical_language: en
approved: 2026-08-11
---

# Protocol: Shared MLP-Parameter Bases And Layerwise Attention-Write Projection

## 0. Approval Snapshot

- Researcher authorization: the 2026-08-11 instruction explicitly authorizes the minimal experiment, at least two common-basis constructions, implementation without another approval round, full local execution, normalized log-scale figures, result analysis, and canonical records.
- A--G audit blocks: `CONFIRMED`; cross-block consistency: `PASS`.
- Execution state: `RESULT_COMPLETE_BASIS_SENSITIVE_AI_DRAFT_AWAITING_HUMAN_CONFIRMATION`; the unchanged frozen estimator completed locally on all 36 layers.
- This experiment is a bounded coordinate diagnostic under A15_02_06. It does not replace the current project-level next decision unless the researcher later confirms such an update.
- Training, Router construction, remote submission, graph editing, root sync, commit, and push are outside scope.

## A. Question And Claim Boundary — CONFIRMED

### A1. Decision question

Can two parameter-only constructions define non-random cross-layer MLP input coordinates, and, in those fixed coordinates, does conditional-fine variance of the isolated Attention write move from earlier to later parameter rank as model depth increases?

Here “Attention write” means the direct `self_attn.o_proj` output before residual addition. “Later rank” is construction-specific and is defined in Section D; it is not assumed to be a universal semantic frequency axis.

### A2. Typed outcomes

- `shared_coordinate_right_shift`: both common-coordinate screens pass; both registered depth contrasts have 95% bootstrap lower bounds above zero; and both expression halves preserve a positive direction.
- `basis_sensitive_shift`: both coordinate screens pass, but the two bases disagree on the registered positive-shift decision or a basis reverses sign in an expression half.
- `shared_coordinate_no_right_shift`: both coordinate screens pass and both depth-contrast 95% upper bounds are at or below zero.
- `insufficient_depth_shift`: both coordinate screens pass but neither the positive nor the non-positive decision is resolved.
- `coordinate_unvalidated`: at least one common basis fails its registered non-random diagonalization screen; any right/left language for that basis is withheld.
- `insufficient_<guard>`: a mandatory provenance, shape, orthogonality, energy-conservation, or replay guard fails.

### A3. Cannot claim

No outcome proves that the Attention write is information absent from the residual stream, that the write is low rank, that later shared-basis rank means finer semantics, that individual directions have cross-layer identity, that MLP gain causes the allocation, or that a Router using these features improves training or inference. This experiment tests only a shared-coordinate variance pattern.

## B. Data Construction And Provenance — CONFIRMED

### B1. Frozen fine-only semantic cube

Reuse exactly the balanced TAX semantic run

`/data/250010109/MoE_Router/experiments/20260809_a15_02_05_balanced_taxonomy_attention_write_atlas/runs/a15-02-05-e01-20260809T165500Z`.

The frozen data contain:

- 8 parent domains;
- 8 children within each parent;
- 4 templates and 2 fact bundles per child;
- 512 records total;
- two balanced expression halves A/B;
- one common readout at absolute position 57 after masked left padding.

The byte SHA-256 of `data/semantic_dataset.json` is `c37329fad2e48d759b659483ed6705306eeb5c19f32c0e98a505901ed588ed88`. The byte SHA-256 of `full_consolidated/extraction_manifest.json` is `6b9554702020e0aef2e51e6022937015c090414fad1c945afda1374f1da68f62`. Every registered Attention-state file must match that manifest.

Only conditional-fine structure is analyzed. Coarse/fine comparison is deliberately absent from this minimal step.

### B2. Conditional-fine variance object

For layer \(\ell\), parent \(p\), child \(c\), and expression record \(r\), let \(a_{\ell pcr}\in\mathbb R^{4096}\) be the cached Attention write. Define

\[
\mu_{\ell pc}=\mathbb E_r[a_{\ell pcr}],\qquad
\mu_{\ell p}=\frac{1}{8}\sum_{c=1}^{8}\mu_{\ell pc},
\]

and the parent-conditional child deviations

\[
d_{\ell pc}=\mu_{\ell pc}-\mu_{\ell p}.
\]

The tested fine-only covariance is

\[
B^{fine}_\ell=\frac{1}{8}\sum_{p=1}^{8}\frac{1}{8}\sum_{c=1}^{8}
d_{\ell pc}d_{\ell pc}^{\top}.
\]

Population weighting is used because every cell is balanced. Expression halves A and B repeat the same construction independently as a sign-stability guard.

### B3. Frozen representation cache

Use `full_consolidated/semantic_states/attention_write/layer_01.pt` through `layer_36.pt`. Each file must contain all 512 records, hidden width 4096, integer record indices covering the frozen dataset exactly once, and `site == attention_write`. No model inference is required.

## C. Diagnostic Task And Uncertainty — CONFIRMED

The model and all bases are frozen functions of parameters; semantic activations never select or tune a basis. There is no learned probe.

Uncertainty is over the eight parent domains. Use 2,000 paired parent bootstraps with replacement, seed 8110602. For each resample, recompute normalized per-layer energy, the rank centroid, and the registered late-minus-early contrast. Layers are not treated as independent replicates.

The two expression halves are diagnostic replications. They are not extra independent samples and are used only for the registered sign guard.

## D. Model, Parameter Operators, And Common Bases — CONFIRMED

### D1. Model and local parameter operator

- model: frozen `/data/share/Qwen3-8B`;
- 36 decoder blocks, hidden width \(d=4096\);
- parameter identity: `data/model_manifest.json` byte SHA-256 `a27a04e41a76b84e1d2a515e726a0607bb313032d432615d37172f347ecc214b`;
- FP32 Gram construction and symmetric eigendecomposition.

For every block,

\[
K_\ell=W_{gate,\ell}^{\top}W_{gate,\ell}
+W_{up,\ell}^{\top}W_{up,\ell}.
\]

For a unit input direction \(x\), \(x^{\top}K_\ell x\) is the squared native MLP input-side parameter response \(\lVert W_{gate,\ell}x\rVert^2+\lVert W_{up,\ell}x\rVert^2\). `down_proj` is excluded because it does not define residual-stream input directions.

### D2. Basis A: mean parameter-response basis (`mean_response`)

Trace-normalize every layer so each block has equal total weight:

\[
\widetilde K_\ell=\frac{K_\ell}{\operatorname{tr}(K_\ell)},\qquad
\overline K=\frac{1}{36}\sum_{\ell=1}^{36}\widetilde K_\ell.
\]

Let

\[
\overline K=V^{MR}\Lambda^{MR}(V^{MR})^{\top},
\qquad \lambda^{MR}_1\ge\cdots\ge\lambda^{MR}_{4096}.
\]

Meaning: \(v^{MR}_j\) is the \(j\)-th orthogonal direction ranked by average normalized squared MLP parameter response across layers. This basis preserves gain magnitudes within each layer but can be dominated by consistently extreme eigenvalues.

### D3. Basis B: rank-consensus basis (`rank_consensus`)

Eigendecompose each local operator \(K_\ell=V_\ell\Gamma_\ell V_\ell^{\top}\) in descending order. Divide each local spectrum into 16 fixed bands of 256 ranks and define projector \(P_{\ell b}\) for band \(b\in\{0,\ldots,15\}\). Give band \(b\) the ordinal score

\[
\omega_b=1-\frac{b+1/2}{16}.
\]

Construct

\[
S=\frac{1}{36}\sum_{\ell=1}^{36}\sum_{b=0}^{15}\omega_bP_{\ell b},
\qquad
S=V^{RC}\Lambda^{RC}(V^{RC})^{\top}
\]

with descending eigenvalues.

Meaning: \(v^{RC}_j\) is ranked by how consistently its subspace is assigned to early rather than late local parameter bands. This basis gives every layer and every direction equal ordinal treatment, discards singular-value magnitude, and is invariant to rotations inside each registered 256-dimensional local band.

## E. Objective And Numerical Contract — CONFIRMED

No parameter or model optimization occurs. The only objectives are the two deterministic symmetric eigendecompositions.

Mandatory numerical guards:

1. all parameter and Attention artifacts pass provenance and shape checks;
2. maximum relative symmetry error of every constructed operator is at most \(10^{-6}\);
3. relative Frobenius orthogonality error \(\lVert V^{\top}V-I\rVert_F/\sqrt d\) is at most \(5\times10^{-4}\);
4. relative eigen residual \(\lVert AV-V\Lambda\rVert_F/\lVert A\rVert_F\) is at most \(5\times10^{-4}\);
5. for every layer and basis, projected fine energy agrees with direct energy within relative error \(5\times10^{-4}\).

Any failed guard stops adjudication. A code repair that leaves Sections A--F unchanged is allowed and recorded; a scientific-definition change reopens approval.

## F. Metrics, Comparisons, And Figure Contracts — CONFIRMED

### F1. Common-coordinate validity screen

For shared basis \(V\) and local operator \(K_\ell\), define the diagonal-energy fraction

\[
\delta_{\ell,V}=
\frac{\sum_j(v_j^{\top}K_\ell v_j)^2}
{\operatorname{tr}(K_\ell^2)}.
\]

It equals one for an exact eigenbasis. Its Haar-random expectation is

\[
\delta^{Haar}_\ell=
\frac{2+(\operatorname{tr}K_\ell)^2/\operatorname{tr}(K_\ell^2)}{d+2}.
\]

A basis passes the non-random screen when all values are finite, the median \(\delta_{\ell,V}/\delta^{Haar}_\ell\) exceeds one, and at least 30 of 36 layers exceed one. This is a minimal coordinate-validity screen, not proof of exact simultaneous diagonalization or shared semantics. Report the complete layerwise ratios and distance from the local optimum \(\delta=1\).

### F2. Projected normalized fine variance

For either fixed shared basis \(V\), compute

\[
e_{\ell j}=v_j^{\top}B^{fine}_\ell v_j
=\frac{1}{64}\sum_{p,c}(d_{\ell pc}^{\top}v_j)^2,
\]

\[
p_{\ell j}=\frac{e_{\ell j}}{\sum_{k=1}^{4096}e_{\ell k}},
\qquad
r_j=\frac{j-1/2}{4096}.
\]

Thus \(p_{\ell j}\) is a within-layer share and \(\sum_jp_{\ell j}=1\). Absolute direct trace is also retained so normalization cannot hide a vanishing fine signal.

### F3. Registered depth statistic

The normalized rank centroid is

\[
C_{\ell,V}=\sum_{j=1}^{4096}p_{\ell j}r_j.
\]

The primary depth contrast is

\[
T_V=\operatorname{median}_{\ell=25:35}C_{\ell,V}
-\operatorname{median}_{\ell=1:12}C_{\ell,V}.
\]

Block 36 is displayed but excluded because it is a known boundary case in the parent experiment. Positive \(T_V\) means later blocks allocate relatively more conditional-fine variance to later rank in that basis.

### F4. Required figures

1. **Normalized log curves (primary requested figure).** Two panels, one per basis; x-axis is normalized shared-basis rank from early to late, y-axis is normalized fine-variance share on a log scale, and line color runs shallow to deep. A centered 129-rank arithmetic moving average is visualization-only; all statistics use unsmoothed \(p_{\ell j}\). Display selected layers 1, 6, 12, 18, 24, 30, 35, and 36 legibly and retain an all-layer companion.
2. **Layer-by-rank atlas.** One heatmap per basis using \(\log_{10}(4096p_{\ell j})\), with identical color limits. Allowed conclusion: relative allocation pattern in that construction, not individual feature identity.
3. **Centroid and validity audit.** Layerwise \(C_{\ell,V}\) with early/late windows and block 36 marked, plus \(\delta/\delta^{Haar}\) for both bases.

Every figure records source arrays, aggregation, axes, normalization, smoothing, allowed conclusion, and limitation. Every rendered image is inspected at full resolution before delivery.

## G. Execution And Reproducibility Boundary — CONFIRMED

### G1. Execution surface

- local host with available H100 GPU;
- worker directory: `/data/250010109/MoE_Router/experiments/20260811_a15_02_06_shared_parameter_basis_attention_projection`;
- canonical record directory: this Protocol's directory;
- no remote job and no new forward inference.

### G2. Run order and stop rules

1. Write unit tests for basis construction, within-band rotation invariance, projected-energy conservation, centroid normalization, and the analytic Haar expectation.
2. Run tests before implementation and record the expected red state.
3. Implement the analysis primitives, then require all unit tests to pass.
4. Smoke on synthetic operators and a reduced real subset; verify provenance, shapes, eigensolver, and projection energy.
5. Run all 36 parameter blocks and all 36 cached Attention-write layers.
6. Execute the frozen bootstrap and typed outcome logic before plotting.
7. Render and inspect every required figure; write `summary.md` and `detailed.md` with artifact checksums.

No failed layer, parent, direction, or expression half may be silently dropped. No result-driven basis, rank reversal, window change, or smoothing change is permitted.

## 1. Cross-Block Consistency Audit

- Question ↔ coordinate: `PASS`; both bases are parameter-only and have distinct registered meanings.
- Coordinate ↔ comparison: `PASS`; all Attention layers are projected into the same 4096-dimensional basis within each construction.
- Data ↔ metric: `PASS`; conditional-fine child deviations use one frozen balanced dataset and population weighting.
- Metric ↔ uncertainty: `PASS`; parent bootstrap targets domain variation without treating layers as replicates.
- Claim ↔ guard: `PASS`; common-coordinate validity is screened before any right-shift claim.
- Figure ↔ estimator: `PASS`; log curves are normalized, and smoothing is display-only.
- Execution ↔ authorization: `PASS`; the researcher explicitly authorized implementation, full analysis, plots, and result records without another approval round.

This file is frozen before inspecting the new projected-variance result. Retrospective changes to the bases, data object, early/late windows, bootstrap unit, primary statistic, or typed-outcome rules invalidate the adjudication.

## 2. Execution Outcome Snapshot

The registered typed outcome is `basis_sensitive_shift`. Both minimal coordinate screens passed, but only the mean-response basis produced a positive registered shift: \(T_{MR}=+0.03171\) with 95% parent-bootstrap interval \([+0.02058,+0.04433]\). The rank-consensus basis produced \(T_{RC}=-0.00755\) with interval \([-0.01869,+0.00121]\). This status update records the execution outcome without changing any frozen scientific definition above. The knowledge wording remains `AI_DRAFT_AWAITING_HUMAN_CONFIRMATION`.
