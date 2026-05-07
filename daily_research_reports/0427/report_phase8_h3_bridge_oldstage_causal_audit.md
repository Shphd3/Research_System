# Phase8-H3 Bridge Old-Stage Causal Audit 中文报告

## 1. Objective and protocol mismatch being resolved

本实验桥接 Phase8p* 与 H3 causal audit 的协议差异：Phase8p* 先进行 old-stage，再进行 new-stage adaptation；H3 直接从初始 replacement block 适配 new-domain support。本轮把 H3-style controls 放回 old-stage continual-learning / CL 协议下，检查 Phase8 信号是否仍能排除 matched dense、raw two-branch、random split、head16 等替代解释。

这不是 full hierarchical MoE 实验；Stage B routing 只有在 Stage A 通过后才应运行。

## 2. Definitions

- `Pretrained LM`：在本实验前已经完成大规模文本预训练且保持冻结的 base language model。
- `Replacement block`：插入第 8 层 MLP 位置、在本实验中可训练的模块。
- `Old-stage`：第一阶段，只用 old-domain data 训练 replacement block，使其形成 old-task state。
- `New-stage`：第二阶段，从 old-stage checkpoint 出发，用 new-domain support data 适配。
- `Forgetting`：new-stage 后 old-domain loss 相对 old-stage checkpoint 的增加量。
- `New-task learning gain`：new-stage 后 new-domain query loss 相对 new-stage 前的下降量。
- `Variance band`：按 PCA/SVD variance rank 选择的 hidden-state subspace。
- `Random split`：维度与目标 variance band 匹配的 random subspace。
- `Branch functional specialization`：non-routed two-branch model 中某个 branch 对特定 token-frequency bucket 或 domain 的贡献更大。
- `Expert specialization`：routed model 中被选择的 expert 相比 counterfactual alternatives 有更低 next-token prediction loss。
- `Routing advantage`：在 matched parameter budget 下，learned routing 超过 non-routing split 与 uniform expert mixture。

## 3. Calibration projector

- base model：`Qwen3-0.6B`
- layer：`8`
- hook point：`post_attention_layernorm`
- 共享 Phase8p1 calibration artifact：同一个 mean vector `mu` 与 PCA/SVD directions `V`。
- `head16 = V_{1:16}V_{1:16}^T(x-mu)`；`u50 = P_{17:207}(x-mu)`；`ext = P_{782:r}(x-mu)`；`u50_ext = u50 + 0.25 * ext`；`full_tail_resid` 是移除 `head16` 后的 residual representation。
- normalized variants 对 projected hidden representation 做 LayerNorm，用于检查 projected-input scale 是否导致 underfitting。

## 4. WoS old/new episode construction

- old domains：`CS, Civil, MAE, Medical, Psychology`
- new domains：`ECE, biochemistry`
- WoS old eval chunks：`120`；本次实际评估限制：`full`
- DCLM eval chunks：`128`；本次实际评估限制：`full`
- episodes per seed：`20`；本次实际运行 episodes：`20`
- 每个 episode 使用 `1` 个 new-domain support chunk 和 `16` 个 new-domain query chunks。
- stress support chunks per episode：`1`。

## 5. Old-stage training and checkpoint matching

- old-stage train steps：`500`
- old-stage learning rate：`0.0002`
- old-stage comparable tolerance：`0.1`
- 当前 runner 使用固定 old-stage step checkpoint；报告 `G_old_stage` 与 post-old-stage old loss range，用于判断是否需要 matched-old-loss analysis。

## 6. New-stage adaptation protocol

- new-stage horizon：`U=8`
- lr multipliers：`0.5`；formal gate 只使用 `0.5x`。
- seeds：`20260418,20260419,20260420`
- random projection seeds：`0,1,2`。
- `G0_ER_matched_dense_replay` 在 new-stage adaptation 中加入 old replay item，old replay token count 与 new support token count 匹配。

## 7. Model groups and parameter counts

| group | label | lr_multiplier | random_projection_seed | trainable_params | old_stage_trainable_params | adaptation_stage_trainable_params | G_old_stage | old_stage_post_old_loss | learning_rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| G0_ER_matched_dense_replay | matched_dense_replay | 0.500000 | -1 | 9437184 | 9437184 | 9437184 | 0.125881 | 3.171384 | 0.000050 |
| G0_matched_dense | matched_dense_baseline | 0.500000 | -1 | 9437184 | 9437184 | 9437184 | 0.125881 | 3.171384 | 0.000050 |
| G1_raw_two_branch | raw_two_branch_control | 0.500000 | -1 | 9437184 | 9437184 | 9437184 | 0.138183 | 3.159001 | 0.000050 |
| G2_random_split | random_projection_split | 0.500000 | 0 | 9437184 | 9437184 | 9437184 | 0.156800 | 3.140576 | 0.000050 |
| G2_random_split | random_projection_split | 0.500000 | 1 | 9437184 | 9437184 | 9437184 | 0.156832 | 3.140632 | 0.000050 |
| G2_random_split | random_projection_split | 0.500000 | 2 | 9437184 | 9437184 | 9437184 | 0.156894 | 3.140433 | 0.000050 |
| G3_head16_split | head16_split | 0.500000 | -1 | 9437184 | 9437184 | 9437184 | 0.131462 | 3.165830 | 0.000050 |
| G0_ER_matched_dense_replay | matched_dense_replay | 0.500000 | -1 | 9437184 | 9437184 | 9437184 | 0.125872 | 3.171393 | 0.000050 |
| G0_matched_dense | matched_dense_baseline | 0.500000 | -1 | 9437184 | 9437184 | 9437184 | 0.125872 | 3.171393 | 0.000050 |
| G1_raw_two_branch | raw_two_branch_control | 0.500000 | -1 | 9437184 | 9437184 | 9437184 | 0.137928 | 3.159450 | 0.000050 |
| G2_random_split | random_projection_split | 0.500000 | 0 | 9437184 | 9437184 | 9437184 | 0.157290 | 3.139845 | 0.000050 |
| G2_random_split | random_projection_split | 0.500000 | 1 | 9437184 | 9437184 | 9437184 | 0.156990 | 3.140545 | 0.000050 |
| G2_random_split | random_projection_split | 0.500000 | 2 | 9437184 | 9437184 | 9437184 | 0.158117 | 3.139133 | 0.000050 |
| G3_head16_split | head16_split | 0.500000 | -1 | 9437184 | 9437184 | 9437184 | 0.132588 | 3.164729 | 0.000050 |
| G0_ER_matched_dense_replay | matched_dense_replay | 0.500000 | -1 | 9437184 | 9437184 | 9437184 | 0.126311 | 3.170954 | 0.000050 |
| G0_matched_dense | matched_dense_baseline | 0.500000 | -1 | 9437184 | 9437184 | 9437184 | 0.126311 | 3.170954 | 0.000050 |
| G1_raw_two_branch | raw_two_branch_control | 0.500000 | -1 | 9437184 | 9437184 | 9437184 | 0.137550 | 3.159894 | 0.000050 |
| G2_random_split | random_projection_split | 0.500000 | 0 | 9437184 | 9437184 | 9437184 | 0.156682 | 3.140656 | 0.000050 |
| G2_random_split | random_projection_split | 0.500000 | 1 | 9437184 | 9437184 | 9437184 | 0.157847 | 3.139526 | 0.000050 |
| G2_random_split | random_projection_split | 0.500000 | 2 | 9437184 | 9437184 | 9437184 | 0.157133 | 3.140222 | 0.000050 |
| G3_head16_split | head16_split | 0.500000 | -1 | 9437184 | 9437184 | 9437184 | 0.134507 | 3.162493 | 0.000050 |
| G4_u50_split | u50_middle_band_split | 0.500000 | -1 | 9437184 | 9437184 | 9437184 | 0.160266 | 3.136990 | 0.000050 |
| G5_ext_split | extreme_low_variance_split | 0.500000 | -1 | 9437184 | 9437184 | 9437184 | 0.107609 | 3.189428 | 0.000050 |
| G6_norm_u50_ext_split | normalized_u50_ext_functional_span_split | 0.500000 | -1 | 9437184 | 9437184 | 9437184 | 0.158340 | 3.138893 | 0.000050 |
| G6_u50_ext_split | u50_ext_functional_span_split | 0.500000 | -1 | 9437184 | 9437184 | 9437184 | 0.160101 | 3.137085 | 0.000050 |
| G7_full_tail_resid_split | full_tail_residual_split | 0.500000 | -1 | 9437184 | 9437184 | 9437184 | 0.159498 | 3.137827 | 0.000050 |
| G7_norm_full_tail_resid_split | normalized_full_tail_residual_split | 0.500000 | -1 | 9437184 | 9437184 | 9437184 | 0.163138 | 3.134456 | 0.000050 |
| G4_u50_split | u50_middle_band_split | 0.500000 | -1 | 9437184 | 9437184 | 9437184 | 0.159720 | 3.137546 | 0.000050 |
| G5_ext_split | extreme_low_variance_split | 0.500000 | -1 | 9437184 | 9437184 | 9437184 | 0.107710 | 3.189574 | 0.000050 |
| G6_norm_u50_ext_split | normalized_u50_ext_functional_span_split | 0.500000 | -1 | 9437184 | 9437184 | 9437184 | 0.158799 | 3.138527 | 0.000050 |
| G6_u50_ext_split | u50_ext_functional_span_split | 0.500000 | -1 | 9437184 | 9437184 | 9437184 | 0.159610 | 3.137705 | 0.000050 |
| G7_full_tail_resid_split | full_tail_residual_split | 0.500000 | -1 | 9437184 | 9437184 | 9437184 | 0.159931 | 3.137627 | 0.000050 |
| G7_norm_full_tail_resid_split | normalized_full_tail_residual_split | 0.500000 | -1 | 9437184 | 9437184 | 9437184 | 0.162950 | 3.134339 | 0.000050 |
| G4_u50_split | u50_middle_band_split | 0.500000 | -1 | 9437184 | 9437184 | 9437184 | 0.159113 | 3.138072 | 0.000050 |
| G5_ext_split | extreme_low_variance_split | 0.500000 | -1 | 9437184 | 9437184 | 9437184 | 0.107960 | 3.189185 | 0.000050 |
| G6_norm_u50_ext_split | normalized_u50_ext_functional_span_split | 0.500000 | -1 | 9437184 | 9437184 | 9437184 | 0.158567 | 3.138850 | 0.000050 |
| G6_u50_ext_split | u50_ext_functional_span_split | 0.500000 | -1 | 9437184 | 9437184 | 9437184 | 0.159379 | 3.137895 | 0.000050 |
| G7_full_tail_resid_split | full_tail_residual_split | 0.500000 | -1 | 9437184 | 9437184 | 9437184 | 0.158176 | 3.138968 | 0.000050 |
| G7_norm_full_tail_resid_split | normalized_full_tail_residual_split | 0.500000 | -1 | 9437184 | 9437184 | 9437184 | 0.162206 | 3.135116 | 0.000050 |

## 8. Main CL result table

| group | label | F_old_mean | F_old_std | G_new_mean | G_new_std | R_mean | R_std | reach_rate_mean | matched_forgetting_mean | n_final_records |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| G0_matched_dense | matched_dense_baseline | 0.000989 | 0.001488 | -0.000466 | 0.002213 | -0.001669 | 0.003074 | 0.450000 | -0.000248 | 60 |
| G0_ER_matched_dense_replay | matched_dense_replay | -0.000294 | 0.001037 | 0.000710 | 0.001827 | 0.000406 | 0.002067 | 0.366667 | -0.000515 | 60 |
| G1_raw_two_branch | raw_two_branch_control | 0.001104 | 0.001992 | -0.000886 | 0.003110 | -0.002273 | 0.004345 | 0.216667 | -0.000500 | 60 |
| G2_random_split | random_projection_split | 0.000380 | 0.001207 | -0.000090 | 0.002103 | -0.000772 | 0.002726 | 0.233333 | -0.000397 | 180 |
| G3_head16_split | head16_split | 0.000461 | 0.002150 | -0.000597 | 0.003032 | -0.001709 | 0.004044 | 0.200000 | -0.000471 | 60 |
| G4_u50_split | u50_middle_band_split | 0.000047 | 0.000987 | 0.000615 | 0.001776 | 0.000204 | 0.002181 | 0.333333 | -0.000169 | 60 |
| G5_ext_split | extreme_low_variance_split | -0.000618 | 0.000874 | 0.000950 | 0.001558 | 0.000833 | 0.001724 | 0.316667 | -0.000552 | 60 |
| G6_u50_ext_split | u50_ext_functional_span_split | -0.000076 | 0.000970 | 0.000541 | 0.001612 | 0.000199 | 0.001986 | 0.216667 | -0.000126 | 60 |
| G6_norm_u50_ext_split | normalized_u50_ext_functional_span_split | -0.000125 | 0.001182 | 0.000369 | 0.002038 | -0.000043 | 0.002358 | 0.283333 | -0.000425 | 60 |
| G7_full_tail_resid_split | full_tail_residual_split | -0.000239 | 0.000803 | 0.000670 | 0.001638 | 0.000455 | 0.001872 | 0.266667 | -0.000487 | 60 |
| G7_norm_full_tail_resid_split | normalized_full_tail_residual_split | -0.000015 | 0.001039 | 0.000795 | 0.001795 | 0.000404 | 0.002134 | 0.316667 | -0.000359 | 60 |

## 9. Matched-learning forgetting analysis

| group | G_new_mean | F_old_mean | matched_forgetting_mean | matched_forgetting_std | reach_rate_mean |
| --- | --- | --- | --- | --- | --- |
| G0_matched_dense | -0.000466 | 0.000989 | -0.000248 | 0.000523 | 0.450000 |
| G0_ER_matched_dense_replay | 0.000710 | -0.000294 | -0.000515 | 0.000548 | 0.366667 |
| G1_raw_two_branch | -0.000886 | 0.001104 | -0.000500 | 0.000575 | 0.216667 |
| G2_random_split | -0.000090 | 0.000380 | -0.000397 | 0.000541 | 0.233333 |
| G3_head16_split | -0.000597 | 0.000461 | -0.000471 | 0.000809 | 0.200000 |
| G4_u50_split | 0.000615 | 0.000047 | -0.000169 | 0.000421 | 0.333333 |
| G5_ext_split | 0.000950 | -0.000618 | -0.000552 | 0.000537 | 0.316667 |
| G6_u50_ext_split | 0.000541 | -0.000076 | -0.000126 | 0.000241 | 0.216667 |
| G6_norm_u50_ext_split | 0.000369 | -0.000125 | -0.000425 | 0.000418 | 0.283333 |
| G7_full_tail_resid_split | 0.000670 | -0.000239 | -0.000487 | 0.000481 | 0.266667 |
| G7_norm_full_tail_resid_split | 0.000795 | -0.000015 | -0.000359 | 0.000439 | 0.316667 |

## 10. Token-frequency-binned results

下表报告 adaptation 后相对 step 0 的 bucket-level change：old split 使用 forgetting 方向，new query split 使用 learning gain 方向。

| group | old_common_F_mean | old_middle_F_mean | old_rare_F_mean | query_common_G_mean | query_middle_G_mean | query_rare_G_mean |
| --- | --- | --- | --- | --- | --- | --- |
| G0_matched_dense | -0.000097 | 0.001255 | 0.001957 | 0.001174 | -0.001096 | 0.001589 |
| G0_ER_matched_dense_replay | -0.000690 | -0.000184 | -0.000224 | 0.001519 | 0.000288 | 0.003458 |
| G1_raw_two_branch | 0.000569 | 0.001293 | 0.000372 | -0.000244 | -0.001282 | 0.002477 |
| G2_random_split | -0.000293 | 0.000546 | 0.000943 | 0.000433 | -0.000434 | 0.002565 |
| G3_head16_split | 0.000905 | 0.000422 | -0.001395 | -0.000941 | -0.000771 | 0.003763 |
| G4_u50_split | -0.000582 | 0.000156 | 0.001563 | 0.001253 | 0.000315 | 0.001870 |
| G5_ext_split | 0.000029 | -0.000768 | -0.001355 | 0.000024 | 0.001131 | 0.001921 |
| G6_u50_ext_split | -0.000785 | 0.000036 | 0.001854 | 0.001051 | 0.000301 | 0.001354 |
| G6_norm_u50_ext_split | -0.001606 | 0.000227 | 0.001421 | 0.001758 | -0.000212 | 0.002484 |
| G7_full_tail_resid_split | -0.000423 | -0.000187 | -0.000212 | 0.000997 | 0.000438 | 0.002117 |
| G7_norm_full_tail_resid_split | -0.001662 | 0.000327 | 0.002745 | 0.001965 | 0.000351 | 0.001834 |

## 11. Branch ablation results

这里的 `plastic_contribution = loss_without_plastic_branch - loss_with_plastic_branch`。如果 middle 或 rare token-frequency bucket 上贡献更大，才支持 branch specialization 的说法。

| group | lr_multiplier | eval_split | token_frequency_bucket | plastic_contribution_mean | plastic_contribution_std | n |
| --- | --- | --- | --- | --- | --- | --- |
| G1_raw_two_branch | 0.500000 | old | common | -0.015487 | 0.006782 | 60 |
| G1_raw_two_branch | 0.500000 | old | middle | 0.167428 | 0.003372 | 60 |
| G1_raw_two_branch | 0.500000 | old | rare | 0.336736 | 0.015379 | 60 |
| G1_raw_two_branch | 0.500000 | query | common | -0.018969 | 0.017486 | 60 |
| G1_raw_two_branch | 0.500000 | query | middle | 0.163492 | 0.020008 | 60 |
| G1_raw_two_branch | 0.500000 | query | rare | 0.332486 | 0.072971 | 60 |
| G2_random_split | 0.500000 | old | common | -0.018039 | 0.006381 | 180 |
| G2_random_split | 0.500000 | old | middle | 0.189622 | 0.002826 | 180 |
| G2_random_split | 0.500000 | old | rare | 0.383720 | 0.011867 | 180 |
| G2_random_split | 0.500000 | query | common | -0.021087 | 0.021815 | 180 |
| G2_random_split | 0.500000 | query | middle | 0.182769 | 0.020001 | 180 |
| G2_random_split | 0.500000 | query | rare | 0.375530 | 0.077211 | 180 |
| G3_head16_split | 0.500000 | old | common | -0.016031 | 0.007626 | 60 |
| G3_head16_split | 0.500000 | old | middle | 0.162185 | 0.003701 | 60 |
| G3_head16_split | 0.500000 | old | rare | 0.335774 | 0.015404 | 60 |
| G3_head16_split | 0.500000 | query | common | -0.016656 | 0.018858 | 60 |
| G3_head16_split | 0.500000 | query | middle | 0.156738 | 0.019439 | 60 |
| G3_head16_split | 0.500000 | query | rare | 0.323433 | 0.077695 | 60 |
| G4_u50_split | 0.500000 | old | common | -0.021225 | 0.007086 | 60 |
| G4_u50_split | 0.500000 | old | middle | 0.194542 | 0.002052 | 60 |
| G4_u50_split | 0.500000 | old | rare | 0.405455 | 0.010515 | 60 |
| G4_u50_split | 0.500000 | query | common | -0.025930 | 0.021827 | 60 |
| G4_u50_split | 0.500000 | query | middle | 0.188016 | 0.019798 | 60 |
| G4_u50_split | 0.500000 | query | rare | 0.394235 | 0.082629 | 60 |
| G5_ext_split | 0.500000 | old | common | -0.023181 | 0.002363 | 60 |
| G5_ext_split | 0.500000 | old | middle | 0.132169 | 0.001690 | 60 |
| G5_ext_split | 0.500000 | old | rare | 0.295823 | 0.003383 | 60 |
| G5_ext_split | 0.500000 | query | common | -0.025030 | 0.014090 | 60 |
| G5_ext_split | 0.500000 | query | middle | 0.127392 | 0.017762 | 60 |
| G5_ext_split | 0.500000 | query | rare | 0.277966 | 0.068546 | 60 |
| G6_norm_u50_ext_split | 0.500000 | old | common | -0.016599 | 0.008909 | 60 |
| G6_norm_u50_ext_split | 0.500000 | old | middle | 0.193349 | 0.002964 | 60 |
| G6_norm_u50_ext_split | 0.500000 | old | rare | 0.402892 | 0.013086 | 60 |
| G6_norm_u50_ext_split | 0.500000 | query | common | -0.022584 | 0.023523 | 60 |
| G6_norm_u50_ext_split | 0.500000 | query | middle | 0.186503 | 0.021021 | 60 |
| G6_norm_u50_ext_split | 0.500000 | query | rare | 0.384634 | 0.078418 | 60 |
| G6_u50_ext_split | 0.500000 | old | common | -0.021216 | 0.007132 | 60 |
| G6_u50_ext_split | 0.500000 | old | middle | 0.194550 | 0.002107 | 60 |
| G6_u50_ext_split | 0.500000 | old | rare | 0.404996 | 0.010509 | 60 |
| G6_u50_ext_split | 0.500000 | query | common | -0.026044 | 0.022002 | 60 |
| G6_u50_ext_split | 0.500000 | query | middle | 0.188125 | 0.019787 | 60 |
| G6_u50_ext_split | 0.500000 | query | rare | 0.393992 | 0.083399 | 60 |
| G7_full_tail_resid_split | 0.500000 | old | common | -0.020410 | 0.005975 | 60 |
| G7_full_tail_resid_split | 0.500000 | old | middle | 0.193387 | 0.001769 | 60 |
| G7_full_tail_resid_split | 0.500000 | old | rare | 0.397238 | 0.010139 | 60 |
| G7_full_tail_resid_split | 0.500000 | query | common | -0.024594 | 0.021303 | 60 |
| G7_full_tail_resid_split | 0.500000 | query | middle | 0.187001 | 0.019916 | 60 |
| G7_full_tail_resid_split | 0.500000 | query | rare | 0.385459 | 0.079603 | 60 |
| G7_norm_full_tail_resid_split | 0.500000 | old | common | -0.017016 | 0.008381 | 60 |
| G7_norm_full_tail_resid_split | 0.500000 | old | middle | 0.196976 | 0.002499 | 60 |
| G7_norm_full_tail_resid_split | 0.500000 | old | rare | 0.404118 | 0.011714 | 60 |
| G7_norm_full_tail_resid_split | 0.500000 | query | common | -0.021810 | 0.023005 | 60 |
| G7_norm_full_tail_resid_split | 0.500000 | query | middle | 0.189570 | 0.020488 | 60 |
| G7_norm_full_tail_resid_split | 0.500000 | query | rare | 0.390463 | 0.081176 | 60 |

## 12. Routing diagnostics

Stage B routing diagnostics 只在 Stage A 通过后运行。本报告若显示 `not run`，表示 Stage A 尚未触发 routing audit。

| group | K | router input | expert input | entropy | G_second_middle | G_second_rare | oracle regret | oracle hit rate | margin-adv corr |
|---|---:|---|---|---:|---:|---:|---:|---:|---:|
| not run | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |

## 13. Oracle routing upper bound

Stage B 未运行时，oracle routing upper bound 不产生结论。如果 Stage A 通过，后续应对 routed groups 计算 token-level counterfactual expert losses。

## 14. Hidden-gradient conflict audit

这里使用 layer 8 `post_attention_layernorm` 输出位置的 hidden-gradient，而不是 full parameter gradient；数值为 old/new loss hidden-gradient 在指定 variance band 内的 cosine。

| group | lr_multiplier | variance_band | hidden_gradient_conflict_cosine_mean | hidden_gradient_conflict_cosine_std | n |
| --- | --- | --- | --- | --- | --- |
| G0_ER_matched_dense_replay | 0.500000 | ext | -0.000368 | 0.084932 | 9 |
| G0_ER_matched_dense_replay | 0.500000 | full_tail_resid | 0.049761 | 0.049345 | 9 |
| G0_ER_matched_dense_replay | 0.500000 | head16 | 0.194909 | 0.209576 | 9 |
| G0_ER_matched_dense_replay | 0.500000 | u50 | 0.079505 | 0.077859 | 9 |
| G0_ER_matched_dense_replay | 0.500000 | u50_ext | 0.035581 | 0.066236 | 9 |
| G0_matched_dense | 0.500000 | ext | 0.007840 | 0.083551 | 9 |
| G0_matched_dense | 0.500000 | full_tail_resid | 0.056113 | 0.053566 | 9 |
| G0_matched_dense | 0.500000 | head16 | 0.225511 | 0.219413 | 9 |
| G0_matched_dense | 0.500000 | u50 | 0.085087 | 0.083994 | 9 |
| G0_matched_dense | 0.500000 | u50_ext | 0.042738 | 0.069396 | 9 |
| G1_raw_two_branch | 0.500000 | ext | 0.045595 | 0.081170 | 9 |
| G1_raw_two_branch | 0.500000 | full_tail_resid | 0.070516 | 0.036550 | 9 |
| G1_raw_two_branch | 0.500000 | head16 | 0.238444 | 0.130383 | 9 |
| G1_raw_two_branch | 0.500000 | u50 | 0.074164 | 0.087564 | 9 |
| G1_raw_two_branch | 0.500000 | u50_ext | 0.058412 | 0.049079 | 9 |
| G2_random_split | 0.500000 | ext | 0.059295 | 0.053654 | 27 |
| G2_random_split | 0.500000 | full_tail_resid | 0.118022 | 0.043017 | 27 |
| G2_random_split | 0.500000 | head16 | 0.151137 | 0.198422 | 27 |
| G2_random_split | 0.500000 | u50 | 0.155979 | 0.097020 | 27 |
| G2_random_split | 0.500000 | u50_ext | 0.104606 | 0.048054 | 27 |
| G3_head16_split | 0.500000 | ext | 0.050078 | 0.098049 | 9 |
| G3_head16_split | 0.500000 | full_tail_resid | 0.111516 | 0.061867 | 9 |
| G3_head16_split | 0.500000 | head16 | 0.478263 | 0.251099 | 9 |
| G3_head16_split | 0.500000 | u50 | 0.113895 | 0.099733 | 9 |
| G3_head16_split | 0.500000 | u50_ext | 0.079319 | 0.078026 | 9 |
| G4_u50_split | 0.500000 | ext | 0.021794 | 0.064413 | 9 |
| G4_u50_split | 0.500000 | full_tail_resid | 0.083545 | 0.037364 | 9 |
| G4_u50_split | 0.500000 | head16 | 0.129782 | 0.190884 | 9 |
| G4_u50_split | 0.500000 | u50 | 0.123329 | 0.077006 | 9 |
| G4_u50_split | 0.500000 | u50_ext | 0.071981 | 0.038091 | 9 |
| G5_ext_split | 0.500000 | ext | 0.084602 | 0.076065 | 9 |
| G5_ext_split | 0.500000 | full_tail_resid | 0.120618 | 0.079189 | 9 |
| G5_ext_split | 0.500000 | head16 | 0.136505 | 0.199643 | 9 |
| G5_ext_split | 0.500000 | u50 | 0.143707 | 0.138085 | 9 |
| G5_ext_split | 0.500000 | u50_ext | 0.110981 | 0.076230 | 9 |
| G6_norm_u50_ext_split | 0.500000 | ext | 0.008941 | 0.054196 | 9 |
| G6_norm_u50_ext_split | 0.500000 | full_tail_resid | 0.060291 | 0.049840 | 9 |
| G6_norm_u50_ext_split | 0.500000 | head16 | 0.186275 | 0.219792 | 9 |
| G6_norm_u50_ext_split | 0.500000 | u50 | 0.073702 | 0.116420 | 9 |
| G6_norm_u50_ext_split | 0.500000 | u50_ext | 0.043021 | 0.050647 | 9 |
| G6_u50_ext_split | 0.500000 | ext | 0.022212 | 0.063119 | 9 |
| G6_u50_ext_split | 0.500000 | full_tail_resid | 0.083319 | 0.036964 | 9 |
| G6_u50_ext_split | 0.500000 | head16 | 0.124785 | 0.198990 | 9 |
| G6_u50_ext_split | 0.500000 | u50 | 0.122860 | 0.075644 | 9 |
| G6_u50_ext_split | 0.500000 | u50_ext | 0.071888 | 0.036153 | 9 |
| G7_full_tail_resid_split | 0.500000 | ext | 0.032241 | 0.063236 | 9 |
| G7_full_tail_resid_split | 0.500000 | full_tail_resid | 0.089536 | 0.041702 | 9 |
| G7_full_tail_resid_split | 0.500000 | head16 | 0.120143 | 0.205366 | 9 |
| G7_full_tail_resid_split | 0.500000 | u50 | 0.125652 | 0.084388 | 9 |
| G7_full_tail_resid_split | 0.500000 | u50_ext | 0.078352 | 0.037918 | 9 |
| G7_norm_full_tail_resid_split | 0.500000 | ext | 0.025573 | 0.062410 | 9 |
| G7_norm_full_tail_resid_split | 0.500000 | full_tail_resid | 0.078543 | 0.054317 | 9 |
| G7_norm_full_tail_resid_split | 0.500000 | head16 | 0.119677 | 0.202643 | 9 |
| G7_norm_full_tail_resid_split | 0.500000 | u50 | 0.104994 | 0.110167 | 9 |
| G7_norm_full_tail_resid_split | 0.500000 | u50_ext | 0.065159 | 0.056816 | 9 |

## 15. Gate decisions

- formal_ready：`True`
- best_real_split：`G7_full_tail_resid_split`
- decision：`no_valid_forgetting_object`
- criteria：`{"gate1_old_stage_all_improve": true, "gate1_old_stage_comparable": true, "old_stage_post_old_loss_range": 0.05475889386669319, "gate2_dense_G_new_positive": false, "gate2_dense_forgetting_or_matched_tradeoff": true, "best_lower_F_old_than_matched_dense": true, "best_comparable_or_better_G_new_than_matched_dense": true, "best_better_R_than_raw_two_branch": true, "best_better_R_than_random_split": true, "best_better_R_than_head16_split": true, "branch_contribution_middle_or_rare_ge_common": true, "hidden_gradient_conflict_not_worse_than_random": false}`
- gate1_old_stage_valid：`True`
- gate2_forgetting_object_exists：`False`
- gate3_real_split_beats_h3_controls：`True`

## 16. What can be claimed

- 可以声称：本实验把 Phase8 old-stage continual-learning / CL 协议与 H3 causal controls 对齐到同一评估框架中。
- 可以声称：Stage A 已比较 dense、replay、raw two-branch、random split、head16、u50、ext、u50_ext、normalized variants、full_tail_resid。
- 只有当 Gate 1-3 都通过时，才可以声称 non-routing real variance-band split 在 old-stage protocol 下经受住 H3 controls。

## 17. What cannot be claimed

- Stage B 未运行时，不能声称 routing advantage 或 expert specialization 成立或失败。
- 即使 Stage B 后续通过，也不能声称 full hierarchical MoE 已被验证。
- 如果 random split 或 raw two-branch 匹配 real variance-band split，不能声称收益来自指定 variance band。

## 18. Recommended next iteration

- 如果 Gate 1 或 Gate 2 失败：先调整 old-stage checkpoint matching 或 CL stress construction，不运行 routing。
- 如果 Gate 3 失败：回到 representation split hypothesis，不运行 Stage B routing。
- 如果 Gate 1-3 都通过：运行 Stage B K=4 routing controls，并加入 uniform mixture、flat raw MoE、oracle routing diagnostics。

Final decision:

The old-stage protocol produced a comparable old-task state, but the matched dense baseline did not show positive new-task learning under the selected new-stage setting, so routing anti-forgetting claims should not be evaluated yet.