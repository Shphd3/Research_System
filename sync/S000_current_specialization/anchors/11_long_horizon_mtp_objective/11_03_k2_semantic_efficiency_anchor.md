# 11_03 K=2 Semantic Efficiency Anchor

Status: evidence-updated after A11_03 decision-only run on 2026-07-07.
Parent line: `11_long_horizon_mtp_objective`.
Prior anchors: `11_01_k2_branch_delayed_next_two_anchor.md`, `11_02_two_token_shared_trunk_signal_interference_anchor.md`.
Source draft: `daily_research_reports/0708/mtp_story_package/02_anchor_k2_semantic_efficiency_v0.md`.

## 0. Thinking Card

**Phenomenon:** The K=2 theorem and experiments show that next-two can force $h_T$ to contain an early branch variable $Z$ when $Y_1$ is shared and $Y_2=S_Z$ is branch-specific. This does not yet prove that next-two learns $Z$ faster or more robustly than next-token prediction.

**Mechanism guess:** Because next-token prediction at the decision state only receives the shared target $Y_1=A$, it has no direct branch-specific loss at that state. Next-two additionally receives $Y_2=S_Z$, so it should inject a direct branch-relevant gradient into the same $h_T$ earlier in training.

**Key variables:** early branch variable $Z$; prefix hidden state $h_T$; shared immediate token $Y_1=A$; branch-specific second token $Y_2=S_Z$; guarded semantic score $Q_{\mathrm{eval}}(t)$; local next-token guard $L_1(t)$.

**Causal relation:** If the direct $Y_2=S_Z$ loss is optimization-useful, then next-two should make branch information recoverable from $h_T$ earlier than fixed next-one, while preserving $Y_1$ learning.

**Observable metric:** Primary metric is `T_0.9_eval`, the first training step where a matched evaluation score $Q_{\mathrm{eval}}(t)$ reaches 0.9 for consecutive checkpoints.

**Rival Explanations:** Apparent next-two advantage could come from extra heads/capacity, random branch embedding leakage, probe-only artifacts, local loss degradation, or noisy/redundant future targets rather than true branch-relevant efficiency.

**Decision:** Treat the K=2 efficiency claim as supported in the controlled decision-only clean regime, with an explicit optimization-instability boundary. Next-two improves guarded branch recovery over matched fixed-next-one while preserving $Y_1$, but identical-branch next-two succeeds in only 2 of 5 seeds.

## 1. Problem Definition

**Parent problem:** Determine whether multi-token prediction helps long-horizon relation learning beyond ordinary next-token prediction.

**Sharper subproblem:** After the K=2 objective-level separation is supported, test whether the same mechanism yields a learning-efficiency advantage: faster or more robust acquisition of $Z$ in $h_T$.

**Terminology / Definitions:**

| Term | Plain meaning | Concrete object or computation | Unit / formula | Why it matters | What it cannot prove |
|---|---|---|---|---|---|
| semantic variable $Z$ | The early long-horizon factor in this controlled task | branch key token $\operatorname{BR}_Z$ | categorical variable | Proxy for delayed relevance | Natural-language semantics |
| fixed next-one | Same model family, but only offset 1 contributes training loss | active loss $L_1$ | objective condition | Capacity / head control | All NTP behavior |
| next-two | Same $h_T$ predicts offsets 1 and 2 | active loss $L_1+\lambda L_2$ | objective condition | Main MTP condition | Universal MTP superiority |
| matched evaluation decoder | A frozen-checkpoint evaluation readout used for all conditions | train a small readout from frozen $h_T$ to $S_Z$ on train split and evaluate on held-out split | accuracy / CE | Makes NTP and MTP comparable even when NTP has no trained head-2 | Native MTP head use |
| native head-2 accuracy | The trained offset-2 head's top-1 accuracy | $q_2(\cdot\mid h_T)$ predicts $S_Z$ | 0 to 1 | Guards that next-two really learned its own target | Fair NTP comparison |
| guarded evaluation score $Q_{\mathrm{eval}}(t)$ | Conservative branch-recovery score | $\min\{A_{\mathrm{eval}}(t),P_{\mathrm{eval}}(t),S_{\mathrm{eval}}(t)\}$ | 0 to 1 | Prevents probe-only false positives | Full causal mechanism |
| `T_0.9_eval` | Time to guarded recovery | first step where $Q_{\mathrm{eval}}(t)\ge0.9$ for consecutive evaluations | training steps | Primary efficiency metric | Final asymptotic superiority |
| local guard | Immediate next-token preservation | $Y_1$ accuracy / $L_1$ loss | accuracy / CE | Ensures efficiency does not come from damaging local learning | Long-horizon use by itself |

**Decision question:** In the controlled K=2 branch-delayed task, does next-two make the early variable $Z$ recoverable from $h_T$ earlier than matched fixed-next-one, without damaging immediate next-token learning?

**Not in scope:** Proving MTP always beats NTP; proving natural-language semantic transfer; proving K>2 behavior; broad hyperparameter sweeps; architecture method claims.

## 2. Physical Priors

**P1: Direct-branch-gradient prior.**
Meaning: When $Y_1=A$ is shared, fixed next-one has no branch-specific target at $h_T$, while next-two has the branch-specific target $Y_2=S_Z$.
Could be wrong if: the optimizer cannot use the $Y_2$ signal, or fixed next-one still exposes $Z$ through incidental branch embedding leakage or all-position background losses.

**P2: Efficiency-from-direct-signal prior.**
Meaning: A direct branch-specific target at the same prefix state should reduce the time needed for $h_T$ to expose $Z$.
Could be wrong if: shared-trunk interference cancels the useful signal, or the task is so easy that both objectives recover $Z$ equally fast.

**P3: Guarded-metric prior.**
Meaning: Branch information should count as useful only when it is predictive, linearly recoverable, and causally branch-sensitive.
Could be wrong if: one of the guards is too strict or the matched evaluation decoder overfits leakage.

## 3. Falsifiable Hypotheses

**H1: K=2 efficiency hypothesis.**
Supported if: next-two has lower `T_0.9_eval` than matched fixed-next-one and higher early `AUC_Q`.
Weakened if: fixed next-one reaches the same guarded score at the same time or earlier.

**H2: Local-preservation hypothesis.**
Supported if: next-two's $Y_1$ accuracy/loss is matched to fixed next-one within a predeclared tolerance.
Weakened if: the branch-recovery gain appears only by degrading $Y_1$ learning.

**H3: Metric-validity hypothesis.**
Supported if: clean branch-specific targets improve $Q_{\mathrm{eval}}$, redundant targets are explained by $Y_1$, and noisy targets do not pass native future prediction guards.
Weakened if: branch probe is high while prediction and branch-swap are weak, or noisy controls behave like clean branch targets.

## 4. Mathematical Model

**Objects:**

$$
Z\sim\operatorname{Unif}\{1,\ldots,m\},
\qquad
X=(\operatorname{BR}_Z,F_1,\ldots,F_L,U,A,S_Z).
$$

Decision state:

$$
h_T=f_\theta(\operatorname{BR}_Z,F_{1:L},U).
$$

Targets:

$$
Y_1=A,\qquad Y_2=S_Z.
$$

Information relation:

$$
I(Z;Y_1)=0,\qquad I(Z;Y_2\mid Y_1)=H(Z).
$$

**Core decomposition:**

$$
L_{\mathrm{fixed1}}=L_1=\operatorname{CE}(q_1(\cdot\mid h_T),A).
$$

$$
L_{\mathrm{next2}}=L_1+\lambda L_2
=\operatorname{CE}(q_1(\cdot\mid h_T),A)
+\lambda\operatorname{CE}(q_2(\cdot\mid h_T),S_Z).
$$

**Mechanism relation:**

$$
\nabla_{h_T}L_{\mathrm{next2}}
=\nabla_{h_T}L_1+\lambda\nabla_{h_T}L_2,
$$

where $\nabla_{h_T}L_2$ depends on $S_Z$ and therefore on $Z$.

**Observable metrics:**

$$
Q_{\mathrm{eval}}(t)=\min\{A_{\mathrm{eval}}(t),P_{\mathrm{eval}}(t),S_{\mathrm{eval}}(t)\}.
$$

Here $A_{\mathrm{eval}}$ is held-out suffix decodability from frozen $h_T$, $P_{\mathrm{eval}}$ is held-out branch-probe accuracy, and $S_{\mathrm{eval}}$ is branch-swap consistency under the same evaluation readout.

Primary efficiency metric:

$$
T_{0.9}^{\mathrm{eval}}=\inf\{t:Q_{\mathrm{eval}}(t)\ge0.9\text{ for consecutive evaluations}\}.
$$

**Falsifier:** If next-two does not improve `T_0.9_eval` or early `AUC_Q` over fixed next-one under matched conditions, then the K=2 efficiency claim is not supported, even though the objective-level theorem remains valid.

## 5. Computational Realization

**Input objects:** Balanced branch-delayed sequences with $Y_1=A$ and $Y_2=S_Z$; redundant and noisy controls remain guards, not the main claim.

**Computed variables:** checkpointed $h_T$; matched evaluation suffix decoder; frozen branch probe; branch-swap score; native head-2 score for next-two only; $Y_1$ loss/accuracy.

**Algorithm stages:**

1. Train matched fixed-next-one and next-two models.
2. At checkpoints, freeze the model and evaluate $Q_{\mathrm{eval}}(t)$ using the same evaluation pipeline.
3. Check native next-two head-2 accuracy and local $Y_1$ preservation.

**Stage-local evidence:** learning curves for $Q_{\mathrm{eval}}(t)$, $Y_1$ loss/accuracy, native head-2 accuracy, and optional branch-useful gradient projection.

**Expected artifacts:** `protocol.md`, `summary.md`, `detailed.md`, compact tables for `T_0.9_eval`, `AUC_Q`, final $Q_{\mathrm{eval}}$, local guards, and control outcomes.

## 6. Minimal Falsification Tests

| Test | Question | Intervention / comparison | Primary metric | Pass / fail / insufficient | Why it decides | Failure means |
|---|---|---|---|---|---|---|
| Efficiency test | Does next-two recover $Z$ earlier in $h_T$? | next-two vs matched fixed-next-one on clean K=2 | `T_0.9_eval` | Pass: next-two lower; fail: fixed-next-one matched or lower; insufficient: neither reaches threshold | Directly tests learning efficiency | Efficiency claim weakened, theorem unchanged |
| Local guard | Is the gain paid for by worse immediate prediction? | Compare $Y_1$ loss/accuracy curves | $L_1$ delta | Pass: within tolerance; fail: next-two degrades $Y_1$ | Protects against tradeoff masquerading as efficiency | Need revise claim to useful-but-costly |
| Control guard | Is the score specific to branch-informative targets? | clean vs redundant/noisy controls | control outcome pattern | Pass: clean improves, noisy fails, redundant explained by $Y_1$; fail: noisy also passes | Separates branch signal from auxiliary noise/leakage | Metric or data construction invalid |

## 7. Current Evidence

**Observation:** A11_01 supports the clean K=2 objective-level separation: fixed-next-one solved $Y_1$ but stayed branch-blind, while next-two solved $Y_2$ and made $h_T$ branch-readable and branch-swap-sensitive.

**Observation:** A11_02 supports that $L_2$ is a useful branch signal in `A_clean` and that noisy targets do not produce native head-2 learning. It also shows that branch probe alone is not sufficient evidence.

**Observation:** A11_03 completed the matched efficiency test. In the clean regime, fixed next-one preserved $Y_1$ but stayed at chance-level guarded recovery: AUC $Q=0.250$ under `identical_branch` and `0.288` under `random`, with threshold reach rate `0.00`. Next-two improved branch recovery: AUC $Q=0.536`, final $Q=0.550`, reach rate `0.40` under `identical_branch`, and AUC $Q=0.895`, final $Q=0.900`, reach rate `0.80` under `random`. Clean $Y_1$ accuracy stayed `1.00`.

**Interpretation:** The representation-requirement mechanism becomes a controlled learning-efficiency advantage: next-two gives a useful direct branch signal that matched fixed-next-one lacks at $h_T$.

**Boundary:** The advantage is not guaranteed optimization success. Under `identical_branch`, only 2 of 5 next-two seeds reached the guarded threshold. The noisy random-init control also showed a weak false-positive bump, so random-init branch recovery must be interpreted with the clean/native-head and noisy-control guards.

**Evidence links:**

- `Projects/from-attention-to-search/main/experiments/A11/A11_01_k2_branch_delayed_next_two/summary.md`
- `Projects/from-attention-to-search/main/experiments/A11/A11_02_two_token_shared_trunk_signal_interference/summary.md`
- `Projects/from-attention-to-search/main/experiments/A11/A11_03_k2_semantic_efficiency/summary.md`
- `Projects/from-attention-to-search/main/experiments/A11/A11_03_k2_semantic_efficiency/detailed.md`
- `daily_research_reports/0708/mtp_story_package/02_anchor_k2_semantic_efficiency_v0.md`

## 8. Claim Boundary And Next Decision

**Can claim:** In the controlled K=2 decision-only task, next-two can improve guarded recovery of the early branch variable $Z$ from $h_T$ over matched fixed-next-one, while preserving immediate next-token accuracy. The measured advantage is learning efficiency / recoverability of the delayed variable, not general language modeling quality.

**Cannot claim:** MTP is generally more efficient; NTP cannot learn $Z$; native head-2 accuracy alone proves branch representation; K=3 follows automatically; optimization always succeeds; random-init recovery is leakage-free causal evidence.

**Next decision:** Use A11_04 to test whether this K=2 result is a special case of first-informative-horizon coverage: MTP should help only when $K$ reaches the first future target that contains new information about $Z$.
