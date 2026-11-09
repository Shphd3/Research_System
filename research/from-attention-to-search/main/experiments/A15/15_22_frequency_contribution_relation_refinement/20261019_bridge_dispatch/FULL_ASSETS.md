# Complete source assets and interfaces

Canonical result: `/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_22_frequency_contribution_relation_refinement/20261019_bridge_dispatch`. Execution root: `/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/frequency_contribution_bridge/20261019T025630Z`.

- `config/frozen.json`: authorized settings; `config/train_frozen.json`: TRAIN-only boundaries, calibration means and selected IDs.
- `cache/train_profiles.npz`, `eval_profiles.npz`: per-position M/R/U and exact IDs/positions; `tables/*_position_profiles.csv`: complete readable position table.
- `cache/counts_{train,eval}_b{1..4}.npz`: exact within-band counts, feature IDs and denominators; `cache/linkage_b*.npy`: actual TRAIN hierarchy. Half reconstruction groups are in `cache/groups.npz`.
- `cache/groups.npz`: relation plus20 matched-random member maps; `cache/routes_*_*.npz`: all42 routes for both splits.
- `metrics/exposure_*.npz`: all84 count/q/r/load/owner matrices. Schema: featureID rows0..16383, expert columns0..7; expert frequency-band=ID//2+1; q/count semantics inDetailed; emptyq=NaN; r=NaNfor globally unseen split features.
- `tables/designated_low_feature_exposure.csv`: full low-feature designated-expert q/r/enrichment/gap; complete CSVs stay execution-side. `tables/dispatch_summary.csv` and other small tables are curated here.
- `texts/all_cases.jsonl`, `all_cases_cn.md`: all302 cards and explicit zero/insufficient notes,174 unique positions.
- `provenance/verification.json`: direct cached-event checks; `text_decoder.json`:3840 original-string comparisons. `dispatch_failure_01.json`, `text_failure_01.json` preserve recovered engineering failures.
- `code`: actual CPU-only analysis, verification, plotting and documentation. No external checkpoints or hidden/zcache copied intoResearch_System.

Source data/cache: `/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/sft_route_learning/20261019T012300Z`; immutable checkpoint/tokenizer and input asset IDs are inexecution_authorization_20261019.json and the asset catalog. Existing pairedDCLM/SFTTRAINplots and migration tables are reused, not regenerated from inference. No ZIP was created; the earlier large ZIP cleanup remains in force.
