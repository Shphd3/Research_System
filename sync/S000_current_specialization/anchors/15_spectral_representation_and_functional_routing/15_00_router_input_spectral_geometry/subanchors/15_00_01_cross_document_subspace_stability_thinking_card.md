---
thinking_card_id: 15_00_01_cross_document_subspace_stability
status: full_execution_authorized
source_language: zh
source_file: 15_00_01_cross_document_subspace_stability_thinking_card_cn.md
formalization_authorized: true
protocol_authorized: true
implementation_authorized: true
full_run_authorized: true
updated: 2026-07-31
---

# Thinking Card: Centered Common-Subspace Stability

This is a faithful translation of the researcher-owned
[Chinese Thinking Card](15_00_01_cross_document_subspace_stability_thinking_card_cn.md).

## Human Judgment

- **Phenomenon:** Decommon removes the Router-representation mean, yet Q1 still
  finds strong Gate alignment with the covariance head of the centered input,
  while fixed M/T/N bands fail to obtain a stable functional certificate.
- **Mechanism guess:** Router representations contain a global mean, stable
  centered variation shared across data groups, and group-specific residuals.
  Decommon removes only the first term. The true group-specific residual may
  change across documents or batches and therefore fail to provide a coherent
  routing coordinate.
- **Strongest rival:** Residual subspaces are not less stable; apparent
  instability is finite-sample covariance noise. Alternatively, instability
  is real but unrelated to expert function or training benefit.
- **Most uncertain point:** Whether centered leading subspaces transfer across
  independent DCLM document groups and whether the remaining subspace is less
  transferable after the pooled leading component is removed.
- **Evidence that would change the judgment:** Centered top subspaces fail to
  transfer beyond matched Haar controls, or the orthogonal local residual
  transfers just as well.
- **Current decision:** Execute the approved frozen Protocol in parallel with
  A15_00_02 and adjudicate the typed verdict. New training is not authorized.

## AI Audit

Mean cosine alone cannot establish centered-subspace stability, and single
minibatch PCA can be dominated by estimation noise. The minimal falsifier is
cross-fitted top-64 transfer across disjoint document groups with matched Haar,
wrong-layer, and sample-size controls, followed by the same-dimensional test
in the orthogonal remainder.

## Confirmation

Formalization, the bilingual Protocol, implementation, and full frozen
execution are approved. Training, graph edits, publication, commit, and push
are not authorized.
