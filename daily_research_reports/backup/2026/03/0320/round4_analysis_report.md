# Round4 Router Denoising 实验详尽报告

## 1. 实验设置

- 输入特征: features_multihead_attn_out.npy
- 输入目录: /data/250010109/GatingMecanism/exp_multihead/results/round1_multihead_layers_4_16_30
- 层(请求): [4, 16, 30]
- 层(实际): [4, 16, 30]
- 层回退映射: []
- 预处理模式: ['train_mean', 'none']
- 标签分布模式: ['balanced', 'imbalanced']
- 不均匀分布衰减: 0.5
- 训练最小类样本: 8
- 低秩r: 16
- seed网格: [42, 43, 44, 45, 46]
- 训练轮数: 50
- 学习率: 0.005
- 优化器: AdamW
- 类别数(专家数): 4

## 2. 三模型整体指标汇总

| label_dist_mode | center_mode | model | test_acc_mean | test_acc_std | load_cv_mean | load_cv_std | mean_ed_mean | mean_ed_std |
|---|---|---|---:|---:|---:|---:|---:|---:|
| balanced | train_mean | full | 0.620747 | 0.073626 | 0.217997 | 0.087750 | 11.702628 | 2.528353 |
| balanced | train_mean | lowrank | 0.620833 | 0.077851 | 0.266008 | 0.142549 | 11.738533 | 2.521146 |
| balanced | train_mean | gated | 0.607205 | 0.074334 | 0.241964 | 0.113361 | 11.819716 | 2.520398 |
| balanced | none | full | 0.618229 | 0.072315 | 0.211950 | 0.088218 | 11.716093 | 2.557701 |
| balanced | none | lowrank | 0.628472 | 0.079789 | 0.225154 | 0.132173 | 11.724118 | 2.553836 |
| balanced | none | gated | 0.614410 | 0.073077 | 0.234587 | 0.099749 | 11.771135 | 2.536059 |
| imbalanced | train_mean | full | 0.467882 | 0.115382 | 0.973773 | 0.403230 | 14.548761 | 3.802265 |
| imbalanced | train_mean | lowrank | 0.511458 | 0.081194 | 0.777077 | 0.272217 | 13.826198 | 3.205893 |
| imbalanced | train_mean | gated | 0.415799 | 0.108966 | 1.177063 | 0.356474 | 16.453897 | 4.733124 |
| imbalanced | none | full | 0.335503 | 0.076238 | 1.484556 | 0.220297 | 17.229803 | 6.437707 |
| imbalanced | none | lowrank | 0.422656 | 0.111914 | 1.189844 | 0.344136 | 15.524098 | 4.658793 |
| imbalanced | none | gated | 0.325000 | 0.074190 | 1.518233 | 0.209500 | 18.117302 | 7.146710 |

## 3. 分层聚合指标

| label_dist_mode | center_mode | layer | model | test_acc_mean | load_cv_mean | mean_ed_mean |
|---|---|---:|---|---:|---:|---:|
| balanced | train_mean | 4 | full | 0.546615 | 0.252571 | 9.417896 |
| balanced | train_mean | 4 | lowrank | 0.539323 | 0.387417 | 9.690403 |
| balanced | train_mean | 4 | gated | 0.536719 | 0.292092 | 9.508868 |
| balanced | train_mean | 16 | full | 0.668750 | 0.171267 | 12.840477 |
| balanced | train_mean | 16 | lowrank | 0.672917 | 0.189317 | 12.687840 |
| balanced | train_mean | 16 | gated | 0.658333 | 0.168322 | 12.877318 |
| balanced | train_mean | 30 | full | 0.646875 | 0.230153 | 12.849512 |
| balanced | train_mean | 30 | lowrank | 0.650260 | 0.221291 | 12.837355 |
| balanced | train_mean | 30 | gated | 0.626563 | 0.265479 | 13.072961 |
| balanced | none | 4 | full | 0.548438 | 0.252364 | 9.423923 |
| balanced | none | 4 | lowrank | 0.549479 | 0.355394 | 9.478841 |
| balanced | none | 4 | gated | 0.544010 | 0.275935 | 9.491787 |
| balanced | none | 16 | full | 0.662760 | 0.170663 | 12.779599 |
| balanced | none | 16 | lowrank | 0.670833 | 0.135211 | 12.789175 |
| balanced | none | 16 | gated | 0.658073 | 0.191817 | 12.851585 |
| balanced | none | 30 | full | 0.643490 | 0.212824 | 12.944758 |
| balanced | none | 30 | lowrank | 0.665104 | 0.184857 | 12.904340 |
| balanced | none | 30 | gated | 0.641146 | 0.236011 | 12.970032 |
| imbalanced | train_mean | 4 | full | 0.324479 | 1.489509 | 12.254847 |
| imbalanced | train_mean | 4 | lowrank | 0.420312 | 1.100210 | 12.106829 |
| imbalanced | train_mean | 4 | gated | 0.276823 | 1.646989 | 12.704109 |
| imbalanced | train_mean | 16 | full | 0.551823 | 0.772540 | 15.810560 |
| imbalanced | train_mean | 16 | lowrank | 0.570573 | 0.663841 | 14.530620 |
| imbalanced | train_mean | 16 | gated | 0.494792 | 0.998803 | 17.733833 |
| imbalanced | train_mean | 30 | full | 0.527344 | 0.659270 | 15.580874 |
| imbalanced | train_mean | 30 | lowrank | 0.543490 | 0.567181 | 14.841147 |
| imbalanced | train_mean | 30 | gated | 0.475781 | 0.885396 | 18.923751 |
| imbalanced | none | 4 | full | 0.250000 | 1.732051 | 12.521367 |
| imbalanced | none | 4 | lowrank | 0.278906 | 1.637311 | 12.049280 |
| imbalanced | none | 4 | gated | 0.250000 | 1.732051 | 12.521367 |
| imbalanced | none | 16 | full | 0.382292 | 1.378972 | 17.312400 |
| imbalanced | none | 16 | lowrank | 0.494010 | 1.036713 | 16.826974 |
| imbalanced | none | 16 | gated | 0.376563 | 1.397217 | 17.404004 |
| imbalanced | none | 30 | full | 0.374219 | 1.342646 | 21.855641 |
| imbalanced | none | 30 | lowrank | 0.495052 | 0.895507 | 17.696042 |
| imbalanced | none | 30 | gated | 0.348437 | 1.425431 | 24.426535 |

## 4. 相对 Full 的改变量

| label_dist_mode | center_mode | scope | model | delta_test_acc | delta_load_cv | delta_mean_ed |
|---|---|---|---|---:|---:|---:|
| balanced | train_mean | global | lowrank | 0.000087 | 0.048011 | 0.035905 |
| balanced | train_mean | global | gated | -0.013542 | 0.023967 | 0.117088 |
| balanced | train_mean | layer_4 | lowrank | -0.007292 | 0.134846 | 0.272507 |
| balanced | train_mean | layer_4 | gated | -0.009896 | 0.039521 | 0.090973 |
| balanced | train_mean | layer_16 | lowrank | 0.004167 | 0.018049 | -0.152637 |
| balanced | train_mean | layer_16 | gated | -0.010417 | -0.002945 | 0.036841 |
| balanced | train_mean | layer_30 | lowrank | 0.003385 | -0.008861 | -0.012157 |
| balanced | train_mean | layer_30 | gated | -0.020312 | 0.035326 | 0.223449 |
| balanced | none | global | lowrank | 0.010243 | 0.013203 | 0.008025 |
| balanced | none | global | gated | -0.003819 | 0.022637 | 0.055042 |
| balanced | none | layer_4 | lowrank | 0.001042 | 0.103030 | 0.054918 |
| balanced | none | layer_4 | gated | -0.004427 | 0.023571 | 0.067865 |
| balanced | none | layer_16 | lowrank | 0.008073 | -0.035452 | 0.009575 |
| balanced | none | layer_16 | gated | -0.004688 | 0.021154 | 0.071986 |
| balanced | none | layer_30 | lowrank | 0.021615 | -0.027968 | -0.040418 |
| balanced | none | layer_30 | gated | -0.002344 | 0.023186 | 0.025274 |
| imbalanced | train_mean | global | lowrank | 0.043576 | -0.196696 | -0.722562 |
| imbalanced | train_mean | global | gated | -0.052083 | 0.203290 | 1.905137 |
| imbalanced | train_mean | layer_4 | lowrank | 0.095833 | -0.389299 | -0.148019 |
| imbalanced | train_mean | layer_4 | gated | -0.047656 | 0.157480 | 0.449261 |
| imbalanced | train_mean | layer_16 | lowrank | 0.018750 | -0.108699 | -1.279941 |
| imbalanced | train_mean | layer_16 | gated | -0.057031 | 0.226263 | 1.923272 |
| imbalanced | train_mean | layer_30 | lowrank | 0.016146 | -0.092089 | -0.739727 |
| imbalanced | train_mean | layer_30 | gated | -0.051562 | 0.226125 | 3.342877 |
| imbalanced | none | global | lowrank | 0.087153 | -0.294712 | -1.705704 |
| imbalanced | none | global | gated | -0.010503 | 0.033677 | 0.887500 |
| imbalanced | none | layer_4 | lowrank | 0.028906 | -0.094740 | -0.472087 |
| imbalanced | none | layer_4 | gated | 0.000000 | 0.000000 | 0.000000 |
| imbalanced | none | layer_16 | lowrank | 0.111719 | -0.342258 | -0.485426 |
| imbalanced | none | layer_16 | gated | -0.005729 | 0.018246 | 0.091604 |
| imbalanced | none | layer_30 | lowrank | 0.120833 | -0.447139 | -4.159599 |
| imbalanced | none | layer_30 | gated | -0.025781 | 0.082785 | 2.570894 |

## 5. 结论

- 若 delta_load_cv < 0，表示无需辅助损失也更均衡。
- 若 delta_mean_ed < 0，表示专家输入流形维度下降，语义更集中。
- 若 delta_test_acc 接近0或为正，表示降噪未明显损伤路由正确性。
