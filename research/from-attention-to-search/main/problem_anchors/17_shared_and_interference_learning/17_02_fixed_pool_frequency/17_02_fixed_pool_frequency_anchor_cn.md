# A17_02：固定数据池的呈现频率与共享学习

[English](17_02_fixed_pool_frequency_anchor.md) · [A17](../README_cn.md)

问题标识：`fixed_pool_frequency_shared_learning`。研究者在北京时间 2026-10-10 激活独立频率 Anchor/Protocol，选定直接更新末层 Attention `o_proj`，LoRA 留在上一阶段作容量对照，并授权 Smoke → Full、监督到完成。机制解释和问题关闭仍由研究者判断。

`question_state=HUMAN_CONFIRMED`；`design_state=USER_ADOPTED_FROZEN_IMPLEMENTATION`；`result_state=MEASURED_STATISTICAL_BRANCH`；`task_state=FULL_COMPLETED`。

## 1. Problem Definition

固定 B 呈现 200 次，把 A 从 200 次增加到 800 次：A 与 B 按相同规则预测，或者按不同规则预测，是否对 B 的独立答案损失产生不同影响？FIRST 取首项，LAST 取末项。规则提示可见，模型可以同时正确完成两者。这里频率是固定数据池的呈现次数，不是增加不同内容。

上游目的，是解释有限资源下共享参数的学习帮助与损害。本实验检验呈现策略与规则关系的交互，不预设逻辑冲突。另设同总答案预算的分配比较。可靠正/负交互支持继续针对方向查机制；有界的实际无效限制该载体上的解释。数据、数值或完整性不足则保留未知。表征与架构效用属于后续不同问题。

## 2. Physical Priors

待验证的工作假设：多练相同规则 A 可能提供可复用练习，不同规则 A 可能需要另一种选择操作。强竞争解释是额外训练只增强词表/读列表能力，或者 FIRST/LAST 初始难度不同。因此交换 B 的规则，采用内容组互斥、生成方式相同且位置与答案边际精确均衡的 A/B 池。只更新一个投影将结论限制在这种学习容量上，不证明完整模型必然冲突。

## 3. Falsifiable Hypotheses

冻结双侧假设：独立训练种子上的交互中位数超过实际阈值，方向可正可负。竞争解释是交互落在 ±0.01 nat/答案内。正交互表示“异规则减同规则”的损失差随 A 次数增长；它可能仅意味着帮助较少。B-only 另测额外训练的净后果；同预算对照另答分配问题。

## 4. Mathematical Model

模型读完可见规则和列表，在答案处预测一个正确词元。损失是全词表交叉熵，单位 nat/答案。\(L_{s,r,n,p}^{q}\) 表示种子 s、B 规则 r、A 次数 n、未见面板 p、关系 q 下，完成 200 次 B 后的 B 平均损失。每个种子的唯一主值为

\[
I_s=\frac{1}{4}\sum_{r\in\{\mathrm{FIRST},\mathrm{LAST}\}}\sum_{p\in\{\mathrm{order},\mathrm{combination}\}}\left[(L_{s,r,800,p}^{\mathrm{different}}-L_{s,r,800,p}^{\mathrm{same}})-(L_{s,r,200,p}^{\mathrm{different}}-L_{s,r,200,p}^{\mathrm{same}})\right].
\]

目标是这个 I 在训练种子分布上的中位数，条件包括同一个预训练父模型、数据构造、可训练矩阵和优化器。每个 I 来自两个 B 方向各四条完整策略轨迹；它不是梯度恒等式，也不是功能的因果分解。δ=0.01 是采纳的实际约定。固定 B 的比较总训练答案量不同；800A/200B 对 500A/500B 总答案量相同但 B 机会不同。两个问题分开解释。

## 5. Computational Realization

新建 A/B 各 200 个不同有序列表，用 20 个经分词边界核验的单词元中文答案。A/B 无序内容组互斥；循环词位平移确保每个位置与答案次数一致。两种规则共用列表和模板，A/B 标签仅作记录，不进入模型输入。每条轨迹重置原始 Qwen3-0.6B Base，只更新 layer27 Attention `o_proj`；恒定学习率，每步 20 个有效答案。不加规则专属适配器或专家。

每个 B 方向运行：同/异规则 A200 或 A800、固定 B200；B-only；同/异规则 A500/B500。顺序未见是 B 见过内容组的新排列；组合未见是所有实际训练均未见的组。分别报告，并等权合并。三个探索种子使用 dev；六个新确认种子在工程门控与协议冻结后使用未打开的模型 test。Dev 不能选择确认条件或学习率。

## 6. Minimal Falsification Tests

数据须通过答案 oracle、单词元续写边界、互斥、均衡和实际训练相对的未见定义。Smoke 通过有限答案归一化遥测、恒定学习率/计数、冻结权重逐字节一致、保存身份、数值 no-op，以及独立进程恢复和下一步一致后，才可 Full。

探索只作描述。确认只判合并种子主值：六个 I 全部大于 +δ，或全部小于 −δ，满足冻结的保守双侧符号规则（p=0.03125）。独立、同生成机制的种子效应假设下，[最小值,最大值] 对中位数至少有 96.875% 覆盖。区间全部落入 [−δ,δ] 支持有界实际无效；跨越相关阈值或工程门控失败均属不足。分项不得补救主值。A 有效学习仅门控另行声称的局部机制，不门控策略估计。

## 7. 当前证据

频率 Smoke56/56工程通过；Full pt-ho4byzg4 完成126轨迹、90,000答案、4500步，工程1520/1520及实际曝光资格126/126通过，平台SUCCEEDED。126个真实保存家族已核验与登记。确认六个独立种子的主交互全部超过δ=.01，中位0.066142 nat/答案，保守区间[0.051485,0.078583]，冻结双侧p=.03125，统计分支REGISTERED_POSITIVE_MEDIAN_INTERACTION。

同规则加练的额外答案CE收益更大，但所有加练条件的96个分项CE都低于B-only，异规则仍有净CE收益。准确率不保证随CE改善：diff800合并中位83.2500%，B-only83.4375%。等预算分配另行报告，不能替代固定B主比较。机制、功能划分、架构价值及问题关闭判断仍为研究者Unknown。[完整结果](../../../experiments/A17/17_02_fixed_pool_frequency/A17_02_E01_fixed_pool_frequency/summary_cn.md)。

## 8. Claim Boundary And Next Decision

合格结果只涉及这个 Base、两个固定池和受限优化器上的条件规则呈现策略。它不确立专家必要性、完整功能划分、自然语料频率机制或长期架构收益。合并结果和规则/未见分项的不一致必须保留。下一研究者决定：冻结交互中位数及净影响/分配结果，是否值得继续机制分析；AI 只完成事实，不代替判断。

[频率 Focus](../../../focus/focus_fixed_pool_frequency_shared_learning_cn.md) · [Protocol](../../../experiments/A17/17_02_fixed_pool_frequency/A17_02_E01_fixed_pool_frequency/protocol_cn.md) · [父 Anchor](../17_01_controlled_list_prediction_rules/17_01_controlled_list_prediction_rules_anchor_cn.md)
