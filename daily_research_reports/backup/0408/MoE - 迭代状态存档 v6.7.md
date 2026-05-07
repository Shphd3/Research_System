# MoE - 迭代状态存档 v6.7

> 0408 用于继续推进 theory analysis、paper consolidation、以及新一轮 experiment handoff 的唯一状态文档。

---

## 0. Metadata

- Project: CORE: Centered Orthogonal Routing for Expert Specialization in Mixture-of-Experts
- Version: v6.7
- Date: 2026-04-08
- Stage: Theory refinement + experiment design
- Mode: `Exploration -> Convergence`

---

## 1. Current State

- 当前论文主线已经从 `continual learning first` 正式转向 `expert specialization first`。
- 当前最重要的理论问题不再是“如何继续为二阶路由辩护”，而是：
  1. 为什么当前表征空间里一阶分发优于二阶分发；
  2. 如何用一个精确指标严格刻画这种差异；
  3. 在哪些条件下，一阶与二阶在数学上等价。
- 当前最强经验结论：
  - `acp_lite` 是当前最强一阶 baseline；
  - 实际 token 表征在中心化后表现出强 mean-separable 几何；
  - 二阶 / hybrid 在当前 regime 下没有带来对应的分离收益，却带来了显著额外开销。

---

## 2. Executive Summary

当前要推进的不是新的 router 结构，而是新的解释框架。

新的核心主张是：

1. 未中心化的一阶路由之所以失败，是因为巨大的 global mean shift 淹没了真正的 token-specific variation。
2. 中心化之后，真实 token 表征依然主要是 mean-separable，因此一阶路由已经足够强。
3. 二阶路由与一阶路由在当前数据 regime 下之所以表现接近，不是因为二阶无用，而是因为在类内协方差趋同的条件下，二阶判别在数学上退化为一阶判别。
4. 下一步需要一个更精确的 instance-level audit，从真实句子级别去找出一阶和二阶的“共识区”和“分歧区”，从而刻画它们的适用边界。

---

## 3. Current Mainline

### 3.1 Hypotheses

- **H1 (Mean-Collapse under Global Shift):**  
  当表征存在巨大的全局均值 $\mu_{\mathrm{global}}$ 且满足
  $$
  \|\mu_{\mathrm{global}}\| \gg \|x_c\|,
  $$
  未中心化的一阶路由
  $$
  w_e^\top x = w_e^\top \mu_{\mathrm{global}} + w_e^\top x_c
  $$
  会被第一项主导，并退化为近似常量分配器。

- **H2 (First-Order Sufficiency after Centering):**  
  在当前 LLM 表征 regime 下，中心化后的 token 表征仍然主要是 mean-separable。因此，一阶路由，尤其是正交解耦的一阶路由 `acp_lite`，已经能够提取足够的 routing signal。

- **H3 (GDA-to-LDA Equivalence Condition):**  
  设去均值后的条件分布满足
  $$
  P(x_c \mid E=e) \sim \mathcal{N}(\mu_e, \Sigma_e).
  $$
  当
  $$
  \Sigma_e = \Sigma, \qquad \forall e,
  $$
  时，GDA 的二次判别项对所有专家相同并在 Softmax 中约掉，后验退化为 LDA 型一阶线性判别。因此，在类内协方差趋同的 regime 下，二阶路由与一阶路由在数学上等价。

- **H4 (Capacity vs. Optimization Gap in Second-Order):**  
  当前二阶 / hybrid 路由没有带来额外收益，可能有两种解释：
  1. 数据本身主要是 Type 1，即主要由均值差异驱动；
  2. 二阶项与一阶项在优化过程中发生竞争，导致其没有形成稳定、独立的几何增益。

- **H5 (Specialization via Total Covariance):**  
  `specialization` 与 `low-rankness` 是同一几何现象的两个侧面。通过
  $$
  \operatorname{Cov}(x_c)
  =
  \mathbb{E}[\operatorname{Cov}(x_c \mid E)]
  +
  \operatorname{Cov}(\mathbb{E}[x_c \mid E]),
  $$
  更强的类间 separation 会压缩类内 spread，并被动诱导更低的 expert effective rank。

---

### 3.2 Mathematical Modeling

#### A. Why global mean destroys uncentered linear routing

若在未中心化表示
$$
x = x_c + \mu_{\mathrm{global}}
$$
上直接做线性路由，
$$
\ell_e(x)=w_e^\top x,
$$
则有
$$
\ell_e(x)=w_e^\top \mu_{\mathrm{global}} + w_e^\top x_c.
$$
当 $\|\mu_{\mathrm{global}}\|$ 极大时，第一项主导 logit，路由器将优先拟合全局偏置，而不是 token-level semantic differences。

#### B. Why first-order and second-order can become equivalent

设条件分布为
$$
P(x_c \mid E=e) \sim \mathcal{N}(\mu_e, \Sigma_e).
$$
则后验对数为
$$
\log P(E=e \mid x_c)
\propto
-\frac{1}{2}(x_c-\mu_e)^\top \Sigma_e^{-1}(x_c-\mu_e)
-\frac{1}{2}\log|\Sigma_e|
+ \log P(E=e).
$$

展开得
$$
\log P(E=e \mid x_c)
\propto
-\frac{1}{2}x_c^\top \Sigma_e^{-1}x_c
+\mu_e^\top \Sigma_e^{-1}x_c
-\frac{1}{2}\mu_e^\top \Sigma_e^{-1}\mu_e
-\frac{1}{2}\log|\Sigma_e|.
$$

其中：

- 二阶项来自
  $$
  x_c^\top \Sigma_e^{-1}x_c;
  $$
- 一阶项来自
  $$
  \mu_e^\top \Sigma_e^{-1}x_c.
  $$

若所有专家满足
$$
\Sigma_e = \Sigma, \qquad \forall e,
$$
则二次项对所有专家相同并可约掉，后验退化为
$$
\log P(E=e \mid x_c)
\propto
(\Sigma^{-1}\mu_e)^\top x_c + C_e,
$$
这是标准的一阶线性判别形式。

#### C. Metrics to quantify the regime

为了定量度量“数据分得更开”和“专家内部是否坍缩”，保留两组 metric：

1. Separation Ratio
$$
\rho_{\mathrm{sep}}
=
\frac{\operatorname{Tr}(\operatorname{Cov}(\mathbb{E}[x_c \mid E]))}
{\operatorname{Tr}(\operatorname{Cov}(x_c))}.
$$

2. Expert Effective Rank
$$
\Sigma_e = \operatorname{Cov}(x_c \mid E=e),
$$
$$
\mathrm{sRank}(\Sigma_e)
=
\frac{\operatorname{Tr}(\Sigma_e)^2}{\operatorname{Tr}(\Sigma_e^2)}.
$$

3. Instance-level PPL divergence ratio
对于句子 $S_i$，定义
$$
R_i=\frac{PPL_{1,i}-PPL_{2,i}}{PPL_{1,i}},
$$
用于比较一阶模型与二阶模型在实例级别的相对差异。

---

## 4. Current Interpretation

- 当前最稳的解释是：
  1. 中心化暴露了一阶语义差异；
  2. 均值方向仍然携带粗粒度 routing signal；
  3. `acp_lite` 的优势来自把这两种一阶信号分开，而不是来自更高阶的 expressivity。
- 当前对二阶项的理解也更谨慎：
  - 不是“它完全无用”；
  - 而是“在当前 regime 下，它没有形成独立且必要的判别收益”。

---

## 5. Analysis Experiments Plan

### 5.1 Completed Evidence

已完成的 analysis 已经支持：

- 真实 token 表征在去均值后主要表现为 mean-separable；
- `acp_lite` 在 separation ratio 上达到当前最强；
- token-level audit 支持 mean channel 与 residual channel 的语义解耦；
- 二阶项在当前 regime 下没有形成值得其代价的几何收益。

### 5.2 Next Experiment: Instance-level PPL Divergence Audit

**Objective**  
通过句子级 PPL / Loss 差异，找到一阶与二阶模型的“共识区”和“分歧区”，并用路由熵解释这些分歧。

**Models**

- Model 1: `acp_lite`
- Model 2: `hybrid` 或 `quadratic_low_rank`

**Data**

- 10,000 个完整句子或固定长度序列
- 优先使用当前验证集；若适合，也可使用 WikiText-103 作为附加对照

**Procedure**

1. 对两个模型分别计算句子级 $PPL$ 或平均 loss；
2. 对每个句子提取路由信息熵；
3. 计算
   $$
   R_i=\frac{PPL_{1,i}-PPL_{2,i}}{PPL_{1,i}};
   $$
4. 按阈值将样本分为：
   - Group A: 共识区
   - Group B: 一阶优势区
   - Group C: 二阶优势区
5. 对每一组统计：
   - 规模占比
   - 平均 PPL 差异
   - 平均路由熵
   - 代表性句子实例

**Expected Outcome**

- Group A 应占绝大多数；
- 若 Group C 存在且稳定，则这些句子应表现出更复杂的结构，使一阶模型的路由熵更高；
- 若 Group C 很小或不稳定，则进一步支持“当前 regime 下一阶已足够”的主张。

---

## 6. Theory Sync Block

如果现在继续和 theory agent 讨论，应聚焦：

1. H3 的等价条件是否还能写得更严谨；
2. 如何更正式地区分“mean-separable regime”与“covariance-separable regime”；
3. `Instance-level PPL Divergence Audit` 的 decision rule 是否已经足够严谨；
4. 如何把这些内容转成论文 analysis 里的正式表述。

---

## 7. Experiment Handoff Block

当前最推荐交给 experiment agent 的任务只有一个：

### Round 6: Instance-level PPL Divergence Audit

需要 experiment agent 完成：

1. 数据准备：
   - 抽取 10,000 个完整句子或定长序列；
   - 保证两个模型使用完全一致的 token IDs。
2. 模型推理：
   - 在 `torch.no_grad()` 下加载同一步数 checkpoint；
   - 记录句子级 PPL / loss 与平均路由熵。
3. 分组分析：
   - Group A: $|R_i| \le 0.05$
   - Group B: $R_i < -0.05$
   - Group C: $R_i > 0.05$
4. 结果产物：
   - `ppl_divergence_audit.jsonl`
   - 统计 Markdown 表
   - Group B / C 的代表性句子样本
   - 一份 `Experiment Return` block

硬边界：

- 先锁协议，再执行；
- 不要改模型公式；
- 不要混入新的训练；
- 不要扩展成大 benchmark。

---

## 8. Experiment Return

待 experiment agent 回写：

- Round executed:
- Result summary:
- Reliability audit:
- Hypothesis update:
- Suggested checkpoint delta:

---

## 9. Version Decision

- 当前版本升为 `v6.7`，因为主线已经从“regime-dependent hybrid necessity”进一步收束成“当前 regime 下的一阶正交解耦为何更优”。
- 如果 Round 6 进一步支持 H2 / H3，则下一版可直接进入 paper-ready analysis checkpoint。
