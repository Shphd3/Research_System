# Experiment Card: E2-B3 Trainable Prototype Dynamics

## 1. Purpose / Main Reason

检验 prototype centers $c_e$ 在真实梯度反传下是否会自然演化成四个 feature 的中心，并自然把 ABC/DEF/GHI/JKL 分到不同 experts。

## 2. Mainline Position

本实验是对 E2-B / E2-B2 的可信度修正。旧 hard top-1 prototype routing 没有让 NTP loss 反传到 router centers，因此不能作为“自然训练动力学”的强证据。

## 3. Known Narrative / Premise

E2 已经显示：synthetic features 能被读回，但 natural router 没有 clean one-feature-one-expert。E2-D 显示：如果给 feature label supervision，同一模型可以 clean specialize。

## 4. Experiment Purpose

重新测试三个问题：

1. 只靠 NTP，trainable centers 是否自然分开并对齐 feature。
2. 加无监督 center separation loss 后，centers 是否会走向四个 feature centers。
3. 加指定 feature-to-expert CE 后，是否仍能作为 supervised upper bound 达到 clean routing。

## 5. Hypothesis And Sub-Hypotheses

H-B3: 若 prototype centers 真的能在 NTP 梯度下自然捕获 feature structure，那么不加 feature supervision 时也应出现较高 NMI / best-permutation accuracy。

Sub-hypotheses:

- H-B3a: gate-value top-1 会让 prototype centers 收到非零 NTP 梯度。
- H-B3b: natural NTP 可能移动 centers，但不一定形成 clean feature assignment。
- H-B3c: center separation 能分开 centers，但只有当 feature clusters 被推向不同 centers 时，才会提升 feature-expert alignment。
- H-B3d: supervised feature CE 是能力上界，不是现实可用方法。

## 6. Experiment Object

数据是 uniform all-trigram synthetic corpus：

| feature | relation |
|---|---|
| ABC | `[1,2] -> 22` |
| DEF | `[3,4] -> 23` |
| GHI | `[6,7] -> 20` |
| JKL | `[8,9] -> 21` |

模型是 1-layer causal Transformer + 4-expert prototype top-1 MoE FFN。

## 7. Experiment Paradigm

Router score:

$$
s_{t,e}
=
\tau
\frac{z_t^\top c_e}{\|z_t\|\|c_e\|}
$$

Gate-value top-1 output:

$$
y_t
=
p_{t,e^*}\mathrm{Expert}_{e^*}(h_t),
\quad
e^*=\arg\max_e p_{t,e}
$$

因此 NTP loss 可以反传到 $p_{t,e^*}$，再反传到 $c_e$。

## 8. Expected Outcomes And Hypothesis Update Logic

- 如果 natural NTP 达到高 NMI：支持 prototype center dynamics 能自然形成 feature specialization。
- 如果 center separation 提高 center geometry 但不提高 NMI：说明“center 彼此远离”不是 feature assignment。
- 如果 supervised CE 达到 NMI=1：说明模型与代码链路能做 clean assignment，失败来自目标压力不足。

## 9. What This Can Prove

它能判断当前 toy setting 中，trainable prototype centers 在真实反传下是否自然对齐人工 sequential features。

## 10. What This Cannot Prove

它不能证明真实语言 MoE 的 expert 语义分工，也不能证明所有无监督 router 几何正则无效。
