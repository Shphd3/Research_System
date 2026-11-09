# 12条原文、前缀与完整候选分数

每条的类别标签均为animal加cat或dog。精确候选固定为ASCII前导空格加cat/dog及句号：`" cat."`、`" dog."`。分数为全部候选token的条件自然对数概率总和，越大越优，差值定义S_cat−S_dog。表显示6位小数，JSONL保留完整精度和逐token分数。

[中文小结](summary_cn.md) · [原始记录](results/raw_scores.jsonl) · [精确token拼接](data/prompts_tokenized.jsonl)

## F01

### S02_F01_cat — 标签 ["animal", "cat"]

原文：

```text
This animal is a cat.
```

完整续写前缀（候选紧接末尾a）：

```text
This animal is a cat.
The animal is a
```

### S02_F01_dog — 标签 ["animal", "dog"]

原文：

```text
This animal is a dog.
```

完整续写前缀（候选紧接末尾a）：

```text
This animal is a dog.
The animal is a
```

| gold   |     S_cat |     S_dog |   delta_cat_minus_dog | choice   | correct   |
|:-------|----------:|----------:|----------------------:|:---------|:----------|
| cat    | -1.711961 | -4.493217 |              2.781256 | cat      | True      |
| dog    | -3.903837 | -2.008686 |             -1.895151 | dog      | True      |

| id          | candidate   | token_ids   |   tokens |   sequence_logprob |
|:------------|:------------|:------------|---------:|-------------------:|
| S02_F01_cat | " cat."     | [8251, 13]  |        2 |          -1.711961 |
| S02_F01_cat | " dog."     | [5562, 13]  |        2 |          -4.493217 |
| S02_F01_dog | " cat."     | [8251, 13]  |        2 |          -3.903837 |
| S02_F01_dog | " dog."     | [5562, 13]  |        2 |          -2.008686 |

## F02

### S02_F02_cat — 标签 ["animal", "cat"]

原文：

```text
In this story, the animal is a cat.
```

完整续写前缀（候选紧接末尾a）：

```text
In this story, the animal is a cat.
The animal is a
```

### S02_F02_dog — 标签 ["animal", "dog"]

原文：

```text
In this story, the animal is a dog.
```

完整续写前缀（候选紧接末尾a）：

```text
In this story, the animal is a dog.
The animal is a
```

| gold   |     S_cat |     S_dog |   delta_cat_minus_dog | choice   | correct   |
|:-------|----------:|----------:|----------------------:|:---------|:----------|
| cat    | -1.400252 | -5.040750 |              3.640498 | cat      | True      |
| dog    | -4.366657 | -1.436516 |             -2.930142 | dog      | True      |

| id          | candidate   | token_ids   |   tokens |   sequence_logprob |
|:------------|:------------|:------------|---------:|-------------------:|
| S02_F02_cat | " cat."     | [8251, 13]  |        2 |          -1.400252 |
| S02_F02_cat | " dog."     | [5562, 13]  |        2 |          -5.040750 |
| S02_F02_dog | " cat."     | [8251, 13]  |        2 |          -4.366657 |
| S02_F02_dog | " dog."     | [5562, 13]  |        2 |          -1.436516 |

## F03

### S02_F03_cat — 标签 ["animal", "cat"]

原文：

```text
We are describing an animal. It is a cat.
```

完整续写前缀（候选紧接末尾a）：

```text
We are describing an animal. It is a cat.
The animal is a
```

### S02_F03_dog — 标签 ["animal", "dog"]

原文：

```text
We are describing an animal. It is a dog.
```

完整续写前缀（候选紧接末尾a）：

```text
We are describing an animal. It is a dog.
The animal is a
```

| gold   |     S_cat |     S_dog |   delta_cat_minus_dog | choice   | correct   |
|:-------|----------:|----------:|----------------------:|:---------|:----------|
| cat    | -1.278424 | -6.060929 |              4.782505 | cat      | True      |
| dog    | -5.451335 | -1.252500 |             -4.198835 | dog      | True      |

| id          | candidate   | token_ids   |   tokens |   sequence_logprob |
|:------------|:------------|:------------|---------:|-------------------:|
| S02_F03_cat | " cat."     | [8251, 13]  |        2 |          -1.278424 |
| S02_F03_cat | " dog."     | [5562, 13]  |        2 |          -6.060929 |
| S02_F03_dog | " cat."     | [8251, 13]  |        2 |          -5.451335 |
| S02_F03_dog | " dog."     | [5562, 13]  |        2 |          -1.252500 |

## F04

### S02_F04_cat — 标签 ["animal", "cat"]

原文：

```text
The note identifies this animal as a cat.
```

完整续写前缀（候选紧接末尾a）：

```text
The note identifies this animal as a cat.
The animal is a
```

### S02_F04_dog — 标签 ["animal", "dog"]

原文：

```text
The note identifies this animal as a dog.
```

完整续写前缀（候选紧接末尾a）：

```text
The note identifies this animal as a dog.
The animal is a
```

| gold   |     S_cat |     S_dog |   delta_cat_minus_dog | choice   | correct   |
|:-------|----------:|----------:|----------------------:|:---------|:----------|
| cat    | -2.258047 | -6.553824 |              4.295776 | cat      | True      |
| dog    | -5.952024 | -2.126770 |             -3.825254 | dog      | True      |

| id          | candidate   | token_ids   |   tokens |   sequence_logprob |
|:------------|:------------|:------------|---------:|-------------------:|
| S02_F04_cat | " cat."     | [8251, 13]  |        2 |          -2.258047 |
| S02_F04_cat | " dog."     | [5562, 13]  |        2 |          -6.553824 |
| S02_F04_dog | " cat."     | [8251, 13]  |        2 |          -5.952024 |
| S02_F04_dog | " dog."     | [5562, 13]  |        2 |          -2.126770 |

## F05

### S02_F05_cat — 标签 ["animal", "cat"]

原文：

```text
A cat is the animal described in this example.
```

完整续写前缀（候选紧接末尾a）：

```text
A cat is the animal described in this example.
The animal is a
```

### S02_F05_dog — 标签 ["animal", "dog"]

原文：

```text
A dog is the animal described in this example.
```

完整续写前缀（候选紧接末尾a）：

```text
A dog is the animal described in this example.
The animal is a
```

| gold   |     S_cat |     S_dog |   delta_cat_minus_dog | choice   | correct   |
|:-------|----------:|----------:|----------------------:|:---------|:----------|
| cat    | -2.420530 | -5.556037 |              3.135507 | cat      | True      |
| dog    | -6.312284 | -1.860151 |             -4.452133 | dog      | True      |

| id          | candidate   | token_ids   |   tokens |   sequence_logprob |
|:------------|:------------|:------------|---------:|-------------------:|
| S02_F05_cat | " cat."     | [8251, 13]  |        2 |          -2.420530 |
| S02_F05_cat | " dog."     | [5562, 13]  |        2 |          -5.556037 |
| S02_F05_dog | " cat."     | [8251, 13]  |        2 |          -6.312284 |
| S02_F05_dog | " dog."     | [5562, 13]  |        2 |          -1.860151 |

## F06

### S02_F06_cat — 标签 ["animal", "cat"]

原文：

```text
The report calls the animal a cat.
```

完整续写前缀（候选紧接末尾a）：

```text
The report calls the animal a cat.
The animal is a
```

### S02_F06_dog — 标签 ["animal", "dog"]

原文：

```text
The report calls the animal a dog.
```

完整续写前缀（候选紧接末尾a）：

```text
The report calls the animal a dog.
The animal is a
```

| gold   |     S_cat |     S_dog |   delta_cat_minus_dog | choice   | correct   |
|:-------|----------:|----------:|----------------------:|:---------|:----------|
| cat    | -1.880962 | -5.706181 |              3.825219 | cat      | True      |
| dog    | -5.632697 | -1.923113 |             -3.709584 | dog      | True      |

| id          | candidate   | token_ids   |   tokens |   sequence_logprob |
|:------------|:------------|:------------|---------:|-------------------:|
| S02_F06_cat | " cat."     | [8251, 13]  |        2 |          -1.880962 |
| S02_F06_cat | " dog."     | [5562, 13]  |        2 |          -5.706181 |
| S02_F06_dog | " cat."     | [8251, 13]  |        2 |          -5.632697 |
| S02_F06_dog | " dog."     | [5562, 13]  |        2 |          -1.923113 |

## 唯一中性前缀

```text
An animal is mentioned in this note.
The animal is a
```

| id      | family   | gold   | candidate   | label   | token_ids   |   tokens |   sequence_logprob |
|:--------|:---------|:-------|:------------|:--------|:------------|---------:|-------------------:|
| neutral | neutral  |        | cat.        | cat     | [8251, 13]  |        2 |          -5.834870 |
| neutral | neutral  |        | dog.        | dog     | [5562, 13]  |        2 |          -5.656862 |

差值=-0.178008199；首选=dog。没有正确标签，不计入12条准确率，不校正其他分数。
