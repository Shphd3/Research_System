派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R04_domain_usage_20261027/token_location_diagnostic_20261028/summary_cn.md`。
[精确原始文件](../../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R04_domain_usage_20261027/token_location_diagnostic_20261028/summary_cn.md)；研究修改仍回到原件。

---

# 一页解释：领域响应更多出现在哪里？

**比较什么：同一套旧领域偏向候选，在真实留出文档、受控文本前文、句末通用目标三处是否出现。以下新增结果全部是探索性诊断。** 无新候选、拟合、模型前向、Attention或新任务。

先核对原结果：

- **已支持有限面板上的领域可读性。** SAE共享/偏向集合准确率95%/100%，CrossCoder为92.5%/97.5%；32个偏向方向均在留出保持。但CrossCoder偏向匹配随机组平均也有95.625%，有的达到100%；词袋95%。这不证明指定候选独有信息或纯概念。[四组核对表](../../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R04_domain_usage_20261027/token_location_diagnostic_20261028/tables/old_four_groups.csv) · [原图2](../../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R04_domain_usage_20261027/figures/figure2_readability_frequency.png)
- **没有支持跨家族稳定的通用目标组级响应。** 四组原确认标准均未达到，CrossCoder偏向组q=.125；DCLM频率核对一致，只代表该参考语料。[原同目标结果及区间](../../../../../../../../../UNAVAILABLE.md) · [原图3](../../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R04_domain_usage_20261027/figures/figure3_fixed_target.png)

| 原偏向候选覆盖（每套共32个） | SAE | CrossCoder |
|---|---:|---:|
| 40篇留出文档，6400个测量位置 | 32 | 32 |
| 36条受控前缀的目标之前，1062个位置 | 24 | 26 |
| 同批36个最终目标位置 | 4 | 5 |
| 目标沉默、但更早前文出现 | **21** | **21** |
| 整条受控文本都未出现 | **7** | **6** |

“覆盖”只要求至少出现一次，不是每篇都出现。36条版本来自6个家族；三处位置数量不同，不能把覆盖差直接解释为信息多少或因果。“位置限制”指读数窗口漏掉更早token，尚未分离位置与token身份。

**图怎么读：** [打开token×feature热图](../../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R04_domain_usage_20261027/token_location_diagnostic_20261028/figures/token_feature_heatmap.png)。左为SAE，右为CrossCoder；每格是某个实际token上的一个旧候选，深色表示较大重构贡献，橙框标末尾目标，黄条标领域线索句。每套固定展示8行，全部32个都在覆盖表中；F08旧反例、F09旧CC正例、F11旧SAE正例均事前固定。

两条更新：

1. **多数“目标沉默”并非整句没用这些候选。** SAE28个沉默候选中21个、CrossCoder27个中21个在更早的领域线索句出现。这支持“只看句末目标会漏掉前文响应”的位置选择限制。例如F09生物句中CC f12630在`protein`、`with`的最后层原空间贡献为35.10、42.87，到了`method`为0。普通词位置的响应仍可能由前面的术语触发，不能据此排除词面解释。
2. **位置也解释不了所有缺失。** 另7个SAE、6个CC候选在整条受控文本都没出现。旧文档高响应例中，SAE f26129常在`x/z`，CC f7383常在变量/数字；受控文本缺少这类公式写法。它们提示文本内容或格式不匹配，不能直接说缺失了领域知识。前文恢复的21个候选中，SAE11个、CC7个也只涉及1个家族，仍缺跨语境验证。[逐候选覆盖与例子](../../../../../../../../../UNAVAILABLE.md)

**最值得做的下一步（建议，未执行）：** 用独立同义改写复核这些已冻结的“前文有、目标无”候选，事前固定术语附近和其后同一普通token的读数，区分词面触发与位置选择。当前不把事后正例写成确认，更不把重构贡献叫功能重要性。

[完整token例子与缺项](../../../../../../../../../UNAVAILABLE.md) · [事前解读规则](../../../../../../../../../UNAVAILABLE.md)。
