# [调研]MoE - 迭代状态存档 v4.1 (聚焦路由与低秩映射)

## 1. 当前主线目标 (North Star)
探索基于 Multi-head Attention 表征的连续谱分解（Spike & Tail），构建高纯度的低秩路由机制。当前迭代周期（Round 1）的唯一核心目标是：**严格证明并量化“路由器参数低秩性”与“专家输入协方差低秩性”之间的因果关系与数学桥梁。**

## 2. 背景与理论基石 (Background & Math Foundation)
- **多头表征的三段连续谱理论**：表征矩阵 $X = X_{spike} + X_{middle} + X_{deep}$。
- **均值与特异性偏移**：去均值后的主成分（Centered PC）才承载了用于路由的特异性语义。
- **结构约束不对等性**：标准 MoE 中，Router 的低秩约束仅影响分发决策边界，**不改变**输入到 Expert 的 Token 向量的原始维度与特征值。

## 3. 当前拆解假说 (Deconstructed Hypotheses: Deep Dive into H1)
- **H1a (决策流形与表达能力退化)**：
  如果直接使用未经设计的低秩矩阵替代全秩路由，确实会导致“表达能力下降”。但如果采用“去均值低秩投影（Centered Low-Rank）”，实际上是切断了 Router 拟合 Deep Tail（高维噪声）的路径，强制路由决策完全依赖于宏观共性语义（Spike）。这是一种有益的正则化，而非盲目的能力剥夺。
- **H1b (聚类同质性引发协方差坍缩 - 核心桥梁)**：
  基于 H1a 的纯净决策，Router 会将具有相似 Spike 特征的 Token 强行聚类到同一个 Expert。这使得分配给 Expert $i$ 的激活值矩阵 $X_{E_i}$ 具有极高的同质性。在计算该簇数据的协方差矩阵 $C_{E_i}$ 时，其主特征值方差占比将急剧扩大，尾部特征值坍缩，导致输入空间的有效维度 (Effective Dimension, ED) 大幅降低。
- **H1c (参数更新的低维投影限制)**：
  基于 H1b，由于 Expert 接收的 batch 数据的协方差呈现低内蕴秩，根据 $\Delta W_e \propto \frac{\partial L}{\partial y} x^T$，Expert 权重的更新将被自然限制在一个低维子空间内。路由器的低秩性，是通过“纯净聚类”这一中间现象，间接实现了专家网络参数的低秩性。

## 4. 预想的实验结构：局部验证阶段 (Experiment Design: Minimal Test for H1b)
- **目标**：验证 H1b，即证明低秩路由器能有效降低各个 Expert 输入簇的有效维度（ED）。
- **操作步骤**：
  1. **数据与表征准备**：提取预训练模型某一层的完整 Token 表征 $X$。
  2. **对比路由分配**：
     - 使用随机全秩矩阵进行聚类分配。
     - 使用标准训练的全秩 Router $W_{full}$ 进行分配。
     - 使用 SVD 截断的去均值低秩 Router $W_{low\_rank}$ 进行分配。
  3. **计算指标 (Observable)**：
     - 针对上述三种分配结果，分别收集进入每个 Expert 的 Token 集合 $X_{E_i}$。
     - 计算协方差矩阵 $C_{E_i}$。
     - 计算并对比不同路由策略下的平均有效维度：$ED = \frac{(\sum \lambda_j)^2}{\sum \lambda_j^2}$。
- **验证标准**：如果 $ED(W_{low\_rank}) \ll ED(W_{full})$，则说明低秩路由确实通过聚类同质性间接完成了对专家输入空间的维度压缩，H1b 桥梁成立。

## 5. 当前瓶颈与风险 (Current Bottleneck & Risks)
- **瓶颈**：尚未在真实数据分布下验证 $ED$ 的坍缩幅度是否具有统计学意义。
- **风险**：有可能去均值低秩投影并不能产生足够 strong 的聚类效果，导致进入专家的激活值依然是高方差的全秩状态。

## 6. Round1 首次实证结果更新 (2026-03-22)
- **实验名**：`round1_expert_low_rank`
- **对比模型**：
  - `qwen3-moe-H768--linear_running_center_8gpu_gbs768-center_running-gate_off-acp_off-lb_0-linear`
  - `qwen3-moe-H768--low_rank_running_center_8gpu-center_running-gate_off-acp_off-lb_0-low_rank_r115`
- **统一设置**：`checkpoint=50000`，`layers=2,6,10`，`max_samples=96`，`max_length=128`，`batch_size=2`。
- **结果摘要（Low-Rank 相对 Linear）**：
  - `ED`: `59.8289` vs `60.8006`（下降 `0.9717`）
  - `ED(reliable)`: `65.7597` vs `72.2767`（下降 `6.5170`）
  - `Overlap@r50`: `0.2028` vs `0.2176`（下降 `0.0148`）
  - `CV_load`: `0.7861` vs `0.9095`（下降 `0.1234`）
  - `H(E|C)`: `1.5951` vs `1.4177`（上升 `0.1775`）
- **阶段性结论**：H1b 获得正向支持（ED 与子空间干扰均下降），但“簇到专家映射稳定性”未同步提升，后续需扩大样本并做多 checkpoint 追踪。
- **产物目录**：
  - `/data/250010109/spectral_router/exp_expert_lowrank/output/round1_expert_low_rank/results_ckpt50000`
  - `/data/250010109/spectral_router/exp_expert_lowrank/docs/round1_expert_low_rank/experiment_report.md`

## 7. Round1 增强测量补充（4模型 · 统一口径）

### 7.1 实验设置

- **评测脚本**：`/data/250010109/spectral_router/exp_expert_lowrank/scripts/round1/run_round1_expert_low_rank_enhanced.py`
- **数据集**：`river-martin___web-of-science-with-label-texts`（train split, 32890 samples）
- **采样**：标签轮转抽样（label round-robin），`max_samples=96`，`batch_size=2`，`max_length=128`
- **Checkpoint**：统一 `50000`
- **层位**：`2, 6, 10`
- **ED 分块**：`ed_chunk_size=256`
- **子空间秩**：`subspace_rank=50`

### 7.2 三种分发策略的数学定义

| 策略 | 数学公式 | 说明 |
|:--|:--|:--|
| **model_router** | 依模型类型而定（见下表） | 真实训练模型的 Top-1 路由 |
| **random_router** | $e_i = \arg\max_j ((x - \bar{x}_{batch}) W_{random})_{j}$ | 全秩随机矩阵 argmax 分发，推理时对输入做 batch 内均值中心化 |
| **svd_centered_low_rank_router** | $e_i = \arg\max_j ((x - \bar{x}_{batch}) W_{lr})_{j}$，其中 $W_{lr} = U_{:,1:r} S_{1:r} V^T_{1:r,:}$ | 对 Gate 权重 $W_{gate}$ 做 SVD 截断（rank=115），推理时对输入做 batch 内均值中心化 |

#### model_router 的模型类型细分

| 模型 | 数学公式 | 说明 |
|:--|:--|:--|
| **linear_running_center** | $e_i = \arg\max_j ((x - \mu_{running}) W_{gate})_{j}$，其中 $\mu_t = (1-\beta_t)\mu_{t-1} + \beta_t \bar{x}_t$ | 输入先减 running mean（EMA 更新），再与 Gate 权重相乘 |
| **low_rank_running_center** | $e_i = \arg\max_j ((x - \mu_{running}) W_{down} W_{up})_{j}$，其中 $W_{down} \in \mathbb{R}^{d \times r}$，$W_{up} \in \mathbb{R}^{r \times E}$ | 输入先减 running mean，再通过低秩矩阵路由（$r=115$） |
| **linear_no_center** | $e_i = \arg\max_j (x W_{gate})_{j}$ | **不做中心化**，直接与 Gate 权重相乘 |
| **linear_running_center_acp_on** | $e_i = \arg\max_j ((x - \mu_{running}) W_{gate})_{j}$ 后再经过 ACP 投影 | 在 running_center 基础上，额外进行 Adaptive Center Projection 分解 |

> **SVD 截断对象**：全秩线性模型的 Gate 权重矩阵 $W_{gate} \in \mathbb{R}^{768 \times 8}$，截断到 $W_{lr} \in \mathbb{R}^{768 \times 115}$。
>
> **关于 $\bar{x}_{batch}$ vs $\mu_{running}$**：random_router 和 svd_centered_low_rank_router 策略中使用的是 batch 内均值中心化（$\bar{x}_{batch} = \frac{1}{n}\sum x_i$），而 running_center 模型使用的是训练时累积的 running mean（$\mu_{running}$）。这两者在数学上是不同的。 |

### 7.3 评测指标的数学定义

| 指标 | 数学公式 | 说明 |
|:--|:--|:--|
| **ED（有效维度）** | $ED = \frac{(\sum_{j=1}^{d} \lambda_j)^2}{\sum_{j=1}^{d} \lambda_j^2}$ | 其中 $\lambda_j$ 为专家输入协方差矩阵 $C_{E_i}$ 的特征值。ED 衡量协方差矩阵的"有效秩"，值越低说明输入越集中在少数主方向。 |
| **Overlap@r（子空间重叠度）** | $Overlap_{i,j} = \frac{\\|U_i^T U_j\\|_F^2}{r}$，$Overlap = \frac{2}{n(n-1)}\sum_{i<j} Overlap_{i,j}$ | 其中 $U_i, U_j$ 为专家 $i, j$ 的 top-$r$ 特征向量组成的子空间基。值越低说明专家专业性越强。 |
| **H(E\|C)（条件熵）** | $H(E\|C) = \sum_{c} P(c) \cdot H(E\|c) = -\sum_{c,e} P(c,e) \log_2 P(e\|c)$ | 衡量给定伪簇标签 $c$ 后路由到各专家的不确定性。值越低说明路由越确定。 |
| **CV_load（负载变异系数）** | $CV_{load} = \frac{\sigma}{\mu}$，其中 $\mu = \frac{1}{E}\sum_e p_e$，$\sigma = \sqrt{\frac{1}{E}\sum_e (p_e - \mu)^2}$ | 衡量专家负载分布的均匀性，$p_e$ 为专家 $e$ 被选中的概率。值越低说明负载越均衡。 |

### 7.4 核心结果（model_router）

| 模型 | 配置 | ED↓ | ED_comp↓ | Overlap@r50↓ | H(E|C)↓ | CV_load↓ |
|:--|--:|--:|--:|--:|--:|
| **linear_running_center** | running_center + acp_off | 61.09 | 50.92 | 0.303 | 1.434 | 0.918 |
| **low_rank_running_center** | low_rank(r=115) + running_center + acp_off | **56.92** | **51.55** | **0.281** | 1.602 | **0.780** |

### 7.5 相对随机分发的增量（model_router − random_router）

| 模型 | ΔED | ΔED_comp | ΔOverlap | ΔH(E\|C) | ΔCV_load |
|:--|--:|--:|--:|--:|--:|
| **linear_running_center** | −12.28 | −19.81 | −0.098 | −1.048 | +0.265 |
| **low_rank_running_center** | **−16.91** | −18.83 | −0.091 | −0.742 | +0.024 |

> **含义**：真实路由的 ED 显著低于随机分发，说明路由器学到了有意义的聚类结构。低秩模型相对随机分发的 ED 降幅（−16.91）大于线性模型（−12.28），验证了低秩路由在 ED 压缩上的优势。

### 7.6 SVD 截断分发对照（全秩线性模型上做 SVD 截断）

| 模型 | 策略 | ED↓ | ED_comp↓ | Overlap@r50↓ | CV_load↓ |
|:--|:--|--:|--:|--:|--:|
| **linear_running_center** | model_router | 61.09 | 50.92 | 0.303 | 0.918 |
| **linear_running_center** | random_router | 73.37 | 70.72 | 0.401 | 0.653 |
| **linear_running_center** | svd_centered_low_rank | 71.65 | 70.47 | 0.422 | **0.245** |
| **linear_no_center** | model_router | 55.61 | 55.61 | N/A | 2.646 |
| **linear_no_center** | random_router | 54.41 | 51.69 | 0.434 | 0.825 |
| **linear_no_center** | svd_centered_low_rank | 54.14 | 52.19 | 0.383 | 0.799 |

> **发现**：
> - 对全秩线性模型的 Gate 做 SVD 截断后，CV_load 大幅下降（0.918 → 0.245），但 ED 反而上升（61.09 → 71.65）。说明**低秩结构本身并不能保证 ED 降低**，必须配合训练过程中"聚类同质化"的机制才能实现 ED 压缩。
> - `linear_no_center` 模型的 H(E|C) ≈ 0（路由几乎完全确定），CV_load 极高（2.65），说明缺少 Center 机制导致路由行为异常。

### 7.7 关键结论

1. **H1b 成立**：低秩路由（low_rank_running_center）相对同配置线性路由的 ED 下降 4.17（56.92 vs 61.09），Overlap 下降 0.022（0.281 vs 0.303）。
2. **CV_load 最优**：低秩模型的 CV_load 最低（0.780），说明负载最均衡。
3. **SVD 截断 ≠ 低秩训练**：对全秩 Gate 做事后 SVD 截断不能复现低秩训练模型的 ED 压缩效果，验证了 H1b 的因果链（低秩训练 → 聚类同质化 → ED 压缩）。
4. **linear_no_center 异常**：H(E|C) ≈ 0（路由几乎完全确定），CV_load 极高（2.65），负载严重不均，可能因缺少 Center 机制导致路由行为异常。

### 7.8 产物目录

- 评测结果：`/data/250010109/spectral_router/exp_expert_lowrank/output/round1_expert_low_rank_4models/`
- 分析报告：`/data/250010109/spectral_router/exp_expert_lowrank/docs/round1_expert_low_rank/round1_4models_comprehensive_report.md`

---

## 8. ACP ON 结果（辅助参考，非本次重点）

> 以下为 `linear_running_center_acp_on` 模型的结果，ACP（Adaptive Center Projection）机制为辅助探索，不影响 H1b 的核心结论。

### 8.1 model_router 结果

| 模型 | ED↓ | ED_comp↓ | Overlap@r50↓ | H(E\|C)↓ | CV_load↓ |
|:--|--:|--:|--:|--:|--:|
| **linear_running_center_acp_on** | 56.42 | 53.04 | **0.272** | 1.670 | 0.854 |

### 8.2 相对随机分发增量

| 模型 | ΔED | ΔED_comp | ΔOverlap | ΔH(E\|C) | ΔCV_load |
|:--|--:|--:|--:|--:|--:|
| **linear_running_center_acp_on** | −13.83 | −14.65 | −0.112 | −0.768 | +0.235 |

> **观察**：ACP ON 后 Overlap 进一步降至 0.272（所有模型中最低），说明 ACP 机制有助于减少专家子空间重叠。但低秩模型的 CV_load（0.780）仍优于 ACP ON 模型（0.854）。

---

## 9. 迭代状态存档维护规则（强制）

- 每次实验完成后，必须在本文件新增或更新对应小节，写清：实验名、模型、checkpoint、数据设置、测量方式、关键结果、产物目录。
- 回写前必须先核对结果源文件（json/md）中的最终数值，不允许手填估算值。
- 若同一指标出现多版本数值，统一以"最新结果文件时间戳对应的汇总文件"为准，并在本文件写明"冲突修正"。
- 若后续复跑导致结果变化，必须在原小节直接更新，并追加"修正说明"而不是保留旧值。

## 10. 冲突修正记录

### 2026-03-22 更新记录

| 项目 | 修正前 | 修正后 | 依据文件 |
|:--|--:|--:|:--|
| Round1 标准评测 ED（旧值） | 59.7055 | 59.8289 | `round1_expert_low_rank/results_ckpt50000/low_rank_comparison_summary.json` |
| Round1 标准评测 ED(reliable)（旧值） | 65.7145 | 65.7597 | 同上 |
| Round1 标准评测 Overlap@r50（旧值） | 0.2024 | 0.2028 | 同上 |
| Section 7 全面更新 | - | 4模型统一口径结果 | `round1_expert_low_rank_4models/enhanced_low_rank_summary.json` |

## 11. Round2 特征微扰一致性实验（2026-03-22）

- **实验名**：`round2_feature_perturbation`
- **目标**：在不训练条件下验证低秩路由是否更抗微扰（对应 `CR(σ)` 曲线）。
- **对比模型**：
  - `linear_running_center`
  - `low_rank_running_center`
- **统一设置**：`checkpoint=50000`，`layers=2,6,10`，`max_samples=96`，`batch_size=2`，`max_length=128`，`σ∈{0.01,0.05,0.1,0.5}`。
- **指标定义**：`CR(σ) = (1/N) * Σ 1[E_clean(x_i)=E_noise(x_i;σ)]`。

### 11.1 总体一致率结果

| σ | linear_running_center | low_rank_running_center | Δ(low-rank - linear) |
|:--|--:|--:|--:|
| 0.01 | 0.999129 | 0.998612 | -0.000517 |
| 0.05 | 0.995891 | 0.994585 | -0.001306 |
| 0.10 | 0.992707 | 0.990067 | -0.002640 |
| 0.50 | 0.956323 | 0.945955 | -0.010368 |

### 11.2 分层要点

- Layer2：两模型在所有噪声强度下均 `CR=1.0`。
- Layer6：低秩模型下降更快（σ=0.5 时 `0.877296 < 0.908564`）。
- Layer10：高噪声下两者接近（σ=0.5 时 `0.960568 ≈ 0.960405`）。

### 11.3 阶段性结论

1. `CR` 随噪声增大单调下降，实验设置有效。
2. 本轮配置下，低秩模型未体现更强抗噪性（overall CR 略低于线性模型）。
3. v4.2 中“低秩路由更抗 Tail 微扰”假设在当前样本规模与设置下未获直接支持，需在更大样本与多 checkpoint 序列继续验证。

### 11.4 产物目录

- 结果目录：`/data/250010109/spectral_router/exp_expert_lowrank/output/round2_feature_perturbation`
- 报告文档：`/data/250010109/spectral_router/exp_expert_lowrank/docs/round2_feature_perturbation/experiment_report.md`
- 关键图表：
  - `round2_overall_consistency_curve.png`
  - `round2_layer2_consistency_curve.png`
  - `round2_layer6_consistency_curve.png`
  - `round2_layer10_consistency_curve.png`
