---
experiment_id: A15_10_E01_qwen3_30b_cross_parent_fine_function_transfer
status: EVIDENCE_COMPLETE_AI_INTERPRETATION_AWAITING_HUMAN_CONFIRMATION
completed: 2026-08-28
acp_job: pt-9dwr9q52
---

# Summary: Cross-Parent Fine-Function Transfer

Primary Anchor: [A15_10 Anchor](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_10_cross_parent_fine_function_transfer/15_10_cross_parent_fine_function_transfer_anchor.md)  
Frozen Protocol: [protocol.md](protocol.md)  
Detailed record: [detailed.md](detailed.md)  
Result status / eligibility: evidence complete; AI interpretation awaits the
researcher's result and boundary confirmation.

## Result Snapshot

**Verdict:** no registered layer established bidirectional, C4/C5-replicated
cross-parent fine-function transfer. Blocks 4 and 12 are
`Fail_to_establish_transfer`; Blocks 20, 28, 36, and 44 are `Insufficient`
because one or more Own/convergence admissions failed.

Across the 18 eligible panel--layer--direction cells, relative retention
\(RR\) was 0.0339--0.1810 with median 0.0743. Cross therefore recovered only a
small fraction of the target-own NLL advantage over its matched source-label
permutation null. Only 1/24 directions beat the registered Cross-null 2.5th
percentile: C5 Block 36 mathematics \(\rightarrow\) physics. It did not reproduce
in C4, and the reverse direction at that layer was ineligible.

The most reliable update is:

> Stable mathematics and physics fine spaces are not functionally
> interchangeable under the registered matched test. At the same time, the
> high fine-label readability of Cross, coarse, and permuted seven-dimensional
> controls shows that decodability is distributed and redundant. Thus this
> result rejects a strong shared-fine-space premise, but it does not prove
> strictly parent-local coordinates.

The experiment does not authorize Router training. The next decision is
whether to promote one matched causal architecture test of a shared fine
Router versus a correct-parent-conditioned local fine Router.

## Decision-Bearing Setup

- **Question:** can a seven-dimensional mathematics fine Fisher space carry
  held-out physics fine classification after retraining a physics head, and
  vice versa?
- **Changed variable:** only the parent supplying the input space: target-own
  (`Own`) versus other-parent (`Cross`).
- **Held fixed:** target rows and labels, seven input coordinates, A/B
  cross-fit, target-head family, train-only regularization selection, held-out
  scoring, and the same pooled within-class Fisher metric.
- **Primary metric:**
  \(RR=(L_{null,50}-L_{Cross})/(L_{null,50}-L_{Own})\), in held-out negative log
  likelihood (NLL); it is continuous and unclipped.
- **Primary gate:** Cross NLL must be below its complete-pipeline permutation
  2.5th percentile in both directions and both panels at a layer, after all Own
  and numerical admissions pass.
- **Known limitation:** C4/C5 are controlled natural-language expression
  panels. They do not represent unrestricted natural-language semantics.

## Verdict Basis

| Registered rule | Observed value | Guard / eligibility | Verdict | Evidence source |
| --- | --- | --- | --- | --- |
| Full registered matrix | 24/24 cells present; 18 eligible | completion audit passed | complete | [completion audit](../../../../../../../../MoE_Router/experiments/20260828_a15_10_e01_qwen3_30b_cross_parent_fine_function_transfer/runs/full-20260828T032514Z/completion_audit.json) |
| Transferable layer | all four panel/direction cells eligible and Cross-null excess | no layer passed; only 1/24 direction had excess | not established | [cells.csv](../../../../../../../../MoE_Router/experiments/20260828_a15_10_e01_qwen3_30b_cross_parent_fine_function_transfer/runs/full-20260828T032514Z/analysis/cells.csv) |
| Eligible RR profile | continuous, unclipped | 0.0339--0.1810; median 0.0743 | small positive retention, not transfer proof | [results.json](../../../../../../../../MoE_Router/experiments/20260828_a15_10_e01_qwen3_30b_cross_parent_fine_function_transfer/runs/full-20260828T032514Z/analysis/results.json) |
| Invalid cells retained | no replacement | five Own-null admissions failed; one cell had a convergence failure | Blocks 20--44 partly insufficient | [detailed.md](detailed.md#7-main-results) |

## Key Evidence

Raw held-out NLL is the decisive reading path. Own is consistently best, while
Cross generally lies near its matched permutation band. Black crosses mark
ineligible cells; they remain visible and were not replaced.

![Matched target-head functional transfer](figures/figure1_functional_transfer_ladder.png)

The raw classification accuracy alone is misleading: Cross balanced accuracy
is often high, but matched permuted spaces and the common coarse space are also
highly readable. The registered comparison therefore uses held-out NLL against
the full-pipeline null, not the statement “Cross accuracy is high.”

## Claim Boundary

### Can claim

- no layer satisfies the registered bidirectional, two-panel transfer rule;
- the other parent's fine space preserves only 3.4%--18.1% of the target-own
  NLL advantage in eligible cells under the empirical RR normalization;
- passive geometric overlap and held-out functional readability are different
  observables;
- dominant shared fine coordinates are not supported for mathematics and
  physics on C4/C5.

### Cannot claim

- that mathematics and physics fine spaces are strictly orthogonal or strictly
  parent-local;
- that high Cross accuracy is evidence for shared semantics;
- that parent-conditioned routing improves language-model loss;
- that the native Router reads the Fisher spaces;
- that any one layer is the correct Router layer;
- that the result generalizes beyond the two parents and controlled panels.

## Next Decision

**Decision:** the researcher confirms or corrects whether the next unique
question should be: under matched capacity and optimization, does a
correct-parent-conditioned local fine Router outperform a single shared fine
Router on held-out fine routing and language-model loss?

**Completion criterion:** one preregistered causal architecture comparison in
which parent conditioning is the only structural difference, with routing
accuracy and held-out NLL both required and no passive subspace proxy used as
the verdict.

**Resume action:** after human confirmation, create a new Focus and Protocol;
do not launch it from this result record.
