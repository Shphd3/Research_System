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
| `research_process/daily_report_template.md` | Full reader-friendly daily experiment or evidence report, with self-contained context, verified results, knowledge update, boundary, and one next decision. |
| `research_process/focus_writing_template.md` | Minimal summary and navigation card derived from one confirmed daily report: one question, concise update, one decisive result, boundary, and one next decision. |
| `research_process/research_loop_folder_template.md` | Standard daily research loop folder structure after a topic becomes an actual iteration. |
| `research_process/experiment_understanding_and_execution_gate_template_cn.md` | Four minimal Chinese cards for understanding, self-check, execution gating, and result reporting. |

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
| `meeting/meeting_focus_template.md` | Required concise meeting update: one named problem proceeds directly; multi-problem synthesis first fixes human scope and one core question. |
| `meeting/meeting_outline_template.md` | Optional speaking order only after a completed meeting focus and an explicit request. |
| `meeting/meeting_notes_template.md` | Optional short post-meeting note only when the meeting changes judgment or action. |

## Archive

| Template | Status |
|---|---|
| `archive/daily_card_template_0519.md` | Historical daily-card backup. |
| `archive/daily_card_template_0521.md` | Historical daily-card backup. |

## Rules

- Create `focus_<problem>.md` only when that problem reaches a bounded knowledge
  update and its source daily report is human-confirmed; several problem
  focuses may exist on one day.
- Create `docs/daily_report_<topic_slug>.md` for each completed
  experiment or bounded evidence synthesis delivered as a daily knowledge
  update. It is the full reader explanation derived from canonical evidence;
  the problem focus is its minimal summary and navigation card.
- Create a new `focus_meeting_<topic>.md` for every meeting. A named one-problem
  meeting uses a progressive question chain directly; a multi-problem meeting
  waits for exact human scope, exclusions, and one core question.
- Legacy bare `focus.md` files may remain, but new files use the two patterns
  above unless an explicit migration says otherwise.
- Do not create separate `recordings.md` files by default. Put meeting-derived
  notes and diagnosis in `meeting_notes.md`.
- Historical archive snapshots may contain old template files. Do not use them
  as current templates.
