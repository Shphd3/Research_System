# Thinking Card：可微负载均衡下的层增量信息路由

状态：根据研究者在 2026-08-10 的明确批准整理

上级研究方向或问题：
A16 研究稀疏 MoE 如何在维持可用专家负载的同时，不牺牲语言模型学习。本卡新增真正可微负载均衡下的长期 Router 干预，不重新打开已经完成的 A16_00 梯度审计。

现象：
Router 通常只读取 attention 后的完整归一化状态。本层 attention 刚写入、并在当前层对 Router 可见的变化与旧状态混在一起，有限容量 Gate 可能难以显式利用它。

机制猜想：
保留 native full-state Gate，同时在实际同层增量上加入零初始化低秩分支，可以在不删除已有上下文的情况下显式暴露本层新写入。可训练投影是最工程化实现；先通过表示门和专家效用门、再冻结方向的分支是最科学化实现。

最强竞争解释：
任何收益都可能来自额外低秩参数、正则化或优化几何，而不是认证增量方向的身份，因此必须有同维 Haar 随机分支。

最不确定点：
在真正可微的 Switch 风格负载目标下，两种增量分支是否改善 30B held-out next-token NLL；认证分支是否超过 Haar 对照。

会改变判断的证据：
两个配对 seed 中工程分支都优于 Native-LB，或具备资格的认证分支都优于 Native-LB 与 Haar-LB。若两个 seed 方向相反、认证门未通过或 LB 没有真实回传，则对应结论不能成立。

当前阻塞不确定性：
实现尚未构建或 smoke。认证方向也只有在 Native 的 2B、5B 或 10B checkpoint 上通过注册的 E1 表示门和 E2 专家效用门后才存在。

为什么现在需要这个决策：
固定 covariance band 没有获得功能证书。下一操作问题是：当同层增量被显式表示，并分别用端到端学习或独立认证来选择方向时，它是否有训练价值。

当前下一决策：
在可微 LB 下实现并 smoke 四个注册条件，随后从 step 0 提交全部八个任务。Certified-Innovation-LB 与 Haar-Innovation-LB 在 2B/5B/10B 首个两 seed 共同通过的 checkpoint 前保持与 Native 完全一致的休眠行为；若到 10B 仍无共同证书，两者保持休眠到 30B，科学身份比较记为 insufficient，而不是伪造认证方向。

已知来源：
- [逐层增量信息路由方法](/daily_research_reports/0810/docs/layerwise_incremental_information_routing/README.md)
- [A15_07 conditional-fine 方向设计](../../15_spectral_representation_and_functional_routing/15_07_layerwise_conditional_fine_discriminant_directions/15_07_layerwise_conditional_fine_discriminant_directions_anchor_cn.md)
- [已验证可微 LB 的 30B 执行合同](/Projects/from-attention-to-search/main/experiments/A15/15_06_online_spectral_routing_and_relay/A15_06_E05_30b_differentiable_lb_restart/protocol_cn.md)
