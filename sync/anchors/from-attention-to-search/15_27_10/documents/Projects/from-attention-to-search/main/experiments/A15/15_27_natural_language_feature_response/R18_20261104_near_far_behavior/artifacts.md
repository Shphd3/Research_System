派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R18_20261104_near_far_behavior/artifacts.md`。
[精确原始文件](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R18_20261104_near_far_behavior/artifacts.md)；研究修改仍回到原件。

---

# Actual artifacts

Canonical owner: /data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R18_20261104_near_far_behavior; sole[Anchor](../../../../../../../../UNAVAILABLE.md) with[Chinese companion](../../../../../../../../UNAVAILABLE.md),[Protocol](protocol.md),[中文](protocol_cn.md),[Summary](summary.md),[中文](summary_cn.md),[Detailed](detailed.md),[中文](detailed_cn.md).

| Artifact | Actual absolute location | Role |
|---|---|---|
| Full actual text/token IDs/offsets/candidates | /data/250010109/MoE_Router/experiments/20261104_near_far_object_fact_use/R01_behavior/data/panel.jsonl |444prefixes, exact evidence/target/gap |
| Families/splits | /data/250010109/MoE_Router/experiments/20261104_near_far_object_fact_use/R01_behavior/data/families.json |28families, smoke vs heldout |
| Templates/filler | /data/250010109/MoE_Router/experiments/20261104_near_far_object_fact_use/R01_behavior/data/templates.json |all literal construction rules |
| Raw complete scores | /data/250010109/MoE_Router/experiments/20261104_near_far_object_fact_use/R01_behavior/results/smoke.jsonl; /data/250010109/MoE_Router/experiments/20261104_near_far_object_fact_use/R01_behavior/results/heldout.jsonl |all candidate token/sum scores |
| Per-token flat table | /data/250010109/MoE_Router/experiments/20261104_near_far_object_fact_use/R01_behavior/tables/token_scores.csv |auditable scoring |
| All paired families | /data/250010109/MoE_Router/experiments/20261104_near_far_object_fact_use/R01_behavior/tables/family_pairs.csv |both directions separately |
| Distance/controls/intervals | /data/250010109/MoE_Router/experiments/20261104_near_far_object_fact_use/R01_behavior/tables/distance_summary.csv |registered operational gate |
| No-fact baseline | /data/250010109/MoE_Router/experiments/20261104_near_far_object_fact_use/R01_behavior/tables/baseline.csv |all candidate priors |
| All complete original pairs | /data/250010109/MoE_Router/experiments/20261104_near_far_object_fact_use/R01_behavior/results/casebook_all_cn.md |180paired cases |
| Scoring | /data/250010109/MoE_Router/experiments/20261104_near_far_object_fact_use/R01_behavior/code/run.py |native complete candidate chain |
| Construction/analysis/replay | /data/250010109/MoE_Router/experiments/20261104_near_far_object_fact_use/R01_behavior/code |prepare.py,analyze.py,verify.py,report.py |
| Frozen config | /data/250010109/MoE_Router/experiments/20261104_near_far_object_fact_use/R01_behavior/config.json |model,hashes,seed,precision,shape |
| Freeze and numerical checks | /data/250010109/MoE_Router/experiments/20261104_near_far_object_fact_use/R01_behavior/evidence |freeze,smoke,heldout,verification |
| Figure | /data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R18_20261104_near_far_behavior/figures/distance_switch.png |actual gap vs family rate and all family outcomes |
| Conversation memory | /data/250010109/Research_System/.research/memory/conversations/1104-长短程依赖分析/memory.md |append-only operational context |

No model/SAE weights, full output distributions or hidden representations copied. Execution raw outputs stay execution-side. Selected small tables/figure are project evidence copies with a payload manifest. Scripts mirror actual executed source; the scientific owner remains the project. No commit,push or external publication.
