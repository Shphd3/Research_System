# Inhibition Logic Note

## 一句话结论

Inhibition 只能作为制造或测试排他性 routing 的诊断机制；它不能单独解决 specialization，更不能推出 reverse index 有用。

## 它想解决什么

组会中 inhibition 的直觉是：对一个 feature，如果 expert A 已经比其他 experts 更适合，就让 A 变得更好，让其他 experts 对这个 feature 变得更差，从而形成排他性。

## 它不能解决什么

### 1. 不能防止多个 features 塌到同一个 expert

即使每个 feature 都只送一个 expert，也可能所有 features 都送到同一个 expert。这正是组会中指出的问题。

### 2. 不能保证 bucket size / latency 最优

Zipf 下，高频 features 可能让某些 buckets 过大；均匀分配 features 也不一定最优，因为 popular features 可能应该常驻 memory。

### 3. 不能保证 attention winners 被召回

某 feature 的 expert 专一，不代表 dense attention 会主要看同 feature 的历史 KV。

### 4. 可能伤害 shared/common computation

如果 non-selected experts 被强行学坏，它们可能损坏本来共享的 common features，尤其是自然语言中的 common directions。

## 更安全的实现

不要直接最大化 non-selected CE。使用 margin ranking：

```text
L_rank = sum_{e != selected} max(0, margin - (CE_e - CE_selected))
```

含义：只要求 selected expert 比 others 好一个 margin，不要求 others 无限变坏。

## 必须搭配的控制项

```text
load balance
feature collision count
expert utility matrix
NTP loss/readback
reverse-index recall/mass/loss
```

## 报告说法

可以说：inhibition 是测试“能否人为制造排他 feature-to-expert mapping”的工具。

不能说：inhibition 从原理上保证有效 specialization 或 reverse index。
