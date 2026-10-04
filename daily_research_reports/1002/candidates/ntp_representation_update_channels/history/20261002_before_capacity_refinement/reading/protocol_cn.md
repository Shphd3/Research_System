> 历史阅读副本：仅将相对链接按原目录解析；正文科学内容未改。原始字节快照：[protocol_cn.md](../protocol_cn.md)。

# Protocol 候选：更新前表征能否预测自然文本的有限更新响应？

[English](/data/250010109/Research_System/daily_research_reports/1002/candidates/ntp_representation_update_channels/history/20261002_before_capacity_refinement/reading/protocol.md) · [Anchor](/data/250010109/Research_System/daily_research_reports/1002/candidates/ntp_representation_update_channels/history/20261002_before_capacity_refinement/reading/anchor_cn.md) · [数学推导](/data/250010109/Research_System/daily_research_reports/1002/candidates/ntp_representation_update_channels/mathematical_analysis_cn.md)。本文是未来确认的完整候选合同，不是对今日探索的事后预注册。今日过程与结果分别归 [过程记录](/data/250010109/Research_System/daily_research_reports/1002/candidates/ntp_representation_update_channels/research_process_cn.md) 和 [研究报告](/data/250010109/Research_System/daily_research_reports/1002/candidates/ntp_representation_update_channels/research_report_cn.md)。

## 0. Approval Snapshot

| 项目 | 当前内容 |
| --- | --- |
| Document status | `DRAFT_NOT_EXECUTABLE` |
| Approval / block audit | 新确认设计未确认；A、C、D、E、F 为 PROPOSED；B、G 为 BLOCKED |
| Cross-block consistency | 候选对象链一致；独立取样单位及新数据清单未定，不能晋级 |
| Execution scope approved | 用户已授权两小时研究及备选文档；已完成范围内本地分析。本文不授权新的远程、训练或确认 Full |
| Design frozen at | 未冻结；2026-10-02 候选；未来批准时记录正文及配置 hash |
| Purpose | 判断固定来源更新下，更新前表征是否提供词面基线以外的有限响应预测信息 |
| Primary Anchor | 本目录 Anchor §3–§6，AI_PROPOSAL，不是已批准科学设计 |
| Existing active Focus | [领域更新几何 Focus](/data/250010109/Research_System/Projects/from-attention-to-search/main/focus/focus_domain_update_geometry_cn.md)，只作上位背景，本轮不改它的问题或状态 |
| Prior / model / falsifier | 自然文本的续写误差与表征共同决定响应；核心量是实际有限损失变化；若冻结读出器没有可分辨增益，则该操作化未获支持 |
| Experiment role | operationalization or proxy test：验证响应信息能否被指定工具读出 |
| Minimal setup | 一个 S7 检查点；四个固定来源梯度；新拟合与新确认记录；两种步长；无 LM／SAE 训练 |
| Treatment / changed variable | 在相同词面基线中加入冻结 SAE 的 320 维系数 |
| Controls / held fixed | 原生输出的 320 维 PCA／随机投影；目标身份诊断；固定数据、更新、损失、拟合和评估规则 |
| Primary metric | 四个来源等权的相对平方误差改善 \(Q_{\rm macro}\)，无量纲 |
| Pass / fail / insufficient | 区间下界 > 0 / 上界 ≤ 0 / 跨零或资格不合格；科学效用门槛 Unknown |
| Cannot claim | SAE 独有信息、纯语义机制、目标前可知全部响应、长期训练负干扰、隔离净收益 |
| Approval decision | 待研究者审阅；不存在默认晋级或新的运行批准 |

2026-10-02续研补充：[同域A/B来源批次迁移](/data/250010109/Research_System/daily_research_reports/1002/candidates/ntp_representation_update_channels/source_transfer_addendum_cn.md)与[跨领域响应结构](/data/250010109/Research_System/daily_research_reports/1002/candidates/ntp_representation_update_channels/domain_response_structure_cn.md)均已完成旧面板探索。前者的平均／差异按同域来源批次定义；后者另查领域差异、较早前文预测及输入通道。两者均不修改本Protocol的主检验、阈值、审批或资源。把前缀相对收益改为主比较仍是待研究者选择的AI建议。

## 1. Terminology / Definitions

**来源更新**是从一组自然文本真实下一词梯度构造的一个矩阵方向。**读出事件**是另一条前文与它的真实下一词。**表征**指末块注意力输出 \(a\)，不是 SAE 重构。**响应** \(I\) 是原模型尾部在指定矩阵变化前后的真实下一词损失差，正值不利、负值有利，单位 nat。**读出器**是只读取更新前特征的 ridge 回归，不参与语言模型训练。**确认**只指未用于当前设计选择的新结果读出；旧 R 不能恢复为未曝光数据。

**固定来源条件推断**保持四个来源矩阵不变，只研究新读出记录上的效果。它不推断重新抽取来源文本后的平均效果。**独立单位**是用于区间估计的实际独立抽样群；它未必等于数据集的一行。

## 2. Anchor Alignment

本实验只改变 Anchor 的一个候选判断：固定更新下，指定更新前表征能否增加有限响应的可读出信息。其计算链为自然前文／目标 → 来源平均梯度 → 原生位移 → 实际损失差 → 新记录预测误差。完整数学模型由 Anchor 与数学分析持有。

主特征提议固定为 SAE320；这是工具的可读出性检验。普通表征对照若更好，应如实记录，不能改为事后选择最好模型作为主检验。SAE 主比较失败不推出整个原生表征没有信息。上述选择为 AI_PROPOSAL。

## 3. Tested Hypothesis

给定四个固定来源矩阵、当前 S7 和候选总体，加入更新前 SAE320 后，指定拟合过程在新记录上比强词面基线降低平方误差。主候选参数为 \(Q_{\rm macro}>0\)。这是条件预测关系，不是“非零就值得做 Router”的效用判断。

目标身份诊断检验竞争解释，但它不进入主假设的输入。只在标签已知后有效的诊断不能支持预测前路由。

## 4. Rival Explanations

| 竞争解释 | 区分条件 | 仍保留的限制 |
| --- | --- | --- |
| 表征增益只是局部词面组成 | 当前／前一 token、前16 token 词袋、位置和表征尺度进入共同基线 | 未覆盖全部前文的任意非线性函数 |
| SAE 是必须的或特别优越 | 同维 PCA 与随机投影，使用同样拟合规则 | 一个随机种子不代表全部基；比较为次要 |
| 看到了实际目标才可预测 | 单独加入真实下一词；与主输入严格区分 | 目标词 one-hot 也不是完整条件分布 |
| 拟合／选择泄漏造成增益 | 按独立群划分；仅拟合集合选择特征和正则；整体记录打乱标签负对照 | 来源与读出总体关系仍条件化 |
| 一阶代理失真 | 主标签直接计算有限 \(I\)，半步与一阶仅诊断 | 只检验一个局部尺度 |

## 5. Data Construction And Provenance

**VERIFIED_SOURCE：**当前可复用来源是 N8_v1 已选自然科学文本，固定 revision `6ae613ba744ee56f645aee9c577d04f7e3d48b30`；计算机、数学、物理、生物四域，每域两个子类。旧 2048 记录及所有旧结果已曝光。来源 root 是 `/data/250010109/MoE_Router/experiments/20260930_ntp_statistics_local_compatibility/`，旧清单在 `data/selected.jsonl` 与 `data/data_manifest.json`。

已核对的子类分别是：计算机 `cs.CL`／`cs.CV`，数学 `math.AG`／`math.NT`，物理 `physics.flu-dyn`／`physics.optics`，生物 `q-bio.GN`／`q-bio.NC`。候选总体限于这个科学文本来源，不代表全部自然语言。

**AI_PROPOSAL：**复用已冻结的四个旧 F-half0 来源矩阵，每域128记录、每记录16目标；新拟合集合每域128条，新确认集合每域256条；每域两个子类等量。每条用前256 token，在零起始位置14、30、…、254预测下一个 token，共16事件；短记录不拼接，重复和截断策略在取样前冻结。这个样本规模只是可审阅的预算候选，功效未被承诺。

新记录须排除所有已曝光记录、跨集合全文 hash 相同项及已登记近重复项。必须保存来源 revision、record ID、群 ID、全文 hash、token IDs hash、位置与目标。只使用原文已有目标，不合成标签，不按效果或领域典型性选确认数据。

**BLOCKED：**当前来源只有 record ID，没有可验证论文 ID。尚未选择能支撑独立群抽样的新清单，也未确认仅以 record 为单位所允许的外推范围。必须在取样前由研究者决定独立单位／总体；不能把同论文的不同片段默认当成独立论文。训练数据是否包含这些文本也未核实，禁止称其训练外泛化。

## 6. Learning Task And Permitted Supervision

读出器对每个事件输出四个来源对应的响应预测。主输入不含真实下一词、损失、梯度、来源／目标领域标签或更新后的表征。它包含：当前和前一 token 的 F 高频128词 one-hot；前16 token 的 F 高频512词袋；16个位置 one-hot；\(\log(1+\|c\|)\)、\(\log(1+\|a\|)\)。词表及缺省零向量只在新拟合集合确定。

SAE 分支加入冻结字典的320个 \(\log(1+\alpha_k)\) 系数。原子在新拟合集合按记录覆盖率排序，tie 按 ID，至少覆盖16个拟合记录；不足320则主条件不完整并停止，不用确认数据补选。响应标签来自原模型真实目标损失，仅用于训练读出器和最终计分。独立目标诊断额外使用 F 高频128目标词 one-hot，明确标记非事前可用。

## 7. Model / Architecture And Frozen Variants

固定 S7 33B 训练词元检查点：`/data/250010109/MoE_Router/experiments/20260920_s7_lambda0p1_from_scratch_4h100/runs/S7_lambda0p1_from_scratch_4h100/milestones/token_033000000000`。`state.pt` 的 SHA256 为 `c30b78e5bcba8f0a09c5e215389be86778874e87fcbb9fe5211175d370bb0803`。33B 是训练词元数，不是参数数。

固定 `blocks[7].attn.o.weight`，形状1024×2048；\(c\) 是2048维输入，\(a=Wc\) 是1024维原生输出，\(r\) 是前置残差。后续归一化、MLP、最终归一化与151936词表投影全部保持原模型计算。SAE 的30000列归一化 decoder、encoder、bias 和 TopK32 全部冻结；SAE 不进入任务损失。

PCA320 仅在新 F 的原生输出上拟合；random320 使用 seed31 的1024×320高斯矩阵 QR 正交化。PCA符号不影响线性读出，但保存实际基。所有主输入分支使用相同 F／确认记录。

## 8. Training Objective And Optimization

这里没有语言模型或 SAE 训练。只拟合四输出的 ridge：对 F 训练折的每列输入与每个响应做均值方差标准化，常数列尺度设1；最小化平均平方误差加 \(\lambda\|\beta\|_F^2\)，截距不惩罚。使用四折群级交叉验证，标准化与均值仅来自训练折。

AI_PROPOSAL 正则网格为 \(10^{-4},10^{-3},10^{-2},10^{-1},1,10,100\)。按四个标准化响应的平均验证误差选最小值；tie 选较大 \(\lambda\)。在全 F 重拟合一次后冻结。若最优值落在100上，确认解封前扩大范围并记修订；解封后禁止因此改网格。没有梯度优化器、训练 schedule 或模型 checkpoint 选择。未来若引入 LM 训练，本文不涵盖该改变，必须另按训练观测合同登记。

## 9. Conditions, Seeds, And Checkpoints

| 条件 | 作用／证据角色 | 固定项 | 所对照的竞争解释 |
| --- | --- | --- | --- |
| B：强词面基线 | 主分母 | §6输入 | 局部组成 |
| B+SAE320 | 唯一主处理 | 冻结原子规则 | SAE可读出的额外响应关系 |
| B+PCA320 / B+random320 | 次要工具对照 | 同维、相同拟合 | SAE独有性 |
| B+target / B+target+SAE | 事后组成诊断 | 真实目标仅在此开放 | 目标身份解释 |
| B+SAE，记录块打乱响应 | 负对照 | F内同类别、整记录打乱，seed1002 | 泄漏／不当计分 |
| 全步／半步 | 主尺度／局部性诊断 | 相同来源方向 | 曲率／符号数值不稳 |

只有一个检查点。主步长固定为 \(\eta=0.05731845587090156\)，来自旧 F pooled 来源更新在旧 F 的相对 RMS 输出位移0.001；半步为其一半。它不是优化器学习率建议。不能在确认集按好看的符号或预测增益挑步长。数据 hash 排序用 seed1002；bootstrap seed1002，2000次。上述为候选固定值，不是批准的最终配置。

## 10. Primary Metric And Frozen Analysis Plan

令确认集事件 \(j\) 在来源 \(A\) 下的真实响应为 \(I_{Aj}\)，两预测分别为 \(\widehat I^B\) 与 \(\widehat I^F\)。先算各来源相对误差改善，再对四来源等权：

\[
Q_A=1-\frac{\sum_j(I_{Aj}-\widehat I^F_{Aj})^2}
{\sum_j(I_{Aj}-\widehat I^B_{Aj})^2},\qquad
Q_{\rm macro}=\frac14\sum_AQ_A.
\]

每域同样记录数，每记录16个目标，因此事件均权也给予记录均权。单位无量纲，百分比报告为100Q。来源等权防止一个来源的大误差主导结论；pooled-SSE比值只作次要读数。此指标不是原模型 perplexity 增益。

在已确认独立群上配对、按子类分层重抽样，保持群内全部事件与两预测成对，生成双侧95% percentile区间。四个来源矩阵与冻结读出器均保持不变，区间不包含来源重抽样、拟合不确定性或设计选择不确定性。唯一主比较无需多重校正；来源分解、其他工具、半步及目标诊断均描述性，不据其单项显著性宣告主假设成立。

缺失事件、非有限值、来源失配、重复群或失败计算不得按结果删去：停止确认，修复并记录是否已经曝光；如有科学相关修订，当前确认材料降为探索，重新冻结新面板。若基线 SSE 为零，Q 未定义，裁决 INSUFFICIENT。禁止按确认离群值剪裁。解封点是第一次写出任何确认损失、预测误差或其汇总。

## 11. Secondary Metrics And Guards

报告各来源／读出域平均 \(I\)、事件有利／不利／未分辨比例；数值带提议为 \(\pm10^{-5}\) nat，同时展示 \(2\times10^{-6}\)、\(5\times10^{-5}\) 的敏感性。它们不替代主Q。

先验证：零变化完全一致；\(G=ec^\top\) 相对误差≤\(10^{-5}\)；全模型临时矩阵变化与尾部重放 CE 差≤\(2\times10^{-5}\) nat；稳定CPU梯度与原生参考相对误差≤0.002；全／半步报告 \(\sum|I-\eta h|/\sum|I|\)，不把线性近似强行当真。所有临时权重修改须在 finally 中恢复，模型状态 hash 前后相同。边界值只支持数值资格，不是科学通过阈值。

若做 SAE 方向图，保留原生位移、全30000坐标端点重构残差、TopK集合是否切换。固定正交子空间与正交补分别执行；只保留／移除／完整三臂都报告。子空间选择只能来自 F；任何新子空间选择与有限干预在确认前附入合同，否则仅作探索。

## 12. Known Good / Known Bad / Known Confusing Cases

已知正确例：线性 logits 的真实有限 CE 与直接矩阵重放一致，半步一阶误差按局部阶数缩小。已知错误例：把平均外积写成均值外积、用目标标签作为主输入、把非正交 atom 内积相加当独立能量。已知混淆例：领域平均帮助且近半事件不利；局部方向不利但完整更新有利；SAE 静态误差小而编码差动态误差大；校准分布下一阶均值零而方差非零。

这些例子验证测量与解释边界。它们不计入自然文本的经验支持票数。

## 13. Scientific Procedure And Stage Contracts

| 阶段 | 输入与操作 | 为什么做／输出 | 通过、失败、不足与交接 |
| --- | --- | --- | --- |
| S0 数据资格 | 经确认的总体、独立群规则、全排除清单；先做无模型抽样检查 | 排除重复和伪独立；输出数据清单、覆盖与碰撞表 | 群来源不明为 DATA_INDEPENDENCE_BLOCKED；不得进入确认 |
| S1 测量资格 | 精确检查点、缓存接口、少量 F 记录；执行 §11恒等式、零变化与临时更新检查 | 确认测到指定 W 更新；输出 qualification.json | 任一数值失败为 MEASUREMENT_FAILED；只许定位修复 |
| S2 F 拟合与冻结 | 固定四来源矩阵，新F原生输入与真实I；仅F完成特征和ridge选择 | 冻结“预测器如何产生”；输出特征、模型、CV与hash | 完整性通过后冻结；R不可见；网格边界先修订 |
| S3 新确认读出 | 冻结正文、代码、模型和确认清单；算实际I并按 §10计分 | 输出唯一主Q、区间、守卫与完整失败项 | 数值／数据失败为 INSUFFICIENT；其余按 §15；不改规则 |
| S4 记录与决定 | 全部条件和边界 | 写 Summary四项与 Detailed；向研究者呈现下一决定 | AI记录事实，科学状态与后续设计由研究者决定 |

## 14. Algorithm, Output, And Provenance Contract

顺序固定为：核验输入hash → 构造／核验来源矩阵 → 提取原生 \(c,a,r,e\) 与 SAE 系数 → 用 \(a-\eta M_Ac\) 计算原生尾部损失 → 仅F拟合 → 冻结 → 新确认评估 → 群级配对区间 → 完整性审计。任一步缺失不得伪造零值。

实现复用旧 `core.py` 的精确模型加载／尾部与当前 `finite_replay.py` 的有限读出；适配新独立群数据和强基线；拒绝旧合成标签、SAE替代前向及训练loss反传到本次NTP来源矩阵。当前执行侧代码在 `/data/250010109/MoE_Router/experiments/20261002_s7_representation_update_channels/scripts/`。未来运行须开新目录 `runs/confirmation_<registered_revision>/`，不能覆盖今日探索。

输出至少包括注册正文hash、配置与代码hash、环境版本、检查点来源、数据与群清单、排除原因、source matrices、qualification、特征冻结、CV、预测和逐事件损失、主指标与完整失败日志。原始数组与缓存留执行仓库；Research_System 只收文字、精选小表／图与payload manifest。

**资源 AI_PROPOSAL：**先在本地CPU8线程、峰值内存≤64GiB、单资格运行≤15分钟内完成检查；新确认总资源上限及执行环境尚未确认，G保持BLOCKED。不得由本候选自动提交GPU或远程作业。

## 15. Success / Failure / Insufficient Evidence

数值、数据与冻结守卫全部通过后：主Q区间下界>0为 SUPPORTS_THIS_READOUT；上界≤0为 DOES_NOT_SUPPORT_THIS_READOUT；跨零为 INSUFFICIENT_PRECISION。任何关键守卫失败为 INSUFFICIENT_VALIDITY。各标签只约束这个条件关系和工具，不裁决整个研究问题关闭。

“足够大，值得做下一步系统设计”的阈值与误判代价为研究者判断，当前 Unknown。若研究者采用非零效用门槛，须在确认解封前登记，并同步修改主决策分支；不得看完结果再加。

## 16. What This Cannot Claim

不能把词面残差称为纯语义；不能把预测器剩余误差称为不可约自然随机性；不能从静态SAE重构推动态忠实性；不能从方向敏感性或局部不利推出长期伤害；不能从固定来源推任意新来源；不能从记录不重复推论文独立或训练未见；不能从此结果决定分开参数或Router有净收益。

## 17. Block Confirmation, Freeze, And Amendment Ledger

| 块 | 状态 | 已写清的内容／未决项 |
| --- | --- | --- |
| A 问题与边界 | PROPOSED | 一个条件读出问题；非长期隔离收益 |
| B 数据与来源 | BLOCKED | 旧来源可复用；新独立群规则与清单未确认 |
| C 任务与监督 | PROPOSED | 事前输入；实际有限响应；目标诊断隔离 |
| D 架构 | PROPOSED | 精确S7及SAE冻结；SAE320主分支与原生对照 |
| E 目标与拟合 | PROPOSED | 无LM训练；群级CV ridge与冻结 |
| F 比较与裁决 | PROPOSED | macroQ、条件区间、三分支；效用门槛Unknown |
| G 执行与复现 | BLOCKED | 新确认环境／资源与运行批准未定 |

2026-10-02：研究者确认的是两小时研究、真实自然文本表征分析、S7／SAE工具及备选存放；本文其余选择是可审阅提案。AI完成对象一致性审计，不冒充A–G人类确认。数据独立性、最终资源与设计确认未满足，因此保持 `DRAFT_NOT_EXECUTABLE`。

未来晋级需要：A–G明确确认、跨块一致性PASS、冻结时间和hash；运行仍只按已批准的具体范围。开始后正文不可静默改写，所有物质性改变以附录记录时间、前后值、理由、已曝光情况、影响块、批准及证据资格。今日探索不会因未来批准变成预先确认。
