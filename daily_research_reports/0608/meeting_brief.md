# Meeting Brief

## Meeting Summary

我们要解决的问题是：
在构造的feature均匀分布，Gating矩阵random uniform初始化（$w_{ij} \sim U(-1/\sqrt{d_{model}}, 1/\sqrt{d_{model}})$）的情形下，为什么MoE还是发生了路由坍缩？

我们的核心数学模型：

$$
h_f = c + r_f \\

logits = w_e^T h_f = w_e^T (c + r_f)
$$

### Conclusion:

uniform collapse 的 step-0 主要来自 routed position / positional embedding 造成的 common offset；但训练最终产生的 collapse 不是仅靠去 position embedding就能完全解决。

在之前的uniform数据分布setting下：
1. 路由坍缩根因不是因为构造的数据是不均匀的和坏的router初始化造成的
2. 数据尽管不存在common feature，但是transformer block输出的hidden state包含一个跨features的common component，这个common component是由于position embedding造成。
    1. 将position embedding减掉进行路由以后，发现初始化时候的expert是能够回归均匀分发的。
    2. 将路由的权重构造成和position embedding垂直时，初始的分发也能回归均匀分发
    3. 但是common偏置的去除主要修复了早期的路由坍缩现象，去除后能够提升feature分发的专一性，但是不能解决feature-to-expert的specialization.（以下max load越低越好，0.25时表明是完美的feature专一化分发）
        - 数据一实验repeated pattern: **r - AAAA B_i - y_{A,B_i} - r**
            final max-load 从 baseline 约 0.70 降到约 0.43。
        - 数据二实验distributed_complex pattern: **r - ABCDE B_i - y_{ABCDE,B_i} - r**
            final max-load 从 baseline 约 0.92 降到约 0.74。

要避免最终的坍缩，除了在初始化的时候要合理避免collapse偏置，还需要在训练过程中在几何上构造防止坍缩的正则化项。（早期使用load-balance能够极大程度缓解最终路由坍缩，但是治标不治本，并且不能构成feature especialization）

### Next decision:

1. 将 05_03 的 claim boundary 更新为：fixed routed position / positional embedding 是 step-0 common offset 的主要因果来源之一。
2. 暂时不要把 load balance 或 anti-lockin 作为主结论；当前 meeting 重点是 common source localization。
3. 下一步需要决定：剩余 final collapse 是继续追踪 training-time amplification，还是先回到 feature-structure specialization 的主线。


### Evidence:
P1/P2: common-score \(w_e^\top c\) 预测 step-0 dominant expert，agreement 接近 1.0。
baseline 是 0.25。full hidden step-0 max-load 约 0.62-0.64；
在logit上减去common component部分贡献后后降到约 0.28-0.29。

P7 position/source ablation:
- baseline_pos: common_ratio 约 0.51，step-0 max-load 约 0.62。
- zero_routed_pos_step0: common_ratio 降到约 0.045，step-0 max-load 降到约 0.33-0.36。
- zero_all_pos_step0: common_ratio 约 0.035，step-0 max-load 约 0.33-0.36。
- random_feature_position_eval_only: common_ratio 降到约 0.081-0.082，step-0 max-load 降到约 0.39-0.41。
- no_pos_frozen_train: accuracy 约 0.998，final max-load 降低，但没有完全消除 final collapse。

**分析**：fixed routed position / positional embedding 是 step-0 common component 的主要因果来源；random feature position 能削弱 early common，但不能可靠解决 final collapse。

P3/P5: 在logit上减去common component部分贡献降低 collapse，accuracy 保持，但 final max-load 仍偏高，专家分得的feature不均匀。
P4: common-aware init 修复 step-0，但 final mixed。

**分析**：所以 offset control 不等于 solve final collapse。

## Meeting Preparation

**Question:**
在 uniform feature frequency 和 bias-free random linear gate 下，为什么 step-0 routing 已经偏向某个 expert，并最终形成 collapse？

**Why this matters?**
如果 uniform baseline 的 route consistency 本身来自 common-offset seeded collapse，那么后续 feature specialization / route consistency 的解释都会被污染。

**Hypothesis:**
routed hidden state 可分解为 \(h_f=c+r_f\)。common component \(c\) 通过 \(w_e^\top c\) 产生 expert-specific effective bias，决定 step-0 dominant expert；final collapse 还需要 top-1 training amplification。

**Evidence:**
1. P1/P2: \(w_e^\top c\) predicts step-0 dominant expert; cancellation lowers step-0 max-load to near random/balanced range.
2. P3/P5/P4: offset control improves early geometry and hard collapse but final max-load remains high.
3. P6/P7: anti-lockin warmup gives strongest final-load control; final route utility is co-adapted, not simply utility-wrong.

**Can claim now:**
fixed routed position / positional embedding is a major causal source of the step-0 common component.

**Cannot claim yet:**
position embedding is the only source;
position ablation solves final collapse;
load balance means feature specialization;
the result transfers beyond this toy setting.

**Next Decision:**
position/template causal ablation + full 4-card verification of baseline, P5B, P4-I4, P6A.

**每个实验具体说明了什么**

| Protocol | 它问的问题                                                   | 结果说明                                                                                         |
| -------- | ------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| **P1**   | common score (w_e^\top c) 能不能预测 step-0 dominant expert？ | 能。说明 step-0 偏向不是普通 random split，而是 common offset 在起作用。                                       |
| **P2**   | 这个预测跨 seed 是否稳定？                                        | 稳定。common-score agreement 接近 1.0，强于 random baseline。                                         |
| **P3**   | 训练时取消 common offset，collapse 会不会下降？                     | hard collapse 下降，但 final max-load 仍偏高。说明 common 是 early driver，但不是全部。                        |
| **P4**   | common-aware initialization 能不能修复 step-0 偏置？            | 能显著降低 step-0 load，但 final 结果 mixed。说明 init 通过 common score 影响 early routing，但 init alone 不够。 |
| **P5**   | 哪种 common subtraction 更稳定？                              | logit-level cancellation 最稳；SVD / low-rank residual 不稳定。                                     |
| **P6**   | anti-lockin warmup 能不能控制 final collapse？                | P6A 最强，final load 明显下降，accuracy 基本保持。说明 final collapse 需要 training-time control。             |
| **P7** | position/template source 是不是 common shift 的因果来源？ | 是。zero routed position embedding 将 common_ratio 从约 0.51 降到约 0.045，并将 step-0 max-load 从约 0.62 降到约 0.33-0.36；但 final collapse 没有完全解决。 |