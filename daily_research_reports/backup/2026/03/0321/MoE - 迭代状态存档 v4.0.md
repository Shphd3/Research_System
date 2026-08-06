# [调研]MoE - 迭代状态存档 v4.0

## 1. 当前主线目标 (North Star)
探索基于 Multi-head Attention 表征的连续谱分解（Spike & Tail），构建高纯度的低秩路由机制。旨在通过严格的数学建模，不仅实现更优的专家专门化，更进一步探究低秩 MoE 架构如何在物理统计特征（Common vs Long tail）层面解决灾难性遗忘问题，最终给出一个具备抗遗忘特性的模型架构。

## 2. 背景与理论基石 (Background & Math Foundation)
- **多头表征的三段连续谱理论**：大模型多头表征空间并非二元的“信号+噪声”，而是呈现长尾的谱分层。特定层不同 Head 的输出表征矩阵 $X$ 经去均值与 SVD 分解后，可被严格划分为：$X = X_{spike} + X_{middle} + X_{deep}$。
  - **Spike (Top 10%-25%)**：高密度压缩的宏观路由共性语义，承载了绝大部分领域分类信息。
  - **Middle Tail (25%-50%)**：渐变过渡区，编码细粒度、弱语义特征（Unique）。
  - **Deep Tail (>50%)**：高维各向同性噪声，在优化理论上与宏观标签完全独立，强行保留会引发容量陷阱。
- **均值与特异性偏移**：不同领域的均值向量 $\mu$ 极度共向（余弦相似度 >0.99），编码通用格式；去均值后的主成分（Centered PC）才承载了用于路由的特异性语义。

## 3. 当前假说 (Current Hypotheses)
- **H1 (路由纯净度与专家低秩性)**：去除均值并约束路由空间于 Spike 流形（如显式低秩投影），是避免网络陷入 Deep Tail 高维噪声陷阱的核心数学条件。纯净的语义分发能大幅降低进入各专家数据的有效特征维度（Effective Dimension, ED）。同时，Spike 路由如实反映流形先验，与工程上的负载均衡目标在数学上是解耦的。
- **H2 (多头一致性的动态演化)**：不同 Head 之间的 Spike 子空间由约 30%-40% 的“共享语义核”和 60%-70% 的“特异性视角”组成。且这种共识随网络深度动态演化，深层网络在主空间对宏观语义的共识更强烈。
- **H3 (世界知识的物理统计特征 - 核心前提假设)**：**【注意：此为当前亟待验证的先验假设】** 世界知识在自然界中的分布由 Common（宏观共性规律）和 Long Tail（微观特异性细节）组成。我们假设，网络激活值表现出的 Spike 与 Tail 的谱分布，**完全是由训练数据本身固有的这种物理统计特征所驱动和塑造的**，而非网络架构的副产物。
- **H4 (知识解耦与抗遗忘机制)**：基于 H3 的假设，Multi-head MoE 具备抗遗忘能力，是因为基于 Spike 的纯净路由将不同簇的 Common 知识稳定锚定在不同专家中。由于专家处理的数据内蕴秩（Intrinsic Rank）被压缩，后续 Long Tail 知识的持续学习（梯度更新），在几何空间上被严格限制在特定专家的低维剩余子空间（或正交子空间）内，从而极难发生干涉，无法破坏（Overwrite）已经建立的主轴 Common 知识权重。
- **H5 (低秩路由驱动的防遗忘)**：若在架构上强制路由矩阵为低秩（Low-Rank Router），不仅能提升特征学习效率，还能从根本上过滤掉导致梯度随机游走的 Deep Tail 噪声，结构化地保证专家网络输入空间的低秩性，从而实现“不遗忘语义”的理想模型。

## 4. 预想的实验结构：第五轮 (Experiment Design: Round 5)
- **目标**：验证 H3、H4 与 H5，严格量化低秩路由机制（结构化压缩内蕴秩）对阻断灾难性遗忘的数学有效性，并反向印证谱分布与数据统计特征的绑定关系。
- **实验范式**：Task-Incremental Continual Learning (CL) 设置。设定序列任务集合 $\mathcal{T} = \{T_1, T_2, \dots, T_N\}$，在此构建包含基础常识与互斥领域知识的序列（例如：$T_1$ 为维基百科通用知识，$T_2$ 为医疗专业问答，$T_3$ 为法律逻辑推理）。
- **操作步骤**：
  1. **构建对比架构矩阵**：
     - **Baseline (Dense)**：标准稠密模型，用于提供遗忘的绝对上限基准。
     - **MoE Baseline (Full-Rank Router)**：标准全秩路由 MoE（$Y = WX$），考察稀疏激活本身自带的抗遗忘能力。
     - **CLRR-MoE (Centered Low-Rank Router)**：去均值低秩路由 MoE。强制路由空间维度 $r \ll d$（提取 Spike）。
  2. **序列化训练与梯度追踪 (Sequential Training)**：
     - 在 $T_k$ 上训练时，仅开放当前步的损失函数 $\mathcal{L}_{k}$，不使用 Replay Buffer，以施加最极端的遗忘压力。
     - 追踪记录每个 Expert 内部的权重更新范数 $\|\Delta W_E^{(k)}\|_F$ 以及其更新梯度的方向矩阵，观察其是否严格限制在输入表征的零空间（Null Space）或极小特征值空间内。
  3. **计算严格的 CL 评估指标**：
     - **Average Accuracy (ACC)**：所有学习过的任务的平均表现。$ACC = \frac{1}{N} \sum_{i=1}^{N} R_{N,i}$ （$R_{N,i}$ 为完成 $N$ 个任务后在任务 $i$ 上的准确率）。
     - **Forgetting Measure (FM)**：量化旧知识的被破坏程度。$FM = \frac{1}{N-1} \sum_{i=1}^{N-1} \max_{j \in \{1, \dots, N-1\}} (R_{j,i} - R_{N,i})$。期望低秩路由的 $FM \to 0$。
  4. **动态内蕴秩监测 (Monitor Intrinsic Rank & ED)**：
     - 针对每一个 Expert $E_i$，收集进入该专家的激活值协方差矩阵 $C_{E_i} = \frac{1}{M} \sum (x_m - \bar{x})(x_m - \bar{x})^T$。
     - 持续计算特征值谱 $\{\lambda_1, \lambda_2, \dots, \lambda_d\}$ 并得出 Effective Dimension (ED)：$ED = \frac{(\sum \lambda_i)^2}{\sum \lambda_i^2}$。验证是否 $\forall T_k$，$ED_{CLRR}$ 始终被稳定压制在低位。

- **当前挑战**：如何在持续学习的漂移过程中，防止 CLRR 路由器自身的低秩投影基向量（Spike 主轴）发生灾难性旋转？是否需要引入 SVD 约束项或冻结前序任务的主轴？

## 5. 预期结果与更新准则 (Expected Results & Update Rule)
- **预期结果**：
  - **抗遗忘验证**：CLRR-MoE 的遗忘指数 $FM$ 显著低于 Full-Rank MoE 和 Dense 模型，证明强制截断 Tail 能从几何上保护 Common 知识。
  - **低秩约束验证**：CLRR-MoE 中各 Expert 的 $ED$ 呈平缓状态，未出现随新任务加入而导致的维度爆炸；同时，新任务的参数更新梯度与旧任务的主特征子空间高度正交。
- **更新策略**：
  - 如果 CLRR 依然发生严重遗忘，且发现 Router 自身的路由分布发生了剧烈突变，说明低秩特征虽好，但在 CL 设置下是不稳定的。防遗忘机制需进一步干预路由器的更新（例如采用正交梯度投影 OGP 保护 Router 权重）。
  - 若发现强行限制低秩导致新任务（Long Tail 知识）的学习准确率（Forward Transfer）极低，说明我们的 $r$ 设置过于严苛，或者 H3 假设有局限（Long Tail 知识不仅需要专家内的微调，也需要路由器提供新的分发流形），此时需要探究动态扩容或软阈值松弛机制。

---

## 6. 阶段性方法设计支持 (Methodology Design Based on Current Evidence)
基于前四轮针对连续谱与去均值特征的确定性结论，我们在当前架构上可以立刻引入以下三种核心设计：

1. **去均值低秩路由器 (Centered Low-Rank Router, CLRR)**
   - **理论支撑**：均值包含非特异性的结构偏移，真正的宏观路由信息高度压缩在极少数主成分中；全秩线性探测会不可避免地引入 Deep Tail 噪声，引发优化路径上的游走。
   - **设计**：设计带有 Batch / Layer 级滑动均值追踪的 Router。
     $$X_{centered} = X - \mu$$
     $$Logits = W_{up} (W_{down} X_{centered})$$
     其中 $W_{down} \in \mathbb{R}^{d \times r}$（提取 Spike 共性投影），$W_{up} \in \mathbb{R}^{r \times E}$（完成分发映射），$r \approx 0.15d$。此举能彻底切断 Deep Tail 的干扰，并保证输出的低秩流形。

2. **路由与负载均衡解耦架构 (Decoupled Semantic-Load Architecture)**
   - **理论支撑**：纯净的 Spike 路由会忠实反映数据的先验分布。在损失函数中强加辅助的 Load Balancing Loss，会用优化器强行扭曲几何空间，导致 Router 偏离 Spike 流形，被迫利用高维噪声（Tail）来凑配容量。
   - **设计**：Router 的前向传播**完全无约束**地遵循 CLRR 计算出的语义 Logits。负载均衡交由**异步 Buffer 与重采样策略**（即对于拥挤的 Expert 队列进行动态阈值自适应调整或 Token 路由重规划）来实现。在数学上将“特征语义纯净度”与“显存负载限制”进行物理分层。

3. **深度感知的频率自适应门控 (Depth-Aware Frequency-Adaptive Gating)**
   - **理论支撑**：实验二与实验三证实，深层网络的 Spike 重合度更强，Tail 退化为纯噪声更为彻底；而浅层网络的主空间不够聚焦，可能需要更多的 Middle Tail 细节来维持底层特征的丰度。
   - **设计**：在 CLRR 架构中，将低秩瓶颈的维度 $r$ 设计为随网络深度 $l$ 单调衰减的函数。浅层 $r_{shallow}$ 较大（保留至 Middle Tail 边界以确保特征多样性），深层 $r_{deep}$ 极小（仅保留绝对共识的核心 Spike），实现参数分配的最大化效用。