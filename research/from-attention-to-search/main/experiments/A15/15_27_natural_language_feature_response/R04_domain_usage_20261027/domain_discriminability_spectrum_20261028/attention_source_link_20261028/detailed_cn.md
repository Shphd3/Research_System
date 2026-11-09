# 完整解释、数值与边界

三条分析路径：行为与因素对照沿用原R05观察分组，本轮不补测输出行为；表征与组织连接固定方向几何和实际前文端使用；功能干预未运行，实现质量由独立核验负责。

## 1. 同一个feature的“在哪里”与“何时使用”

一个feature是固定字典坐标。SAE f11667不等于CC f11667。谱位置问的是：它一旦激活，decoder向量朝原空间的哪些方向重构？使用问的是：哪些真实token处z>0、激活时贡献多少？输入同为真实数学/生物文本，模型和原生稀疏接口不变。

SAE E16为block27的MLP输入（模型原生post-attention RMSNorm之后），30000坐标、原生ReLU/Top32，分解此单层输入。没有额外逐维标准化。CrossCoder A22把blocks1,3,…27的14路residual-post按训练RMS归一，再经各路encoder求和形成共享z，16384坐标、原生推理阈值0.051281172782182693；训练BatchTopK平均256不是本轮每token强制Top256。最后层贡献为共享z × TRAIN_RMS27(374.3495121) × 最后层decoder范数。它重构多层目标，不是最后层独立编码激活；last decoder几何使用block27 residual-post原空间。两种hook、归一化和训练目标不同，不能把原始谱比例差解释为语义多少。

方向投影定义：p(i,b)=sum_{j属于谱段b}(单位decoder_i 与PC_j内积)^2。完整1024正交基、16段×64，逐成员总和1。这里没有乘z、特征值或奇异值。本轮只读取旧基和旧投影，不重新PCA。发现集9600×1024（数学/生物各30篇，每篇160tokens，合并均值中心化、文档/领域等权）固定坐标；已有开发/留出只投影。真实表征方差说的是token表征云沿各方向散布多少；两域均值差说的是两个域平均表征的差向量落在哪里；它们均不等于某feature被用多强。[旧原始谱表](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R04_domain_usage_20261027/domain_discriminability_spectrum_20261028/attention_source_link_20261028/sources/real_variance_and_domain_mean_difference.csv)

## 2. 固定名单、交集和谱定位

[名单](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R04_domain_usage_20261027/domain_discriminability_spectrum_20261028/attention_source_link_20261028/members_cn.md)先列全部定义；[成员CSV](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R04_domain_usage_20261027/domain_discriminability_spectrum_20261028/attention_source_link_20261028/tables/frozen_members.csv)、[交集CSV](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R04_domain_usage_20261027/domain_discriminability_spectrum_20261028/attention_source_link_20261028/tables/set_intersections.csv)是完整可查版本。Top16仅按旧发现区分排序，数学9/生物7；扩展方向各64；原R04共有32、数学16、生物16保持旧角色。R05候选SAE20/CC25，R06合格对象每套26，折叠后SAE25/CC26坐标。Top16及扩展两方向与R06合格坐标交集均0，不能把它们混成已验证词义组。

头段（前64PC）集合几何如下；百分比是方向长度平方占比，不是贡献或方差解释：

|dictionary|set|n_members|projection|background_low|background_median|background_high|offset_from_background_median|
|---|---|---|---|---|---|---|---|
|SAE|top16_math|9|50.75%|30.19%|39.31%|46.07%|11.44%|
|SAE|top16_bio|7|51.80%|29.50%|41.10%|51.14%|10.70%|
|CC|top16_math|9|23.29%|6.21%|8.28%|12.94%|15.00%|
|CC|top16_bio|7|21.34%|7.27%|10.11%|16.05%|11.22%|

背景为同字典、同数量、相近DCLM参考频率和发现文档支持的1000随机集合。旧完整集合复用旧抽样；新的9/7方向子集沿同一联合分箱规则单独抽样，排除整个Top16，无替换、不保留候选充数。每feature背景分箱floor(log2(DCLM命中+.5))×floor(两域发现文档支持总数/5)，失败不放宽。灰带是有限匹配背景的点对点范围，不是因果空模型，也不重现整个筛选过程。各字典对自己的背景偏移，才是可比描述。缺乏足够匹配的完整集合如下，保持NA：

|dictionary|set|status|
|---|---|---|
|SAE|expanded_math64|NA_INSUFFICIENT_MATCH_POOL|
|SAE|expanded_bio64|NA_INSUFFICIENT_MATCH_POOL|
|SAE|old_shared32|NA_INSUFFICIENT_MATCH_POOL|
|SAE|old_math16|NA_INSUFFICIENT_MATCH_POOL|
|SAE|old_bio16|NA_INSUFFICIENT_MATCH_POOL|
|CC|expanded_bio64|NA_INSUFFICIENT_MATCH_POOL|
|CC|old_shared32|NA_INSUFFICIENT_MATCH_POOL|
|CC|old_bio16|NA_INSUFFICIENT_MATCH_POOL|

[全部冻结成员16段数值](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R04_domain_usage_20261027/domain_discriminability_spectrum_20261028/attention_source_link_20261028/tables/all_frozen_member_spectrum.csv) · [全部集合和匹配状态](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R04_domain_usage_20261027/domain_discriminability_spectrum_20261028/attention_source_link_20261028/tables/set_spectrum_and_background.csv)。扩展/原角色不混为同一集合，没有按本轮结果改名单。

## 3. 原Attention配对怎样测使用

原40留出文档，数学/生物各20，320个query；block27全16heads。沿用bin0近1–32及bin4远129–160，同(query,head)在两档都有效的交集4842/5120，保留40文档和320query，丢278单元。主分层为异tokenID且原规则非标点；原“非标点”含空白，现明确标出。同ID的近远共同支持0文档，保持不可估；不声称排除词面。每档高组是档内最高约10%，中等组来自40–60百分位；沿用同ID/标点状态、距离caliper8匹配，不重选位置。

每个feature、每位置定义：出现I(z>0)，原贡献c=z×原尺度decoder范数，含零贡献c。沿位置→head→query逐级等权后得每文档出现率p和含零均值m。每文档激活时贡献=m/p；p=0时NA。条件强度在有定义文档内平均，不能用0代替NA。m=p×条件贡献只对同一个文档/feature成立，跨文档或跨feature均值不能简单相乘。每成员原尺度保留；集合主图先除以该成员旧发现贡献RMS再成员等权，避免少数原幅度大坐标直接支配；原尺度集合、成员、条件强度均另存。[逐成员三量及尺度](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R04_domain_usage_20261027/domain_discriminability_spectrum_20261028/attention_source_link_20261028/tables/member_usage.csv) · [逐文档集合值](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R04_domain_usage_20261027/domain_discriminability_spectrum_20261028/attention_source_link_20261028/tables/set_document_values.csv)

5000次文档配对bootstrap、种子2026102807；先按文档算近远差再重采样，不把token当独立样本。Top16两方向×两文档域×两字典×三个对比=24项主检验，仅针对RMS标准化含零贡献；19999次对称性假设下文档符号翻转，统一BH24。条件强度可能只有部分文档有定义，少于10文档不报告可用区间。8个差中差为：

|dictionary|domain|set|mean|low|high|BH24_q|
|---|---|---|---|---|---|---|
|SAE|math|top16_math|-0.0089|-0.0449|0.0272|0.8651|
|SAE|math|top16_bio|0.0099|-0.0094|0.0320|0.8108|
|SAE|biology|top16_math|0.0038|-0.0111|0.0179|0.8651|
|SAE|biology|top16_bio|0.0133|-0.0236|0.0519|0.8108|
|CC|math|top16_math|-0.0088|-0.0788|0.0605|0.9282|
|CC|math|top16_bio|-0.0077|-0.0195|0.0014|0.5908|
|CC|biology|top16_math|-0.0011|-0.0063|0.0031|0.9180|
|CC|biology|top16_bio|0.0444|-0.0159|0.1044|0.5791|

不能用高组显著、中组不显著断言两者不同。主要的24比较均未过校正；本批没有确认统一远高增强，区间宽时仍记证据不足。各个成员也不同：数学SAE f11667高组原贡献11.158→12.338，但同组f693标准化高组差−0.375；f11667差中差−0.071[-0.214,0.058]。数学SAE主集合8/9成员高组均值下降，13/20文档下降；f693占成员绝对变化总和32.2%，因此不能把平均下降推广成每成员/每文档一致。

保留辅助正线索：CC生物7成员的高组出现18.35%→17.10%、中等19.54%→16.16%，相减后+2.13个百分点[1.06,3.29]；原贡献差中差+0.388[0.063,0.753]，而固定发现RMS标准化差中差+0.044[-0.016,0.104]。CC扩展生物64差中差+0.0305[0.0019,0.0600]，44/64成员方向为正，但仅12/20文档为正；最大单成员占绝对变化8.44%，不是单一成员垄断。它们是未做主校正的探索性读数，尺度和集合不同，不用来替代冻结Top16主结果。远高本身仍为下降点估计，正差中差主要来自中等对照更大下降。[所有集合/指标/差值](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R04_domain_usage_20261027/domain_discriminability_spectrum_20261028/attention_source_link_20261028/tables/set_contrasts.csv) · [逐成员差值](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R04_domain_usage_20261027/domain_discriminability_spectrum_20261028/attention_source_link_20261028/tables/member_contrasts.csv) · [成员/文档影响诊断](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R04_domain_usage_20261027/domain_discriminability_spectrum_20261028/attention_source_link_20261028/tables/member_document_influence.csv)

## 4. 所有活跃坐标的频率组成

这一项复用前文端完整组成，分母是每个来源位置全部z>0坐标，不要求query也激活，也不限定任何候选。主量为每位置低频占比，随后同层级等权；不以合并所有坐标后的比例替代。四类为低/中/高/参考低支持；DCLM共65536参考位置、同模型/原生字典与阈值，命中<20单列。SAE低频上限0.0595093%、中频上限0.123596%；CC低频上限0.259399%、中频上限1.344299%。这些仅是两套字典各自既有DCLM参考分组，不是普遍频率，也不等于PC排行。

低频占比近高→远高：SAE数学7.849%→7.537%，生物9.985%→8.500%；CC数学1.917%→2.056%，生物2.949%→2.904%。CC数学低频数量5.958→6.198，全部活跃307.156→294.660；SAE生物低频数量3.195→2.720，活跃总数32恒定。不同字典的占比、分母和编码接口不同，不能直接排语义价值。原96项校正中，所有低频占比差中差均未过；SAE生物原高组下降区间不含0也不能代替高/中直接比较。[完整四频段/数量/分母](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R04_domain_usage_20261027/domain_discriminability_spectrum_20261028/attention_source_link_20261028/tables/all_active_frequency_composition.csv) · [原对比及原校正](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R04_domain_usage_20261027/domain_discriminability_spectrum_20261028/attention_source_link_20261028/tables/all_active_frequency_contrasts.csv)

## 5. 远高实际上是什么token？

全量导出55,138条合格近远事件，包含全部原分层与中等配对；不是只导出手选例子。其中远高共15,936事件，来自1,872个不同文档×来源位置；同一来源可被多个query/head选中，事件不独立。主共同支持的远高14,055事件，1,686个不同文档×来源位置。实际tokenizer片段、解码片段、合并词显示、完整query可见前缀、源句在可见范围内的部分、query、block27/head、精确距离和原Attention均保存。句子在缓存窗口或query处截断会显式标志，不用未来文字解释当前响应。[全量事件CSV.gz](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R04_domain_usage_20261027/domain_discriminability_spectrum_20261028/attention_source_link_20261028/tables/all_near_far_source_events.csv.gz) · [可见上下文](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R04_domain_usage_20261027/domain_discriminability_spectrum_20261028/attention_source_link_20261028/analysis/query_visible_contexts.json) · [全部源端活跃坐标CSV.gz](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R04_domain_usage_20261027/domain_discriminability_spectrum_20261028/attention_source_link_20261028/tables/all_source_active_features.csv.gz)

词形规则逐条覆盖：纯空白→空白；纯符号→标点/符号；数字；固定术语词表或缩写→术语/实体候选；固定代词/指示词表→照应候选；功能/结构词表；剩余字母词为普通内容词候选；无法判定为未知。词表在analyze.py固定，同流程标全部四组。语义作用另列，代词并未验证指向谁，术语词表未覆盖不等于不是术语；没有可靠人工语义/词性真值，本轮相应验证覆盖为0，不能把规则类别当真实语义比例。

在主共同支持中按文档/层级等权，远高数学：普通内容词候选44.75%、结构词38.16%、术语/实体候选4.57%、代词/指示词5.35%、空白3.02%；生物对应45.94%、34.36%、7.04%、6.38%、1.96%。余下为数字/混合，完整分布含近高和中等对照及区间。[全覆盖量](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R04_domain_usage_20261027/domain_discriminability_spectrum_20261028/attention_source_link_20261028/tables/token_category_coverage.csv) · [文档级类别比例](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R04_domain_usage_20261027/domain_discriminability_spectrum_20261028/attention_source_link_20261028/tables/token_categories_document_weighted.csv)。这些是规则诊断，不推断模型沿边传递该语义。

位置/绝对Attention混杂不可忽略。远高源位置均值数学32.89、生物32.92，近高170.27/169.11；44.76%/44.49%远高在位置32之前，超出原谱/领域评分32:192窗口，近高0%。近高Attention平均数学0.01611、生物0.01721，远高0.005265/0.007701；这些是原概率，没有跨档重新归一。平均距离近高5.93/6.18，远高143.32/142.37；中等对照的近距均值约10.4，配对距离caliper仍有余差。它们限制距离解释，不改原分析分母。[位置与概率诊断](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R04_domain_usage_20261027/domain_discriminability_spectrum_20261028/attention_source_link_20261028/tables/position_attention_diagnostics.csv)

## 6. 真实例子、竞争解释与缺项

四个固定案例和每个激活坐标详见[图4与读法](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R04_domain_usage_20261027/domain_discriminability_spectrum_20261028/attention_source_link_20261028/figures_cn.md)及[cases.json](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R04_domain_usage_20261027/domain_discriminability_spectrum_20261028/attention_source_link_20261028/analysis/cases.json)。数学“nodes”可能指图节点，生物“species”可能指研究中的物种，换行可能分隔标题和正文；这些是文本角色的候选描述。query“matching”到“nodes”的档内高边原Attention仅0.000197，本身展示“高”不等于绝对大。f11667在“nodes”贡献8.704，CC生物方向f652同时出现；“species”处SAE Top16全不命中、原R04生物角色仍命中，说明新排序不覆盖所有领域响应。换行和“exacerbated”反例均保留。

当前可观察到固定方向的几何偏移和具体前文端的使用，但还不能把它们归因于语义传递。词面/术语、文档来源、标题段落位置、早期窗口、档内高组绝对概率不同、原接口和强度尺度均未完全控制。无独立语义角色标签、同ID配对支持不足、部分随机组匹配不足、无法补齐缓存之外的完整句子，均如实标缺。没有新增Attention前向、输出偏好、功能干预或新确认文本。

## 7. 实现、审计与追溯

先冻结[配置](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R04_domain_usage_20261027/domain_discriminability_spectrum_20261028/attention_source_link_20261028/config.json)/[协议](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R04_domain_usage_20261027/domain_discriminability_spectrum_20261028/attention_source_link_20261028/protocol_cn.md)再测。输入为四个登记资产的当前访问通过记录、R04冻结名单/谱基/投影、R05全部原Attention配对与同文本CSR、R06原固定名单/合格记录，只读；逐文档核对原R04与R05的token和CSR完全一致。代码没有模型加载、torch/transformers或优化器。audit.py独立检查全部旧64成员的命中率与前文端原结果完全一致、直接位置权重重算、单位投影全和1、精确分箱匹配/排除目标、全部事件原Attention、配对bootstrap/BH及输入哈希，共32项通过。

统计实现最初有一处括号错误，执行前修复；早期纯离线读取因NPZ字段在循环中重复解压而中止两次，改为一次载入字典，数值/名单/协议不变。审计也采用一次载入避免重复解压。图在实际PNG检查后仅改标签/版式。未覆盖旧产物，未改变旧Focus/Anchor、训练或科学接受状态。代码、原始表、文档值、随机ID、重采样索引均保留。全活跃表另提供无损NPZ，逐列回放与CSV完全一致，便于压缩交付。

科学机制判断与问题关闭仍为Unknown；本文的认识更新是对本批数据的有界解释。所有分支的工程与统计覆盖见[coverage.json](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R04_domain_usage_20261027/domain_discriminability_spectrum_20261028/attention_source_link_20261028/coverage.json)，不把执行完成当作机制通过。
