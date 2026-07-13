# 05-06-07 总研究线：从初始化 collapse 到 interference value

## 结论

当前主线不能写成“已经证明 MoE 形成真实语义专家”。更准确的结论是：

```text
普通 top-1 gate 会被 common component、错误 hidden-state population 和
early-training feedback 推入错误路由对象；route-position feature partition
在受控设置中可发现、可路由、可保持，但真实 DCLM proxy partition 会被普通
next-token training 在 step 5/10 覆盖。functional specialization 必须在
preservation 成立后，再通过 common/rare interference 或 expert utility 判断。
```

0630 更新：

```text
controlled no-position bridge 中，center initialization 的保持已被 A06_21
分解为 margin-budget 机制：pseudo/oracle center 保持正 current margin、
正 cluster-aware margin 和零 sign flip；负向压力主要来自 feature-center
drift，但初始 margin buffer 足够大，没有跨 expert boundary。下一步不是再
做 controlled feature-existence sweep，而是把同样分解带到 real-DCLM
proxy-init failure。
```

0701 更新：

```text
A06_23 进一步说明：controlled bridge 中不是“只要初始 margin 为正就一定
能保持”。通过把 router rows 向共同均值收缩，$q\ge0.05$ 全部保持原来的
feature-to-expert 映射，但 $q=0.02$ 虽然 step 0 仍然分对，训练中会跨过
expert boundary。所以下一步 real-DCLM 审计要看 margin 是否大到足以扛过
step 5/10 的早期漂移，而不是只看 step-0 margin 是否为正。
```

0701 nested-learning 转向：

```text
A06_22 已复现 real-DCLM proxy routing 在 step 5/10 被擦掉，但
common/residual dominance 对 common projector 不稳健：mean-common 支持
common-dominated update，top hidden-PC 和 router-row subspace 不支持。
因此 common 现在是候选机制，不是已确认根因。下一步应把导师
nested learning 中“高频 common 高增益通道可能吸收 rare/组合特征”的
观点转成可证伪审计：先定义更物理的 common operator P_C，再比较 raw h
和 common-subtracted (I-P_C)h 的 routing，看 rare-feature margin、
sign flip 和 LM loss 是否改善。
```

## 总愿景与裁定层级

整个项目的推进逻辑是：

```text
模糊愿景 -> 现象 -> 物理先验 -> 数学建模 -> 可证伪假设
-> minimal 实验 -> 更新理解
```

这不是一条“直接提出方法”的路线，而是逐层裁定：

| 层级 | 要裁定的问题 | 主 metric | 不能声称什么 |
|---|---|---|---|
| 0. Failure | ordinary top-1 为什么 collapse / merge | step-0 NMI、max load、common margin | 不能 claim method |
| 1. Proxy discovery | route-relevant proxy 是否存在 | cluster stability、proxy NMI、nuisance guards | 不能 claim semantic expert |
| 2. Initialization | proxy 是否能转成 gate rows | step-0 `proxy_route_NMI`、load | 不能 claim training success |
| 3. Preservation | partition 是否穿过 early training | `proxy_route_NMI@step5/10` + LM loss | 不能 claim utility |
| 4. Utility | preserved partition 是否减少 interference | rare loss、route-function binding、causal ablation | 不能只凭 load/NMI claim specialization |
| 5. Scaling | many experts 是否提升 activated capacity | per-expert effective rank、routing stability、utility per activated FLOP | 不能只看 active experts |

这里 NMI 是“归一化互信息”，只衡量 route label 和目标划分的对齐程度；
它可以裁定 collapse / alignment，但不能单独证明 expert 有功能价值。

## 当前所处位置

当前主动瓶颈是：

```text
3. Preservation
```

更具体地说：

```text
0 层 failure mechanism 已经有 common component、wrong population 和
early-training feedback 证据；
1 层 proxy discovery 已经有 controlled 与 real-DCLM proxy 证据，但语义边界仍在；
2 层 initialization 已经有 step-0 real-DCLM proxy-center router 证据；
3 层 preservation 仍未解决：ordinary training 会在 step 5/10 覆盖 proxy routing；
4 层 utility 只有 controlled D07 支持；当前正在用 nested-learning 启发把
   common/rare interference 转成 preservation 后的下一步机制问题，但
   real-DCLM / neural utility 仍不能 claim；
5 层 scaling 暂停，等 preservation 与 utility 都更清楚后再进入。
```

## 逻辑链条

```text
05: 为什么普通 top-1 会失败
-> common component 和 early feedback 会制造 collapse 或错误 route basin

06: 正确 partition 是否可发现、可初始化、可保持
-> route-position geometry 可达
-> all-position clustering 是错误样本池
-> center initialization 的保持来自 positive margin buffer，而不是 active tracking
-> A06_21 支持 controlled margin-budget 解释：正 margin / 零 sign flip / 正
   cluster-aware margin 比 NMI alone 更接近 preservation
-> A06_23 支持 finite-threshold 解释：正 margin 需要足够厚；$q=0.02$
   会在训练中跨 boundary，而 $q\ge0.05$ 保持
-> real-DCLM proxy 可在 step 0 线性路由
-> ordinary training 会在 step 5/10 覆盖 proxy routing
-> A06_22 说明真实崩塌存在，但 common/residual 判断随 common projector
   翻转，不能直接 claim common 是根因
-> nested learning 提供下一步物理先验：高频 common 通道可能形成高增益
   空间，rare/组合特征可能在 routing 或 update 中被这个空间吸收

07: 即使 partition 存在，它是否有价值
-> value 不能用 load balance 或 route purity 证明
-> controlled D07 支持 common-control 减少 rare interference 和 route-function binding
-> neural A07_04 仍是 insufficient evidence
```

## 支持线：11 long-horizon MTP objective

MTP 线现在应作为“目标函数如何把长程变量写入当前 hidden state”的支持线，
而不是替代 05/06/07 gating 主线。

当前 A11 结论是：

```text
在受控 long-horizon 构造中，如果 K 覆盖第一个包含早期变量 Z 的未来位置，
并且该未来目标是 Z 的一一对应编码，那么低该位置预测损失会迫使当前
hidden state h_T 含有 Z。
```

A11_05 进一步说明：

```text
在 clean tau=3 的 all-position 训练中，直接加到 decision-prefix h_T 上的
horizon-3 监督，是 K=3 更快、更稳定恢复 Z 的一个受支持机制成分；
但 all-position 间接迁移仍然存在，所以不能说 direct supervision 是唯一
路径，也不能推出自然语言或 MoE 路由收益。
```

A11_06 到 A11_10 进一步更新：

```text
11_06 支持一阶效率机制：在无泄漏 decision-prefix 设置中，K3 的
hidden readout-margin velocity 为正，K1/K2 近似为 0。11_07 支持
direct horizon-3 监督在无泄漏 all-position 训练中给出更强 native H3、
M_Z_ref、reach rate 和 early AUC。11_08 / 11_08b / 11_09 支持
general-K vector-sum 与 next-K inclusion law：K 的作用取决于是否新增
informative horizon，以及新增方向是否对齐。11_10 支持 native/probe
split：K2 和 masked K3 可以有非平凡 Q，但 native H3=0 且 M_Z_ref 近
0；direct 条件 native H3=1 且 M_Z_ref 大。因此 Q 不能单独作为 direct
supervision 证据。
```

它对 gating 主线的意义是提供一个候选桥：

```text
未来可以问：long-horizon / multi-token supervision 是否能让
route-relevant hidden states 更早、更稳定地包含 feature 信息，并形成更厚
的 routing margin？这个桥接必须使用 native H3 / M_Z_ref 保护 direct
semantic-state evidence，不能只看 Q。
```

当前不能 claim：

```text
MTP 已证明自然语言更强；
MTP 已证明 MoE routing preservation；
MTP 已证明 semantic expert identity 或 expert utility；
K 越大越好。
Q 单独证明 direct supervision。
```

0713 更新：

```text
A11_23/23b 表明当前从头训练的神经序列任务没有通过 task gate；更深、更宽、
更长训练和显式 pair-token 均近机会水平。A11_24 在 oracle-factor 线性模型中
支持结构性 rank competition：rank 1 的 MTP 标准损失 gap 为
0.9084--1.0218，rank 2 时消失。A11_25 表明等辅助剂量课程不能修复 rank-1
缺秩，Pareto pass 为 0/5。A11_26 因此 parks real/scale transfer；Router 继续
parked。下一步只能先建立一个已具备两跳能力的 neural bridge。
```

## 当前问题

当前不是继续证明 controlled feature geometry 存在。当前要裁定的是：

```text
能否定义一个稳定、物理上合理的 common operator，并证明 common-subtracted
routing 能让 rare-feature margin 更稳，同时不损害 LM loss？
```

如果不能保持 routing，就不能合法进入真实语料上的 expert utility claim。

## 合成数据边界

合成实验可以证明：

- 在已知 feature label 和可控 nuisance 下，某个机制是否可能成立；
- 某个 metric surface 是否能区分 oracle、null 和 method；
- route-position feature geometry 是否可发现、可路由、可保持；
- common-control 是否在 controlled D07 中减少 rare-feature interference。

合成实验不能证明：

- natural-language semantic feature；
- real checkpoint 中存在同样 expert；
- 真实训练会保持同样 partition；
- 可部署 MoE routing 已经有效；
- reverse KV retrieval 可以由当前结果推出。

## 真实 DCLM proxy 边界

真实 DCLM proxy 实验可以证明：

- hidden states 中存在稳定、可重复的 proxy clusters；
- proxy centers 能转成 step-0 linear top-1 router rows；
- ordinary next-token training 是否保持或覆盖这个 proxy partition。

真实 DCLM proxy 实验不能单独证明：

- proxy cluster 就是语义 feature；
- routed expert 对该 feature 有 causal utility；
- MoE 优于 dense/shared baseline；
- 最终 pretrained MoE 会自然形成该结构。

## 下一步

优先写一个 nested-learning-inspired common/rare routing audit：

```text
给定 common projector P_C，比较 raw routing on h 与 residual routing on
(I-P_C)h。若 residual routing 提高 rare-feature margin、降低 sign flip，
且 LM loss 不恶化，才进入下一轮 gating mechanism 建模。
```

这个审计必须继承 A06_22 的边界：

```text
如果 conclusion 仍随 mean-common / top hidden-PC / router-row subspace
等 common projector 翻转，则不能 claim common-subtraction method。
```

若 common operator 变得稳定，再把导师 nested learning 的谱各向异性机制
写成 anchor：common high-gain band 是否消耗 rare-feature margin。若审计
通过，再回到 A07 utility；若不通过，先修 common operator 定义，不直接换
方法。

## 入口文件

```text
Projects/from-attention-to-search/main/problem_anchors/05_06_07_initialization_collapse_to_interference_chain_cn.md
Projects/from-attention-to-search/main/experiments/A06/A06_12_real_dclm_proxy_init_training_preservation/summary.md
Projects/from-attention-to-search/main/experiments/A06/A06_21_margin_budget_preservation_audit/summary.md
Projects/from-attention-to-search/main/experiments/A06/A06_22_router_common_residual_trajectory_audit/summary.md
Projects/from-attention-to-search/main/experiments/A06/A06_23_top1_lockin_margin_threshold/summary.md
Projects/from-attention-to-search/main/experiments/A07/A07_04_common_rare_gradient_conflict_splitting/summary.md
Projects/from-attention-to-search/main/problem_anchors/11_long_horizon_mtp_objective/README.md
Projects/from-attention-to-search/main/stories/11_long_horizon_mtp_objective/02_mtp_interference_capacity_curriculum_cn.md
Projects/from-attention-to-search/main/experiments/A11/A11_04_03_k3_efficiency_advantage/summary.md
Projects/from-attention-to-search/main/experiments/A11/A11_04_03_k3_efficiency_advantage/meeting_brief.md
Projects/from-attention-to-search/main/experiments/A11/A11_05_semantic_efficiency_bridge/summary.md
Projects/from-attention-to-search/main/experiments/A11/A11_06_readout_effective_margin_efficiency/summary.md
Projects/from-attention-to-search/main/experiments/A11/A11_07_no_leakage_all_position_efficiency/summary.md
Projects/from-attention-to-search/main/experiments/A11/A11_08_general_k_readout_margin_dynamics/summary.md
Projects/from-attention-to-search/main/experiments/A11/A11_08b_output_geometry_dynamics_audit/summary.md
Projects/from-attention-to-search/main/experiments/A11/A11_09_next_k_inclusion_law/summary.md
Projects/from-attention-to-search/main/experiments/A11/A11_10_all_position_indirect_transfer_dynamics/summary.md
daily_research_reports/0629/docs/nested_prediction_spectral_anisotropy_causal_rewrite_v4.md
daily_research_reports/0701/meeting_brief.md
```
