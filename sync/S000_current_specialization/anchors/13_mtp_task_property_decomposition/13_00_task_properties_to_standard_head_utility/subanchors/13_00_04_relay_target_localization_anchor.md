# Is the Answer-Aligned Relay Target the Local Cause of Next-2 Utility?

Thinking Card source:
[long_horizon_compositional_workload_thinking_card_cn.md](/daily_research_reports/backup/2026/07/0717/mtp_long_horizon_compositional_workload/long_horizon_compositional_workload_thinking_card_cn.md)

Parent anchor:
[13_00 task properties to standard-head utility](../13_00_task_properties_to_standard_head_utility_anchor.md)

## 1. Problem Definition

**Single decision question:** holding every other all-position auxiliary target
fixed, does changing only the relay-position target from the structural
`[ANSWER]` marker to answer value $A$ cause the ordinary head to learn faster,
especially when the relay is structurally necessary?

This localizes the E01/E02 candidate effect. It does not compare generic NTP
with generic MTP; it changes one auxiliary label at one state.

## 2. Physical Priors

The relay state must retain $A$ for the later ordinary head. A target that asks
that state to predict $A$ is aligned with its downstream role. A fixed-marker
target can be irrelevant or can encourage the shared state to emphasize a
different direction.

The two prior confirmations showed a 16/16 positive full-objective interaction,
but both remained formally insufficient because a post-treatment capability
guard excluded unstable control outcomes. That pattern motivates, but does not
decide, this fresh-seed localization.

## 3. Falsifiable Hypotheses

Let `background-MTP` use the complete Next-2 auxiliary target sequence except
that the relay state predicts fixed token `[ANSWER]`. Let `full-MTP` differ
only by making the relay state predict $A$.

Define

$$
D_r
=
\operatorname{AULC}_{\mathrm{background},r}
-
\operatorname{AULC}_{\mathrm{full},r},
$$

and

$$
\Delta_D=D_{\mathrm{relay}}-D_{\mathrm{bypass}}.
$$

**H1:** $D_{\mathrm{relay}}>0$ and $\Delta_D>0$.

**Strongest rival:** the earlier result came from the other four shifted
Next-2 targets, not from answer-aligned credit at the relay.

Pass requires positive bootstrap lower bounds, mean effects at least 0.02
nats, and at least seven of eight positive paired seeds for both quantities.

## 4. Mathematical Model

For auxiliary positions $t=0,\ldots,4$, full Next-2 uses

$$
T^{\mathrm{full}}=(x_2,x_3,x_4,x_5,x_6).
$$

The background control uses

$$
T^{\mathrm{bg}}=(x_2,x_3,x_4,x_5,x_5).
$$

Thus

$$
T^{\mathrm{full}}_t=T^{\mathrm{bg}}_t
\quad\forall t<4,
$$

and only

$$
T^{\mathrm{full}}_4=A,
\qquad
T^{\mathrm{bg}}_4=[\mathrm{ANSWER}]
$$

differs. Both targets are Bayes-predictable at the relay in the validated
two-layer carrier.

## 5. Computational Realization

Freeze the E02 carrier, model, optimizer, 3,000-step budget, and 1,000-step
AULC horizon. Cross two paths (`relay`, `bypass`) with two objectives
(`background-MTP`, `full-MTP`) on fresh paired seeds 1601--1608.

The carrier was validated before either treatment using NTP-only data. Arm
capability is therefore an outcome, not a post-treatment inclusion rule.

## 6. Minimal Falsification Tests

1. data hash and attention graph equal the passed carrier;
2. at least seven capability-eligible models per objective must show donor
   follow if that many eligible models exist; otherwise causal-use evidence for
   that arm is insufficient but performance remains a treatment outcome;
3. primary $D_{\mathrm{relay}}$ and $\Delta_D$ use every paired seed;
4. report arm capability without conditioning the performance estimand on it.

The main falsifier is non-positive $\Delta_D$ with a valid pre-treatment
carrier.

## 7. Current Evidence

E01 candidate:
$\bar U_{\mathrm{relay}}=0.7127$ and
$\bar\Delta_{\mathrm{relay}}=0.6333$ nats, 8/8 positive.

E02 candidate:
$\bar U_{\mathrm{relay}}=1.4703$ and
$\bar\Delta_{\mathrm{relay}}=1.3901$ nats, 8/8 positive.

Both original verdicts are insufficient. E02 showed that matched shared-aux
itself destabilized the relay task in three seeds, which is a post-treatment
outcome rather than evidence that the pre-treatment carrier is invalid.

E01 passed the one-label localization:

$$
\bar D_{\mathrm{relay}}=1.0343,
\qquad
\bar\Delta_D=0.8747\ \text{nats}.
$$

Result:
[A13_00_04_E01 summary](/Projects/from-attention-to-search/main/experiments/A13/13_00_task_properties_to_standard_head_utility/A13_00_04_E01_relay_target_localization/summary.md).

## 8. Claim Boundary And Next Decision

The pass establishes that one answer-aligned target at the necessary relay
state is a local sufficient cause of finite-budget ordinary-head utility in
this carrier. It would not show that every MTP position helps, that the full
MTP gain is entirely local, or that code, language, long context, composition,
planning, or MoE inherits the effect.

**Exactly one next decision:** compare answer-$A$ against same-distribution
nuisance-$B$ supervision at the relay.
