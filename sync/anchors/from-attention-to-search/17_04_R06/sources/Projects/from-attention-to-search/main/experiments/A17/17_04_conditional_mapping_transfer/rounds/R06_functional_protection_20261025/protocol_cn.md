# 冻结协议：A17_04 R06 功能导向保护

用户已授权本轮完整设计与有界执行，无需逐项确认。正文为完整对应的英文精确协议；中文研究对象、公式、判据及边界见同轮Anchor中文稿。固定36新+36旧槽、分母72，旧有效0/4/36，64旧TRAIN探针；U/S/F/D×29/43/71，最多36运行×240步。F/D的0:1仍使用旧标签。S保留原1200步调度。240步主终点，新准确率连续两次90%的第二点为次要比较。首个训练更新起4小时，提前10分钟停止训练留出报告；单卡H100 reserve，不扩额。

# Protocol: A17_04 R06 functional protection

## 0. Approval Snapshot
APPROVED_FOR_BOUNDED_FULL by current explicit user request, including routine implementation choices, internal audit, smoke and execution. A-G reflect that request; no inferred permission from earlier results. Execution surface: acp; resource_profile: h100-1-reserved; image_id: shphd-lite-0911. One GPU concurrent within the standing maximum four reserved cards; no quota application, new Work/Codex task, resource fallback or unrelated change. Environment activation reuses the R05 runtime. This is an operationalization/proxy mechanism diagnostic, not algorithm publication.

## 1. Terminology / Definitions
Old=A=mode one FIRST/LAST; new=B=mode two reversed. U is ordinary actual Adam displacement; S initial singular rank-one coefficient attenuation; F old-TRAIN loss-gradient halfspace projection; D direction-preserving norm control. A probe is an additional labelled old TRAIN batch used for local protection, distinct from nonzero old objective slots.

## 2. Anchor Alignment
Primary Anchor is the same-round anchor.md under 17_04/rounds. Existing Focus conditional_mapping_transfer is reused. Purpose: distinguish sensitive direction choice, generic slowing and old-supervision organization at equal new exposure. User owns the question and operational thresholds; AI owns internal consistency checking, not scientific acceptance.

## 3. Tested Hypothesis
F provides extra old/new utility versus U/S, beyond D, especially when objective old supervision is sparse. H1/H2/H3 are enumerated in Anchor; retain all outcomes.

## 4. Rival Explanations
F versus D tests generic local step reduction; paired F-minus-U within k tests relative utility beyond old supervision. More labels, trajectory divergence, finite-step error and one common old model remain limits.

## 5. Data Construction And Provenance
Original conditional_mapping_v1 old/reversed only: TRAIN 2400 each, DEV800 each, original order_new/combination_new panels and two commands. Original data manifest/train/dev SHA are in config/frozen.json. Never open test.jsonl. Old endpoint: E03 attn1_adam/main step1200, 24000 old answers, SHA48595673c24579164e271cfeb1b86be6a234e2dfc06218b74d8ca07e16411b75. Use registered official-a5 Base/tokenizer and R05 frozen native layer27-input caches, bound to these exact inputs. Access snapshot and actual source hashes are retained. Replay old DEV once and require all 800 correct. Historical R02 new and joint endpoints and R05 U/S are traceable background, not reused numerical controls because batch/objective/probe settings differ. An equivalence search of 17_04 named records found no matching F/D matrix.

## 6. Learning Task And Permitted Supervision
Input contains visible mode and command plus three words; predict one next token by full vocabulary CE. Every update has 36 new examples and 36 old input slots, with k=0/4/36 old target losses active; remaining old losses get exactly zero. Protection uses 64 separate old TRAIN probe examples each update for every method. No DEV or TEST label enters gradients or selection. At k=0 only the training objective lacks old replay: all methods access old probe labels, F/D use them. Inactive old slots use a dummy target before loss computation. Count input tokens, slot answers, active target counts and probe label/forward/backward cost separately.

## 7. Model / Architecture And Frozen Variants
Exact Qwen3-0.6B Base plus acquired four matrices; update model.layers.27.self_attn.{q,k,v,o}_proj.weight only, 6291456 elements. FP32, deterministic algorithms, no TF32, native final attention and MLP; frozen blocks0–26 cache is reused after identity checks. All other tensors, including q/k norms, remain frozen; frozen-byte hash and tensor-version guards. No adapter-rank reduction or MoE.

## 8. Training Objective And Optimization
L=(sum36_newCE+sum_k_oldCE)/72. New coefficient is exactly1/72 per new example in every condition. AdamW lr1e-4, betas(.9,.999), eps1e-8, weight_decay0, foreach=False,fused=False; fresh empty Adam state each run. Global objective gradient clip1 before opt.step. Probe gradient is raw gradient of mean64 old losses, not clipped and never accumulated into objective gradient. Save candidate d after Adam, then apply U/S/F/D from Anchor over all four matrices jointly for F/D; S P acts per matrix. Optimizer moments are not modified by filtering. Norms/dots accumulate in float64, parameter displacements FP32. If ||g||²<=1e-24 do not project and increment floor trigger; all nonfinite quantities stop the affected run. d=0 gives zero D displacement. S uses loaded original R05 TS basis and original a(t), t=0..239, denominator1200; no reinterpretation as full left/right subspace protection. Record ideal filtered and realized rounded displacement.

## 9. Conditions, Seeds, And Checkpoints
Seed order29,43,71. For each seed iterate k=0,4,36 and methods U,S,F,D, completing all12 before next seed. Independently shuffled streams of unordered list IDs, preserving paired commands, produce36 new/36 old/64 probes each step. Same seed uses exactly the same streams across methods and k. Old4 chooses two command-pairs from18 pairs by a fixed random slot order rotated by two per step, reshuffled every9 steps; no easy-item selection. Freeze all record IDs and mask order before new results. Max240 steps each. Eval0,1,2,4,8,16,32,64,120,180,240. Save full resumable states0,1,2,16,64,120,180,240 and interruption; no model selection. Save weights, Adam, scheduler position, RNG, exact data cursor/order hash, all counters and projector identity. Necessary step0 baseline evaluation reused, not repeatedly rerun.

## 10. Primary Metric And Frozen Analysis Plan
Primary: step240 old/new full-vocabulary accuracy separately and mean answer CE(nat/answer), fixed800 per mode, four200-example cells. Equal weight three continuation orders from ONE old model, not three independent parents. Record F-minus-U, F-minus-S,F-minus-D old/new pp within each k. Operational support: F-U old average>=5pp, all three old gains>0, each new F-U>=-5pp. No significance claim or model-population CI; report seed values/ranges and all continuous outcomes. Do not drop failed or unmet-learning runs. A missing endpoint is missing, never pooled with a shorter run.
Secondary operating point: new combined DEV accuracy>=90% at two consecutive scheduled readings; report the SECOND reading (and first crossing) old/new performance, exposure, probe labels and elapsed cost. Failure is NOT_REACHED. This does not replace the240-step endpoint. Frequency diagnostic is each seed's F-minus-U gain at0,4,36; strictly increasing gain as k decreases is the predeclared descriptive trend. Three levels do not establish a general law.

## 11. Secondary Metrics And Guards
Every step: objective/probe losses, raw and clipped objective gradient norms/clip flag, ||g||², g·d, g·desired, g·actual, candidate/desired/actual norms, rounding residual, selected16 coefficient displacement energy fraction, projection/floor/zero triggers, counters and phase timings. At steps1,2,4,8,16,32,64,120,180,240 measure same probe loss before/after actual update, finite change, first-order term and remainder. Geometry does not replace behavior. All methods compute same probes. TensorBoard required train_lm_loss is nonzero-target-weighted mean over36+k; actual objective uses72 and is logged separately. Component new_raw/weighted and old_active_raw/weighted; old raw=0 with active_count0 documented as inactive. Primary fairness curves use cumulative NEW answer targets since total nonzero targets differ intentionally; also show total valid prediction targets and updates, probe targets excluded from objective-token coordinate. All input/probe token counters explicit.

## 12. Known Good / Known Bad / Known Confusing Cases
Numeric tests: harmful g·d>0 is removed by F, beneficial dot<=0 unchanged; D matches dF norm and keeps d direction; zero g/d handled; optimizer moments unaffected; projection keeps16-atom meaning. Old DEV replay must100%. Existing R05 cache no-op/shape tests cited; one current actual-batch cached/native comparison bounds new microbatch shapes. Check actual telemetry and external-process exact continuation at steps1->2 on the first U condition before completing its remaining steps, without expanding the run matrix.

## 13. Scientific Procedure And Stage Contracts
Preflight: verify required assets, hashes/data/cache and frozen scope, trace history, freeze config/source/orders; stop only dependent failing work. First U run: evaluate common start, perform first2 authorized updates, validate telemetry and independently replay second update from first saved state in another process; only engineering failure blocks full matrix. Execution: run all conditions in fixed order, retain failing receipts, no optimization-rule changes. Analysis: aggregate all completed readings and retain missingness, compare frozen criteria, write full tables/curves and bilingual Summary/Detailed plus five-paragraph Chinese brief. Completion registers actual checkpoint family and validates links/provenance. No additional training after coverage or budget stop.

## 14. Algorithm, Output, And Provenance Contract
Execution root is /data/250010109/MoE_Router/experiments/20261025_a17_functional_protection. Actual code/config/contracts and imported-source hashes frozen before first update. One H100 reserved worker runs sequentially. From FIRST training update including engineering check, global wallclock limit14400sec; stop launching/advancing training at13800sec to retain600sec reporting allowance. At an in-progress update finish atomic save, mark PARTIAL_BUDGET; never compare as240-step. Eval and reporting stay inside14400sec, using already saved readings if time insufficient. Save explicit wallclock start/deadline, every run status and error. No new quota, resource expansion, Work/Codex task, unrelated experiment mutation, deletion, commit/push or confirmation-TEST access.

## 15. Success / Failure / Insufficient Evidence
F qualifies versus U only by fixed rule above, and direction-specific interpretation additionally needs S/D comparison. If new learning slows substantially, report tradeoff. If U at high replay already solves both and F adds little, prioritize supervision explanation. S effective changes the setting-bound interpretation, not history. Seed inconsistency/new-learning failure is insufficient; do not tune or extend. Missing/engineering-failed conditions remain separate, do not rewrite as negative scientific evidence.

## 16. What This Cannot Claim
No label-free protection, pure frequency isolation, independent pretrained replication, modules, routing, natural-language frequencies, addition transfer, universal optimal direction or permanent deletion of old computation. Old frequency changes target weight too; local F can still increase actual old loss through finite-step curvature and probe generalization.

## 17. Block Confirmation, Freeze, And Amendment Ledger
A-G: confirmed by explicit current task and delegated routine engineering choices; consistency internally PASS before launch. Scientific source request retained verbatim in authorization record. Freeze manifest binds canonical EN/CN Anchor/Protocol, config, source and sampled orders before first update. Three audits (identification/data/numerics) retained. After launch append deviations/amendments; do not edit frozen body. Approval is bounded execution, not positive scientific judgment.
