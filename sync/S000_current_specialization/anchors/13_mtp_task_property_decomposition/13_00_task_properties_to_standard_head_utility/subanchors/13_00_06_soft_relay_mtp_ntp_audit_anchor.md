# Does MTP Utility Grow Continuously With Causal Relay Dependence?


Parent anchor:
[13_00 task properties to standard-head utility](../13_00_task_properties_to_standard_head_utility_anchor.md)

## 1. Problem Definition

### Terminology / Definitions

| Term | Plain meaning | Concrete computation | Cannot prove |
| --- | --- | --- | --- |
| direct path | `ANSWER` reads early answer variable $A$ without first using `RELAY` | the layer-wise `ANSWER` query to the $A$ key | that the model causally uses the edge |
| soft relay | the direct edge remains legal but receives a fixed attention-logit penalty | penalty $\beta\in\{0,2,4\}$ in both layers | a natural-language long-range bottleneck |
| hard relay | the direct edge is forbidden | $\beta=+\infty$ | that difficulty alone is relay dependence |
| direct causal effect | damage caused by deleting the direct edge after training | $D_{\rm direct}=L_{\rm delete\ A}-L_{\rm native}$, nats | that attention weight alone is causal use |
| relay causal effect | damage caused by replacing the layer-1 relay state with an in-distribution state carrying a wrong $A$ | $D_{\rm relay}=L_{\rm wrong\ donor}-L_{\rm native}$, nats | information formation at the source |
| measured relay reliance | the relay share of the two positive intervention effects | $\rho=D^+_{\rm relay}/(D^+_{\rm relay}+D^+_{\rm direct}+10^{-8})$ | exhaustive mediation through only these paths |
| information formation | $A$ becomes encoded in an earlier state | probe or source-state intervention | transport or standard-head use |
| state transport | the formed information survives to the relay state | relay-state decodability/intervention | standard-head use |
| standard-head use | changing the transported state changes the ordinary next-token answer | donor-patch answer response | general task utility |
| AULC | time-average ordinary-head answer NLL from step 0 through 1,000 | trapezoidal area divided by 1,000, in nats; lower is faster learning | wall-clock or compute efficiency |

**Single decision question:** as the only direct `ANSWER`-to-$A$ attention
edge is weakened from normal access to complete removal, does the
information-specific ordinary-head benefit of informative-MTP increase with
the *measured causal use* of `RELAY`, rather than appearing only at the hard
mask endpoint or merely tracking overall task difficulty?

The primary comparison is informative-MTP versus matched shared-aux. NTP-only
is a carrier audit and secondary system baseline, not the information-content
control.

## 2. Physical Priors

1. **Continuity prior.** If earlier answer-aligned credit matters because the
   standard head increasingly depends on the relay state, its benefit should
   grow as causal relay use grows; an effect confined to a hard mask instead
   suggests a graph-discontinuity or difficulty explanation.
2. **Compensation prior.** A finite logit penalty is only a nominal treatment.
   The model may increase its query-key score and compensate, so the mechanism
   variable must be measured by post-training interventions.
3. **Dose prior.** Matching active heads and nominal losses removes a gross
   objective-count confound, but realized auxiliary gradient norms can still
   differ. They must be measured rather than assumed equal.
4. **Formation-use separation.** An auxiliary target may form an $A$-related
   state without transporting it or making the ordinary head depend on it.

These are empirical priors, not Transformer theorems.

## 3. Falsifiable Hypotheses

For path penalty $r$, define

$$
U_r
=
\operatorname{AULC}_{\rm shared\text{-}aux,r}
-
\operatorname{AULC}_{\rm informative\text{-}MTP,r}.
$$

**H1 (continuous relay-dependence hypothesis).** $U_r$ has a positive paired
slope with NTP-measured relay reliance $\rho_r$ across the four registered
path strengths, and the positive trend remains among the three finite
penalties. At least one intermediate penalty must improve over the normal
direct-path condition; the hard endpoint cannot be the sole source of the
trend.

**Strongest rivals.** The apparent trend is caused by (a) larger realized
auxiliary gradients, (b) slower NTP learning as the graph becomes harder, (c)
an abrupt hard-mask regime change, or (d) nominal penalties that do not create
ordered causal dependence.

**Main falsifier:** after Stage 0 establishes ordered, learnable causal relay
dependence, $U_r$ is unrelated to $\rho_r$, or only the hard-mask endpoint has
positive benefit.

**Pass:** the registered overall and finite-penalty relay-reliance slopes are
positive with their paired-bootstrap lower bounds above zero, at least one
intermediate contrast over the normal path is positive, and the reliance
coefficient remains positive after the registered baseline-difficulty and
realized-gradient-dose adjustments.

**Fail / Stop:** Stage 0 is valid and powered, but the benefit is confined to
the hard mask, has no positive relation to measured reliance, or only follows
overall NTP slowing.

**Insufficient:** Stage 0 does not create ordered dependence, any critical
condition is not learnable, the fixed AULC window has no common dynamic range,
or uncertainty/collinearity cannot separate the registered verdicts.

## 4. Mathematical Model

Let $A,B\overset{\rm iid}{\sim}\operatorname{Unif}(\mathcal V)$ and $Y=A$.
The frozen sequence is

```text
[BOS] [FIXED] [A] [B] [RELAY] [ANSWER] [A]
```

At both Transformer layers $\ell\in\{1,2\}$, the only variable attention edge
has logit

$$
z^{(\ell)}_{\text{ANSWER},A}(\beta)
=
\frac{q^{(\ell)}_{\text{ANSWER}}\cdot k^{(\ell)}_A}{\sqrt d}
-\beta,
$$

where $\beta\in\{0,2,4,+\infty\}$. `ANSWER` can always attend to `RELAY` and
itself; `FIXED` and $B$ are never alternate direct inputs. Thus only one graph
edge changes, and $\beta=+\infty$ exactly recovers the hard relay endpoint.

The all-position ordinary loss is

$$
\mathcal L_1
=
\frac{1}{T-1}\sum_{t=0}^{T-2}
\operatorname{CE}(p_1(h_t),x_{t+1}).
$$

The three registered objectives are

$$
\mathcal L_{\rm NTP}=\mathcal L_1,
$$

$$
\mathcal L_{\rm SA}
=
\tfrac12\left[
\mathcal L_1+
\frac{1}{T-2}\sum_{t=0}^{T-3}
\operatorname{CE}(p_2(h_t),x_{t+1})
\right],
$$

and

$$
\mathcal L_{\rm MTP}
=
\tfrac12\left[
\mathcal L_1+
\frac{1}{T-2}\sum_{t=0}^{T-3}
\operatorname{CE}(p_2(h_t),x_{t+2})
\right].
$$

The auxiliary head is instantiated and trainable in all conditions; it is
inactive only in NTP-only. Shared-aux and informative-MTP match active heads,
loss terms, nominal weights, data, parameters, initialization, and batches.

For each paired seed, the primary trend is the least-squares slope

$$
s_i=\operatorname{slope}_r(U_{i,r},\rho_{i,r}).
$$

The difficulty guard uses NTP-only AULC $H_{i,r}$; the dose guard uses

$$
G_{i,r}
=
\log\frac{\overline{\lVert\nabla_{\theta_{\rm trunk}}
\mathcal L_{\rm aux}^{\rm MTP}\rVert}+10^{-8}}
{\overline{\lVert\nabla_{\theta_{\rm trunk}}
\mathcal L_{\rm aux}^{\rm SA}\rVert}+10^{-8}}.
$$

Within-seed centered regressions test whether the coefficient of $\rho$ stays
positive after $H$, then after both $H$ and $G$, are included. These guards
weaken measured dose/difficulty rivals; they cannot eliminate unmeasured
optimization confounds.

## 5. Computational Realization

Freeze the A13 single-value carrier, 16-value vocabulary, held-out pair split,
two-layer width-64 four-head Transformer, optimizer, 3,000-step budget, and
answer rule. Use fresh paired seeds 1801--1808.

The four path levels are fixed before any comparison:

| Label | $\beta$ | Unnormalized multiplier on the direct edge |
| --- | ---: | ---: |
| `direct_0` | 0 | 1.000 |
| `soft_2` | 2 | $e^{-2}=0.135$ |
| `soft_4` | 4 | $e^{-4}=0.018$ |
| `hard` | $+\infty$ | 0 |

These are logit interventions, not assumed realized attention or use levels.
They are applied in both layers and cannot be changed after reading results.

Stage 0 trains NTP-only at all four levels. Stage 1 is launched only if the
automated Stage-0 gate passes and then trains all three objectives under
paired initialization and batches. Causal audits are registered at steps
1,000 and 3,000; gradient diagnostics are registered at steps
$\{0,100,200,400,600,800,1000\}$.

## 6. Minimal Falsification Tests

### Stage 0: NTP-only carrier gate

1. **Capability:** each path has final mean answer accuracy at least 0.95 and
   at least 7/8 seeds at or above 0.90; each has at least 7/8 first-90%
   checkpoints inside the fixed 0--1,000 window.
2. **Ordered direct use:** $D_{\rm direct}$ has a negative paired slope with
   path rank and its bootstrap upper bound is below zero.
3. **Ordered relay use:** both $D_{\rm relay}$ and $\rho$ have positive paired
   slopes with path rank and bootstrap lower bounds above zero.
4. **Seed stability:** at least 7/8 seed slopes have the registered direction
   for each causal-use object.
5. **Common dynamic range:** every path begins above chance-level answer NLL
   and crosses 90% during the same fixed 0--1,000 observation window rather
   than being solved before the first registered positive checkpoint.

Failure of any Stage-0 item stops execution before Stage-1 objective results
are generated or read.

### Stage 1: objective comparison

1. Compute $U_r$ using ordinary-head answer NLL only.
2. Bootstrap paired seeds for the overall $U$-on-$\rho$ slope and the finite
   $\beta\in\{0,2,4\}$ slope; require lower bounds above zero and at least 7/8
   positive seed slopes.
3. Require at least one intermediate-minus-`direct_0` paired contrast to have
   a positive bootstrap lower bound.
4. Regress within-seed centered $U$ on $\rho$ plus NTP AULC, then on $\rho$
   plus NTP AULC and realized auxiliary gradient-dose ratio. Require the
   reliance coefficient's lower bound above zero in both models; standardized
   design condition number above 100 makes the result insufficient.
5. Report NTP-only-to-MTP system differences, first-90% step, final accuracy,
   all seed-level effects, relay donor patch, direct deletion, and gradient
   norm/cosine trajectories.

## 7. Current Evidence

A13_00_05 established that answer-$A$ relay supervision beats matched
nuisance-$B$ supervision when the relay is structurally necessary:

$$
\bar R_{\rm relay}=0.2315,
\qquad
\bar R_{\rm bypass}=0.0181,
\qquad
\bar\Delta_R=0.2134\ \text{nats}.
$$

All relay and interaction signs were positive across eight seeds. This is a
hard-relay sufficient condition.

A13_00_06 Stage 0 then showed that the registered penalties do create an
ordered causal path shift. Every path reached final accuracy 1.0. Across 8/8
seeds, direct-deletion effect slopes were negative, while wrong-relay effect
and relay-reliance slopes were positive. Mean relay reliance at step 1,000 was
approximately $0$, $0$, $0.345$, and $1.0$ for `direct_0`, `soft_2`, `soft_4`,
and `hard`.

However, `direct_0` reached 90% at the first positive checkpoint (step 20) in
8/8 seeds, while NTP AULC increased from 0.0730 nats at `direct_0` to 0.8508
nats at `hard`. The frozen common-dynamic-range gate failed. Stage 1 was not
launched, so $U_r$, gradient-dose adjustment, and a continuous MTP-utility
claim remain undefined.

Result:
[A13_00_06_E01 summary](/Projects/from-attention-to-search/main/experiments/A13/13_00_task_properties_to_standard_head_utility/A13_00_06_E01_soft_relay_mtp_ntp_audit/summary.md).

## 8. Claim Boundary And Next Decision

This subanchor can at most identify a graded mechanism inside one two-layer
synthetic carrier. It cannot establish general MTP superiority, long-context
utility, code-versus-language differences, composition, planning, or MoE
routing value. Even a pass weakens only the *measured* gradient-dose and
baseline-difficulty rivals; it does not prove a unique optimizer mechanism.

**Exactly one next decision:** obtain researcher approval for a measurement-
only Stage-0 repair that preserves all training objects but evaluates every
step through step 40; Stage 1 remains blocked until the common-dynamic-range
gate passes.
