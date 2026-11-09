---
experiment_id: A15_06_E01_10b_online_spectral_routing
legacy_experiment_id: A15_00_E01_10b_five_arm_training
status: complete
scientific_verdict: does_not_support_relay_hmt
last_updated: 2026-08-03
---

# Detailed Evidence Ledger

## Final 10B scientific closure

All ten registered jobs reached step 12,716 (10,000,269,312 nominal tokens)
with zero platform retries, complete terminal checkpoints, and 1,024 paired
per-document held-out NLL values.  The final verdict is a valid negative
result: Relay-HMT did not meet the registered support condition.

| Arm | Seed 17 job | Seed 29 job | Terminal state |
|---|---|---|---|
| Vanilla-Full | `om-fkmj5yx7` | `om-4qbkvqeg` | complete, zero retries |
| Centered-Full | `om-muevfjyo` | `om-1pjjbjny` | complete, zero retries |
| Local-HMT | `om-2lm4lsm4` | `om-tdavr6ta` | complete, zero retries |
| Relay-HMT | `om-tl72cr8v` | `om-anfy4nq2` | complete, zero retries |
| Relay-Random | `om-3x9kpxku` | `om-kjczyqtd` | complete, zero retries |

The final 10B NLL point estimates were 3.59874/3.60203 for Local-HMT,
3.60384/3.60259 for Centered-Full, 3.61309/3.60892 for Relay-HMT,
3.61576/3.60866 for Relay-Random, and 3.71639/3.73053 for Vanilla-Full
(seed 17/29).  Local-HMT was the point-estimate leader in both seeds, but its
paired advantage over Centered-Full was decisive only in seed 17.  Relay-HMT
was decisively worse than Local-HMT and Centered-Full in both seeds and did not
reproducibly beat Relay-Random.

The online updater passed its continuity hypothesis separately from the model
quality verdict.  HMT deployed/target overlap at 10B was approximately
0.756--0.762 for the 64-dimensional flag and 0.854--0.866 for the
320-dimensional flag, well above the never-update baselines.  Across all
registered refresh events, maximum actual high-confidence route flip was
zero.  A direct hard replacement at 10B would instead flip about 25--38% of
high-confidence tokens for Local/Relay-HMT.  No systematic refresh-associated
training-loss jump was found.

Final completeness:

- 110/110 milestone routing snapshots;
- 40/40 expert-function snapshots at 0/2B/6B/10B;
- 192 treatment refresh events and 320 per-tracker refresh rows;
- complete TensorBoard and JSONL telemetry;
- exact Router-input replay/top-1 agreement for every post-hoc snapshot;
- nine rendered figures visually inspected after generation.

Canonical compact evidence:

- [endpoint NLL](tables/endpoint_nll.csv)
- [paired endpoint contrasts](tables/endpoint_pairwise_nll.csv)
- [online refresh summary](tables/online_refresh_summary.csv)
- [analysis completeness](tables/analysis_completeness.json)
- [final summary](summary.md)
- [self-contained Chinese report](../../../../../../../daily_research_reports/backup/2026/08/0803/online_spectral_router_10b_training_report/report.md)

The next decision is not a longer Relay run.  It is whether to create a
target-motion-and-tracking-matched Local-Random control, because the current
five-arm matrix cannot distinguish covariance identity from generic dynamic
low-dimensional regularization in Local-HMT.

## Registered execution

The approved execution is five arms by two seeds. Each independent job uses one
8x5090 SPOT node, starts from the seed-specific step-0 state, retains the 100B
cosine horizon, and stops at step 12,716 (10,000,269,312 nominal tokens).

The immutable calibration/evaluation source is
`/data/250010109/MoE_Router/experiments/20260802_a15_01_04_progressive_band_source_2b_5090/artifacts/eval_tokens.pt`,
SHA-256 `5c8cca2b0821f25b8e7abc50d7653dfba8d71e9ccf167fee61b82624116a52e4`.
WOS rows 0--511 are statistics, rows 512--639 are continuity guard, and all
1,024 DCLM rows are validation documents. The frozen manifest is copied into
each run directory.

## Source snapshots

| Snapshot | Manifest SHA-256 | Use |
|---|---|---|
| `/data/250010109/MoE_Router/experiments/20260803_online_spectral_router_training/` | `6dd1314e969a89b333ea6f0dc257b7dad091593b07dd15c40a328b2ed6ad8beb` | first engineering smoke; retained invalid attempt |
| `/data/250010109/MoE_Router/experiments/20260803_online_spectral_router_training_v2/` | `6e361cc5cdbdd26fe47a41101ea1010d134d3c3482d79ad180feaf0eeafccabd` | retained invalid attempt after Relay-gradient diagnostic repair |
| `/data/250010109/MoE_Router/experiments/20260803_online_spectral_router_training_v3/` | `d958fa118521ff6b651baab4e7905c1f9d3fcb7318b740453e0c2dc94d23244b` | retained diagnostic attempt with allocator cleanup and first-step memory tracing |
| `/data/250010109/MoE_Router/experiments/20260803_online_spectral_router_training_v4/` | `cdf516dfdb2369a5baee0a845fd3f1762df9e6b7448441660b915eeb5248afd4` | retained diagnostic attempt with synchronous smoke loading |
| `/data/250010109/MoE_Router/experiments/20260803_online_spectral_router_training_v5/` | `f8430d231aaee720b166d595b295ae12406c00e010bdce31c703971eef949548` | current contract smoke; production sequence length prevents artificial sampler expansion |
| `/data/250010109/MoE_Router/experiments/20260803_online_spectral_router_training_v6/` | `3246c9c48921876f0177851e879a86dd93ce5a3ef1e05c8b951ac9722497797d` | completed five-arm contract smoke; FP32 estimator master and exact gamma-zero no-op |
| `/data/250010109/MoE_Router/experiments/20260803_online_spectral_router_training_v7/` | manifest-file SHA-256 `2dfb04a372a2022a549185964982e7e4d0829488b951e9c7580586a92db6d5d6` | immutable submission source; efficient exact linear projection, Relay-center equality guard, complete milestone diagnostics |
| `/data/250010109/MoE_Router/experiments/20260803_online_spectral_router_training_v9/` | manifest-file SHA-256 `5b1dda74acc5ff7f8bd8cc05c0485c1eeb8694769f91ec6e16658ef3d3e1dd8f` | final immutable submission source; direct Relay-branch gradient diagnostic and namespace-safe smoke |

## Engineering attempts

### Smoke attempt 1

- Job: `om-cy4590y8`, `osrt-five-arm-smoke`.
- Platform terminal state: `FAILED`, no retries.
- Completed evidence before failure: identical seed-17 parameter hash for the
  first arm, frozen-data manifest, complete step-0 DeepSpeed checkpoint,
  16-document held-out evaluation, and a live TensorBoard event file.
- Failure: the vanilla arm was terminated with return code `-9` during the
  first backward pass. The run never entered a treatment arm and has no
  scientific interpretation.
- Repair: the newly added first-layer gradient diagnostic is now executed only
  in Relay arms and uses an in-place scalar norm reduction instead of materializing
  float64 gradient tensors. The source was then frozen as v2; the failed output
  was not overwritten.

### Smoke attempt 2

- Job: `om-nn3v779f`, `osrt-five-arm-smoke-v2`.
- Intended closure: every arm runs fresh to step 2, resumes exactly to step 3,
  writes evaluations at steps 0/2/3, and treatment arms refresh at steps 0/2.
- Terminal state: `FAILED`, no retries.  Like attempt 1, it was killed before
  the first optimizer step, so the Relay-gradient repair was not causal.

### Smoke attempts 3 and 4: localization

- Jobs: `om-xnbipg9r` (v3) and `om-8riuv1mj` (v4).
- Both completed the distributed preflight, model initialization, step-0
  checkpoint, held-out evaluation, and TensorBoard event creation.
- The added memory trace never reached `before_forward`, including with zero
  DataLoader subprocesses.  The failure therefore occurred while constructing
  the first shuffled sample stream rather than in model forward/backward.
- Root cause: smoke used sequence length 128.  On the fixed binary token stream
  this creates about 2.34 billion dataset samples, eight times the production
  sequence-1024 sample space.  `DistributedSampler` materializes a deterministic
  shuffle over that artificial index space and the process is killed by host
  memory pressure before yielding a batch.
- Repair: v5 uses the production sequence length 1024 in smoke.  This changes
  no full-run setting and makes the smoke data/sampler contract closer to full.

### Smoke attempt 5

- Job: `om-utv4ze0b`, `osrt-five-arm-smoke-v5`.
- Intended closure is unchanged: all five arms fresh to step 2, exact resume to
  step 3, evaluations at 0/2/3, treatment refreshes at 0/2, live TensorBoard,
  and a common seed-17 parameter identity.
- Terminal state: `FAILED`, no retries, after yielding useful localization.
- Vanilla-Full and Centered-Full each completed fresh steps 0--2, exact resume
  to step 3, all registered checkpoints/evaluations, and TensorBoard output.
  Local-HMT completed step-0 PCA and the first optimizer step, then stopped at
  its step-2 refresh before changing the deployed projector.
- Failure: the candidate list eagerly constructed `gamma=0`.  DeepSpeed had
  converted the persistent online basis buffers to BF16; the exact no-update
  candidate therefore failed an inappropriate float64 orthogonality tolerance.
- Repair: online covariance, basis, mean, and Haar state now retain FP32 master
  buffers after DeepSpeed initialization.  Candidate construction is lazy and
  `gamma=0` returns the deployed flag verbatim, preserving its intended exact
  no-op semantics.  Every copied FP32 flag is checked at `1e-5`; seven unit
  tests pass.

### Smoke attempt 6

- Job: `om-gfl2p0ps`, `osrt-five-arm-smoke-v6`.
- Terminal state: `SUCCEEDED`, no retries.
- Machine verdict: `pass`.
- All five arms share step-0 parameter SHA-256
  `dd25272ba2e8c61917f7178adb0844de8892d4eef1bdcdf140a4e6cfe33eb7fe`
  and identical rank-0 batch hashes at optimizer steps 1--3.
- Every arm completed a fresh run to step 2, exact resume to step 3,
  checkpoints and held-out evaluations at steps 0/2/3, and live TensorBoard
  output.  Local-HMT, Relay-HMT, and Relay-Random refreshed at steps 0/2;
  neither full-input baseline executed PCA.
- This validates the five-arm scientific interface.  A final targeted Relay
  smoke remains required because the submission source additionally uses the
  algebraically equivalent `W P` linear-Gate path, enforces exact equality of
  the replicated shared Relay center, records refresh wall-clock/angles/lag,
  and reconstructs post-hoc expert diagnostics from a milestone checkpoint.

### Final-source targeted smoke attempt 7

- Job: `pt-oqhusgx4`, `osrt-final-relay-smoke`.
- State: deliberately stopped after Relay-HMT completed a fresh run to step 2.
- Valid evidence: the algebraically equivalent `W P` Gate path completed
  forward/backward and step-2 refresh; the three replicated shared Relay means
  remained bitwise equal; checkpoints, evaluations, route telemetry, and
  TensorBoard were written.
- Invalid diagnostic: the first-layer Relay gradient was read from ZeRO-sharded
  parameter `.grad` fields and reported zero.  That object is not a reliable
  path diagnostic under DeepSpeed and cannot establish that Relay gradients
  reach the shallow representation.
- Repair: the final runner measures the gradient directly on the normalized,
  Relay-only block-1 branch tensor.  This excludes the ordinary residual path
  and is fail-closed in the final smoke validator.  The stopped output is
  retained and will not be used as submission evidence.

### Final-source targeted smoke attempt 9

- Job: `pt-2efftm0e`, `osrt-final-relay-smoke-v9-final`.
- Terminal state: `SUCCEEDED`, no retries; machine verdict `pass`.
- Relay-HMT and Relay-Random each completed fresh step 0--2 and exact resume to
  step 3, with evaluations at 0/2/3 and nonempty TensorBoard streams.
- Both arms share the same step-0 public-parameter SHA and per-step data hashes.
  The Relay-only branch gradient was nonzero at all three steps; its norms were
  approximately `5.01e-4`--`5.49e-4`.  Replicated shared-center error was
  exactly zero at every step.
- At step 2 the continuity guard accepted `gamma=0.5` for Relay-HMT and chose
  the registered no-op `gamma=0` for Relay-Random.  This is valid guard
  behavior, not a performance verdict.
- A step-3 checkpoint independently reconstructed forced-expert choice regret,
  32 expert-gradient conflict rows, and four expert-output redundancy rows;
  native forced-expert replay error was exactly zero in all four layers.

## Required smoke verdict

`scripts/validate_smoke.py` fails closed unless it finds, for all five arms:

1. one common step-0 parameter SHA-256;
2. the same per-step data hashes;
3. checkpoints and milestone evaluations at steps 0/2/3;
4. explicit resume evidence;
5. live TensorBoard files;
6. refresh closure at steps 0/2 for Local-HMT, Relay-HMT, and Relay-Random;
7. no PCA execution in Vanilla-Full or Centered-Full.

At launch, no 10B scientific verdict was available and early logs, smoke NLL,
load, flip, or accepted gamma were engineering evidence only.  That historical
boundary was respected; the final verdict above uses only completed registered
endpoint and post-hoc evidence.

## Full submission and launch-monitoring snapshot (historical)

The final immutable source is v9, with manifest-file SHA-256
`5b1dda74acc5ff7f8bd8cc05c0485c1eeb8694769f91ec6e16658ef3d3e1dd8f`.
All ten registered jobs were submitted on 2026-08-03.  At the retained
05:48:43 UTC launch snapshot all were `RUNNING`, had zero retries, had written step-0 checkpoints,
1,024-document held-out evaluations, and nonempty TensorBoard event streams,
and had completed 39--51 optimizer steps.  Treatment arms had also completed
their step-0 statistics refreshes.

Within seed, all five arms share one step-0 public-parameter hash and the same
first-batch hash.  Seed 17 uses public-parameter SHA
`dd25272ba2e8c61917f7178adb0844de8892d4eef1bdcdf140a4e6cfe33eb7fe`;
seed 29 uses
`f6b2b0f1a324d95ce6f494cfec90393b8d5a6742fe9f4c59b32eed60c641e980`.
The exact timestamped state is stored in
[early_submission_snapshot.json](early_submission_snapshot.json), while raw
checkpoints, logs, event files, and telemetry remain under the worker output
root.

## Artifact ownership

- Project code/config/tests/records: this project.
- Raw logs/checkpoints/TensorBoard/calibration replay: worker and output roots.
- Full output root: `/data/250010109/MoE_Router/outputs/online_spectral_router_training/`.
- Figure contracts: [figure_contracts.md](figure_contracts.md).
- Canonical Protocol: [protocol.md](protocol.md).
- Final curated report directory:
  `/data/250010109/Research_System/daily_research_reports/backup/2026/08/0803/online_spectral_router_10b_training_report/`.
