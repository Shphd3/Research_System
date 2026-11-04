# 只读准备摘要：CrossCoder的C→R功能依赖

**准备完成，干预尚未执行。** 唯一问题是：同token不同上下文中，在第14层削弱稳定共同候选C，是否相对匹配干预，影响第28层上下文计算方向R与预定预测。已有低频feature／罕见词分析不重跑，A17只提供需要功能检验的动机。

已定位原Qwen3-0.6B Base、A22最终14层16384特征字典、10M联合z缓存、Tulu训练／评价文本及缓存，当前所需资产入口均可读。核对了源码、冻结归一化、hook与原缓存接口。未加载模型／缓存张量，未重算大权重完整哈希；保存SHA及当前小文件哈希已记录，不能把可读当成功加载。

关键限制：①联合z同时读取14层，不能用它的干预后变化说明跨层传播；②Tulu缓存没有源层激活，也没有独立层feature编码器；③历史末层FVE约86.47%、重构替换增加约0.306nat损失；④既有EVAL已暴露，只能探索性留出，近重复独立性未知。

替代测量：在真实后层激活上使用预定义、去干扰的decoder方向分数，明确它不是独立feature激活；用局部重构误差、上下文区分和直接残差携带检验其资格。资格不足即交付不足，不训练字典。最多两个token候选，名单、上下文目标与案例仍NOT_SELECTED，之后在发现侧按预定规则产生并冻结，不编造例子。

协议预设两档C小幅削弱、等实际位移随机方向与其他候选对照。主结果同时看R与上下文预测的配对效果，并报告整体预测损害。只有两项特异作用及测量守卫均通过才支持当前依赖；未做R单独干预，仍不证明预测变化由R中介。

当前模型前向0／训练0／干预0／新资源0。未来计划上限4864条序列，用户硬上限12000，余量不授权追加研究。当前仅只读核对与设计获准；收到“继续执行本协议”后才进入发现、资格与干预。没有组会讲稿或虚构结果图。

[Anchor](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_25_joint_feature_graph/subanchors/15_25_03_context_computation_dependency_anchor_cn.md) · [协议](protocol_cn.md) · [判定表](decision_table_cn.md) · [资产与缺口](asset_audit_cn.md) · [配置](protocol_config.json)。
