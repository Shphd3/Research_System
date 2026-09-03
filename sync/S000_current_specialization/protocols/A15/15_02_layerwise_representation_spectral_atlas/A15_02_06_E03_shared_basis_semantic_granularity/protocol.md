---
experiment_id: A15_02_06_E03_shared_basis_semantic_granularity
anchor_id: 15_02_06_mlp_parameter_geometry_and_semantic_location
status: RESULT_COMPLETE_AI_DRAFT_AWAITING_HUMAN_CONFIRMATION
canonical_language: en
approved: 2026-08-12
---

# Protocol: Semantic Granularity In The Mean-Response Common Parameter Basis

## 0. Approval And Amendment Snapshot

- The researcher explicitly authorized protocol construction, implementation, full execution, and final figures without another approval round on 2026-08-12, and then requested inclusion of medium-granularity data.
- This instruction replaces the E02 report's proposed held-out-coordinate next step for this bounded run. It does not edit the project graph or promote a Router claim.
- Blocks A--G are frozen before activation projection. Scientific-definition changes require an amendment; code repairs that preserve these blocks are allowed and recorded.
- Training, Router construction, graph editing, publication, commit, and push are outside scope.

## A. Question And Claim Boundary — CONFIRMED

### A1. Decision question

In one fixed, parameter-only mean-response coordinate, does the normalized spectrum of the isolated Attention write move to later ranks as semantic granularity changes from coarse to fine within the same balanced taxonomy data?

The primary contrast is fine minus coarse. A constructed medium level is a registered ordinal guard, not a replacement primary endpoint.

### A2. Typed outcomes

- `fine_later_than_coarse`: the 95% parent-bootstrap lower bound of the median block-1--35 fine-minus-coarse centroid is above zero and both expression halves are positive.
- `fine_not_later_than_coarse`: the corresponding upper bound is at or below zero and both expression halves are non-positive.
- `fine_coarse_unresolved`: neither decision is supported.
- `ordered_three_level_support`: in addition to `fine_later_than_coarse`, both medium-minus-coarse and fine-minus-medium lower bounds exceed zero, both expression halves preserve both signs, and the registered semantic pairing score exceeds the 95th percentile of balanced random pairings.
- `medium_descriptive_only`: the medium curve is displayed but any ordering or pairing-specificity guard fails.
- `insufficient_<guard>`: provenance, shape, basis, hierarchy, projection-energy, or resampling guards fail.

### A3. Cannot claim

No outcome proves that the Attention write contains information absent from the incoming residual, that finer semantics are intrinsically low rank, that a parameter rank has universal semantic identity, that MLP gain causes the location, or that routing by this coordinate improves expert utility. The medium level is constructed from a frozen grouping of the existing children and is not an independently collected label hierarchy.

## B. Data And Three-Level Semantic Object — CONFIRMED

### B1. Frozen data and activation site

Reuse the audited balanced run:

`/data/250010109/MoE_Router/experiments/20260809_a15_02_05_balanced_taxonomy_attention_write_atlas/runs/a15-02-05-e01-20260809T165500Z`

- 8 academic parents;
- 8 children per parent;
- 4 templates and 2 fact bundles per child;
- 512 records, balanced expression halves A/B;
- one readout at absolute position 57;
- cached `attention_write` is direct `self_attn.o_proj` output before residual addition, for blocks 1--36.

Frozen hashes: semantic dataset `c37329fad2e48d759b659483ed6705306eeb5c19f32c0e98a505901ed588ed88`; extraction manifest `6b9554702020e0aef2e51e6022937015c090414fad1c945afda1374f1da68f62`; model manifest `a27a04e41a76b84e1d2a515e726a0607bb313032d432615d37172f347ecc214b`.

### B2. Frozen medium grouping

Each parent has four named groups of two children. The mapping is frozen before projections:

| Parent | Medium group 1 | Medium group 2 | Medium group 3 | Medium group 4 |
| --- | --- | --- | --- | --- |
| mathematics | linear algebra + geometry | analysis + topology | number theory + combinatorics | probability + statistics |
| physics | mechanics + relativity | electromagnetism + optics | thermodynamics + condensed matter physics | quantum physics + particle physics |
| chemistry | organic + polymer | inorganic + nuclear | physical + theoretical chemistry | analytical + electrochemistry |
| biology | genetics + evolutionary biology | cell biology + molecular biology | microbiology + ecology | developmental biology + physiology |
| computer science | algorithms + programming languages | operating systems + networks | databases + cybersecurity | artificial intelligence + graphics |
| economics | microeconomics + labor | macroeconomics + international | econometrics + financial economics | public + development |
| medicine | cardiology + pulmonology | neurology + endocrinology | oncology + immunology | gastroenterology + nephrology |
| linguistics | phonetics + phonology | morphology + syntax | semantics + pragmatics | sociolinguistics + psycholinguistics |

These group names are not present in the prompts and do not select the parameter basis. Because the source cube did not contain a native medium field, interpretation requires the random-pairing specificity guard in Section F.

### B3. Hierarchical variance components

Let $a_{\ell p c r}\in\mathbb R^{4096}$ be one cached write and $\mu_{\ell pc}=\mathbb E_r a_{\ell pcr}$. For group $m(c)$, define

$$
\mu_{\ell pm}=\frac12\sum_{c:m(c)=m}\mu_{\ell pc},\quad
\mu_{\ell p}=\frac14\sum_m\mu_{\ell pm},\quad
\mu_\ell=\frac18\sum_p\mu_{\ell p}.
$$

The pure hierarchical deviations are

$$
d^C_{\ell p}=\mu_{\ell p}-\mu_\ell,\quad
d^M_{\ell pm}=\mu_{\ell pm}-\mu_{\ell p},\quad
d^F_{\ell pc}=\mu_{\ell pc}-\mu_{\ell p,m(c)}.
$$

Their population-weighted covariance components are $B^C_\ell=\mathbb E_p d^Cd^{C\top}$, $B^M_\ell=\mathbb E_{p,m}d^Md^{M\top}$, and $B^F_\ell=\mathbb E_{p,c}d^Fd^{F\top}$. The exact reconstruction $\mu_{pc}-\mu=d^C_p+d^M_{pm(c)}+d^F_{pc}$ is mandatory.

## C. Fixed Common Parameter Coordinate — CONFIRMED

Reuse the E02 `mean_response` basis without recomputation or semantic selection:

$$
K_\ell=W_{gate,\ell}^{\top}W_{gate,\ell}+W_{up,\ell}^{\top}W_{up,\ell},\qquad
\bar K=\frac1{36}\sum_{\ell=1}^{36}\frac{K_\ell}{\operatorname{tr}K_\ell},
$$

$$
\bar K=V\Lambda V^\top,\qquad \lambda_1\ge\cdots\ge\lambda_{4096}.
$$

Meaning: rank runs from directions with larger to smaller average trace-normalized MLP input-side parameter response. The frozen source is E02 `arrays/shared_bases.pt`; its byte hash is recorded at execution. Rank-consensus is excluded because this experiment asks one semantic question in the selected gain-sensitive coordinate; the prior basis disagreement remains a claim boundary.

## D. Projected Spectrum And Statistics — CONFIRMED

For $g\in\{C,M,F\}$ and basis vector $v_j$,

$$
e_{\ell gj}=v_j^\top B^g_\ell v_j,\qquad
p_{\ell gj}=\frac{e_{\ell gj}}{\sum_k e_{\ell gk}},\qquad
x_j=\frac{j-1/2}{4096}.
$$

The threshold-free primary location statistic is

$$
r_{\ell g}=\sum_jx_jp_{\ell gj},\qquad
\Delta r^{F-C}_\ell=r_{\ell F}-r_{\ell C}.
$$

The primary scalar endpoint is $T_{F-C}=\operatorname{median}_{\ell=1:35}\Delta r^{F-C}_\ell$. Block 36 is displayed but excluded as the registered boundary block. Medium guards use the analogous $T_{M-C}$ and $T_{F-M}$.

The auxiliary middle-late interval is frozen as normalized ranks $[0.50,0.75)$, exactly ranks 2049--3072 in one-based indexing (old 16-band names F9--F12). Its share is

$$
q_{\ell g}=\sum_{j:x_j\in[0.50,0.75)}p_{\ell gj}.
$$

It is auxiliary because its boundary is conventional. Registered sensitivity intervals are $[0.375,0.625)$ and $[0.625,0.875)$; they may qualify interpretation but cannot replace the centroid endpoint.

## E. Uncertainty And Controls — CONFIRMED

- Use 2,000 paired parent bootstraps with replacement, seed 8120603. Recompute the coarse grand mean inside every draw; do not average already-normalized parent curves. Layers are not independent replicates.
- Recompute the complete analysis in expression halves A and B as sign-stability guards, not extra independent samples.
- Use 256 deterministic balanced random pairings of the eight children inside every parent, seed 8120631. The real medium grouping passes specificity only if its global ordered score $\min(T_{M-C},T_{F-M})$ exceeds the random-pairing 95th percentile.
- Projection energy must equal direct hierarchical-deviation energy within relative error $5\times10^{-4}$ for every layer, level, and expression split.
- No failed layer, parent, child, or expression is dropped.

## F. Exactly Two Figure Contracts — CONFIRMED

### Figure 1: Mean-response common-basis reference, one panel

- Source: unchanged E02 fine-only normalized-energy array.
- Axes: normalized shared-basis rank, early/high response to late/low response; normalized variance density $4096p_{\ell j}$ on a log scale.
- Lines: blocks 1, 6, 12, 18, 24, 30, 35, 36; color shallow to deep.
- Display only: centered 129-rank arithmetic moving average.
- Allowed conclusion: the selected parameter coordinate produces layer-dependent fine-only profiles.
- Limitation: it is a reference plot, not the coarse/fine test and not absolute variance.

### Figure 2: Semantic-granularity result, one three-panel figure

- **A, full redistribution:** layer-by-rank heatmap of $4096(p_{\ell F}-p_{\ell C})$, aggregated only for display into 128 equal 32-rank bins; a symmetric color scale is used.
- **B, threshold-free location:** layerwise $\Delta r^{M-C}$, $\Delta r^{F-C}$, and $\Delta r^{F-M}$ with parent-bootstrap 95% intervals and a zero line.
- **C, requested middle-late share:** layerwise $q_M-q_C$, $q_F-q_C$, and $q_F-q_M$ for ranks $[0.50,0.75)$ with 95% intervals and a zero line.
- Block 36 is marked and excluded from global endpoints. Medium lines are solid only if the specificity guard passes; otherwise they are dashed and labeled descriptive.
- Allowed conclusion: relative spectral redistribution and location ordering in this frozen basis and taxonomy.
- Limitation: normalized shares do not show absolute signal strength, and medium depends on the frozen constructed grouping.

## G. Execution Contract — CONFIRMED

1. Write tests for hierarchical reconstruction, projection-energy conservation, centroid and middle-late definitions, parent-bootstrap recomputation, and balanced random pairings; record the expected failing state before implementation.
2. Implement the unchanged estimators and pass all tests.
3. Smoke on synthetic data and blocks 1/18/35 using the real cache and frozen basis.
4. Run all 36 blocks, 2,000 bootstraps, both expression halves, and 256 pairing controls.
5. Render exactly Figures 1 and 2, inspect them at full resolution, and record checksums and source arrays.
6. Write `summary.md` and `detailed.md`. The human must confirm or correct any knowledge update before it becomes a project-level conclusion.

## Cross-Block Audit

- Question to metric: `PASS`; the primary asks later spectral location and uses a centroid, not effective rank.
- Parameter basis to semantic data: `PASS`; the basis is fixed from parameters before semantic projection.
- Three levels to source data: `PASS_WITH_CONSTRUCTED_MEDIUM_BOUNDARY`; coarse and fine are native labels, medium is a frozen grouping with a specificity guard.
- Uncertainty to sampling unit: `PASS`; parents are resampled and layers are trajectories.
- Figures to estimators: `PASS`; heatmap is threshold-free, centroid is primary, and middle-late share is auxiliary.
- Authorization to execution: `PASS`; the researcher explicitly requested direct execution and medium inclusion.

## H. Execution State Record

- Final run: `a15-02-06-e03-20260812-granularity` on 2026-08-12.
- Frozen estimators, intervals, seeds, mapping, figures, and typed-outcome rules were not changed after projection access.
- Five unit tests, the three-layer real-cache smoke, all source-hash checks, the 36-layer run, 2,000 paired parent bootstraps, 256 random-pairing controls, numerical guards, and the full-resolution two-figure audit passed.
- Registered outcome: primary `fine_later_than_coarse`; medium guard `ordered_three_level_support`.
- The result wording remains `AI_DRAFT_AWAITING_HUMAN_CONFIRMATION`; it does not update the Anchor, graph, daily report, or project next decision without the researcher's post-result judgment.
