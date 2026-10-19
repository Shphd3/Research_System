# Detailed: cached feature relations and frequency

[中文](detailed_cn.md) · [Summary](summary.md) · [Figures](figures_cn.md)

## Result eligibility

Experiment CC_FEATURE_FREQUENCY_20261015T143300Z completed bounded descriptive analysis and qualification. Full H1 is **BOUNDED / INSUFFICIENT**: within-bin H1a replication is measured, all-group H1b is undefined, null qualification fails and formal B99 is NOT RUN. H2 is NOT RUN. Researcher scientific judgment and question closure remain Unknown.

## Objects and estimators

A feature is a fixed latent coordinate. Events are cached gated z>0, not decoder norms or per-layer independent samples. Frequency p_i=n_i/N counts eligible positions; joint n_ij counts the same position. Training k256 is a batch-average budget.

\[
\phi_{ij}=\frac{Nn_{ij}-n_in_j}{\sqrt{n_i(N-n_i)n_j(N-n_j)}}.
\]

Undefined denominators remain NA. Group frequency dispersion is V log10-frequency population SD, ddof0, in dex; lower means more similar. Preserve missing members rather than adding epsilon. Observations are positions; independent documents are unknown. Existing contiguous-block bootstrap1000 intervals are conditional, not document-valid. Random-control95% ranges are not sampling confidence intervals.

## Registration and conformance

[R0/R0.1](execution_amendment.md) records explicit execution authorization and pre-endpoint probability corrections; the earlier draft body is preserved. Frozen config SHA569b8ee9595a4455fd98f8a6912665b282f02925018186a180071bacafa7e7d9. No new Focus/problem_key or scientific approval is fabricated.

| Item | Actual behavior | Eligibility impact |
|---|---|---|
| Input | final14/F16384 fixed full VAL cache and exposed D/V; fresh strict access | Same object, not independent documents |
| Methods | Positive phi, mutual q10, greedy weighted modularity gamma1; q20 sensitivity | No frequency-distance objective; phi bias still needs null |
| Support | D hits100,10 old D blocks,pair hits10 | Engineering filters, not precision/document guarantees |
| Attempt0 | Stopped during marginal/bootstrap/candidate preparation before graph endpoints | Old accepted-step code excluded; corrected fixed-proposal R0.1 version used |
| Controls | Size permutation200; D-mean-constrained membership MCMC±0.1dex | Correlated approximation;44 unqualified groups retained |
| Primary T_b | All186 real groups required | Undefined, not rescued using142 selected groups |
| Null | Each side128contexts×32positions;two chains,4 full qualification endpoints | Margins pass; undefined T_b prevents qualification; no99 formal draws or p-values |
| Input rule | D-only minimum count≥2 with≤1% D hit rate, frozen for V | All V positions included; no forced top1 |
| Examples | Uniform hash-ranked hit contexts then hash-ranked position; high score by count then position | Not uniform-token or amplitude-ranked sampling; right context only a reading aid |
| Rendering | Fixed300 IDs; diagonal masked and phi color saturated; top20 main figure plus all186-group PDF | Presentation-only changes; no statistical or node selection changes |
| Document/H2 | NOT RUN | No independent-document H1 or learning claim |

## Setup and provenance

E=/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder; R=E/analysis/feature_relation_phase1/20261013T173130Z; W=E/analysis/feature_frequency/20261015T143300Z.

Frozen Qwen3-0.6B Base revision da87bfb608c14b7cf20ba1ce41287e8de496c0cd; final checkpoint E/runs/formal_14layer_batchtopk_a22/checkpoint_000999997440.pt, SHA09b432e98dd7426f9ea4170809d75068a2ada2ed38c1e97d3fa18e119cd79628. Observe model blocks2,4,…,28. No weights loaded this round.

Input representation ID representation_crosscoder_qwen3_final14_f16384_val10485760_phase1_20261013t173130z. Saved TRAIN cutoff0.051281172782182693, centered vector RMS, SDPA, BF16/FP32,16contexts/Base and1024eligible/coder remain unchanged. N10,485,760;D5,238,097;V5,247,663;nnz2,669,034,642 over640CSR chunks. Reuse R/counts/total0.npy and total1.npy. W/asset_access_preflight.json records current access; code and config snapshots remain execution-side.

## Evidence ledger

| Quantity | Source/transformation | Observed value | Boundary |
|---|---|---|---|
| Frequency stability | R marginals→W/frequency.csv→descriptive_digest | Spearman0.9979156 | Exposed same-bin description |
| Zero hits | Full marginal counts | D353,V393,whole-window290 | Not permanently dead |
| Positive V frequency | n_V/N_V | Median0.37956%,max99.26360% | Excludes393 V-zero features |
| q10 graph/groups | Full cohit→phi/mutual q10→single method | D34,757edges/186groups;V34,743/185 | P15,666;13,807 D non-singleton members;1,859 singletons |
| Member replication | Maximum one-to-one Jaccard matching |0.5483796213 | No calibrated formal null p-value |
| q20 sensitivity | Change q only |65/61groups;Ta0.5424153390 | Partition scale is parameter dependent |
| Size controls | Group V SD vs random bins |0.35331 vs0.67565dex;delta−0.32234 | Does not remove mean/phi bias |
| Mean-matched primary | All186 fixed groups vs D-matched controls | NA;142qualified groups,48.37%member coverage | Partial delta−0.21516 is selected-subset description only |
| Sample observed | Fixed hash4096positions/side, rerun pipeline | P6750;Ta0.1953114;TbNA | Cannot calibrate full graph |
| Swap qualification | Two full-F row/column-preserving chains | Margins pass;NOT_QUALIFIED;formalB0 | Failure involves undefined Tb, not observed margin corruption |
| Inputs | D threshold→all V cached events |none1,818,978;unique2,073,616;multiple1,355,069 | Denominator5,247,663;exhaustive classes |
| Examples | CSR+original keys+ByteLevel tokenizer decode |176groups×10=1,760 |10 unachievable thresholds;contexts are not documents |

Registered fixed-group dispersion uncertainty is in W/main/dispersion_uncertainty.json. The primary matched-effect interval remains unestimable; random-control ranges must not be mislabeled as that interval.

## Failures, interpretation and next decision

All186 real full-data groups have estimable V frequencies. Of44 unqualified mean-matched controls,15 cannot supply20 scheduled draws within10,000 proposals and29 fail burn-in acceptance≥group size. These are disjoint here. No members/groups were discarded, budgets extended or tolerances tuned after outcomes.

The10,000 cap was not fully checked against group-size scheduling: for size>333,10×size burn-in plus20×size spacing necessarily exceeds the cap. This engineering prerequisite needs a new preregistered correction, not a negative frequency conclusion or post-hoc rescue.

The four checkpoint Ta diagnostics span0.03494–0.04080, versus sample observed0.19531. They are qualification diagnostics rather than a formal null distribution; accepted-count checkpoint times are not formal fixed-proposal draws. Do not compute p from four diagnostics. H1 remains insufficient. Substantial input overlap constrains a direct one-group/top1-expert mapping, without establishing semantics, common function, causality or utility. The one AI-proposed next decision is whether to repair control budget scaling and preregister a bounded H1 rerun; researcher judgment remains Unknown.

## Execution and checks

Main+q20 took186.03s; null qualification279.66s with recorded peakRSS2.964GiB; input scanning/examples542.66s. Stages overlap; their sum is not wall time. cpu-only-local within60minutes, noGPU,0new encoding/training. Main has32GiB address-space/4CPU-affinity/BLAS1 limits. Whole-task aggregate peak RSS was not continuously recorded; the null peak is not the full-task peak.

Nine core synthetic tests and null hand-count/margin/transition-symmetry tests pass engineering scope. Independent checks verify both full matrix diagonals, all69,500q10 edge counts/phi,44 fixed endpoint neighbor sorts, complete candidate partitions and all186 Jaccard matches. Core start/current/snapshot SHAae3567e7e24052e54e09c70cc7ccea34ce9c509fbe166cbb121e84509c904dc3 matches. All118 old text examples match location/token/full-prefix decoding; producer additionally checks10. See W/independent_core_checks.json. None establishes independent scientific replication.

Five figures are actually opened for Chinese text/cropping/legends/NA checks. W retains raw tables, full phi, groups, controls, sample/null diagnostics,1,760 examples, figures/source tables/scripts/commands and receipts. [Artifact manifest](../evidence/original_artifact_manifest.json) binds saved paths/hashes and registered output access. Large payloads stay execution-side. No H2, document confirmation or formalB99 output exists. Anchor/Focus scientific states remain unchanged.


Aggregation matters: real dispersion is0.35331dex with equal group weights, but0.66846dex when weighted by group membership (size-control0.85257dex). Small groups cannot stand in for the feature population. Equal-group weighting remains the primary descriptive aggregation; report both separately.
