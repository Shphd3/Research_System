派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R16_20261102_layerwise_head64_intervention/summary.md`。
[精确原始文件](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R16_20261102_layerwise_head64_intervention/summary.md)；研究修改仍回到原件。

---

# Layerwise head64 intervention: observations

## Purpose
Measure final native next-token preservation after a SINGLE Qwen3-0.6B-Base block residual-post is replaced by its TRAIN mean plus centered top64 PCA projection, followed by the unchanged suffix. This is intervention sensitivity, not intrinsic layer importance. No shallow/coarse or deep/fine order is assumed.

## Observations and key data
Natural panel175documents/700positions; separate37document/the panel. Independent layer-specific PCA uses the same60R04discovery documents/9600positions for every layer, no evaluation fit. Detailed complete values and original inputs are in [Chinese Summary](summary_cn.md), [casebook](casebook_cn.md), [raw evidence](../../../../../../../../UNAVAILABLE.md). Original full NLL=2.341800nat. Old last-layer basis remains separately labeled legacy_head64. Raw records=249843; identity guard passes all28layers. Full original-top1 reference mismatches=0, legacy top1 differences=0; maximum old-basis NLL replay error=0.000201225nat.


Natural-panel preservation (%, equal-document means; complete uncertainty in evidence):

|Layer|All-prefix|Target-only|All-prefix true NLL|Target-only true NLL|
|---|---:|---:|---:|---:|
|1|21.00|77.43|5.8906|2.7565|
|7|15.86|78.00|6.7635|2.6717|
|14|16.00|74.71|7.1134|2.8010|
|21|27.29|41.00|5.5355|3.9061|
|28|23.00|23.00|5.9027|5.9027|

Scope differences are the strongest descriptive observation. All-prefix preservation is nonmonotonic acrossdepth. At28, format/common-nonformat/other-nonformat preservation is38.27/30.32/2.00%; theseIDclasses are not semantic granularity. Head64 preserves much more centeredenergy than random64, so same rankdoesnoteliminateenergyconfounding.

Fixed polygoncase: target-onlyL21preservespolygons40.60%, while all-prefixL21selectsthe and polygonsranks7. Fixed biologycase: originalthe19.55% remains top1atL28with80.77%,but actualhumansdrops2.6457%to0.01129%,rank6to117. Fixed Xraycase: same remains top1throughL21all-prefix while probabilitydrops70.04%to4.31%;L28changes toquote. Selected maximally preservedcase retains the all28layers but actualprime falls24.51%to0.01228%. These arepredictionchanges,notsemanticordering.

An implementation audit corrected inconsistent maximum ties in topk serialization vsargmax reference. Native probabilities/chunks remained unchanged; deterministic probability-descending/ID-ascending produces100%no-op preservation, zero changes tocategorymembership, and exact targeth/NLL replayvsR13atall737positions. First aggregates retainedINELIGIBLE; no extraGPUforward. Seeamendments.md.

## Hypotheses
No direction is presupposed. Same-rank random spaces, mean-only and scope controls distinguish descriptive effects, while energy, source and downstream compensation remain rivals. Common/other ID classes are not semantic granularity.

## Method
Single-layer all-prefix and independently replicated target-only interventions; frozen native norm/head and remaining network. Direct middle-layer head reading includes both raw and projected states, diagnostic only. Record full top1 probability/rank, actual successor NLL/probability/rank, KL(full||condition), native top10, centered energy and perturbation norms. Document means then equal-document aggregation;2000seed20261105 percentile bootstraps. Three random seeds are controls, not independent corpora. Fixed cases selected before new outcomes; outcome-selected examples labeled separately.

## Boundary
Exposed English windows, same narrow reference cohort and checkpoint. Equal rank is not matched energy. Early preservation could reflect sufficient retained signal or downstream compensation; standalone full information is not proven. No layer importance or semantic hierarchy judgment is promoted. Scientific acceptance/closure Unknown, no further experiment automatically authorized.
