# Execution Plan: E2.3 Router Behavior Decomposition

## 1. Run Goal

Diagnose what the learned top-1 router uses to choose experts in E2: feature identity, prefix-end token shortcut, hidden scale, target confidence/difficulty, low-variance router-relevant directions, or shared-path bypass.

## 2. Data Construction

Use existing E2 all-trigram data and checkpoints first.

Required sample table per position:

```text
sample_id
seed
variant                     # moe_top1_no_lb / moe_top1_lb
is_feature_prefix
feature_id                  # ABC / DEF / GHI / JKL / background
A_token
B_token
target_token
feature_count
position_index
hidden_norm
router_logits[4]
router_margin
router_entropy
selected_expert
lm_logits[target]
target_prob
ce_loss
pca_coords[k]
router_weight_projections[4]
```

Recommended matched samples:

- all feature prefix-end positions;
- equal number of background positions matched by token frequency;
- equal number matched by hidden norm bucket;
- equal number matched by CE/loss bucket.

Shortcut control dataset for second phase:

```text
shared_B:
  [1,2] -> 22
  [3,2] -> 23
shared_target:
  [1,2] -> 22
  [3,4] -> 22
frequency_crossed:
  swap feature frequencies across token identities
```

## 3. Model / Training / Evaluation Setup

Phase 1: no training.

- Load E2 trained checkpoints.
- Extract router input hidden states and router logits.
- Fit explanatory models on frozen samples.

Phase 2: optional new data / retraining only if token shortcut remains plausible.

- Generate crossed-feature corpus.
- Train same MoE config as E2.
- Repeat Phase 1 decomposition.

## 4. Configs And Commands

Expected new script:

```bash
python active/synthetic_data_understanding/scripts/analyze_router_behavior_decomposition.py \
  --e2-out-dir active/synthetic_data_understanding/outputs/e2_augmented_all_trigram_v1000 \
  --data-path active/synthetic_data_understanding/data_all_trigram_v1000/four_feature_all_trigram_v1000_tokens.txt \
  --data-config active/synthetic_data_understanding/configs/e1_all_trigram_v1000.json \
  --out-dir active/synthetic_data_understanding/outputs/e2_3_router_behavior_decomposition \
  --fig-dir active/synthetic_data_understanding/figures/e2_3_router_behavior_decomposition \
  --variants moe_top1_no_lb,moe_top1_lb \
  --pca-dims 16 \
  --matched-background 1
```

Optional crossed-feature run:

```bash
python active/synthetic_data_understanding/scripts/generate_synthetic_patterns.py \
  --config active/synthetic_data_understanding/configs/e2_3_crossed_feature_data.json \
  --out-dir active/synthetic_data_understanding/data_e2_3_crossed_feature

python active/synthetic_data_understanding/scripts/train_moe_feature_separation.py \
  --run-config active/synthetic_data_understanding/configs/e2_3_crossed_feature_moe.json

python active/synthetic_data_understanding/scripts/analyze_router_behavior_decomposition.py \
  --e2-out-dir active/synthetic_data_understanding/outputs/e2_3_crossed_feature_moe \
  --data-path active/synthetic_data_understanding/data_e2_3_crossed_feature/tokens.txt \
  --data-config active/synthetic_data_understanding/configs/e2_3_crossed_feature_data.json \
  --out-dir active/synthetic_data_understanding/outputs/e2_3_crossed_feature_router_decomposition \
  --fig-dir active/synthetic_data_understanding/figures/e2_3_crossed_feature_router_decomposition \
  --variants moe_top1_no_lb,moe_top1_lb
```

## 5. Metrics And Artifacts

Tables:

```text
router_behavior_sample_table.csv
expert_id_predictor_summary.csv
conditional_permutation_importance.csv
mutual_information_table.csv
within_bucket_feature_effect.csv
projection_intervention_summary.csv
expert_path_necessity_summary.csv
```

Figures:

```text
expert_predictor_nll_by_variable_group.png
conditional_importance_bar.png
feature_vs_token_explanation.png
norm_ce_router_assignment_scatter.png
feature_subspace_vs_router_subspace_ablation.png
learned_vs_oracle_vs_random_routing_readback.png
```

## 6. Pass / Fail Criteria

Supports `representation separability != router specialization` if:

- feature linear probe from `h` is high;
- feature-only predictor does not best explain expert id after controls;
- router assignment is better predicted by B token, norm, CE/margin, or router projection dimensions;
- projecting out feature subspace changes feature probe more than expert assignment;
- oracle feature routing does not significantly improve CE/readback over learned routing.

Supports `shortcut design` if:

- B-token-only predictor nearly matches full hidden predictor;
- crossed shared-B design breaks routing alignment or readback;
- feature separability is mostly token identity separability.

Supports `shared path bypass` if:

- random/mean/zero MoE output preserves readback;
- feature target logit contribution mainly comes from residual/LM head path;
- weakening shared path increases expert ablation drop and feature-aligned routing.

## 7. Failure Modes To Check

- Background sampling accidentally changes frequency distribution.
- Feature labels are perfectly collinear with B token in the original design.
- CE/margin are downstream consequences rather than causal router variables.
- Linear probes overstate separability because they use information unavailable to the trained router objective.
- Oracle routing proves recoverability, not learned-router success.
- Synthetic trigram evidence does not transfer to real language.

## 8. Result Location

```text
main/experiments/E0_E3_synthetic_data_understanding/stages/E2_moe_feature_separation/versions/E2_3_router_behavior_decomposition/
  purpose_card.md
  execution_plan.md
  summary.md
  detailed.md
  figures/
```
