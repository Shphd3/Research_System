# A17_03_E03：完整执行与证据记录

[English](detailed.md) · [总结](summary_cn.md) · [Protocol](protocol_cn.md)

## 1. 结果与资格

Smoke12/12、四个独立进程重放、Full108/108完成；独立复算3888个汇总量和86400个逐条CE恒等检查通过。36状态案例中，24个在原旧错误集的out_norm−full平均首末优势为负，另12个不是；顺序/阶段均值存在反号。不声称稳定双向损害或完整100步机制。

## 2. 术语和实际设置

模型为原登记Qwen3-0.6B Base，唯一变化参数是末层Attention o_proj[1024,2048]，其余冻结。使用完整FP32原生SDPA前向，eval、确定性、无TF32。原秩16Q固定，不重新选方向。恢复普通/限制历史的新训练第1/16/50步，共三种子29/43/71、双顺序、36状态案例。每状态独立比较完整、只删除、删除并放大；无累计重训或新增检查点。s来自原普通轨迹的实际下一步参考长度；同一步双历史使用相同下一批20个新训练答案。只删除不匹配长度，正用于区分删除与放大。

## 3. 数据、监督与划分

原list_rules_v1训练4000条只用于来源梯度；dev800条即400对列表，每规则每未见面板200答案。两个面板分别/等权合并。原旧错误/正确集由旧训练终点确定，各状态不按结果挑选。dev已暴露，不称盲确认；test关闭。相同步双历史固定来源，同一状态三操作恢复同一基线。跨步骤来源不同，不能把所有变化归因于状态。22输入ID及实际地址见[config](/data/250010109/MoE_Router/experiments/20261011_a17_trajectory_mechanism/runs/trajectory_20261011T090921Z/config.json)和[本轮输入访问](/data/250010109/MoE_Router/experiments/20261011_a17_trajectory_mechanism/provenance/input_access.json)。

## 4. 冻结合同、偏差与执行

| 项目 | 预定/实际 | 资格与证据 |
|---|---|---|
| 科学与代码冻结 | source/config/中途状态/基底/原读数 |freeze.json及快照绑定 |
| Smoke |12单元，4重放 |全部通过 |
| Full |108单元 |无缺失、无重试 |
| 基线重放 |对照原中途读数 |最大差0 |
| 新累计训练 |0 |仅评估与来源梯度计数 |
| test |关闭 |配置及完成回执 |
| 中文协议表述 |提交后展开翻译，设定不变 |冻结正文保留，不改变资格 |

Smoke `pt-c1i5f9pl`、Full `pt-8aoyrzuw`，单节点四H100 reserved、四独立进程。具体镜像/完整命令在acp_receipts及execution_certificate；镜像来源为System envelope。过程无失败或重试。max舍入=0.00017014635，max基外泄漏=1.1398543e-06，max梯度重组=4.198697e-06，max同长度实际误差=1.6391277e-07；各数值资格通过。原冻结参数字节/version、source20/W精确恢复、独立外进程重放均通过。

## 5. 主要指标与证据谱系

主要是原旧错误集的out_norm−full首末优势、全词表最强竞争优势和净修复数量。另报原旧正确集丢失、只删除及放大效应、CE/词池总概率/词对分项/b/h。每案例平均，再按种子等权；双顺序和面板分别及等权合并。只有三独立训练种子，重复列表/状态/来源不增加独立样本量。不作新增显著性检验。

| 判断 | 原始产物→计算→结果 | 边界 |
|---|---|---|
| 修复差异早期出现 |E01保存逐条读数→trajectory.py→trajectory/aggregate.json |只定位保存区间，非精确起始步 |
| 同状态操作效应 |baseline/cells→audit_summarize.py→case_contrasts.json |指定状态来源的一次有限干预 |
| 状态/顺序异质性 |case_contrasts→order_state_heterogeneity.json |不能平均掉反号条件 |
| 概率与选择的区别 |逐条CE、词池/词对、竞争词→metric_changes |输出记账非模块中介 |
| 真实修复示例 |原始cell→example_lost_repair.json |结果后选例，仅说明，不新增独立证据 |

## 6. 完整结果与单轮记录

全部逐案例/面板结果在执行侧，不重复原始历史。[轨迹汇总](/data/250010109/MoE_Router/experiments/20261011_a17_trajectory_mechanism/runs/trajectory_20261011T090921Z/analysis/trajectory/aggregate.json)、[逐案例轨迹](/data/250010109/MoE_Router/experiments/20261011_a17_trajectory_mechanism/runs/trajectory_20261011T090921Z/analysis/trajectory/per_case_panel.json)、[有限变化](/data/250010109/MoE_Router/experiments/20261011_a17_trajectory_mechanism/runs/trajectory_20261011T090921Z/analysis/full/metric_changes.json)、[案例对照](/data/250010109/MoE_Router/experiments/20261011_a17_trajectory_mechanism/runs/trajectory_20261011T090921Z/analysis/full/case_contrasts.json)、[顺序/状态反号](/data/250010109/MoE_Router/experiments/20261011_a17_trajectory_mechanism/runs/trajectory_20261011T090921Z/analysis/full/order_state_heterogeneity.json)。

本轮问题是当前操作与累计状态对旧错误修复差异的作用；实际设置、训练来源、评价划分如上；结果合格且异质；认识更新是可观察的局部操作代价与整体帮助可以并存。完整训练机制仍Unknown，第二轮未执行。本轮没有额外短训练分支，完成以约定有限干预为界。

## 7. 解释、边界与下一判断

来源梯度与下游响应共同随历史改变，跨历史不是独立中介辨认。配对b/h是输出坐标，不能命名内部功能。全词表竞争补足首末margin，但不能由这一例定位参数功能。原旧错误子集可能受损而整体旧CE仍改善，两者不是矛盾。不能推出完整100步中介、规则算法、不可兼容、容量不足、专家收益或自然文本推广。后续科学判断仍由研究者拥有。

## 8. 产物与复现

[执行目录](/data/250010109/MoE_Router/experiments/20261011_a17_trajectory_mechanism/runs/trajectory_20261011T090921Z)、[冻结输入/源](/data/250010109/MoE_Router/experiments/20261011_a17_trajectory_mechanism/runs/trajectory_20261011T090921Z/freeze.json)、[完成回执](/data/250010109/MoE_Router/experiments/20261011_a17_trajectory_mechanism/runs/trajectory_20261011T090921Z/completion.json)、[独立审计](/data/250010109/MoE_Router/experiments/20261011_a17_trajectory_mechanism/runs/trajectory_20261011T090921Z/analysis/full/engineering_audit.json)、[登记回执](/data/250010109/MoE_Router/experiments/20261011_a17_trajectory_mechanism/runs/trajectory_20261011T090921Z/registration/receipt.json)、[当前输出访问](/data/250010109/Research_System/assets/checks/2026-10-11_a17_trajectory_20261011T090921Z.json)。

实际登记ID：representation_a17_03_trajectory_smoke_20261011t090921z, representation_a17_03_trajectory_full_20261011t090921z。manifest逐文件保存新算SHA；无新增模型检查点。运行入口source/run.py，提交入口launch/prepare_submit.py，分析入口analysis/trajectory.py与audit_summarize.py，源版本见冻结文件及analysis_source_manifest。所有原始payload保持执行侧。
