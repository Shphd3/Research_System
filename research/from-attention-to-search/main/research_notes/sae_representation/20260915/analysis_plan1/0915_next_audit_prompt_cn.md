# 给 sol high 的续接 prompt：三模型 0–10B 表征审计

更新于2026-09-15，取代本文件此前“等待宏观裁定”的版本。研究者已经裁定范围和 **2×H100 Spot** 资源，不再回问这些问题。当前文件存在不等于已提交任务；服从新对话中实际给出的审计或执行授权。

```text
请以 sol high 完成 /data/250010109/Research_System 的三模型共同0–10B表征审计续接。

第一步按顺序阅读：
1. AGENTS.md。
2. Projects/from-attention-to-search/main/research_notes/sae_representation/20260915/analysis_plan1/0915_SAE_three_model_execution_plan_cn.md 全文，这是最新完整plan。
3. 同目录 0915_three_model_analysis_spec_v1.json、0915_three_model_source_snapshot.json、0915_local_remote_resource_audit.json。
4. .research/memory/conversations/0914-training-scheduling/memory.md 全文的最新条目，以及 .research/memory/conversations/0914-formal-representation-audit/memory.md 全文与其方法/数据来源。
5. docs/training_reuse_index.md、docs/execution_envelope.md，以及计划指向的实际模型/分析源码。原0915_SAE_three_model_audit_plan_cn.md仅为历史输入，前轮review解释修正原因。

研究者已确定，不需要再次讨论：
- 领域可读性为主，命题单独报告且不是主结论。
- 只比较已有Dense/previous SAE/current SAE，全部共同0/0.5/1/3/5/10B；不新训LM或SAE。
- 数据为冻结360句主面板＋学术M2D2八类1200行开发复核；不新增Wikipedia或DCLM held-out。
- raw-h与实际MLP输入都报告。
- 固定数据、单种子、探索性轨迹；不把M2−M1写成纯detach因果效果，因为AuxK也不同。
- 原始A部分和中心化/去第一奇异方向B部分清楚分开；B是必做内容，不能覆盖A或择优挑变体。
- 不做Phase6/feature ID对齐，不设置新训练启动标准。
- 远程为一个单节点双H100 Spot作业，resource_profile=h100-2-spot，image=shphd-lite-0911。不是reserved、不是本地整卡、不是两个双卡任务。当前容器仅MIG3g.40gb/CPU配额8核/内存128GiB；本地做有界审计，耗时测量和CPU统计放远程。

先核对计划可实现性并写简短审计结论，再在 /data/250010109/MoE_Router/experiments/20260915_three_model_representation_audit/ 隔离实现，所有活跃训练目录与checkpoint只读。严格复用已通过的数据/源码身份审计和可复用缓存；原864句、其他模型M2D2缓存、19B选列均不能填入本轮。

关键技术坑：旧缓存sae_mediated实际上是M1；原训练forward键与旧分析适配器不同；该模型没有block.mlp模块，应核对最后norm2输出与gate/up输入。M2加载保留AuxK buffer，不能strict=False悄悄丢字段。共享embed兼任输出权重，重构梯度到embed不证明梯度穿过下游MLP。Dense终态TensorBoard对齐FAIL保持公开，不能混成checkpoint坏掉或已修复。

按plan冻结P/N划分、读取/池化、关系配对、fit-only标准化、6个probe头/4C、N末位辅助、Fisher公式、5000次成对重采样、梯度每点4批×8行、全部18点和A/B输出。B1中心化对已标准化probe和trace Fisher数学等价，要做等价自检；B2/B3确实删除一维，使用对应A已选C重拟合。不用标签/报告集拟合SVD。命题和高低词面分层保留为次要报告。

执行边界：
- 本prompt的文件本身只是计划入口，服从我在新对话实际给出的审计或执行指令。
- 若我只要求审阅：完成来源检查、实现方案/必要有界CPU检查、具体资格与执行卡，不提交作业。
- 若我明确要求按计划执行：在我确认的范围内，通过仓库模板dry-run后提交上述2H100 Spot；先做plan的S2资格与实测速率，再做全部测量。预算候选为累计远程6小时、最多12GPU小时；如未明确批准该预算，先交付该具体卡，不能自行扩大预算。
- 无LM/SAE optimizer.step、无buffer写回、无新训练、无旧任务停止、无其他资源自动fallback、无commit/push。probe拟合是评测的一部分，不是主模型训练。
- 2卡按checkpoint独立分工，不用DDP同步梯度；最多4CPU分析worker，每worker4BLAS线程。实现Spot缓存原子完成标记和按未完成单元恢复。重提必须在实际获准的次数/累计预算范围内，不能无限重试。

时间要求：以2–5小时远程计算为未实测先验，不含排队抢占。S2测真实I/O、推理/梯度、dense/sparse probe时间，更新完整工作量ETA。超预算先保存并报告；不静默少模型、少点、少数据或省掉B部分。资源已明确选择，不再问Spot/reserved。启动监督按AGENTS短窗口规则，不默认持续占用对话轮询。

最终交付：执行来源/资格/耗时/失败回执；完整缓存清单；A_raw与B_common_direction独立的指标、逐样本预测、三对差值、曲线/热图/示意图；命题次结果；梯度层级表；原模型参数/buffer未变的核验；读者报告和不能声称的边界。科学机制判断和最终解释留给研究者。给新对话建立自己的工作memory，链接来源，不覆盖0914-formal representation audit或旧scheduling记录。
```
