# Protocol: A11_02_01_E02 All-Position Semantic-Path Decomposition

## 0. Approval Snapshot

**Approval status:** approved for implementation and remote 4-GPU execution by the user on 2026-07-10.  
**Purpose:** determine whether K=2 MTP adds a positive native semantic update at the earlier decision state beyond NTP's later all-position semantic loss.  
**Primary anchor:** `../../../../problem_anchors/11_informative_future_branch_mechanism/11_02_hidden_to_parameter_transmission/subanchors/11_02_01_reachability_and_background_sign_anchor.md`.
**Anchor decision question:** is the decision-position H2 loss a resolved positive increment to $h_T$ semantic velocity after separating later semantic transfer and shared losses?  
**Physical prior tested:** earlier semantic credit should act more directly on the native $h_T\rightarrow S_Z$ margin than a later shared-parameter path.  
**Core model term:** $G_D=-\langle\nabla_\theta M_Z,\nabla_\theta L_D\rangle$.  
**Falsifier:** valid decomposition and frozen-path guards, but $G_D$ is unresolved/nonpositive or direct and masked trajectories are indistinguishable.  
**Experiment role:** root-cause audit and bridge validation.  
**Primary metric:** exact component semantic-velocity decomposition at the same checkpoint.  
**Minimal setup:** clean K=2 all-position sequence; one-layer Transformer; frozen embeddings/heads; reference-folded decision state; five seeds; four loss-mask conditions.  
**Basic configuration:** float64, full-batch SGD, 15,000 steps, with dense early checkpoints through step 200 and later checks at `500,1000,2000,5000,10000,15000`.  
**Conditions:** `ntp_all_h1`, `ntp_plus_direct_h2`, `mtp_all_k2`, `mtp_mask_direct_h2`.  
**Pass:** decomposition guards pass; $G_D>0$ in at least 4/5 seeds; full net velocity is positive in at least 4/5; one-step fidelity and early direct-condition ordering pass; local Y1 guard passes.  
**Fail:** direct term is unresolved/nonpositive, later indirect transfer matches it on native velocity and trajectory, or local damage explains the difference.  
**Insufficient:** reference fold, head geometry, decomposition, frozen paths, coverage, or finite-step numerical guards fail.  
**Cannot claim:** natural-language or LLM benefit, sample efficiency, larger-K benefit, AdamW behavior, or MoE utility.  
**Approval decision:** execute without a second approval round, following the user's standing instruction for subsequent anchors.

## 1. Terminology / Definitions

| Term | Plain meaning | Concrete object / computation | Unit / formula | Why it matters | Cannot prove |
|---|---|---|---|---|---|
| direct semantic loss | K=2 prediction of $S_Z$ from the earlier state | $L_D=\ell_{T,2}$ | cross-entropy | MTP-only path | global efficiency |
| indirect semantic loss | NTP prediction of $S_Z$ after reading $A$ | $L_I=\ell_{T+1,1}$ | cross-entropy | all-position NTP path | native use at $h_T$ |
| local shared loss | prediction of shared $A$ from $h_T$ | $L_S=\ell_{T,1}$ | cross-entropy | local-learning guard | long-horizon semantics |
| remaining loss | all other valid all-position terms | $L_R=L_2^{all}-L_D-L_I-L_S$ | cross-entropy | residual background | one causal pathway |
| native margin | H2-head alignment of $h_T$ with branch token $S_Z$ | $M_Z=m^{-1}\sum_zv_z^\top h_T(z)$ | scalar | model-useful semantic state | downstream utility |
| component velocity | parameter-space first-order margin movement from one loss | $G_c=-\langle\nabla M_Z,\nabla L_c\rangle$ | margin per unit SGD learning rate | primary decomposition | convergence |
| direct increment | full-minus-mask velocity at the same checkpoint | $G_{full}-G_{mask-D}=G_D$ | velocity | causal mask audit | cross-checkpoint comparison |

## 2. Anchor Alignment

**Decision question:** does MTP's earlier semantic target create a distinct positive native update at $h_T$ under all-position training?  
**Physical prior tested:** shorter supervision path yields a more direct semantic margin update.  
**Core model term:** $G_D$ versus $G_I+G_S+G_R$.  
**Falsifier:** $G_D\le0$ after all implementation guards pass, or later NTP transfer matches direct native dynamics.  
**Claim boundary:** controlled K=2 shared-encoder SGD only.

## 3. Tested Hypotheses

### H1. Exact path decomposition

At every audited checkpoint:

$$
\frac{|G_{total}-(G_D+G_I+G_S+G_R)|}
{|G_{total}|+|G_D|+|G_I|+|G_S|+|G_R|+10^{-12}}
\le10^{-8}.
$$

At step 0, $G_D>0$ in at least 4/5 seeds and the same-parameter full-minus-mask contrast equals $G_D$ to the same tolerance.

### H2. Direct versus later transfer

Report $G_D,G_I,G_S,G_R$ separately. Support requires direct-enabled conditions to exceed their matched direct-masked baselines on early native-margin area in at least 4/5 seeds. $G_I$ may be positive, zero, or negative; no sign is built into the pass rule.

### H3. Finite update and local guard

For `mtp_all_k2` and `mtp_mask_direct_h2`, at $eta\in\{0.0015,0.003\}$ and step 0:

$$
\operatorname{sign}(\Delta M_Z)=\operatorname{sign}(G_{total}),
$$

$$
\frac{|\Delta M_Z-\eta G_{total}|}
{\eta|G_{total}|+10^{-12}}\le0.25
$$

in at least 4/5 seeds when the predicted movement is above the numerical floor. Final Y1 accuracy must be at least 0.90 in all conditions that train $L_S$.

## 4. Rival Explanations

1. Output heads adapt: both heads are frozen and drift must be zero.
2. Branch embeddings provide trainable lookup: all token embeddings are frozen and update norm must be zero.
3. Initial $h_T$ already reveals the branch: reference-folded decision states and logits must match across branches at step 0.
4. Head mismatch explains the contrast: centered $S_Z$ rows are aligned across H1 and H2.
5. Generic extra loss explains the effect: direct-add and direct-mask contrasts isolate only $L_D$.
6. Decomposition code omits losses: total-loss and gradient reconstruction must pass.
7. Immediate nonlinearity invalidates velocity: virtual SGD updates test actual $\Delta M_Z$.
8. Local degradation explains semantic gain: Y1 loss/accuracy are reported against matched baselines.

## 5. Data / Model / Algorithm / Objective

Data for branch $z$:

```text
BR_z F00 ... F15 U00 U01 U02 U03 A_SHARED S_z
```

The decision index $T$ is `U03`. The semantic token is available through two paths:

```text
K=2 direct:       U03 --H2--> S_z
NTP later path:   A_SHARED --H1--> S_z
```

Model:

- four deterministic branches;
- one-layer causal Transformer, `d_model=64`, one attention head, dropout 0;
- two fixed full-vocabulary softmax heads;
- aligned centered $S_Z$ rows across H1/H2;
- fixed token embeddings;
- train attention, MLP, LayerNorm, and position parameters;
- reference-fold only the decision state;
- float64 full-batch SGD, learning rate `0.003`, no weight decay, 15,000 steps. The longer window matches the all-position scale used in A11_10; early mechanism evidence is still read from steps 0-200.

Loss partition:

$$
L_D=\ell_{T,2},
\quad L_I=\ell_{T+1,1},
\quad L_S=\ell_{T,1},
\quad L_R=L_2^{all}-L_D-L_I-L_S.
$$

## 6. Conditions, Seeds, And Checkpoints

Seeds: `971,972,973,974,975`.

| Condition | Active objective | Anchor clause tested | Why needed | Primary evidence |
|---|---|---|---|---|
| `ntp_all_h1` | all valid H1 losses | later semantic transfer baseline | shows what NTP can do after reading $A$ | $G_I+G_S+G_R$, $M_Z$ trajectory |
| `ntp_plus_direct_h2` | all H1 plus only $L_D$ | direct sufficiency on NTP background | changes only earlier semantic path | full-minus-NTP velocity and trajectory |
| `mtp_all_k2` | all valid H1 and H2 losses | native all-position MTP | tests direct plus complete background | full decomposition and finite step |
| `mtp_mask_direct_h2` | all H1/H2 except $L_D$ | direct necessity | keeps K2 background but removes earlier semantic path | full-minus-mask contrast |

Checkpoints: `0,1,2,5,10,20,50,100,200,500,1000,2000,5000,10000,15000`. Twenty train tasks are sharded across four GPUs.

## 7. Primary Metric

The primary metric is the same-checkpoint decomposition:

$$
G_{total}=G_D+G_I+G_S+G_R.
$$

It decides the anchor because it attributes current-state semantic movement to the earlier MTP path versus the later NTP path without comparing already-diverged parameter points. A false positive would promote generic parameter sharing as direct MTP supervision; a false negative would miss a real direct path. Exact reconstruction, direct masking, and frozen-path guards protect both errors.

## 8. Secondary Metrics

- actual versus predicted one-step $\Delta M_Z$;
- semantic tangent reachability $\|\nabla_\theta M_Z\|^2$;
- native H2 accuracy and target probability at $h_T$;
- branch-swap consistency for the fixed H2 head;
- $M_Z$ and branch-separation energy over time;
- early $M_Z$ area through step 50;
- Y1 loss, accuracy, and early loss area;
- frozen embedding/head drift;
- attention, MLP, LayerNorm, and position-group component velocities;
- cross-position gradient cosine and norm ratio for $L_D$ versus $L_I$.

## 9. Known Good / Known Bad / Known Confusing Cases

- Known good: `ntp_plus_direct_h2` and `mtp_all_k2` contain $L_D$ and should expose its positive same-checkpoint contribution.
- Known bad: reference-folded $h_T$ must have zero branch separation at step 0.
- Known confusing: $G_I$ can be positive without native H2 accuracy becoming high; this is indirect transfer, not implementation failure.
- Known confusing: full K2 can have positive $G_D$ but smaller total velocity if the remaining losses oppose it.
- Known confusing: a local velocity pass does not require every seed to reach perfect H2 accuracy by step 200.

## 10. Stage-Level Profiling Plan

| Stage | Local question | Pass / fail / unclear rule | Debug artifact | Handoff |
|---|---|---|---|---|
| static construction | are loss indices, folds, and aligned heads correct? | exact index/geometry/fold guards | `static_audit.json` | implementation valid/invalid |
| CPU smoke | do all four conditions emit finite tables? | one seed, two steps, all tables present | smoke result dir | proceed/fix |
| GPU smoke | does CUDA match the CPU contract? | same guards and finite values | ACP `gpu_smoke.log` | proceed/fix |
| remote full | do 20 tasks complete on four GPUs? | complete shard coverage | `run_manifest.json` | aggregate/fix |
| analysis | do decision rules apply without missing joins? | 5/5 seed coverage and central figure | `hypothesis_decision.json` | update claim |

## 11. Algorithm Specification

**Input:** four branch sequences, fixed embeddings, fixed aligned H1/H2 heads, reference decision states, condition mask, and checkpoints.  
**Parameters:** `d_model=64`, one layer/head, SGD `0.003`, 15,000 steps, virtual steps `0.0015/0.003`.  
**Intermediate variables:** folded $h_T$, $M_Z$, $L_D,L_I,L_S,L_R$, parameter gradients, component velocities, virtual-step margins.  
**Steps:** build a common per-seed reference; apply the condition mask; at each checkpoint compute the loss partition and all gradients; verify reconstruction; measure virtual updates; then take the active SGD step.  
**Outputs:** `path_velocity.csv`, `parameter_group_velocity.csv`, `finite_step.csv`, `curve_metrics.csv`, `validity_guards.csv`, `coverage_audit.csv`.  
**Pass conditions:** section 12.  
**Failure reasons:** invalid indices, nonaligned heads, nonidentical folded decision state, missing parameter groups, frozen-path movement, decomposition residual, unresolved velocity, or nonlinear sign failure.

## 12. Success / Failure / Insufficient Evidence

**Supported:** all validity guards pass; $G_D>0$ in at least 4/5 seeds; same-checkpoint mask reconstruction passes; full net velocity and one-step fidelity pass in at least 4/5; direct-enabled early native-margin area exceeds matched baselines in at least 4/5; Y1 guard passes.

**Weakened:** implementation is valid but $G_D$ is nonpositive/unresolved, later indirect transfer matches direct native velocity and trajectory, or local loss damage explains the gap.

**Partial:** direct local velocity is supported but finite-step or early ordering is not; retain only the same-checkpoint parameter claim.

**Insufficient:** any construction, frozen-path, numerical, decomposition, or coverage guard fails.

## 13. What This Cannot Claim

- MTP beats NTP on natural language or LLM downstream tasks;
- NTP cannot learn the delayed variable;
- the direct path dominates throughout training;
- SGD margin velocity equals sample/token efficiency;
- larger K is better;
- AdamW or trainable-head dynamics have the same split;
- MoE routing preservation or expert utility follows.

## 14. Review Notes And Protocol Changes

The user authorized subsequent anchor iterations and full runs without separate approval. To prevent mechanism drift, this protocol keeps K=2 and changes only loss masks. It explicitly treats NTP's later $h_{T+1}\rightarrow S_Z$ loss as a valid semantic path rather than a negative control. This anchor is the last controlled parameter-path bridge before the research line moves to a downstream-grounded semantic proxy.

Smoke revision: a valid 200-step one-seed run already showed the predicted direct/masked margin ordering, but all-position H2-background conditions had not yet learned the local Y1 target because each position contributes only about one sequence-length fraction of the averaged loss. The full window was therefore aligned with A11_10 at 15,000 steps. No condition, metric, or claim boundary changed.
