---
thinking_card_id: 15_00_02_gate_common_residual_preference
status: full_execution_authorized
source_language: zh
source_file: 15_00_02_gate_common_residual_preference_thinking_card_cn.md
formalization_authorized: true
protocol_authorized: true
implementation_authorized: true
full_run_authorized: true
updated: 2026-07-31
---

# Thinking Card: Gate Alignment With Transferable Versus Local Residual Modes

This is a faithful translation of the researcher-owned
[Chinese Thinking Card](15_00_02_gate_common_residual_preference_thinking_card_cn.md).

## Human Judgment

- **Phenomenon:** After decommon removes the mean, the Gate remains strongly
  aligned with the centered covariance head.
- **Mechanism guess:** A single linear Gate can accumulate directions that
  recur across data groups more easily than a residual that rotates by group.
  Decommon changes the DC inductive bias but does not force use of truly
  group-specific residuals.
- **Strongest rival:** Alignment is due to input energy, dimensionality,
  shared wrong-layer directions, or native-score redundancy. Alternatively,
  stable directions are functionally useful, so preferring them is not a
  failure.
- **Most uncertain point:** After equalizing input energy and removing the
  expert-common logit direction, whether both Gate gain and native route
  dependence are greater for a pooled centered-common candidate than for
  equal-dimensional shard-local residuals.
- **Evidence that would change the judgment:** The pooled candidate does not
  exceed local residuals or orientation nulls in equal-energy gain, or native
  route ablation depends more on local residuals.
- **Current decision:** Execute the approved frozen Protocol in parallel with
  A15_00_01 and adjudicate the typed verdict. New training is not authorized.

## AI Audit

A15_00_01 has not yet certified the pooled candidate as stable. This subanchor
therefore first reports pooled-versus-local Gate preference. The joint phrase
“Gate prefers stable common” is licensed only if both subanchors pass. The
proposed primary metric is $B_{P:L}=\log(G_P/G_L)$; it cannot establish expert
utility or training benefit.

## Confirmation

Formalization, the bilingual Protocol, implementation, and full frozen
execution are approved. Training, graph edits, publication, commit, and push
are not authorized.
