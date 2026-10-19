# October 18 actual-dispatch audit: offline discussion package

This package contains completed project records for discussion with the director agent and researcher. **The bounded recommendation is to define and calibrate the score first.** Replacement-score validity, global grouping feasibility, and learning benefit remain unknown. This derived reading copy neither replaces canonical project records nor authorizes new execution, training, or design changes. [中文入口](README_cn.md).

Start with the [Chinese director handoff](director_agent_handoff_cn.md) and [Summary](summary.md); consult [Detailed](detailed.md), the [four-figure guide](figures.md), and [twelve Chinese text cards](text_cases_cn.md) for evidence.

## Included reading material

- User [Anchor](design/anchor.md) / [Chinese original](design/anchor_cn.md), and [Protocol](protocol.md) / [Chinese original](protocol_cn.md).
- [Summary](summary.md) / [Chinese](summary_cn.md), [Detailed](detailed.md) / [Chinese](detailed_cn.md), and the [Chinese analysis entry](analysis_cn.md).
- Four figures, each in PNG, SVG, and PDF, under `figures/`; accompanying selected tables under `tables/`.
- [Reasoning audit](reasoning_audit_cn.md), [source bindings](source_bindings_cn.md), and [one next decision](next_decision.md) / [Chinese](next_decision_cn.md).
- [Recent six-stage index](recent_results/20261018_routing_progress.md) / [Chinese](recent_results/20261018_routing_progress_cn.md). Earlier source reports are not all bundled; their absolute paths are external provenance links.

Selected complete final-result tables are included specifically for offline inspection: [original per-feature owner metrics](tables/feature_owner_summary.csv), [original versus C-zero owner metrics](tables/feature_owner_original_and_C_zero.csv), [expert loads](tables/expert_loads_original_and_C_zero.csv), and [winner–runner margin decomposition](tables/winner_runner_margin_components.csv). The [same-feature paired results](tables/paired_feature_summary.csv) are also included. The existing small tables include [group summaries](tables/group_summary.csv), [winner–A0 margins](tables/winner_vs_A0_margin_components.csv), [case/common plotting data](tables/case_common_plot_source.csv), [text-case scores](tables/text_case_scores.csv), and [fixed conflict pairs](tables/conflict_pairs.csv). Winner–runner and winner–A0 margins compare different objects.

The [machine-readable cards with full visible prefixes](text_cases.json), [core receipt](provenance/core_receipt.json), [score receipt](provenance/score_receipt.json), [case receipt](provenance/cases_receipt.json), [execution bindings](provenance/execution_binding.json), and [design freeze](provenance/design_freeze.json) are included for offline inspection. Paths inside JSON retain their original provenance meaning.

## Sources and exclusions

Canonical reports, figures, and small tables originate from `/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/crosscoder_feature_relations/feature_group_to_actual_dispatch/20261018_routing_audit/`. The Anchor comes from the same project's `main/problem_anchors/crosscoder_feature_relations/feature_group_to_actual_dispatch/`; recent indexes come from `main/research_notes/qwen3_crosscoder_tooling/`.

The four additional complete final-result tables were copied only into this discussion package, not back into the project. They originate in `metrics/core/` or `metrics/score/` under execution root `/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/frequency_interval_moe/20261018T103820Z/routing_audit_20261018T143950Z/`.

Excluded: hidden/z caches, models and checkpoints, the complete feature×expert long table, the approximately 927k-row-per-split companion gzip tables, NPZ matrices, and full raw logs. Original bins are excluded; only twelve selected text cards are present.

Current reports, design, figures, and selected tables use package-relative links. Absolute links to historical reports, execution receipts, and source data identify **external provenance**. Their offline absence does not block reading the present results, but this package cannot independently rerun cache statistics. Only reading-copy links were adapted; definitions and results were preserved. The [payload manifest](payload_manifest.json) records sources and hashes.

The [frozen original grouping metadata](provenance/parent_grouping.json) contains exact boundaries, memberships, low/high lists and scoring/tie definitions. It is a provenance JSON snapshot, not an activation cache or a new grouping.
