# 真实家族案例

选取规则：Dense33B按家族ID首个近成功、远失败例；若无则17B；再列相同家族3B。它们是完整结果的阅读示例，不是额外测试或筛选条件。所有失败与成功均在逐家族表保留。

## Dense 33B，T1_F1

| 间隔 | 事实版本 | 证据值token位置 | 前缀末位置 | A总分 nat | B总分 nat | 正确分差 nat | 偏好 |
|---|---|---|---|---|---|---|---|
| 16 | A | [1134] | 1151 | -10.576 | -18.550 | 7.974 | A |
| 16 | B | [1134] | 1151 | -12.862 | -12.162 | 0.700 | B |
| 1024 | A | [126] | 1151 | -10.505 | -18.229 | 7.725 | A |
| 1024 | B | [126] | 1151 | -11.398 | -15.665 | -4.267 | A |

### 间隔16，事实A的完整前缀

```text
Record:
The weekend was relaxing.
The morning was relaxing.
The past evening was warm.
The early morning was gentle.
The afternoon was relaxing.
The last afternoon was pleasant.
The late afternoon was cloudy.
The early day was peaceful.
The next morning was cool.
The next morning was quiet.
The previous night was warm.
The long weekend was relaxing.
The night was quiet.
The next afternoon was warm.
The early evening was cloudy.
The next weekend was calm.
The weekend was pleasant.
The late night was peaceful.
The following evening was warm.
The following night was gentle.
The evening was peaceful.
The afternoon was gentle.
The past weekend was bright.
The following night was cloudy.
The next night was calm.
The weekend was uneventful.
The late night was cool.
The rainy afternoon was quiet.
The early morning was still.
The late evening was quiet.
The early day was warm.
The past evening was calm.
The following evening was cool.
The day was pleasant.
The previous day was relaxing.
The late afternoon was still.
The morning was cloudy.
The following day was quiet.
The previous day was pleasant.
The evening was cool.
The past evening was gentle.
The long weekend was gentle.
The previous night was relaxing.
The next weekend was pleasant.
The last afternoon was bright.
The next afternoon was still.
The morning was peaceful.
The next night was cool.
The evening was uneventful.
The long weekend was uneventful.
The early evening was uneventful.
The weekend was calm.
The next weekend was gentle.
Time passed.
The previous weekend was cloudy.
The past weekend was warm.
The sunny morning was cloudy.
The next weekend was bright.
The previous day was peaceful.
The afternoon was pleasant.
The early day was calm.
The early evening was calm.
The sunny morning was relaxing.
The following night was still.
The rainy afternoon was peaceful.
The previous morning was cloudy.
The weekend was gentle.
The next night was pleasant.
The day was calm.
The day was gentle.
The past weekend was still.
The night was bright.
The long weekend was warm.
The previous day was still.
The next morning was uneventful.
The past evening was relaxing.
The early day was quiet.
The past weekend was calm.
The next afternoon was uneventful.
The later night was peaceful.
The later night was pleasant.
The night was peaceful.
The early evening was warm.
The night was relaxing.
The afternoon was warm.
The early evening was quiet.
The day was cloudy.
The night was gentle.
The following night was relaxing.
The later night was still.
The next morning was cloudy.
The past weekend was uneventful.
The weekend was peaceful.
The next night was peaceful.
The last afternoon was uneventful.
The following day was bright.
The following morning was peaceful.
The previous weekend was bright.
The night was cool.
The later night was bright.
The next night was quiet.
The following evening was uneventful.
The previous night was cloudy.
The next afternoon was quiet.
The past weekend was peaceful.
The late evening was still.
The following day was still.
The previous morning was bright.
The following day was cool.
The next morning was pleasant.
The previous morning was still.
The previous weekend was pleasant.
The evening was pleasant.
The following morning was bright.
The late night was calm.
The prior afternoon was pleasant.
The morning was uneventful.
The past weekend was pleasant.
The last afternoon was quiet.
The early morning was uneventful.
The late afternoon was gentle.
The past weekend was cloudy.
The afternoon was cool.
The late night was pleasant.
The weekend was cool.
The rainy afternoon was bright.
The early day was gentle.
The afternoon was calm.
The previous morning was gentle.
The afternoon was uneventful.
The sunny morning was still.
The last afternoon was peaceful.
The early morning was calm.
The next night was uneventful.
The following day was calm.
The next afternoon was peaceful.
The night was still.
The previous day was quiet.
The following day was uneventful.
The rainy afternoon was still.
The rainy afternoon was uneventful.
The late evening was cloudy.
The long weekend was still.
The early morning was peaceful.
The late afternoon was cool.
The early morning was warm.
The following night was bright.
The next weekend was cool.
The next afternoon was bright.
The previous night was cool.
The previous weekend was still.
The following evening was still.
The following night was warm.
The next weekend was cloudy.
The previous day was cloudy.
The following day was pleasant.
The prior afternoon was relaxing.
The early day was bright.
The previous night was quiet.
The previous night was still.
The early evening was relaxing.
The late afternoon was pleasant.
The later night was quiet.
The early day was uneventful.
The previous day was warm.
The next night was relaxing.
The weekend was still.
The following morning was uneventful.
The late night was warm.
The previous day was bright.
The past weekend was cool.
The last afternoon was gentle.
The early morning was pleasant.
The late afternoon was warm.
The following morning was relaxing.
The next weekend was quiet.
The night was calm.
The following day was relaxing.
The later night was uneventful.
The previous night was uneventful.
The previous night was calm.
The rainy afternoon was cloudy.
The prior afternoon was quiet.
The early morning was bright.
The late evening was calm.
The sunny morning was gentle.
The prior afternoon was cloudy.
The following evening was cloudy.
The box contains the key.
The morning was warm.
The morning was cool.
The item in the box is
```

| 候选原文 | token IDs | 逐token log-prob nat |
|---|---|---|
| ' key.' | [1376, 13] | [-4.918918132781982, -5.657087326049805] |
| ' spoon.' | [45505, 13] | [-13.668917655944824, -4.881042003631592] |

### 间隔16，事实B的完整前缀

```text
Record:
The weekend was relaxing.
The morning was relaxing.
The past evening was warm.
The early morning was gentle.
The afternoon was relaxing.
The last afternoon was pleasant.
The late afternoon was cloudy.
The early day was peaceful.
The next morning was cool.
The next morning was quiet.
The previous night was warm.
The long weekend was relaxing.
The night was quiet.
The next afternoon was warm.
The early evening was cloudy.
The next weekend was calm.
The weekend was pleasant.
The late night was peaceful.
The following evening was warm.
The following night was gentle.
The evening was peaceful.
The afternoon was gentle.
The past weekend was bright.
The following night was cloudy.
The next night was calm.
The weekend was uneventful.
The late night was cool.
The rainy afternoon was quiet.
The early morning was still.
The late evening was quiet.
The early day was warm.
The past evening was calm.
The following evening was cool.
The day was pleasant.
The previous day was relaxing.
The late afternoon was still.
The morning was cloudy.
The following day was quiet.
The previous day was pleasant.
The evening was cool.
The past evening was gentle.
The long weekend was gentle.
The previous night was relaxing.
The next weekend was pleasant.
The last afternoon was bright.
The next afternoon was still.
The morning was peaceful.
The next night was cool.
The evening was uneventful.
The long weekend was uneventful.
The early evening was uneventful.
The weekend was calm.
The next weekend was gentle.
Time passed.
The previous weekend was cloudy.
The past weekend was warm.
The sunny morning was cloudy.
The next weekend was bright.
The previous day was peaceful.
The afternoon was pleasant.
The early day was calm.
The early evening was calm.
The sunny morning was relaxing.
The following night was still.
The rainy afternoon was peaceful.
The previous morning was cloudy.
The weekend was gentle.
The next night was pleasant.
The day was calm.
The day was gentle.
The past weekend was still.
The night was bright.
The long weekend was warm.
The previous day was still.
The next morning was uneventful.
The past evening was relaxing.
The early day was quiet.
The past weekend was calm.
The next afternoon was uneventful.
The later night was peaceful.
The later night was pleasant.
The night was peaceful.
The early evening was warm.
The night was relaxing.
The afternoon was warm.
The early evening was quiet.
The day was cloudy.
The night was gentle.
The following night was relaxing.
The later night was still.
The next morning was cloudy.
The past weekend was uneventful.
The weekend was peaceful.
The next night was peaceful.
The last afternoon was uneventful.
The following day was bright.
The following morning was peaceful.
The previous weekend was bright.
The night was cool.
The later night was bright.
The next night was quiet.
The following evening was uneventful.
The previous night was cloudy.
The next afternoon was quiet.
The past weekend was peaceful.
The late evening was still.
The following day was still.
The previous morning was bright.
The following day was cool.
The next morning was pleasant.
The previous morning was still.
The previous weekend was pleasant.
The evening was pleasant.
The following morning was bright.
The late night was calm.
The prior afternoon was pleasant.
The morning was uneventful.
The past weekend was pleasant.
The last afternoon was quiet.
The early morning was uneventful.
The late afternoon was gentle.
The past weekend was cloudy.
The afternoon was cool.
The late night was pleasant.
The weekend was cool.
The rainy afternoon was bright.
The early day was gentle.
The afternoon was calm.
The previous morning was gentle.
The afternoon was uneventful.
The sunny morning was still.
The last afternoon was peaceful.
The early morning was calm.
The next night was uneventful.
The following day was calm.
The next afternoon was peaceful.
The night was still.
The previous day was quiet.
The following day was uneventful.
The rainy afternoon was still.
The rainy afternoon was uneventful.
The late evening was cloudy.
The long weekend was still.
The early morning was peaceful.
The late afternoon was cool.
The early morning was warm.
The following night was bright.
The next weekend was cool.
The next afternoon was bright.
The previous night was cool.
The previous weekend was still.
The following evening was still.
The following night was warm.
The next weekend was cloudy.
The previous day was cloudy.
The following day was pleasant.
The prior afternoon was relaxing.
The early day was bright.
The previous night was quiet.
The previous night was still.
The early evening was relaxing.
The late afternoon was pleasant.
The later night was quiet.
The early day was uneventful.
The previous day was warm.
The next night was relaxing.
The weekend was still.
The following morning was uneventful.
The late night was warm.
The previous day was bright.
The past weekend was cool.
The last afternoon was gentle.
The early morning was pleasant.
The late afternoon was warm.
The following morning was relaxing.
The next weekend was quiet.
The night was calm.
The following day was relaxing.
The later night was uneventful.
The previous night was uneventful.
The previous night was calm.
The rainy afternoon was cloudy.
The prior afternoon was quiet.
The early morning was bright.
The late evening was calm.
The sunny morning was gentle.
The prior afternoon was cloudy.
The following evening was cloudy.
The box contains the spoon.
The morning was warm.
The morning was cool.
The item in the box is
```

| 候选原文 | token IDs | 逐token log-prob nat |
|---|---|---|
| ' key.' | [1376, 13] | [-7.415865898132324, -5.446251392364502] |
| ' spoon.' | [45505, 13] | [-7.603365898132324, -4.558586597442627] |

### 间隔1024，事实A的完整前缀

```text
Record:
The weekend was relaxing.
The morning was relaxing.
The past evening was warm.
The early morning was gentle.
The afternoon was relaxing.
The last afternoon was pleasant.
The late afternoon was cloudy.
The early day was peaceful.
The next morning was cool.
The next morning was quiet.
The previous night was warm.
The long weekend was relaxing.
The night was quiet.
The next afternoon was warm.
The early evening was cloudy.
The next weekend was calm.
The weekend was pleasant.
The late night was peaceful.
The following evening was warm.
The following night was gentle.
The evening was peaceful.
The box contains the key.
The afternoon was gentle.
The past weekend was bright.
The following night was cloudy.
The next night was calm.
The weekend was uneventful.
The late night was cool.
The rainy afternoon was quiet.
The early morning was still.
The late evening was quiet.
The early day was warm.
The past evening was calm.
The following evening was cool.
The day was pleasant.
The previous day was relaxing.
The late afternoon was still.
The morning was cloudy.
The following day was quiet.
The previous day was pleasant.
The evening was cool.
The past evening was gentle.
The long weekend was gentle.
The previous night was relaxing.
The next weekend was pleasant.
The last afternoon was bright.
The next afternoon was still.
The morning was peaceful.
The next night was cool.
The evening was uneventful.
The long weekend was uneventful.
The early evening was uneventful.
The weekend was calm.
The next weekend was gentle.
Time passed.
The previous weekend was cloudy.
The past weekend was warm.
The sunny morning was cloudy.
The next weekend was bright.
The previous day was peaceful.
The afternoon was pleasant.
The early day was calm.
The early evening was calm.
The sunny morning was relaxing.
The following night was still.
The rainy afternoon was peaceful.
The previous morning was cloudy.
The weekend was gentle.
The next night was pleasant.
The day was calm.
The day was gentle.
The past weekend was still.
The night was bright.
The long weekend was warm.
The previous day was still.
The next morning was uneventful.
The past evening was relaxing.
The early day was quiet.
The past weekend was calm.
The next afternoon was uneventful.
The later night was peaceful.
The later night was pleasant.
The night was peaceful.
The early evening was warm.
The night was relaxing.
The afternoon was warm.
The early evening was quiet.
The day was cloudy.
The night was gentle.
The following night was relaxing.
The later night was still.
The next morning was cloudy.
The past weekend was uneventful.
The weekend was peaceful.
The next night was peaceful.
The last afternoon was uneventful.
The following day was bright.
The following morning was peaceful.
The previous weekend was bright.
The night was cool.
The later night was bright.
The next night was quiet.
The following evening was uneventful.
The previous night was cloudy.
The next afternoon was quiet.
The past weekend was peaceful.
The late evening was still.
The following day was still.
The previous morning was bright.
The following day was cool.
The next morning was pleasant.
The previous morning was still.
The previous weekend was pleasant.
The evening was pleasant.
The following morning was bright.
The late night was calm.
The prior afternoon was pleasant.
The morning was uneventful.
The past weekend was pleasant.
The last afternoon was quiet.
The early morning was uneventful.
The late afternoon was gentle.
The past weekend was cloudy.
The afternoon was cool.
The late night was pleasant.
The weekend was cool.
The rainy afternoon was bright.
The early day was gentle.
The afternoon was calm.
The previous morning was gentle.
The afternoon was uneventful.
The sunny morning was still.
The last afternoon was peaceful.
The early morning was calm.
The next night was uneventful.
The following day was calm.
The next afternoon was peaceful.
The night was still.
The previous day was quiet.
The following day was uneventful.
The rainy afternoon was still.
The rainy afternoon was uneventful.
The late evening was cloudy.
The long weekend was still.
The early morning was peaceful.
The late afternoon was cool.
The early morning was warm.
The following night was bright.
The next weekend was cool.
The next afternoon was bright.
The previous night was cool.
The previous weekend was still.
The following evening was still.
The following night was warm.
The next weekend was cloudy.
The previous day was cloudy.
The following day was pleasant.
The prior afternoon was relaxing.
The early day was bright.
The previous night was quiet.
The previous night was still.
The early evening was relaxing.
The late afternoon was pleasant.
The later night was quiet.
The early day was uneventful.
The previous day was warm.
The next night was relaxing.
The weekend was still.
The following morning was uneventful.
The late night was warm.
The previous day was bright.
The past weekend was cool.
The last afternoon was gentle.
The early morning was pleasant.
The late afternoon was warm.
The following morning was relaxing.
The next weekend was quiet.
The night was calm.
The following day was relaxing.
The later night was uneventful.
The previous night was uneventful.
The previous night was calm.
The rainy afternoon was cloudy.
The prior afternoon was quiet.
The early morning was bright.
The late evening was calm.
The sunny morning was gentle.
The prior afternoon was cloudy.
The following evening was cloudy.
The morning was warm.
The morning was cool.
The item in the box is
```

| 候选原文 | token IDs | 逐token log-prob nat |
|---|---|---|
| ' key.' | [1376, 13] | [-5.8822479248046875, -4.622320175170898] |
| ' spoon.' | [45505, 13] | [-14.444747924804688, -3.784428834915161] |

### 间隔1024，事实B的完整前缀

```text
Record:
The weekend was relaxing.
The morning was relaxing.
The past evening was warm.
The early morning was gentle.
The afternoon was relaxing.
The last afternoon was pleasant.
The late afternoon was cloudy.
The early day was peaceful.
The next morning was cool.
The next morning was quiet.
The previous night was warm.
The long weekend was relaxing.
The night was quiet.
The next afternoon was warm.
The early evening was cloudy.
The next weekend was calm.
The weekend was pleasant.
The late night was peaceful.
The following evening was warm.
The following night was gentle.
The evening was peaceful.
The box contains the spoon.
The afternoon was gentle.
The past weekend was bright.
The following night was cloudy.
The next night was calm.
The weekend was uneventful.
The late night was cool.
The rainy afternoon was quiet.
The early morning was still.
The late evening was quiet.
The early day was warm.
The past evening was calm.
The following evening was cool.
The day was pleasant.
The previous day was relaxing.
The late afternoon was still.
The morning was cloudy.
The following day was quiet.
The previous day was pleasant.
The evening was cool.
The past evening was gentle.
The long weekend was gentle.
The previous night was relaxing.
The next weekend was pleasant.
The last afternoon was bright.
The next afternoon was still.
The morning was peaceful.
The next night was cool.
The evening was uneventful.
The long weekend was uneventful.
The early evening was uneventful.
The weekend was calm.
The next weekend was gentle.
Time passed.
The previous weekend was cloudy.
The past weekend was warm.
The sunny morning was cloudy.
The next weekend was bright.
The previous day was peaceful.
The afternoon was pleasant.
The early day was calm.
The early evening was calm.
The sunny morning was relaxing.
The following night was still.
The rainy afternoon was peaceful.
The previous morning was cloudy.
The weekend was gentle.
The next night was pleasant.
The day was calm.
The day was gentle.
The past weekend was still.
The night was bright.
The long weekend was warm.
The previous day was still.
The next morning was uneventful.
The past evening was relaxing.
The early day was quiet.
The past weekend was calm.
The next afternoon was uneventful.
The later night was peaceful.
The later night was pleasant.
The night was peaceful.
The early evening was warm.
The night was relaxing.
The afternoon was warm.
The early evening was quiet.
The day was cloudy.
The night was gentle.
The following night was relaxing.
The later night was still.
The next morning was cloudy.
The past weekend was uneventful.
The weekend was peaceful.
The next night was peaceful.
The last afternoon was uneventful.
The following day was bright.
The following morning was peaceful.
The previous weekend was bright.
The night was cool.
The later night was bright.
The next night was quiet.
The following evening was uneventful.
The previous night was cloudy.
The next afternoon was quiet.
The past weekend was peaceful.
The late evening was still.
The following day was still.
The previous morning was bright.
The following day was cool.
The next morning was pleasant.
The previous morning was still.
The previous weekend was pleasant.
The evening was pleasant.
The following morning was bright.
The late night was calm.
The prior afternoon was pleasant.
The morning was uneventful.
The past weekend was pleasant.
The last afternoon was quiet.
The early morning was uneventful.
The late afternoon was gentle.
The past weekend was cloudy.
The afternoon was cool.
The late night was pleasant.
The weekend was cool.
The rainy afternoon was bright.
The early day was gentle.
The afternoon was calm.
The previous morning was gentle.
The afternoon was uneventful.
The sunny morning was still.
The last afternoon was peaceful.
The early morning was calm.
The next night was uneventful.
The following day was calm.
The next afternoon was peaceful.
The night was still.
The previous day was quiet.
The following day was uneventful.
The rainy afternoon was still.
The rainy afternoon was uneventful.
The late evening was cloudy.
The long weekend was still.
The early morning was peaceful.
The late afternoon was cool.
The early morning was warm.
The following night was bright.
The next weekend was cool.
The next afternoon was bright.
The previous night was cool.
The previous weekend was still.
The following evening was still.
The following night was warm.
The next weekend was cloudy.
The previous day was cloudy.
The following day was pleasant.
The prior afternoon was relaxing.
The early day was bright.
The previous night was quiet.
The previous night was still.
The early evening was relaxing.
The late afternoon was pleasant.
The later night was quiet.
The early day was uneventful.
The previous day was warm.
The next night was relaxing.
The weekend was still.
The following morning was uneventful.
The late night was warm.
The previous day was bright.
The past weekend was cool.
The last afternoon was gentle.
The early morning was pleasant.
The late afternoon was warm.
The following morning was relaxing.
The next weekend was quiet.
The night was calm.
The following day was relaxing.
The later night was uneventful.
The previous night was uneventful.
The previous night was calm.
The rainy afternoon was cloudy.
The prior afternoon was quiet.
The early morning was bright.
The late evening was calm.
The sunny morning was gentle.
The prior afternoon was cloudy.
The following evening was cloudy.
The morning was warm.
The morning was cool.
The item in the box is
```

| 候选原文 | token IDs | 逐token log-prob nat |
|---|---|---|
| ' key.' | [1376, 13] | [-7.168230056762695, -4.230094909667969] |
| ' spoon.' | [45505, 13] | [-12.004167556762695, -3.6607463359832764] |

## Dense 3B，T1_F1

| 间隔 | 事实版本 | 证据值token位置 | 前缀末位置 | A总分 nat | B总分 nat | 正确分差 nat | 偏好 |
|---|---|---|---|---|---|---|---|
| 16 | A | [1134] | 1151 | -10.830 | -18.606 | 7.775 | A |
| 16 | B | [1134] | 1151 | -13.889 | -13.216 | 0.673 | B |
| 1024 | A | [126] | 1151 | -9.060 | -18.790 | 9.729 | A |
| 1024 | B | [126] | 1151 | -13.423 | -14.001 | -0.578 | A |

### 间隔16，事实A的完整前缀

```text
Record:
The weekend was relaxing.
The morning was relaxing.
The past evening was warm.
The early morning was gentle.
The afternoon was relaxing.
The last afternoon was pleasant.
The late afternoon was cloudy.
The early day was peaceful.
The next morning was cool.
The next morning was quiet.
The previous night was warm.
The long weekend was relaxing.
The night was quiet.
The next afternoon was warm.
The early evening was cloudy.
The next weekend was calm.
The weekend was pleasant.
The late night was peaceful.
The following evening was warm.
The following night was gentle.
The evening was peaceful.
The afternoon was gentle.
The past weekend was bright.
The following night was cloudy.
The next night was calm.
The weekend was uneventful.
The late night was cool.
The rainy afternoon was quiet.
The early morning was still.
The late evening was quiet.
The early day was warm.
The past evening was calm.
The following evening was cool.
The day was pleasant.
The previous day was relaxing.
The late afternoon was still.
The morning was cloudy.
The following day was quiet.
The previous day was pleasant.
The evening was cool.
The past evening was gentle.
The long weekend was gentle.
The previous night was relaxing.
The next weekend was pleasant.
The last afternoon was bright.
The next afternoon was still.
The morning was peaceful.
The next night was cool.
The evening was uneventful.
The long weekend was uneventful.
The early evening was uneventful.
The weekend was calm.
The next weekend was gentle.
Time passed.
The previous weekend was cloudy.
The past weekend was warm.
The sunny morning was cloudy.
The next weekend was bright.
The previous day was peaceful.
The afternoon was pleasant.
The early day was calm.
The early evening was calm.
The sunny morning was relaxing.
The following night was still.
The rainy afternoon was peaceful.
The previous morning was cloudy.
The weekend was gentle.
The next night was pleasant.
The day was calm.
The day was gentle.
The past weekend was still.
The night was bright.
The long weekend was warm.
The previous day was still.
The next morning was uneventful.
The past evening was relaxing.
The early day was quiet.
The past weekend was calm.
The next afternoon was uneventful.
The later night was peaceful.
The later night was pleasant.
The night was peaceful.
The early evening was warm.
The night was relaxing.
The afternoon was warm.
The early evening was quiet.
The day was cloudy.
The night was gentle.
The following night was relaxing.
The later night was still.
The next morning was cloudy.
The past weekend was uneventful.
The weekend was peaceful.
The next night was peaceful.
The last afternoon was uneventful.
The following day was bright.
The following morning was peaceful.
The previous weekend was bright.
The night was cool.
The later night was bright.
The next night was quiet.
The following evening was uneventful.
The previous night was cloudy.
The next afternoon was quiet.
The past weekend was peaceful.
The late evening was still.
The following day was still.
The previous morning was bright.
The following day was cool.
The next morning was pleasant.
The previous morning was still.
The previous weekend was pleasant.
The evening was pleasant.
The following morning was bright.
The late night was calm.
The prior afternoon was pleasant.
The morning was uneventful.
The past weekend was pleasant.
The last afternoon was quiet.
The early morning was uneventful.
The late afternoon was gentle.
The past weekend was cloudy.
The afternoon was cool.
The late night was pleasant.
The weekend was cool.
The rainy afternoon was bright.
The early day was gentle.
The afternoon was calm.
The previous morning was gentle.
The afternoon was uneventful.
The sunny morning was still.
The last afternoon was peaceful.
The early morning was calm.
The next night was uneventful.
The following day was calm.
The next afternoon was peaceful.
The night was still.
The previous day was quiet.
The following day was uneventful.
The rainy afternoon was still.
The rainy afternoon was uneventful.
The late evening was cloudy.
The long weekend was still.
The early morning was peaceful.
The late afternoon was cool.
The early morning was warm.
The following night was bright.
The next weekend was cool.
The next afternoon was bright.
The previous night was cool.
The previous weekend was still.
The following evening was still.
The following night was warm.
The next weekend was cloudy.
The previous day was cloudy.
The following day was pleasant.
The prior afternoon was relaxing.
The early day was bright.
The previous night was quiet.
The previous night was still.
The early evening was relaxing.
The late afternoon was pleasant.
The later night was quiet.
The early day was uneventful.
The previous day was warm.
The next night was relaxing.
The weekend was still.
The following morning was uneventful.
The late night was warm.
The previous day was bright.
The past weekend was cool.
The last afternoon was gentle.
The early morning was pleasant.
The late afternoon was warm.
The following morning was relaxing.
The next weekend was quiet.
The night was calm.
The following day was relaxing.
The later night was uneventful.
The previous night was uneventful.
The previous night was calm.
The rainy afternoon was cloudy.
The prior afternoon was quiet.
The early morning was bright.
The late evening was calm.
The sunny morning was gentle.
The prior afternoon was cloudy.
The following evening was cloudy.
The box contains the key.
The morning was warm.
The morning was cool.
The item in the box is
```

| 候选原文 | token IDs | 逐token log-prob nat |
|---|---|---|
| ' key.' | [1376, 13] | [-5.904272079467773, -4.926126956939697] |
| ' spoon.' | [45505, 13] | [-14.013647079467773, -4.592161178588867] |

### 间隔16，事实B的完整前缀

```text
Record:
The weekend was relaxing.
The morning was relaxing.
The past evening was warm.
The early morning was gentle.
The afternoon was relaxing.
The last afternoon was pleasant.
The late afternoon was cloudy.
The early day was peaceful.
The next morning was cool.
The next morning was quiet.
The previous night was warm.
The long weekend was relaxing.
The night was quiet.
The next afternoon was warm.
The early evening was cloudy.
The next weekend was calm.
The weekend was pleasant.
The late night was peaceful.
The following evening was warm.
The following night was gentle.
The evening was peaceful.
The afternoon was gentle.
The past weekend was bright.
The following night was cloudy.
The next night was calm.
The weekend was uneventful.
The late night was cool.
The rainy afternoon was quiet.
The early morning was still.
The late evening was quiet.
The early day was warm.
The past evening was calm.
The following evening was cool.
The day was pleasant.
The previous day was relaxing.
The late afternoon was still.
The morning was cloudy.
The following day was quiet.
The previous day was pleasant.
The evening was cool.
The past evening was gentle.
The long weekend was gentle.
The previous night was relaxing.
The next weekend was pleasant.
The last afternoon was bright.
The next afternoon was still.
The morning was peaceful.
The next night was cool.
The evening was uneventful.
The long weekend was uneventful.
The early evening was uneventful.
The weekend was calm.
The next weekend was gentle.
Time passed.
The previous weekend was cloudy.
The past weekend was warm.
The sunny morning was cloudy.
The next weekend was bright.
The previous day was peaceful.
The afternoon was pleasant.
The early day was calm.
The early evening was calm.
The sunny morning was relaxing.
The following night was still.
The rainy afternoon was peaceful.
The previous morning was cloudy.
The weekend was gentle.
The next night was pleasant.
The day was calm.
The day was gentle.
The past weekend was still.
The night was bright.
The long weekend was warm.
The previous day was still.
The next morning was uneventful.
The past evening was relaxing.
The early day was quiet.
The past weekend was calm.
The next afternoon was uneventful.
The later night was peaceful.
The later night was pleasant.
The night was peaceful.
The early evening was warm.
The night was relaxing.
The afternoon was warm.
The early evening was quiet.
The day was cloudy.
The night was gentle.
The following night was relaxing.
The later night was still.
The next morning was cloudy.
The past weekend was uneventful.
The weekend was peaceful.
The next night was peaceful.
The last afternoon was uneventful.
The following day was bright.
The following morning was peaceful.
The previous weekend was bright.
The night was cool.
The later night was bright.
The next night was quiet.
The following evening was uneventful.
The previous night was cloudy.
The next afternoon was quiet.
The past weekend was peaceful.
The late evening was still.
The following day was still.
The previous morning was bright.
The following day was cool.
The next morning was pleasant.
The previous morning was still.
The previous weekend was pleasant.
The evening was pleasant.
The following morning was bright.
The late night was calm.
The prior afternoon was pleasant.
The morning was uneventful.
The past weekend was pleasant.
The last afternoon was quiet.
The early morning was uneventful.
The late afternoon was gentle.
The past weekend was cloudy.
The afternoon was cool.
The late night was pleasant.
The weekend was cool.
The rainy afternoon was bright.
The early day was gentle.
The afternoon was calm.
The previous morning was gentle.
The afternoon was uneventful.
The sunny morning was still.
The last afternoon was peaceful.
The early morning was calm.
The next night was uneventful.
The following day was calm.
The next afternoon was peaceful.
The night was still.
The previous day was quiet.
The following day was uneventful.
The rainy afternoon was still.
The rainy afternoon was uneventful.
The late evening was cloudy.
The long weekend was still.
The early morning was peaceful.
The late afternoon was cool.
The early morning was warm.
The following night was bright.
The next weekend was cool.
The next afternoon was bright.
The previous night was cool.
The previous weekend was still.
The following evening was still.
The following night was warm.
The next weekend was cloudy.
The previous day was cloudy.
The following day was pleasant.
The prior afternoon was relaxing.
The early day was bright.
The previous night was quiet.
The previous night was still.
The early evening was relaxing.
The late afternoon was pleasant.
The later night was quiet.
The early day was uneventful.
The previous day was warm.
The next night was relaxing.
The weekend was still.
The following morning was uneventful.
The late night was warm.
The previous day was bright.
The past weekend was cool.
The last afternoon was gentle.
The early morning was pleasant.
The late afternoon was warm.
The following morning was relaxing.
The next weekend was quiet.
The night was calm.
The following day was relaxing.
The later night was uneventful.
The previous night was uneventful.
The previous night was calm.
The rainy afternoon was cloudy.
The prior afternoon was quiet.
The early morning was bright.
The late evening was calm.
The sunny morning was gentle.
The prior afternoon was cloudy.
The following evening was cloudy.
The box contains the spoon.
The morning was warm.
The morning was cool.
The item in the box is
```

| 候选原文 | token IDs | 逐token log-prob nat |
|---|---|---|
| ' key.' | [1376, 13] | [-9.076864242553711, -4.811996936798096] |
| ' spoon.' | [45505, 13] | [-8.764364242553711, -4.451949119567871] |

### 间隔1024，事实A的完整前缀

```text
Record:
The weekend was relaxing.
The morning was relaxing.
The past evening was warm.
The early morning was gentle.
The afternoon was relaxing.
The last afternoon was pleasant.
The late afternoon was cloudy.
The early day was peaceful.
The next morning was cool.
The next morning was quiet.
The previous night was warm.
The long weekend was relaxing.
The night was quiet.
The next afternoon was warm.
The early evening was cloudy.
The next weekend was calm.
The weekend was pleasant.
The late night was peaceful.
The following evening was warm.
The following night was gentle.
The evening was peaceful.
The box contains the key.
The afternoon was gentle.
The past weekend was bright.
The following night was cloudy.
The next night was calm.
The weekend was uneventful.
The late night was cool.
The rainy afternoon was quiet.
The early morning was still.
The late evening was quiet.
The early day was warm.
The past evening was calm.
The following evening was cool.
The day was pleasant.
The previous day was relaxing.
The late afternoon was still.
The morning was cloudy.
The following day was quiet.
The previous day was pleasant.
The evening was cool.
The past evening was gentle.
The long weekend was gentle.
The previous night was relaxing.
The next weekend was pleasant.
The last afternoon was bright.
The next afternoon was still.
The morning was peaceful.
The next night was cool.
The evening was uneventful.
The long weekend was uneventful.
The early evening was uneventful.
The weekend was calm.
The next weekend was gentle.
Time passed.
The previous weekend was cloudy.
The past weekend was warm.
The sunny morning was cloudy.
The next weekend was bright.
The previous day was peaceful.
The afternoon was pleasant.
The early day was calm.
The early evening was calm.
The sunny morning was relaxing.
The following night was still.
The rainy afternoon was peaceful.
The previous morning was cloudy.
The weekend was gentle.
The next night was pleasant.
The day was calm.
The day was gentle.
The past weekend was still.
The night was bright.
The long weekend was warm.
The previous day was still.
The next morning was uneventful.
The past evening was relaxing.
The early day was quiet.
The past weekend was calm.
The next afternoon was uneventful.
The later night was peaceful.
The later night was pleasant.
The night was peaceful.
The early evening was warm.
The night was relaxing.
The afternoon was warm.
The early evening was quiet.
The day was cloudy.
The night was gentle.
The following night was relaxing.
The later night was still.
The next morning was cloudy.
The past weekend was uneventful.
The weekend was peaceful.
The next night was peaceful.
The last afternoon was uneventful.
The following day was bright.
The following morning was peaceful.
The previous weekend was bright.
The night was cool.
The later night was bright.
The next night was quiet.
The following evening was uneventful.
The previous night was cloudy.
The next afternoon was quiet.
The past weekend was peaceful.
The late evening was still.
The following day was still.
The previous morning was bright.
The following day was cool.
The next morning was pleasant.
The previous morning was still.
The previous weekend was pleasant.
The evening was pleasant.
The following morning was bright.
The late night was calm.
The prior afternoon was pleasant.
The morning was uneventful.
The past weekend was pleasant.
The last afternoon was quiet.
The early morning was uneventful.
The late afternoon was gentle.
The past weekend was cloudy.
The afternoon was cool.
The late night was pleasant.
The weekend was cool.
The rainy afternoon was bright.
The early day was gentle.
The afternoon was calm.
The previous morning was gentle.
The afternoon was uneventful.
The sunny morning was still.
The last afternoon was peaceful.
The early morning was calm.
The next night was uneventful.
The following day was calm.
The next afternoon was peaceful.
The night was still.
The previous day was quiet.
The following day was uneventful.
The rainy afternoon was still.
The rainy afternoon was uneventful.
The late evening was cloudy.
The long weekend was still.
The early morning was peaceful.
The late afternoon was cool.
The early morning was warm.
The following night was bright.
The next weekend was cool.
The next afternoon was bright.
The previous night was cool.
The previous weekend was still.
The following evening was still.
The following night was warm.
The next weekend was cloudy.
The previous day was cloudy.
The following day was pleasant.
The prior afternoon was relaxing.
The early day was bright.
The previous night was quiet.
The previous night was still.
The early evening was relaxing.
The late afternoon was pleasant.
The later night was quiet.
The early day was uneventful.
The previous day was warm.
The next night was relaxing.
The weekend was still.
The following morning was uneventful.
The late night was warm.
The previous day was bright.
The past weekend was cool.
The last afternoon was gentle.
The early morning was pleasant.
The late afternoon was warm.
The following morning was relaxing.
The next weekend was quiet.
The night was calm.
The following day was relaxing.
The later night was uneventful.
The previous night was uneventful.
The previous night was calm.
The rainy afternoon was cloudy.
The prior afternoon was quiet.
The early morning was bright.
The late evening was calm.
The sunny morning was gentle.
The prior afternoon was cloudy.
The following evening was cloudy.
The morning was warm.
The morning was cool.
The item in the box is
```

| 候选原文 | token IDs | 逐token log-prob nat |
|---|---|---|
| ' key.' | [1376, 13] | [-4.141861438751221, -4.918541431427002] |
| ' spoon.' | [45505, 13] | [-14.298110961914062, -4.491756439208984] |

### 间隔1024，事实B的完整前缀

```text
Record:
The weekend was relaxing.
The morning was relaxing.
The past evening was warm.
The early morning was gentle.
The afternoon was relaxing.
The last afternoon was pleasant.
The late afternoon was cloudy.
The early day was peaceful.
The next morning was cool.
The next morning was quiet.
The previous night was warm.
The long weekend was relaxing.
The night was quiet.
The next afternoon was warm.
The early evening was cloudy.
The next weekend was calm.
The weekend was pleasant.
The late night was peaceful.
The following evening was warm.
The following night was gentle.
The evening was peaceful.
The box contains the spoon.
The afternoon was gentle.
The past weekend was bright.
The following night was cloudy.
The next night was calm.
The weekend was uneventful.
The late night was cool.
The rainy afternoon was quiet.
The early morning was still.
The late evening was quiet.
The early day was warm.
The past evening was calm.
The following evening was cool.
The day was pleasant.
The previous day was relaxing.
The late afternoon was still.
The morning was cloudy.
The following day was quiet.
The previous day was pleasant.
The evening was cool.
The past evening was gentle.
The long weekend was gentle.
The previous night was relaxing.
The next weekend was pleasant.
The last afternoon was bright.
The next afternoon was still.
The morning was peaceful.
The next night was cool.
The evening was uneventful.
The long weekend was uneventful.
The early evening was uneventful.
The weekend was calm.
The next weekend was gentle.
Time passed.
The previous weekend was cloudy.
The past weekend was warm.
The sunny morning was cloudy.
The next weekend was bright.
The previous day was peaceful.
The afternoon was pleasant.
The early day was calm.
The early evening was calm.
The sunny morning was relaxing.
The following night was still.
The rainy afternoon was peaceful.
The previous morning was cloudy.
The weekend was gentle.
The next night was pleasant.
The day was calm.
The day was gentle.
The past weekend was still.
The night was bright.
The long weekend was warm.
The previous day was still.
The next morning was uneventful.
The past evening was relaxing.
The early day was quiet.
The past weekend was calm.
The next afternoon was uneventful.
The later night was peaceful.
The later night was pleasant.
The night was peaceful.
The early evening was warm.
The night was relaxing.
The afternoon was warm.
The early evening was quiet.
The day was cloudy.
The night was gentle.
The following night was relaxing.
The later night was still.
The next morning was cloudy.
The past weekend was uneventful.
The weekend was peaceful.
The next night was peaceful.
The last afternoon was uneventful.
The following day was bright.
The following morning was peaceful.
The previous weekend was bright.
The night was cool.
The later night was bright.
The next night was quiet.
The following evening was uneventful.
The previous night was cloudy.
The next afternoon was quiet.
The past weekend was peaceful.
The late evening was still.
The following day was still.
The previous morning was bright.
The following day was cool.
The next morning was pleasant.
The previous morning was still.
The previous weekend was pleasant.
The evening was pleasant.
The following morning was bright.
The late night was calm.
The prior afternoon was pleasant.
The morning was uneventful.
The past weekend was pleasant.
The last afternoon was quiet.
The early morning was uneventful.
The late afternoon was gentle.
The past weekend was cloudy.
The afternoon was cool.
The late night was pleasant.
The weekend was cool.
The rainy afternoon was bright.
The early day was gentle.
The afternoon was calm.
The previous morning was gentle.
The afternoon was uneventful.
The sunny morning was still.
The last afternoon was peaceful.
The early morning was calm.
The next night was uneventful.
The following day was calm.
The next afternoon was peaceful.
The night was still.
The previous day was quiet.
The following day was uneventful.
The rainy afternoon was still.
The rainy afternoon was uneventful.
The late evening was cloudy.
The long weekend was still.
The early morning was peaceful.
The late afternoon was cool.
The early morning was warm.
The following night was bright.
The next weekend was cool.
The next afternoon was bright.
The previous night was cool.
The previous weekend was still.
The following evening was still.
The following night was warm.
The next weekend was cloudy.
The previous day was cloudy.
The following day was pleasant.
The prior afternoon was relaxing.
The early day was bright.
The previous night was quiet.
The previous night was still.
The early evening was relaxing.
The late afternoon was pleasant.
The later night was quiet.
The early day was uneventful.
The previous day was warm.
The next night was relaxing.
The weekend was still.
The following morning was uneventful.
The late night was warm.
The previous day was bright.
The past weekend was cool.
The last afternoon was gentle.
The early morning was pleasant.
The late afternoon was warm.
The following morning was relaxing.
The next weekend was quiet.
The night was calm.
The following day was relaxing.
The later night was uneventful.
The previous night was uneventful.
The previous night was calm.
The rainy afternoon was cloudy.
The prior afternoon was quiet.
The early morning was bright.
The late evening was calm.
The sunny morning was gentle.
The prior afternoon was cloudy.
The following evening was cloudy.
The morning was warm.
The morning was cool.
The item in the box is
```

| 候选原文 | token IDs | 逐token log-prob nat |
|---|---|---|
| ' key.' | [1376, 13] | [-9.169488906860352, -4.253189563751221] |
| ' spoon.' | [45505, 13] | [-9.903863906860352, -4.097054958343506] |

所有其他原文、offset及候选在execution data/panel.jsonl，每状态原始分数在results/full，均可按id连接；报告未更改文本。
