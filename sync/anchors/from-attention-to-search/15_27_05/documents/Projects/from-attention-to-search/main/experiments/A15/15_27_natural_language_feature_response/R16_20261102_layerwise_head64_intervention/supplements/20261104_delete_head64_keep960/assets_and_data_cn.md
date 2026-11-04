派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R16_20261102_layerwise_head64_intervention/supplements/20261104_delete_head64_keep960/assets_and_data_cn.md`。
[精确原始文件](../../../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R16_20261102_layerwise_head64_intervention/supplements/20261104_delete_head64_keep960/assets_and_data_cn.md)；研究修改仍回到原件。

---

# 原始数据与复算入口

执行目录：/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R16_20261102_layerwise_head64_intervention/supplements/20261104_delete_head64_keep960

- 原始逐位置候选：[/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R16_20261102_layerwise_head64_intervention/supplements/20261104_delete_head64_keep960/analysis/raw_outputs.jsonl](../../../../../../../../../../UNAVAILABLE.md)。合计207097条，含新增165825条（其中737基线）和复用保留条件41272条。每条保留前10个精确token ID、片段和概率，标明NEW_DELETE/NEW_NATIVE_IDENTITY/R16_REUSED_EXACT。
- [逐位置指标CSV](../../../../../../../../../../UNAVAILABLE.md)：原首选保持、原首选概率/排名、真实后继概率/排名/负对数概率、KL/熵、目标及前缀保留能量、干预范数。
- [全部逐层汇总](../../../../../../../../../../UNAVAILABLE.md)、[完整文档汇总](../../../../../../../../../../UNAVAILABLE.md)、[汇总区间](../../../../../../../../../../UNAVAILABLE.md)、[文档配对差异](../../../../../../../../../../UNAVAILABLE.md)。文档等权，2000次文档重采样。
- [同位置四格原始结果](../../../../../../../../../../UNAVAILABLE.md)、[四格汇总](../../../../../../../../../../UNAVAILABLE.md)、[输出类型频数](../../../../../../../../../../UNAVAILABLE.md)、[精确ID变化对](../../../../../../../../../../UNAVAILABLE.md)。词频分组不是语义粒度。
- 输入索引：[input_position_index.csv](../../../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R16_20261102_layerwise_head64_intervention/supplements/20261104_delete_head64_keep960/evidence/input_position_index.csv)。完整可见输入、原文后继与位置继承data/positions.jsonl；原文窗口data/evaluation_documents.jsonl。737/737输入前缀和causal shift核对通过；自然175篇为175个不同文档家族，the37另报。
- 28套均值/PCA及三种随机空间以只读路径复用R16的data/bases和random1031..1033.npy；没有新拟合。原参考60篇/9600位置，评估不参与拟合，训练未见性Unknown。manifest.json记录所有来源/模型/tokenizer/旧输出哈希，freeze.json冻结GPU代码和参照。数据符号链接只引用旧资产，不复制权重或改动原结果。
- 数值代码复算：CPU scripts/analyze.py → scripts/validate.py → scripts/render.py。validate使用同一挂载tokenizers依赖，不激活GPU。write_report.py仅生成首版事实草稿；已有人工核查报告时保护现有文字，不覆盖认识判断。
- GPU仅在既有授权5090spot上使用scripts/runtime.sh，再先run_gpu.py --stage smoke --rank 0，通过后分别evaluate --rank 0/1；scripts/launch.sh给出完整命令。按完整文档JSON分块恢复，不重新抽样/拟合。
- 实际执行：pt-ay14f1yi，5090-2-spot，同原镜像/SM120依赖；两卡各90篇，评估约340.63/329.96秒，峰值显存1.310/1.310GB。平台和两个rank成功完成，无训练、无新PCA、无H100。
- 核查与来源：audit/03_numerics_smoke.json、audit/validation.json、audit/manual_context_review.json、completion_manifest.json、execution_certificate.md、acp_receipts/pod日志和logs/rank0/1.log。初次CPU校验缺少tokenizers路径已用原挂载依赖修复，未安装新包或重跑GPU，原日志保留provenance。

[完整结果与认识更新](summary_cn.md) · [固定及另标后选例子](casebook_cn.md)。科学接受、闭题Unknown；没有自动扩展后续实验。
