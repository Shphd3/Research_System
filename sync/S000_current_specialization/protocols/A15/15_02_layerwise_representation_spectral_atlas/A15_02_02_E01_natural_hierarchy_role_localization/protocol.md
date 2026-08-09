---
experiment_id: A15_02_02_E01_natural_hierarchy_role_localization
anchor_id: 15_02_02_natural_hierarchy_role_localization
status: executed_completed
approved_by: user
approval_date: 2026-08-01
---

# Protocol: Natural Hierarchy Token Spectral Localization

## 0. Approval Snapshot

Purpose: determine whether coarse versus fine roles in natural hierarchy sentences occupy different covariance-ranked bands. Primary anchor: [A15_02_02](/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_02_layerwise_representation_spectral_atlas/subanchors/15_02_02_natural_hierarchy_role_localization_anchor.md). Role: frozen representation audit. Primary metric: within-sentence, same-intermediate-concept parent-minus-child band enrichment. Models: LB-80k MoE and local Qwen3-8B. Pass requires order-balanced, bootstrap-stable, rank-null-exceeding, directionally replicated evidence. Valid data with no such effect is Fail; failed span, basis, or model guards are Insufficient. This cannot establish Router utility or causal hierarchy formation. The user approved smoke and full execution on 2026-08-01.

## 1. Terminology / Definitions

Root, mid, and leaf are superordinate, intermediate, and subordinate concept spans. The same mid phrase occurs as a child of root and a parent of leaf. Band enrichment is the log ratio between an occurrence's normalized projected-energy share and the calibration covariance energy share.

## 2. Anchor Alignment

The test adjudicates whether covariance rank has a stable natural hierarchy-role meaning. The decisive falsifier is a null or order-reversing same-concept role effect.

## 3. Tested Hypothesis

Parent and child roles yield different head/middle/tail or fine-band enrichment after lexical and position controls.

## 4. Rival Explanations

Lexical identity, subword count, absolute position, syntax, vector norm, or arbitrary rank grouping explains apparent root/leaf differences.

## 5. Data / Model / Algorithm / Objective

Thirty-two disciplinary chains are rendered with twelve calibration and four disjoint evaluation templates, balanced between child-first and parent-first order. Each sentence has four character spans. Calibration content tokens fit one covariance per model-layer; evaluation spans never fit the basis. The current 12-layer width-768 LB-80k MoE contributes actual Gate inputs. Qwen3-8B contributes normalized post-attention, pre-MLP states at nine normalized depths.

## 6. Conditions, Seeds, And Checkpoints

Primary: mid-parent versus mid-child. Secondary: root versus leaf. Guards: order stratification, rank-shuffled null, exact offset alignment, and model-specific reporting.

## 7. Primary Metric

For band $B$, use the anchor-defined $r_B$ and paired $\Delta_B$. Bootstrap 32 chains 2,000 times. Use twelve equal-rank fine bands, H=F1, M=F2--F5, and T=F6--F12. Compare the real ordered bands with 256 randomized assignments of eigenvector ranks.

## 8. Secondary Metrics

Root-leaf contrast, raw energy share, stabilized whitened energy, top-decile role enrichment, and layerwise trajectories.

## 9. Known Good / Known Bad / Known Confusing Cases

Good: exact four-span mapping and identical token-id sequences for both mid occurrences. Bad: unpaired mathematics-versus-linear-algebra comparison. Confusing: causal position, handled by reversed templates.

## 10. Stage-Level Profiling Plan

S0 corpus/token audit; S1 single-sentence hook smoke; S2 covariance and split-half stability; S3 full paired projections; S4 bootstrap/null and visual audit.

## 11. Algorithm Specification

Map character spans with tokenizer offsets; extract states; fit calibration eigensystems; score held-out occurrences; form within-document pairs; compute rank-assignment nulls and chain bootstrap; preserve all manifests and tables.

## 12. Success / Failure / Insufficient Evidence

Apply the Approval Snapshot. Cross-model disagreement produces a model-conditioned verdict, not a universal Pass.

## 13. What This Cannot Claim

No semantic value, expert utility, training efficiency, causal representation mechanism, or dense-model Router claim follows from this audit.

## 14. Review Notes And Protocol Changes

The user explicitly authorized execution. The primary comparison was tightened to same-mid parent versus child to remove lexical confounding; root versus leaf remains secondary.

The Protocol already named occurrence order as a validity guard, but the first aggregation implementation checked only equal signs across the two orders. Before the final claim, the guard was made explicit: both order-specific effects must exceed the rank null, and the 95% chain-bootstrap interval for the child-first-minus-parent-first interaction must include zero. The earlier output is preserved as `role_effect_candidate`; the strict output is `role_effect_pass`. No effect direction or significance threshold was changed in response to the result.
