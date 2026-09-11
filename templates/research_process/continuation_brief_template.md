# Continuation Brief Template

Copy to `.research/memory/conversations/<conversation-name>/continuation.md`.

- **One CURRENT brief per workstream.** Rewrite it at each checkpoint; never
  append. Mark the brief it replaces `SUPERSEDED` and name it under
  `Supersedes:`, so a reader can always find exactly one current entry point.
- **Non-canonical operational artifact.** It points at canonical sources and
  owns no claim, approval, verdict, or next decision.
- **Two sections are mandatory in every brief: B and H** (what to read, what to
  reuse). **E is mandatory whenever the brief authorises any action.** Omit D
  when the brief authorises nothing; keep the rest short rather than padded.
- A brief is written so that an agent with **no** conversation history can
  start working from it without asking a question it could have answered.

---

# Continuation Brief: `<workstream / stage>`

```text
Workstream:     <name>            Problem key: <stable key or none>
Role:           PRIMARY | SECONDARY
Record:         .research/memory/conversations/<conversation-name>/
Continues from: <previous continuation.md or none>
Supersedes:     <previous continuation.md or none>
Updated at:     <UTC>             Status: CURRENT | SUPERSEDED
Non-canonical:  points at canonical sources; owns no claim, approval, verdict,
                or next decision.
```

## A. Environment roots

Name every root this brief's paths resolve against, and say whether the writing
environment can read it.

| Root | Path | Readable here? |
| --- | --- | --- |
| Repository root | `<path>` | yes / no |
| Execution workspace | `<path>` | yes / no |
| Evidence and receipts | `<path>` | yes / no |

A reference under a root marked `no` is **unverifiable here, not stale**: report
it as unverifiable and never silently drop it. Never assume a path resolves
merely because it is written down. State any environment hazard that changes
what may be run (recycling, mounts, missing tooling, platform-only commands).

## B. Read list — in order; stop if a `required` item is absent

| # | Path | Answers which question | Required? |
| --- | --- | --- | --- |
| 1 | `<Focus>` | the current question and the one next decision | yes |
| 2 | `<Anchor>` | the canonical design and its claim boundary | yes |
| 3 | `<protocol.md>` | the approved contract, its scope, its approval ledger | yes |
| 4 | `<summary.md / detailed.md>` | what is established versus not | yes |
| 5 | `<definition owner>` | the experiment's own scientific definition | yes |
| 6 | `<evidence index / manifest>` | which artifacts are eligible evidence | yes |
| 7 | `<PROJECTS.md row>` | priority and role | no |

Rules:

- Each row earns its place by changing what the reader may do next. Do not pad.
- Do not reconstruct a missing `required` file from memory, a daily report, or a
  derived view. Report the absence and its root.
- Separate **must not be read as evidence** from **must not be read at all**.
- A filename, run label, job state, or derived analysis is not a verdict.

## C. Authority and boundaries

- Approved scope and its owner (exact reference):
- NOT approved — do not start:
- May not claim (keep the researcher's wording **verbatim**, never lift it):
- Human-owned decisions still open, and what the agent must do meanwhile:

## D. Execution prerequisites — only if this brief authorises running anything

- Target profile and image key, resolved from `docs/execution_envelope.md`:
- Submission entry point and its gates:
- Working directory and repo roots:
- Inputs (data / model / checkpoint) and their verified identities:
- Fixed parameters (conditions, seeds, steps, budget, qualification gates):
- Outputs (result location, receipt path, artifact map):
- Pre-run gates that must pass before a run counts as evidence:

Do not inline values that another file owns; name the key and the owner.

## E. Action list — in order; every step carries a branch

| # | Action (one verb) | Verify | If pass | If fail |
| --- | --- | --- | --- | --- |
| 1 | | | next | report / stop |

Rules:

- No step may depend on a file absent from section B.
- No step may be reported as done without its verification.
- Stop and redirect conditions are steps here, not an afterthought.
- Name the completion marker to poll, and say explicitly which signal is **not**
  a completion signal.

## F. Current state

- Done / Pending / Blocked, each with the artifact that shows it.
- Material failures, typed `INSUFFICIENT` states, and **retracted claims**.
- Already tried and rejected — do not repeat:
- Live concurrency risk: who else may be writing into the same output, and how
  the new owner takes over safely.

## G. Completion contract

- Deliverables:
- Done when:
- Stop and ask the researcher when:
- Never trade a reduced contract for a `COMPLETE` label.

## H. Reusable assets — reuse before rewriting

| Asset | Path | Reuse for | Verified? |
| --- | --- | --- | --- |
| Code / entry scripts | | | |
| Post-processors / patches | | | |
| Data, caches, presets | | | |
| Figure and plotting code | | | |
| Prior analyses worth not redoing | | | |
| Templates | | | |

Rules:

- **Do not re-implement or re-derive anything listed here.** Read it first.
- Verify an asset's identity (hash, version, provenance) before reuse, and record
  any deviation you introduce.
- An asset listed here is a tool, not evidence. Eligibility is owned by the
  evidence records, not by this table.
