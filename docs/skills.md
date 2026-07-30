# Repository Skills

The canonical repository skills live in `.agents/skills/<skill-name>/`. Codex
discovers this path directly; do not copy these skills into a personal Codex
directory or maintain a second installed version.

Codex first reads each skill's `name` and `description` to decide whether it
matches a task. It loads the `SKILL.md` body, references, and scripts only after
selection. This follows the current [Codex customization
model](https://developers.openai.com/codex/concepts/customization#skills).

## Responsibility And Trigger Index

| Skill | Trigger scope | Does not own | Implicit invocation |
| --- | --- | --- | --- |
| `research-progress-core` | Research judgment, rivals, minimal falsification, result boundary, failure analysis, daily focus | Project paths, document schemas, remote execution | Allowed |
| `problem-anchor-writer` | Thinking Card audit and approved anchor creation or update | Protocols, run commands, result records | Allowed |
| `experiment-card-writer` | `protocol.md`, `summary.md`, `detailed.md`, evidence and figure contracts | Research-question redefinition, remote jobs | Allowed |
| `research-story-writer` | Explicit research-line story or paper-like stage synthesis | Anchors, experiment records, routine meeting notes | Allowed |
| `research-mainline` | Project organization, artifact placement, archive state, status, and explicitly requested root-mirror publication | Research judgment, raw execution, handoff packaging, external collaborator sync | Allowed; guarded actions still require an explicit request |
| `remote-experiment-workflow` | Container, SSH, CCI, SCO, or ACP experiment workflow, monitoring, logs, artifact maps | Hypothesis design or SCO platform resource semantics | Allowed |
| `scholar-mode` | Research-intuition audit, theory or methodology critique, paper analysis, literature positioning | Artifact schemas, graph work, runs, ordinary code | Allowed |
| `meeting-outline-writer` | Advisor meeting, meeting brief, speaking flow, multi-line discussion outline | Researcher's conclusion, handoff packaging, sync | Allowed |
| `handoff-report-writer` | Explicit curated package, handoff, copy, or external sync request | New claims, meeting authorship, raw outputs | Explicit only |
| `research-graph-sop` | Explicit `graph.yaml` inspection, creation, maintenance, or navigation audit | Ordinary research notes or project-state edits without graph scope | Allowed |
| `sidecar-thinking` | Explicit Sidecar display, session, graph inspection, or API/CLI call | Ordinary graph editing or research synthesis | Explicit only |

## Routing Rules

Use the smallest matching skill. Typical composition is:

```text
research-progress-core
-> problem-anchor-writer
-> experiment-card-writer
-> remote-experiment-workflow when execution is remote
-> research-story-writer only for explicit line synthesis
-> research-mainline for project placement or explicit publication
```

Use `meeting-outline-writer` for meeting content and return to
`handoff-report-writer` only after the user explicitly requests packaging or
external sync. `research-mainline` may locate the canonical sources but does
not assemble that package. Use `research-graph-sop` for graph structure and
`sidecar-thinking` only for an explicitly requested Sidecar operation.

For SCO work, `remote-experiment-workflow` owns the research experiment chain;
the independently maintained `Projects/sco-skill/skills/sco-control` owns
platform-specific SCO resources and commands. Do not merge or move it into the
root skill catalog.

## Project-Private Skills

Directories under `Projects/` are independent Git repositories. Their private,
historical, or divergent skills are not root-catalog duplicates and must not be
silently merged with `.agents/skills/`. A project may keep its own
`.agents/skills/` when the workflow is genuinely project-specific. The
narrower project skill takes precedence for its named transport or document
workflow, while root safety, approval, and canonical-artifact boundaries still
apply.

## Validation

Run structural validation from the repository root:

```bash
for skill_dir in .agents/skills/*; do
  python /root/.codex/skills/.system/skill-creator/scripts/quick_validate.py "$skill_dir"
done
```

After changing skill metadata, start a new Codex task or restart Codex before
testing catalog discovery and automatic triggering. Static validation confirms
format and files, not live trigger selection in the already-running task.
