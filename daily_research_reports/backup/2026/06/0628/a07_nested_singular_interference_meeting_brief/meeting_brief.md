# A07 Nested Singular Interference Meeting Brief

## 执行摘要

本次更新把 A07 从旧的 common/rare 二分类冲突面，切到导师主线：语言式嵌套结构中，高频父特征先形成稳定高增益公共子空间，长尾子特征随后可能复用或被该子空间干扰。受控 rank-one 嵌套实验复现了公共子空间稳定后增益继续增长的现象，并显示抑制 tail update 进入公共子空间可以降低 tail loss。这个结果支持“更新空间里的公共子空间吸收”是更干净的机制目标，但不支持直接宣称真实 MoE utility；下一步仍应回到 06 的 preservation 主线。

当前判断：

1. A07_01 支持：嵌套 surface 复现了导师的 common backbone / late gain 机制。
2. A07_02 支持：在该受控 surface 上，common-subspace update control 降低 tail loss 和 tail update 公共子空间占比。
3. A07_03 只支持 diagnostic positive control：固定路由消融能读出 route-function binding，但真实 utility 仍依赖 06 preservation。

## 机制解释与最小模型

导师主线不是简单地说 rare feature 被 common feature 影响，而是：

```text
嵌套结构 A -> AB -> ABC -> ABCD
-> 高频 A 先形成稳定方向
-> 交叉熵继续放大该方向的奇异增益
-> 长尾 ABCD 的更新可能继续落入 A 的公共子空间
-> 如果这种复用阻止子特征方向形成，就成为干扰
```

核心对象：

| 记号 | 含义 | 回答的问题 |
|---|---|---|
| $P_C$ | 公共父特征 $A$ 的冻结投影子空间 | common backbone 是否存在 |
| $\delta_C$ | $P_C$ 随训练漂移多少 | common backbone 是否稳定 |
| $S_C$ | 模型权重在 $P_C$ 里的能量 | 稳定方向是否继续被放大 |
| $\alpha_{\mathrm{tail}}$ | tail update 落入 $P_C$ 的比例 | 长尾是否被公共子空间吸收 |
| tail loss | $ABCD$ 的损失 | 控制是否真的改善长尾学习 |
| ablation selectivity | 消融 routed expert 后的选择性伤害 | route 是否绑定功能 |

数据构造：

```text
A, AB, ABC, ABCD 四层嵌套。
训练频率为 [4096, 1024, 256, 64]。
评估每层 1024 个样本，保持 balanced。
标签由父特征符号和子特征修正共同决定，child-only shortcut 单独不能解决 tail。
```

模型边界：

这次使用 `hidden_dim=1` 的受控 rank-one hidden 模型，是为了贴近导师 two-phase singular-mode proof。它不是 wide MLP，不是 transformer，也不是真实语言模型。

## 主要结果

结论：A07 的机制链条在受控 rank-one 嵌套 surface 上成立，但它只提供 07 utility 的机制目标，不替代 06 preservation。

### 1. 高频父特征形成稳定公共子空间，并且该方向继续增益增长。

机制对齐：A07_01 检查导师的第一段机制，即 $A$ 是否先形成稳定 $P_C$，并在稳定后继续增益增长。

证据：8 seeds full run `a07_nested_full_20260628_2` 中，stable-late-gain pass rate 为 `1.0000`，post-warmup max drift $\delta_C$ 为 `0.1373`，late gain $S_C(T)-S_C(T_0)$ 为 `1.5115`，final $A$ accuracy 为 `1.0000`，final $ABCD$ accuracy 为 `0.8768`。

解释：这说明频率偏斜的嵌套结构确实能产生导师描述的 common backbone。balanced-frequency guard 的 true-$A$ alignment 只有 `0.2121`，说明这个现象不是普通 balanced learning 自动出现的。

边界：这只是在 rank-one 受控 surface 上复现机制，不说明真实语言模型一定同样发生。

来源：`Projects/from-attention-to-search/main/experiments/A07/A07_01_nested_common_backbone_reproduction/summary.md`

### 2. 抑制 tail update 的公共子空间分量可以降低 tail loss。

机制对齐：A07_02 检查导师的第二段机制，即 tail 是否被 $P_C$ 吸收，以及控制 update 是否能改善长尾。

证据：combined control 相比 CE/AdamW 将 tail loss 从 `0.3947` 降到 `0.2872`，改善 `0.1075`；同时 $\alpha_{\mathrm{tail}}$ 从 `0.1387` 降到 `0.0183`，降低 `0.1204`；common loss regression 为 `0.0265`，低于 guard `0.05`。

解释：confidence gate only 能改善 tail loss 但不降低 $\alpha_{\mathrm{tail}}$；subspace suppression only 能降低 $\alpha_{\mathrm{tail}}$ 并改善 tail loss。combined control 同时利用两者，所以效果最强。

边界：这不是完整 C3S-AdamW，也不是 transformer block 级别结果；它只证明这个机制在受控 rank-one surface 上可操作。

来源：`Projects/from-attention-to-search/main/experiments/A07/A07_02_nested_tail_common_subspace_control/summary.md`

### 3. 路由功能绑定诊断可用，但真实 MoE utility 仍然不能升级。

机制对齐：A07_03 检查 route-function binding，也就是专家不是只接收某类样本，而是真的对该类样本有功能。

证据：oracle nested route 的 fixed-route ablation selectivity 为 `0.5699`，route utility 为 `0.1746`；random load-matched route 的 selectivity 只有 `0.0107`。

解释：固定路由消融能读出“该专家是否真的有对应功能”。这说明诊断工具可用。

边界：oracle route 是手工给的正控，不是 learned top-1 route；因此它不能证明真实 MoE expert specialization。

来源：`Projects/from-attention-to-search/main/experiments/A07/A07_03_nested_route_function_binding/summary.md`

## 与 A07_06 的关系

### 问题一：A07_06 是否证明 projected MoE works？

答案：没有。A07_06 的 full method rare loss 确实 beat dense，但 routing-weighted conflict 几乎没降：vs random 只降 `0.0036`，vs centered 只降 `0.0010`。所以它不能说明“路由降低冲突导致 rare loss 改善”。

认知更新：rare loss 正信号不能单独作为机制证据。必须同时看到机制量移动。

### 问题二：A07_06 的 rare loss 改善可能来自哪里？

答案：新的 A07_02 提供了更合理解释：改善更可能来自 update-space control 或 confidence gating，而不是 route-level conflict splitting。A07_02 中 $\alpha_{\mathrm{tail}}$ 随 tail loss 一起下降，这是比 A07_06 的 route conflict 更贴近导师主线的机制量。

认知更新：A07 的核心指标应从“route overlap / weighted conflict”上移到“tail update 落入公共子空间的比例”。

### 问题三：A07_06 还保留什么价值？

答案：A07_06 是一个失败校准案例。它告诉我们：方法看起来改善 rare loss 时，仍然可能没有打中原先声称的机制。

认知更新：之后所有 A07 method run 都需要三件事同时成立：

```text
tail loss 改善
机制量移动，例如 alpha_tail 降低
common / LM loss 不明显回退
```

## 承接 06 主线的推进断言

A07 的新结果不改变当前主瓶颈：真实主线仍然是 06 preservation。

推进断言：

```text
06 要先证明 route/proxy partition 能在早期训练中保存；
07 再问保存下来的 partition 是否降低 update-space tail absorption 或具有 causal expert utility。
```

因此，A07 给 06 的新增要求不是“直接证明专家有用”，而是定义了 preservation 之后应该审计什么：

1. 保留的 route partition 是否让 tail update 更少进入 $P_C$；
2. 保留的 route partition 是否降低 tail loss；
3. 保留的 route partition 是否在 fixed-route ablation 中显示选择性功能。

下一步执行动作：

```text
回到 real-DCLM early-preservation / anti-feedback protocol。
主指标仍是 proxy_route_NMI@step5/10 + LM loss guard。
新增 A07-derived guard：若 preservation 成功，再测 alpha_tail、tail loss 和 fixed-route ablation selectivity。
```

完成标准：

```text
如果 proxy_route_NMI@step5/10 不能保存，A07 utility 不进入真实主线。
如果 preservation 保存成功，再用 A07_02/A07_03 的机制读数判断功能价值。
```

## Evidence Index

| Evidence | Role |
|---|---|
| `A07_01_nested_common_backbone_reproduction/summary.md` | common backbone 复现 |
| `A07_02_nested_tail_common_subspace_control/summary.md` | update-space control 支持 |
| `A07_03_nested_route_function_binding/summary.md` | route-function diagnostic 正控 |
| `A07_06b_projected_moe_conflict_splitting/summary.md` | rare loss 与 route-conflict 不一致的校准案例 |
| `A06_12_real_dclm_proxy_init_training_preservation/summary.md` | 当前 06 preservation bottleneck |

## Source Index

Anchor sources:

- `Projects/from-attention-to-search/main/problem_anchors/07_features_overlap/07.md`
- `Projects/from-attention-to-search/main/problem_anchors/07_features_overlap/07_01_common_rare_conflict_metric_audit_anchor.md`
- `Projects/from-attention-to-search/main/problem_anchors/07_features_overlap/07_02_common_controlled_rare_interference_anchor.md`
- `Projects/from-attention-to-search/main/problem_anchors/07_features_overlap/07_03_route_function_binding_anchor.md`
- `Projects/from-attention-to-search/main/problem_anchors/07_features_overlap/07_06_projected_common_rare_conflict_splitting_anchor.md`

Experiment sources:

- `Projects/from-attention-to-search/main/experiments/A07/A07_01_nested_common_backbone_reproduction/protocol.md`
- `Projects/from-attention-to-search/main/experiments/A07/A07_01_nested_common_backbone_reproduction/summary.md`
- `Projects/from-attention-to-search/main/experiments/A07/A07_01_nested_common_backbone_reproduction/detailed.md`
- `Projects/from-attention-to-search/main/experiments/A07/A07_02_nested_tail_common_subspace_control/protocol.md`
- `Projects/from-attention-to-search/main/experiments/A07/A07_02_nested_tail_common_subspace_control/summary.md`
- `Projects/from-attention-to-search/main/experiments/A07/A07_02_nested_tail_common_subspace_control/detailed.md`
- `Projects/from-attention-to-search/main/experiments/A07/A07_03_nested_route_function_binding/protocol.md`
- `Projects/from-attention-to-search/main/experiments/A07/A07_03_nested_route_function_binding/summary.md`
- `Projects/from-attention-to-search/main/experiments/A07/A07_03_nested_route_function_binding/detailed.md`

Code sources:

- `Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/scripts/run_a07_nested_singular_interference.py`
- `Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/configs/a07_nested_singular_interference.json`

## Backup Material

重要图：

![A07_01 common backbone curves](../../../../../../Projects/from-attention-to-search/main/experiments/A07/A07_01_nested_common_backbone_reproduction/figures/a07_01_backbone_curves.png)

![A07_02 tail control results](../../../../../../Projects/from-attention-to-search/main/experiments/A07/A07_02_nested_tail_common_subspace_control/figures/a07_02_control_results.png)

![A07_03 route binding](../../../../../../Projects/from-attention-to-search/main/experiments/A07/A07_03_nested_route_function_binding/figures/a07_03_route_binding.png)
