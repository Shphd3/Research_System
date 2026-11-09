# A12 Experiment Registry

A12 experiments follow the parent-anchor hierarchy:

```text
A12_<parent>_<subanchor>_E<experiment>
```

| Parent group | Main decision evidence | Canonical anchor |
|---|---|---|
| [`12_0_short_range_single_vs_two_step_composition/`](12_00_short_range_single_vs_two_step_composition) | With length and answer distance fixed, is MTP's standard-head training-speed gain larger for two-step composition than for one-step application? [E02](12_00_short_range_single_vs_two_step_composition/A12_0_E02_in_support_capability_calibration/summary.md) was positive only at exact fit; E03 was rejected for asymmetric query-relevant structure; [E04](12_00_short_range_single_vs_two_step_composition/A12_0_E04_balanced_per_sample_dual_map/summary.md) completed NTP-only Stage A but failed both shared capability and row-removal validity. | [`12_0`](../../problem_anchors/12_structured_compositional_mtp_workload/12_00_short_range_single_vs_two_step_composition/12_00_short_range_single_vs_two_step_composition_anchor.md) |
| [`12_01_compositional_workload_capability_gate/`](12_01_compositional_workload_capability_gate) | Is the workload valid, and can the shared checkpoint solve it? | [`12_01`](../../problem_anchors/12_structured_compositional_mtp_workload/12_01_compositional_workload_capability_gate/12_01_compositional_workload_capability_gate_anchor.md) |
| [`12_02_interference_capacity_curriculum_boundary/`](12_02_interference_capacity_curriculum_boundary) | Can missing rank cause the tradeoff, and can curriculum repair it? | [`12_02`](../../problem_anchors/12_structured_compositional_mtp_workload/12_02_interference_capacity_curriculum_boundary/12_02_interference_capacity_curriculum_boundary_anchor.md) |
| [`12_03_standard_head_causal_use/`](12_03_standard_head_causal_use) | After the capability gate, does informative Next-2 increase causal use by the common standard head? | [`12_03`](../../problem_anchors/12_structured_compositional_mtp_workload/12_03_standard_head_causal_use/12_03_standard_head_causal_use_anchor.md) |

Repository-code transfer, neural scale effects, deeper trees, and capacity-sufficient curriculum remain parked. The immediate `12_0` decision is whether to close E04 or reopen carrier/capability design under a new Protocol; no MTP or `12_03` causal-use work is admissible before a valid shared capability gate passes.
