# Interference, Capacity, And Curriculum Boundary Anchor

Status: completed as a controlled mechanism boundary; neural and scale transfer remain untested.

## 0. Thinking Card

**Phenomenon:** Extra future supervision can improve the future factor while worsening the standard objective in a limited shared representation.

**Mechanism guess:** The local effect is governed by gradient interaction, while a persistent tradeoff can be caused by insufficient task-relevant representation rank. A training schedule cannot create a missing independent direction.

**Observable metric:** standard-objective loss gap under a controlled rank intervention, with future-factor error as the benefit guard.

**Decision:** structural rank competition is a sufficient mechanism in the linear model; curriculum is not a structural-rank repair; do not infer a Transformer scale law yet.

## 1. Problem Definition

### Terminology / Definitions

| Term | Plain meaning | Concrete object | Why it matters | Cannot prove |
|---|---|---|---|---|
| local gradient interaction | whether the auxiliary update helps or opposes the standard loss for one small step | $-\eta\langle g_N,g_A\rangle$ | predicts immediate interference | long-run cause |
| task-relevant rank | number of independent task directions the shared representation can carry | imposed encoder rank in the oracle model | causal capacity variable | parameter-count scaling |
| dose-matched curriculum | change the timing of auxiliary weight while keeping total auxiliary weight equal | equal $\sum_t\lambda(t)$ | isolates schedule order | more capacity |

**Single decision question:** Can insufficient shared representation rank independently cause an MTP/NTP tradeoff, and can curriculum repair that structural deficit?

## 2. Physical Priors

1. One-step gradient conflict is local and cannot alone explain a persistent trained solution.
2. If two independent factors require two directions, a rank-one representation must trade them off.
3. Curriculum may change an optimization path but cannot increase structural rank.

## 3. Falsifiable Hypotheses

At rank one, MTP should improve the future factor while increasing standard loss; at rank two, the standard penalty should vanish. A dose-matched curriculum should not Pareto-repair the rank-one solution.

## 4. Mathematical Model

Let input factors $u$ and $z$ be independent and let the shared representation have rank $r$. The standard objective predicts both factors; the auxiliary objective places extra weight on $z$. With $r=1$, the optimal shared direction must choose a weighted compromise. With $r=2$, both independent directions can coexist.

For one small parameter step, the paired standard-loss difference is

$$
L_N(\theta-\eta(g_N+\lambda g_A))-L_N(\theta-\eta g_N)
\approx-\eta\lambda\langle g_N,g_A\rangle.
$$

## 5. Computational Realization

First verify the local finite-difference equation on paired cloned updates. Then use an oracle-factor linear encoder and change only rank from one to two. Finally compare static MTP and an equal-total-dose NTP-to-MTP curriculum.

## 6. Minimal Falsification Tests

1. Confirm small-step prediction fidelity while retaining the task-capability guard.
2. Require rank-one MTP to improve the future factor and worsen standard loss.
3. Require the standard penalty to disappear at rank two.
4. Test whether dose-matched curriculum Pareto-improves rank one.

## 7. Current Evidence

The local Taylor equation is numerically accurate at small steps, but its neural task checkpoint was at chance and therefore does not establish task-conditioned interference. In the oracle linear model, rank one produces a standard-loss gap of 0.9084--1.0218 while improving the future factor in 5/5 seeds; rank two removes the gap to numerical zero. Dose-matched curriculum passes the rank-one Pareto criterion in 0/5 seeds. See [rank intervention](../../../../../Projects/from-attention-to-search/main/experiments/A12/12_02_interference_capacity_curriculum_boundary/A12_02_01_E01_task_rank_competition/summary.md), [curriculum boundary](../../../../../Projects/from-attention-to-search/main/experiments/A12/12_02_interference_capacity_curriculum_boundary/A12_02_01_E02_curriculum_rank_boundary/summary.md), and [subanchor 12_02_01](subanchors/12_02_01_rank_and_curriculum_controls_anchor.md). The ineligible local-gradient check is archived as supporting evidence rather than a mainline result.

## 8. Claim Boundary And Next Decision

Supported claim: insufficient representation rank is a sufficient cause of an MTP/NTP tradeoff in the stated linear model, and curriculum cannot repair structural missing rank.

Not supported: parameter count explains model-scale behavior, learned Transformers exhibit the same rank mechanism, or curriculum is generally ineffective. Curriculum may still help nonconvex path conflict when capacity is sufficient.

**Exactly one next decision:** test causal use on a task-capable shared neural checkpoint before reopening scale or curriculum questions.
