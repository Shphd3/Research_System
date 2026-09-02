# CLINC150 的细意图是否真的对应不同的任务更新需求？

```text
type: meeting_cycle_core_task
status: RESULT_COMPLETE_AWAITING_HUMAN_CONFIRMATION
problem_key: A15.semantic_supervision_middle_layer_separability
focus_role: PRIMARY
conversation_owner: codex-thread:01a054b9-ff32-7012-aae0-ccfea85152cf
ownership_status: CLAIMED
core_question: HUMAN_CONFIRMED
plain_language_design: HUMAN_CONFIRMED
cycle_start: 2026-09-01
target_meeting: Unknown
active_project: Projects/from-attention-to-search/
anchor: Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_13_semantic_supervision_middle_layer_formation/subanchors/15_13_03_semantic_gradient_functional_alignment_anchor.md
protocol: Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E06_clinc150_hard_route_gradient_functional_audit/protocol.md
source_meeting: daily_research_reports/backup/2026/08/0831/docs/0831_组会校订_训练阶段澄清与Post-training研究重定向.md
core_experiment_count: 1
```

## 1. 核心问题

在冻结 Qwen3-0.6B-Base 并完全指定正确粗领域路径的条件下，CLINC150 的不同细意图是否真的产生稳定且彼此不同的任务更新需求？如果存在这种差异，把同一细意图交给同一个细专家，是否会比随机均衡分组和领域内不细分形成更强的选择性专家功能与留出任务收益？

这里的强制路由是直接用标签选择专家。被选专家的输出权重恒为 1，不乘路由概率。影子路由器只预测领域或意图来记录语义能力；它不选择专家，不缩放专家输出，也不向专家或基座表示传递梯度。

## 2. 本轮实验

**本轮不回答：**不更换数据集，不研究聚类标签，不改善冻结基座的初始语义几何，不声称强制标签路径可直接部署，也不先加入表征正则。

### 实验 1：强制路径下的语义—梯度—功能审计

#### 目的

判断 E05 的细专家写入很弱，究竟是因为路由预测误差、细意图不对应不同任务更新，还是共享路径和任务头代替细专家完成了微调。完成标准是同时得到梯度结构、匹配训练对照、细专家干预和留出任务结果，并据此决定下一步只改路由、只改优化责任，还是停止在 CLINC150 上进行语义细分。

#### 假设

若细意图是合适的功能划分，同意图样本的任务梯度应比同领域异意图更一致，而且真实意图细分应在固定更新量下优于随机均衡细分和领域内不细分。最强竞争解释是交叉熵标签只让梯度看起来可区分，或任何均衡分区都能得到相同收益。

#### 分析方法

1. 在相同的强制粗路由阶段终点冻结全部参数，比较同意图与异意图的任务梯度方向，并用大量领域内随机均衡分组判断这种差异是否超过任意分组。
2. 从每个种子的同一个粗阶段检查点出发，比较领域内不细分、随机均衡细分和真实意图细分；三组保持数据、活动低秩规模、训练步数和影子语义路由诊断一致，只有细专家分组规则不同。
3. 先比较留出任务损失，再用匹配删除、错误替换、各模块梯度和实际参数更新解释收益来自哪里；只有语义梯度存在但细专家仍未承担更新时，才运行冻结共享路径和任务头的责任干预。

#### 结论

**AI 核验的直接结果，等待研究者确认表述：**六个主条件、两个种子和全部干预均完整。真实意图细分相对较强控制仍降低确认集交叉熵 `0.03126`，95% 区间为 `[0.02928, 0.03335]`；两个种子的两个控制差值均为正。删除当前细专家使损失增加 `0.05092`，换成领域内错误细专家使损失增加 `0.05230`，两个 95% 区间均完全大于零。注册裁决为 `PASS_SEMANTIC_FUNCTIONAL_VALUE`。

静态任务梯度按细意图形成强分组，但等范数单步更新没有显示语义组更优。因此可以说完整两阶段训练实现了 Oracle 语义分组价值，不能说这一价值已经被单步局部梯度解释。

## 3. 核心任务卡总结论

- **我的认识更新：**等待研究者确认：CLINC150 真实细意图在强制标签路由下能够形成有留出任务价值、且不可互换的细专家功能。
- **仍不能说：**不能说预测 Router 能恢复该收益，不能说冻结基座的原生表征被重塑，也不能推广到生成任务、新数据集或其他模型。
- **唯一下一决策：**等待研究者确认是否把“预测 Router 能恢复多少强制路由收益”设为下一轮唯一问题。

## 路径

- **实验协议：**[E06 Protocol](../../Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E06_clinc150_hard_route_gradient_functional_audit/protocol.md)
- **前驱结果：**[E05 Summary](../../Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E05_clinc150_frozen_base_staged_semantic_lora_router/summary.md)
- **结果摘要：**[E06 Summary](../../Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E06_clinc150_hard_route_gradient_functional_audit/summary.md)
- **完整证据：**[E06 Detailed](../../Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E06_clinc150_hard_route_gradient_functional_audit/detailed.md)
