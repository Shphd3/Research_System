# 层级语义频谱画像与显式频带路由：报告入口

原综合报告已经按科学问题拆分为两份相互独立、可单独阅读的报告：

1. [实验一：Qwen3-8B 同词父/子语义角色的层 × 频谱投影画像](01_qwen3_semantic_hierarchy_depth_and_spectrum.md)
   回答同一个目标概念作为父级或子级时，raw/white 投影是否在不同层和频带中稳定变化。

2. [实验二：Local / Relay 显式频带 Router 的 2B 与 10B 训练](02_local_relay_spectral_routing_training.md)
   回答显式限制 Gate 读取本层或第一层 H/M/T 后，路由、梯度、专家功能和 held-out NLL 怎样变化。

两份报告共同使用的结论边界是：静态表征可分性不能替代训练效用，局部梯度或路由变化也不能替代配对 held-out NLL。
