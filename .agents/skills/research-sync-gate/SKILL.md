---
name: research-sync-gate
description: Use when a researcher is preparing an advisor or group sync, choosing one next research question, or cannot explain the current evidence boundary and stopping rule in plain language.
---

# Research Sync Gate

Require the researcher to own the judgment before AI polishes it. Use this gate before a formal meeting focus, Protocol, or new experiment.

## Handwritten Card

Ask the researcher to complete this compact card in their own words:

```text
最终目标：
当前阶段：
上次问题：
关键比较与直接结果：
能说明：
不能说明：
当前判断与理由：
最强竞争解释或未知：
明天唯一问题：
完成标准：
Parking Lot：

一分钟口头复述：
上次我们想回答……
所以比较了……
直接看到……
这说明……但不能说明……
明天只解决……完成后决定……
```

## Audit Gate

1. Read the named note/focus, then its linked Anchor and `summary.md`; use chat only as context.
2. Do not invent a blank judgment, unique question, or oral account. Ask one missing question at a time.
3. Check one chain: `question -> key comparison -> direct result -> claim -> cannot claim -> next decision`.
4. Require exact object, token/hook, data unit, metric meaning, strongest rival, and an inspectable completion rule only when they affect that chain.
5. Move every second question, method branch, rank search, or Router idea to `Parking Lot`.
6. Return one status, one blocking gap, and one required rewrite:
   - `READY_FOR_SYNC`
   - `READY_FOR_PROTOCOL`
   - `NOT_READY_MULTIPLE_QUESTIONS`
   - `NOT_READY_OBJECT_OR_LOGIC`

Do not run experiments or create a Protocol through this skill. After `READY_FOR_SYNC`, use `meeting-outline-writer` for the formal meeting artifact. After the researcher separately approves an experimental question, use `experiment-card-writer`.
