# Mainline A: Gating Classification / Routing Mechanism

## 一句话结论

现在不要再做“feature id 线性 probe”作为主证据；要直接重构 router 的实际分区：它在 attention-output 表征空间中把哪些样本放到同一 expert，边界是否对应 loss-relevant computation，而不是人工 feature label。

## Decision Question

在新 oracle-MoE 中：

```text
z_t = attention output -> gate
h_t = original expert input -> expert
```

router 到底在 $z_t$ 空间里学到了什么分类方法？它为什么不能 / 不需要把 ABC、DEF 等人工 features 分成 one-to-one experts？

## Mainline Anchor

已有结果说明：

```text
feature 可读回
supervised routing 可 clean
natural routing 不 clean
clean feature routing 也不保证 KV retrieval
```

所以新的 gating 分析不能只问“feature 能不能读出”，而要问：**router 实际使用的 partition 是否是 NTP 下的低损失分区，是否与 attention/retrieval 需求一致。**

## 新诊断方法：Router Partition Reverse Engineering

### 核心思路

把 router 当成一个把 attention-output 表征空间切成 cells 的函数。我们不先假设 cell = feature，而是反过来问：

```text
每个 expert cell 里面的样本有什么共同结构？
哪些最小输入改变会导致 route 翻转？
route boundary 附近的样本是否对应预测不确定、attention source 改变、还是人工 feature 改变？
```

### 需要导出的 trace

每个 routed position 导出：

```text
sequence_id, position
raw tokens around position
feature annotation if synthetic has it
z_t = attention output used by gate
h_t = expert input
router logits, margin, entropy, selected expert
top-k experts
full attention top keys and attention mass
expert outputs for all experts if forced route is available
NTP loss / target probability
```

## 诊断模块

### D1. Expert Cell Exemplar Analysis

Purpose: 看每个 expert cell 的“典型样本”是什么。

Method:

1. 对每个 expert，取 router margin 最大的 top examples。
2. 比较这些 examples 的 token pattern、attention top keys、loss difficulty、feature annotation。
3. 同时取 margin 最小的 boundary examples，观察边界附近到底混了什么。

Decision:

- 如果 top examples 共享同类 attention source，而不是共享人工 feature，则说明 router 更像 attention-source classifier。
- 如果 top examples 共享 surface token / target token，则说明 router 可能走 token shortcut。
- 如果 top examples 只共享 norm/confidence，则说明 router 是 difficulty/scale partition。

### D2. Counterfactual Route Flip Test

Purpose: 不用线性 probe，而用最小反事实修改判断 router 对什么敏感。

Method:

构造配对样本：

```text
same feature, different surface tokens
same surface tokens, different feature relation
same target, different feature
same prefix, changed future/noncausal token control
same feature, changed distractor/noise tokens
```

观察 route 是否翻转。

Decision:

- 改 feature 不翻转，改 surface token 翻转：router 不是 feature classifier。
- 改 attention source 翻转：router 可能是 attention-source classifier。
- 改 noise 翻转：router boundary 不稳定或表征混杂。

### D3. Boundary Walk / Interpolation Test

Purpose: 直接测分区边界，而不是用 classifier 间接解释。

Method:

取两个样本 $i,j$：

```text
z(alpha) = (1-alpha) z_i + alpha z_j
```

扫 alpha，记录 expert switch point。选择四类 pair：

```text
same feature different expert
different feature same expert
different feature different expert
same expert but different attention source
```

Decision:

- 如果 switch 发生在 attention-source 变化方向，而不是 feature delta 方向，则 router boundary 与 attention 聚合结构更相关。
- 如果很多不同 feature 之间没有 switch，说明 one-feature-one-expert 不是当前 learned partition。

### D4. Common Component Removal / Residual Specificity Test

Purpose: 验证 common component 是否支配 routing。

Method:

对 $z_t$ 做几种去除：

```text
remove top PCs / remove global mean
remove token-identity centroid
remove local-position component
keep only residual after subtracting expert-cell centroid
```

然后重算 router logits / expert id。

Decision:

- 去掉 common PCs 后 routing 大变：router 主要吃 common geometry。
- 去掉 token centroid 后 routing 大变：token identity shortcut。
- 保留 residual 后 feature alignment 上升：feature 信息存在但被 common component 淹没。

### D5. Expert Utility Landscape

Purpose: 判断 router 选择是否有功能必要性。

Method:

对每个样本强制走每个 expert：

```text
U(t,e) = - CE(target_t | force expert e)
```

比较：

```text
selected expert utility
best expert utility
feature-oracle expert utility
random expert utility
```

Decision:

- selected 接近 best：router 是 utility-driven。
- 多个 expert utility 接近：expert 冗余，没必要 clean。
- feature-oracle 差于 selected：人工 feature partition 对 NTP 不是好分区。
- selected 不接近 best：router training / load balance / straight-through 可能有问题。

## Hypotheses

### H-G1: Router 是 attention-source classifier

router 按 $z_t$ 中“上一层 attention 聚合了什么”分，而不是按人工 feature 分。

Prediction: expert cells 内的 top attention keys / source pattern 更一致。

### H-G2: Router 是 common-geometry classifier

router 主要按高频/common directions、norm、position、token identity 分。

Prediction: 去掉 top common components 后 routing 大幅改变；feature residual alignment 上升。

### H-G3: Router 是 low-loss utility partition

router 学到的是多个 experts 都可完成任务时的任意低损失分区。

Prediction: force-route utility matrix 每行多个 expert 接近最优。

### H-G4: Router training 受 early commitment / inhibition / load balance 影响

Prediction: early route 与 final route 高相关；load-balance 或 inhibition 只改变分布均匀性，不保证 feature/expert compatibility。

## Claim Strength

当前 `router 学到 hidden geometry partition`：weakly supported。
需要 D1-D5 才能升级为 supported。

## What cannot be claimed

不能说 router 没学 feature；不能说 attention-output gating 一定会解决；不能说 inhibition 能保证多个 features 不塌到同一 expert。
