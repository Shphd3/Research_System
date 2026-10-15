# 2026-10-08 组会与局部更新审计

[English](README.md) · [每日索引](../README_cn.md)

先读唯一口述入口：[共享参数局部更新：一分钟组会版](meeting_report/meeting_brief_local_update_cn.md)。按目的、模型、测量量、假设、结论、实验数据分析排列，并保留可连续讲的一分钟稿。

[完整版](local_update/full_report_cn.md)给出闭环推导、各条确定认识及边界，再展开受控任务、自然文本、SAE与新增梯度成分审计。用户要求的热力图为主，drawing_prompt三图为辅助证据。

[数据、图与复现入口](local_update/README_cn.md)包含PNG/SVG、小型CSV、脚本、源文件hash和审计回执。新计算复用冻结缓存，没有新训练、模型前向或GPU任务。正式Focus、Anchor、原Summary与裁决保持其所有权。

H2独立候选测试：[SAE相似token的真实误差信号是否同向](candidates/sae_error_signal_alignment/README_cn.md)。研究者授权构建候选Anchor/Protocol并在4卡H100 reserved测试S7fresh和Qwen3-0.6B-Base；与上述报告的缓存分析分别记录。

该候选已完成两模型测量、注册分析与三组PNG/SVG：[有界H2结果](candidates/sae_error_signal_alignment/summary_cn.md)。总体平均优势为正，但不同真实下一词分层的优势转负，原生近邻更好；不得只转述正的总体均值。
