# Thinking Card — Workload Validity And Learner-Eligibility Guard

> Migrated from [12_01_01_workload_validity_and_learner_guard_anchor.md](12_01_01_workload_validity_and_learner_guard_anchor.md) without changing the historical judgment. This file is the human-facing source; the anchor owns formal design and evidence.

**Phenomenon:** The data distribution requires two evidence tables, but the tested small from-scratch learners solve only the output format.
**Mechanism guess:** the workload is valid; the present checkpoint lacks held-out composition capability.
**Key variables:** full-context accuracy, single-table accuracy, evidence-swap consistency, format accuracy.
**Causal relation:** remove or replace one evidence table and compare the predicted answer change.
**Observable metric:** full-context held-out answer accuracy, guarded by partial-evidence controls.
**Rival explanations:** single-table shortcut; tokenizer/interface failure; objective effect.
**Decision:** accept the workload, close further tuning of this from-scratch branch, and require a capable shared checkpoint.
