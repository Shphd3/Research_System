# Protocol: A11_02 Two-Token Shared-Trunk Signal / Interference

Status: canonical protocol, approved for the first `decision_only` run. `decision_only` was executed on 2026-07-07; `all_positions_lm_control` remains unrun.

## 0. Approval Snapshot

**Approval status:** approved for `decision_only`; executed on 2026-07-07.

**Purpose:** Classify whether the K=2 second-token loss $L_2$ in a shared-trunk Transformer is useful branch signal, redundant signal, noisy target, or useful-but-interfering gradient source.

**Primary anchor:** `Projects/from-attention-to-search/main/problem_anchors/11_informative_future_branch_mechanism/11_02_two_token_shared_trunk_signal_interference_anchor.md`

**Anchor decision question:** In a K=2 one-layer causal Transformer, does branch-relevant $L_2$ become a usable shared-trunk representation without harming $L_1$ next-token learning? If it harms $L_1$, does shared-attention separate-expert structure localize and reduce the interference?

**Physical priors tested:** data-information prior; representation-usefulness prior; shared-gradient compatibility prior.

**Core model terms tested:** $I(B;Y_2\mid Y_1)$, branch probe from hidden states, and parameter-group gradient metrics $c_s,r,\rho$ for $g_1=\nabla L_1$ and $g_2=\nabla L_2$.

**Falsifier:** Regime A-clean and Regime C-noisy behave the same; or $L_2$ improves neither head-2 branch prediction nor branch probe; or noisy control shows branch gain; or separate expert fails to reduce any measured interference when interference is present.

**Experiment role:** root-cause / metric audit. This is not method construction, not curriculum, and not K>2.

**Primary decision object:** `two_token_signal_class`.

**First primary metric:** `A_vs_C_branch_probe_gain_at_prediction_site`.

**Claim boundary:** This protocol only classifies K=2 shared-trunk two-token dynamics in controlled synthetic regimes. It cannot claim MTP universally improves NTP, cannot claim K>2 behavior, and cannot claim natural-language transfer.

**Minimal setup:** one-layer causal Transformer; three data regimes; three model conditions; multiple seeds; primary `objective_scope=decision_only`; no curriculum; no K>2.

**Basic configuration to audit:** `num_branches=4`, `filler_length=16`, `shared_context_length=4`, `lambda_offset2=1.0`, at least `5` seeds, normal random branch init plus identical branch-token init. The user approved the numeric configuration on 2026-07-07. All non-target parameters must be unified across comparisons.

**Data regimes:**

- `A_clean`: $Y_1=U$, $Y_2=S_B$.
- `B_redundant`: $Y_1=S_B$, $Y_2=R(S_B)=T_B$, where $R(S_b)=T_b$ is a fixed one-to-one local continuation map.
- `C_noisy`: $Y_1=U$, $Y_2=Z$, where $Z\perp B$ and $Z$ is sampled iid per occurrence from a fixed noise-token distribution $P_Z$.

**Model conditions:**

- `ntp_baseline`: one head, $L_1$ only.
- `shared_trunk_two_token`: shared attention + shared MLP, two heads, $L_1+\lambda L_2$.
- `shared_attention_separate_expert`: shared attention, horizon-specific experts, two heads.

**Pass:** Regime A-clean gives branch probe/head-2/swap gain over NTP, Regime C-noisy does not, and gradient metrics either show no material interference or identify useful-but-interfering behavior. If interference appears, separate expert improves $L_1$ preservation without losing branch metrics.

**Fail:** Regime A-clean does not improve branch probe/head-2/swap; Regime C-noisy improves similarly; gradient metrics do not explain observed $L_1$ degradation; or separate expert does not reduce interference while conflict remains unexplained.

**Insufficient:** data audit fails, active loss/head wiring is wrong, probe split is too small, C-noisy can be memorized, gradient profiling changes training, or too few seeds finish.

**Cannot claim:** curriculum works; K>2 works; natural-language long-horizon reasoning improves; expert separation is generally useful; MTP always beats NTP.

**Approval decision:** approved for the first implementation with `objective_scope=decision_only`. The next approval decision is whether to implement and run `all_positions_lm_control`.

## 1. Terminology / Definitions

| Term | Plain meaning | Concrete object / computation | Unit or formula | Why it matters | What it cannot prove |
|---|---|---|---|---|---|
| `two_token_signal_class` | final experiment classification | useful / redundant / noisy / useful-but-interfering / attention-bottleneck / invalid | categorical | decides the next research route | theorem proof |
| `A_vs_C_branch_probe_gain_at_prediction_site` | branch-probe gain specific to A-clean over C-noisy | $\Delta_{\mathrm{probe}}(A,T)-\Delta_{\mathrm{probe}}(C,T)$ | accuracy delta | tests whether $L_2$ is branch-specific useful signal | head-2 usability |
| `single_prefix_head2_accuracy` | head-2 predicts $Y_2$ from the same $h_T$ | top-1 accuracy | 0 to 1 | tests whether the $L_2$ target is learnable | representation necessarily encodes branch |
| `branch_swap_preference` | after swapping only the early branch token, head-2 prefers the swapped branch suffix | swap success / logit margin | rate or margin | causal guard | excludes all memorization routes |
| `branch_probe_accuracy` | linear branch readout from frozen hidden states | linear probe accuracy | 0 to 1 | tests branch retention in hidden states | native head usability |
| `branch_probe_cross_entropy` | cross-entropy of the branch probe | $\operatorname{CE}(S_\phi(h),B)$ | loss | more sensitive than accuracy near saturation | nonlinear readability |
| $c_s$ | cosine between $L_1$ and $L_2$ gradients | $\langle g_1,g_2\rangle/(\|g_1\|\|g_2\|)$ | -1 to 1 | detects shared-parameter conflict | sufficient causal explanation of training |
| $r$ | norm ratio of $L_2$ gradient to $L_1$ gradient | $\|g_2\|/\|g_1\|$ | ratio | detects whether $L_2$ dominates updates | whether direction is useful |
| $\rho$ | preservation of the $L_1$ update direction under the combined update | $\langle g_1+\lambda g_2,g_1\rangle/\|g_1\|^2$ | scalar | detects whether $L_2$ weakens next-token update | long-term generalization |
| `init_mode=random` | standard random initialization | branch-token embeddings initialized independently | condition label | tests whether the effect survives ordinary initialization | clean objective-only mechanism |
| `init_mode=identical_branch` | symmetry-controlled initialization | all `BR_b` token embeddings start identical but remain trainable | condition label | prevents fixed-next-one from using random branch identity leakage | robustness under random init |
| `loss_site=prediction_site` | the only training position where losses are computed | final prefix hidden state before $Y_1$ | position label | keeps objective aligned with the theory | full-token language modeling |
| `objective_scope=decision_only` | training loss only at the decision prefix | losses computed at `prediction_site` | condition label | directly tests $h_T\to(Y_1,Y_2)$ | standard LM training behavior |
| `objective_scope=all_positions_lm_control` | LM-style control with losses at all valid positions | losses averaged over valid token positions | optional condition | tests whether the conclusion survives background LM loss | clean theory isolation |
| parameter unification | all non-target factors fixed | same data/model/optimizer/seeds/eval contract inside each comparison | implementation rule | prevents hidden confounds | all implementation drift |
| `fully_separated_control` | no shared representation path between horizons | independent horizon-1 and horizon-2 trunks | optional condition | upper-bound for eliminating shared interference | fair capacity-matched method comparison |

## 2. Anchor Alignment

**Decision question:** Is $L_2$ in K=2 shared-trunk training useful, redundant, noisy, or interfering?

**Physical priors tested:** data-level branch information; representation gain; shared-gradient compatibility.

**Core model terms tested:** $I(B;Y_2\mid Y_1)$, branch probe loss, $c_s,r,\rho$.

**Falsifier:** A-clean and C-noisy are indistinguishable, C-noisy shows branch gain, or gradient diagnostics do not explain observed interference.

**Claim boundary:** K=2 synthetic shared-trunk dynamics only.

## 3. Tested Hypotheses

**H1: Useful branch signal.** A-clean two-token improves branch representation and head-2 prediction; C-noisy does not.

**H2: Redundancy.** B-redundant does not add branch gain beyond what $Y_1$ already supplies.

**H3: Shared-trunk interference.** If A-clean $L_2$ improves branch metrics but hurts $L_1$, negative $c_s$ or low $\rho$ should identify the shared parameter group causing interference.

**H4: Expert-separation localization.** If interference is mainly in MLP/expert parameters, shared-attention separate-expert should preserve $L_1$ while retaining head-2/probe gains.

**H5: Diagnostic validity.** C-noisy should remain near chance on branch-specific metrics; otherwise the setup is invalid.

## 4. Rival Explanations

| Rival explanation | Protocol guard |
|---|---|
| $L_2$ success is local or redundant, not branch-specific | Regime B-redundant |
| $L_2$ success is arbitrary auxiliary loss | Regime C-noisy |
| branch metric improvement is probe-only artifact | require head-2 accuracy and branch-swap preference |
| head-2 success hurts $L_1$ | track `L1_structured_loss_delta` and $\rho$ |
| separate experts help only by extra parameters | compare to shared-trunk and inspect where gradient conflict disappears |
| noisy target is memorized | train/eval resampling for C-noisy and held-out probe/eval split |

## 5. Data / Model / Objective

**Shared prefix:**

```text
BR_b F_1 ... F_L U_1 U_2 U_3 U_4
```

**Regime A-clean:**

$$
Y_1=U,\qquad Y_2=S_B.
$$

**Regime B-redundant:**

$$
Y_1=S_B,\qquad Y_2=R(S_B)=T_B,\qquad R(S_b)=T_b.
$$

Here $S_b$ and $T_b$ are unique branch-indexed token sets. $Y_2$ may be branch-specific by itself, but after $Y_1$ is known it adds no information about $B$:

$$
I(B;Y_2\mid Y_1)=0.
$$

**Regime C-noisy:**

$$
Y_1=U,\qquad Y_2=Z,\qquad Z\sim P_Z,\qquad Z\perp B.
$$

$P_Z$ is fixed across train and evaluation, but each occurrence draws a fresh $Z$. Do not create a fixed branch-to-noise or prefix-to-noise table.

**Objectives:**

NTP:

$$
L_{\mathrm{NTP}}=L_1.
$$

Shared-trunk two-token:

$$
L_{\mathrm{2tok}}=L_1+\lambda L_2.
$$

Separate-expert:

$$
L_{\mathrm{sep}}=\operatorname{CE}(p^{(1)}(Y_1\mid h_T^{(1)}),Y_1)+\lambda\operatorname{CE}(p^{(2)}(Y_2\mid h_T^{(2)}),Y_2).
$$

### 5.1 Loss Sites And Optimization Targets

The primary experiment uses `objective_scope=decision_only`: training losses are computed only at the final prefix state, `prediction_site`, immediately before $Y_1$. The probe positions `after_branch_token`, `middle_filler`, and `shared_local_context` are diagnostic positions only; they do not create main-model training loss.

For `ntp_baseline`:

$$
L_{\mathrm{active}}=L_1=\operatorname{CE}(p^{(1)}(Y_1\mid h_T),Y_1).
$$

No $L_2$ gradient is used. The implementation should use a true one-head model when practical. If a second head exists for code symmetry, its loss weight is zero and it is not part of optimization.

For `shared_trunk_two_token`:

$$
L_{\mathrm{active}}=L_1+\lambda L_2,
$$

where

$$
L_2=\operatorname{CE}(p^{(2)}(Y_2\mid h_T),Y_2).
$$

Both heads read the same $h_T$. $L_1$ and $L_2$ both update embedding, shared attention, and shared MLP parameters; each loss also updates its own head.

For `shared_attention_separate_expert`:

$$
L_{\mathrm{active}}=L_1+\lambda L_2.
$$

$L_1$ updates embedding, shared attention, expert_1, and head_1. $L_2$ updates embedding, shared attention, expert_2, and head_2. Therefore this condition can reduce MLP/expert interference but cannot remove embedding or shared-attention interference.

Branch-probe losses are trained only on frozen hidden states and do not update the main model. Gradient profiling computes $g_1$ and $g_2$ separately for measurement, then clears gradients before the normal training update.

Optional LM-style robustness control:

Given a full sequence $x_0,\ldots,x_{N-1}$, define valid position sets $\mathcal P_1=\{t:t+1<N\}$ and $\mathcal P_2=\{t:t+2<N\}$. Then:

$$
L_{\mathrm{allpos}}^{(1)}=\frac{1}{|\mathcal P_1|}\sum_{t\in\mathcal P_1}
\operatorname{CE}(p^{(1)}(x_{t+1}\mid h_t),x_{t+1}),
$$

$$
L_{\mathrm{allpos}}^{(2)}=\frac{1}{|\mathcal P_2|}\sum_{t\in\mathcal P_2}
\operatorname{CE}(p^{(2)}(x_{t+2}\mid h_t),x_{t+2}).
$$

`objective_scope=all_positions_lm_control` uses $L_{\mathrm{active}}=L_{\mathrm{allpos}}^{(1)}$ for NTP and $L_{\mathrm{active}}=L_{\mathrm{allpos}}^{(1)}+\lambda L_{\mathrm{allpos}}^{(2)}$ for two-token models. This is a secondary robustness control. Primary evaluation still uses branch metrics at `prediction_site`.

If the all-position control changes the qualitative conclusion, the allowed claim becomes narrower: $L_2$ is useful or interfering only under the decision-site objective, not under LM-style background training.

### 5.2 Parameter Unification Contract

All experiments must change only named factors. Fixed factors:

```text
num_branches = 4
filler_length = 16
shared_context_length = 4
lambda_offset2 = 1.0
seeds = same 5 seeds for every compared condition
model depth / width / attention heads / dropout = same across matched conditions
optimizer / learning rate / weight decay / training steps = same across matched conditions
probe training config = same across matched conditions
gradient profiling interval = same across matched conditions
train/eval split and data generator seed policy = same across matched conditions
```

Allowed factors:

```text
data_regime: A_clean / B_redundant / C_noisy
model_condition: ntp_baseline / shared_trunk_two_token / shared_attention_separate_expert
init_mode: random / identical_branch
objective_scope: decision_only / all_positions_lm_control
```

Loss scale control: if `all_positions_lm_control` is run, each horizon loss is averaged over active positions before applying $\lambda$. Otherwise the control would change gradient scale, not only objective scope.

Capacity caveat: `shared_attention_separate_expert` has extra horizon-specific parameters. It is a localization diagnostic, not a fair method-performance claim. `fully_separated_control` has an even larger capacity difference and remains parked.

## 6. Conditions, Seeds, And Checkpoints

| Item | Anchor clause tested | Rival explanation | Evidence role | Pass | Fail | Insufficient | Table |
|---|---|---|---|---|---|---|---|
| `A_clean x ntp_baseline` | baseline branch retention | NTP may already encode branch | primary baseline | solves $Y_1$ | fails $Y_1$ | unstable | `per_seed_metrics.csv` |
| `A_clean x shared_trunk_two_token` | useful $L_2$ signal | no branch signal | primary | head-2/probe/swap high | no gain | partial seeds | `regime_condition_summary.csv` |
| `A_clean x shared_attention_separate_expert` | interference localization | expert separation useless | secondary/conditional | preserves $L_1$ and branch metrics | no improvement | no interference to localize | `regime_condition_summary.csv` |
| `B_redundant x all conditions` | redundancy control | $L_2$ is deterministic after $Y_1$ | guard | branch gain explained by $Y_1$ | acts like A without explanation | B invalid | `regime_condition_summary.csv` |
| `C_noisy x all conditions` | noisy control | leakage / arbitrary auxiliary gain | guard | branch metrics near chance | branch gain high | memorization risk | `regime_condition_summary.csv` |
| gradient profiling | shared conflict | hidden interference | diagnostic | $c_s,r,\rho$ explain $L_1$ delta | no relation | profiling alters training | `gradient_profile.csv` |
| `all_positions_lm_control` | objective-scope robustness | prefix-only objective may be artificial | secondary/conditional | same qualitative class as decision-only | class changes | too expensive / unstable | `objective_scope_summary.csv` |

Seeds: proposed `5` seeds.  
Checkpoints: final plus profiling every fixed interval, e.g. every `200` steps.

## 7. Primary Metric

The first primary metric is `A_vs_C_branch_probe_gain_at_prediction_site`:

$$
\Delta_{\mathrm{probe}}(A,T)-\Delta_{\mathrm{probe}}(C,T).
$$

It decides whether $L_2$ improves branch representation specifically when $Y_2$ carries branch information. It is primary because it separates useful branch signal from arbitrary auxiliary loss.

False positive risk: probe-only improvement without usable prediction. Guard: `single_prefix_head2_accuracy` and `branch_swap_preference`.

False negative risk: NTP already encodes branch under random initialization. Guard: identical branch-token initialization and multi-position probes.

## 8. Secondary Metrics

- `single_prefix_head2_accuracy`
- `single_prefix_joint_two_token_accuracy`
- `branch_swap_preference`
- `branch_probe_accuracy_by_position`
- `branch_probe_cross_entropy_by_position`
- `L1_structured_loss`
- `L2_structured_loss`
- `L1_global_loss`
- `L2_global_loss`
- `gradient_cosine_c_s_by_group`
- `gradient_norm_ratio_r_by_group`
- `rho_update_preservation_by_group`

## 9. Known Good / Known Bad / Known Confusing Cases

**Known good:** A-clean should reproduce the A11_01 direction in the shared-trunk two-token condition.

**Known bad:** C-noisy should not improve branch metrics; if it does, the experiment is invalid or leaking branch information.

**Known confusing:** B-redundant can have high head-2 accuracy because $Y_2$ is predictable from $Y_1$ or branch-labeled $Y_1$; this should not be interpreted as new branch information from $L_2$.

## 10. Stage-Level Profiling Plan

| Stage | Local question | Evidence | Pass / fail / unclear rule | Debug artifact | Handoff |
|---|---|---|---|---|---|
| data audit | Are A/B/C regimes correct? | sample table + mutual-information contract | fail if C leaks branch or B adds branch info | `sample_table.csv` | `detailed.md` |
| loss/head audit | Are active objectives correct? | active loss table | fail if NTP has head-2 loss or two-token lacks $L_2$ | `training_history.csv` | `detailed.md` |
| primary eval | Is A gain specific vs C? | probe/head-2/swap | pass if A improves and C does not | result tables | `summary.md` |
| gradient eval | Is interference measured by group? | $c_s,r,\rho$ | pass if metrics explain $L_1$ delta | `gradient_profile.csv` | `detailed.md` |
| expert eval | Does separate expert localize conflict? | condition comparison | pass if $L_1$ preserved and branch metrics retained | summary table | `summary.md` |

## 11. Algorithm Specification

Input: regimes, branches, filler length, shared context length, model condition, seed, $\lambda$.

Intermediate variables: $h$ at four probe positions; $L_1,L_2$; $g_1,g_2$ by parameter group; branch probe logits; head-1/head-2 logits.

Steps:

1. Generate train/eval data for A/B/C.
2. Train NTP, shared-trunk two-token, and shared-attention separate-expert conditions.
3. At profiling intervals, compute $L_1$ and $L_2$ gradients separately without changing training.
4. Evaluate head metrics, branch-swap, branch probes at four positions, and gradient metrics.
5. Aggregate per seed and classify `two_token_signal_class`.

Outputs:

```text
tables/per_seed_metrics.csv
tables/regime_condition_summary.csv
tables/probe_by_position.csv
tables/gradient_profile.csv
tables/branch_swap.csv
tables/refinement_metrics.csv
run_manifest.json
```

## 12. Success / Failure / Insufficient Evidence

**Success for useful signal:** A-clean improves branch probe/head-2/swap over NTP and C-noisy does not.

**Success for useful-but-interfering:** A-clean improves branch metrics but increases $L_1$ loss, with negative $c_s$ or low $\rho$ in shared groups.

**Success for expert localization:** separate expert improves $L_1$ preservation relative to shared-trunk two-token while keeping branch metrics.

**Failure:** A-clean does not improve branch metrics, C-noisy improves similarly, or all gradient diagnostics fail to explain observed degradation.

**Insufficient:** data leakage, broken loss wiring, probe split invalid, too few seeds, or gradient profiling changes training.

## 13. What This Cannot Claim

- It cannot claim curriculum works.
- It cannot claim K>2 works.
- It cannot claim natural-language transfer.
- It cannot claim all MTP objectives are useful.
- It cannot claim expert separation is generally better.
- It cannot replace the A11_01 proof; it builds on it.

## 14. Review Notes, Execution Notes, And Required User Decisions

User review resolved before implementation:

1. Regime B uses $Y_1=S_B,\;Y_2=R(S_B)=T_B$ with $R(S_b)=T_b$.
2. Regime C uses iid per-occurrence noise from a fixed distribution $P_Z$, with no branch-to-noise table.
3. The first run includes both `init_mode=random` and `init_mode=identical_branch`.
4. `num_branches=4`, `filler_length=16`, `shared_context_length=4`, and `5` seeds are fixed.
5. `fully_separated_control` remains parked.
6. `all_positions_lm_control` is reserved as the next objective-scope robustness control after `decision_only`.

Execution notes:

1. Main local run: `a11_02_decision_only_local2gpu_20260707_0411`.
2. Completion diagnostic: `a11_02_decision_only_completion_a_clean_shared_trunk_12000_20260707_0545`.
3. Remote ACP job `pt-tydhqbgx` was submitted but failed before aggregation; partial shard logs exist, and it is not the source of the completed evidence.
4. Result records are `summary.md` and `detailed.md` in this experiment folder.
