# Research_System 研究推理续审：从“为什么”到实验判别

状态：**AI 审阅意见与改写草案，待研究者判断**。日期：2026-09-26。本文是派生审阅材料，不是新的 Anchor、Focus、Protocol 或科学结论来源；未修改原设计、判据、科学状态，未删除文件。

本轮使用 [research-reasoning-auditor](../.agents/skills/research-reasoning-auditor/SKILL.md)。覆盖 12 条主线，浏览 121 份项目 Anchor 与 3 份日期草案的问题定义；在其中 30 份重点核对关键假设、比较设计或结论边界，并对读 12 份结果摘要中的结论与边界。另检查若干关联 Anchor 的边界、主线索引和当前 Focus。这不是对每份全文、全部原始数组或全部历史版本的重新验证。阅读清单与源文件 SHA-256 见 [审阅来源](reasoning_audit_20260926_research_logic_sources.json)。

## 1. 直接判断

**不能把这些 Anchor 概括为“都没有逻辑”，也不能根据文档认定研究者经常把因果方向写反。更明显的问题是：描述结构、解释成因、预测功能、改进方法这几种任务经常相互接续，却没有始终说明当前究竟在回答哪一种问题。** 一条局部设计可以很严谨，但多条设计串起来以后，原来的“为什么”仍然悬着。

同时，确实存在可定位的逻辑问题：把候选机制写成必要条件，把受控充分条件写成“只有如此才成立”，以及用方法的终点胜负同时裁决一组局部机制。它们需要修正；不能只靠结尾的一长段“不能声称”补救。

从 A15_05、A15_06、A15_11、A15_13、A16_01 的问题定义看，方法导向确实明显：不少问题直接问某个指定结构能否提高效果。这是正当的研究类型，但它不能自动回答模型原来的现象为何出现。以下评价针对文档与研究组织，不是对研究者能力或每次思考过程的判断；AI 协助形成的方案和叙述也应接受同样审计。

术语：**代理指标**是便于测量、却只反映目标某一侧面的量；**因果中介**是某个改动通过它影响结果的中间变量；**必要条件**指没有它就不会发生，**充分条件**指有它就足以发生。观察到“条件存在时成功”，不能直接证明该条件必要。

## 2. 反复出现的断点是什么

下面是从多条研究线重建的风险链，并非任何一份 Anchor 已经完整主张了这条链：

> 发现表征有某种结构 → 将结构解释为语义组织 → 设想它对应专家分工 → 设计分路方法 → 方法指标变化 → 回过头解释最初的结构。

这里有四个需要独立检验的连接：

| 连接 | 为什么不能自动成立 | 所需的区分 |
|---|---|---|
| 更集中 → 语义组织更好 | 共同均值、尺度、无关变化收缩，也会使表征集中 | 同面板上的目标可读性或指定功能是否被保留，而非只看秩 |
| 标签可读 → 原模型使用 | 外加分类器可以利用原模型没有使用的方向 | 在模型实际计算中干预该信息并测目标行为 |
| 语义相近 → 更新兼容 | 同类内容可能要求冲突更新，异类内容也可能共享有益更新 | 在同一参数状态上直接测独立样本的跨组损失变化 |
| 改方法有效 → 原机制解释正确 | 改动可能同时改变容量、优化、负载、尺度或信息来源 | 把方法总效果与指定中介的贡献分别检验 |

严格的“因果倒置”是将原因和结果互换。这里更常见的风险是**观察符合一个假说，便把它当作唯一解释**，或**某项改动改善了结果，便倒推出原问题一定由该因素造成**。合理地提出解释不算错误；缺少区分竞争解释的证据，却把解释写成结论，才是错误。

## 3. 可直接定位、值得先修的表述

### 3.1 A07_04：负梯度关系被写成有害共享的必要条件

[原文第 34–35 行][a07conf]写的是“专家共享只有在共享梯度冲突时才有害”；第 52–53 行又以冲突减少且稀有损失改善作为“减少冲突帮助稀有特征”的支持。

第一句范围过强。负梯度内积在指定的小步梯度下降近似下有解释作用，但不能覆盖有限步长、曲率、优化器状态或容量限制下的所有有害共享。第二处同时观察两项改善，也不能单独识别“正是冲突减少造成损失改善”这一中介。

**建议替换草案：**“在本实验指定的更新规则和步长下，更新方向不相容是跨组损失上升的候选解释。主证据是从同一状态施加来源组更新后，独立目标组的损失变化；梯度关系解释该结果，但不替代它。”

最小数学反例：令两任务损失分别为 $L_A(x)=(x-1)^2/2$、$L_B(x)=(x-0.1)^2/2$。在 $x=0$ 两梯度为 $-1$ 和 $-0.1$，方向一致。对 A 做步长为 1 的梯度下降，得到 $x=1$；A 损失从 0.5 降到 0，B 损失却从 0.005 升到 0.405。因此有限步下不能把“负梯度夹角”当作实际互损的必要条件。这是逻辑反例，不是项目实验结果。

针对机制的最小比较应固定参数状态、优化器状态、来源组更新与独立目标组样本，并检验步长变化、实际施加的更新以及有针对性的方向对照。若只比较两个完整路由方法，仍可能留下多个共同变化的原因。

### 3.2 A13_00：子实验的充分条件不能升级为父命题的必要条件

[父 Anchor 第 27–29、41–43 行][a13parent]写“只有中间状态处于必经路径上，额外监督才有功能价值”。但同一父文档第 204 行及[任务相关中继实验][relayresult]保留的是一个**受控充分条件**。

子实验发现：必须通过中继时，答案相关监督相对干扰监督的学习收益更大。中继路径的收益为 0.2315，旁路为 0.0181，交互为 0.2134，均沿原摘要的损失曲线面积定义理解。**更大不等于其他路径绝无收益；这个设计也没有排除所有可能产生辅助监督收益的机制。**

**建议替换草案：**“在这个受控任务中，早期监督与答案变量对齐，且后续计算依赖被监督状态时，可以产生有限训练预算内的额外收益；该收益在必经中继条件下更大。路径必要性是不是普遍必要条件，仍未建立。”

如果将来真要判断“必要”，需要针对该必要性主张寻找有效反例或设计相应干预；继续复现当前充分条件并不能完成那个证明。原实验的局部正结果应保留，不因父文档措辞过强而作废。

### 3.3 A15_05_03／A15_06：方法胜负被用来解释中间机制

[A15_05_03 的 H2][schedule]把“浅层接力胜出”对应到坐标稳定性，把“接力落败”对应到深层需要新信息。但换信息来源同时改变了可用内容、坐标变化和训练适配，单次胜负不足以区分这些解释。

[A15_06 第 46–47 行][online]的 H2 写“接力更好，因为共享浅层来源减少跨层搜索漂移”；第 40–41 行又把整组先验的真假绑定到终点是否胜过对照。然而第 125 行开始记录了追踪模块通过，而接力训练收益不成立。

**建议替换草案：**“方法是否改善任务损失、追踪是否减少坐标变化、坐标变化是否中介任务收益，分别判定。方法没有收益，不自动否定追踪有效；方法有收益，也不自动证明收益由漂移减少造成。”

若科学目标是解释漂移，应尽可能独立改变坐标更新方式与信息来源，并核对其他预算；如果做不到，保留“该实现的效果比较”，不写成漂移机制已经被识别。现有运动匹配随机对照是有价值的修复；它的[结果][randomresult]也确实没有给协方差谱身份稳定优势。

### 3.4 A15_13：目标结构、性能参照与自然形成机制需要分开

[父 Anchor 开头][semparent]已经指定末层教师、粗到细专家树、去除粗方向等方法部件。这可以检验一种人工构造是否有效，但不能回答未经这种干预的原模型为什么自然形成某种表征。第 8 行已经正确保留了这条限制。

同段“真实标签提供上界”也应说明是哪一种上界。真实标签可作为标签正确性的参照；若指任务性能上界，则并无一般保证说，语义标签分区在有限专家容量下就是最优分区。需要区分标签正确与专家最优。

**建议替换草案：**“真实标签提供一个外供语义分区参照；是否具有任务价值、学得的路由能恢复多少价值、价值是否来自语义特异性，分别用匹配对照判断，不预设其为全局性能上界。”

已有结果正说明分开判断的必要性：自然文本上[外供正确路径有局部功能价值][hardresult]，但[学得语义路由未获得相同收益][learnedresult]；进一步的[匹配监督比较][p3result]仍存在种子反号。这些都是可保留的知识，不能为了方法成功而抹平。

### 3.5 A15_08_03：写“一道问题”却同时承担多个判决

[该子 Anchor 第 20–22 行][rankmany]同时询问新增可读性、参数谱位置、表征秩、样本几何、深度变化和稳定低维结构。它有明确的分项判据，因此不是一个简单的逻辑错误；风险是这些量并不共同识别一个唯一的“为什么”。

**建议：**一次机制判断只保留一个待区分的连接。其余量作为条件检查或辅助描述，并说清哪一个结果会改变核心认识。不必为每个指标再新建一条活跃研究线。

### 3.6 父 Anchor 未吸收结果，会让研究看起来一直停在设计阶段

[A15_13 父文档第 76 行][semparent]仍以“完成 E14”为下一决定，而子线已经有 P3 的完整结果。[A15_17_02 原 Anchor][n8anchor]还保留测量前状态；[当前 Focus][n8focus]和[结果摘要][n8result]已写测量完成，研究者认识待确认。

这是文档状态不同步，不应诊断为研究者不懂逻辑。但它会造成实际损害：读者不断看到“再做一个实验”，却看不到已被削弱的解释。

**建议：**先由研究者确认已有证据的有界认识，再同步同一父 Anchor 的当前问题和下一决定。不要用新子 Anchor 代替旧问题的收尾，不把“结果完成”代替研究者最终判断。

## 4. 已有设计中值得沿用的做法

| 例子 | 逻辑上做对的事 | 能学到的习惯 |
|---|---|---|
| [A01_01][common] | 先问“共同”到底按什么准则定义，不把激活共同与优化共同混为一谈 | 先固定科学对象，再选估计器 |
| [A11_01][future] | 明确区分信息进入监督范围、参数传递、普通输出头使用 | 每一轮只推进一个连接 |
| [A13_00_05][relayanchor] | 保持词表、频率、位置等条件，改变监督是否指向后续答案变量 | 给竞争解释一个同样有说服力的对照 |
| [A15_01][speed] | 固定可学习目标后改变方差结构，再看学习速度；没有把真实训练外推当成已完成 | 把受控机制与自然系统中的主因分开 |
| [A15_05][admission] | 静态邻域改变不能通过功能准入；失败后停止该协议的后续训练 | 允许阴性结果真正关闭一个分支 |
| [A15_17_01][reuse] | 明确写复用与集中共现只是必要预测，解码方向和系数共变可同时起作用 | 不用一个符合预期的指标排除未测竞争解释 |
| [A16_00][load] | 区分共同均值维持当前崩塌，与什么训练过程产生该均值和门控状态 | 当前依赖不等于历史形成原因 |
| [0925 更新兼容草案][compat] | 独立区分筛选与验证；没有合格对照就停，不把失败解释成“干扰不存在” | 对照未构造出来，就接受未知 |

这些例子不意味着各原假说全部成功。它们的价值恰恰在于：能解释结果允许改变哪一个判断，又不允许改变哪一个判断。

## 5. 主线应承担什么角色：AI 阅读建议

下表是为减少问题混杂给出的审阅归类，不更改主线优先级、活跃状态或归档状态。

| 主线 | 适合保留的科学任务 | 最需要防止的跳跃 |
|---|---|---|
| A01 | 定义和识别共同对象 | 从某个好估计器直接跳到有效路由 |
| A05／历史 A02 | 受控初始偏置和反馈锁定机制 | 把玩具中的主因当成真实训练通因 |
| A06 | 功能定义、分区保持、专家价值形成与发现 | 把分组正确或负载均衡当作功能分工 |
| A07 | 直接更新互损及其可能机制 | 从梯度代理直接跳到隔离一定更好 |
| A09／历史 A04 | 区分稀有信息写入不足与选择失败 | 把频率、共同方向和语义共享视为同义 |
| A10 | 稳定步长受什么机制限制 | 投影方法有效就声称解释所有优化器差异 |
| A11 | 监督信号、参数传递与后续使用 | 从局部信号直接跳到最终能力 |
| A12 | 为目标比较提供合格任务，以及限定容量机制 | 把修复载体当作已经回答原来的监督问题 |
| A13 | 任务相关监督发挥功能的受控条件 | 把局部充分条件写成普遍必要条件 |
| A14 | 条件定理、复用、状态秩与参数秩之间的桥 | 用“假设低维后保持低维”解释低维如何产生 |
| A15 | 分开表征描述、信息可读、原生使用、路由效用 | 将几何图谱或外加读出直接升级为因果方法依据 |
| A16 | 当前负载控制的功能代价及有用路由信息 | 用冻结状态一步实验解释原有长程训练历史 |

描述性研究有独立价值。若目标就是建立可靠图谱或测量规律，它不必伪装成因果解释。方法研究也不必等到所有机制都证明之后才允许开始；但选做方法研究时，要明确目标已是效果比较，并把机制主张另行限定。

## 6. 用已有自编码结果演示一次认识更新

建议先复盘 A15_17_02，原因是已有正式测量结果，无需新增训练即可练习。当前 Focus 仍将研究者判断留为未知，以下只是示范草案。

**已知现象：**在同一 17B 坐标和领域面板上，重加权条件更集中，却比从头训练条件的领域读出低 14.9375 个百分点；从头训练条件相对稠密基线的主要优势区间跨零。[来源][n8result]

**先分开两种“为什么”：**

1. **为什么更集中？** 可能涉及跨样本重复使用同一字典特征、解码方向相似、系数共变或重建误差。现有复用结果只覆盖其中一个必要预测。若下一步做已有激活和字典的分解，它首先回答当前几何由哪些量构成，仍不等于训练形成原因的因果识别。
2. **这种集中意味着什么？** 它是否保留了领域相关区分，还是主要强化共同/尺度方向，或只是让指定简单读出变难？这才是领域读出实验的直接任务。

**不能直接当目的的写法：**“证明更集中代表更好的语义，然后设计更好的路由。”这已经放入了希望得到的答案。

**可用的目的草案：**“判断这组已观察的集中变化，是否伴随同面板、同读出规则下更强的领域区分，并排除把几何集中直接当成领域可读性的替身。”

**本轮能接受的认识更新草案：**“在这些固定条件中，更集中不单调对应更强的领域可读性。复用和集中可以变化，而领域读出没有相应改善；不能继续仅用集中度为语义改善作证。”

**仍未知：**究竟是哪些训练历史差异产生了变化，信息是否真正丢失还是换了编码形式，以及原模型是否使用这些差异。当前对比不是孤立的正则系数干预，不能回答这些因果问题。

**下一决定应先于下一实验：**先确认上述认识更新是否被接受，以及下一轮究竟要解释“集中怎样形成”还是“读出为什么变差”。若选择后者，当前 Focus 已记尺度或白化检查为 AI 建议；本审阅不将它升级为研究者决定或执行授权。

## 7. 一个足够小的工作习惯

在现有 Anchor 开头形成六句白话即可，不必新增登记系统。建议先由研究者写，再由 AI 审计：

1. **我已经看到：**一个带范围和来源的现象；若没看到，就写“尚待确认是否存在”。
2. **我还不明白：**现象的哪一个具体原因、条件或功能后果。
3. **我的解释是：**哪一个变化通过什么中间过程产生该现象。
4. **最强的另一解释是：**即使我的解释不成立，它怎样也能产生当前观察。
5. **两者会分歧于：**同一比较下分别预期出现什么不同结果。
6. **结果将改变：**支持、不支持、证据不足分别使我保留、放弃或暂缓哪个判断。

第 5 句写不出来，先讨论，不扩成训练矩阵。第 6 句如果无论结果怎样都只是“继续调方法”，应承认这是方法迭代，或重做机制比较。实验可以修改模型；关键是该修改在区分解释还是同时引入了更多解释。

每轮完成后，研究者先不用 AI 写三句话：“我原来如何解释；结果排除了或削弱了什么；我现在仍不能判断什么。”AI 再核对证据与边界。保护这段独立解释时间，比再生成一份长文档更贴近本轮改进目的。

学习入口可直接用本项目的好例子：先读 A11_01 的信号判别，再读 A13_00_05 的竞争对照，最后读 A15_17_01 的必要预测边界。各写一句“少了哪一个对照，两个解释就分不开”。无需先读完整仓库。

## 8. AI 协作也要改变

此前的全量图适合检查遗漏，不宜直接当成推进路线；把每个子检验画成同等大小的卡片，会使测量、修复和独立科学问题看起来一样重要。

后续我的协作应先返回：当前问题类型、最薄弱的一条连接、最强竞争解释、最小区分结果、最多能声称什么。不能先替研究者补出机制，再自动扩成多个方法、多个子 Anchor 和一长列指标。正式写入 Anchor 前，研究者确认问题和认识；确认之后更新原有来源，让已完成的负结果也能缩小后续问题空间。

**优先修订草案：**先审阅 A07_04 的必要条件、A13_00 的必要/充分措辞、A15_06 的方法效果与机制裁决分离；同时完成 A15_17_02 已有结果的研究者认识更新。前者是文本与逻辑修复，后者是研究者拥有的科学判断，二者不可互相代办。


[a07conf]: /data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/07_features_overlap/07_04_common_rare_gradient_conflict_splitting_anchor.md:34
[a13parent]: /data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/13_mtp_task_property_decomposition/13_00_task_properties_to_standard_head_utility/13_00_task_properties_to_standard_head_utility_anchor.md:27
[schedule]: /data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_05_functional_coordinate_admission/subanchors/15_05_03_progressive_band_source_routing_anchor.md:26
[online]: /data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_06_online_spectral_routing_and_relay/15_06_online_spectral_routing_and_relay_anchor.md:40
[semparent]: /data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_13_semantic_supervision_middle_layer_formation/15_13_semantic_supervision_middle_layer_formation_anchor.md:6
[rankmany]: /data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_08_target_conditioned_layer_innovation/subanchors/15_08_03_function_admitted_update_representation_rank_anchor.md:20
[reuse]: /data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_17_three_model_sae_representation_trajectory/subanchors/15_17_01_sae_shared_direction_reuse_anchor.md:45
[n8anchor]: /data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_17_three_model_sae_representation_trajectory/subanchors/15_17_02_sae_n8_separability_anchor.md:1
[common]: /data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/01_common_operator_mechanism/01_01_common_operator_identifiability_anchor.md:1
[future]: /data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/11_informative_future_branch_mechanism/11_01_informative_horizon_supervision/11_01_informative_horizon_supervision_anchor.md:1
[relayanchor]: /data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/13_mtp_task_property_decomposition/13_00_task_properties_to_standard_head_utility/subanchors/13_00_05_task_relevant_relay_target_anchor.md:1
[speed]: /data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_01_spectral_learning_and_feedback_dynamics/15_01_spectral_learning_and_feedback_dynamics_anchor.md:1
[admission]: /data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_05_functional_coordinate_admission/15_05_functional_coordinate_admission_anchor.md:1
[load]: /data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/16_load_control_gradient_interference/16_00_switch_lb_gradient_conflict/16_00_switch_lb_gradient_conflict_anchor.md:6
[compat]: /data/250010109/Research_System/daily_research_reports/0925/docs/update_compatibility/anchor_cn.md:1
[relayresult]: /data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A13/13_00_task_properties_to_standard_head_utility/A13_00_05_E01_task_relevant_target/summary.md
[randomresult]: /data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_06_online_spectral_routing_and_relay/A15_06_E02_local_random_identity_control/summary.md
[hardresult]: /data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E08_m2d2_hard_semantic_route_ntp/summary.md
[learnedresult]: /data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E07_m2d2_learned_semantic_router_ntp/summary.md
[p3result]: /data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E14_P3_matched_training_semantic_comparison/summary.md
[n8result]: /data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_17_three_model_sae_representation_trajectory/A15_17_02_E01_n8_17b_separability_audit/summary.md
[n8focus]: /data/250010109/Research_System/daily_research_reports/0923/focus_sae_n8_separability.md
