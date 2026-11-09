# Summary: A09_01 Common High-Gain Band / Rare Discrimination

Primary anchor: `../../../problem_anchors/09_common_rare_spectral_discrimination/09_01_common_band_rare_discrimination_anchor.md`

Protocol: `protocol.md`

## Purpose

This run tests one mechanism:

> A common high-gain band can take much of the score while rare residual directions carry the useful discrimination.

The experiment asks whether a common/rare split reduces that mismatch while keeping common performance.

## Exact Setup

Data is controlled and synthetic. Each example has 4 common groups and 4 rare subclasses. The hidden vector is

\[
h = 2.6c_i + 0.85r_{i,j} + \epsilon,\qquad \epsilon\sim \mathcal{N}(0,0.55^2).
\]

Training is common-heavy: default common subclass count is 4096 per common group; each rare subclass count is 96. Evaluation uses matched rare pairs: correct rare target `y` versus same-common default distractor `d`.

Models use linear heads trained with AdamW, 900 steps, batch size 256, learning rate 0.03, weight decay 0.0001, 8 seeds.

## Primary Metric

The primary metric is

\[
G_{mis}(k)=C_{score}(k)-C_{disc}(k).
\]

\(C_{score}\) means how much matched-pair score magnitude comes from the baseline high-gain band.

\(C_{disc}\) means how much correct-target-versus-distractor discrimination comes from that band.

Positive \(G_{mis}\) means the band is loud but not equally useful for rare discrimination.

## Result

The controlled mechanism is supported.

At audit rank 4, the shared baseline has a large mismatch:

- baseline \(G_{mis}=0.486\);
- baseline \(C_{score}=0.819\);
- baseline \(C_{disc}=0.332\).

The estimated common/rare split removes the mismatch and improves rare loss:

- estimated split \(G_{mis}\approx 0.000\);
- \(\Delta G_{mis}=0.486\);
- rare loss improves by 0.996;
- system common loss is preserved: 0.006 versus baseline 0.009.

The controls matter:

- random split improves rare loss more, but keeps high mismatch and breaks common loss;
- oracle split also removes mismatch;
- shuffled rare labels remove mismatch but do not improve rare loss.

So the claim is not "lower loss means specialization." The supported claim is narrower: a split must reduce mismatch, improve rare loss, and preserve common performance together.

## Central Figure

![A09 decision metrics](figures/a09_decision_metrics_short_labels.png)

**What this figure tests:** Whether each condition moves the mechanism metric, rare function, and common guard together.

**How to read it:** Lower mismatch is better, lower rare loss is better, and low system common loss means common behavior is preserved.

**Observed result:** Estimated split and oracle split remove mismatch and keep common loss low. Random split lowers rare loss but breaks common loss and does not reduce mismatch. Shuffled guard removes mismatch but rare loss worsens.

**Take-home:** The mechanism is identified only by the joint pattern, not by rare loss alone.

**What it does not prove:** Real language semantics, real-DCLM preservation, or a deployable MoE method.

## Claim Boundary

Can claim:

- On controlled data, a common high-gain band can be a measurable rare-discrimination failure mode.
- A common/rare split can reduce that mismatch while preserving common behavior.

Cannot claim:

- real semantic experts;
- real-DCLM utility;
- final preservation method;
- scaling behavior.

## Next Decision

Use this as a controlled positive mechanism result. The next anchor should test whether an analogous mismatch can be measured on real model activations before claiming real expert utility.
