---
anchor_id: A06_09_training_basin_preservation
parent_node: rq.feature_specialization.training_dynamics
status: active_draft
created: 2026-06-22
canonical_language: en
---

# A06_09 Training Basin Preservation Anchor Draft

## 0. researcher judgment record

父问题：即使初始化时构造了 feature-level routing partition，top-1 MoE 训练是否会保持这个 partition，还是重新进入 collapse / many-to-one merge basin。

当前子问题：A06_06 已证明 oracle feature-centroid 初始化在 step 0 可达；A06_08 若成功，会给出 label-free pseudo-center 初始化。本轮测试这些 good step-0 partitions 在训练中是否保持，以及是否需要 anti-lockin。

当前判断：这是 training-basin diagnostic，不是最终算法评测。先判断 initialization alone 是否足够；只有当它不够时，才把 anti-lockin 作为机制干预加入。

最危险边界：final accuracy 不能替代 feature_NMI；load balance 不能替代 specialization；短训练成功也不能 claim real-data transfer。

下一步决策：如果 oracle / pseudo init 在无 anti-lockin 下保持 high feature_NMI，则初始化可作为主要方向；如果训练破坏 partition，则下一步必须研究 anti-lockin / soft-to-hard / route-preservation dynamics。

Question:
If a feature-aligned router initialization gives high step-0 feature_NMI, is that initialization sufficient to keep the model in a feature-specialization basin during training?

Physical prior:
Good initialization may place top-1 MoE into a specialization basin, but hard top-1 training can amplify early winners and co-adapt experts with router assignments, potentially destroying even a good initial partition.

Core model:
Initialize router rows from random, oracle feature centers, or A06_08 pseudo centers. Track route assignment trajectory `a_i(t)`, feature_NMI(t), load(t), margin(t), and accuracy(t) during training.

Model term being tested:
Training-time preservation or destruction of an initially feature-aligned routing partition.

Primary metric:
Final and trajectory `feature_NMI`, with task accuracy as a constraint and load/margin as secondary diagnostics.

Falsifier:
If oracle or pseudo feature-aligned initialization collapses to low feature_NMI during training, initialization alone is insufficient as a collapse-avoidance mechanism.

Can claim:
Whether feature-aligned initialization is sufficient or insufficient for training-basin preservation in the tested synthetic setting.

Cannot claim:
Real-text transfer, production router method, expert utility alignment, or that anti-lockin is generally solved.

Next decision:
Decide whether to promote initialization as the main method target, or whether early anti-lockin must become a necessary companion mechanism.

---

## 1. Problem Definition

Parent problem:
Uniform feature distribution plus random top-1 MoE routing can enter collapse instead of feature-level specialization.

Immediate prior results:

- A06_06: oracle feature-centroid initialization reaches perfect step-0 feature routing.
- A06_07: global label-free controls do not recover feature routing.
- A06_08: planned test for label-free pseudo-feature center discovery.

Decision question:
Given a step-0 router partition that is feature-aligned, does training preserve that partition while learning the task, or do hard top-1 dynamics collapse / merge the routes?

Why this matters:
Initialization is only useful if it changes the training basin, not merely the step-0 replay. If it fails under training, the research direction must include anti-lockin or route-preservation mechanisms.

Not in scope:
Real text, large-scale LM training, semantic expert utility, top-k > 1, or final method benchmark.

---

## 2. Physical Priors

P1: Good initialization can place routing inside a specialization basin.

Meaning:
If each feature starts assigned to a distinct expert with positive margin, early training may reinforce that partition instead of collapsing.

Could be wrong if:
Top-1 training dynamics override the initial partition and reconcentrate routing.

P2: Hard top-1 routing can amplify early assignment imbalance.

Meaning:
Experts receiving more traffic get more gradient and co-adapt with their assigned routes, which can lock in or merge routes.

Could be wrong if:
Feature-aligned initialization remains stable without any anti-lockin control.

P3: Step-0 margin predicts basin stability.

Meaning:
Higher margin feature assignments should be harder to flip during training.

Could be wrong if:
Training utility gradients dominate initial routing margin.

P4: Pseudo-center initialization may be weaker than oracle initialization.

Meaning:
Even if A06_08 pseudo centers improve step-0 NMI, their lower margin or imperfect feature alignment may collapse under training.

Could be wrong if:
Pseudo centers preserve final NMI nearly as well as oracle centers.

P5: Load balance remains a guard, not the target.

Meaning:
A balanced route distribution with low feature_NMI is not specialization.

Could be wrong only under a separate expert-utility claim, which is outside this anchor.

---

## 3. Falsifiable Hypotheses

H1: Oracle feature-centroid initialization preserves specialization under training.

Supported if:
Oracle init keeps high final feature_NMI, high feature purity, and task accuracy.

Weakened if:
Oracle init starts high but collapses or merges features during early training.

H2: Pseudo-center initialization transfers to training if A06_08 step-0 feature_NMI and margin are high enough.

Supported if:
Best A06_08 pseudo init preserves feature_NMI substantially above random/global-control baselines.

Weakened if:
Pseudo init loses NMI despite good step-0 load.

H3: Early anti-lockin is needed if initialization alone fails.

Supported if:
An early load-balance / soft-to-hard / route-preservation intervention preserves NMI after init-only training collapses.

Weakened if:
No anti-lockin variant improves final feature_NMI over initialization alone.

H4: Step-0 margin predicts final preservation.

Supported if:
Seeds / methods with larger initial margin have higher final feature_NMI and later route-lock collapse.

Weakened if:
Margin has little relation to route survival.

---

## 4. Mathematical Model

Objects:
Feature label `f_i`, expert assignment `a_i(t)`, router score `z_{i,e}(t)`, router rows `w_e(t)`, expert parameters `theta_e(t)`, loss `ell(t)`, and task accuracy.

Initial router construction:

```math
w_e(0) \in \{w_e^{random}, w_e^{oracle}, w_e^{pseudo}\}.
```

Routing:

```math
a_i(t)=\arg\max_e z_{i,e}(t), \qquad z_{i,e}(t)=w_e(t)^T h_i(t).
```

Specialization trajectory:

```math
NMI_t = NMI(f_i,a_i(t)),
```

```math
L_t=m\max_e |p_e(t)-1/m|.
```

Margin trajectory:

```math
\gamma_i(t)=z_{i,a_i(t)}(t)-\max_{e\ne a_i(t)}z_{i,e}(t).
```

Failure mode:

```text
specialization collapse = high or acceptable accuracy but low feature_NMI / many-to-one feature-expert merging.
```

---

## 5. Computational Realization

Fixed setting:
Use the same synthetic feature task as A06_06/A06_08. Train models after initialization. Keep feature distribution uniform. Report feature_NMI, not only load or accuracy.

Initialization conditions:

1. `random_gaussian_init`.
2. `equal_norm_random_init`.
3. `global_control_init` from A06_07, as load-only negative control.
4. `oracle_feature_centroid_init` from A06_06, upper bound.
5. `best_pseudo_center_init` from A06_08, if any method passes step-0 discovery.
6. `label_shuffled_centroid_init`, guard against centroid construction artifacts.

Training controls:

Stage 1: initialization-only basin test.

- No anti-lockin.
- Same training schedule across initialization conditions.

Stage 2: anti-lockin diagnostic, only if Stage 1 shows collapse or many-to-one merging.

Candidate controls:

1. early load-balance warmup;
2. soft-to-hard routing schedule / temperature annealing;
3. route-margin preservation regularizer;
4. short freeze of router rows followed by unfreeze;
5. optional expert-input unchanged / router-input controlled variant.

Primary metrics:

- step-0, early, and final `feature_NMI`;
- task accuracy;
- per-feature route purity;
- route heatmap over checkpoints;
- load imbalance `L`;
- margin percentile, especially `margin_p05`;
- route-lock step;
- many-to-one merge count.

Expected artifacts:

- `tables/training_trajectory_summary.csv`
- `tables/final_by_condition.csv`
- `figures/nmi_trajectory.png`
- `figures/load_trajectory.png`
- `figures/route_heatmaps_by_checkpoint.png`
- `summary.md`
- `detailed.md`

---

## 6. Minimal Falsification Tests

### Test 1: Initialization-only basin preservation

Question:
Does feature-aligned initialization alone preserve feature-level specialization during training?

Primary metric:
Final `feature_NMI`, constrained by task accuracy.

Supports:
Oracle / pseudo initialization maintains high final NMI and accuracy.

Weakens:
NMI collapses despite high step-0 NMI and accuracy.

Insufficient evidence:
Only step-0 metrics are reported, or final accuracy is reported without NMI.

### Test 2: Pseudo vs oracle gap under training

Question:
Does the best A06_08 pseudo initialization behave like oracle or like random under training?

Primary metric:
NMI trajectory gap to oracle and random baselines.

Supports pseudo initialization:
Pseudo stays much closer to oracle than random.

Weakens pseudo initialization:
Pseudo starts better but converges to random-like collapse.

Insufficient evidence:
A06_08 pseudo centers are selected using evaluation labels.

### Test 3: Anti-lockin necessity

Question:
If initialization alone fails, can early anti-lockin preserve the feature partition?

Primary metric:
Final NMI improvement over init-only under matched accuracy.

Supports anti-lockin:
Early control preserves NMI where init-only collapses.

Weakens anti-lockin:
No control improves NMI or all controls hurt accuracy.

Insufficient evidence:
Controls change data/task or use feature labels.

### Test 4: Margin predictor

Question:
Does initial margin predict training preservation?

Primary metric:
Correlation / stratified readout between step-0 margin and final NMI.

Supports margin predictor:
Higher margin seeds/methods survive better.

Weakens margin predictor:
No consistent relation.

Insufficient evidence:
Too few seeds or no per-seed trajectory.

---

## 7. Current Evidence

Observation:
A06_06 shows that oracle feature-centroid initialization can produce perfect step-0 feature routing in the synthetic initialized hidden-state setting.

Interpretation:
The target partition is reachable before training.

Boundary:
This does not show the partition is stable under training.

Evidence links:
`../experiments/A06/A06_06_feature_level_initialization_positive_control/summary.md`
`../experiments/A06/A06_06_feature_level_initialization_positive_control/detailed.md`

Observation:
A06_07 shows that global label-free controls improve load but not feature_NMI.

Interpretation:
Initialization tests must track feature_NMI and not rely on load balance.

Boundary:
This does not rule out feature discovery or anti-lockin.

Evidence links:
`../experiments/A06/A06_07_label_free_common_residual_control_router/summary.md`
`../experiments/A06/A06_07_label_free_common_residual_control_router/detailed.md`

Observation:
Earlier collapse audits support the view that early common-logit bias can seed collapse, while final collapse can require top-1 training amplification / lock-in.

Interpretation:
Even a corrected initialization may need training-time protection.

Boundary:
The current anchor does not assume anti-lockin is necessary; it tests whether it is necessary.

Evidence links:
`../experiments/A05/A05_04_01_round1_slot_specialization_protocol_dot_product/summary.md`
`../experiments/A05/A05_04_02_round2_dotproduct_common_logit/summary.md`

---

## 8. Claim Boundary And Next Decision

Can claim after this test:
Whether good step-0 feature-aligned initialization is sufficient to preserve feature-level specialization through training in the tested synthetic setting.

Cannot claim:
Real-text transfer, final deployable router, semantic expert utility, or that initialization alone solves MoE specialization broadly.

Next decision:
If initialization alone succeeds, proceed to stronger label-free initialization and larger synthetic/real proxy settings. If initialization alone fails, shift the mainline to initialization plus anti-lockin dynamics before any real-data method claim.
