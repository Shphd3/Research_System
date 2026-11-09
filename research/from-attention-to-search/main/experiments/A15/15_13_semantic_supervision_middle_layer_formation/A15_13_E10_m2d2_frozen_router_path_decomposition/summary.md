# Summary: A15_13_E10 Frozen Router Forward-Path Decomposition

Primary Anchor: [A15_13_04](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_13_semantic_supervision_middle_layer_formation/subanchors/15_13_04_m2d2_causal_lm_semantic_routing_anchor.md)
Frozen Protocol: [protocol.md](protocol.md)
Detailed record: [detailed.md](detailed.md)
Result status: `ELIGIBLE`; `AI_DRAFT_AWAITING_HUMAN_CONFIRMATION`

## Result Snapshot

**Registered verdict: `NEITHER_REPAIR_RECOVERS`.**

For the learned-semantic hierarchy, replacing every predicted expert index with the gold domain index and every learned residual coefficient with one made confirmation NLL worse by `0.001952` nats per target token, paired 95% interval `[-0.002074,-0.001828]`. The only positive component was removing the child probability attenuation (`+0.000307 [0.000265,0.000350]`), but it was smaller than the harm from forcing the parent index, parent coefficient, and child index.

The flat controls make the boundary stronger. Forcing gold indices and unit coefficients worsened the task-only flat model by `0.071301` NLL and the gold-route-supervised flat model by `0.020896` NLL. Therefore the observed deficit is not a simple inference-time wrong-index or probability-scaling defect. The experts were trained for their learned routed path and are not interchangeable with an Oracle path imposed only at evaluation.

## Decisive Decomposition

Positive values below mean that the intervention lowers NLL; negative values mean that it harms language modeling.

| Frozen checkpoint | Coarse index | Coarse coefficient | Fine index | Fine coefficient | All factors repaired |
| --- | ---: | ---: | ---: | ---: | ---: |
| Hierarchical task-only | `-0.001115` | `-0.001048` | `-0.001917` | `-0.000010` | `-0.004096` |
| Hierarchical semantic | `-0.000675` | `-0.001303` | `-0.000383` | **`+0.000307`** | `-0.001952` |
| Hierarchical shuffled-label | `-0.000735` | `-0.001297` | `-0.000299` | **`+0.000556`** | `-0.001667` |

For the learned-semantic hierarchy, the original path had seed NLLs `2.881524` and `2.881320`; the fully forced gold/unit path had `2.883708` and `2.883040`. Both seeds agree on the direction.

| Flat checkpoint | Index contribution | Coefficient contribution | Full repair |
| --- | ---: | ---: | ---: |
| Task-only rank-24 leaves | `-0.072462` | `+0.001161` | `-0.071301` |
| Gold-nine supervised rank-24 leaves | `-0.033960` | `+0.013065` | `-0.020896` |

Even the gold-route-supervised flat model was trained under a learned, probability-scaled forward path. Its negative gold-index intervention therefore does not mean gold labels are intrinsically useless; it means an inference-only Oracle substitution does not reproduce Oracle-responsibility training.

## Central Figures

![Hierarchical path contribution decomposition](figures/hierarchical_path_contributions.png)

How to read: bars above zero improve NLL. Only the fine-path coefficient has a small positive effect for semantic and shuffled routing; the other forced changes hurt.

![Flat path decomposition](figures/flat_path_decomposition.png)

How to read: both points lie far left of zero, so forcing the gold expert index damages both frozen flat checkpoints; removing probability scaling recovers only a fraction of that loss.

## Claim Boundary

**Can claim:** probability attenuation at the child path imposes a small measurable cost, but neither a gold-index repair nor a full gold/unit forward repair recovers the learned-semantic model's task deficit. Training-time responsibility and route/expert co-adaptation remain the leading explanation.

**Cannot claim:** that semantic routing has no value, that gold-label training cannot work, or that a hard-route model trained end to end would fail. This audit changed inference only and did not retrain experts under the forced paths.

## Next Decision

Use training-time controls, not further inference-only repairs: compare loss-free load balancing, coarse-information removal before fine routing, and frozen versus trainable coarse experts while preserving a matched task-only control.
