派生阅读副本；原件位置：`Projects/from-attention-to-search/main/focus/focus_conditional_mapping_transfer_cn.md`。
[精确原始文件](../../../../../sources/Projects/from-attention-to-search/main/focus/focus_conditional_mapping_transfer_cn.md)；研究修改仍回到原件。

---

# 条件映射变化与跨任务学习

problem_key: `conditional_mapping_transfer`
question_state: `USER_ACTIVATED_BOUNDED_QUESTION`
design_state: `USER_DELEGATED_BOUNDED_IMPLEMENTATION`
result_state: `R02_DIAGNOSTIC_RESULTS_AVAILABLE_RESEARCHER_JUDGMENT_PENDING`
task_state: `BOUNDED_R02_EXECUTION_AND_FACTUAL_DELIVERY_COMPLETE`
scientific_mechanism_judgment: `Unknown`
question_closure: `Unknown`

## 问题与边界

模型先学会一套“口令决定取哪个位置”的规则。新模式保留或反转这套规则时，共享更新对旧模式的帮助或损害是否随之改变？这是研究任务关系的同级问题，不重复 A17_03 对更新成分的干预。研究者于 2026-10-11 认可将第二轮与此前的条件映射假设合并，明确要求另构数据并完整执行，中间无需批准。

## 目的与完成标准

旧模式已经同时监督两个口令：甲取首项，乙取末项。新模式在“同向”和“反向”两个独立实验中使用相同输入，只改变正确答案的映射。因此，本轮考察条件映射的改变，不考察“新任务补齐此前没有学过的位置知识”。完成标准是冻结数据与契约、通过 Smoke 和独立进程精确恢复、完成全部训练分支和读数、登记实际保存资产、写齐双语事实结果。完成不要求一定出现干扰，也不要求机制得到支持。

## 三步分析

1. 先学习模式一的两个口令，再从同一个旧终点分出模式二的同向、反向训练；呈现次数和预算相同。
2. 在未见顺序、未见组合以及两者等权合并的数据上，比较旧答案优势、损失和准确率。把候选词概率变化与按规则选择答案的相对偏好分开，并比较两种模式的口令响应。
3. 检查同范数单步作用、可比较的新任务学习水平，以及反向映射的旧新联合训练对照。检查失败时保留难度、学习路径和容量的不确定性。

## 结果分支与下一项决定

资格检查通过后，反向条件稳定降低旧答案优势，支持“任务关系会改变跨任务学习作用”这一局部认识。只有反向分支相对自己的共同起点恶化，才能称旧任务受到净损害。效果缺失或相反，削弱本设置下“反转容易产生干扰”的预期。旧映射没有学会、新训练无有效学习，或工程门槛失败，相应问题为证据不足。操作阈值是 AI 的报告约定，不是研究者科学裁决。下一项研究者决定只有一项：这个条件映射效应是否足够明确、足够特异，值得进一步比较参数共享与分开。机制接受和问题关闭仍为 Unknown。

R01有限执行于 2026-10-11 完成。旧 DEV 逐口令／面板准确率为 33%–54%，低于冻结的 80% 学习资格。反向减同向的旧答案优势效应为 −0.005165 nat；两分支的旧平均 CE 和端点优势都改善。因此不能确认已掌握的旧规则受到损害。可比能力点未达到，联合可行性仍为 Unknown。完成是执行事实；机制接受与问题关闭仍为 Unknown。

[Anchor](../problem_anchors/17_shared_and_interference_learning/17_04_conditional_mapping_transfer/17_04_conditional_mapping_transfer_anchor_cn.md) · [Protocol](../../../../../UNAVAILABLE.md) · [Summary](../experiments/A17/17_04_conditional_mapping_transfer/A17_04_E01_consistent_reversed_mapping/summary_cn.md) · [Detailed](../../../../../UNAVAILABLE.md)。

## 已授权的旧规则学习诊断（2026-10-11）

研究者已要求诊断旧规则未学会的原因，允许可行的增参训练，且不需要中间再次批准。父问题及其证据不足结果保持原状。[子Anchor A17_04_01](../problem_anchors/17_shared_and_interference_learning/17_04_conditional_mapping_transfer/subanchors/17_04_01_rule_acquisition_diagnosis_anchor_cn.md)与[E02 Protocol](../experiments/A17/17_04_conditional_mapping_transfer/A17_04_E02_rule_acquisition_diagnosis/protocol_cn.md)负责此前提审计。使用训练与开发集比较优化方式、可训练注意力范围和输入呈现；目前不重启新任务迁移。实验完成与找到学习修复方法是两件事。科学解释与后续迁移决定仍为Unknown。

该诊断已完成。一个诊断种子中，开放最后四层注意力投影，保留原中性口令，在保存的240步点两类DEV、两种口令均100%。改用明文首末指令的单矩阵训练也合格；原SGD、中性单矩阵AdamW及顿号格式未合格。这建立可行学习路线，尚未回答父问题的迁移效应或唯一内部原因。[E02 Summary](../experiments/A17/17_04_conditional_mapping_transfer/A17_04_E02_rule_acquisition_diagnosis/summary_cn.md)负责有界结论，[Detailed](../experiments/A17/17_04_conditional_mapping_transfer/A17_04_E02_rule_acquisition_diagnosis/detailed_cn.md)负责设置、偏离和实际证据。AI建议：重新研究模式条件映射时优先保留中性口令的增范围路线；解释接受、独立确认和新的迁移运行分别判断。

## 已授权的单层范围缩小测试（2026-10-11）

研究者已授权最后一层q/k/v/o全部开放的SGD、AdamW两组有界学习测试，并明确后续步骤需要另行批准。[E03 Protocol](../experiments/A17/17_04_conditional_mapping_transfer/A17_04_E03_single_attention_acquisition/protocol_cn.md)沿用现有获取诊断子Anchor和中性口令TRAIN/DEV。有效结果可证明此较小可训练范围在某套优化设置下是否足够，不证明普遍最小范围或纯容量原因。父迁移结果与科学判断保持原状；不自动继续新模式训练。


单层小测试已完成。在单种子、已公开开发集的诊断中，只训练最后一层q/k/v/o四个权重矩阵并使用AdamW，保存的240步检查点合并准确率为99.375%，最弱口令／分项98.5%；600步和1200步的四个分项均为100%。本次SGD配置终点合并准确率52.75%，最弱分项46.5%。这表明629万可训练参数的单层方案在当前AdamW配置下足够，但不证明通用最小预算或唯一的优化／容量机制。[E03总结](../experiments/A17/17_04_conditional_mapping_transfer/A17_04_E03_single_attention_acquisition/summary_cn.md)和[详细记录](../experiments/A17/17_04_conditional_mapping_transfer/A17_04_E03_single_attention_acquisition/detailed_cn.md)拥有事实结果。Smoke和正式训练完成，实际资产已登记。这修复的是旧规则学习的前置条件，不改变父问题的迁移结论。研究者明确暂缓后续步骤；没有提交新模式迁移或机制实验。下一步批准与科学判断仍是独立决定。


## 合格起点后的R02授权

研究者现已批准从E03合格旧终点，以最后一层Q/K/V/O加AdamW进行同向／反转迁移，并完成有限的同状态优化诊断。新授权仅在这些操作范围取代此前暂缓。[R02 Protocol](../experiments/A17/17_04_conditional_mapping_transfer/A17_04_E01_consistent_reversed_mapping/rounds/R02_single_layer_adamw/protocol_cn.md)拥有执行；原E01保留为证据不足的R01记录。三个续训种子共用一个旧检查点；TRAIN／DEV属于已暴露诊断证据。实际结果登记前，父结果状态与科学判断不变。

## R02事实结果交付

已完成授权的九条单层AdamW训练分支、34个固定状态优化干预、72个真实状态核验及实际资产登记。共同旧起点准确率100%；同向终点旧规则仍100%，反转终点旧规则均0%，新规则97.75%–100%。旧margin反转减同向的合并平均效应−38.9391nat（三个续训顺序共用一个旧终点）。联合监督终点旧新均99.25%–100%，给出当前范围可容纳两映射的实例；它有额外旧标签、仅一半新曝光，不是同监督收益比较。[R02总结](../experiments/A17/17_04_conditional_mapping_transfer/A17_04_E01_consistent_reversed_mapping/rounds/R02_single_layer_adamw/summary_cn.md)和[Detailed](../experiments/A17/17_04_conditional_mapping_transfer/A17_04_E01_consistent_reversed_mapping/rounds/R02_single_layer_adamw/detailed_cn.md)拥有完整结果及边界。原R01证据不足记录保留；新state只表示事实可读与有限执行完成，研究者机制接受、下一项决定及问题关闭仍Unknown。没有启动后续参数分开实验。
