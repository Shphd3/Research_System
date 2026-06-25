# A07 三个 Anchors Meeting Brief

## 结论

三个 anchor 在 controlled synthetic D07 上都得到支持。

最重要边界：这次是 synthetic analytic audit，不是真实神经训练 checkpoint，也不是真实语料迁移。

下一步决策：选择先做 neural D07 training 版，还是直接把 A07_03 诊断迁移到真实 trained checkpoint。

## Run Snapshot

Run: `a07_common_rare_conflict_full_20260623_1`

Seeds: `20260623-20260630`, 8 seeds.

Execution: local full run with 4 logical shards. Four-card ACP submit script was prepared and dry-run recorded; no external ACP job id was created.

Raw result:
`Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/results/a07_common_rare_conflict/a07_common_rare_conflict_full_20260623_1`

## A07_01: Metric Surface 是否合法

问题：D07 和 `Delta_vs_best_null` 是否能作为后续方法测试的合法审计面？

结论：支持。

核心证据：

| Metric | Value |
| --- | ---: |
| `Delta_vs_best_null` | `0.8601 +/- 0.0008` |
| dense rare loss | `1.4399` |
| load-only rare loss | `1.5300` |
| oracle rare loss | `0.5798` |
| hidden conflict readout | `1.0000` |
| strongest shortcut | `0.5000` |

认知更新：D07 有 oracle-relievable rare conflict；后续 common-control 失败时，不能简单归因于数据面无信号。

边界：只证明 controlled synthetic audit surface 可用。

## A07_02: Common-Control 是否真的降低 Rare Interference

问题：common-control 是否比 matched load-only MoE 降低 rare loss？

结论：支持。

核心证据：

| Metric | Value |
| --- | ---: |
| `RIR_cc` | `0.9502 +/- 0.0006` |
| `FoO_cc` | `1.1049 +/- 0.0012` |
| common-control max load | `0.2500` |
| load-only max load | `0.2500` |
| phi conflict readout | `1.0000` |

认知更新：在该 synthetic surface 上，common-control 的收益不是更好 load balance，也没有擦掉 conflict signal。

边界：只证明 controlled D07 method benefit；不是真实模型鲁棒性。

## A07_03: Route Assignment 是否绑定 Expert Function

问题：A07_02 的 rare-loss 改善是否有 conflict-conditioned expert utility 支撑？

结论：支持，但必须读 modal-aligned 指标。

核心证据：

| Metric | Value |
| --- | ---: |
| selected-best rate | `1.0000` |
| chance baseline | `0.2500` |
| route-conditioned utility advantage | `0.9498-0.9502` |
| modal route probability | `1.0000` |
| modal ablation delta | `0.6800` |
| nonmodal ablation delta | `0.0000` |
| early utility advantage | `0.7408-0.7411` |

认知更新：在 synthetic D07 中，routing 不是只有 assignment 结构；它绑定了对应 expert function。

边界：expert id 跨 seed 会置换，所以 raw expert-id heatmap 只能辅助；不能 claim 稳定语义专家编号。

## Meeting Decision

建议会议只讨论一个选择：

1. 先做 neural D07 training 版：验证这三个结论是否在真实训练动态中仍成立。
2. 直接迁移 A07_03 到真实 trained checkpoint：更贴近主线，但若失败，归因会更难。

我的建议：先做 neural D07 training 版。它能把当前 synthetic analytic result 和真实 checkpoint 之间的缺口缩小一层。

## Package Map

Anchors:

- `package/anchors/07_01_common_rare_conflict_metric_audit_anchor.md`
- `package/anchors/07_02_common_controlled_rare_interference_anchor.md`
- `package/anchors/07_03_route_function_binding_anchor.md`

Experiment records:

- `package/experiments/A07/A07_01_common_rare_conflict_metric_audit/`
- `package/experiments/A07/A07_02_common_controlled_rare_interference/`
- `package/experiments/A07/A07_03_route_function_binding/`
