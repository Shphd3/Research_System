# 0522 Research Mainline Rewrite and Work Guidance

## Conclusion

0522 两段录音把当前主线重新收敛为一句话：

> 我们不是先研究遗忘、inference efficiency 或 KV cache 压缩本身，而是先研究 **representation / expert specialization** 是否能作为这些下游能力的上游原因；如果 specialization 成立，再问它能否提供可用的 reverse index。

当前最安全的科研判断是：

> vanilla no-load-balance top-1 MoE 在当前 A/B/AB synthetic setup 中没有自然形成稳定、干净的 feature / rule-level expert bucket；下一步不应继续泛泛地说“按 token ID 分发”，而应验证 router 是否被 hidden state 中的 **common / high-frequency / residual-preserved component** 主导。

下一步的主决策问题是：

> router 的 expert assignment 主要由哪个 factor 决定：token identity、position、left context、rule/function、target、frequency，还是混合的 predictive component？

---

## Self-Contained Context

### Research Object

研究对象是：长上下文 Transformer 中的 dynamic KV memory 是否可以被重写为一个 learned search / reverse index 问题。理想过程是：

```text
query hidden state -> learned index / specialization signal -> candidate KV tokens -> exact sparse attention
```

### Current Evidence Before 0522

已有 H0521 AB feature specialization 实验显示：MoE 可以学会 A-only、B-only、AB-composite，但 router 没把 A/B/AB 分成干净 expert bucket；AB-dominant expert 同时接收 A-only、B-only、background，而且 expert ablation delta 很小。因此，当前证据只支持 mixed router assignment，不足以证明强 shared functional expert。

H0521b seq32 source-token diagnostic 进一步显示：模型能学会 seq_len=32 的连续 AB motif task，但 source-token gating 没有形成干净 A/B/background bucket；跨 seed 稳定交集只有 A token 在 A-only 和 AB 中 dominant expert 一致，B token 不稳定，identity/role NMI 都低。

这两组结果共同说明：

```text
representation 里可能有 feature 信息；
但 router projection / top-1 boundary 没有自然按 feature/rule 切分。
```

---

## Updated Mainline

### Old Rough Mainline

```text
MoE experts may specialize -> use expert IDs as KV reverse index -> reduce attention search cost.
```

### New 0522 Mainline

```text
Attention 是 selective operator
  -> 长上下文需要 learned reverse index
  -> reverse index 需要某种 representation / expert specialization
  -> specialization 不是天然存在，需要先被定义、测量、诱导
  -> vanilla MoE 失败时，不应只说“按 token ID”，而要找 dominant factor
  -> 如果能诱导 slot / feature / frequency-balanced specialization，再测它是否提升 KV retrieval
```

### Key Causal Graph

```text
Architecture / objective / data distribution
        ↓
Representation geometry
        ↓
Specialization quality
        ↓
Reverse-index quality
        ↓
KV cache compression / sparse attention accuracy / inference efficiency
```

辅助下游：

```text
Specialization quality -> less interference -> less forgetting
Specialization quality -> semantic/relation-aligned buckets -> better prediction/retrieval
```

---

## Hypothesis -> Mathematical Modeling -> Experiment Design -> Conclusion/Update

### Hypothesis H1: Specialization is the upstream cause

导师的核心假设是：如果表示空间或 expert 分发形成高质量 specialization，那么 forgetting、prediction、KV reverse index 等下游任务会更容易。

**Mathematical Modeling**

设 hidden state 可分解为：

$$
h = h_{id} + h_{pos} + h_{ctx} + h_{rule} + h_{freq} + h_{target} + \epsilon
$$

router logit 为：

$$
s_e(h) = w_e^\top h
$$

一个好的 specialization 不是让 expert 任意均衡使用，而是让 route assignment 对齐目标 factor：

$$
e^*(h) \approx f(z_{rule}) \quad \text{or} \quad f(z_{slot})
$$

而 vanilla MoE 可能实际学到：

$$
e^*(h) \approx f(h_{id} + h_{freq})
$$

也就是被 common / high-frequency component 主导。

**Conclusion/Update**

当前证据削弱了“vanilla top-1 MoE 自然形成 feature-level specialization”的假设，但没有否定“可通过 oracle / attention relation / hierarchical frequency grouping 诱导 specialization”。

---

### Hypothesis H2: “按 token ID 分发”不是最终解释

0522 会议中导师明确修正了“按 token ID”的说法：这句话不一定错，但没有算法能力。更好的解释是：router 被 hidden state 中最 common / high-frequency / residual-preserved component 主导。

**Mathematical Modeling**

如果 residual 保留 early embedding component：

$$
h_l = h_0 + \Delta h_1 + \cdots + \Delta h_l
$$

而 $h_0$ 或某个 high-frequency component 范数/方差较大，则：

$$
w_e^\top h_l \approx w_e^\top h_0
$$

即使 $h_l$ 中包含 rule 信息，router 仍可能主要按 early/common component 划分。

**Experiment Implication**

下一步不能只画 routing heatmap，要做 factor attribution：

```text
expert_id / router_logit ~ identity / position / left_context / rule / target / frequency
```

---

### Hypothesis H3: Frequency dominance is a bottleneck for reverse index

高频 feature 和低频 feature 放在同一 expert 中时，训练和检索都会被高频 component dominate；因此需要 frequency stratification 或 normalization。

**Mathematical Modeling**

若 feature $i$ 出现频率为 $p_i$，则训练期梯度期望近似受 $p_i$ 加权：

$$
\mathbb{E}[g] = \sum_i p_i g_i
$$

高频 feature 的 $p_i$ 大，会主导 expert 更新。低频 feature 即使语义重要，也可能被覆盖。

**Experiment Implication**

后续 synthetic 不应只用均匀 feature；必须构造 nonuniform / Zipf-like frequency distribution，并测试：

```text
frequency-balanced grouping 是否提升 low-frequency slot recall 和 reverse-index recall
```

---

### Hypothesis H4: Attention relation can supervise specialization

一名同学报告的结构利用 attention score 约束 expert 分发：同 expert token 之间 attention score 高，不同 expert token 之间 attention score 低；据报告，在 synthetic 数据上同 expert relation 与真实 relation 匹配约 80%，分发与 ground-truth slot 匹配约 95%。

**Interpretation**

这说明 attention relation 可能是比 vanilla router 更接近 rule/slot 的 signal。

**Claim Boundary**

这还不能说明真实语言中可用，也不能说明工程成本可接受；还必须与 oracle MoE、post-attention V routing、hierarchical frequency grouping 比较。

---

## Current Claim Boundary

### Supported / Weakly Supported

- 当前 vanilla no-load-balance top-1 MoE 没有在 A/B/AB synthetic 中形成稳定、干净的 feature/rule bucket。
- hidden state 里保留 class 信息，但 router boundary 未按 class 切分。
- source-token expert bucket 目前不能直接作为 feature-level reverse index。
- “token ID routing”应被重写为“common / high-frequency / residual-preserved component dominates routing”的待验证假设。

### Not Yet Claimable

- 不能说 MoE 一般无用。
- 不能说 router 一定按 token ID 分发。
- 不能说 attention-score constrained routing 在真实数据中有效。
- 不能说 reverse index 路线失败。
- 不能从 routing heatmap 单独推出 KV retrieval 质量。
- 不能把 toy synthetic 的 feature 直接等价为真实语言语义。

---

## Next Decision

下一步最重要的决策问题：

> 我们应该继续把 expert ID 当作 reverse-index candidate，还是需要先引入 attention-relation / oracle / hierarchical frequency grouping 来诱导 specialization？

要回答它，必须先做一个 factor audit：

> 当前 router assignment 到底由哪个 factor 主导？

---

## Work Guidance Narrative

当你觉得一个实验结果“不够 impact”时，不要立刻否定它。按下面四步走：

1. **问它削弱了什么。** 这次实验削弱的是“vanilla top-1 MoE 会自然形成干净 feature bucket”。
2. **问它没有区分什么。** 当前没有区分 identity、frequency、position、rule、target、residual component。
3. **把下一步压缩成两个解释的竞争。** 例如：router 是被 rule component 主导，还是被 frequency/common component 主导？
4. **设计一个让解释不可逃避的指标。** 例如 router-logit factor $R^2$、component removal route flip rate、frequency-stratified slot recall。

你现在的成长点不是“多跑实验”，而是每次实验前写清楚：

```text
如果 H_id 对，应看到什么？
如果 H_rule 对，应看到什么？
如果 H_freq 对，应看到什么？
如果 H_mixed 对，应看到什么？
```

---

## Files To Update

建议将本轮主线写入：

```text
Projects/from-attention-to-search/XingyuD/main/experiments/E0522_router_factor_audit/purpose_card.md
Projects/from-attention-to-search/XingyuD/main/experiments/E0522_router_factor_audit/execution_plan.md
Projects/from-attention-to-search/XingyuD/main/experiments/E0522_research_graph/summary.md
daily_research_reports/0522/daily_card.md
```
