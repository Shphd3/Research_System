# Protocol: A15_13_E17 DCLM SAE Candidate Hierarchy Reproduction

## 0. Approval Snapshot

```text
Document status: APPROVED_FOR_FULL_RUN
Approval status: researcher explicitly requested candidate hierarchy reproduction after reviewing the method
Block audit status: A-G CONFIRMED
Cross-block consistency: PASS
Execution scope approved: implementation, tests, one full bounded graph run, rendering, and evidence records
Design frozen at: 2026-09-04 UTC
Purpose: reproduce the senior project's hierarchy construction and visual form on the completed E16 SAE
Primary Anchor: 15_13_08_dclm_sae_candidate_hierarchy_anchor.md
Experiment role: method construction and structural qualification
Primary output: discovery maximum depth and count of frozen relations passing disjoint-source replication
Cannot claim: semantics, causal composition, layer placement, Router or expert utility, or task gain
```

## 1. Terminology / Definitions

- A feature firing is a positive value among the SAE's retained Top-32 activations for one token.
- A candidate containment edge points from a rarer proposed composite feature to a more frequent proposed constituent feature.
- Replication means recomputing a frozen discovery relation on the separate DCLM validation source without changing its endpoints or thresholds.
- Hierarchy depth is longest-path depth in the directed candidate graph; it is not semantic depth.

## 2. Anchor Alignment

This experiment tests only whether the E16 dictionary supports a reproducible candidate containment graph. It does not use M2D2 labels and cannot select Router or LoRA layers.

## 3. Tested Hypothesis

The discovery graph will be acyclic and contain at least one chain of depth two or greater, and at least one frozen relation will retain its asymmetric containment pattern on the replication source. The rival is that the apparent hierarchy is flat, cyclic, empty, or sample-specific.

## 4. Rival Explanations

- Firing-frequency imbalance can make common features appear to be constituents.
- Repeated local text can create discovery-only co-activation.
- A dense all-pairs implementation can silently truncate or miscount relations.
- A visually dense graph can hide that no edge independently replicates.

## 5. Data Construction And Provenance

- Discovery: 256 deterministic 1,024-token windows, totaling 262,144 raw tokens, from `/data/250010109/training_data_views/dclm_pair_v1/train`.
- Replication: 256 deterministic 1,024-token windows, totaling 262,144 raw tokens, from `/data/250010109/training_data_views/dclm_pair_v1/validation/validation.bin`.
- Four ranks each process disjoint windows from both sources.
- The training and validation sources are disjoint. No M2D2 labels, task labels, or historical graph edges enter selection.
- The same 0.999 within-batch norm-outlier filter used by E16 is retained and its removed fraction is reported.

## 6. Learning Task And Permitted Supervision

There is no learning. The frozen base model and frozen SAE produce sparse activations. Discovery activations select relations; replication activations only evaluate frozen relations.

## 7. Model / Architecture And Frozen Variants

- Base: frozen Qwen3-0.6B-Base.
- State: zero-based layer 27 MLP forward pre-hook, width 1,024.
- SAE: E16 final checkpoint SHA-256 `e4e2049aced8ba9a3b043bbb2b3308b497b7ec22f107531e37197873ee545b65`.
- Dictionary: 30,000 ReLU features with Top-32 retention.

## 8. Training Objective And Optimization

Not applicable. No parameter is trainable and no optimizer is instantiated.

## 9. Conditions, Seeds, And Checkpoints

- Sampling seed: 1704.
- Windows per source: 256.
- Sequence length: 1,024.
- Constituent pool: 4,096 most frequent discovery features.
- Minimum discovery composite count: 100.
- Minimum individual containment: 0.98.
- Maximum reverse containment: strictly below 0.98.
- Minimum constituent/composite frequency ratio: 1.5.
- Constituents per composite: 2 to 8.
- Minimum joint containment: 0.90.
- Replication: minimum constituent-given-composite 0.90, maximum composite-given-constituent 0.60, minimum joint gain 0.02.

The historical figure's unexplained scalar threshold 0.5 is not used as a substitute for these documented rules.

## 10. Primary Metric And Frozen Analysis Plan

The unit of observation is a token activation row; the independent source unit is the DCLM source split. The graph is `NONTRIVIAL_REPLICATED` when it is acyclic, discovery maximum depth is at least two, and at least one composite group passes all replication thresholds. It is `FLAT_OR_EMPTY` when the valid discovery graph has maximum depth below two. It is `UNSTABLE_REPLICATION` when discovery depth is at least two but no group passes replication. Cache, identity, cycle, or rendering failures yield `INSUFFICIENT`.

## 11. Secondary Metrics And Guards

- Positive features per retained token must equal 32 within numerical validity.
- Report feature firing counts, candidate groups and edges, replicated groups and edges, role counts, component counts, and node counts by depth.
- Candidate and replication-qualified graphs must be rendered separately from the same edge table.
- Exact historical counts are descriptive only and never a gate.

## 12. Known Good / Known Bad / Known Confusing Cases

- Known good synthetic case: nested activation sets produce the expected directed chain and depth.
- Known bad case: discovery containment that reverses on replication must not pass.
- Known confusing case: two equally frequent features with symmetric co-activation must not be assigned a directed relation.

## 13. Scientific Procedure And Stage Contracts

| Stage | Goal | Input | Operation | Output | Stop rule |
| --- | --- | --- | --- | --- | --- |
| 1 | Verify identities | model, checkpoint, DCLM files | hash and shape checks | preflight receipt | stop on mismatch |
| 2 | Cache activations | two DCLM sources | four-rank frozen forward extraction | rank-local and merged sparse caches | stop on nonfinite or wrong Top-32 shape |
| 3 | Select relations | discovery cache only | documented asymmetric containment and greedy group rule | frozen candidate table | stop on counting/schema failure |
| 4 | Replicate | frozen candidates and validation cache | recompute registered relation metrics | qualified flags and summary | no reselection allowed |
| 5 | Render | one frozen edge table | longest-path levels and PDF-style layout | candidate and replicated figures | stop on cycle or missing artifact |

## 14. Algorithm, Output, And Provenance Contract

Worker root: `/data/250010109/MoE_Router/experiments/20260904_a15_13_e17_sae_hierarchy`.

Required outputs:

```text
activation_cache/discovery_indices.npy
activation_cache/discovery_values.npy
activation_cache/replication_indices.npy
activation_cache/replication_values.npy
tables/composition_candidates.csv
tables/feature_nodes.csv
tables/feature_edges.csv
figures/candidate_hierarchy.png
figures/replicated_hierarchy.png
hierarchy_summary.json
logs/preflight.log
logs/run.log
```

The run uses one reserved four-H100 ACP node, worker spec `n6ls.iu.i40.4`, one worker node, and no retry. Raw caches and logs remain on the worker surface; only curated tables and figures may be referenced from Research_System result records.

## 15. Success / Failure / Insufficient Evidence

- Pass: `NONTRIVIAL_REPLICATED`.
- Scientific negative: `FLAT_OR_EMPTY` or `UNSTABLE_REPLICATION`.
- Insufficient: any identity, cache, cycle, schema, execution, or artifact failure.

## 16. What This Cannot Claim

Neither visual similarity nor a pass proves semantic hierarchy, coarse/fine granularity, feature causality, online routing, expert specialization, or language-model benefit.

## 17. Block Confirmation, Freeze, And Amendment Ledger

| Block | State | Basis |
| --- | --- | --- |
| A | CONFIRMED | user requested this bounded hierarchy reproduction and accepted non-exact counts |
| B | CONFIRMED | prior explained DCLM discovery/replication design; user authorized execution |
| C | CONFIRMED | frozen activation analysis only |
| D | CONFIRMED | completed E16 model and checkpoint |
| E | CONFIRMED | no learning |
| F | CONFIRMED | candidate versus replication graph and no exact-count gate |
| G | CONFIRMED | inherited experiment-two reserved four-H100 resource and explicit run request |

Cross-block consistency: `PASS`. No post-start scientific amendments are permitted without an append-only record.

Execution receipt, 2026-09-04 01:26 UTC: the approved ACP create request was rejected before a job was created with `MEMBER_QUOTA_EXCEEDED`. The requested additional four H100 GPUs and 88 CPU cores had zero remaining member quota because the separately owned layerwise-MoE task was already using the reserved four-H100 allocation. No E17 data were processed and the frozen scientific design is unchanged. A different resource profile requires explicit researcher approval; otherwise resubmit unchanged after the reserved allocation is released.

Execution receipt, 2026-09-04 02:34 UTC: after the reserved allocation was released, ACP job `pt-gsrtu3dp` started the unchanged contract but failed during the first sparse-activation export because PyTorch bfloat16 tensors cannot be converted directly to NumPy. The run produced no candidate table or result and is ineligible. A regression test was added first, then the export path was changed to convert through float32 before saving float16. This was an implementation-only repair; data, model, checkpoint, thresholds, and all decision rules remained frozen.

Execution receipt, 2026-09-04 02:37--02:42 UTC: the repaired, scientifically unchanged job `pt-3c60qjz3` succeeded on one reserved four-H100 node. Run `full-20260904T023742Z` produced every required cache, table, summary, and figure. The registered verdict is `NONTRIVIAL_REPLICATED`: discovery has 1,212 groups, 2,616 edges, 1,279 nodes, and maximum depth two; the disjoint replication source retains 24 groups, 91 edges, 53 nodes, and maximum depth two. The result records are [summary.md](summary.md) and [detailed.md](detailed.md).
