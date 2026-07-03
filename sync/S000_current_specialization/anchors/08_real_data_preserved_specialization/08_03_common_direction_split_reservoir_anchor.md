---
anchor_id: A08_03_common_direction_split_reservoir
parent_node: A08_00_real_data_preserved_specialization_mainline
status: weakened_by_capacity_guard
canonical_language: en
---

# A08_03 Common Direction Split Reservoir Anchor

## 0. Thinking Card

**Phenomenon:** r1 proposes sending the converged common projection to a common expert and the residual to a long-tail reservoir expert.

**Mechanism guess:** removing the converged common component from the tail path prevents common gain from dominating child-direction learning.

**Key variables:** $P_C h$, $(I-P_C)h$, common expert, reservoir expert, tail loss, common retention.

**Causal relation:** converged $P_C$ -> split forward path -> reservoir learns non-common child direction.

**Observable metric:** tail loss improvement with common loss preserved.

**Alternative explanation:** split helps by capacity increase or regularization, not by removing common direction.

**Decision:** pursue if residual reservoir improves tail loss and reduces tail update fraction in $P_C$.

## 1. Problem Definition

**Decision question:** Does common/residual forward splitting protect tail learning on nested synthetic data?

## 2. Physical Priors

**P1:** once common direction is converged, tail examples should not keep using it for child-specific updates.

## 3. Falsifiable Hypotheses

**H1:** reservoir split lowers tail loss.
**H2:** common expert preserves $A$.
**H3:** norm/capacity matched split does not explain the effect.

## 4. Mathematical Model

$$
h_C=P_Ch,\qquad h_R=(I-P_C)h.
$$

**Falsifier:** tail loss improves without reducing $\alpha_{\mathrm{tail}}$, or common loss regresses.

## 5. Computational Realization

Extend A07_02 nested script with a split-forward MoE: common expert receives $h_C$, reservoir receives $h_R$.

## 6. Minimal Falsification Test

**Primary metric:** tail loss improvement over CE baseline.
**Guard:** common loss and $\alpha_{\mathrm{tail}}$.
**Pass:** tail loss improves, common preserved, alpha decreases.
**Fail:** split only changes capacity or hurts common.

## 7. Current Evidence

**Observation:** A08_03 full run `a08_singular_preservation_full_20260628_2`
shows common/residual split improves tail loss by `0.0984` and reduces
$\alpha_{\mathrm{tail}}$ by `0.1558`.

**Observation:** the capacity-matched random split improves tail loss by
`0.1596`, more than the proposed split.

**Interpretation:** the split intervention is active, but the proposed
common/residual mechanism is not identified.

**Boundary:** do not treat tail improvement as mechanism evidence.

**Evidence links:** `../../experiments/A08/A08_03_common_direction_split_reservoir/summary.md`,
`../../experiments/A08/A08_03_common_direction_split_reservoir/detailed.md`.

## 8. Claim Boundary And Next Decision

**Can claim:** split-forward changes tail loss and common-subspace tail update
fraction on controlled data.

**Cannot claim:** common/residual split caused the tail gain or is ready for
real-DCLM preservation.

**Next decision:** revise or park the split method until it beats a
capacity-matched random split.
