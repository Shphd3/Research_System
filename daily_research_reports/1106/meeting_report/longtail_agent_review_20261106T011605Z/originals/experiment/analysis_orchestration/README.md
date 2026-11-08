# Matched evaluation planning and statistics mapping

These tools **write plans only**. They never import model libraries, start GPU
work, launch tasks, read raw predictions/scores/metrics/training losses, or infer
architecture efficacy. They explicitly pin the approved source v4 freeze (semantic QA mask) and the
actual local data/cache metadata. The formal hyperparameter freeze must already
exist; no CLI default is substituted for the selected head penalty.

## Build an evaluation plan

The requested interface is:

```bash
python analysis_orchestration/build_evaluation_plan.py \
  --freeze FORMAL_FREEZE.json --scale 2048 \
  --cohort-data AB.jsonl --eval-data ABplusSentinel128.jsonl \
  --cache caches/AB_2048 --lm-cache caches/general_lm_v3 \
  --diag-data fixed64A64B64sentinel.jsonl \
  --stage pre --out analysis_orchestration/plans/2048_pre.json
```

Repeat with `--stage after_A` / `after_B` and new output filenames. These are
argument examples, not claims that the uppercase placeholder files exist.
`--root` defaults to this experiment's execution root; **all relative input and
plan-output paths are relative to that root**. The preferred scales are2048,
8192, then an even common maximum not exceeding20000. Every scale requires both
seeds1105/1106 and all six trainable arms. New plans/views refuse existing paths.

Freeze fields: `status=FROZEN_BEFORE_CONFIRM_TRAINING`, `seeds`, six
`trainable_arms`, positive `learning_rate`, `kl_weight=.5`, `temperature=2`,
positive formal `spectrum_weight`, `l2_weight=spectrum_weight*.0625`, `spectrum`,
`assignment_seed`, `global_batch`, and optional `swap_exposure_seeds`. Also required:
`source_manifest`, `source_manifest_sha256`, complete `source_sha256` map, and
`gpu_qualification_path`. The exact approved source-v4 manifest SHA is
`e8d77b70e9c5e7530f9e77aae867e97dbb3f427f63eb131787ff2865fdf3504c`.
No automatic latest-file discovery is used. Every file in that manifest and all
required source-map entries are verified. The qualification path is recorded by
hash as the owner-frozen reference; its numeric losses are not parsed. If module
constants are also supplied, they must match the existing train-plan interface:
head64,slots256,key_width64,initial_delta_ratio.001,gate_bias−2,d1024. Actual cache
width, complete AB roster, fixed128 LM roster, student identity and input hashes
are checked from metadata; no hidden-state or logits payload is read.

The input AB file contains exactly scale/2 A and scale/2 B facts, with real
`closed_known`/`source_conditioned` per-row modes. Full evaluation contains those
same AB facts plus exactly128 disjoint sentinel facts. Diag is a **previously
fixed**64A+64B+64sentinel subset; the tool never chooses successful cases. Original
and two held-out forms, answers and source/entity identities must agree across
these files. Declared family IDs cannot cross A/B/sentinel or overlap fixed LM.
This verifies declared IDs, not complete semantic alias isolation.

The tool writes immutable `PLAN.data/eval_data.jsonl` and `diag_data.jsonl`
metadata views. Original files are unchanged. Sentinel mode `candidate`/missing
is explicitly relabeled `zero_exposure_reference`, preserving the original tag.
A sentinel pre-labeled teacher-known is rejected. AB teacher modes are unchanged.
The same source rows/order yield identical view hashes at all stages.

The plan follows `run_parallel.py`'s `{tasks:[{name,argv}]}` interface. Expected
execution receipts are `batch_logs/<scale>_<stage>/<name>.json`. It does **not**
call that runner. Root owns any later authorized scheduling.

| Stage | Physical tasks at2seeds×6arms | Included evaluations |
|---|---:|---|
| pre |4|Once-per-scale full generation,AB answer probability,LM NLL,and independent diag baseline|
| after_A |36|Every seed/arm:full generation,AB probability/diagnostics,LM NLL|
| after_B |76|Same36 plus5memory arms×2seeds×4fixed-diag states|

Live generation uses **all AB+128sentinel facts and all three forms**, batch64,
max32 new tokens, and the unchanged v3-greedy implementation's explicit `do_sample=False,num_beams=1,
use_model_defaults=False`. The tool verifies the exact v4 source manifest hash, unchanged v3-greedy file bytes, and the
actual `model.generate` call without importing Transformers. No source or gold
prefix is supplied to independent generation.

AB `evaluate_cached` uses the identical AB cache, original question prefixes,
`--without-teacher`, batch64 and frozen spectrum; it reports content-token
probabilities and diagnostics without rereading teacher logits. LM uses the fixed
LM cache and `--without-teacher`. Sentinel has generation evaluation only;
**sentinel NLL is NOT_RUN because no sentinel cache was supplied**.

All afterB memory arms receive diag `none` (active), `off`, `keys_only`, and
`values_only`. Active diag is necessary: the full AB evaluation has different
batch composition. Every diag state and its independent pre baseline share
exactly the same192rows/order, three forms and batch64. No joint K/V permutation
is presented as a destructive intervention. Intervention seed is fixed1105002.

Training paths follow the fixed contract:
`runs/<scale>/seed<seed>/<arm>/A|B/checkpoints/final.pt`.

## Materialize statistics mappings after completion

```bash
python analysis_orchestration/build_stats_mapping.py \
  --plans analysis_orchestration/plans/2048_pre.json \
          analysis_orchestration/plans/2048_after_A.json \
          analysis_orchestration/plans/2048_after_B.json \
  --out analysis_orchestration/mappings/2048.json
```

This creates three new files: the main mapping, `2048.diag.json`, and
`2048.materialization_receipt.json`. It requires all three stage plans and actual
completed infrastructure receipts; it never invents absent checkpoints or B
parent hashes. No output is written when prerequisites are missing or inconsistent.
The main/diagnostic populations overlap and **must not be pooled as independent
facts**.

Mapping validation reads only task/rank receipts, checkpoint sidecar manifests,
initialization existence, schedules, immutable source/cache metadata and file
hashes. It **does not open** `predictions_rank*.jsonl`, `fact_scores.jsonl`,
`metrics_rank*.jsonl`, logs or training losses. Raw files are checked for existence
only. Actual greedy config, task argv/plan hash, receipt facts/rows/records,
checkpoint identity and cache/data hashes must match the plan. Changed source,
views, cache records or formal freeze are rejected.

B lineage is taken from the actual training receipt:
`batch_logs/<scale>_train_B/<scale>_seed<seed>_<arm>_B.json`.
Its actual `--continue-from` path and
`input_checkpoints["--continue-from"].sha256` must match evaluated A's checkpoint
manifest; the recorded hash becomes the stats v2 continuation contract. B
`--out/--arm/--phase` must match the fixed run path. The statistics engine later
also hashes current parent checkpoint bytes. No parent SHA is filled from a
placeholder or guessed from `phase_history`.

Every mapping uses `teacher_mode=mixed`, leaving actual row modes separately
stratified, and `cohort=student_not_both_correct`. The main mapping has78 virtual
run records:6 reused baseline labels plus72 trained stage/role records. Its roles
are `facts` (full independent generation), `answer_probability` (AB-only cached
NLL, no generation endpoint), and `general_lm` (fixed next-token NLL). Separating
rosters prevents absent sentinel cached loss from being silently scored as a
failure or a dropped denominator.

The diag companion has42 virtual records and70 explicit paired comparisons:
each state minus its shape-matched baseline, and active minus off/keys/values.
It does not run the ordinary cross-arm defaults on an overlapping subset.
Baseline raw paths are reused for two training-seed quota labels; these are
**one physical baseline measurement**, not two independent seeds of measurement.
The actual per-seed A/B schedules supply1/8 labels, while frozen baseline actual
exposure remains0. Same-arm full afterB generation links to full afterA retention.

To run statistics later, use the amended engine separately on main and diag:

```bash
python analysis_tools/v2/aggregate_facts.py --manifest analysis_orchestration/mappings/2048.json --out NEW_MAIN_STATS
python analysis_tools/v2/aggregate_facts.py --manifest analysis_orchestration/mappings/2048.diag.json --out NEW_DIAG_STATS
```

No statistics command is executed by these generators. Per-fact scoring,
unresolved bounds, paired source-family intervals and qualification flags remain
owned by that frozen engine. Formal interpretation stays with the experiment
owner.

## CPU verification

`python -m unittest -v test_plan_lib.py` from this directory uses only explicitly
synthetic metadata/data/source stubs. The end-to-end fixture's supposed raw score
files contain deliberately invalid poison text; successful mapping proves those
contents were not parsed. Tests cover complete arm/seed/task matrices, immutable
inputs, denominator/mode/identity guards, v3 greedy source+actual receipt guards,
missing/corrupt B lineage, cache drift and CLI plan-only behavior. Temporary
fixtures stay under this directory and are removed. A persisted
`SYNTHETIC_SMOKE/` example, if present, is not an experiment result.

## Semantic-v4 QA mask and raw LM distinction

Formal AB caches must have the complete literal frozen
`layout.answer_mask_policy.version=semantic_content_v4` policy and the v4
prepare-cache source hash. The policy moves only consecutive individually
pure-whitespace answer-leading tokens into the known gold prefix, keeps merged
whitespace/content tokens whole, preserves both full input-ID sequences, rejects
empty semantic answers, and excludes EOS. This does **not** supply whitespace or
gold answers during independent generation.

The formal generator rejects the CPU-derived DEV-cache provenance. That
provenance can be audited by `mask_contract.py` with its explicit DEV-only option:
parent layout/stage hashes, unchanged full IDs, copied slices, deep-verification
and derivation receipts must agree, and inference remains explicitly false.
It is never relabeled as new GPU inference. Formal AB completion instead requires
both student/teacher stage receipts bound to the new layout and rank devices
recording CUDA inference; these metadata proofs are checked during mapping
materialization.

The fixed general LM cache remains
`independent_general_lm_pre_finalnorm_v1`: first token as known prefix, all later
original tokens **including whitespace** predicted, no artificial EOS. It does
not require or fabricate a QA semantic mask and is never semantically clipped.
AB answer probability must be recomputed on semantic-v4 targets; old-mask DEV
training cannot freeze formal hyperparameters. Pure greedy generation did not
change, but this tool never silently rewrites old receipts to call them v4.

The provisional source-v3 tool files/tests are preserved under
`history_provisional_v3/`; they are not the formal entry point. A previous
`SYNTHETIC_SMOKE/` is an explicitly fake v3-era fixture. Current formal-mask CPU
examples use `SYNTHETIC_SMOKE_V4/`. No example is a model result.
