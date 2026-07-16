# Rank Competition And Curriculum Controls

Thinking Card source: [12_02_01_rank_and_curriculum_controls_thinking_card.md](12_02_01_rank_and_curriculum_controls_thinking_card.md)

## 1. Problem Definition

**Parent problem:** [12_02 interference, capacity, and curriculum boundary](../12_02_interference_capacity_curriculum_boundary_anchor.md).
**Decision question:** Does structural rank alone create the tradeoff, and can a dose-matched curriculum remove it?
**Not in scope:** Transformer scaling laws.

**Task-relevant rank** is the number of independent factor directions the shared representation can carry in the oracle linear model. It is causally controlled here; it is not inferred from parameter count.

## 2. Physical Priors

**P1:** Two independent factors require two independent channels for zero-error joint representation.
**P2:** A schedule cannot increase the rank constraint.

## 3. Falsifiable Hypotheses

At rank one, MTP should improve the future factor while worsening the standard loss. At rank two, the standard penalty should disappear. Equal-dose curriculum should not repair rank one.

## 4. Mathematical Model

For whitened factors $x=(u,z)$ and a rank-constrained shared map $h=Wx$, the joint objective selects the top-$r$ task directions of

$$
A^TA+\lambda B^TB.
$$

If $r$ is below the dimension of the joint task subspace, one factor direction must be displaced.

## 5. Computational Realization

Use the same oracle-factor dataset and optimizer; intervene only on rank. For curriculum, match $\sum_t\lambda(t)$ between static and scheduled conditions.

## 6. Minimal Falsification Tests

1. Compare rank one with rank two under the same objective.
2. Compare static and scheduled MTP at equal auxiliary dose under rank one.

## 7. Current Evidence

The [rank intervention](/Projects/from-attention-to-search/main/experiments/A12/12_02_interference_capacity_curriculum_boundary/A12_02_01_E01_task_rank_competition/summary.md) shows a 0.9084--1.0218 standard-loss penalty at rank one while the future factor improves in 5/5 seeds; rank two removes the penalty. The [curriculum control](/Projects/from-attention-to-search/main/experiments/A12/12_02_interference_capacity_curriculum_boundary/A12_02_01_E02_curriculum_rank_boundary/summary.md) repairs rank one in 0/5 seeds.

## 8. Claim Boundary And Next Decision

**Can claim:** missing rank is a sufficient tradeoff mechanism in this linear model; curriculum cannot create rank.
**Cannot claim:** model size is the cause in Transformers or curriculum never helps.
**Next decision:** test task-relevant capacity only after a neural checkpoint passes the A12 capability gate.
