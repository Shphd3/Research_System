# S05 protocol: AC/AD SVD geometry and paired parent-to-fine differences

APPROVED_FOR_BOUNDED_OFFLINE_S05 by current direct user request. Prompt1 is the completed S04 neutral-suffix study; require its completion,verification and exact cache hashes. Never fall back to S03's old suffix. Preserve all S03/S04 files. No model forward,training,probe,intervention,new text or automatic next experiment. Existing H1/H2 scientific hypotheses and question owners15_27_06/07 remain unchanged; this is exploratory geometry, not functional evidence.

## Objects and primary question

Separate two frozen native SAE dictionaries (30000coordinates each), using S04's24texts and final colon token25 after exact newline+'Description:'. ATTN is block27o_proj output before residual add; MLPIN is actual block27mlp input after residual add and post_attention_layernorm. Original ReLU-Top32 encoding and preactivations are already saved; no weights need loading. Positive preactivation excluded by Top32 remains final z=0, not completely unresponsive. The input model/tokenizer/SAE identity is inherited from verified S04 receipts, not freshly rerun.

Compare (1) overall centered variation of P/cat vs P/dog exploration samples and (2) actual paired cat-P vs dog-P differences. Both groups use exactly the same P rows/reference coordinates. Similar overall axes need not imply similar signed parent-to-child changes. Shared parents, wording,object/animal referents,explicit class words and family variation can explain alignment; neither similarity nor difference proves semantic identity,distinct function or causality.

## Frozen matrix design and scales

Exploration F01-03; check F04-06, all four conditions grouped. AC rows are [F01P,F01cat,F02P,F02cat,F03P,F03cat]; AD replaces cat by dog and keeps identical P rows. Each6x30000 matrix is centered by its OWN six-row exploration column mean, both means saved. Rank at most5. Primary raw z; supplemental u=z*own decoder-column L2 norm, both reported. Norm weighting is not a full decoder mapping: decoder nonorthogonality means u-coordinate Euclidean geometry need not equal1024-dimensional representation geometry. No decoder-space comparison is run.

Fit thin float64 SVD separately for each site/scale/group on exploration ONLY. Save original and centered sample matrices,row IDs,means,all singular values and valid right directions. Sign convention: largest absolute coefficient positive,ID breaks ties; all scores/coefficients flip together. Primary comparisons fixed before fitting: absolute cosine of PC1; principal angles and normalized projection overlap for top2subspaces. Save all absolute/relative adjacent singular gaps,rank and relative-gap<.1descriptive warning. Numerical rank tolerance=max(shape)*float64_eps*s1; rank<k makes k-dimensional comparison undefined. Do not interpret arbitrary null vectors. Near-zero vector threshold for cosine=1e-10*max(1,mean exploration-row norm for that site/scale); return undefined rather than epsilon-normalizing.

Freeze top5absolute-loading atoms per valid PC1/PC2,per group/site/scale,ID tie break,using exploration only. Freeze exact bases/means/member lists before accessing check projections. Separately include original S03 H2 member list and particularly ATTN14602/3516,even if zero or not top-ranked. No holding-based atom replacement.

## Direct differences and decomposition

For all6families compute full30000-dimensional cat-P and dog-P, their lengths and signed cosine; compute discovery mean vectors/lengths/signed cosine. Project all these vectors directly onto both frozen bases; paired difference projection equals centered child minus centered parent, so do not subtract a group mean from a difference. Report every check family's alignment/length relative to its discovery mean,not just favorable families.

Split each paired difference into disjoint retained-positive amplitude change,Pzero/finepositive recruitment,and Ppositive/finezero loss. Save vectors,IDs,raw values,preactivations,norms and squared-norm shares. Per-family shares sum1. Means of these parts may overlap across families: do NOT sum their squared lengths as independent energy. Save mean-part norms and the3x3cross-dot contribution table; its nine terms divided by full mean-difference norms sum to the signed mean cosine. Also record componentwise cosines,with near-zero undefined.

For each original fitted group/PC,decompose exploration total scoreSS exactly into2*sum(family-midpoint score squared)+.5*sum(paired child-parent score squared). This distinguishes between-family midpoint variation from within-family parent-child variation without assuming semantic causes.

## Projection, stability and member explanation

Project every exploration/check P/cat/dog/N row using each group's own saved mean and basis. Save coordinates,classwise descriptive center/spread in the frozen2D coordinates and per-family paired score differences. No check refitting or reselection; class summaries are descriptive,not classifiers. Show original texts and raw activations/Top32/preactivations for every selected-loading atom and all fixed H2 atoms across all24rows.

For stability enumerate all27ordered family bootstrap samples of length3with replacement from F01-03,keeping P/C/D and labels paired and using the same resample for AC/AD. There are10distinct unordered multisets;27is not independent sample size. Refit resampled exploration only; rank-deficient k metrics undefined. Report valid counts,min,5th/median/95th/max for reference-axis alignment,top2overlap,AC/AD comparisons and paired mean cosine. Quantiles describe this tiny empirical resampling,not confidence intervals or reliable significance.

Counterexample display is fixed: first check family with fine-P signed cosine to discovery mean<=0; else first check own-basisPC1 paired projection reversing its discovery mean sign; else first check cat-P/dog-P cosine below exploration minimum; else explicitly none meeting rule and show first check case without inventing failure. Keep every family and all failures regardless of chosen example.

## Validation, artifacts and stop

Three proportionate audits cover scientific identification,data/statistics,and numerical implementation. CPU float64 cache-only SVD; optimizer/gradients/LM-loss telemetry not applicable. Validate exact source/matrix row identity,centering,rank,orthogonality,reconstruction,SVD-vs-Gram spectra,subspace formulas,difference/decomposition closure,projection differences,top-member freeze lineage and all old hashes. Curated figures use only frozen data; inspect actual renders. Save scripts,data,means,directions,raw differences,bootstrap rows,member tables,plots,bilingual summaries and ChineseDetailed in new S05 child and register actual output asset. Append a bounded mainline record,not a hypothesis/state rewrite. No commit/push/publication.

Supporting/contrary/insufficient branches concern only observable candidate geometry: aligned or opposed signed differences,aligned overall axes but divergent paired changes,unstable directions/rotations or insufficient rank. Never turn separated plots into a general rule. Stop after delivery for joint review.
