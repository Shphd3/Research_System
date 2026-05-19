# Experiment Cards - Reverse Index Mainline

## Experiment Card R1: Dense Attention Source Decomposition

### 1. Hypothesis To Decide

Layer2 dense attention high-mass KV 不主要按 synthetic feature label 聚集。

### 2. Experiment Question

哪些变量最能召回 high-mass KV？

### 3. Setup

Model: 2-layer Transformer + MoE。

Attention target: full layer2 attention top/mass keys。

### 4. Baselines

local, random same-count, same token, same feature, layer1 expert, layer2 expert two-pass, nearest hidden/key/value, oracle。

### 5. Metrics

recall@B, mass@B, attention output L2/cos, logit KL, NTP loss delta。

### 6. Expected Outcomes

如果 feature bucket 弱而 hidden/key/value/local 强，则 feature specialization 不是当前 RI target。

### 7. What This Can Prove

能说明 RI 应该跟随 attention 的哪个 source signal。

### 8. What This Cannot Prove

不能证明最终 latency speedup。

---

## Experiment Card R2: Layer1 vs Layer2 Guide

### 1. Hypothesis To Decide

上一层 route 是否足够预测下一层 attention winners？

### 2. Experiment Question

用 layer1 MoE bucket 指导 layer2 RI，与用 layer2 two-pass bucket 相比差多少？

### 3. Setup

2-layer model；仅第二层 attention 替换为 RI。

### 4. Variants

```text
R2a: layer2 two-pass bucket guide
R2b: layer1 bucket guide
R2c: hybrid local + layer1 bucket
R2d: hybrid local + nearest hidden/key
```

### 5. Metrics

same as R1 plus candidate budget and runtime proxy。

### 6. Decision

two-pass 好、layer1 差：signal 不可提前获得，难以加速。
layer1 好：进入 RI training。

---

## Experiment Card R3: NTP Loss Influence Test

### 1. Hypothesis To Decide

RI candidate error 是否真正影响 final prediction？

### 2. Experiment Question

attention output error、attention mass recall、NTP loss delta 三者是否一致？

### 3. Setup

For each RI variant, compute:

```text
full_attn_output
ri_attn_output
full_logits
ri_logits
full_loss
ri_loss
```

### 4. Metrics

output error, logit delta, target probability delta, NTP loss delta, readback accuracy。

### 5. Decision

如果 output error 大但 loss 不变，不能说 RI 失败；如果 mass recall 高但 loss 变差，说明 missed values/logit directions 关键。

---

## Experiment Card R4: RI Train vs RI Inference

### 1. Hypothesis To Decide

full-attn-trained checkpoint 对 RI inference 不鲁棒，但 RI train 可能适应 candidate restriction。

### 2. Experiment Question

在 train-time 使用 RI 后，NTP 是否恢复？

### 3. Setup

Train with full vs RI; evaluate both full and RI.

### 4. Metrics

train loss, eval loss, readback, candidate recall, bucket load, stability。

### 5. Decision

RI train works => method may be viable with training alignment。
RI train fails => candidate generator / architecture signal wrong。
