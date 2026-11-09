# A15_27 R03：同位置共激活、频率与远处前文

**已完成：新子图有超出边际频率的共激活，C-03有有界远处编辑响应；同频成簇、低频→高频组织和簇的完整语义功能仍未决。** 先读[中文短结论](summary_cn.md)，再查[完整分析](detailed_cn.md)、[原文例子与反例](examples_cn.md)及[来源清单](artifact_manifest.md)。

本轮主对象是同token共享CrossCoder z的二值共激活。O保留A15_25原图；R为新原始条件图，C为新deltaP关联图。表内R02/C02/C03是本轮图组，正文写R-02/C-02/C-03，以避免R02与旧实验轮次混淆；它们都不是旧G02/G04差值组。主模型/字典固定为Qwen3-0.6B/A22 F16384，不对齐E16编号。

阅读图：

- [图1：原图、新R/C及频率](figures/figure1_graphs_frequency.png)。旧O多数边delta小，但极高频终点的delta有数学上限；新R的26边全部也在C，不能称被校正删去。
- 原[图2a](figures/figure2a_sense_tokens.png)／[图2b](figures/figure2b_person_tokens.png)保留预定全句投影的显示失败：首token主导名单、目标显示值为0。后补[S01目标细图](figures/figure2a_sense_target_detail.png)／[R01目标细图](figures/figure2b_person_target_detail.png)是post-hoc实例解释，不作独立验证。C--表示固定512坐标未覆盖，不能解释为频率校正删除。
- [图3：近远线索效应](figures/figure3_near_far.png)。相关−无关编辑分开，C-03由少数成员主导；句序与编辑量竞争解释保留。

原文档/句子单位和文本类型缺失，参考context区间只描述；频率null无合格稳定组，p/q为NA；低频四分位节点支持不足。命名只到“混合语境候选组”。[冻结协议](protocol_cn.md)、[匹配资产](asset_audit_cn.md)和[文本清单](text_manifest_cn.md)各自保留定义、身份及NOT RUN范围。

R02的Q3（逐步双线索整合）仍为**证据不足**。R03未新增四组合整合检验，当前CrossCoder资格通过也不修复旧E16不同接口的前缀检查失败。

12情境/72文本预先固定，预算内测6完整案例/36输入，另12资格调用通过；其他36文本因预算NOT RUN。新增48条，父任务累计1500/1500。无训练、模型修改、激活干预、封存TEST或新资源；机制接受和问题关闭Unknown。本地记录不是外部发布，唯一后续问题见Summary末尾，不自动执行。
