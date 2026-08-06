# 05_03 Uniform Collapse Common-Offset Anchor

## 0. Thinking Card

Parent problem: ordinary top-1 MoE routing collapses even when feature frequencies are uniform.

Current subproblem: explain why a bias-free linear router still develops a dominant expert in the original uniform feature setting.

Core hypothesis: a shared hidden component creates an expert-specific effective bias $w_e^T c$; top-1 training then amplifies the early winner.

Minimal test: verify data/init, measure common-score prediction, cancel the common offset, and compare anti-lock-in controls.

Current boundary: P0-P7 support common-offset as the step-0 driver and P6A load-balance warmup as the strongest tested control, but not a full solution.

Next decision: run full 4-card verification of baseline, P5B, P4-I4, and P6A before returning to feature-structure claims.

## 1. Problem Definition

Parent problem: route consistency can come from collapse, shortcut, or early lock-in rather than expert specialization.

Sharper subproblem: after auditing data frequency and random router initialization, identify the remaining mechanism that makes one expert dominate under uniform features.

Decision question: does the shared hidden component induce an expert-specific common offset that determines early routing concentration and sets up later collapse?

Not in scope: compositional features, Zipfian frequency, real language data, proof that selected experts are utility-wrong, or a general anti-collapse solution.

## 2. Physical Priors
P1: uniform feature frequency does not imply zero-mean hidden states.
Meaning: fixed positions, template tokens, residual stream offsets, and attention can create a shared component at the routed position.
Could be wrong if: the measured common component is small or unrelated to route load.

P2: a bias-free linear router can still have an effective expert bias.
Meaning: if $h_f=c+r_f$, then $w_e^T c$ shifts all features toward some experts even without a learned bias term.
Could be wrong if: $w_e^T c$ fails to predict early dominant experts.

P3: training collapse is not only initialization imbalance.
Meaning: common-offset control can reduce step-0 concentration, but top-1 training may still re-concentrate load without anti-lock-in pressure.
Could be wrong if: removing common offset alone prevents final collapse across seeds.

## 3. Hypothesis

H1: common-offset predicts the step-0 dominant expert.
Supported if: $\arg\max_e w_e^T c$ matches the step-0 dominant expert across seeds and slot patterns.
Weakened if: agreement is near the random baseline.

H2: common-offset cancellation reduces early concentration without destroying target learning.
Supported if: removing $w_e^T c$ lowers step-0 max load and keeps target accuracy high.
Weakened if: load stays high or accuracy fails.

H3: final collapse requires top-1 amplification beyond the step-0 offset.
Supported if: common-aware initialization or cancellation balances step 0 but final max-load remains seed-dependent, while an early anti-lock-in objective is stronger.
Weakened if: offset cancellation alone reliably solves final collapse.

## 4. Mathematical Model
Objects: $h_f$ is the hidden centroid for feature $f$ at the routed position; $c$ is the mean hidden centroid; $r_f$ is the feature residual; $w_e$ is router row $e$.

Core decomposition:

$$
h_f = c + r_f
$$

Mechanism relation:

$$
z_{f,e}=w_e^T h_f = a_e + b_{f,e}, \quad a_e=w_e^T c,\quad b_{f,e}=w_e^T r_f
$$

Observable metrics: common-score argmax agreement, step-0 max-load, final max-load, collapse rate, load entropy, target accuracy, and forced-routing utility match.

Falsifier: if common-score argmax does not predict step-0 routing, or if common-offset cancellation fails to reduce early load, the common-offset hypothesis is too weak.

## 5. Minimal Tests

Experiment: P0-P2 common-source and common-score audit.
Question: does the shared hidden component explain step-0 dominant expert selection?
Intervention: compare full hidden routing with residual or logit common-offset cancellation.
Primary metric: common-score argmax agreement and step-0 max-load reduction.
Supports: H1/H2 if agreement is 1.0 and load approaches balanced routing.
Weakens: H1/H2 if agreement is near 0.25 or load does not change.

Experiment: P3-P5 offset-control and common-aware initialization.
Question: does controlling the common offset reduce final collapse?
Intervention: logit cancellation, common-orthogonal initialization, residual-subspace initialization, and stable common-subtraction variants.
Primary metric: final max-load and collapse rate under high target accuracy.
Supports: H3 if early load improves but final load remains seed-dependent.
Weakens: H3 if offset control alone reliably prevents final collapse.

Experiment: P6-P7 anti-lock-in and forced-utility diagnostic.
Question: does a training-time anti-lock-in pressure outperform offset-only controls, and is the final route utility-wrong?
Intervention: auxiliary load-balance warmup, dynamic-bias warmup, and forced-routing utility matrix after training.
Primary metric: final max-load, collapse rate, accuracy, and route-utility match rate.
Supports: H3 if P6A is strongest and P7 shows route-expert co-adaptation rather than clear utility mismatch.
Weakens: H3 if utility mismatch alone explains collapse.

## 6. Falsifiable Outcomes

Supported: common-score argmax predicts step-0 dominant expert; common-offset cancellation reduces step-0 load; P6A reduces final concentration more reliably than offset-only controls.

Weakened: data or init bug explains the load; common-offset cancellation has no effect; forced-routing utility shows an unambiguous utility-best expert different from the route expert.

Insufficient evidence: only CPU-shortened runs exist, early hidden states are missing, target accuracy fails, or figures average away seed-level collapse.

## 7. Current Evidence

Observation: P1/P2 show common-score argmax agreement is 1.0 across repeated and distributed-complex patterns, versus a random baseline of 0.25; dot-product logit cancellation lowers step-0 max-load from about 0.62-0.63 to about 0.28-0.29.
Interpretation: $w_e^T c$ is a strong explanation for step-0 dominant expert selection.
Boundary: this is a mechanism diagnostic, not a full training solution.

Observation: P3/P4/P5 reduce hard collapse in several variants, but final training remains seed-dependent; P5B logit cancellation avoids hard collapse in tested shortened runs with final max-load around 0.62-0.67.
Interpretation: controlling the common offset helps but does not fully stop top-1 re-concentration.
Boundary: P3 was CPU-shortened, and P4/P5 were not full 4-card verification.

Observation: P6A auxiliary load-balance warmup gives collapse rate 0.0 with mean final max-load 0.499 on repeated and 0.523 on distributed-complex patterns; P7 route-utility match is about 0.98-0.99 after training.
Interpretation: training-time anti-lock-in is the strongest tested control, and final selected experts are co-adapted with utility rather than clearly utility-wrong.
Boundary: lower load is not feature-level specialization, and P7 does not prove causal utility during early training.

## 8. Claim Boundary And Next Decision

Can claim: in the tested uniform toy setting, common-offset is the best current explanation for step-0 collapse, while final collapse is better explained as common-offset seeded top-1 lock-in; P6A is the strongest tested anti-lock-in control.

Cannot claim: collapse is solved, full 4-card training is verified, load balance equals specialization, selected experts are utility-wrong, or the mechanism transfers directly to compositional or real data.

Next decision: run full 4-card verification comparing baseline full hidden, P5B logit common-offset cancellation, P4-I4 residual-subspace initialization, and P6A auxiliary load-balance warmup.
