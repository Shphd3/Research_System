# Protocol: common-gradient coupling through global clipping

## 0. Approval Snapshot

Document status: `APPROVED_FOR_BOUNDED_LOCAL_EXECUTION`, pending coordinating-agent source/implementation consistency review and freeze. This is an internal qualification step, not a request for another user approval. The researcher has explicitly authorized autonomous distinct mechanism analysis and execution without intermediate approval. The hypothesis, policy and decision criteria below are **AI operationalization within that authority**. Scientific interpretation and question closure are not automatically human-confirmed.

Primary Anchor: [A15_24_01](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_24_frequency_composition_common_path/subanchors/15_24_01_common_optimizer_coupling_anchor.md). No Focus is created, reset or promoted. Role: root-cause audit of one optimization rival within the existing common-path question. Purpose: distinguish observed gradient clipping from actual routed AdamW updates and test whether removing common from the routed clipping denominator improves the fixed low-feature target.

Authorized local scope: source/log audit; bounded GPU qualification; four complete T_F plus-common runs; paired evaluation; checkpoint registration and factual analysis. No new remote allocation, ordinary-MoE extension, hyperparameter sweep, base-model or CrossCoder training. GPU ceiling: 20 active minutes for qualification and four runs combined. Existing user authorization supersedes an additional design-confirmation turn; source checks and engineering gates still apply.

Treatment: `route_isolated`; control: `global`. Both have the same common branch and all model/data/optimizer settings. The only changed rule is the clipping coefficient applied to routed parameters. The primary comparison is final DEV low-feature macro NLL, treatment minus control, separately for seeds 11/22. Both negative gives exploratory support; mixed/zero/positive outcomes do not support stable improvement; missing/invalid pairs are insufficient. No significance or fresh-confirmation claim.

Execution root: `/data/250010109/MoE_Router/experiments/20261022_common_optimizer_coupling`. Freeze time, scientific-body hash, code/config manifest, current strict asset check, runtime identity and audit pass records must be filled in the provenance before formal execution. None is fabricated by this draft.

## 1. Terminology / Definitions

T_F is the existing fixed feature-frequency route: two distinct saved expert indices per valid position, each weighted 0.5. Common is a ninth expert invoked at every position with coefficient one. Every expert reads the complete cached hidden state. The routed parameter group contains eight experts; T_F has no trainable router. A reusable implementation may include router parameters when present, but no learned-router run belongs to this contract.

Raw gradient means the accumulated gradient before clipping. Actual update is the parameter difference after AdamW, including decoupled weight decay. A shadow update applies each clipping policy to clones of the same parameter/optimizer state and raw gradients; it does not train a separate model or advance the real state.

## 2. Anchor Alignment

The parent additional-common experiment changed active capacity and optimization together. This experiment holds the added branch fixed and isolates one optimizer rule. Completion requires the historical audit, four valid endpoints and fixed-state update diagnostics, followed by one bounded result record. Three steps are sufficient: audit existing observations; qualify and execute the matched policy comparison; analyze local update and endpoint effects separately. Feature regrouping and frozen-representation replacement belong to the referenced A15_25 discussion and are excluded here.

## 3. Tested Hypothesis

Removing common's direct contribution to the routed-gradient clipping denominator changes actual routed AdamW updates and lowers final DEV low-feature macro NLL for both seeds. The numerical update measurement and endpoint prediction test answer different parts of this chain. Frequent clipping alone is not a hypothesis success.

## 4. Rival Explanations

AdamW may absorb most positive gradient rescaling; later moment history may produce a different effect without endpoint benefit. The common branch can still influence routed raw gradients through the joint prediction loss. The policy does not remove that functional coupling. Both policies have identical added capacity, so a policy contrast cannot be attributed to parameter count, but it also cannot establish that the original baseline/common difference was entirely mediated by clipping. Historical observations already available before this design must not be counted as successful prospective predictions.

## 5. Data Construction And Provenance

Reuse the original Tulu data revision `6248b175d2ccb5ec7c4aeb22e6d8ee3b21b2c752` and exact prepared caches: TRAIN 1,024 dialogues / 85,548 valid answer targets; EVAL 256 / 22,446; DEV 128 / 10,340. A target is one answer next-token position, including answer EOS and excluding prompt/padding. Inputs are BF16 Qwen3-0.6B block-28 residual-post vectors, width 1,024. Original routes and feature labels come from the same 14-layer, 16,384-feature CrossCoder; activation threshold 0.051281172782182693. No cache reconstruction or new tokenization is required.

Required inherited input IDs: `data_tulu_sft_route_20261019t012300z`, `representation_tulu_sft_route_20261019t012300z`, `model_qwen3_0p6b_base`, `tokenizer_qwen3_0p6b_base`. Verify current access with `tools/check_assets.py --strict` and bind source cache/routes to the recorded producer manifests before loading. Register any additionally consumed historical asset before use. The data/representation entries and source manifests bind the feature-producing checkpoint; the worker must not silently load another dictionary.

Keep source split membership, input/target ordering, hidden normalization scale and label supports unchanged. DEV has been inspected previously and is not untouched confirmation. It cannot select policies, hyperparameters, checkpoints or stopping times. Same-position feature events overlap, and dialogues are the natural dependence clusters.

## 6. Learning Task And Permitted Supervision

Predict original next-answer-token targets through the frozen final normalization and vocabulary head. Train only the eight residual experts and common; the Base, CrossCoder and head remain frozen. Use answer-target cross entropy only. No load-balancing, spectral, reconstruction or new feature loss is introduced. The supervised target is the original corpus next token; no future token enters a route or input.

## 7. Model / Architecture And Frozen Variants

For full hidden vector \(h\) and original TRAIN RMS scale \(s\), both policies compute

\[
h'=h+s\left[\tfrac12E_{r_1}(h/s)+\tfrac12E_{r_2}(h/s)+C(h/s)\right].
\]

All nine modules are bias-free width-1,024 SwiGLUs. The two routed experts retain their original indices and weights; common replaces neither and is not averaged by three. It adds 3,145,728 parameters in both policies. Original routed initialization and isolated common initialization (`seed+987031`, random gate/up, zero down) are reused. Same-seed policy pairs must begin with exactly equal model tensors and identical sample order. Initial common output is zero. No expert capacity dropping or structural projection is introduced.

## 8. Training Objective And Optimization

Loss is the sum of valid-target cross entropies divided by the actual number of targets in the complete effective batch. Accumulate four microbatches of 128 to effective batch 512, with a final batch of 44. One epoch is exactly 168 completed updates and 85,548 valid targets per model; the token coordinates at steps 42/84/126/168 are 21,504 / 43,008 / 64,512 / 85,548.

Reuse AdamW learning rate 0.0003, betas (0.9, 0.95), epsilon 1e-8, weight decay 0.01, nine-step warmup and the inherited cosine schedule with final ratio 0.1. The inherited stateless schedule implementation is authoritative, including update indexing; no new schedule interpretation is substituted. All gradients are computed before clipping.

Let \(n_R=\lVert g_R\rVert_2\), \(n_C=\lVert g_C\rVert_2\), \(q=\min(1,1/(\sqrt{n_R^2+n_C^2}+10^{-6}))\), and \(r=\min(1,1/(n_R+10^{-6}))\). `global` multiplies both groups by \(q\). `route_isolated` multiplies routed gradients by \(r\) and common gradients by \(q\). Compute norms from the same raw accumulated gradients before mutating either group. Then execute the unchanged AdamW update. Keep the clipping stabilizer 1e-6 separate from AdamW epsilon 1e-8. There is no second global clipping pass after the treatment.

Reuse the original frozen-cache trainer and its model, loss, schedule, evaluator, checkpoint and order utilities. Adapt only clipping, policy provenance, fixed-state shadow diagnostics and their telemetry. Do not reuse a full pretraining scaffold for this cached final-layer task. Verified sources are [original trainer](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/shared_common_expert/20261022T103833Z/code/train_shared_common.py) and [configuration](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/shared_common_expert/20261022T103833Z/config/frozen.json). Preserve source hashes and copies without editing the original run.

## 9. Conditions, Seeds, And Checkpoints

Four runs only: `global_s11`, `route_isolated_s11`, `global_s22`, `route_isolated_s22`. Execute serially on the currently available local H100 MIG 3g.40gb after verifying actual device identity and free resources. This is not a new Reserved allocation. Both global controls rerun on the same device/software as treatment. Historical full-H100 outcomes are descriptive context; cross-hardware byte identity is not assumed.

Save initial weights and milestone weights at updates 42/84/126. Save `latest` and final complete training states containing model, optimizer, scheduler state or exact stateless schedule identity, RNG, order/cursor, completed updates and cumulative targets. Freeze filenames in the execution config before launch. Final endpoint is always step 168; no best-checkpoint selection. Restore qualification must verify next-update equality and telemetry-coordinate continuation. Register actually saved final states and milestone families; planned files are not assets.

At updates 1/42/84/126/168, use each run's pre-update state and that effective batch's raw gradients to calculate paired shadow updates. Record group and per-expert update norms, relative difference, dot product/cosine where both norms are nonzero, and zero-norm status otherwise. The shadow step must leave live parameters, moments, RNG, counters and gradients unchanged. Measurements are conditional on the sampled current trajectory, not interchangeable histories.

## 10. Primary Metric And Frozen Analysis Plan

For each of the original 1,694 B1 features, average final DEV per-position NLL over its active positions, then average equally across features with at least one DEV hit. The inherited fixed panel has 838 supported features and 856 unsupported. Recompute that support and stop on mismatch. Unsupported features are missing support, not zero-loss observations. DEV includes 10,340 positions and 1,701 unique low-feature-union positions.

For each seed, compute \(\Delta=L_{\mathrm{route\_isolated}}-L_{\mathrm{global}}\), in natural-log units per target under the stated macro weighting. Report both deltas and their arithmetic mean. Both strictly negative gives exploratory support; any mixed or zero direction fails the stable-improvement criterion; both positive gives exploratory non-support. Invalid or missing endpoints are insufficient. A mean alone cannot replace the per-seed rule. Tiny differences must be shown at adequate precision and interpreted against measured replay/numerical consistency.

No confidence level or significance threshold is claimed from two seeds. Feature occurrences are not independent trials. If descriptive resampling is reported, use dialogue clusters with fixed grouping and mark it secondary; no resampling result can change the seed-sign criterion. Report every planned condition; no outlier seed/feature removal, post-hoc bins or hyperparameter selection. Final DEV evaluation is released only after all four endpoints complete or an explicit partial/failure stop is recorded. The primary rule cannot change after release.

## 11. Secondary Metrics And Guards

Report overall position-mean NLL, low-union position-mean NLL and high-feature macro NLL separately. Record TRAIN/EVAL at original milestones, routed exposure, output norms, raw and post-clip gradient norms, both policy coefficients, actual parameter updates and cumulative update path lengths. Overall deterioration must remain visible even when the low-feature criterion supports the policy. Equal route exposures and target counts are mandatory guards.

TensorBoard lives under each run's `tensorboard/`. Required repository tags: `tokens/train_lm_loss`, `updates/train_lm_loss`, `tokens/train_total_loss`, `updates/learning_rate`, `progress/tokens_seen`, `progress/optimizer_step`, `progress/effective_tokens_per_update`. Use cumulative valid targets for token tags and completed updates for update tags, with progress coordinates as required by the observability contract. The only objective component is task cross entropy with coefficient one and actual valid-target denominator; auxiliary losses are `NOT_APPLICABLE`.

Register stable additional tags in frozen config for raw route/common norms, global/route clipping coefficients, actual route/common updates and routed/common exposure. Emit finite values at all applicable steps; zero-norm cosine is explicitly undefined rather than a fabricated zero. Machine-readable step records retain all per-expert values and shadow measurements. Fixed-state diagnostics do not consume training examples twice in progress counts.

## 12. Known Good / Known Bad / Known Confusing Cases

Known good: zero common gradient makes the two clipping policies coincide; equal initial model/order gives identical pre-update logits, loss and raw gradients. Qualification must show policy execution matches an independent scalar/norm reference.

Known bad: clipping common with its own norm, calculating the routed norm after global clipping, applying a second global clip, changing common coefficient, or resuming with reset moments changes the registered intervention.

Known confusing: substantially smaller clipped gradients can produce almost equal first AdamW updates. A longer cumulative parameter path is not proof of useful learning. An endpoint gain does not establish a semantic grouping mechanism. Disabling common at inference would test another question and is not a required additional condition.

## 13. Scientific Procedure And Stage Contracts

| Stage | Goal and operation | Output / acceptance | Failure and handoff |
|---|---|---|---|
| Historical audit | Read all eight original logs; bind identities; recompute clipping and actual-update statistics | `observational/` tables with complete 168-step coverage and source hashes; preserve already-seen status | Missing fields remain missing; do not infer updates from clipped gradients |
| Qualification | Check assets/source/cache/order; compare policy math; run one effective GPU update; save/restore then compare the next update; verify shadow non-mutation and required TensorBoard tags | `qualification/` identity, gradient, denominator, finite-loss, resume, token and tag checks PASS; measured ETA within remaining ceiling | Data/implementation/telemetry mismatch stops formal execution; preserve evidence |
| Matched training | Run four fixed conditions to 168 updates with unchanged data/order/config | `training/<condition>/` states, step records, milestones, finite curves and equal counts | Nonfinite values, resource ceiling or unexpected mutation stop affected work; no automatic remote fallback or extra seeds |
| Final analysis | Reveal final DEV only after the fixed endpoints; apply frozen macro rule and summarize shadow/trajectory contrasts | `analysis/` position arrays, support checks, paired table, secondary table and diagnostics | Missing or invalid pair gives insufficient evidence; no metric substitution |

The elapsed-time gate is calculated from qualification on actual hardware. It concerns feasibility, not scientific success. Partial and failed results remain in the record. This round does not automatically authorize a repaired second full experiment; harmless implementation repair before a valid formal start must retain its failure audit and new source hash.

## 14. Algorithm, Output, And Provenance Contract

Execution inputs/config/source copies live under the execution root, with `observational/`, `qualification/`, `training/`, `analysis/` and `provenance/`. Actual implementation paths and stable checkpoint filenames are frozen in the source manifest. Record software versions, device/MIG UUID, torch/CUDA, dtype, deterministic settings, config hash, input manifests, paired initialization hash and sample-order hash. Keep canonical narrative in this experiment directory; raw arrays/checkpoints remain execution-side.

GPU active-time ceiling is 20 minutes total for qualification, four models and evaluation. Use one local device, one process and two CPU threads. Inherit a 16 GiB allocated-GPU-memory ceiling, 16 GiB worker RSS and 16 GiB new output ceiling unless actual qualification demonstrates an incompatible inherited measurement; any change requires a recorded pre-start amendment under the same authorized task, not silent fallback. Stop on nonfinite values, hash mismatch, wrong counts, invalid frozen-state checks or resource overrun. Do not overwrite historical outputs. Follow `assets/README.md` for actual checkpoint registration and current selected strict checks at handoff.

## 15. Success / Failure / Insufficient Evidence

Engineering success requires qualification PASS, all four complete models, exact target/order/route pairing, durable endpoint arrays, source/config identity and required telemetry. It does not imply a method benefit. Scientific exploratory support follows the primary rule separately from the immediate-update diagnostic. If clipping changes actual updates but does not improve the primary metric, report a real optimization effect without a supported remedy. If actual updates barely change, retain AdamW rescaling as a rival rather than claiming reduced learning from clipping factors.

## 16. What This Cannot Claim

This intervention estimates the effect of one clipping policy in this model and exposed panel. It does not prove complete mediation of the original common/baseline contrast, optimal optimization, general MoE benefit, correct feature semantics, grouping quality, Rank-one validity, or long-range reasoning. The additional common branch remains present in both arms. Changes in common's later raw gradients and updates are downstream consequences of the policy, not an independently held-fixed common trajectory.

## 17. Block Confirmation, Freeze, And Amendment Ledger

User-confirmed scope: autonomous distinct mechanism analysis and execution without intermediate approvals. Source-verified: original data dimensions/counts, model, routes, learning objective and optimizer settings. AI operationalization: denominator intervention, T_F-only four-run matrix, fixed shadow steps, local ceiling and two-seed exploratory decision rule. No A–G block is represented as a separately elicited human scientific endorsement.

Internal audit ledger at draft: A question/boundary covered; B input identity requires current runtime verification; C task/source verified; D same architecture specified; E clipping rule and optimizer source specified; F primary/secondary rules specified; G runtime qualification and source/config freeze pending. Coordinating agent records consistency PASS and freeze before promotion to the authorized local scope. This internal audit does not add a user gate.

Record three concise audit passes in the result Detailed appendix: source and mathematical consistency; intervention/code/qualification consistency; independent result/denominator/claim audit. Preserve the originally frozen scientific body after formal start. Any material amendment records timestamp, old/new values, reason, already-visible evidence, affected conditions, authorization and evidence eligibility. Results and interpretation belong to Summary/Detailed, not an overwrite of this Protocol.

### Pre-execution freeze receipt

2026-10-22T15:35:06.582991+00:00; coordinator `/root`: strict input access, source/config alignment and independent clipping/shadow code review PASS. User-authorized bounded local execution is frozen; GPU numerical, resume and TensorBoard qualification must pass before full training. Exact hashes are recorded in execution-side `provenance/design_freeze.json`. Actual checkpoint names are `initial_resumable.pt`, `resumable_step{1,42,84,126,168}.pt` and `final_resumable.pt`, all complete states. Only four completed endpoints permit DEV evaluation. The 20-minute bound conservatively counts cumulative execution-process wall time, excluding between-process review gaps. This receipt supersedes draft filename and pending-engineering-review wording above; scientific choices are unchanged.
