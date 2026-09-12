# Templates

This is the only maintained reusable-template area. A template stays here only
when it has a distinct artifact owner and an active caller. Historical or
one-off formats belong in their original records, not in a template archive.

## Current Templates

| Template | Use only when |
|---|---|
| `research_process/task_start_template.md` | The researcher opens a conversation and wants one task clarified and advanced from minimal context. |
| `research_process/focus_writing_template.md` | The researcher activates or resets one workstream question. |
| `research_process/parking_lot_template.md` | A project needs a concise list of consequential inactive questions and has no local format. |
| `research_process/continuation_brief_template.md` | A workstream is handed to a different conversation and needs one current entry point. |
| `reading/paper_summary_card.md` | A paper or essay needs only a first-pass reading record. |
| `reading/paper_reading_record.md` | A paper materially needs deeper argument, formula, or experiment notes. |
| `reading/paper_blog_reading_record.md` | A non-peer-reviewed article materially needs deeper notes. |
| `execution/execution_certificate_template.md` | A job was submitted under `docs/execution_envelope.md` and must certify its resolved tuple, entry point, and monitoring owner. |
| `execution/acp_submit_template.sh` | Any ACP submission. It resolves the tuple from `docs/execution_envelope.md`, dry-runs by default, enforces the gates, and writes a submission receipt. |

## Boundaries

- Templates shape a requested artifact; they do not require an artifact for a
  narrow answer, local diagnosis, or temporary exploration.
- A Focus stores `task_state`, `question_state`, `design_state`, and
  `result_state`. Protocol approval and execution status remain in their own
  files.
- The Anchor is the sole canonical current research design. No template creates
  a parallel `design.md`.
- Meeting and reading templates cannot create or strengthen scientific claims.
- Do not create reusable templates inside `daily_research_reports/`, `docs/`,
  `paper_reading/`, or project folders.
