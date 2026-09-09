# Conversation Memory Contract

Use this contract for repository-local continuity across Codex threads,
accounts, or restarts. It creates working context, not a second research truth.

## Identity And Persistence

One directory represents one source Codex conversation record:

```text
.research/memory/conversations/<YYYYMMDD_conversation-slug>/
  memory.md
  history.md
```

Several records may continue the same logical work. Before any conversation's
first memory write, inspect its current title through available Codex task or
thread metadata. Use a user-supplied conversation name when one is given. If
the title is unavailable or ambiguous, ask the user instead of inferring a
name from the research topic.

Use the creation date and a short lowercase hyphenated slug derived from that
conversation name. If the resulting path already belongs to a different
conversation, add a short stable disambiguating suffix rather than overwrite
it. Keep the directory name stable for later checkpoints made within the same
source conversation.

A new Codex conversation may read a previous record to resume the same logical
work, but its first write creates a new record under its own name and timestamp.
It must not overwrite the previous conversation's `memory.md`. Here,
`conversation` is a continuity record; it is not a `researchctl` owner, a lock,
or scientific authority.

These files are ordinary versionable repository content. Sharing a checkout
makes uncommitted memory visible to other local accounts or threads; sharing
across checkouts requires an explicitly committed and synchronized checkpoint.
Being present in Git does not make any statement canonical, approved, or
consensus. Commit and push retain the repository's normal approval boundary.

## `memory.md`: Current Working Snapshot

`memory.md` is the only file read by default when resuming conversation work.
Prefer 2--4 KB of UTF-8 text. Around 8 KB is a compression signal, not a
validity gate.

Use these headings:

```markdown
# Conversation Memory: <short name>

Conversation name: <current Codex conversation title>
Created at: <UTC timestamp>
Updated at: <UTC timestamp>
Continues from: <prior record path or none>

## Objective
## Current State
## Working Understanding
## Decisions And Constraints
## Open Loops
## Resume Point
## Canonical References
```

Keep only information needed to choose and perform the next action:

- The header identifies the source conversation and timestamps every newly
  created memory. Update `Updated at` on every checkpoint; never rewrite
  `Created at`. `Continues from` links the previous record when this
  conversation resumes earlier work.

- `Objective`: the current bounded outcome, not the original transcript.
- `Current State`: completed work, active work, blockers, and material failures.
- `Working Understanding`: the smallest reasoning state needed to continue.
  Mark scientific interpretations as source-backed, provisional, disputed, or
  unknown when their status is not otherwise obvious.
- `Decisions And Constraints`: operational choices and user constraints. A
  scientific decision or approval must link to its canonical owner. If it
  exists only in prior conversation, label it `pending canonicalization` and do
  not use it to authorize execution or strengthen a claim.
- `Open Loops`: unresolved items that can still change the outcome.
- `Resume Point`: one concrete next action, plus any stop or redirect condition
  already established by an owning source.
- `Canonical References`: the smallest set of repository-relative Focus,
  Anchor, Protocol, Summary, Detailed, code, or evidence paths needed to verify
  the snapshot. State why each reference matters.

Do not include complete code, diffs, command transcripts, logs, result tables,
chat messages, credentials, tokens, or private account data. Link to the owning
source instead. A short exact value or failure message is allowed only when it
is necessary to resume and the source is identified.

## `history.md`: Cold Compressed History

`history.md` is append-only and is not loaded during ordinary resume. Add one
short entry only when the working state materially changes, such as:

- the objective or scope changes;
- an important decision or constraint is confirmed, superseded, or withdrawn;
- a blocker, failure, or evidence boundary changes the route;
- the resume point moves to a different stage;
- the logical conversation is completed, abandoned, or intentionally paused.

Routine reads, commands, test passes, message exchanges, wording changes, and
minor progress do not belong in history. Use this compact form:

```markdown
## <UTC timestamp> -- <transition>

- Change:
- Why it matters:
- Supersedes:
- References:
```

Record a reference to a canonical scientific transition rather than copying
its conclusion. Never append the old `memory.md` wholesale.

## Creation

Create a record only when the user asks to preserve or resume working context,
or when the requested work explicitly spans sessions. First identify the
current conversation name. Initialize both files in a new record for that
conversation, write UTC `Created at` and `Updated at` timestamps in `memory.md`,
and add one timestamped creation entry to `history.md`. The dated directory,
header, and optional `Continues from` link are the saved conversation record;
do not add a repository-wide index, registry, lock, template, database, or
background process.

If the current source conversation already has a record, checkpoint that
record rather than creating a duplicate. Do not reuse a record merely because
another conversation has the same topic. A user-provided conversation name
controls creation and selection; preserve a unique path if names collide.

## Checkpoint And Concurrent Writes

Before rewriting the current conversation's `memory.md`, read its latest
version. Rewrite the snapshot to the new current state, update `Updated at`,
and preserve `Created at` instead of appending chronology. Append to
`history.md` only if the checkpoint contains a material transition.

Version 1 assumes sequential continuation, not concurrent multi-writer merge.
If the file changed incompatibly since it was loaded, do not silently
overwrite the newer checkpoint. Reconcile the two current states or keep
separate logical-conversation records and let the researcher decide.

A checkpoint does not transfer or close a `researchctl` task. When a new thread
will modify a registered scientific problem, run the normal `researchctl
context` operation for that thread. Treat any old-thread overlap as advisory;
do not infer authority from the memory record.

## Compression

When `memory.md` grows beyond roughly 8 KB or contains substantial chronology:

1. Preserve the present objective, current state, live constraints, open loops,
   resume point, and minimal references.
2. Collapse repeated reasoning and remove resolved operational detail.
3. Append only historically material superseded state to `history.md`.
4. Rewrite `memory.md` as a self-contained current snapshot, preferably 2--4 KB.

Compression must preserve uncertainty and negative results. It must not turn a
provisional interpretation into an established claim.

## Retrieval And Resume

When the user names a record, conversation, or path, select it and read only
its `memory.md` first. When no prior record is specified but memory retrieval
is requested, select the latest record by its valid `Updated at` timestamp;
use `Created at` and then the directory name only as deterministic tie-breakers.
Do not scan every `history.md` or old chat export. If timestamps are missing or
invalid and the latest record cannot be determined safely, show only the small
candidate set and ask the user which record to read.

Read `history.md` only when the current snapshot identifies a specific missing
transition or the user explicitly asks for historical reconstruction. Search
for the relevant term, date, decision, or reference and read only the matching
section.

Before acting on resumed scientific content:

- verify that decision-bearing references still exist and are current;
- read only the owning sources needed for the next action;
- preserve provisional, disputed, and unknown states;
- obtain any approval required by the owning Protocol or repository boundary.

## Completion

A memory operation is complete when `memory.md` accurately states the current
objective, open loops, resume point, and minimal references; any material state
transition has one concise history entry; and no statement depends on memory
alone for scientific authority. Retain completed records by default. Deletion,
commit, push, publication, and external synchronization remain separate
explicit actions.
