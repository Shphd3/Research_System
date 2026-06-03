# Research Loop Folder Template

Use this folder shape for a daily sandbox or a small mainline experiment.

```text
00_handwrite_anchor.md
<topic>_anchor.md
01_protocol_for_approval.md
02_execution_plan.md
03_summary.md
04_detailed.md
05_report_card.md
handoff_report.md
figures/
tables/
notes/
archive/
```

## File Roles

`00_handwrite_anchor.md`: rough user judgment. No execution details.

`<topic>_anchor.md`: current research state. Use a subject-bearing name that
matches the research question or mechanism. No raw logs or full implementation
contract.

`01_protocol_for_approval.md`: short pre-run audit surface. AI stops here until
the user approves.

`02_execution_plan.md`: approved implementation contract and stage audit.

`03_summary.md`: first post-run reading path. Short decision report.

`04_detailed.md`: complete evidence ledger and artifact map.

`05_report_card.md`: optional. Meeting/advisor-facing report card derived from
anchor, summary, and detailed. Use
`templates/reporting/report_card_template.md` as the default
template.

`handoff_report.md`: optional legacy name. Prefer packaging existing files with
a short README/index when the user explicitly asks for handoff.

When a handoff report is explicitly requested, this anchor file should also
serve as the local copy of the most important project anchor for that handoff.
Keep the subject-bearing basename; do not rename it to generic `anchor.md`.

`archive/`: old probes or superseded proxies kept for traceability, not for the
main read path.
