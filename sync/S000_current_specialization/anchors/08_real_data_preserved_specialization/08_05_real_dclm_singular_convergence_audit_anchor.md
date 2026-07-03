---
anchor_id: A08_05_real_dclm_singular_convergence_audit
parent_node: A08_00_real_data_preserved_specialization_mainline
status: draft
canonical_language: en
---

# A08_05 Real-DCLM Singular Convergence Audit Anchor

## 0. Thinking Card

**Phenomenon:** Synthetic convergence may not exist in real DCLM matrices or gate inputs.

**Mechanism guess:** early real-DCLM training creates stable high-gain directions in selected blocks and gate inputs.

**Key variables:** $W_Q,W_K,W_{\mathrm{out}}$, gate input covariance, $K_i$, $G_i$, common margin.

**Causal relation:** early CE feedback -> stable high-gain real directions -> route overwrite risk.

**Observable metric:** real-DCLM direction drift $K_i@step0-10$.

**Alternative explanation:** proxy collapse may be gate-specific and unrelated to singular directions.

**Decision:** pursue real method only if real convergence targets are measurable.

## 1. Problem Definition

**Decision question:** Do real-DCLM early checkpoints contain stable singular/gate-input directions usable as gating anchors?

## 2. Physical Priors

**P1:** real early training has the same direction/gain separation as the controlled surface.

## 3. Falsifiable Hypotheses

**H1:** selected directions have low drift and positive gain growth by step 5/10.
**H2:** these directions correlate with common-logit/load changes.

## 4. Mathematical Model

Use $K_i(t)$ and $G_i(t)$ from A08_01 on real checkpoint matrices and gate-input covariance.

## 5. Computational Realization

Read real-DCLM checkpoints used by A05/A06; compute SVD/covariance trajectories for selected layers.

## 6. Minimal Falsification Test

**Primary metric:** fraction of top directions with low $K_i$ and positive $G_i$.
**Pass:** stable targets exist in layers 3/4/5.
**Fail:** no stable target or no relation to routing overwrite.

## 7. Current Evidence

A05_04_03 shows common margin explodes by step 10; A06_12 shows proxy routing is erased by step 5/10.

## 8. Claim Boundary And Next Decision

**Can claim:** real convergence targets exist.
**Cannot claim:** preservation method works.
**Next decision:** define real initialization specialization in A08_06.
