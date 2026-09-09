---
name: research-memory
description: "Use when the user asks to create, checkpoint, compact, resume, or retrieve repository-local non-canonical working memory across Codex threads or accounts. Do not use for scientific-state updates, curated artifact handoff, or publication."
---

# Research Memory

Maintain compact working-state snapshots for work that must continue across
Codex conversations, accounts, or restarts.

Read [references/memory_contract.md](references/memory_contract.md) before
creating, checkpointing, compressing, or retrieving a conversation memory.

## Boundary

- Use `.research/memory/conversations/<YYYYMMDD_conversation-slug>/`.
- Before the first write, inspect the current Codex conversation name from
  available task or thread metadata. If it is unavailable or ambiguous, ask
  the user to name it; do not infer it from the research topic.
- Give each Codex conversation a distinct timestamped record. A continued
  conversation may read a previous record, but its first write creates a new
  record instead of overwriting the previous conversation's `memory.md`.
- Unless the user names an older record, retrieve the latest `memory.md`.
- Treat `memory.md` and `history.md` as non-canonical working context even when
  they are versioned in Git.
- Never derive scientific truth, approval, or authority from memory. Verify it
  against the owning Focus, Anchor, Protocol, Summary, or Detailed record.
- Do not create memory for every task. Use it only when cross-session
  continuation or explicit recall is in scope.
- Do not copy complete chats, code, diffs, logs, tables, or raw outputs into
  memory; preserve the smallest useful state and direct references.

This Skill does not package approved artifacts for another audience. Route
that deliverable to `research-communication` handoff mode.
