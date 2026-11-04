# R03同位置共激活：文本、参考缓存与分析资产

复用A22共享z的匹配模型、14层hook、TRAIN中心/RMS和保存阈值。不同字典坐标不能对应；各层解码贡献不是各层独立激活。模型/字典SHA与当前访问见[资产审计](../Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R03_same_token_coactivation/asset_audit_cn.md)。

| Asset ID | Actual content / boundary |
| --- | --- |
| `data_same_token_coactivation_panel_r03_20261027` | Frozen 12 scenarios / 72 controlled sequences; 36 measured and 36 NOT RUN. English constructed/edited language. |
| `reference_same_token_coactivation_r03_20261027` | Fixed 512 coordinates, 64 D + 64 V packed contexts; 65464 / 65484 eligible token positions, exact counts/moments. Original document/sentence identities unavailable. |
| `representation_crosscoder_context_r03_20261027` | 36 sequence caches, candidate readouts and native decoder geometry; 48 calls including 12 checks. Cache replay approximate within frozen tolerances; eight fixed-prefix checks pass. |
| `analysis_same_token_coactivation_r03_20261027` | Original O audit, R/C graphs, 199 exact-margin null draws with full reclustering, support, naming and context results. Frequency comparison remains NA; far response bounded. |

[Output strict-access snapshot](checks/20261027_same_token_coactivation_r03_outputs.json). Access does not establish scientific eligibility. [完整结论与限制](../Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R03_same_token_coactivation/summary_cn.md) · [可追溯清单](../Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R03_same_token_coactivation/artifact_manifest_cn.md).

Payload root: `/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R03_same_token_coactivation`. R03 uses 48 forwards; cumulative 1500/1500. Zero training steps and interventions. R01/R02 results and failures are unchanged.
