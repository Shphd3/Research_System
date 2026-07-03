---
anchor_id: A08_09_real_dclm_preservation_method
parent_node: A08_00_real_data_preserved_specialization_mainline
status: draft
canonical_language: en
---

# A08_09 Real-DCLM Preservation Method Anchor

## 0. Thinking Card

**Phenomenon:** The final method must preserve real-DCLM initialization specialization through early training.

**Mechanism guess:** singular-converged gating plus anti-feedback control prevents proxy route overwrite.

**Key variables:** `proxy_route_NMI@step5/10`, LM loss, max load, common margin, update-subspace fraction.

**Causal relation:** anti-feedback method -> reduced overwrite -> preserved proxy route identity.

**Observable metric:** `proxy_route_NMI@step5/10`.

**Alternative explanation:** preservation may be caused by frozen/no-learning behavior or load collapse.

**Decision:** support only if NMI is preserved with acceptable LM loss and load.

## 1. Problem Definition

**Decision question:** Does the A08 method preserve real-DCLM proxy routing through step 5/10?

## 2. Physical Priors

**P1:** real preservation is possible if the overwrite mechanism is controlled.

## 3. Falsifiable Hypotheses

**H1:** method keeps `proxy_route_NMI@step5/10` above raw-center baseline.
**H2:** LM loss does not regress beyond tolerance.

## 4. Mathematical Model

Use A06_12 preservation metric with added update-space guard:
$$
\alpha_{\mathrm{stable}}=\|P_{\mathrm{stable}}u_t\|^2/(\|u_t\|^2+\epsilon).
$$

## 5. Computational Realization

Real-DCLM A06_12 runner plus A08 method variants on layers 3/4/5.

## 6. Minimal Falsification Test

**Primary metric:** `proxy_route_NMI@step5/10`.
**Pass:** preserved NMI with LM loss guard.
**Fail:** NMI collapses or loss regresses.

## 7. Current Evidence

A06_12 baseline fails: raw-center NMI drops from `0.7549` at step 0 to `0.0410` at step 5.

## 8. Claim Boundary And Next Decision

**Can claim:** real early-preservation method evidence.
**Cannot claim:** functional utility.
**Next decision:** apply A07 utility metrics in A08_10.
