派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R15_20261102_natural_phenomena_output_geometry_v1/assets_and_data_cn.md`。
[精确原始文件](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R15_20261102_natural_phenomena_output_geometry_v1/assets_and_data_cn.md)；研究修改仍回到原件。

---

# R15资产、数据与术语

600篇源网页、557站，300发现/150开发/150验证；每页128位置，257—512token连续前缀。技术词组不是领域金标。来源缓存可能用于A22训练，不能声称训练外或Qwen未见。

h是block27输出、final norm前；y是真实norm后。两套新谱各用发现38400位置逐坐标均值，不能混号。旧60数学生物谱另命名历史参照。A22共同读取14层，冻结TRAIN均值/RMS与阈值；那套均值不等于新PCA均值。

完整输入与逐位置可见前文、分词器片段编号、来源、稀疏系数和h/y在[执行目录](../../../../../../../../UNAVAILABLE.md)。可读[文档索引](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R15_20261102_natural_phenomena_output_geometry_v1/evidence/document_source_index.csv)、[来源长度](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R15_20261102_natural_phenomena_output_geometry_v1/evidence/source_and_length_coverage.csv)、[解释定义](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R15_20261102_natural_phenomena_output_geometry_v1/evidence/phenomenon_definitions_v1p2.json)和[Manifest](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R15_20261102_natural_phenomena_output_geometry_v1/manifest.json)供离线读者核对身份。文字片段编号不是feature编号；当前片段可能不是完整词；解释不用后文补全。

标签执行器为不读取激活的Python规则；规则由本对话Codex/GPT-6助手依据任务和发现卡提出，精确后端修订未知，并非人类盲标或独立语言模型标注。验证标签不接收分数或谱位置。原始源文只作语料，不作为科学或社会事实的权威引文；网页质量与来源混杂是结果边界。
