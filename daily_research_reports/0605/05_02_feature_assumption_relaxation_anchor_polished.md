---
parent_node: 05_01_geometric_inhibition_anchor
status: draft-for-review
---

# 05_02 Feature Assumption Relaxation

## 汇报前 Summary

**父问题**

ordinary top-1 MoE router 在 NTP 训练下为什么容易形成不稳定、退化或不可解释的 routing，而不是形成可解释的 feature-level expert specialization？

**当前子问题**

导师的 toy claim 已经视为 closed：

> 在 single-feature、uniform feature distribution、top-1 routing / inhibition 的极简 setting 下，同一 feature 可以因为 early lock-in 稳定进入同一 expert。

05_02 不再讨论这个 closed claim，而是逐个放松该 toy claim 依赖的三个假设：

1. 一个 token 只有一个 feature；
2. feature distribution 是 uniform；
3. 不分析多个 features 进入同一个 expert 后的关系。

**为什么要问这个问题**

05_01 / H0604a 说明 exact key `(slot, B_i)` 的 same-feature route consistency 很高，但 high consistency 可能由 collapse 造成。

05_01 / H0604b 说明在 non-collapsed S0/S1-cos 条件下，当前 route axis 更像 slot，而不是 `B_i`；但 H0604b 只是 existing-log audit，没有显式构造 compositional-feature data。

因此，05_02 的目的不是进入 utility binding，而是先回答：当 toy setting 的假设被逐个放松时，router 的 weak consistency 是否还成立，以及这种 consistency 是否有结构。

**决策问题**

当 single-feature / uniform / no-feature-collision 假设被放松时，router 产生的是：

1. stable non-collapsed feature routing；
2. collapse；
3. arbitrary early-locking bucket；
4. surface-axis routing；
5. 还是具有几何、预测目标或训练动态结构的 feature grouping？

**任务构造**

本 anchor 下有三个 minimal protocols：

- P1: Compositional Token Feature Routing
- P2: Zipfian Feature Frequency Routing
- P3: Same-Expert Feature Relation

当前优先执行 P1 和 P3。P2 先写 protocol，占位不立即跑。

**结论边界**

本 anchor 不 claim：

1. expert utility specialization 已形成；
2. center separation 是 causal mechanism；
3. route-feature NMI alone 等于 specialization；
4. Zipf / real-corpus robustness；
5. toy claim 的结论可以直接推广到真实 LM。

**下一步**

先做 P1：显式构造 compositional token，判断 router 是否跟随 target-relevant feature。  
再做 P3：在 feature label 相对明确后，判断进入同一 expert 的多个 features 是否有结构。

---

## 1. Problem Definition

### Broader question

ordinary top-1 MoE router 学到的 routing signal 到底是什么？

可能是：

- feature identity；
- target-relevant predictive factor；
- expert utility gap；
- surface token / position shortcut；
- early random lock-in；
- collapse。

### Sharper question

在导师 closed toy claim 的基础上，逐个放松其假设，判断 stable non-collapsed feature routing 是否仍成立。

### What we do not need to do now

- 不做 real corpus。
- 不做 full Zipf sweep。
- 不做 route-utility binding。
- 不提出新 router。
- 不用 NMI 或 consistency 直接 claim specialization。

### Operational definitions

**same-feature route consistency**

同一 feature label `f` 的多个 samples 是否集中 route 到同一 expert。

Primary metric:

```text
mean_f max_e P(route=e | feature=f)
```

**non-collapse**

router 是否使用多个 experts，而不是 all-to-one / near-all-to-one。

Primary metrics:

```text
load entropy norm
max load fraction
active experts
```

**target-relevant feature routing**

当 token 中有多个 candidate features 时，router 是否主要绑定决定 target 的 factor，而不是 nuisance factor。

**same-expert feature relation**

多个 features 进入同一 expert 后，它们是否共享几何、预测目标、训练动态，还是只是 arbitrary bucket。

---

## 2. Physical Priors

### Prior 1: initial lock-in can create weak consistency

top-1 routing 会强化 early nearest-expert assignment。  
因此 same-feature consistency 可以由 initial lock-in 产生。  
但这只是 weak consistency，不等于 specialization。

### Prior 2: compositional tokens expose feature-selection ambiguity

真实 token 往往不是 single-feature。一个 hidden state 可能同时包含：

- context / slot feature；
- identity feature；
- composite predictive state；
- nuisance variation。

如果 router 只是跟随 surface axis，那么 route consistency 不一定说明它学到了 target-relevant feature。

### Prior 3: F > E forces grouping

feature 数量通常大于 expert 数量。  
所以一个 expert 接收多个 features 是必然的。  
关键问题不是“是否 many-to-one”，而是 same-expert features 是否有结构关系。

### Prior 4: collapse is a false positive

如果所有 features 都进入同一个 expert，每个 feature 也满足“只进入一个 expert”。  
因此所有 consistency metric 都必须配合 load guard。

---

## 3. Mechanistic Motivation

导师 toy claim 的前提是：

```text
A1. 一个 token 只有一个 feature。
A2. feature distribution 是 uniform。
A3. 不分析多个 features 进入同一个 expert 后的关系。
```

05_02 的机制问题是：

```text
当 A1/A2/A3 被逐个放松时，
top-1 + early lock-in 还能产生 stable non-collapsed feature routing 吗？
```

如果不能，我们需要知道失败模式是：

- collapse；
- arbitrary hash-like routing；
- surface-axis shortcut；
- target-irrelevant grouping；
- tail feature starvation。

---

## 4. Mathematical Modeling

Let each sample contain candidate factors:

```text
x = [r_start, S1, S2, B_i, Y, r_end]
```

where:

```text
S1: slot-like feature group 1
S2: slot-like feature group 2
B_i: identity-like feature
Y: target
```

Feature label choices:

```text
F_S1 = S1
F_S2 = S2
F_B  = B_i
F_pair = (S1, S2)
F_comp = (S1, S2, B_i)
```

Routing distribution:

```text
P(e | f) = count(route=e and feature=f) / count(feature=f)
```

Consistency:

```text
Consistency(F) = mean_f max_e P(e | f)
```

Route-feature information:

```text
NMI(route; F)
```

Collapse guard:

```text
load entropy norm
max load fraction
active experts
```

Same-expert relation:

```text
For each expert e:
collect features routed to e;
compare their geometry / target / trajectory relation
against load-matched random grouping.
```

---

## 5. Computational Realization

### 5.1 Workflow Interface

Input:

controlled synthetic sequences with known factors:

```text
S1, S2, B_i, target rule, nuisance variants
```

Computation:

train or evaluate top-1 MoE router under minimal controlled conditions. Start from the cleanest 05_01 condition, e.g. S0/S1-cos or current best non-collapsed setup.

Output:

- route assignment logs;
- feature × expert heatmaps;
- load histograms;
- consistency and NMI metrics;
- same-expert relation statistics.

### 5.2 Minimal protocols

#### P1: Compositional Token Feature Routing

Relaxed assumption:

```text
A1. 一个 token 只有一个 feature。
```

Question:

```text
当 token 同时包含 S1、S2、B_i 时，router 是否跟随 target-relevant factor？
```

Minimal data:

```text
x = [r_start,
     S1_a1, S1_a2, S1_a3,
     S2_b1, S2_b2, S2_b3,
     B_i,
     Y,
     r_end]
```

Use three target rules:

```text
C1: Y = Y(S1)          # S1 relevant, S2 and B_i nuisance
C2: Y = Y(S2)          # S2 relevant, S1 and B_i nuisance
C3: Y = Y(S1, S2)      # compositional target
```

Optional later condition:

```text
C4: Y = Y(S1, S2, B_i) # exact composite identity target
```

Primary decision:

```text
Does the routing axis switch when the target-relevant factor changes?
```

#### P2: Zipfian Feature Frequency Routing

Relaxed assumption:

```text
A2. feature distribution 是 uniform。
```

Question:

```text
当 feature frequency 变成 Zipfian 时，head features 和 tail features 的 route consistency 是否分化？
```

Status:

```text
Protocol written, but experiment parked until P1/P3 clarify feature definition and same-expert relation.
```

#### P3: Same-Expert Feature Relation

Relaxed assumption:

```text
A3. 不分析多个 features 进入同一个 expert 后的关系。
```

Question:

```text
多个 features 进入同一 expert 后，是 arbitrary bucket，还是 shared geometry / target / trajectory group？
```

Minimal setup:

Use the feature axis fixed by P1 or 05_01 best condition. Construct `F > E` features under uniform distribution, then inspect the feature composition of each expert.

---

## 6. Minimal Falsifiable Tests

### P1 supported if

- C1 routing aligns with S1 under non-collapse；
- C2 routing aligns with S2 under non-collapse；
- C3 routing aligns with `(S1, S2)` or a clear target-relevant composite state；
- nuisance axes do not dominate when they are not target-relevant。

### P1 weakened if

- router always aligns with the same surface axis regardless of target rule；
- consistency is high only because of collapse；
- route axis is unrelated to target-relevant factor。

### P2 supported if

- head features keep high consistency；
- tail features show lower consistency / higher instability / starvation；
- load becomes more concentrated than uniform baseline。

### P2 weakened if

- head and tail features have similar consistency and load behavior after controlling for sample count；
- Zipfian frequency does not change routing structure relative to uniform baseline。

### P3 supported if

- same-expert features share geometry / target relation / trajectory more than load-matched random grouping；
- grouping is stable across seeds or training windows。

### P3 weakened if

- same-expert features are no more structured than random grouping；
- grouping changes strongly across seeds；
- apparent structure disappears after collapse guard。

---

## 7. Falsifiable Outcomes

### Outcome A: target-relevant routing

Router switches route axis when target rule changes.  
This supports feature-selection sensitivity, not yet utility specialization.

### Outcome B: surface-axis routing

Router keeps routing by S1 / S2 / B_i regardless of target rule.  
This weakens the claim that router learns target-relevant features.

### Outcome C: composite-key routing

Router only stabilizes on the full composite key.  
This suggests atomic predictive-state or hash-like routing, not clean slot-level specialization.

### Outcome D: collapse

Consistency high but load entropy low.  
This is degenerate route consistency.

### Outcome E: structured same-expert grouping

Multiple features entering one expert share geometry / target / trajectory.  
This supports moving toward capacity or utility analysis.

### Outcome F: arbitrary bucket

Same-expert grouping has no structure beyond random baseline.  
This suggests initial lock-in alone does not create meaningful specialization.

---

## 8. Current Evidence

From 05_01:

```text
H0604a:
Exact (slot, B_i) same-feature consistency is high,
but collapse can produce false positives.

H0604b:
After collapse filtering, S0/S1-cos is best described as slot-aligned routing.
B_i is weak.
slot+B_i remains the exact atomic key for same-feature consistency.

Boundary:
This was an existing-log audit, not a constructed compositional-feature experiment.
```

---

## 9. Claim Boundary and Next Decision

Can claim now:

```text
05_01 gives a bounded starting point:
best non-collapsed routing is slot-aligned,
and exact (slot,B_i) is stable as an atomic key.
```

Cannot claim now:

```text
1. Token compositionality has been tested.
2. Router follows target-relevant feature under compositional tokens.
3. Same-expert features have meaningful structure.
4. Expert utility specialization exists.
5. Zipfian robustness exists.
```

Immediate next decision:

```text
Run P1 first.
Then run P3 if P1 gives a usable feature axis.
Keep P2 parked until feature definition and grouping relation are clearer.
```
