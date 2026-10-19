> **R0: the researcher has authorized bounded cached analysis, qualification and five figures.** 2026-10-15. The original draft is preserved; the [execution registration](execution_amendment.md) supersedes its authorization snapshot and freezes operational choices. Document independence and scientific practical-importance confirmation remain Unknown.

# Draft Protocol: Feature Relation Groups and Frequency

[中文](protocol_draft_cn.md) · [Asset audit](assets_checked.md) · [Decisions needed](decisions_needed.md) · [Report draft](../EXTERNAL_DEPENDENCIES.md#external-75f32fcadb2288d2) · [Reasoning audit](design_reasoning_audit_cn.md)

## 0. Review snapshot

This delivery is a proposal for discussion. All new analyses are NOT RUN. The first question is whether co-occurrence groups in a fixed dictionary are reliable, have similar frequencies, and can be associated with inputs. Expert allocation comes later. Structural evidence cannot replace a learning experiment.

| Item | Status and meaning |
|---|---|
| Document | DRAFT_NOT_EXECUTABLE; no AI proposal has researcher confirmation |
| Current authorization | Local read-only checks, preserving attachments, drafting the Protocol/report, naming this chat, and creating its separate memory; no formal statistics, plotting, analysis implementation, training, or remote job submission |
| Sole scientific design source | [Received Anchor v0.1](../sources/ANCHOR_特征频率与共同出现_v0.1.md), preserved byte for byte; the [later integration requirements](../sources/PROMPT_报告与绘图整合要求_先写Protocol.txt) update hypothesis names and exposition while retaining statistical safeguards |
| v0.2 report | The later prompt refers to 《飞书报告_特征关系分组与频率_v0.2.md》, but its body was not supplied in this delivery. We do not claim to have read it. The current report follows only the integration requirements actually received |
| Focus | No researcher-confirmed Focus/problem_key for this question was bound in the project roadmap and relevant records inspected. The explicit request permits this discussion draft. It does not create or reset a Focus; formal ownership and promotion await the researcher's choice |
| Experiment role | One structural measurement and metric audit; the four analysis stages are not four separate experiments |
| H1 | After checking high-frequency background and sparse-coding constraints, reproducible co-occurrence groups exist, and within-group frequencies are closer than in matched controls |
| H1a / H1b | H1a is the original Anchor's structural hypothesis; H1b is its frequency hypothesis. They have separate readouts, and both must hold to support the new H1 |
| H2 | Using frequency for actual input allocation improves learning on inputs containing low-frequency features, with fixed expert count K, capacity, exposure, and budget, without a material sacrifice in overall loss; planning only, NOT RUN |
| Proposed fixed object | Final 14-layer/F16384 CrossCoder, existing full VAL cache, and D/V joint counts for all features; neither the 0.5B checkpoint nor a 28-layer/F32768 dictionary |
| Minimum feasible scope | Structural and frequency exploration within the existing cache, plus calibration of the complete analysis pipeline against randomized baselines on a bounded sample; replication on independent original documents remains UNKNOWN |
| Conditions preventing promotion | Unresolved document/near-duplicate independence, a null model that fails qualification, or unconfirmed decision-critical parameters; attractive figures cannot repair any of these |
| Approval | A–G are unconfirmed; cross-block consistency has only draft self-review, not design PASS; there is no execution approval or freeze time |

The filename follows the user's requested protocol_draft.md. This directory contains this one English main draft and its Chinese companion; there is no competing protocol.md. Earlier experiment approvals apply only to their earlier stages and do not authorize this run.

## 1. Objects, counts, and scientific question

An input is one valid token position x in its fixed original context. Feature i is one latent coordinate of the fixed CrossCoder. All selected model layers jointly produce one z_i(x) at that position; layers are not independent samples. A decoder norm measures the size of a reconstruction direction, not a hit probability.

The existing cache already applies the encoder's fixed TRAIN threshold. An event is a strictly positive gated z in that cache:

\[
a_i(x)=\mathbf{1}[z_i(x)>0],\quad n_i=\sum_x a_i(x),\quad n_{ij}=\sum_x a_i(x)a_j(x),\quad p_i=n_i/N.
\]

N is the number of valid positions on the analysis side in question. p_i is occurrence frequency. It is neither word frequency, mean amplitude, decoder layer share, nor one mutually exclusive category of a probability distribution. The p_i values therefore need not sum to 1. Co-occurrence means occurrence at the same position; it must not be mixed with window or document co-occurrence. Raw counts must be retained before deriving other quantities.

A group is a candidate set of features formed from positive co-occurrence relations. It is not an expert, causal module, or confirmed semantic object. Main groups are disjoint, but an input can hit multiple groups. A common feature occurs frequently on the inputs associated with several groups; the globally most frequent Top10 cannot automatically define all common features.

The strongest rival for H1a is that marginal frequencies, the per-position activation budget, and a few sources or repeated texts suffice to produce the apparent structure. The strongest rival for H1b is that the relation metric, edge selection, and grouping algorithm already prefer similar frequencies. H2 also faces capacity, exposure, sample difficulty, learning objective, and allocation-conflict rivals. This round does not resolve them.

## 2. Fixed assets and reuse choices

Execution root E is /data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder. Earlier analysis root R is E/analysis/feature_relation_phase1/20261013T173130Z. The exact inventory, current strict-access receipts, source code, and gaps are recorded in [assets_checked.md](assets_checked.md) and its [Chinese companion](assets_checked_cn.md).

| Fixed item | Value and boundary |
|---|---|
| Base/tokenizer | /data/share/Qwen3-0.6B-Base, revision da87bfb608c14b7cf20ba1ce41287e8de496c0cd; 28 blocks, hidden size 1024, frozen |
| Dictionary for this analysis | E/runs/formal_14layer_batchtopk_a22/checkpoint_000999997440.pt; training exposure 999,997,440 |
| Checkpoint SHA256 | 09b432e98dd7426f9ea4170809d75068a2ada2ed38c1e97d3fa18e119cd79628; producer hash, without rereading the 5.6 GB weights to recompute it in this round |
| Selected model layers | One-based 2,4,…,28; zero-based 1,3,…,27; block residual-post, with the last layer before the final global norm |
| Cache | R/feature_cache/manifest.json; N=10,485,760, F=16,384, nnz=2,669,034,642, mean L0=254.538978767395; 640 CSR chunks, about 16.10 GB |
| Binding | The cache manifest binds the checkpoint SHA, data manifest SHA, complete TRAIN normalization/EMA threshold, layer list, BF16/FP32, SDPA, and original inference batches |
| Data | E/data/direct_dclm_bins_a15/index_val; fixed windows from a single DCLM bin; data manifest SHA 874794a8657f8982f7abb12ee517ec551fce840d9f20dfe103f48589a6779849 |
| Count reuse | R/counts/total0.npy and total1.npy: one F×F int64 matrix per D/V side, with all pairs accessible; about 2.147 GB each; use memory mapping and chunks |
| Marginal reuse | R/feature_frequency.npz contains side-specific counts and marginals for 81 contiguous blocks; within-block joint counts for arbitrary new pairs are not already complete |
| Code reuse | CSR/count semantics from R/code_snapshot_v2/features.py, original position mapping from core.py, and context location from inspection.py; read the sources as references rather than invoking the earlier complete run entrypoint |
| Required adaptation | A new undirected phi graph, one main grouping method, randomized baselines, missing-value rules, group-to-input readouts, and new figures; this round defines their interfaces without implementing or running the analyzer |
| Not reused as new evidence | Earlier directed edges, the frequency-doubling rule, graph level h, transitive reduction, and earlier Top10 deletion results do not define or decide this round's H1 |

Training used BatchTopK with global batch mean k=256, rather than exactly 256 activations at each position. The training score is the ReLU activation multiplied by the sum of that feature's decoder L2 norms across layers. Cached inference compares score>threshold strictly, using the complete saved TRAIN EMA threshold. It does not take a new TopK within inference batches. TRAIN centering and vector-RMS are fixed and are not fitted on D/V.

The gating algorithm thus imposes no new inference-batch quota on each position. BF16 GEMM values can nevertheless change with batch size. The earlier small batch check applies only to the positions it checked; it does not establish positionwise equality across the whole window. The main analysis uses the events already saved in the cache. It retains the original definition of 16 complete contexts per Base forward and 1024 valid positions per coder batch, without changing batches or re-encoding.

## 3. Data split and independence: establish the answerable scope first

A document-level design should first recover original_document_id and near_duplicate_group, then assign entire documents/duplicate groups to discovery and untouched confirmation sides. Assignment must not depend on activations, frequencies, or desired groups. Retain source fields. Report within-source and mixed-source results before discussing source effects; do not remove every source difference as noise.

The reusable D/V sets follow the earlier split_manifest.json assignment of contiguous blocks containing 128 contexts each. N_D=5,238,097 and N_V=5,247,663, across 81 blocks. Both sides have already been inspected. A context is not an original document, and contiguous blocks need not contain different documents. The main proposal therefore retains these sets for exploration within the cache; it does not relabel them as untouched confirmation data.

Original-document mapping, near-duplicate isolation, and source-stratification mapping are currently incomplete. This does not prevent frequency description or structural checks conditional on this cache. It does prevent the full H1 judgment of replication on independent texts. This round does not automatically build new data or encode a full dataset. If the researcher requires a document-level claim, first choose an existing alternative dataset with recoverable mappings, confirm its scope, and separately record any encoding authorization required.

The statistical observation unit is a position. The independence unit for uncertainty should be a document/duplicate group. Without original documents, the minimum fallback resamples entire contexts or existing contiguous blocks and explicitly states that their independence assumption is unverified. Token-independent binomial tests and token bootstrap must not produce misleadingly narrow intervals. Resplitting does not erase the fact that the original validation window has already been exposed.

Special tokens, padding, and valid positions follow the original index/excluded_ids; this analysis does not change the denominator. Missing values, duplicate keys, infinities, negative z, repeated feature IDs within a CSR row, or mismatched layers/hashes/splits block measurement. Do not silently discard or impute them.

## 4. Four stages of one analysis

### 4.1 Frequency distribution and stability: which features are reliably measurable in this window?

Inputs are the full D/V marginals, marginals for the 81 blocks, and CSR/context indices. Reuse feature_frequency.npz for frequency ranking and the D/V comparison. Derive context coverage from CSR if required; hits in 81 blocks are not document counts. Report mean amplitude separately from frequency.

Define candidate pool P on discovery data and then freeze it. The main proposal uses hit counts and the number of covered independent units as reliability conditions, excluding p_D=0 or 1 where phi is undefined. All remaining features still appear in the overall frequency table. n_min, minimum document/context coverage, and acceptable interval width remain undecided. The earlier n≥200 rule is not a validated standard for this new question. First inspect existing counts and coverage; then, on an approved calibration sample, choose conditions using target precision and estimable coverage. Record the complete reliability curve and freeze the rule without tuning to the same-frequency result.

Zero hits mean only that the feature was unseen on that side's window. Zero hits or inadequate support in V do not remove members from P and do not justify adding an arbitrary epsilon. The corresponding log frequencies or group readouts are unestimable. Report their coverage and route them to insufficient evidence.

Outputs are n/p, side, coverage, amplitude diagnostics, and reliability flags for all F features; a discovery-fixed rank; frequency intervals and rank stability from document resampling or conditional block resampling. Spearman correlation is auxiliary. Low frequencies and zero hits must remain visible. Good stability supports reproducibility only within the measurement scope, not a natural hierarchy. Features with wide intervals or poor coverage remain undecided in later stages; they are not declared unrelated.

### 4.2 Relations: do they exceed high-frequency background and activation-count constraints?

Derive the following quantities from complete joint counts in chunks, on the domain 0<p_i,p_j<1:

\[
p_{ij}=n_{ij}/N,\quad P(j\mid i)=p_{ij}/p_i,\quad \mathrm{lift}_{ij}=p_{ij}/(p_i p_j),
\]

\[
\phi_{ij}=\frac{p_{ij}-p_i p_j}{\sqrt{p_i(1-p_i)p_j(1-p_j)}}.
\]

AI proposal: use phi as the primary relation measure. It is symmetric, signed, and subtracts the independent marginal background. A necessary sensitivity readout is log2(lift), with raw support and coverage shown alongside it. Large lift for rare events cannot select edges by itself. Save negative relations as diagnostics; they do not form this round's positive co-occurrence groups.

Phi does not remove frequency preference. If 0<p_i≤p_j<1, even complete inclusion of i in j gives the following maximum positive value:

\[
\phi_{\max}=\sqrt{\frac{p_i(1-p_j)}{p_j(1-p_i)}}.
\]

The maximum can be 1 for equal frequencies and is smaller when frequencies differ substantially. Keeping frequency distance out of the clustering objective is therefore insufficient to avoid a circular same-frequency conclusion.

AI proposal for the main graph: operate only within reliable discovery pool P. For each node, retain its top q=10 neighbors with adequate joint support and phi>0. Connect only mutual selections with undirected edges weighted by phi. Break ties by stable feature ID. q controls graph size as an engineering proposal; it is not a significance threshold. The joint-support threshold remains undecided and will freeze with the reliability rule. Use q=20 only as one necessary sensitivity analysis, without selecting a winner by its H1/H1b result. Do not first divide P into frequency bins and build separate graphs within them.

Degree is at most q, so there are at most Fq/2=81,920 edges. Complete pair readouts may still be saved as chunked disk tables. Edges are selected relations, not millions of individually significant discoveries. Any future edge-level testing needs a separate test family, valid tests, and FDR control. This proposal instead calibrates two global endpoints; a few randomized samples must not masquerade as edge-level p-values.

### 4.3 Groups and frequency similarity: does structure remain beyond metric preference?

The sole main grouping method is greedy weighted-modularity merging on the positive-weight undirected graph, with proposed resolution γ=1. It specifies neither expert count nor an expected number of groups. Its objective compares observed within-group edge weight with the expected weight for nodes of the same strength. It does not contain within-group frequency distance. Reuse the existing NetworkX environment. Freeze the exact version, stable ID order, and tie behavior during approved implementation; stop if qualification fails rather than switching algorithms. Report no edges, only singletons, one large cluster, or q sensitivity honestly. Do not force attractive groups.

Freeze candidate pool, graph rule, and groups G_D on D. Independently construct the graph and groups G_V on V using the same P and rules, without tuning on V. If a fixed member has p=0 or 1 in V, retain its candidate identity and mark phi unestimable. Do not calculate 0/0 or fill undefined relations with 0. That node has no estimable edges. Explicitly record the resulting group-replication and coverage losses without removing it from P. The H1a global replication endpoint T_a matches non-singleton D and V groups one to one by maximum total membership Jaccard, then divides by the number of non-singleton D groups. Unmatched groups contribute 0. If D has no non-singleton groups, T_a=0 and the record states that structure did not form. Additional V groups are not directly penalized, so this is a directional replication readout.

Also report the nontrivial-group count, coverage, largest-group share, and the mean within-group phi of frozen D groups on V. A high match for one large cluster does not establish useful partitioning. Minimum practically meaningful group-count, coverage, and effect conditions require researcher confirmation; they cannot be set after seeing results.

H1b evaluates frozen D groups using V frequencies. For a group g whose fixed members are all estimable, define dispersion in decimal orders of frequency:

\[
\ell_i=\log_{10}p_i^V,\quad \bar\ell_g=|g|^{-1}\sum_{i\in g}\ell_i,\quad D_g=\sqrt{|g|^{-1}\sum_{i\in g}(\ell_i-\bar\ell_g)^2}.
\]

Smaller D_g means closer within-group frequencies. The primary summary gives equal weight to groups; a feature-weighted summary is reported separately. Singletons do not participate. A missing member makes its whole group unestimable; deleting members must not improve D_g. Counts of missing groups and members, and their coverage, enter the overall judgment. Minimum total estimable coverage remains undecided. Unconfirmed or unmet coverage routes the result to insufficient evidence.

Three controls are minimally sufficient, and answer different questions:

1. **Random groups from the same candidate pool with the same sizes.** This tests whether frequencies are closer than in arbitrary groups. Preserve the entire group-size sequence, randomly permute members, and fill groups in order. Do not match each member's frequency.
2. **Controls matched on mean group log frequency.** Sample candidate groups of the same sizes from P and match their D mean log frequency to each real D group's mean. Do not match or select on V. The proposed tolerance should depend on the D frequency range and available candidate count; it remains undecided. Freeze tolerance, maximum attempts, and inadequate-match handling before reading V outcomes. Report each group's matching error rather than forcing poor matches. V is used only for evaluation. Candidate groups may recur across randomized repetitions; freeze repetition count and seeds.
3. **A complete-pipeline null preserving row and column marginals.** Preserve each feature's total hit count and each position's activation count. On the same bounded sample, rerun support selection, graph construction, grouping, matched controls, and all endpoints. This tests metric and algorithm preference; the first two controls cannot replace it.

The primary frequency effect T_b is the equal-group-weighted mean of each estimable group's D_g minus the V D_g average of its mean-matched random groups. Negative values support closer frequencies. Report the effect in dex, its difference relative to controls, and an interval, rather than only a p-value. If simple random and mean-matched controls disagree, report the conflict without selecting the favorable control.

### 4.4 Groups to inputs: can candidate structure become an inspectable allocation object?

For each nontrivial group, define score_g(x) as the number of active members divided by group size. The main proposal determines each group's hit threshold on D and requires at least two members to be active together. The threshold follows a fixed reference hit-rate ceiling/random baseline, not attractive V examples. The reference rate and threshold remain undecided. First retain score distributions and groups that cannot meet the rule. After freezing thresholds, evaluate each group's hit independently at every valid V position.

Report the proportions with no hit, exactly one group hit, and multiple group hits. Each denominator is all valid V positions; the three proportions sum to 1. Also report each group's coverage and Jaccard between group-hit events. Forced top-1 allocation must not hide conflicts. Group IDs are neither expert IDs nor semantic labels.

Reuse the earlier index/tokenizer/inspection logic for text location. Proposed examples per group are 5 random and 5 high-score cases, with a seed to freeze and deduplication across contexts. Do not select by text meaning. Retain the sampling population, position, complete model-visible prefix, target token, active members and original z, and other group hits. Predefine high-score ordering by score, activation amplitude, and position ID. Truncation is for display only; the complete visible context remains execution-side. Any right-hand text displayed must be labeled as reading context that the model cannot see at this position.

Because main communities are disjoint, a feature that is common across groups is defined through its hit rate on group-associated inputs: c_ig=P(a_i=1 | group g is hit). It is not claimed to belong to several main communities. If i contributes to a group hit, calculate the diagnostic with i excluded from the score to avoid self-inclusion. Common/discriminative thresholds remain undecided. This is diagnostic only: do not directly delete globally frequent features or remove common components from real model representations.

Extensive multiple-group hits limit a direct mapping of one group to one top-1 expert. They do not automatically refute structure or every routing strategy. Text tables cannot replace aggregate statistics or establish semantic purity or learning benefit by themselves.

## 5. Affordable randomized baselines, statistics, and stop rules

### 5.1 Minimum version of the main question and calibration sample

Use the full cache for description and candidate discovery to avoid re-encoding. Its earlier D/V split is exposed review data. To bound the cost of the marginal-preserving baseline, the AI proposes fixed S_D and S_V samples. On each side, select 128 complete original contexts by a seeded hash of context position keys. Within each context, select 32 valid positions by a fixed hash of position keys, yielding at most 4096 positions per side. Sampling depends only on original position identity, not z, frequency, groups, or text meaning. Keep and record the actual count when fewer than 32 positions are available. Retain original model-visible contexts without re-encoding sampled positions.

Run the same complete analysis from scratch on S_D/S_V, including defining P, groups, and matching parameters independently on S_D and evaluating on S_V. Groups discovered from the full cache cannot be treated as discoveries free of selection bias within the subsample. Low-frequency features lacking support in this subsample are an uncovered population; do not extrapolate to them. Subsample null p-values calibrate only that subsample pipeline. They do not confer significance on the earlier full graph, full-data edges, or original-document H1.

### 5.2 Scope of marginal-preserving swaps

On each side separately, swap legal 2×2 submatrices [1,0;0,1] and [0,1;1,0] in the sparse event matrix, prohibiting duplicate edges. Proposals must be symmetric; rejection remains a self-transition of the randomization chain. The exact proposal distribution and implementation will freeze after qualification tests. Each randomization preserves every row degree k_x and column count n_i. Record seeds, proposed/accepted swaps, and exact marginal equality. This controls activation-count constraints but does not fully simulate the continuous Base/CrossCoder mechanism, document dependence, or numerical threshold geometry.

Use at least two independently seeded chains. At predefined increasing checkpoints in accepted swaps/nnz, monitor overlap with original events, phi quantiles, group count/sizes, and T_a/T_b. Checkpoints, burn-in, spacing, and acceptable chain differences require the small qualification run's timing and mixing record. Do not invent a sufficient number of swaps. Stable diagnostics are necessary but not sufficient. Continued drift, systematic chain differences, a high rejection rate, or failure to qualify within budget means the null failed. Stop inference without automatically extending the run.

AI proposal: target B=99 approximately qualified randomized pairs, each containing separately randomized D and V matrices. Report effective sample count and autocorrelation from the two chains. B does not mean 99 independent documents. The minimum Monte Carlo resolution is 1/(B+1)=0.01. If effective B is too small, do not give finely resolved p-values or claim edge-level FDR. Correlated MCMC draws are not independent exchangeable null draws. Effective sample size (ESS) is diagnostic only; replacing the rank-formula denominator with ESS does not produce valid p-values.

Every null runs the same candidate selection, positive-phi/support filtering, mutual-neighbor rule, grouping algorithm, D mean-matched random controls, and V evaluation. Keeping real groups fixed does not remove the algorithm's same-frequency preference. If a null draw has no non-singleton groups, T_a=0 under the existing rule; T_b is undefined if no groups are estimable. Do not discard and redraw such draws to reach B, or fill their values with 0/epsilon. Before the formal run, freeze an estimable-coverage condition applying equally to real and null data. If either fails it, record the failure proportion and mark H1b calibration insufficient without computing a selectively filtered rank p-value. A source-stratified null becomes a necessary diagnostic only after reliable source IDs are available. For now this remains a gap; context IDs cannot impersonate sources.

### 5.3 Endpoints, intervals, and multiplicity

Larger T_a supports replication; more negative T_b supports closer frequencies. Use (1 + the number of null values at least as extreme)/(B+1) for one-sided approximate Monte Carlo calibration. Apply Holm correction to these two predefined global endpoints, with proposed familywise α=0.05. Both subjudgments of the original H1 must hold. Holm is conservative control for these two endpoints, not authorization for edge-level or group-level discoveries. Its usual error-rate meaning requires valid p-values. Correlated chains here provide approximate conditional calibration; they do not establish a guarantee of nominal FWER. Do not use significance language if null mixing or dependence assumptions fail qualification.

After freezing groups, use document/duplicate-group bootstrap for frequency-effect and input-coverage intervals. With the current cache, intervals are conditional on context/contiguous-block assumptions; the proposal is 1000 repetitions. Retain complete groups and missingness flags in every resample rather than censoring rare members. Report membership stability for T_a separately. Fixed-group bootstrap is not rediscovery stability. An interval for T_a would require whole-block resampling with graph construction and regrouping, plus a separate budget; it is not part of the minimum required run.

n_min, coverage thresholds, practical-importance values δ_a/δ_b, minimum group/overall coverage, matching tolerance, input thresholds, null-qualification parameters, and resource ceilings are undecided. The proposal is to calibrate precision and feasibility on D, then obtain confirmation and freeze them. Do not choose thresholds using V effects or final p-values. Without practical-importance boundaries, report effects and do not equate nonsignificance with absence.

## 6. Figure contract: define now, generate after approval

Each figure answers one question. Within a figure, retain only a short title, axes, units, legends, necessary reference lines, and location markers. Put explanations below it. Use consistent Chinese fonts/sizes and a colorblind-friendly palette, with line/marker styles as additional distinctions. Design for normal Feishu reading width. Export PDF, SVG, and readable PNG. Save each plotting source table, script, command, input files, and hashes. Actually open every figure to check Chinese text, cropping, overlap, legends, zeros, and agreement with its source table. This round generates no new figures and claims no such visual checks.

| Figure | Question, axes, legends, and predefined display rule |
|---|---|
| 1. Frequency rank | x=feature rank fixed by discovery-side p; y=activation frequency, in percent or with an explicitly labeled log axis. D/V lines follow the same ID order; V is not reranked. Count zero hits separately without epsilon. The title states only “Feature activation frequency ranking” |
| 2. Frequency stability | x=p_D, y=p_V; one point per feature and y=x. Separate the positive double-log panel from one-sided/both-sided zero-hit panels. Transparency/density and reliability flags must not hide low frequencies. State N_D/N_V, valid F, and the source of conditional intervals |
| 3. Relations and groups | The main panel is a phi matrix with identical ID ordering on both axes, group boundaries, and a separate frequency color bar. Phi and frequency have separate legends. Save the full matrix. If a subset is required, order groups by D group size and sample equal numbers within groups by stable hash, up to 300 IDs in total (proposed/unconfirmed); selection must not depend on V or appearance. An auxiliary local network has no arrows and does not call its layout a hierarchy. Define the frequency meaning of node size |
| 4. Within-group frequency and controls | x=frozen group ID; y=D_g, the SD of log10 frequency in dex, with lower values meaning closer frequencies. Show real points, random/mean-matched control distributions and intervals, and group sizes. Leave unestimable values blank and marked NA. Do not show only two mean bars. Show complete-pipeline null global endpoints in another panel, not as the same kind of error bar |
| 5. Inputs and activations | A readable text table: group ID, random/high-score status, model-visible context, marked target position, active members and z, and other group hits. Place unique/multiple/no-hit coverage nearby. Cases do not replace population conclusions; mark omissions explicitly |

Every figure has four fixed explanation items below it: “How to read,” “Observation,” “Meaning for the main question,” and “Next step.” Observations and conclusions currently say “To be filled.” Do not presuppose a long tail, natural hierarchy, stable communities, or expert benefit. Comparison with earlier graph level h is optional: its edges required frequency doubling, so it already contains a frequency constraint and cannot establish this round's same-frequency conclusion. Cross-layer decoder heatmaps and spectral analysis are outside the main task.

## 7. Scale, time, peak memory, and qualification stage

These estimates use only saved dimensions and historical execution receipts. No new counting or timing run has started. The hardware plan is a budget proposal rather than a resource request; this round makes no new device connection.

The full CSR logical payload is about 16.10 GB. The two D/V int64 full-pair matrices total about 4.295 GB. Stream chunks and use memory mapping instead of keeping everything resident. Prohibit N×F×F, about 2.81×10^15 entries, and unconstrained dense N×F event matrices.

For k_x hits in row x, sparse enumeration costs Σ_x k_x(k_x−1)/2. Substituting mean L0=254.54 gives only a rough lower-bound scale of about 3.38×10^11; actual cost also depends on row-degree variance and the upper tail. Reuse existing full counts directly. Controlled disk/memory-mapped F×F outputs are allowed; this is not a ban on all two-dimensional matrices.

Each subsample side has at most 4096 rows. Using mean L0 gives about 1.04×10^6 nonzeros and 1.32×10^8 unordered pairs per side. The B=99 D/V complete-pipeline null entails about 2.62×10^10 pair updates, plus swapping, counting implementation, and grouping overhead. Do not cost 198 matrices as one computation. Account for swaps separately using actual proposal/acceptance counts. Retain output summaries and seeds, process randomized matrices serially, and do not save 198 complete F×F matrices.

Historical measurement: earlier phase1 used 629.63 seconds of active compute in a 4 H100 environment. Encoding took about 127 seconds, full joint counting about 87.5 seconds, and merge about 121.5 seconds. The maximum recorded process RSS was about 12.25 GB. This work did not include the proposed swap/null/grouping pipeline and is not a promise of current runtime or single-host peak memory.

| Stage | Current proposed cost, estimates only | Host peak-memory proposal and assumptions |
|---|---|---|
| 1. Frequency/stability | Marginal tables 1–5 minutes; CSR scan for context coverage 2–15 minutes | 4–8 GiB, streaming; do not cache all z; use block marginals for conditional bootstrap |
| 2. Full phi/edge selection | 5–30 minutes | 8–16 GiB, chunks of 128/256 feature rows; reuse both memory-mapped count arrays without re-encoding |
| 3. Main graph grouping, random groups, effect tables | 10–60 minutes | 8–16 GiB, q=10 sparse graph; no repeated runs of different clustering algorithms |
| 3. Bounded complete-pipeline null | A reliable ETA requires qualification; preliminary uncertain budget range 0.5–8 hours | Proposed host RAM ≤32 GiB and allowance of 8 CPU workers, with serial or limited concurrent work; GPU acceleration requires separate device scope and is not requested by default |
| 4. Group scores/coverage/text | 5–30 minutes | 8–16 GiB, streaming CSR and source-token location; do not load the Base |
| Five figures and explanations | 5–20 minutes plus manual inspection of each figure | 4–8 GiB; figure 3 subset ≤300 IDs; full tables remain execution-side |

This is not a promise to finish the whole question in 10 minutes. After approval, the recommendation is a qualification stage first. The researcher confirms resource and total-time ceilings in decisions_needed. Stay within the proposed subsample, use ≤4 nulls and short checkpoints from two chains, with proposed hard limits of CPU 30 minutes and RAM 32 GiB. Statistics from qualification test implementation, cost, and mixing only; they are not H1 results. If limits are exceeded, the null is unqualified, or member coverage is severely inadequate, save failure receipts and stop. Do not automatically enlarge samples, add devices, or remove controls. If the total budget is insufficient after qualification, report current evidence as insufficient rather than dropping the essential null and declaring support.

Optional extensions, in order, are confirmation after recovering original-document/source mapping, increasing sample size to cover rare features, a source-stratified null, an earlier-h comparison, and cross-layer decoder plots. The first two become necessary when full document-level or low-frequency conclusions are required. None of the other extensions enters this round automatically.

## 8. Pre-implementation checks, artifacts, and command boundary

Completed checks are limited to sources, paths, manifests, small files, array headers, and asset access. No checkpoint tensors were loaded, and CSR was not scanned for new statistics. If the next stage is approved, first implement small analytic examples: independent background, repeated pairs, rare high lift, equal/unequal-frequency complete inclusion, one large cluster, V zero hits, and marginal-preserving swaps. Check hand-computed counts and phi/lift, row/column conservation, no self-edges/duplicate graph edges, grouping and matching, missingness propagation, and input proportions summing to 1. Formula implementation checks are engineering qualification rather than empirical discovery.

Do not execute the old run.py directly: it encodes, counts, and plots beyond the present scope. The proposed new entrypoint E/analysis_tools/feature_frequency/run.py and output E/analysis/feature_frequency/<frozen_run_id>/ do not yet exist. The command contract requires explicit input_manifest, fixed_split, sample_manifest, frozen_config, mode=qualification or full, output_root, and hard budgets. Refuse to run if any critical field is absent. Actual executable commands and the code snapshot must be added during later implementation review; this draft does not pretend that a script already exists.

The input manifest records registered IDs, original paths, checkpoint/normalization/threshold/inference/data/cache/code identities, current strict receipts, and large files not rehashed. Outputs comprise frequency tables, support/missingness tables, sample/split manifests, raw counts and relation chunks, graph edges, frozen groups, group matching, T_a/T_b with every control, null qualification/seeds/marginal receipts, input-hit tables/text, five figure source tables and explanations, and resource/failure receipts. Large payloads stay execution-side. Research_System holds only the Protocol, report, and small provenance tables. Register actual outputs through the asset lifecycle after they exist; do not register nonexistent artifacts now.

## 9. How outcomes change judgment

| Branch | Permitted judgment and next step |
|---|---|
| H1a and H1b both supported, with critical qualification/precision conditions satisfied | Structural grouping and close frequencies are compatible within the preregistered cache/sample and its independence assumptions. Only document-level conditions can support full H1. This produces candidate allocation objects for H2, without establishing learning benefit |
| H1a supported, and H1b intervals sufficiently exclude a meaningful same-frequency advantage | Co-occurrence organization may mix frequencies. Retain relation grouping and frequency grouping as separate later strategies; failure of H1b does not refute structure |
| H1a unsupported with sufficient test precision | Weaken the judgment that this encoding/data/relation scheme yields stable groups. Do not refute all feature structure or all frequency-allocation strategies |
| Wide intervals, inadequate rare-feature/document coverage, unqualified null, only one large cluster, or undecided critical parameters | Insufficient evidence. Identify whether the limitation is measurement, independence, sample size, metric, or compute. Do not call nonsignificance absence |
| Strong overlap of multiple groups on inputs | A one-group-to-one-top-1-expert mapping is limited. Retain multiple-group information and leave the routing hypothesis to the researcher rather than forcing labels |

Practical-importance thresholds await confirmation. Without them, the analysis cannot claim to exclude a meaningful effect. The researcher confirms all scientific conclusions. Every actual result in this round is NOT RUN.

## 10. Step two, H2: necessary planning only, no experiment activation

The four stages in step one serve H1. Step two asks whether frequency can guide actual input allocation and help learning. An independently motivated H2 based on constructed frequency allocation remains possible even if H1 is unsupported, but the changed rationale must be explicit.

Determine each mapping in sequence: fixed feature events → predefined input-frequency/group scores → a rule allowing unique, multiple, or unassigned inputs → actual capacity and token loads for fixed K experts → prediction loss on a fixed learning task. Feature-group count need not equal K. Test loss cannot select the mapping rule. Common components remain in the complete inputs received by selected experts. This neither adds a common expert nor deletes common components from representations.

The minimum later comparison is frequency-informed allocation versus frequency-independent allocation with equal K, parameter count, compute, load, and exposure. A claim that relation groups add value also requires an equal-budget relation-group control. The learning object, optimization objective, whether the Base trains, expert insertion position, capacity/K, definition of low-frequency inputs, training/confirmation data, difficulty/loss baseline, budget, and overall-loss noninferiority bound are all unconfirmed. Current z, phi, or graph quality cannot replace them.

The expected primary readout is the loss difference on low-frequency-feature inputs in an independent confirmation set, constrained by overall-loss noninferiority and fair coverage/exposure. Thresholds and aggregation cannot be chosen afterward. This draft contains no executable H2 configuration, run request, or benefit conclusion. Review step one first, then complete H2 from its actual outputs and the researcher's choices, without automatically starting training.

## 11. Approval, audit, and preservation of the earlier design

| A–G block | Draft status | Confirmation needed / blocker |
|---|---|---|
| A. Question/boundary | PROPOSED | Adopt the new H1/H2 names; Focus/problem_key is unbound and will not be created on the researcher's behalf |
| B. Data | BLOCKED | Choose limited cache-conditional claims or separate document confirmation; original-document/near-duplicate mappings are missing |
| C. Task/information | PROPOSED | No new training labels; D selects and V evaluates, with prior exposure and subsample scope explicit |
| D. Model/structure | PROPOSED | Fixed final14 cache, phi, mutual neighbors, one grouping method, and q sensitivity |
| E. Optimization | NOT_APPLICABLE | No trainable parameters in this round; H2 is not yet designed |
| F. Comparisons/decisions | BLOCKED | Support/effect/coverage/matching/input parameters and null qualification are unfrozen; two global endpoints and multiplicity handling are proposals |
| G. Resources/artifacts | PROPOSED | Subsample, B, CPU/RAM/time limits, and stop-on-qualification-failure rule; no execution approval |

The [reasoning audit](design_reasoning_audit_cn.md) checks argument boundaries. It confers neither scientific approval nor run authorization. This document is explicitly a discussion draft. A complete A–G layout cannot replace human confirmation.

Proposed Anchor changes, without altering the original: rename the original H1/H2 to H1a/H1b as requested, then name learning utility H2; add the fact that an existing cache is bound to final14; separate document-level reproducibility from feasible cache-internal block review; and add the phi frequency bound, limits of the subsample null, and precise definitions of disjoint groups/common features. These changes respectively prevent hypothesis-name confusion, avoid re-encoding, preserve independence boundaries, prevent method preference from being mistaken for an empirical regularity, and avoid self-inclusion. Retain the other boundaries between structure, frequency, and learning.

Before design approval, every choice remains AI_PROPOSAL/UNKNOWN_OR_BLOCKED. Design confirmation is not execution approval. If the same scope is later explicitly authorized, continue within that authorization without asking again. Before execution, record in this file the frozen scientific-body hash, code/config/data identities, approved scope, and time. After execution, preserve the original contract. An appended amendment records each change's old value, new value, reason, whether results were already visible, affected conditions, and evidence eligibility.

Stop for this round after completing files and separate memory, awaiting the researcher and discussion assistant's review. No formal statistics, plotting, analysis implementation, training, commit/push, external sync, or new user chat has been performed.
