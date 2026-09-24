# Approved table cleanup, 2026-09-24

Four previously approved redundant CSV copies were removed after their byte-for-byte SHA-256 matches to retained sources were checked. Total removed: **39,399,183 bytes (37.57 MiB)**. The source tables, aggregate decision tables, Protocols, Summaries, and Detailed records remain.

| Removed copy | Bytes | Share of removed bytes | Retained source and SHA-256 |
|---|---:|---:|---|
| `Projects/from-attention-to-search/main/experiments/A06/06_02_partition_preservation_dynamics/A06_02_01_E07_top1_margin_threshold/tables/margin_budget_by_pair.csv` | 18,711,034 | 47.49% | `Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/results/a06_23_top1_lockin_margin_threshold/a06_23_top1_lockin_full_20260701_1/tables/margin_budget_by_pair.csv` · `5ed249c11f2d28060125291ccfc3cd89593b35b4a02f59c2b7dac5719146e571` |
| `Projects/from-attention-to-search/main/experiments/A06/06_02_partition_preservation_dynamics/A06_02_01_E06_margin_budget_audit/tables/margin_budget_by_pair.csv` | 12,271,749 | 31.15% | `Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/results/a06_21_margin_budget_preservation_audit/a06_21_margin_budget_full_20260629_1/tables/margin_budget_by_pair.csv` · `44f3b496bc1abbf55a9ec2616f24ea5b77161226529a03029a7b18d79ee88ecd` |
| `daily_research_reports/backup/2026/08/0807/docs/qwen3_post_o_proj_full_attention_semantic_variance_atlas/tables/eigenvalue_spectrum.csv` | 7,407,936 | 18.80% | `Projects/from-attention-to-search/main/experiments/A15/15_02_layerwise_representation_spectral_atlas/A15_02_E04_qwen3_post_o_proj_semantic_atlas/tables/eigenvalue_spectrum.csv` · `facc4f7af4111e537144be54ac04ff700d875d869e6bbb4e479752ecf00bd4da` |
| `daily_research_reports/backup/2026/06/0604/feature_key_routing_audit/A05_01_feature_axis_audit_existing_logs/tables/feature_expert_matrix_b_id.csv` | 1,008,464 | 2.56% | `Projects/from-attention-to-search/main/experiments/A05/A05_01_feature_axis_audit_existing_logs/tables/feature_expert_matrix_b_id.csv` · `c56cc2e0aaa7ae701da0ae462f1c6aa0178bb1e4c78c28ee93c3506dfae8b5bc` |

The historical plans still name the expected table outputs; their approved contracts were not rewritten. Current reading surfaces point to the retained sources. No raw run, checkpoint, or unique result was removed.
