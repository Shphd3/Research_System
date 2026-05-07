# [调研]MoE - 迭代状态存档 v6.0

> 本版本不是开启全新故事线，而是把当前最有价值的旁路定义修复正式抬升进主线建模。  
> 我们现在要回答三件事：  
> 1. `quadratic` 到底是不是在“按方差分发”，还是只是具有二阶结构的架构？  
> 2. `expert specialization`、`expert low-rankness`、`variance routing` 三者到底分别是什么、彼此如何连接？  
> 3. 在 Continual Learning 主线下，下一步最小实验究竟该先做机制审计，还是直接做 forgetting test？

## 0. Checkpoint Metadata
- **项目**：MoE Router for Continual Learning
- **版本**：`v6.0`
- **日期**：2026-03-31
- **当前阶段**：`主线建模升级 / 定义修复进入主线 / 准备下一轮 CL closing follow-up`
- **本次更新触发器**：`12L / ckpt40000 五轮静态结果 + 理论旁路 card1 + 最小 CL 实验骨架`
- **一句话 North Star**：判断什么样的 routing mechanism 真正能降低 catastrophic forgetting，而不是继续用模糊概念讨论 router“是否更强”。
- **本 checkpoint 的作用域**：冻结当前主线定义、修正概念层级、明确下一步实验必须先回答什么，避免实验 Agent 每轮重新理解项目。

## 1. Executive Summary
- **当前最强主张**：`acp_lite` 已经成为当前最强的公平静态 comparator，说明显式 mean-direction buffering 本身就是一条非常强的一阶路线。
- **当前最大不确定性**：`quadratic_nosvd_debias` 在静态 proxy 上给出最低 `SI`，但我们仍不知道：
  - 它是否真的在按方差分发；
  - 以及这种低 `SI` 是否会转化成更低 forgetting。
- **本版本相较之前的核心升级**：
  - 把 `variance routing` 从口语直觉提升为可操作定义；
  - 把 `expert specialization` 明确重写成 assignment phenomenon；
  - 把 `expert low-rankness` 明确重写成 geometric state，而不是架构属性；
  - 把主线 causal chain 固定为：
    `Architecture -> Mechanism -> Assignment -> Geometry -> CL Outcome`。

## 2. Stable Knowledge / Report-Ready Claims

| ID | Claim | Evidence Type | Confidence | Can Write to Report? | Notes |
| --- | --- | --- | --- | --- | --- |
| C1 | `center` 是必要条件；`linear_no_center` 的高 margin / 高 CR 不代表健康 routing，而更像 collapse | main exp | high | yes | 五轮静态结果一致支持 |
| C2 | Router 质量是多目标问题，`downstream avg`、`SI`、`CR`、`load balance` 不能互相替代 | main exp | high | yes | 已有反例 |
| C3 | `linear_running_center` 是严格 baseline，`acp_lite` 是当前最强公平静态 comparator | main exp | high | yes | 当前 `ckpt40000` 结果支持 |
| C4 | `acp_lite` 擅长静态任务表现与表征复用，但并不在 `SI` 上最优 | main exp | high | yes | `Round0` 最优，`Round3` 非最优 |
| C5 | `quadratic_nosvd_debias` 在当前静态分析中给出最低 `SI`，说明它可能更强地压低跨域重叠 | main exp | medium | partial | 尚未转化为真实 forgetting 证据 |
| C6 | `high margin != specialization`，`low rank != good task performance` | theory + exp | high | yes | 现在应视为稳定认知 |
| C7 | `variance routing` 不能由“架构中存在二阶项”直接推出 | theory | high | yes | 这是当前主线升级点 |
| C8 | 静态 proxy 不能单独充当抗遗忘证明 | theory + exp | high | yes | 当前必须切回 CL 的原因 |

## 3. Hypothesis

| ID | Hypothesis Statement | Status | Why It Matters | Current Evidence | Blocking Risk |
| --- | --- | --- | --- | --- | --- |
| H1 | 对 CL 有用的 `expert specialization` 必须由 assignment / balance 联合定义，而不是由 margin 或 rank 代替 | supported | 修正“专一性”的定义 | `linear_no_center` 反例足够强 | 仍需更系统 assignment 指标 |
| H2 | 更低 overlap / 更低 SI 可能降低 forgetting，但与静态任务表现存在 trade-off | active / partially supported | 建立 routing geometry 到 CL 的桥梁 | `quadratic_debias` 最低 SI，`acp_lite` 最佳任务表现 | 仍缺真实 CL 闭环 |
| H3 | `quadratic architecture` 允许 variance routing，但不等于已经学会 variance routing | active / core | 修正我们对 quadratic 的语言和逻辑 | 来自旁路定义修复 | 需实测 `rho` attribution |
| H4 | `quadratic_nosvd_debias` 只有在它确实执行 variance routing，且这种机制最终降低 forgetting 时，才具备 CL 结构必要性 | active / narrowed | 这是 quadratic 主线的最终判据 | 当前只见低 `SI`，未见 mechanism audit 和 forgetting 证据 | 可能只是 robustness 路线 |
| H5 | `expert low-rankness` 应定义为 expert 内部 covariance 的低维占用状态，主指标应由 `r_{0.9}` 而不是 `ED_comp` 表征 | active | 修复 low-rankness 概念 | 来自理论 card1 | 仍需全量重算 |
| H6 | 静态 proxy 可以筛选候选 router，但不能完成 CL 判决 | supported | 防止主线继续偏题 | 当前所有证据都停在 proxy | 若继续只做静态分析会误导 |

## 4. Mathematical Modeling

### 4.1 Definition Repair: Three Core Concepts

#### 4.1.1 Variance Routing
- **It is NOT**：架构里出现了 `x_c \odot x_c` 就自动叫 variance routing。
- **Working Definition**：
  给定 quadratic router
  $$
  \ell_{\mathrm{quad}}(x)=W_1 x_c + W_2 q_{\mathrm{deb}}(x),
  \qquad
  q_{\mathrm{deb}}(x)=x_c\odot x_c-\lambda_t,
  $$
  对某个 domain pair `(C_1, C_2)`，若用于区分它们的 logit margin 主要由二阶项贡献，则称该 router 在该 pair 上执行了 variance routing。

- **Operational quantity**：
  对任一样本 `x` 定义
  $$
  m_1(x)=\text{margin}(W_1 x_c),\qquad
  m_2(x)=\text{margin}(W_2 q_{\mathrm{deb}}(x)),
  $$
  再定义 attribution ratio
  $$
  \rho = \frac{\mathbb{E}[|m_2(x)|]}{\mathbb{E}[|m_1(x)|]}.
  $$
  若 `\rho > 1` 且稳定存在于 hard domain pair 上，才可以说“二阶项主导了分域 margin”。

#### 4.1.2 Expert Specialization
- **It is NOT**：大 margin、低 rank、低 SI。
- **Working Definition**：
  `expert specialization` 首先是 assignment phenomenon。  
  它表示 routing assignment `E` 与真实语义 domain / cluster `C` 之间具有高 mutual information，同时保持健康的 load balance。

- **Recommended metric**：
  - primary: `NMI(E, C)` 或 `I(E;C)`
  - constraint: `H(E)` / `CV_load`

#### 4.1.3 Expert Low-Rankness
- **It is NOT**：架构自带属性，也不是性能保证。
- **Working Definition**：
  某 expert 内 routed feature covariance
  $$
  C_e = \mathrm{Cov}(x \mid E=e)
  $$
  只占据低维有效子空间，则称该 expert 处于 low-rank geometric state。

- **Recommended metric**：
  - primary: `r_{0.9}(C_e)`
  - supporting: `d_\tau(C_e)`
  - deprecate as primary: `ED_comp`

### 4.2 Main Causal Chain
当前主线建模正式固定为：

$$
\text{Architecture}
\rightarrow
\text{Mechanism}
\rightarrow
\text{Assignment}
\rightarrow
\text{Geometry}
\rightarrow
\text{CL Outcome}.
$$

对应到当前问题：
- `quadratic_nosvd_debias`：Architecture
- `variance routing`：Mechanism
- `specialization (NMI / purity)`：Assignment
- `low-rankness / low overlap / low SI`：Geometry
- `lower forgetting / lower interference`：CL Outcome

这条链条的意义是：  
以后不能再把 architecture、mechanism、geometry、outcome 混用。

### 4.3 Micro-Bridge to Continual Learning
我们当前保留的几何到 CL 的最小桥梁是：

$$
\text{Low-rankness} \Rightarrow \text{smaller occupied subspace}
\Rightarrow \text{higher chance of orthogonal updates}
\Rightarrow \text{lower interference}.
$$

一个可计算 proxy 是：
$$
SI_e = \frac{\mathrm{Tr}(C_{e,A}C_{e,B})}{\|C_{e,A}\|_F\|C_{e,B}\|_F}.
$$

但本版本明确规定：
- `SI` 只是 geometry / interference proxy
- 不能直接等同于 forgetting

### 4.4 What the Current Static Results Mean
- `acp_lite` 更像 mean-shift buffer：它把 mean-direction 单独暴露给 router，因此在静态任务表现上非常强。
- `quadratic_nosvd_debias` 更像 variance-based isolator：它在当前静态分析中压低 `SI`，但尚未证明它真的通过二阶项主导分发。
- `linear_no_center` 的高 margin 不是 specialization，而更像 norm inflation + collapse。

## 5. Experiment Design

### 5.1 New Order of Evidence
在真正做 CL verdict 之前，下一步实验顺序应改为：

1. **Mechanism Audit**
   - 先问：`quadratic_nosvd_debias` 到底有没有在按方差分发？

2. **Geometry Audit**
   - 再问：它的低 `SI` 是否伴随更清楚的 assignment 与更低 occupancy？

3. **CL Follow-up**
   - 最后才问：这些静态结构能否转化成更低 forgetting？

### 5.2 Minimal Mechanism Audit
- **Decision Question**：
  当前 `quadratic_nosvd_debias @ ckpt40000` 是否真的 learned to route by variance？

- **Compared models**：
  - `linear_running_center`
  - `acp_lite`
  - `quadratic_nosvd_debias`

- **Primary quantities**：
  - `rho`：quadratic 一阶/二阶 attribution ratio
  - `NMI(E,C)`：specialization
  - `r_{0.9}`：expert low-rankness

- **Decision rule**：

| Outcome Pattern | Interpretation | Next Action |
| --- | --- | --- |
| `rho <= 1` or unstable | quadratic 尚未学会 variance routing | 不要直接把它推进到 CL verdict；先停在 mechanism audit |
| `rho > 1` on hard domain pairs, with meaningful NMI / geometry pattern | quadratic 可能真实在按方差分发 | 进入 minimal CL forgetting test |
| `rho > 1` but no assignment / geometry improvement | 二阶项被用到了，但没有形成有用 routing structure | 重新审视机制价值 |

### 5.3 Minimal CL Follow-up
只有在 mechanism audit 支持时，才进入：
- `CS -> Medical`
- `Medical -> CS`

比较：
- `linear_running_center`
- `acp_lite`
- `quadratic_nosvd_debias`

核心指标：
- `Acc_A_after_A`
- `Acc_A_after_B`
- `ΔAcc_A`
- `Forgetting`
- `BWT`
- `Avg_after_B`

### 5.4 What Not To Do Right Now
- 不新增 router
- 不直接扩到 TRACE 全量 benchmark
- 不继续堆静态 proxy 轮次
- 不把 `quadratic architecture` 直接写成 `variance routing`

## 6. Conclusion / Update

### 6.1 New Results Integrated
- 静态结果已经足够说明：
  - `acp_lite` 是强的一阶 comparator；
  - `quadratic_nosvd_debias` 的静态剩余价值更可能体现在 anti-interference；
  - 但 mechanism 仍未闭环。

### 6.2 Main Interpretation
- 当前问题不再是“quadratic 强不强”，而是：
  1. 它是否真的在按方差分发？
  2. 如果是，这种机制是否真的减少 forgetting？

### 6.3 Stable vs Tentative
- **可冻结为稳定结论**：
  - `specialization` 不是 margin phenomenon，而是 assignment phenomenon；
  - `low-rankness` 不是架构属性，而是几何状态；
  - `quadratic architecture != variance routing`。

- **仍然只是 tentative evidence**：
  - `quadratic_nosvd_debias` 是否 learned variance routing；
  - 低 `SI` 是否会兑换成更低 forgetting。

### 6.4 Hypothesis Update

| ID | Old Status | New Status | Why Updated |
| --- | --- | --- | --- |
| H3 | active / comparator-focused | supported / expanded | 现在正式引入 mechanism 层 |
| H4 | active / narrowed | active / stricter | 必须先过 mechanism audit 再谈 CL necessity |
| H5 | active | active / strengthened | 低秩定义已被正式提升为主线建模 |

## 7. Version Upgrade / Pivot Decision
- **为什么这次要把旁路讨论升为主线**：
  - 它直接修复了当前最核心的概念混乱；
  - 它决定了实验 Agent 下一步到底在测什么；
  - 它影响 `Hypothesis / Mathematical Modeling / Metric Design / Experiment Design` 四个主干 section。

- **这次 pivot 的实质**：
  - 从“quadratic 有没有更好静态 proxy”
  - 切到“quadratic 是否真实通过二阶机制在做有用 routing”

## 8. Prism Report Sync

### 8.1 Recent Updates
- **Update**：我们把 `variance routing`、`specialization`、`low-rankness` 三个概念正式解耦。
  - **Conclusion**：以后不能再把 architecture、mechanism、assignment、geometry 混作一个词。
- **Update**：`acp_lite` 和 `quadratic_nosvd_debias` 的差异被重新解释为“一阶 buffering vs 二阶 isolating”的对照。
  - **Conclusion**：quadratic 的问题不再是“是否更强”，而是“是否真的在按方差分发”。

### 8.2 What Can Enter Main Text
- `specialization` 的 assignment 定义
- `low-rankness` 的 geometry 定义
- `quadratic architecture != variance routing`
- Architecture -> Mechanism -> Assignment -> Geometry -> CL Outcome 的主线图景

### 8.3 What Should Stay as Idea / Appendix
- `rho` 阈值的最终形式
- 是否用 `NMI` 或 `MI` 作为最终 specialization 指标
- 在完整机制审计前的任何 CL verdict

## 9. Open Problems and Immediate Next Actions
- **当前唯一关键未决问题**：
  - `quadratic_nosvd_debias` 在 `ckpt40000` 上到底有没有 learned variance routing？

- **下一步只做这 1-3 件事**：
  1. 对现有 `quadratic_nosvd_debias` 计算 `rho` attribution ratio
  2. 对现有三模型重算 `NMI(E,C)` 与 `r_{0.9}`
  3. 只有在 mechanism audit 支持时，再运行最小 two-task forgetting test

- **暂时不做的事**：
  - 不直接进入 TRACE 全量 benchmark
  - 不直接把两任务 forgetting test 当作第一步
  - 不继续扩展 `acp_on`

## 10. Key Insights
- **Insight 1**：`quadratic` 是否有价值，首先是一个 mechanism 问题，而不是 performance 排名问题。
- **Insight 2**：`specialization`、`low-rankness`、`variance routing` 已经可以被清楚分层，不应继续混用。
- **Insight 3**：实验 Agent 下一轮最重要的工作不是“再跑一轮 CL”，而是先验证 `quadratic` 是否真的在按方