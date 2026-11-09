# 36条受控文本与两格式全部分数

[中文小结](summary_cn.md) · [精确候选与问法](data/formats.json) · [全部原始记录](results/raw_scores.jsonl)

所有行的“是否方阵”标签均为是。奇异性未知指给定文本不足以判断。各行独立，不能把一个家族的三条描述当成同时成立。分数是完整候选条件自然对数概率之和，越大越优；各格式按自己的候选文本评分，不跨格式比较分数大小。表仅显示6位小数，原始记录保留完整精度。

## F01 — exercise

**方阵／奇异性未知**；方阵=是，奇异性=无法确定；性质词=square。

```text
In this exercise, A is a square matrix.
```

**奇异方阵**；方阵=是，奇异性=是；性质词=singular, square。

```text
In this exercise, A is a singular square matrix.
```

**可逆方阵**；方阵=是，奇异性=否；性质词=invertible, square。

```text
In this exercise, A is an invertible square matrix.
```

| 条件             | 正确     |     F1 是 |     F1 否 |   F1 无法确定 | F1 首选   | F1 正确   |   F2 无法确定 |     F2 否 |     F2 是 | F2 首选      | F2 正确   |
|:-----------------|:---------|----------:|----------:|--------------:|:----------|:----------|--------------:|----------:|----------:|:-------------|:----------|
| 方阵／奇异性未知 | 无法确定 | -4.104760 | -3.734506 |     -5.450908 | 否。      | False     |     -8.880637 | -4.928067 | -4.076306 | 是奇异矩阵。 | False     |
| 奇异方阵         | 是       | -3.768594 | -3.928887 |     -5.543122 | 是。      | True      |     -9.315206 | -4.615188 | -4.006439 | 是奇异矩阵。 | True      |
| 可逆方阵         | 否       | -4.056310 | -3.650422 |     -5.445818 | 否。      | True      |     -9.035015 | -4.793479 | -3.811600 | 是奇异矩阵。 | False     |

## F02 — problem statement

**方阵／奇异性未知**；方阵=是，奇异性=无法确定；性质词=square。

```text
The problem statement specifies that A is a square matrix.
```

**奇异方阵**；方阵=是，奇异性=是；性质词=singular, square。

```text
The problem statement specifies that A is a singular square matrix.
```

**可逆方阵**；方阵=是，奇异性=否；性质词=invertible, square。

```text
The problem statement specifies that A is an invertible square matrix.
```

| 条件             | 正确     |     F1 是 |     F1 否 |   F1 无法确定 | F1 首选   | F1 正确   |   F2 无法确定 |     F2 否 |     F2 是 | F2 首选      | F2 正确   |
|:-----------------|:---------|----------:|----------:|--------------:|:----------|:----------|--------------:|----------:|----------:|:-------------|:----------|
| 方阵／奇异性未知 | 无法确定 | -3.822060 | -2.753779 |     -5.092615 | 否。      | False     |     -5.512918 | -4.255424 | -2.735721 | 是奇异矩阵。 | False     |
| 奇异方阵         | 是       | -3.437941 | -2.834659 |     -5.567708 | 否。      | False     |     -5.755725 | -4.052802 | -2.735824 | 是奇异矩阵。 | True      |
| 可逆方阵         | 否       | -4.098651 | -2.525057 |     -5.583685 | 否。      | True      |     -5.728845 | -4.342711 | -2.698351 | 是奇异矩阵。 | False     |

## F03 — section example

**方阵／奇异性未知**；方阵=是，奇异性=无法确定；性质词=square。

```text
Let A be a square matrix for the example in this section.
```

**奇异方阵**；方阵=是，奇异性=是；性质词=singular, square。

```text
Let A be a singular square matrix for the example in this section.
```

**可逆方阵**；方阵=是，奇异性=否；性质词=invertible, square。

```text
Let A be an invertible square matrix for the example in this section.
```

| 条件             | 正确     |     F1 是 |     F1 否 |   F1 无法确定 | F1 首选   | F1 正确   |   F2 无法确定 |     F2 否 |     F2 是 | F2 首选      | F2 正确   |
|:-----------------|:---------|----------:|----------:|--------------:|:----------|:----------|--------------:|----------:|----------:|:-------------|:----------|
| 方阵／奇异性未知 | 无法确定 | -3.940887 | -3.330365 |     -5.205065 | 否。      | False     |     -6.567378 | -4.426528 | -3.386369 | 是奇异矩阵。 | False     |
| 奇异方阵         | 是       | -3.559140 | -3.160493 |     -5.328664 | 否。      | False     |     -6.096703 | -3.993907 | -3.159086 | 是奇异矩阵。 | True      |
| 可逆方阵         | 否       | -3.854251 | -3.119804 |     -5.210715 | 否。      | True      |     -6.419582 | -4.399146 | -3.224630 | 是奇异矩阵。 | False     |

## F04 — calculation instruction

**方阵／奇异性未知**；方阵=是，奇异性=无法确定；性质词=square。

```text
For the calculation described here, take A to be a square matrix.
```

**奇异方阵**；方阵=是，奇异性=是；性质词=singular, square。

```text
For the calculation described here, take A to be a singular square matrix.
```

**可逆方阵**；方阵=是，奇异性=否；性质词=invertible, square。

```text
For the calculation described here, take A to be an invertible square matrix.
```

| 条件             | 正确     |     F1 是 |     F1 否 |   F1 无法确定 | F1 首选   | F1 正确   |   F2 无法确定 |     F2 否 |     F2 是 | F2 首选      | F2 正确   |
|:-----------------|:---------|----------:|----------:|--------------:|:----------|:----------|--------------:|----------:|----------:|:-------------|:----------|
| 方阵／奇异性未知 | 无法确定 | -4.136759 | -2.791276 |     -4.926062 | 否。      | False     |     -6.159396 | -4.430600 | -3.297609 | 是奇异矩阵。 | False     |
| 奇异方阵         | 是       | -4.043788 | -2.518188 |     -5.015530 | 否。      | False     |     -6.101772 | -4.059446 | -3.204386 | 是奇异矩阵。 | True      |
| 可逆方阵         | 否       | -4.054294 | -2.630639 |     -5.310295 | 否。      | True      |     -6.200617 | -4.378832 | -3.176037 | 是奇异矩阵。 | False     |

## F05 — lecture notes

**方阵／奇异性未知**；方阵=是，奇异性=无法确定；性质词=square。

```text
The lecture notes introduce A as a square matrix.
```

**奇异方阵**；方阵=是，奇异性=是；性质词=singular, square。

```text
The lecture notes introduce A as a singular square matrix.
```

**可逆方阵**；方阵=是，奇异性=否；性质词=invertible, square。

```text
The lecture notes introduce A as an invertible square matrix.
```

| 条件             | 正确     |     F1 是 |     F1 否 |   F1 无法确定 | F1 首选   | F1 正确   |   F2 无法确定 |     F2 否 |     F2 是 | F2 首选      | F2 正确   |
|:-----------------|:---------|----------:|----------:|--------------:|:----------|:----------|--------------:|----------:|----------:|:-------------|:----------|
| 方阵／奇异性未知 | 无法确定 | -3.985372 | -2.697426 |     -4.747396 | 否。      | False     |     -5.596048 | -4.393535 | -2.819004 | 是奇异矩阵。 | False     |
| 奇异方阵         | 是       | -3.713205 | -2.606092 |     -4.908767 | 否。      | False     |     -5.618788 | -4.103604 | -2.560624 | 是奇异矩阵。 | True      |
| 可逆方阵         | 否       | -4.138958 | -2.550686 |     -5.179838 | 否。      | True      |     -5.697879 | -4.334915 | -2.678942 | 是奇异矩阵。 | False     |

## F06 — short report

**方阵／奇异性未知**；方阵=是，奇异性=无法确定；性质词=square。

```text
For the model in this short report, A is a square matrix.
```

**奇异方阵**；方阵=是，奇异性=是；性质词=singular, square。

```text
For the model in this short report, A is a singular square matrix.
```

**可逆方阵**；方阵=是，奇异性=否；性质词=invertible, square。

```text
For the model in this short report, A is an invertible square matrix.
```

| 条件             | 正确     |     F1 是 |     F1 否 |   F1 无法确定 | F1 首选   | F1 正确   |   F2 无法确定 |     F2 否 |     F2 是 | F2 首选      | F2 正确   |
|:-----------------|:---------|----------:|----------:|--------------:|:----------|:----------|--------------:|----------:|----------:|:-------------|:----------|
| 方阵／奇异性未知 | 无法确定 | -3.997551 | -3.059566 |     -4.775708 | 否。      | False     |     -6.420256 | -4.279566 | -3.195703 | 是奇异矩阵。 | False     |
| 奇异方阵         | 是       | -3.544173 | -2.966208 |     -5.207982 | 否。      | False     |     -6.547997 | -4.083854 | -3.016059 | 是奇异矩阵。 | True      |
| 可逆方阵         | 否       | -4.069236 | -2.901761 |     -5.051965 | 否。      | True      |     -6.503221 | -4.379737 | -3.066878 | 是奇异矩阵。 | False     |

## F07 — table heading

**方阵／奇异性未知**；方阵=是，奇异性=无法确定；性质词=square。

```text
The table heading identifies A as a square matrix.
```

**奇异方阵**；方阵=是，奇异性=是；性质词=singular, square。

```text
The table heading identifies A as a singular square matrix.
```

**可逆方阵**；方阵=是，奇异性=否；性质词=invertible, square。

```text
The table heading identifies A as an invertible square matrix.
```

| 条件             | 正确     |     F1 是 |     F1 否 |   F1 无法确定 | F1 首选   | F1 正确   |   F2 无法确定 |     F2 否 |     F2 是 | F2 首选      | F2 正确   |
|:-----------------|:---------|----------:|----------:|--------------:|:----------|:----------|--------------:|----------:|----------:|:-------------|:----------|
| 方阵／奇异性未知 | 无法确定 | -4.052016 | -3.300155 |     -5.561396 | 否。      | False     |     -7.019301 | -4.512610 | -3.401590 | 是奇异矩阵。 | False     |
| 奇异方阵         | 是       | -3.890181 | -3.106969 |     -5.546543 | 否。      | False     |     -7.029012 | -4.285210 | -3.274346 | 是奇异矩阵。 | True      |
| 可逆方阵         | 否       | -4.176853 | -3.167116 |     -5.900900 | 否。      | True      |     -7.384298 | -4.604913 | -3.391278 | 是奇异矩阵。 | False     |

## F08 — symbol definition

**方阵／奇异性未知**；方阵=是，奇异性=无法确定；性质词=square。

```text
Throughout this example, the symbol A denotes a square matrix.
```

**奇异方阵**；方阵=是，奇异性=是；性质词=singular, square。

```text
Throughout this example, the symbol A denotes a singular square matrix.
```

**可逆方阵**；方阵=是，奇异性=否；性质词=invertible, square。

```text
Throughout this example, the symbol A denotes an invertible square matrix.
```

| 条件             | 正确     |     F1 是 |     F1 否 |   F1 无法确定 | F1 首选   | F1 正确   |   F2 无法确定 |     F2 否 |     F2 是 | F2 首选      | F2 正确   |
|:-----------------|:---------|----------:|----------:|--------------:|:----------|:----------|--------------:|----------:|----------:|:-------------|:----------|
| 方阵／奇异性未知 | 无法确定 | -3.981013 | -2.717295 |     -4.663254 | 否。      | False     |     -5.733503 | -4.159342 | -2.971114 | 是奇异矩阵。 | False     |
| 奇异方阵         | 是       | -3.473314 | -2.650673 |     -4.717403 | 否。      | False     |     -5.493924 | -3.947527 | -2.871652 | 是奇异矩阵。 | True      |
| 可逆方阵         | 否       | -4.006026 | -2.540109 |     -4.821496 | 否。      | True      |     -5.652055 | -4.185260 | -2.833459 | 是奇异矩阵。 | False     |

## F09 — fronted noun phrase

**方阵／奇异性未知**；方阵=是，奇异性=无法确定；性质词=square。

```text
A square matrix, denoted by A, is used in the following discussion.
```

**奇异方阵**；方阵=是，奇异性=是；性质词=singular, square。

```text
A singular square matrix, denoted by A, is used in the following discussion.
```

**可逆方阵**；方阵=是，奇异性=否；性质词=invertible, square。

```text
An invertible square matrix, denoted by A, is used in the following discussion.
```

| 条件             | 正确     |     F1 是 |     F1 否 |   F1 无法确定 | F1 首选   | F1 正确   |   F2 无法确定 |     F2 否 |     F2 是 | F2 首选      | F2 正确   |
|:-----------------|:---------|----------:|----------:|--------------:|:----------|:----------|--------------:|----------:|----------:|:-------------|:----------|
| 方阵／奇异性未知 | 无法确定 | -4.042688 | -3.286351 |     -5.402116 | 否。      | False     |     -6.453977 | -4.579723 | -3.190353 | 是奇异矩阵。 | False     |
| 奇异方阵         | 是       | -3.599694 | -3.123219 |     -5.508870 | 否。      | False     |     -6.903991 | -4.124391 | -2.979075 | 是奇异矩阵。 | True      |
| 可逆方阵         | 否       | -3.852522 | -3.208803 |     -5.377886 | 否。      | True      |     -6.860285 | -4.447339 | -3.127107 | 是奇异矩阵。 | False     |

## F10 — procedure step

**方阵／奇异性未知**；方阵=是，奇异性=无法确定；性质词=square。

```text
For this step of the procedure, the supplied object A is a square matrix.
```

**奇异方阵**；方阵=是，奇异性=是；性质词=singular, square。

```text
For this step of the procedure, the supplied object A is a singular square matrix.
```

**可逆方阵**；方阵=是，奇异性=否；性质词=invertible, square。

```text
For this step of the procedure, the supplied object A is an invertible square matrix.
```

| 条件             | 正确     |     F1 是 |     F1 否 |   F1 无法确定 | F1 首选   | F1 正确   |   F2 无法确定 |     F2 否 |     F2 是 | F2 首选      | F2 正确   |
|:-----------------|:---------|----------:|----------:|--------------:|:----------|:----------|--------------:|----------:|----------:|:-------------|:----------|
| 方阵／奇异性未知 | 无法确定 | -4.189066 | -2.850485 |     -4.720060 | 否。      | False     |     -5.647668 | -4.001409 | -2.723333 | 是奇异矩阵。 | False     |
| 奇异方阵         | 是       | -3.850022 | -2.588978 |     -5.117682 | 否。      | False     |     -5.952761 | -3.680715 | -2.649412 | 是奇异矩阵。 | True      |
| 可逆方阵         | 否       | -4.425513 | -2.530621 |     -5.337972 | 否。      | True      |     -5.904107 | -4.000439 | -2.676265 | 是奇异矩阵。 | False     |

## F11 — relative clause

**方阵／奇异性未知**；方阵=是，奇异性=无法确定；性质词=square。

```text
The exercise concerns A, which is a square matrix.
```

**奇异方阵**；方阵=是，奇异性=是；性质词=singular, square。

```text
The exercise concerns A, which is a singular square matrix.
```

**可逆方阵**；方阵=是，奇异性=否；性质词=invertible, square。

```text
The exercise concerns A, which is an invertible square matrix.
```

| 条件             | 正确     |     F1 是 |     F1 否 |   F1 无法确定 | F1 首选   | F1 正确   |   F2 无法确定 |     F2 否 |     F2 是 | F2 首选      | F2 正确   |
|:-----------------|:---------|----------:|----------:|--------------:|:----------|:----------|--------------:|----------:|----------:|:-------------|:----------|
| 方阵／奇异性未知 | 无法确定 | -3.767478 | -2.922039 |     -5.041244 | 否。      | False     |     -6.390072 | -4.450682 | -3.285542 | 是奇异矩阵。 | False     |
| 奇异方阵         | 是       | -3.501581 | -2.872757 |     -5.150215 | 否。      | False     |     -6.408601 | -4.171339 | -3.202762 | 是奇异矩阵。 | True      |
| 可逆方阵         | 否       | -3.700529 | -2.917637 |     -5.185268 | 否。      | True      |     -6.507229 | -4.416993 | -3.180166 | 是奇异矩阵。 | False     |

## F12 — accompanying description

**方阵／奇异性未知**；方阵=是，奇异性=无法确定；性质词=square。

```text
The accompanying description states: A is a square matrix.
```

**奇异方阵**；方阵=是，奇异性=是；性质词=singular, square。

```text
The accompanying description states: A is a singular square matrix.
```

**可逆方阵**；方阵=是，奇异性=否；性质词=invertible, square。

```text
The accompanying description states: A is an invertible square matrix.
```

| 条件             | 正确     |     F1 是 |     F1 否 |   F1 无法确定 | F1 首选   | F1 正确   |   F2 无法确定 |     F2 否 |     F2 是 | F2 首选      | F2 正确   |
|:-----------------|:---------|----------:|----------:|--------------:|:----------|:----------|--------------:|----------:|----------:|:-------------|:----------|
| 方阵／奇异性未知 | 无法确定 | -4.113143 | -2.783430 |     -5.067974 | 否。      | False     |     -5.603663 | -4.067452 | -2.967841 | 是奇异矩阵。 | False     |
| 奇异方阵         | 是       | -3.738041 | -2.711317 |     -5.427639 | 否。      | False     |     -5.922837 | -3.938164 | -2.896424 | 是奇异矩阵。 | True      |
| 可逆方阵         | 否       | -4.147204 | -2.673848 |     -5.431239 | 否。      | True      |     -5.885342 | -4.247425 | -2.928343 | 是奇异矩阵。 | False     |
