# 给实验 Agent 的启动 prompt

请直接实现并完成在线路由正则实验，不要停在规划或提交任务阶段。

工作目录：`/data/250010109/Research_System`。

先读取：
1. `.research/memory/conversations/sae-balanced-routing/memory.md`；
2. `Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E20_sae_flat_router_eight_task_mixed_training/A6_online_regularized_router/protocol.md` 全文；
3. 协议引用的 A5 冻结代码、配置和 task-only 基线，只读必要部分，不重做旧文献或审计流程。

我接受这份协议的默认实现与预算，并授权你完成实现、必要的短程 smoke、full run 提交、监控、完整内部评测与结果整理。请在同一 protocol 中记录这次授权并冻结配置；如旧 Anchor/Focus 仍只描述冻结路由，可做与本次明确范围一致的最小更新，保留旧证据，不自行填写新结果或机制结论。无需逐块再次询问确认。

范围：SAE-A、GMM-A、SAE-B、GMM-B，四个条件各 seeds 17/29/43、512 更新，共 12 条新训练；路由器和专家均在线训练，从对应 task-only 相同初始状态开始，只改变结构正则。按协议固定 lambda=.1、B margin=.5 和成对损失归一化；GMM 按协议只在训练词元状态上拟合一次后冻结。复用兼容的 task-only，不加 random、Dense、参数扫描或 A+B 条件。

实现放到协议指定的新执行目录，旧运行、检查点和评测数据不得覆盖。四张 H100、累计最多六个节点小时（24 GPU 小时），沿用协议的镜像与资源设置；不要影响其他任务。保留必要的梯度/掩码/初始化等价性检查，各新条件八步 smoke 通过后立即 full run，不再重复旧聚类审计、离线路由训练或外部 benchmark 资格流程。若基线不等价或需要超预算，说明具体差异再问；普通实现错误自行修复。

目标是北京时间 2026-09-09 09:00 前给出：12 条完整训练、完整内部测试、与三条 task-only 的逐种子和均值对照、按任务结果表和 loss 曲线。全量外部生成 benchmark 不在本次过夜交付范围。32 步后用实际吞吐估算完成时间；若有延误风险主动通知，不暗中减少种子、更新或测试覆盖。使用支持的监控/唤醒机制持续推进，完成、失败、需我处理或预计延误时通知，不要反复报告无变化状态。

完成后写 summary.md、detailed.md，并更新该会话 memory；只把数值和证据边界写清，机制判断仍待我确认。不要 commit、push 或修改无关任务。
