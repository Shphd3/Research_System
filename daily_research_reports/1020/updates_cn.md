# 逐轮认识更新（2026-10-20 起，临时研究迭代）

每轮更新先给结论与边界，再给证据与下一步。数字来自 `Projects/dxy-local-research/`
下的实验记录；解释均标为假设或 AI 建议，科学判断归 Dxy。

## 更新 1（13:10，环境与认识基线）

结论（边界：以下为阅读综述与计划，尚无新实验证据）：
1. 项目已更新到远端最新（`234aba8`，NTP 迁移记录）；git 曾因 Windows 路径过长误报
   20+ 文件"被删除"，实际文件完好，已用 `core.longpaths=true` 修复，无内容丢失。
2. 三个本地每日文件夹（0921、1014/candidates、1017，约 220MB）按你的决定**不提交**，
   已同步到 `Projects/dxy-local-research/sources/daily_sync/`（本地 Projects/* 不入 Git），
   原位置保留未跟踪。
3. 已通读两份 1019 指导记录与 feature(7).pdf，形成材料综述（学长内容在前、Dxy 在后）：
   `Projects/dxy-local-research/main/research_notes/source_synthesis_20261020/synthesis_cn.md`。

当前认识（AI 建议，待你确认）：
- 频率互斥分发的负面结果有三个可区分的竞争解释：互斥切断 common 复用（导师 H2）、
  分发质量差（最优 expert 预测仅 34%）、贡献竞争天然偏高频（你 1019 的输入侧观察）。
- 三者可以用同一组 toy 实验区分：Zipf 频率合成 feature + common 成分，对照
  dense / 频率互斥 / 频率+common 复用 / 随机分发 / 恒杰式 rank-one+residual。
- 判据已预注册在 `main/experiments/T01_common_reuse/protocol_cn.md`：若"频率+common"
  在低频段显著优于"频率互斥"且高频不退化，支持 H2；若无差异，H2 被削弱。

进行中：T01 toy 实验（本地 GPU，RTX A1000）与学长研究线的深度阅读已交给两个子智能体，
结果回来后给更新 2。
