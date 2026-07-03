---
anchor_id: A08_07_training_feedback_preservation_failure
parent_node: A08_00_real_data_preserved_specialization_mainline
status: draft
canonical_language: en
---

# A08_07 Training Feedback Preservation Failure Anchor

## 0. Thinking Card

**Phenomenon:** A06_12 shows step-0 proxy routing is erased by step 5/10.

**Mechanism guess:** early CE feedback amplifies common/gain directions and overwrites gate-forward identity.

**Key variables:** gate-weight update, hidden-state drift, expert-output feedback, common margin, proxy NMI.

**Causal relation:** early updates -> common/gain amplification -> route identity overwrite.

**Observable metric:** component-attributed drop in `proxy_route_NMI`.

**Alternative explanation:** proxy labels are unstable or the initialization is not useful.

**Decision:** choose anti-feedback method only after localizing the overwrite source.

## 1. Problem Definition

**Decision question:** Which early-training component erases real-DCLM proxy routing?

## 2. Physical Priors

**P1:** preservation failure is training feedback, not step-0 discovery failure.

## 3. Falsifiable Hypotheses

**H1:** freezing gate updates, hidden states, or expert feedback selectively preserves NMI.

## 4. Mathematical Model

$$
\Delta \operatorname{NMI}=\Delta_{\mathrm{gate}}+\Delta_{\mathrm{hidden}}+\Delta_{\mathrm{expert}}+\Delta_{\mathrm{optimizer}}.
$$

## 5. Computational Realization

Run A06_12-style real-DCLM training with component freezes and exact gate-input audits.

## 6. Minimal Falsification Test

**Primary metric:** `proxy_route_NMI@step5/10` under freeze ablations.
**Pass:** one component explains most preservation loss.
**Fail:** no component decomposition changes the collapse.

## 7. Current Evidence

A06_12 says collapse is not an LM-loss crash. A05 says common margin rapidly amplifies by step 10.

## 8. Claim Boundary And Next Decision

**Can claim:** source of preservation failure.
**Cannot claim:** method solution.
**Next decision:** design singular-converged gated training in A08_08.
