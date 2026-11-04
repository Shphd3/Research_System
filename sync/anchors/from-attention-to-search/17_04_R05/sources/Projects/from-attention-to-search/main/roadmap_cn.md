# 项目研究路线图

[English](roadmap.md) · [项目入口](README_cn.md) · [全部 Focus](focus/README_cn.md) · [全部 Anchor](problem_anchors/README_cn.md) · [研究地图](research_map_cn.md)

这是一份按问题定位的导航，不另存研究状态或执行队列。Focus 持有研究者判断，Anchor 持有科学设计，Protocol 持有精确执行契约，Summary / Detailed 持有结果与证据。本次整理不激活、暂停、合并或关闭任何既有 Focus。

研究问题的完整层次与子问题作用见 [研究地图](research_map_cn.md)（[英文入口](research_map.md)）。[地图数据](research_map.json)是派生导航，原 Anchor、Focus 与结果记录保留各自权威；离线交互版的生成方法见 [项目入口](README_cn.md#研究地图与离线交互版)。

## 本对话的阅读入口：A15_18

本轮小模型关系组织／使用分析归入 **A15_18**。先读 [逐项事实报告](experiments/A15/15_18_context_relation_organization_use/first_flow_v3/summary_cn.md)，再按需打开 [Focus](focus/focus_context_relation_organization_use_cn.md)、[Anchor](problem_anchors/15_spectral_representation_and_functional_routing/15_18_context_relation_organization_use/15_18_context_relation_organization_use_anchor_cn.md) 和 [Protocol](experiments/A15/15_18_context_relation_organization_use/first_flow_v3/protocol_cn.md)。结果审阅与机制判断遵循这些 owner 的既有边界；此入口没有赋予其他问题新的状态或运行授权。

## 按研究线查找

编号用于稳定归属，不表示时间先后、重要性或新的依赖关系。研究线内的父问题、局部子问题及其记录见相应入口；完整清单为 [152 个 owner 的归属登记](anchor_ownership.json)。

| 研究线 | 问题范围 | Anchor / 实验入口 | 当前正式 owner 数 |
|---|---|---|---:|
| A01 common 算子机制 | 可识别性、真值恢复、梯度共性与反馈共性。 | [Anchor 索引](problem_anchors/01_common_operator_mechanism/README_cn.md) · [实验记录](experiments/A01_common_operator) | 4 |
| A05 top-1 失败机制 | 早期锁定、抑制、公共偏移与公共 logit 的因果检查。 | [Anchor 索引](problem_anchors/05_failure_mechanism/research_map.md) · [实验记录](experiments/A05) | 7 |
| A06 部分反馈下的功能路由 | 定义 → 状态发现 → 划分保持 → 专家效用及发现 → 真实任务空间。 | [Anchor 索引](problem_anchors/06_geometry_proxy_preservation/research_map.md) · [实验记录](experiments/A06) | 6 |
| A07 共同特征干扰与价值 | common/rare 更新干扰；因果专家价值需单独检验。 | [Anchor 索引](problem_anchors/07_features_overlap/README.md) · [实验记录](experiments/A07) | 7 |
| A09 频率与谱判别 | 特征写入及高增益常见频带与稀有判别的关系。 | [Anchor 索引](problem_anchors/09_common_rare_spectral_discrimination/README.md) · [实验记录](experiments/A09) | 2 |
| A10 优化器与学习率机制 | 公共梯度、奇异值集中与 SGD 稳定性。 | [Anchor 索引](problem_anchors/10_optimizer_learning_rate_mechanism/README.md) · [实验记录](experiments/A10) | 3 |
| A11 信息性未来监督 | 直接状态信号、参数传递与跨位置标准头使用。 | [Anchor 索引](problem_anchors/11_informative_future_branch_mechanism/README.md) · [实验记录](experiments/A11) | 7 |
| A12 结构化组合任务 | 单步／两步能力、任务载体有效性、容量与中间状态使用。 | [Anchor 索引](problem_anchors/12_structured_compositional_mtp_workload/README.md) · [实验记录](experiments/A12) | 6 |
| A13 MTP 任务属性分解 | 中继必要性、监督位置／内容与普通预测头收益。 | [Anchor 索引](problem_anchors/13_mtp_task_property_decomposition/README.md) · [实验记录](experiments/A13) | 7 |
| A14 条件秩及状态／参数桥接 | 条件功能秩、局部雅可比与有限割线／路径积分映射。 | [Anchor 索引](problem_anchors/14_tree_low_rank_language_structure/README.md) · [实验记录](experiments/A14) | 6 |
| A15 表征几何与功能路由 | 几何、读出、原生使用、实际分发与专家学习分别立证。 | [Anchor 索引](problem_anchors/15_spectral_representation_and_functional_routing/README.md) · [实验记录](experiments/A15) | 73 |
| A16 负载控制与梯度干扰 | 负载目标的相互作用与同层增量的功能路由。 | [Anchor 索引](problem_anchors/16_load_control_gradient_interference/README.md) · [实验记录](experiments/A16) | 5 |
| A17 共享与干扰学习 | 条件规则、呈现次数、局部更新、自然文本几何与保持。 | [Anchor 索引](problem_anchors/17_shared_and_interference_learning/README_cn.md) · [实验记录](experiments/A17) | 19 |

[A00 基础定义](problem_anchors/00_foundation_definition/README.md) 是历史重定向，定义由 A06_00 持有，没有另立当前 Anchor。编号间的空号不创建缺失任务。

## 选择读物

- 已给出具体结果：直接读该实验的 Summary，再按证据需要读 Detailed。
- 已给出问题：在 [Focus 索引](focus/README_cn.md) 找原问题，进入其 Anchor 与协议；没有 Focus 的已登记 owner 仍保留原身份，不因此被激活。
- 只想定位设计或旧编号：读 [Anchor 全索引](problem_anchors/README_cn.md)、[归属登记](anchor_ownership.json) 和 [本次迁移记录](organization_migrations/20261022/README_cn.md)。
- 查数据、辅助材料或叙述：分别读 [数据登记](datasets/README.md)、[支持笔记](research_notes/) 与 [Stories](stories/)；它们不替代正式 owner。

[系统 PROJECTS.md](../../../PROJECTS.md) 只选择项目；本路线图负责项目内导航。科研结论和下一决定留在所属 Focus / Anchor，不能从列表顺序或目录存在推断。

## A15_26：低频组合复用

[独立父Anchor](problem_anchors/15_spectral_representation_and_functional_routing/15_26_low_frequency_compositional_reuse/15_26_low_frequency_compositional_reuse_anchor_cn.md)持有核心问题。[R01符号实验事实](experiments/A15/15_26_low_frequency_compositional_reuse/R01_controlled_operations/summary_cn.md)已完整交付，组成跨问法与组合资格失败；[并行订单V2](experiments/A15/15_26_low_frequency_compositional_reuse/20261024_order_v2/summary_cn.md)另持有自己的实验。两轮结果不混合，机制接受与问题关闭Unknown。
