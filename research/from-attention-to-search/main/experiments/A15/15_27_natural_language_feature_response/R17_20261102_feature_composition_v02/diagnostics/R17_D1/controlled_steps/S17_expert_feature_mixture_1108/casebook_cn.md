# S17实际输入、反例与不可识别案例

同一缓存实际测量，不是新文本。相似/低相似案例由DEV冻结候选与首个满足激活条件的CONF记录决定，不按路由挑选；N029/N051例外按用户指定家族核验后各取首条。专家编号零起算，坐标不擅自命名为语义。

## 1. both_same_token：S13_N004_explicit_cat

家族N004，场景partial_visibility，row=289；末冒号ID25、零起索引23。

```text
A curtain briefly exposed a picture of a cat before closing again. The viewer is trying to describe the subject.
Description:
```

| expert | 实际gate |
| --- | ---: |
| 6 | 0.599432 |
| 1 | 0.400568 |

| SAE坐标 | 正Top32后激活 |
| --- | ---: |
| #3460 | 3.599174 |
| #21462 | 1.525634 |

相对平方重建误差=0.203594。

读取：两成员同token共路由是结构事实，不是独立分工证据。

## 2. f_only_token：S13_N004_explicit_animal

家族N004，场景partial_visibility，row=288；末冒号ID25、零起索引23。

```text
A curtain briefly exposed a picture of an animal before closing again. The viewer is trying to describe the subject.
Description:
```

| expert | 实际gate |
| --- | ---: |
| 6 | 0.589090 |
| 1 | 0.410910 |

| SAE坐标 | 正Top32后激活 |
| --- | ---: |
| #16852 | 1.740881 |
| #21724 | 0.000000 |

相对平方重建误差=0.214298。

读取：与另一条不同token案例对应。各自活跃坐标不同，但实际专家组合仍可相同；这直接检查用户所设的激活分离准则，不能证明学习损害。

## 3. g_only_different_token：S13_N026_explicit_cat

家族N026，场景translation_gap，row=2401；末冒号ID25、零起索引24。

```text
The interpreter understood that the speaker meant a cat, but the listener still needed an explanation. A description is requested.
Description:
```

| expert | 实际gate |
| --- | ---: |
| 6 | 0.611598 |
| 1 | 0.388401 |

| SAE坐标 | 正Top32后激活 |
| --- | ---: |
| #16852 | 0.000000 |
| #21724 | 1.770437 |

相对平方重建误差=0.232225。

读取：与另一条不同token案例对应。各自活跃坐标不同，但实际专家组合仍可相同；这直接检查用户所设的激活分离准则，不能证明学习损害。

## 4. exception_context_not_expert_specialization：S13_N029_explicit_animal

家族N029，场景catalogue_recovery，row=2688；末冒号ID25、零起索引25。

```text
The collection database lost the text attached to an animal, although its image was preserved. A curator is repairing the entry.
Description:
```

| expert | 实际gate |
| --- | ---: |
| 6 | 0.723128 |
| 7 | 0.276872 |

| SAE坐标 | 正Top32后激活 |
| --- | ---: |
| #6289 | 0.000000 |
| #21724 | 0.000000 |

相对平方重建误差=0.194736。

读取：该expert例外出现在特定上下文。专家7总共只有23位置、2场景，本例不足以称为它的稳定语义专长。

## 5. exception_context_not_expert_specialization：S13_N051_explicit_fork

家族N051，场景annotation_boundary，row=4823；末冒号ID25、零起索引23。

```text
A highlighted phrase denotes a fork, but its glossary field is empty. The field requires a plain description.
Description:
```

| expert | 实际gate |
| --- | ---: |
| 6 | 0.770887 |
| 7 | 0.229113 |

| SAE坐标 | 正Top32后激活 |
| --- | ---: |
| #6289 | 0.000000 |
| #21724 | 2.694451 |

相对平方重建误差=0.246600。

读取：该expert例外出现在特定上下文。专家7总共只有23位置、2场景，本例不足以称为它的稳定语义专长。

## 不可判定案例：expert6的“偏好”

主条件expert6收到全部1152位置。因此对任何观察成员，P(feature|expert6)=输入出现率，差为0。这是同一数据集的恒等关系，缺少expert6未入选的对照。它既不证明该feature不起作用，也不说明expert6专门偏好这些feature。
