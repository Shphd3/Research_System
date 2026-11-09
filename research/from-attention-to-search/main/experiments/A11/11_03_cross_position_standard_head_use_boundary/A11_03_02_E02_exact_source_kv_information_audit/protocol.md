# Protocol: A11_03_02_E02 Exact Source-K/V Information Audit

## 0. Approval Snapshot

**Approval status:** Approved by the researcher for remote four-GPU execution.  
**Purpose:** Determine whether informative MTP forms branch information in the exact layer-2 `U03` source K/V and whether that information is more linearly decodable than under matched shared-aux training.  
**Primary anchor:** [11_03_02 standard-head causal use](../../../../problem_anchors/11_informative_future_branch_mechanism/11_03_cross_position_standard_head_use_boundary/subanchors/11_03_02_standard_head_causal_use_anchor.md).  
**Anchor decision relation:** Complete the missing source-information guard for the prior negative K/V patch result and locate the failure before or after exact K/V formation.  
**Physical prior tested:** If the informative future target specifically strengthens branch representation in exact source K/V, a fixed-complexity held-out linear decoder should obtain lower branch cross-entropy under informative MTP than under shared aux.  
**Core model term:**

\[
\Gamma_{\mathrm{read},s}
=
\operatorname{CE}_{shared,s}
-
\operatorname{CE}_{info,s}.
\]

**Falsifier:** Informative-MTP K/V is absolutely readable, but \(\Gamma_{\mathrm{read}}\) is not stably positive across seeds.  
**Experiment role:** Root-cause audit, not method construction or a new causal-use test.  
**Primary metric:** Held-out probe cross-entropy improvement of informative MTP over shared aux, in nats per example.  
**Claim boundary:** Exact joint K/V at layer-2 `U03` in the controlled two-layer K=2 A11 task only.  
**Minimal setup:** Original data, model, objectives, five paired seeds, and matched-capability stopping rule.  
**Basic configuration:** 256 calibration nuisances (1,024 sequences), 1,024 confirmation nuisances (4,096 sequences), and \([K_{2,T};V_{2,T}]\in\mathbb R^{128}\).  
**Conditions:** NTP, shared aux, and informative MTP; the primary contrast is informative MTP versus shared aux.  
**Replay boundary:** The original run saved no checkpoints. The models must be reconstructed by a GPU same-contract replay using the original seeds, manifests, batch order, and stopping rule. Replay equivalence is a required guard and is not byte-identical checkpoint reuse.  
**Pass:** Source-formation and replay guards pass; at least 4/5 seeds have \(\Gamma_{\mathrm{read},s}>0\); and the paired hierarchical-bootstrap 95% interval for the five-seed mean lies above zero.  
**Fail:** Source-formation and replay guards pass; at least 4/5 seeds have \(\Gamma_{\mathrm{read},s}\le0\); and the mean interval lies at or below zero.  
**Insufficient:** Replay or formation guard failure, mixed seed directions, an interval crossing zero, or class coverage failure.  
**Cannot claim:** Standard-head use, zero use, arbitrary nonlinear information, general MTP superiority, benefit from shared unembedding, or natural-task transfer.  
**Approval decision:** Authorized for remote four-GPU execution. No local or CPU smoke is authorized.

## 1. Terminology And Definitions

| Term | Plain meaning | Concrete object / computation | Unit or formula | Decision role | Cannot prove |
|---|---|---|---|---|---|
| Exact source K/V | The attention memory actually patched in E01 | Layer-2 `U03` \([K_{2,T};V_{2,T}]\) | 128-vector | Source-formation object | Downstream use |
| Held-out readability | Whether a fixed linear decoder predicts branch on unseen nuisances | Fit on calibration, frozen on confirmation | accuracy and CE | Stable linear information | Arbitrary nonlinear information |
| Formation guard | Whether informative-MTP K/V is absolutely readable | nuisance-bootstrap lower bound on confirmation accuracy | probability; chance `0.25` | Allows post-formation localization | MTP specificity |
| \(\Gamma_{\mathrm{read}}\) | Informative-MTP gain over shared aux | \(\operatorname{CE}_{shared}-\operatorname{CE}_{info}\) | nat/example | Single primary metric | Standard-head use |
| Fisher separation | Between-branch dispersion relative to within-branch nuisance dispersion | \(\operatorname{tr}(S_B)/(\operatorname{tr}(S_W)+\epsilon)\) | dimensionless | Geometry diagnostic | Causal use |
| Same-contract replay | Reconstruct the original training state under the same executable contract | same seeds, manifests, batches, and stopping rule | Boolean guard | Validates reconstructed states | Bit identity |

## 2. Anchor Alignment

**Decision question:** Does informative MTP increase generalizable branch information in exact source K/V beyond matched shared aux?  
**Physical prior:** More source information under a fixed decoder implies lower held-out branch CE.  
**Core term:** \(\Gamma_{\mathrm{read}}\).  
**Falsifier:** Absolute K/V readability without a stable informative-MTP CE advantage.  
**Boundary:** This audit does not retest causal use.

## 3. Tested Hypothesis

The primary hypothesis is

\[
\Gamma_{\mathrm{read},s}>0
\]

in at least 4/5 paired seeds, with the paired hierarchical-bootstrap interval for the mean fully above zero.

## 4. Rival Explanations

1. **Late formation:** branch information enters final `U03` hidden state only during layer-2 attention/MLP, after layer-2 K/V has been formed.
2. **Generic-path formation:** NTP, shared aux, and informative MTP all form equally readable K/V through `BR_z`, layer 1, or residual paths.
3. **Replay mismatch:** reconstructed models do not recover the prior matched-capability and causal-patch state.
4. **Weak or redundant use:** remains a rival for E01, but this source-information audit cannot distinguish it.

## 5. Data, Model, Algorithm, And Objective

- Reuse `manifest_seed=20260715`, all original splits, and seeds `971–975`.
- Reuse the two-layer, width-64, one-head model and all three original objectives.
- The expected matched-capability steps are `500, 500, 900, 600, 700`.
- Replay and K/V extraction run on GPU.
- Fit a separate probe for every condition and seed.
- Confirmation is excluded from normalization, regularization, fitting, and stopping choices.

## 6. Conditions, Seeds, And Checkpoints

| Item | Clause / rival | Why needed | Evidence role | Pass | Fail / insufficient |
|---|---|---|---|---|---|
| Replay reproduction | Replay mismatch | Original checkpoints are absent | Required guard | Original step, capability, and E01 patch effect reproduced | Otherwise insufficient |
| Informative-MTP absolute probe | Late formation | Tests exact source formation | Formation guard | accuracy lower bound above `0.25` in at least 4/5 | Cannot localize after formation |
| Informative MTP vs shared aux | Specific enhancement | Controls auxiliary structure | Primary | stable positive \(\Gamma_{\mathrm{read}}\) | stable nonpositive is fail; mixed is insufficient |
| NTP | System baseline | Describes generic NTP path | Secondary | Descriptive only | Does not alter primary verdict |
| Label shuffle | Probe leakage | Guards analysis validity | Required guard | confirmation accuracy at most `0.30` | Otherwise insufficient |
| Four-class recall | Pair concentration | Prevents one-pair evidence | Formation guard | every recall above `0.25` in at least 4/5 informative seeds | Otherwise insufficient |
| Fisher and six pair distances | Geometry concentration | Describes seed/pair anisotropy | Secondary | Full distribution reported | Does not independently alter verdict |

## 7. Primary Metric

For each condition \(o\) and seed \(s\), use calibration features only to fit

\[
q_{o,s}(z\mid x)=\operatorname{softmax}(W_{o,s}x+b_{o,s}),
\]

with

\[
\min_{W,b}
-
\frac1{N_{cal}}\sum_i\log q_{o,s}(z_i\mid x_i)
+
\frac{\lambda}{2}\|W\|_F^2,
\qquad \lambda=10^{-3}.
\]

Calibration-only standardization is

\[
x_i
=
\frac{S_i-\mu_{cal}}{\max(\sigma_{cal},10^{-8})}.
\]

Freeze the probe and compute confirmation CE:

\[
\operatorname{CE}_{o,s}
=
-
\frac1{N_{conf}}\sum_i\log q_{o,s}(z_i\mid x_i).
\]

The single primary metric is

\[
\boxed{
\Gamma_{\mathrm{read},s}
=
\operatorname{CE}_{shared,s}
-
\operatorname{CE}_{info,s}
}.
\]

CE is used because accuracy may saturate at one while held-out class margins still differ.

## 8. Secondary Metrics

- confirmation macro accuracy and per-class recall;
- \(I_{\mathrm{lin},o,s}=\log4-\operatorname{CE}_{o,s}\);
- Fisher separation;
- all six unordered centroid distances;
- confusion matrices;
- descriptive NTP contrasts.

## 9. Known Good, Bad, And Confusing Cases

- Known good: the trained second head reads branch from final `U03` hidden state at accuracy `1.0`.
- Known bad: a calibration-label-shuffle probe should remain near `0.25` on confirmation.
- Known confusing: E01 seed 972 showed an almost entirely one-directional `3→1` switch effect.

## 10. Stage-Level Profiling Plan

| Stage | Local question | Pass | Failure meaning |
|---|---|---|---|
| Replay | Was the old model state recovered? | E01 steps and patch statistics reproduced | Insufficient |
| Extraction | Is exact layer-2 `U03` K/V read? | position, shape, and replay checks agree | Implementation failure |
| Absolute formation | Is informative-MTP K/V readable? | at least 4/5 above chance with all-class coverage | Cannot claim source formation |
| Specificity | Is it stronger than shared aux? | primary metric passes | Decides MTP-specific enhancement |
| Geometry | Is the result pair-stable? | report all pairs and seeds | Secondary localization |

## 11. Algorithm Specification

```text
replay:
  reconstruct all paired models on four remote GPUs
  verify selected steps, capabilities, and original E01 K/V patch effects

extract:
  collect k2[:, U03, :] and v2[:, U03, :]
  concatenate to [N, 128] for calibration and confirmation

fit:
  calibration-only standardization
  zero-initialized float64 linear softmax probe
  fixed L2 and optimizer convergence rule

evaluate:
  freeze probe
  confirmation CE, accuracy, recall, confusion
  Fisher separation and six centroid distances

uncertainty:
  cluster-bootstrap nuisance IDs while retaining all four branches
  use paired indices for shared aux and informative MTP
  resample paired seeds at the outer level
```

Required outputs:

```text
replay_guard.csv
probe_by_condition_seed.csv
probe_confusion.csv
fisher_by_condition_seed.csv
pairwise_centroid_distance.csv
probe_confirmation_by_nuisance.csv
bootstrap_gamma_read.csv
source_kv_information_audit.png
hypothesis_decision.json
run_manifest.json
```

## 12. Success, Failure, And Insufficient Evidence

**Pass:** All guards pass; informative absolute formation passes in at least 4/5 seeds with four-class coverage; \(\Gamma_{\mathrm{read}}>0\) in at least 4/5 seeds; and the mean interval lies above zero.

**Fail:** All replay and formation guards pass; \(\Gamma_{\mathrm{read}}\le0\) in at least 4/5 seeds; and the mean interval lies at or below zero.

**Insufficient:** Any other outcome.

## 13. What This Cannot Claim

Readability is not standard-head use. A near-chance linear probe does not prove absence of arbitrary nonlinear information. Greater separation cannot be attributed uniquely to attention. This test does not generalize to other layers, positions, horizons, tasks, or MTP architectures.

## 14. Review Notes And Protocol Changes

- The original E01 checkpoints were not saved, so this protocol uses a guarded same-contract replay.
- The researcher completed the comprehension audit and authorized remote four-GPU execution.
- No local or CPU smoke is authorized.
