# 实验总结：A17_04_E03 单层 Attention 获取诊断

[English](summary.md) · [Anchor](../../../../problem_anchors/17_shared_and_interference_learning/17_04_conditional_mapping_transfer/subanchors/17_04_01_rule_acquisition_diagnosis_anchor_cn.md) · [冻结 Protocol](protocol_cn.md) · [Detailed](detailed_cn.md) · [清单](artifact_manifest.json)

Protocol版本 a17_04_e03_single_attention_acquisition_v1，保留追加算术勘误A01。两组有限训练与原生分析均完成，登记工程保护项通过；证据可用于规定的获取诊断。范围为 DEV_DIAGNOSTIC_ONLY、一个训练顺序种子。研究者机制判断、采用决定和父问题闭合仍为 Unknown。

## 1. 目的

判断只训练最后一层 Attention 的四张投影，能否学会旧中性口令规则，以及结果是否依赖本次两种优化设置。这是在缩小后续共享学习所需的获取前提，还没有测新任务迁移。

## 2. 模型

模型是登记的 Qwen3-0.6B Base。输入包含模式一、甲或乙口令，以及三个不同词的空格列表。甲取首项、乙取末项。例如同一“红 蓝 绿”，甲的目标是红，乙的目标是绿。答案都是一个词元，只计算答案位置的下一词损失。

两组均只训练第27层 q/k/v/o 四张权重，共6,291,456参数。其它参数，包括注意力归一化，全部冻结。模型总规模不变，只允许这一层改变注意力读取和输出投影。它不是仅训练Q/K/V，也不是训练Attention相关全部参数。

SGD学习率0.01、无momentum/decay；AdamW学习率0.0001、betas(0.9,0.999)、epsilon1e-8、decay0。两组都对四张权重合起来做全局梯度范数1裁剪，使用种子29、同中性数据/标签/批次顺序、每步20答案和同FP32原生前向。先各自对64个tiny答案训练160步，然后重新从Base和新优化器开始，对2400条记录训练1200步。Main各呈现24000答案，不继承tiny权重。

资格要求“口令×DEV面板”四格的全词表准确率分别达到80%，每格200答案。两种DEV分别测熟悉三元组的未见顺序、未见三元组；合并等权。另测同一列表的两种口令是否都答对，避免把只提高候选词概率误认为学会按口令选择。

## 3. 假设

候选H：最后一层四张投影，在至少一种固定优化设置下，足够在本预算学会规则。最强替代解释是需要更早层的改变、本优化设置无法有效优化较小范围，或CE收益仅来自候选词适应。固定DEV四格和双口令联合成功可区分最后一种解释；SGD/AdamW比较仍混合学习率、预条件与实际步幅。

## 4. 结论

1. **最后一层四张投影配合本次AdamW，已经能够学会。** 固定1200步终点，两种未见DEV、四格和400个双口令配对均为100%。首个保存达标点是240步/4800答案：合并99.375%，最弱格98.5%。因此这个任务、种子和预算下，不需要开放四层才能获取规则；仍不证明全局最小必要范围。
2. **相同单层范围配合本次SGD，没有达标。** 未见顺序52%、未见组合53.5%、合并52.75%、最弱格46.5%。仅16.75%的列表两口令都答对，76.25%在两种口令下仍输出相同答案。失败只限本次SGD学习率/裁剪/预算，不代表所有SGD或单层方案都不可能。
3. **我们缩小了获取障碍，还没有回答迁移问题。** 原中性数据能通过一层注意力和AdamW学会，提供了更小的可行旧规则起点。没有执行同向/反转新模式、参数机制或共享/分开收益比较。

依据是已登记的[原生结果](/data/250010109/MoE_Router/experiments/20261011_a17_single_attention_acquisition/runs/single_attention_20261011T145214Z/analysis/results.json)和[分格轨迹](/data/250010109/MoE_Router/experiments/20261011_a17_single_attention_acquisition/runs/single_attention_20261011T145214Z/analysis/trajectories.csv)。科学机制认可仍为Unknown。

## 5. 分析

下表比较同为1200步/24000答案的Main终点。每种DEV有400答案；最弱格取四个各200答案的口令/面板格。“两口令都对”以400个列表为单位，不是答案级准确率。数值均为百分比。

| 最后层设置 | 未见顺序 | 未见组合 | 合并DEV | 最弱格 | 两口令都对 |
|---|---:|---:|---:|---:|---:|
| 四投影＋SGD | 52.00 | 53.50 | 52.75 | 46.50 | 16.75 |
| 四投影＋AdamW | 100.00 | 100.00 | 100.00 | 100.00 | 100.00 |

固定已见TRAIN面板，SGD为61.5%、AdamW为100%。SGD同时存在未充分拟合/选择与TRAIN–DEV差距，不是只在未见内容失败。AdamW从Base的33.25%合并DEV，升至240步99.375%，600/1200保存点均100%；SGD没有保存点达标。未保存的中间状态不能定位首次学会的精确时刻。[原生轨迹](/data/250010109/MoE_Router/experiments/20261011_a17_single_attention_acquisition/runs/single_attention_20261011T145214Z/analysis/trajectories.csv)保留这些读数。

SGD终点已把98.2288%概率分给三个列表词，但按口令选择仍弱。平均CE为0.941982 nat，其中候选访问0.018152、条件选择0.923831。AdamW的CE为0.000691、条件选择0.000685，双口令联合100%，同答案比例0%。这是精确输出记账和实际预测结果，支持在本DEV上按规则选择，不识别唯一内部机制。[配对轨迹](/data/250010109/MoE_Router/experiments/20261011_a17_single_attention_acquisition/runs/single_attention_20261011T145214Z/analysis/paired_trajectories.csv)保留口令切换。

小集合拟合要单独看。AdamW在64个tiny答案上100%，但tiny训练结束时合并DEV只有65.375%。SGD tiny为59.375%、DEV46.25%。随后Main重启，因此Main成功不是继承tiny记忆。

作为历史参考，同最终答案预算的E02中性输出矩阵AdamW合并DEV为68.5%，最后四层AdamW为100%，数据和优化设置相同。本轮一层也达到100%，可训练参数从25,165,824缩到6,291,456。[E02 Summary](../A17_04_E02_rule_acquisition_diagnosis/summary_cn.md)拥有旧数值。它证明一个更小的可行范围，不证明Q/K/V各自必要，也不能归为纯参数量原因。

两优化组的实际更新也不同。Main平均四张整体位移范数：SGD为0.010000、AdamW为0.015209；AdamW最大单步为0.249701。平均和早期更新均未匹配。因此“AdamW在这里可行”不能改写成纯预条件机制，也不能推出所有SGD都会失败。[曝光与更新表](/data/250010109/MoE_Router/experiments/20261011_a17_single_attention_acquisition/runs/single_attention_20261011T145214Z/analysis/training_exposure.csv)记录这项混杂。

两组实际完成54400个拟合答案，另有Smoke240和外部重放80，分开计数。A01纠正Protocol原总Smoke算术，不改各路径3步或配置。原生分析核验16个tiny/Main保存状态、34个预测文件、17184条记录出现；最大损失恒等式误差1.6231×10⁻⁶ nat。外部恢复、冻结参数、遥测通过；执行后36个冻结文件一致。[登记回执](/data/250010109/MoE_Router/experiments/20261011_a17_single_attention_acquisition/runs/single_attention_20261011T145214Z/full_registration_receipt.json)与[当前输出访问](/data/250010109/Research_System/assets/checks/2026-10-11_a17_single_attention_20261011t145214z_full_outputs.json)绑定实际保存；完整过程由Detailed持有。

一个训练顺序种子和已使用DEV仅支持有限诊断，不能独立确认或推广到任意任务。下一决定为Unknown：研究者是否授权从该单层AdamW设置开展新迁移比较。当前小测试完成，没有启动后续实验。
