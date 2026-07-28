---
anchor_id: 14_03_state_parameter_functional_rank_demand
line: 14_tree_low_rank_language_structure
status: candidate_for_human_review
canonical_language: en
companion: 14_03_state_parameter_functional_rank_demand_anchor_cn.md
thinking_card: 14_03_state_parameter_functional_rank_demand_thinking_card_cn.md
depends_on: 14_02_relation_reuse_root_effective_rank
protocol_status: not_created
---

# A14_03: Does Higher Task-State Functional Rank Require More Parameter Functional Directions?

Line foundation: [A14_00 conditional low-rank hierarchy](../14_00_tree_low_rank_language_structure/14_00_tree_low_rank_language_structure_anchor.md). Upstream decision: [A14_02 ROOT functional rank](../14_02_relation_reuse_root_effective_rank/14_02_relation_reuse_root_effective_rank_anchor.md).

## 1. Problem Definition

This candidate parent anchor asks one conditional question:

> After matching rule structure, exposure, output distribution, capability, and held-out utility, does a condition that requires higher task-state functional rank also causally require a larger functional subspace of a preregistered parameter operator?

The question is downstream of A14_02. It is not eligible for protocol promotion unless A14_02 first establishes a stable, task-sufficient state-rank contrast.

The objects are:

- **co-occurrence**: the training count of an exact relation or activation pattern;
- **task-state functional rank**: the minimum state-subspace dimension that preserves held-out utility within a registered tolerance;
- **parameter functional rank**: the minimum retained rank of a preregistered operator that preserves the same utility within a registered tolerance.

Low co-occurrence is a condition variable, not an assumed cause of high rank.

## 2. Physical Priors

1. Behaviorally necessary state directions must be controllable through some parameter-Jacobian or operator subspace, although that subspace need not be unique.
2. Exposure frequency changes estimation opportunity but does not determine algebraic rank.
3. A parameter direction counts as functionally necessary only when its removal degrades held-out task utility.

## 3. Falsifiable Hypotheses

### Primary hypothesis

Among capability-matched conditions with a preregistered state-rank contrast, the higher-state-rank condition will suffer a larger utility loss when the parameter operator is capped at the lower condition's minimal functional rank. Allowing the higher condition's own larger parameter rank will selectively rescue that loss.

### Strongest rival

Parameter rank reflects optimization redundancy, gauge freedom, function cardinality, or undertraining rather than necessary state capacity. State and parameter functional ranks can therefore remain causally decoupled.

### Verdicts

- **Pass**: the state-rank contrast is stable; the shared low-rank parameter cap selectively harms the higher-state-rank condition; and increasing the cap rescues it across registered seeds.
- **Fail**: a stable state-rank contrast exists, but the matched cap causes no selective harm or higher parameter rank gives no selective rescue.
- **Insufficient**: A14_02 does not establish the state contrast, capability fails, the registered operator is bypassed by compensation, or the effect is unstable.

## 4. Mathematical Model

For condition \(m\), define task-state functional rank

$$
k_H(m;\epsilon_H)
=
\min\left\{
k:
\mathcal L_H(m,k)-\mathcal L_{\mathrm{full}}(m)
\le \epsilon_H
\right\},
$$

where \(\mathcal L_H(m,k)\) is held-out loss after restricting the registered root state to a calibrated \(k\)-dimensional subspace.

For preregistered parameter operator \(B\), define

$$
k_B(m;\epsilon_B)
=
\min\left\{
k:
\mathcal L_B(m,k)-\mathcal L_{\mathrm{full}}(m)
\le \epsilon_B
\right\}.
$$

Let \(m_{\mathrm{lo}}\) and \(m_{\mathrm{hi}}\) be preregistered conditions with lower and higher state functional rank. Set

$$
k_{\mathrm{cap}}=k_B(m_{\mathrm{lo}};\epsilon_B).
$$

The proposed primary metric is the differential cap cost

$$
D_{\mathrm{cap}}
=
\left[
\mathcal L_B(m_{\mathrm{hi}},k_{\mathrm{cap}})
-\mathcal L_{\mathrm{full}}(m_{\mathrm{hi}})
\right]
-
\left[
\mathcal L_B(m_{\mathrm{lo}},k_{\mathrm{cap}})
-\mathcal L_{\mathrm{full}}(m_{\mathrm{lo}})
\right].
$$

A positive \(D_{\mathrm{cap}}\) is not sufficient alone. The higher-rank condition must also be selectively rescued by increasing the operator rank to its own calibrated requirement.

## 5. Computational Realization

The eventual protocol should inherit the matched conditions and checkpoints from A14_02. It should:

1. preregister the state intervention, parameter operator, tolerances, and conditions;
2. estimate state and parameter functional ranks only on calibration data;
3. evaluate cap cost and rescue on held-out data;
4. include random equal-rank subspaces and matched-capability controls;
5. report compensation diagnostics for unregistered layers or operators.

The first operator candidate is the combined QK scoring operator, not separate raw \(W_Q\) and \(W_K\) spectra. This choice remains a proposal until protocol review.

## 6. Minimal Falsification Tests

1. **Prerequisite test**: A14_02 must establish a held-out, task-sufficient state-rank contrast.
2. **Matched-cap test**: apply the lower condition's parameter rank cap to both conditions.
3. **Selective-rescue test**: increase only the allowed operator rank and test whether the higher-state-rank condition recovers.
4. **Random-subspace control**: distinguish functional directions from generic dimensionality.
5. **Undertraining control**: require matched capability before interpreting rank demand.

## 7. Current Evidence

A14_01/E08 provides only bounded composite evidence: shared conditions showed stronger parameter-space compression than state-space compression, while parameter-state rank correlation was weak and non-significant. This motivates a causal test but does not support the hypothesis.

A14_02 has not yet established the prerequisite state-rank contrast. A09 common/rare Router work studies a different question and is not evidence for state-to-parameter rank demand.

## 8. Claim Boundary And Next Decision

Even a positive result would apply only to the registered task, conditions, state intervention, and parameter operator. It would not establish that low co-occurrence universally causes high rank, that natural language is globally low-rank, or that an MoE Router is necessary.

**Exactly one next decision:** review A14_02 and its protocol first; promote A14_03 to a protocol only if A14_02 establishes a stable, task-sufficient state-rank contrast.
