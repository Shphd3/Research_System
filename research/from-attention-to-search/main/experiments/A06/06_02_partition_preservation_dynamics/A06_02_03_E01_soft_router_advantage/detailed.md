# Detailed: A06_02_03_E01 Soft-Router Advantage-To-Margin Dynamics

Primary anchor: `../../../../problem_anchors/06_geometry_proxy_preservation/06_02_partition_preservation_dynamics/06_02_partition_preservation_dynamics_anchor.md`

Protocol: `protocol.md`  
Summary: `summary.md`

## 0. Quick Recap

**Purpose:** Isolate whether expert utility supplies local feature-margin growth.

**Hypothesis:** Matched utility gives positive matched-margin pressure; identical utility removes it; permuted utility redirects it.

**Conclusion:** Supported across all 32 seeds and both local learning rates.

**Evidence:** Positive-sign rate 1.000 under matched utility, zero update under identical experts, and geometry/utility sign separation under permutation.

## 1. Terminology / Definitions

Definitions follow the summary and protocol. The analytical/autograd equality is expected from the chain rule under frozen hidden states and plain SGD. It is not promoted as independent research evidence.

## 2. Protocol Compliance

| Requirement | Planned | Completed |
| --- | --- | --- |
| Seeds | 32 | 32, seeds 0-31 |
| Utility conditions | matched / identical / permuted | all complete |
| Learning rates | 0.01 / 0.05 | both complete |
| Frozen hidden and experts | required | enforced |
| Router optimizer | one-step SGD | enforced |
| Formula guard | numerical closure | maximum error \(2.61\times10^{-18}\) |

No post-hoc condition or threshold was added.

## 3. Data And Model

For each seed, QR decomposition creates four orthogonal feature centers \(\mu_f\in\mathbb R^{16}\). Each feature has 256 states:

\[
h=\mu_f+0.05\epsilon.
\]

The router begins at \(w_f=0.75\mu_f\). Fixed expert outputs are four-dimensional class-logit vectors with strength 4.0. Cross-entropy is applied to the soft mixture output.

## 4. Mathematical Audit

For

\[
\hat y=\sum_e p_eE_e,
\]

router-only SGD obeys

\[
\Delta w_e=\frac{\eta}{\tau}\mathbb E[p_eA_eh].
\]

This equality was checked against autograd. The experiment's falsifiable intervention changes \(E_e\) while holding \(h\), \(W\), labels, and optimization fixed.

## 5. Full Results

At learning rate 0.05:

- matched utility: mean geometry-margin change `+0.011953`, minimum `+0.011832`;
- identical experts: update norm and margin change exactly `0`;
- permuted utility: mean geometry-margin change `-0.009529`, while utility-aligned change is `+0.016093`;
- mean utility-redirection gap under permutation: `+0.025622`.

The same sign pattern holds at learning rate 0.01, so the result is not an oversized-step artifact.

## 6. Visualization Results

### Utility Intervention And Margin Direction

![Utility intervention and margin direction](figures/utility_intervention_margin_change.png)

**Purpose:** Separate route geometry from expert function.

**Data source:** `tables/condition_summary.csv`, 32 seeds and four features per seed.

**Aggregation:** Mean one-step geometry-matched margin change.

**Allowed conclusion:** Local margin pressure follows controlled expert utility.

**Limitation:** The figure does not show sparse selection or multi-step dynamics.

Rendered-artifact audit: axes, zero line, condition labels, and learning rates are readable; the figure does not require source-code knowledge.

## 7. Failure Decomposition

- **Chain-rule tautology:** handled by treating formula closure only as a guard.
- **Norm-only growth:** rejected because permuted utility changes the sign of matched margin despite comparable nonzero update norm.
- **Geometry/function conflation:** rejected by the positive utility-aligned and negative geometry-aligned increments under permutation.

## 8. Interpretation

The correct local mechanism variable is not feature-center alignment alone. It is feature-conditioned relative expert utility. A clean center initialization without matched utility has no reason to be reinforced and can be actively redirected.

This result does not establish that trained experts naturally acquire the required utility. It establishes only the direction of causality once fixed utility is supplied.

## 9. Claim Boundary And Next Decision

Supported: utility interventions control local soft-router margin direction.

Not supported: top-1 counterfactual correction, hidden drift, background accumulation, or semantic expert specialization.

Next decision: A06_02_03_E02 tests whether the useful but unselected expert receives direct utility information.

## 10. Artifact Map

- Runner: `../../../../XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/scripts/run_a06_31_33_router_dynamics.py`
- Config: `../../../../XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/configs/a06_31_soft_router_advantage_margin_dynamics.json`
- Run name: `a06_31_33_full_20260710_001757`
- Raw result: `../../../../XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/results/a06_31_33_router_dynamics/a06_31_33_full_20260710_001757/A06_02_03_E01/`
- Main tables: `tables/cell_results.csv`, `tables/condition_summary.csv`
- Figure: `figures/utility_intervention_margin_change.png`
- Hardware: two local NVIDIA H100 80GB GPUs, seeds split 0-15 and 16-31.
