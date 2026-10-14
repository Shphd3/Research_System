# 高组成列表重叠的背景解释审计：Detailed

[Summary](summary_cn.md)。这是新Anchor下的有限派生审计，不替换阶段一正式结果。执行完整；研究者机制判断Unknown。主阈值未更改，没有科学参数敏感性版本。没有commit/push、Focus／旧Anchor或科学状态变更。

## 1. 目的、比较与资格

上层问题是内容如何共享学习或分到专家。本轮只检查组成列表J的含义：普遍背景覆盖与具体关系额外富集能否区分。边门槛仍是nA、nu≥200、nAu≥20、5nAu≥4nA、2nAu≤nu、nu≥2nA；固定14个一基偶数层2–28，最终训练999,997,440位置状态，TRAIN阈值0.051281172782182693。10,485,760位置，D5,238,097、V5,247,663；81块，原文档去重独立性Unknown。

原正式候选池确实使用V支持≥200及V列表非空，因此V参与了筛选。新对照先只按D频率与D列表大小固定，再查看J/V/text；但不能让旧VAL变成独立确认集。所有结论均为同bin描述或定义推论，不报告总体p值或独立文档置信区间。

## 2. 执行前固定参数与成本

新目录 `/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/background_audit/20261013T220338Z`；执行前execution_record.json及execution_record_cn.md记录至多三项、15–25分钟交付预估、CPU计算1–5分钟预估。当前主机实际8CPU时间核／128GiB，无新付费资源；最多2进程。D侧频率允许目标0.8–1.25倍、D列表大小完全相同（均8）、D支持≥200；排除6个展示节点，seed20261014按target派生。每高J对最多32个唯一角色配对，允许端点共享并报告；无匹配不扩阈值、不依据J/V/text换对象。65×70与65×69小型匹配笛卡尔元数据池抽取，未读120M全池数组。

冻结选择记录先落盘，再读取对照V列表和计数，见[冻结记录](provenance/controls_frozen_before_review.json)。本次各32对，无匹配短缺；各组有53与52个独特端点，非32组独立复制。所有64对后来均满足V支持与非空列表，V没有用于重抽或筛除。原条件并未被放宽。

核心计算实测7.011秒；主进程峰值RSS96.61MiB，最大子进程65.49MiB（不是全进程同时峰值）。图表与报告整理另外记录；这些小表与3图无需GPU。阶段一缓存及完整数组未复制或覆盖；现成总矩阵仅用mmap读取64对的标量单元，未完整读入或计算。

## 3. 第一步：共同项的背景和额外概率

[完整52行D/V表](tables/edge_background.csv)每行字段N、n_A、n_u、n_Au、p_u、P_u_given_A、P_A_given_u、lift、extra_probability、extra_percentage_points及raw_edge_row_index。extra是同侧条件概率减背景，不是因果效应。主表只核查三个高J端点到共同8项的24条边，以及用户指定的0→327、0→10915两条边，全部为原图已通过复核边。

1→7415的V背景0.929377，条件0.801946，lift0.862886，额外−12.743个百分点。这条边通过原门槛并非程序错误；原门槛没有要求超过背景。两对高J同用一组8节点，7个Top10；共同项14不是Top10但覆盖67.934%，不是罕见内容。D侧14额外概率为25.985、26.821、17.627个百分点；V为25.609、25.514、18.536。高频与富集可以同时成立，也不推出单义语义。

已有块计数描述：1、17、242→14在两侧全部有A支持的块都额外富集；V共41块。1→7415在V只有1／41块额外概率为正。0→327、0→10915在V有支持的39块均为正，另2块nA=0。它们是相关块描述，不是独立样本置信区间；详细q10／q50／q90见[selected_block_summary](provenance/selected_block_summary.json)。

0→327 D/V共同支持765／600、lift70.254／72.701；0→10915为719／566、lift80.029／83.390。0→327的600经原始边零基row1、V总矩阵[0,327]、对应块计数加总三方一致。转述737／605已被来源线程更正，不称旧统计错误。0→10915原始边零基row35；1→14零基row47。

![背景与额外概率](figures/01_background_excess.png)

图1读法：行是共同项或两条有界反例，列是源特征，数字为V额外百分点，灰色为本轮未核查。多数共同项普遍，但14有额外关联，0的两条反例也很强。只能比较所列关联，不能把红色叫功能，或把高频叫噪声。

## 4. 第二步：共同删除Top10，两种操作分别记录

固定Top10按D支持递减、同分按ID；列表为[13964, 516, 8060, 10807, 7388, 5913, 7415, 5147, 8345, 13830]。D/V频率均大于0.5，D范围81.501%–99.296%，不是decoder范数、入度或TRAIN频率排序。

定义推论：若u的频率要至少是A的2倍，则出现率大于0.5的节点不可能有出邻居。Top10原始出度D/V都为0，故它们是汇点／叶节点。叶节点不会作为两个保留节点之间路径的中间点；删除它们后保留节点间路径不变，所以本次“过滤原组成列表的重叠”应等于“原始图删节点后重新约简的重叠”。这是代数／图结构预期，不是独立机制稳健性检验，也不证明删除节点改善了对象。完整推理见[读本](provenance/reduction_reasoning_note_reading_copy_cn.md)。

两种操作仍分别实际记录：[完整24行操作表](tables/deletion_comparison_cn.md)、[完整两列表JSON](provenance/joint_deletion.json)。重新约简只计算D的48个、V的46个相关可达节点；独立NetworkX参考在两侧逐源吻合，见[核验](provenance/validation.json)。高J两对在D/V均8／8缩为1／1，只剩共同项[14]且J=1；单项警告是实质限制。0／3在D为32／2、V为32／0；V单方空列表的J=0另标，不能混进原正式非空低J候选。0／4两侧均32／1、J=0，单项警告保留。没有恢复额外直接边，不是算法偷换，而是删汇点的本图性质。

![两种删除操作](figures/02_joint_deletion.png)

图2只展示V，D/V全表在链接内。读数同时看大小、共同项与警告，不能只看J。两张相同单项列表J=1不认证非平凡。

## 5. 第三步：固定匹配对照及文本

[两组对照摘要](tables/control_summary_cn.md)、[完整64行CSV](tables/matched_controls.csv)。1／17对照D/V J=1均8／32；1／242对照D为12／32、V为10／32；两组D/V中位J均0.7778，范围0–1。V共同项含14的对照分别13／32与9／32。这些现象削弱展示高J独特性，但不构成总体频率估计、显著性检验或学习收益对照。

原高J并列区间115,027,260–120,380,886，已有记录给出5,353,627对（含端点，共同组大小不是重新排名所得）。原源码每极端有理J组最多保留8个按ID排序代表，再提名；两对高J共享1。原目标J本来按极端选择，不能把其J=1高于随机对照中位数解释为统计验证；本轮对照也不是完整同频率总体，仍有频率0.8–1.25倍误差、列表内容与样本分布未匹配。

![D侧固定可比对照](figures/03_matched_controls.png)

图3横轴是冻结抽样顺序，不是J排名；点为D/V J，虚线是原极端对象J=1，无抖动伪造数值。没有误差条或p值；结论是匹配对象中高J也常出现，不是证明所有高J都无效。

[全部118条文本核查](tables/text_review_cn.md)保留随机／高激活差异、目标token、可见前文与原数组row；右文未用于判定。0有词族线索及跨词边界例；1的A-only五个高例中3个在10239；17高例有姓名碎片而随机更杂；242高例混合医学引用与摘要结构。1／242高both五例在3196／3197，但总体245个V both分布109上下文，最大单上下文占4.08%；不能把展示偏好外推总体集中。0的词族不认证327／10915，本轮未提取这些目标节点或64对对照的文本，这一环仍不足。

原展示1／17与1／242的V直接共激活分别仅2与245位置，lift为0.028515与0.679395；列表重叠与直接共激活是不同读数，见[既有候选参考](provenance/original_pair_reference.json)。

## 6. 多层几何只作描述

只读取原decoder_geometry.npz的norm[:,feature]，不训练也不生成新的层内图。候选1／17／242在24、26、28层的范数占比分别44.80%、70.44%、40.11%；0在第2层占48.59%。这些几何轮廓不同，但联合编码每位置只有一个z，逐层幅度占比等于范数占比。不能推断层功能、因果贡献、在线路由或专家收益。[原值与摘要](provenance/decoder_geometry_description.json)。

## 7. 来源路径、字段、行及可追溯性

原run_root：`/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/feature_relation_phase1/20261013T173130Z`。输入路径、bytes与小文件SHA见[source_manifest](provenance/source_manifest.json)；大总矩阵只记录原路径与大小，未重新hash。派生表的行号用CSV表头后第1行为第一个数据行；raw_edge_row_index是原npz数组零基索引；文本row是原examples零基索引。

| 派生证据 | 原路径／字段／行键 | 本轮字段与定位 |
|---|---|---|
|背景、支持、lift与extra|run_root/feature_frequency.npz:n[side,node]；graphs/raw_edges.npz:A/u/cD/cV/passV，同一raw_edge_row_index|edge_background.csv中的A/u/side与原数组行索引；完整52行|
|分块核查|run_root/block_edges/block_000.npy至block_080.npy对应原边行；feature_frequency.npz:block_n[block,node]；split_manifest.json:blocks[id]|edge_background_blocks.csv按A/u/side/block；只读26边列|
|原组成列表|run_root/graphs/reduced_D.json与reduced_V.json:lists[node]|joint_deletion.json:rows按pair_id/side/operation，完整C_A/C_B|
|有限对照|D频率及D列表大小先选；run_root/counts/total0.npy与total1.npy:[A,B]只读所选单元|controls_frozen_before_review.json.controls[index]；matched_controls.csv顺序一致|
|选择偏差|run_root/candidates.json:pairs[0/1].discovery_tied_rank_min/max；code_snapshot_v2/candidates.py:keep_extremes、pair_search|scope_and_selection_audit.json.tie_group_size与selection_bias|
|118展示文本|run_root/pair_examples.json:examples[row]，target_token_text、model_visible_prefix、selection_labels、context_index、eligible_position|all_text_review.csv保留原row、目标、末段、原定位；不使用右文标签|
|总体上下文集中|run_root/class_positions/pair_class_side.npz:context、target_positions_per_context|context_concentration.csv按pair_id/side/class，n、unique_contexts和top1/top5|
|几何|run_root/decoder_geometry.npz:norm[:,feature]；原layer_contribution.csv|decoder_geometry_description.json，几何含义与函数证据分离|

新代码：`/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis_tools/background_audit/analyze.py`与report.py；执行日志`/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/background_audit/20261013T220338Z/analysis.log`。源审计线程thread/read未返回，已终止该只读请求；本轮依据落盘Anchor和已核验资产，未依赖远程chat转述作为数值证据。当前主机进程与新派生目录未发现其他同题任务，文件锁防止本run双写；这一检查不冒充跨主机全局证明。

## 8. 结果裁定与认识链

事实支持有信息的具体统计关联；解释层面，展示高J多项被普遍节点占据、删后只有14、同频率／列表大小对照中也常见J=1，削弱把它直接用作内容关系分组依据。节点14的正富集在块上保留，这一正结果不能被背景疑虑抹去；但其语义未测、频率很高，不补足代理有效性。高频不等于无意义；本轮没有干预激活、功能或损失，也没判断应删除这些特征。

昨天原以为（待核查候选解释）：“列表高J或许给出可比较的共同内容对象”；今天证据：高J两对重复同一8项、7项普遍，删后只有14，匹配对象也常见J=1，而14及0的两条具体边仍有超背景关联；保留／缩窄：保留具体关联，缩窄高J即内容相似的解释；未答：目标节点语义、因果、难学性与学习收益；唯一下一问题（AI建议）：剩余具体关联能否在目标token与上下文中给出超出普遍背景的、可比较的内容解释？

研究者判断Unknown。完成本轮有限诊断后停止，不改旧Anchor／Focus，不commit/push，不自动功能验证或训练。
