# Phase8p3 下一步计划：从“分得开”转向“分得好”

## 0. 当前主线一句话

我们的终极目标是构建一个服务于“一学就会，永不遗忘”的 Hierarchical MoE。当前阶段已经证明：

> 在固定 `u50_ext` 和短 adaptation horizon 的设置下，`split-dense u50_ext` 相对 dense FFN 已经有真实 continual learning 价值；但当前 router 还没有稳定带来额外 CL 收益。

因此下一步不是直接上 hierarchy，也不是继续切更多 band，而是先回答：

> 现在的 router 为什么没有把“可分开的数据”转化成“有功能优势、少遗忘的专家分工”？

---

## 1. Phase8p2 已经成立的结论

### 1.1 已成立

固定协议：

- model: `Qwen3-0.6B`
- layer: `8`
- expert input: `u50_ext`
- adaptation horizon: `U = 8`
- main LR regime: `0.5x`
- compared groups: `G0 / G2_u50_ext / G4_u50_ext / G0_ER`

主要结果：

| Group | LG | FC | RAS | ReachRate | Matched Forgetting |
|---|---:|---:|---:|---:|---:|
| `G0` | -0.000251 | 0.000786 | -0.001121 | 0.450 | -0.000017 |
| `G0_ER` | 0.000774 | -0.000282 | 0.000571 | 0.367 | -0.000502 |
| `G2_u50_ext` | 0.000803 | 0.000082 | 0.000503 | 0.217 | -0.000212 |
| `G4_u50_ext` | 0.000785 | -0.000122 | 0.000671 | 0.200 | -0.000184 |

当前可以写：

> `u50_ext` 上的 factorized split-dense block 已经给出真实 CL 价值。

对应结构：

$$
h_{\mathrm{out}}
=
h_{\mathrm{in}}
+
F_c(x)
+
F_p(x_{u50\_ext})
$$

其中 adaptation 主要更新 $F_p$，common branch 保持稳定。

### 1.2 还没有成立

不能写成：

> routed MoE 已经显著优于 split-dense。

原因：

- `G4_u50_ext` 的 fixed-budget `RAS` 略高于 `G2_u50_ext`；
- 但 `G4_u50_ext` 的 matched forgetting 没有优于 `G2_u50_ext`；
- `G4_u50_ext` 的 ReachRate 也没有优于 `G2_u50_ext`。

因此当前结论是：

> routing 有弱信号，但还没有稳定转化成 CL 价值。

也不能写成：

> 结构已经超过 replay baseline。

因为 `G4_u50_ext` fixed-budget `RAS` 接近或略高于 `G0_ER`，但 matched forgetting 和 ReachRate 仍低于 `G0_ER`。

---

## 2. 现在最重要的理论修正

### 2.1 “分得开”不等于“分得好”

过去直觉是：

> router 把数据分开，expert 就会专业化，然后就能逼近“一学就会，永不遗忘”。

现在必须把这条因果链拆开：

```text
数据可分
  ↓
router 能分配
  ↓
expert 有功能优势
  ↓
adaptation 后少遗忘
```

这四步不是自动成立的。

一个 router 可以把 domain、frequency bucket 或 PCA band 分得很开，但这不代表：

1. 被选 expert 的 next-token loss 更低；
2. 被选 expert 的更新更局部；
3. 被选 expert adaptation 后对 old eval 更少破坏；
4. router score 真的预测了 expert advantage。

因此下一步的定义必须从“separability”升级到：

> functional and retention-aware specialization。

---

## 3. 当前 expert specialization 应该怎么定义

### 3.1 静态功能专门化

对 token $t$，router 选中的 expert 是 $e^\star$，替代 expert 是 $e'$。

定义反事实 expert gap：

$$
G_{\mathrm{cf}}(t,e')
=
\ell_t(e')-\ell_t(e^\star)
$$

如果：

$$
G_{\mathrm{cf}}(t,e')>0
$$

说明当前被选 expert 对 token $t$ 比替代 expert 更有 next-token 功能优势。

但是这还不是 CL 的完整定义。

### 3.2 CL 专门化

CL 中需要看 adaptation 之后：

- 新 query 是否学得更好；
- old eval 是否忘得更少。

定义 learning gain：

$$
LG_m(U)
=
L(\theta_0;\mathcal{Q}_m)
-
L(\theta_m^{(U)};\mathcal{Q}_m)
$$

定义 forgetting cost：

$$
FC_m(U)
=
L(\theta_m^{(U)};\mathcal{D}_{old}^{eval})
-
L(\theta_0;\mathcal{D}_{old}^{eval})
$$

定义只惩罚遗忘的项：

$$
FC_m^+(U)=\max(FC_m(U),0)
$$

定义 retention-adjusted score：

$$
RAS_m(U)=LG_m(U)-FC_m^+(U)
$$

因此，CL specialization 应该定义为：

> 一个 expert 或 branch 在某类输入上不仅能降低 next-token loss，还能在少样本 adaptation 后带来正 learning gain，并且在 matched learning gain 下比 dense baseline 忘得更少。

---

## 4. 为什么现在的 gating 没起作用

### 4.1 可能原因一：router 目标没有对齐 expert advantage

当前 router 主要通过语言模型损失和负载约束间接训练。

但是 router 真正应该预测的是：

$$
e^\star(t)
=
\arg\min_e \ell_t(e)
$$

或者在 CL 中更严格地预测：

$$
e^\star_{\mathrm{CL}}(t)
=
\arg\max_e
\left[
\Delta L_{\mathrm{new}}(e,t)
-
\lambda \Delta L_{\mathrm{old}}(e,t)
\right]
$$

当前 router 没有直接看到这个目标，因此即使它能把数据分开，也可能没有把 token 分给真正最有功能优势的 expert。

### 4.2 可能原因二：expert 没有被限制到正确的更新空间

要训练出专一化 expert，不能只靠 router 分配样本，还需要限制 expert 看到和更新的 representation space。

当前 `G2_u50_ext` 成立，说明：

> 把可塑更新限制到 `u50_ext` 这种 functional span，本身就能降低干扰。

这也解释了为什么 `G4` 没有明显赢过 `G2`：如果 expert input space 已经提供了主要收益，那么未校准的 router 可能只是增加不稳定性，而不是增加 CL 价值。

### 4.3 可能原因三：common branch 与 plastic branch 的协作还没有被系统设计

限制 expert 输入有好处，也有代价。

好处：

> 更新更局部，不容易破坏 common knowledge。

代价：

> expert 只看 residual span，common 能力下降，必须依赖 common branch 补齐。

因此结构上应该显式分工：

$$
h_{\mathrm{out}}
=
h_{\mathrm{in}}
+
F_c(x)
+
F_p(x_{u50\_ext})
$$

其中：

- $F_c(x)$ 负责高频、通用、稳定能力；
- $F_p(x_{u50\_ext})$ 负责中尾部、可塑、低干扰更新；
- adaptation 优先更新 $F_p$；
- $F_c$ 冻结或使用极小学习率。

如果 common branch 设计不够好，plastic branch 会被迫补 common 能力，从而破坏专门化。

---

## 5. Zipfian 到 Hierarchical MoE 的逻辑里程碑

导师的直觉是：

> 语言符合 Zipfian 分布，因此模型结构应该分层处理。

这条直觉是合理的，但需要补齐中间逻辑。

### Milestone 1：从 Zipf 到更新风险

语言中少数高频模式出现很多，大量中低频模式出现很少。

因此：

- 高频知识更新密集，应该稳定保存；
- 中频知识有一定支持，适合形成可复用 specialist；
- 极低频知识支持弱，容易过拟合或污染共享参数。

### Milestone 2：从更新风险到 representation split

如果所有知识都写入同一个参数空间，新知识 adaptation 很容易破坏 old knowledge。

因此需要：

$$
x
\rightarrow
(x_{\mathrm{common}}, x_{\mathrm{plastic}})
$$

当前 PCA `u50_ext` 是一个实用的 plastic-space 近似，但不是最终语义分解。

### Milestone 3：从 representation split 到 common/plastic architecture

结构应该至少包含：

$$
F_c(x)
+
F_p(x_{\mathrm{plastic}})
$$

Phase8p2 已经支持这一步。

### Milestone 4：从 common/plastic 到 function-aware routing

只有当多个 plastic experts 的优势不同，且 router 能预测这种优势时，routing 才有必要。

否则 split-dense 已经足够强，routing 只会带来额外不稳定。

### Milestone 5：从 flat routing 到 hierarchy

只有当 coarse split 的功能优势成立，且 learned coarse router 能稳定接近 oracle coarse，才应该进入 hierarchical MoE。

现在还没有到这一步。

---

## 6. Phase7 到底说明了什么

Phase7 不是在证明 PCA 是最终正确语义分解。

Phase7 说明的是：

1. `full PCA tail residual` 太粗，不能直接作为 CL expert input；
2. `mid/upper-mid family` 比 full tail 更有前景；
3. `u50_ext` 是当前 CL 中更好的 functional span；
4. sparse dictionary 的重构优于 PCA top-K，说明真实 token 表征更可能是稀疏、重叠、非正交 feature 的组合；
5. 因此 PCA 应该被看作诊断工具和阶段性工程近似，而不是最终语义 basis。

结论：

> PCA `u50_ext` 现在可以作为低成本主线候选，但未来要准备转向更接近真实语义 feature 的 projection-free 或 dictionary-inspired 表示。

---

## 7. Phase8p3 具体执行计划

### 7.1 实验 A：Router-function audit

目的：

> 判断 `G4_u50_ext` 没有稳定赢 `G2_u50_ext`，到底是 router 选错了，还是 experts 本身没有形成可用差异。

使用已有 Phase8p2 checkpoints，不先训练新结构。

#### 需要计算

对每个 token $t$ 和 expert $e$，计算：

$$
\ell_t(e)
$$

selected expert：

$$
e_{\mathrm{sel}}(t)
=
\arg\max_e g_e(t)
$$

oracle expert：

$$
e_{\mathrm{oracle}}(t)
=
\arg\min_e \ell_t(e)
$$

selected regret：

$$
R_{\mathrm{sel}}(t)
=
\ell_t(e_{\mathrm{sel}})-\min_e \ell_t(e)
$$

best-expert hit rate：

$$
H
=
P(e_{\mathrm{sel}}=e_{\mathrm{oracle}})
$$

route margin：

$$
M(t)
=
g_{e_1}(t)-g_{e_2}(t)
$$

其中 $e_1$ 和 $e_2$ 是 router 分数最高和第二高的 expert。

计算相关性：

$$
\rho
=
\mathrm{Corr}(M(t), -R_{\mathrm{sel}}(t))
$$

#### 必须输出

1. selected regret mean / median；
2. best-expert hit rate；
3. route margin 与 expert advantage 的相关；
4. per-expert load；
5. per-expert average loss；
6. per-frequency-bucket regret；
7. middle / rare token regret；
8. old eval token regret；
9. query token regret。

#### 判定

如果 oracle expert 明显优于 selected expert：

> router 是主要瓶颈，进入 advantage-aware router。

如果 oracle expert 也不明显优于 split-dense：

> routed experts 本身没有形成足够差异，先不要继续 router，回到 common/plastic branch 设计。

---

### 7.2 实验 B：Oracle routing upper bound

目的：

> 估计当前 experts 如果由一个理想 router 使用，最多能比 vanilla G4 好多少。

在 evaluation 时用：

$$
e_{\mathrm{oracle}}(t)
=
\arg\min_e \ell_t(e)
$$

代替 learned router。

输出：

1. oracle-routed query loss；
2. oracle-routed old loss；
3. oracle-routed middle / rare token loss；
4. oracle-vs-learned gap；
5. oracle-vs-G2 gap。

判定：

- 如果 oracle-routed G4 明显优于 G2：router calibration 值得做。
- 如果 oracle-routed G4 仍不优于 G2：当前多 expert 没有提供足够函数差异，routing 暂停。

---

### 7.3 实验 C：Advantage-supervised router smoke

只有在实验 A/B 显示 router 是瓶颈时执行。

构造 soft expert label：

$$
q_e(t)
=
\frac{\exp(-\ell_t(e)/\tau)}
{\sum_{e'}\exp(-\ell_t(e')/\tau)}
$$

训练 router：

$$
L_{\mathrm{router}}
=
\mathrm{KL}(q(t)\Vert g(t))
$$

第一版只训练 router，冻结 experts 和 common branch。

比较：

1. vanilla G4；
2. oracle-routed G4；
3. advantage-supervised-router G4；
4. G2 split-dense。

指标：

- fixed-budget LG / FC / RAS；
- ReachRate；
- matched forgetting；
- route margin 与 advantage correlation；
- selected regret。

判定：

> 只有 advantage-supervised router 同时提高 ReachRate、matched forgetting 或 selected regret，才说明 routing 线值得继续。

---

### 7.4 实验 D：Common/plastic cooperation ablation

目的：

> 判断 `G2_u50_ext` 的收益来自哪里，以及 common branch 是否设计合理。

组别：

1. `G2_freeze_common_update_plastic`：当前主设定；
2. `G2_update_common_and_plastic`：common 和 plastic 都更新；
3. `G2_freeze_plastic_update_common`：只更新 common；
4. `common_only`：只保留 common branch；
5. `plastic_only`：只保留 plastic branch。

核心问题：

- common branch 是否确实承担 common ability；
- plastic branch 是否确实承担 new-domain adaptation；
- 同时更新 common 是否显著增加 forgetting；
- plastic-only 是否 learning gain 高但 common 能力差。

判定：

> 如果 freeze common + update plastic 仍然最好，说明 common/plastic factorization 是正确方向。

---

### 7.5 实验 E：`u50_ext` 投影成本与 surrogate

目的：

> 判断当前路线是否能转成实际可用模型。

需要测量：

1. exact `u50_ext` projection 的时间开销；
2. exact projection 的显存开销；
3. 与普通 FFN / G2 block 的额外开销比例；
4. projection 是否成为训练瓶颈。

然后训练一个 surrogate extractor：

$$
\hat{x}_{u50\_ext}
=
S_\phi(x)
$$

目标：

$$
L_{\mathrm{proj}}
=
\|S_\phi(x)-x_{u50\_ext}\|_2^2
$$

第一版候选：

1. linear low-rank surrogate；
2. small bottleneck MLP surrogate；
3. sparse-dictionary-inspired top-K surrogate。

比较：

- reconstruction MSE；
- cosine similarity；
- G2 CL performance with exact projection；
- G2 CL performance with surrogate projection；
- wall-clock speedup。

判定：

> 如果 surrogate 保留主要 CL 收益并显著降低成本，说明路线具备实际实现可能。

---

## 8. 今晚 Agent 执行优先级

### Priority 1：Router-function audit

必须先做。  
这是判断 router 线是否继续的关键。

### Priority 2：Oracle routing upper bound

和 audit 强相关，最好一起做。

### Priority 3：Common/plastic cooperation ablation

如果算力允许，做小规模 smoke。

### Priority 4：Projection cost benchmark

必须开始测，不一定今晚完成 surrogate 训练。

---

## 9. 暂时不要做什么

1. 不要直接进入 recursive hierarchy。
2. 不要再开一轮大规模 band slicing。
3. 不要把 sparse dictionary 直接塞进主线训练。
4. 不要只用 purity / NMI / domain separability 证明 specialization。
5. 不要只看 fixed-budget RAS，而忽略 matched forgetting 和 ReachRate。

---

## 10. 下一步汇报口径

可以这样汇报：

> 本阶段更新，我的核心结论是：`u50_ext` 上的 split-dense factorized block 已经给出正式 CL 价值，但 routing 的额外价值还没有成立。证据是：`G2_u50_ext` 在等参数设置下相对 `G0` 同时改善 learning gain、forgetting 和 matched forgetting；但 `G4_u50_ext` 虽然 fixed-budget RAS 略高，却没有在 matched forgetting 和 ReachRate 上稳定赢过 `G2`。我现在的理解是，分得开不等于分得好，当前 router 可能没有对齐真正的 expert advantage。还不确定的是：G4 的问题是 router 选错，还是 experts 本身没有形成足够函数差异。下一步我想做 router-function audit 和 oracle routing upper bound，先判断 routing 线是否值得继续。
