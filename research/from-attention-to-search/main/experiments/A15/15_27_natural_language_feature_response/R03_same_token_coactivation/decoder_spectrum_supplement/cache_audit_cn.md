# 匹配参考表征缓存审计

**找到零前向可复用的末层原始表征。** 推荐下一步读取：

`/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/relation_learning/20261015T164000Z/data/train.pt`

已登记资产为 `representation_crosscoder_relation_learning_20261015t164000z`。实际只读加载元数据确认 `hidden=(130712,1024)`、BF16，128个context；`eval.pt`为 `(65402,1024)`、64个context。均为零起始block27的residual-post、最终全局RMSNorm之前。没有计算PCA、decoder cosine或重新聚类，没有加载模型/字典权重，没有模型前向。

## 当前文件身份与接口

| 缓存 | 新鲜SHA256 | 与原manifest一致 | 表征/事件 |
| --- | --- | --- | --- |
| train.pt | `e7ff8530a006749e3811ee1f07f1de35da3cc3fc5fd5c3d78976f134d7c14f97` | 是 | raw hidden、下一token ID、完整正活动CSR ID |
| eval.pt | `43715c78f97db1ae50bdfae60a82274445e19dc5e01ff5e25f1f937d10cab004` | 是 | 同上 |

`data_routes.py`第26–27行固定A22最终checkpoint与 `/data/share/Qwen3-0.6B-Base`；第289–301行恢复14层CrossCoder及extractor；第462行保存 `raw[:,-1,:]`，对应block27原始残差。生产脚本当前SHA为 `935e0f2c0b7de3788ffe45e6fa0ab8b5c7e0073065aac43c86d6afcfe5f73d98`，与旧 `source_freeze_R1_6.json` 和 `data_source_manifest_final.json` 的冻结版本一致。完整路径、代码行与各源哈希见机器审计。

必须保留身份边界：旧缓存manifest没有独立保存Base权重SHA。生产调用 `FrozenQwenExtractor.from_model`，其源码第119–125行将 `identity_verified=False`；不能把同目录路径直接当成历史权重逐字节证明。本审计将匹配定为 **BOUNDED_SOURCE_CHAIN_MATCH**：hook、缓存字节和固定来源代码链已核查；已知A22/R03链中的Base/字典SHA可供兼容核对，但不是旧缓存独立记录的模型哈希。刚重算缓存SHA本身也不能证明历史生成模型字节。

## 独立性与可复用内容

- train与eval来自不同DCLM源文件，且与原结构图VAL源文件不同。它们是原CrossCoder TRAIN来源的既有学习缓存，不是封存TEST。本次未读取封存TEST。
- 字典训练看过这些TRAIN来源，因此不能称独立于字典训练。原文档身份和近重复独立性仍Unknown。
- 缓存保存 `feature_ptr`、`feature_ids`，**没有连续z值**。因此不能直接从该参考缓存得到z加权贡献。控制句的加权贡献可用本轮R03已存z；参考总体加权量若使用R03 moments，必须分别注明样本来源，不能伪称来自这里。
- 参考PCA需用选定训练表征重新估计一个公共均值和基；CrossCoder保存的TRAIN中心不是该参考样本的PCA均值。该计算本审计尚未执行。

## 旧谱为何不能直接当作本轮投影

旧 `analysis_crosscoder_report_spectra_20261016` 的 `20261016_raw_hidden/*raw_hidden_spectra.npz` 记录1119个按频率构造组、各自命中位置128行的中心化特征值谱；只存eigenvalues、normalized、样本行和成员，**没有特征向量**。各组输入集合/均值不同，采样秩最多127，也不是当前C03。因此不能拿它直接报告统一参考谱上的decoder投影。

旧 `analysis_crosscoder_phi_group_input_spectrum_20261016` 也是各组输入及其PC1扣除后的特征值，不提供当前共同参考基。可以复用其定义核查和数据来源，不能用旧“同频/混频”或phi分组替代本轮固定簇。

另有 `representation_crosscoder_relation_learning_eval512_20261015t164000z` 的 `data_eval512/eval.pt`，523136位置、512个context；当前strict访问通过，但本审计没有重新哈希这1.63GB文件。它已在旧谱分析暴露，不是新的语义留出。

本次strict访问检查覆盖上述四个注册ID并全部通过；访问不等于科学资格。语义标签资格由独立审计判断，下一token ID不自动是所需语义真值。
