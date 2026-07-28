# Which Task Properties Convert Earlier Future Supervision Into Standard-Head Utility?

Thinking Card source:
[long_horizon_compositional_workload_thinking_card_cn.md](/daily_research_reports/0717/mtp_long_horizon_compositional_workload/long_horizon_compositional_workload_thinking_card_cn.md)

## 1. Problem Definition

### Terminology / Definitions

| Term | Plain meaning | Concrete object / computation | Why it matters | Cannot prove |
| --- | --- | --- | --- | --- |
| standard head | the ordinary head used to predict the next token and the only head kept at evaluation | $p_1(x_{t+1}\mid h_t)$ | all functional claims must appear here | that the internal state has a particular semantics |
| informative-MTP | an auxiliary head predicts the token two positions ahead | $p_2(x_{t+2}\mid h_t)$ | places the answer target directly on the relay position | a pure information-content effect independent of horizon |
| matched shared-aux | the same auxiliary-head structure predicts the next token instead | $p_2(x_{t+1}\mid h_t)$ with matched active terms and weight | controls generic auxiliary-head and loss-count effects | realized gradient-norm or trajectory matching |
| relay-required | the answer position has no legal evidence path except through an earlier hidden state | graph reachability plus hidden-state intervention | makes state formation and use necessary | long natural-language context |
| finite-budget utility | lower standard-head answer risk during a fixed registered training window | mean answer NLL over registered checkpoints, in nats | measures learning efficiency without relying on final saturation | wall-clock or FLOP superiority |
| task-property interaction | the MTP-minus-control benefit changes when one task property changes | difference of paired utility contrasts | identifies a property-dependent effect in the tested carrier family | general workload transfer |

**Single decision question:** Which minimal task property makes the earlier
task-relevant target supplied by informative-MTP improve the ordinary
next-token head relative to a matched auxiliary control?

The line does not start by assuming that code, planning, composition, or token
distance is the answer. It first establishes one valid carrier, then changes
one property at a time.

## 2. Physical Priors

1. **State-necessity prior.** Earlier supervision can have functional value
   only when the state it trains lies on a necessary path to the standard-head
   answer.
2. **Credit-path prior.** If the ordinary answer loss reaches the same state
   only through an additional state transition, an aligned direct auxiliary
   target may provide a cleaner or shorter training signal.
3. **Conditionality prior.** The benefit disappears or reverses when the later
   NTP path is already sufficient, the future target is noisy or irrelevant,
   transport erases the state, or background gradients conflict with it.

These are empirical priors. They are not Transformer theorems.

## 3. Falsifiable Hypotheses

**Parent hypothesis.** On a valid, learnable, non-saturated carrier,
informative-MTP has positive finite-budget standard-head utility only when its
future target is aligned with a state that the answer must later use.

**Strongest rival.** Apparent MTP gains are caused by invalid carrier design,
learner capacity, auxiliary loss scale, easier target statistics, saturation,
or a direct answer bypass rather than earlier task-relevant credit.

**Pass:** a registered task-property interaction is positive after the carrier,
capability, dynamic-range, and standard-head-use gates pass.

**Fail:** the carrier is valid and powered, but the interaction is practically
zero or opposite.

**Insufficient:** any carrier gate fails, objectives do not share a learnable
performance range, or the comparison changes more than the registered property.

## 4. Mathematical Model

Let $A,B\in\mathcal V$ be early values, $Q\in\{0,1\}$ a delayed selector, and

$$
Y =
\begin{cases}
A,&Q=0,\\
B,&Q=1.
\end{cases}
$$

The required relay state is a sufficient statistic

$$
S=f_\theta(A,B,Q),
\qquad
\hat Y=g_\theta(S).
$$

In the relay-required condition, the graph forbids $g_\theta$ from directly
reading $A$, $B$, or $Q$. In the bypass condition, those direct edges are
allowed while the tokens, labels, vocabulary, and model size remain fixed.

For sequence $x_{0:T-1}$ and hidden states $h_t$, the all-position objectives
are

$$
\mathcal L_{\mathrm{NTP}}
=
\frac{1}{T-1}\sum_{t=0}^{T-2}
\operatorname{CE}(p_1(h_t),x_{t+1}),
$$

$$
\mathcal L_{\mathrm{SA}}
=
\mathcal L_{\mathrm{NTP}}
+
\frac{\lambda}{T-2}\sum_{t=0}^{T-3}
\operatorname{CE}(p_2(h_t),x_{t+1}),
$$

and

$$
\mathcal L_{\mathrm{MTP}}
=
\mathcal L_{\mathrm{NTP}}
+
\frac{\lambda}{T-2}\sum_{t=0}^{T-3}
\operatorname{CE}(p_2(h_t),x_{t+2}).
$$

At relay position $r=T-3$, informative-MTP directly predicts $Y$, while NTP
predicts $Y$ one position later. Schematically,

$$
g_{\mathrm{direct}}
=
\nabla_\theta\ell_{\mathrm{aux}}(h_r,Y),
\qquad
g_{\mathrm{later}}
\supset
J_{r\rightarrow r+1}^{\top}
\nabla_{h_{r+1}}\ell_{\mathrm{std}}(h_{r+1},Y).
$$

A direct path is beneficial only if it aligns with answer-risk reduction,
survives the full-objective background, is transported, and is readable by the
standard head.

For task property $P$, define standard-head finite-budget utility

$$
U_P
=
\operatorname{AULC}_{\mathrm{SA},P}
-
\operatorname{AULC}_{\mathrm{MTP},P},
$$

where AULC is the registered checkpoint-average answer negative
log-likelihood. The parent decision object is an interaction

$$
\Delta_P=U_{P=1}-U_{P=0}.
$$

## 5. Computational Realization

The initially proposed sequence was

```text
[BOS] [value-A] [value-B] [selector] [RELAY] [ANSWER] [selected-value]
```

The answer token is a target, never an input to the prediction state. A fixed
sparse causal attention graph gives `RELAY` access to both values and the
selector. Under relay-required attention, `ANSWER` can read only `RELAY`; with
two layers, layer 1 can form the state and layer 2 can consume it. A one-layer
relay model is therefore a structural negative control. A one-layer bypass
model is a learner/interface positive control.

Stage 0 showed that this sequence bundled relay with query-conditioned
selection. The comparison-ready frozen carrier is therefore

```text
[BOS] [FIXED] [value-A] [nuisance-B] [RELAY] [ANSWER] [value-A]
```

The staged subanchors are:

1. `13_00_01`: audit and close the query-conditioned carrier;
2. `13_00_02`: validate the entropy-matched single-value carrier;
3. `13_00_03`: informative objective by relay-necessity interaction;
4. `13_00_04`: localize the effect to one relay-position target;
5. `13_00_05`: match answer-$A$ against nuisance-$B$ target content;
6. `13_00_06`: soft-relay root-cause audit before adding a new task property;
7. `13_00_07`: query-conditioned selection versus single-value copy;
8. `13_00_08`: surface-form invariance with latent task fixed;
9. `13_00_09`: code/text mapping after matched-property evidence;
9. MoE bridge only if the learned state predicts held-out expert utility.

Each stage inherits all previous gates. Failure stops later interpretation; it
does not trigger a larger task.

## 6. Minimal Falsification Tests

| Order | One uncertainty | Main falsifier | Allowed next step |
| --- | --- | --- | --- |
| 1 | Is the carrier structurally valid, learnable, and used through the relay? | two-layer NTP cannot solve held-out items or relay intervention does not control the standard answer | objective comparison |
| 2 | Does relay necessity amplify the full-objective contrast? | no positive relay utility or interaction | local target audit |
| 3 | Is the effect caused by the relay-position target? | one-label intervention has no positive interaction | content matching |
| 4 | Does downstream relevance matter beyond target variability? | answer-$A$ does not beat matched nuisance-$B$ | query-composition test |
| 5 | Does utility increase continuously with measured relay dependence? | benefit appears only at the hard mask or only tracks overall slowing | query-conditioned composition test |
| 6 | Does query-conditioned binding add value beyond copying one state? | no positive selection-versus-copy interaction | surface invariance only with a reduced claim |
| 7 | Is the effect invariant to equivalent surface encodings? | latent-equivalent rewrites erase or reverse it | code/text mapping |
| 8 | Do matched code-like and text-like workloads differ after property control? | modality label adds no interaction after property matching | MoE bridge remains separate |

## 7. Current Evidence

A11 establishes an earlier task-related direct signal and shared-parameter
reachability, but not a stable strong standard-head use increment. A12 shows
why capability and workload validity must precede objective comparison.

A13 now establishes one controlled sufficient condition. On the passed
single-value carrier, changing only the necessary relay target from
same-distribution nuisance $B$ to answer variable $A$ produced

$$
\bar R_{\mathrm{relay}}=0.2315,
\qquad
\bar R_{\mathrm{bypass}}=0.0181,
\qquad
\bar\Delta_R=0.2134\ \text{nats}.
$$

The relay effect and interaction were positive in 8/8 paired seeds; every
objective/path cell reached final accuracy 1.0 and every relay donor-use audit
scored 1.0. Therefore task-relevant earlier credit has finite-budget
ordinary-head utility when the trained state is structurally necessary in this
carrier.

A13_00_06 established that penalties $0,2,4,+\infty$ shift measured causal use
from the direct edge toward `RELAY`: all three registered path-rank slopes had
the expected sign in 8/8 seeds. It did **not** establish a graded objective
effect. `direct_0` reached 90% at the first positive checkpoint in every seed,
so the frozen common-dynamic-range gate stopped Stage 1 before shared-aux or
informative-MTP ran. The soft-relay question is therefore insufficient, not a
negative MTP result.

## 8. Claim Boundary And Next Decision

Even a complete synthetic staircase cannot establish general Transformer,
code, natural-language, long-context, planning, or MoE superiority. It can
identify a controlled sufficient condition and counterexamples.

**Exactly one next decision:** obtain researcher approval for the registered
measurement-only soft-relay Stage-0 repair; do not test another task property
or launch the objective comparison until its common-range gate passes.
