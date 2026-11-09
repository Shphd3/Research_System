# Additional common expert and hierarchy mixture: summary

[中文](summary_cn.md) · [Frozen protocol](protocol.md)

**All eight models and the hierarchy diagnostic are complete. Adding common while retaining both routed experts produces no stable low-feature benefit in either family. Both low- and high-frequency experts receive multilevel inputs dominated by h1 events.** Frequency rosters differ from input composition; these facts do not establish mixture as the cause of earlier performance differences.

## Purpose, hypothesis, and controls

The old T_H condition replaced one routed expert with a popular expert. This extension preserves both routed experts and adds a common expert called at every position. It tests whether an additional learned path improves prediction associated with low-frequency features. “Common” denotes shared invocation across positions, without presuming shared semantic content.

Compare ordinary MoE with MoE plus common, and frequency routing T_F with T_F plus common. Each family has paired seeds 11/22: eight models overall. Each family runs serially in its own one-H100 Reserved job. Every model uses one epoch, 168 updates, and 85,548 valid answer targets, with identical shared initialization and sample order within each pair. Qwen3-0.6B, the CrossCoder, final normalization, and vocabulary head remain frozen; residual experts and the ordinary MoE router are trainable.

The two original paths retain their weights: 0.5/0.5 for T_F and renormalized selected gates for ordinary MoE. Common is added with coefficient one, without replacement or division by three. Its output projection starts at zero, preserving the initial prediction. It adds 3,145,728 parameters. Parameter matching was explicitly waived, so additional capacity, active compute, and changed optimization remain rival explanations.

The hypothesis requires lower final DEV low-feature macro NLL in both paired seeds within a family. This metric first averages losses over each low feature’s active positions, then averages equally over features with DEV support. It differs from overall position-mean NLL and low-feature-union position-mean NLL. Two improving seeds constitute exploratory support for this setting; mixed directions do not support stable benefit. DEV has been inspected in earlier analyses.

## Additional-common training results

<!-- TRAINING_RESULTS_START -->
**All eight models completed. Neither family meets the predeclared requirement that both seeds improve low-feature macro NLL.** Each model reached 168 updates and 85,548 valid targets. Jobs `pt-7syyz16p` (MoE) and `pt-9bl40h38` (T_F) each used one separate H100 Reserved allocation; platform and pipeline receipts agree. Actual GPU pipelines took 277.6/266.8 seconds. Actual GPU smoke and next-update restore equality passed. All four current baseline DEV arrays exactly match their corresponding earlier seeds. This does not override the separate failed old T_H replay gate.

Two-seed means follow. Overall averages 10,340 positions, low-union averages 1,701 unique positions, and low-feature macro averages 838 DEV-supported B1 features; the remaining 856 of the original 1,694-feature pool are unsupported, not zero-loss observations.

| Model | Overall NLL | Low-feature macro NLL | Low-union NLL |
|---|---:|---:|---:|
| MoE baseline | 1.224985 | 1.054487 | 1.054318 |
| MoE plus_common | 1.226236 | 1.052392 | 1.055173 |
| T_F baseline | 1.226137 | 1.056320 | 1.061886 |
| T_F plus_common | 1.226807 | 1.057341 | 1.063671 |

Primary paired changes are plus_common minus baseline; negative is better:

| Family | Seed 11 delta | Seed 22 delta | Paired mean |
|---|---:|---:|---:|
| MoE | +0.001619 | -0.005810 | -0.002095 |
| T_F | +0.002998 | -0.000958 | +0.001020 |

Both families have opposing seed directions. All four overall-NLL differences are slightly positive. These are exposed-panel exploratory results, not evidence of universal harm or absence of benefit.

TRAIN overall mean improves from 1.032892 to 0.971833 for MoE and 0.951487 to 0.899016 for T_F. EVAL overall instead changes from 1.218746 to 1.219911 and 1.220257 to 1.220880. Global clipping is triggered in 42/28 baseline updates versus 166/160 common updates for MoE; T_F changes from 25/24 to 161/159, out of 168. Added common therefore actually changes routed-update scaling as well as capacity. Neither clipping nor overfitting has been isolated as the cause.

Common participates usefully in the jointly trained model: disabling it raises overall NLL by 0.0040–0.0068 in all four models. Low-feature macro also rises in every seed (MoE +0.000911/+0.006137; T_F +0.000311/+0.004737). This frozen inference effect is distinct from net improvement after retraining. For T_F, retaining only common decreases low-union NLL by 0.007553/0.010986 but raises overall NLL by 0.004516/0.003109. This demonstrates regional differences in the trained combination, not the performance of a separately trained common-only model.

The frozen TRAIN-companion strata give the following paired two-seed means over unique positions within each bin:

| Active selected companions | Events / positions / dialogues | MoE delta | T_F delta |
|---|---:|---:|---:|
| 0 | 120 / 115 / 49 | -0.004658 | -0.002179 |
| 1-2 | 358 / 342 / 82 | +0.001958 | +0.000863 |
| 3-4 | 510 / 475 / 93 | +0.000276 | +0.004332 |
| 5-8 | 1143 / 970 / 116 | +0.000781 | +0.000858 |

There is no monotonic pattern of larger common benefit with more active selected companions. Positions may appear in multiple bins, and events are dependent. Random-companion and per-seed/event/dialogue-weighted results remain available; these strata do not identify a mechanism.

[MoE analysis](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/shared_common_expert/20261022T103833Z/analysis/MoE/summary.json) · [T_F analysis](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/shared_common_expert/20261022T103833Z/analysis/T_F/summary.json) · [Training and telemetry audit](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/shared_common_expert/20261022T103833Z/analysis/telemetry.json) · [Actual saved asset registration](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/shared_common_expert/20261022T103833Z/provenance/registration/catalog_registration.json)
<!-- TRAINING_RESULTS_END -->

## Hierarchy definition and coverage

Reuse the hierarchy plotted on October 14 for the **same final 14-layer joint CrossCoder with 16,384 features**. No hierarchy was refitted. An edge from less frequent A to more frequent u requires P(u|A)≥0.8, P(A|u)≤0.5, at least twice as much support for u, and node/pair support thresholds. Edges were discovered, reviewed, and transitively reduced. Level h is the longest outgoing path to a sink; a qualified sink has h0. This is position in a statistical inclusion graph, not a transformer layer or a certified semantic abstraction level.

All 16,384 feature IDs align: 15,537 are qualified, non-isolated original graph nodes; 847 isolated nodes are retained separately; zero are unmapped. The edge-frequency constraint makes hierarchy and frequency partly coupled by construction. Original DCLM graph labels are carried to Tulu inputs; the original containment thresholds have not been revalidated for every edge on Tulu. [Identity and original-graph checks](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/hierarchy_expert_mixture/20261022T103957Z/input_manifest.json)

## Nominal rosters and actual inputs are different objects

Each feature counts once in its nominal roster. E0/E1 belong to lowest-frequency B1; E6/E7 belong to highest-frequency B4.

| Expert | Roster size | h0 | h1 | h2 | h3 | h4 | h5 | Isolated |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| E0 / B1 | 847 | 0 | 131 | 422 | 226 | 12 | 1 | 55 |
| E1 / B1 | 847 | 0 | 138 | 390 | 246 | 16 | 0 | 57 |
| E6 / B4 | 549 | 13 | 481 | 55 | 0 | 0 | 0 | 0 |
| E7 / B4 | 548 | 7 | 503 | 38 | 0 | 0 | 0 | 0 |

Both low- and high-frequency rosters span levels. E0 has 15.47% h1, 49.82% h2, and 26.68% h3 features; E6 has 87.61% h1. [All eight rosters and background](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/hierarchy_expert_mixture/20261022T103957Z/nominal_roster.csv)

For actual inputs, one activated feature at one position is one event. The denominator below is all feature events in the complete inputs received by that expert, using original TRAIN and T_F.

| Expert | Input positions | Feature events | h0 | h1 | h2 | h3+ | Isolated |
|---|---:|---:|---:|---:|---:|---:|---:|
| Full panel | 85,548 | 26,299,223 | 4.476% | 83.699% | 11.137% | 0.663% | 0.025% |
| E0 / B1 | 4,312 | 1,494,630 | 3.937% | 81.608% | 13.552% | 0.854% | 0.048% |
| E1 / B1 | 4,679 | 1,629,353 | 3.938% | 81.574% | 13.604% | 0.839% | 0.045% |
| E6 / B4 | 44,731 | 13,462,736 | 4.645% | 83.536% | 11.087% | 0.708% | 0.024% |
| E7 / B4 | 22,485 | 6,490,665 | 4.722% | 83.502% | 11.385% | 0.378% | 0.013% |

E0 has only 15.47% h1 features in its roster, but 81.61% of its actual input events are h1. Group scores select experts while each expert still reads the complete hidden state. Event share does not measure output amplitude, gradient, or prediction contribution. [All three panels, both routes, and eight experts](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/hierarchy_expert_mixture/20261022T103957Z/actual_input_composition.csv) · [Distribution figure](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/hierarchy_expert_mixture/20261022T103957Z/hierarchy_mixture.png)

At the position level, **every TRAIN, EVAL, and DEV position activates at least one h0, h1, and h2 feature**. Level coverage percentages therefore can sum beyond 100%. TRAIN h3 coverage for E0/E1/E6/E7 is 69.62%/68.82%/50.34%/38.27%, versus 50.07% in the full panel. Mixture is a universal input background here; its presence alone does not establish harmful interference. [Position counts](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/hierarchy_expert_mixture/20261022T103957Z/position_mixture.csv)

A concrete example is DEV row3730: a Terraform request to create an S3 bucket, with the model prefix reaching the AWS region value “us-east-1.” T_F selects low-frequency E0 and high-frequency E6. The same full input contains 14 h0, 209 h1, 41 h2, and 3 h3 active features; both experts receive it. This illustrates composition without naming individual features as Terraform functions. Selection used a fixed hash; full visible prefixes, feature IDs, and position indices are retained. [Traceable cases](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/hierarchy_expert_mixture/20261022T103957Z/text_cases.json)

## Mapping the advisor’s idea to routing: AI proposal

First identify natural-text feature combinations and their grouping, then ask which computation is shared within a combination. Equal h does not identify the same combination, and frequency or hierarchy labels alone do not determine a shared operator.

For a proposed **linear residual operator**, write total computation as \(W=C+R\), with extracted part C and remaining part R. Extract \(D=\sigma uv^\top\) from R and transfer it to the shared part:

\[
C'=C+D,\qquad R'=R-D,\qquad C'+R'=W.
\]

The transfer preserves the immediate output. If D is shared across a combination, its common path can compute D while downstream experts learn the remainder. Freezing extracted directions and restricting later updates to orthogonal directions are training choices that require testing; an immediate identity does not guarantee lossless future training. Making that shared path global additionally requires establishing its relevance across combinations.

One candidate mapping of the four steps is: flatten singular values only at initialization of the selected linear residual; define normalization and the threshold one; transfer the actual \(\sigma uv^\top\) upon crossing (do not clip its coefficient to one while claiming exact preservation); retain extracted output and learn group residuals under an explicitly chosen orthogonality constraint; repeat within subgroups. Initial scale and extraction rules remain unchosen and do not reproduce the senior student's undocumented loss.

At branching, initialize every downstream expert with the same \(R'\). If \(\sum_e g_e(x)=1\), then \(C'x+\sum_e g_e(x)R'x=Wx\). This preserves the immediate function, not future attainable loss or optimizer trajectories under new constraints.

The existing [15_11 synthetic experiment](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_11_gradient_consistent_hierarchical_routing/A15_11_E03H_counterfactual_utility_residual_tree_h100/summary.md) supplies a relevant precedent. With supplied groups, balanced sampling, and specified orthogonality, the correct grouping permits staged rank-one learning; the wrong grouping leaves a rank-two residual for a rank-one leaf. The exact lower bound additionally requires double orthogonality and exact ancestor orthogonality, as retained in the [original derivation](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_11_gradient_consistent_hierarchical_routing/A15_11_E03H_counterfactual_utility_residual_tree_h100/detailed.md). That toy did not establish a hierarchy advantage over a matched flat model and does not directly explain current natural-text behavior.

A complete SwiGLU expert is nonlinear and cannot be treated as a single matrix for SVD. Choosing a linear residual as the first extraction object is an **unexecuted AI proposal**; flattened-spectrum scale, extraction threshold, and orthogonality constraints still require specification. The current full-width common-expert experiment performs no rank-one extraction and is not a reproduction of the advisor’s algorithm.

## Current conclusion and evidence boundary

Established facts: rosters and full inputs span graph levels; adding common improves TRAIN fit but does not consistently improve low-feature DEV macro NLL across seeds. Similar level shares do not establish identical feature identities or computations. Update conflict, clipping effects, and causes of prior NLL differences remain unisolated.

**AI-proposed next question: within reproducible natural-text feature combinations, is there shared computation that can be retained while subsequent experts learn between-combination differences?** Cluster feature combinations at text positions, allowing overlapping atom membership. First test cross-dialogue reproducibility beyond tokens/source/templates, then inspect whether candidate extracted directions are shared across those combinations. Neither graph depth nor frequency alone substitutes for these checks.

The local diagnostic performed no model forward or training. Original-graph hashes, hierarchy recurrence, route/label alignment, and independent direct counts passed. Complete computation took 17.3 seconds with approximately 0.934 GiB peak RSS. [Diagnostic and checks](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/hierarchy_expert_mixture/20261022T103957Z/README_cn.md) · [Independent verification](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/hierarchy_expert_mixture/20261022T103957Z/verification.json)

