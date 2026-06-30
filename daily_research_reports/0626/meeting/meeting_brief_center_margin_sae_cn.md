# 0626 Meeting Brief：中心几何、margin 保存与 SAE 边界

## 结论

**不用标签、先验的时候，怎样找到对 routing 有用的 feature center对gating的行向量进行初始化，并让它在训练早期保持住均匀feature分发而不坍缩**

目前三条结论：

1. 聚类确实能在合适的隐藏状态群体上找到 feature center；如果用正确 center 初始化 router，早期训练能保持分发，主要原因不是 router 主动追着 center 走，而是初始 routing margin 足够大，更新的时候在不断增加margin. 但是由于聚类背景噪声存在，所以seed 7/8达成了目标，但是有一个seed下，初始化时没有把feature分开.
2. 稀疏自编码器（SAE）目前没有找到这些 center，不是因为 SAE 一定无用，而是因为它的训练目标是重构/稀疏，不是“找出对 routing 有判别力的 center”。
3. 去除common成分有助于让feature分开，但是common的估计方式需要conduct ablation.

这里的 routing margin 指：某个 feature 的隐藏状态中心进入正确 expert 的打分，比进入其他 expert 的打分高多少。margin 大，说明这个 feature 离错误 expert 的边界远，训练轻微扰动后仍不容易换 expert。

## 详细

两个结果。

第一，feature center 不是虚的。在 controlled no-position bridge 里，只看 route 位置，聚类可以完美恢复 feature；即使用更弱的 all-token 聚类，在大 calibration 下也能大概接近，但还不稳定。更关键的是，当我们用正确的 center 初始化 router 后，训练 1600 步还能保持 feature routing：pseudo-center 和 oracle-center 的 final feature NMI 都是 `1.000`。但它不是因为 router 行向量主动跟着 center 移动；movement alignment 是负的，pseudo-center 是 `-0.412`，oracle-center 是 `-0.398`。真正支持的解释是初始 margin 很大，训练后 margin 仍为正，大概在 `+3.5` 左右，所以 routing cone 没被打破。

第二，SAE 这条路目前没有过。SAE 可以把 hidden state 重构得很好，比如 SAE L1 8x 的重构误差很低，但 held-out route-position feature NMI 只有 `0.729`，明显低于 route-only 的 `1.000`。这说明“重构隐藏状态”不等于“找到 routing 需要的 center”。PCA、AE、SAE 都是在优化方差、压缩或重构结构，但我们的目标其实是找出能在 router 打分里产生正 margin 的方向。目标不对齐，所以 center 找不稳。

所以我现在的判断是：下一步不要继续泛泛地试 representation learning，而要把目标改成 routing-aware。也就是说，我们要么直接找能产生正 routing margin 的 center，要么先估计 random-init 训练中造成 expert 偏置的 common 方向，减掉以后看 feature residual geometry 是否变得更可读。

## 证据链

### 1. Center 几何存在，但样本群体必须对

问题：是不是 hidden state 里根本没有 feature center？

结论：不是。route-position hidden states 里 feature geometry 很干净。

证据：

| 条件 | held-out route-position feature NMI | 解释 |
| --- | ---: | --- |
| route-only | `1.000` | 正对照，说明 feature center 存在 |
| slot offset 3 | `1.000` | route 位置就是稳定的 feature 几何位置 |
| raw all-position | `0.831` 到 `0.863` | 能大概接近，但 seed 不稳定 |
| PCA q=4 | `0.871` | 小幅提升，但仍不接近 route-only |
| SAE L1 8x | `0.729` | 重构好，但 routing feature 不好 |

解释：问题不是“有没有 feature center”，而是“无标签时选哪一群 hidden states 来聚类”。把所有位置混在一起，会混入非 route 状态，导致 center 被花在错误几何上。

边界：这是 controlled bridge 结论，不等于真实 DCLM 语义 feature 已经被找到。

### 2. 正确 center 初始化可以早期保持，机制是 margin

问题：如果真的找到了 center，训练会不会立刻破坏？

结论：在 controlled no-position bridge 里，正确 center 初始化可以保持。

证据：

| 初始化 | final feature NMI | movement alignment | final raw margin | 解释 |
| --- | ---: | ---: | ---: | --- |
| pseudo-center | `1.000` | `-0.412` | `+3.544` | 保持成功，但不是主动追踪 |
| oracle-center | `1.000` | `-0.398` | `+3.647` | 与 pseudo 一致 |
| random | `0.797` | `-0.119` | `-3.662` | 任务能学，但 feature routing 不干净 |
| equal-norm random | `0.792` | `-0.108` | `-3.879` | 控制 norm 后仍不行 |

解释：router 不需要一直追着 feature center 走。只要初始化时把 feature center 放进正确 expert 的 cone，并且 margin 足够大，训练中的小漂移不会改变 top-1 routing。

边界：这不证明真实 DCLM preservation 已解决，也不证明 expert 有功能价值。它只说明 controlled setting 里 preservation 的直接机制更像 margin，而不是 active tracking。

### 3. SAE 失败的核心是目标错位

问题：为什么 SAE 没有找到 center？

结论：因为 SAE 的目标是重构和稀疏，不是 routing 判别。

更具体地说：

- SAE 学的是“怎样压缩/重构 hidden state”；
- 我们需要的是“哪些方向能让 router 把 feature 分到不同 expert”；
- 这两个目标不等价。

所以 SAE 重构误差低，不代表它学到的 code cluster 能在 route-position 上恢复 feature。当前实验正好显示了这个错位：SAE 可以 reconstruct，但 feature NMI 不够，且比 PCA/raw all-position 更弱。

边界：不能说 SAE 方法整体无用。只能说：**把 SAE code 直接拿来聚类，再映射回 hidden-space center，这个具体方案没有通过。**

## 当前研究位置

现在主线应该这样表述：

```text
feature center 存在
-> 正确 center 初始化能靠大 margin 保持
-> 但 label-free 地找到这些 center 仍没解决
-> SAE/PCA/AE 这种泛 representation objective 不够
-> 下一步需要 routing-aware center search 或 routing-aware common estimator
```

## 下一步判定

我建议下一步只问一个更窄的问题：

**random-init 训练过程中，能否估计并减去真正造成 expert 偏置的 routing-common 方向，从而让 feature residual center 更容易被聚类出来？**

通过标准不能是 load 更均匀，而必须是：

```text
减 common 后 held-out route-position feature NMI 提升；
或者 residual center 初始化后 raw routing margin 变成正的；
同时不能只是 position / frequency / slot-role shortcut。
```

如果这个通过，它会解释“common 成分挡住了 feature residual”；如果失败，我们就要承认：问题不是简单 common removal，而是需要更直接的 route-readout 或 margin-aware objective。

## 最后一句

这阶段的结论是：**中心几何是有的，正确中心能靠大 margin 被保存；但无标签地找到这些中心仍是瓶颈，SAE 失败的原因是目标没有对准 routing。**
