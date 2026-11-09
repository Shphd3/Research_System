# Protocol: A11_04_03 K=3 Efficiency Advantage

## 0. Approval Snapshot

Approval status: approved by the user on 2026-07-08. Use 5 seeds. Keep default threshold, early window, and controls. Run gradient usefulness diagnostics for K=1, K=2, and K=3 when applicable. Keep noisy control under all-position training. Proceed to implementation and full reserved 4-GPU run.

Purpose: Test whether the direct representation-supervision advantage established in A11_04 becomes a learning-efficiency advantage.

Primary anchor: `Projects/from-attention-to-search/main/problem_anchors/11_informative_future_branch_mechanism/11_04_k3_first_informative_horizon_anchor.md`

Anchor decision question: Given clean $\tau=3$ data where $Y_1=A$, $Y_2=C$, and $Y_3=S_Z$, does the covering condition K=3 learn the early variable $Z$ earlier or more robustly than K=1/K=2?

Anchor physical prior tested: If K covers the first informative future token, the extra active horizon gives direct supervision to $h_T$; this may reduce the time needed to recover $Z$.

Anchor core model term tested:

$$
\lambda_3\operatorname{CE}(q_3(\cdot\mid h_T),S_Z).
$$

Anchor falsifier: If K=3 does not improve time-to-threshold or early AUC over K=1/K=2, and gradient usefulness does not explain later $Q$ improvement, then the current evidence does not support an efficiency advantage.

Experiment role: efficiency adjudication plus gradient mechanism audit.

Primary metric from anchor: time-to-threshold $T_\theta$ with $\theta=0.9$ and $r=2$ consecutive evaluations.

Secondary primary metric: early AUC of $Q_K(t)$ over steps 0-3000.

Claim boundary from anchor: This experiment can support only a controlled learning-efficiency claim. It cannot prove natural-language transfer, universal next-K scaling, or unconditional MTP superiority.

Minimal setup: Same clean $\tau=3$ data/model matrix as A11_04, evaluated at the same decision prefix $h_T$.

Basic configuration: one-layer one-head Transformer, `d_model=64`, `num_branches=4`, `filler_length=16`, `shared_context_length=4`, K=1/K=2/K=3, seeds `971-975`, `identical_branch` and `random` initialization, `15000` steps, default early window 0-3000 steps.

Conditions to run: decision-only and all-position scopes; clean $\tau=3$, noisy horizon-3, and redundant horizon-3 regimes; K=1/K=2/K=3; gradient usefulness diagnostics for all K where the diagnostic is well-defined.

Pass: K=3 has smaller $T_\theta$ and higher early AUC than K=1/K=2 in clean $\tau=3$; local-loss guards pass; noisy controls do not reproduce the same efficiency pattern; gradient usefulness shows that the extra horizon signal predicts or explains later $Q$ improvement.

Fail: K=1/K=2 are equally fast and stable, K=3 early AUC is not higher, local loss degrades, noisy controls reproduce the same effect, or gradient usefulness does not support an extra-horizon explanation.

Insufficient: K=3 trends better but seed variance is high, $T_\theta$ is heavily censored, gradient profiles are too noisy, or early AUC and final $Q$ disagree without a clear explanation.

Cannot claim: MTP is better on natural language, larger K always helps, negative gradient cosine is bad, positive gradient cosine is good, final $Q$ alone proves efficiency, or all-position non-covering horizons cannot recover $Z$.

Approval decision: approved; implement and run.

## 1. Terminology / Definitions

| Term | Plain meaning | Concrete object / computation | Unit or formula | Why it matters | Cannot prove |
| --- | --- | --- | --- | --- | --- |
| representation-supervision advantage | the objective forces $h_T$ to retain $Z$ | low $L_\tau$ implies high $I(h_T;Z)$ | information constraint | established by theory | faster learning |
| learning-efficiency advantage | faster or more robust recovery of $Z$ | lower $T_\theta$ and higher early AUC | steps / score area | main decision | natural-language benefit |
| guarded score $Q$ | conservative recovery of $Z$ from $h_T$ | $Q=\min\{A,P,S\}$ | 0 to 1 | avoids probe-only evidence | full causality |
| time-to-threshold $T_\theta$ | first reliable threshold crossing | $T_\theta=\inf\{t:Q(t)\ge\theta\text{ for }r\text{ evaluations}\}$ | steps | tests "earlier" | final performance |
| early AUC | area under early $Q(t)$ curve | $\operatorname{AUC}_{Q,[0,3000]}$ | score area | tests early learning trajectory | final convergence |
| local-loss guard | local prediction is not sacrificed | $Y_1/Y_2$ loss and accuracy | CE / accuracy | rules out tradeoff-only gains | long-horizon mechanism |
| extra-horizon gradient | gradient from the first informative future target | $g_\tau=\nabla_\theta L_\tau$ | gradient vector | candidate mechanism for MTP efficiency | usefulness by itself |
| gradient usefulness | predictive relation between gradient diagnostics and future $Q$ gains | correlation or grouped comparison with $\Delta Q_\Delta$ | correlation / score delta | tests whether the extra signal explains later recovery | strict causality |

## 2. Anchor Alignment

The upstream A11_04 result supports direct single-prefix supervision: in decision-only clean $\tau=3$, K=3 recovers $Z$ while K=1/K=2 remain low. The all-position control shows that K=1/K=2 can also recover $Z$ indirectly, so the next question is efficiency rather than existence.

Clean data:

$$
Y_1=A,\qquad Y_2=C,\qquad Y_3=S_Z.
$$

Information structure:

$$
I(Z;Y_1)=0,\qquad I(Z;Y_2\mid Y_1)=0,\qquad I(Z;Y_3\mid Y_1,Y_2)>0.
$$

K=3 adds the direct informative-horizon term:

$$
\lambda_3\operatorname{CE}(q_3(\cdot\mid h_T),S_Z).
$$

The experiment tests whether this direct term yields earlier or more stable recovery.

## 3. Tested Hypotheses

H1: In decision-only clean $\tau=3$, K=3 reaches $Q\ge0.9$ earlier and has higher early AUC than K=1/K=2.

H2: K=3 efficiency does not come from local degradation; $Y_1/Y_2$ accuracy remains near 1.0 and loss does not significantly exceed K=1/K=2.

H3: In all-position clean $\tau=3$, K=3 may not be the only condition that recovers $Z$, but it should be earlier, more stable, or less false-positive-prone than K=1/K=2 if MTP has an efficiency advantage.

H4: Extra-horizon gradient diagnostics should help explain later $Q$ improvement. If they do not, the experiment cannot claim that MTP gradients are more useful.

## 4. Rival Explanations

| Rival explanation | Guard |
| --- | --- |
| Extra heads or extra loss improve representation generically | noisy control with $Y_3\perp Z$ |
| Horizon index itself matters | redundant control with $Y_2=S_Z$ |
| K=3 sacrifices local prediction | local-loss guard on $Y_1/Y_2$ |
| All-position lets NTP learn indirectly | compare $T_\theta$, early AUC, and noisy false positives rather than final $Q$ |
| Negative cosine means bad gradient | interpret cosine only with future $\Delta Q$ |
| Early AUC is initial noise | require consecutive threshold, multiple seeds, noisy guard, and seed-level stability |

## 5. Data / Model / Algorithm / Objective

Regimes:

- clean $\tau=3$: $Y_1=A$, $Y_2=C$, $Y_3=S_Z$;
- noisy horizon-3: $Y_3\perp Z$;
- redundant horizon-3: $Y_2=S_Z$.

Scopes:

- decision-only: loss only at the decision prefix;
- all-position: LM-style loss at every valid sequence position.

Objective:

$$
L_K=\sum_{j=1}^{K}\lambda_j\operatorname{CE}(q_j(\cdot\mid h),Y_j).
$$

Gradient profiling computes horizon losses separately on matched batches.

## 6. Conditions, Seeds, And Checkpoints

| Item | Anchor clause tested | Model term / rival explanation | Why needed | Primary or secondary evidence | Pass | Fail | Insufficient | Figure/table |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| decision-only clean K=1 | NTP baseline | no informative target | baseline | $T_\theta$, early AUC | lower than K=3 | matches K=3 | noisy curve | efficiency table |
| decision-only clean K=2 | non-covering MTP | active $Y_1,Y_2$ only | separates next-two from coverage | $T_\theta$, early AUC | lower than K=3 | matches K=3 | leakage unclear | efficiency table |
| decision-only clean K=3 | covering condition | active $Y_3=S_Z$ | main direct-supervision test | $T_\theta$, early AUC, local guard | earlier/higher | no advantage | optimization failure | efficiency table |
| all-position clean K=1/2/3 | LM-style boundary | indirect transfer | tests realistic boundary | $T_\theta$, early AUC | K=3 earlier/stabler | K=1/2 equally fast | indirect path unclear | efficiency table |
| noisy K=1/2/3 | false-positive guard | $Y_3\perp Z$ | rules out generic auxiliary gain | noisy early AUC, noisy $T_\theta$ | does not reproduce clean | reproduces clean | high variance | guard table |
| redundant K=1/2/3 | information-structure guard | $Y_2=S_Z$ | checks target information, not horizon label | K=2/K=3 pattern | explained by $Y_2$ | unexplained | ambiguous | guard table |
| gradient K=1/2/3 | mechanism audit | horizon-specific gradients | explains early recovery | $c,r,\rho,\Delta Q$ | predicts $Q$ gain | no relation | noisy | gradient table |

Seeds: `971-975`.

Training steps: `15000`.

Evaluation frequency: default `eval_every=250` if feasible; otherwise `500` with lower early-window resolution.

Profiling frequency: default `profile_every=500`, concentrated on steps 0-5000 and optionally sparse afterward.

## 7. Primary Metric

$$
T_\theta(K)=\inf\{t:Q_K(t)\ge0.9\text{ for }2\text{ consecutive evaluations}\}.
$$

Runs that never reach the threshold are reported as censored/NA. The summary must report reach rate and cannot average only successful runs.

Why it decides: the claim is about earlier reliable semantic recovery, not final capability.

## 8. Secondary Metrics

Early AUC:

$$
\operatorname{AUC}_{Q,[0,3000]}(K)=\frac{1}{3000}\int_0^{3000}Q_K(t)\,dt.
$$

Full AUC:

$$
\operatorname{AUC}_{Q,[0,T_{\max}]}(K).
$$

Stability metrics: seed-level $T_\theta$, seed-level early AUC, reach rate, mean/std, and optionally bootstrap confidence intervals.

Local-loss guard: $Y_1/Y_2$ loss and accuracy at each checkpoint.

## 9. Gradient Usefulness Plan

At profiling step $t$, compute matched-batch gradients:

$$
g_1(t)=\nabla_\theta L_1(t),
$$

$$
g_\tau(t)=\nabla_\theta L_\tau(t),
$$

$$
g_{\mathrm{MTP}}(t)=g_1(t)+\lambda g_\tau(t).
$$

For clean $\tau=3$, $g_\tau=g_3$.

Record:

$$
c(t)=\frac{\langle g_1(t),g_\tau(t)\rangle}{\|g_1(t)\|\|g_\tau(t)\|},
$$

$$
r(t)=\frac{\|g_\tau(t)\|}{\|g_1(t)\|},
$$

$$
\rho(t)=\frac{\langle g_1(t)+\lambda g_\tau(t),g_1(t)\rangle}{\|g_1(t)\|^2}.
$$

Parameter groups:

- embedding;
- shared attention;
- shared MLP;
- head_1;
- head_2;
- head_3.

The main explanation cannot rely on cosine alone. Add forward-looking windows:

$$
\Delta Q_\Delta(t)=Q(t+\Delta)-Q(t),
\qquad
\Delta\in\{500,1000,2000\}.
$$

Usefulness diagnostics:

- correlation between $r(t)$ or $\|g_\tau(t)\|$ and future $\Delta Q_\Delta(t)$;
- high/low grouped comparison of future $\Delta Q$;
- clean vs noisy contrast to check whether usefulness depends on target information.

K=1/K=2 diagnostics should be included when feasible, but inactive horizon-3 gradients must not be interpreted as the same optimization signal as active K=3 $g_\tau$.

## 10. Stage-Level Profiling Plan

| Stage | Local question | Input evidence | Pass / fail / unclear rule | Debug artifact | Handoff |
| --- | --- | --- | --- | --- | --- |
| data audit | Is clean/noisy/redundant information structure correct? | sample table and target map | no leakage / leakage | sample table | detailed |
| smoke | Does training/eval/profile run? | smoke logs | pass / crash | smoke result dir | not central |
| efficiency | Does K=3 recover earlier? | $T_\theta$, early AUC | pass/fail/insufficient | efficiency tables | summary |
| local guard | Does K=3 hurt local prediction? | $Y_1/Y_2$ loss/accuracy | pass/fail | local curves/tables | summary |
| gradient usefulness | Does $g_\tau$ predict later $Q$ gains? | gradient tables and $\Delta Q$ | supports/weakens/insufficient | gradient tables/plots | detailed |

## 11. Output Tables And Figures

Required tables:

- `efficiency_summary.csv`;
- `gradient_profile_summary.csv`;
- `gradient_usefulness_summary.csv`;
- `local_loss_guard_summary.csv`.

Required central figures:

1. clean $\tau=3$ $Q(t)$ curves, separated by decision-only and all-position scope;
2. $T_\theta$ and early AUC with seed dots;
3. local-loss guard curves;
4. gradient usefulness scatter or binned plot;
5. clean vs noisy usefulness contrast.

## 12. Success / Failure / Insufficient Evidence

Support MTP efficiency only if all are true:

1. K=3 has lower $T_\theta$ or higher reach rate than K=1/K=2 in clean $\tau=3$;
2. K=3 has higher early AUC;
3. local-loss guard passes;
4. noisy control does not reproduce the same efficiency pattern;
5. gradient usefulness supports or plausibly explains K=3 early recovery.

Do not support MTP efficiency if any decisive failure occurs:

1. K=1/K=2 are equally fast and stable;
2. K=3 early AUC is not higher;
3. K=3 local loss degrades;
4. noisy control reproduces the clean pattern;
5. gradient usefulness gives no support for the extra horizon signal.

Insufficient evidence if seed variance is high, $T_\theta$ is heavily censored, gradient profiles are noisy, or early AUC and final $Q$ conflict.

## 13. What This Cannot Claim

This experiment cannot claim:

- MTP improves natural-language tasks;
- all larger K values are better;
- cosine sign alone determines gradient quality;
- all-position K=1/K=2 cannot learn $Z$;
- final $Q$ proves efficiency.

## 14. Review Notes And Protocol Changes

2026-07-08: User approved the Chinese draft with these decisions: use 5 seeds; keep default $\theta=0.9$, $r=2$, and early window 0-3000; run gradient usefulness audits for K=1/K=2/K=3 where feasible; keep noisy control under all-position training; proceed to implementation and full run.
