# 数据字典与来源边界

- feature：冻结14源层、16384维CrossCoder中的原始latent坐标。激活事件是现成CSR中该坐标的门控z>0，不是已确认知识或语义标签。
- D/V：原缓存按既有块规则分成的发现/复核部分，N_D=5238097、N_V=5247663；文档独立性和近重复独立性未知。n是命中次数，p=n/N，是位置比例，不是文本篇数。
- group_id：沿用q10 D分组原始0起始ID。186非单例组共13807成员，各成员只归一个D组；不包括1859个单例。
- phi：二值命中事件的相关系数，计算包含未共同激活位置；不能只用共同次数排名代替。索引CSV的全对分布字段复用原phi float32；案例成对CSV精确表从原int64共同计数重新代入同一公式（数值精度差别不改变原边）。
- 连边：原候选集内，joint≥10、phi>0且互为前10邻居；门槛及排序不变。本报告只审计已有边，未重建图。
- group：原加权greedy modularity分区，resolution=1。同组不要求全连接、全对高phi、频率相等或每次全员激活。原合并过程日志没有保存。互选前10名还强制度≤10，大组密度因此有10/(人数−1)的上界，不能仅凭低密度判定关系弱；同时参考未筛选全对phi与桥结构。
- bridge/桥：在原组诱导子图里删除后增加连通分量数的边；articulation/割点同理但删除节点。这是现成图的描述，不是删feature的模型干预。
- matched_V_jaccard：原全局一对一匹配的交集/并集；matched_V_member_retention是交集/原D人数。actual_V_group_id逐成员给出实际去向，没进匹配V组不表示feature不再激活。
- unconstrained_best_V：只读比较现有V组（包括V单例）、取消全局一对一占位限制得到的最佳J，不是替换原注册匹配。q20_*读取已存在敏感性分组，不是新增q20运行。
- 稳定性：现有一次D/V和一次q20复核，不是时间序列、多个新split或独立文档复现。未测的长期稳定性为NOT_MEASURED；语义主题为NOT_ASSIGNED；学习相容为NOT_ESTABLISHED。
- 原随机案例：每组命中context按固定哈希抽样，再在选中context的命中位置哈希抽样；不是位置均匀、不是独立文档抽样。只复用已保存5+5中的3+3，未补采或补造。
- 高分：活跃组员数/组大小；不是z幅度和，不是统计置信度。同分按较早位置取，可能偏向早位置。
- 预测位置：当前t的feature来自模型可见token0…t；预测目标位于t+1。next_target_token_label_only来自真实语料，不是模型argmax；这些位置的实际模型预测未保存。
- 完整前缀和z：18条逐一复核原CSR，完整前缀独立复核token解码；卡片只显示末45token及当前token，前缀原文另附TXT和完整汇总。激活列表无top-k截断，未列成员z=0，完整含零CSV另存。

表内source_id对应[tables/source_manifest.json](tables/source_manifest.json)，包含绝对源地址、大小、SHA256及推导说明；frequency_source_row_1based_including_header可逐行定位原频率表。原始文本可能跨拼接片段，original_document_id仍UNKNOWN，不把context当独立原文档。
