# Protocol: A17_02_E01 Fixed-Pool Frequency

[中文](protocol_cn.md)

## 0. Approval Snapshot

Document/approval: `APPROVED_FOR_IMPLEMENTATION_SMOKE_AND_FULL`. Researcher decision on 2026-10-10 Asia/Shanghai: adopt the existing consensus without further pre-execution audit, create an independent frequency Anchor/Protocol, direct `o_proj` as primary and LoRA as preceding capacity control, submit reserved four-H100 Full after Smoke, then frequency and SAE analysis with continuous supervision. This contract formalizes the adopted candidate with no dev-dependent choices. A–G/cross-block audit: consistent; execution authority is the current direct user instruction, not an old draft or Smoke. Scientific interpretation/closure remain `Unknown`.

Purpose: test whether extra A presentations alter B loss differently under same/different visible rules. Role: operationalization/proxy test. Strong rival: generic practice or initial position difficulty, rather than rule-related shared-learning demands. Primary: seed-level rule×presentation interaction at B200. Support/non-support/insufficient are computed statistical branches below, not researcher closure. Boundary: one Base, new fixed pools, restricted updater and two novelty panels. [Anchor](../../../../problem_anchors/17_shared_and_interference_learning/17_02_fixed_pool_frequency/17_02_fixed_pool_frequency_anchor.md) and [Focus](../../../../focus/focus_fixed_pool_frequency_shared_learning.md) own meaning.

## 1. Terminology / Definitions

FIRST/LAST select first/last of three distinct words. A is an additional pool, B the recipient pool. A/B metadata is never an input cue. Same/different relation changes the visible rule applied to the same A lists, not an impossible contradictory label for an identical prefix. Presentation is one answer-bearing training record; a repeated record counts again. Loss is full-vocabulary CE in nats/answer. Order-new holds out order of B-seen unordered content; combination-new holds out unordered content from both pools. Positive after-minus-before loss is worse prediction.

## 2. Anchor Alignment

The independent frequency Anchor owns fixed-B presentation interaction. Fixed-budget allocation and B-only net additions are separate secondary estimands. No representation/SAE fitting, router/expert training or LoRA comparison enters this primary. A source improvement guard does not discard a valid policy result; it only qualifies a separate effective-learning mechanism interpretation. Numerical loss readout is fixed FP32; BF16 is reported secondarily from the same saved weights.

## 3. Tested Hypothesis

Registered two-sided hypothesis: the conditional seed-population median interaction exceeds +0.01 or falls below −0.01 nat/answer. Rival: the median lies within that practical band. A positive interaction can coexist with help in every condition. A reliable negative interaction supports the opposite direction under the same two-sided rule. No directional rescue may be selected from dev.

## 4. Rival Explanations

Exact position/answer marginals and new lists control answer priors and wholesale memorization. Same/different conditions share A/B list identities and random presentation order; visible rule text necessarily differs. Two B roles expose initial FIRST/LAST difficulty. Original Base is independently reset. Constant LR avoids different warmup exposure caused by unequal total answers. B-only addresses added-training net outcomes; the 1000-answer controls address allocation, not pure frequency with B opportunity fixed. Restricting capacity can cause conflicts absent in a fully trainable model.

## 5. Data Construction And Provenance

Input IDs: parent/tokenizer `model_qwen3_0p6b_base`; new dataset `data_a17_fixed_pool_frequency_v2`. Fresh strict checks are required locally and in every pod. Generation seed1010. A and B each contain200 different ordered lists, each rendered under both rules (400 metadata rows/pool). Twenty Chinese single-token continuations are inherited only as vocabulary choices, not old train/dev/test rows. Five disjoint content orbits per pool ×two permutations ×20 cyclic shifts balance every position/answer exactly:10 per word per pool/rule. A/B have100 unordered groups each, no group overlap.

B's other four permutations give disjoint order-new dev/test (two permutations each). Separate five-orbit sets give combination-new dev/test. Dev/test each800 rule rows:200 per rule×novelty cell. All ordered lists are disjoint across pools/dev/test; combination-new groups are absent from both pools and disjoint across dev/test. Order-new references actual B training, not an unused universe. Generated metadata is model-independent; qualification does not expose test to a model. Manifest records generator/tokenizer/split hashes, exact oracle and continuation boundary. The dataset is new, not an adaptation of the previous exposed dev.

For500 presentations, use two complete200-list repeats plus100 records from five complete20-shift blocks chosen by a fixed seed. This preserves exact marginals. For800 use four complete repeats. Record actual exposure per list, pool, answer and rule; unique data count is separate from presentations.

## 6. Learning Task And Permitted Supervision

Prefix is `规则：取第一项/最后一项。列表：w1 w2 w3。答案：`. Input excludes the filled answer; correct answer may legally occur in the list. Exactly one next-token answer target per record, with all other positions ignored. Train full-vocabulary CE; no constrained three-candidate head or auxiliary loss. One fixed template; no hidden pool, expert or frequency label enters input.

## 7. Model / Architecture And Frozen Variants

Original Qwen3-0.6B Base,28 layers, hidden1024; only `model.layers.27.self_attn.o_proj.weight`, shape1024×2048,2,097,152 parameters is trainable. No bias, adapter, router or SAE is inserted. Embedding/tied head, norms, MLP and other Attention weights are frozen. Frozen weights and trainables are loaded FP32; training uses BF16 autocast; primary evaluation uses native FP32 with TF32 off, deterministic algorithms and fixed batch20. Every trajectory begins from the original matrix, not another adapted arm. Four workers are independent single-GPU trajectories; no cross-condition DDP reductions. LoRA remains outside this estimand.

## 8. Training Objective And Optimization

AdamW LR1e-4 from the first update (warmup0, no decay), betas(.9,.95), eps1e-8, weight_decay0, gradient clip1. FP32 trainable weights/moments. Microbatch5 ×accumulation4 =20 valid answers/update, data-parallel size1; exact answer loss sum/20. No skipped step is silently counted; nonfinite loss/gradients stop the stage. Every complete update adds20 to valid-token count. Constant LR is a change from E02 and requires this new frequency Smoke. Objective/component registry: LM answer CE only; total loss equals LM loss, no regularization components.

All trajectories record required TensorBoard tags under each trajectory's `tensorboard/<phase>/`: `tokens/train_lm_loss`, `updates/train_lm_loss`, `tokens/train_total_loss`, `updates/learning_rate`, `progress/tokens_seen`, `progress/optimizer_step`, `progress/effective_tokens_per_update`. Token tags use cumulative valid answers; update debugging tags use optimizer steps as prescribed. Raw metrics preserve every batch/record identity, pool/rule counts, LR and grad norm.

## 9. Conditions, Seeds, And Checkpoints

Per B=FIRST and B=LAST, seven conditions:

| Condition | A relation | A presentations | B presentations | Updates |
|---|---|---:|---:|---:|
| same_200 | same |200|200|20|
| diff_200 | different |200|200|20|
| same_800 | same |800|200|50|
| diff_800 | different |800|200|50|
| b_only | none |0|200|10|
| same_budget | same |500|500|50|
| diff_budget | different |500|500|50|

Exploration seeds29/43/71:42 trajectories,30,000 trained answers,1,500 updates. Confirmation new seeds101/113/127/139/151/163:84 trajectories,60,000 trained answers,3,000 updates. Totals90,000 answers/4,500 updates exclude Smoke, evaluations and calibration replays. Confirmatory seeds and conditions are frozen before exploration; no selection based on dev. Same/different task pairs share pool list presentation order for a given seed/quota and only change A's visible rule.

Save trainable matrix plus optimizer, Python/NumPy/CPU/CUDA RNG, counters, presentation cursor/order hash, config/parent/data IDs at update0,2,ceiling(total_updates/2),final (deduplicated). These correspond to0,40,20×middle and final answer counts; final budgets are200,400 or1000. Final weights require the registered Base to load; no full Base copy is claimed. Original Full endpoints' external resume is NOT_CHECKED unless actually verified; engineering Smoke qualifies updater/cursor restore independently.

## 10. Primary Metric And Frozen Analysis Plan

Only B's current rule enters the recipient metric. For each seed, B role and novelty panel, compute `I=(Ldiff800−Lsame800)−(Ldiff200−Lsame200)` at B200. Primary seed I is the equal average over both roles×both panels. Every component, role, panel, per-record CE/accuracy and mean/median/range is reported; the combined primary is sole confirmatory target. Counts are equal, so this matches record weighting across the four recipient panels. Initial accuracy and final accuracy are secondary, not substitute losses.

Exploration n3 is descriptive, without a95% seed CI or significance claim. Independent training seed is the scientific repetition; cyclic shifts/content groups are dependent and cannot inflate n. Confirmation uses a conservative two-sided sign rule at α.05 and δ=.01: six of six I>δ yields the registered positive branch; six of six I<−δ yields the negative branch (two-sidedp=.03125). Report [minI,maxI], a conservative at-least96.875% seed-median interval under independent identically generated seed effects; it is not a mean CI. If the whole interval lies inside[−δ,δ], report bounded practical median absence. Otherwise unresolved/nonpassing evidence is INSUFFICIENT, not zero effect. No subpanel can rescue a failed combined primary. Mechanism interpretation/closure remain human Unknown.

FP32 native reader is primary. Same fixed matrix is also read in BF16 secondarily; this does not recompute different virtual updates as in the old engineering probes. FP32/BF16 results and any disagreement remain recorded. Smoke fixed-state FP32 and BF16 no-op evaluations must reproduce exactly; failing no-op makes affected evidence ineligible. Confirmation uses a new model-unopened test; exploration uses dev only. Test is not used for checkpoint/LR selection or retries.

## 11. Secondary Metrics And Guards

Net addition: each same/different A200/800 endpoint minus B-only at B200, with unequal total compute explicit. Allocation: each relation's800A/200B minus500A/500B at equal1000 answers, with unequal B opportunity explicit. Report both novelty panels, B directions, seeds and combined summaries. Full-vocabulary CE, accuracy, target probability and effective matrix ΔW norm accompany primary. Initial/mastered states stay visible; saturation does not license selecting favorable checkpoints. No cross-task source-update causation is inferred from endpoint training policies. A useful-source guard does not gate primary estimates.

Mandatory engineering: correct targets, exact quotas, finite required telemetry, independent target count, unchanged frozen versions plus before/after full frozen-byte hash per worker, actual checkpoint hashes, deterministic no-op. Required external restart in Smoke compares saved update2 and the next update3 to an uninterrupted reference. LoRA, SAE, new templates, new vocabulary, rank scans and finite-step mechanism probes are not automatic rescue conditions.

## 12. Known Good / Known Bad / Known Confusing Cases

Good: restored original matrix/native logits; source pool quotas and balanced500 remainders; a useful net addition despite positive interaction. Bad: answer pasted after marker, A/B pool labels in input, test-selected LR, frozen head drift, corrupted cursor or a partial accumulation counted as20. Confusing: opposite B-role interactions cancel in the primary; all-correct accuracy with differing CE; another rule helps B less while still beating B-only. Preserve these distinctions.

## 13. Scientific Procedure And Stage Contracts

1. Preflight: current input strict checks, new-data oracle/tokenizer/split/balance, CPU schedule tests over all registered tasks, selected-source and config/Protocol hashes. Failure blocks training.
2. Smoke: four independent tasks B FIRST/LAST ×same/different800, seed29, at most8 trajectory updates/160 answers each. Initial phase saves at2, writes one next-step reference and restores; an independent process restores2, verifies3, then completes8. Calibration next steps are separate extra80 answer presentations, not repeated scientific trajectory updates. All eval is dev. Pass exact restart, freeze, loss/counter/TensorBoard/no-op and four complete outputs.
3. Full exploration: only after recorded Smoke PASS, all42 independent trajectories, dev-only analysis; no hyperparameter/window selection.
4. Full confirmation: only after all exploration engineering checks pass, frozen84 new-seed trajectories and model-unopened test. This gate protects completeness, not favorable exploration outcomes. Any valid adverse/no-effect trajectory is retained. Scientific conclusions are typed separately from run success.
5. Finish actual saved checkpoints, stage analyses, source/artifact manifests, terminal/platform evidence and bilingual Summary/Detailed; register actual output families via the asset lifecycle. Keep all failures and no silent re-run of opened confirmation.

## 14. Algorithm, Output, And Provenance Contract

Execution surface `acp`; resource profile `h100-4-reserved`; image key `shphd-lite-0911`; environment layer `source/runtime.sh`. Envelope owns expanded tuple/image/submission; use its sole supported template and current dry run. One node/four independent GPU workers, complete task assignment in waves, no hardware fallback. Root coordinates the total live reservation; no competing extra four-GPU node is assumed.

Execution root `/data/250010109/MoE_Router/experiments/20261010_a17_fixed_pool_frequency`. Freeze code/config/Protocol/data manifests and exact command before submission. Each run has a new immutable path, durable pod log, execution certificate and submission receipt. Reuse E02 answer wrapper, no-bias final projection, CPU-tree/exact comparison/telemetry/checkpoint interfaces and current mounted runtime; adapt deterministic quota scheduling and multi-trajectory phases. Do not reuse E02 virtual probes, warmup, exposed dev, LoRA or unrelated SAE/router objectives. Data generator adapts balanced cyclic orbit construction but creates new pools/splits.

Ceilings: one frequency Smoke≤1800 payload seconds; Full exploration≤7200s, confirmation≤14400s, combined≤21600s plus bounded kill grace. Stop on nonfinite, frozen drift, wrong counters/quotas, wrong identity, failed restore/no-op/required telemetry, or ceiling. A resource/engineering stop is not a scientific negative. User requested supervision through full completion; inspect existing job/durable progress with progressively spaced polling, not resubmission. Final saved family, raw analyses, manifest and terminal verification are required. No commit/push/publication or unrelated job interruption is authorized.

## 15. Success / Failure / Insufficient Evidence

Engineering PASS requires all data/runtime/telemetry/freeze/save/restart checks and every required trajectory. FAIL is a demonstrated contract violation; missing required outputs is incomplete. Statistical branches use §10 only after qualified confirmation. Practically absent median is bounded by the registered interval and this carrier; non-significance alone is insufficient. A positive interaction is not net harm; the secondary B-only comparison must establish its own direction. Human mechanism interpretation, utility and closure remain Unknown.

## 16. What This Cannot Claim

No pure frequency manipulation with compute and B opportunity both fixed, exact FLOP matching from answer totals, natural-pretraining mechanism, acquisition from scratch, functional decomposition, unrestricted-model conflict, expert necessity or long-term architecture advantage. Independent seeds remain conditional on one parent/pool family. SAE future analysis requires its separate exact interface and contract and cannot rewrite this frozen policy result.

## 17. Block Confirmation, Freeze, And Amendment Ledger

A–C: researcher adopted the established first/last carrier, independent frequency question, exact-answer supervision and both novelty panels. D: researcher selected direct matrix and LoRA preceding capacity control. E–G: the current explicit delegation adopts the existing complete candidate and authorizes implementation/Smoke/PASS-gated reserved Full plus full supervision; numerical δ/sign rules, seed lists, constant LR and ceilings are frozen implementation of that adopted candidate, not claimed physical laws. The previous A17_01_E03 file is a preserved historical draft; this is the sole current frequency Protocol and the new A17_02 Anchor owns scientific design. No post-dev tuning or confirmation rescue is authorized.

Pre-submission freeze records actual file hashes and source lineage in each run. Frozen bodies are archived execution-side; necessary repairs append an amendment with stage eligibility impact, preserve original source/output and do not relax a guard. No result exists at this freeze. User retains the right to adjust future scope tomorrow; new steering will not silently rewrite completed evidence.

## Pre-submission data qualification amendment01

The initial independent-seed v1 construction passed internal guards, but its finite list universe produced40 test rule rows overlapping previously model-evaluated E01 dev. It was never submitted or model-evaluated in this experiment. Preserve v1 as a historical generated asset; actual input is new v2, drawn only from the27 cyclic content orbits unused by every E01 split. All four new splits/pools are now content-group-disjoint from all old train/dev/test. Model-independent filtering uses only old list identities, not model outcomes or answer losses. Same sizes/marginals/conditions/seeds and estimands are preserved. The prior prepared/unsubmitted source freeze stays archived; create a new actual-source freeze before submission.

## Append-only execution ledger: frequency Smoke

After verifying prior job pt-ujjb8f7a SUCCEEDED/terminal, submitted pt-cgmiw5f3 on the approved four-H100 reserved profile. Actual v2 source/config/Protocol/data freeze and certificate: /data/250010109/MoE_Router/experiments/20261010_a17_fixed_pool_frequency/runs/smoke_4h100_v2_20261009T172146Z. This authorizes no change to the statistical plan; Full still requires the actual Smoke gate.

## Append-only execution ledger: frequency Full

After pt-cgmiw5f3 passed56/56 engineering checks and reached platformSUCCEEDED, submitted pt-ho4byzg4 on four-H100 reserved. Uses the Full source/conditions/new confirmation seeds frozen beforeSmoke; no dev selection. Receipt/certificate: /data/250010109/MoE_Router/experiments/20261010_a17_fixed_pool_frequency/runs/full_4h100_v2_20261009T172612Z. Human scientific judgment remainsUnknown.

## Append-only completion ledger: frequency Full

pt-ho4byzg4 reached platform SUCCEEDED at2026-10-09 17:48:33UTC /2026-10-10 01:48:33Asia/Shanghai. All126 trajectories,90,000 training answers and4500 updates completed; exploration508/508,confirmation1012/1012 and actual-exposure126/126 qualified. All126 saved families were registered after1008 member-file SHA checks. Statistical facts belong in Summary/Detailed; the archived pre-result body and decision rule are unchanged. Actual endpoint SAE description is NOT_RUN. Human mechanism/closureUnknown. Terminal, platform and registration receipts: /data/250010109/MoE_Router/experiments/20261010_a17_fixed_pool_frequency/runs/full_4h100_v2_20261009T172612Z.
