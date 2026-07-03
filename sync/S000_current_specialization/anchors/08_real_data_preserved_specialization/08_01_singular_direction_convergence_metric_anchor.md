---
anchor_id: A08_01_singular_direction_convergence_metric
parent_node: A08_00_real_data_preserved_specialization_mainline
status: supported_rank1_with_wide_boundary
canonical_language: en
---

# A08_01 Singular Direction Convergence Metric Anchor

## 0. Thinking Card

**Phenomenon:** The mentor and r1 say stable singular directions can define forward gating, but "converged" is not yet operational.

**Mechanism guess:** A direction is converged when projector drift is small while singular gain may still grow.

**Key variables:** $P_i(t)$, $\sigma_i(t)$, drift window $\Delta$, feature alignment, loss.

**Causal relation:** small direction drift + continuing gain -> forward role fixed but CE pressure still active.

**Observable metric:** convergence score $K_i(t)=\|P_i(t)-P_i(t-\Delta)\|_2$ with gain growth $\Delta\sigma_i>0$.

**Alternative explanation:** low drift may be numerical saturation or rank collapse, not meaningful feature convergence.

**Decision:** use this metric only if it separates stable direction from continuing gain on known synthetic features.

## 1. Problem Definition

**Decision question:** What operational threshold makes a singular direction safe to treat as a fixed gating-forward direction?

## 2. Physical Priors

**P1:** direction convergence and gain growth are separable.
**Could be wrong if:** drift and gain always move together.

## 3. Falsifiable Hypotheses

**H1:** known synthetic features show low $K_i(t)$ before gain stops growing.
**Weakened if:** no stable window exists.

## 4. Mathematical Model

$$
K_i(t)=\|P_i(t)-P_i(t-\Delta)\|_2,\qquad G_i(t)=\sigma_i(t)-\sigma_i(t-\Delta).
$$

**Falsifier:** $K_i$ cannot predict stable feature readout.

## 5. Computational Realization

Use A07 nested rank-one and a wider controlled synthetic model; compute $K_i$, $G_i$, and known-feature alignment.

## 6. Minimal Falsification Test

**Test:** synthetic convergence audit.
**Primary metric:** low $K_i$ with positive $G_i$.
**Pass:** stable direction window exists and matches known feature alignment.
**Fail:** convergence threshold is arbitrary or unrelated to feature readout.

## 7. Current Evidence

**Observation:** A08_01 full run `a08_singular_preservation_full_20260628_2`
supports the metric on the rank-one nested surface: pass rate `1.0000`, final
$K=0.0316$, final $G=0.0301$, A alignment `0.7865`, shuffled B alignment
`0.0218`.

**Interpretation:** direction convergence and gain growth are separable in the
controlled rank-one surface.

**Boundary:** wide robustness is insufficient: wide pass rate is `0.5000`.

**Evidence links:** `../../experiments/A08/A08_01_singular_direction_convergence_metric/summary.md`,
`../../experiments/A08/A08_01_singular_direction_convergence_metric/detailed.md`.

## 8. Claim Boundary And Next Decision

**Can claim:** a rank-one nested common direction can satisfy an operational
convergence metric.

**Cannot claim:** real-data convergence, wide-model robustness, or
preservation.

**Next decision:** use this metric only as a rank-local input to direction-gate
and real-DCLM convergence audits.
