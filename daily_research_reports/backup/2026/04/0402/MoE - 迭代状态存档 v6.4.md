# MoE - 迭代状态存档 v6.4

> 本版 checkpoint 不是对旧主线的否定，而是把当前 4.1 子问题正式提升为主线中的新阶段：  
> 我们现在不仅要问 `current quadratic 是否在按方差分发`，还要进一步问：  
> `二阶项到底编码了什么信息，哪些二阶信息与 MoE 专家分发真正相关，以及它们为何可能诱导更强的 expert specialization 与更低的 expert 内部占用维度。`

---

## 0. Checkpoint Metadata

- 项目：MoE Router for Continual Learning
- 版本：`v6.4`
- 日期：`2026-04-02`
- 当前阶段：`机制问题深化 / 4.1 子迭代启动 / 理论-实验双线联动`
- 当前 North Star：
  找到真正与专家分发强相关的结构信息，并把它从模糊的“二阶项直觉”提升成可定义、可测量、可验证的 routing mechanism。

---

## 1. Executive Summary

当前主线已经进一步收紧。

我们不再满足于说：
- 当前 quadratic 有二阶项；
- 当前 router 可能在按方差分发。

现在真正的问题变成了三层：

1. 二阶项 / 方差信息到底对应数据中的什么本质结构？
2. 这些结构中，哪些与 MoE 的专家分发强相关？
3. 如果专家分发真的利用了这些结构，为什么会表现为更专一的 assignment，以及更低的 expert 内部占用维度？

因此，本版 checkpoint 的核心升级是：

- 从“是否有二阶项”推进到“二阶项到底代表什么”
- 从“specialization 与 low-rankness 有关”推进到“二者为何有关”
- 从“mechanism audit”推进到“因果验证 + 训练进度同步”

### 1.1 Recent Delta for Theory Sync

这一轮相对上一版 `v6.3` 的新增点是：

- 新增理论问题：
  我们不再只问“当前 quadratic 是否在按方差分发”，而是进一步问“二阶项到底反映了什么信息，以及哪些二阶信息与 MoE 专家分发强相关”。

- 新增主线视角：
  当前问题被拆成三层：
  1. data structure layer
  2. routing mechanism layer
  3. geometry consequence layer

- 新增理论要求：
  需要对“specialization -> low-rankness”的关系给出更强解释，而不再只停留在经验观察。

- 新增实验方向：
  当前实验设计正式拆成：
  - Track A：静态因果验证
  - Track B：训练进度同步

- 本轮唯一要推进的问题：
  `哪些二阶结构真正与 MoE 专家分发相关，以及如何证明当前方法确实利用了这些结构。`

### 1.2 Copy-Ready Block for Theory Agent

下面这一块可以直接整段复制给 theory agent 作为连续同步输入。

#### Checkpoint Snapshot

- Executive Summary:
当前主线已从“quadratic 是否更强”推进到“二阶项到底编码什么信息、哪些二阶结构与 MoE routing 真正相关、以及它们为什么会表现为更专一和更低秩的 expert structure”。  
本版的关键升级是把问题分成 data structure、routing mechanism 和 geometry consequence 三层，并把实验设计拆成静态因果验证与训练进度同步两条线。

- Stable Knowledge:
1. `linear_running_center` 是当前严格 baseline。  
2. `acp_lite` 是当前最强公平 first-order comparator。  
3. `specialization`、`low-rankness`、`variance routing` 是三类不同层级的概念，不能混用。  
4. `specialization` 是 assignment-side 概念。  
5. `low-rankness` 是 routed covariance 的 geometry-side 概念。  
6. 当前 quadratic 更准确地说是 diagonal second-moment / centered-energy routing，而不是完整 variance routing。  
7. token-level expert inspection 已证明 experts 的确可以出现微观专一化。

- Hypothesis:
H1：某些二阶统计量确实编码了 domain / semantic separation 的结构信息。  
H2：如果 router 利用了与 separation 相关的二阶信息，则 experts 会表现出更清晰的 assignment specialization。  
H3：更清晰的 assignment specialization 会诱导更低的 expert 内部占用维度。  
H4：当前 quadratic family 只有在 routing decision 真正受相关二阶结构驱动时，才值得继续作为 variance-routing 路线推进。  
H5：更标准的 variance routing 路线应从 diagonal term 升级为 subspace-energy routing。

- Mathematical Modeling:
当前主线要求区分三层问题：
1. 二阶项本身编码了什么数据结构；
2. 这些结构是否真的进入 routing decision；
3. 这种 routing 是否导致更清晰的 assignment 与更低的 expert occupancy。  
当前 quadratic 形式只能访问坐标轴对齐的二阶能量，因此更准确的定位是 diagonal second-moment routing。  
如果要做更标准的 variance routing，目标形式应是 `x_c^T Q_e x_c` 或低秩形式 `||V_e x_c||^2`。

- Theory Handoff Readiness:
当前模式已经是 `Convergence Mode`。  
当前 Single Decision Question 是：  
`当前我们所说的“按方差分发”到底对应哪一类可计算的二阶结构，这些结构中哪些真正与 MoE 的专家分发相关，并且可以通过静态因果验证与训练进度分析被检验出来？`  
当前最小实验已明确为：
Track A：静态因果验证；Track B：训练进度同步。  
Decision rule 已明确，因此本轮 ready to produce Theory Pack。

#### Recent Delta

- 新增理论认识：
  “按方差分发”必须从模糊口语提升为“哪些二阶结构进入 routing decision”的可分析问题。

- 新增实验结果：
  当前还没有本轮新的结果写入这一版，主要是问题重构与实验计划升级。

- 被推翻或降级的旧判断：
  “只要存在二阶项就可以称为 variance routing”这一旧说法已被降级。

- 本轮唯一要推进的问题：
  `哪些二阶结构真正与 MoE routing 强相关，以及如何验证当前方法是否真的在利用它们。`

---

## 2. Stable Knowledge / Report-Ready Claims

| ID | Claim | Confidence | Notes |
| --- | --- | --- | --- |
| C1 | `linear_running_center` 是当前严格 baseline | high | 口径固定 |
| C2 | `acp_lite` 是当前最强公平 first-order comparator | high | 当前 benchmark 支持 |
| C3 | `specialization`、`low-rankness`、`variance routing` 是三个不同层级的概念 | high | 已成为主线前提 |
| C4 | `specialization` 是 assignment-side 概念，不应再由 margin 代替 | high | 已稳定 |
| C5 | `low-rankness` 是 geometry-side 概念，主对象是 routed covariance | high | 已稳定 |
| C6 | 当前 quadratic 形式更准确地说是 diagonal second-moment / centered-energy routing | high | 不应再直接叫完整 variance routing |
| C7 | token-level expert inspection 已证明 experts 的确可以出现清晰的微观专一化 | medium-high | 已有直接证据 |
| C8 | 静态 proxy 不能单独完成 CL verdict，但仍然是筛选路线的必要中间层 | high | 仍成立 |

---

## 3. New Mainline Questions

### Q1. 二阶项到底反映了什么？

我们当前不能再把“二阶项”简单理解成“方差”两个字。

需要区分：
- coordinate-wise fluctuation
- feature interaction / covariance structure
- projected energy on a subspace
- domain-conditional variance gap

当前主线要求把这几类量区分清楚。

### Q2. 哪些二阶信息与专家分发真正相关？

不是所有二阶信息都对 routing 有意义。

当前要回答的是：
- 哪些二阶结构能够帮助不同 domain / semantic groups 更清楚分开；
- 以及这些结构是否真的进入了 routing decision。

### Q3. 为什么专一性会诱导低秩？

这个问题现在不能只停在经验观察。

我们需要更强的理论桥梁说明：
- 更清晰的 assignment partition
- 为什么会压缩 expert 内部的 covariance occupancy
- 以及这件事为什么可能有利于 CL

---

## 4. Hypotheses

| ID | Hypothesis | Status | Reading |
| --- | --- | --- | --- |
| H1 | 某些二阶统计量确实编码了 domain / semantic separation 的结构信息，而不仅仅是噪声尺度 | active / core | 当前 4.1 的第一条主假说 |
| H2 | 如果 router 利用了与 domain / semantic separation 相关的二阶信息，则 experts 会表现出更清晰的 assignment specialization | active | 需要实验支持 |
| H3 | 更清晰的 assignment specialization 会诱导更低的 expert 内部占用维度 | active / strong | 理论上较强，仍需更系统验证 |
| H4 | 当前 quadratic family 只有在其 routing decision 真正受相关二阶结构驱动时，才值得继续作为 variance-routing 路线推进 | active / core | 当前机制主线 |
| H5 | 更标准的 variance routing 路线应从 diagonal term 升级为 subspace-energy routing | active / forward-looking | 当前理论 pivot |

---

## 5. Mathematical Modeling

### 5.1 Three Layers of the Question

当前主线问题必须分成三层：

1. `Data structure layer`
   - 二阶项编码了什么？

2. `Routing mechanism layer`
   - 这些结构是否真的进入 routing decision？

3. `Geometry consequence layer`
   - 这种 routing 是否导致更清晰 assignment 与更低 expert occupancy？

### 5.2 What Second-Order Terms May Represent

给定中心化特征：

$$
x_c = x - \mu_t,
$$

当前使用的二阶对象可写为：

$$
q(x)=x_c \odot x_c
$$
或
$$
q_{\text{deb}}(x)=x_c \odot x_c - \lambda_t.
$$

它至少可能编码三类信息：

1. 局部离散度
   - 某些坐标上的波动幅度

2. domain-conditional energy profile
   - 某些 domain 在某些方向上能量更大

3. concept activation volatility
   - 某类语义 / 风格 /词法 pattern 的激活不只体现在均值，也体现在波动与离散度

但当前形式的局限是：
- 它只能看坐标轴对齐的二阶能量
- 不能表达更一般的协方差方向

### 5.3 What “Routing by Variance” Should Mean Here

在当前项目里，更合理的工作定义应是：

`当 routing decision 主要由 domain-conditional second-order structure 决定，而不是仍由 first-order centered feature 主导时，才可以说 router 在按方差分发。`

因此需要区分：

- `second-order-capable architecture`
- `actually variance-driven routing`

它们不是一回事。

### 5.4 Why Specialization May Induce Low-Rankness

仍从总协方差公式出发：

$$
\mathrm{Cov}(x)=\mathbb{E}[\mathrm{Cov}(x\mid E)] + \mathrm{Cov}(\mathbb{E}[x\mid E]).
$$

如果 router 使 assignment 更清晰，则：
- expert 间中心或典型激活模式更分离；
- 第二项更大；
- 在总体 covariance 近似固定时，第一项更容易被压缩；
- 因而每个 expert 内部只占据更窄的有效子空间。

所以这里的逻辑不是：

`低秩 -> 专一`

而更像：

`更清晰的 routing partition -> 更受限的 expert 内部 occupancy -> 更低秩的几何状态`

### 5.5 Forward-Looking Formal Target

如果要真正做更标准的 variance routing，目标形式应写成：

$$
\ell_e(x)=x_c^\top Q_e x_c + b_e,\qquad Q_e \succeq 0,
$$

或者其低秩实现：

$$
\ell_e(x)=\|V_e x_c\|_2^2 + b_e.
$$

这一步的理论意义是：
- 把“坐标轴平方”升级为“子空间能量比较”
- 使 routing 真正对 feature anisotropy 敏感

---

## 6. Experiment Design

### 6.1 New Two-Track Plan

当前实验设计不再是一条线，而是两条并行但相互支撑的线。

### Track A：因果验证

问题：

`如果我们显式用二阶 / 方差信息去做聚类或 separation analysis，是否真的能看到更清楚的 domain / semantic structure？`

目标：
- 为“二阶项里确有与 routing 有关的信息”提供因果层面的支持

需要输出：
- 一阶特征与二阶特征的 separation 对比
- 可视化或 clustering quality
- domain / semantic grouping evidence

### Track B：训练进度同步

问题：

`当前基于二阶 / 方差改进的 router，在训练中是否逐步形成更清晰的 routing structure、合理收敛与 load balance？`

目标：
- 把“理论可能成立”与“模型真的正在学这个机制”区分开

需要输出：
- 训练 step / loss / convergence
- load balancing
- expert usage
- 可分析 checkpoint

### 6.2 Recommended Metrics

#### Assignment-side

- per-expert token distribution
- per-domain expert usage
- top tokens / top patterns per expert

#### Geometry-side

- `SI_e`
- `r_{0.9}`
- covariance overlap

#### Mechanism-side

- 二阶项贡献度
- `rho` 或同类 attribution ratio
- variance-feature clustering quality

### 6.3 Recommended Execution Split

当前 4.1 子迭代建议直接拆成两个实验 round：

#### Round A：Clustering / Separation Audit

目标：
- 用一阶与二阶表示的对比，验证二阶结构中是否确有与 domain / semantic separation 相关的信息。

输出重点：
- clustering / grouping quality
- separation 结果
- 可视化或结构化表格

#### Round B：Interference / Geometry Audit

目标：
- 在当前训练得到的 router 上，检查 routed activations 是否表现出更清晰的分离、更低 overlap、更明确的几何结构。

输出重点：
- `SI_e`
- overlap / covariance overlap
- `r_{0.9}`
- per-domain expert usage
- 必要的 token-level expert evidence

这两个 round 应顺序执行，不要混成一个大任务。

---

## 7. Workflow Decision

从这一版开始，4.1 子迭代的推荐顺序是：

1. 先和 theory agent 做多轮讨论
   - 修定义
   - 修机制解释
   - 修 specialization -> low-rankness 桥梁

2. 收束成 `Theory Pack`
   - 这轮至少要产生：
     - 因果验证实验卡
     - 训练进度同步实验卡

3. 交给 experiment agent
   - 先生成 `Experiment Pack`
   - 再执行

4. 结果整理成 `Result Pack`
   - 再发回 theory agent 更新 checkpoint

---

## 8. Theory Handoff Readiness

### 8.1 Current Discussion Mode

- 当前模式：`Convergence Mode`

原因：
- 4.1 的主题已经不再是松散探索，而是围绕一个清晰方向收束：
  `什么是按方差分发，以及哪些二阶信息真正与 MoE 专家分发相关`
- 当前已经具备：
  - 明确的主问题
  - 明确的理论分层
  - 明确的两轨实验入口
- 因此现在适合把理论讨论进一步收成正式 `Theory Pack`

### 8.2 Single Decision Question

本轮最核心的 `Single Decision Question` 是：

`当前我们所说的“按方差分发”到底对应哪一类可计算的二阶结构，这些结构中哪些真正与 MoE 的专家分发相关，并且可以通过静态因果验证与训练进度分析被检验出来？`

这句话有三个子层，但它们服务于同一个决策：
- 二阶项的含义是什么
- 哪些二阶信息与 routing 相关
- 应该如何验证这种相关性不是口头直觉

### 8.3 Minimal Experiment

当前最小实验不再是单个指标，而是一个最小双轨组合：

#### Track A：静态因果验证

目标：
- 检查二阶 / 方差特征是否真的比一阶特征更能揭示 domain / semantic separation

最小动作：
- 构造一阶特征表示与二阶特征表示
- 做 clustering / grouping / separation 对比
- 汇报哪些 domain 或 semantic groups 被分得更清楚

#### Track B：训练进度同步

目标：
- 检查新 router 在训练中是否真的形成了理论上想要的 routing 结构

最小动作：
- 汇报当前训练 step
- loss / 收敛情况
- load balancing
- expert usage pattern
- 可分析 checkpoint 的静态结构指标

### 8.4 Decision Rule

本轮 decision rule 应写成：

1. 如果二阶特征在静态因果验证中不能提供比一阶特征更清晰的 separation，
   则“按方差分发”的当前叙述需要降级，不能直接作为主线机制。

2. 如果二阶特征在静态因果验证中提供了更强的 separation，
   且训练中的 router 也逐步表现出更清晰的 expert specialization / load balance / geometry pattern，
   则支持继续推进 variance-aware routing 主线。

3. 如果静态因果验证支持，但训练中没有形成相应 routing structure，
   则说明“信息存在”与“router 学会使用该信息”之间仍有 gap。

### 8.5 What Theory Agent Should Output Next

theory agent 下一步应收束出一份正式 `Theory Pack`，至少包含：

1. `Hypothesis`
   - 二阶结构与语义 / domain separation 是否相关
   - 更清晰的 specialization 是否诱导更低秩 occupancy

2. `Mathematical Modeling`
   - 当前 second-order term 的准确定位
   - “按方差分发”的工作定义
   - 与 expert specialization 相关的可测对象

3. `Experiment Design`
   - Track A：静态因果验证
   - Track B：训练进度同步

4. `Conclusion/Update`
   - 当前能冻结什么
   - 当前仍不确定什么
   - 哪些内容值得交给 experiment agent

并且实验设计部分应明确拆成：
- `Round A: Clustering / Separation Audit`
- `Round B: Interference / Geometry Audit`

### 8.6 Ready to Produce Theory Pack?

- 结论：`Yes`

理由：
- 当前问题已经被压缩成单一决策问题
- 最小实验组合已经明确
- decision rule 已经能写出
- 继续发散讨论的收益已经低于进入实验验证的收益

### 8.7 Execution Constraints Note

这一节不是给 theory agent 的，而是之后交给 experiment agent 时补齐的执行约束。

- 代码目录：
  [待填写]

- 数据目录：
  [待填写]

- checkpoint 路径：
  [待填写]

- 输出目录：
  [待填写]

- 必须沿用的旧框架 / 脚本：
  [待填写]

- 明确不能改的边界：
  1. 本轮先做 4.1 主线下的静态因果验证与训练进度同步，不扩展到更大 benchmark。  
  2. 不允许 experiment agent 擅自重写“按方差分发”的理论定义。  
  3. 不允许擅自新增 router 变体并替代当前被要求分析的方法。  
  4. 如果出现局部阻塞，应先最小化提问，而不是整体换实验。  
  5. 输出必须整理成 `Experiment Pack` 和后续 `Result Pack`，不能只给日志。

---

## 9. Immediate Next Actions

当前推荐的最小动作只有三件：

1. 和 theory agent 先把 4.1 收成一份正式 `Theory Pack`
2. 让 experiment agent 做：
   - variance-based clustering / grouping 实验
   - 新方法训练进度与 load balance 同步
3. 用结果回写主线，决定是否继续推进更标准的 subspace-energy routing

---

## 10. What Not To Do Right Now

- 不要立刻扩大到更大 benchmark
- 不要急着把全部希望压到 two-task / forgetting
- 不要继续新增 router 变体而不先解释清楚二阶项在做什么
- 不要让 experiment agent 自己发散解释理论

---

## 11. Key Insight

本轮 4.1 的真正升级是：

`我们终于不再只是问“二阶 router 有没有用”，而是在问“二阶项到底对应什么信息，这些信息哪些与 MoE 专家分发强相关，以及它们为什么会表现为更专一、更低秩的专家结构”。`

这才是后续继续深入这条线的真正基础。
