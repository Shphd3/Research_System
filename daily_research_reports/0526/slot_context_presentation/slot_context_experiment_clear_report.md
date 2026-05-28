# Slot Context

## 1. 我们在研究什么问题

我们的父问题是，为什么线性分发在 ABC/DBE slots形式的合成数据实验中，没有形成slot-specialized的分发。

我们研究的是：

> **MoE 的 router 为什么没有稳定按照 slot / feature 去分 expert？**

之前的 short-slot 实验中，我们看到：

- 一开始用 slot 信息初始化 router，确实能让 routing 更像 slot 分发；
- 但是训练之后，这种分发会下降；
- 最后 router 没有稳定按照 slot 分 expert。

所以这轮实验要回答一个更具体的问题：

> **之前失败，是不是因为 slot 信息太短、太弱，到了 B token 位置以后，被 B token identity 或 common feature 压过去了？**

也就是说，我们想检查：

> **如果增强 B 前面的 slot context，router 会不会更愿意按照 slot 分发？**

---

## 2. 实验的核心想法

B token 的 hidden state 可以粗略理解成两部分：

```text
B hidden state = B token identity + slot/context feature
```

如果 slot 很短，那么 B hidden state 里可能主要是：

```text
B token identity
```

router 就容易按照 B identity 或 common feature 分发。

如果 slot context 变长，那么 B hidden state 里 slot feature 会更强：

```text
B hidden state = B token identity + 更强的 slot feature
```

这时 router 可能更容易按照 slot 分发。

---

## 3. 数据是怎么构造的

我们使用 4 个 slots 和 4 个 experts。

核心构造是：

```text
slot + B_i -> target
```

并且同一个 `B_i` 在不同 slot 下，对应不同 target：

```text
slot 1 + B_i -> Y_1
slot 2 + B_i -> Y_2
slot 3 + B_i -> Y_3
slot 4 + B_i -> Y_4
```

这样设计的目的：

> **让 B token identity 不能单独决定答案，模型必须利用 slot 信息。**

---

## 4. 为什么要分 fixed-B 和 multi-B

### 4.1 fixed-B：去掉 B identity 干扰

fixed-B 的数据中，只有一个 B token。

```text
slot 1 + B -> Y_1
slot 2 + B -> Y_2
slot 3 + B -> Y_3
slot 4 + B -> Y_4
```

它要回答的问题是：

> **如果没有很多不同 B token 的干扰，slot context 本身能不能控制 router？**

所以 fixed-B 是一个正控实验。

它不是最终主结论，只是用来证明：

> **slot 信息本身是可以被 router 用来分发的。**

---

### 4.2 multi-B：把 B identity 干扰加回来

multi-B 的数据中，有很多不同的 B token。

```text
slot 1 + B_i -> Y_{1,i}
slot 2 + B_i -> Y_{2,i}
slot 3 + B_i -> Y_{3,i}
slot 4 + B_i -> Y_{4,i}
```

其中 `B_i` 有很多个。

它要回答的问题是：

> **当很多 B identity 同时存在时，slot feature 能不能仍然控制 router？**

所以 multi-B 是主实验。

它测试的是：

> **slot feature 能不能压过 B identity / common feature 的干扰。**

---

## 5. 为什么要做两种 long-slot 构造

### 5.1 repeated slot context

第一种是重复的 slot cue：

```text
slot 1: A A A A A + B_i -> target
slot 2: C C C C C + B_i -> target
slot 3: G G G G G + B_i -> target
slot 4: K K K K K + B_i -> target
```

目的：

> **提供一个最强、最简单的 slot 信号，检查 router 是否能按 slot 分发。**

这是比较容易成功的版本。

---

### 5.2 distributed slot context

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

这是更难的版本。

---

## 6. 我们看什么指标

我们主要看三类结果。

### 6.1 router 有没有按 slot 分

看 route 和 slot 的对应关系。

如果 router 按 slot 分，routing 图应该接近：

```text
slot 1 -> expert 1
slot 2 -> expert 2
slot 3 -> expert 3
slot 4 -> expert 4
```

允许 expert 的编号发生交换。

---

### 6.2 expert 是否真的对对应 slot 有用

只看 router 分发不够。

还要看：

> **某个 expert 被分到某个 slot 后，它是否真的能降低这个 slot 的 loss。**

否则只是表面分发，不是真正的 specialization。

---

### 6.3 fixed-B 和 multi-B 的差异

我们特别比较：

```text
fixed-B 是否成功
multi-B 是否仍然成功
```

如果 fixed-B 成功但 multi-B 不稳定，说明：

> **slot 信息能控制 router，但 B identity / common feature 会干扰这种分发。**

---

## 7. 当前结果

结果可以总结成一句话：

> **slot context 变长以后，router 确实更倾向于按照 slot 分发；但是在 multi-B 情况下，这个分发还不稳定。**

更具体地说：

| 情况 | 结果 | 说明 |
|---|---|---|
| fixed-B + repeated slot | 基本能按 slot 分 | slot 信息本身能控制 router |
| fixed-B + distributed slot | 效果也较好 | 不只是单个 prefix token 有用 |
| multi-B + repeated slot | 有明显增强，但不完美 | slot 信息能抵抗一部分 B identity 干扰 |
| multi-B + distributed slot | 增强较弱 | 更复杂的 slot context 更难稳定使用 |
| oracle routing | 可以达到很好结果 | 说明任务本身不是无解 |

---

## 8. 这轮实验能说明什么

这轮实验支持一个较弱但重要的结论：

> **增强 slot 信息，会增强 router 按 slot 分发的倾向。**

也就是说，之前 short-slot 失败，确实可能部分来自：

```text
slot 信息太弱，被 B identity / common feature 压过去了
```

---

## 9. 这轮实验不能说明什么

这轮实验还不能说明：

> **MoE 已经形成了稳定的 expert specialization。**

原因是：

- fixed-B 成功只是正控；
- multi-B 才是主实验；
- multi-B 下 routing 有增强，但还不稳定；
- 只看分发图不够，还要看 expert 是否真的对对应 slot 降 loss。

所以更准确的结论是：

> **slot 强度有帮助，但只靠更长 slot context 和 slot 初始化，还不足以稳定形成 expert specialization。**

---

## 10. 现在的研究推进到了哪里

之前的问题是：

```text
为什么 router 不按 slot / feature 分 expert？
```

现在推进为：

```text
slot 信息不是完全无效；
增强 slot 信息确实能让 router 更按 slot 分；
但在 multi-B 中，B identity / common feature 仍然会干扰这种分发。
```

所以现在真正的问题变成：

> **如何让 router 不只是看到 slot，而是稳定地把 slot 分到真正有用的 expert 上？**

---

## 11. 下一步

下一步不应该马上跳到更复杂的数据分布。

更合理的是先在 multi-B 上继续问：

> **能不能让 router 的分发和 expert 的降 loss 作用绑定起来？**

也就是说，不只是让 router 按 slot 分，还要让：

```text
slot 1 分到的 expert，真的对 slot 1 有用；
slot 2 分到的 expert，真的对 slot 2 有用。
```

如果这一步成功，再去测试更真实、更复杂的数据分布，比如 Zipfian。

---

## 12. 30 秒汇报版本

我现在研究的是：MoE 的 router 为什么没有稳定按照 slot / feature 分 expert。之前 short-slot 实验里，slot 初始化一开始有效，但训练后会下降，所以我怀疑 slot 信息太弱，被 B identity 或 common feature 压过去了。

为此，我构造了一个 4-slot 实验：同一个 B 在不同 slot 下预测不同 target，让模型必须利用 slot 信息。同时我做 fixed-B 和 multi-B：fixed-B 去掉 B identity 干扰，multi-B 把 B identity 干扰加回来。

结果是：fixed-B 下 router 基本能按 slot 分；multi-B 下也有增强，但不稳定。所以我的结论是：增强 slot 信息确实能增强 router 按 slot 分发的趋势，但只靠这个还不足以形成稳定的 expert specialization。
