---
name: research-memory
description: "Create, checkpoint, resume, or retrieve repository-local non-canonical working memory across Codex threads or accounts. Not for scientific state or artifact handoff."
---

# Research Memory

Accumulating append-only per-conversation working log. Checkpoints append one
timestamped summary entry; they never replace older entries.

Read [references/memory_contract.md](references/memory_contract.md) before
creating, checkpointing, or retrieving.

## Boundary

- Record: `.research/memory/conversations/<conversation-name>/memory.md` —
  named by conversation, not by date; mixed Chinese and English is fine; no
  `history.md`.
- Header records the processing agent and its harness and model:
  `Processed by: <agent> (harness: <harness>; model: <model or unknown>)`.
  State the model only when verified; otherwise write `unknown`.
- One record per Codex conversation; resume reads the whole log; the newest
  entry at the end is the current state.
- Non-canonical: never derive truth, approval, or authority from memory;
  verify against Focus, Anchor, Protocol, Summary, or Detailed.
- No chats, code, diffs, logs, tables, or credentials; reference instead.
