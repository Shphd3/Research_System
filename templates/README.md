# Research System Templates

This is the single maintained template area for the research system.

Do not create new reusable templates under `daily_research_reports/`, `docs/`,
`paper_reading/`, or project folders by default. If a template becomes reusable,
put it in the right subfolder here and link to it from the relevant skill,
prompt, or README.

## Folder Map

| Folder | Purpose |
|---|---|
| `research_process/` | Templates for starting, structuring, or continuing a research iteration. |
| `reading/` | Templates for paper, blog, and reading-note work. |
| `meeting/` | Templates for human-completed meeting outlines and private meeting notes. |
| `archive/` | Historical templates kept for compatibility only. |

## Research Process Templates

| Template | Use |
|---|---|
| `research_process/thinking_card_template.md` | Optional human judgment card only when a new mechanism question is promoted. |
| `research_process/daily_report_template.md` | Delayed self-contained experiment story written only after canonical evidence and the researcher's completed result account exist. |
| `research_process/focus_writing_template.md` | Living two-day core-task card: one question, purpose, at most three plain-language methods, expected branches, and later the human-owned result. |
| `research_process/research_loop_folder_template.md` | Standard daily research loop folder structure after a topic becomes an actual iteration. |
| `research_process/experiment_understanding_and_execution_gate_template_cn.md` | Chinese gate from the required four-part explanation through Protocol review, separate run authorization, human result, and delayed Daily Report. |
| `research_process/parking_lot_template.md` | Concise project-level list of important non-active questions and explicit reopening conditions. |

## Reading Templates

Reading templates do not replace research anchors.

| Template | Use |
|---|---|
| `reading/paper_reading_record.md` | Full paper reading record. |
| `reading/paper_blog_reading_record.md` | Blog or informal technical article reading record. |
| `reading/paper_summary_card.md` | Short reading summary card. |

## Meeting Templates

These are meeting-facing preparation and record-keeping surfaces. They do not
replace the anchor, protocol, summary, or detailed evidence record.

| Template | Use |
|---|---|
| `meeting/meeting_focus_template.md` | Optional concise meeting brief or synthesis; ordinary one-problem cycles use their active Focus directly. |
| `meeting/meeting_outline_template.md` | Optional speaking order only after a completed meeting focus and an explicit request. |
| `meeting/meeting_notes_template.md` | Optional short post-meeting note only when the meeting changes judgment or action. |

## Archive

| Template | Status |
|---|---|
| `archive/daily_card_template_0519.md` | Historical daily-card backup. |
| `archive/daily_card_template_0521.md` | Historical daily-card backup. |

## Rules

- Create exactly one active `focus_<problem>.md` after a meeting or explicit
  research reset. It owns the next meeting's core task and persists from design
  through the researcher's result account.
- Create `docs/daily_report_<topic_slug>.md` only after canonical evidence and a
  `HUMAN_RESULT_CONFIRMED` Focus exist. It expands that bounded result into a
  self-contained reasoning story; it is not the source of the Focus.
- Create `focus_meeting_<topic>.md` only for an explicitly requested meeting
  brief or synthesis. A multi-problem synthesis waits for exact human scope,
  exclusions, and one core question.
- Keep non-active key questions in the project's single concise
  `main/parking_lot/README.md`; never run them in parallel with the active task.
- Legacy bare `focus.md` files may remain, but new files use the two patterns
  above unless an explicit migration says otherwise.
- Do not create separate `recordings.md` files by default. Put meeting-derived
  notes and diagnosis in `meeting_notes.md`.
- Historical archive snapshots may contain old template files. Do not use them
  as current templates.
