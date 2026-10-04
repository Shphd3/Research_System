# Conversation Memory: 0930-自然语言统计规律与相容性

Conversation name: 0930-自然语言统计规律与相容性
Processed by: Codex (harness: Codex desktop; model: unknown)
Created at: 2026-10-02T08:35:31Z
Latest update at: 2026-10-02T08:41:24Z
Continues from: none
Environment: repo=/data/250010109/Research_System; project=/data/250010109/Research_System/Projects/from-attention-to-search; exec=/data/250010109/MoE_Router. 三个根目录当前均可读。

本记录仅保存该对话的工作上下文；科学设计、事实结果、授权和研究者判断由 References 中的拥有者记录持有。对话名称由研究者明确提供；首次创建本名称的记录，不复用其他对话的 memory.md。

## 2026-10-02T08:35:31Z -- 完成局部结构实验后的认识重锚定与共享研究方向

- Summary:
  - **目的与位置。**上位问题是哪些数据适合共享参数、哪些值得分开，并尽量避免把人工领域标签当成答案。当前只研究固定模型状态的局部更新候选。此前指定的更新前表征预测没有达到注册改善；领域均值描述器没有取得留出收益，但这不证明表征没有信息或全部领域结构不存在。本轮先测局部结构是否复现，再用已有 SAE 作领域和方向分析工具。用户要求按 reasoning skill 解释目的、模型、三个实验步骤和结果，并反复要求精炼、直白地讲清逻辑。
  - **数学机制已经明确。**固定 S7 累计训练 33B token 的检查点；33B 是历史训练词元数，不是参数量。观察末块注意力输出矩阵 W（1024×2048）。c 是矩阵输入，a=Wc 是原生输出，J 是 a 到下游 logits 的 Jacobian，p 是当前模型概率，y 是真实下一词。交叉熵给出 e=Jᵀ(p−u_y)、G=e cᵀ；两个事件的 K 是 G 的内积，精确分解为输入内积乘输出侧梯度内积。仅 W 做足够小的普通 SGD 更新时，另一事件损失变化一阶近似为 −ηK；该近似不是实际有限步、Adam 或长期共享结论。同一文本换模型状态，c、p、J 和更新关系均可能变化。
  - **自然语言先验的边界。**Zipf 型词频只描述边际目标权重，各向异性只说明指定空间方向分布不均匀，均不能推出有符号帮助／冲突。结构化真实条件续写分布 q_x 与当前模型偏差可能产生可复现平均需求，但本轮没有直接识别 q_x 或证明系统性误差。p=q_x 时固定上下文的自然目标平均梯度为零，模型 Fisher 仍可非零；固定某个真实目标后的均值仍可非零。不能把目标条件均值当成已测校准误差。
  - **必须分开的两个分支。**主 H1 检验真实目标匹配、子领域均衡后的领域平均梯度差是否跨 F/R 记录池复现，并超过历史梯度平方参考的候选 1% 尺度。功能 H2／工具 H3 独立描述模型 Fisher 的领域模式和 SAE 工具能展示什么，没有确认性功能阈值，不救回 H1，也不要求 SAE 赢过对照。“真实目标相同”是下一词 token ID 相同，不要求模型预测相同；它主要控制梯度比较，不能把它与 SAE 敏感性读出合并成一个检验。
  - **SAE 与敏感性的具体角色。**已有 SAE 编码 a，不编码 c；冻结 decoder atom 提供原生输出方向，实际稀疏系数说明是否出现。模型 Fisher 衡量沿方向微小移动会使预测分布改变多少，无须假设 p=q_x。方向敏感性是“容易受影响”，不说明移动会令真实答案更正确还是更错误；激活、敏感性、实际更新经过该方向和有符号损失作用是不同对象。真实目标不直接进入模型 Fisher，但目标身份与上下文相关，所以目标条件取样能改变平均敏感性。真实目标经验梯度二阶矩不能直接替代模型 Fisher；非正交 atom 的敏感性不能相加为独立容量。
  - **已执行的三个实验环节。**①冻结模型／字典／两池数据，核对重复、覆盖、合成校准及严格数值 Smoke，建立测量资格；②四领域、四实际目标构成 192 个不共享文档端点的四元组，用独立跨池梯度差内积估计 T，避免把同池均值估计噪声直接平方成信号，另保留有符号跨作用；③在自然、共同支持及等目标总体上做混合诊断，用 F-only 冻结的 SAE 集合／PCA／随机方向分析出现、Fisher 敏感性和经验协方差，R 不用于选有利方向。总体 2048 记录、每条 16 个位置、32768 个事件；功能分支 4096 上下文、每个 8 探针。模型及 SAE 均为 0 更新。
  - **执行完成与资格。**正式 Smoke 与 Full 已完成，Full 为 pt-z162gb1w，执行根 runs/full_initial；无需重提该任务。前两轮 Smoke 因词表投影 FP32 反传求和／抵消误差失败，临时诊断轮为 DEBUG_ONLY；保持原生前向不变、修复 FP64 反传累加并恢复原门槛后，严格 Smoke 才通过。次级编号映射输出修复保留原件且未改主值。来源重复筛查通过，但历史语料曝光、缺论文身份及文档独立近似限制证据，不能称全新语料确认。具体故障谱系和收据见 Detailed。
  - **主结果仍为不足。**T=0.006637，标准误 0.005170，95% 区间 [−0.003738,0.017012] 同时包含零和 0.01 门槛，程序裁决 INSUFFICIENT。当前测量不能区分稳定差异很弱与差异超过候选尺度；不是程序失败，也不是证明没有结构。T 不是预测改善率。研究者科学判断仍为 Unknown。
  - **“共同模式／领域偏离”的认识更新。**敏感性 profile 的同领域跨池原始 cosine 约 0.9973，不同领域也约 0.9952，说明共同模式很强。扣除各池四领域共有均值后，同领域平均 cosine 约 0.5012，出现部分领域偏离对应；不同领域的中心化负 cosine 不表示梯度冲突。自然上下文组成、目标组成、来源、抽样和探针不确定性仍是竞争解释；目标匹配功能单元存在不足覆盖。R rank32 的共同 SAE span Fisher trace 读数高于本次 PCA／随机点读数，但没有优越性显著检验，也不是容量占用或独有机制证据。自然混合群体内积点估计均正，没有合格的总体符号区间。
  - **用直白语言解释组成因素。**假设某个方向对括号附近预测敏感，而某领域片段括号较多，它的平均敏感性就更高；另一批同领域文本仍有相似组成，差别也会重复。这个例子是说明性假设，不是原子功能的测量结果。“在另一批文本中重复”支持描述性复现，却不能独自区分领域学习需求与重复的词面／句式组成。组成本来也是自然学习任务的一部分，应并列保留整体关系及匹配条件关系，不能自动删除前者。
  - **已完成词面探索。**lexical_readout_01 在现有缓存上用 CPU 检查 F 预选的 320 个共同／富集 atom，分别看当前 token、前一 token、前文 16 token、窗口内完整英文词和真实下一词。F 选择词面映射后冻结，R 报命中率、覆盖率、基础频率、lift、文档覆盖及域内关系。原子 28737 对当前 ` (` 的 R 命中率约 66.23%、覆盖率约 82.59%；21737 与真实下一词 ` to` 有关联，真实下一词并非前向输入。保留两类反例；本子集五模式均无映射达到所登记的高命中率且高 lift 初筛标签。这是运行后探索，不是全部 30000 原子的审计，不证明一词一原子、唯一语义或因果功能，也不排除未覆盖词／低频原子。
  - **共享问题的关键桥。**应研究“A 的学习改变共享参数 → B 的内部表示实际移动 → B 的预测改变 → B 的实际损失变化”。SAE／Fisher 帮助解释方向，但敏感性并不提供真实损失变化符号。当前自然文本冻结实验未运行实际有限 W 更新或长期共同／分开训练。此前受控构造任务已出现局部不利项被更大帮助抵消、B 总损失仍下降；不同状态／损失／数据设置不可直接合并，仍说明局部不利不等于净伤害或分开收益。
  - **最新对话建议（AI_PROPOSAL，pending canonicalization）。**为了推进共享问题，AI 提议并列澄清词面／目标组成，优先补小规模真实自然语言交叉更新：同一检查点出发只让 A 更新指定共享块，独立验证 A 改善，检查独立 B 损失并另测 B→A；用 SAE 查看实际位移与作用，不只看静态敏感性。更后续在参数、数据曝光、计算和初始化可比较的设置下直接比较共同与分开多步训练，判断隔离收益及损失有益共享的代价。一次净帮助或净伤害都不是长期分开收益的充分或必要门槛。“需要分开”仍是待验证结论。
  - **权限及判断不变。**上述新建议尚未经研究者选择、未写入新的 Anchor／Protocol、未获新运行授权，不取代当前 Focus 的下一决定，也不改写 Summary 中“先决定是否提高 H1 精度”的已有建议。本次仅写对话 memory，没有科学状态提升、训练、远程提交、commit 或 push。

- Current work: 已完成 reasoning skill 的解释与推理审计，明确均值需求、模型敏感性、词面关联、实际更新和隔离收益的边界；本次将全部重要更新保存为本对话的首条工作记录。数学／实验／结果的权威仍在下方拥有者文件，研究者科学判断及下一路线选择 Unknown。研究文档在 2026-10-02 迁移到 Projects/from-attention-to-search/main；旧 daily_research_reports/0930/docs 路径不再是当前拥有者位置。本次逐一确认必要新路径可读。入口检查报告 20 个 UNTRACKED 项，不能声称全库导航检查通过；它是当前迁移／Git 跟踪问题，不是本轮科学结果失效，本次不处理他人重组修改。
- Next action: 等研究者选择接下来要减少的具体不确定性。对话当前 AI 优先候选是上述有界交叉更新；若被明确选择，先读现行 Focus／Anchor／Protocol 和已有自然文本干预证据，检查是否复用，再通过相应拥有者落实精确比较、测量精度和资源契约。原 H1 扩样、组成匹配、有限更新与长期隔离各自回答不同问题，不自动串成强制资格门，不依本 memory 直接运行或重提已完成 Full。
- References:
  - [当前 Focus](/data/250010109/Research_System/Projects/from-attention-to-search/main/focus/focus_domain_update_geometry_cn.md)：稳定问题、研究者判断与既有唯一下一决定，未被本对话建议替换。
  - [本轮 Anchor](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/shared_updates/ntp_statistics_local_compatibility/anchor_cn.md)：当前设计、数学对象、独立均值与功能分支；其中 NOT RUN 正文是保留的登记快照，实际执行看顶部更新及结果拥有者。
  - [本轮 Protocol](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/shared_updates/ntp_statistics_local_compatibility/20260930/protocol_cn.md)：真实目标／四元组、精度门、执行授权与追加工程／词面修订。
  - [本轮 Summary](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/shared_updates/ntp_statistics_local_compatibility/20260930/summary_cn.md)：完整目的、假设、分析、结果及边界；[主结果 JSON](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/shared_updates/ntp_statistics_local_compatibility/20260930/evidence/primary.json)核对不足裁决与区间。
  - [本轮 Detailed](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/shared_updates/ntp_statistics_local_compatibility/20260930/detailed_cn.md)：完整执行谱系、偏差、数值修复及词面补充；[完成回执](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/shared_updates/ntp_statistics_local_compatibility/20260930/evidence/completion_receipt.json)核对 0 更新和采集完整性；[词面回执](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/shared_updates/ntp_statistics_local_compatibility/20260930/evidence/lexical_readout_receipt.json)核对 CPU 探索范围。
  - [前序表征预测 Summary](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/shared_updates/natural_ntp_representation_compatibility/20260930/summary_cn.md)：指定预测比较的不支持及其边界，不是普遍无信息证明。
  - [受控交叉更新 Summary](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/shared_updates/shared_update_conditional_interference/20260927_controlled/summary_cn.md)：此前构造任务的实际净损失作用；[阶段报告](/data/250010109/Research_System/Projects/from-attention-to-search/main/stories/shared_updates/01_shared_update_stage_report_cn.md)用于理解不利局部项与更大帮助的区别，报告是派生读物。
  - [路径迁移清单](/data/250010109/Research_System/docs/research_locations.json)：本次核对后的旧路径到当前拥有者位置映射；后续恢复仍须刷新当前路径。

## 2026-10-02T08:41:24Z -- 大问题／六个小问题整理与新对话续接

- Summary: 研究者要求重新梳理大问题、小问题及答案，并生成新对话总结和 prompt。已将“何时共享、何时分开有净收益”的大问题解释性分成六项：平均更新差异稳定性、SAE 敏感性结构、词面／组成解释、更新前预测、实际交叉更新后果、长期共同／分开收益。这是已有工作导航，不创建六个 Focus，也不自动确定新优先级。主均值仍 INSUFFICIENT，功能／词面是描述性线索，指定事前预测不支持注册改善，当前冻结自然文本轮未测有限更新或长期隔离收益。
- Current work: 已生成 [continuation.md](/data/250010109/Research_System/.research/memory/conversations/0930-自然语言统计规律与相容性/continuation.md) 和 [new_conversation_prompt.md](/data/250010109/Research_System/.research/memory/conversations/0930-自然语言统计规律与相容性/new_conversation_prompt.md)。补查旧自然文本一步干预：21B 原子方向机制在本面板主要见平均帮助及收益选择性；更早结构更新使用另一参数位置，也主要见平均帮助。新对话不得把实际自然交叉更新泛称完全没做，应核对状态／矩阵／目标与复用差异。该补查不改变旧冻结科学结果，也不能移植为当前 33B 轮结果。研究者判断与下一决定仍 Unknown，新增交叉更新仍仅 AI 建议。
- Next action: 新对话先读 continuation 的必要拥有者来源，用 reasoning skill 核对六项答案，比较提高主检验精度、澄清组成、有限交叉更新三候选，再给一项最小区分性方案讨论稿供研究者选择。该 prompt 只请求读证据与设计讨论，不授权新训练、远程运行、重提完成作业或研究状态转换。新对话保存自己的 memory 并以 Continues from 链接本记录。
- References: [续接总结](/data/250010109/Research_System/.research/memory/conversations/0930-自然语言统计规律与相容性/continuation.md)提供准确读清单和范围；[开启 prompt](/data/250010109/Research_System/.research/memory/conversations/0930-自然语言统计规律与相容性/new_conversation_prompt.md)提供可粘贴指令；[旧自然文本原子机制 Summary](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/shared_updates/atom_mechanism/20260926/summary_cn.md)及 [旧结构更新 Summary](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/shared_updates/structure_update/20260926/summary_cn.md)拥有本次补查的历史有限步事实；前一条记录的 Focus／Anchor／Protocol／Summary 指针继续有效。

