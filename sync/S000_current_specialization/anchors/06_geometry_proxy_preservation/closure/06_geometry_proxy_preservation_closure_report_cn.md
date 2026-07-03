# A06 几何代理保持线 Closure Report

## 副标题

从 feature center discovery 到 margin-budget preservation。

英文 canonical 文件：[`06_geometry_proxy_preservation_closure_report.md`](06_geometry_proxy_preservation_closure_report.md)  
范围：A06 中关于隐藏状态几何、真实 DCLM proxy 初始化、训练保持机制的阶段性闭环。

## 摘要

当前结论：

```text
router-input hidden state 中可以发现 feature/proxy 结构，
并且这些中心可以初始化 top-1 MoE router。
在修正后的受控桥接实验中，center initialization 能保持，
原因是初始化 router 在 feature center 周围产生了正 route margin。
router 不需要主动追着漂移的 feature center 走。
但在真实 DCLM 下一词训练中，proxy routing 会在 step 5/10 被擦掉。
所以下一步要问：真实 DCLM 训练中，是 margin budget 的哪一项先失败？
```

这个 closure 说明：

- A06 已经从“feature-to-expert specialization 能不能形成”推进到
  “什么几何条件让它保持”。
- 受控实验中的答案是：route-relevant feature/proxy center 周围需要有
  正 margin basin。
- 真实 DCLM 的瓶颈不是 step-0 能不能线性 route，而是普通训练能不能保持。

仍然开放的问题：

- real-DCLM proxy cluster 是否是语义 feature。
- 高 route agreement 是否意味着 expert utility。
- real-DCLM failure 到底来自 common overwrite、representation drift、
  router drift、token spread，还是它们的相互作用。

## 术语解释

| 术语 | 朴素含义 | 具体对象 / 计算 | 为什么重要 | 不能证明什么 |
|---|---|---|---|---|
| feature | 合成数据里真正决定路由/预测的标签。 | 数据构造中的 synthetic feature id。 | 它是受控机制实验的干净目标。 | 真实语言语义。 |
| proxy | 真实 DCLM hidden state 里可复现的 cluster。 | 从 hidden states 聚类得到，并用 held-out stability 检验。 | 它是无标签真实数据中的可操作目标。 | 这个 cluster 是语义 feature。 |
| route-position hidden state | 真正送入 router 做决策的 hidden state。 | 修正后的受控桥接中，是 feature slot 的最后一个 token。 | 它是 router 初始化应该使用的状态群体。 | 所有位置都携带同样的 route 信息。 |
| all-position pool | 把 route 和 non-route 位置的 hidden states 混在一起。 | 对所有 token positions 做聚类或表征学习。 | 检验能否不依赖 position label 找到 route-relevant states。 | 它本身就是可靠的 router initializer。 |
| top-1 router | 每个 token 只发给得分最高 expert 的稀疏 router。 | $s_e(h)=w_e^\top h$，assignment 是 $\arg\max_e s_e(h)$。 | 它把 hidden-state 空间切成 expert 区域。 | expert utility 或语义 specialization。 |
| feature NMI | feature/proxy 标签和 expert assignment 的分区一致性。 | labels 与 top-1 expert ids 的 normalized mutual information。 | 判断 routing 是否把目标分区分开。 | 是否保持了原来的 feature-expert 匹配。 |
| matched preserve fraction | 原始 step-0 feature-expert 映射是否保留。 | 训练后仍落在初始 matched expert 区域的比例。 | 它能发现 NMI 隐藏的 expert swap 或 partial merge。 | expert 是否有用。 |
| route margin | 目标 expert 对最近竞争 expert 的 score gap。 | $m_f=\min_{e\ne a(f)}(w_{a(f)}-w_e)^\top\mu_f$。 | 它是 preservation 的核心几何条件。 | center 之外所有 token 都安全。 |
| cluster-aware margin | 扣除 cluster 内 token spread 后的 margin。 | center margin 减去 spread allowance。 | 判断整个 cluster 是否也在安全区域内。 | 没有 tail audit 时，不能保证每个尾部 token。 |
| common component | 对很多 token 共同起作用的 hidden-state 方向。 | mean、top-PC、route-logit direction 等 common/residual 审计对象。 | 它可能制造 load bias 或遮盖 residual feature geometry。 | 它是通用修复方法。 |
| margin budget | 训练中 margin 增减的分解。 | router drift、feature-center drift、interaction 三项。 | 用来定位 preservation 为什么成功或失败。 | 在真实审计前不能解释 real-DCLM failure。 |
| DCLM | 本线使用的真实语言数据训练表面。 | packed DCLM token stream 及其 router-input hidden states。 | 它是从受控 feature 走向真实 proxy routing 的桥。 | proxy cluster 有语义含义。 |
| MoE | Mixture of Experts，多专家模块。 | top-1 MoE 会把每个 routed token 发给一个 expert。 | 它是被研究的 expert specialization 机制。 | 被选中的 expert 真的学到有用功能。 |
| SAE / autoencoder | 用受限 code 重构 hidden state 的表征学习方法。 | sparse autoencoder 或 bottleneck autoencoder。 | 测试普通表征学习是否能发现 route-relevant states。 | 只靠重构目标不能证明 route relevance。 |
| raw center / residual center | 两种把 cluster center 变成 router rows 的方式。 | raw center 用原始 hidden-state mean；residual center 先减去估计 common component。 | A06_11 显示 raw center 对真实 raw-input routing 更有效。 | residual geometry 无用；它在 centered-input diagnostic 中可能有效。 |
| C0-C4 bridge cells | 受控数据中的不同难度条件。 | C0-C3 测 route-position discovery/preservation；C4 测 all-position clustering。 | 分离 feature strength、nuisance、错误 state population 的影响。 | real-DCLM 行为。 |
| rho | router row 离开 pseudo center 的扰动强度。 | A06_17_05 的 scalar sweep；rho 0 是 exact pseudo-center，rho 1 接近 random-direction scale。 | 测 exact center 是否必要，还是正 margin basin 更关键。 | real-DCLM 中的精确容忍范围。 |

## 1. 研究动机

A06 最开始的问题很宽：

```text
hidden-state geometry 能否支持无标签 feature/proxy 级 top-1 MoE router 初始化，
并且这种 routing 能否在训练中保持？
```

现在更有用的问题是：

```text
如果找到了 feature/proxy center，router 是否在它周围形成正决策 margin，
训练是否能让这个 margin 继续保持为正？
```

这个转变很重要。因为“能聚类出中心”不等于“能 route”；“step 0 能 route”
不等于“训练后能保持”；NMI 高也不等于原始 feature-to-expert 映射还在。
因此 A06 的主线已经变成 margin-budget 研究。

## 2. 必须区分的概念

| 容易混淆的概念 | 正确区分 |
|---|---|
| feature 和 proxy | feature 是合成数据真标签；proxy 是真实 DCLM 中稳定 cluster。 |
| discovery 和 preservation | discovery 问能否找到中心；preservation 问初始化出的 expert 区域训练后是否还在。 |
| route-position 和 all-position | router 只看 route-position；把所有位置混起来会混入不同角色的几何。 |
| NMI 和 matched preservation | NMI 看分区像不像；matched preservation 看原始映射是否还在。 |
| load balance 和 specialization | load 均衡不等于按 feature 分发。 |

## 3. 干净基线 / 无效结果

两个负结果定义了当前问题：

1. 真实 DCLM 中，raw proxy-center routing 在 step 0 很强，但很快被训练擦掉。
   A06_12 中 raw-center NMI 从 step 0 的 0.7549 降到 step 5 的 0.0410，
   step 10 的 0.0131。
2. 在受控桥接中，all-position clustering 不是可靠的 route-position clustering。
   A06_17 中 route-only feature NMI 是 1.000，而 all-position mean NMI 是 0.797。

这排除了一个过于简单的故事：只要找到 cluster 或 load 看起来均衡，就能形成 specialization。

## 4. 机制模型

对 feature/proxy $f$，设 $\mu_f(t)$ 是训练时刻 $t$ 的 route-position center，
$w_e(t)$ 是 router 第 $e$ 行。step 0 中 matched expert 为

$$
a(f)=\arg\max_e w_e(0)^\top \mu_f(0).
$$

对竞争 expert $e\ne a(f)$，定义 pairwise route margin：

$$
g_{f,e}(t)=(w_{a(f)}(t)-w_e(t))^\top\mu_f(t).
$$

center 被保持的条件是：

$$
\min_{e\ne a(f)} g_{f,e}(t)>0.
$$

margin 变化分解为：

$$
\Delta g_{f,e}
=\Delta w_{a,e}^\top\mu_f(0)
+w_{a,e}(0)^\top\Delta\mu_f
+\Delta w_{a,e}^\top\Delta\mu_f,
$$

其中 $w_{a,e}=w_{a(f)}-w_e$。

解释：

| 模型项 | 含义 | 测试的机制 |
|---|---|---|
| $\Delta w_{a,e}^\top\mu_f(0)$ | router 行向量相对旧 center 的移动。 | router drift 是否破坏旧分区。 |
| $w_{a,e}(0)^\top\Delta\mu_f$ | feature center 在旧 router 边界下的移动。 | representation drift 是否越过旧边界。 |
| $\Delta w_{a,e}^\top\Delta\mu_f$ | router 和 center 的共同移动。 | 训练反馈是否共同推动失败。 |

如果 $h=c+r$，score gap 还可以写成：

$$
(w_a-w_e)^\top h=(w_a-w_e)^\top c+(w_a-w_e)^\top r.
$$

这就是 common/residual 审计：看共同方向 $c$ 是否主导了 routing，或者 residual feature geometry $r$ 是否承担了 specialization。

## 5. 可证明命题

**命题 1：正 center margin 足以保持 center assignment。**

如果所有竞争 expert 都有 $g_{f,e}(t)>0$，则 top-1 router 会把 $\mu_f(t)$ 分给 $a(f)$。

证明：对每个竞争 expert $e$，

$$
w_{a(f)}(t)^\top\mu_f(t)-w_e(t)^\top\mu_f(t)=g_{f,e}(t)>0.
$$

所以目标 expert 得分最高。

**命题 2：正 cluster-aware margin 足以保持局部 token。**

如果 cluster 内 token 满足 $h=\mu_f+\epsilon$，且

$$
g_{f,e}(t)>\|(w_{a(f)}(t)-w_e(t))\|\cdot\|\epsilon\|
$$

则这些 token 仍留在目标 expert 区域。

证明：Cauchy-Schwarz 给出 $\epsilon$ 带来的最大 margin 损失上界；扣除后 score gap 仍为正。

**命题 3：margin-budget 分解是恒等式。**

第 4 节的分解是代数恒等式。A06_21 中实现误差最大为 $1.37\times10^{-6}$。

**指标命题：NMI 不能单独证明 preservation。**

NMI 可能在 expert permutation 或 partial merge 后仍然较高。因此 preservation 必须同时看 NMI、matched preserve fraction、margin sign 和 sign-flip rate。

## 6. 受控实验证据

受控桥接使用 one-layer Transformer + top-1 MoE，4 experts，无 learned absolute positional embedding，slot length 4，并在 feature slot 最后一个 token route。

| 实验 | 观察 | 解释 |
|---|---|---|
| A06_16 | C0-C3 step-0 pseudo NMI 和 final feature NMI 都是 1.000。 | 修正后的 route-position feature center 可以初始化并保持 routing。 |
| A06_17 | route-only 和 route-offset NMI 都是 1.000；all-position mean NMI 是 0.797。 | 正确聚类对象是 route-relevant states，不是所有 token。 |
| A06_17_02 | center-init final NMI 是 1.000，但 movement alignment 为负。 | preservation 不是 active router-center tracking。 |
| A06_17_03 | max boundary consumption mean 是 0.530；dynamic switch rate 是 0。 | 漂移只消耗了部分初始 margin buffer。 |
| A06_17_04 | forced row crossing 会破坏原始 feature-to-expert region。 | margin 是有效的几何边界尺子。 |
| A06_17_05 | rho 0.7 仍保持；rho 1.0 margin 为负且 preserve 差。 | exact center 不必要，正 margin basin 必要。 |
| A06_21 | pseudo/oracle center-init 保持 NMI 1.000、preserve 1.000、正 margin、zero sign flip；random/shuffled guard 不满足。 | controlled preservation 的机制是正 current margin 和 cluster-aware margin。 |

受控结论：

```text
在修正后的桥接实验中，只要初始化 router 在 route-relevant feature center 周围
产生正 margin buffer，feature-to-expert specialization 就能保持。
```

## 7. 真实 DCLM 证据 / 负结果

真实 DCLM 实验回答的是另一个问题：同样的 proxy 思路能否在普通下一词训练中保持。

| 实验 | 观察 | 解释 |
|---|---|---|
| A06_10 | step-10 residual proxy stability NMI 0.5211；layer-5 stability 0.6501；frequency/position NMI 更低。 | real-DCLM hidden states 中存在稳定 proxy cluster。 |
| A06_11 | step-10 raw-center equal-norm routing 的 proxy-route NMI 0.8811，random 0.0417。 | proxy center 在 step 0 线性可 route。 |
| A06_12 | raw-center NMI 从 0.7549 降到 step 5 的 0.0410 和 step 10 的 0.0131；loss 与其他条件接近。 | 普通 DCLM 训练会擦掉 proxy routing，且不像是简单训练崩溃。 |

真实数据结论：

```text
real-DCLM 的瓶颈不是 proxy geometry 是否存在，也不是 step-0 linear router bridge。
瓶颈是 early training preservation。
```

## 8. 对齐解释和 refined theory

受控结果和真实结果不冲突，它们回答的是同一机制的不同部分。

| 表面冲突 | 对齐解释 |
|---|---|
| controlled center-init 能保持，real-DCLM center-init 会 collapse。 | controlled 说明正 margin 下可以保持；real-DCLM 尚未审计这个 margin 是否存在或被吃掉。 |
| clustering 能找到 center，但 all-position clustering 失败。 | route-position clustering 和 all-position clustering 是不同 operationalization；后者混入了不同角色状态。 |
| 好初始化重要，但 router 不追踪 center。 | 初始化重要是因为它产生 margin buffer，不是因为它保证未来共同移动。 |
| common subtraction 有时有帮助，但 route-logit common estimator 失败。 | common/residual 是诊断框架；当前 estimator 没有隔离 route-relevant residual feature structure。 |

refined working theory：

```text
feature/proxy specialization 是 router-input hidden-state 空间中的
margin-preservation 问题。center discovery 只有在产生正 cluster-aware margin，
并且训练不迅速吃掉这个 margin 时，才真正有用。
```

## 9. 下一步实验

下一步决策：

```text
把 A06_21 的 margin-budget audit 搬到 A06_12 风格的 real-DCLM proxy-init training 上。
```

最小设计：

1. 复用 A06_12 的 real-DCLM proxy-init 设置。
2. 在 step 0、1、2、3、5、10 保存 router rows、route-input hidden states、proxy centers、proxy labels、expert assignments。
3. 计算 proxy-route NMI、matched preserve fraction、current margin、cluster-aware margin、sign-flip rate、common/residual margin terms、max load、language-model loss。

判定表：

| 结果 | 机制更新 | 下一步 |
|---|---|---|
| step-0 margin 已经弱或为负 | real proxy-center initialization 几何上不够安全。 | 改 proxy selection 或 center normalization。 |
| step-0 margin 为正但 step 5 前消失 | real failure 是 margin-budget collapse。 | 分解 router drift、center drift、common overwrite、token spread、interaction。 |
| common term 主导 margin loss | failure 是 common-direction overwrite。 | 测 common-invariant 或 common-guarded routing。 |
| feature-center drift 主导 | 表征移动越过旧 router 边界。 | 研究 representation-router co-movement 和 early stabilization。 |
| margin 仍为正但 NMI collapse | center-level audit 不够。 | 转向 token-level tail-risk 和 cluster-aware diagnostics。 |
| rerun 中 preservation 成功 | A06_12 和 rerun 不一致。 | 先 reconcile implementation/snapshot 差异，再做 utility。 |

## 10. Source Map 和审计表

### 10.1 实验逻辑链

| 步骤 | 问题 | 结果 | 更新了什么 |
|---|---|---|---|
| A06_03-A06_05 | common 和 residual geometry 是否影响 routing？ | common 能主导 load；centering 后仍有 residual geometry。 | load imbalance 不等于 specialization。 |
| A06_06-A06_09 | synthetic feature routing 是否可达、可保持？ | oracle 和 route-position label-free discovery 可初始化 routing。 | 受控数据里几何上可达。 |
| A06_10-A06_12 | real-DCLM proxy 能否 route 并保持？ | proxy 存在且 step 0 可 route，但 step 5/10 被训练擦掉。 | 真实瓶颈是 preservation。 |
| A06_16-A06_17 | 旧 controlled failure 来自哪里？ | no-position route-position discovery 通过；all-position 不可靠。 | state population 很关键。 |
| A06_17_02-A06_17_05 | controlled center-init 为什么保持？ | 正 margin，而不是 active tracking 或 exact center equality。 | preservation 是 margin-basin 现象。 |
| A06_18-A06_20 | minimal-prior selector / common estimator 能否从 all-position 恢复 center？ | 当前方法没有解决。 | route relevance 仍未被 minimal prior 解决。 |
| A06_21 | 哪个指标解释 controlled preservation？ | current 和 cluster-aware margins 保持为正；sign flip 为 0。 | margin-budget audit 是 real-DCLM 下一步诊断。 |

### 10.2 关键结果

| 实验 | 关键证据 | 判断 |
|---|---|---|
| [A06_10](../../../experiments/A06/A06_10_real_dclm_proxy_feature_operationalization/summary.md) | step-10 residual stability NMI 0.5211；layer-5 stability 0.6501。 | real-DCLM proxy 存在，但非语义边界。 |
| [A06_11](../../../experiments/A06/A06_11_real_dclm_proxy_center_router_initialization/summary.md) | step-10 raw-center equal-norm proxy-route NMI 0.8811，random 0.0417。 | proxy center 在 step 0 可线性 route。 |
| [A06_12](../../../experiments/A06/A06_12_real_dclm_proxy_init_training_preservation/summary.md) | raw-center NMI 0.7549 -> step5 0.0410 -> step10 0.0131。 | 普通 DCLM 训练擦除 proxy routing。 |
| [A06_16](../../../experiments/A06/A06_16_synthetic_to_realistic_proxy_bridge/summary.md) | C0-C3 step-0 pseudo NMI 和 final feature NMI 都是 1.000。 | corrected no-position route-position bridge 通过。 |
| [A06_17](../../../experiments/A06/A06_17_all_position_route_relevant_feature_discovery/summary.md) | route-only NMI 1.000；all-position mean NMI 0.797。 | 必须选择 route-relevant states。 |
| [A06_17_02](../../../experiments/A06/A06_17_02_router_center_tracking_preservation/summary.md) | center-init final NMI 1.000；movement alignment 约 -0.4。 | active tracking 不是机制。 |
| [A06_17_03](../../../experiments/A06/A06_17_03_feature_drift_margin_boundary/summary.md) | pseudo max boundary consumption mean 0.530；switch rate 0。 | drift 在 margin buffer 内。 |
| [A06_17_04](../../../experiments/A06/A06_17_04_margin_crossing_causal_stress/summary.md) | forced crossing 后 margin 为负、preserve collapse。 | margin 是有效几何边界尺子。 |
| [A06_17_05](../../../experiments/A06/A06_17_05_margin_basin_robust_initialization/summary.md) | rho 0.7 保持；rho 1.0 margin 为负、preserve 0.219。 | 关键是正 margin basin。 |
| [A06_18](../../../experiments/A06/A06_18_label_free_route_relevant_state_selector/summary.md) | route-only 1.000；PCA q=4 为 0.871；SAE L1 8x 为 0.729。 | 普通表征学习没有定义 route relevance。 |
| [A06_19](../../../experiments/A06/A06_19_minimal_prior_margin_aware_center_search/summary.md) | raw all-token 0.863；M1 0.843；M2 continuous 0.784。 | 当前 minimal-prior margin signals 不够。 |
| [A06_20](../../../experiments/A06/A06_20_route_logit_common_estimator_random_init_feature_recovery/summary.md) | route-logit subtraction 0.815，raw all-position 0.829。 | 当前 route-logit common estimator 不是解法。 |
| [A06_21](../../../experiments/A06/A06_21_margin_budget_preservation_audit/summary.md) | step-10 pseudo/oracle NMI 1.000、preserve 1.000、正 margin、zero sign flip。 | margin budget 解释 controlled preservation。 |

### 10.3 已证明 / 假设 / 经验命题

| 类型 | 陈述 | 状态 |
|---|---|---|
| 模型可证明 | 正 center margin 保持 center assignment。 | 数学命题。 |
| 模型可证明 | 正 cluster-aware margin 在 spread bound 内保持局部 token。 | 数学命题。 |
| 代数恒等式 | margin-budget decomposition 精确成立。 | A06_21 实现已校验。 |
| 经验结论 | controlled bridge 中 center-init 保持，因为 margin 为正。 | A06_17_02-A06_21 支持。 |
| 经验结论 | real-DCLM proxy cluster 存在且 step 0 可 route。 | A06_10-A06_11 支持。 |
| 经验负结果 | 普通 real-DCLM 训练擦除 proxy routing。 | A06_12 支持。 |
| 假设 | real-DCLM proxy cluster 是有用 specialization target。 | operational assumption，不是语义证明。 |
| 开放经验命题 | real-DCLM failure 是 margin-budget collapse。 | 下一步实验判定。 |

## 11. Claim Boundary

可以说：

- route-position feature/proxy geometry 可以支持 top-1 router specialization；
- raw proxy center 可以在 step 0 初始化 strong real-DCLM proxy router；
- 普通 real-DCLM 下一词训练会快速擦掉该 proxy routing；
- controlled no-position preservation 由正 current margin 和 cluster-aware route margin 解释；
- initialization 在正 margin basin 内时，不需要 exact center equality；
- all-position hidden-state clustering 不能替代 route-relevant state selection。

不能说：

- real-DCLM proxy cluster 是语义 feature；
- 高 route NMI 意味着 expert utility；
- load balance 意味着 specialization；
- common subtraction 是通用修复；
- SAE 或普通 representation learning 永远能或永远不能解决 route relevance；
- real-DCLM preservation 不可能；
- real-DCLM failure 已经被 controlled margin model 完全解释。

## Appendix. 数据 / 模型 / 参数 / 脚本

| 实验 | 数据 / 模型 / 参数 | seeds / checkpoints | 脚本 / config / result path | 主指标 |
|---|---|---|---|---|
| A06_10 | DCLM stream；Qwen-style top-1 MoE；6 layers，hidden 512，8 experts。 | seeds 0-2；checkpoints 0/10。 | `scripts/run_real_dclm_proxy_feature_operationalization.py`；result `runs/real_dclm_proxy_feature_operationalization/.../proxy_cluster_summary.csv`；[summary](../../../experiments/A06/A06_10_real_dclm_proxy_feature_operationalization/summary.md)，[detailed](../../../experiments/A06/A06_10_real_dclm_proxy_feature_operationalization/detailed.md)。 | held-out proxy assignment stability NMI |
| A06_11 | 同 A06_10 hidden states；raw/residual proxy centers 初始化 router rows。 | seeds 0-2；source steps 0/10。 | `scripts/run_real_dclm_proxy_center_router_initialization.py`；result `runs/real_dclm_proxy_center_router_initialization/.../router_initialization_summary.csv`；[summary](../../../experiments/A06/A06_11_real_dclm_proxy_center_router_initialization/summary.md)，[detailed](../../../experiments/A06/A06_11_real_dclm_proxy_center_router_initialization/detailed.md)。 | proxy-route NMI |
| A06_12 | real-DCLM next-token training；random/equal-norm/raw-center/residual-center。 | seeds 0-2；steps 0/1/2/3/5/10/20/50。 | `scripts/run_real_dclm_proxy_init_training_preservation.py`；result `runs/real_dclm_proxy_init_training_preservation/.../training_preservation_summary.csv`；[summary](../../../experiments/A06/A06_12_real_dclm_proxy_init_training_preservation/summary.md)，[detailed](../../../experiments/A06/A06_12_real_dclm_proxy_init_training_preservation/detailed.md)。 | proxy-route NMI over training |
| A06_16 | one-layer Transformer + top-1 MoE；4 experts；no learned absolute positional embedding；slot length 4；route on last slot token。 | C0-C4；8 seeds where applicable。 | `scripts/run_a06_16_synthetic_to_realistic_proxy_bridge.py`；config `configs/a06_16_synthetic_to_realistic_proxy_bridge_no_pos_full.json`；result `results/a06_16_synthetic_to_realistic_proxy_bridge/a06_16_proxy_bridge_no_pos_same_model_audit_full_20260623_1`；[summary](../../../experiments/A06/A06_16_synthetic_to_realistic_proxy_bridge/summary.md)，[detailed](../../../experiments/A06/A06_16_synthetic_to_realistic_proxy_bridge/detailed.md)。 | first failed stage / feature NMI |
| A06_17 | 同 controlled bridge；fit pools 包括 route-only、slot offset、all-position 等。 | 8 seeds。 | `scripts/run_a06_17_all_position_route_relevant_feature_discovery.py`；config `configs/a06_17_all_position_route_relevant_feature_discovery.json`；result `results/a06_17_all_position_route_relevant_feature_discovery/a06_17_route_relevant_pool_audit_full_20260623_1`；[summary](../../../experiments/A06/A06_17_all_position_route_relevant_feature_discovery/summary.md)，[detailed](../../../experiments/A06/A06_17_all_position_route_relevant_feature_discovery/detailed.md)。 | held-out route-position feature NMI |
| A06_17_02 | pseudo-center、oracle-center、random、equal-norm random、label-shuffled center。 | 8 seeds；snapshots to 1600 steps。 | `scripts/run_a06_17_02_router_center_tracking_preservation.py`；config `configs/a06_17_02_router_center_tracking_preservation.json`；result `results/a06_17_02_router_center_tracking_preservation/a06_17_02_router_center_tracking_full_20260626_024804`；[summary](../../../experiments/A06/A06_17_02_router_center_tracking_preservation/summary.md)，[detailed](../../../experiments/A06/A06_17_02_router_center_tracking_preservation/detailed.md)。 | movement alignment、feature NMI、route margin |
| A06_17_03 | boundary-consumption audit。 | 8 seeds；snapshots to 1600 steps。 | `scripts/run_a06_17_03_feature_drift_margin_boundary.py`；config `configs/a06_17_02_router_center_tracking_preservation.json`；[summary](../../../experiments/A06/A06_17_03_feature_drift_margin_boundary/summary.md)，[detailed](../../../experiments/A06/A06_17_03_feature_drift_margin_boundary/detailed.md)。 | boundary consumption / dynamic margin |
| A06_17_04 | margin stress 和 forced row crossing。 | C0-C3，4 seeds。 | `scripts/run_a06_17_04_margin_crossing_causal_stress.py`；config `configs/a06_17_04_margin_crossing_causal_stress.json`；result `results/a06_17_04_margin_crossing_causal_stress/a06_17_04_margin_crossing_full_20260629_1`；[summary](../../../experiments/A06/A06_17_04_margin_crossing_causal_stress/summary.md)，[detailed](../../../experiments/A06/A06_17_04_margin_crossing_causal_stress/detailed.md)。 | static crossing ratio / preserve fraction |
| A06_17_05 | pseudo-center row perturbation。 | C0-C3，4 seeds，rho sweep。 | `scripts/run_a06_17_05_margin_basin_robust_initialization.py`；result `results/a06_17_05_margin_basin_robust_initialization/a06_17_05_margin_basin_full_20260629_1`；[summary](../../../experiments/A06/A06_17_05_margin_basin_robust_initialization/summary.md)，[detailed](../../../experiments/A06/A06_17_05_margin_basin_robust_initialization/detailed.md)。 | final matched preserve fraction |
| A06_18 | PCA、bottleneck AE、SAE、split-stability selectors。 | 8 seeds。 | `scripts/run_a06_18_label_free_route_relevant_state_selector.py`；config `configs/a06_18_label_free_route_relevant_state_selector.json`；run `a06_18_revision_full_local_2gpu_20260625`；[summary](../../../experiments/A06/A06_18_label_free_route_relevant_state_selector/summary.md)，[detailed](../../../experiments/A06/A06_18_label_free_route_relevant_state_selector/detailed.md)。 | held-out route-position feature NMI |
| A06_19 | all-position minimal-prior M1/M2 center search。 | 8 seeds。 | `scripts/run_a06_19_minimal_prior_margin_aware_center_search.py`；config `configs/a06_19_minimal_prior_margin_aware_center_search_full.json`；result `results/a06_19_minimal_prior_margin_aware_center_search/full_m1_m2_8seed_20260626`；[summary](../../../experiments/A06/A06_19_minimal_prior_margin_aware_center_search/summary.md)，[detailed](../../../experiments/A06/A06_19_minimal_prior_margin_aware_center_search/detailed.md)。 | held-out route-position feature NMI |
| A06_20 | equal-norm random router training + common-direction estimators。 | 8 seeds；steps 0/5/10/100/1600。 | `scripts/run_a06_20_route_logit_common_estimator_random_init_feature_recovery.py`；config `configs/a06_20_route_logit_common_estimator_random_init_feature_recovery.json`；run `a06_20_route_logit_common_estimator_full_20260629_010533`；[summary](../../../experiments/A06/A06_20_route_logit_common_estimator_random_init_feature_recovery/summary.md)，[detailed](../../../experiments/A06/A06_20_route_logit_common_estimator_random_init_feature_recovery/detailed.md)。 | delta feature NMI / delta margin |
| A06_21 | controlled margin-budget audit。 | 8 seeds x C0-C3 x 5 conditions x 12 snapshots。 | `scripts/run_a06_21_margin_budget_preservation_audit.py`；config `configs/a06_21_margin_budget_preservation_audit.json`；result `results/a06_21_margin_budget_preservation_audit/a06_21_margin_budget_full_20260629_1`；[summary](../../../experiments/A06/A06_21_margin_budget_preservation_audit/summary.md)，[detailed](../../../experiments/A06/A06_21_margin_budget_preservation_audit/detailed.md)。 | NMI、preserve、margin、sign flip、cluster-aware margin |
