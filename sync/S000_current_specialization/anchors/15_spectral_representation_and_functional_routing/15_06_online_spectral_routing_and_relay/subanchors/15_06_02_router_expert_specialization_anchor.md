---
anchor_id: 15_06_02_router_expert_specialization
parent_anchor: 15_06_online_spectral_routing_and_relay
status: completed_mixed_not_supportive
canonical_language: en
updated: 2026-08-10
---

# A15_06_02 Router--Expert Specialization And Utilization


## 1. Problem Definition

This subanchor asks whether the five differentiable-load-balancing training
arms differ only in terminal language-model loss, or also in two distinct
functional properties: experts become non-interchangeable on the same inputs,
and the Router selects the expert with the best counterfactual next-token
utility.  It inherits the parent A15_06 comparison between covariance-ranked
H/M/T routing and dimension-matched random routing.  It does not reopen the
parent endpoint-NLL verdict or replace the current A15 research mainline.

The decision question is: at paired 2B, 5B, and 10B checkpoints, do Local-HMT
or Relay-HMT form and exploit expert specialization more strongly than their
matched random controls?  Pass changes the parent interpretation from an
undifferentiated architecture effect to covariance-specific functional
evidence; Fail leaves covariance identity unsupported; missing counterfactual
or paired evidence is Insufficient.

## 2. Physical Priors

If a routing coordinate helps divide learnable functions, then expert
transformations should become less interchangeable and Router logits should
rank the experts by their token-specific downstream utility.  Merely lowering
parameter overlap is not enough: arbitrary bottlenecks, permutations, noise,
or redundant parameterizations can produce geometric differences without
better expert choice.  This prior is false here if HMT differs geometrically
but does not beat its random control in counterfactual choice quality.

## 3. Falsifiable Hypotheses

**H1, covariance-specific functional routing:** compared with the matched
random arm, HMT yields lower Router expert-choice regret and higher rank
agreement between Router scores and forced-expert utility at 10B, with a
supporting progression from parameter geometry to same-input expert outputs
and nonzero swap cost.

**Strongest rival, arbitrary-bottleneck differentiation:** HMT and random
controls can both make experts look different, but neither reliably improves
Router choice; a single globally superior expert may also create swap cost
without token-conditional specialization.

## 4. Mathematical Model

For token $x$, target layer $\ell$, Router-selected expert $s(x)$, and the
next-token NLL $L_{\ell,e}(x)$ obtained by forcing expert $e$ only at that
token and layer while leaving all other routing native, define expert-choice
regret

$$
r_\ell(x)=L_{\ell,s(x)}(x)-\min_e L_{\ell,e}(x)\quad\text{nat/token}.
$$

Zero means the Router selected a counterfactually best expert among the eight;
larger values measure the immediate loss paid for its choice.  The metric does
not identify long-horizon training causality, because it intervenes on a
frozen checkpoint at one token and one layer.

## 5. Computational Realization

Five seed-17 checkpoints are frozen at 2B, 5B, and 10B tokens.  For fixed
held-out documents and positions, every sparse expert is forced in turn using
the native Router probability as a common output amplitude; unit-amplitude
sensitivity is a guard.  Router logits are compared with negative
forced-expert NLL by within-token rank correlation.  Expert specialization is
then decomposed into: dominant parameter-subspace overlap; linear centered
kernel alignment on the same expert inputs; counterfactual swap cost and the
diversity of the oracle-best expert; and empirical alignment between Router
scores and activation of each expert's dominant input parameter subspace.
The shared expert remains fixed and is reported separately.

## 6. Minimal Falsification Tests

The decisive comparisons are Local-HMT versus Local-Random-Matched and
Relay-HMT versus Relay-Random at 10B.  The primary metric is the document-
paired difference in mean expert-choice regret, equally averaging the four
layers.  A covariance-specific functional certificate requires the HMT arm to
have a 95% paired interval below zero for regret and above zero for Router
score--utility rank correlation.  Two registered matched comparisons use a
Holm-adjusted paired sign-flip test.  Parameter overlap or CKA alone cannot
pass the anchor.

No-op forced routing, unchanged model buffers, identical held-out token
identity, common checkpoint provenance, same-input CKA, a dimension-matched
Haar overlap null, and diversity of the oracle-best expert are required
guards.  Failure of these guards is Insufficient, not scientific Fail.

## 7. Current Evidence

The completed [E06 audit](/Projects/from-attention-to-search/main/experiments/A15/15_06_online_spectral_routing_and_relay/A15_06_E06_2b_10b_router_expert_specialization_audit/summary.md)
is eligible for a frozen, seed-17 claim and has typed verdict
`mixed_not_supportive`.  At 10B, Local-HMT minus Local-Random regret was
$-0.01042$ nat/token with paired 95% interval $[-0.02878,0.00753]$, while its
score--utility difference was $-0.00022$ with interval
$[-0.01313,0.01278]$.  Relay-HMT minus Relay-Random pointed unfavorably on both
registered quantities: regret $+0.01352$ $[-0.00361,0.03052]$ and
score--utility $-0.01121$ $[-0.02745,0.00481]$.  Neither path passed its
joint interval and Holm-adjusted sign-flip rule.

The functional null is not caused by interchangeable experts.  Across arms,
mean same-input output CKA is $0.326$--$0.335$, forced-expert NLL spread is
$0.467$--$0.505$ nat/token, oracle entropy is $0.996$--$0.997$, and native
best-match rate is about $34\%$ versus $12.5\%$ chance.  Thus experts have
token-conditional functional differences and the Router exploits them
partially; covariance H/M/T identity does not improve that utilization beyond
the matched random bottleneck.

## 8. Claim Boundary And Next Decision

The evidence supports a frozen, single-seed association between expert
non-interchangeability and incomplete Router utilization.  It rejects a
covariance-specific functional certificate at the registered scale.  It does
not establish that specialization caused terminal NLL, that the same result
holds across seeds or scales, that H/M/T have universal semantic meaning, that
random routing is universally superior, or that PCGrad improves training.

This subanchor is complete and does not replace the active A15_07 route.  The
only next A15 decision is whether A15_07 can identify a cross-expression
conditional-fine direction that first passes its semantic certificate and can
then be submitted to a separate expert-utility admission gate.  Completion is
a held-out direction certificate followed by functional admission; resume by
reviewing the six pending A15_07 design choices.
