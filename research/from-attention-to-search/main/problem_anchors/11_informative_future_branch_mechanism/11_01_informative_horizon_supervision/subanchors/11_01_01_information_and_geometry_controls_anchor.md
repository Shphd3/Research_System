# Information Inclusion And Output-Geometry Controls


## 1. Problem Definition

**Parent problem:** [11_01 informative-horizon supervision](../11_01_informative_horizon_supervision_anchor.md).
**Sharper subproblem:** distinguish information-bearing supervision from mere horizon extension.
**Decision question:** Do information inclusion and output geometry explain the direct current-state increment better than horizon length alone?
**Not in scope:** parameter transmission or later standard-head use.

An **informative position** is a future token whose identity still depends on the branch variable after earlier tokens are known. **Hidden semantic velocity** is the one-step movement of the decision state along the branch-correct centered output direction; it decides this local question but cannot prove behavioral benefit.

## 2. Physical Priors

**P1:** A branch-shared label cannot distinguish branches. It could be wrong if it produces a nonzero branch-specific update under matched prefixes.
**P2:** Two informative labels combine as vectors. It could be wrong if alignment interventions fail to predict the signed increment.

## 3. Falsifiable Hypotheses

**H1:** An uninformative added target produces zero direct increment.
**H2:** Aligned informative directions increase the signal; conflicting directions reduce it.

## 4. Mathematical Model

For the covered informative set \(\mathcal I_K\),

\[
v_z^{(K)}=\sum_{j\in\mathcal I_K}\lambda_j(u_{j,z}-\bar u_j).
\]

The falsifier is a signal that follows \(K\) while ignoring changes in \(\mathcal I_K\) or direction alignment.

## 5. Computational Realization

Use matched prefixes and fixed readouts; add either a shared label, an aligned informative label, or a conflicting informative label; record the decision-state update.

## 6. Minimal Falsification Tests

1. Add a shared target and require no direct semantic increment.
2. Add aligned versus conflicting informative targets and require the predicted sign ordering.

## 7. Current Evidence

Both controls pass in the decisive [next-\(K\) inclusion experiment](../../../../experiments/A11/11_01_informative_horizon_supervision/A11_01_01_E01_next_k_inclusion_law/summary.md). Earlier horizon and leakage checks are archived because they do not change this conclusion.

## 8. Claim Boundary And Next Decision

**Can claim:** direct signal is governed by information inclusion and output geometry, not horizon length alone.
**Cannot claim:** shared-parameter or downstream benefit.
**Next decision:** use this result as the fixed premise of parent anchor 11_02; do not reopen the archived horizon variants unless the premise is contradicted.
