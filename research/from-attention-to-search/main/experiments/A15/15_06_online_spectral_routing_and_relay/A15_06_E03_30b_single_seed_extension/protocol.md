---
experiment_id: A15_06_E03_30b_single_seed_extension
legacy_experiment_id: A15_00_E03_30b_single_seed_extension
anchor_id: A15_06_online_spectral_routing_and_relay
status: approved_for_implementation_smoke_and_full
approved_by: user
approval_date: 2026-08-08
resource_profile: 5090-8-spot
primary_metric: paired_seed17_30b_heldout_nll_across_six_arms
---

# Protocol: A15_06_E03 Six-Arm Single-Seed 30B Extension

## 0. Approval Snapshot

The user approved direct exact-resume, smoke, six independent single-node
8x5090 submissions, ten-minute launch monitoring, terminal downstream
evaluation, and later result analysis.  This contract asks whether the six-arm
ranking observed at 10B persists, converges, or reverses after continuation to
30B, and whether the 30B held-out-NLL ranking agrees with downstream tasks.

This is a single-seed budget-extension audit, not a new cross-seed method
certificate.  Seed 17 is fixed for all six arms because its complete paired
10B checkpoints exist for every arm.

## 1. Terminology And Conditions

The six arms are Vanilla-Full, Centered-Full, Local-HMT,
Local-Random-Matched, Relay-HMT, and Relay-Random.  They preserve the completed
10B architectures and differ only in the registered Gate view.  Experts always
receive the full representation.

## 2. Exact Continuation Contract

Each arm resumes its immutable seed-17 checkpoint at step 12,716
(10,000,269,312 tokens) into a new `osrt-30b-*` run directory.  Training ends
at step 38,147 (30,000,021,504 tokens).  Model, optimizer, scheduler, RNG, data
cursor, running centers, covariance EMA, deployed nested flags, fixed random
frames, refresh state, load objective, capacity policy, and calibration data
must restore exactly.  The original 100B cosine horizon and completed 636-step
warmup remain unchanged.

Independent checkpoints and evaluations are required at steps 15,259, 19,074,
25,432, 31,790, and 38,147 (approximately 12B, 15B, 20B, 25B, and 30B).
Dynamic arms continue the registered 512-step refresh cadence after 10B.

## 3. Data And Evaluation

The DCLM stream, tokenizer, sampler order, frozen statistics/guard texts, and
1,024 validation documents are inherited unchanged.  The primary metric is
paired per-document 30B next-token NLL in nat/token.  For any two arms,

\[
\Delta_{A-B}=L_A(30B)-L_B(30B).
\]

Negative favors A.  Report a paired-document bootstrap 95% interval.  This
interval measures evaluation-document uncertainty only and does not replace
training-seed replication.

The terminal downstream suite is fixed before launch: 5-shot LAMBADA,
HellaSwag, PIQA, ARC-Easy, OpenBookQA, and SciQ.  All six endpoints are
evaluated without NLL-based model selection.  Task scores are reported
separately; no post-hoc weighted aggregate is primary.

## 4. Rivals And Diagnostics

The extension separates a transient 10B ordering from a persistent late-budget
ordering.  Milestone NLL, 10B--30B slope, expert load, route entropy, capacity
drop, projection gamma/flip/lag, expert conflict, redundancy, and downstream
task behavior diagnose whether convergence, route dynamics, or task-specific
effects accompany the endpoint result.  They cannot individually establish
the performance verdict.

## 5. Verdict And Validity

Within seed 17, persistence requires the 30B paired contrast to retain its 10B
direction with a document interval excluding zero.  Reversal or convergence is
reported when the direction reverses or the interval contains zero, with the
milestone trajectory locating the change.  Missing or irrecoverable arm,
broken exact resume or pairing, invalid online state, missing per-document NLL,
or missing downstream output makes the requested comparison insufficient.

Performance, load concentration, gamma zero, or degradation never trigger
scientific early stopping.  NaN/Inf, corrupt checkpoints, inconsistent data
cursors, non-orthogonal/non-nested projectors, and unreconstructable artifacts
remain engineering guards eligible for exact repair.

## 6. Claim Boundary

One seed cannot establish method stability or override the completed two-seed
10B result.  This experiment cannot establish universal H/M/T semantics,
cross-scale generality, or a unique expert-specialization mediator.  Its only
post-result decision is whether one candidate merits a new cross-seed test.

## 7. Confirmation Ledger

- 2026-08-08: the user explicitly authorized one shared seed per network,
  inclusion of the new Local-Random-Matched arm, direct 30B 8x5090 launch,
  downstream evaluation, and ten minutes of launch monitoring.
- Block audit and cross-block consistency: pass.
