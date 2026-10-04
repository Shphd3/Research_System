# Conversation Memory: 1002-重构 report 规范与项目结构

Conversation name: 1002-重构 report 规范与项目结构
Processed by: Codex (harness: Codex Desktop; model: gpt-6-astra)
Created at: 2026-10-03 14:23:03 UTC
Latest update at: 2026-10-03 14:23:03 UTC
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
