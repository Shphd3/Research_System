---
experiment_id: A15_02_E05_pseudotaxonomy_specificity_control
anchor_id: 15_02_layerwise_representation_spectral_atlas
status: APPROVED_FOR_IMPLEMENTATION_SMOKE_FULL_LOCAL_ANALYSIS_AND_RESULT_RECORDS
canonical_language: en
created: 2026-08-07
---

# Protocol: Background-Normalized Variance Specificity Under Matched Pseudo-Taxonomies

## 0. Approval Snapshot

- **Document status:** `APPROVED_FOR_IMPLEMENTATION_SMOKE_FULL_LOCAL_ANALYSIS_AND_RESULT_RECORDS`
- **Approval status:** the researcher explicitly approved execution of the complete registered experiment on 2026-08-07 after reviewing the decision-critical design.
- **Block audit status:** A--G `CONFIRMED`.
- **Cross-block consistency:** `PASS`; the data randomization, frozen representation, primary metric, controls, decision rule, and execution boundary form one proxy-specificity audit.
- **Execution scope approved:** implementation, 64-draw smoke, 2,000-draw full local analysis, figures, and canonical result records. No Git, sync, publication, new model forward, or remote job is approved.
- **Purpose:** decide whether the block-25 and late-layer increase in background-normalized semantic variance depends on the registered taxonomy rather than appearing for arbitrary balanced groupings of the same texts.
- **Primary anchor:** [A15_02 coarse/fine semantic variance atlas](/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_02_layerwise_representation_spectral_atlas/15_02_layerwise_representation_spectral_atlas_anchor.md).
- **Anchor decision question:** where coarse/fine between-class variance appears with depth in the natural-background covariance spectrum.
- **Anchor physical prior tested:** a semantic hierarchy should produce a stronger depth-dependent normalized between-class signal than a matched grouping with no semantic parent structure.
- **Anchor core model term tested:** background-normalized band variance $q$.
- **Anchor falsifier:** the true taxonomy's late-minus-early $q$ shift does not exceed the matched pseudo-taxonomy null.
- **Experiment role:** operationalization/proxy audit and robustness check; no model learning.
- **Primary metric:** true-taxonomy excess of the late-minus-early median $\log_{10}q$ shift over 2,000 matched pseudo-taxonomies.
- **Claim boundary:** this can establish taxonomy specificity of the observed $q$ trajectory only. It cannot establish compositionality, information novelty, causal processing, Router utility, or training benefit.
- **Minimal setup:** reuse the frozen E04 post-`o_proj` semantic states and DCLM eigensystems; randomize only the assignment of 64 intact child nodes to eight pseudo parents.
- **Basic configuration:** 36 blocks; 16 equal-rank DCLM covariance bands; coarse and conditional-fine roles; design and confirmation expression splits; 2,000 pseudo-taxonomies; seed 1701.
- **Conditions to run:** registered taxonomy, matched pseudo-taxonomy null, exact true-metric replay guard, design/confirmation guard, and block-24-to-25 diagnostic.
- **Pass:** for both coarse and fine, the true late-minus-early statistic is positive and exceeds the pseudo-taxonomy q95 in both expression splits.
- **Fail:** all validity gates pass, but at least one role fails that joint specificity rule. The semantic-specific joint claim is then unsupported.
- **Insufficient:** cache, basis, split, replay, randomization, numerical, or draw-count guard fails.
- **Cannot claim:** $q$ is class accuracy or within-class compactness; the attention write is information-theoretically new; a spectral band should route tokens.
- **Approval decision:** approved for the execution scope recorded above.

## 1. Terminology / Definitions

| Term | Plain meaning | Concrete object / computation | Unit or formula | Why it matters | Cannot prove |
| --- | --- | --- | --- | --- | --- |
| Child node | One intact fine semantic concept | All eight expressions for one registered parent-child concept | 64 nodes total | Randomization must not break semantic replicates | Composition |
| Pseudo-taxonomy | A balanced hierarchy with no registered parent semantics | Randomly permute 64 child nodes and partition them into eight groups of eight | One draw | Separates semantic grouping from generic grouping | A linguistically meaningful alternative taxonomy |
| $q_{\ell,g,k}$ | Between-class variance relative to natural background variance | Mean projected between-class variance divided by the floor-stabilized DCLM covariance eigenvalue in band $k$ | Dimensionless | Removes the corresponding natural-background variance scale | Within-class compactness or accuracy |
| Late-minus-early shift $T_{q,g}$ | Whether normalized between-class signal is larger in late blocks | Median over blocks 25--35 and F1--F16 minus the corresponding median over blocks 1--12 | $\log_{10}$ units | Primary depth comparison | A sharp change specifically at block 25 |
| Block-25 jump $J_{25,g}$ | Local onset diagnostic | Median-band $\log_{10}q$ at block 25 minus block 24 | $\log_{10}$ units | Checks the visual transition in the current focus | A stable late-layer regime by itself |
| Taxonomy-specific excess | Whether the true hierarchy beats matched arbitrary groupings | True $T_q$ minus the pseudo-taxonomy median; q95 percentile used for the decision | $\log_{10}$ units and percentile | Directly separates the named rival | Functional usefulness |

## 2. Anchor Alignment

- **Decision question:** is the observed late-layer $q$ increase specific to the registered semantic hierarchy?
- **Physical prior tested:** semantic organization should affect between-class covariance beyond sample balance and arbitrary grouping.
- **Core model term tested:** $q$, not raw variance $b$, within-class discriminability $j$, or parameter-rank centroid $C$.
- **Falsifier:** a matched random grouping produces an equal or larger late-minus-early $q$ shift.
- **Claim boundary:** this is a post-hoc specificity audit of an existing frozen representation result.

## 3. Tested Hypothesis

Let $P_\mathrm{true}$ denote the registered eight-parent by eight-child taxonomy and $P_b$ the $b$-th matched pseudo-taxonomy. For role $g\in\{coarse,fine\}$ and expression split $s$,

$$
T_{q,g,s}(P)=
\operatorname{median}_{\ell\in 25{:}35,\,k\in 1{:}16}\log_{10}q_{\ell,g,k,s}(P)
-
\operatorname{median}_{\ell\in 1{:}12,\,k\in 1{:}16}\log_{10}q_{\ell,g,k,s}(P).
$$

The registered joint hypothesis is that $T_{q,g,s}(P_\mathrm{true})>0$ and exceeds the empirical q95 of $\{T_{q,g,s}(P_b)\}_{b=1}^{2000}$ for both roles and both expression splits.

## 4. Rival Explanations

1. **Generic late-layer amplification:** any balanced grouping of the same texts yields the same $q$ rise.
2. **Expression-template artifact:** the result appears only in the already displayed confirmation expressions.
3. **Broken-replicate null:** an apparently strong null is produced by randomizing individual sentences instead of intact semantic nodes.
4. **Basis or replay drift:** the reanalysis no longer reproduces the original E04 true-taxonomy $q$ table.
5. **Block-25 overreading:** the local block-24-to-25 jump is large, but the late window is not consistently distinct from the null.

## 5. Data Construction And Provenance

- Reuse the exact E04 model outputs, semantic row manifest, DCLM eigensystems, eigenvalue floor, and hashes.
- The semantic unit for randomization is one child node: a registered parent-child concept with all four templates and two fact bundles kept together.
- For each pseudo-taxonomy draw, generate one uniform random permutation of the 64 child nodes and partition the result into eight ordered pseudo parents of eight child nodes.
- The same pseudo-taxonomy draw is used across all layers, bands, roles, and expression splits.
- Design uses templates 1--2 and confirmation uses templates 3--4; both retain both fact bundles.
- Forbidden transformations: randomizing individual expressions, changing token rows, changing DCLM basis, choosing a seed after viewing results, filtering layers or bands, or redefining early/late windows.
- Known distribution limitation: all 64 child concepts come from one manually constructed academic taxonomy and one prompt family.

## 6. Learning Task And Permitted Supervision

There is no learning task, target prediction, model update, or hyperparameter selection. Registered labels are used only to compute the true taxonomy covariance. Pseudo labels are generated independently from the frozen representations and never alter model inputs.

## 7. Model / Architecture And Frozen Variants

- Model: frozen local Qwen3-8B exactly as in E04.
- Representation: all 36 direct outputs of `self_attn.o_proj` at the registered readout token, before residual addition.
- Background basis: the frozen E04 DCLM covariance eigensystem for each layer.
- No new forward pass is allowed unless a mandatory cache integrity guard fails; such a failure yields `insufficient_cache` rather than an automatic rerun.

## 8. Training Objective And Optimization

Not applicable. This is deterministic analysis of frozen caches. The only random process is pseudo-taxonomy generation from NumPy `PCG64` seed 1701.

## 9. Conditions, Seeds, And Checkpoints

| Item | Anchor clause tested | Model term / rival explanation | Why needed | Evidence role | Pass | Fail | Insufficient | Figure/table |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| True taxonomy replay | Metric validity | Basis/replay drift | Reproduce E04 $q$ exactly | Guard | Max relative error $\le10^{-6}$ | N/A | Error above tolerance | replay_guard.json |
| 2,000 matched pseudo-taxonomies | Taxonomy specificity | Generic grouping | Primary null | Primary | True statistic above q95 | True at/below q95 | Fewer than 2,000 valid draws | specificity_table.csv |
| Design/confirmation split | Expression robustness | Template artifact | Prevent one-split interpretation | Guard | Same registered verdict in both | Joint claim fails | Split rows incomplete | split_specificity.csv |
| Block-25 jump | Onset description | Block-25 overreading | Audit the current visual claim | Secondary | Report percentile and sign | No effect on primary verdict | Block 24/25 absent | block25_jump.csv |
| Fine/coarse roles | Granularity scope | Role-specific effect | Do not let one role stand for both | Primary | Both pass | Joint claim fails | Role computation invalid | role_summary.csv |

The full run uses exactly 2,000 pseudo-taxonomies and one registered seed, 1701. There are no checkpoints or model seeds because no model is trained.

## 10. Primary Metric

For each role and split, report the true $T_q$, pseudo-null median, pseudo-null q95, true-minus-null-median excess, and the empirical one-sided tail probability

$$
p_\mathrm{emp}=\frac{1+\sum_{b=1}^{2000}\mathbf 1[T_q(P_b)\ge T_q(P_\mathrm{true})]}{2001}.
$$

This metric decides whether the late-layer normalized variance is tied to the registered hierarchy rather than sample balance alone. A false positive would prematurely promote a generic depth effect as a semantic routing coordinate; this cost is higher than a false negative, so the joint rule requires both roles and both splits.

## 11. Secondary Metrics

- $J_{25,g,s}$ and its percentile under the pseudo-taxonomy null.
- Layerwise median $\log_{10}q$ curves for true and pseudo-null median/q05/q95.
- Layer-by-band true-minus-null-median heatmaps.
- Coarse/fine descriptive differences, with no additional pass rule.

## 12. Known Good / Known Bad / Known Confusing Cases

- **Known good:** the true-taxonomy replay reproduces the E04 confirmation $q$ table; each pseudo draw contains every child node exactly once and eight groups of eight.
- **Known bad:** independently shuffling sentence rows destroys the eight-expression child unit and is rejected.
- **Known confusing:** permuting only numeric child labels within the same true parent changes no covariance and is not a valid null.
- **Known confusing:** a large $J_{25}$ with an ordinary late-window $T_q$ supports a local spike, not a sustained semantic depth transition.

## 13. Stage-Level Profiling Plan

| Stage | Local question | Input evidence | Pass / fail / unclear rule | Debug artifact | Handoff |
| --- | --- | --- | --- | --- | --- |
| Contract | Are paths, hashes, shapes, and manifests exact? | E04 artifacts | All exact or stop insufficient | contract_validation.json | Smoke |
| Smoke | Does the null preserve child units and replay true $q$? | Layers 1, 25, 36; 64 draws | All guards pass | smoke_summary.json | Full |
| Full | Do 2,000 draws complete for all layers/splits/roles? | Frozen caches | Complete or insufficient | draw_manifest.json | Analysis |
| Analysis | Does true $T_q$ exceed the matched q95? | Full draw table | Apply frozen joint rule | verdict.json | Records |
| Visual audit | Do axes, roles, bands, split, and null intervals read correctly? | Final figures | Open and inspect all central figures | visualization_audit.json | Summary |

## 14. Algorithm Specification

**Input:** E04 projected semantic states or exact semantic states plus frozen E04 bases; semantic row manifest; DCLM eigenvalues.

**Parameters:** 2,000 pseudo-taxonomies; seed 1701; early blocks 1--12; late blocks 25--35; 16 bands; floor $10^{-6}\lambda_{\ell,1}$.

**Steps:**

1. Verify hashes, shapes, row ordering, layer coverage, and true-taxonomy replay.
2. Build the 64 intact child-node index sets.
3. Generate 2,000 balanced pseudo-parent assignments from uniform permutations.
4. For each layer, split, draw, and role, compute between-class variance in the frozen DCLM basis and aggregate $q$ by band.
5. Compute $T_q$, $J_{25}$, null percentiles, excess, and empirical tail probability.
6. Apply the joint decision rule without selecting layers, bands, roles, or draws.
7. Write tables, verdict, figure data, central figures, and artifact hashes.

**Outputs:** machine-readable configuration, pseudo assignments or deterministic seed manifest, full summary statistics, layerwise curves, heatmaps, verdict, and artifact manifest.

**Pass conditions:** all validity gates plus the registered joint specificity rule.

**Failure reasons:** `generic_or_unresolved_depth_shift`, `mixed_role_or_split`, or an `insufficient_<guard>` code.

## 15. Success / Failure / Insufficient Evidence

- **Pass — `taxonomy_specific_q_depth_shift`:** both roles exceed pseudo q95 with positive $T_q$ in both splits.
- **Fail — `generic_or_unresolved_q_depth_shift`:** validity gates pass but the joint rule fails. Report the exact failing role/split without rescuing the claim through a selected subset.
- **Insufficient:** any mandatory replay, cache, randomization, draw-count, numerical, or visual-audit guard fails.

## 16. What This Cannot Claim

This experiment cannot establish that deeper layers perform composition, that $z_\ell$ is information-theoretically new, that $q$ measures class accuracy, that a DCLM band is shared across layers, that an MLP uses the signal, or that routing on it improves data efficiency.

## 17. Block Confirmation Ledger And Review Notes

| Block | State | Decision requiring confirmation |
| --- | --- | --- |
| A Question and boundary | CONFIRMED | true taxonomy versus matched pseudo-taxonomy; semantic specificity only |
| B Data and provenance | CONFIRMED | intact 64 child nodes; randomize only eight-by-eight parent grouping; both expression splits |
| C Task and supervision | CONFIRMED | no learning; labels used only for covariance grouping |
| D Model and architecture | CONFIRMED | exact E04 post-`o_proj` caches and DCLM bases; no new forward |
| E Objective and optimization | CONFIRMED | deterministic analysis; PCG64 seed 1701 |
| F Comparison and evidence | CONFIRMED | 2,000 draws; late-minus-early $T_q$ primary; both roles/splits must exceed q95 |
| G Execution and reproducibility | CONFIRMED | local implementation, 64-draw smoke, 2,000-draw full analysis, result records; no Git/sync |

### Review note — 2026-08-07

The researcher requested that the exclusion-variable experiment begin and complete, and asked for a subsequent knowledge update. Under the repository experiment contract, exact Blocks B--G and execution scope must be confirmed after this complete draft is available. No implementation or run is authorized by this file until that confirmation is recorded and cross-block consistency passes.

### Confirmation and promotion note — 2026-08-07

The researcher explicitly instructed the assistant to begin execution, reuse the previous code where possible, complete the experiment, and return the result plus knowledge update. This confirms Blocks A--G and authorizes implementation, the registered 64-draw smoke, the registered 2,000-draw full local analysis, figures, and canonical result records. The cross-block audit passed: the intact-child randomization exposes the named arbitrary-grouping rival; labels are used only for grouping; E04 caches and eigensystems match the registered representation; the same pseudo-taxonomy draw is shared across layers, roles, and splits; the primary statistic and joint rule distinguish the registered hypothesis; and the resource/artifact boundary can execute every condition without a new model forward.
