---
experiment_id: A15_02_06_E04_layer8_to9_shared_basis_growth
anchor_id: 15_02_06_mlp_parameter_geometry_and_semantic_location
status: EXECUTED_RESULTS_RECORDED
canonical_language: en
approved: 2026-08-12
---

# Protocol: Layer 8 To 9 Attention-Write Growth In One Shared Parameter Basis

## 0. Approval Snapshot

- The researcher explicitly authorized the complete layer-8/9 experiment, fixed the previously built Mean Response basis, requested normalized rank curves in the same direction identities, and requested all necessary figures on 2026-08-12.
- The one uncertainty is whether block 9, relative to block 8, allocates more Attention-write variance to the previously frozen fine-enriched shared-spectrum region.
- Treatment is block 9; control is block 8. Model, records, readout token, Attention-write hook, basis, rank order, semantic region, normalization, resampling unit, and plotting rules are held fixed.
- The primary metric is the block-9 minus block-8 normalized variance-share change in ranks `[0.50,0.75)`. Absolute variance growth is a mandatory interpretation guard.
- Execution scope includes implementation, tests, local smoke, all 512 cached records for blocks 8 and 9, 2,000 parent bootstraps, exactly two final figures, and canonical result records.
- This is a coordinate and variance audit. It cannot establish information-theoretic novelty, residual-relative target gain, low rank, causal function, or Router utility.

## A. Question And Typed Outcomes — CONFIRMED

### A1. Decision question

In the frozen global Mean Response basis, does the normalized variance of block-9 Attention writes increase relative to block 8 in the independently frozen fine-enriched region `[0.50,0.75)`, and is that increase an absolute energy increase rather than only a within-layer reallocation?

### A2. Typed outcomes

- `aligned_absolute_growth`: normalized-share change in `[0.50,0.75)` has parent-bootstrap 95% lower bound above zero, both expression halves are positive, the region exceeds every other aligned rank quartile under a simultaneous bootstrap contrast, absolute region-energy log-ratio has lower bound above zero, and block-9 fine-minus-coarse semantic share has lower bound above zero with positive A/B signs.
- `aligned_relative_redistribution`: the normalized and semantic clauses pass, but absolute region growth is unresolved or non-positive.
- `positive_not_region_specific`: normalized region growth and semantic fine-enrichment pass, but the region is not larger than every other quartile.
- `no_aligned_growth`: the normalized region-change 95% upper bound is at or below zero.
- `unresolved_alignment`: no previous typed outcome applies.
- `insufficient_<guard>`: a required provenance, balance, basis, hook, energy-conservation, split, bootstrap, or figure guard fails.

“Growth” in the verdict means variance or normalized variance share. It is never silently renamed “new knowledge.”

## B. Frozen Symbols, Data, And Coordinate — CONFIRMED

### B1. Layer objects

For record $x$ and block $\ell\in\{8,9\}$, define

$$
A_\ell(x)\in\mathbb R^{4096}
$$

as the direct `self_attn.o_proj` output before residual addition at the shared final `Classification:` colon. It is the current measurable Attention write, not information proven absent from the incoming residual.

The frozen data are the same audited 512 records used by E03: 8 academic parents, 8 children per parent, 4 templates, 2 fact bundles, balanced expression halves A/B, and absolute readout position 57. Source run:

`/data/250010109/MoE_Router/experiments/20260809_a15_02_05_balanced_taxonomy_attention_write_atlas/runs/a15-02-05-e01-20260809T165500Z`.

### B2. Common parameter spectrum

For every model block,

$$
K_\ell=W_{gate,\ell}^{\top}W_{gate,\ell}+W_{up,\ell}^{\top}W_{up,\ell},
\qquad
\bar K=\frac1{36}\sum_{\ell=1}^{36}\frac{K_\ell}{\operatorname{tr}K_\ell}.
$$

The frozen Mean Response eigensystem is

$$
\bar K=V\Lambda V^\top,
\qquad V=[v_1,\ldots,v_{4096}],
\qquad \lambda_1\ge\cdots\ge\lambda_{4096}.
$$

Both blocks use this exact same $V$ and direction ordering. Rank runs from larger to smaller average trace-normalized MLP input-side parameter response. No block-8/9 activation enters basis construction or direction selection.

### B3. Projected states and covariance

For split $s\in\{full,A,B\}$, center records inside that split:

$$
z^{(s)}_{\ell x}=A_\ell(x)^\top V,\qquad
\tilde z^{(s)}_{\ell x}=z^{(s)}_{\ell x}-\mathbb E_{x\in s}z^{(s)}_{\ell x}.
$$

Directionwise raw variance, normalized share, and rank center are

$$
e^{(s)}_{\ell j}=\mathbb E_{x\in s}(\tilde z^{(s)}_{\ell xj})^2,
\qquad
p^{(s)}_{\ell j}=\frac{e^{(s)}_{\ell j}}{\sum_ke^{(s)}_{\ell k}},
\qquad
r_j=\frac{j-1/2}{4096}.
$$

The primary direction curve is

$$
\Delta p_j=p^{full}_{9j}-p^{full}_{8j}.
$$

$\Delta p_j>0$ means block 9 emphasizes the same shared direction more strongly as a fraction of its own total write variance. It does not by itself mean raw variance increased.

## C. Bands, Primary Metric, And Absolute Guard — CONFIRMED

### C1. Fixed bands

Use 16 aligned equal-rank bands $F_1,\ldots,F_{16}$ of 256 shared directions each. Individual 4096-direction curves are display evidence; inference uses the fixed bands to avoid post-hoc peak selection.

For band $F_b$,

$$
Q_{\ell b}=\sum_{j\in F_b}p_{\ell j},
\qquad
\Delta Q_b=Q_{9b}-Q_{8b},
$$

and

$$
G_b=\log_2\frac{\sum_{j\in F_b}e_{9j}}
{\sum_{j\in F_b}e_{8j}}.
$$

### C2. Independently frozen semantic region

The primary region is

$$
B_{sem}=F_9\cup F_{10}\cup F_{11}\cup F_{12},
$$

equivalent to normalized ranks `[0.50,0.75)` and one-based directions 2049--3072. E03 froze this interval before the present block-8/9 analysis and found positive fine-minus-coarse share across blocks. It is not reselected from the present transition curve.

The primary metric is

$$
D_{sem}=Q_9(B_{sem})-Q_8(B_{sem}).
$$

The absolute guard is

$$
G_{sem}=\log_2\frac{E_9(B_{sem})}{E_8(B_{sem})}.
$$

The aligned-quartile specificity guard compares $D_{sem}$ with the maximum of `[0,0.25)`, `[0.25,0.50)`, and `[0.75,1.00)` using the same bootstrap draw. No sliding window is optimized.

### C3. Semantic bridge at block 9

Reuse E03's frozen hierarchy definition in the same block-9 projected child means. Let $p_{9,C}$ and $p_{9,F}$ be the normalized coarse and fine hierarchical spectra. Define

$$
S_{9,F-C}(B_{sem})
=\sum_{j\in B_{sem}}p_{9,F,j}
-\sum_{j\in B_{sem}}p_{9,C,j}.
$$

This asks whether the same region showing any 8-to-9 growth is fine-enriched at block 9. Medium is reported as a descriptive guard; strict layer-9 coarse < medium < fine ordering is not required because E03's registered three-level result was trajectory-level rather than every-layer.

## D. Uncertainty, Controls, And Numerical Guards — CONFIRMED

- Use 2,000 paired bootstrap draws over the eight parent domains with replacement, seed `8120604`. Each draw recomputes split means, raw variances, within-layer normalization, bands, quartiles, and semantic hierarchy components. Layers are not independent replicates.
- Expression halves A/B repeat the full computation as sign guards and are not treated as independent samples.
- The 16 bandwise normalized changes receive a 95% simultaneous centered-bootstrap envelope using the maximum absolute deviation over all bands. Pointwise intervals are retained only in the detailed table.
- The four quartile specificity contrasts are evaluated jointly inside each bootstrap draw.
- Projection energy must match centered direct-state energy within relative error $5\times10^{-4}$ for both layers and every split.
- E03 block-9 semantic region contrasts recomputed here must match the frozen E03 layerwise table within $5\times10^{-6}$.
- All source files must match their frozen SHA-256 identities. No record, direction, parent, or failed draw is silently dropped.

## E. Exactly Two Required Figures — CONFIRMED

### Figure 1: Same-direction normalized rank curves and difference

- Upper panel: $4096p_{8j}$ and $4096p_{9j}$ on a log scale in the same Mean Response directions.
- Lower panel: $4096\Delta p_j$ with a zero line.
- A centered 129-direction arithmetic moving average is display-only; all statistics use unsmoothed directions.
- Shade `[0.50,0.75)` and label it as the independently frozen semantic region.
- Allowed conclusion: where normalized Attention-write variance is redistributed from block 8 to 9 in one coordinate.
- Cannot prove: raw growth, semantic novelty, or Router utility.

### Figure 2: Bandwise growth and semantic alignment

- Panel A: $\Delta Q_b$ in percentage points for all 16 bands with simultaneous 95% parent-bootstrap intervals.
- Panel B: $G_b$ in log2 units with pointwise 95% intervals, showing absolute band-energy change.
- Panel C: block-9 coarse, medium, and fine normalized shares across the same 16 bands; annotate $S_{9,F-C}(B_{sem})$ and its 95% interval.
- Bands F9--F12 are shaded consistently.
- Allowed conclusion: whether normalized growth, absolute growth, and prior fine-enrichment coincide in the same fixed region.
- Cannot prove: that a variance-growth band contains information unavailable at block 8 or improves routing.

## F. Execution And Reproducibility — CONFIRMED

1. Write unit tests for variance centering, normalization, band aggregation, bootstrap recomputation, simultaneous intervals, and hierarchy-region contrast; record the expected failing state.
2. Implement and pass tests.
3. Run a real-cache smoke on blocks 8 and 9; require basis and energy guards.
4. Run the full 512-record analysis, 2,000 parent bootstraps, expression halves, and semantic cross-check.
5. Render exactly two figures, inspect at full resolution, and record figure contracts and hashes.
6. Write `summary.md` and `detailed.md`; retain `AI_DRAFT_AWAITING_HUMAN_CONFIRMATION` until the researcher states the post-result judgment and boundary.

No new model inference, basis search, sliding-window search, probe, ablation, Router training, graph edit, publication, commit, or push is authorized.

## Cross-Block Consistency Audit

- Question ↔ coordinate: `PASS`; both layers use identical columns of one parameter-only basis.
- “More” ↔ metric: `PASS_WITH_TWO_MEANINGS`; normalized share and raw variance are reported separately.
- Region ↔ prior evidence: `PASS`; `[0.50,0.75)` was frozen before this transition analysis.
- Metric ↔ uncertainty: `PASS`; parent domains, not directions or layers, are resampled.
- Semantic bridge ↔ claim: `PASS`; it tests co-location, not conditional novelty or function.
- Figures ↔ estimators: `PASS`; direction curves are display-only and fixed bands carry inference.
- Authorization ↔ execution: `PASS`; the researcher explicitly requested the complete experiment and figures.

## Execution Receipt — APPEND ONLY

- Full execution completed on 2026-08-12 under run ID `a15-02-06-e04-20260812-layer8-to9`.
- All frozen source hashes, basis identity, cache identity, balance, projection-energy, bootstrap, and E03 semantic cross-check guards passed.
- Registered typed outcome: `no_aligned_growth`.
- Canonical result records: [summary.md](/Projects/from-attention-to-search/main/experiments/A15/15_02_layerwise_representation_spectral_atlas/A15_02_06_E04_layer8_to9_shared_basis_growth/summary.md) and [detailed.md](/Projects/from-attention-to-search/main/experiments/A15/15_02_layerwise_representation_spectral_atlas/A15_02_06_E04_layer8_to9_shared_basis_growth/detailed.md).
