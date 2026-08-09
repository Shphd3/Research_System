---
anchor_id: 15_05_03_progressive_band_source_routing
status: completed_specialization_only_without_quality_pass
canonical_language: en
companion_language: zh
thinking_card: 15_05_03_progressive_band_source_routing_thinking_card_cn.md
parent_anchor: 15_05_functional_coordinate_admission
updated: 2026-08-02
---

# A15_05_03 逐层频带来源与专家分工

## 1. Problem Definition

**唯一决策问题：** 从同一个 0.629B-token 四层 DCLM MoE 状态分叉后，让第 2、3、4 层分别按 head、middle、tail 路由时，使用各层自己的频谱还是统一使用第一层输出的频谱，能否相对完整表征 Router 形成更有功能差异的专家，并改善匹配计算的 2B held-out NLL？

本 Anchor 不把“层级分化”定义为路由不同或负载均衡。功能分化至少要求 held-out 反事实专家效用、路由—效用关系、专家更新冲突或功能冗余中的独立证据。

## 2. Physical Priors

1. covariance 各向异性会因果改变线性 Gate 的有限时间学习速度，但不指定正确的专家划分。
2. 不同层的同名频带可编码不同信息，因此逐层本地频带可能提供深度条件化坐标。
3. 第一层输出的固定坐标可能减少跨层表征漂移，也可能过早锁定粗信息，使深层无法使用新形成的条件。
4. 固定投影会丢失 Gate 信息；只要 native 完整表示已经有效，任何硬频带日程都可能有害。

## 3. Falsifiable Hypotheses

**H1（逐层本地分工）：** `local-HMT` 在第 2/3/4 层依次使用各自 H/M/T 后，相对 native 降低 2B held-out NLL，并形成更低专家内更新冲突或更稳定的条件专家效用。

**H2（浅层坐标 relay）：** `layer1-relay-HMT` 使用同一第一层输出的 H/M/T，若跨层坐标稳定性是关键，应超过 `local-HMT`；若深层新信息不可由第一层预见，则它应落后。

**最强 rival：** 两种处理只改变路由或瓶颈维数，不能改善功能；NLL 差异由负载、计算或续训随机性解释。

**Pass：** 至少一个处理在两套配对续训中都改善 native 的 2B NLL，并有同向专家功能证据；**Fail/distribution-only：** 处理显著改变路由但不改善 NLL/功能；**Insufficient：** 配对、负载、计算、基底、续训或两次复现护栏失败。

## 4. Mathematical Model

四层编号为 $1,2,3,4$；第一层保持 native。令 $r_\ell$ 为第 $\ell$ 层实际 Router 输入，$s_1$ 为第一层完整 block 输出经无参数 RMS 归一化后的同 token 表征。冻结分叉时刻的投影后：

$$
z_\ell^{\mathrm{local}}
=W_\ell\left[\mu_{\ell,B_\ell}
+P_{\ell,B_\ell}(r_\ell-\mu_{\ell,B_\ell})\right],
$$

$$
z_\ell^{\mathrm{relay}}
=W_\ell\left[\mu_{1,B_\ell}
+P_{1,B_\ell}(s_1-\mu_{1,B_\ell})\right],
$$

其中 $B_2=H_{64}$、$B_3=M_{256}$、$B_4=T_{448}$。专家输入始终是本层完整 native 表征。主效应为同一 held-out 文档上的

$$
\Delta L_{a:native}=L_a^{2B}-L_{native}^{2B},
$$

单位为 nat/token，负值更好。

## 5. Computational Realization

模型沿用 A15_05_05 的 H768、4-layer、8 sparse experts + 1 shared expert、top-1、running center 和 $\lambda_{LB}=0.01$。三个 arm 从同一 step-800 checkpoint 分叉并到 step 2544；两套后分叉数据/RNG seeds 为 17、29。每套内模型、优化器、scheduler、游标、投影 artifact 与数据顺序严格配对。

`native-full` 保持完整 Router；`local-HMT` 只改变第 2--4 层 Gate 视图；`layer1-relay-HMT` 将第一层 block 输出作为后三层 Gate source。所有 arm 计算同一个第一层 source 和同形状投影路径，保持参数与核近似匹配。

## 6. Minimal Falsification Tests

1. native no-op、实际 source replay、投影秩/幂等/能量重构和 calibration half-split 必须通过。
2. 同一 replica 的三 arm 必须从相同 model/optimizer/scheduler/data cursor 开始；第二 replica 只改变预注册的后分叉数据/RNG seed。
3. 三 arm 的 token、active parameters、capacity、累计 FLOPs、负载熵、最大 expert share 和 capacity drop 必须可比。
4. 固定 token route disagreement 证明处理确实生效；它不替代 NLL。
5. 专家功能至少报告 forced-expert utility、route regret、专家输出冗余、更新范数和同专家梯度冲突；任何一个都不能单独替代 held-out NLL。
6. 训练后重估谱带 overlap；若身份丢失，只能称 frozen-subspace treatment。

## 7. Current Evidence

A15_02_01 已证明受控四层模型中同名 covariance rank 会随层编码不同变量：L3/L4 F1/head 特异携带中间状态，F2 特异保留粗条件，但组合结果没有固定落入 H/M/T。A15_05_05 又证明同层固定 H/M/T/N 可以改变 4.98%--21.88% 的路由，却全部输给 native 2B NLL。

E01 已完成两个配对 continuation replicas 的三臂 2B 训练，全部 checkpoint、数据哈希、负载、计算和复现护栏通过。`local-HMT` 相对 native 的 pooled 终点 $\Delta$NLL 为 +0.002174 $[0.001758,0.002590]$ nat/token；`layer1-relay-HMT` 为 −0.001756 $[-0.002352,-0.001119]$，两个 replicas 都在终点略好。

但是 relay 从公共分叉切换视图时产生大幅损失，其两条 NLL AUC 均差于 native，平均差 +0.02135 nat/token，因此没有训练效率收益。local 与 relay 分别改变后三层平均 7.12% 与 19.70% 的路由；relay 的 forced-expert route regret 在两个 replicas 中均降低，但专家效用离散度下降、输出冗余上升，其他功能指标不一致。正式裁定为 `specialization_only_without_quality_pass`：显式结构改变了路由和部分功能，却未形成一致的有益专家分工。

## 8. Claim Boundary And Next Decision

该结论只适用于一个公共 0.629B-token 分叉后的四层 DCLM 续训机制；不能证明从初始化形成、H→M→T 是最优顺序、频带对应自然语言层级，或该结构扩展到更深模型。没有同维随机日程训练，因此 relay 的晚期终点优势也不能单独证明 covariance rank 优于任意固定降维日程。

**唯一下一决策：** 关闭“固定 H→M→T rank 日程本身就是功能路由原则”的候选；下一种跨层 Router 必须先以可学习的功能坐标，在 held-out 专家效用或更新兼容性上超过同维随机与错误层，才允许进入匹配训练。
