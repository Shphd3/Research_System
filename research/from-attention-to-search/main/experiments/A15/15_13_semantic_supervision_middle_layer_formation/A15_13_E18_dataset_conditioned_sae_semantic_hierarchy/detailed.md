# A15_13_E18 Detailed Evidence: Dataset-Conditioned SAE Semantic Hierarchy

```text
Execution status: FULL_RUN_COMPLETE
Registered evidence eligibility: ELIGIBLE
Senior-alignment trend eligibility: POST_HOC_DIAGNOSTIC
Registered typed verdict: COARSE_FINE_GRAPH_CONFIRMED
Knowledge wording: AI_DRAFT_AWAITING_HUMAN_CONFIRMATION
```

## 1. Question And Registered Decision

E18 asks whether the 24 DCLM-replicated SAE groups from E17 contain a statistically qualified wide-to-narrow semantic relation on M2D2's balanced three-parent by three-child taxonomy. The frozen DCLM graph owns the primary verdict. Graphs constructed on a local eight-task proxy and on unlabeled M2D2 activations diagnose data conditioning only.

The registered pass requires at least one frozen DCLM edge to pass development assignment, independent confirmation, support, orientation, and the family-wise permutation bound. It does not require full 3-by-3 coverage. Full-taxonomy coverage and simultaneous retention of the original DCLM activation relation are reported as stronger boundary diagnostics.

## 2. What Actually Ran

This experiment had no training stage. Qwen3-0.6B-Base and the completed E16 SAE were frozen throughout; there were zero trainable parameters, zero optimizer updates, no objective, no learning rate, and no checkpoint selection.

| Stage | Trainable / frozen objects | Data pass and update count | Objective / learning rate | Handoff |
|---|---|---|---|---|
| Identity and implementation checks | all objects frozen | 15 tests; 0 updates | not applicable | run only after exact model, SAE, data, graph, and split checks |
| Sparse cache extraction | model and SAE frozen | task proxy train/development/evaluation; M2D2 1,026 balanced train windows plus all 2,304 development and 4,608 confirmation windows; 0 updates | positive Top-32 SAE activations; no learning rate | merge four rank-local caches |
| Data-conditioned graph construction | no model learning | one pass over DCLM tables, task caches, and M2D2 caches | fixed E17 containment gates | freeze graph nodes and edges |
| M2D2 semantic assignment | no model learning | development labels only | assign coarse and parent-local fine labels | freeze assignments before confirmation |
| Independent confirmation and null | no model learning | one confirmation pass and 1,000 joint-label permutations | registered node and edge scores | emit typed verdict and tables |
| Post-hoc boundary guard | no model learning | one replay of unchanged DCLM relation gates on balanced M2D2 development activations | intersection only; no verdict change | restrict claim scope |

The treatment-like primary condition is the frozen DCLM graph evaluated on M2D2. The M2D2- and task-conditioned graphs are sensitivity conditions. The permutation maximum is the null. There is no learned Baseline or Oracle condition and no task-loss evaluation.

## 3. Inputs, Labels, And Identities

- Base model: `/data/250010109/model_cache/Qwen3-0.6B-Base-official`.
- Model config SHA-256: `504a6b58c4271583724e66584b6b7698aea18450209df6b2f7582df0e89cee59`.
- Activation point: zero-based layer 27 MLP input, width 1,024.
- SAE: 30,000 ReLU features with Top-32 activation, checkpoint SHA-256 `e4e2049aced8ba9a3b043bbb2b3308b497b7ec22f107531e37197873ee545b65`.
- M2D2 artifact SHA-256: `8cd04d99ad2576d8a149dc145c83b29d5a977178419304c4490cf8e10cba51a8`.
- Local eight-task proxy SHA-256: `e6320e7aba92c8d9caa36ce43bda5d695843070a54955e63776893334d58a6b6`.
- E17 source run: `full-20260904T023742Z`.
- E18 eligible run: `full-20260904T042013Z`, ACP job `pt-4ni5jy2l`.
- Random seed: 1,704; four H100 processes; M2D2 target positions 64--255.

M2D2 stores a coarse label \(c\in\{0,1,2\}\) and a parent-local child label \(j\in\{0,1,2\}\). Every balancing and identity check uses the single global class \(g=3c+j\). Train, development, and confirmation contain respectively 1,024, 256, and 512 windows in each of the nine joint classes. The M2D2 graph uses 114 windows from each joint train class, for 1,026 total; relation replication uses another balanced 1,026-window selection from development.

The senior script's exact SFT parquet path is absent. Its status is `NOT_RUN_MISSING_DATA`; the local proxy is never named an exact senior-data replication.

## 4. Metrics And Decision Roles

A node is present in a window when it has at least one positive activation in target positions 64--255. Coarse normalized purity subtracts the balanced three-way chance level and rescales perfect precision to one:

\[
S_c=\frac{P(Y_c=\hat c\mid A_f=1)-1/3}{2/3}.
\]

Fine normalized purity uses the same formula after conditioning on the development-assigned parent. Child breadth is one minus total variation distance from a uniform distribution over that parent's three children. The coarse-role score multiplies positive coarse purity by breadth; the fine-role score multiplies positive coarse and fine purities. An edge is nonzero only if both endpoints keep one parent, the proposed composite has greater child purity, and the constituent has greater breadth. Its score is the smaller of the constituent coarse-role score and composite fine-role score.

The 97.5th percentile of the maximum score across 1,000 joint-label permutations is a family-wise bound. It controls selection among all tested nodes or edges under the frozen support pattern. It cannot prove semantic causality or routing utility.

## 5. Execution And Repair Ledger

| Time (UTC) | Job | Outcome | Evidence role |
|---|---|---|---|
| 03:50 | `pt-fakp4xng` | preflight incorrectly expected global fine labels | ineligible; no model forward |
| 03:59 | `pt-8laxsxsx` | stopped before verdict on a zero-development-support node | ineligible; leakage-prevention repair only |
| 04:05 | `pt-n8j170qn` | primary condition completed, but M2D2 graph sampled 342 rather than 1,026 windows | incomplete E18 evidence; secondary graph and cross-corpus M2D2 results excluded |
| 04:20--04:29 | `pt-4ni5jy2l` | `SUCCEEDED`; correct nine-class sampling and all required artifacts | sole complete eligible E18 run |

The final audit computation took 498.092 seconds. The ACP job used one reserved node with four NVIDIA H100 80GB HBM3 GPUs. All 15 tests passed in the job preflight. Engineering repairs unified the label identity \(g=3c+j\), preserved unassigned zero-support nodes without confirmation leakage, excluded nonfinite scores from null maxima, and removed an incorrectly repeated discovery count gate from cross-corpus replication. Model, SAE, graph thresholds, semantic metrics, permutation count, and typed verdict rules were unchanged.

After the registered result was visible, the researcher explicitly authorized Amendment E18-A1 to reproduce the senior-aligned depth--purity and population-edge analyses. This analysis reused the frozen sparse caches, added no model forward pass, trained no parameter, and cannot change the registered E18 verdict. Its 21 tests passed, and recomputed confirmation metrics agree with the frozen E18 node tables to absolute tolerance \(10^{-12}\).

## 6. Primary Frozen-DCLM Result

The registered typed verdict is `COARSE_FINE_GRAPH_CONFIRMED` because two frozen DCLM edges qualify on development and confirmation.

| Edge | Development score | Development family-wise bound | Confirmation score | Confirmation family-wise bound | Parent / child |
|---|---:|---:|---:|---:|---|
| 23,780 -> 1,804 | 0.022333 | 0.013733 | 0.020768 | 0.003234 | Culture and arts / Mass media |
| 26,094 -> 18,373 | 0.017136 | 0.013733 | 0.015543 | 0.003234 | Culture and arts / Performing arts |

The maximum-edge permutation probabilities are 0.001998 on development and 0.000999 on confirmation. Six nodes pass the registered confirmation node tests.

### Endpoint audit

| Endpoint | Structural role | Confirmation support | Coarse normalized purity | Parent-conditioned fine normalized purity | Child breadth |
|---|---|---:|---:|---:|---:|
| 23,780 | proposed composite | 1,337 | 0.26178 | 0.27541 | 0.81640 |
| 1,804 | constituent | 4,293 | 0.02096 | 0.01207 | 0.99061 |
| 26,094 | proposed composite | 271 | 0.08672 | 0.17925 | 0.88050 |
| 18,373 | constituent | 2,660 | 0.03853 | -0.00524 | 0.98255 |

The two constituents are extremely broad across children, but their coarse normalized purities are below the confirmation node-level family-wise bound 0.20420. The registered edge gate therefore validates relative direction within a pair, not a separately strong coarse semantic node. This is why the positive typed verdict must not be expanded into a definite hierarchy claim.

## 7. Three-by-Three Coverage And Stronger Boundary Guard

Both confirmed edges use the `Culture and arts` parent. One is assigned to `Mass media` and one to `Performing arts`. Coverage is therefore one of three parents and two of nine children. There is no confirmed edge for `Visual arts`, any `Health and fitness` child, or any `Natural and physical sciences` child.

Four of the 24 DCLM groups retain all unchanged activation-relation gates on the balanced M2D2 relation sample. Neither of the two semantically confirmed edges belongs to those four retained groups. This intersection was not a registered pass condition and does not retroactively change the typed verdict. It is a post-hoc stronger boundary guard showing that the semantic contrast and transported activation-containment relation do not identify the same edge set.

![M2D2 three-by-three coverage and joint guard](figures/m2d2_3x3_confirmed_edge_coverage.png)

Figure contract:

- Question: does the positive pairwise verdict cover the full balanced taxonomy, and do the same edges retain the original DCLM relation on M2D2?
- Metric and unit: number of confirmed edges per taxonomy cell; number also passing unchanged relation gates.
- Data: frozen DCLM semantic confirmation edge table and balanced M2D2 relation cache.
- Allowed conclusion: only two cells in one parent are covered; joint relation-semantic intersection is zero.
- Limitation: the right panel is post-hoc and can restrict but not replace the registered verdict.
- Visual audit: passed; all nine labels, counts, and the post-hoc designation are visible.

## 8. Data-Condition Diagnostics

| Source graph | Qualified groups | On DCLM | On task proxy | On M2D2 |
|---|---:|---:|---:|---:|
| DCLM | 24 | 24 (100%) | 3 (12.5%) | 4 (16.7%) |
| Task proxy | 60 | 7 (11.7%) | 60 (100%) | 2 (3.3%) |
| M2D2 | 37 | 7 (18.9%) | 4 (10.8%) | 37 (100%) |

The M2D2-conditioned graph has 916 candidate groups, 37 replicated groups, 189 edges, 75 nodes, and maximum depth two. It has 21 M2D2-confirmed semantic edges. Because this graph was constructed from M2D2 activations, it is a target-conditioned sensitivity result and cannot substitute for the primary DCLM transport question. The task-proxy graph has 60 groups, 315 edges, 113 nodes, maximum depth one, and three M2D2-confirmed edges.

![Data-conditioned graph counts and depth](figures/dataset_graph_comparison.png)

Figure contract:

- Question: does the same SAE and relation rule produce the same graph on different analysis corpora?
- Metric and unit: replicated group, edge, node count, and maximum structural depth.
- Data: DCLM E17 graph and E18 task-proxy and M2D2 graphs.
- Allowed conclusion: graph form is materially data conditioned.
- Limitation: count differences do not isolate which corpus property causes the difference.
- Visual audit: passed; counts use a logarithmic axis and all depth bars are legible.

![M2D2 semantic profiles by structural depth](figures/m2d2_depth_semantic_profiles.png)

Figure contract:

- Question: does greater activation-graph depth uniformly imply stronger M2D2 coarse or fine selectivity?
- Metric and unit: confirmation normalized purity under development-frozen assignments.
- Data: all retained nodes for the three graph conditions.
- Allowed conclusion: semantic purity is heterogeneous within every structural level; structural depth alone is not a semantic-granularity label.
- Limitation: points below the minimum support guard remain descriptive, and no causal use is tested.
- Visual audit: passed; graph condition, depth, zero line, and medians are visible.

## 8.1 Post-Hoc Senior-Alignment Depth--Purity Analysis

### Population and confirmation boundary

Development assigns \(\hat c_v\) and \(\hat j_v\) for every node. Confirmation evaluates those frozen identities rather than choosing a new majority label. The primary trend population requires support of at least 30 active windows in both splits. This preserves the earlier teacher support guard and prevents nodes with one or two activations from defining the curve.

| Graph | All nodes by depth | Eligible nodes by depth | Main support limitation |
|---|---|---|---|
| DCLM | 29 / 23 / 1 | 27 / 5 / 0 | the sole depth-two node has development support 0 and confirmation support 2 |
| Task proxy | 53 / 60 | 49 / 29 | 35 low-support nodes excluded |
| M2D2 | 38 / 32 / 5 | 38 / 29 / 5 | three low-support depth-one nodes excluded |

### Per-depth medians and interquartile ranges

| Graph / depth | Nodes | Confirmation support median [Q1, Q3] | \(P_c\) median [Q1, Q3] | \(P_f\) median [Q1, Q3] | Breadth median | Coarse-role median | Fine-role median |
|---|---:|---:|---:|---:|---:|---:|---:|
| DCLM / 0 | 27 | 4,602 [4,040.5, 4,607.5] | 0.00011 [0, 0.03253] | 0 [0, 0.01189] | 0.99957 | 0.00011 | 0 |
| DCLM / 1 | 5 | 445 [271, 1,337] | 0.23448 [0.08672, 0.26178] | 0.27541 [0.17925, 0.38732] | 0.81640 | 0.15962 | 0.07210 |
| DCLM / 2 | 0 | not estimable | not estimable | not estimable | not estimable | not estimable | not estimable |
| Task proxy / 0 | 49 | 4,217 [531, 4,606] | 0.01175 [0, 0.05986] | 0.01171 [0, 0.08333] | 0.99055 | 0.01156 | 0.00000 |
| Task proxy / 1 | 29 | 203 [120, 877] | 0.17500 [0.06757, 0.40826] | 0.21053 [0.00065, 0.62848] | 0.78788 | 0.12648 | 0.02194 |
| M2D2 / 0 | 38 | 4,386.5 [3,034.75, 4,607] | 0.01124 [0, 0.04078] | 0.00233 [0, 0.05054] | 0.99331 | 0.01116 | 0.00002 |
| M2D2 / 1 | 29 | 1,167 [646, 2,115] | 0.17539 [0.10098, 0.31338] | 0.14813 [0.06321, 0.38000] | 0.84675 | 0.12636 | 0.02851 |
| M2D2 / 2 | 5 | 3,035 [2,468, 4,217] | 0.12521 [0.01221, 0.12784] | 0.06087 [0.00375, 0.12875] | 0.93860 | 0.11686 | 0.00762 |

M2D2 depth-one medians exceed depth-two medians for both purity measures. Thus the positive rank correlations distinguish depth zero from later structural levels but do not show a strictly monotonic three-level curve.

### Rank correlation and fixed-support label null

For each of 1,000 permutations, the exact M2D2 confirmation joint labels are shuffled across windows. Graph topology, structural depths, development assignments, activation presence, and every node's support remain fixed. The reported \(p\)-value is one-sided and is not corrected across the three graph conditions and four trend metrics because E18-A1 is post-hoc.

| Graph | \(\rho(P_c)\) / \(p\) | \(\rho(P_f)\) / \(p\) | \(\rho(R_c)\) / shallow-dominance \(p\) | \(\rho(R_f)\) / \(p\) |
|---|---:|---:|---:|---:|
| DCLM | 0.484 / 0.0220 | 0.359 / 0.0649 | 0.490 / 0.9610 | 0.463 / 0.0697 |
| Task proxy | 0.447 / 0.0010 | 0.239 / 0.0380 | 0.477 / 0.9990 | 0.317 / 0.0270 |
| M2D2 | 0.511 / 0.0010 | 0.420 / 0.0030 | 0.503 / 0.9920 | 0.475 / 0.0010 |

\(R_c=P_cB\) is the coarse-role score and \(R_f=P_c\max(0,P_f)\) is the fine-role score. The routing hypothesis predicts coarse role to be relatively stronger at shallow depth, so its test is one-sided toward a negative correlation. Every observed coarse-role correlation is instead positive. The task-proxy and M2D2 graphs therefore exhibit deeper label specificity, not a coarse-role to fine-role handoff. DCLM provides only a coarse-purity depth association; its fine-purity and fine-role trends do not pass 0.05.

![Senior-aligned depth-purity curves](figures/senior_aligned_depth_purity.png)

Figure contract:

- Question: does structural depth predict coarse purity and parent-conditioned fine purity under independent confirmation?
- Metric and unit: normalized purity in \([-0.5,1]\), structural depth, node support count, Spearman rank correlation, and one-sided permutation probability.
- Raw source: frozen M2D2 development/confirmation caches and graph node tables.
- Aggregation: individual eligible nodes, depth median, interquartile range, and 95% permutation band for the depth median.
- Allowed conclusion: DCLM has only a coarse association; task-proxy and M2D2 graphs have depth-related label specificity.
- Limitation: DCLM has no eligible depth-two node; individual post-hoc tests are not multiplicity-adjusted across graphs and metrics.
- Visual audit: passed; node counts, point-support encoding, observed medians, interquartile ranges, null bands, correlations, and probabilities are legible.

![Coarse and fine role transition](figures/coarse_fine_role_transition.png)

Figure contract:

- Question: do shallow nodes carry stronger coarse roles while deeper nodes replace them with stronger fine roles?
- Metric and unit: depth-wise medians and interquartile ranges of \(R_c\) and \(R_f\).
- Raw source: `tables/senior_alignment_node_metrics.csv`.
- Allowed conclusion: coarse and fine roles rise together from depth zero; no role replacement is observed.
- Limitation: this is representational association, not routing or expert-use evidence.
- Visual audit: passed; both role curves and all available structural depths are visible.

## 8.2 Post-Hoc Population Edge Analysis

An edge enters the population analysis only when both endpoints have at least 30 active windows in development and confirmation and share the development-assigned parent. Confirmation computes \(\Delta P_f=P_f(q)-P_f(u)\) and \(\Delta B=B(u)-B(q)\). Label permutation preserves the graph and dependencies among repeated endpoints. The random-edge comparison independently permutes constituent endpoints within the same parent and ordered depth pair, preserving the exact multisets of composite and constituent support counts.

| Graph | Eligible edges / unique composites | \(\Delta P_f>0\) | \(\Delta B>0\) | Both positive | Median \(\Delta P_f\) / random-pair \(p\) | Median \(\Delta B\) / random-pair \(p\) |
|---|---:|---:|---:|---:|---:|---:|
| DCLM | 11 / 4 | 9/11; label-null \(p=0.1159\) | 11/11; \(p=0.9041\) | 9/11; \(p=0.1099\) | 0.26333 / 1.0000 | 0.17421 / 0.7163 |
| Task proxy | 54 / 16 | 33/54; \(p=0.2038\) | 51/54; \(p=0.8382\) | 33/54; \(p=0.1618\) | 0.02834 / 0.1708 | 0.13290 / 0.6014 |
| M2D2 | 96 / 22 | 94/96; \(p=0.0010\) | 96/96; \(p=0.1489\) | 94/96; \(p=0.0010\) | 0.14592 / 0.2238 | 0.11833 / 0.2687 |

Ordinary exact-binomial probabilities against 50% are present in the source table only as descriptive values. They treat repeated edges as independent and are not used for inference. For DCLM, the 11 edges reduce to four unique composite nodes; only three of four composite-level median contrasts are jointly positive. No DCLM population statistic passes its dependency-preserving label null or support-exact random-pair null.

The M2D2 graph has a strong label-permutation fine-direction result, but its median is not larger than support-exact random re-pairing. This separates a depth/endpoint selection effect from adjacency-specific semantic composition.

![Population edge differences](figures/edge_population_deltas.png)

Figure contract:

- Question: does the graph systematically point from broader constituents toward finer composites?
- Metric and unit: per-edge \(\Delta P_f\) and \(\Delta B\), positive-edge fraction, and median difference.
- Raw source: frozen edge tables and confirmation node profiles.
- Aggregation and nulls: eligible edges; graph-preserving label permutations for positive fractions; support-exact endpoint re-pairing for medians.
- Allowed conclusion: DCLM shows descriptive orientation but no null-separated population effect; M2D2 shows target-conditioned fine direction without adjacency-specific median evidence.
- Limitation: edges share endpoints, and all analyses are post-hoc.
- Visual audit: passed; zero line, individual edges, medians, support-matched random bands, sample sizes, fractions, and probabilities are visible.

## 9. Evidence Lineage And Checksums

| Claim | Canonical evidence |
|---|---|
| Job completion, identities, typed verdict, thresholds | `audit_summary.json` |
| Two primary edges | `tables/primary_semantic_edges.csv` and frozen development/confirmation edge tables |
| Endpoint supports and purities | development and confirmation node tables |
| Cross-corpus relation retention | `tables/cross_dataset_relation_retention.csv` |
| Full-taxonomy and joint guard | `tables/joint_relation_semantic_guard.csv` and `tables/dclm_m2d2_joint_relation_semantic_guard.csv` |
| Graph counts | `tables/graph_summary.csv` |
| Per-node depth, support, purity, breadth, and roles | `tables/senior_alignment_node_metrics.csv` |
| Depth medians, interquartile ranges, and counts | `tables/senior_alignment_depth_summary.csv` |
| Rank correlations and fixed-support permutation null | `tables/senior_alignment_spearman.csv` and `tables/senior_alignment_depth_null.csv` |
| Population edge differences and nulls | `tables/edge_population_deltas.csv`, `tables/edge_population_summary.csv`, and `tables/edge_random_pair_null_summary.csv` |

Selected SHA-256 values:

- audit summary: `bb529f6e7512a4dd8fb4b19b18c93aa83e0e69cbb2e0acc3e5822ff38cba40ff`
- coverage figure: `c843a5064a8f4d66b208f973d8069ccbb3b69feb98a9b6d4fd19b2fa69f18816`
- graph-comparison figure: `89dcd6924329694246780c8db841a29057063741a5e084c7789b19f1973b62a0`
- semantic-graph figure: `db9ce2dbfa9995cd830d030117d2ace05778704bb10b3c30b1d9ce8984a59881`
- depth-profile figure: `113f493e6fb2f191ed9df17e9620517dcdf2c3cf210249adc674ecd32de3176d`
- primary edge table: `0b89fd760b279b26bafc0b64c4d58eb44856c6bf68a9f27e57be11408627d2c6`
- cross-corpus retention table: `1cf5babf597dbc453c91aee905b122b38b4d9ff2b8c79aa99aad24e1953f9929`
- trend summary: `9650e1f1f8ca245fb18ea07d2e0679422bb4009932e5bc26d2c4aff1f5bd8164`
- depth-purity figure: `eec93d5a88e34902dcc857cad2d62cfd8eb5c782378ccf0890e43605f0a8f739`
- role-transition figure: `abf2ba460bbc5100d6358be6ae31b558689d744f588a66edf10b7299781bc218`
- population-edge figure: `6db2b725fc098f50750d4733c8864c32481bf60a67a16b24460dc35ff1fa36e9`
- node metric table: `f6beedca3ef284d640e6beb0b62753f60436cd40b0d272b194c6b20822657678`
- depth summary table: `f47dbf12f5298e1a93244d97d0c32b230c852e7162fd273f3f7cacebda234eec`
- rank-correlation table: `c8cb3f675969491d0e918bc99cc25a984db2ef3072ee6b05a0c9af4e8f689aca`
- population-edge summary table: `c89d30dcc7b2e16c845db9d382d5dc71adbdbdee252fb8c5459a3fb2702309a7`

Raw sparse caches, rank shards, and logs remain under `/data/250010109/MoE_Router/experiments/20260904_a15_13_e18_dataset_conditioned_sae_semantics/runs/full-20260904T042013Z`.

## 10. Conclusion, Boundary, And One Next Decision

The registered pairwise gate passes, but M2D2 does not reveal a definite full 3-by-3 hierarchy in the DCLM SAE graph. The post-hoc senior-alignment verdict is `PARTIAL_ALIGNMENT_NO_ROLE_TRANSITION`: the DCLM graph has a coarse-purity association only, while the task-proxy and M2D2 graphs show joint coarse/fine label specificity rather than shallow-coarse to deep-fine role replacement. The DCLM population-edge contrasts also do not separate from dependency-preserving label or support-exact random-pair nulls. The valid teacher claim remains limited to two strict relative wide-to-narrow correspondences in one coarse parent. Structural depth is not itself semantic granularity, exact senior-SFT replication is missing, and the whole DCLM graph is not qualified as a unified routing teacher.

The sole next decision is whether to obtain the exact senior SFT mixture and reconstruct the hierarchy under that task-conditioned corpus before any SAE-teacher layerwise recovery audit is authorized.
