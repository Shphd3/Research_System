# Summary：A17_02_E01 固定池呈现频率实验

[English](summary.md) · [Anchor](../../../../problem_anchors/17_shared_and_interference_learning/17_02_fixed_pool_frequency/17_02_fixed_pool_frequency_anchor_cn.md) · [Protocol](protocol_cn.md) · [Detailed](detailed_cn.md)

冻结的确认规则得到 `REGISTERED_POSITIVE_MEDIAN_INTERACTION`：中位交互 **0.066142 nat/答案**，六个种子全部超过 δ=0.01。同规则加练带来的额外答案 CE 收益更大；异规则加练相对 B-only 仍降低 CE。训练策略实验已经完成，机制解释与问题关闭仍由研究者判断，保持 `Unknown`。

`task_state=FULL_COMPLETED`；`result_state=MEASURED_STATISTICAL_BRANCH`；`design_state=USER_ADOPTED_FROZEN_IMPLEMENTATION`；`question_state=HUMAN_CONFIRMED`，没有关闭问题。

## 1. Purpose：为了回答什么

固定 B 出现200次，把同一 A 池从呈现200次增加到800次。比较 A 执行相同规则和不同规则时，B 的未见测试答案损失怎样变化。FIRST 取首项，LAST 取末项。不同的是可见指令及选择操作；相同的是词表、列表生成方法、答案分布、文本模板和 B 的训练机会。这里的频率指固定池的重复呈现次数，内容量没有增加。

## 2. Hypothesis：候选解释与竞争解释

预注册目标是不同训练种子的交互中位数是否超出 ±0.01 nat/答案。竞争解释认为，额外练习主要增强共同的列表或词汇处理，因此交互不超出这一区间。首项与末项规则都有明确提示，可以同时满足。正交互可以表示异规则帮助较少，不能直接解释为净干扰。

## 3. Analysis Method：实际怎么测

每条轨迹恢复原始 Qwen3-0.6B Base，只更新第27层 Attention 的 `o_proj` [1024,2048]。使用恒定 LR1e-4 的 AdamW，micro5×累积4，每步20个答案；只计算答案位置的全词表 CE。其余参数冻结。A、B 各有200个不同有序列表，内容组互斥，20词的位置与答案频率精确均衡。

对 B=FIRST、LAST 分别执行同/异规则 A200/800 配 B200、B-only、同/异规则 A500/B500。探索3种子只用 dev；确认6个新种子使用条件及代码冻结后才模型评估的新 test。顺序未见测试已实际训练内容组的新排列；组合未见测试未训练内容组。每个种子等权合并两规则与两面板，独立重复数是6，不是24个分项或800条文本。六个合并交互全部超过同侧阈值才通过确认，分项不能挽救主指标。

Smoke pt-cgmiw5f3 的56/56工程检查和外进程恢复通过。Full pt-ho4byzg4 完成126条轨迹、90,000个训练答案、4500步；探索508/508、确认1012/1012工程检查通过。实际曝光下两类未见资格126/126通过。平台终态 SUCCEEDED：UTC2026-10-09 17:48:33／北京时间2026-10-10 01:48:33。126个真实保存家族已独立核验 SHA 并登记。[终点证据](/data/250010109/MoE_Router/experiments/20261010_a17_fixed_pool_frequency/runs/full_4h100_v2_20261009T172612Z/terminal_verification.json)。

## 4. Conclusion：得到什么、不能推出什么

确认均值0.066663，中位数0.066142；保守种子总体中位数区间 [0.051485,0.078583]，在独立同分布种子效果假设下覆盖率至少96.875%。六个交互全部大于0.01，满足冻结的双侧符号规则，p=0.03125。首项/末项与两种未见分项也全部为正；Detailed 保留所有数值。

四个加练条件分别都有24个种子×B规则×未见分项，CE 全部低于 B-only。合并 CE 中位数：B-only0.798928、同规则 A800/B2000.582623、异规则 A800/B2000.667780。因此结论是同规则额外 CE 收益更大、异规则仍有净 CE 收益。准确率必须单列：对应中位数83.4375%、89.1250%、83.2500%；CE 下降不保证正确答案更多。

在总计1000个答案的预算下，A800/B200 的合并 CE 比 A500/B500 更高，同规则种子差值中位数+0.008747、异规则+0.040762。这个比较同时改变了 B 的机会，回答的是预算分配问题，不能替代固定 B 的主比较。

边界是一种预训练 Base、固定数据池、末层矩阵容量和优化器。结果没有证明从头学习机制、因果功能划分、自然语料频率机制、净干扰或专家价值。SAE 后续描述固定36对终点；实际 SAE 分析仍为 NOT_RUN，不能改写本结果。[Raw Full](/data/250010109/MoE_Router/experiments/20261010_a17_fixed_pool_frequency/runs/full_4h100_v2_20261009T172612Z) · [Confirmation](/data/250010109/MoE_Router/experiments/20261010_a17_fixed_pool_frequency/runs/full_4h100_v2_20261009T172612Z/analysis_confirmation.json) · [Engineering](/data/250010109/MoE_Router/experiments/20261010_a17_fixed_pool_frequency/runs/full_4h100_v2_20261009T172612Z/engineering_audit_confirmation.json) · [Terminal](/data/250010109/MoE_Router/experiments/20261010_a17_fixed_pool_frequency/runs/full_4h100_v2_20261009T172612Z/terminal_verification.json) · [Platform](/data/250010109/MoE_Router/experiments/20261010_a17_fixed_pool_frequency/runs/full_4h100_v2_20261009T172612Z/platform_terminal.json) · [Actual asset registration](/data/250010109/MoE_Router/experiments/20261010_a17_fixed_pool_frequency/runs/full_4h100_v2_20261009T172612Z/asset_registration_request_registered_outputs.json)


### SAE真实终点描述完成（仅dev）

固定36对终点的匹配SAE描述也已完成，`pt-h6ke4emg`通过原生reader、数组与冻结守卫。9种子等权合并dev交互均值0.082567 nat/答案，其中SAE解码线性项0.001942、显式残差线性项0.022863、有限步余项0.057762。这是dev终点记账，与上面的六种子test确认分别保留。当前冻结SAE的列表任务重构残差较大，有限步余项不可省略，完整机制解释仍未建立。实际产物已登记为`analysis_a17_frequency_sae_actual1b_36pairs_20261009t2118z`；[Detailed附录](detailed_cn.md)保留顺序未见、组合未见各自读数、完整来源及边界。人类机制判断仍为Unknown。

状态澄清（北京时间2026-10-10）：保留的原Full报告主体中“实际SAE分析仍为NOT_RUN”指原训练报告写成时的历史状态。当前36对终点分析已全部完成并登记，以以上SAE完成附录为准；原六种子test确认结果及其科学边界不变。
