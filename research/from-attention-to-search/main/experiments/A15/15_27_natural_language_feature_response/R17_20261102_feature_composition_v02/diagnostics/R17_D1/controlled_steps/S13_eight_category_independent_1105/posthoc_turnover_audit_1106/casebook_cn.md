# 原始支持与反向案例

固定S11 MLP DEV权重前三、首CONF家族F001；不按确认频率挑ID。频率分母均6000；每侧入选数分母64。

## 猫–狗

### animal__vehicle

A，末冒号索引19：

```text
A caption writer received a request to describe an animal. The request was assigned a number.
Description:
```

B，索引19：

```text
A caption writer received a request to describe a vehicle. The request was assigned a number.
Description:
```

| ID | DEV权重 | A/B入选次数 | A/B原始z | Q% / G% | A/B截断前响应 | A/B第32名阈值 | 更替质量K |
|---|---|---|---|---|---|---|---|
| 20696 | 0.05498 | 0/64，63/64 | 0.0000，17.5917 | 3.133 / 4.850 | -2.3354，17.5917 | 3.0294，2.9565 | 21.62% |
| 24399 | 0.05498 | 64/64，0/64 | 9.6904，0.0000 | 1.817 / 3.800 | 9.6904，-1.2701 | 3.0294，2.9565 | 22.09% |
| 17366 | 0.05326 | 62/64，1/64 | 8.2240，0.0000 | 1.250 / 1.783 | 8.2240，1.1270 | 3.0294，2.9565 | 19.86% |

F001两侧都入选的成员在这一配对的更替质量为0，即使跨64家族净入选率不同。截断前响应不是模型功能贡献。

### cat__dog

A，末冒号索引19：

```text
A caption writer received a request to describe a cat. The request was assigned a number.
Description:
```

B，索引19：

```text
A caption writer received a request to describe a dog. The request was assigned a number.
Description:
```

| ID | DEV权重 | A/B入选次数 | A/B原始z | Q% / G% | A/B截断前响应 | A/B第32名阈值 | 更替质量K |
|---|---|---|---|---|---|---|---|
| 22958 | 0.11567 | 64/64，0/64 | 9.6743，0.0000 | 0.433 / 0.850 | 9.6743，0.6438 | 3.2339，3.1774 | 69.10% |
| 10580 | 0.04478 | 24/64，9/64 | 3.3168，0.0000 | 1.550 / 1.933 | 3.3168，1.6999 | 3.2339，3.1774 | 4.85% |
| 11234 | 0.02612 | 57/64，42/64 | 4.5216，0.0000 | 72.450 / 61.650 | 4.5216，1.1777 | 3.2339，3.1774 | 3.12% |

F001两侧都入选的成员在这一配对的更替质量为0，即使跨64家族净入选率不同。截断前响应不是模型功能贡献。

## 汽车–自行车

### animal__vehicle

A，末冒号索引19：

```text
A caption writer received a request to describe an animal. The request was assigned a number.
Description:
```

B，索引19：

```text
A caption writer received a request to describe a vehicle. The request was assigned a number.
Description:
```

| ID | DEV权重 | A/B入选次数 | A/B原始z | Q% / G% | A/B截断前响应 | A/B第32名阈值 | 更替质量K |
|---|---|---|---|---|---|---|---|
| 20696 | 0.05498 | 0/64，63/64 | 0.0000，17.5917 | 3.133 / 4.850 | -2.3354，17.5917 | 3.0294，2.9565 | 21.62% |
| 24399 | 0.05498 | 64/64，0/64 | 9.6904，0.0000 | 1.817 / 3.800 | 9.6904，-1.2701 | 3.0294，2.9565 | 22.09% |
| 17366 | 0.05326 | 62/64，1/64 | 8.2240，0.0000 | 1.250 / 1.783 | 8.2240，1.1270 | 3.0294，2.9565 | 19.86% |

F001两侧都入选的成员在这一配对的更替质量为0，即使跨64家族净入选率不同。截断前响应不是模型功能贡献。

### car__bicycle

A，末冒号索引19：

```text
A caption writer received a request to describe a car. The request was assigned a number.
Description:
```

B，索引19：

```text
A caption writer received a request to describe a bicycle. The request was assigned a number.
Description:
```

| ID | DEV权重 | A/B入选次数 | A/B原始z | Q% / G% | A/B截断前响应 | A/B第32名阈值 | 更替质量K |
|---|---|---|---|---|---|---|---|
| 16830 | 0.07339 | 0/64，64/64 | 0.0000，12.3484 | 0.117 / 0.417 | -3.3346，12.3484 | 2.9359，2.9399 | 30.80% |
| 19178 | 0.06651 | 60/64，0/64 | 4.4366，0.0000 | 2.350 / 1.383 | 4.4366，-1.5884 | 2.9359，2.9399 | 25.88% |
| 8048 | 0.04358 | 54/64，15/64 | 6.0073，0.0000 | 74.683 / 71.083 | 6.0073，2.9119 | 2.9359，2.9399 | 10.08% |

F001两侧都入选的成员在这一配对的更替质量为0，即使跨64家族净入选率不同。截断前响应不是模型功能贡献。

## 椅子–沙发

### fruit__furniture

A，末冒号索引19：

```text
A caption writer received a request to describe a fruit. The request was assigned a number.
Description:
```

B，索引21：

```text
A caption writer received a request to describe a piece of furniture. The request was assigned a number.
Description:
```

| ID | DEV权重 | A/B入选次数 | A/B原始z | Q% / G% | A/B截断前响应 | A/B第32名阈值 | 更替质量K |
|---|---|---|---|---|---|---|---|
| 27581 | 0.04399 | 61/64，0/64 | 12.3100，0.0000 | 7.117 / 5.983 | 12.3100，1.5179 | 3.1693，3.2937 | 14.03% |
| 13110 | 0.04252 | 0/64，59/64 | 0.0000，12.9046 | 0.150 / 0.733 | -6.5145，12.9046 | 3.1693，3.2937 | 12.77% |
| 5836 | 0.04106 | 60/64，0/64 | 15.0332，0.0000 | 0.350 / 0.133 | 15.0332，-3.8712 | 3.1693，3.2937 | 12.78% |

F001两侧都入选的成员在这一配对的更替质量为0，即使跨64家族净入选率不同。截断前响应不是模型功能贡献。

### chair__sofa

A，末冒号索引19：

```text
A caption writer received a request to describe a chair. The request was assigned a number.
Description:
```

B，索引19：

```text
A caption writer received a request to describe a sofa. The request was assigned a number.
Description:
```

| ID | DEV权重 | A/B入选次数 | A/B原始z | Q% / G% | A/B截断前响应 | A/B第32名阈值 | 更替质量K |
|---|---|---|---|---|---|---|---|
| 18245 | 0.03846 | 8/64，53/64 | 3.6087，4.9996 | 0.350 / 3.683 | 3.6087，4.9996 | 3.2018，3.3817 | 16.19% |
| 13110 | 0.03077 | 14/64，46/64 | 5.5723，8.2104 | 0.150 / 0.733 | 5.5723，8.2104 | 3.2018，3.3817 | 8.07% |
| 14536 | 0.02692 | 55/64，36/64 | 5.6225，3.5324 | 61.817 / 42.967 | 5.6225，3.5324 | 3.2018，3.3817 | 3.72% |

F001两侧都入选的成员在这一配对的更替质量为0，即使跨64家族净入选率不同。截断前响应不是模型功能贡献。
