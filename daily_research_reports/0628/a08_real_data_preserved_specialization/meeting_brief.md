# A08 首批四卡实验 Meeting Brief

## 一句话结论

A08 首批四卡已完成。结论是：

```text
稳定方向可以被定义，也可以变成 gate-forward route；
但 common/residual split 不是已证明的 preservation 方法；
iterative reservoir loop 当前失败。
```

承接 06 的推进断言：

```text
下一步应进入 A08_05/A08_07：
先 audit real-DCLM 是否存在稳定 singular / gate-input directions，
再分解普通训练为什么擦掉 A06 的 proxy route。
不能把 A08_03/A08_04 的 split/reservoir 当成已验证方法带到 real-DCLM。
```

## 物理先验

导师和 r1 的核心不是“方向先收敛、奇异值后收敛”的口号，而是：

```text
方向 align 后，继续 align 的空间变小；
但只要交叉熵还有 residual loss，奇异值/增益仍可能继续涨；
因此稳定方向可以作为 forward routing 轴，
但 training feedback 仍可能继续放大 common direction 并擦掉 partition。
```

08 的目标是把 06 中已经能初始化的 real-DCLM proxy route，推进到 early
training 后仍能保存。

## 四个问题和答案

| Anchor | 问题 | 答案 | 认知更新 |
|---|---|---|---|
| A08_01 | 什么叫 direction converge？ | rank-one surface 上可定义：$K$ 低、$G>0$、A alignment 高。 | “稳定方向”变成可审计指标，但 wide robustness 未证明。 |
| A08_02 | 稳定方向能否变成 gate row？ | 能。direction gate 的 feature NMI 为 `1.0000`。 | r1 的 “direction fixed -> gate forward fixed” 在 synthetic rank-one 上成立。 |
| A08_03 | common/residual split 是否保护 tail？ | 不足。tail 改善 `0.0984`，alpha 降 `0.1558`，但 random split 改善 `0.1596` 更强。 | tail loss 正信号不是机制证据；capacity guard 必须过。 |
| A08_04 | residual reservoir 能否循环抽取新方向？ | 失败。stage 2/3 next alignment 为 `-0.1928` / `-0.1023`。 | 简单 residualization 不等于 nested direction discovery。 |

## 指标含义

`K`：方向漂移。相邻 checkpoint 的 projector 距离；越低表示方向越稳定。

`G`：奇异值增量。方向稳定后若 `G>0`，说明方向不怎么转了，但增益还在涨。

feature-route NMI：route 和真实 feature sign 的一致度。越高表示 gate 真的按目标 feature 分流。

max load：最大 expert 负载。用来排除“全进一个 expert”的假 route。

`alpha_tail`：tail update 落入 common direction 的比例。越低不自动代表成功，必须和 tail loss 与 capacity guard 一起看。

tail loss：长尾层 `ABCD` 的 BCE loss。它是功能指标，但单独不能证明机制。

next-level alignment：新阶段方向对下一层 feature 的对齐，减去旧方向 overlap。正数才表示学到新方向。

## 实验流程

数据是 synthetic nested surface：

```text
A -> AB -> ABC -> ABCD
```

训练分布偏 common，评估分布按 level 平衡。这样可以观察 common direction 是否先被学到，以及 tail 是否被 common direction 吸收。

运行设置：

```text
rank-one MLP / wide guard / split-forward model
AdamW
8 seeds: 20260628-20260635
local CUDA full run
run name: a08_singular_preservation_full_20260628_2
```

## 关键结果

### A08_01 支持

```text
pass rate = 1.0000
final K = 0.0316
final G = 0.0301
A alignment = 0.7865
shuffled B alignment = 0.0218
wide pass rate = 0.5000
```

解释：A 方向稳定，同时增益还在涨。这支持导师/r1 的方向-增益分离图像。

边界：wide 条件不稳，不能说宽模型里已经有稳定可匹配方向。

### A08_02 支持

```text
direction gate NMI = 1.0000
oracle NMI = 1.0000
random equal-norm mean NMI = 0.1741
shuffled direction NMI = 0.0001
nuisance NMI = 0.0002
```

解释：稳定方向可以转成 route identity。

边界：一个 random-control seed 到 `0.5952`，所以未来要用 random-control distribution。

### A08_03 削弱

```text
CE tail loss = 0.4098
common/residual tail loss = 0.3114
common/residual tail gain = 0.0984
alpha reduction = 0.1558
capacity-random tail gain = 0.1596
```

解释：split 确实改变了学习，而且 alpha 降了；但 random split 更能降 tail loss，所以 tail 改善不能归因于 common/residual 机制。

### A08_04 失败

```text
stage 1 A alignment = 0.7819
learned stage 2 next alignment = -0.1928
learned stage 3 next alignment = -0.1023
shuffled guard = 0.0061
oracle A residual stage 2 = 0.0567
oracle A/B residual stage 3 = 0.2601
```

解释：第一层 common direction 能学到；后续 learned residual 没有抽出 B/C。循环抽取需要 stage-local objective 或更强 residual 定义。

## 与 A07_06 的关系

**问题一：A07_06 是否证明 projected MoE 方法成立？**

没有。A07_06 的 rare loss 改善是真的，但 route-level conflict 几乎没动。因此它不能证明“降低 route conflict 导致 rare loss 改善”。

**问题二：A08_03 给了什么更清晰的复现？**

A08_03 复现了同一个方法学风险：common/residual split 改善 tail loss，并且 alpha 也下降；但 capacity-matched random split 改善更大。只看 tail loss 会给 false positive。

**问题三：A07_06 现在的价值是什么？**

它是校准案例：以后任何 preservation / utility 方法都必须同时过机制指标和强 control，不能只拿 rare/tail loss 当成功证据。

## 06 主线承接

06 当前状态：

```text
A06_11: real-DCLM proxy center 可以初始化 route。
A06_12: 普通训练 step 5/10 会擦掉 route。
```

A08 首批四卡给出的推进是：

```text
direction convergence 和 gate-forward conversion 是可操作的；
但 split/reservoir 方法还不能承担 preservation。
```

因此，06 后续应推进为：

```text
A08_05: audit real-DCLM 是否存在稳定 singular / gate-input directions；
A08_06: 定义 real initialization specialization score；
A08_07: 分解 early training 哪个 update component 擦掉 proxy_route_NMI；
之后才允许 A08_08/A08_09 设计 preservation intervention。
```

## Claim Boundary

可以 claim：

```text
在 controlled rank-one nested surface 上，
稳定方向可以定义，也可以变成 gate-forward route。
```

不能 claim：

```text
common/residual split 已经是有效 preservation 方法；
iterative reservoir discovery 成立；
real-DCLM route preservation 已解决；
preserved route 已有 utility；
真实 semantic expert 已出现。
```

## 下一步

推荐下一张卡：

```text
A08_05 real-DCLM singular / gate-input convergence audit
```

最小问题：

```text
在 A06 的 real-DCLM step 0 / step 5 / step 10 窗口里，
是否存在低 drift、可 gate-forward、并且与 proxy route 有关的稳定方向？
```

如果没有，A08 应回到 proxy definition；如果有，再进入 A08_07 训练反馈擦除分解。

## Source Index

Anchors:

- `Projects/from-attention-to-search/main/problem_anchors/08_real_data_preserved_specialization/08_00_real_data_preserved_specialization_mainline_anchor.md`
- `Projects/from-attention-to-search/main/problem_anchors/08_real_data_preserved_specialization/08_01_singular_direction_convergence_metric_anchor.md`
- `Projects/from-attention-to-search/main/problem_anchors/08_real_data_preserved_specialization/08_02_direction_as_gate_forward_anchor.md`
- `Projects/from-attention-to-search/main/problem_anchors/08_real_data_preserved_specialization/08_03_common_direction_split_reservoir_anchor.md`
- `Projects/from-attention-to-search/main/problem_anchors/08_real_data_preserved_specialization/08_04_iterative_reservoir_direction_discovery_anchor.md`

Experiment records:

- `Projects/from-attention-to-search/main/experiments/A08/A08_01_singular_direction_convergence_metric/summary.md`
- `Projects/from-attention-to-search/main/experiments/A08/A08_02_direction_as_gate_forward/summary.md`
- `Projects/from-attention-to-search/main/experiments/A08/A08_03_common_direction_split_reservoir/summary.md`
- `Projects/from-attention-to-search/main/experiments/A08/A08_04_iterative_reservoir_direction_discovery/summary.md`

Runner:

- `Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/scripts/run_a08_singular_direction_preservation.py`

Raw result:

- `Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/results/a08_singular_direction_preservation/a08_singular_preservation_full_20260628_2`
