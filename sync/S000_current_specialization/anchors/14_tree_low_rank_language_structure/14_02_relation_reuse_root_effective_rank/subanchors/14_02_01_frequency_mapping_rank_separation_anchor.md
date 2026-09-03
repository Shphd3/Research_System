---
anchor_id: 14_02_01_frequency_mapping_rank_separation
status: completed_pass_noninferior
canonical_language: en
companion_cn: 14_02_01_frequency_mapping_rank_separation_anchor_cn.md
parent_anchor: 14_02_relation_reuse_root_effective_rank
experiment_id: A14_02_E02_frequency_mapping_rank_separation
---

# A14_02_01 Frequency–Mapping Rank Separation


## 1. Problem Definition

Decision question: after a common mapping has been learned across surface
aliases, does lowering one target cell's exact optimizer-presentation count
from $F=8$ to $F=1$ increase the frozen-readout ROOT functional rank by more
than two directions?

An exact cell is an alias--entity pair $(r,a)$. A frequency target has
$F\in\{1,8\}$; an unseen cell is a different cell with $F=0$ whose alias and
entity are both observed separately in training. ROOT is the post-final-norm
state immediately before the frozen language head.

## 2. Physical Priors

**P1. Mapping reuse, not raw local frequency, can supply the task direction.**
Other aliases expose the same bijection $y=\pi(a)$, so a rare target cell need
not create its own task coordinate.

**P2. Capability is a hard prerequisite.** A smaller rank is not compression
if the model does not solve new contexts and strictly unseen cells.

**P3. Exact frequency must be changed by redistribution.** Total common-function
dose, optimizer presentations, alias/entity/answer/context marginals, model,
initialization, and optimization budget remain fixed.

## 3. Falsifiable Hypotheses

For paired seed $s$ define

$$
D_s
=
k_{\mathrm{func},s}^{\mathrm{LowF}}
-
k_{\mathrm{func},s}^{\mathrm{HighF}}.
$$

The registered non-inferiority hypothesis is

$$
\mathbb E[D_s]\le\tau,
\qquad
\tau=2\ \text{ROOT directions}.
$$

Support requires at least eight valid paired seeds and a one-sided 95% paired
upper confidence bound no greater than two. Refutation requires the one-sided
95% lower bound to exceed two. Crossing the margin or failing a hard gate is
insufficient.

## 4. Mathematical Model

The common task is

$$
p(y\mid r,a,c)=\mathbf1\{y=\pi(a)\},
$$

where $r$ and nuisance context $c$ do not change the answer mapping. A
calibration-only ordered basis $U$ and mean $\mu$ define

$$
\widetilde h_\rho^{(q)}
=
\mu+U_qU_q^\top(h_\rho-\mu).
$$

With the original output head frozen,

$$
k_{\mathrm{func}}^{\mathrm{fix}}
=
\min\left\{
q:
\Delta CE_q\le0.02\ \mathrm{nat},\ 
\Delta Acc_q\le0.01
\right\},
$$

using persistent passage for every higher rank. Rank is selected on a
calibration-selection split and only validated on a disjoint final test.

## 5. Computational Realization

Sixteen aliases and seventeen entities call one fixed random bijection
$\pi:\mathbb Z_{17}\to\mathbb Z_{17}$. For each seed, four cells per alias are
frequency targets, eight disjoint cells per alias form unseen calibration/test
sets, and the other five cells are high-dose donors. Seven presentations per
target are moved between targets and donors by an integer transportation
table, preserving every registered marginal. The model is the registered
two-layer, one-head, width-64 causal Transformer trained with full-position NTP
cross-entropy.

## 6. Minimal Falsification Tests

1. Realized optimizer counts equal the frozen count matrix.
2. Both conditions pass target-new-context accuracy $\ge0.95$, unseen-cell
   final accuracy $\ge0.75$, and target full-state CE $\le0.10$ nat.
3. Final-test replay at the calibration-selected rank passes the 0.02-nat and
   0.01-accuracy tolerances.
4. Full-rank replay is exact, ROOT shuffling damages the task, and matched-rank
   random subspaces fail.
5. A leave-target-out common-update basis fitted on one probe half captures at
   least 80% of the held-out common-step contrast energy; otherwise E03 is
   parked.

## 7. Current Evidence

E01 separated duplicates from context diversity and observed functional-rank
means 10.2, 11.0, and 12.8 for capability-passing lookup $K=1,4,16$. Archived
E02-v1 passed seen-pair new-context capability but failed strong unseen
component recombination in 5/5 seeds. Neither result isolates exact frequency
inside an actually reused common mapping.

The approved full run completed 10/10 valid paired seeds. LowF and HighF mean
functional ranks were 7.6 and 7.4 directions. The paired mean difference was
0.2, with a one-sided 95% upper bound of 0.5, so the two-direction
non-inferiority hypothesis passed. LowF unseen-cell accuracy was 1.0 in every
seed; replay, shuffle, and random-subspace guards all passed.

Results: [summary](/Projects/from-attention-to-search/main/experiments/A14/14_02_relation_reuse_root_effective_rank/A14_02_E02_frequency_mapping_rank_separation/summary.md) · [detailed](/Projects/from-attention-to-search/main/experiments/A14/14_02_relation_reuse_root_effective_rank/A14_02_E02_frequency_mapping_rank_separation/detailed.md).

## 8. Claim Boundary And Next Decision

Even a pass establishes only that lower exact-cell frequency did not force a
greater registered answer-task ROOT functional rank in this controlled NTP
task. It does not prove that frequency never matters, that raw ROOT or complete
parameters are low rank, or that the result transfers to natural language.

Exactly one next decision: E03 is parked because common-step parameter-space
capture was only 0.478--0.631. Define a fresh-probe common functional/secant
space before any new rare-direction intervention.
