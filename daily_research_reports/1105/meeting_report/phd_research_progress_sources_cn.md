# 博士生研究进展报告：编写依据与边界

本文件服务于[第五版填报稿](phd_research_progress_draft_cn.md)，不属于提交到学校系统的正文，也不替代项目中的科学设计或结果记录。初稿日期为2026年11月5日，第二版为11月6日，第三至五版为11月7日。[第一版](phd_research_progress_draft_20261105_cn.md)、[第二版修订前文件](phd_research_progress_draft_v2_20261106_cn.md)、[第三版](phd_research_progress_draft_v3_20261107_cn.md)和[第四版](phd_research_progress_draft_v4_20261107_cn.md)按各次保存时的原字节保留。

## 个人信息与填报口径

- 本人直接提供：2025年10月入组，以 MoE gating 为主要研究方向，做过 MTP 相关研究；目前没有正式科研项目，主要从事基础研究；2026年争取发表1篇主方向论文，预计2029年毕业。
- 本人确认统计范围为2025年10月至2026年11月。截图表头写“2025—2026学年”，正文采用本次确认的统计期，不把10—11月工作暗写成上一学年成果。
- 姓名邓星宇、学号250010109只用于文件识别。未填造项目编号、负责人、正式项目角色、专利、开源贡献或正式发表信息。
- 附件中的旧稿是研究过程材料。正文不列旧稿题目、篇数或投稿身份，不将它们计作正式论文成果。
- 下一阶段的具体技术安排是报告拟写建议，不激活新问题、不批准实验、不改变原记录中的 Unknown。2026年发表是争取目标，不是已发表或保证录用；2029年是预计毕业年份。

## 第五版：根据三次组会更新表征认识与学习假设

研究主线表述为：理解自然语言的共享与细分结构，观察这些结构在表征和训练中的体现，再检验结构化分发是否改善专家学习，最终服务于长尾学习效率与通用能力保持。这里连接的是研究问题，不把结构、学习机制和架构收益写成已经证实的连续因果链。

### 新增材料及其用途

| 组会材料 | 本轮采用的认识更新 | 证据身份与限制 |
|---|---|---|
| [1028会议转写勘误稿](</root/.codex/attachments/c7aac41b-1e9b-47ff-8123-b5583bb3d229/1028_会议转写_勘误稿_v1 (1).md>)、[会后叙述校订稿](</root/.codex/attachments/c7aac41b-1e9b-47ff-8123-b5583bb3d229/1028_会议叙述_单独校订稿_v1 (1).md>)、[解析与后续建议](</root/.codex/attachments/c7aac41b-1e9b-47ff-8123-b5583bb3d229/1028_会议解析与后续分析建议 (1).md>) | 类别代表方向在总体表征谱中的位置、实际区分能力及分开学习的价值，需要分别建立联系。特征频率、谱位置、名单重合和方向正交不能直接互换。 | 原转写含未核词句；解析中的新实验是建议。少量候选不代表一个领域的全部知识，也不认定已经存在互斥的功能子空间。 |
| [1030会议转写纠偏版](</root/.codex/attachments/c7aac41b-1e9b-47ff-8123-b5583bb3d229/1030_会议转写_纠偏版(1).md>)、[1030会议理解](</root/.codex/attachments/c7aac41b-1e9b-47ff-8123-b5583bb3d229/1030 会议理解 (1).md>) | 类别差异既可表现为共享成员的强弱差，也可表现为成员组成不同；路由需要分析二者的实际贡献，并考虑训练中的变化。 | “高频主要靠幅值、中低频主要靠有无”是会议中的观察概括，正文不将其写成普遍分工。先共同后专有、浅层粗深层细、教师引导及渐进门控均保留为待检验解释或方案。 |
| [1106会议总结](/root/.codex/attachments/1f90282d-f2a9-4a7c-a40a-8455265a03ac/1106-会议总结.md)、[完整勘误转写与总结](/root/.codex/attachments/5d18bc7a-fa44-4fd6-b413-d357897bba3b/1106_组会勘误转写与总结.md)、[会议纪要图片](/root/.codex/attachments/64b412e4-66fe-46f6-bc5d-45943ac0b8d4/1106-会议纪要.png) | 将本人共享／更替特征结果接到共同研究路线，并把专家更新的信噪比、数据效率和通用能力保持作为当前待解释问题。 | 学长报告的教师分发收益不计为本人已完成成果；“聚集相关信息提高信噪比”是机制假设，尚无本材料给出的直接梯度检验。材料中的待办不视为本轮运行或对外操作指令。 |

### 正文中保留的实验认识

早期共同打分、受控学习速度及真实训练对照、固定专家下的候选反馈，沿用第三版里程碑表的原始依据；本版压缩其叙述篇幅，将重心移到近期自然语言结构与训练机制问题。

S13独立文本确认支持的是显式类别条件下、指定位置和两个固定字典中的共有成员平均参考频率下降。对同一批数据的共享集合拆解属于事后分析：多数原有共有成员被保留，同时出现额外的、平均参考频率较低的共有成员。这些是集合组织观察，“保留”不是训练时间过程，额外共有也不等于细类专属。成员更替和共有强弱分别叙述；不把原DEV类别偏向加权统计解释为所有更替成员等权统计，也不把更替当作全部语义区分能力。

本版重新核对[训练检查点分析](../../../Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/checkpoint_spectral_dynamics/20261101/summary_cn.md)：同一Dense轨迹12个可读状态的分析已完成，类别信息可读性可以先于表征几何稳定出现，尚无统一的谱前／中／尾稳定次序。正文据此强调训练动态；“粗语义先学、细语义后学”仍是另一个需要检验的对应关系，不能用谱方向结果直接替代。

“共享基础上的细化与组合”是本版采用的工作假设，不等于已确认层级树、独立语义组合机制、因果学习依赖或通用门控收益。浅层少专家、低维度及深层扩展属于设计方向；一个数量级压缩不列为成绩。有效信号和更新波动必须相对于具体学习目标定义，领域标签本身不能把跨类样本判为无用噪声。以上解释与后续安排均不改变原Focus、Anchor或实验的科学接受状态。

### 会议观察与正式结果的区别

正文的“记忆任务局部改善、通用任务下降”来自11月6日本人汇报02:16—02:48，仅用于交代当时观察到的任务权衡；材料没有提供对应运行、指标定义、数值或完整对照。本轮没有将其认定为下表末层记忆72阶段实验的同一结果，也没有用它覆盖正式结果中的未达到可靠学习与保持目标。会议图片把共享特征频率和任务权衡连成因果的说法不采用。

导师关于开放问题探索、相关性与新颖性奖励的讨论属于另一个问题，未并入个人MoE主线成果。关于信噪比的会后补述作为用户提供材料中的研究思路使用，不伪造缺失录音；本轮也没有将延长更新间隔、增大学习率直接列为已成立方法。

## 第四版：按填写提示分部分组织

采用三个不编号的标题：研究目标与阶段进展、承担工作与研究产出、当前问题与后续计划。目标与四个认识节点在同一部分连续叙述，保留研究主线；项目情况、本人工作及产出单独归在一处；困难、下一步问题和时间安排放在末部分。该结构对应填写提示的内容，不将每个提示或每个实验拆成独立小节。

文字调整集中在两处联系：学习偏好如何引出对实际任务收益的评价，专家功能评价为何还需要寻找输入线索。继续沿用第三版已核对的四个节点、实验范围和结论边界；受控实验的认识不改写为普遍机制，表征观察不改写为已验证的门控收益。技术计划仍是AI建议稿。

## 第三版：研究里程碑与认识推进

本版将里程碑限定为：已完成的有界实验或对照能够支持一项明确的认识更新，并使门控主线的问题更具体。工具训练、检查点数量和报告数量作为工作基础记录。下表不替研究者关闭问题或确认机制；受控因果结果、真实训练反例和条件性表征观察分别保留其证据等级。

| 主线中的认识节点 | 完整实验依据 | 可明确保留的认识及边界 | 对后续问题的推进 |
|---|---|---|---|
| 共同成分可以造成路由偏置，训练会改变其影响 | [A05共同打分干预](../../../Projects/from-attention-to-search/main/experiments/A05/A05_04_02_round2_dotproduct_common_logit/summary.md)完成R2-P0至P4；[真实文本审计](../../../Projects/from-attention-to-search/main/experiments/A05/A05_04_03_real_text_common_logit_audit/summary.md)完成四阶段。 | 合成任务中取消共同打分改善路由与槽位的一致性并保持准确率；真实文本中共同项在初始化时平均不占主导，早期训练后影响增强。前者有受控干预证据，后者未独立确定训练放大的中介机制。 | 从描述输入分配，推进到解释路由偏置及其训练演化。 |
| 统计结构影响有限时间学习速度，任务价值需另行检验 | [受控谱学习](../../../Projects/from-attention-to-search/main/experiments/A15/15_01_spectral_learning_and_feedback_dynamics/A15_01_E01_controlled_covariance_learning_speed/summary.md)完成注册S0/S1；[2B固定方向对照](../../../Projects/from-attention-to-search/main/experiments/A15/15_05_functional_coordinate_admission/A15_05_05_E01_2b_matched_band_dispatch/summary.md)九臂完成；[10B匹配随机对照](../../../Projects/from-attention-to-search/main/experiments/A15/15_06_online_spectral_routing_and_relay/A15_06_E02_local_random_identity_control/summary.md)完成两种子。 | 固定高斯表征、匹配目标和纯SGD下，方差影响学习时间，低方差目标可学习；真实模型中已测方向选择方案未获得稳定功能优势。S2未运行，不并入完成范围；负结果不等于所有表征路由无效。 | 将“容易被学到”和“值得用于路由”分开，以实际预测收益评价候选信息。 |
| 有用专家的存在与被门控发现是两个环节 | [A06轮换候选对照](../../../Projects/from-attention-to-search/main/experiments/A06/06_03_utility_binding_and_sparse_discovery/A06_03_03_E01_rotating_challenger/summary.md)完成完整损失、任务损失、反馈覆盖及通用专家对照；[Detailed](../../../Projects/from-attention-to-search/main/experiments/A06/06_03_utility_binding_and_sparse_discovery/A06_03_03_E01_rotating_challenger/detailed.md)说明表征和专家冻结。 | 在这个固定系统中，已选专家反馈未纠正错误身份，加入一个轮换候选的完整损失比较能够纠正大多数或全部单元。不是自然语义分工、联合训练收益或计算最优的确认。 | 将专家实际作用与门控可获得的反馈纳入评价，检查门控能否利用已有功能差异。 |
| 共有成员的频率与类别更替成员的频率具有不同结果 | [S13新文本确认](../../../Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S13_eight_category_independent_1105/summary_cn.md)完成冻结面板和全部前向；[更替原判定审核](../../../Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S13_eight_category_independent_1105/posthoc_turnover_audit_1106/summary_cn.md)保留S11原16项结论。 | S13显式类别的32项预设频率比较通过标准；成员更替仍为6支持、5反向、4未决、1不足。结论限指定文本、字典、位置和参考语料，是条件性统计观察。S13共享集合的事后拆解不计为新的独立确认，隐式行为不足及后续NOT RUN保留。 | 将共享信息与内容差异转化为可测对象，同时保留它们是否对应专家功能差异这一待检验联系。 |

表中节点按报告的解释顺序串联，不把并行开展的研究改写成严格的时间因果链。各节点的数值、限制和来源在下文保留。第四个节点的观察证据不提升为已验证的语义层级、专家最优分工或训练效率收益，原科学接受与机制判断仍以所属记录为准。

第三版压缩了SAE/CrossCoder的层数、检查点数量、具体类别例子和训练臂设置。近远证据、末层记忆与MTP保留在本来源文件中，作为“读出、使用、收益需分别检验”的补充；正文不再为每项工作单列一段。正文仍涵盖研究目标、主要工作与认识、本人角色和产出、当前困难及后续时间安排。

## 前两版的主线与填写提示

研究者要求把已有工作梳理成一条主线。本稿以“门控依据输入中的什么信息选择专家，才能形成有用分工并改善学习”为核心问题。路由偏置与学习动态解释门控为何学到某些选择；专家损失比较提出功能评价；表征研究寻找候选输入信息；证据使用、知识学习和MTP结果帮助检验信息是否真正用于预测。这是报告的叙述组织，各个问题的原有归属、审批与科学状态保持不变。

11月5日至6日新增结果按这条主线选用：S13补充共享结构的有界观察，R01/R02补充行为检验，末层记忆实验补充训练与自主回答不一致的结果。S13的共现边、类别关系差和辅助读出没有被写成已确认的语义交互或专家分工。成员更替反例保留，近期结果不被汇总为一种已经验证的门控方法。正文通过问题之间的联系衔接，不再使用序数式串联。

| 填写提示 | 本文处理 |
|---|---|
| 研究目标及完成情况 | 开头写核心问题、已完成的分析流程和有条件结论，并明确真实语言任务的稳定方法收益仍待验证。 |
| 实验、建模、数据分析或理论推导 | 写共同打分对照、固定表征学习模型、专家损失比较、SAE/CrossCoder分析、行为与训练检验；旧稿推导不提升为已验证普遍定理。 |
| 科研项目及本人角色 | 依据本人说明写基础研究、暂未承担正式科研项目；写本人负责的文献、建模、实现、分析和整理工作，不编造项目名称、编号或负责人。 |
| 开源项目、国产软硬件生态实践 | 当前材料没有本人确认的可填报条目，未新增相关经历，也不把使用开源模型写成参与该开源项目。 |
| 阶段成果与学术产出 | 以机制分析、实验结果、代码工具及研究报告表述，不列未发表小论文的题目、篇数或正式发表身份。 |
| 困难、解决方案及后续时间安排 | 写受控认识向真实任务转化的困难和已用的比较方法；技术计划为AI建议，发表与毕业年份沿用本人目标。 |

## 阅读范围

11月5日编写初稿时，先核对 System 的项目导航和 from-attention-to-search 的路线图、归属登记与研究地图，再沿原问题读取结果。全工作区完成文件清点、文本类别统计和研究导航核对，重点覆盖当时from项目的13条研究线、169个已登记问题的证据导航，并精读下表相关的 Summary、Detailed、阶段综合和近期讨论材料。导航中的历史快照与较新结果分别处理，例如11月4日地图概览的旧计数不作为当前事实。

全仓清点包含约5.8万个文件，其中有大量工程代码、重复阅读副本、图表与生成数据。这里的“全仓梳理”指文件和研究线覆盖，以及围绕报告事实的逐源核对，不表示逐行审计全部工程代码、逐幅查看全部图像或加载全部模型权重。缺失本地旧项目文件不推定为研究没有开展；他人项目或参考代码不计为本人科研产出。

两份附件均检查了目录、主稿和历史版本的研究脉络，重点读取实验结果与认识修订。MoE_Router 检查了实验目录、报告和选定保存记录，尤其是谱路由、SAE/CrossCoder、共享学习和最近的表征动态分析。未重新训练、运行模型前向或查询远程作业；下表的完成事实来自已保存记录。

11月6日复核原稿、学校填写提示截图、11月5日至6日阅读入口，以及S13独立确认、共享集合拆解、成员更替审核、A15_30 R01/R02和末层记忆的结果记录，并复核相关Focus及受控谱学习依据。本轮读取保存的报告，不加载模型权重或激活缓存，不运行新实验。11月6日早期末层记忆简报仍含“最大规模待完成”的旧快照，本稿采用执行侧随后完成的正式结果报告。

11月7日围绕第三版的四个节点，重新读取A05干预与真实文本审计、A15受控谱学习及2B/10B匹配训练结果、A06候选反馈结果与冻结条件、S13独立文本确认，并核对修订前正文和来源说明。选取的是有明确认识更新的已完成范围，不把父问题下所有计划都称为完成，也不重新运行实验。

## 正文主张与原始依据

| 正文内容 | 已核对依据 | 使用边界 |
|---|---|---|
| 共同打分影响受控路由集中；真实文本还需区分初始化与早期训练 | [A05共同打分取消 Summary](../../../Projects/from-attention-to-search/main/experiments/A05/A05_04_02_round2_dotproduct_common_logit/summary.md)、[Detailed](../../../Projects/from-attention-to-search/main/experiments/A05/A05_04_02_round2_dotproduct_common_logit/detailed.md)；[真实文本审计](../../../Projects/from-attention-to-search/main/experiments/A05/A05_04_03_real_text_common_logit_audit/summary.md) | 合成无位置编码、点积 top-1 的路由—槽位 NMI 从0.080到0.963，准确率均1.000。真实DCLM初始化共同项并非平均占优，训练后迅速增强。两者不能合为“所有MoE初始化必然由共同项主导”。 |
| 方差能够影响有限时间学习速度 | [受控谱学习 Summary](../../../Projects/from-attention-to-search/main/experiments/A15/15_01_spectral_learning_and_feedback_dynamics/A15_01_E01_controlled_covariance_learning_speed/summary.md)、[Detailed](../../../Projects/from-attention-to-search/main/experiments/A15/15_01_spectral_learning_and_feedback_dynamics/A15_01_E01_controlled_covariance_learning_speed/detailed.md) | 八种子、固定目标、固定高斯表征、纯SGD。方差4:2:1对应学习时间约1:2:4；白化消除次序，tail-only可学。真实三种子轨迹因负载守卫失败为INSUFFICIENT，未建立真实联合训练的形成机制。 |
| 固定谱规则未获得稳定功能优势 | [固定频带分发](../../../Projects/from-attention-to-search/main/experiments/A15/15_05_functional_coordinate_admission/A15_05_05_E01_2b_matched_band_dispatch/summary.md)、[匹配随机身份对照](../../../Projects/from-attention-to-search/main/experiments/A15/15_06_online_spectral_routing_and_relay/A15_06_E02_local_random_identity_control/summary.md)；[A15综合](../../../Projects/from-attention-to-search/main/stories/15_spectral_representation_and_functional_routing/01_router_spectral_bias_and_learning_dynamics_cn.md) | 结论限于已测固定频带、预算和模型。不能推广为所有表征路由无效，也不能把改变分发本身当作性能改善。 |
| 功能性分工需要同输入上的专家损失比较；受控候选反馈可以修复错误选择 | [A06功能路由综合](../../../Projects/from-attention-to-search/main/stories/06_geometry_proxy_preservation/01_functional_specialization_and_utility_routing_cn.md)、[轮换候选实验](../../../Projects/from-attention-to-search/main/experiments/A06/06_03_utility_binding_and_sparse_discovery/A06_03_03_E01_rotating_challenger/summary.md)、[真实代码实验](../../../Projects/from-attention-to-search/main/experiments/A06/06_04_real_workload_utility_headroom/A06_04_01_E01_context_conditioned_expert_utility/summary.md) | 固定四专家受控系统中，full-pair修复rank-2的128/128与rank-4的125/128单元；selected-only均0/128。真实代码最终层未通过身份稳定及正绝对收益门槛。没有实际系统加速或通用路由收益结论。 |
| 特征分组、实际接收与专家学习是分开的观察环节 | [A15_19接收审计](../../../Projects/from-attention-to-search/main/experiments/A15/15_19_feature_group_to_actual_dispatch/20261018_routing_audit/summary_cn.md)、[A15_20分发对照](../../../Projects/from-attention-to-search/main/experiments/A15/15_20_frequency_priority_actual_dispatch/20261019_dispatch/summary_cn.md)、[A15_24优化器耦合](../../../Projects/from-attention-to-search/main/experiments/A15/15_24_frequency_composition_common_path/common_optimizer_coupling_20261022/summary_cn.md) | 分组变整齐未保证低频目标实际接收；优化器裁剪干预没有稳定低频收益。不写成频率分发或共享路径已解决学习问题。 |
| 14个选定层的CrossCoder训练和特征分析已完成 | [执行侧最终训练分析](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/final_training_20261013T115447Z/report.md)、[联合特征阶段一](../../../Projects/from-attention-to-search/main/experiments/A15/15_25_joint_feature_graph/summary_cn.md) | 冻结Qwen3-0.6B，16,384个特征，999,997,440个配对位置/曝光。第28层重构替换仍增加CE约0.306 nat，数值重构不等于语义或因果解释完成。 |
| 同一Dense轨迹的12个检查点分析已完成 | [谱与方向动态Summary](../../../Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/checkpoint_spectral_dynamics/20261101/summary_cn.md)、[覆盖账本](../../../Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/checkpoint_spectral_dynamics/20261101/tables/coverage_ledger.csv)、[执行清单](/data/250010109/MoE_Router/experiments/20261101_dense_checkpoint_spectral_dynamics/manifest.json) | 同一约2.81亿参数模型、0.5B–33B有效预测token，12个可读状态。另有8个历史缺权重状态保留BLOCKED；33B不是最终收敛真值，没有统一头/中/尾稳定顺序。 |
| 共有与区分特征不服从统一高低频分工；距离变化可伴随成员重组 | [S10新家族结果](../../../Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S10_frequency_shared_discriminative_1105/summary_cn.md)、[R20距离结果](../../../Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R20_20261104_distance_composition/summary_cn.md) | 限指定模型、字典、位置、措辞和有限参考语料。激活频率不等于训练曝光或谱位置；特征码变化不等于模型记忆总量。机制判断与科学接受仍Unknown。 |
| 八组显式类别中，细类共有成员的平均参考频率较低；已有数据拆解显示保留与额外共享并存 | [S13独立确认Summary](../../../Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S13_eight_category_independent_1105/summary_cn.md)、[共享结构事后分析](../../../Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S13_eight_category_independent_1105/posthoc_shared_structure_1106/summary_cn.md) | 48确认家族、16场景簇；8组×2独立SAE×2参考轴的32项显式比较通过冻结标准，平均频率差0.95–9.93个百分点。MLP/Q粗动物–交通工具共有成员46.74%，细猫–狗39.60%，差7.14个百分点，95%联合区间[5.61,8.66]。32项不是32次独立训练。名称改写31/32支持，隐式多数行为不足。后续集合拆解为事后探索：MLP猫狗保留率92.80%，另有平均7.75个额外共有成员；额外共有不等于细类专属。 |
| 成员更替没有统一低频趋势；共享成员也可有强弱差 | [Top32成员更替审核](../../../Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S13_eight_category_independent_1105/posthoc_turnover_audit_1106/summary_cn.md)、[共享结构与强弱案例](../../../Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S13_eight_category_independent_1105/posthoc_shared_structure_1106/summary_cn.md) | S11原16项为6支持、5反向、4未决、1不足，原判定不变；例如MLP/Q汽车–自行车更替频率6.73%→13.50%。指标只覆盖进入/退出Top32的成员，不等于全部类别区别。共享成员强弱差也是描述；不据此识别功能专属或训练依赖。后续独立更替确认仍NOT RUN。 |
| 完成37个训练状态的证据使用检查；较好的单事实调用不能替代关系选择检验 | [R01近远证据使用](../../../Projects/from-attention-to-search/main/experiments/A15/15_30_checkpoint_evidence_use/R01_behavior/summary_cn.md)、[R02关系绑定](../../../Projects/from-attention-to-search/main/experiments/A15/15_30_checkpoint_evidence_use/R02_relation_binding/summary_cn.md) | R01为Dense14、Baseline23个真实状态；与此前12点表征分析不是同一面板，不累加为独立重复。R02选3/15/17B六状态，576绑定前缀和576旧任务FP32参照。候选两世界均正确为1–9/24；Dense15B近程旧23/24、新5/24，Baseline3B远程旧23/24、新7/24。关系分差可向正确方向变化而仍答错。近程同样弱；单轨迹、容量和任务差别限制架构或距离的因果解释。 |
| 末层附加记忆完成受控学习对照，当前实现未达到可靠知识学习与保持目标 | [正式结果与有界分析](/data/250010109/MoE_Router/experiments/20261105_last_layer_memory/results_report_cn.md)、[方法与资产](/data/250010109/MoE_Router/experiments/20261105_last_layer_memory/report_support/methods_assets_cn.md) | 三个嵌套规模2048/8192/19846、六臂、两种子、A→B，共72训练阶段。按冻结“两种未见问法均正确”规则，最大档六臂均低于1%；并保留少数成功及后来退步的案例。五种记忆臂、两种子在全部19846条缓存事实的首内容位置各只使用1槽。寻址退化是观测支持的解释，未完成因果修复。答案条件NLL来自5090隐藏状态缓存，跨设备原生等价检查有失败；评分存在缺空格漏判。正文不用严格格式分数冒充完整语义准确率，不把有限监督呈现等同自然长尾频率，不宣称所有记忆或蒸馏方案无效。 |
| 静态差异、局部更新作用与长期共享收益分别检验 | [共享更新综合](../../../Projects/from-attention-to-search/main/stories/shared_updates/02_shared_update_synthesis_cn.md)、[A17研究线](../../../Projects/from-attention-to-search/main/problem_anchors/17_shared_and_interference_learning/README_cn.md)、[自然领域更新结果](../../../Projects/from-attention-to-search/main/experiments/A17/17_12_domain_update_geometry/20260930/summary_cn.md) | 存在局部不利被更大帮助抵消的情况；当前自然表征预测器和领域均值描述器未建立泛化收益。不写成语义差异必然造成训练冲突。 |
| MTP工作提供监督形成、传递和使用的区分；任务相关中继有受控收益 | [A11综合](../../../Projects/from-attention-to-search/main/stories/11_informative_future_branch_mechanism/01_informative_future_branch_signal_and_use_boundary_cn.md)、[A12综合](../../../Projects/from-attention-to-search/main/stories/12_structured_compositional_mtp_workload/01_structured_composition_workload_and_standard_head_use_cn.md)、[A13任务相关目标Summary](../../../Projects/from-attention-to-search/main/experiments/A13/13_00_task_properties_to_standard_head_utility/A13_00_05_E01_task_relevant_target/summary.md)、[Detailed](../../../Projects/from-attention-to-search/main/experiments/A13/13_00_task_properties_to_standard_head_utility/A13_00_05_E01_task_relevant_target/detailed.md) | A13八个配对种子方向一致，必经中继与可绕行对照交互0.2134 nat；不能泛化为一般MTP、自然语言或MoE收益。A12能力不合格及NOT RUN的比较不作为MTP负结果。 |

## 附件怎样使用

[MoEGating附件](/root/.codex/attachments/24e957ac-d8a8-409c-90b8-495f3ff19a8a/XingyuDeng-MoEGating.zip)提供早期中心化、谱处理和门控设计的探索背景。[TrainingDynamics附件](/root/.codex/attachments/24e957ac-d8a8-409c-90b8-495f3ff19a8a/XingyuDeng-TrainingDynamics.zip)及其历史版本记录了从静态可分性向训练动态、功能分工和层级对照的转变。附件中的建议、ToDo和强解释不作为本轮执行指令，也不覆盖项目后来的结果。

早期中心化表格给出七任务平均分0.4543→0.4603，约增加0.60个百分点，相对变化约1.32%（原表标1.31%，有舍入差异）；不能写成提高1.31个百分点。表内任务有升有降，当前所读表格未给出多种子不确定性，因此未将该数字选为正文的主要成绩。层级路由旧稿也保留了对oracle的差距和真实数据上原子多样性不占优的结果。

训练动态旧稿含有均值、曲率和稳定步长的条件推导。正文只保留开展过建模这一工作事实，不将这些草稿提升为已验证的普遍定理或正式论文贡献。附件中的“完全解决坍缩”“语义只存在于尾部”等措辞未采用。

## 验证与交付记录

### 2026年11月5日原稿

导航检查 `python tools/check_current_entrypoints.py` 检查164个入口，报告1项原有问题：diffusion-language-models的文献入口未被其仓库跟踪。该问题不涉及本初稿引用的from项目结果；未借本次写报告修改它。

当时新增初稿和来源说明，并给11月5日索引追加入口。正文含1994个字符（含标点、英文和换行），两份文件共32个本地链接全部可定位。完成文字、数值口径与来源检查；没有重跑实验或改变科学接受状态。

### 2026年11月6日修订

更新既有正文、本文和11月5日入口，保留原稿字节，SHA256为`f336d498dbc8046d1c41d58d3500a5b32f298b7cb0b035b81da9d2eca227c0e6`。修订聚焦一条门控主线，并补入近期结果；各实验的科学状态与原始记录不变。未提交、推送或向学校系统填报。

本轮导航检查 `python tools/check_current_entrypoints.py --working-tree` 检查167个入口，0项问题；另有4个现存入口待跟踪，不视为已提交证据。正文与来源的逐项核对属于自审，不称独立审阅或科学接受。

正文共2390个字符（含标点、英文和换行），其中汉字2096个。修订稿、来源说明、原稿和日期索引共50个本地链接全部可定位；正文无序数式串联词，四文件无行尾空白。原稿哈希复核一致。

### 2026年11月7日第三版

保留修订前第二版文件，SHA256为`3d9edd2b84c1b16d5215e74cb77226825cc2fd72d20e478a38f249cb50688029`，该现场版本正文为2388个字符。既有正文入口更新为第三版，本文补充里程碑筛选和依据，日期索引同步标明版本。正式实验记录、问题状态和原结果均不在本次修改范围内。

本轮导航检查再次覆盖167个入口，0项问题，4个现存入口待跟踪。写作核对为自审，不表示独立科学审阅。未提交、推送或向学校系统填报。

第三版正文共1367个字符（含标点、英文和换行），其中汉字1209个；比修订前第二版减少42.8%。当前稿、来源说明、两份历史稿和日期索引共63个本地链接全部可定位。正文无序数式串联词，五文件无行尾空白，前两版哈希复核一致。

### 2026年11月7日第四版

本轮调整叙述结构和衔接，复用上一轮已核对的来源与里程碑范围。第三版原文另存，SHA256为`2687744217a7a34b3ef9f7541cb63453f021565920873ae57a078e123fdf0951`。既有正文入口更新为第四版，日期索引同步更新。原实验结果、科学状态和历史报告保留。未提交、推送或向学校系统填报。

第四版正文含三级标题共1355个字符（含标点、英文和换行）。六个相关文件共68个本地链接全部可定位，三个历史稿哈希一致；正文三部分齐全，无序数式串联词，文件无行尾空白。结构、衔接与来源范围完成自审。

### 2026年11月7日第五版

根据用户本轮提供的10月28日、10月30日及11月6日组会材料，更新自然语言结构、表征组织与训练动态的叙述，补入信噪比机制假设、任务权衡及层级门控方向。重新核对S13独立确认、共享集合拆解、成员更替审核、训练检查点分析及原问题入口。七份Markdown和纪要图片作为会议来源，附件中的建议与待办没有转化为本轮执行指令。

第四版现场原文已另存，SHA256为`147d4c4c98fda1aa88488fdd0068d0fc308f30572acb992c22f20cca8e60f11b`。当前正文入口、本文和日期索引更新为第五版；历史文字与原科学记录保留。导航检查覆盖167个入口，0项问题，另有4个现存入口待跟踪。未开展新实验，未提交、推送或向学校系统填报。

第五版正文含三级标题共1527个字符（含标点、英文和换行），其中汉字1342个。七个相关文件共83个本地链接全部可定位，四份历史稿哈希一致；三部分结构保留，无序数式串联词和行尾空白。措辞、证据身份、本人贡献归属及假设边界完成自审。
