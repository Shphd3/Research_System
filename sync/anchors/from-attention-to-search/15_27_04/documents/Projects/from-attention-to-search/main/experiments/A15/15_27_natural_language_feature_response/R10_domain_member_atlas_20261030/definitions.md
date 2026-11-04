派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R10_domain_member_atlas_20261030/definitions.md`。
[精确原始文件](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R10_domain_member_atlas_20261030/definitions.md)；研究修改仍回到原件。

---

# Definitions and protocol changes

| Object | Computation / denominator | Interpretation and boundary |
|---|---|---|
| Native member | A22 joint14-layer shared z, original norm-weighted threshold | Not an independently encoded final-layer activation |
| Document response | mean z over positions32–191 including zeros,160 positions/document | All documents have equal weight |
| Support | >=5 positive discovery documents in at least ONE domain | Failed support is insufficient data, not no information |
| Raw AUC | all30×30 math/bio document comparisons, ties half | Stable ranking discriminator, not every nonlinear rule |
| Main set | support and direction-fixed discovery AUC>=.75 | All members retained regardless of later results |
| Heldout check | fixed direction,20docs/domain;1000 document bootstraps | Exposed exploratory reuse, not a new blind test |
| Feature occurrence | DCLM positive positions/65536; >=20 hits for bins | Occurrence is not activation strength or spectral position |
| Original frequency bins | low<=.002593994140625; middle<=.0134429931640625; otherwise high | Cuts belong to lower group; support<20 outside plotted denominator |
| Log-width sensitivity | cuts.0045172553628813825/.06686505701697326 | R09 used this as main; R10 uses original labels as main |
| Common spectrum | pooled9,600 raw block27 residual-post discovery h rows; one shared mean | Equal domain/doc/position weights,1024 full-rank PCs; no per-domain centering, whitening or h unit normalization |
| Unit projection | squared dot of unit decoder and each PC;1024 sum1 | No z, decoder norm or eigenvalue factor |
| Group overlap | sum PCwise minima of member-equal mean distributions | Band aggregation hides differences; not direction/function overlap |
| Matched background | eligible dictionary, same frequency/support strata/group sizes,1000 disjoint pair draws | Includes selected members; conditional reference range, not a generalization interval |
| Group reconstruction energy | sum z times restored decoder first, project/square, doc-equal mean, normalize | Cross terms preserved; not full-h variance explained |
| Panel token frequency | count ID within19200 natural analysis positions | Type bins: count1/count2/count>=3; type vs position denominators separate |
| High response | >discovery-positive-z90th percentile, threshold fixed before heldout | Quantile needs20 positives; composition needs5events/2heldoutdocs; otherwise retained as insufficient |
| Context A | paired math−bio native z at same target ID and paired position | Changes context/terms/format together; not isolated semantics |
| Ending contrast | E1−E0 at matched core text | Target AND suffix change; pure target identity B missing |

This round changes the support gate (both domains→either), replaces16+16 with all AUC>=.75, fixes Top16/64/128 and.70/.80 sensitivities, makes pooled natural-all-token covariance explicit and uses panel-token counts. It does not splice old32-member values into the new960-member figures. Old R07 “independent natural spectrum” wording is corrected for this analysis: it is the same R04 discovery spectrum. Old rounds are preserved. Old global Top16=9math+7bio is distinct from old per-domain16; every old membership has a separate mapping.
