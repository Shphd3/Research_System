# Protocol: A15_13_E18 Dataset-Conditioned SAE Semantic Hierarchy

## 0. Approval Snapshot

```text
Document status: APPROVED_FOR_FULL_RUN
Approval status: researcher explicitly requested ordered execution and a decisive M2D2 3-by-3 correspondence test
Block audit status: A-G CONFIRMED
Cross-block consistency: PASS
Execution scope approved: implementation, tests, one frozen full audit, rendering, and evidence records
Design frozen at: 2026-09-04 UTC
Primary Anchor: 15_13_09_dataset_conditioned_sae_semantic_hierarchy_anchor.md
Primary condition: E17 DCLM-replicated graph evaluated on M2D2 development and confirmation
Secondary conditions: local eight-task proxy graph, unlabeled M2D2-adapted graph, and frozen cross-dataset edge retention
Cannot claim: exact senior SFT replication, causal composition, Transformer-layer placement, Router/expert utility, or task gain
```

## 1. Terminology And Definitions

- “稀疏自编码器” (SAE) is the frozen E16 dictionary that retains the 32 largest positive feature activations per token.
- “归一化纯度” is majority-label precision corrected for the balanced random baseline: \((p-1/K)/(1-1/K)\).
- “父类条件细纯度” computes that quantity among windows belonging to one fixed coarse parent; it is not flat nine-way purity.
- “数据条件” is the corpus on which sparse co-activation relations are discovered and replicated.
- “任务混合代理” is the locally reconstructible eight-task mixture. It is not the missing senior SFT parquet.
- “确认” means that labels assigned on development are frozen and tested once on the independent confirmation split.

## 2. Anchor Alignment

The experiment adjudicates only whether E17's frozen DCLM graph maps to the known M2D2 coarse--fine taxonomy and whether differing analysis corpora explain graph differences. It does not search Transformer layers or train any model.

## 3. Tested Hypothesis

At least one DCLM-replicated stored composite-to-constituent edge will map to a M2D2 semantic refinement: the constituent selects one coarse parent while covering all three children, the composite selects the same parent and is more concentrated on one child, and this relation reproduces above a 97.5% family-wise matched-null bound on confirmation. The rival is no connected refinement beyond frequency- and coverage-matched chance.

## 4. Rival Explanations

- The E17 graph reflects DCLM frequency and local co-occurrence rather than semantic granularity.
- The senior's different graph reflects SFT task-mixture data rather than a different SAE mechanism.
- A high-purity node reflects one topical word but has no graph-consistent parent--child role.
- Selecting the best node and reporting its same-split purity creates label leakage and multiple-comparison inflation.

## 5. Data Construction And Provenance

1. DCLM uses the completed E17 discovery and replication caches and its 24 already qualified groups; no E17 relation is reselected.
2. The local eight-task proxy is `/data/250010109/datasets/a15_e14_benchmark/processed.pt`: MMLU, MMLU-Pro, BBH, GSM8K, MATH, GPQA, HumanEval, and MBPP, balanced by row. Its train rows are deterministically split within task into relation discovery and replication halves; development and evaluation assign and confirm eight-task selectivity.
3. M2D2 is `/data/250010109/datasets/m2d2_wikipedia_3x3/processed/m2d2_3x3_seq256.pt`. It has 9,216 train, 2,304 development, and 4,608 confirmation windows, balanced across three parents and three children per parent. A seed-1704 balanced 1,026-window train sample discovers target-adapted relations; a disjoint balanced 1,026-window development sample replicates them. All development and confirmation windows serve semantic assignment and confirmation.
4. M2D2 graph construction never reads labels. Labels are opened only after every graph and relation threshold is frozen. Exact duplicate windows across the three splits are zero per the data manifest.
5. The senior script's named SFT parquet is searched and identity-recorded. If absent, the exact-SFT condition is `NOT_RUN_MISSING_DATA`; no proxy result may be labeled exact reproduction.

## 6. Learning Task And Permitted Supervision

There is no learning and no optimizer. The frozen model and SAE produce activations. DCLM, proxy, and M2D2 train/development activations may define or replicate graph edges without labels. M2D2 development labels may assign node roles and class identities. Confirmation labels may only evaluate those frozen assignments.

## 7. Model, State, And Frozen Objects

- Frozen base: `/data/250010109/model_cache/Qwen3-0.6B-Base-official`.
- Frozen state: zero-based layer 27 MLP forward input, width 1,024.
- Frozen SAE: E16 checkpoint SHA-256 `e4e2049aced8ba9a3b043bbb2b3308b497b7ec22f107531e37197873ee545b65`.
- Dictionary: 30,000 ReLU features with Top-32 retention.
- E17 relation thresholds and 4,096-feature constituent pool are unchanged.
- M2D2 uses target positions 64--255. Proxy text uses every non-padding position.

## 8. Optimization

Not applicable. All parameters are frozen, the optimizer-update count is zero, and no checkpoint is selected.

## 9. Conditions And Seeds

- Sampling and permutation seed: 1704.
- Permutations: 1,000 independent joint coarse--fine label permutations per semantic split.
- Minimum node support: 30 active windows in both development and confirmation.
- DCLM primary graph: 24 replicated groups, 91 stored edges, 53 nodes.
- Proxy and M2D2 graph thresholds: identical to E17, including minimum composite count 100, discovery containment 0.98, reverse containment below 0.98, frequency ratio 1.5, group containment 0.90, replication containment 0.90, replication reverse at most 0.60, and joint gain at least 0.02.

## 10. Primary Metric And Frozen Analysis

For each feature, window-level presence is one when it has any positive target-token activation. Development assigns one coarse parent and one child within that parent. The coarse-role score multiplies normalized coarse purity by child breadth; the fine-role score multiplies normalized coarse purity by parent-conditioned normalized fine purity.

For stored edge composite \(q\) to constituent \(u\), the semantic-refinement score is the smaller of the constituent coarse-role score and composite fine-role score, and is zero unless both choose the same parent, the composite has higher fine purity, and the constituent has broader child coverage. The development family-wise threshold is the 97.5th percentile of the maximum edge score under each joint-label permutation. Only development-qualified edges proceed. Confirmation uses frozen class assignments and requires the same orientation, minimum support, and score above its independently permuted family-wise 97.5th percentile.

The primary typed verdict is:

- `COARSE_FINE_GRAPH_CONFIRMED`: at least one E17 DCLM edge qualifies on both development and confirmation.
- `SEMANTIC_SELECTIVITY_WITHOUT_GRAPH_HIERARCHY`: no edge qualifies, but at least one frozen graph node has a confirmation coarse- or fine-role score above its family-wise matched-null bound.
- `NO_SEMANTIC_ALIGNMENT`: neither connected edges nor nodes qualify.
- `INSUFFICIENT`: identity, split, leakage, support, cache, or artifact guards fail.

## 11. Secondary Metrics And Guards

- Report graph groups, edges, nodes, maximum depth, and node counts by depth for DCLM, the task proxy, and M2D2-adapted conditions.
- Report the fraction of each source graph's replicated groups that pass unchanged relation gates on each other corpus.
- Report node support, assigned labels, normalized coarse purity, parent-conditioned normalized fine purity, child breadth, role scores, and depth.
- Report development and confirmation family-wise null thresholds and empirical maximum-statistic \(p\)-values.
- Report depth-wise distributions descriptively; they cannot override the connected-edge primary verdict.
- Assert that no label tensor is passed to graph discovery, and that development assignments are unchanged during confirmation.

## 12. Known Good, Bad, And Confusing Cases

- Known good: a broad parent node active equally across three children plus a connected child-specific composite must produce a positive refinement score.
- Known bad: two pure nodes selecting different parents, or a constituent narrower than its composite, must score zero.
- Known confusing: a highly frequent node may have stable coverage but chance purity; fixed-support label permutation must retain that frequency while removing semantics.

## 13. Ordered Stage Contract

| Stage | Question | Operation | Decision role |
| --- | --- | --- | --- |
| 1 | Is the senior data condition recoverable? | Resolve exact SFT path and hashes; otherwise record missing identity | bounds the senior comparison |
| 2 | Does graph form change by data? | Reuse DCLM and construct proxy then M2D2 graphs with identical rules | secondary data-condition diagnosis |
| 3 | Do frozen relations transfer? | Apply each replicated relation set without reselection to other corpora | secondary stability diagnosis |
| 4 | Does E17 map to M2D2 3-by-3 semantics? | development role assignment, then confirmation with matched null | primary verdict |
| 5 | Could target-adapted construction recover a hierarchy? | run the same semantic test on proxy- and M2D2-derived graphs | sensitivity only |
| 6 | Is the result auditable? | render graphs, depth profiles, null thresholds, and complete artifact audit | completion gate |

## 14. Output And Provenance Contract

Worker root: `/data/250010109/MoE_Router/experiments/20260904_a15_13_e18_dataset_conditioned_sae_semantics`.

Required outputs include dataset identity receipts; rank-local and merged sparse caches; graph candidate, node, and edge tables for the proxy and M2D2; cross-dataset relation retention; M2D2 development and confirmation node/pair tables; permutation thresholds; a typed `audit_summary.json`; one graph-comparison figure; one M2D2 semantic hierarchy figure; one depth-wise semantic-profile figure; and full logs. Raw caches remain on the worker surface.

Execution uses one reserved four-H100 ACP node with profile `n6ls.iu.i40.4`, one node, four processes, and no training. No automatic retry changes scientific settings.

## 15. Success, Failure, And Insufficient Evidence

Scientific success and negative outcomes are exactly the four typed verdicts in Section 10. A completed negative result is not an engineering failure. Missing exact senior data makes only the exact-SFT comparison insufficient unless another required guard also fails.

## 16. Claim Boundary

An eligible edge is evidence of statistical correspondence between a frozen SAE activation graph and one balanced M2D2 taxonomy. It is not evidence that the SAE graph is universally semantic, that activations are causally compositional, that coarse and fine responsibilities begin at different Transformer layers, or that routing and experts will improve language modeling.

## 17. Block Confirmation And Freeze Ledger

| Block | State | Basis |
| --- | --- | --- |
| A | CONFIRMED | user retained the existing SAE-teacher workstream and requested ordered completion |
| B | CONFIRMED | user named clean M2D2 three-by-three correspondence as the decisive target |
| C | CONFIRMED | frozen graph, development assignment, independent confirmation, and matched null |
| D | CONFIRMED | E16/E17 model, SAE, state, and graph identities |
| E | CONFIRMED | no learning or optimization |
| F | CONFIRMED | typed outcomes separate connected hierarchy from isolated selectivity |
| G | CONFIRMED | inherited and explicitly retained `H100-4-reserved` execution profile |

Cross-block consistency: `PASS`. The exact senior SFT file is an identity guard, not a license to relabel the local proxy. Any post-start scientific amendment requires an append-only record.

Execution receipt, 2026-09-04 03:50 UTC: ACP accepted the frozen full audit as job `pt-fakp4xng` on one reserved four-H100 node. The run stamp is `20260904T035000Z`. At submission, Python compilation, shell syntax, the submission dry-run, and all eight semantic-core tests passed. This receipt is not a result.

Engineering failure receipt, 2026-09-04 03:50 UTC: job `pt-fakp4xng` failed in preflight before model forward or graph construction. The preflight incorrectly asserted that the stored `fine` tensor used global labels zero through eight; the frozen M2D2 artifact correctly stores parent-local child labels zero through two alongside a separate coarse tensor. A regression test now fixes the mapping \(3c+j\) used only for human-readable names, and preflight now verifies three balanced local child IDs. Nine tests and the exact identity snippet pass. No data, model, graph threshold, metric, null, or verdict rule changed; the failed job is ineligible evidence.

Engineering failure receipt, 2026-09-04 03:59 UTC: repaired job `pt-8laxsxsx` completed all frozen forward caches and both secondary graph constructions, then stopped before producing a semantic verdict. One DCLM graph node had zero M2D2 development support, so its deliberately unassigned label `-1` reached confirmation profiling. The implementation now preserves such a node as unassigned rather than relabeling it on confirmation, excludes nonfinite unassigned scores from family-wise maxima, and handles a fixed parent with zero confirmation hits without empty-mean warnings. Two regression cases, the full 12-test suite, and a real-cache DCLM-to-M2D2 integration audit pass. This is a leakage-prevention repair; all scientific settings remain frozen, and `pt-8laxsxsx` is ineligible evidence.

Evidence-ineligibility receipt, 2026-09-04 04:14 UTC: job `pt-n8j170qn` completed the frozen DCLM semantic condition, but its secondary M2D2 graph sampled 342 rather than 1,026 windows because the parent-local child tensor `0/1/2` was incorrectly used as the balancing label. The canonical sampling identity is now centralized as \(g=3c+j\). Exact preflight shows 1,026 selected windows and 114 from each of the nine joint classes; all 15 tests pass. The DCLM primary subset remains readable, but `pt-n8j170qn` is not the complete E18 evidence because its M2D2 graph and M2D2 cross-corpus retention are invalid.

Final rerun receipt, 2026-09-04 04:20 UTC: ACP accepted job `pt-4ni5jy2l` on one reserved four-H100 node with run stamp `20260904T042013Z`. Model, SAE, graph gates, semantic metrics, null, and verdict rules are unchanged. This receipt is not a result.

Eligible execution receipt, 2026-09-04 04:29 UTC: job `pt-4ni5jy2l` reached `SUCCEEDED`; all 15 preflight tests, the exact nine-class balance check, and every required artifact passed. The eligible run is `full-20260904T042013Z`. It processed exactly 1,026 M2D2 graph-construction windows, 114 from each joint class. The registered typed verdict is `COARSE_FINE_GRAPH_CONFIRMED` from two development-and-confirmation-qualified DCLM edges. Full-taxonomy coverage and the post-hoc joint relation-semantic guard are reported only as claim-boundary diagnostics in `summary.md` and `detailed.md`; they do not alter the frozen typed-verdict rule.

### Amendment E18-A1: post-hoc senior-alignment trend diagnostic

Time and approval: on 2026-09-04, after E18 results were visible, the researcher explicitly requested this bounded analysis and authorized its execution on the frozen caches.

Before: depth-wise purity distributions were descriptive secondary outputs, while individual family-wise-qualified edges owned the registered teacher verdict.

After: the original verdict remains unchanged, and a second explicitly post-hoc conclusion is added for alignment with the senior's analysis object. For every DCLM-, task-proxy-, and M2D2-graph node, development selects the coarse parent and local child, while confirmation reports the frozen-assignment coarse normalized purity, parent-conditioned fine normalized purity, child breadth, coarse-role score, fine-role score, activation-window support, structural depth, per-depth median, interquartile range, and node count. The primary trend population requires at least 30 active windows in both development and confirmation; excluded and low-support counts remain visible. Spearman rank correlation between structural depth and each confirmation purity is compared one-sided against 1,000 confirmation joint-label permutations. Each permutation preserves all nine label counts, every node's activation support, graph topology, structural depth, and development-frozen assignments.

For every stored structural edge \(q\to u\), the population analysis includes the edge only when both endpoints have at least 30 active windows in both splits and share the development-assigned coarse parent. It reports \(\Delta P_f=P_f(q)-P_f(u)\), \(\Delta B=B(u)-B(q)\), the proportions with each difference positive, and the joint-positive proportion. One-sided confirmation-label permutation tests evaluate whether each positive-edge proportion exceeds its matched null; ordinary 50% exact-binomial values are reported only as descriptive because edges share endpoints. Median differences are compared with 1,000 random endpoint re-pairings within the same assigned parent and ordered depth pair; re-pairing preserves the exact multisets of composite and constituent supports. Results are also aggregated by unique composite to expose edge dependence.

Eligibility impact: `POST_HOC_DIAGNOSTIC`. This amendment cannot change, rescue, or invalidate the registered E18 typed verdict. It may establish or reject only a graph-level depth--purity trend under the frozen M2D2 evaluation. Even a monotonic fine-purity curve cannot by itself establish a coarse-to-fine role transition, Router usability, Transformer-layer placement, expert utility, or task gain.

Post-hoc completion receipt, 2026-09-04: E18-A1 completed locally from the frozen eligible-run caches without a model forward pass or parameter update. All 21 tests passed. The analysis used 1,000 support-preserving confirmation-label permutations and 1,000 support-exact within-parent, ordered-depth endpoint re-pairings. Its typed diagnostic result is `PARTIAL_ALIGNMENT_NO_ROLE_TRANSITION`; canonical tables, figures, source hashes, and the claim boundary are recorded in `summary.md` and `detailed.md`. This receipt does not alter the registered E18 verdict.
