# Purpose Card: E4 Hierarchical Phrase Extension

## 1. Purpose / Main Reason

在 E0-E2 都清楚后，把 planted feature 从简单 n-gram 扩展到 hierarchical phrase，测试 attention / sequence modeling 是否变得必要。

## 2. Hypothesis To Decide

H4: 当 planted feature 变成层级短语时，模型需要同时学习低层 n-gram 和高层 phrase；简单 bigram 记忆不足以解释全部预测行为。

## 3. Experiment Question

模型能否同时学会低层 feature 和高层 phrase，并在不同 hierarchy level 上表现出不同误差和内部结构？

## 4. Data And Task Construction

Dataset: controlled phrases with nested subpatterns and Zipf-like counts.

Examples:

```text
经 常
打 球
A B 经 常 打 球
```

Task: next-token prediction.

## 5. Claim Boundary

这是第二阶段实验。不要在 one-feature / four-feature tests 变干净之前运行。
