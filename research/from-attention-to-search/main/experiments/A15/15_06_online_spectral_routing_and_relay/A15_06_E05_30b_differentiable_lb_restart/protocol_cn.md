---
experiment_id: A15_06_E05_30b_differentiable_lb_restart
anchor_id: 15_06_online_spectral_routing_and_relay
status: approved_for_implementation_smoke_and_full
approved_by: user
approval_date: 2026-08-09
resource_profile: 5090-8-spot
primary_metric: paired_seed17_30b_heldout_nll_across_five_arms_with_verified_lb_backward
---

# Protocol：A15_06_E05 可微负载均衡下的五臂 30B 从头重训

## 0. 批准与修复范围

此前 checkpoint 因 Switch 负载均衡（LB）辅助损失在 reentrant activation
checkpoint 路径中没有回传而被删除。用户已批准从 step 0 重新训练。本实验只修复
辅助张量的 autograd 传输，然后在同一个经过验证的可微 LB 目标下比较五种 Router。
旧 checkpoint 不恢复、不复用，也不进入新证据链。

五个条件为 `vanilla_full`、`local_hmt`、`local_random_matched`、
`relay_hmt`、`relay_random`；本轮不包含 Centered-Full。全部固定 seed 17，
分别使用一个单节点 8×5090 SPOT 任务训练到 30B token。

## 1. 唯一问题与主指标

在模型、数据顺序、初始化、优化器、训练预算均相同，且 LB 已证明能回传到 Gate
参数后，Local-HMT 或 Relay-HMT 是否在 30B held-out NLL 上优于 Vanilla-Full；
covariance 频带身份是否优于维度和动态完全匹配的随机对照？

主指标是 30B 终点的配对 held-out next-token NLL，单位 nat/token，越低越好。
负载、路由熵、投影连续性和 LB 梯度只解释过程，不能替代终点质量裁定。

## 2. 模型、数据与优化器

五臂共享四层 Qwen 风格 top-1 MoE：hidden size 768，6 个 query head、3 个
key/value head、head dimension 128，每层 8 个稀疏专家加 1 个共享专家，专家
intermediate size 1,536。实际构造必须报告 251,199,232 个可训练参数和每 token
152,108,800 个激活参数；Router 参数总计 24,576。

数据固定为
`/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10`，序列长度
1,024，global batch 768，每个 optimizer step 为 786,432 token。使用 BF16、
AdamW、学习率 \(10^{-4}\)、betas \((0.9,0.95)\)、weight decay 0.01、636 步
warm-up、100B-token scheduler horizon、ZeRO-1 和 activation checkpointing。

## 3. 五个 Router 条件

- **Vanilla-Full：**每层 Gate 读取未去均值的本层完整表征。
- **Local-HMT：**第2/3/4层读取本层动态 centered head/middle/tail；第一层读取
  centered full。
- **Local-Random-Matched：**与 Local-HMT 的维度、来源和 tracker 运动一致，
  但用固定 Haar 旋转删除 covariance rank 身份。
- **Relay-HMT：**第2/3/4层读取可训练第一层来源的 centered H/M/T。
- **Relay-Random：**与 Relay-HMT 完全匹配，但使用固定 Haar 随机旋转。

专家始终接收完整本层表征；Relay 梯度允许回传第一层来源。covariance、特征
分解和 Grassmann 更新继续作为不可微控制状态。

## 4. 可微 LB 合同

对每层每个 microbatch，\(p_i(x)\) 是 expert \(i\) 的完整 softmax 概率，\(f_i\) 是
hard top-1 token 比例：

\[
L_{LB}=8\sum_{i=1}^{8}\left(\frac1T\sum_xp_i(x)\right)f_i,
\qquad
L=L_{LM}+0.01\sum_{\ell=1}^{4}L_{LB,\ell}.
\]

hard assignment 比例只作为 stop-gradient 系数；soft probability 路径必须可微。
activation checkpointing 必须继续开启。修复只允许改变辅助张量穿过 checkpoint
的 autograd 传输，不改变 LB 公式、top-1 分配、forward 数值、数据或优化器。

full 提交前，五臂必须同时通过：

1. 每层 `lb_loss` 为有限值且拥有 autograd function；
2. LB-only backward 对每层 Gate 产生有限且非零梯度；
3. LM-only 与 LM+LB shadow 使用相同 step-0 权重和 batch，加入 LB 后 Gate 更新
   确实非零；
4. checkpointed 与非 checkpointed forward 在注册精度内一致；
5. full 命令仍明确启用 activation checkpointing。

仅看到非零 LB 数值或 `lambda_lb=0.01` 不算通过。

## 5. 预算、保存点与续训

全部从 optimizer step 0 开始，在 step 38,147 结束，即 30,000,021,504 token。
只保留以下完整恢复点：

| 标签 | step | 实际累计 token |
| --- | ---: | ---: |
| 2B | 2,544 | 2,000,683,008 |
| 5B | 6,358 | 5,000,134,656 |
| 10B | 12,716 | 10,000,269,312 |
| 25B | 31,790 | 25,000,673,280 |
| 30B | 38,147 | 30,000,021,504 |

每个保存点必须包含模型、8 个 optimizer shard、scheduler、RNG、数据游标、
running means、covariance EMA、部署嵌套基底、随机 frame、刷新计数和连续性
telemetry。full 前必须用“连续运行 vs 保存后恢复”验证精确续训。SPOT 抢占后只
允许从最近一个完整注册保存点恢复。

## 6. 配对、评估与过程记录

五臂共享 step-0 公共参数、token hash、适用范围内的 dropout/RNG 序列、学习率
曲线、评估文档和保存时刻。arm-specific buffer 必须确定性初始化，且不能消耗
公共模型 RNG 流。

每个保存点都要能够重建逐层专家占比、路由熵、LB 数值与系数、LM/LB Gate
梯度范数、projector gamma/flip/lag、吞吐和 TensorBoard 曲线。终点在同一
held-out 文档上做文档级配对 bootstrap。主比较为 Local-HMT−Vanilla、
Local-HMT−Local-Random、Relay-HMT−Vanilla、Relay-HMT−Local-HMT 和
Relay-HMT−Relay-Random。

## 7. Smoke 与工程门

顺序为依赖轻量单测、真实单卡 smoke、五个独立 8×5090 分布式 smoke。每个
分布式 smoke 必须验证 forward/backward、逐层 LB Gate 梯度、共同 step-0 参数
hash、逐步 token hash、在线投影正交/嵌套、TensorBoard/JSONL、完整 checkpoint
保存，以及模型、优化器、scheduler、RNG、数据游标和在线状态的精确恢复。

NaN/Inf、OOM、分布式状态不一致、checkpoint 损坏或 LB Gate 梯度缺失会阻止
full 提交。负载集中、NLL 变差、flip 偏高或 gamma=0 是科学结果，只要数值和
状态有效就不能因此提前停止。

## 8. 裁定与结论边界

本实验只能建立 seed 17、30B、有效 microbatch Switch LB 下的五臂排序。
covariance 身份收益要求 HMT 优于对应随机臂；Relay 来源收益要求 Relay-HMT
优于 Local-HMT。缺臂、无法恢复、LB 回传失败或缺少配对终点评估均为
insufficient。

本实验不能建立 H/M/T 的普遍语义、跨 seed 普遍性、尺度迁移、专家专业化是
NLL 变化的唯一中介，也不能代表 global-batch LB、router z-loss 或动态 bias。

## 9. 执行合同

资源固定为 ACP、workspace `share-space`、AEC2
`computing-cluster-5090-01g`、单个 `n12lp.nn.i10a.8` worker、8 个进程/GPU、
SPOT、normal priority。全部工程门通过后直接提交五个 full，不再次等待审批；
监控到 optimizer 稳定前进并形成一段完整 telemetry。原始日志、checkpoint 和
cache 留在 worker，Research_System 只收 Protocol、smoke verdict、job ledger
和后续策展证据。

## 10. 确认记录

- 2026-08-09：用户删除了旧的无效 checkpoint，并批准五臂、单 seed、30B、
  可微 LB 的 step-0 重训。
- 2026-08-09：用户将保存点固定为 2B、5B、10B、25B、30B，要求可续训，
  并明确选择单节点 8×5090。
- 跨模块一致性审计：实现前通过。

## 11. 追加式修订记录

### E05-AM01——增加 20B 恢复与评估检查点

- 修订时间：`2026-08-10T12:28:02Z`。
- 修订前：在 step `2544`、`6358`、`12716`、`31790`、`38147` 保存完整
  checkpoint 并评估，对应约 2B、5B、10B、25B、30B tokens。
- 修订后：新增 step `25432`（`20,000,538,624` tokens），保留全部原注册点，
  包括 step `31790` 的 25B；完整计划为
  `2544,6358,12716,25432,31790,38147`。
- 原因：五个首次恢复作业在 10B 与 25B 之间没有完整 checkpoint；新增 20B
  可以限制后续 SPOT 中断造成的进度损失，并让 10B--25B 区间中部可独立评估。
- 修订前已见结果：注册的 10B 终点及其中期评估已经可见；五个替代作业还产生了
  一小段 10B 之后、尚未保存的续训前缀。该前缀不参与新里程碑的选择或科学比较。
- 受影响模块：仅 Block G（保存、评估与恢复计划）。研究问题、五臂、数据、
  初始化、目标函数、优化、训练终点、主指标与裁定规则均不改变。
- 审批：用户明确授权在技术可行时增加 20B、25B checkpoint 并重提；25B 已在
  原合同中，因此本次只新增 20B。
- 证据资格：共同的完整 10B checkpoint 继续有效；被替代恢复作业中未保存的
  10B 后前缀排除。新作业必须从 step `12716` 精确恢复；只有恢复恒等性、共同
  token hash、checkpoint 完整性和科学配置不变均通过后，其 20B、25B、30B
  checkpoint 才有资格进入证据链。
- 执行范围：批准建立只改变保存计划的不可变实现副本，停止被替代恢复作业，
  使用已经批准的单节点 8×5090 SPOT 配置重提相同五臂，并监控精确恢复。
