# Conversation Memory: 0911-astra-deepseek执行规划

Conversation name: 0911-astra-deepseek执行规划
Processed by: DeepSeek (harness: DeepSeek Harness; model: deepseek-flash)
Created at: 2026-09-11T14:48:00Z
Latest update at: 2026-09-11T16:42:05Z
Continues from: .research/memory/conversations/0910-memory-system-improvement/memory.md
Environment: container /data/250010109 (`repo`=Research_System, `exec`=MoE_Router);
  this record was written from the Windows checkout
  C:\Users\250010109\data\Research_System, where `repo` is readable but `exec` and
  /root/** are not-visible. /data is a network mount (quarkfs_client); /root/** is
  container-local and lost on recycle.
Continuation: continuation.md in this record directory is the CURRENT entry point
  for the system-level (memory and handoff) workstream.

## 2026-09-11T14:48:00Z -- 记忆与交接架构第三轮改造；两仓库同步；SFT 入口文档合并

- Summary: 本对话把研究系统的「跨会话交接」从口头约定改成可执行架构，并同步了两个仓库。四项研究员确认的决定：(1) 嵌套仓库拓扑没问题，规范材料在嵌套仓库中可以接受；(2) `researchctl check` 在本机跑不了，忽略；(3) 整合只在研究者显式请求时发生，**不定时、无到期信号、无阈值触发**；(4) 续接文档放在 `conversations` 中，**每个 conversation 一份**；某 conversation 没有当前工作时不需要续接文档。已落地的改动：
  - **契约（`.agents/skills/research-memory/references/memory_contract.md`，208+ 行）新增三件**：`Environment:` 头部字段与规则（根不可读＝**不可核验**，不是过期；**不得静默丢弃**）；**P2** 涉及规范工件改动的检查点必须在 `References`/`Supersedes` **只指向、不复述结论**；**P3** 整合仅显式请求、须保留未解决不确定性/负结果/未作废决定/`Created at`；并承认 `continuation.md` 为 record 目录内的合规操作工件与工作流交接入口。
  - **两仓库同步**：外层 `2553473 → 799bd23`；嵌套 `113411f → c2fc628`（22 个提交，取回 A15/E20/E21/`15_13_11` anchor）。两仓库**领先 0**，为干净快进——**未删除任何目录**。
  - **SFT 入口合并**：5 份互相指认的入口文档合并为唯一 CURRENT 续接文件 `.research/memory/conversations/0910-sft-matrix-execution/continuation.md`（A–H 段，含新增 **H 可复用资产**）；5 份原件**原位标 SUPERSEDED、内容一字未删**。`sft_audit_postrun_brief_cn.md` 未标——它是审计入口，列为 H 段可复用资产。
  - **存量清理**：9 条记忆记录**全部**补上 `Environment:`；`0910-sft-matrix-execution/memory.md` 整合 **16.3 KB → 13.6 KB**（仅去重：删已修复的 5 个绘图缺陷清单、训练动态逐通道数值改为指向读面、已被下一检查点取代的渲染计数；原文可在 commit `bcadd93` 复原）。
  - **模板**：新增 `templates/research_process/{continuation_brief_template, daily_theme_log_template, astra_input_template}.md`。
- **测量更正（重要，防再次误判）**：初版普查报「122 条引用 87% 缺失」是**错的**，三个测量错误叠加——① Windows **MAX_PATH 260** 使 `Test-Path` 对 262 字符路径假阴性；② 控制台编码把中文文件名显示成乱码；③ 把「相对片段」（如 `S1/`、`S6/registered_verdict.json`）当成独立路径。**更正后的真实结论**：**30 条绝对容器路径（`/data/...`、`/root/...`）在本机 0% 可解析**；**19 条仓库相对路径 100% 可解析**；73 条相对片段不可独立判定。即：仓库侧交接本来是好的，是容器绝对引用把它淹没了——这正是 `Environment:` 字段要解决的问题。长路径检查须用 `\\?\` 前缀（`[System.IO.File]::Exists`）。
- **Git 环境事实（本机）**：`gh` 2.96.0 已装但**未登录**；Windows 凭据管理器**已有** `git:https://github.com`（用户 Shphd3），故**不需要 gh 登录**；git 默认 `http.sslBackend=schannel` **TLS 握手失败**（`SEC_E_NO_CREDENTIALS`），已在**两个仓库内设 local `http.sslBackend=openssl`** 修复（全局配置在沙箱外，写入被拒；机器上其它仓库仍是 schannel）。沙箱禁止凭据助手 GCM 的管道 stdio，**每次 git 联网操作都需一次 full-access 升级**。
- Current work: 本轮编辑已全部落盘并验证（9/9 有 `Environment:`；模板 6 个；无残留旧路径）。无未完成事项。
- Next action: ① 研究员审核本轮改动；② 研究员指出 **`current` 具体指哪个工件**（`PROJECTS.md` 的 `Current Focus Priority` 段，还是新建独立文档），确认后才可把「研究者拥有 current、AI 只读」写成 `AGENTS.md` 正式规则；③ 按 `templates/research_process/daily_theme_log_template.md` 建每日主题文档；④ 推送需研究员**明确批准**。
- References: `AGENTS.md`（治理与状态归属表）；`.agents/skills/research-memory/references/memory_contract.md`（本轮契约改动本体）；`templates/research_process/{continuation_brief_template,daily_theme_log_template}.md` 与 `prompts/project_instructions/astra_input_template.md`（固定输入模板）；`.research/memory/conversations/0910-sft-matrix-execution/continuation.md`（真实续接文件范例）与同目录 `memory.md`（本轮整合对象）；`docs/execution_envelope.md`（执行信封，与本工作流无科学关系，仅在需要判断资源时读）。本记录非 canonical；科学判决仍由 researcher 拥有。

## 2026-09-11T16:42:05Z -- 模板与工作流再整理；回执改名；Focus 重写；current 取消

- Summary: 研究员确认后完成五组改动。**对上一轮条目的更正（注记，非静默改写）**：`templates/research_process/daily_theme_log_template.md` 已删除，`templates/research_process/astra_input_template.md` 已移出到 `prompts/project_instructions/`；上一轮条目中这两条路径引用已失效。研究员本人的决定（2026-09-11）：(1) meeting 模板不再需要，完全删除；(2) ACP 运行回执确实需要，但改名以消歧义；(3) **`current` 与 `Focus` 不区分，不再新增 current 文件**——Focus 本身就是「我们现在要解决的科研问题」，而它本来就住在 `daily_research_reports/MMDD/`；(4) 参照 `Projects/research-exploration-skill` 的写法改写 Focus；(5) `summary.md` 有中文伴随件 `summary_cn.md`；(6) Astra 模板移出 `templates/`。改动清单：
  - **回执改名**：`templates/execution/run_receipt_template.md` → **`execution_certificate_template.md`**（与 `acp_receipts/` 的提交回执、`<run>/submissions/pt-*.json` 的平台回执区分）。同步 4 处：`docs/execution_envelope.md` §1 与 §5（并在 §5 补一句「平台提交回执是另一回事，它只证明提交被接受，不证明跑了什么」）、`templates/README.md`、`templates/execution/acp_submit_template.sh`。
  - **meeting 模板删除**：删 `templates/meeting/{meeting_focus,meeting_outline}_template.md` 与空目录；同步 `templates/README.md`（移除 2 行、补登 `continuation_brief_template.md`）与 **`.agents/skills/research-communication/references/meeting.md`**（改为「直接用 Focus + 四段式 Summary 组稿，不设模板」）。**上一轮的 grep 漏掉了这个 skill 引用**（未扫 `.agents/`），本轮改用 `Select-String` 显式复查，确认全仓无悬空引用。
  - **Focus 重写**：`templates/research_process/focus_writing_template.md` 改为 7 节（核心问题与边界 / 可证伪预测与最强竞争解释 / 允许与禁止的信息 / 本轮实验只列不展开 / 轮次滚动摘要 / 待研究者决定 / 本轮总结论）+ **5 条显式 FAIL 自检**。四段式细节归 `protocol.md`（执行前）与 `summary.md` + `summary_cn.md`（执行后）；完整轮次记录归 `detailed.md`；Focus 只保留由 `detailed.md` **压缩**而来的滚动摘要，**同一轮次历史两处重复 = FAIL**。同步：`AGENTS.md` 的 Focus 不变量、Formal Experiments 段、Result Reading 段、State Ownership 表（加 `summary_cn.md`；`docs/execution_envelope.md` 行改「execution-certificate」），以及 `.agents/skills/research-progress-core/references/focus_cycle.md`。
  - **`PROJECTS.md` 降为低频文件**：首行定义由「Current-state registry」改为「Project map and decision registry」并加 **Environment 环境根**；**移走 `## Current Focus Priority` 整段**（4,185 字符）到 `daily_research_reports/0911/0911_PROJECTS_current_focus_priority_archive_cn.md`（原文归档，信息不丢）。改动用 **LF 保持**的精确替换完成，未做整文件重写（该文件 LF-only、无 BOM）；`git diff --stat` 为 18 增 / 24 删，范围精确。
  - **命名对齐**：`daily_research_reports/0910/docs/sft_matrix_postrun_analysis_plan_cn.md` 的 `summary_zh` → **`summary_cn`**（2 处）。
  - **模板移位**：`templates/research_process/astra_input_template.md` → `prompts/project_instructions/`（该目录按 `prompts/README.md` 就是放可复用 web 侧 prompt）；删除 `daily_theme_log_template.md`（current 取消后无调用者）。
- **参照来源与取舍**：`Projects/research-exploration-skill/.codex/skills/research-exploration/SKILL.md`（311 行）。**只取三个机制，不整套照搬**（避免过度复杂）：① 每轮六段式读面，且 `NOT RUN` 也算**完整**一轮——这正是「每天完成一个完整推进」的机制；② 关闭时证据压缩、禁止两处重复；③ 契约带显式 `FAIL` 条件。该仓库已拉取 `08b6a24 → 0963fe5`（9 个提交），正是 `docs/skills.md` 记载的适配基线。
- Current work: 上述改动已全部落盘；待提交与推送。
- Next action: ① 提交并推送外层仓库（含研究员本人那 1 行 0907 改动）；② 嵌套仓库 `Projects/from-attention-to-search` **ahead 0 / behind 0，无内容可推**；③ 推送后按需把本次整合写进 daily report。
- References: `.agents/skills/research-progress-core/references/focus_cycle.md` 与 `templates/research_process/focus_writing_template.md`（Focus 新规）；`AGENTS.md`（Focus / Result Reading / State Ownership 三处）；`PROJECTS.md` 与 `daily_research_reports/0911/0911_PROJECTS_current_focus_priority_archive_cn.md`（迁出与归档）；`docs/execution_envelope.md` 与 `templates/execution/execution_certificate_template.md`（回执改名）；`Projects/research-exploration-skill/.codex/skills/research-exploration/SKILL.md`（写法来源）。本记录非 canonical；科学判决仍由 researcher 拥有。
