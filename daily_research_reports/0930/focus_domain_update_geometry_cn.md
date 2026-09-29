# 自然文本更新需求的共同结构与领域特有结构

问题标识 `domain_update_geometry`；任务 ANALYSIS_DELIVERED；问题 HUMAN_CONFIRMED；设计为“已确认方向，具体操作化由本次指令委托”；结果 MEASURED_BOUNDED；核心实验 1 个。[English](focus_domain_update_geometry.md)

**授权。**研究者在 2026-09-29 明确认可领域优先的分析，要求研究共同点和领域特殊性，使用 SVD、已有 SAE atoms 并完整分析激活模式；先完成 Anchor/Protocol，必要时提交四卡 H100 Reserved，期间不再请求批准。具体数字由 AI 在此授权内固定，不冒称研究者逐项选定；未来科学解释仍由研究者决定。

**问题及边界。**固定 S7 的 33B 训练词元状态，四个预定义自然文本领域是否具有超出整体共同更新的可重复更新需求差异？SVD 结构、SAE 激活与这些差异是什么关系？观察末块注意力输出矩阵、纯自然下一词损失及有历史曝光的学术文本面板；不判断语义因果作用、长期隔离收益或 Router 性能。

**目的与完成标准。**先解释更新目标的结构，再考虑新的表征预测器。一个有界观测实验必须给出领域平均梯度留出比较，以及全部谱、激活和梯度投影诊断，包括负结果、空 atom 集合和不足分支。成功不要求低秩、领域分开或 SAE 有效。

**三个分析步骤。**①在相同文本上采集原生表征、纯 NTP 梯度和冻结 SAE 激活，以独立记录比较整体均值与领域均值的更新描述。②用 SVD 分开共同均值、领域偏离与领域内部变化，比较梯度归一化、同规模随机分组以及单目标/固定 16 目标平均尺度。③完整记录所有 atoms 的激活统计和整体模式，在 fit 半边只凭激活选共同/领域富集 atoms，再在 readout 半边测复现及 decoder 子空间对更新结构的覆盖。

**三种分支。**领域均值留出改善可复现，支持有界领域关联；合格却无改善，削弱领域作为平均更新描述的价值；精度不足或测量失败，保留未知。谱与 SAE 的结论独立，主比较不支持也必须完成。结论条件于记录、来源类别、模型和矩阵。

**下一决定。**完整证据齐备后，由研究者判断是否值得前瞻读出领域相关更新结构，还是改变语言分组/观察尺度；当前 Unknown。旧受控 Focus 与自然 NTP 预测冻结裁决不改。

[Anchor 中文](docs/domain_update_geometry/anchor_cn.md) · [Protocol 中文](docs/domain_update_geometry/protocol_cn.md)

**2026-09-29事实完成，结果文本已按用户要求审计为R2终版。** [摘要](docs/domain_update_geometry/summary_cn.md)和[完整记录](docs/domain_update_geometry/detailed_cn.md)持有测量结果与审计资格。四卡H100 Reserved任务pt-t33awf9u成功，全部注册统计交付。程序NON_SUPPORT保持，但总体方向推断因bootstrap未校准而不足；当前有限面板的领域均值描述器无增益，不等于领域结构不存在。执行和文档终版不关闭科学问题，研究者解释仍Unknown。AI建议下一问题同时考察目标组成/聚合尺度下的总领域关联与可比较目标条件下的剩余关联；目标属于任务，不预设为应消除的混杂。此建议不是已批准新实验，冻结Anchor/Protocol正文保留运行前快照。[R2审计](docs/domain_update_geometry/evidence/reasoning_audit_final.json)
