# Protocol: A11_04 K=3 First-Informative-Horizon Experiment

Merge note: this protocol originally specified the decision-only scope. The all-position control was later run under `A11_04_02_k3_all_position_control` with the same data/model matrix and is now merged into this experiment as Scope B. The canonical result records are `summary.md` and `detailed.md` in this folder.

## 0. Approval Snapshot

Approval status: approved by user request on 2026-07-07; implementation and run requested.

Purpose: Test whether MTP advantage appears when the active horizon covers the first future token that contains the early branch variable.

Primary anchor: `Projects/from-attention-to-search/main/problem_anchors/11_informative_future_branch_mechanism/11_04_k3_first_informative_horizon_anchor.md`

Anchor decision question: In a $\tau=3$ branch-delayed task, does K=3 produce guarded branch recovery beyond K=1 and K=2 while preserving $Y_1,Y_2$ learning?

Anchor physical prior tested: If $K<\tau$, active losses contain no branch-specific target; if $K\ge\tau$ and $Y_\tau=S_Z$, low offset-$\tau$ loss requires $h_T$ to contain $Z$.

Anchor core model term tested: $\lambda_3\operatorname{CE}(q_3(\cdot\mid h_T),S_Z)$.

Anchor falsifier: If K=2 matches K=3 on the clean $\tau=3$ task without leakage, the first-informative-horizon explanation is weakened.

Experiment role: mechanism generalization and operationalization test.

Primary metric from anchor: `coverage_gap`, the guarded recovery gap between K=3 and the best non-covering condition.

Claim boundary from anchor: This experiment can support only a controlled horizon-coverage claim, not broad next-K scaling or natural-language transfer.

Minimal setup: Decision-only objective at the prediction site.

Basic configuration: `num_branches=4`, `filler_length=16`, `shared_context_length=4`, one-layer one-head Transformer, `d_model=64`, $\lambda_2=\lambda_3=1.0$, seeds `971-975`, both `identical_branch` and `random` initialization.

Conditions to run: `K1_fixed_3head`, `K2_active`, `K3_active`; clean $\tau=3$, noisy horizon-3, and redundant horizon-3 regimes.

Pass: K=3 has positive `coverage_gap`, local guards pass, and noisy controls remain negative.

Fail: K=2 matches K=3 without leakage; all conditions recover equally; or K=3 wins only by harming local targets.

Insufficient: K=3 does not learn despite direct target, leakage is unresolved, or the evaluation decoder is unstable.

Cannot claim: Larger K always helps, K=2 is generally useless, curriculum helps, or natural-language long-horizon learning improves.

Approval decision: run.

## 1. Terminology / Definitions

| Term | Plain meaning | Concrete object / computation | Unit or formula | Why it matters | Cannot prove |
| --- | --- | --- | --- | --- | --- |
| first informative horizon $\tau$ | First future offset adding information about $Z$ | $\tau=\min\{j:I(Z;Y_j\mid Y_{<j})>0\}$ | token offset | Core mechanism variable | Natural-language horizon structure |
| covering condition | Active horizon includes $\tau$ | $K\ge\tau$ | Boolean | Should receive direct branch supervision | Optimization success |
| non-covering condition | Active horizon stops before $\tau$ | $K<\tau$ | Boolean | Should not receive direct branch supervision | No incidental leakage |
| K=1 | Only horizon 1 active | active horizons `{1}` | condition | NTP-style baseline | All NTP behavior |
| K=2 | Horizons 1 and 2 active | active horizons `{1,2}` | condition | Non-covering control in $\tau=3$ | K=2 useless generally |
| K=3 | Horizons 1, 2, and 3 active | active horizons `{1,2,3}` | condition | Covering condition | Broad next-K scaling |
| guarded score $Q_K$ | Conservative branch recovery score | $\min\{A_K,P_K,S_K\}$ | 0 to 1 | Guards probe-only false positives | Full causal proof |
| `coverage_gap` | K=3 advantage over non-covering horizons | $\operatorname{AUC}_Q(3)-\max(\operatorname{AUC}_Q(1),\operatorname{AUC}_Q(2))$ | score gap | Primary metric | Step-threshold superiority by itself |

## 2. Anchor Alignment

Decision question: Does K=3 produce branch recovery when K=1/K=2 do not in a $\tau=3$ task?

Physical prior tested: horizon coverage of the first informative token creates direct branch supervision.

Core model term tested: $\lambda_3\operatorname{CE}(q_3(\cdot\mid h_T),S_Z)$.

Falsifier: K=2 matches K=3 without leakage.

Claim boundary: controlled first-informative-horizon coverage only.

## 3. Tested Hypothesis

H1: In clean $\tau=3$, K=3 has higher guarded branch recovery than K=1/K=2.

H2: K=3 does not obtain the gain by damaging $Y_1,Y_2$ learning.

H3: Noisy and redundant controls do not create the same coverage claim.

## 4. Rival Explanations

Extra heads, loss scale, branch leakage into $Y_1/Y_2$ or filler, probe-only artifacts, and optimization failure.

## 5. Data / Model / Algorithm / Objective

Clean $\tau=3$ data:

```text
BR_z F00 ... F15 U00 ... U03 A_SHARED C_SHARED S_z STOP
```

Targets:

$$
Y_1=A,\qquad Y_2=C,\qquad Y_3=S_Z.
$$

Information structure:

$$
I(Z;Y_1)=0,\qquad I(Z;Y_2\mid Y_1)=0,\qquad I(Z;Y_3\mid Y_1,Y_2)=H(Z).
$$

Objective:

$$
L_K=\sum_{j=1}^{K}\lambda_j\operatorname{CE}(q_j(\cdot\mid h_T),Y_j).
$$

K=1/K=2 do not include a direct $S_Z$ target. K=3 does.

## 6. Conditions, Seeds, And Checkpoints

| Item | Anchor clause tested | Model term / rival explanation | Why needed | Evidence | Pass | Fail | Insufficient | Figure/table |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| clean K=1 | non-covering baseline | no branch target | baseline | $Q_1(t)$ | low/delayed | high unexplained | unstable eval | main curve |
| clean K=2 | non-covering control | active $Y_1,Y_2$ only | separates next-two from coverage | $Q_2(t)$ | similar to K=1 | matches K=3 | leakage unclear | main curve |
| clean K=3 | covering condition | active $Y_3=S_Z$ | main test | $Q_3(t)$, native head3 | high/earlier | fails | optimization unclear | main curve |
| noisy K=3 | noisy guard | $Y_3\perp Z$ | false-positive guard | head3 near chance | stays low | behaves like clean | high variance | guard table |
| redundant control | redundancy guard | earlier target reveals $Z$ | separates new information from continuation | explained by earlier target | no new claim | unexplained gain | ambiguous | guard table |

Seeds: `971,972,973,974,975`.

Checkpoints: every `500` steps, `15000` steps total.

## 7. Primary Metric

$$
\Delta_{\mathrm{cov}}=
\operatorname{AUC}_Q(3)-\max\{\operatorname{AUC}_Q(1),\operatorname{AUC}_Q(2)\}.
$$

This decides the judgment because the anchor asks whether covering $\tau$ changes branch recovery relative to non-covering horizons.

## 8. Secondary Metrics

`T_0.9_Q`, native head-3 accuracy, branch-swap consistency, frozen branch probe, $Y_1/Y_2$ local losses, and noisy/redundant controls.

## 9. Known Good / Known Bad / Known Confusing Cases

Known good: A11_01 validates the $\tau=2$ special case.

Known bad: noisy targets should not produce native informative-horizon accuracy.

Known confusing: high probe without informative-horizon prediction and swap is not enough.

## 10. Stage-Level Profiling Plan

| Stage | Local question | Input evidence | Pass / fail / unclear rule | Debug artifact | Handoff |
| --- | --- | --- | --- | --- | --- |
| data audit | Is $\tau=3$ actually clean? | sample/frequency table | no leakage / leakage | sample table | detailed |
| smoke | Does train/eval/aggregate work? | smoke logs | pass / crash | smoke output | not central |
| coverage curve | Does K=3 exceed K=1/K=2? | $Q_K(t)$ | pass/fail/insufficient | main figure/table | summary |
| guard audit | Are local/noisy/redundant guards valid? | guard metrics | pass/fail | guard table | summary |

## 11. Algorithm Specification, If Nontrivial

Train matched K=1/K=2/K=3 models. At each checkpoint, evaluate the same frozen-state branch decoder/probe/swap pipeline and compute $Q_K(t)$.

## 12. Success / Failure / Insufficient Evidence

Success: K=3 has positive `coverage_gap`, local guards pass, and noisy guard stays negative.

Failure: K=2 matches K=3 without leakage, all conditions recover equally, or K=3 wins only through local degradation.

Insufficient: direct target does not learn, leakage unresolved, or evaluation unstable.

## 13. What This Cannot Claim

No claim that larger K always helps, K=2 is generally useless, curriculum helps, or natural-language learning improves.

## 14. Review Notes And Protocol Changes

The executed first pass follows the audited choices: decision-only scope, both `identical_branch` and `random` init, K=1 fixed 3-head capacity baseline, `filler_length=16`, A11_03/A11_04 run as separate anchors, and no separate-expert condition in the main matrix.

2026-07-08 merge update: the all-position LM-style control is treated as the second scope of the same experiment, not a separate research question. It changes only the training scope from decision-only to all-position while keeping the data/model/condition matrix and decision-prefix evaluation comparable. Its purpose is to test the boundary of the direct single-prefix theorem under LM-style background losses.
