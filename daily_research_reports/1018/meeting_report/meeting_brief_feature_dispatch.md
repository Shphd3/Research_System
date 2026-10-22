# Discussion brief: listed features versus actual expert dispatch

[Full Chinese discussion brief](meeting_brief_feature_dispatch_cn.md) · [Canonical Summary](../../../Projects/from-attention-to-search/main/experiments/A15/15_19_feature_group_to_actual_dispatch/20261018_routing_audit/summary.md) · [Detailed record](../../../Projects/from-attention-to-search/main/experiments/A15/15_19_feature_group_to_actual_dispatch/20261018_routing_audit/detailed.md) · [Recent-results index](/data/250010109/Research_System/Projects/from-attention-to-search/main/research_notes/qwen3_crosscoder_tooling/20261018_routing_progress.md)

The current evidence favors clarifying and calibrating the scoring rule before prioritizing regrouping. This is an AI recommendation for discussion, not researcher approval or evidence of learning benefit.

The finite CPU-only diagnostic reused frozen cached features, A's original linear-frequency groups and both existing size-matched random groupings. A's 964 low-frequency features had zero assigned-expert reception in TRAIN and EVAL. B1/B2 EVAL feature-macro reception was 4.44%/10.30%; this does not establish better learning. Empty expert conditional frequencies remain NA.

The original score decomposition identifies why low-frequency hits lose the competition. In TRAIN positions containing a low-frequency feature, winner minus A0 averaged 0.567492; C terms contributed +0.569428 and non-C terms −0.001935. C is the original 962-member TRAIN high-frequency list, not a semantic class. Zeroing C scoring terms sends everything to A0 because groups 1–7 contain only C members. It empties seven experts and removes previously positive owner reception for 25 other features; this is a degenerate diagnostic, not a proposed router.

The 27 TRAIN-fixed, case-based cross-owner pairs produce necessary joint-coverage bounds. A's selected bounds are 0.991806–0.996134 in TRAIN and 0.988368–0.997178 in EVAL: they do not force zero reception, nor establish global feasibility. Three fixed feature IDs each have three random and one high-activation EVAL card; no examples were selected for semantic appearance.

The [full brief](meeting_brief_feature_dispatch_cn.md) presents all four figures, a six-stage results table, exact source links and discussion questions. Figure copies and origins are in [SOURCES](../figures/SOURCES.md). Recent records distinguish the older four-expert/rank-32 nine-run learning comparison from the new eight-FFN parent smoke, whose formal learning comparison remains NOT RUN. Graph hierarchy, decoder-layer distributions, phi communities, dispatch and learning are separate measurements.

The sole next proposed direction is a prespecified score calibration comparison with fixed groups, explicit per-feature reception goals and costs to other targets. No calibration, regrouping, inference or training was performed in this diagnostic; it stops here.
