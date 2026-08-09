---
experiment_id: A15_06_E02_local_random_identity_control
legacy_experiment_id: A15_00_E02_local_random_identity_control
anchor_id: A15_06_01_local_random_identity_control
status: approved_for_implementation_smoke_and_full
approved_by: user
approval_date: 2026-08-04
resource_profile: 5090-8-spot
primary_metric: 10B终点Local-HMT减Local-Random-Matched配对NLL
---

# Protocol：A15_06_E02 本层随机频带身份对照

## 0. 审批摘要

用户已批准直接完成合同、实现、smoke、两个 full 任务、终态监控和比较。本实验
只回答：Local-HMT 的弱信号来自 covariance 排名身份，还是任意平滑动态本层
子空间也能复现。只新增 seed 17、29 的 Local-Random-Matched；既有
Local-HMT 与 Centered-Full 作为不可改动的配对对照。

主指标是每个 seed 的 10B 终点逐文档 NLL 差：Local-HMT 减新随机对照，负值
表示 HMT 更好。只有两个 seed 的 95% 配对区间都低于零，且追踪可比性通过，才
支持 covariance 身份。随机对照匹配/更好、任一 seed 区间跨零则不支持；配对、
运动等距、追踪、恢复或终点证据无效则 insufficient。

## 1. 对照的物理含义

Local-HMT 的第2/3/4层分别读取本层 covariance 的 64维 head、256维 middle、
448维 tail。新随机对照对每个 seed、每层固定一个 768维 Haar 正交矩阵 $O$，
把当前嵌套基底变为

$$
(U_{64},U_{320})\longmapsto(OU_{64},OU_{320}).
$$

这是左侧环境旋转，严格保持子空间维度、嵌套关系和相邻刷新间的 principal
angles；它删除 covariance 排名身份，却不引入旧 Relay-Random 的全谱 tail
旋转。随后使用完全相同的 EMA、Grassmann 候选和 continuity guard。

## 2. 固定内容

- 四层、H768、8个稀疏专家加1个共享专家、top-1、专家宽1536；
- 专家始终接收完整本层状态，只有 Gate 视图变化；
- DCLM 数据、tokenizer、同 seed 数据顺序和 step-0 公共参数；
- seq 1024、global batch 768、BF16、ZeRO-1、AdamW、LR $10^{-4}$、
  warmup 636、weight decay 0.01、100B cosine horizon、$\lambda_{LB}=0.01$；
- statistics/guard/1,024验证文档及其 hash；
- 每个新任务 step 12,716 停止，即 10,000,269,312 tokens；
- 里程碑 0、50M、100M、250M、500M、1B、2B、4B、6B、8B、10B。

## 3. 主比较

$$
\Delta_s=L_{Local\text{-}HMT,s}(10B)-L_{Local\text{-}Random,s}(10B).
$$

每个 seed 对相同 1,024 篇文档做 2,000 次配对 bootstrap。两 seed 分别裁定，
等权平均只作摘要。次级比较是新随机对照减 Centered-Full，用来判断一般动态
低维约束是否本身有益。

## 4. 追踪可比性

每次刷新记录真实 HMT 目标运动与旋转目标运动的 principal-angle 误差，必须
$\le10^{-6}$ radians。U64/U320 的部署—目标 overlap 中位数不得比既有
Local-HMT 低超过0.02，gamma=0 比例不得高超过0.10。若 HMT 的 NLL 更好但
上述任一条件失败，只能判 insufficient，不能归因于 covariance 身份。

## 5. 工程与执行

必须通过：正交/嵌套/完备、旋转运动等距、step-0 参数一致、逐步 token hash、
8卡 fresh→resume、动态 buffer 恢复、TensorBoard、JSONL、checkpoint 和逐文档
评估闭环。任务使用单节点 `5090-8-spot`：workspace `share-space`，AEC2
`computing-cluster-5090-01g`，spec `n12lp.nn.i10a.8`，quota `spot`。

任务名：

- `osrt-10b-local-random-matched-s17`
- `osrt-10b-local-random-matched-s29`

NaN、数据漂移、恢复损坏或投影失效才允许工程修复；NLL 差、负载变化、flip、
gamma=0 均为科学结果，不得提前停止或后验改阈值。

## 6. 结论边界

本实验只能裁定注册四层 DCLM、两个 seed、10B 设置中的 covariance 身份效应；
不能证明 H/M/T 具有普遍语义、适用于更大模型，或 NLL 变化唯一来自专家分工。
