# Execution Plan: A05_02_P1_compositional_token_feature_routing Compositional Token Feature Routing

Anchor: `Projects/from-attention-to-search/main/problem_anchors/05_failure_mechanism/05_02_feature_assumption_relaxation_anchor.md`

Approved protocol: `protocol_for_approval.md`

## 1. Run Goal

P1 asks whether routing follows the target-relevant feature axis when the same context contains \(S1\), \(S2\), and nuisance \(B_i\).

## 2. Data Construction

Use three target rules over the same sequence:

- C1: \(Y=Y(S1)\).
- C2: \(Y=Y(S2)\).
- C3: \(Y=Y(S1,S2)\).

All conditions use \(|S1|=4\), \(|S2|=4\), and \(|B_i|=64\).

## 3. System / Evaluation Setup

Train with full-sequence next-token prediction. Record route at the \(B_i\) position, which is the pre-target position.

## 4. Configs And Commands

Code workspace:
`Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments`

Config:
`active/synthetic_data_understanding/configs/h0605b_compositional_token_feature_routing.json`

Command:

```bash
python active/synthetic_data_understanding/scripts/run_h0605bc_feature_assumption_relaxation.py \
  --experiment p1 \
  --config active/synthetic_data_understanding/configs/h0605b_compositional_token_feature_routing.json \
  --run-name h0605b_compositional_token_feature_routing_full_20260604 \
  --run-stage full \
  --max-parallel 2
```

Actual visible GPUs: 2 H100 GPUs. The user requested a 4-card task, but this runtime exposed only 2 GPUs through `nvidia-smi`.

## 5. Metrics And Artifacts

Primary metric:
Normalized mutual information (NMI) between route and \(S1\), \(S2\), \(B_i\), and \((S1,S2)\).

Why it decides:
If routing follows target relevance, the highest NMI should move with the target rule under non-collapse.

Validity metrics:
target accuracy, active experts, expert max-load fraction, load entropy.

## 6. Stage Audit

| Stage | Local Question | Input Evidence | Pass / Fail Rule | Debug Artifact | Handoff |
| --- | --- | --- | --- | --- | --- |
| data | Are C1/C2/C3 built with the same input format? | resolved config and generated batches | same route position and same nuisance \(B_i\) | `resolved_config.json` | detailed |
| training | Does the task learn? | target accuracy and target CE | accuracy near 1.0 | `training_curve_by_seed.csv` | summary |
| routing | Is routing interpretable? | NMI and load metrics | non-collapse before route-axis claim | `summary_by_seed.csv` | summary |
| figures | Are required visuals present? | figure folder | all required figures exist | `figures/` | report card |

## 7. Pass / Fail Criteria

Supported only if C1/C2/C3 all have high target accuracy, non-collapsed routing, and the dominant route axis changes as specified.

Weakened if target learning succeeds but routing collapses or only C3 shows a target-aligned axis.

Invalid if target learning fails.

## 8. Failure Modes To Check

- collapse false positive: consistency is high because one expert handles all features.
- partial concentration: two experts are active but max load remains high.
- fixed-axis routing: the same route axis dominates across C1/C2/C3.
- nuisance routing: route aligns with \(B_i\).

## 9. Result Location

Curated result:
`Projects/from-attention-to-search/main/experiments/A05/A05_02_P1_compositional_token_feature_routing/`

Raw run output:
`Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/results/h0605b_compositional_token_feature_routing/h0605b_compositional_token_feature_routing_full_20260604/`
