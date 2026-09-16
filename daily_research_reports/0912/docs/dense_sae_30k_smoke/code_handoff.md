# Dense LM / SAE 30k: code handoff and next audit

Updated at: 2026-09-12T09:15:12Z
Destination: a researcher-started Sol task using the same mounted workspace.
Scope: local code handoff, audit and subsequent engineering work; no new GPU
submission, formal training, scientific decision, commit, push or external sync.

The researcher requested that this task update the code/work records and prepare
an audit prompt for Sol. This document records engineering facts and suggested
acceptance checks. The prompt becomes the receiving task's instruction when the
researcher forwards it; this document and conversation memory grant no authority.

## Read first and locate the baseline

1. Repository `AGENTS.md` and [training reuse index](../../../../docs/training_reuse_index.md).
2. [Execution scope](execution_scope.md) and [completed execution record](execution_record.md).
3. [Current continuation](../../../../.research/memory/conversations/0912-梳理-sae-动态形成预训练方案/continuation.md),
   then that source task's entire `memory.md` for operational history.
4. Execution root `/data/250010109/MoE_Router/experiments/20260912_dense_sae_pretraining`:
   `README.md`, `docs/reuse_sources.json`, `configs/smoke_4h100_sae30k.json`,
   `handoff/baseline_manifest.json` and its referenced code-only archive.

The execution root is **not a Git repository**. Research_System Git does not
version that execution code. The archive and per-file hashes preserve a
reviewable starting point; no Git commit is implied. Do not overwrite/extract
the archive over later changes. It excludes datasets, weights, checkpoints,
logs, environments, caches and credentials. Raw run evidence stays at its owning
paths; this is a shared-filesystem handoff, not a self-contained external export.
If a root is inaccessible, identify it as unverifiable and stop dependent work.

Thirty current code/config/test files were rechecked against
`runs/local_checks/probe_fix_receipt.json` at handoff preparation, with no drift.
The current runtime contract is
`abb0c6c3d6449bb7324a5e46f81c2f92f71afa41841cd1db78ae2d9da7cb5faf`.
The successful run is `runs/smoke_4h100_sae30k_fix_20260912080957`, job
`pt-ro6ijc54`; its smoke, shell terminal and independent artifact receipts
record PASS, exit 0 and SUCCEEDED. Checkpoint content hashes were verified in
the preceding work; this handoff refresh checks small receipts and current
sources, not another full scan of the approximately 10 GB checkpoint set.
The initial pre-update failure `pt-i9ohovsb` remains in
`runs/smoke_4h100_sae30k_20260912080130` with its failed engine and diagnosis.

## Actual package structure and responsibilities

All paths in this table are relative to the execution root. Inspect the listed
assets before adding another implementation of the same primitive.

| Layer | Files | Current responsibility / reuse |
| --- | --- | --- |
| Configuration and model | `configs/smoke_4h100_sae30k.json`; `dense_sae/model/configuration_qwen3_sae.py`, `modeling_qwen3_sae.py`, `sae.py` | Adapted 0912 native Dense/Top-K reference, random initialization, tied embeddings, aligned next-token CE, final normalized detached observer; no upstream numerical-parity claim |
| Step and optimizer | `dense_sae/engine.py` | Adapted previous DDP/AdamW pattern, disjoint LM/SAE groups, global loss counts, separate clipping, independent sampling, global activity counters, integer-only state-probe indices |
| Orchestration | `dense_sae/train.py` | Bounded smoke CLI, data stream/cursor, validation, paired saves, internal replay, fixed-panel export and runtime receipts |
| Data and identity | `dense_sae/data.py`, `data_contract.py`, `tokenizer_contract.py` | Copied/adapted clean training framework; mmap packed tokens, deterministic sampler, frozen-view and tokenizer identity |
| Recovery and topology | `dense_sae/checkpoint.py`, `distributed_context.py` | Atomic complete-manifest checkpoints, optimizer/scheduler, per-rank RNG and dedicated Generators; DDP-only context with legacy EP=1 compatibility fields |
| Health primitives | `dense_sae/health.py` | Copied helper library; the active engine uses direct finite checks, not every old health/EMA policy |
| Fixed inputs and extraction | `dense_sae/analysis/build_probe_panel.py`, `collect_activations.py` | Explicit causal-position panel, complete-checkpoint reader, bounded representations and sparse codes |
| Analysis | `dense_sae/analysis/feature_statistics.py`, `representation_evolution.py`, `feature_semantics.py` | Reconstruction/activity diagnostics, fixed-panel cross-readout and optional externally supplied relation labels; group/intervention helpers are not invoked by smoke |
| Runtime and entrypoints | `scripts/runtime.sh`, `run_train.sh`, `run_smoke_4h100.sh` | Mounted dependency activation, torchrun and explicit bounded shell launch; no automatic formal continuation |
| Inspection / fixtures | `scripts/inspect_parameter_budget.py`, `prepare_paired_data_view.py` | Meta-device parameter accounting and small test-data view creation; real data view preserved |
| Qualification | `tests/test_pipeline.py`, `distributed_smoke.py`, `test_data.py`, `test_data_contract.py`, `test_health.py` | 17 CPU tests and earlier two-rank Gloo/global-batch check; existing results remain scoped to their recorded source versions |
| Packaging / provenance | `pyproject.toml`, `README.md`, `docs/reuse_sources.json`, `docs/reference_4gpu_smoke.json` | Package layout, 19 original copied-source hashes, configuration ancestry and usage boundaries |

The original training project remains the preferred source for data/checkpoint
primitives. The new Dense package is the target for subsequent work; do not
restart from the flat 0912 draft or transplant the old MoE trainer wholesale.
No general `dense_sae/benchmark.py` or `analysis/run_analysis.py` was implemented.
Formal token scheduling, long-run recovery policy and independent SAE refitting
also remain outside this completed smoke implementation.

## Training and output interfaces to preserve

`BinaryTokenDataset` already provides shifted targets; the model receives
aligned `input_ids` and `target_ids`. The step accepts optional attention/target
masks plus explicit `sae_mask`. It computes separate LM and SAE global sample
counts over ranks and accumulated microbatches, then applies DDP's averaging
correction. The observer receives detached final-post-RMSNorm h; only LM loss
updates the backbone. Optimizer membership and clipping must preserve this
independence, including identical backbone updates in matched none/observer tests.

The retained baseline is the fixed smoke configuration, not a new parameter
selection: hidden size 1024, SAE width 30000 and k=32, random initialization,
approximately 1/8 independent SAE position sampling. LM and SAE reuse separate
AdamW settings/warmups. The first scheduled update uses zero LR under the
inherited LambdaLR convention; the 100-update smoke ends inside LM warmup.
Audit/record this convention instead of silently changing it or selecting a
formal decay/token budget.

| Surface | Input | Output / contract |
| --- | --- | --- |
| Panel builder / collector | `input_ids[N,S]`, `attention_mask[N,S]`, `positions[N]`, unique `sample_ids[N]`; validated paired checkpoint | `raw_h`, `h`, `reconstruction` [N,1024]; `indices`, `values` [N,32]; position/sample/token IDs |
| Paired checkpoint | Model, optimizer, scheduler, cursor/counters, world topology, RNG/Generators, training contract | `state.pt`, four `rng_rank_*.pt` in the GPU run, complete checksum manifest published last |
| Extraction provenance | Checkpoint and fixed panel | Panel/checkpoint hashes, optimizer step and actual tokens; r in the plan is named `raw_h` in files |
| Statistics / cross-readout | Same ordered sample identities, activations and early/late SAE states | JSON diagnostics; no semantic verdict or additive causal decomposition |

The smoke's panel is 16 unlabeled held-out windows. It proves interface wiring,
not a semantic benchmark. The data-view checks establish manifest/path/size and
source-file heldout exclusion, not document-level contamination independence.

## Six audits for Sol, in priority order

**1. External process resume (P0; confirmed implementation gap).** Inspect
`train.py` around restore, initial export, replay and final receipt construction
(current lines 222–336). After restore the code recreates `initial_sae`, initial
validation and `initial` activations, rather than retaining the run's original
step-zero baseline. Resuming at or beyond the replay checkpoint leaves the local
`replay_report` unset because the equality trigger has already passed. Metric
rows can duplicate uncommitted updates, and physical-update/end-to-end accounting
currently describes only the current process. `Path(args.resume)` is also not
normalized like the checkpoint resolver before panel provenance is used.
Fix orchestration, not just checkpoint deserialization. Preserve completed run
guards and old evidence. Acceptance: same-contract tiny CPU uninterrupted run
versus stop/save/exit/new-interpreter/resume, before/at/after the replay boundary;
compare original initial-panel identity, full model/optimizer/scheduler state,
next inputs/masks, RNG/counters, unique log steps and final accounting. Do not
change the contract's max_steps merely to manufacture the interrupted run.

**2. Gradient and optimizer isolation (P0; re-audit invariant).** Inspect
`modeling_qwen3_sae.py`, `engine.py` and matched none/observer tests. Check detach,
tied-weight deduplication, one optimizer owner per parameter, independent LM/SAE
clipping and exact counted DDP scaling. Extend only meaningful missing coverage:
unequal eligible counts across ranks/microbatches, masks and a locally empty SAE
sample with nonempty global count if that input is supported. State the supported
boundary explicitly if rejecting it. A loss curve alone is not a gradient audit.
Do not introduce another objective or silently activate exposed legacy fields.

**3. Data cursor, target semantics and identity (P0; evidence/coverage audit).**
Verify exactly one next-token shift, causal positions/masks, stable frozen-file
ordering, disjoint rank samples and exact next-window/mask identity after process
restart. Preserve the data manifest and tokenizer-only identity; never load the
Qwen checkpoint weights. Source-path split exclusion is not semantic or document
decontamination. Do not choose a new split/order to repair an accounting bug.

**4. Checkpoint completeness and failure exits (P1; stronger coverage needed).**
Inspect `checkpoint.py`, the trainer, shell timeout and tiny recovery tests.
The GPU `state_probe(model)` samples at most 16 values from each **model** state
tensor; it does not compare all Adam moments or scheduler state. The CPU test
does compare complete model/optimizer/scheduler tensors, but runs its loader
comparison inside one interpreter. Add a distinct-process CPU recovery check,
manifest corruption/incomplete-save rejection and a bounded graceful-stop test.
Distinguish incomplete/time-limited execution from acceptance; retain rank and
terminal evidence. A hard kill need not produce a completed checkpoint or shell
receipt. Do not weaken strict source/config/topology checks to load old evidence
after editing code; produce new qualification artifacts for the new version.

**5. Analysis identity and inference side effects (P1; preserve research boundary).**
Audit fixed sample order/positions, checkpoint-panel association, dtype/shape,
width/index bounds and save/load provenance. Ensure extraction leaves training
mode, RNG and activity counters unchanged, or clearly enforces caller-owned
restoration. Same-time and cross-time readouts must identify which h and SAE are
used; record precision where BF16 extraction and FP32 rereading differ. Semantic
labels and interpretation remain researcher-owned; do not enable grouping,
intervention or claim latent-index equality across independently fitted SAEs.

**6. Configuration, bounds and performance accounting (P1; missing general harness).**
Audit inert/unsupported fields, LR step numbering, CLI validation, timeout and
storage limits, and the distinction between logical updates and discarded replay.
Warm-step timing excludes preceding data fetch; end-to-end timing includes setup,
I/O and analysis. This was observer-only: there is no measured no-SAE GPU overhead.
A future benchmark harness may be prepared locally if needed, but do not submit
it. Do not turn this smoke into a formal runner by deleting its <=100-step guard;
record required long-run configuration/approval separately without inventing it.

## Suggested next code delta and completion

Start with audit 1 and its distinct-process regression in `dense_sae/train.py`
and the existing test suite. Reuse `checkpoint.py` and `engine.py`; change them
only for a demonstrated contract defect. Add focused tests for the other audits
when they expose an actual missing boundary. Keep new qualification in a fresh
local output directory, preserving both GPU attempts and the frozen code archive.
Update `README.md` and this engineering record with resolved/open items. Formal
training configuration, additional GPU work and semantic criteria stay pending.

Sol's deliverable should identify each confirmed defect by file/function and
reproduction, distinguish missing tests from observed failures, show the minimal
fix and exact test evidence, and list unresolved items. It must not state that
100-step acceptance establishes width superiority, semantic formation or long-run
stability. Create a new source-task memory under Sol's verified task name with
`Continues from` pointing to this record; do not append to this task's memory.
At takeover, keep one CURRENT continuation for this workstream and supersede the
old brief by reference. No task has been created or sent a message on the
researcher's behalf by this handoff preparation.

## Receiving audit disposition

The researcher-started receiving task completed the requested local repair.
The owning update is the execution record's **Local post-handoff audit and
repair** section; detailed test evidence is in execution
`runs/local_checks/resume_audit_20260912T0920Z/receipt.json`.

- Audit 1 is repaired and CPU-qualified across distinct Python processes before,
  at and after the replay boundary, including a two-rank case. Step-zero
  SAE/panel identity is immutable; resume paths, replay proof, logical logs,
  physical updates and whole-run wall time now have separate explicit records.
- Audits 2 and 3 remain satisfied for the implemented contract: detached SAE
  gradients do not alter LM gradients/updates, optimizer ownership and clipping
  are disjoint, counted normalization matches the global batch, targets shift
  once, and recovery identity now includes attention/target/SAE masks. A rank
  with zero total SAE samples is explicitly unsupported and collectively
  rejected; empty component microbatches remain supported when the rank total is
  nonzero.
- Audit 4 now has distinct-process full AdamW/scheduler and all-rank RNG
  comparison, incomplete/checksum rejection and a graceful incomplete exit.
  Hard-kill behavior remains bounded as originally stated: it need not publish a
  completed checkpoint or terminal receipt.
- Audit 5 now preserves caller training mode across activation collection and
  cross-readout. Fixed sample/position/checkpoint identity and the unlabeled
  engineering-only boundary remain unchanged.
- Audit 6 now tests the inherited zero-LR first update, rejects unsupported SAE
  loss weighting/bottleneck feedback, validates the replay step and storage
  bound, and applies wall time across resumed processes. No no-SAE GPU overhead
  or long-run timing/stability measurement exists.

The modified source has CPU qualification only. A future GPU run, formal 20B
budget/schedule/checkpoint policy, semantic panel and interpretation criterion
remain researcher decisions; this disposition does not authorize them.
