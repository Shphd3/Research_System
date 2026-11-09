# R4 Attention-Output Router Retrieval

R4 是 R3 的支线：把 router 输入从 block1 residual hidden 改成 block1 attention output，不含 residual，检查这种更接近 attention 汇聚信号的表示是否能形成更有用的 reverse index。

核心文件：

- `purpose_card.md`: 实验目的和假设边界。
- `execution_plan.md`: 运行配置、对比组、指标。
- `summary.md`: 跑完后的简短结论。
- `detailed.md`: 更完整的表格和失败分析。
- `figures/`: 汇报图。

