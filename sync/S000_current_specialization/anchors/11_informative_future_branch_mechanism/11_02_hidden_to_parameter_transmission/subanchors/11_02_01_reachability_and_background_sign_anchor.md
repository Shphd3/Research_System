# Shared-Parameter Reachability And Background-Sign Control

Thinking Card source: [11_02_01_reachability_and_background_sign_thinking_card.md](11_02_01_reachability_and_background_sign_thinking_card.md)

## 1. Problem Definition

**Parent problem:** [11_02 hidden-to-parameter transmission](../11_02_hidden_to_parameter_transmission_anchor.md).
**Decision question:** Does the direct MTP path reach shared parameters, and can background losses reverse its net sign?
**Not in scope:** long-run convergence or real-task gain.

**Parameter semantic velocity** is the predicted first-order change in the task margin after a parameter update. It answers whether a local gradient can be realized, but not whether repeated training remains beneficial.

## 2. Physical Priors

**P1:** Nonzero hidden-state direction is insufficient without Jacobian reachability.
**P2:** All-position losses are signed contributors, not neutral background.

## 3. Falsifiable Hypotheses

**H1:** The direct MTP component has positive velocity and predicts a finite small update.
**H2:** The total velocity can differ in sign because remaining losses can cancel the direct component.

## 4. Mathematical Model

$$
G_c=-\langle\nabla_\theta M,\nabla_\theta L_c\rangle,
\qquad
G_{total}=G_D+G_I+G_S+G_R.
$$

$G_D$ is the earlier MTP path; $G_I$ is the later ordinary NTP path. Zero $G_D$ or a failed finite-step prediction falsifies reachability.

## 5. Computational Realization

At one shared checkpoint, compute component gradients, their predicted margin motion, and the observed small-step change without changing the data or model.

## 6. Minimal Falsification Tests

1. Require positive direct-path reachability and finite-step agreement.
2. Report the sign of every all-position component and the total without averaging away adverse seeds.

## 7. Current Evidence

The [transmission experiment](/Projects/from-attention-to-search/main/experiments/A11/11_02_hidden_to_parameter_transmission/A11_02_01_E01_semantic_tangent_transmission/summary.md) supports H1 in 5/5 seeds. The [all-position decomposition](/Projects/from-attention-to-search/main/experiments/A11/11_02_hidden_to_parameter_transmission/A11_02_01_E02_all_position_path_decomposition/summary.md) shows positive direct contribution but one net-sign reversal.

## 8. Claim Boundary And Next Decision

**Can claim:** the direct path is reachable under the controlled model; background terms are signed.
**Cannot claim:** a universal positive total MTP update.
**Next decision:** test whether the reached direction survives to the actual standard-head answer position.
