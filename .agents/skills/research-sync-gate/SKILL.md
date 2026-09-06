---
name: research-sync-gate
description: Use when a researcher is preparing an advisor or group sync, choosing one next research question, or cannot explain the current evidence boundary and stopping rule in plain language.
---

# Research Sync Gate

Require the researcher to own the judgment before AI polishes it. Use this gate
after each group meeting or explicit research reset and before a Protocol or new
experiment. The output is one persistent two-day core-task Focus, not a chat-
only card.

## Active Core-Task Focus

Create or audit exactly one
`daily_research_reports/MMDD/focus_<problem>.md` from
`templates/research_process/focus_writing_template.md`. Ask the researcher to
own this compact content in their own words:

```text
1. 核心问题
2. 实验目的：要解决到什么程度、依赖子问题、完成标准
3. 分析方法：最多三条白话步骤
4. 结论：执行前的支持/不支持两个预期分支；执行后由研究者填写实际结果
```

One self-contained core experiment is preferred; three is the absolute maximum.
Controls and diagnostics that only protect the same verdict are not separate
core experiments. Define every indispensable English term or abbreviation in
plain Chinese before using it.

Track the core question and the full four-part design separately. If a later
Protocol audit materially changes a method, completion rule, or expected
branch, preserve a confirmed core question but set
`design_state: AWAITING_HUMAN_CONFIRMATION` and record the reason in prose;
return to this gate before Protocol promotion.

## Audit Gate

1. Read the named meeting note and active Focus, then its linked Anchor and
   relevant `summary.md`; use chat only as context.
2. Do not invent a blank judgment, unique question, or oral account. Ask one missing question at a time.
3. Before execution, check one chain: `core question -> purpose -> at most three
   methods -> expected positive/negative branches -> completion rule`.
4. After execution, check one chain: `question -> key comparison -> direct
   result -> claim -> cannot claim -> next decision`.
5. Require exact object, token/hook, data unit, metric meaning, strongest rival,
   and an inspectable completion rule only when they affect that chain.
6. Move a second key long-term question to
   `Projects/<project>/main/parking_lot/README.md` with a reopening condition.
   Ignore minor tangents instead of recording them.
7. While the Focus is active, do not start a parked question unless the
   researcher explicitly replaces the core task.
8. Return one status, one blocking gap, and one required rewrite:
   - `READY_FOR_SYNC`
   - `READY_FOR_PROTOCOL`
   - `NOT_READY_MULTIPLE_QUESTIONS`
   - `NOT_READY_OBJECT_OR_LOGIC`

Do not run experiments or create a Protocol through this skill. Ordinary one-
problem meetings use the active Focus directly. Use `research-communication`
meeting mode only when the researcher explicitly requests a meeting brief,
speaking outline, or multi-problem synthesis. After the researcher confirms the
four-part design, use `experiment-card-writer` for the canonical Protocol.
