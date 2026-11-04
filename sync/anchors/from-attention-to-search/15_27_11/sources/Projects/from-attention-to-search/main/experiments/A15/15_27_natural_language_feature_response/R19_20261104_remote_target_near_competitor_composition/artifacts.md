# Artifact and replay index

Canonical records: [Anchor](anchor.md),[Protocol](protocol.md),[Summary](summary.md),[Detailed](detailed.md),[numeric evidence](numeric_evidence.md),[literal cases](casebook_cn.md),[data guide](dataset_guide.md). English canonical; Chinese companions preserve the same evidence and pending states.

|Object|Actual location|Content|
|---|---|---|
|Full actual prefixes, token IDs, roles|/data/250010109/MoE_Router/experiments/20261104_near_far_object_fact_use/R02_feature_composition/data/panel_portable.jsonl|292literal rows; clean display metadata; frozen text/tokens unchanged|
|Frozen input|/data/250010109/MoE_Router/experiments/20261104_near_far_object_fact_use/R02_feature_composition/data/panel.jsonl|Original input retained; inherited suffix metadata audited|
|Clean pair table|/data/250010109/MoE_Router/experiments/20261104_near_far_object_fact_use/R02_feature_composition/data/text_pairing.csv|384paired comparisons and matching flags|
|Legacy mismatch audit|/data/250010109/MoE_Router/experiments/20261104_near_far_object_fact_use/R02_feature_composition/data/R18_comparison_audit.jsonl|48explicit old non-one-factor comparisons|
|Candidates and frequency|/data/250010109/MoE_Router/experiments/20261104_near_far_object_fact_use/R02_feature_composition/data|Both complete native reference tables/bins and discovery-only C/R/scales/joint directions|
|All raw candidate scores|/data/250010109/MoE_Router/experiments/20261104_near_far_object_fact_use/R02_feature_composition/results/behavior_smoke.jsonl;/data/250010109/MoE_Router/experiments/20261104_near_far_object_fact_use/R02_feature_composition/results/behavior_discovery.jsonl;/data/250010109/MoE_Router/experiments/20261104_near_far_object_fact_use/R02_feature_composition/results/behavior_heldout.jsonl|Every candidate token logp and full/item/period score|
|All native sparse activations and h|/data/250010109/MoE_Router/experiments/20261104_near_far_object_fact_use/R02_feature_composition/cache/discovery.npz;/data/250010109/MoE_Router/experiments/20261104_near_far_object_fact_use/R02_feature_composition/cache/heldout.npz|Top32IDs/values reconstruct30000post-TopK coordinates; actual1024hookinputs retained execution-side|
|All member lists|/data/250010109/MoE_Router/experiments/20261104_near_far_object_fact_use/R02_feature_composition/results/membership_pairs.jsonl|768site-specific pairs, exact shared/entered/exited IDs/values|
|Readable raw positives|/data/250010109/MoE_Router/experiments/20261104_near_far_object_fact_use/R02_feature_composition/tables/sparse_activations.csv|Every formal positive coordinate,reference group,token and position|
|Individual/member/geometry/frequency tables|/data/250010109/MoE_Router/experiments/20261104_near_far_object_fact_use/R02_feature_composition/tables|Every family,raw/relative fixed values,T/N/I,missingness,behaviors,frequency support,marginals,sensitivities|
|Full conditional-null statistic traces|/data/250010109/MoE_Router/experiments/20261104_near_far_object_fact_use/R02_feature_composition/cache/*_null.npz|Both splits/sites,4×64draws,all pool pairs,degree snapshots|
|Scoring and complete analysis|/data/250010109/MoE_Router/experiments/20261104_near_far_object_fact_use/R02_feature_composition/code|run.py;select.py;analyze.py;joint_heldout.py;supplement.py;offline_replay.py;all actual figure/report/package code|
|Provenance and checks|/data/250010109/MoE_Router/experiments/20261104_near_far_object_fact_use/R02_feature_composition/evidence|Freeze,strict assets,run incidents,old-byte protection,token/numeric/degree checks,figure review,package receipt|
|Figures|/data/250010109/MoE_Router/experiments/20261104_near_far_object_fact_use/R02_feature_composition/figures;./figures|Two independent site overviews,two literalF23panels,frequency groups,joint nulls|
|Conversation memory|/data/250010109/Research_System/.research/memory/conversations/1104-长短程依赖分析/memory.md|Append-only operational log; noncanonical|
|Small result packet|/data/250010109/Research_System/daily_research_reports/1104/20261104_R19_remote_target_competitor_composition.zip|Under20MB;raw sparse/text/score/null inputs,documents,code and fresh-extraction replay|

The packet omits pretrained weights/fullh/compiledlibrary; omitted_assets.jsonlists actual path,size,SHAand unsaved preactivations. No checkpoint was trained or modified. Full model/SAEconfiguration and source hashes are in config.json. R18is unchanged. No commit/push/external publication.
