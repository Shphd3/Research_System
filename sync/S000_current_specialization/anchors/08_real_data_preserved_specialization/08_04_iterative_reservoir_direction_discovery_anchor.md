---
anchor_id: A08_04_iterative_reservoir_direction_discovery
parent_node: A08_00_real_data_preserved_specialization_mainline
status: weakened_iterative_loop_failed
canonical_language: en
---

# A08_04 Iterative Reservoir Direction Discovery Anchor

## 0. Thinking Card

**Phenomenon:** r1 suggests a loop: freeze a converged direction, route residual to reservoir, then extract the next long-tail direction.

**Mechanism guess:** nested features can be discovered one stable direction at a time.

**Key variables:** extracted directions $P_1,P_2,\ldots$, residual space, per-level loss, old-feature retention.

**Causal relation:** freeze stable direction -> residual learns next child -> new stable direction -> repeat.

**Observable metric:** new child-direction alignment after each iteration.

**Alternative explanation:** apparent discovery may be supervised labels or capacity growth.

**Decision:** pursue only if each iteration discovers a new nested level while preserving old levels.

## 1. Problem Definition

**Decision question:** Can repeated common/residual extraction discover nested directions sequentially?

## 2. Physical Priors

**P1:** nested learning has a direction hierarchy, not a single common/rare split.

## 3. Falsifiable Hypotheses

**H1:** iteration 1 aligns to $A$, iteration 2 to $B|A$, iteration 3 to $C|AB$.
**H2:** old levels remain accurate.

## 4. Mathematical Model

$$
P_{\le k}=\sum_{j=1}^k P_j,\qquad h_{k+1}=(I-P_{\le k})h.
$$

**Falsifier:** later directions repeat old directions or old losses regress.

## 5. Computational Realization

Run synthetic nested levels with known directions; after each stage freeze the discovered projector and train residual reservoir.

## 6. Minimal Falsification Test

**Primary metric:** next-level direction alignment.
**Pass:** new directions align to new child features and old losses stay stable.
**Fail:** repeated extraction collapses to the same common direction.

## 7. Current Evidence

**Observation:** A08_04 full run `a08_singular_preservation_full_20260628_2`
recovers stage-1 A alignment `0.7819`, but learned stage-2 next alignment is
`-0.1928` and learned stage-3 next alignment is `-0.1023`.

**Observation:** oracle residual debug gives weak B alignment `0.0567` after
removing true A, but positive C alignment `0.2601` after removing true A/B.

**Interpretation:** simple "freeze old direction and train residual" does not
discover nested directions sequentially.

**Boundary:** a stage-local objective or better residualization is needed before
iterative discovery can be a method claim.

**Evidence links:** `../../experiments/A08/A08_04_iterative_reservoir_direction_discovery/summary.md`,
`../../experiments/A08/A08_04_iterative_reservoir_direction_discovery/detailed.md`.

## 8. Claim Boundary And Next Decision

**Can claim:** the first common direction is recoverable.

**Cannot claim:** sequential reservoir discovery or real-data hierarchy
discovery.

**Next decision:** park iterative discovery and move the 06 bridge through
real-DCLM convergence/preservation audits that do not rely on A08_04.
