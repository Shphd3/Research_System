# Detailed: complete checkpoint evidence-use record

[Summary](summary.md) explains the question, frozen native models, controls and bounded observations. This record and its aligned Chinese companion own all execution details. Scientific judgment remains Unknown.

## All actual main conditions

The table uses 24 families, 48 A/B prompts per gap, complete-candidate margins in nats, family Wilson success intervals and paired family bootstrap margin intervals. Family is the statistical unit; six-template cluster sensitivity and every individual family are in the linked execution tables. Checkpoints are dependent trajectory states, not training replications.

| 模型 | 实际 B | 间隔 | 成功 /24 | 95% Wilson | 提示准确率 | 正确分差 nat [家族区间] |
|---|---|---|---|---|---|---|
| Baseline | 0 | 16 | 0 | [0.000, 0.138] | 0.500 | 0.000 [-0.001, 0.002] |
| Baseline | 0 | 256 | 1 | [0.007, 0.202] | 0.521 | 0.001 [-0.006, 0.009] |
| Baseline | 0 | 1024 | 1 | [0.007, 0.202] | 0.521 | -0.001 [-0.009, 0.008] |
| Baseline | 0.5 | 16 | 7 | [0.149, 0.492] | 0.646 | 0.608 [0.411, 0.851] |
| Baseline | 0.5 | 256 | 4 | [0.067, 0.359] | 0.583 | 0.235 [0.151, 0.332] |
| Baseline | 0.5 | 1024 | 2 | [0.023, 0.258] | 0.542 | 0.100 [0.034, 0.177] |
| Baseline | 1 | 16 | 12 | [0.314, 0.686] | 0.750 | 1.635 [0.943, 2.390] |
| Baseline | 1 | 256 | 8 | [0.180, 0.533] | 0.667 | 0.982 [0.494, 1.489] |
| Baseline | 1 | 1024 | 5 | [0.092, 0.405] | 0.604 | 0.961 [0.507, 1.436] |
| Baseline | 3 | 16 | 24 | [0.862, 1.000] | 1.000 | 5.099 [4.240, 6.014] |
| Baseline | 3 | 256 | 23 | [0.798, 0.993] | 0.979 | 4.978 [4.247, 5.716] |
| Baseline | 3 | 1024 | 23 | [0.798, 0.993] | 0.979 | 4.762 [4.095, 5.443] |
| Baseline | 5 | 16 | 23 | [0.798, 0.993] | 0.979 | 5.336 [4.334, 6.402] |
| Baseline | 5 | 256 | 23 | [0.798, 0.993] | 0.979 | 5.739 [4.733, 6.823] |
| Baseline | 5 | 1024 | 24 | [0.862, 1.000] | 1.000 | 4.901 [4.167, 5.683] |
| Baseline | 10 | 16 | 23 | [0.798, 0.993] | 0.979 | 4.797 [3.722, 5.953] |
| Baseline | 10 | 256 | 23 | [0.798, 0.993] | 0.979 | 5.259 [4.216, 6.375] |
| Baseline | 10 | 1024 | 23 | [0.798, 0.993] | 0.979 | 5.191 [4.098, 6.337] |
| Baseline | 12.2217 | 16 | 23 | [0.798, 0.993] | 0.979 | 5.006 [3.808, 6.251] |
| Baseline | 12.2217 | 256 | 23 | [0.798, 0.993] | 0.979 | 4.924 [3.827, 6.087] |
| Baseline | 12.2217 | 1024 | 23 | [0.798, 0.993] | 0.979 | 4.623 [3.584, 5.692] |
| Baseline | 13.0002 | 16 | 23 | [0.798, 0.993] | 0.979 | 4.832 [3.816, 5.899] |
| Baseline | 13.0002 | 256 | 24 | [0.862, 1.000] | 1.000 | 5.533 [4.548, 6.531] |
| Baseline | 13.0002 | 1024 | 24 | [0.862, 1.000] | 1.000 | 5.707 [4.701, 6.674] |
| Baseline | 15 | 16 | 21 | [0.690, 0.957] | 0.938 | 4.228 [3.059, 5.434] |
| Baseline | 15 | 256 | 22 | [0.742, 0.977] | 0.958 | 4.705 [3.616, 5.838] |
| Baseline | 15 | 1024 | 23 | [0.798, 0.993] | 0.979 | 4.903 [3.887, 5.990] |
| Baseline | 17 | 16 | 22 | [0.742, 0.977] | 0.958 | 4.224 [3.133, 5.370] |
| Baseline | 17 | 256 | 23 | [0.798, 0.993] | 0.979 | 5.013 [4.007, 6.042] |
| Baseline | 17 | 1024 | 21 | [0.690, 0.957] | 0.938 | 4.934 [3.920, 5.968] |
| Baseline | 19 | 16 | 21 | [0.690, 0.957] | 0.938 | 3.647 [2.708, 4.695] |
| Baseline | 19 | 256 | 20 | [0.641, 0.933] | 0.917 | 3.948 [3.025, 4.968] |
| Baseline | 19 | 1024 | 18 | [0.551, 0.880] | 0.875 | 3.745 [2.895, 4.643] |
| Baseline | 21 | 16 | 16 | [0.467, 0.820] | 0.833 | 3.603 [2.486, 4.816] |
| Baseline | 21 | 256 | 22 | [0.742, 0.977] | 0.958 | 4.157 [3.205, 5.169] |
| Baseline | 21 | 1024 | 21 | [0.690, 0.957] | 0.938 | 3.842 [2.794, 4.954] |
| Baseline | 22.9155 | 16 | 24 | [0.862, 1.000] | 1.000 | 4.059 [3.157, 5.069] |
| Baseline | 22.9155 | 256 | 21 | [0.690, 0.957] | 0.938 | 3.512 [2.649, 4.471] |
| Baseline | 22.9155 | 1024 | 22 | [0.742, 0.977] | 0.958 | 3.176 [2.406, 4.060] |
| Baseline | 23 | 16 | 23 | [0.798, 0.993] | 0.979 | 4.595 [3.411, 5.899] |
| Baseline | 23 | 256 | 22 | [0.742, 0.977] | 0.958 | 4.699 [3.598, 5.883] |
| Baseline | 23 | 1024 | 21 | [0.690, 0.957] | 0.938 | 4.587 [3.483, 5.802] |
| Baseline | 25 | 16 | 24 | [0.862, 1.000] | 1.000 | 4.218 [3.330, 5.212] |
| Baseline | 25 | 256 | 23 | [0.798, 0.993] | 0.979 | 4.418 [3.496, 5.482] |
| Baseline | 25 | 1024 | 22 | [0.742, 0.977] | 0.958 | 4.446 [3.498, 5.504] |
| Baseline | 27 | 16 | 21 | [0.690, 0.957] | 0.938 | 4.334 [3.253, 5.481] |
| Baseline | 27 | 256 | 24 | [0.862, 1.000] | 1.000 | 4.515 [3.673, 5.455] |
| Baseline | 27 | 1024 | 23 | [0.798, 0.993] | 0.979 | 4.692 [3.780, 5.690] |
| Baseline | 29 | 16 | 24 | [0.862, 1.000] | 1.000 | 4.558 [3.529, 5.651] |
| Baseline | 29 | 256 | 24 | [0.862, 1.000] | 1.000 | 4.794 [3.982, 5.706] |
| Baseline | 29 | 1024 | 23 | [0.798, 0.993] | 0.979 | 4.497 [3.748, 5.325] |
| Baseline | 31 | 16 | 23 | [0.798, 0.993] | 0.979 | 3.898 [3.045, 4.784] |
| Baseline | 31 | 256 | 22 | [0.742, 0.977] | 0.958 | 4.067 [3.233, 4.924] |
| Baseline | 31 | 1024 | 21 | [0.690, 0.957] | 0.938 | 3.518 [2.768, 4.284] |
| Baseline | 33 | 16 | 22 | [0.742, 0.977] | 0.958 | 4.366 [3.522, 5.250] |
| Baseline | 33 | 256 | 23 | [0.798, 0.993] | 0.979 | 5.024 [4.235, 5.843] |
| Baseline | 33 | 1024 | 22 | [0.742, 0.977] | 0.958 | 5.198 [4.276, 6.176] |
| Baseline | 35 | 16 | 19 | [0.595, 0.908] | 0.896 | 3.578 [2.559, 4.696] |
| Baseline | 35 | 256 | 21 | [0.690, 0.957] | 0.938 | 3.436 [2.529, 4.342] |
| Baseline | 35 | 1024 | 21 | [0.690, 0.957] | 0.938 | 3.409 [2.620, 4.231] |
| Baseline | 36.9598 | 16 | 19 | [0.595, 0.908] | 0.896 | 3.168 [2.233, 4.190] |
| Baseline | 36.9598 | 256 | 22 | [0.742, 0.977] | 0.958 | 3.905 [2.949, 4.942] |
| Baseline | 36.9598 | 1024 | 22 | [0.742, 0.977] | 0.958 | 3.976 [2.986, 5.090] |
| Baseline | 37 | 16 | 21 | [0.690, 0.957] | 0.938 | 3.390 [2.496, 4.371] |
| Baseline | 37 | 256 | 23 | [0.798, 0.993] | 0.979 | 3.846 [2.984, 4.776] |
| Baseline | 37 | 1024 | 22 | [0.742, 0.977] | 0.958 | 4.053 [3.055, 5.113] |
| Baseline | 37.2218 | 16 | 18 | [0.551, 0.880] | 0.875 | 3.846 [2.737, 5.071] |
| Baseline | 37.2218 | 256 | 18 | [0.551, 0.880] | 0.875 | 3.664 [2.522, 4.884] |
| Baseline | 37.2218 | 1024 | 19 | [0.595, 0.908] | 0.896 | 3.595 [2.495, 4.791] |
| Dense | 0 | 16 | 1 | [0.007, 0.202] | 0.521 | 0.001 [-0.001, 0.003] |
| Dense | 0 | 256 | 0 | [0.000, 0.138] | 0.500 | -0.001 [-0.002, 0.001] |
| Dense | 0 | 1024 | 0 | [0.000, 0.138] | 0.500 | -0.001 [-0.004, 0.002] |
| Dense | 0.5 | 16 | 8 | [0.180, 0.533] | 0.667 | 0.723 [0.517, 0.929] |
| Dense | 0.5 | 256 | 7 | [0.149, 0.492] | 0.646 | 0.451 [0.278, 0.635] |
| Dense | 0.5 | 1024 | 5 | [0.092, 0.405] | 0.604 | 0.367 [0.223, 0.522] |
| Dense | 1 | 16 | 9 | [0.212, 0.573] | 0.688 | 1.366 [1.032, 1.718] |
| Dense | 1 | 256 | 9 | [0.212, 0.573] | 0.688 | 0.811 [0.478, 1.186] |
| Dense | 1 | 1024 | 9 | [0.212, 0.573] | 0.688 | 0.685 [0.349, 1.074] |
| Dense | 3 | 16 | 20 | [0.641, 0.933] | 0.917 | 3.823 [2.797, 4.885] |
| Dense | 3 | 256 | 18 | [0.551, 0.880] | 0.875 | 3.486 [2.585, 4.416] |
| Dense | 3 | 1024 | 19 | [0.595, 0.908] | 0.896 | 3.322 [2.667, 4.037] |
| Dense | 5 | 16 | 23 | [0.798, 0.993] | 0.979 | 4.209 [3.240, 5.216] |
| Dense | 5 | 256 | 22 | [0.742, 0.977] | 0.958 | 4.160 [3.381, 4.990] |
| Dense | 5 | 1024 | 19 | [0.595, 0.908] | 0.896 | 3.158 [2.537, 3.848] |
| Dense | 10 | 16 | 23 | [0.798, 0.993] | 0.979 | 5.012 [4.133, 5.931] |
| Dense | 10 | 256 | 23 | [0.798, 0.993] | 0.979 | 6.094 [5.130, 7.083] |
| Dense | 10 | 1024 | 19 | [0.595, 0.908] | 0.896 | 4.275 [3.396, 5.146] |
| Dense | 15 | 16 | 23 | [0.798, 0.993] | 0.979 | 5.018 [3.986, 6.140] |
| Dense | 15 | 256 | 24 | [0.862, 1.000] | 1.000 | 6.542 [5.510, 7.619] |
| Dense | 15 | 1024 | 21 | [0.690, 0.957] | 0.938 | 5.777 [4.457, 7.122] |
| Dense | 17 | 16 | 23 | [0.798, 0.993] | 0.979 | 4.565 [3.542, 5.642] |
| Dense | 17 | 256 | 23 | [0.798, 0.993] | 0.979 | 5.201 [4.056, 6.376] |
| Dense | 17 | 1024 | 19 | [0.595, 0.908] | 0.896 | 5.001 [3.640, 6.409] |
| Dense | 19 | 16 | 23 | [0.798, 0.993] | 0.979 | 4.687 [3.612, 5.857] |
| Dense | 19 | 256 | 23 | [0.798, 0.993] | 0.979 | 5.585 [4.603, 6.670] |
| Dense | 19 | 1024 | 22 | [0.742, 0.977] | 0.958 | 5.387 [4.091, 6.756] |
| Dense | 21 | 16 | 20 | [0.641, 0.933] | 0.917 | 3.445 [2.351, 4.630] |
| Dense | 21 | 256 | 21 | [0.690, 0.957] | 0.938 | 5.358 [4.145, 6.576] |
| Dense | 21 | 1024 | 17 | [0.508, 0.851] | 0.854 | 5.027 [3.686, 6.367] |
| Dense | 22.0187 | 16 | 22 | [0.742, 0.977] | 0.958 | 4.513 [3.422, 5.672] |
| Dense | 22.0187 | 256 | 20 | [0.641, 0.933] | 0.917 | 4.944 [3.872, 6.074] |
| Dense | 22.0187 | 1024 | 19 | [0.595, 0.908] | 0.896 | 5.115 [3.683, 6.572] |
| Dense | 31 | 16 | 21 | [0.690, 0.957] | 0.938 | 4.356 [3.209, 5.565] |
| Dense | 31 | 256 | 22 | [0.742, 0.977] | 0.958 | 5.403 [4.112, 6.804] |
| Dense | 31 | 1024 | 20 | [0.641, 0.933] | 0.917 | 5.265 [3.858, 6.729] |
| Dense | 33 | 16 | 23 | [0.798, 0.993] | 0.979 | 4.372 [3.358, 5.470] |
| Dense | 33 | 256 | 22 | [0.742, 0.977] | 0.958 | 5.143 [4.083, 6.289] |
| Dense | 33 | 1024 | 21 | [0.690, 0.957] | 0.938 | 4.984 [3.604, 6.451] |
| Dense | 34.0764 | 16 | 22 | [0.742, 0.977] | 0.958 | 4.142 [3.053, 5.307] |
| Dense | 34.0764 | 256 | 22 | [0.742, 0.977] | 0.958 | 4.737 [3.597, 5.968] |
| Dense | 34.0764 | 1024 | 22 | [0.742, 0.977] | 0.958 | 4.430 [3.259, 5.681] |

## Real equal-token comparisons and descriptive crossings

The following tables retain real equal-token observations and the frozen 60/80/90 percent descriptive sensitivity. The Chinese column labels state model, actual billions of pretraining tokens, gap, successes/24, intervals and margins. No checkpoint interpolation occurs.

| 真实预训练 B token | Dense 近16 /24 | Dense 远1024 /24 | Baseline 近16 /24 | Baseline 远1024 /24 |
|---|---|---|---|---|
| 0 | 1 | 0 | 0 | 1 |
| 0.5 | 8 | 5 | 7 | 2 |
| 1 | 9 | 9 | 12 | 5 |
| 3 | 20 | 19 | 24 | 23 |
| 5 | 23 | 19 | 23 | 24 |
| 10 | 23 | 19 | 23 | 23 |
| 15 | 23 | 21 | 21 | 23 |
| 17 | 23 | 19 | 22 | 21 |
| 19 | 23 | 22 | 21 | 18 |
| 21 | 20 | 17 | 16 | 21 |
| 31 | 21 | 20 | 23 | 21 |
| 33 | 23 | 21 | 22 | 22 |

| 模型 | 阈值（仅描述） | 近16首次 B | 远1024首次 B | 远程连续下一点仍达标的起点 B |
|---|---|---|---|---|
| Dense | 60% | 3 | 3 | 3 |
| Dense | 80% | 3 | 15 | 31 |
| Dense | 90% | 5 | 19 | 未达到 / NOT REACHED |
| Baseline | 60% | 3 | 3 | 3 |
| Baseline | 80% | 3 | 3 | 3 |
| Baseline | 90% | 3 | 3 | 3 |

## Ineffective-evidence preferences and sensitivity

No-evidence and wrong-entity conditions have no gold answer. The wrong-entity diagnostic carries candidate A only; it does not establish a balanced irrelevant-evidence treatment. High preference for that word limits entity-binding claims. Every checkpoint control is in execution tables/no_evidence_preferences.csv.

| 模型33B | 条件 | 名义间隔 | 偏A /24 | 偏B /24 | A−B均值 nat |
|---|---|---|---|---|---|
| Baseline | no_evidence | 16 | 13 | 11 | 0.313 |
| Baseline | no_evidence | 256 | 14 | 10 | 0.272 |
| Baseline | no_evidence | 1024 | 13 | 11 | 0.268 |
| Baseline | irrelevant | 16 | 24 | 0 | 3.533 |
| Baseline | irrelevant | 256 | 22 | 2 | 2.436 |
| Baseline | irrelevant | 1024 | 19 | 5 | 2.578 |
| Dense | no_evidence | 16 | 14 | 10 | 0.452 |
| Dense | no_evidence | 256 | 14 | 10 | 0.444 |
| Dense | no_evidence | 1024 | 15 | 9 | 0.480 |
| Dense | irrelevant | 16 | 24 | 0 | 4.121 |
| Dense | irrelevant | 256 | 20 | 4 | 3.935 |
| Dense | irrelevant | 1024 | 21 | 3 | 4.228 |

All candidates have one lexical token and a period. First-token and no-period results must agree; equal lengths make mean-score ranking identical. Filler reversal preserves the sentence inventory; prefix extension at fixed gap also adds filler and cannot isolate pure position.

| 模型33B | 间隔 | 完整含句号 /24 | 只计词汇token /24 | 填充反序 /24 | 固定间隔、回答后移 /24 |
|---|---|---|---|---|---|
| Dense | 16 | 23 | 23 | — | — |
| Dense | 256 | 22 | 23 | — | — |
| Dense | 1024 | 21 | 21 | 21 | 21 |
| Baseline | 16 | 22 | 23 | — | — |
| Baseline | 256 | 23 | 23 | — | — |
| Baseline | 1024 | 22 | 22 | 22 | 21 |

## Content-family results

The table gives every task type at selected real states, not a selected favorable subset. All other states/templates/gaps remain in the complete tables; the denominator is eight families per type.

| 模型 | 实际 B | 内容 | 间隔 | 成功 /8 | 平均分差 nat |
|---|---|---|---|---|---|
| Baseline | 1 | color | 16 | 4 | 1.188 |
| Baseline | 1 | destination | 16 | 7 | 3.428 |
| Baseline | 1 | object | 16 | 1 | 0.289 |
| Baseline | 1 | color | 1024 | 1 | 0.995 |
| Baseline | 1 | destination | 1024 | 3 | 1.529 |
| Baseline | 1 | object | 1024 | 1 | 0.359 |
| Baseline | 3 | color | 16 | 8 | 3.679 |
| Baseline | 3 | destination | 16 | 8 | 7.292 |
| Baseline | 3 | object | 16 | 8 | 4.326 |
| Baseline | 3 | color | 1024 | 8 | 4.691 |
| Baseline | 3 | destination | 1024 | 8 | 5.576 |
| Baseline | 3 | object | 1024 | 7 | 4.020 |
| Baseline | 5 | color | 16 | 8 | 3.939 |
| Baseline | 5 | destination | 16 | 8 | 8.416 |
| Baseline | 5 | object | 16 | 7 | 3.653 |
| Baseline | 5 | color | 1024 | 8 | 4.181 |
| Baseline | 5 | destination | 1024 | 8 | 6.154 |
| Baseline | 5 | object | 1024 | 8 | 4.369 |
| Baseline | 15 | color | 16 | 7 | 2.614 |
| Baseline | 15 | destination | 16 | 8 | 7.991 |
| Baseline | 15 | object | 16 | 6 | 2.080 |
| Baseline | 15 | color | 1024 | 8 | 2.907 |
| Baseline | 15 | destination | 1024 | 8 | 8.195 |
| Baseline | 15 | object | 1024 | 7 | 3.605 |
| Baseline | 33 | color | 16 | 8 | 3.182 |
| Baseline | 33 | destination | 16 | 8 | 6.878 |
| Baseline | 33 | object | 16 | 6 | 3.039 |
| Baseline | 33 | color | 1024 | 8 | 4.418 |
| Baseline | 33 | destination | 1024 | 8 | 8.043 |
| Baseline | 33 | object | 1024 | 6 | 3.133 |
| Dense | 1 | color | 16 | 6 | 1.834 |
| Dense | 1 | destination | 16 | 1 | 0.913 |
| Dense | 1 | object | 16 | 2 | 1.350 |
| Dense | 1 | color | 1024 | 6 | 1.656 |
| Dense | 1 | destination | 1024 | 0 | -0.196 |
| Dense | 1 | object | 1024 | 3 | 0.596 |
| Dense | 3 | color | 16 | 7 | 2.498 |
| Dense | 3 | destination | 16 | 8 | 6.801 |
| Dense | 3 | object | 16 | 5 | 2.171 |
| Dense | 3 | color | 1024 | 7 | 4.244 |
| Dense | 3 | destination | 1024 | 8 | 3.513 |
| Dense | 3 | object | 1024 | 4 | 2.210 |
| Dense | 5 | color | 16 | 7 | 2.538 |
| Dense | 5 | destination | 16 | 8 | 6.654 |
| Dense | 5 | object | 16 | 8 | 3.436 |
| Dense | 5 | color | 1024 | 8 | 3.757 |
| Dense | 5 | destination | 1024 | 5 | 2.699 |
| Dense | 5 | object | 1024 | 6 | 3.018 |
| Dense | 15 | color | 16 | 7 | 2.970 |
| Dense | 15 | destination | 16 | 8 | 8.190 |
| Dense | 15 | object | 16 | 8 | 3.894 |
| Dense | 15 | color | 1024 | 8 | 5.400 |
| Dense | 15 | destination | 1024 | 8 | 9.769 |
| Dense | 15 | object | 1024 | 5 | 2.162 |
| Dense | 33 | color | 16 | 8 | 2.324 |
| Dense | 33 | destination | 16 | 8 | 7.664 |
| Dense | 33 | object | 16 | 7 | 3.130 |
| Dense | 33 | color | 1024 | 8 | 4.356 |
| Dense | 33 | destination | 1024 | 8 | 9.336 |
| Dense | 33 | object | 1024 | 5 | 1.261 |

## Execution conformance and provenance

All 37 selected states and all 384 prompts/state completed. Every state file has a fresh full SHA, actual counter check and native strict-load receipt. Weights and load bias remain frozen; zero gradient updates. The original pre-behavior Protocol, data/config/source hashes and three audit records remain in execution audit/. A01 fixes only the cost estimator: 4579.790s incorrectly multiplied checkpoint load/hash overhead by four; 1394.601s accounts for one load plus four times scoring and the real state composition. The 3600s ceiling, texts, criteria and numerical tolerances did not change. Initial construction dependency/filler failures occurred before model behavior and are described in the Chinese companion; tokenizers used an existing isolated dependency, no download.

Two actual 33B models each scored 96 engineering prompts. Native CE versus chain scores differs by at most approximately 4.77e-7 nat for Dense and 0.02555 nat for MoE, inside the predeclared 0.03 tolerance; prefix hidden differences were zero. That calibration does not provide a universal error bound for every margin. Both models use the same PyTorch 2.3.0 CUDA layer; old CPU 2.8 measurements are historical context only. Selected cases are reading examples, not a new confirmation set.

Ten missing paths, including one recovered 19B identity, and three equivalent state-hash aliases are retained in audit/checkpoints.csv and tables/coverage_ledger.csv. Nine state identities remain inaccessible in the bounded roots. The latest independent evening senior transcript remains unavailable; user-provided and attached summary material is labeled accordingly. Native training data order agrees only through22.018691584B; total capacity differs throughout.

Full cost: 14,208 prompts, 33,701,376 duplicated-prefix input tokens, 56,832 scored answer tokens; 1323.19s including 1134.68s loading/hash, approximately 0.368 existing MIG-slice hours and 2.624GiB peak allocated. Add 62.18s engineering smoke and CPU preparation/aggregation/figure overhead; this is not whole-H100-equivalent billing or end-to-end training speedup. No new ACP job was submitted.

[Reproduction](reproduce.md), [all artifact identities](artifact_manifest.json), [dataset guide](dataset_guide.md), [cases](cases_cn.md), [complete coverage](/data/250010109/MoE_Router/experiments/20261105_checkpoint_evidence_use/tables/coverage_ledger.csv). Actual input IDs: checkpoint_family_evidence_use_dense_snapshot_20261105, checkpoint_family_evidence_use_baseline_snapshot_20261105, dataset_checkpoint_evidence_use_frozen_20261105 and tokenizer_qwen3_0p6b_base. Actual MoE SAE-final backfill is sae_moe_baseline33b_gate_input_formal_1b_20261104; it is not a base checkpoint. Output registration is analysis_checkpoint_evidence_use_20261105. Current access evidence is linked in artifact_manifest.json.

Coverage: native states/controls/families/figure/code/cost DONE_EXPLORATORY; unavailable paths BLOCKED; aliases explicitly reused; representation/interventions/new training NOT RUN. Scientific interpretation and formal-definition revision remain Unknown. No difference directly identifies interference, specialization or long-tail mechanisms.


[Training assets, optimizer/data provenance and comparison limits](training_assets.md) · [训练资产和预算边界](training_assets_cn.md).


Numerical supplement:24states/122selected small-margin prompts were rescored inFP32;11choices and11state/gap family counts change. First sampled60/80/90percent crossings and Dense5/10/15/17Bkey comparisons remain under this subset sensitivity. Latest Dense34.076B22/22in primary BF16 becomes21/22in the subset. The figure remains registered BF16. This is not a completeFP32trajectory. [Full numerical audit](numerical_audit.md).


Cost clarification: primary serialized input counts exclude right padding. Physical primary forward positions are36,429,312, including2,727,936padding positions. Recorded smoke/full/precision stages total26.0minutes; CPU preparation/reporting is not separately timed and this is not whole-GPU billing. [Costs](/data/250010109/MoE_Router/experiments/20261105_checkpoint_evidence_use/audit/overall_cost.json).
