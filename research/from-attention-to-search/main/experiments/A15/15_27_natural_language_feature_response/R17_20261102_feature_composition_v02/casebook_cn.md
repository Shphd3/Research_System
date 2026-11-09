# 固定案例：从实际文本看“组合”解释的边界

本案例固定为M05_0，留出spectrum定理组的第一家族，n=22。它展示具体方向翻转，不代表所有家族。所有原子为0起点ID，token位置也是0起点。底模从完整可见文本读取，在最后Summary冒号处记录联合CC响应；没有生成答案。

## 7803的可逆性方向随表述改变

| 文本条件 | 原始z_7803 | u_7803=z×743.696655 | 末token位置 |
|---|---:|---:|---:|
| coarse / explicit | 0.0000000000 | 0.0000000 | 31 |
| coarse / description | 0.0000000000 | 0.0000000 | 36 |
| invertible / explicit | 0.0000000000 | 0.0000000 | 46 |
| invertible / description | 0.0084945438 | 6.3173637 | 40 |
| singular / explicit | 0.0120193241 | 8.9387312 | 44 |
| singular / description | 0.0000000000 | 0.0000000 | 39 |

显式术语中，7803对奇异为正、可逆为零；无术语描述“零不是特征值”中，可逆反而为正、奇异为零。因此不能给它稳定命名为“奇异矩阵feature”。C在这两条描述中8个成员均活跃，q的L2差为0.063833；冻结H2模型在这对描述的损失由0.692954升至0.701830。强度变化本身没有保证正确方向。

## 完整输入与token

### M05_0_coarse_explicit

条件：coarse；标签：None；末位置：31；token数：32。依据：square-matrix invertibility equivalences over R; certificate: dimensions alone; invertibility Unknown。

```text
In an algebra lesson, we consider a real square matrix A with n = 22.
Summarize the mathematical object and its stated properties.
Summary:
```

Token IDs：`[641, 458, 46876, 17755, 11, 582, 2908, 264, 1931, 9334, 6172, 362, 448, 308, 284, 220, 17, 17, 624, 9190, 5612, 551, 279, 35972, 1633, 323, 1181, 10982, 5888, 624, 19237, 25]`。

### M05_0_coarse_description

条件：coarse；标签：None；末位置：36；token数：37。依据：square-matrix invertibility equivalences over R; certificate: dimensions alone; invertibility Unknown。

```text
Let A be a real array with 22 rows and 22 columns. Only its dimensions are specified here.
Summarize the mathematical object and its stated properties.
Summary:
```

Token IDs：`[10061, 362, 387, 264, 1931, 1334, 448, 220, 17, 17, 6978, 323, 220, 17, 17, 8147, 13, 8278, 1181, 15336, 525, 5189, 1588, 624, 9190, 5612, 551, 279, 35972, 1633, 323, 1181, 10982, 5888, 624, 19237, 25]`。

### M05_0_invertible_explicit

条件：invertible；标签：1；末位置：46；token数：47。依据：square-matrix invertibility equivalences over R; certificate: zero is not an eigenvalue。

```text
In an algebra lesson, we consider a real square matrix A with n = 22 such that zero is not an eigenvalue. This square matrix is invertible.
Summarize the mathematical object and its stated properties.
Summary:
```

Token IDs：`[641, 458, 46876, 17755, 11, 582, 2908, 264, 1931, 9334, 6172, 362, 448, 308, 284, 220, 17, 17, 1741, 429, 7168, 374, 537, 458, 28724, 957, 13, 1096, 9334, 6172, 374, 42199, 1238, 624, 9190, 5612, 551, 279, 35972, 1633, 323, 1181, 10982, 5888, 624, 19237, 25]`。

### M05_0_invertible_description

条件：invertible；标签：1；末位置：40；token数：41。依据：square-matrix invertibility equivalences over R; certificate: zero is not an eigenvalue。

```text
Let A be a real array with 22 rows and 22 columns. For this array, zero is not an eigenvalue.
Summarize the mathematical object and its stated properties.
Summary:
```

Token IDs：`[10061, 362, 387, 264, 1931, 1334, 448, 220, 17, 17, 6978, 323, 220, 17, 17, 8147, 13, 1752, 419, 1334, 11, 7168, 374, 537, 458, 28724, 957, 624, 9190, 5612, 551, 279, 35972, 1633, 323, 1181, 10982, 5888, 624, 19237, 25]`。

### M05_0_singular_explicit

条件：singular；标签：0；末位置：44；token数：45。依据：square-matrix invertibility equivalences over R; certificate: zero is an eigenvalue。

```text
In an algebra lesson, we consider a real square matrix A with n = 22 such that zero is an eigenvalue. This square matrix is singular.
Summarize the mathematical object and its stated properties.
Summary:
```

Token IDs：`[641, 458, 46876, 17755, 11, 582, 2908, 264, 1931, 9334, 6172, 362, 448, 308, 284, 220, 17, 17, 1741, 429, 7168, 374, 458, 28724, 957, 13, 1096, 9334, 6172, 374, 33944, 624, 9190, 5612, 551, 279, 35972, 1633, 323, 1181, 10982, 5888, 624, 19237, 25]`。

### M05_0_singular_description

条件：singular；标签：0；末位置：39；token数：40。依据：square-matrix invertibility equivalences over R; certificate: zero is an eigenvalue。

```text
Let A be a real array with 22 rows and 22 columns. For this array, zero is an eigenvalue.
Summarize the mathematical object and its stated properties.
Summary:
```

Token IDs：`[10061, 362, 387, 264, 1931, 1334, 448, 220, 17, 17, 6978, 323, 220, 17, 17, 8147, 13, 1752, 419, 1334, 11, 7168, 374, 458, 28724, 957, 624, 9190, 5612, 551, 279, 35972, 1633, 323, 1181, 10982, 5888, 624, 19237, 25]`。

### N05_0_explicit

条件：nonmatrix；标签：None；末位置：48；token数：49。依据：nonmatrix object: derivative。

```text
In an algebra lesson, we consider a differentiable real function on an open interval. For this object, its local rate of change is defined. This is exercise 22.
Summarize the mathematical object and its stated properties.
Summary:
```

Token IDs：`[641, 458, 46876, 17755, 11, 582, 2908, 264, 2155, 2156, 1931, 729, 389, 458, 1787, 9873, 13, 1752, 419, 1633, 11, 1181, 2205, 4379, 315, 2297, 374, 4512, 13, 1096, 374, 10158, 220, 17, 17, 624, 9190, 5612, 551, 279, 35972, 1633, 323, 1181, 10982, 5888, 624, 19237, 25]`。

### N05_0_description

条件：nonmatrix；标签：None；末位置：44；token数：45。依据：nonmatrix object: derivative。

```text
In exercise 22, this mathematical example concerns a differentiable real function on an open interval. In this setting, its local rate of change is defined.
Summarize the mathematical object and its stated properties.
Summary:
```

Token IDs：`[641, 10158, 220, 17, 17, 11, 419, 35972, 3110, 10520, 264, 2155, 2156, 1931, 729, 389, 458, 1787, 9873, 13, 758, 419, 6243, 11, 1181, 2205, 4379, 315, 2297, 374, 4512, 624, 9190, 5612, 551, 279, 35972, 1633, 323, 1181, 10982, 5888, 624, 19237, 25]`。

## 自然配置反例：稀有响应可以出现在普通非目标内容中

配置3604强+15445弱的一个验证命中为R15_general_132，来源host为www.zootoo.com，0起点位置277，blind_id `8298cb7653c3649beb`。可见前缀开头为“Why Sea Food Considered as healthy diet”，随后讨论海鲜营养。自动规则标为non_target。匹配对照R15_general_119来自www.waterstones.com，位置232，blind_id `c7b5704b5c34cecc57`，讨论Francis Cauffman建筑书目，同样non_target。两者同general关键词cohort、位置四分位，前缀长度比233/278约0.838。

这个实例不证明配置没有语义；它说明不能把由数学发现面板挑出的配置直接认作自然文本中的可逆性内容。无关网页中的命中可能来自更一般的词面、语体或其他未知性质。完整可见前缀见[去响应文本表](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/H4/results/blind_texts.jsonl)，document／position对应见[合并表](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/H4/evidence/blind_merge_map.json)，所有配置见[原始频率表](tables/natural_prevalence.csv)。

[全部固定案例原子数值](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/shared/fixed_case_raw.csv) · [各路线逐条预测](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/H1/results/predictions.csv) · [总认识](summary_cn.md)
