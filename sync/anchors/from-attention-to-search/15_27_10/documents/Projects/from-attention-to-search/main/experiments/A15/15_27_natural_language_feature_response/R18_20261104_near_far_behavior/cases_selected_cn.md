派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R18_20261104_near_far_behavior/cases_selected_cn.md`。
[精确原始文件](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R18_20261104_near_far_behavior/cases_selected_cn.md)；研究修改仍回到原件。

---

# 原文和原始分数

每组完整A/B前缀与所有候选token分数均保留。自然对数为单位nat，总分越高越偏好；每token均分不代替主判定。展示规则在评分前冻结：优先128首个成功、首个失败，若无再查64／16；另报首个诱饵失败。本轮不是自由生成测试。全部原始记录在/data/250010109/MoE_Router/experiments/20261104_near_far_object_fact_use/R01_behavior/data/panel.jsonl与results/*.jsonl。

## 成功配对：F05，cup / mug，main，计划d=128

### 事实A；正确答案cup

```text
Record:
The weekend was cool.
The day was peaceful.
The evening was pleasant.
The night was pleasant.
The night was peaceful.
Rain continued until dawn.
The early morning was warm.
The evening was quiet.
The evening was cool.
The morning was quiet.
The weekend was calm.
The early morning was bright.
The temperature remained steady.
The morning was pleasant.
The late afternoon was calm.
The weekend was peaceful.
The sky became clearer later.
The morning was peaceful.
The wind eased before midnight.
The night was warm.
The late afternoon was quiet.
The day was cool.
The afternoon was quiet.
The evening was calm.
The weekend was quiet.
The late afternoon was bright.
The late afternoon was cool.
The evening was peaceful.
The day was quiet.
The early morning was quiet.
The evening was warm.
The afternoon was cool.
The morning was calm.
The night was calm.
The day was bright.
The pouch contains the cup.
The weather was mild.
The late afternoon was warm.
The afternoon was bright.
The day was pleasant.
The late afternoon was cloudy.
The day was calm.
The early morning was calm.
The weekend was warm.
The night was cool.
The afternoon was warm.
The morning was cool.
A breeze arrived after noon.
The morning was cloudy.
The morning was warm.
The evening was bright.
The night was cloudy.
The early morning was cool.
The late afternoon was pleasant.
The night was bright.
The afternoon was cloudy.
The late afternoon was peaceful.
The afternoon was pleasant.
Morning came.
What is in the pouch?
Answer:
```

前缀320token；证据物品`cup`的全部token ID=[10525]、位置=[190]；最后e=190；p=319、目标token ID=25。实际间隔d=128，两端都排除。完整前缀ID／offset见panel.jsonl中`F05_main_128_A`。

| 候选 | 完整token序列 | 逐token logprob | 总分 nat | 每token均分 |
|---|---|---|---|---|
|  cup. | [10525, 13] | [-4.346385956, -2.948430538] | -7.294816494 | -3.647408247 |
|  mug. | [51489, 13] | [-9.370889664, -3.754960775] | -13.125850439 | -6.562925220 |

模型候选首选=A；是否正确=True；正确减错误=5.831033945 nat。

### 事实B；正确答案mug

```text
Record:
The weekend was cool.
The day was peaceful.
The evening was pleasant.
The night was pleasant.
The night was peaceful.
Rain continued until dawn.
The early morning was warm.
The evening was quiet.
The evening was cool.
The morning was quiet.
The weekend was calm.
The early morning was bright.
The temperature remained steady.
The morning was pleasant.
The late afternoon was calm.
The weekend was peaceful.
The sky became clearer later.
The morning was peaceful.
The wind eased before midnight.
The night was warm.
The late afternoon was quiet.
The day was cool.
The afternoon was quiet.
The evening was calm.
The weekend was quiet.
The late afternoon was bright.
The late afternoon was cool.
The evening was peaceful.
The day was quiet.
The early morning was quiet.
The evening was warm.
The afternoon was cool.
The morning was calm.
The night was calm.
The day was bright.
The pouch contains the mug.
The weather was mild.
The late afternoon was warm.
The afternoon was bright.
The day was pleasant.
The late afternoon was cloudy.
The day was calm.
The early morning was calm.
The weekend was warm.
The night was cool.
The afternoon was warm.
The morning was cool.
A breeze arrived after noon.
The morning was cloudy.
The morning was warm.
The evening was bright.
The night was cloudy.
The early morning was cool.
The late afternoon was pleasant.
The night was bright.
The afternoon was cloudy.
The late afternoon was peaceful.
The afternoon was pleasant.
Morning came.
What is in the pouch?
Answer:
```

前缀320token；证据物品`mug`的全部token ID=[51489]、位置=[190]；最后e=190；p=319、目标token ID=25。实际间隔d=128，两端都排除。完整前缀ID／offset见panel.jsonl中`F05_main_128_B`。

| 候选 | 完整token序列 | 逐token logprob | 总分 nat | 每token均分 |
|---|---|---|---|---|
|  cup. | [10525, 13] | [-8.698576927, -2.979955196] | -11.678532124 | -5.839266062 |
|  mug. | [51489, 13] | [-5.13057375, -3.615938425] | -8.746512175 | -4.373256087 |

模型候选首选=B；是否正确=True；正确减错误=2.932019949 nat。

两事实均正确=1；A事实下正确边际=5.831034，B事实下正确边际=2.932020；无确定事实基线A减B=1.805526 nat。

## 近处错误物品诱饵：失败：F10，hat / cap，lure，计划d=128

### 事实A；正确答案hat

```text
Record:
Shadows grew longer by evening.
The early morning was pleasant.
The morning was peaceful.
The afternoon was calm.
The evening was warm.
The early morning was calm.
The afternoon was pleasant.
The late afternoon was pleasant.
Sunlight faded near sunset.
The day was calm.
The evening was quiet.
The night was bright.
The afternoon was cloudy.
The weekend was bright.
The night was pleasant.
The wind eased before midnight.
The morning was quiet.
The morning was bright.
A breeze arrived after noon.
The afternoon was bright.
The evening was calm.
The evening was cloudy.
The early morning was warm.
The weather was mild.
The late afternoon was peaceful.
The evening was peaceful.
The day was quiet.
The night was cool.
The early morning was cloudy.
The early morning was quiet.
The day was warm.
The weekend was peaceful.
The weekend was cloudy.
The night was warm.
Inside the chest there is the hat.
The late afternoon was warm.
The late afternoon was calm.
The late afternoon was bright.
The late afternoon was quiet.
The day was cool.
The morning was calm.
The weekend was quiet.
The weekend was warm.
The morning was cloudy.
The day was peaceful.
Rain continued until dawn.
The night was cloudy.
The evening was bright.
The night was quiet.
The weekend was cool.
The late afternoon was cool.
The weekend was calm.
The day was cloudy.
The afternoon was warm.
The night was calm.
The evening was cool.
Time passed.
The other container holds the cap.
What does the chest contain?
Answer:
```

前缀320token；证据物品`hat`的全部token ID=[8896]、位置=[190]；最后e=190；p=319、目标token ID=25。实际间隔d=128，两端都排除。完整前缀ID／offset见panel.jsonl中`F10_lure_128_A`。

| 候选 | 完整token序列 | 逐token logprob | 总分 nat | 每token均分 |
|---|---|---|---|---|
|  hat. | [8896, 13] | [-7.585793018, -3.316061258] | -10.901854277 | -5.450927138 |
|  cap. | [2062, 13] | [-5.668600559, -2.956992626] | -8.625593185 | -4.312796593 |

模型候选首选=B；是否正确=False；正确减错误=-2.276261091 nat。

### 事实B；正确答案cap

```text
Record:
Shadows grew longer by evening.
The early morning was pleasant.
The morning was peaceful.
The afternoon was calm.
The evening was warm.
The early morning was calm.
The afternoon was pleasant.
The late afternoon was pleasant.
Sunlight faded near sunset.
The day was calm.
The evening was quiet.
The night was bright.
The afternoon was cloudy.
The weekend was bright.
The night was pleasant.
The wind eased before midnight.
The morning was quiet.
The morning was bright.
A breeze arrived after noon.
The afternoon was bright.
The evening was calm.
The evening was cloudy.
The early morning was warm.
The weather was mild.
The late afternoon was peaceful.
The evening was peaceful.
The day was quiet.
The night was cool.
The early morning was cloudy.
The early morning was quiet.
The day was warm.
The weekend was peaceful.
The weekend was cloudy.
The night was warm.
Inside the chest there is the cap.
The late afternoon was warm.
The late afternoon was calm.
The late afternoon was bright.
The late afternoon was quiet.
The day was cool.
The morning was calm.
The weekend was quiet.
The weekend was warm.
The morning was cloudy.
The day was peaceful.
Rain continued until dawn.
The night was cloudy.
The evening was bright.
The night was quiet.
The weekend was cool.
The late afternoon was cool.
The weekend was calm.
The day was cloudy.
The afternoon was warm.
The night was calm.
The evening was cool.
Time passed.
The other container holds the hat.
What does the chest contain?
Answer:
```

前缀320token；证据物品`cap`的全部token ID=[2062]、位置=[190]；最后e=190；p=319、目标token ID=25。实际间隔d=128，两端都排除。完整前缀ID／offset见panel.jsonl中`F10_lure_128_B`。

| 候选 | 完整token序列 | 逐token logprob | 总分 nat | 每token均分 |
|---|---|---|---|---|
|  hat. | [8896, 13] | [-7.249449253, -3.428558826] | -10.678008080 | -5.339004040 |
|  cap. | [2062, 13] | [-6.455061436, -3.003599167] | -9.458660603 | -4.729330301 |

模型候选首选=B；是否正确=True；正确减错误=1.219347477 nat。

两事实均正确=0；A事实下正确边际=-2.276261，B事实下正确边际=1.219347；无确定事实基线A减B=-1.698397 nat。

## 预定去句号敏感性：全部不一致案例：F28，card / stamp，main，计划d=64

### 事实A；正确答案card

```text
Record:
The afternoon was cloudy.
The night was cloudy.
The evening was warm.
The day was calm.
The morning was pleasant.
The night was cool.
The weather was mild.
The evening was calm.
The morning was bright.
The day was pleasant.
The morning was cloudy.
The weekend was pleasant.
The evening was bright.
The early morning was quiet.
The weekend was cool.
The day was bright.
The early morning was cool.
The morning was calm.
The evening was cool.
Sunlight faded near sunset.
The morning was peaceful.
The day was warm.
The weekend was warm.
Rain continued until dawn.
The morning was cool.
The day was cloudy.
The morning was warm.
The afternoon was quiet.
The late afternoon was warm.
The day was quiet.
The night was pleasant.
The early morning was bright.
The early morning was calm.
The evening was pleasant.
Morning came.
The weekend was peaceful.
The afternoon was cool.
The weekend was quiet.
The day was peaceful.
The night was warm.
The night was calm.
The late afternoon was cool.
The afternoon was warm.
The weekend was cloudy.
The late afternoon was bright.
The late afternoon was peaceful.
The wind eased before midnight.
According to the note, the tin holds the card.
The afternoon was peaceful.
The late afternoon was cloudy.
The weekend was bright.
The weekend was calm.
The morning was quiet.
The day was cool.
The early morning was pleasant.
The night was quiet.
Clouds drifted slowly overhead.
Time passed.
It rained.
Which item is in the tin?
Answer:
```

前缀320token；证据物品`card`的全部token ID=[3701]、位置=[254]；最后e=254；p=319、目标token ID=25。实际间隔d=64，两端都排除。完整前缀ID／offset见panel.jsonl中`F28_main_64_A`。

| 候选 | 完整token序列 | 逐token logprob | 总分 nat | 每token均分 |
|---|---|---|---|---|
|  card. | [3701, 13] | [-6.174668312, -3.795941353] | -9.970609665 | -4.985304832 |
|  stamp. | [21206, 13] | [-12.806794167, -3.506427288] | -16.313221455 | -8.156610727 |

模型候选首选=A；是否正确=True；正确减错误=6.342611790 nat。

### 事实B；正确答案stamp

```text
Record:
The afternoon was cloudy.
The night was cloudy.
The evening was warm.
The day was calm.
The morning was pleasant.
The night was cool.
The weather was mild.
The evening was calm.
The morning was bright.
The day was pleasant.
The morning was cloudy.
The weekend was pleasant.
The evening was bright.
The early morning was quiet.
The weekend was cool.
The day was bright.
The early morning was cool.
The morning was calm.
The evening was cool.
Sunlight faded near sunset.
The morning was peaceful.
The day was warm.
The weekend was warm.
Rain continued until dawn.
The morning was cool.
The day was cloudy.
The morning was warm.
The afternoon was quiet.
The late afternoon was warm.
The day was quiet.
The night was pleasant.
The early morning was bright.
The early morning was calm.
The evening was pleasant.
Morning came.
The weekend was peaceful.
The afternoon was cool.
The weekend was quiet.
The day was peaceful.
The night was warm.
The night was calm.
The late afternoon was cool.
The afternoon was warm.
The weekend was cloudy.
The late afternoon was bright.
The late afternoon was peaceful.
The wind eased before midnight.
According to the note, the tin holds the stamp.
The afternoon was peaceful.
The late afternoon was cloudy.
The weekend was bright.
The weekend was calm.
The morning was quiet.
The day was cool.
The early morning was pleasant.
The night was quiet.
Clouds drifted slowly overhead.
Time passed.
It rained.
Which item is in the tin?
Answer:
```

前缀320token；证据物品`stamp`的全部token ID=[21206]、位置=[254]；最后e=254；p=319、目标token ID=25。实际间隔d=64，两端都排除。完整前缀ID／offset见panel.jsonl中`F28_main_64_B`。

| 候选 | 完整token序列 | 逐token logprob | 总分 nat | 每token均分 |
|---|---|---|---|---|
|  card. | [3701, 13] | [-9.556379318, -3.940423965] | -13.496803284 | -6.748401642 |
|  stamp. | [21206, 13] | [-9.757873535, -3.508815765] | -13.266689301 | -6.633344650 |

模型候选首选=B；是否正确=True；正确减错误=0.230113983 nat。

两事实均正确=1；A事实下正确边际=6.342612，B事实下正确边际=0.230114；无确定事实基线A减B=2.478208 nat。

主实验留出没有失败配对；不虚构失败例。
