# Common and domain-specific natural-language update geometry

[Day index](README.md) · [Current Summary](docs/domain_update_geometry/summary.md) · [Meeting report](meeting_report_shared_update.md) · [中文](focus_domain_update_geometry_cn.md)

~~~text
type: meeting_cycle_core_task
problem_key: domain_update_geometry
task_state: ANALYSIS_DELIVERED
question_state: HUMAN_CONFIRMED
design_state: HUMAN_CONFIRMED_DIRECTION_WITH_DELEGATED_OPERATIONALIZATION
result_state: MEASURED_BOUNDED
human_result_judgment: Unknown
core_experiment_count: 1
anchor: daily_research_reports/0930/docs/domain_update_geometry/anchor.md
protocol: daily_research_reports/0930/docs/domain_update_geometry/protocol.md
~~~

**Question and purpose.** At a fixed S7 state, do four predefined natural-text domains have reproducible local update differences beyond the pooled mean? How do SVD and trained SAE activation relate to those differences? Understand update geometry before deciding on another representation-only predictor.

**Hypothesis and rival.** Fit domain means should describe heldout gradients better than the pooled mean. Recurring activity need not imply recurring mean updates; weak domain differences and high-dimensional estimation error remain unresolved alternatives.

**Three analyses delivered.** Compare pooled/domain means; examine common/domain/within variation and aggregation scales with SVD and controls; characterize all SAE atoms and check fit-selected common/enriched patterns and decoder-span coverage on readout. Exact methods belong to the [Protocol](docs/domain_update_geometry/protocol.md).

| Round | Result and boundary |
| --- | --- |
| One completed domain-analysis round; R2 result text | Domain-average activity recurs, but the current domain-mean descriptor gives no gain. Uncalibrated bootstrap coverage leaves population directional inference insufficient; absent domain structure is not established. |

The [Summary](docs/domain_update_geometry/summary.md) owns the complete conclusion and [Detailed](docs/domain_update_geometry/detailed.md) the evidence. Program NON_SUPPORT is preserved. Qualified reproducible improvement supports the mean relation, qualified precise non-improvement weakens it, and unqualified inference remains insufficient. Spectral/SAE outcomes do not substitute for the primary comparison.

**One next decision, still pending.** Is prospective readout of domain-associated updates justified, or should grouping and scale first be clarified? The existing AI suggestion is to compare total domain association with additional association under comparable targets, after qualifying estimation and common support. It is not a new Focus or executable follow-up design.

**Authority and boundary.** Existing delegation and operational completion are documented in the [execution record](docs/domain_update_geometry/execution_record.md) and [receipt](docs/domain_update_geometry/evidence/completion_receipt.json). Scope remains a fixed model's final attention matrix, pure next-token loss and a historical academic panel. No semantic causality, representation-only prediction success, finite-step natural-text harm, isolation benefit or router gain follows. The older controlled Focus and [natural-NTP prediction result](docs/summary.md) remain separate.

Formal design: [Anchor](docs/domain_update_geometry/anchor.md). Reorganized on 2026-09-30 (Asia/Shanghai), preserving the question, existing state fields and pending researcher judgment.
