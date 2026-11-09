# Informative-Horizon Supervision Anchor

Status: completed and supported in the controlled hidden-state setting.


## 1. Problem Definition

### Terminology / Definitions

| Term | Plain meaning | Concrete object | Why it matters | Cannot prove |
|---|---|---|---|---|
| informative future position | a future target whose identity depends on the task variable after matching the local context | a target \(Y_{t+j}\) with branch-dependent label | identifies where extra supervision begins | downstream usefulness |
| centered output direction | the correct output row after removing the branch-common component | \(u_{j,z}-\bar u_j\) | separates semantic movement from common-token movement | final accuracy |
| hidden semantic velocity | first-order movement of \(h_T\) along the aggregate task direction | \(G_{hidden}\) | primary metric | parameter-space transmission |

**Single decision question:** When does a next-\(K\) objective add a direct task-relevant update to the current hidden state?

## 2. Physical Priors

1. A branch-shared future target cannot directly distinguish the task variable.
2. A branch-dependent target can do so only through its output-readout geometry.
3. Several informative targets may reinforce or cancel one another.

## 3. Falsifiable Hypotheses

The direct signal is zero before the first informative future position, turns on when that position is included, remains unchanged when only an uninformative position is added, and changes according to direction alignment when another informative position is added.

The main falsifier is a nonzero semantic velocity before any informative target is covered, or a horizon increment that is unrelated to the predicted output-direction increment.

## 4. Mathematical Model

For task variable \(Z=z\), define the informative positions covered by horizon \(K\) as

\[
\mathcal I_K=\{j\le K:Y_{t+j}\text{ depends on }Z\}.
\]

The aggregate task direction is

\[
v_z^{(K)}=\sum_{j\in\mathcal I_K}\lambda_j(u_{j,z}-\bar u_j).
\]

The direct hidden-state effect is determined by this vector sum, not by \(K\) alone.

## 5. Computational Realization

Use controlled branches with matched prefixes, fixed output heads, and future positions that are either branch-shared or one-to-one encodings of \(Z\). Compare horizons immediately before and after an informative position, then add an aligned or conflicting informative target.

## 6. Minimal Falsification Tests

1. Compare hidden semantic velocity before and at the first informative position.
2. Add a branch-shared target and test for zero direct increment.
3. Add aligned and conflicting informative targets and compare the signed increment.

Supported means all three patterns hold across confirmation seeds. Weakened means horizon length predicts the result better than information inclusion and direction alignment.

## 7. Current Evidence

The controlled next-\(K\) experiment supports the inclusion law: velocity is zero before the informative horizon, becomes positive when it is covered, receives no one-step increment from a shared target, increases under aligned geometry, and decreases under conflicting geometry. The decisive source is the [next-\(K\) inclusion summary](../../../experiments/A11/11_01_informative_horizon_supervision/A11_01_01_E01_next_k_inclusion_law/summary.md). The supporting controls are compressed in [subanchor 11_01_01](subanchors/11_01_01_information_and_geometry_controls_anchor.md).

## 8. Claim Boundary And Next Decision

Supported claim: informative future targets give the current hidden state a direct first-order task signal, and multiple targets combine through output-direction geometry.

Not supported: larger \(K\) is generally better, the signal reaches model parameters, or the standard next-token head uses it.

**Exactly one next decision:** determine whether this hidden-state signal is reachable through shared model parameters.
