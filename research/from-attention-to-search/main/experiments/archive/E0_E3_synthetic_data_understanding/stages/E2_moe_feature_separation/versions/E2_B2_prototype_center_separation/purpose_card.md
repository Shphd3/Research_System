# Experiment Card: E2-B2 Prototype Center Separation

## 1. Purpose / Main Reason

E2-B2 要回答一个更接近实际可用的问题：

```text
如果不使用人工 feature label，
只让不同 expert 的 prototype center 彼此远离，
能否自然产生 one-feature-one-expert？
```

## 2. Mainline Position

E2-B 已经显示：prototype / center gating 能在 feature CE 监督下 clean specialize，但 no-aux prototype 不会自然 clean。E2-B2 补充测试一种更弱、更实际的无监督几何压力。

## 3. Known Narrative / Premise

已知：

- feature identity 可以从 hidden state 中读出；
- natural router 不会自动按 feature 分 expert；
- feature CE 可以直接把 feature-to-expert assignment 做 clean；
- 但真实场景里通常没有明确 feature label。

## 4. Experiment Purpose

检验 center separation 是否能避免 prototype collapse，并进一步推动 feature clusters 自动靠近不同 expert centers。

## 5. Hypothesis And Sub-Hypotheses

H-B2: 只让 prototype centers 彼此远离，可以提升 expert diversity，但不足以保证 clean feature assignment。

H-B2a: center separation loss 会让 prototype cosine 降低，避免 centers 聚在一起。

H-B2b: 如果 feature clusters 自然受到 NTP loss 驱动，centers 分开后可能提高 NMI / best-permutation accuracy。

H-B2c: 如果 NMI 仍不高，则说明 one-to-one 需要 feature-to-center assignment pressure，而不只是 center geometry pressure。

## 6. Experiment Object

对象为均匀 all-trigram synthetic data：

```text
ABC / DEF / GHI / JKL
feature count = 3900 / 3900 / 3900 / 3900
vocab_size = 1000
```

## 7. Experiment Paradigm

在 E2-B prototype router 上加入 center separation loss：

$$
L = L_{\text{NTP}} + \lambda L_{\text{center-sep}} + \alpha L_{\text{LB}}
$$

其中：

$$
L_{\text{center-sep}}
=
\frac{1}{E(E-1)}
\sum_{e\neq e'}
\max(0, \cos(c_e,c_{e'}) - m)^2
$$

本实验使用 $m=0$，即惩罚正余弦相似度，鼓励 centers 至少接近正交或互斥。

## 8. Expected Outcomes And Hypothesis Update Logic

如果 center separation 使 NMI 接近 1，说明无监督 prototype geometry pressure 可能足以诱导 one-to-one。

如果 prototype cosine 被压低但 NMI 仍不高，说明 centers 分开不等于 feature cluster 分配；缺的是 assignment-level pressure。

## 9. What This Can Prove

它可以检验“让 expert centers 远离”是否足以支持 synthetic feature one-to-one routing。

## 10. What This Cannot Prove

它不能证明真实语言 MoE 的 expert 语义分工；也不能证明所有无监督 router geometry 方法都无效。
