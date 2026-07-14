# 11 信息性未来分支机制

## 回答的问题

当紧邻词元不含分支信息、稍后词元首次包含分支信息时，MTP 相比 NTP 在当前位置多出什么？

## 数据与结论

两个分支共享当前位置和紧邻词元，只在稍后的分支词元不同：

```text
<DECIDE> <SHARED> <BRANCH_0>
<DECIDE> <SHARED> <BRANCH_1>
```

结果支持三个连续判断：

1. 预测范围首次覆盖包含分支变量的新词元时，当前位置出现 NTP 同位置没有的直接一阶更新；没有新信息的位置不给直接增量。
2. 多个信息性目标的作用取决于输出更新方向是否一致：一致时增强，冲突时削弱。
3. 该信号能到达共享参数，但当前位置形成的信息不保证在下一个位置仍对共同标准头有用。

## 边界与状态

这是一条稳定的目标机制基线，没有活动实验。它不证明长文本组合、树推理、模型尺度规律、课程收益或真实任务迁移。结构化功能使用由 A12 负责。

## 当前父锚点链

1. `11_01`：判定哪些未来位置真正给当前位置增加信息，以及多个目标方向何时增强或抵消。
2. `11_02`：判定当前位置的一阶信号能否通过共享参数形成实际更新。
3. `11_03`：界定当前位置形成信息与后续标准头实际使用之间的缺口。

这三步已经构成完整的稳定结论链；旧的局部诊断已降为各父锚点下的控制证据或实验归档，不再作为并列主线。

来源：[A11 索引](../../../Projects/from-attention-to-search/main/problem_anchors/11_informative_future_branch_mechanism/README.md) · [A11 故事](../../../Projects/from-attention-to-search/main/stories/11_informative_future_branch_mechanism/01_informative_future_branch_signal_and_use_boundary_cn.md)
