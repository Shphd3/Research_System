# Normalized routing and frozen-base expert learning assets

[中文结果](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/crosscoder_feature_relations/activation_to_expert_learning/20261019_normalized_learning/summary_cn.md) · [Full record](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/crosscoder_feature_relations/activation_to_expert_learning/20261019_normalized_learning/detailed_cn.md) · [Protocol](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/crosscoder_feature_relations/activation_to_expert_learning/20261019_normalized_learning/protocol.md)

The sole payload root is `/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/normalized_route_learning/20261018T173143Z`. Base, dictionary and original output path are frozen; saved states contain the residual branch and optional learned router, not a standalone language model.

Twenty condition/seed families each enumerate actual epoch0/1/2/3 states. Final checkpoint full-file SHA256 was freshly computed; earlier milestone sizes/access were checked without full hashing. Each formal state saves optimizer, RNG, exact data orders/cursor and valid-position counters. Exact next-update recovery passed in a separate engineering Smoke; individual formal continuations were NOT RUN.

The independent target background excludes269 feature2 TRAIN positions, trains510steps/260886valid exposures, and is distinct from the main T_S1 model. The adaptation family has8expert copies,32steps/2048exposures each, with actual8/32/final states. Their full-file hashes were not computed; named files, sizes and producer/config identity are recorded. The Smoke replay state is an engineering artifact, not the100-step fitted endpoint. Mutable latest pointers are not selected milestone identities.

All20 main models completed768updates/392136exposures each. Learning results are negative against the frozen baseline in this setting; registration is not scientific approval, general pretraining capacity evidence, or phi-learning validation. Document independence remains Unknown.

Selected current output access: [24 IDs](checks/2026-10-19_normalized_learning_20261018T173143Z.json), not a whole-library check.

- `adapter_normalized_route_t_s0_seed11_20261018t173143z`
- `adapter_normalized_route_t_s0_seed22_20261018t173143z`
- `adapter_normalized_route_t_s1_seed11_20261018t173143z`
- `adapter_normalized_route_t_s1_seed22_20261018t173143z`
- `adapter_normalized_route_t_s2_seed11_20261018t173143z`
- `adapter_normalized_route_t_s2_seed22_20261018t173143z`
- `adapter_normalized_route_t_s3_seed11_20261018t173143z`
- `adapter_normalized_route_t_s3_seed22_20261018t173143z`
- `adapter_normalized_route_r11_s0_seed11_20261018t173143z`
- `adapter_normalized_route_r11_s0_seed22_20261018t173143z`
- `adapter_normalized_route_r11_s1_seed11_20261018t173143z`
- `adapter_normalized_route_r11_s1_seed22_20261018t173143z`
- `adapter_normalized_route_r11_s2_seed11_20261018t173143z`
- `adapter_normalized_route_r11_s2_seed22_20261018t173143z`
- `adapter_normalized_route_r11_s3_seed11_20261018t173143z`
- `adapter_normalized_route_r11_s3_seed22_20261018t173143z`
- `adapter_normalized_route_learned_seed11_20261018t173143z`
- `adapter_normalized_route_learned_seed22_20261018t173143z`
- `adapter_normalized_route_learnedlb_seed11_20261018t173143z`
- `adapter_normalized_route_learnedlb_seed22_20261018t173143z`
- `adapter_normalized_route_target_background_20261018t173143z`
- `adapter_normalized_route_target_adapt_family_20261018t173143z`
- `adapter_normalized_route_engineering_replay_20261018t173143z`
- `analysis_normalized_route_learning_20261018t173143z`
