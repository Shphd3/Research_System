# 1112-层级二分路由HT与H1
- 接续 1111 A5 长续训；当前授权以 1112 执行附件为准，会议记录提供分析背景。
- 日志：research/from-attention-to-search/main/explore/1112_hier_routing/log.md。
- 执行根：/data/250010109/MoE_Router/experiments/20261112_hier_bisection_routing。

## 2026-11-11T17:25Z — 离线审计与 Spot 提交
- Summary: HT 和 H1 的 2×2 H100 Spot 启动器已提交，单卡资格通过并放行远端冒烟；两臂的正式训练均需等真实节点。
- Current work: 监督器在执行根持续更新 `status/live.json`；原生 1B 和两个可用的 A0 存档离线完成，A0-250 缺档。
- Next action: 等 30 步分布式资格和首个正式步，超过一小时仍无节点按规则加提 2×1。只有两个正式完成回执出现后才读取配对分析。
- References: 执行根 `status/提交状态_cn.md`、`status/预计分析_cn.md`、`offline/离线集中度_cn.md`；探索日志为认识记录，研究者决定 Unknown。
