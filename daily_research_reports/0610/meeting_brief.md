# Meeting Brief: Common-Logit Driven Collapse in Minimal Sparse Top-1 MoE

## Meeting Summary

### Question

在无 position embedding、feature 均匀、`SLOT_s B_CONST Y_s（ABC）`最小任务中，为什么 线性router sparse MoE 仍然从随机初始化进入 collapse，而不是形成 slot-to-expert specialization？

---

### Setup

我们使用一个最小合成 moving-block 数据集。序列长度为 12；`0` 是 filler token；`SLOT_s` 使用 token `1..4`；固定的 `B_CONST` 是 token `10`；目标 `Y_s` 使用 token `20..23`。

每条样本只包含一个连续三元组：`prefix filler + SLOT_s B_CONST Y_s + suffix filler`。

实验约束：position embedding disabled / zeroed；router 是 dot-product sparse top-1；loss 和 routing metrics 都只在 `B_CONST` 位置计算；主实验中 `B_CONST` 固定。

任务含义：在 `B_CONST` 位置根据前一个 `SLOT_s` 预测对应的 `Y_s`。

具体样本：

```text
Example 1:
slot = 0, block_start = 0
sequence = [1, 10, 20, 0, 0, 0, 0, 0, 0, 0, 0, 0]
meaning  = [SLOT_0, B_CONST, Y_0, filler, ..., filler]
route position = 1, target = Y_0

Example 2:
slot = 2, block_start = 5
sequence = [0, 0, 0, 0, 0, 3, 10, 22, 0, 0, 0, 0]
meaning  = [filler, ..., SLOT_2, B_CONST, Y_2, filler, ..., filler]
route position = 6, target = Y_2
```

---

## Conclusions

1. **Collapse 不是因为任务学不会，也不是因为 `h_B` 缺少 slot 信息。** Baseline accuracy 是 `1.0`，slot probe 在 held-out position 上也是 `1.0`，但 random-init routing 仍然 collapse。
2. **dot-product router 的 top-1 决策被 common-logit 主导。** Common margin 在 step 0 已经大于 slot margin，并在 step 10 前迅速放大；早期 common argmax 能预测 final dominant expert。
3. **主动消除 common-logit 可以显著提高 slot-level specialization。** Common cancellation 在保持 accuracy `1.0` 的同时，把 mean slot NMI 从 `0.080` 提高到 `0.896` 或 `0.963`。

### 1. Collapse 是因为合成数据中去除了position embedding仍然含有common部分，减去common部分（或者给定slot信息初始化）slot-specialization 是可以达成的。

无 position moving-block baseline 仍 collapse，但 `h_B` 中 slot 信息可线性解码；slot-aware initialization 可以形成高 NMI 的 slot-level specialization。

| Evidence | Result |
|---|---:|
| Round-1 baseline accuracy | 1.000 |
| Round-1 baseline mean max_load | 0.969 |
| Round-1 baseline mean slot NMI | 0.080 |
| held-out-position slot probe accuracy | 1.000 |
| slot-init positive-control mean slot NMI | 0.980 |
| slot-init positive-control mean max_load | 0.278 |

Interpretation: task learning succeeds, slot information exists in the routed hidden state, and slot-specialization is reachable under favorable initialization. Therefore the failure is not primarily data imbalance, missing slot representation, or intrinsic impossibility of slot-specialization.

### 2. 进一步分析，common component 对 router logit 的贡献是可分解的；common-logit 在 step 0 已经强于 feature 特有的 logit margin，并在 step 10 前迅速放大，且能预测 final dominant expert。

The hidden state at the routed position is decomposed as:

$$
h = c + r_{\mathrm{slot}} + u_{\mathrm{position}} + \epsilon
$$

Because the router is dot-product, the score decomposes linearly:

$$
score_e(h)
= w_e^\top h
= w_e^\top c
+ w_e^\top r_{\mathrm{slot}}
+ w_e^\top u_{\mathrm{position}}
+ w_e^\top \epsilon
$$

| Evidence | Result |
|---|---:|
| decomposition mean reconstruction error | $1.073 \times 10^{-7}$ |
| decomposition max reconstruction error | $5.849 \times 10^{-7}$ |
| common-dominant cells | 2238 / 2560 |
| step-0 common margin | 0.2993 |
| step-0 slot margin | 0.0523 |
| step-0 common argmax predicts final expert | 0.844 |
| step-10 common margin | 1.7087 |
| step-10 slot margin | 0.2993 |
| step-10 common argmax predicts final expert | 0.969 |

Interpretation: common-logit is not merely a late consequence of collapse. It is already present at initialization and grows before early lock-in.

### 3. 减去 common 部分显著提高 slot-level specialization，并保持 accuracy=1.0，说明坍塌原因来源于：随机初始化下，线性 Router 是学到了 common 部分的分发偏置。

In this controlled dot-product setting, common-logit cancellation gives intervention-relevant evidence that common-logit contribution helps cause random-init collapse.

| Condition | slot NMI | max_load | accuracy |
|---|---:|---:|---:|
| baseline | 0.080 | 0.969 | 1.000 |
| cancel_0_10 | 0.896 | 0.434 | 1.000 |
| cancel_0_final | 0.963 | 0.309 | 1.000 |

Interpretation: removing common-logit does not merely improve load balance; it substantially improves slot-to-expert specialization while preserving task learning.

---

## Minimum Reason

这个合成无位置编码、且 feature 在 sequence 中移动的实验设定，排除了三个一阶解释：数据分布或 position shortcut、hidden state 中缺失 slot 信息、slot-specialization 本身不可实现。

最小解释应转向 router-side geometry：

The routed hidden state contains slot information, but the dot-product router score is dominated by an expert-specific common score $w_e^\top c$. This common score creates an early effective expert bias; sparse top-1 training then locks into the common-dominated routing basin.

中文直觉：

feature 在 hidden state 里，但 router 的早期打分坐标系被 common 方向劫持了。

---

## Current Interpretation

在 dot-product sparse top-1 router 中，router decision 不是直接由“是否存在 slot 信息”决定，而是由各个 expert 的 router score 排序决定。

虽然 `h_B` 中 slot 信息可解码，但 routing score 可以被分解为：

$$
score_e(h_B)
= w_e^\top c
+ w_e^\top r_{\mathrm{slot}}
+ w_e^\top u_{\mathrm{position}}
+ w_e^\top \epsilon
$$

当前结果显示：

$w_e^\top c$ often dominates the top-1 decision before slot-specific margin becomes decisive.

因此，random initialization 容易进入 common-collapse basin：

random init -> one expert has higher common score $w_e^\top c$ -> early top-1 routing sends many slots to that expert -> sparse top-1 training stabilizes this route assignment -> final routing collapses despite slot information being present.

slot-aware initialization 和 common-logit cancellation 可以把 routing 推向另一个 basin：

slot margin strong enough / common score controlled -> slot-level routing becomes stable -> high slot NMI with accuracy preserved.

---

## Additional Evidence: Basin and Source

### Basin evidence

Slot-init interpolation shows a basin transition: as router initialization moves from random toward slot-aligned directions, final slot_NMI rises from collapse to specialization.

| alpha | mean NMI | mean max_load | initial slot-minus-common |
|---:|---:|---:|---:|
| 0.00 | 0.080 | 0.969 | -0.2421 |
| 0.05 | 0.699 | 0.588 | 0.0056 |
| 0.10 | 0.856 | 0.466 | 0.1676 |
| 0.20 | 0.930 | 0.372 | 0.2743 |

Interpretation: slot-init success likely comes from moving the router across a slot-vs-common margin boundary into a specialization basin. Alpha `0.20` is the first tested mean-NMI value above `0.90`.

### Source evidence

Common source is narrowed, but not fully identified.

| Variant | common margin | slot NMI |
|---|---:|---:|
| original | 2.3158 | 0.080 |
| route_at_slot | 0.4681 | 0.504 |
| varied_b | 0.9528 | 0.070 |
| varied_filler | 1.9539 | 0.080 |

Interpretation: `B_CONST` / B-position representation is a leading source candidate. However, varied-B reduces common margin but does not restore slot NMI, so the common source is not fully identified.

---

## Boundaries

This conclusion covers:

- minimal synthetic no-position moving-block task;
- dot-product sparse top-1 router;
- fixed `B_CONST` main setting;
- loss and routing metrics at `B_CONST` position;
- slot NMI as primary specialization metric.

This conclusion does not yet cover:

- real language models;
- multi-B or natural data settings;
- causal expert functional specialization;
- label-free deployable router method;
- complete identification of common component source.

---

## Cannot Claim Yet

1. Cannot claim common source is fully identified.
2. Cannot claim common-logit cancellation is a deployable method.
3. Cannot claim expert computation is causally slot-specialized.
4. Cannot claim results transfer beyond this toy setting.
5. Cannot claim load balance alone equals feature-level specialization.

---

## Next Decision

Should we design a label-free anti-common / anti-lockin dot-product sparse top-1 router that removes or equalizes early common-logit bias and tests whether random-init training can reach high slot_NMI without slot labels or slot-centroid initialization?

---

## Next Iteration

Run one minimal label-free common-control router.

Core rule:

- expert receives full $h$;
- router score controls the estimated common-logit term;
- sparse top-1 routing is preserved;
- intervention acts during the early lock-in window;
- no slot labels or slot-centroid initialization are used.

Primary success:

- slot NMI increases substantially from random init;
- accuracy stays near `1.0`;
- max_load decreases as secondary evidence.

Failure cases:

- load balance improves but slot NMI remains low;
- accuracy drops;
- routing re-collapses after the early window;
- method depends on slot labels.

---

## One-Sentence Takeaway

在这个 minimal dot-product sparse top-1 MoE setting 中，collapse 不是因为 feature 不存在，而是因为 common component 通过 $w_e^\top c$ 形成早期 expert-specific routing bias；random initialization 容易进入 common-collapse basin，而 slot-init 和 common-cancel 证明 slot-specialization basin 是可达的。
