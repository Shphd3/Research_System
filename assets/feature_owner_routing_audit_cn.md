# CrossCoder 分组到实际分发：诊断资产

[English](feature_owner_routing_audit.md)

资产 `analysis_crosscoder_feature_owner_routing_audit_20261018t143950z` 登记本轮已完成的 **CPU 缓存诊断**，不代表新训练模型或可上线 router。父缓存为 `representation_crosscoder_frequency_interval_moe_20261018t103820z`；基座、字典、tokenizer 与来源数据身份仍绑定父资产和本次条目。本轮没有模型推理、GPU、训练或新增训练检查点。

[用户原 Anchor](../Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_19_feature_group_to_actual_dispatch/15_19_feature_group_to_actual_dispatch_anchor_cn.md) 与 [用户原 Protocol](../Projects/from-attention-to-search/main/experiments/A15/15_19_feature_group_to_actual_dispatch/20261018_routing_audit/protocol_cn.md) 保留设计权威。[执行目录](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/frequency_interval_moe/20261018T103820Z/routing_audit_20261018T143950Z) 保存实际表、数组、文本、图、代码及三个生产回执；登记绑定其 hash，不改旧缓存或旧资产科学状态。

实际产物包括：TRAIN 130,712／EVAL 65,402 位置上 A/B1/B2 的逐 feature p/a/q/富集及分母和 NA；964 个低频目标 × 962 个原高频伴随项的计数；评分分解与仅把 C 评分项置零的虚拟去向；三个 TRAIN 冻结案例的12张文本卡；27个固定跨负责专家的共现对；200次上下文块描述性重采样；四幅 PNG/SVG/PDF 图。A 两种子相同分发只计一次。虚拟评分诊断不修改原路由，也不能证明学习收益。

[本次限定 strict-access 快照](checks/2026-10-18_feature_owner_routing_audit_20261018T143950Z.json) 只检查新产物与父缓存，不是全库重查、完整加载认证、科学批准或新执行授权。EVAL 已被查看，字典训练见过来源语料，原始文档及近重复独立性未知。学习收益和容量改善仍未检验。
