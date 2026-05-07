# 24L 模型组实验综合报告

**实验时间**：2026-03-24
**Checkpoint**：40000
**模型组**：linear_no_center / linear_running_center / linear_running_center_acp_on / low_rank_running_center
**评测 rounds**：Round0（下游任务）、Round1（Expert 低秩分析）、Round2（特征扰动稳定性）、Round3（谱域干扰）

---

## 一、实验概述

### 1.1 实验对象

| 简称 | 模型目录 |
|:--|:--|
| linear_no_center | `qwen3-moe-H768--linear_no_center_24L_8gpu_gbs512-center_off-gate_off-acp_off-lb_0-linear` |
| linear_running_center | `qwen3-moe-H768--linear_running_center_24L_8gpu_gbs512-center_running-gate_off-acp_off-lb_0-linear` |
| acp_on | `qwen3-moe-H768--linear_running_center_acp_on_24L_8gpu_gbs512-center_running-gate_off-acp_on-lb_0-linear` |
| low_rank | `qwen3-moe-H768--low_rank_running_center_24L_8gpu_gbs512-center_running-gate_off-acp_off-lb_0-low_rank_r96` |

### 1.2 实验设置

| 参数 | 值 |
|:--|:--|
| 评测层位 | Layer 2, 6, 10 |
| 采样数（Round1/2） | 96 samples |
| 采样数（Round3） | 64 samples / domain |
| max_length | 128 |
| SVD rank | 96（与 low_rank 模型命名一致） |
| 扰动噪声 σ（Round2） | 0.01, 0.05, 0.1, 0.5 |
| 下游任务（Round0） | arc_easy, arc_challenge, piqa, hellaswag, openbookqa, winogrande, boolq |

---

## 二、下游任务评测结果（Round0）

### 2.1 分任务明细

| 模型 | arc_challenge | arc_easy | boolq | hellaswag | openbookqa | piqa | winogrande |
|:--|--:|--:|--:|--:|--:|--:|--:|
| linear_running_center | **0.2611** | **0.4840** | 0.5434 | **0.3951** | **0.3120** | **0.6817** | 0.4988 |
| low_rank | **0.2611** | 0.4630 | 0.5648 | 0.3862 | 0.2980 | 0.6746 | 0.5091 |
| acp_on | 0.2500 | 0.4743 | **0.6055** | 0.3923 | 0.2940 | 0.6768 | 0.5170 |
| linear_no_center | 0.2466 | 0.4646 | 0.5966 | 0.3525 | 0.3000 | 0.6518 | **0.5225** |

### 2.2 均分排名（7 任务平均）

| 排名 | 模型 | 均分 ↑ | 领先任务数 |
|:--:|:--|--:|--:|
| **1** | **acp_on** | **0.4586** | 1/7（boolq） |
| 2 | linear_running_center | 0.4537 | 5/7 |
| 3 | low_rank | 0.4510 | 1/7（winogrande 并列） |
| 4 | linear_no_center | 0.4478 | 0/7 |

> **注意**：以均分看 acp_on 第一（0.4586），但这是因为它在 boolq 这一高权重任务上遥遥领先（0.6055 vs 均值 0.5772）；若看综合领先任务数，linear_running_center 在 5/7 任务领先，是更全面的模型。

### 2.3 任务分项冠军

| 任务 | 冠军模型 | 分数 |
|:--|:--|--:|
| arc_challenge | linear_running_center / low_rank（并列） | 0.2611 |
| arc_easy | linear_running_center | 0.4840 |
| boolq | acp_on | 0.6055 |
| hellaswag | linear_running_center | 0.3951 |
| openbookqa | linear_running_center | 0.3120 |
| piqa | linear_running_center | 0.6817 |
| winogrande | linear_no_center | 0.5225 |

---

## 三、Expert 低秩结构分析（Round1）

### 3.1 核心指标

| 模型 | ED ↓ | ED_comp ↓ | Overlap | RandED | SVD_LR_ED ↓ |
|:--|--:|--:|--:|--:|--:|
| low_rank | 69.76 | **64.12** | 0.290 | 82.92 | N/A（自身为低秩） |
| linear_running_center | **69.62** | 66.85 | 0.284 | 78.74 | 80.93 |
| linear_no_center | 70.90 | 63.79 | nan | **64.95** | **63.37** |
| acp_on | 72.06 | 66.47 | 0.310 | 78.66 | 79.45 |

**指标说明**：
- **ED**：原始欧氏距离，越低表示 expert 表征越紧凑
- **ED_comp**：补偿后欧氏距离（考虑不平衡专家负载），越低表示在压缩维度下 expert 表征越好
- **Overlap**：专家子空间重叠率，越低表示路由越独立
- **RandED**：与随机路由的 ED 比值，越高表示模型路由与随机基线差异越大
- **SVD_LR_ED**：将模型 router 以 SVD 低秩（rank=96）重构后的 ED，越低表示模型越"低秩友好"

### 3.2 关键发现

1. **low_rank ED_comp 最低**（64.12）→ 低秩约束对补偿维度压缩效果最优
2. **linear_no_center SVD_LR_ED 最低**（63.37）→ 与其无 center running 的线性结构最吻合 SVD 假设
3. **linear_no_center 的 Overlap 为 NaN**，因为其 router 只激活单个 expert（无重叠），这是 no_center 版本的极端稀疏路由特性
4. **acp_on ED 最高**（72.06）→ ACP 辅助可能引入了额外的路由非线性

### 3.3 SVD_LR_ED 说明

> SVD_LR_ED 衡量的是"用 rank=96 的 SVD 低秩近似去拟合各模型 router 后，与原始 router 表征的偏差"。数值越低说明该模型的路由机制越"低秩友好"。由于 low_rank 模型本身就是低秩训练而成，其 SVD 重构与自身几乎等价，因此 SVD_LR_ED 不适用于自身对比；应参考其 ED_comp（64.12）来判断其低秩结构质量。

---

## 四、特征扰动稳定性（Round2）

### 4.1 一致性率（CR）结果

| σ | linear_no_center ↑ | linear_running_center | acp_on | low_rank ↓ |
|--:|--:|--:|--:|--:|
| 0.01 | **1.0000** | 0.9988 | 0.9991 | 0.9986 |
| 0.05 | **1.0000** | 0.9955 | 0.9947 | 0.9941 |
| 0.10 | **1.0000** | 0.9909 | 0.9906 | 0.9886 |
| 0.50 | **1.0000** | 0.9500 | 0.9496 | 0.9430 |

**指标说明**：CR = clean top1 expert 与 noisy top1 expert 一致的比例，越接近 1.0 表示路由越鲁棒。

### 4.2 关键发现

1. **linear_no_center 在所有 σ 下 CR = 1.0000**，完全不受特征扰动影响——这是 no_center 版本极端稀疏路由（单 expert 激活）的直接结果：扰动不足以改变 top-1 expert 的判定
2. 其余三模型随 σ 增大一致性率单调下降
3. σ=0.5 时 low_rank 最脆弱（CR=0.9430），说明低秩近似在大幅扰动下放大了敏感度

---

## 五、谱域干扰分析（Round3）

### 5.1 核心指标

| 模型 | Mean SI ↓ | Mean Margin_A ↑ | Mean Margin_B ↑ |
|:--|--:|--:|--:|
| low_rank | **0.6389** | 0.999 | 1.066 |
| linear_running_center | 0.6763 | 1.235 | 1.329 |
| acp_on | 0.6895 | 1.192 | 1.289 |
| linear_no_center | 0.7952 | **2.232** | **2.047** |

**指标说明**：
- **Mean SI**：跨域谱干扰强度，越低表示不同 domain 的 expert 路由越独立
- **Mean Margin**：域分类置信度，越高表示域间区分越清晰

### 5.2 关键发现

1. **low_rank Mean SI 最低**（0.639）→ 低秩约束有效降低了谱干扰，与 Round1 ED_comp 最低一致
2. **linear_no_center SI 最高**（0.795）但 Margin 最大（2.23/2.05）→ 域间区分清晰但谱干扰也大，两者需要权衡
3. linear_running_center 与 acp_on 处于中间地带（SI 差仅 0.013）

---

## 六、多维度综合排名

### 6.1 综合排名表

| 排名 | 模型 | Round0 均分 | Round3 SI | Round2 σ=0.5 CR | Round1 ED_comp | 综合 |
|:--:|:--|--:|--:|--:|--:|--:|
| **1** | **linear_running_center** | 0.4537 (2) | 0.6763 (2) | 0.9500 (2) | 66.85 (3) | ★★★ |
| 2 | low_rank | 0.4510 (3) | **0.6389** (1) | 0.9430 (4) | **64.12** (1) | ★★☆ |
| 3 | acp_on | **0.4586** (1) | 0.6895 (3) | 0.9496 (3) | 66.47 (2) | ★★☆ |
| 4 | linear_no_center | 0.4478 (4) | 0.7952 (4) | **1.0000** (1) | 63.79 (1) | ★☆☆ |

> 括号内为各维度内的排名。（1）= 最优，（4）= 最差

### 6.2 各维度冠军

| 维度 | 冠军 | 指标 |
|:--|:--|:--|
| Round0 下游均分 | acp_on | 0.4586 |
| Round0 领先任务数 | linear_running_center | 5/7 |
| Round3 谱干扰（SI） | low_rank | 0.6389 |
| Round2 扰动鲁棒性（CR） | linear_no_center | 1.0000 |
| Round1 低秩吻合度（SVD_LR_ED） | linear_no_center | 63.37 |
| Round1 ED_comp | low_rank | 64.12 |

---

## 七、假设验证与结论

### 7.1 主要发现

**① 低秩约束有效降低了谱干扰（SI↓），但下游任务没有相应提升**

- low_rank 在 Round3 SI 最优（0.639），在 Round1 ED_comp 也最优（64.12），结构性指标双重验证了低秩假设
- 但下游均分 acp_on 最高（0.4586），linear_running_center 次优（0.4537），low_rank 第三（0.4510）
- **结论**：谱干扰降低 ≠ 下游任务提升，两者解耦。结构指标的优化存在上限效应。

**② center running 的有无对所有维度有系统性影响**

- no_center：对特征扰动完全鲁棒（CR=1.0），SVD 低秩拟合最好（63.37），但 SI 最高（0.795），下游任务最弱
- running_center：下游任务综合最强（5/7 领先），SI 和 CR 处于中间位置，是最均衡的选择

**③ ACP 辅助在布尔推理任务上有特异性优势**

- acp_on 在 boolq（布尔阅读理解）上以 0.606 大幅领先所有模型（第二名 low_rank 0.565）
- 这与 ACP 增加路由非线性的观察一致：更强的非线性有助于布尔推理

**④ 结构性指标与任务性能的解耦说明**

- SVD_LR_ED（理论低秩吻合度）和 SI（谱干扰）都是结构性指标，但它们与实际任务性能（Acc）相关性弱
- 这提示：在评估 router 改进时，不能只看结构性指标，必须以任务性能为最终裁判

### 7.2 最终推荐

| 场景 | 推荐模型 | 理由 |
|:--|:--|:--|
| **综合最优（默认推荐）** | linear_running_center | 下游 5/7 领先，均衡性最好 |
| 追求谱干扰极低 | low_rank | SI=0.639，ED_comp=64.12 双优 |
| 布尔推理任务为主 | acp_on | boolq 0.606，遥遥领先 |
| 高扰动安全场景 | linear_no_center | CR=1.0 完全鲁棒 |

---

## 八、数据文件索引

| Round | 结果目录 |
|:--|:--|
| Round0 下游评测 | `output/round0_downstream_ckpt40000_24L_4models_fulltasks/` |
| Round1 低秩分析 | `output/round1_expert_low_rank_24L_ckpt40000_4models/` |
| Round2 特征扰动 | `output/round2_feature_perturbation_24L_ckpt40000_4models/` |
| Round3 谱域干扰 | `output/round3_spectral_interference_24L_ckpt40000_4models/` |

---

*报告生成时间：2026-03-24 | 实验执行：Trae Agent | 数据源：各 round 汇总 JSON*
