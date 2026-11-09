# Summary: A15_13_E07 M2D2 Learned Semantic Router Next-Token Prediction

Primary Anchor: [A15_13_04](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_13_semantic_supervision_middle_layer_formation/subanchors/15_13_04_m2d2_causal_lm_semantic_routing_anchor.md)  
Frozen Protocol: [protocol.md](protocol.md)  
Detailed record: [detailed.md](detailed.md)  
Result status: `ELIGIBLE`; `AI_DRAFT_AWAITING_HUMAN_CONFIRMATION`

## Result Snapshot

**Verdict:** `FAIL_NO_LEARNED_FUNCTION`.

Gold fine-domain supervision made the learned token Router substantially more semantic and its children measurably non-interchangeable, but it did not recover the Oracle language-modeling value. It increased rather than reduced held-out next-token NLL relative to the architecture-identical task-only Router in both seeds. The next decision is an evaluation-only decomposition of route-selection error versus probability attenuation before any retraining.

## Decision-Bearing Setup

The learned hierarchy first trained a coarse Router and parent experts for 144 updates, froze them, then trained the fine Router and child experts for another 144 updates. The treatment added gold fine-domain route cross-entropy; the primary control used only next-token loss; the shuffled control used balanced labels unrelated to text. Qwen3-0.6B-Base, its language head, data, child initialization, updates, optimizer, and block-14 rank-eight LoRA capacity were held fixed.

The primary metric is equal-fine-domain confirmation NLL in natural-log units per target token. Positive `task-only minus semantic` would favor semantic supervision.

## Verdict Basis

| Registered rule | Observed value | Guard / eligibility | Verdict | Evidence source |
| --- | --- | --- | --- | --- |
| Semantic NLL below task-only in both seeds | seed effects `-0.001353`, `-0.000755`; pooled `-0.001054` | negative means semantic is worse | Fail | [Detailed evidence](detailed.md) |
| Positive paired 95% lower bound | `[-0.001142, -0.000966]` | entirely below zero | Fail | same aggregate |
| Fine routing becomes more semantic | mean NMI `0.00646 -> 0.12059`; macro-F1 `0.284 -> 0.564` | both seeds improve; causal guard max error `0.0` | Pass diagnostic | same aggregate and completion audit |
| Active child is useful | deletion `+0.001292 [0.001211, 0.001375]`; wrong child `+0.000737 [0.000666, 0.000811]` | positive in both seeds | Pass functional diagnostic | same aggregate |

## Central Figure

![Decision-bearing NLL and intervention contrasts](figures/decisive_contrasts.png)

How to read: values above zero favor semantic routing or show intervention harm; the first point is below zero while both learned-expert interventions are above zero.

## Claim Boundary

**Can claim:** fine-domain supervision organized causal token routes and created non-interchangeable child function, but this learned route-and-scale policy was worse than task-only continued training on held-out NLL.

**Cannot claim:** that semantic supervision is useless, that the Oracle partition lacks value, that wrong expert choice alone caused the failure, or that native Qwen representations were reshaped. The Router selected experts and scaled them by probabilities, so selection error, probability attenuation, and route-loss trade-off remain confounded.

## Next Decision

Evaluate the frozen learned-semantic checkpoints under four forward paths—predicted versus gold expert index crossed with learned probability versus unit coefficient. Completion requires paired confirmation NLL and the same deletion/substitution audit without retraining; this identifies whether the lost Oracle value comes mainly from wrong selection, probability scaling, or child training.
