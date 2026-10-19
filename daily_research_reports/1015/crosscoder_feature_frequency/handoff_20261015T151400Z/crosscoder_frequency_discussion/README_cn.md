# CrossCoder 特征频率与关系分组：主 agent 讨论包

本包是已完成记录的派生读本，不新增结论或运行授权。**完整 H1 为 INSUFFICIENT，H2 为 NOT RUN。** 44组均值匹配对照不足，随机基线资格未通过；99次正式校准没有启动，无有效主p值。原始文档独立性仍为Unknown。

## 建议阅读顺序

1. [中文结果摘要](documents/summary_cn.md)：问题、模型、主要认识和一个AI建议的下一决策。
2. [五图与逐图说明](documents/figures_cn.md)：每图PDF/SVG/PNG；[全部186组分页PDF](figures/figure4_all_groups.pdf)。
3. [完整记录](documents/detailed_cn.md)和[结果推理审计](documents/reasoning_audit_cn.md)：区分数据现象、控制工程缺口与科学边界。
4. [执行登记 R0/R0.1](documents/execution_amendment_cn.md)，再看[原Protocol草稿](documents/protocol_draft_cn.md)；原草稿中的未运行状态是历史快照，以执行登记和结果记录为准。
5. [原始Anchor](sources/ANCHOR_特征频率与共同出现_v0.1.md)、[资产核对](documents/assets_checked_cn.md)和[evidence](evidence/terminal_receipt.json)。英文同名文档一并保留。

## 交给主 agent 的讨论重点

- 同size随机组有描述性同频优势，但均值匹配和全流程null没有完整裁定，不能用142组子集替代全体186组。
- 固定10,000提案上限与大组留样规则冲突：size>333不能满足10×size burn-in和20×size间隔留样。下一步建议来自原Summary：是否先修复对照预算规模并重新登记有界复验。
- D/V关系组186/185及成员Jaccard0.54838只属于已接触单bin；q20组数65/61体现分组尺度敏感。原文档/近重复确认尚缺。
- V有25.82%位置多组命中；组→输入→唯一专家需要另定映射。当前不是H2学习收益证据。

请先讨论上述证据与下一决策，保留Unknown、NA、INSUFFICIENT与NOT RUN；本包不能自动授权扩跑、训练或科学关闭。

## 文件与校验

figures/含五类图三种格式和全组PDF；tables/含绘图所需精选表，图5只含展示案例；evidence/含直接相关的小型统计与资格/访问收据。运行脚本、原始日志、模型、语料、完整激活/大矩阵不携带。

[PACKAGE_MANIFEST.json](PACKAGE_MANIFEST.json)记录每项原路径、原hash、包内hash和改链方式；[验证回执](PACKAGE_VALIDATION.json)记录解压后链接及字节校验。[外部依赖](EXTERNAL_DEPENDENCIES.md)明确未携带来源。文档中的本地阅读链接已改为包内相对路径，JSON里的原绝对路径仅为来源证据。
