# October 31 meeting: five analyses of domain-discriminating CrossCoder members

Prepared 2026-10-30, Asia/Shanghai. [Chinese speaking entry](meeting_brief_crosscoder_domain_members_cn.md). This is a derived meeting record; scientific acceptance/closure remain Unknown. No new model forwards, training, PCA fitting or distance expansion. Existing R04–R09 results are preserved.

## Five bounded conclusions

1. **Frequency:** original groups contain low/middle/high counts 0/8/8 for math and 3/10/3 for biology (16 each). The eligible pool has 602/3241/4262 plus8 low-support members, n=8113. Math's 50% high-frequency fraction is close to the pool's52.53%; biology's18.75% is lower. R09 log-width sensitivity changes these counts to0/14/2 and4/10/2. Group labels depend on binning.
2. **Decoder geometry:** mean PC1–64 squared unit projections are20.55%/19.85%, medians18.96%/14.89%; dictionary mean8.85%. Math exceeds its exact frequency/support-matched set range6.73%–11.81%. Biology matching is unavailable. No math and one biology member exceed50% head energy; an average head bias does not mean every member is head-concentrated, or that head energy is knowledge.
3. **Spectral overlap:** per-PC overlap0.778438; 64-PC-band overlap0.980014. Aggregation hides within-band differences. Above-matched-background overlap is unanswered because one required bin has no noncandidate. Unmatched dictionary16+16 pairs have per-PC95% range0.7792–0.8078 and band range0.9285–0.9797, a descriptive context only. Actual decoder subspaces have mean squared principal cosine0.07647, not0.7784/0.9800. Spectral overlap is not semantic or functional overlap.
4. **Real input tokens:** each member activates on306–2972 observed token IDs across19200 natural positions. Single most frequent ID contributes0.78%–32.34% of a member's active positions. Active-token panel domain composition follows selection direction, descriptively. Reference-seen-token conditional median frequency has pooled Spearman correlation0.02165 with member occurrence; fixed-list document-bootstrap interval[-0.01377,0.04735]. Reference-unseen IDs occupy8.1%–56.4% of active positions and remain missing. The unconditional frequency relationship is unanswered.
5. **Context versus identity:**5/32 have descriptive same-target context replication across wordings, discovery and exposed old heldout;0 are B;27 are C. Nineteen never activate on either fixed target and have insufficient coverage, not identity-only evidence. A members are f8963,f14394,f3464,f10937,f652; three pass both targets, two onlyexample. Lexical/topic rivals remain.

## Unified objects and selection

A22: native14-layer joint shared z,16384 coordinates, fixed999997440-token checkpoint SHA25609b432e98dd7426f9ea4170809d75068a2ada2ed38c1e97d3fa18e119cd79628. Only its zero-based block27 residual-post decoder is analyzed, before final norm. No last-layer-only encoder is used.

R04 has120 real English documents:60/domain, discovery/development/old-heldout30/10/20. Each has192 tokens; native z is averaged over positions32–191 including zeros. A member qualifies with positive activation in at least5 discovery documents in each domain. The math-oriented AUC is the probability a random math document has a higher mean than a random biology document, counting tieshalf. A fixed positive decoder norm leaves this within-member AUC unchanged. Rank by absolute distance from0.5, IDascending for ties, take first16/sign. Pool8113 includes17 exact-chance ties excluded from directional selection. The 16+16 prefixes agree with the existing natural-document64/sign ranking; this reporting cut is exploratory. Old heldout is repeatedly exposed and never used to replace members. Direction-fixed heldout AUC medians0.9750/0.9406; minima0.9075/0.8175.

Math: f8963, f14394, f11163, f14316, f4309, f12351, f3098, f3464, f8030, f7134, f6718, f10937, f11420, f14491, f359, f1382.

Biology: f11710, f652, f12141, f598, f8838, f4862, f1010, f14278, f3477, f12266, f734, f13132, f9491, f6289, f15702, f11852.

Reference basis is R07's independently acquired natural-document PCA,1024 orthonormal columns, fit on9600 positions from the60 R04 discovery documents. It is not R08's refitted mixed basis. Every decoder is unit-normalized; squared projections sum1. No activation, norm, RMS or eigenvalue weighting. Zero norms0/32.

## 1. Activation-frequency groups

![figure1_frequency](/data/250010109/Research_System/daily_research_reports/1031/meeting_report/crosscoder_domain_members/figures/figure1_frequency.png)

Question: are discriminating members unusually rare or frequent? Left axes show16 members/group as stacked counts; right axes show8113-eligible-pool proportions. Main equal-count cuts are0.259399%/1.344299%, minimum20 reference hits; sensitivity log-width cuts0.451726%/6.686506%. Frequency is native z>0 count/65536 DCLM positions. The result revises an assumption that domain discrimination requires rarity; the labels and pool composition limit stronger interpretation. No contribution totals substitute for member counts, and no selection-uncertainty inference is claimed.

## 2. Unit decoder direction

![figure2_decoder_spectrum](/data/250010109/Research_System/daily_research_reports/1031/meeting_report/crosscoder_domain_members/figures/figure2_decoder_spectrum.png)

Question: which covariance ranks contain decoder orientation, and is an average driven by a few members? Sixteen bands have64 PCs each; pale lines are individual members, solid means, dashed medians, dotted full-dictionary mean. The math gray band is a1000-set exact-matching composition range. Its observed head mean exceeds the matched range; biology matching remains NA. Top2 members account for26.80%/34.39% of group head mass. This revises 'all selected members sit in head PCs'; the quantity is orientation, not actual activation/contribution or knowledge amount.

## 3. Shared spectral distribution

![figure3_spectral_overlap](/data/250010109/Research_System/daily_research_reports/1031/meeting_report/crosscoder_domain_members/figures/figure3_spectral_overlap.png)

Question: how much do group-mean squared projections cover the same PC ranks? Both curves average16 unit decoders equally. Shading sums the smaller group fraction in each64-PC band; separate per-PC overlap retains within-band differences. The two overlap resolutions differ substantially. Pairwise absolute cosine mean0.03044, maximum0.97850 (f359–f12266); both actual decoder spans rank16. Principal cosines start0.97934 then at most0.25187, with average square0.07647. Similar spectral position does not imply equal direction or subspace. Matching bins are floor(log2(reference hits+0.5)) × floor(total discovery active documents/5), excluding all32. f9491 has39 reference hits and5/27 discovery supporting documents: its required bin has0 alternatives. No fallback or forced retention was used. Full matched pair comparison and observed selection-uncertainty intervals remain unavailable; random-set ranges are not such intervals.

## 4. Real tokens and token occurrence

![figure4_tokens](/data/250010109/Research_System/daily_research_reports/1031/meeting_report/crosscoder_domain_members/figures/figure4_tokens.png)

Question: does a member respond across input IDs, and does feature frequency track token frequency? Panel4a uses the first discovery rank/domain, with high, median-positive and same-ID low/inactive examples, at most2 examples/document/member. Exact input IDs, strings, positions and read prefixes are saved; future text is excluded. Panel4b has one point/member, log axes, conditional median of reference-seen input-token rates and10th–90th percentiles. For f8963, input5322 ` problems` has observed z0.16433 versus0 in another document; for f11710,785 `The` has0.11758 versus0. Natural examples are not controlled edits. All16 math member active-token panel math-fraction medians exceed0.5; all16 biology ones fall below0.5 (group medians0.631/0.278), still a same-panel selected association.

Feature frequency counts positive feature positions; token frequency counts token IDs in the same independent65536-position reference (256windows/254canonical document groups). Unseen IDs are excluded from rate quantiles, reported separately, never declared zero true probability. Within-group correlations are-0.1001 (math, document interval[-0.1605,-0.0507]) and-0.0147 (biology,[-0.0590,0.0252]). The300-draw within-domain document bootstrap keeps selection/reference fixed and is not selection uncertainty or independent generalization. No consistent positive relation or complete unconditional relation is established. No decoder-to-vocabulary output analysis was added.

## 5. Fixed-token context responses

![figure5_context](/data/250010109/Research_System/daily_research_reports/1031/meeting_report/crosscoder_domain_members/figures/figure5_context.png)

Question: does the selected direction persist while current token identity stays fixed? Main examples are the first2 ranks/domain, retaining the all-zero case. The appendix plots all32. X=example/explanation × W0/W1; y=raw mean z(math)-z(biology). Discovery24 versus old-heldout12 families are separate; whole-family paired2000-draw bootstrap gives pointwise95% intervals. Development12-family values are also saved. Active-member counts in the four cells are11/11/8/8 in discovery and12/9/7/8 in old-heldout, denominator32. Thirteen members are ever active;19 never are.

Descriptive A requires, for at least one fixed target, both wordings in discovery and old heldout to retain the natural-discovery direction with all four pointwise95% intervals excluding0 and at least3 active families in one domain/cell. This is not the original R09 rule or multiplicity-corrected inference. B requires nonzero controlled-target support, no A, and at least50% natural activation concentrated on5 IDs; it still cannot prove identity-only encoding. Otherwise C. A=5,B=0,C=27 (19zero+8unstable). Old R09's36-member rule intersects this list only at f8963,f14394,f3464,f359,f652; that intersection differs from the new A set. Comparingexample with explanation changes both token and ending and cannot itself establish context response. A weakens pure current-token identity while retaining earlier-term/topic rivals.

## Evidence, missing items and stopping

Existing: R04 natural/reference cache and discovery ranking, R07 fixed PCA, R08 full joint z, R09 decoder and old candidate lists. New offline: the16+16 reporting cut, member-count frequency summaries, geometry/overlap/background recomputation, actual-token examples/counts, and per-member fixed-target effects/categories. All 2795 independent checks passed. Images received visual self-review; no independent listener test or rendered-math validation was claimed.

Further resolving the19zero/8unstable C members would require fixed-token/position paired-prefix tests on actual responding natural IDs, hence new forwards; these are recorded as missing and NOT RUN. Missing match alternatives and reference-unseen token rates are distinct background/counting gaps, not permissions for forwards. No new execution is proposed or started. See [definitions, full list and reproduction](/data/250010109/Research_System/daily_research_reports/1031/meeting_report/crosscoder_domain_members/appendix.md), [master](/data/250010109/Research_System/daily_research_reports/1031/meeting_report/crosscoder_domain_members/tables/master_members.csv), [frozen list](/data/250010109/Research_System/daily_research_reports/1031/meeting_report/crosscoder_domain_members/tables/frozen_list.csv), [mapping](/data/250010109/Research_System/daily_research_reports/1031/meeting_report/crosscoder_domain_members/tables/list_mapping.csv), [frequency history](/data/250010109/Research_System/daily_research_reports/1031/meeting_report/crosscoder_domain_members/frequency_history.json). Computation stops after this delivery.
