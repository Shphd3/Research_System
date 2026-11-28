# Protocol：路由—表征梯度反馈对照训练

## 0. Approval Snapshot

状态：APPROVED_FOR_IMPLEMENTATION_SMOKE_AND_PASS_GATED_SUBMISSION。批准来自[研究者直接请求及最新修订](../../../handoff/researcher_request_cn.md)和当前执行委托。研究者委托执行者具体化模型、优化器、预算与后测；这覆盖 skill 默认重新逐块确认流程，不冒称每个超参数由研究者指定。R1 登记时间：2026-10-05T09:37:28.180373+00:00。A-G 核心/范围由请求确认；工程细节 DELEGATED_AND_REGISTERED，跨块自行审计，资格须实测。科学门槛、最强对手排序、采用和关闭仍 Unknown。[Focus](../../focus/focus_router_representation_gradient_feedback_cn.md)、[Anchor](../../problem_anchors/router_representation_gradient_feedback/anchor_cn.md)。两种硬件 Smoke 均 PASS 后，各一次正式提交 A4H100 reserved、B8RTX5090 spot，只保存直接回执立即停止正式轮询，不等待运行、首步或完成，不设监控或自动重提。

## 1. Terminology / Definitions

r 是残差相加前 Attention 输出，h 是相加后归一化专家输入。detach 只切断 router 对 r 的导数，保留数值与 router 权重梯度。valid token 是非忽略的下一 token 目标。A/B 是算法；H/G 是 Smoke 硬件，每种硬件都运行 A/B。

## 2. Anchor Alignment

全部12层干预 LM gate→r 边。CE 检验有限轨迹效用；模型内部匹配负载的路由替换读功能依赖。路径恒等式是实现资格，不是学习发现。单 seed、算法与硬件完全混杂。

## 3. Tested Hypothesis

双向开放，B减A CE 正值支持 A 的有界效用，负值支持 B。只几何变化不证明效用。次要指标不能挽救失败的主效用。

## 4. Rival Explanations

可信对手包括梯度幅度/Adam 状态、实际负载/专家曝光、硬件 kernel/归约拓扑。无第三臂作独立识别。两种硬件 Smoke 同初态 A/B 短窗、共同库/数学模式及数值差只诊断，不能消除长期硬件解释。

## 5. Data Construction And Provenance

训练 view=/data/250010109/training_data_views/dclm_pair_v1/train，manifest SHA256=8a91bdbb0eb537bd80612015b99f178ca1cbb54a2fa7cf8442ab1eae7f0a2f2d。核验完整 path/size/target 清单、validation 排除和起中终样本。不是1.2TB全内容 hash。首遍顺序固定，无 epoch 重复；每更新256条连续1024预测目标样本，卡数只改变划分，不改变全局批次。边界输入重叠，目标不重叠。Tokenizer=/data/share/Qwen3-0.6B-Base，仅 fingerprint/load tokenizer，不读预训练权重。后测用独立 global-shard02 原文；analysis_manifest 冻结源hash、文档和tokens。只保证来源分片隔离及面板内文本去重，不证明全语料语义去重。

## 6. Learning Task And Permitted Supervision

只用因果前缀预测下一 token。无 ignore 目标；独立计数不等于源元素数立即失败。router 不读领域标签/未来目标。Smoke 只用训练样本。heldout 不参与训练、选模型或资格调参。

## 7. Model / Architecture And Frozen Variants

342,097,408 参数：hidden512、12层、8路由专家、top2、专家width1536、每层1共享专家、tied vocab151936、4attention/2KV heads、head_dim128、dropout0。不重归一化 top2，温度1、EMA none、aux0、无 token dropping、无 SAE/谱正则。唯一 A=false/B=true 的 router_input_detached，专家完整 h 始终 live。两臂 BF16 autocast、FP32参数/Adam状态、相同 mounted torch2.8/cu128 与 transformers4.53.3、SDPA、TF32 off、无 activation checkpointing、CE chunk256。硬件 SDPA 数值仍可不同。

## 8. Training Objective And Optimization

目标是全局 token-mean LM CE；raw router_aux 两臂均计算并记日志，weighted0，不反传。固定无ignore等长样本的局部均值/DDP平均等于全局 token均值。AdamW betas(0.9,0.95)、eps1e-8、所有组 LR1e-4、weight_decay0.01、fused=false、全局clip1.0。warmup128updates=33,554,432tokens；cosine 到 update7629 归零。终点1,999,896,576tokens，低于2B和10B。约2B用于控制首轮成本并读早中终变化，不声称收敛或计算最优。非有限在更新前失败，不跳步；完整累计并成功更新后才推进 token 坐标。不得根据正式结果/heldout调终点或超参数。

## 9. Conditions, Seeds, And Checkpoints

唯一seed1005；inputs/initial_state.pt 是 CPU 随机初态，保存文件与 tensor hash，每臂加载同一state，优化器 moments为空。seqlen1024、全部microbatch1：A正式4×64累计，B正式8×32；G Smoke2×128，H Smoke4×64。每更新262,144真实目标。weights保存updates0/64/1024/3814/7629，对应tokens0/16,777,216/268,435,456/999,817,216/1,999,896,576。rolling全状态10分钟或≥0.2B先到者，保留最新2个；终点完整状态保留。仅在本执行目录保存checkpoint/optimizer/RNG/weights。

## 10. Primary Metric And Frozen Analysis Plan

主终点只有7629，不选最佳早期 checkpoint。[analysis_protocol_cn.md](analysis_protocol_cn.md)冻结 paired B-A token加权文档 CE，整文档bootstrap5000、seed1005、双侧percentile95%。token是权重、文档是簇，数据bootstrap不覆盖seed不确定性。AI建议实用差异0.01nat/token，与0效应区间分开报，研究者采用门槛Unknown。

## 11. Secondary Metrics And Guards

严格遵守系统 observability contract；raw/weighted0 aux tags 两臂一致。每完整更新记load/entropy/dead、peak allocated/reserved、valid targets/s。任一层effective experts<1.5或≥6零load专家持续128全局更新，停止为LOAD_COLLAPSE。两臂同阈值/窗口，不切均衡算法。health EMA0.9，从128步起，EMA>log(vocab)+1、反转>2nat、embedding RMS ratio>4或logit RMS>20持续3步则失败。100GiB/臂cap；估计每臂约40GiB，含最新2个全状态、临时发布、终点与5weights。保留失败，不删除旧项目。

## 12. Known Good / Known Bad / Known Confusing Cases

好例：同状态前向logits/routes/gates/CE一致；隔离block同出向adjoint时router/专家参数梯度一致；expert-input与residual梯度存在，B router更新。完整多层网络较低层专家梯度可因上层detach间接改变，只要求末层router/专家梯度一致；独立 gate-only VJP 求和分解全部被移除边。坏例：detach专家h或gate权重应被路径测试识别；aux>0/top1归一化1拒绝。混淆例：相同logits、不同上游梯度是干预目的；更高有效秩而无CE收益不是支持。

## 13. Scientific Procedure And Stage Contracts

本地：核验source/data、共同初态/后测面板、tiny FP64路径恒等式、采样拓扑及CE chunk。硬件：H4H100 reserved、G2RTX5090 spot，各自同初态同样本A/B。同硬件完整模型前向atol/rtol1e-6；隔离FP64路径atol1e-10/rtol1e-8。保存梯度/VJP/router专家更新。跨硬件logits相对RMS≤0.02、CE绝对差≤0.02nat是预定工程阈值，routes近tie差异只报告，不强迫零；失败后不得无解释放宽。每A/B完成2次正式global-batch更新，在update1外进程checkpoint/resume；另有tiny外进程连续/恢复状态对照。生产形状peak<物理容量减2GiB且吞吐有限。G只资格2卡。
两硬件均审计PASS后冻结源/共同config，dry-run逐项比tuple。正式8卡内置world/rank、collective、分片/global batch、初态一致、OOM/finite自检，失败即停止，不自动切资源。正式A/B各一次create，保存直接结果jobID/错误；SUBMISSION_UNKNOWN不盲重提。提交后停止轮询，不设后台监控。

## 14. Algorithm, Output, And Provenance Contract

execution_surface=acp；image_id=shphd-lite-0911；H/A=h100-4-reserved；G=5090-2-spot；B=5090-8-spot。tuple仅从系统execution_envelope解析，使用系统acp_submit_template；回执保存展开镜像/command。env_layer=scripts/runtime.sh，使用现有隔离torch280_cu128_py310与Qwen3 HF层，缺层即失败，不改base。新执行root=/data/250010109/MoE_Router/experiments/20261005_router_representation_coupling。Smoke/full前锁code/config/request/Protocol/init/data/analysis hash。每run flock单writer、atomic/checksum manifest；同拓扑精确恢复限既有job内，不自动平台重提。owner=01a10b5e-939f-7302-ab6f-bac7b48758d9；formal监控=NONE_BY_USER_REQUEST。无commit/push/发布。

## 15. Success / Failure / Insufficient Evidence

工程PASS要求两种硬件的梯度/计数/恢复/TensorBoard/data/runtime/resource及数值阈值全部合格；FAIL阻断两项正式创建。科学：定向CE与功能证据支持有界继续验证；无收益/反向削弱对应方向；对手未分清、区间/终点不足=INSUFFICIENT。研究者持有采用和机制判断，Smoke不产生科学支持。

## 16. What This Cannot Claim

不能声称硬件无关算法因果、跨seed普遍性、必然防坍缩、冻结表示/固定路由、gradient dot保证未来效用、几何/域标签保证语义功能、所有共同适应、下游基准收益或收敛。

## 17. Block Confirmation, Freeze, And Amendment Ledger

R1：研究者最新修订覆盖最初两个8×5090。A4H100 reserved、G2×5090 Smoke、B8×5090正式及直接返回后停止已明确授权。模型/optimizer/预算/后测是受托具体化，不冒称A-G每个超参数逐项人工审阅。最强对手排序/科学门槛Unknown。运行前记录body/hash；运行后只追加含before/after、理由、已曝光data、资格影响和已有权限的amendment，不静默重写注册体。失败容差保留，不能改写PASS。实际执行记录由Detailed持有。


### Amendment A1 — 2026-10-05T09:54:38.943548+00:00, before GPU Smoke and formal data exposure

Original body retained. Source qualification disclosed FP32 casts inside nominal FP64 HF norms/softmax/CE: strict multi-layer VJP comparison failed with max residual1.65e-8 (receipts/local_gradient_contract_r5.log). A true FP64 independent reference now tests the unchanged chain-rule identity at original atol1e-10/rtol1e-8, max residual<8e-17. This qualifies the reference calculation, not production bitwise gradients. Native BF16 final-layer gradient/path GPU checks are prospectively atol2e-6/rtol2e-3 for reference-path subtraction and1e-6/1e-6 for parameter/forward parity; no failed GPU tolerance has been relaxed. Block F/G affected; initial formal weights/objective unchanged. Smoke optimization schedule is explicitly engineering-only warmup1/total2 updates, preserving actual production shape and262144target batch; formal warmup128/total7629 unchanged.

Runtime adaptation stays project-local: mounted torch2.8 libraries precede incompatible base CUDA libraries; optional base FlashAttention/torchvision are hidden for registered text-only SDPA. No base or shared dependency files edited. torchrun wraps preemption75 as launcher1: external continuation is allowed only after durable preempted_checkpoint_complete at step1 with manifest/checksum, inside the same Smoke allocation. Formal create calls never include scheduling polls. Existing scoped delegation authorizes these engineering repairs; science result NOT RUN.


## 修订 A2：诊断索引与 Smoke 重试（2026-10-05）

首轮 4H100 `pt-0bhf38z4` 与 2RTX5090 `pt-oz88x40i` 均在进入训练前失败。梯度指纹采用 FP32 linspace，对 77,791,232 元素的 embedding 张量把末索引舍入为越界值 77,791,232。改用 int64 `arange(16) * (numel - 1) // 15`；维度 1、2、4,096、2,359,296、77,791,232 的边界检查通过。算法、硬件、优化器、数据、模型、预算及验收容差均未改变。保留 v1 日志与源码锁；仅已确认 FAILED 的 Smoke 允许显式 v2 create，正式任务仍只允许一次 v1 create。重试前未生成 GPU 训练 run 产物。


## 修订A3：加入共同负载均衡后从头重训（2026-10-06T02:44:52.859460+00:00）

本修订覆盖本轮的aux=0、不监控与原正式v1仅一次条款；原文与失败记录保留为历史。用户本对话明确要求“请重提，重新训练，然后监督训练”，并选择“两臂共同加入负载均衡后重训（改变原训练目标，需要另列新条件）”。新条件`rrc_1006_balanced_r3`只含一对共同seed；原A `pt-9egkfirg`、B `pt-86fsmog5`不变，不使用不同步恢复点。无需再次询问提交许可。

两臂目标均为纯LM CE加0.01×router_aux。系数是原授权范围内的执行者具体化，提交前冻结。逐层、逐序列（1024位置）定义：f_i为专家i的top2槽数除以2048；pbar_i为该序列所有位置的softmax概率均值；L_l=8∑f_i pbar_i。均衡项先在12层平均，再在全局256条序列平均。均匀分配时为1。这是逐序列均衡，不是把整次更新的平均f与平均p相乘；两种卡数都保持microbatch1，因此目标一致。硬top2选择不求导。

**辅助项回传主干的路径必须相同。** 两臂辅助概率都重新计算为softmax(W stop_gradient(r))，仍更新router权重W，均不沿r回传主干。LM分支A为Wr，B为W stop_gradient(r)；完整expert输入h、共享专家及残差均保持live。故两臂差异仍只为LM门控反馈；不能将B多切辅助梯度后声称纯LM对照。新增均衡不保证不会再集中。

负载保护改为逐层计数：必须同一层连续128次越过原阈值。阈值、健康/有限性检查不变。恢复完整逐层计数。post-update保护退出前写终步metrics、TensorBoard、failure JSON及完整Adam/RNG检查点，不再丢失触发保护的更新；保护失败不自动继续。原tag保留，weighted=0.01×raw，total记录实际目标。

执行root：/data/250010109/MoE_Router/experiments/20261006_router_representation_coupling_balanced。模型、共同初态及hash、seed1005、数据/顺序/面板、AdamW、精度、262144targets/update、warmup128、终点7629updates/1999896576targets及weights0/64/1024/3814/7629保持原合同。A4H100 reserved、B8RTX5090 spot、默认镜像/隔离runtime不变。新目标需重新跑本地辅助路径正反例，以及4H100与2RTX5090两种Smoke；各硬件含A/B两次完整global-batch更新及step1外进程恢复。新双Smoke与跨硬件资格PASS后，新正式每臂各一次create；唯一回执防重复，无额外seed/臂或fallback。

监督由同一thread负责。此次“监督训练”覆盖旧的停止轮询要求。两个正式ACP任务各自运行任务内监督器，每30秒写supervision.json，仅状态变化写事件；不建本地定时任务或额外GPU监控任务。首步前30分钟／训练中20分钟无进展时写共享preemption请求文件触发优化边界的原子保存，再5分钟仍卡住则终止子进程。监督器不重提任务，也没有主动向桌面推送消息的能力；本对话核验启动与首步，后续监督状态持久化。

原失败274步训练读数已曝光，新TEST尚未读。不得把无均衡失败臂与本新条件合并为一个效应，不按早期CE改终点。单seed、算法与硬件完全混杂、研究者机制/采用/关闭判断Unknown的边界保留。
