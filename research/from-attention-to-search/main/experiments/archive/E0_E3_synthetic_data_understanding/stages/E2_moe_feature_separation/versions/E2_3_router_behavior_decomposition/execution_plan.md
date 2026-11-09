# Execution Plan: E2.3 Router Behavior Decomposition

## 1. Run Goal

本实验先不重训模型。第一阶段只读取 E2 已训练 MoE checkpoint，抽取 router input hidden states、router logits、expert choices 和 target prediction signals。

目标是回答：

```text
learned router 的 expert choice 到底更像由 feature identity 决定，
还是由 token shortcut、hidden scale、prediction difficulty/confidence、
router-specific hidden directions 决定？
```

## 2. Phase Design

### Phase A: Frozen-checkpoint decomposition

必做。读取 E2 checkpoints，不训练新模型。

任务：

1. 收集 feature prefix-end positions 与 matched background positions。
2. 为每个样本记录 feature、token、hidden、router、loss、confidence 等变量。
3. 训练若干简单解释模型，比较哪类变量最能预测 `selected_expert`。
4. 做 feature-subspace / router-subspace projection intervention，检查 router 是否使用 feature-separating directions。

### Phase B: Expert-path necessity check

建议与 Phase A 同轮做，仍然不必重训。

任务：

1. learned routing：使用原始 router。
2. oracle feature routing：人为规定 feature 到 expert。
3. random matched routing：随机选 expert，但匹配总体 expert load。
4. zero / mean-replaced expert output：削弱 expert path。
5. 比较 feature readback、CE loss、target probability 是否变化。

### Phase C: Crossed-feature control

第二轮再做，只有当 Phase A 显示 token shortcut 风险高时执行。

构造示例：

```text
shared_B:
  [1,2] -> 22
  [3,2] -> 23

shared_target:
  [1,2] -> 22
  [3,4] -> 22

frequency_crossed:
  same feature rules, swapped frequencies across token identities
```

目的：排除“router 只是看 B token 或 target token”的解释。

## 3. Data And Sample Construction

使用现有 E2 all-trigram 数据和 checkpoints：

```text
dataset = four_feature_all_trigram_v1000
features = ABC / DEF / GHI / JKL
variants = moe_top1_no_lb / moe_top1_lb
seeds = 20260513-20260517
position = prefix-end token, e.g. B in [A,B] -> C
```

样本分三类：

- feature prefix samples：真实 planted feature 的 prefix-end positions；
- matched background samples：非 feature positions，但按 token frequency / hidden norm / CE loss 匹配；
- optional hard negatives：token 相似但不是 planted feature 的 positions。

每个样本至少记录：

```text
sample_id
seed
variant
is_feature_prefix
feature_id
A_token
B_token
target_token
feature_count
position_index
hidden_state
hidden_norm
router_logits[4]
router_margin
router_entropy
selected_expert
target_prob
ce_loss
pca_coords[16]
router_weight_projections[4]
```

## 4. Predictor Groups

这些不是复杂模型，而是“解释变量组”。每组变量都尝试预测 `selected_expert`。

| Predictor group | 中文解释 | 它在问什么 |
|---|---|---|
| majority baseline | 永远猜最常用 expert | 任何解释模型都必须超过这个基线 |
| random-load baseline | 按总体 expert 使用比例随机猜 | 检查结果是否只是 expert load 不均匀 |
| feature-only | 只用 ABC / DEF / GHI / JKL | router 是否按人工 feature 分 |
| B-token-only | 只用 prefix-end token | router 是否只看最后一个 prefix token |
| target-token-only | 只用要预测的 target token | router 是否按目标 token 分 |
| A+B-token | 用完整 prefix token pair | router 是否看上下文组合 |
| frequency-only | 只用 feature 出现频率 | router 是否按高频/低频分 |
| norm-only | 只用 hidden norm | router 是否按 hidden 向量大小分 |
| difficulty-only | 用 CE loss / target probability / margin | router 是否按预测难度或置信度分 |
| PCA-only | 用 PCA 前几个坐标 | router 是否沿可视化主方向分 |
| router-projection | 用 router weight projections | router 是否沿 router 自己敏感的方向分 |
| full hidden linear probe | 用完整 hidden state 的线性分类器 | expert choice 是否可由 hidden state 线性读出 |
| combined model | 所有变量一起放入 | 哪些变量在互相控制后仍有独立解释力 |

## 5. Metrics

指标含义见 `metric_glossary.md`。执行时至少输出：

```text
expert-id prediction accuracy
expert-id NLL
McFadden pseudo-R2
mutual information with selected_expert
conditional permutation importance
within-B-token feature effect
within-norm-bucket feature effect
within-CE-bucket feature effect
feature linear probe accuracy
assignment stability after feature-subspace projection
assignment stability after router-subspace projection
learned vs oracle vs random routing readback
expert-path necessity score
```

## 6. Planned Tables

```text
router_behavior_sample_table.csv
predictor_group_summary.csv
conditional_permutation_importance.csv
mutual_information_table.csv
within_bucket_feature_effect.csv
projection_intervention_summary.csv
routing_counterfactual_readback.csv
expert_path_necessity_summary.csv
```

## 7. Planned Figures

```text
predictor_accuracy_by_variable_group.png
predictor_nll_by_variable_group.png
conditional_importance_bar.png
feature_vs_token_explanation.png
norm_ce_router_assignment_scatter.png
feature_subspace_vs_router_subspace_projection.png
learned_vs_oracle_vs_random_routing_readback.png
expert_path_necessity.png
```

每张图都必须放入：

```text
main/experiments/E0_E3_synthetic_data_understanding/stages/E2_moe_feature_separation/versions/E2_3_router_behavior_decomposition/figures/
```

并在结果 `summary.md` 中用相对路径引用。

## 8. Expected Script Interface

计划新增脚本：

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

注意：这是待执行接口。你确认 plan 后再实现和运行。

## 9. Decision Criteria

### Supports feature-based routing

满足以下现象：

- `feature-only` 明显强于 token、norm、difficulty；
- 控制 `B_token`、hidden norm、CE loss 后，`feature_id` 仍有高 conditional importance；
- 去掉 feature subspace 会明显改变 expert assignment；
- oracle feature routing 能提高 readback 或 CE。

结论：router 确实主要按人工 feature 分 expert，只是不一定严格 one-feature-one-expert。

### Supports token shortcut

满足以下现象：

- `B-token-only` 或 `target-token-only` 接近 full hidden predictor；
- 控制 token 后，`feature_id` 的独立作用很小；
- crossed-feature shared-B control 中 routing alignment 明显变化。

结论：当前 E2 的 routing alignment 可能混入 token shortcut，不能直接解释为完整 context relation specialization。

### Supports scale / difficulty routing

满足以下现象：

- hidden norm、CE loss、target probability 或 margin 比 feature_id 更能预测 expert choice；
- 在相同 norm/CE bucket 内，feature effect 明显减弱；
- router assignment 与 confidence/difficulty 呈稳定关系。

结论：router 更像按“样本强弱或难度”分 expert，而不是按 feature family 分 expert。

### Supports router-specific direction

满足以下现象：

- PCA 坐标解释力弱，但 router projection 解释力强；
- 去掉 feature subspace 不改变 expert choice；
- 去掉 router boundary subspace 明显改变 expert choice。

结论：router 使用的是自己权重敏感的方向，不是 PCA 图里最显眼的 feature direction。

### Supports expert-path non-necessity

满足以下现象：

- learned、oracle、random routing 的 readback / CE 接近；
- zero 或 mean-replaced expert output 不显著破坏 feature readback；
- feature-oracle routing 让分配更干净，但不明显改善 NTP loss。

结论：clean one-feature-one-expert 不是当前任务的必要解。

## 10. Failure Modes To Check

- 原始 E2 中 `feature_id` 与 `B_token` 近似绑定，容易把 token shortcut 误判成 feature routing。
- CE loss 和 target probability 是训练结果，不一定是 router 的因果输入，只能先当相关解释。
- PCA 可视化不能证明线性可分，必须配合 feature linear probe。
- Oracle routing 只能说明“某种分配可行”，不能说明 learned router 应该自然学到它。
- Synthetic trigram 的结果不能直接推广到真实语言语义。

## 11. Result Location

计划结果位置：

```text
main/experiments/E0_E3_synthetic_data_understanding/stages/E2_moe_feature_separation/versions/E2_3_router_behavior_decomposition/
  README.md
  purpose_card.md
  metric_glossary.md
  execution_plan.md
  summary.md          # after run
  detailed.md         # after run
  figures/            # after run
```

运行产物位置：

```text
XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/outputs/e2_3_router_behavior_decomposition/
XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/figures/e2_3_router_behavior_decomposition/
```

## 12. Stop Condition Before Running

执行前需要你确认两点：

1. 第一轮是否只做 frozen-checkpoint decomposition，不重训；
2. 是否把 crossed-feature shared-B control 放到 E2.4，而不是混入 E2.3 第一轮。
