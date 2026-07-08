# 11_05 Semantic Efficiency Bridge Anchor

Status: completed Protocol A; result supports direct supervision as a mechanism component, with all-position indirect transfer still alive.
Parent line: `11_long_horizon_mtp_objective`.
Prior anchor: `11_04_k3_first_informative_horizon_anchor.md`.
Source draft: `daily_research_reports/0708/mtp_semantic_efficiency_package_v1/03_next_decision_anchor_semantic_efficiency_bridge_cn.md`.

## 0. Thinking Card

**Phenomenon:** A11 now supports the direct representation claim: when MTP covers the first informative future horizon, low loss at that horizon forces the current prefix state $h_T$ to contain the early variable $Z$. The open question is no longer only whether $h_T$ can contain $Z$, but whether the direct supervision makes learning $Z$ faster, more stable, and more usable.

**Mechanism guess:** In clean $\tau=3$ data, the K=3 objective includes the direct term $\lambda_3\operatorname{CE}(q_3(\cdot\mid h_T),S_Z)$. This term gives $h_T$ a shorter credit-assignment path to $Z$ than non-covering K=1/K=2. In all-position training, K=1/K=2 can still recover $Z$ indirectly through losses at other positions, so the next test must separate direct supervision from indirect transfer.

**Key variables:** early semantic variable $Z$; current prefix state $h_T$; first informative horizon $\tau=3$; active horizon K; direct decision-prefix horizon-3 loss; all-position indirect horizon-3 losses; semantic recovery score $Q(t)$; time-to-threshold $T_\theta$; early AUC; local $Y_1/Y_2$ loss; gradient usefulness $U_3$.

**Causal relation:** If direct horizon-3 supervision is the efficiency mechanism, then adding $\operatorname{CE}(q_3(\cdot\mid h_T),S_Z)$ at the decision prefix should reduce $T_\theta$ or increase early AUC, while masking that direct term should weaken K=3 even when all-position indirect losses remain.

**Observable metric:** Primary metric is $T_\theta$, the first step where $Q(t)\ge0.9$ for consecutive evaluations. In the completed run, $T_{0.9}$ required 3 consecutive evaluations. Secondary metric is early AUC of $Q(t)$.

**Rival explanations:** K=3 may look better because of all-position indirect transfer, generic auxiliary loss regularization, larger loss scale, probe false positives, initialization leakage, or a tradeoff where local next-token learning is sacrificed.

**Decision:** Protocol A supports direct decision-prefix horizon-3 supervision as a measurable efficiency component. The next decision is whether to tighten the optimization bridge in a no-leakage setup or move to a harder all-position construction where indirect transfer does not saturate the metric.

## 1. Problem Definition

**Parent problem:** Determine whether MTP learns long-horizon semantic information more efficiently than NTP, rather than merely imposing a stronger representation constraint after optimization succeeds.

**Sharper subproblem:** In the minimal clean $\tau=3$ construction, decide whether the K=3 efficiency advantage comes from direct horizon-3 supervision on the current state $h_T$, rather than all-position indirect transfer or local-loss tradeoff.

**Terminology / Definitions:**

| Term | Plain meaning | Concrete object or computation | Unit / formula | Why it matters | What it cannot prove |
|---|---|---|---|---|---|
| early variable $Z$ | Information present in the prefix but needed later | branch identity | discrete label | target semantic variable | natural-language semantics |
| current state $h_T$ | Representation at the decision prefix | hidden state after shared local context | vector | object supervised by MTP | later-state knowledge |
| first informative horizon $\tau$ | first future offset that reveals $Z$ | $\tau=\min\{j:I(Z;Y_j\mid Y_{<j})>0\}$ | token offset | defines coverage | fixed real-language horizon |
| direct decision-prefix supervision | horizon-3 loss applied at $h_T$ | $\operatorname{CE}(q_3(\cdot\mid h_T),S_Z)$ | CE | candidate efficiency mechanism | all MTP usefulness |
| indirect transfer | $Z$ recovery through losses at other positions | all-position shared-parameter updates excluding direct $h_T$ horizon-3 loss | training effect | rival explanation | direct supervision |
| guarded recovery $Q$ | conservative $Z$ recovery score | $Q(t)=\min\{A(t),P(t),S(t)\}$ | 0 to 1 | avoids probe-only evidence | exact causal path |
| $T_\theta$ | reliable time-to-threshold | earliest step where $Q(t)\ge0.9$ for consecutive evals | steps | primary efficiency metric | final capability |
| early AUC | early recovery area | average $Q(t)$ over an early window | score area | speed and stability | gradient cause |
| local guard | local next-token learning is preserved | $Y_1/Y_2$ accuracy and CE | accuracy / CE | rules out tradeoff | full LM quality |
| gradient usefulness $U_3$ | whether horizon-3 update reduces semantic recovery loss | $U_3=\langle\nabla_\theta R_\phi,g_3\rangle$ | inner product | tests optimization bridge | causality alone |

**Decision question:** In clean $\tau=3$ all-position training, does direct decision-prefix horizon-3 supervision reduce semantic recovery time or improve early recovery beyond indirect transfer, while preserving local $Y_1/Y_2$ learning?

**Not in scope:** broader K sweeps, natural-language transfer, curriculum, final downstream utility, or proving K=3 is always better.

## 2. Physical Priors

**P1: Direct supervision prior.**
Meaning: The shortest route from the loss to $h_T$ is the decision-prefix horizon-3 loss.
Could be wrong if: all-position indirect losses update shared parameters enough that direct $h_T$ supervision adds no measurable speed or stability.

**P2: Indirect transfer prior.**
Meaning: All-position training can make K=1/K=2 branch-readable even without active decision-prefix coverage.
Could be wrong if: non-covering recovery was caused by leakage or metric false positives rather than real shared-parameter transfer.

**P3: Local guard prior.**
Meaning: An efficiency win is clean only if it does not degrade shared local targets $Y_1,Y_2$.
Could be wrong if: the only way to recover $Z$ faster is to trade off local next-token learning.

**P4: Gradient bridge prior.**
Meaning: If $g_3$ is useful, a one-step update along $-g_3$ should reduce semantic recovery loss $R_\phi$ more than control directions.
Could be wrong if: useful learning occurs through multi-step representation dynamics not captured by the one-step diagnostic.

## 3. Falsifiable Hypotheses

**H1: Direct horizon-3 supervision improves semantic efficiency.**
Supported if: adding decision-prefix $L_3$ lowers $T_\theta$ or raises early AUC relative to indirect-only controls.
Weakened if: indirect-only matches full K=3.

**H2: All-position indirect transfer explains part of non-covering recovery.**
Supported if: masking the decision-prefix horizon-3 loss still leaves some $Z$ recovery, but less than full K=3.
Weakened if: masking has no effect or destroys all recovery without explaining K=1/K=2 recovery.

**H3: K=3 efficiency is not a local-learning tradeoff.**
Supported if: $Y_1/Y_2$ loss and accuracy match K=1/K=2 within tolerance.
Weakened if: K=3 gains $Q$ while worsening local targets.

**H4: One-step gradient counterfactuals explain part of the speed advantage.**
Supported if: $-g_3$ or $-(g_1+\lambda_3g_3)$ produces larger immediate improvement in $R_\phi$, $Q$, or branch margin without hurting local loss.
Weakened if: gradient diagnostics remain mixed and unrelated to later recovery.

## 4. Mathematical Model

Clean $\tau=3$ construction:

$$
X=(\operatorname{BR}_Z,F_1,\ldots,F_L,U,A,C,S_Z).
$$

Decision state:

$$
h_T=f_\theta(\operatorname{BR}_Z,F_1,\ldots,F_L,U).
$$

Future targets:

$$
Y_1=A,\qquad Y_2=C,\qquad Y_3=S_Z.
$$

Information structure:

$$
I(Z;Y_1)=0,\qquad I(Z;Y_2\mid Y_1)=0,\qquad I(Z;Y_3\mid Y_1,Y_2)=H(Z).
$$

All-position next-K loss:

$$
L_K^{all}=\sum_t\sum_{j=1}^{K}\lambda_j\operatorname{CE}(q_j(\cdot\mid h_t),X_{t+j}).
$$

The direct term under test is:

$$
L_{3,\mathrm{direct}}=\lambda_3\operatorname{CE}(q_3(\cdot\mid h_T),S_Z).
$$

Semantic recovery loss:

$$
R_\phi(\theta)=\operatorname{CE}(s_\phi(h_T(\theta)),Z).
$$

Gradient usefulness:

$$
U_3=\langle\nabla_\theta R_\phi,g_3\rangle,\qquad g_3=\nabla_\theta L_3.
$$

If $U_3>0$, then a small gradient descent step along $-g_3$ lowers $R_\phi$ to first order. This is a conditional optimization bridge, not an unconditional theorem.

## 5. Computational Realization

**Protocol A:** Tau-3 semantic efficiency mechanism decomposition.

Core conditions:

- K=1 all-position baseline;
- K=2 all-position non-covering baseline;
- K=3 full all-position direct-plus-indirect condition;
- K=3 with decision-prefix horizon-3 loss masked, to measure indirect transfer;
- K=2 all-position plus decision-prefix horizon-3 loss only, to isolate direct supervision.

Optional second stage after approval:

- vary $\lambda_3$ on the direct decision-prefix term to test signal strength.

Held fixed:

- clean $\tau=3$ data;
- architecture;
- optimizer;
- seeds;
- evaluation pipeline;
- local $Y_1/Y_2$ targets.

Primary outputs:

- $Q(t)$ curves;
- $T_\theta$;
- early AUC;
- local $Y_1/Y_2$ loss and accuracy;
- one-step counterfactual $\Delta R_\phi$, $\Delta Q$, and $\Delta L_{\mathrm{local}}$.

## 6. Minimal Falsification Tests

| Test | Question | Intervention / comparison | Primary metric | Pass | Fail | Failure meaning |
|---|---|---|---|---|---|---|
| Direct supervision | Does direct $h_T\to S_Z$ supervision speed recovery? | K2 all-position vs K2 plus decision-prefix $L_3$ | $T_\theta$, early AUC | direct condition improves | no improvement | direct term not sufficient |
| Indirect transfer | How much of K=3 comes from other positions? | K3 full vs K3 with decision-prefix $L_3$ masked | AUC drop, $T_\theta$ delay | masking weakens but does not necessarily erase recovery | masking no effect | direct supervision not the measured cause |
| Full K3 advantage | Does full K3 beat non-covering baselines? | K1/K2 vs K3 full | $T_\theta$, early AUC | K3 faster/higher | K1/K2 match | indirect path is enough |
| Local guard | Is the gain a tradeoff? | local $Y_1/Y_2$ metrics across conditions | CE / accuracy | matched local learning | local degradation | efficiency claim becomes tradeoff |
| One-step gradient | Does $g_3$ help semantic recovery immediately? | update by $g_1$, $g_3$, $g_1+\lambda_3g_3$ | $\Delta R_\phi$, $\Delta Q$, $\Delta L_{\mathrm{local}}$ | $g_3$ improves semantic metrics without local harm | mixed/no relation | gradient bridge unsupported |

## 7. Current Evidence

A11_04 and A11_04_03 support the first-informative-horizon mechanism in clean decision-only $\tau=3$: K=1/K=2 never reliably reach high guarded recovery, while K=3 reaches threshold in a subset of seeds and has much higher early AUC. This supports direct supervision at a fixed prefix.

A11_04_02 and A11_04_03 show the all-position boundary: K=3 remains strongest, but K=1/K=2 can also recover $Z$ through indirect shared-parameter paths. Noisy all-position controls can produce high recovery, so all-position $Q$ alone is not evidence of direct horizon supervision.

A11_04_03 gradient diagnostics are insufficient as a causal explanation. Cosine and norm metrics are mixed across parameter groups and initialization. The next test must use interventions and one-step counterfactuals, not cosine sign alone.

A11_05 completed Protocol A in clean $\tau=3$ all-position training. Under identical-branch initialization, K2 plus decision-prefix L3 reached $Q\ge0.9$ in 5/5 seeds with early AUC 0.969 and final $Q=1.00$, compared with K2's 3/5 seeds, early AUC 0.771, and final $Q=0.85$. Full K3 reached 5/5 seeds with early AUC 0.965 and final $Q=1.00$, while K3 with decision-prefix L3 masked reached 3/5 seeds, early AUC 0.817, and final $Q=0.70$. Active local $Y_1/Y_2$ learning stayed intact. Random initialization saturated $Q$ at step 0, so it is a boundary condition rather than speed evidence. Evidence links: `../../experiments/A11/A11_05_semantic_efficiency_bridge/summary.md` and `../../experiments/A11/A11_05_semantic_efficiency_bridge/detailed.md`.

## 8. Claim Boundary And Next Decision

**Can claim now:** In controlled first-informative-horizon data, covering $\tau$ gives direct representation supervision. In clean decision-only training, this supervision produces earlier recovery than non-covering horizons. In clean $\tau=3$ all-position training, direct decision-prefix horizon-3 supervision is a supported mechanism component: adding it to K2 makes K2 match full K3 under identical-branch initialization, and removing it from K3 weakens K3.

**Cannot claim now:** MTP has an unconditional learning-efficiency proof; all-position K=1/K=2 cannot learn $Z$; direct supervision is the only all-position recovery path; random-init speed metrics are meaningful; gradient cosine proves usefulness; K larger than $\tau$ is better; natural-language or MoE utility follows.

**Next decision:** Do not broaden to K>3 yet. Decide whether to tighten the optimization-efficiency bridge under a no-leakage setup, or move to a harder all-position construction where indirect transfer exists but does not saturate $Q$ at initialization.
