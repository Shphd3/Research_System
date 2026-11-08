派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_30_checkpoint_evidence_use/R02_relation_binding/cases_cn.md`。
[精确原始文件](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_30_checkpoint_evidence_use/R02_relation_binding/cases_cn.md)；研究修改仍回到原件。

---

# 真实正例、反例与失败

按下面类别选取字典序首例，来自全部结果，用于阅读而非独立确认或筛选分母。所有原文与失败在执行data/panel.jsonl和results/full保留。

## 两世界候选与生成都正确

Baseline，实际3B，T3_F1，锚点gap16。

### 世界A

```text
The ribbon is red.
The carpet is blue.
The color of the ribbon is
```

正确值：red；实际正确值gap：21；值位置：{'red': [1129], 'blue': [1134]}；关系块长10token；p=1151，预测下标1152。

| 候选 | IDs | 逐token log概率 | 总分nat |
|---|---|---|---|
| ' red.' | [2518, 13] | [-0.7860338687896729, -7.709303855895996] | -8.495337724685669 |
| ' blue.' | [6303, 13] | [-2.0854456424713135, -7.633280277252197] | -9.71872591972351 |

正确分差1.223388nat；偏好A。greedy原文 `' red.\n'`，解析A，正确True，停止PUNCTUATION，IDs[2518, 624]。

### 世界B

```text
The carpet is red.
The ribbon is blue.
The color of the ribbon is
```

正确值：blue；实际正确值gap：16；值位置：{'red': [1129], 'blue': [1134]}；关系块长10token；p=1151，预测下标1152。

| 候选 | IDs | 逐token log概率 | 总分nat |
|---|---|---|---|
| ' red.' | [2518, 13] | [-2.012718915939331, -7.610291481018066] | -9.623010396957397 |
| ' blue.' | [6303, 13] | [-0.8848273754119873, -7.622365474700928] | -8.507192850112915 |

正确分差1.115818nat；偏好B。greedy原文 `' blue.\n'`，解析B，正确True，停止PUNCTUATION，IDs[6303, 624]。

## 偏好随绑定移动但未两侧答对

Baseline，实际15B，T1_F1，锚点gap1024。

### 世界A

```text
The box contains the key.
The bag contains the spoon.
The item in the box is
```

正确值：key；实际正确值gap：1030；值位置：{'key': [120], 'spoon': [126]}；关系块长12token；p=1151，预测下标1152。

| 候选 | IDs | 逐token log概率 | 总分nat |
|---|---|---|---|
| ' key.' | [1376, 13] | [-6.633355140686035, -3.627506971359253] | -10.260862112045288 |
| ' spoon.' | [45505, 13] | [-13.543949127197266, -4.229324817657471] | -17.773273944854736 |

正确分差7.512412nat；偏好A。greedy原文 `' the key.\n'`，解析A，正确True，停止PUNCTUATION，IDs[279, 1376, 624]。

### 世界B

```text
The bag contains the key.
The box contains the spoon.
The item in the box is
```

正确值：spoon；实际正确值gap：1024；值位置：{'key': [120], 'spoon': [126]}；关系块长12token；p=1151，预测下标1152。

| 候选 | IDs | 逐token log概率 | 总分nat |
|---|---|---|---|
| ' key.' | [1376, 13] | [-7.316689491271973, -3.988097667694092] | -11.304787158966064 |
| ' spoon.' | [45505, 13] | [-13.045132637023926, -4.569716453552246] | -17.614849090576172 |

正确分差-6.310062nat；偏好A。greedy原文 `' the key.\n'`，解析A，正确False，停止PUNCTUATION，IDs[279, 1376, 624]。

## 近程仍失败

Dense，实际17B，T1_F1，锚点gap16。

### 世界A

```text
The box contains the key.
The bag contains the spoon.
The item in the box is
```

正确值：key；实际正确值gap：22；值位置：{'key': [1128], 'spoon': [1134]}；关系块长12token；p=1151，预测下标1152。

| 候选 | IDs | 逐token log概率 | 总分nat |
|---|---|---|---|
| ' key.' | [1376, 13] | [-7.909753322601318, -2.999208450317383] | -10.908961772918701 |
| ' spoon.' | [45505, 13] | [-8.512028694152832, -3.008823871612549] | -11.52085256576538 |

正确分差0.611891nat；偏好A。greedy原文 `' the key.\n'`，解析A，正确True，停止PUNCTUATION，IDs[279, 1376, 624]。

### 世界B

```text
The bag contains the key.
The box contains the spoon.
The item in the box is
```

正确值：spoon；实际正确值gap：16；值位置：{'key': [1128], 'spoon': [1134]}；关系块长12token；p=1151，预测下标1152。

| 候选 | IDs | 逐token log概率 | 总分nat |
|---|---|---|---|
| ' key.' | [1376, 13] | [-7.582328796386719, -3.025297164916992] | -10.607625961303711 |
| ' spoon.' | [45505, 13] | [-9.02485179901123, -2.991203784942627] | -12.016055583953857 |

正确分差-1.408430nat；偏好A。greedy原文 `' the key.\n'`，解析A，正确False，停止PUNCTUATION，IDs[279, 1376, 624]。

## 生成出现OTHER

Baseline，实际17B，T1_F1，锚点gap16。

### 世界A

```text
The box contains the key.
The bag contains the spoon.
The item in the box is
```

正确值：key；实际正确值gap：22；值位置：{'key': [1128], 'spoon': [1134]}；关系块长12token；p=1151，预测下标1152。

| 候选 | IDs | 逐token log概率 | 总分nat |
|---|---|---|---|
| ' key.' | [1376, 13] | [-8.521339416503906, -3.6604931354522705] | -12.181832551956177 |
| ' spoon.' | [45505, 13] | [-11.162553787231445, -3.335139274597168] | -14.497693061828613 |

正确分差2.315861nat；偏好A。greedy原文 `' the key.\n'`，解析A，正确True，停止PUNCTUATION，IDs[279, 1376, 624]。

### 世界B

```text
The bag contains the key.
The box contains the spoon.
The item in the box is
```

正确值：spoon；实际正确值gap：16；值位置：{'key': [1128], 'spoon': [1134]}；关系块长12token；p=1151，预测下标1152。

| 候选 | IDs | 逐token log概率 | 总分nat |
|---|---|---|---|
| ' key.' | [1376, 13] | [-8.536421775817871, -3.702568769454956] | -12.238990545272827 |
| ' spoon.' | [45505, 13] | [-11.235179901123047, -3.298715829849243] | -14.53389573097229 |

正确分差-2.294905nat；偏好A。greedy原文 `' a small piece of paper.\n'`，解析OTHER，正确False，停止PUNCTUATION，IDs[264, 2613, 6573, 315, 5567, 624]。

