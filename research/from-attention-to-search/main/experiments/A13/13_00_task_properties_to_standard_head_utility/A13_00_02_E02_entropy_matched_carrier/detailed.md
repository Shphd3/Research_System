# A13_00_02_E02 Detailed Evidence

## 1. Setup

Sequence:

```text
[BOS] [FIXED] [A] [B] [RELAY] [ANSWER] [A]
```

Data: 256 unique \((A,B)\) pairs over 16 values; 204 train and 52 held-out
pairs under \((A+2B)\bmod5=0\), with zero overlap. Data SHA-256:
`20de1e96d5c9c44bc5d7a119f4d8779af41a7936189bcdf2c0bfa5b80c405db5`.

Model/training: width 64, four heads, FFN width 256, cosine learning rate
0.003 to 0.0001, 3,000 steps, seeds 1301--1305. Only all-position NTP was
active.

## 2. Registered Gate Results

| Gate object | Aggregate | Threshold | Verdict |
| --- | ---: | ---: | --- |
| two-layer relay mean accuracy | 0.9846 | \(\ge0.95\) | pass |
| two-layer relay seeds \(\ge0.90\) | 5/5 | \(\ge4/5\) | pass |
| one-layer relay mean accuracy | 0.0577 | \(\le0.15\) | pass |
| one-layer bypass mean accuracy | 1.0000 | \(\ge0.95\) | pass |
| \(A\) counterfactual follow | 0.9769 | \(\ge0.90\) | pass |
| nuisance-\(B\) prediction invariance | 0.9808 | \(\ge0.90\) | pass |
| different-label donor follow | 1.0000 | \(\ge0.90\) | pass |
| same-label donor preservation | 0.9962 | \(\ge0.95\) | pass |

All six carrier gates passed.

## 3. Seed-Level Capability

Two-layer relay final accuracies were 0.9423, 1.0000, 1.0000, 0.9808, and
1.0000. The corresponding first checkpoints at or above 95% were steps 2,220,
200, 360, 860, and 260. Thus four of five seeds crossed 95% by step 1,000;
this fact was used before objective results to freeze the Stage-1 AULC horizon
at 1,000.

## 4. Entropy-Matching Audit

Shared-aux predicts \(x_1,\ldots,x_5\); Next-2 predicts
\(x_2,\ldots,x_6\). The shared-only boundary \(x_1=[\mathrm{FIXED}]\) and
Next-2-only boundary \(x_6=A\) both have zero Bayes uncertainty at their intended
prediction states. Across the full five terms, each objective contains two
independent value targets and three deterministic structural targets.

This matches conditional-entropy sums, not the complete gradient distribution.

## 5. Artifact Map

- [Final metrics](tables/final_metrics.csv)
- [Input counterfactual audit](tables/counterfactual_audit.csv)
- [Relay patch audit](tables/relay_patch_audit.csv)
- [Trajectory figure](figures/carrier_trajectory.png)
- Raw execution directory:
  `XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/outputs/a13_00_02_e02_entropy_matched_full_20260716`

Runtime: 144.1 seconds on `cuda:0`.

## 6. Claim Boundary

The exact carrier is valid, learnable by NTP, nontrivial, and causally used by
the ordinary head. It does not show that Next-2 is useful, isolate pure
semantic information from horizon, or transfer to code, language, long
context, planning, or MoE.
