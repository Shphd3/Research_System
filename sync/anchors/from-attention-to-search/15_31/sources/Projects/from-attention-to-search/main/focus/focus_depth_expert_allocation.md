# Does moving fixed expert capacity toward depth improve infrequent-token learning?

```text
problem_key: depth_expert_allocation
anchor_id: 15_31
task_state: AUTHORIZED_PAIR_AND_REPORTS_COMPLETE
question_state: USER_ACTIVATED
design_state: USER_SCOPE_WITH_JOINT_ENGINEERING_FREEZE_COMPLETE
result_state: PAIRED_MEASUREMENTS_COMPLETE_PENDING_RESEARCHER_JUDGMENT
human_result_judgment: Unknown
```

## Question, hypothesis and boundary

The researcher asks whether moving experts from shallow to deep layers, with equal total parameters and top-k/expert width and the same training data order and token budget, improves relatively infrequent-token prediction while retaining overall language modeling. The rival is no benefit or a frequency-group trade-off. Token frequency is a proxy; semantic long-tail knowledge and causal expert mechanisms are separate questions.

## Necessary comparison and existing evidence

One core experiment compares an eight-layer uniform ordinary MoE with a deep-increasing MoE. The researcher explicitly authorized design, source/data checks, jointly feasible short tests, a frozen common budget, full A/B training and evaluation on four reserved H100 GPUs in the current 6 November request. No repeated permission is required for that scope. The final configuration is frozen after both smoke tests; a failure blocks the dependent stage rather than fabricating completion.

The at-most-three plain-language steps are: (1) audit parameters, common initialization, data exposure and buckets; (2) qualify both models, freeze and complete a common budget; (3) compare the registered low-frequency endpoint with overall/high-frequency costs, compute and route loads. Completion requires both budgets and the full evidence trail or an explicit failure record.

A reliable low-frequency improvement supports further validation; improvement with general loss identifies a trade-off; no observed advantage weakens this allocation; broken fairness or missing evidence leaves it insufficient. Evaluation intervals cannot replace training seeds. The advisor's allocation intuition is not already a measured result. Prior SAE findings do not establish semantic or causal benefit for this architecture.

## Researcher judgment and one next decision

Scientific acceptance, mechanism judgment and question closure remain Unknown. The one next decision after the bounded paired result is whether its measured potential warrants later entity/relation and representation or functional validation. No later architecture or intervention starts automatically.

## Sources

[Anchor](../problem_anchors/15_spectral_representation_and_functional_routing/15_31_depth_expert_allocation/15_31_depth_expert_allocation_anchor.md) · [Protocol](../experiments/A15/15_31_depth_expert_allocation/R01_paired_token_frequency/protocol.md). Results are NOT RUN at registration; factual result records will preserve failures and missing outputs. Exact execution choices belong to Protocol, not this Focus.

Current execution facts: A and B each completed 229,113,856 valid targets, 874 updates and all initial/midpoint/endpoint evaluations. See the [joint freeze](../experiments/A15/15_31_depth_expert_allocation/R01_paired_token_frequency/joint_freeze.md) and result-owning [Summary](../experiments/A15/15_31_depth_expert_allocation/R01_paired_token_frequency/summary.md). Observed endpoint B minus A is +0.217210 nat/token for low frequency and +0.014258 overall: B is worse in this measured pair. Actual output registration, independent audit and reports are complete; scientific acceptance, mechanism judgment and continuation remain researcher decisions.
