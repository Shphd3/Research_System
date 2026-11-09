# Protocol: A14_02_E04 Shared Jacobian / Path Image

Primary anchor:
[A14_02 shared compositional rules and task-functional ROOT rank](../../../../problem_anchors/14_tree_low_rank_language_structure/14_02_relation_reuse_root_effective_rank/14_02_relation_reuse_root_effective_rank_anchor.md)

## 0. Execution Snapshot

**Approval status:** Directly authorized by the user on 2026-07-25 for
autonomous implementation, smoke, confirmation, and the smallest
judgment-changing follow-up. No additional approval stop is required.

**Purpose:** Decide whether one learned task mapping in a one-layer,
one-head trainable causal-attention model has a context-shared ROOT
Jacobian/path image, or whether its task-parameter directions rotate into
many ROOT directions across held-out contexts.

**Anchor decision question:** Can the missing parameter-to-ROOT bridge in the
conditional-functional-rank theorem be observed in the minimal trainable
Transformer for which the theorem is intended?

**Physical prior tested:** Reusing one learned mapping across independent
nuisance contexts should reuse a small ROOT path-image space.

**Core model term tested:** Theory H9,

\[
J_\rho(x)G_m=B_mA_x+E_x,
\qquad
\dim\operatorname{Col}(B_m)\le q.
\]

**Strongest rival:** A capable model can implement the same input-output
mapping while context-dependent attention, residual, or normalization
rotates the task update into many ROOT directions. Low fixed-readout rank may
then coexist with failure of raw ROOT H9.

**Experiment role:** Direct proxy/operationalization test of H9, with an
embedded root-cause audit if raw H9 fails.

**Primary metric:**

\[
\tau_J^2(q)
=
\frac{\sum_{i>q}\lambda_i(C_{\mathrm{test}})}
{\sum_i\lambda_i(C_{\mathrm{test}})},
\qquad
C_{\mathrm{test}}
=
\frac1{ng}
\sum_{x\in D_{\mathrm{test}}}
[J_\rho(x)G_m][J_\rho(x)G_m]^\top.
\]

Here \(g=q=8\). \(G_m\) is fit on calibration examples only.

**Primary transfer guard:** Let \(\widehat B_{\mathrm{cal}}\) be the top-\(q\)
eigenspace of calibration Jacobian covariance. Report

\[
R_{\mathrm{cal}\to\mathrm{test}}
=
\frac{\sum_x
\|\widehat B_{\mathrm{cal}}\widehat B_{\mathrm{cal}}^\top
J_\rho(x)G_m\|_F^2}
{\sum_x\|J_\rho(x)G_m\|_F^2}.
\]

**Minimal setup:** One pre-norm causal Transformer block, one attention head,
width 64, explicit `ROOT` token, frozen trained output head during all
Jacobian and projection measurements, full-position NTP training.

**Support H9 in the registered model:** Capability and numerical guards pass;
at least 4/5 confirmation seeds have

\[
\tau_J^2(8)\le0.10,
\qquad
R_{\mathrm{cal}\to\mathrm{test}}\ge0.85,
\]

and the aggregate paired confidence interval excludes the refutation region.

**Refute H9 in the registered model:** Capability and numerical guards pass;
at least 4/5 seeds have either

\[
\tau_J^2(8)\ge0.25
\]

or

\[
R_{\mathrm{cal}\to\mathrm{test}}\le0.70.
\]

**Insufficient:** Fewer than four capability-passing seeds; top-eight task
gradient energy below 0.80; finite-difference Jacobian relative disagreement
above 0.05; known-good or known-bad metric controls fail; or the result lies
strictly between the support and refutation regions.

**Cannot claim:** A general Transformer theorem, natural-language H9, global
hidden-state low rank, full-parameter low rank, or Router utility.

## 1. Terminology / Definitions

| Term | Plain meaning | Computation | Decision role | Cannot prove |
|---|---|---|---|---|
| learned common mapping | One answer function reused by every surface alias | A fixed permutation \(\pi\) with held-out alias--entity recombination accuracy | Ensures the mapping is behaviorally available outside seen pairs | A unique internal algorithm |
| nuisance context | A token that does not change the answer | Context id varies while \(Y=\pi(a)\) is fixed | Tests cross-context stability | Natural-language context independence |
| task parameter subspace \(G_m\) | Calibration-estimated directions that change the task loss | Top 8 right singular vectors of per-example answer-loss gradients for the single Transformer block | Defines the parameter directions whose ROOT image is tested | The unique training trajectory |
| Jacobian path image | ROOT changes induced by task parameter directions | \(Z_x=J_\rho(x)G_m\) | Direct H9 object | Long-distance nonlinear movement |
| Jacobian tail \(\tau_J^2(8)\) | Energy outside the best joint eight-dimensional ROOT image | Spectral tail of held-out \(C_{\mathrm{test}}\) | Primary decision metric | Task utility by itself |
| calibration-to-test capture | Held-out Jacobian energy captured by the calibration image | \(R_{\mathrm{cal}\to\mathrm{test}}\) | Prevents test-fit low rank | Natural-language transfer |
| fixed-readout rank | ROOT directions preserving the already-trained answer head | Calibration projection, frozen head, test CE/accuracy | Functional consequence of the bridge | Raw ROOT geometry |

## 2. Data, Model, And Objective

The registered sequence is

```text
ALIAS_r ENTITY_a CONTEXT_c ROOT ANSWER_pi(a)
```

with 16 aliases, 8 entities, and 32 context ids. The same non-identity
permutation \(\pi\) is used for every alias. Two of eight alias--entity cells
per alias are excluded from training by a deterministic balanced pattern.
Every alias and every entity remains well represented in training. Context
assignments are relation-specific: train, calibration, and test contexts are
disjoint for each relation, while every context token appears elsewhere in
training so that the test does not use untrained embeddings.

The model is trained with full-position next-token cross-entropy. Checkpoint
selection uses calibration capability only and never reads test Jacobians,
test functional rank, or test projection effects.

## 3. Capability And Validity Gates

All confirmation seeds must report:

- seen-pair test accuracy at least 0.98;
- held-out alias--entity calibration accuracy at least 0.95;
- held-out alias--entity final-test accuracy at least 0.95;
- held-out nuisance consistency at least 0.98;
- full-state replay absolute CE error at most \(10^{-6}\);
- top-eight calibration gradient energy at least 0.80;
- central finite-difference agreement at \(\epsilon\) and \(\epsilon/2\) at most
  0.05 relative error.

A seed failing capability is ineligible rather than assigned zero rank.

## 4. Conditions And Controls

| Item | Rival separated | Evidence | Required behavior |
|---|---|---|---|
| trained task-gradient \(G_m\) | H9 target | Primary \(\tau_J^2\), transfer capture | Support or refutation thresholds above |
| initialization checkpoint | Architecture-only sharing | Same metrics before training | Descriptive; determines whether sharing was learned or pre-existing |
| equal-dimensional random \(G\) | Any parameter subspace looks shared | Paired tail and capture | Task result must be interpreted as task-specific only if it improves on random |
| constructed fixed-image control | Metric cannot recover exact H9 | Known-good spectrum | Tail \(\le10^{-6}\) and capture \(\ge0.999\) |
| context-rotated image control | Metric is insensitive to rotation | Known-bad spectrum | Tail \(\ge0.25\) or capture \(\le0.70\) |
| output-visible / head-null decomposition | Raw H9 is stronger than required for function | Tail energy in the two components | Distinguishes functional bridge failure from output-invisible gauge variation |
| frozen-head ROOT projection | Low Jacobian tail has no task consequence | Test excess CE and accuracy | Secondary H10/T7 check |

## 5. Jacobian Algorithm

1. Select the first checkpoint with three consecutive calibration capability
   passes.
2. On a balanced calibration subset, compute per-example answer CE gradients
   with respect to the first block's `q/k/v/out` and MLP weights.
3. Form the uncentered gradient matrix and obtain its top eight right singular
   directions without using test examples.
4. For each direction, compute post-final-normalization ROOT central
   finite differences at \(\epsilon=5\times10^{-3}\) and \(\epsilon/2\).
5. Build calibration and held-out covariance matrices, spectral tails, and
   calibration-to-test capture.
6. Repeat the same measurement for initialization and a seeded Haar-random
   parameter subspace.
7. Run the fixed-image and context-rotated metric controls.
8. Decompose ROOT Jacobian vectors into the row space of the frozen
   answer-logit contrast head and its orthogonal complement.
9. Fit the ROOT image on calibration only, project final-test ROOT states,
   freeze the output head, and report excess answer CE and accuracy drop.

## 6. Seeds, Development, And Follow-Up Rule

- Development seed: 100. It may diagnose implementation, capability, and
  numerical issues but never contributes to the verdict.
- Confirmation seeds: 0, 1, 2, 3, 4.
- Thresholds above are frozen before confirmation.
- A follow-up is allowed without additional approval only when the first
  confirmation result is insufficient. It must distinguish exactly one of:
  capability failure, Jacobian numerical failure, task-subspace proxy failure,
  or raw-versus-output-visible H9 mismatch.
- A follow-up may not weaken the original support/refutation thresholds or
  reuse the original final-test examples for tuning. It receives a new
  experiment id and fresh confirmation seeds.

## 7. Required Artifacts

The execution workspace must retain configuration, manifest, per-seed
capability, gradient spectrum, Jacobian spectra, controls, fixed-readout
curves, checkpoints, and raw logs. The curated project record retains:

- `summary.md`;
- `detailed.md`;
- `tables/seed_summary.csv`;
- the minimum central figures for Jacobian tail/capture and
  output-visible/null decomposition.

## 8. Frozen Pre-Confirmation Numerical Repair

Development seed 100 passed capability and both constructed metric controls,
but float32 probing at \(\epsilon=10^{-2}\) was numerically unstable for
low-energy random directions. Re-evaluating the same frozen checkpoint in
float64 removed that failure. A development-only step-size convergence audit
then measured relative disagreements of 0.1070, 0.0316, 0.0083, and 0.0021 for
the pairs \((10^{-2},5\times10^{-3})\) through
\((1.25\times10^{-3},6.25\times10^{-4})\). The registered confirmation
measurement therefore uses float64 and the first pair below the frozen 0.05
guard: \(\epsilon=5\times10^{-3}\) versus \(\epsilon/2\). No confirmation seed,
decision threshold, data split, model, or primary metric was inspected or
changed.
