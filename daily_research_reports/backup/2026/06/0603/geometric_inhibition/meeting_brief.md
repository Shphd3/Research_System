# Meeting Brief

## Meeting Summary

**要回答的问题：**

如果对Router的行向量（视作专家的中心）进行归一化，构成严格cosine similarity分发，并且在每次更新的时候进行几何上的Inhibition，看能否在数据均匀分布情况下形成feature-level的专一化。

**结论：**

1. 在均匀分布的合成数据实验上，只靠几何上的Inhibition没有办法自然形成feature-level的specialization，但是能让不同的feature分得更开
2. 注入几何先验初始化的基础上，再使用inhibition，能够相比random初始化使用inhibition更能形成feature-level专一化，但是仍然不能稳定形成，推测需要更强的 分发-优化目标 绑定正则化项，也就是显式地注入表征几何分化的优化目标，才能保证优化过程中保持feature专一化分发

**Next Step：**

1. 将feature的Zipfian分布纳入考虑，推测此时使用归一化的Router相比普通的Router能够更好地分发
2. 并且要探究真实数据可实现的表征空间分发约束，以此构想真实场景router-专家初始化 + 表征-router binding的正则化项

**当前解释：**

Observation:
slot-stable init 提高初始 route-slot alignment；cosine router + slot init 在 center separation only 下最好，但仍然 seed-unstable；target accuracy 全部为 1.000。

Interpretation:

1. slot prototype geometry 是可用的；
2. cosine similarity router 比 dot-product router 更适合这个几何入口；
3. 但 center separation 只是在分开 router rows，没有解决 token-to-expert assignment binding；
4. 因此它不能单独作为稳定 specialization 机制。

### 数据叙述

每个样本只看一个关键预测位置：$B_i \rightarrow Y_{s,i}$。同一个 $B_i$ 在不同 slot/context 下目标 token 不同，所以 router 如果只看 $B_i$ identity，就不能解释 slot-specific target。

| Case                       | Sequence example                                                                                                                  | Prediction tested                                           | What this controls                                            |
| -------------------------- | --------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------- | ------------------------------------------------------------- |
| same $B_i$, different slot | $[r_{\mathrm{start}}, C_0, B_{17}, Y_{0,17}, r_{\mathrm{end}}]$ / $[r_{\mathrm{start}}, C_1, B_{17}, Y_{1,17}, r_{\mathrm{end}}]$ | $B_{17}\rightarrow Y_{0,17}$ / $B_{17}\rightarrow Y_{1,17}$ | 同一 $B_i$ 在不同 slot 下目标不同，测试 routing 是否能看 slot |
| same slot, different $B_i$ | $[r_{\mathrm{start}}, C_0, B_{17}, Y_{0,17}, r_{\mathrm{end}}]$ / $[r_{\mathrm{start}}, C_0, B_{42}, Y_{0,42}, r_{\mathrm{end}}]$ | $B_{17}\rightarrow Y_{0,17}$ / $B_{42}\rightarrow Y_{0,42}$ | 同一 slot 下仍有不同 target，任务不是只按 slot 分类           |

### 最重要实验代号

这次组会只需要最小代号。`geometric separation` 在这里等于 `router-center separation only`，不包括 supervised token-margin / logit-margin 正则化。

| Code | Router            | Init             | Extra loss / mechanism | Why it matters                                        |
| ---- | ----------------- | ---------------- | ---------------------- | ----------------------------------------------------- |
| C0   | 普通线性分发      | random           | none                   | 05 中最朴素 baseline                                  |
| C1   | 普通线性分发      | slot-stable init | none                   | 05 中只加 slot init 的朴素对照                        |
| C3   | cosine similarity | random           | none                   | cosine router 的朴素 baseline                         |
| C4   | cosine similarity | slot-stable init | none                   | cosine + slot init 的朴素对照                         |
| D1   | 普通线性分发      | slot-stable init | center separation only | 05_01：dot 下的 geometric separation                  |
| K1   | cosine similarity | slot-stable init | center separation only | 05_01：cosine 下的 geometric separation，最强但不稳定 |

### 关键实验结果

| Question                   | Pair               | Key metric            | Result                         | Interpretation                             |
| -------------------------- | ------------------ | --------------------- | ------------------------------ | ------------------------------------------ |
| slot init 是否注入几何     | C1 vs C0; C4 vs C3 | step-0 route-slot NMI | 0.242 vs 0.009; 0.242 vs 0.008 | slot prototype 有初始几何信息              |
| cosine路由 是否更适合          | K1 vs D1           | final route-slot NMI  | 0.566 vs 0.446                 | cosine + slot init 是更好的 center-only 条件 |
| center separation 是否足够 | D1 / K1            | final NMI std         | 0.320 / 0.491                  | seed variance 高，不能 claim 稳定 routing  |
| 是否有 accuracy tradeoff   | all                | target accuracy       | 1.000                          | task learning 不等于 specialization        |



## Meeting Preparation

**Question:**

在 top-1 MoE 中，如果我们先用 slot prototype 初始化 router，再只加入 router-center geometric separation，是否能稳定形成 slot-aligned routing？

**Why this matters?**

之前 ordinary top-1 router 的失败可能来自 early assignment lock-in。这个实验检查一个更清晰的几何机制：先给 slot prototype 作为 router center 初始方向，再只让 router centers 互相分开，问它是否足以防止 route mixing。

**Hypothesis:**

slot centroid prototype 含有可用的 slot direction；router-center separation 可能维持不同 expert center 的几何分离，从而减少 route mixing。

**Evidence:**

最重要 metric 是 final route-slot NMI 及其 seed variance，因为本次组会目标是判断 center separation 是否能稳定 routing，不是完整 utility specialization。

| Evidence item                    | Comparison     | Result                          | Decision meaning                           |
| -------------------------------- | -------------- | ------------------------------- | ------------------------------------------ |
| slot initialization 有信息            | C1/C4 vs C0/C3 | step-0 NMI 约 0.242 vs 约 0.009 | slot init 是有效入口                       |
| center separation 的 结果    | D1             | final NMI 0.446, std 0.320      | 不稳定                                     |
| center separation 的 cosine similarity 结果 | K1             | final NMI 0.566, std 0.491      | 分得最开但 seed-unstable                       |
| center separation 是否足够       | D1/K1          | 都没有稳定到 NMI=1              | 只分开 centers 不能解决 assignment binding |
| no accuracy tradeoff             | all            | target accuracy 1.000           | accuracy 不是 specialization 证据          |

**Boundaries:**

这个结论只覆盖 uniform multi-B synthetic、slot-stable init、router-center separation only、无 router bias、top-1 selected-gate MoE。

**Cannot claim yet:**

不能说 center separation alone 解决 specialization；不能说 cosine 自然产生稳定 specialization；不能说 Zipfian 高频/低频已经解决；不能说 expert utility 完整解决。

**Next Decision:**

slot prototype + cosine router 有几何信号，但 center separation alone 仍不足以稳定 assignment binding。

**Next Iteration:**

下一步要进入 Zipfian