# Conversation Memory: 0914-training scheduling

Conversation name: 0914-training scheduling
Processed by: Codex (harness: Codex; model: unknown)
Created at: 2026-09-14T11:26:13Z
Latest update at: 2026-09-15T15:47:22Z
Continues from: .research/memory/conversations/0912-梳理-sae-动态形成预训练方案/memory.md
Environment: repo=/data/250010109/Research_System; exec=/data/250010109/MoE_Router. Both roots readable in this conversation.

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
