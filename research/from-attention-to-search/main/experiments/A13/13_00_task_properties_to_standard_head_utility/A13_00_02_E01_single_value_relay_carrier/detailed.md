# A13_00_02_E01 Detailed Evidence

## 1. Setup

Sequence:

```text
[BOS] [A] [B] [random selector] [RELAY] [ANSWER] [A]
```

Data: all 512 \((A,B,Q)\) triples over 16 values and two selector markers; 409
train and 103 held-out triples with zero overlap.

Model/training: width 64, four heads, FFN width 256, cosine learning rate
0.003 to 0.0001, 3,000 steps, five registered seeds. Only all-position NTP was
active.

## 2. Registered Gate Results

| Gate object | Aggregate | Verdict |
| --- | ---: | --- |
| two-layer relay answer accuracy | 1.0000 | pass |
| one-layer bypass answer accuracy | 1.0000 | pass |
| one-layer relay answer accuracy | 0.0583 | pass negative control |
| \(A\) counterfactual follow | 1.0000 | pass |
| nuisance-\(B\) invariance | 1.0000 | pass |
| different-label donor follow | 1.0000 | pass |
| same-label donor preservation | 1.0000 | pass |

All six carrier gates passed.

## 3. Causal Reading

The one-layer relay cannot reach evidence under the fixed graph and stayed at
chance. The two-layer relay solved unseen triples, changed its answer when
\(A\) changed, ignored \(B\), and followed the label encoded in a donor relay
state. This jointly rejects direct-edge, nuisance-correlation, and mere-linear-
readability explanations on this carrier.

## 4. Why This Version Was Not Used for Objective Comparison

Shared-aux predicts label set \(x_1,\ldots,x_5\) and Next-2 predicts
\(x_2,\ldots,x_6\). Here \(x_1=A\) is unpredictable from `[BOS]`, while
\(x_6=A\) is predictable from the relay. The two full auxiliary objectives
therefore have different irreducible target entropy. The carrier result is
valid, but the intended objective contrast is not.

## 5. Artifact Map

- [Final metrics](tables/final_metrics.csv)
- [Input counterfactual audit](tables/counterfactual_audit.csv)
- [Relay patch audit](tables/relay_patch_audit.csv)
- [Trajectory figure](figures/carrier_trajectory.png)
- Raw execution directory:
  `XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/outputs/a13_00_02_e01_single_value_relay_full_20260716`

Runtime: 143.2 seconds on `cuda:0`.

## 6. Claim Boundary

This establishes only carrier validity. It does not establish an MTP effect,
query-conditioned composition, long-distance benefit, code transfer, or MoE
value.
