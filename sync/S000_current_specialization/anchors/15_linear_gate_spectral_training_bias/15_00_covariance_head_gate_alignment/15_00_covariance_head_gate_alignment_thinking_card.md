# Thinking Card: A15_00 Linear-Gate Access To And Training Allocation Across Covariance Bands

> Status: faithful English translation of the researcher-facing Chinese card,
> revised and authorized for anchor formalization on 2026-07-30. The Chinese
> card remains the human judgment surface; the Protocol is still pending audit.

## My Judgment

- **Phenomenon:** The question is not to presume that a trained Router sees
  only the covariance head. It is to measure how much access and current
  decision use the linear Gate has for head, middle, and tail directions of
  its actual input, and whether training allocates weaker weight change to
  middle/tail than to the head.
- **Mechanism guess:** Large singular values mechanically enlarge logit
  response, and optimization may additionally allocate more equal-energy Gate
  gain to those directions. Middle/tail may remain visible but receive weaker
  realized response, decision use, or net Gate updates.
- **Strongest rival:** Head-dominant logits are fully explained by larger input
  covariance eigenvalues, or apparent training trends arise from Router-input
  basis drift rather than Gate-weight allocation.
- **Most uncertain point:** "Accessible," "currently used for routing," "given
  more weight change during training," and "functionally useful under spectral
  dispatch" are different claims. Frozen checkpoints answer only the first
  three.
- **Evidence that would change my mind:** Complete coarse/fine measurements on
  the actual Router input show that middle/tail equal-energy gain and decision
  effect are not weaker than the head, or that 30k--40k and 40k--80k Gate
  displacements are not stably head-biased. Conversely, head-biased updates in
  both intervals that strengthen fixed-basis endpoint contrasts support a late
  training tendency.
- **Current next decision:** Audit a frozen Q1 Protocol for access, current use,
  and training allocation. Functional effects of middle/tail dispatch require
  a separate later Protocol.

## AI Audit

- **Undefined object / hidden assumption:** If "weaker utility" means held-out
  loss or joint-training compatibility, a frozen geometry audit cannot answer
  it. E01 can only operationalize weaker gain, realized response, route effect,
  or net weight change.
- **Smallest distinguishing test:** On the directly hooked Router input, report
  coarse three-band and fine `12x64` $V/S/G$ at 30k, 40k, and 80k; measure both
  update intervals and cross $W_{30/40/80}$ with $U_{30/40/80}$.
- **AI recommendation:** Revise and pursue.

## My Confirmation

- **Preserved or revised judgment:** Use two resolutions, actual Router input,
  and 30k/40k/80k trajectory comparisons without 25%, 10%, or 8-of-12
  practical hard margins.
- **Permission to formalize:** `yes`; Protocol execution remains unapproved.

This card is not an approved anchor, Protocol, or result record.
