# Conversation Memory: 0910-memory-system improvement

Conversation name: 0910-memory-system improvement
Processed by: DeepSeek (harness: DeepSeek Harness; model: deepseek-v4-flash-vision-exp)
Created at: 2026-09-09T17:29:37Z
Latest update at: 2026-09-09T17:29:37Z
Continues from: none

## 2026-09-09T17:29:37Z -- Memory 系统语义改版、记录迁移与用语润色完成

- Summary: 本对话把 memory 系统从"快照替换"改为"累积增加"并完成全库一致性迁移，随后按推文规则完成 skill/AGENTS 用语评估与润色，最后将本对话归类为 research system 记录。属仓库维护工作，未注册科学 problem_key（AGENTS.md：仓库维护不发明 problem_key、不要求注册）。研究人员确认的四项决策：(1) 累积单文件——memory.md 末尾追加带时间戳条目、永不替换旧条目；(2) 记录目录按对话名命名（名称含日期则保留、中英混用允许）；(3) 取消 history.md，全部并入 memory.md；(4) launch_prompt.md 保留在记录内不动（授权本体在 A6 protocol §10 审批台账）。执行成果：memory_contract.md 重写为累积单文件语义并新增 `Processed by`（Codex / DeepSeek / DeepSeek via Claude）强制字段；SKILL.md 精简至短描述 + 边界 + 指向契约（约 20 行）；5 条记录迁移（sae-balanced-routing 6 条、0907-sae-routing-validation 1 条、head-account-switching 1 条、head-codex-backup-deepseek-harness-backup 3 条、0909-router-regularization 1 条），history.md 全部并入删除，旧日期目录名全库零残留，头部字段补齐；AGENTS.md / README.md / docs/skills.md 同步累积语义，并按"轻量"原则仅压缩常驻的 AGENTS.md memory 段落；撤销"只读 memory list"提议（违反契约"不设索引/注册表"，属投机式过度设计）；两条最重 skill（experiment-card-writer 256 行、problem-anchor-writer 267 行）刻意不拆——按需加载且已完成引用路由，拆解属过度设计。推文规则来源：pvncher 推文（OpenAI Codex DX 负责人），经报道为"skill 描述要短、正文只指引子文档、不要过度手册化、AGENTS.md 每行都要问是否需要"。
- Current work: 无未完成事项。所有请求的修改已落地并验证（无旧路径残留、无 history.md、头部字段齐全）。
- Next action: 无待办。后续若提交 git（按仓库边界需单独请求）或审计其余 6 个 skill 的引用完整性，均属新的显式请求。
- References: 本记录为非规范工作上下文。本对话改动面：`.agents/skills/research-memory/SKILL.md` 与 `references/memory_contract.md`（memory 语义与处理者字段）、`AGENTS.md`（memory 段落与状态表）、`README.md`、`docs/skills.md`；迁移产物：`.research/memory/conversations/{sae-balanced-routing, 0907-sae-routing-validation, head-account-switching, head-codex-backup-deepseek-harness-backup, 0909-router-regularization}/memory.md`。本记录处理者证据：DSH_HOME=/root/.dsh、DSH_SESSION_JSONL=/root/.dsh/sessions/--data-250010109-Research_System--/、`dsh` CLI 在 /data/250010109/tools/deepseek-harness。
