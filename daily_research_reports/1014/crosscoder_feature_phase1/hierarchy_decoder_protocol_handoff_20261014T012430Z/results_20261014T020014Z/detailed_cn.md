# 完整结果：特征图层级与跨层解码幅度分布

结果记录日期：2026-10-14T10:19:13.139328+08:00（北京时间）。处理者Codex，原科研线程01a1343f-32aa-7500-9835-000956218089。运行20261014T020014Z，平台任务pt-icv8hyi3。

主Anchor：[完整Anchor](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/hierarchy_decoder_distribution_anchor_user_20261014_cn.md)。冻结Protocol：[本次批准的完整契约](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/provenance/protocol_frozen.md)，SHA256 `39530a9a36eee0403a8bc3ee53ad19d3e82a5dcb18c86fa7287c1ca4cc8894fb`。[简短中文结论](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/summary_cn.md)。

## 0. 先读结果与证据资格

整体不支持“统计图层级越高，解码幅度平均位置整体越深”；没有由此证明整个p分布向浅层移动。主相关−0.277976；频率内11格7正4负，方向混合。局部图不替代全体结果，正向格不能补救主结果。

执行测量为ELIGIBLE：按冻结对象、窗口、主集合、坐标和比较规则完成；解释为BOUNDED：频率耦合、同bin、节点依赖和工具保真限制仍在。研究者的机制判断、科学状态转移和下一轮决策为Unknown，本报告不关闭问题。

## 1. 目的与实际对象

研究问题是统计图层级与跨层解码幅度分布是否对应。本轮减少的是“图层级能否作为模型深度代理”的不确定性，不是判断何种专家结构更有训练收益。

最终checkpoint为 `/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/runs/formal_14layer_batchtopk_a22/checkpoint_000999997440.pt`，累计999,997,440训练位置。Base `/data/share/Qwen3-0.6B-Base` 冻结，revision da87bfb608c14b7cf20ba1ce41287e8de496c0cd。14个激活空间为零基block1,3,…,27，即一基2,4,…,28的residual-post（最终全局norm之前），每个向量维1024；字典16,384。不是0.5B权重，也不是另一28层字典任务。

沿用已有TRAIN均值／向量RMS、原严格分数门控阈值0.051281172782182693。训练BatchTopK不是逐位置恰好Top256。模型和coder均未重新加载；本轮没有模型前向、训练、激活生成或全量共现计数。

数据为原10,485,760合格位置、10,249完整／尾上下文；按128上下文成块共81块，种子20261014。D=5,238,097，V=5,247,663。原bin同一份，原文档ID未保留、近重复独立性未知。

## 2. 图层级、解码量与假设的边界

边A→u要求两端支持≥200、共同支持≥20、P(u|A)≥0.8、P(A|u)≤0.5、n_u≥2n_A。在D发现、V只复核这些原始边，分别约简。组成列表是直接出邻居，尚非认证的语义组成。

h为完整约简图到无出边节点的最长路径：叶节点0，其他节点1＋最大后继h。沿路径频率至少翻倍，所以无环性由构造保证。孤立、零支持、低支持的h=0不自动成为基础语义。

一个Feature在一个位置只有一个联合非负z，各层解码分量为z乘本层decoder向量；分量幅度为z乘decoder L2范数。p把14层范数按总范数归一，L以实际一基层号对p加权。共同z约消，p/L是decoder几何，不随该Feature的文本改变。

零总范数应记NA；本轮16,384个Feature均无零总范数或非有限几何，主集合全部15,537个有效。GPU FP64归一化与CPU公式最大差约0；所有p行和为1。

**L仅表示幅度加权平均位置。** 浅层和深层可以同时有峰。L增加不推出整条分布后移；本轮也不从负相关推出整个分布向浅层移动。不同Feature向量可能抵消，幅度相加不等于重构能量，更不是独立预测贡献。

原假设预期较高h整体更深。最强竞争解释是频率与h由建边规则耦合，另有层尺度与工具保真差异。沿长度h路径，节点支持≤N/2^h，这是结构约束，不能当作新机制发现。

## 3. 既有图事实与完整集合

D/V约简边分别149,945／146,947。V全字典h直方图为867、8,896、5,347、1,209、63、2；其中847个是孤立节点，h=0的另20个为非孤立合格叶节点。主集合Q=两侧支持≥200且V非孤立，为15,537个；仅支持合格集合恰好与Q相同，引用同一结果，不算独立稳健性证据。

D全字典h直方图835、8,563、5,544、1,356、82、4；同一Q上为20、8,561、5,537、1,336、80、3。D孤立815，D/V本侧零支持353／393，1—199支持462／424；这些资格和孤立性是交叉标签，不混加。[完整节点及资格](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/tables/hierarchy_members.csv)；[分类计数](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/tables/hierarchy_counts.csv)。

最高V层级5仅937、3461。按h和ID选锚点，再完整沿出边展开，分别19节点45边、22节点56边，并集30节点101边；节点选择在新p/L读取前冻结，不按解码结果或文本内容筛选。

## 4. 本次新结果：全体平均位置

| 图层级h | Feature数 | L中位数 | L四分位范围 |
|---|---|---|---|
| 0 | 20 | 22.717 | 22.321—23.414 |
| 1 | 8,896 | 19.902 | 14.319—22.759 |
| 2 | 5,347 | 15.007 | 12.660—20.696 |
| 3 | 1,209 | 14.305 | 12.420—18.297 |
| 4 | 63 | 16.226 | 13.527—19.187 |
| 5 | 2 | 18.509 | 16.704—20.313 |


L以实际模型block号计量。每Feature一票，无激活频率加权。主描述性相关采用平均并列秩；未计算p值、独立节点置信区间或事后合并h组。表中的四分位区间是Feature分布，不是估计误差区间。

h=1到3的中位数下降；h=4回升，h=5两点分散。整体负相关与“逐档严格单调”是不同命题。这份证据缩窄原预期：目前不能把统计图层级当作更深平均解码位置的整体代理。

[图3实际源表](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/tables/figure3_source.csv)含全部15,537个点。图上抖动仅改变排版横坐标，源h保持整数。

## 5. 本次新结果：14层分布形状

下表为主Q内每Feature等权的平均p，单位**百分比**；每行和约100%，显示舍入误差。不是把范数相加后再归一，未按频率或z加权。各层原始精度及D/raw参照见[各层级14层平均p](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/tables/hierarchy_mean_p.csv)。

| h | n | 2 | 4 | 6 | 8 | 10 | 12 | 14 | 16 | 18 | 20 | 22 | 24 | 26 | 28 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 20 | 2.508 | 0.284 | 0.493 | 0.776 | 1.136 | 1.878 | 2.373 | 3.395 | 5.662 | 9.507 | 12.339 | 14.721 | 17.715 | 27.214 |
| 1 | 8896 | 15.391 | 1.076 | 1.535 | 1.820 | 2.127 | 2.838 | 3.084 | 3.625 | 5.599 | 7.896 | 10.687 | 12.745 | 14.581 | 16.998 |
| 2 | 5347 | 25.057 | 1.530 | 1.896 | 2.012 | 2.241 | 2.817 | 2.919 | 3.222 | 4.941 | 6.822 | 9.475 | 11.091 | 12.030 | 13.947 |
| 3 | 1209 | 30.196 | 1.970 | 2.241 | 2.249 | 2.397 | 2.845 | 2.885 | 3.123 | 4.494 | 6.044 | 8.028 | 9.736 | 10.543 | 13.249 |
| 4 | 63 | 24.541 | 1.625 | 1.928 | 2.028 | 2.348 | 2.891 | 3.026 | 3.371 | 5.044 | 7.053 | 8.958 | 10.739 | 11.618 | 14.831 |
| 5 | 2 | 17.748 | 1.430 | 2.188 | 2.178 | 2.617 | 2.888 | 2.883 | 3.135 | 4.494 | 5.396 | 7.431 | 8.994 | 10.858 | 27.760 |


h=1、2、3的第2层平均p递增，第28层平均p递减，同时深层仍有非零幅度。这是轮廓组成的变化，并非单峰平移。h=4和5又不同，最高级只含两点。

937的p在第28层为46.07%，第2层为12.04%，L=22.118；3461在第2层为23.46%，第28层9.45%，L=14.899。两个最高层级Feature也不能概括为相同解码深度或相同功能。图2保留同30节点的全部14层，按h再ID排序，没有按L重排来制造层级对应。

平均p会掩盖组内差异；个体表与热图仍保留。没有做分布随机支配、整分布平移或功能检验；这类结论不能由均值表代替。

## 6. 本次新结果：频率竞争解释检查

在Q上用D侧log10(n_D/N_D)固定5个分位组，重复边界合并，本轮实际5组。组内预先比较相邻h，在两组观测频率范围交集中保留实际节点，各≥20才作为可比较格。即使交集只一个值，只要双方实际有效节点各≥20也允许固定频率局部比较；本轮没有通过这一单值格门槛的情况，不表示该情况在定义上不可能。

以下列出主V的**全部25格**；组编号1为最低频组，5为最高频组。NO_GROUP缺一个h组；NO_OVERLAP观测频率范围不交；SMALL_N交集内至少一侧<20；COMPARABLE_RANGE为达到门槛的区间格。完整频率边界、两组x/L四分位数与D参照在[全部频率比较格](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/tables/frequency_overlap_comparison.csv)。

| D频率组 | 相邻h | 交集内n低／高 | L中位差（高−低） | 状态 |
|---|---|---|---|---|
| 1 | 0—1 | 0/0 | NA | NO_GROUP |
| 1 | 1—2 | 733/1642 | +0.1700 | COMPARABLE_RANGE |
| 1 | 2—3 | 1640/682 | +0.9182 | COMPARABLE_RANGE |
| 1 | 3—4 | 678/38 | +0.6882 | COMPARABLE_RANGE |
| 1 | 4—5 | 19/2 | +3.5431 | SMALL_N |
| 2 | 0—1 | 0/0 | NA | NO_GROUP |
| 2 | 1—2 | 1422/1367 | +0.1940 | COMPARABLE_RANGE |
| 2 | 2—3 | 1352/291 | +0.4572 | COMPARABLE_RANGE |
| 2 | 3—4 | 290/20 | +4.6153 | COMPARABLE_RANGE |
| 2 | 4—5 | 0/0 | NA | NO_GROUP |
| 3 | 0—1 | 0/0 | NA | NO_GROUP |
| 3 | 1—2 | 1809/1126 | +0.4123 | COMPARABLE_RANGE |
| 3 | 2—3 | 1098/165 | -6.9652 | COMPARABLE_RANGE |
| 3 | 3—4 | 42/4 | +3.7703 | SMALL_N |
| 3 | 4—5 | 0/0 | NA | NO_GROUP |
| 4 | 0—1 | 0/0 | NA | NO_GROUP |
| 4 | 1—2 | 2208/829 | -0.5367 | COMPARABLE_RANGE |
| 4 | 2—3 | 814/62 | -8.9823 | COMPARABLE_RANGE |
| 4 | 3—4 | 0/0 | NA | NO_GROUP |
| 4 | 4—5 | 0/0 | NA | NO_GROUP |
| 5 | 0—1 | 0/0 | NA | NO_OVERLAP |
| 5 | 1—2 | 2443/371 | -0.3998 | COMPARABLE_RANGE |
| 5 | 2—3 | 181/8 | -10.5028 | SMALL_N |
| 5 | 3—4 | 0/0 | NA | NO_GROUP |
| 5 | 4—5 | 0/0 | NA | NO_GROUP |


11个区间格达到门槛，7正4负，格差值中位数+0.193974层。它是11个格等权的摘要，不是所有Feature的平均效应、调整后相关或因果效应。方向差异明显，例如中间频率组h=2→3为−6.9652层，而较低频率组h=3→4为+4.6153层，后者较高h只有20个节点。

可比较格覆盖h对1—2、2—3、3—4；h=0与1无可比范围，h=4与5小样本。五分位和连续范围交集不保证两组频率分布相同，仍有组内频率残差。整体负向、若干频率内局部正向可以同时成立，不能据此断言“控制频率后整体反转”，也不能宣布频率已造成原趋势。

## 7. 固定D/raw参照

| 条件 | 同一Q有效数 | 描述性Spearman |
|---|---|---|
| V_train_normalized | 15537 | -0.277975867 |
| D_train_normalized | 15537 | -0.279321478 |
| V_raw_coordinate | 15537 | -0.157788083 |


D参照保持同一Q、同一decoder、同一D频率分组，只换h定义。D频率检查同样11格、7正4负，中位差+0.237944层。D/V高度相关且V来自D候选边复核，不是独立重复。

raw参照使用保存的每层RMS恢复范数，再计算p_raw/L_raw；只做预定整体摘要，不追加频率版本或选择更好坐标。raw相关仍负，但数值变化提醒层尺度影响。三个参照都没有证明整体分布移动、层功能或因果关系。[整体与参照统计](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/tables/depth_vs_layer_summary.csv)。

## 8. 文本与同位置幅度：完整交付

30节点各5个随机、3个最高z，合计240个Feature—位置记录，随机150、高激活90，没有两类重合导致的减少。共226个上下文，跨Feature可共享位置／上下文；这不是226个独立文档样本。

全部640块共16,098,567,532 bytes读取并核对SHA256；筛出V活跃位置后，各节点数量均等于已保存n_V。流式抽样按全局位置升序、每Feature固定PCG64种子合并；worker完成顺序不参与抽样。高激活同z按位置升序。抽样没有依据文本好看程度重选。

随机样本是V侧该Feature全部活跃位置中的等概率5条。分块合并时先按全体旧＋新位置等概率决定来自旧／新批的数量，再从旧的均匀reservoir抽对应子集，因此保留均匀不放回性质。它不是按块等权抽5条，也不是旧A-only/both类别样本。

[全部随机／高激活文本](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/text_examples_cn.md)保留完整模型可见前文（包含目标token）、目标token和位置、右文阅读辅助、z与h。[机器可读文本](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/text_examples.jsonl)和[逐位置14层幅度](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/tables/text_layer_amplitude.csv)可核对。同一位置的14层a=z×norm，不是换目标token拼出来的响应。

仅作有界可读性观察：937展示的随机5条和高激活3条目标都为t或空格+t；3461高激活3条目标均为Edit，随机5条含编辑标记闭合和article(s)等。这提醒最高统计层级也可能与词片或格式有关，不能自动叫“更复杂主题”。没有从这些例子认证单义语义、进行人工语义标注或把它们纳入趋势筛选。

交付核对逐条重新连接原索引与bin，240个目标token ID／offset一致，14层a与z×范数一致。完整前文留档；本轮只对展示目标及必要前文做辅助阅读，不声称完成人工语义验证。

## 9. Protocol符合性、修正与成本

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

CPU affinity限制8核，aggregate RSS上限16GiB，新磁盘上限1GiB。没有模型推理、训练、全量共现统计、图重建、额外参数扫描或commit/push。代码／配置／环境／任务提交来源见provenance及code目录。

## 10. 证据链与缺项

| 有界结论 | 原输入→计算→源表 | 资格／限制 |
|---|---|---|
| 整体平均位置不随h增大而整体更深 | reduced_V.depth＋decoder_geometry.norm→p/L→figure3_source、depth_vs_layer_summary | 15,537节点，描述性负相关；不推出整分布后移／前移 |
| 分布有浅深并存、最高两点轮廓不同 | norm→完整p→figure2_source、hierarchy_mean_p | 同30局部节点及全Q均值；均值会掩盖异质性 |
| 频率内方向混合，未排除频率解释 | D n＋固定分位边界＋V h/L→frequency_overlap_comparison | 全25格，11合格；组内残差与缺覆盖仍在 |
| D/raw负向参照存在 | 固定Q，h_D或raw_norm→预定摘要 | 同一字典／数据，不是独立确认 |
| 文本与位置及共享幅度可追溯 | 原CSR＋prefix/records＋bin/tokenizer→text_examples、text_layer_amplitude | 240记录，语义功能验证未做 |

所有必需计算与交付已完成；没有用缺项补造值。仍未检验的事项为文档独立性、单义语义、层功能、因果组合、长程学习效益及MoE分发收益。原第28层工具FVE86.4722%、固定替换CE+0.305962nats来自既有报告，本轮没有重测。

## 11. 认识变化、下一问题与停止

原先待检验的直觉是：统计图较高的Feature可能对应更深解码分布。今天全体数据给出相反的平均位置方向；14层p显示浅深成分并存；频率局部比较混合。保留局部结构可用于选对象的可能性，但缩窄“h是模型深度代理”的整体说法；频率、词片／格式与工具尺度如何共同影响仍未回答。

AI建议的唯一下一讨论问题：**我们应如何理解统计图层级与频率的耦合，才决定是否继续把h作为后续分层分析对象的索引？** 这是讨论建议，不授权下一轮计算或训练。研究者的下一步决策Unknown。

本轮交付后停止，不修改Focus、旧Anchor、旧统计或科学状态，不启动共享／分离学习实验。

完整来源：执行目录 `/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/hierarchy_decoder_distribution/20261014T020014Z`；原输入目录 `/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/feature_relation_phase1/20261013T173130Z`；portable目录 `/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z`。[全部源表索引](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/tables_cn.md)；[三类图及读图说明](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/figures_cn.md)；payload_manifest.json列每文件来源和hash。
