派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R10_domain_member_atlas_20261030/README.md`。
[精确原始文件](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R10_domain_member_atlas_20261030/README.md)；研究修改仍回到原件。

---

# R10 reproducibility and reading entry

[中文结果](summary_cn.md) · [English results](summary.md) · [Protocol](protocol.md) · [Detailed](detailed.md) · [Definitions](definitions.md)

[Near-single-domain real-token/context supplement](../../../../../../../../UNAVAILABLE.md) · [中文](../../../../../../../../UNAVAILABLE.md). It defines the separate55-member population, new script order, three main figures and annotation/coverage gaps. Historical parent scripts below retain the960-member object.

Use `/root/anaconda3/envs/spectral-hier/bin/python`. All operations are CPU cache statistics; no model is imported or called.

```bash
/root/anaconda3/envs/spectral-hier/bin/python /data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R10_domain_member_atlas_20261030/scripts/analyze.py --output /tmp/r10_reproduction_unique
/root/anaconda3/envs/spectral-hier/bin/python /data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R10_domain_member_atlas_20261030/scripts/refine_background.py --output /tmp/r10_reproduction_unique
/root/anaconda3/envs/spectral-hier/bin/python /data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R10_domain_member_atlas_20261030/scripts/render.py --output /tmp/r10_reproduction_unique
/root/anaconda3/envs/spectral-hier/bin/python /data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R10_domain_member_atlas_20261030/scripts/audit.py --output /tmp/r10_reproduction_unique
```

The first command writes an independent directory using the frozen R10 config and existing source caches. Default output is the canonical execution root, where an existing freeze is verified and preserved. All four analysis/render/audit scripts accept the same --output root; their default is `/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R10_domain_member_atlas_20261030`. Raw tables/matched IDs/position arrays remain there. Input registry access must be refreshed before cache use on another host. See provenance/input_access.json for this session. No checkpoint/dataset download, model forward or training occurs. Supplement B is NOT RUN.


[Proposed R11three-domain independent-data replication](../R11_three_domain_replication_20261030/README.md) · [中文](../R11_three_domain_replication_20261030/README_cn.md). Planning only,DRAFT_NOT_EXECUTABLE;R10results/forward counts remain unchanged.
