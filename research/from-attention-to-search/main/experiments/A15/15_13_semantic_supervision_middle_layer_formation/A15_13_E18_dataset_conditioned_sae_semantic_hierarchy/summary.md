# A15_13_E18 Result Summary: Dataset-Conditioned SAE Semantic Hierarchy

```text
Execution status: FULL_RUN_COMPLETE
Registered evidence eligibility: ELIGIBLE
Senior-alignment trend eligibility: POST_HOC_DIAGNOSTIC
Registered typed verdict: COARSE_FINE_GRAPH_CONFIRMED
Knowledge wording: AI_DRAFT_AWAITING_HUMAN_CONFIRMATION
Successful ACP job: pt-4ni5jy2l
Worker run: full-20260904T042013Z
```

## Direct Answer

The balanced M2D2 audit does **not** recover a complete or definite three-parent by three-child hierarchy from the frozen DCLM SAE graph. The registered pairwise test is positive: two of 91 frozen graph edges pass development and independent confirmation permutation bounds. Both edges, however, cover only the `Culture and arts` parent and two of its three children (`Mass media` and `Performing arts`). The post-hoc senior-alignment analysis also does not recover a coarse-to-fine role transition: DCLM graph depth is associated with coarse purity but not significantly with fine purity, while the task-proxy and M2D2 graphs make both coarse and fine roles stronger at greater depth. Thus the registered verdict is `COARSE_FINE_GRAPH_CONFIRMED`, but the evidence supports only partial graph-to-taxonomy correspondence and label specificity, not a usable unified 3-by-3 teacher.

## Primary Result

| Frozen DCLM edge | Development score / family-wise bound | Confirmation score / family-wise bound | M2D2 assignment |
|---|---:|---:|---|
| 23,780 -> 1,804 | 0.02233 / 0.01373 | 0.02077 / 0.00323 | Culture and arts -> Mass media refinement |
| 26,094 -> 18,373 | 0.01714 / 0.01373 | 0.01554 / 0.00323 | Culture and arts -> Performing arts refinement |

The family-wise maximum-test probabilities are 0.001998 on development and 0.000999 on confirmation. Six frozen DCLM nodes pass their registered node-level confirmation tests. Nevertheless, the two edge constituents that supply the broad role have confirmation coarse normalized purities only 0.02096 and 0.03853, both below the node-level family-wise coarse bound 0.20420. The edge result therefore establishes a relative wide-to-narrow contrast, not a strongly identified coarse semantic endpoint.

## Decisive Coverage Boundary

![M2D2 three-by-three confirmed-edge coverage](figures/m2d2_3x3_confirmed_edge_coverage.png)

How to read: the left panel is the registered result and shows that only two of nine taxonomy cells receive a confirmed DCLM edge. The right panel adds a post-hoc stronger guard: neither confirmed semantic edge belongs to one of the four DCLM groups whose original activation relation also survives on M2D2. This guard does not replace the registered verdict, but it blocks the stronger claim that the same DCLM hierarchy was transported intact to M2D2.

## Data-Condition Result

Using the same SAE and relation gates, the graph changes materially with the analysis corpus:

| Analysis corpus | Replicated groups | Edges | Nodes | Maximum depth |
|---|---:|---:|---:|---:|
| DCLM | 24 | 91 | 53 | 2 |
| Local eight-task proxy | 60 | 315 | 113 | 1 |
| M2D2 | 37 | 189 | 75 | 2 |

Only 4/24 DCLM groups retain the unchanged relation gates on M2D2, and only 3/24 retain them on the task proxy. Conversely, only 7/37 M2D2 groups retain on DCLM. These are descriptive cross-corpus stability results, not a causal proof that dataset choice alone creates the hierarchy. The exact senior SFT mixture remains `NOT_RUN_MISSING_DATA`; the local task proxy is not treated as its replication.

![Graph comparison across analysis corpora](figures/dataset_graph_comparison.png)

How to read: graph counts and depth differ even though the model, SAE, and relation gates are fixed. Therefore the activation hierarchy is substantially analysis-data-conditioned.

## Post-Hoc Senior-Alignment Result

The senior-alignment population requires at least 30 active windows in both M2D2 development and confirmation. Development chooses each node's parent and child; confirmation evaluates those frozen assignments. The chance-corrected purity curves report medians, interquartile ranges, node counts, per-node supports, Spearman rank correlation, and 1,000 confirmation-label permutations that preserve every node's support.

| Graph | Eligible nodes by depth | \(\rho(\mathrm{depth},P_c)\) / permutation \(p\) | \(\rho(\mathrm{depth},P_f)\) / permutation \(p\) | Alignment reading |
|---|---|---:|---:|---|
| DCLM | 27 / 5 / 0 | 0.484 / 0.0220 | 0.359 / 0.0649 | coarse association only; no supported depth-two node |
| Task proxy | 49 / 29 | 0.447 / 0.0010 | 0.239 / 0.0380 | deeper nodes are more label-specific |
| M2D2 | 38 / 29 / 5 | 0.511 / 0.0010 | 0.420 / 0.0030 | deeper nodes differ from depth zero, but medians peak at depth one rather than increase monotonically |

For the DCLM graph, coarse-purity medians are 0.00011 at depth zero and 0.23448 at depth one; fine-purity medians are 0 and 0.27541. The depth-one medians are based on only five nodes, while the sole structural depth-two node has zero development support and two confirmation activations and is excluded. Per-node development and confirmation supports are retained in `tables/senior_alignment_node_metrics.csv`.

![Senior-aligned depth-purity curves](figures/senior_aligned_depth_purity.png)

How to read: orange is the observed median with interquartile range, gray is the 95% label-permutation median band, blue points are individual nodes sized by confirmation support, and each depth shows its eligible node count. The DCLM fine trend misses the one-sided 0.05 level, and its depth-two count is zero.

### Role-transition check

The required coarse-to-fine pattern is absent. Coarse-role rank correlation with depth is positive in all three graphs—DCLM 0.490, task proxy 0.477, and M2D2 0.503—rather than negative as required for shallower coarse dominance. Fine-role correlation is also positive. Therefore the task-proxy and M2D2 purity trends mean that deeper nodes are more label-specific; they do not mean that shallow nodes implement coarse routing while deeper nodes implement fine routing.

![Coarse and fine role curves](figures/coarse_fine_role_transition.png)

How to read: the green coarse-role curve and pink fine-role curve generally rise together from depth zero. There is no swap from high shallow coarse role to dominant deep fine role.

### Population edge differences

Only 11 DCLM edges, from four unique composite nodes, have the same development-assigned parent and at least 30 active windows at both endpoints in both splits. Nine of 11 have \(\Delta P_f>0\), all 11 have \(\Delta B>0\), and nine satisfy both. These fractions do not exceed the dependency-preserving label-permutation null: \(p=0.1159\), \(0.9041\), and \(0.1099\). Median \(\Delta P_f=0.26333\) and median \(\Delta B=0.17421\) also do not beat exact-support endpoint re-pairing: \(p=1.0000\) and \(0.7163\). Ordinary edge-wise binomial values are retained as descriptive only because repeated endpoints make edges non-independent.

The M2D2-conditioned graph has 94/96 positive fine-purity differences and a label-permutation \(p=0.0010\), but its median difference is not larger than support-exact random re-pairing (\(p=0.2238\)). This suggests graph-level endpoint stratification rather than evidence that each stored adjacency is a special semantic parent--child relation.

![Population edge differences](figures/edge_population_deltas.png)

How to read: points are eligible edges, the orange line is the observed median, and the gray band is the 95% median range after support-exact endpoint re-pairing. DCLM medians sit inside the random-pair bands.

## Two-Level Conclusion

| Decision level | Result | Consequence |
|---|---|---|
| Senior-alignment conclusion | `PARTIAL_ALIGNMENT_NO_ROLE_TRANSITION` | task-proxy and M2D2 graphs show depth-related label specificity, but DCLM lacks a significant fine trend and no graph shows shallow-coarse to deep-fine role replacement |
| Teacher-qualification conclusion | registered `COARSE_FINE_GRAPH_CONFIRMED`, but only 1/3-parent and 2/9-child coverage | retain two strict edges as diagnostics; do not promote the full DCLM graph as a routing teacher |

## Bounded Interpretation

M2D2 confirms that the SAE contains semantic-selective nodes and a small number of pairwise wide-to-narrow relations. The additional population analysis finds a data-conditioned depth--label-specificity relation, but not the coarse-to-fine responsibility transfer needed by the routing hypothesis. It does not confirm that DCLM training produced the clean 3-by-3 semantic hierarchy required for coarse/fine routing. The correct operational conclusion is to retain the two edge pairs only as diagnostic candidates; the whole DCLM graph must not yet be promoted as the unified teacher for layerwise Router recovery.

## Claim Boundary

The registered result is frozen statistical correspondence on one balanced taxonomy. The depth and population-edge analyses are explicitly post-hoc and their individual permutation values are not family-wise corrected across graph conditions and metrics. Neither evidence layer establishes causal feature composition, universal semantic hierarchy, Transformer-layer onset, online Router recoverability, expert utility, or task-performance gain. The M2D2-adapted graph's 21 strict edges and 96 population-eligible edges are target-conditioned sensitivity results and cannot replace the frozen-DCLM primary condition.

## One Next Decision

Decide whether to obtain the exact senior SFT mixture and reconstruct the hierarchy under that task-conditioned corpus before authorizing any SAE-teacher layerwise recovery audit. Until that decision, the DCLM SAE graph is not approved as a complete coarse/fine teacher.

## Sources

- [Protocol](protocol.md)
- [Detailed evidence record](detailed.md)
- [Raw audit summary](audit_summary.json)
- [Primary edge table](tables/primary_semantic_edges.csv)
- [Cross-corpus retention](tables/cross_dataset_relation_retention.csv)
- [Joint boundary guard](tables/joint_relation_semantic_guard.csv)
- [Post-hoc trend summary](trend_analysis_summary.json)
- [Per-node supports and metrics](tables/senior_alignment_node_metrics.csv)
- [Depth medians and interquartile ranges](tables/senior_alignment_depth_summary.csv)
- [Depth rank correlations](tables/senior_alignment_spearman.csv)
- [Population edge summary](tables/edge_population_summary.csv)
