# Does Task Relevance, Not Target Variability, Cause Relay Utility?


Parent anchor:
[13_00 task properties to standard-head utility](../13_00_task_properties_to_standard_head_utility_anchor.md)

## 1. Problem Definition

**Single decision question:** when auxiliary targets have the same vocabulary,
marginal frequency, conditional predictability, head, weight, and position,
does supervising the relay with downstream answer variable $A$ help the
ordinary head more than supervising it with nuisance variable $B$?

This is the narrowest current test of task-relevant future content.

## 2. Physical Priors

The standard answer is $Y=A$. Carrier audit E02 established that changing $A$
changes the answer and changing $B$ should not. Both values are independently
sampled from the same 16-token vocabulary and are directly available to the
relay.

If any variable-valued target or larger gradient is enough, $A$ and $B$
supervision should be equivalent. If downstream alignment matters, $A$ should
help more specifically on the relay-required path.

## 3. Falsifiable Hypotheses

Let `nuisance-aux` equal full Next-2 at the first four auxiliary positions and
predict $B$ at the relay. Let `answer-aux` predict $A$ there.

$$
R_r
=
\operatorname{AULC}_{B,r}
-
\operatorname{AULC}_{A,r},
\qquad
\Delta_R=R_{\mathrm{relay}}-R_{\mathrm{bypass}}.
$$

**H1:** $R_{\mathrm{relay}}>0$ and $\Delta_R>0$.

**Main falsifier:** either effect is non-positive with the pre-treatment
carrier valid.

Pass requires positive bootstrap lower bounds, means at least 0.02 nats, and
at least seven of eight positive paired seeds for both effects.

## 4. Mathematical Model

Let $A,B\overset{\mathrm{iid}}{\sim}\operatorname{Unif}(\mathcal V)$ and
$Y=A$. The two objective vectors are identical except at relay position
$t=4$:

$$
T^A=(x_2,x_3,x_4,x_5,A),
$$

$$
T^B=(x_2,x_3,x_4,x_5,B).
$$

Therefore

$$
H(T^A_4)=H(T^B_4)=\log|\mathcal V|,
$$

and both are deterministically recoverable from the relay input evidence. The
causal difference is

$$
Y(\operatorname{do}(A=a),\operatorname{do}(B=b))=a
\quad\forall a,b.
$$

Thus changing $A$ changes the correct answer, while changing $B$ at fixed $A$
does not. The held-out combination split induces observational association
between $A$ and $B$ inside each split, so this experiment does not claim
$I(B;Y)=0$ on the realized train or evaluation subset.

## 5. Computational Realization

Freeze all A13_00_04 objects. Use two paths, two objectives, and fresh paired
seeds 1701--1708. The nuisance target is the actual $B$ token already present
in each sample; no vocabulary, length, mask, or answer changes.

## 6. Minimal Falsification Tests

1. verify $A$ and $B$ target counts and vocabulary support match;
2. preserve the passed data hash and attention graph;
3. compute $R_{\mathrm{relay}}$ and $\Delta_R$ on all paired seeds;
4. report treatment-arm capability and capability-eligible donor use
   separately from the performance estimand;
5. retain the same effect thresholds as A13_00_04.

## 7. Current Evidence

A13_00_04 passed fixed-marker localization:

$$
\bar D_{\mathrm{relay}}=1.0343,
\qquad
\bar\Delta_D=0.8747\ \text{nats}.
$$

E01 then passed the matched task-relevance control:

$$
\bar R_{\mathrm{relay}}=0.2315,
\qquad
\bar\Delta_R=0.2134\ \text{nats},
$$

with positive signs in 8/8 seeds, all four final capability cells at 1.0, and
donor follow at 1.0 in every relay model.

Result:
[A13_00_05_E01 summary](/Projects/from-attention-to-search/main/experiments/A13/13_00_task_properties_to_standard_head_utility/A13_00_05_E01_task_relevant_target/summary.md).

## 8. Claim Boundary And Next Decision

The pass establishes a minimal task-relevance interaction in this carrier:
earlier supervision helps more when it names the variable the later standard
head must use. It does not establish arbitrary MTP, future-only necessity,
code/language transfer, long context, composition, planning, MoE, or
compute-scaling value. It also does not establish zero observational
association between the nuisance and answer under the held-out split.

**Exactly one next decision:** validate query-conditioned binding as a separate
NTP-only carrier property before comparing objectives on a compositional task.
