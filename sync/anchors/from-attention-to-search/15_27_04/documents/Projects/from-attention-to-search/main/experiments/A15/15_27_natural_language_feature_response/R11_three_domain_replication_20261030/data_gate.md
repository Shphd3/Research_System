派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R11_three_domain_replication_20261030/data_gate.md`。
[精确原始文件](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R11_three_domain_replication_20261030/data_gate.md)；研究修改仍回到原件。

---

# R11 data qualification: inventory complete,450-document manifest unqualified

[中文](data_gate_cn.md) · [Stage results](summary.md) · [Quota contract](../../../../../../../../UNAVAILABLE.md)

All59,812documents in the registered local DCLM raw archive were scanned. V1 yielded1,940candidate families;expanded source-only topic recall produced2,537v2families. Preserve both. Provisional v2labels are327math,1,890biology,and337physics and may overlap;these are not reviewed samples.

The proposal requires150documents/domain,25/topic,with60discovery/30development/60heldout. Heldout divides30same-platform new families and30new-platform families;the latter needs7QA documents and at least4platforms,with platforms covering at least2domains. Old120families,reference families,exact and near duplicates are excluded;source,family,and final split identities still require review.

Current provisional shortfalls versus25/topic:math discrete/logic14,analysis24;physics thermal/statistical16,materials/solid18. Physics has only2provisional QA candidates on new-source cross-domain platforms against7required. Pre-review counts may fall,and heuristic labels may miss relevant content;this does not prove universal absence. It means no quota-compliant450-document manifest has been established. The118platforms with provisional multi-domain candidates do not prove source balance.

M2D2fluid/optics train/valid/test archives are readable,but original document/paper family boundaries are not qualified. Lines cannot be treated as independent papers,and two physical subdomains cannot automatically satisfy6topics and platform holdout. One attempted public QA retrieval returned403;no usable corpus was obtained and no restriction was bypassed.

Producer:this round's`scripts/prepare_candidates.py`,original and`--broad`. Outputs live execution-side under`preparation/`and`preparation/broader_topic_inventory_v2/`,including configs,candidate text,line/URL/family/span provenance. `source_inventory_manifest.json`records actual files and hashes.

Dependent three-domain forwards/analyses remain NOT RUN;actual new forwards0. Cached spectral supplementation is complete independently. The next dependency is a reviewed450-document manifest meeting source,topic,and independent-split gates. Preserve the protocol;do not silently reduce quotas or substitute a different experiment.
