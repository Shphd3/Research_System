# Protocol: natural_ntp_representation_compatibility_v1

## 0. Approval Snapshot

- Document status: **EXECUTION_AUTHORIZED_PENDING_QUALIFICATION**; results were **NOT RUN** at this instruction. [中文 companion](protocol_cn.md).
- On 2026-09-29, after reviewing the draft delivery, the researcher explicitly instructed implementation, Smoke submission and supervision, then Full submission if Smoke passes. This adopts this Protocol's exact design and authorizes those two stages. Data, numerical, fit, resource, sealing and Smoke gates still apply. No commit, push or change to the old Focus scientific verdict is authorized.
- Primary Anchor: [natural NTP compatibility](anchor_natural_ntp_representation_compatibility.md), [中文](anchor_natural_ntp_representation_compatibility_cn.md). The scientific choices and numbers below were AI proposals and are adopted for this execution by the instruction above; qualification is not thereby passed.
- Focus alignment: the [existing 0927 Focus](../../0927/focus_shared_update_conditional_interference.md) owns the completed controlled-binary question, not this new natural-text design. The new Focus confirmation is **BLOCKED for promotion**, not a reason to leave this user-requested draft incomplete. Do not modify the old Focus by implication.
- Purpose/role: operationalization test of whether native pre-update representations predict continuous local NTP update compatibility on independent documents; not Router construction.
- Minimal setup: one fixed S7 reconstruction-weight-0.1 checkpoint at exactly 33B training tokens, one last-block attention output matrix, one natural-text document shard, genuine next-token targets.
- Changed quantity: predictor input/functional family; fixed quantities: model, matrix, corpus, events, pair labels, splits, fitting and evaluation rules. Prediction is observational; small temporary matrix updates test the finite-loss bridge.
- Primary comparison: development-selected geometry/full predictor versus training-mean constant; primary statistic Q (§10), proposed useful threshold 0.05. All-positive compatibility is allowed.
- Support/non-support/insufficient: respectively lower 95% bound >0.05, upper bound <0.05, interval crossing/touching 0.05 or qualification failure. Finite-step qualification is a separate result.
- Cannot claim: irreducible uncertainty measured, causal feature use, beneficial routing/isolation, or cross-model generality.
- A-G blocks were adopted for this version by the 2026-09-29 execution directive. Focus-level scientific status remains researcher-owned; stage qualifications require actual receipts. Paper consistency was reviewed; engineering/result status comes from durable evidence.

## 1. Terminology / Definitions

An **event** is 256 consecutive tokens from the beginning of a real document plus original token 257 as its one target. A **pair** contains two distinct documents. **Complete representation** means all 2048 coordinates entering the chosen matrix at the final prefix position, not all layers or all information available to the downstream network.

The matrix input/output/residual are c (2048), a (1024), r (1024). The derivative e (1024) is from one full-vocabulary NTP cross-entropy; G is the matrix gradient (1024×2048). K is its Frobenius inner product across a pair. K>0 means first-order cross-help under ordinary scalar-rate SGD. I is post-minus-pre loss, in nats/target; I<0 means actual help. Q is dimensionless relative squared-error reduction, not a gradient cosine or a routing utility.

OPS, TRAIN, DEV and CONFIRM are disjoint duplicate-component sets. OPS tests engineering; TRAIN fits parameters/statistics; DEV chooses allowed hyperparameters/rate; CONFIRM evaluates frozen choices. An auxiliary readout is a fitted predictor, not a trained language model.

## 2. Anchor Alignment

Preserve three plain-language steps: (1) collect native representations and exact NTP gradient-pair labels; (2) fit representation-only predictors and evaluate on independent documents; (3) check a small finite-update panel and, only after primary support, perform registered secondary structure comparisons. Completion is all mandatory stages accounted for, including typed failures, not a positive result.

The Anchor asks whether meaningful continuous differences are predictable. It does not require negative K, full>geometry, successful SAE, or the original toy label-flip pattern. The mathematical gradient identity is measurement qualification; unseen-document prediction is the empirical test. The sole current human decision is whether to accept this design before implementation/execution promotion.

## 3. Tested Hypothesis

H1: the proposed representation-only estimator has at least 5% confirmation-MSE reduction relative to a constant training mean. This is an operational lower-bound test of accessible information at one model state. A dev selection of geometry is legitimate support. The incremental full-versus-geometry relation is secondary.

For one-position gradients:

\[
G_i=e_ic_i^\top,\quad K_{ij}=(c_i^\top c_j)(e_i^\top e_j),\quad
\mu(c_i,c_j)=\mathbb E[K_{ij}\mid c_i,c_j].
\]

The learned predictor estimates this mean under squared error. State dependence across checkpoints is not measured in this run.

## 4. Rival Explanations

| Rival / shortcut | Separator | Remaining boundary |
|---|---|---|
| Overall mean / predominance of help | Constant-MSE reference, continuous target | A single sign is allowed |
| Simple norm/cosine structure | Geometry baseline and full increment | Geometry success is representation success |
| Document or near-duplicate memorization | Group deduplication before splitting; no repeated confirm endpoint | Undetected semantic duplication remains possible |
| Target, gradient or future-token leakage | Allowlist predictor fields; prefix excludes target; seal confirmation truth | Training uses gradient supervision openly |
| Poor estimator or insufficient samples | Training curves, finite outputs, fixed three-seed ensemble, fixed capacity and dev sweep | Non-support never proves information absence |
| First-order approximation failure | Ordinary SGD at two fixed rates; measured remainder | Failure restricts loss interpretation, not valid K prediction |

## 5. Data Construction And Provenance

**Chosen source (AI_PROPOSAL):** raw DCLM document file
`/mnt/bucket/109_cache_dir/hf_data/dclm_eval_holdout/global-shard_02_of_10/local-shard_0_of_10/shard_00000000_processed.jsonl.zst`.
SHA256 freshly computed in this drafting turn: `4c5ce60258943051758148653c448bb57724af7592cc9d3e9c053cc6f9e10323`. The file exists, and one decompressed record has string `text` and `url` fields. Full schema, eligible count and deduplication have **not** been measured. Fail rather than substitute a different shard if capacity is insufficient. This is file-level holdout from the checkpoint's global-shard-01 training view, not proof of semantic non-overlap with pretraining. The source has historical audit use; claim novelty only for the current sealed predictor evaluation, subject to the exposure ledger below.

**Deterministic construction, seed 20260930:** parse JSONL in original line order; require nonempty string `text`, no U+FFFD, and at least 257 tokens with the checkpoint tokenizer, `add_special_tokens=False`. Reject records whose first257 tokens include tokenizer-designated special IDs. Do not filter on domain, loss, target frequency, gradient or model confidence. Prefix=token indices 0..255; target=index256, no packing, padding or inserted BOS. All scoring uses final prefix position255 only. The induced population is eligible document openings in this shard, not all positions of natural language.

Use NFC text with collapsed Unicode whitespace only for duplicate hashes; feed original text to tokenization. Define doc_id as SHA256 of `source_sha:line_index:normalized_text_sha`. Sort eligible records by SHA256(`20260930:pool:doc_id`), retain first20,000 or all if fewer. On this candidate pool build connected duplicate components by: identical normalized-text hash; identical nonempty URL after strip; identical first257 token sequence; or Jaccard similarity ≥0.80 between sets of contiguous 5-token shingles in those first257 tokens. Exact verification is required for qualifying shingle pairs (an exact inverted-index threshold join is acceptable; approximate retrieval alone is not). Use the lowest doc_id representative per component and record all members. The threshold is an engineering leakage guard, not semantic identity. Pool-level content deduplication is outcome-blind and is recorded explicitly.

Maintain `exposure_ledger.json`: compare available prior event/window hashes, record prior sample sources and any inaccessible ledgers; do not claim universally never-viewed text. Exclude exact 257-token matches from previously inspected gradient/prediction events when their IDs are available, before ranking allocations. If current CONFIRM outcomes have been inspected during development, abort that confirmation; do not silently resample after seeing results. Old 12 synthetic families and all sealed 0924 confirmation artifacts are excluded from reuse; do not open them for this task.

Sort remaining representatives by SHA256(`20260930:split:doc_id`) and allocate in order: OPS64, TRAIN4096, DEV1024, CONFIRM2048. Require at least7232; stop `DATA_CAPACITY` otherwise. Drop unused representatives with a logged count. Each group contributes one event only. No adaptive enlargement or fallback to packed binary streams without document boundaries.

**Pairs:** TRAIN uses 32,768 unordered pairs with smallest SHA256(`20260930:train_pair:min_id:max_id`) among all distinct TRAIN events. For each of DEV and CONFIRM independently, hash-sort IDs using `20260930:pair:<split>:doc_id` and pair adjacent IDs, giving512 and1024 disjoint pairs. OPS uses the same adjacent-pair rule to form32 pairs. Each DEV/CONFIRM endpoint occurs exactly once. Record IDs and hashes before target-gradient collection. Do not balance by observed K sign. CONFIRM units are disjoint document-component pairs, so bootstrapping them does not count a shared endpoint repeatedly; intervals still condition on this shard and fitted model.

Tokenizer assets: `/data/share/Qwen3-0.6B-Base`, used as tokenizer only. `tokenizer.json` SHA256 `c0382117ea329cdf097041132f6d735924b697924d6f6fc3945713e96ce87539`; vocabulary151936. Cross-check all tokenizer files against the checkpoint run's `resolved_config.json`; never load pretrained weights from the tokenizer directory.

## 6. Learning Task And Permitted Supervision

Input: c_i,c_j only; output: one real-valued estimate of raw K. Training supervision: K computed from the real TRAIN targets with pure NTP gradients. Standardize targets using TRAIN-pair mean m and population SD s: target=(K−m)/s; undo the transform for all reported metrics. If s is zero or below the measurement resolution (§11), stop. No log transform, sign balancing, target clipping or outlier deletion.

Allowed transforms are TRAIN-only coordinate means/SDs and registered projections. Forbidden predictor inputs include IDs, URL, document/domain labels, y, loss, confidence, e, G, gradient norms, K and post-update activations. Truth files and permitted feature files are separate; the feature schema must reject unknown fields. Offline diagnostics may use truth after freeze, never to refit/reselect. Labels are inherent next tokens, not human domain annotations.

## 7. Model / Architecture And Frozen Variants

**Language model:** checkpoint root
`/data/250010109/MoE_Router/experiments/20260920_s7_lambda0p1_from_scratch_4h100/runs/S7_lambda0p1_from_scratch_4h100/milestones/token_033000000000`.
Require manifest complete, tokens_seen=33,000,000,000, optimizer_step125894; state SHA256 `c30b78e5bcba8f0a09c5e215389be86778874e87fcbb9fe5211175d370bb0803`. Runtime must hash actual state before load. Eight-layer native dense causal LM, backbone281,431,040 parameters; SAE61,471,024; total342,902,064. SAE mode sidecar, hook7 after attention projection before residual, width30000, TopK32, training reconstruction coefficient0.1. Actual source/config, not a guessed Qwen model, defines computation.

Only `model.blocks[7].attn.o.weight` (1024×2048, no bias expected) is temporarily updated. Freeze all other weights and buffers, eval mode, FP32 model arithmetic, no autocast/TF32, no optimizer state imported. Compute final full-vocabulary log-softmax/CE in FP64; derivatives flow through this cast. Keep each event's own residual r. Cache c,a,r and full-vocabulary-loss derivative e at position255. NTP excludes reconstruction and AuxK even though they shaped the historical checkpoint.

All representation coordinate transforms use TRAIN means and SDs, with denominator max(SD,1e−6); no per-example length normalization of the full vector. Geometry features are computed from native c before coordinate standardization: sum of norms, absolute norm difference, dot product, cosine with denominator max(norm product,1e−12); standardize these four features on TRAIN pairs.

| Variant | Definition | Role |
|---|---|---|
| B0 | Constant raw TRAIN-pair mean m | Main no-input reference |
| B1 geometry | 4→32→1 MLP; GELU hidden, linear scalar output, biases | Simple representation readout |
| B2 full-c | Shared 2048→256→128 encoder, GELU after each layer; concat(u_i+u_j, abs(u_i−u_j), u_i*u_j), 384→128→1 head, GELU hidden, biases | Complete-vector readout, exactly symmetric |

No dropout or batchnorm. Use framework default Linear initialization with recorded software version and the registered seeds. The encoder width is a readout capacity choice; full input access does not establish an information-theoretic upper bound.

**Conditional secondary panel, after primary support:** PCA of centered TRAIN c at ranks32,128,512, exact SVD; random projections at same ranks using Gaussian matrices and QR with positive R diagonal, seeds101/102/103. Project native centered c, then TRAIN-standardize projected coordinates. Full-a uses native1024-dimensional output; SAE-a uses frozen TopK codes of native a, width30000, then coordinate standardization. Each uses the B2 topology with changed input dimension. PCA and random input spaces are shared across pair endpoints. No SAE fitting, atom selection or reconstruction insertion. Use B2's DEV-selected learning-rate/decay, train each variant for the same selected B2 epoch count and three seeds, average predictions; no separate confirmation tuning. Unequal input-layer parameter counts and representation-specific optimization may affect results, so these are operational readout comparisons, not proof of lost information. Report equal-parameter refinement as future work rather than silently change capacity.

## 8. Training Objective And Optimization

Fit B1/B2 by the mean squared error of standardized K over minibatches. AdamW with betas(0.9,0.999), eps1e−8; clip global gradient norm to1.0. DEV sweep: learning rates{1e−3,3e−4} × weight decay{0,1e−4}, constant LR, no schedule/warmup. Batch512 pairs, one GPU per independent fit, no cross-fit gradient averaging. TRAIN has64 complete batches/epoch; run50 epochs (3200 updates) per configuration/seed, no early stopping. Shuffle with that fit's seeded generator each epoch. Reject nonfinite targets, loss, gradient or parameters; no skipped optimizer updates.

Fit seeds17,29,43 for every configuration and family. At each epoch compute DEV MSE of the mean prediction across these three seeds. Select the smallest DEV MSE across the4 configurations×50 epochs for each family; exact ties choose earliest epoch, smaller weight decay, then smaller LR. Retain all three weights at the selected common epoch; do not pick a best seed. Choose q_* between selected B1 and B2 by DEV MSE; exact ties choose B1. No TRAIN+DEV refit. Freeze preprocessing, all selected weights, q_* and pair manifests before CONFIRM features/predictions are evaluated.

Fitting qualification: each retained run finite with training MSE improvement ≥1e−4 from its initialized value in standardized units; otherwise mark `FIT_UNQUALIFIED`, do not convert poor optimization to absence of information. Three seeds and this guard do not prove optimization is globally sufficient. Record learning curves for all candidates, not only winners.

**Observability:** apply [training observability contract](../../../docs/training_observability_contract.md) without inventing LM training. Backbone is frozen; LM optimizer updates=0. Pure NTP measurement tags `measurement/ntp_loss` and `measurement/valid_targets_seen` count one target per event once; prefix tokens are context, not256 supervised targets. LM-training/auxiliary-loss tags are `NOT_APPLICABLE` in a scope registry. Auxiliary predictor training writes `<run>/tensorboard/<variant/config/seed>/`, `pairs/train_mse`, `updates/train_mse`, `pairs/train_total_loss`, `updates/learning_rate`, `progress/pairs_seen`, `progress/optimizer_step`, `progress/effective_pairs_per_update`=512; component `compatibility_mse` raw=weighted, coefficient1, mean over512 pairs. Pairs_seen increments only after completed updates; repeated event appearances are pair exposures, not new LM tokens. All conditions match pair batch/order/budget. Save optimizer, RNG, epoch, within-epoch cursor and both counters; resume must reproduce the next update and avoid duplicate event steps. No language-model training curve or token-efficiency claim is made from these fits.

## 9. Conditions, Seeds, And Checkpoints

One backbone checkpoint; base construction seed20260930; fitting seeds17/29/43; projection seeds101/102/103; bootstrap seed20260931. Seeds do not add model-state replication. B0/B1/B2 mandatory; primary q_* chosen on DEV. Conditional panel: PCA3 + random9 + full-a1 + SAE-a1 =14 secondary readouts, each a3-seed ensemble. Confirm predictions and K targets for all primary models retained regardless of outcome. A condition ledger lists executed/NOT_RUN_BY_GATE/FAILED for every item.

Read [reuse index](../../../docs/training_reuse_index.md) before implementation. Reuse checkpoint/config/tokenizer; adapt `.../20260927_common_rule_controlled/scripts/smoke_worker.py` load_model/capture for this new workspace, and actual `.../20260920_s7_lambda0p1_from_scratch_4h100/dense_sae/model/modeling_qwen3_sae.py`. Source inspection confirms sample-specific residual capture and last-block positionwise tail. Reject old `make_tail` as-is: it selects vocabulary rows[100,101] and one fixed residual. New full-vocabulary per-event replay must be numerically qualified. Reject old synthetic generator, common-atom selector, normalized update and confirmation arrays. No code is copied or implemented in this document-writing turn.

## 10. Primary Metric And Frozen Analysis Plan

On1024 disjoint CONFIRM pairs, each equally weighted:

\[
Q=1-\frac{\sum_{ij}(K_{ij}-q_*(c_i,c_j))^2}{\sum_{ij}(K_{ij}-m)^2}.
\]

Use raw K, no sign partition or trimming. This is an out-of-sample MSE skill score relative to the TRAIN mean, not a score whose baseline is refit to test truth. Perform2000 bootstrap draws of1024 pair indices with replacement using NumPy PCG64 seed20260931; recompute numerator and denominator with identical indices for all variants. Report percentile[2.5,97.5] using linear quantiles. No predictor refitting in bootstrap. Intervals condition on fitted predictors and this corpus; they do not cover training-set, model-seed or semantic-source uncertainty. Disjoint deduplicated pairs are the sampling unit; report that source-site dependence may remain.

Support if lower bound>0.05; non-support if upper bound<0.05; otherwise insufficient. Predeclare0.05 as a reviewable 5% relative-MSE continuation threshold, not a measured effect or routing utility. One primary selection fixed on DEV means no test-time winner selection. Secondary scores use the same bootstrap for descriptive intervals, with no multiplicity-adjusted hypothesis claims.

Missing/nonfinite mandatory event or pair makes the affected primary run `INSUFFICIENT`; never drop or replace based on K/loss. All finite outliers remain. No checkpoint selection on confirmation. If baseline MSE is ≤100δ_K² or empirical K variance is ≤100δ_K² (§11), label `LOW_RESOLUTION_TARGET` rather than classify using unstable ratios. A sign-constant target with resolvable variation remains valid. If all K are identically constant, there is no variation to predict and the score is not interpretable.

Unsealing: after OPS/DEV gates, selected predictor/rate and scientific/config/source hashes are saved to immutable `registration.json`; produce and hash `confirmation_predictions.npz` before releasing CONFIRM targets to analysis. A measurement process may compute CONFIRM targets earlier but stores them sealed from fitting and selection. Runtime append-only receipts do not change the registration body.

## 11. Secondary Metrics And Guards

**Numerical qualification on OPS:** runtime state hash; FP32 eval; complete forward to pure final-position CE; direct autograd of W versus e*c^T, relative Frobenius error≤1e−5 (denominator max(norm,1e−12)). At other positions output-loss derivative must have norm≤1e−7 times final derivative norm; otherwise stop `POSITION_CONTRACT`. Full-shape Wc must match captured a with relative norm error≤1e−5. Tail logits must match complete forward with max abs≤2e−4 and CE abs≤2e−5. Exact no-op repeats and batch-shape/replay comparisons produce loss discrepancy δ_L=max discrepancy and K discrepancy δ_K=max absolute discrepancy against direct gradient inner products, with floors1e−10 and1e−12. Evaluate all32 OPS pairs. Batch-shape discrepancies are reported separately from exact repeat noise; the larger bound is used conservatively. At least8 OPS events must also pass temporary-W full-forward versus tail-update checks at the selected DEV rate. Restore W exactly, check all frozen tensor hashes before/after. No autograd identity pass is a scientific discovery.

**Finite-step calibration:** use first32 DEV pairs by hash, both directions; choose one common rate from

\[
\eta(\alpha)=\alpha\|W_0\|_F/\operatorname{median}_{i\in\mathrm{OPS}}\|G_i\|_F,
\quad\alpha\in\{10^{-4},3\times10^{-5},10^{-5},3\times10^{-6}\}.
\]

The denominator is one fixed OPS scale, not per-source normalization. Test candidates in descending alpha, each with its half rate. Require positive OPS median norm. A candidate passes when at both rates ≥90% of DEV directed pairs satisfy

\[
|I+\eta K|\le0.1|\eta K|+5\delta_L,
\]

≥90% of source events have own loss change<−5δ_L, ≥80% of directed effects have |ηK|>20δ_L, and every relative matrix step≤1e−3. Select first passing candidate. If none passes, record `FINITE_BRIDGE_UNQUALIFIED`; keep primary K measurement/prediction eligible if their own gates pass, and skip confirm updates (no implicit rate expansion). Zero/tiny gradient sources remain in the record.

**CONFIRM finite panel:** before truth unsealing, sort all1024 primary predicted K by (prediction,pair_id); define thirds using index floor(3*rank/1024). Take32 pairs per third by hash seed20260930, total96 pairs; no label-based choice. Evaluate both directions at selected η and η/2 from W0 independently:384 directed effects. Save actual I, source-event loss change, first-order effect, remainder, norm and restore receipt. Validate the same90% remainder and source-improvement criteria,80% resolution and maximum-step guard without retuning. Compare prediction of actual I (−η*q_*) against constant −η*m using Q_I with the §10 formula and2000 bootstraps over the96 unordered pairs, keeping all directions/rates together per draw. Use equal weight within each sampled third; report this stratified-panel estimand, not population performance. `FINITE_LOSS_PREDICTION_SUPPORTED` requires all bridge guards and Q_I lower95% bound>0; otherwise report whether numerical bridge failed or prediction transfer was not established. A valid primary K result remains unchanged.

**Secondary readouts:** raw sign fractions; rank correlation; gradient cosine κ with zero-norm values marked undefined; B1 and B2 skill scores and paired normalized MSE difference `(MSE_B1−MSE_B2)/MSE_B0`. Full>geometry supports extra readout structure; equality with both successful supports simple geometry, not absence of signal. Residuals are not an estimate of irreducible variance. Structure curves display full/PCA/random performance with rank and actual readout parameter counts; SAE compares against full-a only. Low-dimensional parity requires the full comparator itself to perform well and is conditional on these estimators; no causal localization or information-loss proof.

## 12. Known Good / Known Bad / Known Confusing Cases

Engineering tests only, not empirical evidence: a scalar quadratic same-target example yields positive K; opposite targets yield negative K; orthogonal inputs yield zero cross-term; finite differences match autograd for small perturbations. Test symmetric-pair permutation invariance, target exclusion from prefixes, duplicate endpoint rejection, deliberate train/confirm collision rejection, forbidden-field rejection, and exact checkpoint restoration. A positive-only but varying synthetic regression target must remain scoreable; a constant target must refuse an unstable variance score. A deliberately unqualified optimizer run must not produce scientific non-support. Every test writes explicit expected/observed status.

## 13. Scientific Procedure And Stage Contracts

| Stage | Input → operation → output | Decision purpose / pass / failure / handoff |
|---|---|---|
| S0 provenance | Approved scope + exact source/config → hashes, data schema/dedup/split, runtime → manifests | Exclude leakage/substitution. Stop on identity, count or schema failure; no confirm truth read |
| S1 OPS qualification |64 engineering events → native capture, full autograd, tail/no-op tests, small predictor/resume smoke → preflight and smoke receipts | Qualify objects/resources only. 64-event smoke may use temporary fits on OPS, never scientific scores |
| S2 train/dev |4096+1024 events → labels, fixed paired fits, DEV selection and finite-rate calibration → selected immutable weights/rate | Estimate accessible structure; fit failure is insufficient; finite-rate failure is separate |
| S3 freeze/confirm | Selected choices and hashes → registration, sealed predictions, release truth, primary analysis → Q/interval/verdict | One main falsifier; no feedback to S2, no pair replacement |
| S4 finite check |96 prediction-selected confirm pairs → both directions/two rates → Q_I and guard report | Link gradients to loss; separate eligibility/result; skipped only by failed DEV bridge |
| S5 conditional structure | Primary support + cached events → registered14 readouts → PCA/random and full-a/SAE curves | Secondary only; failure cannot invalidate or rescue primary; NOT_RUN_BY_GATE otherwise |
| S6 audit/report | All manifests, selected and failed conditions → independent completeness/identity/analysis verification → Summary/Detailed | Results and human judgment remain separate; no inferred research closure |

Future bounded remote smoke: OPS64 only, all engineering tests, one20-update B1 and B2 fit, one saved-state resume replay; confirm never opened. Require finite logs, schema completeness, exact resumed counters and next-step predictions within1e−6 relative error. It does not grant a full run.

Proposed resource ceiling: use [execution envelope](../../../docs/execution_envelope.md) default `h100-4-reserved`, image key `shphd-lite-0911`, existing ACP template; one allocation, four independent workers, no DDP averaging between different events/fits. Aggregate GPU allocation time≤24GPU-hours (four GPUs×6h), including remote smoke; smoke≤20min, storage≤50GiB, no automatic retries/fallback. Local read-only preparation≤60min per envelope. Check projected remaining runtime from OPS throughput with1.5 safety factor against remaining budget before full work; if it exceeds ceiling, report `RESOURCE_UNQUALIFIED`, do not reduce conditions silently. No ETA is claimed now. Device memory, runtime availability and image qualification are NOT RUN. Resource extensions or corpus enlargement require a reviewed amendment.

## 14. Algorithm, Output, And Provenance Contract

Future execution workspace (proposed; not created here): `/data/250010109/MoE_Router/experiments/20260930_natural_ntp_compatibility/`; immutable per-attempt runs under `runs/<UTC>/`. The research repository stores this Anchor/Protocol and future small reports only. Proposed script interfaces, all **NOT IMPLEMENTED**: `prepare_data.py`, `qualify_measurement.py`, `collect_events.py`, `fit_predictors.py`, `freeze_and_predict.py`, `finite_check.py`, `analyze.py`, `audit.py`. Entry interfaces are responsibilities, not claims that files exist. The implementation chat must map them to actual versioned code/config and hashes before promotion.

Required artifacts and minimum schemas:

| Artifact | Required contents |
|---|---|
| `data_manifest.json`, `events.jsonl`, `pairs_<split>.npz` | Source/tokenizer hashes, exclusions and duplicate groups, IDs/split/line/prefix/target hashes, counts, pair endpoints, construction seeds, exposure ledger |
| `features_<split>.npz` | Event ID, c[2048], a[1024], r[1024]; optional frozen SAE indices/values; no target/gradient fields in predictor export |
| `truth_<split>.npz` | Event ID, y, CE, e[1024], gradient norm, K per pair, dtype; access stage; direct G retained for OPS only, factors suffice elsewhere |
| `preflight.json`, `smoke_receipt.json` | Actual hashes, architecture checks, errors/tolerances, δ_L/δ_K, tensors-restored checks, resource estimate, failed gates |
| `fits/`, `selection.json`, `registration.json` | Every fit/config/seed/epoch, optimizer/RNG/counters, TRAIN transforms, selected ensemble and q_*, rate choices, scientific source and code hashes |
| `confirmation_predictions.npz` | Frozen pair IDs, all primary predictions, pre-unseal hash/timestamp; truth stored separately |
| `finite_pairs.csv`, `finite_results.npz` | Selection bins/IDs, source/target IDs, η, I, own loss, ηK, remainder, step norms, zero/restore checks |
| `analysis/primary.json`, `secondary.csv`, `condition_ledger.json` | Metric numerators/denominators, pair/bootstrap indices, intervals, typed outcomes, every required/conditional condition status |
| `verification.json`, `failure.json`, `environment.json`, `tensorboard/` | Completeness, provenance, numerical/analysis verification; failure stage/reason/completed work; versions/device/runtime; declared telemetry |

Write atomically and never overwrite another run. Save original errors and terminal status on failure. Resume reuses exact manifest/config, source model and sealed state, skips already verified event IDs, and restores predictor optimizer/RNG/counters; mismatches require a new attempt and eligibility decision. No source checkpoint writes; hash source and all non-W parameters before/after. Actual G matrices need not be saved for all events because the certified factors reproduce K exactly; no lossy gradient sketch in the main label. GPU worker receipts contain assigned disjoint IDs and checksum counts; never treat worker count as sample size.

Expected figures after execution: (1) confirmation prediction versus K with constant reference and Q/CI; (2) predicted strata versus measured finite I at both rates, labeled stratified-panel scope; (3) conditional rank/readout curves with full baselines and random spread. Each must name model/matrix/unit/split, counts, data source and claim limit, retain negative results and distinguish measured from schematic. Store raw figures in execution root and requested reading copies under date-local `figures/` with `SOURCES.md`. No figures/results are fabricated now.

## 15. Success / Failure / Insufficient Evidence

Main outcome is exactly §10. If Q passes via B1, report representation prediction supported with simple geometry sufficient for this readout; do not mark full-vs-B1 equality as failure. If interval is below0.05 but above0, report small accessible signal below continuation threshold. Single-sign K is valid; unresolvable variation is insufficient. Fit/data/measurement failures are not scientific refutations. Finite-loss and structural results carry independent typed statuses; neither changes the main outcome retrospectively. Structural failures preserve successful primary evidence and narrow only the affected readout claim.

A completed run may legitimately end with non-support or insufficiency. Complete factual Summary/Detailed with purpose, hypothesis, method, result or NOT RUN, failure diagnosis, evidence paths and unresolved human judgment. Do not claim negative pair subgroups are stable without an independent test.

## 16. What This Cannot Claim

This single2.81e8-parameter backbone, checkpoint, matrix, document-opening population and estimator set cannot establish universal LLM geometry, causal SAE atoms, irreducible conditional variance, long-term shared/separate benefit, expert number or a deployable router. No training-token efficiency comparison is being performed. Source-event improvement is not source-task generalization. Gradient-supervised fitting is not a wholly gradient-free method. Full-c versus full-a/SAE gaps can reflect readout capacity, not just information destruction.

## 17. Block Confirmation, Freeze, And Amendment Ledger

| Block | Submitted choice | Status / promotion dependency |
|---|---|---|
| A question | Continuous natural-NTP K prediction; geometry can support | Adopted by 2026-09-29 directive; Focus conclusion remains Unknown |
| B data | Named raw shard, first256→1, dedup,64/4096/1024/2048, disjoint evaluation pairs | Adopted; capacity/exposure qualification requires receipts |
| C task | Only representations at inference; real TRAIN K supervision | Adopted |
| D model | Exact S7 λ=0.1/33B, last attention W, fixed readouts | Adopted; runtime identity/gradient qualification requires receipts |
| E fitting | Standardized MSE, fixed sweep/three-seed ensembles, DEV selection | Adopted; fit qualification requires receipts |
| F decision | Q versus constant, threshold0.05, separate finite bridge, conditional structure | Adopted; 0.05 is this experiment's continuation criterion only |
| G execution | One allocation≤24GPU-hours/50GiB, immutable artifacts and stop rules | Smoke and pass-gated Full explicitly directed; no gate relaxation |

Historical review ledger: the researcher first requested an Anchor for review, then a full Protocol and memory, deferring code to another chat. In the new chat on 2026-09-29 the researcher explicitly requested completing the task, submitting and supervising Smoke, then submitting Full after Smoke passes. This later direct instruction adopts this version's A-G and authorizes those stages. It does not confirm a Focus-level scientific conclusion or next decision. English and Chinese are companions; the earlier reasoning report is provenance, not another execution contract.

Paper consistency review: data→pure NTP→last-W gradient→pair labels→allowed-input fitting→independent confirmation→finite-step extension are specified. Direct authorization does not pass any technical qualification: source/code/config/data identity and each stage receipt must be verified, and Full follows only a passing Smoke. Unconfirmed Focus judgment is not recorded as a scientific verdict.

Before first run, a material change reopens affected blocks. After registration/run start, preserve the scientific body and append amendments with reason, affected evidence and confirmation exposure; no threshold changes after seeing results. `NOT RUN` stays until actual receipts exist.
