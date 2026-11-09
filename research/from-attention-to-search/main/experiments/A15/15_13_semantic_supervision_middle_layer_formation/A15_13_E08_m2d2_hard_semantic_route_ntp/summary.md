# Summary: A15_13_E08 M2D2 Hard Semantic Route Next-Token Prediction

Primary Anchor: [A15_13_04](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_13_semantic_supervision_middle_layer_formation/subanchors/15_13_04_m2d2_causal_lm_semantic_routing_anchor.md)  
Frozen Protocol: [protocol.md](protocol.md)  
Detailed record: [detailed.md](detailed.md)  
Result status: `ELIGIBLE`; `AI_DRAFT_AWAITING_HUMAN_CONFIRMATION`

## Result Snapshot

**Verdict:** `PASS_SEMANTIC_FUNCTIONAL_VALUE_NTP`.

When the correct M2D2 coarse and fine paths were supplied, semantic child grouping achieved lower held-out next-token NLL than both balanced-random grouping and no fine split, and its children were not interchangeable. This removes the preceding CLINC150 classification-target shortcut, but the benefit is an average over domains rather than a universal gain.

## Decision-Bearing Setup

The hard hierarchy trained a gold coarse path for 144 updates, froze the parent experts, then trained three matched stage-two arms for 144 updates: one common child per coarse domain, balanced random assignment to three children, and the true fine-domain child. Every selected expert had coefficient exactly one. Shadow Router probabilities were diagnostic only and could not select, scale, or update experts.

The primary metric is the worse of semantic NLL advantage over random and over no fine split, averaged equally over nine fine domains and two seeds.

## Verdict Basis

| Registered rule | Observed value | Guard / eligibility | Verdict | Evidence source |
| --- | --- | --- | --- | --- |
| Semantic beats both controls in both seeds | worst-control seed effects `+0.001468`, `+0.001544` | all directions positive | Pass | [Detailed evidence](detailed.md) |
| Positive paired 95% lower bound | worst-control `+0.001506 [0.001396, 0.001618]` NLL/token | interval fully above zero | Pass | same aggregate |
| Deleting active child increases NLL | `+0.004691 [0.004559, 0.004825]` | positive in both seeds | Pass | same aggregate |
| Wrong within-parent child increases NLL | `+0.005355 [0.005205, 0.005504]` | positive in both seeds | Pass | same aggregate |

## Central Figure

![Decision-bearing NLL and intervention contrasts](figures/decisive_contrasts.png)

How to read: all four hard-route points are above zero with intervals clear of zero, so semantic grouping beats both controls and its trained children cannot be deleted or swapped freely.

## Robustness Boundary

![Per-domain NLL contrast](figures/per_domain_robustness.png)

How to read: hard semantic routing is better on seven fine domains, but Biology and Physical sciences are below zero against both controls; the Pass is therefore an equal-domain average claim, not a universal-domain claim.

## Claim Boundary

**Can claim:** the registered 3-by-3 Wikipedia semantic partition has Oracle functional value for continued causal language modeling in this frozen-base block-14 LoRA hierarchy.

**Cannot claim:** that a learned Router recovers the gain, that all domains benefit, that the effect reflects deep reasoning rather than topical regularity, or that original Qwen representations changed. Gold metadata is required at inference in this condition.

## Next Decision

Use the frozen E07 learned-semantic checkpoints to separate predicted-versus-gold expert selection from learned-probability-versus-unit expert scaling. Completion requires a no-retraining paired confirmation audit showing which forward-path change recovers the `0.001506` Oracle headroom.
