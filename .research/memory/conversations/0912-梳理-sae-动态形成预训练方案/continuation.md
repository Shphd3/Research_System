# Continuation Brief: Dense LM + SAE pretraining — implementation preparation

```text
Workstream:     Random-initialized Dense LM / last-layer SAE observation preparation
Problem key:    none confirmed; do not register an inferred key
Role:           PRIMARY within this preparation request; no project priority change
Record:         .research/memory/conversations/0912-梳理-sae-动态形成预训练方案/
Continues from: none
Supersedes:     none — first brief for this preparation workstream
Updated at:     2026-09-12T06:18:39Z
Status:         CURRENT
Non-canonical:  points at owning sources; owns no claim, approval, verdict,
                or scientific next decision. Every implementation choice below is proposed.
```

## A. Environment roots

| Root | Path | Readable here? |
| --- | --- | --- |
| Repository | `/data/250010109/Research_System` | yes |
| Execution workspace | `/data/250010109/MoE_Router` | yes |
| Preferred engineering source | `/data/250010109/Research_System/Projects/decommon-router-training` | yes; ignored by root Git |
| Evaluation source | `/data/250010109/Research_System/Projects/decommon-router-evaluation` | yes; ignored by root Git |
| Frozen data view | `/data/250010109/training_data_views/dclm_pair_v1` | yes |
| Tokenizer asset | `/data/share/Qwen3-0.6B-Base` | yes; also contains weights that must not initialize this LM |
| Historical engineering record | `/mnt/bucket/MoE_Router/experiments/active/exp_hierarchical/2026-05-05-real_dclm_qwen3_hier_moe` | yes; existence checked, results not re-audited |
| Proposed new execution directory | `/data/250010109/MoE_Router/experiments/20260912_dense_sae_pretraining` | not created |

Current interpreter has no transformers distribution. Do not install into the base environment. rg is unavailable; scoped find/grep were used. No current GPU node was acquired or queried. The execution envelope identifies future approved resources; its existence is not approval.

## B. Read list — in order

Paths below are absolute or relative to the repository root declared in A. Resume this conversation by reading memory.md completely first.

| # | Path | Answers which question | Required? |
| --- | --- | --- | --- |
| 1 | `AGENTS.md` | Current authority, code placement, human scientific ownership | yes |
| 2 | `docs/training_reuse_index.md` | Which actual engineering sources must be inspected before implementation | yes |
| 3 | `daily_research_reports/0912/docs/resources/01_Meeting_Transcript_Advisor_Intent_cn.md`, segments 079–099 and section 2 | Meeting intent and its transcription boundary | yes |
| 4 | `daily_research_reports/0912/docs/resources/05_Pretraining_Plan_Compute_Budget_cn.md` and `06_Online_SAE_Architecture_Design_cn.md` | Proposed architecture, losses, sampling and checkpoint schedule | yes, design references only |
| 5 | `daily_research_reports/0912/docs/resources/04_Hypothesis_Falsification_Framework_cn.md` and `07_Experiment_Protocol_Analysis_Playbook_cn.md` | What the researcher must decide; fixed panels and cross-readout definitions | yes, not approved Protocols |
| 6 | `Projects/decommon-router-training/docs/source_audit.md`, its README.md, and actual files in H | Engineering reuse and mismatches | yes |
| 7 | `docs/execution_envelope.md` | Future resource/image/runtime/submission authority | required before any GPU-stage planning is finalized |
| 8 | A newly researcher-confirmed Focus/Anchor/Protocol, if created after this checkpoint | Approved scientific question and exact formal-run scope | required before formal execution; absent in this preparation stage |

Do not use old SFT/router protocols to authorize the Dense pretraining task. No existing result Summary for this new experiment was identified; 0912 resource 07 is explicitly a draft. Read 03/08 only for needed explanatory context; no need to reopen unrelated workstreams or research graphs.

## C. Authority and boundaries

- Current request authorizes read-only inspection, proposal preparation, and this memory/continuation checkpoint only. Source: current researcher instruction, pending any later canonicalization; it is a restriction, not inherited execution approval.
- Researcher wording: “当前阶段只允许只读检查、整理和提出方案，未经我再次明确批准，不修改正式代码、不运行大规模实验、不提交任务。”
- Researcher wording: “不要自行决定科学假设，不要主动增加复杂 loss、router、MoE 或额外模块。”
- No implementation, smoke execution, dependency installation, benchmark, formal training, submit, commit, push, graph edit or external sync is authorized by this brief. Stop at the completed proposal.
- Open scientific decisions: intended semantic/classification relation and independent labels; expected change, rival and falsifier; insufficient branch; stable problem key and next scientific decision. Engineering approval need not silently decide these.
- Open engineering decisions: accept the proposed 313M/8192/32 observer, dataset/view limitations and prefix ordering, checkpoint policy, local implementation+CPU smoke scope, separate four-H100 benchmark scope. Final token/time budget is unapproved; 0912's 32-hour table has not started.

## E. Action list — conditional resumption, no authorization from this list

| # | Action | Verify | If pass | If fail |
| --- | --- | --- | --- | --- |
| 1 | Read | Current researcher instruction and B sources | Determine the actually authorized stage | Preserve restrictions and stop dependent work |
| 2 | Implement | Only after explicit local-code approval; use H first, record source hashes | Build proposed isolated package and CPU smoke | Report failure, do not start GPU work |
| 3 | Qualify | Only after explicit benchmark approval; resolve current envelope and fixed budget | Record bounded four-H100 timings and recovery receipt | Stop; no automatic architecture/sampling/profile change |
| 4 | Report | Code/test evidence and benchmark limits, if those stages were approved | Return for the researcher's formal-run decision | Record unknowns; do not substitute microbenchmark for evidence |

No monitor or completion marker exists because no run was submitted. Future completion must come from the authorized stage's persisted terminal receipt and actual artifacts; scheduling/accepted submission is not completion.

## F. Current state and reviewable proposal

### Audited state

- Done: current instructions, minimal 0912 materials, training reuse index, clean train/data/checkpoint/model/tokenizer/health/provenance sources, old binary loader and E16 SAE capture/training sources, and 0912 model/SAE/analysis/test source inspection.
- Done: static AST parsing of all 15 draft Python files, with no module import/test execution. The expected model/analysis/data/utils/scripts directories are all absent. The source-shape parameter calculation is LM 312,892,928; SAE 16,786,432; combined 329,679,360. This is not a live-model or throughput qualification.
- Done: frozen data-view manifest SHA-256 `8a91bdbb0eb537bd80612015b99f178ca1cbb54a2fa7cf8442ab1eae7f0a2f2d`; 2,419 linked training files, 302,089,493,820 uint32 IDs, matching path/size/target checks. Validation is excluded. No whole-corpus content hash or document/probe decontamination proof was produced.
- Pending: usable package layout; Dense-only trainer; target-alignment adapter; independent SAE optimizer grouping/clipping/randomness; complete paired recovery; panel and analysis manifests; real-data validation and bounded benchmark driver. Independent frozen-checkpoint SAE refitting is a later analysis driver, not an automatically authorized extra run.
- Material source mismatch: clean loader returns already shifted `(source, target)`; draft `_ce` shifts again. Clean trainer jointly clips all parameters and depends on `router_blocks`, MoE outputs and retired pair contracts. Draft sampler is a fixed residue mask in the microbenchmark; its optimizer also differs from the proposed LM/SAE groups. Its model-only `model.pt` save is incompatible with clean trainer `state.pt` without an adapter. Clean checkpoint RNG capture omits dedicated Generator states. SAE counters require global aggregation without recounting.
- Historical E16 SAE was fitted to a frozen pretrained LM at a final-block MLP pre-hook, not the final block output after final RMSNorm. Its centering, normalization and loss differ; its 30,000-wide checkpoints and grouping are not compatible initial states for the proposed observer.
- Root Git had pre-existing edits/deletions/untracked files. No code, research state or prior memory log was altered in this turn. No job ownership is being transferred.

### Proposed minimal implementation (unapproved)

- Baseline: retain the native Qwen3-style reference from 0912, random initialization only; 10 Dense blocks, hidden 1024, FFN 3072, Q/KV heads 16/8, head_dim 128, context 2048, vocab 151936, tied embeddings, seed 17. It is not claimed numerically equivalent to official upstream. Reuse the local tokenizer only. No default distillation, feedback, bottleneck, router, MoE or extra loss.
- Representation: last complete block residual r; h=final RMSNorm(r); language logits use h. The sparse autoencoder reads detached h in a side branch, width 8192, at most 32 positive entries. Use the draft's per-position normalized reconstruction error, with detached target and denominator. Only LM next-token loss reaches LM parameters; only reconstruction reaches SAE parameters. Both parameter sets train. Analysis and evaluation update neither parameters nor SAE counters.
- Optimization: one AdamW with disjoint LM matrix / LM bias-norm / SAE parameter groups; LM LR 3e-4, betas (0.9,0.95), matrix decay 0.1 and bias/norm decay 0; SAE LR 1e-3, betas (0.9,0.999), decay 0. Clip LM and SAE separately at 1.0. These are engineering defaults from 05, not an optimized recipe. LM token-based 20M warmup then plateau; SAE LR fixed. No short-run cosine end-point inherited from the old trainer.
- Train batches: clean loader's aligned `input_ids[B,S]` and `target_ids[B,S]`; model must not shift them again. S=2048 means 2048 eligible predictions for a full unmasked sequence. Target mask excludes invalid targets; denominator counts eligible predictions, not raw input length. Fix ordered manifest/prefix and sampler cursor; old sampler's whole-corpus block shuffle must not silently replace a declared sequential prefix.
- Four-rank data parallel starting point: 2 sequences/rank, S=2048, 16 accumulated microbatches, giving 262,144 eligible predictions/update when fully populated. BF16 autocast and FP32 loss/norm statistics. Sum local LM and SAE numerators; normalize with each loss's global count across all ranks and all accumulated microbatches. Use no_sync on non-final microbatches. One SAE optimizer update per LM update; draw approximately 1/8 eligible training positions through its own rank-specific Generator. Save actual sample counts. Keep initialization/data/SAE-sampling/evaluation randomness separate.
- Checkpoints: retain paired LM+SAE at targets 0, 1M, 4M, 16M, 64M, 256M, 512M, 1B, 2B, 4B eligible prediction tokens, only if reached within an approved budget. Save at actual completed optimizer boundaries and record target plus actual counts. Beyond 4B is not currently proposed for execution; 05's 1B extension cadence is only a future reference. Additionally save a rolling recovery point every 30 minutes and on orderly exit/preemption, keeping two rolling points. Every retained point includes optimizer, scheduler, cursor, per-rank RNG including dedicated Generators, global SAE counters, tokens/updates, data/tokenizer/config/source hashes. Manifest last, atomic files; rank 0 writes one model/optimizer state and each rank writes its RNG. Resume requires the same four-rank topology unless separately qualified.
- Observation storage: at each retained point, run eval/inference on the exact same bounded prefix panel, proposed at most 2048 records for the first interface. Save the predeclared causal prediction position per record: r, h, reconstruction as FP32 [N,1024], sparse IDs int32 [N,32], positive values FP32 [N,32], selected token ID, sample ID/position and split metadata. Save zeros among Top-K entries correctly and count actual positive entries. Per-step logs keep aggregate reconstruction, activity and coverage counts; do not store every training token or dense [N,8192] codes. Tokenized panel is saved once. Optional future SAE-fit data must have its own train-only position manifest; confirmation examples must not fit the reader.
- Timestamp semantics: save paired state after both optimizer updates (and state 0 before any update), then extract panel r/h/z from those exact parameters; do not attach pre-update training activations to a post-update checkpoint. Restoring eval/train flags and RNG must leave the continuation trajectory unchanged.

### Proposed analysis input/output contract

- Build panel: researcher-validated JSONL fields `sample_id,prefix,relation_label,format_label,block_id,split`, optional validated continuation. Output one NPZ per discovery/calibration/confirmation split: `input_ids[N,S],attention_mask[N,S],positions[N],sample_ids[N]`, metadata and optional `expected_next_ids[N]`. Store source/tokenizer hashes. Reject duplicates, mixed split content blocks, silent truncation, invalid positions and answer-in-input leakage. No labels invented by the agent; shape-only smoke uses explicitly artificial fixtures.
- Collect: `checkpoint manifest + fixed panel NPZ -> activations NPZ + activation manifest`. Manifest joins run ID, actual LM tokens/update, LM checkpoint hash, SAE checkpoint hash/sample budget, panel/tokenizer hash, position and layer semantics, precision and schema version. Use reconstruction to reproduce qualification statistics; use r to distinguish scale changes around final normalization.
- Statistics: `activations + dictionary width -> statistics.json`, including actual L0, per-feature support, panel activity coverage and reconstruction error relative to centered variance. Never-fired-on-panel is not permanent deadness. Default grouping is disabled; do not inherit 8 as a natural class count.
- Evolution: `early/late activations + early/late paired checkpoints -> cross_readout.json and trajectory metrics.csv`. Verify sample IDs/order/positions/panel hash and schema. Evaluate H_a/E_a, H_b/E_a, H_a/E_b, H_b/E_b from saved h with either SAE; report relation changes without additive causal percentages or direct cross-checkpoint neuron-identity claims.
- Semantic audit, only after relationship approval: `activations + validated triplets CSV(anchor_id,positive_id,negative_id,block_id) -> descriptive h/z margins, covered counts, block-level uncertainty`. Do not automatically convert a statistic into a scientific verdict. Grouping/q and functional interventions remain disabled unless separately scoped.

### Proposed files and responsibilities

All paths below are planned additions in the new execution directory; none has been created. Preserve the 0912 imported source bundle and old projects as references. Namespace package imports explicitly; record copied/adapted source hashes in the new README/manifest. Do not add a parallel scientific design.md.

| Planned absolute path | Responsibility |
| --- | --- |
| `/data/250010109/MoE_Router/experiments/20260912_dense_sae_pretraining/README.md` | Scope, source/reuse audit, verified commands and I/O map after qualification |
| `/data/250010109/MoE_Router/experiments/20260912_dense_sae_pretraining/pyproject.toml` | Installable package and pinned qualified dependency layer; replace broken imports |
| `/data/250010109/MoE_Router/experiments/20260912_dense_sae_pretraining/configs/observer.json` | Proposed Dense/SAE/data/checkpoint/optimizer settings; no implicit formal token-budget approval |
| `/data/250010109/MoE_Router/experiments/20260912_dense_sae_pretraining/dense_sae/model/configuration_qwen3_sae.py` | Strict serialization; only none/observer modes in first execution package |
| `/data/250010109/MoE_Router/experiments/20260912_dense_sae_pretraining/dense_sae/model/modeling_qwen3_sae.py` | Adapt native Dense backbone, aligned-target chunked loss, final r/h and detached observer |
| `/data/250010109/MoE_Router/experiments/20260912_dense_sae_pretraining/dense_sae/model/sae.py` | Reuse draft Top-K encoding, normalized decoder, sparse outputs and reconstruction objective |
| `/data/250010109/MoE_Router/experiments/20260912_dense_sae_pretraining/dense_sae/data.py` | Adapt clean packed loader/sampler, frozen ordered prefix, valid-target masks and recoverable cursor |
| `/data/250010109/MoE_Router/experiments/20260912_dense_sae_pretraining/dense_sae/data_contract.py` | Reuse manifest/path/size/heldout checks; state limitations of content provenance |
| `/data/250010109/MoE_Router/experiments/20260912_dense_sae_pretraining/dense_sae/tokenizer_contract.py` | Reuse tokenizer-only identity hashing, excluding pretrained weights |
| `/data/250010109/MoE_Router/experiments/20260912_dense_sae_pretraining/dense_sae/train.py` | Adapt DDP runtime, LM/SAE groups and independent clipping, counted accumulation, token schedule, validation, logging and stop boundaries |
| `/data/250010109/MoE_Router/experiments/20260912_dense_sae_pretraining/dense_sae/checkpoint.py` | Adapt atomic DDP paired saves/load, optimizer/scheduler/cursor and dedicated rank RNG, retention and manifests |
| `/data/250010109/MoE_Router/experiments/20260912_dense_sae_pretraining/dense_sae/health.py` | Reuse finite-loss/gradient and recoverable health checks, without inheriting old scientific thresholds |
| `/data/250010109/MoE_Router/experiments/20260912_dense_sae_pretraining/dense_sae/analysis/build_probe_panel.py` | Adapt existing prefix-only panel builder and stronger identity/split checks |
| `/data/250010109/MoE_Router/experiments/20260912_dense_sae_pretraining/dense_sae/analysis/collect_activations.py` | Adapt paired checkpoint reader, bounded fixed-position r/h/z/reconstruction export |
| `/data/250010109/MoE_Router/experiments/20260912_dense_sae_pretraining/dense_sae/analysis/feature_statistics.py` | Reuse reconstruction/activity diagnostics; grouping disabled by default |
| `/data/250010109/MoE_Router/experiments/20260912_dense_sae_pretraining/dense_sae/analysis/representation_evolution.py` | Reuse fixed-sample relation metrics and four cross-readout combinations |
| `/data/250010109/MoE_Router/experiments/20260912_dense_sae_pretraining/dense_sae/analysis/feature_semantics.py` | Reuse external-triplet descriptive statistics only; require researcher-validated relation, omit intervention path |
| `/data/250010109/MoE_Router/experiments/20260912_dense_sae_pretraining/dense_sae/analysis/run_analysis.py` | Thin checkpoint/panel manifest driver, schema checks, trajectory JSON/CSV and optional plots |
| `/data/250010109/MoE_Router/experiments/20260912_dense_sae_pretraining/dense_sae/benchmark.py` | Bounded four-rank benchmark through actual training step, none/observer comparison and I/O-inclusive qualification |
| `/data/250010109/MoE_Router/experiments/20260912_dense_sae_pretraining/scripts/runtime.sh` | Activate researcher-approved runtime layer; no base-environment install |
| `/data/250010109/MoE_Router/experiments/20260912_dense_sae_pretraining/scripts/run_train.sh` | Explicit torchrun entrypoint, no submission or automatic formal-run continuation |
| `/data/250010109/MoE_Router/experiments/20260912_dense_sae_pretraining/tests/test_pipeline.py` | Small CPU end-to-end contract tests adapted from draft tests and clean checkpoint/data tests |
| `/data/250010109/MoE_Router/experiments/20260912_dense_sae_pretraining/tests/distributed_smoke.py` | Two-rank CPU Gloo counted-accumulation/state/cursor parity; GPU topology checked only in approved benchmark |

Also add package-only `__init__.py` files at `/data/250010109/MoE_Router/experiments/20260912_dense_sae_pretraining/dense_sae/__init__.py`, `/data/250010109/MoE_Router/experiments/20260912_dense_sae_pretraining/dense_sae/model/__init__.py`, and `/data/250010109/MoE_Router/experiments/20260912_dense_sae_pretraining/dense_sae/analysis/__init__.py`. No formal repository scientific artifact is in the current edit scope. Independent SAE-refit trainer and grouping driver are explicitly later scope, if the researcher selects that analysis.

### Proposed minimum smoke and 4×H100 benchmark (not executed)

- CPU smoke after local implementation approval: bounded at 5 minutes, no CUDA, tiny vocab 47 / hidden 24 / 2 blocks / Q-KV heads 4-2 / head_dim 8 / SAE width 64 / k=4 / short unequal-length sequences. Check imports/config validation and metadata-only full-shape count. Check actual next-token targets (no double shift), future-token causality and padding. Compare no-observer versus observer backbone gradients AND post-step parameter deltas with matched initial weights/data, verify all LM parameters and SAE membership, isolated SAE-only gradients and separate clipping. Check actual positive sparsity and finite/decreasing toy-batch loss as implementation evidence only.
- CPU accumulation/recovery: compare unequal microbatches and two Gloo ranks with one equivalent concatenated batch, with separate exact LM/SAE denominators. Compare uninterrupted 8 updates with 4+save/reload+4, including model/optimizer, sampler next IDs, sampling masks, counters and RNG. Exercise one fixed panel through collect/stats/cross-readout; prove inference leaves state and subsequent training unchanged. CPU determinism is expected; BF16 GPU uses an explicitly recorded numerical tolerance rather than an invented bitwise claim.
- GPU benchmark requires separate explicit authorization: resolve `h100-4-reserved` and current image/runtime from execution envelope, use its existing submission entrypoint and durable receipt contract. Proposed hard cap: 60 minutes from runtime start, 4 GPUs (at most 4 GPU-hours), no retries/resubmission or formal continuation without instruction.
- Benchmark first uses identical saved LM initialization and input schedule for none/observer; 4 ranks, per-rank batch 2, S=2048, accumulation 16, actual optimizer groups and BF16 path, 10 warmup + 30 timed optimizer updates each. SAE uses the independent random 1/8 sampler, not the draft's fixed stride. Record per-update synchronized max-rank time (including p50/p95), aggregate eligible prediction tokens/s, max allocated/reserved memory, measured observer overhead and separate sampled component timings. Instrumented component timing is identified separately from ordinary step timing.
- Then at most 100 actual-DCLM observer updates through the same trainer, including a checkpoint+same-topology resume, fixed held-out validation batch and a bounded panel extraction. Count I/O/save/load/evaluation wall time separately and end-to-end; report save duration/bytes, data-wait time, global SAE samples, terminal state and all nonfinite/OOM/mismatch failures. All benchmark outputs are disposable qualification artifacts outside the scientific trajectory. If any gate fails or the wall cap is hit, stop and report; do not silently shrink model or change sampling.
- Use measured I/O-inclusive throughput with the 05 plan's 0.8 planning margin to estimate 2B/4B time only after the run. Observer overhead >20% is a trigger to return a sampling/cost proposal, not automatic permission for 1/16 or another run. No measured throughput currently exists for this package, and no 15B/20B or 32-hour commitment is made.

## G. Completion contract

- This preparation is complete when source-backed status, missing components, the above minimal plan/file map/tests/risks, and memory+one CURRENT continuation exist. No successful training result is required or claimed.
- Stop now for explicit researcher approval. Local engineering approval, benchmark approval, and full pretraining approval are different scopes. Missing scientific judgment must remain pending; do not infer it to fill a Protocol.
- Current risks: double target shift, joint clipping affecting the LM, sampler/Generator/counter resume drift, stale pair/launch guards, frozen binary view lacking document-level decontamination, changing online SAE readout confounding representation changes, large-vocabulary loss and checkpoint I/O limiting actual throughput, and old reference sources being ignored by root Git. Proposed full FP32 model plus two Adam moment states are about 4GB/paired checkpoint before ancillary state; ten retained points are about 40GB plus rolling points and outputs. Measure actual serialized sizes before fixing storage limits.

## H. Reusable assets — inspect before rewriting

| Asset | Path | Reuse for | Verified? |
| --- | --- | --- | --- |
| Clean packed loader/contracts | `/data/250010109/Research_System/Projects/decommon-router-training/src/decommon_router/data.py`, `data_contract.py`, `tokenizer_contract.py` | Preferred data/cursor/provenance source, with explicit target/order adaptation | source read; data view path/size targets checked |
| Clean trainer/recovery | `/data/250010109/Research_System/Projects/decommon-router-training/src/decommon_router/train.py`, `checkpoint.py`, `health.py` | DDP/accumulation pattern, atomic files, rank RNG, recovery and finite guards | source read; MoE/pair/clip/scheduler coupling identified; no new tests run |
| Draft Dense and observer | `/data/250010109/Research_System/daily_research_reports/0912/docs/code/configuration_qwen3_sae.py`, `modeling_qwen3_sae.py`, `sae.py` | Architecture and existing observer objective; copy/adapt only after approval | complete source read, AST valid; not an installed package |
| Draft analysis/tests | `/data/250010109/Research_System/daily_research_reports/0912/docs/code/` | Fixed prefix builder, collect, sparse statistics, relation drift, external triplets, CPU test cases | source read; package layout/driver/provenance gaps identified |
| DCLM and tokenizer | `/data/250010109/training_data_views/dclm_pair_v1/manifest.json`; `/data/share/Qwen3-0.6B-Base` | Existing uint32 token assets and tokenizer identity; never pretrained initialization | view hash and path/size/target checks; local config read; no decontamination proof |
| Old SAE source | `/data/250010109/MoE_Router/experiments/20260903_a15_13_e16_dclm_final_layer_sae/sae_core.py`, `train_sae.py` | Historical comparator only; rejects blind reuse of hook/weights/auxiliary objective | relevant source read; capture-location and objective mismatches established |
| Old 0911 analysis | `/data/250010109/MoE_Router/experiments/20260910_sft_routing_representation_full_matrix/audits/0911_minimal_followup/sae_analysis.py`, `replay_sae.py` | Cross-readout/trajectory implementation reference | entrypoints inspected; hard-coded SFT/router paths and answer positions not reused |
| Evaluation project | `/data/250010109/Research_System/Projects/decommon-router-evaluation/src/decommon_eval/run_validation_loss.py` | Weighted held-out evaluation and immutable-state checks | source read; model adapter is MoE-specific, not drop-in |
| Execution/continuation templates | `/data/250010109/Research_System/docs/execution_envelope.md`; `/data/250010109/Research_System/templates/research_process/continuation_brief_template.md` | Existing submission authority and operational continuity format | read; no submission invoked |

These assets establish available implementation material, not scientific evidence or execution approval. Record source hashes before reuse; do not re-implement their working primitives without an identified interface reason.
