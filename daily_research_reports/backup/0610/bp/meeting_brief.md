# Meeting Brief

## Meeting Summary

Questions:

父问题：
在无 position embedding、feature 均匀的最小任务中，为什么 baseline线性router sparse top-1 MoE 仍然从随机初始化进入 collapse，而不是形成 slot-to-expert specialization？

Setup:

实验使用的是一个最小合成 moving-block 数据集。序列长度为 12；`0` 是 filler token；`SLOT_s` 使用 token `1..4`；固定的 `B_CONST` 是 token `10`；目标 `Y_s` 使用 token `20..23`。每条样本只包含一个连续三元组：

```text
prefix filler + SLOT_s B_CONST Y_s + suffix filler
```

loss 和 routing metric 都在 `B_CONST` 位置计算；任务是根据当前 slot 预测对应的 `Y_s`。下面是两个具体样本：

```text
Example 1:
slot = 0, block_start = 0
sequence = [1, 10, 20, 0, 0, 0, 0, 0, 0, 0, 0, 0]
meaning  = [SLOT_0, B_CONST, Y_0, filler, filler, filler, filler, filler, filler, filler, filler, filler]
route position = 1, routed token = B_CONST = 10, target = Y_0 = 20

Example 2:
slot = 2, block_start = 5
sequence = [0, 0, 0, 0, 0, 3, 10, 22, 0, 0, 0, 0]
meaning  = [filler, filler, filler, filler, filler, SLOT_2, B_CONST, Y_2, filler, filler, filler, filler]
route position = 6, routed token = B_CONST = 10, target = Y_2 = 22
```

Conclusion:

1. Collapse 不是因为 slot 信息缺失，也不是因为 slot-specialization 不可达。无 position moving-block baseline 仍 collapse，但 h_B 中 slot 信息可线性解码；slot-aware initialization 可以形成高 NMI 的 slot-level specialization。
    - evidence：
    ```text
    Round-1 baseline: accuracy=1.0, mean max_load=0.969, mean slot_NMI=0.080。
    Slot probe: held-out-position slot probe accuracy=1.0。
    Slot-init positive control: mean slot_NMI=0.980, mean max_load=0.278, accuracy=1.0。
    ```
2. common component 对 router logit 的贡献是确定可分解的；common-logit 在 step 0 已经强于 feature特有的logit margin，并在 step 10 前迅速放大，且能预测 final dominant expert。（最终发生坍缩）
    - evidence：
    ```text
    Decomposition reconstruction error: mean 1.073e-7，max 5.849e-7。
    Common-dominant cells: 2238/2560。
    Step 0: common margin=0.2993，slot margin=0.0523，common argmax predicts final expert=0.844。
    Step 10: common margin=1.7087，slot margin=0.2993，prediction=0.969。
    ```
3. 减去common部分显著提高 slot-level specialization，并保持 accuracy=1.0，说明坍塌原因来源于：线性Router是学到了common部分的分发偏置
    - evidence：
    ```text
    baseline: slot_NMI=0.080, max_load=0.969, accuracy=1.000。
    cancel_0_10: slot_NMI=0.896, max_load=0.434, accuracy=1.000。
    cancel_0_final: slot_NMI=0.963, max_load=0.309, accuracy=1.000。
    ```

1. 没有position embedding，同时feature在sequence中移动情况下，collapse仍然存在，此时的collapse主要来源于hidden state中的common元素主导了gating logits $w_e^T c \gg w_e^T h_{feature}$
2. 在合成数据实验的情形下，random initialization 在训练的初期总是会对齐hidden state中的common部分，如果这种对齐行为不被纠正，那么在NTP的训练范式下，线性gating矩阵就会发生lock-in，最后所有feature坍缩到唯一分发的专家上
3. 当我们将common部分删除，能够形成feature-level的specialization
4. 这个common的来源有一大部分来源于我们的数据构造：

```text


```

如上，由于我们的B是给定的，因此B经过attention + normalized之后的，所有的slot中都存在共同的部分：
我们根据这个消融，将B换成了B_i以后，发现路由NMI缓解了，但是还是存在common部分，这部分common部分的来源我们尚不知晓
5. 当我们给定一个特定的先验初始化，我们发现gating能够在早期lock-in到对应的specialization的情形，同时，这种初始化是在空间中连续变化的

Minimum reason:

这个合成无位置编码、且特征在序列中移动的实验设定，排除了三种一阶解释：

数据分布不均衡；
hidden state 中缺失 slot 信息；
slot-specialization 本身不可实现。

实验证据：
1 P1 表明：即使发生路由坍缩（collapse），模型仍然能够达到接近完美的任务性能。
2 P2 表明：slot 信息可以从 h_B中被准确解码。
3 P5 表明：在有利的 router 初始化条件下，slot-specialization 是可以实现的。

因此，现在对collapse最合理的解释是：
router 侧：common logit 主导（common-logit dominance）以及 sparse top-1 路由导致的早期锁定（early lock-in）。

Current interpretation:

显式控制位置因素之后，我们发现：
> 被路由的 B-position hidden state 中仍然存在一个 common component，而该 common component 对应的 router score 主导了 top-1 路由决策。

这个 common score 可能有两种来源：

1. 在初始化时就已经存在；
2. 在训练最开始的几个优化步骤中迅速增长。
随后，sparse top-1 routing 会在 slot-specific 信号尚未建立之前，将路由锁定到某一个早期占优的 expert 上，从而导致 collapse。

Next decision:

第二轮实验需要回答以下问题：

1. common-logit 优势是在 step 0 就已经很大，还是在训练初期逐渐增长出来的？
在移除 position embedding 之后，这个 common component 究竟来自哪里？
2. 如果主动消除（cancel）common-logit，是否能够让随机初始化的 sparse top-1 MoE 进入 slot-specialization 的可达优化盆地（reachable basin）？
3. 为什么 slot-initialized routing 能够保持稳定，而随机初始化 routing 会发生 collapse？

## Meeting Preparation

**Question:**

[One core question this meeting should answer.]

**Why this matters?**

[Explain why it affects the mainline judgment, claim boundary, or next experiment decision.]

**Hypothesis:**

[Falsifiable research hypothesis. State the parent problem / subproblem relation when needed.]

**Evidence:**

[Summarize the key evidence. Put the most important metric or figure first because it decides this judgment.]

1. [Evidence point: metric / figure / table / experiment condition.]
2. [Evidence point: what it cannot prove.]

**Boundaries:**

[State which conditions, data, model, training objective, initialization, or metric this conclusion covers.]

**Cannot claim yet:**

[State the stronger conclusion that cannot be claimed yet.]

**Next Decision:**

[The smallest decision after this meeting: continue, redirect, add one diagnostic, or park.]

**Next Iteration:**

[If continuing, write the minimal decisive experiment. If not, write the park or redirect condition.]
