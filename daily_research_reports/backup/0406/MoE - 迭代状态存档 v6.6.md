# MoE - 迭代状态存档 v6.6

> 用于 0406 阶段 NeurIPS 论文收束、theory discussion、analysis planning 的唯一状态文档。

---

## 0. Metadata

- Project: CORE: Covariance-Oriented Routing for Experts in Continual Learning
- Version: v6.6
- Date: 2026-04-07
- Stage: Paper consolidation + analysis refinement
- Mode: `Convergence`

---

## 1. Current State

- 当前最强 baseline 仍然是 `acp_lite`。
- 当前主问题已经从“如何继续为旧 diagonal quadratic 辩护”转向：
  1. 为什么一阶正交解耦路由已经足够强；
  2. 二阶 / hybrid 路由为什么没有达到最初预期；
  3. 如何严格定义 `specialization` 与 `low-rankness` 的关系；
  4. 如何把这些分析写成论文可用的理论与 analysis evidence。
- 当前单一决策问题：
  **是否应将论文主线正式收束为：在高度各向异性的 LLM 表征中，一阶正交解耦路由是主导机制，而二阶 / hybrid 路由的必要性仅在特定 regime 下成立。**

---

## 2. Results Analysis

### 2.1 Real-model checkpoint audit

来源：
- `0406/round12l_ckpt40000_full_experiment_synthesis.md`
- `0406/round12340_metrics_and_implementation_ckpt40000.md`

当前可以稳定写入论文的结论：

- `acp_lite` 在现有真实模型 checkpoint audit 中仍是最强一阶 baseline。
- `linear_no_center` 是关键反例：它的高 certainty / 高 margin 主要来自 collapse，而不是有效 specialization。
- `linear_nocenter_lb001` 说明单纯 load balancing control 能缓解部分退化，但不能取代几何上更合理的 routing 设计。
- 若干 low-rank / hybrid 变体在 overlap、鲁棒性或局部几何指标上有优势，但尚未形成“全面优于 `acp_lite`”的统一证据。

### 2.2 Controlled benchmark

来源：
- `0406/summary_continuous_hmm_v5_30law_r20260407_v5full.md`

当前最清晰的 controlled 结论：

- Type 1（Mean-separable）: `linear_running_center` 最强。
- Type 2（Covariance-separable）: `subspace_energy` 最强。
- Type 3（Mixed）: `hybrid_subspace_energy` 最强。

这意味着：
- covariance-aware routing 不是 universally necessary；
- 它是 regime-dependent necessary；
- 真实 LLM 表征是否主要落在 Type 1，还是混合到 Type 2/3，需要通过 analysis audit 进一步坐实。

### 2.3 What current results support

当前结果足以支持：

- `acp_lite` 是认真对待的强 baseline；
- 真实模型中的 routing specialization 不能只靠 load balancing 解释；
- controlled benchmark 已经说明不同 regime 对应不同最优 gating family；
- 二阶路由是否必要，必须回到“数据分离体制”和“优化状态”两条主线来回答。

当前结果还不足以支持：

- “二阶项一定必要”；
- “low-rankness 自动推出更低 forgetting”；
- “specialization 自动推出更低 gradient interference / forgetting”；
- 完整的 `specialization -> lower forgetting` 经验闭环。

---

## 3. Current Mainline (Pivoted to First-Order Orthogonal Decoupling)

### 3.1 Hypotheses

- **H1 (The Geometric Sufficiency of First-Order Routing) [Confirmed]:**  
  即使去除全局均值后，表征空间依然具有强各向异性，但 LLM 的 token 表征在中心化空间中仍然主要呈现均值可分（mean-separable）。因此，保留了一阶残差信息的中心化线性路由（如 `acp_lite`）已经能够提取足够的分发信号。

- **H2 (The Capacity vs. Optimization Gap in Second-Order):**  
  二阶或 hybrid 路由未达到预期，不一定是理论表达能力不足，而是可能陷入两个困境：  
  1. 在均值可分占主导的数据流上，二阶项退化成冗余的噪声拟合器；  
  2. 纯正值且呈二次缩放的 $\|V_e x_c\|_2^2$ 项在与一阶项共同优化时，遭遇 Softmax 数值缩放或梯度主导问题。

- **H3 (Defining Specialization via Total Covariance):**  
  专家的“专一性（specialization）”和“低秩性（low-rankness）”是同一几何现象的两个侧面。在全局协方差预算固定的情况下，更强的分发专一性必然导致更大的类间方差，从而被动挤压类内（专家内）协方差，迫使其呈现低秩特性。

- **H7 (Routing Channel Decoupling):**  
  在 hybrid router 中，不同的路由项自然解耦并负责不同类型的 token 分发。具体而言：均值投影项 $a_e^\top x_{\parallel}$ 主要响应功能词（function words）或高频无语义 token；中心化一阶项 $b_e^\top x_c$ 处理局部上下文游走；低秩子空间项 $\|V_e x_c\|_2^2$ 集中响应具有明确领域/语义特征的 domain keywords。

- **H8 (Function Word Sink):**  
  由于功能词缺乏特异性的语义方差，它们在良好的分发机制下，应当被稳定地“汇聚”到少数几个特定的专家中，而不是均匀散布或造成路由混乱。

- **H9 (The Orthogonal Decoupling Hypothesis):**  
  `acp_lite` 成为最强一阶 baseline 的核心几何机制在于正交解耦。公式
  $$
  \ell_e(x)=a_e^\top x_{\parallel}+b_e^\top x_c
  $$
  将最大方差方向（PC1，响应粗粒度 / 高频词）与残差空间（响应细粒度语义）进行了线性隔离。这种显式的一阶解耦比隐式的二阶拟合更高效，避免了极大方差方向对残差均值切分的掩盖。

- **H11 (Passive Dimensionality Reduction):**  
  专家的低秩性无需由二阶 router 主动寻找。基于全方差定律，通过一阶路由最大化类间方差（高 $\rho_{\mathrm{sep}}$），会挤压类内总方差 $\operatorname{Tr}(\Sigma_E)$。在天然各向异性的 LLM 表征中，这种“方差挤压”会迫使次要噪声维度坍缩，被动诱导出低有效秩 $\mathrm{sRank}(\Sigma_e)$，从而实现专家的几何专一化。

### 3.2 Core Modeling (The First-Order Endgame)

我们回到全方差定律：
$$
\operatorname{Cov}(x_c)
=
\underbrace{\mathbb{E}[\operatorname{Cov}(x_c\mid E)]}_{\text{Within-expert spread}}
+
\underbrace{\operatorname{Cov}(\mathbb{E}[x_c\mid E])}_{\text{Between-expert separation}}.
$$

路由的核心几何目标是最大化 separation ratio：
$$
\rho_{\mathrm{sep}}
=
\frac{\operatorname{Tr}(\operatorname{Cov}(\mathbb{E}[x_c\mid E]))}
{\operatorname{Tr}(\operatorname{Cov}(x_c))}.
$$

由于分子纯粹由条件均值决定，一阶线性变换是捕捉这种均值散度的直接数学形式。

为了定量评估专家低秩性，对分配给专家 $e$ 的局部特征定义：
$$
\Sigma_e = \operatorname{Cov}(x_c \mid E=e).
$$

进一步定义有效秩：
$$
\mathrm{sRank}(\Sigma_e)
=
\frac{\operatorname{Tr}(\Sigma_e)^2}{\operatorname{Tr}(\Sigma_e^2)}.
$$

解释：

- $\rho_{\mathrm{sep}}$ 刻画的是“数据是否被 router 按条件均值拉开”；
- $\mathrm{sRank}(\Sigma_e)$ 刻画的是“单个专家内部的占用子空间是否被压缩”。

当前 hybrid router 的工作形式仍记为：
$$
\ell_e(x)=a_e^\top x_{\parallel}+b_e^\top x_c+\|V_e x_c\|_2^2,
$$
但它当前的作用不再被默认解释为“理论上必然更好”，而是被视为一个待验证的机制候选。

### 3.3 Specialization, low-rankness, and interference

- `specialization` 是 assignment-side 现象；
- `low-rankness` 是 geometry-side 现象；
- 二者通过 total covariance decomposition 相连，但并不等价；
- overlap regularization 只能提供结构偏置，不能直接推出 zero interference 或 zero forgetting。

更谨慎的链路表达应当是：

1. stronger routing specialization  
2. larger between-expert separation  
3. smaller within-expert spread / lower effective rank  
4. potentially weaker overlap and interference  
5. possibly lower forgetting

其中第 4、5 步仍需专门实证支撑。

---

## 4. Missing Pieces for NeurIPS

### A. Empirical proof of decoupling

需要直接验证：

- $a_e^\top x_{\parallel}$ 是否主要响应 function words / high-frequency tokens；
- $b_e^\top x_c$ 是否主要承担局部上下文游走；
- $\|V_e x_c\|_2^2$ 是否在 domain keywords 上表现出更高活跃度。

### B. FLOPs / Overhead

需要正式回应：
$$
O(r \cdot d)
$$
级别的额外 router 开销，在
$$
r \ll d
$$
时是否可接受，并补充 wall-clock evidence。

### C. Task-agnostic continual learning

需要更清晰地实证：

- CORE 的 router 不依赖 task ID；
- 它在 protocol 上天然兼容 task-agnostic continual learning；
- 但这一点仍然需要专门设计的 experiment support。

### D. Specialization to forgetting

需要补足如下经验链：

- stronger specialization
- lower overlap
- weaker gradient interference
- lower forgetting

当前只完成了前半段，还没有完成最终闭环。

---

## 5. Analysis Experiments Plan & Status

### 5.1 [Completed] Round 1-5: The Regime Discovery

- **Status:** Executed (Medium Scale, Paper-Ready).
- **Key Findings:**
  1. `acp_lite` 产生了最强的 $\rho_{\mathrm{sep}}$（0.1015），说明真实数据流高度 mean-separable。
  2. K-Means 的 $\rho_{\mathrm{sep}}$ 在六个提取层中全面高于 K-Subspaces，支持“当前 regime 更偏向均值可分”。
  3. `hybrid` 路由的二阶分支虽然未在优化中被完全“饿死”（梯度比均值约 0.8685），但引入了高昂 FLOPs 开销（1.196M vs 15.4K），且未带来对应的几何分离收益。

### 5.2 [Next] Round 6: The Eigen-Spectrum Decay Audit (Inference Only)

- **目标:** 实证检验 H11（被动降维假说）。证明 `acp_lite` 在切分均值后，确实迫使专家内部数据呈现更低秩的局部几何。
- **实验:** 在已训练的 `acp_lite` 和 `linear_no_center` 中，收集分配给特定专家 $E$ 的 $x_c$。计算局部协方差矩阵 $\Sigma_E$，提取特征值
  $$
  \lambda_1 \ge \lambda_2 \ge \dots \ge \lambda_d.
  $$
- **预期产物:** 绘制特征值衰减曲线。预期 `acp_lite` 的特征值曲线更陡，前少数特征值占据主要能量；`linear_no_center` 的谱衰减相对更平缓。

### 5.3 [Next] Round 7: Orthogonal Subspace Ablation & CL Bridge (Training)

- **目标:** 剥离验证 $a_e^\top x_{\parallel}$ 与 $b_e^\top x_c$ 解耦带来的 $1+1>2$ 收益，并将这种几何解耦与 continual learning 边界上的 interference 联系起来。
- **实验:** 设立三组纯一阶对比：
  1. 仅靠均值方向路由；
  2. 仅靠残差方向路由；
  3. 正交解耦路由（`acp_lite`）。
- **观测:** 追踪其在多任务连续学习边界上的 cross-task gradient interference，以及对应的 forgetting proxy。

### 5.4 [Planned] Round 8: Token Decoupling & Expert Assignment Audit (Inference Only)

- **目标:** 直接验证 H7 与 H8。
- **模型:** `linear_running_center`, `acp_lite`, `hybrid_subspace_energy`
- **实验:**
  1. 按词性或词频划分 token groups：function words / domain keywords / mixed tokens。
  2. 统计不同 token group 的 expert assignment 分布。
  3. 针对 `hybrid_subspace_energy`，拆解并记录 $a_e^\top x_{\parallel}$、$b_e^\top x_c$、$\|V_e x_c\|_2^2$ 三项 logit 在不同 token group 上的绝对贡献和方差。
- **预期:** 均值通道在 function words 上更活跃，子空间通道在 domain keywords 上更活跃；function words 在 `acp_lite` 和 `hybrid` 中呈现更强的 expert 一致性。

### 5.5 [Planned] Round 9: Specialization Metric Tracking

- **目标:** 定量比较 $\rho_{\mathrm{sep}}$ 与 $\mathrm{sRank}(\Sigma_e)$ 是否在不同 router 中共同变化。
- **模型:** `linear_no_center`, `linear_running_center`, `acp_lite`, `hybrid_subspace_energy`
- **实验:**
  1. 计算各模型的 $\rho_{\mathrm{sep}}$；
  2. 计算各专家的 $\mathrm{sRank}(\Sigma_e)$；
  3. 检查最强模型是否同时具有更高 separation 和更低有效秩。
- **预期:** `linear_no_center` 会表现出虚假的 certainty；`acp_lite` 应在 $\rho_{\mathrm{sep}}$ 上最强；如果 `hybrid` 要证明必要性，则必须在 $\mathrm{sRank}(\Sigma_e)$ 或其它几何结构指标上给出 `acp_lite` 难以达到的额外收益。

---

## 6. Theory Sync Block

当前最适合发给 theory agent 的 focus：

1. 继续收紧“first-order orthogonal decoupling”是否已经足够作为主线；
2. 讨论 H11 的理论强度是否足够，或者需要更谨慎地写成经验倾向；
3. 讨论 Round 6 / Round 7 的预期证据是否真的能支撑论文主张；
4. 避免重新回到“旧 diagonal quadratic 必须成立”的叙事。

---

## 7. Experiment Handoff Block

当前 experiment side 的核心任务：

1. 先完成 inference-only 的几何 audit（Round 6 / Round 8 / Round 9）；
2. 再进入需要训练的 CL bridge（Round 7）；
3. 输出必须包含：
   - 实验目标
   - 实验步骤
   - 结果表 / 图
   - 结果分析
   - 对状态文档的回写建议

硬边界：

- 不要擅自改 router 公式；
- 不要把未确认的理论主张直接写成结论；
- 所有结果都必须能回写到本状态文档的假说或实验计划中。

---

## 8. Experiment Return

待实验端回写：

- Round executed:
- Result summary:
- Reliability audit:
- Hypothesis update:
- Suggested checkpoint delta:

---

## 9. Version Decision

- 当前版本仍然是 `v6.6`，因为主线没有彻底切换，只是在现有主线下完成“first-order orthogonal decoupling”方向的收束。
- 若 Round 6 / Round 7 明确支持 H11 与 H9，则下一版可升为新的论文主线版本。
