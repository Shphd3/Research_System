---
thinking_card_id: 15_05_02_shallow_feature_specificity_pilot
status: human_direction_approved_details_pending
source_language: zh
source_file: 15_05_02_shallow_feature_specificity_pilot_thinking_card_cn.md
formalization_authorized: true
protocol_authorized: false
implementation_authorized: false
full_run_authorized: false
updated: 2026-07-30
---

# Thinking Card: Controlled Four-Layer Shallow-Head Pilot

Faithful translation of the
[Chinese Thinking Card](15_05_02_shallow_feature_specificity_pilot_thinking_card_cn.md).

## Human Judgment

The researcher proposes a controlled four-layer model in which layers 3 and 4
train with the high-variance component from layer 2 and are compared with other
conditions. If layer-2 head already separates a coarse variable relevant to
deep-expert compatibility, the side channel may reduce routing search cost.
The strongest rival is pending AI proposal. Evidence against the judgment is
failure to beat same-dimensional random and token-shuffled controls, benefit
only on a nuisance task, or no held-out loss improvement at matched FLOPs.

## AI Audit

The minimal falsifier is a held-out compatibility gate followed by matched
head/random/shuffled training on informative and nuisance tasks. The proposed
implementation first stabilizes layers 1--2 and uses an additive side channel
in layers 3--4.

## Confirmation

The four-layer direction and later 8x5090 submission route are approved. Every
Protocol Snapshot detail remains pending. No implementation or run is approved.

