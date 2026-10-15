# Repository skills

Canonical research skills live in `.agents/skills/<name>/`. Keep one root catalog;
project-specific skills and installed platform skills keep their own ownership.
For independent repositories such as NTP, install thin home routes with
`python tools/install_skill_routes.py --backup <outside-discovery-directory> --apply`.
The default destination is `~/.codex/skills`, verified on the installed clients;
`--destination` can select another supported user or persistent skill directory.
The script preserves replaced directories, copies canonical metadata and points
to the actual source. It changes no model, authentication or invocation policy.
Keep route targets on each host, never copy a Windows path to Linux. On 11109,
also install routes into the existing persistent `codex_skills/` source used by
bootstrap. No separate NTP skill implementation or copied reference tree is needed.

A repeated name may appear at repo and user scope. The user entry must only route
to the same canonical owner; it must not carry a second workflow. Verify both
working directories through the installed runtime's `skills/list` with
`forceReload: true`. This proves discovery and metadata, not that a model read
or followed the body; verify actual reads separately in a bounded read-only test.

## Select by the requested outcome

Choose one primary owner. An explicitly named artifact determines its authoring
owner; a question about that artifact may need only explanation or audit. Add
another skill only for a distinct necessary subtask, not as a serial checklist.
Routine rewriting, arithmetic or file inspection may need no research skill.

| Requested outcome | Primary skill |
|---|---|
| Audit a specific inference, causal chain, mathematical mechanism or proxy | `research-reasoning-auditor` |
| Discover/refine a research question, maintain Focus or choose its next falsifier | `research-progress-core` |
| Write or audit a formal Anchor and scientific design | `problem-anchor-writer` |
| Write/audit Protocol, Summary, Detailed or their evidence lineage | `experiment-card-writer` |
| Write/audit a settled-question final synthesis | `research-final-report` |
| Understand a named document, result, formula or idea | `research-document-explainer` |
| Write a requested meeting brief, stage Story or curated handoff | `research-communication` |
| Checkpoint/resume conversation context or prepare an operational continuation | `research-memory` |
| Assess advisor-discussion readiness or its next question | `research-sync-gate` |
| Place, reorganize, archive or explicitly publish artifacts | `research-mainline` |
| Inspect or execute an authorized remote job; retrieve logs/artifacts | `remote-experiment-workflow` |
| Critique an unsettled idea, theory, method or literature position | `scholar-mode` |
| Inspect, create, edit or validate an explicitly requested research graph | `research-graph-sop` |
| Explicitly requested local Sidecar display/API work | `sidecar-thinking` |

A brief explanation or audit may finish in chat. Missing human interpretation does
not block independent factual work. Scientific authority, execution and publication
follow [AGENTS.md](../AGENTS.md); skill selection grants none of them.

## Read only what this task needs

Read the selected `SKILL.md`, then its applicable references and named source
artifacts. Reuse unchanged instructions already in context; refresh sources that
can change the decision. Do not reread the whole catalog or all linked references
at every turn. A reference link is a route, not an instruction to load everything.

The advisor research-exploration method is integrated into these owners. Read the
[kernel](methodology/research_exploration_kernel.md) for open research stages;
read the [coverage mapping](methodology/research_exploration_mapping.md) only when
auditing that integration. Do not invoke a second top-level research-exploration
workflow or import its `design.md`, automatic graph, closure or viewer behavior.
Attribution remains in [THIRD_PARTY_NOTICES](../THIRD_PARTY_NOTICES.md).

Reports and replies use the shared [content and depth rules](report_writing.md#content-and-depth).
A full report preserves the model-to-evidence chain; a short answer expands only
the parts needed for the current question. No webpage is required. Root owns
process, projects own research and daily folders own dated communication; use
[project access](project_access.md) for missing checkouts or legacy paths.

## Validate changes and measure the right cost

Run `python tools/check_skills.py` and the installed skill-creator
`quick_validate.py` for changed skills. Run relevant local tests; changed math
uses `python tools/check_markdown_math.py <files>`. These check structure/source
behavior, not scientific truth or model routing.

Test realistic requests and actual outputs on the named models when behavior is
in scope. Compare like-for-like paths including required references, not only
entrypoint size. Bytes or tokenizer estimates are not observed API billing.
Keep routing concise; measure size as a diagnostic, not an unchanged-length gate.
If a delivery surface has an actual limit, link detailed sources rather than
discarding essential explanation. Do not change model settings
or implicit invocation policy merely to make a context-cost number smaller.

Codex discovers names/descriptions before loading selected skill bodies. If a
running task still shows old metadata, verify a fresh task rather than claiming
its already-loaded context changed. See [official skill documentation](https://learn.chatgpt.com/docs/build-skills).
