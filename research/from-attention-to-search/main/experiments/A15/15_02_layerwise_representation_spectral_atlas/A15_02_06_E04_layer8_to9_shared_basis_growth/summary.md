---
experiment_id: A15_02_06_E04_layer8_to9_shared_basis_growth
status: AI_DRAFT_AWAITING_HUMAN_CONFIRMATION
date: 2026-08-12
---

# Block 9 does not shift normalized Attention-write variance toward the frozen fine-enriched region

## Direct result

Blocks 8 and 9 were projected into identical directions of the frozen Mean Response basis. Projection coefficients were not normalized record by record. Instead, directionwise across-record variance was computed first and then normalized within each block:

\[
z_{\ell xj}=A_\ell(x)^\top v_j,
\qquad
e_{\ell j}=\operatorname{Var}_x(z_{\ell xj}),
\qquad
p_{\ell j}=\frac{e_{\ell j}}{\sum_k e_{\ell k}}.
\]

For the independently frozen fine-enriched region `[0.50,0.75)` (bands F9--F12), the registered normalized-share change was

\[
D_{sem}=Q_9-Q_8=-0.018314,
\qquad 95\%\ \mathrm{CI}=[-0.021459,-0.015450].
\]

Both expression halves were negative (`-0.021707`, `-0.014631`). The registered outcome is therefore `no_aligned_growth`: block 9 allocates **1.83 percentage points less** of its total Attention-write variance to this region than block 8.

This is not an absolute decrease. Raw region variance increased by

\[
G_{sem}=\log_2\frac{E_9}{E_8}=+0.78997,
\qquad 95\%\ \mathrm{CI}=[+0.74506,+0.86178],
\]

or approximately `1.73×`. Total write variance increased more, by `1.88×`; consequently the region's normalized share fell. Bands F1--F6, not F9--F12, had simultaneously positive normalized-share changes.

At block 9, the same F9--F12 region remains fine-enriched: fine minus coarse semantic share was `+0.012511`, with interval `[+0.001083,+0.020505]`. Thus “fine semantics lie relatively later” and “the 8→9 transition moves relatively later” are empirically different statements; the first does not imply the second here.

## Required figures

Figure 1 shows both normalized curves in the same direction identities and their signed difference. The 129-rank moving average is display-only.

![Same-direction block-8 and block-9 curves](figures/figure1_layer8_layer9_same_direction_curves.png)

Figure 2 separates relative redistribution, absolute growth, and the block-9 semantic bridge.

![Registered band evidence](figures/figure2_registered_band_evidence.png)

## Claim boundary

This result rejects the registered **normalized later-spectrum growth** claim for block 8→9 in the frozen Mean Response basis. It does not show that block 9 adds no information, that the raw later spectrum shrinks, or that the basis is universally invalid. Attention write is not proven residual-relative novelty, and no low-rank, causal, probe, or Router-utility claim was tested.

## One next decision

Human confirmation required: decide whether the next bounded test should replace total Attention-write variance with a residual-relative conditional-novelty estimator for the same fixed block 8→9 comparison. Do not search for a new basis merely to recover the rejected normalized shift.

Evidence: [Protocol](protocol.md), [Detailed record](detailed.md), [registered summary](tables/registered_summary.csv), [bandwise transition](tables/bandwise_transition.csv), and [split guards](tables/split_guards.csv).
