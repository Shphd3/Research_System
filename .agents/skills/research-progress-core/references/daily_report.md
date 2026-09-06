# Delayed Daily Report

Use this reference only after canonical evidence exists and the researcher has
confirmed the direct result, boundary, knowledge update, and next decision in
the active Focus.

Create or update:

```text
daily_research_reports/MMDD/docs/daily_report_<topic_slug>.md
```

Use `templates/research_process/daily_report_template.md`. The report is a
self-contained explanation of one adjudicated question. It is derived from the
Anchor, frozen Protocol, `summary.md`, `detailed.md`, and human-confirmed Focus;
it is not another evidence owner or run ledger.

## Reader Order

Write the argument once:

```text
question-form title and exact sources
-> short abstract with question, decisive result, boundary, next decision
-> necessary objects and why the previous evidence was insufficient
-> method distinction and registered comparison
-> direct results and decision-bearing visuals
-> inference, cannot-claim boundary, and exactly one next decision
```

Define only terms needed to judge the result. State data splits, statistical
unit, aggregation, and any reused frozen asset when they affect eligibility.
Keep commands, retries, receipts, hashes, full tables, and artifact inventories
in `detailed.md` unless one changes how the result can be interpreted.

Use the smallest sufficient set of tables or figures. Put each visual beside
the conclusion it supports and explain in one sentence how to read its axes,
unit, comparison, and boundary. Preserve negative results, deviations, and
uncertainty; never turn `Fail` or `Insufficient` into progress language.

Keep `AI_DRAFT_AWAITING_HUMAN_CONFIRMATION` visible until the researcher
confirms the report wording. Completion requires agreement with all canonical
values and boundaries, readable decision-bearing visuals, and no duplicated
verdict section or new claim.
