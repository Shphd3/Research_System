# Summary: A15_17_01_E01 — same-panel SAE atom reuse

Primary Anchor: [shared atom reuse](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_17_three_model_sae_representation_trajectory/subanchors/15_17_01_sae_shared_direction_reuse_anchor.md).  
Frozen Protocol: [E01-full-v1-A2](protocol.md).  
Detailed record: [complete evidence ledger](detailed.md).  
Execution: COMPLETE; measurement: ELIGIBLE for the registered existing-panel test.  
Registered branch: PASS — necessary condition only. Human mechanism judgment: AWAITING_RESEARCHER.  
Verified: 2026-09-22T09:08:48.084508+00:00. No new scientific judgment or subsequent experiment is approved by this record.


## 1. Purpose

Test whether S7's lower native effective dimension accompanies greater cross-example reuse of the same SAE atoms, a necessary prediction of the shared-support explanation—not a test of improved domain semantics.

## 2. Hypothesis

H1 predicts higher cross-example similarity of native atom-selection frequency profiles in S7 than SALL, together with lower native effective dimension on identical examples. Global usage concentration is secondary. H2 permits low dimension through aligned decoder columns or low-dimensional coefficient covariance; it can coexist with H1. A positive H1 prediction cannot exclude H2 or identify causal contributions.

## 3. Analysis Method

1. **Matched measurement, not matched training treatment.** Frozen exact-21B reweighted last-layer-sidecar S7 versus original all-eight-layer-sidecar SALL; identical 192 N8 examples ×256 body tokens, layer 8, 30,000 atoms, K=32. The native write is post-output-projection and pre-residual, not SAE reconstruction. Four extraction workers qualified; no labels, training or exclusions. SALL is not a no-SAE Dense baseline; training histories/topologies differ.
2. **Within-model reuse.** For each example, \(u_{ij}=\sum_t1[j\in S_{it}]/(256\times32)\). \(R\) is the mean cosine over distinct example pairs. Primary \(\Delta R=R_{S7}-R_{SALL}\) uses 2,000 paired record-ID bootstrap draws, seed 20260922, percentile 95% interval. Pairs/tokens are not independent replicates. IDs are never aligned across models; frequency similarity is not semantic similarity.
3. **Aligned geometry and decision.** Center covariance of the same-pass token-mean native writes: \(d_{eff}=(\mathrm{tr}\Sigma)^2/\mathrm{tr}(\Sigma^2)\) counts equivalent variance-bearing directions, not concepts. Eligible measurement + lower S7 dimension + positive CI lower bound passes the necessary condition; with lower dimension, a nonpositive upper bound fails; otherwise insufficient. An independent CPU recomputation reproduced reuse, dimension and the 2,000-draw bootstrap interval and verified 22 artifact hashes without changing the rule.

## 4. Conclusion

### Direct result: registered necessary-condition PASS

| Quantity | SALL | S7 |
|---|---:|---:|
| Mean usage-profile cosine R | 0.512117 | 0.597905 |
| Same-panel native effective dimension | 17.160447 | 14.486918 |

**Delta R = +0.085788, 95% CI [0.072687, 0.098599].** The interval is wholly positive and S7 dimension is lower: the registered necessary condition passes. Sources: [primary](tables/primary.csv), [conditions](tables/conditions.csv), [independent audit](/data/250010109/MoE_Router/experiments/20260922_sae_shared_direction_reuse_audit/runs/full_4x5090_20260922T074451Z/independent_audit.json). Dimension ordering is a registered point-estimate guard, not a significant dimension-difference claim; no dimension CI was registered. These are two frozen conditions, not a within-model temporal decline.

![Primary interval and concentration](figures/reuse_necessary_condition.png)

How to read: left is the decisive interval entirely right of zero; center shows globally sorted atom selection-frequency mass, not activation/reconstruction energy; right shows sorted centered native variance, not semantic content. Earlier accumulation indicates concentration. Ranks are independently sorted, not aligned semantic directions; secondary curves have no uncertainty bands and cannot replace the primary decision. Source result.json and concentration_curves.csv hashes are preserved in the figure manifests.

### Atom-count disparity and extraction qualification

Distinct selected atoms across the full panel: SALL **17,060**, S7 **142**; effective usage counts are **229.34**, **73.99**, respectively. Both still select exactly 32 per token: global coverage is not token sparsity. The large SALL tail explains why distinct and effective counts differ so much; neither counts semantic concepts or determines native dimension. [Source](tables/conditions.csv).

Native Top32 and same-forward top128-prefix32 supports matched on every token in both full conditions (zero mismatches), despite boundary ties. Thus the potential extraction discrepancy was not observed and cannot explain this panel's count difference. This is a same-forward operation check, not universal historical-platform equivalence. [Source](/data/250010109/MoE_Router/experiments/20260922_sae_shared_direction_reuse_audit/runs/full_4x5090_20260922T074451Z/analysis/result.json).

### Intuition versus evidence and boundary

![Hypothetical chain versus observed association](figures/intuition_vs_observation.png)

How to read: the left causal chain is hypothetical; the right reports only higher reuse and lower dimension together. The arrow 17.16→14.49 denotes SALL-to-S7 contrast, not training evolution. Passing the necessary prediction does not prove the left arrows.

Can claim: this fixed panel and these exact checkpoints exhibit greater S7 model-local selection-profile similarity and lower native-mean effective dimension under the registered rule. Cannot claim: reuse causes or primarily explains low dimension; coefficient strength alone caused the difference; improved semantic separation, model utility or task performance; optimal K=32; representational collapse or a training trajectory. Geometry, coefficient covariance, reconstruction residual and cross-covariance contributions remain unmeasured.

This inherited, historically stratified panel includes smoke-development-exposed records, not untouched confirmation. Record bootstrap does not establish article-level independence or training-seed uncertainty.

### Next step analysis — AI proposal, not execution approval

Exactly one researcher decision remains: retain same-ID reuse as a candidate and proceed to a minimal control separating support reuse from decoder-geometry/coefficient-covariance contributions, or not. The result resolves presence of increased reuse, not its explanatory share. More count plots cannot settle that gap. Completion criterion before further execution: specify a constructible control, held-fixed objects, divergent predictions, residual boundary and stopping rule, then obtain researcher approval. If the control cannot distinguish explanations, stop expansion and redesign. No new job is submitted.

Researcher-owned fields remain unfilled: confirmed/weakened claims, current mechanism and reason, and final next decision. This record reports verified observations and the preapproved mechanical branch, not an invented human knowledge update.
