# R11 A02: qualified three-domain input data

[中文](A02_qualified_data_cn.md) · [Execution amendment](../protocol_A02_execution.md)

The actual panel contains **450 new original document families**,150 per domain. The manifest and content labels were frozen before new activations were used for selection. The original topic,genre,publisher and source-split quotas passed without relaxation. Researcher scientific acceptance remains Unknown.

| Domain | Split | Families | Expository | QA | Measured positions |
|---|---|---:|---:|---:|---:|
| math | discovery | 60 | 45 | 15 | 9600 |
| math | development | 30 | 22 | 8 | 4800 |
| math | heldout | 60 | 45 | 15 | 9600 |
| biology | discovery | 60 | 45 | 15 | 9600 |
| biology | development | 30 | 22 | 8 | 4800 |
| biology | heldout | 60 | 45 | 15 | 9600 |
| physics | discovery | 60 | 45 | 15 | 9600 |
| physics | development | 30 | 22 | 8 | 4800 |
| physics | heldout | 60 | 45 | 15 | 9600 |

Each excerpt is192 real input tokens with no chat template or added BOS. Positions32–191 are measured,including zero activations. Each domain contributes60 discovery,30 development and60 heldout families. Heldout contains30 new families on familiar platforms and30 on platforms absent all discovery/development and old120documents. Each heldout stratum has at least4platforms;25% split/domain publisher caps and six-topic quotas pass. No selected platform appears in only one domain.

A separate,activation-blind AI reading pass reviewed1002candidate windows:730PASS,272REJECT. This is not claimed as human review. After original-family/near-duplicate exclusions and platform qualification,660candidate families entered the fixed-quota,hash-ranked selection;round05found the optimal450-document combination. Eight already-reviewed,disjoint D/V-platform pilots are excluded from all scientific sample counts. The first unreviewed450proposal had300PASS/150REJECT and was never run.

Independent articles,books/courses and question threads define families. DOI/article/figure aliases,Oxford publication IDs,Wikipedia mobile/mirror URLs and whole-course/book paths are consolidated;Springer,Nature,BMC andSpringerOpen share one platform family. Exact token windows and5-shingle Jaccard>=.8duplicates against old120,reference inputs and new study families are excluded. The saved review retains every exclusion and label correction.

The source frame combines pinned public DCLM raw text and publicly accessible scientific/reference/QA articles. It is a purposive quota sample;domains still differ in vocabulary,format,topic and publication period. Source holdouts test transfer across the sampled source strata;they do not isolate source as a causal factor or establish LM-pretraining non-contamination.

Original raw pages and all extraction versions stay execution-side. Table-of-contents/share controls were removed from named body selectors before taking a continuous192-token body-text window;math-image alt text in the Tao source is original source text. Final excerpts,IDs,offsets,source hashes,labels and split metadata are saved.

Dataset asset:`data_a15_27_r11_qualified_three_domain_A02_20261030`. Manifest SHA256:`c7d6abb9ad79ca2e732cdeeb3966812ffac4d4f90d54e7a11dc2757092f781c2`.

[Manifest](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R11_three_domain_replication_20261030/qualified_three_domain_A02/data/manifest.json) · [All450documents](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R11_three_domain_replication_20261030/qualified_three_domain_A02/data/documents.jsonl) · [Qualification audit](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R11_three_domain_replication_20261030/qualified_three_domain_A02/data/qualification_audit.json) · [All review decisions](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R11_three_domain_replication_20261030/qualified_three_domain_A02/review/decisions.jsonl) · [Final input candidates](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R11_three_domain_replication_20261030/qualified_three_domain_A02/selection/round05/eligible_candidates.jsonl).

Selected source asset IDs:

- `data_a15_27_r11_byjus_clean_sources_A02_20261030`
- `data_a15_27_r11_livescience_clean_sources_A02_20261030`
- `data_a15_27_r11_quanta_sources_A02_20261030`
- `data_a15_27_r11_quanta_supplement_A02_20261030`
- `data_a15_27_r11_raw_supplement_A02_20261030`
- `data_a15_27_r11_sciencedaily_sources_A02_20261030`
- `data_a15_27_r11_terrytao_sources_A02_20261030`
- `data_a15_27_r11_web_qa_A02_20261030`
- `dclm_raw_holdout_global02`

Some selected windows retain titles,contents lists or navigation residue as actually input. No response-dependent cleaning was done;format and source-style rivals remain.
