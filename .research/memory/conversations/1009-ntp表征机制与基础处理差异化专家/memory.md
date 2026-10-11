# Conversation Memory: 共享与干扰学习：列表规则数据与Anchor

Conversation name: 1009-共享与干扰学习：列表规则数据与Anchor
Thread ID: 01a11f73-a1db-7643-9767-fc252c756741
Processed by: Codex (harness: Codex; model: unknown)
Created at: 2026-10-09T09:01:30Z
Latest update at: 2026-10-09T15:50:55Z
Continues from: none
Environment: repo=/data/250010109/Research_System; exec=/data/250010109/MoE_Router (both filesystem roots visible)

This is conversation-scoped, non-canonical working context. Append later checkpoints to this file. Do not use it to authorize scientific state changes, experiments, commit, push or publication.

## 2026-10-09T09:01:30Z -- 建立本对话记录，澄清基础处理与差异化专家的研究层次

- Processing agent: Codex /root; harness Codex; exact model identifier unknown. Current title and thread identity were verified using set_thread_title and read_thread before this first write.
- Summary:
  - 本对话从指定 ChatGPT 对话“1008-共享学习相关调研推进”的近期讨论及 1002—1008 原件开始。读取返回最近5轮；用户发言和一篇完整助手更新可读，其他数条助手回复仅返回内容引用，截图及最新深度研究正文不可核查。不可把这些未读内容作为证据。
  - 上位目标保持：在有限数据、参数和计算预算下，理解哪些学习需求值得共享、哪些值得分别学习，以改善习得与保持。当前讨论向上游展开：上下文出现分布与条件下一词预测规律，如何分别及共同通过NTP塑造预测功能和内部表征。1002已有条件续写、预测误差及局部更新后果推导；新讨论不意味着原机制缺失。
  - 研究者明确纠正：不把“高频造成各向异性”作为先验或已知事实。该关系是独立待考证问题，可用文献或实验，要求最终给出对象和条件明确的结论。当前特定NTP测点的频率因果作用为Unknown。词元频率、上下文频率、规律曝光量、条件后继概率必须分开。
  - 研究者提出的直觉：足够容量的基础处理模块承担可复用处理，不称其为common expert；其余unique experts提供相对于基础处理的差异化处理能力，使输入获得有侧重的处理。此为对话确认的研究意图、pending canonicalization；实际可复用结构、功能形成机制与净收益仍未确认。
  - 必须分开两个层面：功能组织（哪些计算可复用、哪些需要条件化补充）与数据/学习分配（哪些样本调用或更新哪些参数）。同一条输入可以同时需要基础计算和某个差异化专家，不应预先把样本分成互斥的“common数据/unique数据”。基础共享权重也可以产生随输入变化的输出。
  - AI审计建议：将该直觉放在“NTP习得预测功能”与“架构及路由/学习分配”之间，作为可复用处理与差异化补充的候选功能组织假设。链条用于区分问题层次，不规定所有研究必须串行完成。
  - “独特参数方向”先作为待解释直觉，建议操作化为特定输入上相对基础处理的有用补充计算。参数不同、夹角大或正交不保证不同预测功能。路由识别的是处理需求，其决策信息必须在目标揭示前可见；专家负责执行处理。
  - 基础与差异的分解可能不唯一。模块名称不保证实际功能纯度；容量可实现性不保证优化成功、实际复用、稳定保持或资源收益。串行/并行连接、联合/分阶段训练及容量分配尚未在本对话中选定。差异化分工可以在学习过程中形成，无需预设冻结模型已经有可用差异。
  - 既有1002容量工作已讨论共同映射和私有残余、统计汇聚及不能小容量分解的反例；private-only也保留共享embedding/Attention/norm。该直觉与这些既有模型兼容，不应包装为首次建立模型或已验证的自然语言机制。
  - 正式roadmap仍指向domain_update_geometry Focus，研究者机制判断Unknown。没有修改Focus、Anchor、冻结Protocol或原结果裁决。
- Current work:
  - 已重读当前磁盘AGENTS.md，包含新资产登记与当前会话访问检查规则；已核对research-memory契约、当前标题与身份，建立此唯一记录。
  - 已完成三项并行只读核对：历史容量/共享模型定位、推理审计、频率与几何文献对象边界。文献目前只支持特定对象与条件的机制，不能作为任意中间层频率因果结论。
  - 本次仅文档阅读、对话重命名及本记录写入；未使用模型/SAE权重、表征缓存或数据内容，未新建实验或提交远程作业。后续若使用资产，先按assets/README.md查询ID并执行tools/check_assets.py --strict，旧快照不作为当前访问证明。
  - 导航检查已运行：79个入口，3个已有未跟踪项（diffusion文献入口、assets/README.md及README_cn.md）。未处理其他会话的改动；这些导航问题不产生科学结论。
- Next action:
  - 继续讨论时，先把“基础模块＋差异化专家”的直觉转写成可判别的功能互补假设，明确基础参照、目标前可见信息、最强竞争解释及差异化收益的含义；保留“频率是否影响指定表征的各向异性”为独立待考证项。正式科学问题、设计采用和昂贵运行仍以研究者及各自owner为准。
- References:
  - AGENTS.md：当前会话规则，尤其科学权属、资产登记及实验边界。
  - .agents/skills/research-memory/references/memory_contract.md：记录路径、身份验证及append-only规则。
  - .agents/skills/research-reasoning-auditor/SKILL.md：本次推理审计owner。
  - Projects/from-attention-to-search/main/roadmap_cn.md；main/focus/focus_domain_update_geometry_cn.md（后者相对同项目根）：现有正式导航及科学判断，不由本记忆变更。
  - daily_research_reports/1002/candidates/ntp_representation_update_channels/research_report_cn.md：上位目标、局部问题及§5条件续写推导。
  - daily_research_reports/1002/candidates/ntp_representation_update_channels/capacity_report_cn.md：基础主干、额外共同模块、私有专家，及功能复用/容量/学习动态的边界。
  - daily_research_reports/1002/candidates/ntp_representation_update_channels/capacity_mathematics_cn.md：可复用结构到表示能力、实际学习和收益的分层模型。
  - daily_research_reports/1002/candidates/ntp_representation_update_channels/sharing_routing_mathematics_cn.md：路由与专家信息职责、学习分配形成差异、有限样本共享权衡。
  - daily_research_reports/1004/cognition_update_cn.md：当前计算选择与未来学习分配；初始功能匹配不等于后续优化轨迹匹配。
  - daily_research_reports/1008/local_update/full_report_cn.md；daily_research_reports/1008/candidates/sae_error_signal_alignment/summary_cn.md：局部更新及有界H2证据，不能外推长期分工收益。
  - assets/README.md：未来资产lookup-before-pause与strict访问检查；本轮没有使用资产内容。
  - ChatGPT conversation ID 6ac76c82-2064-83ee-ad9e-ce1c6822699c：指定讨论源，可读取内容的边界见Summary。
  - https://arxiv.org/pdf/1907.12009；https://aclanthology.org/2024.eacl-long.3/；https://arxiv.org/html/2408.15417v2：频率/softmax/几何文献，各自对象和模型条件必须保留，不能泛化成当前测点因果。

## 2026-10-09T14:47:17Z -- 数据集优先：首项/末项规则 Anchor 草稿与学习线建议

- Processing agent: Codex /root; harness Codex; exact model identifier unknown. Current title was updated to `1009-共享与干扰学习：列表规则数据与Anchor`; thread identity and this memory path are preserved.
- Summary:
  - 研究者将当前范围明确为第一部分的数据集构造，本轮不研究表征；要求先写 Anchor 供评判，再评估“共享和干扰学习”新线及旧材料归类。
  - 1009 对话读取只返回用户正文及助手内容引用；研究者随后在本对话粘贴完整助手方案，已补全首项/末项数据方案的来源。1008 仅读取最后三轮；未读取不可用图片和附件。
  - 同一有序三词列表配对两条可见规则 FIRST/LAST，答案分别取首项/末项；列表相同不等于完整前文相同。不同列表可以服从同一规则，规则不同也不意味着共享模型无法同时完成。
  - 原方案每规则训练2,000、开发400、测试400条，共2,800个基础列表、5,600条记录（未扩展改写）。单答案词元资格、均衡、划分均尚未执行。AI 建议按无序三词集合分组，以减少跨划分共享组合；20词仅有1,140个无序集合，不能声称2,800个独立集合。
  - 第一阶段规则曝光均衡；第二阶段频率建议固定样本池改变呈现次数，以区别频率与独特样本量。增加 A 且固定 B 的曝光会改变总预算，频率对照设计暂缓，不声称已消除计算混杂。
  - 后续判据为有效来源更新后的接收者净损失，补完整来源×接收规则二乘二表及不更新参照。帮助幅度减小不等于净伤害；大步长竞争解释限制更强机制推断，不取消已经合格测出的有限损失符号。
  - 推荐新线 A17“共享与干扰学习”，属于 AI 建议。局部编号核对发现 A16 已有负载控制/梯度干扰归属；A07、A15、A16 原有权属保留。未激活 A17、未创建新 Focus、未修改 roadmap、未迁移历史材料。旧材料先关联，后续按当前问题归属选择性迁移，保留冻结结果。
- Current work:
  - 已创建唯一问题的中英文 Anchor 草稿：`Projects/from-attention-to-search/main/problem_anchors/shared_updates/controlled_list_prediction_rules/anchor.md` 与 `anchor_cn.md`，并在既有 `shared_updates/README.md`、`README_cn.md` 添加草稿入口。
  - 草稿为 `AI_PROPOSAL_PENDING_REVIEW`，结果 `NOT_RUN`，机制判断 `Unknown`；包含八节契约。新增分组、完整二乘二比较和有限作用判据均明确为 AI 建议，不冒充原方案或研究者批准。
  - 独立只读推理审计完成；已纠正答案输入表述：正确词本来就是合法列表候选，禁止的是答案标记后的已填答案字段进入前文。已区分有限伤害观测与稳定任务不相容解释。
  - 两份 Anchor 数学源码检查通过；两份 Anchor 和两份索引的82个本地链接检查通过；项目 `git diff --check` 通过。导航 working-tree 检查79入口、零问题、3个既有 pending tracking；严格跟踪检查的旧问题未由本轮处理。检查不验证科学机制。
  - 本轮未加载模型、分词器、数据或表征资产，未生成数据，未训练、未远程提交。项目分支 Xingyu 未切换；没有 commit、push、Graph 编辑或外部同步。
- Next action:
  - 本条接续并更新此前“先形式化专家直觉”的工作顺序：先由研究者评判首项/末项载体、分词器与答案损失、划分独立单位及样本规模/均衡，然后实现并核验选定数据生成器。当前草稿不提供昂贵运行授权；后续学习测量需另行落实 Protocol 中的模型、参数、更新及确认设置。
- References:
  - `Projects/from-attention-to-search/main/problem_anchors/shared_updates/controlled_list_prediction_rules/anchor.md`、`anchor_cn.md`：本轮可评判草稿，唯一科学设计候选。
  - `Projects/from-attention-to-search/main/problem_anchors/README.md`、`16_load_control_gradient_interference/README.md`（后者相对同一 problem_anchors 根）：现有编号与 A16 归属核对。
  - `Projects/from-attention-to-search/main/problem_anchors/shared_updates/README.md`、`README_cn.md`：既有证据与本轮草稿导航。
  - `Projects/from-attention-to-search/main/experiments/shared_updates/shared_update_conditional_interference/20260927_controlled/summary_cn.md`：此前不同向量载体的有界结果；不能作为本轮列表结果。
  - `.agents/skills/problem-anchor-writer/SKILL.md`、`.agents/skills/research-reasoning-auditor/SKILL.md`、`.agents/skills/research-mainline/SKILL.md`：本轮设计草稿、审计与组织评估责任边界。
  - ChatGPT conversation IDs `6ac8f187-8260-83ec-8bf9-b7cd80c55898`、`6ac76c82-2064-83ee-ad9e-ce1c6822699c`，以及研究者本轮粘贴的完整1009方案：源内容及可访问边界见 Summary。

## 2026-10-09T15:50:55Z -- A17创建迁移与第一阶段Smoke完成

- Processing agent: Codex /root; harness Codex; exact model identifier unknown. Thread与记录路径保留；当前标题为1009-共享与干扰学习：列表规则数据与Anchor。
- Summary:
  - 研究者确认首项/末项、Qwen3-0.6B分词器、答案损失、两种未见分别及合并报告、频率按固定池呈现次数；明确授权A17创建迁移、第一阶段代码与4H100 reserved Smoke，最后要求开始实现并测量。授权边界已落实于Protocol；不由本记忆提供权限。
  - 唯一Anchor迁移至A17_01，problem_key仍为list_rule_shared_update；稳定Focus已建立，导航更新；旧共享更新历史关联保留，A07/A15/A16归属未改，没有改写冻结旧结果。当前规范中英文Summary/Detailed完整记录结果。
  - 已生成并核验5,600行数据；两种未见相对于本轮任务训练，不保证预训练未见。Dense exact33B和Qwen Base分别短适配；S7-fresh exact33B只读初始能力，不做SAE/表征。S7 sidecar保持原生LM前向，主要区别为训练历史/目标。
  - 作业pt-2m4rvpt4已SUCCEEDED，31/31工程门PASS。Dense/Qwen各32更新/2,048有效答案，16/32实际保存并外进程恢复16。32状态恢复和不中断轨迹一致性未检查，GB载荷hash未计算。实际dataset与两训练输出已登记并strict访问通过。
  - 能力与四格作用分别/合并见Summary和Detailed；不能从初始零推断完全无能力，从开发全对推断普遍掌握，或把模型差异归因架构。终点饱和；按编号前32来源令首项答案全“红”；部分来源未改善同规则dev，分项符号会抵消，数值分辨率未校准。科学NOT_EVALUATED，机制Unknown；test模型未开。
- Supersedes: 前条“未激活A17、无Focus、未迁移、未生成/运行”为旧事实，现由A17 Anchor、Focus、Protocol及Summary/Detailed更新；原日志保留。
- Current work:
  - 授权代码/数据/Smoke与事实记录已完成。10项CPU训练测试、10项资产登记测试、冻结18文件hash、两Anchor数学源码、345相关链接和git diff --check通过。导航working-tree84入口0问题，8项pending tracking；未commit/push/Graph/外部同步。
  - 无重试/自动监控/新增Full；频率草案暂缓。该Smoke工程完成不改变科学判断。
- Next action:
  - 研究者验收或修复第一阶段工程链路，再决定独立科学Protocol。AI建议前瞻选择较早未饱和状态、均衡独立来源批与数值分辨率/步长检查；建议未形成科学采纳或新运行授权。
- References:
  - Projects/from-attention-to-search/main/focus/focus_list_rule_shared_update_cn.md：稳定问题与独立状态。
  - Projects/from-attention-to-search/main/problem_anchors/17_shared_and_interference_learning/17_01_controlled_list_prediction_rules/17_01_controlled_list_prediction_rules_anchor_cn.md：迁移后唯一科学设计；../README_cn.md持有A17线导航。
  - Projects/from-attention-to-search/main/experiments/A17/17_01_controlled_list_prediction_rules/A17_01_E01_stage1_smoke/protocol.md：冻结Smoke范围与执行契约；同目录summary_cn.md、detailed_cn.md：已完成事实、原始证据、限制与未运行分支。
  - /data/250010109/MoE_Router/experiments/20261009_a17_list_rules/README_cn.md：源码与复用说明；runs/smoke_4h100_20261009T152323Z/terminal_verification.json、artifact_manifest.json、execution_certificate.md、completion_checks.json：实际作业、工程检查和产物证据。
  - assets/a17_list_rules_cn.md、assets/checks/2026-10-09_a17_inputs.json、assets/checks/2026-10-09_a17_smoke_outputs.json：实际输入/数据/保存状态与访问；不授予科学结论。
