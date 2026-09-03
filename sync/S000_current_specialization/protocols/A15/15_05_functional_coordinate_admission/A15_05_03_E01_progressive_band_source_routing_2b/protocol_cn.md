---
experiment_id: A15_05_03_E01_progressive_band_source_routing_2b
anchor_id: 15_05_03_progressive_band_source_routing
status: approved_with_load_neutral_calibration_for_smoke_and_full
approved_by: user
approval_date: 2026-08-02
canonical_protocol: protocol.md
resource_profile: 5090-8-spot
---

# Protocol：逐层本地频带与第一层频带 Relay 的 2B 匹配训练

## 0. Approval And Decision

研究者已明确批准直接完成实现、smoke、每个模型两次训练、2B full、结果审计与 0803 Focus。任何会改变三臂、H→M→T 映射、公共分叉、2B 终点、负载规则或主判据的修改必须停下；工程修复可在不改变科学问题时 fail-closed 重跑。

## 1. Decision Question

从同一个 0.629B-token 四层 DCLM MoE 分叉后，第 2/3/4 层依次按 H/M/T 路由是否比 native 更好；频带来自各层本地 Router 输入，还是统一来自第一层 block 输出，哪一种形成更有功能差异的专家并改善 2B held-out NLL？

## 2. Hypotheses And Rivals

- **H1 local-HMT：**逐层本地频带与深度计算匹配，改善 NLL 和专家功能。
- **H2 layer1-relay-HMT：**稳定浅层坐标减少跨层漂移，超过 local-HMT。
- **R0 distribution-only：**处理只换专家，不改善功能或 NLL。
- **R1 bottleneck：**丢失完整 Router 信息使两种处理都更差。
- **R2 load/compute：**差异由负载、容量、额外 source 路径或累计 FLOPs 解释。
- **R3 stale basis：**冻结投影不再对应训练后的频谱。

## 3. Model And Three Arms

共同模型：H768、4 Transformer blocks、8 sparse experts + 1 shared expert、top-1、expert width 1536、running-center linear Gate、$\lambda_{LB}=0.01$。专家始终接收本层完整 post-attention-normalized 表征。

| Arm | Block 1 | Block 2 Gate | Block 3 Gate | Block 4 Gate |
| --- | --- | --- | --- | --- |
| `native_full` | native full | native full | native full | native full |
| `local_hmt` | native full | 本层 H64 | 本层 M256 | 本层 T448 |
| `layer1_relay_hmt` | native full | 第一层输出 H64 | 第一层输出 M256 | 第一层输出 T448 |

第一层 source 定义为完整 block-1 residual output 经无参数 RMS normalization 后的同 token 向量。所有 arm 都计算该 source 与同形状投影路径；native/local 中未使用的结果只形成零值依赖，以匹配 kernel/FLOP。没有新增可训练参数。

## 4. Branch, Replicas, Data, And Training

- 公共 checkpoint：A15_05_05 的 step 800，模型、optimizer、scheduler、data cursor 与 running centers 完整恢复；629,145,600 nominal tokens。
- 两套后分叉 replicas：data/RNG seeds 17、29。每个 replica 内三 arm 完全配对；replica 之间只改变预注册的续训数据 permutation/RNG。
- 训练数据：DCLM `global-shard_01_of_10`；held-out：固定 1,024 个独立 DCLM 文档；WOS 仅作领域/主题路由描述。
- seq 1024；local batch 12/GPU；8 GPUs；gradient accumulation 8；global batch 768；每 optimizer step 786,432 nominal tokens。
- AdamW，LR $10^{-4}$，betas (0.9,0.95)，weight decay 0.01；warmup 636；100B-token cosine scheduler horizon；BF16、ZeRO-1。
- milestone steps：800、954、1272、1908、2544；终点 2,000,683,008 nominal tokens。处理实际作用 1,744 steps，即 1,371,537,408 nominal tokens。

## 5. Frozen Spectral Artifact

使用与训练/held-out 评估分离的固定 DCLM calibration tokens。分叉模型上同时捕获：各层实际 Gate-effective input，以及第一层完整 block output 的无参数 RMS-normalized source。每个 source 以独立均值中心化并按 covariance 特征值降序分解。

H64=ranks 1--64；M256=ranks 65--320；T448=ranks 321--768。投影只在分叉前离线构造一次。两个 calibration halves 的 projector overlap 必须超过 256 个同维 Haar random q95；投影对称、幂等、trace-rank 和能量重构必须通过。训练后重估相应 source 的当前 basis overlap。

### 5.1 负载中性校准修订

首次 8×5090 smoke 显示，`local_hmt` 的 block 3/4 在分叉后两步即超过预注册的负载可比性门；该尝试保留为无效工程证据，负载阈值不放宽。为使三臂从可比的专家边际分布起步，在同一独立 calibration token 上，为每个处理臂、每层拟合一个冻结的专家常数 logit offset，使硬 top-1 专家占比匹配分叉点 native 占比。native offset 恒为零；offset 不依赖 token、不增加可训练参数、不改变频带投影或专家输入，并在整个 2B 续训中固定。artifact 必须同时证明：（1）校准后 entropy/max-share 与 native 的差异分别不超过 0.005；（2）blocks 2--4 的 token 级 route disagreement 仍大于 2%，以排除“校准抹掉干预”。正式 smoke 仍执行第 8 节更严格的训练后负载门。

## 6. Primary Metric

在相同 1,024 个 held-out DCLM 文档上计算每文档 next-token NLL。对 replica $s$：

$$
\Delta L_{a:native}^{(s)}
=L_a^{(s)}(2B)-L_{native}^{(s)}(2B).
$$

单位 nat/token，负值表示处理更好。每个 replica 做 2,000 次 paired document bootstrap；同时报告两个 replica 的点估计、区间和等权 pooled effect。主结论要求两个 replica 方向一致，不把文档数伪装成训练 seed 数。

token-normalized held-out NLL AUC 为共同主支持指标，用来排除只在终点偶然反转。

## 7. Expert Differentiation And Utility Metrics

这些指标解释机制，不能替代 NLL：

1. **专家更新范数：**相邻 milestone 间每个 expert 参数位移，除以该 expert 接收的 routed token 数。
2. **同专家梯度冲突：**在固定、互斥 held-out document groups 上，对同一 expert 参数的 LM-loss gradient 做 cosine；报告中位 cosine 与负值比例。负值表示两组数据要求该 expert 朝相反方向更新。
3. **forced-expert utility：**在固定层保留 native routing weight，只把 top-1 expert 身份替换为每个候选 expert，得到每文档/条件的反事实 NLL；报告专家效用离散度、校准/测试最优专家稳定性和 native route regret。
4. **功能冗余：**同一固定 token 上不同 expert 输出的 pairwise cosine；越高表示功能越重复。
5. **路由—效用绑定：**native/处理 Router 选择的 expert 相对反事实最优 expert 的 regret；越低表示选择更接近有用专家。

WOS domain/topic purity 只描述路由结构，不进入功能裁定。

## 8. Manipulation, Load, And Compute Guards

- 固定 DCLM token 相对同 replica native 的 route disagreement 必须在 block 2--4 至少一层超过 2%；否则 treatment 未生效。
- 所有层无 dead expert、无 capacity drop；milestone normalized load entropy $>=0.95$，最大 expert share $<=0.25$。
- 同 replica 处理相对 native 的 load entropy 差绝对值 $<=0.02$、最大 share 差绝对值 $<=0.05$；否则 NLL 只可判 insufficient。
- active parameters、训练 token、optimizer steps、capacity、checkpoint、数据顺序与 kernel 路径一致；记录实测 step time 和解析 FLOPs。
- native replay、source replay、selected-expert top-1 与 checkpoint exact-resume 必须通过。
- 为使 SPOT 恢复不引入额外随机实验臂，训练启用确定性 CUDA 算法与固定 cuBLAS workspace；续训 seed 只在公共 step 800 分叉时重置，后续恢复保留 checkpoint RNG。每个 optimizer step 记录 rank-0 实际输入 batch 的 SHA-256；同源连续/恢复 smoke 必须具有相同 batch hash、参数相对误差 $\le2\times10^{-6}$、logit 相对误差 $\le2\times10^{-5}$、top-1 完全一致与 NLL 差 $\le2\times10^{-5}$。若恢复时已达到目标 step，runner 必须零更新退出。

## 9. Statistics And Comparisons

主比较分组为：

1. `local_hmt - native_full`：逐层本地频带约束的总效应；
2. `layer1_relay_hmt - native_full`：固定浅层坐标的总效应；
3. `layer1_relay_hmt - local_hmt`：频带 source 层的效应。

层内机制比较为 blocks 2/3/4；训练阶段为 954/1272/1908/2544。两 replicas 是复现单位；文档 bootstrap 只评估同一模型上的 held-out 文档不确定性。

## 10. Stage Plan And Stop Rules

1. **S0 provenance：**代码、branch、数据、artifact、replica seeds 与资源 hash。
2. **S1 unit/local：**公式恒等、source gradient、各 arm 参数/FLOP、forced-expert no-op、resume unit tests。
3. **S2 8×5090 smoke：**每 replica 三 arm 从 step800 到 step802；检查八 rank、source、Gate 梯度、中心 cadence、负载、checkpoint/resume 与 analyzer closure。
4. **S3 full：**六个独立 ACP jobs 到 step2544；任一 arm load guard terminal failure 时停止该 replica 的主比较。
5. **S4 evaluation：**NLL、route/load、basis、update/conflict、forced utility、redundancy。
6. **S5 verdict/docs：**typed verdict、图表、summary/detailed、Anchor 与 0803 Focus。

smoke 只验证实现；短程 loss 不作科学裁定。full 中不得降低负载门、缩短 2B 或删除不利 replica。

## 11. Runtime Resource Contract

执行面为 SCO ACP；`workspace=share-space`、`AEC2=computing-cluster-5090-01g`、`worker_spec=n12lp.nn.i10a.8`、1 node、8×RTX5090、`quota=spot`、priority normal。每 arm/replica 一个 job。SPOT 断点必须能 exact-resume；不得替换 debug cluster。

## 12. Figures And Tables

- Figure 1：两 replicas 的 held-out NLL vs cumulative FLOPs；三 arm 同图。
- Figure 2：最终 $\Delta$NLL 与 paired CI，按 replica 和 pooled 分组。
- Figure 3：block 2--4 的 route disagreement、load entropy 与 max share。
- Figure 4：专家 gradient conflict、forced utility/regret、output redundancy 的机制面板。
- Table 1：三 arm 的参数、FLOPs、tokens、负载与完成护栏。
- Table 2：三项主 pairwise comparison 与 typed verdict。

每张图必须实际打开检查；图注明确单位、允许结论和不能证明之处。

## 13. Pass / Fail / Insufficient

- **Pass with functional differentiation：**至少一个 treatment 在两个 replicas 中相对 native 的最终 $\Delta$NLL paired 95% 上界均小于 0，NLL AUC 同向，并至少一项专家功能指标在两个 replicas 中同向改善且不是负载造成。
- **Quality-only：**NLL 通过，但预注册功能指标不支持更明确分工；只能称训练质量改善。
- **Specialization-only：**功能指标改善但 NLL 不改善；不能称训练收益。
- **Distribution-only / Fail：**路由明显改变，但两个 treatments 都没有稳定 NLL 或功能改善，或稳定更差。
- **Insufficient：**配对、两个 replicas、2B 完成、load/compute、basis/source、resume、forced-expert 或 held-out 评估任一关键 guard 失败。

## 14. Claim Boundary And Deliverables

本实验不能证明从初始化形成、H→M→T 顺序最优、covariance rank 具有普遍语义、随机同维日程更差，或扩展到更深模型。它只回答一个公共早期状态后的四层 DCLM 因果分叉。

交付：artifact/branch/data/source manifest；六个 job IDs 与完整 milestones；held-out per-document NLL；route/load/update/conflict/utility/redundancy tables；四张中心图；`summary.md`、`detailed.md`；Anchor 更新；`daily_research_reports/backup/2026/08/0803/focus.md`。不修改 graph，不 commit/push。
