# 待讨论：归一化路由与学习闭环

**阅读副本，来源项目：** `/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_21_activation_to_expert_learning/20261019_normalized_learning`。事实冻结于本次交付；不授予下一轮执行权限，不替代研究者判断。

先读 [一页简版](one_page_cn.md)，再看 [完整报告](detailed_cn.md)、[逐图说明与术语](figures_cn.md)、[实际文本与评分项](text_profiles_cn.md)。

- 20/20完整训练、20/20功能与谱、8/8目标适配。
- S1改善目标接收；主学习联合门槛未通过；无安全目标归属。
- tables携带全部条件/逐feature/逐步精选日志/实际q/适配结果。evidence携带小标量全谱、终点逐位置NLL及核验回执。
- 原Anchor/原v1/整合Protocol与用户补充均保留。code/config是执行来源副本；复算仍依赖清单中的base、字典和原缓存，不是开箱即训授权。
- 不携带raw hidden/z、模型权重、大响应矩阵或原始TensorBoard事件；其确切地址见source/checkpoint/asset清单。阅读图表自包含。

任务pt-falmqs6x平台SUCCEEDED；执行根 `/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/normalized_route_learning/20261018T173143Z`。首次工程失败回执保留。没有commit/push。
