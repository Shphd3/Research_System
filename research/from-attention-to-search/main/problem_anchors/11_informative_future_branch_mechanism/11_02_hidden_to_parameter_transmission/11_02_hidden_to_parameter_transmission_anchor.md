# Hidden-to-Parameter Transmission Anchor

Status: completed and conditionally supported in controlled Transformer settings.


## 1. Problem Definition

### Terminology / Definitions

| Term | Plain meaning | Concrete object | Why it matters | Cannot prove |
|---|---|---|---|---|
| hidden-to-parameter transmission | whether shared parameters can move the state along the useful direction | \(J^Tv\) | connects representation theory to training | natural-language benefit |
| parameter semantic velocity | first-order task-margin movement caused by a parameter update | \(-\langle\nabla_\theta M,\nabla_\theta L\rangle\) | primary metric | long-run convergence |
| direct path | earlier MTP loss from the decision state to the informative target | \(L_D\) | MTP-specific contribution | positive total update |
| background | all other losses acting on the same parameters | signed component velocities | exposes interference | one universal cause |

**Single decision question:** Does the direct hidden-state signal transmit through shared Transformer parameters once ordinary all-position losses are included?

## 2. Physical Priors

1. A useful hidden direction matters only if the encoder Jacobian has nonzero reachability along it.
2. All-position NTP already receives later supervision for the same answer; MTP adds an earlier path rather than exclusive information.
3. The net update is the signed sum of direct, later-semantic, local, and remaining background components.

## 3. Falsifiable Hypotheses

The direct component is positive at a shared checkpoint and predicts an actual small update. The full net component need not be positive in every seed because the background is signed.

The main falsifier is zero direct parameter velocity or failure of the finite-step update to follow the measured local velocity.

## 4. Mathematical Model

Let \(M\) be the task margin and partition the all-position loss as

\[
L^{all}=L_D+L_I+L_S+L_R.
\]

For each component,

\[
G_c=-\langle\nabla_\theta M,\nabla_\theta L_c\rangle,
\qquad
G_{total}=G_D+G_I+G_S+G_R.
\]

\(G_D\) measures the earlier MTP path; \(G_I\) measures the later standard NTP path.

## 5. Computational Realization

Use a one-layer causal Transformer with frozen embeddings and output heads, trainable shared encoder parameters, matched branch data, and a reference-folded decision state. First test decision-only transmission, then decompose every valid all-position loss at the same checkpoint.

## 6. Minimal Falsification Tests

1. Verify \(G_D>0\) and nonzero Jacobian reachability.
2. Compare predicted and observed one-step margin changes.
3. Partition the all-position update into \(G_D,G_I,G_S,G_R\) and report the net sign without hiding adverse seeds.

## 7. Current Evidence

Decision-only transmission is positive in 5/5 seeds and accurately predicts finite updates. Under all-position training, \(G_D\) is positive and exceeds \(G_I\) in 5/5 seeds, but remaining losses reverse the full net velocity in one seed. See [decision-only transmission](../../../experiments/A11/11_02_hidden_to_parameter_transmission/A11_02_01_E01_semantic_tangent_transmission/summary.md), [all-position decomposition](../../../experiments/A11/11_02_hidden_to_parameter_transmission/A11_02_01_E02_all_position_path_decomposition/summary.md), and [subanchor 11_02_01](subanchors/11_02_01_reachability_and_background_sign_anchor.md).

## 8. Claim Boundary And Next Decision

Supported claim: the earlier informative MTP path is reachable through shared parameters in the controlled model and is separable from NTP's later path. Background losses are signed, so direct benefit does not imply positive net training dynamics.

Not supported: natural-language efficiency, universal positive total gradients, or downstream use.

**Exactly one next decision:** test whether the formed direction remains useful after the state transition to the standard answer position.
