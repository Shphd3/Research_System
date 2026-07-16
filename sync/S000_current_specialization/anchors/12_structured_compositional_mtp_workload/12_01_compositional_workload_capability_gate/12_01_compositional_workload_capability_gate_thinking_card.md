# Thinking Card — Compositional Workload And Capability-Gate Anchor

> Migrated from [12_01_compositional_workload_capability_gate_anchor.md](12_01_compositional_workload_capability_gate_anchor.md) without changing the historical judgment. This file is the human-facing source; the anchor owns formal design and evidence.

**Phenomenon:** A long context is not necessarily a long-range reasoning task. The relevant case requires remote evidence that remains necessary after local context is known and must be combined through an intermediate state.

**Mechanism guess:** A two-table composition task isolates this computational skeleton while removing lexical shortcuts. It is useful only if the tested model can first learn the task.

**Observable metric:** full-context held-out answer accuracy, guarded by single-table and evidence-intervention controls.

**Decision:** accept the workload construction, reject further tuning of the current from-scratch learner, and require a capable shared checkpoint before objective comparison.
