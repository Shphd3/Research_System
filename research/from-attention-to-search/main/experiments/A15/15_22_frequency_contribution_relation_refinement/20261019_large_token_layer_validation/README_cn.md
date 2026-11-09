# 大样本与跨层复核：统计倾向不等于逐输入的可靠对应

**已完成无训练缓存分析。** [先读一页白话](one_page_cn.md) · [概要](summary_cn.md) · [完整报告](detailed_cn.md) · [Protocol](protocol_cn.md) · [推理审计](reasoning_audit_cn.md) · [全部源表](tables) · [图说明](figures/figure_notes_cn.md)。

这轮只问低频token和低频feature是否有关、不同模型层是否一样。新增DCLM窗口10,485,760位置：发现侧5,238,097估频率、复核侧5,247,663测关联；另复用Tulu SFT原85,548/22,446位置。DCLM只作大样本跨数据分析，没有重新训练模型或专家，也没有扩大SFT答案缓存。原文档独立性未知，现有留出均已被查看，结论限探索性。

- **逐feature的总体频率趋势存在。** 在DCLM中，feature越低频，其命中位置的平均token稀有程度总体越高；已知token复核命中≥20的15,749个feature等权相关0.339。这是跨全部合格feature的趋势，不是最低频314项都已充分验证。
- **输入位置的极低频画像不可靠。** 用当地发现侧定义最低频314项，位置相关仅0.006；tokenID等权变成−0.119。不能把0.339替代0.006，二者对象和加权不同。
- **14层方向接近，但不是14套独立feature。** 每位置共享同一z，跨层只换decoder幅度；命中统计不按层重复。旧Tulu1694池迁到DCLM只有25项仍属于当地最低频段，固定旧池与当地低频定义必须分开。

这轮不改旧Anchor/Focus或旧实验结论，不作学习收益、知识难度、梯度干扰、功能或容量推断。研究者最终科学判断仍待讨论；下一实验仅列AI建议，交付后停止。

## 图与数据

1. [各层相关及块间波动](figures/figure1_layer_correlations.png)：global点估计与等块平均相关区间分开。
2. [末层四频段的token频率分组对照](figures/figure2_r28_token_band.png)：保留未见token和NA。
3. [命中、总量与份额分解](figures/figure3_binary_contribution.png)：分开解释二元命中与幅度代理。
4. [逐feature对应散点](figures/figure4_feature_level_correspondence.png)：每点一个feature，support≥20，不能代替输入位置分析。

每图有PNG/PDF/SVG；13张表包括逐feature频率/命中支持、冻结名单、全部层、固定旧池迁移、块相关及条件均值。原始缓存、代码和完整日志留执行侧；精确来源、文件哈希与完成成本见[完成回执](completion_receipt.json)和[payload manifest](payload_manifest.json)。
