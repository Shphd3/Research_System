# SFT 审计的资产、memory 与证据核验

工作日：2026-09-10；核验时间：2026-09-09 UTC。处理 Agent：Codex。

这是[开发计划](sft_representation_audit_plan_cn.md)的来源索引。以下将“可复用的文件/实现”与“足以支持的科学结论”分别写明；可加载、已完成、存在结果表都不自动变成机制结论。本次只读核验，没有重跑旧实验或更新其科学状态。

## 最新v2范围及本次新增核验

最新合同为[14条件全矩阵](sft_representation_audit_plan_cn.md)和[十配置离线附件](sae_hierarchy_offline_extension_cn.md)，覆盖旧单条件计划。全部模型重训以取得统一精度、分组裁剪和21检查点；旧模型提供数据/初始化/日程/教师及历史核验，不代替新主轨迹。

研究者确认主高层教师使用historical_depth_reference的support_qualified_graph中depth≥2原子。已按nodes.csv核验：depth0=99、depth1=198、depth2=27、depth3=1；因此高层主集28，非叶补集226。原全原子group映射缺其中4个ID（2712、4246、8335、29727），不能截旧稀疏邻接图就说完成high28构造。用历史discovery词元缓存重新计算28原子的全部正phi，已做只读可构造性检查：28个均出现，最少53次，26个正度节点、4个连通分量（含2个孤立点）。新教师因此需保留孤立点的明确构组规则，尚未在本对话拟合/训练。

结构约束仅更新router是研究者已确认决定。v2为隔离其即时梯度影响，采用attention/router/shared+experts三组分别裁剪；最后attention在F/U都用相同float32局部前向。固定t0教师目标是明确标注的AI默认，需执行回执记录；不能将旧h缓存认作新t0实现下已匹配。

离线十配置含原六个及原来标deferred/diagnostic的四个新增配置；本次用户明确授权参数层级探索，不自动选择最深图替换28主教师。下文关于旧结果完成度是此次核验时的历史资产状态，不等于新矩阵完成。

## 1. 给下一位 Agent 的最短阅读顺序

先完整读v2开发计划与离线附件，确定主对象、明确默认、全部矩阵和预算。再读下面的模型/训练快照、数据与初始检查点身份。只有需要解释旧结果时才读后训练表格；只有需要回顾原子关系时才读离线层级结果。不要一开始遍历全部历史运行，也不要把旧S0–S6作为本轮必跑工作。

导师要求的来源是[0909会议记录](../../../../../../../daily_research_reports/backup/2026/09/0909/docs/0909_组会逐句校订稿_含原文对照.md)：08:53、09:35、13:09、14:52附近。它支持“观察训练变化、讲清坐标与可证伪猜想”的研究方向；没有直接指定本计划的学习率、判据或完整远程预算，这些仍是讨论中的方案。

## 2. 模型与训练实现：能够直接复用什么

| 资产 | 本次核验 | 可复用范围与限制 |
|---|---|---|
| [本地Qwen配置](/data/250010109/model_cache/Qwen3-0.6B-Base-official/config.json) | 28层、hidden1024、16 query heads、8 KV heads、head_dim128、attention_dropout0 | 模型架构身份；不是新训练成本测量 |
| [A6R1正式manifest](/data/250010109/MoE_Router/experiments/20260909_online_sae_gmm_regularized_router_decay/runs/full-20260909T020300Z/formal_manifest.json) | snapshot的model/train/backbone/config/teacher五个文件哈希与manifest一致 | 优先从不可变run/source读实现，不让可变工作源码冒充当时执行代码 |
| [snapshot model.py](/data/250010109/MoE_Router/experiments/20260909_online_sae_gmm_regularized_router_decay/runs/full-20260909T020300Z/source/model.py) | Router与expert共享MLP pre-hook h；并行残差；实际路由含平衡bias，系数来自原生softmax | 复用注入、低秩专家、路由定义；增加只读提取器 |
| [snapshot backbone.py](/data/250010109/MoE_Router/experiments/20260909_online_sae_gmm_regularized_router_decay/runs/full-20260909T020300Z/source/backbone.py) | 加载后整个backbone `requires_grad_(False).eval()` | 证明旧h冻结；新构造必须显式开放最后attention |
| [snapshot train.py](/data/250010109/MoE_Router/experiments/20260909_online_sae_gmm_regularized_router_decay/runs/full-20260909T020300Z/source/train.py) | 优化器只含shared/expert和router两组；保存仅adapter；直接加载旧task-only起点与日程 | 复用身份、样本和损失口径；优化器、日程、裁剪、冻结断言、checkpoint必须一起改 |
| [本地Qwen实现](/data/250010109/dependency_packages/hf_transformers_qwen3/transformers/models/qwen3/modeling_qwen3.py) | 最后attention后残差→post_attention_layernorm→MLP→残差→模型最终norm | 支撑h、b、v的取点定义；还须锁定实际运行所导入的transformers路径/版本 |

每个低秩分支的参数数为 \(2\times1024\times16=32768\)；九个分支加 \(1024\times8+8\) 的router共303,112。attention投影为 \(1024(2048+1024+1024)+2048\times1024=6,291,456\)，再加两个长度128的归一化权重，共6,291,712；本次还从实际model.safetensors文件头逐张量形状核验了该数。执行时仍须用参数白名单验证真正被优化的成员。

## 3. 可重放的旧检查点与数据

旧task-only根目录：

`/data/250010109/MoE_Router/experiments/20260908_sae_h_input_balanced_router/runs/full-20260908T111248Z/`

新正则旧实验根目录：

`/data/250010109/MoE_Router/experiments/20260909_online_sae_gmm_regularized_router_decay/runs/full-20260909T020300Z/`

已检查 task-only及sae_a/gmm_a/sae_b/gmm_b共五条件×17/29/43×0/128/256/384/512，75个检查点均存在。15条轨迹的sample_schedule哈希与各自对应种子预期相符。这里只核对存在性、日程身份及三份task-only初始状态；未宣称本轮将全部75个检查点加载进模型重放。v1曾拟复用task-only的15个旧点；v2不以这些旧点替代新全轨迹，旧点只用于必要历史核验。

每种子的旧路径格式是 `conditions/task_only__seed{seed}/checkpoints/update_0000.pt` 与 `conditions/task_only__seed{seed}/sample_schedule.pt`。完整预期SHA见上述[config快照](/data/250010109/MoE_Router/experiments/20260909_online_sae_gmm_regularized_router_decay/runs/full-20260909T020300Z/source/config.py)，不要手工另造同名初始模型。三种子初始shared.b和experts.b全零已核验。

[固定data.pt](/data/250010109/MoE_Router/experiments/20260908_sae_h_input_balanced_router/runs/full-20260908T111248Z/data/data.pt)的SHA256：`58e409ca9d903d146c9ae8e3cee834a4eb5f0e6f2e24de4fe521349d05e527f2`。已读取字段与计数：

| source | development | test |
|---|---:|---:|
| mmlu | 2357 | 2357 |
| mmlu_pro | 1753 | 1753 |
| bbh | 976 | 976 |
| gsm8k | 1319 | 1319 |
| math | 1875 | 1875 |
| gpqa | 30 | 30 |
| humaneval | 25 | 25 |
| mbpp | 145 | 146 |
| 合计 | 8480 | 8481 |

训练39571条。现有payload还包含discovery/router等分区；它们不是新增独立test。字段有input_ids、attention_mask、labels、source、record_id、content_sha256、prompt_length、answer_token_count。评估主点必须从labels定位，不能仅因字段叫prompt_length就假定它等于截断后索引。

新h发生变化后，旧h缓存、固定教师target缓存不能直接当新h使用。原始文本、token序列、身份、日程可复用；旧表征缓存最多用于冻结参照。在旧冻结路径可缓存h和注入前b，再按各adapter重建v；新路径默认完整前向，优化缓存前必须做位置与数值相容验证。

## 4. 现有结果各自能支持哪一环

[A6R1后训练正式运行](/data/250010109/MoE_Router/experiments/20260909_a6r1_post_training_analysis/runs/full-20260909T052900Z/completion.json)及[阶段状态](/data/250010109/MoE_Router/experiments/20260909_a6r1_post_training_analysis/runs/full-20260909T052900Z/stage_status.json)存在并记录完成。S1是任务NLL，S2是路由关系，S3是专家干预功能，S4是更新兼容性资格，S5是局部动作，S6是顺序适应。S4记录`INSUFFICIENT`；S6注册机器映射也记录`INSUFFICIENT`，不能叫全部机制验证通过。

它们可以提供独立旧证据或实现参考，不能回答新模型的h时间轨迹，也不能把S2颜色对应改写成S3功能结论。本次核验时A6R1训练及其后训练目录尚未见canonical `summary.md`/`detailed.md`，所以不能从memory中的运行状态直接拿出一段研究者已确认的结论。旧A5和旧常数正则A6拥有自己的结果记录，不能混为A6R1。

离线层级最新核验根目录：

`/data/250010109/MoE_Router/experiments/20260909_sae_hierarchy_offline_analysis/runs/static-20260909T085200Z/`

[run_receipt.json](/data/250010109/MoE_Router/experiments/20260909_sae_hierarchy_offline_analysis/runs/static-20260909T085200Z/run_receipt.json)记录六条件全缓存静态计算完成；[static_analysis/receipt.json](/data/250010109/MoE_Router/experiments/20260909_sae_hierarchy_offline_analysis/runs/static-20260909T085200Z/static_analysis/receipt.json)记录分析完成，同时有记录映射不可用、语义结论未检验的边界。任务组成目录已有阶段1表和阶段2中间产物，但本次未找到足以证明阶段2全范围完成的总收据。因此标“静态完成、任务组成部分存在”，不要因新文件存在而抹去缺口，也不要因旧README而重跑已经完成的静态计算。

## 5. 三份 repository memory 的可用性

下面三份日志均已完整读取；它们是历史工作上下文，不是科学证据所有者。本次不覆盖或改写它们。

| memory | 当前可用内容 | 已核验的过时点／使用限制 |
|---|---|---|
| [0909-Router Regularization](../../../../../../../.research/memory/conversations/0909-router-regularization/memory.md) | 最后条目06:39:43，正确指向完成的A6R1后训练运行；提醒区分S1–S6 | 可作入口。`COMPLETE`不代表科学通过，Summary/Detailed缺口仍须面对 |
| [0907-SAE 路由有效性验证](../../../../../../../.research/memory/conversations/0907-sae-routing-validation/memory.md) | 08:39条目保留层级定义、门槛耦合、旧缓存缺口 | “仅21项合成检查、尚未真实静态运行”落后于08:52目录；实现入口可以用，最新完成度不能照抄 |
| [SAE/GMM online routing and post-training analysis](../../../../../../../.research/memory/conversations/sae-balanced-routing/memory.md) | 记录A5→online router→A6R1问题与范围演进，最后03:33:06 | “S6未实现／后训练未运行”已过时；当时授权仅属于当时实验，不能迁移成新attention训练授权 |

全局memory曾提供旧日期前缀的路径；本次已以当前实际目录名为准。`PROJECTS.md`和旧Focus的执行进度描述也落后于正式run证据。它们的科学归属和人类决定仍由原表面拥有，本任务只指出不一致，没有借机改变别的任务的科学状态。

## 6. 尚缺什么

新v2矩阵尚无本对话执行的训练、资格或完整审计结果；本轮交付是完整开发计划和Renew Prompt。42轨迹、882检查点及十配置离线范围已明确；数值不可定义、覆盖不足或某参数没有增加深度均需作为真实结果记录，不伪造完整性。正式problem_key/Focus/Anchor归属待正式化，不自动改变已有研究问题；执行授权来自研究者本次具体请求，不能从memory本身推导。
