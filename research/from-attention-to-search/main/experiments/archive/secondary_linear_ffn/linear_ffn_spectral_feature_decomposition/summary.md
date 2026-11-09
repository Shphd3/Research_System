# Result Summary: linear_ffn_spectral_feature_decomposition

Anchor: [03_hierarchical_route_utility_binding_anchor.md](../../../../problem_anchors/06_geometry_proxy_preservation/06_00_functional_specialization_contract/06_00_functional_specialization_contract_anchor.md)

Story: 不改模型，只在 recovery full run 保存的 trained $W$ 上做 spectral decomposition，判断 tail failure 是被高频方向干扰，还是 tail component 本身没写进去。

## 0. Closure Summary

目的：

在已有 linear FFN 机制上做 post-hoc audit：top-r subspace、spectral truncation、oracle feature projection。

结论：

结果更支持 “tail feature 主要没被写进 $W$”，而不是 “tail 已经写入但被高频/common top directions 污染”。Zipf-normal 下，tail-tail oracle component 明显弱；remove top directions 对 tail error 的改善很小，不足以作为主要机制。

关键证据：

| Condition | Head->Head Fro Ratio | Tail->Tail Fro Ratio | Head Own Unique MSE | Tail Own Unique MSE |
| --- | ---: | ---: | ---: | ---: |
| uniform_normal | 0.0677 | 0.0666 | 0.00063 | 0.00064 |
| zipf_normal | **0.2869** | **0.0219** | **0.00010** | **0.00254** |
| zipf_reweight | 0.0676 | 0.0661 | 0.00062 | 0.00066 |

Zipf-normal tail unique MSE under spectral truncation:

| r | full W | W_top(r) | W_low(r) |
| ---: | ---: | ---: | ---: |
| 8 | 0.00318 | 0.00397 | 0.00312 |
| 16 | 0.00318 | 0.00401 | 0.00308 |
| 32 | 0.00318 | 0.00402 | 0.00307 |
| 64 | 0.00318 | 0.00390 | 0.00319 |
| 128 | 0.00318 | 0.00348 | 0.00361 |

解释：

`W_low` 在 r=8/16/32 对 tail 有非常小的改善，但量级有限；如果 tail 失败主要是被 high-frequency top subspace 污染，remove top 应该显著改善 tail。这里没有出现。相反，`P_tail_key W P_tail_value` 自身弱，说明 tail mapping 没有被充分学进去。

结论边界：

这是 linear FFN/KV toy 的 post-hoc 结论，不直接证明 Transformer router failure。但它把机制边界收窄了：Zipf 的主要效应不是“tail 已经学会但被污染”，而是“训练目标把容量/谱能量优先分配给 common/head，tail 写入不足”。

## Key Figures

![Zipf spectral truncation](figures/spectral_truncation_error_zipf_normal.png)

支持：`W_low` 没有显著降低 tail error；top-only 对 tail 也不好。

![Zipf oracle projection](figures/oracle_projection_energy_zipf_normal.png)

支持：Zipf-normal 下 head->head component 强，tail->tail component 弱。

![Uniform oracle projection](figures/oracle_projection_energy_uniform_normal.png)

对照：uniform 下 head/tail own components 更平衡。

![Reweight oracle projection](figures/oracle_projection_energy_zipf_reweight.png)

对照：reweight 把 tail-tail component 拉回 uniform 附近。

## Claim Update

Supported:

- Zipf 下 head feature 被强写入 $W$，tail feature 写入不足。
- Inverse-frequency reweight 能恢复 tail component。
- top-r / decomposition 比 top-1 更可靠；top-1 不能单独决定机制。

Weakened:

- “tail 失败主要因为被高频 value 污染”没有得到强支持。

Next decision:

如果回到 MoE/router，应该优先测试 frequency-balanced objective 或 tail-write-in pressure，而不是只做 remove-top/common-residual。
