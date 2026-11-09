# 10月31日研究地图更新：新增问题、归属与证据位置

[完整地图](research_map_cn.md) · [English](research_map_update_20261031.md) · [逐项核对清单](research_map_refresh_20261031.json)

从10月22日的登记版本到现在，正式问题从 **145个增加到159个**：新增4个独立父问题、10个局部子问题。13条研究线保持不变。另有旧问题下的新轮次，不能只按新增Anchor计数。

归类整体合理。本次修的是地图遗漏、过期描述和跨问题入口；保留原编号与研究归属。此次未运行实验，未改变科学接受状态。

## 先用七个问题理解新增工作

### 1. 自然语言响应 → 领域分解与三域复核

**要问：** 固定词后还响应什么？领域偏向成员是否等于独立语义或独立谱区？

**已有记录：** 450篇新文档复核中，旧名单的16个“严格单域”成员都在物理文本激活。领域偏向可以观察，但旧命名不能直接外推为领域专属。

[A15_27](research_map_cn.md#a15-27) · [A15_27_01](research_map_cn.md#a15-27-01) · [A15_27_02](research_map_cn.md#a15-27-02) · [A15_27_03](research_map_cn.md#a15-27-03) · [A15_27_04](research_map_cn.md#a15-27-04)

### 2. 学习经历 → 哪些状态差异影响作答

**要问：** 顺序与混合学习得到的差异，哪些真会影响答案？

**已有记录：** 把混合模型的16维状态差移入顺序模型，旧题准确率从0升至80.88%；每道题仍需要供体状态。训练保护策略另在A17检验。

[A15_25_02](research_map_cn.md#a15-25-02) · [A17_04](research_map_cn.md#a17-04)

### 3. 统计关系 → 功能依赖的资格

**要问：** 反复出现或共同变化，是否意味着预测依赖和可复用？

**已有记录：** 布尔组合子问题尚未运行；上下文计算依赖子问题每类只匹配到23例，低于64例要求，按规则停止，未做干预。

[A15_25_01](research_map_cn.md#a15-25-01) · [A15_25_03](research_map_cn.md#a15-25-03)

### 4. 频率与保留方向 → 实际更新后果

**要问：** 加common、隔离裁剪或限制补空间，是否真能改善低频预测？

**已有记录：** 改变裁剪确实改变更新，但两种子低频收益方向相反。限制更新方向虽比其他更新少伤害，仍比原保存模型差。

[A15_24](research_map_cn.md#a15-24) · [A15_24_01](research_map_cn.md#a15-24-01) · [A15_24_02](research_map_cn.md#a15-24-02) · [A15_24_03](research_map_cn.md#a15-24-03)

### 5. 已有单项 → 低频组合学习

**要问：** 训练格式下会单项，是否已经有可跨语境调用的组成计算？

**已有记录：** 符号任务和订单任务均未通过完整的单项／组合资格，尚不能据此回答“真正掌握单项以后能否复用”。

[A15_26](research_map_cn.md#a15-26)

### 6. 句内位置 → 同坐标延续还是图关联替换

**要问：** 前后位置仍是同一坐标，还是能用旧边说明替换？

**已有记录：** 有限匹配范围内，同一坐标在句内额外延续；旧图约99%的覆盖率仍未通过背景对照，不能据此认定发生了替换。

[A15_28](research_map_cn.md#a15-28)

### 7. 数值计算 → 是否改变一次学习更新

**要问：** 数学等价的Router实现是否产生不同且有任务作用的更新？

**已有记录：** 60行合成校准已完成，真实训练状态回放尚未运行。它检查更新的数值实现，归A10优化问题。

[A10_03](research_map_cn.md#a10-03)

## 重点更新怎样改变读法

- **A15_27_04 / R11 A02已经执行。** 450篇新文档、462次前向。旧两域面板中的16个“严格单域”成员，在新增物理文档中全部激活。因此旧命名不能直接外推为跨领域专属。新三域主成员为129/133/27个；整体复核未建立，不能把运行完成写成假设通过。
- **A15_25_02提供状态干预结果。** 16维供体状态差把旧题准确率从0恢复到80.88%，等规模随机对照为0.12%。它仍依赖每道题的混合学习供体状态，不是已经学会自主修复，也没有找出独立规则模块。
- **A15_28已经有结果。** 匹配范围内存在额外同坐标延续；严格匹配只覆盖SAE候选对的2.19%、CrossCoder的1.48%。旧图边覆盖很高，但完整背景控制未通过。SAE的第二项分析受接口不匹配阻塞。
- **A15_25_03只执行了数据资格检查。** 匹配后每类最多23例，低于预定64例；模型前向为0，功能干预未运行。不能把它理解成共同计算不被使用。
- **A15_24和A17的新轮次测试学习后果。** 优化耦合、有限状态干预、持续训练后的保持收益分别报告；某个局部对照较好，不自动代表相对训练前变好。

每个数值的对象、对照和边界仍以地图卡片链接的原结果记录为准。

## 新增14个正式问题

“父问题”有独立决策；“子问题”检验其父问题的一部分。下面只说明归属，不授予科学认可。

| 编号 | 归属 | 在问什么 | 当前事实位置 |
|---|---|---|---|
| A10_03 | 独立父问题，属A10 | [固定同一模型、完整目标和优化器历史，等价的稳定数值计算是否改变超出回放误差的一步任务损失作用？](problem_anchors/10_optimizer_learning_rate_mechanism/10_03_router_numerical_update_fidelity_anchor.md) | [设计／结果原件](research_notes/router_numerical_fidelity/20261024_scope_audit.md)；[地图说明](research_map_cn.md#a10-03) |
| A15_24_01 | A15_24 | [只排除 common 梯度对路由专家裁剪分母的贡献，能否稳定改善低频 feature 的最终预测？](problem_anchors/15_spectral_representation_and_functional_routing/15_24_frequency_composition_common_path/subanchors/15_24_01_common_optimizer_coupling_anchor.md) | [设计／结果原件](experiments/A15/15_24_frequency_composition_common_path/common_optimizer_coupling_20261022/summary.md)；[地图说明](research_map_cn.md#a15-24-01) |
| A15_24_02 | A15_24 | [严格保留选定矩阵响应时，补空间限制的条件是什么；这样限制实际 AdamW 位移后，低频预测怎样变化？](problem_anchors/15_spectral_representation_and_functional_routing/15_24_frequency_composition_common_path/subanchors/15_24_02_frequency_complement_anchor.md) | [设计／结果原件](experiments/A15/15_24_frequency_composition_common_path/frequency_complement_20261023/summary.md)；[地图说明](research_map_cn.md#a15-24-02) |
| A15_24_03 | A15_24 | [同一次参数改动的预测影响，是否在匹配条件后仍随特征TRAIN激活频率不同？](problem_anchors/15_spectral_representation_and_functional_routing/15_24_frequency_composition_common_path/subanchors/15_24_03_frequency_effect_association_anchor.md) | [设计／结果原件](experiments/A15/15_24_frequency_composition_common_path/frequency_effect_association_20261024/summary.md)；[地图说明](research_map_cn.md#a15-24-03) |
| A15_25_01 | A15_25 | [反复出现的表征分量是否影响布尔组合预测，能否从单条件语境迁入？](problem_anchors/15_spectral_representation_and_functional_routing/15_25_joint_feature_graph/subanchors/15_25_01_component_reuse_anchor.md) | [设计／结果原件](experiments/A15/15_25_01_component_reuse/20261022/protocol_cn.md)；[地图说明](research_map_cn.md#a15-25-01) |
| A15_25_02 | A15_25 | [学习经历如何改变条件规则的表征，以及哪些方向对任务作答最重要？](problem_anchors/15_spectral_representation_and_functional_routing/15_25_joint_feature_graph/subanchors/15_25_02_learning_history_representation_anchor.md) | [设计／结果原件](experiments/A15/15_25_02_learning_history_representation/20261023/summary.md)；[地图说明](research_map_cn.md#a15-25-02) |
| A15_26 | 独立父问题，属A15 | [已学组成能力能否支持条件组合，更新与分支效用需要哪些资格证据？](problem_anchors/15_spectral_representation_and_functional_routing/15_26_low_frequency_compositional_reuse/15_26_low_frequency_compositional_reuse_anchor.md) | [设计／结果原件](experiments/A15/15_26_low_frequency_compositional_reuse/20261024_order_v2/summary.md)；[地图说明](research_map_cn.md#a15-26) |
| A15_25_03 | A15_25 | [同一token换上下文时，在第14层削弱共同候选C，是否特异改变第28层上下文方向R和预测？](problem_anchors/15_spectral_representation_and_functional_routing/15_25_joint_feature_graph/subanchors/15_25_03_context_computation_dependency_anchor.md) | [设计／结果原件](experiments/A15/15_25_03_context_computation_dependency/R01_bounded_execution_20261026/summary_cn.md)；[地图说明](research_map_cn.md#a15-25-03) |
| A15_27 | 独立父问题，属A15 | [同一目标词的前文含义改变，能否使既有feature跨措辞响应并抵抗指定词面诱饵？当前父设计聚焦这一问题；后继领域差异由子Anchor分别持有。](problem_anchors/15_spectral_representation_and_functional_routing/15_27_natural_language_feature_response/15_27_natural_language_feature_response_anchor.md) | [设计／结果原件](experiments/A15/15_27_natural_language_feature_response/R01_bounded_panel_20261026/summary.md)；[地图说明](research_map_cn.md#a15-27) |
| A15_28 | 独立父问题，属A15 | [一句话前面的feature到后面是同坐标延续、旧图关联出现，还是不再出现，并且是否超过匹配背景？](problem_anchors/15_spectral_representation_and_functional_routing/15_28_sentence_feature_continuation/15_28_sentence_feature_continuation_anchor.md) | [设计／结果原件](experiments/A15/15_28_sentence_feature_continuation/R01_cached_sentence_pairs/summary_cn.md)；[地图说明](research_map_cn.md#a15-28) |
| A15_27_01 | A15_27 | [同一个目标token处的数学/生物上下文差异能否跨措辞复现，且在总体谱哪里可读出？](problem_anchors/15_spectral_representation_and_functional_routing/15_27_natural_language_feature_response/subanchors/15_27_01_fixed_target_domain_spectrum_anchor.md) | [设计／结果原件](experiments/A15/15_27_natural_language_feature_response/R07_fixed_target_domain_spectrum_20261029/summary.md)；[地图说明](research_map_cn.md#a15-27-01) |
| A15_27_02 | A15_27 | [两域主要变化空间是否相近，混合方差来自域内还是领域中心差？](problem_anchors/15_spectral_representation_and_functional_routing/15_27_natural_language_feature_response/subanchors/15_27_02_within_mixed_subspaces_anchor.md) | [设计／结果原件](experiments/A15/15_27_natural_language_feature_response/R08_within_mixed_subspaces_20261029/summary.md)；[地图说明](research_map_cn.md#a15-27-02) |
| A15_27_03 | A15_27 | [哪些固定成员组成同一目标的领域均值差，字典遗漏多少，频率与谱位置怎样连接？](problem_anchors/15_spectral_representation_and_functional_routing/15_27_natural_language_feature_response/subanchors/15_27_03_domain_difference_decomposition_anchor.md) | [设计／结果原件](experiments/A15/15_27_natural_language_feature_response/R09_domain_difference_decomposition_20261029/summary.md)；[地图说明](research_map_cn.md#a15-27-03) |
| A15_27_04 | A15_27 | [完整字典中能区分领域文本的成员，在出现率、共同谱及真实输入响应上如何分布；这些描述能否扩展到新文档和第三个领域？](problem_anchors/15_spectral_representation_and_functional_routing/15_27_natural_language_feature_response/subanchors/15_27_04_domain_member_atlas_anchor.md) | [设计／结果原件](experiments/A15/15_27_natural_language_feature_response/R11_three_domain_replication_20261030/summary_A02_cn.md)；[地图说明](research_map_cn.md#a15-27-04) |

## 归类核对与这次修正

| 对象 | 核对结果 | 本次处理 |
|---|---|---|
| A10_03 | Router数值误差影响学习更新，属于A10 | 保留归属，与表征结果分开 |
| A15_24及三个子问题 | 更新策略、优化耦合与频率关联，属于同一策略问题的不同检验 | 保留父子关系，逐项补当前证据边界 |
| A15_25_02 ↔ A17_04 | 前者分析学习得到的表征，后者持有训练来源及保持实验 | 增加跨问题阅读链接，不改父归属 |
| A15_26、A15_28 | 分别问组合学习和句内延续，有独立对象 | 保留独立父问题，不因共用资产合并 |
| A15_27_01—04 | 分别持有R07、R08、R09、R10/R11子问题 | 保留正式登记；实验轮次留在原目录 |
| A15_27父文档 | 当前正文聚焦R06固定词含义；后继子问题范围更广 | 在地图显式提示范围差异；本次不改写科学设计 |
| 地图与索引 | 地图漏A15_25_03、A15_27_04；两项原件引用过期，多个计数滞后 | 补至159项、84父问题、75子问题；更新哈希、入口和轮次说明 |

**仍需研究者决定的边界：** A15_27是否需要正式扩大父设计范围，留在其科学owner中决定。本次地图明确R06与后继子问题的差别，已经可以完整导航。

## 使用地图时分清五个量

1. **出现频率：** 字典坐标在多少token／文档上激活。
2. **训练暴露：** 模型训练时见过某类关系或组合多少次。
3. **谱位置：** 一个向量的能量落在某组主方向上的比例。
4. **输入中的贡献：** 给定输入时，实际激活加权后对状态或差值的贡献。
5. **领域可区分性：** 根据状态或坐标能否区分领域标签。

这些量有联系，但互不替代。可读出、改变预测、改善学习仍需不同证据。地图连线表示登记归属；卡片中的“相关问题”只表示阅读或来源联系。

## 范围与复核

精确文件名为`summary_cn.md`的新增记录有42份，另有R11的`summary_A02_cn.md`。这些记录包含资格失败、数据关卡和补充轮次，不能称为42次成功独立实验。计数依据、文件清单及修复前缺口见[审计清单](research_map_refresh_20261031.json)。

原Anchor、Protocol、Summary、Detailed及冻结科学状态保持原件。本轮只维护派生地图与导航；本地阅读副本会记录来源和未打包的依赖。GitHub可见性以实际提交／推送为准。
