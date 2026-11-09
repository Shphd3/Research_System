# Experiment Card: R3 Perfect Router Retrieval

## 1. Purpose / Main Reason

R1/R2 的 retrieval 失败可能有两种解释：

```text
1. natural router 没有学到 clean specialization；
2. 即使 clean specialization 成立，feature bucket 也不是 block2 attention 的好 KV index。
```

R3 用 router CE 构造近似完美 one-feature-one-expert 的 upper bound，直接测试第二个问题。

## 2. Mainline Position

该实验位于主线的中间判断点：

```text
router specialization -> KV retrieval usefulness
```

它不再问 natural MoE 会不会自动 specialize，而是问：

```text
specialization 如果已经成功，是否足以支撑 attention search？
```

## 3. Known Narrative / Premise

已有结果显示：

- dense block2 attention sparse，retrieval 问题有意义；
- natural flat/H-MoE/spectral router bucket 没有稳定优于 random/local；
- controlled synthetic 中 feature 可读出，但 natural router 不自动 clean specialize。

因此需要一个 upper-bound 检验来拆分 failure source。

## 4. Experiment Purpose

在 synthetic all-trigram 数据上，通过 `RouterFeatureCE` 强制：

```text
ABC -> expert 0
DEF -> expert 1
GHI -> expert 2
JKL -> expert 3
```

然后测试 feature-aligned router bucket 是否能以低 candidate ratio 召回 block2 full attention high-mass KV，并保持接近 full attention 的输出和 NTP CE。

## 5. Hypothesis And Sub-Hypotheses

H1: 如果 block2 high-mass KV 主要来自同 feature 历史 token，perfect router bucket 应明显优于 same-count random/local。

H2: 如果 perfect router 仍不优于 random/local，说明 feature label 不是 block2 attention 的主要 index variable。

H3: uniform vs feature-long-tail 对比可判断 feature frequency imbalance 是否破坏 index quality。

## 6. Experiment Object

Data:

```text
uniform feature distribution
feature-long-tail distribution
```

Model:

```text
Embedding + TransformerBlock1
-> 4-bucket MoE router with RouterFeatureCE
-> TransformerBlock2
-> LM head
```

## 7. Experiment Paradigm

先训练 NTP + router CE，再冻结 checkpoint 做 E2 retrieval-only analysis。

Inference 比较：

```text
router cumulative top-K buckets, K=1..4
router rank-K-only buckets
same-count random
same-count local
oracle dense top-M
full prefix sanity
```

## 8. Expected Outcomes And Hypothesis Update Logic

If router works:

```text
K=1/2 candidate ratio 低，Recall/MassRecall 高于 random/local，OutputRelativeL2 和 CE_delta 接近 full。
```

Update:

```text
specialization 足以支撑 synthetic KV index；之前失败主要是 natural router 没学到正确 partition。
```

If router fails:

```text
router recall 接近 random/local，或需要 K=4/full prefix 才有效。
```

Update:

```text
feature-aligned bucket 不是 block2 attention 的主要索引变量；下一步转向 attention source 变量诊断。
```

## 9. What This Can Prove

能证明或否定：

```text
在 synthetic feature 已近乎完美 specialize 的 upper-bound 条件下，
feature-aligned router bucket 是否可作为 block2 KV candidate index。
```

## 10. What This Cannot Prove

不能证明：

- natural router 会自己学到这个 index；
- 真实语言数据中 feature bucket 同样有效；
- 已经有推理加速。

## 11. Result

TBD.

## 12. Conclusion

TBD.

## 13. Next Step

TBD.

