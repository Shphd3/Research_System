派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_25_02_learning_history_representation/20261023/sample_cards.md`。
[精确原始文件](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_25_02_learning_history_representation/20261023/sample_cards.md)；研究修改仍回到原件。

---

# Measured sample cards: four fixed evaluation lists

Research question: How does learning history change conditional-rule representations, and which directions matter most for answering?

Take the first four sorted evaluation list IDs and retain both modes and commands, giving sixteen cards. First/last refer to list endpoints; other includes the middle word and every other vocabulary token. Probabilities are rounded for display; 100% is not a mathematical exact-one claim. Rank-16 retains the full sequential residual and adds a projection of this same input's mixed-minus-sequential difference.

## dev/old/甲/0-1-14

`模式：一。口令：甲。列表：红 黄 牛。答案：`

正确答案 / Correct answer: **红**.

| 状态 / State | 预测 / Prediction | P(first) | P(last) | P(other) |
|---|---|---:|---:|---:|
| 原始 Base / Original Base | `红` | 12.81071% | 11.67121% | 75.51808% |
| 学会 A / Learned A | `红` | 99.99979% | 0.00000% | 0.00021% |
| A 后只学 B / A then B | `牛` | 0.00000% | 99.99999% | 0.00001% |
| A 后混合学习 / A then mixed | `红` | 99.99990% | 0.00000% | 0.00009% |
| 顺序状态加 16 维变化 / Sequential + rank16 | `红` | 99.80678% | 0.00252% | 0.19070% |

## dev/old/乙/0-1-14

`模式：一。口令：乙。列表：红 黄 牛。答案：`

正确答案 / Correct answer: **牛**.

| 状态 / State | 预测 / Prediction | P(first) | P(last) | P(other) |
|---|---|---:|---:|---:|
| 原始 Base / Original Base | `红` | 13.20419% | 9.79384% | 77.00197% |
| 学会 A / Learned A | `牛` | 0.00000% | 100.00000% | 0.00000% |
| A 后只学 B / A then B | `红` | 99.99931% | 0.00022% | 0.00047% |
| A 后混合学习 / A then mixed | `牛` | 0.00000% | 100.00000% | 0.00000% |
| 顺序状态加 16 维变化 / Sequential + rank16 | `牛` | 0.00122% | 99.99877% | 0.00001% |

## dev/reversed/甲/0-1-14

`模式：二。口令：甲。列表：红 黄 牛。答案：`

正确答案 / Correct answer: **牛**.

| 状态 / State | 预测 / Prediction | P(first) | P(last) | P(other) |
|---|---|---:|---:|---:|
| 原始 Base / Original Base | `甲` | 10.58031% | 9.16686% | 80.25283% |
| 学会 A / Learned A | `红` | 99.99549% | 0.00000% | 0.00450% |
| A 后只学 B / A then B | `牛` | 0.00000% | 100.00000% | 0.00000% |
| A 后混合学习 / A then mixed | `牛` | 0.00000% | 100.00000% | 0.00000% |
| 顺序状态加 16 维变化 / Sequential + rank16 | `牛` | 0.00000% | 99.99999% | 0.00001% |

## dev/reversed/乙/0-1-14

`模式：二。口令：乙。列表：红 黄 牛。答案：`

正确答案 / Correct answer: **红**.

| 状态 / State | 预测 / Prediction | P(first) | P(last) | P(other) |
|---|---|---:|---:|---:|
| 原始 Base / Original Base | `红` | 11.13795% | 7.68768% | 81.17436% |
| 学会 A / Learned A | `牛` | 0.00000% | 100.00000% | 0.00000% |
| A 后只学 B / A then B | `红` | 99.99926% | 0.00021% | 0.00053% |
| A 后混合学习 / A then mixed | `红` | 99.99964% | 0.00002% | 0.00034% |
| 顺序状态加 16 维变化 / Sequential + rank16 | `红` | 99.99952% | 0.00001% | 0.00047% |

## dev/old/甲/0-1-17

`模式：一。口令：甲。列表：红 黄 虎。答案：`

正确答案 / Correct answer: **红**.

| 状态 / State | 预测 / Prediction | P(first) | P(last) | P(other) |
|---|---|---:|---:|---:|
| 原始 Base / Original Base | `虎` | 10.16945% | 23.17169% | 66.65887% |
| 学会 A / Learned A | `红` | 99.99989% | 0.00000% | 0.00011% |
| A 后只学 B / A then B | `虎` | 0.00000% | 100.00000% | 0.00000% |
| A 后混合学习 / A then mixed | `红` | 99.99983% | 0.00001% | 0.00015% |
| 顺序状态加 16 维变化 / Sequential + rank16 | `红` | 99.98236% | 0.00012% | 0.01752% |

## dev/old/乙/0-1-17

`模式：一。口令：乙。列表：红 黄 虎。答案：`

正确答案 / Correct answer: **虎**.

| 状态 / State | 预测 / Prediction | P(first) | P(last) | P(other) |
|---|---|---:|---:|---:|
| 原始 Base / Original Base | `虎` | 10.16211% | 22.41160% | 67.42628% |
| 学会 A / Learned A | `虎` | 0.00000% | 100.00000% | 0.00000% |
| A 后只学 B / A then B | `红` | 99.98474% | 0.01491% | 0.00035% |
| A 后混合学习 / A then mixed | `虎` | 0.00000% | 100.00000% | 0.00000% |
| 顺序状态加 16 维变化 / Sequential + rank16 | `虎` | 0.00001% | 99.99998% | 0.00001% |

## dev/reversed/甲/0-1-17

`模式：二。口令：甲。列表：红 黄 虎。答案：`

正确答案 / Correct answer: **虎**.

| 状态 / State | 预测 / Prediction | P(first) | P(last) | P(other) |
|---|---|---:|---:|---:|
| 原始 Base / Original Base | `虎` | 9.11319% | 16.89118% | 73.99564% |
| 学会 A / Learned A | `红` | 99.99890% | 0.00017% | 0.00092% |
| A 后只学 B / A then B | `虎` | 0.00000% | 100.00000% | 0.00000% |
| A 后混合学习 / A then mixed | `虎` | 0.00000% | 100.00000% | 0.00000% |
| 顺序状态加 16 维变化 / Sequential + rank16 | `虎` | 0.00000% | 99.99999% | 0.00001% |

## dev/reversed/乙/0-1-17

`模式：二。口令：乙。列表：红 黄 虎。答案：`

正确答案 / Correct answer: **红**.

| 状态 / State | 预测 / Prediction | P(first) | P(last) | P(other) |
|---|---|---:|---:|---:|
| 原始 Base / Original Base | `虎` | 9.27095% | 15.69597% | 75.03309% |
| 学会 A / Learned A | `虎` | 0.00000% | 100.00000% | 0.00000% |
| A 后只学 B / A then B | `红` | 99.99421% | 0.00560% | 0.00019% |
| A 后混合学习 / A then mixed | `红` | 99.99926% | 0.00064% | 0.00009% |
| 顺序状态加 16 维变化 / Sequential + rank16 | `红` | 99.99920% | 0.00026% | 0.00054% |

## dev/old/甲/0-1-16

`模式：一。口令：甲。列表：红 黄 羊。答案：`

正确答案 / Correct answer: **红**.

| 状态 / State | 预测 / Prediction | P(first) | P(last) | P(other) |
|---|---|---:|---:|---:|
| 原始 Base / Original Base | `红` | 12.97142% | 9.72109% | 77.30750% |
| 学会 A / Learned A | `红` | 99.99993% | 0.00000% | 0.00007% |
| A 后只学 B / A then B | `羊` | 0.00000% | 100.00000% | 0.00000% |
| A 后混合学习 / A then mixed | `红` | 99.99994% | 0.00000% | 0.00006% |
| 顺序状态加 16 维变化 / Sequential + rank16 | `红` | 99.94467% | 0.01386% | 0.04147% |

## dev/old/乙/0-1-16

`模式：一。口令：乙。列表：红 黄 羊。答案：`

正确答案 / Correct answer: **羊**.

| 状态 / State | 预测 / Prediction | P(first) | P(last) | P(other) |
|---|---|---:|---:|---:|
| 原始 Base / Original Base | `红` | 12.41687% | 8.20932% | 79.37381% |
| 学会 A / Learned A | `羊` | 0.00000% | 100.00000% | 0.00000% |
| A 后只学 B / A then B | `红` | 99.99965% | 0.00005% | 0.00029% |
| A 后混合学习 / A then mixed | `羊` | 0.00000% | 99.99999% | 0.00001% |
| 顺序状态加 16 维变化 / Sequential + rank16 | `羊` | 0.06512% | 99.93456% | 0.00032% |

## dev/reversed/甲/0-1-16

`模式：二。口令：甲。列表：红 黄 羊。答案：`

正确答案 / Correct answer: **羊**.

| 状态 / State | 预测 / Prediction | P(first) | P(last) | P(other) |
|---|---|---:|---:|---:|
| 原始 Base / Original Base | `红` | 10.76225% | 8.79555% | 80.44220% |
| 学会 A / Learned A | `红` | 99.99923% | 0.00000% | 0.00077% |
| A 后只学 B / A then B | `羊` | 0.00000% | 100.00000% | 0.00000% |
| A 后混合学习 / A then mixed | `羊` | 0.00000% | 99.99998% | 0.00002% |
| 顺序状态加 16 维变化 / Sequential + rank16 | `羊` | 0.00000% | 99.99990% | 0.00009% |

## dev/reversed/乙/0-1-16

`模式：二。口令：乙。列表：红 黄 羊。答案：`

正确答案 / Correct answer: **红**.

| 状态 / State | 预测 / Prediction | P(first) | P(last) | P(other) |
|---|---|---:|---:|---:|
| 原始 Base / Original Base | `红` | 10.59112% | 7.74186% | 81.66701% |
| 学会 A / Learned A | `羊` | 0.00000% | 100.00000% | 0.00000% |
| A 后只学 B / A then B | `红` | 99.99971% | 0.00004% | 0.00024% |
| A 后混合学习 / A then mixed | `红` | 99.99982% | 0.00000% | 0.00018% |
| 顺序状态加 16 维变化 / Sequential + rank16 | `红` | 99.99849% | 0.00000% | 0.00151% |

## dev/old/甲/0-1-10

`模式：一。口令：甲。列表：红 黄 猫。答案：`

正确答案 / Correct answer: **红**.

| 状态 / State | 预测 / Prediction | P(first) | P(last) | P(other) |
|---|---|---:|---:|---:|
| 原始 Base / Original Base | `红` | 13.35441% | 5.27455% | 81.37104% |
| 学会 A / Learned A | `红` | 99.99988% | 0.00001% | 0.00011% |
| A 后只学 B / A then B | `猫` | 0.00007% | 99.99864% | 0.00129% |
| A 后混合学习 / A then mixed | `红` | 99.99968% | 0.00028% | 0.00004% |
| 顺序状态加 16 维变化 / Sequential + rank16 | `红` | 99.95654% | 0.04039% | 0.00306% |

## dev/old/乙/0-1-10

`模式：一。口令：乙。列表：红 黄 猫。答案：`

正确答案 / Correct answer: **猫**.

| 状态 / State | 预测 / Prediction | P(first) | P(last) | P(other) |
|---|---|---:|---:|---:|
| 原始 Base / Original Base | `红` | 12.45949% | 5.18445% | 82.35607% |
| 学会 A / Learned A | `猫` | 0.00030% | 99.99911% | 0.00060% |
| A 后只学 B / A then B | `红` | 99.99996% | 0.00003% | 0.00001% |
| A 后混合学习 / A then mixed | `猫` | 0.00003% | 99.99944% | 0.00053% |
| 顺序状态加 16 维变化 / Sequential + rank16 | `猫` | 0.54278% | 99.45565% | 0.00157% |

## dev/reversed/甲/0-1-10

`模式：二。口令：甲。列表：红 黄 猫。答案：`

正确答案 / Correct answer: **猫**.

| 状态 / State | 预测 / Prediction | P(first) | P(last) | P(other) |
|---|---|---:|---:|---:|
| 原始 Base / Original Base | `红` | 11.03440% | 4.44186% | 84.52373% |
| 学会 A / Learned A | `红` | 99.99883% | 0.00004% | 0.00113% |
| A 后只学 B / A then B | `猫` | 0.00002% | 99.99875% | 0.00123% |
| A 后混合学习 / A then mixed | `猫` | 0.00004% | 99.99930% | 0.00067% |
| 顺序状态加 16 维变化 / Sequential + rank16 | `猫` | 0.00004% | 99.99938% | 0.00058% |

## dev/reversed/乙/0-1-10

`模式：二。口令：乙。列表：红 黄 猫。答案：`

正确答案 / Correct answer: **红**.

| 状态 / State | 预测 / Prediction | P(first) | P(last) | P(other) |
|---|---|---:|---:|---:|
| 原始 Base / Original Base | `红` | 10.38376% | 4.27089% | 85.34535% |
| 学会 A / Learned A | `猫` | 0.00024% | 99.99926% | 0.00050% |
| A 后只学 B / A then B | `红` | 99.99996% | 0.00002% | 0.00002% |
| A 后混合学习 / A then mixed | `红` | 99.99943% | 0.00056% | 0.00001% |
| 顺序状态加 16 维变化 / Sequential + rank16 | `红` | 99.99973% | 0.00025% | 0.00003% |

## An actual unrecovered example

This is the first lexicographic old-task rank-16 error, chosen only as a post-hoc failure illustration. It did not select directions.

`模式：一。口令：乙。列表：黄 龙 白。答案：`

Correct answer: **白**.

| 状态 / State | 预测 / Prediction | P(first) | P(last) | P(other) |
|---|---|---:|---:|---:|
| 原始 Base / Original Base | `乙` | 4.12870% | 7.17468% | 88.69661% |
| 学会 A / Learned A | `白` | 0.00092% | 99.99907% | 0.00001% |
| A 后只学 B / A then B | `黄` | 99.99857% | 0.00142% | 0.00001% |
| A 后混合学习 / A then mixed | `白` | 1.21871% | 98.70074% | 0.08054% |
| 顺序状态加 16 维变化 / Sequential + rank16 | `黄` | 99.98895% | 0.01088% | 0.00017% |

[Raw fixed sample cards](../../../../../../../../UNAVAILABLE.md) · [All evaluation intervention arrays](../../../../../../../../UNAVAILABLE.md)
