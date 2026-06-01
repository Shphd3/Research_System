# Execution Plan: 0531_auto_route_function_binding

Anchor:

```text
Projects/from-attention-to-search/main/problem_anchors/gated_main_causes/route_function_binding_stable_gating_anchor.md
```

Story:

```text
在 synthetic NTP 中，判断哪些 routing/training 机制能让 route assignment 同时对齐 target-deciding feature 和 expert causal utility，并且训练/推理稳定。
```

## 1. Run Goal

主目标：

```text
找到至少一种候选 routing 机制，在 controlled synthetic NTP 下稳定分开不同 feature，并通过 forced expert utility 证明 selected expert 真正有 causal utility。
```

主判断不是 CE，不是 NMI 单项，而是：

```text
BindingPassRate = across seeds/conditions，同步通过 route-feature alignment、forced utility、assignment-utility、CE health、training stability、inference stability 的比例。
```

半晚 auto-research 的目标不是最终论文结论，而是确定下一条主线：

```text
A. representation decomposition / residual router
B. utility-binding regularization
C. nonlinear gate
D. linear gate + prior/margin
E. route-only fix 不够，需要 feature write-in pressure
```

## 2. Data / Material / Case Construction

### 2.1 Known Good / Known Bad / Known Confusing

| Case | Purpose | Expected |
|---|---|---|
| `T0_2x2_fixed_complementary` | sanity: NTP gate has utility signal | split |
| `T0_2x2_identical_experts` | negative control: no utility gap | no gate learning |
| `T0_2x2_same_best_expert` | collapse control | both features route same expert |
| `T1_uniform_noncompositional` | advisor's minimal uniform/non-compositional case | should split if utility specialization forms |
| `T2_multiB_slot_uniform` | current main failure case | flat may learn task but route-function binding unstable |
| `T3_common_unique_uniform` | disentangle common vs unique without Zipf | tests common interference |
| `T4_zipf_common_unique` | robustness after uniform works | tests head/tail frequency stress |
| `T5_heldout_shift` | inference stability | routes should remain stable under heldout/noise/shift |

### 2.2 Synthetic NTP Contract

Each sample is a next-token prediction tuple:

```text
input/context: x or token sequence ending at routed position
routed hidden factor: h = c_i + q_rho + u_s + noise
target token: y = target(feature, B identity, slot)
loss: next-token CE
```

Required factor annotations for diagnostics only:

```text
feature_id / slot_id
B_identity
frequency_rank
common_component_id
train/heldout split
```

These labels may be used for evaluation and oracle controls. Candidate mechanisms marked real-plausible must not require them at inference.

## 3. System / Procedure / Evaluation Setup

### 3.1 Baselines

| ID | Model | Purpose |
|---|---|---|
| `M0_flat_top1` | ordinary trainable top-1 MoE | baseline failure/success point |
| `M0_soft_gate` | soft MoE gate | check whether hard top-1 creates artifact |
| `M1_common_flat` | global common path + leaf router | existing weak positive baseline |
| `M_oracle_feature_router` | oracle feature/slot route | upper bound; diagnostic only |
| `M_oracle_utility_router` | route to forced-loss-best expert | utility upper bound; diagnostic only |

### 3.2 Candidate Mechanisms

| ID | Candidate | Mainline impact | Real-training plausibility |
|---|---|---|---|
| `C1_residual_linear` | linear gate on $h - P_common h$ or whitened residual | tests representation decomposition | plausible if common subspace estimated online |
| `C2_utility_binding` | KL from gate to detached per-expert NTP utility posterior | directly binds route to expert utility | plausible; uses NTP labels and expert losses |
| `C3_prior_linear` | prototype init / warmup / margin / temperature | tests linear gate + prior | diagnostic if uses feature labels; later replace by self-supervised prototypes |
| `C4_nonlinear_gate` | small MLP gate, raw and residual input | tests non-linear separability | plausible if stable and not overfit |
| `C5_residual_plus_binding` | residualized gate + utility-binding regularizer | tests combined interference + utility fix | plausible if both mechanisms matter |
| `C6_tail_writein_pressure` | inverse-frequency or feature-balanced NTP auxiliary | tests missing tail write-in | plausible with sampling/reweighting; not pure router fix |

### 3.3 Candidate Algorithm Specifications

#### C1: Residualized Linear Gate

Input:

```text
hidden states h at routed positions; optional known common labels for oracle diagnostic; running hidden-state buffer for learned subspace.
```

Parameters:

```text
rank_common: [1, 2, 4, 8]
subspace_source: oracle_common | PCA_all | PCA_head | running_PCA
update_interval: 100 steps
router_input: raw | residual | whitened
```

Steps:

```text
1. Estimate common/head subspace U_c.
2. Transform router input: h_res = h - U_c U_c^T h.
3. Train ordinary top-1 or soft gate on h_res.
4. Measure route-feature NMI, route-B NMI, forced utility matrix, stability.
```

Pass:

```text
Improves BindingPassRate without CE degradation > 5%, and lowers route-B/head NMI while increasing route-feature NMI.
```

Fail:

```text
CE improves but route-function binding does not; or residual removes target feature and hurts oracle route utility.
```

Debug artifacts:

```text
common subspace explained variance; factor attribution before/after; route heatmaps; forced CE heatmaps.
```

#### C2: Utility-Binding Regularizer

Input:

```text
For each sample, expert/path logits before mixture or forced-route outputs.
```

Parameters:

```text
tau_utility: [0.25, 0.5, 1.0]
lambda_bind: [0.01, 0.05, 0.1, 0.2]
start_step: [0, warmup_200]
expert_eval: all_experts for synthetic; topk_or_sampled for larger runs
```

Intermediate variables:

```text
ell_e = CE(f_e(h), y)
q_e = softmax(-ell_e / tau_utility)
p_e = gate probability
L_bind = KL(stopgrad(q) || p)
L_total = L_NTP + lambda_bind * L_bind + optional load/margin health terms
```

Pass:

```text
Raises assignment-utility and forced-loss diagonal together, with stable route-feature NMI and no collapse.
```

Fail:

```text
Gate chases transient utility and collapses; high assignment-utility occurs with low route-feature NMI; CE worsens strongly.
```

Debug artifacts:

```text
utility posterior entropy; gate-vs-utility KL trajectory; route changes after utility switches; seed-level failure examples.
```

#### C3: Prototype / Prior Linear Gate

Input:

```text
feature prototypes from synthetic labels for diagnostic, or self-supervised clusters for real-plausible variant.
```

Parameters:

```text
init: random | feature_centroid | orthogonal_prototype
warmup_steps: [0, 200, 1000]
lambda_proto: [0.0, 0.01, 0.05]
margin: [0.0, 0.2, 0.5]
temperature_schedule: fixed | annealed
```

Pass:

```text
Prototype alignment persists after warmup and selected experts become utility-best, not just route-aligned.
```

Fail:

```text
Routes start aligned but NTP washes out alignment, or experts do not become functionally specialized.
```

Boundary:

```text
Oracle feature prototypes are diagnostic, not a deployable mechanism. They test whether stable priors can hold binding long enough for utility to form.
```

#### C4: Nonlinear Gate

Input:

```text
raw h and residual h_res.
```

Parameters:

```text
router: MLP 1 hidden layer
hidden_width: [16, 32, 64]
activation: GELU/ReLU
regularization: weight_decay, router_entropy, load_health
input_variant: raw | residual | raw+residual
```

Pass:

```text
Improves binding on distributed slot code where linear gate fails, and keeps inference stability on held-out B/noise.
```

Fail:

```text
Memorizes B identity, improves train NMI but fails held-out B; or load collapses.
```

#### C6: Tail Write-In Pressure

Use only if factor attribution shows target/tail feature has weak forced expert utility.

Candidate forms:

```text
inverse-frequency sample reweight
feature-balanced batches
auxiliary per-feature CE balance
minimum utility margin for rare features
```

Pass:

```text
Tail/slot forced utility improves before route intervention, making router fixes meaningful.
```

Fail:

```text
Write-in pressure improves tail CE but still does not create route-function binding; then combine with C2/C1.
```

## 4. Configs And Commands

### 4.1 Repository/Remote Preflight

Run before modifying or launching:

```bash
pwd
git status --short --branch
python --version
nvidia-smi || true
find . -maxdepth 3 -name AGENTS.md -o -name PROJECTS.md
```

Read in order:

```text
AGENTS.md
PROJECTS.md
sync/S000_current_specialization/README.md
sync/S000_current_specialization/anchors/expert_specialization/slot_context_dominance_router_specialization_anchor.md
sync/S000_current_specialization/anchors/expert_specialization/hierarchical_route_utility_binding_anchor.md
daily_research_reports/0529/meeting/group_meeting_thought_update.md
this execution_plan.md
```

### 4.2 If Runner Already Exists

Adapt existing runner and create configs:

```bash
python -m experiments.route_binding.run --config configs/0531/T0_2x2_ntp.yaml --smoke
python -m experiments.route_binding.run --config configs/0531/T2_multiB_slot_uniform_baselines.yaml --smoke
python -m experiments.route_binding.run --config configs/0531/T2_multiB_slot_uniform_candidates.yaml --smoke
```

Full run pattern:

```bash
python -m experiments.route_binding.run_sweep \
  --matrix Projects/from-attention-to-search/main/experiments/0531_auto_route_function_binding/experiment_matrix.yaml \
  --output runs/0531_auto_route_function_binding
```

### 4.3 If No Runner Exists

Create minimal workspace:

```text
experiments/route_binding/
  data.py
  models.py
  train.py
  metrics.py
  factor_attribution.py
  run.py
  analyze.py
  configs/0531/*.yaml
```

Required smoke command:

```bash
python experiments/route_binding/run.py \
  --task T0_2x2_ntp \
  --model M0_soft_gate \
  --steps 200 \
  --seeds 0 1 \
  --output runs/0531_auto_route_function_binding/smoke_T0
```

Do not launch full sweeps until T0 and one T2 smoke create valid `metrics.csv`, `routes.csv`, `utility_matrix.csv`, and at least one heatmap.

## 5. Metrics And Artifacts

### 5.1 Primary Decision Metric

`BindingPassRate`: fraction of seeds/conditions satisfying all of:

```text
route_feature_nmi >= 0.85
assignment_utility >= 0.90
forced_loss_diag_margin >= 0.10 nats or >= 10% relative margin
final_ce <= 1.05 * best_baseline_ce
load_max_fraction <= 0.80 unless task truly needs collapse
checkpoint_binding_drop <= 0.10 from best checkpoint to final
inference_route_consistency >= 0.85 on held-out/noise/shift
```

Why primary:

```text
It prevents false positives from route heatmaps alone, CE alone, or utility collapse alone.
```

Cannot prove:

```text
It cannot prove real-corpus transfer; it only supports controlled synthetic route-function binding.
```

### 5.2 Supporting Metrics

| Metric | Question | False Positive It Catches | Cannot Prove |
|---|---|---|---|
| `route_feature_nmi` | Does route align with target feature? | random load skew | expert utility |
| `route_B_nmi` | Is router controlled by token identity? | feature-looking route caused by B identity | utility |
| `assignment_utility` | Is chosen route utility-best? | route-feature alignment without utility | can be high under collapse |
| `forced_loss_diag_margin` | Does each feature have a useful expert/path? | high utility due common path | stable training |
| `ablation_delta_ce` | Is expert causally used? | passive route assignment | feature identity |
| `checkpoint_stability` | Does specialization persist? | early alignment washout | real transfer |
| `inference_consistency` | Is routing robust after training? | train memorization | downstream utility |
| `factor_logit_R2` | Which factor controls logits? | wrong diagnosis of failure | causal proof alone |
| `tail_head_utility_gap` | Are tail features written in? | router-only blame | route stability |

### 5.3 Required Artifacts

```text
runs/<id>/metrics.csv
runs/<id>/seed_metrics.csv
runs/<id>/checkpoint_metrics.csv
runs/<id>/routes.csv
runs/<id>/forced_loss_matrix.csv
runs/<id>/ablation_utility_matrix.csv
runs/<id>/factor_attribution.csv
runs/<id>/figures/route_heatmap_*.png
runs/<id>/figures/forced_loss_heatmap_*.png
runs/<id>/figures/checkpoint_trajectory_*.png
runs/<id>/figures/factor_attribution_*.png
runs/<id>/config_resolved.yaml
runs/<id>/run_manifest.json
runs/<id>/logs/*.txt
```

## 6. Stage Audit

| Stage | Local Question | Input Evidence | Pass / Fail Rule | Debug Artifact | Handoff |
|---|---|---|---|---|---|
| S0 sanity | Is the NTP toy implemented correctly? | T0 fixed/identical/same-best | complementary splits; identical no signal; same-best collapse | 2x2 trajectory table | continue only if passes |
| S1 baseline replication | Does flat/common reproduce known failure? | T2 multi-B uniform | slot visible/oracle works but learned route imperfect | route/utility heatmaps | if not reproduce, debug setup |
| S2 factor attribution | Which factor controls router logits? | saved h/logits/routes/factors | component swap/R2 identifies common/B/head/slot contribution | factor attribution table | choose intervention path |
| S3 write-in check | Is target/tail feature in expert function? | forced CE/ablation matrix | target feature has feature-specific utility margin | forced CE heatmap | if absent, run C6 first |
| S4 candidate smoke | Does method improve binding on 2 seeds? | C1-C6 smoke | improves at least two binding metrics without CE crash | seed metrics | select top 2 |
| S5 candidate full | Does method pass across seeds/conditions? | top candidates 5-10 seeds | higher BindingPassRate than baselines | summary tables | write summary/detailed |
| S6 inference stability | Does route persist after training? | heldout/noise/shift | consistency >= threshold | stability trajectories | decide claim boundary |
| S7 documentation | Can result update anchor? | all curated artifacts | summary/detailed complete | artifact map | update anchor/sync |

## 7. Pass / Fail Criteria

### Overall Success

```text
At least one candidate beats M0_flat_top1 and M1_common_flat in BindingPassRate on T2/T3 uniform, keeps CE within 5%, and passes T5 inference stability.
```

### Stronger Success

```text
The same candidate also improves T4 Zipf stress or combines with C6 to restore tail feature binding.
```

### Failure

```text
No candidate improves forced-loss diagonal + route-feature NMI + stability together.
```

### Redirect

```text
If forced expert utility for target/tail feature is absent, stop router-only search and open a feature-write-in pressure anchor.
```

### Insufficient Evidence

```text
Runs are too few, smoke only, missing forced utility matrix, missing checkpoint trajectory, or metrics disagree without failure decomposition.
```

## 8. Failure Modes To Check

```text
1. CE improves but routes collapse.
2. Route-feature NMI high but forced utility not diagonal.
3. Assignment-utility high but route-feature NMI low: utility-best collapse.
4. Prototype init works early then washes out.
5. Nonlinear gate memorizes B identity and fails held-out B.
6. Residualization removes target feature along with common feature.
7. Utility-binding chases transient utility and locks into bad early expert.
8. Reweight improves tail CE but hurts common/head enough to destroy task.
9. Load balance creates artificial spread without causal expert utility.
10. Metrics computed on training data hide inference instability.
```

## 9. Result Location

Curated result docs:

```text
Projects/from-attention-to-search/main/experiments/0531_auto_route_function_binding/summary.md
Projects/from-attention-to-search/main/experiments/0531_auto_route_function_binding/detailed.md
```

Figures/tables:

```text
Projects/from-attention-to-search/main/experiments/0531_auto_route_function_binding/figures/
Projects/from-attention-to-search/main/experiments/0531_auto_route_function_binding/tables/
```

Optional handoff:

```text
Projects/from-attention-to-search/XingyuD/sync/0531_gating_auto_research/report.md
daily_research_reports/0531/gating_auto_research/report.md
```

Anchor update:

```text
Projects/from-attention-to-search/main/problem_anchors/gated_main_causes/route_function_binding_stable_gating_anchor.md
sync/S000_current_specialization/anchors/expert_specialization/route_function_binding_stable_gating_anchor.md
```
