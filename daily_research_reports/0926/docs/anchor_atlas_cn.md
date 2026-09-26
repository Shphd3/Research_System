# 全部 Anchor 判定图与逐条来源

状态：`DERIVED_AI_DRAFT_FOR_HUMAN_JUDGMENT`。2026-09-26 来源快照；未修改任何科学状态或既有文件，未删除。

项目范围内独立 Anchor 共 121 份：118 份非归档、3 份归档。另列 3 份近期待归属草案，总计 124 张卡。中英文伴随稿、日期阅读副本不重复计数。非归档不等于当前活跃；研究者的最终认识与去留判定保持空白。

![全部 Anchor 判定总览](../figures/anchor_atlas_all_20260926.png)

[矢量图，适合放大](../figures/anchor_atlas_all_20260926.svg) · [来源清单及 SHA-256](../report_assets/anchor_atlas_data.json) · [生成脚本](../report_assets/render_anchor_atlas.py)

## 如何判定

每张卡依次是：研究问题、来源记录中的证据、AI 压缩的有界认识更新。科学结论是否接受由你决定。本图没有将运行完成、工程通过、描述性相关或前驱实验转换为机制确认，也没有打开封存的确认数据。没有结果摘要只表示归档缺口，不能推断工作没有运行。

可在最后一列填写：保留当前问题、合并导航、退出当前议程、待补证据；若要删除，另指明具体文件并批准。父子问题有包含关系不代表文件重复，反例与失败记录仍可能需要保留。

## 范围与编号

- A00 是入口跳转，不是独立 Anchor；未发现独立 A03/A08 Anchor。历史 A02 位于 05 线，A04 位于 09 线。
- 两份 A15_08_06 是不同问题，分别标为 8B 复现和语义子空间；没有更改编号。
- A14 的旧版归档与现版同号，但问题和证据不同；图中分别列出。
- 三份根目录日期草案尚未纳入 from 的正式 Anchor 所有权链；列出不代表激活新主线。
- 来源优先于本图。默认依据对应 Anchor 的证据与边界；发现结果记录更新时补核，并标出记录不同步或缺口。未逐一复算全部历史原始数组。

## 逐条来源与留白判定

### 形成与路由基础 · A01—A10

**A01 · 共同结构的定义与识别**

| Anchor / 类型 | 在做什么 | 证据 | 认识更新（AI 待审） | 你的判定 |
|---|---|---|---|---|
| [A01_01](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/01_common_operator_mechanism/01_01_common_operator_identifiability_anchor.md) · Anchor | 如何定义并识别“共同方向”？ | 4 类准则给出的最佳估计器随构造条件改变。 | 共同激活、共同梯度与共同功能不是同一对象。 | — |
| [A01_02](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/01_common_operator_mechanism/01_02_ground_truth_projector_recovery_anchor.md) · Anchor | 已知真值时能否找回共同子空间？ | 合成真值下，激活、均值、梯度等方法各有胜负。 | 估计器必须匹配目标；尚未验证通用的自然数据估计器。 | — |
| [A01_03](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/01_common_operator_mechanism/01_03_gradient_common_vs_activation_common_anchor.md) · Anchor | 共同激活能否代表共同优化方向？ | 4 类失配构造中，梯度交集比激活主成分更贴近优化真值。 | 激活相似不能替代更新兼容性。 | — |
| [A01_04](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/01_common_operator_mechanism/01_04_feedback_common_preservation_bridge_anchor.md) · Anchor | 共同分量能否解释反馈与分区保持？ | 受控移除/回放有效；真实文本中低秩共同分量不足以解释崩塌。 | 受控桥接成立，真实训练还涉及状态和门控共同变化。 | — |

**A05 / 历史 A02 · 初始化与分路锁定**

| Anchor / 类型 | 在做什么 | 证据 | 认识更新（AI 待审） | 你的判定 |
|---|---|---|---|---|
| [A02](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/05_failure_mechanism/02_ntp_style_top1_router_lockin_anchor.md) · Anchor | 下一词训练为何早期锁定某种分路？ | 玩具任务去偏置后正确分组由 3/10 增至 6/10；好初始分区 10/10。 | 早期分区会被保留；不能直接推断真实语言模型。 | — |
| [A05_01](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/05_failure_mechanism/05_01_geometric_inhibition_anchor.md) · Anchor | 几何抑制能否阻止路由集中？ | 9/9 最终集中案例在初始时已偏向同一专家。 | 路由一致不等于专家有功能分工。 | — |
| [A05_02](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/05_failure_mechanism/05_02_feature_assumption_relaxation_anchor.md) · Anchor | 放松特征假设后抑制法仍有效吗？ | 简单目标可达满分，但家族分组仍弱且不稳定。 | 任务答对不足以验证分路机制。 | — |
| [A05_03](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/05_failure_mechanism/05_03_uniform_collapse_common_offset_anchor.md) · Anchor | 共同偏移是否决定均匀任务的崩塌？ | 消除共同打分使初始最大负载约 0.62→0.28；后续仍依赖种子。 | 共同项影响初始吸引区域，但不是完整解释。 | — |
| [A05_04_01](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/05_failure_mechanism/05_04_01_uniform_feature_specialization_after_position_removal_anchor.md) · Anchor | 去掉位置后能否学成特征分工？ | 初始集中减弱，训练后仍会重新集中。 | 位置是部分原因；特征分工尚未成立。 | — |
| [A05_04_02](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/05_failure_mechanism/05_04_02_dotproduct_common_logit_causality_anchor.md) · Anchor | 共同打分对点积路由有何因果作用？ | 无位置玩具中的消除与时序干预改变分区和反馈。 | 支持该受控构造的因果关系，未推广至真实文本。 | — |
| [A05_04_03](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/05_failure_mechanism/05_04_03_real_text_common_logit_initialization_anchor.md) · Anchor | 真实文本初始化由共同项主导吗？ | 残差打分间隔 0.2364 大于共同项 0.1237；中心化降低负载集中。 | 共同项会偏置负载，但并非初始化打分的主导项。 | — |

**A06 · 从分区到专家功能**

| Anchor / 类型 | 在做什么 | 证据 | 认识更新（AI 待审） | 你的判定 |
|---|---|---|---|---|
| [A06_00](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/06_geometry_proxy_preservation/06_00_functional_specialization_contract/06_00_functional_specialization_contract_anchor.md) · Anchor | 怎样才算真正的专家功能分化？ | 同样完美的分组标签，正确与打乱的训练暴露产生不同功能。 | 必须测留出任务效用，标签一致度不够。 | — |
| [A06_01](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/06_geometry_proxy_preservation/06_01_geometry_and_state_discovery/06_01_geometry_and_state_discovery_anchor.md) · Anchor | 能否发现并保持可用的状态分区？ | 正确分区几何可构造；所测选择器失败，真实代理训练会改写几何。 | 发现分区、保住分区、用好分区需分别验证。 | — |
| [A06_02](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/06_geometry_proxy_preservation/06_02_partition_preservation_dynamics/06_02_partition_preservation_dynamics_anchor.md) · Anchor | 哪些动力学使分区保持或翻转？ | 低尾间隔、背景更新方向、门控移动共同决定跨界。 | 不存在仅靠一个静态间隔的通用保证。 | — |
| [A06_03](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/06_geometry_proxy_preservation/06_03_utility_binding_and_sparse_discovery/06_03_utility_binding_and_sparse_discovery_anchor.md) · Anchor | 稀疏探索能否把路由绑定到专家价值？ | 正确暴露和挑战者探索均 128/128 成功；仅更新所选专家 0/128。 | 受控条件下探索可建立功能绑定，尚非大模型结论。 | — |
| [A06_04](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/06_geometry_proxy_preservation/06_04_real_workload_utility_headroom/06_04_real_workload_utility_headroom_anchor.md) · Anchor | 真实任务是否有稳定的专家价值余量？ | 真实代码任务交互为正，但可恢复余量 0.00540 的区间跨零。 | 没有获得稳定且可恢复的专家价值证据。 | — |
| [A06_04_01](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/06_geometry_proxy_preservation/06_04_real_workload_utility_headroom/subanchors/06_04_01_context_conditioned_expert_utility_anchor.md) · 子 Anchor | 上下文能否稳定决定哪个专家更有用？ | 交互 0.01163 为正；最优专家身份不稳，恢复余量不足。 | 可能是某专家更有害，不能直接称为可利用分工。 | — |

**A07 · 嵌套骨架、干扰与功能绑定**

| Anchor / 类型 | 在做什么 | 证据 | 认识更新（AI 待审） | 你的判定 |
|---|---|---|---|---|
| [A07](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/07_features_overlap/07.md) · Anchor | 嵌套共同骨架能否解释干扰与分路？ | 受控骨架、尾部更新控制、正确分路功能分别有结果。 | 这些是受控环节证据，尚未连成自然语言机制。 | — |
| [A07_01](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/07_features_overlap/07_01_common_rare_conflict_metric_audit_anchor.md) · Anchor | 嵌套分布能否形成稳定共同骨架？ | 偏斜构造在 8 个种子形成稳定晚期能量；平衡对照对齐较弱。 | 支持该构造的骨架形成，未测得真实任务干扰。 | — |
| [A07_02](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/07_features_overlap/07_02_common_controlled_rare_interference_anchor.md) · Anchor | 控制共同子空间能否改善尾部学习？ | 联合置信度/子空间控制改善尾部损失约 0.1075。 | 支持受控更新处理；尚非完整优化器或通用方法。 | — |
| [A07_03](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/07_features_overlap/07_03_route_function_binding_anchor.md) · Anchor | 正确嵌套分路是否对应专家功能？ | 正确分路消融选择性 0.5699，对照随机分路 0.0107。 | 外供正确分区有功能；学得的路由尚未被证明。 | — |
| [A07_04](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/07_features_overlap/07_04_common_rare_gradient_conflict_splitting_anchor.md) · Anchor | 分路能否减少共同—稀有梯度冲突？ | 中心化的冲突和稀有损失改变量较小，种子波动较大。 | 尚无稳定证据把功能收益归因于冲突拆分。 | — |
| [A07_05](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/07_features_overlap/07_05_common_update_interference_diagnostic_anchor.md) · Anchor | 共同更新是否实际伤害稀有目标？ | 直接更新伤害 0.00168，低于预设 0.005 门槛。 | 局部效应未达规则；真实数据桥接未形成结果。 | — |
| [A07_06](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/07_features_overlap/07_06_projected_common_rare_conflict_splitting_anchor.md) · Anchor | 投影分路收益是否由冲突降低解释？ | 稀有损失改善约 0.1538，但冲突下降仅 0.0036，准确率未变。 | 性能变化不能单独识别“拆分冲突”机制。 | — |

**A09 / 历史 A04 · 频率与稀有判别**

| Anchor / 类型 | 在做什么 | 证据 | 认识更新（AI 待审） | 你的判定 |
|---|---|---|---|---|
| [A04](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/09_common_rare_spectral_discrimination/04_ntp_zipf_feature_factorization_anchor.md) · Anchor | 频率偏斜影响路由还是特征写入？ | 非下一词玩具出现高频各向异性与尾部欠拟合；重加权可恢复。 | 启发了归因问题，未证明下一词训练的路由成因。 | — |
| [A09_01](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/09_common_rare_spectral_discrimination/09_01_common_band_rare_discrimination_anchor.md) · Anchor | 共同高方差方向是否保留稀有判别？ | 共同带与判别方向错配约 0.486；部分指标改善不伴随任务改善。 | 几何分离和稀有功能恢复必须同时核对。 | — |

**A10 · 频率谱与学习稳定性**

| Anchor / 类型 | 在做什么 | 证据 | 认识更新（AI 待审） | 你的判定 |
|---|---|---|---|---|
| [A10_01](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/10_optimizer_learning_rate_mechanism/10_01_common_projected_sgd_lr_anchor.md) · Anchor | 移除共同方向能否提高稳定学习率？ | Anchor 主要记录机制设想；未给出直接稳定学习率结果。 | 目前是待检验命题，不能当成已验证优化规律。 | — |
| [A10_02](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/10_optimizer_learning_rate_mechanism/10_02_frequency_singular_sgd_instability_anchor.md) · Anchor | 频率谱是否造成随机梯度下降不稳定？ | 受控高学习率压制稀有学习；裁剪等可救回，但未达晚期失稳定义。 | 稀有学习受压不等于已证明全训练失稳机制。 | — |

### 监督、组合与复用 · A11—A14

**A11 · 监督信号如何变成功能**

| Anchor / 类型 | 在做什么 | 证据 | 认识更新（AI 待审） | 你的判定 |
|---|---|---|---|---|
| [A11_01](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/11_informative_future_branch_mechanism/11_01_informative_horizon_supervision/11_01_informative_horizon_supervision_anchor.md) · Anchor | 更远监督何时提供有效学习信号？ | 有信息目标进入预测范围后直接信号出现；输出对齐也有影响。 | 起作用的是信息内容与方向，不是预测步数本身。 | — |
| [A11_01_01](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/11_informative_future_branch_mechanism/11_01_informative_horizon_supervision/subanchors/11_01_01_information_and_geometry_controls_anchor.md) · 子 Anchor | 信息量与输出几何能否分开？ | 受控内容/几何对照复现信息目标被覆盖时的信号变化。 | 不能把更长监督范围直接解释成更强能力。 | — |
| [A11_02](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/11_informative_future_branch_mechanism/11_02_hidden_to_parameter_transmission/11_02_hidden_to_parameter_transmission_anchor.md) · Anchor | 隐状态收益能传到实际参数更新吗？ | 直接传递 5/5 为正；加入所有位置背景后 1 个种子净效应反转。 | 路径可达不保证总体更新有益。 | — |
| [A11_02_01](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/11_informative_future_branch_mechanism/11_02_hidden_to_parameter_transmission/subanchors/11_02_01_reachability_and_background_sign_anchor.md) · 子 Anchor | 传递失败来自不可达还是背景抵消？ | 直接路径可达；背景项足以改变净更新方向。 | 应分清局部信号与整次优化步的结果。 | — |
| [A11_03](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/11_informative_future_branch_mechanism/11_03_cross_position_standard_head_use_boundary/11_03_cross_position_standard_head_use_boundary_anchor.md) · Anchor | 学到的状态是否被后续标准输出头使用？ | 当前位置状态效用为正，下一位置为负；行为收益不稳定。 | 状态可读并不证明后续计算实际利用。 | — |
| [A11_03_01](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/11_informative_future_branch_mechanism/11_03_cross_position_standard_head_use_boundary/subanchors/11_03_01_cross_position_proxy_falsification_anchor.md) · 子 Anchor | 跨位置代理指标是否真的测到使用？ | 状态代理和真实行为不一致，部分打乱对照未获资格。 | 代理不通过时不能宣称跨位置功能使用。 | — |
| [A11_03_02](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/11_informative_future_branch_mechanism/11_03_cross_position_standard_head_use_boundary/subanchors/11_03_02_standard_head_causal_use_anchor.md) · 子 Anchor | 更严格干预能否证明标准头因果使用？ | 匹配后的因果使用测试未见稳定增益；各目标都可读相关分支。 | 尚无多步预测特有的标准头使用收益。 | — |

**A12 · 组合任务与容量边界**

| Anchor / 类型 | 在做什么 | 证据 | 认识更新（AI 待审） | 你的判定 |
|---|---|---|---|---|
| [A12_01](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/12_structured_compositional_mtp_workload/12_01_compositional_workload_capability_gate/12_01_compositional_workload_capability_gate_anchor.md) · Anchor | 两步组合任务是否适合比较学习目标？ | 数据生成有效、格式通过，但学习器答案仍接近随机。 | 学习器资格门槛未过，目标优劣暂不能判定。 | — |
| [A12_01_01](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/12_structured_compositional_mtp_workload/12_01_compositional_workload_capability_gate/subanchors/12_01_01_workload_validity_and_learner_guard_anchor.md) · 子 Anchor | 失败来自任务不合法还是学习器不足？ | 有效生成器下答案约 1/8，格式指标可达 1.0。 | 格式成功不等于组合能力；不是对目标的反证。 | — |
| [A12_02](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/12_structured_compositional_mtp_workload/12_02_interference_capacity_curriculum_boundary/12_02_interference_capacity_curriculum_boundary_anchor.md) · Anchor | 干扰、容量与课程各限制什么？ | 秩 1 时未来目标改善但标准损失变差；秩 2 解开冲突。 | 受控任务中的容量约束不能靠课程凭空消除。 | — |
| [A12_02_01](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/12_structured_compositional_mtp_workload/12_02_interference_capacity_curriculum_boundary/subanchors/12_02_01_rank_and_curriculum_controls_anchor.md) · 子 Anchor | 秩和课程对照能否隔离容量解释？ | 提高容量解除权衡；课程在受限容量下未救回，0/5。 | 支持该线性构造的容量边界，不能泛化成网络定律。 | — |
| [A12_03](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/12_structured_compositional_mtp_workload/12_03_standard_head_causal_use/12_03_standard_head_causal_use_anchor.md) · Anchor | 组合中间态是否被标准头因果使用？ | 前置学习器门槛未过，本项直接干预未运行。 | 仍无结果；前驱局部现象不能代替本项检验。 | — |
| [A12_0](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/12_structured_compositional_mtp_workload/12_0_short_range_single_vs_two_step_composition/12_0_short_range_single_vs_two_step_composition_anchor.md) · Anchor | 短距一步与两步组合能否形成合格对照？ | E04 的 2/4 层候选均未达资格；更早完美拟合有记忆捷径。 | 当前载体不能承载多步预测的功能比较。 | — |

**A13 · 中继必要性与目标作用**

| Anchor / 类型 | 在做什么 | 证据 | 认识更新（AI 待审） | 你的判定 |
|---|---|---|---|---|
| [A13_00](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/13_mtp_task_property_decomposition/13_00_task_properties_to_standard_head_utility/13_00_task_properties_to_standard_head_utility_anchor.md) · Anchor | 什么任务属性使中继表征具有功能？ | 任务相关中继交互 0.2134，8/8 正；软中继目标比较被天花板挡住。 | 受控中继内容有因果作用，未证明多步目标增益。 | — |
| [A13_00_01](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/13_mtp_task_property_decomposition/13_00_task_properties_to_standard_head_utility/subanchors/13_00_01_query_conditioned_relay_carrier_anchor.md) · 子 Anchor | 带查询绑定的中继能否稳定学会？ | 初版准确率约 0.72/0.81；调节可升高但低成本设置不稳定。 | 该载体关闭，不等于中继任务普遍不可学。 | — |
| [A13_00_02](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/13_mtp_task_property_decomposition/13_00_task_properties_to_standard_head_utility/subanchors/13_00_02_single_value_relay_carrier_anchor.md) · 子 Anchor | 简化为单值中继后载体是否合格？ | 两层中继准确率 0.9846，一层约 0.0577，旁路 1.0。 | 得到可用受控载体，尚未产生目标方法收益。 | — |
| [A13_00_03](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/13_mtp_task_property_decomposition/13_00_task_properties_to_standard_head_utility/subanchors/13_00_03_relay_necessity_objective_interaction_anchor.md) · 子 Anchor | 中继必要性是否改变训练目标收益？ | 原目标比较方向为正，但正式门槛未过，结论不足。 | 后续更干净的实验不能追认原实验已经通过。 | — |
| [A13_00_04](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/13_mtp_task_property_decomposition/13_00_task_properties_to_standard_head_utility/subanchors/13_00_04_relay_target_localization_anchor.md) · 子 Anchor | 把监督放在中继位置是否足够？ | 单标签定位实验通过：中继效应 1.0343，交互 0.8747。 | 指定位置的任务标签局部足够；不是普遍监督规律。 | — |
| [A13_00_05](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/13_mtp_task_property_decomposition/13_00_task_properties_to_standard_head_utility/subanchors/13_00_05_task_relevant_relay_target_anchor.md) · 子 Anchor | 任务相关性是否比无关监督更关键？ | 匹配答案/干扰标签下交互 0.2134，8/8 为正且能力门槛通过。 | 受控构造支持任务相关内容的因果作用。 | — |
| [A13_00_06](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/13_mtp_task_property_decomposition/13_00_task_properties_to_standard_head_utility/subanchors/13_00_06_soft_relay_mtp_ntp_audit_anchor.md) · 子 Anchor | 软中继能否区分多步与下一词目标？ | 惩罚可改变路径依赖，但直接任务早饱和；目标比较阶段未运行。 | 载体区分力不足，不是多步预测的负结果。 | — |

**A14 · 层级、关系复用与秩**

| Anchor / 类型 | 在做什么 | 证据 | 认识更新（AI 待审） | 你的判定 |
|---|---|---|---|---|
| [A14_00](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/14_tree_low_rank_language_structure/14_00_tree_low_rank_language_structure/14_00_tree_low_rank_language_structure_anchor.md) · Anchor | 层级语言结构为何可能带来低秩？ | 条件矩阵定理成立；受控全局共享线性传播没有获得支持。 | 数学条件、模型形成与自然语言解释需分开。 | — |
| [A14_01](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/14_tree_low_rank_language_structure/14_01_relation_reuse_parameter_state_bridge/14_01_relation_reuse_parameter_state_bridge_anchor.md) · Anchor | 关系复用能否连接状态秩与参数秩？ | 独立重建观察到复用/规则数变化伴随秩变化，但变量未完全分离。 | 存在关联；尚非频率或复用的单独因果证据。 | — |
| [A14_02](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/14_tree_low_rank_language_structure/14_02_relation_reuse_root_effective_rank/14_02_relation_reuse_root_effective_rank_anchor.md) · Anchor | 共享规则是否降低任务所需状态秩？ | 组合资格、频率对照、稀有更新子空间检验给出不同门槛结果。 | 频率、函数复用、组合能力不能互相替代。 | — |
| [A14_02_01〔旧版归档〕](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/14_tree_low_rank_language_structure/14_02_relation_reuse_root_effective_rank/archive/e02_v1_component_recombination_capability/14_02_01_component_recombination_capability_anchor.md) · 归档 | 已见组件能否可靠组合成未见配对？ | 10 个任务完成；共享条件未见配对门槛 0/5，平均准确率 0.2125。 | 该载体的注册组合能力被否定；不能继续借它论证组合低秩。 | — |
| [A14_02_02〔旧版归档〕](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/14_tree_low_rank_language_structure/14_02_relation_reuse_root_effective_rank/archive/e03_v0_low_frequency_common_mapping_rank/14_02_02_low_frequency_common_mapping_rank_anchor.md) · 归档 | 低频调用是否还使用已学共同映射？ | 旧设计在批准和执行前停止；没有保留正式协议与本项结果。 | 保留历史问题边界，不能把预期结果当作证据。 | — |
| [A14_02_01〔现版〕](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/14_tree_low_rank_language_structure/14_02_relation_reuse_root_effective_rank/subanchors/14_02_01_frequency_mapping_rank_separation_anchor.md) · 子 Anchor | 固定映射后频率本身是否必然增加秩？ | 低/高频平均秩 7.6/7.4；差异上界 0.5，小于预设 2 维界限。 | 低频不必然需要更高功能秩；仅限固定共同映射。 | — |
| [A14_02_02〔现版〕](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/14_tree_low_rank_language_structure/14_02_relation_reuse_root_effective_rank/subanchors/14_02_02_rare_common_subspace_reuse_anchor.md) · 子 Anchor | 稀有更新是否复用共同参数子空间？ | 共同更新子空间捕获率 0.478–0.631；0/10 达到 0.8 门槛。 | 载体准入失败，稀有干预未运行；不能说稀有必须另开方向。 | — |
| [A14_03](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/14_tree_low_rank_language_structure/14_03_state_parameter_functional_rank_demand/14_03_state_parameter_functional_rank_demand_anchor.md) · Anchor | 状态低秩能否推出参数功能低秩？ | 尚缺合格的状态秩因果对照；Anchor 未记录本项完成结果。 | 状态秩到参数秩的桥仍是开放问题。 | — |

### 谱结构与新增可读性 · A15 · 前半

**A15_00 · 输入几何与门控偏好**

| Anchor / 类型 | 在做什么 | 证据 | 认识更新（AI 待审） | 你的判定 |
|---|---|---|---|---|
| [A15_00](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_00_router_input_spectral_geometry/15_00_router_input_spectral_geometry_anchor.md) · Anchor | 真实路由输入偏好哪些方差方向？ | 门控偏向高方差头部，同时保留非零中尾访问。 | 可访问与几何偏好不等于语义或专家价值。 | — |
| [A15_00_01](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_00_router_input_spectral_geometry/subanchors/15_00_01_cross_document_subspace_stability_anchor.md) · 子 Anchor | 共同子空间能否跨文档稳定存在？ | 中心化前 64 维稳定；残差跨文档迁移也高于随机。 | 共享几何存在，但残差不能直接叫噪声。 | — |
| [A15_00_02](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_00_router_input_spectral_geometry/subanchors/15_00_02_gate_common_residual_preference_anchor.md) · 子 Anchor | 门控更偏好共同还是残差方向？ | 共同空间相对残差增益比约 2.83–4.55，原生打分更偏共同。 | 确认偏好，未证明这种偏好带来更好训练。 | — |
| [A15_00_03](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_00_router_input_spectral_geometry/subanchors/15_00_03_condition_local_residual_modes_anchor.md) · 子 Anchor | 不同条件有互不兼容的残差空间吗？ | 条件内更相似，但跨条件仍捕获约 95% 域/92% 主题结构。 | 局部差异存在，强“互不相容子空间”说法不成立。 | — |

**A15_01 · 学习速度与反馈**

| Anchor / 类型 | 在做什么 | 证据 | 认识更新（AI 待审） | 你的判定 |
|---|---|---|---|---|
| [A15_01](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_01_spectral_learning_and_feedback_dynamics/15_01_spectral_learning_and_feedback_dynamics_anchor.md) · Anchor | 谱学习速度与专家反馈如何形成锁定？ | 受控高方差方向学得更快；真实载体稳定性门槛未过。 | 受控动力学成立，真实训练外推尚缺桥梁。 | — |
| [A15_01_01](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_01_spectral_learning_and_feedback_dynamics/subanchors/15_01_01_selected_expert_feedback_lockin_anchor.md) · 子 Anchor | 只更新所选专家会否锁死发现过程？ | 32 个种子中覆盖率约 0.5，正确暴露 0.977，差值 0.477。 | 受控反馈足以造成锁定；未证明真实任务的主因。 | — |
| [A15_01_02](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_01_spectral_learning_and_feedback_dynamics/subanchors/15_01_02_low_variance_functional_delay_anchor.md) · 子 Anchor | 低方差方向是随机还是学得慢？ | 同信噪比头/中/尾均 32/32 学会，尾部达到稳定更晚。 | 受控低方差可表现为延迟，不能直接判成无功能噪声。 | — |

**A15_02 · 逐层语义与谱位置**

| Anchor / 类型 | 在做什么 | 证据 | 认识更新（AI 待审） | 你的判定 |
|---|---|---|---|---|
| [A15_02](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_02_layerwise_representation_spectral_atlas/15_02_layerwise_representation_spectral_atlas_anchor.md) · Anchor | 语义粒度如何随层和谱位置改变？ | 细粒度深层更可读；固定中尾身份在多项对照中不稳定。 | 支持深度相关可读性，不支持通用“细语义在尾部”。 | — |
| [A15_02_01](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_02_layerwise_representation_spectral_atlas/subanchors/15_02_01_controlled_layer_information_identity_anchor.md) · 子 Anchor | 受控组合信息究竟出现在哪层哪带？ | 完整深层状态的答案可读性提高，但固定谱带不稳定胜过随机。 | 信息位置与原生路由实际使用的位置不同。 | — |
| [A15_02_02](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_02_layerwise_representation_spectral_atlas/subanchors/15_02_02_natural_hierarchy_role_localization_anchor.md) · 子 Anchor | 同一概念当父/子角色时位置会变吗？ | 自然文本校准后出现层特异角色选择性；通用父=头部规则不成立。 | 角色相关方向存在，不等于普遍语义层级坐标。 | — |
| [A15_02_03](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_02_layerwise_representation_spectral_atlas/subanchors/15_02_03_architectural_head_channel_concentration_anchor.md) · 子 Anchor | 语义集中在真实注意力头还是任意通道？ | 少数真实头超过随机最大值对照；典型头和固定通道组不通过。 | 少量非随机集中成立，因果语义回路尚未建立。 | — |
| [A15_02_04](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_02_layerwise_representation_spectral_atlas/subanchors/15_02_04_compositional_attention_write_atlas_anchor.md) · 子 Anchor | 更多组合步骤是否使注意力写入移向尾部？ | 三档任务能力均未过门槛；写出端主统计区间跨零。 | 载体不足，不能判定一般组合深度—谱规律。 | — |
| [A15_02_05](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_02_layerwise_representation_spectral_atlas/subanchors/15_02_05_balanced_taxonomy_attention_write_atlas_anchor.md) · 子 Anchor | 平衡粗细标签后细粒度是否额外右移？ | 实际输入增量的深度差为 −0.009573，方向稳定为负。 | 该对象上细粒度额外右移被否定；谱形相似不等于方向相同。 | — |
| [A15_02_06](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_02_layerwise_representation_spectral_atlas/subanchors/15_02_06_mlp_parameter_geometry_and_semantic_location_anchor.md) · 子 Anchor | 参数共同性与语义位置能否组成机制？ | 尾部共同性强于头部；位置结果依赖权重和坐标，用途未确认。 | 联合机制未获支持；共享坐标只是描述量尺。 | — |
| [A15_02_07](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_02_layerwise_representation_spectral_atlas/subanchors/15_02_07_matched_semantic_complexity_anchor.md) · 子 Anchor | 匹配复杂度后仍有细语义谱迁移吗？ | 分类与组合两分支的额外位移和新增线性信息区间均跨零。 | 保留目标共有变化，不支持复杂度特异机制。 | — |

**A15_03 / 04 · 中尾固定带边界**

| Anchor / 类型 | 在做什么 | 证据 | 认识更新（AI 待审） | 你的判定 |
|---|---|---|---|---|
| [A15_03〔归档〕](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/archive/15_03_middle_band_information/15_03_middle_band_information_anchor.md) · 归档 | 中部谱稳定是真结构还是平均假象？ | 记录前驱几何与失败边界；独立共享中带检验未形成结果。 | 该归档设计不能借尾部实验的对照宣称中部有功能。 | — |
| [A15_04](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_04_tail_band_information/15_04_tail_band_information_anchor.md) · Anchor | 局部右移是否进入跨层共享尾部？ | 局部右移复现，但共享尾部富集深度差 −0.103453。 | 注册的共享宽尾解释失败，不能事后缩窄尾部救结论。 | — |

**A15_05 · 谱坐标的功能准入**

| Anchor / 类型 | 在做什么 | 证据 | 认识更新（AI 待审） | 你的判定 |
|---|---|---|---|---|
| [A15_05](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_05_functional_coordinate_admission/15_05_functional_coordinate_admission_anchor.md) · Anchor | 谱坐标能否获准用于专家分流？ | 固定谱带兼容性门槛失败，没有合格坐标，后续匹配训练未运行。 | 静态结构不足以授权功能性分流。 | — |
| [A15_05_01](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_05_functional_coordinate_admission/subanchors/15_05_01_shallow_feature_guidance_anchor.md) · 子 Anchor | 浅层特征能否指导深层专家？ | 受控层特征有身份，但尚无兼容性或全程效率证书。 | 可读浅层信息是候选，不能直接当分流依据。 | — |
| [A15_05_02](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_05_functional_coordinate_admission/subanchors/15_05_02_shallow_feature_specificity_pilot_anchor.md) · 子 Anchor | 浅层头部指导试验能否排除随机坐标？ | 头部与随机子空间均准确率 1.0；特异性 0/10，后续未运行。 | 测量饱和使对照无区分力，并非指导方法已失败。 | — |
| [A15_05_03](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_05_functional_coordinate_admission/subanchors/15_05_03_progressive_band_source_routing_anchor.md) · 子 Anchor | 逐层头—中—尾分流能改善训练吗？ | 浅层接力终点略优，但全程损失更差；局部安排终点也更差。 | 路由和部分功能可改变，未获得全程质量收益。 | — |
| [A15_05_04](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_05_functional_coordinate_admission/subanchors/15_05_04_fixed_band_cross_update_compatibility_anchor.md) · 子 Anchor | 非头部几何能额外预测共同训练兼容性吗？ | 3,072 对完成；无候选在两条模型谱系均超过随机/错层对照。 | 固定谱带的局部兼容性准入失败。 | — |
| [A15_05_05](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_05_functional_coordinate_admission/subanchors/15_05_05_matched_fixed_band_dispatch_anchor.md) · 子 Anchor | 固定谱带分流在匹配训练中是否有益？ | 9 个条件完成 2B；真实头/中/尾/非头均比原生损失高。 | 该单支匹配实验不支持固定带独占分流。 | — |

**A15_06 · 在线谱路由与专家利用**

| Anchor / 类型 | 在做什么 | 证据 | 认识更新（AI 待审） | 你的判定 |
|---|---|---|---|---|
| [A15_06](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_06_online_spectral_routing_and_relay/15_06_online_spectral_routing_and_relay_anchor.md) · Anchor | 在线谱追踪与跨层接力能改善路由吗？ | 10B 配对完成；接力不稳定优于随机，在线平滑追踪工程通过。 | 追踪可行不能代替谱身份的训练价值。 | — |
| [A15_06_01](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_06_online_spectral_routing_and_relay/subanchors/15_06_01_local_random_identity_control_anchor.md) · 子 Anchor | 谱身份是否比同样运动的随机空间更好？ | 两种子谱−随机损失差 −0.005370 / +0.001272。 | 没有可复现的协方差谱身份优势。 | — |
| [A15_06_02](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_06_online_spectral_routing_and_relay/subanchors/15_06_02_router_expert_specialization_anchor.md) · 子 Anchor | 谱路由是否更会利用非同质专家？ | 专家输出/功能确有差异，但谱路由遗憾值和效用绑定未胜随机。 | 专家有差异与路由有效利用差异是两件事。 | — |

**A15_07 · 监督方向与跨域图谱**

| Anchor / 类型 | 在做什么 | 证据 | 认识更新（AI 待审） | 你的判定 |
|---|---|---|---|---|
| [A15_07](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_07_layerwise_conditional_fine_discriminant_directions/15_07_layerwise_conditional_fine_discriminant_directions_anchor.md) · Anchor · [补核1](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_07_layerwise_conditional_fine_discriminant_directions/A15_07_E01_stable_domain_discriminant_subspaces/summary.md) · 记录不同步/缺口 | 监督低维方向能否跨表达保留功能？ | 受控新面板保留率下界 >0.987；自然任务有小增量但秩交点缺失。 | 受控功能迁移成立，自然任务的局部/共享维度关系不足。 | — |
| [A15_07_01](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_07_layerwise_conditional_fine_discriminant_directions/subanchors/15_07_01_layerwise_domain_direction_atlas_anchor.md) · 子 Anchor | 不同领域方向的层间位置和共享度怎样？ | 15/16 域层通过完整增量；均需 7 个输出对比，固定轴稳健性未过。 | 得到依赖坐标的几何图谱，未获共享功能方向。 | — |

**A15_08 · 层新增信息与功能维度**

| Anchor / 类型 | 在做什么 | 证据 | 认识更新（AI 待审） | 你的判定 |
|---|---|---|---|---|
| [A15_08](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_08_target_conditioned_layer_innovation/15_08_target_conditioned_layer_innovation_anchor.md) · Anchor | 层增量提供了旧状态之外什么信息？ | 合格 E04 增量 0.767207；2 维只留 33.24%，低于 80% 规则。 | 局部新增可读性成立，指定二维解释失败。 | — |
| [A15_08_01](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_08_target_conditioned_layer_innovation/subanchors/15_08_01_layerwise_long_range_compositional_innovation_anchor.md) · 子 Anchor | 深层是否增加长距组合的可读信息？ | 必要性×距离交互为正，但远距两跳的绝对新增可读性下降。 | 交互为正不足以说深层获得更多长距信息。 | — |
| [A15_08_02](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_08_target_conditioned_layer_innovation/subanchors/15_08_02_layerwise_conditional_fine_added_accessibility_anchor.md) · 子 Anchor | 哪些层增加条件细粒度可读性？ | 多重校正后仅 24/28 层通过，增量 0.1087 / 0.0653。 | 限定目标和线性读出下成立，不等于新知识或原生使用。 | — |
| [A15_08_03](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_08_target_conditioned_layer_innovation/subanchors/15_08_03_function_admitted_update_representation_rank_anchor.md) · 子 Anchor | 功能增量是否处于稳定低秩空间？ | 24/28 层首次功能保留通过在 256 维；稳定表征低秩联合规则未过。 | 能压缩到 256 维，不等于全局稳定的低维更新云。 | — |
| [A15_08_04](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_08_target_conditioned_layer_innovation/subanchors/15_08_04_transition_object_spectrum_sensitivity_anchor.md) · 子 Anchor | 低秩外观是否由对象定义和归一化造成？ | 整状态谱差异明显；相邻增量差异较小，首位置异常放大原始状态。 | 表观秩依赖对象和尺度；不能把秩一叫语义低秩。 | — |
| [A15_08_05](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_08_target_conditioned_layer_innovation/subanchors/15_08_05_aligned_geometric_rank_scale_anchor.md) · 子 Anchor | 统一模型、样本和指标后秩差还在吗？ | 百万 token 后不同对象仍需数百维，残差化更新较窄但不极低秩。 | 对象/方法差异稳定存在，几何秩尚无功能含义。 | — |
| [A15_08_06〔8B复现〕](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_08_target_conditioned_layer_innovation/subanchors/15_08_06_qwen8b_geometric_rank_replication_anchor.md) · 子 Anchor | 大模型是否复现宽谱与对象差异？ | 百万 token 下宽谱复现；残差化更新相对变窄，绝对仍约 1328 维。 | 存在模型尺度差异，不能推出语义或功能低秩。 | — |
| [A15_08_06〔语义子空间〕](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_08_target_conditioned_layer_innovation/subanchors/15_08_06_semantic_conditioned_functional_subspace_anchor.md) · 子 Anchor · [补核1](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_08_target_conditioned_layer_innovation/A15_08_06_E06_rank_specific_multirepresentation_shared_scaling/summary.md) · 记录不同步/缺口 | 语义条件能否揭示局部与共享功能维度？ | 回顾面板局部 6–7 维、共享 16–25 维；新表达共享交点均缺失。 | 旧“7/56”不能当稳定事实，跨表达扩维未确认。 | — |
| [A15_08_09](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_08_target_conditioned_layer_innovation/subanchors/15_08_09_random_projection_router_preservation_anchor.md) · 子 Anchor | 随机投影能保住已有线性语义结构吗？ | 31/48 层有条件增量；人工审核未定，独立空间低尾间隔为负。 | 条件可读不等于独立可分；投影主检验跳过。 | — |

### 语义功能、自编码与更新 · A15 · 后半 / A16 / 草案

**A15_09 / 10 · 方向复用与功能转移**

| Anchor / 类型 | 在做什么 | 证据 | 认识更新（AI 待审） | 你的判定 |
|---|---|---|---|---|
| [A15_09](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_09_layerwise_coarse_fine_reuse_geometry/15_09_layerwise_coarse_fine_reuse_geometry_anchor.md) · Anchor | 粗细判别方向是否稳定复用？ | 24 个单元几何稳定，但全部原始重叠低于匹配置换中位数。 | 低重叠可复现，正的粗细复用证据未成立。 | — |
| [A15_09_01](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_09_layerwise_coarse_fine_reuse_geometry/subanchors/15_09_01_native_g_domain_consensus_variance_atlas_anchor.md) · 子 Anchor · 记录不同步/缺口 | 原生路由空间是否有跨域共同方向？ | 前驱回顾共享秩 16；本项未见正式结果摘要。 | 跨域共识与方差位置仍需正式证据归档和判定。 | — |
| [A15_10](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_10_cross_parent_fine_function_transfer/15_10_cross_parent_fine_function_transfer_anchor.md) · Anchor | 一个父类的细粒度功能能转移到另一父类吗？ | 0/6 层通过双向、双面板迁移规则。 | 共享细功能未获准；也不能据此证明严格父类局部性。 | — |

**A15_11 / 12 · 专家树与表达边界**

| Anchor / 类型 | 在做什么 | 证据 | 认识更新（AI 待审） | 你的判定 |
|---|---|---|---|---|
| [A15_11](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_11_gradient_consistent_hierarchical_routing/15_11_gradient_consistent_hierarchical_routing_anchor.md) · Anchor | 效用监督能否驱动残差专家树增长？ | 受控正确树有结构作用；效用监督及树相对通用非线性无正增益。 | 未发现层级或效用监督优势，不能推成自动语义树。 | — |
| [A15_12](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_12_semantic_representation_separability/15_12_semantic_representation_separability_anchor.md) · Anchor | 相同事实换表达后能否共用分类边界？ | 单表达库内部可读，跨库边界不兼容；混合训练部分层可兼容。 | 固定事实存在表达依赖；混合同时改变覆盖和样本量。 | — |

**A15_13 · 语义监督与结构路由**

| Anchor / 类型 | 在做什么 | 证据 | 认识更新（AI 待审） | 你的判定 |
|---|---|---|---|---|
| [A15_13](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_13_semantic_supervision_middle_layer_formation/15_13_semantic_supervision_middle_layer_formation_anchor.md) · Anchor · [补核1](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E14_P3_matched_training_semantic_comparison/summary.md) · 记录不同步/缺口 | 末层语义能否组织更有效的中层专家？ | 外供正确分路局部有效；P3 学得语义相对任务路由两种子反号。 | 语义可解释性与稳定任务增益之间仍有缺口。 | — |
| [A15_13_01](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_13_semantic_supervision_middle_layer_formation/subanchors/15_13_01_clinc150_one_layer_backward_hierarchical_router_anchor.md) · 子 Anchor · [补核1](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E03_qwen06b_clinc150_one_layer_backward_hierarchical_router/summary.md) · 记录不同步/缺口 | 末层向中层的监督链改善意图表征吗？ | E03 探针差 −0.0109 / +0.0440 个百分点，合并区间跨零。 | 这一学得层级链尚无可靠表征收益。 | — |
| [A15_13_02](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_13_semantic_supervision_middle_layer_formation/subanchors/15_13_02_frozen_base_staged_semantic_lora_router_anchor.md) · 子 Anchor · [补核1](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E05_clinc150_frozen_base_staged_semantic_lora_router/summary.md) · 记录不同步/缺口 | 冻结底座的分阶段层级能改善细意图吗？ | E05 金标签增益 +0.191 个百分点，区间跨零；父专家干预有作用。 | 父专家有功能，但细意图可分性改进不足。 | — |
| [A15_13_03](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_13_semantic_supervision_middle_layer_formation/subanchors/15_13_03_semantic_gradient_functional_alignment_anchor.md) · 子 Anchor | 真实意图分组是否有梯度和任务价值？ | 正确强制分组优于两对照 0.03126；删除/替换均增加损失。 | 受控强制分组有功能，一步梯度代理未解释多步收益。 | — |
| [A15_13_04](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_13_semantic_supervision_middle_layer_formation/subanchors/15_13_04_m2d2_causal_lm_semantic_routing_anchor.md) · 子 Anchor | 语义分组价值能否扩展到语言建模？ | 金标签强制分路优势 0.001506；学得语义分路仍比任务路由差。 | 真实文本上存在局部外供分组价值，学得路径尚未兑现。 | — |
| [A15_13_05](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_13_semantic_supervision_middle_layer_formation/subanchors/15_13_05_gmm_pseudolabel_oracle_gap_anchor.md) · 子 Anchor | 充分匹配训练后语义监督仍额外有效吗？ | P3 两种子任务−语义损失 +0.010320 / −0.002078。 | 正式结论不足，不能声称可复现语义监督增益。 | — |
| [A15_13_06](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_13_semantic_supervision_middle_layer_formation/subanchors/15_13_06_dclm_final_layer_topk_sae_teacher_anchor.md) · 子 Anchor · [补核1](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E16_dclm_final_layer_topk_sae_teacher/summary.md) · 记录不同步/缺口 | 最终层稀疏自编码器能成为合格教师候选吗？ | E16 完成 1B token，重建误差 0.053382，重载完全一致。 | 技术合格的字典已得到；语义、层级和路由价值待另测。 | — |
| [A15_13_07](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_13_semantic_supervision_middle_layer_formation/subanchors/15_13_07_true_label_layerwise_static_audit_anchor.md) · 子 Anchor | 真实粗细标签在什么层稳定可读？ | 中层描述性峰值可见，但 E19 的 16 项打乱资格中有 5 项失败。 | 静态层位置未正式合格，不能单凭峰值授权功能结论。 | — |
| [A15_13_08](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_13_semantic_supervision_middle_layer_formation/subanchors/15_13_08_dclm_sae_candidate_hierarchy_anchor.md) · 子 Anchor | 自编码特征包含关系能否跨数据复现？ | 1,212 个发现组中 24 组、91 边复现，最大深度 2。 | 有小规模激活包含图，不等于语义父子树。 | — |
| [A15_13_09](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_13_semantic_supervision_middle_layer_formation/subanchors/15_13_09_dataset_conditioned_sae_semantic_hierarchy_anchor.md) · 子 Anchor | 激活包含图是否对应粗细语义分类？ | 仅 2 条语义边通过，覆盖 1 个父类、2 个子类；图形依赖分析数据。 | 局部宽窄关系成立，不支持完整可迁移语义教师树。 | — |
| [A15_13_10](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_13_semantic_supervision_middle_layer_formation/subanchors/15_13_10_sae_flat_router_functional_anchor.md) · 子 Anchor · [补核1](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_13_semantic_supervision_middle_layer_formation/subanchors/15_13_11_structural_routing_incremental_learning_anchor.md) · 记录不同步/缺口 | 自编码/聚类结构正则能改善在线路由吗？ | 固定 0.1 的 A6 四种正则各种子均更差；减弱后仍有种子反号。 | 结构压力可造成损失代价，稳定收益仍未建立。 | — |
| [A15_13_11](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_13_semantic_supervision_middle_layer_formation/subanchors/15_13_11_structural_routing_incremental_learning_anchor.md) · 子 Anchor · [补核1](/data/250010109/MoE_Router/experiments/20260909_a6r1_post_training_analysis/runs/full-20260909T052900Z/completion.json) · 记录不同步/缺口 | 结构路由能否支持增量学习和局部增长？ | A6R1 损失收益不稳定；后训练完成收据存在，正式摘要/详录未写。 | 执行完成不等于增量学习链条已获验证。 | — |

**A15_14 / 15 / 16 · 几何与功能位置**

| Anchor / 类型 | 在做什么 | 证据 | 认识更新（AI 待审） | 你的判定 |
|---|---|---|---|---|
| [A15_14](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_14_semantic_representation_geometric_form/15_14_semantic_representation_geometric_form_anchor.md) · Anchor | 自然领域语义主要在方向、长度还是形状？ | 文本段均值以方向为主、长度也有贡献；末 token 信号近零。 | 结论属于段级领域信息，词汇/主题解释仍然成立。 | — |
| [A15_15](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_15_layerwise_moe_insertion_validation/15_15_layerwise_moe_insertion_validation_anchor.md) · Anchor | 静态可读性是否决定最佳专家插入层？ | 0/10/13 层强制分路都有效；13 对 10 的优势区间跨零。 | 存在多个功能位置，没有唯一最佳层或学得路由证据。 | — |
| [A15_16](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_16_headwise_causal_semantic_retrieval/15_16_headwise_causal_semantic_retrieval_anchor.md) · Anchor | 不同注意力头是否承担不同粗细语义角色？ | 粗细头排名近乎一致；注册头间异质性门槛未过。 | 有描述性可读排名，没有合格的角色分工或因果头。 | — |

**A15_17 · 自编码约束、复用与可分性**

| Anchor / 类型 | 在做什么 | 证据 | 认识更新（AI 待审） | 你的判定 |
|---|---|---|---|---|
| [A15_17](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_17_three_model_sae_representation_trajectory/15_17_three_model_sae_representation_trajectory_anchor.md) · Anchor · 记录不同步/缺口 | 旁路自编码约束如何改变可复用表征？ | E05 局部几何差异、固定面板损失更差；21B 父线未见正式摘要。 | 几何变化未换得该面板质量收益；复用与可分性子线分别判定。 | — |
| [A15_17_01](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_17_three_model_sae_representation_trajectory/subanchors/15_17_01_sae_shared_direction_reuse_anchor.md) · 子 Anchor · [补核1](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_17_three_model_sae_representation_trajectory/A15_17_01_E01_shared_direction_reuse_audit/summary.md) | 更集中是否因为反复使用相同稀疏特征？ | 21B S7−SALL 复用差 +0.085788，区间全正；有效维数约 14.49/17.16。 | 必要预测符合；解码器几何和系数协方差仍是共存解释。 | — |
| [A15_17_02](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_17_three_model_sae_representation_trajectory/subanchors/15_17_02_sae_n8_separability_anchor.md) · 子 Anchor · [补核1](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_17_three_model_sae_representation_trajectory/A15_17_02_E01_n8_17b_separability_audit/summary.md) · 记录不同步/缺口 | 更集中是否伴随更好原生领域区分？ | 17B fresh−Dense +1.4375 个百分点，区间跨零；重加权低 14.9375 点。 | 主要优势不足；集中度不单调对应领域可分性。 | — |

**A16 · 负载控制与功能增量路由**

| Anchor / 类型 | 在做什么 | 证据 | 认识更新（AI 待审） | 你的判定 |
|---|---|---|---|---|
| [A16_00](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/16_load_control_gradient_interference/16_00_switch_lb_gradient_conflict/16_00_switch_lb_gradient_conflict_anchor.md) · Anchor | 负载均衡梯度是否与任务学习冲突？ | 早期反事实梯度有代价，跨阶段不稳定；原 30B 辅助梯度实际断开。 | 不能用影子更新解释原长程负载均衡训练效应。 | — |
| [A16_00_01](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/16_load_control_gradient_interference/16_00_switch_lb_gradient_conflict/subanchors/16_00_01_dc_sustainer_boundary_anchor.md) · 子 Anchor | 共同均值是否维持已经形成的路由崩塌？ | 去真实均值使最大专家份额降 0.68678；反向加回不胜随机。 | 即时维持作用成立，独特累积成因或反向充分性未成立。 | — |
| [A16_00_02](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/16_load_control_gradient_interference/16_00_switch_lb_gradient_conflict/subanchors/16_00_02_multistage_gradient_pathway_anchor.md) · 子 Anchor | 中心化是否在所有训练阶段降低干扰？ | 50M 有收益，6B 反向、10B 混合；两种子全阶段规则失败。 | 支持早期局部缓解，否定统一全阶段解释。 | — |
| [A16_01](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/16_load_control_gradient_interference/16_01_incremental_information_lb_routing/16_01_incremental_information_lb_routing_anchor.md) · Anchor · [补核1](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A16/A16_01_E01_30b_incremental_information_lb_routing/detailed.md) · 记录不同步/缺口 | 真实负载均衡下新增信息路由能改善训练吗？ | 详录到共同 20B：收益种子反号，各功能门槛失败；30B 判定缺失。 | 阶段结果不足，不能将旧启动状态当作当前运行状态。 | — |
| [A16_01_01](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/16_load_control_gradient_interference/16_01_incremental_information_lb_routing/subanchors/16_01_01_regret_distilled_conditional_innovation_anchor.md) · 子 Anchor | 专家遗憾值蒸馏能否给增量路由功能资格？ | 有冻结准入与后续训练协议；未见本项完成结果记录。 | 这是待证的功能准入方案，不是已有效的新路由。 | — |

**待归属的近期草案 · 不计为正式项目 Anchor**

| Anchor / 类型 | 在做什么 | 证据 | 认识更新（AI 待审） | 你的判定 |
|---|---|---|---|---|
| [草案 D1 · 0924](/data/250010109/Research_System/daily_research_reports/0924/docs/plan/anchor_cn.md) · 未归属草案 · [补核1](/data/250010109/Research_System/daily_research_reports/0924/docs/analysis/dev_rollback_reading_cn.md) | 共享参数更新是否产生可分离的域间干扰？ | 18 条轨迹及开发集诊断完成；确认集仍封存。 | 仅有开发集趋势，尚无正式机制确认结论。 | — |
| [草案 D2 · 0925](/data/250010109/Research_System/daily_research_reports/0925/docs/update_compatibility/anchor_cn.md) · 未归属草案 · [补核1](/data/250010109/Research_System/daily_research_reports/0925/docs/update_compatibility/detailed.md) | 可分任务是否存在稳定的负兼容更新对？ | 15 对均可分，但 0 对同时通过两半负梯度夹角筛选；训练未运行。 | 筛选载体失败，不等于更新干扰不存在。 | — |
| [草案 D3 · 0925](/data/250010109/Research_System/daily_research_reports/0925/docs/human_semantic_updates/anchor_cn.md) · 未归属草案 · [补核1](/data/250010109/Research_System/daily_research_reports/0925/docs/human_semantic_updates/summary.md) | 人类语义距离能否预测共享更新代价？ | 640 条轨迹；交互约 0.001631，区间跨零；格式/动态资格不足。 | 未确认语义距离预测干扰；自编码特征尚未测。 | — |

## 图件来源与复现

图件是本清单的派生阅读视图，所有图件物理位于同日 figures/。`anchor_atlas_data.json` 保存每张卡的完整来源路径、SHA-256、补核记录与空白人工判定；没有复制原始运行日志或数据。

- `/data/250010109/Research_System/daily_research_reports/0926/report_assets/anchor_atlas_data.json` — SHA-256 `0fe77e4c85dfa0e064e11a804dfc77fc4e27aa3007281f120a56d4406a99850e`
- `/data/250010109/Research_System/daily_research_reports/0921/report_assets/fonts/NotoSansCJKsc-Regular.otf` — SHA-256 `2c76254f6fc379fddfce0a7e84fb5385bb135d3e399294f6eeb6680d0365b74b`
- `/data/250010109/Research_System/daily_research_reports/0926/figures/anchor_atlas_all_20260926.png` — SHA-256 `835902529890fb0f4bed87d9880843bbf6b071ca0d593ccbf36b74c1a6a6332b`
- `/data/250010109/Research_System/daily_research_reports/0926/figures/anchor_atlas_all_20260926.svg` — SHA-256 `3ef08d9cf306ba97d7690814092a42cfa1b2b00d3c4192c1403b8b4c5831c077`

生成命令：

```bash
python /data/250010109/Research_System/daily_research_reports/0926/report_assets/render_anchor_atlas.py
```
