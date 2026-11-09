# 图2补图：完整样本活跃并集

冻结主图的24列只覆盖各实例0%–54.2%的低频份额。主图、原样本、列规则及完整统计均保留，不根据本轮结果改选候选。

为让实例可读，新增此事后展示补图：仍使用冻结的8个来源位置，将它们原生z>0的全部低频成员取并集，共67个，按feature编号排序；不按贡献大小、K80或领域关联选列。所有14接口使用同一组列，前7/后7均值同色标。完整并集覆盖每行全部份额，已核验和为1。

![完整活跃成员](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R05_distance_attention_20261028/low_frequency_concentration_20261028/figures/aux_full_active_member_heatmap.png)

它解释这8个实例“谁在贡献”，不是新增验证、重聚类或统计支持。全量领域比较仍使用全部4469维，未因补图改变。实例每行前5成员ID及份额已在[原完整成员表](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R05_distance_attention_20261028/low_frequency_concentration_20261028/tables/display_case_top_members.csv)中。无新前向或模型修改。
