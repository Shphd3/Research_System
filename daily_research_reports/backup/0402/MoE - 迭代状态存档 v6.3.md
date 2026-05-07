# MoE - 迭代状态存档 v6.3

> 本版的目标不是再开一条新故事线，而是把当前主线正式收束成可持续执行的研究工作流。  
> 我们现在已经不再缺“更多想法”，而是要把：
> 1. 主线理论，
> 2. 机制验证，
> 3. 实验交接，
> 4. 结果回写  
> 统一成一个稳定闭环。

---

## 0. Checkpoint Metadata

- 项目：MoE Router for Continual Learning
- 版本：`v6.3`
- 日期：`2026-04-02`
- 当前阶段：`主线建模已收束 / workflow 重构完成 / 下一步进入机制审计与实验闭环`
- 唯一 North Star：
  判断什么样的 routing mechanism 真正有助于 Continual Learning，而不是继续把不同层级的概念混在一起讨论“router 是否更强”。

---

## 1. Executive Summary

当前项目已经进入一个更清楚的阶段。

我们现在的主线不再是：
- “quadratic 是不是更强”

而是：
- `specialization` 到底是什么；
- `low-rankness` 到底是什么；
- 当前 quadratic 到底是不是在按方差分发；
- 如果它真的在按方差分发，这种机制是否对 CL 有结构性价值。

这版 checkpoint 的核心升级有两点：

1. 主线理论已经稳定成一条明确链条：

`Architecture -> Mechanism -> Assignment -> Geometry -> CL Outcome`

2. 工作流正式改造为：

`Checkpoint -> Theory Pack -> Experiment Pack -> Result Pack -> Checkpoint`

这意味着后续推进不再依赖临时 prompt 和人肉转述，而是依赖结构化包。

---

## 2. Stable Knowledge / Report-Ready Claims

| ID | Claim | Confidence | Notes |
| --- | --- | --- | --- |
| C1 | `linear_no_center` 的高 margin 不是健康 routing，而更像 norm inflation 与 collapse | high | 已有多轮静态结果支持 |
| C2 | `linear_running_center` 是当前最干净的严格 baseline | high | 口径已固定 |
| C3 | `acp_lite` 是当前最强的公平 first-order comparator | high | `ckpt40000` benchmark 支持 |
| C4 | `specialization`、`low-rankness`、`variance routing` 是三类不同层级的概念，不能再混用 | high | 已成为主线理论前提 |
| C5 | `specialization` 首先是 assignment phenomenon，而不是 margin 现象 | high | 反例足够清楚 |
| C6 | `low-rankness` 首先是 expert 内部 covariance 的几何状态，而不是架构属性 | high | 主定义已稳定 |
| C7 | 当前 quadratic 形式最多只能算 diagonal second-moment routing，不应直接叫做完整 variance routing | high | 理论澄清已稳定 |
| C8 | 静态 proxy 可以筛选路线，但不能单独完成 CL 判决 | high | 当前应作为稳定约束 |
| C9 | token-level routed token inspection 能直接提供专家专一性的微观证据 | medium-high | 已有结果卡支持 |

---

## 3. Current Mainline Questions

当前只保留下面三个主问题：

### Q1. 专家能不能变得更专一？

现在的答案不是抽象的“能”或“不能”，而是：
- 能；
- 但这种专一性首先体现在 token-level / micro-semantic / functional assignment 上；
- 不能简单等同为 document-level 主题纯度。

### Q2. 专一性与低秩性是什么关系？

现在的答案是：
- 二者不是同义词；
- `specialization` 是 routing assignment 的操作层结果；
- `low-rankness` 是 expert 内部特征分布的几何后果；
- 它们通过总协方差分解联系起来。

### Q3. 当前 quadratic 到底是不是“按方差分发”？

现在的答案是：
- 当前实现允许使用二阶信息；
- 但这不等于已经激活真正的 variance routing；
- 需要机制审计来判断二阶项是否真的主导了分发 margin。

---

## 4. Hypotheses

| ID | Hypothesis | Status | Current Reading |
| --- | --- | --- | --- |
| H1 | 对 CL 有意义的 specialization 必须由 assignment + balance 联合定义 | supported | 已成为稳定前提 |
| H2 | 更清晰的 expert partition 会诱导更低的 expert 内部占用维度 | active / strong | 理论上成立，实证上仍需系统重算 |
| H3 | 当前 `acp_lite` 的优势来自对 mean-related direction 与 centered residual 的显式一阶分解 | active / plausible | 是当前最合理解释，但仍需更系统机制证据 |
| H4 | 当前 quadratic architecture 只有在真正激活 variance routing 时，才可能对 CL 有独立结构价值 | active / core | 当前主线 bottleneck |
| H5 | 真正值得推进的 variance routing 方向，应从对角二阶项升级到子空间能量路由 | active / forward-looking | 这是当前理论 pivot |

---

## 5. Mathematical Modeling

### 5.1 Three Concepts

#### 5.1.1 Expert Specialization

`specialization` 是 assignment-side 概念。

它回答的问题是：
- 某类 token / domain / cluster 是否稳定地被送往某些专家；
- 同时这种分配是否保持非塌缩的 load balance。

它不是：
- 高 margin
- 低秩
- 低 SI

推荐理解：

`specialization = selective assignment under non-collapse`

#### 5.1.2 Expert Low-Rankness

`low-rankness` 是 geometry-side 概念。

对于 expert `e`，定义 routed feature covariance：

$$
C_e = \mathrm{Cov}(x \mid E=e).
$$

若 `C_e` 的有效能量主要集中在较少维度上，则称 expert `e` 处于 low-rank geometric state。

推荐主指标：
- `r_{0.9}(C_e)`

辅助指标：
- `d_\tau(C_e)`
- `ED_comp`

其中 `ED_comp` 不再作为首要定义量，只保留为历史兼容 proxy。

#### 5.1.3 Variance Routing

`variance routing` 是 mechanism-side 概念。

它回答的问题不是“模型里有没有二阶项”，而是：
- 路由决策是否真正由二阶统计结构主导。

对当前 quadratic 形式：

$$
\ell_{\text{quad}}(x)=W_1 x_c + W_2 \big(x_c \odot x_c - \lambda_t\big),
$$

它只能访问按原坐标轴分解的中心化二阶能量。

因此更准确的名字是：

- `diagonal second-moment routing`
或
- `coordinate-wise centered-energy routing`

而不是完整的 variance routing。

### 5.2 Why Specialization and Low-Rankness Are Related but Not Identical

用总协方差公式：

$$
\mathrm{Cov}(x)=\mathbb{E}[\mathrm{Cov}(x\mid E)] + \mathrm{Cov}(\mathbb{E}[x\mid E]).
$$

它说明：
- 第二项变大，意味着 expert 间均值或中心更分离；
- 在总体能量近似固定时，第一项更容易被压缩；
- 于是更清晰的 assignment partition 往往诱导更低的 expert 内部占用维度。

所以：

- `specialization` 是 routing mechanism 的 assignment 结果；
- `low-rankness` 是这种 partition 的一个几何后果。

一句话固定：

`Specialization is the routing-side operation; low-rankness is one geometric consequence.`

### 5.3 From Centering to ACP-Lite

定义：

$$
x_c = x - \mu_t.
$$

对 `acp_lite`，我们把输入拆成：
- `x_{\parallel}`：沿 mean-related dominant direction 的分量
- `x_c`：中心化后的 residual 通道

当前最合理的一阶解释是：
- `x_{\parallel}` 更接近 domain bias / frequency-like / global shift information
- `x_c` 更接近去偏后的 semantic residual

因此 `acp_lite` 的优势并不是“神奇地更好”，而是它给 router 提供了一个更干净的 first-order decomposition。

### 5.4 From Diagonal Quadratic to True Variance Routing

如果我们真的要做“按方差分发”，更标准的目标形式应是：

$$
\ell_e(x)=x_c^\top Q_e x_c + b_e,\qquad Q_e \succeq 0.
$$

其低秩实现可写为：

$$
\ell_e(x)=\|V_e x_c\|_2^2 + b_e.
$$

这对应的不是单个坐标上的平方，而是：
- 某个 learnable subspace 上的 energy；
- 也就是 feature anisotropy 在专家级路由上的显式利用。

因此当前理论 pivot 很清楚：

- 旧问题：`quadratic 有没有二阶项`
- 新问题：`router 是否学会了沿关键子空间比较 energy`

---

## 6. Empirical Position So Far

### 6.1 What We Can Already Say

- `acp_lite` 在当前 `ckpt40000` benchmark 上是最强 first-order comparator。
- `quadratic_nosvd` 与 `quadratic_nosvd_debias` 提供了不同的二阶路线信号，但不能合并成一个简单故事。
- token audit 已经显示专家确实会出现较清楚的功能性或微语义专一化。

### 6.2 What We Still Cannot Say

- 不能说当前 quadratic 已经在真正按方差分发。
- 不能说低 `SI` 已经证明更低 forgetting。
- 不能说当前 static audit 足以替代 CL 验证。

---

## 7. Workflow Upgrade

从本版开始，工作流正式固定为：

`Checkpoint -> Theory Pack -> Experiment Pack -> Result Pack -> Checkpoint`

### 7.1 Theory Pack

理论端讨论结束后，必须输出：
- `Checkpoint Snapshot`
- `Discussion Distillate`
- `Target Experiment`
- `Metrics and Decision Rule`
- `Implementation Constraints`
- `Theory -> Experiment Card`

### 7.2 Experiment Pack

实验端收到后，必须先锁协议：
- `Task Restatement`
- `Implementation Plan`
- `Protocol Lock`
- `Output Contract`
- `Risk Check`
- `Execution Checklist`

### 7.3 Result Pack

实验完成后，必须回传：
- `What Was Actually Run`
- `Core Result Table`
- `Reliability / Anomaly Audit`
- `Theory-Implementation Mismatch`
- `Hypothesis Update Suggestion`
- `Recommended Checkpoint Delta`
- `Report-Ready Summary`
- `Experiment -> Theory Card`

### 7.4 Why This Upgrade Matters

它直接解决了你当前最痛的两个问题：

1. 理论 AI 多轮讨论后的信息无法稳定交给实验 AI
2. 实验 AI 每轮容易 task drift，且完成后结果又不容易回写主线

从现在开始，聊天记录不再是交接物；
结构化包才是交接物。

---

## 8. Next-Step Decision

### 当前唯一 bottleneck

当前唯一真正值得推进的 bottleneck 是：

`当前 quadratic 路线到底有没有激活足够明确的二阶机制，值得继续往真正的 variance routing 深挖。`

### 下一步推荐顺序

1. 先做一轮标准化的机制审计包
   - 输入：当前 checkpoint + Theory Pack
   - 输出：清楚区分
     - 当前 quadratic 在按什么分发
     - 当前 expert specialization 在 token-level 上到底长什么样

2. 在机制层证据更清楚后，再决定：
   - 是继续推进 subspace-energy routing
   - 还是转入更强的 CL 验证

### 当前不做

- 不再堆新的 prompt 文档
- 不再把聊天记录直接发给实验 AI
- 不在没有机制闭环时就把所有希望压到 CL 结果上

---

## 9. Immediate Action List

今天开始，严格执行下面三步：

1. 用新的 [科研迭代Prompts.md](C:/Users/250010109/iCloudDrive/SLAI_ios/research_files/科研迭代Prompts.md) 作为唯一主文档
2. 每一轮理论讨论结束后，产出一个 `theory_pack.md`
3. 每一轮实验结束后，产出一个 `result_pack.md`

如果下一轮要给实验 AI 开工，默认输入应当是：

- 当前 checkpoint
- 当前轮次 `Theory Pack`
- 一张 `Theory -> Experiment Card`
- 补充的工程路径 / checkpoint / 输出目录

---

## 10. Key Insight

你现在最重要的升级，不只是理论更清楚了，而是推进方式变得更稳了。

以前的问题是：
- 理论讨论很多
- 实验执行很多
- 但交接和回写很松

现在要改成：
- 理论先收成包
- 实验按包执行
- 结果按包回写

只有这样，生产力才会真正提升。
