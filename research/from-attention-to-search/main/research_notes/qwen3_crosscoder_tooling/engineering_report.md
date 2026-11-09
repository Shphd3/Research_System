> 2026-10-12 A03: The evidence below is the historical8192 qualification. Current32768 choices and actual H100 pilot startup are recorded in [the updated operational plan](validation_plan.md) and execution-side `runs/pilot_32768_20261012/execution_certificate.json`. Historical results are not relabeled.

# Frozen Qwen3 all-layer CrossCoder: local engineering report

[中文](engineering_report_cn.md) · [Validation plan](validation_plan.md) ·
[Execution entry](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/README.md)

**Local implementation checks pass. Pilot training has not run. Measurement
quality is not evaluated, and no scientific answer is claimed.** This is a
factual engineering note for the researcher's requested tool, not a scientific
Summary or formal-run authorization. Sources were checked on2026-10-12.

## Subsequent timing amendment A01

The one-hour/4GPU-hour values below describe the original proposal. The
researcher subsequently rejected that restriction; the current draft allows
12 hours/48GPU-hours. Exposure limits are unchanged and no job was submitted.
See the [current validation plan](validation_plan.md).

## Purpose

Check whether a frozen Qwen3-0.6B Base can supply correctly paired block outputs
to the requested all-layer CrossCoder, and whether architecture, loss, scaling,
gradients, telemetry and exact recovery are implemented consistently. The tool
is intended for future structural, occurrence-frequency and common-learning
measurements. Engineering success cannot establish those scientific properties.

## Model

Current Base path is `/data/share/Qwen3-0.6B-Base`, revision
`da87bfb608c14b7cf20ba1ce41287e8de496c0cd`. The full weight hash is
`cd2a512003e2f9f3cd3c32a9c3573f820bb28c940f73c57b1ddaa983d9223eba`.
Model card, config, pinned download metadata and complete hash were checked;
this is Base/Pretraining, 28 layers, hidden1024. No Instruct model, router,
trainable Base, model download or additional saved Base copy is used.

The CrossCoder has independent encoder[28,1024,8192] and
decoder[28,8192,1024], shared bias[8192] and decoder bias[28,1024]. Count is
469798912. FP32 loss averages paired positions and sums hidden dimensions and
layers. The L1 weight is sum of per-layer decoder vector norms. TRAIN-only
coordinate RMS=1 scales are uncentered and invertible. Reviewed L1 initialization
uses decoder norm0.05, fixed upstream commit
`d1fd6f3fea41fc1123699cc09f4cdad47ca35160`; weights are initially transposed
copies but remain independent.

The prepared DCLM view contains 2000000 unique TRAIN positions from1935
documents, and32768 VAL positions from41 documents. Scanning20000 source
records processed22669105 original token IDs before selection. There were12
invalid source texts,3 exact duplicate texts and2 detected near-duplicate links.
Same-document chunks retain the same split. No padding is emitted. The selected
view is English by source fastText labels; this is not an independent language
audit. The original full source has59812 records. Exact upstream dataset
revision is Unknown; its complete local SHA256 pins the payload. Historical
audit exposure and bounded near-duplicate recall remain explicit limitations.

## Hypothesis

Correct implementation should match hand calculations, collect every block
once at identical positions, preserve Base weights, reconstruct the inverse
scale, allow gradients only into CrossCoder, and reproduce the next optimizer
update after restoring RNG and data cursor. Incorrect hook indexing, unpaired
rows, loss reduction, tied storage or contaminated calibration are plausible
wiring failures. These tests adjudicate those engineering alternatives only.

## Conclusion

The local checks passed:

| Check | Actual evidence and boundary |
| --- | --- |
| Unit/integration/runtime suite |42 CPU tests passed in29.07s; includes real tiny-Qwen28-layer integration and2-rank CPU DDP |
| Full requested architecture |469798912 real parameters; finite full-size FP32 CPU forward/backward on2 positions; no optimizer update |
| Actual pretrained Base hooks |28 hooks each invoked once; first27 outputs exactly match hidden_states references; last block exactly matches final norm input |
| Base immutability |FP32 in-memory state hash unchanged before/after checks; BF16 state also unchanged; all parameters frozen and gradients absent |
| No-op next-token control |Actual Base all-layer original-output overwrite gives delta0.0 nats/prediction on8-token CPU panel |
| Loss/scaling/pairing |Hand-computed squared-loss and sum-of-norms cases, masked positions, untied weights and inverse scaling pass |
| Recovery |Synthetic FP32 Adam/RNG/normalization/mid-document cursor replay reproduces next parameters and moments bitwise |
| Parallel objective |2-rank gloo/no_sync accumulated gradients, loss and Adam update match serial paired batch; full4-H100 path unrun |
| Input/source gates |Current strict model/tokenizer/raw access checks, derivative data/config binding,23-file source freeze and dry-run submission pass |

The actual Base/full-size local qualification took29.81s. An8-token CPU BF16
versus FP32 diagnostic had per-layer relative activation RMS differences from
0.001361 to0.057669. These are measured differences, not a claim of target-GPU
numerical equivalence or an acceptance threshold. Target-GPU checks remain
required before treating the BF16 pipeline as qualified for training.

No full-size optimizer update, trained checkpoint, GPU pilot, cluster job ID,
measurement curves or trained next-token reconstruction result exists.
Actual training exposure is0. Random initial losses were checked only for
finiteness and are not measurement-quality results. The researcher has not
judged an instrument operating point or answered a scientific question.

## Analysis

The implementation adapts reviewed CrossCoder architecture/initialization and
the existing natural-document processing, checkpoint, DDP and telemetry patterns.
The tokenizer fingerprint module is copied unchanged from the clean trainer.
Old MoE/TopK architectures, packed bins without document boundaries, random
activation-row split and incompatible loss reductions are not reused. All code,
tokens, raw logs and runtime evidence remain execution-side.

Evidence owner:
`/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/`.
Relevant receipts are `docs/local_qualification_20261012.json`,
`docs/tests_20261012.txt`, `docs/input_inventory.json`,
`docs/reference_audit.json`, `docs/asset_access_20261012.json`,
`docs/tokenizer_access_20261012.json`, `docs/data_release.json`,
`docs/source_manifest.json`, `docs/preflight_with_data.json`, and
`docs/submission_dry_run.txt`. The prepared data owner is
`data/pilot_v1/data_manifest.json`, with hashed event payloads and document/
position/shard IDs. No existing research records, sealed splits or asset
catalog entries were overwritten by this task. The default entrypoint check
reported one pre-existing untracked literature path; `--working-tree` found
0 navigation issues and correctly retained the pending-tracking distinction.

Prepared files total29770578 bytes; transient token spool peaked at102958014
bytes. No full activation cache is saved. FP32 model/grad/Adam memory lower
bound is7.00GiB/rank, before Base, DDP and workspaces. A full resumable state
is about5.25GiB; total checkpoint payload ceiling is14GB. GPU peak memory,
activation-generation throughput, training throughput, finish ETA and monetary
cost remain Unknown. CPU qualification duration is not a GPU ETA.

The proposed pilot is488 updates,1998848 exposures, 4×full H100 Reserved and
at most one hour before budget stop, with finalization/save reserves. Its
proposed allocation cost ceiling is4GPU-hours, including up to60s outer
termination cleanup grace; actual consumption must be recorded. No live
capacity or reservation is inferred from the local40GB MIG device or envelope
default. Source/config/data hashes and limits are bound in
`docs/authorization_request_pilot.json`; `researcher_approved=false`.
That request is reviewable and cannot start training. Formal plan is24414
updates,99999744 exposures; it needs pilot-quality and resource/budget confirmation
and does not start automatically. The current2M TRAIN pool would be revisited.

The replacement implementation reports28 single-layer and simultaneous all-layer
comparisons, both with no-op controls. A fixed original-source absolute overwrite
at the highest selected residual dominates earlier replacements. All28 replacement
therefore equals last-block replacement; it is not cumulative-error evidence.
Feature frequency means token occurrence, and zero-hit statistics refer only
to the fixed32768-position validation window.41 validation documents and an
English source do not establish broad multilingual measurement quality.

AI suggestion: approve the concrete bounded pilot after reviewing its frozen
config, data and proposed4GPU-hour resource ceiling. This approval is requested
because the user explicitly required prior approval for new cluster submission.
No automatic formal run or L1 calibration is included. Registration through
the asset lifecycle will be required for actual trained saves; there are none
to register now. Engineering implementation passes local checks; measurement
quality is `NOT_EVALUATED`; scientific answer is `Unknown`.
