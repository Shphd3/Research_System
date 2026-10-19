# 10月19日：频率贡献桥梁与关系细分

[白话一页](../../../Projects/from-attention-to-search/main/experiments/crosscoder_feature_relations/frequency_contribution_relation_refinement/20261019_bridge_dispatch/one_page_cn.md) · [项目概要](../../../Projects/from-attention-to-search/main/experiments/crosscoder_feature_relations/frequency_contribution_relation_refinement/20261019_bridge_dispatch/summary_cn.md) · [完整报告](../../../Projects/from-attention-to-search/main/experiments/crosscoder_feature_relations/frequency_contribution_relation_refinement/20261019_bridge_dispatch/detailed_cn.md) · [随机及高份额文本](../../../Projects/from-attention-to-search/main/experiments/crosscoder_feature_relations/frequency_contribution_relation_refinement/20261019_bridge_dispatch/texts/all_cases_cn.md)。

本轮不训练。复用TRAIN85548、EVAL22446答案预测位置，完成4段画像、词频/上下文检查、关系复核及21名单×2评分×2split统计。EVAL此前已看过，全部为探索性。

1. 低频贡献份额与当前词片稀有程度ρ≈0.26，但平均份额仅0.108%、约84%位置为0，不能叫难知识指标。
2. 同频段内部分关系在复核中优于随机，但组人数极不平衡，分半成员不稳定，尚非可靠自然专家。
3. 原始贡献规则的低频接收率0%；校准后关系组72.22%，随机20均值70.99%。主要变化来自评分竞争，关系细分增量较小；完整输入仍混频，学习收益未测。

![实际分发](../figures/frequency_contribution_bridge_20261019T025630Z/figure4_actual_dispatch.png)

左边是输入位置负载，右边是1198个可估低频feature的平均接收率，分母不同。496个未在EVAL出现的feature保留NA。低频专家0仍平均接收1.4个最低频和196个最高频激活项，不能据此宣称学习干扰。

4/8预选词片无法构造不同R1的高低文本，另2个位置数不足；保留不换人。核心计算约4.4分钟，核验和整理另记，准确成本以[完成回执](../../../Projects/from-attention-to-search/main/experiments/crosscoder_feature_relations/frequency_contribution_relation_refinement/20261019_bridge_dispatch/completion_receipt.json)为准。

**AI建议的下一问题：接收改善能否在新留出、共同DEV预算下转成学习收益？** 本轮结束，不自动训练。旧大ZIP保持删除，资料由项目直接访问。

## 三个认识：简洁图表

[四张新图与逐图解释](../../../Projects/from-attention-to-search/main/experiments/crosscoder_feature_relations/frequency_contribution_relation_refinement/20261019_bridge_dispatch/redraw_three_insights_20261019/README_cn.md)。前三张来自新无训练分析；最后一张单列旧T_S1第一轮、两种子与已有对话重采样区间。观察、允许的结论和对设计的影响分开写，不把接收改善当作学习收益。

### 少见token对照：结论具体化

[四段对照图与精确口径](../../../Projects/from-attention-to-search/main/experiments/crosscoder_feature_relations/frequency_contribution_relation_refinement/20261019_bridge_dispatch/redraw_three_insights_20261019/token_rarity_contrast/README_cn.md)。tokenTRAIN计数1对≥5时，最低频段平均末层贡献份额为0.266%对0.047%（5.61倍），B2/B3/B4约1.22/1.01/0.99倍。不是feature命中率，绝对份额仍小；中间组不严格单调。仅对照已存统计，不重新推理、训练或估计区间。
