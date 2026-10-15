# 科研表达修订交付：四个对话、当前正文与保留边界

日期：2026-10-07。处理者：Codex / 当前对话。**本轮只修订技能和文档，未新增实验、改动实验结果或启动/重提GPU作业。**科学问题、阈值、机制和采用判断仍由研究者持有。这是编辑交付记录，不是新Focus、Anchor、Protocol或最终科学报告。

## 1. 权威目录与对话访问

这一节回答“去哪里读、哪个文件负责什么”。四个对话都通过read_thread成功访问；长对话按相关近期轮次和其指向原件核对，没有宣称逐条通读所有历史工具消息。聊天提供定位背景，科学事实回到各自owner与已有执行证据。

| 对话 | 当前材料与职责 |
| --- | --- |
| 1002-自然语言统计规律与更新相容性：两小时研究 | [1002候选目录](../1002/candidates/ntp_representation_update_channels/README_cn.md)。该临时目录仍在，没有迁为正式Focus；Anchor/Protocol持有当时设计与合同，Summary/Detailed持有各次结果，报告/数学说明解释，research_process保留时间线。 |
| 1005-研究学习：从更新作用到共享与路由 | [1005学习指南](../1005/learning_guide_cn.md)。它是派生教学材料，不拥有新结论或批准。1004认识更新与当日总结仍按各自截止点解释。 |
| 1005-路由表征共同学习：梯度反馈对照执行 | [独立临时项目](../../Projects/router-representation-coupling/README_cn.md)。其roadmap→Focus→Anchor→Protocol→Summary/Detailed独立；不是把1002固定更新实验改名。本地此目录没有独立.git，研究职责独立与Git仓库身份不能混用。 |
| 1006-共享还是分开：组会收束与科研掌控 | [唯一组会入口](../1006/meeting_report/meeting_brief_sharing_research_recovery_cn.md)。只负责讲述、解释和备答，不改科学状态。 |

System的[PROJECTS](../../PROJECTS.md)负责导航；既有正式主线仍由[from项目roadmap](../../Projects/from-attention-to-search/main/roadmap.md)指向原Focus。旧0930域更新Summary已通过迁移解析器核实为`Projects/from-attention-to-search/main/experiments/shared_updates/domain_update_geometry/20260930/summary.md`，没有复制第二个可编辑原件。1002→1005学习→1006汇报是派生阅读关系，1002→独立路由项目是另一个获激活问题，均不是自动提升原结果。

代码、数据、权重和收据在`/data/250010109/MoE_Router/experiments/`。当前路由共同均衡条件为`20261006_router_representation_coupling_balanced`；`20261005_router_representation_coupling`保留原零均衡条件。两者不可合成同一实验。更新的训练状态只引用已有10月7日09:33持久化完成记录，没有本轮新测量。

当前对话是唯一写入者。复用三个既有审读代理进行只读核查，没有新建Work/Codex任务。读取时学习/执行对话为idle、1002为notLoaded；这只是该时点的写入检查，另用修改前字节快照避免覆盖已有变化。

## 2. 通用规则改在哪里

这一节回答“下一次怎样复用，避免规则分叉”。

- [report_writing.md](../../docs/report_writing.md)与[中文](../../docs/report_writing_cn.md)集中持有操作性定义、构造/选择/学习状态、比较理由、公式语义、噪声对象和证据边界。
- [markdown_math.md](../../docs/markdown_math.md)仍只管数学源码格式，引用上述公式语义要求。
- [research-reasoning-auditor](../../.agents/skills/research-reasoning-auditor/SKILL.md)与[research-document-explainer](../../.agents/skills/research-document-explainer/SKILL.md)引用同一规范。讲解技能的terminology_contract、experiment_reasoning、explanation_contract同步引用；取消“有Summary就不解释其对象”的歧义，也不把相关研究支线自动设为串行门槛。
- [结果写作契约](../../.agents/skills/experiment-card-writer/references/result_evidence_lineage.md)同步引用规范。research-communication原已引用共享写作规则，引用生效，不复制另一份规则。

原八节Anchor、四部分Summary和审批/执行归属保持。术语表只是辅助，核心操作写在正文及对应公式附近。

## 3. 逐份修改清单

表中每个中英文伙伴均实际修改。共43份报告、数学说明、学习指南和组会正文；另有导航与版本说明。修改关键解释层，保留数值台账、证据链接及完整推导，并非删除后重新编造整份报告。

| 当前文件 | 关键修订 | 验收范围 |
| --- | --- | --- |
| [research_report_cn.md](../1002/candidates/ntp_representation_update_channels/research_report_cn.md) · [EN](../1002/candidates/ntp_representation_update_channels/research_report.md) | 来源更新→真实位移→有限CE；来源/接收角色及SAE工具 | 正文修订；六问自审 |
| [mathematical_analysis_cn.md](../1002/candidates/ntp_representation_update_channels/mathematical_analysis_cn.md) · [EN](../1002/candidates/ntp_representation_update_channels/mathematical_analysis.md) | 精确接口与局部近似；三种随机量；响应预测风险和局部V | 正文修订；六问自审 |
| [source_transfer_addendum_cn.md](../1002/candidates/ntp_representation_update_channels/source_transfer_addendum_cn.md) · [EN](../1002/candidates/ntp_representation_update_channels/source_transfer_addendum.md) | 同域A/B来源迁移；拟合冻结与99.02%的平均范围 | 正文修订；六问自审 |
| [domain_response_structure_cn.md](../1002/candidates/ntp_representation_update_channels/domain_response_structure_cn.md) · [EN](../1002/candidates/ntp_representation_update_channels/domain_response_structure.md) | 四来源去均值对照；相对响应与目标前预测的区别 | 正文修订；六问自审 |
| [capacity_report_cn.md](../1002/candidates/ntp_representation_update_channels/capacity_report_cn.md) · [EN](../1002/candidates/ntp_representation_update_channels/capacity_report.md) | 六臂目的、结构/参数/资源；仅指定条件初始函数匹配 | 正文修订；六问自审 |
| [capacity_mathematics_cn.md](../1002/candidates/ntp_representation_update_channels/capacity_mathematics_cn.md) · [EN](../1002/candidates/ntp_representation_update_channels/capacity_mathematics.md) | 共同模块与专家；合并样本均值；估计MSE/总风险/半平方 | 正文修订；六问自审 |
| [sharing_routing_report_cn.md](../1002/candidates/ntp_representation_update_channels/sharing_routing_report_cn.md) · [EN](../1002/candidates/ntp_representation_update_channels/sharing_routing_report.md) | 总体论证；固定构造/选择/学习状态；噪声与有限样本风险 | 正文修订；六问自审 |
| [sharing_routing_mathematics_cn.md](../1002/candidates/ntp_representation_update_channels/sharing_routing_mathematics_cn.md) · [EN](../1002/candidates/ntp_representation_update_channels/sharing_routing_mathematics.md) | 同一步/固定选择/未来训练各模型；Q/B映射；n=1绝对风险 | 正文修订；六问自审 |
| [probe_33b_summary_cn.md](../1002/candidates/ntp_representation_update_channels/probe_33b_summary_cn.md) · [EN](../1002/candidates/ntp_representation_update_channels/probe_33b_summary.md) | 共同更新/固定选择；FIT拟合；两对照与净采用边界 | 正文修订；六问自审 |
| [probe_33b_detailed_cn.md](../1002/candidates/ntp_representation_update_channels/probe_33b_detailed_cn.md) · [EN](../1002/candidates/ntp_representation_update_channels/probe_33b_detailed.md) | 完整操作；经验ΔCE记账；保留所有设置/数值/来源 | 正文修订；六问自审 |
| [probe_33b_group_summary_cn.md](../1002/candidates/ntp_representation_update_channels/probe_33b_group_summary_cn.md) · [EN](../1002/candidates/ntp_representation_update_channels/probe_33b_group_summary.md) | 为何保留组内使用比例；组别解释与固定基线分开 | 正文修订；六问自审 |
| [probe_33b_group_detailed_cn.md](../1002/candidates/ntp_representation_update_channels/probe_33b_group_detailed_cn.md) · [EN](../1002/candidates/ntp_representation_update_channels/probe_33b_group_detailed.md) | 组内重排的计算对象；保留完整184条件台账 | 正文修订；六问自审 |
| [router_shrinkage_summary_cn.md](../1002/candidates/ntp_representation_update_channels/router_shrinkage_summary_cn.md) · [EN](../1002/candidates/ntp_representation_update_channels/router_shrinkage_summary.md) | 收缩预测分数，不改更新大小；改善原规则不等于胜固定 | 正文修订；六问自审 |
| [router_shrinkage_detailed_cn.md](../1002/candidates/ntp_representation_update_channels/router_shrinkage_detailed_cn.md) · [EN](../1002/candidates/ntp_representation_update_channels/router_shrinkage_detailed.md) | FIT整记录折外拟合/选择；DEV仅评价；不重训专家 | 正文修订；六问自审 |
| [sharing_literature_20261004_cn.md](../1002/candidates/ntp_representation_update_channels/sharing_literature_20261004_cn.md) · [EN](../1002/candidates/ntp_representation_update_channels/sharing_literature_20261004.md) | 定向文献用途与共享对象；保留原版本和配置边界 | 正文修订；六问自审 |
| [cognition_update_cn.md](../1004/cognition_update_cn.md) · [EN](../1004/cognition_update.md) | 匹配与净收益；Adam状态；同域四时点习得/遗忘 | 正文修订；六问自审 |
| [daily_summary_cn.md](../1004/daily_summary_cn.md) · [EN](../1004/daily_summary.md) | 当日固定库认识与截止点；不回填后续事实 | 正文修订；六问自审 |
| [learning_guide_cn.md](../1005/learning_guide_cn.md) · [EN](../1005/learning_guide.md) | 操作与学习目标；公式条件；历史时点；实际习得与遗忘 | 正文修订；全文只读复核 |
| [summary_cn.md](../../Projects/router-representation-coupling/main/experiments/router_representation_gradient_feedback/summary_cn.md) · [EN](../../Projects/router-representation-coupling/main/experiments/router_representation_gradient_feedback/summary.md) | r/h、反向切边与AdamW更新；训练损失/TEST不同 | 当前正文修订；只读复核 |
| [detailed_cn.md](../../Projects/router-representation-coupling/main/experiments/router_representation_gradient_feedback/detailed_cn.md) · [EN](../../Projects/router-representation-coupling/main/experiments/router_representation_gradient_feedback/detailed.md) | 仅重写最新事实解释层；完整日期历史不变 | 当前正文修订；只读复核 |
| [analysis_notes_20261006_cn.md](../../Projects/router-representation-coupling/main/experiments/router_representation_gradient_feedback/analysis_notes_20261006_cn.md) · [EN](../../Projects/router-representation-coupling/main/experiments/router_representation_gradient_feedback/analysis_notes_20261006.md) | 当前完成与旧失败分开；rank/CKA未执行及位移边界 | 当前正文修订；只读复核 |
| [两分钟组会稿](../1006/meeting_report/meeting_brief_sharing_research_recovery_cn.md) | 主讲约两分钟；首先/其次的目的、假设、操作和对照详细备答 | 正文重写；全文只读复核 |

额外修订：1002的README与reading_guide两组中英文入口；1005的README两版；1006的README_cn。1002的research_process两版**只增加历史阅读说明，其时间线原文不改**；路由Anchor两版**只补R1历史条件/A3现行条件的版本辨识并澄清旧措辞，不改八节设计或状态**。每日索引增加本交付链接。逐文件摘要值见[编辑清单](editorial_revision_manifest.json)。

## 4. 关键改前、改后

原文：“当前选择器利用了匹配信息，但采用它仍不如采用强共同动作。”

改后操作说明：先把四领域原始平均梯度等权汇总，再按该实验配方独立缩放，构造一次矩阵更新，简称共同更新。在FIT中测量并比较各候选后，基线选这一类更新给所有DEV位置使用，简称固定选择。候选在评价中不再变化，简称固定候选库。输入相关规则逐位置更换更新，比保留相同使用比例的随机分配损失低，却比这个固定选择损失高。

认识更新：当前输入—更新对应有用，但这套规则未获得替代强固定选择的价值；没有培养不同专家，不能宣布分开学习的长期胜负。“共同”是构造、“固定”是选择、“候选库冻结”是学习状态，三者不互换。

## 5. 更正与澄清的依据

这一节区分措辞修复与科学结果改变。本轮没有无法裁定而被编造的数值；仍未测的量继续未知。

| 原误读风险 | 核对后正文 | 依据与边界 |
| --- | --- | --- |
| 容量均值模型的R可被读成新目标总风险 | R是任务真实均值估计的全平方MSE；m是合并样本均值。独立新观测全平方风险另加σ²，半平方整体除2 | capacity_mathematics原推导及statistical_pooling_round5；公式和0.05/0.10/0.04375不变 |
| 0.5→0.405/0.605称平方损失；g=−Y例也称平方损失 | 两处明确半平方损失；其他确实用全平方的模型保持原定义 | 原公式、scalar_counterexample及conditional-gradient说明；仅更正名称，不改值 |
| n=1共享更好被读成更新改善 | 初始2.5；共享3.5、私有4.0。−0.5是策略差，两者均比初始差；n=4为2.75/2.5、差+0.25 | finite_sample_sharing_checks.json和check_finite_sample_sharing.py；独立新目标总体半平方风险 |
| 同名V/Q被跨文档代入 | 梯度均值差异V、任务均值差异Vδ、有符号响应Vs,d分开；曲率Q对应主报告B，条件动作Qe与预测改善Q不同 | 保留原符号与冻结证据，公式旁给局部对应 |
| 全部六臂都匹配初始函数、全部私有条件都是复制common | 匹配仅指common_parallel/private_active；串行同权重不保证同输出，private_total按总参数设置 | 原Protocol及实现资格记录；不把1个数值资格失败改成科学结果 |
| 两臂r始终相同；优化器直接更新激活r | detach只在同状态同输入下保持数值；梯度改变上游参数，AdamW更新参数后才可能改变下一次前向r | qwen3.py/moe.py/train.py；保持单反馈边干预 |
| 训练尾部CE或计划中的几何可当完成后测 | 训练CE来自更新前batch；TEST/功能未跑；几何只登记有效秩/CKA，capture未实现 | 当前Summary/Detailed、analysis_protocol、analysis_entrypoints；没有新增范数终点 |
| 习得意味着首次学新域，遗忘只能非负 | 同一域留出记录四时点评CE，混合期已见各域；额外集中阶段改善和有符号遗忘分开 | 本容量Protocol；各域4096记录/1,048,576目标的预热事实，不移植到路由项目 |

数学核对是源码/对象一致性核查，不是本轮新增理论、实验发现或渲染认证。

## 6. 六问正文验收

每个主文件均按六问自审；学习/路由当前正文另经只读交叉复核。下面说明回答应落在哪些正文，完整设置和数值仍在原Detailed。没有独立听众实验，不能声称读者理解率已经改善。

| 读者问题 | 当前正文给出的回答 |
| --- | --- |
| 研究对象是什么 | 指定矩阵增量、由它引起的激活位移、预测器系数与持续训练的模块分别定义；每篇注明自身语境。 |
| 实际做了哪几步 | 来源梯度→构造/缩放→原生有限损失→FIT拟合/固定选择→DEV读出，或持续训练的r/h→切边→AdamW→匹配训练记录；未跑后测明确列出。 |
| 为什么这样做 | 各文件Purpose或章节开头给具体疑问、候选解释与对手；纯数学说明给所证明关系或反例要排除的推论。 |
| 对照怎样有意义 | 相同状态/事件/候选控制局部差；使用率与类别内重排分别控制对应/组成；固定选择检验采用；容量/路由资源条件另报。 |
| 改变了什么判断 | 平均帮助不保证逐事件帮助；有匹配不保证净采用；估计量不同不共用“风险”；当前路由训练拟合差不完成机制或泛化结论。 |
| 仍未回答什么 | 长期共享/私有净收益、普遍分离判据、反馈机制归因、独立TEST/功能、研究者资源计价与采用门槛。 |

保留性检查核对原公式、数值表/区间和受保护文件字节；技能结构、数学源码、本地链接与入口检查结果在编辑清单中记录。路径通过不验证科学。

## 7. 推荐阅读顺序

1. [两分钟组会稿](../1006/meeting_report/meeting_brief_sharing_research_recovery_cn.md)第1节；不先读全部历史。
2. 同文件第2.1/2.2节：分别重建“首先”“其次”的目的、假设、操作和对照。
3. [固定库Summary](../1002/candidates/ntp_representation_update_channels/probe_33b_summary_cn.md)，需要解释随机收益时接[组内对照](../1002/candidates/ntp_representation_update_channels/probe_33b_group_summary_cn.md)与[收缩](../1002/candidates/ntp_representation_update_channels/router_shrinkage_summary_cn.md)。
4. [共享主报告](../1002/candidates/ntp_representation_update_channels/sharing_routing_report_cn.md)第4节，以及[学习指南](../1005/learning_guide_cn.md)第7—8节：风险、估计噪声、持续学习与保持。
5. [路由当前Summary](../../Projects/router-representation-coupling/main/experiments/router_representation_gradient_feedback/summary_cn.md)，再按问题查Detailed与冻结协议。训练已完成，后测状态另读，不能从口述稿推运行许可。

## 8. 仍需研究者确认与尚未覆盖

需要研究者确认的科学问题，不是本轮编辑审批：下一步主要收束到直接反馈的净价值，还是长期共享/私有学习；当前最强竞争解释的排序；独立评价结果达到多大差异才值得采用；参数/计算/时间如何计价；什么证据足以支持机制或关闭问题。正文保留Unknown或AI建议，本轮不代选。

明确保留、未全面重写的材料：

- 1002 Anchor/Protocol及history、原始数组、日志、执行收据、图件与checkpoint不重写；research_process只加版本说明。
- 路由的protocol.md、protocol_cn.md、analysis_protocol.md、analysis_protocol_cn.md被原68文件source_lock直接锁定，四者原SHA保持一致；不更新旧锁冒称新训前版本。读者所需操作解释已补进Summary/Detailed/analysis_notes。
- 前序正式from项目（0927/0930的受控干扰、统计、域梯度与表征预测）的原owner是引用依赖，没有扩成本轮整个项目重写。旧路径已核实；其裁决不因新材料更名。
- 外部17篇论文保持10月4日已记录版本和引用，本轮未重新逐篇浏览全文、不做新颖性审计；执行实现只检查了关系到此次澄清的接口/定义，不复算全部原始结果或大权重checksum。
- 四个对话均可访问，没有关键正文因无法访问而留空；完整长期聊天历史未逐条通读。已有材料中论文身份、近重复、预训练重叠仍Unknown，这些是证据边界，不能靠文字编辑消除。
- 两分钟稿441个汉字、498个非空白字符，静态计数不能替代实际计时；需研究者按正常语速排练。个人状态评价未写入报告，旧会话memory保持历史、只追加本轮工作。

未提交、推送、发布或修改Graph；本次文件存在于当前工作区，未跟踪入口如实保留待跟踪提示。
