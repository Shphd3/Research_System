---
parent_node: problem.moe_expert_specialization
proposed_source_path: Projects/from-attention-to-search/main/problem_anchors/gated_main_causes/route_function_binding_stable_feature_routing_anchor.md
proposed_root_sync_copy: sync/S000_current_specialization/anchors/expert_specialization/route_function_binding_stable_feature_routing_anchor.md
---

# Route-Function Binding For Stable Feature Routing

## 汇报前 Summary

父问题：

```text
MoE router 能否形成稳定、可解释、可复用的 feature-level expert specialization？
```

当前子问题：

```text
在 synthetic NTP 中，能否找到一种 routing / representation decomposition / regularization，使不同 target-deciding feature 稳定分到不同 expert，并且选中的 expert 对该 feature 有 causal utility？
```

为什么要问：

```text
已有结果说明：slot 信息可见，oracle routing 可行，但 learned top-1 routing 在 multi-B 下不能稳定把 slot 轴绑定到 utility-best expert。
同时 Zipf / common feature 可能造成 head/common 写入强、tail/slot 写入弱。
因此当前失败可能来自 routing interference，也可能来自 feature write-in failure。
```

决策问题：

```text
下一步应该改 router input / gating mechanism，还是先改 expert function write-in pressure？
```

任务构造：

```text
受控 synthetic NTP：每个样本有 common、family、B identity、frequency rank、slot / target-deciding feature。目标是预测 next token。
```

当前预期结果：

```text
先用 diagnostic 判断 failure 类型：
1. 若 utility-best expert 已存在但 route 读错 factor，则做 common-residual / high-frequency-removed / consistency-regularized routing。
2. 若 tail/slot utility 本身不存在，则做 reweight / tail-write-in pressure / responsibility binding。
```

结论边界：

```text
本 anchor 只证明 synthetic NTP 中的 route-function binding 机制；不证明真实语料、端侧收益、KV reverse index 或 general H-MoE 有效。
```

下一步：

```text
执行 H0531_route_function_binding_auto_research：先跑 NTP 2x2 sanity，再跑 factor attribution + tail write-in diagnostic，然后按机制选择干预。
```

## 1. Problem Definition

Broader question:

```text
How can gating make MoE experts form stable, interpretable, reusable feature-level specialization?
```

Sharper question:

```text
Can we make routing bind to the target-deciding feature and to the expert that has causal utility for that feature, under controlled synthetic NTP?
```

Inside boundary:

```text
synthetic NTP;
known task factors;
known feature labels for evaluation;
small MoE / router variants;
route stability during training and inference;
expert utility measured by forced / ablation loss.
```

Outside boundary:

```text
real-corpus specialization;
KV-cache retrieval gain;
deployment-level speedup;
large-scale model claims;
architecture novelty without a falsifiable mechanism.
```

Operational definitions:

```text
feature: a controlled factor that changes the next-token distribution.
expert causal utility: forcing or retaining one expert improves next-token CE for a feature relative to alternatives.
route-function binding: route aligns with the feature and the selected expert is utility-best for that feature.
training stability: feature-expert assignment remains permutation-consistent across checkpoints after burn-in.
inference stability: route remains consistent under perturbations that preserve target-deciding feature and changes when that feature changes.
applicability: the method does not require test-time target labels or oracle feature labels; oracle labels are allowed only for synthetic evaluation or training-time auxiliary diagnostics explicitly marked as synthetic-only.
```

Success / failure / insufficient evidence:

```text
success: target acc >= 0.99, route-feature NMI >= 0.80, assignment-utility agreement >= 0.90, utility diagonal gap > 0, checkpoint route flip <= 0.05 after burn-in, seed-permutation stability >= 0.80.
failure: target acc high but route-feature NMI < 0.50 or assignment-utility < 0.70; or stability fails even when final metrics look good.
insufficient evidence: metrics conflict, target acc is low, implementation sanity fails, or forced/ablation utility is not trustworthy.
```

## 2. Physical Priors

### Prior 1: Functional specialization requires two links, not one.

```text
A route is useful only if the selected expert function actually helps predict the feature-conditioned next token.
```

Mathematical constraint:

$$
\operatorname{route}(x) \approx f(x)
\quad \text{and} \quad
\operatorname{route}(x) \approx \arg\max_e U(f,e)
$$

Implementation constraint:

```text
Always report route-feature alignment and forced/ablation utility together. Do not treat heatmap diagonalization as sufficient.
```

Refutable if:

```text
A method obtains stable feature routing but selected experts have no forced/ablation utility, or utility exists without any route-function agreement.
```

### Prior 2: NTP routing follows expert utility / responsibility, not feature identity itself.

For a sample $(x,y)$:

$$
P(y|x)=\sum_e g_e(x)P_e(y|x).
$$

The gate logit gradient follows:

$$
\frac{\partial L}{\partial z_e}=g_e-\rho_e,
\qquad
\rho_e=\frac{g_eP_e(y|x)}{\sum_k g_kP_k(y|x)}.
$$

Interpretation:

```text
gate probability is pushed toward expert posterior responsibility.
```

Implementation constraint:

```text
The first sanity test must reproduce known 2x2 NTP cases: complementary experts split, identical experts do not move, same-best experts collapse.
```

### Prior 3: Hidden states are mixtures of target and non-target factors.

At the target position:

$$
h=a_c c+a_g g+a_i b_i+a_s u_s+\epsilon,
$$

where $c$ is common factor, $g$ is family, $b_i$ is B identity, and $u_s$ is the slot / target-deciding factor.

Router logits:

$$
\ell_e=r_e^\top h.
$$

Factor attribution should estimate:

$$
\ell_e^{(F)}=r_e^\top P_F h.
$$

Refutable if:

```text
router logits and selected route cannot be explained by common / head / identity / slot factors better than random controls.
```

### Prior 4: Frequency can prevent tail/slot write-in.

```text
Zipfian feature frequency creates more gradient opportunities for head/common features; tail/slot features may not form a clear utility-best expert even when they determine the next token.
```

Refutable if:

```text
head and tail features have the same forced utility diagonal under Zipf, and reweighting does not change tail utility.
```

## 3. Mechanistic Motivation

The current failure can be decomposed into two competing mechanisms:

```text
Mechanism A: routing interference.
Tail/slot utility exists, but router reads common/head/B-identity factor.

Mechanism B: write-in failure.
Tail/slot feature does not form a utility-best expert; routing cannot bind to a function that does not exist.
```

The intervention depends on the mechanism:

```text
A -> common-residual / high-frequency-removed / consistency-regularized / nonlinear residual gating.
B -> reweight / tail-write-in pressure / responsibility binding / balanced expert utility formation.
```

## 4. Mathematical Modeling

Data factor:

$$
z=(c,g,i,s,r),
$$

where $r$ is frequency rank.

Next-token target:

$$
y=Y_{s,g,i}.
$$

Expert utility:

$$
U(f,e)=-CE_f(\operatorname{force}(e))
$$

or ablation utility:

$$
\Delta CE(f,e)=CE_f(\operatorname{ablate}(e))-CE_f(\operatorname{full}).
$$

Route-function binding metric bundle:

```text
route-feature NMI / route heatmap / forced expert CE matrix / ablation utility matrix / assignment-utility agreement / stability.
```

A method is valid only if it improves the bundle, not one metric alone.

## 5. Computational Realization

Synthetic NTP task:

```text
sequence: [common prefix, slot code, family token, B_i, target Y]
measure at B_i position and predict Y.
```

Controlled factors:

```text
common: shared across all samples;
slot: target-deciding factor;
family: group-level nuisance factor;
B identity: unique nuisance factor;
frequency rank: uniform / Zipf / reweighted.
```

Model variants:

```text
baseline_linear_top1
baseline_linear_soft
common_flat
common_residual_router
frequency_residual_router
nonlinear_residual_router
route_consistency_regularized_router
responsibility_binding_router
tail_write_in_pressure
combined_residual_plus_write_in
```

## 6. Minimal Decisive Test

### Test 0: 2x2 NTP sanity

Known good / bad / confusing cases:

```text
complementary experts -> split;
identical experts -> no gate signal;
same-best expert -> collapse;
weak complementary -> weak split.
```

Purpose:

```text
Verify implementation uses NTP CE and measures route-function binding, not fixed-gate proxies.
```

### Test 1: factor attribution + write-in diagnostic

Purpose:

```text
Determine whether baseline failure is routing interference or write-in failure.
```

Primary outputs:

```text
factor -> router logit R2;
factor -> selected route NMI;
factor removal -> route flip rate;
forced expert CE matrix;
ablation utility matrix;
head/mid/tail utility diagonal.
```

### Test 2A: routing-interference interventions

Only run as primary if Test 1 shows utility exists but route reads wrong factor.

```text
common-residual router;
high-frequency-removed router;
feature-preserving route consistency regularization;
small nonlinear residual router.
```

### Test 2B: write-in interventions

Only run as primary if Test 1 shows tail/slot utility is weak.

```text
inverse-frequency reweight;
tail-write-in auxiliary CE;
stop-gradient responsibility binding;
balanced exposure curriculum.
```

### Test 3: stability and transfer screen

```text
checkpoint route flip;
seed permutation stability;
inference augmentation consistency;
no-oracle inference constraint;
matched compute / matched accuracy controls.
```

## 7. Falsifiable Outcomes

Supported if:

```text
At least one method reaches the full success bundle on synthetic NTP, and the improvement matches the diagnosed mechanism.
```

Weakened if:

```text
All interventions improve target CE but fail route-function binding or stability.
```

Redirected if:

```text
metrics conflict repeatedly; then run a metric / goal audit before adding more routing methods.
```

Still not proven:

```text
real-corpus transfer;
deployment utility;
large-model scaling;
feature labels discoverable without synthetic factors.
```

## 8. Current Evidence

Current evidence from the project state:

```text
slot signal is visible and oracle routing works;
ordinary learned top-1 routing does not robustly bind slot to utility-best expert in multi-B;
common_flat has weak help but hierarchy alone is not established as the mechanism;
Zipf / common frequency may create tail write-in failure.
```

This anchor treats those as motivation, not final proof.

## 9. Claim Boundary And Next Decision

Safest current claim:

```text
The next useful research object is not “more hierarchy” but the route-function binding mechanism: whether to decompose router input or to strengthen feature write-in.
```

What cannot be claimed:

```text
Any proposed router is valid before it passes forced utility, stability, and no-oracle inference checks.
```

Next smallest decision:

```text
Run H0531_route_function_binding_auto_research Stage 0 and Stage 1. Decide whether the next intervention should target routing interference or write-in failure.
```
