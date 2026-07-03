---
anchor_id: A06_09_training_basin_preservation
parent_node: rq.feature_specialization.training_dynamics
status: supported_synthetic_training_basin
created: 2026-06-22
canonical_language: en
---

# A06_09 Training Basin Preservation Anchor

## 0. Thinking Card
父问题：step-0 feature-level routing 可构造时，top-1 MoE 训练是否会保持它。
当前子问题：A06_06 oracle init step-0 可达；A06_08 若通过会给 pseudo init。A06_09 只问 initialization-only 是否足够。
当前判断：支持。feature-aligned initialization 在本合成训练面上足以保持 feature-level routing。
关键证据：oracle init 和 A06_08 pseudo init 都是 `24/24` 支持；step-0 和 final held-out `feature_NMI=1.0`，final target accuracy `1.0`，load $L=0.0$。A06_08 dependency audit 选择 `route_kmeans_residual_K4`。
最危险边界：训练目标是 route-position target prediction，不是完整真实文本 next-token training；不能推出真实 DCLM 或语义专家。
下一步决策：继续初始化路线，优先测试 label-free discovery / pseudo-init 在更弱、更真实 feature proxy 下是否仍可用；anti-lockin 暂时不是主线必需步骤。

- Question: Does feature-aligned initialization preserve feature_NMI during ordinary top-1 MoE training?
- Physical prior: good initialization may define a specialization basin, but top-1 training may override it.
- Core model: track $a_i(t)=\arg\max_e w_e(t)^\top h_i(t)$ and $NMI(f_i,a_i(t))$.
- Model term being tested: training-time preservation of an initial feature partition.
- Primary metric: held-out `feature_NMI(t)` and final `feature_NMI`, with accuracy as constraint.
- Falsifier: high step-0 NMI becomes low final NMI while accuracy is acceptable.
- Can claim: whether initialization alone is sufficient in this synthetic setting.
- Cannot claim: real-text transfer, expert utility, deployable router, or solved anti-lockin.
- Current result: supported in the synthetic uniform `slot_token_len=4` route-position training setting.
- Next decision: test whether the initialization route transfers to weaker feature proxies and less controlled training settings.

## 1. Problem Definition

Parent problem: feature-level specialization requires both a good initial partition and a training trajectory that preserves it.
Sharper subproblem: A06_06 proves step-0 oracle reachability; A06_09 tests whether that partition survives training.
Decision question: given feature-aligned initialization, does ordinary training preserve held-out feature_NMI while learning the task?
Not in scope: anti-lockin intervention search, real DCLM, top-k routing, expert utility, final benchmark.

## 2. Physical Priors

- P1: Good initialization may define a specialization basin. Could be wrong if training drifts away from the initial partition.
- P2: Top-1 training can amplify early winners. Could be wrong if oracle init remains stable without intervention.
- P3: Step-0 margin may predict preservation. Could be wrong if task gradients dominate margin.

## 3. Falsifiable Hypotheses

- H1: Oracle feature-centroid init is sufficient. Supported in the tested setting: final NMI stays at `1.0` with target accuracy `1.0`.
- H2: Passed A06_08 pseudo init transfers. Supported in the tested setting: `route_kmeans_residual_K4` pseudo init matches oracle.
- H3: Step-0 margin predicts survival. Not adjudicated as a general predictor because both oracle and pseudo have perfect preservation across all full-run cells.

## 4. Mathematical Model

Objects: feature label $f_i$, router row $w_e(t)$, hidden state $h_i(t)$, assignment $a_i(t)$, load $p_e(t)$, accuracy.

Routing:
$$
a_i(t)=\arg\max_e w_e(t)^\top h_i(t).
$$

Trajectory:
$$
NMI_t=NMI(f_i,a_i(t)),\qquad L_t=m\max_e |p_e(t)-1/m|.
$$

Margin:
$$
\gamma_i(t)=z_{i,a_i(t)}(t)-\max_{e\ne a_i(t)}z_{i,e}(t).
$$

Observable metrics: step-0 / early / final NMI, accuracy, load, margin p05, route heatmap, route-change rate.
Falsifier: high accuracy with low final NMI.

## 5. Computational Realization

- Input: uniform synthetic feature task lineage from A06_06-A06_08.
- Conditions: random, equal-norm random, oracle feature-centroid, conditional A06_08 pseudo init.
- Run: audit step-0 routing, train with matched ordinary top-1 schedule, evaluate checkpoints.
- Evidence: NMI trajectory, accuracy trajectory, load/margin trajectory, heatmaps.
- Artifacts: `protocol.md`, `summary.md`, `detailed.md`, `tables/training_trajectory.csv`, `figures/nmi_trajectory.png`.

## 6. Minimal Falsification Tests

Test 1: oracle initialization preservation.
Question: does oracle init keep feature routing during training?
Comparison: random/equal-norm random vs oracle init.
Supports: oracle keeps high NMI and learns.
Weakens: oracle NMI collapses or merges features.

Test 2: pseudo init preservation, conditional on A06_08.
Question: if A06_08 passes, does pseudo init train more like oracle or random?
Comparison: pseudo vs oracle vs random.
Supports: pseudo remains closer to oracle.
Weakens: pseudo becomes random-like.

Test 3: margin predictor.
Question: does initial margin predict final NMI?
Comparison: per-seed step-0 margin p05 vs final NMI.
Supports: higher margin predicts preservation.
Weakens: no relation.

## 7. Current Evidence

- A06_06: oracle feature-centroid init reaches perfect step-0 held-out routing. This proves reachability, not training preservation.
- A06_07: load-improving controls do not improve feature_NMI. A06_09 must judge NMI trajectory.
- Earlier collapse audits: top-1 dynamics can amplify bias. This motivates preservation testing, not immediate anti-lockin.
- A06_08: label-free residual k-means recovers pseudo-feature centers with held-out `feature_NMI=1.0` across the full grid and selects `route_kmeans_residual_K4` for A06_09.
- A06_09 full run `a06_09_training_basin_full_20260622_2`: oracle init and A06_08 pseudo init both preserve `feature_NMI=1.0`, target accuracy `1.0`, and load $L=0.0$ across 8 seeds and depths `{1,2,4}`. Random, equal-norm random, and label-shuffled guards learn the target but do not provide clean supported specialization.

## 8. Claim Boundary And Next Decision

Can claim: feature-aligned initialization alone preserves specialization through route-position target training in the synthetic uniform `slot_token_len=4` setting, and the A06_08 pseudo-center method is good enough to enter that basin here.
Cannot claim: real-text transfer, full next-token training stability, expert utility, semantic specialization, deployable router, or solved anti-lockin.
Next decision: continue the initialization route by weakening the feature proxy and training assumptions. Anti-lockin should remain parked unless preservation fails under the next, less controlled setting.
