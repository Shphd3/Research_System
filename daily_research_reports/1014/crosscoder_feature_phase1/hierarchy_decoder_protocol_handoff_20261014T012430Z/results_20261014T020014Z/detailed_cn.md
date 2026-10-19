# 完整报告：统计图层级与跨层解码幅度分布（图表修订版）

本报告是原运行 `20261014T020014Z` 的图表与解释修订，不是第二次正式实验。处理者：Codex，线程 `01a1343f-32aa-7500-9835-000956218089`。原任务 `pt-icv8hyi3`。**原全体趋势、频率比较、节点选择和文本均保持不变；新峰值类别统计标记为事后描述。**

Anchor：[研究者给定问题](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/hierarchy_decoder_distribution_anchor_user_20261014_cn.md)。冻结 Protocol：[原执行契约](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/provenance/protocol_frozen.md)，SHA256 `39530a9a36eee0403a8bc3ee53ad19d3e82a5dcb18c86fa7287c1ca4cc8894fb`。[简短报告](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/summary_cn.md)；[本次修订范围](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/provenance/visual_revision_scope_cn.md)。

执行结果可用于冻结定义下的描述性比较；不能升级为机制或效用证明。研究者的机制判断、科学状态转移与后续实验决策仍为 Unknown。本次修订没有改变 Focus、Anchor 或原冻结 Protocol。

## 目的

本轮要判断统计图层级 h 是否可以直接作为模型深度的正向排序。这关系到未来如何选择学习对象，但目前不直接测共享／分离学习的收益。原待检验预期是较高 h 对应更偏深层的解码分布；竞争解释是建边规则使 h 与激活频率耦合，且不同模型层的尺度改变幅度比较。

若两种坐标均支持正向，且完整 p 与频率内比较一致，才可能保留这种描述性排序；若方向不支持或高度依赖尺度，必须缩窄代理含义；覆盖不足的频率格保持不足。以上不把相关升级为因果或训练效用。

## 方法

### 实际对象与术语

研究问题是统计图层级与跨层解码幅度分布是否对应。本轮减少的是“图层级能否作为模型深度代理”的不确定性，不是判断何种专家结构更有训练收益。

最终checkpoint为 `/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/runs/formal_14layer_batchtopk_a22/checkpoint_000999997440.pt`，累计999,997,440训练位置。Base `/data/share/Qwen3-0.6B-Base` 冻结，revision da87bfb608c14b7cf20ba1ce41287e8de496c0cd。14个激活空间为零基block1,3,…,27，即一基2,4,…,28的residual-post（最终全局norm之前），每个向量维1024；字典16,384。不是0.5B权重，也不是另一28层字典任务。

沿用已有TRAIN均值／向量RMS、原严格分数门控阈值0.051281172782182693。训练BatchTopK不是逐位置恰好Top256。模型和coder均未重新加载；本轮没有模型前向、训练、激活生成或全量共现计数。

数据为原10,485,760合格位置、10,249完整／尾上下文；按128上下文成块共81块，种子20261014。D=5,238,097，V=5,247,663。原bin同一份，原文档ID未保留、近重复独立性未知。



| 固定术语 | 对象、计算与单位 | 不能当作什么 |
|---|---|---|
| 统计图层级 h | 在完整约简统计图中，到无出边节点的最长出边路径；叶节点为 0；无量纲 | 模型层号、语义复杂度或因果先后 |
| 模型层号 | Qwen3 实际 block 的一基编号：2、4、…、28 | 图中节点的纵向位置 |
| 激活频率 | 某侧有效位置中该 Feature 命中的比例；图节点明确写“V 激活频率：×%” | 解码占比 p |
| 跨层解码幅度占比 p | 同一 Feature 的 14 层 decoder 向量 L2 范数分别除以其总和；图中单位 %，每 Feature 合计 100% | 激活概率、重构能量或功能贡献 |
| 幅度加权平均层号 L | 用 p 对实际模型层号求加权平均；单位为模型层号 | 整条 p 分布后移或前移的证明 |


固定最终 14 个选定模型层、16,384 个 Feature 的 CrossCoder，复用冻结 TRAIN 归一化和原推理规则产生的已有统计图与 decoder 几何。主集合是 D/V 支持均 ≥200、且 V 图非孤立的同一批 **15,537 个 Feature**。各统计图层级 h 的样本数依次为 **20、8,896、5,347、1,209、63、2**。每个 Feature 等权；图中四分位范围描述节点差异，不是置信区间。

三类图回答不同问题：图1看固定节点的统计关联；图2及图4—7看跨层解码幅度占比 p；图3看全部合格 Feature 的 h—L 关系。图8是频率解释边界。TRAIN 归一化坐标与恢复原始坐标使用同一批节点；恢复原始坐标是将各层范数乘回保存的 TRAIN 向量 RMS，再计算 p 和 L。

本次按用户要求重画已有结果，并从保存的 p **新增一次事后峰值比例描述**：逐 Feature 取 14 层最大 p，分为“第 2 层最大”“第 28 层最大”“其他层最大”。两种坐标均无精确并列最大值。类别只描述幅度峰值，不命名功能。没有重跑推理、训练、缓存扫描、关系计数或频率比较，也没有新 GPU 任务。


### p 和 L 的具体含义

一个 Feature 在一个位置只有一个联合非负激活值 z。该 Feature 在某模型层的解码向量是 z 乘该层 decoder 向量，幅度是 z 乘 decoder L2 范数。p 将同一 Feature 的 14 层幅度按总和归一；共同 z 约消，所以 p 和 L 是固定 decoder 的几何描述，不随展示文本改变。

对模型层号 ℓ∈{2,4,…,28}，记该层的 decoder 范数为 dℓ，则 pℓ=dℓ/Σdℓ，L=Σℓ·pℓ。恢复原始坐标时先以保存的该层 TRAIN 向量 RMS 乘 dℓ，再重复同样计算。p 无量纲，图中乘 100 显示百分比；L 的单位是实际模型层号。p 总和为 1；16,384 个 Feature 都没有零总范数或非有限几何，主集合 15,537 个全部有效。

L 只表示幅度加权平均层号。浅层与深层可同时有峰；L 增减不推出整个分布平移。不同 Feature 的解码向量可能抵消，因此幅度相加不是重构能量，更不是独立功能贡献。

### 图、集合与比较规则

边 A→u 要求两端支持 ≥200、共同支持 ≥20、P(u|A)≥0.8、P(A|u)≤0.5、n_u≥2n_A。在 D 发现，在 V 只复核这些原始边，然后分别约简。箭头标签固定为“A→更常见的 u”。h 在完整约简图上计算；显示子图不会另改 h。沿路径频率至少翻倍是构造约束，不是机制发现。

D/V约简边分别149,945／146,947。V全字典h直方图为867、8,896、5,347、1,209、63、2；其中847个是孤立节点，h=0的另20个为非孤立合格叶节点。主集合Q=两侧支持≥200且V非孤立，为15,537个；仅支持合格集合恰好与Q相同，引用同一结果，不算独立稳健性证据。

D全字典h直方图835、8,563、5,544、1,356、82、4；同一Q上为20、8,561、5,537、1,336、80、3。D孤立815，D/V本侧零支持353／393，1—199支持462／424；这些资格和孤立性是交叉标签，不混加。[完整节点及资格](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/tables/hierarchy_members.csv)；[分类计数](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/tables/hierarchy_counts.csv)。

最高V层级5仅937、3461。按h和ID选锚点，再完整沿出边展开，分别19节点45边、22节点56边，并集30节点101边；节点选择在新p/L读取前冻结，不按解码结果或文本内容筛选。



频率规则保持原样：Q 上以 D 侧 log10 激活频率固定 5 个分位组，在每组内比较相邻 h 的实际频率共同范围；双方有效节点各 ≥20 才可比较。共同范围只有一个值时同样适用各 ≥20 的规则。本轮无合格单值格。频率比较使用 TRAIN 归一化坐标；本次没有追加恢复原始坐标的频率版本。

原全体结果与 D/raw 参照直接复用。新图3共享节点、横向抖动、横纵轴范围及绘图规则。新组平均热图直接取旧表中各 Feature 等权平均的 p，未按激活频率加权。新峰值比例从已存 p 取唯一最大层后分类计数，不做检验；小于 3% 的柱段仍保留，精确值在源表。h=0 热图包括全部 20 个合格非孤立叶节点；h=5 为两个个体曲线。

## 现象

整体描述性 Spearman 在 TRAIN 归一化坐标为 **−0.277976**，恢复原始坐标为 **−0.157788**；方向保留，数值差异明显。TRAIN 归一化坐标下，h=1、2、3 的 L 中位数为 **19.902、15.007、14.305**，h=4 回升至 16.226；不是逐级严格单调。

完整 6×14 组平均 p 显示，TRAIN 归一化坐标下 h=1、2、3 的第 2 层平均 p 为 **15.39%、25.06%、30.20%**，第 28 层平均 p 为 **17.00%、13.95%、13.25%**。浅层和深层可以同时有幅度，不能把 L 的变化说成整条分布平移。两种坐标的完整热图使用相同 0–40% 色标。

事后峰值比例中，TRAIN 归一化坐标下 h=1、2、3 的“第 2 层最大”分别占 **34.95%、60.58%、74.19%**；恢复原始坐标下，这一类别均为 0，但第 2 层的 p 并非为 0。h=0 的 20 个节点在两种坐标下都以第 28 层为最大分量，完整轮廓仍不同。h=5 仅 937、3461 两点，其 TRAIN 归一化坐标 L 分别为 **22.118、14.899**。


![TRAIN归一化坐标6×14组平均p](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/figures/figure4_mean_p_train.png)

![恢复原始坐标6×14组平均p](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/figures/figure4_mean_p_raw.png)

读图：行是统计图层级 h 与该组 Feature 数，列是实际模型层号；每格为组内等权平均 p 的百分比，每行合计 100%。两图共用 0–40% 色标；少数单元超过 40% 时以色标上限显示，格内数字保留实值。均值保留双端幅度，但不能说明组内每个节点都相同。[原完整均值源表（含D参照）](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/tables/hierarchy_mean_p.csv)；[两坐标168格展示源表](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/tables/group_mean_p_source.csv)。

| 统计图层级 h | n | TRAIN 归一化坐标 L 中位数 | 恢复原始坐标 L 中位数 |
|---|---:|---:|---:|
| 0 | 20 | 22.717 | 24.015 |
| 1 | 8,896 | 19.902 | 22.359 |
| 2 | 5,347 | 15.007 | 21.099 |
| 3 | 1,209 | 14.305 | 21.025 |
| 4 | 63 | 16.226 | 21.905 |
| 5 | 2 | 18.509 | 22.778 |

这不是逐级严格单调，也不是同一个 Feature 的变化轨迹。源表含每组四分位数以及 D 参照；h=5 正文与图均保留两个个体，不用两点概括总体。

## 解释

为什么整体负相关，频率内却有 7 格为正？两者比较的对象与权重不同。整体相关包含不同 h 组之间的频率构成差异，使用全部 15,537 个节点的秩；频率格只比较固定频率组的共同范围内、某一对相邻 h 的 L 中位数。建边规则要求箭头指向至少常见两倍的节点，所以 h 与激活频率本来就耦合。不同频率构成可能与整体负向同时出现，但本轮没有识别它造成了多少差异。

必须看全部 **25 格**：11 格可比较，7 正、4 负；其余 10 格缺组、1 格无共同范围、3 格样本不足。可比较格的差值大小并不对称，例如 +0.170 与 −8.982 都各被算作“一格”。h=0↔1 和 h=4↔5 都没有合格格，不能用 11 格替代整体。五分位和范围交集也不保证组内频率分布相同。这不是“控制频率后的效应”。

![全部25格频率共同范围内比较](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/figures/figure8_frequency_all25.png)

读图：横轴为相邻统计图层级 h 对，纵轴为预定的 5 个 D 激活频率组。颜色是高 h 减低 h 的 L 中位差，单位为模型层号；每格标低 h／高 h 的样本数。灰格保留原因，不表示差值为 0。缺组／无共同范围格另标交集前组内人数。[完整频率源表](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/tables/frequency_comparison_25cells_source.csv)。

坐标尺度是另一条边界：恢复原始坐标后，整体负向仍在，但相关数值和峰值类别明显改变。这说明数值依赖层尺度；它没有删除 Feature，也不能被讲成功能差异。峰值类别相同也不代表完整 p 相同。

D 图参照的描述性 Spearman 为 **−0.279321**，D 频率检查也有 11 个合格格、7 正 4 负。D/V 来自同 bin，V 曾参与资格筛选和原始边复核，文档独立性未知；这些不是独立总体检验。节点也不独立，不报告 p 值或独立节点置信区间。h=5 只有两个节点，不能代表最高统计图层级的总体规律。


另外，原第 28 层工具 FVE 86.4722%、固定替换 CE +0.305962 nats 是既有评估，本轮没有重测。解码几何无法直接说明语义复杂度、模型层功能、层间因果组合，亦不能证明训练或专家分发收益。

## 结论

### 认识一：统计图层级 h 不能直接承担模型深度的正向排序，需要另外测跨层分布

![相同15537节点两种坐标的h—L对照](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/figures/figure3_all_features.png)

关键数据：两面板使用完全相同的 **15,537 个 Feature、横向抖动、坐标范围和绘图规则**，分别给出中位数、四分位范围、各组 n 与描述性 Spearman；h=5 单列两个点。相关分别为 −0.277976、−0.157788。[逐点双坐标源表](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/tables/figure3_coordinate_comparison_source.csv)；[中位数与四分位源表](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/tables/depth_vs_layer_summary.csv)。

推断的变化：保留 h 作为统计关联结构的描述，不再直接用“h 更高”代替“模型中更深”。**下一项研究决策（待研究者讨论）：选取学习对象时，是否要求明确所用坐标，并同时保留完整 p，而不是只按 h 排序？** 本报告不因此启动新的学习实验。

### 认识二：同级内部存在不同轮廓，后续应同时看具体节点、关联分支和跨层分布

![同级内部峰值类别比例，事后描述](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/figures/figure5_peak_composition_posthoc.png)

关键数据：TRAIN 归一化坐标 h=1 有 3,109 个“第 2 层最大”、4,493 个“第 28 层最大”、1,294 个“其他层最大”，都在同一个 h 内。h=5 的 937 与 3461 也具有不同 p 轮廓。恢复原始坐标改变峰值排序，因此不把类别命名成功能。[完整峰值比例与计数（事后描述）](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/tables/peak_composition_posthoc.csv)。

![最高统计图层级的两个个体轮廓](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/figures/figure7_h5_individual_curves.png)

图7保留两个节点各自的 14 层 p 与 L；n=2，不作最高级总体推断。[两个节点逐层源表](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/tables/h5_curves_source.csv)。全部 20 个 h=0 节点的逐个热图、固定 30 节点热图，以及原关联分支见 [完整图与读图说明](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/figures_cn.md)。

推断的变化：组平均和 L 能概括差异，但不能替代个体轮廓。不同 h 组含不同 Feature，本轮没有观察“同一个 Feature 随 h 增长而移动”。**下一项研究决策（待研究者讨论）：比较候选学习对象时，是否将具体节点、关联分支和 p 作为共同保留的信息，而不是仅使用层级或峰值类别？** 当前不能据此判断 common／unique、共享／分离学习或专家收益。


认识变化是：原先待检验“较高 h 也许对应更深解码分布”；现在全体 L 的方向不支持正向排序，完整 p 显示同级差异和尺度依赖；保留 h 对统计关联的描述，缩窄 h 作为模型深度代理的说法。频率构成能解释多少、具体分支为何形成、何种对象值得共同学习仍未回答。AI 建议下一次只先讨论上述信息应如何共同保留；不自动启动计算。

## 附录 A：全部图与文本的可追溯性

![全部20个合格h=0节点的两坐标p](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/figures/figure6_h0_individual.png)

图6两面板共用 0–50% 色标；每行是一个 Feature，百分比在全部 14 层合计 100%。20 个节点都以第 28 层为最大分量，但各层幅度比例不同，不能将相同峰值类别当成相同完整轮廓。源表 [20节点×14层×2坐标](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/tables/h0_individual_source.csv)。这不是新增文本选择，新增展示的 h=0 节点不自动有新的文本例子。

[图索引](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/figures_cn.md)完整保留两个原关联子图及密集边分面、同 30 节点 p 热图；不能用 30 个局部节点代替全体比较。

30节点各5个随机、3个最高z，合计240个Feature—位置记录，随机150、高激活90，没有两类重合导致的减少。共226个上下文，跨Feature可共享位置／上下文；这不是226个独立文档样本。

全部640块共16,098,567,532 bytes读取并核对SHA256；筛出V活跃位置后，各节点数量均等于已保存n_V。流式抽样按全局位置升序、每Feature固定PCG64种子合并；worker完成顺序不参与抽样。高激活同z按位置升序。抽样没有依据文本好看程度重选。

随机样本是V侧该Feature全部活跃位置中的等概率5条。分块合并时先按全体旧＋新位置等概率决定来自旧／新批的数量，再从旧的均匀reservoir抽对应子集，因此保留均匀不放回性质。它不是按块等权抽5条，也不是旧A-only/both类别样本。

[全部随机／高激活文本](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/text_examples_cn.md)保留完整模型可见前文（包含目标token）、目标token和位置、右文阅读辅助、z与h。[机器可读文本](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/text_examples.jsonl)和[逐位置14层幅度](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/tables/text_layer_amplitude.csv)可核对。同一位置的14层a=z×norm，不是换目标token拼出来的响应。

仅作有界可读性观察：937展示的随机5条和高激活3条目标都为t或空格+t；3461高激活3条目标均为Edit，随机5条含编辑标记闭合和article(s)等。这提醒最高统计层级也可能与词片或格式有关，不能自动叫“更复杂主题”。没有从这些例子认证单义语义、进行人工语义标注或把它们纳入趋势筛选。

交付核对逐条重新连接原索引与bin，240个目标token ID／offset一致，14层a与z×范数一致。完整前文留档；本轮只对展示目标及必要前文做辅助阅读，不声称完成人工语义验证。



本次没有重扫缓存、重抽文本或新语义标注。原 240 记录全部保留。

## 附录 B：原正式执行符合性、历史与成本

| 条款 | 实际 | 对证据的影响 |
|---|---|---|
| 最终14层F16384，完整冻结TRAIN规则 | 复用绑定缓存与几何；没有权重加载或前向 | 符合 |
| 主V图、同一15,537集合、D/raw固定参照 | 全部完成，源表保留 | 符合 |
| L只描述平均位置，同时看p形状 | 完整p、热图及18行14层平均p表 | 用户澄清已执行 |
| 单一共同频率值双方各≥20可比较 | 代码允许FIXED_FREQUENCY_LOCAL；本轮无合格单值格 | 不因频率无变化自动拒绝 |
| 三类图独立，选择不依赖L | 两锚点子图、同30节点热图、全体散点 | 符合 |
| 640块扫描、30节点文本 | 全hash匹配、240条、n_V匹配 | 符合，没有缩水 |
| 资源从CPU草案改为4卡H100 Reserved | 用户明确澄清授权，冻结后提交一个任务 | 无科学定义变化；未新增第二个任务 |
| 图1标签密集 | 仅三行标签及同边局部分面；保留初始render源码和修订hash | 工程排版，无统计重跑 |
| 交付验证脚本初次低效 | 停止反复载入NPZ成员的验证，改为一次载入；重新完成表格核对 | 已记成本；正式结果不变，未重扫缓存 |
| 6.1 sol high请求 | 工具不能核实或切换当前对话模型，已说明 | 不声称完成模型切换；脚本／配置hash可查 |

正式任务计算64.129秒，其中完整缓存扫描37.582秒；原渲染5.930秒与扫描并行，已包含在64.129秒中，不能重复相加。峰值aggregate RSS按1秒采样为3,814,838,272 bytes，约3.55GiB；不是理论瞬时精确峰值。4卡筛选的最大allocated为47,243,776 bytes（约45.1MiB），低于单卡4GiB上限；不含CUDA context及reserved显存。

任务平台SUCCEEDED，并有持久pod日志、阶段与完成回执。4卡预留额度与模型请求的授权不同，前者已实际执行，后者未通过工具验证。无CPU性能对照或性能smoke，因此不能从这个耗时推断GPU相对CPU的加速倍数。

图1本地排版修正5.096秒；成功交付验证2.787秒；第一次验证被停止，预算保守计≤130秒（没有精确进程耗时回执，不将130当作实测精确值）。连同打包仍远低于主动计算30分钟；全部阶段、工程成本和可核验的墙钟时间见[最终完成回执](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/completion_receipt.json)。报告撰写不计正式主动计算，墙钟单独记录，未超90分钟。

CPU affinity限制8核，aggregate RSS上限16GiB，新磁盘上限1GiB。没有模型推理、训练、全量共现统计、图重建、额外参数扫描。正式计算之后曾按用户明确请求单独提交并推送旧版portable ZIP；本次修订没有commit/push。代码／配置／环境／任务提交来源见provenance及code目录。



以上是原正式执行历史，不是本次修订的新开销。原始报告、图与 manifest 的修订前版本另存于 `/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/hierarchy_decoder_distribution/20261014T020014Z/visual_revision_20261014T025700Z/before/`，此前已推送的 portable ZIP 保持原字节及 hash。原执行目录与冻结表不被覆盖。

## 附录 C：本次图表修订与证据链

| 项目 | 输入／操作 | 输出与边界 |
|---|---|---|
| 术语与箭头 | 原节点支持数、频率及原图；只更换标签 | V 激活频率明确单位 %；图层级与模型层号分开 |
| 双坐标 h—L | 原 p/L、固定 Q、原抖动、原分位数和相关 | 同 15,537 节点；源表 figure3_coordinate_comparison_source；无重新选择 |
| 完整均值 p | 原 hierarchy_mean_p | 2×6×14 展示格，共用色标；无新均值口径 |
| 峰值类别【事后描述】 | 原 p 逐 Feature 取唯一最大层 | 31,074 个坐标—Feature 标签、36 个比例格；不是预注册检验 |
| 逐节点 p | 原 p 与固定 h | h=0 的全部 20 个、h=5 的原两点；不是扩展文本抽样 |
| 全部频率格 | 原 frequency_overlap_comparison 的 V 25 行 | 原差值与样本数，灰格保留原因；不将不足数值用于比较 |
| 推理审计 | research-reasoning-auditor 对定义、尺度、比较和决策桥的核查 | 保留两个有限认识；不能从描述跳到功能、因果或效益 |

本次本地 CPU 渲染与事后比例计数 23.424 秒，修复图6色标排版另用 3.921 秒；这两个测量程序的最大 RSS 分别约 0.421、0.781 GiB。复核／复制／写报告成本另计，完成回执记录其墙钟。没有新 GPU 分配或远程任务。中文字体只保留执行侧；PDF/SVG 以嵌入字形／路径保证可读，不将字体包加入交付。

修订执行侧：`/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/hierarchy_decoder_distribution/20261014T020014Z/visual_revision_20261014T025700Z`；源输入：`/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/hierarchy_decoder_distribution/20261014T020014Z` 与原阶段一目录；阅读副本：`/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z`。[修订记录与输入hash](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/provenance/visual_revision_record.json)；[修订完成回执](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/visual_revision_receipt.json)；[全部源表](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/tables_cn.md)；`payload_manifest.json` 记录当前每个文件的来源、字节与 hash。

本次用户只要求图与报告修订；未 commit/push，未修改 Focus、Anchor 或原科学状态。完成后停止，不启动共享／分离学习实验、额外参数扫描或训练。
