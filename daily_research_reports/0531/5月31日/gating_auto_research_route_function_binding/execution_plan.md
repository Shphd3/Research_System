# Execution Plan: H0531_route_function_binding_auto_research

Anchor:

```text
Projects/from-attention-to-search/main/problem_anchors/gated_main_causes/route_function_binding_stable_feature_routing_anchor.md
```

## 1. Run Goal

结论先行：

```text
这不是 architecture sweep。目标是让 agent 判定：当前 synthetic NTP 的 specialization failure 是 routing interference，还是 tail/slot write-in failure；然后只沿对应机制测试最小干预。
```

最终目标：

```text
找到一种 routing / representation decomposition / regularization，使 synthetic NTP 中不同 target-deciding features 稳定分到不同 expert，并且该 expert 对该 feature 有 causal utility。
```

Primary decision:

```text
route-function binding 能否被显式机制稳定建立？
```

Secondary decision:

```text
有效路径更像：
A. representation decomposition / residual routing；
B. nonlinear gating；
C. linear gating + prior / regularization；
D. write-in pressure before routing。
```

## 2. Data / Material / Case Construction

### 2.1 Known sanity cases

Use 2x2 NTP cases before any larger run.

| Case | Data | Expert utility | Expected |
|---|---|---|---|
| complementary | $x_0\to A$, $x_1\to B$ | $E_0$ best for A, $E_1$ best for B | split |
| identical | same | experts identical | no route signal |
| same-best | same | $E_0$ best for A and B | collapse |
| weak complementary | same | weak utility gap | slow / weak split |

Pass rule:

```text
complementary final correct route >= 0.95;
identical route remains 0.5 +/- 0.05;
same-best sends both features to same expert;
weak complementary improves monotonically but with weaker margin.
```

### 2.2 Main synthetic NTP

Construct sequences:

```text
[common tokens] [slot code] [family token] [B_i] [target Y_{slot,family,i}]
```

Prediction position:

```text
B_i position predicts target Y.
```

Controlled factors:

| Factor | Role | Use |
|---|---|---|
| common | nuisance / shared | tests common dominance |
| slot | target-deciding feature | desired route axis |
| family | group nuisance | tests shortcut routing |
| B identity | nuisance / unique token | tests identity dominance |
| frequency rank | head/mid/tail | tests Zipf write-in |

Required splits:

```text
train / validation / heldout B identities / heldout perturbation pairs.
```

Heldout perturbations:

```text
same slot, different B identity;
same B identity, different slot;
same slot, changed common prefix;
same slot and family, tail vs head identity.
```

### 2.3 Distribution regimes

```text
uniform;
zipf_alpha_1.1;
zipf_alpha_1.3;
zipf_reweight;
balanced_curriculum_then_zipf.
```

Do not run all as a blind sweep. Use:

```text
uniform + zipf_alpha_1.3 + zipf_reweight
```

as the first decisive diagnostic trio.

## 3. System / Procedure / Evaluation Setup

### 3.1 Models

Baseline group:

```text
linear_soft_router
linear_top1_router
common_flat
oracle_slot_router
oracle_identity_router
random_router
```

Mechanism-intervention group:

```text
common_residual_router
frequency_residual_router
linear_residual_plus_consistency
nonlinear_residual_mlp_router
responsibility_binding_router
tail_write_in_pressure
combined_residual_plus_write_in
```

### 3.2 Router variants

#### Variant R0: baseline linear router

$$
g(x)=\operatorname{softmax}(Wh).
$$

Purpose:

```text
Measure ordinary NTP routing failure.
```

#### Variant R1: common-residual router

Estimate common / nuisance subspace $P_C$ from hidden states using labels available in synthetic data:

$$
h_{res}=h-P_Ch.
$$

Route on:

$$
g(x)=\operatorname{softmax}(W h_{res}).
$$

Purpose:

```text
If slot utility exists but router reads common / identity, removing nuisance subspace should improve route-slot binding.
```

No-oracle warning:

```text
Synthetic labels may be used to estimate and evaluate the mechanism. For future transfer, replace labels with unsupervised high-frequency/common estimates or training-time metadata. Do not claim real applicability until the no-oracle version passes.
```

#### Variant R2: high-frequency-removed router

Estimate head-frequency subspace $P_H$ from head-rank samples:

$$
h_{leaf}=h-P_Hh.
$$

Route on $h_{leaf}$.

Purpose:

```text
Test whether head/common feature dominance causes route interference.
```

#### Variant R3: route consistency regularization

For augmentations preserving slot $s$ but changing nuisance factors:

$$
L_{same}=\operatorname{KL}(g(h_a)\|g(h_b)).
$$

For pairs changing slot but preserving nuisance factors:

$$
L_{diff}=\max(0, m-\|g(h_a)-g(h_b)\|_1).
$$

Total:

$$
L=L_{NTP}+\lambda_{same}L_{same}+\lambda_{diff}L_{diff}+\lambda_{lb}L_{load}.
$$

Purpose:

```text
Make routing invariant to nuisance factors and sensitive to target feature.
```

#### Variant R4: nonlinear residual MLP router

$$
g(x)=\operatorname{softmax}(W_2\sigma(W_1 h_{res})).
$$

Purpose:

```text
Test whether failure is linear separability after removing nuisance factors.
```

Control:

```text
MLP on raw h may use identity shortcut; only MLP residual improvement counts as mechanism support.
```

#### Variant R5: responsibility binding router

Compute stop-gradient responsibility target:

$$
\rho_e=\frac{g_e P_e(y|x)}{\sum_k g_k P_k(y|x)}.
$$

Add:

$$
L_{bind}=\operatorname{CE}(\operatorname{stopgrad}(\rho), g).
$$

Purpose:

```text
Directly align route probability with NTP-derived expert utility.
```

Risk:

```text
Can reinforce early collapse. Must combine with load / entropy / feature-balanced batches and check seed stability.
```

#### Variant R6: tail-write-in pressure

Use feature-balanced or inverse-frequency loss:

$$
L=\alpha_f L_{NTP},\qquad \alpha_f \propto \frac{1}{p(f)}.
$$

Optional auxiliary forced-expert write-in:

```text
For each target feature, force candidate experts during auxiliary batches and maximize diagonal utility gap under permutation-matched assignment.
```

Purpose:

```text
If tail/slot feature lacks utility-best expert, create expert function before changing router.
```

## 4. Configs And Commands

The agent must adapt commands to the actual code workspace. If the current remote workspace already has runners, use them; otherwise implement a minimal local runner with the following CLI contract.

### 4.1 Required CLI contract

```bash
python -m experiments.route_function_binding.run \
  --config configs/H0531/<config>.yaml \
  --out results/H0531_route_function_binding_auto_research/<run_id>
```

Required common flags:

```text
--seed
--distribution {uniform,zipf,zipf_reweight}
--model_variant
--num_slots
--num_experts
--num_b_identities
--zipf_alpha
--router_lr
--expert_lr
--lambda_load
--lambda_same
--lambda_diff
--lambda_bind
--lambda_tail
--top_k
--save_checkpoints_every
```

### 4.2 Smoke run

```bash
python -m experiments.route_function_binding.run \
  --config configs/H0531/smoke_2x2_ntp.yaml \
  --out results/H0531_route_function_binding_auto_research/smoke_2x2
```

### 4.3 Stage 1 diagnostic

```bash
python -m experiments.route_function_binding.run \
  --config configs/H0531/stage1_factor_writein_diagnostic.yaml \
  --out results/H0531_route_function_binding_auto_research/stage1_diagnostic
```

### 4.4 Stage 2 routing interference branch

```bash
python -m experiments.route_function_binding.run \
  --config configs/H0531/stage2A_residual_routing.yaml \
  --out results/H0531_route_function_binding_auto_research/stage2A_residual
```

### 4.5 Stage 2 write-in branch

```bash
python -m experiments.route_function_binding.run \
  --config configs/H0531/stage2B_tail_writein.yaml \
  --out results/H0531_route_function_binding_auto_research/stage2B_writein
```

### 4.6 Stage 3 stability

```bash
python -m experiments.route_function_binding.run \
  --config configs/H0531/stage3_stability_transfer_screen.yaml \
  --out results/H0531_route_function_binding_auto_research/stage3_stability
```

## 5. Metrics And Artifacts

### 5.1 Primary metric bundle

| Metric | Question it answers | Failure it catches | Cannot prove |
|---|---|---|---|
| target acc / CE | Did model learn NTP task? | trivial undertraining | specialization |
| route-feature NMI | Does route align with target feature? | routing collapse / identity shortcut | expert utility |
| forced expert CE matrix | Which expert can perform which feature? | no write-in | natural routing |
| ablation utility matrix | Which expert causally matters? | decorative routing | route alignment |
| assignment-utility agreement | Does selected route pick utility-best expert? | route-function mismatch | feature purity alone |
| factor logit R2 | Which factor controls router logits? | wrong-factor routing | causal utility |
| route flip under factor removal | Is routing sensitive to nuisance factors? | hidden shortcut | performance |
| checkpoint route flip | Is training assignment stable? | transient diagonalization | inference stability |
| seed permutation stability | Is specialization reproducible up to permutation? | seed-specific story | real transfer |
| augmentation consistency | Is inference route stable to nuisance changes? | brittle routing | no-oracle transfer |

### 5.2 Required figures

```text
figures/route_heatmap_by_slot.png
figures/forced_expert_ce_matrix.png
figures/ablation_utility_matrix.png
figures/factor_attribution_r2.png
figures/route_flip_by_factor_removal.png
figures/checkpoint_route_stability.png
figures/seed_permutation_stability.png
figures/head_mid_tail_utility_gap.png
figures/inference_augmentation_consistency.png
```

### 5.3 Required tables

```text
tables/primary_decision_table.csv
tables/stage1_factor_attribution.csv
tables/stage1_writein_utility.csv
tables/stage2_intervention_comparison.csv
tables/stage3_stability_screen.csv
tables/failure_decomposition.csv
```

## 6. Stage Audit

| Stage | Local Question | Input Evidence | Pass / Fail Rule | Debug Artifact | Handoff |
|---|---|---|---|---|---|
| S0 2x2 sanity | Is implementation truly NTP gate learning? | 2x2 CE curves | analytic pattern reproduced | 2x2 table + loss curve | continue or fix implementation |
| S1 factor attribution | What factor controls router logits? | trained baseline checkpoints | factor R2 / NMI / removal flip decisive | attribution tables + heatmaps | choose S2A/S2B |
| S1 write-in | Does tail/slot have utility-best expert? | forced/ablation utility | diagonal gap exists or not | forced CE + ablation utility | choose S2A/S2B |
| S2A routing intervention | Does residual/consistency routing fix wrong-factor route? | S1 says utility exists but route wrong | improves NMI + assignment-utility + stability | route/stability figures | candidate mechanism |
| S2B write-in intervention | Does reweight/write-in pressure create utility-best experts? | S1 says tail utility weak | improves tail utility diagonal + route binding | utility gap trajectory | candidate mechanism |
| S3 stability | Does method survive training/inference perturbations? | best S2 candidate | passes checkpoint/seed/augmentation stability | stability summary | update anchor |
| Closure | What is the safest claim? | all curated metrics | summary/detailed/anchor updated | artifact map | optional handoff |

## 7. Pass / Fail Criteria

### 7.1 Overall success

```text
target_acc >= 0.99;
route-feature NMI >= 0.80;
assignment-utility agreement >= 0.90;
forced utility diagonal gap > 0 for head/mid/tail;
checkpoint route flip <= 0.05 after burn-in;
augmentation consistency same-feature >= 0.90;
different-feature route separation >= 0.80;
seed-permutation stability >= 0.80.
```

### 7.2 Failure

```text
target_acc high but route-feature NMI < 0.50;
assignment-utility < 0.70;
tail utility diagonal absent under all write-in interventions;
final diagonal exists but checkpoint/seed/inference stability fails;
method relies on test-time oracle labels.
```

### 7.3 Insufficient evidence

```text
target_acc < 0.95;
2x2 sanity fails;
forced expert CE cannot be computed reliably;
metrics conflict without failure localization;
only one seed passes;
only heatmap improves but utility does not.
```

## 8. Failure Modes To Check

| Failure mode | Diagnostic | Response |
|---|---|---|
| NTP task not learned | target acc / CE | fix data/model before routing claims |
| route heatmap diagonal but no utility | forced/ablation matrix | do not claim specialization |
| high Assign-Utility from collapse | route NMI + route load | require both route alignment and utility |
| B identity shortcut | factor R2 / heldout B | residual router or consistency pairs |
| common/head shortcut | removal flip / head-tail gap | common/high-frequency residual router |
| tail not written | tail forced CE diagonal absent | reweight / tail-write-in pressure |
| early collapse reinforced by responsibility binding | route entropy / seed stability | add entropy/load/balanced batches |
| nonlinear gate overfits identity | heldout B and residual-only control | reject raw-h MLP claim |
| stability failure | checkpoint and augmentation consistency | reject method despite final score |
| metric mismatch | conflicting metrics repeatedly | run goal audit before more methods |

## 9. Result Location

Experiment folder:

```text
Projects/from-attention-to-search/main/experiments/H0531_route_function_binding_auto_research/
```

Expected structure:

```text
H0531_route_function_binding_auto_research/
  execution_plan.md
  summary.md
  detailed.md
  figures/
  tables/
  configs/
  runs/
  artifact_map.md
```

Raw outputs should stay in remote/container result dirs. Commit only curated tables, report-ready figures, configs, summary/detailed, and anchor updates.

## 10. Auto-Research Branch Logic

### Branch after S1

```text
If utility-best expert exists for slot/tail but route factor attribution is dominated by common/head/B identity:
  run S2A routing-interference branch first.

If slot/tail utility-best expert is absent or weak, especially under Zipf:
  run S2B write-in branch first.

If both are true:
  run minimal S2B to create utility, then S2A to route to it.

If neither is measurable:
  stop and write metric / data construction audit.
```

### Stop rules

```text
Stop after the first candidate passes S3 stability; write summary/detailed and update anchor.
Stop if two reasonable variants fail the same way; write failure decomposition before trying a third.
Stop if any result suggests the synthetic construction no longer tests the desired object.
```

## 11. Minimal Final Report Table

Agent must fill this table before handoff:

| Method | Distribution | Target Acc | Route NMI | Assign-Utility | Tail Utility Gap | Checkpoint Flip | Aug Consistency | Decision |
|---|---|---:|---:|---:|---:|---:|---:|---|
| baseline_linear_top1 | uniform | | | | | | | |
| baseline_linear_top1 | zipf | | | | | | | |
| common_residual_router | zipf | | | | | | | |
| tail_write_in_pressure | zipf | | | | | | | |
| combined_residual_plus_write_in | zipf | | | | | | | |

Decision labels:

```text
support / weaken / redirect / insufficient evidence
```
