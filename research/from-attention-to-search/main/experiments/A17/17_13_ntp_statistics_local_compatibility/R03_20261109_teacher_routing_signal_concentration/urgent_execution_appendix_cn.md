# R03 紧急计划：执行事实与证据附录

当前结果为**单种子的中途描述性比较，科学判断 Unknown**。研究者将核心任务改为 A1 对 A2 的 2000 步比较；本附录不改变 Anchor、Focus 或冻结的 R02 结果。现行执行授权见 [Protocol 紧急修订](protocol_cn.md)。早期 3815 步计划和失败记录保留为历史，不是当前完成状态。

执行根为 `/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration`，下称 R。2000步统一结果见 [Summary](summary_cn.md)。早期交付入口为 [紧急执行报告](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/urgent_report_cn.md)。

## 要比较的对象与当前读数

原 Prompt 的问题是：按 teacher feature 分发，是否使长尾信息学得更快，所观察到的变化能否与信号集中度联系起来。A1 与 A2 都把同一个 token 交给两个专家、各取权重 0.5；两者的区别是分数来自冻结 teacher feature 的聚类，还是可重放的随机数。固定路由分支不通过 router 向表征反传梯度。A0 是原生路由；A4 增加仅更新 router 的蒸馏项；A1-deep 只在后四层使用 teacher 固定分数。它们是原 Prompt 定义的不同条件，不能把共同变化自动归因于某一个中介量。

五臂的总体 EVAL NLL（自然对数单位/有效预测 token）如下。500 步是额外的中途预览；1000/1500/2000 是研究者指定的交付点。

| 步数 | 有效训练 token | A0 | A1 | A2 | A4 | A1-deep |
|---|---:|---:|---:|---:|---:|---:|
| 500 | 131072000 | 5.591045 | 5.563205 | 5.768516 | 5.618351 | 5.515214 |
| 1000 | 262144000 | 4.628777 | 4.682595 | 4.845255 | 4.685438 | 4.622654 |
| 1500 | 393216000 | 4.253703 | 4.312842 | 4.457404 | 4.300965 | 4.245135 |
| 2000 | 524288000 | 4.083142 | 4.157604 | 4.286028 | 4.129442 | 4.085093 |

- [500 步完整表、差值、图与来源](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/analysis/urgent_step0500_1794186131200204225/report_cn.md)。
- [1000 步完整表、差值、图与来源](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/analysis/urgent_step1000_1794187368656337385/report_cn.md)。
- [1500 步完整表、差值、图与来源](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/analysis/urgent_step1500_1794188725469468032/report_cn.md)。
- [2000步统一分析、趋势与loss曲线](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/deliverables/1109_teacher_routing_2000_20261109T022417Z/README.md)。A1/A2均已保存并评估2000步；全包只比较≤2000步。[完成证据](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/evidence/urgent_2000_completion_certificate.json)。

## 数据、测量和读图

训练复用原 507988992 参数、8 层/1024 hidden、8 expert/top-2 MoE，来自同一 seed17 的随机初始权重。每步四个数据并行 rank，各两次累积、每次16条2048-token序列，独立计数为262144个有效目标 token。原学习率是1000步线性预热后恒定；实际原配置 horizon=50B，teacher checkpoint 位于33B，不把“33B checkpoint”误写成原调度总长度。新目标没有压缩或重启预热。

训练数据为 `dclm_pair_v1`。DEV 与 EVAL 各2097152个位置，来自训练视图排除的同一验证源分片内不同文档区间。按实际预处理分隔符划界；没有全语料近重复文本穷尽证明。feature ID 是冻结 teacher SAE 的30000维字典，不是学生内部已匹配的同名 feature。各臂都在同一 EVAL、同一组 teacher feature 激活位置上测 CE。

bin 按冻结 DEV 的 feature 激活频率划成十组。bin NLL 是其中所有 feature 激活位置的 CE 总和除以激活次数总和。同一 token 可激活多个 feature，因此这些 bin 不是互斥 token 分区。主差值是 **A1 NLL − A2 NLL**，负值只表示该点 A1 的数值较小。

集中度沿用 Prompt §6 和 `evaluation.concentration`：覆盖率是 feature 激活时专家被选中的条件概率，纯度是专家被选中时该 feature 激活的条件概率，分母频率来自 DEV。先计算各层的实际路由集中度，再在图3中对8层取算术均值，之后取自然对数；逐层原值保留在 EVAL payload 和 A0 CSV 中。这不是 log 值的平均。

图3的每个点是一个 teacher feature：横轴为该臂相对 A2 的 Δlog M̄，纵轴为 NLL(A2)−NLL(该臂)。图中使用含当前 load bias 的**实际路由**，不是训练前 b=0 的预登记预测。原始点坐标见同目录 `fig3_*_features.csv`。500步主图已实际检查，无裁切或坐标歧义；后续中央交付图按同一过程检查。30,000个 feature 不是30,000次独立训练重复。

原 Prompt 已登记逐 feature Spearman 秩相关。A1 对 A2 的点估计为：500步0.311408；1000步0.260775；1500步0.233929；2000步0.255924。相关区间、支持/削弱判定均不补造：研究者未指定 feature 家族映射，家族 bootstrap 区间 Unknown；目标 loss 未指定，达标 token 数 Unknown。不能把点估计代替所需区间。

## 授权与实际执行的核对

| 项目 | 当前授权 | 实际与证据 | 状态及边界 |
|---|---|---|---|
| 冻结旧臂 | A0@2000，A4/A1-deep@2573；先暂停三后续臂 | `chain_manifest_main.json`、`chain_manifest_secondary.json`；旧存档保留 | 已执行；A0未保存的2001–2264日志是历史尾段，不续跑 |
| 主对比资源 | share A2、P12 A1，各4 H10080GB Reserved、16c256g | `pt-4bh1k6uc`、`pt-kw43x8ls`，两份ACP回执与 `urgent_jobs.json` | 两个工作区、两个独立4卡allocation；不改数值批量 |
| 从零开始 | 同一随机初始状态 | `runs/A*/fresh_start_receipt.json`、`urgent_startup_certificate.json` | 两臂初始身份一致；正式首段与各自50步Smoke loss差0 |
| teacher 分片 | 核验0–2000，每个micro的input_ids哈希一致 | 实际额外核验到2573，10296分片、20592个micro哈希，全PASS | 无缺失，无补算，无跳过；运行时继续逐micro核对 |
| DDP遥测 | 关闭每expert梯度噪声comm hook并记录原因 | 使用原生DDP reducer；TB关闭标量与原因已读回 | 旧hook版本配对40步验证不自动转移到新版本 |
| 评估/存档 | 每250步；所有rank同步，写盘不与NCCL异步重叠 | 评估和保存前后barrier，同步不可变快照写盘；每250步至2000的边界实际通过 | 完整manifest发布后才登记存档；保留全部新存档 |
| 超时与错误 | NCCL30分钟，异步错误处理，失败显式退出 | trainer设置及 `scripts/urgent.sh`；A1 Smoke退出异常实际触发重启 | 不是长期无故障证明 |
| 任务内恢复 | 异常后30秒，最近完整存档auto，最多3次重试 | `urgent_runner.py`、`urgent_runner_A1.jsonl` | A1实际从50步末尾恢复，未重复optimizer updates |
| 指定交付 | 同步数≤2000，单种子，科学判断Unknown | `analyze_morning.py --step <step>`；出现次数/bin严格对齐，源文件哈希 | 500、1000、1500、2000完整；2000五臂50个bin单元全部对齐 |

A1 的50步更新、完整存档和EVAL已完成后，首次退出发生NCCL heartbeatMonitor/TCPStore连接重置。实际安装的PyTorch 2.3源码表明，默认 `destroy_process_group` 不主动关闭NCCL backend；修复开启 `TORCH_NCCL_ABORT_IN_DESTROY_PG=1`，不改变模型、数据或优化器。异常原日志、30秒等待、恢复和正常退出全部保留。A2已运行的进程保留其已加载退出路径；若同类退出异常重现，任务内重试加载修复版本并恢复保存的端点。证据见 `evidence/urgent_teardown_repair.json`。

## 三类审计记录

1. **识别审计**：主对比及后续A3/学习率/deep条件来自原Prompt §3/§8和研究者紧急授权。A1与A2比较改变了token共享专家的结构；集中度、语义对齐和实际负载可能一起变化，不称为独立操纵M̄。当前只报告相同步数NLL和实际集中度，机制与研究者最强替代解释判断均Unknown，不把运行完成当成科学认可。
2. **数据与统计审计**：一个训练种子；共同初态、原输入顺序、全局批量、冻结DEV/EVAL/SAE身份；0–2573分片逐micro哈希通过。五臂EVAL feature出现次数与频率bin完全一致。总体NLL与feature出现次数加权bin NLL分开；家族映射与loss阈值缺失不阻塞独立的描述性输出，不制造区间或达标数。
3. **实现与数值审计**：实际参数量、fixed router梯度/哈希、偏置与目标计数、原调度、bf16与TF32关闭均按实际源代码和运行回执核对。新50步Smoke通过；新旧A1/A2前10步的输入及loss差0，只限定首段。新版本外部打断后长期轨迹等价性未重做，不借旧版本证明。完整250步边界已经反复通过；源代码版本、恢复异常、不同退出清理路径明确记录。

审计只是数据、实现和来源核对，不改变科学状态。三类审计的源证据分别是 Protocol/原Prompt、`urgent_score_audit_0_2573.json`与各步analysis/source/status、`urgent_startup_certificate.json`和实际checkpoint manifests。

## 本轮六项记录与后续动作

- **问题/假设**：沿用原Prompt关于teacher分发、长尾学习和集中度的检验；本次优先得到A1对A2在2000步的匹配读数，不修改数学假设。
- **设置/对照**：五臂含义和同一步数控制见上文；A1/A2训练数值路径相同，退出清理补丁差异已明示；旧A0/A4/deep使用原遥测版本，跨版本比较保持描述性边界。
- **训练数据**：`dclm_pair_v1`，seed17，原4-lane样本顺序，262144有效token/步。
- **确认数据**：同一冻结EVAL的2097152个目标token，同一teacher SAE feature和DEV频率bin。
- **结果**：500/1000/1500/2000步实际读数及哈希见上表和analysis目录；五臂2000步均使用其自身同一步数存档/评估。
- **认识/边界/下一决定**：科学认识与下一科学决定Unknown。已授权的执行动作明确：A1/A2均2000后续2573，再A1-hi→A0-hi→A3各2000。研究者随后要求停止续训监督并先交付2000步统一结果；前台urgent_watch已停止，未停止ACP任务。任务内自动接续保留，不宣称后续臂已完成。不commit/push。

## 资产与复现入口

- 共同初始状态：`checkpoint_moe_baseline_dense_aligned_initial_20261030`；数据：`dclm_pair_v1`。
- DEV/EVAL/字典缓存：`dataset_teacher_routing_dev_eval_20261109`、`representation_teacher_routing_sparse_codes_20261109`、`analysis_teacher_routing_frozen_clusters_20261109`。
- 已逐micro核验的分数前缀：`representation_teacher_routing_training_scores_through_002573_20261109`。
- 旧臂实际保存状态：`checkpoint_family_teacher_routing_r03_training_A0_through_002000_20261109`；`checkpoint_family_teacher_routing_r03_training_A4_through_002573_20261109`、`checkpoint_family_teacher_routing_r03_training_A1_deep_through_002573_20261109`。
- 新实际存档：`checkpoint_family_teacher_routing_r03_training_A1_through_002000_20261109`、`checkpoint_family_teacher_routing_r03_training_A2_through_002000_20261109`，家族清单包含每250步至2000全部实际manifest。
- 本次访问回执：[strict access](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/evidence/urgent_assets_2000_access_20261109T0214Z.json)。登记与strict只证明所列文件的存在/访问，不替代恢复等价性或科学认可。
- 复现指定分析：在R执行 `python analyze_morning.py --step 2000`。两臂正式训练由 `scripts/urgent.sh A1|A2` 和 `urgent_runner.py`驱动；配置为 `arms/<arm>.yaml`；日志为 `logs/<arm>/urgent_target*.log`；正式TB为 `tb/<arm>/`。
- 代码和数据版本：原始复用diff、紧急修订前备份、`urgent_release_20261109T002855Z`、`urgent_teardown_repair_source/`及各analysis/source/和status中的输入artifact SHA256。
- 监控：`evidence/urgent_status_history.jsonl`、`evidence/urgent_watch_events.jsonl`、`evidence/urgent_live_status.json`；对话日志 `.research/memory/conversations/1109-teacher分发训练与2000步分析/memory.md`。监控最新日志按实际写入时间选择，不把50步Smoke日志当作正式训练尾部。


## 交付与监督范围的最新变更

研究者要求先统一2000步、打包并分析，暂不监督续训。本附录的训练状态止于2000步完成证据及停止监督前的检查；不再持续轮询。正式A1/A2从2000存档恢复的检查保留在执行侧，后续结果不混入本包。脚本/命令/版本索引见当前对话memory目录中的 `scripts_inventory.md`；科学判断仍Unknown。
