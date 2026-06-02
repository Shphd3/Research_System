---
parent_node: problem.moe_expert_specialization
---

# Hierarchical Route-Utility Binding Under Compositional Features

## Report Summary

父问题：

```text
Edge-side MoE swapping needs feature-level expert specialization: common/shared computation should be resident, and long-tail/unique computation should be dynamically routed.
```

当前子问题：

```text
在已有 multi-B slot-context synthetic 中，ordinary flat top-1 MoE 已经证明 slot 信息可见但 routing 不稳定。两级 Hierarchical Common-Unique MoE 是否能让 common/token-identity component 与 slot/unique predictive component 分开，从而恢复 route-utility binding？
```

为什么要问这个问题：

```text
学长主线已经说明：Zipf feature 会诱导 hot/cold expert locality，load balance 会抹平这种 locality；H-MoE 在真实任务上保持建模能力并给出系统侧 swapping 收益。
但这还没有证明 H-MoE 的 gating 真的解决了我们观察到的 multi-B route-function binding failure。
导师建议：先试 hierarchical 方法，看原来的 gating 问题是否不存在；再用 uniform 数据集验证问题是否由 Zipf 引起。
```

决策问题：

```text
下一步应该继续调 flat router / context init，还是把研究线转向 hierarchical/common-residual gating 作为解决普通 top-1 routing failure 的核心机制？
```

任务构造：

```text
复用上次 multi-B slot-context setup：same B identity 在不同 slot 下有不同 target；slot/context feature 是 target 所需信息，B identity/common component 是干扰项。
比较 flat MoE 与 two-level H-MoE / common-residual router。
先跑 uniform 数据；若 uniform 已改善，再加 Zipf stress。
```

当前结果 / 预期结果：

```text
已有结果 1：multi-B 中 slot probe 和 oracle 都接近 1，但 flat top-1 learned routing 不能稳定绑定 slot 与 utility-best expert。
已有结果 2：uniform 64-B active-compute-matched 对照中，common_flat 平均优于 flat_top1；但 hierarchical_common 没有稳定超过 common_flat。
已有结果 3：random-init 对照中，NTP 仍能学会 target，但 route-slot NMI 明显下降；高 Assign-Utility 可以由 utility-best path collapse 产生，不等于形成清晰 slot experts。
已有结果 4：linear FFN/KV toy 支持 frequency-induced head-feature anisotropy；Zipf-normal 先学 head unique feature，tail error 被拉高，inverse-frequency reweight 能把谱和 head/tail error 拉回 uniform 附近。
已有结果 5：linear FFN spectral decomposition 显示 Zipf tail failure 主要是 tail component 没写进 $W$；remove-top / W_low 只带来很小 tail 改善，P_tail_key W P_tail_value 明显弱。
当前更新：common path 是值得保留的候选机制；两层 group/common hierarchy 本身还不能作为已支持的核心解决方案；更小的上游机制应写成 frequency-driven head write-in / tail write-in failure，而不是直接写成 H-MoE works。
```

结论边界：

```text
这个 anchor 只判断 H-MoE/common-residual gating 是否解决受控 NTP synthetic 中的 route-function binding failure。
它不能证明真实语料 feature-level specialization，也不能证明端侧系统收益；那些属于学长 story 已经部分覆盖、后续需要联合验证的部分。
```

下一步：

```text
先不要继续加 hierarchy 深度。
下一步应先做 router-factor attribution：区分 common component、head-frequency unique component、B identity、slot/target feature 到底哪个在控制 routing logits。
同时要检查 rare/tail feature 是否进入 expert function；如果 tail component 根本没写进专家，单纯 remove-top/common-residual 不能解决。
只有确认 router 主要被 common component 控制时，common-residual leaf router 才是最直接干预；如果主要是 head-frequency / tail-write-in failure，则应优先考虑 reweight、tail-write-in pressure 或 frequency-balanced diagnostic。
```

## 1. Problem Definition

Broader question:

```text
What is feature-level expert specialization, and how can MoE routing form it under NTP rather than merely route by token identity or load balance constraints?
```

Sharper question:

```text
Does Hierarchical Common-Unique routing fix the failure where slot/context information is visible and useful, but flat top-1 routing does not bind that feature axis to utility-best experts?
```

What we do not need to do now:

```text
Do not prove full H-MoE deployment gain.
Do not move immediately to real corpus.
Do not treat expert load skew alone as specialization.
Do not define specialization by surface token identity.
```

Operational definitions:

```text
feature: a contextual predictive factor that changes next-token distribution.
common component: high-frequency or token-identity/shared component that many samples use.
unique/slot component: context-specific component needed to disambiguate target under same B identity.
route-utility binding: selected expert/path is both aligned with feature and causally useful for that feature's prediction.
```

## 2. Physical Priors

```text
1. NTP hidden state at a routed position is compositional: it contains token identity, context/slot feature, and other common predictive features.
2. Feature frequency is often non-uniform and hierarchical, but even uniform multi-B can expose route-function binding failure.
3. Ordinary flat top-1 routing can read a dominant component without guaranteeing that selected experts become functionally useful for the target-deciding feature.
4. H-MoE is meaningful only if common/shared computation is separated from unique/leaf routing, not merely because it has more routers.
```

## 3. Mechanistic Motivation

Previous anchor showed:

```text
slot information is visible in h_B;
oracle slot routing works;
but learned flat routing is unstable in multi-B.
```

This suggests the failure is not simply missing information. It may be a binding failure:

```text
h_{i,s} = c_i + beta u_s + epsilon
```

where `c_i` is B identity / common component and `u_s` is slot predictive component. Flat router sees both at once and may route by the wrong component or learn utility collapse.

H-MoE hypothesis:

```text
top/common path absorbs c_i / shared computation;
leaf/group router is forced or biased to bind u_s to a smaller expert path;
therefore route-feature alignment and forced expert utility should improve together.
```

Current evidence refines this hypothesis:

```text
common path may help, but adding a second routing level does not by itself guarantee route-utility binding.
The next sharper mechanism is not "hierarchy is enough"; it is "router should not be controlled by dominant common/B-identity/head-frequency directions when the target-deciding feature is slot/unique."
Random-init shows that NTP alone does not reliably recover the slot-specialized routing seen under semantic slot-centroid init.
Linear FFN/KV toy shows frequency imbalance alone can create head-feature anisotropy and tail underfitting, even without MoE or slot.
```

## 4. Mathematical Modeling

Flat routing:

$$
r = \arg\max_e W_e h_{i,s}, \qquad h_{i,s}=c_i+\beta u_s+\epsilon.
$$

H-MoE / common-unique routing:

$$
y = f_{common}(h) + f_{leaf, r_s}(h),
$$

with either:

$$
r_s = \arg\max_j R_j h
$$

or a common-residual variant:

$$
h_{res}=h-P_{common}(h), \qquad r_s=\arg\max_j R_j h_{res}.
$$

The 0528 experiment used active-compute-matched variants:

$$
y_{\mathrm{flat}} = p_e f_e(h),
$$

$$
y_{\mathrm{common\_flat}} = f_{\mathrm{global}}(h)+p_j f_{\mathrm{leaf},j}(h),
$$

$$
y_{\mathrm{hier}} =
f_{\mathrm{global}}(h)+p_g f_{\mathrm{group},g}(h)+p_g p_{\ell|g} f_{\mathrm{leaf},g,\ell}(h).
$$

Primary metrics:

```text
route-slot NMI
route-B identity NMI
forced expert loss / ablation utility matrix
assignment-utility agreement
final CE / target accuracy
expert load health
```

A model supports specialization only if route-slot NMI and forced-loss diagonal improve together.

## 5. Computational Realization

### 5.1 Workflow Interface

Input:

```text
Existing multi-B synthetic data:
slot context + B_i -> target pi_s(B_i)
```

Models:

```text
A. flat top-1 MoE baseline
B. common_flat: global common expert + one-level leaf top-1 router
C. hierarchical_common: global common + selected group common + two-level leaf router
D. next candidate: common-residual leaf router, where leaf router uses h - P_common(h)
```

Output:

```text
Table comparing route-slot NMI, route-B NMI, Assign-Utility, forced-loss diagonal, CE/accuracy, expert load.
```

### 5.2 Minimal Computational Test

Core  test:

```text
completed 0528:
uniform 64-B + A_long/B_long:
flat_top1 vs common_flat vs hierarchical_common, 4 seeds, 3000 steps.
```

Result:

```text
common_flat is the strongest current variant.
hierarchical_common does not show a stable advantage over common_flat.
```

Next minimal test:

```text
common_flat vs common_residual_leaf_router on 64-B and 256-B.
Only if that supports route-utility binding should Zipf stress be added.
```

## 6. Minimal Falsifiable Test

Supported if:

```text
common/hierarchical/common-residual routing improves Assign-Utility, slot-B route consistency, and forced/ablation utility alignment over flat baseline while keeping CE/accuracy comparable.
```

Weakened if:

```text
common/hierarchy only improves loss or route heatmaps, but does not improve assignment-utility binding.
```

Refuted for this mechanism if:

```text
hierarchy/common-residual behaves like flat routing: slot is visible, oracle works, but learned routing still does not bind slot to utility-best path.
```

## 6.1 Current Evidence

Experiment:

```text
Projects/from-attention-to-search/main/experiments/hierarchical_route_utility_binding/summary.md
Projects/from-attention-to-search/main/experiments/hierarchical_route_utility_binding/detailed.md
```

Setup:

```text
uniform 64-B
4 slots / 4 leaf paths
active FFN width = 256 for all compared models
semantic slot-centroid init
3000 full NTP steps
4 seeds
```

Main result:

| Condition | Model | Assign-Utility | Slot-B Consistency | Route-Slot NMI | Target Acc |
|---|---|---:|---:|---:|---:|
| A_long | flat_top1 | 0.935 | 0.948 | 0.883 | 1.0 |
| A_long | common_flat | **0.952** | 0.951 | 0.883 | 1.0 |
| A_long | hierarchical_common | 0.932 | **0.968** | 0.853 | 1.0 |
| B_long | flat_top1 | 0.880 | 0.912 | 0.689 | 1.0 |
| B_long | common_flat | **0.918** | **0.921** | **0.787** | 1.0 |
| B_long | hierarchical_common | 0.878 | 0.900 | 0.727 | 1.0 |

Interpretation:

```text
common_flat modestly improves route-utility binding, especially in B_long.
hierarchical_common is not a stable improvement; it helps one B_long seed but loses on others.
Therefore "structural hierarchy alone fixes binding" is weakened.
```

Random-init control:

| Condition | Model | Assign-Utility | Route-Slot NMI | Slot-B Consistency |
|---|---|---:|---:|---:|
| A_long | flat_top1 | 0.795 | 0.450 | 0.819 |
| A_long | common_flat | 0.911 | 0.536 | 0.908 |
| A_long | hierarchical_common | 0.952 | 0.237 | 0.954 |
| B_long | flat_top1 | 0.690 | 0.174 | 0.756 |
| B_long | common_flat | 0.948 | 0.058 | 0.964 |
| B_long | hierarchical_common | 0.835 | 0.078 | 0.834 |

Interpretation:

```text
Without semantic initialization, route-slot NMI is much lower.
Some high Assign-Utility values are caused by utility-best paths collapsing to a common path, not by slot-specialized experts.
Therefore Assign-Utility must be read together with route-slot NMI and utility heatmaps.
```

## 6.2 Linear FFN Frequency-Anisotropy Evidence

Experiment:

```text
Projects/from-attention-to-search/main/experiments/linear_ffn_frequency_anisotropy/summary.md
Projects/from-attention-to-search/main/experiments/linear_ffn_frequency_anisotropy/detailed.md
```

Setup:

```text
linear FFN / KV toy
x = k_c + k_{u_i} + noise
y = v_c + v_{u_i}
conditions: uniform_normal, zipf_normal, zipf_reweight
5 seeds, 5000 steps
4-GPU ACP full run: pt-98tw742y
```

Main result:

| Step | Condition | Top Energy | Effective Rank | Tail/Head Full MSE | Head Key Align | Head Value Align |
|---:|---|---:|---:|---:|---:|---:|
| 1000 | uniform_normal | 0.0174 | 142.9 | 1.04 | 0.036 | 0.092 |
| 1000 | zipf_normal | **0.0316** | **108.6** | **32.32** | **0.099** | **0.177** |
| 1000 | zipf_reweight | 0.0174 | 142.5 | 1.05 | 0.035 | 0.085 |
| 5000 | uniform_normal | 0.0175 | 142.9 | 1.02 | 0.036 | 0.094 |
| 5000 | zipf_normal | **0.0314** | **108.9** | **33.12** | **0.095** | **0.171** |
| 5000 | zipf_reweight | 0.0174 | 142.6 | 1.06 | 0.036 | 0.093 |

Interpretation:

```text
Frequency imbalance is sufficient to create head-feature dominant anisotropy in a minimal linear model.
Inverse-frequency reweight removes most of this effect.
Top-1 was insufficient: subspace analysis shows common mode enters top-r subspace, while head unique directions enter earlier and stronger than tail.
This supports a frequency-driven high-energy subspace allocation story, not a pure top-1 story.
```

Post-hoc spectral decomposition:

```text
Projects/from-attention-to-search/main/experiments/linear_ffn_spectral_feature_decomposition/summary.md
Projects/from-attention-to-search/main/experiments/linear_ffn_spectral_feature_decomposition/detailed.md
```

Main result:

| Condition | Head->Head Fro Ratio | Tail->Tail Fro Ratio | Head Own Unique MSE | Tail Own Unique MSE |
|---|---:|---:|---:|---:|
| uniform_normal | 0.0677 | 0.0666 | 0.00063 | 0.00064 |
| zipf_normal | **0.2869** | **0.0219** | **0.00010** | **0.00254** |
| zipf_reweight | 0.0676 | 0.0661 | 0.00062 | 0.00066 |

Interpretation:

```text
Zipf-normal writes head feature strongly but tail feature weakly.
W_low / remove_top does not significantly reduce tail error, so the stronger diagnosis is tail write-in failure rather than high-frequency value interference.
Reweight restores the tail component.
```

## 7. Claim Boundary And Next Decision

If supported:

```text
Claim: common-residual routing is a plausible mechanism for solving flat top-1 route-function binding failure in controlled NTP feature specialization.
Next: add Zipf feature frequencies and test whether common path protects long-tail leaf specialization.
```

If weakened/refuted:

```text
Claim: structural hierarchy alone is insufficient; need explicit routing objective, route-neutral representation, or auxiliary route-function binding loss.
Next: return to router objective rather than architecture.
```

Current decision after 0528:

```text
Do not claim H-MoE has solved the gating problem.
Keep common path as a candidate.
Do not continue architecture depth before the factor attribution question is sharper.
The next diagnostic should separate common component, head-frequency unique component, B identity, and slot/target feature in router inputs.
Also check whether rare/tail features are written into expert functions at all before attributing failure to route-time interference.
If testing true hierarchy later, explicitly set root group to B-family/B-cluster and leaf to slot; merely increasing hierarchy depth is not enough.
```
