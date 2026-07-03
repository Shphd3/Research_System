# 07 线重构：从路由分区到功能价值的 common/rare 干扰模型

## 摘要

07 线的核心问题不是“MoE 能不能把 token 分开”，也不是“负载是否均匀”。它问的是更晚一层的问题：

```text
如果 06 已经给出了一个能保持的 partition，这个 partition 是否真的有功能价值？
```

这里的“功能价值”必须比 route label alignment 更强。一个 partition 只有满足以下链条，才可以被称为有价值：

```text
分区被保持
-> common/rare 或 nested features 在共享 expert 中存在可测干扰
-> 路由或更新控制降低这个干扰
-> rare/tail loss 改善且 common loss 不显著退化
-> fixed-route ablation 显示被选 expert 对对应 feature 有因果作用
```

因此 07 是 06 之后的价值判据线。它不能替代 06 preservation。如果真实 DCLM proxy route 在 step 5/10 已经消失，那么 utility 实验会混淆两个问题：

```text
partition 没有价值
vs
partition 已经不存在
```

07 现在应该被重构成两层：

1. **审计工具层。** 旧 D07 结果证明 controlled surface 可以读出 rare interference reduction 和 route-function binding。
2. **机制模型层。** 新 nested 结果把导师的高增益公共骨架理论转成 update-space common-subspace control：先证明公共骨架形成，再证明抑制 tail update 的 common-subspace 成分可以改善 tail loss。

当前最稳结论是：

$$
\boxed{
\text{07 已经有 controlled value diagnostics，但真实 MoE utility 必须等待 06 的 preserved partition。}
}
$$

## 1. 术语解释

| 术语 | 中文含义 | 具体对象或计算 | 为什么重要 | 不能证明什么 |
|---|---|---|---|---|
| 分区（partition） | router 把样本分配到不同 expert 后形成的 group-to-expert 结构。 | $q_{f,e}=P(E=e\mid F=f)$。 | 是 specialization 的结构前提。 | 分区本身不能证明 expert 有用。 |
| 保持（preservation） | 初始分区在训练后仍然存在。 | `proxy_route_NMI@step5/10`、matched preserve、margin sign flip。 | 没有保持，就无法解释 utility 失败。 | 保持不能证明 rare loss 改善。 |
| 常见特征（common feature） | 高频、共享、容易主导更新的结构。 | 在 D07 中是 common group；在 nested 中是 parent feature $A$ 或 common projector $P_C$。 | 它可能造成 rare learning 被覆盖。 | common 不等于有害；也不等于 top hidden-PC。 |
| 稀有特征（rare / tail feature） | 低频、具体、需要与 common 区分的结构。 | D07 中的 rare group；nested 中的 child level $ABCD$。 | 它是价值判断的主要受害对象。 | rare 不自动等于 attention context 或语义复杂性。 |
| 路由重叠（expert overlap） | common 和 rare 被送到同一 expert 的程度。 | $O_{C,R}=\sum_e q_{C,e}q_{R,e}$。 | 只有共享 expert 时，梯度干扰才可能发生。 | 高 overlap 不一定有害。 |
| 梯度冲突（gradient conflict） | 两类样本在同一 expert 上的更新方向相反。 | $[-\cos(g_{C,e},g_{R,e})]_+$。 | 它是 common update 伤害 rare loss 的机制条件。 | 冲突下降不保证 rare loss 改善。 |
| 路由加权冲突（routing-weighted conflict） | 同时考虑 expert overlap 和负梯度相似度的干扰指标。 | $\mathcal{C}_{C,R}=\sum_e q_{C,e}q_{R,e}[-\cos(g_{C,e},g_{R,e})]_+$。 | 它是 07 的核心中介指标。 | 不能单独证明 expert utility。 |
| 稀有损失（rare loss） | rare/tail 样本上的预测损失。 | $L_R$ 或 $L_{\mathrm{tail}}$。 | 它是 value 的必要 guard。 | rare loss 改善可能来自正则化、欠训练或 dense effect。 |
| 固定路由消融（fixed-route ablation） | 固定 route 不变，只移除某个 expert 的计算。 | 比较 routed expert ablation 与 non-routed expert ablation。 | 分离 expert function 和 rerouting effect。 | 需要 preserved route；否则对象不稳定。 |
| 路由-功能绑定（route-function binding） | 被路由选中的 expert 对对应 feature 有因果效用。 | route-conditioned utility、ablation selectivity。 | 它是 functional specialization 的关键读数。 | 不证明语义专家或泛化能力。 |
| 公共子空间更新比例（tail update fraction in $P_C$） | tail 更新有多少进入公共子空间。 | $\alpha_{\mathrm{tail}}=\|P_Cu_{\mathrm{tail}}\|^2/(\|u_{\mathrm{tail}}\|^2+\epsilon)$。 | 它连接导师 nested 理论和 07 干扰机制。 | 需要稳定 $P_C$，且不等于 route utility。 |

## 2. 07 必须解决的概念混淆

### 2.1 均匀负载不是价值

均匀负载只说明 expert 被使用得均匀：

$$
\max_e P(E=e)\approx \frac{1}{E}.
$$

但它不说明 common 和 rare 是否被功能性分开，也不说明 selected expert 是否有对应计算。

### 2.2 高 route NMI 不是价值

高 route NMI 说明 route label 和 audit label 对齐：

$$
NMI(route;feature)\approx 1.
$$

但如果 expert 内部函数相同，或者 route alignment 只是固定初始化的标签排列，那么它仍然没有 utility。

### 2.3 rare loss 改善不是机制

rare loss 改善是必要证据，但不是机制解释。它可能来自：

- common examples 被少训练；
- update norm 被缩小；
- router 更均匀；
- dense/shared baseline 过强或过弱；
- projector 引入了额外正则化；
- 真正的 common/rare conflict reduction。

所以 07 必须要求机制 guard：梯度冲突下降、update-space projection 改变、或 fixed-route ablation selectivity。

## 3. 第一层数学模型：common/rare 梯度干扰

令 $C$ 是常见特征，$R$ 是稀有特征，频率满足：

$$
\pi_C\gg \pi_R.
$$

令 $q_{f,e}=P(E=e\mid F=f)$ 表示 feature $f$ 被送到 expert $e$ 的概率。令 $g_{f,e}$ 是 feature $f$ 在 expert $e$ 上的平均梯度。

expert $e$ 的一步更新近似为：

$$
\Delta\theta_e=-\eta(\pi_C q_{C,e}g_{C,e}+\pi_R q_{R,e}g_{R,e}).
$$

rare loss 的一阶变化中，由 common update 造成的项为：

$$
\Delta L_R^{C\rightarrow R}
\approx
-\eta\pi_C\sum_e q_{R,e}q_{C,e}\langle g_{R,e},g_{C,e}\rangle.
$$

如果某些共享 expert 上：

$$
\langle g_{R,e},g_{C,e}\rangle<0,
$$

那么 common update 会增加 rare loss。由此定义路由加权负冲突：

$$
\mathcal{C}_{C,R}
=\sum_e q_{C,e}q_{R,e}[-\cos(g_{C,e},g_{R,e})]_+.
$$

### 命题 1：只有 overlap 和负梯度同时存在时，expert sharing 才是 harmful

**命题。** 若对所有 expert 都有 $q_{C,e}q_{R,e}=0$，或对所有共享 expert 都有 $\langle g_{C,e},g_{R,e}\rangle\ge 0$，则 common update 不会通过一阶项增加 rare loss。

**证明。** rare loss 的 common-induced 一阶项为：

$$
\Delta L_R^{C\rightarrow R}
\approx
-\eta\pi_C\sum_e q_{R,e}q_{C,e}\langle g_{R,e},g_{C,e}\rangle.
$$

若 $q_{C,e}q_{R,e}=0$，对应项为 0。若 $\langle g_{R,e},g_{C,e}\rangle\ge 0$，对应项非正，即不会增加 rare loss。因此 harmful sharing 需要 overlap 和负梯度同时存在。

**意义。** 这解释了为什么 07 不能只看 expert overlap，也不能只看梯度 cosine；必须看 routing-weighted conflict。

## 4. 第二层数学模型：route-function binding

即使 routing 降低了 common/rare conflict，也还需要问：被选中的 expert 是否真的承担了对应 feature 的计算？

令 nested level 或 feature group 为 $\ell$。令 forced expert loss 为：

$$
CE_{\ell,e}.
$$

route-conditioned loss：

$$
CE_{\ell,\mathrm{route}}=\sum_e P(e\mid \ell)CE_{\ell,e}.
$$

uniform expert loss：

$$
CE_{\ell,\mathrm{uniform}}=\frac{1}{E}\sum_e CE_{\ell,e}.
$$

route utility advantage：

$$
U_\ell=CE_{\ell,\mathrm{uniform}}-CE_{\ell,\mathrm{route}}.
$$

固定路由消融选择性：

$$
A_\ell
=CE_{\ell}^{-\mathrm{routed}}
-\frac{1}{E-1}\sum_{e\ne \mathrm{routed}}CE_{\ell}^{-e}.
$$

这里 $A_\ell>0$ 表示移除 routed expert 比移除非 routed experts 更伤害该 level。

### 命题 2：route alignment 和 route-function binding 是不同性质

**命题。** 可以存在完美 route alignment 但没有 route-function binding。

**构造。** 令 $P(e\mid \ell)$ 对每个 $\ell$ 都是单一 expert，即 route alignment 完美。但令：

$$
CE_{\ell,1}=CE_{\ell,2}=\cdots=CE_{\ell,E}.
$$

则：

$$
CE_{\ell,\mathrm{route}}=CE_{\ell,\mathrm{uniform}},
$$

所以 $U_\ell=0$。同时消融任何 expert 造成相同损失变化，因此 $A_\ell=0$。故 route alignment 不推出 function binding。

**意义。** 这就是 A07_03 采用 forced-routing utility 和 fixed-route ablation 的原因。

## 5. 第三层数学模型：nested common backbone 和 update-space 控制

导师的 nested 理论给 07 一个更深的机制对象：频繁 parent feature 先形成高增益公共骨架，后续 child/tail feature 会被这个骨架吸引。

令模型矩阵为：

$$
W(t)=\sum_i\sigma_i(t)u_i(t)v_i(t)^\top.
$$

令公共子空间投影为：

$$
P_C(t)=V_C(t)V_C(t)^\top.
$$

公共子空间漂移：

$$
\delta_C(t)=\|P_C(t)-P_C(T_0)\|_2.
$$

公共能量：

$$
S_C(t)=\sum_{i\in C}\sigma_i(t)^2.
$$

two-phase common backbone signature 是：

```text
P_C 在 common warmup 后稳定，
但 S_C 仍继续增长。
```

若 tail 更新方向为 $u_{\mathrm{tail}}(t)$，tail update 落入 common subspace 的比例是：

$$
\alpha_{\mathrm{tail}}(t)
=\frac{\|P_Cu_{\mathrm{tail}}(t)\|^2}{\|u_{\mathrm{tail}}(t)\|^2+\epsilon}.
$$

update-space 抑制定义为：

$$
\tilde u_t=(I-\rho P_C)u_t.
$$

因为 $P_C$ 是正交投影：

$$
(I-\rho P_C)u_t=(1-\rho)P_Cu_t+(I-P_C)u_t.
$$

所以 common-subspace 更新能量相对于互补成分被乘以 $(1-\rho)^2$。这说明 intervention 的对象不是 hidden norm，而是真实 update direction。

## 6. 旧 D07 证据：审计工具层成立

旧 D07 链条回答的是：

```text
如果 controlled common/rare surface 确实有 conflict，审计工具能不能读出 partition value？
```

### 6.1 A07_01：metric surface 合法

核心数字：

```text
Delta_vs_best_null = 0.8601 +/- 0.0008
oracle rare loss = 0.5798
dense rare loss = 1.4399
load-only rare loss = 1.5300
shortcut guard passed
```

读法：controlled D07 surface 中，oracle routing 可以显著缓解 rare loss，且不是 shortcut。它证明 surface 可以测 value，但不证明任何 learned method。

### 6.2 A07_02：common-control 方法效应

核心数字：

```text
RIR_cc = 0.9502 +/- 0.0006
load-only max load = 0.2500
common-control max load = 0.2500
active experts = 4.0000
```

读法：在 matched load 下，common-control 可以降低 rare interference。它支持 controlled synthetic method effect，但不能外推真实语料。

### 6.3 A07_03：route-function binding 正例

核心数字：

```text
selected-best rate = 1.0000
route-conditioned utility advantage ~= 0.950
modal ablation delta = 0.6800
nonmodal ablation delta = 0.0000
```

读法：forced-routing utility 和 fixed-route ablation 可以读出专家功能绑定。它支持 diagnostic，但不证明真实 learned MoE 已经有 utility。

## 7. 神经 proxy 证据：真实一点的 utility 仍不闭合

### 7.1 A07_04：common/rare gradient conflict 可测，但不足以支持 specialization

核心数字：

| Condition | Weighted conflict | Rare loss | Rare acc |
|---|---:|---:|---:|
| dense shared | 0.9982 | 1.7321 | 0.1301 |
| random top-1 MoE | 0.2641 | 1.8827 | 0.1449 |
| centered unsup split | 0.2370 | 1.8195 | 0.1373 |
| oracle split | 0.0000 | 0.0004 | 1.0000 |

centered split 相比 random：

```text
Delta C_CR = 0.0271 +/- 0.0398
rare loss improvement = 0.0632 +/- 0.0617
```

判断：方向略对，但小且 noisy；dense shared rare loss 更低，所以不能 claim MoE functional value。

### 7.2 A07_05：common-update harm 存在但太小

核心数字：

```text
common_to_rare_loss_effect = 0.00168
threshold = 0.005
rare_common_update_fraction = 0.22076
projector_stability = 0.85250
```

判断：rare update 和 common subspace 有 overlap，common update 对 rare 有方向性伤害，但强度不足以成为主线机制。

### 7.3 A07_06：rare loss 改善但机制未闭合

核心数字：

```text
full method Delta C vs random = 0.0036
rare-loss improvement vs random = 0.2848
rare-loss improvement vs centered = 0.2155
rare-loss margin vs dense = -0.1538
raw projector stability = 0.3309
AdamW-like projector stability = 0.7327
```

判断：方法对 rare loss 有正效果，但 route-level conflict 几乎没动，raw projector stability 失败。因此不能说 intended conflict mechanism 解释了 rare-loss gain。

这组证据给 07 一个重要边界：

```text
rare loss gain without mechanism guard is not enough.
conflict metric improvement without dense/utility guard is not enough.
```

## 8. 新 nested 证据：机制模型层更干净

### 8.1 A07_01 nested：公共骨架形成

核心数字：

```text
stable-late-gain pass rate = 1.0000
post-warmup max drift delta_C = 0.1373
late common energy gain = 1.5115
final A accuracy = 1.0000
final ABCD accuracy = 0.8768
balanced-frequency guard pass rate = 0.3750
```

判断：controlled rank-one nested surface 复现了导师的 common-backbone / late-gain geometry。

### 8.2 A07_02 nested：update-space common control 改善 tail

核心数字：

| Condition | Tail loss | Tail acc | A loss | $\alpha_{\mathrm{tail}}$ |
|---|---:|---:|---:|---:|
| CE/AdamW | 0.3947 | 0.8806 | 0.0325 | 0.1387 |
| confidence gate only | 0.3242 | 0.8829 | 0.0600 | 0.1558 |
| subspace suppression only | 0.3196 | 0.8896 | 0.0325 | 0.0234 |
| combined control | 0.2872 | 0.8933 | 0.0590 | 0.0183 |

关键结论：

```text
combined control tail loss improvement = 0.1075
alpha_tail reduction = 0.1204
common loss regression = 0.0265 < 0.05 guard
```

判断：在 controlled rank-one nested surface 上，common-subspace update control 既改善 tail loss，也降低 tail update concentration。

### 8.3 A07_03 nested：route-function diagnostic 正例

核心数字：

| Condition | Ablation selectivity | Route utility | Selected-best rate |
|---|---:|---:|---:|
| oracle nested route | 0.5699 | 0.1746 | 0.7500 |
| random load-matched route | 0.0107 | -0.0024 | 0.2188 |

判断：diagnostic 可以读出 route-function binding，但这是 oracle positive control，不是 learned real-DCLM utility。

## 9. 07 与 06 的正确连接

06 的问题是：

```text
route/proxy partition 是否能穿过 early training 保持？
```

07 的问题是：

```text
被保持的 partition 是否减少干扰并产生 expert utility？
```

二者顺序不能反过来。

如果 06 失败，07 的 utility test 会失去对象。此时 rare loss 变差可能是因为 partition 消失，而不是 partition 没有价值。反过来，如果 06 成功但 07 失败，才可以说“结构被保持但未产生功能价值”。

因此，07 在主线中的位置是：

```text
06 preservation pass
-> 07 conflict / tail-loss audit
-> 07 fixed-route utility audit
-> stronger specialization claim
```

## 10. 07 与当前 common/rare routing audit 的连接

当前主线正在考虑：

$$
h\quad\text{vs}\quad (I-P_C)h
$$

对 rare/proxy margin、sign flip、LM loss 的影响。

这属于 06/07 之间的桥：

- 如果 primary metric 是 rare/proxy margin 和 preservation，它仍是 06-level audit。
- 如果进一步测 $\mathcal{C}_{C,R}$、$L_R$、fixed-route ablation，它才进入 07-level utility。

因此当前不能把 attention context 直接叫 rare feature，也不能把 common-subtracted routing 直接叫 utility method。正确表述是：

```text
先检验 common-subtracted routing 是否保护待保持分区；
再检验被保护的分区是否减少 common/rare gradient conflict 或 tail loss；
最后检验 routed expert 是否有 causal utility。
```

## 11. 重构后的 07 当前决策问题

07 当前最小 decision question 应该是：

> 给定一个已经在 06 中保持的 route/proxy partition，它是否通过降低 overlap-weighted negative gradient conflict 来改善 rare/tail loss，并且在 fixed-route ablation 中显示 route-function binding？

形式化成功条件：

1. Preservation gate 通过：

$$
NMI_{t} \text{ 或 matched preserve 足够高，sign flip 足够低。}
$$

2. Conflict gate 通过：

$$
\Delta\mathcal{C}_{C,R}>0.
$$

3. Rare-loss guard 通过：

$$
L_R(\mathrm{candidate})<L_R(\mathrm{baseline})
$$

且 common loss 不显著退化。

4. Utility gate 通过：

$$
A_\ell>0,\qquad U_\ell>0.
$$

如果只通过 1，不是 utility。只通过 2，不是 value。只通过 3，不是 mechanism。只通过 4 但没有 1，也不是真实主线 utility。

## 12. 可以成立和不能成立的逻辑

### 可以成立

```text
Controlled D07 证明了 value-audit surface 和 route-function diagnostic 是可用工具。
```

理由：A07_01/A07_02/A07_03 形成 metric surface -> rare interference reduction -> route-function binding 的 controlled chain。

```text
Nested rank-one surface 证明导师 common-backbone 机制可以被本项目操作化。
```

理由：A07_01 nested 通过 stable-late-gain signature，A07_02 nested 通过 tail-loss 和 alpha_tail 双指标。

```text
07 必须等待 06 preservation。
```

理由：没有 preserved partition，utility object 不稳定。

### 不能成立

```text
旧 D07 controlled result 直接证明 real-DCLM functional specialization。
```

不能成立，因为它是 synthetic oracle/controlled surface。

```text
A07_04/A07_06 已经证明 neural MoE specialization。
```

不能成立，因为 A07_04 小而 noisy，A07_06 rare-loss gain 和 intended conflict metric 脱钩。

```text
rare loss 改善就说明 common/rare conflict 被修复。
```

不能成立，因为 rare loss 需要 mechanism guard。

```text
attention context 可以直接等同于 rare feature。
```

不能成立，除非先给出操作化证据，例如 attention-derived grouping 的 rarity、route margin、gradient conflict 或 tail-loss link。

## 13. 下一步最小测试骨架

当 06 给出 preserved partition 后，07 应该按以下顺序进入：

### Test 1：conflict existence

问题：common 和 rare 是否真的在共享 expert 中负梯度冲突？

主指标：

$$
\mathcal{C}_{C,R}>0.
$$

失败含义：没有干扰对象，不应谈 conflict-splitting method。

### Test 2：conflict reduction

问题：candidate routing 或 update control 是否降低 $\mathcal{C}_{C,R}$？

主指标：

$$
\Delta\mathcal{C}_{C,R}
=\mathcal{C}_{C,R}^{\mathrm{baseline}}
-\mathcal{C}_{C,R}^{\mathrm{candidate}}.
$$

保护指标：负载、active experts、LM loss、common loss。

### Test 3：rare/tail loss

问题：降低冲突是否改善 rare/tail loss？

主指标：

$$
\Delta L_R=L_R(\mathrm{baseline})-L_R(\mathrm{candidate}).
$$

失败含义：conflict metric 不是当前 value 的有效中介，或 candidate 只改变几何不改变功能。

### Test 4：fixed-route utility

问题：被选 expert 是否有 causal utility？

主指标：

$$
A_\ell=CE_{\ell}^{-\mathrm{routed}}
-\frac{1}{E-1}\sum_{e\ne \mathrm{routed}}CE_{\ell}^{-e}.
$$

失败含义：partition 可能降低干扰但没有专家功能绑定，或 expert function 仍是 shared。

## 14. 主张边界

可以 claim：

- controlled D07 支持 partition value 的审计链：metric surface、rare interference reduction、route-function binding。
- neural A07_04 测到了 common/rare gradient conflict，但只给弱方向性证据。
- A07_05/A07_06 暴露了 rare-loss gain 和 intended mechanism 脱钩的风险。
- nested A07 支持 common-backbone formation 和 update-space tail control 的 controlled mechanism。
- 07 必须在 06 preservation 之后才能支持真实 utility。

不能 claim：

- real-DCLM 已有 functional MoE specialization。
- balanced load、high NMI 或 route purity 证明 value。
- dense-beating MoE 已经成立。
- 所有 rare feature 都位于 common 正交补。
- common-subspace update control 已经适用于真实语言模型或真实 MoE。

## 15. 来源索引

| 角色 | 来源 |
|---|---|
| 07 入口 anchor | `Projects/from-attention-to-search/main/problem_anchors/07_features_overlap/07.md` |
| D07 metric surface | `Projects/from-attention-to-search/main/experiments/A07/A07_01_common_rare_conflict_metric_audit/summary.md` |
| D07 common-control | `Projects/from-attention-to-search/main/experiments/A07/A07_02_common_controlled_rare_interference/summary.md` |
| D07 route-function binding | `Projects/from-attention-to-search/main/experiments/A07/A07_03_route_function_binding/summary.md` |
| Neural conflict proxy | `Projects/from-attention-to-search/main/experiments/A07/A07_04_common_rare_gradient_conflict_splitting/summary.md` |
| Common-update diagnostic | `Projects/from-attention-to-search/main/experiments/A07/A07_05_common_update_interference_diagnostic/summary.md` |
| Projected MoE warning | `Projects/from-attention-to-search/main/experiments/A07/A07_06b_projected_moe_conflict_splitting/summary.md` |
| Nested backbone | `Projects/from-attention-to-search/main/experiments/A07/A07_01_nested_common_backbone_reproduction/summary.md` |
| Nested update control | `Projects/from-attention-to-search/main/experiments/A07/A07_02_nested_tail_common_subspace_control/summary.md` |
| Nested utility diagnostic | `Projects/from-attention-to-search/main/experiments/A07/A07_03_nested_route_function_binding/summary.md` |
| 主线同步 | `sync/S000_current_specialization/research_lines/07_interference_value_line_cn.md` |

