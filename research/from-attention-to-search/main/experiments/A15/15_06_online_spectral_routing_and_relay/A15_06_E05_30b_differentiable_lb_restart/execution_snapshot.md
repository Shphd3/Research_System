# A15_06_E05 Execution Snapshot

Status: `FULL_R2_RESUMED_FROM_REGISTERED_10B_CHECKPOINT_WITH_20B_MILESTONE`

This is an execution record, not a scientific result summary. Registered
milestone comparisons may be reported as interim observations, but the Router
quality verdict remains owned by the paired 30B endpoints.

## What was repaired

The previous lineage transported per-layer auxiliary losses inside a nested
dictionary across a re-entrant activation-checkpoint boundary. PyTorch did not
attach the checkpoint backward node to those nested tensors, so the configured
load-balancing term could appear in logs without updating the Gates.

The repaired lineage returns each layer's load-balancing tensor as a top-level
checkpoint output and aggregates it outside the checkpoint. The first live
microbatch fails closed unless all of the following are true:

1. the aggregate LB tensor has an autograd function;
2. every layer-specific LB tensor receives the registered upstream coefficient;
3. an autograd hook on every Gate sees a finite non-zero gradient before ZeRO-1
   moves parameter gradients into partition buffers;
4. an isolated same-architecture LB-only probe gives every Gate a finite
   non-zero gradient; and
5. an LM-only versus LM+LB shadow step changes every Gate update.

## Validated execution contract

- Model: 4 Transformer blocks, hidden size 768, 8 sparse experts plus one
  shared expert, top-1 routing.
- Exact counts: 251,199,232 trainable parameters; 152,108,800 active parameters
  per token; 24,576 Router parameters.
- Data: fixed DCLM binary shard, sequence length 1,024, global batch 768.
- Objective: language-model loss plus always-on microbatch Switch LB with
  coefficient 0.01 for every arm.
- Optimizer: BF16 AdamW, learning rate \(10^{-4}\), warmup 636 optimizer steps.
- Arms: Vanilla-Full, Local-HMT, matched Local-Random, Relay-HMT, matched
  Relay-Random.
- Pairing: one seed (17), identical step-0 parameter hash and identical batch
  hashes across arms.
- Endpoint: step 38,147 = 30,000,021,504 training tokens.
- Full recovery checkpoints: 2B, 5B, 10B, 25B, and 30B only.

## Smoke result

All five arms completed fresh steps 1--2 and exact resume to step 3. Every rank
and layer received the BF16 representation of the registered LB coefficient
(`0.010009765625`), all Gate hooks were non-zero, and the isolated LB-only and
shadow-update probes were non-zero for all four Gates. All arms shared step-0
parameter SHA-256
`dd25272ba2e8c61917f7178adb0844de8892d4eef1bdcdf140a4e6cfe33eb7fe`
and the same three rank-0 batch hashes.

The five smoke platform jobs are marked failed only because the frozen-v4
post-run validator searched for `zero_pp_*` while DeepSpeed wrote
`bf16_zero_pp_*`. Frozen-v5 changed that analyzer glob only and reconstructed
all five pass verdicts from the preserved checkpoints, logs, telemetry, and
TensorBoard files. See [smoke_verdict.json](smoke_verdict.json).

## Original full jobs

| Arm | Job ID | Early live verification; current state |
| --- | --- | --- |
| Vanilla-Full | `om-riuwrb5e` | early guards passed; later `SUSPENDED`, 0 retries |
| Local-HMT | `om-eukhawyn` | early guards passed; later `SUSPENDED`, 0 retries |
| Local-Random | `om-4i2j9q71` | early guards passed; later `SUSPENDED`, 0 retries |
| Relay-HMT | `om-xo0fuc7v` | early guards passed; later `SUSPENDED`, 0 retries |
| Relay-Random | `om-gj30tlyj` | early guards passed; later `SUSPENDED`, 0 retries |

The live check at 2026-08-09 17:06 UTC found, for every arm, all eight
distributed-rank receipts for the LB autograd edge, all eight receipts for the
per-layer LB backward terms, and all eight Gate-gradient-hook receipts. The
TensorBoard event files and route/load telemetry were growing for all five
arms. No traceback, runtime error, NaN, OOM, or platform retry was observed.
These early losses and step counts are engineering evidence only and must not
be used to rank the arms.

## 10B milestone and recovery

All five arms completed the registered step-12,716 checkpoint
(10,000,269,312 tokens). Each checkpoint contains the model state and eight
ZeRO-1 optimizer shards, and each arm has a complete evaluation over the same
1,024 held-out documents. The mean held-out NLLs in nat/token were:

| Arm | 10B NLL | Maximum held-out expert share | Minimum layer route entropy |
| --- | ---: | ---: | ---: |
| Vanilla-Full | 3.600622 | 0.1392 | 0.9993 |
| Local-HMT | **3.598306** | 0.1470 | 0.9980 |
| Local-Random | 3.601321 | 0.1484 | 0.9980 |
| Relay-HMT | 3.605606 | 0.1438 | 0.9967 |
| Relay-Random | 3.608777 | 0.1462 | 0.9970 |

Document-paired 20,000-draw bootstrap differences at 10B were Local-HMT minus
Vanilla \(-0.002316\) [\(-0.003746\), \(-0.000848\)], Local-HMT minus Local-Random
\(-0.003015\) [\(-0.004507\), \(-0.001510\)], Relay-HMT minus Relay-Random
\(-0.003171\) [\(-0.004672\), \(-0.001662\)], and Relay-HMT minus Vanilla
\(+0.004984\) [\(+0.003366\), \(+0.006583\)]. These are one-seed interim effects,
not the registered 30B verdict. Every arm had zero capacity drop.

The original SPOT jobs were suspended on 2026-08-10 at about 09:00 UTC after
their last complete registered checkpoint. Their unsaved prefixes reached
different points and are excluded. Five replacement jobs started from the
common 10B boundary at about 12:08 UTC:

| Arm | Recovery job | State at 12:18 UTC |
| --- | --- | --- |
| Vanilla-Full | `om-xi2i7ucx` | `RUNNING`, 0 retries |
| Local-HMT | `om-bazbkey0` | `RUNNING`, 0 retries |
| Local-Random | `om-bjv3c2hd` | `RUNNING`, 0 retries |
| Relay-HMT | `om-l35z9buo` | `RUNNING`, 0 retries |
| Relay-Random | `om-1n7i1poz` | `RUNNING`, 0 retries |

Each recovery log identifies `checkpoint-12716`, restores the saved data
offset and continuation RNG, and advances beyond step 12,716. Rank-0 batch
SHA-256 values match across all five arms at recovery steps 12,717, 12,720,
12,725, and 12,730. At the last audit the arms were at 10.13--10.14B tokens,
with zero capacity drop and no NaN, OOM, traceback, or platform retry.

Worker source:
`/data/250010109/MoE_Router/experiments/20260809_online_spectral_router_30b_differentiable_lb_frozen_v5`

Source-manifest SHA-256:
`55728cbe1be8fe69aac0634fec5d86530ce14584e3b9e4bf5cdbb969354b2904`

Raw run root:
`/data/250010109/MoE_Router/outputs/online_spectral_router_training_lb_fixed`

## E05-AM01: added 20B milestone and second recovery

On 2026-08-10 the user requested an additional 20B recovery checkpoint.  The
25B checkpoint was already present in the frozen schedule; therefore the only
scientific change was to add step 25,432 = 20,000,538,624 nominal tokens.  The
registered schedule is now 2B, 5B, 10B, 20B, 25B, and 30B at optimizer steps
2,544, 6,358, 12,716, 25,432, 31,790, and 38,147.  The model, data, objective,
optimizer, arm definitions, seed, endpoint, and all other save points are
unchanged.  The amendment is recorded append-only in both canonical Protocols.

The five first-recovery jobs were safely stopped after the common 10B
checkpoint and reached `SUSPENDED`.  Their unequal, unsaved prefixes ended at
approximately 10.387--10.396B tokens and are excluded from every scientific
trajectory.  No r1 checkpoint after step 12,716 is used.

The amended immutable worker is:

`/data/250010109/MoE_Router/experiments/20260810_online_spectral_router_30b_differentiable_lb_frozen_v6`

Its source-manifest SHA-256 is
`58a9a7bd3ef8614bd832a5df4edc7051da94555ee0725806d10759814ce8ebe5`.
The contract validator reproduces every registered step/token pair, all 24
unit tests pass in the frozen dependency environment, and all 152 manifest
entries verify against their recorded SHA-256 values.

Five second-recovery jobs were submitted from the common step-12,716 state:

| Arm | r2 job | State at 2026-08-10 12:38 UTC |
| --- | --- | --- |
| Vanilla-Full | `om-x8hrb5kb` | live telemetry advancing beyond step 12,716 |
| Local-HMT | `om-bqq8igyg` | live telemetry advancing beyond step 12,716 |
| Local-Random-Matched | `om-2x9gx4wo` | live telemetry advancing beyond step 12,716 |
| Relay-HMT | `om-y9lzp3e7` | live telemetry advancing beyond step 12,716 |
| Relay-Random | `om-k0oy0kuu` | live telemetry advancing beyond step 12,716 |

Every r2 run records `RESUME_MODE=latest_registered`, target step 38,147,
source checkpoint 12,716, restored data offset, and restored continuation RNG.
Rank-0 batch hashes agree across all five arms at the same recovery steps,
including 12,717, 12,720, and 12,725.  At 12:38 UTC, the shared telemetry files
were still growing and had reached steps 12,780--12,795 with zero capacity
drop.  The local SCO CLI could not refresh the platform state because its
workspace decoder rejected a newly added billing-schema field; this client
error is reported separately and is not used as evidence of job failure.

Submission ledger:

`/data/250010109/MoE_Router/outputs/online_spectral_router_training_lb_fixed/submission/job_ledger_r2_20b.jsonl`

## Claim boundary

The smoke establishes implementation validity, LB differentiability, arm
pairing, and resumability. It does not establish that any Router is better,
that load is balanced in outcome, or that spectral identity is useful. Those
claims require the registered 30B endpoints and matched evaluation.
