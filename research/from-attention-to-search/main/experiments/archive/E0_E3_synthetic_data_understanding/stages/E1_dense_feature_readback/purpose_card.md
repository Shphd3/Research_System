# Purpose Card: E1 Dense Transformer Feature Readback

## 1. Purpose / Main Reason

在随机背景没有稳定语义的 synthetic 数据中，测试传统 dense Transformer 是否能从重复出现的上下文 feature 中学到稳定表征。

## 2. Known Narrative / Premise

如果数据中存在强 controlled pattern，一个小型 dense next-token model 应该能在 feature prefix 上预测正确 next token，并在随机背景上保持高熵。

## 3. Hypothesis To Decide

H1: 在传统 Transformer 中，FFN 更倾向于学习训练数据中高频出现的 feature；feature 频率越高，其在 FFN 中形成的表征越稳定、越可分，对模型输出的因果影响越大。

细化假设：

- H1a: 高频 feature 的 $P_\theta(\text{target}\mid\text{prefix})$ 高于低频 feature。
- H1b: 高频 feature 在 hidden state / FFN activation / logit-delta 中形成更稳定、更可分的方向。
- H1c: feature-context 的有效秩低于随机背景，主要可学习信号来自 planted repeated patterns。

## 4. Experiment Question

给定随机背景中重复出现的若干 feature，dense Transformer 能否在 NTP 任务中读出这些 feature，并把它们和随机背景区分开？

## 5. Data And Task Construction

Dataset: E0 通过后的 one-feature corpus 和 four-feature corpus。

Task: next-token prediction。

Diagnostic target: feature prefix 上的 target probability、CE、logit margin 和 representation separability。

## 6. What This Can Prove

它可以证明 controlled synthetic feature 对 dense NTP model 是可学习、可读出的。

## 7. What This Cannot Prove

它不能证明 MoE 会 specialization，也不能证明真实语言数据里有同样干净的 feature。

## 8. Next Step

如果 dense readback 通过，再进入 `E2_moe_feature_separation`。
