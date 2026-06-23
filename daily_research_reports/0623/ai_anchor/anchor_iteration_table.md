# Anchor Iteration Table

## Purpose

This note summarizes the anchor line as research decisions, not as experiment logs.

Four questions are used for each iteration:

1. What parent question did this iteration answer?
2. What belief did it update?
3. Did it have a clear decision tree?
4. What next step did it open?

## Current Mainline Judgment

The project has moved through three levels:

```text
definition
-> failure mechanism
-> initialization / preservation
```

Current strongest conclusion:

```text
Real-data proxy features are measurable and linearly routable,
but ordinary DCLM next-token training does not preserve proxy routing.
The next mainline is preservation / anti-feedback, not utility binding.
```

## Iteration Table

| Iteration | 更新了什么 | 是否可信 | 下一步 |
| --- | --- | --- | --- |
| I0. Specialization definition and ordinary top-1 audit: A01-A04 | 父问题：什么才算 expert specialization，以及 ordinary top-1 为什么不自然形成它。更新：高 route purity、same-feature consistency、load balance 都不是充分证据；必须区分 feature identity、non-collapse、training preservation、expert utility。 | 中高。Decision tree 清楚：先定义 feature，再查 routing，再查 utility。但早期证据更多是诊断和边界，不是方法闭环。 | 不直接 claim specialization；先找 collapse / shortcut / lock-in 机制。 |
| I1. Minimal top-1 lock-in mechanism: A02 | 父问题：top-1 collapse 是训练中逐渐漂移，还是早期 assignment 被放大。更新：失败 seed 在 step 0 就 collapse，成功 seed 初始 split 后能保持；early top-1 lock-in 是核心机制候选。 | 高。Decision tree 明确：若 step0 决定最终，则研究 initialization / anti-lockin；若 late drift，则研究训练中控制。结果支持前者。 | 研究 structured initialization、anti-lockin、anti-collapse，而不是只看最终 routing。 |
| I2. Inhibition / center separation intervention: A05_01-A05_02 | 父问题：几何分离或 inhibition 能否直接修复 routing collapse。更新：center separation alone 不够；token-conditioned inhibition 是相关机制类，但当前形式会强化 early lock-in / collapse。 | 中高。Decision tree 清楚：若中心分离成功则走 geometry method；若失败则回到 early feedback/control。结果边界清楚。 | 不把 inhibition 当主方法；转向 common-logit / hidden geometry 的更细机制。 |
| I3. Common component and early common-logit feedback: A05_03-A05_04, A06_01-A06_02 | 父问题：uniform feature 下为什么仍出现 load concentration；真实 DCLM 里 early concentration 从哪里来。更新：common component / common logit 是强机制；real DCLM step10 有 hidden-producing path 与 gate-hidden interaction；expert-spectrum/common-filtered init 不足以解决。 | 高。Decision tree 明确：若 common control 可修复则走 common-filtered init；若不行则需要 proxy feature 和 preservation。A06_01 negative + A06_02 mechanism 形成闭环。 | 不再把 common/load repair 当 specialization；需要定义真实 feature proxy，并分离 initialization 与 training preservation。 |
| I4. Synthetic hidden-state geometry decomposition: A06_03-A06_07 | 父问题：均匀 feature 是否意味着均匀 routing / feature specialization。更新：gate row-norm 是 gate-only baseline；synthetic hidden state 中 common component 主导 load；common 后仍有 residual geometry；oracle feature partition 可达；simple label-free global controls 只修 load，不修 feature NMI。 | 高。Decision tree 很清楚：row-norm -> common -> residual geometry -> oracle reachability -> label-free global controls。每一步都有正反对照。 | 停止推进 simple centering/projection/whitening；转向 label-free feature discovery，而不是 load-only method。 |
| I5. Synthetic label-free discovery and basin preservation: A06_08-A06_09 | 父问题：不用 label 能否发现 pseudo-feature centers；发现后训练能否保持。更新：route-position residual k-means 可无标签恢复 synthetic feature partition；在 synthetic route-position training 中 pseudo init 可保持 feature routing。 | 高，但边界窄。Decision tree 明确：A06_08 先问 discovery，A06_09 再问 training basin。可信点是 synthetic positive control 完整；边界是不能外推到真实 DCLM。 | 进入真实数据前，必须先定义 real-data proxy feature；不能直接用 synthetic feature_NMI。 |
| I6. Real-DCLM proxy and router bridge: A06_10-A06_11 | 父问题：真实 DCLM 没有 feature label 时，能否构造可评估 proxy，并用它初始化 router。更新：真实 hidden geometry 有稳定 label-free proxy；raw proxy centers 可以强力初始化 raw-input linear router。 | 高。Decision tree 明确：proxy exists -> bridge works。A06_10/A06_11 都有 random、nuisance、shuffled guard。边界是 proxy 不是 semantic feature，raw center 优于 residual center。 | 进入训练保持测试；主条件应是 raw-center equal-norm，不是 residual-center。 |
| I7. Real-DCLM training preservation and failure localization: A06_12-A06_13 | 父问题：真实 proxy routing 能否被普通 DCLM training 保持；如果失败，第一失败点在哪。更新：raw-center step0 routing 很强，但 step5/10 迅速坍缩；loss 与 random 相近；第一失败点是 training feedback override，不是 proxy discovery 或 linear bridge。 | 高。Decision tree 最清楚：A06_12 preservation fail -> A06_13 bottleneck audit -> stop utility branch。结论可信，因为 stage contract 顺序完整。 | 下一步必须是 preservation / anti-feedback anchor：router freeze、delayed router updates、lower router LR、proxy-preservation loss、common/load anti-collapse。 |
| I8. Utility binding and utility-aware init: A06_14-A06_15 | 父问题：如果 routing preserved，专家是否对 proxy group 有 causal utility，以及 utility 能否改进初始化。更新：目前没有执行资格；A06_12 preservation dependency failed，所以 utility branch 被正确 parked。 | 可信，作为 decision-tree 停止点。不是实验结论，而是流程结论：当前不能测 utility，否则会混淆“无 utility”和“routing 已坍缩”。 | 等 preservation 通过后再恢复 A06_14；A06_15 必须等 A06_14 给出 utility table。 |

## Condensed Decision Tree

```text
What counts as specialization?
-> route purity/load is insufficient

Why does ordinary top-1 fail?
-> early lock-in and common/load feedback are central

Can geometry/common controls solve it?
-> simple load controls are insufficient

Can feature partition be reached?
-> yes with oracle / synthetic pseudo centers

Can label-free discovery work in synthetic hidden states?
-> yes

Can the idea transfer to real DCLM?
-> proxy exists and linear bridge works

Does ordinary training preserve it?
-> no

Therefore next:
preservation / anti-feedback before utility binding
```

## Current Next Anchor

The next valuable anchor should answer:

```text
Can we preserve raw-center proxy routing through the step-5/10 DCLM collapse window?
```

Minimal decision tree:

```text
If preservation succeeds:
  resume A06_14 utility binding.

If preservation partially succeeds:
  identify which intervention delays collapse and refine.

If preservation fails:
  decompose whether the failure is router LR, hidden drift, common logit, or top-1 starvation.
```

Recommended first intervention set:

- router freeze / delayed router update;
- lower router learning rate;
- proxy-route preservation auxiliary loss;
- common/load anti-collapse regularizer.
