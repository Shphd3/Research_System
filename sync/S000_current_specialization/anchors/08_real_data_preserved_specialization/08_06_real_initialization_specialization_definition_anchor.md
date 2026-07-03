---
anchor_id: A08_06_real_initialization_specialization_definition
parent_node: A08_00_real_data_preserved_specialization_mainline
status: draft
canonical_language: en
---

# A08_06 Real Initialization Specialization Definition Anchor

## 0. Thinking Card

**Phenomenon:** Current "specialization" is underdefined for real data.

**Mechanism guess:** real initialization specialization should mean a stable direction-derived route identity, not semantic naming.

**Key variables:** direction stability, proxy-route NMI, gate row alignment, load, nuisance guards.

**Causal relation:** converged direction + gate row alignment -> step-0 route identity.

**Observable metric:** `init_specialization_score`.

**Alternative explanation:** high NMI may come from frequency, position, or common load.

**Decision:** use the definition only if it separates proxy identity from load/nuisance.

## 1. Problem Definition

**Decision question:** What is a valid real-data definition of initialization specialization?

## 2. Physical Priors

**P1:** before utility, specialization means stable route identity with nuisance guards.

## 3. Falsifiable Hypotheses

**H1:** direction-derived/proxy gates beat random on route identity while guards stay low.

## 4. Mathematical Model

$$
S_{\mathrm{init}}=\operatorname{NMI}(\text{route},\text{proxy})-\max(\operatorname{NMI}_{\mathrm{freq}},\operatorname{NMI}_{\mathrm{pos}}).
$$

## 5. Computational Realization

Apply to A06_11 raw-center and future direction-gate initializers.

## 6. Minimal Falsification Test

**Primary metric:** `init_specialization_score`.
**Pass:** proxy NMI high and nuisance NMI low.
**Fail:** score explained by frequency/position/load.

## 7. Current Evidence

A06_11 raw-center gate has high proxy-route NMI and low frequency/position NMI at step 0.

## 8. Claim Boundary And Next Decision

**Can claim:** initialization specialization is operationally defined.
**Cannot claim:** preservation or utility.
**Next decision:** diagnose why initialization is erased in A08_07.
