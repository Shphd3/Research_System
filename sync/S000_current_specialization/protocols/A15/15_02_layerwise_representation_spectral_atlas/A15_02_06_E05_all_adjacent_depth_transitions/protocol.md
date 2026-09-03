---
experiment_id: A15_02_06_E05_all_adjacent_depth_transitions
anchor_id: 15_02_06_mlp_parameter_geometry_and_semantic_location
status: EXECUTED_RESULTS_RECORDED
canonical_language: en
approved: 2026-08-12
---

# Protocol: All Adjacent-Layer Attention-Write Transitions In The Frozen Mean Response Basis

## 0. Approval Snapshot

- Purpose: determine whether the block-8-to-9 normalized result is local or part of a depth-dependent pattern.
- Role: robustness and depth-heterogeneity audit of the E04 variance proxy; it does not reopen variance growth as a definition of added information.
- Human authorization: the researcher explicitly requested more layer pairs from shallow to deep, eight separately displayed pairs, full execution, and significance analysis on 2026-08-12.
- Treatment/control: for each adjacent transition $\ell\to\ell+1$, treatment is block $\ell+1$ and control is block $\ell$.
- Held fixed: Qwen3-8B, 512 records, final-colon readout, post-`o_proj` pre-residual Attention write, Mean Response basis, direction order, centering, variance normalization, F9--F12 semantic region, parent bootstrap, and expression-half guards.
- Conditions: all 35 adjacent transitions are analyzed. Eight preselected transitions are display-only: `1→2`, `5→6`, `8→9`, `13→14`, `18→19`, `24→25`, `30→31`, and `35→36`.
- Primary depth metric: deep-stage mean $D_{sem}$ minus early-stage mean $D_{sem}$, with paired parent-bootstrap uncertainty.
- Fail for a later-depth shift: the registered deep-minus-early interval is non-positive or the linear depth slope does not have a positive lower bound.
- Insufficient: any source, balance, hook, basis, projection-energy, bootstrap, or artifact guard fails.
- Approved scope: implementation, unit tests, all 36 cached layers, 2,000 parent bootstraps, three final figures, and canonical result records.
- Cannot claim: residual-relative novelty, low rank, causal use, new knowledge, Router utility, or population-general layer laws.

## A. Question And Claim Boundary — CONFIRMED

For each $\ell=1,\ldots,35$, does the same-direction normalized Attention-write transition

$$
\Delta p_{\ell,j}=p_{\ell+1,j}-p_{\ell,j}
$$

place more variance share in the independently frozen fine-enriched region F9--F12, and does this transition metric differ systematically between shallow and deep model stages?

The strongest rival is that block 8→9 is one point in a non-monotonic depth profile, so its negative normalized change should not be generalized. A second rival is pure scale growth: raw variance may increase everywhere while normalized shares move in either direction.

## B. Data, Activation, And Coordinate — CONFIRMED

Use the unchanged balanced 512-record taxonomy cube: 8 parent domains, 8 children per parent, 4 templates, and 2 fact bundles. For record $x$ and block $\ell$,

$$
A_\ell(x)\in\mathbb R^{4096}
$$

is the direct Attention `o_proj` output before residual addition at absolute readout position 57.

The parameter-only Mean Response basis is frozen as

$$
\bar K=\frac1{36}\sum_{\ell=1}^{36}\frac{W_{gate,\ell}^{\top}W_{gate,\ell}+W_{up,\ell}^{\top}W_{up,\ell}}{\operatorname{tr}K_\ell}
=V\Lambda V^\top.
$$

All blocks use the identical columns and ordering of $V$. No activation or observed transition selects or changes the coordinate.

## C. Estimators And Fixed Regions — CONFIRMED

For split $s\in\{full,A,B\}$,

$$
z^{(s)}_{\ell x}=A_\ell(x)^\top V,
\qquad
e^{(s)}_{\ell j}=\operatorname{Var}_{x\in s}(z^{(s)}_{\ell xj}),
\qquad
p^{(s)}_{\ell j}=\frac{e^{(s)}_{\ell j}}{\sum_ke^{(s)}_{\ell k}}.
$$

Projection coefficients are not normalized record by record. Normalization occurs only after across-record variance estimation.

Use 16 equal bands $F_1,\ldots,F_{16}$, each containing 256 fixed directions. For transition $\ell\to\ell+1$:

$$
\Delta Q_{\ell b}=\sum_{j\in F_b}(p_{\ell+1,j}-p_{\ell,j}),
$$

$$
G_{\ell b}=\log_2\frac{\sum_{j\in F_b}e_{\ell+1,j}}{\sum_{j\in F_b}e_{\ell,j}}.
$$

The independently frozen fine-enriched region is

$$
B_{sem}=F_9\cup F_{10}\cup F_{11}\cup F_{12}=[0.50,0.75).
$$

Define

$$
D_{sem,\ell}=\sum_{b=9}^{12}\Delta Q_{\ell b},
\qquad
G_{sem,\ell}=\log_2\frac{E_{\ell+1}(B_{sem})}{E_\ell(B_{sem})}.
$$

## D. Depth Analysis And Multiplicity — CONFIRMED

All 35 adjacent transitions carry inference. The eight display pairs do not select the conclusion.

The fixed stages use transition start blocks:

- early: 1--12;
- middle: 13--24;
- deep: 25--35.

For each stage, average $D_{sem,\ell}$ with equal weight over its fixed transitions. The primary depth contrast is

$$
H_{D-E}=\overline D_{deep}-\overline D_{early}.
$$

Secondary contrasts are middle-minus-early and deep-minus-middle. Their intervals are simultaneous over these three stage contrasts. A linear slope of $D_{sem,\ell}$ against centered transition start block 1--35 is a secondary monotonicity guard.

Use 2,000 paired bootstrap draws over the eight parent domains, seed `8120605`. Each draw recomputes centering, direction variances, within-layer normalization, adjacent differences, stage means, contrasts, and slopes. Blocks and transitions are fixed architecture positions, not independent replicates.

The 35 transition-specific $D_{sem}$ intervals use one centered maximum-deviation simultaneous 95% envelope across all transitions. The 35 raw $G_{sem}$ intervals use a separate simultaneous envelope. Pointwise intervals remain in the detailed table.

Typed depth outcomes:

- `later_transitions_more_positive`: $H_{D-E}$ and the linear slope both have 95% lower bounds above zero.
- `later_transitions_more_negative`: both have 95% upper bounds below zero.
- `stage_dependent_nonmonotonic`: at least one simultaneous stage contrast excludes zero, but neither ordered outcome applies.
- `no_detectable_stage_difference`: all simultaneous stage contrasts include zero and the slope includes zero.
- `insufficient_<guard>`: a required guard fails.

These outcomes concern the normalized variance proxy only.

## E. Expression And Scale Guards — CONFIRMED

- Recompute every point estimate on expression halves A and B.
- Report $G_{sem,\ell}$ beside $D_{sem,\ell}$ so a relative-share change is not confused with absolute variance change.
- Reproduce E04's block-8-to-9 full/A/B point estimates within $5\times10^{-6}$.
- Projection energy must match centered direct-state energy within relative error $5\times10^{-4}$ for every block and split.
- No transition, parent draw, direction, or failed artifact is silently dropped.

## F. Required Figures — CONFIRMED

### Figure 1: Eight separately displayed adjacent transitions

Eight panels show the two normalized log curves $4096p_{\ell j}$ and $4096p_{\ell+1,j}$ in identical directions. A centered 129-rank moving average is display-only. Each panel prints $D_{sem,\ell}$ and its 35-transition simultaneous interval. F9--F12 is shaded.

### Figure 2: Complete 35-transition atlas

- heatmap: transition by fixed band, color $\Delta Q_{\ell b}$;
- trajectory: all 35 $D_{sem,\ell}$ with simultaneous intervals and stage boundaries;
- scale trajectory: all 35 $G_{sem,\ell}$ with simultaneous intervals.

### Figure 3: Depth-difference inference

- early/middle/deep stage means of $D_{sem}$ and $G_{sem}$;
- three simultaneous stage contrasts for $D_{sem}$;
- linear $D_{sem}$ depth slope and interval.

No figure may label a variance band as new information.

## G. Execution And Reproducibility — CONFIRMED

1. Unit-test centering, band aggregation, parent-bootstrap recomputation, simultaneous intervals, stage summaries, and slopes.
2. Hash-verify dataset, model, extraction manifest, all 36 Attention-write caches, Mean Response basis, and E04 reference table.
3. Project all layers, run numerical guards, compute all 35 transitions, and run 2,000 bootstraps.
4. Render and inspect exactly three full-resolution figures.
5. Write source tables, arrays, provenance, `summary.md`, and `detailed.md`.

Worker root:

`/data/250010109/MoE_Router/experiments/20260812_a15_02_06_all_adjacent_depth_transitions/`

Canonical root:

`Projects/from-attention-to-search/main/experiments/A15/15_02_layerwise_representation_spectral_atlas/A15_02_06_E05_all_adjacent_depth_transitions/`

No new model inference, basis search, task probe, Router run, graph edit, publication, commit, or push is authorized.

## Cross-Block Consistency Audit

- Same-direction comparison across depth: `PASS`.
- Eight display pairs versus all-pair inference: `PASS`; display selection cannot alter statistics.
- Relative versus absolute interpretation: `PASS`; $D_{sem}$ and $G_{sem}$ are separated.
- Depth significance without treating layers as replicates: `PASS`; parent domains are resampled and depth positions are fixed.
- Region independence: `PASS`; F9--F12 was frozen before E04 and E05.
- Claim boundary: `PASS`; robustness of a variance proxy only.
- Authorization and scope: `PASS`.

## Execution Receipt — APPEND ONLY

- Full execution completed on 2026-08-12 under run ID `a15-02-06-e05-20260812-all-adjacent`.
- All 36 layer caches, frozen source identities, basis identity, projection-energy guards, 2,000 bootstrap draws, and the E04 8→9 identity cross-check passed.
- Registered typed outcome: `stage_dependent_nonmonotonic`.
- A post-hoc ±1-stage-boundary sensitivity audit was added only to bound interpretation; it does not replace the registered equal-third result.
- Canonical result records: [summary.md](/Projects/from-attention-to-search/main/experiments/A15/15_02_layerwise_representation_spectral_atlas/A15_02_06_E05_all_adjacent_depth_transitions/summary.md) and [detailed.md](/Projects/from-attention-to-search/main/experiments/A15/15_02_layerwise_representation_spectral_atlas/A15_02_06_E05_all_adjacent_depth_transitions/detailed.md).
