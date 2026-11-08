# Durable matched expansion runner

This utility runs only inside the **existing allocated2GPU worker**, after the
initial complete2048 matrix and expanded-screen/cohort gates. It never submits a
job, changes the frozen training/evaluation/statistics sources, chooses arms or
parameters from scores, writes an asset catalog, or creates another research
project. **No GPU execution was performed while implementing/testing it.**

Review/dry-run:

```bash
python expansion_runner/run_expansion.py \
  --root /data/250010109/MoE_Router/experiments/20261105_last_layer_memory \
  --gpus 2 \
  --out /data/250010109/MoE_Router/experiments/20261105_last_layer_memory/expansion_runner/runtime_0044 \
  --controller-start 2026-11-05T16:48:33.980235+00:00 \
  --max-hours 28 --reserve-hours 2 --cost-safety-factor 1.25 --dry-run
```

After root reviews the source, queue the same direct Python command with
`--execute` instead of `--dry-run`. An existing output requires
`--resume-existing`; its configuration must match. Dry-run never imports the GPU
guard or launches a subprocess. If prerequisites are still running/missing, it
writes a WAITING report and starts no GPU work. `--execute` is required explicitly;
it checks worker_live.gpus2, direct parent PID, resource profile, and exactly two
visible CUDA devices. It must be invoked directly by the current worker,not a new
allocation or an unrelated SSH process. No SCO/submit operation exists.

## Immutable prerequisites

`0036` is a queue number,not a count of phases. The five initial receipts are:
0032pre,0033trainA,0034afterA,0035trainB,0036afterB. Each must be COMPLETE/exit0,
bound to its original queue JSON/task hash and actual argv. The nested
`batch_logs/2048_{pre,train_A,after_A,train_B,after_B}` summaries and every child
receipt must match the original plan, with counts **4/12/36/12/76**, no unstarted
entries. TrainA/B certificates must bind the same formal freeze and plan.

The runner pins Protocol SHA
`e92dd33c7f3ce1c17f98efd8b3b224450005e1cff5f91e0de684797a82acbe01`, verifies frozen
source/qualification/contract references, requires completed queue0037–0043,
and checks the three all20000 CPU merge summaries. Expanded selection must be
`cohorts/expanded_greedy_semantic_v4/manifest.json` with
FROZEN_PRETRAIN_SELECTION status. It selects8192 if available and the largest
balanced eligible file<=20000, excluding2048 and deduplicating equal scales.
Dataset hashes are checked before use. No raw screen outputs, accuracy or loss
values are used to choose scale/arms/hyperparameters.

## Workflow for each admitted scale

All path components use a numeric **string** scale. Every scale has the same
six trainable arms and seeds1105/1106; fresh initialization and the same frozen
Protocol apply. Stages are:

1. New semantic-v4 cache layout (`prepare`,32GiB cap).
2. Student then teacher cache inference using `python -m torch.distributed.run
   --standalone --nproc_per_node=2` in the existing allocation.
3. Full `verify_cache.py` verification.
4. Dataset copy:expandedAB plus the identical pilot128sentinel and fixed
   64A+64B+64sentinel diagnostic IDs/questions/source fields. No new questions or
   score-dependent case selection.
5. Existing CLI builders generate pre/afterA/afterB evaluation plans and trainA/B
   plans.
6. Sequential full batches:run_parallel pre → execute_formal_plan trainA →
   run_parallel afterA → execute_formal_plan trainB → run_parallel afterB.

Paths remain `runs/N/seedSEED/ARM/A|B/checkpoints/final.pt`, `plans/N/*.json`,
`batch_logs/N_{pre,train_A,after_A,train_B,after_B}`. Cache is
`caches/expanded_N_semantic_v4`. New datasets live under this runner output.
No partial best-arm expansion is selected.

## Adaptive time and space

The hard deadline is controller_start+max_hours (never>28h). At least2h is
reserved for verification. Initial forecasts use complete pilot matrix wall time,
cache-stage timings, actual file sizes and filesystem free space. The default
cost safety multiplier is1.25. Cache planned bytes come from the actual pilot
layout; filesystem checks reserve4GiB plus conservative checkpoint/output space.
Actual account quota beyond filesystem df remains outside this measurement.

**Initial DEFER is tentative.** After every complete new scale, its15 actual
step runtimes and measured storage are saved. All not-yet-run candidate scales
are re-budgeted from the **latest completed N** and current time/free space. For
example, a fast8192 matrix can change the maximum scale from tentativeDEFER to
ADMIT. Only runtime/space drive that change. Budget snapshots append under
`budget_history/`; old decisions are never overwritten. If8192 cannot fit, the
larger full matrix is deferred; no preferred arm is substituted.

Started/resumed scales skip only verified completed steps. Remaining work is
forecast before new subprocesses; an incomplete scale that no longer fits is
stopped for explicit recovery/budget review. Each subprocess timeout ends before
the matrix-work deadline, preserving the2h reserve. A timeout sends TERM,then
KILL after grace if necessary, **only to the process group started by this
runner** (`start_new_session=True`); parent worker and other tasks are not killed.
STOP files at output/STOP or orchestration/queue/STOP prevent subsequent steps.

## Durable receipts and explicit recovery

Each of15 steps has an exclusive log, RUNNING marker and final receipt containing
full argv, input hashes, frozen source hashes,start/end,exit code,elapsed seconds,
log hash and verified output identities. Completed steps are revalidated and
skipped; they are not re-executed in the same process or a clean resume. A changed
input/source/output, orphan output, missing receipt, prior failure or interrupted
RUNNING marker produces RECOVERY_REQUIRED. **There is no --force or silent
adoption.** Root must audit and explicitly repair/recover that affected step;
this tool will not erase guards, overwrite failed outputs or fabricate completion.

Large cache payloads use completed-stage SHA/size/mtime attestations, followed by
one full deep verification; they are not rehashed repeatedly. Saved checkpoint
requests use the writer's sidecar SHA and actual file size/mtime, explicitly
marking when the payload was not rehashed here. Exact optimizer/RNG resume still
belongs to the qualified training interface.

Monitoring files contain no model scores:

- `state.json`:status,current_scale,current_step,completed_steps,deadlines,
  latest_budget_snapshot.
- `steps/NAME.receipt.json`:status,exit_code,start,end,elapsed_seconds and hashes.
- `runtime_calibration/N.json`:per-step/cache/matrix pure runtime,scale,storage.
- `runner_receipt.json`:final complete/deferred/failed/recovery states.
- `registration_requests/N_STAGE.json`:actually saved cache/dataset/checkpoint
  references for **root to register**. Partial failed-stage saves are labeled.
  Existing parent assets/Protocol are reused by references; no asset ID is invented
  and no catalog is written.

Nine CPU/fakeprocess tests pass, including every initial child gate, adaptive
maximum-scale reconsideration, exact sentinel/diag reuse, no duplicate completed
subprocess, explicit orphan/failure recovery, numeric-scale full workflow,
reserve/append-only history, launch failures, and a real harmless CPU sleep
subprocess timeout that leaves a separate owned sentinel process alive. No model
inference or training was run for these tests.
