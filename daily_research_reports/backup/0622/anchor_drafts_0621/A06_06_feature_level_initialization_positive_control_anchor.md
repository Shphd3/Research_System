---
anchor_id: A06_06_feature_level_initialization_positive_control
parent_node: rq.feature_specialization.initialization_geometry
status: draft_for_user_review
created: 2026-06-21
canonical_language: en
---

# A06_06 Feature-Level Initialization Positive Control Anchor

## 0. Thinking Card

父问题：uniform feature distribution 下，初始化时能否让 dot-product top-1 MoE 形成 feature-level specialization，而不是进入 common-collapse basin。
当前子问题：在已知 feature identity / feature centroid 的 oracle 条件下，构造 equal-norm、common-controlled expert centers，判断初始化路由是否可达到 load-balanced feature specialization。
当前判断：这是 positive control，不是 final method；它回答“目标是否可达”，不回答“label-free 怎么做”。
关键证据：已有 handoff 显示 slot information 存在、slot-init positive control 可达到高 NMI；A06_04 显示 hidden common 是初始化路由的主偏置源。
最危险边界：不能把 oracle feature-centroid init 当作可部署方法；不能 claim expert utility 或真实文本泛化。
下一步决策：如果 oracle init 成功，则进入 label-free common/residual-control initialization；如果失败，则说明当前 hidden geometry 或 metric 不足以支持初始化 specialization。

Question:
Given uniform discrete features and initialized hidden states, can an oracle feature-centroid / residual-geometry initialization produce feature-level top-1 routing specialization at step 0 while keeping load balanced?

Physical prior:
If feature information is present in residual hidden geometry after common control, expert centers aligned with feature residual centroids should route each feature consistently to a distinct expert.

Core model:
For feature `f`, write hidden centroid `mu_f = c + r_f`. Construct expert centers from `r_f` or a balanced spherical code in the residual subspace, then route by `z_{f,e}=w_e^T(mu_f-c)` or replay on per-sample centered hidden states.

Model term being tested:
Reachability of feature-level specialization under favorable initialization geometry.

Primary metric:
slot_NMI / feature_NMI, read jointly with load imbalance `L` and margin.

Falsifier:
If oracle centroid-aligned or residual-space balanced centers do not produce high feature_NMI with acceptable load and margin, then initialization-only feature-level specialization is not reachable under the tested hidden geometry.

Can claim:
A positive-control reachability result for feature-level initialization in the synthetic setting.

Cannot claim:
A label-free algorithm, trained stability, expert causal utility, or real-text generalization.

Next decision:
Use the positive-control result to decide whether a label-free initialization / router-input control is worth testing.

## 1. Problem Definition

Parent problem:
A uniform feature distribution should not be mistaken for guaranteed feature-level expert specialization.

Decision question:
Under oracle access to feature identity or feature centroids, can we initialize expert centers so that step-0 top-1 routing assigns each feature to a stable expert with balanced load and positive margin?

Why this matters:
If positive control fails, label-free method construction is premature. If it succeeds, the next problem becomes approximating the oracle without feature labels.

Not in scope:
Label-free estimation, final trained collapse, real text, route-utility binding, or expert functional specialization.

## 2. Physical Priors

P1: Feature information exists in routed hidden states.
Meaning: feature labels should be linearly or geometrically separable enough for an oracle routing center to exploit.
Could be wrong if: feature centroids are not separated after common-centering.

P2: Common control is required before feature-aligned routing.
Meaning: raw hidden centroids `mu_f` may be dominated by common component `c`, so centers should be built from `r_f=mu_f-c`.
Could be wrong if: raw centroid initialization performs as well as common-centered initialization.

P3: Balanced feature distribution plus one expert per feature should support balanced load.
Meaning: if every feature is equally frequent and routes one-to-one to experts, load should be near uniform.
Could be wrong if: within-feature context variation or top-1 boundaries merge features despite centroid alignment.

P4: Margin matters.
Meaning: high NMI with tiny routing margin may not survive training.
Could be wrong if: low-margin routing remains stable in short training checks.

## 3. Falsifiable Hypotheses

H1: Oracle residual-centroid initialization can produce feature-level specialization.
Supported if: `feature_NMI` is high, load is near balanced, and feature purity is high at step 0.
Weakened if: oracle residual-centroid centers still merge features or create severe load imbalance.

H2: Common-centered centroids outperform raw centroids.
Supported if: centers built from `r_f=mu_f-c` produce higher NMI / margin than centers built from `mu_f`.
Weakened if: raw and common-centered centers perform similarly.

H3: Equal-norm centers improve load without destroying specialization.
Supported if: equalizing center norms keeps NMI high and reduces load distortion.
Weakened if: equal norm reduces margin or causes feature merging.

H4: Positive control is stable enough to justify label-free approximation.
Supported if: short training preserves high NMI and accuracy.
Weakened if: step-0 specialization immediately collapses under training.

## 4. Mathematical Model

Objects:
Features `f=1..F`, experts `e=1..m`, routed hidden state `h_i`, feature centroid `mu_f=E[h_i | f]`, common component `c`, residual centroid `r_f=mu_f-c`.

Centroid decomposition:

```math
\mu_f = c + r_f
```

Oracle center construction:

```math
w_{\pi(f)} = \alpha \cdot \frac{r_f}{\|r_f\|}
```

for a feature-to-expert permutation `pi`, with equal norm `alpha`.

Routing score:

```math
z_{i,e}=w_e^T(h_i-c)
```

or, for raw-hidden comparison:

```math
z_{i,e}=w_e^T h_i.
```

Metrics:

```math
feature\_NMI = NMI(f_i, a_i), \quad
L=m\max_e |p_e-1/m|, \quad
margin_i=z_{i,a_i}-\max_{e\ne a_i} z_{i,e}.
```

## 5. Computational Realization

Input objects:
Use the same synthetic uniform feature / slot setting and extracted initialized hidden states. Use feature labels only for oracle positive-control construction and evaluation.

Conditions:

1. `random_gaussian_init`: standard random router baseline.
2. `equal_norm_random_direction`: removes row-norm variation but not feature alignment.
3. `raw_feature_centroid_init`: centers aligned with raw feature centroids `mu_f`.
4. `common_centered_feature_centroid_init`: centers aligned with `r_f=mu_f-c`.
5. `residual_spherical_code_init`: balanced centers in residual subspace, if `F=m` and centroid geometry is clean enough.
6. Optional short-training check: freeze / unfreeze variants only after step-0 positive control is read.

Primary artifacts:
Condition table with `feature_NMI`, per-feature purity, load imbalance, margin, and accuracy if training is run.

Required visualizations:
Feature-to-expert route heatmap and margin distribution by condition.

## 6. Minimal Falsification Tests

Test 1: Step-0 oracle initialization reachability.
Question: Is feature-level specialization reachable at initialization under oracle residual-centroid centers?
Primary metric: `feature_NMI`, read with `L` and margin.
Supports: high NMI, balanced load, positive margin.
Weakens: persistent feature merging or low margin under oracle centers.
Insufficient: feature distribution not uniform, centers are built from evaluation labels without train/eval split, or only load is reported.

Test 2: Raw vs common-centered centers.
Question: Does common control matter for feature-aligned initialization?
Primary metric: NMI and margin difference between raw-centroid and residual-centroid initialization.
Supports common-control: residual-centroid centers outperform raw-centroid centers.
Weakens common-control: raw centers match residual centers.

Test 3: Short training basin check.
Question: Does a positive-control initialization remain in the specialization basin under training?
Primary metric: final `feature_NMI` with accuracy constraint.
Supports basin entry: NMI remains high and accuracy is preserved.
Weakens basin entry: step-0 specialization collapses during early training.

## 7. Current Evidence

Observation:
A06_04 supports hidden common component as a dominant source of synthetic hidden-state step-0 load imbalance. This motivates common-centered feature-centroid initialization rather than raw hidden-centroid initialization.
Boundary:
A06_04 does not prove feature-level specialization is reachable.

Observation:
Prior handoff evidence reports that routed hidden states contain slot information and that slot-init positive control can reach high slot_NMI with balanced load.
Boundary:
That evidence should be re-expressed under the current anchor's stricter positive-control framing and metrics.

Observation:
A06_03 shows row-norm variation can create gate-only imbalance, so positive-control centers should use equal norms unless norm is explicitly being tested.
Boundary:
Norm control is a guard here, not the main claim.

## 8. Claim Boundary And Next Decision

Can claim after support:
Feature-level routing specialization is reachable at initialization under oracle residual-geometry initialization in the synthetic setting.

Cannot claim:
A label-free initialization method, training robustness beyond the tested short run, expert causal specialization, real-text transfer, or final MoE solution.

Next decision:
If the oracle positive control succeeds, move to A06_07 label-free common/residual-control initialization. If it fails, return to residual geometry diagnostic and feature representation audit.
