# E2-D Router Supervision Diagnostic

This folder records a diagnostic branch for E2 MoE feature separation.

The experiment removes spectral projection and uses uniform-frequency all-trigram data. It adds a supervised router auxiliary loss using true synthetic feature labels. The purpose is to check whether the current MoE implementation can form clean specialization when the router is explicitly told which feature each prefix-end hidden state belongs to.

Read:

1. `purpose_card.md` - why this diagnostic exists.
2. `execution_plan.md` - exact run setup and pass/fail criteria.
3. `summary.md` - result closure after the run.
4. `detailed.md` - longer tables and figure index.
