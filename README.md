# Research System

Shared research rules and project access. Each project owns its questions,
designs and evidence; the execution workspace owns running code, raw outputs,
logs and checkpoints. Daily folders hold meetings and short reading indexes.

## Start with the task

- Named question, result or file: read that source first.
- Choose research work: [PROJECTS](PROJECTS.md) -> project roadmap -> named Focus,
  Anchor or Summary. Do not load all records.
- Prepare a meeting: open the date's `meeting_report/` speaking entry; follow
  sources only for the explanation or evidence needed.
- Old path or incomplete checkout: [project access](docs/project_access.md)
  ([中文](docs/project_access_cn.md)); use the resolver or generated reading bundle.

[Daily reading](daily_research_reports/README_cn.md) ·
[from project](research/from-attention-to-search/main/roadmap_cn.md) ·
[Skills](docs/skills.md) · [Writing](docs/report_writing_cn.md)

For project material readable from System alone, use the
[Anchor reading copies](sync/anchors/README_cn.md). They refresh after an Anchor
guidance delivery under the [shared sync workflow](docs/anchor_sync.md).

[Research assets](assets/README.md) ([中文](assets/README_cn.md)) indexes local
model/SAE checkpoints, saved representations and datasets, with live access checks.

## Research logic

```text
question, importance and scope
-> candidate explanation or formal claim, assumptions and rivals
-> appropriate model and smallest distinguishing check
-> eligible evidence and bounded answer
-> affected question or assumption and researcher-owned next decision
```

Evidence can be a proof, counterexample, observation, intervention or system
comparison. Return to the unresolved link when a check fails. A chosen route is
not a necessary prerequisite without a justified dependency.

## One owner for each record

| Record | Owns |
|---|---|
| System PROJECTS / project roadmap | Project access / research-line routing |
| Project `main/focus/` | Stable question and researcher-owned next decision |
| Anchor | Sole current scientific design, eight-section contract |
| Protocol | Exact experiment contract, approval and amendments |
| Summary | A readable answer connecting purpose, necessary model, hypothesis, key observations and bounded meaning |
| Detailed / execution record | Explain how the comparison was performed and calculated; retain setup, controls, deviations and provenance |
| Meeting brief, Story, final report | Derived explanations of named sources |

Focus keeps `task_state`, `question_state`, `design_state` and `result_state`
independent. A run or completed report does not confirm scientific judgment.
Reuse confirmed decisions; do not ask for repeated approval to satisfy a form.
Creating, replacing or closing a question remains a researcher decision.

Formal records live in the project; dates never become the only home of an
active design or result. A relocation preserves question identity and original
frozen hashes. [Location records](docs/research_locations.json) resolve earlier
paths without keeping duplicate editable sources.

## Explain for understanding

Use short, direct sentences and consistent terms. Define objects before symbols,
and keep assumptions and uncertainty. Put the answer early, with enough reasoning
for a new reader to understand it. Match headings to the research type.

Markdown carries the complete explanation; requested interactive maps provide a derived reading view. State decisive values
and figure findings in prose; define formulas and use headings for deeper detail.
Move complete audits and long per-item explanations to the owning appendices,
with clear links from Summary and Detailed. Figures and evidence links support verification. A meeting brief keeps the short
core and Q&A together. A stable bounded question may have
one researcher-confirmed final synthesis. See [writing rules](docs/report_writing.md).

## Shared working rules

[AGENTS](AGENTS.md) owns language, authority, completion and Git boundaries.
[Skills](docs/skills.md) select the smallest task owner, not a mandatory chain.
Before training implementation read the [reuse index](docs/training_reuse_index.md)
and actual source; training follows [observability](docs/training_observability_contract.md)
and the [execution envelope](docs/execution_envelope.md).

`templates/` owns reusable templates. `.research/memory/conversations/` holds
append-only conversation logs, not scientific authority. Explicit resumption
reads the full named log. `paper_reading/` and `papers/` retain their source and
writing roles. Independent repositories under `Projects/` keep their ownership.

Proceed with authorized reads, edits and proportionate checks. Commit, push,
external publication, sync, Graph changes and unapproved expensive runs retain
their explicit scope. Finish the deliverable and evidence trace; structural tests
do not prove scientific validity, rendered correctness or reader comprehension.
