# S15 分析协议中文说明

状态：当前用户直接批准完整的现有数据分析。上传协议原件保留在sources/user_feature_routing_protocol.md，其中旧阶段A等待由当前授权覆盖。本轮不训练、不改权重、不干预路由、不生成新文本、不申请GPU资源，不执行独立新确认；无新Focus/Anchor和科学状态变更。

研究问题：由DEV先识别的共享／偏向成员，是否对应超过expert负载、类别和可交换模板结构的实际路由关联。主要竞争解释是读出位置、词面、长度、模板、共激活成员及类别路由差别。观测不能证明专家效用或共享学习的好坏。

1. 固定原生8层MoE 33B训练token模型及末层norm2/router输入SAE，1024/30000/ReLU Top32，实际8选2，无共享expert／drop；保存原load bias，不更新。特征与实际路由从同一个向量读取。
2. 复用S14的6912条S13英语前缀，DEV24家族8场景、CONF48家族16场景，24标签4表达。旧CONF已看过。显式文本末冒号为主；其余表达与原正文位置分表。保留旧行为每侧≥0.75门槛，失败仍展示。
3. 路由前冻结成员：共享为DEV同家族两侧交集频率≥0.75；偏向为边际差≥0.25、至少6/8开发场景同向；普遍背景≥0.90。后三个数值细则为公开技术补齐，未声称研究者此前逐项审核。评估每成员类别≥12家族／8场景，组相关角色≥80%合格。共享与偏向可重叠，不强制语义分区。
4. 主质量为r/2，每token和为1；Q1逐成员相对类别负载的TV等权均值；Q2共享成员A/B分布TV等权均值；Q3两侧偏向组各自等权平均分布的TV。每个token的成员承接同一完整路由，不算独立分配。真实gate权重和feature幅值加权为次要敏感性。5pp仅展示筛选，不是效用阈值。
5. 种子2026110815，1000全局完整场景／家族／标签块置换、1000固定类别表达位置的条件块置换，2000场景bootstrap。长度以DEV场景均长中位数分层，CONF任一层少于4簇则合并并如实报告控制损失。各问题八组Holm8及合并Holm24，成员另校正；原TV区间不能当等价性检验。
6. 随机成员同时匹配Q/G及DEV出现率绝对差≤0.10，DEV≥0.125，排除当前对候选，取最近32，1000次不重复抽组；不足不放宽。随机组为描述性参照。预先冻结匹配与重采样，再计算路由统计。
7. 已有本机H100 MIG，FP32/TF32关/batch16，12GiB／1800秒上限。先验证分词、hook完全相同、原生路由公式、单批误差≤1e−4及Top32／路由一致；校准重建均误差<1。采集6912条的两个位置，存hidden、8维logits／概率、Top2及权重、Top32及值、重建敏感性；不再次前向Q/G。不改参数或bias。
8. 主输出逐成员／类别／专家表、实际负载、三个问题、两层null、匹配覆盖、区间、真实案例和独立复算。零出现留NaN，证据不足不转成通过。科学验收Unknown，仅提一项AI后续建议，不自动训练。

完整精确口径：[protocol.md](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S15_feature_expert_routing_1108/protocol.md)、[statistics_plan.json](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S15_feature_expert_routing_1108/statistics_plan.json)。配置／成员／输入冻结早于前向；详细协议与完整主统计实现早于路由统计；完整gate次要重采样实现及补全192校正的后加性质在[差异记录](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S15_feature_expert_routing_1108/amendments.md)中。结果不得倒改为“全部文档事先冻结”。
