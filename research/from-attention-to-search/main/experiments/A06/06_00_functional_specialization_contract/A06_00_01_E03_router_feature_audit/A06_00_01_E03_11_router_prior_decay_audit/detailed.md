# Detailed Report: H0528a Router Prior Decay Audit

## 1. 目的

H0528a 追问 H0527a 的失败链条：

```text
为什么一个有效的 step-0 semantic routing prior 没有变成 final stable functional specialization？
```

H0527a 已证明 semantic initialization 能改变初始 routing，但 final B-context NMI 衰减，\(S_{AB}\) 没有稳定增强。H0528a 不再问 initialization 是否有效，而是判断 prior 衰减来自 representation drift、router objective drift、direction misspecification，还是 expert utility degeneracy。

## 2. Artifact Reality Check

H0527a 正式 run 保存了：

```text
final model.pt for each condition/seed
trajectory CSVs
final figures/tables
```

H0527a 没有保存：

```text
model checkpoints at steps 200, 400, 800, 1200
```

因此 H0528a 没有伪造 full checkpoint replay。实际执行的是：

```text
step 0: reconstruct initial router from seed/config
step 1600: load final model.pt
```

Per-step H0527a CSV 只作为背景，不作为 H0528a 的三-router comparison 证据。

## 3. 实验设置

Source experiment:

```text
main/experiments/H0521_router_feature_specialization/H0527a_router_initialization_trajectory/
```

Conditions:

```text
random_init
semantic_context_init
```

Seeds:

```text
20260521, 20260522, 20260523, 20260524
```

Audit split:

```text
calibration split: estimate recentered semantic router C^t
eval split: evaluate routing NMI, heatmap, load entropy, forced utility
```

This split is important: `recentered_current` is fitted on calibration hidden states and evaluated on held-out audit hidden states.

## 4. Router Variants

H0528a compares three routers on final hidden states \(h^{1600}\).

### 4.1 Frozen-init router

Reconstruct the condition-specific step-0 router:

```text
random_init: random router from seed
semantic_context_init: original whitened B-context semantic init from seed/config
```

Then apply it to final hidden states:

\[
r_{W^0}(h^{1600})
\]

This tests whether the original static boundary still works after representation drift.

### 4.2 Recentered-current router

Use final hidden states to rebuild B-context whitened directions:

\[
C^{1600}
\]

Then evaluate:

\[
r_{C^{1600}}(h^{1600})
\]

This tests whether the current representation still contains a recoverable B-context boundary.

### 4.3 Trained-final router

Use the actual trained router from `model.pt`:

\[
r_{W^{1600}}(h^{1600})
\]

This tests what the task-trained router actually uses.

## 5. Primary Metric

Primary metric:

\[
\Delta_{\text{unused}}
=
\mathrm{NMI}(r_{C^{1600}}(h^{1600}),\kappa)
-
\mathrm{NMI}(r_{W^{1600}}(h^{1600}),\kappa).
\]

Interpretation:

```text
If Delta_unused is positive and large, B-context structure is recoverable but unused by trained router.
```

## 6. Primary Result

Mean B-context NMI:

| Condition | Frozen-init | Recentered-current | Trained-final | Unused gap | Repr-drift gap |
|---|---:|---:|---:|---:|---:|
| random_init | 0.0419 | 0.2126 | 0.0452 | 0.1674 | 0.1708 |
| semantic_context_init | 0.0475 | 0.3040 | 0.0422 | 0.2618 | 0.2565 |

Per-seed semantic condition:

| Seed | Frozen-init | Recentered-current | Trained-final | Unused gap |
|---:|---:|---:|---:|---:|
| 20260521 | 0.1711 | 0.3203 | 0.1533 | 0.1669 |
| 20260522 | 0.0126 | 0.3755 | 0.0111 | 0.3644 |
| 20260523 | 0.0032 | 0.2993 | 0.0020 | 0.2973 |
| 20260524 | 0.0031 | 0.2211 | 0.0025 | 0.2186 |

Interpretation:

```text
Final hidden states still support a B-context semantic partition, because recentered-current NMI is much higher than trained-final NMI.
```

Also:

```text
The original frozen semantic init mostly becomes stale, because frozen-init NMI is much lower than recentered-current NMI.
```

## 7. Forced-Routing Utility

Forced routing uses the actual selected-gate path:

```text
gate_mode = router_prob
```

When forcing a group token to expert \(e\), the output uses:

\[
p_e(h)E_e(h)
\]

not:

\[
1 \cdot E_e(h).
\]

Therefore this is actual sparse-path utility, not pure expert-only utility.

Mean utility margins:

| Condition | B_in_B_only | B_in_AB | B_in_CB |
|---|---:|---:|---:|
| random_init | 0.0024 | 0.0060 | 0.0001 |
| semantic_context_init | 0.0095 | 0.0034 | 0.0012 |

Class-level margins:

| Condition | A-only | B-only | AB-composite | CB-composite |
|---|---:|---:|---:|---:|
| random_init | 0.0140 | 0.0024 | 0.0060 | 0.0001 |
| semantic_context_init | 0.0104 | 0.0095 | 0.0034 | 0.0012 |

Interpretation:

```text
The best expert and second-best expert have very similar forced CE for the B-context and AB groups. Under the actual selected-gate path, task loss has weak reason to preserve a fixed B-context expert assignment.
```

## 8. Figures

![Router NMI comparison](figures/router_nmi_comparison.png)

这张图说明：final hidden states 中 `recentered_current` 能恢复 B-context routing structure，但 trained router 没有使用这条 boundary。

![Unused semantic gap by seed](figures/unused_semantic_gap_by_seed.png)

这张图说明：unused semantic gap 在多数 seed 上稳定为正，semantic init condition 的 gap 更大。

![B-context routing heatmap](figures/b_context_routing_heatmap_by_variant.png)

这张图说明：recentered semantic router 的 B-context heatmap 更有结构，而 trained-final router 的 B-context 区分弱。

![Forced utility margin](figures/forced_utility_margin_heatmap.png)

这张图说明：forced routing 的 expert utility margin 很小，支持 expert utility underdetermination。

## 9. 解释链

Observed:

```text
recentered_current NMI high, trained_final NMI low.
```

Suggests:

```text
B-context semantic boundary remains recoverable in final representation, but trained router does not use it.
```

Observed:

```text
frozen_init NMI low, recentered_current NMI high.
```

Suggests:

```text
static initialization boundary becomes stale as representation changes.
```

Observed:

```text
forced utility margins are small.
```

Suggests:

```text
task loss does not strongly prefer one expert for each B-context group, so semantic assignment has weak functional attractor.
```

Final judgment:

```text
H0528a supports Case C with representation-drift component: semantic routing is recoverable, but expert utility is weakly identified under the current selected-gate task loss.
```

## 10. 结论边界

Can claim:

```text
In H0527a final checkpoints, B-context boundary is recoverable by a recentered semantic router but unused by the trained router.
```

Can claim:

```text
Under actual selected-gate forced routing, expert utility margins are small.
```

Cannot claim:

```text
The final representation lost all B-context information.
```

Cannot claim:

```text
Any new router objective or regularizer will fix the issue.
```

Cannot claim:

```text
Pure expert-only utility is also weak, because this audit used gate_mode = router_prob.
```

## 11. Artifact / Repro Map

Runner:

```text
XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/scripts/run_h0528a_router_prior_decay_audit.py
```

Config:

```text
XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/configs/h0528a_router_prior_decay_audit.json
```

Result dir:

```text
XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/results/h0528a_router_prior_decay_audit/h0528a_router_prior_decay_audit_20260524
```

Figure dir:

```text
XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/figures/h0528a_router_prior_decay_audit/h0528a_router_prior_decay_audit_20260524
```

Repro command:

```bash
python XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/scripts/run_h0528a_router_prior_decay_audit.py \
  --config XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/configs/h0528a_router_prior_decay_audit.json \
  --run-name h0528a_router_prior_decay_audit_20260524
```
