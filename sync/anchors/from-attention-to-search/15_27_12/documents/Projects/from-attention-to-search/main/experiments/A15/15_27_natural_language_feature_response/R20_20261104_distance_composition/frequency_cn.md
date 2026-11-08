派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R20_20261104_distance_composition/frequency_cn.md`。
[精确原始文件](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R20_20261104_distance_composition/frequency_cn.md)；研究修改仍回到原件。

---

# 频率组：参与不等于重要性

| 字典 | 参考组 | 字典基数 | 本任务出现成员 | 位置/72 | 家族/12 |
|---|---|---|---|---|---|
| ATTN_SAE | high | 4377 | 136 | 72 | 12 |
| ATTN_SAE | middle | 4585 | 50 | 72 | 12 |
| ATTN_SAE | low | 4158 | 18 | 70 | 12 |
| ATTN_SAE | insufficient | 15579 | 33 | 72 | 12 |
| ATTN_SAE | zero | 1301 | 0 | 0 | 0 |
| MLPIN_SAE | high | 3429 | 63 | 72 | 12 |
| MLPIN_SAE | middle | 3503 | 30 | 72 | 12 |
| MLPIN_SAE | low | 3299 | 25 | 72 | 12 |
| MLPIN_SAE | insufficient | 19024 | 41 | 66 | 12 |
| MLPIN_SAE | zero | 745 | 1 | 29 | 8 |

| 字典 | 参考组 | 共同成员 | 换入 | 换出 | 参考期待换入 | 任务期待换入 | 绝对改变占比 |
|---|---|---|---|---|---|---|---|
| ATTN_SAE | high | 18.0833 | 4.3333 | 4.8333 | 4.4296 | 4.6206 | 0.6784 |
| ATTN_SAE | middle | 3.4167 | 1.4583 | 1.6250 | 1.3589 | 1.3934 | 0.1843 |
| ATTN_SAE | low | 1.4167 | 0.6250 | 0.4167 | 0.6670 | 0.5296 | 0.0614 |
| ATTN_SAE | insufficient | 1.8750 | 0.7917 | 0.3333 | 0.7528 | 0.6549 | 0.0759 |
| ATTN_SAE | zero | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0098 | 0.0000 |
| MLPIN_SAE | high | 19.1250 | 1.8333 | 1.7917 | 2.6430 | 2.2096 | 0.6217 |
| MLPIN_SAE | middle | 3.5417 | 0.7917 | 0.7083 | 0.5857 | 0.7774 | 0.1430 |
| MLPIN_SAE | low | 3.0000 | 0.7083 | 0.3750 | 0.3214 | 0.4021 | 0.0955 |
| MLPIN_SAE | insufficient | 1.9167 | 0.7083 | 1.1667 | 0.5333 | 0.6486 | 0.1327 |
| MLPIN_SAE | zero | 0.3333 | 0.0417 | 0.0417 | 0.0000 | 0.0457 | 0.0071 |

## 实际换入与换出的成员

| 字典 | 参考组 | 角色 | 按家族支持排序的真实ID/平均强度 |
|---|---|---|---|
| ATTN_SAE | high | entered | #12018: 8 families, mean z=2.3547; #3516: 4 families, mean z=2.1734 |
| ATTN_SAE | high | exited | #26496: 6 families, mean z=2.2935; #9560: 5 families, mean z=2.6187 |
| ATTN_SAE | middle | entered | #1086: 3 families, mean z=2.3444; #25257: 3 families, mean z=2.6773 |
| ATTN_SAE | middle | exited | #16694: 4 families, mean z=2.2591; #14700: 4 families, mean z=2.3062 |
| ATTN_SAE | low | entered | #17882: 5 families, mean z=2.1844; #5917: 2 families, mean z=2.0193 |
| ATTN_SAE | low | exited | #21601: 1 families, mean z=2.0012; #22224: 1 families, mean z=2.4762 |
| ATTN_SAE | insufficient | entered | #18234: 2 families, mean z=2.4620; #28277: 2 families, mean z=2.5989 |
| ATTN_SAE | insufficient | exited | #20347: 2 families, mean z=2.1341; #23436: 2 families, mean z=2.5525 |
| ATTN_SAE | zero | entered | none |
| ATTN_SAE | zero | exited | none |
| MLPIN_SAE | high | entered | #20289: 4 families, mean z=3.9177; #22309: 4 families, mean z=3.1865 |
| MLPIN_SAE | high | exited | #11234: 5 families, mean z=4.4193; #14536: 4 families, mean z=4.1165 |
| MLPIN_SAE | middle | entered | #11623: 2 families, mean z=3.6801; #5669: 2 families, mean z=3.0073 |
| MLPIN_SAE | middle | exited | #14578: 4 families, mean z=3.1288; #10580: 2 families, mean z=3.7158 |
| MLPIN_SAE | low | entered | #19579: 2 families, mean z=3.0824; #861: 1 families, mean z=2.7407 |
| MLPIN_SAE | low | exited | #3681: 2 families, mean z=2.9074; #1690: 1 families, mean z=2.9563 |
| MLPIN_SAE | insufficient | entered | #25748: 3 families, mean z=3.5119; #4324: 2 families, mean z=4.4100 |
| MLPIN_SAE | insufficient | exited | #7478: 3 families, mean z=3.2305; #11933: 2 families, mean z=2.7667 |
| MLPIN_SAE | zero | entered | #24506: 1 families, mean z=3.2948 |
| MLPIN_SAE | zero | exited | #24506: 1 families, mean z=3.3074 |


上表只为阅读，全部ID与每家族强度在执行侧feature_turnover_atlas.csv及*_member_values.csv，不据此重新选择组合。Attention高频换入均值4.33，参考期待4.43；MLP低频换入0.708，参考期待0.321、发现任务期待0.402，但家族区间跨零，不能宣称低频特别易换入。逐族机会、字典基数、旧活跃基数与旧排名四档匹配均保留；参考未出现组的零期待是未校准，不算无穷富集。高频绝对改变量占比大，不等于输出贡献、因果重要性或谱位置。
