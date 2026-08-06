# Meeting Brief: Real-Text Early Route Concentration and Common-Logit Amplification

## Question

真实 DCLM 文本中，随机初始化的 top-1 MoE router 为什么在训练前 10 步快速出现专家负载集中？

这里区分两个现象：

- **raw route concentration**：少数专家接收过多 token。
- **common-logit amplification**：不同专家在共同分量分数 `w_e^T c` 上的差距变大。

本轮不是继续证明 step 0 已经共同分量主导，而是问：step 10 的快速集中主要来自 router 权重更新、router 输入隐藏状态变化、专家参数更新，还是它们的相互作用？

## Conclusion

当前结论：真实文本上的早期集中不是单纯的 router 初始化问题，也不是 step 0 common 已经静态主导。更准确地说：

1. **step 0 已有负载偏置，但共同分量不是主要分数来源。**  
   step 0 `dominance_ratio=0.5251`，说明 residual 分数间隔大于 common 分数间隔；但 `raw_max_load=0.2781` 降到 `centered_max_load=0.1561`，说明 common 仍是负载偏置源。

2. **step 10 出现稳定的早期负载集中。**  
   3 seeds × 6 layers 平均：`raw_max_load` 从 `0.2781` 到 `0.8602`，`common_margin` 从 `0.1237` 到 `0.6236`。这说明真实问题从“初始化时是否已经 common 主导”转向“早期训练如何放大”。

3. **late-layer common-logit spike 不是 router 权重单独造成。**  
   第 5 层 replay 中，正常 `common_margin` 增量为 `1.2760`；gate-only 贡献 `-0.0137`，hidden-only 贡献 `0.4858`，剩余 interaction `0.8038`。

4. **raw 负载集中和 common-margin 放大必须分开解释。**  
   `freeze_gate_all` 仍保留几乎完整 raw load spike：`0.7314` vs normal `0.7334`；但 common-margin spike 只保留 `0.5354` vs normal `1.2760`。固定随机 gate + hidden drift 足以造成强 raw 负载集中；完整 common-margin spike 还需要 gate-hidden interaction。

5. **专家参数更新主要增强 common-margin 通道，不是 raw load 集中的必要条件。**  
   `freeze_experts_all` 把第 5 层 `common_margin_delta` 从 `1.2760` 降到 `0.1919`，但 `raw_max_load_delta` 仍为 `0.7183`。

6. **第 5 层 spike 被定位到进入第 5 层 router 之前的 hidden-producing path。**  
   `freeze_prefix_before_layer5` 把 `common_margin_delta` 降到 `0.0278`，把 `raw_max_load_delta` 降到 `0.0660`。因此第 5 层 step-10 spike 不是普通随机波动，而是由该层 router 输入之前的隐藏状态生成路径驱动。

## Key Evidence

### Evidence 1: 合成实验给出的边界

在 no-position moving-block 合成任务中，collapse 不是因为 feature 信息缺失，也不是 specialization 不可达。

```text
baseline accuracy = 1.000
baseline max_load = 0.969
baseline slot_NMI = 0.080
slot probe accuracy = 1.000
slot-init slot_NMI = 0.980
```

common-logit cancellation 能显著提高 specialization：

```text
baseline slot_NMI = 0.080
cancel_0_10 slot_NMI = 0.896
cancel_0_final slot_NMI = 0.963
accuracy = 1.000
```

解释：在合成任务里，common-logit 是可干预的 collapse source。但这不能直接推出真实文本 step 0 也由 common 主导。

### Evidence 2: 真实文本 step 0 削弱了“静态 common 主导”解释

```text
common_margin = 0.1237
residual_margin = 0.2364
dominance_ratio = 0.5251
raw_max_load = 0.2781
centered_max_load = 0.1561
delta_max_load = 0.1220
```

解释：真实文本中 step 0 的最大分数间隔主要来自 token residual，而不是 common。但 common 仍然会推动负载偏置。

### Evidence 3: 正常训练复现 step-10 早期集中

3 seeds × 6 layers 平均：

```text
step0  common_margin = 0.1237
step10 common_margin = 0.6236
step0  raw_max_load  = 0.2781
step10 raw_max_load  = 0.8602
step300 raw_max_load = 0.4805
```

解释：这是早期训练动力学，不是永久 expert death。step 300 有部分回落。

### Evidence 4: late layers 最强

第 5 层：

```text
step0  common_margin = 0.1482
step10 common_margin = 1.4242
step0  raw_max_load  = 0.2582
step10 raw_max_load  = 0.9916
step10 dominance_ratio = 47.2098
```

解释：spike 集中在后层，说明它更像 hidden-producing path 的层间反馈，而不是所有 gate 同步发生的简单权重漂移。

### Evidence 5: replay 排除 gate-only 解释

第 5 层 step0 -> step10：

```text
A_actual      = 1.2760
A_gate        = -0.0137
A_hidden      = 0.4858
A_interaction = 0.8038
```

解释：只更新 gate 权重不能解释 spike。hidden 变化和 gate-hidden interaction 是主要来源。

### Evidence 6: freeze split 区分 raw load 与 common-margin

第 5 层 step0 -> step10：

| condition | common_margin_delta | raw_max_load_delta | interpretation |
|---|---:|---:|---|
| normal | 1.2760 | 0.7334 | 正常 spike |
| freeze_gate_all | 0.5354 | 0.7314 | 固定 gate 仍有 raw 集中，但 common-margin 不完整 |
| freeze_experts_all | 0.1919 | 0.7183 | 专家更新增强 common-margin，但 raw 集中仍存在 |
| freeze_gate_and_experts | 0.2872 | 0.7114 | 非专家 hidden path 仍可造成 raw 集中 |
| freeze_prefix_before_layer5 | 0.0278 | 0.0660 | 第 5 层 spike 基本被压掉 |

解释：raw load 和 common-margin 是相关但不同的指标。只看一个会误判机制。

### Evidence 7: common direction 是 checkpoint 内稳定，不是训练全程固定

step 10，layers 3--5：

```text
pairwise_cos_mean >= 0.9999
primary_secondary_cos = 1.0000
common-winner agreement = 1.0000
```

但第 5 层 common direction 相对 step 0：

```text
step10 cos_to_step0  = 0.2574
step300 cos_to_step0 = 0.1417
```

解释：common direction 不是固定 audit batch 的偶然均值；它在同一 checkpoint 跨 batch 稳定。但它会随训练旋转，不能说是从 step 0 保持不变的静态方向。

## Detailed Setup

**Data**

```text
dataset = DCLM packed binary stream
sample_span = 257 tokens
input_tokens = 256
target_tokens = shifted 256
padding = none
train_sequences = 32768
audit_sequences = 8192
audit_tokens = 8192 x 256 = 2,097,152
```

**Model**

```text
model = random-initialized Qwen-style decoder-only MoE
pretrained = false
layers = 6
hidden_size = 512
attention_heads = 8
kv_heads = 4
experts = 8
expert_hidden_dim = 2048
vocab_size = 151936
initializer_range = 0.02
```

**Router and MoE**

```text
router = bias-free linear gate
router_input = exact hidden state entering the real gate
top_k = 1
shared_expert = false
load_balance_loss = 0.0
norm_topk_prob = false
oracle_gating = false
multihead_routing = false
```

**Runs**

```text
A05_04_03: real-text step-0 common-logit audit and early trajectory.
A06_02_01: 300-step trajectory + cross-checkpoint replay.
A06_02_02: freeze split + common-stability audit.
```

A06_02_01 的 ACP job 标记 failed，但失败发生在结果写完之后的 idle rank barrier timeout；结果表可用。A06_02_02 正常 succeeded。

## Current Interpretation

当前最稳妥解释：

```text
真实文本 step 0 已有负载偏置，但共同分量不是最大分数间隔来源。
训练早期隐藏状态快速变化，固定随机 top-1 gate 已能把这种变化转成 raw 负载集中。
完整 common-margin spike 需要 hidden drift、expert update 和 gate-hidden interaction。
第 5 层快速 spike 需要进入该层 router 前的 hidden-producing path。
```

因此，当前不能再说：

```text
router 权重更新单独造成 step-10 spike；
共同分量从 step 0 开始静态主导；
所有专家已经永久死亡；
合成实验机制可直接迁移到真实文本。
```

## Boundary

当前结论覆盖：

- DCLM packed text。
- 随机初始化小型 Qwen-style top-1 MoE。
- 6 layers，8 experts。
- 无 shared expert。
- 无 load-balance loss。
- exact gate input audit。
- 0--300 step 早期训练。
- 指标：common_margin、residual_margin、dominance_ratio、raw/centered max_load、replay terms、freeze deltas。

当前结论不覆盖：

- 预训练大模型。
- top-2 / soft routing。
- shared expert MoE。
- 长期最终 expert specialization。
- 可部署方法。
- expert-spectrum initialization 是否有效。
- raw load 残余机制到底来自 residual anisotropy、position structure，还是 forward expert-output feedback。

## Next Step

**Anchor2 下一步**

当前 common-margin claim 已经足够收窄：第 5 层 fast spike 需要 hidden-producing path 和 gate-hidden interaction。下一步如果继续 Anchor2，应只做一个残余机制拆分：

```text
residual / position / forward expert-output feedback split
```

目标：解释在 freeze_gate_all、freeze_experts_all、freeze_gate_and_experts 下仍存在的 raw route concentration。

**转向 Anchor1 的理由**

Anchor2 已说明真实问题不是简单 gate-only initialization failure。Anchor1 不应只问“初始化后负载是否均匀”，而应问：

```text
利用 expert 初始化谱结构的 router initialization，是否能改变 early hidden-gate interaction，并减少 common-margin / raw-load early spike？
```

**Anchor1 最小决策**

先不要直接声称方法有效。先做：

```text
1. expert spectrum 是否可稳定定义；
2. top spectrum 是否主要对齐 common；
3. common-filtered spectrum score 是否预测 forced-routing utility；
4. 该初始化是否减少 step0--10 common amplification 和 replay interaction。
```
