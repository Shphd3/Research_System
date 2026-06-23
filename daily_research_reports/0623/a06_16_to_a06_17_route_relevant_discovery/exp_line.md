# A06_16-A06_17 Exp Line

| Anchor | 父问题 | 更新了什么 | 是否可信 | 下一步 |
| --- | --- | --- | --- | --- |
| A06_16 | 从干净 synthetic 走向更真实序列时，feature 初始化先坏在哪里？ | 去掉 learned absolute position 后，route-position feature 发现和训练保持都不坏；C0-C3 step0/final `feature_NMI=1.0`。 | 可信，但只在 no-pos controlled bridge 内成立。 | 不再主攻 preservation，转向 all-position / route-relevant state 边界。 |
| A06_17 | all-position 聚类失败，是 feature 不存在，还是聚类对象选错？ | route-only 和 slot 最后位置 8/8 完美；all-position 均值 0.797，说明所有 hidden states 一起聚类不可靠。 | 可信；有 8 seeds、oracle/route/slot/non-slot/role-balanced 对照。 | 构建无标签 route-relevant state selector，然后只对筛出的状态聚类。 |

当前主线：feature 几何存在 -> 训练保持不是这个 synthetic bridge 的主瓶颈 -> 真正缺的是无标签地选出“应该参与路由判断的 hidden states”。
