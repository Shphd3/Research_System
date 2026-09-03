# Anchor A 中文拆分稿：真实表征初始化几何审计

Source: `daily_research_reports/0611/draft/moe_storyline_anchor_plan_0611.md`

Scope: This file extracts the Anchor A part. It asks whether the common-logit bias mechanism exists in real or semi-real hidden representation spaces. It does not propose a new initialization method.

## 0. researcher judgment record

父问题：稀疏 top-1 点积 MoE 为什么会早期路由坍缩。  
当前子问题：真实/半真实 hidden representation 中，随机 router 初始化是否也产生 common-induced imbalance。  
核心假设：隐藏状态可分解为共享成分和残差成分，随机 router 会把共享成分投影成专家特异偏置。  
最小测试：冻结 hidden states，随机 top-1 router，测 common margin、route concentration、expert-count scaling 和 common removal。  
当前边界：只审计初始化几何是否存在，不测试新方法，也不声称完整 LM MoE 训练收益。  
下一步决策：若支持，进入 Anchor B 的无标签 common-aware 初始化。

## 1. Purpose

Anchor A 回答：

```text
Does the common-logit bias mechanism exist at initialization in real or semi-real hidden representation spaces?
```

中文含义：在真实或半真实 hidden states 中，初始化时是否也能看到共享成分导致的专家特异打分偏置。

它是从 toy 机制走向导师所说“真实表征空间”的桥。

## 2. Why This Must Be Separate

Anchor A 和 Anchor B 不能合并。

原因很简单：如果真实表征里没有 common-induced route imbalance，那么初始化方法的动机就会弱很多。Anchor A 是 Anchor B 的有效性入口。

Anchor A 问的是问题是否存在；Anchor B 问的是能否利用这个几何设计方法。

## 3. Decision Question

```text
In frozen real/semi-real hidden states, does random dot-product top-1 routing produce expert-specific common-logit bias that causes initialization-time route concentration, and does this risk increase with expert count?
```

中文表述：

```text
在冻结的真实/半真实 hidden states 中，随机点积 top-1 路由是否会产生专家特异的 common-logit bias，
从而造成初始化时路由集中，并且这个风险是否随专家数增加而上升？
```

## 4. Problem Definition

合成证据不足以支撑论文的真实表征 claim。下一步必须判断 common-logit bias 是否也出现在冻结真实表征的随机 router 初始化中。

不在范围内：

- 不测试完整 LM MoE 训练。
- 不证明部署级初始化方法。
- 不声称 feature-level functional specialization 已经成立。

## 5. Physical Prior

物理先验指可被证伪的机制直觉。

P1：真实 hidden states 含有较大的共享成分。  
含义：token identity、position/template、layernorm mean directions、domain/task common directions 都可能形成样本间共享方向。  
可能错误的情况：这些共享方向很弱，或不会影响 router score。

P2：随机点积 router 会把共享方向变成专家特异 offset。  
含义：每个专家 row $w_e$ 对共享向量 $c$ 的投影不同，所以 $w_e^Tc$ 会成为与 feature 无关但专家相关的 bias。  
可能错误的情况：共享投影的 spread 小于 residual/feature margin，无法主导 top-1。

P3：专家数越多，极端 common projection winner 越容易出现。  
含义：专家集合越大，越可能存在某个专家在 $w_e^Tc$ 上异常大。  
可能错误的情况：归一化、router 结构或 hidden-state 分布抵消了这个极值效应。

## 6. Hypothesis

H1：冻结 hidden states 可近似分解为 $h_i=c+r_i$。  
支持条件：估计的 common subspace 能解释非判别共享变化，去除后残差仍保留 feature/residual structure。  
削弱条件：不存在稳定 common component，或 common removal 破坏所有有用结构。

H2：随机 router rows 会产生 $a_e=w_e^Tc$，并造成初始化 route concentration。  
支持条件：common margin 大，common argmax 能预测 route winner，max_load 高且 active experts 少。  
削弱条件：random routing 不集中，common margin 不大，或 residual/feature margin 主导 routing。

H3：专家数增加会放大 common winner dominance。  
支持条件：$E=4,8,16,32,64,128$ 中 max_load、common margin 或 dominant persistence 随 $E$ 变差。  
削弱条件：专家数增加不改变集中程度，或集中只由别的因素解释。

## 7. Minimal Mathematical Model

只使用一个核心模型：

$$
z_{i,e}=w_e^T h_i=w_e^T c+w_e^T r_i
$$

对象：

- $h_i$：第 $i$ 个 hidden state。
- $c$：共享成分或共享子空间中的代表方向。
- $r_i$：样本特异的残差/feature 成分。
- $w_e$：第 $e$ 个 expert 的 router row。
- $z_{i,e}$：样本 $i$ 分配给 expert $e$ 的 router score。

关键指标：

- common margin：由 $w_e^Tc$ 形成的 top expert gap。
- residual/feature margin：由 $w_e^Tr_i$ 形成的路由相关 gap。
- route concentration：max_load、routing entropy、active experts。

可证伪点：

```text
如果 common margin 不大，且 common removal 不改变 route concentration，
则 common-logit bias 不是当前真实表征初始化坍缩的主要解释。
```

## 8. Feature Definition in Real Representation Space

不要先讨论“语言模型的真实 feature 是什么”。本锚点采用可操作定义：

```text
feature 是 hidden states 中可控制或可测量、且应被 routing 保留的变化。
```

本周推荐两类：

1. 主要定义：有标签受控 prompts，例如 relation type、question type、answer type、domain、template family、syntactic role。
2. 次要定义：去除 common subspace 后的 residual cluster，用来检查 routing 是否保留残差结构。

主要指标：

- feature_NMI：路由分配和已知 feature label 的互信息归一化指标。
- per-feature route purity：每个 feature 是否集中到可解释的 expert 集合。
- cluster_NMI：路由分配和残差聚类身份的对齐程度。

边界：residual cluster 支持的是“残差结构对齐路由”，不是语义 feature specialization。

## 9. Minimal Tests

Experiment 1：冻结随机 router 审计。  
问题：真实/半真实 hidden states 的 random dot-product top-1 router 是否在 step 0 已经集中。  
输入：真实/半真实模型的 hidden states。  
router：随机点积 top-1，无训练。  
主要指标：common margin、residual margin、max_load、entropy、active experts。

Experiment 2：专家数 scaling。  
问题：common winner dominance 是否随专家数增加而恶化。  
条件：$E=4,8,16,32,64,128$。  
主要指标：common winner dominance、max_load、active experts、entropy。

Experiment 3：common projection control。  
问题：移除 common component 后 route concentration 是否下降。  
比较：random router on $h$ vs random router on $P_{\perp C}h$。  
主要指标：route concentration drop、common margin drop、feature/residual alignment change。

## 10. Falsifiable Outcomes

Supported if:

- random router on real hidden states shows large common margin and route concentration.
- common projection removal lowers route concentration.
- expert-count scaling increases common-winner dominance.

Weakened if:

- common margin is not larger than residual/feature margin.
- random routing is not concentrated.
- common projection removal does not change routing.

Insufficient evidence if:

- routing becomes more balanced but no feature/residual alignment metric exists.
- common removal changes utilization but destroys residual structure.
- only one representation source or one seed is checked.

## 11. Current Evidence

Observation：合成设置中，common-logit 是早期且可干预的机制信号。  
Interpretation：它可能解释 top-1 router 的 early collapse 和专家可访问性偏置。  
Boundary：真实表征证据尚未建立，不能直接从 synthetic 推到 real/semi-real hidden states。

## 12. Claim Boundary And Next Decision

Can claim, if supported:

```text
initialization-time common-logit geometry is visible in real/semi-real representation spaces.
```

Cannot claim:

- 已经有可部署初始化方法。
- 完整 LM MoE 训练稳定性已解决。
- 负载均衡不需要。
- functional expert specialization 已证明。

Next decision:

```text
If supported, proceed to Anchor B: label-free common-aware router initialization.
```

## 13. Agent Task Extraction

Agent Task A：Real Representation Geometry Audit。

Deliverables:

- hidden-state extraction pipeline.
- feature labels or residual clusters.
- random router step-0 audit.
- expert-count sweep.
- common projection ablation.

Metrics:

- common margin.
- residual/feature margin.
- max_load.
- entropy.
- active experts.
- feature_NMI / cluster_NMI.

Expert-count scaling 可以作为 Anchor A 的一个必要压力测试；如果时间不足，优先保留随机 router step-0 审计和 common projection control。
