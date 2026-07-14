# A12: Structured Compositional MTP Workload

A12 asks when the objective-level signal isolated by A11 becomes functionally useful on a task that requires dispersed evidence, an intermediate state, and ordered composition.

Current story:

- [English canonical story](../../../../Projects/from-attention-to-search/main/stories/12_structured_compositional_mtp_workload/01_structured_composition_workload_and_standard_head_use.md)
- [Chinese companion](../../../../Projects/from-attention-to-search/main/stories/12_structured_compositional_mtp_workload/01_structured_composition_workload_and_standard_head_use_cn.md)

## Terminology / Definitions

| Term | Plain meaning | Concrete object | Why it matters | Cannot prove |
|---|---|---|---|---|
| computation tree | evidence is combined through explicit intermediate states before the root answer is produced | $Z_v=g_v(Z_{c_1},\ldots,Z_{c_k})$ | formalizes coupling, order, and staged aggregation | that a network internally uses the same tree |
| depth-two path | the smallest serial instance of the tree | $A\xrightarrow{\pi_1}B\xrightarrow{\pi_2}Y$ | isolates binding and ordered composition | multi-branch aggregation |
| capability gate | one shared checkpoint solves unseen full-context examples and fails the intended partial-evidence controls | held-out accuracy plus evidence guards | prevents objective comparison on an unlearned task | why the task was learned |
| causal use | changing only an intermediate-state component changes the common standard-head answer as predicted | cross-fitted hidden-state intervention | distinguishes readable information from functional reliance | real-benchmark transfer |

## Parent Anchors

| Order | Parent anchor | Stable knowledge update | Status |
|---|---|---|---|
| 1 | [12_01 Workload and capability gate](12_01_compositional_workload_capability_gate/12_01_compositional_workload_capability_gate_anchor.md) / [中文](12_01_compositional_workload_capability_gate/12_01_compositional_workload_capability_gate_anchor_cn.md) | The two-table depth-two path validly removes single-table shortcuts, but the tested from-scratch small Transformers did not learn it. | workload supported; learner branch closed |
| 2 | [12_02 Capacity and curriculum boundary](12_02_interference_capacity_curriculum_boundary/12_02_interference_capacity_curriculum_boundary_anchor.md) / [中文](12_02_interference_capacity_curriculum_boundary/12_02_interference_capacity_curriculum_boundary_anchor_cn.md) | Missing representation rank is a sufficient tradeoff mechanism in the oracle linear model; dose-matched curriculum cannot create rank. | completed; neural transfer untested |
| 3 | [12_03 Standard-head causal use](12_03_standard_head_causal_use/12_03_standard_head_causal_use_anchor.md) / [中文](12_03_standard_head_causal_use/12_03_standard_head_causal_use_anchor_cn.md) | First establish one shared task-capable checkpoint, then compare NTP and informative Next-2 through the same standard head and intervene on intermediate state $B$. | active design |

The line is read as

$$
\text{valid structured workload}
\rightarrow
\text{shared capability gate}
\rightarrow
\text{common-head objective comparison}
\rightarrow
\text{intermediate-state causal use}.
$$

Repository-code transfer, neural scale laws, deeper trees, and capacity-sufficient curriculum are parked. They become eligible only after 12_03 passes its shared capability gate.

## Claim Boundary

A12 establishes a valid depth-two joint-evidence workload, a failed current from-scratch learner branch, and a controlled linear missing-rank mechanism. It does not establish neural causal use, MTP superiority, general tree reasoning, a model-scale law, curriculum benefit in a capacity-sufficient regime, real-workload transfer, or Router/MoE value.

## Exactly One Next Decision

Review the [12_03 protocol](../../../../Projects/from-attention-to-search/main/experiments/A12/12_03_standard_head_causal_use/A12_03_E01_standard_head_causal_use/protocol.md), then run only its shared capability gate. If the gate fails, do not compare NTP with informative Next-2 and do not interpret hidden-state patches.

Decision-bearing evidence is indexed in [the A12 experiment registry](../../../../Projects/from-attention-to-search/main/experiments/A12/README.md).
