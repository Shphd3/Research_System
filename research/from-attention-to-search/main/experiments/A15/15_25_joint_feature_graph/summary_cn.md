# 特征关系分析与候选学习对象：阶段一总结

## 目的

检查联合特征关系能否在发现／复核侧保留，并准备可读的候选学习对象。共享／分离学习效果留待后续设计。

## 模型

最终14选定层、16384特征CrossCoder，冻结Base、完整TRAIN阈值和归一化。完整10,485,760位置，128上下文成块、种子20261014；发现5,238,097、复核5,247,663位置。完整稀疏激活已保存，16384个命中次数与原最终验证逐项一致。

## 假设

共同主题、词汇、格式、上下文及高频背景都是待讨论解释；组成列表是统计代理，不是因果组成。

## 实测结果与认识变化

发现原始边214,711，复核通过206,136（96.01%），失败8,575；复核约简后146,947条边。正式池120,380,886对，单次搜索交付4对：

| 特征A／B | J发现／复核 | 复核组成列表大小A／B | 复核both位置数 |
|---|---|---|---:|
| 1／17 | 1／1 | 8／8 | 2 |
| 1／242 | 1／1 | 8／8 | 245 |
| 0／3 | 0／0 | 32／10 | 0 |
| 0／4 | 0／0 | 32／9 | 7 |

已得到可复核、可定位的统计对象。但两对高J的8个共同组成项中，7个属于Top10高频节点（87.5%）。逐个删除Top10后四对J均未变，仍不能排除多个背景节点共同支配。**高组成列表重叠不等于两个特征经常共同激活，也不等于内容相似。**

## 分析、限制与下一步

边先复核再约简；正式候选四个组成列表均非空。已交付16幅局部图、14层热图、候选表及118条按候选对去重文本，保留随机／高激活标签。0／3无both文本；1／17只有2例，按实交付。

同bin复核，原文档与近重复独立性未知；VAL曾用于训练评估。四对共享两个锚点，频率未匹配，不是独立重复。解码幅度不是因果贡献；低频特征不等于难学内容。第28层FVE86.4722%，替换CE增加0.305962nats。

AI建议下一步：共同核查随机文本、背景项及层间解码轮廓，先讨论组成列表能否作为内容关系代理，再决定后续学习比较对象。**阶段一交付后停止；未启动共享／分离专家、MoE或CrossCoder训练。**

正式主动计算及交付计数核验合计10.51分钟（含首次失败41.22秒），上限220分钟。记录的新增磁盘峰值43.05GiB，CPU RSS峰值11.41GiB。

[候选指标](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/feature_relation_phase1/20261013T173130Z/candidate_metrics.csv) · [文本](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/feature_relation_phase1/20261013T173130Z/pair_examples_cn.md) · [局部图与热图](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/feature_relation_phase1/20261013T173130Z/figures_cn.md) · [背景敏感性](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/feature_relation_phase1/20261013T173130Z/sensitivity.json) · [完整指标](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/feature_relation_phase1/20261013T173130Z/pair_metrics.json) · [失败原因](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/feature_relation_phase1/20261013T173130Z/graphs/edge_review_summary.json)
