---
experiment_id: A15_06_E02_local_random_identity_control
legacy_experiment_id: A15_00_E02_local_random_identity_control
anchor_id: A15_06_01_local_random_identity_control
status: approved_for_implementation_smoke_and_full
approved_by: user
approval_date: 2026-08-04
resource_profile: 5090-8-spot
primary_metric: paired_10b_nll_local_hmt_minus_local_random_matched
---

# Protocol: A15_06_E02 Local Random Identity Control

## 0. Approval Snapshot

Document status: executable canonical contract.  Approval status: user approved
direct construction, smoke, two full submissions, terminal monitoring, and
comparison.  Block audit: confirmed.  Cross-block consistency: pass.

Purpose: decide whether the weak Local-HMT signal is specific to covariance
rank or is reproduced by an arbitrary motion-matched dynamic local partition.
Primary anchor: [A15_06_01](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_06_online_spectral_routing_and_relay/subanchors/15_06_01_local_random_identity_control_anchor.md).
Experiment role: causal identity control.  Primary metric: paired 10B held-out
NLL, Local-HMT minus Local-Random-Matched, per seed.  Conditions: only the two
missing Local-Random-Matched jobs, seeds 17 and 29; completed Local-HMT and
Centered-Full are immutable controls.

Pass: Local-HMT has lower 10B NLL in both seeds, both paired-document 95% CIs
are below zero, and tracking comparability passes.  Fail: random matches/beats
HMT, a seed reverses, or either paired CI includes zero.  Insufficient: pairing,
motion isometry, tracking comparability, resume, or terminal evidence fails.
Cannot claim: universal spectral semantics, scale generality, or a unique
expert-specialization mediator.

## 1. Terminology / Definitions

| Term | Plain meaning | Computation | Unit | Decision role | Cannot prove |
| --- | --- | --- | --- | --- | --- |
| Local-HMT | each later Gate reads a covariance-ranked band of its own layer | block 2/3/4 use ranks 1--64, 65--320, 321--768 | subspace | treatment | semantic hierarchy |
| Local-Random-Matched | same local sources and dimensions after fixed ambient random rotation | \((OU_{64},OU_{320})\) | subspace | decisive control | usefulness by itself |
| target motion | how far the desired subspace moves between refreshes | principal angles between successive targets | radians | control validity | deployed tracking |
| tracking overlap | closeness of deployed and target subspaces | mean squared canonical cosine | [0,1] | confound guard | NLL benefit |
| terminal NLL | held-out next-token surprise at 10B | mean negative log probability | nat/token | primary outcome | mechanism alone |

## 2. Anchor Alignment

The experiment tests the parent anchor's only unresolved Local clause.  It
separates covariance-rank identity from generic smooth dynamic restriction.

## 3. Tested Hypothesis

Covariance-ranked local H/M/T gives lower terminal NLL than an equal-dimension
random local partition whose target motion and updater are matched.

## 4. Rival Explanations

1. Any centered smooth dynamic bottleneck explains the Local-HMT signal.
2. The random control loses only because its target moves farther.
3. The random control loses only because the continuity guard tracks it worse.
4. Apparent differences come from initialization, data order, load, compute, or
   endpoint evaluation mismatch.

## 5. Data Construction And Provenance

Reuse the E01 immutable DCLM train stream and frozen evaluation artifact.  The
statistics, guard, and 1,024 validation documents are disjoint and retain the
same token order and SHA-256.  No document or threshold is selected from E02
outcomes.

## 6. Learning Task And Permitted Supervision

Both arms optimize ordinary next-token likelihood plus the same load-balancing
term.  Covariance estimation, eigendecomposition, random rotation, Grassmann
tracking, and continuity selection receive no gradients and no validation
labels.

## 7. Model / Architecture And Frozen Variants

Four Transformer blocks, hidden size 768, eight sparse plus one shared expert,
top-1 routing, expert width 1,536.  Block 1 is Centered-Full.  Blocks 2--4 use
their own local centered representation.  Local-HMT uses the current nested
covariance flag.  Local-Random-Matched left-rotates that flag with one fixed
seed- and layer-specific 768-dimensional Haar matrix.  Experts always receive
the full local state.

## 8. Training Objective And Optimization

BF16, ZeRO-1, AdamW betas (0.9,0.95), weight decay 0.01, LR \(10^{-4}\), 636-step
warmup, existing 100B cosine horizon, \(\lambda_{LB}=0.01\), sequence 1,024,
global batch 768.  Each new job stops at 12,716 optimizer steps, equal to
10,000,269,312 nominal tokens.

## 9. Conditions, Seeds, And Checkpoints

| Item | Rival separated | Why needed | Evidence | Pass | Fail | Insufficient | Output |
| --- | --- | --- | --- | --- | --- | --- | --- |
| completed Centered-Full | no band restriction | reference | secondary | reference | reference | endpoint invalid | table 1 |
| completed Local-HMT | covariance identity | treatment | primary | below random | otherwise | endpoint invalid | figures 1--3 |
| new Local-Random-Matched | generic dynamic constraint | decisive control | primary | above HMT | matches/beats HMT | control invalid | figures 1--4 |

Seeds are 17 and 29.  Existing and new runs must share the same seed-specific
public step-0 parameter hash, data stream, token hashes, optimizer schedule,
milestones, validation order, capacity policy, and evaluation documents.

## 10. Primary Metric

For each seed \(s\),

\[
\Delta_s=L_{Local\text{-}HMT,s}(10B)-L_{Local\text{-}Random,s}(10B).
\]

Negative favors covariance identity.  Compute 2,000 paired-document bootstrap
replicates.  Both seed-specific CIs must be below zero; pooling is descriptive.

## 11. Secondary Metrics

Local-Random minus Centered-Full endpoint NLL; milestone NLL trajectory;
8B--10B slope; load, routing entropy and capacity drop; expert conflict,
redundancy and forced-expert regret; refresh gamma, high-confidence flip,
principal angles, target lag, throughput, and statistics overhead.

Tracking comparability is a validity condition, not a performance outcome:
target-motion isometry error must be at most \(10^{-6}\) radians at every refresh.
For both U64 and U320, the new arm's median deployed-target overlap may not be
more than 0.02 below the completed Local-HMT value, and its gamma-zero rate may
not exceed Local-HMT by more than 0.10.  If HMT wins NLL but either guard fails,
the covariance-identity verdict is insufficient.

## 12. Known Good / Known Bad / Known Confusing Cases

- Known good: fixed orthogonal left rotation preserves nested ranks and target
  principal angles exactly; gamma zero is an exact no-op.
- Known bad: right-mixing the complete eigenbasis, which imports unstable tail
  rotations; independent random frames at each refresh; unpaired step-0 state.
- Known confusing: a random arm can have different route flips even with exact
  geometric motion matching, because its routing treatment is intentionally
  different.  Such flips are outcomes unless they destroy tracking comparability.

## 13. Stage-Level Profiling Plan

| Stage | Question | Pass rule | Artifact | Handoff |
| --- | --- | --- | --- | --- |
| S0 | provenance paired? | old/new hashes and paths frozen | manifest | unit |
| S1 | rotation mathematically matched? | tests pass at float64/FP32 tolerances | pytest | smoke |
| S2 | distributed train/resume valid? | two seeds step 0--3, refresh, resume, TB | smoke record | full |
| S3 | full launch healthy? | both jobs accepted and first refresh closes | job ledger | monitor |
| S4 | terminal evidence complete? | step 12,716 plus 1,024 documents | artifact map | verdict |

## 14. Algorithm Specification

At each refresh and source layer, estimate and EMA-update covariance, compute
the current nested HMT target \(F_k\), and retrieve fixed \(O_{s,\ell}\).  Form
\(F_k^{rand}=O_{s,\ell}F_k\).  Log the principal-angle difference between
\((F_{k-1},F_k)\) and \((F_{k-1}^{rand},F_k^{rand})\).  Feed the rotated target to
the unchanged nested Grassmann candidate generator and route-continuity guard.
Persist covariance EMA, deployed flag, Haar rotation, refresh counter and
telemetry in every checkpoint.

## 15. Success / Failure / Insufficient Evidence

Use the rules in Section 0.  NaN/Inf, data drift, broken resume, non-nested
projectors, missing endpoint evaluation, or irrecoverable job state are
engineering failures eligible for exact repair.  NLL degradation, load change,
gamma zero, or high route divergence are scientific outcomes and do not stop a
numerically valid full run.

## 16. What This Cannot Claim

No universal H/M/T semantics, cross-scale generality, compositionality, or
unique expert-specialization mechanism follows from this experiment.

## 17. Block Confirmation Ledger And Review Notes

- 2026-08-04: user explicitly waived further approval and authorized direct
  construction, smoke, two-seed 8x5090 submission, monitoring, comparison, and
  knowledge update.
- All design blocks confirmed; implementation, smoke, and full scope approved.
