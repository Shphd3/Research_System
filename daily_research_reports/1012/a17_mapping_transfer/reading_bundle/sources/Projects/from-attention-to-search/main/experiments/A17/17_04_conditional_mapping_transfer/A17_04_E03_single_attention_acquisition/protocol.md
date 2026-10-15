# Protocol: A17_04_E03 single-attention acquisition

## 0. Approval Snapshot

- Document status: `APPROVED_FOR_TWO_ARM_ACQUISITION_SMOKE_AND_FULL`. The researcher explicitly requested the final attention layer's Q/K/V/O weights, one SGD arm and one AdamW arm, then instructed us to finish this small test before considering later steps. No further transfer run is authorized.
- Approval status: implementation, bounded engineering Smoke, exact external-process resume, the two finite training arms and factual delivery are authorized. Scientific mechanism judgment and parent question closure remain `Unknown`.
- Block audit: A–G consistent within delegated diagnostic scope; cross-block consistency `PASS`. Numerical settings and reporting conventions below inherit E02 or are AI operationalization of the authorized test; they are not researcher scientific confirmation.
- Registered revision: `a17_04_e03_single_attention_acquisition_v1`. Initial measurement state: `NOT_RUN`. Freeze this bilingual Protocol, owning Anchor/Focus snapshot, source/config/data identities and current input access before the first GPU run. The actual timestamp and hashes belong in the execution freeze manifest.
- Purpose: determine whether opening only the last attention layer's four projection weights is a feasible neutral-command acquisition route under either frozen optimization package, after final-output-projection training failed and final-four-layer attention AdamW succeeded.
- Primary Anchor: [A17_04_01 acquisition diagnosis](../../../../problem_anchors/17_shared_and_interference_learning/17_04_conditional_mapping_transfer/subanchors/17_04_01_rule_acquisition_diagnosis_anchor.md). Active [Focus](../../../../focus/focus_conditional_mapping_transfer.md) keeps the parent conditional-mapping question and its claim boundary.
- Tested premise/model term: the allowed trainable set \(T_j\) may constrain command-dependent selection. This run reduces the known successful attention scope to the final layer; it does not prove a mathematically minimal parameter set.
- Role: `root-cause audit`; old mode only. Primary metric: the minimum full-vocabulary DEV accuracy over both commands and both unseen-data panels; qualification requires every cell at least80% at the fixed endpoint.
- Conditions: `attn1_sgd` and `attn1_adam`. Both train exactly four layer27 q/k/v/o weight tensors, 6,291,456 parameters; all other parameters freeze.
- Held fixed: registered Base, neutral input/target data, seed29, list/label order, answer-only CE,20 targets/update, checkpoints and final exposure. Changed: SGD versus AdamW together with their inherited learning rates and resulting update dynamics. Not held fixed: actual displacement size, preconditioning or FLOPs relative to older scope controls.
- Pass: an engineering-eligible arm reaches at least80% in all four final DEV cells. Non-support: a valid arm does not qualify within its finite budget. Insufficient: required primary cells or eligibility evidence are missing/invalid.
- Completion: two independent160-update microfits, independent Base restarts for two1,200-update main runs, all specified readouts/saves, qualified Smoke and actual output registration; success is not required for completion.
- Cannot claim: a pure optimizer effect, pure parameter-count cause, all attention parameters trained, minimum necessary layer/parameter count, statistical replication, transfer/interference, expert/SAE mechanism or question closure.
- Approval decision after delivery: report results and stop. Any consistent/reversed new-mode experiment or additional scientific branch requires subsequent researcher authorization.

## 1. Terminology / Definitions

An **old-mode record** contains visible mode one, neutral command甲 or乙, a spaced list of three distinct candidate words, and one answer token. 甲 selects the first word;乙 selects the last. A **list pair** asks the same list with both commands. Each fitting batch contains complete pairs.

An **answer target** is the one nonignored next token after the answer prefix. Prefix and padding tokens do not contribute to CE or the valid-target budget. **Full-vocabulary accuracy** asks whether the highest-probability token in the entire vocabulary is the correct target; restricting the choice to three candidates cannot replace it.

`order_new` tests an unseen ordering of a familiar unordered triple. `combination_new` tests an unseen unordered triple. **Microfit** checks fitting of64 fixed training targets. **Main** restarts from Base and independently learns all2,400 old TRAIN records. Microfit weights never initialize Main.

**Single-attention scope** here means only layer27's q/k/v/o projection weights. Q/K/V can change attention retrieval and information combination; O changes the output projection. Attention normalization, biases and all remaining parameters are frozen. This is more than Q/K/V-only training, and less than training every parameter associated with an attention module.

## 2. Anchor Alignment

E02 found a feasible neutral-task route with the final four attention layers. Its projection-only AdamW condition did not qualify. This follow-up narrows that scope while retaining the task and acquisition reader. It addresses the acquisition prerequisite; it does not revise the parent transfer hypothesis. [E02 Summary](../A17_04_E02_rule_acquisition_diagnosis/summary.md) supplies the historical observation, not new confirmation evidence.

| Item | Anchor clause/model term or rival | Why needed/evidence role | Supporting / non-supporting / insufficient | Artifact |
|---|---|---|---|---|
| Two single-layer arms | Section4 trainable set \(T_j\); section6 qualified acquisition | Test whether a smaller attention scope can supply a learned old starting point | Final all-cell qualification / valid nonqualification / invalid or missing cells | Endpoint table and tensor inventory |
| SGD versus AdamW | Optimization rival in section3 | Check whether qualification depends on the inherited optimization package | One/both qualify, preserving scale confound / neither qualifies / invalid comparison | Matched trajectories and displacement norms |
| Tiny/full restart | Section5 fitting versus generalization | Separate tiny fitting from DEV performance without transferring fitted weights | Record each observed pattern / tiny success cannot rescue Main failure / absent restart guard | Tiny/Main state and readouts |
| Frozen TRAIN and two DEV panels | Section4 accuracy minimum | Prevent one command or familiar data from dominating qualification | Four DEV cells meet threshold / at least one valid cell fails / incomplete readout | Cellwise/paired tables |
| E02 B/C reference | Scope comparison and computational-range rival | Place the new scope between known projection/four-layer routes | Descriptive matched-exposure comparison / scope alone not identified / inaccessible raw reference | Source-bound reference table |

## 3. Tested Hypothesis

AI candidate H: opening layer27's four projection weights can establish command-dependent selection within the inherited finite budget under at least one frozen optimizer package. The prior successful four-layer route does not imply that one layer must succeed. Qualification under only AdamW would establish a package-dependent feasible route; qualification under both would establish feasibility under both tested packages.

The falsifier is a valid endpoint whose minimum DEV command/panel accuracy remains below80%. Failure of both arms rejects their practical sufficiency within this budget, not the possibility of any single-layer solution. An invalid training or measurement implementation leaves the corresponding empirical claim insufficient.

## 4. Rival Explanations

1. Four-layer success required changes at earlier attention layers. Both new arms hold earlier layers frozen. One-layer success weakens that necessity here; failure does not prove universal necessity.
2. Optimization package rather than scope determines fitting. Two arms use inherited SGD/AdamW settings. Because their learning rates and actual displacements differ, this is not an isolated optimizer-family or equal-step comparison.
3. Candidate probability improves without command selection. Keep candidate mass, conditional-selection CE, paired-list success, command response and full-vocabulary errors separate.
4. Tiny examples can be memorized without generalization. Main restarts Base and reads two fixed unseen panels separately.
5. Labels, tensor selection, normalization or resume may be wrong. Data identity, exact runtime tensor inventory, global four-tensor clipping, frozen-state checks, native CE and external-process replay protect eligibility. Engineering PASS is not scientific acquisition.
6. DEV is already exposed and one seed can be favorable. Treat this as bounded diagnosis; no untouched confirmation or seed-replicated inference is claimed.

## 5. Data Construction And Provenance

Do not generate a new dataset. Reuse only the `neutral` members of registered `data_a17_mapping_acquisition_diagnostic_v1` at `/data/250010109/MoE_Router/experiments/20261011_a17_mapping_acquisition_diagnostic/data/acquisition_v1`. Required model and tokenizer asset IDs are `model_qwen3_0p6b_base_official_a5` and `tokenizer_qwen3_0p6b_base_official_a5`; exact Base directory `/data/250010109/model_cache/Qwen3-0.6B-Base-official`. Run current selected `tools/check_assets.py --strict` before payload use and bind file hashes in the freeze.

`train_neutral.jsonl` has1,200 lists/two commands=2,400 targets. `dev_neutral.jsonl` has200 lists/two commands in each unseen panel=800 targets. `train_panel_neutral.jsonl` is a fixed200-list/400-target seen-training panel. `tiny_neutral.jsonl` has32 lists/two commands=64 targets. The existing model-independent selection and split ownership remain unchanged. Preserve record/list/pair IDs, vocabulary, words, neutral prefix, input IDs, target IDs and panel fields exactly; no labels, delimiter or command wording change.

Verify hashes and schema, first/last labels, paired commands, prefix-plus-answer tokenization, source split ownership and the original allowed permutation-versus-combination overlap. Some input words in spaced lists use a different token sequence from their single-token answer; this inherited encoding is logged rather than changed. Formal training/readout must never load original TEST, explicit or normalized views, mode two or historical mixed DEV/TEST prediction JSON.

E02's original audit exposure is historical and cannot be erased. This new run uses only fixed TRAIN/DEV and is not untouched confirmation. Historical reference values may be read from the canonical E02 Summary. Loading raw E02 reference readouts requires their current registered analysis asset check and TRAIN/DEV-only filtering before use; it never requires opening TEST.

## 6. Learning Task And Permitted Supervision

For `模式：一；口令：甲；列表：红 蓝 绿；答案：`, predict红; with乙, predict绿. Use the actual registered neutral prefix instead of constructing these illustrative punctuation variants. Compute loss only on that answer token. No prefix-language loss, extra task, explanation label, distillation, answer replay, natural-text sample, SAE or hidden teacher is permitted. The selected task asks whether a visible command changes endpoint selection; lower CE alone cannot establish that behavior.

## 7. Model / Architecture And Frozen Variants

Use the registered28-layer Qwen3-0.6B Base, native FP32 SDPA forward, evaluation mode without dropout, deterministic algorithms and no TF32. Both arms start at byte-identical Base. No activation cache may freeze an upstream computation that now depends on trained Q/K/V.

| Arm | Trainable tensor names | Count | Optimization package |
|---|---|---:|---|
| `attn1_sgd` | `model.layers.27.self_attn.{q_proj,k_proj,v_proj,o_proj}.weight` | 6,291,456 | Plain SGD |
| `attn1_adam` | Same four weights | 6,291,456 | AdamW |

Exact weight shapes are Q2,048×1,024; K1,024×1,024; V1,024×1,024; O1,024×2,048. Enumerate actual runtime names/shapes, require exactly four tensors, and check total before the first update. Freeze all earlier layers, attention biases/q-k norms, MLPs, embeddings, final norm and vocabulary head. Check frozen version counters during updates and byte identities at initialization and each stage end. Saves record the frozen-state identity; they do not independently rehash all frozen weights. This is three times the E02 projection scope and one quarter of the four-layer scope. It jointly changes parameter count and available attention computation; it does not isolate capacity alone.

## 8. Training Objective And Optimization

For an effective batch of20 valid answer targets, the empirical objective is

\[
L_j(\theta_{T_j})=\frac1{20}\sum_{i=1}^{20}-\log p_{\theta_{T_j},\theta_{\bar T_j}}(y_i\mid x_i).
\]

Here \(T_j\) is the four trainable weights, \(\bar T_j\) their frozen complement, \(x_i\) the neutral prefix and \(y_i\) its answer token. CE uses natural-log units per valid target. Four microbatches of five contribute loss sums divided by20. Prefix/padding targets are ignored. No auxiliary term or regularizer is enabled; component registry is empty/NOT_APPLICABLE.

SGD: learning rate 0.01, no momentum, no weight decay. AdamW: learning rate 0.0001, betas (0.9,0.999), epsilon 1e-8, weight decay 0. Both use constant rates and clip the aggregate gradient across **all four tensors** at global L2 norm 1 before updating all four weights. For gradient tuple \(g\), use one scale \(\alpha=\min(1,1/\lVert g\rVert_2)\), then SGD applies \(\Delta W_k=-0.01\alpha g_k\) to every selected matrix \(k\). Per-matrix clipping or updating only the original O tensor violates the contract.

Microfit:160 completed updates×20=3,200 targets/arm. Main: restart Base/optimizer/RNG and perform1,200×20=24,000 targets/arm, ten full TRAIN exposures. Total two-arm fitting is54,400 targets:6,400 tiny and48,000 Main. No adaptive continuation, early stopping, learning-rate search, additional seeds or arms. Record raw/clipped gradient norms, actual combined parameter displacement, relative displacement and prefix token counts; equal answer exposure does not equal actual update magnitude.

## 9. Conditions, Seeds, And Checkpoints

Use training-order seed29 in both independent arms; preserve complete pairs and identical batch/list/label order. Each independent worker has batch20, microbatch5 and accumulation4; data-parallel size is1. A four-GPU node does not multiply tokens/update by4.

Main save/evaluation milestones:0,1,240,600,1200 updates=0,20,4,800,12,000,24,000 valid answers. Tiny saves0,1,160 and reads its own64 targets plus fixed TRAIN/DEV at0 and160. All endpoint readers retain per-command and per-panel fields. Fixed final1200 is primary; earliest qualifying saved checkpoint is descriptive and not a stopping/selection rule.

Smoke exercises both tiny and main paths for3 updates/arm/path, from independent Base starts:120 gradient targets total. A fresh process restores step1 and reproduces step2 for both paths/arms:80 replay targets separately counted. Compare all trainable weights, complete optimizer state, RNG, counters and next-batch IDs byte-exactly. Save resumable tensors, optimizer/constant schedule, Python/NumPy/CPU/CUDA RNG, update/target counters, stage/arm, data cursor and order, parent/source/config/data hashes. These are adapters requiring exact Base, not standalone LMs.

## 10. Primary Metric And Frozen Analysis Plan

Let \(\operatorname{Acc}_{j,c,p}\) be correct full-vocabulary predictions divided by 200 targets for arm \(j\), command \(c\in\{甲,乙\}\) and DEV panel \(p\in\{\mathrm{order\_new},\mathrm{combination\_new}\}\). Freeze

\[
Q_j=\min_{c,p}\operatorname{Acc}_{j,c,p},\qquad \text{qualification: }Q_j\ge0.80.
\]

This inherited80% convention prevents averaging over an unlearned command/panel. It is not a confidence level or universal mastery definition. Primary endpoint is Main update1200. Report exact correct/total counts for all four cells, each panel's400-target mean, equal-weight combined800-target mean, and paired arm differences on identical records. Report fixed TRAIN panel separately. Report every saved milestone and first saved qualification without selecting the best later checkpoint.

Observation unit is a record; joint-command observations use a list. Independent training realization is one seed, not800 samples or four GPU replicas. No p-value, population interval, multiplicity-adjusted confirmation or three-seed conclusion is planned. No outlier/list/failed-arm exclusion is allowed. Missing primary cells make that arm insufficient; invalid engineering is not scientific non-support. Secondary losses cannot rescue failed primary qualification.

Compare the two new arms at matched target counts. Use E02 projection AdamW and four-layer AdamW only as source-bound descriptive historical references at common milestones; reproduce their input, batch and optimizer identities before claiming matched scope comparison. An SGD/AdamW difference leaves rate, preconditioning and displacement confounded. All settings freeze before new outputs are visible. DEV is exposed diagnostic data; TEST remains excluded. Analysis files under `<run>/analysis/` contain endpoint, cellwise trajectory, paired-command and loss-decomposition tables plus eligibility manifest.

## 11. Secondary Metrics And Guards

Record CE; candidate probability \(P_S=\sum_{w\in S}p(w\mid x)\) for the three list words \(S\); access loss \(-\log P_S\); conditional selection loss \(-\log[p(y\mid x)/P_S]\). Their sum is exactly CE. Report correct-versus-opposite endpoint log-probability margin and correct-versus-strongest-full-vocabulary-competitor margin/token ID. Output accounting does not establish an internal mechanism.

For each list pair, record both-correct and same-argmax indicators. With \(s_c=\log p(L_3\mid x_c)-\log p(L_1\mid x_c)\), command response \(a=(s_{乙}-s_{甲})/2\) shows whether the command changes endpoint preference in the expected direction. Positive mean alone cannot qualify the task; preserve middle-word/full-vocabulary competition.

Each arm/stage writes `<run>/<phase>/<arm>/<stage>/tensorboard/` and raw JSONL metrics. Required tags are `tokens/train_lm_loss`, `updates/train_lm_loss`, `tokens/train_total_loss`, `updates/learning_rate`, `progress/tokens_seen`, `progress/optimizer_step`, `progress/effective_tokens_per_update`. Token-loss steps use cumulative completed valid targets; update-loss steps use completed updates. For each stage, count20 targets per completed update once; no DDP aggregation across arms. Restore coordinates on resume without conflicting event steps. Tiny and Main counters are stage-local, with separate reset provenance; fitting totals sum actual completed stages rather than treating a reset as uninterrupted training.

Guards: finite losses/gradients/weights; no skipped updates; independent counts and20 batch IDs/update; no-op evaluation identity; exact tensor inventory and frozen-state identity; CE decomposition error<2e-5 nat; exact external-process replay; unchanged freeze hashes before/after. Failed guards stop the affected branch and retain logs/states. Four-device node verification and per-worker one-device visibility are engineering evidence, not scientific repetitions.

## 12. Known Good / Known Bad / Known Confusing Cases

- Good: the same list has甲→first and乙→last; exact Base repeated no-op evaluation agrees. All four intended tensors are present/trainable and every other tensor frozen.
- Bad: wrong target position, contradictory labels for an identical prefix, missing a command, TEST or mode-two input, per-matrix rather than global clipping, only O updated, hidden cached Q/K/V computations, or a missing/altered resume counter. Reject or mark affected branch ineligible.
- Confusing: CE falls while command switching remains poor; tiny succeeds while DEV fails; SGD and AdamW differ in actual step size; one layer succeeds without proving other layers unnecessary for other tasks. Preserve these distinctions.

## 13. Scientific Procedure And Stage Contracts

| Stage | Goal / input | How and why | Expected output / artifact | Pass, failure and handoff |
|---|---|---|---|---|
| Preflight | Qualify actual registered neutral data/Base and exact four-weight scope | Current strict inputs; labels/pairs/token boundaries/hash checks; header/runtime inventory | Access/data/parameter manifests | Invalid data or inventory stops; `INPUT_INELIGIBLE` cannot test scientific acquisition |
| Freeze | Prevent result-driven changes | Bind EN/CN contracts, input/member hashes, source/config, image/profile and user scope | Freeze manifest / certificate | Missing decisive identity is `FREEZE_INCOMPLETE`; no GPU start |
| Smoke/replay | Qualify both actual optimizer paths and both stage resets |3 updates per path/arm; fresh-process step1→2 replay; telemetry, global clipping, frozen weights | Smoke/readout/states, exact replay and gate | Engineering PASS enables only already-authorized Main; low accuracy is not engineering failure |
| Tiny fitting | Measure finite seen-set fit | Independent Base starts,64 targets,160 steps | Tiny checkpoints/readouts | Report valid finite outcome; no success-selected extension; reset before Main |
| Main acquisition | Test the two one-layer routes | Fresh Base/optimizer, same neutral batches, fixed1,200 steps | Required five milestone states and TRAIN/DEV readers | Valid all-cell qualification or non-support; partial/invalid is insufficient |
| Analysis/registration | Make bounded result auditable | Recompute metric/count identities, compare fixed cells, register actual saves and current output access | Tables, manifest, Summary/Detailed | Finish factual record then stop; scientific judgment/any subsequent experiment remain separate |

## 14. Algorithm, Output, And Provenance Contract

Execution root: `/data/250010109/MoE_Router/experiments/20261011_a17_single_attention_acquisition`. Run root is the timestamped member under its `runs/`, recorded in freeze and receipt. Code, configs, raw predictions, TensorBoard, logs and checkpoints stay execution-side. Canonical records stay in this E03 directory; never add raw states to Git.

Reuse the inspected E02 native Base/AnswerLM, collation, paired data order, readers, telemetry, checkpoint fields and freeze/resume guards. Adapt trainable tensor selection to exactly layer27's four weights and generalize SGD from its earlier one-tensor implementation to the single global four-tensor gradient norm/update. Read `docs/training_reuse_index.md` and actual reused source, record reuse/adaptation/rejection, and retain the training observability contract. Reject prior mode-two/TEST paths, presentation changes, SAE/expert/LoRA hooks and fixed upstream caches.

Use root canonical `templates/execution/acp_submit_template.sh`, `h100-4-reserved`, image key `shphd-lite-0911`, one node/four actual H100s and per-job7200-second ceiling. Main and Smoke run two independent workers only: GPU0 `attn1_sgd`, GPU1 `attn1_adam`; GPU2/3 perform no extra fitting, replicas or seeds. Verify allocated four-device node and each worker's isolated one-device view. Capture dry-run, resolved specification/image URL, submitted command, direct job ID and durable pod log. No silent hardware fallback, automatic exposure extension or unapproved extra arm.

Save each actual milestone as `<run>/<phase>/<arm>/<stage>/checkpoints/update_<step>/state.pt` plus manifest; exact directory spelling is bound in the frozen source/config before GPU. State manifests carry member hashes, sizes, reached targets/updates and required Base; raw metrics/readouts and completion/telemetry/replay/frozen checks share the same run identity. Register actual Smoke, tiny, Main checkpoint families and analysis assets with stable IDs, explicit member lists, producer/source/config/data/parent identity and current selected strict output checks. Missing saves remain explicit; platform `SUCCEEDED` alone does not qualify outputs.

## 15. Success / Failure / Insufficient Evidence

**Qualified route:** required outputs/engineering qualify and all four final DEV cells reach80%. State separately which optimizer package qualifies. Success establishes one feasible one-layer acquisition setting in this seed and data; it does not prove a minimum necessary scope.

**Non-support:** a valid arm fails at least one cell at the fixed endpoint. If both fail, the two one-layer packages are insufficient within this budget. Tiny success/low Main DEV supports a fitting/generalization distinction; tiny failure is not architectural impossibility. Never extend a failed arm until it passes.

**Insufficient/ineligible:** incomplete runtime, unavailable required input/state, invalid data/tensor selection, nonfinite update, failed freeze/resume/telemetry or missing primary cell bounds the affected comparison. Register valid partial saves and failure receipts honestly. Complete execution/factual delivery is possible even if neither scientific route qualifies.

## 16. What This Cannot Claim

No pure parameter-number, optimizer-family or Q/K/V-only effect; no proof that all module parameters or the smallest sufficient scope were trained; no universal one-layer limit; no independent statistical confirmation from one diagnostic seed and exposed DEV; no cross-mode transfer, task incompatibility, forgetting of an acquired rule, shared/separate expert benefit, SAE mechanism or natural-text conclusion. Matched targets do not imply equal compute or update size. Subsequent consistent/reversed mapping runs, parameter mechanisms and other branches remain unauthorized until the researcher reviews this test.

## 17. Block Confirmation, Freeze, And Amendment Ledger

User scope on2026-10-11 (Asia/Shanghai): “最后一层 Q/K/V/O 全部开放，然后做两个，一个是sgd的实验，一个是adamw的”; subsequent clarification: “暂时不考虑，先进行完小测试”. Reuse prior authorization for4H100 reserved within this bounded test. This is execution delegation, not mechanism acceptance. Do not request redundant approval or autonomously continue later steps.

| Block | Content | Grounding / state |
|---|---|---|
| A | Old-rule acquisition, no subsequent transfer | `HUMAN_CONFIRMED` requested bounded test; science `Unknown` |
| B | Existing neutral TRAIN/DEV/tiny/panel; no new data/TEST | `VERIFIED_SOURCE` E02 release; inherited diagnostic boundary |
| C | One answer token, paired commands, full-vocabulary success | Existing accepted task and answer-only objective |
| D | Only last-layer four projection weights | `HUMAN_CONFIRMED`; exact names/count from parent configuration, runtime guard required |
| E | Inherited optimizer packages,20 targets/update,160/1200steps | E02 verified settings; AI operationalization under authorized finite test |
| F | Every final DEV cell≥80%, fixed endpoint, secondary readers | Inherited operational qualification; not researcher confidence threshold |
| G | Two independent workers on4H100reserved,7200sec, actual saves | Existing resource authorization and finite current scope |

Cross-block consistency self-review: the task, data/supervision, four-tensor architecture, objective normalization, optimizer comparison, fixed budgets, primary branch mapping, TEST exclusion and artifact ownership agree. This audit is not scientific approval. Freeze actual source/config/data/runtime identities before GPU and verify afterward.

Before execution, update this single Protocol and its CN companion for any decision-bearing correction, then refreeze. After first GPU execution, preserve the registered body. Append material amendments with ID/time, before/after values, reason, visible results, affected blocks/arms, authorization and evidence-eligibility impact. Permitted later factual additions are receipts/status and result links; do not write observations or new scientific decisions into the pre-run body.


### A01: Smoke target-count arithmetic erratum

Recorded at 2026-10-11 23:14:54 Asia/Shanghai (15:14:54 UTC), after Smoke completed and while Main was in progress. The original body above and its pre-run frozen snapshot remain preserved.

- Before: section9 described the three-update Smoke on both stages and both arms as **120** gradient targets.
- After: the actual total is **240** targets: 2 arms × 2 stages × 3 completed updates × 20 targets/update. External step1→2 replay remains **80** separately counted targets.
- Reason: arithmetic reporting typo; the registered source/config, per-stage three-update budget, batch normalization, stage initialization, saves and scientific criteria never changed.
- Visible evidence at discovery: completed Smoke artifacts and in-progress Main, including the saved240-update readers. This correction is not selected from learning performance.
- Affected fields: sections8–9/G's aggregate engineering bookkeeping and downstream completion reports only. Two-arm fitting remains54,400 targets; no training exposure is added or removed.
- Authority/eligibility: factual correction within the already-authorized audit, communicated by the root execution owner. No scientific design amendment, new run approval or evidence exclusion is required. Evidence eligibility remains governed by the original engineering and scientific guards. The execution certificate and Detailed record must report actual240 Smoke targets and retain this erratum.
