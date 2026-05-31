# Research Loop Folder Template

Use this folder shape for a daily sandbox or a small mainline experiment.

```text
00_handwrite_anchor.md
anchor.md
01_protocol_for_approval.md
02_execution_plan.md
03_summary.md
04_detailed.md
05_report_card_for_advisor.md
figures/
tables/
notes/
archive/
```

## File Roles

`00_handwrite_anchor.md`: rough user judgment. No execution details.

`anchor.md`: current research state. No raw logs or full implementation
contract.

`01_protocol_for_approval.md`: short pre-run audit surface. AI stops here until
the user approves.

`02_execution_plan.md`: approved implementation contract and stage audit.

`03_summary.md`: first post-run reading path. Short decision report.

`04_detailed.md`: complete evidence ledger and artifact map.

`05_report_card_for_advisor.md`: 60-second advisor-facing card derived from
anchor, summary, and detailed.

`archive/`: old probes or superseded proxies kept for traceability, not for the
main read path.
