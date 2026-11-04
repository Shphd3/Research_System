派生阅读副本；原件位置：`assets/native_spectral_decoding_20261101_cn.md`。
[精确原始文件](../../sources/assets/native_spectral_decoding_20261101_cn.md)；研究修改仍回到原件。

---

# 原生谱解码资产与复算入口

主属：A15_27_05。对应R13_20261101_native_spectral_decoding的summary_cn.md、protocol_cn.md与detailed_cn.md。

实际输出登记：

- `representation_qwen3_0p6b_block27_native_spectral_decoding_20261101`：同一官方Qwen3-0.6B、同一block27 norm前接口，当前5090运行时对180篇固定文档的重缓存；不是旧缓存身份的替换。
- `analysis_a15_27_05_native_spectral_decoding_20261101`：737位置×21条件的原生解码结果、逐篇配对、参考频率与格式恢复、真实文本。

旧缓存未通过原预设重放阈值，失败与原缓存均保留。新提取没有改变模型／测点／文本，没有重拟合训练侧谱，没有训练分类器或字典。参考词频不等于Qwen真实曝光，语义层级与研究者科学接受仍Unknown。

全量执行根：`/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R13_20261101_native_spectral_decoding/`。原始逐位置概率在analysis/raw_outputs.jsonl，全部新h在data/native_h27_fresh/，绑定索引为data/native_positions.jsonl。项目只保留明确选择的图、逐文档表、固定样例和审计，见selected_evidence_manifest.json。

CPU复算：analyze.py → recovery_groups.py → validate.py → render.py；不调用模型。历史实际执行A4协议与事后A5/A6修订分开，不能把事后文本冒充输出前冻结版本。
