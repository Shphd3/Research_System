---
experiment_id: A15_02_06_E05_all_adjacent_depth_transitions
status: AI_DRAFT_AWAITING_HUMAN_CONFIRMATION
date: 2026-08-12
eligibility: ELIGIBLE_REGISTERED_RESULT_WITH_POSTHOC_BOUNDARY_AUDIT
---

# Summary: all adjacent-layer transitions in the frozen Mean Response basis

## Result snapshot

All 35 adjacent transitions were computed using identical Mean Response directions. The normalized F9--F12 transition is significantly heterogeneous across fixed depth positions: after a simultaneous 95% correction over all 35 transitions, 16 are positive, 11 are negative, and 8 are unresolved. Therefore block 8→9's negative result is not a whole-model law.

The registered early/middle/deep means are

| Transition-start stage | Mean \(D_{sem}\) | 95% parent-bootstrap interval | Half A / B |
| --- | ---: | ---: | ---: |
| early, 1--12 | +0.002168 | [+0.001678,+0.002425] | +0.002261 / +0.001986 |
| middle, 13--24 | -0.003779 | [-0.004046,-0.003294] | -0.003831 / -0.003693 |
| deep, 25--35 | +0.007947 | [+0.007512,+0.008050] | +0.008011 / +0.008064 |

The registered deep-minus-early contrast is `+0.005779`, with simultaneous interval `[+0.005019,+0.006539]`. However, the linear depth slope is `−2.27×10⁻⁵` per block with interval `[−4.63×10⁻⁵,+1.27×10⁻⁵]`, so there is no supported monotonic “deeper means more later-spectrum growth” law. The typed outcome is `stage_dependent_nonmonotonic`.

A necessary boundary qualification is that the equal-third stage result is sensitive to the middle/deep cut around the unusually large `24→25` decrease and `25→26` rebound. In a post-hoc ±1-boundary audit, deep-minus-early ranges from `−0.000535` to `+0.006355`. This does not invalidate the registered comparison, but it prevents treating its magnitude or sign as a stable stage law.

Absolute F9--F12 variance growth also changes with depth: mean \(G_{sem}\) falls from `+0.6831` early to `+0.4371` middle and `+0.2545` deep, and all three stage contrasts are simultaneously nonzero. Relative share and raw scale frequently disagree at individual transitions, so neither may substitute for the other.

## Central figures

The eight requested, preselected pairs are shown separately. Their selection is display-only; inference uses all 35 transitions.

![Eight adjacent pairs](figures/figure1_eight_representative_adjacent_pairs.png)

The complete atlas shows that transition signs alternate across depth rather than moving smoothly in one direction.

![All adjacent transitions](figures/figure2_all_adjacent_transition_atlas.png)

The registered stage comparison and non-significant monotonic slope are separated below.

![Depth-difference inference](figures/figure3_depth_difference_inference.png)

## Claim boundary

Can claim: this model, data, hook, common basis, and normalized variance proxy have a reproducible, non-monotonic adjacent-depth profile, with many individually significant positive and negative transitions.

Cannot claim: deeper blocks progressively add finer information, a positive \(D_{sem}\) is new knowledge, F9--F12 is a causal module, or any transition band improves routing. Layers are fixed architecture positions, not independent population replicates.

## One next decision

Human decision required: whether to close total normalized Attention-write variance as the candidate “new information” metric and replace it with a residual-relative, held-out accessibility estimator while keeping one fixed adjacent-layer comparison. Do not select a favorable layer pair or new basis from this atlas.

Evidence: [Protocol](protocol.md), [Detailed](detailed.md), [all transition metrics](tables/transition_metrics.csv), [stage contrasts](tables/depth_contrasts.csv), and [boundary sensitivity](tables/stage_boundary_sensitivity.csv).
