# Detailed: A15_17_E04 Layer-8 Attention-Sidecar Representation Trajectory

Primary Anchor: [A15_17](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_17_three_model_sae_representation_trajectory/15_17_three_model_sae_representation_trajectory_anchor.md)  
Frozen Protocol and registered revision: [protocol.md](protocol.md), recovered S7-only contract plus A01--A03  
Summary: [summary.md](summary.md) / [summary_cn.md](summary_cn.md)  
Result eligibility: `ELIGIBLE` for bounded single-seed descriptive representation/accessibility, reconstruction, and local-gradient claims; `INELIGIBLE` for causal functional-use or cross-seed claims. Result judgment remains an AI draft pending researcher confirmation.

## 0. Quick Recap

Purpose: determine whether a layer-8 raw-Attention-output SAE sidecar produces a coherent Dense-relative representation trajectory through 10B tokens after removing the leading fit-only centered direction.

Hypothesis: a residual organization effect should survive B3 and have a consistent direction on both P and N.

Experiment logic: compare identical rows/checkpoints; separate raw versus B3; pair uncertainty by report row; inspect reconstruction and the local LM-versus-sidecar gradient to explain rather than substitute for the accessibility result.

Direct result: S7 learned a strong reconstruction objective and substantially redistributed variance, but B3 domain readability did not improve coherently across panels. At 10B the P probe decreased by 6.11 points with a paired interval excluding zero, while N changed by only +0.25 points with an interval spanning zero.

Eligibility: all six checkpoints and required guards passed; the final probe analysis restores the pre-existing raw-C reuse rule from immutable caches.

Verdict: `difference observed` in geometry and local objective pressure; `no coherent eligible improvement detected` in de-commoned cross-panel domain accessibility.

Claim boundary: no causal LM benefit/harm, native SAE-feature use, stable atom semantics, or generality beyond this trajectory.

## 1. Terminology / Definitions

| Term | Plain meaning | Concrete computation | Unit | Why it matters | Cannot prove |
| --- | --- | --- | --- | --- | --- |
| `M0` | Dense control | qualified prior cache at matched token checkpoints | model condition | reference trajectory | perfect counterfactual across seeds |
| `S7` | layer-8 Attention sidecar | SAE hooks block 7 output after `W_O`, before residual add | model condition | tested trajectory | sidecar causality by itself |
| native final representation | state shared by both models | final block post-`norm2` vector | 1024-vector | common comparison surface | functional use of SAE atoms |
| B3 | de-commoned coordinates | subtract fit mean, remove fit centered first singular direction | transformed 1024-vector | tests dependence on dominant direction | removal of every nuisance direction |
| Fisher ratio | class separation relative to within-class scatter | class-balanced between trace / within trace | ratio | geometry without fitting classifier | task utility |
| frozen probe | constrained linear readout | fit labels, tune C on raw, report accuracy; C reused for transforms | balanced accuracy | accessible label information | model-native use or causality |
| contribution share | normalized active-atom contribution | `z_j ||d_j||` normalized within token; N averaged across positions | share | sparse-code allocation | atom semantics |
| FVU | unexplained variance fraction | reconstruction squared error / centered input variance | ratio | reconstruction fidelity | semantic quality |
| support gradient | gradient on sampled SAE positions | local reconstruction gradient versus LM gradient at same node | norm ratio, cosine, degrees | direct local optimization pressure | accumulated causal effect |

## 2. Anchor Link And Decision Point

The Anchor asks whether SAE-related training produces a representation-accessibility trajectory that remains after common-direction removal. E04 adds one new topology: a sidecar whose reconstruction never enters the native forward path. The result informs whether this topology merits a later causal intervention; it does not itself authorize or settle such an intervention.

## 3. Protocol Freeze, Conformance, And Deviations

| Registered item | Expected | Actual | Status | Evidence | Eligibility impact |
| --- | --- | --- | --- | --- | --- |
| scope | S7 only | S7 only | PASS | task/completion records | none |
| checkpoints | 0/.5/1/3/5/10B | all 6 complete | PASS | `completed/*.json` | none |
| panels | P 360, N 1,200 | exact counts and IDs | PASS | completion records and row checks | none |
| hook | block 7 raw Attention output | hook layer `[7]` | PASS | completion records | none |
| execution | one 4x5090 Spot Smoke then full | `pt-4zcfwzwp`, `pt-ub07t6fc` | PASS | receipts and pod log | none |
| immutability | zero updates; state unchanged | zero optimizer updates; sampled hashes recorded | PASS | terminal/completion receipts | none |
| gradient guards | zero outside support; zero AuxK node gradient | exact zeros at every checkpoint | PASS | gradient JSONs | none |
| artifacts | all figures/tables | 16 PNG, 16 SVG, 13 source tables | PASS | curated E04 copies | none |
| probe transform rule | raw-selected C reused | first synthesis retuned; analysis_v2 reused raw C | REPAIRED | source hash and final tables | final v2 eligible; superseded v1 probe outputs ineligible |
| protocol path | isolated S7 record | E03 collided with concurrent multi-model workflow | RELOCATED | protocol A03 | no scientific impact; E04 owns S7 reading path |

Frozen Protocol revision: S7-only scope recorded before eligible computation; relocated without scientific changes.

Execution scope approved: local implementation/tests, one 4x5090 Spot Smoke, and after PASS one full run.

Retries and exclusions: `pt-hxlku819` and `pt-aafi4o85` are engineering failures only and contribute no scientific observation.

Post-hoc analyses: none used to select a condition or endpoint. The v2 probe repair applies the pre-existing method to every condition and checkpoint.

## 4. Actual Setup

Research question: does layer-8 sidecar training change accessible domain organization beyond a dominant common direction?

Data construction and provenance:

- P: frozen controlled synthetic panel, 360 rows, four coarse domains and finer families; 120/60/180 fit/tune/report; last valid token.
- N: frozen M2D2 academic panel, 1,200 rows, four parents and eight fine classes; 600/200/400 fit/tune/report; mean positions 0--255.
- P hash: `7aaf0ec96fdae2f2eecc4a011cd03539d6dc2268d3198203fcd6e3344781bf61`.
- N hash: `16eaced1320579b8aa736001a79e3babb699b862d3bc9245e7cd5d4af9929361`.

Model / architecture: eight transformer blocks, hidden size 1,024, Dense backbone 281,431,040 parameters. S7 adds a 61,471,024-parameter width-30,000 Top-32 SAE sidecar at block 7. The reconstruction does not replace or enter residual/MLP/logit computation.

Training objective, for interpretation only: next-token cross-entropy plus reconstruction loss with weight 1.0 plus SAE-only AuxK with coefficient 1/32. Reconstruction input is live; target and normalization denominator are detached. Analysis performs no training.

Training coordinates: seed 17, sequence length 2,048, microbatch 2 per device, four H100 devices during training, gradient accumulation 16, 50B target. E04 audits only 0--10B. Analysis ran on four RTX 5090 Spot devices; hardware choice does not alter frozen checkpoints.

Changed variable: the S7 training trajectory versus Dense.

Held fixed in analysis: tokenizer, panel rows, splits, token checkpoints, anatomical final state, transforms, label definitions, report units, and bootstrap pairing.

Known setup limitations: one trajectory per condition; Dense and S7 are not replicated experimental units; training loss is not held-out validation; P is a templated panel; N is development replication rather than untouched confirmation.

## 5. Metrics And Decision Rules

Primary reading: paired S7-minus-M0 coarse Fisher and balanced-accuracy trajectories in raw and B3 coordinates, separately for P and N. A coherent improvement requires consistent direction across checkpoints/panels and survival after B3. There is no registered magnitude threshold.

Secondary readings: coarse/fine hierarchy, covariance spectrum, sparse contribution probes, fixed-atom contributions, FVU and feature coverage, local gradient norm/cosine/angle, and token-aligned training loss.

Uncertainty: 5,000 stratum-preserving paired bootstrap resamples of report rows. Rows are the independence unit for displayed intervals; checkpoints are correlated trajectory points, not independent replications.

## 6. Evidence Lineage

| Claim or decision | Protocol criterion | Raw artifact | Computation | Aggregation / uncertainty | Observed value | Eligibility | Verdict | Limitation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| no coherent B3 probe improvement | paired B3 trajectory on both panels | matched M0/S7 P/N caches | fixed raw-selected C, report prediction pairing | 5,000 row bootstrap draws | 10B P `-0.0611 [-0.1000,-0.0278]`; N `+0.0025 [-0.0275,+0.0325]` | ELIGIBLE | non-supporting | one seed |
| no decisive 10B B3 Fisher improvement | paired B3 Fisher | same caches | class-balanced trace ratio | paired bootstrap | P `+0.1001 [-0.1666,+0.1422]`; N `+0.0040 [-0.0008,+0.0090]` | ELIGIBLE | unresolved | unstable ratio on P |
| local auxiliary pressure is strong and orthogonal | same node/support | gradient JSONs | reconstruction/LM norm, cosine, angle | mean of four frozen fit batches | 10B support `1.4608`, `0.00069`, `89.96°` | ELIGIBLE | difference observed | local derivative, not long-run cause |
| reconstruction improves | report recon/input energy | S7 caches | centered FVU | report rows | 10B P `0.1799`, N `0.1358` | ELIGIBLE | reconstruction learned | no semantic inference |
| variance redistributed on P | B3 covariance summaries | final-state caches | eigenvalue shares and participation ratio | report covariance | 10B B3 P top1 M0 `0.5820`, S7 `0.1332`; PR `2.79` vs `18.24` | ELIGIBLE | geometry changed | weak analogue on N |
| training LM loss is slightly higher | token-aligned loss curves | two metrics JSONL files | 200-update trailing mean, 25M grid | descriptive trajectory | +10.59 millinats near 10B | BOUNDED | cost signal observed | not held-out, one run |
| sparse code contains domain signal | sparse contributions | S7 z indices/values and decoder norms | frozen contribution-share probe | report balanced accuracy | 10B coarse P `0.8889`, N `0.7075` | BOUNDED | readable code | no native use or stable atom meaning |

## 7. Main Results

### Eligible decision evidence

The main result is negative with respect to a stable accessibility improvement. P and N do not agree after B3, and the P trajectory changes sign across time. At 3B and 10B, P B3 probe accuracy is lower for S7; at 5B it is slightly higher but unresolved. N B3 differences remain only a few points or less and are generally unresolved.

At 10B, the raw P probe is saturated for both models (M0 98.89%, S7 98.33%), hiding a large geometry difference. B3 exposes that S7 is lower (93.33%) than M0 (99.44%). N stays close in both raw and B3 coordinates. This is why removing the first common direction changes the scientific reading: raw separability alone would overstate stability.

### Bounded evidence

The sidecar's reconstruction becomes substantially better by 10B, but it is non-monotone: P FVU is worse than a centered-mean baseline at 0.5B (`1.176`) before falling to `0.228` at 1B, rising to `0.574` at 3B, and ending at `0.180`. N follows the same broad improvement with smaller excursions. Feature coverage collapses from initialization and remains sparse; Top-32 makes the mean active count exactly 32 by construction.

The token-aligned training loss difference peaks early and shrinks. It remains positive near 10B, consistent with but not proving a tradeoff between reconstruction pressure and next-token optimization.

### Descriptive evidence

The fixed-atom heatmap includes 0B and uses one retrospectively selected set across 0.5--10B fit rows. Atom contribution patterns rotate substantially over checkpoints. PCA, UMAP, and t-SNE are jointly fitted descriptive projections after B3; none is used for the verdict.

### Failed and ineligible evidence

The overbroad suspended job and missing-tokenizer Smoke contain no result. The first synthesis's transform-specific retuning is superseded; its probe values are not used. All other original full-run values remain eligible because they do not depend on probe C.

## 8. Visualization Results

### Paired geometry and readability

![Paired geometry and readability](figures/03_paired_geometry_and_readability.png)

Purpose: determine whether S7-minus-M0 differences have a coherent sign after common-direction removal.  
Source: [paired_fisher_differences.csv](tables/paired_fisher_differences.csv), [paired_probe_differences.csv](tables/paired_probe_differences.csv).  
How to read: purple intervals are paired Fisher differences; orange values are paired probe accuracy differences; zero is no difference.  
Observed result: P B3 changes sign and ends with a probe decrease; N remains near zero.  
Take-home: no coherent cross-panel residual accessibility benefit.  
Cannot prove: no representation difference of any kind.

### Local gradient geometry

![Support gradient geometry](figures/06_gradient_magnitude_ratio_angle_support.png)

Purpose: verify that the sidecar exerts a non-negligible training force at its hook and measure its direction relative to LM loss.  
Source: [gradient_metrics.csv](tables/gradient_metrics.csv).  
How to read: norm ratio compares reconstruction to LM gradient; 90 degrees is orthogonal.  
Observed result: ratio grows to 1.46 at 10B while angle remains 89.96 degrees.  
Take-home: strong distinct local objective pressure.  
Cannot prove: that this pressure caused any endpoint difference.

### Reconstruction and dictionary health

![Reconstruction health](figures/09_reconstruction_fvu_trajectory.png)

Purpose: test whether the SAE actually learns the hooked input and whether dictionary use collapses.  
Source: [reconstruction_health.csv](tables/reconstruction_health.csv).  
Observed result: FVU ends below 0.2 on both panels; coverage is low and non-monotone; exactly 32 atoms are active by design.  
Take-home: reconstruction learned, but a small subset of the 30,000-atom dictionary dominates each panel.  
Cannot prove: semantic quality or native use.

### Token-aligned loss

![Token-aligned loss](figures/10_training_loss.png)

Purpose: show whether the sidecar trajectory pays an observable next-token training-loss cost.  
Source: [training_loss_trajectory.csv](tables/training_loss_trajectory.csv), [training_loss_delta_25m.csv](tables/training_loss_delta_25m.csv).  
Observed result: both losses descend; S7 remains about 10.59 millinats higher near 10B after a larger early transient.  
Take-home: a small training-loss cost signal is present.  
Cannot prove: held-out generalization harm.

### Fixed atom contributions

![Fixed atom contribution trajectory](figures/04_fixed_feature_activation_trajectory.png)

Purpose: show how the same selected atom IDs contribute across all checkpoints, including 0B.  
Source: [fixed_feature_selection.csv](tables/fixed_feature_selection.csv), [fixed_feature_contribution_trajectory.csv](tables/fixed_feature_contribution_trajectory.csv).  
Observed result: active contribution mass migrates across atom IDs and domains over time.  
Take-home: sparse codes are readable but atom identity is not stable enough here for semantic naming.  
Cannot prove: atom-level causal function.

### Complete figure inventory

| Figure | Evidence role | Decision status |
| --- | --- | --- |
| [01 topology](figures/01_hypothesis_and_gradient_paths.png) | forward/gradient-path explanation | setup only |
| [02 readability](figures/02_domain_readability_trajectories.png) | absolute raw/B3 probe trajectories | supporting |
| [03 paired differences](figures/03_paired_geometry_and_readability.png) | primary paired comparison | decision-bearing |
| [04 fixed atoms](figures/04_fixed_feature_activation_trajectory.png) | contribution evolution including 0B | descriptive |
| [05 variance distribution](figures/05_variance_distribution_trajectories.png) | top shares/effective dimension | supporting |
| [06 full-node gradients](figures/06_gradient_magnitude_ratio_angle_full.png) | whole-node pressure | supporting |
| [06 support gradients](figures/06_gradient_magnitude_ratio_angle_support.png) | non-diluted local pressure | decision-relevant mechanism clue |
| [07 raw Fisher](figures/07_fisher_absolute_raw.png) | absolute raw geometry | supporting |
| [07 B3 Fisher](figures/07_fisher_absolute_b3.png) | absolute de-commoned geometry | supporting |
| [09 reconstruction](figures/09_reconstruction_fvu_trajectory.png) | SAE health | decision-relevant guard |
| [10 loss](figures/10_training_loss.png) | token-aligned training dynamics | bounded outcome |
| [11 PCA](figures/11_pca_joint.png) | joint 2D linear projection | descriptive only |
| [12 UMAP](figures/12_umap_joint.png) | joint nonlinear projection | descriptive only |
| [13 t-SNE](figures/13_tsne_joint.png) | joint nonlinear projection | descriptive only |
| [14 spectrum](figures/14_variance_spectrum_10b.png) | endpoint covariance spectrum | supporting |
| [15 internal heatmaps](figures/15_s7_internal_variance_heatmaps.png) | Attention/reconstruction variance match | supporting |

## 9. Stage Evidence And Failure Decomposition

| Stage | Evidence | Status | Failure reason | What this rules out | What remains live |
| --- | --- | --- | --- | --- | --- |
| local qualification | 5 tests, direct 0B load | PASS | none | schema/hook mismatch | scientific effect |
| corrected Smoke | `pt-4zcfwzwp` | PASS | none | immediate runtime/gradient guard failure | full-matrix completion |
| full collection | 6 checkpoint receipts | PASS | none | missing checkpoint/row/hook | analysis correctness |
| original synthesis | 16 figures, 11 tables | PASS with probe-method deviation | transform-specific C retuning | non-probe computations valid | probe comparability |
| fixed-probe synthesis | 96 final, 288 hierarchy, 48 paired rows | PASS | none | probe retuning confound | single-seed uncertainty |
| source-table completion | atom and loss trajectory exports | PASS | none | missing visual lineage | causal interpretation |

Falsified implementation failure: yes; eligible job completed and passed all guards.

Falsified “sidecar did nothing” explanation: yes; reconstruction, gradients, variance, and loss all differ measurably.

Not falsified: geometry-only regularization, template sensitivity, single-trajectory noise, and lack of model-native feature use.

## 10. Full Experiment Record

1. Question: does the layer-8 Attention sidecar produce a coherent residual-domain organization trajectory?
2. Setup: M0 versus S7, same final anatomical state, same P/N rows, same 0--10B endpoints, no updates during analysis.
3. Training data: the frozen DCLM pair view used by the existing checkpoints; no training data were read to fit representation probes.
4. Testing/confirmation data: P report 180 rows and N report 400 rows; transforms/probes use only fit/tune where registered.
5. Result: full job `pt-ub07t6fc` completed 6/6 points; final v2 tables and all figures are curated here.
6. Insight: sidecar pressure reshapes variance and learns reconstruction but does not establish coherent B3 readability improvement. The next scientific uncertainty is causal attribution of this pressure, not another descriptive projection.

## 11. Interpretation And Potential Causes

### Directly supported mechanism links

1. The reconstruction never enters the forward path, so any backbone change must arise through training gradients rather than inference-time replacement.
2. The support-only reconstruction gradient is non-negligible and becomes larger than the LM gradient at 10B.
3. The two gradients remain nearly orthogonal at every audited checkpoint.
4. Reconstruction quality improves, final covariance organization changes, and training LM loss stays slightly higher.

Together these observations support a bounded explanation: the sidecar imposes an additional optimization pressure that is different from the instantaneous next-token direction and preferentially improves reconstructibility/geometry.

### AI inference

The nearly orthogonal pressure may spend update capacity on directions that preserve or spread Attention-output information without making the registered domain labels more linearly accessible. This explains the coexistence of lower FVU, higher effective dimension on P, a small LM-loss cost, and no stable B3 probe gain. It remains an inference because the experiment does not intervene on gradient flow.

### Strongest live rivals

- P-specific template structure and M0's unusual 10B variance concentration can produce a large P geometry contrast without a general semantic effect.
- Single-seed trajectory noise can produce endpoint differences and sign changes.
- The registered domain labels may be orthogonal to information that the SAE preserves; no domain benefit does not imply no useful information.
- Sparse feature selection is retrospective on fit rows, so atom heatmaps cannot establish prospective stable feature identities.

## 12. Claim Boundary

Can claim:

- S7 learned a substantially lower-FVU reconstruction by 10B.
- Its local reconstruction gradient is strong and nearly orthogonal to the LM gradient.
- It substantially redistributes P-panel variance and modestly changes N-panel geometry.
- It does not show coherent cross-panel B3 domain-readability improvement through 10B.

Cannot claim:

- causal LM improvement or harm;
- held-out generalization change;
- model-native use of SAE atoms;
- stable atom semantics or functional specialization;
- sidecar causality isolated from training stochasticity;
- generality across seeds, layers, data panels, or model scales.

## 13. Next Decision

Decision: `AI PROPOSAL` — run no further descriptive atlas by default. If causal attribution is required, first formalize a matched gradient-blocked sidecar control with multiple seeds.

Completion criterion: token-matched held-out LM loss and B3 accessibility with seed-level uncertainty.

Stop/redirect: if the gradient-blocked control retains the same outcome, reject backbone reconstruction-gradient pressure as the main explanation and examine panel/statistical effects.

Resume action: researcher confirms or rejects this proposal; a new Protocol and execution approval are required.

## 14. Artifact Manifest

| Artifact | Purpose | Producer / revision | Source inputs | Hash / identity | Complete | Claim-eligible | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [protocol.md](protocol.md) | recovered frozen contract | E04 relocation | pre-result S7 instruction | local file | yes | yes | collision-safe |
| `full_5090_4spot_v1/caches` | raw representations and sparse states | full job | 6 S7 checkpoints, P/N | per-checkpoint hashes in completion JSON | yes | yes | remains in execution workspace |
| `full_5090_4spot_v1/gradients` | local gradient summaries | full job | four fit batches/checkpoint | per-checkpoint hashes | yes | yes | no full gradient tensors |
| [final representation table](tables/final_representation_metrics.csv) | final-state geometry/probes | analysis_v2 | M0/S7 caches | `da1896...a22dd` | yes | yes | corrected fixed-C rule |
| [paired Fisher table](tables/paired_fisher_differences.csv) | geometry uncertainty | full synthesis | matched report rows | `a4c190...fe5e56` | yes | yes | 5,000 draws |
| [paired probe table](tables/paired_probe_differences.csv) | readability uncertainty | analysis_v2 | matched predictions | `46788c...301fb` | yes | yes | fixed-C rule |
| [gradient table](tables/gradient_metrics.csv) | local objective geometry | full synthesis | gradient JSONs | `f59c9f...c6be98` | yes | yes | full/support separated |
| [reconstruction table](tables/reconstruction_health.csv) | FVU/coverage | full synthesis | S7 caches | `803313...491ec` | yes | yes | semantics excluded |
| [atom trajectory](tables/fixed_feature_contribution_trajectory.csv) | source for figure 04 | source-table export | fixed selection + caches | `2614aa...b6c05` | yes | bounded | retrospective fit selection |
| [loss trajectory](tables/training_loss_trajectory.csv) | source for figure 10 | source-table export | two metrics JSONL | `8674e2...e0d0e` | yes | bounded | training only |
| [results overview](results_overview.json) | machine-readable map | analysis_v2 | final tables/figures | `04cda2...a3cb` | yes | yes | 16 figures, 13 tables |
| [execution receipt](execution_receipt.md) | operations provenance | curated record | ACP receipts/logs | job `pt-ub07t6fc` | yes | operations only | platform SUCCEEDED |

## 15. Links

- anchor: [A15_17](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_17_three_model_sae_representation_trajectory/15_17_three_model_sae_representation_trajectory_anchor.md)
- protocol: [protocol.md](protocol.md)
- summary: [summary.md](summary.md) / [summary_cn.md](summary_cn.md)
- code workspace: `/data/250010109/MoE_Router/experiments/20260917_sidecar_representation_gradient_audit`
- training workspace: `/data/250010109/MoE_Router/experiments/20260916_attention_output_sidecar_last_50b`
- raw run: `/data/250010109/MoE_Router/experiments/20260917_sidecar_representation_gradient_audit/runs/full_5090_4spot_v1`
- curated analysis: `/data/250010109/MoE_Router/experiments/20260917_sidecar_representation_gradient_audit/runs/full_5090_4spot_analysis_v2`
- job IDs: Smoke `pt-4zcfwzwp`; full `pt-ub07t6fc`
