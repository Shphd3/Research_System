# E21 supplementary readout audit — representations, dictionaries, grouping and semantic interpretation

Evidence status: **COMPUTED / BOUNDED / EXPLORATORY**. Interpretation: **AI_DRAFT_AWAITING_HUMAN_CONFIRMATION**. The researcher requested the initial follow-up and then its fixed-input repeatability/semantic audit on 2026-09-11. No main-model or SAE optimizer updates were performed. This supplement does not close the parent E21 registered verdict or replace its missing parent result records. [Detailed evidence](detailed.md); [frozen parent Protocol](../protocol.md).

Later requested reading path: [meeting v2 SAE classification trajectories and high-node coverage](meeting_v2_readout/summary.md). Its new geometry uses a different arm, position panel and label construction from item1 below; see its scope before comparing numbers.

## Purpose

Determine whether changing SAE-based teacher relations reflects model structure, the readout construction, or unstable grouping, and whether those relations can yet be interpreted as useful semantic supervision.

## Hypothesis

The researcher's intuition is that existing semantic information can be exposed by sparse features and guide expert allocation. A rival is that grouping rules, co-occurrence units, sample composition or token roles change the teacher without establishing new semantic structure. The advisor asked how structure forms and evolves, not that it must become finer or change dramatically.

## Analysis method

- Fix initial geometric members and source weights across original representations; replay identical held-out answer positions and swap encoders/group maps separately on the same h.
- Freeze h/encoder, repeat the actual eight-group algorithm on an identical graph and on source-stratified record bootstraps. Audit the old/new grouping lineage; change only token-versus-segment co-occurrence on identical sampled codes/common features.
- Lock content-only AI judgments of48 masked text pairs before revealing old/new teacher relations. Separate topic, operation, surface format and token role; these are exploratory AI annotations, not independent human ground truth.

## Conclusion

1. **Measured fixed geometric groups do not tighten on average.** Task-only development, mean seed-wise0→512 changes: K-means within dispersion **+5.13%**, between dispersion **+10.97%**; diagonal GMM **+4.19% / +12.55%**, with matching signs in test. Relative separation is not within-group contraction and is not semantic validation. [Geometry](tables/decisive_geometry.csv).
2. **Readout changes are real, but large teacher changes do not establish semantic reorganization.** Final fixed-dictionary support retention is **72.07%**; teacher-relation drift is **0.0534 fixed vs0.3527 refreshed** on the same dynamic trajectory. On the same h, group-only change exceeds encoder-only change in **12/12** windows, ratio **2.45–9.90**; common-feature restriction preserves12/12, ratio **2.44–9.87**. These are dependent windows and nonadditive RMS magnitudes. [Readout](tables/sae_metrics.csv), [swaps](tables/grouping_decomposition.csv), [common support](tables/grouping_common_support.csv).
3. **Later grouping is repeatable on an identical graph but sensitive to sample composition.** At update256, across the three training seeds, solver-repeat teacher-relation RMS ranges **0–0.00391**; record-bootstrap pair comparisons range **0.0682–0.2668**. The initial-state solver range is larger, **0.00595–0.09017**. This weakens the explanation that all later changes are arbitrary solver randomness, while leaving sample sensitivity live. [Repeat table](tables/group_stability/repeat_summary.csv).
4. **The co-occurrence unit itself can produce a large change without any model or encoder update.** The old group artifact references an authenticated segment-incidence matrix with up-to256-token segments; the current refresh recipe uses individual answer-prediction positions. On identical sampled codes and common feature IDs, changing only this unit gives RMS **0.1909–0.3300** at update256, and **0.3528** at the initial state. This is a bounded unit-only reconstruction, not attribution of the historical trajectory: old/new sampling, support rules and historical dynamic code identity are not all matched. [Unit comparison](tables/group_stability/unit_comparison.csv), [lineage limitations](detailed.md#7-follow-up-fixed-input-grouping-and-masked-text-audit).
5. **Semantic guidance and necessity of adaptive grouping remain unestablished.** Among12 deliberately selected persistently high-similarity text pairs, **8/12** were judged topically unrelated and **12/12** shared surface format and token role by one blinded AI annotator. This supplies concrete counterexamples to equating high teacher similarity with common subject matter; it is not a population accuracy estimate or proof that token-role specialization lacks utility. Refreshed reconstruction improves (weighted residual/variance **0.3374 fixed vs0.1078 refreshed** at512), but teacher-change/next-router-change correlations remain mixed (**−0.128 to+0.160**). [All48 judgments](tables/group_stability/semantic_pairs.csv), [stratified counts](tables/group_stability/semantic_summary.csv), [router response](tables/route_response.csv).

![Grouping repeatability and content audit](figures/0911_grouping_followup.png)

Read left as three different sources of variation at256, not additive shares; ranges are empirical repeats, not confidence intervals. Read right as selected-pair AI judgments, not human semantic labels or population proportions.

**Nearest boundary:** original static/dynamic t0 stored h differs despite matching saved weights; unified replay fixes current input equality, not historical training confounding. Historical dynamic source identity remains unverified. The new grouping fit panel is1010 training records/16341 selected positions, not the historical262144-position mixed-step buffers. Fixed K8 cannot establish when the first semantic class was born or a hierarchy formed. No expert-utility, data-efficiency, downstream-gain, SAE-versus-PCA superiority, or universal no-adaptation claim follows.

**Corrected AI proposed next decision:** establish one semantically interpretable structure under a common co-occurrence unit and observation rule, then track it over training. Use independently judged same-operation/different-format and different-operation/same-format pairs to separate content from token role. If the relation follows only format, narrow the claim to format/position structure and do not call it semantic specialization; do not stop observing structural evolution. The researcher owns the semantic granularity, final interpretation and any new main-training scope. “Adaptive grouping is necessary” is currently unsupported, not disproven.


Native-membership comparison (2026-09-11): see [common input empirical centers](native_soft_centers.md). This post-hoc addendum uses GMM posterior and SAE soft mass, unlike the earlier all-hard membership plots.
