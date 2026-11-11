# R05最终结果包

AI分析；研究者判断 Unknown。

按此顺序阅读：

1. [汇报与学习效果分析](README_cn.md)：目的、三条结论、主要数据和后续架构讨论。
2. [集中度拆解](concentration_cn.md)：逐层／频段、条件分布q与全局负载u的代数分摊。
3. [学会、遗忘与恢复](learning_forgetting_cn.md)：原判据、全部区间、共同起点对照及切换修复。
4. [简明结果](summary_cn.md)／[完整证据记录](detailed_cn.md)，另有summary.md、detailed.md英文版。
5. F_coverage.csv/md列逐项范围；predictions.csv/md列冻结P5–P9结果。

F_loss_detailed为10臂训练CE与EVAL曲线；F_concentration_decomposition为集中度拆解；F_learning_forgetting为学会／遗忘。所有图另有PDF，汇总表同时有CSV和Markdown。

A8、A9、A9d训练完成；A9/A9d新增1000步。原生A0历史1250／1750和A4的1500未保留逐位置数据及权重，5个配对组合共55个总体／频段区间为BLOCKED。聚合曲线、全部终点判据、其余学习／遗忘分析完整。

包内per_atom保留关键原子切换、t50及最终集中度分摊数据；其余大型明细以omitted_large_tables.json列绝对路径，保留在执行工作区。包不含模型权重、训练数据、逐位置大文件。file_manifest.json提供包内SHA256；reading_copy_changes.json只记录阅读副本的链接适配，原始冻结protocol字节不变。旧阶段讨论包不是本包的当前状态。

臂名速查：A0原生路由；A1 teacher token聚类固定路由；A1-deep仅后4层token聚类；A2随机固定路由；A4蒸馏token聚类分数；A5 teacher原子共激活分组固定路由；A6原子集中正则；A8蒸馏A5原子分组；A9全8层student自举原子路由；A9d仅后4层student自举。A7未执行。
