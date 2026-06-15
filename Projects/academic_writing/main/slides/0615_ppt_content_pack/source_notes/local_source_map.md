# Local Source Map

This file records where the slide claims and figures came from. It is for checking and later paper/poster writing, not for direct presentation.

## Main Research Documents

- `daily_research_reports/0601/meeting/meeting_brief.md`  
  Initial 2x2 top-1 router lock-in framing: early routing geometry can be amplified by training.

- `daily_research_reports/0605/feature_assumption_relaxation_05_02/meeting_brief.md`  
  P1/P3 assumption-relaxation results: target prediction succeeds, but ordinary top-1 routing does not robustly produce meaningful feature-level specialization.

- `daily_research_reports/0607/uniform_collapse_audit/meeting_brief_cn.md`  
  Uniform feature collapse audit: common direction is not frequency imbalance; hidden common direction can create early routing bias.

- `daily_research_reports/0608/meeting_brief.md`  
  Common-offset model and position/source ablation: fixed routed position is a major source, but offset control is not sufficient.

- `daily_research_reports/0610/meeting_brief.md`  
  Minimal no-position dot-product setup: common-logit timing, cancellation intervention, and basin interpretation.

- `daily_research_reports/0611/real_text_common_logit_audit/summary.md`  
  Real DCLM audit: step-0 common margin is not dominant, but common centering reduces load and early training amplifies concentration.

- `daily_research_reports/0614/meeting/experiments/A06_02_01_cross_checkpoint_replay/summary.md`  
  Replay evidence: step-10 common-margin spike is not gate-weight-only; hidden drift and interaction matter.

- `daily_research_reports/0614/meeting/experiments/A06_02_02_freeze_split_common_stability/summary.md`  
  Freeze split: raw concentration can survive fixed gate/expert freezing; full common-margin spike requires hidden-producing path and gate-hidden interaction.

- `daily_research_reports/0614/draft/06_01_Common-Filtered Expert-Spectrum Router Initialization.md`  
  Next mechanism hypothesis: common-filtered expert-spectrum router initialization.

- `daily_research_reports/0615/sync_common_filtered_expert_spectrum/summary.md`  
  Latest A06_01 result: common-filtered expert-spectrum linear initialization improves step-0 balance but fails to reduce step-10 common-margin amplification or top-1 load concentration.

- `daily_research_reports/0615/next/decision1.md`  
  Next diagnostic decision: test whether the initially common-aligned router winner is directly amplified by early router updates.

## Copied Figures

| Pack figure | Original source |
|---|---|
| `figures/s04_baseline_collapse_heatmaps.png` | `Projects/from-attention-to-search/main/experiments/A05_04_01_round1_slot_specialization_protocol_dot_product/figures/round1_slot_specialization_dot_product_4gpu_20260609/p1_route_heatmaps.png` |
| `figures/s05_slot_init_positive_control_heatmaps.png` | `Projects/from-attention-to-search/main/experiments/A05_04_01_round1_slot_specialization_protocol/figures/round1_slot_specialization_4gpu_20260609/route_heatmaps/P5_slot_centroid_init_final_route_heatmaps.png` |
| `figures/s05_oracle_release_trajectory.png` | `Projects/from-attention-to-search/main/experiments/A05_04_01_oracle_to_trainable_release/figures/a05_05_oracle_to_trainable_release_4gpu_20260609/release_trajectory_by_seed.png` |
| `figures/s07_common_vs_slot_margin_timing.png` | `Projects/from-attention-to-search/main/experiments/A05_04_02_round2_dotproduct_common_logit/figures/round2_dotproduct_common_logit_4gpu_20260609/r2_p1_common_slot_margin_trajectory.png` |
| `figures/s07_common_cancellation_metrics.png` | `Projects/from-attention-to-search/main/experiments/A05_04_02_round2_dotproduct_common_logit/figures/round2_dotproduct_common_logit_4gpu_20260609/r2_p3_baseline_vs_cancel.png` |
| `figures/s09_realtext_step0_common_vs_residual.png` | `daily_research_reports/0611/real_text_common_logit_audit/figures/phase1_common_vs_residual_margin.png` |
| `figures/s09_realtext_raw_vs_centered_load.png` | `daily_research_reports/0611/real_text_common_logit_audit/figures/phase1_raw_vs_centered_load.png` |
| `figures/s10_realtext_early_load_amplification.png` | `daily_research_reports/0611/real_text_common_logit_audit/figures/phase3_max_load_over_steps.png` |
| `figures/s10_normal_max_load_trajectory.png` | `daily_research_reports/0614/meeting/experiments/A06_02_02_freeze_split_common_stability/figures/trajectory_max_load_normal.png` |
| `figures/s11_replay_heatmap_common_margin.png` | `daily_research_reports/0614/meeting/experiments/A06_02_01_cross_checkpoint_replay/figures/replay_heatmap_common_margin.png` |
| `figures/s12_0615_step10_common_margin_by_variant.png` | `daily_research_reports/0615/sync_common_filtered_expert_spectrum/figures/step10_common_margin_by_variant.png` |
| `figures/s12_0615_step10_raw_max_load_by_variant.png` | `daily_research_reports/0615/sync_common_filtered_expert_spectrum/figures/step10_raw_max_load_by_variant.png` |
| `figures/s12_0615_replay_A_interaction_by_variant.png` | `daily_research_reports/0615/sync_common_filtered_expert_spectrum/figures/replay_A_interaction_by_variant.png` |

## Generated Figures

Generated by `generate_diagrams.py`:

- `figures/s02_background_gap_diagram.png`
- `figures/s03_storyline_ladder.png`
- `figures/s06_common_logit_model.png`
- `figures/s08_position_source_simplified.png`
- `figures/s11_freeze_split_key_numbers.png`
- `figures/s12_next_mechanism_hypothesis.png`
- `figures/s12_0615_spectrum_init_stress_test.png`

The simplified generated figures are derived from numeric claims in the listed summaries and meeting briefs. They are presentation aids, not new experimental outputs.
