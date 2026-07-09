# Story: Expert Specialization As Advantage-Separable Margin Preservation

文档状态：

- 日期：2026-07-09
- 类型：daily working story / mechanism reframing package
- 研究线：feature-level expert specialization in top-1 MoE gating
- 语言：中文工作稿
- canonical 状态：不是 `Projects/from-attention-to-search/` 下的正式 story；后续由用户决定是否迁入项目主线

## 0. Verdict

当前主线应从“不同 feature / slot 是否被分到不同 expert”重定义为：

> expert specialization 是一个 feature-conditioned expert advantage 能否形成、能否增厚 route margin、能否穿过训练扰动保持，并最终降低 interference 的问题。

因此下一步不是直接设计新 router，也不是继续做 common subtraction / spectral / MPI 式浅层方法尝试。下一步是先建立一个最小动力学模型：router row 的一步移动是否可以由 expert advantage 预测；feature margin 的增长或消耗是否可以被 signal / noise / common / hidden-drift budget 解释。

如果这个模型成立，后续 router 改进才有明确靶点：让 router 和 expert utility 建立直接联系，避免 top-1 selected-expert feedback 只强化当前被选 expert、缺少反事实 expert comparison。MPI / expert spectral router 可以作为浅层参考，但不能作为当前主线解法。

## 1. 术语约定

| 术语 | 中文含义 | 具体对象或公式 | 为什么重要 | 不能证明什么 |
| --- | --- | --- | --- | --- |
| expert specialization | 专家专业化 | 某个 feature 或 conflict group 被路由到对它有功能优势的 expert，并且该绑定被训练保持 | 这是主线想证明的对象 | 不能由 NMI 或 load balance 单独证明 |
| route purity / NMI | 路由标签纯度 | NMI(feature label, expert route) | 可判断 collapse / alignment | 不能证明 expert utility |
| route margin | 路由间隔 | $m_f=\min_{b\ne a(f)}(w_{a(f)}-w_b)^\top\mu_f$ | 判断 feature center 是否仍在 matched expert 区域 | 不证明 expert 输出有用 |
| expert advantage | 专家优势 | $A_e=-\langle\nabla_{\hat y}\ell,E_e(h)-\hat y\rangle$ | 衡量增加 expert $e$ 权重是否会降低当前 loss | 不等于语义解释 |
| probability-weighted advantage | 概率加权专家优势 | $p_eA_e$ | 决定 soft router row 的一阶移动强度 | 不自动说明 top-1 hard router 有相同反馈 |
| advantage gap | 专家优势差 | $p_aA_a-p_bA_b$ | 判断 matched expert 是否相对 competitor 有正信号 | 不证明长期 preservation |
| margin budget | 间隔预算 | $m_f(T)$ 的 signal / noise / common / hidden-drift 分解 | 把 preservation failure 定位到可测项 | 不证明真实 DCLM 语义专家 |
| cross-feature margin damage | 跨特征间隔损害 | $C_{g\to f}=-\mathbb E[\Delta m_f\mid g]_+$ | 判断两个 feature 是否真的冲突、是否值得分 expert | 不等于完整下游 utility |
| selected-expert feedback | 被选专家反馈 | top-1 只实际使用当前 selected expert 的 loss feedback | 解释 lock-in 和弱纠错 | 不说明所有 sparse router 必然失败 |
| router-expert coupling | router 与 expert 的直接联系 | router update 直接利用 expert utility / advantage / spectral function 的机制 | 后续新 router 的可能靶点 | 当前尚未被本 story 证明 |

## 2. 为什么旧问题会卡住

旧问题是：

> 能否把不同 feature / slot 分到不同 expert？

它会卡住，因为它把“划分现象”和“功能价值”混在一起。

一个 feature-pure route bucket 可能只是：

- deterministic shortcut；
- load balance artifact；
- common / position / token identity cue；
- 初始化给出的几何分区；
- NMI 高但 expert identity 已经换了；
- target accuracy 高但 router margin 已经负了。

所以“分到不同 expert”本身不是因果目标。真正目标应是：

> 分开是否减少了同 expert 共享时的负干扰？

更具体地说，如果训练 feature $g$ 会系统性降低 feature $f$ 的 matched route margin，或者提高 $f$ 的 rare loss，那么 $f$ 和 $g$ 有 conflict。只有这时，把它们路由到不同 expert 才有可证明价值。

## 3. 新定义：specialization 的三个条件

### 3.1 routing identity

某个 feature $f$ 稳定进入 matched expert $a(f)$：

$$
P(r(h)=a(f)\mid f)\text{ high},\qquad m_f>0.
$$

主指标是 matched preserve fraction、margin p05、sign flip rate。NMI 只能做辅助，因为 label permutation 或 high-NMI wrong identity 可以骗过它。

### 3.2 advantage separability

matched expert 对 feature $f$ 有稳定的 probability-weighted advantage：

$$
G_{f,a,b}=\mathbb E[p_aA_a-p_bA_b\mid f]>0.
$$

这才说明训练信号会把 matched router row 朝 $f$ 的方向推，或者至少相对 competitor 增厚 margin。

### 3.3 functional value

分开后，conflict / rare feature 的 functional metric 改善：

- rare loss 下降；
- route-function binding 成立；
- modal expert ablation 有损害，nonmodal ablation 无损害；
- causal intervention 显示 routed expert 对对应 feature 有 utility。

因此新的 claim ladder 是：

1. feature route is reachable；
2. feature route has positive margin；
3. margin growth is predicted by expert advantage；
4. margin survives signal/noise/common/hidden drift；
5. preserved partition reduces interference or has causal expert utility。

## 4. 物理先验

### P1: router row 不会抽象地学习 feature；它沿 hidden direction 被 expert advantage 推动

在 soft mixture 近似下：

$$
\Delta w_e=\eta\frac{p_e}{\tau}A_e(h,y)h.
$$

含义：router row 的移动只由三项决定：

1. 当前 router 对 expert $e$ 的概率 $p_e$；
2. expert $e$ 对当前 loss 的局部好坏 $A_e$；
3. 当前样本 hidden direction $h$。

如果 $A_e$ 对 feature 没有差异，那么线性 router center 再漂亮，也可能只是初始化几何，不是 specialization learning。

### P2: feature 分 expert 的必要性来自 conflict，不来自 feature label 本身

两个 feature 是否需要分开，应由 cross-feature margin damage 判断：

$$
C_{g\to f}=-\mathbb E[\Delta m_f\mid g]_+.
$$

如果 $C_{g\to f}$ 很小，硬分开 $f$ 和 $g$ 可能没有 functional value。若 $C_{g\to f}$ 大，且分开后 rare loss 降低，才是有效 specialization。

### P3: preservation 是有限 margin budget，不是二值现象

A06 已经支持：正 margin 必须足够厚。训练中的 router drift、feature drift、common / background signal 和 noise 会消耗 margin。

因此 preservation 应写成：

$$
\begin{aligned}
m_f(T)
&\approx m_f(0)
+\sum_{t<T}\Delta m_f^{signal}(t) \\
&\quad+\sum_{t<T}\Delta m_f^{noise}(t)
+\sum_{t<T}\Delta m_f^{common}(t)
+\sum_{t<T}\Delta m_f^{hidden}(t).
\end{aligned}
$$

### P4: top-1 selected-expert feedback 可能缺少反事实 expert comparison

在 top-1 中，训练实际只看到 selected expert 的输出。未选 expert 没有被真正试用，因此 router 很难知道“哪个未选 expert 更适合当前 feature”。这会造成 early lock-in 和 weak correction。

这给后续 router 方法一个明确方向：让 router update 更直接地看到 expert utility / advantage，而不是只看到当前 selected expert feedback。

## 5. 数学模型

### 5.1 hidden state 分解

令 routed hidden state 为：

$$
h=c+\mu_f+\epsilon,
$$

其中 $c$ 是 common / background direction，$\mu_f$ 是 feature center，$\epsilon$ 是同 feature 内 spread。

router score：

$$
s_e(h)=w_e^\top h.
$$

matched route margin：

$$
m_{f,a,b}=(w_a-w_b)^\top\mu_f.
$$

### 5.2 expert advantage

soft mixture output：

$$
\hat y=\sum_e p_e(h)E_e(h).
$$

expert advantage：

$$
A_e(h,y)=-\langle\nabla_{\hat y}\ell(\hat y,y),E_e(h)-\hat y\rangle.
$$

如果 $A_e>0$，提高 expert $e$ 权重会降低 loss；如果 $A_e<0$，提高它的权重会升高 loss。

### 5.3 margin update

冻结 hidden center 时，一步 margin 变化近似为：

$$
\Delta m_{f,a,b}\approx(\Delta w_a-\Delta w_b)^\top\mu_f.
$$

代入 soft router row update：

$$
\Delta m_{f,a,b}^{pred}
\approx
\eta\frac{1}{\tau}\mathbb E[(p_aA_a-p_bA_b)h^\top\mu_f\mid f].
$$

这个式子是下一步实验的核心。

它可以被直接证伪：如果 $\Delta m^{pred}$ 与实际一步 $\Delta m^{actual}$ 的符号和排序不一致，说明这个模型不能作为 router 改进的理论基础。

## 6. 当前证据如何进入新 story

### Observation

现有 A06 证据支持：

- controlled route-position feature geometry 可发现、可初始化、可保持；
- controlled preservation 来自 positive margin buffer，不是 active center tracking；
- A06_23 支持 finite safe-margin threshold；
- real-DCLM proxy routing step 0 存在，但 ordinary training 在 step 5/10 擦除；
- common/residual causality 在 A06_22 中随 projector 翻转，不能直接 claim common 是 root cause；
- A06_30 支持 no-background full-slot 条件下 ideal centers 可以长训保持，说明 background / non-feature positions 是 mixed full-LM 失败的必要机制候选。

### Interpretation

这些证据共同指向：

> 当前不是 feature geometry 不存在，而是 training feedback 没有稳定地把 feature advantage 转换为 margin growth，或者 margin growth 被 background/common/noise/hidden drift 吃掉。

### Boundary

不能说：

- real semantic experts 已经存在；
- high NMI / load balance 证明 specialization；
- common subtraction 是方法；
- MPI / spectral router 已经解决 routing；
- MTP 已经证明 MoE routing preservation。

## 7. 接下来的研究路线

### Stage 0: 机制审核，不训练模型

先在 frozen-hidden / one-step setting 中测：

$$
\Delta m^{pred}\quad\text{vs}\quad\Delta m^{actual}.
$$

目标是验证 expert advantage 是否真能解释 router row movement 和 route margin change。

### Stage 1: signal/noise margin budget

如果 Stage 0 通过，再逐步加入 background / non-feature positions，审计哪一项首先把 positive margin 吃掉：

- 正确 feature signal；
- zero-mean noise；
- common / background biased signal；
- hidden drift；
- top-1 selected-feedback bias。

### Stage 2: soft-to-top1 dynamics

比较 soft router、low-temperature router、top-1 router：

- soft 是否有 matched advantage correction？
- top-1 是否因为 selected feedback 而弱纠错？
- 温度降低是否连续逼近 lock-in？

### Stage 3: router method construction

只有当 Stage 0-2 指出明确缺陷后，才设计新 router。

可能方向：

1. **advantage-aware router update**：router row update 显式利用 $A_e$ 或估计的 counterfactual expert advantage；
2. **expert-guided router geometry**：router rows 不只来自 hidden centers，也来自 expert input/output function geometry；
3. **margin-protected refresh**：当 margin budget 低于阈值时重估 route-state pool 或 row projection；
4. **soft-to-sparse bridge**：训练早期用 soft / counterfactual feedback，后期收缩到 sparse top-1；
5. **MTP / long-horizon objective as signal source**：只有在 margin model 清楚后，才测试 MTP 是否增厚 route-relevant margin。

MPI 可以作为第 2 类的浅层 baseline，但它目前不是理论闭环。我们需要知道 expert geometry 中哪一项真正对应 $A_e$ 或 $\Delta m_f$，否则 spectral direction 只是另一个 proxy。

### Stage 4: utility / interference value

只有 preserved margin 成立后，才进入 A07 utility：

- shared vs separated expert；
- rare loss；
- route-function binding；
- causal ablation；
- cross-feature margin damage reduction。

## 8. 下一步 falsifiable 假设

下一步唯一主假设：

> 在 frozen-hidden controlled setting 中，probability-weighted expert advantage gap $p_aA_a-p_bA_b$ 可以预测 matched route margin 的一步变化。如果它不能预测，当前 advantage-based specialization story 必须修正；如果它能预测，后续 router 改进应围绕增强 matched advantage signal、减少 background/common margin consumption、补足 top-1 counterfactual feedback 展开。

最重要主指标：

$$
\operatorname{sign\_agree}(\Delta m^{pred},\Delta m^{actual})
$$

以及：

$$
\operatorname{corr}(\Delta m^{pred},\Delta m^{actual}).
$$

支持预期：

- matched expert 条件下 $p_aA_a-p_bA_b>0$；
- $\Delta m^{pred}$ 与 $\Delta m^{actual}$ 符号一致；
- known bad 条件中 advantage gap 接近 0 或不能预测 positive margin；
- high NMI but wrong matched identity 的 confusing case 被 matched preserve / margin 指标识别。

削弱预期：

- $A_e$ 无法解释 router row movement；
- $\Delta m^{pred}$ 与 $\Delta m^{actual}$ 低相关或反号；
- identical / shuffled expert control 也通过；
- margin 改善只来自 load scale 或 norm artifact。

不充分预期：

- 实现中的 top-1 hard argmax 让 task loss 对 router row 没有可测梯度；
- 没有保存 expert outputs、loss gradient、router probabilities 或 hidden centers；
- hidden drift 未冻结，导致 one-step row update 和 hidden update 混在一起。

## 9. Mainline impact

- affects hypothesis? yes. specialization 从“feature purity”改成“advantage-separable margin preservation”。
- affects claim boundary? yes. NMI / load 进一步降级为 guards；expert advantage 和 margin budget 成为机制证据。
- affects next decision? yes. 下一步从 common-subtraction / spectral-router method 转为 frozen-hidden advantage-to-margin audit。
- recommendation: pursue.

## 10. Source map

Project state and rules:

- `AGENTS.md`
- `PROJECTS.md`
- `sync/README.md`

Current specialization surfaces:

- `sync/S000_current_specialization/README.md`
- `sync/S000_current_specialization/research_lines/00_overall_current_line_cn.md`
- `sync/S000_current_specialization/research_lines/06_proxy_preservation_line_cn.md`
- `sync/S000_current_specialization/research_lines/07_interference_value_line_cn.md`

Key A06 / A07 / A11 sources:

- `sync/S000_current_specialization/stories/06_geometry_proxy_preservation/story_cn.md`
- `sync/S000_current_specialization/anchors/06_geometry_proxy_preservation/research_map.md`
- `sync/S000_current_specialization/anchors/06_geometry_proxy_preservation/06_23_top1_lockin_margin_threshold_anchor.md`
- `sync/S000_current_specialization/anchors/06_geometry_proxy_preservation/06_24_synthetic_common_rare_transformer_moe_anchor_cn.md`
- `sync/S000_current_specialization/anchors/06_geometry_proxy_preservation/06_27_gradient_fisher_route_state_selector_anchor.md`
- `sync/S000_current_specialization/anchors/06_geometry_proxy_preservation/06_30_noise_free_full_slot_preservation_anchor.md`
- `sync/S000_current_specialization/research_lines/07_interference_value_line_cn.md`
- `sync/S000_current_specialization/stories/11_long_horizon_mtp_objective/story_cn.md`
