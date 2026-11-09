# 远处目标与近处竞争：相同成员，不同强弱，仍不足以完整解释错误

我们要看模型利用远处物品事实时，近处竞争词怎样改变同一批SAE成员。当前结果支持MLP输入中一组六成员的事实差异跨近词和近远条件保持；竞争时成员强弱与模型偏好一起改变。行为解释仍有反例，未通过全部预定门槛。Attention因共同支持不足保持证据不足。

## 先讲抽屉里的 magnet

F23远处说`The drawer was packed with the magnet.`，最后问抽屉装了什么。保持完整320token、远物品e190、答案前冒号p319不动，只把近处另一个容器的object换成battery（近词末token309）。完整全文和候选逐token分数见[原文](/data/250010109/Research_System/research/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R19_20261104_remote_target_near_competitor_composition/casebook_cn.md)。

MLP输入#17390从7.418升到9.967，低频#25508从3.941降到3.272，#16240从15.728升到18.058，#27076从13.515降到11.247；同一组同时激活但搭配改变。battery/magnet完整候选分数由−14.919/−10.371变成−8.837/−9.626，模型由正确转为错误。固定近处词后单独改变远目标仍影响这些成员，目标分量没有全部消失。所选坐标中目标投影0.600、近词投影0.663，相反差−0.063；作差等式是定义，不是机制证明。

![真实成员与候选偏好](/data/250010109/Research_System/research/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R19_20261104_remote_target_near_competitor_composition/figures/MLPIN_SAE_F23_case.png)

图的下六行是严格匹配矩阵；上六行是旧主距离任务，中间黑线表示文本框架改变，不能跨线当作单因素竞争效果。颜色只用于观察每个成员的相对变化，格内是真实激活。

## 总体上保持了什么，失败在哪里

24家族按整家族分12发现/12表征留出，模板两侧共享。补96条匹配文本，所有292前向及原196条评分重放通过。主三个距离仍各12/12成对；匹配中性11/12、一致12/12、相反9/12，正确分差平均降3.814nat（区间2.847–4.912）。

MLP六共同成员的事实差异H1cos0.745（12族）、近远H2cos0.971（11族）通过。竞争变化与行为损失ρ0.636，Holm p0.0568、模板内p0.25，仅局部支持；Attention远矩阵只有5族、近远6族严格共同激活，低于8族门槛。不能把这当成两个位置的显著差异。

反例F11：组合相反差−0.023仍成对答对；F27：差仍+0.531却有误判。F28中性已错，不能把所有失败起点都归给竞争。二元共同出现超边际证据未保持；幅值重排两侧p0.0156，但家族区间跨0，稳定组合的主要判定证据不足。高/中/低频共同参与已见，参考低频不等于在本任务少见。

![跨家族总体](/data/250010109/Research_System/research/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R19_20261104_remote_target_near_competitor_composition/figures/MLPIN_SAE_membership_geometry.png)

左上展示成员复用和更换，右上展示事实差异方向；下方保留每个家族，红色为相反条件成对失败。可见表征指标与行为不一一对应，不能靠成功例宣布统一机制。

## 两个现场追问

为什么这组对照能区分解释？因为远目标A/B与近词A/B分别改变；相反对角T−N可以拆为固定近词的目标差和固定目标的近词差。旧主任务/竞争直接比较没有这个识别条件。

为什么还不能说这几个feature导致错误？我们只比较配对前缀在同一答案位置的稀疏表征；反例、候选先验、其他成员、后续句号评分和字典重建损失仍存在。没有激活干预，也没有跨任务验证。

[完整认识更新](/data/250010109/Research_System/research/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R19_20261104_remote_target_near_competitor_composition/summary_cn.md) · [每家族与频率数据](/data/250010109/Research_System/research/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R19_20261104_remote_target_near_competitor_composition/numeric_evidence.md) · [执行与原始文件](/data/250010109/Research_System/research/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R19_20261104_remote_target_near_competitor_composition/artifacts_cn.md)。本轮停止。待共同审阅后再决定是否设计功能实验；科学接受Unknown。
