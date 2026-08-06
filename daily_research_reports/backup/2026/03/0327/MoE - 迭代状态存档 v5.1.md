# [调研]MoE - 迭代状态存档 v5.1

## 1. 当前主线目标 (North Star)
探索并验证“去偏二阶路由 (Debiased Second-Order Routing)”机制。通过在数学底层消除特征的一阶与二阶均值漂移（期望偏移），解决路由器的初始化负载坍塌问题；同时利用二阶协方差特征实现领域间的严格正交隔离，促使专家接收低秩输入，最终实现抗遗忘的持续学习 (Continual Learning)。

## 2. 背景与理论基石 (Background & Math Foundation)
- **现象 1 (The Curse of Mean Bias)**：LLM 激活值存在巨型的 Rank-1 均值漂移 $\mu$。未去均值时，路由 Logit 的方差由 $\mu$ 主导，导致 Step-0 的 Softmax 赢者通吃（初始化坍塌）。
- **现象 2 (Limits of Linear Routing)**：一阶去均值 $x_c = x - \mu$ 解决了负载坍塌，但不同领域的数据往往具有相同的零均值和不同的协方差结构。线性超平面无法高效区分“同均值、异方差”的分布。
- **理论解法 (Debiased Variance-Aware Routing)**：贝叶斯最优边界需要二次型 $r \odot r$ 来识别方差。但二次型会产生新的期望偏移 $\lambda = \mathbb{E}[r \odot r] > 0$。必须进行二阶去偏 $\tilde{q} = r \odot r - \lambda$，才能在保持特征可分性的同时，避免二次坍塌。

## 3. 当前假说 (Current Hypothesis)
- **H1 [已证实（理论），待代码验证] (初始化坍塌与均值漂移)**：无论是原始输入的一阶均值 $\mu$，还是平方特征的二阶均值 $\lambda$，只要不进行去中心化，都会在随机初始化的路由权重上产生巨大的 Logit 极差，导致 $CV_{load}$ 在 Step-0 爆炸。
- **H2 [活跃] (线性路由的方差盲区)**：仅仅使用一阶去均值（Linear Centered）的路由器，虽然能保证负载均衡，但由于缺乏二阶信息，在面对协方差差异大的 Domain 时，路由器的分类 Margin 较低，专家内部的跨领域谱干扰（SI）较高。
- **H3 [活跃/核心] (二阶去偏隔离假说)**：Debiased Second-Order Router 能够同时满足 (1) Step-0 完美负载均衡；(2) 相比线性路由，显著提高跨领域的分类 Margin；(3) 降低同一专家内部的谱干扰（SI），促使专家的输入有效维度（ED）降低。
- **H4 [活跃/远期] (持续学习假说)**：基于 H3 构造的低秩专家空间，能有效保留正交零空间，从而在面对 Domain Shift 时抵抗灾难性遗忘。

## 4. 预想的实验结构 (Expected Experiment Design)
- **模型/数据集**：Qwen3-0.6B 架构，WOS 数据集（按 Domain A/B 严格切分）。
- **实验目的**：验证 H1（消融均值漂移与坍塌的因果关系）以及 H2/H3（二阶去偏路由的正交隔离优势）。
- **实验变量**：三种路由策略
  1. `linear_centered_router`: $l = W x_c$
  2. `raw_quadratic_router`: $l = W (x_c \odot x_c)$
  3. `debiased_quadratic_router`: $l = W_1 x_c + W_2 (x_c \odot x_c - \lambda_t)$
- **实验具体步骤**：
  - **Test 1 (Step-0 Initialization Test)**：不进行反向传播。向 3 个模型输入同一批随机 Batch，记录并对比初始化状态下的 $CV_{load}$ 和选通概率分布。
  - **Test 2 (Static Routing & Domain Separation)**：训练路由器（冻结 LLM 主干）。用 WOS 的 Domain A 和 B 喂入模型，收集进入每个 Expert 的特征。
- **评估指标**：
  1. 负载均衡：$CV_{load}$ (Step-0 及 训练后)
  2. 决策确信度：分类 Margin (Top-1 logit 减去 Top-2 logit)
  3. 几何隔离度：Domain A 和 B 在专家内部的谱干扰度 (SI)，专家输入的有效维度 ($ED_{comp}$) 和子空间重叠度 (Overlap@r)。

## 5. 预期结果与更新准则 (Expected Results & Update Rule)
- **预期 1**：在 Test 1 中，`raw_quadratic` 的 $CV_{load}$ 将直接爆炸（极度不均衡），而 `linear_centered` 和 `debiased_quadratic` 的 $CV_{load}$ 极低（近乎完美均衡）。
- **预期 2**：在 Test 2 中，`debiased_quadratic` 的 Margin 显著高于 `linear_centered`，且 SI 和 Overlap 指标降低。
- **更新策略**：如果 `debiased_quadratic` 在 Test 2 中训练极不稳定或 Loss 无法收敛，需要检查 EMA 的更新率 $\beta_t$ 是否过小导致方差估计抖动，可考虑引入 Batch-level 的归一化稳定前期训练。