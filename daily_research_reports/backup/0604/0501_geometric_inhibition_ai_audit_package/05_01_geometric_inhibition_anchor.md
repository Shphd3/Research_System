# 05_01_geometric_inhibition_anchor.md

## 0. Thinking Card

当前 05_01 只保留一个当前主线问题：

> **center separation 是否能帮助 top-1 MoE router 形成非坍缩的 feature-level routing；以及在说 feature 之前，router 实际绑定的是 `slot`、$B_i$，还是 `(slot,B_i)`？**

当前定义：

```text
geometric inhibition = router center separation only
```

不再把 supervised token-margin / slot-assigned margin 作为当前 05_01 claim。旧 H0603a 中的 supervised slot-assigned margin 只能作为历史背景：它说明外部指定 assignment 时可以构造 routing stabilization，但它不回答当前 label-free / center-only 问题。

Current result:

1. H0603b / center-only diagnostics：center separation alone 不能决定 token assignment；router centers 分开不等于 feature specialization。
2. H0604a：同一 tentative feature key `(slot,B_i)` 可以稳定 route 到同一 expert，但 FeatureKeyConsistency 不能区分 specialization 与 collapse。
3. H0604a 去掉 collapse / near-collapse seeds 后，`S0-cos` 和 `S1-cos` 最好，但二者近似相同；所以当前证据支持 `cosine router + slot init` 的 route structure，不支持 center separation 的独立增益。
4. H0604b feature-axis audit 已完成：在最佳非坍缩条件 `S0/S1-cos` 下，route 更像绑定 `slot`，不是 $B_i$；但 exact `(slot,B_i)` 仍是 same-feature consistency 的 atomic key。

Current next decision:

```text
For non-collapsed slot-aligned conditions, test what relation multiple
slot features share when they enter the same expert.
```

Do not move to route-utility binding, Zipf / high-frequency distribution, or real data until the relation among multiple routed features inside one expert is characterized.

---

## 0.1 Experiment Index

本 anchor 下面的实验线索按问题层级读：

| Stage | Experiment | Question | Result / status | Consequence |
|---|---|---|---|---|
| 1 | H0603a historical supervised slot-margin run | 外部指定 slot assignment 时，不同 slot feature 能否被送到不同 expert？ | 可以稳定 route-slot NMI | 只证明 supervised assignment 下可构造；不是当前 label-free claim |
| 1b | H0603b center-only diagnostics | 只做 center separation 是否足够？ | center separation alone 不足以决定 token assignment | 不能把 router center 分开等同于 specialization |
| 2 | `A05_01_feature_key_routing_stability_center_only` | 同一 tentative feature 是否稳定送到同一 expert？feature 暂定为 `(slot,B_i)` | weak same-feature consistency 基本成立；collapse 可造成假阳性；center separation 无独立增益 | FeatureKeyConsistency 是弱指标，必须加 load / composition guard |
| 3 | `A05_01_feature_axis_audit_existing_logs` | 当前所谓 feature 到底是 `slot`、$B_i$，还是 `(slot,B_i)`？ | completed; best non-collapsed `S0/S1-cos` is slot-aligned, $B_i$ is weak, exact `(slot,B_i)` is stable | choose branch 2C for current best setup |

当前逻辑：

1. 先问“不同 feature 是否送到不同 expert”；
2. 再问“同一 feature 是否送到同一 expert”；
3. 发现 feature 定义不完整；
4. 因此转向 feature-axis audit。

H0604b branch decision：

| Branch | Audit outcome | Next step |
|---|---|---|
| 2A | exact feature `(slot,B_i)` 都不稳定 | 继续诊断 router 为什么连弱 route consistency 都没有 |
| 2B | exact feature 稳定但 slot 不稳定 | 承认 router 绑定 composite identity / atomic predictive state，不 claim slot-level feature |
| 2C | exact feature 稳定且非坍缩 | current branch; 进入“多个 feature 进同一个 expert 后是什么关系” |

Zipf / 高频 feature 分布只在 feature axis 和 same-expert feature relation 都更清楚后再做。

---

## 1. Problem Definition

### Parent problem

ordinary top-1 MoE router 在 NTP 训练下容易形成不稳定或不可解释的 routing，导致 feature-level expert specialization 失败。

### Current small question

在 uniform multi-B synthetic 中，router 的稳定分发到底对应什么 operational feature：

```text
slot / B_i / (slot,B_i)
```

### Decision question

Current immediate decision after H0604b:

```text
When multiple slot features are routed into the same expert, what relation do they share?
```

### What this anchor does not decide

本 anchor 当前不回答：

1. 真实语言数据中怎么获得 feature label；
2. Zipfian 高频/低频问题；
3. expert utility 是否已经形成；
4. route-function binding 的最终形式；
5. 多个 feature 进入同一 expert 后共享什么关系。

第 5 点是当前下一步。

---

## 2. Physical Priors
top-1 selected-gate router 会强化 early assignment。如果早期 assignment 形成 all-to-one 或 many-to-one collapse，那么 same-feature consistency 可以很高，但这不是 specialization。

对当前 multi-B synthetic：

$$
x_{s,i} = [r_{\mathrm{start}}, C_s, B_i, Y_{s,i}, r_{\mathrm{end}}]
$$

同一个 hidden state at $B_i$ 可能同时包含：

$$
h_{s,i}=c_i+\beta u_s+\epsilon
$$

where:

1. $c_i$ 表示 $B_i$ identity；
2. $u_s$ 表示 slot/context information；
3. $(s,i)$ 表示 atomic predictive state，因为 target $Y_{s,i}$ 由二者共同决定。

因此，在说 “feature-level routing” 前，必须先判断 router 绑定的是哪一个轴：

```text
slot
B_i
(slot,B_i)
```

Center separation 的物理含义只限于：

> 鼓励 router rows 在几何上分开，减少所有 expert rows 聚到同一方向。

它不能自己决定某个 token 应该进入哪个 expert。因此如果 center separation 后 route-feature NMI 不提高，或 load collapse 仍存在，就不能 claim specialization。

---

## 3. Current Hypotheses

### H1: weak same-feature consistency

同一个 operational feature $f$ 的多个 variants 会稳定 route 到同一个 expert：

$$
\max_e P(route=e\mid f)\approx 1
$$

Current status:

H0604a 支持 weak claim when $f=(slot,B_i)$，但该指标本身不排除 collapse。

### H2: center separation independent gain

Center separation only 应该在同样 init/router 下提高 non-collapsed route-feature structure。

Current status:

H0604a 削弱该假说。`S0 ~= S1` 且 `S0-cos ~= S1-cos`；center separation 没有独立增益。

### H3: cosine + slot init structure

Cosine router + slot init 可能比 dot-product / random init 更容易形成非坍缩、slot-related route structure。

Current status:

H0604a/H0604b filtered read 支持该方向：`S0/S1-cos` 是当前最干净的非坍缩 slot-aligned routing 条件。但它不是 utility specialization 证据。

### H4: feature-axis ambiguity

当前 “feature” 可能不是 slot，而是 $B_i$ 或 `(slot,B_i)`。

Current status:

H0604b 基本固定当前最佳条件下的 operational feature axis：`slot` 是最合适的下一阶段 feature label；`(slot,B_i)` 作为 exact same-feature consistency key；$B_i$ 不是最佳条件中的主要 route axis。

---

## 4. Mathematical Model
For a feature label type $F$:

```text
F in {slot, B_i, slot+B_i}
```

Define:

$$
P(e\mid f)=
\frac{\#\{samples:\ route=e,\ feature=f\}}
{\#\{samples:\ feature=f\}}
$$

Consistency:

$$
\mathrm{Consistency}(F)=
\frac{1}{|F|}
\sum_{f\in F}
\max_e P(e\mid f)
$$

Route-feature information:

$$
NMI(route;F)
$$

Collapse guard:

$$
P(e)=
\frac{\#\{samples:\ route=e\}}
{\#\{samples\}}
$$

Report:

```text
load entropy norm
max load fraction
active experts
```

Primary interpretation rule:

High consistency with low load entropy is weak lock-in / collapse, not specialization.

---

## 5. Current Center-Separation Definition

This anchor now uses only router center separation:

$$
u_e=\frac{w_e}{\|w_e\|_2+\epsilon}
$$

$$
L_{\mathrm{sep}}=
\frac{1}{E(E-1)}
\sum_{e\neq e'}
\max(0,\ u_e^\top u_{e'}-\delta_{\mathrm{sep}})
$$

Total objective for center-only conditions:

$$
L = L_{\mathrm{NTP}} + \lambda_{\mathrm{sep}}L_{\mathrm{sep}}
$$

No supervised token-margin, no feature separation objective, no route-utility binding objective.

---

## 6. H0604b Minimal Test

Use existing H0604a route matrix logs. No retraining.

For each condition / seed / checkpoint:

1. construct feature labels:
   - `slot`;
   - $B_i$;
   - `slot+B_i`;
2. compute feature × expert heatmaps;
3. compute consistency for all three feature definitions;
4. compute expert load histogram;
5. compute `NMI(route; slot)`, `NMI(route; B_i)`, `NMI(route; slot+B_i)`;
6. apply collapse filter before branch decision.

Required central figures:

| Figure | Purpose |
|---|---|
| feature × expert heatmap | Rows are features, columns are experts; tests whether each feature concentrates on one expert |
| consistency bar plot | Compares `slot`, $B_i$, and `slot+B_i`; tests which feature definition gives stable routing |
| expert load histogram | Rejects all-to-one / near-all-to-one collapse |
| NMI bar plot | Compares route information about `slot`, $B_i$, and `slot+B_i` |

Status:

```text
completed at main/experiments/A05/A05_01_feature_axis_audit_existing_logs/
```

---

## 7. Current Evidence

H0604a compact evidence:

| Condition | FeatureKeyConsistency | Load entropy norm min | Max load max | Route-slot NMI |
|---|---:|---:|---:|---:|
| R0-dot | 0.9987 | 0.0000 | 1.0000 | 0.3456 |
| R1-dot | 0.9982 | 0.0000 | 1.0000 | 0.2975 |
| S0-dot | 0.9942 | 0.1131 | 0.9711 | 0.4516 |
| S1-dot | 0.9942 | 0.1131 | 0.9711 | 0.4516 |
| R0-cos | 0.9945 | 0.2701 | 0.8762 | 0.3132 |
| R1-cos | 0.9889 | 0.2614 | 0.8823 | 0.3182 |
| S0-cos | 0.9991 | 0.0000 | 1.0000 | 0.5711 |
| S1-cos | 0.9991 | 0.0000 | 1.0000 | 0.5711 |

Interpretation:

1. same `(slot,B_i)` consistency is high across conditions;
2. collapse can produce perfect consistency;
3. center separation does not independently improve over NTP-only paired conditions;
4. this motivated H0604b because the feature definition was unresolved at that point.

H0604b compact evidence after collapse / near-collapse filtering:

| Condition | Feature label | Consistency | `NMI(route; feature)` | Load entropy norm | Max load |
|---|---|---:|---:|---:|---:|
| S0-cos | `slot` | 0.964 | 0.852 | 0.869 | 0.407 |
| S0-cos | $B_i$ | 0.410 | 0.012 | 0.869 | 0.407 |
| S0-cos | `slot+B_i` | 0.999 | 0.295 | 0.869 | 0.407 |
| S1-cos | `slot` | 0.964 | 0.852 | 0.869 | 0.407 |
| S1-cos | $B_i$ | 0.410 | 0.012 | 0.869 | 0.407 |
| S1-cos | `slot+B_i` | 0.999 | 0.295 | 0.869 | 0.407 |

H0604b branch result:

```text
2C: 16 condition-seed pairs
2B: 2 condition-seed pairs
2A: 0 condition-seed pairs
```

Interpretation:

1. Exact `(slot,B_i)` stability is real enough to pass the weak consistency question after collapse filtering.
2. In the best current setup, route information is mostly `slot`, not $B_i$.
3. `slot+B_i` is still the exact atomic key for same-feature consistency, but it is not the best route-axis interpretation.
4. `S0-cos` and `S1-cos` are identical in this audit, so center separation still has no independent gain.
5. Current claim should be `cosine router + slot init gives the cleanest non-collapsed slot-aligned routing`, not `geometric inhibition causes specialization`.

---

## 8. Next Decision

H0604b fixes the current branch as 2C for the best non-collapsed setup.

Current branch table:

| Branch | Condition | Interpretation | Next step |
|---|---|---|---|
| 2A | not current | `(slot,B_i)` unstable after non-collapse filtering | would diagnose weak route consistency failure |
| 2B | only random-cos edge cases | `(slot,B_i)` stable but `slot` weak | do not generalize slot claim to random init |
| 2C | current best setup | exact feature stable, non-collapsed, slot-aligned | ask what relation multiple slot features share inside one expert |

Immediate next diagnostic:

```text
Given non-collapsed slot-aligned routing, inspect the composition of each expert:
which slots/features enter the same expert, and do they share any geometric,
predictive, or training-dynamic relation?
```

Parked until later:

1. route-utility binding;
2. Zipf / high-frequency feature distribution;
3. real-corpus robustness.

Claim boundary:

After H0604b, `slot` is a valid operational feature axis for the next local diagnostic in `S0/S1-cos`, but this still does not prove functional expert specialization.
