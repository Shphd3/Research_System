# Dense checkpoint动态资产：2026-11-01

一条281,431,040参数原生Dense轨迹的12个实际可读状态，覆盖0.5B–33B累计有效预测token。本轮只读分析，语言模型训练和checkpoint修改均为0。

- checkpoint_family_dense_spectral_dynamics_20261101：精确12状态路径、架构/分词器、内部token/step和实际核验的权重摘要。
- data_dense_spectral_dynamics_paired_panels_20261101：2048条几何文本，参考/评估各32768位置，另有R12同the桥接96条。
- representation_dense_checkpoint_spectral_dynamics_20261101：21个实际数组，12点主层、三点block0/3、三点语义桥接，原子缓存索引。
- analysis_dense_checkpoint_spectral_dynamics_20261101：18层位谱、原始/只旋转对齐子空间、CKA、配对拆分、126读出、36主增量及四组主图。

[Summary](../Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/checkpoint_spectral_dynamics/20261101/summary_cn.md)和[完整资产/数据说明](../Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/checkpoint_spectral_dynamics/20261101/assets_and_data_cn.md)解释用途与边界。payload留在/data/250010109/MoE_Router/experiments/20261101_dense_checkpoint_spectral_dynamics，缓存键绑定checkpoint、父模型/测点、文本位置、精度与代码。Qwen/A22缓存不作为Dense测量。

A01限定det(R)=+1，A02不虚构保存点网格。8个历史有manifest而权重缺失状态保留。记录级独立性近似、小标签集和旧H暴露仍是边界。访问与工程完成不授予新训练或科学接受，研究者接受/闭合Unknown。
