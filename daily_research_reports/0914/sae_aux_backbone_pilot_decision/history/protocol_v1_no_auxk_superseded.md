# Protocol: auxiliary reconstruction gradient into the backbone — paired development pilot

## 0. Approval snapshot

Revision: candidate v1, 2026-09-14. **SUPERSEDED_DRAFT_NOT_EXECUTABLE**.

This draft describes the earlier fresh C/T, coefficient-0.1, no-AuxK proposal.
The researcher later requested a T-only engineering Smoke with SAE-only AuxK;
that Smoke is owned by the isolated execution workspace's
`docs/smoke_execution_scope.md` and run-local receipts. This document was not
silently rewritten into a different scientific comparison. A development/full
run still requires one replacement Protocol after the researcher chooses
whether the estimand is the combined T+AuxK intervention against old C or a
fresh AuxK-matched C/T contrast.

This is the single review draft for this pair, temporarily stored in the date folder because canonical project ownership is unconfirmed. The researcher explicitly requested a concrete draft before resolving ownership. No Focus, Anchor, project priority, approval or execution state is created by this document. After ownership is confirmed, move this same contract to the owning experiment directory; leave a pointer here, not a second maintained Protocol.

| Field | Candidate contract |
|---|---|
| Purpose | Determine whether allowing sampled SAE reconstruction gradients into the backbone improves domain readability of the final block's pre-SAE normalized state, and measure language-model cost. |
| Role | Operationalization / proxy test of an explicitly requested gradient intervention; not an established semantic mechanism. |
| Primary Anchor / Focus / stable problem_key | **BLOCKED: researcher confirmation required**. Candidate key `sae_aux_backbone_domain_readability`; candidate parent A15 in `Projects/from-attention-to-search/`, not yet assigned. |
| Anchor clause / physical prior | Not available for this new question. Candidate hypothesis: the specified auxiliary update may alter representation accessibility; no theorem of separability is assumed. |
| Pair | Fresh serial control C and treatment T, copied from one seed-17 complete initialization. |
| Unique difference | `aux_backbone_grad=false` in C, `true` in T; only the sampled auxiliary encoder input changes gradient connectivity. |
| Objective | Global next-token cross-entropy + 0.1 × global sampled energy-normalized reconstruction error; target and energy denominator stop gradients in both arms. |
| Primary decision quantity | T minus C macro-F1 in percentage points on the fixed 400-document development set, using frozen pre-SAE representations and fit-only classifier selection, at exactly 1,073,741,824 valid prediction tokens. |
| Cost | Paired T minus C next-token NLL, natural-log units per valid target, on a fixed 1,048,576-target development window. |
| Development branches | Supporting direction, non-supporting direction, or insufficient resolution/eligibility; rules in §15. No formal scientific acceptance threshold is adopted. |
| Conditions / budget | Two arms only. Independent engineering Smoke ≤100 logical updates each; scientific development from common zero to 1024 and, if the approved gate permits, cumulatively 4096 updates each. |
| Resource proposal | `h100-4-reserved`, image `shphd-lite-0911`; one node occupied at a time. Smoke ≤1 h/arm; development training ≤5 h/arm cumulatively; all checkpoint evaluation ≤2 node-hours for the pair. Total candidate ceiling 14 allocated four-GPU node-hours / 56 GPU-hours. Queue time excluded. |
| Smallest recommended next authorization | Adopt the candidate design for preparation, authorize isolated implementation + bounded CPU checks + preparation of the 1200-document development panel. This does **not** include GPU Smoke or development execution. |
| Execution scope currently approved | Documentation audit and decision drafting only. Implementation, CPU training checks, data download, GPU Smoke and development runs are **not executed or approved by this draft**. |
| Freeze / registration | Not frozen; no approval timestamp. All new parameters below are AI_PROPOSAL unless explicitly identified as inspected historical configuration. |
| Cannot claim | Semantic purity, factual understanding, sparse-mechanism necessity, useful routing, downstream gain, or cross-seed reproducibility. |

The [Chinese decision card](decision_card_cn.md) and [executor checklist](execution_checklist_cn.md) are extracts of this file; this file owns candidate values. The [source audit](source_audit.json) records inspected file identities, not approval.

## 1. Terminology / definitions

SAE means sparse autoencoder. Its encoder emits at most 32 positive activations from 30,000 slots and its decoder reconstructs a 1024-dimensional vector. LM means the next-token language-model task. MLP means the Transformer block's feed-forward module. DDP means data-parallel training with averaged gradients. NLL means average negative log-likelihood in natural-log units per target.

`h_pre_sae` is the last block's post-attention-residual, post-`norm2` state, currently returned as `features["sae_input"]`. `hhat_mlp_input` is its SAE reconstruction, currently `features["mediated_reconstruction"]`, actually consumed by the serial MLP. **The primary metric uses h_pre_sae.** Calling both objects simply “MLP input” is prohibited in exports and reports. The paired design's final MLP receives hhat, while the question asks whether the upstream original state becomes more readable.

C is the auxiliary-detached control; T is the auxiliary-backpropagating treatment. `sg` / detach preserves a forward value while stopping gradients. A logical update means one completed accumulation window and optimizer/scheduler step; replay work is tracked separately from unique logical progress. B denotes 10^9 valid prediction targets.

## 2. Anchor alignment and ownership audit

[PROJECTS.md](../../../PROJECTS.md) maps the active project to `Projects/from-attention-to-search/` and A15 representation/routing research. Its related SAE row points to older Anchor `15_13_10`. The linked [current Focus](../../0907/focus_sae_flat_router_functional_training.md) instead owns `A15.sae_hierarchical_teacher_construction` and Anchor `15_13_11_structural_routing_incremental_learning_anchor.md`, a post-training routing/incremental-learning question with a frozen backbone. Neither owns random-initialized Dense pretraining with auxiliary gradients into the backbone. The actual `15_13_11` problem definition was read; the mismatch is recorded, not repaired outside scope.

The three date-local `focus_meeting_*_cn.md` files explicitly describe AI meeting drafts, not a confirmed new Focus. Within these checked owner sources, no confirmed owner for this pair was found. This is a bounded ownership audit, not a claim that no related document exists anywhere.

Before canonical promotion, the researcher must confirm the parent workstream, stable key and one next decision. Candidate next decision: whether the eligible one-seed development pair warrants a separately designed independent confirmation. No Anchor/Focus is authored or reassigned here. The user instruction to finish a reviewable draft takes precedence over the skill's usual confirmed-Anchor-before-drafting workflow; it does not waive scientific approval.

## 3. Tested hypothesis

Candidate H: at the fixed final development token checkpoint, T yields greater domain macro-F1 from h_pre_sae than C, with bounded LM cost. The primary falsifier is no positive difference at a qualified fixed endpoint, or a positive difference accompanied by unacceptable cost. Cost acceptance is human-owned; §15 registers descriptive branches and a conservative proposed engineering stop, not a universal scientific success cutoff.

Initialization, forward computation and data are matched. Under this contract an eligible difference estimates the effect of the auxiliary-gradient switch for this architecture, schedule, seed and panel. It does not identify why this update works or prove sparse coding is necessary. No positive result exists yet.

## 4. Rival explanations and guards

| Rival / failure | Required separating evidence | Role / artifact |
|---|---|---|
| Only the online SAE adapts better | Primary h_pre_sae readout alongside SAE quality and hhat diagnostic | `metrics/representation.csv`, `metrics/sae_quality.csv` |
| Forward structure, initialization, data or weight differs | Same-state no-op test; full tensor initialization equality; stepwise batch/mask identity; config allowlist | `checks/gradient_contract.json`, `audit/pair_identity.json` |
| Apparent gain is representation scale or collapse | Unit-length h_pre_sae readout; raw norms/variance and paired mean cosine | Same representation/health tables |
| Domain labels leak through metadata or duplicate documents | Remove metadata; group duplicates before splitting; lexical baseline | `data/domain_manifest.json`, `checks/panel_preflight.json` |
| Hyperparameter selection inflates the reported development score | Select classifier strength exclusively within fitting data | `analysis/readout_selection.json` |
| Different effective batches or loss reductions change optimization | Frozen counts, DDP reference checks, token-aligned schedules | `checks/reduction_contract.json`, TensorBoard events |
| Recovery changes the next update | Separate-process replay, RNG/cursor/LR/state checks | `checks/resume_replay.json` |

No third LM training arm, feature matching, full downstream benchmark, separate SAE refitting or new regularizer is required to resolve this first contrast.

## 5. Data construction and provenance

### 5.1 LM training and development loss

Reuse `/data/250010109/training_data_views/dclm_pair_v1/train` and manifest `/data/250010109/training_data_views/dclm_pair_v1/manifest.json`, expected SHA-256 `8a91bdbb0eb537bd80612015b99f178ca1cbb54a2fa7cf8442ab1eae7f0a2f2d`. Verify linked paths, sizes and validation exclusion. This is not a whole-corpus content-hash or document-decontamination proof.

Use only the tokenizer assets in `/data/share/Qwen3-0.6B-Base`; never load its pretrained weights. Inherit the inspected 30B-source-token prefix, sequential 512-sample per-rank block sampler, `shuffle_blocks=false`, `drop_partial_superblock=false`, and initial cursor zero. At a 1.074B budget no cycling is needed; propose `cycle_data=false` for both new arms so exhaustion fails explicitly. This does not alter the prefix they consume within budget.

The mmap loader reads 2049 IDs and supplies 2048 aligned input/next-token target pairs, advancing by 2048 IDs. Do not shift targets again. Count actual eligible non-ignored targets; full development updates must each have 262144 targets. Never pad a partial final update to claim the fixed coordinate.

Candidate LM development window: validation dataset sample indices **4096 through 4607 inclusive**, context 2048, exactly 512 sequences / 1,048,576 valid targets; absolute stream target offsets are `4096*2048+1` through `4608*2048`. Use the same windows and target masks for both arms and every checkpoint. Record source path, sample indices and token-content hashes before any new evaluation. Engineering Smoke may use indices 0 through 7, 16384 targets, separately labelled.

**Historical contamination correction:** the [completed analysis1 report](../docs/analysis1/08_complete_experiment_report_cn.md) records evaluation of all 56,146 sequences / 114,987,008 positions of this validation stream. Changing offsets within it cannot create untouched confirmation data. Both windows here are development/engineering assets only. Independent LM confirmation data are deferred, not a prerequisite for this explicitly exploratory pilot. Language-model training exclusion remains distinct from analyst exposure and document-level overlap.

### 5.2 Natural domain development panel

Candidate source: [official M2D2 dataset card](https://huggingface.co/datasets/machelreid/m2d2). It lists the eight requested configurations and uses a loading script. The card was checked on 2026-09-14; data files, document granularity, quota sufficiency and loader compatibility have **not** been qualified or downloaded in this task.

Freeze eight classes: `cs.CL`, `cs.CV`, `math.AP`, `math.NT`, `q-bio.GN`, `q-bio.NC`, `physics.optics`, `physics.flu-dyn`. Fit: 100 documents/class from official train; development: 50/class from official validation, total 800+400=1200. Reserve official test for future independent confirmation; do not evaluate it. If official validation, document identity or quotas cannot be recovered, record DATA_BLOCKED and return the exact missing item; do not invent a new split or replace a class.

Candidate deterministic preparation rule:

1. Pin dataset repository revision and loading script; record source file hashes, source split, document identity and category. Inspect the loader before using it. A separately network-enabled acquisition process may be used after preparation authorization; the old training runtime's offline flags must not cause a silent synthetic fallback.
2. Remove category fields, source headers and explicit category metadata; keep natural terms in body text. Normalize Unicode NFKC and whitespace for matching, retaining original text/hash. Require at least 257 tokenizer IDs with `add_special_tokens=false`; do not append prompts/newlines or special tokens. Use the first 257 IDs; representations use positions 0..255 inclusive, final-position sensitivity uses position 255.
3. Build duplicate groups before sampling: same recovered source document ID, same normalized-text hash, same first-257-token hash, or normalized word 5-gram Jaccard similarity >=0.8 joins a connected component. Any candidate-search acceleration must be versioned and validated; missed near duplicates remain a reported limit. To avoid multi-label/split arbitration, exclude groups spanning requested categories or official splits; select one deterministic representative per remaining group. Never copy documents to fill quotas.
4. Rank each class/split's groups by SHA-256 of `20260914|class|split|group_id` and take the first quota. Document grouping and adequacy must be audited before scientific training. Freeze text/token/source/group hashes, exact positions, labels and excluded counts in `domain_manifest.json`.
5. Derived examples from the same underlying document cannot be split across pools. If source rows are fragments without recoverable parent IDs, mark document independence unverified and do not silently call the panel document-held-out. The researcher must decide any weaker scope before development execution.

The existing 360-sentence artificial panel is interface/debug material only. The future 9600-document panel and extra sources are outside this pilot. A pilot preparation failure does not require conducting the entire later confirmation study.

## 6. Learning task and permitted supervision

Train both LM arms solely on next-token targets plus the specified self-reconstruction target. Domain labels never enter LM/SAE updates, initialization, sample selection during LM training, or a training schedule. After checkpoint freezing, labelled fitting documents train a separate linear classifier. Development labels score the selected classifier and inform only this development-stage decision.

Malformed data, empty eligible accumulation windows, missing categories or invalid caches are typed failures; do not drop failing examples post hoc or substitute samples after seeing predictions.

## 7. Model / architecture and frozen variants

All inherited values below were checked in actual source/config; adopting them for new runs remains proposed.

| Parameter | Both arms |
|---|---|
| Backbone | 8 blocks; hidden 1024; intermediate 3072; query/KV heads 16/8; head_dim 128 (not hidden/heads) |
| Tokenizer/context | Vocabulary 151936; context 2048; tied input/output embedding; random init std 0.02 |
| Normalization/positions | RMS epsilon 1e-6; RoPE theta 1000000 |
| SAE | `sae_mode=bottleneck`, alpha=1; width 30000, k=32; nonnegative selected values; forward-normalized decoder columns |
| Parameter count | Backbone 281431040 + SAE 61471024 = total 342902064 |
| Forward | Last attention residual -> norm2 -> SAE reconstruction -> last MLP; residual bypass retained |
| Numerics | Existing CUDA bfloat16 autocast; FP32 parameter/optimizer storage as inherited; CE chunks 128 with CE recomputation; no block gradient checkpointing |
| New field | C: `aux_backbone_grad=false`; T: `true`; strictly serialized boolean, default false for legacy loading |
| Exclusions | No AuxK, reset/resampling, sidecar arm, optimizer change, cosine decay, third training arm or pretrained warm start |

## 8. Training objective, gradients, optimization and telemetry

For each sampled eligible position with h = h_pre_sae, let A be the SAE reconstruction function:

$$x_C=\mathrm{sg}(h),\quad x_T=h,\qquad R(h)=\frac{\|A(x)-\mathrm{sg}(h)\|_2^2}{\max(\|\mathrm{sg}(h)\|_2^2,1024\cdot10^{-4})}.$$

For one full optimizer update, N is the total eligible LM target count over all ranks and accumulation microbatches, M is the analogous sampled SAE count:

$$L_{LM}=\frac{\sum\ell_{LM}}{N},\quad L_R=\frac{\sum R}{M},\quad L=L_{LM}+0.1L_R.$$

DDP backward uses world_size × each rank/microbatch loss sum divided by the corresponding full-update global denominator, then relies on DDP gradient averaging. Do not divide by accumulation twice or average per-microbatch/per-rank means. M and N are different denominators. Main-path SAE uses all valid positions; only the auxiliary branch samples 1/8. Preserve the inspected per-microbatch exact-count random-subset rule, independent sampler RNG and stepwise mask identity.

Stop gradients at target and energy denominator in both arms. Only T's auxiliary input has a backbone gradient. This is the reconstruction-input-path update, not full differentiation of both sides of reconstruction and not a differentiable L0 count penalty. At the same state auxiliary SAE gradients agree between arms; backbone auxiliary gradients differ. Subsequent learned SAE states may diverge indirectly.

Parameter ownership: auxiliary gradients can reach `embed.weight`, earlier blocks, final attention and final `norm2`; they do not reach the last MLP gate/up/down or final output norm through this auxiliary graph. The tied output weight **is** `embed.weight` and can receive auxiliary gradients through its input role. Audit by tensor identity, not a string containing “head”. Do not require every individual upstream tensor or every embedding row to have a nonzero gradient on one batch.

| Optimization field | Value |
|---|---|
| Optimizer | One AdamW with disjoint LM matrix / LM non-matrix / SAE groups; epsilon 1e-8; fused on qualified CUDA |
| LM groups | Peak LR 3e-4; betas (0.9,0.95); matrix decay 0.1, norm/bias decay 0 |
| SAE group | Peak LR 3e-4; betas (0.9,0.999); decay 0 |
| Clipping | LM and SAE separately, maximum norm 1 after accumulation/synchronization |
| Batch | 4 ranks × 2 sequences/rank/microbatch × 16 accumulation × 2048 targets = 262144/update |
| Warmup | LM 262144000 tokens (1000 updates), SAE 2621440 tokens (10 updates); constant thereafter |
| Exact inherited indexing | For zero-based update u starting after u completed updates, applied LR is `3e-4*min(1,u/warmup_updates)`; scheduler steps after optimizer. First applied LR is 0. Log applied LR, not the next scheduler value. A zero parameter delta on that first update is not a failed gradient connection. |
| Skipped/incomplete updates | Any nonfinite/skipped update stops the arm; no silent skip. Primary counters advance only after a complete successful logical update. Interrupted/replayed physical work is recorded separately. |

### Telemetry contract

Follow [the repository contract](../../../docs/training_observability_contract.md). One logging rank writes globally reduced values to `<run_root>/tensorboard/` each logical update; retain unsmoothed JSONL metrics too. Component registry name is `sae_reconstruction`; coefficient=0.1, position set=auxiliary sampled eligible positions, denominator=M, one final-block module.

- Token-coordinate tags: `tokens/train_lm_loss`, `tokens/train_total_loss`, `tokens/loss_component/sae_reconstruction_raw`, `tokens/loss_component/sae_reconstruction_weighted`.
- Update-coordinate tags: `updates/train_lm_loss`, `updates/train_total_loss`, `updates/loss_component/sae_reconstruction_raw`, `updates/loss_component/sae_reconstruction_weighted`, `updates/learning_rate`, `updates/sae_learning_rate`.
- Progress: `progress/tokens_seen` and `progress/effective_tokens_per_update` against optimizer update; `progress/optimizer_step` against cumulative valid targets; auxiliary count under `updates/sae_samples` and `updates/cumulative_sae_samples`.
- Fixed-checkpoint evaluation: `tokens/eval_lm_nll`, `tokens/dev_domain_macro_f1` (fraction 0..1), plus manifest identity in the companion JSONL. Report T-C macro-F1 as percentage points in tables.
- Gradient probes: raw LM and raw/weighted auxiliary backbone norms, cosine and zero-norm reason, before clipping; fixed engineering batch at initial state and scientific checkpoints 128/1024/4096. Restore RNG and avoid optimizer/counter changes. No every-step extra full backward.

No mandatory unrelated z-loss exists. AuxK is `NOT_APPLICABLE: absent from objective`; no invented zero trace. Weighted auxiliary equals 0.1 × raw and total equals LM + weighted under their registered global denominators. Resume restores coordinates; archive conflicting stale event tails or use named non-overlapping resume segments.

## 9. Conditions, seeds and checkpoints

Scientific initialization: seed 17, initialize once and copy complete model and initial optimizer/scheduler state plus compatible per-rank RNG/cursor state. Full tensor comparison, not seed equality or sampled hashes alone, establishes initial identity. Preserve a shared initialization artifact and arm-specific config linkage. Smoke has separate disposable trajectories and is not continued into scientific development.

| Completed updates | Valid targets | Purpose |
|---:|---:|---|
| 0 | 0 | No-op/readout reference |
| 128 | 33554432 | Early state and gradient probe |
| 512 | 134217728 | First full activity-window checkpoint |
| 1024 | 268435456 | Development stage gate |
| 2048 | 536870912 | Intermediate learning trajectory |
| 4096 | 1073741824 | Fixed primary development endpoint |

All checkpoints receive the same panel and loss-window evaluation. Do not select the best checkpoint or smooth into a better verdict. C/T execute C-1024, T-1024, gate, C-4096, T-4096 on one node at a time; the second stage resumes full state without restarting warmup. Its immutable target remains 4096 throughout; a separate stage ceiling pauses at 1024 so resumption does not silently change the scientific configuration.

Rolling recovery every 256 updates / 67108864 targets, keep two; science checkpoints above are retained separately. Store full optimizer/scheduler/cursor/counters/source/data identities, the rolling activity-window state and all-rank RNG. Before Smoke use an existing same-architecture complete optimizer checkpoint's file sizes for a preliminary storage estimate; before development replace this with measured new-Smoke state after Adam moments exist, never a step-zero/model-only size. For complete checkpoint size S, allow nine full copies/arm including a transient atomic write, plus one initialization copy, Smoke outputs, artifacts and 20% headroom. Proposed hard experiment disk ceiling 160 GiB. If estimated need exceeds it or free space, stop before launch; never delete science points to fit a cap. Do not claim actual storage cost before measurement.

## 10. Primary metric and candidate frozen analysis plan

Primary estimand: development-domain accessibility difference `100*(macroF1_T - macroF1_C)` at the fixed 4096 endpoint. Observational unit=one retained document; sampling unit=deduplicated document group; training unit=one paired seed. Eight classes receive equal weight. Per-class F1=2TP/(2TP+FP+FN), zero denominator -> 0; macro-F1 is the mean over all eight declared classes.

For each checkpoint/arm, export float32 mean h_pre_sae over positions 0..255. Fit an L2 multinomial logistic classifier with intercept, solver lbfgs, tolerance 1e-6, maximum 5000 iterations, candidate inverse regularization strengths {0.01,0.1,1,10}. Fit-only standardization: per-coordinate mean/std, zero variance scale=1. Select strength by five fitting-only class-stratified group folds, fixed seed 20260914; standardization is fitted inside each fold. Maximize mean fold macro-F1, exact ties choose the smaller strength. Refit on all 800 fitting documents and evaluate once on the 400 development documents. Store predictions, selected strengths and convergence status. Unresolved nonconvergence is metric failure, not permission to choose a different solver after seeing results.

This replaces the input plan's development-selected classifier strength: it preserves all documents and all LM training, and adds 17 small CPU classifier fits per representation/arm/checkpoint (21 versus 4). It targets selection optimism without a new GPU condition. Actual CPU time is not measured; use bounded execution per the envelope. Repeated viewing of development results still makes this development evidence, not formal confirmation.

Paired sampling interval: 2000 class-stratified document-group bootstrap replicates, seed 20260914, resample the same group indices for C and T; use fixed trained predictions, no classifier refitting within bootstrap. Report two-sided 2.5/97.5 percentiles. This measures evaluation-sample sensitivity conditional on this fit panel and seed, not training-seed or classifier-fit uncertainty. All valid groups are included; no outlier exclusions. Missing arm/checkpoint, label or prediction => insufficient, no imputation.

Only 4096 is the primary endpoint; intermediate checkpoints and secondary views are descriptive, not additional significance opportunities. No multiplicity-adjusted discovery is claimed. No independent confirmation data are opened under this contract.

## 11. Secondary metrics and guards

1. LM cost: fixed development window mean NLL, sum of target losses / valid-target count. Report per-sequence sums, paired difference and 2000 paired sequence bootstrap percentiles (seed 20260914). Adjacent sequences may be dependent; label this interval descriptive, not a document-independent confidence claim.
2. Scale guard: normalize each document mean h_pre_sae to unit norm (zero norms are reported) then apply the same classifier pipeline; also report original norm median/p10/p90, per-coordinate variance and paired mean cosine. Final-position h_pre_sae readout at position 255 is sensitivity, never a replacement primary metric.
3. SAE reader diagnostic: hhat mean readout using the same pipeline, fixed-panel reconstruction quality, positive activation count, and per-domain all-dictionary activation probabilities. Reconstruction quality is `sum||hhat-h||² / sum||h-mu_fit||²`, where mu_fit is the current arm/checkpoint fitting-position mean; denominator zero => insufficient. This is distinct from the training energy-normalized R. Also record mean training-form R on fitting documents as the fixed stability signal.
4. Activity: globally aggregate actual sampled-training positions over an exact last-10000000-position window; not a whole-training deadness claim. Define window order by logical update, rank, accumulation microbatch and flattened selected-position order; preserve the partial boundary and rolling state across resume. Before the window fills report WINDOW_INSUFFICIENT (100-step Smoke has about 3276800 samples; a full window needs about 306 updates). Record unused fraction, positive-activation count and top-300 activation-count share; zero total positive activity is a typed ZERO_ACTIVITY failure rather than a fabricated concentration ratio. Do not infer permanent death from short text coverage.
5. Lexical guard: fit a word 1–2-gram TF-IDF classifier on the same 800 fitting texts (max_features=20000, min_df=2, lowercase, L2 normalization) with the same fit-only strength selection; transform development with fit-only vocabulary/IDF. This tests whether ordinary words separate domains; a strong score alone does not disprove model structure.
6. High-frequency sensitivity: for each arm/checkpoint rank 30000 features by fitting-panel per-position positive-activation probability, ties by feature ID; freeze top 300 for development summaries. Show all-feature and removed-feature views together, removed activation share and remaining coverage. Never delete them from the LM forward path or substitute filtered views for the primary h metric.

Save per-document sparse summaries; do not create document × token × 30000 dense dumps. Figures are optional derived views after evaluation, not launch gates or expected evidence.

## 12. Known good / bad / confusing cases and acceptance

All tolerances below are proposed engineering limits, not measured achievements.

| Check | Passing evidence | Failure / confusion handled |
|---|---|---|
| Same-state switch | Exact tensor initialization equality; identical same-state forward tensors/losses in deterministic CPU fixture; real-GPU repeated same-state comparison atol 1e-5, rtol 1e-4 | A numeric forward change means intervention is not isolated; train-diverged arms need not have equal outputs |
| Auxiliary only | C backbone grads absent/exact zero; T aggregate upstream grad >0 and finite; both SAE groups >0; no last-MLP/final-norm auxiliary grads | Shared embedding is upstream; not every upstream tensor/row must activate |
| LM only | Both arms give same-state matching gradients into SAE and upstream | No claim based on total-gradient norm alone |
| Weight/stop paths | λ=0/0.1/1 gradients scale before clipping; target/denominator have no backward path; CPU float64 atol 1e-10, rtol 1e-7 | λ tests do not add scientific arms; finite differencing the stopped target is not the intended derivative |
| Distributed reduction | Unequal per-rank/microbatch counts match single-process reference (CPU float64 atol 1e-10, rtol 1e-7); count independently | Detect mean-of-means or double accumulation scaling |
| Actual export | Training h_pre_sae equals offline `sae_input` on the same fixture; hhat equality separately | Old evaluator uses `pre_mlp_input`, which the current package does not export |
| Resume | Separate-process tiny CPU replay full tensors/states within atol 1e-7, rtol 1e-6; real four-GPU replay at 50->51 compares input/mask/RNG/cursor/LR exactly, losses/state probes atol 1e-6, rtol 1e-5 | GPU probes are bounded samples, not full optimizer-tensor proof. Replayed steps do not count twice. |
| Telemetry | Required tags finite; counters independently correct; raw/weighted/total agree; resumed event coordinates non-conflicting | Missing logs make affected curves ineligible |
| Panel metric fixtures | Synthetic separable/permuted-label fixtures detect indexing/leakage bugs; real baseline quality is not pre-assumed | Fixture success is engineering evidence only |

First optimizer LR is zero under the inherited schedule. Check actual gradient connectivity at zero and parameter change after a positive-LR update. No failed test is “fixed” by weakening tolerances without a documented reviewed revision.

## 13. Scientific procedure and stage contracts

| Stage | Inputs / operation / why | Output and exit | Handoff |
|---|---|---|---|
| P: preparation | Authorized isolated code copy; reviewed contract; construct gradient switch, telemetry and panel using §5/§8/§12 | CPU checks, pair-config diff, source hashes, data manifests; any missing quota/identity recorded | Concrete GPU request; no submission under preparation scope |
| S: engineering Smoke | P gradient/reduction/telemetry checks; tiny fixed engineering panel; each arm ≤100 logical updates, ≤1h wall including startup/replay | Real gradient and separate-process replay receipts, throughput/memory/storage measurements; finite events and terminal receipts | Qualified engineering only. No scientific continuation from Smoke. |
| D1: early development | S passed, natural panel and LM window frozen, explicit D1 scope; common initialization; both arms to 1024 | Checkpoints/paired metrics/activity gates; no-effect is not a scientific failure near warmup | Proceed only if D2 scope already approved and gate below allows; otherwise stop scheduled work at D1 |
| D2: development endpoint | Full-state resume, same immutable target/schedule/data; D1 gate passed; explicit D2 scope | Both arms to 4096, fixed endpoint metrics, all deviations/cost recorded | Stop at 4096 and return result for human judgment, regardless of sign |

Proposed D1->D2 gate: both arms reached 1024 exactly, identity/gradient/recovery/telemetry/data/export checks pass, full activity window exists, all registered intermediate metrics are finite, neither of the following conservative stability stops fired at **both 512 and 1024**:

- fixed LM development `NLL_T - NLL_C > 0.10` natural-log units/target; or
- in either arm, fitting-panel mean training-form reconstruction error >2 × its own step-zero value **and** the top-300 share of positive training activations exceeds 0.90 in the full activity window.

These newly specified cutoffs are **AI_PROPOSAL cost/degeneration stops**, not scientific effect thresholds, optimal values or confirmation criteria. They apply symmetrically where relevant, add no training conditions, and use already planned evaluations. On trigger, pause the pair, preserve both arms and return the concrete diagnostic; do not add AuxK or sweep λ automatically. No F1 improvement is required at D1. Failed data/metric eligibility pauses both arms; completed evidence remains preserved.

At any stage: nonfinite loss/gradient, empty auxiliary count on a rank, wrong counters or mask identity, corrupted/incompatible checkpoint, insufficient storage, wrong runtime/source/profile, or resource ceiling => stop the affected job and do not advance its mate beyond the current approved comparison gate. A scheduled but unstarted job is not a passed stage. If a mate fails, report a partial pair; never substitute historical checkpoints. No automatic retry or extra training beyond the approved ceiling.

Development training wall cap is five hours **per arm across both stages/processes**, not five per resubmission. Evaluation has a separate pair-total two-hour cap; track initialization and save times honestly. The overall allocation cap includes startup, checks, saves and evaluations. If actual measured throughput predicts cap overrun, report it; do not reduce token budget and call the original endpoint complete. Future three-seed 5B confirmation is not authorized by any pilot gate.

## 14. Algorithm, outputs, provenance and reuse

Proposed execution root E_NEW: `/data/250010109/MoE_Router/experiments/20260914_sae_aux_backbone_pilot` (absent at this audit). If it exists at implementation time, inspect ownership and choose an isolated suffix; never overwrite it. E_OLD: `/data/250010109/MoE_Router/experiments/20260912_dense_sae_pretraining`. Analysis reference: `/data/250010109/MoE_Router/experiments/20260914_semantic_feature_reuse_analysis/semantic_confirmation_v1.py`.

| Local asset | Reuse decision |
|---|---|
| E_OLD data.py / data_contract.py / tokenizer_contract.py | Direct reuse of aligned targets, data view and tokenizer-only identity checks |
| E_OLD checkpoint.py | Reuse full-state/rank RNG API; adapt new switch/stage-cap contract and event reconciliation, requalify rather than inherit old test scope |
| E_OLD model config / model forward / engine.py / train.py | Adapt explicit switch, λ validation and objective call, staged budget, telemetry and gradient diagnostics |
| E_OLD model/sae.py | Reuse top-k/nonnegative encoding, forward decoder normalization, target detach and normalized objective; no first-pilot AuxK |
| E_OLD scripts/runtime.sh | Reuse isolated environment pattern; activation must resolve the new package first. Qualify TensorBoard dependency in a process-local layer if missing; no base-image modification. |
| Existing paired analysis | Adapt loading and probing; replace `pre_mlp_input` lookup with verified h_pre_sae export, last-token/newline pooling with fixed-window mean, old balanced-accuracy/strength grid with §10. No claim of direct drop-in reuse. |
| Historical runs / old full launcher | Background only; do not use as C, load 19B weights, or call the old 50B automatic-resume entrypoint |
| Upstream sources | M2D2 is a proposed external data source; two unnamed package papers are unidentified, not local reusable assets or algorithm evidence. No new paper reproduction is claimed. |

After isolated implementation, proposed entrypoints are new bounded `scripts/run_pair_smoke_4h100.sh` and `scripts/run_pair_development_4h100.sh`, not implemented here. Resolve submission through [execution envelope](../../../docs/execution_envelope.md) and `templates/execution/acp_submit_template.sh` only. Protocol declaration:

```yaml
execution_surface: acp
resource_profile: h100-4-reserved
image_id: shphd-lite-0911
env_layer: /data/250010109/MoE_Router/experiments/20260914_sae_aux_backbone_pilot/scripts/runtime.sh
execution_approval: NONE
```

The env_layer path is proposed, not existing/qualified. Resolve image URL, mount and submission entrypoint live from the envelope; do not copy a second registry here. A submission certificate records expanded tuple, runtime versions, command, code/config/data/protocol hashes, actual device use, output roots, owner conversation and terminal log. No image listing or platform call was performed by this draft.

Expected E_NEW layout: `audit/`, `checks/`, `data/`, `initialization/`, `runs/smoke/{C,T}/`, `runs/development/{C,T}/`, `evaluation/`, `acp_receipts/`. Each run owns tensorboard events, unsmoothed metrics, failure/terminal receipts and checkpoints. Each evaluation records arm/seed/update/tokens/source and checkpoint hash/panel hash/pooling/metric/denominator. Save document predictions and representations, sparse SAE summaries, per-sequence NLL, pair deltas and sampling intervals. No public data/raw caches in Research_System.

Canonical result destinations, after ownership assignment, are sibling `summary.md`, `summary_cn.md`, `detailed.md` under the owning experiment directory. Until then no synthetic result record is created: status is NOT RUN. Reader-facing figures must be copied into the owning date's figures directory with provenance. One designated execution agent owns startup observation and receipts; unless asked for completion monitoring, observe only the bounded startup gate, report job ID/progress/measured ETA, then end polling while the job runs. D1/D2 stop logic belongs in the bounded job, not in an indefinitely active chat.

## 15. Success / failure / insufficient evidence

Engineering PASS means only all applicable §12 checks passed with their receipts. Development completion means both arms reached the registered endpoint, or a typed stop and preserved partial evidence explain why not.

For eligible endpoint metrics define ΔF = T-C macro-F1 in percentage points and its conditional sampling interval [lF,uF]; define ΔN = T-C LM NLL. Descriptive classification, in priority order:

1. Missing/invalid pair, failed checks, exhausted budget before the endpoint, nonconverged readout or unusable data: **INSUFFICIENT / typed cause**; no method verdict.
2. Qualified endpoint with ΔN >0.10: **LM_COST_WARNING**; do not recommend expansion from F1 alone. This is the proposed conservative engineering flag, not the accepted scientific cost margin.
3. lF >0 and ΔN <=0.10: **SUPPORTING_DEVELOPMENT_DIRECTION**; report ΔN and its descriptive interval in full. This is a candidate for human review, not confirmation or automatic approval of its cost.
4. uF <=0 and ΔN <=0.10: **NON_SUPPORTING_DEVELOPMENT_DIRECTION** in the tested setting; it does not prove no later/on-other-data effect.
5. Otherwise: **INSUFFICIENT_RESOLUTION**; retain zero-crossing intervals and both signs.

SAE-only improvement cannot rescue the primary h result. Unit-normalized/lexical sensitivity can qualify interpretation but cannot replace the endpoint. An early degeneration stop is an operational limitation, not a final 1B falsification. Formal +2pp/three-seed/sign-agreement/0.02 NLL rules from the input package remain deferred candidates, absent from this pilot's confirmation claims.

## 16. Cannot-claim boundary and deferred branches

| Deferred item | Trigger and next bounded question | Added cost / current status |
|---|---|---|
| Two unnamed papers | Researcher supplies titles/links or package identifies them; check what objectives/gradient paths they actually justify | Reading only; identities UNKNOWN; not a launch dependency |
| Cross-checkpoint semantic feature matching | A later question requires tracking stable meaning, beyond fixed parameter-slot trajectories | Separate analysis design; no required startup fit or matching |
| AuxK / anti-dead-feature method | Joint reconstruction/usage degeneration or a qualified activity failure motivates intervention | New implementation and paired restart, both arms identically configured; retain unique backbone-gradient switch, specify new auxiliary gradient owner; budget to be reviewed, not slipped into this run |
| Sidecar pair | Serial pilot is interpretable and question becomes whether the effect survives removal of serial inference dependency | At least another matched pair and new forward/control contract; not free extrapolation |
| Dense/non-sparse autoencoder control | A future claim attributes the benefit specifically to sparse coding | Additional matched condition and compute; not required to estimate this switch's effect |
| Independent SAE refits | Online SAE improves but raw-h evidence does not; distinguish reader adaptation under matched refit budgets | Checkpoint-only extra fitting, separately bounded |
| Three seeds × ~5B / downstream / new confirmation sources | Researcher accepts the development result boundary and specifies one confirmation question | Separate contract and budget; old throughput gives 228–392 GPU-hour reference for six ~5B trajectories, not a reservation or ETA |

## 17. Block audit, freeze and amendment ledger

| Block | State | Remaining prerequisite |
|---|---|---|
| A: question/claim/owner | BLOCKED | Researcher chooses parent/key/Focus/Anchor and adopts the candidate bounded hypothesis; no source document owns it yet |
| B: data/provenance | PROPOSED | Preparation must materialize/pin/audit the domain panel and fixed LM hashes; official document IDs and quotas unverified |
| C: task/supervision | PROPOSED | Candidate fully stated; labels never update LM |
| D: model | PROPOSED | Historical config verified; new adoption and full-state no-op checks pending |
| E: objective/optimization | PROPOSED | λ chain/new switch and exact inherited LR semantics specified; implementation unrun |
| F: comparison/analysis | PROPOSED | Fit-only selection, descriptive branches and operational thresholds await adoption |
| G: execution | PROPOSED | Preparation/Smoke/D1/D2 are separate named scopes; runtime/data checks pending; none approved |

Cross-block audit: proposed comparison, coordinates and units are internally consistent; **canonical alignment and executability NOT PASSED** because owner/adoption/preflight are pending. This is not a failed document delivery. It is a complete candidate awaiting the decisions it cannot own.

Grounding ledger: user explicitly authorized document audit/draft and supplied the target question; historical config/source identities are VERIFIED_SOURCE; all future settings/thresholds/resource ceilings are AI_PROPOSAL. User emphasis on reviewing the candidate is not blanket design confirmation. Before first execution approval record scientific-body hash, approved scope and time; preserve that body thereafter. Any material change uses an append-only amendment with old/new values, reason, exposed results, approval and eligibility impact. Do not record observed results in the registered hypothesis/criteria.

Final draft audit: cold-reader question/pair/objective/data/metrics/stages/stops/artifacts present; no new training source edited; no jobs submitted; no owner state or source package rewritten. A-G confirmation and actual preflight remain pending by design.
