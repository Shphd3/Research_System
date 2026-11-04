派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R14_20261102_concept_specificity_v1/assets_and_data_cn.md`。
[精确原始文件](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R14_20261102_concept_specificity_v1/assets_and_data_cn.md)；研究修改仍回到原件。

---

# R14资产与数据口径

完整输入、候选、文字片段编号和标签在[288条输入清单](../../../../../../../../UNAVAILABLE.md)。48家族，三领域各4开发、12评估；独立评估单位36。此处是长度诊断已更正的元数据视图，模型输入token及候选与实际冻结输入完全相同；原件及更正关系保留在manifest和Detailed。

模型仍为官方Qwen3-0.6B-Base，字典仍为A22的14选层共享系数，干预最后层原始坐标。谱来自旧数学／生物60篇9600位置，1024数值秩，熵有效秩281.915；物理未参与拟合，复用不算独立复现。成员频率参考65536位置，原文档映射未知。输出词频是另一份4194304个token的参考，不是Qwen真实曝光次数。

最终数据1.3，全部四个候选名称均未在本家族前文直接出现；AI语义审核与参考出处逐条保留，不称人类盲标。CPU数值路径经新开发检查后完成，GPU0；没有训练或更换模型。大缓存、权重和完整原始分数留在[执行入口](reproduce.md)。
