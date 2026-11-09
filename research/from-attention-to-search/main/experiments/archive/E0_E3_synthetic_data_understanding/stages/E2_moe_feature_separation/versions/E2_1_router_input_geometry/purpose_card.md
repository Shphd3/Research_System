# Experiment Card: E2.1 Router Input Geometry Diagnostic

## 1. Purpose / Main Reason

E2.1 的目的，是解释 E2 中 MoE feature separation 为什么不是 clean one-feature-one-expert。

E2 已经显示：feature prefix 与 expert choice 有 alignment，dominant expert ablation 和 force-routing 都支持 expert 有实际贡献；但 expert 分工仍有 sharing、低频不稳定和 LB 后混合。E2.1 不先假设 feature family，而是拆开 representation、router boundary、expert competence 三个可能原因。

## 2. Mainline Position

E2.1 位于：

```text
E1 dense feature readback
-> E2 MoE feature-expert alignment
-> E2.1 为什么不是 clean one-feature-one-expert
```

它决定下一步应该继续做 expert direction causality，还是先改变 router / feature / capacity 设定。

## 3. Known Narrative / Premise

已知前提：

- synthetic feature 是三元上下文关系 `[A,B]->C`；
- E1 证明 dense model 学到 sequential context relation，而不是 unigram frequency；
- E2 证明 MoE 有 feature-expert alignment，但不是严格一一对应；
- router 的输入是 prefix-end hidden state，expert 选择来自线性 router logits。

## 4. Experiment Purpose

E2.1 要回答：

```text
不完全分离来自 router input geometry、router boundary choice，还是 expert capacity sharing？
```

## 5. Hypothesis And Sub-Hypotheses

H2.1a：Embedding 可分，但 router input 不可分。

H2.1b：Router input 可分，但 router 没有使用 feature-difference directions。

H2.1c：Expert 容量足够，多个 expert 都能预测同一 feature，因此没有 one-feature-one-expert 的优化压力。

## 6. Experiment Object

使用 E2 已训练 checkpoints：

```text
dataset = four_feature_all_trigram_v1000
features = ABC / DEF / GHI / JKL
variants = moe_top1_no_lb / moe_top1_lb
seeds = 20260513-20260517
```

观察位置是每个 feature 的 prefix-end token，即 `[A,B]->C` 中负责预测 `C` 的 `B` 位置。

## 7. Experiment Paradigm

E2.1 做六个诊断：

- embedding token cosine；
- router input centroid geometry；
- router input PCA by feature and expert；
- router boundary alignment；
- router margin / entropy；
- force-routing expert competence。

## 8. Expected Outcomes And Hypothesis Update Logic

如果 embedding 可分但 router input 混合，支持 H2.1a。

如果 router input 可分但 boundary alignment 低，支持 H2.1b。

如果多个 expert forced-routing 都能预测同一 feature，支持 H2.1c。

如果 dominant expert 是 best forced expert 且 advantage 大，说明 specialization 更强；如果不是，说明 router choice 与 expert competence 只有部分一致。

## 9. What This Can Prove

E2.1 可以判断 imperfect feature separation 更像来自 representation geometry、router boundary choice，还是 expert capacity sharing。

## 10. What This Cannot Prove

它不能证明真实 LLM expert 语义分工，也不能证明 spectral direction 等于 semantic direction。

## 11. Result

TBD.

## 12. Conclusion

TBD.

## 13. Next Step

TBD.
