# Summary: A15_08_07_E06 Rank-Specific Multi-Representation Shared Scaling

Primary Anchor: [15_08_07 semantic-conditioned functional subspace](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_08_target_conditioned_layer_innovation/subanchors/15_08_07_semantic_conditioned_functional_subspace_anchor.md)  
Frozen Protocol: [protocol.md](protocol.md)  
Detailed record: [detailed.md](detailed.md)  
Result status / eligibility: **AI_DRAFT_AWAITING_HUMAN_JUDGMENT; evidence ELIGIBLE; registered verdict INSUFFICIENT**

Decision terms: \(U\) is the normalized attention update; \(G=X+U\) is the native same-block Router input; \(\Delta G\) is the adjacent-layer difference in \(G\); \(R_U\) is the part of \(U\) left after a TRAIN-fitted linear prediction from \(X\). A local space serves one domain's eight child labels, while a shared space uses one input basis for all eight domains. `NA_FULL_NOT_ADMITTED` means the complete map has no reliably positive benefit; `NA_NOT_IDENTIFIED` means the complete map is admitted but no tested rank reaches the registered simultaneous 90% threshold.

## Result Snapshot

**Verdict:** `INSUFFICIENT`. Per-rank learning removes the old literal `7 versus 56` claim. On the retrospective same-template panel, the independently learned shared spaces for \(U\), \(G\), and \(\Delta G\) need 18, 16, and 25 dimensions, while identified single-domain requirements are usually 6--7. This is broader than one local task but substantially smaller than the sums of eight local requirements, 54, 53, and 56. The strict shared \(r_{90}\) crossings do not replicate on the independent 640-row confirmation set; \(R_U\) does not even admit a positive full-map benefit there.

**What we established:** all 728 registered rank-specific fits, four TEST-blind layer scans, controls, 2,000 template-family bootstraps, sealed confirmation extraction, and the final artifact audit completed. The algorithmic correction is real: candidate ranks were independently optimized rather than taken as prefixes of one rank-56 solution.

**What the experiment shows:** there is retrospective evidence that some representations need a shared discriminant space broader than a single-domain space. There is not independent confirmation of a stable cross-expression functional-rank expansion. The conditional \(R_U\mid X\) branch has no admitted positive full-map increment on any panel.

**What we do next:** `AWAITING_HUMAN_JUDGMENT` — confirm or correct the bounded knowledge update above in the active Focus before any Anchor update, daily report, or new representation-learning experiment.

## Decision-Bearing Setup

**Question:** after independently optimizing every candidate rank, does one eight-domain linear input subspace require more dimensions than a single-domain subspace, and does that relation replicate on fresh expressions?  
**Treatment and control:** rank-specific direct shared learning versus eight local fits, the old maximum-rank prefix, a local-union oracle, and Haar subspaces.  
**Changed variable:** representation (\(R_U\), \(U\), \(G\), or \(\Delta G\)), task count, and requested rank.  
**Held fixed:** Qwen3-30B-A3B, the 19,200-row taxonomy and split, the eight within-domain eight-class tasks, TRAIN standardization, DEVELOPMENT selection, bootstrap rule, and sealed 640-row confirmation set.  
**Primary metric and unit:** \(r_{90}\), the smallest number of projection dimensions whose simultaneous one-sided lower bound for \(B_r-0.9B_{full}\) is positive under template-family resampling and the worst-domain rule.  
**Known limitation:** this measures linear child-label accessibility, not native gate use, expert-relative utility, causality, or nonlinear rank.

## Verdict Basis

| Registered rule | Observed value | Guard / eligibility | Verdict | Evidence source |
| --- | --- | --- | --- | --- |
| Every candidate rank must be learned directly | 728/728 hashed states; six DEVELOPMENT candidates per state | synthetic rank-3 recovery passed; direct-versus-prefix projector gap 0.1766 | ELIGIBLE | worker `fit/fit_manifest.json`; `synthetic_guard.json` |
| Same-template shared rank should exceed a typical local rank | \(U\): shared 18 versus locals 6--7; \(G\): 16 versus 6--7; \(\Delta G\): 25 versus 7 | full maps admitted; simultaneous worst-domain rule | RETROSPECTIVE SUPPORT | [shared curves](tables/shared_curves.csv), [local curves](tables/local_curves.csv) |
| The direction must replicate on new expressions | confirmation shared \(r_{90}\) is `NA_NOT_IDENTIFIED` for \(U\), \(G\), \(\Delta G\); \(R_U\) is `NA_FULL_NOT_ADMITTED` | independent 640-row set; no confirmation tuning | INSUFFICIENT | [shared curves](tables/shared_curves.csv), worker `analysis/results.json` |
| \(R_U\) should add label access beyond the \(X\) baseline | all three panels are `NA_FULL_NOT_ADMITTED`; confirmation domain full-map LCBs range from -10.252 to -2.809 nats | three-fold leave-one-template-family-out TRAIN baseline | NOT ADMITTED | [conditional shared curves](tables/conditional_shared_curves.csv), [conditional local curves](tables/conditional_local_curves.csv) |
| Secondary rank diagnostics must not exceed requested rank | 3,360 rows checked; 840 precision-bug rows corrected; zero remaining violations | six decision-bearing artifacts remained byte-identical | PASS, DIAGNOSTIC ONLY | [rank diagnostics](tables/rank_diagnostics.csv), worker `diagnostic_reaggregation_receipt.json` |

## Key Evidence

The strongest retrospective pattern is not `7 versus 56`. It is “single-domain 6--7 dimensions versus one shared space of 16--25 dimensions” on the same-template panel, with partial compression relative to eight independent local budgets. On the new-template retrospective panel, only \(\Delta G\) has an identified shared crossing, at 43 dimensions. On the sealed confirmation panel, none of the four shared direct curves has an identified \(r_{90}\).

## Central Figures

![Rank-specific local-versus-shared result across panels](figures/functional_rank_comparison.png)

This figure shows point retention only. The typed `IDENTIFIED`, `NA_NOT_IDENTIFIED`, and `NA_FULL_NOT_ADMITTED` verdicts come from the simultaneous bootstrap analysis in the table above, not from visually crossing the dashed 0.9 line.

![Conditional R_U beyond X has non-positive mean benefit](figures/conditional_rank_comparison.png)

The conditional figure uses mean cross-entropy benefit in nats rather than an undefined ratio. Every conditional full-map result is not admitted, so no conditional functional rank exists in this experiment.

## Claim Boundary

**Can claim:** per-rank correction invalidates the old maximum-rank-prefix interpretation; same-template \(U\), \(G\), and \(\Delta G\) show a shared linear label-accessibility requirement broader than one local task; that relation is not independently confirmed on fresh expressions.  
**Cannot claim:** stable intrinsic semantic rank, a universal `7/56` law, native Router use, expert utility, causal benefit of projection, nonlinear low rank, or justification to start representation-space learning.

## Next Decision

**Decision:** `AWAITING_HUMAN_JUDGMENT` — confirm or correct this proposed update: “the old `7/56` fact is rejected; retrospective shared-rank expansion remains for some representations, but robust cross-expression expansion is unestablished.”  
**Completion criterion:** the researcher records `Direct result`, `My conclusion`, `Cannot claim`, and exactly one next scientific decision in the active Focus.  
**Resume action:** after that confirmation, synchronize the Anchor boundary and create the delayed daily report; do not open a new Router or representation-learning run before the decision is explicit.
