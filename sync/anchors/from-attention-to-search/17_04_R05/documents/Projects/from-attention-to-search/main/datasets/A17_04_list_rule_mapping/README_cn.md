派生阅读副本；原件位置：`Projects/from-attention-to-search/main/datasets/A17_04_list_rule_mapping/README_cn.md`。
[精确原始文件](../../../../../../sources/Projects/from-attention-to-search/main/datasets/A17_04_list_rule_mapping/README_cn.md)；研究修改仍回到原件。

---

# A17_04：首项／末项条件规则数据

[English](README.md) · [逐文件清单与核验](../../../../../../sources/Projects/from-attention-to-search/main/datasets/A17_04_list_rule_mapping/inventory.json) · [资产库入口](https://github.com/Shphd3/Research_System/blob/master/assets/a17_list_rule_mapping_cn.md)

**你记得的是 A17_04 的 E01／R02：先学模式一，再学反转的模式二时，旧规则准确率从100%降到0%；混合监督两种模式时，两者都接近100%。** 正式来源是[父Anchor](../../../../../../UNAVAILABLE.md)与[R02结果](../../../../../../UNAVAILABLE.md)。

这是一组人工生成的三词列表任务。正式数据资产ID是 `data_a17_conditional_mapping_v1`。本页整理已有版本和使用入口；原数据、标签、划分、生成器和历史结果保持原样。

## 先看一道真实题

下面四行来自DEV中的同一列表 `0-1-10`，不是新造的演示数据。输入到“答案：”结束，目标词由模型预测。

| 数据字段 `world` | 完整输入前缀 | 目标词 | 要用的规则 |
|---|---|---|---|
| `old` | 模式：一。口令：甲。列表：红 黄 猫。答案： | 红 | 首项 |
| `old` | 模式：一。口令：乙。列表：红 黄 猫。答案： | 猫 | 末项 |
| `reversed` | 模式：二。口令：甲。列表：红 黄 猫。答案： | 猫 | 末项 |
| `reversed` | 模式：二。口令：乙。列表：红 黄 猫。答案： | 红 | 首项 |

模型能看到模式和口令，所以同一列表在两种模式下有不同答案，仍是可以共同学会的任务。另一个 `consistent` 对照也使用模式二，但保留“甲首、乙末”。`consistent` 与 `reversed` 的完整输入相同、答案相反，属于两个不同实验世界；复用时分别选取，不能把两个世界的标签一起作为同一训练任务。

[R02真实预测案例](../../../../../../UNAVAILABLE.md)记录：旧模式甲最初答红，反转续学后答猫，混合训练后又能答红。该案例是事后挑选的说明样本。

## 哪个版本对应什么

| 版本与资产ID | 作用与实际规模 | 位置 |
|---|---|---|
| 原始首／末任务 `data_a17_list_rules_v1` | A17_01直接写“取第一项／最后一项”；TRAIN/DEV/TEST为4000/800/800行。是任务前身。 | [list_rules_v1](../../../../../../UNAVAILABLE.md) |
| **条件映射母版 `data_a17_conditional_mapping_v1`** | **A17_04 R02实际使用。** 文件包含old、consistent、reversed三个世界，TRAIN/DEV/TEST共7200/2400/2400行；每世界2400/800/800。 | [conditional_mapping_v1](../../../../../../UNAVAILABLE.md) |
| 获取诊断 `data_a17_mapping_acquisition_diagnostic_v1` | 母版old的neutral／explicit／normalized三种呈现。每视图TRAIN2400、DEV800，另有64行tiny和400行TRAIN读数面板；E03的合格旧起点使用neutral。 | [acquisition_v1](../../../../../../UNAVAILABLE.md) |
| 联合与分模式视图 `data_a17_shared_routed_joint_v1` / `data_a17_shared_routed_mode_partition_v1` | 后续E04将母版old＋reversed整理为同一组记录的联合文件和模式分区。联合TRAIN4800／DEV1600；每模式2400／800。两个ID指同一物理版本。 | [mapping_view_v1](../../../../../../UNAVAILABLE.md) |

共四个物理数据版本、五个资产ID。后续E04的低秩结构与R02完整四矩阵不同；数据视图可对应，训练结果各归其原实验。

## 原始文件与划分

R02母版目录：

```text
/data/250010109/MoE_Router/experiments/20261011_a17_conditional_mapping_transfer/data/conditional_mapping_v1/
  manifest.json       生成种子、词表、tokenizer身份、划分和文件哈希
  qualification.json  原始生成资格记录
  train.jsonl         7200行，三个世界各2400
  dev.jsonl           2400行，三个世界各800
  test.jsonl          2400行；R02不读取
```

生成种子为20261011。20个答案词是：红、黄、蓝、黑、绿、白、紫、灰、金、银、猫、狗、鸟、鱼、牛、马、羊、虎、龙、花。每列表三个不同词，每个答案在登记的tokenizer中是一个词元；监督只计算答案位置。

每世界TRAIN包含1200个有序列表，每个列表配甲、乙两题。每世界DEV有两个面板，各400行：

- `order_new`：三词集合在TRAIN见过，这个排列没有见过。
- `combination_new`：无序三词集合没有在TRAIN出现；使用的单词仍来自相同词表。

两面板分别报告，再等权合并。旧新模式有意共享底层列表内容，完整输入因模式字段不同而不同。R02的TRAIN／DEV此前已使用，不能当作新确认数据；母版TEST在早期R01已用于评价，R02没有重新读取。

## 直接找到可用文件

复核R02时，读取母版并按 `world` 过滤，保持原采样和曝光定义：

```python
import json
from pathlib import Path

root = Path('/data/250010109/MoE_Router/experiments/20261011_a17_conditional_mapping_transfer/data/conditional_mapping_v1')
with (root / 'train.jsonl').open() as stream:
    rows = [json.loads(line) for line in stream if line.strip()]
old = [row for row in rows if row['world'] == 'old']
new_reversed = [row for row in rows if row['world'] == 'reversed']
new_consistent = [row for row in rows if row['world'] == 'consistent']
assert len(old) == len(new_reversed) == len(new_consistent) == 2400
```

若只想拿已整理的首／末反转任务，在已有 `mapping_view_v1` 目录读：

| 使用方式 | TRAIN | DEV |
|---|---|---|
| 模式一 | `mode1_train.jsonl`，2400行 | `mode1_dev.jsonl`，800行 |
| 反转模式二 | `mode2_train.jsonl`，2400行 | `mode2_dev.jsonl`，800行 |
| 两模式联合 | `joint_train.jsonl`，4800行 | `joint_dev.jsonl`，1600行 |

联合文件恰等于两个模式分区的并集，保留母版的 `record_id`、输入和目标。R02本身没有读取这些后来生成的文件，它在母版上构造联合批次；它的[原采样器](../../../../../../UNAVAILABLE.md)定义每批5列表×2口令×2模式＝20答案。复现R02需沿用该采样器和[R02 Protocol](../../../../../../UNAVAILABLE.md)。

## 一行数据怎样读

| 字段 | 含义 |
|---|---|
| `record_id` | 划分／世界／口令／有序列表，定位完整题目 |
| `list_id`, `words` | 有序列表身份和三个原词；同列表的两口令配对 |
| `unordered_group_id` | 忽略顺序的三词集合，用于判断组合是否未见 |
| `world`, `mode`, `command` | 实验世界、模型可见模式和模型可见口令 |
| `panel`, `split` | 未见面板及TRAIN／DEV／TEST身份 |
| `prefix`, `input_ids` | 不含答案的原文及分词结果 |
| `target_word`, `target_id`, `rule` | 正确答案、其词元ID及FIRST／LAST规则 |

实际模型只接收 `input_ids`；`world`、`rule`和目标等字段用于组织数据及监督，不额外输入模型。换tokenizer时要重新检查答案边界；不能把原来的词元ID直接当成新分词器的ID。

## 你记得的现象对应哪些数值

旧起点准确率100%。下表按800行旧／新DEV、两面板等权汇总：

| 续训顺序种子 | 只续学反转：旧／新准确率 | 混合旧新：旧／新准确率 |
|---|---|---|
| 29 | 0% / 100% | 100% / 100% |
| 43 | 0% / 100% | 99.75% / 99.75% |
| 71 | 0% / 97.75% | 99.75% / 99.25% |

三顺序共用一个旧终点。单学分支各24000个新答案；混合分支总量也是24000，但旧新各12000。它给出两套规则可以共同学会的实例，不是等新任务曝光的结构收益比较。完整解释留在[R02 Summary](../../../../../../UNAVAILABLE.md)。

## 本次整理做了什么

补齐项目的数据入口、版本关系、真实样例、字段和复用路线；[清单](../../../../../../sources/Projects/from-attention-to-search/main/datasets/A17_04_list_rule_mapping/inventory.json)记录当前文件大小、哈希、行数及必要配对核对。原文件有生成清单和划分，问题主要是这些入口散在不同实验目录。本次保留全部原路径，不重生成或移动冻结数据，不运行模型。GitHub保存说明和小型元数据；完整JSONL仍在执行存储。
