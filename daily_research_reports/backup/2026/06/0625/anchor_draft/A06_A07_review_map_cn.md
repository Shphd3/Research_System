# A06 / A07 Review Map

## 结论

A06 是当前主线的局部推进面：先把 route-relevant state selector 做干净，再把
通过的 proxy 交给 real-DCLM initialization / preservation。A07 是机制储备：
可以并行准备，但不能替代 A06 preservation。

本轮清理后的判断：两个 anchors 合格作为审阅稿；两个 protocols 合格作为
“待批准实验设计”，但还不能直接运行。A06/A07 都加入了 gated real-data
touchpoint：主裁决仍在 controlled surface 上，真实数据只作为通过后的兼容性
或迁移 guard。

## 阅读方式

每个 anchor 只需要先读四处：

1. `0. researcher judgment record`
2. `Decision question`
3. `Primary metric / Minimal Falsification Test`
4. `Can claim / Cannot claim / Next decision`

如果这四处不能让人直接判断“做什么、为什么做、什么结果会改变判断”，这个
anchor 就要继续压缩，不能靠 protocol 里的大表来补。

## A06 当前认知

**主问题：** hidden-state geometry 能否支持 label-free proxy-level gate
initialization，并且 routing 能否被训练保持？

**当前结论：**

```text
real-DCLM proxy geometry exists;
proxy centers can initialize a strong step-0 raw-input router;
ordinary DCLM training overwrites the proxy routing by step 5/10;
controlled no-pos bridge shows route-position discovery/preservation can pass;
A06_17 shows all-position clustering fails because the fit pool is wrong.
```

**当前可做下一步：** label-free route-relevant state selection。

**主 metric：** held-out route-position `feature_NMI`。

**不能 claim：** real-DCLM semantic feature、training preservation、expert
utility。

## A06 实验审阅

| Experiment | 更新的认知 | 当前状态 |
|---|---|---|
| A06_01 | expert-spectrum/common-filtered initialization 不足以成为方法；需要 stage-wise mechanism。 | negative / informative |
| A06_02_01 | real-DCLM early common/load amplification 是风险；不能只看 step-0。 | mechanism prior |
| A06_02_02 | freeze/split 支持 common-stability audit；保护 early dynamics 判断。 | mechanism prior |
| A06_03 | row-norm variation 会制造 load 假象；equal-norm guard 必需。 | guard |
| A06_04 | synthetic hidden states 中 common component 是 load imbalance 主因。 | mechanism evidence |
| A06_05 | common-centered residual 中仍有 feature-like geometry。 | supports discovery |
| A06_06 | oracle feature-centroid initialization 可达。 | positive control |
| A06_07 | centering/projection/whitening主要修 load，不恢复 feature NMI。 | weakened |
| A06_08 | route-position residual clustering 可 label-free 发现 synthetic feature centers。 | supported, synthetic |
| A06_08 slot length | A06_04-A06_07 结论对 slot length 稳定。 | supporting |
| A06_09 | synthetic pseudo init 在简单训练中可保持。 | supported, synthetic |
| A06_10 | real-DCLM hidden states 有稳定 proxy clusters，但不是语义证明。 | supported with boundary |
| A06_11 | real-DCLM proxy centers 可转成 strong step-0 raw-input router。 | supported with boundary |
| A06_12 | ordinary DCLM training 不保持 proxy routing，step 5/10 被覆盖。 | not supported |
| A06_13 | 第一失败点是 training feedback override，不是 proxy discovery 或 step-0 bridge。 | supported |
| A06_14 | real proxy utility binding 依赖 preservation。 | parked |
| A06_15 | utility-aware initialization 依赖 A06_14。 | parked |
| A06_16 | corrected no-pos bridge 中 discovery 和 same-model preservation 可过。 | supported with boundary |
| A06_17 | route-only/slot offset 3 完美；all-position 因 wrong pool 发生 whole-feature merge。 | supported |

## A06 下一步 anchor

**One-line anchor:** 不使用 feature label，判断能否选出该被聚类的
route-relevant hidden states，使 held-out route-position `feature_NMI` 高于
all-position baseline 并接近 route-only positive control。

**最小实验：** controlled selector audit。

**真实数据触点：** controlled selector 通过后，复用 A06_10/A06_11-style
real-DCLM hidden states 做 compatibility read；它只判断是否值得写 real proxy
extraction / step-0 initialization anchor，不证明 preservation 或 utility。

**具体条件放 protocol：** selector family、SAE 是否加入、seeds、nuisance guards、
load guards、real-DCLM bridge 是否加入、exact pass/fail threshold。

## A07 当前认知

**主问题：** 如果 partition 已经存在并被保持，它为什么有 functional value？

**当前结论：**

```text
controlled D07 已支持 metric surface -> common-control rare-loss gain
-> route-function binding；
neural A07_04 仍是 insufficient evidence；
A07 不应绕开 A06 preservation。
```

**机制储备方向：** common-update interference。

**当前应先裁定：** common-example update 是否因果伤害 rare/conflict loss。

## A07 实验审阅

| Experiment | 更新的认知 | 当前状态 |
|---|---|---|
| A07_01 | D07 controlled metric surface 合法；oracle 明显优于 null。 | supported |
| A07_02 | common-control 在 matched load 下减少 rare interference。 | supported, controlled |
| A07_03 | routed expert 对 conflict group 有 causal utility。 | supported, controlled |
| A07_04 | neural proxy 可测 conflict，但 rare-loss gain 小且 noisy；不能 claim real utility。 | insufficient evidence |
| A07_E01 | high-dimensional centered geometry 给 A07 提供支持性 metric/geometry audit。 | supporting |
| A07_E02 | text static geometry transfer 是支持性诊断，不是 utility 证明。 | supporting |

## A07 下一步 anchor

**One-line anchor:** 在 controlled nested-conflict surface 上，测试 common
update 是否比 norm-matched controls 更伤 rare loss；只有因果伤害成立，才进入
partition-value anchor。

**主 metric：** `common_to_rare_loss_effect`。

**guard：** `rare_common_update_fraction`、projector stability、common loss、
update norm、data/capacity controls。

**真实数据触点：** controlled causal perturbation 通过后，才看 real-DCLM
proxy/common/rare groups 上是否有同方向 observational signal；它只判断机制是否
值得迁移，不证明 MoE partition utility。

**具体条件放 protocol：** D1/D2 data surface、projector rank、optimizer-state
reconstruction、perturbation step size、matched controls、real-data bridge 是否
加入。

## 当前决策

1. A06 优先推进 `A06_route_relevant_proxy_extraction_anchor.md` 和对应
   protocol；批准后先跑 controlled selector audit。
2. A07 保留为 mechanism reserve，可并行跑 smoke，但 claim 不能越过
   controlled causal perturbation。
3. 所有 anchor 保留 0-8 结构；每节只放决策必要信息；详细实验条件进
   protocol。
4. 今晚审阅时只需批准三件事：A06 selector list、A06 是否包含 real-DCLM
   touchpoint、A07 是否只做 smoke 或进入完整 perturbation protocol。
