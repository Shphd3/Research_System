派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R14_20261102_concept_specificity_v1/protocol_cn.md`。
[精确原始文件](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R14_20261102_concept_specificity_v1/protocol_cn.md)；研究修改仍回到原件。

---

# R14 冻结协议中文导读

已获本轮完整前向、分析、修复与报告授权，无新模型或分类器训练；最多两张5090 spot、优先一张。正式操作合同见[protocol.md](protocol.md)。

48概念家族，三领域各4开发、12评估；288前缀，216评估前缀但只有36独立评估家族。每家族上位U、错误上位V、同层A/B，宽泛／指向A／指向B各两种措辞。所有完整答案与结束句号逐片段评分，不含结束符。

主要终点为完整模型的对称线索区分量减去频率组删除后的量；同时比较三种随机同成员数组和逐评分位置等扰动范数。J=[r(A线索)-r(B线索)]/2，r为完整候选A与B的对数概率差；宽泛基线在J中消去，因此gA、gB和宽泛偏好同时报告。上位U-V单独报告，不能将两个任务绝对降幅相减宣称细语义专属。

按家族先平均措辞、再分域平均，总体三域等权；4000次配对家族重采样。全部对照和谱段条件落在conditions.json，不按结果改样本或阈值。当前资料是AI语义审核，并非人类盲标；两种全局模板不构成独立模板泛化。
