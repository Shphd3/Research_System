---
parent_node: problem.moe_expert_specialization
---

# Slot-Context Signal And Route-Utility Binding

## Reporting Summary

我们的父问题是，为什么线性分发在 ABC/DBE slots形式的合成数据实验中，没有形成slot-specialized的分发，怎么才能形成slot-specialized的分发。

我们研究的是：

> **MoE 的 router 为什么没有稳定按照 slot / feature 去分 expert？**

之前的 short-slot 实验中，我们看到：

- 一开始用 slot 信息初始化 router，确实能让 routing 更像 slot 分发；
- 但是训练之后，这种分发会下降；
- 最后 router 没有稳定按照 slot 分 expert。

所以这轮实验要回答一个更具体的问题：

> **之前在slot信息初始化后，训练后Router坍缩到根据 B 的common feature分发，是不是因为 slot 信息太短、太弱，到了 B token 位置以后，被 B token identity 或 common feature 压过去了？**

也就是说，我们想检查：

> **如果增强 B 前面的 slot context，让NTP目标更加依赖slot的类型，router 会不会更按照 slot 分发？**

### **任务构造**

#### 1 repeated slot context

第一种是重复的 slot cue：

```text
slot 1: A A A A A + B_i -> target
slot 2: C C C C C + B_i -> target
slot 3: G G G G G + B_i -> target
slot 4: K K K K K + B_i -> target
```

目的：

> **提供一个最强、最简单的 slot 信号，检查 router 是否能按 slot 分发。**

---

#### 2 distributed slot context

第二种是组合式 slot cue：

```text
slot 1: p0 q0 r0 t0 u0 + B_i -> target
slot 2: p0 q1 r1 t1 u1 + B_i -> target
slot 3: p1 q0 r1 t0 u1 + B_i -> target
slot 4: p1 q1 r0 t1 u0 + B_i -> target
```

这里单个 prefix token 不能唯一决定 slot，必须看整体组合。

目的：

> **避免模型只靠一个 prefix token 偷懒，测试它是否真的利用了更完整的 slot context。**

### **当前结果：**

结果可以总结成一句话：

> **slot context 变长以后，router 确实更倾向于按照 slot 分发；但是在 multi-B 情况下，这个分发还不稳定。**

新增的 2x2 top-1 mechanism audit 给出了一个更底层的解释：

> **top-1 routing 很依赖 step 0/10 的 router 几何。初始同 expert 会被 selected gate 和 expert starvation 放大；初始分开则可以稳定保持。**

更具体地说：

| 情况 | 结果 | 说明 |
|---|---|---|
| fixed-B + repeated slot | 基本能按 slot 分 | slot 信息本身能控制 router |
| fixed-B + distributed slot | 效果也较好 | 不只是单个 prefix token 有用 |
| multi-B + repeated slot | 有明显增强，但不完美 | slot 信息能抵抗一部分 B identity 干扰 |
| multi-B + distributed slot | 增强较弱 | 更复杂的 slot context 更难稳定使用 |
| oracle routing | 可以达到很好结果 | 说明任务本身不是无解 |

## Question

Broader question:

```text
Why does ordinary top-1 MoE gating fail to produce stable, interpretable feature-level expert specialization?
```

Sharper question:

```text
If the context before B determines B's next-token target, and the router is initialized from slot centroids, is slot visibility sufficient for learned top-1 routing to become slot-functional?
```

This anchor is a diagnostic child of the specialization mainline. It tests the weak-context explanation for prior routing failure. It does not test real-corpus specialization, Zipfian robustness, KV-cache reverse indexing, or a new MoE architecture.

## Physical Prior

In language, the same surface token can require different continuations in different contexts. Therefore the relevant feature is not token identity alone, but a context-dependent predictive state.

For a B token under slot $s$, the router input can be decomposed as:

$$
h_{i,s}^{(m)} = c_i + \beta_m u_s + \epsilon
$$

where $c_i$ is B-token identity, $u_s$ is slot/context information, and $\beta_m$ is the strength of that context at the B position.

A linear router can route by slot only if $u_s$ is visible in $h_{i,s}^{(m)}$ and useful for reducing NTP loss. But routing alignment alone is not specialization. A slot-specialized route must also select the expert that has causal utility for that slot.

## Mechanistic Motivation

Previous short-slot experiments showed:

```text
semantic / context initialization can create early routing alignment;
NTP training can wash that alignment out;
hidden states may still contain recoverable slot boundaries.
```

This leaves two rival explanations:

```text
A. slot signal at B was too weak, so B identity dominated routing;
B. slot is visible and useful, but top-1 NTP does not bind route assignment to expert utility.
```

The experiment separates them by first removing B-identity variation, then adding it back.

## Mathematical Modeling

Use four slots and four experts:

$$
s\in\{0,1,2,3\}, \qquad e\in\{0,1,2,3\}.
$$

Each sample has:

$$
x_{i,s}=(C_s^{(m)}, B_i), \qquad y_{i,s}=\pi_s(B_i).
$$

For the same $B_i$, the four slots produce distinct targets. Thus $B_i$ alone cannot determine the next token; slot context must disambiguate prediction.

The top-1 selected-gate router is:

$$
p=\operatorname{softmax}(Wh_{i,s}), \qquad r_{i,s}=\arg\max_e p_e.
$$

Slot-conditioned expert utility is measured by ablation:

$$
\Delta CE(s,e)=CE_s(\operatorname{ablate}(e))-CE_s(\operatorname{full}).
$$

The core judgment is not one metric but the bundle:

```text
route-slot NMI / route heatmap / forced expert loss / assignment-utility agreement
```

A result supports functional specialization only if final route assignment is slot-aligned and the assigned expert is also utility-best for that slot.

## Minimal Computational Test

Two modes:

```text
single_b_sanity: one shared B token; tests whether slot context can control routing when B identity is removed.
multi_b_primary: 256 B identities; tests whether slot routing survives B-identity variation.
```

Conditions:

```text
C0_short_slot_init: one-token slot cue baseline
A_long_repeated_slot_init: 5-token repeated slot cue
B_long_distributed_slot_init: 5-token distributed slot code
Oracle_slot_router / Oracle_b_position_only: slot-utility upper bound
A_long_random_init / B_long_random_init: natural-discovery controls
```

The repeated cue is the strongest context signal. The distributed code is cleaner because no single prefix token uniquely identifies the slot.

## Current Evidence

Supported weak result:

```text
Stronger context plus slot-centroid init can control routing in fixed-B diagnostics.
```

Evidence:

```text
single-B A_long_repeated: route NMI = 1.000, Assign-Utility = 1.000
single-B B_long_distributed: route NMI = 0.893, Assign-Utility = 1.000
bridge fixed-B long semantic: final NMI = 1.000 across seeds
```

Weakened strong result:

```text
slot visibility plus slot-centroid init is not sufficient for robust multi-B functional specialization.
```

Evidence:

```text
multi-B h_B -> slot probe = 1.000 and target accuracy = 1.000;
multi-B Oracle = 1.000, so slot-specific utility is available;
multi-B A_long_repeated improves but remains imperfect: route NMI 0.243 -> 0.591, Assign-Utility 0.565 -> 0.925;
multi-B B_long_distributed remains weak: route NMI 0.078 -> 0.313, Assign-Utility 0.326 -> 0.747.
```

Metric caveat:

```text
multi-B B_long_random_init reaches Assign-Utility = 0.998 while route NMI = 0.010.
```

Therefore Assign-Utility alone can be high under utility collapse. It must be read together with route-slot alignment and forced expert loss.

## Claim Boundary

What can be claimed:

```text
Context strength matters. Long slot context and semantic centroid initialization make B-position routing more slot-aligned, especially when B identity is fixed.
```

What cannot be claimed:

```text
ordinary top-1 NTP naturally forms robust slot-functional experts;
init-final diagonal improvement alone proves specialization;
route heatmap diagonalization alone proves expert utility;
this transfers to Zipfian or real-corpus data.
```

The current failure is more specific than weak representation:

```text
slot information is visible and useful, but learned routing does not reliably bind the slot axis to utility-best experts under many B identities.
```

Additional 2x2 mechanism audit:

```text
In a minimal 2-feature / 2-expert NTP-style top-1 proxy, failed seeds are
already collapsed at step 0, not after late optimization drift.

Success seeds start with A/B split across experts and keep that split through
training while forming counterfactual CE advantage.

Removing router bias improves random-router initial split from 3/10 to 6/10,
but does not guarantee route-pattern separation.
```

Evidence:

```text
Projects/from-attention-to-search/main/experiments/H0531_2x2_top1_router_lockin/summary.md
Projects/from-attention-to-search/main/experiments/H0531_2x2_top1_router_lockin/detailed.md
Projects/from-attention-to-search/main/experiments/H0531_2x2_top1_router_lockin/report_card_for_advisor.md
```

## Next Decision

Do not move directly to Zipfian stress tests. First test the smallest mechanism that addresses the observed gap:

```text
multi_b_primary + explicit route-function binding at the B / target position
```

The 2x2 top-1 audit sharpens the next mechanism choice:

```text
Before broadening conditions, test one anti-lock-in mechanism that changes
early router geometry or prevents starvation:
structured router initialization / exploration noise / load-balancing.
```

Primary check:

```text
Can a binding signal raise A_long and B_long assignment-utility while also improving route-slot NMI and forced-loss diagonal structure across seeds?
```

If this works, then Zipfian data becomes a robustness test. If it fails, the problem is likely not context strength but the top-1 routing dynamics or expert-utility formation mechanism.
