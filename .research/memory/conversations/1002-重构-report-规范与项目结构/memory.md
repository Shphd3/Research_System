# Conversation Memory: [System]重构Report用语规范以及工作流

Conversation name: [System]重构Report用语规范以及工作流
Processed by: Codex (harness: Codex Desktop; model: gpt-6-astra)
Created at: 2026-10-03 14:23:03 UTC
Latest update at: 2026-10-04 03:36:20 UTC
Continues from: none
Environment: `repo=/data/250010109/Research_System`; `project=/data/250010109/Research_System/Projects/from-attention-to-search`; `exec=/data/250010109/MoE_Router`。本次均可读取。System 与 project 是独立 Git 仓库。

## 2026-10-03 14:23:03 UTC -- 结构重构完成，并复查写作、展示与读取接口

- Summary: 本对话完成了用户授权的本地规则与目录重构，并按后续请求修复写作和阅读接口中的实际问题。目标是让人和 AI 更容易找到原件、理解论证和使用结果，同时减少模板冗余。以下是工作记录；科学判断、批准和状态仍由各自原件持有。

  2026-10-02 的结构重构把 465 个文件迁回合适归属：443 个进入独立项目，22 个进入 daily 的会议位置。System 维护规则与项目入口；项目维护稳定 Focus、Anchor、Protocol、Summary/Detailed 和研究线路；daily 维护会议、短更新与日期索引。没有因开会或跨日期重建 Focus，没有把执行完成变成科研确认。旧路径映射、原始字节哈希和归档位置由迁移清单持有；科学文本仅作导航或路径调整。当时核对了 465 份迁移原件、1,428 份既有研究 Markdown 及 1,133 份受保护的历史、memory、同步和 Graph 文件，结果见当日核验记录。本次复查没有重做这轮全量迁移核验。

  写作规则吸收简明表达和按理解收益选媒介的原则：短句、明确主语、统一术语、先对象后符号，保留条件和结论边界。最终报告不强制十一节；Anchor 八节和 Summary 四部分仍分别承担原有职责。Markdown 持有原件，本地 HTML 是可重建的阅读副本。根 AGENTS、README、PROJECTS 和网页项目提示词没有因本次复查继续膨胀。

  2026-10-03 复查修改了 11 个既有文件。写作侧修正了任务开始模板可能自动创建 daily Focus、无训练分析仍要求训练审计、配图被当作必选、临时综合被最终闭合条件阻断、普通解释被固定栏目束缚等冲突。未确认的下一决定只写一次 Unknown 和未决问题，不机械填空；来源身份仍须核验，但正文按需链接原件或清单，同一范围的边界不反复解释。这些简化没有转移研究者的判断职责。

  接口侧修复了显式 `--source` 意外扩大文档范围、默认选择误用 problem_key 作为目录名、owner 字段遗漏、章节和引用式链接、跨项目来源版本遗漏、同名 ZIP 覆盖，以及同一文件重复读取导致网页/副本/哈希可能不一致的问题。默认包跟随当前 Focus 的明确设计和实验原件；指定来源只加入所列文件、已有语言伴随稿、项目导航和引用小资产。显式历史来源标为“指定来源”。新输出目录和 ZIP 均不得已存在，原始 Markdown 副本保持字节不变；便携跳转使用 index.html。

- Current work: 本轮交付与检查已完成，修改仍在本地，未暂存、提交、推送、发布或外部同步；没有启动实验或修改科学判断。此前同时出现的 1002 候选草稿、其他并行新增内容不属于本次修改范围。

  本轮 46 项测试通过；其中 23 项读取接口测试另在可选 MathML 配置下通过。检查 61 个中英 System/项目入口，无路径问题，35 个入口仍未跟踪；14 个技能的 71 条本地链接通过，3 个修改过的技能包结构校验通过。7 份修改 Markdown 的数学源码检查通过；这不验证数学真值。65 个精选证据资产的载荷检查通过，根仓库无已跟踪生成载荷。两个仓库空白检查通过，并保留已有 Markdown 硬换行。

  已实际生成并浏览默认包（14 份文档、22 个资产）与指定 Summary 包（4 份文档、11 个资产）。桌面和手机宽度、搜索、折叠展开、章节跳转通过；抽查了实际公式与图件显示。默认包有 57 个 MathML 公式和 2 张图片；没有失效内部章节链接、坏图、页面横向溢出、脚本错误或自动外部请求。源码副本、哈希、本地资源链接及默认包 ZIP 内容核对通过。默认包列出 130 条未包含链接，指定包列出 96 条；它们包含未选入、不可访问、工作区外或超出资产范围的依赖，不能统称为坏链。2026-10-02 的 174 条历史不可用引用属于另一轮、更广的审计范围，不与本轮数字合并。

  两份合成输入下的实际试写，经受指导修订后分别从 2,579/3,481 个字符缩短到 1,393/1,802 个字符，保留面板内描述、不可外推总体或迁移、没有重跑模型以及人工判断与下一决定的不同 Unknown。复查还修正了试写把“迁移未验证”升为固定面板答案闭合条件的范围扩张；不是新增规则或新的研究发现。试写材料有 synthetic 标记，仅验证工作流可用性；不是项目证据，也不是独立读者理解测试。

  读取限制仍显式保留：无渲染依赖时显示源码；不支持的公式保留 TeX；执行数据和历史资料不递归复制。源文件、结构、浏览器和合成试写检查不能证明所有研究论证正确或所有读者都能理解。网页和本地核验材料位于被忽略的 runtime，单独克隆 System 不会带入这些产物或独立项目。

- Next action: 本轮无待办。后续按用户指定来源继续；未指定时从项目 roadmap 选择所需 owner，再处理具体问题。若另行请求提交或推送，先分别检查 System 与项目的实际差异、精选载荷和远端状态；当前记录不授权发布或新实验。读取旧引用可用 `tools/research_paths.py`，不要建立第二份可编辑原件。

- References:
  - [PROJECTS](../../../../PROJECTS.md)、[项目 roadmap](../../../../Projects/from-attention-to-search/main/roadmap_cn.md)：项目选择与当前研究线路；不是结果账本。
  - [当前默认 Focus](../../../../Projects/from-attention-to-search/main/focus/focus_domain_update_geometry.md)、[对应 Summary](../../../../Projects/from-attention-to-search/main/experiments/shared_updates/domain_update_geometry/20260930/summary_cn.md)：核验当前科学问题和判断的原件入口；memory 不重述其结论。
  - [重构交付说明](../../../../docs/research_refactor_20261002_cn.md)、[当日核验](../../../../docs/research_refactor_20261002_validation.json)、[迁移清单](../../../../docs/research_locations.json)：465 个文件的归属、精确旧新路径、身份和上一轮检查范围。日期记录不被本轮计数覆盖。
  - [写作规则](../../../../docs/report_writing_cn.md)、[技能导航](../../../../docs/skills.md)、[目录规则](../../../../.agents/skills/research-mainline/references/layout_and_naming.md)、[Focus 周期](../../../../.agents/skills/research-progress-core/references/focus_cycle.md)、[沟通技能](../../../../.agents/skills/research-communication/SKILL.md)：上轮规则重构与角色分工的现行来源。
  - [任务开始模板](../../../../templates/research_process/task_start_template.md)、[完成回复](../../../../.agents/skills/experiment-card-writer/references/plain_language_completion_reply.md)、[结果证据契约](../../../../.agents/skills/experiment-card-writer/references/result_evidence_lineage.md)、[解释契约](../../../../.agents/skills/research-document-explainer/references/explanation_contract.md)、[最终报告技能](../../../../.agents/skills/research-final-report/SKILL.md)：本轮写作修订。
  - [跨仓库读取说明](../../../../docs/project_access_cn.md)、[阅读包工具](../../../../tools/build_reading_bundle.py)、[路径工具](../../../../tools/research_paths.py)、[入口检查](../../../../tools/check_current_entrypoints.py)、[接口测试](../../../../tools/tests/test_research_access.py)：本轮接口行为与回归。
  - [本轮核验清单](../../../runtime/validation/20261003_writing_access/review.json)：11 处修改的前后哈希、浏览器结果、合成试写与边界；同目录保留截图、输入和输出，均为本地产物。
  - [默认阅读页](../../../runtime/reading/20261003_writing_access/index.html)、[便携 ZIP](../../../runtime/reading/20261003_writing_access.zip)、[指定 Summary 阅读页](../../../runtime/reading/20261003_writing_access_explicit/index.html)：重新生成并验证过的派生交付，不是新科学原件。

## 2026-10-04 02:57:11 UTC -- 按用户要求改为完整文字交付

Processed by: Codex (harness: Codex Desktop; model: gpt-6-astra)

- Summary: 用户说明可能无法使用网页查看，要求取消网页这一项并把文字规范做好。已将研究交付改为可独立阅读的 Markdown：开头给问题、有边界的回答和证据状态；按理解顺序展开；公式解释目的、符号、条件和含义；结果写清对象、基线、指标、关键数值与不确定性；图件发现写入正文；证据链接用于核查，长文通过标题与文件路径导航。规则是内容要求，不增加固定栏目或重复说明。此前目录归属、稳定 Focus 和科学判断边界继续有效。
- Supersedes: 上一条记录中的“本地 HTML 阅读副本”和“便携跳转使用 index.html”不再是现行交付方式。现行依据是 [文字规范](../../../../docs/report_writing_cn.md)、[读取说明](../../../../docs/project_access_cn.md)、[沟通技能](../../../../.agents/skills/research-communication/SKILL.md) 与[最终报告技能](../../../../.agents/skills/research-final-report/SKILL.md)。旧网页及其核验保留为历史产物，不再作为本轮阅读入口。
- Current work: 修改完成。根与项目 AGENTS、README、技能导航、会议规则及中英写作/读取说明已同步。阅读工具改为 Markdown 包，删除 HTML/CSS/JavaScript 生成和可选排版依赖；`README.md` 给出阅读顺序和路径，`documents/` 只调整链接并附来源，`sources/` 保留原始字节，`UNAVAILABLE.md` 列出缺失或未选入来源，manifest 记录版本和两类哈希。正文与公式内容不被工具重写。仅用 Python 标准库即可生成。

  47 项测试、61 个工作区入口、14 个技能的 71 条链接和 2 个技能包结构检查通过；31 个入口仍未跟踪。4 份修改文稿的数学源码检查通过。实际默认包为 14 份文档、22 个资产，记录 130 条未包含引用；另生成写作规范包检验指定来源范围。两包共 441 个本地链接目标可达，原件/阅读副本哈希与 ZIP 一致性通过，没有生成 HTML 文件。检查是代码、结构与文字自审，不是科学正确性或独立读者理解实验。现有历史文稿不会因打包自动补足解释，后续写作按新规则执行。本轮未提交、推送或启动实验；未改动科学原件内容。
- Next action: 直接使用 Markdown 原件或下面的新文字阅读入口；本轮无待办。后续按指定来源完成文字写作，不自动恢复网页交付。提交、推送与运行仍按独立请求和原件授权处理。
- References:
  - [根规则](../../../../AGENTS.md)、[项目规则](../../../../Projects/from-attention-to-search/AGENTS.md)、[技能导航](../../../../docs/skills.md)、[会议规则](../../../../.agents/skills/research-communication/references/meeting.md)：交付方式的一致入口。
  - [文字规范](../../../../docs/report_writing_cn.md)、[读取说明](../../../../docs/project_access_cn.md)：现行写作与使用要求；各自链接英文伴随稿。
  - [打包工具](../../../../tools/build_reading_bundle.py)、[路径工具](../../../../tools/research_paths.py)、[回归测试](../../../../tools/tests/test_research_access.py)：Markdown 副本、原始身份、范围和可移植链接行为。
  - [文字阅读入口](../../../runtime/reading/20261004_markdown/README.md)、[文字包 ZIP](../../../runtime/reading/20261004_markdown.zip)、[核验记录](../../../runtime/validation/20261004_markdown/review.json)：本地派生产物及边界，不替代研究原件。


## 2026-10-04 03:25:16 UTC -- Karpathy 简明表达核对、6.1 Sol 实测与发布检查

Processed by: Codex (harness: Codex Desktop; model: gpt-6-astra); writing checks: gpt-6.1-sol

- Summary: 用户确认所指的是 Karpathy 的文字建议，要求核验 6.1 Sol 能否使用这套规范，并授权提交、推送当前更改及全部暂存内容。对话已按请求更名为 `[System]重构Report用语规范以及工作流`，经 App 列表复核；同一对话的 memory 路径保持稳定。现行规范采用短句、明确主语、统一术语、按理解顺序解释的原则，保留研究条件和不确定性；不宣称符合 ASD-STE100 全部标准。用户此前选择纯文字交付继续有效。
- Current work: 规则修订与本轮范围内检查完成。研究推进报告明确连接“目的→观察→假设→模型与分阶段推导→检验→阶段认识更新”，每阶段交代输入、关系、输出和依据。结果分析解释测量、比较与有效性，结论回答理解怎样改变。简单任务不必另建模型或实验；数值模型、证明、反例和观察性研究保留各自证据边界；缺口不靠编造补齐，研究者判断仍由原件持有。

  实际指定 gpt-6.1-sol 完成六份合成写作。首轮四份中发现一项实质失败：Summary 把固定题集目的扩大为迁移假设。已在共享规范和结果契约中限定假设须保持原问题范围。修订后由新会话生成固定题集 Summary 与分阶段模型报告，两份经另一个审阅代理检查通过；有限步算术另行精确复算。原失败产物保留，不能把本轮写成六份初次全部通过。这是少量指定任务的可用性检查，不是通用模型保证、真实研究结果或人类理解效果实验。

  47 项单元测试、61 个 System/项目入口、14 个技能的 72 条本地链接、4 个修改技能包结构和 7 份变更文稿的数学源码检查通过。项目发布审计覆盖 544 个候选文件，65 个精选资产及 465 个迁移文件的来源身份全部匹配；84 个既有科学文稿只调整链接或登记路径，没有科学正文改写。System 已有本地提交及新增载荷另作检查，未发现本轮扫描范围内的发布阻碍。测试与路径检查不证明科学结论。

  System 与独立项目按用户授权分别提交推送；本条随规则提交，实际完成状态与提交身份以两个仓库 Git 记录和远端核对为准，不由 memory 自行证明。发布检查开始后，另一个仍 active 的研究对话继续修改 1002 候选报告；其未完成工作保留在工作区，不主动暂存到本次 System 提交。未启动实验、改写 Graph、批准机制结论或关闭问题。
- Next action: 本轮规则修改无待办。后续直接使用现行文字规范；对模型输出仍按来源检查问题范围、算术和推理，不能由本轮样例通过推断未来输出必然正确。恢复发布操作前先核对分支和远端，不重复提交或覆盖并行工作。
- References:
  - [现行文字规范](../../../../docs/report_writing_cn.md)：简明表达、六段论证关系、结果分析与结论的职责；链接英文伴随稿和 Karpathy/STE 来源。
  - [结果证据契约](../../../../.agents/skills/experiment-card-writer/references/result_evidence_lineage.md)、[完成回复](../../../../.agents/skills/experiment-card-writer/references/plain_language_completion_reply.md)：原问题范围和认识更新。
  - [结果解释](../../../../.agents/skills/research-progress-core/references/result_interpretation.md)、[阶段 Story](../../../../.agents/skills/research-communication/references/story.md)、[最终报告技能](../../../../.agents/skills/research-final-report/SKILL.md)：相同论证关系在不同文档中的使用，未改变科学权限。
  - [Sol 实测核验](../../../runtime/validation/20261004_language_portability/review.json)、[修订后产物审阅](../../../runtime/validation/20261004_language_portability/final_output_audit.json)：本地合成输入、六份输出、失败与修复、规则版本、检查边界。runtime 不随 Git 发布。
  - [文字包核验](../../../runtime/validation/20261004_markdown/review.json)、[读取说明](../../../../docs/project_access_cn.md)：无网页依赖的接口及范围。
  - [迁移身份清单](../../../../docs/research_locations.json)、[项目精选载荷](../../../../Projects/from-attention-to-search/main/curated_evidence.json)：项目重构发布所需的来源身份，不是科研确认。


## 2026-10-04 03:36:20 UTC -- 暂存范围核对与项目推送完成

Processed by: Codex (harness: Codex Desktop; model: gpt-6-astra)

- Summary: 项目重构已提交并普通推送到 `BinaryCheater/from-attention-to-search` 的 `Xingyu` 分支，提交为 `0959b841cb82997f8c845b3e871a0d978cf36db4`。544 个提交文件均与审计快照逐字节一致。自动审批最初因目的地授权不够明确拒绝推送；用户随后明确批准这个提交、544 个文件和该分支，之后推送成功。此授权只涉及发布，不涉及科学确认或实验。
- Current work: System 本轮 19 个文件已完成暂存和核验，本条随规则一并提交；System 远端 `Shphd3/Research_System` 经 GitHub 连接核实为当前账号管理的私有仓库，具备写入权限。实际远端完成状态以 `origin/master` 与本条所属提交的核对为准。另一个活跃对话的 1002 报告仍留在工作区，未混入此次暂存。

  最终入口检查的精确边界是：61 个工作区入口均可达，60 个已跟踪；diffusion-language-models 的一个既有文献入口未跟踪，该独立仓库无远端，未在此任务初始化提交或建立远端。故全局严格跟踪检查仍报告这一项，不能记为全部通过。其余 47 项测试、技能与载荷检查通过。项目暂存空白检查有 5 处文末空行提示；允许 Markdown 硬换行和文末空行后通过，原件内容保留不动。
- Next action: 本轮内容修改无待办。恢复时先核对两个既有远端；不要重复推送已完成的项目提交。diffusion 项目的远端、并行报告和其他独立仓库未暂存工作不由本条创建发布状态或科学授权。
- References: [发布与检查记录](../../../runtime/validation/20261004_language_portability/review.json)、[现行文字规范](../../../../docs/report_writing_cn.md)、[项目导航](../../../../Projects/from-attention-to-search/main/roadmap_cn.md)。运行记录在本地 runtime，Git 提交与远端是发布状态的核验来源。
