---
experiment_id: A15_06_E03_30b_single_seed_extension
legacy_experiment_id: A15_00_E03_30b_single_seed_extension
status: complete
scientific_verdict: complete_seed17_persistence_with_relay_failure
last_updated: 2026-08-09
---

# Execution Evidence Ledger

The approved experiment exact-resumed all six seed-17 10B checkpoints to the
registered 30B endpoint.  All six terminal checkpoint and paired evaluation
artifacts are complete.

## Pre-submission smoke record

- First smoke job `om-m470cqgn` exact-resumed Vanilla-Full from optimizer step
  12,716, consumed the next paired batch, and wrote complete checkpoint 12,717.
- The wrapper then stopped before the dynamic-arm smoke because its log check
  mistook the legacy client-state `global_step=101728` microstep counter for an
  optimizer-step counter.  The runtime's independent engine guard had already
  verified optimizer step 12,716.  This is a smoke-checker wording failure, not
  a training or resume failure.
- The check was changed to require the unambiguous engine message
  `Continuation RNG restored ... step 12716` plus the exact global sample
  offset 9,765,888.  Scientific configuration and runtime code were unchanged.
- Corrected dynamic smoke job `om-7glq1o7o` exact-resumed
  Local-Random-Matched, restored the same sample/RNG state, completed one
  optimizer step, and wrote complete checkpoint 12,717.  The platform marked
  the short job failed only after `Training finished`, during distributed
  process teardown (`TCPStore server has shut down too early`).  The persisted
  load/train/save evidence is valid; the teardown condition occurs after the
  requested smoke evidence and cannot affect a long-running job before its
  endpoint.  It remains recorded for terminal-job cleanup review.

## Frozen execution source

- Worker snapshot:
  `/data/250010109/MoE_Router/experiments/20260808_online_spectral_router_30b_v2`
- `SOURCE_MANIFEST.sha256` file digest:
  `567fcd507a571d816fff3aa0a75a917aa5843842be4fa3f66e17864ce4264acc`
- Contract validator: pass for six arms, seed 17, resume step 12,716,
  endpoint step 38,147, and the six-task downstream suite.
- Nine dependency-light unit tests passed.  Runtime/model construction was
  exercised on the registered 8x5090 smoke because the login environment does
  not provide the frozen NGC Transformers dependency layer.

## Full job ledger and 10-minute launch audit

All jobs use workspace `share-space`, AEC2 `computing-cluster-5090-01g`, one
`n12lp.nn.i10a.8` worker, SPOT quota, and the frozen NGC 25.06 image.

| Arm | Job ID | Start UTC | State at 17:06:46 UTC | Retries | Observed optimizer step | Observed tokens |
| --- | --- | --- | --- | ---: | ---: | ---: |
| Vanilla-Full | `om-49e2qle4` | 16:56:35 | RUNNING | 0 | 12,901 | 10,145,759,232 |
| Centered-Full | `om-42hkbafl` | 16:56:46 | RUNNING | 0 | 12,889 | 10,136,322,048 |
| Local-HMT | `om-0hozktg1` | 16:56:46 | RUNNING | 0 | 12,888 | 10,135,535,616 |
| Local-Random-Matched | `om-jemmzjp3` | 16:56:47 | RUNNING | 0 | 12,887 | 10,134,749,184 |
| Relay-HMT | `om-4s7jz55t` | 16:56:47 | RUNNING | 0 | 12,888 | 10,135,535,616 |
| Relay-Random | `om-0angrw82` | 16:56:47 | RUNNING | 0 | 12,887 | 10,134,749,184 |

For all six jobs, the audit observed the exact global sample cursor 9,765,888,
the checkpointed RNG continuation at optimizer step 12,716, at least 171 new
optimizer steps for the slowest arm, finite training loss/LR values, one
growing TensorBoard event file, and no RuntimeError, traceback, OOM, or NaN
signature.  Step differences at this snapshot reflect launch time and runtime
overhead; every arm retains the same registered endpoint step 38,147.

The first post-10B online refresh is scheduled at step 13,056, beyond this
ten-minute audit.  Online-state restoration itself was already exercised by
the Local-Random-Matched resume smoke.  Per user instruction, continuous
monitoring stops here; terminal evaluation begins only after all six runs reach
30B.

## Terminal evidence

All six runs reached optimizer step 38,147 = 30,000,021,504 tokens and wrote
complete model plus eight optimizer shards.  The 1,024 held-out DCLM documents
remained paired.

| Arm | 30B NLL |
| --- | ---: |
| Vanilla-Full | 3.49394693 |
| Centered-Full | 3.39598511 |
| Local-HMT | **3.39191286** |
| Local-Random-Matched | 3.39679848 |
| Relay-HMT | 3.40752990 |
| Relay-Random | 3.40865494 |

Registered paired effects in nat/token, with 2,000-draw document intervals:

| Contrast | Mean | 95% CI | Reading |
| --- | ---: | ---: | --- |
| Centered − Vanilla | -0.097962 | [-0.099938, -0.096070] | Centered better |
| Local-HMT − Centered | -0.004072 | [-0.005586, -0.002555] | seed-17 local gain persists |
| Local-HMT − Local-Random | -0.004886 | [-0.006425, -0.003359] | covariance identity gain in seed 17 only |
| Relay-HMT − Local-HMT | +0.015617 | [+0.014139, +0.017159] | Relay worse |
| Relay-HMT − Centered | +0.011545 | [+0.009926, +0.013140] | Relay worse |
| Relay-HMT − Relay-Random | -0.001125 | [-0.002635, +0.000381] | unresolved |

Within seed 17, Local-HMT's late-budget advantage persists and Relay-HMT remains
worse.  The covariance-identity reading remains seed-conditioned because the
registered seed-29 10B control did not reproduce it; extending only seed 17 to
30B cannot establish a cross-seed claim.

## Source-model LB boundary

The configs and logs recorded `lambda_LB=0.01`, but the later A16 implementation
audit established that re-entrant checkpointing detached the nested LB
auxiliary tensor from backward.  These six source trajectories therefore did
not receive an effective LB gradient.  Their NLL and routing outcomes remain
valid observations, but they cannot be attributed to LB regularization.

## Downstream handoff

The requested eight-task terminal evaluation is owned by
[A15_06_E04](../A15_06_E04_30b_downstream_evaluation/summary.md).  It found no
broad-transfer Pass; Local-HMT retained task-specific ARC-Easy and LAMBADA gains,
while covariance identity and Relay lacked a downstream certificate.
