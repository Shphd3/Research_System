# 既有层级与关系：一页对象对照

**结论：旧材料没有给出一种可直接沿用的统一“语义高度”。** 已找到10/21保守校对稿、学长组合/跨层源码和E17/E18定义；在下述范围未找到10/26 cluster／cosine会议原始稿。类别树、激活包含图、网络层、聚类树与本轮两线索整合各自测量不同对象。

| 材料/原文短语 | 实际计算对象 | 已验证到哪里 | 猜想或缺口 |
| --- | --- | --- | --- |
| 10/21：“深层句子层面的cluster” [S1] | 导师浅层细节+深层句子信息分工的mental model；未指定cluster算法/距离尺度 | 找到保守校对文本与原转写，释义不是重听逐字稿 | 复杂语义/长程偏后层尚是解释；不能补成已验证算法 |
| 10/26会议 [S2] | 本日日索引只检到A17旧行为保留的汇报/审阅 | **未找到所指cluster／cosine原始稿** | 限定为本次搜索范围；不虚构导师定义 |
| M2D2/CLINC粗细树 [S3] | 3粗×3细或10domain×15intent的外部类别标签；feature激活与标签纯度的对应 | E18仅2/91边通过，覆盖1粗/2细；没有浅粗深细职责替换 | 标签树不是feature树，更不是句内整合级别 |
| 组合→组成 [S4] | 非对称激活包含与频率比；图深为到叶最长路径 | E17旧记录24/1212组合复现，91边/53节点、深2 | **频率直接入构图**，不适合Q1独立分组；包含不是语义因果组合 |
| 学长decoder/residual cosine [S5] | 完整decoder方向；或扣除constituent span投影后的残余方向余弦 | 原说明与源码公式吻合；残余近零记NA | 不是编辑响应相似性，也不自动等于功能关系 |
| 跨层/网络深度 [S6] | 各层独立SAE的同token共激活P(f\|g)、decoder几何匹配；层号为计算位置 | 实际代码已找到 | 字典ID不能直接对应；网络深度不等于图深或语义高度 |
| CrossCoder矩阵/层贡献 [S7] | 共享z的包含图与组成名单Jaccard；逐层读数是z×decoder范数 | 已有冻结接口与缓存；14层不是独立激活验证 | 旧图同样含频率比规则；不推出浅→深信息生成链 |
| 1026 R01关系组 [S8] | 配对语义编辑贡献差去共同幅度后的相关，average-linkage树 | G02/G04过旧操作门槛但集中bass；已看留出仅能发现用 | 聚类树高度只是距离；需目标词条件支持null，频率身份/精度也需补齐 |
| 本轮线索整合 [S9] | 两线索四组合的联合项；同token分阶段与位置控制 | 本轮用户给定的待测定义 | 联合/非加性不自动“高级”，需跨措辞和语义候选对应 |

四种“层级”必须分开：**类别树**是外部标签包含；**整合层级**是本轮联合线索利用假说；**网络深度**是Transformer block号；**层次聚类树**是响应距离的合并结构。旧激活包含图又是第五种有向图结构，其深度也不能代替上述任何一种高度。

## 最短公式核对

旧组合图用激活集合计算 P(B|C)=nBC/nC，并显式要求freq(B)/freq(C)≥1.5。旧E17的联合增益是P(C|全部B)−max_B P(C|B)，不是本轮四种线索响应的非加性。图深源码定义为叶节点0、其余1+最大子深。旧图不能用来证明“频率独立构造后仍同频成组”。

学长 residual decoder 是r=d−Proj_constituent_span(d)，residual cosine为两个r的夹角；实际代码在范数乘积≤1e−30时记NA。它与本轮成对编辑差向量的cosine/相关不是同一测量。CrossCoder的共享z在每层乘不同decoder，仅能报告层贡献，不能复制成独立层激活。

## 可追溯来源

### S1 10月21日 cluster／长短程直觉

- 来源：[1021_张鑫讨论_保守校对稿.txt](/data/250010109/Research_System/daily_research_reports/1022/meeting_report/sources/1021_张鑫讨论_保守校对稿.txt:41)，范围[41, 62]。
- 另见：[1021_intuition讨论_保守校对稿.txt](/data/250010109/Research_System/daily_research_reports/1022/meeting_report/sources/1021_intuition讨论_保守校对稿.txt:25)。
- 可允许结论：找到了对应保守校对稿与保留的原转写；未定义数值cluster算法或token距离阈值。
- 边界：网络后面更复杂、深层易低维路由、token→短句→句子的整合过程均为待检验解释，不能当测量定义。

### S2 10月26日 cluster／cosine会议原文

- 来源：[README_cn.md](/data/250010109/Research_System/daily_research_reports/1026/README_cn.md:1)，范围[1, 3]。
- 可允许结论：在指定日期目录、1022源文目录、命名附件与日期txt检索范围内，未找到10/26 cluster／cosine／长短程原始稿。
- 边界：不把10/21释义或本轮用户约束冒称10/26导师已确认方案；全库或其他机器是否另有材料Unknown。

### S3 粗细类别树

- 来源：[detailed.md](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E18_dataset_conditioned_sae_semantic_hierarchy/detailed.md:44)，范围[44, 58]。
- 实现：[semantic_core.py](/data/250010109/MoE_Router/experiments/20260904_a15_13_e18_dataset_conditioned_sae_semantics/semantic_core.py:64)，范围[64, 110]。
- 可允许结论：E18记录91条冻结边仅2条通过，覆盖一个粗类与两个细类；整体浅粗→深细职责替换未出现。
- 边界：类别标签树不是feature父子树，也不是句中两个线索联合利用的整合层级。

### S4 旧feature父子／组合图

- 来源：[EXPERIMENT_SUMMARY.md](/data/250010109/Research_System/Projects/Ruijun_Separable_Gating/MTP/feature—composition0730/EXPERIMENT_SUMMARY.md:34)，范围[34, 64]。
- 实现：[hierarchy_core.py](/data/250010109/MoE_Router/experiments/20260904_a15_13_e17_sae_hierarchy/hierarchy_core.py:62)，范围[62, 85]。
- 可允许结论：E17旧正式记录1212发现组中24组/91边/53节点复现，最大图深2；这是已发表内部记录的历史事实，未读取其确认payload重算。
- 边界：旧图构造直接使用频率与频率比，不能作为Q1的独立于频率分组；包含并非语义因果组合，图上高节点可能更稀有具体而非更粗。

### S5 学长cosine

- 来源：[FEATURE_RELATION_FINDINGS.md](/data/250010109/Research_System/Projects/Ruijun_Separable_Gating/MTP/feature—composition0730/FEATURE_RELATION_FINDINGS.md:177)，范围[177, 238]。
- 实现：[analyze_feature_relation_spectral_bridge.py](/data/250010109/Research_System/Projects/Ruijun_Separable_Gating/MTP/feature—composition0730/code/analyze_feature_relation_spectral_bridge.py:233)，范围[233, 280]。
- 可允许结论：定义和实现已直接读到；本次未重算学长参数更新/训练收益，也未将其历史结果升级。
- 边界：不能混为激活cosine、成对编辑差值cosine、语义相同、功能相同或时间传播。

### S6 网络深度与跨层feature匹配

- 来源：[analyze_cross_layer_feature_relations.py](/data/250010109/Research_System/Projects/Ruijun_Separable_Gating/MTP/feature—composition0730/code/analyze_cross_layer_feature_relations.py:114)，范围[114, 143]。
- 另见：[analyze_shared_feature_properties.py](/data/250010109/Research_System/Projects/Ruijun_Separable_Gating/MTP/feature—composition0730/code/analyze_shared_feature_properties.py:123)。
- 可允许结论：实际源码存在并定义了这些对象；跨字典编号不直接相同，匹配只建立候选几何/共激活关系。
- 边界：没有从这些计算自动得到逐层信息诞生或语义整合因果链。

### S7 CrossCoder关系矩阵／层贡献

- 来源：[protocol.md](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_25_joint_feature_graph/protocol.md:133)，范围[133, 147]。
- 可允许结论：已有冻结协议与完整缓存/统计资产；共享z不是14个独立层激活。
- 边界：频率比也直接入旧CrossCoder图；层幅度不能说明何层先产生信息，不能与R02频率独立响应组混为同一对象。

### S8 上一轮响应关系／层次聚类树

- 来源：[summary_cn.md](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R01_bounded_panel_20261026/summary_cn.md:3)，范围[3, 17]。
- 实现：[analyze.py](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/offline/analyze.py:231)，范围[231, 258]。
- 可允许结论：R01 G02/G04满足旧操作判据，主要由bass支持；旧null没匹配目标词条件支持。已查看的旧留出只能作本轮发现材料。
- 边界：树高不是语义高级程度；旧频率BF16/FP32和历史parent hash缺口不能直接用于本轮严格Q1。

### S9 本轮两线索语义整合

- 来源：Current researcher request,2026-10-26。
- 可允许结论：这是本轮明确的新操作性定义，尚待冻结与执行；不冒称旧图/标签树已证明。
- 边界：非加性本身不等于高层语义；还需要跨措辞、预定关系对应及超过仅位置对照。

## 搜索与访问边界

本次定向阅读1026日索引/meeting_report、1022会议阅读包内的1021原文、A15_13 E17/E18、A15_25、A15_27R01及其引用的学长MTP说明/代码；额外按1021/1026命名与1026日期检索了可用文字附件。没有全盘搜索所有机器，没有读取封存TEST实例/标签/激活缓存，没有加载模型或字典，没有前向、训练、干预或修改旧记录。历史Summary中的旧确认结果只按原记录引用，不称本轮独立重算。完整逐对象数据见 [definitions_audit.json](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R02_frequency_distance_integration/audit/definitions_audit.json)。


CrossCoder当前接口与真实语料描述另由 [资产审计](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R02_frequency_distance_integration/audit/crosscoder_asset_audit.md) 和 [固定八位置描述](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R02_frequency_distance_integration/real_corpus/README_cn.md) 保存；它们不对齐E16的feature编号，也不替代新面板的确认检验。
