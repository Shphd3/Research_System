派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_25_02_learning_history_representation/20261023/evidence_tables_cn.md`。
[精确原始文件](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_25_02_learning_history_representation/20261023/evidence_tables_cn.md)；研究修改仍回到原件。

---

# A15_25_02 证据表

研究问题：学习经历如何改变条件规则的表征，以及哪些方向对任务作答最重要？

原生行为与资格使用全部 1,600 条已暴露 DEV；干预使用 816 条评估样本、204 个无序词组。统计推断均为一个选定训练种子下的探索证据。三个主要区间使用 5,000 次配对组级重采样。字典重建资格失败与方向干预的数值结果分别判断。表中的英文条件名是可追溯的原始标识。

## 原生行为

| State | Task | Full-vocabulary accuracy | Forced first/last accuracy | Mean margin (logits) | Mean NLL (nats) |
|---|---|---:|---:|---:|---:|
| Base | old | 33.250% | 52.250% | 0.0357 | 2.4465 |
| Base | new | 26.250% | 48.375% | -0.0107 | 2.6611 |
| Learned A | old | 100.000% | 100.000% | 17.5247 | 0.0007 |
| Learned A | new | 0.000% | 0.000% | -16.0350 | 16.0378 |
| A then B only | old | 0.000% | 0.000% | -15.0797 | 15.0799 |
| A then B only | new | 100.000% | 100.000% | 15.5408 | 0.0002 |
| A then mixed A+B | old | 99.625% | 99.750% | 17.0696 | 0.0269 |
| A then mixed A+B | new | 99.750% | 99.875% | 15.2472 | 0.0148 |

## 字典资格

| State | Final-layer centered FVE | Relative squared reconstruction error | Native accuracy | Reconstructed accuracy | Dictionary gate |
|---|---:|---:|---:|---:|---|
| Base | -1.0452 | 4.425% | 29.750% | 28.938% | FAIL |
| Learned A | -0.8642 | 82.608% | 50.000% | 43.562% | FAIL |
| A then B only | -0.8647 | 95.970% | 50.000% | 35.688% | FAIL |
| A then mixed A+B | -0.9710 | 104.478% | 99.688% | 56.750% | FAIL |

## 主要对比

| Registered contrast | Excess effect (logits) | 98.333% group interval | Numerical decision |
|---|---:|---|---|
| mixed_old_half_attenuation | 1.1299 | [1.0369, 1.2278] | SUPPORTED_LOCAL |
| mixed_new_half_attenuation | 1.4274 | [1.2738, 1.5747] | SUPPORTED_LOCAL |
| raw_rank16_old_transfer | 17.8079 | [16.7392, 18.8967] | SUPPORTED_LOCAL |

## 配对原始几何

| Paired states | Relative change norm, final layer | Mean final-layer cosine | Largest earlier-layer absolute change |
|---|---:|---:|---:|
| base__A | 0.9192 | 0.3949 | 0.0 |
| A__sequential | 0.6791 | 0.7453 | 0.0 |
| A__mixed | 0.5802 | 0.8129 | 0.0 |
| sequential__mixed | 0.5041 | 0.8562 | 0.0 |

## 发现阶段的变化谱

| Discovery rank | Cumulative state-change energy |
|---:|---:|
| 1 | 28.339% |
| 4 | 50.553% |
| 16 | 75.481% |

## 冻结候选 ID

| Discovery candidate set | Feature IDs (ranked) |
|---|---|
| A_old | 10838, 13964, 6199, 5332, 13465, 2506, 14886, 2468, 15993, 2919, 11318, 5776, 15379, 1102, 12921, 14, 11546, 7415, 2393, 1741, 14794, 4300, 13944, 12179, 15493, 8060, 6706, 557, 864, 2431, 7636, 3079 |
| sequential_new | 10838, 6199, 13964, 13465, 2506, 5332, 14886, 2468, 15993, 2919, 11318, 8060, 557, 1102, 7415, 15379, 12921, 4300, 5776, 14, 2393, 11546, 12179, 14794, 9900, 6706, 7388, 864, 2163, 13944, 1741, 2431 |
| mixed_old | 10838, 13964, 6199, 13465, 2506, 5332, 14886, 2468, 2919, 8060, 15993, 12921, 1102, 5776, 7415, 11318, 14, 15379, 13944, 1741, 12179, 11546, 15493, 2393, 14794, 4300, 557, 864, 6706, 7388, 9900, 12671 |
| mixed_new | 10838, 13964, 6199, 5332, 2506, 13465, 14886, 2468, 15993, 2919, 1102, 8060, 11318, 557, 12921, 7415, 15379, 5776, 4300, 14, 11546, 1741, 2393, 12179, 14794, 9900, 6706, 864, 13944, 7388, 2163, 2431 |
| mixed_frequent | 14, 23, 864, 1265, 1819, 1982, 2138, 2145, 2174, 2252, 2286, 2408, 2468, 3097, 4080, 4226, 4299, 4380, 4764, 5332, 5646, 5913, 6356, 6432, 7134, 7303, 7304, 7310, 7388, 7415, 7798, 7880 |

The two primary 32-feature sets share 30 IDs (Jaccard 0.8824). Shared IDs are not proof of a common computation.

## 全部 253 个干预条件

| Condition | Recipient | Type | Old accuracy | New accuracy | Old margin | New margin | Mean edit norm | Isotropic fallback rows |
|---|---|---|---:|---:|---:|---:|---:|---:|
| `whole_base` | base | whole_transfer | 99.510% | 99.755% | 16.9793 | 15.1816 | 786.3216 | 0 |
| `whole_A` | A | whole_transfer | 99.510% | 99.755% | 16.9793 | 15.1816 | 208.4539 | 0 |
| `whole_sequential` | sequential | whole_transfer | 99.510% | 99.755% | 16.9793 | 15.1816 | 157.0275 | 0 |
| `ablate_base_A_old_0.5` | base | feature_attenuation | 1.225% | 0.000% | 0.0316 | -0.0088 | 204.3692 | 0 |
| `ablate_base_A_old_1.0` | base | feature_attenuation | 0.000% | 0.000% | 0.0218 | -0.0043 | 408.7383 | 0 |
| `ablate_base_sequential_new_0.5` | base | feature_attenuation | 1.716% | 0.000% | 0.0314 | -0.0087 | 199.2771 | 0 |
| `ablate_base_sequential_new_1.0` | base | feature_attenuation | 0.000% | 0.000% | 0.0215 | -0.0042 | 398.5542 | 0 |
| `ablate_base_mixed_old_0.5` | base | feature_attenuation | 1.716% | 0.000% | 0.0319 | -0.0087 | 199.8809 | 0 |
| `ablate_random_base_mixed_old_0.5_0` | base | matched_random_attenuation | 9.314% | 9.559% | 0.0375 | 0.0035 | 199.8809 | 0 |
| `ablate_random_base_mixed_old_0.5_1` | base | matched_random_attenuation | 0.245% | 0.000% | 0.0409 | -0.0136 | 199.8809 | 0 |
| `ablate_random_base_mixed_old_0.5_2` | base | matched_random_attenuation | 5.882% | 2.696% | 0.0267 | -0.0023 | 199.8809 | 0 |
| `ablate_random_base_mixed_old_0.5_3` | base | matched_random_attenuation | 0.000% | 0.000% | 0.0384 | -0.0129 | 199.8809 | 0 |
| `ablate_random_base_mixed_old_0.5_4` | base | matched_random_attenuation | 8.333% | 1.716% | 0.0392 | -0.0128 | 199.8810 | 0 |
| `ablate_random_base_mixed_old_0.5_5` | base | matched_random_attenuation | 16.667% | 6.618% | 0.0324 | -0.0069 | 199.8810 | 0 |
| `ablate_random_base_mixed_old_0.5_6` | base | matched_random_attenuation | 5.147% | 1.716% | 0.0356 | -0.0079 | 199.8809 | 0 |
| `ablate_random_base_mixed_old_0.5_7` | base | matched_random_attenuation | 0.000% | 0.000% | 0.0408 | -0.0130 | 199.8810 | 0 |
| `ablate_base_mixed_old_1.0` | base | feature_attenuation | 0.000% | 0.000% | 0.0224 | -0.0041 | 399.7619 | 0 |
| `ablate_random_base_mixed_old_1.0_0` | base | matched_random_attenuation | 0.000% | 0.000% | 0.0340 | 0.0190 | 399.7619 | 0 |
| `ablate_random_base_mixed_old_1.0_1` | base | matched_random_attenuation | 0.000% | 0.000% | 0.0408 | -0.0136 | 399.7619 | 0 |
| `ablate_random_base_mixed_old_1.0_2` | base | matched_random_attenuation | 3.431% | 2.451% | 0.0136 | 0.0082 | 399.7619 | 0 |
| `ablate_random_base_mixed_old_1.0_3` | base | matched_random_attenuation | 0.000% | 0.000% | 0.0359 | -0.0122 | 399.7619 | 0 |
| `ablate_random_base_mixed_old_1.0_4` | base | matched_random_attenuation | 2.206% | 0.980% | 0.0374 | -0.0120 | 399.7619 | 0 |
| `ablate_random_base_mixed_old_1.0_5` | base | matched_random_attenuation | 7.843% | 3.431% | 0.0234 | 0.0002 | 399.7619 | 0 |
| `ablate_random_base_mixed_old_1.0_6` | base | matched_random_attenuation | 0.000% | 0.000% | 0.0307 | -0.0026 | 399.7619 | 0 |
| `ablate_random_base_mixed_old_1.0_7` | base | matched_random_attenuation | 0.000% | 0.000% | 0.0405 | -0.0124 | 399.7619 | 0 |
| `ablate_base_mixed_new_0.5` | base | feature_attenuation | 1.716% | 0.000% | 0.0314 | -0.0087 | 199.2771 | 0 |
| `ablate_random_base_mixed_new_0.5_0` | base | matched_random_attenuation | 0.000% | 0.000% | 0.0377 | -0.0117 | 199.2771 | 0 |
| `ablate_random_base_mixed_new_0.5_1` | base | matched_random_attenuation | 15.686% | 8.088% | 0.0423 | -0.0127 | 199.2771 | 0 |
| `ablate_random_base_mixed_new_0.5_2` | base | matched_random_attenuation | 5.147% | 2.206% | 0.0365 | -0.0083 | 199.2771 | 0 |
| `ablate_random_base_mixed_new_0.5_3` | base | matched_random_attenuation | 5.882% | 2.696% | 0.0438 | -0.0151 | 199.2771 | 0 |
| `ablate_random_base_mixed_new_0.5_4` | base | matched_random_attenuation | 28.922% | 19.118% | 0.0310 | -0.0075 | 199.2771 | 0 |
| `ablate_random_base_mixed_new_0.5_5` | base | matched_random_attenuation | 31.618% | 24.265% | 0.0405 | -0.0098 | 199.2771 | 0 |
| `ablate_random_base_mixed_new_0.5_6` | base | matched_random_attenuation | 9.804% | 3.186% | 0.0358 | -0.0209 | 199.2771 | 0 |
| `ablate_random_base_mixed_new_0.5_7` | base | matched_random_attenuation | 1.225% | 0.000% | 0.0412 | -0.0141 | 199.2771 | 0 |
| `ablate_base_mixed_new_1.0` | base | feature_attenuation | 0.000% | 0.000% | 0.0215 | -0.0042 | 398.5542 | 0 |
| `ablate_random_base_mixed_new_1.0_0` | base | matched_random_attenuation | 0.000% | 0.000% | 0.0345 | -0.0099 | 398.5542 | 0 |
| `ablate_random_base_mixed_new_1.0_1` | base | matched_random_attenuation | 0.000% | 0.000% | 0.0440 | -0.0119 | 398.5542 | 0 |
| `ablate_random_base_mixed_new_1.0_2` | base | matched_random_attenuation | 0.000% | 0.000% | 0.0318 | -0.0026 | 398.5542 | 0 |
| `ablate_random_base_mixed_new_1.0_3` | base | matched_random_attenuation | 0.000% | 0.000% | 0.0473 | -0.0171 | 398.5542 | 0 |
| `ablate_random_base_mixed_new_1.0_4` | base | matched_random_attenuation | 11.029% | 9.069% | 0.0222 | -0.0020 | 398.5542 | 0 |
| `ablate_random_base_mixed_new_1.0_5` | base | matched_random_attenuation | 26.716% | 24.265% | 0.0401 | -0.0059 | 398.5542 | 0 |
| `ablate_random_base_mixed_new_1.0_6` | base | matched_random_attenuation | 1.225% | 0.490% | 0.0311 | -0.0272 | 398.5542 | 0 |
| `ablate_random_base_mixed_new_1.0_7` | base | matched_random_attenuation | 0.000% | 0.000% | 0.0417 | -0.0149 | 398.5542 | 0 |
| `ablate_base_mixed_frequent_0.5` | base | feature_attenuation | 32.108% | 24.020% | 0.0388 | -0.0128 | 78.3582 | 0 |
| `ablate_base_mixed_frequent_1.0` | base | feature_attenuation | 23.529% | 12.010% | 0.0387 | -0.0127 | 156.7164 | 0 |
| `ablate_A_A_old_0.5` | A | feature_attenuation | 100.000% | 0.000% | 15.2105 | -13.9891 | 158.4886 | 0 |
| `ablate_A_A_old_1.0` | A | feature_attenuation | 90.931% | 0.245% | 11.7459 | -10.8676 | 316.9772 | 0 |
| `ablate_A_sequential_new_0.5` | A | feature_attenuation | 100.000% | 0.000% | 15.3757 | -14.1351 | 152.2899 | 0 |
| `ablate_A_sequential_new_1.0` | A | feature_attenuation | 94.853% | 0.245% | 12.0498 | -11.1393 | 304.5798 | 0 |
| `ablate_A_mixed_old_0.5` | A | feature_attenuation | 100.000% | 0.000% | 15.3589 | -14.1182 | 153.1436 | 0 |
| `ablate_random_A_mixed_old_0.5_0` | A | matched_random_attenuation | 100.000% | 0.000% | 16.7661 | -15.3434 | 153.1435 | 0 |
| `ablate_random_A_mixed_old_0.5_1` | A | matched_random_attenuation | 100.000% | 0.000% | 17.4556 | -16.0370 | 153.1436 | 0 |
| `ablate_random_A_mixed_old_0.5_2` | A | matched_random_attenuation | 100.000% | 0.000% | 16.5642 | -15.2341 | 153.1436 | 0 |
| `ablate_random_A_mixed_old_0.5_3` | A | matched_random_attenuation | 100.000% | 0.000% | 17.5163 | -16.1194 | 153.1435 | 0 |
| `ablate_random_A_mixed_old_0.5_4` | A | matched_random_attenuation | 100.000% | 0.000% | 16.5722 | -15.2628 | 153.1435 | 0 |
| `ablate_random_A_mixed_old_0.5_5` | A | matched_random_attenuation | 100.000% | 0.000% | 16.7231 | -15.4130 | 153.1436 | 0 |
| `ablate_random_A_mixed_old_0.5_6` | A | matched_random_attenuation | 100.000% | 0.000% | 16.5255 | -15.1768 | 153.1435 | 0 |
| `ablate_random_A_mixed_old_0.5_7` | A | matched_random_attenuation | 99.510% | 0.000% | 17.4073 | -15.9903 | 153.1436 | 0 |
| `ablate_A_mixed_old_1.0` | A | feature_attenuation | 95.098% | 0.245% | 12.0225 | -11.1158 | 306.2871 | 0 |
| `ablate_random_A_mixed_old_1.0_0` | A | matched_random_attenuation | 100.000% | 0.245% | 13.9331 | -12.8099 | 306.2871 | 0 |
| `ablate_random_A_mixed_old_1.0_1` | A | matched_random_attenuation | 87.010% | 0.245% | 14.8292 | -13.7393 | 306.2871 | 0 |
| `ablate_random_A_mixed_old_1.0_2` | A | matched_random_attenuation | 99.020% | 0.490% | 13.6367 | -12.6323 | 306.2871 | 0 |
| `ablate_random_A_mixed_old_1.0_3` | A | matched_random_attenuation | 86.029% | 0.000% | 14.9031 | -13.8404 | 306.2871 | 0 |
| `ablate_random_A_mixed_old_1.0_4` | A | matched_random_attenuation | 100.000% | 0.735% | 13.7286 | -12.7412 | 306.2871 | 0 |
| `ablate_random_A_mixed_old_1.0_5` | A | matched_random_attenuation | 99.265% | 0.980% | 13.8245 | -12.8536 | 306.2871 | 0 |
| `ablate_random_A_mixed_old_1.0_6` | A | matched_random_attenuation | 100.000% | 0.245% | 13.6802 | -12.6406 | 306.2871 | 0 |
| `ablate_random_A_mixed_old_1.0_7` | A | matched_random_attenuation | 69.118% | 0.000% | 14.7830 | -13.6816 | 306.2871 | 0 |
| `ablate_A_mixed_new_0.5` | A | feature_attenuation | 100.000% | 0.000% | 15.3757 | -14.1351 | 152.2899 | 0 |
| `ablate_random_A_mixed_new_0.5_0` | A | matched_random_attenuation | 100.000% | 0.000% | 17.4005 | -15.9980 | 152.2899 | 0 |
| `ablate_random_A_mixed_new_0.5_1` | A | matched_random_attenuation | 100.000% | 0.000% | 17.4098 | -16.0260 | 152.2899 | 0 |
| `ablate_random_A_mixed_new_0.5_2` | A | matched_random_attenuation | 100.000% | 0.000% | 17.5102 | -16.1180 | 152.2899 | 0 |
| `ablate_random_A_mixed_new_0.5_3` | A | matched_random_attenuation | 100.000% | 0.000% | 17.5451 | -16.1119 | 152.2899 | 0 |
| `ablate_random_A_mixed_new_0.5_4` | A | matched_random_attenuation | 100.000% | 0.000% | 16.5958 | -15.2835 | 152.2899 | 0 |
| `ablate_random_A_mixed_new_0.5_5` | A | matched_random_attenuation | 100.000% | 0.000% | 16.8375 | -15.5078 | 152.2899 | 0 |
| `ablate_random_A_mixed_new_0.5_6` | A | matched_random_attenuation | 100.000% | 0.245% | 16.5639 | -15.1958 | 152.2899 | 0 |
| `ablate_random_A_mixed_new_0.5_7` | A | matched_random_attenuation | 100.000% | 0.000% | 17.7216 | -16.3221 | 152.2899 | 0 |
| `ablate_A_mixed_new_1.0` | A | feature_attenuation | 94.853% | 0.245% | 12.0498 | -11.1393 | 304.5798 | 0 |
| `ablate_random_A_mixed_new_1.0_0` | A | matched_random_attenuation | 95.343% | 0.245% | 14.8087 | -13.7081 | 304.5798 | 0 |
| `ablate_random_A_mixed_new_1.0_1` | A | matched_random_attenuation | 89.216% | 0.245% | 14.7830 | -13.7132 | 304.5798 | 0 |
| `ablate_random_A_mixed_new_1.0_2` | A | matched_random_attenuation | 90.686% | 0.245% | 14.9065 | -13.8360 | 304.5798 | 0 |
| `ablate_random_A_mixed_new_1.0_3` | A | matched_random_attenuation | 70.343% | 0.000% | 14.9804 | -13.8498 | 304.5798 | 0 |
| `ablate_random_A_mixed_new_1.0_4` | A | matched_random_attenuation | 99.755% | 0.490% | 13.7492 | -12.7645 | 304.5798 | 0 |
| `ablate_random_A_mixed_new_1.0_5` | A | matched_random_attenuation | 99.755% | 0.245% | 14.0497 | -13.0392 | 304.5798 | 0 |
| `ablate_random_A_mixed_new_1.0_6` | A | matched_random_attenuation | 100.000% | 0.490% | 13.7200 | -12.6631 | 304.5798 | 0 |
| `ablate_random_A_mixed_new_1.0_7` | A | matched_random_attenuation | 86.029% | 0.000% | 15.2125 | -14.1406 | 304.5798 | 0 |
| `ablate_A_mixed_frequent_0.5` | A | feature_attenuation | 100.000% | 0.000% | 17.5739 | -16.0987 | 68.6772 | 0 |
| `ablate_A_mixed_frequent_1.0` | A | feature_attenuation | 100.000% | 0.000% | 17.1360 | -15.7337 | 137.3545 | 0 |
| `ablate_sequential_A_old_0.5` | sequential | feature_attenuation | 0.000% | 99.755% | -12.9956 | 13.3749 | 161.6823 | 0 |
| `ablate_sequential_A_old_1.0` | sequential | feature_attenuation | 0.000% | 68.627% | -9.5483 | 9.8049 | 323.3645 | 0 |
| `ablate_sequential_sequential_new_0.5` | sequential | feature_attenuation | 0.000% | 99.755% | -13.1352 | 13.5217 | 155.7932 | 0 |
| `ablate_sequential_sequential_new_1.0` | sequential | feature_attenuation | 0.000% | 72.059% | -9.7919 | 10.0541 | 311.5864 | 0 |
| `ablate_sequential_mixed_old_0.5` | sequential | feature_attenuation | 0.000% | 99.755% | -13.1115 | 13.4911 | 156.7645 | 0 |
| `ablate_random_sequential_mixed_old_0.5_0` | sequential | matched_random_attenuation | 0.000% | 99.755% | -14.1057 | 14.5130 | 156.7645 | 0 |
| `ablate_random_sequential_mixed_old_0.5_1` | sequential | matched_random_attenuation | 0.000% | 100.000% | -14.6959 | 15.0750 | 156.7645 | 0 |
| `ablate_random_sequential_mixed_old_0.5_2` | sequential | matched_random_attenuation | 0.000% | 99.755% | -14.1186 | 14.5101 | 156.7645 | 0 |
| `ablate_random_sequential_mixed_old_0.5_3` | sequential | matched_random_attenuation | 0.000% | 99.755% | -14.7009 | 15.1169 | 156.7645 | 0 |
| `ablate_random_sequential_mixed_old_0.5_4` | sequential | matched_random_attenuation | 0.000% | 100.000% | -14.0008 | 14.4339 | 156.7645 | 0 |
| `ablate_random_sequential_mixed_old_0.5_5` | sequential | matched_random_attenuation | 0.000% | 100.000% | -14.2975 | 14.7020 | 156.7645 | 0 |
| `ablate_random_sequential_mixed_old_0.5_6` | sequential | matched_random_attenuation | 0.000% | 100.000% | -13.9394 | 14.3756 | 156.7645 | 0 |
| `ablate_random_sequential_mixed_old_0.5_7` | sequential | matched_random_attenuation | 0.000% | 99.020% | -14.6468 | 15.0410 | 156.7645 | 0 |
| `ablate_sequential_mixed_old_1.0` | sequential | feature_attenuation | 0.000% | 72.794% | -9.7522 | 10.0125 | 313.5290 | 0 |
| `ablate_random_sequential_mixed_old_1.0_0` | sequential | matched_random_attenuation | 1.225% | 93.873% | -11.0521 | 11.3111 | 313.5290 | 0 |
| `ablate_random_sequential_mixed_old_1.0_1` | sequential | matched_random_attenuation | 0.000% | 71.078% | -11.7658 | 12.0087 | 313.5290 | 0 |
| `ablate_random_sequential_mixed_old_1.0_2` | sequential | matched_random_attenuation | 1.225% | 96.324% | -11.0973 | 11.3434 | 313.5290 | 0 |
| `ablate_random_sequential_mixed_old_1.0_3` | sequential | matched_random_attenuation | 0.000% | 53.922% | -11.7543 | 12.0306 | 313.5290 | 0 |
| `ablate_random_sequential_mixed_old_1.0_4` | sequential | matched_random_attenuation | 0.980% | 98.529% | -11.0047 | 11.3140 | 313.5290 | 0 |
| `ablate_random_sequential_mixed_old_1.0_5` | sequential | matched_random_attenuation | 0.735% | 98.775% | -11.3375 | 11.6134 | 313.5290 | 0 |
| `ablate_random_sequential_mixed_old_1.0_6` | sequential | matched_random_attenuation | 0.490% | 96.078% | -10.9536 | 11.2537 | 313.5290 | 0 |
| `ablate_random_sequential_mixed_old_1.0_7` | sequential | matched_random_attenuation | 0.000% | 38.971% | -11.7067 | 11.9524 | 313.5290 | 0 |
| `ablate_sequential_mixed_new_0.5` | sequential | feature_attenuation | 0.000% | 99.755% | -13.1352 | 13.5217 | 155.7932 | 0 |
| `ablate_random_sequential_mixed_new_0.5_0` | sequential | matched_random_attenuation | 0.000% | 100.000% | -14.6917 | 15.1001 | 155.7932 | 0 |
| `ablate_random_sequential_mixed_new_0.5_1` | sequential | matched_random_attenuation | 0.000% | 99.755% | -14.6562 | 15.0555 | 155.7932 | 0 |
| `ablate_random_sequential_mixed_new_0.5_2` | sequential | matched_random_attenuation | 0.000% | 99.755% | -14.8324 | 15.2007 | 155.7932 | 0 |
| `ablate_random_sequential_mixed_new_0.5_3` | sequential | matched_random_attenuation | 0.000% | 99.755% | -14.8276 | 15.2075 | 155.7932 | 0 |
| `ablate_random_sequential_mixed_new_0.5_4` | sequential | matched_random_attenuation | 0.000% | 100.000% | -13.9780 | 14.3950 | 155.7932 | 0 |
| `ablate_random_sequential_mixed_new_0.5_5` | sequential | matched_random_attenuation | 0.000% | 99.755% | -14.2024 | 14.6621 | 155.7932 | 0 |
| `ablate_random_sequential_mixed_new_0.5_6` | sequential | matched_random_attenuation | 0.000% | 100.000% | -14.0448 | 14.4769 | 155.7932 | 0 |
| `ablate_random_sequential_mixed_new_0.5_7` | sequential | matched_random_attenuation | 0.000% | 100.000% | -14.9382 | 15.3113 | 155.7932 | 0 |
| `ablate_sequential_mixed_new_1.0` | sequential | feature_attenuation | 0.000% | 72.059% | -9.7919 | 10.0541 | 311.5864 | 0 |
| `ablate_random_sequential_mixed_new_1.0_0` | sequential | matched_random_attenuation | 0.245% | 72.549% | -11.8623 | 12.1335 | 311.5863 | 0 |
| `ablate_random_sequential_mixed_new_1.0_1` | sequential | matched_random_attenuation | 0.245% | 67.402% | -11.7783 | 12.0371 | 311.5864 | 0 |
| `ablate_random_sequential_mixed_new_1.0_2` | sequential | matched_random_attenuation | 0.000% | 68.137% | -11.9871 | 12.2103 | 311.5863 | 0 |
| `ablate_random_sequential_mixed_new_1.0_3` | sequential | matched_random_attenuation | 0.000% | 48.039% | -11.9584 | 12.1925 | 311.5863 | 0 |
| `ablate_random_sequential_mixed_new_1.0_4` | sequential | matched_random_attenuation | 0.245% | 99.265% | -11.0028 | 11.3013 | 311.5864 | 0 |
| `ablate_random_sequential_mixed_new_1.0_5` | sequential | matched_random_attenuation | 0.735% | 98.775% | -11.2241 | 11.5497 | 311.5864 | 0 |
| `ablate_random_sequential_mixed_new_1.0_6` | sequential | matched_random_attenuation | 0.000% | 100.000% | -11.0464 | 11.3389 | 311.5864 | 0 |
| `ablate_random_sequential_mixed_new_1.0_7` | sequential | matched_random_attenuation | 0.000% | 59.069% | -12.0641 | 12.2845 | 311.5864 | 0 |
| `ablate_sequential_mixed_frequent_0.5` | sequential | feature_attenuation | 0.000% | 100.000% | -15.2287 | 15.7129 | 68.1678 | 0 |
| `ablate_sequential_mixed_frequent_1.0` | sequential | feature_attenuation | 0.000% | 100.000% | -14.7105 | 15.1727 | 136.3355 | 0 |
| `ablate_mixed_A_old_0.5` | mixed | feature_attenuation | 99.020% | 99.510% | 14.5309 | 13.1555 | 161.5330 | 0 |
| `ablate_mixed_A_old_1.0` | mixed | feature_attenuation | 39.461% | 66.667% | 10.4667 | 9.6686 | 323.0659 | 0 |
| `ablate_mixed_sequential_new_0.5` | mixed | feature_attenuation | 99.265% | 99.755% | 14.7076 | 13.2966 | 155.5051 | 0 |
| `ablate_mixed_sequential_new_1.0` | mixed | feature_attenuation | 46.569% | 71.078% | 10.7480 | 9.9057 | 311.0101 | 0 |
| `ablate_mixed_mixed_old_0.5` | mixed | feature_attenuation | 99.265% | 99.755% | 14.6885 | 13.2642 | 156.4843 | 0 |
| `ablate_random_mixed_mixed_old_0.5_0` | mixed | matched_random_attenuation | 99.020% | 98.775% | 15.8086 | 14.2550 | 156.4843 | 0 |
| `ablate_random_mixed_mixed_old_0.5_1` | mixed | matched_random_attenuation | 99.020% | 98.775% | 16.1309 | 14.9142 | 156.4843 | 0 |
| `ablate_random_mixed_mixed_old_0.5_2` | mixed | matched_random_attenuation | 99.020% | 99.265% | 15.5998 | 14.1742 | 156.4843 | 0 |
| `ablate_random_mixed_mixed_old_0.5_3` | mixed | matched_random_attenuation | 99.020% | 99.020% | 16.2453 | 15.0185 | 156.4843 | 0 |
| `ablate_random_mixed_mixed_old_0.5_4` | mixed | matched_random_attenuation | 99.510% | 99.510% | 15.5558 | 14.1775 | 156.4843 | 0 |
| `ablate_random_mixed_mixed_old_0.5_5` | mixed | matched_random_attenuation | 99.265% | 99.755% | 15.5969 | 14.4332 | 156.4843 | 0 |
| `ablate_random_mixed_mixed_old_0.5_6` | mixed | matched_random_attenuation | 99.020% | 99.510% | 15.4836 | 14.1610 | 156.4843 | 0 |
| `ablate_random_mixed_mixed_old_0.5_7` | mixed | matched_random_attenuation | 95.098% | 97.304% | 16.1267 | 14.8782 | 156.4843 | 0 |
| `ablate_mixed_mixed_old_1.0` | mixed | feature_attenuation | 46.569% | 70.343% | 10.7193 | 9.8616 | 312.9685 | 0 |
| `ablate_random_mixed_mixed_old_1.0_0` | mixed | matched_random_attenuation | 75.000% | 91.176% | 11.8995 | 11.0801 | 312.9685 | 0 |
| `ablate_random_mixed_mixed_old_1.0_1` | mixed | matched_random_attenuation | 61.275% | 70.588% | 12.2522 | 11.8826 | 312.9685 | 0 |
| `ablate_random_mixed_mixed_old_1.0_2` | mixed | matched_random_attenuation | 93.873% | 94.853% | 11.6558 | 10.9964 | 312.9685 | 0 |
| `ablate_random_mixed_mixed_old_1.0_3` | mixed | matched_random_attenuation | 36.765% | 59.069% | 12.3756 | 11.9763 | 312.9685 | 0 |
| `ablate_random_mixed_mixed_old_1.0_4` | mixed | matched_random_attenuation | 98.529% | 98.529% | 11.6870 | 11.0706 | 312.9685 | 0 |
| `ablate_random_mixed_mixed_old_1.0_5` | mixed | matched_random_attenuation | 97.549% | 98.284% | 11.6673 | 11.3689 | 312.9685 | 0 |
| `ablate_random_mixed_mixed_old_1.0_6` | mixed | matched_random_attenuation | 74.510% | 94.853% | 11.6001 | 11.0729 | 312.9685 | 0 |
| `ablate_random_mixed_mixed_old_1.0_7` | mixed | matched_random_attenuation | 12.010% | 46.814% | 12.2892 | 11.8330 | 312.9685 | 0 |
| `ablate_mixed_mixed_new_0.5` | mixed | feature_attenuation | 99.265% | 99.755% | 14.7076 | 13.2966 | 155.5051 | 0 |
| `ablate_random_mixed_mixed_new_0.5_0` | mixed | matched_random_attenuation | 99.265% | 99.265% | 15.9789 | 14.9180 | 155.5051 | 0 |
| `ablate_random_mixed_mixed_new_0.5_1` | mixed | matched_random_attenuation | 98.284% | 98.775% | 15.9579 | 14.9299 | 155.5051 | 0 |
| `ablate_random_mixed_mixed_new_0.5_2` | mixed | matched_random_attenuation | 98.775% | 98.775% | 16.0039 | 15.0082 | 155.5051 | 0 |
| `ablate_random_mixed_mixed_new_0.5_3` | mixed | matched_random_attenuation | 96.324% | 98.039% | 16.2083 | 15.0179 | 155.5051 | 0 |
| `ablate_random_mixed_mixed_new_0.5_4` | mixed | matched_random_attenuation | 99.265% | 99.265% | 15.4096 | 14.0834 | 155.5051 | 0 |
| `ablate_random_mixed_mixed_new_0.5_5` | mixed | matched_random_attenuation | 98.775% | 99.020% | 15.7954 | 14.4813 | 155.5051 | 0 |
| `ablate_random_mixed_mixed_new_0.5_6` | mixed | matched_random_attenuation | 99.510% | 99.510% | 15.6457 | 14.1603 | 155.5051 | 0 |
| `ablate_random_mixed_mixed_new_0.5_7` | mixed | matched_random_attenuation | 98.529% | 98.775% | 16.5035 | 15.1927 | 155.5051 | 0 |
| `ablate_mixed_mixed_new_1.0` | mixed | feature_attenuation | 46.569% | 71.078% | 10.7480 | 9.9057 | 311.0101 | 0 |
| `ablate_random_mixed_mixed_new_1.0_0` | mixed | matched_random_attenuation | 66.912% | 72.059% | 12.1703 | 11.9699 | 311.0101 | 0 |
| `ablate_random_mixed_mixed_new_1.0_1` | mixed | matched_random_attenuation | 48.529% | 69.118% | 12.0934 | 11.9532 | 311.0101 | 0 |
| `ablate_random_mixed_mixed_new_1.0_2` | mixed | matched_random_attenuation | 43.873% | 67.892% | 12.1098 | 12.0418 | 311.0101 | 0 |
| `ablate_random_mixed_mixed_new_1.0_3` | mixed | matched_random_attenuation | 34.314% | 56.618% | 12.3778 | 12.0408 | 311.0101 | 0 |
| `ablate_random_mixed_mixed_new_1.0_4` | mixed | matched_random_attenuation | 98.529% | 98.775% | 11.5302 | 11.0045 | 311.0101 | 0 |
| `ablate_random_mixed_mixed_new_1.0_5` | mixed | matched_random_attenuation | 97.304% | 98.039% | 11.9912 | 11.4285 | 311.0101 | 0 |
| `ablate_random_mixed_mixed_new_1.0_6` | mixed | matched_random_attenuation | 98.775% | 98.529% | 11.8256 | 11.0468 | 311.0101 | 0 |
| `ablate_random_mixed_mixed_new_1.0_7` | mixed | matched_random_attenuation | 45.833% | 61.275% | 12.6881 | 12.1981 | 311.0101 | 0 |
| `ablate_mixed_mixed_frequent_0.5` | mixed | feature_attenuation | 99.510% | 99.755% | 17.1751 | 15.3736 | 67.3559 | 0 |
| `ablate_mixed_mixed_frequent_1.0` | mixed | feature_attenuation | 99.510% | 98.775% | 16.3548 | 14.8110 | 134.7117 | 0 |
| `patch_base_mixed_old` | base | feature_transfer | 37.255% | 41.912% | 0.6863 | 0.8466 | 290.3037 | 0 |
| `patch_random_base_mixed_old_0` | base | matched_random_transfer | 39.461% | 22.304% | 0.4218 | 0.4499 | 290.3037 | 0 |
| `patch_random_base_mixed_old_1` | base | matched_random_transfer | 0.000% | 0.000% | 0.1488 | 0.0860 | 290.3037 | 0 |
| `patch_random_base_mixed_old_2` | base | matched_random_transfer | 48.529% | 40.686% | 0.5212 | 0.4739 | 290.3037 | 0 |
| `patch_random_base_mixed_old_3` | base | matched_random_transfer | 0.000% | 0.000% | 0.1350 | 0.1039 | 290.3037 | 0 |
| `patch_random_base_mixed_old_4` | base | matched_random_transfer | 40.931% | 33.088% | 0.1868 | 0.1179 | 290.3037 | 0 |
| `patch_random_base_mixed_old_5` | base | matched_random_transfer | 31.373% | 25.735% | 0.1902 | 0.0900 | 290.3038 | 0 |
| `patch_random_base_mixed_old_6` | base | matched_random_transfer | 26.716% | 12.745% | 0.3665 | 0.2460 | 290.3037 | 0 |
| `patch_random_base_mixed_old_7` | base | matched_random_transfer | 0.000% | 0.000% | 0.1385 | 0.1023 | 290.3037 | 0 |
| `patch_base_mixed_new` | base | feature_transfer | 37.010% | 41.912% | 0.7020 | 0.8489 | 290.5627 | 0 |
| `patch_random_base_mixed_new_0` | base | matched_random_transfer | 0.000% | 0.000% | 0.1287 | 0.0471 | 290.5627 | 0 |
| `patch_random_base_mixed_new_1` | base | matched_random_transfer | 12.255% | 12.745% | 0.1568 | 0.0539 | 290.5627 | 0 |
| `patch_random_base_mixed_new_2` | base | matched_random_transfer | 1.961% | 1.961% | 0.1625 | 0.0625 | 290.5627 | 0 |
| `patch_random_base_mixed_new_3` | base | matched_random_transfer | 5.392% | 2.451% | 0.1341 | 0.0425 | 290.5627 | 0 |
| `patch_random_base_mixed_new_4` | base | matched_random_transfer | 42.157% | 38.971% | 0.5372 | 0.3650 | 290.5627 | 0 |
| `patch_random_base_mixed_new_5` | base | matched_random_transfer | 42.157% | 34.559% | 0.1434 | 0.1075 | 290.5627 | 0 |
| `patch_random_base_mixed_new_6` | base | matched_random_transfer | 33.824% | 33.088% | 0.3981 | 0.4109 | 290.5627 | 0 |
| `patch_random_base_mixed_new_7` | base | matched_random_transfer | 4.167% | 2.941% | 0.1238 | 0.0860 | 290.5627 | 0 |
| `patch_A_mixed_old` | A | feature_transfer | 100.000% | 0.000% | 16.9351 | -12.8293 | 38.8251 | 0 |
| `patch_random_A_mixed_old_0` | A | matched_random_transfer | 100.000% | 0.000% | 17.3804 | -15.3384 | 38.8251 | 0 |
| `patch_random_A_mixed_old_1` | A | matched_random_transfer | 100.000% | 0.000% | 17.5445 | -15.5402 | 38.8251 | 0 |
| `patch_random_A_mixed_old_2` | A | matched_random_transfer | 100.000% | 0.000% | 17.2861 | -15.0811 | 38.8251 | 0 |
| `patch_random_A_mixed_old_3` | A | matched_random_transfer | 100.000% | 0.000% | 17.5485 | -15.4839 | 38.8251 | 0 |
| `patch_random_A_mixed_old_4` | A | matched_random_transfer | 100.000% | 0.000% | 17.3951 | -15.3878 | 38.8251 | 0 |
| `patch_random_A_mixed_old_5` | A | matched_random_transfer | 100.000% | 0.000% | 17.3382 | -15.3031 | 38.8251 | 0 |
| `patch_random_A_mixed_old_6` | A | matched_random_transfer | 100.000% | 0.000% | 17.3968 | -15.4570 | 38.8251 | 0 |
| `patch_random_A_mixed_old_7` | A | matched_random_transfer | 100.000% | 0.000% | 17.5319 | -15.5187 | 38.8251 | 0 |
| `patch_A_mixed_new` | A | feature_transfer | 100.000% | 0.000% | 16.9442 | -12.8024 | 38.8876 | 0 |
| `patch_random_A_mixed_new_0` | A | matched_random_transfer | 100.000% | 0.000% | 17.5481 | -15.6192 | 38.8876 | 0 |
| `patch_random_A_mixed_new_1` | A | matched_random_transfer | 100.000% | 0.000% | 17.5595 | -15.5440 | 38.8876 | 0 |
| `patch_random_A_mixed_new_2` | A | matched_random_transfer | 100.000% | 0.000% | 17.5885 | -15.5907 | 38.8876 | 0 |
| `patch_random_A_mixed_new_3` | A | matched_random_transfer | 100.000% | 0.000% | 17.5699 | -15.6345 | 38.8876 | 0 |
| `patch_random_A_mixed_new_4` | A | matched_random_transfer | 100.000% | 0.000% | 17.4342 | -15.3863 | 38.8876 | 0 |
| `patch_random_A_mixed_new_5` | A | matched_random_transfer | 100.000% | 0.000% | 17.3685 | -15.4043 | 38.8876 | 0 |
| `patch_random_A_mixed_new_6` | A | matched_random_transfer | 100.000% | 0.000% | 17.3366 | -15.2730 | 38.8876 | 0 |
| `patch_random_A_mixed_new_7` | A | matched_random_transfer | 100.000% | 0.000% | 17.5526 | -15.5283 | 38.8876 | 0 |
| `patch_sequential_mixed_old` | sequential | feature_transfer | 0.000% | 100.000% | -11.9701 | 15.2516 | 26.9788 | 0 |
| `patch_random_sequential_mixed_old_0` | sequential | matched_random_transfer | 0.000% | 100.000% | -14.4390 | 15.4534 | 26.9788 | 0 |
| `patch_random_sequential_mixed_old_1` | sequential | matched_random_transfer | 0.000% | 100.000% | -14.6767 | 15.4180 | 26.9788 | 0 |
| `patch_random_sequential_mixed_old_2` | sequential | matched_random_transfer | 0.000% | 100.000% | -14.2827 | 15.4591 | 26.9788 | 0 |
| `patch_random_sequential_mixed_old_3` | sequential | matched_random_transfer | 0.000% | 100.000% | -14.5780 | 15.3955 | 26.9788 | 0 |
| `patch_random_sequential_mixed_old_4` | sequential | matched_random_transfer | 0.000% | 100.000% | -14.5281 | 15.4593 | 26.9788 | 0 |
| `patch_random_sequential_mixed_old_5` | sequential | matched_random_transfer | 0.000% | 100.000% | -14.4169 | 15.4288 | 26.9788 | 0 |
| `patch_random_sequential_mixed_old_6` | sequential | matched_random_transfer | 0.000% | 100.000% | -14.5255 | 15.4291 | 26.9788 | 0 |
| `patch_random_sequential_mixed_old_7` | sequential | matched_random_transfer | 0.000% | 100.000% | -14.6597 | 15.4027 | 26.9788 | 0 |
| `patch_sequential_mixed_new` | sequential | feature_transfer | 0.000% | 100.000% | -11.9269 | 15.2476 | 27.0443 | 0 |
| `patch_random_sequential_mixed_new_0` | sequential | matched_random_transfer | 0.000% | 100.000% | -14.7435 | 15.4226 | 27.0443 | 0 |
| `patch_random_sequential_mixed_new_1` | sequential | matched_random_transfer | 0.000% | 100.000% | -14.6328 | 15.3953 | 27.0443 | 0 |
| `patch_random_sequential_mixed_new_2` | sequential | matched_random_transfer | 0.000% | 100.000% | -14.6411 | 15.4105 | 27.0443 | 0 |
| `patch_random_sequential_mixed_new_3` | sequential | matched_random_transfer | 0.000% | 100.000% | -14.8335 | 15.4205 | 27.0443 | 0 |
| `patch_random_sequential_mixed_new_4` | sequential | matched_random_transfer | 0.000% | 100.000% | -14.4077 | 15.4794 | 27.0443 | 0 |
| `patch_random_sequential_mixed_new_5` | sequential | matched_random_transfer | 0.000% | 100.000% | -14.5454 | 15.4195 | 27.0443 | 0 |
| `patch_random_sequential_mixed_new_6` | sequential | matched_random_transfer | 0.000% | 100.000% | -14.4041 | 15.4609 | 27.0443 | 0 |
| `patch_random_sequential_mixed_new_7` | sequential | matched_random_transfer | 0.000% | 100.000% | -14.7195 | 15.4010 | 27.0443 | 0 |
| `raw_rank1` | sequential | raw_state_difference_transfer | 0.245% | 100.000% | -15.3570 | 16.0399 | 84.9401 | 0 |
| `raw_random_rank1_0` | sequential | random_subspace_transfer | 0.000% | 100.000% | -14.2574 | 15.1877 | 84.9401 | 0 |
| `raw_random_rank1_1` | sequential | random_subspace_transfer | 0.000% | 100.000% | -14.2484 | 15.0871 | 84.9401 | 0 |
| `raw_random_rank1_2` | sequential | random_subspace_transfer | 0.000% | 100.000% | -14.0180 | 15.0170 | 84.9401 | 0 |
| `raw_random_rank1_3` | sequential | random_subspace_transfer | 0.000% | 100.000% | -14.1324 | 15.0258 | 84.9401 | 0 |
| `raw_random_rank1_4` | sequential | random_subspace_transfer | 0.000% | 100.000% | -14.0283 | 14.8581 | 84.9401 | 0 |
| `raw_random_rank1_5` | sequential | random_subspace_transfer | 0.000% | 100.000% | -14.2574 | 15.1383 | 84.9401 | 0 |
| `raw_random_rank1_6` | sequential | random_subspace_transfer | 0.000% | 100.000% | -14.1417 | 15.1444 | 84.9401 | 0 |
| `raw_random_rank1_7` | sequential | random_subspace_transfer | 0.000% | 100.000% | -13.9913 | 14.9250 | 84.9401 | 0 |
| `raw_rank4` | sequential | raw_state_difference_transfer | 15.931% | 100.000% | -6.4792 | 15.4289 | 111.1415 | 0 |
| `raw_random_rank4_0` | sequential | random_subspace_transfer | 0.000% | 100.000% | -13.3267 | 14.7551 | 111.1415 | 0 |
| `raw_random_rank4_1` | sequential | random_subspace_transfer | 0.000% | 100.000% | -12.4969 | 14.7560 | 111.1415 | 0 |
| `raw_random_rank4_2` | sequential | random_subspace_transfer | 0.000% | 100.000% | -13.0706 | 14.7619 | 111.1415 | 0 |
| `raw_random_rank4_3` | sequential | random_subspace_transfer | 0.245% | 100.000% | -12.5808 | 14.8160 | 111.1415 | 0 |
| `raw_random_rank4_4` | sequential | random_subspace_transfer | 0.245% | 100.000% | -12.7063 | 14.7276 | 111.1415 | 0 |
| `raw_random_rank4_5` | sequential | random_subspace_transfer | 0.000% | 100.000% | -13.0498 | 15.0210 | 111.1415 | 0 |
| `raw_random_rank4_6` | sequential | random_subspace_transfer | 0.000% | 100.000% | -12.9851 | 14.9064 | 111.1415 | 0 |
| `raw_random_rank4_7` | sequential | random_subspace_transfer | 0.000% | 100.000% | -12.9449 | 14.8857 | 111.1415 | 0 |
| `raw_rank16` | sequential | raw_state_difference_transfer | 80.882% | 98.284% | 7.2218 | 14.1894 | 134.4864 | 0 |
| `raw_random_rank16_0` | sequential | random_subspace_transfer | 0.245% | 100.000% | -11.2146 | 14.8080 | 134.4865 | 0 |
| `raw_random_rank16_1` | sequential | random_subspace_transfer | 0.000% | 100.000% | -10.7426 | 14.9415 | 134.4864 | 0 |
| `raw_random_rank16_2` | sequential | random_subspace_transfer | 0.000% | 100.000% | -11.3872 | 14.6576 | 134.4864 | 0 |
| `raw_random_rank16_3` | sequential | random_subspace_transfer | 0.000% | 100.000% | -10.6332 | 14.6870 | 134.4864 | 0 |
| `raw_random_rank16_4` | sequential | random_subspace_transfer | 0.245% | 100.000% | -10.8516 | 14.8384 | 134.4864 | 0 |
| `raw_random_rank16_5` | sequential | random_subspace_transfer | 0.245% | 100.000% | -10.0878 | 14.6835 | 134.4864 | 0 |
| `raw_random_rank16_6` | sequential | random_subspace_transfer | 0.000% | 100.000% | -9.4276 | 14.6606 | 134.4864 | 0 |
| `raw_random_rank16_7` | sequential | random_subspace_transfer | 0.245% | 100.000% | -10.3446 | 14.8973 | 134.4864 | 0 |
| `raw_rank16_complement` | sequential | raw_complement_transfer | 12.010% | 100.000% | -7.0434 | 16.4590 | 80.2137 | 0 |

## 精确来源

- [behavior.json](../../../../../../../../UNAVAILABLE.md) — SHA256 `b0b0f6ea456bc7256c3c661cebdc2b56528e51c2b30ce36ec5ddc313a2d1361f`.
- [qualification.json](../../../../../../../../UNAVAILABLE.md) — SHA256 `9a87bf4afb2f684fd779407610d6c5fc2993adab30a75ee1a5098ac3594d3834`.
- [primary_results.json](../../../../../../../../UNAVAILABLE.md) — SHA256 `68c946cb7ed56e2e40f5548013b885e85ac3d0a7a1cc6908ca7ddfc7e3406bcc`.
- [intervention_summary.json](../../../../../../../../UNAVAILABLE.md) — SHA256 `ed13039a6d1bd532d9df24320d3f231d8085814d95e69e16d0da193c3a7f8135`.
- [geometry.json](../../../../../../../../UNAVAILABLE.md) — SHA256 `697bc0de184b63a605557c866a8824f994ce26c40f1ed378d7d7e2a6c3abfa29`.
- [selection_frozen.json](../../../../../../../../UNAVAILABLE.md) — SHA256 `14a2ec1bb2b302a154ade257c9999c8bd03d3238e7888caf9c6a3caecc12124b`.
- [analysis_receipt.json](../../../../../../../../UNAVAILABLE.md) — SHA256 `21ac7775cb10e9f054b981cfb895983db1892891596119420143ec388c7d5b74`.
- [interventions.pt](../../../../../../../../UNAVAILABLE.md) — SHA256 `7a2355e4f733deecd3871a4f58fd7824fe67449a582cb62ba20ba7c5e38179b2`.
