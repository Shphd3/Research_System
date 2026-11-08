# Depth-allocation actual output assets

<!-- owner: depth_expert_allocation actual registration guide -->

[中文](depth_expert_allocation_20261106_cn.md) · [Current scoped access](checks/20261106T175506021038Z_depth_expert_allocation_full_outputs.json) · [Registration receipt](/data/250010109/MoE_Router/experiments/20261106_depth_expert_allocation/audit/asset_registration_full_20261106T175506021038Z/registration_receipt.json)

| Asset ID | Actual object |
|---|---|
| `checkpoint_family_depth_expert_allocation_smoke_20261106` | 7 complete saved states |
| `data_depth_expert_allocation_formal_frequency_20261106` | exact_supervised_training_exposure_frequency |
| `checkpoint_family_depth_expert_allocation_A_20261106` | 3 complete saved states |
| `checkpoint_family_depth_expert_allocation_B_20261106` | 3 complete saved states |
| `analysis_depth_expert_allocation_20261106` | bounded_single_seed_paired_token_frequency_analysis |

Only cataloged, actually saved objects are listed. All payloads remain in /data/250010109/MoE_Router/experiments/20261106_depth_expert_allocation. The snapshot checks selected output/input read access, not the whole catalog. Scientific acceptance remains Unknown.

The formal-frequency asset counts the fixed future/full target stream defined by the common budget. Its registration does not certify that both models have completed that exposure. Checkpoint members have exact saved step/token counters, full-file SHA256 and size matched to their complete manifests, and CPU meta/mmap schema checks for optimizer, scheduler and all four rank RNG states. Meta inspection does not test model inference.

Exact continuous-versus-external-resume evidence applies only to the actual A Smoke comparison endpoints recorded by replay_micro16.json. Other saved members retain NOT_CHECKED for member-specific external resume. Step0 is a random initialization; no pretrained model weights are inherited. Only the existing tokenizer and DCLM-derived data interface are reused. Smoke and formal states have separate asset identities; registration does not establish semantic long-tail knowledge or a causal routing mechanism.

[Canonical R01 Protocol](../Projects/from-attention-to-search/main/experiments/A15/15_31_depth_expert_allocation/R01_paired_token_frequency/protocol.md) · [Actual member index](/data/250010109/MoE_Router/experiments/20261106_depth_expert_allocation/audit/actual_output_members)


## Temporal routing audit, 2026-11-07

New asset `analysis_depth_expert_allocation_routing_temporal_20261107` preserves the post-hoc inspection of all874 training updates per arm. [Review](/data/250010109/MoE_Router/experiments/20261106_depth_expert_allocation/analysis/routing_audit_20261107/routing_review.md), [manifest](/data/250010109/MoE_Router/experiments/20261106_depth_expert_allocation/analysis/routing_audit_20261107/artifact_manifest.json), and [selected input/output access](checks/20261107_routing_temporal_analysis_access.json) bind the actual saved analysis. No new forward/training occurred. Whole-run zero-receipt experts remain0; transient zero-receipt layer-updates are A2/B37, all during warmup. Later load balance recovers; causality remains Unknown. The new snapshot covers only the parent analysis and this derived output, not all model assets.


## Fixed-weight bias intervention, 2026-11-07

Asset `analysis_depth_expert_allocation_bias_intervention_20261107` registers10existing states and complete same-input DEV routes with retained bias, zero bias on identical hidden states, and a full propagated zero-bias forward. [Review](/data/250010109/MoE_Router/experiments/20261106_depth_expert_allocation/analysis/bias_ablation_20261107_v3/review.md), [manifest](/data/250010109/MoE_Router/experiments/20261106_depth_expert_allocation/analysis/bias_ablation_20261107_v3/artifact_manifest.json), [current scoped access](checks/20261107_bias_ablation_analysis_access.json). No training. All10states exactly match the same-device unmodified evaluator; original four-GPU NLL reproduction at2e-5 remainsFAIL and is explicitly separate. Formal early weights are missing; a numerically qualified local order bound applies to A75/136 and B69/152 concentrated updates. Historical mechanism remainsUnknown.
