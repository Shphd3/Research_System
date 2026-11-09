# S13完整案例册

案例规则在看确认统计前固定：每类别／SAE保留首确认家族、Q频率差中位数和最小值。最小值可能仍为正，不伪造反例。所有原文原样保留，类别名和冠词可同时变化。0只代表Top32排除；Q/G是次数/6000，不等于z。每幅12成员图仅为可读示例；完整并集保存在case_member_values.csv。


## 动物 · Attention输出 · N004

规则：first_confirmation；场景簇partial_visibility；Q粗−细差+1.482pp。标签顺序['animal', 'cat', 'dog']，读取冒号索引[23, 23, 23]，全向量L2=[36.1032, 37.6692, 38.2194]。父→两细类交集[26, 28]；同父细类交集26。

```text
A curtain briefly exposed a picture of an animal before closing again. The viewer is trying to describe the subject.
Description:
```

```text
A curtain briefly exposed a picture of a cat before closing again. The viewer is trying to describe the subject.
Description:
```

```text
A curtain briefly exposed a picture of a dog before closing again. The viewer is trying to describe the subject.
Description:
```

| ID | 父z / q | 细1z / q | 细2z / q | Q / G次数 | 本例成员 |
| --- | --- | --- | --- | --- | --- |
| 18691 | 0.0000 / 0.0000 | 2.3814 / 0.0632 | 5.2143 / 0.1364 | 80 / 157 | 细类换入 |
| 18034 | 3.8262 / 0.1060 | 0.0000 / 0.0000 | 2.3044 / 0.0603 | 48 / 194 | 父子保留／分支变化 |
| 28120 | 0.0000 / 0.0000 | 5.1354 / 0.1363 | 0.0000 / 0.0000 | 8 / 8 | 细类换入 |
| 18237 | 2.3469 / 0.0650 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 14 / 25 | 父类退出 |
| 19948 | 2.3340 / 0.0646 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 29 / 256 | 父类退出 |
| 8644 | 2.1670 / 0.0600 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 10 / 64 | 父类退出 |
| 2046 | 0.0000 / 0.0000 | 2.6813 / 0.0712 | 0.0000 / 0.0000 | 1 / 2 | 细类换入 |
| 23918 | 0.0000 / 0.0000 | 2.6564 / 0.0705 | 0.0000 / 0.0000 | 39 / 60 | 细类换入 |
| 18535 | 0.0000 / 0.0000 | 2.5229 / 0.0670 | 0.0000 / 0.0000 | 0 / 59 | 细类换入 |
| 18460 | 2.4035 / 0.0666 | 2.5227 / 0.0670 | 0.0000 / 0.0000 | 132 / 110 | 父子保留／分支变化 |
| 25754 | 2.2756 / 0.0630 | 0.0000 / 0.0000 | 2.5409 / 0.0665 | 18 / 32 | 父子保留／分支变化 |
| 2520 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 2.4948 / 0.0653 | 116 / 224 | 细类换入 |


## 动物 · Attention输出 · N048

规则：median_D_Q；场景簇identification_without_object；Q粗−细差+3.435pp。标签顺序['animal', 'cat', 'dog']，读取冒号索引[24, 24, 24]，全向量L2=[31.4182, 31.6424, 31.7396]。父→两细类交集[22, 24]；同父细类交集26。

```text
The exhibit case was empty, but its note referred to an animal. A visitor asked what should have been there.
Description:
```

```text
The exhibit case was empty, but its note referred to a cat. A visitor asked what should have been there.
Description:
```

```text
The exhibit case was empty, but its note referred to a dog. A visitor asked what should have been there.
Description:
```

| ID | 父z / q | 细1z / q | 细2z / q | Q / G次数 | 本例成员 |
| --- | --- | --- | --- | --- | --- |
| 18034 | 3.7737 / 0.1201 | 0.0000 / 0.0000 | 2.0015 / 0.0631 | 48 / 194 | 父子保留／分支变化 |
| 21585 | 0.0000 / 0.0000 | 2.0346 / 0.0643 | 2.1163 / 0.0667 | 792 / 3154 | 细类换入 |
| 24307 | 0.0000 / 0.0000 | 1.8655 / 0.0590 | 2.1484 / 0.0677 | 31 / 173 | 细类换入 |
| 19815 | 0.0000 / 0.0000 | 1.7873 / 0.0565 | 1.9797 / 0.0624 | 3 / 55 | 细类换入 |
| 13196 | 1.8457 / 0.0587 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 9 / 26 | 父类退出 |
| 4647 | 0.0000 / 0.0000 | 1.7429 / 0.0551 | 1.9124 / 0.0603 | 852 / 354 | 细类换入 |
| 3843 | 1.7291 / 0.0550 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 52 / 518 | 父类退出 |
| 7855 | 1.6947 / 0.0539 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 737 / 105 | 父类退出 |
| 29472 | 1.6829 / 0.0536 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 8 / 46 | 父类退出 |
| 6757 | 1.6675 / 0.0531 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 27 / 22 | 父类退出 |
| 20439 | 1.6524 / 0.0526 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 1203 / 1160 | 父类退出 |
| 18331 | 1.6382 / 0.0521 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 62 / 128 | 父类退出 |


## 动物 · Attention输出 · N025

规则：minimum_D_Q；场景簇translation_gap；Q粗−细差-2.491pp。标签顺序['animal', 'cat', 'dog']，读取冒号索引[22, 22, 22]，全向量L2=[34.5949, 35.3939, 35.6506]。父→两细类交集[25, 27]；同父细类交集28。

```text
Everything in the leaflet was translated except the line describing an animal. A translator has reached that gap.
Description:
```

```text
Everything in the leaflet was translated except the line describing a cat. A translator has reached that gap.
Description:
```

```text
Everything in the leaflet was translated except the line describing a dog. A translator has reached that gap.
Description:
```

| ID | 父z / q | 细1z / q | 细2z / q | Q / G次数 | 本例成员 |
| --- | --- | --- | --- | --- | --- |
| 18034 | 3.1095 / 0.0899 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 48 / 194 | 父类退出 |
| 24998 | 0.0000 / 0.0000 | 2.1479 / 0.0607 | 2.0430 / 0.0573 | 1908 / 2255 | 细类换入 |
| 18691 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 3.3815 / 0.0949 | 80 / 157 | 细类换入 |
| 5897 | 0.0000 / 0.0000 | 1.5327 / 0.0433 | 1.7975 / 0.0504 | 4505 / 2474 | 细类换入 |
| 5767 | 1.6119 / 0.0466 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 1 / 28 | 父类退出 |
| 13358 | 0.0000 / 0.0000 | 1.4644 / 0.0414 | 1.6412 / 0.0460 | 134 / 2196 | 细类换入 |
| 29508 | 1.5069 / 0.0436 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 64 / 55 | 父类退出 |
| 12212 | 1.4531 / 0.0420 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 3 / 6 | 父类退出 |
| 11779 | 1.4519 / 0.0420 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 44 / 175 | 父类退出 |
| 16033 | 1.5570 / 0.0450 | 0.0000 / 0.0000 | 1.8266 / 0.0512 | 8 / 49 | 父子保留／分支变化 |
| 26542 | 0.0000 / 0.0000 | 1.6807 / 0.0475 | 0.0000 / 0.0000 | 101 / 97 | 细类换入 |
| 5552 | 0.0000 / 0.0000 | 1.6764 / 0.0474 | 0.0000 / 0.0000 | 81 / 347 | 细类换入 |


## 交通工具 · Attention输出 · N004

规则：first_confirmation；场景簇partial_visibility；Q粗−细差+1.270pp。标签顺序['vehicle', 'car', 'bicycle']，读取冒号索引[23, 23, 23]，全向量L2=[37.6704, 38.5313, 38.671]。父→两细类交集[28, 24]；同父细类交集25。

```text
A curtain briefly exposed a picture of a vehicle before closing again. The viewer is trying to describe the subject.
Description:
```

```text
A curtain briefly exposed a picture of a car before closing again. The viewer is trying to describe the subject.
Description:
```

```text
A curtain briefly exposed a picture of a bicycle before closing again. The viewer is trying to describe the subject.
Description:
```

| ID | 父z / q | 细1z / q | 细2z / q | Q / G次数 | 本例成员 |
| --- | --- | --- | --- | --- | --- |
| 25754 | 0.0000 / 0.0000 | 2.1444 / 0.0557 | 3.2035 / 0.0828 | 18 / 32 | 细类换入 |
| 11363 | 0.0000 / 0.0000 | 2.1097 / 0.0548 | 2.4625 / 0.0637 | 37 / 55 | 细类换入 |
| 22343 | 0.0000 / 0.0000 | 2.0831 / 0.0541 | 2.1941 / 0.0567 | 12 / 165 | 细类换入 |
| 715 | 1.8848 / 0.0500 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 11 / 407 | 父类退出 |
| 758 | 4.9841 / 0.1323 | 4.1839 / 0.1086 | 2.2028 / 0.0570 | 272 / 338 | 三者共有 |
| 5897 | 1.8612 / 0.0494 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 4505 / 2474 | 父类退出 |
| 16431 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 2.7417 / 0.0709 | 2 / 37 | 细类换入 |
| 14503 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 2.7288 / 0.0706 | 3 / 29 | 细类换入 |
| 23918 | 2.3227 / 0.0617 | 2.0950 / 0.0544 | 0.0000 / 0.0000 | 39 / 60 | 父子保留／分支变化 |
| 9450 | 1.9932 / 0.0529 | 2.5009 / 0.0649 | 0.0000 / 0.0000 | 100 / 133 | 父子保留／分支变化 |
| 9560 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 2.4664 / 0.0638 | 15 / 294 | 细类换入 |
| 15469 | 1.9765 / 0.0525 | 0.0000 / 0.0000 | 2.4334 / 0.0629 | 107 / 257 | 父子保留／分支变化 |


## 交通工具 · Attention输出 · N029

规则：median_D_Q；场景簇catalogue_recovery；Q粗−细差+1.071pp。标签顺序['vehicle', 'car', 'bicycle']，读取冒号索引[25, 25, 25]，全向量L2=[35.7685, 36.1821, 35.1096]。父→两细类交集[23, 21]；同父细类交集21。

```text
The collection database lost the text attached to a vehicle, although its image was preserved. A curator is repairing the entry.
Description:
```

```text
The collection database lost the text attached to a car, although its image was preserved. A curator is repairing the entry.
Description:
```

```text
The collection database lost the text attached to a bicycle, although its image was preserved. A curator is repairing the entry.
Description:
```

| ID | 父z / q | 细1z / q | 细2z / q | Q / G次数 | 本例成员 |
| --- | --- | --- | --- | --- | --- |
| 18831 | 0.0000 / 0.0000 | 2.5797 / 0.0713 | 3.0688 / 0.0874 | 1 / 15 | 细类换入 |
| 758 | 3.9151 / 0.1095 | 2.8159 / 0.0778 | 0.0000 / 0.0000 | 272 / 338 | 父子保留／分支变化 |
| 10899 | 2.4586 / 0.0687 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 85 / 292 | 父类退出 |
| 1016 | 2.4492 / 0.0685 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 27 / 13 | 父类退出 |
| 17199 | 0.0000 / 0.0000 | 1.9142 / 0.0529 | 2.7917 / 0.0795 | 1 / 37 | 细类换入 |
| 21378 | 0.0000 / 0.0000 | 2.0449 / 0.0565 | 2.4177 / 0.0689 | 12 / 14 | 细类换入 |
| 28693 | 2.1498 / 0.0601 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 46 / 72 | 父类退出 |
| 23798 | 2.1461 / 0.0600 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 0 / 3 | 父类退出 |
| 18427 | 2.1257 / 0.0594 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 102 / 80 | 父类退出 |
| 13938 | 2.0969 / 0.0586 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 133 / 140 | 父类退出 |
| 1081 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 4.0163 / 0.1144 | 1 / 19 | 细类换入 |
| 3939 | 2.1681 / 0.0606 | 0.0000 / 0.0000 | 3.6925 / 0.1052 | 15 / 274 | 父子保留／分支变化 |


## 交通工具 · Attention输出 · N025

规则：minimum_D_Q；场景簇translation_gap；Q粗−细差-2.907pp。标签顺序['vehicle', 'car', 'bicycle']，读取冒号索引[22, 22, 22]，全向量L2=[35.1779, 36.2017, 35.5902]。父→两细类交集[25, 19]；同父细类交集22。

```text
Everything in the leaflet was translated except the line describing a vehicle. A translator has reached that gap.
Description:
```

```text
Everything in the leaflet was translated except the line describing a car. A translator has reached that gap.
Description:
```

```text
Everything in the leaflet was translated except the line describing a bicycle. A translator has reached that gap.
Description:
```

| ID | 父z / q | 细1z / q | 细2z / q | Q / G次数 | 本例成员 |
| --- | --- | --- | --- | --- | --- |
| 12277 | 0.0000 / 0.0000 | 1.6443 / 0.0454 | 2.3978 / 0.0674 | 95 / 108 | 细类换入 |
| 758 | 4.5048 / 0.1281 | 3.2212 / 0.0890 | 2.0972 / 0.0589 | 272 / 338 | 三者共有 |
| 1081 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 3.7537 / 0.1055 | 1 / 19 | 细类换入 |
| 8587 | 0.0000 / 0.0000 | 1.6782 / 0.0464 | 2.0891 / 0.0587 | 45 / 43 | 细类换入 |
| 24998 | 0.0000 / 0.0000 | 1.6480 / 0.0455 | 2.1026 / 0.0591 | 1908 / 2255 | 细类换入 |
| 13196 | 1.7928 / 0.0510 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 9 / 26 | 父类退出 |
| 10962 | 1.7485 / 0.0497 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 76 / 111 | 父类退出 |
| 17229 | 1.7254 / 0.0490 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 9 / 20 | 父类退出 |
| 22258 | 1.6743 / 0.0476 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 546 / 318 | 父类退出 |
| 13358 | 1.4953 / 0.0425 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 134 / 2196 | 父类退出 |
| 12212 | 1.4945 / 0.0425 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 3 / 6 | 父类退出 |
| 1016 | 1.4694 / 0.0418 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 27 / 13 | 父类退出 |


## 水果 · Attention输出 · N004

规则：first_confirmation；场景簇partial_visibility；Q粗−细差+0.138pp。标签顺序['fruit', 'apple', 'banana']，读取冒号索引[23, 23, 23]，全向量L2=[36.8957, 39.1175, 38.62]。父→两细类交集[28, 24]；同父细类交集25。

```text
A curtain briefly exposed a picture of a fruit before closing again. The viewer is trying to describe the subject.
Description:
```

```text
A curtain briefly exposed a picture of an apple before closing again. The viewer is trying to describe the subject.
Description:
```

```text
A curtain briefly exposed a picture of a banana before closing again. The viewer is trying to describe the subject.
Description:
```

| ID | 父z / q | 细1z / q | 细2z / q | Q / G次数 | 本例成员 |
| --- | --- | --- | --- | --- | --- |
| 15178 | 2.9811 / 0.0808 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 376 / 267 | 父类退出 |
| 5552 | 2.9396 / 0.0797 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 81 / 347 | 父类退出 |
| 25186 | 0.0000 / 0.0000 | 2.7492 / 0.0703 | 3.0209 / 0.0782 | 364 / 408 | 细类换入 |
| 568 | 0.0000 / 0.0000 | 2.5843 / 0.0661 | 3.1635 / 0.0819 | 3 / 40 | 细类换入 |
| 22343 | 0.0000 / 0.0000 | 2.5852 / 0.0661 | 2.8903 / 0.0748 | 12 / 165 | 细类换入 |
| 4849 | 2.9546 / 0.0801 | 0.0000 / 0.0000 | 4.1556 / 0.1076 | 7 / 81 | 父子保留／分支变化 |
| 3843 | 2.8204 / 0.0764 | 2.4811 / 0.0634 | 0.0000 / 0.0000 | 52 / 518 | 父子保留／分支变化 |
| 21585 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 3.4206 / 0.0886 | 792 / 3154 | 细类换入 |
| 2503 | 2.5219 / 0.0684 | 0.0000 / 0.0000 | 3.2835 / 0.0850 | 59 / 38 | 父子保留／分支变化 |
| 23497 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 3.2491 / 0.0841 | 10 / 50 | 细类换入 |
| 26856 | 2.6555 / 0.0720 | 3.0919 / 0.0790 | 0.0000 / 0.0000 | 13 / 24 | 父子保留／分支变化 |
| 25754 | 2.6571 / 0.0720 | 2.6156 / 0.0669 | 0.0000 / 0.0000 | 18 / 32 | 父子保留／分支变化 |


## 水果 · Attention输出 · N069

规则：median_D_Q；场景簇feedback_request；Q粗−细差+2.393pp。标签顺序['fruit', 'apple', 'banana']，读取冒号索引[21, 21, 21]，全向量L2=[40.8221, 45.2599, 45.0052]。父→两细类交集[25, 22]；同父细类交集22。

```text
Someone submitted only a fruit in response to an explanation task. The response needs a complete descriptive sentence.
Description:
```

```text
Someone submitted only an apple in response to an explanation task. The response needs a complete descriptive sentence.
Description:
```

```text
Someone submitted only a banana in response to an explanation task. The response needs a complete descriptive sentence.
Description:
```

| ID | 父z / q | 细1z / q | 细2z / q | Q / G次数 | 本例成员 |
| --- | --- | --- | --- | --- | --- |
| 3939 | 4.0642 / 0.0996 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 15 / 274 | 父类退出 |
| 18460 | 3.0641 / 0.0751 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 132 / 110 | 父类退出 |
| 27768 | 0.0000 / 0.0000 | 3.4457 / 0.0761 | 3.1590 / 0.0702 | 2 / 2 | 细类换入 |
| 18787 | 0.0000 / 0.0000 | 3.4860 / 0.0770 | 3.0305 / 0.0673 | 98 / 25 | 细类换入 |
| 14723 | 0.0000 / 0.0000 | 2.5470 / 0.0563 | 3.1091 / 0.0691 | 188 / 39 | 细类换入 |
| 9247 | 2.3304 / 0.0571 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 119 / 131 | 父类退出 |
| 3516 | 2.2389 / 0.0548 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 17 / 15 | 父类退出 |
| 9302 | 0.0000 / 0.0000 | 4.2810 / 0.0946 | 0.0000 / 0.0000 | 28 / 22 | 细类换入 |
| 19510 | 3.2107 / 0.0787 | 0.0000 / 0.0000 | 2.8580 / 0.0635 | 152 / 261 | 父子保留／分支变化 |
| 21585 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 3.6520 / 0.0811 | 792 / 3154 | 细类换入 |
| 14769 | 3.1325 / 0.0767 | 3.2925 / 0.0727 | 0.0000 / 0.0000 | 965 / 99 | 父子保留／分支变化 |
| 24998 | 2.4578 / 0.0602 | 0.0000 / 0.0000 | 3.3638 / 0.0747 | 1908 / 2255 | 父子保留／分支变化 |


## 水果 · Attention输出 · N006

规则：minimum_D_Q；场景簇partial_visibility；Q粗−细差-4.303pp。标签顺序['fruit', 'apple', 'banana']，读取冒号索引[28, 28, 28]，全向量L2=[37.5194, 39.1258, 38.5634]。父→两细类交集[26, 21]；同父细类交集21。

```text
One corner of a projected image showed a fruit; the rest was covered by a loose sheet. A witness was asked what appeared there.
Description:
```

```text
One corner of a projected image showed an apple; the rest was covered by a loose sheet. A witness was asked what appeared there.
Description:
```

```text
One corner of a projected image showed a banana; the rest was covered by a loose sheet. A witness was asked what appeared there.
Description:
```

| ID | 父z / q | 细1z / q | 细2z / q | Q / G次数 | 本例成员 |
| --- | --- | --- | --- | --- | --- |
| 15178 | 2.2920 / 0.0611 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 376 / 267 | 父类退出 |
| 12964 | 0.0000 / 0.0000 | 2.0607 / 0.0527 | 2.5348 / 0.0657 | 228 / 43 | 细类换入 |
| 2425 | 2.2157 / 0.0591 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 129 / 21 | 父类退出 |
| 20439 | 2.1002 / 0.0560 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 1203 / 1160 | 父类退出 |
| 17791 | 1.9761 / 0.0527 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 6 / 2 | 父类退出 |
| 12212 | 1.9712 / 0.0525 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 3 / 6 | 父类退出 |
| 772 | 2.7450 / 0.0732 | 2.0673 / 0.0528 | 0.0000 / 0.0000 | 21 / 32 | 父子保留／分支变化 |
| 19948 | 2.4067 / 0.0641 | 2.0371 / 0.0521 | 0.0000 / 0.0000 | 29 / 256 | 父子保留／分支变化 |
| 3637 | 0.0000 / 0.0000 | 2.7505 / 0.0703 | 0.0000 / 0.0000 | 0 / 0 | 细类换入 |
| 14518 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 2.6393 / 0.0684 | 487 / 184 | 细类换入 |
| 9785 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 2.3914 / 0.0620 | 2102 / 241 | 细类换入 |
| 18034 | 1.9545 / 0.0521 | 0.0000 / 0.0000 | 2.3607 / 0.0612 | 48 / 194 | 父子保留／分支变化 |


## 家具 · Attention输出 · N004

规则：first_confirmation；场景簇partial_visibility；Q粗−细差+1.402pp。标签顺序['furniture', 'chair', 'sofa']，读取冒号索引[25, 23, 23]，全向量L2=[35.7017, 37.1517, 37.0975]。父→两细类交集[29, 24]；同父细类交集26。

```text
A curtain briefly exposed a picture of a piece of furniture before closing again. The viewer is trying to describe the subject.
Description:
```

```text
A curtain briefly exposed a picture of a chair before closing again. The viewer is trying to describe the subject.
Description:
```

```text
A curtain briefly exposed a picture of a sofa before closing again. The viewer is trying to describe the subject.
Description:
```

| ID | 父z / q | 细1z / q | 细2z / q | Q / G次数 | 本例成员 |
| --- | --- | --- | --- | --- | --- |
| 22343 | 0.0000 / 0.0000 | 2.5488 / 0.0686 | 3.2640 / 0.0880 | 12 / 165 | 细类换入 |
| 9270 | 2.5174 / 0.0705 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 399 / 399 | 父类退出 |
| 22258 | 0.0000 / 0.0000 | 2.2290 / 0.0600 | 2.7985 / 0.0754 | 546 / 318 | 细类换入 |
| 9450 | 0.0000 / 0.0000 | 2.2979 / 0.0619 | 2.6771 / 0.0722 | 100 / 133 | 细类换入 |
| 7214 | 2.3145 / 0.0648 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 34 / 123 | 父类退出 |
| 21173 | 2.3728 / 0.0665 | 0.0000 / 0.0000 | 3.1495 / 0.0849 | 9 / 21 | 父子保留／分支变化 |
| 18460 | 2.6891 / 0.0753 | 2.5389 / 0.0683 | 0.0000 / 0.0000 | 132 / 110 | 父子保留／分支变化 |
| 4647 | 2.7046 / 0.0758 | 3.0327 / 0.0816 | 0.0000 / 0.0000 | 852 / 354 | 父子保留／分支变化 |
| 22267 | 2.6576 / 0.0744 | 3.0139 / 0.0811 | 0.0000 / 0.0000 | 199 / 148 | 父子保留／分支变化 |
| 22384 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 2.8752 / 0.0775 | 0 / 3 | 细类换入 |
| 27013 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 2.7366 / 0.0738 | 197 / 65 | 细类换入 |
| 18510 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 2.5873 / 0.0697 | 359 / 189 | 细类换入 |


## 家具 · Attention输出 · N058

规则：median_D_Q；场景簇rehearsal；Q粗−细差+1.433pp。标签顺序['furniture', 'chair', 'sofa']，读取冒号索引[29, 27, 27]，全向量L2=[31.0807, 30.6428, 31.0862]。父→两细类交集[23, 24]；同父细类交集22。

```text
Before the microphone was switched on, the presenter was given a piece of furniture as a subject to explain. The rehearsal is about to begin.
Description:
```

```text
Before the microphone was switched on, the presenter was given a chair as a subject to explain. The rehearsal is about to begin.
Description:
```

```text
Before the microphone was switched on, the presenter was given a sofa as a subject to explain. The rehearsal is about to begin.
Description:
```

| ID | 父z / q | 细1z / q | 细2z / q | Q / G次数 | 本例成员 |
| --- | --- | --- | --- | --- | --- |
| 21596 | 2.2203 / 0.0714 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 46 / 154 | 父类退出 |
| 1609 | 2.1799 / 0.0701 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 93 / 94 | 父类退出 |
| 19492 | 0.0000 / 0.0000 | 2.0213 / 0.0660 | 2.2971 / 0.0739 | 7 / 8 | 细类换入 |
| 9270 | 2.1156 / 0.0681 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 399 / 399 | 父类退出 |
| 10899 | 2.0710 / 0.0666 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 85 / 292 | 父类退出 |
| 14086 | 2.0377 / 0.0656 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 63 / 41 | 父类退出 |
| 24149 | 2.0147 / 0.0648 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 12 / 2 | 父类退出 |
| 9560 | 2.4743 / 0.0796 | 0.0000 / 0.0000 | 2.2310 / 0.0718 | 15 / 294 | 父子保留／分支变化 |
| 22343 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 2.7097 / 0.0872 | 12 / 165 | 细类换入 |
| 19297 | 2.4662 / 0.0793 | 0.0000 / 0.0000 | 2.6595 / 0.0856 | 29 / 321 | 父子保留／分支变化 |
| 7163 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 2.5658 / 0.0825 | 0 / 6 | 细类换入 |
| 27177 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 2.5009 / 0.0805 | 9 / 250 | 细类换入 |


## 家具 · Attention输出 · N036

规则：minimum_D_Q；场景簇unfinished_correspondence；Q粗−细差-8.298pp。标签顺序['furniture', 'chair', 'sofa']，读取冒号索引[30, 28, 28]，全向量L2=[35.4755, 39.8115, 36.9809]。父→两细类交集[13, 22]；同父细类交集15。

```text
Someone began an explanation of a piece of furniture on the back of a postcard, then ran out of space. A fuller description is wanted.
Description:
```

```text
Someone began an explanation of a chair on the back of a postcard, then ran out of space. A fuller description is wanted.
Description:
```

```text
Someone began an explanation of a sofa on the back of a postcard, then ran out of space. A fuller description is wanted.
Description:
```

| ID | 父z / q | 细1z / q | 细2z / q | Q / G次数 | 本例成员 |
| --- | --- | --- | --- | --- | --- |
| 18373 | 3.1579 / 0.0890 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 624 / 748 | 父类退出 |
| 9785 | 0.0000 / 0.0000 | 3.6576 / 0.0919 | 2.7056 / 0.0732 | 2102 / 241 | 细类换入 |
| 9140 | 2.8133 / 0.0793 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 6 / 203 | 父类退出 |
| 10041 | 2.8079 / 0.0791 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 145 / 1262 | 父类退出 |
| 19815 | 2.7244 / 0.0768 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 3 / 55 | 父类退出 |
| 2585 | 2.5858 / 0.0729 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 208 / 500 | 父类退出 |
| 7214 | 3.2887 / 0.0927 | 0.0000 / 0.0000 | 2.1028 / 0.0569 | 34 / 123 | 父子保留／分支变化 |
| 20439 | 0.0000 / 0.0000 | 2.3997 / 0.0603 | 2.3131 / 0.0625 | 1203 / 1160 | 细类换入 |
| 18460 | 2.1594 / 0.0609 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 132 / 110 | 父类退出 |
| 3407 | 5.2929 / 0.1492 | 2.6337 / 0.0662 | 4.1785 / 0.1130 | 95 / 33 | 三者共有 |
| 10899 | 2.1122 / 0.0595 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 85 / 292 | 父类退出 |
| 24998 | 0.0000 / 0.0000 | 2.3226 / 0.0583 | 2.2058 / 0.0596 | 1908 / 2255 | 细类换入 |


## 衣物 · Attention输出 · N004

规则：first_confirmation；场景簇partial_visibility；Q粗−细差+2.168pp。标签顺序['clothing', 'shirt', 'trousers']，读取冒号索引[25, 23, 25]，全向量L2=[36.8144, 37.638, 38.1758]。父→两细类交集[26, 26]；同父细类交集29。

```text
A curtain briefly exposed a picture of an item of clothing before closing again. The viewer is trying to describe the subject.
Description:
```

```text
A curtain briefly exposed a picture of a shirt before closing again. The viewer is trying to describe the subject.
Description:
```

```text
A curtain briefly exposed a picture of a pair of trousers before closing again. The viewer is trying to describe the subject.
Description:
```

| ID | 父z / q | 细1z / q | 细2z / q | Q / G次数 | 本例成员 |
| --- | --- | --- | --- | --- | --- |
| 3843 | 0.0000 / 0.0000 | 2.6358 / 0.0700 | 3.3645 / 0.0881 | 52 / 518 | 细类换入 |
| 715 | 0.0000 / 0.0000 | 2.6021 / 0.0691 | 3.3950 / 0.0889 | 11 / 407 | 细类换入 |
| 23918 | 2.7631 / 0.0751 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 39 / 60 | 父类退出 |
| 24998 | 0.0000 / 0.0000 | 2.7074 / 0.0719 | 2.8518 / 0.0747 | 1908 / 2255 | 细类换入 |
| 18460 | 0.0000 / 0.0000 | 2.6787 / 0.0712 | 2.8158 / 0.0738 | 132 / 110 | 细类换入 |
| 18625 | 2.5500 / 0.0693 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 155 / 93 | 父类退出 |
| 4849 | 2.5454 / 0.0691 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 7 / 81 | 父类退出 |
| 22258 | 0.0000 / 0.0000 | 2.4361 / 0.0647 | 2.4022 / 0.0629 | 546 / 318 | 细类换入 |
| 2520 | 8.5240 / 0.2315 | 5.6006 / 0.1488 | 7.1374 / 0.1870 | 116 / 224 | 三者共有 |
| 7214 | 2.2497 / 0.0611 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 34 / 123 | 父类退出 |
| 22267 | 2.9269 / 0.0795 | 2.5575 / 0.0679 | 0.0000 / 0.0000 | 199 / 148 | 父子保留／分支变化 |
| 6260 | 2.8539 / 0.0775 | 2.5434 / 0.0676 | 0.0000 / 0.0000 | 3 / 19 | 父子保留／分支变化 |


## 衣物 · Attention输出 · N022

规则：median_D_Q；场景簇misplaced_caption；Q粗−细差+3.428pp。标签顺序['clothing', 'shirt', 'trousers']，读取冒号索引[25, 23, 25]，全向量L2=[35.221, 35.8841, 38.9529]。父→两细类交集[24, 21]；同父细类交集24。

```text
The caption slipped off the photograph of an item of clothing while the display was being moved. A volunteer must write another.
Description:
```

```text
The caption slipped off the photograph of a shirt while the display was being moved. A volunteer must write another.
Description:
```

```text
The caption slipped off the photograph of a pair of trousers while the display was being moved. A volunteer must write another.
Description:
```

| ID | 父z / q | 细1z / q | 细2z / q | Q / G次数 | 本例成员 |
| --- | --- | --- | --- | --- | --- |
| 5552 | 0.0000 / 0.0000 | 3.1347 / 0.0874 | 3.1873 / 0.0818 | 81 / 347 | 细类换入 |
| 14516 | 2.9789 / 0.0846 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 91 / 95 | 父类退出 |
| 29824 | 0.0000 / 0.0000 | 2.6803 / 0.0747 | 3.6673 / 0.0941 | 2 / 373 | 细类换入 |
| 20029 | 2.8409 / 0.0807 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 56 / 50 | 父类退出 |
| 18625 | 2.7097 / 0.0769 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 155 / 93 | 父类退出 |
| 22744 | 0.0000 / 0.0000 | 2.4733 / 0.0689 | 3.2550 / 0.0836 | 0 / 36 | 细类换入 |
| 10899 | 2.6801 / 0.0761 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 85 / 292 | 父类退出 |
| 3514 | 0.0000 / 0.0000 | 2.3126 / 0.0644 | 3.2587 / 0.0837 | 32 / 737 | 细类换入 |
| 3975 | 0.0000 / 0.0000 | 2.3353 / 0.0651 | 3.0952 / 0.0795 | 246 / 1250 | 细类换入 |
| 22267 | 2.4093 / 0.0684 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 199 / 148 | 父类退出 |
| 19510 | 2.3760 / 0.0675 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 152 / 261 | 父类退出 |
| 16763 | 3.2817 / 0.0932 | 0.0000 / 0.0000 | 2.9120 / 0.0748 | 7 / 51 | 父子保留／分支变化 |


## 衣物 · Attention输出 · N036

规则：minimum_D_Q；场景簇unfinished_correspondence；Q粗−细差-3.421pp。标签顺序['clothing', 'shirt', 'trousers']，读取冒号索引[30, 28, 30]，全向量L2=[38.1322, 39.3859, 41.0458]。父→两细类交集[14, 19]；同父细类交集14。

```text
Someone began an explanation of an item of clothing on the back of a postcard, then ran out of space. A fuller description is wanted.
Description:
```

```text
Someone began an explanation of a shirt on the back of a postcard, then ran out of space. A fuller description is wanted.
Description:
```

```text
Someone began an explanation of a pair of trousers on the back of a postcard, then ran out of space. A fuller description is wanted.
Description:
```

| ID | 父z / q | 细1z / q | 细2z / q | Q / G次数 | 本例成员 |
| --- | --- | --- | --- | --- | --- |
| 25047 | 5.1500 / 0.1351 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 0 / 9 | 父类退出 |
| 20369 | 5.5202 / 0.1448 | 0.0000 / 0.0000 | 2.3674 / 0.0577 | 0 / 23 | 父子保留／分支变化 |
| 23955 | 2.9832 / 0.0782 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 20 / 89 | 父类退出 |
| 9140 | 3.9244 / 0.1029 | 0.0000 / 0.0000 | 2.5981 / 0.0633 | 6 / 203 | 父子保留／分支变化 |
| 25846 | 2.5475 / 0.0668 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 2 / 14 | 父类退出 |
| 19815 | 2.4794 / 0.0650 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 3 / 55 | 父类退出 |
| 18373 | 2.3024 / 0.0604 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 624 / 748 | 父类退出 |
| 9560 | 2.2830 / 0.0599 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 15 / 294 | 父类退出 |
| 25754 | 0.0000 / 0.0000 | 1.8774 / 0.0477 | 2.5243 / 0.0615 | 18 / 32 | 细类换入 |
| 26542 | 0.0000 / 0.0000 | 1.8767 / 0.0476 | 2.5096 / 0.0611 | 101 / 97 | 细类换入 |
| 27491 | 2.0727 / 0.0544 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 0 / 8 | 父类退出 |
| 11363 | 0.0000 / 0.0000 | 1.8858 / 0.0479 | 2.4423 / 0.0595 | 37 / 55 | 细类换入 |


## 乐器 · Attention输出 · N004

规则：first_confirmation；场景簇partial_visibility；Q粗−细差+1.892pp。标签顺序['instrument', 'piano', 'guitar']，读取冒号索引[24, 23, 23]，全向量L2=[35.9696, 35.3503, 35.2042]。父→两细类交集[25, 27]；同父细类交集25。

```text
A curtain briefly exposed a picture of a musical instrument before closing again. The viewer is trying to describe the subject.
Description:
```

```text
A curtain briefly exposed a picture of a piano before closing again. The viewer is trying to describe the subject.
Description:
```

```text
A curtain briefly exposed a picture of a guitar before closing again. The viewer is trying to describe the subject.
Description:
```

| ID | 父z / q | 细1z / q | 细2z / q | Q / G次数 | 本例成员 |
| --- | --- | --- | --- | --- | --- |
| 3514 | 0.0000 / 0.0000 | 2.3055 / 0.0652 | 2.2110 / 0.0628 | 32 / 737 | 细类换入 |
| 16431 | 0.0000 / 0.0000 | 2.1026 / 0.0595 | 2.1138 / 0.0600 | 2 / 37 | 细类换入 |
| 18510 | 2.1382 / 0.0594 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 359 / 189 | 父类退出 |
| 10041 | 2.1170 / 0.0589 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 145 / 1262 | 父类退出 |
| 21197 | 2.1107 / 0.0587 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 27 / 4 | 父类退出 |
| 13389 | 2.9840 / 0.0830 | 0.0000 / 0.0000 | 2.3856 / 0.0678 | 347 / 515 | 父子保留／分支变化 |
| 4647 | 2.7981 / 0.0778 | 2.3306 / 0.0659 | 0.0000 / 0.0000 | 852 / 354 | 父子保留／分支变化 |
| 18237 | 2.6005 / 0.0723 | 0.0000 / 0.0000 | 2.2719 / 0.0645 | 14 / 25 | 父子保留／分支变化 |
| 23918 | 0.0000 / 0.0000 | 2.8042 / 0.0793 | 0.0000 / 0.0000 | 39 / 60 | 细类换入 |
| 13284 | 2.4762 / 0.0688 | 0.0000 / 0.0000 | 2.1879 / 0.0621 | 5 / 82 | 父子保留／分支变化 |
| 9450 | 2.1449 / 0.0596 | 0.0000 / 0.0000 | 2.5350 / 0.0720 | 100 / 133 | 父子保留／分支变化 |
| 24351 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 2.4418 / 0.0694 | 1141 / 1463 | 细类换入 |


## 乐器 · Attention输出 · N037

规则：median_D_Q；场景簇image_reconstruction；Q粗−细差+4.229pp。标签顺序['instrument', 'piano', 'guitar']，读取冒号索引[25, 24, 24]，全向量L2=[40.6821, 39.8191, 40.5489]。父→两细类交集[22, 25]；同父细类交集22。

```text
A designer must recreate a missing illustration from the words a musical instrument. Before drawing, the designer asks for a description.
Description:
```

```text
A designer must recreate a missing illustration from the words a piano. Before drawing, the designer asks for a description.
Description:
```

```text
A designer must recreate a missing illustration from the words a guitar. Before drawing, the designer asks for a description.
Description:
```

| ID | 父z / q | 细1z / q | 细2z / q | Q / G次数 | 本例成员 |
| --- | --- | --- | --- | --- | --- |
| 18176 | 4.9665 / 0.1221 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 0 / 8 | 父类退出 |
| 22625 | 0.0000 / 0.0000 | 4.4399 / 0.1115 | 4.0339 / 0.0995 | 163 / 518 | 细类换入 |
| 8644 | 6.8526 / 0.1684 | 3.3771 / 0.0848 | 3.5060 / 0.0865 | 10 / 64 | 三者共有 |
| 13317 | 2.9350 / 0.0721 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 0 / 5 | 父类退出 |
| 17795 | 0.0000 / 0.0000 | 2.6088 / 0.0655 | 2.4211 / 0.0597 | 145 / 387 | 细类换入 |
| 5321 | 2.3919 / 0.0588 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 67 / 99 | 父类退出 |
| 12666 | 2.3543 / 0.0579 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 11 / 65 | 父类退出 |
| 4849 | 2.2264 / 0.0547 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 7 / 81 | 父类退出 |
| 5709 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 4.2496 / 0.1048 | 1 / 5 | 细类换入 |
| 23751 | 5.1675 / 0.1270 | 2.5768 / 0.0647 | 4.2695 / 0.1053 | 15 / 57 | 三者共有 |
| 8830 | 2.2909 / 0.0563 | 0.0000 / 0.0000 | 3.3621 / 0.0829 | 17 / 17 | 父子保留／分支变化 |
| 25645 | 2.8613 / 0.0703 | 2.3432 / 0.0588 | 0.0000 / 0.0000 | 0 / 11 | 父子保留／分支变化 |


## 乐器 · Attention输出 · N035

规则：minimum_D_Q；场景簇unfinished_correspondence；Q粗−细差-1.773pp。标签顺序['instrument', 'piano', 'guitar']，读取冒号索引[26, 25, 25]，全向量L2=[32.0311, 31.9222, 31.8726]。父→两细类交集[23, 22]；同父细类交集18。

```text
The last intact line of the message names a musical instrument; the descriptive sentence was never sent. It must be supplied now.
Description:
```

```text
The last intact line of the message names a piano; the descriptive sentence was never sent. It must be supplied now.
Description:
```

```text
The last intact line of the message names a guitar; the descriptive sentence was never sent. It must be supplied now.
Description:
```

| ID | 父z / q | 细1z / q | 细2z / q | Q / G次数 | 本例成员 |
| --- | --- | --- | --- | --- | --- |
| 13389 | 3.7059 / 0.1157 | 0.0000 / 0.0000 | 3.1745 / 0.0996 | 347 / 515 | 父子保留／分支变化 |
| 8644 | 2.0301 / 0.0634 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 10 / 64 | 父类退出 |
| 18176 | 1.7427 / 0.0544 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 0 / 8 | 父类退出 |
| 15726 | 1.4648 / 0.0457 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 11 / 687 | 父类退出 |
| 24351 | 1.3854 / 0.0433 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 1141 / 1463 | 父类退出 |
| 27382 | 1.3219 / 0.0413 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 1 / 7 | 父类退出 |
| 9169 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 2.2918 / 0.0719 | 30 / 94 | 细类换入 |
| 9560 | 1.8601 / 0.0581 | 0.0000 / 0.0000 | 1.5725 / 0.0493 | 15 / 294 | 父子保留／分支变化 |
| 11779 | 0.0000 / 0.0000 | 2.0326 / 0.0637 | 0.0000 / 0.0000 | 44 / 175 | 细类换入 |
| 13954 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 2.0081 / 0.0630 | 5 / 57 | 细类换入 |
| 19510 | 0.0000 / 0.0000 | 2.0038 / 0.0628 | 0.0000 / 0.0000 | 152 / 261 | 细类换入 |
| 27471 | 0.0000 / 0.0000 | 1.9499 / 0.0611 | 0.0000 / 0.0000 | 64 / 52 | 细类换入 |


## 花 · Attention输出 · N004

规则：first_confirmation；场景簇partial_visibility；Q粗−细差+0.906pp。标签顺序['flower', 'rose', 'tulip']，读取冒号索引[23, 23, 24]，全向量L2=[37.5407, 38.7851, 38.1197]。父→两细类交集[28, 29]；同父细类交集27。

```text
A curtain briefly exposed a picture of a flower before closing again. The viewer is trying to describe the subject.
Description:
```

```text
A curtain briefly exposed a picture of a rose before closing again. The viewer is trying to describe the subject.
Description:
```

```text
A curtain briefly exposed a picture of a tulip before closing again. The viewer is trying to describe the subject.
Description:
```

| ID | 父z / q | 细1z / q | 细2z / q | Q / G次数 | 本例成员 |
| --- | --- | --- | --- | --- | --- |
| 27676 | 2.8144 / 0.0750 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 6 / 14 | 父类退出 |
| 11468 | 2.4711 / 0.0658 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 4 / 13 | 父类退出 |
| 22384 | 2.8237 / 0.0752 | 2.4708 / 0.0637 | 0.0000 / 0.0000 | 0 / 3 | 父子保留／分支变化 |
| 12233 | 2.7598 / 0.0735 | 0.0000 / 0.0000 | 2.9333 / 0.0769 | 97 / 314 | 父子保留／分支变化 |
| 6221 | 2.4948 / 0.0665 | 0.0000 / 0.0000 | 2.8662 / 0.0752 | 83 / 176 | 父子保留／分支变化 |
| 24351 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 2.8472 / 0.0747 | 1141 / 1463 | 细类换入 |
| 978 | 0.0000 / 0.0000 | 2.7067 / 0.0698 | 0.0000 / 0.0000 | 8 / 12 | 细类换入 |
| 8349 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 2.5050 / 0.0657 | 184 / 73 | 细类换入 |
| 6883 | 0.0000 / 0.0000 | 2.5486 / 0.0657 | 0.0000 / 0.0000 | 365 / 267 | 细类换入 |
| 27013 | 0.0000 / 0.0000 | 2.5091 / 0.0647 | 0.0000 / 0.0000 | 197 / 65 | 细类换入 |
| 3514 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 2.4410 / 0.0640 | 32 / 737 | 细类换入 |
| 9450 | 0.0000 / 0.0000 | 2.4108 / 0.0622 | 0.0000 / 0.0000 | 100 / 133 | 细类换入 |


## 花 · Attention输出 · N036

规则：median_D_Q；场景簇unfinished_correspondence；Q粗−细差+2.698pp。标签顺序['flower', 'rose', 'tulip']，读取冒号索引[28, 28, 29]，全向量L2=[36.8887, 40.3946, 38.3694]。父→两细类交集[19, 16]；同父细类交集16。

```text
Someone began an explanation of a flower on the back of a postcard, then ran out of space. A fuller description is wanted.
Description:
```

```text
Someone began an explanation of a rose on the back of a postcard, then ran out of space. A fuller description is wanted.
Description:
```

```text
Someone began an explanation of a tulip on the back of a postcard, then ran out of space. A fuller description is wanted.
Description:
```

| ID | 父z / q | 细1z / q | 细2z / q | Q / G次数 | 本例成员 |
| --- | --- | --- | --- | --- | --- |
| 29508 | 2.5473 / 0.0691 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 64 / 55 | 父类退出 |
| 7349 | 2.2778 / 0.0617 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 0 / 9 | 父类退出 |
| 22258 | 0.0000 / 0.0000 | 1.6694 / 0.0413 | 2.5342 / 0.0660 | 546 / 318 | 细类换入 |
| 10041 | 1.9764 / 0.0536 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 145 / 1262 | 父类退出 |
| 15726 | 1.9233 / 0.0521 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 11 / 687 | 父类退出 |
| 772 | 1.9222 / 0.0521 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 21 / 32 | 父类退出 |
| 6554 | 1.8712 / 0.0507 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 207 / 253 | 父类退出 |
| 6221 | 1.6992 / 0.0461 | 0.0000 / 0.0000 | 3.7808 / 0.0985 | 83 / 176 | 父子保留／分支变化 |
| 12233 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 3.7682 / 0.0982 | 97 / 314 | 细类换入 |
| 18034 | 1.8105 / 0.0491 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 48 / 194 | 父类退出 |
| 19510 | 1.7736 / 0.0481 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 152 / 261 | 父类退出 |
| 14769 | 1.7685 / 0.0479 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 965 / 99 | 父类退出 |


## 花 · Attention输出 · N046

规则：minimum_D_Q；场景簇identification_without_object；Q粗−细差-1.646pp。标签顺序['flower', 'rose', 'tulip']，读取冒号索引[24, 24, 25]，全向量L2=[38.0692, 38.5577, 38.489]。父→两细类交集[24, 21]；同父细类交集21。

```text
The actual subject was unavailable, so the instructor supplied only the phrase a flower. A participant must explain that phrase.
Description:
```

```text
The actual subject was unavailable, so the instructor supplied only the phrase a rose. A participant must explain that phrase.
Description:
```

```text
The actual subject was unavailable, so the instructor supplied only the phrase a tulip. A participant must explain that phrase.
Description:
```

| ID | 父z / q | 细1z / q | 细2z / q | Q / G次数 | 本例成员 |
| --- | --- | --- | --- | --- | --- |
| 18186 | 2.9704 / 0.0780 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 14 / 12 | 父类退出 |
| 29508 | 2.6209 / 0.0688 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 64 / 55 | 父类退出 |
| 22783 | 0.0000 / 0.0000 | 1.7595 / 0.0456 | 2.4158 / 0.0628 | 1058 / 5 | 细类换入 |
| 4236 | 1.9670 / 0.0517 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 88 / 262 | 父类退出 |
| 11019 | 1.7421 / 0.0458 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 11 / 10 | 父类退出 |
| 22247 | 1.7202 / 0.0452 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 3 / 10 | 父类退出 |
| 21964 | 1.5551 / 0.0408 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 21 / 10 | 父类退出 |
| 14038 | 1.5466 / 0.0406 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 20 / 13 | 父类退出 |
| 2249 | 2.3001 / 0.0604 | 1.6270 / 0.0422 | 0.0000 / 0.0000 | 4 / 0 | 父子保留／分支变化 |
| 978 | 0.0000 / 0.0000 | 2.7149 / 0.0704 | 0.0000 / 0.0000 | 8 / 12 | 细类换入 |
| 11081 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 2.3978 / 0.0623 | 1049 / 203 | 细类换入 |
| 24351 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 2.3579 / 0.0613 | 1141 / 1463 | 细类换入 |


## 餐用器具 · Attention输出 · N004

规则：first_confirmation；场景簇partial_visibility；Q粗−细差+1.044pp。标签顺序['cutlery', 'spoon', 'fork']，读取冒号索引[27, 23, 23]，全向量L2=[36.7973, 37.8393, 36.9566]。父→两细类交集[27, 28]；同父细类交集27。

```text
A curtain briefly exposed a picture of a piece of cutlery before closing again. The viewer is trying to describe the subject.
Description:
```

```text
A curtain briefly exposed a picture of a spoon before closing again. The viewer is trying to describe the subject.
Description:
```

```text
A curtain briefly exposed a picture of a fork before closing again. The viewer is trying to describe the subject.
Description:
```

| ID | 父z / q | 细1z / q | 细2z / q | Q / G次数 | 本例成员 |
| --- | --- | --- | --- | --- | --- |
| 2520 | 2.5642 / 0.0697 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 116 / 224 | 父类退出 |
| 24351 | 0.0000 / 0.0000 | 2.3731 / 0.0627 | 2.4543 / 0.0664 | 1141 / 1463 | 细类换入 |
| 22343 | 2.2889 / 0.0622 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 12 / 165 | 父类退出 |
| 3975 | 2.0553 / 0.0559 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 246 / 1250 | 父类退出 |
| 4647 | 2.7108 / 0.0737 | 0.0000 / 0.0000 | 2.8836 / 0.0780 | 852 / 354 | 父子保留／分支变化 |
| 3153 | 0.0000 / 0.0000 | 2.6038 / 0.0688 | 0.0000 / 0.0000 | 1 / 21 | 细类换入 |
| 28205 | 2.0538 / 0.0558 | 0.0000 / 0.0000 | 2.4761 / 0.0670 | 7 / 13 | 父子保留／分支变化 |
| 568 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 2.4280 / 0.0657 | 3 / 40 | 细类换入 |
| 9720 | 0.0000 / 0.0000 | 2.4722 / 0.0653 | 0.0000 / 0.0000 | 3 / 6 | 细类换入 |
| 22258 | 2.3519 / 0.0639 | 2.3681 / 0.0626 | 0.0000 / 0.0000 | 546 / 318 | 父子保留／分支变化 |
| 29455 | 0.0000 / 0.0000 | 2.4437 / 0.0646 | 0.0000 / 0.0000 | 20 / 904 | 细类换入 |
| 21585 | 0.0000 / 0.0000 | 2.4160 / 0.0638 | 0.0000 / 0.0000 | 792 / 3154 | 细类换入 |


## 餐用器具 · Attention输出 · N030

规则：median_D_Q；场景簇catalogue_recovery；Q粗−细差+1.733pp。标签顺序['cutlery', 'spoon', 'fork']，读取冒号索引[25, 21, 21]，全向量L2=[37.4278, 37.6114, 36.3227]。父→两细类交集[24, 21]；同父细类交集24。

```text
Someone found a miniature illustration of a piece of cutlery between two catalogue pages. The illustration has no readable description.
Description:
```

```text
Someone found a miniature illustration of a spoon between two catalogue pages. The illustration has no readable description.
Description:
```

```text
Someone found a miniature illustration of a fork between two catalogue pages. The illustration has no readable description.
Description:
```

| ID | 父z / q | 细1z / q | 细2z / q | Q / G次数 | 本例成员 |
| --- | --- | --- | --- | --- | --- |
| 9255 | 0.0000 / 0.0000 | 3.0267 / 0.0805 | 3.9881 / 0.1098 | 69 / 323 | 细类换入 |
| 21585 | 0.0000 / 0.0000 | 2.8647 / 0.0762 | 3.6032 / 0.0992 | 792 / 3154 | 细类换入 |
| 5649 | 0.0000 / 0.0000 | 3.1704 / 0.0843 | 3.0485 / 0.0839 | 4 / 172 | 细类换入 |
| 26496 | 0.0000 / 0.0000 | 3.1286 / 0.0832 | 2.8496 / 0.0785 | 3 / 11 | 细类换入 |
| 14744 | 2.8784 / 0.0769 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 38 / 62 | 父类退出 |
| 19296 | 2.7098 / 0.0724 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 100 / 81 | 父类退出 |
| 9270 | 2.6928 / 0.0719 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 399 / 399 | 父类退出 |
| 6554 | 2.6583 / 0.0710 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 207 / 253 | 父类退出 |
| 24741 | 2.5727 / 0.0687 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 3 / 14 | 父类退出 |
| 772 | 2.5195 / 0.0673 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 21 / 32 | 父类退出 |
| 3407 | 2.4785 / 0.0662 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 95 / 33 | 父类退出 |
| 23751 | 5.3502 / 0.1429 | 3.4494 / 0.0917 | 3.1304 / 0.0862 | 15 / 57 | 三者共有 |


## 餐用器具 · Attention输出 · N035

规则：minimum_D_Q；场景簇unfinished_correspondence；Q粗−细差-4.388pp。标签顺序['cutlery', 'spoon', 'fork']，读取冒号索引[29, 25, 25]，全向量L2=[34.8149, 34.3323, 34.0404]。父→两细类交集[19, 20]；同父细类交集20。

```text
The last intact line of the message names a piece of cutlery; the descriptive sentence was never sent. It must be supplied now.
Description:
```

```text
The last intact line of the message names a spoon; the descriptive sentence was never sent. It must be supplied now.
Description:
```

```text
The last intact line of the message names a fork; the descriptive sentence was never sent. It must be supplied now.
Description:
```

| ID | 父z / q | 细1z / q | 细2z / q | Q / G次数 | 本例成员 |
| --- | --- | --- | --- | --- | --- |
| 23751 | 2.9357 / 0.0843 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 15 / 57 | 父类退出 |
| 25186 | 3.5710 / 0.1026 | 2.0342 / 0.0592 | 0.0000 / 0.0000 | 364 / 408 | 父子保留／分支变化 |
| 6643 | 0.0000 / 0.0000 | 1.7428 / 0.0508 | 1.9348 / 0.0568 | 8 / 21 | 细类换入 |
| 830 | 1.8498 / 0.0531 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 0 / 3 | 父类退出 |
| 2520 | 1.8446 / 0.0530 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 116 / 224 | 父类退出 |
| 28624 | 1.7727 / 0.0509 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 103 / 301 | 父类退出 |
| 5169 | 1.7677 / 0.0508 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 15 / 20 | 父类退出 |
| 27382 | 1.7278 / 0.0496 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 1 / 7 | 父类退出 |
| 9560 | 1.6408 / 0.0471 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 15 / 294 | 父类退出 |
| 9005 | 1.6185 / 0.0465 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 270 / 15 | 父类退出 |
| 17072 | 1.5990 / 0.0459 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 34 / 117 | 父类退出 |
| 2254 | 0.0000 / 0.0000 | 1.5558 / 0.0453 | 1.4757 / 0.0434 | 3309 / 311 | 细类换入 |


## 动物 · MLP输入 · N004

规则：first_confirmation；场景簇partial_visibility；Q粗−细差+2.501pp。标签顺序['animal', 'cat', 'dog']，读取冒号索引[23, 23, 23]，全向量L2=[110.4319, 108.0576, 108.3124]。父→两细类交集[26, 28]；同父细类交集27。

```text
A curtain briefly exposed a picture of an animal before closing again. The viewer is trying to describe the subject.
Description:
```

```text
A curtain briefly exposed a picture of a cat before closing again. The viewer is trying to describe the subject.
Description:
```

```text
A curtain briefly exposed a picture of a dog before closing again. The viewer is trying to describe the subject.
Description:
```

| ID | 父z / q | 细1z / q | 细2z / q | Q / G次数 | 本例成员 |
| --- | --- | --- | --- | --- | --- |
| 22958 | 0.0000 / 0.0000 | 8.0001 / 0.0740 | 0.0000 / 0.0000 | 26 / 51 | 细类换入 |
| 17366 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 6.1694 / 0.0570 | 75 / 107 | 细类换入 |
| 22309 | 0.0000 / 0.0000 | 2.9416 / 0.0272 | 2.8792 / 0.0266 | 33 / 11 | 细类换入 |
| 24399 | 6.5141 / 0.0590 | 3.3630 / 0.0311 | 3.7201 / 0.0343 | 109 / 228 | 三者共有 |
| 28550 | 2.7496 / 0.0249 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 17 / 45 | 父类退出 |
| 16425 | 2.7134 / 0.0246 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 0 / 26 | 父类退出 |
| 29893 | 2.7081 / 0.0245 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 2292 / 430 | 父类退出 |
| 15123 | 2.6122 / 0.0237 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 44 / 1630 | 父类退出 |
| 16240 | 8.0728 / 0.0731 | 10.6037 / 0.0981 | 9.5656 / 0.0883 | 5801 / 4833 | 三者共有 |
| 2491 | 3.1211 / 0.0283 | 0.0000 / 0.0000 | 2.8584 / 0.0264 | 13 / 30 | 父子保留／分支变化 |
| 8856 | 6.4400 / 0.0583 | 8.5584 / 0.0792 | 7.2629 / 0.0671 | 5358 / 4904 | 三者共有 |
| 11234 | 0.0000 / 0.0000 | 3.0540 / 0.0283 | 0.0000 / 0.0000 | 4347 / 3699 | 细类换入 |


## 动物 · MLP输入 · N025

规则：median_D_Q；场景簇translation_gap；Q粗−细差+7.225pp。标签顺序['animal', 'cat', 'dog']，读取冒号索引[22, 22, 22]，全向量L2=[114.5974, 112.3544, 114.0175]。父→两细类交集[26, 24]；同父细类交集29。

```text
Everything in the leaflet was translated except the line describing an animal. A translator has reached that gap.
Description:
```

```text
Everything in the leaflet was translated except the line describing a cat. A translator has reached that gap.
Description:
```

```text
Everything in the leaflet was translated except the line describing a dog. A translator has reached that gap.
Description:
```

| ID | 父z / q | 细1z / q | 细2z / q | Q / G次数 | 本例成员 |
| --- | --- | --- | --- | --- | --- |
| 24399 | 6.1150 / 0.0534 | 2.4411 / 0.0217 | 0.0000 / 0.0000 | 109 / 228 | 父子保留／分支变化 |
| 8856 | 0.0000 / 0.0000 | 5.1033 / 0.0454 | 4.2858 / 0.0376 | 5358 / 4904 | 细类换入 |
| 22958 | 0.0000 / 0.0000 | 7.4353 / 0.0662 | 0.0000 / 0.0000 | 26 / 51 | 细类换入 |
| 17366 | 2.5821 / 0.0225 | 3.6155 / 0.0322 | 8.5189 / 0.0747 | 75 / 107 | 三者共有 |
| 3556 | 0.0000 / 0.0000 | 3.4628 / 0.0308 | 3.2830 / 0.0288 | 13 / 10 | 细类换入 |
| 11697 | 0.0000 / 0.0000 | 2.9237 / 0.0260 | 3.6818 / 0.0323 | 3 / 21 | 细类换入 |
| 939 | 3.1111 / 0.0271 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 108 / 162 | 父类退出 |
| 10580 | 0.0000 / 0.0000 | 3.0461 / 0.0271 | 2.2578 / 0.0198 | 93 / 116 | 细类换入 |
| 14187 | 0.0000 / 0.0000 | 2.5250 / 0.0225 | 2.7078 / 0.0237 | 132 / 1645 | 细类换入 |
| 3011 | 2.6108 / 0.0228 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 35 / 244 | 父类退出 |
| 14202 | 2.5082 / 0.0219 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 5 / 62 | 父类退出 |
| 21451 | 2.3381 / 0.0204 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 1191 / 115 | 父类退出 |


## 动物 · MLP输入 · N007

规则：minimum_D_Q；场景簇disputed_memory；Q粗−细差-1.760pp。标签顺序['animal', 'cat', 'dog']，读取冒号索引[24, 24, 24]，全向量L2=[105.0493, 102.1636, 104.4083]。父→两细类交集[24, 25]；同父细类交集27。

```text
Two friends remembered the background differently, yet both recalled an animal in the foreground. They now need a neutral description.
Description:
```

```text
Two friends remembered the background differently, yet both recalled a cat in the foreground. They now need a neutral description.
Description:
```

```text
Two friends remembered the background differently, yet both recalled a dog in the foreground. They now need a neutral description.
Description:
```

| ID | 父z / q | 细1z / q | 细2z / q | Q / G次数 | 本例成员 |
| --- | --- | --- | --- | --- | --- |
| 24399 | 5.9416 / 0.0566 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 109 / 228 | 父类退出 |
| 22958 | 0.0000 / 0.0000 | 8.5706 / 0.0839 | 0.0000 / 0.0000 | 26 / 51 | 细类换入 |
| 14753 | 0.0000 / 0.0000 | 3.9944 / 0.0391 | 3.7222 / 0.0357 | 3163 / 213 | 细类换入 |
| 29479 | 0.0000 / 0.0000 | 3.3727 / 0.0330 | 4.0122 / 0.0384 | 468 / 267 | 细类换入 |
| 22965 | 3.7112 / 0.0353 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 29 / 105 | 父类退出 |
| 14879 | 3.4229 / 0.0326 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 900 / 27 | 父类退出 |
| 2432 | 0.0000 / 0.0000 | 3.4222 / 0.0335 | 3.1956 / 0.0306 | 837 / 45 | 细类换入 |
| 25899 | 3.3467 / 0.0319 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 0 / 2 | 父类退出 |
| 14202 | 5.1406 / 0.0489 | 3.5688 / 0.0349 | 0.0000 / 0.0000 | 5 / 62 | 父子保留／分支变化 |
| 8856 | 5.0360 / 0.0479 | 8.6522 / 0.0847 | 7.7343 / 0.0741 | 5358 / 4904 | 三者共有 |
| 18809 | 3.2542 / 0.0310 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 11 / 73 | 父类退出 |
| 17366 | 6.5997 / 0.0628 | 7.8763 / 0.0771 | 11.4792 / 0.1099 | 75 / 107 | 三者共有 |


## 交通工具 · MLP输入 · N004

规则：first_confirmation；场景簇partial_visibility；Q粗−细差-0.612pp。标签顺序['vehicle', 'car', 'bicycle']，读取冒号索引[23, 23, 23]，全向量L2=[109.2325, 110.6171, 111.0457]。父→两细类交集[29, 25]；同父细类交集24。

```text
A curtain briefly exposed a picture of a vehicle before closing again. The viewer is trying to describe the subject.
Description:
```

```text
A curtain briefly exposed a picture of a car before closing again. The viewer is trying to describe the subject.
Description:
```

```text
A curtain briefly exposed a picture of a bicycle before closing again. The viewer is trying to describe the subject.
Description:
```

| ID | 父z / q | 细1z / q | 细2z / q | Q / G次数 | 本例成员 |
| --- | --- | --- | --- | --- | --- |
| 20696 | 4.7704 / 0.0437 | 2.7968 / 0.0253 | 0.0000 / 0.0000 | 188 / 291 | 父子保留／分支变化 |
| 16830 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 6.3674 / 0.0573 | 7 / 25 | 细类换入 |
| 14913 | 2.7325 / 0.0250 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 1293 / 1852 | 父类退出 |
| 8048 | 2.7016 / 0.0247 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 4481 / 4265 | 父类退出 |
| 5196 | 3.7195 / 0.0341 | 3.2019 / 0.0289 | 0.0000 / 0.0000 | 5097 / 4610 | 父子保留／分支变化 |
| 27101 | 3.5530 / 0.0325 | 3.2030 / 0.0290 | 0.0000 / 0.0000 | 3 / 10 | 父子保留／分支变化 |
| 8917 | 3.0783 / 0.0282 | 2.7692 / 0.0250 | 0.0000 / 0.0000 | 10 / 22 | 父子保留／分支变化 |
| 16240 | 11.5250 / 0.1055 | 10.4022 / 0.0940 | 9.5694 / 0.0862 | 5801 / 4833 | 三者共有 |
| 27974 | 3.1291 / 0.0286 | 3.0464 / 0.0275 | 0.0000 / 0.0000 | 58 / 85 | 父子保留／分支变化 |
| 2491 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 3.1573 / 0.0284 | 13 / 30 | 细类换入 |
| 19178 | 0.0000 / 0.0000 | 3.0367 / 0.0275 | 0.0000 / 0.0000 | 141 / 83 | 细类换入 |
| 25748 | 0.0000 / 0.0000 | 2.8514 / 0.0258 | 0.0000 / 0.0000 | 72 / 8 | 细类换入 |


## 交通工具 · MLP输入 · N008

规则：median_D_Q；场景簇disputed_memory；Q粗−细差+5.531pp。标签顺序['vehicle', 'car', 'bicycle']，读取冒号索引[24, 24, 24]，全向量L2=[120.7651, 120.9934, 120.8183]。父→两细类交集[27, 28]；同父细类交集26。

```text
Years later, the only detail the visitor could recall was a vehicle. The recollection is being put into words.
Description:
```

```text
Years later, the only detail the visitor could recall was a car. The recollection is being put into words.
Description:
```

```text
Years later, the only detail the visitor could recall was a bicycle. The recollection is being put into words.
Description:
```

| ID | 父z / q | 细1z / q | 细2z / q | Q / G次数 | 本例成员 |
| --- | --- | --- | --- | --- | --- |
| 16830 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 5.7111 / 0.0473 | 7 / 25 | 细类换入 |
| 5067 | 0.0000 / 0.0000 | 2.4034 / 0.0199 | 2.8958 / 0.0240 | 7 / 169 | 细类换入 |
| 20696 | 6.8900 / 0.0571 | 5.3634 / 0.0443 | 3.3734 / 0.0279 | 188 / 291 | 三者共有 |
| 47 | 2.2146 / 0.0183 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 4177 / 3417 | 父类退出 |
| 3 | 2.1894 / 0.0181 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 12 / 14 | 父类退出 |
| 8048 | 3.4501 / 0.0286 | 3.8148 / 0.0315 | 0.0000 / 0.0000 | 4481 / 4265 | 父子保留／分支变化 |
| 10385 | 3.0128 / 0.0249 | 0.0000 / 0.0000 | 2.7274 / 0.0226 | 26 / 225 | 父子保留／分支变化 |
| 5196 | 4.8110 / 0.0398 | 4.0332 / 0.0333 | 2.5982 / 0.0215 | 5097 / 4610 | 三者共有 |
| 11234 | 0.0000 / 0.0000 | 2.9410 / 0.0243 | 0.0000 / 0.0000 | 4347 / 3699 | 细类换入 |
| 13262 | 2.3473 / 0.0194 | 0.0000 / 0.0000 | 2.8421 / 0.0235 | 0 / 37 | 父子保留／分支变化 |
| 15123 | 2.6924 / 0.0223 | 0.0000 / 0.0000 | 2.8171 / 0.0233 | 44 / 1630 | 父子保留／分支变化 |
| 4700 | 0.0000 / 0.0000 | 2.7944 / 0.0231 | 0.0000 / 0.0000 | 4684 / 632 | 细类换入 |


## 交通工具 · MLP输入 · N057

规则：minimum_D_Q；场景簇retrieval_error；Q粗−细差-4.820pp。标签顺序['vehicle', 'car', 'bicycle']，读取冒号索引[22, 22, 22]，全向量L2=[112.4292, 113.3289, 112.9041]。父→两细类交集[28, 25]；同父细类交集25。

```text
Only a cached illustration of a vehicle could be recovered from the broken page. The original caption is unavailable.
Description:
```

```text
Only a cached illustration of a car could be recovered from the broken page. The original caption is unavailable.
Description:
```

```text
Only a cached illustration of a bicycle could be recovered from the broken page. The original caption is unavailable.
Description:
```

| ID | 父z / q | 细1z / q | 细2z / q | Q / G次数 | 本例成员 |
| --- | --- | --- | --- | --- | --- |
| 20696 | 4.9347 / 0.0439 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 188 / 291 | 父类退出 |
| 24203 | 0.0000 / 0.0000 | 4.0185 / 0.0355 | 5.0428 / 0.0447 | 1 / 10 | 细类换入 |
| 19327 | 3.8438 / 0.0342 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 80 / 79 | 父类退出 |
| 11234 | 3.1852 / 0.0283 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 4347 / 3699 | 父类退出 |
| 16830 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 6.0060 / 0.0532 | 7 / 25 | 细类换入 |
| 19178 | 0.0000 / 0.0000 | 5.6529 / 0.0499 | 0.0000 / 0.0000 | 141 / 83 | 细类换入 |
| 10013 | 3.9827 / 0.0354 | 3.6182 / 0.0319 | 0.0000 / 0.0000 | 96 / 503 | 父子保留／分支变化 |
| 29506 | 22.4179 / 0.1994 | 21.2775 / 0.1878 | 19.9297 / 0.1765 | 4677 / 5864 | 三者共有 |
| 28295 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 3.7754 / 0.0334 | 8 / 29 | 细类换入 |
| 27346 | 3.3476 / 0.0298 | 3.7737 / 0.0333 | 0.0000 / 0.0000 | 326 / 1285 | 父子保留／分支变化 |
| 16905 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 3.7073 / 0.0328 | 131 / 244 | 细类换入 |
| 28792 | 3.7568 / 0.0334 | 4.8762 / 0.0430 | 6.2838 / 0.0557 | 3 / 21 | 三者共有 |


## 水果 · MLP输入 · N004

规则：first_confirmation；场景簇partial_visibility；Q粗−细差-2.724pp。标签顺序['fruit', 'apple', 'banana']，读取冒号索引[23, 23, 23]，全向量L2=[109.8461, 108.5609, 108.7395]。父→两细类交集[28, 27]；同父细类交集24。

```text
A curtain briefly exposed a picture of a fruit before closing again. The viewer is trying to describe the subject.
Description:
```

```text
A curtain briefly exposed a picture of an apple before closing again. The viewer is trying to describe the subject.
Description:
```

```text
A curtain briefly exposed a picture of a banana before closing again. The viewer is trying to describe the subject.
Description:
```

| ID | 父z / q | 细1z / q | 细2z / q | Q / G次数 | 本例成员 |
| --- | --- | --- | --- | --- | --- |
| 9293 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 6.5233 / 0.0600 | 37 / 11 | 细类换入 |
| 16240 | 8.1250 / 0.0740 | 10.9391 / 0.1008 | 10.8385 / 0.0997 | 5801 / 4833 | 三者共有 |
| 28276 | 0.0000 / 0.0000 | 5.5209 / 0.0509 | 0.0000 / 0.0000 | 33 / 61 | 细类换入 |
| 29886 | 2.6912 / 0.0245 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 3 / 127 | 父类退出 |
| 2491 | 3.4503 / 0.0314 | 4.5073 / 0.0415 | 0.0000 / 0.0000 | 13 / 30 | 父子保留／分支变化 |
| 10167 | 3.2953 / 0.0300 | 0.0000 / 0.0000 | 2.9498 / 0.0271 | 1 / 23 | 父子保留／分支变化 |
| 1814 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 3.5186 / 0.0324 | 53 / 82 | 细类换入 |
| 27974 | 2.7666 / 0.0252 | 0.0000 / 0.0000 | 3.4526 / 0.0318 | 58 / 85 | 父子保留／分支变化 |
| 29188 | 2.8597 / 0.0260 | 3.3891 / 0.0312 | 0.0000 / 0.0000 | 2 / 10 | 父子保留／分支变化 |
| 27076 | 2.6893 / 0.0245 | 0.0000 / 0.0000 | 3.3030 / 0.0304 | 242 / 1097 | 父子保留／分支变化 |
| 5836 | 3.1163 / 0.0284 | 2.8636 / 0.0264 | 0.0000 / 0.0000 | 21 / 8 | 父子保留／分支变化 |
| 10974 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 3.2453 / 0.0298 | 10 / 18 | 细类换入 |


## 水果 · MLP输入 · N059

规则：median_D_Q；场景簇rehearsal；Q粗−细差+2.672pp。标签顺序['fruit', 'apple', 'banana']，读取冒号索引[21, 21, 21]，全向量L2=[110.948, 109.1908, 107.9888]。父→两细类交集[27, 25]；同父细类交集27。

```text
A speaker practiced introducing a fruit without relying on a prepared script. The first descriptive sentence is needed.
Description:
```

```text
A speaker practiced introducing an apple without relying on a prepared script. The first descriptive sentence is needed.
Description:
```

```text
A speaker practiced introducing a banana without relying on a prepared script. The first descriptive sentence is needed.
Description:
```

| ID | 父z / q | 细1z / q | 细2z / q | Q / G次数 | 本例成员 |
| --- | --- | --- | --- | --- | --- |
| 8856 | 0.0000 / 0.0000 | 6.8070 / 0.0623 | 6.2332 / 0.0577 | 5358 / 4904 | 细类换入 |
| 16240 | 3.2988 / 0.0297 | 8.2373 / 0.0754 | 8.8670 / 0.0821 | 5801 / 4833 | 三者共有 |
| 9293 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 10.2665 / 0.0951 | 37 / 11 | 细类换入 |
| 29506 | 39.7925 / 0.3587 | 34.9570 / 0.3201 | 33.2861 / 0.3082 | 4677 / 5864 | 三者共有 |
| 5836 | 6.9394 / 0.0625 | 4.9826 / 0.0456 | 0.0000 / 0.0000 | 21 / 8 | 父子保留／分支变化 |
| 28276 | 0.0000 / 0.0000 | 8.4363 / 0.0773 | 0.0000 / 0.0000 | 33 / 61 | 细类换入 |
| 25279 | 0.0000 / 0.0000 | 3.6775 / 0.0337 | 4.5456 / 0.0421 | 7 / 13 | 细类换入 |
| 5300 | 3.7916 / 0.0342 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 0 / 17 | 父类退出 |
| 12186 | 3.3349 / 0.0301 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 22 / 16 | 父类退出 |
| 8048 | 3.1948 / 0.0288 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 4481 / 4265 | 父类退出 |
| 17390 | 9.4200 / 0.0849 | 6.6984 / 0.0613 | 5.6772 / 0.0526 | 4665 / 5371 | 三者共有 |
| 5530 | 3.0030 / 0.0271 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 22 / 122 | 父类退出 |


## 水果 · MLP输入 · N023

规则：minimum_D_Q；场景簇misplaced_caption；Q粗−细差-6.880pp。标签顺序['fruit', 'apple', 'banana']，读取冒号索引[27, 27, 27]，全向量L2=[111.9777, 110.6688, 111.7248]。父→两细类交集[27, 24]；同父细类交集27。

```text
A loose label was found beside a picture of a fruit, but nobody could match the old wording. A fresh description is needed.
Description:
```

```text
A loose label was found beside a picture of an apple, but nobody could match the old wording. A fresh description is needed.
Description:
```

```text
A loose label was found beside a picture of a banana, but nobody could match the old wording. A fresh description is needed.
Description:
```

| ID | 父z / q | 细1z / q | 细2z / q | Q / G次数 | 本例成员 |
| --- | --- | --- | --- | --- | --- |
| 8856 | 0.0000 / 0.0000 | 5.6819 / 0.0513 | 4.5095 / 0.0404 | 5358 / 4904 | 细类换入 |
| 29893 | 0.0000 / 0.0000 | 3.1189 / 0.0282 | 3.2251 / 0.0289 | 2292 / 430 | 细类换入 |
| 3693 | 0.0000 / 0.0000 | 2.9496 / 0.0267 | 2.7659 / 0.0248 | 10 / 35 | 细类换入 |
| 11887 | 2.8402 / 0.0254 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 170 / 13 | 父类退出 |
| 3011 | 2.8223 / 0.0252 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 35 / 244 | 父类退出 |
| 9293 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 5.6106 / 0.0502 | 37 / 11 | 细类换入 |
| 18758 | 2.6197 / 0.0234 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 94 / 112 | 父类退出 |
| 28550 | 2.5873 / 0.0231 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 17 / 45 | 父类退出 |
| 14202 | 2.5517 / 0.0228 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 5 / 62 | 父类退出 |
| 8758 | 3.6932 / 0.0330 | 2.7124 / 0.0245 | 0.0000 / 0.0000 | 83 / 447 | 父子保留／分支变化 |
| 5836 | 6.4738 / 0.0578 | 5.0812 / 0.0459 | 3.5321 / 0.0316 | 21 / 8 | 三者共有 |
| 28276 | 0.0000 / 0.0000 | 4.0583 / 0.0367 | 0.0000 / 0.0000 | 33 / 61 | 细类换入 |


## 家具 · MLP输入 · N004

规则：first_confirmation；场景簇partial_visibility；Q粗−细差-0.442pp。标签顺序['furniture', 'chair', 'sofa']，读取冒号索引[25, 23, 23]，全向量L2=[111.4401, 112.5097, 112.315]。父→两细类交集[28, 28]；同父细类交集25。

```text
A curtain briefly exposed a picture of a piece of furniture before closing again. The viewer is trying to describe the subject.
Description:
```

```text
A curtain briefly exposed a picture of a chair before closing again. The viewer is trying to describe the subject.
Description:
```

```text
A curtain briefly exposed a picture of a sofa before closing again. The viewer is trying to describe the subject.
Description:
```

| ID | 父z / q | 细1z / q | 细2z / q | Q / G次数 | 本例成员 |
| --- | --- | --- | --- | --- | --- |
| 13110 | 4.7764 / 0.0429 | 0.0000 / 0.0000 | 3.8434 / 0.0342 | 9 / 44 | 父子保留／分支变化 |
| 14913 | 2.7316 / 0.0245 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 1293 / 1852 | 父类退出 |
| 13262 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 3.7177 / 0.0331 | 0 / 37 | 细类换入 |
| 27076 | 2.7499 / 0.0247 | 0.0000 / 0.0000 | 3.6823 / 0.0328 | 242 / 1097 | 父子保留／分支变化 |
| 27101 | 2.9293 / 0.0263 | 3.4329 / 0.0305 | 0.0000 / 0.0000 | 3 / 10 | 父子保留／分支变化 |
| 29886 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 3.2715 / 0.0291 | 3 / 127 | 细类换入 |
| 4740 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 3.2420 / 0.0289 | 0 / 2 | 细类换入 |
| 10167 | 2.8679 / 0.0257 | 3.0860 / 0.0274 | 0.0000 / 0.0000 | 1 / 23 | 父子保留／分支变化 |
| 27974 | 0.0000 / 0.0000 | 2.9835 / 0.0265 | 0.0000 / 0.0000 | 58 / 85 | 细类换入 |
| 24428 | 2.8728 / 0.0258 | 2.9293 / 0.0260 | 0.0000 / 0.0000 | 22 / 5 | 父子保留／分支变化 |
| 8856 | 4.3985 / 0.0395 | 6.1479 / 0.0546 | 3.2436 / 0.0289 | 5358 / 4904 | 三者共有 |
| 24871 | 0.0000 / 0.0000 | 2.8747 / 0.0256 | 0.0000 / 0.0000 | 4 / 58 | 细类换入 |


## 家具 · MLP输入 · N005

规则：median_D_Q；场景簇partial_visibility；Q粗−细差+3.240pp。标签顺序['furniture', 'chair', 'sofa']，读取冒号索引[25, 23, 23]，全向量L2=[111.0625, 113.6307, 111.3874]。父→两细类交集[28, 28]；同父细类交集27。

```text
Through a small opening in an envelope, someone recognized a piece of furniture in the photograph. The accompanying message was hidden.
Description:
```

```text
Through a small opening in an envelope, someone recognized a chair in the photograph. The accompanying message was hidden.
Description:
```

```text
Through a small opening in an envelope, someone recognized a sofa in the photograph. The accompanying message was hidden.
Description:
```

| ID | 父z / q | 细1z / q | 细2z / q | Q / G次数 | 本例成员 |
| --- | --- | --- | --- | --- | --- |
| 21807 | 3.1007 / 0.0279 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 9 / 41 | 父类退出 |
| 14187 | 0.0000 / 0.0000 | 2.7540 / 0.0242 | 3.0264 / 0.0272 | 132 / 1645 | 细类换入 |
| 27007 | 2.6066 / 0.0235 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 67 / 35 | 父类退出 |
| 8758 | 3.7577 / 0.0338 | 2.7656 / 0.0243 | 0.0000 / 0.0000 | 83 / 447 | 父子保留／分支变化 |
| 11234 | 3.1617 / 0.0285 | 0.0000 / 0.0000 | 3.8188 / 0.0343 | 4347 / 3699 | 父子保留／分支变化 |
| 15844 | 3.1849 / 0.0287 | 2.7057 / 0.0238 | 0.0000 / 0.0000 | 5 / 381 | 父子保留／分支变化 |
| 10013 | 0.0000 / 0.0000 | 3.2870 / 0.0289 | 0.0000 / 0.0000 | 96 / 503 | 细类换入 |
| 14913 | 2.8698 / 0.0258 | 0.0000 / 0.0000 | 3.1937 / 0.0287 | 1293 / 1852 | 父子保留／分支变化 |
| 4700 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 2.9596 / 0.0266 | 4684 / 632 | 细类换入 |
| 29886 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 2.9567 / 0.0265 | 3 / 127 | 细类换入 |
| 8351 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 2.6902 / 0.0242 | 17 / 2811 | 细类换入 |
| 3700 | 0.0000 / 0.0000 | 2.6218 / 0.0231 | 0.0000 / 0.0000 | 1 / 44 | 细类换入 |


## 家具 · MLP输入 · N039

规则：minimum_D_Q；场景簇image_reconstruction；Q粗−细差-4.685pp。标签顺序['furniture', 'chair', 'sofa']，读取冒号索引[27, 25, 25]，全向量L2=[113.9959, 113.8416, 111.1953]。父→两细类交集[29, 27]；同父细类交集25。

```text
Only the subject, a piece of furniture, was preserved in the instructions for a lost picture. The artist needs more explanatory wording.
Description:
```

```text
Only the subject, a chair, was preserved in the instructions for a lost picture. The artist needs more explanatory wording.
Description:
```

```text
Only the subject, a sofa, was preserved in the instructions for a lost picture. The artist needs more explanatory wording.
Description:
```

| ID | 父z / q | 细1z / q | 细2z / q | Q / G次数 | 本例成员 |
| --- | --- | --- | --- | --- | --- |
| 13110 | 6.3252 / 0.0555 | 0.0000 / 0.0000 | 7.1703 / 0.0645 | 9 / 44 | 父子保留／分支变化 |
| 14753 | 0.0000 / 0.0000 | 3.4130 / 0.0300 | 3.3037 / 0.0297 | 3163 / 213 | 细类换入 |
| 29506 | 28.6690 / 0.2515 | 26.8395 / 0.2358 | 23.7672 / 0.2137 | 4677 / 5864 | 三者共有 |
| 8758 | 4.7896 / 0.0420 | 0.0000 / 0.0000 | 5.1416 / 0.0462 | 83 / 447 | 父子保留／分支变化 |
| 25748 | 3.0839 / 0.0271 | 4.3673 / 0.0384 | 0.0000 / 0.0000 | 72 / 8 | 父子保留／分支变化 |
| 5196 | 3.6201 / 0.0318 | 3.0981 / 0.0272 | 0.0000 / 0.0000 | 5097 / 4610 | 父子保留／分支变化 |
| 16905 | 3.0342 / 0.0266 | 4.0122 / 0.0352 | 0.0000 / 0.0000 | 131 / 244 | 父子保留／分支变化 |
| 18245 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 3.8685 / 0.0348 | 21 / 221 | 细类换入 |
| 729 | 3.5636 / 0.0313 | 3.3650 / 0.0296 | 0.0000 / 0.0000 | 29 / 25 | 父子保留／分支变化 |
| 11234 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 3.4342 / 0.0309 | 4347 / 3699 | 细类换入 |
| 12027 | 3.1257 / 0.0274 | 3.3777 / 0.0297 | 0.0000 / 0.0000 | 2 / 1 | 父子保留／分支变化 |
| 16240 | 6.8775 / 0.0603 | 5.1309 / 0.0451 | 5.1515 / 0.0463 | 5801 / 4833 | 三者共有 |


## 衣物 · MLP输入 · N004

规则：first_confirmation；场景簇partial_visibility；Q粗−细差+14.392pp。标签顺序['clothing', 'shirt', 'trousers']，读取冒号索引[25, 23, 25]，全向量L2=[108.0263, 110.5399, 112.5147]。父→两细类交集[26, 24]；同父细类交集27。

```text
A curtain briefly exposed a picture of an item of clothing before closing again. The viewer is trying to describe the subject.
Description:
```

```text
A curtain briefly exposed a picture of a shirt before closing again. The viewer is trying to describe the subject.
Description:
```

```text
A curtain briefly exposed a picture of a pair of trousers before closing again. The viewer is trying to describe the subject.
Description:
```

| ID | 父z / q | 细1z / q | 细2z / q | Q / G次数 | 本例成员 |
| --- | --- | --- | --- | --- | --- |
| 2260 | 0.0000 / 0.0000 | 3.4998 / 0.0317 | 4.6270 / 0.0411 | 48 / 596 | 细类换入 |
| 15123 | 0.0000 / 0.0000 | 3.4053 / 0.0308 | 4.4962 / 0.0400 | 44 / 1630 | 细类换入 |
| 18245 | 10.1066 / 0.0936 | 6.5824 / 0.0595 | 6.5594 / 0.0583 | 21 / 221 | 三者共有 |
| 16240 | 11.9259 / 0.1104 | 9.3222 / 0.0843 | 8.0462 / 0.0715 | 5801 / 4833 | 三者共有 |
| 29893 | 3.4776 / 0.0322 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 2292 / 430 | 父类退出 |
| 16905 | 0.0000 / 0.0000 | 3.1100 / 0.0281 | 3.8436 / 0.0342 | 131 / 244 | 细类换入 |
| 8917 | 3.2699 / 0.0303 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 10 / 22 | 父类退出 |
| 2189 | 0.0000 / 0.0000 | 2.9116 / 0.0263 | 3.3229 / 0.0295 | 429 / 773 | 细类换入 |
| 340 | 3.0100 / 0.0279 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 1 / 8 | 父类退出 |
| 4740 | 2.9951 / 0.0277 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 0 / 2 | 父类退出 |
| 1683 | 2.8740 / 0.0266 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 18 / 39 | 父类退出 |
| 29342 | 48.0883 / 0.4452 | 51.3549 / 0.4646 | 53.7240 / 0.4775 | 6000 / 6000 | 三者共有 |


## 衣物 · MLP输入 · N047

规则：median_D_Q；场景簇identification_without_object；Q粗−细差+7.043pp。标签顺序['clothing', 'shirt', 'trousers']，读取冒号索引[27, 25, 27]，全向量L2=[107.984, 106.8745, 106.8489]。父→两细类交集[27, 25]；同父细类交集24。

```text
No object was brought into the room; the written cue simply refers to an item of clothing. The exercise calls for a description.
Description:
```

```text
No object was brought into the room; the written cue simply refers to a shirt. The exercise calls for a description.
Description:
```

```text
No object was brought into the room; the written cue simply refers to a pair of trousers. The exercise calls for a description.
Description:
```

| ID | 父z / q | 细1z / q | 细2z / q | Q / G次数 | 本例成员 |
| --- | --- | --- | --- | --- | --- |
| 5300 | 3.6635 / 0.0339 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 0 / 17 | 父类退出 |
| 18245 | 13.4553 / 0.1246 | 10.2163 / 0.0956 | 9.8793 / 0.0925 | 21 / 221 | 三者共有 |
| 14913 | 0.0000 / 0.0000 | 2.8770 / 0.0269 | 3.2160 / 0.0301 | 1293 / 1852 | 细类换入 |
| 29479 | 2.9921 / 0.0277 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 468 / 267 | 父类退出 |
| 7186 | 5.0146 / 0.0464 | 0.0000 / 0.0000 | 4.1461 / 0.0388 | 1 / 8 | 父子保留／分支变化 |
| 22374 | 2.7974 / 0.0259 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 1 / 2 | 父类退出 |
| 22965 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 4.2582 / 0.0399 | 29 / 105 | 细类换入 |
| 17548 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 4.1517 / 0.0389 | 25 / 37 | 细类换入 |
| 8048 | 0.0000 / 0.0000 | 3.8163 / 0.0357 | 0.0000 / 0.0000 | 4481 / 4265 | 细类换入 |
| 11514 | 3.4289 / 0.0318 | 3.1769 / 0.0297 | 0.0000 / 0.0000 | 1 / 0 | 父子保留／分支变化 |
| 964 | 3.5592 / 0.0330 | 0.0000 / 0.0000 | 3.4624 / 0.0324 | 0 / 6 | 父子保留／分支变化 |
| 7258 | 3.5223 / 0.0326 | 3.5554 / 0.0333 | 0.0000 / 0.0000 | 1922 / 31 | 父子保留／分支变化 |


## 衣物 · MLP输入 · N050

规则：minimum_D_Q；场景簇annotation_boundary；Q粗−细差-2.581pp。标签顺序['clothing', 'shirt', 'trousers']，读取冒号索引[28, 26, 28]，全向量L2=[113.434, 112.6692, 114.2137]。父→两细类交集[25, 26]；同父细类交集27。

```text
The reader placed a bookmark at the mention of an item of clothing. On returning, the reader asked for the subject to be explained.
Description:
```

```text
The reader placed a bookmark at the mention of a shirt. On returning, the reader asked for the subject to be explained.
Description:
```

```text
The reader placed a bookmark at the mention of a pair of trousers. On returning, the reader asked for the subject to be explained.
Description:
```

| ID | 父z / q | 细1z / q | 细2z / q | Q / G次数 | 本例成员 |
| --- | --- | --- | --- | --- | --- |
| 47 | 8.4132 / 0.0742 | 4.9583 / 0.0440 | 2.8467 / 0.0249 | 4177 / 3417 | 三者共有 |
| 13535 | 0.0000 / 0.0000 | 3.5016 / 0.0311 | 4.3762 / 0.0383 | 50 / 81 | 细类换入 |
| 14753 | 0.0000 / 0.0000 | 3.3938 / 0.0301 | 3.3818 / 0.0296 | 3163 / 213 | 细类换入 |
| 14536 | 0.0000 / 0.0000 | 3.4828 / 0.0309 | 2.9139 / 0.0255 | 3709 / 2578 | 细类换入 |
| 18245 | 9.6575 / 0.0851 | 6.1101 / 0.0542 | 6.8455 / 0.0599 | 21 / 221 | 三者共有 |
| 18933 | 3.1659 / 0.0279 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 135 / 102 | 父类退出 |
| 29934 | 2.8964 / 0.0255 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 58 / 59 | 父类退出 |
| 16240 | 7.8121 / 0.0689 | 6.4863 / 0.0576 | 3.3586 / 0.0294 | 5801 / 4833 | 三者共有 |
| 12628 | 2.7871 / 0.0246 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 3 / 0 | 父类退出 |
| 8917 | 2.7020 / 0.0238 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 10 / 22 | 父类退出 |
| 416 | 2.6244 / 0.0231 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 1406 / 1275 | 父类退出 |
| 11887 | 3.9078 / 0.0345 | 0.0000 / 0.0000 | 3.0401 / 0.0266 | 170 / 13 | 父子保留／分支变化 |


## 乐器 · MLP输入 · N004

规则：first_confirmation；场景簇partial_visibility；Q粗−细差+18.270pp。标签顺序['instrument', 'piano', 'guitar']，读取冒号索引[24, 23, 23]，全向量L2=[111.2482, 114.7805, 114.4286]。父→两细类交集[28, 30]；同父细类交集30。

```text
A curtain briefly exposed a picture of a musical instrument before closing again. The viewer is trying to describe the subject.
Description:
```

```text
A curtain briefly exposed a picture of a piano before closing again. The viewer is trying to describe the subject.
Description:
```

```text
A curtain briefly exposed a picture of a guitar before closing again. The viewer is trying to describe the subject.
Description:
```

| ID | 父z / q | 细1z / q | 细2z / q | Q / G次数 | 本例成员 |
| --- | --- | --- | --- | --- | --- |
| 1683 | 2.8960 / 0.0260 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 18 / 39 | 父类退出 |
| 28842 | 0.0000 / 0.0000 | 2.5861 / 0.0225 | 2.7794 / 0.0243 | 15 / 146 | 细类换入 |
| 27076 | 0.0000 / 0.0000 | 2.5411 / 0.0221 | 2.7998 / 0.0245 | 242 / 1097 | 细类换入 |
| 29934 | 2.5825 / 0.0232 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 58 / 59 | 父类退出 |
| 1818 | 3.2968 / 0.0296 | 0.0000 / 0.0000 | 2.7768 / 0.0243 | 14 / 312 | 父子保留／分支变化 |
| 23110 | 3.3681 / 0.0303 | 0.0000 / 0.0000 | 2.9530 / 0.0258 | 21 / 76 | 父子保留／分支变化 |
| 16240 | 8.8507 / 0.0796 | 6.9774 / 0.0608 | 7.6320 / 0.0667 | 5801 / 4833 | 三者共有 |
| 15788 | 5.4641 / 0.0491 | 4.1602 / 0.0362 | 4.1639 / 0.0364 | 19 / 12 | 三者共有 |
| 12843 | 0.0000 / 0.0000 | 2.5973 / 0.0226 | 0.0000 / 0.0000 | 1 / 39 | 细类换入 |
| 4700 | 4.5941 / 0.0413 | 3.5018 / 0.0305 | 3.4026 / 0.0297 | 4684 / 632 | 三者共有 |
| 23121 | 0.0000 / 0.0000 | 2.5647 / 0.0223 | 0.0000 / 0.0000 | 2 / 22 | 细类换入 |
| 808 | 5.8577 / 0.0527 | 4.9292 / 0.0429 | 4.6780 / 0.0409 | 1132 / 418 | 三者共有 |


## 乐器 · MLP输入 · N030

规则：median_D_Q；场景簇catalogue_recovery；Q粗−细差+9.353pp。标签顺序['instrument', 'piano', 'guitar']，读取冒号索引[22, 21, 21]，全向量L2=[115.8387, 116.4076, 116.2117]。父→两细类交集[25, 26]；同父细类交集25。

```text
Someone found a miniature illustration of a musical instrument between two catalogue pages. The illustration has no readable description.
Description:
```

```text
Someone found a miniature illustration of a piano between two catalogue pages. The illustration has no readable description.
Description:
```

```text
Someone found a miniature illustration of a guitar between two catalogue pages. The illustration has no readable description.
Description:
```

| ID | 父z / q | 细1z / q | 细2z / q | Q / G次数 | 本例成员 |
| --- | --- | --- | --- | --- | --- |
| 23110 | 4.6558 / 0.0402 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 21 / 76 | 父类退出 |
| 19999 | 0.0000 / 0.0000 | 3.9875 / 0.0343 | 3.8405 / 0.0330 | 123 / 849 | 细类换入 |
| 11291 | 0.0000 / 0.0000 | 3.9216 / 0.0337 | 3.8160 / 0.0328 | 28 / 229 | 细类换入 |
| 28550 | 3.3335 / 0.0288 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 17 / 45 | 父类退出 |
| 21807 | 0.0000 / 0.0000 | 3.4944 / 0.0300 | 3.1388 / 0.0270 | 9 / 41 | 细类换入 |
| 4432 | 3.2477 / 0.0280 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 1 / 37 | 父类退出 |
| 1818 | 4.4505 / 0.0384 | 0.0000 / 0.0000 | 3.5797 / 0.0308 | 14 / 312 | 父子保留／分支变化 |
| 4700 | 3.8709 / 0.0334 | 3.0273 / 0.0260 | 0.0000 / 0.0000 | 4684 / 632 | 父子保留／分支变化 |
| 29506 | 20.4257 / 0.1763 | 18.9421 / 0.1627 | 17.5979 / 0.1514 | 4677 / 5864 | 三者共有 |
| 3371 | 3.5773 / 0.0309 | 0.0000 / 0.0000 | 3.1282 / 0.0269 | 79 / 104 | 父子保留／分支变化 |
| 5196 | 3.4623 / 0.0299 | 3.0792 / 0.0265 | 0.0000 / 0.0000 | 5097 / 4610 | 父子保留／分支变化 |
| 3011 | 3.5879 / 0.0310 | 3.4622 / 0.0297 | 0.0000 / 0.0000 | 35 / 244 | 父子保留／分支变化 |


## 乐器 · MLP输入 · N050

规则：minimum_D_Q；场景簇annotation_boundary；Q粗−细差-0.616pp。标签顺序['instrument', 'piano', 'guitar']，读取冒号索引[27, 26, 26]，全向量L2=[117.4165, 117.296, 115.3027]。父→两细类交集[25, 24]；同父细类交集27。

```text
The reader placed a bookmark at the mention of a musical instrument. On returning, the reader asked for the subject to be explained.
Description:
```

```text
The reader placed a bookmark at the mention of a piano. On returning, the reader asked for the subject to be explained.
Description:
```

```text
The reader placed a bookmark at the mention of a guitar. On returning, the reader asked for the subject to be explained.
Description:
```

| ID | 父z / q | 细1z / q | 细2z / q | Q / G次数 | 本例成员 |
| --- | --- | --- | --- | --- | --- |
| 11234 | 0.0000 / 0.0000 | 4.3683 / 0.0372 | 5.4649 / 0.0474 | 4347 / 3699 | 细类换入 |
| 1818 | 6.7463 / 0.0575 | 0.0000 / 0.0000 | 4.1203 / 0.0357 | 14 / 312 | 父子保留／分支变化 |
| 23110 | 4.5137 / 0.0384 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 21 / 76 | 父类退出 |
| 11887 | 3.6635 / 0.0312 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 170 / 13 | 父类退出 |
| 9524 | 3.6268 / 0.0309 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 11 / 7 | 父类退出 |
| 6963 | 0.0000 / 0.0000 | 2.9068 / 0.0248 | 3.9727 / 0.0345 | 11 / 219 | 细类换入 |
| 18614 | 3.3320 / 0.0284 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 10 / 107 | 父类退出 |
| 5196 | 0.0000 / 0.0000 | 3.8710 / 0.0330 | 2.5272 / 0.0219 | 5097 / 4610 | 细类换入 |
| 861 | 0.0000 / 0.0000 | 3.3118 / 0.0282 | 3.0687 / 0.0266 | 304 / 521 | 细类换入 |
| 23326 | 3.1529 / 0.0269 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 59 / 31 | 父类退出 |
| 12843 | 5.2760 / 0.0449 | 4.4221 / 0.0377 | 0.0000 / 0.0000 | 1 / 39 | 父子保留／分支变化 |
| 25309 | 2.8809 / 0.0245 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 255 / 54 | 父类退出 |


## 花 · MLP输入 · N004

规则：first_confirmation；场景簇partial_visibility；Q粗−细差-2.529pp。标签顺序['flower', 'rose', 'tulip']，读取冒号索引[23, 23, 24]，全向量L2=[111.72, 113.4294, 111.1629]。父→两细类交集[28, 26]；同父细类交集24。

```text
A curtain briefly exposed a picture of a flower before closing again. The viewer is trying to describe the subject.
Description:
```

```text
A curtain briefly exposed a picture of a rose before closing again. The viewer is trying to describe the subject.
Description:
```

```text
A curtain briefly exposed a picture of a tulip before closing again. The viewer is trying to describe the subject.
Description:
```

| ID | 父z / q | 细1z / q | 细2z / q | Q / G次数 | 本例成员 |
| --- | --- | --- | --- | --- | --- |
| 17369 | 3.5937 / 0.0322 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 20 / 26 | 父类退出 |
| 14913 | 3.0231 / 0.0271 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 1293 / 1852 | 父类退出 |
| 16440 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 5.2436 / 0.0472 | 11 / 20 | 细类换入 |
| 27974 | 3.9734 / 0.0356 | 3.0472 / 0.0269 | 0.0000 / 0.0000 | 58 / 85 | 父子保留／分支变化 |
| 16905 | 3.7472 / 0.0335 | 2.8103 / 0.0248 | 0.0000 / 0.0000 | 131 / 244 | 父子保留／分支变化 |
| 6888 | 0.0000 / 0.0000 | 4.7483 / 0.0419 | 0.0000 / 0.0000 | 43 / 52 | 细类换入 |
| 808 | 6.9149 / 0.0619 | 4.8550 / 0.0428 | 4.9176 / 0.0442 | 1132 / 418 | 三者共有 |
| 17390 | 10.8801 / 0.0974 | 9.8635 / 0.0870 | 8.0645 / 0.0725 | 4665 / 5371 | 三者共有 |
| 24871 | 2.7999 / 0.0251 | 0.0000 / 0.0000 | 3.7587 / 0.0338 | 4 / 58 | 父子保留／分支变化 |
| 27101 | 2.7707 / 0.0248 | 0.0000 / 0.0000 | 3.5064 / 0.0315 | 3 / 10 | 父子保留／分支变化 |
| 29934 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 3.3748 / 0.0304 | 58 / 59 | 细类换入 |
| 27005 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 3.3585 / 0.0302 | 22 / 40 | 细类换入 |


## 花 · MLP输入 · N060

规则：median_D_Q；场景簇rehearsal；Q粗−细差+5.363pp。标签顺序['flower', 'rose', 'tulip']，读取冒号索引[24, 24, 25]，全向量L2=[114.1947, 114.5105, 112.7015]。父→两细类交集[27, 23]；同父细类交集24。

```text
The rehearsal notes list a flower but omit what the speaker should say about it. That explanation must now be written.
Description:
```

```text
The rehearsal notes list a rose but omit what the speaker should say about it. That explanation must now be written.
Description:
```

```text
The rehearsal notes list a tulip but omit what the speaker should say about it. That explanation must now be written.
Description:
```

| ID | 父z / q | 细1z / q | 细2z / q | Q / G次数 | 本例成员 |
| --- | --- | --- | --- | --- | --- |
| 808 | 4.5678 / 0.0400 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 1132 / 418 | 父类退出 |
| 17369 | 3.9661 / 0.0347 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 20 / 26 | 父类退出 |
| 6888 | 0.0000 / 0.0000 | 7.6801 / 0.0671 | 0.0000 / 0.0000 | 43 / 52 | 细类换入 |
| 18933 | 0.0000 / 0.0000 | 3.3636 / 0.0294 | 2.9436 / 0.0261 | 135 / 102 | 细类换入 |
| 10900 | 3.0841 / 0.0270 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 21 / 7 | 父类退出 |
| 27038 | 2.9716 / 0.0260 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 17 / 25 | 父类退出 |
| 3487 | 2.9238 / 0.0256 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 82 / 29 | 父类退出 |
| 16440 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 5.2707 / 0.0468 | 11 / 20 | 细类换入 |
| 18620 | 8.4349 / 0.0739 | 6.1834 / 0.0540 | 5.8829 / 0.0522 | 11 / 18 | 三者共有 |
| 17390 | 7.4616 / 0.0653 | 5.3949 / 0.0471 | 4.9180 / 0.0436 | 4665 / 5371 | 三者共有 |
| 10580 | 4.1143 / 0.0360 | 3.7892 / 0.0331 | 0.0000 / 0.0000 | 93 / 116 | 父子保留／分支变化 |
| 8048 | 3.9380 / 0.0345 | 3.7087 / 0.0324 | 0.0000 / 0.0000 | 4481 / 4265 | 父子保留／分支变化 |


## 花 · MLP输入 · N015

规则：minimum_D_Q；场景簇cropped_media；Q粗−细差-3.893pp。标签顺序['flower', 'rose', 'tulip']，读取冒号索引[23, 23, 24]，全向量L2=[95.0492, 96.8639, 96.763]。父→两细类交集[27, 21]；同父细类交集21。

```text
An image was separated from its surrounding article; it depicts a flower. The detached illustration needs an identifying description.
Description:
```

```text
An image was separated from its surrounding article; it depicts a rose. The detached illustration needs an identifying description.
Description:
```

```text
An image was separated from its surrounding article; it depicts a tulip. The detached illustration needs an identifying description.
Description:
```

| ID | 父z / q | 细1z / q | 细2z / q | Q / G次数 | 本例成员 |
| --- | --- | --- | --- | --- | --- |
| 808 | 4.3087 / 0.0453 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 1132 / 418 | 父类退出 |
| 23170 | 3.8840 / 0.0409 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 40 / 31 | 父类退出 |
| 16905 | 3.7914 / 0.0399 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 131 / 244 | 父类退出 |
| 6888 | 0.0000 / 0.0000 | 7.6226 / 0.0787 | 0.0000 / 0.0000 | 43 / 52 | 细类换入 |
| 17369 | 3.7286 / 0.0392 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 20 / 26 | 父类退出 |
| 20822 | 3.3374 / 0.0351 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 0 / 3 | 父类退出 |
| 29893 | 4.5634 / 0.0480 | 3.5634 / 0.0368 | 0.0000 / 0.0000 | 2292 / 430 | 父子保留／分支变化 |
| 16440 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 5.6079 / 0.0580 | 11 / 20 | 细类换入 |
| 9139 | 3.9790 / 0.0419 | 4.3846 / 0.0453 | 0.0000 / 0.0000 | 5 / 5 | 父子保留／分支变化 |
| 24428 | 3.6655 / 0.0386 | 3.9024 / 0.0403 | 0.0000 / 0.0000 | 22 / 5 | 父子保留／分支变化 |
| 862 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 3.8067 / 0.0393 | 41 / 116 | 细类换入 |
| 14536 | 0.0000 / 0.0000 | 3.7615 / 0.0388 | 0.0000 / 0.0000 | 3709 / 2578 | 细类换入 |


## 餐用器具 · MLP输入 · N004

规则：first_confirmation；场景簇partial_visibility；Q粗−细差-3.249pp。标签顺序['cutlery', 'spoon', 'fork']，读取冒号索引[27, 23, 23]，全向量L2=[112.1586, 112.9681, 111.6811]。父→两细类交集[24, 25]；同父细类交集26。

```text
A curtain briefly exposed a picture of a piece of cutlery before closing again. The viewer is trying to describe the subject.
Description:
```

```text
A curtain briefly exposed a picture of a spoon before closing again. The viewer is trying to describe the subject.
Description:
```

```text
A curtain briefly exposed a picture of a fork before closing again. The viewer is trying to describe the subject.
Description:
```

| ID | 父z / q | 细1z / q | 细2z / q | Q / G次数 | 本例成员 |
| --- | --- | --- | --- | --- | --- |
| 5196 | 0.0000 / 0.0000 | 4.0305 / 0.0357 | 3.6924 / 0.0331 | 5097 / 4610 | 细类换入 |
| 729 | 0.0000 / 0.0000 | 2.9782 / 0.0264 | 3.4007 / 0.0305 | 29 / 25 | 细类换入 |
| 27101 | 0.0000 / 0.0000 | 3.0208 / 0.0267 | 3.1991 / 0.0286 | 3 / 10 | 细类换入 |
| 15160 | 3.0102 / 0.0268 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 4 / 9 | 父类退出 |
| 10580 | 0.0000 / 0.0000 | 3.1446 / 0.0278 | 2.8528 / 0.0255 | 93 / 116 | 细类换入 |
| 18245 | 2.9151 / 0.0260 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 21 / 221 | 父类退出 |
| 1683 | 2.8889 / 0.0258 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 18 / 39 | 父类退出 |
| 2491 | 0.0000 / 0.0000 | 2.9233 / 0.0259 | 2.7374 / 0.0245 | 13 / 30 | 细类换入 |
| 10024 | 2.7388 / 0.0244 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 57 / 21 | 父类退出 |
| 29188 | 3.4590 / 0.0308 | 0.0000 / 0.0000 | 2.7385 / 0.0245 | 2 / 10 | 父子保留／分支变化 |
| 13262 | 3.0484 / 0.0272 | 3.6171 / 0.0320 | 0.0000 / 0.0000 | 0 / 37 | 父子保留／分支变化 |
| 14202 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 3.5661 / 0.0319 | 5 / 62 | 细类换入 |


## 餐用器具 · MLP输入 · N050

规则：median_D_Q；场景簇annotation_boundary；Q粗−细差+1.719pp。标签顺序['cutlery', 'spoon', 'fork']，读取冒号索引[30, 26, 26]，全向量L2=[116.2388, 114.9801, 114.4332]。父→两细类交集[23, 21]；同父细类交集25。

```text
The reader placed a bookmark at the mention of a piece of cutlery. On returning, the reader asked for the subject to be explained.
Description:
```

```text
The reader placed a bookmark at the mention of a spoon. On returning, the reader asked for the subject to be explained.
Description:
```

```text
The reader placed a bookmark at the mention of a fork. On returning, the reader asked for the subject to be explained.
Description:
```

| ID | 父z / q | 细1z / q | 细2z / q | Q / G次数 | 本例成员 |
| --- | --- | --- | --- | --- | --- |
| 5196 | 0.0000 / 0.0000 | 5.9348 / 0.0516 | 5.4174 / 0.0473 | 5097 / 4610 | 细类换入 |
| 47 | 0.0000 / 0.0000 | 3.9159 / 0.0341 | 7.1105 / 0.0621 | 4177 / 3417 | 细类换入 |
| 20681 | 3.6417 / 0.0313 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 0 / 0 | 父类退出 |
| 27881 | 0.0000 / 0.0000 | 3.1018 / 0.0270 | 3.7995 / 0.0332 | 325 / 619 | 细类换入 |
| 861 | 3.3251 / 0.0286 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 304 / 521 | 父类退出 |
| 23326 | 0.0000 / 0.0000 | 3.2518 / 0.0283 | 3.0804 / 0.0269 | 59 / 31 | 细类换入 |
| 15160 | 3.0857 / 0.0265 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 4 / 9 | 父类退出 |
| 11887 | 3.0842 / 0.0265 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 170 / 13 | 父类退出 |
| 27038 | 0.0000 / 0.0000 | 3.2854 / 0.0286 | 2.7421 / 0.0240 | 17 / 25 | 细类换入 |
| 27581 | 7.9570 / 0.0685 | 6.2116 / 0.0540 | 3.5627 / 0.0311 | 427 / 359 | 三者共有 |
| 27346 | 2.9926 / 0.0257 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 326 / 1285 | 父类退出 |
| 14187 | 2.7045 / 0.0233 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 132 / 1645 | 父类退出 |


## 餐用器具 · MLP输入 · N054

规则：minimum_D_Q；场景簇remote_collaboration；Q粗−细差-13.313pp。标签顺序['cutlery', 'spoon', 'fork']，读取冒号索引[23, 19, 19]，全向量L2=[107.4032, 108.1287, 111.202]。父→两细类交集[27, 19]；同父细类交集19。

```text
The connection failed after the presenter named a piece of cutlery. The remaining participants requested a text description.
Description:
```

```text
The connection failed after the presenter named a spoon. The remaining participants requested a text description.
Description:
```

```text
The connection failed after the presenter named a fork. The remaining participants requested a text description.
Description:
```

| ID | 父z / q | 细1z / q | 细2z / q | Q / G次数 | 本例成员 |
| --- | --- | --- | --- | --- | --- |
| 16240 | 13.5514 / 0.1262 | 16.1916 / 0.1497 | 32.0664 / 0.2884 | 5801 / 4833 | 三者共有 |
| 27076 | 6.7070 / 0.0624 | 2.6398 / 0.0244 | 0.0000 / 0.0000 | 242 / 1097 | 父子保留／分支变化 |
| 27581 | 8.1237 / 0.0756 | 6.9882 / 0.0646 | 0.0000 / 0.0000 | 427 / 359 | 父子保留／分支变化 |
| 20681 | 5.7787 / 0.0538 | 3.4239 / 0.0317 | 0.0000 / 0.0000 | 0 / 0 | 父子保留／分支变化 |
| 729 | 3.9000 / 0.0363 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 29 / 25 | 父类退出 |
| 28240 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 7.7937 / 0.0701 | 7 / 194 | 细类换入 |
| 8856 | 7.9822 / 0.0743 | 10.9117 / 0.1009 | 13.0693 / 0.1175 | 5358 / 4904 | 三者共有 |
| 47 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 7.6386 / 0.0687 | 4177 / 3417 | 细类换入 |
| 10580 | 3.4353 / 0.0320 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 93 / 116 | 父类退出 |
| 5554 | 0.0000 / 0.0000 | 2.7296 / 0.0252 | 3.8181 / 0.0343 | 100 / 89 | 细类换入 |
| 14481 | 80.4678 / 0.7492 | 80.8982 / 0.7482 | 77.2828 / 0.6950 | 6000 / 6000 | 三者共有 |
| 11697 | 2.8296 / 0.0263 | 0.0000 / 0.0000 | 0.0000 / 0.0000 | 3 / 21 | 父类退出 |
