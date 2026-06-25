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

## 逻辑链条

```text
05: 为什么普通 top-1 会失败
-> common component 和 early feedback 会制造 collapse 或错误 route basin

06: 正确 partition 是否可发现、可初始化、可保持
-> route-position geometry 可达
-> all-position clustering 是错误样本池
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

优先写一个 real-DCLM preservation / anti-feedback protocol：

```text
固定 step-0 proxy labels；
比较 ordinary training 与若干 anti-feedback / preservation 条件；
主指标是 step 5/10 proxy_route_NMI；
保护指标是 LM loss、max load、active experts、common margin。
```

若 preservation 成功，再回到 A07 utility。若 preservation 失败，先分解
gate update、hidden-state drift、expert feedback 和 optimizer geometry，不直接换方法。

## 入口文件

```text
Projects/from-attention-to-search/main/problem_anchors/05_06_07_initialization_collapse_to_interference_chain_cn.md
Projects/from-attention-to-search/main/experiments/A06/A06_12_real_dclm_proxy_init_training_preservation/summary.md
Projects/from-attention-to-search/main/experiments/A07/A07_04_common_rare_gradient_conflict_splitting/summary.md
```
