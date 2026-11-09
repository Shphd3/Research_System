# 资产：A15_27 R02

主接口沿用R01：official Qwen3-0.6B BF16 eval/no-grad/SDPA，原生E16 FP32 ReLU Top32，hook为零起始27层post-attention归一化后的实际MLP输入。编码器不作输入归一化或预减decoder偏置。原始贡献幅度为z乘保存decoder列L2范数；偏置另存，向量抵消使其不能称解释方差比例。

本轮重新计算模型、字典、tokenizer与loader哈希并匹配记录。[机器资产审计](provenance/asset_audit.json) 和 [原输入当前严格访问](provenance/input_access.json) 保存完整路径与环境。模型SHA256为cd2a512003e2f9f3cd3c32a9c3573f820bb28c940f73c57b1ddaa983d9223eba；SAE为e4e2049aced8ba9a3b043bbb2b3308b497b7ec22f107531e37197873ee545b65。

两项实际新输入已登记且[访问通过](provenance/new_input_access.json)：data_natural_language_feature_panel_r02_20261026（12情境/120前缀，最长139token）与data_e16_fp32_reference_windows_r02_20261026（固定1024个DCLM TRAIN窗口，每窗256，前16只作上下文，245760频率位置）。参考将用同父模型、hook和FP32 SAE重新计数，补齐旧参考精度与历史父模型缺口；首次前向前仍NOT RUN，只估计这套有限窗口的频率。

已有配套CrossCoder可用，单独完成审计：A22 final14层/F16384，以保存TRAIN均值/RMS归一化14个residual-post输入，联合编码一个共享z；严格保存分数阈值0.051281172782182693不是每tokenTop256。每层原hook贡献幅度为z_f×rms_l×decoder列范数，不能称各层独立激活。[当前审计](provenance/crosscoder_asset_audit.json)含新算模型/字典/源bin/cache身份。固定旧缓存行0–7已实际join可见前缀，无新前向；它们只是同一context的8位置，不是8文档。[对象对照](object_comparison_cn.md)保持编号与E16不同，不由此验证层间生成链或Q1–Q3。

没有新训练、资源申请、干预或封存TEST访问。每阶段仍须本地重构/重放/前缀数值资格；旧验证不替代新测量。
