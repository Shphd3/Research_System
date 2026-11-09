# 完整原文、真实 feature 与候选评分

F23在留出读取前固定，取自旧R18首次留出失败；反例按协议规则确定，不更换主要六成员。所有数字来自真实前向。ID只在本字典有意义；本表不是语义命名或因果贡献。灰/零值代表实际未激活，不补选成员。

## F23

### ATTN_SAE：同一固定六成员

| 文本ID | #2520 | #26235 | #29969 | #23899 | #772 | #2254 | 候选A总分 | 候选B总分 | 选择 | 正确分差 |
|---|---|---|---|---|---|---|---|---|---|---|
| F23_main16_A | 4.9328 | 3.7756 | 6.1008 | 32.6751 | 3.5052 | 3.5788 | -8.6913 | -17.5696 | A | 8.8782 |
| F23_main16_B | 4.8470 | 4.1487 | 5.0533 | 33.3041 | 3.0309 | 3.2980 | -14.8533 | -9.7940 | B | 5.0593 |
| F23_main64_A | 4.2100 | 4.3685 | 6.3227 | 30.4227 | 3.4008 | 2.6902 | -6.8365 | -17.3444 | A | 10.5079 |
| F23_main64_B | 4.2493 | 4.8485 | 5.3124 | 32.0725 | 2.9275 | 2.6232 | -14.4406 | -8.3110 | B | 6.1295 |
| F23_main128_A | 3.9565 | 4.1611 | 6.3299 | 30.1031 | 3.3975 | 2.8114 | -6.9034 | -17.4149 | A | 10.5114 |
| F23_main128_B | 4.0235 | 4.7443 | 5.4932 | 31.8362 | 3.0244 | 2.5948 | -14.3000 | -8.5279 | B | 5.7720 |
| F23_nearN_A | 4.0832 | 2.3982 | 6.2934 | 31.5673 | 3.4426 | 3.3521 | -9.0567 | -16.8970 | A | 7.8403 |
| F23_nearN_B | 4.1291 | 2.7314 | 5.5463 | 32.3810 | 3.1863 | 3.2649 | -14.9192 | -10.3705 | B | 4.5487 |
| F23_nearA_A | 3.4762 | 3.2747 | 6.5557 | 31.2482 | 3.4096 | 3.1116 | -8.0813 | -17.5549 | A | 9.4736 |
| F23_nearA_B | 3.5003 | 3.3469 | 6.0378 | 32.1311 | 3.3032 | 2.9445 | -8.8371 | -9.6264 | A | -0.7893 |
| F23_nearB_A | 3.3620 | 3.1796 | 5.9528 | 31.9283 | 3.2022 | 3.1685 | -8.1911 | -10.1139 | A | 1.9229 |
| F23_nearB_B | 3.9007 | 3.5383 | 5.8541 | 32.1289 | 3.0734 | 3.0229 | -15.0070 | -9.5110 | B | 5.4960 |

同一族的相对强弱分解：T投影=0.4903，近词N投影=0.4823，相反条件保留=0.0080；模式损失=0.9920，行为分差损失=5.6277 nat；严格支持=True。T−N为恒等式，不是额外发现。

### MLPIN_SAE：同一固定六成员

| 文本ID | #17390 | #25508 | #3011 | #4700 | #16240 | #27076 | 候选A总分 | 候选B总分 | 选择 | 正确分差 |
|---|---|---|---|---|---|---|---|---|---|---|
| F23_main16_A | 11.9461 | 0.0000 | 4.6446 | 6.1749 | 17.3311 | 12.9109 | -8.6913 | -17.5696 | A | 8.8782 |
| F23_main16_B | 11.2632 | 2.8038 | 4.3200 | 5.9867 | 14.6659 | 13.6424 | -14.8533 | -9.7940 | B | 5.0593 |
| F23_main64_A | 10.0735 | 3.5882 | 5.6557 | 5.9348 | 20.4350 | 11.9969 | -6.8365 | -17.3444 | A | 10.5079 |
| F23_main64_B | 8.6132 | 3.9844 | 5.2371 | 5.6805 | 16.0065 | 12.4472 | -14.4406 | -8.3110 | B | 6.1295 |
| F23_main128_A | 9.8294 | 3.4805 | 5.5980 | 5.8732 | 20.5510 | 11.7979 | -6.9034 | -17.4149 | A | 10.5114 |
| F23_main128_B | 8.6073 | 3.9980 | 5.1109 | 5.4551 | 16.1872 | 12.1418 | -14.3000 | -8.5279 | B | 5.7720 |
| F23_nearN_A | 7.8277 | 3.7913 | 5.7305 | 6.8684 | 18.8802 | 12.8812 | -9.0567 | -16.8970 | A | 7.8403 |
| F23_nearN_B | 7.4179 | 3.9407 | 5.4201 | 6.8184 | 15.7281 | 13.5152 | -14.9192 | -10.3705 | B | 4.5487 |
| F23_nearA_A | 8.5853 | 3.5081 | 5.7458 | 6.4414 | 19.5579 | 10.9803 | -8.0813 | -17.5549 | A | 9.4736 |
| F23_nearA_B | 9.9673 | 3.2722 | 5.1052 | 6.1574 | 18.0583 | 11.2466 | -8.8371 | -9.6264 | A | -0.7893 |
| F23_nearB_A | 9.6226 | 3.1275 | 5.1482 | 6.3560 | 18.5635 | 11.9607 | -8.1911 | -10.1139 | A | 1.9229 |
| F23_nearB_B | 8.0898 | 3.6694 | 5.1039 | 6.2147 | 15.8441 | 12.2463 | -15.0070 | -9.5110 | B | 5.4960 |

同一族的相对强弱分解：T投影=0.6001，近词N投影=0.6631，相反条件保留=-0.0631；模式损失=1.0631，行为分差损失=5.6277 nat；严格支持=True。T−N为恒等式，不是额外发现。

### F23_main16_A：完整前缀

远目标=battery；近处=None；e=302，目标物品token=[11602]；p=319，token=25；d=16。近处token位置=[]，IDs=[]。

```text
Record:
Clouds drifted slowly overhead.
The evening was cool.
The weekend was peaceful.
Rain continued until dawn.
The afternoon was peaceful.
The day was cloudy.
The night was pleasant.
The day was peaceful.
The late afternoon was pleasant.
The evening was calm.
The night was calm.
The morning was peaceful.
It rained.
The afternoon was bright.
The evening was bright.
Morning came.
The weekend was bright.
The early morning was peaceful.
The night was cloudy.
The late afternoon was warm.
The early morning was cloudy.
The weekend was pleasant.
The evening was pleasant.
The morning was pleasant.
The day was calm.
The afternoon was warm.
The day was pleasant.
The wind eased before midnight.
The temperature remained steady.
The late afternoon was cool.
The late afternoon was peaceful.
The early morning was warm.
The evening was warm.
The late afternoon was cloudy.
The evening was cloudy.
The late afternoon was calm.
The morning was cool.
The late afternoon was bright.
A breeze arrived after noon.
The weekend was warm.
The early morning was calm.
The weekend was cool.
The day was bright.
The day was warm.
The afternoon was quiet.
The evening was peaceful.
The afternoon was pleasant.
The weather was mild.
The evening was quiet.
The morning was calm.
The morning was cloudy.
The afternoon was cloudy.
The night was peaceful.
The night was cool.
The day was cool.
The morning was warm.
Time passed.
The drawer was packed with the battery.
Shadows grew longer by evening.
What was stored in the drawer?
Answer:
```

| 候选完整串 | token IDs | 逐token条件log p | 完整总分 | 物品部分 | 句号部分 |
|---|---|---|---|---|---|
| ' battery.' | [11602, 13] | [-5.692725658416748, -2.998610019683838] | -8.6913 | -5.6927 | -2.9986 |
| ' magnet.' | [32197, 13] | [-14.055519104003906, -3.5140323638916016] | -17.5696 | -14.0555 | -3.5140 |

### F23_main16_B：完整前缀

远目标=magnet；近处=None；e=302，目标物品token=[32197]；p=319，token=25；d=16。近处token位置=[]，IDs=[]。

```text
Record:
Clouds drifted slowly overhead.
The evening was cool.
The weekend was peaceful.
Rain continued until dawn.
The afternoon was peaceful.
The day was cloudy.
The night was pleasant.
The day was peaceful.
The late afternoon was pleasant.
The evening was calm.
The night was calm.
The morning was peaceful.
It rained.
The afternoon was bright.
The evening was bright.
Morning came.
The weekend was bright.
The early morning was peaceful.
The night was cloudy.
The late afternoon was warm.
The early morning was cloudy.
The weekend was pleasant.
The evening was pleasant.
The morning was pleasant.
The day was calm.
The afternoon was warm.
The day was pleasant.
The wind eased before midnight.
The temperature remained steady.
The late afternoon was cool.
The late afternoon was peaceful.
The early morning was warm.
The evening was warm.
The late afternoon was cloudy.
The evening was cloudy.
The late afternoon was calm.
The morning was cool.
The late afternoon was bright.
A breeze arrived after noon.
The weekend was warm.
The early morning was calm.
The weekend was cool.
The day was bright.
The day was warm.
The afternoon was quiet.
The evening was peaceful.
The afternoon was pleasant.
The weather was mild.
The evening was quiet.
The morning was calm.
The morning was cloudy.
The afternoon was cloudy.
The night was peaceful.
The night was cool.
The day was cool.
The morning was warm.
Time passed.
The drawer was packed with the magnet.
Shadows grew longer by evening.
What was stored in the drawer?
Answer:
```

| 候选完整串 | token IDs | 逐token条件log p | 完整总分 | 物品部分 | 句号部分 |
|---|---|---|---|---|---|
| ' battery.' | [11602, 13] | [-11.497715950012207, -3.3556201457977295] | -14.8533 | -11.4977 | -3.3556 |
| ' magnet.' | [32197, 13] | [-6.43993616104126, -3.354058265686035] | -9.7940 | -6.4399 | -3.3541 |

### F23_main64_A：完整前缀

远目标=battery；近处=None；e=254，目标物品token=[11602]；p=319，token=25；d=64。近处token位置=[]，IDs=[]。

```text
Record:
Clouds drifted slowly overhead.
The evening was cool.
The weekend was peaceful.
Rain continued until dawn.
The afternoon was peaceful.
The day was cloudy.
The night was pleasant.
The day was peaceful.
The late afternoon was pleasant.
The evening was calm.
The night was calm.
The morning was peaceful.
It rained.
The afternoon was bright.
The evening was bright.
Morning came.
The weekend was bright.
The early morning was peaceful.
The night was cloudy.
The late afternoon was warm.
The early morning was cloudy.
The weekend was pleasant.
The evening was pleasant.
The morning was pleasant.
The day was calm.
The afternoon was warm.
The day was pleasant.
The wind eased before midnight.
The temperature remained steady.
The late afternoon was cool.
The late afternoon was peaceful.
The early morning was warm.
The evening was warm.
The late afternoon was cloudy.
The evening was cloudy.
The late afternoon was calm.
The morning was cool.
The late afternoon was bright.
A breeze arrived after noon.
The weekend was warm.
The early morning was calm.
The weekend was cool.
The day was bright.
The day was warm.
The afternoon was quiet.
The evening was peaceful.
The afternoon was pleasant.
The drawer was packed with the battery.
The weather was mild.
The evening was quiet.
The morning was calm.
The morning was cloudy.
The afternoon was cloudy.
The night was peaceful.
The night was cool.
The day was cool.
The morning was warm.
Time passed.
Shadows grew longer by evening.
What was stored in the drawer?
Answer:
```

| 候选完整串 | token IDs | 逐token条件log p | 完整总分 | 物品部分 | 句号部分 |
|---|---|---|---|---|---|
| ' battery.' | [11602, 13] | [-3.6029112339019775, -3.233588933944702] | -6.8365 | -3.6029 | -3.2336 |
| ' magnet.' | [32197, 13] | [-14.003509521484375, -3.3408567905426025] | -17.3444 | -14.0035 | -3.3409 |

### F23_main64_B：完整前缀

远目标=magnet；近处=None；e=254，目标物品token=[32197]；p=319，token=25；d=64。近处token位置=[]，IDs=[]。

```text
Record:
Clouds drifted slowly overhead.
The evening was cool.
The weekend was peaceful.
Rain continued until dawn.
The afternoon was peaceful.
The day was cloudy.
The night was pleasant.
The day was peaceful.
The late afternoon was pleasant.
The evening was calm.
The night was calm.
The morning was peaceful.
It rained.
The afternoon was bright.
The evening was bright.
Morning came.
The weekend was bright.
The early morning was peaceful.
The night was cloudy.
The late afternoon was warm.
The early morning was cloudy.
The weekend was pleasant.
The evening was pleasant.
The morning was pleasant.
The day was calm.
The afternoon was warm.
The day was pleasant.
The wind eased before midnight.
The temperature remained steady.
The late afternoon was cool.
The late afternoon was peaceful.
The early morning was warm.
The evening was warm.
The late afternoon was cloudy.
The evening was cloudy.
The late afternoon was calm.
The morning was cool.
The late afternoon was bright.
A breeze arrived after noon.
The weekend was warm.
The early morning was calm.
The weekend was cool.
The day was bright.
The day was warm.
The afternoon was quiet.
The evening was peaceful.
The afternoon was pleasant.
The drawer was packed with the magnet.
The weather was mild.
The evening was quiet.
The morning was calm.
The morning was cloudy.
The afternoon was cloudy.
The night was peaceful.
The night was cool.
The day was cool.
The morning was warm.
Time passed.
Shadows grew longer by evening.
What was stored in the drawer?
Answer:
```

| 候选完整串 | token IDs | 逐token条件log p | 完整总分 | 物品部分 | 句号部分 |
|---|---|---|---|---|---|
| ' battery.' | [11602, 13] | [-11.341506958007812, -3.0990607738494873] | -14.4406 | -11.3415 | -3.0991 |
| ' magnet.' | [32197, 13] | [-4.613895893096924, -3.697141647338867] | -8.3110 | -4.6139 | -3.6971 |

### F23_main128_A：完整前缀

远目标=battery；近处=None；e=190，目标物品token=[11602]；p=319，token=25；d=128。近处token位置=[]，IDs=[]。

```text
Record:
Clouds drifted slowly overhead.
The evening was cool.
The weekend was peaceful.
Rain continued until dawn.
The afternoon was peaceful.
The day was cloudy.
The night was pleasant.
The day was peaceful.
The late afternoon was pleasant.
The evening was calm.
The night was calm.
The morning was peaceful.
It rained.
The afternoon was bright.
The evening was bright.
Morning came.
The weekend was bright.
The early morning was peaceful.
The night was cloudy.
The late afternoon was warm.
The early morning was cloudy.
The weekend was pleasant.
The evening was pleasant.
The morning was pleasant.
The day was calm.
The afternoon was warm.
The day was pleasant.
The wind eased before midnight.
The temperature remained steady.
The late afternoon was cool.
The late afternoon was peaceful.
The early morning was warm.
The evening was warm.
The late afternoon was cloudy.
The evening was cloudy.
The drawer was packed with the battery.
The late afternoon was calm.
The morning was cool.
The late afternoon was bright.
A breeze arrived after noon.
The weekend was warm.
The early morning was calm.
The weekend was cool.
The day was bright.
The day was warm.
The afternoon was quiet.
The evening was peaceful.
The afternoon was pleasant.
The weather was mild.
The evening was quiet.
The morning was calm.
The morning was cloudy.
The afternoon was cloudy.
The night was peaceful.
The night was cool.
The day was cool.
The morning was warm.
Time passed.
Shadows grew longer by evening.
What was stored in the drawer?
Answer:
```

| 候选完整串 | token IDs | 逐token条件log p | 完整总分 | 物品部分 | 句号部分 |
|---|---|---|---|---|---|
| ' battery.' | [11602, 13] | [-3.4971888065338135, -3.4062581062316895] | -6.9034 | -3.4972 | -3.4063 |
| ' magnet.' | [32197, 13] | [-14.082225799560547, -3.332655429840088] | -17.4149 | -14.0822 | -3.3327 |

### F23_main128_B：完整前缀

远目标=magnet；近处=None；e=190，目标物品token=[32197]；p=319，token=25；d=128。近处token位置=[]，IDs=[]。

```text
Record:
Clouds drifted slowly overhead.
The evening was cool.
The weekend was peaceful.
Rain continued until dawn.
The afternoon was peaceful.
The day was cloudy.
The night was pleasant.
The day was peaceful.
The late afternoon was pleasant.
The evening was calm.
The night was calm.
The morning was peaceful.
It rained.
The afternoon was bright.
The evening was bright.
Morning came.
The weekend was bright.
The early morning was peaceful.
The night was cloudy.
The late afternoon was warm.
The early morning was cloudy.
The weekend was pleasant.
The evening was pleasant.
The morning was pleasant.
The day was calm.
The afternoon was warm.
The day was pleasant.
The wind eased before midnight.
The temperature remained steady.
The late afternoon was cool.
The late afternoon was peaceful.
The early morning was warm.
The evening was warm.
The late afternoon was cloudy.
The evening was cloudy.
The drawer was packed with the magnet.
The late afternoon was calm.
The morning was cool.
The late afternoon was bright.
A breeze arrived after noon.
The weekend was warm.
The early morning was calm.
The weekend was cool.
The day was bright.
The day was warm.
The afternoon was quiet.
The evening was peaceful.
The afternoon was pleasant.
The weather was mild.
The evening was quiet.
The morning was calm.
The morning was cloudy.
The afternoon was cloudy.
The night was peaceful.
The night was cool.
The day was cool.
The morning was warm.
Time passed.
Shadows grew longer by evening.
What was stored in the drawer?
Answer:
```

| 候选完整串 | token IDs | 逐token条件log p | 完整总分 | 物品部分 | 句号部分 |
|---|---|---|---|---|---|
| ' battery.' | [11602, 13] | [-11.176600456237793, -3.1233510971069336] | -14.3000 | -11.1766 | -3.1234 |
| ' magnet.' | [32197, 13] | [-4.6110758781433105, -3.916844367980957] | -8.5279 | -4.6111 | -3.9168 |

### F23_nearN_A：完整前缀

远目标=battery；近处=object；e=190，目标物品token=[11602]；p=319，token=25；d=128。近处token位置=[309]，IDs=[1633]。

```text
Record:
Shadows grew longer by evening.
Clouds drifted slowly overhead.
The evening was cool.
The weekend was peaceful.
Rain continued until dawn.
The afternoon was peaceful.
The day was cloudy.
The night was pleasant.
The day was peaceful.
The late afternoon was pleasant.
The evening was calm.
The night was calm.
The morning was peaceful.
It rained.
The afternoon was bright.
The evening was bright.
The weekend was bright.
The early morning was peaceful.
The night was cloudy.
The late afternoon was warm.
The early morning was cloudy.
The weekend was pleasant.
The evening was pleasant.
The morning was pleasant.
The day was calm.
The afternoon was warm.
The day was pleasant.
The wind eased before midnight.
The temperature remained steady.
The late afternoon was cool.
The late afternoon was peaceful.
The early morning was warm.
The late afternoon was cloudy.
The early morning was bright.
The drawer was packed with the battery.
The late afternoon was calm.
The morning was cool.
The late afternoon was bright.
A breeze arrived after noon.
The weekend was warm.
The early morning was calm.
The weekend was cool.
The day was bright.
The day was warm.
The afternoon was quiet.
The evening was peaceful.
The afternoon was pleasant.
The weather was mild.
The evening was quiet.
The morning was calm.
The morning was cloudy.
The afternoon was cloudy.
The night was peaceful.
The night was cool.
The day was cool.
The morning was warm.
Time passed.
The other container holds the object.
What was stored in the drawer?
Answer:
```

| 候选完整串 | token IDs | 逐token条件log p | 完整总分 | 物品部分 | 句号部分 |
|---|---|---|---|---|---|
| ' battery.' | [11602, 13] | [-5.910952568054199, -3.145709753036499] | -9.0567 | -5.9110 | -3.1457 |
| ' magnet.' | [32197, 13] | [-13.688517570495605, -3.208468437194824] | -16.8970 | -13.6885 | -3.2085 |

### F23_nearN_B：完整前缀

远目标=magnet；近处=object；e=190，目标物品token=[32197]；p=319，token=25；d=128。近处token位置=[309]，IDs=[1633]。

```text
Record:
Shadows grew longer by evening.
Clouds drifted slowly overhead.
The evening was cool.
The weekend was peaceful.
Rain continued until dawn.
The afternoon was peaceful.
The day was cloudy.
The night was pleasant.
The day was peaceful.
The late afternoon was pleasant.
The evening was calm.
The night was calm.
The morning was peaceful.
It rained.
The afternoon was bright.
The evening was bright.
The weekend was bright.
The early morning was peaceful.
The night was cloudy.
The late afternoon was warm.
The early morning was cloudy.
The weekend was pleasant.
The evening was pleasant.
The morning was pleasant.
The day was calm.
The afternoon was warm.
The day was pleasant.
The wind eased before midnight.
The temperature remained steady.
The late afternoon was cool.
The late afternoon was peaceful.
The early morning was warm.
The late afternoon was cloudy.
The early morning was bright.
The drawer was packed with the magnet.
The late afternoon was calm.
The morning was cool.
The late afternoon was bright.
A breeze arrived after noon.
The weekend was warm.
The early morning was calm.
The weekend was cool.
The day was bright.
The day was warm.
The afternoon was quiet.
The evening was peaceful.
The afternoon was pleasant.
The weather was mild.
The evening was quiet.
The morning was calm.
The morning was cloudy.
The afternoon was cloudy.
The night was peaceful.
The night was cool.
The day was cool.
The morning was warm.
Time passed.
The other container holds the object.
What was stored in the drawer?
Answer:
```

| 候选完整串 | token IDs | 逐token条件log p | 完整总分 | 物品部分 | 句号部分 |
|---|---|---|---|---|---|
| ' battery.' | [11602, 13] | [-11.887373924255371, -3.0318431854248047] | -14.9192 | -11.8874 | -3.0318 |
| ' magnet.' | [32197, 13] | [-6.749786376953125, -3.6207516193389893] | -10.3705 | -6.7498 | -3.6208 |

### F23_nearA_A：完整前缀

远目标=battery；近处=battery；e=190，目标物品token=[11602]；p=319，token=25；d=128。近处token位置=[309]，IDs=[11602]。

```text
Record:
Shadows grew longer by evening.
Clouds drifted slowly overhead.
The evening was cool.
The weekend was peaceful.
Rain continued until dawn.
The afternoon was peaceful.
The day was cloudy.
The night was pleasant.
The day was peaceful.
The late afternoon was pleasant.
The evening was calm.
The night was calm.
The morning was peaceful.
It rained.
The afternoon was bright.
The evening was bright.
The weekend was bright.
The early morning was peaceful.
The night was cloudy.
The late afternoon was warm.
The early morning was cloudy.
The weekend was pleasant.
The evening was pleasant.
The morning was pleasant.
The day was calm.
The afternoon was warm.
The day was pleasant.
The wind eased before midnight.
The temperature remained steady.
The late afternoon was cool.
The late afternoon was peaceful.
The early morning was warm.
The late afternoon was cloudy.
The early morning was bright.
The drawer was packed with the battery.
The late afternoon was calm.
The morning was cool.
The late afternoon was bright.
A breeze arrived after noon.
The weekend was warm.
The early morning was calm.
The weekend was cool.
The day was bright.
The day was warm.
The afternoon was quiet.
The evening was peaceful.
The afternoon was pleasant.
The weather was mild.
The evening was quiet.
The morning was calm.
The morning was cloudy.
The afternoon was cloudy.
The night was peaceful.
The night was cool.
The day was cool.
The morning was warm.
Time passed.
The other container holds the battery.
What was stored in the drawer?
Answer:
```

| 候选完整串 | token IDs | 逐token条件log p | 完整总分 | 物品部分 | 句号部分 |
|---|---|---|---|---|---|
| ' battery.' | [11602, 13] | [-4.872198581695557, -3.2090563774108887] | -8.0813 | -4.8722 | -3.2091 |
| ' magnet.' | [32197, 13] | [-14.262537002563477, -3.2923424243927] | -17.5549 | -14.2625 | -3.2923 |

### F23_nearA_B：完整前缀

远目标=magnet；近处=battery；e=190，目标物品token=[32197]；p=319，token=25；d=128。近处token位置=[309]，IDs=[11602]。

```text
Record:
Shadows grew longer by evening.
Clouds drifted slowly overhead.
The evening was cool.
The weekend was peaceful.
Rain continued until dawn.
The afternoon was peaceful.
The day was cloudy.
The night was pleasant.
The day was peaceful.
The late afternoon was pleasant.
The evening was calm.
The night was calm.
The morning was peaceful.
It rained.
The afternoon was bright.
The evening was bright.
The weekend was bright.
The early morning was peaceful.
The night was cloudy.
The late afternoon was warm.
The early morning was cloudy.
The weekend was pleasant.
The evening was pleasant.
The morning was pleasant.
The day was calm.
The afternoon was warm.
The day was pleasant.
The wind eased before midnight.
The temperature remained steady.
The late afternoon was cool.
The late afternoon was peaceful.
The early morning was warm.
The late afternoon was cloudy.
The early morning was bright.
The drawer was packed with the magnet.
The late afternoon was calm.
The morning was cool.
The late afternoon was bright.
A breeze arrived after noon.
The weekend was warm.
The early morning was calm.
The weekend was cool.
The day was bright.
The day was warm.
The afternoon was quiet.
The evening was peaceful.
The afternoon was pleasant.
The weather was mild.
The evening was quiet.
The morning was calm.
The morning was cloudy.
The afternoon was cloudy.
The night was peaceful.
The night was cool.
The day was cool.
The morning was warm.
Time passed.
The other container holds the battery.
What was stored in the drawer?
Answer:
```

| 候选完整串 | token IDs | 逐token条件log p | 完整总分 | 物品部分 | 句号部分 |
|---|---|---|---|---|---|
| ' battery.' | [11602, 13] | [-5.524581432342529, -3.312483072280884] | -8.8371 | -5.5246 | -3.3125 |
| ' magnet.' | [32197, 13] | [-5.988175868988037, -3.638223648071289] | -9.6264 | -5.9882 | -3.6382 |

### F23_nearB_A：完整前缀

远目标=battery；近处=magnet；e=190，目标物品token=[11602]；p=319，token=25；d=128。近处token位置=[309]，IDs=[32197]。

```text
Record:
Shadows grew longer by evening.
Clouds drifted slowly overhead.
The evening was cool.
The weekend was peaceful.
Rain continued until dawn.
The afternoon was peaceful.
The day was cloudy.
The night was pleasant.
The day was peaceful.
The late afternoon was pleasant.
The evening was calm.
The night was calm.
The morning was peaceful.
It rained.
The afternoon was bright.
The evening was bright.
The weekend was bright.
The early morning was peaceful.
The night was cloudy.
The late afternoon was warm.
The early morning was cloudy.
The weekend was pleasant.
The evening was pleasant.
The morning was pleasant.
The day was calm.
The afternoon was warm.
The day was pleasant.
The wind eased before midnight.
The temperature remained steady.
The late afternoon was cool.
The late afternoon was peaceful.
The early morning was warm.
The late afternoon was cloudy.
The early morning was bright.
The drawer was packed with the battery.
The late afternoon was calm.
The morning was cool.
The late afternoon was bright.
A breeze arrived after noon.
The weekend was warm.
The early morning was calm.
The weekend was cool.
The day was bright.
The day was warm.
The afternoon was quiet.
The evening was peaceful.
The afternoon was pleasant.
The weather was mild.
The evening was quiet.
The morning was calm.
The morning was cloudy.
The afternoon was cloudy.
The night was peaceful.
The night was cool.
The day was cool.
The morning was warm.
Time passed.
The other container holds the magnet.
What was stored in the drawer?
Answer:
```

| 候选完整串 | token IDs | 逐token条件log p | 完整总分 | 物品部分 | 句号部分 |
|---|---|---|---|---|---|
| ' battery.' | [11602, 13] | [-5.169370174407959, -3.021688222885132] | -8.1911 | -5.1694 | -3.0217 |
| ' magnet.' | [32197, 13] | [-6.401475429534912, -3.712458848953247] | -10.1139 | -6.4015 | -3.7125 |

### F23_nearB_B：完整前缀

远目标=magnet；近处=magnet；e=190，目标物品token=[32197]；p=319，token=25；d=128。近处token位置=[309]，IDs=[32197]。

```text
Record:
Shadows grew longer by evening.
Clouds drifted slowly overhead.
The evening was cool.
The weekend was peaceful.
Rain continued until dawn.
The afternoon was peaceful.
The day was cloudy.
The night was pleasant.
The day was peaceful.
The late afternoon was pleasant.
The evening was calm.
The night was calm.
The morning was peaceful.
It rained.
The afternoon was bright.
The evening was bright.
The weekend was bright.
The early morning was peaceful.
The night was cloudy.
The late afternoon was warm.
The early morning was cloudy.
The weekend was pleasant.
The evening was pleasant.
The morning was pleasant.
The day was calm.
The afternoon was warm.
The day was pleasant.
The wind eased before midnight.
The temperature remained steady.
The late afternoon was cool.
The late afternoon was peaceful.
The early morning was warm.
The late afternoon was cloudy.
The early morning was bright.
The drawer was packed with the magnet.
The late afternoon was calm.
The morning was cool.
The late afternoon was bright.
A breeze arrived after noon.
The weekend was warm.
The early morning was calm.
The weekend was cool.
The day was bright.
The day was warm.
The afternoon was quiet.
The evening was peaceful.
The afternoon was pleasant.
The weather was mild.
The evening was quiet.
The morning was calm.
The morning was cloudy.
The afternoon was cloudy.
The night was peaceful.
The night was cool.
The day was cool.
The morning was warm.
Time passed.
The other container holds the magnet.
What was stored in the drawer?
Answer:
```

| 候选完整串 | token IDs | 逐token条件log p | 完整总分 | 物品部分 | 句号部分 |
|---|---|---|---|---|---|
| ' battery.' | [11602, 13] | [-11.978447914123535, -3.028557300567627] | -15.0070 | -11.9784 | -3.0286 |
| ' magnet.' | [32197, 13] | [-5.979914665222168, -3.5310542583465576] | -9.5110 | -5.9799 | -3.5311 |

## F11

### ATTN_SAE：同一固定六成员

| 文本ID | #2520 | #26235 | #29969 | #23899 | #772 | #2254 | 候选A总分 | 候选B总分 | 选择 | 正确分差 |
|---|---|---|---|---|---|---|---|---|---|---|
| F11_nearN_A | 3.2713 | 0.0000 | 4.4351 | 31.4199 | 0.0000 | 5.4415 | -9.7029 | -22.1632 | A | 12.4603 |
| F11_nearN_B | 3.8994 | 0.0000 | 4.8793 | 32.7232 | 2.3317 | 4.7535 | -15.0602 | -9.8625 | B | 5.1976 |
| F11_nearA_A | 3.2018 | 0.0000 | 4.7772 | 31.3638 | 0.0000 | 5.0733 | -8.7023 | -22.6589 | A | 13.9565 |
| F11_nearA_B | 3.6679 | 0.0000 | 4.9890 | 32.3069 | 0.0000 | 4.3583 | -9.5642 | -9.2130 | B | 0.3512 |
| F11_nearB_A | 3.2498 | 0.0000 | 4.7348 | 32.7514 | 0.0000 | 4.5115 | -9.5902 | -11.1460 | A | 1.5558 |
| F11_nearB_B | 4.3984 | 2.4084 | 5.3867 | 33.2499 | 0.0000 | 3.9098 | -15.5685 | -7.4860 | B | 8.0825 |

同一族的相对强弱分解：T投影=0.1747，近词N投影=0.1133，相反条件保留=0.0614；模式损失=0.9386，行为分差损失=7.8755 nat；严格支持=False。T−N为恒等式，不是额外发现。

### MLPIN_SAE：同一固定六成员

| 文本ID | #17390 | #25508 | #3011 | #4700 | #16240 | #27076 | 候选A总分 | 候选B总分 | 选择 | 正确分差 |
|---|---|---|---|---|---|---|---|---|---|---|
| F11_nearN_A | 9.1101 | 3.9891 | 6.6458 | 9.1091 | 17.4400 | 11.8780 | -9.7029 | -22.1632 | A | 12.4603 |
| F11_nearN_B | 11.2399 | 4.0273 | 6.3489 | 7.9381 | 16.8370 | 12.6941 | -15.0602 | -9.8625 | B | 5.1976 |
| F11_nearA_A | 9.1948 | 4.0478 | 6.4237 | 8.3864 | 16.9223 | 11.8100 | -8.7023 | -22.6589 | A | 13.9565 |
| F11_nearA_B | 12.8130 | 3.9408 | 5.9882 | 7.4854 | 16.0403 | 13.3676 | -9.5642 | -9.2130 | B | 0.3512 |
| F11_nearB_A | 12.7828 | 4.1878 | 5.8300 | 7.6972 | 15.5832 | 13.3302 | -9.5902 | -11.1460 | A | 1.5558 |
| F11_nearB_B | 12.5975 | 4.3464 | 6.0480 | 6.5696 | 16.3104 | 13.1536 | -15.5685 | -7.4860 | B | 8.0825 |

同一族的相对强弱分解：T投影=0.7565，近词N投影=0.7799，相反条件保留=-0.0234；模式损失=1.0234，行为分差损失=7.8755 nat；严格支持=True。T−N为恒等式，不是额外发现。

### F11_nearN_A：完整前缀

远目标=ball；近处=object；e=190，目标物品token=[4935]；p=319，token=25；d=128。近处token位置=[310]，IDs=[1633]。

```text
Record:
The evening was quiet.
The night was cool.
The temperature remained steady.
A breeze arrived after noon.
The morning was calm.
The weekend was pleasant.
The evening was peaceful.
Morning came.
The sky became clearer later.
The day was cool.
Rain continued until dawn.
The early morning was cloudy.
The weekend was calm.
The evening was pleasant.
The day was calm.
The morning was peaceful.
The morning was warm.
The afternoon was bright.
The late afternoon was bright.
The afternoon was quiet.
The evening was warm.
The afternoon was calm.
The weekend was quiet.
The night was cloudy.
The morning was cloudy.
The night was calm.
The afternoon was warm.
The afternoon was pleasant.
The afternoon was cloudy.
The day was quiet.
The evening was cloudy.
The evening was cool.
The night was bright.
The day was cloudy.
The weekend was cloudy.
The weekend was warm.
Inside the cabinet there is the ball.
The early morning was quiet.
The late afternoon was quiet.
The day was bright.
The late afternoon was cloudy.
The morning was pleasant.
The weekend was cool.
The night was peaceful.
The night was warm.
The day was peaceful.
The morning was quiet.
The morning was bright.
The late afternoon was peaceful.
The wind eased before midnight.
The night was quiet.
It rained.
The weekend was peaceful.
The weekend was bright.
The early morning was peaceful.
The evening was calm.
The day was warm.
The day was pleasant.
Time passed.
The other container holds the object.
What does the cabinet contain?
Answer:
```

| 候选完整串 | token IDs | 逐token条件log p | 完整总分 | 物品部分 | 句号部分 |
|---|---|---|---|---|---|
| ' ball.' | [4935, 13] | [-6.503037929534912, -3.199855327606201] | -9.7029 | -6.5030 | -3.1999 |
| ' die.' | [2746, 13] | [-15.311168670654297, -6.8520307540893555] | -22.1632 | -15.3112 | -6.8520 |

### F11_nearN_B：完整前缀

远目标=die；近处=object；e=190，目标物品token=[2746]；p=319，token=25；d=128。近处token位置=[310]，IDs=[1633]。

```text
Record:
The evening was quiet.
The night was cool.
The temperature remained steady.
A breeze arrived after noon.
The morning was calm.
The weekend was pleasant.
The evening was peaceful.
Morning came.
The sky became clearer later.
The day was cool.
Rain continued until dawn.
The early morning was cloudy.
The weekend was calm.
The evening was pleasant.
The day was calm.
The morning was peaceful.
The morning was warm.
The afternoon was bright.
The late afternoon was bright.
The afternoon was quiet.
The evening was warm.
The afternoon was calm.
The weekend was quiet.
The night was cloudy.
The morning was cloudy.
The night was calm.
The afternoon was warm.
The afternoon was pleasant.
The afternoon was cloudy.
The day was quiet.
The evening was cloudy.
The evening was cool.
The night was bright.
The day was cloudy.
The weekend was cloudy.
The weekend was warm.
Inside the cabinet there is the die.
The early morning was quiet.
The late afternoon was quiet.
The day was bright.
The late afternoon was cloudy.
The morning was pleasant.
The weekend was cool.
The night was peaceful.
The night was warm.
The day was peaceful.
The morning was quiet.
The morning was bright.
The late afternoon was peaceful.
The wind eased before midnight.
The night was quiet.
It rained.
The weekend was peaceful.
The weekend was bright.
The early morning was peaceful.
The evening was calm.
The day was warm.
The day was pleasant.
Time passed.
The other container holds the object.
What does the cabinet contain?
Answer:
```

| 候选完整串 | token IDs | 逐token条件log p | 完整总分 | 物品部分 | 句号部分 |
|---|---|---|---|---|---|
| ' ball.' | [4935, 13] | [-11.630843162536621, -3.4293181896209717] | -15.0602 | -11.6308 | -3.4293 |
| ' die.' | [2746, 13] | [-6.900662899017334, -2.961884021759033] | -9.8625 | -6.9007 | -2.9619 |

### F11_nearA_A：完整前缀

远目标=ball；近处=ball；e=190，目标物品token=[4935]；p=319，token=25；d=128。近处token位置=[310]，IDs=[4935]。

```text
Record:
The evening was quiet.
The night was cool.
The temperature remained steady.
A breeze arrived after noon.
The morning was calm.
The weekend was pleasant.
The evening was peaceful.
Morning came.
The sky became clearer later.
The day was cool.
Rain continued until dawn.
The early morning was cloudy.
The weekend was calm.
The evening was pleasant.
The day was calm.
The morning was peaceful.
The morning was warm.
The afternoon was bright.
The late afternoon was bright.
The afternoon was quiet.
The evening was warm.
The afternoon was calm.
The weekend was quiet.
The night was cloudy.
The morning was cloudy.
The night was calm.
The afternoon was warm.
The afternoon was pleasant.
The afternoon was cloudy.
The day was quiet.
The evening was cloudy.
The evening was cool.
The night was bright.
The day was cloudy.
The weekend was cloudy.
The weekend was warm.
Inside the cabinet there is the ball.
The early morning was quiet.
The late afternoon was quiet.
The day was bright.
The late afternoon was cloudy.
The morning was pleasant.
The weekend was cool.
The night was peaceful.
The night was warm.
The day was peaceful.
The morning was quiet.
The morning was bright.
The late afternoon was peaceful.
The wind eased before midnight.
The night was quiet.
It rained.
The weekend was peaceful.
The weekend was bright.
The early morning was peaceful.
The evening was calm.
The day was warm.
The day was pleasant.
Time passed.
The other container holds the ball.
What does the cabinet contain?
Answer:
```

| 候选完整串 | token IDs | 逐token条件log p | 完整总分 | 物品部分 | 句号部分 |
|---|---|---|---|---|---|
| ' ball.' | [4935, 13] | [-5.666378021240234, -3.0359270572662354] | -8.7023 | -5.6664 | -3.0359 |
| ' die.' | [2746, 13] | [-15.601316452026367, -7.057534217834473] | -22.6589 | -15.6013 | -7.0575 |

### F11_nearA_B：完整前缀

远目标=die；近处=ball；e=190，目标物品token=[2746]；p=319，token=25；d=128。近处token位置=[310]，IDs=[4935]。

```text
Record:
The evening was quiet.
The night was cool.
The temperature remained steady.
A breeze arrived after noon.
The morning was calm.
The weekend was pleasant.
The evening was peaceful.
Morning came.
The sky became clearer later.
The day was cool.
Rain continued until dawn.
The early morning was cloudy.
The weekend was calm.
The evening was pleasant.
The day was calm.
The morning was peaceful.
The morning was warm.
The afternoon was bright.
The late afternoon was bright.
The afternoon was quiet.
The evening was warm.
The afternoon was calm.
The weekend was quiet.
The night was cloudy.
The morning was cloudy.
The night was calm.
The afternoon was warm.
The afternoon was pleasant.
The afternoon was cloudy.
The day was quiet.
The evening was cloudy.
The evening was cool.
The night was bright.
The day was cloudy.
The weekend was cloudy.
The weekend was warm.
Inside the cabinet there is the die.
The early morning was quiet.
The late afternoon was quiet.
The day was bright.
The late afternoon was cloudy.
The morning was pleasant.
The weekend was cool.
The night was peaceful.
The night was warm.
The day was peaceful.
The morning was quiet.
The morning was bright.
The late afternoon was peaceful.
The wind eased before midnight.
The night was quiet.
It rained.
The weekend was peaceful.
The weekend was bright.
The early morning was peaceful.
The evening was calm.
The day was warm.
The day was pleasant.
Time passed.
The other container holds the ball.
What does the cabinet contain?
Answer:
```

| 候选完整串 | token IDs | 逐token条件log p | 完整总分 | 物品部分 | 句号部分 |
|---|---|---|---|---|---|
| ' ball.' | [4935, 13] | [-6.479274272918701, -3.0848875045776367] | -9.5642 | -6.4793 | -3.0849 |
| ' die.' | [2746, 13] | [-6.3107123374938965, -2.9022951126098633] | -9.2130 | -6.3107 | -2.9023 |

### F11_nearB_A：完整前缀

远目标=ball；近处=die；e=190，目标物品token=[4935]；p=319，token=25；d=128。近处token位置=[310]，IDs=[2746]。

```text
Record:
The evening was quiet.
The night was cool.
The temperature remained steady.
A breeze arrived after noon.
The morning was calm.
The weekend was pleasant.
The evening was peaceful.
Morning came.
The sky became clearer later.
The day was cool.
Rain continued until dawn.
The early morning was cloudy.
The weekend was calm.
The evening was pleasant.
The day was calm.
The morning was peaceful.
The morning was warm.
The afternoon was bright.
The late afternoon was bright.
The afternoon was quiet.
The evening was warm.
The afternoon was calm.
The weekend was quiet.
The night was cloudy.
The morning was cloudy.
The night was calm.
The afternoon was warm.
The afternoon was pleasant.
The afternoon was cloudy.
The day was quiet.
The evening was cloudy.
The evening was cool.
The night was bright.
The day was cloudy.
The weekend was cloudy.
The weekend was warm.
Inside the cabinet there is the ball.
The early morning was quiet.
The late afternoon was quiet.
The day was bright.
The late afternoon was cloudy.
The morning was pleasant.
The weekend was cool.
The night was peaceful.
The night was warm.
The day was peaceful.
The morning was quiet.
The morning was bright.
The late afternoon was peaceful.
The wind eased before midnight.
The night was quiet.
It rained.
The weekend was peaceful.
The weekend was bright.
The early morning was peaceful.
The evening was calm.
The day was warm.
The day was pleasant.
Time passed.
The other container holds the die.
What does the cabinet contain?
Answer:
```

| 候选完整串 | token IDs | 逐token条件log p | 完整总分 | 物品部分 | 句号部分 |
|---|---|---|---|---|---|
| ' ball.' | [4935, 13] | [-6.506233215332031, -3.0839953422546387] | -9.5902 | -6.5062 | -3.0840 |
| ' die.' | [2746, 13] | [-8.011829376220703, -3.1341638565063477] | -11.1460 | -8.0118 | -3.1342 |

### F11_nearB_B：完整前缀

远目标=die；近处=die；e=190，目标物品token=[2746]；p=319，token=25；d=128。近处token位置=[310]，IDs=[2746]。

```text
Record:
The evening was quiet.
The night was cool.
The temperature remained steady.
A breeze arrived after noon.
The morning was calm.
The weekend was pleasant.
The evening was peaceful.
Morning came.
The sky became clearer later.
The day was cool.
Rain continued until dawn.
The early morning was cloudy.
The weekend was calm.
The evening was pleasant.
The day was calm.
The morning was peaceful.
The morning was warm.
The afternoon was bright.
The late afternoon was bright.
The afternoon was quiet.
The evening was warm.
The afternoon was calm.
The weekend was quiet.
The night was cloudy.
The morning was cloudy.
The night was calm.
The afternoon was warm.
The afternoon was pleasant.
The afternoon was cloudy.
The day was quiet.
The evening was cloudy.
The evening was cool.
The night was bright.
The day was cloudy.
The weekend was cloudy.
The weekend was warm.
Inside the cabinet there is the die.
The early morning was quiet.
The late afternoon was quiet.
The day was bright.
The late afternoon was cloudy.
The morning was pleasant.
The weekend was cool.
The night was peaceful.
The night was warm.
The day was peaceful.
The morning was quiet.
The morning was bright.
The late afternoon was peaceful.
The wind eased before midnight.
The night was quiet.
It rained.
The weekend was peaceful.
The weekend was bright.
The early morning was peaceful.
The evening was calm.
The day was warm.
The day was pleasant.
Time passed.
The other container holds the die.
What does the cabinet contain?
Answer:
```

| 候选完整串 | token IDs | 逐token条件log p | 完整总分 | 物品部分 | 句号部分 |
|---|---|---|---|---|---|
| ' ball.' | [4935, 13] | [-12.210862159729004, -3.3576653003692627] | -15.5685 | -12.2109 | -3.3577 |
| ' die.' | [2746, 13] | [-4.689885139465332, -2.7961626052856445] | -7.4860 | -4.6899 | -2.7962 |

## F27

### ATTN_SAE：同一固定六成员

| 文本ID | #2520 | #26235 | #29969 | #23899 | #772 | #2254 | 候选A总分 | 候选B总分 | 选择 | 正确分差 |
|---|---|---|---|---|---|---|---|---|---|---|
| F27_nearN_A | 0.0000 | 4.8640 | 2.8736 | 31.7893 | 2.7887 | 3.0693 | -9.0299 | -14.9900 | A | 5.9601 |
| F27_nearN_B | 0.0000 | 5.0892 | 2.4527 | 32.3656 | 2.8060 | 3.1055 | -13.6644 | -12.8376 | B | 0.8268 |
| F27_nearA_A | 0.0000 | 5.9699 | 3.1761 | 30.8049 | 0.0000 | 0.0000 | -8.5870 | -14.8622 | A | 6.2752 |
| F27_nearA_B | 0.0000 | 6.3046 | 2.6012 | 31.1582 | 0.0000 | 0.0000 | -10.7712 | -10.9989 | A | -0.2278 |
| F27_nearB_A | 0.0000 | 6.2090 | 2.6799 | 30.9637 | 0.0000 | 0.0000 | -7.5109 | -11.5111 | A | 4.0002 |
| F27_nearB_B | 0.0000 | 6.2382 | 2.6336 | 31.3349 | 0.0000 | 2.7502 | -14.5727 | -11.8097 | B | 2.7630 |

同一族的相对强弱分解：T投影=0.6562，近词N投影=0.4305，相反条件保留=0.2257；模式损失=0.7743，行为分差损失=1.5072 nat；严格支持=False。T−N为恒等式，不是额外发现。

### MLPIN_SAE：同一固定六成员

| 文本ID | #17390 | #25508 | #3011 | #4700 | #16240 | #27076 | 候选A总分 | 候选B总分 | 选择 | 正确分差 |
|---|---|---|---|---|---|---|---|---|---|---|
| F27_nearN_A | 11.7646 | 5.0951 | 4.7170 | 6.5541 | 14.1218 | 11.5452 | -9.0299 | -14.9900 | A | 5.9601 |
| F27_nearN_B | 13.1399 | 4.9556 | 4.1803 | 7.0901 | 13.6896 | 10.9227 | -13.6644 | -12.8376 | B | 0.8268 |
| F27_nearA_A | 11.9135 | 5.7524 | 5.5497 | 5.4627 | 16.7265 | 9.7001 | -8.5870 | -14.8622 | A | 6.2752 |
| F27_nearA_B | 13.2948 | 5.6013 | 5.6690 | 5.9269 | 17.3833 | 7.9832 | -10.7712 | -10.9989 | A | -0.2278 |
| F27_nearB_A | 12.9692 | 5.5308 | 6.0979 | 5.3610 | 17.9466 | 8.6845 | -7.5109 | -11.5111 | A | 4.0002 |
| F27_nearB_B | 13.5956 | 5.6911 | 5.0259 | 6.2142 | 16.4648 | 8.7953 | -14.5727 | -11.8097 | B | 2.7630 |

同一族的相对强弱分解：T投影=0.8376，近词N投影=0.3068，相反条件保留=0.5307；模式损失=0.4693，行为分差损失=1.5072 nat；严格支持=True。T−N为恒等式，不是额外发现。

### F27_nearN_A：完整前缀

远目标=map；近处=object；e=190，目标物品token=[2415]；p=319，token=25；d=128。近处token位置=[309]，IDs=[1633]。

```text
Record:
Morning came.
The late afternoon was warm.
The weekend was peaceful.
The evening was warm.
The day was cloudy.
The morning was cloudy.
The night was cloudy.
The late afternoon was cloudy.
The morning was bright.
The early morning was quiet.
The night was quiet.
The night was peaceful.
Rain continued until dawn.
The morning was cool.
The wind eased before midnight.
The afternoon was peaceful.
The early morning was peaceful.
The morning was calm.
The evening was pleasant.
The sky became clearer later.
The afternoon was calm.
The day was cool.
A breeze arrived after noon.
The day was warm.
The evening was quiet.
The evening was cloudy.
The late afternoon was cool.
The early morning was cool.
The late afternoon was peaceful.
The weekend was quiet.
The night was cool.
The weekend was calm.
The early morning was calm.
The day was peaceful.
According to the note, the cabinet holds the map.
The late afternoon was quiet.
The afternoon was bright.
The day was bright.
The night was calm.
The early morning was bright.
The evening was peaceful.
Sunlight faded near sunset.
The weekend was cloudy.
The morning was pleasant.
The late afternoon was pleasant.
The afternoon was pleasant.
The day was pleasant.
The night was bright.
The afternoon was warm.
The temperature remained steady.
The day was calm.
The early morning was warm.
The early morning was pleasant.
The night was warm.
The late afternoon was bright.
The weather was mild.
The other container holds the object.
Which item is in the cabinet?
Answer:
```

| 候选完整串 | token IDs | 逐token条件log p | 完整总分 | 物品部分 | 句号部分 |
|---|---|---|---|---|---|
| ' map.' | [2415, 13] | [-5.55317497253418, -3.4766998291015625] | -9.0299 | -5.5532 | -3.4767 |
| ' chart.' | [9487, 13] | [-11.409486770629883, -3.580519199371338] | -14.9900 | -11.4095 | -3.5805 |

### F27_nearN_B：完整前缀

远目标=chart；近处=object；e=190，目标物品token=[9487]；p=319，token=25；d=128。近处token位置=[309]，IDs=[1633]。

```text
Record:
Morning came.
The late afternoon was warm.
The weekend was peaceful.
The evening was warm.
The day was cloudy.
The morning was cloudy.
The night was cloudy.
The late afternoon was cloudy.
The morning was bright.
The early morning was quiet.
The night was quiet.
The night was peaceful.
Rain continued until dawn.
The morning was cool.
The wind eased before midnight.
The afternoon was peaceful.
The early morning was peaceful.
The morning was calm.
The evening was pleasant.
The sky became clearer later.
The afternoon was calm.
The day was cool.
A breeze arrived after noon.
The day was warm.
The evening was quiet.
The evening was cloudy.
The late afternoon was cool.
The early morning was cool.
The late afternoon was peaceful.
The weekend was quiet.
The night was cool.
The weekend was calm.
The early morning was calm.
The day was peaceful.
According to the note, the cabinet holds the chart.
The late afternoon was quiet.
The afternoon was bright.
The day was bright.
The night was calm.
The early morning was bright.
The evening was peaceful.
Sunlight faded near sunset.
The weekend was cloudy.
The morning was pleasant.
The late afternoon was pleasant.
The afternoon was pleasant.
The day was pleasant.
The night was bright.
The afternoon was warm.
The temperature remained steady.
The day was calm.
The early morning was warm.
The early morning was pleasant.
The night was warm.
The late afternoon was bright.
The weather was mild.
The other container holds the object.
Which item is in the cabinet?
Answer:
```

| 候选完整串 | token IDs | 逐token条件log p | 完整总分 | 物品部分 | 句号部分 |
|---|---|---|---|---|---|
| ' map.' | [2415, 13] | [-9.7147855758667, -3.9496302604675293] | -13.6644 | -9.7148 | -3.9496 |
| ' chart.' | [9487, 13] | [-9.331740379333496, -3.5058953762054443] | -12.8376 | -9.3317 | -3.5059 |

### F27_nearA_A：完整前缀

远目标=map；近处=map；e=190，目标物品token=[2415]；p=319，token=25；d=128。近处token位置=[309]，IDs=[2415]。

```text
Record:
Morning came.
The late afternoon was warm.
The weekend was peaceful.
The evening was warm.
The day was cloudy.
The morning was cloudy.
The night was cloudy.
The late afternoon was cloudy.
The morning was bright.
The early morning was quiet.
The night was quiet.
The night was peaceful.
Rain continued until dawn.
The morning was cool.
The wind eased before midnight.
The afternoon was peaceful.
The early morning was peaceful.
The morning was calm.
The evening was pleasant.
The sky became clearer later.
The afternoon was calm.
The day was cool.
A breeze arrived after noon.
The day was warm.
The evening was quiet.
The evening was cloudy.
The late afternoon was cool.
The early morning was cool.
The late afternoon was peaceful.
The weekend was quiet.
The night was cool.
The weekend was calm.
The early morning was calm.
The day was peaceful.
According to the note, the cabinet holds the map.
The late afternoon was quiet.
The afternoon was bright.
The day was bright.
The night was calm.
The early morning was bright.
The evening was peaceful.
Sunlight faded near sunset.
The weekend was cloudy.
The morning was pleasant.
The late afternoon was pleasant.
The afternoon was pleasant.
The day was pleasant.
The night was bright.
The afternoon was warm.
The temperature remained steady.
The day was calm.
The early morning was warm.
The early morning was pleasant.
The night was warm.
The late afternoon was bright.
The weather was mild.
The other container holds the map.
Which item is in the cabinet?
Answer:
```

| 候选完整串 | token IDs | 逐token条件log p | 完整总分 | 物品部分 | 句号部分 |
|---|---|---|---|---|---|
| ' map.' | [2415, 13] | [-5.3139824867248535, -3.272998809814453] | -8.5870 | -5.3140 | -3.2730 |
| ' chart.' | [9487, 13] | [-11.18578052520752, -3.6763904094696045] | -14.8622 | -11.1858 | -3.6764 |

### F27_nearA_B：完整前缀

远目标=chart；近处=map；e=190，目标物品token=[9487]；p=319，token=25；d=128。近处token位置=[309]，IDs=[2415]。

```text
Record:
Morning came.
The late afternoon was warm.
The weekend was peaceful.
The evening was warm.
The day was cloudy.
The morning was cloudy.
The night was cloudy.
The late afternoon was cloudy.
The morning was bright.
The early morning was quiet.
The night was quiet.
The night was peaceful.
Rain continued until dawn.
The morning was cool.
The wind eased before midnight.
The afternoon was peaceful.
The early morning was peaceful.
The morning was calm.
The evening was pleasant.
The sky became clearer later.
The afternoon was calm.
The day was cool.
A breeze arrived after noon.
The day was warm.
The evening was quiet.
The evening was cloudy.
The late afternoon was cool.
The early morning was cool.
The late afternoon was peaceful.
The weekend was quiet.
The night was cool.
The weekend was calm.
The early morning was calm.
The day was peaceful.
According to the note, the cabinet holds the chart.
The late afternoon was quiet.
The afternoon was bright.
The day was bright.
The night was calm.
The early morning was bright.
The evening was peaceful.
Sunlight faded near sunset.
The weekend was cloudy.
The morning was pleasant.
The late afternoon was pleasant.
The afternoon was pleasant.
The day was pleasant.
The night was bright.
The afternoon was warm.
The temperature remained steady.
The day was calm.
The early morning was warm.
The early morning was pleasant.
The night was warm.
The late afternoon was bright.
The weather was mild.
The other container holds the map.
Which item is in the cabinet?
Answer:
```

| 候选完整串 | token IDs | 逐token条件log p | 完整总分 | 物品部分 | 句号部分 |
|---|---|---|---|---|---|
| ' map.' | [2415, 13] | [-7.244075298309326, -3.5271100997924805] | -10.7712 | -7.2441 | -3.5271 |
| ' chart.' | [9487, 13] | [-7.554601192474365, -3.4443359375] | -10.9989 | -7.5546 | -3.4443 |

### F27_nearB_A：完整前缀

远目标=map；近处=chart；e=190，目标物品token=[2415]；p=319，token=25；d=128。近处token位置=[309]，IDs=[9487]。

```text
Record:
Morning came.
The late afternoon was warm.
The weekend was peaceful.
The evening was warm.
The day was cloudy.
The morning was cloudy.
The night was cloudy.
The late afternoon was cloudy.
The morning was bright.
The early morning was quiet.
The night was quiet.
The night was peaceful.
Rain continued until dawn.
The morning was cool.
The wind eased before midnight.
The afternoon was peaceful.
The early morning was peaceful.
The morning was calm.
The evening was pleasant.
The sky became clearer later.
The afternoon was calm.
The day was cool.
A breeze arrived after noon.
The day was warm.
The evening was quiet.
The evening was cloudy.
The late afternoon was cool.
The early morning was cool.
The late afternoon was peaceful.
The weekend was quiet.
The night was cool.
The weekend was calm.
The early morning was calm.
The day was peaceful.
According to the note, the cabinet holds the map.
The late afternoon was quiet.
The afternoon was bright.
The day was bright.
The night was calm.
The early morning was bright.
The evening was peaceful.
Sunlight faded near sunset.
The weekend was cloudy.
The morning was pleasant.
The late afternoon was pleasant.
The afternoon was pleasant.
The day was pleasant.
The night was bright.
The afternoon was warm.
The temperature remained steady.
The day was calm.
The early morning was warm.
The early morning was pleasant.
The night was warm.
The late afternoon was bright.
The weather was mild.
The other container holds the chart.
Which item is in the cabinet?
Answer:
```

| 候选完整串 | token IDs | 逐token条件log p | 完整总分 | 物品部分 | 句号部分 |
|---|---|---|---|---|---|
| ' map.' | [2415, 13] | [-4.190820217132568, -3.3200573921203613] | -7.5109 | -4.1908 | -3.3201 |
| ' chart.' | [9487, 13] | [-8.115190505981445, -3.3958985805511475] | -11.5111 | -8.1152 | -3.3959 |

### F27_nearB_B：完整前缀

远目标=chart；近处=chart；e=190，目标物品token=[9487]；p=319，token=25；d=128。近处token位置=[309]，IDs=[9487]。

```text
Record:
Morning came.
The late afternoon was warm.
The weekend was peaceful.
The evening was warm.
The day was cloudy.
The morning was cloudy.
The night was cloudy.
The late afternoon was cloudy.
The morning was bright.
The early morning was quiet.
The night was quiet.
The night was peaceful.
Rain continued until dawn.
The morning was cool.
The wind eased before midnight.
The afternoon was peaceful.
The early morning was peaceful.
The morning was calm.
The evening was pleasant.
The sky became clearer later.
The afternoon was calm.
The day was cool.
A breeze arrived after noon.
The day was warm.
The evening was quiet.
The evening was cloudy.
The late afternoon was cool.
The early morning was cool.
The late afternoon was peaceful.
The weekend was quiet.
The night was cool.
The weekend was calm.
The early morning was calm.
The day was peaceful.
According to the note, the cabinet holds the chart.
The late afternoon was quiet.
The afternoon was bright.
The day was bright.
The night was calm.
The early morning was bright.
The evening was peaceful.
Sunlight faded near sunset.
The weekend was cloudy.
The morning was pleasant.
The late afternoon was pleasant.
The afternoon was pleasant.
The day was pleasant.
The night was bright.
The afternoon was warm.
The temperature remained steady.
The day was calm.
The early morning was warm.
The early morning was pleasant.
The night was warm.
The late afternoon was bright.
The weather was mild.
The other container holds the chart.
Which item is in the cabinet?
Answer:
```

| 候选完整串 | token IDs | 逐token条件log p | 完整总分 | 物品部分 | 句号部分 |
|---|---|---|---|---|---|
| ' map.' | [2415, 13] | [-10.57643985748291, -3.9962902069091797] | -14.5727 | -10.5764 | -3.9963 |
| ' chart.' | [9487, 13] | [-8.454370498657227, -3.355334520339966] | -11.8097 | -8.4544 | -3.3553 |

## F28

### ATTN_SAE：同一固定六成员

| 文本ID | #2520 | #26235 | #29969 | #23899 | #772 | #2254 | 候选A总分 | 候选B总分 | 选择 | 正确分差 |
|---|---|---|---|---|---|---|---|---|---|---|
| F28_nearN_A | 2.3234 | 3.5476 | 3.1111 | 33.5943 | 3.3261 | 4.6796 | -10.8863 | -16.0583 | A | 5.1720 |
| F28_nearN_B | 2.3288 | 3.3954 | 3.3742 | 33.0060 | 3.5295 | 4.8159 | -13.1667 | -13.6286 | A | -0.4619 |
| F28_nearA_A | 2.7190 | 4.8828 | 3.8287 | 34.0942 | 3.1059 | 4.3520 | -10.0683 | -16.5984 | A | 6.5301 |
| F28_nearA_B | 2.4597 | 4.1760 | 3.7251 | 33.1679 | 3.2229 | 4.4584 | -10.0167 | -12.2010 | A | -2.1842 |
| F28_nearB_A | 2.5369 | 4.3338 | 3.6126 | 33.8125 | 3.1494 | 4.2551 | -9.8160 | -12.6715 | A | 2.8555 |
| F28_nearB_B | 2.7553 | 4.5131 | 4.0963 | 33.1778 | 3.3538 | 4.5290 | -13.5684 | -12.8829 | B | 0.6854 |

同一族的相对强弱分解：T投影=0.9947，近词N投影=0.2954，相反条件保留=0.6993；模式损失=0.3007，行为分差损失=2.0194 nat；严格支持=True。T−N为恒等式，不是额外发现。

### MLPIN_SAE：同一固定六成员

| 文本ID | #17390 | #25508 | #3011 | #4700 | #16240 | #27076 | 候选A总分 | 候选B总分 | 选择 | 正确分差 |
|---|---|---|---|---|---|---|---|---|---|---|
| F28_nearN_A | 9.2277 | 4.3687 | 4.7869 | 7.8010 | 11.7129 | 13.3315 | -10.8863 | -16.0583 | A | 5.1720 |
| F28_nearN_B | 8.5135 | 4.6298 | 5.0383 | 7.6392 | 12.2094 | 13.5042 | -13.1667 | -13.6286 | A | -0.4619 |
| F28_nearA_A | 9.3000 | 4.9740 | 5.5370 | 6.7809 | 13.7802 | 11.7477 | -10.0683 | -16.5984 | A | 6.5301 |
| F28_nearA_B | 9.9589 | 4.9805 | 6.0098 | 6.4157 | 15.4511 | 12.3344 | -10.0167 | -12.2010 | A | -2.1842 |
| F28_nearB_A | 10.0752 | 4.9261 | 5.7821 | 6.6346 | 14.2578 | 12.0299 | -9.8160 | -12.6715 | A | 2.8555 |
| F28_nearB_B | 8.2915 | 5.1813 | 5.6430 | 6.7270 | 14.0584 | 12.1647 | -13.5684 | -12.8829 | B | 0.6854 |

同一族的相对强弱分解：T投影=0.8977，近词N投影=0.1829，相反条件保留=0.7148；模式损失=0.2852，行为分差损失=2.0194 nat；严格支持=True。T−N为恒等式，不是额外发现。

### F28_nearN_A：完整前缀

远目标=card；近处=object；e=190，目标物品token=[3701]；p=319，token=25；d=128。近处token位置=[309]，IDs=[1633]。

```text
Record:
The late afternoon was peaceful.
The night was cloudy.
The wind eased before midnight.
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
The early morning was bright.
The early morning was calm.
The early morning was cloudy.
According to the note, the tin holds the card.
The weekend was peaceful.
The afternoon was cool.
The weekend was quiet.
The day was peaceful.
Time passed.
The night was warm.
The night was calm.
The late afternoon was cool.
The afternoon was warm.
The weekend was cloudy.
The afternoon was cloudy.
The late afternoon was bright.
It rained.
The afternoon was peaceful.
The late afternoon was cloudy.
The weekend was bright.
The weekend was calm.
The morning was quiet.
The day was cool.
The early morning was pleasant.
The night was quiet.
Clouds drifted slowly overhead.
The other container holds the object.
Which item is in the tin?
Answer:
```

| 候选完整串 | token IDs | 逐token条件log p | 完整总分 | 物品部分 | 句号部分 |
|---|---|---|---|---|---|
| ' card.' | [3701, 13] | [-7.075092315673828, -3.8112053871154785] | -10.8863 | -7.0751 | -3.8112 |
| ' stamp.' | [21206, 13] | [-12.566507339477539, -3.4917616844177246] | -16.0583 | -12.5665 | -3.4918 |

### F28_nearN_B：完整前缀

远目标=stamp；近处=object；e=190，目标物品token=[21206]；p=319，token=25；d=128。近处token位置=[309]，IDs=[1633]。

```text
Record:
The late afternoon was peaceful.
The night was cloudy.
The wind eased before midnight.
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
The early morning was bright.
The early morning was calm.
The early morning was cloudy.
According to the note, the tin holds the stamp.
The weekend was peaceful.
The afternoon was cool.
The weekend was quiet.
The day was peaceful.
Time passed.
The night was warm.
The night was calm.
The late afternoon was cool.
The afternoon was warm.
The weekend was cloudy.
The afternoon was cloudy.
The late afternoon was bright.
It rained.
The afternoon was peaceful.
The late afternoon was cloudy.
The weekend was bright.
The weekend was calm.
The morning was quiet.
The day was cool.
The early morning was pleasant.
The night was quiet.
Clouds drifted slowly overhead.
The other container holds the object.
Which item is in the tin?
Answer:
```

| 候选完整串 | token IDs | 逐token条件log p | 完整总分 | 物品部分 | 句号部分 |
|---|---|---|---|---|---|
| ' card.' | [3701, 13] | [-9.426471710205078, -3.7402396202087402] | -13.1667 | -9.4265 | -3.7402 |
| ' stamp.' | [21206, 13] | [-10.278364181518555, -3.350217342376709] | -13.6286 | -10.2784 | -3.3502 |

### F28_nearA_A：完整前缀

远目标=card；近处=card；e=190，目标物品token=[3701]；p=319，token=25；d=128。近处token位置=[309]，IDs=[3701]。

```text
Record:
The late afternoon was peaceful.
The night was cloudy.
The wind eased before midnight.
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
The early morning was bright.
The early morning was calm.
The early morning was cloudy.
According to the note, the tin holds the card.
The weekend was peaceful.
The afternoon was cool.
The weekend was quiet.
The day was peaceful.
Time passed.
The night was warm.
The night was calm.
The late afternoon was cool.
The afternoon was warm.
The weekend was cloudy.
The afternoon was cloudy.
The late afternoon was bright.
It rained.
The afternoon was peaceful.
The late afternoon was cloudy.
The weekend was bright.
The weekend was calm.
The morning was quiet.
The day was cool.
The early morning was pleasant.
The night was quiet.
Clouds drifted slowly overhead.
The other container holds the card.
Which item is in the tin?
Answer:
```

| 候选完整串 | token IDs | 逐token条件log p | 完整总分 | 物品部分 | 句号部分 |
|---|---|---|---|---|---|
| ' card.' | [3701, 13] | [-6.5304741859436035, -3.537849187850952] | -10.0683 | -6.5305 | -3.5378 |
| ' stamp.' | [21206, 13] | [-13.288743019104004, -3.3096845149993896] | -16.5984 | -13.2887 | -3.3097 |

### F28_nearA_B：完整前缀

远目标=stamp；近处=card；e=190，目标物品token=[21206]；p=319，token=25；d=128。近处token位置=[309]，IDs=[3701]。

```text
Record:
The late afternoon was peaceful.
The night was cloudy.
The wind eased before midnight.
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
The early morning was bright.
The early morning was calm.
The early morning was cloudy.
According to the note, the tin holds the stamp.
The weekend was peaceful.
The afternoon was cool.
The weekend was quiet.
The day was peaceful.
Time passed.
The night was warm.
The night was calm.
The late afternoon was cool.
The afternoon was warm.
The weekend was cloudy.
The afternoon was cloudy.
The late afternoon was bright.
It rained.
The afternoon was peaceful.
The late afternoon was cloudy.
The weekend was bright.
The weekend was calm.
The morning was quiet.
The day was cool.
The early morning was pleasant.
The night was quiet.
Clouds drifted slowly overhead.
The other container holds the card.
Which item is in the tin?
Answer:
```

| 候选完整串 | token IDs | 逐token条件log p | 完整总分 | 物品部分 | 句号部分 |
|---|---|---|---|---|---|
| ' card.' | [3701, 13] | [-6.188358783721924, -3.828369379043579] | -10.0167 | -6.1884 | -3.8284 |
| ' stamp.' | [21206, 13] | [-8.8204927444458, -3.3804821968078613] | -12.2010 | -8.8205 | -3.3805 |

### F28_nearB_A：完整前缀

远目标=card；近处=stamp；e=190，目标物品token=[3701]；p=319，token=25；d=128。近处token位置=[309]，IDs=[21206]。

```text
Record:
The late afternoon was peaceful.
The night was cloudy.
The wind eased before midnight.
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
The early morning was bright.
The early morning was calm.
The early morning was cloudy.
According to the note, the tin holds the card.
The weekend was peaceful.
The afternoon was cool.
The weekend was quiet.
The day was peaceful.
Time passed.
The night was warm.
The night was calm.
The late afternoon was cool.
The afternoon was warm.
The weekend was cloudy.
The afternoon was cloudy.
The late afternoon was bright.
It rained.
The afternoon was peaceful.
The late afternoon was cloudy.
The weekend was bright.
The weekend was calm.
The morning was quiet.
The day was cool.
The early morning was pleasant.
The night was quiet.
Clouds drifted slowly overhead.
The other container holds the stamp.
Which item is in the tin?
Answer:
```

| 候选完整串 | token IDs | 逐token条件log p | 完整总分 | 物品部分 | 句号部分 |
|---|---|---|---|---|---|
| ' card.' | [3701, 13] | [-6.12675142288208, -3.6892073154449463] | -9.8160 | -6.1268 | -3.6892 |
| ' stamp.' | [21206, 13] | [-9.173162460327148, -3.4983036518096924] | -12.6715 | -9.1732 | -3.4983 |

### F28_nearB_B：完整前缀

远目标=stamp；近处=stamp；e=190，目标物品token=[21206]；p=319，token=25；d=128。近处token位置=[309]，IDs=[21206]。

```text
Record:
The late afternoon was peaceful.
The night was cloudy.
The wind eased before midnight.
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
The early morning was bright.
The early morning was calm.
The early morning was cloudy.
According to the note, the tin holds the stamp.
The weekend was peaceful.
The afternoon was cool.
The weekend was quiet.
The day was peaceful.
Time passed.
The night was warm.
The night was calm.
The late afternoon was cool.
The afternoon was warm.
The weekend was cloudy.
The afternoon was cloudy.
The late afternoon was bright.
It rained.
The afternoon was peaceful.
The late afternoon was cloudy.
The weekend was bright.
The weekend was calm.
The morning was quiet.
The day was cool.
The early morning was pleasant.
The night was quiet.
Clouds drifted slowly overhead.
The other container holds the stamp.
Which item is in the tin?
Answer:
```

| 候选完整串 | token IDs | 逐token条件log p | 完整总分 | 物品部分 | 句号部分 |
|---|---|---|---|---|---|
| ' card.' | [3701, 13] | [-9.8350830078125, -3.7332680225372314] | -13.5684 | -9.8351 | -3.7333 |
| ' stamp.' | [21206, 13] | [-9.628652572631836, -3.2542548179626465] | -12.8829 | -9.6287 | -3.2543 |

