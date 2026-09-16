# 新一轮探索启动 prompt

下方正文可直接复制到新对话。它接续准备任务，不代替研究者批准科学状态或GPU预算。

---

请在 `/data/250010109/Research_System` 接续“四层模型 + 在线旁路 SAE 的从零预训练探索”。

先读：

1. `AGENTS.md`。
2. `.research/memory/conversations/0914-training-scheduling/memory.md`，完整累计记录。
3. `daily_research_reports/0915/sae_sidecar_small_pretraining/00_plan_cn.md`。
4. 同目录 `candidate_pair.json`、`data_audit.json`、`source_audit.json`、`compute_estimate.json`。
5. `docs/training_reuse_index.md`、`docs/training_observability_contract.md`、`docs/execution_envelope.md`。
6. 如需已有远程T的背景，读 `.research/memory/conversations/0914-training-excution/memory.md` 和 `daily_research_reports/0914/sae_mediated_pretraining/protocol.md`，不得把旧串联执行批准转移给新旁路。

研究目标：语言模型从随机初始化进行DCLM预训练时，语义领域结构是否在表征中逐渐形成；在线SAE重构梯度能否使结构更容易被读出，SAE能否追踪这一形成过程。训练没有领域标签；SAE产生的候选概念不能同时作为训练标签与证明成功的真值。后续画像对象先限定文本/模型的议题、立场、论证框架，不把领域词汇激活等同政治立场。

研究者已提出：主干缩小到4层、减小hidden；SAE10000维/Top20；使用DCLM并监督训练后观察表征。计划中的hidden512、FFN1536及精确预算是可审阅AI建议。资源明确允许考虑本地H100（当前2张、迁移后可能1张）、1张H100 Spot以及**两个独立的2×RTX5090 Spot任务，共4卡**；不是仅两张5090。envelope已登记`h100-1-spot`并扩展`5090-2-spot`在本探索的范围。不要依据旧Spot延后/仅分析记录反复询问是否允许考虑这些资源。资源选项不是5B执行批准。

当前任务先完成 P0：在 `/data/250010109/MoE_Router/experiments/20260915_sae_sidecar_small` 创建隔离实现、数据冻结和CPU验收；若目录已存在先审计，不覆盖。复用现有合格训练/data/checkpoint/runtime模块，所有新训练代码与原始执行材料放执行目录。研究仓库保留计划、证据索引和审阅结果。

候选配对：4层hidden512、FFN1536、Q8/KV4/head_dim64、seq2048、原151936词表和共享embedding、SAE10k/Top20。一份seed17随机LM+SAE状态复制成C/T。原生LM不消费SAE重构；最后块post-norm2/pre-MLP的h挂在线SAE。C仅SAE得到重构梯度，T的SAE和h上游得到；只切换辅助编码输入detach，目标/能量分母都detach；lambda_R=1、AuxK两组相同且SAE-only。不要永久冻结SAE，不加伪标签反馈、MP在线替换、多尺度损失、新余弦或额外种子。

实现时特别注意：

- 旧observer模式读取final_h，并非目标post-norm2；需要新挂接，不能只改JSON或模式名字。
- 2026-09-15磁盘源码已支持lambda范围且engine传了系数，旧“强制1且未传系数”的记录已过时；新副本仍需做配置→计算→梯度→raw/weighted日志验证。不要假定磁盘源码就是历史提交归档。
- 辅助梯度测试分别检查独立上游/下游参数，共享embedding在上游，不能因输出权重共享而误判为直接监督输出头。
- 推荐每条件双5090，两个独立ACP任务各自world_size=2/microbatch2/accum32/seq2048=262144有效目标。若采用单H100，则world_size=1/accum64，C/T串行或各占一张H100。复制初始完整状态和采样RNG，固定每更新token集合。不要把两个双卡任务变成跨节点4-rank训练，也不要新增两组种子。
- 双5090保持当前默认镜像，复用现成torch2.8/cu128运行层，在新runtime中明确识别`5090-2-spot`；旧脚本只识别4/8卡。资格覆盖SM120、单卡32GB显存、BF16/SDPA/CE/TopK、DDP计数/活动同步和恢复，不修改base环境。两组用相同硬件和软件环境；先比较合格平台的实测吞吐、排队、恢复代价再选择，不同时启动多个候选平台的重复5B。单/双rank恢复须验证全局样本顺序与各rank RNG，未通过则正式轨迹拓扑固定。
- 5B是每条件5000000000有效预测目标；成对共10B。原始前缀需要5000001537 token；最后序列512有效目标、末更新127488目标；两组精确匹配，无数据循环。
- 预热后恒定与AdamW沿计划；保留100步Smoke、1024步早期门、约1B开发、候选5B延长的阶段边界。不要把刚过预热的无信号当科学失败。
- 主指标在原始h上，用前256位置平均池化和固定M2D2 800 fit/400 dev的8类宏F1；单token读出次要。M2D2只评价、不反馈训练，也不是未触碰确认集。
- Spot必须有原子完整状态、100更新恢复间隔、run-root/contract连续性、抢占回执和物理重算计数；恢复不得只看metrics尾行。

P0交付：可审阅源代码与来源hash、可运行但未提交的C/T配置、参数计数、数据前缀与tokenizer冻结、CPU梯度归属/系数/末批/恢复验收、确定性forced-AuxK资格、TensorBoard、单卡入口及每条件双卡DDP入口。通过后给出一张具体Smoke卡：两组各≤100更新/各≤1 GPU小时（双卡每组≤30分钟墙时），候选资源本地H100、单卡H100 Spot或两个双卡5090 Spot任务，明确所选平台、预算与失败停止。除非本对话另外明确授权GPU执行，做到此卡后停在可审阅状态；不自动启动5B。

如果研究者已在本对话明确授权阶段，直接完成该范围，不重复询问同一批准。若授权Smoke，实测后用 `compute_estimate.py --throughput 实测有效目标每秒` 更新5B估算，报告训练与评估/存盘、抢占/排队分别多少；不能只报FLOPs估算。若获长期运行授权，按要求设置唯一监督owner与持久恢复，通知失败/阶段结束/ETA变化；不能声称当前聊天结束后仍在监督，除非持久机制已配置并验证。

PROJECTS中的旧SAE路由Focus不能拥有这个新问题；候选problem_key `sae_sidecar_pretraining_structure_formation`、owner和科学状态尚待研究者确认。先把具体实现与实验卡准备好，勿依靠memory创建科学批准；也不要因这些正式归属尚待确认而停止已授权的P0准备。

论文启示：Matryoshka是多尺度字典约束候选；MP-SAE是检验普通SAE读出盲区的离线对照。先完成最小在线TopK配对；只有具体证据触发时才扩展。已有远程串联T与Dense用于只读轨迹观察，不替代新C/T因果比较，不修改或重提已有任务。

结束时交付：改动和复用说明、关键验收、具体可批准卡、未解决问题、下一条最小动作。新对话如需memory，按自己的实际对话名建立记录并链接本记录，不覆盖`0914-training scheduling`。
