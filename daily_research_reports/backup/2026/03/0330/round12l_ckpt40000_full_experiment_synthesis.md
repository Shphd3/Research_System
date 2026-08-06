# 12L / ckpt40000 五轮综合报告（Round0–4，含 Round4 方法全量披露）

**实验时间**：2026-03-30  
**Checkpoint**：40000  
**模型组**：linear_no_center / linear_running_center / acp_lite / low_rank / quadratic_nosvd / quadratic_nosvd_debias / quadratic_nosvd_debias2  
**评测顺序**：Round1 → Round2 → Round3 → Round4 → Round0  
**结果目录**：`/data/250010109/spectral_router/exp_expert_lowrank/output/round_12L/ckpt40000`

---

## 1. 中心目标与评测框架

本轮目标是联合回答“结构健康度、稳定性、跨域干扰、任务能力”四条证据链在同一 checkpoint 上是否一致。  
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
| Round0 任务 | arc_easy, arc_challenge, piqa, hellaswag, openbookqa, winogrande, boolq |

---

## 3. Round0：下游任务表现（lm_eval）

| 模型 | arc_challenge | arc_easy | boolq | hellaswag | openbookqa | piqa | winogrande | Avg |
|:--|--:|--:|--:|--:|--:|--:|--:|--:|
| linear_no_center | 0.2381 | 0.4184 | **0.5862** | 0.3175 | 0.2700 | 0.6371 | 0.5099 | 0.4253 |
| linear_running_center | 0.2637 | 0.4575 | 0.5505 | 0.3571 | 0.3040 | 0.6491 | 0.4893 | 0.4387 |
| low_rank | 0.2466 | 0.4348 | 0.5471 | 0.3499 | 0.2960 | 0.6583 | 0.4996 | 0.4332 |
| acp_lite | 0.2423 | **0.4638** | 0.5755 | **0.3605** | **0.3200** | **0.6638** | **0.5217** | **0.4497** |
| quadratic_nosvd | **0.2705** | 0.4550 | 0.5700 | 0.3543 | 0.2860 | 0.6605 | 0.5146 | 0.4444 |
| quadratic_nosvd_debias | 0.2474 | 0.4545 | 0.5664 | 0.3529 | 0.2880 | 0.6605 | 0.5043 | 0.4392 |
| quadratic_nosvd_debias2 | 0.2509 | 0.4583 | 0.4868 | 0.3577 | 0.2960 | 0.6529 | 0.5020 | 0.4292 |

结论：Round0 综合均值为 `acp_lite > quadratic_nosvd > linear_running_center > quadratic_debias > low_rank > quadratic_debias2 > linear_no_center`。

---

## 4. Round1：专家低秩与路由分工

| 模型 | ED_comp（model_router） | 路由条件熵 | CV_load |
|:--|--:|--:|--:|
| linear_no_center | 53.6698 | 0.000250 | 2.6457 |
| linear_running_center | 50.8785 | 1.421625 | 0.9429 |
| low_rank | 50.8026 | 1.597135 | 0.7886 |
| acp_lite | 50.7609 | 1.611968 | 0.7985 |
| quadratic_nosvd | 53.5015 | 1.568084 | 0.9301 |
| quadratic_nosvd_debias | 49.1629 | 1.386068 | 1.1425 |
| quadratic_nosvd_debias2 | 53.5837 | 1.494893 | 0.9023 |

结论：`linear_no_center` 体现最强塌缩特征（近零熵 + 高负载离散），其余模型在分工上显著更均衡。

---

## 5. Round2：加噪分发一致性

### 5.1 Overall CR（按 sigma）

| 模型 | σ=0.01 | σ=0.05 | σ=0.10 | σ=0.50 |
|:--|--:|--:|--:|--:|
| linear_no_center | **1.0000** | **1.0000** | **1.0000** | **1.0000** |
| linear_running_center | 0.9990 | 0.9958 | 0.9926 | 0.9610 |
| low_rank | 0.9989 | 0.9954 | 0.9913 | 0.9539 |
| acp_lite | 0.9989 | 0.9956 | 0.9919 | 0.9566 |
| quadratic_nosvd | 0.9992 | 0.9965 | 0.9931 | **0.9651** |
| quadratic_nosvd_debias | 0.9988 | 0.9951 | 0.9919 | 0.9524 |
| quadratic_nosvd_debias2 | 0.9993 | 0.9971 | 0.9935 | 0.9645 |

### 5.2 解释

- 非塌缩模型中，quadratic 系列在高噪声点（σ=0.5）保持更高 CR。  
- `linear_no_center` 的 1.0000 与其塌缩路由形态一致，不能单独解读为“最佳鲁棒性”。

---

## 6. Round3：Domain Interference（SI + Margin）

| 模型 | Mean SI（层2/6/10均值） | Margin 信号可用性 |
|:--|--:|:--|
| linear_no_center | 0.8063 | 可用，但单专家主导 |
| linear_running_center | 0.6522 | 可用 |
| low_rank | 0.6747 | 可用 |
| acp_lite | 0.6844 | 不可用（summary 中均值为 0） |
| quadratic_nosvd | 0.6960 | 可用 |
| quadratic_nosvd_debias | **0.6510** | 可用 |
| quadratic_nosvd_debias2 | 0.6746 | 可用 |

结论：SI 上 `quadratic_nosvd_debias` 与 `linear_running_center` 最低；`linear_no_center` 最高，且与塌缩特征一致。

---

## 7. Round4：新增实验（方向敏感性）方法与结果

### 7.1 Round4 是怎么做的

对每个目标层 \(l\in\{2,6,10\}\)：

1. 计算层均值方向 \(u_l\)；
2. 构造两种等幅扰动：  
   - 平行扰动（parallel）：沿 \(u_l\) 加噪；  
   - 正交扰动（orthogonal）：沿与 \(u_l\) 正交子空间加噪；
3. 对 clean 与扰动后路由 top1 做一致性统计：
   \[
   CR = \frac{\#(e^{clean}=e^{perturbed})}{\#tokens}
   \]
4. 定义方向敏感指数：
   \[
   DSI = CR_{orthogonal} - CR_{parallel}
   \]

本轮使用 `perturb_scale=0.1`，先算层内 CR，再对层 2/6/10 做平均得到整体 CR 与 DSI。

### 7.2 Round4 结果总表

| 模型 | CR_parallel | CR_orthogonal | DSI |
|:--|--:|--:|--:|
| linear_no_center | 1.000000 | 1.000000 | 0.000000 |
| linear_running_center | 0.999673 | 0.999864 | 0.000190 |
| low_rank | 0.999456 | 0.999755 | 0.000299 |
| acp_lite | 0.999565 | 0.999810 | 0.000245 |
| quadratic_nosvd | 0.999673 | 0.999755 | 0.000082 |
| quadratic_nosvd_debias | 0.999592 | 0.999782 | 0.000190 |
| quadratic_nosvd_debias2 | 0.999782 | 0.999864 | 0.000082 |

### 7.3 Round4 完成度与偏差（单独判断）

- 完成度：**已完成**（7/7 模型有结果，parallel/orthogonal/DSI 全量产出）。  
- 偏差：DSI 量级极小（约 \(10^{-4}\)），方向效应弱，难支持“强方向敏感机制”结论。

---

# Result Summary
- Round0 测任务能力，acp_lite 均分第一，quadratic_nosvd 第二，linear_no_center 最末。
- Round1 测结构分工，linear_no_center 出现显著塌缩，其余模型条件熵与负载分布更健康。
- Round2 测扰动稳定性，非塌缩模型中 quadratic 在高噪声点更稳；no_center 的满分稳定性与塌缩耦合。
- Round3 测跨域干扰，debias/linear_running 的 SI 更低，no_center 干扰最高。
- Round4 测方向敏感性，流程完整但 DSI 普遍极小，方向性证据弱。

# Reliability Audit
- 数据完整性：round0/1/2/3/4 汇总齐全，round1-4 均 `success_models=7, failed_models=0`。
- 高可信：no_center 塌缩（Round1）与高干扰/低综合表现（Round3/0）同向出现。
- 中等可信：quadratic 系列在 Round2 高噪声稳定性优势清晰，但与任务提升并非一一对应。
- 需谨慎：Round4 的 DSI 效应量过小，当前只能给出“弱方向性差异”结论。

# Hypothesis-Relevant Findings
- 被支持：
  - 抑制塌缩与更低跨域冲突、较好综合任务表现相关。
  - 运行中心/低秩/quadratic 路线整体优于 no_center 退化对照。
- 未被支持：
  - “方向敏感性是主要机制”未获强证据支持（Round4 DSI 过小）。
  - 单一方案在所有维度全面最优未成立。

# Checkpoint Delta
- 可回写：
  - ckpt40000 已形成五轮闭环证据，能够支撑“no_center 退化、结构化路由更优”的阶段结论。
  - Round4 已按方案执行完成，可作为机制补充证据入档。
- 仅 tentative evidence：
  - Round4 对方向机制的支持为弱证据。
  - Round2 的极高 CR 需要结合 Round1/3 才能解释。

# Report-Ready Summary
- 可直接用于 checkpoint/report 的内容：
  - 五轮实验均完成且覆盖 7 模型；
  - no_center 的塌缩与综合劣势已被多轮一致验证；
  - acp_lite 与 quadratic 家族在任务与结构维度保持竞争力；
  - Round4 方法、公式、全量结果已披露并可复核。
- 仅可作为 tentative evidence 的内容：
  - Round4 的方向性差异。

# Experiment -> Theory Result Card
- **Scope**：ckpt40000，7 模型，层位 2/6/10，round0-4 全覆盖。
- **Positive Evidence**：塌缩抑制与结构健康度/低干扰/更优综合任务表现同向。
- **Negative/Null Evidence**：Round4 DSI 量级过小，未形成强机制区分。
- **Reliability Grade**：Round0 A- / Round1 A- / Round2 B / Round3 B+ / Round4 B-。
- **Theory Result**：当前主线更支持“塌缩抑制与跨域冲突控制”，不支持把“方向敏感性”提升为核心决定因素。
