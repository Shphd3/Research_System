# 0721 理论审计与 Router 后续研究计划

> 日期：2026-07-22  
> 依据：0721 组会 ASR 原文、组会问题笔记、概率性稀疏激活树文档、NTP 层级—频率实验说明，以及 ResearchSystem 当前正式 anchors。

> 本文负责理论裁定、真实证据边界与后续 Router 研究安排；为便于与原合并稿回溯，保留原第 0、4–13 节编号。
> 组会原话校订与术语答疑见 [0721 组会语义校订与理解答疑](0721_组会语义校订与理解答疑.md)。

## 0. 核心判断与总裁定

你的核心判断可以准确重述为：

> 你试图用“语言具有可复用的层级/树状关系—NTP 更容易把高频共享关系集中到少数方向—MoE Router 应当隔离 common 与 rare、短程与长程、不同组合模式”形成一条研究主线；但你已经意识到，当前缺失的不是又一个 Router 结构，而是四个前提：被讨论的“秩”究竟属于什么对象、概率树是否给出非平凡预测、真实工作负载是否存在稳定专家效用差异、Router 的成功指标究竟是什么。

**总裁定：**

1. 组会中“高秩/低秩、熵、确定性、长序列”被混用了。首先必须固定被测对象，否则所有后续结论都会换义。
2. 概率树定理在数学上成立，但目前只是条件计算容量上界；它不是自然语言低秩定理，也没有推出 MoE 必要性。
3. 学长的 NTP 实验与概率树有“关系复用”这一候选联系，但实验实际操纵的是共享频率和规则复杂度，不是树层级或距离；它测的是参数删谱后的功能敏感性，而不是条件根表示秩。
4. 当前最优先任务不是设计 Router，而是验证真实工作负载上是否存在**跨切分稳定的反事实专家效用 headroom**。没有这一点，任何 Router 都没有功能目标。
5. 四卡资源应拆成 2+2：两卡做真实 MoE 的 utility headroom 审计，两卡做严格控制的合成桥接实验。只有真实 headroom 通过后，才进入 Router 方法设计。

---

## 4. 最关键问题：这是对语言的描述，还是我们要创造的表征空间？

### 4.1 结论

**两者都不是简单的“是”。正确对象应当是：为 Router 构造任务充分的决策表征，而不是把整个语言表征强行改造成低秩树空间。**

### 4.2 描述性层面

当前语言模型表示中确实常见：

- 各向异性或共享方向；
- 某些语言结构可被低维线性 probe 读取；
- 不同层对词法、句法、语义等信息的可读性不同；
- 某些任务适应只需低维更新。

但这些现象不等于存在一个普适、错误的 “common 子空间”。共享方向可能承载词频、位置、语法或稳定语言规律，对主模型本身可能有用。

### 4.3 规范性层面

对 Router 而言，common 成分只有满足以下条件时才是 nuisance：

1. 它强烈影响 Router logits 或负载；
2. 它对“哪个专家能降低任务损失”几乎没有预测力；
3. 去掉它能够降低 routing regret，同时不损害任务效用。

ResearchSystem 的现有证据只支持：common 可以改变负载和几何可解释性；它没有证明 common removal 能恢复专家身份或专家效用。真实 DCLM 上，简单低秩 common-logit bridge 也不足以解释和救援训练覆盖。

### 4.4 更准确的 Router 表征目标

定义每个输入的反事实专家效用向量：

$$
u(x)=\big(L^{cf}_1(x),\ldots,L^{cf}_E(x)\big).
$$

Router 不需要恢复“完整语义”，它只需要保留足以预测 $u(x)$ 或其最优专家的状态。

**AI 提议：utility quotient representation。**

把具有相同专家效用排序的 hidden state 视为路由等价：

$$
h\sim h'\quad\Longleftrightarrow\quad
\operatorname{order}(u(h))=\operatorname{order}(u(h')).
$$

Router 应学习这个等价类，而不是对 hidden state 做无目标聚类。只有被证明对 $u(x)$ 不变的 common 方向才应被商掉或投影掉。

这回答了你的逻辑疑问：

- 当前表征空间可能已经包含路由所需信号，也可能没有；要先测可达性。
- 当前表征中的 common 不一定是语言模型的问题，而可能是 Router 读出时的 nuisance。
- 我们需要设计的是**路由充分表征**，不是“正确语言空间”的大一统定义。

---

## 5. 概率性稀疏激活树：正确性、非平凡性与缺口

### 5.1 数学上成立的部分

给定固定激活模式 $m$，若活动叶子集合为 $A(m)$，路径算子为 $B_u(m)$，则

$$
h_\rho^{(m)}=\sum_{u\in A(m)}B_u(m)h_u.
$$

因此根表示属于路径像空间之和：

$$
\mathcal R_\rho(m)=\sum_{u\in A(m)}B_u(m)S_u,
$$

并有

$$
\operatorname{rank}(H_\rho^{(m)})
\le q(m)
\le \sum_{u\in A(m)}r_u
\le rN(m).
$$

若 $\Pr[N(M)\le s\mid C=c]\ge 1-\delta$，则以至少 $1-\delta$ 的概率有 $q(M)\le sr$。这个证明正确。

### 5.2 它目前是什么，不是什么

它是：

> 固定线性路径算子下，任务条件稀疏计算的可达维数上界。

它不是：

- 自然语言全局低秩定理；
- token 概率生成树；
- NTP 参数低秩定理；
- 低维活动树保留任务信息的证明；
- 必须使用 MoE 或 Router 的证明。

### 5.3 何时才非平凡

上界 $q(m)\le sr$ 只有同时满足以下条件才有科学内容：

1. $sr\ll d$，否则只是环境维数的平凡上界；
2. 每个条件不是对应一个独一无二模式，否则“每次低维”无法泛化；
3. 少量模式能跨样本复用；
4. 固定/共享路径算子近似真实计算；
5. 非线性、残差和未激活分支造成的误差足够小；
6. 活动子树在 held-out 数据上保持任务效用。

第 6 条与低维性独立，是当前最重要的缺口。

### 5.4 当前模型的四个必须改进

#### 改进一：区分三张图

必须分别定义：

1. 语言或任务的潜在依赖图；
2. 模型实际使用的活动计算图；
3. 参数/表示的线性几何。

树拓扑只描述依赖，不直接决定参数秩。

#### 改进二：从二元门改为有效活动支持

真实 attention/router 多为 soft gate。若所有权重非零，严格秩很容易满秩。更实际的对象是：选取贡献最大的 $s$ 条路径后，遗漏项的能量是否小于 $\varepsilon$。需要证明近似可达维数，而非严格秩。

#### 改进三：加入模式复用复杂度

即使每个模式只有一维，若每个样本使用不同模式，其并集仍可全维。应同时度量：

- 模式数或模式熵 $H(M\mid C)$；
- 模式跨样本复用率；
- 路径像空间重叠；
- 模式能否由输入稳定识别。

#### 改进四：加入任务充分性

定义完整表示与稀疏表示的最优任务风险：

$$
R_{sparse}-R_{full}\le\varepsilon.
$$

只有同时满足条件低维和低 excess risk，才是有效任务摘要。

### 5.5 与 NTP 参数低秩之间缺失的桥

当前概率树约束的是条件根表示；NTP 实验删减的是 $W_q/W_k$ 参数谱。两者不是同一个对象。

**AI 提议：复用加权梯度桥接命题。**

令 $B_{QK}$ 表示真正决定 attention score 的双线性算子。设模式 $m$ 的每样本梯度期望为 $G_m$，且 $\operatorname{rank}(G_m)\le r_m$。局部线性化下，训练更新近似为

$$
\Delta B_{QK}
\approx -\eta\sum_m n_m G_m+E,
$$

其中 $n_m$ 是模式出现次数，$E$ 是优化、上下文和有限样本残差。对少量高频复用模式集合 $F$，

$$
\operatorname{rank}\left(\sum_{m\in F}n_mG_m\right)
\le\sum_{m\in F}r_m.
$$

若高频项形成谱隙、残差谱范数较小，并且任务损失对该局部算子扰动稳定，那么高频模式会集中在头部功能子空间；稀有、彼此不对齐的模式则更多进入尾部方向。

这条桥接假设可以解释“高频复用关系删尾后仍稳定”，但还不是证明。它需要直接测：

- per-example 梯度对齐；
- $B_{QK}$ 的谱，而非只看单独 $W_q/W_k$；
- 关系频率、规则复杂度和距离的独立操纵；
- held-out 功能秩。

---

## 6. 学长 NTP 实验的正确解读

### 6.1 实验实际上做了什么

数据为 $A|B|C|D$。核心任务是在 B 结束后预测 C，固定 A/C 节点频率、句长、样本数和 A→C 距离，只改变同一套 A→C 映射能跨多少种 B 上下文复用：share16、share4、share2、random_unshared。

主要结果：

- 64 维模型中复用越多，达到 matched fit 越快；
- share16 对 $W_q/W_k$ 尾部删谱最稳定；
- $W_v/W_o$ 和第一层 hidden 在保留四分之一 rank 时差异较小；
- 因此候选机制集中在 QK 路由，而非值传输。

### 6.2 它与树模型的联系

树或层级结构可以提供跨上下文复用的中间关系；真正把关系推入主要方向的候选原因是这些关系被反复调用。因此较安全的链条是：

$$
\text{层级结构}
\rightarrow\text{允许中间关系复用}
\rightarrow\text{重复梯度更一致}
\rightarrow\text{QK 功能方向更集中}.
$$

树是复用的结构来源，不是低秩的充分原因。

### 6.3 当前结论不能说什么

1. 没有比较长程与短程：A→C 距离在各 setting 中固定。
2. B→D 是删谱损坏对照，不是严格的短程机制对照。
3. 数据是链式条件关系，不是真正的多分支树计算。
4. 单独 $W_q/W_k$ 的谱依赖参数分解方式。若
   $$W_Q'=W_QR,\quad W_K'=W_KR^{-T},$$
   则 attention score 算子不变，但单个矩阵的奇异谱可以变化。因此应优先分析不变的 $B_{QK}$ 或联合功能压缩。
5. share16 到 random_unshared 不仅改变频率，也改变独立映射规则数量和对 B 的条件依赖，即“关系频率”与“函数描述复杂度”混杂。

### 6.4 更准确的实验结论

> 在当前单层单头 NTP 合成任务中，跨上下文复用程度更高的 A→C 关系学得更快，并且在当前参数化下更能耐受 Q/K 尾部方向删除；这支持“共享复用使路由计算集中”的候选机制，但尚未证明层级、距离、表示秩或概率树机制。

### 6.5 下一轮合成实验必须分离的变量

第一轮只做四个轴，避免继续大一统：

| 轴 | 操纵 | 主要预测 |
|---|---|---|
| 复用频率 | 固定规则数，改变每条规则重复次数 | 提高梯度对齐、降低功能秩 |
| 规则复杂度 | 固定频率，改变 B 条件映射数量/描述长度 | 复杂度提高需要更多功能方向 |
| 距离 | 固定频率和规则，插入不同长度干扰 | 主要增加 score margin，不必增加 rank |
| 组合分支数 | 目标需一个或多个独立证据源 | 独立源增多时条件功能维数上升，除非路径空间复用 |

必须加入：树 vs 平坦依赖的匹配对照、$B_{QK}$ 谱、梯度协方差谱、随机子空间删减、held-out 功能秩和条件表示秩。

---

## 7. NTP、MTP 与“短视”的正确理解

### 7.1 NTP 并非简单短视

NTP 在位置 $t$ 的直接标签是 $x_{t+1}$，但 $h_t$ 可以读取整个前缀，参数又跨位置共享。只要下一个 token 的正确预测需要远程信息，NTP 就能学习长程依赖。因此“只预测一步”不等于“只能使用一步信息”。

更准确的局限是：

> 当前位置的直接监督只奖励对下一 token 有用的信息；更远未来的信息只有在通过共享参数、后续位置或下一 token 需求间接产生梯度时才被强化。

### 7.2 MTP 提供了什么

典型 MTP 为同一 $h_t$ 增加多个未来目标：

$$
L_{MTP}=\sum_t\sum_{k=1}^{K}\lambda_k
\operatorname{CE}(g_k(h_t),x_{t+k}).
$$

它能把更远目标的直接梯度提前送到当前位置，并在大模型与代码任务中显示样本效率和性能收益。但它不自动证明：

- $h_t$ 已形成连贯的未来 belief state；
- 标准 next-token head 会使用这些信息；
- Router 会因此学到更好的专家划分；
- 长程语义而非相邻 token 相关性造成收益。

ResearchSystem 的 A11 结论与此一致：future target 的信息形成和参数传输有受控证据，但强的标准头因果使用增量尚未建立。

### 7.3 MTP 在 Router 研究中的正确位置

MTP 不应先被当成“更好的专家标准”。它是一个训练干预。应比较它是否改变：

- 反事实专家效用矩阵 $L^{cf}_{z,e}$；
- 最优专家身份的跨切分稳定性；
- 长程/组合条件上的 oracle headroom；
- learned Router 的 route regret；
- 标准 NTP 与最终任务效用。

只有在 matched task performance/checkpoint 下，MTP 产生更清晰、更稳定、可捕获的 utility structure，才能说它帮助了 specialization。

---

## 8. Expert specialization 的严格定义

对工作负载条件 $z$、专家 $e$，定义强制选择专家后的 held-out 损失：

$$
L^{cf}_{z,e}=\mathbb E[\ell(y,F_e(h(x)))\mid z].
$$

最优专家与效用间隔：

$$
e^*(z)=\arg\min_eL^{cf}_{z,e},
$$

$$
G_z=\min_{b\ne e^*(z)}
\big[L^{cf}_{z,b}-L^{cf}_{z,e^*(z)}\big].
$$

Router regret：

$$
R_{route}=L_{learned}-L_{oracle}.
$$

功能性 specialization 至少要求：

1. 不同条件存在不同的最优专家；
2. 最优专家身份在 calibration/test 或不同 repository split 上稳定；
3. 效用 gap 为正并超过噪声；
4. learned Router 能捕获一部分 oracle headroom；
5. 在相同 active FLOPs、通信和负载约束下仍成立；
6. 替换/移除匹配专家会因果降低效用。

NMI、负载均衡、专家激活数、token 类别可解释性都不能单独证明 specialization。

### 8.1 你对 loss utility 的疑问

NTP cross-entropy 不是天然错误的 utility。如果部署任务就是 next-token repository completion，它是合理主指标。问题在于：

- 单次 token loss 噪声大；
- strict top-1 只观察被选专家，缺少未选专家反事实；
- 训练期 loss 可能偏向高频局部 token；
- 真实任务可能关心整行、编译、测试或跨文件正确性。

因此应使用分层指标：

1. token NLL：高效、适合 forced-expert 大规模审计；
2. target-line exact/edit/compile：验证局部生成；
3. repository-level tests 或 endpoint task：最终 utility；
4. q10/LCVaR 等尾部指标：检查 rare/long-range 条件是否被牺牲。

---

## 9. 重新归纳后的研究问题：先不给方案

### 9.1 主问题

> 在未预筛选的 repository-level code completion 工作负载中，跨文件、长程、低频或多证据组合条件是否产生跨 repository split 稳定的专家效用异质性，并且现有 Router 未能捕获这部分 headroom？

### 9.2 三个必要子问题

1. **存在性：**冻结专家后，forced-expert utility matrix 是否存在稳定结构？
2. **可达性：**当前 hidden state 是否包含足以预测最优专家的信号，还是 expert 本身近似可交换？
3. **学习性：**若信号存在，普通 top-k 训练为何没有捕获——common nuisance、selected-path blindness、早期锁定，还是尾部样本不足？

顺序不能颠倒。没有第 1 项，研究 Router 读出或训练机制没有目标。

### 9.3 最强竞争解释

> MoE 的收益主要来自总参数容量和负载分配；在具体真实工作负载内，专家函数对条件近似可交换，所谓语义/树状 specialization 只是 token 频率、位置和负载的表面相关。

第一阶段实验必须能直接否定或接受这个解释。

---

## 10. Benchmark 选择

### 10.1 主现实工作负载

| Benchmark | 用途 | 适合原因 | 主要局限 |
|---|---|---|---|
| CrossCodeEval | 跨文件代码补全 | 静态分析筛出确需跨文件上下文的样例；四种语言 | 主要是补全指标，未必有执行测试 |
| RepoBench-C/P | repository-level 补全与检索—补全管线 | 有 in-file、cross-file-first、cross-file-random 分层 | Edit/Exact 等表面指标不能完全代表功能正确 |

它们比 HumanEval/MBPP 更适合作为第一主任务，因为后两者主要是短、单文件函数生成，不能直接诊断你的跨文件、长程组合 workload。

### 10.2 机制诊断任务

| Benchmark | 诊断变量 | 地位 |
|---|---|---|
| RULER multi-hop tracing / aggregation | 距离、检索、聚合、多跳 | 合成诊断，不是现实效用证明 |
| BABILong | 长干扰文本中的事实链、归纳、演绎 | 长程组合诊断 |
| 自建 factorial tree 数据 | 频率、规则复杂度、距离、分支数完全可控 | 理论桥接必要，但不能单独证明现实价值 |

SWE-bench 不应作为第一阶段：它混入代理规划、工具调用、检索、补丁生成和测试执行，成本高且难以归因 Router 机制。

---

## 11. 四卡资源的具体顺序

## 阶段 0：冻结问题与判据，不训练新 Router

产物只需一页：

- 主问题；
- utility 定义；
- calibration/test 按 repository 切分；
- 最强竞争解释；
- go/no-go 阈值；
- 哪个结果会停止 Router 设计。

不要先决定 common projection、树 Router 或 MTP Router。

## 阶段 1A：两卡做真实工作负载 utility headroom

### 模型

优先选择可完全访问专家和 Router 的开放 MoE。OLMoE-1B-7B 是合适候选：总参数约 7B、每 token 激活约 1B、代码和训练资产开放。具体是否两卡可运行取决于显存；显存不足时先量化冻结权重或缩短序列，而不要换成不可审计 API 模型。

### 数据

- CrossCodeEval + RepoBench-C 的未筛选样本；
- 按 repository 切 calibration/test；
- 预注册条件：in-file / cross-file、依赖距离、相关文件数、证据 hop 数、符号频率、目标类型。

### 实验

1. 预先固定少量 early/mid/late MoE layer；
2. 冻结模型；
3. 对 calibration 样本逐专家强制通过，构造 $L^{cf}_{z,l,e}$；
4. 在 calibration 选择 $a_l(z)$；
5. 在 test 只评估预先选择的专家、native Router、load-matched random 和 shortcut controls；
6. bootstrap 单位使用 repository，而不是 token；
7. 同时报平均 NLL、尾部 NLL、目标行指标和 active cost。

### 通过条件

- held-out oracle headroom 的置信区间下界为正；
- useful expert identity 跨 split 高于置换/机会基线；
- 优势在 token identity、长度、频率和 local-only 控制后仍存在；
- 不是单一专家全局更强造成的。

若失败，停止在该 workload 上设计语义 Router。

## 阶段 1B：另两卡并行做概率树—NTP 桥接

只做一个 factorial 小模型，不扩展到大一统语言：

- 复用频率 × 规则复杂度；
- 固定节点边际、距离、样本数；
- 之后再单独加入距离和分支数；
- 同时测 $B_{QK}$、per-example gradient alignment、条件 hidden rank、功能删谱曲线；
- 加入 tree vs flat matched control；
- 使用 matched checkpoint 和 held-out context。

关键判据：频率效应是否在规则复杂度匹配后仍存在，以及梯度对齐能否中介频率—功能秩关系。

## 阶段 1 决策门

| 真实 headroom | 合成桥接 | 决策 |
|---|---|---|
| 无 | 任意 | 停止 Router 架构；换 workload 或 expert capacity |
| 仅窄条件有 | 有/无 | 把 Router 目标缩窄到该条件，不做通用 Router |
| 稳定为正 | 无 | 先研究真实 utility signal，不用树理论包装 |
| 稳定为正 | 有 | 才进入树/utility-aware Router 候选 |

## 阶段 2：仅在 headroom 通过后设计 Router

两卡训练、两卡验证：

- 基线：native top-k、load-balanced Router、共享/稠密 matched-compute；
- 候选 Router 必须预测 expert advantage，而非聚类 hidden state；
- 定期强制少量 challenger expert，获得未选专家反事实；
- 对 rare/long-range strata 采用尾部保护或有限探索；
- common projection 只有在被证明 utility-invariant 后才使用；
- 所有方法匹配 active FLOPs、通信和专家容量。

**AI 提议，条件性方法：utility-contrastive Router。**

让 Router 学习相对共享专家的效用增益：

$$
s_e(x)\approx L_{shared}(x)-L^{cf}_e(x),
$$

训练标签来自低比例 forced challenger，而非 token 类别或谱聚类。该想法只有在阶段 1A 的 headroom 通过后才值得实现。

## 阶段 3：最后再引入 MTP

在相同数据、初始化、任务性能和模型规模下比较 NTP/MTP：

- utility matrix 是否更稳定；
- 长程条件 oracle headroom 是否扩大；
- Router regret 是否下降；
- 标准 NTP/task head 是否真正使用 MTP 形成的信息。

MTP 是独立因果因素，不应与 Router 结构同时改变。

---

## 12. 解决到什么程度可以推进，而不是钻牛角尖

一个问题不需要“完全解决”，只需达到当前决策所需的证据层级。

### 12.1 四项推进标准

当以下四项都具备时，就应推进：

1. **对象固定：**清楚说明熵、表示秩、参数秩还是功能秩；
2. **主张边界：**明确只声称什么、不声称什么；
3. **竞争解释：**保留一个最强 rival，而不是列十种可能；
4. **决策实验：**下一实验的不同结果会导致不同动作。

若一个实验无论成功失败都不改变下一步，它不值得做。

### 12.2 三个关闭层级

| 层级 | 达标含义 | 是否需要继续 |
|---|---|---|
| 定义关闭 | 对象、指标、条件无歧义 | 可以进入机制实验 |
| 机制关闭 | 至少一个受控实验区分主机制与最强 rival | 可以进入现实验证 |
| utility 关闭 | held-out 真实任务、matched cost、因果控制通过 | 可以做方法与论文主张 |

不要为了进入下一阶段而等待“自然语言为何低秩”的普适理论。对当前 Router 决策，概率树做到假设和边界明确已经足够；真正阻塞的是现实 utility headroom。

### 12.3 明确的 park 规则

出现任一条件就 park：

- 两次预注册、控制充分的实验效应都低于最小效应阈值；
- 结果跨 seed/split 符号不稳定；
- 只改善 NMI、负载或谱指标，不改善反事实 utility；
- 新理论不改变预测、主张边界或下一决策；
- 当前资源无法区分最强竞争解释。

---

## 13. 现在应立即完成的唯一任务

先完成阶段 0 和阶段 1A 的最小协议：

> 冻结一个开放 MoE，在 CrossCodeEval/RepoBench 的 repository-held-out split 上，测少数预注册层的 forced-expert utility matrix、split-stable oracle headroom 及其 nuisance controls。

这是下一阶段的 start point。概率树修正与合成实验可以并行，但不能替代这道现实 workload gate。

---

## 参考论文（按用途）

### 信息论、秩与表示

1. Shannon, C. E. *A Mathematical Theory of Communication*. Bell System Technical Journal, 1948.
2. Roy, O. & Vetterli, M. *The Effective Rank: A Measure of Effective Dimensionality*. EUSIPCO, 2007.
3. Ethayarajh, K. *How Contextual are Contextualized Word Representations?* EMNLP-IJCNLP, 2019.
4. Hewitt, J. & Manning, C. D. *A Structural Probe for Finding Syntax in Word Representations*. NAACL, 2019.
5. Tenney, I. et al. *BERT Rediscovers the Classical NLP Pipeline*. ACL, 2019.
6. Aghajanyan, A. et al. *Intrinsic Dimensionality Explains the Effectiveness of Language Model Fine-Tuning*. ACL, 2021.
7. Hu, E. et al. *LoRA: Low-Rank Adaptation of Large Language Models*. ICLR, 2022.
8. Zhang, C. et al. *Understanding Deep Learning Requires Rethinking Generalization*. ICLR, 2017.
9. Yun, C. et al. *Are Transformers Universal Approximators of Sequence-to-Sequence Functions?* ICLR, 2020.
10. Rahaman, N. et al. *On the Spectral Bias of Neural Networks*. ICML, 2019.

### MoE 与 Router

11. Shazeer, N. et al. *Outrageously Large Neural Networks: The Sparsely-Gated Mixture-of-Experts Layer*. ICLR, 2017.
12. Fedus, W. et al. *Switch Transformers: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity*. JMLR, 2022.
13. Zhou, Y. et al. *Mixture-of-Experts with Expert Choice Routing*. NeurIPS, 2022.
14. Xue, F. et al. *OpenMoE: An Early Effort on Open Mixture-of-Experts Language Models*. 2024.
15. Muennighoff, N. et al. *OLMoE: Open Mixture-of-Experts Language Models*. ICLR, 2025.

### NTP、MTP 与 diffusion

16. Gloeckle, F. et al. *Better & Faster Large Language Models via Multi-token Prediction*. ICML, 2024.
17. Ahn, K. et al. *Efficient Joint Prediction of Multiple Future Tokens*. 2025.
18. Ho, J. et al. *Denoising Diffusion Probabilistic Models*. NeurIPS, 2020.
19. Li, X. et al. *Diffusion-LM Improves Controllable Text Generation*. NeurIPS, 2022.

### 工作负载与 benchmark

20. Ding, Y. et al. *CrossCodeEval: A Diverse and Multilingual Benchmark for Cross-File Code Completion*. NeurIPS Datasets and Benchmarks, 2023.
21. Liu, T. et al. *RepoBench: Benchmarking Repository-Level Code Auto-Completion Systems*. ICLR, 2024.
22. Hsieh, C.-P. et al. *RULER: What’s the Real Context Size of Your Long-Context Language Models?* COLM, 2024.
23. Kuratov, Y. et al. *BABILong: Testing the Limits of LLMs with Long Context Reasoning-in-a-Haystack*. 2024.

