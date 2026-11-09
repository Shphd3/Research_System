# Task-Relevant Relay Supervision and Standard-Head Utility

## Summary

A13 identifies one controlled sufficient condition under which earlier
future-style supervision improves the ordinary next-token head. The target
must name a variable required by the final answer, it must supervise an earlier
state that lies on the only legal answer path, and that state must be
transported and consumed by the ordinary head. With every other auxiliary
target fixed, answer-\(A\) relay supervision beat same-vocabulary nuisance-\(B\)
supervision by 0.2315 nats of 0--1,000-step answer AULC on the relay path but
only 0.0181 nats on the bypass path. The 0.2134-nat interaction had a 95%
paired-bootstrap interval of [0.1646, 0.2585] and was positive in 8/8 seeds.

This is a finite-budget credit-assignment result, not a claim that NTP never
sees the answer. NTP sees the same answer one position later and can learn the
carrier.

## 1. Definitions

- **Ordinary or standard head:** the next-token prediction head used for both
  training and evaluation; no auxiliary head is used at evaluation.
- **Relay-required:** the answer state has no evidence path except through an
  earlier relay state.
- **Bypass-available:** the answer state may read the early evidence directly.
- **Task-relevant target:** an auxiliary label whose value changes the correct
  answer under the known data-generating rule.
- **Finite-budget utility:** reduction in the ordinary-head answer NLL averaged
  over a frozen training window.

## 2. Minimal Model

Let \(A,B\) be value tokens and define the answer \(Y=A\). The relay state is

\[
S=f_\theta(A,B).
\]

In the relay condition,

\[
\hat Y=g_\theta(S),
\]

while in the bypass condition \(g_\theta\) can also read \(A\) directly.

The final controlled objectives are identical except for one auxiliary label
at the relay:

\[
T^A=(x_2,x_3,x_4,x_5,A),
\]

\[
T^B=(x_2,x_3,x_4,x_5,B).
\]

\(A\) and \(B\) use the same vocabulary and have exactly matching marginal counts
inside each split. Both are predictable from relay evidence. Their causal task
roles differ:

\[
Y(\operatorname{do}(A=a),\operatorname{do}(B=b))=a.
\]

NTP still predicts \(A\) from the later answer state. Answer-\(A\) auxiliary
supervision supplies an additional direct path at the earlier relay state.

## 3. Why the Research Line Previously Stalled

Three questions had been mixed:

1. can a model form and transport a state?
2. can it bind a query to the correct value?
3. does earlier task-relevant supervision improve the later ordinary head?

The first query-conditioned carrier required all three at once and was
unstable. Removing query binding produced a valid carrier. This showed that
query binding is a separate workload property rather than a harmless carrier
detail.

The first broad objective comparisons then imposed a second bad condition:
every post-treatment objective arm had to pass capability. Because shared-aux
itself destabilized the relay task, that rule conditioned on an outcome of the
treatment and marked two 8/8-sign effects insufficient. A13 retained those
verdicts, removed post-treatment selection in a new estimand, and changed only
one label at a time.

## 4. Evidence Chain

| Stage | Decision object | Result | Recognition update |
| --- | --- | --- | --- |
| A11 prior | does informative future supervision create earlier signal? | yes locally; later standard-head use not established | formation is not use |
| A12 warning | is the proposed compositional carrier valid and NTP-learnable? | no | objective comparison must wait |
| A13_00_01 | query selection plus relay | unstable NTP carrier | query binding is a separate property |
| A13_00_02 | single-value relay | all six carrier gates pass | NTP has a real learnable scale and the ordinary head uses the relay |
| A13_00_03 | full Next-2 versus shared-aux | positive in 16/16 combined seeds, but original gates insufficient | post-treatment capability must not define carrier validity |
| A13_00_04 | fixed marker versus answer \(A\) at one relay target | pass; interaction 0.8747 nats | effect localizes to the relay target |
| A13_00_05 | nuisance \(B\) versus answer \(A\) at one relay target | pass; interaction 0.2134 nats, 8/8 | downstream task relevance matters beyond target variability |

## 5. What MTP Is Better For Under Current Evidence

The supported object is not “code” or “long context” as a modality. It is a
task state with the following conjunction:

1. a future target reveals or names a variable needed downstream;
2. that variable must be represented at an earlier state;
3. the final ordinary head has no adequate bypass around that state;
4. transport and readout are learnable;
5. the later NTP credit path is not already equally efficient under the fixed
   budget;
6. the earlier auxiliary target is predictable and does not add overwhelming
   noise or conflicting background gradients.

The advantage should shrink or disappear when a direct path exists, the
future target is nuisance content, NTP already supplies sufficient credit,
transport erases the state, the ordinary head does not read it, or the future
target is too uncertain.

## 6. Code Versus Natural-Language Hypothesis

The result gives a testable reason that some code or planning workloads may
benefit more than ordinary local text:

- exact identifiers, program state, constraints, and intermediate results may
  be created well before their executable consequence;
- the later output may require that state rather than a semantically redundant
  local paraphrase;
- control flow and data flow create explicit state-transport paths;
- a wrong intermediate value often changes an exact downstream token or
  execution result.

Natural-language text often contains local redundancy, paraphrases, and
multiple bypass cues, although some long-context reasoning tasks do not.
Therefore the prediction is property-based, not modality-based:

> MTP should help code more only to the extent that matched code examples
> contain more necessary, answer-aligned delayed states than matched text
> examples.

No real code/text comparison has yet tested this prediction.

## 7. MoE Boundary

The learned relay state may become a Router signal only if it predicts
held-out differences in expert utility. Readability, geometry, or MTP benefit
alone does not imply that different experts should receive the token. The MoE
bridge therefore remains downstream of a fixed-budget expert-utility test.

## 8. Claim Boundary And Next Decision

Supported: one synthetic sufficient condition for finite-budget ordinary-head
utility of earlier task-relevant supervision.

Not supported: general MTP superiority, standard implementation equivalence,
long token-distance effects, multi-evidence composition, paraphrase
invariance, code/text transfer, planning value, long-context scaling, or MoE
utility.

**Exactly one next decision:** validate query-conditioned binding as a
separate NTP-only carrier property before testing an objective interaction on
composition.
