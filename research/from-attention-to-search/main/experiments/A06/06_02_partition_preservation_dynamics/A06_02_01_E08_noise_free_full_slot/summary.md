# Summary: A06_02_01_E08 Noise-Free Full-Slot Preservation

Primary anchor:
`../../../../problem_anchors/06_geometry_proxy_preservation/06_02_partition_preservation_dynamics/06_02_partition_preservation_dynamics_anchor.md`

Protocol: `protocol.md`

## Result Snapshot

Verdict: **supported as a synthetic necessity check for the background-noise hypothesis.**

What we established: when every token position is feature-bearing, ideal feature-center router initialization is preserved through 2000 full-sequence LM steps. This sharply differs from the mixed-slot full-LM setting where oracle/route centers lost positive low-tail margin by step 2000.

What the experiment shows: in the no-background full-slot sequence, all three ideal-center variants keep all-position feature NMI at 1.000 and final margin p05 at about 4.566. The random router control does not recover a stable feature partition and remains negative-margin.

What we do next: treat background/non-feature positions as a necessary component of the previous mixed full-LM erosion, then run a graded signal/noise margin-budget audit before claiming the complete mechanism.

## Purpose

A06_01_05_E04/A06_02_02_E04 showed that under mixed full-sequence LM training, even clean oracle/route-center initialization can lose positive margin after long training. This run tests a direct rival explanation: maybe the previous erosion was driven by background-token gradients rather than by router dynamics alone.

## Terminology / Definitions

| Term | Plain meaning | Concrete object / computation | Unit or formula | Why it matters | Cannot prove |
| --- | --- | --- | --- | --- | --- |
| No-background full-slot sequence | Every token in the sequence is the feature token | \(x=(F_f,\ldots,F_f)\), length 32 | token sequence | Removes neutral/background positions | Real-text behavior |
| Full-LM loss | Predict every next token | CE over positions 0 to 30 | loss | Matches the all-position objective form | Utility or semantics |
| Ideal center initialization | Router rows initialized from label-known feature centers | mean hidden states by feature | router rows | Tests preservation from a clean start | Label-free method |
| All-position feature NMI | Agreement between feature id and routed expert over all token positions | NMI(feature, expert) | 0 to 1 | Primary partition metric | Margin or utility |
| Margin p05 | Low-tail matched expert score gap | 5th percentile target-vs-competitor score gap | router-logit gap | Preservation guard | Correct prediction |

## Exact Setup

Data: four uniformly sampled features. A sample with feature \(f\) is:

\[
x=(F_f,F_f,\ldots,F_f),\qquad |x|=32.
\]

There are no neutral/background tokens. Calibration and evaluation use balanced features; training batches sample features uniformly.

Model: one causal Transformer layer plus one weighted top-1 MoE layer, four experts, hidden size 64, four attention heads, expert FFN size 128.

Objective: full next-token LM loss over positions 0 to 30.

Conditions: random router, oracle all-position centers, oracle predictive-position centers, and oracle last-predictive-position centers.

Training: 8 seeds, 2000 steps, batch size 256, checkpoints 0/160/500/1000/2000, AdamW learning rate 0.002, weight decay 0.0001.

Result path: `Projects/from-attention-to-search/main/experiments/A06/06_02_partition_preservation_dynamics/A06_02_01_E08_noise_free_full_slot/`.

## Primary Result

At step 2000:

| Condition | All-position feature NMI | Margin p05 | Matched preserve | Positive margin frac | Next-token accuracy |
| --- | ---: | ---: | ---: | ---: | ---: |
| oracle all-position centers | 1.000 | 4.566 | 1.000 | 1.000 | 1.000 |
| oracle predictive-position centers | 1.000 | 4.566 | 1.000 | 1.000 | 1.000 |
| oracle last-predictive-position centers | 1.000 | 4.566 | 1.000 | 1.000 | 1.000 |
| random router | 0.789 | -2.964 | 0.594 | 0.594 | 1.000 |

The ideal-center result passes the primary preservation test: NMI remains perfect and low-tail margin remains positive after long full-LM training.

## Key Evidence

Step-0 and final comparison:

| Condition | Step-0 NMI | Step-0 margin p05 | Step-2000 NMI | Step-2000 margin p05 |
| --- | ---: | ---: | ---: | ---: |
| oracle all-position centers | 1.000 | 11.515 | 1.000 | 4.566 |
| oracle predictive-position centers | 1.000 | 11.515 | 1.000 | 4.566 |
| oracle last-predictive-position centers | 1.000 | 11.515 | 1.000 | 4.566 |
| random router | 0.789 | -1.003 | 0.789 | -2.964 |

The oracle margin becomes thinner early but does not cross zero. By step 2000 it remains safely positive in all ideal-center variants.

## Key Figures

### Figure: Margin p05 Trajectory

![Margin p05 trajectory](figures/margin_p05_trajectory.png)

What this tests: whether the low-tail matched route margin crosses below zero during long no-background full-LM training.

How to read: values above zero mean the matched expert still beats the strongest competitor for the low-tail token positions.

Observed result: all three oracle center variants remain positive through 2000 steps. Random remains negative.

Take-home: no-background full-slot data preserves ideal feature routing under the same long full-LM training length.

What it does not prove: background noise is the only mechanism in mixed full-LM erosion.

### Figure: All-Position Feature NMI

![All-position feature NMI trajectory](figures/allpos_feature_nmi_trajectory.png)

What this tests: whether routed expert identity remains aligned with feature identity across all token positions.

Observed result: ideal-center conditions stay at 1.000. Random stays below perfect and does not become a stable margin-positive partition.

## Interpretation

Observation: removing background tokens changes the long-train outcome. In the mixed A06_01_05_E04 long-train run, oracle centers ended at feature NMI 0.845 and margin p05 -5.359. Here, oracle centers end at feature NMI 1.000 and margin p05 4.566.

Interpretation: background/non-feature positions are a necessary part of the prior synthetic full-LM margin-erosion surface. The previous failure should not be explained only as "top-1 always destroys ideal centers" or "long training always erodes margins."

Claim update: the background-gradient hypothesis is supported as a root-cause direction, but not closed. The next mechanism question is how much background fraction, background token diversity, and feature/background loss weight are needed to flip the margin sign.

## Claim Boundary

Can claim:

- In the no-background full-slot synthetic setting, ideal center initialization is preserved through 2000 full-LM steps.
- The previous mixed full-LM ideal-center erosion is not reproduced when every supervised position is feature-bearing.
- Background/non-feature positions are a necessary mechanism candidate for the mixed-setting failure.

Cannot claim:

- Background gradients are the only cause of mixed full-LM erosion.
- Real-DCLM preservation follows from this synthetic result.
- The preserved feature partition has expert utility.
- Label-free discovery is solved; the run uses oracle feature centers.

## Next Decision

Run a graded background-ratio margin-budget audit: start from full-slot no-background data and gradually add neutral/background positions while measuring the cumulative correct-signal, background-signal, router-drift, and hidden-drift contributions to margin.

