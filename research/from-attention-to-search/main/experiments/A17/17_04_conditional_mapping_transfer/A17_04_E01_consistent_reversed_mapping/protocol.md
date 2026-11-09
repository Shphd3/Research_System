# Protocol: A17_04_E01 consistent versus reversed conditional mapping

## 0. Approval Snapshot

Document status: `APPROVED_FOR_IMPLEMENTATION_SMOKE_AND_FULL`.
Approval basis: on 2026-10-11 the researcher adopted the merged task and requested Anchor/Protocol, another dataset and completed experiments, explicitly saying intermediate approval is unnecessary. Earlier four-H100 reserved resource authorization remains in scope. This is `USER_DELEGATED_BOUNDED_IMPLEMENTATION`; AI-selected operational details are recorded as delegated choices, not separate researcher scientific judgments.
Block audit: A–G `USER_DELEGATED_IMPLEMENTATION_RECORDED`; consistency self-review `PASS`, subject to implementation/data checks below. Scientific verdict and question closure: `Unknown`.
Revision: `A17_04_E01_r1`; snapshot English/Chinese Anchor, Protocol, config and source before first GPU execution. Freeze timestamp and hashes go in the execution manifest.

Purpose: determine whether changing a new mode's command-position mapping changes old-mode retention, beyond candidate-word adaptation.
[Active Focus](../../../../focus/focus_conditional_mapping_transfer.md) owns the activated question; the [Anchor](../../../../problem_anchors/17_shared_and_interference_learning/17_04_conditional_mapping_transfer/17_04_conditional_mapping_transfer_anchor.md) owns the scientific design.
Experiment role: root-cause audit of task-relation dependence.
Primary quantity: paired reversed-minus-consistent change in old answer advantage at 4,800 new answer targets.
Treatment: reversed mode-two mapping. Control: consistent mapping. Inputs, old endpoint, answer marginals, minibatch order and optimization budget are fixed.
Support: qualified old/new learning and stable negative primary effect. Non-support: no stable negative effect; preserve opposite effects. Insufficient: acquisition/engineering failure or inconclusive seed pattern.
Cannot claim: inevitable incompatibility, identified internal modules, expert utility or natural-text generalization.
Execution ceiling: the envelope's `h100-4-reserved` and `shphd-lite-0911`; one Smoke, then one separate qualified Full, each runtime ceiling 7,200 seconds. No resource fallback, unrelated training, commit, push or publication.

## 1. Terminology / Definitions

The old task is mode one with 甲→FIRST and 乙→LAST. The new task is mode two. `consistent` preserves these mappings; `reversed` swaps them. These are separate label-consistent experimental worlds. `joint_reversed` continues with both modes under the reversed-world rules and supplies additional old supervision.

An example is one prefix plus one correct answer token. A paired list has two examples, one for each command. `order_new` is a new ordering of a three-word set used in training. `combination_new` is an unordered three-word set absent from all training lists. Both panels use familiar vocabulary, not unseen word tokens. DEV selects only the prespecified comparable-learning point; frozen TEST supplies primary readouts after training. An operational threshold is a descriptive reporting convention, not statistical significance or scientific approval.

## 2. Anchor Alignment

The experiment changes the relation between two conditional mappings, whereas A17_03 changed components of updates for fixed tasks. Merging means one causal mapping intervention with output readers and guards; it does not mean repeating both descriptions as two experiments. Both commands are already supervised in the old task. No claim about supplying previously absent position knowledge is eligible.

| Item | Anchor clause / uncertainty | Why needed | Evidence role and branch | Artifact |
|---|---|---|---|---|
| Consistent/reversed continuation | H and primary paired effect | Change mapping while holding inputs/exposure fixed | Primary; support/non-support/insufficient under §15 | Branch checkpoints, TEST readouts, paired table |
| Candidate and mode-command readers | General candidate adaptation versus conditional response | Separate probability access from relative answer choice | Diagnostic, cannot rescue primary non-support | Per-record logits/probabilities and contrasts |
| Equal-norm one-step probes | Update-scale rival | Compare immediate effects at the same old state | Local causal effect only; invalid norm/freeze is ineligible | Source gradients/norms and finite readouts |
| Comparable new skill | Difficulty/learning-path rival | Compare registered first DEV acquisition points | Secondary; missing point is insufficient; initial/path differences remain | DEV selection receipt and corresponding TEST readouts |
| Joint reversed continuation | Joint feasibility | Check a concrete supervised realization | Success is a witness; failure leaves capacity Unknown | Joint milestones and mode-specific readouts |

## 3. Tested Hypothesis

H predicts that reversed new mapping gives less old correct-versus-opposite answer advantage than consistent mapping at matched presentation count. For each seed, both branches start from the identical old endpoint. Lower retention than the consistent branch is distinct from net deterioration relative to that endpoint. We separately report whether old CE rises, margin falls or accuracy declines in each branch.

## 4. Rival Explanations

1. Candidate words receive more probability without improved rule selection. Track list-three access/selection CE, pool-20 mass and pair/full-competitor margins.
2. Reversal is harder, starts at different new accuracy, or learns along a different path. Report baseline ability, learning curves and first registered comparable DEV levels; this does not fully control post-treatment difficulty.
3. Larger actual updates produce a larger retention cost. Report every actual norm; add same-state equal-norm immediate probes. The cumulative primary training retains ordinary SGD and does not norm-match every trajectory step.
4. The frozen tensor or optimizer cannot realize both mappings. A successful joint branch is a feasibility witness. Joint failure can also arise from data, optimization, freeze or limited supervision; it does not establish capacity impossibility.
5. Lexical or ordering shortcuts generate the contrast. Mode-visible prompts, neutral commands, exact answer marginals, paired batch histograms and heldout order/combination panels constrain shortcuts. One template remains a scope limitation.

## 5. Data Construction And Provenance

Build `conditional_mapping_v1` from the 20 answer words already single-token under registered `tokenizer_qwen3_0p6b_base_official_a5`. Retain and independently validate each word/token ID; abort multi-token answers or distinct words sharing IDs. Dataset generation seed is 20261011.

Enumerate all 1,140 unordered triples of 20 distinct words. Partition by cyclic index rotation into 57 orbits of 20 triples each, then shuffle these orbits with the fixed seed. Allocate 30 training orbits, 10 DEV-combination orbits, 10 TEST-combination orbits; seven remain unused. For each training triple use two fixed permutations, producing 1,200 training lists. DEV-order uses a third permutation from 10 training orbits; TEST-order uses a fourth permutation from 10 other training orbits. Each evaluation panel has 200 lists. The generator manifest records the exact orbit/permutation ordering and selected IDs; it is part of the frozen data identity.

Each list is paired with both commands in both modes. There are 2,400 training records per mode/world; each evaluation panel contains 400 records per mode/world. Combined evaluation contains 800 records per mode/world with equal panel weight. Across each complete rotation orbit, word counts per position are balanced. Paired commands make FIRST/LAST answer counts identical between consistent and reversed worlds, including every effective batch of 10 paired lists (20 targets).

Template: `模式：一。口令：甲。列表：红 蓝 绿。答案：`, changing mode/command/list as appropriate. No explicit answer label is supplied after `答案：`; all candidate words, including the correct token, do occur in the list. Lists have three distinct tokens. Primary new training reuses underlying old training content intentionally but changes the mode field; it never includes old full inputs or old labels. Both new worlds have byte-identical prefixes and source batch order and different target mappings. Do not mix opposite labels for identical full inputs inside one world.

Required fields: `record_id`, `list_id`, `orbit_id`, `unordered_group_id`, `panel`, `split`, `mode`, `command`, `mapping_world`, `words`, `first_id`, `middle_id`, `last_id`, `target_id`, `prefix`, `input_ids`, `template_id`. Data guards verify counts, balanced positions/targets, label consistency, complete paired commands, identical new-world prefixes/batch histograms, no full-list overlap across training/DEV/TEST, no unordered-group leakage for combination panels, and permitted order-panel group reuse only. Freeze every data file/hash and register the actual dataset before loading training payloads.

## 6. Learning Task And Permitted Supervision

Predict one next answer token after `答案：`. Train only that token's CE. Every input may contain mode, command and list, including the correct word as a list candidate, but no explicit answer label, split marker, diagnostic target, feature annotation or hidden oracle flag. Answers come deterministically from the registered mode-command mapping. No SAE, expert router, position classifier or extra supervision is trained. List/mode metadata may be used for evaluation grouping but must not silently enter the model prefix.

## 7. Model / Architecture And Frozen Variants

Use asset `model_qwen3_0p6b_base_official_a5`, parent directory `/data/250010109/model_cache/Qwen3-0.6B-Base-official`, and its registered tokenizer. Match parent config/weights hashes through the carrier source and current strict input-access manifest. Qwen3 has 28 layers; train only `model.layers.27.self_attn.o_proj.weight`, shape 1,024×2,048. Freeze every other parameter and verify both parameter versions and byte hashes. FP32 forward/gradients, native SDPA, evaluation mode/no dropout, no TF32, deterministic algorithms. Prefix hidden states feed the unchanged vocabulary output head at the last valid prefix position. This matrix-only carrier is the earlier controlled update scope, not full-model learning.

## 8. Training Objective And Optimization

For a batch of 20 examples, minimize mean answer-token CE: \(L=20^{-1}\sum_i-\log p_\theta(y_i\mid x_i)\). Use manual plain SGD, learning rate 0.01, global trainable-gradient norm clipping at 1, no momentum, decay, regularizer or scheduler change. Four microbatches of five examples accumulate one gradient. One completed update counts 20 valid prediction targets. Four GPU workers handle independent cases; they are not four data-parallel replicas of one update. No skipped updates are permitted; nonfinite losses/gradients stop the affected run.

Each old and primary new stage has 240 updates = 4,800 answer targets = two deterministic epochs over 2,400 records. Joint has 240 updates and 4,800 total targets, half old and half reversed-new. Use batch-paired commands, fixed seed-derived list ordering, the same order in consistent/reversed branches, and record all batch IDs. At joint update index i, take five list keys from primary new_order[i*5:i*5+5] and include each list's two old-mode and two reversed-new-mode records, giving ten old plus ten new targets. Joint traverses the 1,200-list pool once and receives 2,400 old and 2,400 new targets; its extra old supervision is explicit and its new exposure differs from the primary branches.

No DEV/TEST early stopping or tuning. Required TensorBoard tags under each stage's `tensorboard/`: `tokens/train_lm_loss`, `updates/train_lm_loss`, `tokens/train_total_loss`, `updates/learning_rate`, `progress/tokens_seen`, `progress/optimizer_step`, `progress/effective_tokens_per_update`. LM/total loss are the same mean CE; component registry is empty/NOT_APPLICABLE. Tokens and steps are stage-local with explicit cumulative branch totals. All milestones align valid targets; independent counters verify completed windows. Resume restores both coordinates, data cursor/order and RNG, preserving nonconflicting event series.

## 9. Conditions, Seeds, And Checkpoints

Seeds: 29, 43, 71. For each seed: one old stage followed independently by consistent, reversed and joint_reversed continuations from the identical saved old endpoint. Evaluate/save updates 0, 1, 16, 50, 120, 240 in every stage; corresponding stage targets are 0, 20, 320, 1,000, 2,400, 4,800. Preserve all checkpoints even if acquisition is poor. Checkpoints contain trainable weights, parent ID, manual optimizer/scheduler description, Python/NumPy/CPU/CUDA RNG, step, actual target count, data cursor and order identity, stage/seed/config identity and next-batch contract. These are matrix adapters requiring their frozen parent, not standalone full-model exports.

From each old endpoint, compute consistent and reversed source gradients on their identical first 20 inputs, restore the same state, and independently apply \(d=-0.01g/\|g\|\). Record actual norm and finite old/new readouts; no sequential probe stacking. This equal-norm probe is separate from ordinary training. A zero/nonfinite gradient is a named insufficient/ineligible probe; it is never replaced with arbitrary noise.

Smoke uses three updates per stage and all three continuations, preserves baseline/step1/final checkpoints, and qualifies independent-process exact step1→step2 resume for a source branch on every worker that runs a case. Smoke panels use the first 10 list IDs of each DEV panel, not TEST. It qualifies engineering properties only. Full reruns fresh from the frozen parent, not from Smoke training.

## 10. Primary Metric And Frozen Analysis Plan

For each old-mode record, let \(y\) be its correct endpoint and \(o\) its opposite endpoint. Compute \(m=\log p(y\mid x)-\log p(o\mid x)\). At new update 240 compute \(E_s=\Delta M_{A,s}^{reversed}-\Delta M_{A,s}^{consistent}\), where \(M\) is the record mean and both changes use the same old endpoint. Units are nat/answer. Report order_new and combination_new separately, then their equal-weight combination. Commands have equal weight, as do seeds. Seed is the replication unit; examples, commands and panels are not independent model runs.

Freeze the combined-panel equal-budget effect as primary. Show all three \(E_s\), arithmetic mean, minimum/maximum and sample standard deviation; no p-values, population confidence claim, post-hoc seed exclusion or outlier deletion. An AI operational stable negative effect requires all three seed effects <0 and mean ≤−0.01 nat. Positive stability uses all >0 and mean ≥0.01. Smaller/mixed effects are reported as weak/heterogeneous, not proof of equality. Do not choose the panel, endpoint or threshold by TEST results. Full mechanically computes and saves frozen TEST at every preregistered milestone; these values do not choose stops, budgets, labels, hyperparameters or checkpoints. Analysis and researcher interpretation open them only after all bounded training finishes and freeze verification passes. Smoke never loads TEST. This is fixed-rule heldout evaluation, not a claim of cryptographically sealed or fully blinded execution.

For the secondary comparable-level reader, use the earliest saved new milestone whose DEV full-vocabulary accuracy is ≥0.80 on both unseen panels. If baseline already qualifies, select step0 and explicitly retain the initial-ability/path confound. If an arm never qualifies, mark the comparison unavailable; do not extend training until it passes. Read the corresponding TEST old/new quantities. This does not make new learning paths or difficulty identical.

Missing cells remain `MISSING/INELIGIBLE` and block their dependent paired estimand; retain qualified unrelated readouts. No synthetic imputation. The primary result is descriptive evidence in this fixed setting, not a researcher scientific verdict. False support matters because it could motivate unnecessary module separation; absence of support must not erase smaller measured effects.

## 11. Secondary Metrics And Guards

Report CE \(-\log p(y)\), full-vocabulary accuracy, correct-versus-opposite margin, correct-versus-strongest-full-competitor margin, competitor token ID and all three list logits/probabilities. For list set \(S=\{L_1,L_2,L_3\}\), CE splits exactly into access \(-\log\sum_{w\in S}p(w)\) plus selection \(-\log[p(y)/\sum_{w\in S}p(w)]\). Also report probability mass on all 20 candidates and conditional-20 CE. A loss split is output bookkeeping, not evidence for two internal functions.

For each paired list/mode use \(s_{m,c}=\log p(L_3)-\log p(L_1)\), \(a_m=(s_{m,乙}-s_{m,甲})/2\), \(q_m=(s_{m,乙}+s_{m,甲})/2\), \(C=(a_1+a_2)/2\), \(K=(a_2-a_1)/2\). Old desired \(a_1>0\); consistent new desired \(a_2>0\); reversed new desired \(a_2<0\). Increased mode difference can coexist with worsening old response. These are exact output contrasts, not a parameter decomposition.

Engineering thresholds: repeated no-op baseline identical; frozen byte hashes and parameter versions unchanged; independent-process resumed weights/RNG/metrics/counters/data IDs byte-exact; finite CE split absolute error <2e-5 nat; actual update norm/rounding relative error <1e-2; all required scalar tags finite with independently correct target coordinates. Actual norms and full source hashes are retained. Reporting conventions: material CE magnitude 0.005 nat, accuracy magnitude 1 percentage point and margin magnitude 0.01 nat. These guard/report thresholds are delegated operational choices, not scientific confidence levels.

## 12. Known Good / Known Bad / Known Confusing Cases

Good: mode-one 甲/乙 on `红 蓝 绿` has red/green targets; reversed mode-two uses green/red and keeps identical new-world prefixes. A no-op restores identical readouts. Cyclic rotations and paired commands preserve answer marginals.
Bad: mode field omitted while mixing conflicting worlds; TEST triple used in training; label inside prefix; one command missing; branch batches reordered independently; frozen tensor changes; resume uses a different data cursor.
Confusing but valid: correct CE improves while another word increases more and argmax is lost; reverse is worse than consistent while both improve old performance; baseline mode-two already achieves the comparable-level threshold; joint learns neither mode. Preserve these outcomes rather than reclassifying them as mechanism support.

## 13. Scientific Procedure And Stage Contracts

| Stage | Goal / input | Operation and rationale | Output / handoff | Failure branch |
|---|---|---|---|---|
| Preflight | Bind parent/tokenizer and new data | Inspect reused source; generate and register dataset; strict access, hashes, schema and oracle tests | Frozen config/data/contract identities → Smoke | Asset, label, split or schema error blocks GPU execution |
| Smoke | Qualify native update and observability | Four reserved H100 workers, three-update stages and independent-process exact resume | Complete finite readouts, telemetry/freeze/resume PASS → Full | Engineering failure retained; Full blocked until qualified repair |
| Full old learning | Supply common learned state | Fresh parent per seed, 240 old updates; DEV old acquisition check | All old milestones and endpoint → each continuation | Poor acquisition is CONDITIONAL_START_NOT_QUALIFIED; still finish bounded branches, interpretation insufficient |
| Full branches | Test mapping relation | Matched consistent/reversed SGD; separately joint old/new; equal-norm old-endpoint probes | All stage milestones and frozen readouts → analysis | Nonfinite, freeze, source or save failure stops and preserves partial evidence |
| Analysis | Determine bounded understanding update | Verify source/freeze, interpret saved TEST only after bounded training, paired effects plus registered readers and DEV selection | Independent recomputation, Summary/Detailed → researcher | Unqualified/missing effects cannot become primary evidence |
| Handoff | Preserve reusable facts | Register actual adapters and analysis assets; strict saved-output checks; bilingual records | Factual completion receipt and bounded conclusion | Missing checkpoint or result explicitly retained; no manufactured completion |

## 14. Algorithm, Output, And Provenance Contract

Execution root: `/data/250010109/MoE_Router/experiments/20261011_a17_conditional_mapping_transfer`. Use one unique UTC run directory; preserve failed attempts under their identities. Code/data/config/raw readouts/checkpoints stay execution-side. Record `source/`, `configs/`, frozen scientific snapshots, data/hash manifest, strict input access, dataset registry ID, parent/tokenizer IDs, job/profile/image/command receipt, mounted logs, worker environment/progress, stage metrics/TensorBoard/checkpoints, per-record DEV/TEST predictions, equal-norm probes, comparable-level selection receipt, independent analysis and output manifest. Keep dirty source identity and hashes; do not infer a clean Git revision.

Reuse/adapt the inspected A17_03 AnswerLM, collate, frozen-parent carrier, manual SGD, checkpoint/RNG and telemetry helpers. Adapt evaluation for mode/command, list-three decomposition and full competitors. Reject old sensitivity-basis/projection logic: it is not this treatment. Consult the clean training scaffold's checkpoint/observability contracts; do not import its unrelated router intervention or MoE architecture. Submit only through root `templates/execution/acp_submit_template.sh` using the envelope's profile/image keys and an execution certificate. Full requires this run's qualified Smoke identity. Finish current authorized finite runs through results; do not resubmit an existing active job.

Freeze all source/config/contracts/data before GPU execution. Save actual parent-tensor hash, checkpoint field manifest and SHA-256, actual optimizer step/valid targets and loader identity. Register actual Smoke and Full adapter families separately after saving; every adapter requires the exact frozen parent. Do not register planned milestones as saved. Mathematical checks are source/computation checks, not a claim of verified rich rendering.

## 15. Success / Failure / Insufficient Evidence

Old acquisition qualification: endpoint DEV accuracy ≥0.80 for each command on each unseen panel. Failure yields `CONDITIONAL_START_NOT_QUALIFIED` and insufficient retention interpretation, without hiding final measurements. Useful new learning: combined new TEST CE improves by ≥0.01 nat or accuracy improves by ≥1 percentage point from its own starting state. Failure raises insufficient acquired-signal interpretation; baseline skill remains reported.

Under qualified primary branches, a stable negative \(E\) under §10 supports relation-dependent transfer cost relative to consistency. Absence or opposite effects are non-support for H here. Mixed signs are heterogeneous/insufficient for a stable directional claim. An absolute old decline is separately required for a net-harm statement. Joint feasibility success requires endpoint DEV accuracy ≥0.80 in each mode on each panel; failure leaves capacity/optimization feasibility Unknown. Engineering qualification is distinct from all these scientific readers; no gate compels a favorable result or authorizes a closure verdict.

## 16. What This Cannot Claim

No universal task incompatibility; no proof that reversal forces forgetting; no internal common/differential module identification; no benefit of separating experts or parameters; no claim that old CE sensitivity is harmful; no natural-text transfer; no full-model capacity statement from a matrix-only carrier. Output contrasts and CE identities cannot establish a complete parameter-mediated mechanism. Comparable-level selection cannot fully remove difficulty or learning-path confounds. Joint has extra old labels and cannot serve as an equal-supervision winner.

## 17. Block Confirmation, Freeze, And Amendment Ledger

| Block | Scope recorded | Source / authority | State |
|---|---|---|---|
| A | Question, merger, boundary | User adopted merged mapping task and requested reasoning/knowledge update | USER_DELEGATED_BOUNDED_IMPLEMENTATION |
| B | Balanced new data and two unseen panels | Earlier user accepted both unseen types; exact orbit split delegated here | USER_DELEGATED_IMPLEMENTATION_RECORDED |
| C | Neutral commands, visible mode, answer-only CE | Adopted mapping task; earlier answer-loss decision | USER_DELEGATED_IMPLEMENTATION_RECORDED |
| D | Registered Base, last o_proj freeze | Earlier direct o_proj decision; current reused bounded carrier | USER_DELEGATED_IMPLEMENTATION_RECORDED |
| E | SGD, budget and deterministic counting | Inspected trainer and training-observability contract; exact values delegated | USER_DELEGATED_IMPLEMENTATION_RECORDED |
| F | Paired primary effect, rivals, readers, descriptive thresholds | Adopted task-relation comparison; explicit AI operational realization | USER_DELEGATED_IMPLEMENTATION_RECORDED |
| G | Smoke, Full, saves, four reserved H100 ceiling | Explicit execution without intermediate approval and prior resource choice | APPROVED_FOR_IMPLEMENTATION_SMOKE_AND_FULL |

This ledger records explicit authorization and delegated choices; it does not assert that the researcher separately confirmed every AI threshold or accepted a scientific mechanism. Self-review checks question alignment, supervised task, realizable objective, matched primary inputs/exposure, split isolation, constructible readers, artifact completeness and typed branches. Data/runtime checks still must qualify execution. Freeze the scientific body at first GPU start. After start, only append receipts/result links/amendments; retain old values. Each material amendment records time, before/after, reason, visible results, affected blocks, inherited authorization and eligibility impact. Failed attempts remain evidence; no silent changes to labels, tensor, primary endpoint, thresholds or TEST selection.
