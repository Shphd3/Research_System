派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/H2/summary.md`。
[精确原始文件](../../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/H2/summary.md)；研究修改仍回到原件。

---

# H2: Conditional relative strength

Protocol result branch: `COMPLETED_INSUFFICIENT`. Scientific acceptance and next decision: `Unknown`. Corrected output reuses an exposed holdout. The original imported hypothesis is unchanged.

## Purpose and hypothesis

Test relative-strength increment conditional on support and total amplitude in fixed C; a static classifier is not conditional mutual information or evidence of native use.

## Experiment and analysis

With u=z times last-layer decoder norm, r=norm(u), b=1(z>0), q=u/(r+1e−12), compare[b,r] to[q,b,r]. Loss0.690265→0.616439; gain0.073825,95% family[0.009994,0.129799], three-theorem-group[−0.010718,0.173821]. Explicit gain0.188398; description gain−0.040747. Same-support coverage17/24 paired texts,10 families; description subset7 pairs, mean gain−0.060363[−0.225542,0.096753]. No subset refitting. Decoder norms195.0443–991.2906 are not unit; no C zero vectors; q finite. Serialized main-model replay passes1e−10. Global support/norm covariates, lexical and nuisance strata executed; optional shuffle omitted as allowed.

## Conclusion, hypothesis revision and AI suggestion

Strength changes and mixed-wording increment are observable, but stable semantic strength coding is insufficient. Fixed candidate set does not mean identical active support. AI suggests requiring consistent relation tracking without answer terms, with wording and length controlled.

See the [Chinese companion with all three figures](summary_cn.md), [main results](../summary.md), [raw metrics](../../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/tables/H2_readout_metrics.csv), [full execution tables](../../../../../../../../../UNAVAILABLE.md) and [Detailed](../detailed.md).
