派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/casebook_cn.md`。
[精确原始文件](../../../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/casebook_cn.md)；研究修改仍回到原件。

---

# D1固定全文与反例

本案例家族在发现阶段指定为展示对象，不按新分离效果挑选。n=62，证书为det(t I − A)在t=0非零／为零；因为det(−A)=(−1)^n det(A)，分别推出可逆／奇异。下列text为模型完整输入，token零基位置，观察最后一项。p表示逻辑probe的可逆概率；原生模型另列，不能混用。

## D1_M05_0_invertible_description_p0_main

家族D1_M05_0；定理组spectrum；答案description；改写0；label=1；观察位置=55。

```text
Consider a real square matrix A with n = 62. It satisfies the following condition: det(t I - A) evaluated at t = 0 is nonzero. This is the full description for this exercise.
Summarize the mathematical object and its stated properties.
Summary:
```

token_ids：`[37175, 264, 1931, 9334, 6172, 362, 448, 308, 284, 220, 21, 17, 13, 1084, 67901, 279, 2701, 2971, 25, 3392, 1155, 358, 481, 362, 8, 25070, 518, 259, 284, 220, 15, 374, 72232, 13, 1096, 374, 279, 2480, 4008, 369, 419, 10158, 624, 9190, 5612, 551, 279, 35972, 1633, 323, 1181, 10982, 5888, 624, 19237, 25]`

### ATTN_SAE

|   atom | group   |     raw_z |
|-------:|:--------|----------:|
|   1359 | C       |  2.159655 |
|   2603 | C       |  3.054364 |
|   3198 | F       |  0.000000 |
|   4730 | F       |  0.000000 |
|   6857 | F       |  0.000000 |
|   7211 | C       | 12.415058 |
|  11707 | C       |  0.000000 |
|  11811 | C       |  3.572770 |
|  13009 | F       |  0.000000 |
|  16799 | F       |  0.000000 |
|  16947 | F       |  0.000000 |
|  20017 | C       |  2.049756 |
|  25221 | F       |  0.000000 |
|  25409 | F       |  4.064008 |
|  26105 | C       |  0.000000 |
|  27002 | C       |  4.148403 |

| arm                 |   p_invertible |     loss |   correct |
|:--------------------|---------------:|---------:|----------:|
| C                   |       0.491065 | 0.711180 |         0 |
| C_union_F           |       0.585093 | 0.535985 |         1 |
| binary_union        |       0.587837 | 0.531306 |         1 |
| location_original_h |       0.098689 | 2.315778 |         0 |

### MLPIN_SAE

|   atom | group   |     raw_z |
|-------:|:--------|----------:|
|     47 | F       |  9.657923 |
|   2104 | C       |  3.311796 |
|   2196 | C       |  0.000000 |
|   5196 | C       |  6.518068 |
|   8048 | C       |  4.540512 |
|   8856 | F       |  4.282662 |
|  10262 | F       |  0.000000 |
|  11234 | F       |  0.000000 |
|  11471 | F       |  0.000000 |
|  14879 | F       |  3.280279 |
|  18758 | C       |  4.333022 |
|  20886 | F       |  0.000000 |
|  20957 | C       | 13.890637 |
|  28024 | F       |  9.314697 |
|  29342 | C       | 46.928169 |
|  29669 | C       |  0.000000 |

| arm                 |   p_invertible |     loss |   correct |
|:--------------------|---------------:|---------:|----------:|
| C                   |       0.453777 | 0.790149 |         0 |
| C_union_F           |       0.209771 | 1.561738 |         0 |
| binary_union        |       0.315053 | 1.155016 |         0 |
| location_original_h |       0.276339 | 1.286127 |         0 |

### CC_CORRECTED

|   atom | group   |    raw_z |
|-------:|:--------|---------:|
|   1053 | F       | 0.000000 |
|   2919 | C       | 0.012720 |
|   3604 | F       | 0.000000 |
|   4828 | C       | 0.015866 |
|   5308 | F       | 0.000000 |
|   6440 | C       | 0.029322 |
|   7557 | C       | 0.148414 |
|   7803 | F       | 0.007149 |
|   8086 | C       | 0.014947 |
|   8693 | C       | 0.127724 |
|  11090 | F       | 0.000000 |
|  11318 | C       | 0.015323 |
|  12820 | F       | 0.007758 |
|  14693 | C       | 0.013427 |
|  14796 | F       | 0.000000 |
|  15445 | F       | 0.000000 |

| arm                 |   p_invertible |     loss |   correct |
|:--------------------|---------------:|---------:|----------:|
| C                   |       0.535367 | 0.624803 |         1 |
| C_union_F           |       0.642636 | 0.442177 |         1 |
| binary_union        |       0.001928 | 6.251208 |         0 |
| location_original_h |       0.157002 | 1.851497 |         0 |

### 原生完整候选得分

```json
[
  {
    "id": "D1_M05_0_invertible_description_p0_main",
    "family": "D1_M05_0",
    "cluster": "spectrum",
    "split": "heldout",
    "wording": "description",
    "label": 1,
    "format": "continuation",
    "prefix": "Consider a real square matrix A with n = 62. It satisfies the following condition: det(t I - A) evaluated at t = 0 is nonzero. This is the full description for this exercise.\nTherefore, A is",
    "scores": [
      {
        "candidate": " invertible.",
        "candidate_id": 0,
        "score": -1.6029242277145386,
        "candidate_token_ids": [
          42199,
          1238,
          13
        ],
        "candidate_length": 3,
        "prefix_tokens": 47
      },
      {
        "candidate": " singular.",
        "candidate_id": 1,
        "score": -6.7260847091674805,
        "candidate_token_ids": [
          33944,
          13
        ],
        "candidate_length": 2,
        "prefix_tokens": 47
      }
    ],
    "correct_margin": 5.123160481452942,
    "correct": true,
    "p_two_candidate_invertible": 0.9940781120668382
  },
  {
    "id": "D1_M05_0_invertible_description_p0_main",
    "family": "D1_M05_0",
    "cluster": "spectrum",
    "split": "heldout",
    "wording": "description",
    "label": 1,
    "format": "question",
    "prefix": "Consider a real square matrix A with n = 62. It satisfies the following condition: det(t I - A) evaluated at t = 0 is nonzero. This is the full description for this exercise.\nIs A invertible or singular? Answer:",
    "scores": [
      {
        "candidate": " invertible.",
        "candidate_id": 0,
        "score": -5.496676445007324,
        "candidate_token_ids": [
          42199,
          1238,
          13
        ],
        "candidate_length": 3,
        "prefix_tokens": 52
      },
      {
        "candidate": " singular.",
        "candidate_id": 1,
        "score": -5.637255668640137,
        "candidate_token_ids": [
          33944,
          13
        ],
        "candidate_length": 2,
        "prefix_tokens": 52
      }
    ],
    "correct_margin": 0.1405792236328125,
    "correct": true,
    "p_two_candidate_invertible": 0.5350870409084129
  }
]
```

## D1_M05_0_invertible_description_p1_main

家族D1_M05_0；定理组spectrum；答案description；改写1；label=1；观察位置=59。

```text
The object in this problem is a real square matrix A with n = 62. The stated property is that det(t I - A) evaluated at t = 0 is nonzero. This is the full description for this exercise.
Summarize the mathematical object and its stated properties.
Summary:
```

token_ids：`[785, 1633, 304, 419, 3491, 374, 264, 1931, 9334, 6172, 362, 448, 308, 284, 220, 21, 17, 13, 576, 10982, 3343, 374, 429, 3392, 1155, 358, 481, 362, 8, 25070, 518, 259, 284, 220, 15, 374, 72232, 13, 1096, 374, 279, 2480, 4008, 369, 419, 10158, 624, 9190, 5612, 551, 279, 35972, 1633, 323, 1181, 10982, 5888, 624, 19237, 25]`

### ATTN_SAE

|   atom | group   |     raw_z |
|-------:|:--------|----------:|
|   1359 | C       |  0.000000 |
|   2603 | C       |  2.899511 |
|   3198 | F       |  0.000000 |
|   4730 | F       |  0.000000 |
|   6857 | F       |  0.000000 |
|   7211 | C       | 13.936668 |
|  11707 | C       |  0.000000 |
|  11811 | C       |  2.425862 |
|  13009 | F       |  0.000000 |
|  16799 | F       |  0.000000 |
|  16947 | F       |  0.000000 |
|  20017 | C       |  0.000000 |
|  25221 | F       |  0.000000 |
|  25409 | F       |  7.187548 |
|  26105 | C       |  0.000000 |
|  27002 | C       |  2.426174 |

| arm                 |   p_invertible |     loss |   correct |
|:--------------------|---------------:|---------:|----------:|
| C                   |       0.397968 | 0.921384 |         0 |
| C_union_F           |       0.577312 | 0.549372 |         1 |
| binary_union        |       0.551948 | 0.594301 |         1 |
| location_original_h |       0.997812 | 0.002190 |         1 |

### MLPIN_SAE

|   atom | group   |     raw_z |
|-------:|:--------|----------:|
|     47 | F       |  8.099495 |
|   2104 | C       |  3.560624 |
|   2196 | C       |  0.000000 |
|   5196 | C       | 10.248079 |
|   8048 | C       |  6.719121 |
|   8856 | F       |  7.982633 |
|  10262 | F       |  0.000000 |
|  11234 | F       |  0.000000 |
|  11471 | F       |  0.000000 |
|  14879 | F       |  0.000000 |
|  18758 | C       |  4.155982 |
|  20886 | F       |  0.000000 |
|  20957 | C       | 12.993804 |
|  28024 | F       |  8.506454 |
|  29342 | C       | 44.061424 |
|  29669 | C       |  0.000000 |

| arm                 |   p_invertible |     loss |   correct |
|:--------------------|---------------:|---------:|----------:|
| C                   |       0.396686 | 0.924610 |         0 |
| C_union_F           |       0.230402 | 1.467929 |         0 |
| binary_union        |       0.795312 | 0.229020 |         1 |
| location_original_h |       0.999209 | 0.000792 |         1 |

### CC_CORRECTED

|   atom | group   |    raw_z |
|-------:|:--------|---------:|
|   1053 | F       | 0.000000 |
|   2919 | C       | 0.017979 |
|   3604 | F       | 0.000000 |
|   4828 | C       | 0.016714 |
|   5308 | F       | 0.000000 |
|   6440 | C       | 0.036015 |
|   7557 | C       | 0.151475 |
|   7803 | F       | 0.006913 |
|   8086 | C       | 0.000000 |
|   8693 | C       | 0.081163 |
|  11090 | F       | 0.000000 |
|  11318 | C       | 0.028549 |
|  12820 | F       | 0.000000 |
|  14693 | C       | 0.013788 |
|  14796 | F       | 0.000000 |
|  15445 | F       | 0.000000 |

| arm                 |   p_invertible |     loss |   correct |
|:--------------------|---------------:|---------:|----------:|
| C                   |       0.308816 | 1.175009 |         0 |
| C_union_F           |       0.999581 | 0.000419 |         1 |
| binary_union        |       0.000461 | 7.682231 |         0 |
| location_original_h |       0.998225 | 0.001777 |         1 |

### 原生完整候选得分

```json
[
  {
    "id": "D1_M05_0_invertible_description_p1_main",
    "family": "D1_M05_0",
    "cluster": "spectrum",
    "split": "heldout",
    "wording": "description",
    "label": 1,
    "format": "continuation",
    "prefix": "The object in this problem is a real square matrix A with n = 62. The stated property is that det(t I - A) evaluated at t = 0 is nonzero. This is the full description for this exercise.\nTherefore, A is",
    "scores": [
      {
        "candidate": " invertible.",
        "candidate_id": 0,
        "score": -1.7038671970367432,
        "candidate_token_ids": [
          42199,
          1238,
          13
        ],
        "candidate_length": 3,
        "prefix_tokens": 51
      },
      {
        "candidate": " singular.",
        "candidate_id": 1,
        "score": -6.419816970825195,
        "candidate_token_ids": [
          33944,
          13
        ],
        "candidate_length": 2,
        "prefix_tokens": 51
      }
    ],
    "correct_margin": 4.715949773788452,
    "correct": true,
    "p_two_candidate_invertible": 0.9911280557086902
  },
  {
    "id": "D1_M05_0_invertible_description_p1_main",
    "family": "D1_M05_0",
    "cluster": "spectrum",
    "split": "heldout",
    "wording": "description",
    "label": 1,
    "format": "question",
    "prefix": "The object in this problem is a real square matrix A with n = 62. The stated property is that det(t I - A) evaluated at t = 0 is nonzero. This is the full description for this exercise.\nIs A invertible or singular? Answer:",
    "scores": [
      {
        "candidate": " invertible.",
        "candidate_id": 0,
        "score": -5.430629253387451,
        "candidate_token_ids": [
          42199,
          1238,
          13
        ],
        "candidate_length": 3,
        "prefix_tokens": 56
      },
      {
        "candidate": " singular.",
        "candidate_id": 1,
        "score": -5.59202241897583,
        "candidate_token_ids": [
          33944,
          13
        ],
        "candidate_length": 2,
        "prefix_tokens": 56
      }
    ],
    "correct_margin": 0.1613931655883789,
    "correct": true,
    "p_two_candidate_invertible": 0.5402609370647442
  }
]
```

## D1_M05_0_invertible_explicit_p0_main

家族D1_M05_0；定理组spectrum；答案explicit；改写0；label=1；观察位置=53。

```text
Consider a real square matrix A with n = 62. It satisfies the following condition: det(t I - A) evaluated at t = 0 is nonzero. This square matrix is invertible.
Summarize the mathematical object and its stated properties.
Summary:
```

token_ids：`[37175, 264, 1931, 9334, 6172, 362, 448, 308, 284, 220, 21, 17, 13, 1084, 67901, 279, 2701, 2971, 25, 3392, 1155, 358, 481, 362, 8, 25070, 518, 259, 284, 220, 15, 374, 72232, 13, 1096, 9334, 6172, 374, 42199, 1238, 624, 9190, 5612, 551, 279, 35972, 1633, 323, 1181, 10982, 5888, 624, 19237, 25]`

### ATTN_SAE

|   atom | group   |     raw_z |
|-------:|:--------|----------:|
|   1359 | C       |  2.365072 |
|   2603 | C       |  2.465641 |
|   3198 | F       |  0.000000 |
|   4730 | F       |  0.000000 |
|   6857 | F       |  0.000000 |
|   7211 | C       | 11.267194 |
|  11707 | C       |  2.216938 |
|  11811 | C       |  2.513337 |
|  13009 | F       |  0.000000 |
|  16799 | F       |  0.000000 |
|  16947 | F       |  0.000000 |
|  20017 | C       |  2.552164 |
|  25221 | F       |  0.000000 |
|  25409 | F       |  5.213519 |
|  26105 | C       |  2.824985 |
|  27002 | C       |  2.742794 |

| arm                 |   p_invertible |     loss |   correct |
|:--------------------|---------------:|---------:|----------:|
| C                   |       0.478940 | 0.736179 |         0 |
| C_union_F           |       0.629474 | 0.462871 |         1 |
| binary_union        |       0.603241 | 0.505439 |         1 |
| location_original_h |       0.936737 | 0.065353 |         1 |

### MLPIN_SAE

|   atom | group   |     raw_z |
|-------:|:--------|----------:|
|     47 | F       | 10.692802 |
|   2104 | C       |  2.779185 |
|   2196 | C       |  0.000000 |
|   5196 | C       |  5.850809 |
|   8048 | C       |  6.113053 |
|   8856 | F       |  3.305340 |
|  10262 | F       |  2.703562 |
|  11234 | F       |  0.000000 |
|  11471 | F       |  0.000000 |
|  14879 | F       |  0.000000 |
|  18758 | C       |  4.779571 |
|  20886 | F       |  2.698397 |
|  20957 | C       | 11.179317 |
|  28024 | F       | 10.445394 |
|  29342 | C       | 45.106747 |
|  29669 | C       |  0.000000 |

| arm                 |   p_invertible |     loss |   correct |
|:--------------------|---------------:|---------:|----------:|
| C                   |       0.471032 | 0.752828 |         0 |
| C_union_F           |       0.790068 | 0.235636 |         1 |
| binary_union        |       0.950087 | 0.051201 |         1 |
| location_original_h |       0.971123 | 0.029302 |         1 |

### CC_CORRECTED

|   atom | group   |    raw_z |
|-------:|:--------|---------:|
|   1053 | F       | 0.000000 |
|   2919 | C       | 0.020694 |
|   3604 | F       | 0.000000 |
|   4828 | C       | 0.017917 |
|   5308 | F       | 0.000000 |
|   6440 | C       | 0.031911 |
|   7557 | C       | 0.146919 |
|   7803 | F       | 0.000000 |
|   8086 | C       | 0.014098 |
|   8693 | C       | 0.066327 |
|  11090 | F       | 0.000000 |
|  11318 | C       | 0.017040 |
|  12820 | F       | 0.000000 |
|  14693 | C       | 0.014985 |
|  14796 | F       | 0.000000 |
|  15445 | F       | 0.000000 |

| arm                 |   p_invertible |     loss |   correct |
|:--------------------|---------------:|---------:|----------:|
| C                   |       0.541708 | 0.613029 |         1 |
| C_union_F           |       0.999997 | 0.000003 |         1 |
| binary_union        |       0.999578 | 0.000422 |         1 |
| location_original_h |       0.947803 | 0.053609 |         1 |

### 原生完整候选得分

```json
[
  {
    "id": "D1_M05_0_invertible_explicit_p0_main",
    "family": "D1_M05_0",
    "cluster": "spectrum",
    "split": "heldout",
    "wording": "explicit",
    "label": 1,
    "format": "continuation",
    "prefix": "Consider a real square matrix A with n = 62. It satisfies the following condition: det(t I - A) evaluated at t = 0 is nonzero. This square matrix is invertible.\nTherefore, A is",
    "scores": [
      {
        "candidate": " invertible.",
        "candidate_id": 0,
        "score": -2.225922107696533,
        "candidate_token_ids": [
          42199,
          1238,
          13
        ],
        "candidate_length": 3,
        "prefix_tokens": 45
      },
      {
        "candidate": " singular.",
        "candidate_id": 1,
        "score": -6.277770042419434,
        "candidate_token_ids": [
          33944,
          13
        ],
        "candidate_length": 2,
        "prefix_tokens": 45
      }
    ],
    "correct_margin": 4.0518479347229,
    "correct": true,
    "p_two_candidate_invertible": 0.9829070411681546
  },
  {
    "id": "D1_M05_0_invertible_explicit_p0_main",
    "family": "D1_M05_0",
    "cluster": "spectrum",
    "split": "heldout",
    "wording": "explicit",
    "label": 1,
    "format": "question",
    "prefix": "Consider a real square matrix A with n = 62. It satisfies the following condition: det(t I - A) evaluated at t = 0 is nonzero. This square matrix is invertible.\nIs A invertible or singular? Answer:",
    "scores": [
      {
        "candidate": " invertible.",
        "candidate_id": 0,
        "score": -5.49825382232666,
        "candidate_token_ids": [
          42199,
          1238,
          13
        ],
        "candidate_length": 3,
        "prefix_tokens": 50
      },
      {
        "candidate": " singular.",
        "candidate_id": 1,
        "score": -6.096169471740723,
        "candidate_token_ids": [
          33944,
          13
        ],
        "candidate_length": 2,
        "prefix_tokens": 50
      }
    ],
    "correct_margin": 0.5979156494140625,
    "correct": true,
    "p_two_candidate_invertible": 0.6451792950128097
  }
]
```

## D1_M05_0_invertible_explicit_p1_main

家族D1_M05_0；定理组spectrum；答案explicit；改写1；label=1；观察位置=57。

```text
The object in this problem is a real square matrix A with n = 62. The stated property is that det(t I - A) evaluated at t = 0 is nonzero. This square matrix is invertible.
Summarize the mathematical object and its stated properties.
Summary:
```

token_ids：`[785, 1633, 304, 419, 3491, 374, 264, 1931, 9334, 6172, 362, 448, 308, 284, 220, 21, 17, 13, 576, 10982, 3343, 374, 429, 3392, 1155, 358, 481, 362, 8, 25070, 518, 259, 284, 220, 15, 374, 72232, 13, 1096, 9334, 6172, 374, 42199, 1238, 624, 9190, 5612, 551, 279, 35972, 1633, 323, 1181, 10982, 5888, 624, 19237, 25]`

### ATTN_SAE

|   atom | group   |     raw_z |
|-------:|:--------|----------:|
|   1359 | C       |  0.000000 |
|   2603 | C       |  2.417892 |
|   3198 | F       |  0.000000 |
|   4730 | F       |  2.589528 |
|   6857 | F       |  0.000000 |
|   7211 | C       | 12.861531 |
|  11707 | C       |  3.226490 |
|  11811 | C       |  0.000000 |
|  13009 | F       |  0.000000 |
|  16799 | F       |  0.000000 |
|  16947 | F       |  0.000000 |
|  20017 | C       |  0.000000 |
|  25221 | F       |  0.000000 |
|  25409 | F       |  7.522852 |
|  26105 | C       |  0.000000 |
|  27002 | C       |  0.000000 |

| arm                 |   p_invertible |     loss |   correct |
|:--------------------|---------------:|---------:|----------:|
| C                   |       0.365206 | 1.007295 |         0 |
| C_union_F           |       0.558831 | 0.581908 |         1 |
| binary_union        |       0.488497 | 0.716421 |         0 |
| location_original_h |       0.999250 | 0.000750 |         1 |

### MLPIN_SAE

|   atom | group   |     raw_z |
|-------:|:--------|----------:|
|     47 | F       |  8.214044 |
|   2104 | C       |  3.533097 |
|   2196 | C       |  0.000000 |
|   5196 | C       |  9.249521 |
|   8048 | C       |  7.519876 |
|   8856 | F       |  7.264186 |
|  10262 | F       |  0.000000 |
|  11234 | F       |  0.000000 |
|  11471 | F       |  0.000000 |
|  14879 | F       |  0.000000 |
|  18758 | C       |  3.459649 |
|  20886 | F       |  0.000000 |
|  20957 | C       | 11.499544 |
|  28024 | F       |  9.316855 |
|  29342 | C       | 44.149529 |
|  29669 | C       |  0.000000 |

| arm                 |   p_invertible |     loss |   correct |
|:--------------------|---------------:|---------:|----------:|
| C                   |       0.445853 | 0.807765 |         0 |
| C_union_F           |       0.398695 | 0.919558 |         0 |
| binary_union        |       0.795312 | 0.229020 |         1 |
| location_original_h |       0.999253 | 0.000747 |         1 |

### CC_CORRECTED

|   atom | group   |    raw_z |
|-------:|:--------|---------:|
|   1053 | F       | 0.000000 |
|   2919 | C       | 0.021124 |
|   3604 | F       | 0.000000 |
|   4828 | C       | 0.020320 |
|   5308 | F       | 0.000000 |
|   6440 | C       | 0.040404 |
|   7557 | C       | 0.148687 |
|   7803 | F       | 0.000000 |
|   8086 | C       | 0.000000 |
|   8693 | C       | 0.053660 |
|  11090 | F       | 0.000000 |
|  11318 | C       | 0.018074 |
|  12820 | F       | 0.000000 |
|  14693 | C       | 0.015680 |
|  14796 | F       | 0.000000 |
|  15445 | F       | 0.000000 |

| arm                 |   p_invertible |     loss |   correct |
|:--------------------|---------------:|---------:|----------:|
| C                   |       0.460454 | 0.775541 |         0 |
| C_union_F           |       1.000000 | 0.000000 |         1 |
| binary_union        |       0.830459 | 0.185777 |         1 |
| location_original_h |       0.999184 | 0.000816 |         1 |

### 原生完整候选得分

```json
[
  {
    "id": "D1_M05_0_invertible_explicit_p1_main",
    "family": "D1_M05_0",
    "cluster": "spectrum",
    "split": "heldout",
    "wording": "explicit",
    "label": 1,
    "format": "continuation",
    "prefix": "The object in this problem is a real square matrix A with n = 62. The stated property is that det(t I - A) evaluated at t = 0 is nonzero. This square matrix is invertible.\nTherefore, A is",
    "scores": [
      {
        "candidate": " invertible.",
        "candidate_id": 0,
        "score": -2.15354323387146,
        "candidate_token_ids": [
          42199,
          1238,
          13
        ],
        "candidate_length": 3,
        "prefix_tokens": 49
      },
      {
        "candidate": " singular.",
        "candidate_id": 1,
        "score": -5.63886833190918,
        "candidate_token_ids": [
          33944,
          13
        ],
        "candidate_length": 2,
        "prefix_tokens": 49
      }
    ],
    "correct_margin": 3.4853250980377197,
    "correct": true,
    "p_two_candidate_invertible": 0.9702673273408547
  },
  {
    "id": "D1_M05_0_invertible_explicit_p1_main",
    "family": "D1_M05_0",
    "cluster": "spectrum",
    "split": "heldout",
    "wording": "explicit",
    "label": 1,
    "format": "question",
    "prefix": "The object in this problem is a real square matrix A with n = 62. The stated property is that det(t I - A) evaluated at t = 0 is nonzero. This square matrix is invertible.\nIs A invertible or singular? Answer:",
    "scores": [
      {
        "candidate": " invertible.",
        "candidate_id": 0,
        "score": -5.4748759269714355,
        "candidate_token_ids": [
          42199,
          1238,
          13
        ],
        "candidate_length": 3,
        "prefix_tokens": 54
      },
      {
        "candidate": " singular.",
        "candidate_id": 1,
        "score": -5.542230129241943,
        "candidate_token_ids": [
          33944,
          13
        ],
        "candidate_length": 2,
        "prefix_tokens": 54
      }
    ],
    "correct_margin": 0.06735420227050781,
    "correct": true,
    "p_two_candidate_invertible": 0.5168321876562082
  }
]
```

## D1_M05_0_singular_description_p0_main

家族D1_M05_0；定理组spectrum；答案description；改写0；label=0；观察位置=55。

```text
Consider a real square matrix A with n = 62. It satisfies the following condition: det(t I - A) evaluated at t = 0 is zero. This is the full description for this exercise.
Summarize the mathematical object and its stated properties.
Summary:
```

token_ids：`[37175, 264, 1931, 9334, 6172, 362, 448, 308, 284, 220, 21, 17, 13, 1084, 67901, 279, 2701, 2971, 25, 3392, 1155, 358, 481, 362, 8, 25070, 518, 259, 284, 220, 15, 374, 7168, 13, 1096, 374, 279, 2480, 4008, 369, 419, 10158, 624, 9190, 5612, 551, 279, 35972, 1633, 323, 1181, 10982, 5888, 624, 19237, 25]`

### ATTN_SAE

|   atom | group   |     raw_z |
|-------:|:--------|----------:|
|   1359 | C       |  2.293647 |
|   2603 | C       |  2.900092 |
|   3198 | F       |  0.000000 |
|   4730 | F       |  0.000000 |
|   6857 | F       |  0.000000 |
|   7211 | C       | 12.345583 |
|  11707 | C       |  0.000000 |
|  11811 | C       |  3.419086 |
|  13009 | F       |  0.000000 |
|  16799 | F       |  0.000000 |
|  16947 | F       |  0.000000 |
|  20017 | C       |  2.052446 |
|  25221 | F       |  0.000000 |
|  25409 | F       |  4.471904 |
|  26105 | C       |  0.000000 |
|  27002 | C       |  4.255969 |

| arm                 |   p_invertible |     loss |   correct |
|:--------------------|---------------:|---------:|----------:|
| C                   |       0.502732 | 0.698626 |         0 |
| C_union_F           |       0.601276 | 0.919485 |         0 |
| binary_union        |       0.587837 | 0.886336 |         0 |
| location_original_h |       0.005481 | 0.005496 |         1 |

### MLPIN_SAE

|   atom | group   |     raw_z |
|-------:|:--------|----------:|
|     47 | F       |  9.185410 |
|   2104 | C       |  3.279635 |
|   2196 | C       |  0.000000 |
|   5196 | C       |  6.478675 |
|   8048 | C       |  4.163965 |
|   8856 | F       |  4.132464 |
|  10262 | F       |  0.000000 |
|  11234 | F       |  0.000000 |
|  11471 | F       |  0.000000 |
|  14879 | F       |  3.250370 |
|  18758 | C       |  4.359598 |
|  20886 | F       |  0.000000 |
|  20957 | C       | 13.684242 |
|  28024 | F       |  9.551103 |
|  29342 | C       | 46.629417 |
|  29669 | C       |  0.000000 |

| arm                 |   p_invertible |     loss |   correct |
|:--------------------|---------------:|---------:|----------:|
| C                   |       0.449378 | 0.596707 |         1 |
| C_union_F           |       0.178811 | 0.197002 |         1 |
| binary_union        |       0.315053 | 0.378413 |         1 |
| location_original_h |       0.014583 | 0.014690 |         1 |

### CC_CORRECTED

|   atom | group   |    raw_z |
|-------:|:--------|---------:|
|   1053 | F       | 0.006603 |
|   2919 | C       | 0.012993 |
|   3604 | F       | 0.000000 |
|   4828 | C       | 0.015758 |
|   5308 | F       | 0.000000 |
|   6440 | C       | 0.027537 |
|   7557 | C       | 0.146384 |
|   7803 | F       | 0.010259 |
|   8086 | C       | 0.014730 |
|   8693 | C       | 0.124491 |
|  11090 | F       | 0.000000 |
|  11318 | C       | 0.016460 |
|  12820 | F       | 0.008812 |
|  14693 | C       | 0.013296 |
|  14796 | F       | 0.000000 |
|  15445 | F       | 0.008675 |

| arm                 |   p_invertible |     loss |   correct |
|:--------------------|---------------:|---------:|----------:|
| C                   |       0.531265 | 0.757717 |         0 |
| C_union_F           |       0.007660 | 0.007689 |         1 |
| binary_union        |       0.000017 | 0.000017 |         1 |
| location_original_h |       0.006246 | 0.006266 |         1 |

### 原生完整候选得分

```json
[
  {
    "id": "D1_M05_0_singular_description_p0_main",
    "family": "D1_M05_0",
    "cluster": "spectrum",
    "split": "heldout",
    "wording": "description",
    "label": 0,
    "format": "continuation",
    "prefix": "Consider a real square matrix A with n = 62. It satisfies the following condition: det(t I - A) evaluated at t = 0 is zero. This is the full description for this exercise.\nTherefore, A is",
    "scores": [
      {
        "candidate": " invertible.",
        "candidate_id": 0,
        "score": -4.61599063873291,
        "candidate_token_ids": [
          42199,
          1238,
          13
        ],
        "candidate_length": 3,
        "prefix_tokens": 47
      },
      {
        "candidate": " singular.",
        "candidate_id": 1,
        "score": -2.7107269763946533,
        "candidate_token_ids": [
          33944,
          13
        ],
        "candidate_length": 2,
        "prefix_tokens": 47
      }
    ],
    "correct_margin": 1.9052636623382568,
    "correct": true,
    "p_two_candidate_invertible": 0.12951389071259672
  },
  {
    "id": "D1_M05_0_singular_description_p0_main",
    "family": "D1_M05_0",
    "cluster": "spectrum",
    "split": "heldout",
    "wording": "description",
    "label": 0,
    "format": "question",
    "prefix": "Consider a real square matrix A with n = 62. It satisfies the following condition: det(t I - A) evaluated at t = 0 is zero. This is the full description for this exercise.\nIs A invertible or singular? Answer:",
    "scores": [
      {
        "candidate": " invertible.",
        "candidate_id": 0,
        "score": -6.073742389678955,
        "candidate_token_ids": [
          42199,
          1238,
          13
        ],
        "candidate_length": 3,
        "prefix_tokens": 52
      },
      {
        "candidate": " singular.",
        "candidate_id": 1,
        "score": -5.66507625579834,
        "candidate_token_ids": [
          33944,
          13
        ],
        "candidate_length": 2,
        "prefix_tokens": 52
      }
    ],
    "correct_margin": 0.40866613388061523,
    "correct": true,
    "p_two_candidate_invertible": 0.39923200030907197
  }
]
```

## D1_M05_0_singular_description_p1_main

家族D1_M05_0；定理组spectrum；答案description；改写1；label=0；观察位置=59。

```text
The object in this problem is a real square matrix A with n = 62. The stated property is that det(t I - A) evaluated at t = 0 is zero. This is the full description for this exercise.
Summarize the mathematical object and its stated properties.
Summary:
```

token_ids：`[785, 1633, 304, 419, 3491, 374, 264, 1931, 9334, 6172, 362, 448, 308, 284, 220, 21, 17, 13, 576, 10982, 3343, 374, 429, 3392, 1155, 358, 481, 362, 8, 25070, 518, 259, 284, 220, 15, 374, 7168, 13, 1096, 374, 279, 2480, 4008, 369, 419, 10158, 624, 9190, 5612, 551, 279, 35972, 1633, 323, 1181, 10982, 5888, 624, 19237, 25]`

### ATTN_SAE

|   atom | group   |     raw_z |
|-------:|:--------|----------:|
|   1359 | C       |  0.000000 |
|   2603 | C       |  2.921905 |
|   3198 | F       |  0.000000 |
|   4730 | F       |  2.377812 |
|   6857 | F       |  0.000000 |
|   7211 | C       | 14.100141 |
|  11707 | C       |  0.000000 |
|  11811 | C       |  2.504362 |
|  13009 | F       |  0.000000 |
|  16799 | F       |  0.000000 |
|  16947 | F       |  0.000000 |
|  20017 | C       |  0.000000 |
|  25221 | F       |  0.000000 |
|  25409 | F       |  7.276264 |
|  26105 | C       |  0.000000 |
|  27002 | C       |  2.654257 |

| arm                 |   p_invertible |     loss |   correct |
|:--------------------|---------------:|---------:|----------:|
| C                   |       0.401976 | 0.514125 |         1 |
| C_union_F           |       0.552786 | 0.804718 |         0 |
| binary_union        |       0.510378 | 0.714121 |         0 |
| location_original_h |       0.990265 | 4.631997 |         0 |

### MLPIN_SAE

|   atom | group   |     raw_z |
|-------:|:--------|----------:|
|     47 | F       |  7.722024 |
|   2104 | C       |  3.582583 |
|   2196 | C       |  0.000000 |
|   5196 | C       | 10.283773 |
|   8048 | C       |  6.226080 |
|   8856 | F       |  7.766532 |
|  10262 | F       |  0.000000 |
|  11234 | F       |  0.000000 |
|  11471 | F       |  0.000000 |
|  14879 | F       |  0.000000 |
|  18758 | C       |  4.234501 |
|  20886 | F       |  0.000000 |
|  20957 | C       | 13.180900 |
|  28024 | F       |  8.688347 |
|  29342 | C       | 43.981800 |
|  29669 | C       |  0.000000 |

| arm                 |   p_invertible |     loss |   correct |
|:--------------------|---------------:|---------:|----------:|
| C                   |       0.388403 | 0.491682 |         1 |
| C_union_F           |       0.189703 | 0.210355 |         1 |
| binary_union        |       0.795312 | 1.586270 |         0 |
| location_original_h |       0.996728 | 5.722356 |         0 |

### CC_CORRECTED

|   atom | group   |    raw_z |
|-------:|:--------|---------:|
|   1053 | F       | 0.000000 |
|   2919 | C       | 0.018419 |
|   3604 | F       | 0.000000 |
|   4828 | C       | 0.016557 |
|   5308 | F       | 0.000000 |
|   6440 | C       | 0.033559 |
|   7557 | C       | 0.149387 |
|   7803 | F       | 0.007872 |
|   8086 | C       | 0.000000 |
|   8693 | C       | 0.085135 |
|  11090 | F       | 0.000000 |
|  11318 | C       | 0.029514 |
|  12820 | F       | 0.000000 |
|  14693 | C       | 0.013738 |
|  14796 | F       | 0.000000 |
|  15445 | F       | 0.000000 |

| arm                 |   p_invertible |     loss |   correct |
|:--------------------|---------------:|---------:|----------:|
| C                   |       0.308349 | 0.368675 |         1 |
| C_union_F           |       0.996861 | 5.763741 |         0 |
| binary_union        |       0.000461 | 0.000461 |         1 |
| location_original_h |       0.992794 | 4.932838 |         0 |

### 原生完整候选得分

```json
[
  {
    "id": "D1_M05_0_singular_description_p1_main",
    "family": "D1_M05_0",
    "cluster": "spectrum",
    "split": "heldout",
    "wording": "description",
    "label": 0,
    "format": "continuation",
    "prefix": "The object in this problem is a real square matrix A with n = 62. The stated property is that det(t I - A) evaluated at t = 0 is zero. This is the full description for this exercise.\nTherefore, A is",
    "scores": [
      {
        "candidate": " invertible.",
        "candidate_id": 0,
        "score": -4.181917667388916,
        "candidate_token_ids": [
          42199,
          1238,
          13
        ],
        "candidate_length": 3,
        "prefix_tokens": 51
      },
      {
        "candidate": " singular.",
        "candidate_id": 1,
        "score": -2.6524505615234375,
        "candidate_token_ids": [
          33944,
          13
        ],
        "candidate_length": 2,
        "prefix_tokens": 51
      }
    ],
    "correct_margin": 1.5294671058654785,
    "correct": true,
    "p_two_candidate_invertible": 0.17807166793699916
  },
  {
    "id": "D1_M05_0_singular_description_p1_main",
    "family": "D1_M05_0",
    "cluster": "spectrum",
    "split": "heldout",
    "wording": "description",
    "label": 0,
    "format": "question",
    "prefix": "The object in this problem is a real square matrix A with n = 62. The stated property is that det(t I - A) evaluated at t = 0 is zero. This is the full description for this exercise.\nIs A invertible or singular? Answer:",
    "scores": [
      {
        "candidate": " invertible.",
        "candidate_id": 0,
        "score": -6.002040863037109,
        "candidate_token_ids": [
          42199,
          1238,
          13
        ],
        "candidate_length": 3,
        "prefix_tokens": 56
      },
      {
        "candidate": " singular.",
        "candidate_id": 1,
        "score": -5.751153945922852,
        "candidate_token_ids": [
          33944,
          13
        ],
        "candidate_length": 2,
        "prefix_tokens": 56
      }
    ],
    "correct_margin": 0.2508869171142578,
    "correct": true,
    "p_two_candidate_invertible": 0.43760521063573504
  }
]
```

## D1_M05_0_singular_explicit_p0_main

家族D1_M05_0；定理组spectrum；答案explicit；改写0；label=0；观察位置=52。

```text
Consider a real square matrix A with n = 62. It satisfies the following condition: det(t I - A) evaluated at t = 0 is zero. This square matrix is singular.
Summarize the mathematical object and its stated properties.
Summary:
```

token_ids：`[37175, 264, 1931, 9334, 6172, 362, 448, 308, 284, 220, 21, 17, 13, 1084, 67901, 279, 2701, 2971, 25, 3392, 1155, 358, 481, 362, 8, 25070, 518, 259, 284, 220, 15, 374, 7168, 13, 1096, 9334, 6172, 374, 33944, 624, 9190, 5612, 551, 279, 35972, 1633, 323, 1181, 10982, 5888, 624, 19237, 25]`

### ATTN_SAE

|   atom | group   |     raw_z |
|-------:|:--------|----------:|
|   1359 | C       |  2.303865 |
|   2603 | C       |  2.643312 |
|   3198 | F       |  0.000000 |
|   4730 | F       |  4.391024 |
|   6857 | F       |  3.149176 |
|   7211 | C       | 10.789186 |
|  11707 | C       |  2.940666 |
|  11811 | C       |  2.642590 |
|  13009 | F       |  3.316371 |
|  16799 | F       |  0.000000 |
|  16947 | F       |  0.000000 |
|  20017 | C       |  2.553629 |
|  25221 | F       |  0.000000 |
|  25409 | F       |  3.638327 |
|  26105 | C       |  3.477154 |
|  27002 | C       |  0.000000 |

| arm                 |   p_invertible |     loss |   correct |
|:--------------------|---------------:|---------:|----------:|
| C                   |       0.417097 | 0.539735 |         1 |
| C_union_F           |       0.385753 | 0.487359 |         1 |
| binary_union        |       0.368381 | 0.459469 |         1 |
| location_original_h |       0.000176 | 0.000176 |         1 |

### MLPIN_SAE

|   atom | group   |     raw_z |
|-------:|:--------|----------:|
|     47 | F       |  9.919621 |
|   2104 | C       |  2.954401 |
|   2196 | C       |  0.000000 |
|   5196 | C       |  6.650310 |
|   8048 | C       |  5.924777 |
|   8856 | F       |  0.000000 |
|  10262 | F       |  3.219536 |
|  11234 | F       |  0.000000 |
|  11471 | F       |  2.772379 |
|  14879 | F       |  0.000000 |
|  18758 | C       |  5.295190 |
|  20886 | F       |  0.000000 |
|  20957 | C       | 11.568068 |
|  28024 | F       | 10.024366 |
|  29342 | C       | 44.978344 |
|  29669 | C       |  0.000000 |

| arm                 |   p_invertible |     loss |   correct |
|:--------------------|---------------:|---------:|----------:|
| C                   |       0.435734 | 0.572230 |         1 |
| C_union_F           |       0.085211 | 0.089062 |         1 |
| binary_union        |       0.017474 | 0.017629 |         1 |
| location_original_h |       0.000977 | 0.000977 |         1 |

### CC_CORRECTED

|   atom | group   |    raw_z |
|-------:|:--------|---------:|
|   1053 | F       | 0.009465 |
|   2919 | C       | 0.026084 |
|   3604 | F       | 0.031405 |
|   4828 | C       | 0.016282 |
|   5308 | F       | 0.013870 |
|   6440 | C       | 0.033060 |
|   7557 | C       | 0.146823 |
|   7803 | F       | 0.013926 |
|   8086 | C       | 0.013421 |
|   8693 | C       | 0.067032 |
|  11090 | F       | 0.014601 |
|  11318 | C       | 0.026177 |
|  12820 | F       | 0.010163 |
|  14693 | C       | 0.014142 |
|  14796 | F       | 0.014409 |
|  15445 | F       | 0.016963 |

| arm                 |   p_invertible |     loss |   correct |
|:--------------------|---------------:|---------:|----------:|
| C                   |       0.406683 | 0.522026 |         1 |
| C_union_F           |       0.000150 | 0.000150 |         1 |
| binary_union        |       0.000000 | 0.000000 |         1 |
| location_original_h |       0.000584 | 0.000584 |         1 |

### 原生完整候选得分

```json
[
  {
    "id": "D1_M05_0_singular_explicit_p0_main",
    "family": "D1_M05_0",
    "cluster": "spectrum",
    "split": "heldout",
    "wording": "explicit",
    "label": 0,
    "format": "continuation",
    "prefix": "Consider a real square matrix A with n = 62. It satisfies the following condition: det(t I - A) evaluated at t = 0 is zero. This square matrix is singular.\nTherefore, A is",
    "scores": [
      {
        "candidate": " invertible.",
        "candidate_id": 0,
        "score": -4.539767742156982,
        "candidate_token_ids": [
          42199,
          1238,
          13
        ],
        "candidate_length": 3,
        "prefix_tokens": 44
      },
      {
        "candidate": " singular.",
        "candidate_id": 1,
        "score": -2.5796680450439453,
        "candidate_token_ids": [
          33944,
          13
        ],
        "candidate_length": 2,
        "prefix_tokens": 44
      }
    ],
    "correct_margin": 1.960099697113037,
    "correct": true,
    "p_two_candidate_invertible": 0.12345625845599122
  },
  {
    "id": "D1_M05_0_singular_explicit_p0_main",
    "family": "D1_M05_0",
    "cluster": "spectrum",
    "split": "heldout",
    "wording": "explicit",
    "label": 0,
    "format": "question",
    "prefix": "Consider a real square matrix A with n = 62. It satisfies the following condition: det(t I - A) evaluated at t = 0 is zero. This square matrix is singular.\nIs A invertible or singular? Answer:",
    "scores": [
      {
        "candidate": " invertible.",
        "candidate_id": 0,
        "score": -6.4731221199035645,
        "candidate_token_ids": [
          42199,
          1238,
          13
        ],
        "candidate_length": 3,
        "prefix_tokens": 49
      },
      {
        "candidate": " singular.",
        "candidate_id": 1,
        "score": -5.840859889984131,
        "candidate_token_ids": [
          33944,
          13
        ],
        "candidate_length": 2,
        "prefix_tokens": 49
      }
    ],
    "correct_margin": 0.6322622299194336,
    "correct": true,
    "p_two_candidate_invertible": 0.3469977611506472
  }
]
```

## D1_M05_0_singular_explicit_p1_main

家族D1_M05_0；定理组spectrum；答案explicit；改写1；label=0；观察位置=56。

```text
The object in this problem is a real square matrix A with n = 62. The stated property is that det(t I - A) evaluated at t = 0 is zero. This square matrix is singular.
Summarize the mathematical object and its stated properties.
Summary:
```

token_ids：`[785, 1633, 304, 419, 3491, 374, 264, 1931, 9334, 6172, 362, 448, 308, 284, 220, 21, 17, 13, 576, 10982, 3343, 374, 429, 3392, 1155, 358, 481, 362, 8, 25070, 518, 259, 284, 220, 15, 374, 7168, 13, 1096, 9334, 6172, 374, 33944, 624, 9190, 5612, 551, 279, 35972, 1633, 323, 1181, 10982, 5888, 624, 19237, 25]`

### ATTN_SAE

|   atom | group   |     raw_z |
|-------:|:--------|----------:|
|   1359 | C       |  0.000000 |
|   2603 | C       |  2.774101 |
|   3198 | F       |  0.000000 |
|   4730 | F       |  5.031419 |
|   6857 | F       |  0.000000 |
|   7211 | C       | 13.423867 |
|  11707 | C       |  3.741635 |
|  11811 | C       |  0.000000 |
|  13009 | F       |  2.700259 |
|  16799 | F       |  0.000000 |
|  16947 | F       |  0.000000 |
|  20017 | C       |  0.000000 |
|  25221 | F       |  0.000000 |
|  25409 | F       |  6.531425 |
|  26105 | C       |  2.627622 |
|  27002 | C       |  0.000000 |

| arm                 |   p_invertible |     loss |   correct |
|:--------------------|---------------:|---------:|----------:|
| C                   |       0.352155 | 0.434104 |         1 |
| C_union_F           |       0.463781 | 0.623213 |         1 |
| binary_union        |       0.441001 | 0.581607 |         1 |
| location_original_h |       0.262174 | 0.304047 |         1 |

### MLPIN_SAE

|   atom | group   |     raw_z |
|-------:|:--------|----------:|
|     47 | F       |  7.577167 |
|   2104 | C       |  3.836411 |
|   2196 | C       |  0.000000 |
|   5196 | C       |  9.779281 |
|   8048 | C       |  7.471858 |
|   8856 | F       |  5.751637 |
|  10262 | F       |  3.347433 |
|  11234 | F       |  0.000000 |
|  11471 | F       |  0.000000 |
|  14879 | F       |  0.000000 |
|  18758 | C       |  3.898577 |
|  20886 | F       |  0.000000 |
|  20957 | C       | 12.040065 |
|  28024 | F       |  9.321725 |
|  29342 | C       | 44.107906 |
|  29669 | C       |  0.000000 |

| arm                 |   p_invertible |     loss |   correct |
|:--------------------|---------------:|---------:|----------:|
| C                   |       0.419385 | 0.543667 |         1 |
| C_union_F           |       0.112237 | 0.119050 |         1 |
| binary_union        |       0.563719 | 0.829468 |         0 |
| location_original_h |       0.442073 | 0.583527 |         1 |

### CC_CORRECTED

|   atom | group   |    raw_z |
|-------:|:--------|---------:|
|   1053 | F       | 0.000000 |
|   2919 | C       | 0.022840 |
|   3604 | F       | 0.025774 |
|   4828 | C       | 0.019849 |
|   5308 | F       | 0.000000 |
|   6440 | C       | 0.043053 |
|   7557 | C       | 0.148077 |
|   7803 | F       | 0.011765 |
|   8086 | C       | 0.000000 |
|   8693 | C       | 0.059426 |
|  11090 | F       | 0.014064 |
|  11318 | C       | 0.023724 |
|  12820 | F       | 0.000000 |
|  14693 | C       | 0.015291 |
|  14796 | F       | 0.000000 |
|  15445 | F       | 0.011146 |

| arm                 |   p_invertible |     loss |   correct |
|:--------------------|---------------:|---------:|----------:|
| C                   |       0.389914 | 0.494156 |         1 |
| C_union_F           |       0.981759 | 4.004089 |         0 |
| binary_union        |       0.000035 | 0.000035 |         1 |
| location_original_h |       0.369994 | 0.462026 |         1 |

### 原生完整候选得分

```json
[
  {
    "id": "D1_M05_0_singular_explicit_p1_main",
    "family": "D1_M05_0",
    "cluster": "spectrum",
    "split": "heldout",
    "wording": "explicit",
    "label": 0,
    "format": "continuation",
    "prefix": "The object in this problem is a real square matrix A with n = 62. The stated property is that det(t I - A) evaluated at t = 0 is zero. This square matrix is singular.\nTherefore, A is",
    "scores": [
      {
        "candidate": " invertible.",
        "candidate_id": 0,
        "score": -4.758119106292725,
        "candidate_token_ids": [
          42199,
          1238,
          13
        ],
        "candidate_length": 3,
        "prefix_tokens": 48
      },
      {
        "candidate": " singular.",
        "candidate_id": 1,
        "score": -2.249527931213379,
        "candidate_token_ids": [
          33944,
          13
        ],
        "candidate_length": 2,
        "prefix_tokens": 48
      }
    ],
    "correct_margin": 2.5085911750793457,
    "correct": true,
    "p_two_candidate_invertible": 0.07525809703797318
  },
  {
    "id": "D1_M05_0_singular_explicit_p1_main",
    "family": "D1_M05_0",
    "cluster": "spectrum",
    "split": "heldout",
    "wording": "explicit",
    "label": 0,
    "format": "question",
    "prefix": "The object in this problem is a real square matrix A with n = 62. The stated property is that det(t I - A) evaluated at t = 0 is zero. This square matrix is singular.\nIs A invertible or singular? Answer:",
    "scores": [
      {
        "candidate": " invertible.",
        "candidate_id": 0,
        "score": -5.300838470458984,
        "candidate_token_ids": [
          42199,
          1238,
          13
        ],
        "candidate_length": 3,
        "prefix_tokens": 53
      },
      {
        "candidate": " singular.",
        "candidate_id": 1,
        "score": -5.317347049713135,
        "candidate_token_ids": [
          33944,
          13
        ],
        "candidate_length": 2,
        "prefix_tokens": 53
      }
    ],
    "correct_margin": -0.01650857925415039,
    "correct": false,
    "p_two_candidate_invertible": 0.5041270510840973
  }
]
```

## 固定失败：二值并不总是更好

D1_M05_0可逆、无答案、改写0：MLPIN连续可逆概率0.209771、二值0.315053，均错；CC连续0.642636正确，但二值0.001928高置信错。连续强度并非一律更差，二值也不是通用修复。正文结论始终使用logloss及冻结比较，不按这一个例子改指标。

## 原R17固定错误与正确例

这些实例在旧诊断阶段固定，含最坏错误、分组正确例和M05_0，不用于新候选选择。

### M05_0_invertible_description

```text
Let A be a real array with 22 rows and 22 columns. For this array, zero is not an eigenvalue.
Summarize the mathematical object and its stated properties.
Summary:
```

tokens: `41`

| arm             |   p_invertible |   signed_margin |   correct |     loss |    Brier |
|:----------------|---------------:|----------------:|----------:|---------:|---------:|
| C               |       0.537335 |        0.149618 |         1 | 0.621134 | 0.214059 |
| C_union_F       |       0.499885 |       -0.000461 |         0 | 0.693378 | 0.250115 |
| binary_union    |       0.009743 |       -4.621451 |         0 | 4.631241 | 0.980610 |
| best_single     |       0.197195 |       -1.403920 |         0 | 1.623563 | 0.644496 |
| full_continuous |       0.160086 |       -1.657586 |         0 | 1.832042 | 0.705455 |
| H               |       0.033993 |       -3.347019 |         0 | 3.381603 | 0.933170 |
| b_r             |       0.501037 |        0.004150 |         1 | 0.691074 | 0.248964 |
| q_b_r           |       0.652998 |        0.632245 |         1 | 0.426181 | 0.120410 |

### M05_0_singular_description

```text
Let A be a real array with 22 rows and 22 columns. For this array, zero is an eigenvalue.
Summarize the mathematical object and its stated properties.
Summary:
```

tokens: `40`

| arm             |   p_invertible |   signed_margin |   correct |     loss |    Brier |
|:----------------|---------------:|----------------:|----------:|---------:|---------:|
| C               |       0.537640 |       -0.150845 |         0 | 0.771411 | 0.289057 |
| C_union_F       |       0.967111 |       -3.381172 |         0 | 3.414614 | 0.935303 |
| binary_union    |       0.348851 |        0.624094 |         1 | 0.429017 | 0.121697 |
| best_single     |       0.852874 |       -1.757326 |         0 | 1.916469 | 0.727395 |
| full_continuous |       0.054539 |        2.852756 |         1 | 0.056083 | 0.002975 |
| H               |       0.318822 |        0.759190 |         1 | 0.383932 | 0.101648 |
| b_r             |       0.500843 |       -0.003370 |         0 | 0.694834 | 0.250843 |
| q_b_r           |       0.623741 |       -0.505459 |         0 | 0.977479 | 0.389053 |

### M05_1_invertible_description

```text
Let A be a real array with 23 rows and 23 columns. For this array, all of its complex eigenvalues are nonzero.
Summarize the mathematical object and its stated properties.
Summary:
```

tokens: `43`

| arm             |   p_invertible |   signed_margin |   correct |     loss |    Brier |
|:----------------|---------------:|----------------:|----------:|---------:|---------:|
| C               |       0.654117 |        0.637185 |         1 | 0.424469 | 0.119635 |
| C_union_F       |       0.841465 |        1.669171 |         1 | 0.172611 | 0.025133 |
| binary_union    |       0.685298 |        0.778226 |         1 | 0.377902 | 0.099038 |
| best_single     |       0.852874 |        1.757326 |         1 | 0.159143 | 0.021646 |
| full_continuous |       0.890426 |        2.095104 |         1 | 0.116055 | 0.012006 |
| H               |       0.795764 |        1.360025 |         1 | 0.228453 | 0.041712 |
| b_r             |       0.529172 |        0.116821 |         1 | 0.636442 | 0.221679 |
| q_b_r           |       0.577477 |        0.312424 |         1 | 0.549087 | 0.178526 |

### M05_1_singular_description

```text
Let A be a real array with 23 rows and 23 columns. For this array, at least one of its complex eigenvalues is zero.
Summarize the mathematical object and its stated properties.
Summary:
```

tokens: `45`

| arm             |   p_invertible |   signed_margin |   correct |     loss |    Brier |
|:----------------|---------------:|----------------:|----------:|---------:|---------:|
| C               |       0.546337 |       -0.185883 |         0 | 0.790401 | 0.298484 |
| C_union_F       |       0.038409 |        3.220302 |         1 | 0.039166 | 0.001475 |
| binary_union    |       0.017953 |        4.001877 |         1 | 0.018116 | 0.000322 |
| best_single     |       0.151624 |        1.721920 |         1 | 0.164431 | 0.022990 |
| full_continuous |       0.065911 |        2.651266 |         1 | 0.068184 | 0.004344 |
| H               |       0.061580 |        2.723854 |         1 | 0.063558 | 0.003792 |
| b_r             |       0.500022 |       -0.000089 |         0 | 0.693192 | 0.250022 |
| q_b_r           |       0.663731 |       -0.679965 |         0 | 1.089844 | 0.440539 |

### M05_3_invertible_description

```text
Let A be a real array with 25 rows and 25 columns. For this array, the constant coefficient of its characteristic polynomial is nonzero.
Summarize the mathematical object and its stated properties.
Summary:
```

tokens: `44`

| arm             |   p_invertible |   signed_margin |   correct |     loss |    Brier |
|:----------------|---------------:|----------------:|----------:|---------:|---------:|
| C               |       0.535223 |        0.141127 |         1 | 0.625071 | 0.216017 |
| C_union_F       |       0.306492 |       -0.816570 |         0 | 1.182563 | 0.480953 |
| binary_union    |       0.262359 |       -1.033746 |         0 | 1.338043 | 0.544115 |
| best_single     |       0.852874 |        1.757326 |         1 | 0.159143 | 0.021646 |
| full_continuous |       0.373775 |       -0.516055 |         0 | 0.984101 | 0.392158 |
| H               |       0.788666 |        1.316901 |         1 | 0.237413 | 0.044662 |
| b_r             |       0.526074 |        0.104392 |         1 | 0.642313 | 0.224606 |
| q_b_r           |       0.310137 |       -0.799477 |         0 | 1.170740 | 0.475911 |

### M05_3_singular_description

```text
Let A be a real array with 25 rows and 25 columns. For this array, the constant coefficient of its characteristic polynomial is zero.
Summarize the mathematical object and its stated properties.
Summary:
```

tokens: `44`

| arm             |   p_invertible |   signed_margin |   correct |     loss |    Brier |
|:----------------|---------------:|----------------:|----------:|---------:|---------:|
| C               |       0.413790 |        0.348318 |         1 | 0.534078 | 0.171222 |
| C_union_F       |       0.671208 |       -0.713653 |         0 | 1.112329 | 0.450520 |
| binary_union    |       0.498870 |        0.004521 |         1 | 0.690889 | 0.248871 |
| best_single     |       0.852874 |       -1.757326 |         0 | 1.916469 | 0.727395 |
| full_continuous |       0.033819 |        3.352341 |         1 | 0.034404 | 0.001144 |
| H               |       0.756018 |       -1.130971 |         0 | 1.410661 | 0.571563 |
| b_r             |       0.497785 |        0.008862 |         1 | 0.688726 | 0.247789 |
| q_b_r           |       0.282698 |        0.931117 |         1 | 0.332259 | 0.079918 |

### M06_0_invertible_description

```text
Let A be a real array with 26 rows and 26 columns. For this array, Gaussian elimination gives a pivot in every column.
Summarize the mathematical object and its stated properties.
Summary:
```

tokens: `43`

| arm             |   p_invertible |   signed_margin |   correct |     loss |    Brier |
|:----------------|---------------:|----------------:|----------:|---------:|---------:|
| C               |       0.763733 |        1.173257 |         1 | 0.269537 | 0.055822 |
| C_union_F       |       0.999367 |        7.364835 |         1 | 0.000633 | 0.000000 |
| binary_union    |       0.981307 |        3.960720 |         1 | 0.018870 | 0.000349 |
| best_single     |       0.852874 |        1.757326 |         1 | 0.159143 | 0.021646 |
| full_continuous |       0.609790 |        0.446431 |         1 | 0.494640 | 0.152264 |
| H               |       0.571428 |        0.287680 |         1 | 0.559616 | 0.183674 |
| b_r             |       0.530293 |        0.121323 |         1 | 0.634325 | 0.220624 |
| q_b_r           |       0.853798 |        1.764704 |         1 | 0.158061 | 0.021375 |

### M06_0_singular_description

```text
Let A be a real array with 26 rows and 26 columns. For this array, Gaussian elimination leaves a column without a pivot.
Summarize the mathematical object and its stated properties.
Summary:
```

tokens: `43`

| arm             |   p_invertible |   signed_margin |   correct |     loss |    Brier |
|:----------------|---------------:|----------------:|----------:|---------:|---------:|
| C               |       0.744616 |       -1.070103 |         0 | 1.364989 | 0.554454 |
| C_union_F       |       0.000329 |        8.017877 |         1 | 0.000329 | 0.000000 |
| binary_union    |       0.085936 |        2.364299 |         1 | 0.089855 | 0.007385 |
| best_single     |       0.003345 |        5.696914 |         1 | 0.003351 | 0.000011 |
| full_continuous |       0.006154 |        5.084414 |         1 | 0.006173 | 0.000038 |
| H               |       0.000254 |        8.279229 |         1 | 0.000254 | 0.000000 |
| b_r             |       0.528057 |       -0.112347 |         0 | 0.750898 | 0.278845 |
| q_b_r           |       0.863734 |       -1.846658 |         0 | 1.993148 | 0.746037 |

### M06_3_singular_description

```text
Let A be a real array with 29 rows and 29 columns. Let n denote its number of rows. For this array, its row echelon form has fewer than n nonzero rows.
Summarize the mathematical object and its stated properties.
Summary:
```

tokens: `54`

| arm             |   p_invertible |   signed_margin |   correct |      loss |    Brier |
|:----------------|---------------:|----------------:|----------:|----------:|---------:|
| C               |       0.835246 |       -1.623272 |         0 |  1.803301 | 0.697636 |
| C_union_F       |       0.999994 |      -12.052008 |         0 | 12.052013 | 0.999988 |
| binary_union    |       0.913377 |       -2.355578 |         0 |  2.446185 | 0.834257 |
| best_single     |       0.852874 |       -1.757326 |         0 |  1.916469 | 0.727395 |
| full_continuous |       0.166482 |        1.610770 |         1 |  0.182100 | 0.027716 |
| H               |       0.805484 |       -1.420927 |         0 |  1.637239 | 0.648804 |
| b_r             |       0.556388 |       -0.226516 |         0 |  0.812805 | 0.309568 |
| q_b_r           |       0.860177 |       -1.816760 |         0 |  1.967377 | 0.739904 |

### M08_0_invertible_description

```text
Let A be a real array with 34 rows and 34 columns. Let n denote its number of rows. For this array, it maps an n dimensional unit cube to a body with positive n dimensional volume.
Summarize the mathematical object and its stated properties.
Summary:
```

tokens: `58`

| arm             |   p_invertible |   signed_margin |   correct |     loss |    Brier |
|:----------------|---------------:|----------------:|----------:|---------:|---------:|
| C               |       0.607079 |        0.435050 |         1 | 0.499097 | 0.154387 |
| C_union_F       |       0.760392 |        1.154831 |         1 | 0.273921 | 0.057412 |
| binary_union    |       0.876860 |        1.963022 |         1 | 0.131408 | 0.015164 |
| best_single     |       0.852874 |        1.757326 |         1 | 0.159143 | 0.021646 |
| full_continuous |       0.889093 |        2.081509 |         1 | 0.117554 | 0.012300 |
| H               |       0.813915 |        1.475653 |         1 | 0.205899 | 0.034628 |
| b_r             |       0.493871 |       -0.024519 |         0 | 0.705482 | 0.256167 |
| q_b_r           |       0.787424 |        1.309465 |         1 | 0.238989 | 0.045189 |

### M08_0_singular_description

```text
Let A be a real array with 34 rows and 34 columns. Let n denote its number of rows. For this array, it maps an n dimensional unit cube to a body with zero n dimensional volume.
Summarize the mathematical object and its stated properties.
Summary:
```

tokens: `58`

| arm             |   p_invertible |   signed_margin |   correct |     loss |    Brier |
|:----------------|---------------:|----------------:|----------:|---------:|---------:|
| C               |       0.519195 |       -0.076818 |         0 | 0.732294 | 0.269564 |
| C_union_F       |       0.962455 |       -3.243942 |         0 | 3.282210 | 0.926319 |
| binary_union    |       0.972196 |       -3.554395 |         0 | 3.582592 | 0.945166 |
| best_single     |       0.852874 |       -1.757326 |         0 | 1.916469 | 0.727395 |
| full_continuous |       0.545769 |       -0.183589 |         0 | 0.789149 | 0.297864 |
| H               |       0.825846 |       -1.556471 |         0 | 1.747818 | 0.682022 |
| b_r             |       0.481490 |        0.074074 |         1 | 0.656796 | 0.231833 |
| q_b_r           |       0.527312 |       -0.109357 |         0 | 0.749320 | 0.278058 |

### M08_1_singular_description

```text
Let A be a real array with 35 rows and 35 columns. For this array, it maps some two different points to the same point.
Summarize the mathematical object and its stated properties.
Summary:
```

tokens: `45`

| arm             |   p_invertible |   signed_margin |   correct |     loss |    Brier |
|:----------------|---------------:|----------------:|----------:|---------:|---------:|
| C               |       0.532151 |       -0.128781 |         0 | 0.759610 | 0.283185 |
| C_union_F       |       0.000094 |        9.269273 |         1 | 0.000094 | 0.000000 |
| binary_union    |       0.115645 |        2.034335 |         1 | 0.122897 | 0.013374 |
| best_single     |       0.099848 |        2.198919 |         1 | 0.105191 | 0.009970 |
| full_continuous |       0.145486 |        1.770451 |         1 | 0.157223 | 0.021166 |
| H               |       0.016196 |        4.106652 |         1 | 0.016329 | 0.000262 |
| b_r             |       0.494470 |        0.022120 |         1 | 0.682148 | 0.244501 |
| q_b_r           |       0.530654 |       -0.122771 |         0 | 0.756416 | 0.281594 |

### M08_3_singular_description

```text
Let A be a real array with 37 rows and 37 columns. Let n denote its number of rows. For this array, it takes no basis of R^n to a basis of R^n.
Summarize the mathematical object and its stated properties.
Summary:
```

tokens: `56`

| arm             |   p_invertible |   signed_margin |   correct |     loss |    Brier |
|:----------------|---------------:|----------------:|----------:|---------:|---------:|
| C               |       0.546042 |       -0.184692 |         0 | 0.789751 | 0.298162 |
| C_union_F       |       0.995740 |       -5.454235 |         0 | 5.458504 | 0.991498 |
| binary_union    |       0.760888 |       -1.157555 |         0 | 1.430824 | 0.578951 |
| best_single     |       0.852874 |       -1.757326 |         0 | 1.916469 | 0.727395 |
| full_continuous |       0.517983 |       -0.071965 |         0 | 0.729777 | 0.268307 |
| H               |       0.798535 |       -1.377160 |         0 | 1.602137 | 0.637657 |
| b_r             |       0.497930 |        0.008281 |         1 | 0.689015 | 0.247934 |
| q_b_r           |       0.668583 |       -0.701784 |         0 | 1.104379 | 0.447004 |

## H4标注修复与仍未知的实例

已知控制包含“n rows and n columns”“nonzero null vector”等旧规则漏检，控制表保存逐例旧新标签。自然富集的funcall博客包含“invertible 2×2 matrices / determinant±1”；MathWorks正定矩阵内容可给可逆证书。另一段同时含可逆P与奇异(lambda I−H)，对象不唯一，保留undetermined，不强行赋细标签。只有2篇可逆、没有可明确奇异篇，不能估计稳健语义敏感性。

[盲文本与审核目录](../../../../../../../../../../UNAVAILABLE.md)；[富集可见全文](../../../../../../../../../../UNAVAILABLE.md)。
