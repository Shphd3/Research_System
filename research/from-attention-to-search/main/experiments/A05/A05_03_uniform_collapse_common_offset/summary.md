# Result Summary: A05_03_uniform_collapse_common_offset

Anchor: `../../../problem_anchors/05_failure_mechanism/05_03_uniform_collapse_common_offset_anchor.md`

Story: P0-P7 test whether uniform-feature collapse is initiated by a shared hidden component acting as an expert-specific common offset, and whether offset control or anti-lock-in training reduces collapse.

## 0. Closure Summary

Purpose: explain why a bias-free linear top-1 router collapses even after feature frequencies and random router initialization are verified.

Hypothesis / question: if hidden states decompose as \(h_f=c+r_f\), then \(w_e^T c\) acts like an expert-specific effective bias. The expert with the largest common score should dominate at step 0, and top-1 training can amplify that early advantage.

Conclusion: P0-P7 support the common-offset account for **step-0 collapse** and support training-amplified lock-in for **final collapse**. P6A auxiliary load-balance warmup is the strongest tested anti-lock-in control. The result is not a full solution.

Key evidence: common-score argmax predicts the step-0 dominant expert with agreement 1.0 across repeated and distributed-complex patterns, versus a random baseline of 0.25. Dot-product common-offset cancellation reduces step-0 max-load from about 0.62-0.63 to about 0.28-0.29. P6A keeps collapse rate 0.0 with mean final max-load 0.499 on repeated and 0.523 on distributed-complex patterns.

Claim boundary: P3 was CPU-shortened; P4-P7 used `cuda:0` with 2 visible H100 GPUs, not full 4-card verification. Lower max-load is not specialization, and P7 shows post-training route-utility co-adaptation rather than proving early utility causality.

Next decision: run full 4-card verification of baseline full hidden, P5B logit common-offset cancellation, P4-I4 residual-subspace initialization, and P6A auxiliary load-balance warmup.

## Observation

P1/P2 show that \(w_e^T c\) predicts the step-0 dominant expert. Removing or canceling the common offset makes step-0 routing close to balanced.

P3/P4/P5 show that offset control helps but does not by itself guarantee stable final routing across seeds.

P6 shows that a training-time anti-lock-in pressure is stronger than offset-only controls in the shortened runs.

P7 shows that after training, router-chosen experts usually match the forced-routing best expert. This means final collapsed models should not be described as obviously utility-wrong.

## Interpretation

The safest mechanism statement is:

\[
common\ hidden\ component \rightarrow expert\ common\ score \rightarrow early\ dominant\ expert \rightarrow top\text{-}1\ amplified\ lock\text{-}in
\]

The common offset explains the early selection; top-1 amplification explains why final collapse can return even after early balancing.

## Operationalization Boundary

This result supports: common-offset as the strongest current step-0 mechanism.

This result does not support: "subtracting the common offset solves collapse" or "load balance equals feature specialization."

Tested operationalization: uniform features, repeated and distributed-complex slot patterns, 3 seeds, 400-step shortened runs, dot-product and cosine diagnostics, and forced-routing utility after training.

Alternative operationalizations still open: full 4-card verification, longer training, feature-structure readout after P6A, and early forced-utility dynamics.

## Limitation

The run is a mechanism audit, not a final training benchmark. P0-P3 were initially run on CPU due local CUDA unavailability; P4-P7 ran on `cuda:0` with two H100 GPUs visible. No claim should depend on full 4-card completion yet.

## Key Figures

![P1/P2 common source prediction](figures/p1_p2_common_source_prediction.png)

Supports: common-score argmax predicts the step-0 dominant expert and common cancellation reduces initial load.

![P3 seed-level training load and accuracy](figures/p3_seed_level_training_load_accuracy.png)

Supports: common-offset cancellation reduces hard collapse but final load remains seed-dependent.

![Remaining protocol variant heatmap](figures/remaining_protocol_variant_heatmap.png)

Supports: P6A is the strongest tested final-load control among P4-P6.

![Selected remaining methods by seed](figures/remaining_selected_methods_by_seed.png)

Supports: P6A improves seed-level max-load while preserving accuracy.

![P7 utility aggregate](figures/remaining_p7_utility_aggregate.png)

Supports: post-training route choice and forced-routing best expert are highly aligned.

## Claim Update

- Supported: common-offset drives step-0 dominant expert selection.
- Supported: final collapse needs training-amplified lock-in in addition to early offset.
- Supported: P6A is the strongest tested control in shortened runs.
- Still unclear: whether P6A holds under full 4-card verification and whether it creates meaningful feature specialization.

## What Cannot Be Claimed

Do not claim collapse is solved, utility mismatch is proven, lower load equals specialization, or the result transfers to compositional or real data.

## Next Decision

Run full 4-card verification for baseline, P5B, P4-I4, and P6A. Use final max-load and collapse rate as the primary decision metrics; use target accuracy as a validity guard.
