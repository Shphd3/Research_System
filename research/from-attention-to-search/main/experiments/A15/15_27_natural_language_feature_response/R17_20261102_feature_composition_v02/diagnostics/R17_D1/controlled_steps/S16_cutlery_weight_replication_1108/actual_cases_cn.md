# 新场景首个家族的实际输入与路由

按冻结排序取首个家族，不按路由挑案例；全部八个固定成员都展示。

## S16_C01_F1_explicit_spoon

```text
During the evening stock count, a spoon was placed in an empty drawer. The clerk recorded the object before closing the drawer.
Description:
```

末冒号ID25，零起索引26，长度27。

| expert | 实际gate权重 |
| --- | ---: |
| 6 | 0.637325 |
| 1 | 0.362675 |

| 成员角色 | 固定坐标 | Top32后激活值 |
| --- | ---: | ---: |
| A_bias | #8934 | 1.872882 |
| A_bias | #17384 | 0.000000 |
| A_bias | #23973 | 0.000000 |
| B_bias | #7438 | 0.000000 |
| B_bias | #15113 | 0.000000 |
| B_bias | #21724 | 0.000000 |
| B_bias | #25048 | 0.000000 |
| B_bias | #26926 | 0.000000 |

原始行号row=0；相对平方重建误差=0.246541。

## S16_C01_F1_explicit_fork

```text
During the evening stock count, a fork was placed in an empty drawer. The clerk recorded the object before closing the drawer.
Description:
```

末冒号ID25，零起索引26，长度27。

| expert | 实际gate权重 |
| --- | ---: |
| 6 | 0.655940 |
| 1 | 0.344060 |

| 成员角色 | 固定坐标 | Top32后激活值 |
| --- | ---: | ---: |
| A_bias | #8934 | 0.000000 |
| A_bias | #17384 | 0.000000 |
| A_bias | #23973 | 0.000000 |
| B_bias | #7438 | 1.763762 |
| B_bias | #15113 | 1.659642 |
| B_bias | #21724 | 0.000000 |
| B_bias | #25048 | 2.105810 |
| B_bias | #26926 | 0.000000 |

原始行号row=1；相对平方重建误差=0.243171。

同一token中的所有活跃成员承接同一份实际路由。单例中的权重差不是Q3：Q3须先逐成员跨其出现的所有文本平均，再对成员等权。0表示未进入正Top32，不代表preactivation为0。
