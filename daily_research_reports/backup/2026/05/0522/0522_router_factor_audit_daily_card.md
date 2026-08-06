# Daily Card - 0522

## 1. Today's Purpose

完成 H0522 `seq_len=32` SVD feature-mixing diagnostic 和 router factor audit，判断 ordinary top-1 MoE 的 expert bucket 是否能解释为 clean feature/function bucket。

## 2. Mainline Anchor

主线问题：

```text
attention 是高度 selective 的算子；当前 token 真正需要的信息通常只是
历史 KV memory 中很小的一部分。核心问题是：长上下文 attention 的
KV memory 有没有一种可学习的 index structure？
```

基于 MoE 的当前验证链条分成两问：

```text
1. expert 能不能实现 specialization？
2. specialization 能不能帮助 Reverse Index / inverted index / KV retrieval？
```

今天的实验主要回答第一问。即使 specialization 不完美，只要它比随机或既有 baseline 更好，第二问仍然可以独立测试其 retrieval utility。

## 3. Task Conclusions

### Task 1

Did:

在已训练 H0521b `seq_len=32` MoE 上完成 SVD feature-mixing analysis，本地两卡使用 `cuda:0, cuda:1`，4 个 seed，`n_eval_per_class=4096`。

Conclusion:

AB-composite 有 dominant expert，但该 expert 对 A/B/AB interaction 都高投影，且不优于 random/global baseline；mask damage 也不跨 seed 稳定指向 AB-composite。因此 AB-dominant expert 不是稳定 clean AB specialist。

### Task 2

Did:

完成 ACP 四卡 job `pt-xceqs84c`，跑完 Stage 1-5，四个 seed 全部完成。

Conclusion:

Stage 1/2 显示 source-position 和 token-id 对 router 的解释力强于 rule/class。

### Task 3

Did:

完成 factor-disentangled seq_len=32 synthetic task。

Conclusion:

模型 accuracy 为 1.0，但 rule_label 没有稳定胜过 identity；target/second-token shortcut 更强。

## 4. Mainline Update

H0522 更新主线：

```text
ordinary top-1 expert id 目前不能作为 clean rule/function Reverse Index。
```

更精确地说，SVD 诊断显示 AB-dominant expert 不是稳定 clean AB specialist；factor audit 进一步支持 position/token-id/target-shortcut modulated mixed routing。

## 5. What I Cannot Claim Yet

不能说 MoE routing 一般无效，也不能说真实语言模型中一定同样失败。

SVD 只分析 prediction-position expert，不能直接证明 source-token KV retrieval 失败。Stage 5 仍有 target/second-token shortcut，所以下一步必须做更严格的 anti-shortcut 构造。

## 6. Next Decision

设计下一版 anti-shortcut synthetic：

```text
balance identity x position x target;
test rule/function -> expert_id after shortcuts are controlled.
```

## 7. 30s Explanation

我们今天先看了已训练 seq_len=32 MoE 的 AB expert：AB 样本确实集中到某个 expert，但这个 expert 的子空间不是 AB-only，而且 mask 后也不稳定只伤害 AB。随后 factor audit 显示，旧模型里位置和具体 token 更能解释 expert id；新解耦任务里模型能做对任务，但 router 更贴近 target/second-token shortcut，而不是稳定 rule/function。所以现在不能把 ordinary top-1 expert id 当作干净的检索索引，下一步要做去 shortcut 的 synthetic。

## 8. Recording / Class Notes

无。

## 9. Small Thought Parking Lot

暂无。
