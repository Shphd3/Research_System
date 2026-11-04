派生阅读副本；原件位置：`Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_27_natural_language_feature_response/subanchors/15_27_05_spectral_semantic_granularity_anchor_cn.md`。
[精确原始文件](../../../../../../../../sources/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_27_natural_language_feature_response/subanchors/15_27_05_spectral_semantic_granularity_anchor_cn.md)；研究修改仍回到原件。

---

# A15_27_05：谱位置与语义粒度

## 1. 问题定义

冻结Qwen3-0.6B-Base最后block27输出、最终归一化之前的表征后，等维大／中／小
方差谱段对领域和域内主题的可读性是否不同？中尾信息是否在谱头之外有增量？
原生A22哪些响应解释重构保留的部分？父A15_27连接可见文本与真实表征及字典响应。
R07已发现头尾均可读领域，R10发现decoder谱分布重合；它们没有说明每段具体分什么。
正结果支持具名任务的相对偏好；相反结果削弱粗细谱排序；覆盖不足限制本路径。
MoE应用和原生因果机制留在后续。

R13在同一主属下增加原生下一token恢复问题：依次加入按方差排序的方向，常见／格式预测是否更早接近原模型，能否超越词频／能量解释？这是获准的有限扩展，不是未知T5设置的复现。

## 2. 物理先验

语料方差、feature出现频率和当前响应强度是不同量。外部主题关系不必服从方差排序。
固定线性读出测可访问关联，不等于模型原生使用。主要竞争解释是词汇、来源／格式
和正则化造成表面粒度偏好；不把粗细谱结构写成先验事实。

R13先验：仅训练均值即可造成常见／格式输出偏置。原生最终归一化与固定输出头的敏感性不同于新训练读出的可读性。token ID语料频率、CrossCoder feature频率和语义粒度必须分开。

## 3. 可证伪假设

H1：匹配训练预算后，中尾相对谱头的优势在具名细任务中大于粗任务。竞争解释：
信息混合，或谱头同样容易读出细类。H2：加入等量中尾方向比谱头延长／随机新增
方向更改善原头部分类。竞争解释：无稳定增量或仅一般维数增益。H3：原始固定读出
在重构后保留判别分数，且成员系数可稳定描述它。竞争解释：残差承担重要分数，
或feature／文本解释不在新文档成立。三者分开裁定。

H4（R13）：固定原生输出头后，常见参考ID／格式预测可能在较小累积k时恢复。竞争解释为均值／输出头偏置、一般维数／能量恢复、词面与上下文难度；词频次序本身不建立语义次序。

## 4. 数学模型

每篇文档在预定常见token处的真实向量h是一条观测，标签只依据已读前文。
固定正交基V来自R04发现自然文本的共同中心化协方差，按特征值下降排序；它与
中心化表征矩阵的奇异值平方只差样本归一化。谱段坐标为
\(x_B=V_B^T(h-\mu)\)。标签是外部领域或主题。线性logistic读出以类别均衡的
经验对数损失和L2正则拟合，开发集选正则强度。平衡正确率是两个类别正确率的平均。
先比较同任务谱段差，再比较任务间差值，不以跨任务绝对正确率定义粒度。

共享z由14层共同编码。在原模型单位中，重构为
\(\widehat h=b+\sum_f z_f d_f\)，b包括decoder偏置及TRAIN中心、RMS还原。
残差\(e=h-\widehat h\)。固定线性分数精确满足
\(w^T h=w^T b+\sum_f z_f w^T d_f+w^T e\)。这是有符号加和账目，
不是因果或功能交互模型；不能把成员平方能量直接相加。

R13采用h_B=mu+Q Q^T(h−mu)，既有PC坐标选择器／旋转B须经Q=VB回到原生坐标；经原生RMSNorm与冻结W解码。真恒等直接使用h，全部PC重建另验。分别测真实后继NLL、KL、熵、首选／前十恢复和独立训练参考词频。

## 5. 计算实现

复用R11的192token自然文本和h27／共享z缓存。每篇在不看响应的情况下选择一个
后部常见token，以其可见前文核查标签。在继承的外部主题体系中，先检查发现集
标签／来源，再冻结数学和生物各两个子类。粗任务与条件细任务用同一选中文档，
保留原文档家族划分及新平台评估层。R11留出已在旧分析暴露；本轮是新方案冻结后
的探索性评估，不声称全新独立确认。

比较64维头／中／尾／随机、全空间，以及128维的头加谱段对照。训练集估计尺度，
并核查不标准化结果。固定原投影和读出评估重构、残差，残差另拟合读出单列。
发现集选成员与解释，按原生出现／幅值、独立DCLM发生率和有符号贡献统计；留出
检验文本假说和频率控制关系。旧A15_07研究Qwen3-8B层内增量，是方法先例，
对象与坐标不同，不代替本轮证据。

R13保留37篇R12/the评估文档，并加入输出无关抽样的175篇700自然位置。旧h未通过5090原生重放，因此只在同一官方权重／测点／固定文本上重缓存；原训练mu/V与所有条件／目标位置不变。21固定条件，无训练或分类器。精确合同在轮次Protocol。

## 6. 最小证伪检验

先检查全空间可读，再解释谱段无信号。设置机会／标签置换、等维、匹配训练预算、
来源／格式及文档家族留出对照。按文档分层重采样，比较配对差，报告多重比较。
区间下界正支持相应局部预测；精确非正差削弱预测；区间宽或资格失败则不足。
重构分别报告固定读出正确率、分数改变、残差分数和总体归一化平方误差。
实例不能替代总体覆盖与留出反例。

R13在解码前验证原生接口、同形状因果前文／缓存重放、真恒等与全PC。比较等64维谱段、等128维新增及三个正交随机新增，报告方差／能量与文档重采样。常见ID概率质量本身不等于恢复了正确语义。

## 7. 当前证据

R07受控数／生前16维正确率98.96%、尾16维90.62%、尾64维97.92%。R10的433／527
主成员decoder谱重合0.9493，特殊头偏未超过细匹配背景。R04／R07／R10复用同一
两域发现谱，不是独立谱复现。R09领域差的相对残差长度0.5368／0.7214，表明重构
可能遗漏重要区别。R11已保存450文档、原462前向；旧16名全部在物理留出激活。
这些是动机，不是本轮答案。R12初始版本记录NOT RUN；当前已完成96篇同token文档（D39／V20／H37），各任务拟合D16／V8，细任务H17／18。粗任务头／中／尾平衡正确率94.7／62.3／51.3%，数学细任务81.9／57.6／58.3%，生物细任务88.9／88.9／77.8%。细减粗交互未过Holm4；中尾新增没有超过128维对照的已确认增益。重构保留固定平均判别分数差82.1／79.6／81.2%，残差另读76.3／75.7／88.9%。细类严格来源／文体／位置匹配仅1／3对，旧H已暴露。因此粗细谱排序未建立，残差遗漏仍重要；这些是有界AI解释，非研究者科学接受。

完整事实由[R12 Summary](../../../../experiments/A15/15_27_natural_language_feature_response/R12_spectral_semantic_granularity_20261031/summary_cn.md)和[Detailed](../../../../../../../../UNAVAILABLE.md)拥有。前置证据仍分别归[R07](../../../../../../../../UNAVAILABLE.md)、[R10](../../../../../../../../UNAVAILABLE.md)、[R09](../../../../../../../../UNAVAILABLE.md)和[R11 A02](../../../../../../../../UNAVAILABLE.md)。

R13完成737位置／180物理文档、21固定条件，无训练。新缓存重放／因果NLL及全PC恒等误差为0。自然面板头64 NLL5.901→前256维3.914→全维2.342；非格式常见／其他ID首选在64维恢复30.3%／2.0%。仅均值已有55.5%空白标点概率。加中／尾改善0.427／0.151nat，继续加前部64改善0.924；中部没有稳定超过随机新增。固定真实文本存在具体上下文候选及准确性／保真反转。它们是探索性输出／频率观察，粗细语义与机制仍Unknown。

2026-11-02，研究者授权补充PC1／PC2单独及前8／16维，原生头与原面板不变，只有PC2／前8维新计算。自然面板恢复率：k1:common2.15%,format10.49%,other0.00%; pc2:common6.95%,format3.70%,other0.00%; k8:common9.46%,format27.57%,other0.00%; k16:common14.37%,format26.13%,other0.00%. 常见组实际含数字、子词与$／=，不等于完整词或语义粒度。 [supplement](../../../../../../../../UNAVAILABLE.md)

2026-11-02补充完成：独立谱段与尾部原生解码，700自然位置、11段；固定12例的全文前文、当前token ID及0/1基位置已给出。同token异文档系数对照312位置/158篇。 b16_32 NLL9.139; b32_64 NLL9.299; b64_128 NLL8.956; b128_256 NLL8.662; b256_512 NLL8.037; b512_768 NLL8.769; b768_960 NLL9.416; b960_1025 NLL10.203. 原生头单独输出是否贴切、真实后继概率和语境关联分别解释；不将孤立子空间失败直接称为模型储存随机噪声。 [result](../../../../../../../../UNAVAILABLE.md)

## 8. 结论边界与下一决策

限于已暴露英文前文、当前权重／接口及参考谱，R12的可读性与R13的固定原生输出干预。它们不建立知识本体、由粗到细语义层级、feature因果机制、训练动态或MoE收益。执行完成不等于科学接受；研究者机制判断和闭题仍Unknown。

唯一AI建议：做一组词频匹配、同token前文的对象／关系最小对照。该建议没有授权本轮继续新层／新分类器／新语义实验；R12证据和旧建议保留在其结果记录。

[R13原生轮次扩展](../../../../experiments/A15/15_27_natural_language_feature_response/R13_20261101_native_spectral_decoding/anchor_cn.md) · [协议](../../../../experiments/A15/15_27_natural_language_feature_response/R13_20261101_native_spectral_decoding/protocol_cn.md) · [完整测量与原始阅读](../../../../experiments/A15/15_27_natural_language_feature_response/R13_20261101_native_spectral_decoding/summary_cn.md)。2026-11-01完成；R12保留。


R14 authorized 1102 round: [task-bound concept specificity](../../../../experiments/A15/15_27_natural_language_feature_response/R14_20261102_concept_specificity_v1/anchor.md), [protocol](../../../../experiments/A15/15_27_natural_language_feature_response/R14_20261102_concept_specificity_v1/protocol.md). Frequency-group deletion is primary; full spectral matrix secondary. Initial state NOT RUN; scientific acceptance Unknown.


### 2026-11-02 R14认识更新（有边界的AI解释）

研究者将“频率组在具体概念任务中的贡献和较难替代性”固定为主要问题，谱条件全部保留但作为次要联系。实际完成48家族、288前缀、36评估家族（每域12）、167独立条件和19别名；无新模型、字典或分类器训练。原生完整候选评分与旧读出、外部定义线索是三层不同证据。

完整线索分数1.539，删低／中／高为1.558／1.441／1.152。高频超过同人数控制0.358，但六主比较同时区间[-0.031,0.778]；超过范数匹配0.161，95%[-0.172,0.499]。尚未建立频率分工或哪组更难替代。完整模型具体102/144、双侧31/72；高频删组也损伤上位204/216→173/216和整体输出。固定核糖体／溶酶体反例表明，候选偏好移动可造成新错，而线索分数同时上升；不能把分数与正确性混同。重建分数0.956不是信息保留率。

数据1.3按文字审核修正20显名上位前缀，旧版全部保留；80分支、166位置重算，2474位置h/z及未改分数逐值一致。修正改变同人数比较的局部同时区间判断；范数匹配两版均未建立。另纠正全零成员被叫作高响应反例，原规则找不到时记未找到。最终用现有CPU两线程，GPU0，未占H100，模型与测点未变。科研接受和关闭Unknown。

唯一后续（AI建议，未执行）：整体预测损伤匹配后，高频组是否仍额外损伤具体线索区分？不因本轮完成自动启动新实验。完整证据：[Summary](../../../../experiments/A15/15_27_natural_language_feature_response/R14_20261102_concept_specificity_v1/summary_cn.md)、[报告](../../../../experiments/A15/15_27_natural_language_feature_response/R14_20261102_concept_specificity_v1/report_cn.md)、[原始数据与代码](../../../../experiments/A15/15_27_natural_language_feature_response/R14_20261102_concept_specificity_v1/reproduce.md)。


2026-11-02研究者授权R15自然文本语言现象与表征／输出头谱分析：[新轮Anchor](../../../../experiments/A15/15_27_natural_language_feature_response/R15_20261102_natural_phenomena_output_geometry_v1/anchor.md)、[协议](../../../../experiments/A15/15_27_natural_language_feature_response/R15_20261102_natural_phenomena_output_geometry_v1/protocol.md)。先发现与开发、冻结解释后独立验证；旧数学生物谱只作历史参照，不预设粗细。当前数据与协议已冻结，结果NOT_RUN；科学接受Unknown。


### R15 completed bounded natural-text update (2026-11-02)

600真实网页、557网站，300发现/150开发/150验证，76800位置；新h/y谱各自拟合，旧60数学生物谱只作历史参照。128项能量主比较0通过，4项成员候选0通过；未触发确认干预。补齐有符号方向A6发生在主表之后，明确只探索：空行和数字等关联共享谱头方向，最稳候选为空行→零基2方向负移(−0.249发现SD；146篇1029对)，位置／数字共现限制仍同向；不是新确认或功能分工。空行实际变化单位输出增益1.0057×各向同性参照，未建立强选择放大。源是网页技术词候选组，不是学科金标，也不证明底模／字典训练未见。

[R15认识更新](../../../../experiments/A15/15_27_natural_language_feature_response/R15_20261102_natural_phenomena_output_geometry_v1/summary_cn.md)、[完整报告](../../../../experiments/A15/15_27_natural_language_feature_response/R15_20261102_natural_phenomena_output_geometry_v1/report_cn.md)、[冻结协议及修订](../../../../experiments/A15/15_27_natural_language_feature_response/R15_20261102_natural_phenomena_output_geometry_v1/protocol.md)、[实际资格](../../../../experiments/A15/15_27_natural_language_feature_response/R15_20261102_natural_phenomena_output_geometry_v1/detailed_cn.md)、[原始数据与代码](../../../../experiments/A15/15_27_natural_language_feature_response/R15_20261102_natural_phenomena_output_geometry_v1/reproduce.md)。唯一后续为前置冻结空行有符号指标并在新文本复核，区分可转移关联与本轮探索适配；AI建议，未执行。实际CPU两线程，GPU0，无训练；科研接受与闭题Unknown。旧轮次保留，不将本结果用作MoE、Dense动态或幅值／有无机制证明。


2026-11-02 R16逐层单层头64干预已完成：[完整观察](../../../../experiments/A15/15_27_natural_language_feature_response/R16_20261102_layerwise_head64_intervention/summary_cn.md)。同60篇训练侧文本分别拟合28层谱，复用700自然/37the位置，两种范围分开；第1/7/14/21/28层全前缀保持21.00/15.86/16.00/27.29/23.00%，仅目标77.43/78.00/74.71/41.00/23.00%。范围差异明显，全前缀随深度非单调。737原表征/损失精确重放，旧谱首选全同，并列排序修复不改概率或词类。早层保持不能排除后续补偿，同维随机未匹配能量；不推导层的独立重要性或语义层级。科学接受与闭题Unknown。


2026-11-04 R16删除头64补充已完成：[完整结果](../../../../experiments/A15/15_27_natural_language_feature_response/R16_20261102_layerwise_head64_intervention/supplements/20261104_delete_head64_keep960/summary_cn.md)。同模型、文本、28套PCA，无训练或重拟合。前中层保留头64更能保持原预测，后部保留后960更好；最后层其余非格式ID保持2.0%/27.6%。两种操作都不能替代完整原生状态，常见/具体不是排他分区；维数/能量/上下文和后续计算仍为边界。认识为AI有边界解释，研究者接受与闭题Unknown。


### 2026-11-04 等维谱段与均值对照完成

[结果](../../../../../../../../UNAVAILABLE.md)：16段各64方向、28层、两个干预范围。加均值时头64在所有层均达到最高保持率；当前范围第1/14/25/28层加/不加为77.43/17.71%、74.71/40.71%、34.29/12.71%、23.00/4.29%。其余非格式最后层2.00→5.07%，但NLL变差。后960整体优势不等于某等维后段优势，能量和共同基线仍是竞争解释。5篇辅助数值修复后737旧对照精确一致，主面板统计不变。AI有边界解读；科学接受、语义粒度、补偿机制与闭题Unknown。
