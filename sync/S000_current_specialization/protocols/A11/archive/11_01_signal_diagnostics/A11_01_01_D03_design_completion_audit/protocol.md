# Protocol: A11_02b Advisor K=2 Design Completion Audit

## 0. Approval Snapshot

**Approval status:** approved by the user for implementation and remote 4-GPU full run on 2026-07-10.  
**Purpose:** execute every operationally defined audit in the advisor K=2 shared-trunk design that A11_02 did not complete.  
**Primary anchor:** `11_02b_advisor_design_completion_audit_anchor.md`.  
**Decision question:** Does useful K=2 second-token supervision survive the complete diagnostic suite, and does negative gradient geometry predict realized $L_1$ harm?  
**Experiment role:** root-cause and metric-completion audit.  
**Primary metric:** clause-level design coverage plus matched-condition relation among $U_2,c_h,c_s,\rho$, and realized $L_1$ change.  
**Claim boundary:** controlled one-layer synthetic K=2 only.  
**Minimal setup:** both objective scopes, A/B/C regimes, original model controls, 5 seeds, deep diagnostics, lambda audit, fully separated upper bound.  
**Pass:** every design clause has valid evidence and A-clean is distinguished from redundant/noisy controls without unexplained $L_1$ damage.  
**Fail:** A-clean and C-noisy are indistinguishable, diagnostics are internally inconsistent, or conflict predicts damage that separation cannot localize.  
**Insufficient:** diagnostic gradients are numerically invalid, refinement buckets collapse, or fewer than 5 seeds complete.  
**Cannot claim:** natural-language or general MTP superiority.  
**Approval decision:** run after smoke and two implementation audits.

## 1. Terminology / Definitions

| Term | Plain meaning | Formula / computation | Decision role | Cannot prove |
|---|---|---|---|---|
| refinement KL $D_t$ | distribution change after revealing $Y_1$ | KL of refined head-1 and earlier head-2 predictions | duplicate-target difficulty | semantic usefulness alone |
| refinement gain $G_t$ | target log-probability improvement after $Y_1$ | negative head-2 log-prob plus refined head-1 log-prob | bucket variable | causal gradient harm |
| hidden cosine $c_h$ | horizon-gradient alignment at the shared activation | cosine of hidden gradients | tests Jacobian rotation with $c_s$ | final training state |
| parameter cosine $c_s$ | horizon-gradient alignment in a parameter group | cosine of $g_1,g_2$ | local conflict diagnostic | harmful interference alone |
| usefulness $U_2$ | whether descending $L_2$ lowers frozen branch-readout loss | $\langle\nabla R_\phi,g_2\rangle$ | task-directed gradient evidence | long-term causality |
| separation $\Delta_h$ | branch-center distance in hidden space | mean pairwise squared center distance | representation audit | native usability |
| fully separated | independent trunks for the two horizons | no shared horizon parameters | conflict upper bound | capacity-matched method gain |

## 2. Anchor Alignment

The protocol adds only diagnostics or controls explicitly requested in the source advisor design. It does not change the original A11_02 research question.

## 3. Tested Hypotheses

H1-H5 are defined in the primary anchor. Each is judged separately; no aggregate score can override a failed noisy-control guard.

## 4. Rival Explanations

Probe false positive, extra separated capacity, vanishing $g_1$, objective-scope background loss, duplicate-target difficulty, and noise memorization are guarded explicitly.

## 5. Data / Model / Objective

Original matrix at $\lambda=1$:

```text
data: A_clean / B_redundant / C_noisy
models: ntp_baseline / shared_trunk_two_token / shared_attention_separate_expert
init: random / identical_branch
scope: decision_only / all_positions_lm_control
seeds: 971,972,973,974,975
```

Targeted additions:

```text
A_clean shared_trunk: lambda 0.25 / 0.5 / 1.0
A_clean fully_separated_two_token: lambda 1.0
```

Fixed model/training defaults follow A11_02: one layer, `d_model=64`, `4000` steps, profile every `200`, deep diagnostics at step `0` and final.

## 6. Conditions, Seeds, And Checkpoints

| Item | Clause tested | Why needed | Evidence | Pass | Fail | Insufficient | Table |
|---|---|---|---|---|---|---|---|
| original matrix | signal/redundant/noisy | reproduce core decision | primary | prior ordering reproduced | ordering changes | seed failure | `tables/core_outcomes.csv` |
| lambda audit | conflict strength | test dose response | primary | geometry/damage relation interpretable | unexplained nonmonotonicity | scale invalid | `tables/lambda_local_cost.csv` |
| fully separated | localization | upper-bound no-sharing control | secondary | removes shared conflict | conflict remains on independent params | wiring invalid | `tables/separation_control.csv` |
| duplicate refinement | $D_t,G_t$ | test forecast refinement | primary | valid nondegenerate values | target alignment wrong | bucket collapse | `tables/refinement_dynamics.csv` |
| hidden/parameter gradients | $c_h,c_s,r,\rho$ | test Jacobian rotation | primary | finite and comparable | inconsistent gradients | vanishing norms | `tables/gradient_timeline.csv` plus raw hidden-gradient table |
| usefulness | $U_2$ | task-directed gradient | primary | A differs from C | C matches A | probe invalid | `tables/usefulness_summary.csv` |
| representation | probes and $\Delta_h$ | retention/separation | guard | A native+separated | probe-only false positive | rank failure | raw probe and representation-separation tables |

## 7. Primary Metric

The primary result is the matched-condition decomposition table joining target information, refinement difficulty, gradient geometry, task-directed usefulness, realized local loss, and native branch behavior. Harm requires realized $L_1$ damage; negative cosine alone is never a pass/fail criterion.

## 8. Secondary Metrics

Head-1/head-2/joint accuracy, branch swap, probe accuracy/CE at four positions, gradient norms, target probability, per-bucket losses, and local/global objectives.

## 9. Known Good / Known Bad / Known Confusing Cases

- Known good: A-clean shared-trunk all-position learns head-2 and swap.
- Known bad: C-noisy head-2 stays near $1/16$ chance.
- Known confusing: C-noisy probe can be high; B-redundant can have perfect head-2 without new conditional branch information; $\rho$ is unstable when $g_1$ vanishes.

## 10. Stage-Level Profiling Plan

| Stage | Question | Pass | Debug artifact |
|---|---|---|---|
| smoke | wiring and schema valid | all tables nonempty | smoke manifest |
| step 0 | diagnostics finite before learning | guards finite or explicitly NA | deep profile rows |
| training | original learning behavior reproduced | losses and heads move as expected | history/profile |
| final | every clause adjudicable | 5/5 seeds and complete joins | coverage table |

## 11. Algorithm Specification

Deep profiling fits a detached linear branch readout, freezes it, differentiates its CE through the current hidden state, and computes $U_2$ against $g_2$. Refinement metrics compare head-2 at the decision prefix with head-1 one position later on the same $Y_2$. Quantile buckets use per-sample $G_t$ and record losses, accuracy, and gradient geometry.

## 12. Success / Failure / Insufficient Evidence

Each advisor clause receives one of `supported`, `weakened`, or `insufficient`. The overall run is complete only when no clause is missing due to implementation.

## 13. What This Cannot Claim

No natural-language, K>2, general sample-efficiency, MoE, or fair architecture-performance claim.

## 14. Review Notes And Protocol Changes

The broad Cartesian product was reduced without dropping a design clause: lambda variation is limited to the primary A-clean shared-trunk condition, and fully separated is limited to the A-clean upper-bound role. The final run completed as ACP job `pt-27zjtage`; result filenames above are the curated post-run evidence paths and do not change the approved question or condition matrix.
