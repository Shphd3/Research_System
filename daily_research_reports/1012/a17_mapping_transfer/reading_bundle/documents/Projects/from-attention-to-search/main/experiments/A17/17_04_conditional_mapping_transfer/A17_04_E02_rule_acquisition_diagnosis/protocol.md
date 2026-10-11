派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A17/17_04_conditional_mapping_transfer/A17_04_E02_rule_acquisition_diagnosis/protocol.md`。
[精确原始文件](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A17/17_04_conditional_mapping_transfer/A17_04_E02_rule_acquisition_diagnosis/protocol.md)；研究修改仍回到原件。

---

# Protocol: A17_04_E02 rule acquisition diagnosis

## 0. Approval Snapshot

- Document status: `APPROVED_FOR_BOUNDED_DIAGNOSIS_SMOKE_AND_FULL` under the researcher's explicit execution delegation on 2026-10-11. No fresh approval is required for the finite scope below.
- Approval status: diagnosis, data presentation controls and increased trainable scope are authorized. Exact finite settings are AI delegated operational choices, not a researcher-confirmed scientific mechanism verdict.
- Block audit status: A–G checked for the delegated diagnostic scope; cross-block consistency `PASS`. Scientific interpretation and question closure remain `Unknown`.
- Registered revision: `a17_04_e02_acquisition_diagnosis_v1`; status at contract writing `NOT_RUN`. Before the first GPU execution, snapshot both languages of Anchor/Protocol and hash source, config, data, preflight and required input identities in the execution freeze manifest. The actual freeze timestamp belongs to that manifest.
- Purpose: distinguish failure to fit old training inputs from failure to generalize, and identify whether optimization, trainable computation or presentation offers a practical acquisition repair.
- Primary Anchor: [A17_04_01](../../../../problem_anchors/17_shared_and_interference_learning/17_04_conditional_mapping_transfer/subanchors/17_04_01_rule_acquisition_diagnosis_anchor.md), inherited from the active [Focus](../../../../focus/focus_conditional_mapping_transfer.md).
- Tested premise: projection-only training may improve candidate probability without learning command-controlled selection. Its rival is inadequate optimization/exposure, presentation difficulty or unseen-data generalization.
- Role: `root-cause audit`, restricted to old-mode acquisition. No new-rule transfer, expert or SAE branch.
- Primary reader: minimum full-vocabulary DEV accuracy across both commands and both unseen-data panels, qualification at 80% for every cell.
- Conditions: original projection SGD; projection AdamW; final-four-layer attention AdamW; explicit-command projection AdamW; normalized-separator projection AdamW if its CPU encoding guard passes.
- Matched: Base start, underlying list IDs, labels, one training-order seed, answer-only objective, 20 valid targets/update and final target budget. Not matched: input token counts, wall clock or FLOPs across scopes/presentations.
- Completion: all eligible finite arms and prior-endpoint diagnostics, qualified engineering Smoke/resume, registered actually saved states and readouts, and bilingual bounded results. Scientific acquisition success is not a completion requirement.
- Cannot claim: universal capacity limits, a pure parameter-count effect, a pure tokenizer mechanism, cross-task interference, expert benefits, statistical replication or question closure.

## 1. Terminology / Definitions

An **old-mode record** contains visible mode one, command 甲 or 乙, a list of three distinct words and one answer token. 甲 selects FIRST and 乙 LAST. A **list pair** is the same list asked with both commands. All fitting batches contain complete list pairs. An **answer target** is the single nonignored next token after the answer prefix; prefix/padding tokens do not count toward the training budget.

`neutral` preserves the original command text and spaced list. `explicit` replaces the command text by `取第一项` or `取最后一项`, while retaining list, mode and target. `normalized` preserves the neutral command but replaces spaces between list candidates with the fixed separator `、`. This is a presentation intervention, not a relabeling. Full-prefix token offsets must verify all candidate boundaries for the normalized view.

`order_new` holds out a permutation of a familiar unordered triple; `combination_new` holds out the unordered triple itself. A **fixed training panel** contains training lists but is used without gradients. **Microfit** trains a tiny fixed subset to check fitting feasibility, not rule generalization. Full acquisition restarts from Base and never resumes from microfit.

## 2. Anchor Alignment

The parent cannot interpret acquired-rule retention because its old DEV command/panel accuracies were 33%–54%. This child only tests how to obtain a qualified old-rule starting point. Source evidence is the [E01 Summary](../A17_04_E01_consistent_reversed_mapping/summary.md); its TEST results are historical exposed evidence and cannot select this diagnostic's settings.

| Item | Anchor clause / rival | Why needed and evidence role | Supporting / non-supporting / insufficient reader | Artifact |
|---|---|---|---|---|
| Prior endpoints, training panel versus DEV | Fit versus generalization | Classify the earlier failure at the same saved state | High train/low DEV favors generalization limitation; low both favors unresolved fitting; invalid load is insufficient | `prior_endpoint_diagnostic.json` |
| A versus B | Optimization versus projection impossibility | Same data/scope, different optimizer | B qualifies and A fails: optimizer route viable; both fail: unresolved; invalid run ineligible | Paired endpoint table |
| B versus C | Trainable scope | Same optimizer/data, expanded attention | C qualifies and B fails: scope route viable; both fail: no repair here; no count-only claim | Tensor manifest and endpoint table |
| B versus D | Neutral versus explicit instruction | Same labels/scope/optimizer, changed presentation | D qualifies and B fails: presentation route viable; otherwise preserve outcome | View manifest and endpoint table |
| B versus E | Original versus normalized list encoding | Same labels/scope/optimizer, fixed separator | E qualifies and B fails: format route viable; unmet guard: NOT_RUN | Offset preflight and endpoint table |
| Microfit and full restart | Fitting versus generalization | Small memorization witness before independent full training | Tiny success is not generalization; failure not impossibility | Microfit states/readouts |

## 3. Tested Hypothesis

AI candidate H: at least one of the predeclared optimization, scope or presentation changes supplies a qualified old-rule starting point within the finite budget. The candidate mechanism is that ordinary candidate-word adaptation is easier than condition-controlled selection when the trainable computation or input cue is restrictive. No arm is required to succeed. If the original SGD arm succeeds with more exposure, a stronger mechanism change is not needed to explain practical repair.

## 4. Rival Explanations

1. The earlier two epochs supplied too little exposure or unsuitable SGD dynamics. All arms receive 24,000 full-training targets, with intermediate readings at the original 4,800-target point.
2. The projection can fit seen inputs but cannot generalize to new permutations or triples. Keep train and each DEV panel separate, with per-command readings and paired-command success.
3. Neutral symbols demand learning a mapping that explicit pretrained language already supplies. D tests that presentation route; it does not isolate token length or task novelty.
4. The spaced list encodes a candidate differently from its single-token answer. E tests a normalized representation and separator together, not tokenization alone.
5. More parameters alter update scale or information processing rather than providing raw capacity alone. Preserve exact trainable tensor counts, clipping, actual update norms and computational limits; B/C does not identify pure parameter count.
6. An implementation or label error could mimic failed learning. CPU label/token/offset checks, direct loss checks, frozen-weight guards, no-op identity and external-process exact resume protect eligibility. Engineering qualification cannot establish rule learning.

## 5. Data Construction And Provenance

Required input asset IDs are `model_qwen3_0p6b_base_official_a5`, `tokenizer_qwen3_0p6b_base_official_a5`, source `data_a17_conditional_mapping_v1`, and derived `data_a17_mapping_acquisition_diagnostic_v1`. Consult the asset registry and run current strict checks before payload use. The exact Base directory is `/data/250010109/model_cache/Qwen3-0.6B-Base-official`.

Take only original mode-one `old` TRAIN and DEV rows. TRAIN has 1,200 lists × two commands = 2,400 records. DEV has two panels, each 200 lists × two commands = 400 records, for 800 combined records. Preserve original list/split/panel membership, original targets and vocabulary. Derived views retain `record_id` or an explicit original-record link, `list_id`, command alias, mode, words, target ID, source split, panel, presentation, prefix and input IDs. Record IDs have a view prefix; original command aliases remain甲/乙, world remainsold and mode remains1. The derived release contains twelve files at `data/acquisition_v1/{train,dev,train_panel,tiny}_{neutral,explicit,normalized}.jsonl`. Formal generation, fitting and diagnostic analysis do not copy, load or evaluate the original TEST.

Select the fixed training panel before GPU execution: take the first ten original TRAIN unordered `orbit_id` groups in lexical order; within each group take the complete20-list word-rotation cycle whose ordered tuple has the smallest representative. This gives200 lists and complete command pairs =400 targets, with exact vocabulary/position balance. Microfit takes the first cycle's20 lists and the next cycle's first12 lexical lists =32 lists/64 targets; it need not be vocabulary-balanced. Freeze all IDs and the selection rule in the manifest; use identical IDs across views/arms and prior endpoint evaluation. No IDs are selected by model loss or accuracy. Build complete20-target batches by cycling/shuffling these list pairs as declared; a tiny epoch boundary does not discard targets or create incomplete accumulation windows.

CPU checks verify labels FIRST/LAST, unique list/command pairs, two commands per list, source/derived label agreement, source split ownership, permitted order-panel overlap and disjoint combination groups. Explicit and normalized views must preserve lists, labels and per-batch target histograms. A target is a single vocabulary token; prefix-plus-target tokenization must equal prefix IDs followed by that target. Input candidates need not be single tokens in the original or explicit view, and this fact is logged.

For E, `、` must make every candidate occurrence in the full prefix correspond to exactly its intended target-token ID at the correct character span, without merged or extra candidate tokens. Before contract freeze, CPU inspection reported zero failures over 9,600 candidate occurrences in 3,200 old TRAIN/DEV records and 120 candidate occurrences in 40 cyclic vocabulary probes. Freeze the actual preflight JSON and rerun guards on generated files. This is tokenizer evidence, not a learning result. If regeneration violates the criterion, E is NOT_RUN; do not search for a replacement separator after GPU results.

## 6. Learning Task And Permitted Supervision

Predict exactly the next answer token after the full prefix. Only that target contributes CE. The correct word is present in the input list; there is no additional explanation, hidden teacher, mode-two sample, answer replay, distillation label or external semantic supervision. Explicit instruction wording is an allowed input intervention, not an extra training answer. Full-vocabulary argmax determines accuracy; candidate-restricted argmax must not replace it.

## 7. Model / Architecture And Frozen Variants

Use the registered 28-layer Qwen3-0.6B Base and native forward path. All arms start from the identical pretrained parameters. The existing three old adapters are loaded only for prior-state evaluation, never as a new arm's initial state.

| Arm | Presentation | Trainable scope | Parameter count | Optimizer |
|---|---|---|---:|---|
| `o_sgd` (A) | neutral | `model.layers.27.self_attn.o_proj.weight` | 2,097,152 | SGD |
| `o_adam` (B) | neutral | Same final `o_proj` | 2,097,152 | AdamW |
| `attn4_adam` (C) | neutral | Layers 24–27, attention q/k/v/o projection weights | 25,165,824 | AdamW |
| `explicit_o_adam` (D) | explicit | Same final `o_proj` | 2,097,152 | AdamW |
| `neutral_normalized_o_adam` (E) | normalized | Same final `o_proj` | 2,097,152 | AdamW |

C trains exactly 16 weight tensors, named `model.layers.{24,25,26,27}.self_attn.{q_proj,k_proj,v_proj,o_proj}.weight`. Immutable parent safetensors-header inspection counted 25,165,824 parameters, twelve times the original matrix. Save `provenance/parameter_header_audit.json`; before training, independently enumerate runtime named parameters and verify names, shapes and total. Do not train attention biases, q/k norms, MLP, embeddings, final norm or output head. Projection-only shape is 1,024×2,048. All untargeted parameters stay frozen and unchanged.

Use FP32 model/gradients, native SDPA, evaluation mode without dropout, no TF32 and deterministic algorithms. Q/k/v training legitimately changes attention retrieval; C therefore changes computation location as well as parameter count. No LoRA, SAE, router or expert is introduced.

## 8. Training Objective And Optimization

Each update minimizes the mean of 20 valid answer losses: \(L=20^{-1}\sum_{i=1}^{20}-\log p(y_i\mid x_i)\). Accumulate four microbatches of five examples. Each microbatch contributes its loss sum divided by20. No prefix/padding token enters this denominator. There is no auxiliary loss, regularizer or enabled component; component registry is empty/NOT_APPLICABLE.

A uses manual plain SGD, learning rate0.01, no momentum or decay. B/C/D/E use AdamW with learning rate0.0001, betas(0.9,0.999), epsilon1e-8 and weight decay0. In every arm clip the aggregate trainable gradient's global L2 norm at1 before the optimizer step. Keep the learning rate constant; no warmup, scheduler decay, adaptive stopping or early stopping. Report raw/clipped gradient norm and actual parameter displacement norm; the same learning rate or clipping bound does not imply matched actual updates.

Microfit performs160 completed updates =3,200 valid targets per arm on the frozen64-target set, from Base with a fresh optimizer. Full restarts Base and fresh optimizer/RNG, then performs1,200 updates =24,000 targets per arm. This is ten complete exposures of2,400 full TRAIN records. All five eligible arms total120,000 full-training targets plus16,000 microfit targets. Smoke, resume replay and evaluation targets are additional and reported separately. Missing E reduces actual totals explicitly.

## 9. Conditions, Seeds, And Checkpoints

Use training-order seed29 for all arms. This is one diagnostic realization, not three-seed confirmation. Freeze paired list order; A/B/C share identical input/target batches, D/E share the underlying list/label order. Use complete command pairs in every effective batch. GPU workers are independent arms, not data-parallel replicas: worker0 runs A then E; workers1/2/3 run B/C/D concurrently. Serial placement of E does not change initialization or budget.

Full save/evaluation milestones are0,1,240,600,1200 updates, corresponding to0,20,4,800,12,000,24,000 targets. Microfit saves0,1,160 and evaluates its own64 targets plus the fixed training/DEV panels at least at0 and160. Do not treat microfit's overlapping training-panel subset as independent generalization evidence. Smoke runs3 updates per eligible arm and saves the state needed for the external-process next-step replay.

Save resumable state for every trainable tensor, optimizer moments/step (or manual-SGD descriptor), constant schedule, Python/NumPy/CPU/CUDA RNG, completed update, valid-target count, stage, arm, parent asset/hash, config/source/data hashes, ordered data cursor and the next-batch identity. States require the exact frozen Base and are not standalone exported language models. Save actual tensor/optimizer/state manifests and missing saves explicitly.

Prior-endpoint evaluation loads each registered family `adapter_a17_04_mapping_full_20261011t095038z_seed_{29,43,71}_old` at its actually saved240-update member, with the required Base. These three diagnostic readouts describe existing states; they are not additional new training seeds.

## 10. Primary Metric And Frozen Analysis Plan

For arm \(j\), command \(c\) and panel \(p\), accuracy is the fraction of that cell's targets whose full-vocabulary argmax equals the true target. The primary reader is \(Q_j=\min_{c,p}\operatorname{Acc}_{j,c,p}\) at update1200. Each command/panel cell contains200 targets; panels and commands are reported separately before an equal-weight combined mean. Qualification requires every cell at least0.80. The threshold is an inherited AI operational acquisition convention, not a scientific confidence level.

The observation unit is a list/command record; paired-command metrics use a list. The new training realization is one seed; lists do not create independent training replications. Report exact cell counts, means and paired cross-arm differences, without p-values, population intervals or three-seed language. Do not discard difficult lists, outliers, failed arms or low-scoring commands. A missing required cell leaves acquisition unqualified; an engineering-ineligible arm is not a negative scientific result.

Primary comparison is the fixed endpoint. Also report all frozen milestones and the earliest saved milestone meeting all four DEV cells; this descriptive learning-time reader does not select different final budgets. Compare A/B for optimizer, B/C for trainable scope, B/D for explicit presentation and B/E for normalized presentation. These are descriptive diagnostic comparisons; no multiplicity-adjusted confirmatory claim is planned.

Read original-state training and DEV diagnostics only after current input access qualifies. All new settings are frozen before GPU results. DEV is openly used for diagnosis, not claimed untouched confirmation. A preceding CPU source-structure QA inspected the parent TEST's schema/tokenization. An initial audit also deserialized old evaluation JSON containing both DEV and TEST prediction records, while every model-readout computation filtered `split == 'dev'`. No TEST model result was used to select settings or reported as new diagnostic evidence. Preserve this exposure fact; do not claim that TEST prediction records were never read. The present formal generator/trainer/analysis must not load original TEST rows. No setting is promoted to a new transfer run automatically. Analysis saves an endpoint table, cellwise trajectories, paired-switch table, loss-decomposition table and run eligibility manifest under `<run>/analysis/`. Scientific claims are bounded to these finite settings and this seed.

## 11. Secondary Metrics And Guards

Record answer CE, full-vocabulary accuracy, correct-versus-opposite endpoint log-probability margin, correct-versus-strongest-full-competitor margin and competitor token ID. For list candidate set \(S\), save probability mass \(P_S=\sum_{w\in S}p(w\mid x)\), access loss \(-\log P_S\) and conditional selection loss \(-\log[p(y\mid x)/P_S]\). Their sum equals answer CE exactly; this output accounting does not identify internal modules.

For each paired list, record whether both command answers are correct. Define \(s_c=\log p(L_3\mid x_c)-\log p(L_1\mid x_c)\) and command response \(a=(s_{乙}-s_{甲})/2\). Positive response is consistent with the old mapping, but a positive mean alone is not qualification or causal mechanism evidence. Preserve individual command probabilities, middle-word competition and failures, since average endpoint margins can hide full-vocabulary errors.

Per update record answer-weighted CE, raw/clipped gradient norm, actual step norm, relative weight displacement, valid targets and actual prefix tokens, batch IDs, throughput and cumulative stage coordinates. Preserve all seven required TensorBoard tags: `tokens/train_lm_loss`, `updates/train_lm_loss`, `tokens/train_total_loss`, `updates/learning_rate`, `progress/tokens_seen`, `progress/optimizer_step`, `progress/effective_tokens_per_update`. Token loss uses completed valid-answer count as global step; update loss uses optimizer step. No four-worker aggregation is applied to independent arms. Resume restores both coordinates without overlapping conflicting event steps.

Numerical/engineering guards: finite losses/gradients/weights; no skipped update; independent target counts; no-op evaluation identity; frozen parameter version/byte-hash identity; CE decomposition error below2e-5 nat; exact external-process next-step weights, optimizer, RNG, counters and batch identity. A failure stops the affected arm and retains evidence. Source/config/data/frozen-contract hashes must match before and after execution.

## 12. Known Good / Known Bad / Known Confusing Cases

- Known good label: list `红 蓝 绿`, old command甲 has target红 and乙 target绿; explicit wording changes neither. Complete paired labels must swap endpoints as required.
- Known bad construction: identical full input within one view with contradictory targets, missing a command, wrong answer position, leaking an original TEST row, or an E candidate encoded contrary to the preflight promise. Reject before fitting.
- Known confusing result: correct CE falls while both-command success stays low or conditional selection worsens. This is not rule acquisition. Tiny-set fitting can be memorization; E success can be separator/presentation assistance; C success can be changed retrieval or optimization rather than parameter count alone.

## 13. Scientific Procedure And Stage Contracts

| Stage | Goal / input | How and why | Expected output / artifact | Pass, failure and handoff |
|---|---|---|---|---|
| CPU preflight | Qualify registered Base, source old TRAIN/DEV and derived views | Strict assets; verify source/derived labels, splits, pair IDs, tokenizer boundaries; runtime tensor inventory | Data/view/parameter manifests and access checks | Invalid data `DATA_INELIGIBLE`; optional E encoding failure `NOT_RUN`; valid eligible views pass to freeze |
| Freeze | Prevent outcome-driven design changes | Snapshot bilingual contracts, source/config/data/input identities and authorization | `freeze.json`, execution certificate | Missing decisive hash `FREEZE_INCOMPLETE`; no GPU scale-up |
| Prior-state readout | Diagnose existing fit versus unseen performance | Load three old240 states and evaluate fixed train/DEV, without gradient | `prior_endpoint_diagnostic.json` | Valid readout contributes diagnosis; unavailable state recorded missing, not fabricated |
| Smoke / resume | Qualify actual five-arm trainer | Three updates per eligible arm; verify telemetry/freeze; fresh process restores saved step and reproduces next update exactly | Smoke states, tags, replay comparison, gate | Engineering PASS permits already-authorized Full; scientific low accuracy is not a Smoke failure |
| Microfit | Check tiny-set fitting route | Independent Base starts,64 fixed targets,160 updates/arm | Saved states and readouts | Finite bounded result regardless of scientific success; full restarts rather than inherits |
| Full | Compare acquisition routes | Independent Base starts, same full list/label order,1200 updates/arm | Required states and fixed train/DEV readouts | Finite completion; failed/incomplete arm preserved without automatic extension |
| Analysis / registration | Produce auditable bounded answer | Recompute metrics, check counters/hashes, register actual states and readouts, strict output access | Analysis tables, registration receipts, Summary/Detailed | Complete factual handoff; scientific verdict and next-run choice remain researcher-owned |

## 14. Algorithm, Output, And Provenance Contract

Execution root: `/data/250010109/MoE_Router/experiments/20261011_a17_mapping_acquisition_diagnostic`; implementation `source/diagnose.py`. Source/config/derived data, preflight, contracts, environments, receipts, logs, TensorBoard, checkpoints and analysis remain execution-side. Canonical scientific records remain in this experiment directory; no raw weights or bulk predictions enter Git.

Use the repository execution envelope, root `templates/execution/acp_submit_template.sh`, resource profile `h100-4-reserved` and image key `shphd-lite-0911`. One node/four H100s, maximum7200seconds per job. Capture dry-run resolution, actual profile/spec/image URL, direct job ID and submitted command. Full is permitted only after this implementation's bounded Smoke qualifies. A runtime ceiling yields explicit partial completion, not silent extension or a new arm.

Reuse/adapt the inspected A17_04 E01 AnswerLM/collate, native model loading, data pairing, evaluation, SGD, provenance, freeze and telemetry; expand tensor selection and resumable optimizer state for AdamW. Preserve source lineage and differences. Reject inherited sensitive-direction projections, SAE hooks, mode-two tasks, TEST loading and old scientific branch logic. Read the actual source and training reuse/observability requirements before execution; do not weaken the parent guards when adding multi-tensor updates.

Per-stage outputs include raw update metrics, exact batch IDs, readouts with source list/command/panel/view IDs, checkpoint states/member hashes, frozen-weight checks, environment and source/config/input manifests. Register only actual Smoke, microfit and full saves, with stable family IDs, exact member lists, Base requirement, reached answers/updates and resume boundary. Run current selected strict output checks and link receipts from artifact manifest/Detailed. A job-success flag alone cannot qualify saved artifacts.

## 15. Success / Failure / Insufficient Evidence

**Qualified acquisition:** all four endpoint DEV command/panel accuracies meet80%, engineering checks qualify, and required outputs are present. This establishes a feasible old-acquisition route in one seed. Preserve training/DEV and pair-success readings; qualification is not cross-task mechanism support.

**Non-support for a repair:** the relevant valid arm fails qualification at the frozen budget. Compare against its matched arm rather than claiming universal incapacity. If only training fits, classify a generalization limitation. If all valid arms fail, report `NO_QUALIFIED_ACQUISITION_ROUTE_IN_BOUNDED_DIAGNOSTIC`, not model impossibility.

**Insufficient/ineligible:** missing required cells/checkpoints, invalid label/data/freeze, nonfinite update, failed resume or runtime partial execution bounds the affected comparison. E with failed encoding guard is NOT_RUN. No secondary metric rescues missing primary acquisition. None of these branches authorizes arbitrary additional training or a transfer claim.

## 16. What This Cannot Claim

No task incompatibility, forgetting of an acquired rule, expert benefit, SAE mechanism, natural-text conclusion, universal0.6B capacity limit, pure parameter-count effect or isolated tokenization cause. B/C changes computational scope; B/D/E changes presentation; A/B changes optimizer and its numerical dynamics. Matched answer counts are not matched FLOPs or wall clock. One seed and exposed DEV provide bounded diagnosis rather than independent confirmation. Any future confirmatory transfer experiment needs new heldout data and its own explicit contract/scope.

## 17. Block Confirmation, Freeze, And Amendment Ledger

The researcher's latest request explicitly authorizes this diagnostic, assessment of data versus parameters and feasible increased-parameter training without intermediate approval. The parent account remains the scientific owner; AI exact settings below are delegated operationalization, not manufactured human scientific confirmation.

| Block | Frozen content | Basis / status |
|---|---|---|
| A | Old-acquisition diagnosis only, bounded claim | Researcher request plus inherited parent insufficiency; authorized delegated scope |
| B | Original old TRAIN/DEV and three presentation views; no original TEST | Verified source and AI diagnostic control; authorized delegated implementation |
| C | Single answer token; paired commands; no extra targets | Inherited task and explicit answer-loss agreement |
| D | Projection or final-four-layer attention; exact runtime inventory | Authorized parameter-budget diagnosis; header-derived counts; runtime guard required |
| E | Fixed SGD/AdamW, batch20, micro160/full1200; no adaptive continuation | AI operational choices under user delegation |
| F | Minimum DEV cell accuracy80%, fixed endpoint, specified diagnostic comparisons | Inherited operational qualification; no new scientific confidence claim |
| G | Four H100 reserved, image/profile, two-hour ceiling, actual saves/registration | Persisting resource authorization and current finite execution scope |

Cross-block audit: question, supervision, data views, optimizer normalization, fixed budgets, test exclusion, tensor scope, artifact ownership and branch meanings are consistent. This check does not grant scientific approval. The pre-GPU freeze manifest records actual timestamps/hashes; current scientific mechanism judgment and closure remain Unknown.

Before first GPU execution, changes to any decision-bearing item update this single Protocol and both language companions, then refresh the freeze. After execution starts, preserve its registered body. Any material change requires an append-only amendment stating before/after, reason, results already visible, affected blocks/arms, authorization and evidence eligibility. Do not erase unfavorable results, silently alter a budget or relabel an optional arm failure as successful preflight. Result links may be appended without rewriting the original scientific body.
