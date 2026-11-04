派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_26_low_frequency_compositional_reuse/20261024_order_v2/protocol.md`。
[精确原始文件](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_26_low_frequency_compositional_reuse/20261024_order_v2/protocol.md)；研究修改仍回到原件。

---

# Protocol: A15_26 Order V2 Six-Stage And Symbolic Auxiliary Round

[中文](protocol_cn.md)

## 0. Approval Snapshot

- Document status: **APPROVED_FOR_BOUNDED_V2_EXECUTION**, subject to runtime identity binding and engineering gates; this does not claim those gates already passed.
- Authority: current user explicitly requests executing the attached V2 package autonomously to the finite terminal conditions and then analysing causes/hypotheses. Attached instructions are adopted only within that request; current user steering prevails.
- Registered scientific revision: `order_moe_v2`; created 2026-10-24T15:57:22.723159+00:00. Actual design_frozen_at/code/config/data/model hashes: **PENDING runtime freeze receipt**, to be bound before formal learning.
- Primary owner: [A15_26 Anchor](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_26_low_frequency_compositional_reuse/15_26_low_frequency_compositional_reuse_anchor.md). A concurrent R01 Focus was registered after the initial source inspection. It owns that round; this V2 order Protocol has its own explicit user scope and does not rewrite it. Question state stays OPEN.
- Purpose / role: operationalization and controlled proxy test of learned component help, adaptation tradeoffs, exposure and branch/selector utility; not a proved mechanism turned into a production method.
- Minimal setup: exact Qwen3-0.6B Base, native answer generation, three fine-tuned parents, one order rule system, specified update/exposure/branch controls; symbolic permutations are separate auxiliary evidence.
- Execution root: `/data/250010109/MoE_Router/experiments/20261024_order_moe_v2`. Project text owns this contract; runtime payloads stay there.
- Scope: initial 69 order + 48 symbolic training trajectories before qualification branches; bounded one scientific revision per task family; 1/2 single-H100 reserved workers preferred, four-GPU ceiling. No unrelated jobs are displaced.
- Main falsifier: qualified matched controls fail the expected transfer/retention/exposure/branch contrast. Prerequisite or measurement failure yields insufficient/not-applicable, not hypothesis refutation.
- Approval / freeze boundary: the current request already authorizes finite execution; real hash/asset/smoke binding remains an engineering condition, not a request for renewed permission.

## 1. Terminology / Definitions

P is a component-trained parent; B is the unchanged exact Base; C is a field-copy parent. They share one pretrained origin; seeds 29/43/71 produce three independent fine-tuned parents, not independent pretraining runs. An adapter is a new bottleneck branch, not a previously located functional module. Replay means continuing to include old single-operation examples. Oracle routing uses true semantic task labels; learned routing sees actual input hidden state only. CE/NLL is negative natural-log probability of the correct target, reported separately per valid token and per answer.

## 2. Anchor Alignment

The uncertainty is whether previously learned order components help conditional combinations, and under that prerequisite whether slower parent updates and separate residual branches have bounded utility. S1/S2 establish prerequisites; S3 compares learning help; S4 compares update policies; S5 exchanges pair exposure; S6 compares branch capacity, active computation and input selection. Functional intervention provides separate, bounded reuse evidence. No result transfers automatically to the next claim. The pre-V2 symbolic discussion is retained as history; the concurrent R01 now has its own authorized rule-revision experiment, with results Unknown here. It is not an added V2 training obligation.

## 3. Tested Hypothesis

S1: base-amount multiplication qualifies. S2: each discount/comparison/addition component qualifies. S3: P helps combination learning relative to B and C under matched downstream supervision. S4: slowing original candidate parameters with the same added branch improves retention while combination learning remains qualified. S5: the same discount-threshold pair changes with high/low exposure after its marginals are fixed; the interaction with S4 is a second estimand. S6: semantic private branches outperform sharing on qualified learning after both capacity-budget comparisons; a separately trained selector can use the same frozen branches from input. Specific intermediate-state replacement is required for an internal-carrier claim.

## 4. Rival Explanations

The decisive alternatives are missing component ability, format adaptation, extra prior training, arithmetic fluency, parent starting performance, extra capacity, altered active computation, task-label supervision, load, answer distribution, fixed numerical difficulty, global slowing and general intervention damage. P/B/C, U/J/S/F/G/Z, frequency exchange, shared/private budget lines, hash grouping, routing shuffle and matched activation controls preserve these distinctions. No claim of perfect matching is made for P versus C or private versus shared capacity.

## 5. Data Construction And Provenance

The exact scientific clauses in Appendix A are adopted without altering their source bytes. All amounts use integer cents; price 1–200 integer yuan, quantity 1–12, discounts 80/85/90/95%, thresholds 50/75/100/125 yuan and shipping 5/10/15 yuan. Equality gives free shipping; the threshold uses discounted merchandise when discount applies, and shipping is not discounted. Complete-order split unit is the canonical numerical pair (p,q), shared across families, renderings and derived diagnostics. Single-operation tasks without p,q use canonical-input deduplication and separate splits, with intermediate-value overlap reported rather than called leakage.

Source targets are up to 2048/256/512 unique cases per order family and single task where constructible. The finite 2400 (p,q) pool at 70/15/15 yields 1680/360/360 numerical pairs; a requested independent count exceeding that support must be reduced and recorded, never padded by paraphrases. The actual builder manifest determines unique canonical counts and selected validation/test subsets before formal testing. Rendered templates are exposures, not independent cases. A clear primary prompt, two training variants and one held-out wording variant remain separately evaluated. Input/model/data identities and all current input asset IDs must be recorded in the runtime freeze before full execution.

Use two independently implemented label calculators, at least 24 canonical order checks covering four families and threshold boundaries, exact exposure/marginal checks, simple shortcut baselines and split-disjointness checks. The packaged 24 semantic examples are engineering examples only. Formal test is unavailable for method selection, stopping, revision choice and candidate selection.

## 6. Learning Task And Permitted Supervision

Base uses native causal LM encoding, no chat template. Each prompt ends with the fixed suffix `\n答案：`. Main orders output only one amount with exactly two decimal places; threshold-only single questions output 包邮 or 不包邮. No true intermediate amount is supplied in main combination training and no chain-of-thought is requested. Answer-token and EOS targets are supervised; prompt/padding targets are ignored. Scoring requires one canonical answer, separates format errors, and cannot choose a true-looking value among multiple generated numbers. Generation is deterministic, unrestricted over the native vocabulary, with fixed max-new-token/stopping settings in the frozen implementation config. True/wrong/swapped intermediate information is explicitly diagnostic and advantaged.

## 7. Model / Architecture And Frozen Variants

Input model/tokenizer asset: `model_qwen3_0p6b_base_official_a5`, physical source `/data/250010109/model_cache/Qwen3-0.6B-Base-official`; actual disk hashes, tokenizer revision and strict current access receipt bind the runtime. R05's learned reversed-rule checkpoint is not a parent. Initial updates use the actual last layer's Q/K/V/O matrices; other Base parameters are frozen. Actual layer number, shapes and trainable counts are emitted from the loaded model.

Adapter input is the final native attention output before its existing residual addition. Its additional output is B GELU(Ah), bottleneck 32, A randomly initialized and B zero; the native attention output is added exactly once. All comparable branch initializations match within each parent seed. U adds no adapter and updates parent at 1e-4. J uses parent 1e-4/adapter 1e-3; S uses 1e-5/1e-3; F freezes all parent weights and uses adapter 1e-3; G uses 1e-5/1e-4. Z is unchanged parent evaluation. J/S/F are same-structure primary comparisons; U differs in capacity and G tests overall slowing.

S6 fixes the P parent: R1 shared32 reuses F balanced; R2 has four private32 adapters selected by known task type; R3 shared128 approximately matches R2 total branch capacity; R4 private4x8 approximately matches R1 total capacity; R5 private4x32 uses stable data-ID hashing, independent of answer. Report exact bias/router parameters and active FLOPs. Old single-task routing is S1→BASE, S2a→DISCOUNT, S2b/c/d→SHIPPING; this supervision advantage is explicit. Never give each branch extra full-data supervision to compensate different subsets.

The learned selector freezes P and R2 adapters. It reads the last prompt token's pre-branch hidden state through hidden→64→4 softmax, once per prompt, reusing that weight vector for all answer positions. Only final-answer NLL trains it for 2000 updates. All four branches are computed in training: no top-one training-compute claim. Evaluate soft and hard top-one deployment, true-label routing, uniform mixture, each fixed branch and load-matched random/shuffled routing on the same frozen branches and inputs. Ground-truth labels, answers, true intermediate values and future answer tokens are forbidden selector inputs.

## 8. Training Objective And Optimization

AdamW uses betas (0.9,0.999), eps 1e-8, weight decay 0, clip global grad norm 1 and constant group learning rates above. Each downstream arm has a fresh optimizer from the same parent weights. Training/inference dropout is disabled. FP32 is the registered precision, TF32 disabled, optimizer state FP32. A precision change requires a result-before numerical comparison and a common amendment for all affected conditions.

Effective batch is 32 records, via accumulation if needed. Ten batches contain exactly 288 new and 32 old records; order-family new counts and old replay order match across compared policies. The objective is 0.9 times the new-subset token-mean NLL plus 0.1 times the old-subset token-mean NLL. In no-replay sensitivity, only the old weighted term becomes zero; the same records, new examples, new-loss weight and forward exposure remain. This reduces effective supervised targets and is not equal-total-supervision training. Parent P/C uses globally target-token-weighted NLL across its balanced task samples. No auxiliary or router load loss is added.

Record the raw all-supervised-target globally token-weighted LM NLL separately from the weighted optimization objective. TensorBoard `<run_root>/tensorboard/` must contain `tokens/train_lm_loss`, `updates/train_lm_loss`, `tokens/train_total_loss`, `updates/learning_rate`, `progress/tokens_seen`, `progress/optimizer_step`, `progress/effective_tokens_per_update`; enabled `new_answer_nll` and `old_answer_nll` components have tokens/updates raw and weighted tags with explicit denominators. No-replay's old weighted component is zero; raw old loss remains diagnostic. Tokens_seen counts nonignored answer/EOS targets in completed accumulation windows once, with effective-loss-target counts also explicit. Restore both raw/weighted counters, optimizer step, RNG and cursor on resume.

Primary loss-curve coordinate is cumulative valid prediction tokens; new-order exposure is an additional package-requested axis. Update axes are secondary unless effective tokens/update exactly match. Between methods at one frequency condition the same full record stream ensures exact valid-target equality. Between different frequency distributions, answer lengths may differ; show actual tokens and new-record exposure rather than pretending updates are equal-token comparisons. No GPU-count increase changes effective batch, order or reduction.

## 9. Conditions, Seeds, And Checkpoints

Independent fine-tuning parent seeds are 29,43,71 with one fixed dataset split. P/C each train 3000 updates; every downstream trajectory including learned selector trains 2000. Save 0,1,10,50,100,250,500,1000,1500,2000 and parent 3000. Fixed endpoint is primary, never a best-validation replacement. Preserve checkpoints, optimizer/RNG/cursors, actual target counts and manifests in execution storage.

| Order trajectories per parent seed | Count | Reuse/dependency |
| --- | ---: | --- |
| P and C parents | 2 | B has no parent training |
| P/B/C joint J balanced transfer | 3 | P-J balanced serves S3/S4/S5 |
| P-U/S/F/G balanced | 4 | J already counted; Z evaluation only |
| P-J/S/F unbalanced and exchanged | 6 | Balanced reused |
| P-J/S/F balanced with old loss zero | 3 | Same new exposure; reduced effective supervision |
| S6 R2/R3/R4/R5 | 4 | R1 is F balanced |
| Learned selector on frozen R2 | 1 | Subject to branch qualification |
| **Unique total** | **23** | **69 over three seeds** |

Symbolic auxiliary retains legacy transfer U: P-U/B-U/C-U balanced. Its strategy matrix is P-U/F/J/S × balanced/unbalanced/exchanged; P-U balanced is the same transfer trajectory, so there are 14 unique combination trajectories plus two P/C parents per seed, 16 per seed and 48 total. The symbolic C parent retains the legacy alternative-permutation task; unlike the order field-copy C, it may introduce incorrect-mapping interference. Disclose this difference. Apply the V2 3000/2000 steps, rates, saves and exact 10% replay to this previously unspecified symbolic budget. Then new symbolic exposure is 57600, exactly 400 × 144 pair cycles. The 69+48=117 counts are finite plans, not unconditional obligations when scientific prerequisites fail.

Order downstream exposure is 64000 total records, 57600 complete orders and 6400 replay records. Balanced family allocation gives 14400 BOTH records, exactly 100 × 144 cycles. Balanced BOTH pairs each appear 900 times; unbalanced high/low pairs 1600/200 times; d and T marginals 3600 each, with high identity exchanged. Non-BOTH exposure and replay remain identical. Deterministic within-pair input cycling records any maximum-one exposure differences.

## 10. Primary Metric And Frozen Analysis Plan

Exact canonical answer accuracy is primary, with four complete families equally weighted and 16 BOTH pairs equally weighted at test. Report each component, parent seed, family, pair, high/low identity, wording split and threshold stratum before aggregate means/ranges. NLL per token, NLL per answer, target length and format accuracy are separate. Test predictions include prediction/target/loss/family/condition/data_id/split/checkpoint/protocol_hash. Missing, failed or ineligible arms remain visible; never substitute a winner seed or unqualified best checkpoint.

S3 reports P−B and P−C at the fixed endpoint and common exposure curve. S4 primary is J/S/F; U/G are declared controls. S5 measures same-pair high-minus-low accuracy under exchange and the low/high difference in S−J and F−J benefits, separately from the main exposure effect. S6 compares R2 with R1/R3/R4/R5 on exact total parameters and active compute; router interventions hold branches fixed. Speed-to-qualification requires two consecutive saved points; right-censor failures.

Report all three parent seeds separately, then arithmetic mean and range. Within-parent paired bootstrap resamples canonical numerical families, not template rows; 2000 draws with fixed seed 20261024 and two-sided 2.5/97.5% percentiles are a registered engineering resolution of the package's unspecified bootstrap count. Symbolic pairing clusters combination-input cases and reports small support. These conditional intervals are not cross-training confidence intervals. No significance fishing or pooled p-value across tasks; supplementary contrasts are exploratory. Test unsealing occurs only after scientific body, executable/data hashes and eligibility rules are frozen. No test-dependent choices or stopping.

## 11. Secondary Metrics And Guards

Track validation/train gaps, shortcut baseline accuracy, charged/free and threshold-distance strata, equal-base-amount consistency, wordings, true/wrong intermediate diagnostics, branch scaling 0/0.5/1, group gradients and actual/candidate optimizer step norms, clipping, cumulative step length, cumulative squared length and endpoint net displacement. F's parent hash must remain exact. Learning-rate ratios do not establish displacement ratios. Report total parameters, trainable parameters, active computation, supervision and prior-training costs whenever using “better.”

The internal diagnostic uses exactly one predeclared position: final-layer attention output before residual addition at the last prompt token. Candidate one replaces its full vector; candidate two projects controlled paired hidden differences onto one rank-one direction fitted on diagnostic data. Choose at most once on the diagnostic split, then one locked confirmation pass. Keep recipient subsequent rules fixed; compare different intermediate amounts with different expected answers, same-amount/different-surface donors, irrelevant position and same-norm random interventions. Full-vector movement may transfer rule or answer surface; late answer carriage is a live rival, so decoding, damage or donor-answer copying alone cannot qualify a computation-reuse direction. No qualified candidate means internal reuse UNLOCATED/Unknown and ends the search.

## 12. Known Good / Known Bad / Known Confusing Cases

Known good: 50 yuan × 2 with 80% discount gives 80.00 yuan, threshold 100.00 and shipping 5.00 gives 85.00. At discounted amount exactly 100.00, shipping is free. Known bad calculators compare the undiscounted amount, use > instead of >=, or discount the shipping fee; the independent labels must reject them. Known confusing: same final amount can arise from different base values; unchanged answers after a rule edit may be legitimately non-triggering and must not inflate conditional-switch accuracy. Packaged examples are not held-out evidence.

## 13. Scientific Procedure And Stage Contracts

| Stage | Goal / operation | Expected artifact and handoff | Qualification/failure |
| --- | --- | --- | --- |
| E0 | Rules, memory, ownership and exact source audit | Source hashes, Protocol, run plan and current input-access receipt | Missing permission/resources blocks dependent execution only |
| E1 | CPU labels/splits/marginals; real tokenizer, masks and unrestricted Base generation; bounded smoke | Data audit, Base per-item predictions, zero-insertion/freezing/zero-LR/resume/token checks | Engineering errors repaired before scientific evidence |
| E2 | Seed29 P/C parents and all S1/S2 validation | Parent states and per-component scores | Every component ≥95%; at most one registered scientific revision |
| E3 | Seed29 eligible S3–S6 and functional diagnostics | Full first-seed view, including all prescribed negatives | Learning gates below determine allowed dependent claims |
| E4 | Same final protocol for seed43/71; symbolic in idle authorized slots | All seeds and auxiliary contrasts | Never select seeds or arms after first-seed results |
| E5 | Reaggregate and independently reload one method per seed | Fixed-endpoint prediction replay, hashes, tables, reading package | Exit 0 alone is insufficient; require reached steps and real payloads |

Initial qualification range is final attention Q/K/V/O. The sole scientific revision per task family is selected before its confirmation test: either increase parent/downstream caps to 6000/4000, expand to final attention+MLP while keeping steps/rates, or a capacity change with proportional controls. Only one option is allowed, never stacked. The result-before contingency selected for implementation is **attention+MLP expansion**, triggered only if initial P single-component validation fails or the prescribed combination qualification fails and train/validation evidence makes this a justified qualification attempt. Record that evidence, exact affected arms and revision before any revised run; retain original negative runs. Every affected comparison restarts from the same legal origin with the same final scope, including other seeds. This is a permitted contingency, not an already-triggered amendment. If the observed evidence does not justify this option, retain the initial negative and mark the remaining scientific decision Unknown rather than change budgets silently.

After one revision, if P components still fail, allow one P-J direct-combination qualification trajectory per seed and mark dependent protection/reuse comparisons NOT_APPLICABLE. Independent Base/C feasibility may be reported if already planned and meaningful, without claiming mastered-component transfer. If P qualifies but all combination arms fail, preserve the specified learning comparisons and restrict S6 to shared32 versus oracle4x32 qualification; selector may receive forward/load/capability diagnostics but no routing-utility verdict. If Base already solves combinations, retain ceiling and registered frequency/retention diagnosis; do not secretly increase difficulty.

Engineering issues (labels, leakage, masks, incorrect update sets, cache/precision mismatch, bad saving) require a logged repair and affected rerun from a legal checkpoint/start. They are not scientific negative results and do not consume the single scientific revision, but repeated errors cannot be silently rerun. Pending or failed dependencies stay explicit in every stage.

## 14. Algorithm, Output, And Provenance Contract

Execution root: `/data/250010109/MoE_Router/experiments/20261024_order_moe_v2`. The project holds text/small provenance only; model/data/cache/prediction payloads remain execution-side. Use one deterministic plan with IDs containing task_family/parent_seed/condition/frequency/replay/protocol_version, explicit dependencies and no duplicate shared trajectories. `run_plan.csv` records all plans; `run_status.csv` records timestamps, GPU/PID/job, heartbeat, step, exit code, saved endpoint and reason. Monitor this authorized pipeline to terminal state, respecting the user's explicit full-run request.

Freeze actual model/tokenizer/data/code/config hashes and environment receipts before each scientific runtime. Frozen-prefix cache may store only the first 27 blocks while all updated layers are executed natively. Prove cached/uncached alignment under actual train/eval, positions, masks, padding, dtype and batch shapes, including logits, generation and argmax. Never cache a layer later updated. Register actual saved final/milestone checkpoint families through the root asset lifecycle before handoff; actual full resumability is separately proven, not inferred from saved weights. Save optimizer, RNG, data cursors, counters and required source identity; perform an external-process next-step recovery check.

Resource choice follows the latest user steering: prefer one or two single-H100 reserved workers, using `h100-1-reserved` for independent small trajectories; maximum four H100 reserved across this task. Check actual pool/other work first; queue rather than preempt unrelated jobs or substitute paid/larger resources. Use the current root execution envelope's supported submission entry, exact image/runtime/profile and durable receipts. No new hardware pool, unrelated Work/Codex conversation or eight-billion model. Record measured seconds/step and per-trajectory/whole-matrix ETA in run_plan before scale-up and update with actual timing; no promised overnight deadline.

Deliver morning_readme, observations_cn, ai_interpretation_cn, hypothesis_update_cn, Anchor/Protocol and revisions, conversation memory link, run plan/status, result manifest, tables/figures, predictions/logs/checkpoint loading entry, reproduction commands, input/code/model hashes and audit report. Factual reports precede independent AI cause analysis; the current user explicitly requests analysis and hypothesis advancement without an intermediate review pause. AI hypotheses remain suggestions, not researcher acceptance or authorization for extra runs. The package's structural checker is necessary but not a scientific audit.

## 15. Success / Failure / Insufficient Evidence

S1/S2 validation requires ≥95% for every single operation. Full-order eligibility is ≥90% each family and ≥95% overall; S5 low subset ≥90%. S4 retention requires component macro decline ≤1 percentage point, every component ≥95%, and combination decline versus J ≤2 points. S6 benefit requires qualified learning and ≥2-point combination macro gain or ≥20% less supervision to stable eligibility, with old capability no worse by >1 point. Thresholds are practical design constants, not significance tests or universal truths. Confidence limits and seed direction remain visible, and coarse samples may make a two-point claim inconclusive.

Stage terminal types are COMPLETE, NEGATIVE_RESULT, INCONCLUSIVE and NOT_APPLICABLE, each with evidence and boundary. RUNNING/BLOCKED/FAILED cannot be relabeled complete. Overall closure requires every necessary stage terminal and no overlooked active work, actual endpoint saves, finite metrics, per-item predictions and replay audit. A parent or expert prerequisite failure is not evidence that all reuse or routing is false.

## 16. What This Cannot Claim

Semantic task graphs are label definitions, not neural modularity. Training success alone does not prove old internal computation is reused. Parameter freezing does not guarantee output retention after adding a branch. S6 oracle grouping contains task supervision; soft selection computes all branches and does not establish sparse MoE. These synthetic order/symbol results do not establish natural-language feature semantics, eight-billion scaling, complete explanations of old frequency routing, universal low-rank experts or a best hierarchy.

## 17. Block Confirmation, Freeze, And Amendment Ledger

| Block | Scientific source | Status before runtime freeze |
| --- | --- | --- |
| A question/boundary | User's adoption of V2; current A15_26 | CONFIRMED_FOR_BOUNDED_V2 |
| B data/provenance | V2 Data §§1–6, finite-support implementation audit | CONFIRMED; actual manifest hash pending bind |
| C supervision | V2 Data §7 and Training; native prompt and answer/EOS mask | CONFIRMED; smoke required |
| D architecture | V2 Training A/E/G/G.1; actual layer/count emission | CONFIRMED; actual source hash pending bind |
| E objective/optimization | V2 defaults plus explicit replay token reduction above | CONFIRMED; implementation equivalence required |
| F metrics/analysis | V2 thresholds/stats; all seeds/fixed endpoint | CONFIRMED_FOR_BOUNDED_V2 |
| G resources/operations | Current user authorization and 1/2-preferred, 4-ceiling steering | CONFIRMED; current platform receipt required |

The user has explicitly authorized implementation, CPU tests, bounded engineering smoke and full finite protocol with permitted qualification handling; do not ask again for these scopes. No Focus is fabricated or overwritten: the concurrent R01 Focus retains its scope; the current user instruction and Anchor are the direct authorization/meaning sources for this V2 order round, recorded as an explicit exception to the skill's ordinary Focus-first drafting preference. Scientific question remains OPEN, results NOT RUN at protocol registration, mechanism acceptance Unknown.

Runtime execution is permitted only after the actual source/config/data/model identity ledger is bound and engineering gates pass. The scientific body/source clauses are frozen by digest at that point. Before/after values, reason, visible train/validation/test state, affected conditions, authorization and eligibility effect are append-only in `revisions.md`. After start, do not rewrite the registered scientific body to match observed results; status links and provenance receipts may append. Output state must never be inferred from process acceptance or exit code alone.

## Appendix A. Adopted Exact Scientific Source Clauses / 逐字科学条款

The following UTF-8 text is copied verbatim from the package; the original source files and hashes remain in [sources](sources/README.md). Package instructions to request already-granted permission or create another conversation are superseded by the current user request. Current user resource steering and the explicit engineering resolutions in this Protocol prevail where stated. No result is contained here.

### Source: 02_ANCHOR.txt

```text
研究 Anchor V2
主题：订单条件组合中的已有计算复用与 MoE 学习分工
状态：执行前设计；没有本轮新训练结果。

目的
上次讨论提出：已掌握、仍可复用的计算降低更新速度，未解决的细粒度差异继续学习，并在有必要时分化成专家。
本次研究：在同一订单系统中，逐步检验基础操作、条件组合、更新速度、组合频率和分开学习，判断这条链的哪些环节成立。

语义区别
表面不同：换商品名、数字或措辞，不必改变处理方式。
条件不同：已有基础处理仍需要，但折扣/包邮条件改变后续处理。
能力缺口：基础乘法、比较或加法本身还不会，不能直接归因于不会组合。
已掌握不一定共同；共同需要不一定应该共同更新；剩余差异不一定需要多个专家。

与导师讨论的对应
1. 共同使用与共同更新是两件事：本轮的核心比较。
2. 多粒度信息可组合：用单项与组合任务具体化，不把数学类别树当成模型结构事实。
3. 低维信息可能足够路由，专家本身不必低秩：在最后阶段分离已知规则分配和学习路由。
4. 频率可能影响学习进度：控制操作/条件边际曝光，改变条件组合频率，不混同短程/长程。
5. 汇报须指出新旧方案差别：旧频率分桶、top16系数保护与本轮语义组合不是同一个实验。
这些是讨论归纳，不是导师逐字引用或已证明定理。

六阶段及假设
S1/H1 基础资格：模型能在留出订单数值上计算基础价格。若未达到，本轮“只差组合”前提不成立。
S2/H2 条件资格：直接给基础金额时，模型能完成折扣、门槛比较、运费加法及相应规则。若失败需定位单项而非归咎组合。
S3/H3 组合迁移：组成操作预训练有助于完整订单的学习或留出泛化，相比未预训练和等格式对照。若只有训练集提升，不能称组合泛化。
S4/H4 更新分工：开放相同新增路径时，对父模型候选更新范围采用小步长，可比正常更新更好兼顾基础操作与组合学习；固定父模型作为端点，不预设一定最佳。
S5/H5 频率条件：基础/规则边际曝光相同，组合曝光改变仍影响组合学习；进一步检查 S4 的收益是否随频率变化。两层判断分开报告。
S6/H6 专家价值：同一基础模型上，组合差异分别学习比共享新增分支更有价值；容量、活跃计算、负载和监督解释须分别控制。路由能否挑对分支是独立子假设 H6b。

关键竞争解释
- 看似组合难：实际上基础操作不会，或指令/答案格式变化。
- 看似复用：只是预训练更久、熟悉输入格式或记住订单答案。
- 看似保护有效：只是所有部分学慢、组合没学会。
- 看似分专家有效：只是更多总参数、已知任务标签、更少干扰数据或更多训练计算。
- 看似低频困难：实际上固定组合难、答案分布、边界距离或数值范围不同。
- 看似功能分离：只是选定参数不动，但后续输出仍可被其他更新改写。

主张强度
语义计算图是任务定义。行为成功是学习证据。功能复用需定向干预并控制一般破坏。参数保护不等于功能保护。合成订单结果不直接证明自然语言 MoE 收益。
不在本轮回答：长短程物理距离、所有层的低秩性、原频率分发失败的完整因果解释、8B或预训练尺度效果。

归属
由执行 Agent 读取最新图谱后决定。建议 A15 MoE 主线承接问题，A17 合适节点承载受控学习验证；A15_25 若只允许关系图，则只加证据链接而不扩写其定义。旧结果回链 A15_24 与 A17_04 R05，保留各自边界。

阶段性认识更新格式
原以为什么 → 本阶段改变哪个因素 → 实际看见什么 → 哪个竞争解释被削弱 → 仍不能说什么 → 下一阶段为何必要。

```

### Source: 03_DATA_PROTOCOL.txt

```text
数据与评价协议

1. 任务语义 唯一解释
所有金额以整数分保存，提示用两位小数元展示；用整数或 Decimal 计算，禁止浮点误差标签。
变量：单价 p，件数 q，基础金额 b=p*q，折扣百分数 d，折后金额 s=b*d/100，包邮门槛 T，运费 f。
本轮选择可精确得到整数分的数值，不引入四舍五入争议。达到门槛即包邮（>=），运费不参与折扣，门槛比较的是折后商品金额。
四类完整订单：
BASE：y=b。
DISCOUNT：y=s。
SHIPPING：不打折，y=b + f*I(b<T)。
BOTH：先打折再判断，y=s + f*I(s<T)。
题面必须说明生效规则，不让模型猜门槛、折扣或处理顺序。家族身份可用于分层评价/已知标签路由参照，但不作为 learned router 的额外输入。

单项任务
S1 给 p,q，预测 b。
S2a 直接给 b,d，预测 s。
S2b 直接给 s,T，回答“包邮/不包邮”。
S2c 直接给 s,f 和明确是否收费，预测最终金额。
S2d 直接给 s,T,f，预测最终金额。
S2d 是条件判断与加法整合；不能单独代替 S2b/c 定位。
S3–S6 完整订单仅输出最终金额；主实验不提供真实 b 或 s，不要求输出思维过程。
诊断时可以单独问 b/s，但独立问答正确不证明最终回答沿用同一个内部计算。

2. 数值和样本规模 初始默认
p取1–200元的整数元，q取1–12件。折扣 d∈{80,85,90,95}；门槛 T∈{50,75,100,125}元；运费 f∈{5,10,15}元。
BASE/SHIPPING不使用折扣，不能为了统一字段偷偷乘一个隐藏折扣。正式提示可不显示无关字段。
自动生成候选池，再按规范切分：建议每类完整订单训练2048条、验证256条、测试512条，四类共8192/1024/2048。单项每类至少2048训练、256验证、512测试，必要的重复监督必须按曝光而非独立样本计数。
若唯一题目组合不足或配平失败，不通过改名或改模板伪造新样本；缩小实际规模并登记原因、评估分辨率。

3. 防泄漏
按基础数值对 (p,q) 划分 train/validation/test，70/15/15；同一基础数值对的各类订单、措辞、衍生诊断共享划分。不得将最终测试题改写后加入训练。
单项折扣/比较等没有 p,q 的任务单独按其规范输入元组去重与切分。记录它与完整题中间值的重合；基础操作训练本来允许见过中间数值，不得将“出现同一数值”误报成泄漏，也不得把这种测试称为全数值未见。
所有最终测试仅在协议锁定后运行。方法/层/干预强度选择只能使用验证/专用诊断集，不能通过测试结果挑选。
数值划分与模板划分分开：主测试检验留出数值对；补充测试检验未用于训练的措辞。两者分别报告。
固定一个清楚模板作为主任务，2个表述变体训练，1个完全留出的表述变体辅助评价。不要把文本改写数量算成独立数值案例数。

4. 边界和捷径审计
为 s<T、s=T、s>T 以及接近/远离门槛设独立评价层。边界集合是额外压力测试，若刻意富集，不能混进自然分布均值而不说明。
检查仅预测 b、仅预测 s、总加运费、总不加运费、忽略模式、最近训练答案等简单基线。报告规则切换真正改变答案的子集；禁止用许多未触发条件的简单题冲高分。
先抽取至少24条真实数据检查：每类6条，覆盖边界、折扣触发、不同金额。使用两个独立写法的标签计算器逐条一致；不要让模型自身做唯一判题器。
本包07文件只是教学样例，不可作为正式测试证据。

5. 频率设计 S5
只在 BOTH 家族操纵 d×T 的16种组合频率，其余家族曝光不变。
4×4棋盘每行每列2个高频、2个低频；高低比8:1，另设均衡和高低身份交换。
所有分布具有相同训练监督总数、同样的 d 边际计数、T 边际计数。每一组合使用同一套合法 (p,q,f) 训练池并循环，保证整体 (p,q,f) 曝光可比。使用确定计数构造/平衡批次，不只声称随机期望相同。
一个均衡样本周期16种组合各9次，共144次；不均衡周期高频8种各16次、低频8种各2次，共144次，行列各36次。交换时高低反转。
同一组合内部各基础数值的曝光差最多1次，记录实际差；若要完全平衡，使用完整周期。训练步数须与周期相容，或报告不足一个周期的实际偏差。
主测试始终对16种组合等权，统计同一个组合在高/低身份下的配对差。逐组合配对有助排除固定难度，不保证所有混杂已消除。
报告各分布答案频率、包邮比例、边界距离、金额范围；频率与这些内容仍可能共同作用。不得把没有操纵的 CrossCoder 激活频率写成因果变量。
S5保留独立基础回放数据的曝光；要比较低频方案收益，必须方法间使用同一份采样序列。

6. 回放与预算
主实验批次32条：每10批共320条中32条旧单项回放、288条完整订单，回放恰好10%；按循环精确安排，不能用近似概率掩盖差异。
S4/S5/S6各比较内回放序列完全相同、组合总曝光相同。
无回放敏感性：不要简单把旧题替换成更多新题。保持每批新题及其损失权重0.9不变，将旧题损失置零；报告有效监督减少，不能称等总监督。可保持相同前向计算以排除计算预算差，注明浪费成本。
H3未预训练父模型在主实验中也收到同样回放，估计的是先前基础训练在当前相同监督条件下的收益。另报早期学习曲线，不能只看最终饱和分数。

7. 评分
无工具、无计算器辅助、无答案候选限制的原生生成，temperature=0，固定最大新token数与停止规则。
只提取规范的单一最终金额。格式错误单列；不得用答案真值从多个生成数字中挑最接近的一个。
金额精确到分，使用 Decimal 比较；金额准确率、格式正确率分别报告。主loss为答案token平均NLL，另报每答案NLL总和与答案长度，避免长数字被混淆。
tokenizer/model revision、special tokens、mask、padding、EOS监督、生成配置全部固定。不能用多选概率代替开放生成而不说明。

8. 判定门槛 在正式测试前锁定
S1：验证基础价格准确率≥95%，留出数值测试单独核查。
S2：每个单项验证≥95%，边界压力集另报；不能靠平均掩盖比较失败。
S3–S6组合学习资格：四类完整订单各≥90%，总体≥95%；S5低频子集≥90%。这些是实用阈值，不是普适定理。
S4保留：单项宏平均相对父模型下降≤1个百分点且各单项≥95%；组合相对正常更新下降≤2个百分点。若基线本就不合格，不以“下降少”称成功。
S6分支收益：在学习资格通过时，组合宏平均提高≥2个百分点或达到固定资格所需监督减少≥20%，且旧单项不劣于1个百分点。最终点和学习速度分开，速度至少连续两个保存点通过；未达资格时报告右删失，不填为最大步数。
阈值不足以建立统计结论；同时展示各种子和配对不确定性，样本不足就说不能排除小差异。

9. 频率主张的精确范围
本轮改变的是折扣参数与门槛参数的配对频率，不直接等于不同算法的出现频率，更不是自然语义feature频率。它是组合曝光的受控入口。若模型仅需连续数值泛化就能解决，此负结果也有信息；不得将它解释成所有低频语义组合都不困难。

```

### Source: 04_TRAINING_PROTOCOL.txt

```text
训练与干预协议

A. 模型与通用设置
Qwen3-0.6B Base，读取并锁定项目实际 revision/tokenizer。不要混用 instruct 与 base，不从R05已学规则反转的终点起步；可复用代码，不复用不合适的任务状态。
主模型学习范围先采用最后一层 attention Q/K/V/O，其他权重固定。实际层号和参数量由代码输出核验，不仅引用旧记录。
该范围只是统一候选更新区，不称为已定位的基础功能。训练失败时允许一次预注册资格扩展到末层 attention+MLP；需从原起点重做所有受影响的可比条件，不能只救主方法。
AdamW：父权重lr=1e-4，adapter/router lr=1e-3，betas=(0.9,0.999)，eps=1e-8，weight_decay=0，clip_grad_norm=1。默认恒定lr，以独立倍率控制父权重，避免将全局日程混入主要比较。
FP32、TF32关闭优先。若性能必须更换精度，先做数值一致性小测试并对所有可比条件统一；记录优化器状态精度，不比较不同精度结果后归因策略。
批次32，可用梯度累积达到相同有效批次，padding和mask单元测试通过。optimizer每个后续训练臂从空状态开始；父权重完全相同。
训练和推理禁用随机dropout，记录所有随机源。梯度非零、实际权重改变量、可训练参数名单必须抽查。
独立父训练种子29、43、71；数据划分固定、父初始化来自同一base，但组成学习顺序与新增初始化独立。准确称为3个独立微调父模型，不是3个独立预训练大模型。

B. 步数与保存
父模型组成训练固定3000步；后续每条完整订单学习轨迹2000步。保存0、1、10、50、100、250、500、1000、1500、2000；父模型另存3000终点。
先用seed29训练/验证进行资格试跑。若明确未收敛：最多一轮将父模型上限提高到6000、后续提高到4000，或扩展更新范围，二者择一并说明证据；不要同时增加容量、步数、LR后无法解释。
所有最终可比臂必须按锁定版完整运行。修订前负结果保留；固定最终终点为主，不用最优验证点替换主终点。
先遍历seed29所有可执行阶段，尽早产出全流程初览；随后seed43/71完整复现，无论首种子正负都执行同样计划。不得按结果选种子。

C. 父模型与 S1/S2
P：从base出发，在S1与S2全部单项上均衡训练，得到组成已学父模型。
B：未进行该轮单项训练的base模型。
C：等步数、等格式、近似等词表长度的复制/字段提取任务训练父模型，不教算术组合。输入含同样数字字段，目标为明确指定的原字段。比较前报告答案长度和任务难度差异。
C不是完美的“除组成知识外完全相同”对照；P>C可能同时包括算术熟练效应，不能单独证明内部复用。
父阶段先评价base零样本，若单项已达资格，可仍做预定P训练但要指出不能声称是本轮新学会；若组合起点也接近满分，保留该结果，主学习缺口不足，不暗中换难题追求差距。
资格不通过先完成允许的修订，再判断该任务是否可用于后续机制结论。不得只筛出少数模型恰好答对的题来制造“单项全会”。

D. S3 组合迁移
P、B、C均用同一种J策略学习均衡完整订单，比较固定终点、早期曲线和测试泛化。
J定义见下；不同父模型更新范围、adapter结构、组合与回放序列相同。
P-J-均衡轨迹与S4、S5复用，不重复训练。总预训练投入不同必须明示，比较的是已有组成学习的帮助，不是端到端同算力优势。

E. S4 更新安排
新增路径：在最后一层attention输出、进入原残差相加之前加入 bottleneck adapter：r(h)=B GELU(Ah)，A随机初始化，B=0，瓶颈32。实际h维度由模型核实。不得重复加入原attention输出；插入当下预测应与父模型一致。
所有可比adapter从相同初值出发。
U：不加adapter，只更新原指定父权重，lr=1e-4。
J：加adapter，父权重lr=1e-4，adapter lr=1e-3。
S：同J结构，父权重lr=1e-5，adapter lr=1e-3。
F：同J结构，父模型全冻结，仅adapter lr=1e-3。
G：同J结构，父权重lr=1e-5，adapter lr=1e-4（整体减速对照）。
Z：父模型不更新不加路径，只评价。
J/S/F为同结构、不同父更新倍率的主要比较；U为普通学习参照，总容量不同；G检验是否整体慢一点即可。
不要把lr倍率直接当成实际权重位移倍率。记录各参数组候选/实际step norm及累计/净变化，检查Adam与裁剪。F应无父权重变化。
无回放敏感性仅运行J/S/F均衡条件，沿用03规定，不开启第二套新题曝光预算。
本轮不继续搜索top16；若做谱观察，仅辅助，不作为C已定位证据。

F. S5 频率
对P父模型的J/S/F分别运行不均衡与交换分布，均衡结果复用S4。其他任务家族、基础回放、训练步数和总预算一致。
主效应：同一个(d,T)组合在高/低曝光的差；交互：S相对J或F相对J的收益在低/高曝光是否不同。
分层报告金额区间、是否包邮与边界距离，不将一条平均曲线解释为所有内容都学得更好。

G. S6 分支分化与选择器
本阶段默认从同一个合格P父模型开始，父模型固定，以免同时改变共同学习和分支分工。S4若表明固定很差，仍可以做本阶段，但结论限于此设置；不得根据测试临时选择最优父倍率。若要改为S倍率，整套S6另登记修订。
分组默认四类完整订单BASE/DISCOUNT/SHIPPING/BOTH；这是语义标签分组参照，不证明发现了真正功能类别。
旧单项回放的分支映射固定：S1→BASE，S2a→DISCOUNT，S2b/c/d→SHIPPING。公开这一监督优势，所有 oracle 分组结论均注明。
必须比较：
R1 shared32：一个共享瓶颈32 adapter，直接复用F均衡轨迹。
R2 private4x32：4个瓶颈32 adapter，已知任务类型hard选1，单次活跃adapter容量与R1近似相同，但总参数约4倍。
R3 shared128：一个共享瓶颈128 adapter，总参数与R2接近，但每次计算更多。
R4 private4x8：4个瓶颈8 adapter，总参数与R1接近，每次活跃容量更少。
R5 random4x32：同R2，但由固定数据ID哈希分配，尽量平衡训练负载，划分不依赖答案；测试使用同一规则。哈希是诊断参照，不是可用自然语言router。
精确报告bias/router参数，不能把“近似匹配”写成完全等参；给出总参数与活跃FLOPs两个比较面。
不同分支接收的数据天然不同，这是干预，不要通过给每个专家额外完整数据补齐而暗中增加总监督。

G.1 learned router 原型 子阶段必须有记录
复用R2已训练的同一套分支并冻结它们，只训练一个读取真实输入hidden state的4路MLP router，不给外部任务标签、正确答案、正确中间值或未来生成token。
输入取答案生成前最后一个提示token在分支前的hidden state；同一提示产生固定权重，生成各答案token时沿用。记录因果mask与取值位置。
默认router为hidden→64→4，输出softmax，用最终答案NLL训练2000步。训练时四分支软组合都计算，明确不具备top1训练计算优势。
评价同时给soft组合与hard top1部署表现。soft学得好但hard失败，不能说稀疏MoE成立。
固定分支、同一输入比较：learned、oracle任务标签、均匀权重、固定单分支、负载匹配随机/打乱路由。检查准确率、CE、分支负载、任务-分支交叉表、对路由打乱的性能敏感性。
oracle不是理论上界：其分组未必最优。不能以利用全部分支的soft结果超过oracle就宣称发现最佳分工。
若既有项目有经过审计的hard router实现，可在结果前登记替代，但必须保留matched对照，不能仅报告利用标签训练的分类准确率。
这回答“已有分支能否被输入有效选择”，不证明联合训练完整MoE更好。本轮不再扩大联合router+专家搜索或自然文本预训练。

H. 功能复用诊断 不人为指定模块
必须完成行为与输入级诊断：
1. 同一基础订单只改门槛/折扣，检查输出是否按规则切换。
2. 两个不同p,q但基础金额相同，检查后续规则是否一致；同时记录格式/数字差异。
3. 给真实中间值作为额外信息正对照；给等格式错误中间值或交换样本中间值作为诊断。它们改变输入信息，不能直接证明原模型内部中介。
4. 将训练后的adapter关闭或按0/0.5/1缩放，检查单项与组合行为。关闭回到父模型是结构事实，不是自动定位旧知识。

定向激活干预：在专用诊断集选择一个候选位置/方向，然后锁定测试。候选可来自原始hidden的受控配对差，不要求新训练SAE/CrossCoder。
固定后续规则，交换对应不同中间金额的候选激活；预测应转向“替换金额经过原规则”的答案。设置相同中间金额替换、不相关位置、同范数随机替换。
不能只因准确率下降就声称必要性；不能只因probe能解码b就声称模型用b。完整hidden替换可能同时搬运规则和词面，需明确这个竞争解释。
若找不到满足特异性、独立集复核的候选，仍完成本阶段并写“内部复用未定位”；不制造功能标签，不无限找方向。
最多考察预注册3个层位置，每个最多2种候选，诊断集选择一次、测试一次。没有经过资格的候选，不进入“已确认功能方向”分析。

I. 旧符号组合辅助证据
完整保留legacy原包，但不执行其旧prompt里的重复权限询问或额外新会话要求。按原数据定义生成32符号、4个F、4个G的置换组合与频率交换。
必须完成原资格、迁移、均衡/不均衡/交换，以及固定/正常新增学习对照；另加入本轮S小步更新臂。3个种子按相同规则执行，若已有一致配置的完整结果可直接复核复用。
不要求在符号任务上再复制一整套S6；它是辅助，而非第二套全面MoE搜索。
对照订单报告：同向/反向/不可比较/资格不足。符号单项没学会时不能作为反对订单组合假设的证据。
不得把符号结果称为自然语言feature证据，不得合并两任务准确率或p值制造总胜利。

```

### Source: 05_EXECUTION_AND_AUDIT.txt

```text
自动执行与验收协议

1. 规则、权限与资源
从用户已授权的现有环境读取规则，不自行创建额外Work/Codex会话或新硬件池。最多使用4张H100 reserved；不覆盖、终止或抢占无关用户作业。
如果指定池有其他正在运行的工作，排队和监控，不把“4卡可用”当作已核实事实。不可用时说明，不替换付费或更大模型资源。
没有固定时间限制不等于允许无限训练。按照本包固定矩阵运行，超出修订规则的新实验需要新的研究决定。

2. 执行顺序
E0 规则/从属/命名/memory、代码与数据审计。
E1 CPU判题器测试、样例核对、真实tokenizer/生成与mask检查、base零样本。
E2 seed29父模型P/C，S1/S2资格及一次允许修订。
E3 seed29订单S3–S6及机制诊断，优先完成跨阶段初览；可独立的任务在空闲卡并行。
E4 其余两个父种子按相同协议完整复现；符号辅助任务在独立空闲卡运行。
E5 全部轨迹重聚合、固定终点评价复核、解释与证据包。
不得因为先跑的某个方法不优就不跑对应其他种子；不得为了尽快完工只保留一个最有利种子。
先估算每条轨迹耗时和总规模，写入run_plan，随后边跑边更新实际耗时。不保证明早必跑完；每个阶段完成即更新阅读包。

3. 具体训练清单及去重
订单每个父种子：
- P、C父训练各1条（base B无父训练）。
- S3 P/B/C的J均衡各1条，P-J被后续复用。
- S4 U、S、F、G均衡各1条，J已存在。
- S5 J/S/F的不均衡与交换各1条，共6条。
- 无回放敏感性J/S/F均衡共3条。
- S6 R2/R3/R4/R5均衡共4条，R1复用F。
- 固定R2分支训练router1条。
合计每种子23条训练（2父+21后续），3种子69条；资格门槛不成立时按第4节降级，不假装69条都已跑。所有只读评价、函数诊断另外登记但不计训练轨迹。
符号任务沿legacy矩阵，P/B/C均衡迁移与J/F/S×3频率有交集；正式运行清单须明确逐项去重、父检查点与精确数量，不能复制旧包里的33条后又盲加重复臂。
运行ID至少含 task_family/parent_seed/condition/frequency/replay/protocol_version，结果名不能覆盖同条件旧版本。

4. 门槛与失败处理
工程门槛：标签、泄漏、mask、起点一致性、实际更新范围未通过时，禁止把后续结果当科学证据。修复后对受影响轨迹从合法检查点或起点重跑，明确版本。
科学资格：P在单项训练后仍未达到S1/S2门槛，可完成一次限定修订；仍失败时可以跑一条P-J组合资格轨迹，判断直接联合训练是否可行。其余依赖“已掌握”的保护/复用比较标记 NOT_APPLICABLE，并保留负结果。不要烧完全部矩阵制造无效比较。
若P单项合格但所有组合臂不合格：完整保留已规定的比较；允许一次资格修订后仍失败，S6至多执行shared32与oracle4x32的资格比较，router收益不下结论。
若oracle分支和共享模型都学不好，router可以完成前向负载与分支能力诊断，但不把失败解释为“路由不行”；监督不足的分支使router效用问题未就绪。
若base已把组合全学会，训练改进缺乏空间；保留起点事实，进行预注册的频率/保持诊断，不临时上调难度制造正结果。
所有被阻塞的阶段仍须有完整原因、证据和下一最小动作。NOT_APPLICABLE不是“假设不成立”，FAILED不是“负结果”。

5. 修订上限
科学修订每个任务族最多1轮：从初始步数扩展或更新范围扩展中选择一个，依据训练/验证，不看正式测试。明确选择何者、为什么、影响哪些轨迹。
adapter容量修订若确有需要，可作为该唯一科学修订替代前两者，不能额外叠加。扩大为128时所有相应容量对照按比例重建，另记版本。
工程修复不算科学搜索，但每次记录具体错误和验证；同一错误反复出现不得无日志重跑。
不允许用大量LR、种子、层或方向试验后只挑胜者。

6. 更新实现审计
- 插入adapter零输出时，与父模型的logits、loss、生成逐题比对。B=0导致第一步A梯度为0是预期，不是“全部adapter没训练”；后续检查。
- F父权重hash/数值差应完全一致；J/S/G各组有实际更新且未误冻结。
- 同结构比较初始化、父状态、数据顺序一致。保存实际lr、grad/step norm、裁剪比例、Adam状态是否重置。
- 对lr为0/冻结、adapter关闭、固定权重前向等至少各做一个单元测试。
- 累计步长长度、累计平方、终点净位移分开，不能拿其中一个代替另一个。
- 如果缓存frozen前缀hidden，必须证明train/eval、token位置、mask、padding、精度与未缓存前向一致，且没有缓存后来会更新的层。

7. 统计与结论
每种子先单独显示，之后给均值与范围。3个父种子不足以精确估计总体分布，不把窄的题目bootstrap区间当作跨训练稳定性。
题目配对bootstrap按规范订单数值家族聚类；主比较J/S/F及S6指定对照提前锁定。大量辅助比较标探索，不挑显著者。
最终测试完整保存prediction、target、loss、family、condition、data_id、split、checkpoint、protocol_hash。
任何“优于”同时说明新任务资格、旧任务变化、总参数、活跃计算、曝光和置信边界。
模型内部机制未定位时写UNKNOWN，不以语义说明替代因果证据。

8. 状态管理与可复核证据
run_plan.csv列出每条计划轨迹及依赖；run_status.csv记录时间、GPU、PID/Job ID、最后心跳、step、退出码、终点检查点与失败原因。
活跃作业要监控到终态，不能只提交任务后说完成。进程退出码0也要核对实际终点步数与有效评价产物。
训练发生必须有权重/adapter保存、非空metrics与逐题结果。只生成表格、目录或空memory不算完成。
存数据/代码/协议/模型版本hash；每个结论能回到运行ID及逐题证据。
抽取至少一个方法每种子重新载入终点评价，验证聚合结果与原日志一致。重评失败先查校准，不解释差异机制。
若存储允许保留关键完整权重；否则明确父权重+增量+加载代码与依赖来源，不能只有图片。

9. 完成判定
COMPLETE：该阶段计划内必要比较已终止，结果审计通过，可给范围明确的判断。
NEGATIVE_RESULT：科学比较有效但未支持假设，也是阶段完成。
INCONCLUSIVE：比较有效但精度/区分力不足，也是可交付结果，不等于成功。
NOT_APPLICABLE：前提失败，已完成必要资格检查，有可定位依据。
RUNNING/BLOCKED/FAILED：不能写全流程完成，必须给已完成部分、剩余项与下一动作。
当全部阶段为前四类且没有活跃遗漏作业，才可宣布流程收束。外部阻塞时如实交付，不假装达到用户希望的结果。

```

### Source: 06_MORNING_READING.txt

```text
明早阅读与产物交付要求

先给一页 morning_readme
1. 截至几点：哪些完成、哪些仍跑、哪些未适用。禁止只有“整体已完成”一句话。
2. 每阶段一句话：原假设、最关键观察、目前判断、证据入口。
3. 仅列两条最重要的认识更新和一条下一步。
4. 研究者先看观察再看AI判断；不要求研究者一次读完所有阶段。

每阶段解释的固定格式
首先给三条分析路径：
A 假设与干预：原先预测什么，具体改变了哪个因素。
B 观察与对照：所有条件的结果、差值及不确定性。
C 竞争解释与更新：排除了什么、没排除什么、为什么。
然后给：
- 一个原始真实例子（输入、规则、正确金额、模型输出）。
- 这个例子如何体现主要错误，而非仅选最漂亮样本。
- 主表：逐种子、逐任务、逐频段的准确率、CE、资格。
- 不超过两张主图，配中文轴名与图注。
- 事实段落，不夹AI归因。
- 独立AI判断段落，清楚标支持/削弱/未知。
- 请研究者复述的一道问题，但不要因此中止其他运行。

建议图表
S1/S2：各单项准确率及混淆/错误类别，边界单列。
S3：按新任务曝光对齐的组合学习曲线，P/B/C全部显示；初始分数必须可见。
S4：横轴组合准确率、纵轴基础保持的散点/轨迹，以及J/S/F/G/U完整表。不要只画旧任务。
S5：同一组合交换高低频后的配对差；不同更新策略的低频收益差。无需漂亮但无关的表征图。
S6：共享/分开在总参数与活跃计算两个面上的比较；router任务-分支交叉表、负载及打乱干预。
符号任务：单独一页，与订单结论逐条比较；不混合平均分。

每个术语都用第一次出现时的中文说明
parent：已经做完基础阶段的模型起点，不等于已定位共同模块。
adapter：在原计算旁新增的可训练小分支，不等于天然特有功能。
replay：继续训练时再加入少量旧单项例子。
oracle routing：使用真实任务类型分配分支的参照，不是模型自行发现。
learned routing：根据实际输入决定使用哪些分支。
资格：达到事先设定的最低可解释表现，不是统计显著性。
CE/NLL：模型给正确答案的负对数概率，越低通常越好；与准确率分开。

交付文件 最少要求
morning_readme.md或项目规定格式
observations_cn.md
ai_interpretation_cn.md
hypothesis_update_cn.md
anchor与最终protocol、所有revision记录
project_memory（路径遵从项目规则）
run_plan.csv、run_status.csv、result_manifest.json
tables/、figures/、predictions/、logs/及权重/增量加载入口
reproduce_commands.txt、数据/代码/模型hash、audit_report

若支持HTML，可以额外生成只读折叠式阅读页，但保留项目规定的文本与证据源。不得为HTML另外开网站项目或发布服务。交互选择/反馈不自动上传。

研究者明早只需先检查五件事
1. 实际训练的是订单任务吗？题目规则和我们讨论的一致吗？
2. 单项是否真的会？组合真的存在学习缺口吗？
3. 每个对照只改变了所宣称的因素吗？还有哪些容量/数据差异？
4. 结论是否来自留出题、完整种子和固定终点？
5. Agent说的是行为有效、内部复用、还是专家必要？有没有跨级推断？

```

### Source: legacy/protocol.txt

```text
执行 Protocol 草案 v0.1｜低频组合、已有功能与新增学习
本文件是可执行设计建议，不是已在项目登记的协议。先核对规则，预注册后执行；严禁把执行前调整伪装成事先不变。

0. 本轮范围与顺序
本轮必做：历史核对、数据单元测试、组成任务资格、组合频率对照、受限新增学习对照、有限功能诊断、结果解释。
本轮不做：8B 扩展、新训 SAE/CrossCoder、完整 MoE 架构搜索、长短程研究、无上限调参。
允许后续预备：共享/分开学习对照的规格，不要求本轮就训练整个 MoE。
科学门槛失败不等于停止交付：完成所有可解释且不依赖失效前提的检查；其余标记“因何未执行”，不能为了全流程而生产无解释力结果。

1. 开始前查证
读取项目根与目标目录 AGENTS.md、最新 formulate/protocol、sink 分类、资源规则、已有 memory。
读取 A15_24、A15_25、A15_11、A17_04 R02/R05 中与本问题直接相关的内容，尤其既有 B/D/E 的共享/分支结果，避免重复实验。
列出“可直接复用、需修改、不能复用”：模型版本、数据生成器、评价器、统计脚本、检查点。
旧规则反转数据不能作为本轮组合问题的主要数据；可复用生成/评价框架。
核对实际硬件与授权预算，先写预计 GPU 时间、运行数、参数量。没有明确训练资源额度时，不默认为无限预算；完成 CPU 数据和现有产物审计，再集中询问一次缺失额度。
不创建额外 Work/Codex 会话或外部作业环境，除非用户另行同意。

2. 数据：最小可控组合系统
默认使用32个经 tokenizer 核对可稳定评分的符号、4个基础操作 f_i、4个后续操作 g_j。每个操作是32个符号上的固定置换。
置换用数据种子生成；检查无重复操作、非恒等、组合不过度重复、单个操作捷径不能解释大部分组合答案。保存完整表和测试。
单操作输入：“操作 F2，输入 s7”；标签 f_2(s7)。G 操作同理。
组合输入：“先 F2，再 G3，输入 s7”；标签 g_3(f_2(s7))。不显示中间答案，不改变操作含义。
这检验离散操作组合，不能直接称为自然语言语义 feature；也不要求模型内部按人类步骤计算。

2.1 划分
组成训练覆盖所有8个操作及全部32个符号。每个操作身份的曝光相同。
组合阶段每个 (i,j) 的32个输入符号固定划分20训练、6验证、6测试。划分只生成一次；同一组合-输入的重复措辞不能跨集合。
测试符号在单操作阶段出现过，但该组合-输入映射从未被组合监督。称“留出组合输入泛化”，不能称“完全未见操作对泛化”。
如果加入未见操作对外推，必须另外登记新的划分和指标，不混入主结果。
验证/测试各组合等权。所有抽样和划分存档；不靠重复模板虚增独立样本数。

2.2 频率干预
16种操作对用4×4棋盘分为8种高频、8种低频，每行每列各2种高频、2种低频。
- 均衡分布：每对相同曝光。
- 不均衡分布：高/低对曝光比8:1。
- 交换分布：保持同样不均衡程度，但高低频身份反转。
三者组合训练总监督数相同；每个 F、G 的边际出现次数相同；同一对内部训练输入均匀循环。使用确定计数批次而非只保证期望。
输出实际计数表，检查操作曝光、组合曝光、正确答案符号分布和长度。总输出符号频率若未完全匹配，明确报告并检查是否足以解释差异；不能声称所有混杂都已消除。
主因果对照：同一组合在高频与低频身份下的表现，跨组合对称汇总。均衡条件用于判断总体及尾部权衡。
组合低频自然意味着较少监督；这是被操纵因素，不要再“控制掉”它。跨方法比较必须对同一分布使用完全相同曝光。

3. 模型与父检查点
优先复用项目已核对的 Qwen3-0.6B Base tokenizer、模型版本和训练实现，不凭记忆填版本。
组成阶段建议沿用末层 Q/K/V/O 更新范围，其他参数固定；这不是认定共同功能就在这四张矩阵。
组成学习资格：每个操作的独立格式留出准确率至少95%，且操作查表评价通过。可预注册一个额外模板作格式泛化检查，但不将模板泛化冒充新知识泛化。
至少3个独立组成训练种子，建议29、43、71。若仅复用一个父模型并改变组合顺序，明确只有一个父模型，不能声称跨父模型复现。
训练步数和学习率：优先用经过核实的旧配置作起点，但先做仅使用训练/验证集的有限资格试跑；正式组合测试前锁定。禁止直接复制1200步并假定任务可学。
记录每个父模型组合零样本表现；若已接近满分，本轮没有“尚未学会的组合”空间，先报告任务失去裁决力。

4. 最小比较矩阵：分阶段，不一次爆炸
4A 迁移资格（先均衡组合分布）
P：正确组成操作预训练后的模型。
B：相同基础模型，未进行组成操作预训练。
C：等监督量、等输入格式、等答案词表，但采用另一套固定操作置换的预训练模型。
三者都按下文 U 的更新范围接受相同组合训练。C包含错误映射干扰这一额外因素，因此 P>C 不能单独证明复用；必须同时报告 P>B、起点难度和 C 的负迁移可能。
本阶段目的只是检验相关预训练是否有用；它不是内部功能定位实验。

4B 学习策略 × 频率（主实验）
使用合格 P 父模型，对三种频率分布分别比较：
U：原指定权重继续更新，无新增路径。
F：固定父模型所有权重，在指定 attention 输出位置加入零初始化输出的残差适配器，只更新适配器。
J：与 F 完全相同的新增路径，同时允许 U 的指定原权重更新。
Z：固定父模型且不加可学习路径，仅做评价，不重复训练。
F 与 J 的总结构相同，但可训练参数量不同；U 与 F 的容量不同。均如实记录，不宣称这些比较已严格等容量、等优化能力。
适配器默认瓶颈32，形式为 h + B·GELU(Ah)，B初始为0，保证插入当下输出不变。位置和输入张量必须审计，所有方法一致的路径不能重复添加残差。
若项目已有更适合且经过审计的适配器，可在正式结果前替换并写出理由；不能见负结果后不断扩大。
首轮仅一个适配器容量、一个主学习率；如容量资格失败，最多一轮事先登记的修订（如瓶颈128），与首轮独立报告，不能抹去首轮。
每个方法在同一父模型、同一频率分布下使用相同训练序列、批大小、监督次数、保存点。记录实际计算量，不把等步数写成等 FLOPs。

4C 运行规模和登记
完整设计的4A为3种父条件×3种子，共9条组合训练；4B为3种学习策略×3种频率×3种子，共27条，其中 P-U-均衡3条与4A重合，应复用。因此是33条不同的组合训练轨迹，另有组成预训练和不更新权重的诊断。此规模不是资源授权。
若预算不足，预先锁定“第一批”只做合格P的U/F/J×均衡/不均衡/交换×1个父种子，共9条，外加同种子的B/C均衡迁移参照2条；这仅是单父模型探索，不替代完整设计，也不外推跨种子稳定性。不得看了哪个方法好再选择扩展哪些种子。
在任何正式训练前，运行清单必须填齐：模型revision、父检查点hash、训练步数、学习率与日程、优化器、批大小、总监督数、保存点、实际可训练参数、精度、裁剪、种子、数据hash、GPU预算上限、主终点与主比较。未填齐不算已预注册。预算耗尽需如实交付，不承诺全部实验必能完成。

5. 指标与裁决标准
主结果必须同时报告：
- 组合测试宏平均准确率及各16种组合准确率，低/高频分开。
- 单操作能力保持：同一父模型前后每个操作的准确率和 CE。
- 学习曲线：按组合监督次数对齐，固定终点评价，不能挑最优点改主结论。
- 频率交换效应：同一操作对在高/低曝光下的配对差，报告父种子差异。
建议预注册实用标准：组合宏平均≥95%，低频组宏平均≥90%；单操作平均下降≤1个百分点且每个操作≥95%；F 相对 J 的组合宏平均下降≤2个百分点。
这些是设计阈值，不是理论常数。若验证阶段显示不适合，正式测试前一次性修订并说明，测试结果揭晓后不得改。
三种结果：达到门槛并跨父模型方向稳定；明显未达到；区间宽/资格不足而证据不足。小测试集不够排除2个百分点差异时，必须报告无法裁决，不只看点估计。
统计按父模型和配对问题分层，展示所有种子；同一符号、操作对的重复模板不可作为独立样本。置信区间不能替代实用阈值，也不能以不显著宣称等效。

6. 功能诊断：避免把“冻结”当成“复用已证实”
6A 行为边界
固定父权重仍不保证复合系统保持单操作输出，适配器同样可能改变它。必须实际评估。
保住单操作且组合答对，也不保证模型内部使用了这些单操作计算。

6B 正对照与负对照
用已经学会的单操作模型顺次调用两次，先得到 f_i(x)，再把该预测喂给 g_j。记录中间正确率及终点准确率。
再用真实中间值替换第一步预测，检查后续操作是否可处理。
上述增加了调用/信息，只是任务可组合、评价器有效的正对照，不是公平单次前向基线，不证明单次模型内部机制。
负对照：替换成另一个输入的中间值，确认输出按预定义 g_j 发生相应变化；不能仅观察随机噪声使结果变差。

6C 真实模型的初步因果诊断
先用独立诊断集定位候选层/feature，再用未参与选择的测试集验证。没有现成 SAE/CrossCoder 不新训，先用原始激活和行为检查。
优先构造匹配输入：固定后续 G，改变 F/输入，使真实中间值变化；以及改变 F/输入但真实中间值相同的配对。
候选激活替换要检查：能否选择性把答案推向“替换后的中间值经过原 G”的预期结果，而不只是降低准确率。设置同中间值替换、同层随机/等幅替换及不相关位置替换对照。
候选层选择只用诊断集；正式测试锁定。报告替换是否离开原分布、是否同时改变了其他信息、能否排除通用破坏。
若无法定位，不要编造“功能保护已成立”；可交付 H2 的行为可行性，H1 的内部复用仍未知。
本轮不以高奇异值、激活相关或线性可解码单独判定共享功能。

7. 如何回到 feature 和 MoE
第一轮只建立“语义组成要素/组合频率”的受控证据，不能直接外推到 CrossCoder feature。
若既有匹配的 CrossCoder 可用：固定它并记录训练版本、层、阈值、重构质量。比较组成操作与组合条件下的激活、配对输入的关系，并做独立集复现。未经验证的编码器差异仅探索。
下一轮共享/分开学习设计：相同保留路径下，共享一个新增分支 vs 按已知组合类别选择多个分支；必须有等总参数、等激活计算、随机分组和不分组对照，无法同时匹配则分别做预算线。
已知类别路由是可行性参照，不是 learned gating。不能通过“旧模式关闭新增分支”就宣称共同功能已找到。
只有组合/复用资格有依据，再检验特征关系能否预测分支分工；不要现在自动展开路由搜索。

8. 交付与解释顺序
先给三条路径：①组成与组合频率如何独立控制；②已有能力与新增学习如何比较；③怎样检查复用、哪些只是行为证据。
随后按 H1/H2/H3 逐条给出：实验改了什么→完整数值→对照差异→可靠性→支持/削弱/未知→下一决策。
观察与 AI 判断分开两个文件，用户可先读观察；执行过程中不需要因等待阅读而暂停全部工作。
所有术语第一次出现用中文解释；至少一个真实输入逐步展示正确中间值、最终标签、模型答案及干预答案。
输出模型/数据/代码版本、参数范围、随机种子、训练预算、各组实际计数、运行状态、失败原因、全部主表、图、原始逐题结果和命令。
最后最多两条认识更新，不将“已运行”当作“假设成立”。

```

## Runtime Binding Appendix / 运行身份追加记录

Appended 2026-10-24T16:09:43.995743+00:00, after the scientific body was frozen. This is provenance, not a change to scientific choices. The registered scientific-body hash `50517762ebf4be79d5f029f4e0234930ef529b72a7ffae1f30fa91f54cc2ddf3` refers to the immutable [pre-append snapshot](../../../../../../../../UNAVAILABLE.md), not to this now-longer file. The [execution freeze](../../../../../../../../UNAVAILABLE.md) binds actual code/config/data/model identities. [Runtime/job binding](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_26_low_frequency_compositional_reuse/20261024_order_v2/sources/runtime_binding_20261024.json) and [Detailed](detailed.md) record receipt identities and current limits. Full scientific results remain RUNNING; submission acceptance and smoke PASS do not establish six-stage completion.
