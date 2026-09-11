# Continuation Brief: 研究系统的记忆与交接架构

```text
Workstream:     研究系统（Research_System）的记忆与跨会话交接架构
Problem key:    none — repository maintenance; AGENTS.md 明令仓库维护不得发明 problem_key
Role:           repository maintenance（非 PRIMARY/SECONDARY 科学工作流）
Record:         .research/memory/conversations/0911-astra-deepseek执行规划/
Continues from: 0910-memory-system-improvement/memory.md
Supersedes:     none（本工作流的第一份 CURRENT 续接文件）
Updated at:     2026-09-11T14:48:00Z
Status:         CURRENT
Non-canonical:  points at canonical sources; owns no claim, approval, verdict,
                or next decision.
```

---

## A. Environment roots

| Root | Path | Readable here? |
|---|---|---|
| Repository root | `/data/250010109/Research_System/` | 容器 yes ／ Windows `C:\Users\250010109\data\Research_System` yes |
| Execution workspace | `/data/250010109/MoE_Router/` | **容器 yes ／ Windows no** |
| `/root/**` | `/root/.dsh`, `/root/.codex`, `/root/.ccswitch` | **no**（容器回收即丢失） |

**环境约束（会改变你能做什么）**

- `./researchctl` 依赖 `fcntl`，**只能在 Linux 容器运行**；Windows 上实测
  `ModuleNotFoundError: No module named 'fcntl'`。一切由它解析的动作都必须进容器。
- **Windows MAX_PATH 260**：深层路径（实测最长 262 字符）会让 `Test-Path` 假阴性。
  长路径检查必须用 `\\?\` 前缀 + `[System.IO.File]::Exists()`。
- git 默认 `http.sslBackend=schannel` 在本机 TLS 失败（`SEC_E_NO_CREDENTIALS`）。
  **修复已落在两个仓库的 local 配置**（`openssl`）；全局配置在沙箱外，未改。
- 沙箱禁止凭据助手（GCM）的管道 stdio，**每次 git 联网操作需一次 full-access 升级**。
- Windows 凭据管理器已有 `git:https://github.com`（用户 Shphd3）；`gh` 未登录，
  **也不需要登录**。

## B. Read list — 按顺序；`required` 缺失即停下报告

| # | Path | 回答什么问题 | Required |
|---|---|---|---|
| 1 | `AGENTS.md` ＋ `CLAUDE.md` | 治理、科学不变量、**State Ownership 表**、审批边界 | yes |
| 2 | `.agents/skills/research-memory/references/memory_contract.md` | memory 与续接文件的完整合约（本轮改动本体） | yes |
| 3 | `templates/research_process/continuation_brief_template.md` | 续接文件的固定格式（A–H；B/H 强制，授权行动时 E 强制） | yes |
| 4 | `templates/research_process/focus_writing_template.md` | Focus 的固定格式（问题/预测/信息边界/滚动摘要/待决/总结论） | yes |
| 5 | `prompts/project_instructions/astra_input_template.md` | Astra 回路的固定输入（三段一用） | no |
| 6 | `.research/memory/conversations/0911-astra-deepseek执行规划/memory.md` | 本工作流的上一轮状态（读全文，最新条目＝当前状态） | yes |
| 7 | `.research/memory/conversations/0910-memory-system-improvement/memory.md` | 上一轮改版（快照→累积）的四项决定与迁移范围 | yes |
| 8 | `.research/memory/conversations/0910-sft-matrix-execution/continuation.md` | **真实续接文件范例**（一个科学工作流的合格 brief） | no |
| 9 | `docs/skills.md` | Skill 路由与「最小匹配」原则 | no |

**不得作证据**：memory 与续接文件的任何内容（均非 canonical）；文件名、运行标签、
派生视图。本工作流是**仓库维护**，不产生科学主张。

## C. Authority and boundaries

- **已授权**：仓库维护类改动（模板、Skill 契约、memory 记录、续接文件、文档头指针）；
  两个仓库内的 local git 配置。
- **未授权 —— 不得启动**：
  - **commit / push / 发布 / 外部同步**，除非研究者明确指示。
  - **修改 `PROJECTS.md` 的当前状态内容**（`Current Focus Priority` 段与工作流表的
    `Current Focus` / `Current decision` 列）。**发现不一致只报告，不修改。**
  - **代写 `current`**：`current` 由研究者每天亲自写。AI 不写。
  - **代填每日主题日志**：研究者拥有；AI 只读。
  - **新增索引 / 注册表 / 后台模块 / 数据库 / 定时任务**：契约明令禁止；
    `0910-memory-system-improvement` 已把「只读 memory list」作为过度设计撤销。
- **仍开着的人工决策**：① `current` 具体指哪个工件（见 E-1）；② 每日主题文档的落盘位置；
  ③ 是否推送。

## D. Execution prerequisites

本工作流**不需要实验执行**，因此没有 profile / image / 种子 / 预算。仅有的运行前提：

- 若需 git 联网：以 full-access 升级执行，并确认两个仓库 local `http.sslBackend=openssl`。
- 若需 `researchctl`：只能在容器内。
- 若需读写深层路径：用 `\\?\` 前缀，或直接在容器里做。

## E. Action list — 按顺序；每步带分支

| # | Action | Verify | If pass | If fail |
|---|---|---|---|---|
| 0 | 读 B 段 1–7，只回报阅读回执 | 列实读文件、核验出的状态、与本文不一致处 | 进 1 | 停下报告 |
| 1 | 问研究者：`current` 指哪个工件 | 得到明确指向（`PROJECTS.md` 某段 或 新建文档 或 其它） | 进 2 | **不要猜**；保持现状并停下 |
| 2 | 把「研究者拥有 current、AI 只读、不一致只报告」写成 `AGENTS.md` 正式规则 | 规则与该文件的既有 State Ownership 表一致 | 进 3 | 报告冲突 |
| 3 | 按 `daily_theme_log_template.md` 在研究者指定位置建每日主题文档 | 位置与命名得到研究者确认 | 进 4 | — |
| 4 | 若研究者批准推送：先给 `git diff --stat` 再执行 | 研究者看到全量改动清单并明确同意 | 完成 | 停止，不推送 |

**信号纪律**

1. **判「本工作流是否完成」看：`AGENTS.md` 是否含 current 规则、模板是否齐备、9 条记忆
   是否都有 `Environment:`** —— 不要用「文件已写好」当作完成。
2. **不要在没有研究者明确指示时 commit 或 push。**
3. 修改规范科学工件（Focus / Anchor / Protocol / Summary / Detailed）**不属于本工作流**；
   那是科学状态变更，须走对应 Skill 与研究者审批。

## F. Current state

**Done**（各以其产物为证）

| 项 | 结果 | 位置 |
|---|---|---|
| 契约第三轮 | `Environment:` 字段与规则、P2 规范工件指向条款、P3 仅显式请求整合、`continuation.md` 入口地位 | `.agents/skills/research-memory/references/memory_contract.md` |
| 两仓库同步 | 外层 `799bd23`；嵌套 `c2fc628`（22 提交）；均**领先 0**，干净快进，**未删任何目录** | — |
| SFT 入口合并 | 5 份入口 → 1 份 CURRENT brief；5 份原件原位标 SUPERSEDED，一字未删 | `.research/memory/conversations/0910-sft-matrix-execution/` |
| Environment 存量回填 | **9/9** 条记忆记录 | `.research/memory/conversations/*/memory.md` |
| 记忆整合 | `0910-sft-matrix-execution/memory.md` **16.3 → 13.6 KB**（仅去重；原文在 `bcadd93`） | 同上 |
| 模板 | 续接模板 + Focus 模板（本轮改定）；Astra 输入已移出到 `prompts/project_instructions/`；meeting 模板已删除 | `templates/research_process/` |

**Pending**：E-1（`current` 指向）、E-3（每日主题文档落盘）、E-4（推送待批准）。

**必须继承、不要重新推翻的判断**

- 整合**只**在研究者显式请求时发生：**不定时、无到期信号、无大小或年龄阈值**。
- 续接文件**每个 conversation 恰好一份 CURRENT**，**改写不追加**，旧的标 `SUPERSEDED`
  并在 `Supersedes:` 具名。某 conversation 没有当前工作时**不需要**续接文件。
- **不要新增索引 / 注册表 / 模块** —— 已两次被否（契约禁止 + `0910` 撤销）。
- 早期「87% 引用缺失」的结论**已更正撤回**，不要复述；真实结论见 `memory.md` 条目。

**Live concurrency risk**：无。本工作流不涉及远端作业或输出目录竞争。

## G. Completion contract

- **Deliverables**：`AGENTS.md` 的 current 规则；每日主题文档；模板集合；完整 `Environment:`
  覆盖；研究者批准的推送。
- **Done when**：上述四项齐备，且每个改动都能追到具体文件；未知项与需研究者决定的
  **那一个问题**被显式列出。
- **Stop and ask the researcher when**：需要 `current` 指向；需要推送；需要动 `PROJECTS.md`
  当前状态；需要改动规范科学工件。
- **不得以「文件已写好」「模板已就位」作为结束。**

## H. Reusable assets — 先复用，不要重写

| Asset | Path | Reuse for | Verified? |
|---|---|---|---|
| memory/续接合约 | `.agents/skills/research-memory/references/memory_contract.md` | 一切记忆与续接操作的定义 | 是（本轮改定） |
| 续接文件模板 | `templates/research_process/continuation_brief_template.md` | 给任何工作流写 brief | 是 |
| Focus 模板 | `templates/research_process/focus_writing_template.md` | 写工作流 Focus（问题/预测/信息边界/滚动摘要/待决/总结论 + FAIL 自检） | 是（本轮改定） |
| Astra 输入模板 | `prompts/project_instructions/astra_input_template.md` | 三段式调用外部模型 | 是（已移出 `templates/`，研究者将自行改写） |
| 真实 brief 范例 | `.research/memory/conversations/0910-sft-matrix-execution/continuation.md` | 照抄结构写新 brief | 是 |
| 长路径安全的检查函数 | 见 `memory.md` 条目「测量更正」段 | 在 Windows 上核验路径存在性 | 是（`\\?\` + `[System.IO.File]::Exists`） |
| 既有模板 | `templates/research_process/{daily_report,focus_writing,parking_lot}_template.md` | 读面写作 | 是 |

**规则**：不要重新实现或重新推导本表任一项；复用前核验身份并记录偏差；
**本表是工具表，不是证据表**。

**已知不可复用 / 会误导的东西**

- 早期「122 条引用 87% 缺失」的普查脚本输出：含 MAX_PATH 假阴性与编码假阴性，**已作废**。
- Windows 控制台对中文文件名的显示：会乱码，**不代表文件内容损坏**（用 read 工具验证）。
- 全局 git 配置：本机仍为 `schannel`；只有这两个仓库被 local 覆盖。
