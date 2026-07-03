---
anchor_id: A08_08_singular_converged_gating_method
parent_node: A08_00_real_data_preserved_specialization_mainline
status: draft
canonical_language: en
---

# A08_08 Singular-Converged Gating Method Anchor

## 0. Thinking Card

**Phenomenon:** We need a gating mechanism that uses stable directions without letting CE feedback overwrite them.

**Mechanism guess:** gate rows should be tied to converged directions, while active updates suppress already-converged common subspace components.

**Key variables:** converged gate rows, residual reservoir, confidence gate, update suppression, route NMI, LM loss.

**Causal relation:** stable direction gate + anti-feedback update -> preserved initialization specialization.

**Observable metric:** synthetic `route_NMI@late` with loss guard.

**Alternative explanation:** preservation may come from freezing too much and harming learning.

**Decision:** test method on controlled synthetic before real-DCLM.

## 1. Problem Definition

**Decision question:** Does singular-converged gating preserve specialization under training on controlled data?

## 2. Physical Priors

**P1:** preservation requires controlling both forward route rows and update feedback.

## 3. Falsifiable Hypotheses

**H1:** method preserves route identity better than ordinary top-1.
**H2:** loss guard remains acceptable.

## 4. Mathematical Model

$$
g_i\propto v_i,\qquad \tilde u_t=r_t(I-\rho P_{\mathrm{stable}})u_t.
$$

## 5. Computational Realization

Synthetic nested and proxy-bridge tasks with ordinary, frozen-gate, direction-gate, and direction-gate-plus-update-control variants.

## 6. Minimal Falsification Test

**Primary metric:** route NMI after training.
**Pass:** method preserves NMI and loss.
**Fail:** preservation requires unacceptable loss regression.

## 7. Current Evidence

A07_02 supports update control; A06_12 shows ordinary training erases proxy routing.

## 8. Claim Boundary And Next Decision

**Can claim:** controlled method candidate.
**Cannot claim:** real-DCLM preservation.
**Next decision:** run real preservation in A08_09.
