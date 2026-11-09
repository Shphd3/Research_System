# Experiment Card: R4 Attention-Output Router Retrieval

## 1. Purpose / Main Reason

检验 R3 的失败是否来自 router 输入表示不合适：如果 router 直接读取上一层 attention output，不含 residual，是否更容易把 block2 会关注的 KV 组织成可检索 index。

## 2. Mainline Position

R3 已经说明：即使 one-feature-one-expert 几乎完美，feature bucket 也不必然是好的 block2 KV index。R4 进一步问：若路由输入换成更接近 attention 汇聚后的信号，reverse index 是否改善。

## 3. Known Narrative / Premise

当前主线不是证明 MoE 训练 loss 更低，而是判断 router bucket 是否能作为 block2 dense attention 的 KV candidate index。候选内仍用 exact QK attention 重算输出。

## 4. Experiment Purpose

比较两种 attention-output routing：

- `attn_route_ntp_only`: 只用 NTP CE 训练。
- `attn_route_router_ce`: NTP CE + RouterFeatureCE 对齐约束。

## 5. Hypothesis And Sub-Hypotheses

H1: block1 attention output 比 residual hidden 更贴近 block2 attention 的检索变量。

H1a: 不加 RouterFeatureCE 时，router bucket 仍可能自然带有 retrieval signal。

H1b: 加 RouterFeatureCE 时，若 retrieval 仍不改善，说明 feature-aligned reverse index 不是 block2 attention 的主要检索结构。

H1c: 若 NTP CE 或 sparse CE 明显变好，说明 reverse index 可能对推理质量有贡献；否则只能说 specialization 存在，不能说 index 有用。

## 6. Experiment Object

E-series all-trigram 数据：uniform feature 分布和 feature-long-tail 分布各跑一个支线。

## 7. Experiment Paradigm

统一模型骨架：

```text
TokenEmbedding -> TransformerBlock1 -> Router/MoE -> TransformerBlock2 -> LMHead
```

唯一结构变化：

```text
router_input = block1.attn_out
```

这里 `attn_out` 是 self-attention 输出投影后的张量，不包含 residual，也不是 block1 FFN 后 hidden。

## 8. Expected Outcomes And Hypothesis Update Logic

如果 router top-K 在 recall、attention mass、output L2、CE delta 上优于 random/local，则支持 attention-output routing 有 reverse-index 信号。

如果 RouterFeatureCE 让 feature alignment 变强但 retrieval 仍差，则强化 R3 结论：feature specialization 不等于 KV retrieval index。

如果 NTP-only 好于 RouterFeatureCE，则说明强行 feature 对齐可能损伤真正的 attention 检索变量。

## 9. What This Can Prove

能判断 attention-output routing 在当前 E-series toy NTP 中是否比 R3 的 residual-hidden routing 更适合作为 reverse index。

## 10. What This Cannot Prove

不能证明真实长上下文 DCLM 可加速，也不能证明所有 MoE/router 都不适合作为 KV index。

## 11. Result

TBD.

## 12. Conclusion

TBD.

## 13. Next Step

TBD.

