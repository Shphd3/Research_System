---
experiment_id: A15_06_E01_10b_online_spectral_routing
legacy_experiment_id: A15_00_E01_10b_five_arm_training
anchor_id: A15_06_online_spectral_routing_and_relay
status: approved_for_implementation_smoke_and_full
approved_by: user
approval_date: 2026-08-03
resource_profile: 5090-8-spot
primary_metric: 10B-token终点配对held-out NLL
---

# Protocol：A15_06_E01 五臂在线频谱 Router 10B训练

## 0. Approval Snapshot

本实验已批准实现、smoke和十个full任务。唯一目的，是裁定动态
Relay-HMT在10B终点是否具有超出去均值、本层动态频带和同维随机Relay的
价值。主指标是固定未见文档上的next-token NLL，单位nat/token，越低越好。

只有seed 17和29中的Relay-HMT都以文档配对区间优于Centered-Full、
Local-HMT和Relay-Random，并且收益不能由负载或额外计算解释，才支持
Relay-HMT。缺少这一排序则不支持；终点或工程证据无效则insufficient。

批准范围：完成合同、实现、单元测试、单卡与8卡smoke，随后直接提交十个
10B任务；监控到真实训练步和至少一次动态刷新闭环后结束本轮对话，不等待
10B终态。不修改graph、root sync，不commit/push。

## 1. 术语解释

| 术语 | 人话含义 | 计算对象 | 作用 | 不能证明 |
| --- | --- | --- | --- | --- |
| running center | Gate看到的表征减去可部署均值 | 旧runner的分布式EMA均值 | 分离去均值效应 | 语义价值 |
| H/M/T | 背景方差由高到低的64/256/448维 | 嵌套\(P_{64}\)和\(P_{320}\) | 频谱处理 | 语义层级 |
| Relay | 后层Gate读取同token的第一层输出 | 无参数RMS归一化block-1 residual | 统一来源效应 | 浅层表征静态不变 |
| route flip | 刷新前后换专家的token比例 | 固定guard token上的top-1 | 连续性 | 质量收益 |
| margin | 第一名与第二名专家分数差 | 旧Gate logits | 定义高置信 | 专家正确性 |
| 终点NLL | 模型对未见正确token的平均意外程度 | 10B逐文档负对数概率 | 主裁定 | 机制 |

## 2. Anchor Alignment

主Anchor：[A15_06](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_06_online_spectral_routing_and_relay/15_06_online_spectral_routing_and_relay_anchor_cn.md)。本实验唯一减少的不确定性是：动态covariance身份，而非去均值或任意平滑瓶颈，是否改善10B终点。

## 3. 假设与竞争解释

- H1：动态Local-HMT优于Centered-Full。
- H2：Relay-HMT优于Local-HMT。
- H3（决定性）：Relay-HMT优于Relay-Random。
- H4：EMA、嵌套Grassmann和回溯使高置信刷新flip不超过1%。
- 最强rival：收益来自任意稳定旁路、去均值、负载或额外计算。

## 4. 模型、数据与公共设置

模型固定为四层H768、8个稀疏专家加1个共享专家、top-1、专家宽1536。
seq=1024，global batch=768，每步786,432 tokens；BF16、ZeRO-1、AdamW，
betas=(0.9,0.95)，weight decay=0.01，LR=\(10^{-4}\)，warmup=636，保留
100B-token余弦horizon。每个job在step12,716停止，即10,000,269,312 tokens。
所有arm的\(\lambda_{LB}=0.01\)。复用实现不做有限容量截断：每个top-1
分配都实际执行，因此capacity drop结构性为0，并在每个里程碑作为守卫记录，
而不是把它当成会随arm变化的结果。

训练、验证、statistics和guard四者严格隔离。statistics至少65,536 tokens，
guard至少16,384 tokens；文本、token id、顺序和SHA-256在full前冻结。

## 5. 五个Arm

| Arm | 第1层 | 第2/3/4层Gate |
| --- | --- | --- |
| Vanilla-Full | 完整、不去均值 | 完整本层、不去均值 |
| Centered-Full | 去running mean后的完整输入 | 去running mean后的完整本层输入 |
| Local-HMT | Centered-Full | 本层动态H/M/T |
| Relay-HMT | Centered-Full | 第一层动态H/M/T；W2/W3/W4独立 |
| Relay-Random | Centered-Full | 第一层同维随机64/256/448嵌套子空间 |

第一层始终可训练，Relay梯度可以回传；固定的是来源层身份。专家始终收到完整
本层expert input，只有Gate视图变化。逻辑上唯一的第一层running mean在三个
后层Gate中物理复制，但每步检查数值和更新次数严格相等；任一分歧均为工程失败。

## 6. 配对、种子与保存点

seed固定17和29。每个seed生成唯一step-0模型和优化器状态，五臂参数必须
bitwise一致；数据顺序、逐步token hash、dropout/RNG、优化器、LR、LB、
不截断容量和评估顺序配对。

里程碑及实际step：0、64(50.33M)、127(99.88M)、318(250.09M)、
636(500.17M)、1272(1.00034B)、2543(1.99990B)、5086(3.99979B)、
7629(5.99969B)、10173(8.00037B)、12716(10.00027B)。

## 7. 主指标

\[
\Delta_{A-B}^{(s)}=L_A^{(s)}(10B)-L_B^{(s)}(10B).
\]

负值表示A更好。每个seed在相同1,024篇验证文档上做2,000次配对bootstrap；
两seed等权平均只作摘要。AUC只描述轨迹，不作主判据。

核心比较依次为Centered−Vanilla、Local−Centered、Relay−Local、
Relay−Centered、Relay−Random。

## 8. 动态统计与刷新

step0令\(\bar\Sigma_0=\widehat\Sigma_0\)。之后\(\rho=0.1\)。刷新步固定为
0、128、…、1152、1280，之后每512步直到10B。每次使用同一statistics语料，
eval模式重放并在返回训练前恢复RNG，不对covariance、eigh、Grassmann和guard
求梯度。

## 9. 嵌套Grassmann与随机对照

状态是\((U_{64},U_{320})\)嵌套flag。先Procrustes对齐并更新320维空间，再在
候选320维内部更新64维空间；M和T分别由\(P_{320}-P_{64}\)与\(I-P_{320}\)得到。
候选\(\gamma=1,1/2,\ldots,1/128,0\)从大到小回溯。

由于Gate是线性的，部署时使用\(W_\ell P_B\)作为有效的\(8\times768\)权重，
而不是给每个token显式计算\(P_Bx\)；二者的logit和对\(W\)的梯度严格等价，并有
单元测试守卫，因此不会把大维投影乘法放到每个token路径上。

Local每个source层独立选\(\gamma_\ell\)；Relay对唯一第一层来源选一个\(\gamma\)，
必须同时通过第2/3/4层guard。Relay-Random在每个seed初始化并持久化固定Haar
矩阵\(R_s\)，每次用\(U^*_kR_s\)产生目标嵌套子空间，再走完全相同tracker。

## 10. Continuity Guard

每层旧margin前25%的guard token定义为高置信集合。候选必须同时满足：

- 高置信route flip \(\le0.01\)；
- 最大专家份额变化\(\le0.01\)；
- \(R_{cont}\le0.01\)，其中

\[
R_{cont}=\mathbb E_{x\in\mathcal H}
\frac{\|C_E(z_{cand}-z_{old})\|_2^2}{m_{old}^2+10^{-6}}.
\]

低置信flip只记录。所有非零候选失败则\(\gamma=0\)，保留旧投影。gamma经常为0、
flip偏高、负载集中或NLL较差均为科学结果，不自动停止。

## 11. Checkpoint、TensorBoard与里程碑证据

每个checkpoint必须完整保存模型、优化器、scheduler、RNG、sampler cursor、
running means、covariance EMA、目标/部署嵌套基底、Haar frame、刷新计数、
gamma/guard状态和milestone完成状态。

每个里程碑写入逐文档NLL、route/load/capacity、projector/gamma/flip/margin、
Relay梯度，并执行forced-expert regret、专家梯度冲突和输出冗余评估，评估耗时
与纯训练耗时分开。TensorBoard实时镜像loss、LR、tokens、负载、路由、投影、
continuity、刷新接受率、吞吐和评估状态。任意里程碑可独立聚合并生成六张图。

## 12. 工程守卫与Smoke

必须通过：step-0五臂参数一致；逐步数据hash配对；forward/backward；projection
正交、嵌套、完备和重构；八rank状态一致；fresh→resume参数/logit/top-1/NLL与
动态buffer恢复；统计数据隔离；TensorBoard/JSONL/checkpoint可重建。

NaN/Inf、OOM/通信、数据漂移、checkpoint损坏、rank分歧、投影重构失败或产物
不可恢复时才停止工程修复。不得改变五臂、阈值、数据、seed、LR或主指标。

## 13. 裁定与边界

全部十个工程有效任务直接训练到10B，不设早期性能门。Relay-HMT的支持条件见
第0节；否则不支持。关键终点缺失或配对/恢复/投影/数据隔离失败则insufficient。

本实验不能声称H/M/T具有普遍语义、适用于所有规模、直接导致组合计算，或任何
NLL收益必然来自专家专业化。

## 14. 执行合同与图

单节点8×5090 SPOT：workspace `share-space`，AEC2
`computing-cluster-5090-01g`，spec `n12lp.nn.i10a.8`，worker nodes=1，
quota=spot，8个进程。十个正式job使用批准名称。

必须生成：五臂NLL轨迹、10B配对差、负载/熵/capacity、gamma/flip/margin/
Grassmann、Relay-HMT与Random的NLL/FLOP和wall-clock、Relay梯度与专家机制图。
每图先写plot contract并实际视觉审核。

2026-08-03最终修订：第一层不冻结；高置信continuity阈值固定0.01；嵌套联合
更新；10B使用100B余弦horizon；完整milestone与实时TensorBoard为硬合同。
