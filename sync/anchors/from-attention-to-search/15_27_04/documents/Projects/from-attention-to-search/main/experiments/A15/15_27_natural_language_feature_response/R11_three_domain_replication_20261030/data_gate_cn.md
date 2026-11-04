派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R11_three_domain_replication_20261030/data_gate_cn.md`。
[精确原始文件](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R11_three_domain_replication_20261030/data_gate_cn.md)；研究修改仍回到原件。

---

# R11数据资格：候选清点完成，450篇清单未合格

[English](data_gate.md) · [阶段结果](summary_cn.md) · [原配额](../../../../../../../../UNAVAILABLE.md)

本次扫描已登记DCLM原始档案全部59,812篇。v1预筛候选1,940家族；补足概率、离散及其他主题词后的v2为2,537家族。两版独立保存。v2数学327、生物1,890、物理337是允许重叠的暂定领域标签，不是已审核样本。

本轮要求每域150篇，每主题25篇；每域60发现、30开发、60独立留出。留出各30篇同平台新家族与全新平台新家族，新平台部分需要7篇问答和至少4个平台，平台不能只对应单一领域。旧120篇及其家族、参考文档和近重复排除；精确来源、家族和划分仍需审阅。

| 当前清点的暂标缺口 | 候选数 | 方案所需 |
|---|---:|---:|
| 数学：离散／逻辑 |14|25|
| 数学：分析 |24|25|
| 物理：热／统计 |16|25|
| 物理：材料／固体 |18|25|
| 物理：全新来源且跨域平台问答候选 |2|7|

候选数在内容审核前，不能保证通过；标签本身可能漏召回或误判，不能据此说所有可用原文都不够。当前只能说没有完成满足协议的清单与划分证明。118个平台暂时在两个以上领域有候选，不等于来源平衡已合格。

M2D2流体和光学原始train/valid/test档案可读，但文档／论文家族边界尚未核验，不能把每行当一篇独立文档；仅两类物理来源也不能直接满足6主题和平台留出。一次公开问答页面读取遇403，未取得可用新语料，未绕过访问限制。

复现入口：本轮`scripts/prepare_candidates.py`，原版与`--broad`版本；执行结果在`preparation/`及`preparation/broader_topic_inventory_v2/`。配置、候选原文、原始行号／URL／家族及片段位置保留执行侧。`source_inventory_manifest.json`记录字节及hash。

依赖此清单的三域前向和统计保持NOT RUN，实际新增前向0。缓存谱分析已完成，不受本门槛影响。下一输入是经审核、满足来源／主题／独立划分的450篇清单。保持协议，不自动降低配额或改成另一类语料实验。
