---
thinking_card_id: 15_05_04_fixed_band_cross_update_compatibility
parent_anchor: 15_05_functional_coordinate_admission
status: human_approved_for_execution
source_language: zh
source_file: 15_05_04_fixed_band_cross_update_compatibility_thinking_card_cn.md
formalization_authorized: true
protocol_authorized: true
implementation_authorized: true
full_run_authorized: true
updated: 2026-07-30
---

# Thinking Card: A15_05_04 One-Step Cross-Update Compatibility Gate

This is a faithful translation of the researcher-owned
[Chinese Thinking Card](15_05_04_fixed_band_cross_update_compatibility_thinking_card_cn.md).

## My Judgment

- **Phenomenon:** Middle and long-tail bands can alter representation
  neighborhoods, but frozen evidence does not show whether the new partition
  groups tokens that help each other when training one expert.
- **Mechanism guess:** If a band preserves functional relations, two
  independent token groups that are similar in that band should produce less
  conflicting or more mutually beneficial updates to the same expert than the
  native Gate logits predict.
- **Strongest rival explanation:** Compatibility is fully explained by native
  expert identity, logits, token loss, gradient norm, document, or batch; the
  band increment does not beat equal-dimensional random directions.
- **Most uncertain point:** Whether a small-step, fixed-route cross-loss target
  is stable and reproducible.
- **Evidence that would change my mind:** The document-held-out compatibility
  $\Delta R^2$ interval is above zero and beats the equal-dimensional random
  q95 and wrong-layer control, while step-size, route-replay, self-update, and
  data-independence guards all pass.
- **Current next decision:** Decide whether the selected band is admitted to a
  matched joint-training test.

## AI Audit

- **Undefined object or hidden assumption:** Compatibility is conditional on
  the target layer, expert, and local step size and cannot be promoted to a
  long-horizon model benefit.
- **Minimal discriminator:** Static neighborhoods may be novel while
  compatibility $\Delta R^2$ is no better than random. That result falsifies
  the claim that geometric resolution is already functional resolution.
- **AI recommendation:** pursue; keep static novelty diagnostic and use
  held-out $\Delta R^2$ as the only admission metric.

## My Confirmation

- **Preserved or revised judgment:** The researcher approved the overall A/B
  bidirectional update, three non-head treatments, and random/wrong-layer
  control design.
- **May this enter a formal anchor:** yes; exact sample sizes, aggregation, and
  execution authorization remain under review.
