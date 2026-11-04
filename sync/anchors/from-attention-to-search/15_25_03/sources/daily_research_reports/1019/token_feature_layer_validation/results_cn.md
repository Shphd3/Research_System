# 大样本与跨层：低频token是否对应低频feature？

[一页白话](../../../Projects/from-attention-to-search/main/experiments/A15/15_22_frequency_contribution_relation_refinement/20261019_large_token_layer_validation/one_page_cn.md) · [概要和完整来源](../../../Projects/from-attention-to-search/main/experiments/A15/15_22_frequency_contribution_relation_refinement/20261019_large_token_layer_validation/README_cn.md)。

完成DCLM 1,048万位置窗口的发现／复核及原SFT 14层对照。逐feature的总体频率趋势存在（DCLM≥20已知token命中项等权ρ0.339），但当地最低频段逐输入位置的联系很弱（ρ0.006），tokenID等权反向（−0.119）；不能将这三种单位混在一起。14层近似一致来自同一共享z上的decoder幅度画像，不是独立层feature验证。旧SFT低频池迁到DCLM只25项仍在当地最低频段。

实际核心CPU计算314.8秒、峰值RSS4.16GiB；没有新推理、训练、GPU任务、路由更改、ZIP或Git操作。四图、13表、原输入绑定与完整中文解读位于项目。DCLM同bin、原文档独立性未知；没有把较大DCLM样本当成扩大SFT独立验证。待研究者讨论，不启动下一实验。
