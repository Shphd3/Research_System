---
thinking_card_id: 15_05_functional_coordinate_admission
status: human_approved_for_execution
source_language: zh
source_file: 15_05_functional_coordinate_admission_thinking_card_cn.md
formalization_authorized: true
protocol_authorized: true
implementation_authorized: true
full_run_authorized: conditional_on_e01_pass_and_pilot_guards
updated: 2026-07-30
---

# Thinking Card: A15_05 Functional Resolution In Middle And Long-Tail Bands

> This card translates the researcher's direct Q2 judgment from 2026-07-30
> in the [Chinese Thinking Card](15_05_functional_coordinate_admission_thinking_card_cn.md).
> It preserves the human research intent and is not the formal anchor or a
> Protocol.

## My Judgment

- **Phenomenon:** Q1 established that the trained linear Router relies mainly
  on the covariance head, while middle and long-tail bands remain accessible
  and alter a minority of native routing decisions.
- **Mechanism guess:** The small set of linear Gate logits may compress
  structure in middle or long-tail bands that is relevant to same-expert
  co-training compatibility. Those bands may therefore add functional
  resolution beyond the native Router and alter Router--Expert co-learning.
- **Strongest rival explanation:** Middle and long-tail bands may create only
  a different high-dimensional geometry. Equal-dimensional random subspaces,
  representation norm, outliers, documents, or batches may reproduce the
  partition without predicting expert-update compatibility or improving
  matched-compute training.
- **Most uncertain point:** Whether one-step cross-update compatibility truly
  separates functional information from geometric noise, and whether it is a
  valid admission gate for a 1--2B-token joint-training test.
- **Evidence that would change my mind:** On independent DCLM documents,
  middle, long-tail, or their union must add held-out prediction of co-training
  compatibility after controlling native logits, margin, expert identity,
  load, capacity, token count, norm, and batch, and must beat equal-dimensional
  random and wrong-layer bases. A later matched 8×5090 run must separately
  improve held-out loss per FLOP.
- **Current next decision:** Approve, revise, or reject the local functional
  admission Protocol. Do not run spectral-dispatch training before it passes.

## AI Audit

- **Undefined object or hidden assumption:** A different partition is not a
  functional gain, and one-step compatibility is only a proxy for long-horizon
  training benefit.
- **Minimal discriminator:** On the same independent token-group pairs, use
  actual cross-update loss as the target and compare the held-out increment
  from middle, tail, and middle+tail features against equal-dimensional random
  and wrong-layer controls.
- **AI recommendation:** pursue, with separate sequential Protocols for the
  local compatibility gate and the conditional eight-GPU training test.

## My Confirmation

- **Preserved or revised judgment:** The researcher approved the overall
  design and requested reuse of the actual Router-input spectrum, explicit A/B
  update steps, all three non-head treatments, and a predesigned but not
  prematurely executed eight-GPU training test.
- **May this enter a formal anchor:** yes; exact Protocol conditions and metric
  boundaries remain subject to section-by-section researcher review.
