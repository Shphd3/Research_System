# Conversation Memory: 0914-training scheduling — source 01a0a878

Conversation name: 0914-training scheduling (user-supplied historical name; distinct source 01a0a878-2ce3-7a30-99f1-5ab072cea6db)
Processed by: Codex (harness: Codex desktop; model: unknown)
Created at: 2026-09-16T07:25:35Z
Latest update at: 2026-09-16T10:05:31Z
Continues from: ../0914-training-scheduling/memory.md
Environment: repo=/data/250010109/Research_System; exec=/data/250010109/MoE_Router; both readable.

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
