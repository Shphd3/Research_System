派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_25_03_context_computation_dependency/R00_readonly_design_20261026/asset_audit_cn.md`。
[精确原始文件](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_25_03_context_computation_dependency/R00_readonly_design_20261026/asset_audit_cn.md)；研究修改仍回到原件。

---

# 资产核对及测量缺口

本轮只读取已知本人资产的登记、源码、文本schema及小文件，不查找他人checkpoint。两份当前strict访问回执见provenance。可读不等于实际加载；大权重仅核对存在和大小，保存SHA沿用原始回执，没有假称重新全量哈希。

| 对象 | 已核对 | 尚未完成 |
|---|---|---|
| Qwen3-0.6B Base／原tokenizer | 登记入口、配置当前哈希与原绑定一致，28层／1024宽 | 当前模型实际加载与hook复放未做 |
| A22最终14层字典 | checkpoint路径与保存SHA、244140更新／999997440配对位置、共享16384特征、原源码 | 当前完整张量反序列化未做 |
| 归一化／门控 | 冻结TRAIN均值14×1024、逐层向量RMS14，标定65536位置，完整阈值原状态 | 不重拟合；执行时加载精确buffers |
| 编码／解码 | z由14层求和编码，decoder每层一套；偏置与单位已定义 | 没有独立层feature激活接口 |
| 历史重构质量 | DCLM FVE14=99.4707923%、28=86.4722113%；父记录末层重构CE代价0.305962nat | 不是当前Tulu及选定方向的资格 |
| Tulu文本与缓存 | train／eval原JSON哈希、字段、TRAIN1024／EVAL256对话；末层h＋共享z接口 | 不含源层h；需获准后的真实前向 |
| 留出独立性 | 对话ID、prompt哈希与来源可定位；旧EVAL已暴露 | 近重复未知，因此只能探索性 |
| 局部R测量 | 可以用既有decoder构造去干扰方向分数 | 不是独立feature；重构／分辨／携带资格NOT_RUN |

替代方案的级别：①首选真实后层局部方向读数，需过协议资格；②只保留预测功能读数时，可报告C干预是否有预测效应，但不能回答C→R；③若必须有独立层feature激活，则所选资产当前不提供，此轮不训练新SAE／CrossCoder，直接说明缺口。

原跨层共享z画像与低频token分析仅作已知边界，不重新当实验目标。当前入口导航检查有7项原有UNTRACKED，位于其他已存在材料，未修改；不影响已直接核实的命名源访问，也不是科研资格结论。
