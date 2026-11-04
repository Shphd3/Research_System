派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A17/17_04_conditional_mapping_transfer/rounds/R06_functional_protection_20261025/detailed_cn.md`。
[精确原始文件](../../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A17/17_04_conditional_mapping_transfer/rounds/R06_functional_protection_20261025/detailed_cn.md)；研究修改仍回到原件。

---

# R06实际执行、差异与可复核证据

已完成36/36条240步轨迹；单卡H100 reserve作业pt-f2wnbino，训练墙钟25.18分钟。开始UTC 2026-10-25T17:50:16.741554+00:00，结束2026-10-25T18:15:27.657718+00:00；没有追加步数、其他Work/Codex任务或资源扩额。

任务是可见模式的首末词映射，不是加法。沿用同一合格旧终点、原官方Base、原划分及末层Q/K/V/O范围。旧DEV800/800。旧终点、数据和缓存当前身份核验通过；R02六个新/混训端点的身份沿原回执追溯，未重复加载或冒充本轮对照。具体哈希与来源见reproduce/history_lineage.json和freeze.json。

每步新答案固定36；旧输入槽固定36，其中0/4/36个有监督，统一除72。各方法另用同一规则的64条旧TRAIN探针，计算旧平均损失梯度。0槽也有探针旧标签，所以不能叫无旧监督信息。每条完整轨迹有8640新答案、0/960/8640旧目标答案和15360旧探针梯度标签使用；另有10个固定检查步复用640次标签做更新后诊断，探针合计16000次标签使用；输入token与额外计算独立计数。

F约束的是Adam已提出的实际位移，使用四矩阵拼接后的旧梯度；D在自身状态保持原方向，仅匹配自身F候选长度。原Adam矩不修改。S复用旧完整权重的每矩阵16个秩一系数及原1200步调度，只截取前240步，不能扩大解释为保留完整左右子空间。

评价是全词表151936输出最大值，不将答案限制在三词列表；旧/新各800题、四格各200。主终点240步；连续两次新平均准确率≥90%的第二次读数为次要比较，未达到不删除。全部逐题记录、每步标量、逐种子曲线、配对差和成本保留，表格已从逐题记录独立复算。三个顺序共用一个旧模型，范围不是模型总体置信区间。

实现校验包括有害/有益/零梯度和方向幅度反例、旧模型资格、当前缓存形状原生重放，以及独立进程第1步恢复到第2步的权重、Adam、随机数与计数逐字节一致。当前12例缓存最大logit差8.3923e−5，小于冻结的2e−4且预测一致。其它终点未逐个外进程复放，不能扩大恢复资格。

发现并修复了一个TensorBoard轴标签工程错误：progress/optimizer_step曾混写更新步与token步。原损失JSON、检查点计数和科学计算不受影响；训练结束后完整保留原events到tensorboard_raw，从原逐步JSON重建规范events，逐标签核对有限性、步轴单调和损失一致。主源码冻结后未改写。外部继承的carriers.py/runtime.sh在启动后补记哈希，明确不冒充事前封存。详见deviations.md。

实际保存288个状态，全部240步终点另行核验payload哈希；保存四矩阵、Adam、RNG、调度、数据位置、曝光计数及顺序/投影身份。逐步位移长度和、平方和及终点净位移不可混用；本轮诊断表明确只报所计算的逐步统计，不凭它反推终点或功能。有限步旧探针损失与一阶预测分开报告。

英文详细记录在detailed.md，完整结果在summary_cn.md和tables/，所有回执及源码在reproduce/。本轮不读取TEST，不引入SAE/CrossCoder/MoE，不改R02/R05结果，不混入加法证据。科学机制接受与总问题关闭仍待研究者判断。

Legacy R05 configuration fields objective/moe/natural/reselect_steps/old milestones are inert in this engine. Actual R06 objective, batches, probes and evaluations use the explicit new flat fields and hard-bounded engine loop. full_updates=1200 owns only the inherited S attenuation horizon; max_updates=240 owns the scientific run budget. No legacy stage was launched.

360 fixed finite-step probe checks and all original DEV cells are in tables/probe_finite_diagnostics_360.csv and DEV_cells_all_readings.csv. Probe-gradient label uses15360 plus640post-update diagnostic reuses=16000per full run; objective old labels0/960/8640are separate. Positive raw finite differences include small floating-point values and are not significance tests.

**交付时限偏差：** 训练25.18分钟，核心分析、登记及检查在起点后38分钟内完成；最终打包与归档在后续续接时完成，超过原定4小时墙钟交付窗口。不能称端到端预算内完成；期间没有新增训练或资源。时间依据见[回执](../../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A17/17_04_conditional_mapping_transfer/rounds/R06_functional_protection_20261025/reproduce/report_budget_deviation.json)。
