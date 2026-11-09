# Selected evidence manifest

Actual analysis asset: `analysis_a17_r06_adam_swap_20261026`. [English result](summary.md), [中文一页](one_page_cn.md), [full appendix](appendix_cn.md). Execution owner: `/data/250010109/MoE_Router/experiments/20261025_a17_functional_protection/analysis/adam_swap_20261026`.

- Frozen inputs and all sample IDs: `reproduce/plan.json`; original pre-result file identities: `reproduce/freeze.json`. The frozen Anchor lives at `/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/17_shared_and_interference_learning/17_04_conditional_mapping_transfer/rounds/R06_functional_protection_20261025/adam_swap_20261026`; it is not rewritten after results.
- Actual worker and reused sources/config: `reproduce/adam_swap_20261026.py`, `engine.py`, `retention_r05_v1.py`, `local_dynamics_20261026.py`, `entry.py`, `frozen.json`. CPU analysis: `analyze_adam_swap_20261026.py`.
- Required all-seed/all-batch measurements: `tables/candidate_DEV_effects_72.csv`, `candidate_geometry_36.csv`, `four_cells_by_seed_batch_9.csv`, `paired_effects_and_interactions_90.csv`.
- Native replay: `tables/native_firstbatch_replay.csv`, `reproduce/native_replay_gate.json`; all24checks pass. Numerical noise: `baseline_noop_noise_12.csv`. Named-moment reconstruction and donor hashes: `reproduce/named_mapping_and_inputs.json`.
- Immutability: `reproduce/original_assets_immutable.json`;6checkpoint SHA256 before/after equal, original contracts and non-target model parameters unchanged. No candidate checkpoint exists.
- Receipt and forward count: `reproduce/receipt.json`, `sequence_calls.json`;10320/12000. Current required inputs and output read-access checks: `input_access.json`, `output_access.json`; load/hash/replay evidence is separate.
- One figure: SVG/PDF editable vectors and320dpiPNG, with data/aggregation identity in `figure_provenance.json`.

Selected evidence exception: small derived group/geometry/contrast/noise/replay CSVs and one result figure are intentionally tracked with SHA256 in `artifact_manifest.json`. Full4608per-item readouts remain execution-side at `/data/250010109/MoE_Router/experiments/20261025_a17_functional_protection/analysis/adam_swap_20261026/tables/per_item_DEV_effects_4608.csv`; included only in execution ZIP as `execution_evidence/`, not mainline Git. No model weights, cached activations, full raw logs or fonts are copied into the repository.

Scientific acceptance and parent-question closure remain Unknown. Execution and factual report complete. No commit, push or publication performed in this round.
