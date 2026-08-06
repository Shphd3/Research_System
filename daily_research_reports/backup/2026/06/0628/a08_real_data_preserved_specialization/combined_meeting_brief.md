# A08 Real-Data Preserved Specialization Combined Meeting Brief

## 执行摘要

08 系列的目标是把 05/06/07 和导师主线合成一个新的研究目标：构造一种能在真实数据上初始化 specialization、并在 early training 中保持该 specialization 的 MoE gating/training 方法。这里的 specialization 需要重新定义：不是语义命名，也不是 load balance，而是稳定方向产生的 route identity 能否被初始化、保存，并最终显示功能效用。

当前 08 的主张还不是“方法已经成功”，而是一个十轮可证伪科研流程：

1. 先复现导师和 r1 的奇异方向收敛直觉；
2. 再把稳定方向转成 gate-forward 机制；
3. 再做 common projection / residual reservoir 的合成微实验；
4. 最后回到 real DCLM，测试 preservation 和 utility。

最重要的推进断言：

```text
05 解释 ordinary top-1 为什么会被 common/early feedback 干扰；
06 证明 real-DCLM proxy 可以初始化，但普通训练不能保存；
07 证明 controlled nested surface 上 update-space control 可以降低 tail absorption；
08 要把这三者合成为一个 real-data preserved specialization 方法。
```

## 导师与 r1 intuition 的正确落点

导师文档给出的物理图像是：

```text
嵌套语言结构 A -> AB -> ABC -> ABCD
-> 高频 A 先被学会
-> A 形成稳定高增益方向
-> 交叉熵仍会继续放大该方向的奇异值
-> 后来的长尾特征可能被吸收到这个方向
-> C3S 类方法要控制实际 update 中的 common-subspace 分量
```

r1 录音补充了 gating 直觉：

```text
当奇异方向基本稳定后，可以把它当成 gating forward 的固定方向；
但必须先定义什么叫 converge；
然后可以把 common projection 发给 common expert，
把 residual 发给 long-tail reservoir，
再尝试循环抽取新的 tail 方向。
```

这里的关键修正是：不要把问题说成“奇异方向先收敛、奇异值后收敛”的简单口号。更准确的说法是：

```text
方向 align 后不太能继续 align；
但只要交叉熵还有 residual loss，奇异值仍可能继续增长。
```

因此 08 的第一个任务不是发明方法，而是定义 direction convergence。

## 新的 specialization 定义

08 中 specialization 分三层，不能混用：

| 层级 | 定义 | 主指标 | 不能 claim |
|---|---|---|---|
| Initialization specialization | 稳定方向或 proxy cluster 能变成 step-0 route identity | step-0 proxy-route NMI + nuisance guards | training success |
| Preserved specialization | route identity 经 early training 后仍保持 | proxy_route_NMI@step5/10 + LM loss | functional utility |
| Functional specialization | preserved route 对学习有功能价值 | tail loss / alpha_tail / fixed-route ablation | semantic experts / scaling |

这一定义直接承接 06：

```text
A06_11 已经支持 initialization specialization；
A06_12 说明 preserved specialization 失败；
A08 的主任务是修复 preserved specialization；
A07/A08_10 才能测试 functional specialization。
```

## 05 / 06 / 07 如何串联进 08

### 05 给出失败源

05 的核心不是“step-0 common component 一定主导”，而是更窄的结论：

```text
real text step 0 common component 会影响 load；
early training 后 common margin 会快速放大；
失败更可能来自 early feedback，而不是纯初始化几何。
```

证据：A05_04_03 中 step 10 common margin 上升到 `0.7427`，dominance ratio 到 `21.7874`，raw max load 到 `0.8507`。

### 06 给出真实 bottleneck

06 的核心结果是：

```text
real-DCLM proxy clusters 可以变成 gate rows；
但普通 next-token training 会在 step 5/10 擦掉这个 partition。
```

证据：A06_11 raw-center step-0 proxy-route NMI 为 `0.7449`；A06_12 raw-center 从 step 0 `0.7549` 掉到 step 5 `0.0410`、step 10 `0.0131`。

### 07 给出 utility 的机制读数

07 的新结果说明：

```text
在 controlled nested surface 上，
common backbone 可以复现；
tail update 进入 common subspace 的比例可以被控制；
tail loss 会随之改善。
```

证据：A07_02 nested full run 中 combined control 将 tail loss 改善 `0.1075`，将 $\alpha_{\mathrm{tail}}$ 降低 `0.1204`。

但 07 也给出反例边界：A07_06 rare loss 改善但 route-level conflict 几乎不动，所以 rare loss 不能单独当机制证据。

## 十轮迭代路线

| 轮次 | Anchor | 当前问题 | 实验性质 | 主指标 |
|---:|---|---|---|---|
| 1 | A08_01 | 什么叫 singular direction converge？ | 合成机制复现 | $K_i(t)$ 低且 $G_i(t)>0$ |
| 2 | A08_02 | converged direction 能否变成 gate row？ | 合成 proxy test | feature-route NMI |
| 3 | A08_03 | common/residual split 是否保护 tail？ | 合成方法微实验 | tail loss + $\alpha_{\mathrm{tail}}$ |
| 4 | A08_04 | residual reservoir 能否循环抽取新方向？ | 合成迭代实验 | next-level alignment |
| 5 | A08_05 | real DCLM 是否有稳定方向？ | 真实机制诊断 | real direction drift |
| 6 | A08_06 | real initialization specialization 如何定义？ | 指标定义/审计 | init specialization score |
| 7 | A08_07 | early training 擦掉 proxy 的原因是什么？ | 真实失败分解 | component-attributed NMI drop |
| 8 | A08_08 | singular-converged gating 方法是否在 controlled data 上保持 partition？ | 合成方法实验 | route NMI after training |
| 9 | A08_09 | 方法能否保存 real-DCLM proxy routing？ | 真实方法实验 | proxy_route_NMI@step5/10 |
| 10 | A08_10 | 保存下来的 partition 是否有功能价值？ | 真实 utility audit | alpha_tail / ablation selectivity |

这十轮的逻辑是：

```text
先定义 converge
-> 再定义 gate-forward
-> 再定义 synthetic method mechanism
-> 再搬到 real data
-> 最后才 claim utility
```

## 首批四卡执行

首批四张 protocol 已经写好：

1. `A08_01_singular_direction_convergence_metric/protocol.md`
2. `A08_02_direction_as_gate_forward/protocol.md`
3. `A08_03_common_direction_split_reservoir/protocol.md`
4. `A08_04_iterative_reservoir_direction_discovery/protocol.md`

它们共同回答一个问题：

```text
r1 里说的“方向稳定后可以当 gating forward”是否能在 controlled synthetic 上被定义、转换、分流、迭代？
```

如果前四卡失败，08 不能进入 real-DCLM method claim；如果前四卡通过，才进入 A08_05 real-DCLM singular convergence audit。

## 当前 claim boundary

现在可以 claim：

```text
08 已经形成一条从导师奇异方向机制到 real-data preserved specialization 的可证伪研究路线。
```

现在不能 claim：

```text
新的 gating 方法已经有效；
real-DCLM preservation 已经解决；
preserved route 已经有 utility；
真实语义 expert 已经存在。
```

## 执行动作

下一步最小执行是四卡 batch：

```text
A08_01 -> A08_02 -> A08_03 -> A08_04
```

完成标准：

```text
A08_01 定义 convergence threshold；
A08_02 证明 stable direction 可变成 gate-forward row；
A08_03 证明 common/residual split 改善 tail 且机制量移动；
A08_04 证明 residual reservoir 能循环抽取新方向且不忘旧方向。
```

如果四卡通过，进入 real-DCLM：

```text
A08_05 real convergence audit
-> A08_06 real initialization specialization definition
-> A08_07 preservation failure decomposition
-> A08_08/A08_09 method
-> A08_10 utility closure
```

## Source Index

Main A08 anchors:

- `Projects/from-attention-to-search/main/problem_anchors/08_real_data_preserved_specialization/08_00_real_data_preserved_specialization_mainline_anchor.md`
- `Projects/from-attention-to-search/main/problem_anchors/08_real_data_preserved_specialization/08_01_singular_direction_convergence_metric_anchor.md`
- `Projects/from-attention-to-search/main/problem_anchors/08_real_data_preserved_specialization/08_02_direction_as_gate_forward_anchor.md`
- `Projects/from-attention-to-search/main/problem_anchors/08_real_data_preserved_specialization/08_03_common_direction_split_reservoir_anchor.md`
- `Projects/from-attention-to-search/main/problem_anchors/08_real_data_preserved_specialization/08_04_iterative_reservoir_direction_discovery_anchor.md`

First four protocols:

- `Projects/from-attention-to-search/main/experiments/A08/A08_01_singular_direction_convergence_metric/protocol.md`
- `Projects/from-attention-to-search/main/experiments/A08/A08_02_direction_as_gate_forward/protocol.md`
- `Projects/from-attention-to-search/main/experiments/A08/A08_03_common_direction_split_reservoir/protocol.md`
- `Projects/from-attention-to-search/main/experiments/A08/A08_04_iterative_reservoir_direction_discovery/protocol.md`

Evidence inputs:

- `Projects/from-attention-to-search/main/experiments/A05/A05_04_03_real_text_common_logit_audit/summary.md`
- `Projects/from-attention-to-search/main/experiments/A06/A06_11_real_dclm_proxy_center_router_initialization/summary.md`
- `Projects/from-attention-to-search/main/experiments/A06/A06_12_real_dclm_proxy_init_training_preservation/summary.md`
- `Projects/from-attention-to-search/main/experiments/A07/A07_01_nested_common_backbone_reproduction/summary.md`
- `Projects/from-attention-to-search/main/experiments/A07/A07_02_nested_tail_common_subspace_control/summary.md`
- `Projects/from-attention-to-search/main/experiments/A07/A07_06b_projected_moe_conflict_splitting/summary.md`
- `daily_research_reports/0625/docs/two_phase_singular_mode_learning_proof_and_test.md`
- `daily_research_reports/0625/docs/c3s_adamw_merged_rigorous_proof_with_negative_results.md`
- `daily_research_reports/0626/recordings/r1.md`
