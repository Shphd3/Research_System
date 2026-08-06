# 12L / ckpt60000 五模型综合报告（Continual Learning 导向）

**实验时间**：2026-03-28  
**Checkpoint**：60000  
**模型组**：linear_no_center / linear_running_center / acp_on / low_rank / quadratic_nosvd  
**评测顺序**：Round1 → Round2 → Round3 → Round0  
**结果目录**：`/data/250010109/spectral_router/exp_expert_lowrank/output/round_12L/ckpt60000`

---

## 1. 中心目标与评测框架

本轮评测目标不是单项最优，而是判断不同路由是否更接近 continual learning 的三项核心诉求：

- 抗干扰：新域进入时跨域干扰更低（Round3 SI）且噪声扰动更稳（Round2 CR）。
- 可分化：专家结构具备专门化与可分离性（Round1 ED/ED_comp/Overlap）。
- 能力保留：结构改造不能明显牺牲下游任务表现（Round0）。

---

## 2. 实验设置

| 参数 | 值 |
|:--|:--|
| 评测层位 | Layer 2, 6, 10 |
| Round1/2 样本数 | 96 |
| Round3 样本数 | 64 / domain |
| max_length | 128 |
| Round2 噪声 | 0.01, 0.05, 0.1, 0.5 |
| Round0 任务 | arc_easy, arc_challenge, piqa, hellaswag, openbookqa, winogrande, boolq |
| 排除模型 | fixedbeta |

---

## 3. Round0：下游任务表现（能力保留）

### 3.1 分任务结果

| 模型 | arc_challenge | arc_easy | boolq | hellaswag | openbookqa | piqa | winogrande | Avg |
|:--|--:|--:|--:|--:|--:|--:|--:|--:|
| linear_no_center | 0.2474 | 0.4411 | 0.6040 | 0.3302 | 0.2740 | 0.6425 | 0.5130 | 0.4360 |
| linear_running_center | 0.2662 | 0.4672 | 0.5893 | **0.3754** | 0.2900 | 0.6589 | 0.5162 | 0.4519 |
| acp_on | 0.2611 | **0.4844** | **0.6193** | 0.3746 | **0.3080** | **0.6697** | 0.4988 | **0.4594** |
| low_rank | 0.2577 | 0.4668 | 0.5957 | 0.3681 | 0.3000 | 0.6638 | 0.5178 | 0.4528 |
| quadratic_nosvd | **0.2688** | 0.4672 | 0.6052 | 0.3732 | 0.2900 | 0.6610 | **0.5217** | 0.4553 |

### 3.2 结论（CL 视角）

- `acp_on` 仍是下游均分最优，`quadratic_nosvd` 与 `low_rank` 为中上表现。
- `quadratic_nosvd` 在 `arc_challenge` 与 `winogrande` 有优势，但均分略低于 `acp_on`。

![Round0 热力图](./figures/round0_downstream_heatmap.png)

---

## 4. Round1：专家低秩结构（专门化与可分离）

| 模型 | ED ↓ | ED_comp ↓ | Overlap@r ↓ | RandED | SVD_LR_ED ↓ |
|:--|--:|--:|--:|--:|--:|
| linear_no_center | **56.2947** | **46.2362** | nan | N/A | N/A |
| linear_running_center | 61.8067 | 51.1212 | 0.2949 | N/A | N/A |
| acp_on | 56.4576 | 52.8773 | **0.2684** | N/A | N/A |
| low_rank | 57.4564 | 53.6336 | 0.2746 | N/A | N/A |
| quadratic_nosvd | 61.9766 | 56.4000 | 0.2702 | N/A | N/A |

### 4.1 结论（CL 视角）

- `linear_no_center` 依旧在 ED_comp 上最低，但其跨域干扰与任务表现并不构成 CL 全局最优。
- `quadratic_nosvd` Overlap 处于较低区间，说明专家分离还在；但 ED_comp 最差，专家内部压缩能力仍是短板。

![Round1 双轴图](./figures/round1_edcomp_overlap_dual_axis.png)

---

## 5. Round2：特征扰动稳定性（抗漂移）

### 5.1 Overall CR

| 模型 | σ=0.01 | σ=0.05 | σ=0.10 | σ=0.50 |
|:--|--:|--:|--:|--:|
| linear_no_center | **1.0000** | **1.0000** | **1.0000** | **1.0000** |
| linear_running_center | 0.9991 | **0.9965** | 0.9927 | 0.9547 |
| acp_on | 0.9991 | 0.9953 | 0.9904 | 0.9424 |
| low_rank | 0.9987 | 0.9946 | 0.9901 | 0.9452 |
| quadratic_nosvd | 0.9992 | 0.9960 | **0.9926** | **0.9592** |

### 5.2 高噪声分层（σ=0.5）

| 模型 | Layer2 | Layer6 | Layer10 | Overall |
|:--|--:|--:|--:|--:|
| linear_no_center | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| linear_running_center | 1.0000 | 0.9040 | 0.9602 | 0.9547 |
| acp_on | 1.0000 | 0.9135 | 0.9137 | 0.9424 |
| low_rank | 1.0000 | 0.8771 | 0.9585 | 0.9452 |
| quadratic_nosvd | 1.0000 | **0.9321** | 0.9455 | **0.9592** |

### 5.3 结论（CL 视角）

- `quadratic_nosvd` 在 running-center 家族中仍是高噪声最稳（0.9592）。
- `linear_no_center` 仍表现为“最稳但不一定最优”的保守路由形态。
- Layer6 依然是区分模型稳健性的关键层。

![Round2 总曲线](./figures/round2_overall_cr_curve.png)
![Round2 Layer6 曲线](./figures/round2_layer6_consistency_curve.png)

---

## 6. Round3：跨域谱干扰（抗干扰核心）

| 模型 | Mean SI ↓ | Mean Margin_A ↑ | Mean Margin_B ↑ |
|:--|--:|--:|--:|
| linear_no_center | 0.7907 | **7.6372** | **8.5844** |
| linear_running_center | 0.6535 | 1.7539 | 1.7610 |
| acp_on | **0.6501** | 1.9915 | 2.0313 |
| low_rank | 0.6607 | 1.9471 | 1.8700 |
| quadratic_nosvd | 0.6867 | 0.0000 | 0.0000 |

### 6.1 结论（CL 视角）

- `acp_on` 在 SI 上继续最优，`linear_running_center` 紧随其后。
- `low_rank` 的 SI 在 ckpt60000 略高于 linear_running_center。
- `quadratic_nosvd` 的 margin 继续全 0，建议按“实现/导出口径核验项”处理，不直接当作模型行为结论。

![Round3 SI-Margin 散点](./figures/round3_si_margin_scatter.png)

---

## 7. 围绕 Continual Learning 的综合评估

### 7.1 四维综合排名（Round0 Avg↑ / Round1 ED_comp↓ / Round2 CR@0.5↑ / Round3 SI↓）

| 模型 | Round0 Rank | Round1 Rank | Round2 Rank | Round3 Rank | RankSum |
|:--|--:|--:|--:|--:|--:|
| acp_on | 1 | 3 | 5 | 1 | **10** |
| linear_running_center | 4 | 2 | 3 | 2 | **11** |
| linear_no_center | 5 | 1 | 1 | 5 | 12 |
| quadratic_nosvd | 2 | 5 | 2 | 4 | 13 |
| low_rank | 3 | 4 | 4 | 3 | 14 |

### 7.2 解释

- ckpt60000 下，`acp_on` 成为综合第一，主要受益于 Round0 与 Round3 的领先。
- `linear_running_center` 保持稳定均衡，综合第二。
- `quadratic_nosvd` 仍是“鲁棒性较强但结构压缩与跨域干扰待改进”的候选路线。

---

## 8. 对 quadratic_nosvd 的重点判断（面向下一轮）

### 8.1 当前状态

- 正向信号：Round2 高噪声鲁棒性在 running-center 家族中最优（0.9592）。
- 负向信号：Round1 ED_comp 偏高（56.4000），Round3 SI 为 0.6867，未进入前列。
- 异常信号：Round3 margin 持续全 0，仍需单独核验。

### 8.2 下一步建议

1. 继续优先排查 Round3 margin 导出链路，确保 quadratic 与其它路由统计口径一致。  
2. 维持 Round2 噪声评测协议，做 ckpt 纵向对比（50k/60k/70k）。  
3. 针对 quadratic_nosvd 做 ED_comp 友好化调参，目标是提升结构压缩能力。  

---

## 9. 图片与数据索引

### 9.1 图片目录

- `docs/round_12L/ckpt60000/figures/round0_downstream_heatmap.png`
- `docs/round_12L/ckpt60000/figures/round1_edcomp_overlap_dual_axis.png`
- `docs/round_12L/ckpt60000/figures/round2_overall_cr_curve.png`
- `docs/round_12L/ckpt60000/figures/round2_layer2_consistency_curve.png`
- `docs/round_12L/ckpt60000/figures/round2_layer6_consistency_curve.png`
- `docs/round_12L/ckpt60000/figures/round2_layer10_consistency_curve.png`
- `docs/round_12L/ckpt60000/figures/round2_overall_consistency_curve.png`
- `docs/round_12L/ckpt60000/figures/round3_si_margin_scatter.png`

### 9.2 数据来源

- Round0：`output/round_12L/ckpt60000/round0_downstream_fulltasks/round0_downstream_summary.csv`
- Round1：`output/round_12L/ckpt60000/round1_expert_low_rank/enhanced_low_rank_summary.json`
- Round2：`output/round_12L/ckpt60000/round2_feature_perturbation/round2_feature_perturbation_summary.json`
- Round3：`output/round_12L/ckpt60000/round3_spectral_interference/spectral_interference_with_margin_summary.json`

---

*报告生成时间：2026-03-28*  
*报告口径：Continual Learning 主线（抗干扰 + 专门化 + 能力保留）*
