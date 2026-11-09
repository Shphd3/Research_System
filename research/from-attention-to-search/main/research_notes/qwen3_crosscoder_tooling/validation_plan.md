# Frozen Qwen3 CrossCoder: A12 audit and execution recommendation

[中文](validation_plan_cn.md). Updated2026-10-13 UTC. Historical A08–A10 plan
is preserved execution-side in `docs/revisions/A12_before_14layer_audit/`.
This is a measurement-tool engineering note, not a new scientific Anchor.

**Current answer (A15,2026-10-13):** the researcher selected direct reuse of
existing S7 DCLM bins. A small offset view is built and registered:1B eligible
TRAIN positions and10,485,760 VAL positions in disjoint source files. It took
47.5s without re-tokenization or token-payload copying. Original-document and
near-duplicate split separation are UNKNOWN and no longer a preparation gate.
Job **pt-68ys31o7** is submitted on4xH100 Reserved for fresh14-layer/F16384
smoke followed by pass-gated formal training. Formal optimizer startup is not
yet verified. Earlier A12 preparation statements below are historical; A15
supersedes their raw-document recovery requirement. Measurement quality remains
UNKNOWN.

## Purpose

Measure comparable sparse features across sampled depths of a frozen
Qwen3-0.6B Base. One example means the same document and token position
in every selected layer. Fourteen layers do not create14 independent examples.
The proposed instrument covers14 sampled layers; it must not be called a full
28-layer instrument. Execution completion does not establish measurement quality,
feature causality, expert routing benefit or feature-emergence time in pretraining.

## Model

Unchanged Base: `/data/share/Qwen3-0.6B-Base`, revision
`da87bfb608c14b7cf20ba1ce41287e8de496c0cd`, weightSHA256
`cd2a512003e2f9f3cd3c32a9c3573f820bb28c940f73c57b1ddaa983d9223eba`.
596,049,920 parameters,28 blocks,H1024,Qwen2TokenizerFast. Freeze all Base
parameters, eval/no_grad/use_cache=False; no router or Base optimizer.

AI recommendation: predeclare block numbers **2,4,...,28**, zero-based indices
1,3,...,27. This uniformly samples architectural depth without outcome-based
selection and includes the final block. It does not prove uniform semantic
spacing or capture features confined to omitted blocks. Block27 residual-post
is the input to the final global norm; other selected block l outputs match
hidden_states[l+1]. Fresh selected-hook verification remains required.

Use independent E[L,H,F] and D[L,F,H], shared bias b[F], decoder bias c[L,H].
With L14,H1024,F16384, each layer has33,555,456 parameters; add16,384 shared
bias parameters once: **469,792,768**. The28-layer/F16384 version has939,569,152;
28-layer/F8192 has469,798,912. Four FP32 parameter/gradient/two-Adam tensors
alone need7.00046GiB/rank; Base, workspaces, DDP and activations are additional.
F16384 is16 times single-layer width and8/7 times the14-layer concatenated
width14336. These ratios describe capacity, not empirical measurement coverage.

TRAIN-only fixed coordinate RMS uses65,536 calibration positions, with saved
inverse scaling. For N paired positions, encode by summing layer encoders then
adding shared bias and ReLU. Reconstruct each selected layer independently.
The exact loss remains:

\[
\mathcal L=\frac1N\sum_{n,l,h}(\hat x_{nlh}-x_{nlh})^2
+\frac{\lambda}{N}\sum_{n,f}z_{nf}\sum_l\sqrt{\sum_h D_{lfh}^2}.
\]

Average over positions; sum hidden coordinates, selected layers and features.
Sum of layer decoder L2 norms, never L2-of-norms. Decoder gradients are retained.
Initialization remains the reviewed L1 transpose-copy implementation at commit
`d1fd6f3fea41fc1123699cc09f4cdad47ca35160`, independent storage, norm0.05 per
layer/feature, zero biases. With14 layers initial summed norm is0.70, previously
1.40. A coefficient0.04 therefore needs a new sparsity check; unchanged coefficient
does not imply unchanged operating point. No unrecorded tuning is authorized.

| Candidate setting | Value |
| --- | --- |
| Shared features / selected layers | 16384 /2,4,...,28 |
| Optimizer | Adam,lr1e-4,betas(0.9,0.999),eps1e-8,weight_decay0 |
| Batch / context / seed | 4096 global positions;4ranks x1024 xaccum1;1024;42 |
| Precision | BF16 Base and GEMMs; FP32 master weights,gradients,Adam,norms,loss |
| Schedule | constant learning rate; no new router/TopK/AuxK/projection |
| L1 | 0.04 provisional at fixed TRAIN RMS and exact objective |
| Formal requested target | 1B unique TRAIN positions, once |
| Complete-batch target | 999,997,440 exposures;244,140 updates;2560 unused positions |
| Validation | fixed10,485,760 positions, never normalization fitting |
| Formal compute recommendation | retain previously selected4xH100 reserved;24h/96GPUh ceiling |
| New14-layer formal ETA | UNKNOWN until target-hardware short smoke |

DCLM cached global01 provides12 selected bins/1,566,635,607 legacy IDs and
3,251,185,248bytes of verified compressed raw text, at
`mlfoundations/dclm-baseline-1.0@a3b142c183aebe5af344955ae20836eb34dcf69b`.
Verify complete original-document prefixes against every cached token and its
appended legacy delimiter; exclude uncached raw suffixes. Do not split text by
special-token occurrences. Preserve document/position/shard IDs. Group normalized
exact text, URL and discovered near duplicates before TRAIN/VAL split and1024
chunks. Bounded near-duplicate candidates are not exhaustive deduplication.
Language metadata indicates English DCLM, not independently certified multilingual
coverage. Raw token counts, unique positions and optimization exposures remain separate.

## Hypothesis

Uniform14-layer sampling may reduce CrossCoder cost while retaining useful
features distributed through model depth. A credible rival is that omitted layers
contain narrow or rapidly changing features that the instrument cannot measure.
The current audit establishes dimensions and mathematical consistency only;
selected-layer fidelity tests cannot settle omitted-layer completeness.

## Conclusion

Observed: old local preparation stopped after1,252,280,824 processed source tokens,
but its temporary spool was unlinked and no qualified data_manifest was saved.
That count is not a usable1B training set. Old local launcher/supervisor are dead;
no formal job was submitted by them. Cached raw sources remain accessible.

Observed:26 new data checks pass, including actual Qwen tokenizer/source-prefix
correspondence, fresh-process restoration, byte-identical TRAIN/VAL payloads,
uncommitted-tail rollback and corruption/source/config rejection. Persistent
checksummed token spool plus two bounded state generations replace temporary
unrecoverable state. Frozen previous math/data/train sources are not rewritten.
The14-layer generic core matches exact parameter counts, hand-calculated loss,
finite CrossCoder gradients and detached activation inputs. Selected-hook real
model extraction and14-layer GPU smoke are NOT_RUN.

Decision authorized by researcher: submit one4xRTX5090Spot data-preparation
allocation. Job **pt-4ulnlmdb** requests56vCPU/240GiB and4GPUs; one CPU producer
uses no CUDA. Six-hour/24 allocatedGPU-hour cap, no automatic retry, extension
or formal submission. Source checks/hashes and submission receipt are durable.
Registration occurs inside the worker only after actual1B TRAIN/10MiVAL data,
correspondence and indices pass. Intended asset:
`data_qwen3_alllayer_crosscoder_dclm_formal_1b_unique_v2`; not registered speculatively.

## Analysis

Alternating layers is a transparent budget tradeoff compared with selecting a
contiguous half. It is not intrinsically more scientifically complete than all28.
Fixed layer index spacing is not fixed representation-change spacing. Retaining
the last block supports final-depth fidelity checks; early layer1 and all odd
blocks remain outside the instrument. No additional28-layer training or offset
ensemble is needed for the present recommendation.

The Base still executes all28 blocks to reach block28. Only CrossCoder matrix
work and selected activation storage approximately halve; whole-run time does
not halve automatically. Historical28-layer H100 step timing implied18–22h
for1B, but is not a measured14-layer ETA. New CPU preparation provisionally
needs4–6h from previous throughput; current worker measurements must refine it.
Money tariff is UNKNOWN. Allocated GPUs during CPU preparation still count
against resource cost; no four-GPU preprocessing speedup is claimed.

AI execution recommendation: finish and register actual data; adapt the selected
extractor, normalizer,14-layer evaluation/replacement and resume contracts in a
separate source revision. Run a short target-H100 check of16 updates/65,536
positions first, then at most the already requested2M-position pilot if needed
for reconstruction/sparsity inspection. Record its budget before submission.
Do not reuse old28-layer checkpoints/scales or claim the earlier H100 smoke
qualifies14-layer training or RTX5090 CUDA. Estimate formal ETA from measured
completed updates plus activation-generation/validation/checkpoint overhead.
Submit the concrete14-layer formal job only after its new engineering contract
and pilot/resource review; do not silently launch the old28-layer entry.

Evaluation retains per-selected-layer normalizedMSE/FVE, globalL0, descriptive
layer contribution, occurrence frequencies, zero-hit fraction and exposure
curves. Zero-hit means no z_f>0 in the explicitly reported fixed VAL window,
not permanent absence. Occurrence frequency is not Fourier frequency. Use fixed
32 distinct-document next-token panels, original/repeat/noop controls and single
selected-layer reconstruction replacement. Fixed-original absolute multi-layer
overwrites are dominated by the highest replaced layer; they are not a cumulative
error or feature-causality experiment. Save config, RMS,manifest,checkpoint,
Adam/RNG/cursors,logs and resume commands; register actual trained saves only.

Execution evidence: [current entry](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/docs/FORMAL_RUN_ENTRY.md),
[candidate config](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/configs/formal_14layer_1b_bf16_candidate.json),
[core audit](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/qualification/14layer_core_audit_A12.json),
[data tests](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/qualification/resumable_data_tests_A12.log),
[execution certificate](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/runs/dclm_prepare_resumable_5090/execution_certificate.md).

## A15 researcher-authorized direct-bin amendment

### Purpose

Remove original-text reprocessing as a prerequisite while retaining reproducible
paired activation measurements. This is an execution/data-contract change,
not a scientific finding or a change to the frozen Base.

### Model

Reuse `/data/250010109/training_data_views/dclm_pair_v1` with its existing
file-separated TRAIN/VAL. Keep the previously selected seed42 TRAIN-bin order;
index only enough eligible positions to reach1B. Exclude tokenizer special IDs
and legacy151645 from training/statistics; retain them as context. Contexts are
contiguous1024-token chunks within one file, and may cross original document
boundaries. Preserve source SHA256 plus absolute token offsets. Compatibility
context keys are explicitly not original document IDs. No new deduplication or
raw re-tokenization is performed. Source token IDs are not copied.

Keep14 even-numbered blocks2–28,F16384,469,792,768 independent CrossCoder
parameters, Adam1e-4/(.9,.999)/eps1e-8/weight_decay0,global batch4096,
TRAIN RMS calibration65,536,lambda.04 under the unchanged norm-sum L1 objective.
Base and matrix compute use BF16; master weights,gradients,Adam and losses stay
FP32. Batch frozen Base forwards over128 contexts, with4GiB activation cap per
rank; this does not change the optimizer's4096-position effective batch.
Feature-statistics validation partitions positions disjointly across four GPUs.
Routine fixed VAL prefix is1,048,576 positions; full window10,485,760 at
approximately.1/.25/.5/.75/1B. Initial validation uses the routine window.
Replacement panel is32 fixed bin contexts, not32 certified distinct documents.

### Hypothesis

Direct-bin reuse preserves same-position cross-layer pairing and permits earlier
training. The credible limitation is cross-split duplicate/document overlap,
which can make held-out quality optimistic. These data cannot establish fresh
independent confirmation or original-document-level generalization.

### Conclusion

Observed: direct-bin view and asset registration passed;20 relevant local tests
passed. Prior CPU data job pt-u4ch7s12 was stopped on the researcher's workflow
switch; its files are preserved. pt-4ulnlmdb failed and was not retried.
Authorized job pt-68ys31o7 requests one4H100 Reserved node. It must pass actual
BF16/FP32 numerical checks,hook pairing,freeze/finite checks,TensorBoard/counting
and fresh-four-process byte-exact next-update replay before formal optimization.
Submission alone is not a passed smoke or a completed training run.

### Analysis

The planned smoke uses135,168 original optimization exposures plus4,096 replay
exposures,below the2M cap. Formal training starts from initialization, not smoke
weights, and consumes999,997,440 positions once. Preserve the499,998,720
checkpoint, full-window statistics and replacement controls for early analysis.
Combined allocation cap is24h/96GPUh; formal cap is23h/92GPUh including teardown.
No automatic retry, budget extension, L1 tuning or omitted-layer claim. Estimate
time from measured generation plus optimizer and evaluation/save overhead.

Execution evidence: amendment `docs/amendment_A15_direct_bin_authorization.json`,
source manifest `docs/source_manifest_A15.json`,config
`configs/formal_14layer_direct_a15.json`,data
`data/direct_dclm_bins_a15/data_manifest.json`,run
`runs/gated_direct_a15/execution_certificate.md` under the execution root.


## A16 observed stop and A17 sparsity review

### Purpose

Check the exact requested ReLU+weightedL1 implementation and avoid committing1B training to an unqualified dense representation.

### Model

14even blocks2–28, shared dictionary16,384,469,792,768 CrossCoder parameters; frozenBase, BF16 GEMMs and FP32 master/Adam/loss. The actual CUDA path already implements the screenshot's sum-of-encoders plus shared bias followed byReLU. The objective remains squared reconstruction summed across layers/coordinates plus0.04 times decoder-norm-sum weightedL1, averaged over positions. No architectural change is required to match the supplied equations.

### Hypothesis

The uncalibrated soft penalty can allow many positive features under this activation scale and reduction. Early density cannot establish a converged operating point.

### Conclusion

A15 jobpt-68ys31o7 failed exact fresh-process replay. A16 used fixed-order gradient reduction and a longer bounded pilot on4H100 Reserved; jobpt-cvgrbthf stopped at its predeclared density guard on2026-10-13T01:47:14Z. After1,839,104 optimization exposures, validation65,536positions yieldedL0=9,313.7078/16,384(56.8464%). Formal1B training has not started. A16 GPU fresh-process replay was not reached; it remains unqualified despite local two-process replay passing.

A16 complete saved state is at1,835,008 exposures and was registered as `crosscoder_qwen3_14layer_16384_bf16_a16_smoke_14layer_direct_a16_1835008_20261013`, explicitly a failed qualification checkpoint. A15+A16 actual exposures total1,978,368. Full A16 layer/replacement statistics were computed in memory but not persisted before the exception; no numerical claims use those unavailable values.

### Analysis

ReLU and L1 implementation checks pass; this does not establish sparse measurement quality. Current positive-feature density remains excessive. The publicly reviewed trainer defaults to unsquared L2 with a different layer reduction, so its numeric coefficient is not a calibrated transfer to this screenshot objective.

A17 proposes three independent L1 bracketing trials0.16/0.64/2.56, at most6M additional exposures including replay,4H100 Reserved up to20minutes. These are candidates, not defaults or confirmed optima. Extra budget is NOT APPROVED and no new job has been submitted. Compare per-layer reconstruction, strict positive-feature counts, frequency, zero-hit fraction and next-token fidelity together. Do not auto-launch formal training from calibration. Execution details: `docs/sparsity_review_A17.md`, `_cn.md`, `docs/sparsity_calibration_proposal_A17.json`, `runs/gated_direct_a16/execution_certificate.md` under the existing execution root. Scientific question remains unanswered.
