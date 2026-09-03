---
experiment_id: A16_01_E01_30b_incremental_information_lb_routing
anchor_id: 16_01_incremental_information_lb_routing
status: approved_for_implementation_smoke_and_full
approved_by: user
approval_date: 2026-08-10
design_frozen_at: 2026-08-10
resource_profile: 5090-8-spot
primary_metric: paired_document_30b_endpoint_nll_contrast
---

# Protocol：A16_01_E01 可微 LB 下的层增量信息 Router 30B 训练

## 0. 审批摘要

**目的：**检验实际同层 attention 可见增量上的显式低秩路径，能否在真正可微的负载均衡（LB）下改善 30B 语言建模；独立认证方向是否比同秩随机路径更有价值。

**主 Anchor：**[A16_01 层增量信息路由](/Projects/from-attention-to-search/main/problem_anchors/16_load_control_gradient_interference/16_01_incremental_information_lb_routing/16_01_incremental_information_lb_routing_anchor_cn.md)。

**四个条件：**Native-LB、Trainable-Innovation-LB、Certified-Innovation-LB、Haar-Innovation-LB；seed 17/29，共八个 full job。全部从 step 0 启动。Certified/Haar 在 2B/5B/10B 首个两 seed 共同通过 E1+E2 的里程碑前保持与 Native 完全一致的休眠行为。

**唯一主指标：**30B 总 token 终点的文档配对 held-out next-token NLL，单位 nat/token，越低越好。工程比较为 Trainable−Native；科学身份比较为 Certified−Haar，并要求 Certified−Native 同方向。

**裁定：**Pass 要求两个 seed 各自的点估计都为负，文档配对 95% 区间上界也低于零；完整有效数据不满足为 Fail。身份、LB 梯度、恢复、数据、准入或终点评估守卫失败为 Insufficient。若到 10B 无共同 E1+E2 证书，Certified/Haar 保持休眠到 30B，科学结论为 `INSUFFICIENT_NO_CERTIFICATE`。

**批准范围：**正式 Protocol、实现、单元测试、单卡 smoke、四臂 8×5090 smoke、提交八个 full job、里程碑准入与按合同激活均已批准；不授权 Git、graph、sync 或发布。

**不能声称：**不能证明普遍语义层级、尺度迁移、工程投影具有语义身份、LB 是收益原因，或专家专业化是唯一中介。

## 1. 术语解释

- **旧状态** $n_\ell^{old}$：本层 attention 输出加入前的归一化 token 状态。
- **新状态** $n_\ell^{new}$：attention 后实际给当前 MoE Router 的归一化状态。
- **可见增量** $u_\ell=n_\ell^{new}-n_\ell^{old}$：本层写入在 Router 位置造成的变化，不等于新增 Shannon 信息。
- **增量分支：**保留 native full-state Gate，同时从 $u_\ell$ 产生加性低秩 Router logits。
- **认证方向：**不查看终点 NLL，由 E1 条件可读性与 E2 专家效用共同准入的冻结方向。
- **Haar 方向：**层集合、秩、尺度、参数、启动状态和训练时长都与 Certified 匹配的固定随机正交 frame。
- **可微 LB：**soft probability 路径确实对 Gate 产生非零梯度的 Switch 辅助损失；只有标量日志不算。
- **30B 终点：**累计 30,000,021,504 token（step 38,147），不是增量分支激活后再训练 30B。

## 2. Anchor 对齐

本实验不改变 A16_01 的问题、公式或边界。它属于有准入保护的**方法构造比较**。A15 保留语义方向证书所有权；A16_01 只负责在真正可微 LB 下评价长期训练。最强竞争解释是额外低秩容量、正则化、延迟激活或负载变化，而非认证方向身份。

## 3. 待检验假设

1. **工程效用：**两个 seed 中 Trainable-Innovation-LB 的 30B NLL 都低于 Native-LB。
2. **科学方向身份：**若存在共同证书，两个 seed 中 Certified-Innovation-LB 都低于 Haar-Innovation-LB 与 Native-LB。

两者分别给 typed verdict；工程成功不能挽救科学比较缺失或失败。

## 4. 竞争解释

| 竞争解释 | 对照或守卫 |
| --- | --- |
| 额外参数或普通低秩正则 | Certified 对参数匹配 Haar；Trainable 对 Native 明报参数/FLOPs |
| 启动点或训练时长不同 | Certified/Haar 从 step 0 休眠，激活前验证与 Native 身份一致，并一起到 30B |
| LB 只有日志、没有优化作用 | activation checkpointing 下 LB-only backward 与 LM+LB 影子更新 |
| Native 已经利用全部增量 | Trainable 对 Native |
| 语义可读但不预测专家 | E2 选专家遗憾门 |
| NLL 变化只由硬负载变化造成 | 配对负载/capacity 过程量；只解释、不替换终点 NLL |

## 5. 数据构造与来源

### 5.1 语言模型数据与终点评价

- 训练：`/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10`。
- sequence length 1,024，global batch 768，每 optimizer step 786,432 token。
- 终点评价固定为已验证 runner 的 1,024-document artifact：`/data/250010109/MoE_Router/experiments/20260802_a15_01_04_progressive_band_source_2b_5090/artifacts/eval_tokens.pt` 及 `eval_tokens.json`。
- Preflight 冻结训练 bin、tokenizer、评价 tensor 与 manifest 的 SHA-256；全部 arm 使用相同文档顺序。终点评价文档不得拟合方向、读出器、阈值或 checkpoint。

### 5.2 E1 表示数据

使用 SHA-256 为 `ce91dbbd3c5071e17beeccf0d86a280dc8a3e48e0fdbf2178868da45eea18af4` 的 1,920 条英文 conditional-fine taxonomy bank：八个 parent，每个八个 child，每个 child 各 10 条 TRAIN、10 条 DEVELOPMENT、10 条 CONFIRMATION 表达。TRAIN 构造 $\mu,S,P$；DEVELOPMENT 检查跨表达稳定；选择冻结后才打开 CONFIRMATION。该数据绝不进入 LM 优化。

### 5.3 E2 专家效用数据

Smoke 前冻结一份与训练 shard 和 LM 终点评价文档 hash 不相交的 DCLM 功能 bank，按完整文档拆成 FIT、DEVELOPMENT、CONFIRMATION。FIT 训练冻结的小 Router readout，DEVELOPMENT 只选停止点，CONFIRMATION 只计算一次 expert-choice regret。反事实专家损失和 E1 标签都不得更新 30B 模型。

冻结后的 bank 含 384 篇相互独立的 256-token DCLM 文档，FIT、DEVELOPMENT、CONFIRMATION 各 128 篇。token tensor 的 SHA-256 为 `827129cdf5b1d44af06a034b607e40c98d5353ac8e5276b994b906c917479fd5`，manifest 的 SHA-256 为 `0a8a00d2370735821bb553fcc5f27a8c7c0006a749e4d5b4628c8df2ee6f0192`。manifest 记录每篇文档的源行号、文档哈希、确定性切片和 token 哈希，并验证与 1,024 篇终点评价文档的文档哈希交集为零。

## 6. 学习任务与允许监督

full 训练任务只有 next-token prediction。线上 Router 只读取当前层此刻可用张量并输出八个 expert logits。Trainable 从 LM+LB 梯度端到端学习 rank-56 因子，不接触语义或专家效用标签。Certified/Haar 只读取当前样本的冻结投影；配对双差分不在线出现。E1 标签只学/审计 $P$，E2 反事实损失只审计功能，二者都不得更新 backbone、experts、native Gate 或 30B 目标。

## 7. 模型、架构与冻结变体

四臂共享四层 Qwen 风格 MoE：hidden 768，6 个 query head、3 个 key/value head、head dimension 128，每层 8 个稀疏专家加 1 个 shared expert，专家 intermediate 1,536，top-1。Native 构造必须复现 251,199,232 个可训练参数、每 token 152,108,800 个活跃参数和 24,576 个 native Router 参数。

$$
n_\ell^{old}=N_\ell(h_\ell),\quad
n_\ell^{new}=N_\ell(h_\ell+a_\ell),\quad
u_\ell=n_\ell^{new}-n_\ell^{old}.
$$

1. **Native：**$g=Wn^{new}$。
2. **Trainable：**$g=Wn^{new}+BA^\top\operatorname{RMS}(u)$；$A\in\mathbb R^{768\times56}$ 可训练，$B\in\mathbb R^{8\times56}$ 零初始化；四层共增加 173,824 个参数。
3. **Certified：**在两 seed 共同通过的层集合 $\mathcal L^*$，$g=Wn^{new}+CP^\top S^{-1}(u-\mu)$；$P,\mu,S$ 冻结，$C$ 零初始化；其他层保持 Native。
4. **Haar：**除 $P$ 换成固定同秩 Haar 外与 Certified 完全相同。

E1 与训练固定 rank 56。Certified/Haar 在 $t^*$ 前分支严格乘零；$\mathcal L^*$ 是在 $t^*$ 时两个 seed 的 E1+E2 通过层交集，终点结果不能选层。专家始终接收完整本层表示。

## 8. 训练目标与优化

$$
L_{LB,\ell}=8\sum_{e=1}^8\left(\frac1T\sum_xp_{\ell,e}(x)\right)f_{\ell,e},
\qquad
L=L_{LM}+0.01\sum_{\ell=1}^4L_{LB,\ell}.
$$

$p$ 是完整 softmax 概率，$f$ 是 stop-gradient hard top-1 token 比例。activation checkpointing 下必须保留修复后的辅助张量 autograd 路径。优化固定 BF16、AdamW、LR $10^{-4}$、betas $(0.9,0.95)$、weight decay 0.01、warm-up 636 steps、100B-token scheduler horizon、ZeRO-1 和 activation checkpointing。新分支零输出，新参数 AdamW moment 为零；禁止性能早停或按结果选 checkpoint。

## 9. 条件、种子与保存点

seed 固定 17/29。同一 seed 四臂共享公共模型/专家初始化、数据顺序和适用的 RNG 流；arm-specific 初始化不得消耗公共模型 RNG。

| Arm | 启动 | 终点 | 任务数 |
| --- | --- | --- | ---: |
| Native | step 0 | 30B | 2 |
| Trainable | step 0，零输出分支 | 30B | 2 |
| Certified | step 0，休眠至 $t^*$ | 30B | 2 |
| Haar | step 0，休眠至 $t^*$ | 30B | 2 |

完整保存与独立评价点为 2B（step 2,544）、5B（6,358）、10B（12,716）、20B（25,432）、25B（31,790）、30B（38,147）。Certified/Haar 保存全部里程碑与激活 receipt，并可在准入点等待冻结 gate receipt；不得用部分结果或终点结果激活。SPOT 只从完整注册 checkpoint 恢复。

## 10. 主指标与冻结分析

对每个终点评价文档 $j$ 计算 mean next-token NLL。每个 seed 内：

$$
\Delta_{s,j}(A-B)=NLL_{s,j}^{A}-NLL_{s,j}^{B}.
$$

文档等权平均；按完整文档配对重采样 2,000 次，给 two-sided 95% 区间。不得删除离群文档、token、层或 seed；缺失/非有限文档使该终点 insufficient，直到确定性重建。

- **Engineering Pass：**两个 seed 的 $\Delta(Trainable-Native)$ 均值和 95% 上界都小于零。
- **Scientific Pass：**存在合格 $t^*$，且两个 seed 的 $\Delta(Certified-Haar)$ 与 $\Delta(Certified-Native)$ 均值和 95% 上界都小于零。
- 完整有效数据未通过为 Fail；硬守卫失败为 Insufficient；10B 无 $t^*$ 为 `INSUFFICIENT_NO_CERTIFICATE`。

两 seed 等权均值、NLL AUC 和 late slope 只作描述。只有相关 30B per-document 数组完整后才解封主分析。

## 11. 次级指标与守卫

逐里程碑、逐层记录：LM NLL、LB 标量与系数、LB-only/native/innovation Gate 梯度范数、最忙专家占比、路由熵、capacity drop、分支/native logit RMS 比、logit 余弦、相对 Native 的 route divergence、专家遗憾、吞吐、理论 FLOPs、wall clock 与 TensorBoard。

硬守卫：

1. 每层 $n^{new}=n^{old}+u$ 通过 BF16/FP32 replay 容差。
2. 零输出分支在启动时复现 Native logits、top-1、LM loss 与 LB loss。
3. LB-only backward 对每层 native Gate 产生有限非零梯度；第一步到 innovation head，head 非零后的第二步到 Trainable $A$ 与增量上游。
4. Certified $P$ 冻结、Haar 正交；二者层集合、秩、参数量和在线 FLOPs 相同。
5. 模型、optimizer、scheduler、RNG、数据游标、分支状态和 token hash 按注册精度恢复一致。

次级指标只能解释，不能反转主裁定。

## 12. Known-good / Known-bad / Known-confusing

- Known-good：在 $u$ 中注入 rank-56 且预测构造专家效用的信号，E1/E2 应恢复；head 非零前不能改变 logits。
- Known-bad：$u=0$、完全相同配对、父类内标签置乱与 LB 系数 0 不得产生证书或 LB-only Gate 梯度。
- Known-confusing：Trainable 改善但 Certified 不改善，只支持工程容量；Certified/Haar 都优于 Native，只支持普通稳定旁路，不支持方向身份。

## 13. 科学阶段合同

| 阶段 | 目标与操作 | 必须产物 / 交接 |
| --- | --- | --- |
| P0 preflight | 固定模型、数据、评价、TAX、hash、30B 计划、8×5090 和空间 | 签名 manifest；失败阻止 smoke |
| P1 单测/单卡 | 合成+真实 microbatch 检查重构、no-op、LB backward、两步分支梯度 | typed smoke JSON；全部守卫通过 |
| P2 8卡 smoke | 四臂接口；Certified/Haar 仅用 synthetic frame 验证实现；保存恢复、token hash、TensorBoard | 分布式 verdict；synthetic frame 不准入科学 full |
| P3 full 提交 | 四臂×seed 17/29 从 step 0 提交；Certified/Haar 休眠 | 八个 job receipt 与里程碑 checkpoint |
| P4 准入 | 2B 运行 E1→E2，失败则 5B，再失败则 10B | $t^*$ 与逐 seed/layer gate receipt，或 `NO_CERTIFICATE_BY_10B` |
| P5 激活 | P4 通过才向已运行休眠任务加载 Certified/Haar frame；否则持续休眠 | 激活身份 receipt 或 dormant-to-30B receipt |
| P6 终点评价 | 同一文档评价全部合格 30B arm，配对 bootstrap | per-document 数组、对比表、typed verdict |

负载集中、早期 NLL 差、分支 logits 小或性能差不能停止数值有效 full。NaN/Inf、OOM、通信失败、checkpoint 损坏、hash 分叉、LB 回传失效、frame 破坏或终点不可恢复会停止并记录 Insufficient。

## 14. 算法、产物与 provenance

实现从已验证可微 LB runner 复制到新的不可变 worker surface；Research_System 不接收原始日志、checkpoint、activation cache。原始产物根为 `/data/250010109/MoE_Router/outputs/a16_incremental_information_lb_routing/`。

必须保存 source/config/data manifest、单测/smoke verdict、step-0 与激活身份 receipt、job ledger、TensorBoard、里程碑指标、完整 checkpoint、E1/E2 ledger、逐文档 NLL、bootstrap、参数/FLOP 表和失败 receipt。证据审计后才在本目录写 summary/detailed 与策展图表。

任务名：`a16-inc-native-s17/s29`、`a16-inc-trainable-s17/s29`、`a16-inc-certified-s17/s29`、`a16-inc-haar-s17/s29`。资源固定 ACP、`share-space`、`computing-cluster-5090-01g`、`n12lp.nn.i10a.8`、八进程、SPOT、normal priority。

## 15. Success / Failure / Insufficient

输出 `engineering_utility`、`certified_direction_identity` 和 execution-validity 三个 typed verdict。只有第 10 节决定科学结论；平滑 loss 或成功 job receipt 不是 Pass。E1 语义证书不等于 E2 功能准入；没有证书必须保留为 Insufficient，不得换成任意方向。

## 16. 不能声称什么

不能声称 conditional-fine 方向普遍存在、每层都创造新信息、工程投影有语义身份、两 seed 足以外推尺度、LB 普遍有益或有害，也不能把终点 NLL 变化唯一归因于专家专业化。

## 17. 确认、冻结与修订记录

| Block | 状态 | 确认依据 |
| --- | --- | --- |
| A 问题与边界 | CONFIRMED | 用户批准两种实现、配对 LB、30B 比较 |
| B 数据 | CONFIRMED | 复用验证 DCLM/eval；语义与效用 bank 隔离 |
| C 任务监督 | CONFIRMED | 在线仅 LM+LB；E1/E2 不进入 LM 训练 |
| D 架构 | CONFIRMED | native residual + Trainable/Certified/Haar |
| E 目标优化 | CONFIRMED | microbatch Switch LB=0.01 与既有 30B 配置 |
| F 比较证据 | CONFIRMED | 四臂、两 seed、终点配对 NLL、准入 typed rule |
| G 执行复现 | CONFIRMED | 实现、smoke、八个 8×5090 full 与注册激活均获批 |

跨块一致性：`PASS`。首次实现 smoke 时冻结科学正文和决策配置。执行后任何实质变化只能以 append-only amendment 记录 before/after、原因、已见数据、受影响 arm、用户批准和证据资格；Protocol 只追加执行 receipt/结果链接，结果与解释写入 `summary.md`、`detailed.md`。

### 修订 A16_01_E01-AMEND-20260810-01：确定性证书协调

- **时间：**2026-08-10T18:28:17Z。
- **修订前：**第 7、9、13 节已经冻结“两 seed 共同通过 E1+E2 后，Certified/Haar 配对激活”，但没有完整规定证书生产者/消费者顺序、等待语义和消费证书时的状态身份检查。
- **修订后：**seed 17 与 seed 29 的 Native 任务各自独立生成候选通过层，只有两个 Native 候选都通过的层才进入共同证书层集合。Certified 与 Haar 是相互独立的惰性消费者，各自接收本 arm 的证书 artifact。任何消费者激活前，其规范模型状态摘要（参数、持久 buffer 与注册 step）必须与同 seed Native 完全一致。`wait_seconds=0` 表示无限等待；任何有限超时都必须抛出异常并停止对应消费者，且绝不能把该里程碑标成“已检查”。生产 E1 的 rank 固定为 56。full 提交顺序固定为 Native 17/29、Trainable 17/29、Certified 17/29、Haar 17/29。
- **原因：**消除证书到达竞态，避免迟到 artifact 或等待超时被静默误判成“无证书”，同时保持已经注册的两 seed 共同门和配对激活身份。
- **已见数据状态：**当时只有实现测试与 smoke receipt；尚未观察 full 里程碑、准入、终点 NLL 或任何科学结果。
- **影响范围：**执行块 G 与 P3--P5；只影响 Native、Certified、Haar 的协调。四个科学条件、E1/E2 阈值、rank、训练目标、主指标和裁定规则均不改变。
- **批准：**用户在 2026-08-10 的实现与提交请求中批准该执行修订。
- **证据资格影响：**新增摘要、等待与顺序守卫通过时不改变资格；摘要不一致或有限超时异常会使相应激活路径判为 Insufficient，不能改记为 `NO_CERTIFICATE_BY_10B`。

### 修订 A16_01_E01-AMEND-20260810-02：与设备精度无关的投影校验

- **时间：**2026-08-10T19:02:00Z。
- **修订前：**rank-56 投影的正交性与 Gram 守卫直接在当前 CUDA float32 张量上计算；RTX 5090 的 TF32 矩阵乘法可能使合法 QR 基底看起来超过未改变的 $10^{-5}$ 容差。
- **修订后：**安装投影前，先对 detached CPU float64 副本进行确定性校验。注册的 $10^{-5}$ 容差、rank 56、模型实际使用的投影数值和全部科学条件均不改变。安装、证书激活、smoke 与恢复路径共用同一校验器；真正不正交的基底仍会被拒绝。
- **原因：**第一次分布式 smoke 将合法 QR 基底测得约 $7\times10^{-5}$ 的 GPU Gram 误差，而相同存储基底在 CPU float64 下约为 $1.4\times10^{-6}$；这是设备精度造成的假拒绝，不是科学失败。
- **已见数据状态：**问题只出现在 P2 smoke 作业 `om-jmdqeig5`；当时没有 full 作业、里程碑、证书裁定、终点 NLL 或科学比较。
- **影响范围：**仅影响执行块 G 与 P1--P2 的数值校验。训练数据、初始化、模型方程、LB 目标、rank、优化器、保存计划、准入阈值、终点指标和裁定规则均不改变。
- **批准：**包含在用户明确要求修复实现、完成 smoke，并在确认正确后提交全部 full 作业的授权中。
- **证据资格影响：**修正版不可变 worker 通过校验器和坏基底回归测试后，full 作业资格不受影响。修复前失败的 smoke 作为工程 provenance 保留，不构成科学证据。

### 修订 A16_01_E01-AMEND-20260811-03：标量持久状态的规范哈希恢复

- **时间：**2026-08-11T03:42:00Z。
- **修订前：**证书协调器使用 `tensor.view(torch.uint8)` 读取规范模型状态的原始字节；当 2B 里程碑首次哈希零维 `int32` 持久 buffer `active_rank` 时，PyTorch 拒绝将零维整型直接重解释为字节，Native、Certified 与 Haar 六条轨迹在完整 `checkpoint-2544` 保存后停止。Trainable 不调用该证书协调路径并继续运行。
- **修订后：**在不改变张量名称、dtype、shape、注册 step 或字节内容的前提下，先用 `reshape(-1)` 将任意标量或高维连续张量展平，再以 `uint8` 读取相同底层字节。新增两个回归测试，分别验证零维持久 buffer 可被哈希，以及注册 step 仍改变摘要。恢复只从原作业已经完整注册的 `checkpoint-2544` 开始，目标仍为 step 38,147。
- **原因：**修复证书状态序列化的形状兼容性缺陷；该错误发生在里程碑证书编排阶段，不在 Router forward、LB backward、优化器更新或 checkpoint 写入路径。
- **已见数据状态：**六条受影响轨迹只有 2B checkpoint 与里程碑工程异常，尚无证书裁定、30B 终点 NLL 或主比较。两条 Trainable 轨迹未中断。不得使用已见 2B loss 调整模型、数据、阈值或恢复点。
- **影响范围：**仅影响 P4--P5 的规范状态摘要与六条 Native/Certified/Haar 轨迹的工程恢复。四个 arm、两个 seed、step-0 状态、训练 token、LB 系数、rank、优化器、scheduler、保存点、E1/E2 门、主指标与裁定规则均不改变。
- **批准：**用户在 2026-08-11 明确要求检查任务、修正新实现并直接提交 30B 恢复训练。
- **验证与证据资格：**冻结 worker v8 的本地完整测试为 86/86；目标 8×5090 环境的标量哈希回归为 2/2；四臂分布式 smoke 作业 `om-lo6v9cvi` 为 `SUCCEEDED`，四臂均通过 LB 可微性、0/2/3 保存恢复、共同 step-0 与 token hash，Certified/Haar 各八个 rank 的激活证书恢复误差为零。六条旧失败作业不构成终点证据；由 v8 从完整 2B checkpoint 恢复的轨迹在全部恢复守卫通过后保持原科学资格。
