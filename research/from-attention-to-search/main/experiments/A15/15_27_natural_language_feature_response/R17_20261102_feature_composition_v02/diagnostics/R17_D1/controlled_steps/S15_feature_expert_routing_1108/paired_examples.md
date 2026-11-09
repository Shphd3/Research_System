# 实际输入与路由案例

这些是本轮确实前向的构造语言文本，不冒充自然网页或新独立确认。前四例按DEV成员清单及首个可展示CONF家族选取；反例是事后按“共享成员在两类均出现但组合不同”寻找的首例，不重新定义主检验。

专家编号零起算。SAE激活为原生Top32后的值；0仅表示未入选且正值为0，不代表未截断preactivation为0。路由作用于整个token，不是逐成员独立作决定。

## 1. 共享候选一：固定成员与两类实际路由

类别对：animal；家族：N004；成员：#3460。

### cat：S13_N004_explicit_cat

```text
A curtain briefly exposed a picture of a cat before closing again. The viewer is trying to describe the subject.
Description:
```

实际读取：冒号，token ID=25，零起索引=23；场景=partial_visibility。

| 成员 | 激活值 |
| --- | ---: |
| #3460 | 3.599174 |

| 实际expert | gate权重 | 原softmax概率 | load bias |
| --- | ---: | ---: | ---: |
| 6 | 0.599432 | 0.274827 | 2.390009 |
| 1 | 0.400568 | 0.183652 | 2.396009 |

输入重建相对平方误差=0.203594。完整8维logits、概率和原生hidden见observations索引。

### dog：S13_N004_explicit_dog

```text
A curtain briefly exposed a picture of a dog before closing again. The viewer is trying to describe the subject.
Description:
```

实际读取：冒号，token ID=25，零起索引=23；场景=partial_visibility。

| 成员 | 激活值 |
| --- | ---: |
| #3460 | 4.716168 |

| 实际expert | gate权重 | 原softmax概率 | load bias |
| --- | ---: | ---: | ---: |
| 6 | 0.583508 | 0.263823 | 2.390009 |
| 1 | 0.416492 | 0.188310 | 2.396009 |

输入重建相对平方误差=0.206794。完整8维logits、概率和原生hidden见observations索引。

**读取边界：** 此处同时活跃的成员共享这份token路由。专家组合相同不能证明分配正确或错误；组合不同也不能证明该共享成员应当被独立路由。

## 2. 共享候选二：另一个固定成员

类别对：animal；家族：N004；成员：#6289。

### cat：S13_N004_explicit_cat

```text
A curtain briefly exposed a picture of a cat before closing again. The viewer is trying to describe the subject.
Description:
```

实际读取：冒号，token ID=25，零起索引=23；场景=partial_visibility。

| 成员 | 激活值 |
| --- | ---: |
| #6289 | 1.760793 |

| 实际expert | gate权重 | 原softmax概率 | load bias |
| --- | ---: | ---: | ---: |
| 6 | 0.599432 | 0.274827 | 2.390009 |
| 1 | 0.400568 | 0.183652 | 2.396009 |

输入重建相对平方误差=0.203594。完整8维logits、概率和原生hidden见observations索引。

### dog：S13_N004_explicit_dog

```text
A curtain briefly exposed a picture of a dog before closing again. The viewer is trying to describe the subject.
Description:
```

实际读取：冒号，token ID=25，零起索引=23；场景=partial_visibility。

| 成员 | 激活值 |
| --- | ---: |
| #6289 | 1.935158 |

| 实际expert | gate权重 | 原softmax概率 | load bias |
| --- | ---: | ---: | ---: |
| 6 | 0.583508 | 0.263823 | 2.390009 |
| 1 | 0.416492 | 0.188310 | 2.396009 |

输入重建相对平方误差=0.206794。完整8维logits、概率和原生hidden见observations索引。

**读取边界：** 此处同时活跃的成员共享这份token路由。专家组合相同不能证明分配正确或错误；组合不同也不能证明该共享成员应当被独立路由。

## 3. 类别偏向候选一：A侧成员

类别对：animal；家族：N004；成员：#29184, #21462。

### cat：S13_N004_explicit_cat

```text
A curtain briefly exposed a picture of a cat before closing again. The viewer is trying to describe the subject.
Description:
```

实际读取：冒号，token ID=25，零起索引=23；场景=partial_visibility。

| 成员 | 激活值 |
| --- | ---: |
| #29184 | 5.130621 |
| #21462 | 1.525634 |

| 实际expert | gate权重 | 原softmax概率 | load bias |
| --- | ---: | ---: | ---: |
| 6 | 0.599432 | 0.274827 | 2.390009 |
| 1 | 0.400568 | 0.183652 | 2.396009 |

输入重建相对平方误差=0.203594。完整8维logits、概率和原生hidden见observations索引。

### dog：S13_N004_explicit_dog

```text
A curtain briefly exposed a picture of a dog before closing again. The viewer is trying to describe the subject.
Description:
```

实际读取：冒号，token ID=25，零起索引=23；场景=partial_visibility。

| 成员 | 激活值 |
| --- | ---: |
| #29184 | 0.000000 |
| #21462 | 4.873860 |

| 实际expert | gate权重 | 原softmax概率 | load bias |
| --- | ---: | ---: | ---: |
| 6 | 0.583508 | 0.263823 | 2.390009 |
| 1 | 0.416492 | 0.188310 | 2.396009 |

输入重建相对平方误差=0.206794。完整8维logits、概率和原生hidden见observations索引。

**读取边界：** 此处同时活跃的成员共享这份token路由。专家组合相同不能证明分配正确或错误；组合不同也不能证明该共享成员应当被独立路由。

## 4. 类别偏向候选二：B侧成员

类别对：animal；家族：N004；成员：#21462, #29184。

### cat：S13_N004_explicit_cat

```text
A curtain briefly exposed a picture of a cat before closing again. The viewer is trying to describe the subject.
Description:
```

实际读取：冒号，token ID=25，零起索引=23；场景=partial_visibility。

| 成员 | 激活值 |
| --- | ---: |
| #21462 | 1.525634 |
| #29184 | 5.130621 |

| 实际expert | gate权重 | 原softmax概率 | load bias |
| --- | ---: | ---: | ---: |
| 6 | 0.599432 | 0.274827 | 2.390009 |
| 1 | 0.400568 | 0.183652 | 2.396009 |

输入重建相对平方误差=0.203594。完整8维logits、概率和原生hidden见observations索引。

### dog：S13_N004_explicit_dog

```text
A curtain briefly exposed a picture of a dog before closing again. The viewer is trying to describe the subject.
Description:
```

实际读取：冒号，token ID=25，零起索引=23；场景=partial_visibility。

| 成员 | 激活值 |
| --- | ---: |
| #21462 | 4.873860 |
| #29184 | 0.000000 |

| 实际expert | gate权重 | 原softmax概率 | load bias |
| --- | ---: | ---: | ---: |
| 6 | 0.583508 | 0.263823 | 2.390009 |
| 1 | 0.416492 | 0.188310 | 2.396009 |

输入重建相对平方误差=0.206794。完整8维logits、概率和原生hidden见observations索引。

**读取边界：** 此处同时活跃的成员共享这份token路由。专家组合相同不能证明分配正确或错误；组合不同也不能证明该共享成员应当被独立路由。

## 5. 反例：同一共享成员、同一家族，两类的专家组合仍可不同

类别对：instrument；家族：N029；成员：#14800。

### piano：S13_N029_explicit_piano

```text
The collection database lost the text attached to a piano, although its image was preserved. A curator is repairing the entry.
Description:
```

实际读取：冒号，token ID=25，零起索引=25；场景=catalogue_recovery。

| 成员 | 激活值 |
| --- | ---: |
| #14800 | 2.932667 |

| 实际expert | gate权重 | 原softmax概率 | load bias |
| --- | ---: | ---: | ---: |
| 6 | 0.724335 | 0.387214 | 2.390009 |
| 7 | 0.275665 | 0.147364 | 2.397009 |

输入重建相对平方误差=0.204957。完整8维logits、概率和原生hidden见observations索引。

### guitar：S13_N029_explicit_guitar

```text
The collection database lost the text attached to a guitar, although its image was preserved. A curator is repairing the entry.
Description:
```

实际读取：冒号，token ID=25，零起索引=25；场景=catalogue_recovery。

| 成员 | 激活值 |
| --- | ---: |
| #14800 | 2.893579 |

| 实际expert | gate权重 | 原softmax概率 | load bias |
| --- | ---: | ---: | ---: |
| 6 | 0.735138 | 0.391220 | 2.390009 |
| 1 | 0.264862 | 0.140952 | 2.396009 |

输入重建相对平方误差=0.222851。完整8维logits、概率和原生hidden见observations索引。

**读取边界：** 此处同时活跃的成员共享这份token路由。专家组合相同不能证明分配正确或错误；组合不同也不能证明该共享成员应当被独立路由。

