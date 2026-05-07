# Analysis v6.6 Paper-Ready Integrated Report

## 0. Scope

- 执行目录：`/data/250010109/spectral_router/exp_quadratic_proportion/output/analysis_v6.6_paper_ready_20260407`
- 目标：在 `v6.6` 主线下完成 Round1-5 的 paper-ready 口径复跑，并给出可直接交付理论分析的结构化结论。
- 关键口径：中等规模、可复现、带进度监控，不追求最大规模。

## 1. 执行配置与步骤

### 1.1 Round1 Token Decoupling & Expert Assignment

- 步骤：
  1. 固定 WoS 样本清单（`max_samples=1200`）。
  2. 执行 function/domain 词表单-token清洗。
  3. 在 `linear_running_center` / `acp_lite` / `hybrid` 上统计 token assignment 与 hybrid 三项 logit 记录。
- 输出：
  - `round1/summary_round1.json`
  - `round1/token_group_assignment.json`
  - `round1/hybrid_logit_components.jsonl`

### 1.2 Round2 Specialization Metric Tracking

- 步骤：
  1. 对四模型提取各层 `x_c` 与 expert assignment（`max_samples=1200`，`max_tokens_per_layer=30000`）。
  2. 按层计算 `rho_sep` 与 `sRank`。
  3. 聚合跨层均值。
- 输出：
  - `round2/rho_sep_srank_report.json`
  - `round2/summary_round2.md`

### 1.3 Round3 Empirical Separation & Subspace Audit

- 步骤：
  1. 在 `1/3/5/7/9/11` 六层提取去均值激活（`target_tokens_per_layer=12000`）。
  2. 各层独立执行 KMeans 与 K-Subspaces。
  3. 对比 `rho_sep` 与 `avg_sRank`。
- 输出：
  - `round3/summary_round3.json`
  - `round3/summary_cross_model.md`
  - 每层 `kmeans_vs_ksubspaces_metrics.json`

### 1.4 Round4 Routing Logit Dynamics

- 步骤：
  1. 从随机初始化 `step0` 训练 hybrid（`train_steps=100`）。
  2. 逐步记录 mean/centered/subspace 三项 logit 均值方差与梯度 L2。
  3. 统计 `ratio_sub_to_first_order_grad` 序列。
- 输出：
  - `round4/logit_dynamics_stepwise.jsonl`
  - `round4/summary_round4.json`

### 1.5 Round5 Overhead Audit

- 步骤：
  1. 六模型统一 checkpoint、固定 batch/token 设置。
  2. 统计总参数、router参数、router FLOPs/token。
  3. 统计 warmup 后 wall-clock latency（`measure_iters=12`）。
- 输出：
  - `round5/params_flops_latency_table.json`
  - `round5/summary_round5.md`

## 2. 关键结果

### 2.1 Round1

| 指标 | 数值 |
| --- | ---: |
| 样本量 | 1200 |
| function 单token保留 | 43/44 |
| domain 单token保留 | 109/127 |
| function top-share 均值（linear/acp/hybrid） | 0.5778 / 0.6036 / 0.6094 |

hybrid 分项绝对 logit（按 token group）显示：`subspace` 项量级显著大于一阶项，function/domain/mixed 三组均如此。

### 2.2 Round2

| Model | rho_sep_mean | sRank_mean |
| --- | ---: | ---: |
| linear_no_center | 0.006024 | 30.305109 |
| linear_running_center | 0.061512 | 55.334178 |
| acp_lite | 0.101529 | 66.092753 |
| hybrid | 0.064503 | 43.766388 |

`acp_lite` 在 separation 上最强；`linear_no_center` 依然是分离能力最弱的反例。

### 2.3 Round3

跨模型六层均值（来自 `summary_cross_model.md` 聚合）：

| Model | KMeans rho | KSubspaces rho | KMeans sRank | KSubspaces sRank | KMeans rho > KSubspaces rho |
| --- | ---: | ---: | ---: | ---: | ---: |
| linear_running_center | 0.257289 | 0.072623 | 63.664634 | 66.557462 | 6/6 |
| acp_lite | 0.359459 | 0.107409 | 63.340858 | 68.974256 | 6/6 |
| hybrid | 0.435242 | 0.104338 | 57.325770 | 64.934151 | 6/6 |

在本次口径下，三模型均表现为 `rho_sep(KMeans) > rho_sep(K-Subspaces)`，且 `K-Subspaces` 未稳定给出更低 `sRank`。

### 2.4 Round4

| 指标 | 数值 |
| --- | ---: |
| train_steps | 100 |
| final_loss | 7.6999 |
| final_grad(mean/centered/subspace) | 3.26e-4 / 1.13e-3 / 2.01e-3 |
| ratio_sub_to_first_order_grad 区间 | [0.2756, 2.0896] |
| ratio_sub_to_first_order_grad 均值/中位数 | 0.8685 / 0.8183 |

结论：二阶分支未呈现“全程被饿死”，但训练中存在明显竞争与波动。

### 2.5 Round5

| Model | Router Params | Router FLOPs/token | Latency(ms) |
| --- | ---: | ---: | ---: |
| quadratic_low_rank | 7.08M | 1.180M | 35.603±0.819 |
| hybrid | 7.23M | 1.196M | 36.605±0.460 |
| linear_nocenter_lb001 | 73.7K | 6.1K | 33.265±3.346 |
| acp_lite | 221.2K | 15.4K | 32.751±0.402 |
| linear_running_center | 73.7K | 6.1K | 30.926±0.469 |
| linear_no_center | 73.7K | 6.1K | 26.282±0.402 |

二阶/混合路线在复杂度上显著高于线性路线，工程代价真实存在。

## 3. 面向 v6.6 主线的综合分析

### 3.1 支持点

- 与 v6.6 主线一致：`acp_lite` 仍是强一阶 comparator，说明 mean-dominant 条件下一阶路线仍强。
- Round3 在当前口径进一步把证据推向 mean-separable 解释，H1 获得增强支持。
- Round4 显示“二阶分支并未系统性饿死”，使 H2 更偏向“竞争存在但非单边压制”。
- Round5 完成 FLOPs/latency 实证回应，为 reviewer 开销问题提供直接证据。

### 3.2 我对不同模型的评估

- `linear_no_center`：稳定反例。其低 `rho_sep` 与历史 collapse 叙事一致，不应作为主线方案。
- `linear_running_center`：干净 baseline，几何上更稳，仍是必保对照组。
- `acp_lite`：当前最强一阶 comparator，在 separation 维度反复占优；论文里必须正面承认其强度。
- `hybrid`：在某些层的 KMeans 指标更激进，但尚未形成“跨层一致、跨指标一致”的几何优势证据。
- `quadratic_low_rank`：开销高于线性族，价值取决于是否在特定 regime 提供可复现实益。

### 3.3 我的顾虑

- 统计稳健性仍不足：本轮为单 seed 口径，尚未给出 bootstrap CI 与多 seed 稳健性。
- Round3 指标与“子空间更优”假设存在张力：当前证据更偏 mean-separable，H3 仍需更强支撑。
- Round4 仍是短程训练观察：能否外推到真实长程训练还不充分。
- 开销叙事需更严谨：尽管 latency 差距在本机不大，但 FLOPs/params 差异客观存在，必须强调 regime-specific 收益抵偿。

## 4. 假设更新（v6.6 对齐）

- H1/H7：增强支持。
- H2：更新为“竞争存在但非单边压制”。
- H3/H5：仍为部分支持，尚不足以形成强几何结论。
- H8：仍待词频分层补证。
- regime-dependent necessity：支持增强，但应继续避免 universal claim。

## 5. 下一步（最小增量）

1. Round2/3 增加 bootstrap CI。  
2. Round4 增加 2-3 个 seed 复跑。  
3. Round1 增加 function-word 词频分层。  
4. 在状态文档中显式标注“paper-ready 中等规模口径已完成”。  
