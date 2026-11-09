# 转交分析 AI：语义组合复用的两轨分析

后续转交请优先使用[04_report_execution_prompt_cn.md](04_report_execution_prompt_cn.md)。本版保留历史；新版明确领域主线与更强同义检验的关系，并把待审核候选面板修订为保留4×3结构的360句。

以下文本供研究者转发。它指定工作对象与建议顺序，**不会自动继承旧 analysis1 的 GPU 授权，也不授权修改正在训练的模型**。研究者可以在转发时明确批准其中的实施、checkpoint-only 推理、离线 SAE 试拟合范围；未明确批准的范围保持计划状态。

---

请先阅读 `/data/250010109/Research_System/AGENTS.md`，再完整阅读：

1. `/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_17_three_model_sae_representation_trajectory/supporting_records/sae_representation/semantic_confirmation/20260914_v1/01_hypothesis_audit_plan_cn.md`。
2. 同目录 `audit_snapshot.json`，理解它是 2026-09-14 的只读时点快照，运行状态需要刷新。
3. `/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_17_three_model_sae_representation_trajectory/supporting_records/sae_representation/checkpoint_trajectory/20260914_audit/08_complete_experiment_report_cn.md` 及它引用的关键表。
4. `/data/250010109/Research_System/.research/memory/conversations/0912-梳理-sae-动态形成预训练方案/memory.md` 全文与当前 `continuation.md`；按需核对被引用的 `0912-sae-llm训练执行/memory.md` 全文。memory 不拥有科学判断和批准。
5. `/data/250010109/Research_System/docs/training_reuse_index.md`、`docs/training_observability_contract.md`；若本次明确批准远程执行，再读取当前 execution envelope 与相应技能，冻结确切资源、镜像、预算和作用域。

目标是检验一个具体的候选假设：固定外部语义标签下，随着预训练，同一命题的不同表达是否越来越复用相似稀疏组合，且相对于词面/主题匹配的异义反例，复用优势增大。领域分类是辅助变量，不替代命题等价。不要把它改成组合推理、feature语义原子、router/MoE或新loss实验。

两条轨道必须都可追踪：

- 第一轨：当前 SAE-mediated 模型本身的 `h / online z / online h_hat` 时间演化。
- 第二轨：同实际累计有效预测词元上的普通 baseline 对照。先比较两臂 h；要比较稀疏组织，再对两臂冻结 h 同规则训练离线 SAE，将 `online / offline_mediated / offline_baseline` 三类结果分开。

实际位置是最后块 post-norm2、SAE 前的 h。mediated 的 MLP 消费 h_hat，普通模型消费 h，原生残差旁路仍在。LM loss 穿过 SAE；独立重构 pass 输入/目标 detach，只更新 SAE。所有外部语义标签只用于分析。不要把 `final_h` 当作这里的 h，也不要把 mediated 的 h 当普通无干预训练。

训练输入路径：

- SAE：`/data/250010109/MoE_Router/experiments/20260912_dense_sae_pretraining/runs/full_50b_bottleneck8_202609121130/`。
- baseline：`/data/250010109/MoE_Router/experiments/20260913_dense_baseline_pretraining/runs/full_10b_8x5090_20260913T102944Z/`。
- 读取时点快照显示两边共同完整里程碑为 0/0.5/1/3B，之后按实际完整保存点补5/10B，不能按各自最新进度混比。主要最终窗口建议0.5→10B，0.5→3B是阶段分析，0B是初始化参照。没有0–0.5B密集快照，不能定位早期出现的准确时刻。
- 原SAE作业 `pt-x0dxui5n` 已暂停，续训是 `pt-srfey9kz`；baseline是 `pt-79x53njx`。状态仅供定位，不得恢复、停止或重复提交它们。
- SAE续训回滚后的权威 metrics 与 `recovery_history` 要分开，不重复计入被舍弃的更新。阈值提升的恢复点按实际tokens命名，不冒充精确17B等点。

在实施被批准后，建立独立执行目录：

`/data/250010109/MoE_Router/experiments/20260914_semantic_feature_reuse_analysis/`

先声明直接复用、改编和新写项。优先读旧 `dense_sae/analysis/semantic_evolution.py`、`checkpoint_audit.py` 与有效 `model/sae.py`。按原提交来源和依赖锁定版本；不要把新增文件放进运行 trainer 的源码合同扫描范围，不修改其配置/环境/检查点。旧模板化864句用于调试和探索，不能升级成新确认结果。

实施顺序：

1. 输出输入资格表：checkpoint完整性、tap、初始化、tokenizer、真实全局batch和顺序、优化器/LR、续训坐标、日志。SAE原run缺TensorBoard事件须显式记录，不能说已经满足训练曲线比较合同；可核验JSONL并另写带来源的事后派生结果，但不得冒称原生TensorBoard。重新评估的checkpoint loss与语义比较分别审计。
2. 按计划给出新320句命题面板候选及PAWS dev200/test800对抽样清单；历史8×8 data_v3只作层级辅助。研究者完成/确认命题等价审核后，冻结families、模板、来源、同义/异义×词面高/低的分层与统计权重；不按目标模型表现选题。公开数据不能假设每个pair独立，按共享源句或连通分量分组。
3. 编写简单可人工核对的 Jaccard、L1归一化激活的加权Jaccard W，报告 S+、S−、G=S+−S− 和各自端点变化。只计正激活，零码单列；全体同码应G=0，feature整体重编号不改变这些量。先在旧缓存做实现诊断并明确标记探索性。
4. 在明确批准的checkpoint-only范围内提取新固定面板。h/h_hat保存fp32；z只存indices/values；保存有效token位置、样本ID与所有manifest；不存N×30000稠密z，不用全句token并集冒充单位置组合。
5. 输出主复用曲线、h/h_hat原空间关系曲线、SAE质量轴与词面置换参照。复杂读出、少坐标容量曲线和跨时期关系矩阵是辅助，不得以分类/漂亮二维图替代组合主指标。
6. 若统一离线读法预算明确获批，先做0.5/3B×两臂4格；冻结LM，只更新SAE；M=30000/k=32，复用现有标准化重构，不新增loss。试拟合提案为每格1,048,576拟合位置、131,072验证位置，全局batch4096，256更新，一seed；这不是拟合充分性保证。先测质量与吞吐，再按共同规则提出扩量预算。最终主差异增加第二个SAE seed并补两臂10B，不能只延长较差一臂或用确认语义分数选训练步数。
7. 以命题/源句组做配对bootstrap，同抽样索引覆盖两臂/时刻。主W固定，J/余弦/探针为辅助。输出绝对水平差与增长差，不能称为唯一的形成速度或纯SAE因果效应。若最小关注差异尚未确认，只报估计与区间。
8. 写全正面、负面和不足结果；保留样本及reader资格失败。一个LM seed的限制不因bootstrap或多个reader seed而消失。完成自己的summary/详细记录与来源图，并在接手任务自己的memory中追加记录，链接来源continuation，不写入别的任务memory。

核心验收问题：

- 标签真的是同命题改写，还是只是同领域？
- 同义重合本身上升了吗，还是只有异义下降/所有样本一起集中？
- h、线上code、统一离线code的变化是否一致？质量相当吗？
- 词面、长度、模板和源句依赖是否解释了结果？
- 两臂是否在完全相同样本/词元点上比较？同读法预算是否匹配？
- 观测支持的是整体配置差异，还是已有足够干预证据谈机制？本轮没有后者。

最小交付：`checkpoint_manifest.json`、带审核与冻结记录的panel/pairs/triplets、配置与版本、cache manifests、`metrics_long.csv`、`paired_deltas.csv`、`sae_quality.csv`、`eligibility.json`、固定案例册、主图与清晰的结果读取面。精确schema、公式、判决分支、文件职责和预算见主计划。

遇到数据审核、读法拟合或输入资格不足，明确写 `INSUFFICIENT/NOT_RUN`，给最小补充建议。不要为了“完整汇报”推测缺失结果。若研究者只批准审计或本地实现，完成该范围后停止；远程推理、离线SAE、新预训练、干预、提交/推送各自不互相授权。
