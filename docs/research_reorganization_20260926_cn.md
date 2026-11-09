# 项目重构与编号清理记录（第一轮入口重构已完成）

**第一轮已完成项目入口和规则重构；导师原始讨论是当前路线的主要依据。编号映射仍是检索方案，实体 Anchor 路径、科研状态和待确认删除项保持各自原有身份。**

本轮把 PROJECTS 压缩为项目归属、工作流和证据入口；两层 AGENTS 合并重复规则并按任务引用已有合同；长篇项目历史移入[注明日期的快照](archive/project_map_20260926_before_refactor.md)。实施范围、读取量对比和检查结果见[重构验收](archive/process_records/research_system_astra_review_20260926_cn.md)。上一阶段完成的四组 Anchor 措辞修订保留，候选科学解释仍标 AI_PROPOSAL。

## 当前默认推进：以导师原文和已有证据为依据

2026-09-26 已完整读取研究者补充的《0924-指导.md》；本轮以其中导师的直接要求为准，未以学长建议设定推进顺序。导师要求先弄清可检验的相互影响，展示实际表征结构和能量，再研究参数更新与表征、预测后果的关系。低秩、相关或语义远近导致伤害是待检验猜想；“99%能量在300维”是示意数字。稀疏自编码器（SAE）是分析工具。

[最新结果](../research/from-attention-to-search/main/experiments/shared_updates/structure_update/20260926/summary_cn.md)中的结构图与局部更新后果已完成。尚缺的是对受影响的下游表征在更新前后的变化及其解释作用的测量，不能把已有梯度关系和损失变化称为完整机制解释。当前均值帮助也必须保留；不以找到伤害作为推进成功。

具体阅读与推理依赖见[当前 roadmap](../research/from-attention-to-search/main/roadmap.md)。它不是新的实验顺序或执行合同。正在继续的“0926-共享参数冲突整理分析”对话负责该分析的结果、图稿、Focus及科学讨论；这轮没有改写这些文件，也未创建并行科学设计。

下面的十类编号、L1–L7审计和D01/D02删除候选保留其原有边界。它们不自动开启十项任务，也不把未确认的科学收束或删除变成已批准操作。

**术语解释：**Anchor 是一个研究问题及其可裁决设计；Focus 是研究者当前推进的问题和下一决定；稀疏自编码器（SAE）用少量激活特征重建表征；多词预测（MTP）指同时监督后续多个位置；机制研究要区分现象为何发生，方法比较要判断一种做法在约定条件下是否更有效。

## 1. 编号的逻辑

先定义研究对象，再分别理解形成过程、结构和信息后果，最后把方法比较单独列出。第 2–8 线是相关但独立的解释/测量分支，数字相邻不表示存在已证明的因果链，也不表示必须逐线完成后才能研究方法。第 9–10 线明确承认自己在比较方法；方法效果本身不能替代第 2–8 线的机制判断。

1. **主线用 1–10。** 同一大类下可有数个独立父问题，不能把一个大类强装成一个当前 Anchor。
2. **父问题用 1.1、1.2……；已有局部子问题用 1.1.1、1.1.2……。** 文件前缀可对应 `01_01`、`01_01_01`。每一层都从 1 开始，本轮拟编号无跳号。
3. **每个问题只归一个主目录。** 跨线关系用链接；不复制一份 Anchor，也不因依赖关系把一个独立问题变成另一个的子问题。当前已有的明确父子关系在对照表中保留。
4. **编号表示归属，不表示重要性、通过、完成或活跃。** 当前推进由已有 Focus/研究者决定。历史归档保留旧标识；日期草案的拟归属不等于正式激活。
5. **实验、种子、图和修复轮次不自动取得新的问题编号。** 能改变独立研究决定才需要独立父问题；否则放回对应实验或局部子问题。
6. **这次批准后统一迁移，之后不随删一项反复洗牌。** 旧号保留在映射中；远程作业、原始产物和冻结协议/收据中的历史标识保留原值，不能把审计用的历史字符串全局替换。

| 新主线 | 核心问题 | 主要旧来源 | 清理方向 |
|---|---|---|---|
| **1. 共同性与功能分工的判定** | 先定义：什么才算共同方向、专家不同且确实有用？ | A01_01–03；A06_00、03、04 | 定义与判据 |
| **2. 路由锁定与分工形成** | 为什么早期分路会被保留，什么过程阻碍功能分工？ | A02、A05；A01_04；A06_01–02；A15_01 | 形成机制 |
| **3. 共享更新、优化与干扰** | 一次更新何时帮助或伤害另一目标，哪些优化过程造成差异？ | A07、A10、A16_00；0924/0925 三份草案 | 更新机制 |
| **4. 监督信号与任务必要性** | 更早的任务相关监督，何时真正改变后续答案计算？ | A11、A12、A13 | 监督机制 |
| **5. 频率、复用与低维结构** | 低维结构来自频率、函数复用，还是构造中的先验假设？ | A04、A09、A14 | 结构解释 |
| **6. 表征结构与测量边界** | 哪些层、谱位置、方向和长度差异可以稳定测到？ | A15_00、02、04、09、14；旧 03 | 描述与测量 |
| **7. 信息增量、使用与迁移** | 额外可读的信息有多少，能否被使用或迁移？ | A15_07、08、10、12、16 | 信息与功能 |
| **8. 稀疏自编码约束与表征变化** | SAE 条件下，集中和复用变化伴随什么信息变化？ | A15_17 及两个子问题 | 约束与表征 |
| **9. 表征坐标驱动的路由方法** | 谱带、接力和增量坐标，是否有超出匹配对照的分流价值？ | A15_05、06；A16_01 | 方法比较 |
| **10. 语义与效用监督的路由方法** | 指定分组的价值能否变成可学习的路由和专家结构？ | A15_11、13、15 | 方法比较 |

完整[新旧编号表](research_reorganization_20260926_mapping_cn.md)覆盖全部 124 项；[CSV](research_reorganization_20260926_mapping.csv)便于筛选；[机器清单](research_reorganization_20260926_manifest.json)记录源文件哈希、处置范围及尚未批准的状态。121 项获得候选编号，其中 3 项是未归属草案；另外 3 项保留归档身份。[编号总览图](../daily_research_reports/0926/figures/research_lines_renumbered_20260926.png)给出十条线及其旧来源。

具体例子：旧 A06_00 → **1.1**；旧 A15_17 → **8.1**，其复用与领域读出子问题 → **8.1.1、8.1.2**。两个同名旧 A15_08_06 分别成为 **7.2.6（8B 几何复现）**和 **7.2.7（语义条件功能子空间）**，不再靠旧短编号猜来源。

## 2. 可以明确指出的逻辑/设计问题

以下保存审计发现和处理状态。L1–L4 所述旧句已经修订；“依据”中的行号指修订前审计位置，原判断见[上一版推理审计](archive/process_records/reasoning_audit_20260926_research_logic_cn.md)，前后哈希见[修订清单](../daily_research_reports/0926/report_assets/reasoning_anchor_revisions_20260926.json)。L5 是问题过载，L6 是对照设计实质失效，L7 是执行与证据资格失败；这些边界不因改写而成为支持证据。

### L1：逻辑命题过强；不是整条线无效

**处理状态：**文字已修订；科学候选待研究者确认。

**来源：**[A07_04](../research/from-attention-to-search/main/problem_anchors/07_features_overlap/07_04_common_rare_gradient_conflict_splitting_anchor.md)。

**审计发现：**把“共享有害”限定为必须存在负梯度夹角；同时用冲突降低与损失改善共同发生来支持因果中介。

**依据：**Anchor 第 34–36、52–54、167 行。有限步长下，即使梯度同向，源目标更新也可能越过另一目标最优点而伤害它。

**最强竞争解释：**有限步长、曲率、容量或其他优化变化造成代价；负夹角只是某些条件下的一阶指标。

**处置：**删去无条件 only when；把实际独立目标损失变化作为互害证据，将梯度指标限定为局部预测；已有结果保留。

**区分办法：**从同一状态做源目标更新，固定更新范数/步长规则并读取独立目标；要归因冲突还须让候选冲突过程相对对照单独改变。

### L2：必要条件与交互证据混用

**处理状态：**文字已修订；科学候选待研究者确认。

**来源：**[A13_00](../research/from-attention-to-search/main/problem_anchors/13_mtp_task_property_decomposition/13_00_task_properties_to_standard_head_utility/13_00_task_properties_to_standard_head_utility_anchor.md)、[A13_00_05](../research/from-attention-to-search/main/problem_anchors/13_mtp_task_property_decomposition/13_00_task_properties_to_standard_head_utility/subanchors/13_00_05_task_relevant_relay_target_anchor.md)。

**审计发现：**父 Anchor 说辅助监督仅在中继为必要路径时才有效；当前结果建立的是受控条件下更大的相对收益。

**依据：**父 Anchor 第 27–29、41–43 行为 only when，第 204 行则称 controlled sufficient condition；中继 0.2315、绕过 0.0181、交互 0.2134。

**最强竞争解释：**必要性放大收益，但非必要时仍可通过优化或其他学习路径带来小收益。

**处置：**把主张收窄为已测任务相关性×必要性条件下的收益差；不把交互为正当作普遍必要性。保留 A13_00_05 的有效实验。

**区分办法：**先用已有中继/绕过的匹配对照裁决交互；若继续主张必要性，必须明确非必要条件的收益界与反例判据。

### L3：机制比较同时改变两个关键因素

**处理状态：**文字已修订；科学候选待研究者确认。

**来源：**[A15_05_03](../research/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_05_functional_coordinate_admission/subanchors/15_05_03_progressive_band_source_routing_anchor.md)。

**审计发现：**用浅层接力与深层本地坐标的胜负区分“稳定性”与“新增信息”；两者在这组比较中一起变化。

**依据：**Anchor 第 21、26、34–41 行；第 64 行还明确没有等维随机调度训练对照。

**最强竞争解释：**信息来源、瓶颈或一般正则作用，而非稳定性本身解释方法差异。

**处置：**保留该实验的有界方法比较，删除从这组胜负单独确定稳定性机制的推断；停止原封不动重复头—中—尾排程。

**区分办法：**若仍有独立理由研究稳定性，固定信息来源和维数再比较坐标运动；先问能否构造这种独立操纵，不能就保留机制未知。

### L4：方法成败裁决了过多机制命题

**处理状态：**文字已修订；科学候选待研究者确认。

**来源：**[A15_06](../research/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_06_online_spectral_routing_and_relay/15_06_online_spectral_routing_and_relay_anchor.md)。

**审计发现：**把接力方法最终损失不胜出写成全部物理先验为假；把胜出预先归因于跨层漂移减少。

**依据：**Anchor 第 40–41、46–47 行；第 125–129 行却分别记录平滑追踪通过、接力终点收益不支持。

**最强竞争解释：**追踪确实有效，但信息来源或瓶颈代价抵消其作用；也可能收益只来自中心化。

**处置：**删除一揽子先验否决与未经隔离的 because；分开追踪、谱身份、接力收益三条结论。保留随机匹配对照和负结果。

**区分办法：**优先采用已有运动匹配随机对照收束谱身份主张；工程追踪效果不能直接用终点质量反推真伪。

### L5：问题过载；不等于数据失效

**处理状态：**保留审计边界；未更改实验或科学状态。

**来源：**[A15_08_03](../research/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_08_target_conditioned_layer_innovation/subanchors/15_08_03_function_admitted_update_representation_rank_anchor.md)。

**审计发现：**声称只有一个条件问题，却同时要求回答新增信息、参数谱位置、秩、层深和 token 几何。

**依据：**Anchor 第 20–26 行。其注册对照与边界已有明确设计，不应笼统称为“无逻辑实验”。

**最强竞争解释：**几何与坐标变化可能并无功能信息增加；多张图的一致外观不能代替决定性比较。

**处置：**从默认待办中移除独立的“再画一种几何图”；保留一个主裁决，其余作为该裁决所需的控制或历史证据。

**区分办法：**先选“稳定低维投影是否保留已合格增量”这一明确问题；其他读数仅在排除命名的对手时保留。

### L6：实质性的对照设计失效

**处理状态：**保留审计边界；未更改实验或科学状态。

**来源：**[A15_08](../research/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_08_target_conditioned_layer_innovation/15_08_target_conditioned_layer_innovation_anchor.md)；[A15_08_E01_layer25_conditional_innovation_matrix Summary](../research/from-attention-to-search/main/experiments/A15/15_08_target_conditioned_layer_innovation/A15_08_E01_layer25_conditional_innovation_matrix/summary.md)、[A15_08_E04_strict_conformance_repair Summary](../research/from-attention-to-search/main/experiments/A15/15_08_target_conditioned_layer_innovation/A15_08_E04_strict_conformance_repair/summary.md)。

**审计发现：**A15_08_E01 的循环标签替换仍保留全局可学习的一一映射，未构造出目标无关对照。

**依据：**E01 Summary 明确 PRIMARY_H2_INELIGIBLE_CONTROL_DESIGN，不能裁决层增量假设。

**最强竞争解释：**额外读出容量仍可以解码被重命名的目标，不能用该对照分离目标信息。

**处置：**从确认性支持证据中排除 E01，以已修复 E04 为该轮后续结果入口；保留 E01 作为失效设计记录。

**区分办法：**修复必须破坏目标对应关系而保持相关容量，且遵守冻结和独立确认；本线已有 E04，不因此再启动实验。

### L7：执行/证据资格失效；并非核心问题没有逻辑

**处理状态：**保留审计边界；未更改实验或科学状态。

**来源：**[A15_08](../research/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_08_target_conditioned_layer_innovation/15_08_target_conditioned_layer_innovation_anchor.md)；[A15_08_E02_fresh_balanced_mismatch_repair Summary](../research/from-attention-to-search/main/experiments/A15/15_08_target_conditioned_layer_innovation/A15_08_E02_fresh_balanced_mismatch_repair/summary.md)、[A15_08_E03_fresh_confirmation_freeze_repair Summary](../research/from-attention-to-search/main/experiments/A15/15_08_target_conditioned_layer_innovation/A15_08_E03_fresh_confirmation_freeze_repair/summary.md)、[A15_08_E04_strict_conformance_repair Summary](../research/from-attention-to-search/main/experiments/A15/15_08_target_conditioned_layer_innovation/A15_08_E04_strict_conformance_repair/summary.md)。

**审计发现：**E02 在冻结前使用了协议不允许的确认标签；E03 未满足注册的身份标识、提取收据及清单要求。

**依据：**E02 Summary 为 INELIGIBLE_PROTOCOL_CONFIRMATION_LABEL_PREUSE；E03 为 INELIGIBLE_GUARD。

**最强竞争解释：**协议与结果不一致使该轮不能承担确认性判断；不等于已证明效应不存在。

**处置：**从正向证据链排除 E02/E03 的假设判决；修复链折叠为历史记录，保留具体失败原因和原产物。

**区分办法：**使用已有合格 E04 的有界结果，不通过改旧协议或删除失败文件使旧数值重新合格。

L1 的一个可复核反例：令 \(L_A(x)=(x-1)^2/2\)，\(L_B(x)=(x-0.1)^2/2\)，在 \(x=0\) 两梯度分别为 \(-1\)、\(-0.1\)，方向相同。以步长 1 对 A 更新到 \(x=1\) 后，A 损失从 0.5 降为 0，B 从 0.005 升为 0.405。它只反驳“不加条件的必要性”，不否定小步长下的一阶梯度分析。

相反，A15_15 关于可读性最高层的预测可以被结果否定，这本身是合法研究。三个位置都表现出功能价值、唯一最优未定，应该保留这种认识限制，不能仅因预测未成就把实验判为混乱。A15_17_02 的结果不足以及 0925 筛选停止也必须保留；不足和负结果不是删除证据的理由。

## 3. 建议退出默认推进的具体分支

这是待确认的阅读/议程收缩建议，不是已经修改科学状态。若某分支本来已经关闭，只纠正旧入口，不再次宣告关闭。P1–P4 的收益是减少自动延续的工作；P5 是维护历史边界。

| 编号 | 范围与直接来源 | 为何应收束 | 执行后保留什么 / 何时可重开 |
|---|---|---|---|
| P1 | 固定谱带及头—中—尾排程作为默认方法路线：[A15_05_03](../research/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_05_functional_coordinate_admission/subanchors/15_05_03_progressive_band_source_routing_anchor.md)、[A15_05_05](../research/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_05_functional_coordinate_admission/subanchors/15_05_05_matched_fixed_band_dispatch_anchor.md) | 已有固定带比较和排程结果未建立可重复的整体功能收益；不能从层/谱外观继续推出方法必然有效。 | 从默认待做中移除该原方案；保留其方法比较和停止边界。 重开条件：新的独立功能证据显示坐标相对等维随机或错误层控制有额外价值。 |
| P2 | 在线接力必然因谱身份改善质量的原方法主张：[A15_06](../research/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_06_online_spectral_routing_and_relay/15_06_online_spectral_routing_and_relay_anchor.md)、[A15_06_01](../research/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_06_online_spectral_routing_and_relay/subanchors/15_06_01_local_random_identity_control_anchor.md)、[A15_06_02](../research/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_06_online_spectral_routing_and_relay/subanchors/15_06_02_router_expert_specialization_anchor.md) | 接力收益不支持，运动匹配随机对照后谱身份优势不跨种子稳定；平滑追踪成功单独成立。 | 不再默认扩大原接力训练；将方法结果与可复用工程组件分开记录。 重开条件：新问题明确改变了哪个已失败前提，并提供可分离对照；不能只增加预算。 |
| P3 | A15_08 E01–E03 修复链作为多个并行项目或确认性支持：[A15_08](../research/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_08_target_conditioned_layer_innovation/15_08_target_conditioned_layer_innovation_anchor.md) | E01 对照失效、E02/E03 资格失效，已有 E04 合格修复。 | 当前入口只保留 E04 及一条修复历史索引；旧协议和结果不删除。 重开条件：只在复核资格或复现来源时展开，不自动重新执行。 |
| P4 | 未合格或饱和载体上继续作训练目标优劣比较：[A12_01](../research/from-attention-to-search/main/problem_anchors/12_structured_compositional_mtp_workload/12_01_compositional_workload_capability_gate/12_01_compositional_workload_capability_gate_anchor.md)、[A12_01_01](../research/from-attention-to-search/main/problem_anchors/12_structured_compositional_mtp_workload/12_01_compositional_workload_capability_gate/subanchors/12_01_01_workload_validity_and_learner_guard_anchor.md)、[A12_0](../research/from-attention-to-search/main/problem_anchors/12_structured_compositional_mtp_workload/12_0_short_range_single_vs_two_step_composition/12_0_short_range_single_vs_two_step_composition_anchor.md)、[A13_00_01](../research/from-attention-to-search/main/problem_anchors/13_mtp_task_property_decomposition/13_00_task_properties_to_standard_head_utility/subanchors/13_00_01_query_conditioned_relay_carrier_anchor.md)、[A13_00_02](../research/from-attention-to-search/main/problem_anchors/13_mtp_task_property_decomposition/13_00_task_properties_to_standard_head_utility/subanchors/13_00_02_single_value_relay_carrier_anchor.md)、[A13_00_06](../research/from-attention-to-search/main/problem_anchors/13_mtp_task_property_decomposition/13_00_task_properties_to_standard_head_utility/subanchors/13_00_06_soft_relay_mtp_ntp_audit_anchor.md) | A12 的可学性/捷径问题与 A13 的旧查询载体、软中继天花板会阻断目标裁决；合格单值载体与后续有效结果应保留。 | 把载体资格及修复收回第 4 线的支持证据，不作为一串当前独立项目。此建议不是宣布整个 MTP 方向停止。 重开条件：先有可学、无绕过、未饱和的对照载体，再决定目标比较。 |
| P5 | 已归档的三个历史 Anchor：[A14_02_01〔旧版归档〕](../research/from-attention-to-search/main/problem_anchors/14_tree_low_rank_language_structure/14_02_relation_reuse_root_effective_rank/archive/e02_v1_component_recombination_capability/14_02_01_component_recombination_capability_anchor.md)、[A14_02_02〔旧版归档〕](../research/from-attention-to-search/main/problem_anchors/14_tree_low_rank_language_structure/14_02_relation_reuse_root_effective_rank/archive/e03_v0_low_frequency_common_mapping_rank/14_02_02_low_frequency_common_mapping_rank_anchor.md)、[A15_03〔归档〕](../research/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/archive/15_03_middle_band_information/15_03_middle_band_information_anchor.md) | 它们分别是已关闭反例、执行前停止草案和执行前归档提案；科学含义不同。 | 维持历史身份，从新编号的当前目录中分离；不重复归档，不把未运行改成负结果。 重开条件：保留各自原有条件；本方案不主动重新激活。 |

**A15_13 的额外整理要求：**第 10 线可以容纳语义监督、教师资格、结构路由、增量学习，但这些不能在同一 Focus 被当成一个已经获准自动展开的大计划。已完成的教师、层级图、静态读出及失败控制归回各自证据；研究者选定下一决定之前，不把每项技术产物都升级为新的当前项目。本表保留现有来源的父子关系，正式拆并需确认具体问题。

**与近期主问题的关系：**第 8 线的表征变化、第 3 线的更新互害、第 9/10 线的分配价值可以互相提供证据，但没有一条自动成立的“更集中 → 更语义 → 梯度更兼容 → 路由更好”链。先选择其中一个未知，再决定哪个实验能让两种解释产生不同预测。

## 4. 本轮可提交审批的实体文件删除

此前扫描发现 42 组完全相同正文、43 份额外副本；“相同”不等于没有独立职责。当前只建议第一批删除下列两份孤立/别名正文，已再次核对哈希。其他 4 份跨日副本仍需确认逐日自包含的用途；其余 36 组没有加入删除名单。

| 编号 | 拟删除 | 必须保留 | 字节数 |
|---|---|---|---|
| D01 | [0923_SAE_N8_组会汇报整理稿.md](../daily_research_reports/0923/docs/draft/0923_SAE_N8_组会汇报整理稿.md) | [0923_SAE_N8_组会汇报整理稿.md](../daily_research_reports/0923/docs/0922_SAE_N8_separability_v3/0923_SAE_N8_组会汇报整理稿.md) | 20,528 |
| D02 | [随机降维与可路由低维语义结构_正式证明与实验协议.md](../daily_research_reports/backup/2026/08/0823/docs/随机降维与可路由低维语义结构_正式证明与实验协议.md) | [random_projection_router_proof_protocol.md](../daily_research_reports/backup/2026/08/0823/docs/random_projection_router_proof_protocol.md) | 50,269 |

删除执行前必须再查引用与哈希，因为本审阅材料也新增了候选路径引用。本清单只授权范围提案，不授权删除其他同名或相邻文件。唯一 Protocol、Summary、Detailed、失败记录、已归档原设计、新增未版本化证据，以及运行目录/检查点均不在删除范围。

## 5. 整理后的最小工作方式

每个当前问题先写六句：看到了什么；还不知道什么；我的解释；最强竞争解释；两者在哪个结果上不同；三类结果分别改变什么决定。第 5 句写不出来，先澄清问题；三类结果都只是继续调参，就将其明确归为方法迭代，或重新设计机制比较。

本方案不把 10 条目录设成 10 条活跃线，也不要求立即重写 121 份文档。先选一个当前问题，处理该问题的断点；其余按已有状态收回证据导航。旧 A11/A12/A13 和 A14 等线包含可用的机制分解、反例与有效结果，不应为了目录简洁而整线抹掉。

## 6. 审阅和实施范围

- **第一轮已落实：**PROJECTS、roadmap、根与项目 AGENTS 已完成结构收缩；历史正文已归档，入口检查器已适配。讨论稿属于上一阶段的改动，本轮按并发边界保留。
- **编号方案仍待审：**确认 10 条线及全量归属后才迁移路径；当前只保留检索映射。
- **推理文字已修：**L1–L4 共六份 Anchor 已收窄；L5–L7 保留审计/资格边界，不改实验。正式认识更新仍由研究者确认。
- **默认推进已收缩：**方法分支不自动进入本轮；P1–P5 的原科学状态和历史记录保持，未整线归档或删除。
- **实体删除仍待认可：**仅 D01、D02 共 70,797 字节列入候选；未执行。

按研究者先前“我认可以后需要删除”的要求，未实施实体删除。当前改写请求已用于修订默认入口与逻辑措辞，不推定为批准编号迁移或新的实验。编号提案没有替代 PROJECTS/Focus；本轮不声称已完成全仓迁移验收。

当前入口检查覆盖47项，文件均存在；8项尚未版本化，包括原有A15_17_02的5项以及本轮新纳入检查的3项0926文档。保留这些提示，未做git add/commit。完整验收见[第一轮记录](archive/process_records/research_system_refactor_20260926_checks.json)。

