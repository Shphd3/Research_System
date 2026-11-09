# Protocol: A17_04_E04 sharing allocation under matched budgets

[中文](protocol_cn.md) · [Child Anchor](../../../../problem_anchors/17_shared_and_interference_learning/17_04_conditional_mapping_transfer/subanchors/17_04_02_shared_routed_budget_anchor.md) · [Focus](../../../../focus/focus_conditional_mapping_transfer.md)

Document state: **APPROVED_FOR_IMPLEMENTATION_SMOKE_AND_SINGLE_SEED_ACQUISITION_PILOT**. Created2026-10-12. Draft revision:1.
Task state: `BOUNDED_IMPLEMENTATION_AND_QUALIFICATION_COMPLETE`; result state: `SINGLE_SEED_QUALIFICATION_RESULTS_AVAILABLE`; implementation state: `GPU_ENGINEERING_PASS_LEARNING_NOT_PASSED`; mechanism judgment: `Unknown`.
The researcher adopted this design and explicitly authorized implementation, Smoke and a bounded learning qualification on2026-10-12. Formal multi-seed experiment submission remains forbidden. This supersedes the document-only hold for those scopes only. Design frozen at `2026-10-12T05:36:59.199829+00:00`; scientific-body hash is recorded in the execution freeze manifest.


## 1. Purpose and approval ledger

The parent asks when shared learning incurs a cost and when differentiated processing is useful. R02 found acquired-old failure after reversed-only learning, but successful coexistence under joint supervision. This experiment asks whether parameter allocation improves joint learning under the same supervision and budgets. It compares allocation utility, rather than simply demonstrating that freezing an old copy prevents forgetting.

| Block | Candidate content | State |
| --- | --- | --- |
| A: question/boundary | Compare fully shared, known-mode separate and hybrid; document-only scope is confirmed. Utility criterion is adopted for a future formal comparison, not evaluated by this pilot. | CONFIRMED; direction HUMAN_CONFIRMED |
| B: data/provenance | Reuse registered mapping TRAIN/DEV with paired joint-reversed batches; no new labels or TEST. | CONFIRMED |
| C: task/supervision | Answer-only CE; both modes receive the same labels in every arm. | CONFIRMED |
| D: architecture | Frozen acquired-old backbone, final q/k/v/o rank-slot bank, fixed mode masks. | CONFIRMED |
| E: objective/optimization | One globally normalized CE, common fresh AdamW and budgets. | CONFIRMED |
| F: comparison/verdict | Equal-total main groups, active-rank controls, weakest-cell criterion. | CONFIRMED |
| G: execution/reproducibility | Future engineering gates,15 bounded trajectories, registered actual saves. | CONFIRMED; only Smoke/pilot authorized |

A–G design adoption comes from the current researcher instruction, not this audit. The authorized scope is bounded below; earlier runs do not authorize a new formal comparison.

## 2. Data and task

Use registered `data_a17_conditional_mapping_v1`. A sample contains visible mode, neutral command and three distinct single-token list words; the answer is the next target token after the prefix. Example schema below is illustrative; implementation must reuse the registered `input_ids`, not silently retokenize a new prompt.

| Visible input | Old mode1 target | Reversed new mode2 target |
| --- | --- | --- |
| command甲; list红 蓝 绿; answer prefix | 红 | 绿 |
| command乙; same list; answer prefix | 绿 | 红 |

The mode field differs in actual old/new prefixes. No full input has contradictory labels. Input may contain only mode, command, list and formatting. Target is never part of the supplied prefix. Mode routing reads the visible mode; verify the metadata mode agrees with its prefix. Routing must not read `world`, answer, loss, list ID or DEV outcomes.

The registered inventory contains7200 TRAIN and2400 DEV records across old/consistent/reversed worlds. Use old and reversed only:4800 TRAIN and1600 DEV. Each world has800 DEV answers:400 unseen-order and400 unseen-combination,200 per command per panel. Unseen order uses unseen permutations of familiar unordered triples; unseen combination uses wholly unseen unordered triples. Preserve split identities and report panels separately and equally combined. Existing DEV is exposed diagnosis; original TEST was exposed and must not be called untouched confirmation or accessed here. No fresh confirmation claim is available.

Reuse the existing joint sampler: five list IDs per update, both commands for each list in old mode and reversed new mode. Thus each update processes10 old and10 new valid targets. Every arm/seed uses identical ordered record IDs, prefixes, targets, padding and microbatch boundaries. Training weights are exactly50:50. A shared block receives signals from20 answers per update; an old or new private block receives eligible signals from10. This difference is the allocation treatment, not extra data. No balancing or independent per-expert normalization is allowed.

## 3. Model and implementation contract

Reconstruct the identical Qwen3-0.6B Base plus acquired-old four-weight state. Freeze **all** original model parameters, including the old q/k/v/o matrices, embeddings, output head and normalizations. At layer27, add low-rank increments to all four projections, preserving native attention, positional encoding and normalization.

For each projection, use \(\Delta W(m)=B\operatorname{diag}(g_m)A\). Main-arm factors are \(A\in\mathbb R^{16\times d_{in}}\), \(B\in\mathbb R^{d_{out}\times16}\). Masks act per sequence and apply to all its prefix positions. In mixed-mode batches, broadcasting a batch-level mode is prohibited. Effective rank is at most the count of active slots; it need not equal that count after learning.

| Main arm | Mode1 slots | Mode2 slots | Shared slots | Private slots per mode |
| --- | --- | --- | --- | --- |
| S16: fully shared updates | 0–15 | 0–15 |16 |0 |
| U8/8: known-mode separate updates | 0–7 | 8–15 |0 |8 |
| H8/4/4: hybrid updates | 0–11 | 0–7 and12–15 |8 |4 |

The frozen backbone is shared even in U8/8. H8/4/4 has a **trainable shared increment** in addition to that frozen base. Separate increments are addressable parameter blocks; unique semantic processing is not assumed. This is the minimal conditional-update prototype of the MoE question. It does not introduce full feed-forward experts, a learned router, top-k competition, orthogonality, SAE, SVD-selected directions or a load-balancing loss.

Proposed implementation, not executable training code:

```text
z = linear(prefix_hidden, A16)
z = z * mask_from_visible_mode          # same multiply in S16, with all-one mask
increment = linear(z, B16)
output = frozen_original_projection(prefix_hidden) + increment
```

Use one implementation in every arm. Do not replace masks with sparse grouped dispatch in this experiment. Use fixed gain1; no rank-dependent alpha/r multiplier. Per projection and seed, draw a master A16 with independent zero-mean Gaussian entries of standard deviation \(d_{in}^{-1/2}\), and initialize B16 to zero. Main arms copy this same master bank. Initial outputs equal the acquired-old state. Do not duplicate A blocks to equalize old/new private bases: duplication would create a symmetry and accidentally reduce S16's effective capacity. S8/S12 use the first8/12 master rows, with matching zero B; new-mode private slots have different initial basis draws. Seed variation probes this residual initialization dependence.

S8 and S12 are fully shared supporting controls with only8/12 trainable rows/columns. Pad to16 using constant frozen zeros before the same dense products; padding must not enter the optimizer parameter list. These controls match U/H active rank and test the smaller-rank rival. They have fewer stored parameters, so they are not substitutes for the equal-total S16 comparison.

## 4. Parameter and compute budgets

Projection dimensions are inherited from the actual carrier:

| Projection | Weight shape: output × input | Parameters per rank slot |
| --- | --- | --- |
| Q |2048 ×1024 |3072 |
| K |1024 ×1024 |2048 |
| V |1024 ×1024 |2048 |
| O |1024 ×2048 |3072 |
| Total | Four projections |10,240 |

A rank slot costs \(d_{in}+d_{out}\) factor parameters. Counts exclude identical frozen-base storage, which is still reported separately.

| Arm | Total trainable | Shared trainable | Private per mode | Active per example | Executed factor rank |
| --- | --- | --- | --- | --- | --- |
| S16 |163,840 |163,840 |0 |163,840 |16 |
| U8/8 |163,840 |0 |81,920 |81,920 |16 |
| H8/4/4 |163,840 |81,920 |40,960 |122,880 |16 |
| S8 control |81,920 |81,920 |0 |81,920 |16 with frozen padding |
| S12 control |122,880 |122,880 |0 |122,880 |16 with frozen padding |

For \(N\) processed prefix positions, factor forward matrix multiply-add count across four projections is \(N\times16\times10,240\); count a multiply-add as two FLOPs if reporting FLOPs. Backpropagation must preserve the same dense operator shapes and retain computation through the input at every adapter. Original model, sequence lengths, padding, kernels, dtype and checkpointing policy are identical. Main arms have identical total parameter/optimizer shapes. Runtime profiling must verify forward/backward matrix FLOPs within1% among the three main arms; otherwise the equal-compute claim is ineligible until the discrepancy is explained/repaired under the change policy.

S8/S12 share dense matrix shapes but have fewer optimizer/vector operations and padding overhead. Report those differences; do not claim exact end-to-end wall time equality. Dynamic masks must not be compiled into condition-specific sparse kernels. This compute padding buys a controlled scientific comparison, not a systems speedup. Genuine sparse activation, reduced inference FLOPs and increased expert storage require a later comparison.

## 5. Objective, exposure and optimization

Use full-vocabulary answer CE only, no auxiliary or retention penalty:

\[
J_t=\frac1{20}\sum_{i\in\mathcal B_t}-\log p_{\phi_t}(y_i\mid x_i).
\]

\(\phi\) denotes only trainable factor parameters; the base remains frozen. Microbatch5 × accumulation4 × data-parallel size1 gives20 valid answer targets per optimizer update. Divide each microbatch's summed CE by20 before backward; never average per active expert. Whole-prefix tokens count actual computation, but only answer targets count the canonical training exposure coordinate.

Adopted settings: FP32 native eager forward; the inspected parent used SDPA, so eager is a common new-arm backend choice, model training dropout disabled in all arms, fresh AdamW lr1e-4, betas(.9,.999), eps1e-8, weight decay0, constant schedule, global factor-gradient clipping1. No inherited old Adam moments, no differential learning rates or per-mode step scaling. Common optimizer settings do not imply identical effective update norms; record measured per-mode effective matrix displacements and clipping coefficient. Do not normalize those displacements post hoc.

| Budget point | Updates | Total valid answers | Old answers | New answers |
| --- | --- | --- | --- | --- |
| Primary |240 |4800 |2400 |2400 |
| Terminal qualification/secondary trajectory |1200 |24000 |12000 |12000 |

Save/evaluate at0,1,16,50,120,240,600,1200, corresponding to0,20,320,1000,2400,4800,12000,24000 targets. Train all eligible arms to1200; do not early-stop a favored arm or select a best DEV checkpoint. Seeds29/43/71 change both adapter initialization and batch order, paired across arms. All15 trajectories share one old acquisition. The primary endpoint is240, chosen to test the previously practical acquisition budget, not from new results. Earlier learning curves and1200 are secondary; they cannot rescue a failed240 utility criterion. No adaptive rank/LR sweep is authorized by the draft.

## 6. Readouts, decision rule and rivals

For each checkpoint, seed, mode and unseen panel, report CE in nat/answer, full-vocabulary argmax accuracy, and rule margin

\[
M=\operatorname{mean}\left[\log p(y\mid x)-\log p(o\mid x)\right],
\]

where \(o\) is the opposite endpoint required by the other command-position mapping. Margin compares the two rule answers, while full-vocabulary accuracy also tests other candidates and words. Compute candidate mass \(P_C=\sum_{w\in\{L_1,L_2,L_3\}}p(w\mid x)\), access CE \(-\log P_C\), and conditional-choice CE \(-\log[p(y\mid x)/P_C]\). Their sum equals answer CE samplewise. A CE decrease alone cannot prove rule learning; these readers retain the candidate-probability rival.

Primary \(Q_{\min}\) is the minimum accuracy of eight mode×command×panel cells. Per seed and routed arm define \(d_s=100(Q_{\min,route,s}-Q_{\min,S16,s})\) in percentage points. Define analogous active-rank comparisons U−S8 and H−S12. Proposed typed outcomes:

| Outcome | Exact proposed condition | Permitted interpretation |
| --- | --- | --- |
| SUPPORTS_LOCAL_ALLOCATION_UTILITY | At240, every routed seed has Qmin≥.95; mean paired gain≥5pp and every seed gain>0 versus both S16 and its active-rank shared control; old and new panel-combined accuracies each lose≤1pp per seed versus each comparator; engineering/data/compute guards pass. | This allocation improves joint competence under the stated storage/exposure/compute budget. |
| RANK_OR_OPTIMIZATION_RIVAL_SURVIVES | Gains over S16 fail the corresponding S8/S12 comparison. | Cannot credit mode allocation; a smaller shared rank may suffice. |
| NO_FIXED_BUDGET_ADVANTAGE | Shared qualifies and no routed arm passes the registered utility rule, including all-arm ceilings. | No demonstrated reason to separate at this tested budget; equal success is retained. |
| ALLOCATION_WEAKENED | Shared qualifies but the routed allocation fails or harms one mode. | Private allocation may lose useful capacity/transfer here. |
| INSUFFICIENT | All designs fail eight-cell95% qualification at1200, or comparison qualification remains invalid. | This new factor family/config is not an adjudicated architecture test. |

When no support occurs and some arms remain underqualified, report the exact cell failures rather than forcing a binary architecture verdict. CE and margin are explanatory evidence, not replacement success criteria. Report CE regressions explicitly even when accuracy-based support holds; such support is about rule accuracy at this budget, not universal loss dominance. H beating U does not identify semantic common/unique functions: it changes the shared/private allocation and active capacity together.

The95% floor requires both conditional rules to work;5pp requires at least10 additional correct answers in the weakest200-answer cell and protects against calling saturated fractions a material gain;1pp is a proposed tolerance for task-average tradeoffs. These are AI operational criteria, not calibrated significance levels or researcher scientific acceptance. Predeclare both routed comparisons; do not select one after inspecting DEV and call that an unbiased winner.

Unit of observation: one answer. Data resampling unit: underlying list, keeping all its mode/command records together within each unseen panel. Stochastic comparison unit: one paired continuation/init seed, conditional on one acquired-old model. Report all three paired effects, mean/sampleSD/range and every cell denominator; no population-level independence claim. Optional descriptive95% intervals use2000 within-panel list-cluster bootstrap replicates with seed20261012, then average seeds, and are conditional on this old model; they do not override the all-seed/size rule. No p-values or claims of multiplicity-controlled significance. Do not exclude outliers, silently substitute missing seeds or impute failed readouts. A missing arm/seed leaves its utility contrast insufficient.

Key rival protections: same old/new labels remove extra old supervision; same total rank removes extra stored capacity in main arms; S8/S12 probe effective-rank regularization; same initialization function and paired batches constrain start/data differences. Known-mode routing supplies privileged visible conditional information in the allocation operator, so this estimates an oracle-mode architecture benefit, not learned-router benefit. The same information is already in the dense model prefix. Factorization and optimizer dynamics remain a bounded architectural package.

## 7. Small shared-update bridge (supporting, proposed)

At fixed240 snapshots of the three main arms, restore the same snapshot before each source experiment. Use one fixed five-list TRAIN window, ten old answers or ten reversed-new answers. Start a fresh diagnostic AdamW state with the same hyperparameters and a ten-target loss denominator. Apply one actual source-only step and evaluate both modes on the full1600-record DEV view. Report \(\Delta L_{s\to r}=L_r(\phi+\delta_s)-L_r(\phi)\) and changes in recipient accuracy/margin; \(\delta_s\) is the measured applied factor displacement, not a hypothetical SGD gradient.

This gives18 full source interventions (3 arms×3 seeds×2 sources). For H only, also apply the shared-block portion or source-private-block portion of the same measured factor displacement separately, restoring the baseline each time:12 additional conditions. Use actual factor replacement plus complete forward; no gradient inner-product, SVD or SAE analysis is needed. The portions need not have additive downstream loss effects. Fresh moments and decay0 prevent inactive private parameters moving through carried optimizer momentum. Preserve normal mixed-training moments in the saved trajectory; the diagnostic is explicitly a new local intervention.

U's cross-mode no-change is an implementation identity, not a discovery. Reject a broken mask/frozen-base implementation if another mode changes beyond the numerical no-op tolerance. Finite effects in S/H can connect shared update allocation to concrete predictions but cannot explain1200-step optimization by themselves. A source step below numerical resolution is `UNRESOLVED_LOCAL_EFFECT`, not evidence of no reusable function. Primary utility remains the joint trajectories.

## 8. Source reuse, assets and provenance

Inspect `docs/training_reuse_index.md`, the actual source, and observability contract before future code adaptation. Reuse selected native `AnswerLM`/collation, split validation, `make_batches(...,'joint_reversed')`, finite output readers, FP32 carrier and checkpoint/TensorBoard guards from `/data/250010109/MoE_Router/experiments/20261011_a17_single_layer_mapping_transfer/source/transfer.py` and its audited imports. **Adapt** the loader to freeze original q/k/v/o and install factors; the current loader makes those four full matrices trainable and must not be reused unchanged. Adapt parameter lists, mode masks, metadata and exact resume. Do not reuse an old o-only LoRA wrapper or production router without inspection: scope and optimizer contracts differ. Factor-bank implementation is currently NOT_IMPLEMENTED.

Required input asset IDs:

- `model_qwen3_0p6b_base_official_a5`
- `tokenizer_qwen3_0p6b_base_official_a5`
- `data_a17_conditional_mapping_v1`
- `adapter_a17_04_single_attention_20261011t145214z_full_attn1_adam_main`

Parent source config: `/data/250010109/MoE_Router/experiments/20261011_a17_single_layer_mapping_transfer/runs/transfer_20261011T160256Z/config.json`.
Old member: `/data/250010109/MoE_Router/experiments/20261011_a17_single_attention_acquisition/runs/single_attention_20261011T145214Z/full/attn1_adam/main/checkpoints/update_01200/state.pt`; member SHA256 `48595673c24579164e271cfeb1b86be6a234e2dfc06218b74d8ca07e16411b75`. The adapter asset is a family; choose this1200-step member, never the family's step0 member.
Data manifest SHA256 `a2c899d858cc267d3ec10bf2ca189c6915d01e0f7026bd1369f1541daac7dc2b`; TRAIN `3b57c72970cba2a5478caab85369bfb53804094960422ba7e2fca9ddcf14ca03`; DEV `e382ae70dea12c65aeb9178e1c32ec1eb205039181be2dbc38b38ec9379a0471`.

These identities were read from the prior source config, not freshly rehashed payloads. Before actual payload use, query the registry and run `tools/check_assets.py --strict` for these four IDs; verify exact member/parent and all data identities. Reading these documents requires no model load. Future code/config/source hashes, environment/image, execution receipt and actual output IDs are Unknown until implemented/submitted. Proposed execution owner: `/data/250010109/MoE_Router/experiments/20261012_a17_shared_routed_budget/`; canonical design remains here. Do not store tensors/logs/checkpoints in this repository.

## 9. Qualification, observability and future execution

Everything in this section is planned **NOT RUN**. Model-independent preflight validates masks/counts/schema, complete command pairs, balanced label marginals, record order, exact list split separation and route-prefix agreement. No regeneration of labels or filtering by performance. Known-good initial old predictions must match the acquired-old checkpoint; zero-B adapters must preserve logits/CE and all accuracy exactly within max-logit1e-5/CE1e-6 numerical tolerances. Known-bad route swapping must fail the route-prefix guard. Known-confusing constant candidate probabilities must not qualify as rule learning.

Future Smoke: five arms, seed29, eight updates each with independent2-step checkpoint replay, finite objectives/readouts, exact parameter counts, original frozen hashes, mode-isolation checks, per-sequence mixed-mode routing, nonzero active learning and required logs. Compare full shared update semantics to an unmasked rank16 implementation. Validate dense forward/backward FLOPs, counters, saved fields and RNG reconstruction. Engineering failures stop before full submission. Smoke need not learn the task and cannot establish architecture utility. Planned15 scientific trajectories are5 arms×3 seeds,1200updates each; if all full trajectories remain unqualified, retain the insufficiency instead of expanding rank after seeing results.

Future resource proposal: four H100 reserved GPUs, independent one-GPU lanes, not four-way data parallelism. Execute at most four independent trajectories concurrently. Proposed ceiling8 wall-hours/32 GPU-hours for the full four-GPU allocation, including lane waves; benchmark/ETA Unknown. A ceiling hit preserves partial results and stops, without automatic resubmission. Resource profile/image/submission wrapper must be checked against the current execution envelope after explicit run authorization. None is selected/submitted now.

Follow [training observability](../../../../../../../docs/training_observability_contract.md) without weakening it. Each lane logs `tokens/train_lm_loss`, `updates/train_lm_loss`, `tokens/train_total_loss`, `updates/learning_rate`, `progress/tokens_seen`, `progress/optimizer_step`, `progress/effective_tokens_per_update`. Global/token denominator is20; training total equals LM CE because no auxiliary term exists. Router balancing/SAE losses are NOT_APPLICABLE. Also log old/new loss/exposure, actual processed prefix tokens, masks/route counts, stored/active parameter counts, clipping coefficient and effective per-mode matrix displacement norms. Each completed accumulation window advances20 targets; skipped/invalid updates are fatal and explicitly recorded rather than silently changing exposure. Evaluation has no smoothing; primary plot x-axis is valid targets, update count is secondary and wall-time is throughput only.

Required saves: each planned milestone's factors plus optimizer/scheduler state, Python/NumPy/Torch/CUDA RNG, counters, data cursor/ordered record IDs, masks, names/counts, dtype/kernel settings, parent/old/data hashes, source/config/Protocol hashes and TensorBoard segment identity. Retain old/base references to reconstruct full weights. Freeze checks cover every original model tensor and zero padding buffers. Fresh training and external-process replay must produce identical deterministic updates; nondeterminism invalidates exact-resume eligibility until fixed. Save state files under `<run_root>/<arm>/seed_<seed>/checkpoints/update_<step>/state.pt` and atomic manifests, not `latest` alone. Register actual Smoke and Full save families separately through the asset lifecycle, with actual member digests/progress and resume evidence; never register merely planned outputs.

## 10. Deliverables, interpretation and freeze policy

No new Summary exists because this experiment is NOT RUN. Future outputs: bilingual Summary/Detailed, per-seed eight-cell tables, old/new CE/accuracy/margin panels and equal-weight combined tables, candidate decomposition, matched-budget table, unsmoothed trajectory figures with valid-answer x-axis and named units, actual profiles/guards, local-update table, actual asset receipts and missing-save log. Histories and evidence belong once in Detailed/execution; meeting text derives from those outcomes.

The meeting update **now** is a change in the next test, not an experiment finding: “Shared parameters can represent both rules. We will hold supervision and resources fixed, and test whether allocating some updates by mode makes joint learning more effective. If it does, we can then ask how to learn that allocation from inputs.” Do not announce that common and unique functions have been discovered.

Before execution, confirm A–G and record the exact authorized scope plus immutable scientific-body/config/source identities. After first execution, preserve this registered body and record append-only amendments with before/after, reason, approval, data visibility and eligibility impact. The current document audit checks semantic consistency and arithmetic only; it does not promote design, authorize any run or change the parent's scientific judgment.


## 11. Current bounded authorization and qualification procedure

The user requested asset registration, implementation of all five arms, Smoke and a check that low-rank increments can learn both rules, with **no formal experiment submission**. Use one h100-4-reserved ACP engineering/acquisition job, not the planned15-trajectory formal run. Seed29 only. First complete8 Smoke updates per arm and exact external-process step1-to2 replay, with the declared schema, budget, exposure, prefix routing, frozen-byte and compute guards. Only after all five engineering cases pass, start fresh factor/optimizer states for a240-update learning qualification on all1600 DEV records. If every arm passes all eight95% cells, stop the pilot at240. Otherwise continue **all five** from their actual240 states to1200, with the same data order and settings; retain failures without changing rank/LR. This adds an engineering qualification stage, not a new architecture-utility hypothesis. Single-seed differences are descriptive; the formal criterion requiring three seeds is NOT_EVALUATED. Section7's optional30 local interventions are NOT_RUN in this scope.

Prepared assets now bind the same records as joint and partitioned views: `data_a17_shared_routed_joint_v1` and `data_a17_shared_routed_mode_partition_v1`, under `/data/250010109/MoE_Router/experiments/20261012_a17_shared_routed_budget/data/mapping_view_v1`. Joint4800 TRAIN/1600 DEV equals the disjoint unions of mode1/mode2 views. These views add no samples/labels and do not change the task. Routing signatures are exact first-four input token IDs: mode1 `[100144,5122,14777,1773]`, mode2 `[100144,5122,40820,1773]`; metadata agreement is independently checked before loading into the trainer. The factor module reads those input signatures, not row world/target metadata. Engine and raw outputs remain execution-side. Implementation/qualification approval does not authorize commit/push.


## 12. Execution status and result links

Authorized task pt-1rb3s2t0 completed. Five engineering Smokes/replays pass; five1200-step acquisition pilots complete;55 real states registered. No formal submission. Registered scientific body and thresholds remain unchanged. [Summary](summary.md) · [Detailed](detailed.md) · [manifest](artifact_manifest.json).
