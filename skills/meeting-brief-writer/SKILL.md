---
name: meeting-brief-writer
description: Revise a human-first advisor-facing meeting executive summary from existing research artifacts. The final brief contains only the executive summary.
---

# Meeting Brief Writer

The meeting brief is a speaking and decision surface, not a second research
report. Its final content is one executive summary only.

## Human-First Gate

Before AI writes the final brief, the researcher first drafts from memory:

```text
Research question:
My initial judgment:
Direct result:
Claim boundary:
Exactly one next action:
```

If this draft is absent, provide the blank template and audit questions only.
Do not generate the researcher's initial judgment from chat history.

## Required Template

Read and follow exactly:

```text
templates/meeting/meeting_brief_template.md
```

The final file contains only `## 执行摘要` with these bold fields:

```text
研究问题
我的初始判断
本次结果
机制解释
决定性证据
结论边界
执行动作
来源
```

Do not append questions, background, model derivations, experiment timelines,
full tables, appendices, or a second conclusion. Link the anchor, `summary.md`,
or `detailed.md` for those details.

## Evidence Order

Do not use chat as evidence. Read:

```text
PROJECTS.md -> CURRENT.md -> anchor -> protocol.md -> summary.md -> detailed.md
```

Use only the sources needed to audit the executive summary.

## AI Revision Role

AI may:

- define unclear terms in plain Chinese;
- put the direct result first;
- verify metrics, numbers, and links;
- separate observation, interpretation, claim, speculation, and boundary;
- expose a live rival explanation;
- shorten repetition and improve wording.

AI must not:

- invent the researcher's initial judgment;
- silently replace the mechanism belief;
- upgrade a correlation into a causal claim;
- add a stronger claim than the linked sources;
- turn the brief into a full report.

If AI proposes a new interpretation, label it and obtain human approval before
including it in the final brief.

## Output

Write the dated copy to:

```text
daily_research_reports/MMDD/meetings/<topic>_meeting_brief_cn.md
```

Use Chinese by default and a topic-bearing filename. A project-local brief may
also be updated when explicitly requested.

## Validation

1. A human draft exists.
2. The final document contains only the executive summary.
3. The direct result appears before setup detail.
4. Every metric or project label used in a claim is defined inline.
5. Evidence links exist and support the nearby sentence.
6. Observation and mechanism interpretation are distinguishable.
7. The cannot-claim boundary and strongest live rival are explicit.
8. There is exactly one next action with pass/stop/insufficient criteria.
