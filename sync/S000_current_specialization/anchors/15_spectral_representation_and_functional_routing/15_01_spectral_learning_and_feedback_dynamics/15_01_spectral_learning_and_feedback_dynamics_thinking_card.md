---
thinking_card_id: 15_01_spectral_learning_and_feedback_dynamics
status: human_core_approved_details_pending
source_language: zh
source_file: 15_01_spectral_learning_and_feedback_dynamics_thinking_card_cn.md
formalization_authorized: true
protocol_authorized: false
implementation_authorized: false
full_run_authorized: false
updated: 2026-07-30
---

# Thinking Card: Router Spectral Learning Dynamics

This is a faithful translation of the researcher-owned
[Chinese Thinking Card](15_01_spectral_learning_and_feedback_dynamics_thinking_card_cn.md).

## Human Judgment

- **Phenomenon:** On the actual Router input, the linear Gate is already
  strongly aligned with the covariance head at the earliest 10k checkpoint,
  but the alignment does not strengthen from 10k to 30k and middle/tail catch
  up relatively.
- **Mechanism guess:** The researcher approved the conditional finite-time
  spectral-acceleration claim. When expert advantage is comparable across
  spectral directions, the Gate is unsaturated, the optimizer does not whiten,
  and the representation basis is locally stable, larger covariance
  eigenvalues make the corresponding Gate modes learn faster. An isotropic
  spectrum supplies no covariance-defined preferred direction.
- **Strongest rival:** `Unknown`; the researcher requested AI proposals for
  itemized review.
- **Most uncertain point:** Whether real-MoE head alignment is caused by an
  already head-biased expert-advantage signal, the optimizer, representation
  drift, or Router--Expert feedback.
- **Evidence that would change the judgment:** Matched expert-advantage signals
  show no band learning-time difference under anisotropy; whitening fails to
  remove the difference; or real head alignment cannot be localized within
  2B tokens.
- **Current decision:** Review the E03-S controlled-causality and E03-R
  real-trajectory Approval Snapshots. No implementation or run is approved.

## AI Audit

The strongest live rival is expert-advantage orientation rather than input
covariance, followed by optimizer preconditioning and representation-basis
drift. The smallest separator is flat/anisotropic/whitened fixed-advantage
training with a tail-only counterexample, followed by a real run that records
raw gradients, optimizer-applied updates, and full $W\times U$ crossings.

## Confirmation

The theorem core is approved. Spectrum ratios, expert regime, primary metric,
real-model size, seeds, and logging density remain pending. Implementation and
execution are not authorized.

