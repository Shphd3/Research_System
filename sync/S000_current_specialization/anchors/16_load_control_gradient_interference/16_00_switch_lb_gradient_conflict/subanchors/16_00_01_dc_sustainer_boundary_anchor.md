# A16_00_01 DC Sustainer Boundary


## 1. Problem Definition

This subanchor now belongs to the A16_00 load-control mechanism line. It adjudicates one completed local uncertainty: whether the token-shared mean of the actual Router input immediately sustains Vanilla-Full's deep-layer hard-routing collapse and makes the same Switch-style load-balancing objective less able to change winners. A15 training exposed the phenomenon; this migration changes evidence ownership, not the experiment, values, or verdict.

The decision question is: **with tokens, Gate weights, experts, and checkpoints frozen, does removing the true common mean rescue Vanilla routing, and does adding the saved common center back damage Centered routing, beyond equal-size random and wrong-layer shifts?**  This is a root-cause audit of current routing, not a claim about language-model quality or an intervention training result.

## 2. Physical Priors

For a linear Gate, a token-shared input component becomes a token-shared but expert-dependent logit offset.  Such an offset can align one expert's winner margin across many tokens.  The prior is falsified as the primary frozen explanation if true-mean removal is not more effective than matched control shifts, or if Centered is insensitive to adding its saved center back.

## 3. Falsifiable Hypotheses

- **H1, DC necessity:** subtracting an independently estimated layer mean from frozen Vanilla reduces busiest-expert share and increases route entropy more than matched random and wrong-layer shifts.
- **H2, DC sufficiency:** adding the checkpointed running center back to frozen Centered increases busiest-expert share and reduces route entropy more than matched random and wrong-layer shifts.
- **H3, LB saturation mechanism:** collapsed native Vanilla has a high Switch auxiliary value but lower per-token logit-gradient leverage than its centered counterfactual.
- **Strongest rival:** learned Gate geometry or Router--expert feedback, not the common component, is already sufficient for collapse; the registered counterfactuals will then have little or nonspecific effect.

Pass requires H1 and H2 in the registered aggregate.  H1 alone is `necessary_only`; H2 alone is `sufficient_only`; neither is Fail.  Invalid replay, data identity, or missing checkpoint evidence is Insufficient.  H3 is mechanistic support and cannot rescue a failed H1/H2 verdict.

## 4. Mathematical Model

Write the actual pre-center Router source as $h=\mu+\delta$, where $\mu$ is constant across the fixed statistics tokens and $\delta$ is token-varying.  With Gate matrix $W$ and expert-common logit direction removed by $C_E=I-\mathbf 1\mathbf 1^\top/E$,

$$
C_EWh=C_EW\mu+C_EW\delta.
$$

$C_EW\mu$ is the decision-relevant DC offset.  The Switch loss is $L_{LB}=E\sum_e f_e\bar p_e$, where $f_e$ is the hard top-1 token fraction and $\bar p_e$ is the mean soft probability.  Treating $f$ as detached, the sample-scaled derivative is

$$
N\frac{\partial L_{LB}}{\partial z_{t,j}}
=E p_{t,j}\left(f_j-\sum_e f_ep_{t,e}\right).
$$

It can approach zero after probabilities saturate even when $L_{LB}$ remains large.  This relation explains only instantaneous Gate pressure, not the total parameter update after adding the language-model gradient and AdamW state.

## 5. Computational Realization

At fixed seed-17 Vanilla-Full and Centered-Full checkpoints, capture the exact pre-center `gating_reference` for every layer on frozen statistics and validation text.  Fit one independent mean per arm, checkpoint, and layer from the fixed statistics split.  Replay native logits exactly, then change only the constant Router-input component offline:

- Vanilla: raw deployment versus subtracting the independent mean;
- Centered: centered deployment versus adding back its checkpointed running center;
- controls: cyclic wrong-layer shifts and deterministic isotropic shifts matched in decision-relevant logit norm.

Experts never run under counterfactual assignments; the test measures Router decisions only.  Early and late checkpoints expose when the relation appears without treating checkpoints or layers as independent experimental replicates.

## 6. Minimal Falsification Tests

The primary metric is the change in busiest-expert share, the fraction of validation tokens routed to the most-used expert.  For Vanilla, positive rescue is native share minus mean-removed share.  For Centered, positive damage is center-added share minus native share.  The registered aggregate averages the fixed layer-3/layer-4 cells over 50M, 100M, 250M, 500M, 1B, 10B, and 20B token checkpoints.  Documents are the bootstrap unit; layers and checkpoints are fixed repeated views.

Each directional effect must have a paired-document 95% lower bound above zero and exceed the 95th percentile of 256 matched random-shift aggregate effects.  Native logit/winner replay, frozen token hashes, checkpoint identity, and deterministic controls are hard guards.  Normalized route entropy, margins, DC alignment, $L_{LB}$, and analytic LB logit-gradient leverage explain the outcome but do not replace it.

## 7. Current Evidence

Verified training evidence shows the same $0.01$ LB coefficient in all six arms.  At 20B, Vanilla's busiest-expert shares are 49.4%, 66.0%, 99.9%, and 99.8% across layers 1--4, whereas Centered's are 21.3%, 29.3%, 27.0%, and 23.9%.  Vanilla layers 3--4 were already near 99% by roughly 50M tokens.

A16_00_01_E01 completed all 16 registered frozen cells and returned `necessary_only`. Across layers 3--4 and seven nonzero checkpoints, subtracting the independent true mean from Vanilla reduced busiest-expert share by 0.68678, with document-bootstrap 95% CI [0.68435, 0.68922], versus matched-random q95 0.18326. It flipped 72.63% of routes; the DC term favored the deployed winner over its runner-up for 99.75% of tokens. Conversely, adding the saved center to independently trained Centered changed share by 0.14225 [0.14010, 0.14446], below random q95 0.22588 and below the wrong-layer effect on average. The common term therefore immediately sustains current Vanilla collapse, but is not direction-specific sufficiency in Centered's adapted Gate geometry.

The LB mechanism is stage-specific rather than uniformly gradient-dead. Vanilla's LB value remains near its maximum after collapse, while layer-4 local logit leverage becomes small at some saturated checkpoints; layer 3 does not show universal vanishing. Penalty magnitude alone therefore does not diagnose corrective force.

Protocol: [A16_00_01_E01](/Projects/from-attention-to-search/main/experiments/A16/A16_00_01_E01_dc_sustainer_audit/protocol.md)

Result: [Summary](/Projects/from-attention-to-search/main/experiments/A16/A16_00_01_E01_dc_sustainer_audit/summary.md)

## 8. Claim Boundary And Next Decision

This audit establishes a direction-specific immediate dependency of current Vanilla collapse on the true common component. It does not establish cumulative unique causality, language-model benefit of the offline intervention, or the best LB repair. The failed inverse intervention makes a purely static offset story insufficient and retains learned-path adaptation as the strongest remaining explanation.

Exactly one next decision is owned by parent Anchor A16_00: use the already
approved Vanilla/Centered paired gradient and shadow-update result to select
dynamic expert bias, retained differentiable LB, or a hard/soft-control repair.
Resume from the A16_00 parent Anchor and freeze its Protocol before execution.
