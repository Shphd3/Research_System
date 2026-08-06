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
  - `ED`: `59.7055` vs `60.8006`（下降 `1.0950`）
  - `ED(reliable)`: `65.7145` vs `72.2767`（下降 `6.5622`）
  - `Overlap@r50`: `0.2024` vs `0.2176`（下降 `0.0152`）
  - `CV_load`: `0.7861` vs `0.9095`（下降 `0.1234`）
  - `H(E|C)`: `1.5951` vs `1.4177`（上升 `0.1775`）
- **阶段性结论**：H1b 获得正向支持（ED 与子空间干扰均下降），但“簇到专家映射稳定性”未同步提升，后续需扩大样本并做多 checkpoint 追踪。
- **产物目录**：
  - `/data/250010109/spectral_router/exp_expert_lowrank/output/round1_expert_low_rank/results_ckpt50000`
  - `/data/250010109/spectral_router/exp_expert_lowrank/docs/round1_expert_low_rank/experiment_report.md`

## 7. Round1 增强测量补充（随机分发 + SVD去均值低秩分发）
- **为何此前缺少随机 gating 分发结果**：首次实证脚本仅统计“真实模型路由”并做模型间比较，未把“随机全秩矩阵分发”和“全秩路由 SVD 截断分发”接入同一评测循环。
- **现已补齐**（checkpoint=50000，层2/6/10，max_samples=96）：
  - `model_router`（真实路由）
  - `random_router`（随机全秩矩阵 argmax 分发）
  - `svd_centered_low_rank_router`（在全秩线性路由模型上，用 gate 权重做 SVD 截断并对输入去均值后分发）
- **测量方式（当前统一口径）**：
  - 数据多样化：按标签轮转抽样（label round-robin），避免单标签主导。
  - 跨模型一致性：先固定同一批 tokenized batches，再用 `batch_signature` 做一致性校验。
  - 过载专家 ED：对每个专家按 `t_s // 256` 次分块计算 ED 并取均值（`ed_chunk_size=256`）。
  - 不均衡补偿：对测量次数不足的专家，基于池样本重采样得到 `ED_comp`（补偿统计）。
  - 子空间重叠：计算 `Overlap@r50`，并同时报告随机子空间期望 `r/d` 与 excess。
- **增强结果摘要**：
  - 线性模型：`ED(model)=61.0928`，`ED(random)=73.3719`，`ED(svd_centered_low_rank)=71.6543`
  - 低秩模型：`ED(model)=56.9206`，`ED(random)=73.8329`
  - 低秩 vs 线性（真实路由）：`ED 56.9206 < 61.0928`，`Overlap 0.2806 < 0.3028`，`CV_load 0.7796 < 0.9177`，`H(E|C) 1.6024 > 1.4343`
  - 说明真实训练路由在 ED 压缩与子空间分离上显著优于随机分发，且低秩模型相对随机分发的 ED 降幅更大。
- **增强产物目录**：
  - `/data/250010109/spectral_router/exp_expert_lowrank/output/round1_expert_low_rank/enhanced_ckpt50000`
  - `/data/250010109/spectral_router/exp_expert_lowrank/docs/round1_expert_low_rank/round1_enhanced_report.md`
