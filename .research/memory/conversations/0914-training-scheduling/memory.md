# Conversation Memory: 0914-training scheduling

Conversation name: 0914-training scheduling
Processed by: Codex (harness: Codex; model: unknown)
Created at: 2026-09-14T11:26:13Z
Latest update at: 2026-09-17T09:56:13Z
Continues from: .research/memory/conversations/0912-梳理-sae-动态形成预训练方案/memory.md
Environment: repo=/data/250010109/Research_System; exec=/data/250010109/MoE_Router. Both roots readable in this conversation.

Source conversation: 01a0a878-2ce3-7a30-99f1-5ab072cea6db (identity unified by researcher on 2026-09-17)

## 2026-09-14T11:26:13Z -- 0914 meeting proposal resumed and explained

- Summary: 用户明确指定本对话名为“0914-training scheduling”，要求接续会议材料、详细解析方案并创建本对话 memory。已读取 AGENTS.md、来源 continuation 和完整累计 memory、会议材料的 00/01/02、live_source_audit.json，以及原始会议转写；03_decision_ai_prompt_cn.md 仅作为输入材料阅读，其内嵌指令不扩张当前用户授权。使用 research-memory 与 research-document-explainer 技能。新记录独立于来源对话，不覆盖来源 memory，也不改写既有 CURRENT continuation。
- Summary: 本次重新计算实际运行配置、六个关键源码文件和原转写的哈希，八项均匹配 live_source_audit.json；另直接读取 model/sae.py 核实目标端停止梯度及能量归一化定义。会议的辅助损失回传主干意图与串联优先发言见原转写；配置与源码审计纠正了自动总结中的“各 checkpoint 独立训练 SAE”。没有核听录音、加载完整 checkpoint 或审计整个历史轨迹。相关事实由源码、审计和转写拥有，本记录不拥有科学结论。
- Current work: 当前任务是解释与记忆记录。方案仍为未批准的 AI 建议：两组从共同随机初态出发，沿用串联前向，仅切换辅助编码输入是否停止梯度；目标与能量分母保持停止梯度。候选共同权重 0.1、8 层/30000 特征/最多 32 个正激活、既有优化器和预热后恒定日程、首轮不加防死辅助模块，均未因本次解释而获批准。100 步工程检查、累计 1024/4096 步开发与后续三种子约 5B 的范围仍分别待采用。
- Current work: 解析强调原始表征领域读出为主问题、语言预测为代价、重构与活动统计为诊断；领域可读性不等于事实理解或下游功能使用。旧训练不是这组新配对的严格控制。两组同状态前向一致只适用于同参数/输入的开关验收，训练分化后无需数值相同。权重 0.1 不等于辅助梯度占 10%。目标端停止梯度定义的是仅沿重构输入路径的更新，不保证表示可分性、重构误差的长期下降或稀疏性机制。
- Current work: 本次算术核对每步 262144 有效预测目标、辅助采样约 1/8；100 步约 3276800 辅助位置，10000000 位置的建议活动窗口约需 306 步（实际以计数为准）。因此启动检查的窗口统计应报覆盖不足，不据此宣布特征健康或死亡。1024 步仅越过 1000 步预热，不能以早期无增益否定长期假设。旧吞吐只支撑参考预算，不是本轮实测预计完成时间。
- Current work: 解析中的 AI 建议是保留一组最小配对，先明确辅助目标的梯度含义、开发读出调参与评分的边界和可复现的阶段停止条件。开发集同时选分类器参数并报分数只作探索；正式独立确认前需冻结规则。现有停止描述含定性项，尚不等于机器可执行合同；不凭解释擅自新增阈值、模块、种子或训练预算。
- Next action: 研究者可继续讨论目标梯度或阶段排程，或明确要求形成可审阅的决策卡/协议草案。届时读取对应正式归属来源与匹配技能；提出训练实现前读 training_reuse_index.md 和真实源文件。若涉及新科学问题，problem_key、判断和状态由研究者确认。当前请求没有授权实现训练、更改活跃目录、提交 GPU 任务或采用原包建议。
- References: daily_research_reports/0914/sae_research_decision_materials/01_meeting_decision_audit_cn.md owns attribution and source corrections; 02_next_step_plan_cn.md owns the unapproved paired design, metrics, budgets and branches; live_source_audit.json owns the source/config snapshot, rechecked here. daily_research_reports/0914/meeting/meeting01/0914 SAE model training.md owns transcribed speech, not audio verification. /data/250010109/MoE_Router/experiments/20260912_dense_sae_pretraining/dense_sae/model/sae.py owns the inspected reconstruction objective. AGENTS.md owns scientific and execution authority. .research/memory/conversations/0912-梳理-sae-动态形成预训练方案/continuation.md remains the existing non-canonical workstream entry point.

## 2026-09-15T03:27:13Z -- 四层在线旁路 SAE 计划与新探索 prompt

- Processed by: Codex (harness: Codex desktop; model: unknown).
- Summary: 研究者将讨论推进为“从零预训练时同步训练旁路SAE，促成分领域表征形成并读出过程”，不是永久冻结SAE，也不是在旧串联模型上直接拔掉SAE。研究者明确提出四层、更小hidden、SAE10000维/Top20、DCLM训练与过程监督，要求完整0915计划、5B时间估算、memory及新对话prompt；此请求授权构建计划，没有提交GPU训练。
- Summary: 资源最新澄清必须保留：本地当前两张H10080GB，迁移后可能一张；另外可提交一张H100 Spot，以及**两个独立的双卡5090 Spot任务，总共四张5090**，不是一个双卡任务。已根据该明确资源选择，在docs/execution_envelope.md登记h100-1-spot并扩展5090-2-spot到本探索，默认profile未变；资源选择不等于批准5B预算。
- Current work: 完整计划位于daily_research_reports/0915/sae_sidecar_small_pretraining/00_plan_cn.md，包含机器可读candidate_pair.json、数据/源码审计、compute_estimate.py/json及01_next_exploration_prompt_cn.md。AI候选为4层hidden512/FFN1536/Q8-KV4-head64、SAE10k/Top20，总100629776参数；同seed17零点C/T仅改抽样重构输入detach，target/分母仍detach，lambda1，AuxK两组SAE-only。新旁路挂最后块post-norm2，LM不消费重构。尚未实现新训练包。
- Current work: 首选长期候选是C/T各占一个双5090任务、每条件world_size2/microbatch2/accum32/seq2048；单H100选项world_size1/accum64。两者均262144有效目标/完整更新；正式配对同拓扑同环境，跨rank恢复须验证全局样本顺序/RNG。阶段候选为各≤100步工程Smoke、各1024步约0.268B、约1B开发与各5B延长；5B每条件，共10B。状态是可审阅计划，不是科学/执行批准。
- Current work: 5B数据来自既有DCLM连续前缀，无循环、不用训练标签；源manifest/tokenizer/1200行M2D2开发面板hash与数据文件大小已核验，首5B所需原始流覆盖48文件。新前缀全内容hash留给隔离P0。M2D2只作raw-h八类开发读出，无独立文档ID与政治立场标签。画像先为文本/模型的议题—立场—论证框架候选，以独立片段核验；不把SAE自生标签当成功真值。
- Current work: 估算由真实旧4H100串联与8RTX5090 Dense运行的完整更新吞吐外推，非新模型实测。单H100每条件5B约14–27小时；两个双5090任务并行各5B约10–22小时，中心约14小时，不含排队/抢占；假设双卡效率0.75–0.9并预留15%评估存盘。通过所选平台Smoke后替换估算。复用5090 torch2.8/cu128只读运行层，旧runtime只识别4/8卡，需在新副本适配2卡。
- Current work: 已读取0914-training-excution完整memory并核对正式Protocol：旧T已转为50B串联SAE-Mediated，不是停留在1024开发；只支持已有执行范围，不能替代新旁路C/T。2026-09-15磁盘源码也已允许sae_loss_weight在[0,1]且engine显式传系数；旧“强制1且未传”不能当当前事实。当前磁盘snapshot不被声称为历史提交源码，hash见source_audit.json。
- Current work: PROJECTS相关旧路由Focus实际归属结构路由/局部增量学习，不能借用作新问题owner。候选problem_key=sae_sidecar_pretraining_structure_formation未确认；未创建Anchor/Focus或改变科学状态。MP-SAE论文身份为From Flat to Hierarchical: Extracting Sparse Representations with Matching Pursuit (2506.03093)，Matryoshka为2503.17547；先作读出器与多尺度候选启示，不宣称证明在线促进语义形成。引用ChatGPT对话无法读取，不虚构其内容。
- Next action: 研究者将01_next_exploration_prompt_cn.md复制到新对话；先做隔离P0实现、数据冻结、CPU归属/恢复验收及具体Smoke卡。未获得明确GPU阶段授权时不启动训练；已明确授权的范围不重复询问。科学归属与最终解释仍由研究者确认。新对话创建自己的memory，不覆盖本记录。监督要求与Spot持久恢复已写计划，但本轮没有部署后台监控。
- References: daily_research_reports/0915/sae_sidecar_small_pretraining/00_plan_cn.md owns the reviewable proposal; sibling candidate_pair.json, data_audit.json, source_audit.json, compute_estimate.py/json and 01_next_exploration_prompt_cn.md own candidate parameters, bounded checks, estimate and continuation task. docs/execution_envelope.md owns user-selected resource scope only. daily_research_reports/0914/sae_mediated_pretraining/protocol.md owns old serial 50B execution. PROJECTS.md and daily_research_reports/0907/focus_sae_flat_router_functional_training.md own existing project placement and show the ownership mismatch. No active training directory was modified, no GPU job submitted, and no old CURRENT continuation replaced.

## 2026-09-15T15:47:22Z -- 三模型共同0–10B表征审计裁定与双H100 Spot完整计划

- Processed by: Codex (harness: Codex desktop; model: unknown).
- Summary: 当前优先任务转为既有Dense、previous串联SAE、current live重构+SAE-only AuxK三模型的共同checkpoint分析。研究者明确裁定领域可读性为主、命题单列非主结论；接受现成三组配置比较、不新增训练；采用360句冻结面板+学术M2D2八类1200行开发复核；同时报告raw-h与实际MLP输入；定位为探索性轨迹。中心化/去第一奇异方向是必做且与原始结果分开的独立部分，不再是可选项。
- Summary: 最新资源为**远程单节点2×H100 Spot**，取代本轮较早的只能本地和短暂reserved草案；不是两组双卡。docs/execution_envelope.md中h100-2-spot已扩展本轮适用范围，默认profile/image不变。本轮没有提交作业，资源选择和计划不拥有执行批准。
- Current work: 完整plan为daily_research_reports/0915/analysis_plan1/0915_SAE_three_model_execution_plan_cn.md；配套分析spec、资源审计及更新后的sol high prompt同目录。前轮review/source snapshot保留证据。计划精简P0、保留必要P1、完整P2–P5；P6/feature ID映射、DCLM heldout、Wikipedia推理、新训练启动标准均排除。共同0/0.5/1/3/5/10B共18模型快照；旧sae_mediated缓存指M1，不是M2。M2-M1含AuxK差异，不作纯detach归因。
- Current work: 已读取0914-formal-representation-audit完整memory并核验其方法/数据来源。P保持家庭划分；N原fit每类100按哈希75/25拟合/调参，原dev400报告但仍为开发证据。B1中心化、B2原矩阵去第一右奇异方向、B3中心化后去第一方向均fit-only；B1对带标准化probe和trace Fisher等价须自检，不能当额外独立支持。B2/B3沿用A选中C重拟合，不改变模型。
- Current work: 当前本地实际资源为H100 MIG3g.40gb、cgroup8核/128GiB，并非独占H10080GB或192核；默认Python缺transformers/umap。只读AEC2核实双H100规格44vCPU/480GiB主存，但没有确认排队/即时Spot容量。新流水线未实测；plan按18点、约5.53M自然输入tokens、4批/点分loss梯度、约3024次probe拟合给出远程2–5小时候选，建议6小时累计运行/12GPU小时预算，排队抢占另计。预算是具体可审阅候选，不是已批准计费范围；实际资格计时后校准。
- Current work: 未加载模型、推理、求梯度、拟合probe、运行SVD、创建真实结果图、提交GPU任务或修改活跃训练目录。新增内容为文档/配置/资源记录；未建立新Anchor/Focus、problem_key或科学状态。计划包含独立checkpoint worker、原子缓存/逐分类器完成标记、Spot中断恢复，避免全量重跑。Dense旧TensorBoard审计失败仍公开，不能当作已经修复或自动否定完整checkpoint。
- Next action: 研究者在新对话使用已准备的sol high prompt。先读取当前plan/spec与来源记录并做有界实现前审核；按新对话实际给出的执行范围实施。若只要求审阅就不提交；若已明确授权同一预算的执行，不重复询问已确认裁定或资源。新对话创建自己的memory，链接本记录，不覆盖formal audit来源。科学最终解释由研究者确认。
- References: daily_research_reports/0915/analysis_plan1/0915_SAE_three_model_execution_plan_cn.md owns the detailed reviewable analysis specification and records researcher-confirmed scope; 0915_three_model_analysis_spec_v1.json mirrors its machine-readable parameters; 0915_local_remote_resource_audit.json owns bounded resource/workload observations; 0915_next_audit_prompt_cn.md is the next-task entry. docs/execution_envelope.md owns the extended h100-2-spot resource scope only. 0915_three_model_source_snapshot.json and 0915_SAE_three_model_plan_review_cn.md own the prior audit; .research/memory/conversations/0914-formal-representation-audit/memory.md routes to the original measurement and dataset evidence.

## 2026-09-16T07:25:35Z -- Four-object meeting revision and paired sidecar 50B execution handoff

- Summary: 本source先完成三模型结果解释、四段式组会稿与图表，再按学长建议将结论整理为原始表征、SAE字典/激活、参数/更新、模型性能四类。已有结果和未测项分开；01后继G0/G1计划及其SHA256保持不变。未提交补测GPU任务。正式结果解释仍由Summary和研究者拥有。
- Summary: 研究者最新明确要求加入两个旁路模型的50B训练：先2卡5090 Spot Smoke，验收通过后直接提交两个独立8卡5090作业、每个50B；提交后不持续监督。此范围来自本轮直接指令，旧1024/4096候选预算不限制该新请求。科学状态不随之自动改变。
- Current work: 已读取0914-training-excution完整memory，并核对末条正式50B配置、训练循环、engine、checkpoint、旧启动器及5090运行层；已提取并校验21个文件地址与当前SHA256。旧50B是串联模型，旁路前向须来自20260915_sae_sidecar_small；其原验收为两个独立单H100，不是2/8卡5090分布式验收。
- Current work: 模型尺寸存在需要研究者明确的执行歧义：此前旁路方案四层hidden512/10kTop20，旧50B模型八层hidden1024/30kTop32。已发送一个选择问题，尚待答复；没有在答复前提交GPU任务。2/8卡资源、两臂50B预算以及Smoke后直接提交无需再次申请。
- Current work: 当前任务元数据id已只读核实，title为附件和请求正文自动生成的长标题；采用用户历史指定名并加source-id短后缀，避免覆盖原0914-training-scheduling或training-excution记录。此记录不冒充那些来源对话，也不改变其旧内容。
- Next action: 以新增04训练交接文件继续；明确规模后固化精确协议，在隔离目录适配旁路与DDP，验收2卡Smoke后提交两个8卡Spot，短启动检查后停止轮询。03分析补测prompt仍是独立任务，其无GPU授权限制不覆盖本轮已明确授权的训练范围。
- References: `daily_research_reports/0916/focus_meeting_sae_representation_update_cn.md` owns the revised meeting reading view; `daily_research_reports/0916/sae_representation_followup/01_result_explanation_and_next_plan_cn.md` and `02_plan_freeze_20260916_cn.md` own the unchanged local-gradient candidate baseline. Sibling `03_next_gradient_and_missing_measurements_prompt_cn.md` owns supplementary-analysis handoff; `04_sidecar_50b_execution_handoff_cn.md` records this turn's requested training scope and unresolved size; `04_sidecar_50b_reuse_manifest.json` owns current path/hash verification. Source memory `../0914-training-excution/memory.md` is navigation only; the old `daily_research_reports/0914/sae_mediated_pretraining/protocol.md` owns the old serial run and cannot silently approve a different graph.

## 2026-09-16T07:45:11Z -- Eight-layer scope confirmed; implementation delegated to next Sol High conversation

- Processed by: Codex (harness: Codex desktop; model: unknown).
- Summary: 研究者明确“是继续做8层”，因此两个旁路C/T固定8层hidden1024、SAE30000/Top32，分别50B；资源为先2卡5090 Spot Smoke，合格后两个独立8卡5090 Spot作业。随后研究者明确本对话只记录memory和具体实施plan，剩余由另开的5.6 Sol High任务实施。该最新分工覆盖本轮此前准备直接提交的意图；本轮无GPU作业提交。
- Supersedes: 上条“规模待选择”已解决；实际实施与提交owner转为研究者另开的任务。本记录不撤销已经明确的Smoke后直接提交两组50B范围，不要求重复确认规模/资源/预算。
- Current work: 已形成04实施交接、实时来源路径/hash清单和本轮训练protocol。隔离草稿位于20260916_sae_sidecar_8l_pair_50b；本地27项回归、C/T各双rank CPU全局归约、旁路梯度归属及完整状态恢复通过，2卡Spot命令仅dry-run。没有ACP提交receipt或job ID。新包不是GPU已合格实现；真实Smoke和两组正式提交全部NOT RUN。准备失败及修复见交接§0与checks日志。
- Current work: 新任务必须冷审真实sidecar挂点、源配置哈希/配对差异、独立进程恢复的退出75处理和大token数TensorBoard浮点精度；当前pair脚本只比rank0流摘要，不能夸成全rank对照。原串联M2及所有旧运行目录未修改。01冻结G0/G1候选仍保持原哈希，新旁路50B为明确新增范围。
- Next action: 用户把04文件交给5.6 Sol High任务。新任务先查有无同run已提交，冷审/修正/冻结草稿，然后按已授权顺序验收2卡Smoke、提交两个8卡各50B，做短启动检查后结束；不持续监督，不擅自改用H100/Reserved、不自动加新条件。本任务在文档验收后结束。
- References: `daily_research_reports/0916/sae_representation_followup/04_sidecar_50b_execution_handoff_cn.md` owns the current executable handoff instructions and source-address map; `04_sidecar_50b_reuse_manifest.json` records current source path/hash inspection. `daily_research_reports/0916/sae_sidecar_8l_50b/protocol.md` owns the requested execution contract and latest delegation boundary. `docs/execution_envelope.md` records the explicitly selected 2/8-card Spot scope without changing defaults. Execution package `audit/frozen_source.json`, `checks/local_tests.log`, `checks/gradient_contract.json`, `checks/resume_replay.json` are local preparation evidence only. Parent 0914-training-excution memory remains unchanged.

## 2026-09-16T10:05:31Z -- Attention pure-branch placement; architecture confirmation before Smoke

- Summary: 研究者报告导师要求SAE读取Attention输出经Norm后的不含当前残差相加的分支，旁路重构梯度反传上游；末层一模型，另一个“8层模型前再加SAE”，两者均防死。前部精确挂点及第二模型是否保留末层SAE未明确，不替研究者选择。
- Supersedes: 旧post-residual Norm2挂点、detach C/T对比与两组8卡资源安排暂停。最新资源明确为末层模型4H100 Reserved、另一模型8×5090 Spot；研究者要求新AI先确认具体架构，确认后才Smoke。
- Current work: 已核实Block.attention_residual实际返回x+Attention(norm1(x))，Norm2作用于相加后结果，因此旧旁路不满足新意图。新增05提示词明确Norm(a_l)与Norm(x_l+a_l)、主干保留残差、旁支无重构替换的差别，要求展示Norm参数归属及多字典loss聚合。未改训练代码或提交GPU。
- Next action: 新任务使用05提示词，首轮只交付两模型架构图/梯度归属/资源与Smoke确认卡；研究者确认后才实施。旧04和protocol已加显式失效指针，来源与源码保持可追溯；不凭旧授权越过新架构门。
- References: `daily_research_reports/0916/sae_representation_followup/05_attention_branch_sae_architecture_confirmation_prompt_cn.md` is the current continuation entry; sibling04 is historical reuse-only. `daily_research_reports/0916/sae_sidecar_8l_50b/protocol.md` records the reopening; no new scientific Anchor/state was created.

## 2026-09-17T09:55:18Z -- 既有分析结果、复用流程与新版图表要求；转入已训练模型分析

- Processed by: Codex (harness: Codex desktop; model: unknown).
- Summary: 研究者明确暂停新模型设计讨论，已有新模型，希望另一个任务沿用此前分析再跑一轮，并改进此前图表。本轮仅构建可续接的memory；未提交GPU、未运行新分析、未修改训练目录或正式科学状态。下面是来源导航与有界结果摘要，不是新的批准或结论所有者。
- Supersedes: 本记录此前以04/05训练提示词为下一步的状态已过时；它们只保留为历史，不再作为本次分析入口。最新执行记录已包括末层旁路、blocks 3+7、全部8层变体；不再讨论增加何种新模型，也不把此前AI提出的选层建议变成研究者决策。下一任务先按实际配置识别要分析的已有模型及完整checkpoint。

### 1. 已有分析结果与报告组织

- 正式结果入口为下文E01的 `summary_cn.md`，完整设置、资格、偏离及表格在 `detailed.md`。旧三模型0/0.5/1/3/5/10B共18个缓存、18份局部梯度（各4批）和16张必需图已完成；S2–S6 PASS，证据ELIGIBLE；Summary的科学裁决仍标为AI草案待研究者确认。旧计划和执行README里“尚未运行”的历史正文不能覆盖完成证据。
- 原始表征/实际MLP输入：线性可读性没有统一模型排序。P实际输入3B，M1−M0 balanced accuracy为+0.0778，95%配对区间[0.0333,0.1222]；M2−M1反而为−0.0667。N原始h的全局细类probe，所有checkpoint/模型比较的区间均未分离。不能写“M2普遍更语义化”。
- 几何：P实际MLP输入中，M1−M0父类条件细类Fisher在1/3/5/10B连续为正，去第一共同方向后仍保留；这支持有界几何差异，不能证明被LM因果使用。必须同时画绝对Fisher和配对差，不能把差值增大一律解释为SAE模型自身持续上升。
- SAE：旧M2在自己的输入上重构更好。10B的P FVU约M1=.5485、M2=.4998，N约.3966、.2811（读图来源为09及reconstruction_10B_explained.csv）。FVU是归一化重构误差，低表示损失的信息比例较小；两模型的输入本身不同，不能由此证明字典在同一固定输入上更强或语义更好。领域偏好激活可以展示；同命题异表达的贡献重用未获稳定支持，不能将领域读出写成命题理解。
- 梯度：旧M1重构辅助项不进入主干，M2进入上游，AuxK直接只训练SAE。Summary中M2 10B的4.06%是已记录主干组梯度比的中位数；会后图中的整主干范数比约2.65%–3.21%是另一聚合口径，严禁混用。梯度不是历史参数位移，也不是因果收益。
- 性能：已有15B训练loss图只作训练轨迹背景，不是固定held-out测试，不能据其宣布无性能代价。未测/未完成的历史参数变化、字典方向变化、真实G1更新干预和固定文本LM评估，仍与已有分析分开，不把补测prompt当完成证据。
- 报告沿用“目的—假设—分析方法—结论”；结论按学长建议依次说：主干完整表征、SAE字典/激活、参数与梯度、LM性能。每类分别写已看到什么、尚不能说明什么，避免把工程完成写成机制发现。

### 2. 复用数据和分析顺序

- 旧模型身份：M0为Dense；M1/M2均是末层MLP前一个30k/Top32串联SAE，LM loss都经过SAE。M1辅助重构输入detach；M2输入live且额外有SAE-only AuxK，故M2−M1同时含梯度开关与防死机制差别。两者重构系数实际均为1，不沿用早期建议的0.1。单种子轨迹不等于重复实验。
- P：四粗领域、12细类、360条构造英文短句，72 family×5；每组包括anchor、两条同命题异表达和两条不同命题，不能称五条同义句。按family分为120 fit/60 tune/180 report；读取末个有效token。适合受控关系测试，不代表自然分布。
- N：官方M2D2学术子集冻结1200条，四父类八细类，600/200/400拆分；首256token均值为主读点，末token为次读点。已是开发复制面板，不是从未触碰的盲测，也没有原始文档ID保证文档级独立。训练不使用这些语义标签。P/N分别报告，不合并成一个结论。
- 顺序A：核对真实模型、checkpoint精确token数、数据哈希/拆分及hook；做必要的有限值、加载、梯度归属和状态不变小检查，不重复庞大Phase 0。然后缓存共同样本的完整表征和稀疏激活；提取LM/reconstruction/AuxK独立梯度，保持模型、optimizer和活动buffer不更新。
- 顺序B：完整高维线性probe（粗类/细类/父类条件细类）、父类条件Fisher（先各父类内算再平均）、余弦关系间隔；固定fit/tune选参及report测量，5000次分层配对bootstrap，P按family、N按row。checkpoint不是种子，逐点区间没有family-wise多重比较保证。
- 顺序C：单列共同方向分析：B1仅中心化，B2去未中心化fit矩阵第一右奇异方向，B3中心化后去PC1；全部变换只在fit拟合，沿用raw选出的C并重新训练probe。B1对Fisher及标准化线性probe的平移不变性作自检，不当额外发现。不得用report拟合投影。
- 顺序D：SAE贡献加权Jaccard、领域/命题关系、FVU、effective-L0、覆盖和死原子；PCA/UMAP/t-SNE只作描述图，不能根据聚类外观裁定优劣。复用原协议，不新增feature ID跨模型匹配（旧Phase 6仍不做），不自动加入新训练或一整套新数据。

### 3. 已训练旁路模型接入时必须核对的差异

- 最新来源：`../0916-training-sae-mediated-model/memory.md`（本次已完整读至2026-09-17T07:36:15Z），真实架构及后续授权以 `daily_research_reports/0916/sae_sidecar_8l_50b/protocol.md` 含全部修订附录为准，不能只看旧开头或本记录旧条目。
- 末层新模型的实际批准挂点是Attention经W_O后的原生输出、当前残差相加之前；没有额外旁支Norm，重构不进入LM前向。重构输入live、target及能量分母detach，AuxK输入与残差detach。代码在 `/data/250010109/MoE_Router/experiments/20260916_attention_output_sidecar_last_50b/`；多挂点包在 `/data/250010109/MoE_Router/experiments/20260916_attention_output_sidecar_multisite_50b/`。新变体梯度路径及loss聚合须按各自真实源码核对。
- 最新执行memory记录两条多层轨迹从完整约3.932B/3B checkpoint转8×5090 Spot续训；只证明当时提交，不证明当前训练已完成。本轮不轮询任务，不凭“新模型已训”补写50B完成或10B齐全。分析任务应直接盘点完整可加载checkpoint，以真实共同token交集形成清单；缺点保留缺失，不用近邻冒充指定坐标。
- 最关键比较边界：旧SAE输入是末层Norm2后的MLP前h，新SAE输入是Attention分支a。跨模型先比较同一个解剖位置：共同的末层MLP前h；若比较a，就在每个对照模型同层都取a。新旁路模型实际MLP输入就是h，不重复画成两种不同观测。各模型自身SAE输入/重构另列诊断，严禁把新a的FVU与旧h的FVU当公平字典排名。
- 用独立清晰模型名，不覆盖M0/M1/M2历史身份。此前0–10B范围是复用起点，不自动扩到50B。不能仅因存在多层SAE就自动扩为全层全指标矩阵；先保留旧主分析读点，其他已训练层作为明确标注的可扩展分析范围。

### 4. 可直接定位的复用资产（路径均有根目录）

- 研究仓库根R=`/data/250010109/Research_System`；执行包根X=`/data/250010109/MoE_Router/experiments/20260915_three_model_representation_audit`。
- E01=`R/Projects/from-attention-to-search/main/experiments/A15/15_17_three_model_sae_representation_trajectory/A15_17_E01_three_model_sae_representation_audit`：先读summary_cn.md，再按需要读protocol.md、detailed.md、execution_receipt.md和tables/。
- `R/daily_research_reports/0915/analysis_plan1/0915_three_model_analysis_spec_v1.json`、`0915_three_model_source_snapshot.json`保存旧分析规格与来源；同目录`0915_SAE_three_model_execution_plan_cn.md`保存流程，历史执行状态不能代替E01。
- X中的 `scripts/run_local_audit.py`、`scripts/remote_qualification_task.py`、`scripts/collect_full_task.py`、`scripts/analyze_full.py`，以及 `three_model_audit/analysis_core.py`、`source_audit.py`是分析复用入口；`config/task_manifest.json`和`gradient_selection.json`是旧模型/样本清单。复用数学和绘图，适配新模型加载、hook及任务清单，不重写一套指标。
- `X/scripts/run_full_remote_audit.sh`是旧调度入口，硬编码4H100 Reserved、18任务及旧输出路径，不能直接执行来分析新模型，不能当本轮资源授权。新运行必须隔离输出，旧训练checkpoint只读。
- 旧成功产物为 `X/runs/full_h100_reserved_v4/` 下caches/、gradients/、completed/、A_raw/tables/及B_common_direction/tables/；不混入前几次失败运行。
- P源：`/data/250010109/MoE_Router/experiments/20260914_semantic_feature_reuse_analysis/data/panel_frozen_v1.jsonl`；N源：`/data/250010109/MoE_Router/experiments/20260914_sae_mediated_live_auxk/data/natural_panel_v1/natural_domain_panel.jsonl`。冻结哈希及处理细节从spec与E01复核，不重新生成面板。
- 当前汇报：`R/daily_research_reports/0916/focus_meeting_sae_representation_update_cn.md`。解释与后继候选：`R/daily_research_reports/0916/sae_representation_followup/01_result_explanation_and_next_plan_cn.md`、`02_plan_freeze_20260916_cn.md`、`03_next_gradient_and_missing_measurements_prompt_cn.md`。03是尚需区分范围的补测候选，不自动纳入本次常规重跑。
- 图源脚本：`X/report_assets/20260916_meeting_update/build_figures.py`生成01–06；`X/report_assets/20260916_meeting_clarity/build_reading_figures.py`生成07–10。读图副本及来源清单在 `R/daily_research_reports/0916/figures/sae_representation_update/` 的figure_manifest.json、figure_manifest_clarity.json。
- 图清单：01假设/梯度路径；02领域可读性轨迹；03配对几何与可读性；04固定feature激活轨迹；05特征使用与重构；06重构梯度强度；07原始Fisher绝对轨迹；08去PC1后Fisher；09FVU轨迹；10训练loss背景。另从E01保留PCA/UMAP/t-SNE轨迹。旧01是串联图，新模型须更新实际拓扑。

### 5. “图更好”的具体交接要求（展示改进，不改变统计问题）

- 所有图统一模型名称、颜色与顺序；清楚区分旧串联/新旁路。时间曲线用真实累计有效预测token的数值横轴，不能把0/.5/1/3/5/10画成等距而不说明；缺checkpoint断线，禁止外推成已测结果。
- Fisher画原始和去共同方向的绝对轨迹，并配对应模型差值与已有/重算配对区间；不把几何、线性读出与命题语义合并为一项。保留07/08已修正的纵轴防截断检查，所有点和区间完整入框。
- 激活图固定样本行及模型内部feature列；旧选择方法为fit上汇总0.5–10B一次选择30个（6共享+每领域6个）后回看全部时期，report只展示。必须标注这是回顾性选择。不同模型feature列不是一一语义对齐，0B所选列很淡不等于SAE全死。
- 激活热图颜色按原脚本的贡献份额口径，不能写成“激活率”；统一色阶、清楚说明变换和单位，领域分界清晰、字号足够。必要时拆为每页少量时间点及全量附图，不能靠删除不理想点改善趋势。
- 重构曲线标明原生输入位置，辅以原表征能量/范数，解释低FVU不等于语义好；梯度图分开整主干范数比与参数组分布，共享embedding去重，局部梯度不写成真实历史更新。
- PCA/UMAP/t-SNE交代共同坐标如何拟合，PCA注明解释方差；只作读图辅助。LM曲线同token对齐，训练与固定评测分开，平滑口径透明，不能继承旧15B范围掩盖新模型缺点。
- 输出高分辨率PNG和SVG（需要时PDF）、源指标表、脚本及哈希来源清单；中文不缺字、图例不挡数据、轴不裁切。每图配一句“回答什么、怎么读、边界是什么”。科学图用标准绘图工具，不生成伪实验图。
- 新产物放独立执行目录；汇报引用的读图副本放汇报当日自己的figures目录，保留0916旧图，不覆盖旧证据。重跑完成后按四类结论回写正式结果阅读面，而不是只给图册。

- Current work: 已核对正式Summary、最新执行memory、现行protocol及修订入口、旧执行/制图脚本地址；本轮只追加此工作记录。新模型具体共同checkpoint、实际运行时长/算力及新结果均未核定，不能写成已完成分析。
- Next action: 新任务完整读本memory，再读E01 Summary/Protocol和最新训练执行记录；先交付已有模型身份—同位置读点—完整checkpoint清单，随后在相应分析执行范围内复用旧流程和改进图表。旧训练授权不自动授权新远程分析；无需重开模型设计讨论。遇到同位置不可比、checkpoint不完整或状态会被诊断修改时，停止该单元并报告原因，其他独立合格单元可继续准备。
- References: 上述E01拥有旧结果与证据边界，0916训练protocol（含附录）拥有实际模型/执行范围；本memory只为跨任务导航，未修改Focus、Anchor、Protocol或科学裁决。本轮不提交、不发布、不push。

## 2026-09-17T09:56:13Z -- 同一对话记录合并与唯一读取入口

- Processed by: Codex (harness: Codex desktop; model: unknown).
- Summary: 研究者明确指出0914-training-scheduling-01a0a878与0914-training-scheduling为同一对话，要求合并；已核对本对话可见请求与两份记录的连续内容。现统一到本文件，保留原始Created at及全部七条历史记录的正文和时间顺序。未取得独立平台元数据来补证早期线程ID；身份统一依据为研究者此次明确纠正与可见历史的一致性。
- Supersedes: 2026-09-16条目中“distinct source/独立记录”的判断及各处要求以带后缀目录续接的导航已被本条纠正；历史正文原样保留以便追溯。旧目录最初保留跳转说明；随后按研究者明确要求删除，不再维护第二份累计memory。
- Current work: 本次仅合并记忆。2026-09-17上一条完整保留了既有分析结果边界、数据与流程、执行和制图脚本地址、新模型读点适配及图表改进要求；这些仍是当前工作上下文。没有启动训练、分析或GPU作业，没有修改科学状态。
- Next action: 新任务完整读取本文件，按上一条“既有分析结果、复用流程与新版图表要求”接续已有模型的分析准备；核对真实checkpoint与相同测量位置，复用旧流程并改进图表，不重新讨论新模型设计。
- References: 原带后缀目录 `.research/memory/conversations/0914-training-scheduling-01a0a878/` 已按研究者要求删除；唯一入口为本文件；正式证据、协议和脚本路径均见上一条，合并不改变其权威归属。
