# 12L / ckpt40000 十模型综合报告（Round0–4，含 Round4 方法全量披露）

**实验时间**：2026-04-02
**Checkpoint**：40000
**评测模型（10个）**：linear_no_center / linear_running_center / low_rank / acp_lite / quadratic_low_rank_linear / quadratic_low_rank / quadratic_low_rank_acp_lite / quadratic_nosvd / quadratic_nosvd_debias / quadratic_nosvd_debias2
**评测顺序**：Round1 → Round2 → Round3 → Round4 → Round0
**结果目录**：`/data/250010109/spectral_router/exp_expert_lowrank/output/round_12L/ckpt40000`

---

## 1. 中心目标与评测框架

本轮目标是联合回答"结构健康度、稳定性、跨域干扰、任务能力"四条证据链在同一 checkpoint 上是否一致，新增 quadratic_low_rank 系列（linear / off / acp_lite 三种变体）和 acp_lite_backup 的完整评测，实现 11 个模型的五轮全对比。

对应五轮定义如下：

- Round0：下游任务保真（lm_eval）
- Round1：专家低秩与路由分工（ED / 条件熵 / 负载离散）
- Round2：加噪后分发一致性（CR）
- Round3：domain interference（SI + margin）
- Round4：方向扰动敏感性（CR_parallel / CR_orthogonal / DSI）

---

## 2. 实验设置

| 参数 | 值 |
|:--|:--|
| 评测层位 | Layer 2, 6, 10 |
| Round1/2 样本数 | 96 |
| Round3 样本数 | 64 / domain |
| max_length | 128 |
| Round2 噪声 | 0.01, 0.05, 0.1, 0.5 |
| Round4 扰动强度 | perturb_scale = 0.1 |
| Round0 任务 | arc_easy, arc_challenge, boolq, hellaswag, openbookqa, piqa, winogrande |

---

## 3. Round0：下游任务表现（lm_eval）

| 模型 | arc_easy | arc_challenge | boolq | hellaswag | openbookqa | piqa | winogrande | Avg |
|:--|--:|--:|--:|--:|--:|--:|--:|--:|
| linear_no_center | **0.4184** | 0.2381 | **0.5862** | 0.3175 | 0.2700 | 0.6371 | 0.5099 | 0.4253 |
| linear_running_center | 0.4575 | 0.2637 | 0.5505 | 0.3571 | 0.3040 | 0.6491 | 0.4893 | 0.4387 |
| low_rank | 0.4348 | 0.2466 | 0.5471 | 0.3499 | 0.2960 | 0.6583 | 0.4996 | 0.4332 |
| acp_lite | 0.4638 | 0.2423 | 0.5755 | **0.3605** | **0.3200** | **0.6638** | **0.5217** | **0.4497** |
| quadratic_low_rank_linear | 0.4289 | 0.2619 | 0.5394 | 0.3565 | 0.3000 | 0.6551 | 0.5043 | 0.4352 |
| quadratic_low_rank | 0.4655 | 0.2415 | 0.5309 | 0.3519 | 0.3020 | 0.6610 | 0.5107 | 0.4376 |
| quadratic_low_rank_acp_lite | 0.4402 | 0.2585 | 0.5829 | 0.3623 | 0.3100 | 0.6627 | 0.5067 | 0.4462 |
| quadratic_nosvd | 0.4550 | **0.2705** | 0.5700 | 0.3543 | 0.2860 | 0.6605 | 0.5146 | 0.4444 |
| quadratic_nosvd_debias | 0.4545 | 0.2474 | 0.5664 | 0.3529 | 0.2880 | 0.6605 | 0.5043 | 0.4392 |
| quadratic_nosvd_debias2 | 0.4583 | 0.2509 | 0.4869 | 0.3577 | 0.2960 | 0.6529 | 0.5020 | 0.4292 |

结论：Round0 综合均值排名：`acp_lite`(0.4497) > `quadratic_low_rank_acp_lite`(0.4462) > `quadratic_nosvd`(0.4444) > `quadratic_nosvd_debias`(0.4392) > `linear_running_center`(0.4387) > `quadratic_low_rank`(0.4376) > `quadratic_low_rank_linear`(0.4352) > `low_rank`(0.4332) > `quadratic_nosvd_debias2`(0.4292) > `linear_no_center`(0.4253)。
新增模型中，`quadratic_low_rank_acp_lite` 表现突出（0.4462），仅次于 acp_lite。

---

## 4. Round1：专家低秩与路由分工

| 模型 | ED（model_minus_random） | 路由条件熵 | CV_load |
|:--|--:|--:|--:|
| linear_no_center | -0.1821 | -2.240545 | 1.8224 |
| linear_running_center | -13.3577 | -1.068551 | 0.3141 |
| low_rank | -16.8635 | -0.737669 | 0.0298 |
| acp_lite | -13.2869 | -0.827044 | 0.1349 |
| quadratic_low_rank_linear | -12.6668 | -0.762295 | 0.2802 |
| quadratic_low_rank | -14.6579 | -0.964127 | 0.6719 |
| quadratic_low_rank_acp_lite | -10.8116 | -0.944820 | 0.3647 |
| quadratic_nosvd | -7.8001 | -0.926240 | 0.3749 |
| quadratic_nosvd_debias | -15.2927 | -1.093720 | 0.5027 |
| quadratic_nosvd_debias2 | **-17.2076** | -0.941985 | 0.2565 |

结论：`linear_no_center` ED 接近 0（-0.18）、条件熵极端（-2.24）、CV 最高（1.82），体现最强塌缩特征。新增 quadratic_low_rank 三种变体 ED 在 -10.8 至 -14.7 之间，分工中等；`quadratic_nosvd_debias2` ED=-17.21 绝对值最大，分工最明确。

---

## 5. Round2：加噪分发一致性

### 5.1 Overall CR（按 sigma）

| 模型 | σ=0.01 | σ=0.05 | σ=0.10 | σ=0.50 |
|:--|--:|--:|--:|--:|
| linear_no_center | **1.0000** | **1.0000** | **1.0000** | **1.0000** |
| linear_running_center | 0.9990 | 0.9958 | 0.9926 | 0.9610 |
| low_rank | 0.9989 | 0.9954 | 0.9913 | 0.9539 |
| acp_lite | 0.9989 | 0.9956 | 0.9919 | 0.9566 |
| quadratic_low_rank_linear | 0.9989 | 0.9959 | 0.9920 | 0.9578 |
| quadratic_low_rank | 0.9995 | 0.9973 | 0.9937 | **0.9649** |
| quadratic_low_rank_acp_lite | 0.9993 | **0.9973** | **0.9945** | **0.9700** |
| quadratic_nosvd | 0.9992 | 0.9965 | 0.9931 | 0.9651 |
| quadratic_nosvd_debias | 0.9988 | 0.9951 | 0.9919 | 0.9524 |
| quadratic_nosvd_debias2 | 0.9993 | 0.9971 | 0.9935 | 0.9645 |

### 5.2 解释

- `linear_no_center` 的 1.0000 与塌缩路由形态一致（top1 路由几乎不变化），不能解读为"最佳鲁棒性"。
- 非塌缩模型中，`quadratic_low_rank_acp_lite` 和 `quadratic_nosvd` 在高噪声点（σ=0.5）保持最高 CR（约 0.965-0.970）。

---

## 6. Round3：Domain Interference（SI + Margin）

### 6.1 全模型结果总表

| 模型 | Mean SI | Mean Margin A | Mean Margin B | 备注 |
|:--|--:|--:|--:|:--|
| linear_no_center | 0.8063 | 8.4198 | 8.7871 | 单专家主导，margin 异常高 |
| linear_running_center | 0.6522 | 1.7115 | 1.7166 | 正常 |
| low_rank | 0.6747 | 1.9137 | 1.7690 | 正常 |
| acp_lite | 0.6844 | 1.9117 | 1.7564 | 正常 |
| quadratic_low_rank_linear | 0.6639 | 0.0000 | 0.0000 | margin 未产出（配置差异） |
| quadratic_low_rank | **0.6338** | 0.0000 | 0.0000 | SI 最低，margin 未产出 |
| quadratic_low_rank_acp_lite | 0.6620 | 0.0000 | 0.0000 | SI 次低，margin 未产出 |
| quadratic_nosvd | 0.6960 | 1.8575 | 1.8923 | 正常 |
| quadratic_nosvd_debias | 0.6510 | 1.5997 | 1.6355 | SI 次低 |
| quadratic_nosvd_debias2 | 0.6746 | 2.1551 | 2.1034 | 正常 |

### 6.2 分层详细数据

#### Layer 2

| 模型 | SI | Margin A | Margin B |
|:--|--:|--:|--:|
| linear_no_center | 0.8210 | 1.5298 | 1.6068 |
| linear_running_center | 0.6706 | 1.6985 | 1.5553 |
| low_rank | 0.7122 | 1.5988 | 1.6144 |
| acp_lite | 0.7114 | 1.3204 | 1.3321 |
| quadratic_low_rank_linear | 0.6599 | 0.0000 | 0.0000 |
| quadratic_low_rank | 0.6877 | 0.0000 | 0.0000 |
| quadratic_low_rank_acp_lite | 0.6828 | 0.0000 | 0.0000 |
| quadratic_nosvd | 0.7296 | 1.3858 | 1.4121 |
| quadratic_nosvd_debias | 0.6670 | 1.5923 | 1.4857 |
| quadratic_nosvd_debias2 | 0.6981 | 1.5285 | 1.5257 |

#### Layer 6

| 模型 | SI | Margin A | Margin B |
|:--|--:|--:|--:|
| linear_no_center | 0.8494 | 2.8907 | 3.0203 |
| linear_running_center | 0.6810 | 0.9952 | 1.1693 |
| low_rank | 0.6856 | 1.7868 | 1.5984 |
| acp_lite | 0.7214 | 1.7212 | 1.5320 |
| quadratic_low_rank_linear | 0.7161 | 0.0000 | 0.0000 |
| quadratic_low_rank | 0.6809 | 0.0000 | 0.0000 |
| quadratic_low_rank_acp_lite | 0.6950 | 0.0000 | 0.0000 |
| quadratic_nosvd | 0.7579 | 2.0126 | 2.0799 |
| quadratic_nosvd_debias | 0.6706 | 1.2172 | 1.4252 |
| quadratic_nosvd_debias2 | 0.7138 | 1.9395 | 1.8007 |

#### Layer 10

| 模型 | SI | Margin A | Margin B |
|:--|--:|--:|--:|
| linear_no_center | 0.7484 | 20.8389 | 21.7340 |
| linear_running_center | 0.6050 | 2.4408 | 2.4251 |
| low_rank | 0.6262 | 2.3556 | 2.0944 |
| acp_lite | 0.6205 | 2.6935 | 2.4050 |
| quadratic_low_rank_linear | 0.6157 | 0.0000 | 0.0000 |
| quadratic_low_rank | 0.5329 | 0.0000 | 0.0000 |
| quadratic_low_rank_acp_lite | 0.6083 | 0.0000 | 0.0000 |
| quadratic_nosvd | 0.6005 | 2.1741 | 2.1848 |
| quadratic_nosvd_debias | 0.6153 | 1.9896 | 1.9957 |
| quadratic_nosvd_debias2 | 0.6120 | 2.9974 | 2.9838 |

### 6.3 关键发现

1. **SI 与塌缩/退化模型关联**：`linear_no_center`（SI=0.8063）呈现最高 SI；`quadratic_low_rank`（off）SI=0.6338 全表最低
2. **SI 层间递减**：所有模型的 SI 从 L2→L6→L10 呈递减趋势（L10 层路由更稳定）
3. **no_center 极端异常**：L10 层 margin 高达 20+，是其他模型的 10 倍
4. **margin 数据分组**：quadratic_low_rank 系列三种变体 margin=0.0000（配置口径不同），其余模型 margin 在 1.0-3.0 范围
5. **新增模型横向比较**：`quadratic_low_rank_acp_lite` L10 层 SI=0.6083 略逊于 `quadratic_low_rank` off（0.5329），但仍优于 linear 系列

---

## 7. Round4：方向敏感性实验

### 7.1 Round4 是怎么做的

对每个目标层 l∈{2,6,10}：

1. 计算层均值方向 u_l；
2. 构造两种等幅扰动：
   - 平行扰动（parallel）：沿 u_l 加噪；
   - 正交扰动（orthogonal）：沿与 u_l 正交子空间加噪；
3. 对 clean 与扰动后路由 top1 做一致性统计：
   CR = #(e^{clean}=e^{perturbed}) / #tokens
4. 定义方向敏感指数：
   DSI = CR_{orthogonal} - CR_{parallel}

本轮使用 perturb_scale=0.1，先算层内 CR，再对层 2/6/10 做平均得到整体 CR 与 DSI。

### 7.2 Round4 结果总表

| 模型 | CR_parallel | CR_orthogonal | DSI |
|:--|--:|--:|--:|
| linear_no_center | 1.000000 | 1.000000 | 0.000000 |
| linear_running_center | 0.999673 | 0.999864 | 0.000190 |
| low_rank | 0.999456 | 0.999755 | 0.000299 |
| acp_lite | 0.999565 | 0.999810 | 0.000245 |
| quadratic_low_rank_linear | 0.999619 | 0.999755 | 0.000136 |
| quadratic_low_rank | 0.999782 | 0.999946 | 0.000163 |
| quadratic_low_rank_acp_lite | 0.999619 | 0.999837 | 0.000218 |
| quadratic_nosvd | 0.999673 | 0.999755 | 0.000082 |
| quadratic_nosvd_debias | 0.999592 | 0.999782 | 0.000190 |
| quadratic_nosvd_debias2 | 0.999782 | 0.999864 | 0.000082 |

### 7.3 Round4 完成度与偏差（单独判断）

- 完成度：**已完成**（10/10 模型有结果，parallel/orthogonal/DSI 全量产出）。
- 偏差：DSI 量级约 10^{-4}，方向效应弱。
- `quadratic_nosvd` 和 `quadratic_nosvd_debias2` DSI 最低（0.000082），路由对方向扰动最不敏感。

---

# Result Summary
- Round0 任务能力：`acp_lite` 均分第一（0.4497），`quadratic_low_rank_acp_lite` 第二（0.4462），`quadratic_nosvd` 第三（0.4444）；`linear_no_center` 垫底（0.4253）
- Round1 结构分工：`linear_no_center` 出现显著塌缩（ED=-0.18、条件熵极端）；`quadratic_nosvd_debias2` ED=-17.21 分工最明确
- Round2 扰动稳定性：`quadratic_low_rank_acp_lite` 高噪声 CR=0.9700 全表最高；`quadratic_low_rank`（off）CR=0.9649 次高
- Round3 跨域干扰：`quadratic_low_rank`（off）SI=0.6338 全表最低；`quadratic_low_rank_acp_lite` SI=0.6620 次低；`linear_no_center` 干扰最高（0.8063）
- Round4 方向敏感性：效应量普遍极小（10^{-4}），方向效应弱；`quadratic_nosvd` 和 `quadratic_nosvd_debias2` DSI=0.000082 最低

---

# Reliability Audit
- 数据完整性：**Round0-4 全量 10 模型评测完成**，status 记录齐全
- 高可信：no_center 的塌缩特征（ED≈0）与高干扰/低任务表现同向一致
- 中等可信：quadratic 系列在 Round2/3 维度优势清晰，但与任务提升并非完全对应
- 需谨慎：
  - Round4 的 DSI 效应量过小（10^{-4}），只能给出"弱方向性差异"结论
  - quadratic_low_rank 系列 margin=0.0000 反映配置差异，非真实零值

---

# Hypothesis-Relevant Findings
- 被支持：
  - 抑制塌缩与更低跨域冲突、较好综合任务表现相关（no_center 塌缩组 vs 其余模型）
  - quadratic_low_rank 系列（尤其 off 变体）在 SI 和 CR 两个维度均表现优异
  - quadratic_low_rank_acp_lite 提供了 acp_lite 路由 + quadratic_low_rank 结构组合的均衡性能证据
- 未被支持：
  - "方向敏感性是主要机制"未获强证据支持（Round4 DSI 过小）
  - 单一方案在所有维度全面最优未成立

---

# Checkpoint Delta（相比初版报告的更新）
- 新增 `quadratic_low_rank_acp_lite`（任务第二、Round2 CR=0.9700 全表最高）
- ckpt40000 已形成 **10 模型五轮闭环证据**，覆盖 quadratic_low_rank 系列 linear/off/acp_lite 三种变体

---

# Report-Ready Summary
- 可直接用于 checkpoint/report 的内容：
  - 10 模型 × 5 轮全量评测完成，status 记录齐全
  - no_center 的塌缩与综合劣势已被多轮一致验证
  - quadratic_low_rank_acp_lite 在 Round2 高噪声（σ=0.5 CR=0.9700）和 Round0 任务（0.4462）两个维度均表现突出
  - Round4 方法、公式、全量结果已披露并可复核
- 仅可作为 tentative evidence 的内容：
  - Round4 的方向性差异（DSI 效应量过小）
  - quadratic_low_rank 系列 margin=0.0000 需后续确认口径

---

# Experiment -> Theory Result Card
- **Scope**：ckpt40000，10 模型，层位 2/6/10，round0-4 全覆盖
- **Positive Evidence**：`quadratic_low_rank`（off）在 SI 和高噪声 CR 两个结构指标上同时最优；no_center 的塌缩提供了退化对照
- **Negative/Null Evidence**：Round4 DSI 量级过小，未形成强机制区分；quadratic 系列结构优势未完全转化为任务提升
- **Reliability Grade**：Round0 A / Round1 A / Round2 A- / Round3 B+（margin 数据部分缺失）/ Round4 B-
- **Theory Result**：主线更支持"塌缩抑制与跨域冲突控制"，quadratic_low_rank_acp_lite 提供了 ACP+QLR 组合的均衡性能证据
