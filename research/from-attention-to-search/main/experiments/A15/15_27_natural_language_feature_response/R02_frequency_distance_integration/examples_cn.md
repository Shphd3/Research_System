# 成功读数与反例

本轮没有通过全部确认门槛的研究成功例。下面分清旧发现成功、局部测量成功和新反例；不把它们混成同一种证据。所有R02数字只作条件性描述，原前缀资格失败未被覆盖。

## 既有成功：R01 A01

末尾目标bank，tokenID6073，零起始位置16。可见前缀分别为“Mara began a field note on Monday. In it, Mara described the river bank”和相同前缀末尾“savings bank”。f6401的原激活及原始贡献从0变为4.0446；R01完整留出H1中该feature通过。该例是已暴露发现材料，本轮没有把它重新称为全新验证。

## 本轮测量成功：未出现的线索不能解释过去

R02 B01三个目标均为bass，ID21529，短版本位置90／106／111。位置90看到的前缀只有：

> At a catalog desk in Wrenford, two cards use the word bass. A report will select one card. The form was filed on Monday. A separate note gives routine filing details. It says that the page has a very wide margin and a clearly written date at the top. After the spelling and punctuation had been checked, the paper size was noted. The first card describes a freshwater fish, while the second card describes a musical instrument. The bass

00与01在线索一后是完全相同的可见前缀，f19601都为5.1622；10与11同为另一前缀，都为5.5294。改变此时尚不可见的线索二设置不改变该对齐读数，联合项为0。它是本例可见性和读数的一致性成功，不是两线索整合成功。

## 新反例：非加性不等于语义整合

在相同B01的第二位置106，f1818四组合z为00:4.1272、10:4.3947、01:4.6110、11:4.1076，联合项I=11−10−01+00=−0.7709。最终位置111没有新增相关线索，I却为+0.2463。预定义兼容续写只在2/4组合中胜出；两线索语义对应未通过。因此不能用这一条feature“突然出现联合项”解释高级语义。

另一个按冻结反例规则找到的组例是G02：旧R01 B17的f28673主差−8.7426；在新B01中，同一feature四组合、三个位置全为0。该组的新确认最少成员支持仅1/6；旧强响应不能自动外推到新联合关系。这里不把缺少支持写成“所有上下文都无效”。

## 频率的直接反例

G04的f1818参考命中4634/245760(1.8856%)，按窗口重采样95%区间[1.3928%,2.4423%]；f1205为45/245760(0.01831%)，区间[0.00692%,0.03418%]。同组成员点频率相差约103倍，足以反对“同组必须全员同频”的说法；它没有解决五组整体相对空模型的问题，Q1仍不足。

完整文本/三位置/候选/绝对与比例贡献见执行侧[例值](provenance/examples.json)、[逐位置成分表](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R02_frequency_distance_integration/offline/stagewise_feature_response_components.csv)和[参考频率表](tables/reference_frequency_counts_CI.csv)。不使用目标之后的文字给先前位置贴含义。
