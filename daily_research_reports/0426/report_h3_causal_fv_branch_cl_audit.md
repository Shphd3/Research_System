# H3-Causal FV-Branch CL Audit 中文报告

## 1. 实验目标（Experiment objective）

本实验独立于 Phase8p* 命名序列，目标是检验 variance band / token-frequency bucket-aware two-branch plastic update 是否在 continual learning / CL 中提供真实隔离收益。核心比较对象包括 matched dense baseline、dense replay baseline、raw two-branch control、random split control，以及若干基于 variance band 的真实 representation split。

这不是 hierarchical MoE 实验，也不测试 routing；它是进入多 branch 或 hierarchical MoE 之前的最小因果审计。

## 2. 英文术语定义（Definitions of all English terms）

- `Pretrained LM`：在本实验前已经在大规模文本上完成预训练的语言模型。
- `Hidden state / representation`：选定模型层中每个 token 对应的向量表示。
- `Subspace`：由一组选定 PCA/SVD 方向张成的线性空间。
- `Variance band`：按照奇异值或方差排序后选出的一组 hidden-state directions。
- `Token-frequency bucket`：按训练语料中目标 token 出现次数划分出的 high / middle / rare token 组。
- `Head / common directions`：最高方差的 hidden-state directions，本实验固定为前 16 个方向。
- `Tail residual`：hidden state 减去均值后，再移除 top common directions 后得到的 residual representation。
- `Two-branch factorization`：common branch 加 plastic branch 的模块分解形式。
- `Matched budget`：不同模型条件之间 trainable parameter count 被匹配。
- `Continual learning / CL`：在 new-domain support data 上适配，同时测量 old-domain forgetting 的设置。
- `Forgetting`：new-domain adaptation 之后 old-domain loss 相对 adaptation 之前的增加量。
- `Branch specialization`：某个 branch 对特定 token-frequency bucket 或 domain 的贡献更大。
- `Expert specialization`：仅用于 routed model；被 router 选中的 expert 相比未选中的 expert 有更低 NTP loss。

## 3. 数据集构造（Dataset construction）

- old domains：`CS, Civil, MAE, Medical, Psychology`
- new domains：`ECE, biochemistry`
- WoS old eval chunks：`120`；本次实际评估限制：`full`
- DCLM eval chunks：`128`；本次实际评估限制：`full`
- episodes per seed：`20`；本次实际运行 episodes：`20`
- 每个 episode 使用 `1` 个 new-domain support chunk 和 `16` 个 new-domain query chunks。

## 4. 校准细节（Calibration details）

- base model：`Qwen3-0.6B`
- layer：`8`
- hook point：`post_attention_layernorm`
- calibration artifact 在所有 group 之间共享，包含同一个 mean vector `mu` 与 PCA/SVD directions `V`。
- `head16` 使用 PCA/SVD directions `1:16`；`u50` 使用 `17:207`；`ext` 使用 `782:r`；`u50_ext = u50 + 0.25 * ext`；`full_tail_resid` 是移除 head / common directions 后的 residual representation。

## 5. 模型条件与参数量（Model conditions and parameter counts）

| group | label | lr_multiplier | random_projection_seed | trainable_params | learning_rate |
| --- | --- | --- | --- | --- | --- |
| G0_ER_matched_dense_replay | matched_dense_replay | 0.500000 | -1 | 9437184 | 0.000050 |
| G0_matched_dense | matched_dense_baseline | 0.500000 | -1 | 9437184 | 0.000050 |
| G1_raw_two_branch | raw_two_branch_control | 0.500000 | -1 | 9437184 | 0.000050 |
| G2_random_split | random_projection_split | 0.500000 | 0 | 9437184 | 0.000050 |
| G2_random_split | random_projection_split | 0.500000 | 1 | 9437184 | 0.000050 |
| G2_random_split | random_projection_split | 0.500000 | 2 | 9437184 | 0.000050 |
| G0_ER_matched_dense_replay | matched_dense_replay | 0.500000 | -1 | 9437184 | 0.000050 |
| G0_matched_dense | matched_dense_baseline | 0.500000 | -1 | 9437184 | 0.000050 |
| G1_raw_two_branch | raw_two_branch_control | 0.500000 | -1 | 9437184 | 0.000050 |
| G2_random_split | random_projection_split | 0.500000 | 0 | 9437184 | 0.000050 |
| G2_random_split | random_projection_split | 0.500000 | 1 | 9437184 | 0.000050 |
| G2_random_split | random_projection_split | 0.500000 | 2 | 9437184 | 0.000050 |
| G0_matched_dense | matched_dense_baseline | 0.500000 | -1 | 9437184 | 0.000050 |
| G3_head16_split | head16_split | 0.500000 | -1 | 9437184 | 0.000050 |
| G4_u50_split | u50_middle_band_split | 0.500000 | -1 | 9437184 | 0.000050 |
| G5_ext_split | extreme_low_variance_split | 0.500000 | -1 | 9437184 | 0.000050 |
| G6_u50_ext_split | u50_ext_functional_span_split | 0.500000 | -1 | 9437184 | 0.000050 |
| G7_full_tail_resid_split | full_tail_residual_split | 0.500000 | -1 | 9437184 | 0.000050 |
| G3_head16_split | head16_split | 0.500000 | -1 | 9437184 | 0.000050 |
| G4_u50_split | u50_middle_band_split | 0.500000 | -1 | 9437184 | 0.000050 |
| G5_ext_split | extreme_low_variance_split | 0.500000 | -1 | 9437184 | 0.000050 |
| G6_u50_ext_split | u50_ext_functional_span_split | 0.500000 | -1 | 9437184 | 0.000050 |
| G7_full_tail_resid_split | full_tail_residual_split | 0.500000 | -1 | 9437184 | 0.000050 |
| G3_head16_split | head16_split | 0.500000 | -1 | 9437184 | 0.000050 |
| G0_ER_matched_dense_replay | matched_dense_replay | 0.500000 | -1 | 9437184 | 0.000050 |
| G1_raw_two_branch | raw_two_branch_control | 0.500000 | -1 | 9437184 | 0.000050 |
| G2_random_split | random_projection_split | 0.500000 | 0 | 9437184 | 0.000050 |
| G2_random_split | random_projection_split | 0.500000 | 1 | 9437184 | 0.000050 |
| G2_random_split | random_projection_split | 0.500000 | 2 | 9437184 | 0.000050 |
| G4_u50_split | u50_middle_band_split | 0.500000 | -1 | 9437184 | 0.000050 |
| G5_ext_split | extreme_low_variance_split | 0.500000 | -1 | 9437184 | 0.000050 |
| G6_u50_ext_split | u50_ext_functional_span_split | 0.500000 | -1 | 9437184 | 0.000050 |
| G7_full_tail_resid_split | full_tail_residual_split | 0.500000 | -1 | 9437184 | 0.000050 |

## 6. 训练协议（Training protocol）

- backbone、LM head、attention、layer norm 均冻结；只训练 replacement block 中被允许的参数。
- adaptation horizon：`U=8`
- main LR multiplier：`0.5x`；本次 `lr_multipliers=0.5`
- seeds：`20260418,20260419,20260420`
- random projection seeds：`0,1,2`；`G2_random_split` 的 random subspace dimension 与 `u50_ext` 比较对象匹配。
- `G0_ER_matched_dense_replay` 在 adaptation 中加入 old replay item，old replay token count 与 new support token count 匹配。

## 7. 主结果表（Main result table）

| group | label | F_old_mean | F_old_std | G_new_mean | G_new_std | R_mean | R_std | reach_rate_mean | matched_forgetting_mean | n_final_records |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| G0_matched_dense | matched_dense_baseline | -0.025405 | 0.005914 | 0.026537 | 0.006086 | 0.026537 | 0.006086 | 1.000000 | -0.025405 | 60 |
| G0_ER_matched_dense_replay | matched_dense_replay | -0.030705 | 0.004402 | 0.030982 | 0.004649 | 0.030982 | 0.004649 | 0.900000 | -0.025517 | 60 |
| G1_raw_two_branch | raw_two_branch_control | -0.034429 | 0.008022 | 0.034492 | 0.008266 | 0.034492 | 0.008266 | 1.000000 | -0.026566 | 60 |
| G2_random_split | random_projection_split | -0.004928 | 0.001964 | 0.005209 | 0.001938 | 0.005209 | 0.001938 | 0.000000 |  | 180 |
| G3_head16_split | head16_split | -0.016503 | 0.003822 | 0.017174 | 0.003345 | 0.017174 | 0.003345 | 0.000000 |  | 60 |
| G4_u50_split | u50_middle_band_split | -0.001056 | 0.000553 | 0.001499 | 0.000832 | 0.001499 | 0.000832 | 0.000000 |  | 60 |
| G5_ext_split | extreme_low_variance_split | 0.000152 | 0.000216 | 0.000032 | 0.000744 | -0.000148 | 0.000754 | 0.000000 |  | 60 |
| G6_u50_ext_split | u50_ext_functional_span_split | -0.001189 | 0.000572 | 0.001416 | 0.000918 | 0.001416 | 0.000918 | 0.000000 |  | 60 |
| G7_full_tail_resid_split | full_tail_residual_split | -0.001075 | 0.000533 | 0.000970 | 0.000678 | 0.000970 | 0.000678 | 0.000000 |  | 60 |

## 8. Token-frequency-binned NTP loss

下表报告 adaptation 后相对 step 0 的 bucket-level change：old split 使用 forgetting 方向，new query split 使用 learning gain 方向。

| group | old_common_F_mean | old_middle_F_mean | old_rare_F_mean | query_common_G_mean | query_middle_G_mean | query_rare_G_mean |
| --- | --- | --- | --- | --- | --- | --- |
| G0_matched_dense | -0.004333 | -0.030093 | -0.054121 | 0.002752 | 0.030954 | 0.067505 |
| G0_ER_matched_dense_replay | -0.006368 | -0.036073 | -0.064839 | 0.004845 | 0.036178 | 0.071275 |
| G1_raw_two_branch | -0.003130 | -0.041548 | -0.073793 | 0.002808 | 0.040358 | 0.088983 |
| G2_random_split | -0.000840 | -0.005790 | -0.011499 | 0.001003 | 0.006043 | 0.011536 |
| G3_head16_split | -0.002193 | -0.019725 | -0.035210 | 0.002025 | 0.020155 | 0.040956 |
| G4_u50_split | 0.000002 | -0.001264 | -0.003075 | 0.000415 | 0.001720 | 0.003024 |
| G5_ext_split | -0.000187 | 0.000248 | 0.000186 | 0.000027 | 0.000064 | -0.000388 |
| G6_u50_ext_split | -0.000071 | -0.001419 | -0.003107 | 0.000284 | 0.001612 | 0.003312 |
| G7_full_tail_resid_split | -0.000141 | -0.001312 | -0.001735 | 0.000162 | 0.001079 | 0.003083 |

## 9. Branch ablation results

这里的 `plastic_contribution = loss_without_plastic_branch - loss_with_plastic_branch`。如果 middle 或 rare token-frequency bucket 上贡献更大，才支持 branch specialization 的说法。

| group | lr_multiplier | eval_split | token_frequency_bucket | plastic_contribution_mean | plastic_contribution_std | n |
| --- | --- | --- | --- | --- | --- | --- |
| G1_raw_two_branch | 0.500000 | old | common | 0.003541 | 0.006408 | 60 |
| G1_raw_two_branch | 0.500000 | old | middle | 0.041050 | 0.010511 | 60 |
| G1_raw_two_branch | 0.500000 | old | rare | 0.074484 | 0.018010 | 60 |
| G1_raw_two_branch | 0.500000 | query | common | 0.002457 | 0.008465 | 60 |
| G1_raw_two_branch | 0.500000 | query | middle | 0.040568 | 0.009902 | 60 |
| G1_raw_two_branch | 0.500000 | query | rare | 0.088883 | 0.033355 | 60 |
| G2_random_split | 0.500000 | old | common | 0.001087 | 0.000527 | 180 |
| G2_random_split | 0.500000 | old | middle | 0.005520 | 0.002399 | 180 |
| G2_random_split | 0.500000 | old | rare | 0.011945 | 0.004254 | 180 |
| G2_random_split | 0.500000 | query | common | 0.000451 | 0.001574 | 180 |
| G2_random_split | 0.500000 | query | middle | 0.006117 | 0.002061 | 180 |
| G2_random_split | 0.500000 | query | rare | 0.011664 | 0.007402 | 180 |
| G3_head16_split | 0.500000 | old | common | 0.002546 | 0.001419 | 60 |
| G3_head16_split | 0.500000 | old | middle | 0.019482 | 0.004771 | 60 |
| G3_head16_split | 0.500000 | old | rare | 0.036520 | 0.008512 | 60 |
| G3_head16_split | 0.500000 | query | common | 0.001601 | 0.002920 | 60 |
| G3_head16_split | 0.500000 | query | middle | 0.020225 | 0.003984 | 60 |
| G3_head16_split | 0.500000 | query | rare | 0.040333 | 0.015830 | 60 |
| G4_u50_split | 0.500000 | old | common | 0.000435 | 0.000373 | 60 |
| G4_u50_split | 0.500000 | old | middle | 0.001229 | 0.000651 | 60 |
| G4_u50_split | 0.500000 | old | rare | 0.003922 | 0.001781 | 60 |
| G4_u50_split | 0.500000 | query | common | -0.000154 | 0.001292 | 60 |
| G4_u50_split | 0.500000 | query | middle | 0.001760 | 0.000939 | 60 |
| G4_u50_split | 0.500000 | query | rare | 0.003424 | 0.004971 | 60 |
| G5_ext_split | 0.500000 | old | common | 0.000382 | 0.000362 | 60 |
| G5_ext_split | 0.500000 | old | middle | -0.000264 | 0.000247 | 60 |
| G5_ext_split | 0.500000 | old | rare | 0.000793 | 0.001419 | 60 |
| G5_ext_split | 0.500000 | query | common | -0.000452 | 0.001163 | 60 |
| G5_ext_split | 0.500000 | query | middle | 0.000178 | 0.000824 | 60 |
| G5_ext_split | 0.500000 | query | rare | 0.000683 | 0.003762 | 60 |
| G6_u50_ext_split | 0.500000 | old | common | 0.000525 | 0.000384 | 60 |
| G6_u50_ext_split | 0.500000 | old | middle | 0.001204 | 0.000671 | 60 |
| G6_u50_ext_split | 0.500000 | old | rare | 0.003631 | 0.001480 | 60 |
| G6_u50_ext_split | 0.500000 | query | common | -0.000210 | 0.001478 | 60 |
| G6_u50_ext_split | 0.500000 | query | middle | 0.001621 | 0.001012 | 60 |
| G6_u50_ext_split | 0.500000 | query | rare | 0.003274 | 0.004699 | 60 |
| G7_full_tail_resid_split | 0.500000 | old | common | 0.000463 | 0.000411 | 60 |
| G7_full_tail_resid_split | 0.500000 | old | middle | 0.000835 | 0.000599 | 60 |
| G7_full_tail_resid_split | 0.500000 | old | rare | 0.003184 | 0.001633 | 60 |
| G7_full_tail_resid_split | 0.500000 | query | common | -0.000339 | 0.001364 | 60 |
| G7_full_tail_resid_split | 0.500000 | query | middle | 0.001180 | 0.000885 | 60 |
| G7_full_tail_resid_split | 0.500000 | query | rare | 0.002830 | 0.004326 | 60 |

## 10. Hidden-gradient conflict audit

这里使用 layer 8 `post_attention_layernorm` 输出位置的 hidden-gradient，而不是 full parameter gradient；数值为 old/new loss hidden-gradient 在指定 variance band 内的 cosine。

| group | lr_multiplier | variance_band | hidden_gradient_conflict_cosine_mean | hidden_gradient_conflict_cosine_std | n |
| --- | --- | --- | --- | --- | --- |
| G0_ER_matched_dense_replay | 0.500000 | ext | 0.118367 | 0.069697 | 60 |
| G0_ER_matched_dense_replay | 0.500000 | full_tail_resid | 0.101997 | 0.074175 | 60 |
| G0_ER_matched_dense_replay | 0.500000 | head16 | 0.064579 | 0.224381 | 60 |
| G0_ER_matched_dense_replay | 0.500000 | u50 | 0.101873 | 0.112179 | 60 |
| G0_ER_matched_dense_replay | 0.500000 | u50_ext | 0.112821 | 0.080765 | 60 |
| G0_matched_dense | 0.500000 | ext | 0.123221 | 0.068878 | 60 |
| G0_matched_dense | 0.500000 | full_tail_resid | 0.107009 | 0.071721 | 60 |
| G0_matched_dense | 0.500000 | head16 | 0.045432 | 0.216263 | 60 |
| G0_matched_dense | 0.500000 | u50 | 0.105858 | 0.111982 | 60 |
| G0_matched_dense | 0.500000 | u50_ext | 0.117502 | 0.080008 | 60 |
| G1_raw_two_branch | 0.500000 | ext | 0.120914 | 0.066779 | 60 |
| G1_raw_two_branch | 0.500000 | full_tail_resid | 0.103032 | 0.074421 | 60 |
| G1_raw_two_branch | 0.500000 | head16 | 0.080787 | 0.257002 | 60 |
| G1_raw_two_branch | 0.500000 | u50 | 0.103703 | 0.111206 | 60 |
| G1_raw_two_branch | 0.500000 | u50_ext | 0.115161 | 0.078283 | 60 |
| G2_random_split | 0.500000 | ext | 0.170208 | 0.079711 | 180 |
| G2_random_split | 0.500000 | full_tail_resid | 0.150913 | 0.080710 | 180 |
| G2_random_split | 0.500000 | head16 | 0.085982 | 0.253025 | 180 |
| G2_random_split | 0.500000 | u50 | 0.134241 | 0.113313 | 180 |
| G2_random_split | 0.500000 | u50_ext | 0.156578 | 0.085215 | 180 |
| G3_head16_split | 0.500000 | ext | 0.156003 | 0.078181 | 60 |
| G3_head16_split | 0.500000 | full_tail_resid | 0.134019 | 0.080074 | 60 |
| G3_head16_split | 0.500000 | head16 | 0.074506 | 0.240821 | 60 |
| G3_head16_split | 0.500000 | u50 | 0.120690 | 0.114760 | 60 |
| G3_head16_split | 0.500000 | u50_ext | 0.142595 | 0.084550 | 60 |
| G4_u50_split | 0.500000 | ext | 0.173827 | 0.080079 | 60 |
| G4_u50_split | 0.500000 | full_tail_resid | 0.155525 | 0.081316 | 60 |
| G4_u50_split | 0.500000 | head16 | 0.096939 | 0.259662 | 60 |
| G4_u50_split | 0.500000 | u50 | 0.138459 | 0.113764 | 60 |
| G4_u50_split | 0.500000 | u50_ext | 0.160448 | 0.085651 | 60 |
| G5_ext_split | 0.500000 | ext | 0.175958 | 0.080834 | 60 |
| G5_ext_split | 0.500000 | full_tail_resid | 0.157424 | 0.082079 | 60 |
| G5_ext_split | 0.500000 | head16 | 0.099365 | 0.262294 | 60 |
| G5_ext_split | 0.500000 | u50 | 0.140414 | 0.113692 | 60 |
| G5_ext_split | 0.500000 | u50_ext | 0.162502 | 0.086164 | 60 |
| G6_u50_ext_split | 0.500000 | ext | 0.173678 | 0.080797 | 60 |
| G6_u50_ext_split | 0.500000 | full_tail_resid | 0.155475 | 0.081608 | 60 |
| G6_u50_ext_split | 0.500000 | head16 | 0.097631 | 0.258626 | 60 |
| G6_u50_ext_split | 0.500000 | u50 | 0.138166 | 0.113801 | 60 |
| G6_u50_ext_split | 0.500000 | u50_ext | 0.160221 | 0.086152 | 60 |
| G7_full_tail_resid_split | 0.500000 | ext | 0.173293 | 0.081173 | 60 |
| G7_full_tail_resid_split | 0.500000 | full_tail_resid | 0.155256 | 0.082009 | 60 |
| G7_full_tail_resid_split | 0.500000 | head16 | 0.098908 | 0.259605 | 60 |
| G7_full_tail_resid_split | 0.500000 | u50 | 0.138678 | 0.114110 | 60 |
| G7_full_tail_resid_split | 0.500000 | u50_ext | 0.160228 | 0.086477 | 60 |

## 11. H3 pass/fail decision

- formal_ready：`True`
- best_real_split：`G6_u50_ext_split`
- decision：`fail_against_random_split`
- criteria：`{"lower_F_old_than_matched_dense": false, "comparable_or_better_G_new_than_matched_dense": false, "better_R_than_raw_two_branch": false, "better_R_than_random_split": false, "branch_contribution_middle_or_rare_ge_common": true, "hidden_gradient_conflict_not_worse_than_random": true}`

The observed benefit is not specific to the proposed variance band. The representation-split hypothesis must be revised.

## 12. What can be claimed

- 可以声称本实验已经把 dense capacity、raw two-branch factorization、random projection 三类替代解释放进同一个 matched-budget continual learning / CL 审计框架中。
- 如果 `formal_ready=false`，只能声称 runner、指标与报告格式已经连通，不能声称 H3 通过或失败。
- 如果最终 gate 通过，只能声称 coarse two-branch isolation 得到支持，不能直接声称 hierarchical MoE 或 routing 有额外价值。

## 13. What cannot be claimed

- 本实验没有测试 routed model，所以不能声称 expert specialization 成立。
- 本实验没有测试多层、多 branch hierarchy，所以不能声称 hierarchical MoE 已被验证。
- 如果 `G2_random_split` 接近或超过真实 variance band split，就不能声称收益来自指定 variance band。

## 14. Recommended next step

- 先完成 main `0.5x` formal matrix：所有 group，3 个 model seeds，每个 seed 20 个 episodes，`G2_random_split` 每个 model seed 使用 3 个 random projection seeds。
- formal matrix 完成后，用同一批 saved episodes/checkpoints 跑完整 branch ablation 与 hidden-gradient conflict audit。
- 只有当 `G6_u50_ext_split` 或 `G7_full_tail_resid_split` 同时超过 matched dense、raw two-branch、random split，并且 token-frequency bucket 与 hidden-gradient conflict 证据一致时，才进入 routing 或 hierarchical MoE 的下一阶段。
