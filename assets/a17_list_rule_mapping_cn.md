# A17 列表规则与条件映射：来源导览

[English](a17_list_rule_mapping.md) · [根资产登记](catalog.json)

完整Anchor、R02协议／结果和数据说明已收入本仓库的[只读同步阅读包](../sync/anchors/from-attention-to-search/17_04/README.md)；无需访问独立项目即可阅读全文。来源与副本哈希见包内manifest.json。


你记得的“先学会旧规则，只学新规则后旧规则丢失，混合后两者都能做”，精确对应 **A17_04 → E01 → R02_single_layer_adamw**。本页让只有 Research_System 仓库的读者看懂任务与证据；科学设计和判断仍由 [Anchor同步副本](../sync/anchors/from-attention-to-search/17_04/documents/Projects/from-attention-to-search/main/problem_anchors/17_shared_and_interference_learning/17_04_conditional_mapping_transfer/17_04_conditional_mapping_transfer_anchor_cn.md) 与 [R02结果同步副本](../sync/anchors/from-attention-to-search/17_04/documents/Projects/from-attention-to-search/main/experiments/A17/17_04_conditional_mapping_transfer/A17_04_E01_consistent_reversed_mapping/rounds/R02_single_layer_adamw/summary_cn.md)持有。

## 实际问了什么

输入包含可见模式、口令甲／乙与三词列表。模式一教“甲取首项、乙取末项”；新模式二的反转分支交换这两条映射。同向对照则保留映射。下面是 `list_id=0-1-10` 的四条真实输入，取自母版的old与reversed两个分组：

| 输入前缀（答案从冒号后开始） | 正确答案 |
|---|---|
| `模式：一。口令：甲。列表：红 黄 猫。答案：` | 红 |
| `模式：一。口令：乙。列表：红 黄 猫。答案：` | 猫 |
| `模式：二。口令：甲。列表：红 黄 猫。答案：` | 猫 |
| `模式：二。口令：乙。列表：红 黄 猫。答案：` | 红 |

模型是 Qwen3-0.6B Base，只更新最后一层注意力的 q/k/v/o 四张矩阵（6,291,456 个参数）。先取得模式一准确率100%的旧终点，再分支续训。原R01旧规则未达到资格；R02使用后续E03得到的合格起点，二者结果分别保留。

## R02 测到什么

表中是两个DEV面板等权合并的准确率。三个数字依次对应续训顺序种子29／43／71；它们共用同一个已训练旧终点。

| 续训方式 | 旧规则准确率 | 新规则准确率 |
|---|---|---|
| 旧起点 | 100%／100%／100% | 尚未续训 |
| 只学同向新规则 | 100%／100%／100% | 100%／100%／100% |
| 只学反转新规则 | **0%／0%／0%** | **100%／100%／97.75%** |
| 旧／反转新混合 | **100%／99.75%／99.75%** | **100%／99.75%／99.25%** |

同一真实列表中，种子29的旧口令甲预测“红→猫→红”，旧口令乙预测“猫→红→猫”，分别对应旧起点、只学反转、混合训练。这是事后选取的说明性样本；总体证据以上表为准。

**怎样使用这些数字。** 这是已暴露DEV上的诊断，R02没有读取TEST，三个续训顺序也不是三个独立旧模型。混合分支额外得到旧标签：同为24,000个训练答案，混合含12,000旧＋12,000新，纯新分支为24,000新。它提供两套可见规则能在共享参数中共存的见证，不能据此判断等新曝光下的重放收益、参数分开或专家架构收益。研究者机制判断与问题关闭仍为Unknown。

## 五个 data ID，四个物理 release

这些是前驱和派生视图，不是五份独立数据或一条简单的版本升级链。完整计数、文件hash、生成及划分关系见项目的 [正规数据导览](../sync/anchors/from-attention-to-search/17_04/documents/Projects/from-attention-to-search/main/datasets/A17_04_list_rule_mapping/README_cn.md) 和 [inventory.json](../sync/anchors/from-attention-to-search/17_04/sources/Projects/from-attention-to-search/main/datasets/A17_04_list_rule_mapping/inventory.json)。

| 资产ID | 关系与用途 | 执行侧父目录 |
|---|---|---|
| `data_a17_list_rules_v1` | A17_01前驱FIRST／LAST任务；4000／800／800条TRAIN／DEV／TEST | `/data/250010109/MoE_Router/experiments/20261009_a17_list_rules/data/list_rules_v1` |
| `data_a17_conditional_mapping_v1` | A17_04正式三世界版本；每世界TRAIN2400、DEV800、TEST800；**R02用此版本的TRAIN／DEV** | `/data/250010109/MoE_Router/experiments/20261011_a17_conditional_mapping_transfer/data/conditional_mapping_v1` |
| `data_a17_mapping_acquisition_diagnostic_v1` | 从上一版本旧模式TRAIN／DEV派生neutral／explicit／normalized三种呈现，供旧规则习得诊断 | `/data/250010109/MoE_Router/experiments/20261011_a17_mapping_acquisition_diagnostic/data/acquisition_v1` |
| `data_a17_shared_routed_joint_v1` ＋ `data_a17_shared_routed_mode_partition_v1` | 后续预算比较的同一批记录：联合TRAIN4800／DEV1600，或按模式各TRAIN2400／DEV800 | `/data/250010109/MoE_Router/experiments/20261012_a17_shared_routed_budget/data/mapping_view_v1` |

最后两个ID共享同一目录和manifest，分别登记联合视图与按模式分区；不是R02的额外训练样本。原始JSONL、模型状态和完整逐样本输出都在执行侧，**没有随本导览放到GitHub**。本机绝对路径只是位置说明，远端读者先用 [项目数据导览](../sync/anchors/from-attention-to-search/17_04/documents/Projects/from-attention-to-search/main/datasets/A17_04_list_rule_mapping/README_cn.md)、[清单](../sync/anchors/from-attention-to-search/17_04/sources/Projects/from-attention-to-search/main/datasets/A17_04_list_rule_mapping/inventory.json) 与 [资产登记](catalog.json)核对身份。

正式 owner 的父目录是 `main/problem_anchors/17_shared_and_interference_learning/17_04_conditional_mapping_transfer/`；R02记录位于 `main/experiments/A17/17_04_conditional_mapping_transfer/A17_04_E01_consistent_reversed_mapping/rounds/R02_single_layer_adamw/`。阅读顺序：[任务与边界](../sync/anchors/from-attention-to-search/17_04/documents/Projects/from-attention-to-search/main/problem_anchors/17_shared_and_interference_learning/17_04_conditional_mapping_transfer/17_04_conditional_mapping_transfer_anchor_cn.md) → [R02事实与对照](../sync/anchors/from-attention-to-search/17_04/documents/Projects/from-attention-to-search/main/experiments/A17/17_04_conditional_mapping_transfer/A17_04_E01_consistent_reversed_mapping/rounds/R02_single_layer_adamw/summary_cn.md) → [数据版本](../sync/anchors/from-attention-to-search/17_04/documents/Projects/from-attention-to-search/main/datasets/A17_04_list_rule_mapping/README_cn.md)。本页是来源导览，不另建 Anchor 或改变科研状态。

原项目地址：[from-attention-to-search / Xingyu](https://github.com/BinaryCheater/from-attention-to-search/tree/Xingyu)。本仓库副本带来源路径和哈希；科研修改仍回该项目。


### R06第120步：参数与Adam累积状态交换（2026-10-26）

[一页中文](../Projects/from-attention-to-search/main/experiments/A17/17_04_conditional_mapping_transfer/rounds/R06_functional_protection_20261025/adam_swap_20261026/one_page_cn.md) · [逐种子逐批](../Projects/from-attention-to-search/main/experiments/A17/17_04_conditional_mapping_transfer/rounds/R06_functional_protection_20261025/adam_swap_20261026/appendix_cn.md)。已完成36次独立临时普通更新、10320条前向。固定F参数，换U矩状态的旧CE变化9/9次更有利，但新任务存在取舍，参数与矩状态也存在交互。未进行F投影、完整续训或TEST评价；不构成长期因果分解。资产：`analysis_a17_r06_adam_swap_20261026`；当前输出访问检查的持久回执保存在交付的`reproduce/output_access.json`。
