# A06_16 到 A06_17 Meeting Brief

## 一句话结论

我们现在知道：在这个 controlled synthetic bridge 里，feature 本身不是找不到；真正的问题是不能把所有 hidden states 一起拿来聚类。下一步应该先无标签地找出“真正参与路由判断的 hidden states”，再做 feature 聚类初始化。

## 要解决的父问题

真实数据里没有现成 feature label，也不知道哪些位置的 hidden state 应该决定 expert 分发。所以父问题是：

能不能从模型 hidden states 里，无标签地找到可用于 expert 初始化的 feature 结构？

这里的“路由位置”指 feature slot 的最后一个 token，也就是实际让 router 做 expert 选择的位置。

## A06_16 更新了什么

A06_16 问：如果我们把输入做得更接近真实序列，只控制 token 序列而不直接控制 hidden state，feature 初始化会先坏在“发现阶段”，还是坏在“训练保持阶段”？

结论：在去掉 learned absolute positional embedding 后，route-position 的 feature 发现和训练保持都成功。

关键结果：

| 条件 | 结果 |
| --- | --- |
| route-position 聚类 | C0-C3 全部 `feature_NMI=1.0` |
| 训练后保持 | C0-C3 final `feature_NMI=1.0` |
| all-position 聚类 | 仍有不稳定边界 |

认知更新：不要再把 synthetic no-pos bridge 的主断点放在训练保持上。当前最自然的断点是：不知道该拿哪些 hidden states 去聚类。

## A06_17 更新了什么

A06_17 问：all-position 聚类失败，是因为 feature 几何本身不清楚，还是因为聚类对象选错了？

结论：支持“聚类对象选错”。route-position 上 feature 很清楚，但所有位置混在一起聚类会把完整 feature 合并到同一个 expert。

关键结果：

| 聚类对象 | route-position `feature_NMI` | 判断 |
| --- | ---: | --- |
| oracle route | 1.000 | route feature 几何存在 |
| route-only | 1.000 | 无标签聚类能找到 feature |
| slot 最后位置 | 1.000 | 真正稳定的是路由位置 |
| all-position | 0.797 | 不可靠，经常合并 feature |
| slot 四个位置混合 | 0.900 | 比 all-position 好，但仍不稳 |
| role-balanced all-position | 0.854 | 只平衡数量不够 |
| 非 slot 位置 | 0.664 | 有 feature 泄露，但不是干净路由结构 |

失败方式很重要：不是 nuisance，也不是 slot start。all-position 的 `nuisance_NMI=0`、`slot_start_NMI=0`，但 active experts 变少，说明是多个完整 feature 被塞进同一个 expert。

## 当前研究线

1. A06_16：feature 在路由位置可以被无标签发现，并能被当前训练保持。
2. A06_17：所有 hidden states 一起聚类不是可靠 feature 初始化对象。
3. 下一步：先找 route-relevant hidden states，再聚类这些状态。

这条线把问题从“feature 是否存在”推进到“如何无标签地选择正确的 hidden-state population”。

## 边界

现在不能 claim：

- 这已经能用于 real DCLM；
- RoPE 下也一样；
- whole-slot composition 已解决；
- 非 slot 位置没有 feature 信息；
- 已经有了最终可部署的初始化方法。

现在可以 claim：

- 在 corrected no-pos bridge 中，route-position feature 几何是清楚的；
- all-position clustering 不是可靠 proxy；
- 下一步必须研究 route-relevant state selection。

## 下一步 Anchor

最自然的下一张判定卡：

不用 feature label，只用 hidden-state 或模型内部可观测统计，先筛出“像路由位置”的状态；然后只对这些状态做聚类，看是否能恢复 route-only 的 `feature_NMI=1.0`。
