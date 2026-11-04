派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R05_distance_attention_20261028/endpoint_composition_20261028/protocol.md`。
[精确原始文件](../../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R05_distance_attention_20261028/endpoint_composition_20261028/protocol.md)；研究修改仍回到原件。

---

# Offline protocol: R04 roles at R05 source endpoints

Authorized exploratory cache-only analysis. Complete active z>0 sets at past endpoints,not intersections. Original40heldout math/biology documents,originalR05head/query/pairs and R04role IDs. Common query-head support for near/far;equal positions/heads/queries/documents. 5000document bootstrap,19999two-sided symmetric signflips,96primary tests pooledBH. All finite effects observational. No new model calls/training/tasks/candidate selection.

Exact operational contract:

```json
{
  "kind": "EXPLORATORY_REANALYSIS_OF_EXISTING_CACHE",
  "authorization": "current user request explicitly authorizes all applicable offline statistics and four figures,no additional approval required",
  "new_forwards": 0,
  "training": 0,
  "task_creation": 0,
  "dictionaries": [
    "SAE",
    "CC"
  ],
  "domain_labels": [
    "math",
    "biology"
  ],
  "primary_split": "original40heldout,20/domain",
  "measured_object": "complete z>0 active feature set at the past/source endpoint,irrespective of query activation;not intersection",
  "source_attention": "R05block27all16heads,savedoriginalcausalprobabilities,andunchangedmatchedpairs;topceil(.1N)withinbin,middlefloor(.4N):ceil(.6N),sameIDstatus/sourcepunctuation,nearestwithoutreplacementcaliper8",
  "frequency_groups": "reuse exact R05 frequency_low/middle/high/low_support IDs,not refit;DCLMpositivehits>=20 before terciles",
  "role_groups": "unchanged R04shared32/math16/bio16;otherallremainingcoordinates,not no-domain-information",
  "primary_stratum": 0,
  "strata": [
    "different_tokenID_nonpunctuation",
    "same_tokenID_nonpunctuation",
    "different_tokenID_punctuation",
    "same_tokenID_punctuation"
  ],
  "comparison_support": "within each document and stratum,intersect valid(query_index,head)cells forbins0/4;retain samecell forbothhigh/control;queries/headswithnocellsremainmissing",
  "trend_support": "separate within-document/stratum allfive-bin commoncell intersection;report lost support;no substituting unconstrained trends",
  "averaging": "positionsequalwithinquery/head/bin/group;headsequalwithinquery;queriesequalwithindoc;docsequalwithindomain;no activity-weighted primary pooling",
  "primary_metrics": [
    "frequency_share_low",
    "frequency_share_middle",
    "frequency_share_high",
    "frequency_share_low_support",
    "role_member_hit_shared",
    "role_member_hit_math",
    "role_member_hit_bio",
    "active_count"
  ],
  "primary_contrasts": [
    "far_high-minus-near_high",
    "far_middle-minus-near_middle",
    "(far_high-minus-near_high)-(far_middle-minus-near_middle)"
  ],
  "statistic": {
    "bootstrap": 5000,
    "unit": "document within domain",
    "seed": 20261028,
    "CI": "pairedpercentile95%",
    "signflips": 19999,
    "test": "two-sided document sign flips about0,symmetry assumption,MonteCarlo plus1",
    "multiple_testing": "one BH over2dict*2domains*8metrics*3contrasts=96;missingp1;no besthead/distance/feature",
    "alpha": 0.05,
    "min_documents": 10,
    "interpretation": "exploratory associations;no preregistered new confirmation or causal inference"
  },
  "zero_activation": "zero active totals recorded;compositionandmeanpositiveintensityNA,not0;percoordinatehitcounts/rates0aredefined;reportdenominators",
  "secondary": "fullrolecounts/shares,othermemberhit,frequencycounts,zsum/activezmean/nativecontributionandcompositions,querysharingseparately;allstratawithCIs,nomoreprimarytests",
  "diagnostics": "docweightedactualattention/distance,pooledquantileswithpairdenominators,rawdata saved;tokenIDfrequencyinexistingDCLMwindows and character-shape classes:not linguistic POS;sourcehost/genreavailable",
  "sample_rule": "firstoriginalheldoutdocumentbyseq_id;firstquerypositionthenheadwithvalidnear/farpairsinprimarystratum;withinbinchoosefirstsorted(high,control). Nofeatureresponsesused. Showonlyquery-visibleprefix,fullpastendpointactivecoordinatesinappendix;fixedR04candidateorderplusfirstnumericIDs of source-onlyotherfeatures for illustration,not newcandidates",
  "feature_heatmap": "all64frozenR04coordinatesperdict,inoriginalshared/math/bioorder;8columns(domain*nearhigh/farhigh/nearmiddle/farmiddle);group-levelsamecommon2support;no rows selected bycurrentheldout",
  "boundaries": [
    "sourceendpointsetsnotinformationcontent",
    "sharedrolemeanssharedmathbiologyonly",
    "jointCCznotlastlayerlocal",
    "nativeSAE/CCdifferenthooksnotqualityranking",
    "notransmissioncausality",
    "notlongshortexclusive",
    "noR06candidateimport"
  ]
}
```
