# 明日组会可直接汇报：MTP 的最小有效任务属性

## 一句话结论

**我们第一次用受控实验确认：MTP 的价值不在于“多看一个未来
token”，而在于把最终答案所需变量的监督，提前施加到答案必须经过的
较早状态；如果答案可以绕行，或提前监督的是无关变量，收益会大幅
缩小。**

## 最小任务

序列包含答案变量 $A$、无关变量 $B$、一个 `RELAY` 状态和答案位置。
正确答案恒为 $A$。

- 必须中继：答案位置只能读取 `RELAY`；
- 允许绕行：答案位置可以直接读取 $A$；
- 答案监督：`RELAY` 的辅助头预测 $A$；
- 无关监督：同一个辅助头在同一位置预测同词表、同词频、同样可预测
  的 $B$；
- 测试时只使用普通 next-token 主头。

NTP 并非看不到 $A$：它仍在晚一个位置预测 $A$，而且可以学会任务。
比较的是“较早直接信用”相对“稍晚信用”的有限预算效率。

## 决定性结果

主指标是前 1000 步普通主头答案 NLL 的曲线面积均值。NLL 是模型给
正确答案的负对数概率，越低越好；单位 `nat` 是自然对数单位。

| 对照 | 必须中继收益 | 允许绕行收益 | 结构必要性交互 |
| --- | ---: | ---: | ---: |
| 无关 $B$ → 答案 $A$ | 0.2315 nats | 0.0181 nats | 0.2134 nats |

交互的 95% 区间为 `[0.1646, 0.2585]`，8/8 种子为正。四组最终均
8/8 达到 100% 准确率；替换 relay 状态后，普通主头均 100% 跟随供体
答案。

更直观地：

- 必须中继时，答案监督达到 90% 准确率的中位步数是 60；
- 无关监督需要 160 步；
- 第 100 步两者平均准确率为 99.28% 对 16.35%；
- 允许绕行时，两者第 100 步都已 100%。

![任务相关性对照学习曲线](../../../../../../Projects/from-attention-to-search/main/experiments/A13/13_00_task_properties_to_standard_head_utility/A13_00_05_E01_task_relevant_target/figures/objective_learning_curves.png)

## 对 MTP/NTP 认识的更新

过去只能说：MTP 能在更早状态产生直接梯度，但“形成”不等于普通头
“使用”。

现在可以进一步说：

> 当较早状态是最终答案的必经载体，而且 MTP 的提前目标与该状态需要
> 承担的答案变量一致时，提前监督能显著加速普通 NTP 主头学习；这不是
> 因为 NTP 永远看不到答案，也不是一般辅助正则化。

最小充分条件是：

```text
future target 含答案变量
-> 变量在较早状态形成
-> 该状态是答案必经路径
-> 状态可运输
-> 普通主头因果使用
-> NTP 的稍晚信用尚未在固定预算内充分
```

## 本轮还纠正了两个研究错误

1. 最初把“状态中继”和“根据查询选择正确值”混为一个任务，导致 NTP
   载体不稳定。移除查询绑定后载体通过，所以查询绑定应是后续独立
   sub-anchor。
2. 曾要求每个训练目标施加后都必须学会才允许比较，这会按处理后的
   结果筛选数据，把“某目标导致学不会”这个真实效应删除。现在载体
   有效性只由处理前的 NTP-only 阶段决定。

## 为什么代码可能更受益

当前只形成一个待验证解释：代码更常出现“早期程序状态或约束，必须
沿数据流/控制流运输，晚些时候才决定精确输出”的结构；普通文本更常
有局部冗余和同义绕行。因此不是“代码天然适合 MTP”，而是：

> 代码中若有更多答案相关、必须运输、延迟生效的状态，MTP 才应比匹配
> 文本获得更大收益。

这不是本轮实验结论，必须以后做属性匹配的代码/文本对照。

## 唯一下一步

**先用 NTP-only 验证 query-conditioned binding（根据晚到查询绑定正确
值）能否成为稳定载体；通过后，再只改变“是否需要组合”，检验本轮的
提前答案信用效应能否延伸到代码/规划所需要的组合状态。**

详细证据入口：

- [A13 主 anchor](../../../../../../Projects/from-attention-to-search/main/problem_anchors/13_mtp_task_property_decomposition/13_00_task_properties_to_standard_head_utility/13_00_task_properties_to_standard_head_utility_anchor.md)
- [决定性结果](../../../../../../Projects/from-attention-to-search/main/experiments/A13/13_00_task_properties_to_standard_head_utility/A13_00_05_E01_task_relevant_target/summary.md)
- [完整中文 story](../../../../../../Projects/from-attention-to-search/main/stories/13_mtp_task_property_decomposition/01_task_relevant_relay_supervision_cn.md)
