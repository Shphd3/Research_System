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
4 层 utility 只有 controlled D07 支持，real-DCLM / neural utility 不能 claim；
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
-> real-DCLM proxy 可在 step 0 线性路由
-> ordinary training 会在 step 5/10 覆盖 proxy routing

07: 即使 partition 存在，它是否有价值
-> value 不能用 load balance 或 route purity 证明
-> controlled D07 支持 common-control 减少 rare interference 和 route-function binding
-> neural A07_04 仍是 insufficient evidence
```

## 当前问题

当前不是继续证明 controlled feature geometry 存在。当前要裁定的是：

```text
real-DCLM proxy routing 能否穿过 step 5/10 的 early-training overwrite window？
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

优先把 A06_21 的 margin-budget audit 搬到 real-DCLM A06_12 proxy-init
training：

```text
step-0 proxy routing 被擦掉，是因为 residual margin 一开始就弱，
还是 early training 吃掉了 margin，还是 common direction 压过
residual feature term？
```

然后再写 real-DCLM preservation / anti-feedback protocol：

```text
固定 step-0 proxy labels；
比较 ordinary training 与若干 anti-feedback / preservation 条件；
主指标是 step 5/10 proxy_route_NMI；
保护指标是 LM loss、max load、active experts、common margin。
```

若 preservation 成功，再回到 A07 utility。若 preservation 失败，先用
A06_21-style diagnostics 分解 weak step-0 residual margin、early margin
consumption、common overwrite、token spread、expert feedback 和 optimizer
geometry，不直接换方法。

## 入口文件

```text
Projects/from-attention-to-search/main/problem_anchors/05_06_07_initialization_collapse_to_interference_chain_cn.md
Projects/from-attention-to-search/main/experiments/A06/A06_12_real_dclm_proxy_init_training_preservation/summary.md
Projects/from-attention-to-search/main/experiments/A06/A06_21_margin_budget_preservation_audit/summary.md
Projects/from-attention-to-search/main/experiments/A07/A07_04_common_rare_gradient_conflict_splitting/summary.md
```
