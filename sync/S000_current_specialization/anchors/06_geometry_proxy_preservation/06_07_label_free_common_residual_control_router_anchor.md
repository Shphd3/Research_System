---
anchor_id: A06_07_label_free_common_residual_control_router
parent_node: rq.feature_specialization.initialization_method
status: closed_weakened
created: 2026-06-21
updated: 2026-06-21
canonical_language: en
---

# A06_07 Label-Free Common / Residual-Control Router Anchor

## 0. Thinking Card
父问题：random-init sparse top-1 MoE 能否在 uniform feature setting 中进入 feature-level specialization basin，而不是 common-collapse basin。
当前子问题：不用 slot label、slot centroid、oracle feature identity，只通过 router-side common / residual control，能否削弱 early common-logit bias 并提高 slot_NMI。
当前判断：A06_07 step-0 gate 削弱 simple label-free common/residual control 作为方法候选；它主要改善 load，不恢复 feature specialization。
关键证据：0/336 label-free rows 通过；full-sweep mean NMI baseline `0.2302`，calibration mean `0.2353`，heldout batch mean `0.2350`，whitened residual `0.0150`；但 load 从 `0.6867` 降到约 `0.283` 或 `0.086`。
最危险边界：这是 synthetic initialized hidden-state step-0 replay；不能排除 learned feature discovery、anti-lockin training、或真实 DCLM 机制。
下一步决策：不要推进 simple global common-centering / top-PC / whitening；下一步需要 feature discovery 或 anti-lockin，而真实模型实验必须避免 load-only 指标。

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
Do not promote simple global common / residual controls. Move to feature-discovery or anti-lockin mechanisms, and treat load-only improvement as insufficient in any real-model / DCLM test.

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

Observation:
A06_06 proved oracle feature-centroid reachability: raw, common-centered, and whitened centroid oracle conditions all reached `feature_NMI=1.0`, `L=0`, and positive margin across all 48 seed-depth-readout cells.
Boundary:
This is an oracle upper bound, not label-free.

Observation:
A06_07 tested label-free global common / residual controls on the same initialized hidden-state replay surface. Across all 336 condition cells, no label-free row passed the step-0 gate. Full-sweep mean NMI stayed near baseline (`0.2302 -> 0.2353` for calibration mean, `0.2350` for heldout batch mean) while load improved strongly (`0.6867 -> about 0.283`). Whitened residual control had low load (`0.0860`) but collapsed NMI (`0.0150`).
Interpretation:
Simple label-free common/residual controls remove load imbalance but do not discover feature-aligned router directions. Load balance is not a valid specialization proxy.
Evidence links:
`../../experiments/A06/A06_07_label_free_common_residual_control_router/summary.md`
`../../experiments/A06/A06_07_label_free_common_residual_control_router/detailed.md`

## 8. Claim Boundary And Next Decision

Can claim:
The tested label-free global common / residual controls do not approximate the A06_06 oracle feature partition at step 0; their apparent success is mostly load-only.

Cannot claim:
Real LM transfer, trained expert utility, final deployability, full collapse solution, or that load balance alone equals specialization.

Next decision:
Park simple common-centering / projection / whitening as method candidates. Test a stronger label-free feature-discovery mechanism or an anti-lockin training mechanism. Any real DCLM experiment should report feature_NMI/proxy feature structure or another feature-specialization metric, not load alone.
