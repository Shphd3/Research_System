# Protocol Focus And Anchor Alignment

Use for Protocol work. Audit-only tasks inspect these requirements without
promoting, reopening or rewriting scientific records.

## Confirmed Core-Task Focus

Before drafting a Protocol, require one active
`daily_research_reports/MMDD/focus_<problem>.md` whose four-part **plain
language** design is explicitly researcher-confirmed:

```text
1. core question and its boundary
2. experiment purpose, dependent subquestions, and completion standard
3. at most three plain-language analysis steps
4. expected supporting, non-supporting, and insufficient outcome branches
```

The Focus carries the plain-language version; this Protocol carries the
**precise** version of the same four parts — exact settings, thresholds,
registered criteria, and audit blocks. The two must not contradict each other.
When they differ, the Protocol governs execution and the Focus governs what the
researcher intended.

The Focus may name at most three core experiments and should normally name one.
Controls, nulls, robustness checks, and leakage guards that protect the same
verdict remain supporting analyses inside that experiment. If the Focus is
missing, unconfirmed, or inconsistent with the Anchor, stop and route the
conflict to `research-sync-gate` or `problem-anchor-writer`.

If the researcher adopts a material revision to the Focus's plain-language
method, completion rule or expected branches, record
`design_state: AWAITING_HUMAN_CONFIRMATION` and record the reason in prose. A
separately confirmed core question may remain confirmed, but the Protocol
cannot be promoted until the revised four-part design is confirmed again.

Use confirmations already present in the session or owning records; do not
require another intake or approval just to satisfy a form. A missing scientific
prerequisite blocks its dependent drafting/promotion, not independent evidence
or consistency auditing. Report the exact missing decision; do not create or
reset a Focus on the researcher's behalf. An AI-proposed correction alone is
not a human scientific state transition.
