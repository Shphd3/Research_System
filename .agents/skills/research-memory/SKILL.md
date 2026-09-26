---
name: research-memory
description: "Checkpoint or resume conversation working memory, or prepare an operational continuation brief for another model/thread. Non-canonical; not scientific judgment or an external artifact handoff."
---

# Research Memory

Keep continuation portable across models, threads and accounts while canonical
sources retain all scientific authority. Select the requested operation:

| Request | Required input and reading | Output |
|---|---|---|
| Create/checkpoint a conversation log | Verified conversation name; [memory contract](references/memory_contract.md); existing log before appending | One timestamped entry in that conversation's `memory.md` |
| Resume a named log/conversation | The [memory contract](references/memory_contract.md) and **whole** selected `memory.md`; current owner sources for the next action | Verified next action; a new conversation writes only its own record |
| Prepare or receive a model/thread continuation | [Continuation contract](references/continuation_contract.md); the named brief and its task-required sources | Compact operational brief or scoped continuation |

For writing a continuation, use the existing root
[template](../../../templates/research_process/continuation_brief_template.md).
A named brief need not expand into every historical log; explicitly requested
log/history resume still reads the full selected log. Do not scan unrelated
conversations or create a global registry.

## Shared boundaries

- `memory.md` is append-only; never rewrite another conversation's history.
- A brief is a pointer, not permission. Verify scientific approval against its
  canonical owner and preserve the user's current authorized scope.
- Record processing agent, harness and model only from verified metadata;
  unknown identity stays `unknown`. Model changes do not alter permissions.
- No full code, diffs, transcripts, result tables, logs or credentials: link them.
- Missing optional material does not block a supported task. Missing decisive
  evidence or approval blocks only the action that depends on it.
- External packages/sync belong to `research-communication`, only if requested.
