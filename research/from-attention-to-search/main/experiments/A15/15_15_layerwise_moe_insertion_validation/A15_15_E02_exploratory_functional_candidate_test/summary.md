# Summary: A15_15_E02 Exploratory Functional Candidate Test

Primary Anchor: [A15_15](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_15_layerwise_moe_insertion_validation/15_15_layerwise_moe_insertion_validation_anchor.md)

Frozen Protocol: [protocol.md](protocol.md)

Detailed record: [detailed.md](detailed.md)

Result status: `FULL_RUN_COMPLETE`; evidence `ELIGIBLE`; interpretation `AI_DRAFT_AWAITING_HUMAN_CONFIRMATION`

Registered typed verdict: `MULTIPLE_TESTED_FUNCTIONAL_POSITIONS`

## 1. Purpose

Determine which of blocks `{0,10,13}` makes correct parent/child specialization add next-token task value and matched child-expert function, and whether that functional order agrees with the static-readability order `10 > 13 > 0`.

## 2. Hypothesis

Block 10 should be the only tested block with replicated positive ordinary-minus-correct, shuffled-minus-correct, and both wrong-child-minus-correct NLL differences, and should lead the other blocks outside paired article-component uncertainty. The strongest rival is that static readability exposes labels without selecting a uniquely better functional insertion point.

## 3. Analysis Method

- Compare the correct forced hierarchy with the ordinary rank-24 adapter and the capacity-matched shuffled hierarchy at each block and seed; positive \(A\) and \(F\) isolate overall specialization and correct-grouping task value.
- Replace each correct model's child expert by both same-parent alternatives without updating weights; positive \(W^1\) and \(W^2\) establish matched expert function rather than route-label readability.
- Define \(H=\min(A,F,W^1,W^2)\) in nats per target token, require \(H>0\) in both seeds, and use 2,000 paired article-component bootstrap replicates to decide whether one passing block leads both competitors.

## 4. Conclusion

Verdict: `MULTIPLE_TESTED_FUNCTIONAL_POSITIONS`.

All three tested blocks have positive \(H\) in both seeds. Correct grouping therefore adds task value over both controls and creates non-interchangeable same-parent child experts at blocks 0, 10, and 13. The point order is `13 > 10 > 0`, but block 13's lead is unresolved: its paired interval versus block 10 is `[-0.000054, 0.001263]` nat/token and versus block 0 is `[-0.000414, 0.002093]`. No unique functional position is identified.

| Block | \(H_{17}\) | \(H_{29}\) | Two-seed mean \(H\) | Registered status |
|---:|---:|---:|---:|---|
| 13 | `0.004196` | `0.004260` | `0.004228` | matched-functional; lead unresolved |
| 10 | `0.003967` | `0.004001` | `0.003984` | matched-functional |
| 0 | `0.003425` | `0.002930` | `0.003177` | matched-functional |

Evidence: [functional components](tables/01_functional_components.csv), [ordering](tables/02_functional_order.csv), [paired intervals](tables/02_pairwise_leads.csv), and [completion audit](tables/05_completion_audit.json).

The functional point order only partly agrees with static readability: `13 > 10 > 0` versus `10 > 13 > 0`, with three-item Spearman correlation `0.5`. The top two reverse, and their functional difference is unresolved. Static readability remains a candidate generator, not a unique layer selector.

The task-only online hierarchy does not establish semantic dispatch. Its confirmation parent accuracy is `0.324–0.335`, leaf accuracy is `0.111–0.120`, and route loads collapse heavily in every block/seed. This does not affect the forced-path \(H\) verdict, but it prevents claiming that the matched function is reachable by the tested unsupervised online Router.

### Claim Boundary

Can claim: under this frozen Qwen3-0.6B/M2D2 setup, all three tested blocks show replicated correct-grouping task value and same-parent expert matching relative to the registered controls.

Cannot claim: block 13 or block 10 is uniquely best, any block is optimal or earliest among all 28 blocks, static readability preserves the functional ranking, or the task-only Router learns semantic dispatch.

### Next Step Analysis

Decision: `AI 建议` stop treating E02 as a layer-selection result and retain blocks 10 and 13 as an unresolved shortlist only if a later system decision truly requires one insertion point.

Why it follows: all candidates pass the functional floor, while the registered pairwise intervals do not resolve a winner and the static top two reverse.

Unresolved uncertainty: whether the small block-13 versus block-10 difference survives fresh seeds and an untouched evaluation corpus.

Completion criterion: a separately approved replication resolves the paired block-13 versus block-10 contrast or establishes a prespecified practical equivalence margin.

Stop or redirect condition: if no downstream decision requires one layer, stop here; do not spend another run merely to rank statistically indistinguishable candidates.

Resume action: the researcher confirms or corrects the verdict boundary and decides whether a unique layer is operationally necessary.
