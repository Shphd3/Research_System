# \[调研]MoE - 迭代状态存档 v4.3 (谱空间正交化与遗忘抵抗实验)

## 1. 当前主线目标 (North Star)

探索基于 Multi-head Attention 表征的连续谱分解（Spike & Tail），构建高纯度的低秩路由机制以实现**持续学习 (Continual Learning, CL)**。
当前迭代（Round 3）的核心目标：**建立并验证“低秩路由 $\rightarrow$ 专家谱空间容量未饱和 $\rightarrow$ 跨任务正交性提升 $\rightarrow$ 避免灾难性遗忘”的完整数学因果链。**

## 2. 核心假设全景 (Hypotheses Tracking)

*(注：保留所有历史假设以追踪思维演进，当前重点验证的假设已加粗标出)*

- **H1a \[活跃/已修正] (Spike 的双重属性与决策流形)**：Spike 承载宏观共性特征，Tail 承载微观特征。低秩约束迫使路由器仅依赖 Spike 进行决策。
- **H1b \[已实证] (低秩瓶颈引发共适应与协方差坍缩)**：低秩信息瓶颈在训练中迫使进入专家的表征流形高度同质化，实证表现为 $ED$（有效维度）大幅下降。
- **H1c \[活跃] (参数更新的低维投影限制)**：由于输入 $ED$ 下降，专家网络权重的梯度更新将被自然限制在低维子空间内。
- **H1d \[未证伪/已降级] (抗噪性悖论)**：低秩路由对高斯白噪声的敏感度并未显著低于全秩模型（Round 2 结论），该假设与持续学习的因果关联较弱，当前暂缓探究。
- **👉 H1e \[当前核心/待验证] (谱空间容量未饱和假说 Spectral Capacity Under-saturation)**：
  低秩路由通过压低 $ED$，使得每个专家仅在极少数 Spike 方向上建立了激活响应，保留了海量的**正交零空间 (Orthogonal Null Space)**。当新任务（Domain Shift）到来并被路由至该专家时，新任务的特征大概率落在未被占据的正交方向上，从而避免了对旧知识主轴的谱干扰（Spectral Interference），这是实现持续学习防遗忘的根本物理机制。

## 3. 数学模型构建 (Mathematical Formalization)

定义跨任务**专家内谱干扰度 (Intra-Expert Spectral Interference, $\mathcal{I}$)**：
针对特定专家 $i$，设 Domain A 和 Domain B 数据的输入协方差矩阵分别为 $C\_{A,i}$ 和 $C\_{B,i}$。
$$\mathcal{I}_i = \frac{\text{Tr}(C_{A,i} C\_{B,i})}{|C\_{A,i}|_F |C_{B,i}|\_F}$$
该指标衡量了两个不同领域的知识在同一个专家权重空间内发生碰撞和相互覆写的剧烈程度。

## 4. 实验迭代记录 (Experiment Design & Records)

- **第三轮** ✅ 已完成
  - **目标**：验证 H1e（谱空间容量未饱和假说）。
  - **实验内容**：证明低秩路由器在面对宏观领域偏移（Domain Shift）时，能在同一个专家内部维持显著更低的跨领域谱干扰度（$\mathcal{I}$）。
  - **实验步骤：操作步骤**：
    - <br />
      1. **数据与表征准备**：从 WOS 数据集中提取两个语义无交集的数据子集（例如 Domain A: `CS/Math`，Domain B: `Medical`）。
    - <br />
      1. **对比路由分配**：
      - 使用标准训练的全秩模型 `linear_running_center` 进行分发。
      - 使用标准训练的低秩模型 `low_rank_running_center` 进行分发。
    - <br />
      1. **计算指标 (Observable)**：
      - 分别将 Domain A 和 Domain B 的文档独立输入模型。
      - 针对上述两种模型，分别收集进入每个 Expert $i$ 的 Domain A Token 集合 $X\_{A,i}$ 和 Domain B Token 集合 $X\_{B,i}$。
      - 计算对应的协方差矩阵 $C\_{A,i}$ 和 $C\_{B,i}$。
      - 计算并对比不同路由策略下，全模型的平均谱干扰度：$\bar{\mathcal{I}} = \frac{1}{E} \sum\_{i} \frac{\text{Tr}(C\_{A,i} C\_{B,i})}{|C\_{A,i}|_F |C_{B,i}|\_F}$。
      - 写 Round 3 提取激活值 $X\_{A,i}, X\_{B,i}$ 脚本的同时，顺手把路由器的输出 Logits 也记录下来。我们只需多写两行代码，计算一下所有样本的 Top-1 logit 减去 Top-2 logit 的差值（Margin），考虑margin的影响。
    - **验证标准**：如果 $\bar{\mathcal{I}}(low\_rank) \ll \bar{\mathcal{I}}(linear)$，则说明低秩路由确实通过保留正交零空间，在数学底层上极大地减弱了跨领域特征碰撞，H1e 假说成立。
  - **产物路径**：
    - 代码：`scripts/round3/run_round3_spectral_interference.py`
    - ckpt50000 结果：`output/round3_spectral_interference_ckpt50000_v2`
    - ckpt60000 结果：`output/round3_spectral_interference_ckpt60000_v2`
    - 报告：`docs/round3_spectral_interference/experiment_report.md`
  - **详细结果**：见下方「第三轮实验结果」章节

### 第三轮实验结果 (Round 3 - Spectral Interference + Margin)

#### 3.1 实验设置

| 参数                            | 值                                                         |
| :---------------------------- | :-------------------------------------------------------- |
| **Dataset**                   | WOS (Web of Science)                                      |
| **Domain A**                  | CS, Civil, ECE, MAE (Engineering)                         |
| **Domain B**                  | Medical, Psychology, biochemistry (Medical/Life Sciences) |
| **max\_samples\_per\_domain** | 64                                                        |
| **layers**                    | 2, 6, 10                                                  |
| **checkpoints**               | 50000, 60000                                              |

#### 3.2 核心结果

| 模型                            | ckpt=50000 SI | ckpt=60000 SI | Margin (ckpt=50000) | Margin (ckpt=60000) |
| :---------------------------- | ------------: | ------------: | ------------------: | ------------------: |
| **Linear**                    |        0.6687 |        0.6678 |              1.7297 |              1.7531 |
| **Low-rank**                  |        0.7021 |        0.6990 |              1.8284 |              1.8668 |
| **Delta (Low-rank - Linear)** |   **+0.0333** |   **+0.0312** |         **+0.0987** |         **+0.1138** |

#### 3.3 分层结果

| Layer | Linear SI (ckpt=50000) | Low-rank SI | Delta SI |
| :---- | ---------------------: | ----------: | -------: |
| L2    |                 0.6782 |      0.7205 |  +0.0423 |
| L6    |                 0.6753 |      0.7238 |  +0.0485 |
| L10   |                 0.6526 |      0.6618 |  +0.0092 |

#### 3.4 关键发现

**发现 1：H1e 谱干扰降低假说 未获支持** ❌

- Low-rank 的谱干扰度（SI）比 Linear 高约 **+0.03**
- 所有三层都显示 Low-rank 的 SI > Linear
- Layer 6 差异最大（Δ=+0.0485 @ ckpt=50000）

**发现 2：Margin 意外增大** ✅

- Low-rank 的 Margin 显著高于 Linear（约 **+0.1**）
- 说明低秩路由在做决策时 **更加确信**
- 这与"低秩路由更依赖少数方向"的理论一致

#### 3.5 假设验证结论

| 假设             | 状态        | 证据                              |
| :------------- | :-------- | :------------------------------ |
| H1e (谱干扰降低)    | ❌ **未支持** | Low-rank SI 比 Linear 高 +0.03    |
| H1e (Margin增大) | ✅ **新发现** | Low-rank Margin 比 Linear 高 +0.1 |

#### 3.6 结果分析

**为什么低秩路由的谱干扰更高？**

1. **决策空间受限**：低秩路由器只利用少数 Spike 方向决策，当两个领域落在相似方向时会被路由到同一专家，导致干扰增加。
2. **正交零空间并非真正空闲**：H1e 假设正交空间是"空闲"的，但实验表明这些方向可能仍被旧任务占据。
3. **Domain 划分仍有重叠**：Engineering 和 Medical 领域可能存在较多共享语义。

**为什么低秩路由的 Margin 更大？**

1. \*\* logits 极值化\*\*：低秩投影（down\_proj + up\_proj）压缩信息，使 Top-1 vs Top-2 差异更明显。
2. **专家选择更极端**：低秩路由更确信地选择特定专家。

***

## 5. 后续研究建议

### 5.1 短期（验证 H1e 修正版）

1. **修正 Domain 划分**：使用更无交集的领域（如 CS vs Law 或 CS vs Finance）
2. **引入教师模型**：使用 CLIP 或其他语义距离更大的模型进行 Domain 聚类
3. **时序干扰分析**：不仅测 Static SI，还要测训练过程中的动态 SI 变化

### 5.2 中期（探索 Margin 与 SI 的关联）

1. **Margin 分层分析**：按 Margin 大小分层计算 SI，观察是否 Margin 越大 SI 越高
2. **噪声注入对照**：在高噪声输入下计算 Margin 和 SI，验证鲁棒性

### 5.3 长期（完整因果链验证）

1. **权重更新轨迹**：追踪专家权重在 Domain Shift 后的变化方向
2. **正交空间利用率**：计算专家激活向量在正交空间的投影占比
3. **持续学习下游任务**：在真实持续学习任务（如连续微调多个 Domain）上验证防遗忘效果

