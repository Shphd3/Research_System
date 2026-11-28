# 理论推导原件与阅读顺序

要回答“什么条件下分开学才划算”，可以从 V5 的条件、V6.2 的修正和 10 月共享更新的原稿读起。目录中保留收到的版本。两份 V6.2 有不同措辞、预测和证据边界；本轮新增判断写在日期化的探索日志。[11 月 28 日修订](../../main/explore/1128_feature_grouping/log.md)

| 问题 | 原件 | 阅读重点 |
|---|---|---|
| 最初为什么选树？ | [Tree-MoE V5 英文原稿](tree_moe/tree_moe_theory_v5.md) · [中文全译](tree_moe/树形混合专家与稠密层_v5_中文全译.md) | 对照 A1–A6，分清有效容量、投影干扰、平方回归步长和每个输出的计算。 |
| 实测怎样修正 V5？ | [研究者此前发送的 V6.2 自包含稿](tree_moe/v6_2.md) · [协作仓 V6.2 推导草稿](tree_moe/research_draft/v6_2_derivation_draft.md) · [假设](tree_moe/research_draft/hypotheses.md) · [当时的 TODO](tree_moe/research_draft/TODO.md) | 看共享输出的交叉协方差、目标信号保留、叶条件曲率，以及哪些速度倍数只是预测。V6 合成检验另有[执行报告](/data/250010109/MoE_Router/experiments/v6_dynamics_1125/v6_dynamics_report.md)。 |
| 窄专家怎样维持可分性？ | [可分性与等效容量中文推导](capacity/1119_可分性与等效容量_理论推导_v1.md) · [英文稿](capacity/Separability_Capacity_of_Block_Experts.md) · [11 月 19 日推演记录](capacity/1119-建模推演-勘误稿.md) | 区分分类所需的维度和处理类内内容所需的维度。 |
| 两种特征何时合学？ | [10 月 8 日一步干扰原稿](grouping/Draft.pdf) · [特征组与专家的优化模型](<grouping/01_已有特征组到专家_模型与正则直觉 (1).md>) · [关系分组到学习验证](grouping/02_ANCHOR_关系分组到学习验证.md) · [共激活关系定义](grouping/共同激活关系_phi_定义检验与认识更新.md) | 将表征相似、预测误差信号、真实有限更新和共同激活的不同含义对齐。 |
| 哪些理想条件受过检验？ | [CHJ 的 V5 受控验证](validation/tree_moe_theory_v5_验证报告.pdf) · [11 月 26 日严格树分析](validation/11-26-为什么不要树形MoE.pdf) · [11 月 27 日实证报告](validation/11-27-SAE表征与MoE架构_实证结论.pdf) · [四叶表征组会交接](../meetings/组会交接.pdf) | 原作者的阶段判断和本项目的解释可对照阅读。HRJ 的实验条件与测试图在[协作仓报告](../../../../Projects/small_model/users/ruijunHuang/tree_moe_report/report.md)。 |
| 更早的研究版本 | [原稿与按收到日期区分的同名版本](earlier_work) · [MoE gating LaTeX 原包](earlier_work/XingyuDeng-MoEGating.zip) · [训练动力学 LaTeX 原包](earlier_work/XingyuDeng-TrainingDynamics.zip) | 保留特征分发长稿、早期 PDF 和包含推导的原始 TeX 包，便于查版本。 |

在只含系统 Git 的检出中可阅读 Markdown 推导。表中 PDF、原始 TeX 压缩包与逐字稿的链接指向共享工作区副本。

导入时按文件内容去重，相同文件名而内容有变化的版本分别保留。来源清单逐行记录接收路径、当前相对路径与 SHA-256。[来源清单](../source_documents.tsv) · [会议原件](../meetings)
