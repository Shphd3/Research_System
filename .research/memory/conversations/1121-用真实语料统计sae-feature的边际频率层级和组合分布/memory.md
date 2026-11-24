# Conversation Memory: SAE 真实语料分布

Conversation name: 1121 SAE 真实语料中的共同特征与长尾组合（01a1fc58-6256-7562-8130-72fd0629cdd7）
Processed by: Codex (harness: Codex desktop; model: gpt-6.2-astra)
Created at: 2026-11-21T05:06:14+00:00
Latest update at: 2026-11-21T09:44:34+00:00
Continues from: none
Environment: repo=/data/250010109/Research_System, exec=/data/250010109/MoE_Router/experiments/1121_sae_corpus_model, receipts=/data/250010109/Research_System/assets/checks

## 2026-11-21T05:06:14+00:00 -- 留出观测与条件搭档

- Summary: 已完成 E16 教师的原文对齐、频率及 HIFER 图、文档与等长窗口、条件组合和词形对照，以及换上下文和种子重分复核。研究者对模型变更的决定为 Unknown。
- Current work: 中文报告与离线图解位于执行侧。三条登录对话正文和独立 11/20 会议逐字稿未取得；在报告中逐项记录。
- Next action: 讨论数据模型时先从执行侧报告开头和图 3/4 的留出对照复核。新训练、干预或正式研究状态变更需研究者另行决定。
- References: /data/250010109/Research_System/research/from-attention-to-search/main/explore/1121_sae_corpus_model/log.md 保存跑前分支、结果与资产 ID；/data/250010109/MoE_Router/experiments/1121_sae_corpus_model/report.md 给出读稿和数值；/data/250010109/MoE_Router/experiments/1121_sae_corpus_model/run.sh 是复跑入口；/data/250010109/MoE_Router/experiments/1121_sae_corpus_model/index.html 是图解。

## 2026-11-21T09:20:31+00:00 -- 对话命名与交付包清理

- Summary: 对话已命名为《1121 SAE 真实语料中的共同特征与长尾组合》。E16 实测中，整篇和 256-token 窗口达到 95% 覆盖的 feature 分别为 43/30,000、33/30,000。条件搭档模型是 AI 建议，研究者决定为 Unknown。
- Current work: 已按研究者要求删除执行目录中的 sae_feature_results.zip，并核实该路径已不存在。报告、离线 HTML 与逐 feature 表可直接读取。
- Next action: 后续复查本轮结果时，从报告和图解进入。
- References: /data/250010109/MoE_Router/experiments/1121_sae_corpus_model/report.md 提供口径及结果，/data/250010109/MoE_Router/experiments/1121_sae_corpus_model/index.html 提供逐 token 实例。

## 2026-11-21T09:44:34+00:00 -- 句末读数、搭档图与 Zipf

- Summary: 已完成逐句原文对齐、严格句末幅度、词元搭档图和频率排名对照。
- Current work: 按用户要求交付独立离线 HTML；跨措辞概念解释为 Unknown。
- Next action: 复核句末读数时优先使用精确右边界子集，背景模型的功能主张仍需另行判断。
- References: /data/250010109/MoE_Router/experiments/1121_sae_corpus_model/sentence_study/index.html 与本项目 1121_sae_corpus_model/log.md。
