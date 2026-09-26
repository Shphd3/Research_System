# Operational Continuation Contract

Use this for a bounded task passed to another model/thread. It is distinct from
curated research-artifact delivery and from reading an entire conversation log.
Use `templates/research_process/continuation_brief_template.md` when writing.

## Authority and ownership

A continuation owns no scientific claim, priority, approval or decision. Point
to the owning Focus/Anchor/Protocol/result only when needed for this next action.
A user instruction already authorizing local work remains applicable; a brief
cannot expand it into remote execution, scientific approval or publication.
If a scientific approval exists only in chat, record `pending canonicalization`
and do not treat the brief as a substitute for its required owning contract.

Write `.research/memory/conversations/<this-conversation>/continuation.md`
only after identifying the conversation as required by the memory contract.
One `CURRENT` brief per record; replace that record's brief on update. `CURRENT`
means current in that record, not exclusive ownership of a research workstream.
A new conversation uses `Continues from` to link its predecessor and writes
its own record; it does not relabel another thread's brief `SUPERSEDED`.
For a handoff within an existing record, reread it and check for concurrent
changes before replacing it. Never overwrite another writer's changes.

## Minimum useful content

Keep the brief short enough to understand the next action without chat history:

- objective and concrete requested deliverable;
- exact read list, with why each source is needed and whether needed **now**;
- next authorized action and its verification/stop condition;
- current outputs, unresolved failures and prior work that should not be repeated;
- reusable code/artifacts with verified paths or `none needed`;
- writable files, protected/concurrent work, existing job IDs if relevant;
- source of scope/approval and any still-missing human decision.

Use about one screen when feasible, not a hard word limit. Preserve material
uncertainty and failure boundaries before saving space. Do not copy the canonical
result or a large history into the brief. Name a stable artifact or section;
include a hash/version when mutable identity affects the next action.

## Receiving

1. Read the named brief. Check its objective against the current user request.
2. Verify the small required read list. Open only sources whose role is needed
   for this action; neither a source label nor a hash establishes approval.
3. If a source changed, reread it and resolve the affected action. Do not use a
   stale brief to override a current owner. An inaccessible environment root is
   unverifiable here, not stale or safe to delete.
4. Continue already-authorized reversible work after those checks. A missing
   optional file is a recorded limitation, not a stop. Missing necessary evidence,
   authorization or input blocks the dependent action; complete independent work.
5. Inspect any named existing job before deciding to resume or submit. Switching
   models or threads does not justify relaunching a job or reopening a stopped test.

Do not infer a previous agent's intent or execution from its self-description.
Compare actual artifacts/receipts to the requested completion condition.
A named `memory.md` or explicit history-resume request follows the full-log rule;
a brief-only handoff does not silently require unrelated history.

## Completion

Another model with no chat history can identify the next allowed action, its
minimum sources, existing outputs, file boundaries and completion/stop condition.
No scientific state changed solely because a brief was written. External sync,
commit and push still require explicit instructions. Do not create a global
registry, lock, automatic archive or background monitor.
