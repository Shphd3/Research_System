派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R05_distance_attention_20261028/protocol_cn.md`。
[精确原始文件](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R05_distance_attention_20261028/protocol_cn.md)；研究修改仍回到原件。

---

# R05 冻结执行协议

用户本轮整合修订为两个实验的执行授权。正式数值合同为config.json；英文协议保留完整17项审计。下列中文设置与其同义。

Exact executable settings: [config.json](../../../../../../../../UNAVAILABLE.md). Frozen texts: [B.jsonl](../../../../../../../../UNAVAILABLE.md), [A.jsonl](../../../../../../../../UNAVAILABLE.md). All values below are fixed before forwards.

# A15_27：距离响应、频率与 Attention 两端共同激活

## 1. 问题定义
哪些固定 feature 对远处可见前文内容仍有可复现响应？再描述其 DCLM 参考频率、Attention 两端共享关系和联合字典的跨层重构贡献。本轮 R05 替换旧距离设置与预算，旧轮结果及预算不改写。不要求自然簇。

## 2. 物理先验
目标响应可以依赖前文；共同命中可能来自基准频率、重复词和位置分布。SAE 读取 block27 的 MLP 输入；CrossCoder 合并14个同位置 residual-post 得到一个共享 z。两者不是 Attention value。

## 3. 可证伪假设
B：相关线索编辑的贡献变化超过无关编辑，且在独立家族和两种措辞复现。竞争解释是词面、重复填充、句序或个别家族。A：相近距离内，高 Attention 配对比中等 Attention 对照额外共同命中；竞争解释是同词与标点等共现因素。两个实验分别判定；不显著不等于不存在。

## 4. 数学模型
距离为目标位置减线索末尾位置，测试16/48/80/112/144；A使用1–32等五个区间。一个feature是冻结字典坐标。原空间贡献幅度为 z 乘 native decoder 范数。B按家族计算 |cX−cY|−(|cX−cXU|+|cY−cYU|)/2；发现RMS只作固定尺度。A计算两端 z>0 的比例，比较高/中 Attention 位置并按查询、head、文档等权汇总。

## 5. 计算实现
原生E16和A22共用一次Base前向，不截取encoder分支。B24家族12发现/12留出、两措辞五距离四版本，共960条。发现两端各选最多16去重，至少4家族支持。A复用120篇R04真实文档，固定block27、16heads和每篇最多8查询。复用R04全坐标DCLM频率；≥20次命中按三分位分组，低支持另列。CrossCoder逐层贡献和decoder范数一同保存，层参考RMS来自A发现文档，不追加参考前向。

## 6. 最小证伪检查
B家族区间、4096符号翻转、最小效应0.10发现RMS；候选全部五距离和近远差在两字典内合并BH。A按文档区间、9999符号翻转，最小共同命中差0.001；频率组、B类别与B候选、五档、同词/异词和两字典合并BH。具体缺项、支持和数值资格在R05冻结协议。最多1096次完整前缀，含最多16检查；不显著不追加。

## 7. 当前证据
执行前为 NOT RUN。旧R04支持文档使用模式可读，但固定通用目标确认不足；旧结果保存在原Summary。新证据由R05 Summary与Detailed拥有，不通过写作自动更新机制判断。

## 8. 边界与下一决定
这轮测距离编辑响应和Attention端点关联，不能证明理解正确、频率造成组织、边传输feature或逐层语义产生。完成冻结范围后交付四图、一页结论及详细证据；研究者讨论后只选择一个后续问题。scientific_mechanism_judgment: Unknown；question_closure: Unknown。


## 数值、缺项与停止规则

B最低效应0.10发现RMS；4096家族符号翻转与5000家族重采样；两字典所有候选五档及近远差合并BH。留出每档至少4家族激活，两措辞均值正，区间下界与均值均超过0.10且q<.05才称稳定。A最低共同命中差0.001，2000文档重采样、9999文档符号翻转；至少10匹配文档。频率三组、B三类别及逐候选、五档、同词异词、两字典合并BH。原R04角色、标点与低支持为描述，不参与主结论。距离匹配控制caliper8tokens；未匹配不补。非显著不等于不存在。

检查最多16、总计最多1096；冻结数值容差不随结果改。SDPA读数与原R04缓存重放，selected-query注意力与最后层eager对照，重构与可见前缀检查后执行。工程修复记账续跑；对象变化或资源/预算扩张才暂停。无新训练、干预、聚类、参考语料或封存TEST。完整代码和缺项由Detailed记录。
