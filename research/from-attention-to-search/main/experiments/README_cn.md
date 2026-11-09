# 实验协议与证据目录

[English](README.md) · [路线图](../roadmap_cn.md) · [Anchor 全索引](../problem_anchors/README_cn.md)

按 A 编号及拥有问题查找协议与结果。本页不复写实验状态、已批准预算或科研结论。精确 owner→实验路径由 [145 个 owner 归属登记](../anchor_ownership.json) 持有，全部问题见 [Anchor 全索引](../problem_anchors/README_cn.md)。

本轮入口：[A15_18 逐项事实报告](A15/15_18_context_relation_organization_use/first_flow_v3/summary_cn.md) · [Protocol](A15/15_18_context_relation_organization_use/first_flow_v3/protocol_cn.md) · [Detailed](A15/15_18_context_relation_organization_use/first_flow_v3/detailed_cn.md)。

## 按研究线进入

| 研究线 | 问题范围 | Anchor / 实验入口 | 当前正式 owner 数 |
|---|---|---|---:|
| A01 common 算子机制 | 可识别性、真值恢复、梯度共性与反馈共性。 | [Anchor 索引](../problem_anchors/01_common_operator_mechanism/README_cn.md) · [实验记录](A01_common_operator) | 4 |
| A05 top-1 失败机制 | 早期锁定、抑制、公共偏移与公共 logit 的因果检查。 | [Anchor 索引](../problem_anchors/05_failure_mechanism/research_map.md) · [实验记录](A05) | 7 |
| A06 部分反馈下的功能路由 | 定义 → 状态发现 → 划分保持 → 专家效用及发现 → 真实任务空间。 | [Anchor 索引](../problem_anchors/06_geometry_proxy_preservation/research_map.md) · [实验记录](A06) | 6 |
| A07 共同特征干扰与价值 | common/rare 更新干扰；因果专家价值需单独检验。 | [Anchor 索引](../problem_anchors/07_features_overlap/README.md) · [实验记录](A07) | 7 |
| A09 频率与谱判别 | 特征写入及高增益常见频带与稀有判别的关系。 | [Anchor 索引](../problem_anchors/09_common_rare_spectral_discrimination/README.md) · [实验记录](A09) | 2 |
| A10 优化器与学习率机制 | 公共梯度、奇异值集中与 SGD 稳定性。 | [Anchor 索引](../problem_anchors/10_optimizer_learning_rate_mechanism/README.md) · [实验记录](A10) | 2 |
| A11 信息性未来监督 | 直接状态信号、参数传递与跨位置标准头使用。 | [Anchor 索引](../problem_anchors/11_informative_future_branch_mechanism/README.md) · [实验记录](A11) | 7 |
| A12 结构化组合任务 | 单步／两步能力、任务载体有效性、容量与中间状态使用。 | [Anchor 索引](../problem_anchors/12_structured_compositional_mtp_workload/README.md) · [实验记录](A12) | 6 |
| A13 MTP 任务属性分解 | 中继必要性、监督位置／内容与普通预测头收益。 | [Anchor 索引](../problem_anchors/13_mtp_task_property_decomposition/README.md) · [实验记录](A13) | 7 |
| A14 条件秩及状态／参数桥接 | 条件功能秩、局部雅可比与有限割线／路径积分映射。 | [Anchor 索引](../problem_anchors/14_tree_low_rank_language_structure/README.md) · [实验记录](A14) | 6 |
| A15 表征几何与功能路由 | 几何、读出、原生使用、实际分发与专家学习分别立证。 | [Anchor 索引](../problem_anchors/15_spectral_representation_and_functional_routing/README.md) · [实验记录](A15) | 67 |
| A16 负载控制与梯度干扰 | 负载目标的相互作用与同层增量的功能路由。 | [Anchor 索引](../problem_anchors/16_load_control_gradient_interference/README.md) · [实验记录](A16) | 5 |
| A17 共享与干扰学习 | 条件规则、呈现次数、局部更新、自然文本几何与保持。 | [Anchor 索引](../problem_anchors/17_shared_and_interference_learning/README_cn.md) · [实验记录](A17) | 19 |

## 正式记录与支持材料

每个正式实验的 Protocol 持有设计、审阅、批准及修订；Summary 是结果首读入口，Detailed 保存完整证据与偏差。运行内的自动摘要不能替代实验根目录的正式记录。此目录不存在某项结果文件时，不据目录存在声称它已执行或完成。

`supporting_records/`、`historical_support/`、`sources/` 保存归属明确的支持材料和来源。A15_17 的 SAE 预训练及表征支持材料由该 owner 收纳；A15_19 和 A17_12 的历史支持仍为背景，不各自升格成正式 Anchor。[archive/](archive/) 保留退役材料；不从历史运行名自动派生新的科学身份。

原始输出、模型／字典权重、完整激活、大缓存与未筛选日志留在执行仓库。本仓库保存正式文本、脚本、配置和小型可核查证据；运行权限与保存要求由 [项目规则](../../AGENTS.md) 及所属协议决定。原路径、新位置和保留的不可变运行身份见 [迁移记录](../organization_migrations/20261022/README_cn.md)。
