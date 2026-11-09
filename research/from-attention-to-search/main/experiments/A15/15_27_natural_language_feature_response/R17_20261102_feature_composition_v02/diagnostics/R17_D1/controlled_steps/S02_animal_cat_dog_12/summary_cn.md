# S02：animal—cat/dog普通语言续写检查

**本固定续写格式下，12条全部正确，6组均随明确的cat/dog词变化而向正确方向改变首选。** 本步已完成并停止，等待共同审阅。只有一种事先冻结的续写格式，没有追加prompt或数据。

## 目的与S01的关系

S01方阵三选一的两格式大多固定选否／是，中性前缀也有相似偏好。本步按用户指定，改用明确animal+cat/dog的短英文文本及二候选续写，只检查同一冻结模型能否随明示类别改变后续偏好。方阵实验原文、脚本、分数和结论均保留，核验81个原文件SHA不变；没有修改研究假设。

两轮同时改变了概念、语言、任务和候选形式，不是单因素对照。因此即使本步成功，也不能把差异唯一归因“改成二选一”或“自然概念更简单”。

## 数据与唯一格式

6短语境家族，每组cat/dog一对，共12条；每对只替换细类词，其他句子和背景一致。标签为animal+cat或animal+dog，12条均人工式逐条审核后、任何模型响应前冻结。无预测筛选，无新增同义词／属性推断。

全部文本使用相同后缀：换行后`The animal is a`，紧接两个固定完整候选。实际tokenizer逐项检查26个拼接，未预设token数：

| candidate   | token_ids   |   tokens |   neutral_sequence_logprob |
|:------------|:------------|---------:|---------------------------:|
| " cat."     | [8251, 13]  |        2 |                  -5.834870 |
| " dog."     | [5562, 13]  |        2 |                  -5.656862 |

候选字符串中的前导空格和句号都保留；token长度恰好同为2，包含句号token13。主指标是完整候选的条件自然对数概率总和，单位为nats；取最大总分，不做长度、先验或温度校正。FP32原生模型/logsoftmax、FP64求和；同一官方Qwen3-0.6BBase和tokenizer，权重/配置/tokenizer SHA与S01实际加载版本一致；CPU2线程、无chat模板。没有另训分类器、字典加载、feature记录/分析/干预。

## 结果

| class_label   |   correct |   N |
|:--------------|----------:|----:|
| cat           |         6 |   6 |
| dog           |         6 |   6 |
| all           |        12 |  12 |

配对中首选发生变化：**6/6组**；两条都判断正确：**6/6组**；反向切换：0/6组。“发生切换”与“正确跟随”分别记账，避免把两条都反向误判当成正确跟随。

| family   | cat_choice   | dog_choice   |   cat_delta |   dog_delta | choice_changed   | both_correct   | reversed_switch   |
|:---------|:-------------|:-------------|------------:|------------:|:-----------------|:---------------|:------------------|
| F01      | cat          | dog          |    2.781256 |   -1.895151 | True             | True           | False             |
| F02      | cat          | dog          |    3.640498 |   -2.930142 | True             | True           | False             |
| F03      | cat          | dog          |    4.782505 |   -4.198835 | True             | True           | False             |
| F04      | cat          | dog          |    4.295776 |   -3.825254 | True             | True           | False             |
| F05      | cat          | dog          |    3.135507 |   -4.452133 | True             | True           | False             |
| F06      | cat          | dog          |    3.825219 |   -3.709584 | True             | True           | False             |

错误共0条，见[全部错误](errors_cn.md)。没有错误时明确注明；没有筛选只展示有利家族。[完整逐家族记录](casebook_cn.md)给全部12条原文、标签、完整前缀、token ID/长度、两分数、差值、首选与对错。

## 固定第一组的完整前缀与分数

F01在响应前已固定为展示组。原文分别为“This animal is a cat.”和“This animal is a dog.”，标签分别animal+cat、animal+dog。

```text
This animal is a cat.
The animal is a
```

```text
This animal is a dog.
The animal is a
```

| gold   |     S_cat |     S_dog |   delta_cat_minus_dog | choice   | correct   |
|:-------|----------:|----------:|----------------------:|:---------|:----------|
| cat    | -1.711961 | -4.493217 |              2.781256 | cat      | True      |
| dog    | -3.903837 | -2.008686 |             -1.895151 | dog      | True      |

## 中性前缀与基础偏好

中性文本不指明猫或狗，后缀和候选完全相同：

```text
An animal is mentioned in this note.
The animal is a
```

上方候选表已列中性两分数；S_cat−S_dog=-0.178008199，首选**dog**。中性记录没有正确标签、不计准确率；它仅描述一个固定前缀下的基础偏好，未用于扣分、调阈值或改选候选。

## 本步能说明什么、不能说明什么

本步说明该冻结模型在这6组明确词语的受控文本、固定续写位置及完整候选计分下的实际偏好，及偏好是否随cat/dog替换改变。候选恰好等长，排除了本轮两个候选token数量不等这一具体因素；词汇先验、上下文概率及句号条件概率仍是总分的组成部分，等长不代表先验相同。

**成功可以只是复制／复述前文中完全相同的cat或dog。** 本步没有用未出现的细类词、没有测试类别抽象或未知动物，因此不能证明抽象概念理解、animal与细类的内在层级组织、feature成员或强弱组合、因果使用及广泛泛化。这是二候选续写偏好，不是自由生成准确率；中性前缀也不作为未知类别题评分。

**停止：仅S02完成，下一步未运行，等待共同审阅。** 没有自动增加数据、修改假设或开展feature分析。

[协议](protocol_cn.md) · [数据](data/panel.jsonl) · [完整原始分数](results/raw_scores.jsonl) · [逐候选CSV](results/candidate_scores.csv) · [原生评分脚本](code/score_native.py) · [核验](evidence/verification.json)
