# A06 Experiment Registry

The experiment tree follows the active parent-anchor hierarchy. The identifier
format is:

```text
A06_<parent>_<subanchor>_E<experiment>
```

The directory name is the current research identity. Historical runner names,
remote job identifiers, and result directory names may remain in artifact maps
only when they are required for reproduction.

| Parent experiment group | Question answered | Canonical anchor |
|---|---|---|
| [`06_00_functional_specialization_contract/`](06_00_functional_specialization_contract) | What evidence distinguishes a route partition from functional specialization? | [`A06_00`](../../problem_anchors/06_geometry_proxy_preservation/06_00_functional_specialization_contract/06_00_functional_specialization_contract_anchor.md) |
| [`06_01_geometry_and_state_discovery/`](06_01_geometry_and_state_discovery) | Can route-relevant geometry be reached and found without privileged state labels? | [`A06_01`](../../problem_anchors/06_geometry_proxy_preservation/06_01_geometry_and_state_discovery/06_01_geometry_and_state_discovery_anchor.md) |
| [`06_02_partition_preservation_dynamics/`](06_02_partition_preservation_dynamics) | Which signed dynamics preserve, cross, or restore a supplied partition? | [`A06_02`](../../problem_anchors/06_geometry_proxy_preservation/06_02_partition_preservation_dynamics/06_02_partition_preservation_dynamics_anchor.md) |
| [`06_03_utility_binding_and_sparse_discovery/`](06_03_utility_binding_and_sparse_discovery) | How do expert functions form, and how can sparse feedback discover them? | [`A06_03`](../../problem_anchors/06_geometry_proxy_preservation/06_03_utility_binding_and_sparse_discovery/06_03_utility_binding_and_sparse_discovery_anchor.md) |
| [`06_04_real_workload_utility_headroom/`](06_04_real_workload_utility_headroom) | Does a registered real-code surface contain split-stable positive expert-utility headroom? | [`A06_04`](../../problem_anchors/06_geometry_proxy_preservation/06_04_real_workload_utility_headroom/06_04_real_workload_utility_headroom_anchor.md) |

`A06_04_01_E01_context_conditioned_expert_utility` is complete and failed on
its registered CrossCodeEval final-layer surface: context interaction passed,
but calibration identity stability and positive absolute headroom failed. See
[`summary.md`](06_04_real_workload_utility_headroom/A06_04_01_E01_context_conditioned_expert_utility/summary.md)
and
[`detailed.md`](06_04_real_workload_utility_headroom/A06_04_01_E01_context_conditioned_expert_utility/detailed.md).

The cross-run synthesis for the real-proxy subanchor is
[`06_01_04_real_proxy_full02_rerun_report.md`](06_01_geometry_and_state_discovery/06_01_04_real_proxy_full02_rerun_report.md).

## Raw Artifact Retention Notice

On 2026-08-09, after explicit researcher approval, the untracked raw `runs/`
subtrees embedded in the `source_bundle` directories of
`A06_01_01_E01_common_filtered_spectrum`,
`A06_01_01_E02_cross_checkpoint_common_replay`, and
`A06_01_01_E03_freeze_split_common_stability` were permanently removed.  They
occupied 636,803,403,776 bytes and consisted primarily of checkpoints and full
run state.  The canonical Protocols, summaries, detailed records, scripts,
figures, and tables remain in this experiment tree; the deleted raw states are
not locally recoverable.

Future checkpoints, optimizer state, activation caches, and full run outputs
must stay in the worker or cluster workspace.  Only curated evidence needed by
the canonical result records belongs under `main/experiments/`.
