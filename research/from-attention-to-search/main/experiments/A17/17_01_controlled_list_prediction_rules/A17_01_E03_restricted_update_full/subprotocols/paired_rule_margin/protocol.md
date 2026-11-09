# A17_01 E03 supplemental Protocol: paired-rule margin

[中文](protocol_cn.md)

State: `APPROVED_FOR_IMPLEMENTATION_SMOKE_AND_FULL_ANALYSIS`.
Owner: parent problem_key `list_rule_shared_update`, E03 supplemental analysis, sub Anchor A17_01_01. No fourth core experiment. No new training or SAE.

## Authorization and audit ledger

2026-10-10 researcher: “没问题，那就执行吧。完成 sub anchor 和 sub protocol 的书写，然后进行执行。现在开始，可以使用4卡H100 reserved计算资源”. This accepts the discussed paired-margin diagnostic and authorizes formalization and execution. Exact replay/readout settings below are delegated operational choices, not separately researcher-adjudicated scientific findings. A–G are confirmed within that accepted scope; scientific result interpretation/closure remain Unknown. Publication and Git operations are not authorized.

| Block | State | Audit basis |
| --- | --- | --- |
| A Question/boundary | CONFIRMED | Accepted same-list FIRST/LAST diagnostic; local relative selection only |
| B Data/provenance | CONFIRMED | Reuse registered selection-v2 heldout dev, independent source groups; no test access |
| C Task/supervision | CONFIRMED | Existing visible rule, one-token answer; no new supervision |
| D Architecture | CONFIRMED | Adopted Qwen direct final o_proj; complete native FP32 reader |
| E Objective/optimization | CONFIRMED | No training; replay saved actual updates with exact restoration |
| F Comparison/evidence | CONFIRMED | Paired update/no-update margin and CE, source qualification, rival controls |
| G Execution | CONFIRMED | Authorized four H100 reserved; internal four-worker Smoke gate before Full |

Cross-block consistency: PASS. Same fixed paired lists, exact updates and complete native forward expose the named uncertainty; no test truth or SAE proxy enters. Resolution checks are engineering-only. This exposed-development follow-up is frozen before its own execution, not presented as blind confirmation.

## A. Question, hypothesis and permitted claim

Question: when source learning helps recipient answer loss, does correct-versus-other-rule answer preference improve? H1 predicts a positive recipient margin effect. R1 is candidate-pool probability adaptation without that relative improvement. R2 is a position bias common to both prompts; paired separation checks its identical additive case. R3 is pair-margin improvement without beating the middle word/full vocabulary. Allowed claim: a bounded local prediction effect from a specified actual matrix intervention. Internal rule algorithms, general transfer, SAE mechanisms and expert architecture utility are outside scope.

## B. Inputs and independence

Input registry IDs and fresh strict access receipts are in execution `provenance/input_access.json` and `partial_input_access.json`; exact file hashes in `required_input_hashes.json`. Required IDs: official Qwen Base/tokenizer; data_a17_list_rules_v1; data_a17_raw_sae_list_analysis_selection_v2; three E03 direct-adapter u100 assets; Qwen29/43 analysis payloads; Qwen71 u0/u16 payload and u100 partial-recovery matrix payload. The u100 partial payload supplies saved matrices only: incomplete prior intervention output is not evidence here. Its exact bytes are independently replayed through the full native reader.

Reuse 120 selection-v2 heldout dev rows/60 FIRST–LAST pairs. Source batches0–4 per rule each contain20 answers, balanced over20 answer words. Source and recipient unordered content groups are disjoint. Existing source batches2–4 were heldout in prior analysis; batches0–1 were discovery. Both sets have now been exposed and are not blinded. Freeze source IDs, recipient IDs, data/selector hashes, checkpoint/manifest hashes and all280 matrix hashes. Do not read test.jsonl.

Pair unit: one ordered list, with both rule prefixes. Verify distinct words, exact list equality across rules, correct target IDs, complete pairs, group independence and answer-ID mapping. Recompute actual training exposure from checkpoint-specific optimizer-step ledgers, check against prior audit, and retain nominal panel labels. Report nominal order_new/combination_new, actual seen-group-unseen-order/unseen-group-in-this-round, and combined. Count pairs/groups; do not count pairs as independent training seeds.

## C. Prediction task

Input is the existing rule/list prefix through the answer marker, excluding completed answer. Prediction unit is one answer token. FIRST target is item1, LAST target is item3. Existing Qwen tokenizer and stored input IDs are reused without re-tokenizing prompts. The rule/list candidates are allowed input. Oracle/tokenization admission follows the registered dataset and its checks, plus exact answer mapping and pair checks here. Invalid inputs stop execution rather than being silently dropped.

## D. Model, states and intervention

Exact official Qwen3-0.6B Base disk identity is checked by the reused carrier. Load FP32, eval mode, SDPA, no sampling/dropout, TF32 off, deterministic algorithms and CUBLAS workspace configuration. Complete model forward and final answer logits are used; no SAE, reconstructed activation or tail-only replay.

Restore only layer27 Attention `o_proj.weight` (1024×2048) from each exact E03 direct checkpoint; all other weights stay at the official parent. States: one Base u0, and u16/u100 for training seeds29,43,71 (7 unique states). Base is deduplicated. Per-state treatment: FIRST/LAST × b0–b4 × eta{0.001,0.01} × multiplier{1,0.5}, 40 saved strict actual FP32 matrices. Total280. Recreate `(W0+delta)-W0 == delta` exactly; verify finite shape/dtype, source metadata, restored matrix and non-target frozen-weight digest. Restore before every independent condition.

## E. Objective and optimization

No optimizer, new gradient, learning trajectory, LM/SAE training or checkpoint selection. Apply existing actual delta; eta/multiplier are provenance labels, not re-estimated updates. Every endpoint is deterministic and paired to its exact no-update baseline. Readout batch20 answers; four workers process disjoint states, without DDP. Numeric reads use FP32 logits and FP64 logsumexp/differences. CE is nats/answer, arithmetic mean over equally weighted records. List-level separation uses equal pair weights. Pool-mass/conditional-CE identity is exact under the same logits.

Training telemetry/resume provisions are NOT_APPLICABLE because training_updates=0. Analysis instead saves exact endpoint logits for20 answer words, full-vocabulary lognormalizer/top1, metrics, finite condition counts, elapsed time and exact source/config/input manifest. No new saved-model checkpoint is claimed.

## F. Measurements and decision branches

For each list: m_FIRST=z(first|FIRST)-z(last|FIRST); m_LAST=z(last|LAST)-z(first|LAST); S=m_FIRST+m_LAST. Report before/after/delta for each. Also correct-minus-max(other two list words), list-restricted top1, full-vocabulary top1, CE, conditional20 CE and log20-pool mass. Store raw per-record and per-pair values, plus separate/combined panel aggregates.

Primary descriptive slice: u16, eta0.01, multiplier1, b2/b3/b4, both directions, seeds29/43/71. Six seed×source-direction cells each contain three source batches. Publish all three values and their mean; no p-value or population CI. Sensitivity: b0/b1, u0/u100, smaller eta and half multiplier. Preserve signs and qualification; do not select better-looking conditions.

Compute deterministic baseline twice. Any nonzero repeated readout drift stops the run. Per-metric resolution eps=max(1e-6,10×measured repeat drift); separation epsilon is twice margin epsilon. The threshold is numerical, not substantive. Source qualification: independent source-rule recipient-set mean CE change < -eps_loss. Recipient help: other-rule mean CE change < -eps_loss. Classify effective/helping updates by margin delta >eps, <-eps or unresolved. Ineffective source and unresolved recipient help are separate statuses; don't convert them to conflict.

Descriptive support for consistent local pair-margin improvement requires every batch in all six primary cells to be effective, recipient-helping and margin-improving. Otherwise report heterogeneous/insufficient, with the exact negative or unresolved cells. Loss help plus non-improving margin contradicts the broad inference that every loss improvement improves this relative choice; it does not by itself prove pool mass is the sole source. Positive S does not excuse recipient harm, and positive pair-margin does not imply higher top1. Mechanism judgment remains Unknown.

Engineering examples required locally: uniform answer-word lift (loss can fall, margin unchanged); identical positional bias under both prompts (margins oppose, S unchanged); loss drop with worse pair margin; positive pair margin while middle word wins; missing pair rejection; CE decomposition identity; nonfinite rejection. These are implementation tests, not empirical discoveries.

## G. Execution, gates and artifacts

Resource profile `h100-4-reserved`; image key `shphd-lite-0911`; resolved tuple/image/mount from docs/execution_envelope.md via canonical submission template. Reuse the inspected mounted Transformers layer and runtime, with CUBLAS deterministic setting added. No environment installation. One node/four GPU workers; two-hour wall ceiling. No fallback profile or second live job. All source/config/protocol/input hashes are checked before execution; immutable run root and writer lock prevent overwrite.

Internal Smoke: four workers each load one checkpoint; select four paired lists from each nominal panel (eight pairs/16records); replay FIRST/LAST b2 eta0.01 multiplier1 (two conditions each, eight total). Require four H100 devices, finite native outputs, exact no-op/restore, source identity, matrix fidelity, non-target frozen weights and complete pair metrics. Only four successful Smoke receipts allow Full workers to start. Full: seven states,120rows/state,280finite conditions. Smoke success certifies engineering only.

Any missing/mismatched input, source overlap, nonfinite value, non-deterministic no-op, wrong GPU/device count, matrix/restore/frozen-weight failure, process error or wall timeout stops the job. Preserve logs and partial results; retry only after inspecting existing job/output, with a distinct recovery root and amendment for material change. Do not silently replace scientific input or count failure as scientific non-support.

Expected outputs: freeze/config snapshots, environment/execution certificate, four Smoke and four Full worker receipts, qualification receipts, seven state summaries, baseline/endpoint NPZ, condition per-pair JSONL, results.json, payload_manifest.json, completion.json and bounded startup receipt. Execution root: /data/250010109/MoE_Router/experiments/20261010_a17_paired_rule_margin. Run root gets UTC identity under runs/. Code reuse: adapted Qwen loader/restore/collate from 20261010_a17_raw_projection_sae/source/carriers.py; removed unused S7/SAE/tail functions. Complete native inference is retained. Runtime reused from 20261010_a17_projection_full/source/runtime.sh. New margin computation/replay receives seven local tests and four-GPU Smoke.

Monitoring: /root performs bounded startup and first progress verification, reports job ID and measured ETA when available, then stops polling unless requested. Platform success alone is insufficient: verify condition coverage, receipts, endpoint counts/hashes, restored/frozen weights and manifest before claiming engineering completion. Register actually saved analysis outputs; produce bilingual E03 supplemental Summary/Detailed after verified completion. Researcher owns scientific adjudication. No commit/push/publication.

## Pre-run freeze and post-start record

Canonical scientific body above is frozen by a run-local snapshot and SHA256 before launch. Execution observations are appended here or in Detailed; do not rewrite the pre-run contract. Any material change requires an explicit amendment and evidence-eligibility note.

### Execution receipt (2026-10-10T14:12:45.060800+00:00)

Job `pt-hz9kc697`; platform `QUEUEING`. Runtime gates pending. [Detailed](detailed.md) records mutable execution observations; the run-local pre-start Protocol snapshot remains frozen.

### Bounded startup outcome (2026-10-10T14:13:43Z)

Four Smoke workers PASS; Full auto-started;50/280 completed at the last observation. Runtime H100/profile/image verified. Monitoring stopped after first progress. Full completion remains unverified; no design amendment.

### Verified completion (2026-10-10T14:45:45.395007+00:00)

Job pt-hz9kc697 SUCCEEDED;Smoke8/8 and Full280/280 PASS;7 states;330 frozen input and642 payload hashes matched. Registered output `representation_a17_paired_rule_margin_20261010t141041z`. [Summary](summary.md) records the unchanged frozen descriptive verdict; human mechanism/closure Unknown. No amendment/retry.
