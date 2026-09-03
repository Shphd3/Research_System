---
parent_node: problem.moe_expert_specialization
---

# Stable Route-Function Binding For Synthetic Feature Specialization

## researcher judgment record

目的：

```text
找到一种 routing / training 机制，使 synthetic NTP 中不同 feature 能稳定分到不同 expert，并且被选中的 expert 对该 feature 的 next-token prediction 有 causal utility。
```

物理建模 / 假设：

```text
NTP hidden state 是 compositional 的：common / token identity / frequency / slot-target feature 同时存在。普通 flat router 可能读到 dominant factor，但 selected expert 不一定是 target-deciding feature 的 utility-best expert。
```

最小实验：

```text
先做 factor attribution，判断 router logits 被 common、B identity、head-frequency 还是 slot/target feature 控制；再只测试能改变 route-function binding 的机制：residualized linear gate、utility-binding regularizer、prototype/prior gate、nonlinear gate。
```

当前结论：

```text
已有证据显示：slot 信息可见，oracle works，但 learned routing 不稳定；common_flat 有弱帮助，hierarchy 本身没有稳定解决；Zipf toy 显示 head write-in 强、tail write-in 弱。因此下一步不是加更深 architecture，而是做 factor attribution + route-function binding intervention。
```

结论边界：

```text
该 anchor 只判断 controlled synthetic NTP 中的 mechanism。不能直接 claim 真实语料 specialization、端侧 swapping 收益，或 H-MoE 已解决问题。
```

下一步：

```text
执行 0531_auto_route_function_binding：先定位失败机制，再按决策门测试最小候选方法。
```

## 1. Problem Definition

Parent problem:

```text
How can gating make MoE experts form stable, interpretable, reusable feature-level specialization?
```

Sharper subproblem:

```text
In controlled synthetic NTP, can we train a routing mechanism that separates known predictive features into different expert paths, while the selected experts remain causally useful for those features during training and inference?
```

Decision question:

```text
Should the next research direction be representation decomposition, explicit utility-binding regularization, nonlinear gating, or linear gating with priors/residualization?
```

Inside boundary:

```text
- synthetic NTP tasks with known feature factors;
- trainable gate and trainable experts;
- route-function binding diagnostics;
- training stability across checkpoints/seeds;
- inference stability under held-out B identities, feature noise, and frequency shift;
- mechanisms that can plausibly be used later without synthetic labels.
```

Outside boundary:

```text
- proving real-corpus specialization;
- claiming deployment/system-side swapping gain;
- using downstream retrieval as the success criterion;
- claiming route heatmap or NMI alone proves functional specialization;
- adding architecture depth without a factor-attribution reason.
```

Operational definitions:

```text
feature-level separation: success if route-feature NMI >= 0.85 and route purity >= 0.85 across held-out samples; failure if high CE accuracy occurs with NMI < 0.3 or single-route collapse; insufficient if only training-set route heatmaps are available.

route-function binding: success if the chosen route matches the utility-best expert/path for >= 0.90 of samples and forced-route CE has a diagonal or feature-specific margin; failure if route is feature-aligned but forced expert utility is not; insufficient if only assignment-utility is high without forced-loss heatmaps.

training stability: success if binding metrics do not wash out after early alignment and final-vs-best drop <= 0.10; failure if semantic/prototype routing decays during NTP; insufficient if only final checkpoint is measured.

inference stability: success if routes remain consistent under held-out B identities, small hidden-state perturbation, and frequency shift; failure if training specialization vanishes on held-out identities or distribution shift; insufficient if only training distribution is measured.

real-training plausibility: success if the intervention uses only NTP labels, hidden states, expert losses, routing probabilities, or unsupervised/online subspace estimates; failure if it requires synthetic slot labels at inference; insufficient if it works only with oracle feature IDs.
```

## 2. Physical Priors

Prior 1: NTP hidden states are compositional.

```text
At routed positions, h contains common/shared component, token identity, frequency-associated component, and target-deciding feature. The router can read any of them, but only some are causally relevant for the next token.
```

Refutable evidence:

```text
Factor swap/intervention shows route logits are not explained by any decomposed factor, or the supposed target feature has no measurable effect on target CE.
```

Prior 2: Feature-level specialization requires route-feature alignment and expert causal utility together.

```text
A route is not a feature expert if it only receives a feature's samples but does not reduce CE for that feature under forced routing or ablation.
```

Refutable evidence:

```text
Route heatmaps are diagonal but forced expert loss is not diagonal, or assignment-utility is high only because all features share one utility-best route.
```

Prior 3: Ordinary NTP may create utility collapse or wash out semantic initialization.

```text
NTP optimizes next-token loss, not directly feature identity. If one path can learn many features, router specialization is not guaranteed.
```

Refutable evidence:

```text
Across hard synthetic tasks, flat top-1 NTP consistently creates route-function binding without extra priors, residualization, load/capacity pressure, or utility-binding objective.
```

Prior 4: A useful routing mechanism must be stable at inference.

```text
If the router depends on unstable training-only labels or fragile hidden directions, it cannot become a reusable feature index.
```

Refutable evidence:

```text
A method passes training metrics but fails held-out B identities, perturbation, or checkpoint stability.
```

## 3. Motivation And Mechanism

Existing evidence narrows the failure:

```text
slot/context information can be visible and predictive;
oracle routing can work;
common_flat helps weakly;
hierarchy depth alone does not reliably fix binding;
Zipf frequency can make head features write into W much more strongly than tail features.
```

This creates two main rival mechanisms:

```text
Rival A: tail/slot feature is written into expert functions, but router logits are controlled by common / B identity / head-frequency directions.
Rival B: tail/slot feature is not written into expert functions, so changing router input alone cannot solve the failure.
```

Mechanism candidates:

```text
1. representation decomposition / residualized routing: remove or downweight common/head/B identity subspace before gating.
2. explicit route-function binding: use per-expert NTP utility to regularize gate probabilities toward utility-best experts.
3. nonlinear gate: learn a non-linear decision boundary when linear gate cannot isolate target-deciding feature.
4. linear gate + priors: prototype initialization, warmup constraints, margin, temperature, or load/capacity pressure that keeps routing aligned long enough for expert utility to form.
```

## 4. Mathematical Model
Let a routed hidden state be:

$$
h_{i,s}=c_i + q_{ho(i)} + u_s + \epsilon
$$

where:

```text
c_i: token / B identity component
q_{rho(i)}: frequency/head-family/common component
u_s: target-deciding slot/feature component
epsilon: nuisance/noise
```

A router observes either the raw or transformed hidden state:

$$
p_\theta(e|h)=\mathrm{softmax}(g_\theta(T(h)))
$$

where candidate transforms include:

$$
T_{raw}(h)=h
$$

$$
T_{res}(h)=h-U_cU_c^\top h
$$

$$
T_{white}(h)=\Lambda^{-1/2}U^\top(h-\mu)
$$

For expert path $e$, define forced expert loss:

$$
\ell_e(x,y)=CE(f_e(h), y)
$$

and detached utility posterior:

$$
q_e = \mathrm{softmax}(-\ell_e/\tau)
$$

A direct route-function binding objective is:

$$
L = L_{NTP} + \lambda_{bind} KL(\mathrm{sg}(q)||p_\theta(e|h)) + \lambda_{margin}L_{margin} + \lambda_{health}L_{load}
$$

where $\mathrm{sg}$ means stop-gradient. This uses NTP labels and expert losses, not synthetic feature labels. It should therefore be closer to real-training plausibility than oracle route labels.

Primary observable:

```text
BindingPassRate = fraction of seeds/conditions passing route-feature alignment, utility agreement, forced-loss diagonal margin, CE health, training stability, and inference stability together.
```

## 5. Computational Realization

Data construction:

```text
T0_2x2_ntp: two one-hot features, two tokens, fixed and trainable expert variants.
T1_uniform_noncompositional: K independent features with uniform frequency and one target per feature.
T2_multiB_slot_uniform: many B identities; same B maps to different targets under slot context.
T3_compositional_common_unique: h contains common + unique/slot factors; uniform first.
T4_zipf_common_unique: same as T3, but unique features follow Zipf; tests robustness after uniform works.
T5_heldout_shift: held-out B identities, feature noise, frequency shift, and checkpoint stability.
```

Models:

```text
M0_flat_top1: ordinary top-1 MoE baseline.
M1_common_flat: global common path + leaf router baseline.
M2_residual_linear: linear gate on residualized hidden state.
M3_utility_binding: flat gate with KL-to-expert-utility regularizer.
M4_prototype_prior_linear: feature/prototype warmup or margin prior, diagnostic only if it uses oracle feature labels.
M5_nonlinear_gate: small MLP gate, with and without residual input.
M6_combined_residual_binding: residualized input + utility-binding objective.
```

Measured artifacts:

```text
route heatmaps by feature / B identity / frequency rank
route-feature NMI and route-B NMI
forced expert CE matrix
ablation utility matrix
assignment-utility agreement
checkpoint trajectories
inference perturbation/heldout consistency
factor attribution tables and intervention plots
expert load health
CE / target accuracy
```

## 6. Minimal Decisive Test

The first decisive test is not a broad architecture sweep. It is:

```text
Stage 1: factor attribution on current baseline.
Stage 2: choose the smallest intervention that matches the diagnosed failure.
Stage 3: test stability and inference robustness only for methods that pass Stage 2.
```

Decision gates:

```text
If router logits are controlled by common/B/head component and slot utility exists -> pursue residualized/common-removed routing.
If slot/tail utility is absent in forced experts -> pursue write-in pressure or utility-binding objective before router-only fixes.
If both failures appear -> test combined residual + utility-binding.
If flat baseline already passes uniform but fails Zipf -> treat Zipf as robustness and test frequency-balanced binding.
If a method improves CE but not route-function binding -> reject for this anchor.
```

## 7. Falsifiable Outcomes

Supported if:

```text
At least one mechanism improves BindingPassRate over flat_top1/common_flat in uniform synthetic NTP and retains stability on held-out B / perturbation / checkpoint tests, while CE remains comparable.
```

Weakened if:

```text
Methods improve routing heatmaps or CE but not forced-loss diagonal / assignment-utility / stability together.
```

Redirected if:

```text
All routing interventions fail because tail/slot features are not written into expert functions. Then the next anchor should shift from router design to feature write-in pressure.
```

Still not proven:

```text
Even a successful synthetic mechanism does not prove real-corpus expert specialization or deployment utility.
```

## 8. Current Evidence

Evidence already supports the need for this anchor:

```text
- slot information can be visible and useful, but learned routing does not reliably bind slot axis to utility-best experts under many B identities;
- common_flat gives weak improvement, but hierarchy alone is not stable;
- high assignment-utility can be caused by utility collapse, so it must be read with route-slot NMI and forced-loss heatmaps;
- Zipf linear toy shows head feature write-in is much stronger than tail feature write-in and reweight restores tail.
```

Pre-run evidence to add after execution:

```text
summary.md
detailed.md
figures/*.png
tables/*.csv
anchor update section
```

## 9. Claim Boundary And Next Decision

Safest current claim:

```text
The active uncertainty is not whether features are visible, but whether routing can be trained to bind the target-deciding feature to a causally useful expert path in a stable way.
```

What cannot be claimed:

```text
- H-MoE already solved the gating problem.
- A diagonal routing heatmap proves specialization.
- A high assignment-utility score alone proves specialization.
- Synthetic success directly transfers to real corpora.
```

Next smallest decision:

```text
Run 0531_auto_route_function_binding. The first decision is factor attribution: is failure dominated by router-input interference or by missing feature write-in?
```
