# Protocol: A11_03 K=2 Semantic Efficiency Curves

## 0. Approval Snapshot

Approval status: approved by user request on 2026-07-07; implementation and run requested.

Purpose: Test whether the K=2 next-two representation requirement becomes a learning-efficiency advantage over matched fixed-next-one.

Primary anchor: `Projects/from-attention-to-search/main/problem_anchors/11_informative_future_branch_mechanism/11_03_k2_semantic_efficiency_anchor.md`

Anchor decision question: In the controlled K=2 branch-delayed task, does next-two make $Z$ recoverable from $h_T$ earlier than matched fixed-next-one without damaging $Y_1$ learning?

Anchor physical prior tested: When $Y_1=A$ is shared and $Y_2=S_Z$ is branch-specific, next-two gives the same $h_T$ direct branch supervision that fixed next-one lacks.

Anchor core model term tested: $\lambda_2\operatorname{CE}(q_2(\cdot\mid h_T),S_Z)$.

Anchor falsifier: If next-two does not improve `T_0.9_eval` or early `AUC_Q` over matched fixed-next-one, the K=2 learning-efficiency claim is not supported.

Experiment role: metric audit and efficiency test.

Primary metric from anchor: `T_0.9_eval`, the first training step where $Q_{\mathrm{eval}}(t)\ge0.9$ for consecutive evaluations.

Claim boundary from anchor: This experiment can test controlled K=2 learning efficiency only. It cannot prove universal MTP superiority, natural-language transfer, or K>2 behavior.

Minimal setup: Decision-only objective at the prediction site.

Basic configuration: `num_branches=4`, `filler_length=16`, `shared_context_length=4`, one-layer one-head Transformer, `d_model=64`, $\lambda_2=1.0$, seeds `971-975`, both `identical_branch` and `random` initialization.

Conditions to run: `fixed_next_one_2head` and `shared_trunk_next_two`; clean, noisy, and redundant data regimes.

Pass: next-two reaches $Q_{\mathrm{eval}}\ge0.9$ earlier and has higher early `AUC_Q`, while local $Y_1$ guard passes and noisy controls remain negative.

Fail: fixed-next-one matches or beats next-two, next-two wins only by damaging $Y_1$, or noisy targets pass the same guards.

Insufficient: neither condition reaches threshold, evaluation decoder is unstable, or leakage is unresolved.

Cannot claim: MTP generally improves NTP; NTP cannot encode branch information; K>2 follows automatically.

Approval decision: run.

## 1. Terminology / Definitions

| Term | Plain meaning | Concrete object / computation | Unit or formula | Why it matters | Cannot prove |
| --- | --- | --- | --- | --- | --- |
| fixed next-one | Capacity-matched baseline with only horizon 1 active | same trunk and two heads; loss is $L_1$ | condition | Controls extra head capacity | All NTP behavior |
| next-two | Same $h_T$ predicts two future tokens | loss is $L_1+\lambda_2L_2$ | condition | Main MTP condition | Universal advantage |
| matched evaluation decoder | Shared evaluation readout for all conditions | linear readout from frozen $h_T$ to branch label / suffix identity | accuracy / CE | Makes fixed-next-one comparable with next-two | Native head use |
| native head-2 accuracy | Accuracy of trained offset-2 head | top-1 accuracy of $q_2(\cdot\mid h_T)$ on $Y_2$ | 0 to 1 | Checks whether next-two learned its own target | Fair NTP comparison |
| guarded score $Q_{\mathrm{eval}}$ | Conservative branch recovery score | $\min\{A_{\mathrm{eval}},P_{\mathrm{eval}},S_{\mathrm{eval}}\}$ | 0 to 1 | Guards against probe-only false positives | Full causal proof |
| `T_0.9_eval` | Time to guarded recovery | first step where $Q_{\mathrm{eval}}\ge0.9$ for consecutive evaluations | steps | Primary efficiency metric | Final capability limit |

## 2. Anchor Alignment

Decision question: Does next-two recover $Z$ from $h_T$ earlier than fixed next-one?

Physical prior tested: $L_2$ provides direct branch-specific supervision.

Core model term tested: $\lambda_2\operatorname{CE}(q_2(\cdot\mid h_T),S_Z)$.

Falsifier: no improvement in `T_0.9_eval` or `AUC_Q`.

Claim boundary: controlled K=2 efficiency only.

## 3. Tested Hypothesis

H1: Next-two reaches guarded branch recovery earlier than fixed-next-one in the clean K=2 regime.

H2: The gain does not come from degraded $Y_1$ learning.

H3: The gain is specific to branch-informative $Y_2$, not noisy future loss.

## 4. Rival Explanations

Extra capacity, branch-token leakage, probe-only artifacts, local-loss tradeoff, and arbitrary auxiliary-loss effects.

## 5. Data / Model / Algorithm / Objective

Clean data:

```text
BR_z F00 ... F15 U00 ... U03 A_SHARED S_z STOP
```

Targets:

$$
Y_1=A,\qquad Y_2=S_Z.
$$

Fixed-next-one objective:

$$
L_{\mathrm{fixed1}}=L_1.
$$

Next-two objective:

$$
L_{\mathrm{next2}}=L_1+\lambda_2L_2.
$$

The runner evaluates frozen $h_T$ at checkpoints with a matched evaluation decoder, a branch probe, and branch-swap prefixes.

## 6. Conditions, Seeds, And Checkpoints

| Item | Anchor clause tested | Model term / rival explanation | Why needed | Evidence | Pass | Fail | Insufficient | Figure/table |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| clean fixed next-one | baseline efficiency | no active $L_2$ | baseline | $Q(t)$ | below next-two | matches next-two | unstable eval | curves/table |
| clean next-two | main mechanism | active $L_2=S_Z$ | main test | $Q(t)$, native head2 | earlier recovery | no gain | no threshold | curves/table |
| noisy next-two | noisy auxiliary guard | $Y_2\perp Z$ | false-positive guard | native head2 near chance | stays low | behaves like clean | high variance | guard table |
| redundant next-two | redundancy guard | $Y_2=R(Y_1)$ | separates new information from local continuation | explained by $Y_1$ | no new claim | unexplained gain | ambiguous | guard table |

Seeds: `971,972,973,974,975`.

Checkpoints: every `500` steps, `10000` steps total.

## 7. Primary Metric

$$
T_{0.9}^{\mathrm{eval}}=\inf\{t:Q_{\mathrm{eval}}(t)\ge0.9\text{ for consecutive evaluations}\}.
$$

This decides the judgment because the anchor asks whether next-two learns the branch variable earlier, not merely whether it eventually reaches a high final score.

## 8. Secondary Metrics

`AUC_Q`, `final_Q`, native head-2 accuracy, branch-swap consistency, $Y_1$ accuracy/loss, and noisy/redundant control outcomes.

## 9. Known Good / Known Bad / Known Confusing Cases

Known good: A11_01 next-two reaches perfect final offset-2, probe, and swap.

Known bad: A11_01 fixed-next-one remains branch-blind under identical branch initialization.

Known confusing: A11_02 shows that branch probe can be high in noisy controls; probe alone is not decisive.

## 10. Stage-Level Profiling Plan

| Stage | Local question | Input evidence | Pass / fail / unclear rule | Debug artifact | Handoff |
| --- | --- | --- | --- | --- | --- |
| data audit | Does the generated data match the intended regimes? | sample table | no leakage / leakage | sample table | detailed |
| smoke | Does train/eval/aggregate work? | smoke logs | pass / crash | smoke output | not central |
| main curve | Does next-two recover earlier? | $Q(t)$ | pass/fail/insufficient | curve table | summary |
| guard audit | Are local and noisy guards valid? | local/noisy metrics | pass/fail | guard table | summary |

## 11. Algorithm Specification, If Nontrivial

At each checkpoint, freeze the model, collect $h_T$, fit the same linear evaluation decoder and branch probe on the training split, evaluate on the held-out split, compute branch-swap consistency, then compute $Q_{\mathrm{eval}}(t)$.

## 12. Success / Failure / Insufficient Evidence

Success: next-two beats fixed-next-one on `T_0.9_eval` and `AUC_Q`, while guards pass.

Failure: fixed-next-one matches or beats next-two, or next-two wins only through local degradation or noisy false positives.

Insufficient: no threshold, unstable evaluation decoder, or unresolved leakage.

## 13. What This Cannot Claim

No universal MTP claim, no natural-language transfer, no K>2 conclusion, and no claim that NTP cannot encode branch information.

## 14. Review Notes And Protocol Changes

The executed first pass includes the six audited choices from the user discussion: decision-only scope, both `identical_branch` and `random` init, matched fixed-next-one with extra heads, `filler_length=16`, A11_03 and A11_04 run as separate but parallel anchors, and no separate-expert rescue in the main matrix.
