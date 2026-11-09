# E17 Follow-up: Activation Hierarchy Parameter and Static Audit

## 0. Approval and scope snapshot

Status: APPROVED_FOR_LOCAL_EXPLORATORY_STATIC_ANALYSIS.
Researcher authorization: 2026-09-09, explicitly requested starting the experiment,
with emphasis on static analysis after discovering hierarchy relations.
This supersedes the preceding implementation-only scope, not the old E17 contract.
Registered before new graph mining; no new results were inspected when selecting
the six conditions below. Numerical settings come from the previously presented
implementation plan, section 9. Deferred and weak-containment presets are excluded.

Purpose: determine whether candidate-pool/selection/support rules explain shallow
activation graphs, and describe the support, coverage, connections, and replication
of the resulting higher-depth nodes. This is a bounded robustness/root-cause audit
of existing activation artifacts, not a new semantic or functional experiment.

Primary design source: [candidate-hierarchy Anchor](../../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_13_semantic_supervision_middle_layer_formation/subanchors/15_13_08_dclm_sae_candidate_hierarchy_anchor.md),
sections 3--6: acyclic non-flat containment structure and frozen-relation replication.
The separately active [functional-routing Focus](../../../../../focus/focus_sae_flat_router_functional_training.md)
is not modified or treated as approval for this static audit's scientific verdict.
No new Focus/Anchor transition, model training, GPU allocation, or external evaluation.

## 1. Question, rivals, and boundaries

Primary quantities are maximum longest-path depth and number of frozen composite
groups passing replication, separately before/after a replication support gate.
Rivals: high-frequency candidate restriction, greedy selection skipping intermediate
nodes, rare-node exclusion, and discovery-only relations rejected on replication.
All are descriptive parameter contrasts; no deepest-graph winner selection or
confirmation p-values. Six displayed levels are not a success threshold.

This audit cannot establish semantic hierarchy, independent-record uncertainty,
textual interpretation, causal composition, routing usefulness, or expert utility.
It does not execute the plan's two clustering stages or invent semantic labels.

## 2. Data and artifact qualification

Reuse exactly the existing E17 arrays from
`/data/250010109/MoE_Router/experiments/20260904_a15_13_e17_sae_hierarchy/runs/full-20260904T023742Z/activation_cache/`:
discovery has 261632 token rows; replication has 261634; each has 32 positive
feature slots in the same 30000-feature dictionary. All four indices/values files
must match the previously saved structural-audit SHA-256 values. Use no labels,
language-model inference, or new feature fitting. Cache files are read-only.

The old canonical E17 ledger identifies Qwen3-0.6B-Base layer-27 MLP input and SAE
SHA-256 `e4e2049aced8ba9a3b043bbb2b3308b497b7ec22f107531e37197873ee545b65`.
The current SAE and model hashes are recorded as supporting provenance, not a
retroactive proof of an unrecorded historical full-backbone hash. Baseline graph
must exactly reproduce the saved 20260904 depth-exploration endpoints/counts.

Eligibility is conditional on these fixed historical cache artifacts. They were
already used in prior exploration; replication here is not a newly untouched
confirmation set. Filtered token-to-original-record mapping is unavailable, so no
record bootstrap, text examples, corpus-independence claim beyond the historical
ledger, or fabricated mapping. Source overlap with semantic datasets is not used
as a premise because semantic evaluation is outside this execution scope.

## 3. Frozen algorithm and conditions

For rarer composite C and constituent B, let a=P(B|C), b=P(C|B), r=count(B)/count(C).
Edges point C -> B. Baseline: top-16000 observed constituent pool; count(C)>=50;
a>=0.90; b<0.70; r>=1.2; 2--6 constituents; joint containment>=0.85.
Historical sorting is descending (a,r,feature ID). Greedily add a constituent only
if the entire selected set retains joint containment. Freeze selected sets before
reading replication statistics. Near-frequency sorting is ascending r, then
descending a, then ascending feature ID.

| Condition | Change from baseline | Diagnostic purpose |
|---|---|---|
| historical_depth_reference | none | exact historical endpoint parity |
| all_observed_candidates | candidate cap 30000 | exclusion by high-frequency pool |
| lower_discovery_support | count(C)>=30 | rare-node exclusion |
| closer_frequency | r>=1.1 | algebraic negative control; a/b already requires r>1.2857 |
| prefer_near_frequency | near-frequency sorting | intermediate-node skipping |
| reverse_085_discovery_diagnostic | discovery b<0.85 | reverse-gate exclusion, same replication requirement |

Replication, identical across conditions: minimum constituent-given-composite
>=0.90; maximum composite-given-constituent<=0.70; joint prediction gain>=0.02.
Joint prediction gain is P(C|all selected constituents)-max_B P(C|B).
An additional qualified graph requires count_replication(C)>=30. The old-rule
replicated graph remains separately reported, so added support qualification cannot
silently change the historical reference.

No parameter learning, optimizer, fit seeds, or model checkpoint selection.
Cooccurrence counts may be precomputed sparsely once for all conditions, with
synthetic equality against direct multiplication. No 30000x30000 dense allocation.
Cycle detection is fatal; do not delete edges to repair a graph.

## 4. Static analysis and interpretation rules

For each condition, independently rebuild discovery, replicated, and support-
qualified graphs. Compute depth from leaves (0) as one plus maximum child depth.
Report nodes/edges/groups, occupied levels, depth histogram, components, multi-parent
structure, largest constituent hub, and edges that bypass one or more depth levels.

Per-depth activation analysis: token coverage and node support min/median/max in
both sources. Export per-node supports and per-edge joint counts and conditional
probabilities. At each depth pair, report co-coverage conditional probabilities;
these are activation-set statistics, not a probability of causal transmission.

For each node at the maximum qualified depth, save one deterministic longest path
(smallest feature ID on ties) plus the complete descendant edge set. Retain group
joint-gain/support flags beside path metrics. Compare qualified endpoints against
baseline with intersection/union and additions/removals; report gate attrition and
raw replication rates. No automatic new scan is triggered by shallow results.

Typed descriptive readings:
- NONTRIVIAL_REPLICATED: discovery depth>=2 and at least one old-rule replicated group.
- FLAT_OR_EMPTY: valid discovery maximum depth<2 (empty maximum depth is null).
- UNSTABLE_REPLICATION: non-flat discovery but zero replicated groups.
- INSUFFICIENT: failed input/parity/counting/cycle/completeness/resource gate.
Depth gain under a parameter is descriptive only, and must be accompanied by
qualified-node support/coverage and retention; no strong mechanism verdict is
automatically inferred. Human Focus-level interpretation remains pending.

## 5. Procedure, resources, and artifacts

1. Recheck cache hashes and shapes; capture code/config identities. Run synthetic
   checks and a bounded real-cache timing smoke with exactly the same algorithm.
2. Freeze source/config/protocol snapshot into a new run directory. Mine the six
   full-cache conditions, with per-condition progress/receipts and no old overwrite.
3. Verify baseline endpoint parity and the frequency-ratio negative control.
   Compute all static tables and figures from completed condition outputs only.
4. Write Summary/Detailed with exact provenance, limitations, and AI-labeled
   interpretation. Do not update Anchor/Focus or silently launch clustering.

Current local container only: one sequential worker, BLAS/OMP threads=1, no GPU,
90-minute full-mining wall ceiling, 32 GiB address-space safety ceiling, 2 GiB new
artifact limit. Exceeding a ceiling stops with retained partial evidence and a
specific resource diagnosis; it does not reduce rows or drop conditions.
The small timing smoke is implementation evidence, not a six-condition result.

Worker root:
`/data/250010109/MoE_Router/experiments/20260909_sae_hierarchy_offline_analysis/`.
Required outputs in a new `runs/static-<UTC>/`: source/protocol/config snapshots,
input manifest, per-condition results and receipts, graph/node/edge/depth tables,
longest paths and descendant-edge tables, comparison tables, figures, and final
run receipt with elapsed time and peak memory. Raw outputs stay on the worker;
only curated figures/tables are placed beside these research records.

## 6. Approval and freeze ledger

- A (question/boundary): inherited containment-graph question, latest user static-analysis scope.
- B (data): verified fixed historical artifacts; cache-conditional qualification and missing original-record mapping explicit.
- C--E (task/architecture/objective): no learning or new inference; frozen activations only.
- F (comparisons): six non-deferred diagnostic settings from the presented plan, unchanged replication rules; no semantic claims.
- G (execution): current explicit execution request, bounded local CPU use, no external cost.
Cross-block consistency: PASS for this cache-conditional descriptive audit only.
Full semantic/two-stage clustering qualification remains NOT APPROVED BY THIS CONTRACT.
After execution starts, keep the scientific body fixed; additions are receipts,
result links, or explicit amendments with before/after and eligibility impact.

## Amendment A1 -- task-composition clustering, 2026-09-09 before clustering

Authorization: researcher explicitly answered "continue both clustering stages,
first analyze task composition." This adds the two static stages from the named
implementation plan. The six-condition token mining above is unchanged and was
already running; baseline/all-candidate/support diagnostics were visible. No
clustering assignments or task-composition outcomes were inspected before this
extension. Numerical defaults are the presented plan, not selected from outcomes.

Before: graph discovery/static statistics only. After: additionally compare node
selection and true versus shuffled anchor-leaf organization using task-source
labels. This is not semantic qualification, Router training, or expert evaluation.

### Fixed graph roles and data

- Primary: support-qualified historical-depth-reference graph from this run.
- Parameter sensitivity: support-qualified near-frequency graph from this run.
- Support sensitivity: previously saved 20260904 robust graph. Do not pick a graph
  by purity, coverage, depth, or any task-composition result.
- Reuse existing discovery and development segment-incidence caches from
  `20260907_sae_flat_router_candidate/runs/full-20260907T164318Z/cache/`.
  Authenticate cache matrix and record hashes, data SHA, SAE/model/site identities,
  and segment-to-record ownership/lengths against the original padded records.
- Use 19784 discovery records for fitting and all 8480 development records split
  into explanation/check halves by deterministic content-cluster hashing with salt
  `sae-offline-v1`, source stratification, and no outcome-based exclusion.
- Content identity uses the authenticated original data's whitespace-normalized
  full prompt-plus-answer SHA plus exact unpadded input-token SHA. Duplicate
  connected clusters never cross discovery/explanation/check; if cross-partition
  clusters exist, assign the entire cluster to discovery and regenerate manifests,
  reporting every moved record/segment. Do not silently drop duplicates. This
  normalization is explicit; no unsupported claim of exhaustive near-duplicate or
  Unicode-normalization exclusion. Original data audit additionally removed known
  cross-split question and truncated-input duplicates.
- Task labels are the eight source IDs only. Prior data reuse makes all results
  exploratory. Token-graph source and task corpus differ; graph transfer support
  is measured rather than assumed. No semantic labels are imputed.

### Stage 1: selected atoms and task composition

Retain nodes with discovery segment count>=32 and nonoccurrence>=32. Compare graph
leaves (depth 0) against higher nodes (depth>0), same positive-correlation graph,
top-50 neighbors, eight spectral groups, 20 KMeans initializations, fitting seeds
17/29/43. Existing eight-group map is an unchanged reference scored with the same
binary occurrence rule, not an exact reproduction of an activation-weight teacher.
Match leaf/high node counts in five pooled discovery-frequency rank bins, both
sides sampled without replacement, 20 repeats (seed 17), with all three fit seeds.
Save bin membership and selected IDs. If eight supported groups cannot be formed,
record the exact insufficiency; never change group count or duplicate nodes.

Score segments by normalized selected-feature group occurrence; average over each
record's covered segments, retaining record and segment coverage. All-uncovered
records remain unassigned. Lowest canonical group ID breaks ties; report tie rate.
Fit majority task labels on explanation only (alphabetical tie-break), then report
check coverage, covered purity, and macro task recall with abstention counted as
incorrect. Report per-task coverage and three-seed assignment ARI on common covered
records plus coverage-set Jaccard. Depth 1 and >=2 are descriptive strata, not
additional clustering conditions.

Paired original-record bootstrap: 2000 draws, source strata; source and label are
the same object here, so the earlier source-vs-source-times-label distinction
collapses exactly. All metrics use fractions in machine tables and percentages or
percentage-point differences in prose. Matched-set variation is reported separately
from record resampling; matched repetitions are not independent datasets.

### Stage 2: true organization on the same public leaves

For each graph, fit supported high anchors into two parent groups per seed. Freeze
anchor identities and form U from supported graph leaves reachable by at least one
retained anchor. Deduplicate reachable anchors, not path counts. Parent weights for
each leaf are normalized reachable-anchor counts. Per parent, multiply leaf
cooccurrence affinity by the square root of endpoint parent-weight product, then
form four child groups. Every leaf contributes total mass one across eight terminals.
Compare: flat eight-group U; true 2x4 hierarchy; shuffled 2x4 hierarchy. No high-node
activation is added to scoring. An unsupported public leaf or an infeasible parent
group stops that graph's Stage 2; no hidden U change, 3+5 repair, or group reduction.

Generate 199 degree-preserving anchor-leaf shuffles within five leaf-frequency rank
bins, seed 17+null index, target 10 accepted swaps per edge, attempts capped at 50
times target. Same 199 relation arrays are shared across the three fitting seeds;
they are not 597 independent controls. Record target completion, changed-edge
fraction, unique relation hash, parent-weight mean absolute change and fraction of
changed leaves for every seed. Parent weights unchanged within absolute tolerance
1e-12, unsuccessful swaps, identical original, duplicate arrays, or clustering
failure are inadequate controls; do not replace them based on task scores. If fewer
than 199 adequate unique controls remain for a seed, report the null distribution
descriptively and its registered comparison as INSUFFICIENT.

Report true-minus-flat 2000-draw paired record intervals; compare true macro task
recall against the adequate-null 95th percentile separately. Also report task
entropy conditional on parent and on terminal, normalized by check-set task entropy,
including the shuffled reference; missing entropy support stays undefined. Stage 1
does not need to favor high nodes to enter Stage 2; only construction/support gates
can stop it. Task composition or better coverage never proves semantics or utility.

### Resource and output extension

Same local CPU-only container, threads=1, no remote job. Additional clustering
ceiling: two hours, 32 GiB working-process memory target, 2 GiB new artifacts. Full
budgets (three seeds, 20 matched sets, 199 nulls, 2000 record draws) are not silently
reduced. On a ceiling or unavailable input, retain complete partial receipts and
report the exact unexecuted scope. Small synthetic/real-interface checks precede
full fitting; a valid construction-insufficient branch is a result, not a crash.

Save a separate `task_composition/` directory with source/config/protocol snapshot,
input/duplicate/split manifests, role and matched-set lists, group and parent maps,
per-record assignments, metrics/intervals/stability, nulls and their diagnostics,
figures, and terminal receipt. Example selection is on explanation data only;
store record IDs and roles (center/ordinary/boundary), not benchmark text in the
research mainline. Keep original static mining identities unchanged.

Interpretation remains an AI-labeled measurement reading awaiting human judgment.
No automatic Focus/Anchor/Graph update or downstream training is authorized.

A1 execution clarification, before any clustering fit: the 2000-draw paired
record intervals apply to the primary unmatched high-minus-leaf and true-minus-
flat contrasts per graph/seed. All 20 matched-set contrast values are retained
as a separate distribution per fitting seed, without pooling them as independent
records or multiplying the bootstrap budget by matched-set count.
