# [调研]MoE - 迭代状态存档 v5.0（24L 全量重构版）

## 1. 版本定位与迁移说明

- **版本目标**：在 v4.1/v4.2/v4.3 的方法论基础上，形成面向 **24 层模型组** 的统一结论存档。
- **核心差异**：v4 系列主要围绕 12L 训练体系（训练了40B左右数据）；v5 统一切换到 24L 模型（ckpt=40000）（训练了20B左右数据）进行 Round0/1/2/3 的联动评估。
- **结果来源**：`/data/250010109/spectral_router/exp_expert_lowrank/docs/round1230_4models_ckpt40000_report.md`。
- **模型集合（4个）**：
  - `linear_no_center`
  - `linear_running_center`
  - `linear_running_center_acp_on`
  - `low_rank_running_center`

## 2. 当前主线目标（North Star）

在 24L 条件下验证并量化以下链路是否成立：

`路由结构约束（center / ACP / low-rank） → 专家几何结构（ED / Overlap / SI） → 路由稳定性（CR） → 下游任务收益（Acc）`

目标不是只找“单指标最优”，而是明确：

1. 哪种结构约束带来**最稳健的综合收益**；
2. 哪些指标之间存在**同向耦合**；
3. 哪些指标之间存在**结构-性能解耦**。

## 3. 假设状态总览（24L 口径）

| 假设 | 状态 | 24L 证据摘要 |
|:--|:--|:--|
| H1a：低秩/结构约束改变路由决策流形 | ✅ 支持 | Round1/3 显示不同结构在 Overlap、SI、Margin 上存在稳定分化 |
| H1b：低秩促进输入低维化（ED压缩） | ✅ 部分支持 | low_rank 在 ED_comp 最优（64.12），但 ED 绝对值并非全局最优 |
| H1c：低维输入限制参数更新子空间 | ⚠️ 间接支持 | 结构指标支持，但未做权重更新轨迹直接验证 |
| H1d：低秩天然更抗噪 | ❌ 当前不支持 | Round2 在高噪声下 low_rank CR 最低（0.943） |
| H1e：低秩降低跨域谱干扰 | ✅ 在24L支持 | Round3 low_rank Mean SI 最低（0.6389） |
| 新发现：结构指标与任务性能强耦合 | ❌ 不成立 | low_rank 结构指标优，但下游均分非第一，存在显著解耦 |

## 4. 统一实验设置（24L）

| 项 | 配置 |
|:--|:--|
| 模型深度 | 24L |
| checkpoint | 40000 |
| Round1/2 层位 | 2, 6, 10 |
| Round1/2 采样 | 96 samples |
| Round3 采样 | 64 samples / domain |
| max_length | 128 |
| Round1 SVD rank | 96 |
| Round2 噪声 | σ = 0.01, 0.05, 0.1, 0.5 |
| Round0 任务 | arc_easy, arc_challenge, piqa, hellaswag, openbookqa, winogrande, boolq |

## 5. Round1：专家低秩结构与路由几何（24L）

### 5.1 核心指标

| 模型 | ED↓ | ED_comp↓ | Overlap@r↓ | RandED | SVD_LR_ED↓ |
|:--|--:|--:|--:|--:|--:|
| low_rank | 69.76 | **64.12** | 0.290 | 82.92 | N/A |
| linear_running_center | **69.62** | 66.85 | **0.284** | 78.74 | 80.93 |
| linear_no_center | 70.90 | 63.79 | NaN | **64.95** | **63.37** |
| acp_on | 72.06 | 66.47 | 0.310 | 78.66 | 79.45 |

### 5.2 ED 与 ED_comp 计算公式

**ED（有效维度）**：

$$ED(e) = \frac{\left(\sum_{j=1}^{D} \lambda_j\right)^2}{\sum_{j=1}^{D} \lambda_j^2}$$

其中 $\lambda_j$ 为专家输入协方差矩阵 $C_{E_i}$ 的特征值（eigvalsh 降序排列）。

**ED_comp（补偿后有效维度）**：

通过 pool 重采样补偿消除专家负载不均衡对 ED 估计的系统性偏差：

1. 对每个 expert $e$，收集 chunk 内 ED 样本集合 $\mathcal{V}_e = \{ED_1, ..., ED_{n_e}\}$；
2. 计算中位 chunk 数 $t = \text{median}(\{n_e | n_e > 0\})$；
3. 对 $n_e < t$ 的 expert，从备用 pool 中有放回重采样，补足至约 $t$ 个 chunk；
4. 取补偿后 $\text{ED\_comp}(e) = \text{mean}(\mathcal{V}_e^{\text{compensated}})$。

### 5.3 子空间夹角口径与结果

Round1 的 `Overlap@r` 对应主夹角余弦平方均值：

`Overlap(i,j) = (1/r) * ||U_i^T U_j||_F^2 = (1/r) * Σ cos²θ_k`

可换算为等效平均夹角：

`θ_eff = arccos(sqrt(Overlap@r))`

| 模型 | Overlap@r↓ | θ_eff↑ |
|:--|--:|--:|
| linear_running_center | **0.284** | **57.84°** |
| low_rank | 0.290 | 57.39° |
| acp_on | 0.310 | 56.16° |
| linear_no_center | NaN | 无法定义（负载不均衡） |

### 5.4 边界条件与公平性处理口径

1. **训练端公平约束**：采用 `lb_loss = N * Σ(P_i * f_i)`，其中 `P_i` 为软概率质量，`f_i` 为专家负载占比；单专家过载时两项同步升高，惩罚增强。  
2. **归一化公平**：`f_i` 分母使用 `T * top_k`，保证不同 `top_k` 配置间可比。  
3. **数值边界**：Top-k 概率归一化使用 `clamp_min(1e-9)`，规避分母接近 0。  
4. **评测可靠性筛选**：仅 `tokens >= min_tokens_per_expert` 的 expert 参与 `ED_reliable / Overlap` 统计；低样本专家单独记录。  
5. **极端不均衡处理**：有效 expert 数不足或子空间秩不可定义时返回 `NaN`，避免伪造“0干扰”。

### 5.5 Round1 深度结论

- **low_rank 的优势是“补偿维度压缩 + 负载均衡”**，而非所有几何指标都第一。  
- **linear_running_center 的几何分离（Overlap/夹角）更优**，说明 center 机制在专家隔离上更稳定。  
- **linear_no_center 是高风险极端态**：某些指标漂亮（如 SVD_LR_ED）但不可解释性强，且与其他轮次结果冲突。

## 6. Round2：特征微扰鲁棒性（24L）

### 6.1 总体结果（CR，越高越稳）

| σ | linear_no_center | linear_running_center | acp_on | low_rank |
|--:|--:|--:|--:|--:|
| 0.01 | **1.0000** | 0.9988 | 0.9991 | 0.9986 |
| 0.05 | **1.0000** | 0.9955 | 0.9947 | 0.9941 |
| 0.10 | **1.0000** | 0.9909 | 0.9906 | 0.9886 |
| 0.50 | **1.0000** | 0.9500 | 0.9496 | 0.9430 |

### 6.2 深度结论

- **H1d（低秩更抗噪）在 24L 上不成立**：低秩在大噪声下最脆弱。  
- `linear_no_center` 的“满分鲁棒性”并非真实鲁棒，而是**路由过度刚性**导致扰动难以翻转 top-1。  
- `linear_running_center` 与 `acp_on` 表现接近，属于“可控退化”的工程可用区间。

## 7. Round3：谱域干扰与域间可分性（24L）

### 7.1 结果

| 模型 | Mean SI↓ | Mean Margin_A↑ | Mean Margin_B↑ |
|:--|--:|--:|--:|
| low_rank | **0.6389** | 0.999 | 1.066 |
| linear_running_center | 0.6763 | 1.235 | 1.329 |
| acp_on | 0.6895 | 1.192 | 1.289 |
| linear_no_center | 0.7952 | **2.232**（因为存在很大的负载不均衡） | **2.047** |

### 7.2 深度结论

- **H1e 在 24L 口径得到支持**：low_rank 显著降低 SI，表明跨域谱干扰更小。  
- 但 low_rank 的 Margin 并不最高，提示“低干扰”与“高置信”并非同一目标。  
- `linear_no_center` 再次出现“Margin 高但 SI 也高”的冲突现象，说明其决策极化并不等于跨域隔离。

## 8. Round0：下游任务表现（24L）

### 8.1 分任务结果

| 模型 | arc_challenge | arc_easy | boolq | hellaswag | openbookqa | piqa | winogrande |
|:--|--:|--:|--:|--:|--:|--:|--:|
| linear_running_center | **0.2611** | **0.4840** | 0.5434 | **0.3951** | **0.3120** | **0.6817** | 0.4988 |
| low_rank | **0.2611** | 0.4630 | 0.5648 | 0.3862 | 0.2980 | 0.6746 | 0.5091 |
| acp_on | 0.2500 | 0.4743 | **0.6055** | 0.3923 | 0.2940 | 0.6768 | 0.5170 |
| linear_no_center | 0.2466 | 0.4646 | 0.5966 | 0.3525 | 0.3000 | 0.6518 | **0.5225** |

### 8.2 均分与冠军结构

| Rank | 模型 | 平均分↑ | 领先任务数 |
|:--:|:--|--:|--:|
| 1 | acp_on | **0.4586** | 1 |
| 2 | linear_running_center | 0.4537 | **5** |
| 3 | low_rank | 0.4510 | 1 |
| 4 | linear_no_center | 0.4478 | 1 |

### 8.3 深度结论

- 若看 **平均分**：`acp_on` 第一。  
- 若看 **全面性**：`linear_running_center` 在 5/7 任务领先，是更稳健主力。  
- `low_rank` 在结构指标侧优势明显，但任务侧未转化为第一，验证“结构-性能解耦”。

## 9. 跨轮次联合分析（24L）

### 9.1 指标耦合矩阵（定性）

| 指标对 | 关系判断 | 证据 |
|:--|:--|:--|
| ED_comp vs SI | 同向偏正相关 | low_rank 在两者均优 |
| Overlap vs SI | 非强耦合 | linear_running_center Overlap优，但 SI不及 low_rank |
| SI vs 下游均分 | 弱相关/解耦 | low_rank SI最优但均分第3 |
| Margin vs SI | 可冲突 | linear_no_center Margin最高但 SI最差 |
| CR vs 下游均分 | 非单调 | linear_no_center CR最高但综合任务最弱 |

### 9.2 工程解释

1. **结构指标是必要非充分条件**：能约束路由几何，但无法保证任务收益。  
2. **center 机制贡献“稳定基线”**：在多指标上最均衡，是当前默认优选。  
3. **ACP 更偏任务收益增强器**：提升某些任务（如 boolq）但不保证谱干扰最优。  
4. **low-rank 更偏结构治理器**：压低 SI/ED_comp，但需配合训练策略把结构收益转译到任务端。

## 10. v4→v5 的关键迁移结论

1. **研究对象升级**：从“12L 的局部验证”升级为“24L 的全链路对照”。  
2. **证据强度升级**：v5 同时覆盖 Round0/1/2/3，避免单轮次结论偏差。  
3. **假设状态更清晰**：
   - H1b、H1e：在 24L 上获得可复现支撑；
   - H1d：在 24L 上暂不支持；
   - 新增“结构-性能解耦”作为核心结论。  
4. **决策建议可执行**：
   - 默认生产候选：`linear_running_center`（均衡）；
   - 谱干扰优先：`low_rank`；
   - boolq 等布尔推理优先：`acp_on`；
   - 不建议主线采用：`linear_no_center`（极端刚性导致多指标冲突）。

## 11. 冲突修正记录（v5 新增）

| 项目 | 修正说明 | 依据 |
|:--|:--|:--|
| Round1 子空间口径 | 统一使用 `Overlap@r` 与等效夹角 `θ_eff` 解释，避免“Overlap/夹角”混用歧义 | round1230 报告 Round1 段落 |
| 负载公平描述 | 明确区分训练端 `lb_loss` 与评测端 `CV_load + min_tokens`，避免将两者混为一个指标 | 训练/评测实现口径 |
| 版本定位 | v5 明确标注为 24L 存档，避免与 v4（12L 主线）混读 | 本文件版本说明 |

## 12. 数据与文档索引（24L）

- 总报告：`/data/250010109/spectral_router/exp_expert_lowrank/docs/round1230_4models_ckpt40000_report.md`
- Round1：`/data/250010109/spectral_router/exp_expert_lowrank/output/round1_expert_low_rank_24L_ckpt40000_4models`
- Round2：`/data/250010109/spectral_router/exp_expert_lowrank/output/round2_feature_perturbation_24L_ckpt40000_4models`
- Round3：`/data/250010109/spectral_router/exp_expert_lowrank/output/round3_spectral_interference_24L_ckpt40000_4models`
- Round0：`/data/250010109/spectral_router/exp_expert_lowrank/output/round0_downstream_ckpt40000_24L_4models_fulltasks`

## 13. 下一步建议（v5.1 规划输入）

1. **多 checkpoint 轨迹化**：在 24L 上补 `20k/30k/40k/50k/60k` 的统一四轮评测，做趋势而非点估计。  
2. **结构指标可转译性实验**：围绕 low_rank 增加轻量校准（如 router 温度/辅助损失权重）观察 SI→Acc 的可转移性。  
3. **极端模型治理**：针对 `linear_no_center` 增加负载上限或软中心机制，验证是否能保留其 CR 优势同时降低 SI。  
4. **假设收敛标准**：将 H1c 从间接证据升级为直接证据（专家权重更新方向的主子空间重叠追踪）。

---

*更新时间：2026-03-25（基于 24L ckpt40000 四轮综合结果重写）*
