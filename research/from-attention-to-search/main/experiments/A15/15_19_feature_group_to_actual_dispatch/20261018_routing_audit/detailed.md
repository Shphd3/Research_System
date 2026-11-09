# Per-feature actual-dispatch diagnosis: execution and interpretation

[Summary](summary.md) · [Original Protocol](protocol_cn.md) · [Source bindings](source_bindings_cn.md) · [Reasoning audit](reasoning_audit_cn.md) · [中文](detailed_cn.md)

## 1. Purpose, hypotheses and comparison boundaries

The parent question concerns improving learning across different content. This round examines its prerequisite: when a low-frequency feature is already active, why does the full input miss the expert designated by its membership list? Rivals are suppression by the original score, top-1 tradeoffs between targets that co-occur but belong to different groups, or insufficient evidence to distinguish them.

We did not assume frequency grouping is effective, equate allocation quality with learning, or call this a φ-grouping validation. No model forward, training, graph reconstruction or deployed-route modification occurred. All measurements derive from the parent run's frozen caches and memberships. Cited old results and newly recomputed quantities are distinguished.

**Bounded AI judgment: define what scores should compare, then test limited score calibration before immediately regrouping.** We localized the winning score path; inspected pair bounds do not force zero reception. Global membership feasibility, separate frequency/amplitude causes, replacement-score utility and learning benefit remain unknown. The question was not closed and scientific state was not changed.

## 2. Authorization, inputs and operations

The user explicitly authorized the uploaded Anchor/Protocol's finite diagnosis, project placement and Daily discussion curation without stagewise review. Chinese originals were preserved byte-for-byte; English companions translate the design without adding primary thresholds. `provenance/design_freeze.json` records source hashes and freeze time. All new computation is in an independent child run; old outputs were preserved.

| Object | Actual binding and treatment |
|---|---|
| Parent run | `/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/frequency_interval_moe/20261018T103820Z`; original Protocol, grouping, route/score code and caches read |
| New execution root | `/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/frequency_interval_moe/20261018T103820Z/routing_audit_20261018T143950Z`; scripts, complete tables, logs and receipts |
| Base | `/data/share/Qwen3-0.6B-Base`, frozen; not loaded for a forward in this round |
| Dictionary | Final A22 selected-14-layer, 16,384-feature `checkpoint_000999997440.pt`; z not re-extracted |
| Encoding | Shared z jointly generated from 14 layers; frozen TRAIN normalization and threshold 0.051281172782182693, not 14 independent within-layer codes |
| Scoring pool | Original 9,615 reliable features: TRAIN n_i≥200, hit contexts≥20, n_i<N; zero reception does not remove a feature |
| Rules | A's original eight linear intervals; B1 seed 20261018 and B2 seed 20261019, each original membership and own route |
| Low set | Original 964 `low_ids`: TRAIN p_i≤q10 of the reliable pool, including ties; threshold 0.002455780647530449 |
| Frequent companion set C | Original 962 `high_ids`, at or above the original TRAIN 90th percentile including ties, p threshold approximately 4.5861%; no p≥0.5 fallback used |
| TRAIN | 130,712 valid prediction positions, 128 existing 1024-token contexts |
| EVAL | 65,402 valid prediction positions, 64 contexts of the same length |
| Access | Current scoped strict checks passed for inputs and the new analysis ID; `assets/checks/2026-10-18_feature_owner_routing_audit_20261018T143950Z.json` |

TRAIN source is `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_5_of_10_shard_00000041_processed.bin`, source blocks 8192–8319. EVAL uses `local-shard_2_of_10_shard_00000247_processed.bin` in the same global shard. Cached global context IDs 117658–117721 correspond to source-file blocks 8192–8255; the fixed offset 109466 was verified.

We retained the parent's valid next-token mask and checked every source-bin t+1 label, unique positions, feature IDs/events, low/high union masks and equality of A's two seed routes. The latter are one deterministic allocation, not independent replications.

TRAIN/EVAL use distinct token files. Original document identity, deduplication and near-duplicate independence are unknown. CrossCoder training saw the source corpus and EVAL had already been inspected. This is held-out-position replication, not new independent confirmation or population inference.

### Reuse and implementation corrections

We reused CSR events, decoder-norm weights, memberships, top-1 and hash rules. Three small entries implement metrics, scoring, and text/finite pairs. Each used at most two threads; concurrency stayed below the eight-core quota. No remote job was added or training loop reused/changed.

An integer assertion caught int16 overflow in the first scoring-script index product; int32 corrected it before successful output. The p×a/load identity check was restricted to n_i>0, retaining a=NA when n_i=0. No failed attempt yielded accepted measurements, and corrections remain in the receipt. Text scores were checked against the original saved norm sums rather than a rounded display table; core counts were not recomputed. Figure adjustments changed legend/NA placement only.

## 3. Objects, formulas and missing values

A position t consists of the current token and its visible prefix; its label is the next token. Feature i is active iff cached z_i>0. Designated expert g_R(i) comes from the membership list; actual route e_R(t) sends the full input to one expert.

With N valid positions, n_i feature hits, N_e received positions and n_ei feature hits sent to e:

\[
p_i=\frac{n_i}{N},\quad a_{ei}=\frac{n_{ei}}{n_i},\quad
\ell_e=\frac{N_e}{N},\quad q_{ei}=\frac{n_{ei}}{N_e},\quad
\mathrm{enrichment}_{ei}=\frac{q_{ei}}{p_i}=\frac{a_{ei}}{\ell_e}.
\]

p is global activation frequency; a is the destination share conditional on feature presence; load ℓ is the destination share over all inputs; q is feature frequency among an expert's inputs. This p is a frequency, distinct from the cross-layer decoder-amplitude share p used in earlier work.

When N_e=0, q/enrichment are NA; a is still zero if n_i>0. With nonempty expert and present feature but n_ei=0, a=q=enrichment=0. With n_i=0, a/enrichment are not estimable. Long tables retain integer denominators and NA reasons. Each rule uses its own g_R and e_R; matching B expert numbers has no semantic meaning across strategies.

We verified Σ_eN_e=N, Σ_en_ei=n_i, n_ei≤min(N_e,n_i), and q=p×a/ℓ. The maximum defined-domain absolute error is approximately 3.33×10⁻¹⁶. Original route-block counts and CSR recounts match exactly. No input was deleted for weak matching or multiple group hits.

## 4. Observation one: membership and reception diverged

A's group sizes are `[9253,183,124,34,7,3,2,9]`, not equal-size groups. Its TRAIN expert counts are `[0,0,0,129,201,646,9893,119843]` and EVAL counts `[0,0,0,64,97,184,6934,58123]`. Three A experts are empty; neither B has empty experts on either split.

| Split/rule | Low features | Feature-equal mean owner a | Median | Zero-reception features | Event-weighted owner a |
|---|---:|---:|---:|---:|---:|
| TRAIN A | 964 | 0% | 0% | 964 | 0% |
| TRAIN B1 | 964 | 5.8868% | 4.1502% | 21 | 5.9343% |
| TRAIN B2 | 964 | 8.8222% | 7.5906% | 5 | 8.7662% |
| EVAL A | 964 | 0% | 0% | 964 | 0% |
| EVAL B1 | 964 | 4.4358% | 3.2808% | 122 | 4.3729% |
| EVAL B2 | 964 | 10.2956% | 9.0909% | 48 | 11.1407% |

Of all 9,615 reliable features, 9,590 have zero designated-expert reception under A. For 9,560 features the designated expert itself is empty, so q is NA. Of the 55 defined q values, 30 are genuinely zero. Do not merge these categories into q=0 or depict only 25 positive values as the entire pool.

The low-feature union covers 95,544/130,712 TRAIN positions (73.10%) and 49,291/65,402 EVAL positions (75.37%). This union is frequent; it cannot replace the 964 individual reception rates. A expert 7 receives 88,524 and 44,608 of these positions, respectively; designated expert 0 remains empty.

[Figure 1](figures/figure1_actual_reception.png) shows expert loads and membership-group zero reception; [Figure 2](figures/figure2_global_vs_owner_frequency.png) shows global p against designated-expert q with real zeros and empty-expert NAs. `tables/group_summary.csv` includes feature-equal quartiles and event-weighted summaries. Full long tables remain execution-side in `metrics/core/feature_expert_metrics.csv` and `feature_owner_summary.csv`.

### Enrichment at a high-load expert

A expert 7's load is 91.6848% on TRAIN and 88.8704% on EVAL. Its enrichment across the 964 low features has 25th/50th/75th percentiles 0.9997/1.0369/1.0650 on TRAIN and 0.9955/1.0549/1.0999 on EVAL. Most are mildly enriched; neither “no enrichment whatsoever” nor “now high-frequency content” follows.

Since a≤1, enrichment=a/ℓ≤1/ℓ: at the current load, any feature's maximum is 1.0907 on TRAIN and 1.1252 on EVAL. This is a denominator/load identity, not a learning-capacity bound. An expert receiving most inputs naturally has q near p; this differs from A0 never receiving targets. These aggregates use `metrics/discussion_aggregates.json`, without another cache scan.

### Descriptive intervals

With seed 20261018 and 200 context-block resamples, the EVAL low-feature mean a has 2.5%–97.5% ranges A [0,0], B1 approximately [3.91%,4.93%], B2 [9.29%,11.17%]. These describe the current context blocks, not independent documents or population significance. See `tables/bootstrap_summary.csv`.

## 5. Observation two: the winning score path

The implementation uses

\[
s_e(t)=\frac{\sum_{i\in G_e}z_{ti}w_i}{|G_e|},
\]

where w_i is the original sum of 14 decoder-vector L2 norms and z is nonnegative. Inactive members contribute zero; the denominator remains the full list size. We did not renormalize, average only active members or change coordinate norms. FP64 sparse accumulation followed by original FP32 storage and top-1 exactly reproduces all six split×rule scenarios. Every 3×8 score at all 12 text positions also matches bit-for-bit.

C counts in A are `[600,183,124,34,7,3,2,9]`: **groups 1–7 consist entirely of C**. C is the original high-frequency list, not a semantic category or a set requiring p≥0.5.

C/non-C decomposition preserves denominators and signed margins. A's original winner and runner-up both come from all-C groups, so their non-C margin is always zero. To address low-frequency failure directly, saved scores also give winner-minus-A0 margins:

| Positions containing low features | N | Mean total margin | C component | Non-C component |
|---|---:|---:|---:|---:|
| TRAIN | 95,544 | +0.567492 | +0.569428 | −0.001935 |
| EVAL | 49,291 | +0.550900 | +0.552779 | −0.001879 |

Non-C terms favor A0 but cannot offset C's margin. This explains the score computation, without treating amplitude, frequency and composition as independently identified empirical causes.

We also verified mean score = overall active-member fraction × event-weighted mean amplitude: H_e/(N|G_e|) multiplied by Σ_ti z_tiw_i/H_e, where H_e counts all member activation events. `tables/score_identity.csv` records the identity. Do not substitute two ordinary per-token means or interpret the factors as independent causal mechanisms.

### Virtual score-term removal and its costs

Only C's score terms were zeroed virtually. z, memberships, denominators, inputs, labels and hash/tie rules remained unchanged. Under A, 100% of positions on both splits move to expert 0, with no all-zero or tied positions. The other seven groups have no non-C scoring members; this is a mechanical composition outcome, **not a successful router**.

All 9,253 A0 features move from a=0 to a=1, while 25 other features with positive owner reception move to zero; 30 group-3 features were already zero. Four additional experts become empty, raising the total from three to seven. C removal accounts for 99.8490% of TRAIN's sum of group-mean scores, not 99.85% of raw z mass.

B1/B2 reassign 60.43%/76.53% of TRAIN and 64.08%/73.71% of EVAL positions, retaining eight nonempty experts. These are within-rule virtual sensitivities. `tables/virtual_routing_summary.csv`, `frequency_band_costs.csv` and full execution-side per-feature tables retain both gains and losses.

No existing effective within-group matched removal was available. Seven all-C A groups also lack comparable replacements, and no new matching search was undertaken. Frequency, amplitude and common semantics were therefore not separately identified causally. Removing high-frequency representation components is not supported.

## 6. Observation three: finite co-occurrence tradeoffs do not force zero

Case eligibility was restricted to original TRAIN low features with n≥30 and at least five contexts. All 964 qualified and all owner a values were zero, so no low/median/high reception contrast existed. Descending context support then ascending ID froze 9297, 1133 and 2704. For each case and rule, only cross-owner partners within the existing 9,615 pool were ranked by TRAIN n_ij/(n_i+n_j), breaking ties by ID; the top three were frozen. This gives 3×3×3=27 records, followed by EVAL lookup only for those records. There was no full-pool pair scan or optimal assignment.

For i,j with different designated experts, requiring at least the same fraction τ of each feature's hits to reach its own expert under top-1 implies

\[
\tau(n_i+n_j)\le n_i+n_j-n_{ij},\qquad
\tau\le1-\frac{n_{ij}}{n_i+n_j}.
\]

An intersection position cannot reach both experts, so total successful reception is at most the hit union. This condition is necessary, not sufficient, and is not a learning-capacity upper bound. No numeric τ requirement was supplied, so no pass/fail threshold was invented. The parent's 200-position/20-context expert engineering gate is not a per-feature reception target.

| Rule | TRAIN necessary upper-bound range | Fixed-pair EVAL range |
|---|---:|---:|
| A | 0.991806–0.996134 | 0.988368–0.997178 |
| B1 | 0.929019–0.982916 | 0.898396–0.985112 |
| B2 | 0.937232–0.988822 | 0.919101–1.000000 |

A's tightest TRAIN-selected pair is 9297/16240: TRAIN n_i=304, n_j=19,588, n_ij=163 gives 0.991806; EVAL 162, 8,521 and 101 gives 0.988368. These restrict near-complete joint coverage, not force feature 9297's reception to zero. B's pairs follow B's own membership and do not diagnose A-specific conflicts.

Unselected pairs, higher-order and joint multi-target conflicts remain possible. Near-one necessary bounds do not prove global feasibility. `tables/conflict_pairs.csv` contains all 54 split rows; TRAIN selections and three-case×pool counts remain execution-side. The evidence does not prioritize regrouping on a claim of unavoidable conflict, but neither clears grouping of all problems.

## 7. What the text checks actually checked

Each TRAIN-frozen ID has three fixed-seed random EVAL hits plus one high-activation hit, preferring unshown contexts: 12 cards total. The high-activation sampling constraints and global maximum z are separately recorded; a context-diverse high example is not falsely called the global maximum.

Cards include original bin, global context, source-block offset, current token, full visible prefix, separate next-token target, z, major companion frequencies/groups, all eight scores for all three rules, winner/runner-up/margin and the result of removing only U's score term. Markdown shows at most the final 100 tokens of the visible prefix, with the current token listed separately; JSON retains the full prefix. Model input was not limited to that preview. Group −1 means outside the reliable scoring pool, not absent from the representation/input.

All 12 A positions reach expert 7. None of the 12×3=36 single-U score removals changes the winner. This shows local argmax insensitivity, not U's uselessness to prediction or a single semantic meaning.

[Figure 4](figures/figure4_text_and_score.png) takes the first frozen random example for each ID without content selection; see [all 12 cards](text_cases_cn.md). For example, one 9297 position has current token “ established” and next-token label “,”: A0 scores 0.002242, A7 0.438244 and runner-up A4 0.183983. Target presence is insufficient to change the winning route. The next token is an explanatory label and never enters the score.

## 8. Frequent companions and actual within-expert frequencies

All 964×962=927,368 low–C pairs are retained for each split in NPZ and compressed CSV, with joint counts, P(c|i), p, each rule's own-expert q_i/q_c, denominators and NA reasons. Few displayed examples did not replace the full target table. No 16,384² matrix was calculated.

Figure 3's three companions per target were frozen by descending TRAIN P(c|i), ties by ID, before EVAL q lookup. Panels distinguish A's designated expert 0 (NA), its main receiving expert 7, and B1/B2's respective designated experts. EVAL support and expert denominators are shown. “Main receiving” never redefines “designated”; real zero and NA remain distinct. The execution tables preserve full distributions; the figure addresses fixed cases only, not all features.

## 9. Completed, unexecuted and genuinely unresolved work

| Protocol item | Status | Delivery/limit |
|---|---|---|
| Assets, mask, label shift, routes and IDs | Complete | Original counts match recount; every source label checked |
| Full-pool p/a/q/enrichment and summaries | Complete | Both splits, 9,615×8; denominators, zeros and NA reasons |
| Context descriptive intervals | Complete | 200 fixed-seed resamples, no independent-population test |
| All low×C companions | Complete | 927,368 rows per split in compressed CSV/NPZ; no target deletion |
| Original score decomposition and virtual C zeroing | Complete | Each rule's membership/route; all feature costs and empty groups |
| Comparable matched-removal control | Not implemented | No effective existing per-group match; no expanded search; independent causes unidentified |
| TRAIN-selected, EVAL random/high text | Complete | Three IDs×four cards; 36 single-U sensitivities |
| Finite cross-owner co-occurrence checks | Complete | 27 TRAIN-frozen pairs, then EVAL; global feasibility unknown |
| Four figures, scalable files, sources, audit and Daily | Delivered | PNG/SVG/PDF, origins and hashes in manifest |
| New calibration, regrouping or learning training | Not run | Outside this round, not a task failure or negative learning result |

**No core in-scope step was skipped because of a missing file.** What remains unresolved is the score objective, per-feature reception requirements and acceptable losses elsewhere, and whether changing reception improves learning. These need a later explicit design and authorization.

## 10. Resources, records and reproduction

The CPU quota was eight cores, aggregate RSS limit 16GiB and new-disk limit 2GiB. No GPU or paid job was submitted. Successful entry wall times were 22.13 seconds for core metrics, 15.26 seconds for scoring and 49.10 seconds for companions/text/conflicts; exact original-weight text-score verification took another 8.28 seconds. Entries overlapped, so their sum is not end-to-end wall time. Other time covered input checks, freeze, correctness, figures and writing.

Per-entry maximum RSS was approximately 0.95GiB core, 1.45GiB scoring and 1.38GiB cases; their sum is below 4GiB. The two-second concurrent monitor sampled approximately 1.98GiB at peak; this is not a continuously observed maximum. `provenance/completion_receipt.json` records full wall time, final disk increase and monitoring scope. No analysis window or statistical object was reduced to fit the budget.

`provenance/core_receipt.json`, `score_receipt.json` and `cases_receipt.json` retain parameters, count checks and outputs; source identities are bound by the delivery records. `provenance/figures_manifest.json` stores figure hashes and sources. Computation entries are `scripts/core_metrics.py`, `score_audit.py` and `cases_conflicts.py`; `plot_audit.py` reads saved tables only. Full data stay execution-side; selected evidence tables, figures and texts enter the research project, with itemized provenance in `payload_manifest.json`.

## 11. Knowledge update, rivals and one next decision

The earlier idea was that grouping rare features might let their designated expert learn them. We now know that membership does not guarantee input reception: the current full-group mean first lets high-frequency-list terms dominate routing. Frequency grouping remains an unvalidated design candidate. The failure explanation narrows to a checkable score path rather than a universal rejection of grouping or learning.

Rivals remain amplitude/frequency scale, group size/composition, higher-order co-occurrence tradeoffs, route load, and whether received inputs offer useful learning. Their independent effects were not identified. The sole recommendation is to define reception goals and costs, then separately register score calibration with unchanged lists—not simultaneously regroup, train or scan parameters. If explicit reception requirements are later excluded by concrete co-occurrence bounds, that tradeoff would justify priority attention.

This round stops after computation and records. Mechanism judgment, scientific approval and the next decision remain with the researcher.
