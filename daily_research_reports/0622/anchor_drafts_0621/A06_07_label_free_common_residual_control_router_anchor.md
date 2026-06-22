---
anchor_id: A06_07_label_free_common_residual_control_router
parent_node: rq.feature_specialization.initialization_method
status: draft_for_user_review
created: 2026-06-21
canonical_language: en
---

# A06_07 Label-Free Common / Residual-Control Router Anchor

## 0. Tiny Summary

父问题：random-init sparse top-1 MoE 能否在 uniform feature setting 中进入 feature-level specialization basin，而不是 common-collapse basin。
当前子问题：不用 slot label、slot centroid、oracle feature identity，只通过 router-side common / residual control，能否削弱 early common-logit bias 并提高 slot_NMI。
当前判断：这是从机制诊断走向方法构造的第一步，但方法必须服务于已定位机制项：common-logit bias / residual path amplification / top-1 early lock-in。
关键证据：common-logit cancellation 可显著提高 slot_NMI；no-attention-residual B-routing 将 NMI 从 `0.080` 提到 `0.780` 并保持 accuracy；A06_04 支持 hidden common 是 synthetic hidden-state 主导 tested source。
最危险边界：不能 claim final deployable router；不能把 load balance 当作 specialization；不能使用 labels 后声称 label-free。
下一步决策：判断 label-free common / residual control 是否足够接近 oracle common-cancel / slot-init upper bound。

Question:
Can a label-free router-side common / residual-control intervention move random-init dot-product sparse top-1 MoE toward feature-level specialization while preserving accuracy?

Physical prior:
The router should not make top-1 decisions from feature-independent common components; if experts still receive full hidden states while router scores use common-controlled inputs, early common-logit bias can be reduced without removing task information from experts.

Core model:
Raw score `z_e=w_e^T h`. Common-controlled score `z'_e=w_e^T phi(h)`, where `phi(h)=h-c_hat`, projected residual, or residual-path router input. Experts still receive the full hidden state unless explicitly tested.

Model term being tested:
Label-free approximation to common-logit control and residual-path control.

Primary metric:
slot_NMI / feature_NMI with accuracy constraint.

Falsifier:
If label-free controls only improve load but not slot_NMI, or if they improve NMI only by using labels / oracle centroids, then this is not a valid label-free specialization method.

Can claim:
Intervention evidence that label-free common / residual control can move routing toward the specialization basin in the minimal synthetic setting.

Cannot claim:
Real LM transfer, final deployable router, expert utility, or that initialization alone solves final collapse.

Next decision:
Decide which label-free control should become the next method candidate, or whether remaining failure requires anti-lockin training control.

## 1. Problem Definition

Parent problem:
Uniform feature data plus random dot-product sparse top-1 routing tends to enter common-collapse rather than feature-to-expert specialization.

Immediate prior results:
Common-logit bias is intervention-relevant; oracle / controlled cancellation can improve specialization; direct residual identity at the routed position appears to amplify common-logit dominance.

Decision question:
Without slot labels or oracle feature centroids, can a router-side common / residual-control intervention improve slot_NMI from random initialization while preserving task accuracy?

Not in scope:
Real text, final production architecture, soft routing, top-k > 1, or expert functional causality.

## 2. Physical Priors

P1: Common-logit bias is a removable router-side nuisance term.
Meaning: `w_e^T c` acts like an expert-specific feature-independent bias.
Could be wrong if: removing label-free common estimates does not reduce common margin or improve NMI.

P2: Router input and expert input can be decoupled.
Meaning: experts can receive full `h` for computation, while router scores use `phi(h)` to avoid common-dominated assignment.
Could be wrong if: decoupling harms accuracy or produces unstable routing.

P3: Label-free common estimates can approximate oracle common control.
Meaning: batch mean, EMA mean, projection, or residual-only router input may estimate the nuisance direction without labels.
Could be wrong if: oracle works but all label-free estimates fail.

P4: Load balance is not enough.
Meaning: a control must improve feature_NMI / slot_NMI, not only max-load.
Could be wrong if: downstream expert utility proves load balance alone is sufficient, which is not the current claim.

## 3. Falsifiable Hypotheses

H1: Label-free common-centering improves specialization.
Supported if: batch/EMA common-centering increases slot_NMI and lowers common margin while preserving accuracy.
Weakened if: load improves but slot_NMI remains low.

H2: Residual-path router input improves specialization.
Supported if: router input based on residual / attention-output path increases slot_NMI and slot margin while preserving accuracy.
Weakened if: it lowers common margin but causes accuracy loss or feature merging.

H3: Projection-based common removal is less stable than direct logit/common control unless carefully constrained.
Supported if: broad SVD/top-PC removal is seed-unstable or removes task-relevant slot signal.
Weakened if: projection control is stable and matches oracle upper bound.

H4: Anti-lockin may still be needed after common control.
Supported if: step-0 / early NMI improves but final routing reconcentrates.
Weakened if: label-free common-control alone preserves high final NMI.

## 4. Mathematical Model

Raw router:

```math
z_{i,e}=w_e^T h_i
```

Common decomposition:

```math
h_i=c+r_i, \quad z_{i,e}=w_e^T c + w_e^T r_i
```

Label-free controlled router score:

```math
z'_{i,e}=w_e^T \phi(h_i)
```

Candidate `phi` functions:

```math
\phi_{batch}(h_i)=h_i-\hat c_{batch}
```

```math
\phi_{EMA}(h_i)=h_i-\hat c_{EMA}
```

```math
\phi_{proj}(h_i)=h_i-U_kU_k^T h_i
```

```math
\phi_{residual}(h_i)=LN(attention\_output_i)
```

Oracle upper bound:

```math
z^{oracle}_{i,e}=w_e^T h_i - w_e^T c
```

Primary success metric:

```math
NMI(feature_i, a_i), \quad accuracy, \quad L=m\max_e |p_e-1/m|.
```

## 5. Computational Realization

Fixed setting:
Use the minimal no-position moving-block dot-product sparse top-1 MoE setting unless explicitly testing synthetic hidden-state replay. Keep feature distribution uniform, B position / routing metric definition fixed, and experts receiving full hidden states by default.

Candidate variants:

1. `baseline_raw_router`: standard router score on full `h`.
2. `early_batch_mean_router`: router score on `h - batch_mean(h_routed)` during early window.
3. `early_ema_mean_router`: router score on `h - EMA_mean` during early window.
4. `residual_path_router`: router score from residual / attention-output path, experts still use full hidden.
5. `projection_common_router`: remove estimated common direction, with guard against removing slot signal.
6. `oracle_common_cancel`: upper bound, not label-free.
7. Optional guard: `equal_norm_router_rows` from A06_03, not main claim.

Primary metrics:
slot_NMI, per-slot route purity, accuracy.

Secondary metrics:
max_load, active experts, common margin, slot margin, route-lock step, many-to-one merge count, final route heatmap.

## 6. Minimal Falsification Tests

Test 1: Label-free common-control vs oracle upper bound.
Question: Can label-free common estimates approximate oracle common-logit cancellation?
Primary metric: slot_NMI with accuracy constraint.
Supports: label-free NMI approaches oracle and accuracy stays high.
Weakens: oracle works but label-free variants fail.
Insufficient: label-free variant leaks labels or uses feature centroids.

Test 2: Router-input-only residual control.
Question: Can changing only the router input reduce common dominance while preserving expert computation?
Primary metric: slot_NMI and accuracy.
Supports: NMI rises, common margin falls, slot margin rises, accuracy preserved.
Weakens: accuracy drops or NMI remains low.
Insufficient: expert input also changed, making mechanism ambiguous.

Test 3: Load-vs-specialization guard.
Question: Does the method improve feature specialization, not just load balance?
Primary metric: slot_NMI / purity, not max-load alone.
Supports: max-load decreases and NMI increases.
Weakens: max-load improves while NMI remains low or many-to-one merging persists.

Test 4: Early-window vs full-training control.
Question: Is common-control needed only to avoid early basin entry, or throughout training?
Primary metric: final NMI and route-lock step.
Supports early-basin view: early-window control is enough to preserve high final NMI.
Weakens: final routing reconcentrates after control stops.

## 7. Current Evidence

Observation:
0608 collapse audit and follow-up handoff support the model `h=c+r`, `z=w^T c+w^T r`: common-logit can dominate early routing, while final collapse still needs top-1 training amplification.
Boundary:
This motivates common-control but does not by itself define a deployable method.

Observation:
Common-logit cancellation and slot-init positive control can substantially improve slot_NMI while preserving accuracy in the minimal setting.
Boundary:
These are oracle / favorable controls and should be treated as upper bounds.

Observation:
No-attention-residual B-routing improved mean NMI from `0.080` to `0.780`, reduced common margin from `2.316` to `1.080`, raised slot margin from `0.556` to `1.863`, and preserved accuracy `1.000`.
Boundary:
It does not fully solve specialization; remaining failure is many-to-one slot merging, and the intervention may not isolate the only common source.

Observation:
A06_04 supports hidden common component as the dominant tested source in synthetic initialized hidden-state replay. Row norm is not the main explanation in that setting.
Boundary:
This supports common-control as the main method target, with row-norm equalization only as a guard.

## 8. Claim Boundary And Next Decision

Can claim after support:
A label-free common / residual-control intervention can move random-init routing toward feature-level specialization in the minimal synthetic setting while preserving accuracy.

Cannot claim:
Real LM transfer, trained expert utility, final deployability, full collapse solution, or that load balance alone equals specialization.

Next decision:
If one label-free control approaches oracle NMI and preserves accuracy, promote it to a method candidate and run basin / anti-lockin tests. If all label-free controls fail while oracle works, return to common-estimation design. If oracle fails, return to the mechanism model.
