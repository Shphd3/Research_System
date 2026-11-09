# 当前入口：Attention纯分支SAE——先确认架构，再Smoke

状态：**ARCHITECTURE_CONFIRMATION_REQUIRED / NO_SMOKE_BEFORE_CONFIRMATION**。
本文件取代04训练交接中的旧挂点、C/T条件及两组8卡资源安排。04仍可用作脚本地址索引；其自动执行指令不再适用于新版架构。以下全文可发给新的执行AI。

---

请在 `/data/250010109/Research_System` 接续八层语言模型的旁路SAE研究。**第一轮只审查来源、解释并画出两种待训练模型的架构，给我一张具体确认卡；等我确认架构后才能实施并开始Smoke。不要一上来运行旧C/T脚本，也不要将本提示词当作架构已经确认。**

## 1. 导师最新要求与我的目标

我们想观察SAE重构梯度是否促进领域相关表征形成，以及作用位置改变后效果是否不同。导师建议SAE读取不含该层残差相加的Attention分支输出，并在归一化后训练；SAE作为旁支，重构损失往上游反传，原语言模型主前向不消费SAE重构。

我希望准备两个八层模型：

- 模型A：最后一层的Attention输出经Norm后，接一个SAE旁支，重构损失反传上游。
- 模型B：“在8层模型前，再加上一层SAE”，重构损失也反传。**这句话的精确挂点、是否保留最后层SAE，需要你先向我确认，不能替我选。**
- 两模型都要有SAE原子防死机制。沿用已验收的AuxK作为实现起点；每个字典独立维护活动统计。主重构项输入live，目标和能量分母detach；AuxK直接只更新SAE。这些是继承方案，须列入确认卡。

最新资源安排：

| 模型 | 正式训练资源 |
|---|---|
| A：最后层Attention纯分支SAE | 单节点4×H100 **Reserved**，profile `h100-4-reserved` |
| B：前部SAE方案，架构待确认 | 单节点8×RTX5090 **Spot**，profile `5090-8-spot` |

此前预算为每个模型50B有效预测词元，八层hidden1024、SAE30000/Top32。它们作为继承设置列出，不要擅自缩成四层或1024步，也不要默认增加第三个模型。**资源数量已明确，不再询问Reserved/Spot的拼写；Smoke资源单列在确认卡，不能把旧“两臂都用双5090 Smoke”自动套到H100模型上。**

## 2. 必须先讲清的张量位置

先读实际代码，画出一个Transformer块。旧实现为：

```text
x_l ──Norm1──Attention（含输出投影W_O）── a_l ──┐
  └───────────────────────────────────────── + ── r_l ──Norm2── MLP ── + ── x_(l+1)
                                               ↑                       ↑
                                           r_l=x_l+a_l ────────────────┘
```

更精确地写：

- `a_l = Attention_l(Norm1_l(x_l))`：Attention模块返回值，已经过输出投影，尚未与当前层残差x_l相加。
- `r_l = x_l + a_l`。
- 旧旁路位置为`h_l = Norm2_l(r_l)`，**它含残差，不能称为本次要求的纯Attention分支。**
- 导师新要求的候选位置为`u_l = Norm_side_l(a_l)`，再令`z_l = SAE_encoder(u_l)`、`u_hat_l = SAE_decoder(z_l)`。原主干仍计算`r_l`与原MLP；`u_hat_l`不替换主前向。

“纯分支”仅表示排除当前层残差加法的直接分量；a_l仍依赖x_l及其历史信息，不能宣称历史残差信息完全被去掉。也不要把Q/K head normalization、Attention前Norm1或模型末尾Norm误作这里的Attention输出Norm。

旧代码没有独立的Attention输出后Norm：必须说明新Norm具体怎样定义。**AI建议供确认：旁支专用、无可训练仿射参数的RMS归一化，eps沿用1e-6，梯度可经过归一化回到Attention。**这避免新增可训练缩放参数成为额外变量。若建议训练旁支Norm、共享现有Norm2，或把新Norm放进主干，请分别解释它改变了哪些参数和前向路径；不能不加说明就选。冻结归一化参数不等于detach整个u_l。

SAE旁支不含identity skip；“不加残差连接的地方”不等于删除语言模型自身的残差连接。若你认为导师实际要求删主干残差，先列为不同架构问我，不得自行实施。

## 3. 第一轮只向我确认真正未定的架构

先给出推荐解释和至多三项关键选择，避免问配置文件能核实的事实：

1. **“8层模型前”的位置：**是token embedding输出、进入第1个Transformer块之前，还是第1层Attention输出经旁支Norm之后？前者此处还没有Attention，主要梯度直接作用于输入embedding；后者才是与末层同类型的早期Attention挂点。若我的本意是“8层每层都加”，须由我明确说出，你不能自行扩展为8个SAE。
2. **模型B的SAE数量：**是在模型A基础上保留末层SAE、再增加前部SAE，还是第二个模型只在前部放一个SAE？若目标是比较位置，AI可推荐“前部一个 vs 末部一个”，因为字典数和损失数量一致；若我选择“末部一个 vs 前后各一个”，接受这个设计，但准确称为额外前部约束的配置对比，不能纯归因于层位置。
3. **Norm与多字典loss契约：**提出可审阅的固定方案让我确认；若有两个SAE，明确总重构项是各λ=1求和还是平均，以及AuxK如何相应聚合。两种方式梯度总强度不同，不能悄悄沿用一个SAE的系数解释。

模型A的“Attention输出投影后、当前残差相加前”也需在图中明确展示供我确认。两个模型的主重构梯度均live，不再是旧C(detach)/T(live)实验；不要沿用C/T名称掩盖比较对象变化。

## 4. 第一轮交付：一张架构确认卡

卡上逐项列出两模型：

- 八层主干与SAE数量/宽度/Top-k；精确层号与代码张量名。
- 主前向图、残差相加位置、旁支分叉点、新Norm位置及是否可训练。
- LM、每个重构项、每个AuxK项的梯度归属；哪个参数组会被哪个损失更新。
- 总目标公式与各系数、每个损失分母、多个字典的聚合规则。
- 两模型的共有项、实际差异、参数量差异和能回答/不能回答的问题。
- 继承的数据、seed17、优化器、日程、每模型50B和checkpoint规则。
- 最新正式资源分配，以及各自最小Smoke资源/更新数/恢复检查。
- 我确认后执行的具体顺序与停止门。

推荐Smoke方案：A在已指定4H100 Reserved拓扑上作有界Smoke；B复用先前2×5090 Spot授权作Smoke，并在正式8卡启动时检查八rank通信/计数。将此安排放入卡中确认，不先提交。也可提出更贴近最终拓扑的B Smoke，但改变Smoke卡数要明确说明。

**第一轮结束时请问我：“请确认卡中的两个挂点、模型B是否保留末层SAE，以及Norm/损失聚合设置；确认后按卡开始Smoke。”**这是我主动要求的架构确认门，不是因为旧memory或脚本建议而加的审批。

## 5. 确认后才做的实现与Smoke

先读`docs/training_reuse_index.md`、真实源文件和`docs/training_observability_contract.md`；提交前从`docs/execution_envelope.md`解析profile、image和runtime。现有代码只作来源，建立新隔离版本，不修改旧活跃训练目录，也不把旧挂点的测试PASS当成新挂点通过。

Smoke至少验证：

- 捕获的是Attention输出投影后的a_l；SAE输入正是确认的Norm(a_l)，不是Norm(x_l+a_l)。前部挂点也必须同样用张量级对照证明。
- 固定主干和输入，改变SAE参数不改变LM logits；不小心插入串联替换、删除残差或改变主干Norm必须失败。
- LM-only不给SAE梯度；主重构梯度进入相应上游；target与能量分母保持detach；AuxK直接SAE-only。共享embedding是同一物理参数，输入端梯度不能冒充输出端路径；若选embedding挂点，这一点尤其重要。
- 每个SAE活动计数独立、跨rank同步，强制dead-mask测试有限非零AuxK且不更新主干。短Smoke未达到10M抽样窗口就报告自然防死未验证，不冒称长期有效。
- 全局LM/重构/AuxK归一化、独立LM/SAE梯度裁剪、raw与weighted日志、单字典/多字典聚合都符合确认卡；所有必需标量有限。
- 全局有效批量保持262144词元：seq2048、micro2时，4H100 accum16、8×5090 accum8、2×5090 Smoke accum32。端点不足整步时按真实mask精确计数。
- 完整存盘和独立进程恢复，模型、优化器、scheduler、RNG、数据/抽样游标、各字典活动状态及token/update坐标恢复；下一更新对照通过。

两模型运行在不同硬件上，仍需统一有效批量、数据顺序、初始化和日程；不要声称硬件数改变后的算力严格匹配或浮点位级一致，也不因此擅自更换已指定资源。

Smoke失败就停止正式提交并修复。若确认卡明确包含“通过后提交各50B”，通过后按该范围执行，无需再次泛问是否继续；否则按我确认的范围停在Smoke结果。本任务最先只能做架构确认，不能援引旧方案的直接提交授权跳过它。正式启动后只做短启动核对，不持续监督。

## 6. 最小来源与脚本地图

1. 当前新要求以本文件为准。旧交接：`/data/250010109/Research_System/Projects/from-attention-to-search/main/research_notes/sae_representation/20260916/sae_representation_followup/04_sidecar_50b_execution_handoff_cn.md`，仅复用地址与历史边界。
2. 来源记忆：`/data/250010109/Research_System/.research/memory/conversations/0914-training-excution/memory.md`。当前工作记录：`/data/250010109/Research_System/.research/memory/conversations/0914-training-scheduling-01a0a878/memory.md`，均读最新有效条目，不能从记忆创造科学批准。
3. 旧完整50B训练/恢复：`/data/250010109/MoE_Router/experiments/20260914_sae_mediated_live_auxk/dense_sae/train.py`、`engine.py`、`checkpoint.py`；模型在该目录`model/modeling_qwen3_sae.py`。旧串联前向不继承。
4. 之前准备的八层旁路草稿：`/data/250010109/MoE_Router/experiments/20260916_sae_sidecar_8l_pair_50b/`，其中`dense_sae/model/modeling_qwen3_sae.py`的`Block.attention_residual`返回`x + attention(norm1(x))`，旧sidecar挂在其后的Norm2，**正是本次要替换的位置**。源码冻结和CPU验收只覆盖旧设计。
5. AuxK实现：`/data/250010109/MoE_Router/experiments/20260914_sae_mediated_live_auxk/dense_sae/model/sae.py`。
6. 运行与提交：`/data/250010109/Research_System/docs/execution_envelope.md`和`/data/250010109/Research_System/templates/execution/acp_submit_template.sh`；5090运行层参考`/data/250010109/MoE_Router/experiments/20260913_dense_baseline_pretraining/scripts/activate_5090_runtime.sh`。

最终目标是可解释的作用位置比较。未经确认，不新增语义标签loss、不增加第三臂、不扩到每层SAE、不改变主干残差，也不把低重构误差当成语义促进。
