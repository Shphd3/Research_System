# Summary: A11_04_03 K=3 Efficiency Advantage

## Conclusion

This run supports a **qualified efficiency claim**: when the first future token that contains the early semantic variable is at horizon $\tau=3$, K=3 learns that variable earlier and more reliably than K=1/K=2 in the clean decision-only setting. In the all-position LM-style setting, K=3 is still the strongest condition, but K=1/K=2 can also recover the variable through indirect losses, and noisy controls show false-positive recovery. Therefore the clean claim is **direct-supervision efficiency**, not general natural-language superiority.

Strict protocol status: **partial pass**. H1 and H2 are supported. H3 is supported for clean strength but weakened by all-position noisy false positives. H4 is insufficient: gradient diagnostics are useful as an audit, but they do not yet robustly prove that the extra horizon gradient is the cause of later semantic recovery.

One-sentence meeting version: **In our controlled construction, MTP is better than NTP in the precise sense that once its horizon reaches the first semantic future token, it gives direct supervision to the current hidden state and recovers the long-horizon variable earlier; in LM-style all-position training this advantage remains visible but is no longer exclusive because indirect paths also exist.**

## Terminology / Definitions

| Term | Plain meaning | Concrete object / computation | Why it matters | What it cannot prove |
| --- | --- | --- | --- | --- |
| early semantic variable $Z$ | information present in the prefix that matters only later | branch identity embedded before the decision prefix | target of long-horizon recovery | natural-language semantics |
| first informative horizon $\tau$ | first future offset whose token depends on $Z$ | clean task uses $Y_1=A$, $Y_2=C$, $Y_3=S_Z$, so $\tau=3$ | decides whether K covers useful supervision | broad next-K scaling |
| guarded recovery $Q$ | conservative score for whether $h_T$ contains $Z$ | minimum of suffix decoding, branch probe, and swap consistency | primary semantic-recovery metric | exact causal path |
| time-to-threshold $T_\theta$ | first reliable time $Q$ crosses a target | $T_\theta=\inf\{t:Q(t)\ge0.9\text{ for 2 consecutive evaluations}\}$ | tests "learns earlier" | final performance alone |
| early AUC | average early recovery over training | normalized area under $Q(t)$ from step 0 to 3000 | tests learning speed before convergence | cause of the speed |
| local-loss guard | check local next-token learning is not sacrificed | $Y_1/Y_2$ accuracy and loss | rules out a tradeoff explanation | long-horizon mechanism |
| gradient usefulness | whether an extra horizon gradient predicts later recovery | correlations and high/low comparisons against future $\Delta Q$ | audits the mechanism | proof of causality by itself |

## Setup

Clean construction:

$$
Y_1=A,\qquad Y_2=C,\qquad Y_3=S_Z.
$$

Thus:

$$
I(Z;Y_1)=0,\qquad I(Z;Y_2\mid Y_1)=0,\qquad I(Z;Y_3\mid Y_1,Y_2)>0.
$$

Compared conditions: K=1, K=2, K=3; 5 seeds `971-975`; `identical_branch` and `random` initializations; decision-only and all-position LM-style objectives; clean, noisy, and redundant controls. The full run used reserved 4-GPU resources.

Result artifact map:

- Protocol: `protocol.md`
- Main tables: `tables/condition_summary.csv`, `tables/decision_contrasts.csv`, `tables/efficiency_summary.csv`, `tables/local_loss_guard_summary.csv`
- Gradient tables: `tables/gradient_profile_summary.csv`, `tables/gradient_usefulness_summary.csv`
- Figures: `figures/clean_q_curves.png`, `figures/noisy_all_position_q_curves.png`, `figures/local_loss_guard_y1.png`, `figures/gradient_usefulness_clean_h3.png`

## Primary Results

### Decision-Only Clean $\tau=3$

This is the clean test of the theory. K=1 and K=2 do not cover the first informative future token. K=3 does.

| init | K | reach rate for $Q\ge0.9$ | mean $T_\theta$ among reached | early AUC | full AUC | final $Q$ |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| identical | K=1 | 0.00 | NA | 0.250 | 0.250 | 0.250 |
| identical | K=2 | 0.00 | NA | 0.250 | 0.250 | 0.250 |
| identical | K=3 | 0.60 | 2167 | 0.537 | 0.671 | 0.800 |
| random | K=1 | 0.00 | NA | 0.277 | 0.255 | 0.250 |
| random | K=2 | 0.00 | NA | 0.281 | 0.255 | 0.250 |
| random | K=3 | 0.40 | 0 | 0.644 | 0.728 | 0.750 |

Interpretation: K=3 clearly separates from K=1/K=2. This supports the core efficiency statement in the controlled single-prefix setting: covering the first informative horizon gives earlier semantic recovery from $h_T$.

![Clean Q curves](figures/clean_q_curves.png)

### All-Position Clean $\tau=3$

All-position training is closer to LM-style training because every valid position contributes loss. Here K=3 remains strongest, but K=1/K=2 are no longer blind because other positions create indirect learning paths.

| init | K | reach rate for $Q\ge0.9$ | mean $T_\theta$ among reached | early AUC | full AUC | final $Q$ |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| identical | K=1 | 0.80 | 375 | 0.838 | 0.834 | 0.850 |
| identical | K=2 | 0.60 | 333 | 0.771 | 0.731 | 0.850 |
| identical | K=3 | 1.00 | 300 | 0.965 | 0.993 | 1.000 |
| random | K=1 | 1.00 | 1000 | 0.956 | 0.935 | 0.950 |
| random | K=2 | 0.80 | 0 | 0.952 | 0.929 | 0.950 |
| random | K=3 | 1.00 | 0 | 1.000 | 1.000 | 1.000 |

Interpretation: K=3 is still best, especially in final and full-AUC recovery, but the claim must shrink: all-position training tests relative efficiency, not exclusive learnability.

## Controls

Noisy control sets the horizon-3 target independent of $Z$. In decision-only, noisy K=3 does not reproduce clean K=3: final $Q$ remains 0.25/0.30 and early AUC is 0.250/0.396. This protects the clean decision-only mechanism.

In all-position, noisy controls can produce high early recovery, especially under random initialization: noisy K=1/K=2/K=3 early AUC is 0.958/0.946/0.985. This is a boundary warning. It means all-position $Q$ can be inflated by indirect paths or initialization effects, so noisy all-position results cannot be used as clean evidence of direct MTP usefulness.

![Noisy all-position Q curves](figures/noisy_all_position_q_curves.png)

Redundant control sets an earlier target to reveal $Z$. As expected, K=2 and K=3 both reach near-perfect recovery in all-position, because the useful information is already available before horizon 3. This supports the information-structure interpretation rather than a horizon-label-only story.

## Local-Loss Guard

K=3 does not gain long-horizon recovery by sacrificing the local shared targets. In clean decision-only and all-position, K=3 keeps final $Y_1$ and $Y_2$ accuracy at 1.00 with near-zero loss. The local guard passes for the active local targets.

![Local loss guard](figures/local_loss_guard_y1.png)

## Gradient Usefulness

The gradient audit records:

$$
c=\frac{\langle g_1,g_\tau\rangle}{\|g_1\|\|g_\tau\|},\qquad
r=\frac{\|g_\tau\|}{\|g_1\|},\qquad
\rho=\frac{\langle g_1+\lambda g_\tau,g_1\rangle}{\|g_1\|^2}.
$$

The important result is negative but useful: gradient cosine or norm ratio alone does not robustly explain future semantic recovery. For clean K=3 horizon-3 gradients, some all-position identical-branch MLP signals support later $\Delta Q$, but decision-only and random-init patterns are mixed or insufficient. Therefore H4 is not yet established.

![Gradient usefulness audit](figures/gradient_usefulness_clean_h3.png)

Interpretation: we should not say "MTP gradients are more useful" yet. The stronger supported statement is objective-level: K=3 exposes $h_T$ to a direct semantic target; the optimization-level explanation remains open.

## Hypothesis Verdict

| Hypothesis | Verdict | Reason |
| --- | --- | --- |
| H1: K=3 is earlier in decision-only clean $\tau=3$ | supported | K=1/K=2 never reach threshold; K=3 reaches in 40-60% of seeds and has much higher early AUC |
| H2: K=3 does not hurt local targets | supported | active $Y_1/Y_2$ accuracy stays 1.00 with near-zero loss |
| H3: all-position K=3 is earlier/stronger and controls are clean | partial | K=3 is strongest in clean all-position, but noisy all-position creates false-positive recovery |
| H4: extra-horizon gradient explains later $Q$ | insufficient | gradient metrics are mixed; cosine/norm ratio are not enough |

## Claim Boundary

Can claim: in the controlled $\tau=3$ construction, MTP with K=3 is more efficient than K=1/K=2 at recovering the early variable from the decision hidden state when the objective directly covers the first informative future token.

Cannot claim: MTP is generally better in natural language; larger K is always better; all-position K=1/K=2 cannot learn $Z$; gradient cosine sign determines usefulness; noisy all-position recovery is valid semantic evidence.

## Next Decision

Do not jump to broad next-K scaling yet. The next theoretical discussion should focus on how to turn the direct-supervision result into an optimization-efficiency statement: under what assumptions does adding the first informative horizon reduce sample/time complexity rather than merely add a representational constraint?
