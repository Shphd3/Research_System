# Protocol: A06_02_01_E08 Noise-Free Full-Slot Preservation

## 0. Approval Snapshot

Approval status: approved by user request; run directly.

Purpose: test whether background-token gradient noise is necessary for the long full-LM margin erosion observed after ideal router initialization.

Primary anchor: `../../../../problem_anchors/06_geometry_proxy_preservation/06_02_partition_preservation_dynamics/06_02_partition_preservation_dynamics_anchor.md`

Anchor decision question: Does removing background-token noise make ideal feature-center routing survive long full-sequence LM training?

Anchor physical prior tested: mixed all-position LM loss may destroy feature routing because many non-feature positions send background gradients.

Anchor core model term tested: matched route margin \(m=(w_a-w_b)^\top h\) under a no-background all-feature sequence.

Anchor falsifier: ideal feature-center initialization still loses positive margin in the no-background full-slot setting.

Experiment role: root-cause audit.

Primary metric from anchor: final all-position feature NMI, guarded by final matched margin p05.

Claim boundary from anchor: can only test the synthetic no-background necessity of background gradient noise; cannot claim real-DCLM behavior or expert utility.

Minimal setup: sequence length 32; every token is the feature token; four uniformly sampled features; one Transformer layer; one weighted top-1 MoE layer; full next-token LM loss.

Basic configuration: 8 seeds, 2000 post-initialization training steps, checkpoints 0/160/500/1000/2000.

Conditions to run: random router, oracle all-position center, oracle predictive-position center, oracle last-predictive-position center.

Pass: ideal-center conditions retain high all-position feature NMI and positive final margin p05.

Fail: ideal-center conditions lose margin p05 or feature NMI despite no background tokens.

Insufficient: step-0 ideal routing fails, target loss does not train, or fewer than 8 seeds complete.

Cannot claim: real-language preservation, semantic expert identity, expert utility, or that background noise is the only cause.

Approval decision: proceed.

## 1. Terminology / Definitions

| Term | Plain meaning | Concrete object / computation | Unit or formula | Why it matters | Cannot prove |
| --- | --- | --- | --- | --- | --- |
| No-background full-slot sequence | Every token in the sequence carries the feature identity | \(x=(F_f,\ldots,F_f)\), length 32 | tokens | Removes neutral/background positions | Real-text behavior |
| Full-LM loss | Predict every next token except after the last position | CE over positions 0 to 30 | loss | Matches the all-position loss form | Semantic utility |
| Ideal center initialization | Router rows initialized from label-known feature centers | mean hidden states by feature | vector rows | Tests preservation after a clean start | Label-free method |
| All-position feature NMI | Agreement between feature id and routed expert over all token positions | NMI(feature, expert) | 0 to 1 | Primary partition metric | Margin or utility |
| Margin p05 | 5th percentile matched expert score gap | target expert score minus strongest competitor | logit gap | Low-tail stability guard | Correct prediction |

## 2. Anchor Alignment

Decision question: Does no-background full-slot training preserve ideal feature routing?

Physical prior tested: background positions are the main source of full-LM gradient noise.

Core model term tested: cumulative change in matched route margin.

Falsifier: ideal center routing fails despite every position being feature-bearing.

Claim boundary: synthetic root-cause audit only.

## 3. Tested Hypothesis

If background-token gradients drive the mixed-setting preservation failure, then the no-background full-slot data should preserve ideal feature-center routing under long full-LM training.

## 4. Rival Explanations

- Selected-expert feedback can still move router rows incorrectly.
- Softmax/router competition can erode matched margins even without background tokens.
- Hidden feature centers can drift during training.
- Experts may learn the repeated-token task without preserving the original routing partition.

## 5. Data / Model / Algorithm / Objective

Data: four features, uniformly sampled. A sample with feature \(f\) is a length-32 sequence containing only token \(F_f\).

Model: same minimal Transformer+weighted-top-1-MoE class used in A06_02_02_E03/A06_01_05_E04.

Objective: full next-token LM loss over positions 0 to 30.

Evaluation: route every token position and compute all-position feature NMI and matched margin.

## 6. Conditions, Seeds, And Checkpoints

| Item | Anchor clause tested | Model term / rival explanation | Why needed | Primary or secondary evidence | Pass | Fail | Insufficient | Figure/table |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| random | guard | random routing baseline | confirms ideal init is necessary | secondary | low NMI | high NMI unexplained | unstable | tables |
| oracle_allpos | main | ideal center under no-background data | direct test | primary | positive final margin | negative final margin | step0 fail | trajectory |
| oracle_predpos | guard | centers from supervised prediction positions | avoids last-position mismatch | secondary | positive final margin | negative final margin | step0 fail | trajectory |
| oracle_lastpred | guard | centers from the final predictive position | closest to old route-position evaluation | secondary | positive final margin | negative final margin | step0 fail | trajectory |

Seeds: 0 to 7.

Checkpoints: 0, 160, 500, 1000, 2000.

## 7. Primary Metric

The primary metric is final all-position feature NMI. It decides whether the feature partition survives over all token positions. Margin p05 is the guard: high NMI with negative low-tail margin is not a stable preserved partition.

## 8. Secondary Metrics

- predictive-position feature NMI;
- last-predictive-position feature NMI;
- matched preserve fraction;
- positive margin fraction;
- sign-flip rate;
- full-LM loss;
- next-token accuracy;
- max load and effective experts.

## 9. Known Good / Known Bad / Known Confusing Cases

Known good: ideal centers should have high step-0 feature NMI.

Known bad: random routing may be imbalanced or accidentally align by chance in a small four-feature setting.

Known confusing: target accuracy can become high even if routing margin is destroyed.

## 10. Stage-Level Profiling Plan

| Stage | Local question | Input evidence | Pass / fail / unclear rule | Debug artifact | Handoff |
| --- | --- | --- | --- | --- | --- |
| step0 | Does ideal center init work? | checkpoint 0 table | NMI high and margin positive | training_trajectory.csv | summary |
| long train | Does no-background full-LM preserve? | checkpoint 2000 table | final margin sign | final table | summary |
| trajectory | When does margin move? | checkpoint trajectory | monotonic or crossing | figure | detailed |

## 11. Algorithm Specification

1. Sample balanced feature labels for calibration/evaluation and random feature labels for training batches.
2. Build full-slot sequences \(x=(F_f,\ldots,F_f)\).
3. Initialize the base model.
4. Compute feature centers from all positions, predictive positions, or final predictive position.
5. Set router rows to equal-norm feature centers.
6. Train with full next-token LM loss for 2000 steps.
7. Evaluate routing metrics at checkpoints.

## 12. Success / Failure / Insufficient Evidence

Supported: ideal-center no-background conditions preserve high feature NMI and positive margin p05 at step 2000.

Weakened: ideal-center no-background conditions lose margin or feature NMI.

Insufficient: step-0 ideal centers do not initialize a clean partition.

## 13. What This Cannot Claim

This run cannot claim that real-text background gradients behave the same way, that preserved routing is useful, or that background noise is the only possible cause of prior margin erosion.

## 14. Review Notes And Protocol Changes

The user explicitly requested direct execution without a separate approval round.

