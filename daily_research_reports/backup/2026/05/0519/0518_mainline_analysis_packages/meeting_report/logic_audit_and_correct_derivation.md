# 0518 Logic Audit and Correct Derivation

## 一句话结论

0518 汇报的最大逻辑漏洞是把三件事串得太快：`feature 可分`、`router clean`、`bucket 可检索 attention KV`；正确链条必须把 gating 分类、attention 检索需求、系统 latency 三个目标拆开。

## Mainline update

Yes. 这是一次主线修正：从“找一种 gating 让语义 feature 分到专家”改为“验证什么样的 routing partition 与 attention high-mass KV 兼容”。

## Result / Interpretation / Claim / Speculation

**Result:** 之前汇报已有两个负结果：natural router 不自动 one-feature-one-expert；即使用监督 feature routing 达到 clean assignment，router bucket 对 high-mass KV 的召回仍然弱于 local baseline。

**Interpretation:** clean feature routing 不是 reverse index 的充分条件。它也不说明 feature routing 没价值，只说明当前 synthetic all-trigram 的 attention 需求不主要按人工 feature label 聚集。

**Claim:** 当前最安全 claim 是：`feature separability != router specialization`，并且 `router specialization != KV-index usefulness`。

**Speculation:** 如果 gate 使用 attention output，可能更接近 attention 所需的信息；但这只解决 routed representation mismatch，不自动解决 query-key bucket compatibility，也可能引入同层 attention 的 circular dependency。

## 之前汇报中不可靠 / 攻击点

### 1. 把 recall / attention-output error 当成导师要看的最终指标

组会中导师明确追问的是：如果用 reverse index 推理，输入 A/B 是否还能预测 C，也就是 NTP/inference loss 是否受影响。attention output error 可以作为中间指标，但不能替代 NTP loss。

需要补齐：

```text
candidate recall / attention mass
-> attention output reconstruction
-> final logits / NTP loss
-> task readback accuracy
```

### 2. 假设 missed experts / missed KV 是正交噪声

这不可信。漏掉的 KV/value 可能与保留 KV 同向、反向或通过后续 MLP/LM head 非线性放大。不能用“召回不高但可能不影响预测”或“attention output 差很多所以一定坏”直接跳结论。

需要补齐：

```text
full_attn_logits - ri_logits
full_attn_loss - ri_loss
projection of missed values onto logit-relevant directions
```

### 3. 把 one-feature-one-expert 当作目标本身

组会中真正目标不是每个 expert 学一个 feature，而是大量 features 在有限 experts 中形成可控、低访问成本的索引映射。一个 expert 可以包含多个 features；popular features 也可能应该被特殊处理或常驻内存。

正确目标：

```text
给定 query 需要 K 个 latent features / KV groups，路由应返回尽量少且高召回的 candidate buckets。
```

### 4. 没区分“训练目标”和“推理替换”

如果 full attention 训练、reverse index 推理，得到差的 NTP loss 不能直接说明 reverse index 训练无效；它只能说明当前 checkpoint 对这种推理替换不鲁棒。

需要比较三种设置：

```text
A. full-attn train + full-attn infer: upper baseline
B. full-attn train + RI infer: compatibility test
C. RI train + RI infer: actual method test
```

### 5. Gate representation 和 expert representation 可能混了

新模型必须实现：gate 用 attention output，expert 输入不变。若代码把 expert 输入也换成 attention-only / stripped representation，实验结论失效。

## 正确逻辑推导过程

### Step 0: 最终目标

目标不是解释性 specialization；目标是降低长上下文推理中的 KV memory access / attention candidate scan，同时保持 NTP loss 或任务行为。

### Step 1: Reverse index 成立的必要条件

对每个 query token $t$，dense attention 有 high-mass key set $H_t$。某个 routing/index 方法 $g$ 成立，需要满足：

```text
j in H_t  =>  index(j) is in CandidateBuckets(g(query_t))
```

也就是说：**高 attention mass 的历史 token 必须被 query 的 bucket 召回。**

### Step 2: MoE gating 能提供 index 的必要条件

MoE route id 能做 index，需要满足至少一个 compatibility：

```text
same route(query) and route(key) implies high QK relevance
or
query route can predict key route set containing attention winners
```

这不是普通 NTP MoE objective 自动优化的目标。

### Step 3: Feature routing 只是一个候选充分性假设，不是定理

原假设是：

```text
same feature -> same expert -> same bucket -> high attention KV retrieved
```

0518 结果说明它至少不是充分条件。原因可能是 attention winner 由 locality、token identity、hidden similarity、value similarity 或 head-specific pattern 决定，而不是人工 feature identity。

### Step 4: 新 oracle-MoE 形式的合理性与边界

把 gate input 改为 attention output，是为了让 router 看见“已经聚合后的上下文证据”；expert input 不变，是为了不破坏原计算通道。它能测试：**attention-informed representation 是否比 raw hidden 更适合 routing**。

边界：如果同一层 gate 需要同一层 full attention output，它不能直接用于加速；只能作为分析或 two-pass upper bound。真正可用于 reverse index 的版本应该使用上一层 attention/MoE signal 或低成本 approximate signal。

### Step 5: 研究应拆成两个闭环

```text
闭环 A: routing classification
what representation is partitioned, what boundary, what objective pressure?

闭环 B: reverse-index usefulness
whether the partition retrieves attention-relevant KV under equal budget and improves/maintains NTP loss with lower memory cost?
```

## Weakest point

最弱点是 `feature` 仍可能是人类定义的人工标签，而 attention 需要的是 QK/value/logit-relevant 的动态关系。只有 source decomposition 能证明两者是否相关。

## 30s advisor version

我把 0518 的逻辑重新拆开了。之前我们跳得太快：feature 可分不等于 router 会按 feature 分，router 按 feature 分也不等于 KV index 有用。现在正确链条是：先看新 oracle-MoE 中 gate 用 attention output 后，router 的实际分区边界是什么；再看这个分区是否召回 dense attention 的 high-mass KV，并用 NTP loss 而不是只用 attention error 判断推理是否可用。inhibition 只能作为让 feature 更排他的诊断工具，不能直接证明 reverse index 成立。
