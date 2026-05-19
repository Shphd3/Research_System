# Purpose Cards - Reverse Index Mainline

## R0. Reverse Index Implementation Sanity

**Purpose:** 确认 reverse index 代码没有 off-by-one、layer mismatch、causal leak、candidate budget mismatch。

**Must check:**

```text
index key/value comes from the same layer as the attention being approximated
query position t cannot retrieve future positions
candidate count equals random/local baselines
current token excluded if dense attention excludes it
bucket ids are computed from the intended gate representation
same checkpoint, eval mode, no dropout
```

**Decision:** R0 未通过，所有 RI 结果只标记为 invalid / debugging。

---

## R1. Attention Source Decomposition

**Purpose:** 找出 dense layer2 attention high-mass KV 到底由什么变量解释。

**Hypothesis:** 当前 synthetic setting 中，attention winner 不主要由 feature label 决定。

**Setup:** 2-layer Transformer + MoE；layer2 dense attention as teacher。

**Metrics:** recall@budget, mass retained, output reconstruction, NTP loss delta。

**Decision:** 如果 local/token/value similarity 明显强于 feature/expert bucket，则 one-feature-one-expert 不是合适 index。

---

## R2. Candidate Generator Tournament

**Purpose:** 比较不同 candidate generators 谁更接近 dense attention。

**Generators:**

```text
local
random same-count
same feature oracle
same layer1 expert
same layer2 expert two-pass
top-k expert union
nearest hidden/key/value
hybrid: local + expert bucket
oracle attention top-M
```

**Decision:** 胜出的 generator 定义下一步 architecture direction。

---

## R3. Train/Inference Mismatch Test

**Purpose:** 判断 bad RI 是方法本身差，还是 full-attn training 后 RI inference 的 mismatch。

**Settings:**

```text
A full train + full infer
B full train + RI infer
C RI train + RI infer
D RI train + full infer
```

**Metrics:** NTP loss, readback accuracy, candidate count, training stability。

**Decision:** 如果 C 好而 B 差，说明需要 train-time RI；如果 C 也差，说明 candidate generator 不对。

---

## R4. Latency Proxy Under Zipf

**Purpose:** 把导师强调的最终目标从“index 数量”转成 memory latency proxy。

**Cost model:**

```text
ExpectedCost = gate_compute + bucket_lookup + KV_bytes_loaded + bucket_switch_penalty + exact_QK_rerank
```

**Zipf question:** popular features 是否应集中到常驻 buckets，而不是均匀分配？

**Decision:** 如果某种 bucket 分配召回好但 cost 高，不能作为系统 claim。
