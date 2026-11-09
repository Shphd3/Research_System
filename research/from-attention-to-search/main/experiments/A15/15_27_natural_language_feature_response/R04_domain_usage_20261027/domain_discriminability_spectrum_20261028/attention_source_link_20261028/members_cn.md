# 先确认：连起来的是哪些成员？

这些是固定候选集合，不是新聚类。feature编号只在同一字典内有意义。Top16按旧发现方向分9数学、7生物；两个扩展方向各64独立列出。原R04共有32／数学16／生物16仍按旧定义，不能与新区分排序混名。

## SAE

top16_math：f11667, f693, f28024, f15133, f6042, f9403, f19841, f23363, f5179

top16_bio：f1004, f391, f11604, f10875, f18318, f2977, f13997

|set1|set2|n1|n2|intersection_size|intersection_ids|
|---|---|---|---|---|---|
|new_top16|R05_context_candidates|16|20|0|无|
|new_top16|R06_qualified_coordinates|16|25|0|无|
|expanded_math64|R05_context_candidates|64|20|2|16240 / 29461|
|expanded_math64|R06_qualified_coordinates|64|25|0|无|
|expanded_bio64|R05_context_candidates|64|20|1|24399|
|expanded_bio64|R06_qualified_coordinates|64|25|0|无|
|old_shared32|R05_context_candidates|32|20|3|5196 / 16240 / 20058|
|old_shared32|R06_qualified_coordinates|32|25|1|47|
|old_math16|R05_context_candidates|16|20|0|无|
|old_math16|R06_qualified_coordinates|16|25|0|无|
|old_bio16|R05_context_candidates|16|20|0|无|
|old_bio16|R06_qualified_coordinates|16|25|0|无|

## CC

top16_math：f8963, f14394, f11163, f14316, f4309, f12351, f3098, f3464, f8030

top16_bio：f11710, f652, f12141, f598, f8838, f4862, f1010

|set1|set2|n1|n2|intersection_size|intersection_ids|
|---|---|---|---|---|---|
|new_top16|R05_context_candidates|16|25|0|无|
|new_top16|R06_qualified_coordinates|16|26|0|无|
|expanded_math64|R05_context_candidates|64|25|0|无|
|expanded_math64|R06_qualified_coordinates|64|26|0|无|
|expanded_bio64|R05_context_candidates|64|25|2|2764 / 12266|
|expanded_bio64|R06_qualified_coordinates|64|26|0|无|
|old_shared32|R05_context_candidates|32|25|0|无|
|old_shared32|R06_qualified_coordinates|32|26|0|无|
|old_math16|R05_context_candidates|16|25|0|无|
|old_math16|R06_qualified_coordinates|16|26|0|无|
|old_bio16|R05_context_candidates|16|25|0|无|
|old_bio16|R06_qualified_coordinates|16|26|0|无|

R06原始对象为“概念×feature”，这里为核对交集才折叠成唯一坐标：合格SAE26对象涉及25坐标，CC26对象涉及26坐标。交集0不证明两类概念在模型中无关系，只说明不能把同编号资格直接借用。

[全部名单（含扩展128和原R04三组）](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R04_domain_usage_20261027/domain_discriminability_spectrum_20261028/attention_source_link_20261028/tables/frozen_members.csv) · [所有成对交集](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R04_domain_usage_20261027/domain_discriminability_spectrum_20261028/attention_source_link_20261028/tables/set_intersections.csv) · [R05全频段坐标表SAE](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R04_domain_usage_20261027/domain_discriminability_spectrum_20261028/attention_source_link_20261028/sources/SAE_R05_all_frequency_and_role_ids.json) · [CC](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R04_domain_usage_20261027/domain_discriminability_spectrum_20261028/attention_source_link_20261028/sources/CC_R05_all_frequency_and_role_ids.json)