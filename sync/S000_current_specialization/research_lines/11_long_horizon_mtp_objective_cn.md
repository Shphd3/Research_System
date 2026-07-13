# 11 Long-Horizon MTP Objective：当前机制边界

## 当前结论

这条线仍是 supporting objective line，不进入 Router 方法设计。

最新 anchor 链给出三个层级不同的结果：

1. **神经序列任务 gate 未通过。** A11_23 的深度/训练时长/宽度阶梯全部停在机会水平；最强 `3L-128d-3000` 的 train accuracy 为 `0.1249`。A11_23b 的显式 pair-token 修复在五 seed test 上为 `0.1274--0.1353`。
2. **线性低秩机制得到受控支持。** A11_24 中，rank 1 的 MTP-minus-NTP 标准损失 gap 为 `0.9084--1.0218`，同时未来因子 MSE 在 `5/5` 改善；rank 2 的 gap 消失到数值零。
3. **课程不能修复结构性缺秩。** A11_25 的等辅助剂量课程 Pareto pass 为 `0/5`；rank 2 下静态与课程均接近零损失。

因此当前可以声称：结构性表示秩竞争在 oracle-factor 线性模型中成立。不能声称：同一机制已经解释小/大 Transformer、真实语言 MTP、课程预训练收益或 Router。

## Anchor 状态

| Anchor | 状态 | 当前边界 |
|---|---|---|
| A11_22 | insufficient | 一阶有限差分公式数值成立，但任务未校准 |
| A11_23 | weakened | 深度、时长、宽度修复均失败 |
| A11_23b | weakened | 显式绑定修复仍近机会水平 |
| A11_24 | supported, controlled only | rank competition 仅在线性模型成立 |
| A11_25 | weakened as structural repair | 不否定神经非凸/有限预算课程收益 |
| A11_26 | parked | neural task gate 未通过，禁止 real/scale transfer |

Router 明确 parked。

## 唯一下一决策

选择一个已有两跳能力的预训练小模型或显式结构化 neural bridge，先通过 held-out task gate，再测任务相关 Jacobian rank、安全更新比例和标准主头 MTP/NTP 差异。未通过前不进入真实 benchmark、尺度律或 Router。

## Source Paths

```text
Projects/from-attention-to-search/main/stories/11_long_horizon_mtp_objective/02_mtp_interference_capacity_curriculum_cn.md
Projects/from-attention-to-search/main/experiments/A11/A11_23_composition_calibration/summary.md
Projects/from-attention-to-search/main/experiments/A11/A11_23b_explicit_binding_calibration/summary.md
Projects/from-attention-to-search/main/experiments/A11/A11_24_task_rank_competition/summary.md
Projects/from-attention-to-search/main/experiments/A11/A11_25_curriculum_rank_boundary/summary.md
Projects/from-attention-to-search/main/problem_anchors/11_long_horizon_mtp_objective/11_26_scale_real_transfer_gate_anchor_cn.md
```
