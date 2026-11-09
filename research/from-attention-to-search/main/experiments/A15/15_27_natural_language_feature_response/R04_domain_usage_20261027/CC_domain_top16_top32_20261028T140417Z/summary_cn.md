# CrossCoder数学/生物候选：前16与前32的频率组成

**能够选出每域32个，不需放宽标准。** 原发现规则下数学有59、生物78个合格候选；固定前32，前16为其前缀，不根据频率或原留出结果重新排序。新增模型前向/训练/假设检验均0。它们是发现集领域使用候选，不是64个已确认语义feature。

## 主结果

|领域|候选数|高频|中频|低频|参考低支持|开发+原留出均满足两词复核|
|---|---|---|---|---|---|---|---|
|数学|前16|3 (18.75%)|13 (81.25%)|0 (0.00%)|0|2|
|数学|前32|9 (28.12%)|20 (62.50%)|3 (9.38%)|0|6|
|生物|前16|1 (6.25%)|11 (68.75%)|4 (25.00%)|0|3|
|生物|前32|4 (12.50%)|20 (62.50%)|8 (25.00%)|0|5|

每域前32合计64：高频13（20.31%）、中频40（62.50%）、低频11（17.19%）。两域均以中频为主；本轮生物候选的低频比例25%，数学9.38%。这是当前规则选出集合的描述，不是两个领域总体的频率规律或频率形成原因，也没有独立显著性检验。

## 分段对象与选择规则

频率来自匹配原生A22编码的R04 DCLM256窗口×256=65536token缓存，z>0计数；参考命中至少20的13357个坐标按频率排序大致三等分，原低/中/高成员数4469/4437/4451， ties不拆。低频20—170命中（0.03052%—0.25940%），中频171—881（>0.25940%至1.34430%），高频≥882（>1.34430%）。不是把候选本身平均分组；少于20命中另列低支持，本64个没有该类。

沿用上一轮：发现集30文档/域；整体本域命中偏向比例≥90%，≥10本域文档、≥2来源host，至少3说明文/2问答支持，单文档≤25%；至少两个预定普通token在两域各有≥15位置、≥5文档机会，本域≥8命中/≥4文档、同词偏向≥90%、单文档≤40%。按最强两词中较弱的本域减另一域命中率差排序，整体差和ID破同分。唯一范围改变是只保留CC、每域前4扩成前32，同时输出前16；没有按DCLM频率选人。

开发集/旧留出仍按上一轮预定门槛检查两词，不改变候选资格/排名、不换失败成员。前32中数学6、生物5同时满足两次缓存条件；其频段为数学高1/中5/低0、生物高1/中2/低2。可优先安排受控验证，但不是新独立确认。其余不是一律没响应，有同词机会少、命中支持少、或偏向未达90%等不同原因。

## 具体低频成员，全部保留

数学前32低频：f1097（第22，136/65536=0.2075%）、f754（第25，70/65536=0.1068%）、f7474（第29，165/65536=0.2518%）。

生物前32低频：f12141、f10013、f7922、f63、f5691、f6552、f9491、f3225。其中f9491（39/65536=0.0595%）和f3225（36/65536=0.0549%）均满足开发+原留出两词缓存条件，说明低频候选也可能保留领域偏向。它们频率估计仍有窗口重采样不确定性，不将“低频”当成专属语义标签。

全64频率均有5000次参考窗口重采样区间，若跨边界完整标注；主统计按既有点估计分段。不能用这些点计数断定频段归属绝对可靠。频率不等于强度、语义复杂度或长短程属性；两域同词仍可能有不同句法、话题和来源。

## 完整名单与来源

- [64候选、频率区间、两词计数和复核缺项](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R04_domain_usage_20261027/CC_domain_top16_top32_20261028T140417Z/CC_64候选_频率与复核完整表.csv)
- [四组频率计数及百分比](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R04_domain_usage_20261027/CC_domain_top16_top32_20261028T140417Z/CC_前16前32频段统计.csv)
- [数学前16](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R04_domain_usage_20261027/CC_domain_top16_top32_20261028T140417Z/CC_math_top16_原始候选.csv) / [前32](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R04_domain_usage_20261027/CC_domain_top16_top32_20261028T140417Z/CC_math_top32_原始候选.csv)
- [生物前16](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R04_domain_usage_20261027/CC_domain_top16_top32_20261028T140417Z/CC_biology_top16_原始候选.csv) / [前32](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R04_domain_usage_20261027/CC_domain_top16_top32_20261028T140417Z/CC_biology_top32_原始候选.csv)
- [全部feature编号JSON](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R04_domain_usage_20261027/CC_domain_top16_top32_20261028T140417Z/CC_四份固定名单.json)、[筛选规则](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R04_domain_usage_20261027/CC_domain_top16_top32_20261028T140417Z/selection_rules.json)、[发现名单冻结](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R04_domain_usage_20261027/CC_domain_top16_top32_20261028T140417Z/candidate_freeze.json)、[参考频段](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R04_domain_usage_20261027/CC_domain_top16_top32_20261028T140417Z/original_frequency_boundaries.json)、[审计](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R04_domain_usage_20261027/CC_domain_top16_top32_20261028T140417Z/audit.json)。

只用A22原14层共享z，不把最后层decoder贡献当独立激活；本轮二值计数不依赖decoder幅度。原R04角色和R06资格不因本次入选/未入选而变化；没有新训练、干预、模型前向或新Work/Codex任务。旧结果原样保留，完成本轮统计后停止。
