# 逐组理解报告：先看一个真实小组

**先读[四成员G87完整案例](cases/group_087_cn.md)。** 它把成员次数、六对共同次数/phi、四条实际边、分组依据和六条文本连在一起：三角形加一条桥，并不是四人两两都连边。

本次只整理现有缓存、分组、频率和文本，未训练、未编码新位置，也未改变或重跑建图/分组参数。所有解释是AI依据现有证据的有界阅读，不改变科学批准。

## 三张卡要回答什么

- [G87：4成员](cases/group_087_cn.md)。三角形加桥，D/V及已有q20都保留同四人，但D频率仍相差5.67倍。六例语境分散，不能强命名主题。
- [G74：14成员](cases/group_074_cn.md)。原14人中12人仍在同一V组，却被并入98人的大组，导致Jaccard只有0.12；这是边界扩张，不能误读为多数成员丢失。高分字符片段的共同点被随机博客ID、用户名和DOI案例限制。
- [G34：149成员](cases/group_034_cn.md)。局部边292/310保留，但完整成员只有86/149进入匹配V组；D频率相差约605倍。关系图明确只画30人，频率图和成员表覆盖全部149人。六例都在当前token ` of`，仍不能推出统一话题或全部成员一起激活。

## 全部组与原始表

[186组可读索引](group_index_cn.md) · [186行索引CSV](tables/all_groups_index.csv) · [13807行完整成员CSV](tables/all_group_members.csv) · [每组完整成员/边表](tables/groups/)

[原始频率表](source_tables/frequency.csv)、[原始D分组](source_tables/groups_D.json)、[原始D边表](source_tables/edges_D.csv)、[原始V分组](source_tables/groups_V.json)、[原始V边表](source_tables/edges_V.csv)、[原始匹配表](source_tables/matches.csv)均为来源文件的字节副本。[数据字典](data_dictionary_cn.md)说明分母、来源和未知项。

每卡有3随机/3高分既有案例，逐条标注当前已见token、下一预测位置、完整前缀链接和全部非零组内z；[完整文本与激活](text_evidence/selected_cases.json)另含所有成员的零值。旧文件名target_token实际指当前已见token，本次已区分；真实下一token只是标签，不能写成模型实际预测。

**本次应保留的理解：** 同一个组里可以同时有较密局部、桥接成员、很宽的频率范围和不一致的文本触发。现有稳定性告诉我们哪部分在这次复核中重复，并不把这些统计组升级为语义组合，更不说明适合共同学习。此前“比匹配随机对照更同频”是群体相对比较，不保证每组频率范围都窄；本报告的宽范围并不与那个平均结果矛盾。

[审计与完整性核对](reasoning_audit_cn.md) · [全部产物来源/哈希](artifact_manifest.json)
