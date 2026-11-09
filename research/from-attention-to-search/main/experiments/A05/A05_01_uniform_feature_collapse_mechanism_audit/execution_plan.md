# A05_01 Uniform Feature Collapse Mechanism Audit - Execution Plan

## 目标

审计原始 uniform feature 设定中的路由坍缩：最终坍缩 expert 是由初始化/早期几何已经决定，还是训练中经由 top-1 routing 放大后锁定。

## 边界

- 不引入 compositional feature 数据。
- 不增加新数据集或新 broad experiment。
- 优先审计已有 H0605a 日志与 checkpoint 覆盖。
- 原始日志缺少 step 10/20/50 的模型态；因此对这些早期点使用同配置 diagnostic replay，仅用于 hidden/router 几何审计。
- 不声称 utility mismatch，除非 forced-routing utility matrix 被单独分析。

## 原始设定

- 来源实验：`A05_01_true_token_conditioned_inhibition_replay`
- 原始 raw result：
  `Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/results/h0605a_true_token_conditioned_inhibition_replay/h0605a_true_token_conditioned_inhibition_replay_4gpu_20260604`
- features：exact feature `(slot, B_i)`；图中主要使用 slot-aggregated heatmap，完整 exact-feature 汇总保存在表中。
- conditions：`R0-dot`, `R1-dot`, `S0-dot`, `S1-dot`, `R0-cos`, `R1-cos`, `S0-cos`, `S1-cos`
- seeds：`20260521`, `20260522`, `20260523`
- audit checkpoints：`0, 10, 20, 50, 100, 200, 800, 1600`
- collapse guard：`max_load_fraction >= 0.95` 或 `active_experts <= 1`

## 审计项目

1. route load over checkpoints：判断坍缩是 step 0、early step 还是 late step。
2. feature-to-expert assignment timeline：判断 exact/slot feature 是否早期就集中到最终 expert。
3. feature centroid x router-vector cosine：判断 feature hidden centroid 与 router vector 的早期关系。
4. top-1 margin dynamics：判断 top-1 选择置信度是否被训练放大。
5. common-direction alignment：判断最终坍缩 expert 是否更贴近全局共同 hidden 方向。
6. router vector geometry：判断 router vector 是否发生分离、norm/movement 是否放大。

## 输出

- `summary.md`：第一阅读入口。
- `detailed.md`：完整设置、表格、图、解释边界。
- `figures/`：六张主图与一个 router pairwise 辅助图。
- `tables/`：seed-level metrics 与 checkpoint-level tables。
