# Protocol：R10领域成员整体分析

## 0. Approval Snapshot

状态APPROVED_FOR_CACHE_ONLY_ANALYSIS。用户当前完整替代指令已明确授权续接Anchor、Protocol、五项缓存统计、图表和报告，无需逐步再确认。R10-v1冻结于2026-10-30T02:41:30.403304+00:00；[精确配置](provenance/config.json)。主Anchor[15_27_04](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_27_natural_language_feature_response/subanchors/15_27_04_domain_member_atlas_anchor_cn.md)，现有自然语言响应Focus。A–G科学范围来自本次明确指令；下述重采样、匹配和支持标签是范围内AI操作实现，不等于新增科研判断。实验角色为代理指标审计与描述分析。无新模型前向授权，科研接受/关闭Unknown。

## 1. Terminology / Definitions

成员指同A22的16,384共享z坐标。文档响应为固定160位置z均值含零；原始AUC为30×30文档对的数学响应排序概率、平局半次。feature发生率分母DCLM65,536；token频率分母本批19,200。单位几何、实际贡献平方能量、完整表征方差严格分开。

## 2. Anchor Alignment

一个问题：全字典领域区分成员在频率/共同谱/真实输入关联上如何分布？三步：冻结支持与排名；比较频率和共同谱几何/实际使用；检验真实token与固定词上下文。完成所有缓存支持项并列明缺口后停止，不要求出现正结果。

## 3. Tested Hypothesis

低频相对富集、不同谱位置、跨措辞上下文分别检验，互不替代。

## 4. Rival Explanations

候选池本身组成、字典普遍前偏、平方分布隐藏符号、向量交叉项、词汇/格式/后缀共同改变。对应池背景、匹配、余弦/子空间、先向量和再平方、固定目标配对。

## 5. Data Construction And Provenance

R04每域60文档：30发现/10开发/20旧留出；使用原文档分组，位置[32,192)。每篇相同160位置使域/文档等权。检查组无跨划分重复；源文件hash可追溯。留出已经使用，标探索复核，不能称盲测。读取前当前严格资产检查通过。

## 6. Learning Task And Permitted Supervision

不拟合分类器、不训练字典或模型，无优化器。领域标签沿用原真实网页摘录内容审阅；来源、体裁与词汇仍混淆。PCA只是离线协方差统计。

## 7. Model / Architecture And Frozen Variants

固定A22 checkpoint SHA09b432e98dd7426f9ea4170809d75068a2ada2ed38c1e97d3fa18e119cd79628；14个奇数block1–27联合编码，共享z，门控阈值0.051281172782182693。block27 residual-post为最终归一化前hook；decoder模型尺度=TRAIN_RMS27×原权重，不再按h单位化或白化。零decoder单列。

## 8. Training Objective And Optimization

不适用。模型前向、训练、参数更新、路由干预、距离扩展均为0。

## 9. Conditions, Seeds, And Checkpoints

种子2026103004；文档/家族重采样各1000次，匹配背景1000次。至少一域有5篇发现文档激活即合格，不能要求两域。区分方向按AUC偏离0.5；排序绝对偏离降序再ID升序；精确0.5不入方向排名。主集合取全部方向校正AUC≥0.75；冻结0.70/0.80与每域Top16/64/128敏感性，不补人不调门槛。

## 10. Primary Metric And Frozen Analysis Plan

图1原频率阈值0.002593994140625/0.0134429931640625，边界归低组；少于20次支持不计三组分母、仍保留表。log等宽敏感性0.0045172553628813825/0.06686505701697326。

共同谱用60发现文档9,600个真实h，一次共同均值，域/文档/位置等权。通过raw-h协方差、特征方程和正交性核对后复用完整1024PC；样本分母9599与人口权重只差统一标量、不改方向。旧R07为同一谱，真正独立参照缺失；旧R08目标谱不得替换。

图2单位decoder逐PC内积平方，全谱1；16段各64PC。另拆PC1/PC2–64/PC65+，维数参照1/1024、63/1024、960/1024。保留成员分布、均值、中位数。

匹配背景按原频率低/中/高/不足×总发现支持文档数除10向下取整，支持合格非零decoder池包括入选成员。每层无放回抽相同规模，两组互斥，1000次；报告主集合被抽中比例。此为条件字典参照，非独立零假设或重新选择的文档bootstrap。

图3逐PC和64PC段分别取两组平均平方分布较小值求和；PC2–64同时保留完整质量及段内归一化重合。附全部跨组绝对余弦和真实decoder子空间。实际贡献在40篇旧留出逐token先求组内z×尺度还原decoder向量和，再平方投影，文档等权；四种组×输入条件。总平方范数≤1e−12报NA，不称完整h解释率。

## 11. Secondary Metrics And Guards

留出每域20文档独立重采样1000次，保持发现方向，95%点式百分位区间下界>0.5才标复核支持；不换人，不做确认性多重发现。

图4token按本批120文档19,200有效位置计数，保留子词标点及特殊ID清单；类型计数高位经验1/3、2/3分位，同频不拆。类型/位置分母各报。成员高响应阈值为发现正z第90百分位，留出严格超过；操作支持要求发现至少20正事件，留出至少5高事件跨2文档，不足保留。先成员内比例再成员等权；散点feature参考率对高响应token语料内频率中位数。实例固定发现前三名/域，每文档最多一个高例，优先另一文档同ID低例，只给已读前文。

图5复用48家族24/12/12、2域2措辞2后缀。A为同目标、同配对位置的领域差。上下文复现标签：至少一个目标条件中两措辞在发现/留出同非零方向，目标内措辞均值的家族95%区间两划分均排零，每划分至少3活跃家族。另记与自然文本方向一致与否。词面+后缀标签：E1−E0对两域/措辞均值，发现留出同号且区间排零、支持充分；交互为两目标间领域差的差，同规则。标签点式探索、可重叠；汇总四类，始终零只能覆盖不足。B纯换目标词不存在，不能把同时换后缀当identity。

## 12. Known Good / Known Bad / Known Confusing Cases

相同文档数组AUC应0.5、全数学更高为1、反转为0；全谱份额1、合并谱段不降低重合；直接模型向量求和与PC系数求和再平方一致。各成员平方能量相加是有意保留的错误对照，不准代替实际贡献。全零fixed-token不判identity。

## 13. Scientific Procedure And Stage Contracts

先查资产/hook/分组/逐位置与汇总一致；再仅用发现冻结成员；再核对共同谱并算五项，保留NA；最后公式独立复算、契约审计、查看实际图片、写双语记录与manifest。某项缺失只阻断依赖，不阻断其余。B与独立谱稳健性缺口保留。

## 14. Algorithm, Output, And Provenance Contract

脚本scripts/；执行数据/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R10_domain_member_atlas_20261030。保存全部16,384筛选表、冻结名单、主表、原新映射、逐成员投影/激活、真实高/普通/同ID低例、重采样及背景索引、绘图数据。研究库仅精选小证据与manifest，raw数组不入库。不覆盖旧结果。

## 15. Success / Failure / Insufficient Evidence

低频需比池富集才支持稀有承担；无富集削弱。特殊几何需匹配比较；相似削弱谱分离，缺覆盖则不足。固定词复现削弱纯身份，但不能证明语义功能；后缀变化只算关联。不得以数值失败为由调科学门槛。

## 16. What This Cannot Claim

领域专有知识、谱重合等于功能、因果必要性、完整h方差解释率、学习干扰/MoE收益、盲测泛化或纯identity。新前向仍需用户另外确认。

## 17. Block Confirmation, Freeze, And Amendment Ledger

A问题边界/B模型/C数据/D筛选/E频率谱/F上下文缺口/G交付范围均由当前详细用户指令明确给定。科学范围已授权；重采样/匹配/事件支持与标签是明确标注的操作实现。机器配置在结果前冻结；新增诊断须标附加描述，不得改主集合。数据/数值/识别三审计入Detailed；执行偏差追加记录，不回改冻结协议。

### Amendment A01: fine background reference

Active background reference follows [background_amendment_cn.md](background_amendment_cn.md); frozen v1 coarse draws are retained as method sensitivity. Post-v1 audit correction within authorized cache-only statistics; main feature selection and scientific thresholds unchanged,0new forwards. Precise machine revision in provenance/fine_background_config.json.
