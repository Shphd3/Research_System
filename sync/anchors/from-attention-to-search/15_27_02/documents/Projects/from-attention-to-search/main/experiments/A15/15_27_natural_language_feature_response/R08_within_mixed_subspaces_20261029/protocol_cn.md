派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R08_within_mixed_subspaces_20261029/protocol_cn.md`。
[精确原始文件](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R08_within_mixed_subspaces_20261029/protocol_cn.md)；研究修改仍回到原件。

---

# R08执行协议

用户已授权本轮固定范围执行，无需逐步审核。主问题、四种解释及禁区与Anchor一致。

复用384条R07文本和24/12/12家族分割，只补必要早中层和共享z，同一次前向核对最后层，总新增不超过384。真实接口为零起算block1/13/27 residual-post，A22仍为14层联合输入，不更改门控。

发现集拟合各域/混合PCA，保留原尺度；k=4/8/16/32。重复200次家族分半，与同样本量跨域分半和200次随机子空间比较；分半范围为划分敏感性，不冒充总体置信区间。200次家族重采样重拟合给逐项95%区间，完整记录所有k和两种结尾。单结尾分半每域24样本，32维不可估。无正式显著性/等价性判断。

协方差统一除以n，验证混合=域内平均+均值差外积/4，报告混合前k维内两项比例。留出均值差只投到发现固定空间。另存开发/留出的固定空间方差保留量。

UMAP发现拟合、其余transform；cosine，邻居15，min_dist=0.1，主种子42、辅助17/73，500epochs，transform_seed42，单线程；不按图挑参数。零向量明确标缺。

数据已看过，全部为探索性。缺资产仅停止依赖项，不换对象；不训练模型/字典、不新增资源或任务、不删除、不新增routing/聚类。完成六类图与完整记录后停止。完整公式、种子、路径、校验和解释规则见同目录英文协议及config.json。
