# Prompt For Theory AI: E2 MoE Feature Separation

请你作为理论合作者，诊断一个 controlled synthetic MoE 实验中的反常现象。

## 背景

我们构造了一个 next-token prediction toy corpus。数据中有人为种下的 trigram context features，例如：

```text
ABC: [1,2] -> 22
DEF: [3,4] -> 23
GHI: [6,7] -> 20
JKL: [8,9] -> 21
```

这里的 `feature` / `motif` 指数据层面的重复上下文规则；`representation` 指模型在 prefix-end 位置形成的 hidden state；`expert specialization` 指 router 是否把不同 feature 的 hidden states 分给不同 experts。

## 我们原本想检验的假设

在重复出现的人工 sequential features 下，top-1 MoE 是否会仅通过 NTP loss 自然而然地形成：

```text
different feature representations -> different experts
```

也就是 clean feature-aligned expert partition。

## 已有实验现象

E2.0:

- MoE 能读回 planted trigram features；
- shuffled unigram control 不能读回这些 features；
- `P(expert | feature)` 明显高于 random routing baseline；
- dominant expert ablation 会损伤 feature readback；
- 但结果不是严格 one-feature-one-expert。

E2.1:

- token embedding 大体可分；
- router input hidden states 中 feature centroids 仍可分，Fisher ratio 很高；
- 但 router boundary direction 与 feature-difference direction alignment 很低；
- router entropy 接近 $\log(4)$，margin 不强；
- force-routing 显示多个 experts 都能支持同一 feature prediction。

E2.2:

- 降低 expert FFN 容量没有让 routing 更 feature-aligned；
- 增加到 16 个 trigram features 也没有强制 one-feature-one-expert；
- readback 仍然很高，但 dominant expert ablation effect 明显变弱。

## 核心反常现象

我们现在的问题不是“模型有没有学到 feature”。它学到了。

更准确的问题是：

```text
feature identity 在 router input hidden space 中似乎仍可分，
但 learned router 没有按这些 feature-separating directions 形成 clean expert specialization。
```

请重点分析：

1. 这是否真的是一个理论上值得追的现象？
2. 为什么 linear top-1 router 没有使用 feature-separating directions？
3. router 可能实际按什么变量划分？
   - prefix-end token shortcut?
   - hidden norm / activation scale?
   - target confidence / CE difficulty?
   - low-variance but loss-relevant directions?
   - early routing history / expert co-adaptation?
4. 如何区分：
   - representation 不可分；
   - representation 可分但 router 不使用；
   - expert 功能差异不足；
   - shared attention/residual/LM head 已经承担预测；
   - 当前 NTP loss 根本不要求 feature-aligned partition。
5. 下一轮最应该做哪些诊断实验？

## 请给出的输出

请不要泛泛解释 MoE。请围绕这个具体实验给出：

1. 最可能的 3 个机制解释，并说明各自可证伪预测；
2. 一个最小实验集合，用来判断 router 到底在按什么划分；
3. 哪个结果会支持“representation separability != router specialization”；
4. 哪个结果会说明我们只是实验设计有 shortcut；
5. 下一轮实验的优先级排序。

请保持 claim 边界：这个实验只涉及 controlled toy trigram NTP，不直接证明真实 LLM expert 语义分工。
