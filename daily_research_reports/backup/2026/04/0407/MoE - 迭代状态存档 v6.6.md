# MoE - 迭代状态存档 v6.6

> 0406 之后用于 NeurIPS 论文收束的唯一状态文档。  
> 当前目标：把 CORE 的理论主线、analysis 缺口，以及下一轮 analysis experiments 写清楚。

---

## 0. Metadata

- Project: CORE: Covariance-Oriented Routing for Experts in Continual Learning
- Version: v6.6
- Date: 2026-04-06
- Current Stage: Paper consolidation
- Current Mode: `Convergence`

---

## 1. Executive Summary

- 当前主线不是继续为旧的 diagonal quadratic 辩护，而是把 CORE 写成一个 **regime-dependent hybrid routing** 框架。
- 当前最稳的结果有三条：
  1. `linear_running_center` 是干净 baseline，`acp_lite` 是当前最强的一阶 comparator。
  2. 在 controlled benchmark 中，mean-separable / covariance-separable / mixed 三种 regime 的最优 router 不同。
  3. 因此 covariance-aware routing 不是 universally necessary，而是 **regime-dependent necessary**。
- 当前还不能过度宣称的三条：
  1. overlap regularization 不会自动保证 zero interference 或 zero forgetting；
  2. 当前 token-level 证据还不足以严格证明完整 semantic routing；
  3. 现有结果还没有完成 `specialization -> forgetting` 的闭环。
- Current single decision question:
  **是否可以把论文正式写成：CORE = mean projection + centered linear + low-rank subspace energy + overlap regularization，并以 regime-dependent necessity 作为核心理论主张？**

---

## 2. Results Analysis

### 2.1 Real-model checkpoint audit

来源：
- `0406/round12l_ckpt40000_full_experiment_synthesis.md`
- `0406/round12340_metrics_and_implementation_ckpt40000.md`

当前可以稳定写入论文的结论：

- `acp_lite` 的 `Round0 Avg` 最好，是必须认真对待的强 baseline。
- `quadratic_low_rank` 的 `Mean SI` 最低，是当前最强的 overlap-oriented variant。
- `quadratic_low_rank_acp_lite` 在高噪声 `CR@0.5` 上最好，同时 `Round0` 也强，说明它是当前最均衡的 hybrid candidate。
- `linear_no_center` 是关键反例：其高 `CR` 和高 margin 来自 collapse，而不是 meaningful specialization。
- `linear_nocenter_lb001` 是已完成的 load-balancing control：它比原始 `no_center` 更好，但仍未超过最强的 geometry-aware variants。

这些结果说明：

- 一阶路线不能被轻易打倒；
- low-rank quadratic family 确实带来了 robustness / overlap 优势；
- no-centering control 和 load-balancing control 都已经进入 eval，因此当前 gains 不能被简单解释成“只是 balancing regularization”；
- 但没有单一模型在所有维度上全面胜出。

### 2.2 Controlled benchmark

来源：
- `0406/summary_continuous_hmm_v5_30law_r20260407_v5full.md`

最关键结论：

- Type1（mean-separable）：`linear_running_center` 最好。
- Type2（covariance-separable）：`subspace_energy` 最好。
- Type3（mixed）：`hybrid_subspace_energy` 最好。

更强的机制证据来自 hybrid contribution decomposition：

$$
\text{Type1: mean} > \text{centered} > \text{subspace}
$$

$$
\text{Type2: subspace} > \text{centered} > \text{mean}
$$

$$
\text{Type3: subspace} \approx \text{centered} \approx \text{mean}
$$

这组结果第一次把“什么时候需要 ACP-like term，什么时候需要 subspace / quadratic term”按 regime 写清楚了。

### 2.3 What current results support

当前结果足以支撑：

- real-model checkpoint audit；
- controlled synthetic benchmark；
- `SI / H(E|C)` 的谨慎解释；
- hybrid 三项 logit 贡献分解。

当前结果还不足以支撑：

- $x_{\parallel}$ 与 $x_c$ 的严格 empirical decoupling；
- FLOPs / overhead 的正式回应；
- task-agnostic CL 的专门证据；
- `specialization -> forgetting` 的最终闭环。

结论：

**当前证据足以支撑 analysis + controlled evidence 版本的论文，但还不足以单独支撑最终的 CL forgetting claim。**

---

## 3. Current Mainline

### 3.1 Hypotheses

- H1 \& H7 (First-Order Sufficiency \& PC1 Decoupling):  
  LLM 表征高度各向异性，全局均值方向与第一主成分（PC1）高度对齐。`acp_lite` 的均值投影项
  $a_e^\top x_{\parallel}$
  本质上是在最大方差方向上提取粗粒度、均值可分的 routing signal；当这部分主导方差被显式解耦后，中心化残差
  $x_c$
  中的细粒度上下文变化即可由
  $b_e^\top x_c$
  充分处理。因此，在真实数据流主要是 mean-separable 时，一阶 route 已经可能足够。

- H2 (The Capacity vs. Optimization Gap in Second-Order):  
  二阶或 hybrid 路由未达到预期，不一定是理论表达能力不足，而是可能陷入两个困境：
  1. 在均值可分占主导的数据流上，二阶项退化为冗余的噪声拟合器；
  2. 纯正值且呈二次缩放的
  $\|V_e x_c\|_2^2$
  在与一阶项共同优化时，遭遇 Softmax 数值缩放或梯度主导问题。

- H3 (Defining Specialization via Total Covariance \& Low-Rankness):  
  真正的“专一化”不应被定义为 K-Means 式的球形聚类，而应表现为**子空间坍缩（subspace collapse）**。在全方差分解下，更强的分发专一性不仅增大类间方差，更迫使专家内的局部协方差矩阵
  $\Sigma_e$
  呈现低秩特性。因此，理想分发机制在几何上更接近子空间聚类（subspace clustering），而不只是球形聚类。

- H4:  
  overlap regularization 不保证 zero interference，但会为更强的 expert specialization 和更低的 subspace overlap 提供结构偏置。

- H5:  
  `specialization` 是 assignment-side 现象，`low-rankness` 是 geometry-side 现象；二者相关，但不等价。

- H6:  
  在 fixed global covariance budget 下，更强 specialization 倾向于提高 between-expert separation，并压缩 within-expert occupancy，因此更容易诱导低秩 expert geometry；但这仍需更严格理论与实验支持。

- H8 (Function Word Sink):  
  由于功能词缺乏特异性的语义方差，它们在良好的分发机制下，应当被稳定地汇聚到少数几个特定专家（function-word experts）中，而不是均匀散布或造成路由混乱。

### 3.2 Core modeling

设

$$
u=\frac{\mu_{\mathrm{global}}}{\|\mu_{\mathrm{global}}\|_2},\qquad
x_{\parallel}=(u^\top x)u,\qquad
x_c=x-\mu_{\mathrm{global}}.
$$

当前 hybrid router 的工作形式为：

$$
\ell_e(x)=a_e^\top x_{\parallel}+b_e^\top x_c+\|V_e x_c\|_2^2.
$$

为了度量“数据分得更开”和“专家专一性”，引入全方差分解作为数学基础：

$$
\operatorname{Cov}(x_c)
=
\underbrace{\mathbb{E}[\operatorname{Cov}(x_c\mid E)]}_{\text{Within-expert spread}}
+
\underbrace{\operatorname{Cov}(\mathbb{E}[x_c\mid E])}_{\text{Between-expert separation}}.
$$

这一定义导出两个关键 metric。

**Metric 1: Separation Ratio**

$$
\rho_{\mathrm{sep}}
=
\frac{\operatorname{Tr}\!\left(\operatorname{Cov}(\mathbb{E}[x_c\mid E])\right)}
{\operatorname{Tr}\!\left(\operatorname{Cov}(x_c)\right)}.
$$

当 $\rho_{\mathrm{sep}}$ 趋近于 1 时，表示 router 的 gating 行为更成功地把数据按均值在空间中分离开。

**Metric 2: Expert Effective Rank**

对分配给专家 $e$ 的局部特征，定义局部协方差矩阵

$$
\Sigma_e = \operatorname{Cov}(x_c \mid E=e).
$$

再定义有效秩：

$$
\mathrm{sRank}(\Sigma_e)
=
\frac{\operatorname{Tr}(\Sigma_e)^2}{\operatorname{Tr}(\Sigma_e^2)}.
$$

当 $\mathrm{sRank}(\Sigma_e)$ 越低，说明该专家内部特征越接近坍缩到低维子空间。

当前建模判断：

1. `acp_lite` 成功的原因，不一定是引入了更高阶结构，而可能是中心化后的一阶差异仍然足够强。
2. 二阶或 hybrid 路由失败时，必须区分“数据本身是纯 Type 1”与“二阶项在优化上被饿死”这两种解释。
3. `specialization` 不应只被口头定义，而应同时通过 $\rho_{\mathrm{sep}}$ 和 $\mathrm{sRank}(\Sigma_e)$ 去刻画 separation-side 与 geometry-side 两个侧面。

当前 regularization 仍写为：

$$
\mathcal{L}_{\mathrm{internal}}=\sum_e \|V_eV_e^\top-I_r\|_F^2
$$

$$
\mathcal{L}_{\mathrm{cross}}=\sum_{i\neq j}\|V_iV_j^\top\|_F^2.
$$

### 3.3 Specialization, low-rankness, and interference

- `specialization`：expert assignment 对 domain / token structure 的选择性。
- `low-rankness`：单个 expert 接收的特征协方差主要集中在较低维子空间上。
- 二者的桥来自 total covariance decomposition：

$$
\operatorname{Cov}(x_c)
=
\mathbb{E}[\operatorname{Cov}(x_c\mid E)]
+
\operatorname{Cov}(\mathbb{E}[x_c\mid E]).
$$

解释：

- 第二项越大，说明 experts 之间分得越开；
- 在总体协方差预算固定时，第一项更容易被压缩；
- 这就是“更专一的分发更容易诱导低秩 expert geometry”的结构原因。

但要谨慎：

- 这不是“specialization 自动推出 low-rankness”的定理；
- 更不是“low-rankness 自动推出 low forgetting”的定理。

Regularization 与梯度串扰的更谨慎表述：

- $\mathcal{L}_{\mathrm{cross}}$ 减少不同 expert 子空间重叠；
- 在 selective routing 条件下，这会降低 wrong-expert activation；
- 因而有助于减轻 cross-task gradient interference；
- 但这是一条 **bias / upper-bound** 式论证，不应写成无条件的零干扰结论。

---

## 4. Missing Pieces for NeurIPS

### A. Empirical proof of decoupling

需要直接验证：

- $a_e^\top x_{\parallel}$ 是否主要响应 coarse / high-frequency / function-like signals；
- $\|V_e x_c\|_2^2$ 是否更多响应 domain-specific / semantic signals。

### B. FLOPs / Overhead

需要明确回应：

$$
O(r d)
$$

级别的额外开销在

$$
r \ll d
$$

时是可接受的，并补上 wall-clock evidence。

### C. Task-agnostic continual learning

需要更清楚地写出并验证：

- CORE 的 router 不依赖 task ID；
- 因此方法天然兼容 task-agnostic CL protocol；
- 但该点还需要专门实证。

### D. Specialization to forgetting

需要补足：

- overlap reduction
- stronger specialization
- weaker interference
- lower forgetting

这四者之间的 empirical chain。

---

## 5. Analysis Experiments Plan

### Round 1: Token Decoupling \& Expert Assignment Audit (Inference Only)

模型：
- `linear_running_center`
- `acp_lite`
- `hybrid_subspace_energy`

实验：
1. 按照词性或词频划分 token groups：
   - function words（如 `the`, `is`, `at`）
   - domain keywords（领域特定名词/动词）
   - mixed tokens
2. 统计这三类 token 在上述模型中的 expert assignment 分布，重点观察功能词是否进入少数固定专家。
3. 针对 `hybrid_subspace_energy`，拆解并记录三项 logit：$a_e^\top x_{\parallel}$、$b_e^\top x_c$、$\|V_e x_c\|_2^2$ 在不同 token group 上的绝对贡献值与方差。

预期：

- 均值通道在 function words 上最活跃；
- 子空间通道在 domain keywords 上最活跃；
- function words 在 `acp_lite` 和 `hybrid` 中呈现更高的 expert 一致性；
- 若成立，则 H1/H7/H8 获得直接 inference-side 支持。

### Round 2: Specialization Metric Tracking (Pending)

待 Round 1 结论明确后，再切入对 separation 与低秩性的定量测量。

模型：
- `linear_no_center`
- `linear_running_center`
- `acp_lite`
- `hybrid_subspace_energy`

实验：
1. 计算 $\rho_{\mathrm{sep}}$，比较不同 router 是否真的把数据在均值意义上分得更开。
2. 计算每个专家的 $\mathrm{sRank}(\Sigma_e)$，检查性能更好的模型是否对应更低的局部有效秩。
3. 检查最强模型是否同时对应更高的 $\rho_{\mathrm{sep}}$ 和更低的 $\mathrm{sRank}(\Sigma_e)$，以及这两者是否真的共变。

预期：

- `linear_no_center` 会表现出虚假的 routing certainty，但不会给出理想的 specialization geometry；
- `acp_lite` 若确实是当前强 baseline，则应在 $\rho_{\mathrm{sep}}$ 上表现较强；
- `hybrid` 若要证明自身必要性，则必须在 $\mathrm{sRank}(\Sigma_e)$ 或 $\rho_{\mathrm{sep}}$ 上给出 `acp_lite` 难以达到的额外结构收益。

### Round 3: Empirical Separation \& Subspace Audit (Frozen Model)

目标：探明真实 token 在去均值表征空间中，究竟更符合基于距离的球形聚类（mean-separable），还是符合基于投影的低秩聚类（covariance-separable）。

实验：
1. 在预训练模型的特定层抽取 10 万个 token 激活值 $x_c$。
2. 分别使用 K-Means（基于欧氏距离）和 K-Subspaces / K-PCA（基于低秩子空间投影误差）将 token 分为 $K$ 个簇。
3. 对比两种聚类结果的 $\rho_{\mathrm{sep}}$ 以及各簇的平均有效秩 $\mathrm{sRank}(\Sigma_e)$。

预期：

- 如果 K-Subspaces 能产生比 K-Means 更低的 $\mathrm{sRank}(\Sigma_e)$ 且聚类纯度更好，则直接支持“理想专一化在几何上更接近子空间聚类”；
- 如果 K-Means 已经足够好，则说明真实数据流更偏 Type 1，进一步支持 H1。

### Round 4: Routing Logit Dynamics (Training Model)

目标：检查 hybrid 路由内部的一阶项与二阶项是否在优化中发生冲突。

实验：
1. 训练包含 hybrid router 的 MoE：

$$
\ell_e(x)=a_e^\top x_{\parallel}+b_e^\top x_c+\|V_e x_c\|_2^2
$$

2. 在训练过程中独立记录三项在 pre-softmax 阶段的：
   - 均值
   - 方差
   - 反向传播梯度的 $L_2$ 范数
3. 重点比较一阶项与二阶项的量级关系。

预期：

- 如果一阶项梯度比二阶项大几个数量级，则说明二阶项在优化上被“饿死”；
- 如果二者量级相当但二阶项仍然无贡献，则更支持“数据本身是纯 Type 1”而非“二阶项不会学”。

### Round 5: Overhead Audit

实验：

- 统计参数量、router FLOPs、wall-clock overhead。

预期：

- 低秩子空间项带来的额外复杂度应保持在可接受范围内；
- 可以正式回应 reviewer 对 FLOPs / overhead 的质疑。

---

## 6. Paper Writing Guidance

### 6.1 Contribution wording

建议写成：
1. regime-dependent routing theory
2. CORE hybrid router
3. a conditional interference view of expert specialization
4. controlled + real-model empirical evidence

### 6.2 Abstract boundary

摘要可以写：

- ACP-like routing 在 mean-dominant regime 有必要；
- covariance-aware routing 在 covariance-separable regime 有必要；
- hybrid route 在 mixed regime 最合理。

摘要不要写：

- zero interference 已经被证明；
- forgetting 已经被全面解决。

---

## 7. Theory Sync Block

- Mainline:
  CORE 要写成一个 regime-dependent hybrid routing 框架。
- What to discuss now:
  1. ACP 项的必要性如何写得更严谨；
  2. quadratic / subspace term 的必要性如何写成正式 proposition；
  3. `specialization -> low-rankness -> weaker interference` 这条桥怎样写得更谨慎但更清楚；
  4. 缺失环节 A/B/C/D 怎样压成 paper-ready analyses；
  5. H1/H7/H8 能否通过 token-level decoupling audit 与 subspace audit 获得直接支持。

---

## 8. Experiment Handoff Block

- Current objective:
  先补 analysis experiments，再补 final CL bridge。

- Priority:
  1. Round 1: Token Decoupling \& Expert Assignment Audit
  2. Round 2: Specialization Metric Tracking
  3. Round 3: Empirical Separation \& Subspace Audit
  4. Round 4: Routing Logit Dynamics
  5. Round 5: Overhead Audit

- Return format:
  experiment agent 必须回写：
  - 实验目标
  - 实验步骤
  - 实验结果
  - 实验分析
  - 更新了什么假设

---

## 9. Experiment Return (Executed)

执行目录：
- `exp_quadratic_proportion/output/analysis_v6.6`
- 综合报告：`exp_quadratic_proportion/output/analysis_v6.6/final_integrated_report.md`
- 回填块：`exp_quadratic_proportion/output/analysis_v6.6/experiment_return_block.md`

### 9.1 Round 1: Token Decoupling & Expert Assignment

- 实验目标  
  验证 function/domain token 分发与 hybrid 三项 logit 响应差异。
- 实验步骤  
  固定 WoS 样本清单，执行词表单-token清洗，在 `linear_running_center` / `acp_lite` / `hybrid` 上统计 token 分发与 hybrid 分项 logit。
- 实验结果  
  - function 词：44 -> 43 可用单 token。  
  - domain 词：205 -> 119 可用单 token。  
  - function 组 top-share 均值：linear 0.5796 / acp 0.5778 / hybrid 0.5870。
- 实验分析  
  已落实 subword Hotfix，避免了碎片词误匹配；hybrid 在 function 组集中度略高。
- 更新了什么假设  
  H1/H7 获得弱到中等支持；H8 需要词频分层补证。

### 9.2 Round 2: Specialization Metric Tracking

- 实验目标  
  量化 `rho_sep` 与 `sRank` 的模型差异。
- 实验步骤  
  对四模型按全 MoE 层提取 `x_c` 与 expert assignment，并逐层计算 `rho_sep` 与 `sRank(Sigma_e)`。
- 实验结果  
  - `rho_sep_mean`: acp_lite 0.0991 > hybrid 0.0656 > linear_running_center 0.0611 >> linear_no_center 0.0058。  
  - `sRank_mean`: acp_lite 57.13 > linear_running_center 49.34 > hybrid 39.09 > linear_no_center 28.65。
- 实验分析  
  `acp_lite` separation 最强；`linear_no_center` 分离能力最弱。
- 更新了什么假设  
  H3/H5 仅部分支持，二者关系仍需更强证据。

### 9.3 Round 3: Empirical Separation & Subspace Audit

- 实验目标  
  在层级隔离前提下比较 KMeans 与 K-Subspaces 几何解释力。
- 实验步骤  
  按 `1/3/5/7/9/11` 六层独立抽取 `x_c`，逐层独立执行 KMeans 与 K-Subspaces。
- 实验结果  
  三模型均呈 `rho_sep(KMeans) > rho_sep(K-Subspaces)`；avg_sRank 上 K-Subspaces 未稳定领先。
- 实验分析  
  当前样本规模下更偏 mean-separable 解释；需扩大 token 规模复核。
- 更新了什么假设  
  H1 进一步增强；H3 尚未形成强支撑。

### 9.4 Round 4: Routing Logit Dynamics

- 实验目标  
  从 step0 观察三项 logit 与梯度竞争。
- 实验步骤  
  使用随机初始化 hybrid 路由轻量训练，逐步记录 mean/centered/subspace 的 pre-softmax 统计与梯度 L2。
- 实验结果  
  - subspace/first-order 梯度比值区间 `[0.3096, 0.4538]`。  
  - 最后一步梯度：centered 0.00794 > subspace 0.00362 > mean 0.00126。
- 实验分析  
  二阶分支早期并未完全饿死，centered 一阶分支更强。
- 更新了什么假设  
  H2 倾向“存在竞争但不是单边压制”。

### 9.5 Round 5: Overhead Audit

- 实验目标  
  给出参数/FLOPs/延迟三位一体开销证据。
- 实验步骤  
  六模型统一 step60000，固定 tokens/批进行延迟评测。
- 实验结果  
  - hybrid：router params 7.23M，router FLOPs/token 1.196M，latency 122.07ms。  
  - quadratic_low_rank：7.08M，1.180M，76.26ms。  
  - 线性族：73.7K，6.1K，39.63-116.32ms。
- 实验分析  
  二阶/混合路线存在显著额外开销，需由 regime-specific 收益抵偿。
- 更新了什么假设  
  regime-dependent necessity 的工程代价维度已补齐。

### 9.6 Current Decision Update

- 已完成 Round1-5 首轮可运行闭环与结果回写。  
- 下一步建议：  
  1. 按论文口径放大 Round3 token 规模与 Round4 步数；  
  2. 在 Round1 增加 function-word sink 的词频分层图；  
  3. 对 Round2/3 添加 bootstrap CI，提升统计稳健性。

---

## 10. Paper-Ready Re-run (2026-04-07, analysis_v6.6_paper_ready_20260407)

执行目录：
- `exp_quadratic_proportion/output/analysis_v6.6_paper_ready_20260407`
- 综合报告：`exp_quadratic_proportion/output/analysis_v6.6_paper_ready_20260407/final_integrated_report.md`
- 回填块：`exp_quadratic_proportion/output/analysis_v6.6_paper_ready_20260407/experiment_return_block.md`
- 进度看板：`exp_quadratic_proportion/output/analysis_v6.6_paper_ready_20260407/progress_dashboard.md`

### 10.1 Round1 (paper-ready medium scale)

- 实验目标  
  在中等规模样本下复核 function/domain token 分发与 hybrid 分项响应。
- 实验步骤  
  固定 WoS 清单（1200 样本）→ 单-token 清洗 → 三模型统计分发与 hybrid 分项 logit。
- 实验结果  
  - function: `44 -> 43`；domain: `127 -> 109`。  
  - function top-share 均值：`linear 0.5778 / acp 0.6036 / hybrid 0.6094`。
- 实验分析  
  `acp_lite/hybrid` 在 function 集中度上更强；H8 获得中等支持但仍需词频分层补证。
- 更新了什么假设  
  H1/H7 增强，H8 部分增强。

### 10.2 Round2 (paper-ready medium scale)

- 实验目标  
  复核 `rho_sep/sRank` 的模型排序稳定性。
- 实验步骤  
  四模型逐层提取 `x_c + assignment`，计算并聚合 `rho_sep/sRank`。
- 实验结果  
  - `rho_sep_mean`: `acp_lite 0.1015 > hybrid 0.0645 > linear_running_center 0.0615 >> linear_no_center 0.0060`。  
  - `sRank_mean`: `acp_lite 66.09 > linear_running_center 55.33 > hybrid 43.77 > linear_no_center 30.31`。
- 实验分析  
  `acp_lite` 继续是最强一阶 comparator；`linear_no_center` 继续作为反例。
- 更新了什么假设  
  H1 继续增强；H3/H5 仍为部分支持。

### 10.3 Round3 (paper-ready medium scale)

- 实验目标  
  复核 KMeans vs K-Subspaces 在六层的几何解释力。
- 实验步骤  
  每模型每层抽取 `12000` token 的 `x_c`，分别执行 KMeans 与 K-Subspaces 比较 `rho_sep/avg_sRank`。
- 实验结果  
  三模型在六层均满足 `rho_sep(KMeans) > rho_sep(K-Subspaces)`，且 K-Subspaces 未稳定给出更低 `avg_sRank`。
- 实验分析  
  当前证据更偏 mean-separable 解释，H1 增强；H3 仍未形成强支撑。
- 更新了什么假设  
  H1 增强，H3 暂不增强。

### 10.4 Round4 (paper-ready medium scale)

- 实验目标  
  复核 hybrid 一阶/二阶分支是否发生单边梯度压制。
- 实验步骤  
  随机初始化 step0 起跑，训练 `100` steps，逐步记录三项 logit 与梯度 L2。
- 实验结果  
  - ratio 区间：`[0.2756, 2.0896]`，均值 `0.8685`。  
  - 末步梯度：`subspace 0.00201 > centered 0.00113 > mean 0.00033`。
- 实验分析  
  二阶分支未见“全程饿死”，更接近竞争共存动态。
- 更新了什么假设  
  H2 更新为“存在竞争但非单边压制”。

### 10.5 Round5 (paper-ready medium scale)

- 实验目标  
  形成统一口径下的参数/FLOPs/latency 工程代价证据。
- 实验步骤  
  六模型固定输入设置，warmup 后执行 12 次测时并汇总。
- 实验结果  
  - hybrid：`7.23M router params, 1.196M FLOPs/token, 36.61ms`。  
  - quadratic_low_rank：`7.08M, 1.180M, 35.60ms`。  
  - 线性族：`73.7K, 6.1K, 26.28-33.27ms`。
- 实验分析  
  二阶/混合路线开销显著高于线性路线，必须由 regime-specific 收益抵偿。
- 更新了什么假设  
  regime-dependent necessity 的工程代价维度得到强化支撑。

### 10.6 Current Decision Update (Paper-Ready)

- `analysis_v6.6_paper_ready_20260407` 的 Round1-5 已执行完成。  
- 当前可写入论文主线的更稳结论：  
  1. `acp_lite` 依然是必须正面应对的强一阶基线；  
  2. covariance-aware 路线的必要性应坚持 regime-dependent 叙事；  
  3. 对 `specialization -> low-rankness -> forgetting` 保持谨慎，不做无条件强宣称。  
- 当前最大顾虑：  
  1. 统计稳健性（多 seed / CI）仍未补齐；  
  2. Round3 对 H3 支撑仍不足；  
  3. Round4 仍是短程训练口径，外推需谨慎。
