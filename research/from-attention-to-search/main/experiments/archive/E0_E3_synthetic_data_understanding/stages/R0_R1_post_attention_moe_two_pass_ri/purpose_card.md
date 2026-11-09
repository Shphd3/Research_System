# Experiment Card: R0/R1 Post-Attention MoE Two-Pass RI

## 1. Purpose / Main Reason

检验一个更符合当前设想的 Reverse Index 诊断：先让模型完成 full attention，再用 post-attention router 的 expert bucket 作为第二次 attention 的候选 KV 集合，比较 restricted attention 与原 full attention 的 CE 差。

## 2. Mainline Position

这是 R0/R1 two-pass RI 的修正版。旧诊断是用前一层 router bucket 指导后一层 attention；本实验改成：

```text
tokens -> full attention -> post-attention MoE/router -> logits
```

然后在第二次前向中，用第一次得到的 expert bucket 限制同一层 attention 的候选 KV。

## 3. Known Narrative / Premise

E4 已经显示：router 可以被设计成不同程度的 feature-aligned 或 functionally useful expert assignment。但这还不能说明 router bucket 能作为 KV 候选生成器。RI 质量必须直接看 restricted attention 的 CE 代价。

## 4. Experiment Purpose

回答：post-attention expert bucket 是否比 random same-count KV 更适合做 restricted attention 的候选集合？

## 5. Hypothesis And Sub-Hypotheses

核心假设：如果 router bucket 捕获了对预测有用的上下文结构，那么用 same-bucket KV 重建 attention 时，CE 上升应显著小于 random same-count KV。

细化假设：

- H1：自然 post-attention router 可能不 clean feature-aligned，但仍可能提供有用 KV 候选。
- H2：oracle one-feature-one-expert router 如果真适合 RI，应比自然 router 更小 CE 损失。
- H3：clean inhibition 如果提升 expert functional separation，应改善 restricted attention 的 CE 保真。

## 6. Experiment Object

模型：

- `P0`: natural post-attention router + LB。
- `P1`: oracle feature-router auxiliary loss，强制 one-feature-one-expert。
- `P2`: clean inhibition + LB，不使用 feature label。

数据：

- `uniform`: 四个 trigram feature 等频。
- `zipf`: 四个 trigram feature 长尾频率。

## 7. Experiment Paradigm

每个模型先训练 NTP。评估时做两次前向：

1. full forward：记录 full attention 输出与每个位置的 expert bucket；
2. restricted forward：只允许 query attend 到同 bucket 的 KV，再计算 target CE。

对照包括 random same-count、local same-count、same-feature oracle 和 dense top-M oracle。

## 8. Expected Outcomes And Hypothesis Update Logic

- RI CE 低于 random：router bucket 有候选信号。
- RI CE 接近 local / oracle：router bucket 有强 RI 可用性。
- oracle feature router 比自然 router差：one-feature-one-expert 不等价于 RI 好候选。
- inhibition 改善 CE：功能性 expert separation 可能比 feature purity 更重要。

## 9. What This Can Prove

它可以证明在当前 toy setting 中，post-attention router bucket 是否提供了优于 random 的 KV 候选信号。

## 10. What This Cannot Prove

它不能证明真实长上下文任务可加速，也不能证明 one-feature-one-expert 是最佳 RI 结构。

## 11. Result

见 `summary.md`。

## 12. Conclusion

见 `summary.md`。

## 13. Next Step

如果继续 RI，应比较更多 candidate generator，而不是只追求更高 feature-expert NMI。
