---
experiment_id: A16_00_01_E01_dc_sustainer_audit
legacy_experiment_id: A15_00_E04_vanilla_centered_lb_dc_audit
status: complete
scientific_verdict: necessary_only
last_updated: 2026-08-09
---

# A16_00_01_E01 final result summary

## Direct conclusion

The registered frozen audit yields **`necessary_only`**.  The independently
estimated token-shared mean is a direction-specific immediate sustainer of
Vanilla-Full's frozen deep-layer collapse: removing it reduces the busiest
expert's share by 0.68678 on average over the registered layer/checkpoint
cells, far beyond equal-size random shifts.  The inverse intervention does not
pass: adding the saved center to a separately trained Centered-Full Router
changes concentration, but less than generic matched shifts.  Centering
therefore changed the learned path; a common offset is not, by itself, a
universal sufficient cause of collapse for arbitrary trained Gate geometry.

This answers why identical \(\lambda_{LB}=0.01\) did not imply identical expert
use: the objectives were the same, but Vanilla exposed a coherent expert-
relative DC logit offset that rapidly aligned winners, whereas Centered did
not.  It does **not** yet identify whether language-model gradients, LB
gradients, AdamW state, or expert feedback created that alignment.

## Registered decision

The **busiest-expert share** is the fraction of validation tokens assigned to
the most-used of eight experts; 0.125 is uniform and 1.0 is single-expert
routing.  A positive effect means that removing the mean rescues Vanilla or
adding the center damages Centered.

| Frozen direction | Mean effect | Paired-document 95% CI | Matched-random q95 | Decision |
| --- | ---: | ---: | ---: | --- |
| Vanilla: remove independent mean | 0.68678 | [0.68435, 0.68922] | 0.18326 | passes necessity direction |
| Centered: add saved center | 0.14225 | [0.14010, 0.14446] | 0.22588 | fails sufficiency direction |

The Vanilla effect exceeds all 256 aggregate random shifts.  The Centered
effect exceeds only 6.64% of them and is smaller than the cyclic wrong-layer
control on average.  Thus a nonzero Centered response cannot be attributed
specifically to its covariance-derived center.

![Registered direction-specific counterfactual](figures/figure2_registered_effect_vs_random_null.png)

## What happens over training

By about 50M tokens, native Vanilla layers 3/4 already route 98.7%/97.8% of
tokens to one expert.  At about 100M tokens they reach 99.9%/99.9%; removing
the independently fitted mean immediately lowers these shares to 27.7%/30.0%.
At 20B, removal still lowers 99.9%/99.8% to 20.5%/21.5%.

Across the 14 primary cells, mean removal flips 72.63% of Vanilla routes.  The
true DC term favors the deployed winner over its runner-up for 99.75% of
tokens, and its cell-level median contribution is about 1.09 times the final
native margin.  A ratio above one means the token-varying residual often
partly opposes the common offset rather than creating the winner.

![Checkpoint trajectory](figures/figure1_route_concentration_counterfactual.png)

## What the LB diagnostics do and do not show

The **Switch LB value** is 1 under ideal uniform use and approaches 8 when one
expert owns all tokens and the soft probabilities agree.  Its analytic
**logit-gradient leverage** is the RMS local derivative through the soft
probabilities, with token-count and the common coefficient factored out for
state comparison.

Vanilla's deep-layer LB value rises toward 8 as collapse forms.  Its local
leverage is high during parts of the 50M--100M transition, but later becomes
small in saturated layer 4 even while the penalty remains near 8.  Layer 3
does not show universal gradient disappearance at 10B/20B.  Therefore the
broad hypothesis "LB is always gradient-dead after collapse" is not supported;
the valid update is narrower: penalty magnitude and corrective leverage are
different, layer- and time-dependent quantities, and a hard top-1 collapse is
not guaranteed to recover merely because the auxiliary value is large.

![LB penalty and local leverage](figures/figure3_lb_penalty_and_gradient_dynamics.png)

## Boundary and one next decision

This frozen Router audit establishes immediate dependence of the current
Vanilla collapse on the true common component.  It does not establish the
historical unique cause, execute counterfactual experts, measure NLL benefit,
or justify increasing the LB coefficient.

The one next decision is owned by A16_00: run a paired early gradient and
shadow-update audit.  Its primary metric asks whether adding the LB gradient
from an otherwise identical AdamW state worsens one-step NLL on independent
text; the mechanism metric is the raw language-model versus LB gradient cosine
over the complete global batch.  Dynamic expert bias becomes the first
intervention only if held-out cost, improved hard load, and opposing gradient
direction occur together.
