# 12 结构化组合任务与标准头使用

## 回答的问题

A11 发现的更早直接信号，能否在必须形成中间状态的组合任务中转化为共同标准头的功能收益？

## 数据

每条样本包含两张完整随机一一映射表。给定起点 $A$，第一张表产生中间实体 $B$，第二张表产生答案 $Y$：

$$
B=\pi_1(A),\qquad Y=\pi_2(B).
$$

任意单表都不能确定答案，两表联合才能完成有序组合。它是计算树的深度二串行基础情形，不是一般多分支树。

## 当前结论

1. 数据构造能排除单表捷径，工作负载定义成立。
2. 当前两层、宽度 64 的从零训练模型仍接近八分类机会水平，因此没有资格比较 NTP 与 MTP。
3. 在线性 oracle 因子模型中，单一表征方向会导致 MTP 改善未来因子却损害标准目标；两个方向时损害消失。等辅助训练量课程不能补出缺失方向。

线性结果只证明缺少独立方向是一个充分冲突机制，不证明 Transformer 参数量与 MTP 收益的尺度律。

## 唯一下一决策

先审阅因果使用协议并运行共享预训练模型的能力门槛。通过后，才从同一检查点比较 NTP 与信息性 Next-2，并干预中间实体 $B$，判断共同标准头是否按第二张表的规则改变答案。门槛失败则停止。

来源：[A12 索引](../../../Projects/from-attention-to-search/main/problem_anchors/12_structured_compositional_mtp_workload/README.md) · [A12 故事](../../../Projects/from-attention-to-search/main/stories/12_structured_compositional_mtp_workload/01_structured_composition_workload_and_standard_head_use_cn.md) · [待审协议](../../../Projects/from-attention-to-search/main/experiments/A12/A12_07_standard_head_causal_representation_use/protocol_cn.md)
