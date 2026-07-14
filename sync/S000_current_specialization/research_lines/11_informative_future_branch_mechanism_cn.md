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

来源：[A11 索引](../../../Projects/from-attention-to-search/main/problem_anchors/11_informative_future_branch_mechanism/README.md) · [A11 故事](../../../Projects/from-attention-to-search/main/stories/11_informative_future_branch_mechanism/01_informative_future_branch_signal_and_use_boundary_cn.md)
