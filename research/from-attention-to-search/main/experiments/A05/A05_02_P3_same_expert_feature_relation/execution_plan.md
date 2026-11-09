# Execution Plan: A05_02_P3_same_expert_feature_relation Same-Expert Feature Relation

Anchor: `Projects/from-attention-to-search/main/problem_anchors/05_failure_mechanism/05_02_feature_assumption_relaxation_anchor.md`

Approved protocol: `protocol_for_approval.md`

## 1. Run Goal

P3 asks whether same-expert features share family structure more than load-matched random grouping.

## 2. Data Construction

Use \(G=4\) families, \(K=4\) features per family, \(F=16\), \(E=4\), uniform distribution.

P3a:
Input contains family tokens and feature tokens. Each feature predicts its own target \(Y_{gk}\).

P3b:
Input contains the same family and feature tokens. Features in the same family share target \(Y_g\).

## 3. System / Evaluation Setup

Train with full-sequence next-token prediction. Record route at the last \(F_{gk}\) token position, immediately before target prediction.

## 4. Configs And Commands

Code workspace:
`Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments`

Config:
`active/synthetic_data_understanding/configs/h0605c_same_expert_feature_relation.json`

Command:

```bash
python active/synthetic_data_understanding/scripts/run_h0605bc_feature_assumption_relaxation.py \
  --experiment p3 \
  --config active/synthetic_data_understanding/configs/h0605c_same_expert_feature_relation.json \
  --run-name h0605c_same_expert_feature_relation_full_20260604 \
  --run-stage full \
  --max-parallel 2
```

Actual visible GPUs: 2 H100 GPUs. The user requested a 4-card task, but this runtime exposed only 2 GPUs through `nvidia-smi`.

## 5. Metrics And Artifacts

Primary metric:
Family purity over load-matched random baseline, \(\Delta_{\mathrm{family}}\).

Why it decides:
It directly asks whether same-expert features share family more than expected from the observed expert loads.

Validity metrics:
target accuracy, active experts, expert max-load fraction, load entropy.

## 6. Stage Audit

| Stage | Local Question | Input Evidence | Pass / Fail Rule | Debug Artifact | Handoff |
| --- | --- | --- | --- | --- | --- |
| data | Are P3a/P3b separated correctly? | target construction and config | P3a uses \(Y_{gk}\), P3b uses \(Y_g\) | `resolved_config.json` | detailed |
| training | Does target prediction learn? | target accuracy and target CE | accuracy near 1.0 | `training_curve_by_seed.csv` | summary |
| grouping | Is family grouping above random? | purity table | positive and seed-stable \(\Delta_{\mathrm{family}}\) | `family_relation_by_seed.csv` | summary |
| figures | Are required visuals present? | figure folder | all required figures exist | `figures/` | report card |

## 7. Pass / Fail Criteria

P3a positive if input-side family alone gives seed-stable positive family purity over random under non-collapse.

P3b positive if shared family target gives stronger seed-stable family purity over random than P3a under non-collapse.

Both negative if deltas are small, seed-unstable, or explained by collapse.

Invalid if target learning fails.

## 8. Failure Modes To Check

- collapse false positive.
- load artifact.
- one-seed family grouping that does not replicate.
- shared target causing easier prediction without routing structure.

## 9. Result Location

Curated result:
`Projects/from-attention-to-search/main/experiments/A05/A05_02_P3_same_expert_feature_relation/`

Raw run output:
`Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/results/h0605c_same_expert_feature_relation/h0605c_same_expert_feature_relation_full_20260604/`
