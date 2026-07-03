---
anchor_id: A08_02_direction_as_gate_forward
parent_node: A08_00_real_data_preserved_specialization_mainline
status: supported_controlled_direction_gate
canonical_language: en
---

# A08_02 Direction As Gate-Forward Anchor

## 0. Thinking Card

**Phenomenon:** r1 suggests that once a singular direction is stable, its expert assignment can be treated as fixed.

**Mechanism guess:** a converged feature direction can initialize a gate row that routes examples using that direction.

**Key variables:** converged $v_i$, gate row $g_i$, route-label agreement, load, feature readout.

**Causal relation:** stable singular direction -> gate row alignment -> stable route-forward partition.

**Observable metric:** feature-route NMI from $g_i^\top h$.

**Alternative explanation:** routing may follow norm/frequency shortcuts, not the converged direction.

**Decision:** pursue if direction-derived gates beat random/load-only gates on known synthetic features.

## 1. Problem Definition

**Decision question:** Can a converged singular direction be converted into a useful gate-forward row?

## 2. Physical Priors

**P1:** a stable read/write direction is also a stable routing axis when exposed in gate input.

## 3. Falsifiable Hypotheses

**H1:** direction-gate rows recover known feature partitions.
**H2:** shuffled directions and norm-only gates fail.

## 4. Mathematical Model

$$
q(x)=\arg\max_e g_e^\top h(x),\qquad g_e\propto v_e.
$$

**Falsifier:** route NMI is no better than random or is explained by norm.

## 5. Computational Realization

Use A08_01 converged directions from controlled nested data; initialize gate rows; compare random, norm-matched random, direction gate, and oracle direction.

## 6. Minimal Falsification Test

**Primary metric:** feature-route NMI.
**Pass:** direction gate NMI beats random and norm controls.
**Fail:** no route identity despite direction convergence.

## 7. Current Evidence

**Observation:** A08_02 full run `a08_singular_preservation_full_20260628_2`
shows direction-gate feature NMI `1.0000`, oracle NMI `1.0000`, random
equal-norm mean NMI `0.1741`, shuffled direction NMI `0.0001`, and nuisance
NMI `0.0002`.

**Interpretation:** the converged rank-one direction can be converted into a
route identity on controlled data.

**Boundary:** one random-control seed reached NMI `0.5952`; future protocols
should use a random-control distribution.

**Evidence links:** `../../experiments/A08/A08_02_direction_as_gate_forward/summary.md`,
`../../experiments/A08/A08_02_direction_as_gate_forward/detailed.md`.

## 8. Claim Boundary And Next Decision

**Can claim:** direction-to-gate conversion works on the controlled rank-one
surface.

**Cannot claim:** route preservation, utility, or real-DCLM transfer.

**Next decision:** require training-preservation evidence before promoting this
to a method.
