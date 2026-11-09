from common import *
import shutil
cfg=json.load(open(R/'config.json'));C.mkdir(parents=True,exist_ok=True)
P=SYS/'Projects/from-attention-to-search/main';A=P/'problem_anchors/15_spectral_representation_and_functional_routing/15_27_natural_language_feature_response/subanchors/15_27_10_near_far_fact_use'
A.mkdir(exist_ok=True);F=P/'focus/focus_near_far_object_fact_use.md'
stamp=now()
anchor=r'''# Object-fact use at near and far context distances

## 1. Problem Definition
The researcher ultimately wants to study SAE member coactivation, strength and combinations when models use context at different distances. The present prerequisite is behavioral: with the local question unchanged, does frozen Qwen3-0.6B Base select the correct object in BOTH fact versions A and B, at each registered distance? A response at a fixed token is not evidence of correct fact use. This one round measures behavior only; no SAE extraction, fitting, model training or activation intervention is authorized. The researcher explicitly requested execution and review before any next step. The next decision is whether a tested distant condition is suitable for later feature analysis.

## 2. Physical Priors
A causal decoder can condition answer probabilities on its visible prefix. Candidate priors, familiar wording and nearest-object copying are live alternatives to target-fact use. Holding question bytes and filler inventory fixed within each fact pair permits a bounded behavioral comparison; moving a fact also changes its absolute position and its order relative to filler, so it does not isolate a universal distance mechanism.

## 3. Falsifiable Hypotheses
H_behavior: changing only the target fact's object changes the preferred answer correctly in both directions, including at a predeclared farther distance. A prior-only preference cannot satisfy both members of a paired switch. Near-foil failure can still reveal a nearest-copy shortcut; natural paraphrase failure limits the wording scope. Low paired success weakens task eligibility, not general long-context ability.

## 4. Mathematical Model
One family is a fixed container, object pair and template stratum, with paired fact versions and repeated distances. Prefix tokens have zero-based positions. Let e be the LAST token overlapping the whole object phrase in the key fact, and p the LAST prefix token before answer prediction. The gap is d = p - e - 1: neither endpoint is counted. Every token ID, offset and endpoint is saved. A multi-token object's evidence position is its last token. Each candidate is the complete leading-space object phrase followed by a period. Its score is the sum of natural-log conditional probabilities of all its tokens, conditioned on the prefix and its previous answer tokens. A family succeeds at d only if score(A)>score(B) under fact A AND score(B)>score(A) under fact B; a tie fails. Family mean correct-minus-incorrect log-score is descriptive. No candidate-length normalization is needed to compare within this panel because all predeclared within-family lengths match; same-length lexical priors remain possible.

## 5. Computational Realization
Use the existing official Base model and tokenizer, 28 layers, hidden size1024, unchanged native forward and output head. Adapt the already inspected S06 complete-sequence scorer, remove all SAE hooks, and verify against the public full forward. Synthetic English records contain one target container fact and a question without candidate names. Fixed answer-start position320 means the last prefix position is319. Main actual gaps are16,64,128. The same complete filler sentences are moved around the fact with an identical token multiset across distances. Four smoke families use two distinct template groups;24 untouched families use six other groups and24 different object pairs. Secondary fact paraphrases retain their actual near gaps16–18; deliberate wrong-object facts in another container are a separate128-gap diagnostic. No-fact baselines use an unidentified object; their slot gap is nominal, not a factual distance.

## 6. Minimal Falsification Tests
The researcher's operational threshold is80% paired correct switching on near heldout families and at least one predeclared far condition, with multiple families and object pairs. Report all24 families, family Wilson intervals and template-cluster sensitivity; no failed family is removed. A point estimate meeting80% is only the numerical gate. An interval crossing80% is reported as insufficient evidence for stable eligibility rather than promoted into a main condition. This conservative uncertainty reading is an AI operational choice under the requested evidence-insufficient branch, not a universal ability standard. Baseline preference, complete token scoring, paraphrases and the nearest-wrong-object diagnostic bound alternative explanations. Secondary success cannot rescue a failed primary.

## 7. Current Evidence
Before this run: NOT RUN. R09 measured target-token feature responses at16/32/64/96/144 gaps in240-token records, without this answer-correctness test. In its new16-gap frame only9/36 old replicated members kept direction across both endings; this forbids equating all response changes with distance decay. S06 found cat-property behavior3/8 versus dog8/8, so feature contrasts alone did not establish successful implicit identification. S09 found overlap gaps largely reproduced by fixed margins, while separate pair statistics retained residual structure; neither establishes object-fact use. These are distinct prior observations, not current behavioral results. Exact source paths and the source-reading receipt are in the linked experiment's prior_context.md. Current observations will be recorded in the Summary without making the next scientific decision.

## 8. Claim Boundary And Next Decision
Success supports conditional candidate selection for these constructed English records and this model, with their tested gaps relative to a320-token prefix. It does not establish general memory, comprehension of arbitrary relations, a SAE mechanism or router utility. Full-sequence candidate ranking is not unconstrained generation accuracy. After completing all registered behavior and controls, STOP and show raw family data to the researcher. Scientific acceptance, mechanism judgment and permission for SAE work remain Unknown. [Protocol](../../../../../experiments/A15/15_27_natural_language_feature_response/R18_20261104_near_far_behavior/protocol.md).
'''
anchorcn='''# 近处与远处物品事实的行为利用

## 1. Problem Definition
最终方向是研究不同距离的上下文如何对应SAE共同激活、强弱和组合。本轮只回答前置问题：局部提问不变、关键物品事实从A改为B时，冻结Qwen3-0.6B Base是否在近、远距离都正确切换候选？固定token处有上下文响应与行为答对是不同对象。本轮用户已授权完整行为实验，完成后共同审阅；SAE分析、训练和干预均不在范围内。

## 2. Physical Priors
答案概率可依赖可见前文。候选先验、熟悉措辞和复制最近物品词是竞争解释。配对时保持提问和填充库存一致；移动事实同时改变其绝对位置和相对填充顺序，结果不能直接识别普适距离机制。

## 3. Falsifiable Hypotheses
行为假设：只改关键事实中的物品，模型在A、B两个版本都选对，且至少一个预定远距条件保持。固定先验不能让一对都正确切换。近处错误物品诱饵或自然改写失败会收窄任务适用范围。行为未过门槛只限制当前模型／任务条件。

## 4. Mathematical Model
家族固定一个容器、两个物品和模板分层，包含事实A/B和重复距离。token位置从0开始。e为关键事实物品短语最后一个token位置，p为答案前最后一个token位置。d=p-e-1，两端都不计入；保存全部ID、字符偏移与端点。多token物品取最后token。完整候选为“前导空格＋物品短语＋句号”，总分是逐token自然对数条件概率之和。只有事实A时A分高、事实B时B分高才算成对正确切换；平分失败。每家族正确减错误的平均总分差另报。本轮所有配对候选token数相等，但词汇先验仍可能不同。

## 5. Computational Realization
复用已核实的官方Base模型和tokenizer：28层、隐藏维1024。改编S06完整序列评分，去掉SAE读取，用原生前向及输出头。英语构造记录含一个容器事实和不含候选词的提问。前缀固定320token，答案前p=319。主条件实际d=16/64/128。跨距离只搬动同一批完整无关句，token多重集合一致。4个smoke家族属于2类模板；24个未评分留出家族覆盖另外6类模板及24对物品。附加自然事实改写的近距实际16–18；近处错误物品诱饵仅在128做诊断。无确定事实基线用不明确身份的object／small object，只有名义槽位距离。

## 6. Minimal Falsification Tests
采用用户首轮操作门槛：近距留出及至少一个预定远距的成对正确切换率至少80%，并保留足够家族和物品对。全部24家族展示，给家族Wilson区间及模板聚类敏感性，不删失败。点估计达到80%只称数值门槛满足；区间跨80%则对稳定准入报告证据不足。这是针对用户“不足时保留不确定性”的AI操作细化，不是普适能力标准。先验基线、完整评分、自然改写、最近错误物品诊断共同界定竞争解释；附加结果不挽救失败主指标。

## 7. Current Evidence
本轮前向前NOT RUN。R09测的是固定目标处的feature响应：240token、16/32/64/96/144五档，没有这里的正确答案行为测试；原36个复现成员只有9个在新的16条件都保留方向，不能把全部变化称远距衰减。S06动物属性行为猫3/8、狗8/8；表征差异不能替代隐含识别成功。S09中边际频率可重现大部分重叠差，另有独立联合统计的残余结构；两者都不证明当前物品事实利用。来源在实验prior_context.md。本轮事实由Summary保存，下一科学决定仍待研究者。

## 8. Claim Boundary And Next Decision
通过只支持当前英语构造任务、固定模型及320token前缀中的指定距离条件。它不证明普遍记忆、任意关系理解、SAE机制或router收益；候选评分也不等于自由生成正确率。完成全部行为与对照后停止，展示逐家族原始数据。研究者共同决定是否进入下一步；科学接受、机制判断和SAE执行授权Unknown。
'''
(A/'anchor.md').write_text(anchor);(A/'anchor_cn.md').write_text(anchorcn)
# Single owning Anchor; experiment entry is a symlink, not an independently editable duplicate.
for name in ['anchor.md','anchor_cn.md']:
    p=C/name
    if not p.exists():p.symlink_to(A/name)
focus=f'''# 1104-长短程依赖分析：物品事实行为关卡

problem_key: `1104-长短程依赖分析`
anchor_id: `15_27_10` (operational navigation identifier)
task_state: `AUTHORIZED_BEHAVIOR_EXECUTION`
question_state: `USER_ACTIVATED`
design_state: `USER_SCOPE_WITH_FROZEN_IMPLEMENTATION`
result_state: `NOT_RUN`
scientific_acceptance: `Unknown`
next_decision: researcher jointly reviews raw behavior before deciding whether to enter SAE analysis

The current user explicitly supplies the question, three planned distances, paired candidate scoring, controls,80%operational threshold and stop. This Focus formalizes that same bounded meaning; no inherited chat permission is used. Three steps: freeze paired English records and scoring; smoke then all heldout behavior/controls; show all family data, uncertainty and eligibility and stop. Supporting evidence makes a tested far condition discussable for later feature analysis; inadequate near performance asks for a task/scoring audit; far weakness or borderline uncertainty leaves far eligibility insufficient. No automatic template search, training, intervention or SAE extraction follows.

[Anchor]({A/'anchor.md'}) · [Protocol]({C/'protocol.md'}). Summary will be written at {C/'summary.md'} after scoring.
'''
F.write_text(focus)
(F.with_name(F.stem+'_cn.md')).write_text(f'''# 1104-长短程依赖分析：行为关卡

问题标识：1104-长短程依赖分析；导航编号15_27_10。用户本轮明确激活并授权：冻结成对文本与评分→smoke后运行全部留出行为／对照→展示完整数据和区间后停止。通过只让对应远距条件成为后续讨论对象；近距不足先查任务和评分；远距弱或边界不清保留证据不足。无自动改模板、训练、干预或SAE分析。四独立状态及英文主记录见[Focus]({F.name})；科学接受／下一步授权Unknown。
''')
protocol=f'''# Protocol: R18 near/far object-fact behavior

## 0. Approval Snapshot
Document: APPROVED_FOR_BOUNDED_LOCAL_BEHAVIOR. Registered at {stamp}. Scope approval: direct current user request, including implementation, smoke, full inference, controls, figure and raw delivery, then STOP. [Focus]({F}) and [Anchor]({A/'anchor.md'}) carry the user-activated question. A–G scientific/data/model/metric/numerics/artifact/boundary checks: PASS under this same authorization; self-audit, not independent review or scientific acceptance. Role: operationalization of behavioral eligibility before SAE research. No training, feature analysis or intervention. Selected engineering settings below implement the delegated task; they are not independently researcher-confirmed mechanism judgments.

## 1. Terminology / Definitions
Family = one container/object pair/template instantiation. Versions and distances are repeated within a family. Six heldout template strata each contain4families. Zero-based evidence e is the last tokenizer token overlapping the whole item phrase; p=319 is the last prefix token. Gap d=p-e-1 excludes BOTH endpoints. Answer begins at token index320. Main actual gaps16/64/128. Natural paraphrase near gaps16/17/18 are kept with each row. Baseline has no identifiable factual item and only a nominal slot gap. “Far” is relative to this task's16gap, never a universal threshold.

## 2. Anchor Alignment
Question: can facts in the visible prefix control paired candidate choice at a fixed local question? This behavior is prerequisite evidence, separate from fixed-token feature sensitivity in R09. The sole next decision belongs to the researcher after raw delivery.

## 3. Tested Hypothesis
Both fact directions induce the correct candidate ordering on at least80%of heldout families at near and at least one predeclared far distance. Primary population is the24constructed families, not natural language or all possible templates.

## 4. Rival Explanations
One-candidate prior is checked using paired A/B and neutral unidentified-item baselines. Answer leakage is prohibited in main questions/filler; whole-word item matching and complete tokenizer offsets protect against substring matches. Nearest-object copying is diagnosed with a wrong candidate in a separate other-container fact near the question,128gap only. A/B in this lure condition also changes the opposing foil, so it is diagnostic and is not a clean single-fact treatment. Natural fact paraphrases test wording scope. Absolute fact position and order relative to filler co-vary with distance and remain inseparable in this manipulation.

## 5. Data Construction And Provenance
Frozen file: {R/'data/panel.jsonl'}; SHA256 {cfg['panel_sha256']}. Family metadata: {R/'data/families.json'};24heldout+4smoke families,28distinct object pairs. Main/neutral baseline have168/84prefixes; heldout paraphrase/lure have144/48; total444. English templates, full actual texts, filler inventory and all token IDs/offsets are saved. Four smoke families use two S templates; six H templates appear only in heldout. No rewrite of a smoke skeleton crosses into heldout. Objects may recur across different pairs; the exact pairs are distinct and no weight fitting occurs. Shared generic task form limits independence beyond these named templates. Candidate phrases have a leading space and final period:25pairs have2tokens per candidate,3pairs have3tokens; all pairs match within family. No difficult item is removed after responses.

## 6. Learning Task And Permitted Supervision
Frozen causal inference only. Ground truth is generated from the explicit target fact; no discovery fit, labels as input, in-context demonstrations, chat template, BOS or thinking mode. Candidate names appear only in main fact and hypothetical scored completion. No free-generation correctness claim.

## 7. Model / Architecture And Frozen Variants
Asset IDs {cfg['model_asset']} and {cfg['tokenizer_asset']}; path {MODEL}. Architecture28layers,hidden1024,context32768,vocab151936,tied embeddings. Native AutoModelForCausalLM, eval, requires_grad(False), FP32 CPU, SDPA,2threads. Current strict access passed and full file hashes are in config.json; hash before and after each stage. Inspect/reuse S06 run.py native model and complete-sequence scoring; remove SAE hooks and keep no SAE in memory. No decommon or Dense model is substituted. Runtime dependencies use existing /data/250010109/dependency_packages/hf_transformers_qwen3; no downloads.

## 8. Training Objective And Optimization
NOT_APPLICABLE. Trainable parameters0; updates0; no optimizer, SAE, fitting, PCA or representation cache. Saved data are input tokens and output scores only.

## 9. Conditions, Seeds, And Checkpoints
Random seed20261104 for deterministic filler permutations and10000uncertainty resamples. Main/neutral at planned16,64,128. Paraphrase at all distances; lure128only. Prefix length320, physical scoring shape2x328with right padding, same position/mask convention. For a given family/mode, all distances have exactly the same token multiset and unchanged filler sentence inventory/order, with only the target fact's insertion point moving. Prefix length is fixed across all families/modes, but filler inventories can differ across families/modes. Candidate lengths are equal within pair. Config and scripts are frozen before smoke; no selection or tuning after smoke.

## 10. Primary Metric And Frozen Analysis Plan
For each candidate sum EVERY token log probability, including period, with teacher forcing of its own preceding candidate tokens. Preserve per-token values, token count, total, mean and item-only total. Correctness requires a strictly higher score; ties fail. For each family-distance pair, success=correct(A) AND correct(B), never simple change of choice. Primary switch rate=mean of these binary family outcomes. Also report family-mean accuracy and family-mean correct-minus-wrong margin (nat). Use95%Wilson family intervals for binary switch,10000paired-family bootstrap for mean margins and paired changes; use template-cluster bootstrap sensitivity with six heldout templates. Distances are paired, not independent. No multiple hypothesis significance claims; all three planned points reported, no best-distance search beyond this fixed set.

## 11. Secondary Metrics And Guards
Report raw accuracy A/B, candidate-only preferences under no identifiable fact, A/B preference delta, item-only/mean-score sensitivity, multi-token pair results, per-template results and every family. Baseline-centered margins are descriptive, never replacement primary scoring. The local-question suffix is byte-identical between A/B and across distances for each main family. Leakage guard treats an explicit foil as intentional only in lure. Keep no missing or failed condition silently; a technical failure blocks affected row, not a new template search.

## 12. Known Good / Known Bad / Known Confusing Cases
Ground truth in explicit fact pairs is directly readable; a neutral object has no identifiable A/B truth. The same candidates with different lexical priors can be confusing despite equal lengths. Implementation checks compare separate public full-forward token probabilities, candidate-prefix lane equality and prefix-only causal equality (tolerances2e-5for logprob,1e-5for hidden state). A separate toy-car/toy-truck multi-token calibration fixture verifies chain scoring without opening heldout behavioral results. Smoke is an implementation gate, not a model-accuracy filter.

## 13. Scientific Procedure And Stage Contracts
1. Prepare all444rows before inference: full tokenization, true endpoints, pair invariance, multiset, leakage and split checks. Failure stops construction and preserves development history.
2. Freeze Anchor/Protocol/config/data/scripts by hash. Score only4smoke families36prefixes; independently verify public-forward scores and causal position. Smoke behavior cannot modify templates. Failures preserve logs and permit only implementation fixes with amendments.
3. With implementation PASS, score the remaining408prefixes unchanged. CPU2threads,each stage<3600s; no remote job or GPU allocation. Report observed speed and stop if ceiling reached; no automatic costly escalation.
4. Aggregate by family, write all scores/pairs/uncertainty, show success and failure cases according to fixed rule below, plot, verify and stop. No dependent SAE execution.

## 14. Algorithm, Output, And Provenance Contract
Scripts and config live at {R}; text copies and canonical records at {C}; sole Anchor at {A}. Raw tokenized panel/JSONL outputs remain execution-side. Save immutable freeze receipt, input strict check, code/input hashes, stage timing and explicit no-update evidence. Display first heldout family with paired success at128, and first heldout family with a failed pair at128 (then64then16 if absent); if no failure, say none, without inventing one. Each selected case includes FULL A/B input, evidence/target IDs, per-token candidate scores and margins. Also show one lure failure if it exists. Full complete casebook covers all pairs.

## 15. Success / Failure / Insufficient Evidence
User numerical gate: paired switch>=.80 at near; a predeclared far condition additionally>=.80 with diverse families/pairs before becoming a candidate for main feature analysis. Sample/coverage fixed24families,24pairs,6templates, with the actual counts always shown. Numerical pass and evidential sufficiency are reported separately. AI conservative operationalization of “near threshold/evidence insufficient”: if a95%Wilson interval includes .80, mark stable eligibility INSUFFICIENT even if point gate passes. If upper bound<.80, current-task gate NOT_PASSED; if lower bound>.80 and coverage remains complete, evidence clears this bounded behavior gate. Equality at boundary is insufficient. No universal standard is claimed. Weak natural paraphrase/lure limits the usable task variant even if main passes. No template repair to chase threshold.

## 16. What This Cannot Claim
No general memory/understanding verdict; no isolated distance mechanism; no semantic/causal feature role; no permission for SAE, training, intervention, router work or scientific closure. Candidate ranking does not test unrestricted answer generation.

## 17. Block Confirmation, Freeze, And Amendment Ledger
Researcher directly authorized the same question, requested controls,80%point threshold and complete bounded execution in the current message. All routine numerical choices implement that request; scientific acceptance remainsUnknown. Self-audit A purpose/rival, B data/split, C frozen model, D metric, E numerics, F artifacts, G scope: PASS before first inference. Record freeze.json with timestamp and exact hashes. Preserve original scientific Protocol body after this point. Any later change appends amendment with UTC,before/after,reason,visible results,affected rows,authorization and eligibility. The earlier construction bug matched “cord” inside “According”; corrected to whole-word offset matching before any panel save/freeze/forward; old prepare.py retained in versions. No data deletion or response selection occurred.
'''
(C/'protocol.md').write_text(protocol)
cn=f'''# 协议：R18近远物品事实行为

冻结时间{stamp}。用户本轮直接授权完整行为实验；执行后停止。科学接受、下一步SAE授权Unknown。英文[Protocol](protocol.md)为完整精确合同；问题和模型见[Anchor](anchor_cn.md)。

英语、28家族（4smoke／24留出）、不同物品对28个，留出六类模板各4家族。主条件168条、无确定物品事实基线84条、留出自然改写144条、留出近处错误物品诱饵48条，共444条前缀。所有前缀320token，答案前p=319；主条件d=16/64/128，d=p-e-1，两端都不包含。e取物品短语最后token。自然改写的近距实际16–18，如实分列。基线没有确定答案，只有名义槽位距离。

同一家族／模式跨距离移动同一批完整无关句，词元多重集合不变。主条件A/B除了关键物品外完全相同，局部提问不含选项。诱饵属于单独诊断：另一容器近处放相反候选；事实A/B同时交换诱饵，不能当作纯单事实干预。不同模式之间的填充库存可能不同，不能把模式差全部归于某一因素。

复用Qwen3-0.6B官方Base与原tokenizer，FP32、CPU2线程、SDPA、固定2×328评分形状。改编已检查的S06原生前向及完整候选评分，移除全部SAE hook。候选是“前导空格＋物品短语＋句号”，每个token分别条件评分，总分求和。所有28对长度匹配：25对各2token、3对各3token；不把长度相等解释为无词先验。逐token／总分／均分／去句号分数均保留。无训练、优化器、权重更新、SAE读取或激活干预。

只有同家族同距离的A事实答A、B事实答B，才算成对正确切换。平分失败。准确率和正确减错误总分差另报。家族为统计单位，跨距离配对。切换率给95%Wilson家族区间；分数差用10000次家族重采样；另给六模板聚类敏感性。全部数据保留，不按结果剔除。

用户数值门槛为近距80%及至少一个预定远距80%。24家族／24物品对／6模板的实际覆盖完整展示。数值门槛与证据充分性分开：区间跨80%时按用户接近门槛的分支报告证据不足；上界低于80%时当前任务未通过；下界高于80%且覆盖完整时通过本轮行为关卡。这是AI对不确定性分支的保守操作细化。附加对照不挽救失败主指标，也不自动授权SAE。

先冻结全部文本、代码和合同，再跑36条smoke。smoke只裁决token／位置／完整评分实现，不能据正确率反复改模板。与公开完整前向逐token核对，logprob容差2e-5；因果前缀／候选两lane隐状态差<1e-5；另用不属于留出观察的toy car／toy truck校验多token。通过后跑408条留出。每阶段CPU壁钟上限3600秒。输出数据、图、完整案例与审计后停止。

案例规则：先取128首个成功家族和首个失败家族；若128无失败依次查64／16；仍无则明确没有。另报首个诱饵失败。完整casebook保留全部家族。原始数据／代码／配置在{R}；正式记录在{C}。

所有更改须追加UTC、旧新值、原因、当时结果可见性、影响范围、授权和资格。前向前构造曾把cord误匹配到According内，已按完整词边界修正并保留旧脚本，未看任何响应、未改统计或删除样本。冻结后正文不重写。
'''
(C/'protocol_cn.md').write_text(cn)
prior=f'''# Prior context and reuse audit

Read current project rules, PROJECTS,roadmap, owning15_27Anchor/Focus, R09Summary and distanceSummary, S06/S09Summary, repository conversation memories and all three directly referenced live chats through read_thread (not inferred from titles). Their scientific authority stays with owners.

- Fixed-token context sensitivity: holding target token constant while changing prefix can change its feature activation; it does not imply correct downstream answer or causal necessity. R04objects_and_settings_cn.md and15_27Anchor operationalize this distinction. The1102senior/advisor transcript and1102post-meeting communication were consulted; the exact phrase “context-sensitive feature” was not found in these bounded extracts, so this report does not attribute an unverified verbatim definition to the senior. Original wording remainsUnknown; project operational definition is used explicitly.
- R09 distance: {P/'experiments/A15/15_27_natural_language_feature_response/R09_domain_difference_decomposition_20261029/summary_cn.md'}; raw distance owner {R.parents[1]/'20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/distance/summary_cn.md'}. Its old gap was endpoint-index difference; this round's gap excludes both endpoints, so nominal numbers differ by one for identical indices.
- Recent composition: S06semantic hierarchy and S09marginal-vs-joint, at /data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/. S06property animal behavior and S09margin-control findings are bounded prior evidence; neither substitutes for current fact-use behavior.
- Senior source: /root/.codex/attachments/3decf081-ede6-4063-907d-1df5805a2e20/1102-会后沟通.md and /data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/evidence/advisor_meeting_extracted.txt (red unconfirmed spans remain unconfirmed).
- Memory: .research/memory/conversations/1102-feature组合与自然语言关系四路线初步实验/memory.md;1104-sae特征组合与语义层级/memory.md. No other conversation log changed.
- REUSE: exact model/tokenizer, S06native CPU forward and chain-rule candidate scoring. ADAPT: fixed320prefix,2x328shape, whole-item offset matching and two-candidate behavior. NOT_REUSED: SAE hooks/dictionaries, probes, intervention logic, decommon/Dense training code. Existing HF dependency mount verified4.53.3; torch2.3.0a0. No new installation or download.
- Navigation check:149entrypoints, pre-existing unrelated untracked diffusion entry and stale15_27_05derived-map explanation; direct owner sources readable. No claim of a globally clean workspace.
'''
(C/'prior_context.md').write_text(prior)
(C/'dataset_guide.md').write_text(f'''# Dataset guide

Constructed English container/object records, not a sampled external corpus. [Protocol](protocol.md) owns definitions and freeze. Actual text+token IDs+offsets+candidate sequences: {R/'data/panel.jsonl'}; family/split/templates: {R/'data/families.json'}; complete grammar/filler inventory: {R/'data/templates.json'}. Panel SHA256={cfg['panel_sha256']}. Keep all444prefixes, including failures. No-fact baseline has no gold label. Deliberate lure is separately marked. Input weights and any pre-existing dataset are not copied into this panel. Asset IDs only for model/tokenizer in config. A/B and distances are repeated within family; heldout template groups are absent from smoke; no train/test fit occurs.
''')
(C/'dataset_guide_cn.md').write_text('''# 数据说明

本轮是英语容器—物品构造文本，不冒充自然语料采样。完整原文、token ID／偏移、候选序列、家族／模板划分、填充库存和哈希见[数据索引](dataset_guide.md)。保留444条全部前缀；无确定事实基线无正确标签；近处错误物品诱饵单列。A/B与不同距离为同家族重复条件，不是独立样本。留出模板不进入smoke，无任何训练或挑选。
''')
M=SYS/'.research/memory/conversations/1104-长短程依赖分析/memory.md';M.parent.mkdir(parents=True,exist_ok=True)
assert not M.exists()
M.write_text(f'''# Conversation Memory: 长短程依赖分析

Conversation name: 1104-长短程依赖分析
Conversation ID: 01a1a478-4f02-7d83-bd6d-128f6ac58cbe
Processed by: Codex /root (harness: Codex desktop; model: GPT-6)
Created at: {stamp}
Latest update at: {stamp}
Continues from: related1102-feature组合与自然语言关系四路线初步实验 and1104-sae特征组合与语义层级 memories; separate new conversation
Environment: repo={SYS};exec={R}

## {stamp} -- 本轮行为关卡设计与数据冻结前

- Summary: 用户明确最终方向为不同距离的SAE组合，但本轮只测冻结模型近／远物品事实行为；已读三个指定livechat及相关记忆、R09／近期组合owner。不能把固定token上下文敏感性当作行为正确。完整先验来源审计见prior_context.md；学长原句未在所读材料中查到，不编造归属。
- Current work: 已构造28家族（4smoke／24留出）、444条英语前缀；主条件真实d16/64/128，p319，前缀320。所有候选配对等token数。模型／tokenizer strict可读且全哈希核实；改编S06CPU评分，不加载SAE。尚未前向。原协议与数据即将按SHA冻结。
- Next action: 实现校验smoke→全部原定留出行为／基线／改写／诱饵→原始逐家族分数、图、Summary／Detailed→停止待共同讨论。不得根据失败反复改模板或自动启动SAE／训练／干预。
- References: {A/'anchor.md'};{C/'protocol.md'};{R/'config.json'};{R/'data/panel.jsonl'};{C/'prior_context.md'}.
''')
# Frozen originals are copied as execution evidence, not an alternative authoring owner.
for name in ['protocol.md','protocol_cn.md']:
    shutil.copy(C/name,R/name)
dump(R/'evidence/freeze.json',dict(UTC=stamp,authorization='Direct current user request',hashes={str(p):sha(p) for p in [A/'anchor.md',A/'anchor_cn.md',C/'protocol.md',C/'protocol_cn.md',R/'config.json',R/'data/panel.jsonl',R/'data/families.json',*sorted((R/'code').glob('*.py'))]}))
dump(R/'evidence/pre_run_audits.json',dict(UTC=stamp,scientific=dict(status='SELF_REVIEW_PASS',question='paired answer use, not feature sensitivity',rival='prior/nearest copying',confound='distance+absolute position+filler order'),data_statistics=dict(status='PASS',families=28,heldout_families=24,template_strata=6,split_by_template=True,exclusions=0,all_scores_unseen=True),implementation=dict(status='PENDING_SMOKE',model_weights_hashed=True,trainable_parameters=0,SAE_loaded=False),correction=dict(old_problem='cord substring in According',change='whole-word regex before tokenizer offsets',stage='pre-freeze/pre-forward',affected_rows='all construction rechecked',response_seen=False)))
print('FROZEN',stamp)
