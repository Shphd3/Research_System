# 图1：组内频率差异

1. 统计对象：固定发现侧 D 得到的全部 186 个非单元素关系组，以及逐组匹配的随机组；186 组均满足本次复核资格，未使用旧的 142 组合格子集。
2. 计算方法：对每组成员的验证侧 V 激活频率取 log10，计算总体标准差（ddof=0），再对组等权平均；随机组与对应关系组大小相同，D 侧平均 log10 频率相差不超过 0.1 dex，每组先对匹配抽样取均值，再对 186 组等权平均。
3. 实际观察：关系组为 0.353310533，匹配随机组为 0.604781172，前者小 0.251470639；图中只画两根柱，无误差条，柱高不是 186 组标准差的合并计算。
4. 推断边界：这说明当前关系分组的 V 侧组内频率更接近，但该匹配对照没有复刻 phi 选边及完整建图过程，因此不能排除 phi 对频率相近组合的选择偏好，也不能推出语义组合或共同学习收益；检验该替代解释需另看完整流程的固定边际命中数随机化结果。

来源：`/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/relation_learning/20261015T164000Z/structure/full_repair_summary.json`、`/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/relation_learning/20261015T164000Z/structure/full_group_controls.csv`；对应列 `observed_strict_SD` 和 `meanmatched_strict_SD`。

# 图2：预测损失

1. 统计对象：关系、频率、匹配随机三种已有分发下的 3 个配对种子，固定低频 feature 条件验证损失；细线是种子，粗线是算术均值，虚线是冻结原模型。
2. 计算方法：低频 feature 名单由 D 侧可靠 feature 频率最低四分之一预先确定（3916 个），仅估计固定学习评估缓存中至少命中 20 次的 3737 个；先对每个 feature 激活位置的真实下一个 token 交叉熵求均值，再对这 3737 个 feature 等权平均，横轴为累计有效预测目标曝光（最终 1,566,720），各 feature 可共享文本位置。
3. 实际观察：原模型为 2.439615 nat；最终关系、频率、匹配随机三组种子均值分别为 3.358713、3.342884、3.352730 nat，三者都高于原模型，本轮关系分发未显示预定的低频条件损失收益。
4. 推断边界：这里的“低频”修饰 D 侧 feature 的激活频率，并非输出 token 频率或知识准确率；结果限于已有冻结模型、终端适配器、分发和训练预算，不能据此否定所有同频学习方案。

来源：`/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/relation_learning/20261015T164000Z/analysis_outputs/learning_metrics.csv`；绘图读取 `low_loss`，总体损失单独保存在 `overall_loss_table.csv`，未混入此图。
