# Protocol: A17_01_E01 First-Stage Engineering Smoke

## 0. Approval Snapshot

Document status: `APPROVED_FOR_IMPLEMENTATION_AND_SMOKE`. Approval source: researcher confirmed the task/tokenizer/loss, both novelty types, four reserved H100 training, A17 migration, model assessment, initial capability checks, then explicitly requested code and measurement to begin. Routine bounded engineering settings below are implementer-selected under that scope, not confirmed scientific operating points. A-G: `CONFIRMED_FOR_SMOKE_SCOPE`; cross-block consistency: `PASS`. Scientific Full remains `NOT_AUTHORIZED`; mechanism judgment `Unknown`.

Purpose: qualify controlled list data, initial capability and short training/update readouts. Role: operationalization/proxy test. Primary Anchor: [A17_01](../../../../problem_anchors/17_shared_and_interference_learning/17_01_controlled_list_prediction_rules/17_01_controlled_list_prediction_rules_anchor.md). Active Focus: [Focus](../../../../focus/focus_list_rule_shared_update.md). Smoke cannot adjudicate shared-learning mechanism or expert utility.

## 1. Terminology / Definitions

FIRST/LAST select positions one/three in a list of three distinct words. A prefix contains the rule/list and ends at `答案：`; the target is the next token. Order-new means exact order unseen but unordered content seen in training. Combination-new means unordered content also unseen. A paired row is not an independent content group.

## 2. Anchor Alignment

Test the carrier and finite observable in Anchor §§4–6. Source s and recipient r are independently FIRST/LAST. Delta is recipient mean loss after a source update minus its mean loss at the same base state; negative helps, positive harms. No-update is required. A smaller benefit is not harm.

## 3. Tested Hypothesis

Engineering hypothesis: the generator, one-answer loss, DDP training, save/resume and virtual-update observable work as declared. Scientific local harm versus shared parsing benefit remains unadjudicated. Initial capability checks answer observed performance on this specific development carrier, not complete abstract mastery.

## 4. Rival Explanations

Position preference, pre-existing mastery/saturation, wrong target alignment, parameter restoration failure, optimizer state drift and excess step size can obscure a learning interpretation. Initial capability, oracle checks, no-op and exact base restoration protect the relevant engineering chain. A harmful finite sign remains descriptive even if a large step explains it.

## 5. Data Construction And Provenance

Twenty qualified Chinese words: 红 蓝 绿 黄 黑 白 紫 灰 金 银 猫 狗 鸟 鱼 牛 马 羊 虎 龙 花. Use local Qwen tokenizer, no chat template, no special tokens and no answer-field input. Template: `规则：取第一项。列表：红 蓝 绿。答案：` and corresponding last-item rule. Actual tokenization verifies prefix(full answer) equals prefix IDs followed by exactly one target token, for every released row.

A deterministic seed-1009 cyclic-orbit generator balances every word/position exactly. Twenty unordered-content orbits × twenty shifts × five orderings create 2,000 training base lists. The unused sixth ordering supplies 200 order-new development and 200 order-new test lists from disjoint orbit halves. Five unused content orbits per combination-new split × twenty shifts × two orders supply 200 development/200 test base lists. FIRST/LAST paired expansion gives train 4,000, dev 800, test 800 rows. Every position/word count is 100 in train and 10 in each evaluation panel. IDs, words, rule, panel, group, prefix, target, token IDs and hashes are saved execution-side.

Both evaluation types are intentionally present. Order-new content overlaps training by definition; exact order must not. Combination-new groups must not overlap training or each other across dev/test. All evaluation exact ordered lists remain disjoint. The balancing structure is declared; this is not iid natural text.

## 6. Learning Task And Permitted Supervision

Each record contributes exactly one full-vocabulary CE target in nats. Feed only prefix IDs; gather the hidden state at its last valid token, then project to full vocabulary. This is mathematically the next-answer prediction without loading the answer as input. Train/dev readers open only their named JSONL. Test is generated and structurally audited but never opened by a model in this Smoke.

## 7. Model / Architecture And Frozen Variants

Dense: registered exact-33B 281,431,040-parameter native eight-layer, hidden-1024, FFN-3072 Dense checkpoint; strict native loader. Qwen Base: registered local HF Qwen3-0.6B-Base, 28-layer, hidden-1024, FFN-3072, original tied embeddings. Train all LM parameters in independent sequential four-rank processes. Existing pretraining optimizer/scheduler are not carried into the new task; new AdamW is deliberate task adaptation, not exact original-pretraining continuation.

S7-fresh: exact-33B eight-layer model with attention-output sidecar. Its native LM forward is preserved; read-only initial capability only, no SAE activation export, no feature analysis, no optimization. Three models are separate carriers, not a matched architecture-effect experiment. S7 checkpoint source must match its actual sidecar config, not older bottleneck code.

## 8. Training Objective And Optimization

Objective is globally answer-weighted CE only; auxiliary component registry is empty. FP32 trainable parameters/optimizer state, BF16 autocast forward/backward, AdamW LR 1e-4, betas (0.9,0.95), epsilon 1e-8, weight decay zero, gradient norm clip 1.0. Native DDP, four ranks, eight rows/rank/microbatch, accumulation two, exactly 64 answer targets/update, balanced FIRST/LAST within every update. Warmup 256 targets; fixed LR thereafter. No update skips allowed; nonfinite loss/gradient fails immediately. Counting advances only at completed updates. Thirty-two updates = 2,048 valid training answers/model. Settings qualify engineering only.

## 9. Conditions, Seeds, And Checkpoints

Seed 17, same fixed data order across Dense/Qwen. S7 read-only first; Dense then Qwen each run 0→16, exit, and new four-rank process restores 16→32. At 16/32 save complete current weights, AdamW/scheduler, per-rank CPU/CUDA/Python/NumPy RNG, counters and stateless sampler position derived from next update. Hash source/config/data/parent manifest. Strict topology/config checks refuse changed resume. Check initial and final dev capability; retain every update's metrics. No test-driven checkpoint selection.

## 10. Primary Metric And Frozen Analysis Plan

Primary Smoke decision is the conjunction of registered data/runtime/telemetry/save/resume/finite-readout gates. Initial and final capability tables report every rule × novelty type and sample-weighted combined CE/accuracy. Mean combined loss = sum of per-answer losses / number of answers; accuracy likewise. Observational unit is an answer; unordered set is the future uncertainty cluster. No CI or significance claim is made by this one-seed Smoke. All-correct observed development performance is flagged `OBSERVED_ALL_CORRECT`, not complete rule mastery.

After update 32, two source batches (32 FIRST,32 LAST, from training only) separately apply one ordinary SGD step of size 1e-5 on all trainable LM parameters, starting at identical saved weights and eval-mode buffers. The new-task AdamW state is untouched. Evaluate full dev recipient panels before/after, restore exact parameters and RNG, then no-op re-read. Record all four rule cells per panel plus combined, self/cross loss deltas, average-gradient norms/dot and relative update norm. Descriptive only; ineffective/saturated sources cannot supply scientific interference evidence.

## 11. Secondary Metrics And Guards

Record full-vocabulary top-1 accuracy, correct-token probability, first/last-position bias and source effectiveness flag (independent same-rule loss decreases). Every record-level loss remains finite; no failed/outlier rows silently excluded. TensorBoard under each model run's `tensorboard/`: `tokens/train_lm_loss`, `updates/train_lm_loss`, `tokens/train_total_loss`, `updates/train_total_loss`, `updates/learning_rate`, `progress/tokens_seen`, `progress/optimizer_step`, `progress/effective_tokens_per_update`. Also record finite gradient norm, memory and valid-answers/sec. Rank 0 alone writes globally reduced quantities. Resume uses separate named segments; monotonic coordinate map and independent target counts must match.

## 12. Known Good / Known Bad / Known Confusing Cases

Good: oracle produces first/last correct labels; combined aggregation matches record totals; masked-prefix loss agrees with the final-position calculation on a tiny learner. Bad: duplicate orders, missing pair, incorrect answer, boundary token mismatch and illicit combination overlap must fail. Confusing: an order-new group intentionally seen in training is valid; an all-correct model is saturated observationally rather than proof of no shared learning. CPU tiny-model tests exercise finite-update sign restoration and one-answer token accounting; remote model gates remain separate.

## 13. Scientific Procedure And Stage Contracts

| Stage | Goal / input | How / why | Output / gate | Handoff |
|---|---|---|---|---|
| Data | Known-rule qualified records | Deterministic generator and independent count/leakage audit | data manifest/qualification; failure stops | registered release |
| Preflight | Target runtime and inputs | Fresh strict registry, hashes, 4 H100 ranks | runtime.json; failure stops | three exact carriers |
| Initial | Existing capability | Frozen dev readout on three carriers | initial_capability.json by both panels | no scientific saturation conclusion |
| Train | One-answer DDP adaptation | 16 updates/save, new process/resume to32 | checkpoint/metrics/TB; failure stops | final dev and virtual update |
| Audit | Artifact and restoration validity | independently read files/tokens/TB/checkpoints | terminal_verification.json PASS/FAIL | report only, no Full |

## 14. Algorithm, Output, And Provenance Contract

Execution root: `/data/250010109/MoE_Router/experiments/20261009_a17_list_rules`. Config: `configs/smoke.json`. Code and data remain execution-side. Required outputs: data JSONL+manifest+qualification; input-access snapshot; frozen code/config manifest; per-model runtime; initial/final capability (including separate/combined novelty); metrics/TB; checkpoints at16/32 and per-rank resume receipts; two-by-two update readout with no-op; terminal_verification; durable pod log; ACP submission receipt and execution certificate. Missing outputs are explicit `MISSING`/`INSUFFICIENT`. Saved states are registered as actual Smoke assets, distinct from input checkpoint identities.

## 15. Success / Failure / Insufficient Evidence

PASS: every engineering gate present/true, 4 ranks and exact token coordinates, complete saves/resume, both novelty reports and finite restored readouts. FAIL: qualified evidence demonstrates a declared data/runtime/coordinate/save/restore violation. INSUFFICIENT: the job is queued, output missing or unfinished. Model low accuracy or saturation does not fail an otherwise qualified engineering Smoke. Scientific result is always `NOT_EVALUATED` in this stage.

## 16. What This Cannot Claim

No expert requirement, shared/unique representation decomposition, natural-pretraining conclusion, clean architecture treatment, long-term sharing benefit, frequency effect or scientific positive/negative verdict. Development readouts cannot become untouched confirmation. Full and frequency training remain unauthorized.

## 17. Block Confirmation, Freeze, And Amendment Ledger

A question/boundary, B paired data/two novelty panels, C tokenizer/answer loss, D two chosen training carriers plus S7 read-only, E bounded engineering optimizer, F engineering decision plus descriptive metrics, G four-H100 reserved Smoke: confirmed for this authorized engineering scope by session instructions. Scientific statistical operating-point choices remain proposed for a future Protocol. Freeze code/config/data identity before submission; record scientific-body SHA256 in run provenance. Later material changes require append-only amendment, and cannot overwrite a started contract. Startup supervision: up to five minutes, first bounded progress/failure; if queued, hand off the same job without resubmission. Job wall ceiling 1,800 seconds (two GPU-hours maximum allocation). No automatic retries or Full submissions.
