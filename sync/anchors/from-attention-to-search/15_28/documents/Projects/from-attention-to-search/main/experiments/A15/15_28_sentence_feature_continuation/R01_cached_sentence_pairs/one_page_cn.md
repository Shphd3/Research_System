派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_28_sentence_feature_continuation/R01_cached_sentence_pairs/one_page_cn.md`。
[精确原始文件](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_28_sentence_feature_continuation/R01_cached_sentence_pairs/one_page_cn.md)；研究修改仍回到原件。

---

# 一页结果：句内 feature 延续与旧图关联

**问题：前面激活的坐标，后面如何再次出现，是否超过无关背景？** 每个 token 有自己的稀疏活跃集合；一句话中既有多处重复的坐标，也有只在局部出现的坐标。不同字典分别统计，坐标编号没有预设语义标签。

**本轮认识更新：同坐标延续获得有界支持；旧图的高覆盖尚不能证明关联坐标替换。** 非重复词面条件下，近处真实减对照的全频差值约为 20–27 个百分点，16–31 token 处约为 7–11 个百分点。旧图正向覆盖在真实和对照中都接近 99%；固定共同消失的源成员后，严格匹配条件下的正向差值全部为零。

这些结论只覆盖可匹配子集。严格匹配率为 SAE 2.19%、CrossCoder 1.48%，约 84% 的目标是 `the、and、of、a、with`。64+ 无主比较匹配；SAE 的旧图接口不合格。结果不证明因果传递、信息完整保留或语义提升。

先读 [完整结论与认识更新](summary_cn.md)，再看三类图：

1. [数学热图](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_28_sentence_feature_continuation/R01_cached_sentence_pairs/figures/figure1_math.png)／[生物热图](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_28_sentence_feature_continuation/R01_cached_sentence_pairs/figures/figure1_biology.png)：横轴 token、纵轴坐标，深色为激活。常出现的 24 行不能代表所有成员。
2. [同坐标延续与距离](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_28_sentence_feature_continuation/R01_cached_sentence_pairs/figures/figure2_distance.png)：重点看下方紫色“真实减对照”，同时看区间与文档块数。
3. [旧图覆盖与距离](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_28_sentence_feature_continuation/R01_cached_sentence_pairs/figures/figure3_distance.png)：正反向分开；接近 100% 的原始覆盖不代表额外句内联系。[实际旧边示意](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_28_sentence_feature_continuation/R01_cached_sentence_pairs/figures/figure3_sentence_edges.png)。

[两个实句及最弱例的逐项解释](summary_cn.md#两个真实例子与一个弱例) · [完整证据、脚本和缺项](detailed_cn.md)。严格“三项均非正”的反例未找到，未补造。研究者机制判断和问题关闭仍为 Unknown；本次仅本地保存与同步，未 commit/push。
