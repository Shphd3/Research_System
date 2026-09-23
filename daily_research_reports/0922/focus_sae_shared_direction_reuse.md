# S7 的低有效维数是否伴随跨样本 SAE 方向复用增加？

```text
type: meeting_cycle_core_task
task_state: ACTIVE
problem_key: sae_shared_direction_reuse
focus_role: SECONDARY
question_state: HUMAN_CONFIRMED
design_state: HUMAN_CONFIRMED
result_state: EVIDENCE_AVAILABLE_AWAITING_RESEARCHER
cycle_start: 2026-09-22
target_meeting: Unknown
active_project: Projects/from-attention-to-search/
anchor: Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_17_three_model_sae_representation_trajectory/subanchors/15_17_01_sae_shared_direction_reuse_anchor.md
protocol: Projects/from-attention-to-search/main/experiments/A15/15_17_three_model_sae_representation_trajectory/A15_17_01_E01_shared_direction_reuse_audit/protocol.md
source_meeting: Unknown (2026-09-21 advisor discussion; transcript is not yet a canonical repository artifact)
core_experiment_count: 2
```

2026-09-22 研究者确认本轮独立问题、稳定 `problem_key=sae_shared_direction_reuse` 与唯一下一决策。本轮继承 A15_17 的旁路 SAE 表征审计，但只追问一个更小的机制问题：已经观察到的低有效维数，是否至少伴随跨样本复用相同 SAE 原子方向的增加。

## 1. 核心问题与它的边界

长期问题是：**SAE 作为训练正则时，究竟给主干表征施加了什么表示偏好，以及这种偏好什么时候会影响模型任务能力？**

本轮只处理其中一个局部机制。已有 21B 冻结审计中，第 8 层正文均值的原生注意力写入显示：重加权 S7 的全局方差有效维数低于 Dense 与原版 SALL；同时 S7 的在线 SAE 原子使用也明显更加集中。这里的“有效维数”只描述方差集中到多少个等效方向，不是语义维数；“原子复用”只描述不同样本是否反复使用相同 SAE 原子编号，不自动等于同一语义被统一编码。

**核心问题：** S7 的较低有效维数，是否至少伴随不同样本对同一批 SAE 原子的复用增加？

这个问题之所以现在需要解决，是因为“每个 token 只保留 Top-K 原子”只保证单 token 稀疏，**不能推出全体样本共享少量方向**。如果跨样本复用没有增加，就不能继续用“共享原子复用导致低维化”解释当前观察。

**本轮不回答：**

- SAE 是否让领域或其他语义信息更容易读出；
- 低有效维数是好还是坏；
- 原子复用是否因果导致语言损失或数据效率改善；
- S7 与 SALL 的差异是否由正则系数、旁路层数或训练谱系中的某一个因素单独造成。S7 与 SALL 不是严格匹配的正则强度消融，因此本轮不把二者差异称为“强正则的因果效应”。

## 2. 可证伪的预测与最强竞争解释

### 当前机制假设

如果 S7 的低维化主要经过“共享原子复用”这条路径，那么在相同输入、相同第 8 层和相同 Top-K 预算下，**不同样本的 SAE 原子使用分布应比 SALL 更相似，同时全局使用质量应集中在更少的原子编号上**。

逻辑只写成必要链：

```text
S7 的稀疏重构压力
-> 跨样本复用相同 SAE 原子增加
-> 全局使用方向的多样性降低
-> 低有效维数成为可能
```

本轮不把最后一个箭头当成已经建立的因果关系。

### 最强竞争解释

低有效维数不一定需要不同样本复用相同原子编号。另一种可能是：不同样本仍使用许多不同 SAE 原子，但这些原子的 decoder 方向本身越来越共线，或其系数变化只占据少数联合方向，因此主干仍可表现为低有效维数。

### 区分结果

- 若 S7 在同一面板上确实表现出更强的跨样本同-ID 原子复用，而有效维数同时更低，则“共享原子复用”通过第一轮必要条件检查，但**不能据此声称它已经因果解释低维化**。
- 若 S7 的有效维数更低，但跨样本同-ID 原子复用不高于 SALL，则当前机制的必要条件失败，停止用“共享原子复用”解释低维化，下一步转向 decoder 方向共线或系数协方差等竞争解释。
- 若样本、token mask、Top-K、字典身份或原生表征面板不能严格对齐，则结果不足，不能把两个不同面板的统计量拼成机制证据。

## 3. 允许与禁止的信息

本轮是冻结检查点的只读机制审计，不训练模型、不拟合语义分类器，也不需要领域标签。

允许使用：

- 21B 的重加权 S7 与原版 SALL；
- 两模型共同的 N8 固定输入、正文 token mask 与第 8 层在线 SAE 激活；
- 同一批样本上的原生注意力写入，用于复核有效维数；
- SAE 每个有效 token 实际进入 Top-K 的原子编号。

禁止使用：

- N8 领域标签来选择原子、阈值、样本或模型；
- 把 S7 的 feature 123 与 SALL 的 feature 123 当成同一个语义方向；
- 用不同样本池上的“复用统计”和“有效维数”拼接成一条机制链；
- 用本轮结果反推正则系数、旁路层数或训练谱系的独立因果效应。

## 4. 本轮实验（白话四要素；精确版在 protocol）

### 实验 1：同面板跨样本 SAE 原子复用审计

- **目的：** 检查“共享原子复用增加”是否真的是 S7 低有效维数的必要伴随现象，从而决定这条机制是否值得继续研究。

- **假设：** 若当前机制成立，S7 相比 SALL 应在相同 N8 样本上表现出更高的跨样本 SAE 原子使用相似度，并且全局使用更集中；竞争解释允许有效维数下降而同-ID 原子复用不增加。

- **分析方法：**

  1. 先核对两模型使用完全相同的样本、正文 token、层位、Top-K 与字典规模；同时确认有效维数也能在这批完全相同的样本上计算。任何一个对象不一致就停止机制比较。
  2. 对每个样本统计“哪些 SAE 原子在它的有效 token 上被实际选中、各自被选中的频率”，再比较不同样本之间的原子使用相似程度；同时检查整个面板的原子使用是否集中在更少的编号上。
  3. 将复用结果与同面板原生注意力写入的有效维数并列解释。这里只检查必要伴随关系；不把两项相关变化写成因果证明。

- **结论（执行前先写分支）：**
  - **若支持：** S7 的跨样本同-ID 原子复用更强，且同面板有效维数更低。允许说“共享原子复用机制仍然成立得通，并通过必要条件检查”；下一步才设计能区分“代码复用”与“decoder 几何共线”的控制。
  - **若不支持：** S7 的有效维数更低，但跨样本同-ID 原子复用没有增加。削弱或停止当前机制，下一步转向 decoder 方向几何或系数协方差。
  - **若证据不足：** 输入、mask、层位、Top-K、字典身份、缓存或同面板有效维数无法对齐时，不作机制判断；只补齐该对齐缺口。

→ `protocol`: `Projects/from-attention-to-search/main/experiments/A15/15_17_three_model_sae_representation_trajectory/A15_17_01_E01_shared_direction_reuse_audit/protocol.md`

### 实验 2：同为S7、当前λ=0.1的17B训练历史对比（研究者新指定）

- **目的：** 排除S7/SALL旁路层数不同这一混淆，检查相同S7结构及当前系数下，训练历史不同是否仍伴随复用/原生几何差异。
- **假设与竞争解释：** 历史不同可能留下不同端点状态，也可能在当前面板无法区分；不预设哪一支更集中。微批划分等残余差异尚未消融，所以不是纯系数历史因果试验。
- **分析方法：** 同面板、同原生支持定义与配对不确定性，对比重加权减从零训练的复用差值，并独立列出原生有效维数；先核对同初始化、输入与模型身份，禁止跨模型对齐原子ID。
- **结果分支：** 区间完全为正或负分别表明相应条件复用更高；跨零只表明未分辨差异，不是等价。几何单列，不用它选择差值方向；测量失败则证据不足。以上为测量解释，不自动确立历史因果或主要机制。
- **执行范围：** 研究者明确要求直接full、不做本轮smoke；提交后停止轮询，等研究者通知后审计结果与写四段式分析。精确合同：[E02](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_17_three_model_sae_representation_trajectory/A15_17_01_E02_s7_17b_training_history_reuse_audit/protocol.md)。

## 5. 轮次滚动摘要

| 日期（UTC） | 本轮问题 | 结果或 `NOT RUN` | 认识更新 |
|---|---|---|---|
| 2026-09-22 | 共享原子复用能否作为低有效维数的候选机制？ | [E01证据已到位](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_17_three_model_sae_representation_trajectory/A15_17_01_E01_shared_direction_reuse_audit/summary_cn.md)，预注册必要条件检查通过 | 研究者认识更新待填写；因果及decoder共线竞争解释未裁定。完整本轮记录仅在Detailed。 |

## 6. 待研究者决定

- [x] 2026-09-22 研究者明确确认192个固定N8样本、原生Top-32频率向量平均余弦差、2000次配对样本bootstrap与必要条件判据，并授权smoke通过后完成full run。精确合同由E01 Protocol A2拥有；不是对结果或因果机制的预先确认。

2026-09-22 执行范围补充（研究者本次明确要求继续实现并提交 4 卡 5090 smoke）：
上述待确认项继续约束**正式科学分析**，不把它们默认为已批准。允许 E01
Protocol 单独登记 `APPROVED_FOR_IMPLEMENTATION_AND_ENGINEERING_SMOKE_ONLY`：
冻结模型、小面板验证真实 Top-32 原子 ID、同输入/同 mask、统计实现与只读性；
不运行完整面板主比较、不作机制判断、不自动转正式任务。此补充不改变本轮
科学问题、结果状态或研究者的唯一下一决策。

后续执行范围更新：上段smoke-only限制已由研究者本次完整运行指令与精确判据确认在E01 A2范围内取代；其他实验、训练、资源切换仍未授权。

## 7. 本轮总结论（研究者完成审计后填写）

- **我的认识更新：** `NOT AVAILABLE`。
- **仍不能说：** `NOT AVAILABLE`。
- **唯一下一决策：** 按研究者新要求，先完成同为S7的17B从零训练/重加权对比，判断控制旁路结构和当前系数后，复用与几何差异是否仍与训练历史相伴；不据此确立历史因果。decoder几何区分实验暂不执行。

## 路径

- **父 Anchor：** `Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_17_three_model_sae_representation_trajectory/15_17_three_model_sae_representation_trajectory_anchor.md`
- **本轮 Subanchor：** `Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_17_three_model_sae_representation_trajectory/subanchors/15_17_01_sae_shared_direction_reuse_anchor.md`
- **实验协议：** `Projects/from-attention-to-search/main/experiments/A15/15_17_three_model_sae_representation_trajectory/A15_17_01_E01_shared_direction_reuse_audit/protocol.md`
- **结果摘要：** [中文四段式分析](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_17_three_model_sae_representation_trajectory/A15_17_01_E01_shared_direction_reuse_audit/summary_cn.md) / [English](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_17_three_model_sae_representation_trajectory/A15_17_01_E01_shared_direction_reuse_audit/summary.md)
- **完整证据：** [Detailed](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_17_three_model_sae_representation_trajectory/A15_17_01_E01_shared_direction_reuse_audit/detailed.md)
- **最终报告：** `NOT_YET_WRITTEN`
- **待研究问题清单：** `Projects/from-attention-to-search/main/parking_lot/README.md`
