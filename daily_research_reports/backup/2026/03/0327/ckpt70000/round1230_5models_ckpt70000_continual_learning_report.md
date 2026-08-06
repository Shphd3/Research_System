# 12L / ckpt70000 五模型综合报告（Continual Learning 导向）

**实验时间**：2026-03-28  
**Checkpoint**：70000  
**模型组**：linear_no_center / linear_running_center / acp_on / low_rank / quadratic_nosvd  
**评测顺序**：Round1 → Round2 → Round3 → Round0  
**结果目录**：`/data/250010109/spectral_router/exp_expert_lowrank/output/round_12L/ckpt70000`

---

## 1. 中心目标与评测框架

本轮评测的中心目标不是“单点指标最优”，而是检验不同路由形式是否更接近 **continual learning（持续学习）** 的核心诉求：

- **抗干扰**：新域/新任务进入后，旧能力不被破坏（Round3 SI、Round2 CR）
- **可分化**：专家表征可形成有用专门化，减少互相污染（Round1 ED/ED_comp/Overlap）
- **可保留任务性能**：结构优化不能明显牺牲下游任务表现（Round0）

因此，本报告采用“结构指标 + 稳定性 + 任务性能”三轴联合判断。

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
| 排除模型 | fixedbeta（按本轮要求排除） |

---

## 3. Round0：下游任务表现（能力保留）

### 3.1 分任务结果

| 模型 | arc_challenge | arc_easy | boolq | hellaswag | openbookqa | piqa | winogrande | Avg |
|:--|--:|--:|--:|--:|--:|--:|--:|--:|
| linear_no_center | 0.2457 | 0.4478 | 0.6003 | 0.3370 | 0.2860 | 0.6453 | 0.5162 | 0.4398 |
| linear_running_center | 0.2560 | 0.4747 | 0.5572 | 0.3800 | 0.3000 | 0.6719 | 0.5051 | 0.4493 |
| acp_on | 0.2551 | **0.4790** | **0.6147** | **0.3822** | 0.3080 | **0.6779** |**0.5225** | **0.4628** |
| low_rank | 0.2517 | 0.4760 | 0.6110 | 0.3751 | **0.3140** | 0.6692 | 0.5138 | 0.4587 |
| quadratic_nosvd | **0.2679** | 0.4747 | 0.5847 | 0.3782 | 0.2940 | 0.6659 | 0.5122 | 0.4540 |

### 3.2 结论（CL 视角）

- 若把 Round0 作为“旧任务能力保留”的代理指标，`acp_on` 当前最好，`low_rank` 第二，`quadratic_nosvd` 第三。
- `quadratic_nosvd` 在 `arc_challenge` 有明显优势，但在 boolq/openbookqa 上偏弱，导致均分未进入前二。

![Round0 热力图](./figures/round0_downstream_heatmap.png)

---

## 4. Round1：专家低秩结构（专门化与可分离）

| 模型 | ED ↓ | ED_comp ↓ | Overlap@r ↓ | RandED | SVD_LR_ED ↓ |
|:--|--:|--:|--:|--:|--:|
| linear_no_center | 56.7420 | **46.5672** | nan | 54.9660 | 54.9073 |
| linear_running_center | 61.9413 | 51.1608 | 0.2909 | 73.9479 | 72.1815 |
| acp_on | **56.6278** | 52.4893 | 0.2649 | 70.9361 | 71.9223 |
| low_rank | 57.4795 | 52.3292 | 0.2701 | 73.3872 | N/A |
| quadratic_nosvd | 61.2054 | 55.8015 | **0.2635** | 70.8613 | N/A |

### 4.1 结论（CL 视角）

- `quadratic_nosvd` 的 Overlap 最低（专家子空间更分离），说明有减少专家间耦合的潜力。  
- 但 `ED_comp` 最差（55.80），表示在“样本不均衡补偿后”的有效维度压缩不理想，结构紧凑性不足。  
- 这意味着它目前更像“把专家分开了”，但还没有“把专家内部压紧”，对 continual learning 里的抗遗忘仍不够稳。

![Round1 双轴图](./figures/round1_edcomp_overlap_dual_axis.png)

---

## 5. Round2：特征扰动稳定性（稳定性/抗漂移）

### 5.1 Overall CR

| 模型 | σ=0.01 | σ=0.05 | σ=0.10 | σ=0.50 |
|:--|--:|--:|--:|--:|
| linear_no_center | **1.0000** | **1.0000** | **1.0000** | **1.0000** |
| linear_running_center | 0.9991 | 0.9953 | 0.9922 | 0.9512 |
| acp_on | 0.9986 | 0.9946 | 0.9907 | 0.9387 |
| low_rank | 0.9986 | 0.9942 | 0.9895 | 0.9405 |
| quadratic_nosvd | 0.9991 | 0.9963 | 0.9932 | **0.9583** |

### 5.2 高噪声分层（σ=0.5）

| 模型 | Layer2 | Layer6 | Layer10 | Overall |
|:--|--:|--:|--:|--:|
| linear_no_center | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| linear_running_center | 1.0000 | 0.8971 | 0.9565 | 0.9512 |
| acp_on | 1.0000 | 0.9073 | 0.9087 | 0.9387 |
| low_rank | 1.0000 | 0.8686 | 0.9528 | 0.9405 |
| quadratic_nosvd | 1.0000 | 0.9319 | 0.9431 | 0.9583 |

### 5.3 结论（CL 视角）

- 在高噪声下，`quadratic_nosvd` 在 running-center 家族里表现最好（0.9583），说明其路由边界更稳。  
- `low_rank` 与 `acp_on` 的 Layer6 衰减更明显，是潜在干扰放大层。  
- `linear_no_center` 虽最稳，但结合 Round3/Round0 看其“稳而不优”，更像过度保守路由，不是理想持续学习解。

![Round2 总曲线](./figures/round2_overall_cr_curve.png)
![Round2 Layer6 曲线](./figures/round2_layer6_consistency_curve.png)

---

## 6. Round3：跨域谱干扰（抗干扰核心）

| 模型 | Mean SI ↓ | Mean Margin_A ↑ | Mean Margin_B ↑ |
|:--|--:|--:|--:|
| linear_no_center | 0.7869 | **7.8222** | **8.2731** |
| linear_running_center | 0.6504 | 1.7698 | 1.7566 |
| acp_on | **0.6430** | 2.0159 | 2.0711 |
| low_rank | 0.6505 | 2.0918 | 1.9256 |
| quadratic_nosvd | 0.6708 | 0.0000 | 0.0000 |

### 6.1 结论（CL 视角）

- 若把 SI 视作“跨域干扰强度”，`acp_on` 最优，`low_rank≈linear_running_center`，`quadratic_nosvd` 落后于前 3。  
- `quadratic_nosvd` 的 margin 结果为 0，需要谨慎解读：这更像当前实现/导出口径问题，而非“真实无置信度”。  
- 因此在 CL 主线下，`quadratic_nosvd` 目前证据更偏“稳定性有潜力（Round2）”，但“抗跨域干扰（Round3）未证明优势”。

![Round3 SI-Margin 散点](./figures/round3_si_margin_scatter.png)

---

## 7. 围绕 Continual Learning 的综合评估

### 7.1 四维综合排名（Round0 Avg↑ / Round1 ED_comp↓ / Round2 CR@0.5↑ / Round3 SI↓）

| 模型 | Round0 Rank | Round1 Rank | Round2 Rank | Round3 Rank | RankSum |
|:--|--:|--:|--:|--:|--:|
| linear_running_center | 4 | 2 | 3 | 2 | **11** |
| acp_on | 1 | 4 | 5 | 1 | **11** |
| low_rank | 2 | 3 | 4 | 3 | 12 |
| linear_no_center | 5 | 1 | 1 | 5 | 12 |
| quadratic_nosvd | 3 | 5 | 2 | 4 | 14 |

### 7.2 解释

- **目前最接近 CL 实用最优的两条路线**：`acp_on` 与 `linear_running_center`  
  - `acp_on`：任务性能与跨域 SI 最强，但噪声稳定性一般。  
  - `linear_running_center`：四项都不极端，整体均衡。
- `low_rank` 在本轮是“中上但未统治”：任务和 SI 都不错，但未形成显著领先。
- `quadratic_nosvd` 是“候选潜力型”：
  - 优点：Round2 稳定性强、Round0 均分中上；
  - 短板：Round1 ED_comp 偏弱、Round3 SI 偏高且 margin 异常为 0；
  - 结论：离 CL 目标“更近了一些”，但还没到可替代当前最优方案的程度。

---

## 8. 对 quadratic_nosvd 的重点判断（面向下一轮）

### 8.1 当前状态

- **正向信号**：高噪声鲁棒性（CR@0.5=0.9583）优于 linear/low_rank/acp_on。  
- **负向信号**：跨域干扰 SI=0.6708，仍高于 acp_on 与 linear/low_rank。  
- **可疑信号**：Round3 margin 全 0，不应直接拿来判定模型“置信度为零”。

### 8.2 工程优先级建议

1. 先修正/核验 Round3 margin 导出链路（确保 quadratic 的 router logits 统计路径一致）。  
2. 保持现有 Round2 噪声评测口径，增加 checkpoint 纵向比较（50k/60k/70k）。  
3. 对 quadratic 增加“ED_comp 友好化”调参方向，目标是把结构压缩能力拉回前 3。  

---

## 9. 图片与数据索引

### 9.1 图片目录（已复制）

- `docs/round_12L/figures/round0_downstream_heatmap.png`
- `docs/round_12L/figures/round1_edcomp_overlap_dual_axis.png`
- `docs/round_12L/figures/round2_overall_cr_curve.png`
- `docs/round_12L/figures/round2_layer2_consistency_curve.png`
- `docs/round_12L/figures/round2_layer6_consistency_curve.png`
- `docs/round_12L/figures/round2_layer10_consistency_curve.png`
- `docs/round_12L/figures/round2_overall_consistency_curve.png`
- `docs/round_12L/figures/round3_si_margin_scatter.png`

### 9.2 数据来源

- Round0：`output/round_12L/ckpt70000/round0_downstream_fulltasks/round0_downstream_summary.csv`
- Round1：`output/round_12L/ckpt70000/round1_expert_low_rank/enhanced_low_rank_summary.json`
- Round2：`output/round_12L/ckpt70000/round2_feature_perturbation/round2_feature_perturbation_summary.json`
- Round3：`output/round_12L/ckpt70000/round3_spectral_interference/spectral_interference_with_margin_summary.json`

---

*报告生成时间：2026-03-28*  
*报告口径：Continual Learning 主线（抗干扰 + 专门化 + 能力保留）*
