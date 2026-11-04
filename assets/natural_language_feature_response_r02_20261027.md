# R02: matched reference frequency, panel cache and analysis assets

[Summary](../Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R02_frequency_distance_integration/summary.md) · [Manifest](../Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R02_frequency_distance_integration/artifact_manifest.md) · [Strict access snapshot](checks/20261027_natural_language_feature_r02_outputs.json)

The official Qwen3-0.6B and native E16 FP32 Top32 SAE are reused. The [asset audit](../Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R02_frequency_distance_integration/asset_audit.md) records hashes, hook and computation. CrossCoder uses its own paired model/shared-z cache; its feature IDs are not E16 IDs.

Input IDs: `data_natural_language_feature_panel_r02_20261026` (12 scenarios,120 controlled sequences) and `data_e16_fp32_reference_windows_r02_20261026` (1024 fixed TRAIN windows). Output IDs: `reference_e16_fp32_dclm_r02_20261026` (245760 matching-precision positions and per-window counts), `representation_natural_language_feature_r02_20261026` (360 readouts; prefix numerical qualification FAIL), and `analysis_natural_language_feature_r02_20261026` (Q1/Q2/Q3 all INSUFFICIENT). The frequency estimate belongs to this finite window corpus; low support remains NA.

Payloads remain execution-side at `/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R02_frequency_distance_integration/`. Strict access passed for the three outputs; access does not confer scientific eligibility. R02 used1160 forwards; R01+R02 used1452/1500. No new training occurred.
