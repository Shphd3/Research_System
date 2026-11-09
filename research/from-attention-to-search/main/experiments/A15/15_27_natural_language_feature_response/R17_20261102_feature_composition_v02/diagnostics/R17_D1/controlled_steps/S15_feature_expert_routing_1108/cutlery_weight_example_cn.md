# 餐具权重的补充实际案例

该案例在权重结果可见后补充，仅为直观展示，选择显式CONF首个家族，不用于检验或选成员。全部冻结偏向成员均展示，包括未激活的0。

## S13_N004_explicit_spoon

```text
A curtain briefly exposed a picture of a spoon before closing again. The viewer is trying to describe the subject.
Description:
```

读取末冒号ID25，零起索引23；实际路由[(6, 0.61500084400177), (1, 0.38499915599823)]。

| 成员角色 | 坐标 | 实际激活 |
| --- | ---: | ---: |
| A_bias | #8934 | 1.951127 |
| A_bias | #17384 | 1.483981 |
| A_bias | #23973 | 0.000000 |
| B_bias | #7438 | 0.000000 |
| B_bias | #15113 | 0.000000 |
| B_bias | #21724 | 0.000000 |
| B_bias | #25048 | 0.000000 |
| B_bias | #26926 | 0.000000 |

完整逐位置原始表row=310，对应token_records.jsonl。

## S13_N004_explicit_fork

```text
A curtain briefly exposed a picture of a fork before closing again. The viewer is trying to describe the subject.
Description:
```

读取末冒号ID25，零起索引23；实际路由[(6, 0.6279764175415039), (1, 0.3720235824584961)]。

| 成员角色 | 坐标 | 实际激活 |
| --- | ---: | ---: |
| A_bias | #8934 | 0.000000 |
| A_bias | #17384 | 0.000000 |
| A_bias | #23973 | 0.000000 |
| B_bias | #7438 | 1.991124 |
| B_bias | #15113 | 1.549577 |
| B_bias | #21724 | 0.000000 |
| B_bias | #25048 | 0.000000 |
| B_bias | #26926 | 1.391342 |

完整逐位置原始表row=311，对应token_records.jsonl。

此例中的权重差不等于组指标Q3；Q3先逐成员跨所有确认文本求分布，再等权汇总。成员同token共路由，不能独立分发解释。
