# Conversation Memory Contract

Use this contract for repository-local continuity across Codex threads,
accounts, or restarts. Each record is one accumulating working log: a new
checkpoint appends a new timestamped summary entry on top of the previous
entries; it never replaces them. It creates working context, not a second
research truth.

## Identity And Persistence

One directory represents one source Codex conversation record, and one file
stores that record:

```text
.research/memory/conversations/<conversation-name>/
  memory.md
```

- `<conversation-name>` is derived from the conversation title, not from a
  date. Use lowercase, whitespace to hyphens, and drop decorative punctuation.
  Keep a date when the conversation name itself contains one (for example
  `0909-router-regularization`, `0907-sae-routing-validation`). Non-ASCII
  characters are allowed as they appear; transliteration is not required.
  Mixed Chinese and English in a name or in the memory content is fine.
- If the resulting path already belongs to a different conversation, add a
  short stable disambiguating suffix rather than overwrite it. Keep the
  directory name stable for later checkpoints made within the same source
  conversation.
- Before any conversation's first memory write, inspect its current title
  through available Codex task or thread metadata. Use a user-supplied
  conversation name when one is given. If the title is unavailable or
  ambiguous, ask the user instead of inferring a name from the research topic.

A new Codex conversation may read a previous record to resume the same logical
work, but its first write creates a new record under its own name. It must not
overwrite the previous conversation's `memory.md`. Here, `conversation` is a
continuity record; it is not a `researchctl` owner, a lock, or scientific
authority.

Other files may exist inside the record directory (for example a one-time
launch prompt, or a `continuation.md` brief). They are operational artifacts,
not memory: they follow the memory boundary below but are not governed by the
entry format of this contract, and no approval or scientific status may be
derived from them.

`continuation.md` is the sanctioned entry point for handing a workstream to a
different conversation. Keep exactly one CURRENT brief per workstream: rewrite
it at each checkpoint rather than appending, mark the brief it replaces
`SUPERSEDED`, and name it under `Supersedes:` so a reader can always find the
single current entry point. Its shape is fixed by
`templates/research_process/continuation_brief_template.md`. The mandatory
sections are the read list and the reusable assets, plus the action list
whenever the brief authorises any action. A brief points at canonical sources
and never restates their conclusions.

These files are ordinary versionable repository content. Sharing a checkout
makes uncommitted memory visible to other local accounts or threads; sharing
across checkouts requires an explicitly committed and synchronized checkpoint.
Being present in Git does not make any statement canonical, approved, or
consensus. Commit and push retain the repository's normal approval boundary.

## `memory.md`: Accumulating Working Log

`memory.md` is the read surface when resuming conversation work. It is
append-only by convention: old entries are preserved, and each checkpoint adds
one new entry with a UTC timestamp. The newest entry, at the end of the file,
is the current state; earlier entries form the evolution chain of summaries.

Use this shape:

```markdown
# Conversation Memory: <short name>

Conversation name: <current Codex conversation title>
Processed by: <Codex | DeepSeek | DeepSeek via Claude> (harness: <harness>; model: <model or unknown>)
Created at: <UTC timestamp>
Latest update at: <UTC timestamp>
Continues from: <prior record memory.md path or none>
Environment: <named roots this record's paths resolve against, for example
  `repo=<path>` `exec=<path>` `receipts=<path>`; mark every root that the
  writing environment cannot read as `not-visible`>

## <UTC timestamp> -- <transition or stage title>

- Summary: <the comprehensive state at this point, built on the previous
  entries>
- Current work: <what is being done now, its own status, blockers, and material
  failures>
- Next action: <one concrete action, plus any stop or redirect condition
  already established by an owning source>
- References: <the smallest set of Focus, Anchor, Protocol, Summary, Detailed,
  code, or evidence paths needed to verify this entry; state why each matters>
```

- `Created at` is written on creation and never rewritten. `Latest update at`
  is the timestamp of the newest entry and is updated on every checkpoint.
  `Continues from` links the previous record when this conversation resumes
  earlier work. `Processed by` names the agent that performed the recorded
  work (one of `Codex`, `DeepSeek`, or `DeepSeek via Claude`), then the
  harness and the model it ran under, as
  `(harness: <harness>; model: <model or unknown>)`. State the harness only
  from the environment or an authoritative record, and the model only when it
  is verified; otherwise write `model: unknown`. Never invent a harness or a
  model.
- `Environment` names the filesystem roots this record's paths resolve against,
  and marks any root the writing environment cannot read as `not-visible`. A
  reference whose root is absent from the current environment is unverifiable,
  not stale: report it as unverifiable and never silently drop it. Do not
  assume a path resolves merely because it is written in this record.
- Every entry carries a `Summary`; the newest entry additionally carries
  `Current work`, `Next action`, and `References`. Optional `On top of:` and
  `Supersedes:` bullets may name the prior entry a summary extends or a
  decision a transition overturns. Never append the old file wholesale as a
  new entry; each entry re-summarizes, does not replay.
- A checkpoint that covers a change to a canonical artifact (`PROJECTS.md`, a
  `focus_<problem>.md`, an Anchor, `protocol.md`, `summary.md`, `detailed.md`,
  or a catalog Skill) must name that artifact under `References` and, when the
  change supersedes a prior decision or state, under `Supersedes`. Record the
  pointer and its bounded effect only; never restate the artifact's conclusion
  as memory-owned content. The change is owned by its artifact, and memory
  never carries its authority.
- Keep only information needed to choose and perform the next action. Mark
  scientific interpretations as source-backed, provisional, disputed, or
  unknown when their status is not otherwise obvious. A scientific decision or
  approval must link to its canonical owner; if it exists only in prior
  conversation, label it `pending canonicalization` and do not use it to
  authorize execution or strengthen a claim.
- Do not include complete code, diffs, command transcripts, logs, result
  tables, chat messages, credentials, tokens, or private account data. Link to
  the owning source instead. A short exact value or failure message is allowed
  only when it is necessary to resume and the source is identified.

## Growth

The log grows by design; there is no separate cold archive and no automatic
compaction. `history.md` is not used. If a log becomes unwieldy, prefer a new
record for the same logical work with `Continues from` pointing here, which is
already the sanctioned cross-record mechanism.

In-place consolidation of redundant narration happens only on an explicit
researcher request: never on a schedule, and never automatically. There is no
expiry signal and no size or age threshold that triggers it. Before
consolidating, re-verify every open item against its owning source.
Consolidation must preserve every unresolved uncertainty, every negative or
`INSUFFICIENT` result, every decision that is not explicitly superseded, and
the original `Created at`. It may remove only superseded narration and resolved
operational detail. After consolidating, append one entry stating what was
removed and why. If a log is merely long rather than redundant, prefer a new
record with `Continues from` over rewriting the old one.

## Creation

Create a record only when the user asks to preserve or resume working context,
or when the requested work explicitly spans sessions. First identify the
current conversation name. Initialize `memory.md` with the header, write UTC
`Created at` and `Latest update at` timestamps, and add one timestamped
creation entry. Do not add a repository-wide index, registry, lock, template,
database, or background process.

If the current source conversation already has a record, checkpoint that
record rather than creating a duplicate. Do not reuse a record merely because
another conversation has the same topic. A user-provided conversation name
controls creation and selection; preserve a unique path if names collide.

## Checkpoint And Concurrent Writes

Before rewriting the current conversation's `memory.md`, read its latest
version. Append one new entry for the new current state, update `Latest update
at`, and preserve `Created at`. Old entries are not edited; correction of a
factual error in an old entry is allowed only as an annotated correction, not
as a silent rewrite.

Version 1 assumes sequential continuation, not concurrent multi-writer merge.
If the file changed incompatibly since it was loaded, do not silently
overwrite the newer checkpoint. Reconcile the two current states or keep
separate logical-conversation records and let the researcher decide.

A checkpoint does not transfer or close a `researchctl` task. When a new thread
will modify a registered scientific problem, run the normal `researchctl
context` operation for that thread. Treat any old-thread overlap as advisory;
do not infer authority from the memory record.

## Retrieval And Resume

When the user names a record, conversation, or path, select it and read its
`memory.md` in full: the cumulative log, from the header through the newest
entry. The newest entry is the current state. When no prior record is
specified but memory retrieval is requested, show the small candidate set
(directory name plus `Latest update at`) and ask which record to read; if one
record is clearly meant by the conversation name, select it. Use `Latest
update at` (then `Created at`, then the directory name) only as deterministic
tie-breakers, never as a substitute for the name. Do not scan old chat exports.

Before acting on resumed scientific content:

- verify that decision-bearing references still exist and are current;
- read only the owning sources needed for the next action;
- preserve provisional, disputed, and unknown states;
- obtain any approval required by the owning Protocol or repository boundary.

## Completion

A memory operation is complete when `memory.md` has one newest entry that
accurately states the current objective, current work, next action, and
minimal references; older entries remain intact; and no statement depends on
memory alone for scientific authority. Retain completed records by default.
Deletion, commit, push, publication, and external synchronization remain
separate explicit actions.
