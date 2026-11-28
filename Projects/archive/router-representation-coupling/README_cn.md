# 路由—表征共同学习：梯度反馈对照

> **2026-10-30 存储更新：** 研究者要求清理A3普通router与detach两臂模型。24个权重、续训状态及RNG文件已删除（20.393929 GiB）；代码、配置、日志、manifest和历史结果保留，共同随机初态保留。两臂现不可加载评估或续训，后续重点转向新的MoE训练。历史训练完成与NOT RUN判断不变。[逐项删除记录](/data/250010109/MoE_Router/experiments/20261006_router_representation_coupling_balanced/storage_cleanup_receipts/20261030T154131Z/README_cn.md)。


研究者委托的独立临时项目。**共同均衡双臂均完成全预算并SUCCEEDED，终点保存及监督退出正常。A匹配训练CE略低，B均衡项更低；主终点后测NOT_RUN，事实与边界见当前Summary。**

- [当前Summary](main/experiments/router_representation_gradient_feedback/summary_cn.md)：事实、决定性证据与边界。
- [研究路线](main/roadmap_cn.md)、[唯一Anchor](main/problem_anchors/router_representation_gradient_feedback/anchor_cn.md)。
- [当前训练Protocol A3](main/experiments/router_representation_gradient_feedback/protocol_cn.md)：用户本次重新训练/监督及共同均衡条件覆盖原零辅助项、不监控安排。
- [冻结后测合同](main/experiments/router_representation_gradient_feedback/analysis_protocol_cn.md)、[读取1002后的AI分析思路](main/experiments/router_representation_gradient_feedback/analysis_notes_20261006_cn.md)。
- [完整执行记录](main/experiments/router_representation_gradient_feedback/detailed_cn.md)：新条件与原零均衡失败历史分开。
- [原委托请求](handoff/researcher_request_cn.md)、[原执行prompt](handoff/execution_prompt_cn.md)：历史权限；当前修订由Protocol A3持有。
- [English](README.md)。

执行对话1005-路由表征共同学习：梯度反馈对照执行，thread01a10b5e-939f-7302-ab6f-bac7b48758d9，已核验模型gpt-6.1-sol/high。新代码/raw/checkpoint在/data/250010109/MoE_Router/experiments/20261006_router_representation_coupling_balanced；原执行root保留不变。本文仅导航，本项目仍为本地临时项目，未commit/push或发布。
