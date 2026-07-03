# 01 线重构：路由对象与公共算子的可识别性

## 摘要

01 线不应该被理解为一条已经过时的 toy-specialization 线。它更适合被重构为主线最前面的**对象识别层**：

```text
先问 router 应该绑定什么对象；
再问 common 到底是哪一种机制对象；
最后才允许把这些对象带入 06 preservation 或 07 utility。
```

这条线回答两个容易混淆的问题。

第一个问题是：路由器读到的是词元身份、位置/slot、二者的原子组合，还是公共偏置？早期 slot/context 实验证明：slot 信号可以进入 B-position hidden state，并且在 fixed-B 正例中能控制路由；但在 multi-B 中，B identity 和 top-1 路径依赖仍会干扰路由。因此“slot 可见”不等于“路由绑定到 slot 功能”。

第二个问题是：当我们说 common component 时，它是 hidden-state 方差方向、均值方向、梯度重叠方向、还是训练反馈漂移方向？后来的 common-operator 线证明：common 不是一个通用 hidden-state 方向，而是一族由机制判据索引的算子。受控实验支持这个结论；真实 DCLM gate-logit bridge 则削弱了“简单低秩 logit common 解释真实 collapse”的说法。

所以 01 对主线的作用不是直接提供方法，而是给 05、06、07 三条后续线加上定义约束：

```text
05 不能把所有失败都叫 common collapse；
06 不能在未定义 P_C 时直接做 common-subtracted routing；
07 不能把 route NMI、load balance 或 rare-loss gain 单独当成 functional specialization。
```

当前重构后的 01 最小结论是：

$$
\boxed{
\text{路由对象和公共算子必须先按机制判据定义；否则后续 preservation 或 utility 结论不可读。}
}
$$

## 1. 术语解释

| 术语 | 中文含义 | 具体对象或计算 | 为什么重要 | 不能证明什么 |
|---|---|---|---|---|
| 路由器（router / gate） | 给每个 token 选择 expert 的打分函数。 | 本线主要用线性打分 $z_e=w_e^\top h$ 和 top-1 选择 $r(h)=\arg\max_e z_e$。 | 它决定 hidden state 被送到哪个 expert。 | 路由对齐不能证明 expert 有功能价值。 |
| 可操作特征（operational feature） | 当前实验中被允许作为“feature”的具体分组对象。 | 例如 slot、$B_i$、原子对 $(slot,B_i)$、真实 DCLM proxy cluster。 | 不先定义它，NMI 或一致性指标没有对象。 | 不等于自然语言语义特征。 |
| slot/context 信号 | 同一个 B token 在不同上下文中需要不同预测目标的上下文信息。 | 早期 A01 中的 slot $s$、role context、long repeated cue 或 distributed role code。 | 它测试 router 能否利用上下文，而不是只读 B identity。 | slot 可见不证明 route-function binding。 |
| 词元身份（token identity） | 由 $B_i$ 自身携带的稳定表面身份信息。 | 在模型中可表示为 hidden component $c_i$。 | 它会和 slot 信号竞争路由支配权。 | token identity routing 不等于 feature-level specialization。 |
| 路由一致性（route-feature NMI） | 路由 label 和特征 label 的一致程度。 | 归一化互信息，范围 0 到 1。 | 判断路由是否按某个 feature 分。 | 不能证明 expert 计算有用；也可能受 expert 身份交换影响。 |
| 分配-效用一致（assignment-utility agreement） | 被 router 选中的 expert 是否也是某个 group 的 causal utility-best expert。 | 比较 assigned expert 与 forced expert loss / ablation 得到的 best expert。 | 它比 NMI 更接近功能绑定。 | 单独使用会被 utility collapse 误导。 |
| 公共成分（common component） | 多个 group、token 或更新共享的结构。 | 可以来自 activation 方差、均值、梯度重叠、checkpoint drift。 | 这是 common-subtraction 和 anti-feedback 的候选对象。 | common 不一定有害，也不一定可删除。 |
| 公共算子（common operator / projector $P_C$） | 选择某类公共结构的线性算子。 | residualization 用 $(I-P_C)h$；feedback removal 用 $(I-P_C)\Delta h$。 | 把 common 从直觉变成可审计对象。 | 一个判据下有效的 $P_C$ 不能自动迁移到另一个判据。 |
| 激活公共（activation common） | hidden state 中高方差或均值可见的公共结构。 | activation PCA、group mean。 | 它是最直观的 common 估计。 | 高方差不等于优化干扰或训练反馈因果。 |
| 梯度公共（gradient common） | 不同 group 的更新方向中共享、冗余的部分。 | 删除 $Ph$ 后 pairwise group-gradient cosine 下降多少。 | 它更接近 optimization interference。 | 不直接等于真实 checkpoint feedback drift。 |
| 反馈公共（feedback common） | 训练从 step 0 到 step $t$ 的漂移中会覆盖路由的共享成分。 | $\Delta h=h_t-h_0$ 或 $\Delta z=z_t-z_0$ 的 replay/removal。 | 它连接 01 和 06 preservation failure。 | 低秩 logit drift 失败不等于 hidden feedback 无关。 |

## 2. 为什么 01 线看起来散

01 线表面上包含两组不同材料：

```text
slot/context dominance:
  router 实际绑定 slot、B_i，还是二者组合？

common operator mechanism:
  common 是 activation direction、gradient direction，还是 feedback drift？
```

它们其实在问同一个上游问题：

> 在讨论 MoE 专家专业化之前，我们到底知道 router 和 intervention 正在读哪个对象吗？

如果不知道 feature 对象，route NMI 无法解释。如果不知道 common 算子，common subtraction 无法解释。如果两个都不知道，后续任何方法都可能只是改变负载、打分尺度或路径依赖，而不是修复 specialization。

因此 01 的重构不是把旧材料强行并成一个实验，而是把它们放到同一条逻辑链：

```text
feature object ambiguity
-> route binding ambiguity
-> common operator ambiguity
-> feedback source ambiguity
-> 06 preservation 和 07 utility 的前置定义约束
```

## 3. 干净基线：可见性不等于绑定，绑定不等于效用

### 3.1 路由输入分解

早期 slot/context 实验可以写成：

$$
h_{i,s}=c_i+\beta u_s+\epsilon.
$$

这里，$h_{i,s}$ 是 token $B_i$ 在 slot $s$ 下的路由位置 hidden state；$c_i$ 是 B-token identity；$u_s$ 是 slot/context 方向；$\beta$ 是 slot 信号强度；$\epsilon$ 是噪声和未建模结构。

线性 router 的 expert 打分是：

$$
z_e(i,s)=w_e^\top h_{i,s}
=w_e^\top c_i+\beta w_e^\top u_s+w_e^\top\epsilon.
$$

如果 $w_e^\top c_i$ 或 $w_e^\top\epsilon$ 的变化幅度大于 $\beta w_e^\top u_s$，则即使 slot 可以被 probe 读出，top-1 router 也可能主要按 B identity 或 nuisance 分。

### 3.2 命题 1：slot 可见不推出 slot 路由

**命题。** 存在 hidden representation 使 slot 可以被线性 probe 完美读出，但 top-1 router 的分配与 slot 近似无关。

**构造。** 令 $u_s$ 是 slot 方向，$c_i$ 是 token identity 方向，并令 $u_s\perp c_i$。假设 probe 权重 $a_s$ 对 $u_s$ 有高对齐，所以 probe 可由 $a_s^\top h$ 恢复 slot。另一方面，令 router rows $w_e$ 全部位于 $\operatorname{span}\{c_i\}$，即 $w_e^\top u_s=0$。则：

$$
z_e(i,s)=w_e^\top c_i+w_e^\top\epsilon
$$

与 $s$ 无关。因此 $NMI(route;slot)$ 可以很低，而 $Probe(h\to slot)$ 仍然可以是 1。

**意义。** A01 multi-B 结果正落在这个风险区：`h_B -> slot` probe 和 target accuracy 都可以达到 1，但 learned top-1 route 没有稳定绑定 slot utility。

### 3.3 命题 2：route alignment 不推出 expert utility

定义 forced expert loss：

$$
CE_{s,e}=CE(\text{slot }s\text{ 被强制送到 expert }e).
$$

若 router 对 slot 的分配是 $q_{s,e}=P(r=e\mid s)$，则 route-conditioned loss 是：

$$
CE_{s,\mathrm{route}}=\sum_e q_{s,e}CE_{s,e}.
$$

均匀 expert 使用的 loss 是：

$$
CE_{s,\mathrm{uniform}}=\frac{1}{E}\sum_e CE_{s,e}.
$$

即使 $q_{s,e}$ 完全对角，如果所有 expert 对所有 slot 的 loss 相同：

$$
CE_{s,1}=CE_{s,2}=\cdots=CE_{s,E},
$$

则 route alignment 没有任何功能效用。

所以 route NMI 是结构指标，不是效用指标。真正的 route-function binding 需要 forced-routing utility 或 fixed-route ablation。

## 4. 公共算子的不可能性：只看 loss 不能分配 common 属于哪条 branch

假设模型输出由 shared branch 和 routed branch 相加：

$$
F_g(h)=S(h)+R_g(h).
$$

对任意 common function $\Delta(c)$，定义：

$$
S'(h)=S(h)+\Delta(c),
$$

$$
R'_g(h)=R_g(h)-\Delta(c).
$$

则：

$$
S'(h)+R'_g(h)=S(h)+R_g(h)=F_g(h).
$$

这说明：只看总输出或 loss，不能唯一判断 common computation 应该属于 shared branch 还是 routed expert。这个不可能性结果解释了为什么 01 不能直接变成“加 common branch”方法。必须先说明 common 的机制判据。

## 5. 公共算子的机制索引模型

令候选公共投影为 $P$。不同机制对应不同判据。

### 5.1 激活判据

激活公共关注 hidden state 的高方差或均值结构：

$$
J_{\mathrm{act}}(P)=\operatorname{Var}(Ph)
$$

或：

$$
J_{\mathrm{mean}}(P)=\left\|\mathbb{E}[h]\right\|_P^2.
$$

它适合回答：

```text
hidden state 中哪个方向最大、最共享？
```

但它不保证该方向造成优化干扰。

### 5.2 功能判据

功能公共关注删除 $Ph$ 后 shared prediction 是否受损：

$$
\Delta L_c(P)=L_c((I-P)h)-L_c(h).
$$

它适合回答：

```text
这个方向是不是有用公共计算？
```

但有用公共计算不能被轻易删除。

### 5.3 梯度判据

梯度公共关注不同 group 的更新是否被同一方向耦合。令 group $g$ 的梯度对象为 $G_g$，删除 $P$ 后为 $G_g^r(P)$。定义：

$$
\Delta C(P)=
\mathbb{E}_{g\ne g'}\cos(G_g,G_{g'})
-
\mathbb{E}_{g\ne g'}\cos(G_g^r(P),G_{g'}^r(P)).
$$

如果 $\Delta C(P)$ 大，说明 $P$ 删除了跨 group 冗余更新。

### 5.4 反馈判据

反馈公共关注训练漂移是否覆盖路由。令：

$$
\Delta h_t=h_t-h_0.
$$

反馈 replay 使用：

$$
h_{\mathrm{fb}}=h_0+P_{\mathrm{fb}}\Delta h_t.
$$

反馈 removal 使用：

$$
h_{\mathrm{res}}=h_0+(I-P_{\mathrm{fb}})\Delta h_t.
$$

只有当 replay 能复现 collapse、removal 能 rescue routing 时，$P_{\mathrm{fb}}$ 才是与 preservation 相关的 feedback common。

## 6. 命题：activation common 和 gradient common 可以正交分离

令 $a,b$ 为正交单位向量。构造 hidden state：

$$
h=s_a a z_a+s_b b z_b+\epsilon,
$$

其中 $z_a,z_b$ 独立且单位方差，$s_b^2>s_a^2$。此时 activation covariance 的最大方向是 $b$。

再构造 group gradient：

$$
G_g=q_g a^\top+E_g,
$$

其中 $E_g$ 不包含比 $a$ 更强的共享 right-singular direction。则跨 group 梯度共享方向是 $a$。

因为 $a\perp b$，activation PCA 会选 $b$，gradient intersection 会选 $a$。所以：

$$
\boxed{
\text{高 activation 方差不是 optimization common 的充分定义。}
}
$$

这正是 A01_03 的数学核心：当 activation nuisance、unique variance 或 functional shared common 与 gradient common 不一致时，gradient intersection 才是优化干扰判据下的合适 estimator。

## 7. 真实 collapse 分解：gate logit drift 混合三种机制

真实 router logit 是：

$$
z_t=W_t h_t.
$$

从 step 0 到 step $t$ 的变化为：

$$
z_t-z_0=W_t h_t-W_0 h_0.
$$

加减项得到精确分解：

$$
z_t-z_0=(W_t-W_0)h_0+W_0(h_t-h_0)+(W_t-W_0)(h_t-h_0).
$$

三项分别是：

| 项 | 中文含义 | 如果它主导，说明什么 |
|---|---|---|
| $(W_t-W_0)h_0$ | gate weights 自己漂移。 | router rows 离开 step-0 proxy partition。 |
| $W_0(h_t-h_0)$ | hidden states 被训练推走。 | 表征反馈覆盖了原路由对象。 |
| $(W_t-W_0)(h_t-h_0)$ | gate 和 hidden 同时变化的交互项。 | collapse 是耦合机制，不能用单个 projector 解释。 |

因此，aggregate gate-logit drift 能复现 collapse，不等于已经知道 collapse 的 hidden 因果来源。

## 8. 证据链

### 8.1 Slot/context 可见性证据

A01 slot-context 实验的读法如下：

| 证据 | 结果 | 支持什么 | 不能支持什么 |
|---|---:|---|---|
| fixed-B long repeated slot init | route NMI = 1.000，Assign-Utility = 1.000 | context signal 可以控制 B-position routing。 | 不能推出 multi-B 稳健 specialization。 |
| fixed-B distributed role semantic | final NMI = 0.893 | distributed context 也有可读信号。 | 不能证明所有种子和 all-token routing 稳定。 |
| multi-B A_long_repeated | route NMI 0.243 -> 0.591，Assign-Utility 0.565 -> 0.925 | stronger context 改善 routing。 | 不能证明 B identity 干扰已解决。 |
| multi-B B_long_distributed | route NMI 0.078 -> 0.313，Assign-Utility 0.326 -> 0.747 | distributed signal 仍有帮助但弱。 | 不能支持强 specialization。 |
| multi-B random distributed | Assign-Utility = 0.998，route NMI = 0.010 | 说明 Assign-Utility 会被 utility collapse 误导。 | 不能把 Assign-Utility 单独当主指标。 |

结论：

```text
slot/context signal matters, but signal visibility is not enough.
```

### 8.2 Common-operator 可识别性证据

| 实验 | 主指标 | 结果 | 主线含义 |
|---|---:|---:|---|
| A01_01 | `criterion_winner_diversity` | 4 | common estimator 依赖机制判据，不支持 universal common direction。 |
| A01_03 | `n_passed_mismatch_regimes` | 4 / 4 | optimization common 在 mismatch regimes 中更接近 gradient intersection，而不是 activation PCA。 |
| A01_04 controlled | `n_passed_main_feedback_regimes` | 2 / 2，controls ok | feedback-common replay/removal 是有效受控 preservation-collapse 机制。 |
| A01_04 real-DCLM | rank-1 logit bridge pass | false | 简单低秩 gate-logit common 不能解释真实 A06 collapse。 |

真实 DCLM bridge 的关键数字：

```text
step0 proxy-route NMI = 0.7549
step5 full NMI = 0.0410
step10 full NMI = 0.0131
rank-1 mean_explain_valid = 0.4230
rank-1 mean_rescue_valid = 0.1625
mean_random_explain_valid = 0.3355
```

这说明 full logit drift 可以复现 collapse，但低秩 logit common 的特异解释和 rescue 都不足。

## 9. 与 05、06、07 的重新串联

### 9.1 01 到 05：失败对象不能只叫 collapse

05 线说 ordinary top-1 会因为 common component、错误 hidden-state population 和 early-training feedback 失败。01 给它加上定义约束：

```text
先说清楚 collapse 是 route object 错了、common operator 错了，还是 feedback source 错了。
```

否则所有失败都会被模糊地叫做 common collapse。

### 9.2 01 到 06：preservation 需要先定义 route-relevant object

06 的可达/保持逻辑依赖一个前提：要保持的 partition 是正确对象。01 的 slot-context 线说明：

```text
hidden state 中有 slot，不代表 router 读 slot；
router 读 slot，不代表 expert function 绑定 slot。
```

这也是 06 后来必须从 all-position clustering 转向 route-position state selector 的原因。

### 9.3 01 到 07：utility 不能建立在未定义的 common 上

07 需要判断 partition 是否减少 common/rare interference。01 的 common-operator 线说明：

```text
common/rare 的 common 必须先说明是 activation common、gradient common，还是 feedback common。
```

否则 rare-loss 改善可能只是负载、正则化或路由尺度改变，而不是真正减少干扰。

## 10. 重构后的 01 当前问题

01 不再应该问：

```text
能不能直接设计一个 anti-common router？
```

而应该问：

```text
在进入 preservation 或 utility 之前，当前实验中的 route object 和 common operator 是否已经被机制判据定义到足够可审计？
```

对应到当前主线，它给 common/rare routing audit 提出三个硬要求：

1. $P_C$ 不能默认是 top hidden-PC 或 mean-common，必须说明机制判据。
2. 若审计对象是 preservation failure，必须区分 gate-weight drift、hidden-state drift 和 interaction。
3. 若审计对象是 utility interference，必须优先用 gradient common 或 update-space common，而不是 activation common。

## 11. 主张边界

可以 claim：

- slot/context signal 在受控设置中可以控制 B-position routing。
- multi-B 下，slot 可见和 target accuracy 高仍不足以保证稳定 route-function binding。
- common 是机制索引的 operator family，而不是单一 hidden-state direction。
- 受控 feedback-common replay/removal 可以造成并救回 proxy-route collapse。
- 真实 DCLM 中，简单低秩 gate-logit common 不足以解释 A06 preservation failure。

不能 claim：

- 普通 top-1 NTP 自然形成 slot-level functional experts。
- high FeatureKeyConsistency、route NMI 或 Assign-Utility 单独证明 specialization。
- activation PCA 就是真实 common operator。
- real hidden-state feedback common 已被识别。
- common branch、residualized MoE 或 common-subtracted routing 已被验证。

## 12. 下一步决策

对当前 06/07 主线，01 给出的最小下一步不是新方法，而是分解：

$$
z_t-z_0=(W_t-W_0)h_0+W_0(h_t-h_0)+(W_t-W_0)(h_t-h_0).
$$

如果 collapse 主要来自 $(W_t-W_0)h_0$，下一步是 router-update / gate-loss intervention。

如果 collapse 主要来自 $W_0(h_t-h_0)$，下一步是 hidden feedback-common estimator。

如果 collapse 主要来自 interaction，下一步应先建耦合 feedback model，而不是做单 projector method。

## 13. 来源索引

| 角色 | 来源 |
|---|---|
| slot/context anchor | `Projects/from-attention-to-search/main/problem_anchors/01_slot_context_dominance_router_specialization_anchor.md` |
| slot-context summary | `Projects/from-attention-to-search/main/experiments/A01/A01_slot_context_dominance_router_specialization/summary.md` |
| bridge summary | `Projects/from-attention-to-search/main/experiments/A01/A01_slot_context_bridge_abcd_context_length/summary.md` |
| common-operator closure | `Projects/from-attention-to-search/main/problem_anchors/01_common_operator_mechanism/closure/01_common_operator_mechanism_closure_report_cn.md` |
| A01_01 summary | `Projects/from-attention-to-search/main/experiments/A01_common_operator/A01_01_common_operator_identifiability_full_run/summary.md` |
| A01_03 summary | `Projects/from-attention-to-search/main/experiments/A01_common_operator/A01_03_gradient_common_vs_activation_common_full_run/summary.md` |
| A01_04 controlled summary | `Projects/from-attention-to-search/main/experiments/A01_common_operator/A01_04_feedback_common_preservation_bridge_controlled_full_run/summary.md` |
| A01_04 real-DCLM summary | `Projects/from-attention-to-search/main/experiments/A01_common_operator/A01_04_real_dclm_feedback_logit_bridge_bounded_run/summary.md` |

