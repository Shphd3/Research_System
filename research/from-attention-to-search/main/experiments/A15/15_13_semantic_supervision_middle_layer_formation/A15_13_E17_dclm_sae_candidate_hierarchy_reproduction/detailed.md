# A15_13_E17 Detailed Evidence: DCLM SAE Candidate Hierarchy Reproduction

```text
Execution status: FULL_RUN_COMPLETE
Evidence eligibility: ELIGIBLE
Typed verdict: NONTRIVIAL_REPLICATED
Knowledge wording: AI_DRAFT_AWAITING_HUMAN_CONFIRMATION
```

## 1. Question And Registered Decision

E17 asks whether the technically qualified E16 final-layer sparse autoencoder supports a non-flat, acyclic candidate activation-containment graph and whether at least one frozen discovery relation survives an independent DCLM source. The registered pass requires discovery maximum depth at least two and at least one replication-qualified composite group. It does not require the historical node count or historical depth.

## 2. What Actually Ran

This experiment had no training stage. Qwen3-0.6B-Base and the E16 SAE were frozen throughout; no optimizer or trainable parameter existed.

| Stage | Trainable / frozen objects | Data pass and update count | Objective / learning rate | Checkpoint or handoff |
|---|---|---|---|---|
| Identity and tests | all objects frozen | no corpus pass; 4 synthetic tests; 0 optimizer updates | not applicable | proceed only after model and SAE identity checks |
| Discovery cache | base and SAE frozen | 256 windows x 1,024 raw tokens; 0 updates | Top-32 sparse activation extraction; no learning rate | rank-local caches merged into one discovery cache |
| Candidate selection | no model execution | one pass over the merged discovery cache | registered asymmetric-containment rules | endpoints and thresholds frozen before replication |
| Replication cache and evaluation | base and SAE frozen | separate 256 windows x 1,024 raw tokens; 0 updates | evaluate frozen candidates; no reselection | replication flags and graph emitted |
| Rendering | no model execution | one pass over each edge table | longest-path layout | candidate and qualified figures |

The treatment-like comparison is discovery-selected relations versus those same frozen relations on a disjoint source. There is no learned Baseline, Oracle, semantic label, or task-performance condition in E17. Synthetic known-good, relation-breaking, cycle, and bfloat16-export tests protect implementation validity rather than serve as scientific controls.

## 3. Inputs And Identities

- Base model: `/data/250010109/model_cache/Qwen3-0.6B-Base-official`.
- Model config SHA-256: `504a6b58c4271583724e66584b6b7698aea18450209df6b2f7582df0e89cee59`.
- Activation point: zero-based layer 27 MLP input, width 1,024.
- SAE checkpoint: `/data/250010109/MoE_Router/experiments/20260903_a15_13_e16_dclm_final_layer_sae/runs/full-20260903T150734Z/sae_full_final.pt`.
- SAE SHA-256: `e4e2049aced8ba9a3b043bbb2b3308b497b7ec22f107531e37197873ee545b65`.
- Discovery source: DCLM training view with 2,419 files.
- Replication source: `/data/250010109/training_data_views/dclm_pair_v1/validation/validation.bin`.
- Seed: 1,704; four ranks; 256 windows per source; sequence length 1,024.

Discovery processed 262,144 raw tokens and retained 261,632 after the registered 0.999 within-batch norm filter. Replication processed 262,144 raw tokens and retained 261,634. Every retained token had exactly 32 positive SAE features.

## 4. Frozen Construction

Candidate constituents were restricted to the 4,096 most frequent discovery features. A discovery composite needed at least 100 firings, two to eight constituents, minimum individual containment 0.98, reverse containment below 0.98, constituent/composite frequency ratio at least 1.5, and joint containment at least 0.90. Frozen candidates passed replication only when minimum constituent-given-composite was at least 0.90, maximum composite-given-constituent was at most 0.60, and joint gain was at least 0.02.

The unexplained historical scalar threshold 0.5 was not substituted for these documented rules. No endpoint, threshold, or constituent set was reselected on validation.

## 5. Execution Ledger

| Time (UTC) | Job | Outcome | Evidence role |
|---|---|---|---|
| 2026-09-04 01:26 | no job created | member quota rejected the request before execution | platform receipt only; no scientific evidence |
| 2026-09-04 02:34 | `pt-gsrtu3dp` | failed during first activation export because PyTorch bfloat16 tensors cannot be converted directly to NumPy | ineligible debug run; no result table |
| after failure | local regression and fix | added a failing bfloat16-export regression; converted through float32 before NumPy float16 export; 4/4 tests passed | implementation-only repair; scientific contract unchanged |
| 2026-09-04 02:37--02:42 | `pt-3c60qjz3` | `SUCCEEDED`; run `full-20260904T023742Z` | sole eligible full-run evidence |

The successful analysis itself took 164.599 seconds. ACP wall time from start to completion was approximately 4 minutes 8 seconds, including preflight, tests, distributed startup, extraction, analysis, and rendering. The run used one reserved node with four NVIDIA H100 80GB HBM3 GPUs.

## 6. Primary Results

| Graph | Groups | Edges | Nodes | Depth 0 | Depth 1 | Depth 2 | Maximum depth | Components |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Discovery | 1,212 | 2,616 | 1,279 | 67 | 1,201 | 11 | 2 | 1 |
| Replication-qualified | 24 | 91 | 53 | 29 | 23 | 1 | 2 | 1 |

The registered typed verdict is `NONTRIVIAL_REPLICATED`: the discovery graph is acyclic and has maximum depth two, and 24 frozen groups pass all replication gates.

### Replication gate audit

| Gate | Passing groups | Fraction |
|---|---:|---:|
| Minimum one-sided containment | 1,171 / 1,212 | 96.62% |
| Maximum reverse containment | 1,210 / 1,212 | 99.83% |
| Minimum joint gain | 24 / 1,212 | 1.98% |
| All registered gates | 24 / 1,212 | 1.98% |
| Replication composite count at least 100, diagnostic only | 1,118 / 1,212 | 92.24% |

Twenty-two of the 24 qualified groups also had at least 100 replication composite firings; the two smaller groups had 62 and 69. The joint-gain rule, rather than one-sided containment or reverse asymmetry, is the binding replication gate.

### Graph-shape diagnostic

The discovery graph is strongly hub dominated: constituent feature 14,481 receives 1,062 of 2,616 edges (40.60%), followed by feature 3,989 with 493. In the qualified graph the largest constituent hubs are feature 29,342 with 15 edges and features 8,856 and 3,989 with nine each. This is a descriptive warning that frequency and broad reuse remain plausible graph-shape explanations; it is not part of the registered pass/fail rule.

### Only replicated depth-two chain

Feature 27,821 is the sole qualified depth-two node. Its frozen constituent set is `[8856, 29342, 3321, 29506, 6187]`; feature 6,187 is itself a qualified composite of `[8856, 29342]`. On replication:

| Composite | Replication firings | Minimum \(P(U\mid C)\) | Maximum \(P(C\mid U)\) | Joint gain |
|---|---:|---:|---:|---:|
| 27,821 | 1,741 | 0.98449 | 0.28303 | 0.07959 |
| 6,187 | 6,056 | 0.99141 | 0.06222 | 0.07838 |

The graph also contains direct edges from feature 27,821 to constituents already under feature 6,187. Therefore, the graph includes transitive or redundant relations and should not be read as a unique semantic tree.

## 7. Figure Contracts And Visual Audit

### `figures/candidate_hierarchy.png`

- Question: did discovery produce a non-flat acyclic graph?
- Metric and unit: longest-path depth and node/edge counts.
- Data source: frozen discovery edge table.
- Encoding: vertical position is depth; color is structural role; labels are shown only for the small depth-two band.
- Allowed conclusion: the candidate graph is non-flat with maximum depth two and is hub dominated.
- Limitation: density and layout do not show semantics, causality, or independent replication.
- Visual audit: passed; all three depth bands, count annotations, legend, and title are visible.

### `figures/replicated_hierarchy.png`

- Question: what remains after applying every frozen replication gate?
- Metric and unit: longest-path depth and retained node/edge counts.
- Data source: replication-qualified edge table.
- Encoding: the same structural-role and depth layout as the candidate graph.
- Allowed conclusion: a much smaller but non-flat graph survives, with one depth-two node.
- Limitation: retention does not assign semantic labels or establish Router utility.
- Visual audit: passed; retained depth bands, feature labels, legend, and title are visible.

## 8. Evidence Lineage

| Claim | Source artifact | Derivation |
|---|---|---|
| Typed verdict and graph counts | worker `hierarchy_summary.json` | emitted by the frozen analysis and checked against node/edge tables |
| Candidate and qualified relations | `tables/composition_candidates.csv` | discovery selection followed by validation-only evaluation of frozen endpoints |
| Depth and roles | node and edge tables | directed-acyclic longest-path computation |
| Gate bottleneck | `tables/gate_breakdown.csv` | post-run counting of registered per-candidate fields; diagnostic, not a new gate |
| Graph shape | two PNG figures | rendered from the corresponding frozen edge table and visually audited |

Curated artifact SHA-256 values:

- candidate figure: `9ef12a6a48f6f2322e54f004c879c30c99f6c5d5a5d9e9a05038b023aec08ba2`
- qualified figure: `1815473ce207a4653d89c29c2b6cf07036517f303bd1f7742fb62f985dc583d5`
- candidate groups: `d12d5742f767aa0fde49e13234e37be71fd8668dc0b61a5b4079aa57898a1fde`
- discovery edges: `b986dddf4b565f705a2c98bbfd09567d53ff294c379444d6338934c87b5939f8`
- discovery nodes: `f515162a4ec41145dd3f4335182088cddf00da6440c0889a2de76a37ca61fb92`
- qualified edges: `8dab3d7d086ff0b4dfd79acee5adcd88beecb426a8da348cb54693628f2aad70`
- qualified nodes: `c68202dd42b11e225d71d9564c38efd54da2ee28674f5784bcc96133afdb8498`

Raw caches, full logs, and the source `hierarchy_summary.json` remain under `/data/250010109/MoE_Router/experiments/20260904_a15_13_e17_sae_hierarchy/runs/full-20260904T023742Z`.

## 9. Deviations And Eligibility

There was no scientific deviation. The bfloat16-to-NumPy correction changed only serialization compatibility and was protected by a new regression test before the eligible rerun. Candidate selection, data, thresholds, identities, and decision gates stayed frozen. The first executed job is excluded because it produced no analysis result. The successful retry is eligible.

## 10. Conclusion, Boundary, And Next Decision

E17 passes its registered structural gate. It reproduces a nontrivial candidate activation-containment graph, but only 24 of 1,212 discovery groups survive the independent joint-composition requirement and the maximum depth remains two rather than the historical five. The result cannot support semantic hierarchy, coarse/fine teacher labels, causal composition, layer selection, Router behavior, expert utility, or downstream gain.

The sole next decision is whether to approve a new M2D2 semantic-qualification protocol restricted to the 24 replicated groups and 53 nodes, with coarse-label concentration, parent-conditioned fine-label concentration, and frequency/coverage-matched controls. No Router or LoRA execution is implied.
