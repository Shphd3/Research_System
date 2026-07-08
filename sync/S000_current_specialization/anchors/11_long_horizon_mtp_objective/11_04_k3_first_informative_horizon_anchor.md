# 11_04 K=3 First-Informative-Horizon Anchor

Status: evidence-updated after A11_04 decision-only, A11_04_02 all-position control, and A11_04_03 efficiency runs.
Parent line: `11_long_horizon_mtp_objective`.
Prior anchors: `11_01_k2_branch_delayed_next_two_anchor.md`, `11_02_two_token_shared_trunk_signal_interference_anchor.md`, `11_03_k2_semantic_efficiency_anchor.md`.
Source draft: `daily_research_reports/0708/mtp_story_package/04_anchor_k3_first_informative_horizon_v0.md`.

## 0. Thinking Card

**Phenomenon:** The K=2 result may be a special case of next-two. To claim a next-$K$ principle, we need a task where the first branch-informative future token appears at horizon 3, not horizon 2.

**Mechanism guess:** MTP helps only when its active horizon covers the first future token that reveals the early variable. If $Y_1$ and $Y_2$ are shared but $Y_3=S_Z$ is branch-specific, then K=3 should create direct branch supervision on $h_T$, while K=1 and K=2 should not.

**Key variables:** early branch variable $Z$; first informative horizon $\tau=3$; active horizon $K$; prefix state $h_T$; targets $Y_1=A$, $Y_2=C$, $Y_3=S_Z$; guarded coverage score $Q_K(t)$.

**Causal relation:** If horizon coverage is the mechanism, then branch recovery should improve when $K$ reaches $\tau$, not merely when model capacity or objective size increases.

**Observable metric:** Primary metric is `coverage_gap`, the guarded semantic recovery gap between K=3 and the best non-covering condition K=1/K=2.

**Rival Explanations:** K=3 could win because of extra parameters, loss scale, leakage into $Y_1/Y_2$, random branch embedding identity, or optimization schedule rather than first-informative-horizon coverage.

**Decision:** Treat the first-informative-horizon mechanism as supported for direct single-prefix supervision in the controlled decision-only $\tau=3$ task. Do not state the stronger all-position claim that only K=3 can recover $Z$: A11_04_02 shows that all-position background losses can make K=1/K=2 branch-readable through indirect shared-parameter transfer.

## 1. Problem Definition

**Parent problem:** Generalize the K=2 objective-level mechanism into a falsifiable next-$K$ statement.

**Sharper subproblem:** Test whether MTP advantage is controlled by whether $K$ covers the first informative horizon $\tau$, rather than by the special fact that K=2 predicts one extra token.

**Terminology / Definitions:**

| Term | Plain meaning | Concrete object or computation | Unit / formula | Why it matters | What it cannot prove |
|---|---|---|---|---|---|
| first informative horizon $\tau$ | First future offset that adds information about $Z$ | $\tau=\min\{j:I(Z;Y_j\mid Y_{<j})>0\}$ | token offset | Core mechanism variable | Natural-language horizon structure |
| covering condition | Active horizon includes $\tau$ | $K\ge\tau$ | Boolean | Should receive direct semantic supervision | Optimization success |
| non-covering condition | Active horizon stops before $\tau$ | $K<\tau$ | Boolean | Should not receive direct semantic supervision | Absence of incidental leakage |
| K=1 / NTP | Predict only $Y_1$ | active horizon 1 | objective condition | Baseline | All NTP behavior |
| K=2 | Predict $Y_1,Y_2$ | active horizons 1,2 | non-covering control when $\tau=3$ | Separates next-two from coverage | That K=2 is useless generally |
| K=3 | Predict $Y_1,Y_2,Y_3$ | active horizons 1,2,3 | covering condition | Main test of horizon coverage | Broad next-K scaling |
| guarded score $Q_K(t)$ | Conservative branch-recovery score | $\min\{A_K(t),P_K(t),S_K(t)\}$ using a matched evaluation pipeline | 0 to 1 | Prevents probe-only false positives | Full causal mechanism |
| coverage gap | K=3 advantage over non-covering horizons | $\Delta_{\mathrm{cov}}=\operatorname{AUC}_Q(3)-\max(\operatorname{AUC}_Q(1),\operatorname{AUC}_Q(2))$ | score gap | Primary coverage metric | Step-wise threshold superiority by itself |

**Decision question:** In a $\tau=3$ branch-delayed task, does K=3 produce guarded branch recovery from $h_T$ beyond K=1 and K=2, while local $Y_1,Y_2$ prediction remains matched?

**Not in scope:** A broad K sweep; curriculum; natural-language transfer; proving larger $K$ is always better; architecture superiority.

## 2. Physical Priors

**P1: Non-coverage prior.**
Meaning: If $K<\tau$ and $Y_{1:K}$ is branch-independent, the active loss has no direct branch-specific target at $h_T$.
Could be wrong if: data construction leaks $Z$ into $Y_1$, $Y_2$, filler, positions, frequencies, or embeddings.

**P2: Coverage prior.**
Meaning: If $K\ge\tau$ and $Y_\tau=S_Z$ is branch-specific, low offset-$\tau$ loss requires $h_T$ to contain $Z$.
Could be wrong if: the model/optimizer cannot use the offset-$\tau$ supervision, or the evaluation metric fails to observe the information.

**P3: Specificity prior.**
Meaning: K=3 should help in the clean $\tau=3$ regime, but not when $Y_3$ is noisy or already redundant with earlier branch-revealing targets.
Could be wrong if: auxiliary losses improve representation through unrelated regularization rather than horizon coverage.

## 3. Falsifiable Hypotheses

**H1: Coverage-threshold hypothesis.**
Supported if: K=3 has positive `coverage_gap` and reaches guarded branch recovery while K=1/K=2 remain low or delayed.
Weakened if: K=2 behaves like K=3 in the clean $\tau=3$ regime.

**H2: Local-guard hypothesis.**
Supported if: K=3 preserves $Y_1$ and $Y_2$ learning relative to K=1/K=2.
Weakened if: K=3 wins only by degrading local prediction.

**H3: Leakage/control hypothesis.**
Supported if: noisy horizon-3 controls do not pass guarded recovery, and redundant controls behave as explained by earlier branch-revealing targets.
Weakened if: non-covering conditions pass the guarded score without a branch-informative active target.

## 4. Mathematical Model

**Objects:**

$$
Z\sim\operatorname{Unif}\{1,\ldots,m\},
\qquad
X=(\operatorname{BR}_Z,F_1,\ldots,F_L,U,A,C,S_Z).
$$

Decision state:

$$
h_T=f_\theta(\operatorname{BR}_Z,F_{1:L},U).
$$

Targets:

$$
Y_1=A,\qquad Y_2=C,\qquad Y_3=S_Z.
$$

Information relation:

$$
I(Z;Y_1)=0,
$$

$$
I(Z;Y_2\mid Y_1)=0,
$$

$$
I(Z;Y_3\mid Y_1,Y_2)=H(Z).
$$

Thus:

$$
\tau=3.
$$

**Core decomposition:**

For active horizon $K$:

$$
L_K(h_T)=\sum_{j=1}^{K}\lambda_j\operatorname{CE}(q_j(\cdot\mid h_T),Y_j).
$$

For $K<3$, a $Z$-blind $h_T$ can solve all active deterministic shared targets. For $K=3$, low offset-3 loss implies:

$$
\mathbb E[-\log q_3(S_Z\mid h_T)]\le\varepsilon
\quad\Rightarrow\quad
I(h_T;Z)\ge H(Z)-\varepsilon.
$$

**Mechanism relation:**

K=3 adds the first branch-dependent gradient term:

$$
\lambda_3\nabla_{h_T}\operatorname{CE}(q_3(\cdot\mid h_T),S_Z).
$$

K=1 and K=2 do not include such a term in the clean $\tau=3$ construction.

**Observable metrics:**

$$
Q_K(t)=\min\{A_K(t),P_K(t),S_K(t)\}.
$$

Here $A_K$ is held-out $S_Z$ decodability from frozen $h_T$, $P_K$ is held-out branch-probe accuracy, and $S_K$ is branch-swap consistency under the same matched evaluation pipeline.

Primary metric:

$$
\Delta_{\mathrm{cov}}=
\operatorname{AUC}_Q(3)-\max\{\operatorname{AUC}_Q(1),\operatorname{AUC}_Q(2)\}.
$$

**Falsifier:** If K=2 matches K=3 on $Q_K(t)$ in the clean $\tau=3$ regime without identified leakage, then first-informative-horizon coverage is not the operative explanation.

## 5. Computational Realization

**Input objects:** Clean $\tau=3$ sequences with shared $Y_1=A$, shared $Y_2=C$, and branch-specific $Y_3=S_Z$; tau=2 positive control; noisy and redundant controls.

**Computed variables:** checkpointed $h_T$ for K=1/K=2/K=3; matched horizon-3 evaluation decoder; branch probe; branch-swap score; native head-3 accuracy for K=3; local $Y_1,Y_2$ losses.

**Algorithm stages:**

1. Train K=1, K=2, and K=3 conditions with the same base architecture and matched active-loss scaling.
2. Evaluate $Q_K(t)$ at checkpoints using the same frozen-state evaluation pipeline.
3. Audit leakage and local-loss guards before interpreting a coverage gap.

**Stage-local evidence:** $Q_1(t)$, $Q_2(t)$, $Q_3(t)$ on the same axis; horizon-3 decodability; branch-swap; branch probe; local $Y_1,Y_2$ losses; optional gradient projection $U_3$.

**Expected artifacts:** `protocol.md`, `summary.md`, `detailed.md`, compact coverage-gap table, control-result table, and leakage audit.

## 6. Minimal Falsification Tests

| Test | Question | Intervention / comparison | Primary metric | Pass / fail / insufficient | Why it decides | Failure means |
|---|---|---|---|---|---|---|
| Coverage test | Does the first branch-informative horizon drive the advantage? | K=1 vs K=2 vs K=3 on clean $\tau=3$ | `coverage_gap` | Pass: K=3 exceeds K=1/K=2; fail: K=2 matches K=3; insufficient: all fail | Directly tests horizon coverage | First-informative-horizon story weakened or optimizer failed |
| Local guard | Does K=3 hurt shared local targets? | Compare $Y_1,Y_2$ losses across K | local loss delta | Pass: within tolerance; fail: local degradation | Prevents tradeoff interpretation | Claim must become useful-but-costly |
| Leakage/control guard | Are non-covering gains caused by leakage or noise? | noisy/redundant controls and data audit | control pattern | Pass: noisy fails, redundant explained, no leakage; fail: false positives | Protects causal interpretation | Data or metric invalid |

## 7. Current Evidence

**Observation:** A11_01 validates the $\tau=2$ special case: K=2 can force $h_T$ to expose branch information when $Y_2=S_Z$ and $Y_1$ is shared.

**Observation:** A11_02 validates the target-information distinction at K=2: branch-informative targets behave differently from noisy controls, and branch probe alone is not sufficient.

**Observation:** A11_04 completed the clean $\tau=3$ coverage test. In clean $\tau=3$, K=1 and K=2 stayed at chance-level guarded recovery under both initializations: final $Q=0.25$ and threshold reach rate `0.00`. K=3 improved recovery: under `identical_branch`, AUC $Q=0.665$, final $Q=0.800$, reach rate `0.60`; under `random`, AUC $Q=0.735$, final $Q=0.750$, reach rate `0.40`.

**Observation:** The clean coverage gap was positive: $\Delta_{\mathrm{cov}}=+0.415$ for `identical_branch` and $+0.465$ for `random`. K=3 preserved clean $Y_1,Y_2$ accuracy at `1.00`.

**Observation:** Noisy K=3 did not match clean K=3 in final recovery, but it produced weak transient false positives: noisy K=3 reach rate was `0.20` in both initializations, while final $Q$ stayed low (`0.25` identical, `0.30` random).

**Observation:** A11_04_02 completed the all-position LM-style control. In clean $\tau=3$, K=3 remained strongest: AUC $Q=0.976/1.000$, final $Q=1.000$, and reach rate `1.00`. However, non-covering K=1/K=2 were also high: K=1 AUC $Q=0.823/0.942$, K=2 AUC $Q=0.715/0.942$. Random-init K=2 reached final $Q=1.000$, matching K=3. Noisy all-position controls were also high, especially under random init: noisy K=1/K=2/K=3 AUC $Q=0.798/0.932/0.913$.

**Observation:** A11_04_03 completed the efficiency run with 5 seeds and gradient audits for K=1/K=2/K=3. In clean decision-only $\tau=3$, K=1/K=2 never reached $Q\ge0.9$, while K=3 reached in `0.60/0.40` of seeds under identical/random initialization. K=3 early AUC was `0.537/0.644`, versus best non-covering early AUC `0.250/0.281`. K=3 preserved active $Y_1/Y_2$ accuracy at `1.00`.

**Observation:** In clean all-position A11_04_03, K=3 remained strongest: reach rate `1.00/1.00`, early AUC `0.965/1.000`, and final $Q=1.000/1.000`. However, K=1/K=2 also recovered through indirect paths: best non-covering early AUC was `0.838/0.956`, and final $Q$ reached `0.850/0.950`.

**Observation:** A11_04_03 noisy controls protect the decision-only mechanism but weaken a strict all-position specificity claim. Decision-only noisy K=3 stayed low in final $Q$ (`0.250/0.300`), but all-position noisy controls produced high early AUC under random initialization (`0.958/0.946/0.985` for K=1/K=2/K=3).

**Observation:** A11_04_03 gradient usefulness is insufficient as a causal explanation. Some clean K=3 all-position shared-MLP diagnostics correlate with later $Q$ improvement, but the pattern is mixed across initialization, parameter group, and objective scope. Cosine sign or norm ratio alone is not a valid usefulness metric.

**Interpretation:** The K=2 mechanism generalizes as a direct single-prefix coverage statement and now has qualified efficiency evidence: MTP helps when $K$ includes the first future target that contains new information about $Z$ at $h_T$, and in the clean decision-only setting this direct supervision is learned earlier than non-covering K. K=2 fails in decision-only clean $\tau=3$ not because next-two is intrinsically weak, but because it does not cover $\tau$. Under all-position training, this clean separation no longer holds because losses at other positions can update shared parameters and make $h_T$ branch-readable indirectly.

**Boundary:** The supported claim is direct-supervision efficiency at a fixed prefix state, not all-position exclusivity. In all-position LM-style training, high $Q(h_T)$ is not sufficient evidence that the active decision-prefix horizon covered $\tau$; it may reflect indirect transfer from other positions. The gradient audit does not yet prove that extra-horizon gradients are universally more useful. This still does not prove natural-language transfer, curriculum, or broad next-$K$ scaling.

**Evidence links:**

- `Projects/from-attention-to-search/main/experiments/A11/A11_01_k2_branch_delayed_next_two/summary.md`
- `Projects/from-attention-to-search/main/experiments/A11/A11_02_two_token_shared_trunk_signal_interference/summary.md`
- `Projects/from-attention-to-search/main/experiments/A11/A11_03_k2_semantic_efficiency/summary.md`
- `Projects/from-attention-to-search/main/experiments/A11/A11_04_k3_first_informative_horizon/summary.md`
- `Projects/from-attention-to-search/main/experiments/A11/A11_04_k3_first_informative_horizon/detailed.md`
- `Projects/from-attention-to-search/main/experiments/A11/A11_04_02_k3_all_position_control/summary.md`
- `Projects/from-attention-to-search/main/experiments/A11/A11_04_02_k3_all_position_control/detailed.md`
- `Projects/from-attention-to-search/main/experiments/A11/A11_04_03_k3_efficiency_advantage/summary.md`
- `Projects/from-attention-to-search/main/experiments/A11/A11_04_03_k3_efficiency_advantage/detailed.md`
- `daily_research_reports/0708/mtp_story_package/04_anchor_k3_first_informative_horizon_v0.md`

## 8. Claim Boundary And Next Decision

**Can claim:** In a controlled decision-only task, MTP improves both recoverability and early learning efficiency of an early branch variable when its active horizon $K$ reaches the first informative future token $\tau$. In all-position LM-style training, K=3 remains the strongest direct-supervision condition, but K=1/K=2 can also recover $Z$ through indirect shared-parameter transfer.

**Cannot claim:** Larger $K$ always helps; K=3 improves natural language; curriculum is useful; broad next-$K$ efficiency follows automatically; non-covering horizons can never encode $Z$ under all-position training; noisy controls are perfectly clean under threshold metrics; extra-horizon gradient cosine or norm ratio alone proves useful optimization direction.

**Next decision:** Turn the direct-supervision result into an optimization statement: identify the assumptions under which covering $\tau$ reduces learning time or sample complexity, rather than merely imposing a representation constraint. Do not launch a broader next-K sweep until this efficiency mechanism is stated and falsified locally.
