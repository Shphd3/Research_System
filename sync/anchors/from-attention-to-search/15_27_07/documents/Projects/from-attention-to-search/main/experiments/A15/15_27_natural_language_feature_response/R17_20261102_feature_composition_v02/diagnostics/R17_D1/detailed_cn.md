派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/detailed_cn.md`。
[精确原始文件](../../../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/detailed_cn.md)；研究修改仍回到原件。

---

# R17_D1详细记录

[Summary](summary_cn.md) · [Protocol](protocol_cn.md) · [修正](corrections_cn.md) · [案例](casebook_cn.md)

## 目的与识别范围

原四假设保持。所有结果是静态对应或可读性：逻辑probe是另训读出，不证明底模使用该成员；重建与残差各自可读不能等同信息被删除；频率是参考语料激活频率，不是语义频率或训练暴露。人工式文本审核由当前Codex处理agent执行，未作独立人工确认。用户明确要求本轮同时给AI判定和认识更新，故不等待另一轮解读批准；研究者的接受、机制判断、下一决策不因此改变。

## 对象、数据与计算

Qwen3-0.6B Base官方冻结版本，28块、宽1024。ATTN在block27 self_attn.o_proj实际输出，MLPIN在同块mlp前hook、post_attention_layernorm之后。两SAE均FP32线性编码→ReLU→正值Top32，30000坐标，无输入单位范数化或decoder bias减法。原表示h、重建b+zD、残差h−重建都保留；用u_i=z_i乘该hook decoder范数报告加权响应。A22按保存的FP64均值/RMS归一化后FP32编码、保存阈值0.051281172782182693作用于ReLU值×联合decoder范数；最后层重建单独反归一化，不能把联合z叫作仅最后层输入的SAE。

A17训练raw=1000980480，prediction-valid=1000002960，SAEeligible=999025471；E16 raw=1000001536，累计过滤后精确数未记录；A22累计位置999997440，包含A21的4096000。计数对象不同，不混叫相同精确1B。三个asset_identity.json保存路径、SHA、配置、hook与训练记录。权重本轮均已实际加载，旧资产记录的历史Unknown不代替本轮装载证据。

旧384：48家族，24/12/12家族，6/3/3定理组。更正对象框架和n绑定，答案有无只替换答案句与中性句。旧留出只作diagnostic_old；corrected_old与original_old全384均前向。新288主面板含24家族×2细类×2答案条件×2改写=192，以及48粗方阵和48非矩阵；粗类无可逆性标签。n52–75，配对同n。新定理暴露分为旧发现6组、旧开发3组、未见3组，原始逐例和条件分层表均交付。不能把24新实例家族全部叫24新定理。

附表48只在12组第一家族、无答案p0各两细类，分别替换array框架或逻辑否定。同一冻结模型评分，不重新拟合。对应main基线每24条；例如CC联合小集合main LL0.0906→array3.1615、否定3.6540，ATTN0.6906→0.7023/0.6986，MLPIN0.6554→0.8153/0.7734。该24条子集不是96条无答案总体；不以总体作其配对基线。

自然600文档来自原R15固定数据，文档划分300/150/150，每篇固定128可见位置，共76800。频率只从发现38400位置估计，各字典分别正激活计数；至少20位置、5文档才可分频组。按正计数两个整数三分位边界、同计数不拆分。缓存一遍底模同时捕获三个对象，原数据文档/位置身份一致，但不是全研究未见语料，且与A22训练源潜在重叠。

## 候选、读出与统计

H1共同C按三矩阵条件相对非矩阵的最小发现标准化差选最多8，F按发现细标签差选最多8；A=F−C。旧发现冻结，不用新测试重排。记录C16/32交集、实际off→on/on→on/on→off/off→off。新增成员是零→正而非任何增幅。匹配随机按频率/覆盖等冻结条件20seed11021..11040，每个随机模型独立拟合，聚合的loss为20模型loss均值，不是平均概率的loss。

H2定义b为是否激活，r为C加权响应L2范数，q=u/(r+1e−12)；比较[b,r]和[q,b,r]，并保留相同支持的成对例。统计控制总幅值，不是逐样本等范数硬匹配；相对强弱仍可能携带非线性混杂。各改写分别给表，保留same-support条件变化后的样本N。

H3按冻结频率组与发现细类排名，固定成员预算K16、不足降12/8；本轮各集合实际数在selected_arms_frozen.json，不复制坐标补数。J由高与中低拼接，与纯H、纯M等预算比较，必须两项正收益同时成立。另保留中、低、范数化、协变量和随机敏感性。

H4只在旧发现做一次有限搜索：最多8高频候选、20对、80状态配置；自然发现正值q75分弱／强、零独立。两边际状态≥.01、联合≤.005、至少30位置和10文档筛选。SAE各只有1合格发现候选，第一为主；CC10，余9探索。验证文档bootstrap2000；原子常见与指定状态常见分别列，不能混淆。语义匹配控制同域、位置四分位、上下文比0.5–2，不跨命中/对照文档复用。ATTN6命中文档全部匹配失败，MLPIN37对成功；两SAE的随机配置池都20/20失败，不编造匹配增量。冻结配置非空的加性与配置probe已实际拟合。旧版表对未知的处理保留历史，新v4对应表区分检测比例和可判定配对，不用零区间证明无语义。

L2逻辑回归CPU拟合，lbfgs最多5000，class_weight balanced；旧发现fit scaler，五C=.01,.1,1,10,100用开发LL选择，平局小C。原混合开发方案先定位；修正H1-H4统一混合旧发现训练、无答案旧开发选C。三核心方案均对连续/二值/高频16运行。ATTN与MLPIN的旧全h优于小集合，启用一次描述选择及K16/32/64和20随机对照；CC旧小集合已经较好，门槛未触发。所有门槛、排名和随机成员先于新响应冻结，不在新测试拟合温度或非线性模型。

家族bootstrap2000、定理组敏感性，随机种子20261103，协议组内Bonferroni。H1组5、H2组1、H3组2、H4主配置组2；跨位置前五同含义增量组成m5直接差。H4若无可接受匹配配置，仅加性差可估，不能把缺对照当支持。逐答案条件和逐改写是明确标识的条件诊断，不扩大成独立确认；定理仅12组，置信区间有精度限制。所有逐例loss、Brier、margin、五箱可靠性N、系数/scaler均保存。

## 原生行为和位置诊断

原生使用完整候选“ invertible.”(3tokens)与“ singular.”(2tokens)的总序列logprob，两种预先固定格式；不作长度/先验校正，单独给无内容先验。若展示概率，是两候选内归一化，不是全词表正确token概率。续写直接答案控制2/2；问答只1/2，通过奇异、可逆失败。新无答案续写73/96、问答50/96，说明外壳／候选偏置是竞争解释。不得因原生失败宣布知识不存在，也不得因成功证明SAE坐标因果使用。

只检查一次问答前缀末token，原旧训练/开发重新拟合各位置h/reconstruction/residual/原冻结小集合，成员不重选。无答案h在ATTN79/96 LL0.5071，MLPIN76/96 LL0.5203；重建60/96 LL0.6541和59/96 LL0.7443。小集合48/96 LL0.7467和54/96 LL0.6798。这是context+position联合变化，不能把提升唯一归因末token位置。与原Summary中的pre-answer摘要后缀位置分开列。

## 精度与执行记录

唯一pt-viic7g4p，2×5090 spot，平台创建02:11:23UTC、完成02:30:02UTC。第一SDK请求被service_time_expression字段拒绝且未建job；D1本地兼容代理过滤该字段后一次有效提交，未修改共享脚本。复用已存在torch2.8cu128运行时，无依赖安装，无底模／字典梯度。CPU/GPU no-op和同物理shape单例/批次h差为0，账本误差<1e−6。主面板8×128、自然2×512、precision8×64、原生4×192，真实长度与padding保留，不截断长例。原模型保存BF16提升FP32并不能恢复已丢失的训练精度。

24旧精度例：ATTN/MLPIN/CC h相对L2差约.01737/.01434/.01402，z相对差.06368/.03652/.05196；支持翻转36/32/147。固定旧probe连续联合阈值分类均0翻转，但最大概率差.199/.312/.272；二值MLPIN2/24、CC1/24翻转。故不以大绝对差宣布语义bug，也不声称dtype无关。主结果、自然频率、前向和读出一致FP32，BF16旧参照单列。

## H4内容、规则和覆盖的定位

旧49盲例由当前agent逐条阅读：39non_target、10undetermined，无fine。新ATTN6例均non_target，MLPIN40例39non_target、1undetermined。不是独立盲审，也不是人工研究者确认。规则已知20控制从9/20→20/20，但不是总体召回估计。所有旧CC参照、两SAE及其before、校正CC共7根重新标注；pre_v4保留原件。

600源文档按source_line取回，首次误按1基全部SHA失败，改0基后600/600精确匹配，失败载荷保留。完整篇标签544非目标、52未知、4粗未知，自动细标签0；完整篇与当前可见前缀分开，不以未来内容补当前标签。一次最多10万源行的合法本地检索产生48独立自然文档可见窗口，限定首次细词前128起、最多512token，在最后可见位置捕获冻结坐标；搜索词标签不是ground truth。v4有2可逆、0奇异、43未知、2粗未知、1非目标。每配置对各标签的原始命中z和事件均交付，不并回原R15估计频率，不因零命中否定机制，不在新命中重新命名海鲜／书目等为新概念。

## 图与读法

1. [文本×坐标热图](../../../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/figures/01_text_member_heatmaps.png)：固定D1_M05_0、n62、p0的完整文本与各字典C/F raw z；每面板独立色标，不比较不同字典颜色幅度。共同响应在粗类与两细类复用，但细类响应不等于语义嵌套。
2. [二坐标散点](../../../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/figures/02_frozen_pair_scatter.png)：原子对旧发现冻结，颜色为可逆/奇异、点形为答案条件及改写，箭头p0→p1。192行、24家族、12定理，零值重合保留；不能挑测试最分离坐标。
3. [表示定位](../../../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/figures/03_representation_localization.png)：无答案96条LL，旁列正确数；NMSE为残差平方能量/原h平方能量。不同目标分别解释，低NMSE不证明细类信号保留。
4. [固定例置信度](../../../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/figures/04_fixed_case_confidence.png)：连续/二值probe与原生两候选概率分栏；固定1家族1定理4例，CC二值对可逆例0.001928，是实测高置信反例。
5. [hook概览](../../../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/figures/05_hook_locations.png)：明确o_proj输出、残差相加、RMSNorm、MLP输入与CC block输出。

## 证据与状态

八格SAE和四格校正CC的规定计算均实际完成。依赖失败有实际数量，统计不足不冒充没运行，没合格对照不冒充有效估计。全[模块台账](../../../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/tables/coverage_ledger.csv)、[原始表索引](dataset_guide.md)、[数值核验](verification.md)可追溯。三项独立审计见执行evidence/audit_identification.md、audit_statistics.md、audit_implementation.md。科学接受、机制归因与问题关闭Unknown；没有commit/push、外部发布或持续监控。


### 最终断点核对：有响应、有效对照与输出语境

H4的原始配置事件计数进一步定位了问题。MLPIN主配置11234强+47强在旧发现、开发、旧诊断和新细标签中均为0次；它的20个随机配置又与主配置在面板上有完全相同的指示值，因此全部IDENTICAL_INDICATOR_FAILED。ATTN没有合格距离匹配池，20次均MATCH_FAILED；新无答案中主配置只在可逆48条的2条、奇异48条的2条出现。这里分别卡在当前配置的内容响应、可区分的对照，以及自然语料目标覆盖，不能把0增量解释为没有组合机制。没有因此重选配置。

描述专用K曲线并非全部毫无变化。ATTN K16/32/64无答案LL为0.6840/0.6716/0.6854，K32比原联合0.7064更好、58/96正确，但其相对匹配随机收益0.02203、定理组同时区间[−0.00539,0.04949]仍不足。ATTN K64随机匹配0/20成功，故没有匹配增量估计；K16/32各20/20。MLPIN三个K均20/20，LL0.8213/0.8245/0.7433，未优于原联合0.7034。有限选择可以改变结果，尚未给稳定或单调的结构结论。

问答位置诊断中的“无答案”指正文未直接给出正确答案。追加问句同时包含invertible和singular两个选项词，但不揭示哪个正确；它不是“整个可见前缀不含选项词”的重现。这进一步限制了跨语境迁移的解释。

[H4逐条件事件数](../../../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/tables/H4_semantic_panel_event_counts.csv) · [K匹配成功数](../../../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/tables/optional_K_matching_status.csv) · [K条件效应](../../../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/tables/optional_K_conditioned_effects.csv)。这些表从冻结缓存/预测读取，没有新前向、重选、拟合或额外搜索。
