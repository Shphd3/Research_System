# MTP 的额外学习信号能否被标准预测使用

## 0. 执行摘要

**研究问题：** 多词元训练（MTP）比普通下一词元训练（NTP）多学到了什么；这份信息能否被同一个标准预测头用于需要多段证据组合的任务？

**本次更新：** 研究被拆成两层：先确定 MTP 特有的直接学习信号，再用一个必须先形成中间结果、再继续查询的任务检验功能使用。

**当前结论：**

1. 信息性未来词元会给当前位置增加 NTP 没有的直接更新；新增位置是否含新信息、更新方向是否一致，比预测跨度本身更重要。
2. 这份信息可以在当前位置形成并传到共享参数，但不保证在下一个位置仍被标准头使用。
3. 表征方向不足可以造成 MTP 学好未来目标却损害标准目标；课程安排不能补出缺失的方向。

**结论边界：** 尚未证明真实长文本收益或大模型尺度规律；当前从零训练的小模型也尚未学会新的组合任务。

**执行动作：** 先让一个预训练小模型通过组合任务能力门槛；失败即停止，成功后才从同一检查点公平比较 NTP 与 MTP。

## 1. 当前必须回答的问题

1. 为什么这个组合任务能隔离我们关心的能力？
2. MTP 相比 NTP 已经确定多出了什么，标准头是否使用了它？
3. 为什么 MTP 可能损害标准目标，课程学习能否修复？

### 术语解释

| 术语 | 直接含义 | 本文中的具体对象 | 不能证明什么 |
|---|---|---|---|
| 标准头 | 正常自回归生成所用的下一词元预测头 | 两种训练条件共享的答案预测接口 | 辅助头好不等于标准生成好 |
| 中间状态 | 第一步计算得到、第二步必须继续使用的结果 | 第一张表得到的实体 $B$ | 能被探针读出不等于被模型使用 |
| 功能使用 | 改变中间状态会按任务规则改变标准头答案 | 对 $B$ 做反事实干预 | 真实任务一定提升 |

## 2. 最小模型与确切数据

两张表都是对全部实体的随机一一映射。起点为 $A$，第一张表产生中间实体 $B$，第二张表产生答案 $Y$：

$$
B=\pi_1(A),\qquad Y=\pi_2(B).
$$

只看第一张表不知道第二步映射；只看第二张表不知道该查哪一行；联合两张表才能作答。这对应多文档问答、知识图谱查询和代码依赖追踪中“先确定中间对象，再继续查询”的计算骨架。

**一条确切数据：**

```text
表1：v0→v2, v1→v0, v2→v3, v3→v1
表2：v0→v1, v1→v3, v2→v0, v3→v2
问题：从 v1 出发，依次查表1、表2。
中间状态：v0；答案：v1
输出：<DECIDE> <FMT_0> <ANS_v1>
```

**训练与评价：** NTP 在决策位置预测格式词元，再由下一个位置的标准头预测答案；MTP 保留这些损失，并额外从决策位置直接预测答案。最终只比较共同标准头的答案，不用辅助头准确率代替结果。

## 3. 当前回答

### 问题 1：任务是否合理？

**回答：** 数据在构造上严格要求有序组合，但当前小模型没有学会它。

**决定性证据：** 两层、宽度 64 的模型训练 3000 步后，五个种子的答案准确率为 `0.1274–0.1353`，接近 8 类机会水平 `0.125`；格式准确率为 `1.0`。

**边界：** 这否定当前模型作为目标比较载体，不否定预训练模型能学会该任务。

**来源：** [能力校准总结](../../../Projects/from-attention-to-search/main/experiments/A12/A12_03b_explicit_binding_calibration/summary.md)

### 问题 2：MTP 信息是否被使用？

**回答：** 直接信息形成已得到支持，跨位置的标准头使用尚未成立。

**决定性证据：** 首个信息性未来位置使直接更新从 `0` 打开；共享参数传递在 `5/5` 种子为正。但标准头有用性在当前位置为 `5/5` 正，在下一位置为 `0/5` 正。

**边界：** 只能说明当前受控任务中的“形成不保证使用”，不能推出一般语言模型规律。

**来源：** [信息位置](../../../Projects/from-attention-to-search/main/experiments/A11/A11_09_next_k_inclusion_law/summary.md) · [参数传递](../../../Projects/from-attention-to-search/main/experiments/A11/A11_11_k2_semantic_tangent_kernel_transmission/summary.md) · [跨位置使用](../../../Projects/from-attention-to-search/main/experiments/A11/A11_18_head_position_cross_kernel/summary.md)

### 问题 3：容量与课程怎么解释？

**回答：** 缺少独立表征方向足以造成 MTP/NTP 权衡，课程不能修复这种结构性缺失。

**决定性证据：** 线性模型只有一个方向时，MTP 的标准损失增加 `0.9084–1.0218`，但未来变量在 `5/5` 种子改善；两个方向时损害降为数值零。等辅助训练量的课程通过率为 `0/5`。

**边界：** 这是线性受控机制，不是 Transformer 参数规模定律；课程仍可能缓解容量足够时的优化路径问题。

**来源：** [表征秩总结](../../../Projects/from-attention-to-search/main/experiments/A12/A12_04_task_rank_competition/summary.md) · [课程边界](../../../Projects/from-attention-to-search/main/experiments/A12/A12_05_curriculum_rank_boundary/summary.md)

## 4. 唯一下一决策

**动作：** 用同一个预训练小模型先学习上述任务。

**要区分的解释：** 当前失败究竟来自任务接口不适合从零学习，还是该任务本身无法被小模型掌握。

**通过条件：** 完整答案准确率至少 `0.70`、格式至少 `0.99`、单表不高于 `0.20`、证据替换一致率至少 `0.90`；通过后才比较 NTP/MTP，并干预中间状态 $B$。

**停止条件：** 任一门槛失败，停止目标比较和表征干预。[待审协议](../../../Projects/from-attention-to-search/main/experiments/A12/A12_07_standard_head_causal_representation_use/protocol_cn.md)

## 5. 来源索引

- **当前研究边界：** [A11 索引](../../../Projects/from-attention-to-search/main/problem_anchors/11_informative_future_branch_mechanism/README.md) · [A12 索引](../../../Projects/from-attention-to-search/main/problem_anchors/12_structured_compositional_mtp_workload/README.md)
- **下一实验：** [标准头因果使用协议](../../../Projects/from-attention-to-search/main/experiments/A12/A12_07_standard_head_causal_representation_use/protocol_cn.md)
- **完整实验设置：** 需要精确模型、种子和干预实现时，进入上述各 `summary.md` 所链接的 `detailed.md`。
