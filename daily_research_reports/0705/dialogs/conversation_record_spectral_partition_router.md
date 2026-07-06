# 对话记录：Uniform Feature Dispatch / Spectral Partition Router 研究线

生成时间：2026-07-05  
用途：开启新对话时作为上下文压缩文件。  
范围：过滤冗余情绪与重复讨论，仅保留研究问题、理论、实验、代码路径、结论边界、下一步计划。

---

## 0. 一句话总览

我们最初从导师要求的“最简单数学 case：feature / spectral space 均匀时，能否把 feature 均匀分到 experts”出发。经过 V1、V2、V2.1 三轮迭代，当前问题已经从“证明均匀分发的几何充分条件”演化为：

> 在 spectrally normalized route-relevant feature space 中，构造一个 non-cheating router，使其同时满足 **equal mass、feature coherence、training preservation**。

当前最重要的判断：

> V2 基本解决了 equal-mass feature dispatch，但没有完整解决“好的路由”。V2.1 是下一步：geometry-aware, margin-preserved dispatch。

---

## 1. 导师录音中的原始任务

导师录音大意：

1. 短程 next-token prediction 下，例如 `ABCAB -> C`，hidden feature 本身通常不是均匀的，奇异值也可能不均匀。
2. 但是导师要求先完成一个最简单数学 case：
   - 假设 feature 表征空间均匀；
   - 假设 spectral space 均匀；
   - 在这个 case 中给出理论证明和实验结果；
   - 非均匀谱、大奇异值情形后续再做。
3. 导师提到的 MPI / expert singular direction intuition 本质上是：router row 可以作为 expert proxy，expert 的最大奇异方向可以作为 expert-side center。
4. 导师的目标不是让我们马上解决真实 LM hidden states，而是先把“均匀 case”完全理解、定义清楚、闭环掉。

我们对这个任务的操作化理解逐步变成：

> “均匀地把 feature 分给 experts”本身需要定义。我们需要自己定义目标、指标、non-cheating 标准，并在该定义下给出方法与实验。

---

## 2. V1：Uniform Feature Routing in Controlled Top-1 MoE

### 2.1 文件路径

```text
papers/uniform_feature_moe_initialization/latex/paper.tex
papers/uniform_feature_moe_initialization/exp/
```

### 2.2 V1 的问题定义

V1 研究的是强几何设定：

```text
spherical feature directions + equal-measure expert prototype cells
=> uniform top-1 expert usage
```

即：

- token feature direction：
  \[
  z \sim \mathrm{Unif}(\mathbb S^{d-1})
  \]
- expert prototype cells 等测度；
- top-1 routing：
  \[
  a(z)=\arg\max_e \langle z,u_e\rangle
  \]
- 则：
  \[
  \Pr(a(z)=e)=1/E
  \]

### 2.3 V1 的主要理论

1. **Equal-measure cells sufficient condition**：球面均匀 feature + 等测度 cells => expert usage 期望均匀。
2. **Regular simplex corollary**：若 expert prototypes 是 regular simplex，则 cells 等测度。
3. **Finite-token decomposition**：
   \[
   \widehat p_e-1/E=(p_e-1/E)+(\widehat p_e-p_e)
   \]
   第一项是 prototype-cell geometry error，第二项是 sampling noise。
4. **Covariance isotropy 不等于 directional uniformity**：谱均匀只是二阶诊断。
5. **Whitening proposition**：在 elliptical toy family 中，population whitening 可以恢复 spherical directions。
6. **MPI / expert SVD 的位置**：expert singular directions 是 candidate centers，不是 balance guarantee。

### 2.4 V1 实验主线

- uniform sphere + prototype geometry；
- random prototype geometry floor；
- expert spectral prototypes as centers, not balance guarantees；
- covariance-isotropy counterexample；
- elliptical whitening recovery；
- balanced assignment 作为 non-geometric control。

### 2.5 V1 的结论边界

V1 是一个强特殊 case。它回答：

> 如果 token directions spherical uniform，且 expert prototype cells 等测度，那么 top-1 routing 期望均匀。

它没有回答：

- 标准 expert initialization 是否天然给出好 prototypes；
- 只给 covariance isotropy 是否足够；
- 如何构造一个更一般的 router；
- 训练中是否保持。

---

## 3. 从 V1 到 V2 的问题转变

我们发现：导师说“feature 谱均匀 / 空间均匀”，并不意味着“任意 router 自动均匀”。我们真正想要的是一个构造问题：

> 给定 spectrally uniform features，能否构造一个 non-cheating router，使 feature 均匀 dispatch 到 experts？

于是 V2 把目标定义为：

## Uniform Feature Dispatch

给定：

\[
X\in \mathbb R^d
\]

router：

\[
g:\mathbb R^d\to\{1,\dots,E\}
\]

cells：

\[
C_e=\{x:g(x)=e\}
\]

目标：

\[
P(C_e)=P(g(X)=e)=1/E
\]

这不是 batch-level load balancing，而是 feature distribution 的 equal-probability partition。

### Non-cheating 标准

允许：

- unlabeled calibration features；
- feature mean / covariance；
- projection quantiles；
- unsupervised locality objectives；
- model-internal expert weights；
- expert spectral prototypes from SVD / MPI。

禁止：

- feature labels during router construction；
- task labels / next-token answers；
- evaluation labels；
- current-batch expert counts；
- balanced assignment 作为主方法。

---

## 4. V2：Spectral Partition Routing

### 4.1 文件路径

```text
papers/spectral_partition_router_v2/latex/paper.tex
papers/spectral_partition_router_v2/exp/src/synthetic_suite.py
papers/spectral_partition_router_v2/exp/run_*.py
papers/spectral_partition_router_v2/exp/results/
papers/spectral_partition_router_v2/latex/tables/
papers/spectral_partition_router_v2/latex/figures/
```

### 4.2 V2 方法：SPR

核心思想：

```text
route-relevant features
→ spectral normalization
→ recursive quantile partition
→ equal-mass feature cells
→ each cell assigned to one expert
```

每个 node 中：

- 当前 expert set：\(\mathcal E_\mathcal N\)
- 左右专家组：\(\mathcal E_L, \mathcal E_R\)
- 目标比例：
  \[
  \rho_\mathcal N=\frac{|\mathcal E_L|}{|\mathcal E_\mathcal N|}
  \]
- 投影：
  \[
  T=q_\mathcal N^\top \tilde X
  \]
- 阈值：
  \[
  \tau_\mathcal N=F_\mathcal N^{-1}(\rho_\mathcal N)
  \]

递归切到每个 leaf 一个 expert。

### 4.3 V2 方法变体

- `SPR-Fixed`：当前代码中其实是 seeded random axis，不是真正 fixed orthogonal basis。
- `SPR-Local`：在候选方向中选择 within-cell variance 最低的方向。
- `SPR-Expert`：使用 expert weights / expert spectral prototypes 选择切分方向。
- `Frozen-SPR`：固定 tree。
- `SPR-init-linear`：用 SPR cell centers 初始化 linear router。
- `SlowUpdate-SPR`：定期重估 tree；当前实验中是负结果。

### 4.4 V2 主要理论

1. **Node quantile split**：连续 CDF 情况下，quantile split 给指定质量。
2. **Recursive uniform dispatch**：按 expert 数比例递归切，leaf mass 为 \(1/E\)。
3. **Not capacity assignment**：校准后 router 是固定函数 \(g(x)\)，不看当前 batch counts。
4. **Finite calibration error**：holdout balance 依赖 calibration size 和 distribution shift。
5. **Expert weights role**：expert weights choose geometry，quantiles provide mass。

### 4.5 V2 实验结果摘要

#### E1 Static equal-mass dispatch

结果：

- best SPR mean held-out LoadCV：0.0340；
- vanilla random linear routing：0.0855。

含义：

> Equal-mass dispatch 基本有效；calibration exact，holdout 有有限样本误差。

#### E2 Spectrally flat but non-spherical

结果：

- whitened non-spherical datasets condition number = 1.000；
- prototype-only routing mean held-out LoadCV = 0.3076；
- best SPR mean held-out LoadCV = 0.0619。

含义：

> covariance flatness 不保证 prototype-router balance；quantile calibration 才控制 mass。

边界：Paired-directions 中 SPR LoadCV 仍有 0.18–0.21，说明 finite support / near ties / calibration-holdout mismatch 是问题。

#### E3 Expert-weight-guided partition

结果：

- SPR-Expert mean held-out LoadCV = 0.0180；
- prototype-only top-1 = 0.1106；
- SPR-Expert cell-to-prototype alignment = 0.8955。

含义：

> expert weights can guide geometry，quantiles control mass。

但这是 conditional：当前 expert weights 是 synthetic 构造，含 useful principal directions。

#### E4 Feature partition quality

结果：

| Method | LoadCV | NMI |
|---|---:|---:|
| Balanced assignment | 0.000 | 0.007 |
| SPR-Fixed | 0.019 | 0.031 |
| SPR-Local | 0.021 | 0.034 |
| SPR-Expert | 0.015 | 0.233 |

含义：

> Equal-mass 不等于 meaningful feature partition。SPR-Fixed / Local 基本没有恢复 latent feature structure。SPR-Expert 在 expert weights aligned 时显著更好。

#### E5 Controlled hard-routing expert training

结果：

| Router | Val MSE | LoadCV | NMI | Flip |
|---|---:|---:|---:|---:|
| SPR-Expert | 9.030 | 0.047 | 0.385 | 0.024 |
| Vanilla linear | 12.613 | 0.107 | 0.087 | 0.023 |
| Frozen-SPR | 12.472 | 0.050 | 0.077 | 0.025 |
| SPR-init-linear | 11.558 | 0.053 | 0.179 | 0.020 |
| SlowUpdate-SPR | 17.432 | 0.053 | 0.096 | 0.888 |

含义：

- SPR-Expert 是正结果；
- SlowUpdate-SPR 是负结果；
- naive recalibration 不安全；
- 当前 E5 不是完整 learned-router MoE training，只是 controlled hard-routing expert training。

### 4.6 V2 实现审核问题

必须注意：

1. `svd_prototypes` 存在 SVD sign ambiguity；需要 projective prototypes \(P_e=v_ev_e^T\) 或 deterministic orientation。
2. `SPR-Fixed` 实际是 random-axis，应改名或实现 true fixed basis。
3. 离散 / atom-supported data 需要 feature-derived tie handling。
4. `Linear + load-balance` 实际是 BalancedAssignment，不是 auxiliary loss baseline。
5. 当前 E5 没有训练 router，本质是 hard-routing expert training audit。
6. `clustered` prototype 设置不够明显，spread metric 不能区分 clustered / random / symmetric。

### 4.7 V2 结论

V2 已经回答：

> Can we non-cheatingly construct equal-mass feature dispatch in a controlled spectrally uniform setting?

答案：

> Yes, under continuous / stable calibration assumptions, recursive quantile routing solves this.

但 V2 没有完全回答：

> Can we construct a generally good router whose feature partition is meaningful and preserved through training?

答案：

> Not yet. 需要 expert-weight alignment、feature clusterability、low boundary mass、margin-preserving dynamics。

---

## 5. V2.1：Geometry-Aware Spectral Partition Routing

### 5.1 新文件夹

已创建：

```text
papers/spectral_partition_router_v2_1/
```

核心文件：

```text
papers/spectral_partition_router_v2_1/README.md
papers/spectral_partition_router_v2_1/PROBLEM_STATEMENT.md
papers/spectral_partition_router_v2_1/METHOD_AND_THEORY_NOTES.md
papers/spectral_partition_router_v2_1/NOTES_ON_RELATION_TO_V1_V2.md
papers/spectral_partition_router_v2_1/latex/paper.tex
papers/spectral_partition_router_v2_1/exp/EXPERIMENT_PLAN.md
papers/spectral_partition_router_v2_1/exp/CODEX_TASKS.md
papers/spectral_partition_router_v2_1/exp/TABLE_TEMPLATES.md
papers/spectral_partition_router_v2_1/exp/IMPLEMENTATION_AUDIT_CHECKLIST.md
```

注意：scaffold 过程中额外生成了一些 marker/note 文件，可忽略或后续清理。

### 5.2 V2.1 核心目标

V2.1 不再满足于 equal mass，而是定义“好的 dispatch”为三层：

```text
equal mass + feature coherence + margin-based preservation
```

即：

1. Equal mass：
   \[
   P(g(X)=e)=1/E
   \]
2. Feature coherence：如果存在 latent feature structure，route 要保留这种结构。
3. Preservation：训练 / drift 后 route 不应轻易变化。

### 5.3 V2.1 方法：GA-SPR

全名：

```text
Geometry-Aware Spectral Partition Routing
```

核心 slogan：

```text
Quantiles give mass.
Geometry gives feature meaning.
Margins give preservation.
```

方法分层：

1. **Mass layer**：recursive quantile split，保证 equal mass。
2. **Geometry layer**：split directions 由 local geometry 或 expert weights 指导。
3. **Preservation layer**：margin-aware updates / hysteresis / route-change budget。

### 5.4 V2.1 理论组件

#### Theorem 1：Recursive quantile dispatch

如果每个 node 按 child expert counts 比例切 mass，则最终每个 leaf mass = \(1/E\)。

#### Proposition 2：Atom impossibility

如果存在 atom：

\[
P(X=x_0)>1/E
\]

那么 deterministic feature-only router 不可能精确 equal mass，同时保持 identical features 同 route。

#### Proposition 3：Projected-separation coherence

如果方向 \(q\) 能以误差 \(\varepsilon\) 分开 latent groups，则该 split 与 latent grouping 的 disagreement 至多 \(\varepsilon\)。

#### Proposition 4：Expert-direction perturbation

如果 expert-guided direction 与 ideal feature-separating direction 距离 \(\delta\)，且 feature norm 有界 \(R\)，则 disagreement 只可能发生在 ideal margin \(\le \delta R\) 的样本上。

#### Theorem 5：Margin preservation

如果 drift 满足：

\[
\|\Delta X\|_2 < m_{\mathrm{tree}}(X)
\]

则 route 不变。

### 5.5 V2.1 mild assumptions

V2.1 不再只假设 covariance isotropy。它明确测试 mild assumptions：

1. globally spectrally normalized features；
2. local clusterability / feature coherence；
3. expert weights aligned with feature geometry；
4. low boundary mass；
5. bounded feature drift。

这是比 V1 更一般、比 V2 更可解的中间设定。

---

## 6. V2.1 实验方案

文件：

```text
papers/spectral_partition_router_v2_1/exp/EXPERIMENT_PLAN.md
```

### E1 Equal-mass sanity

目的：确认修正后的 quantile routing 仍能 equal mass。

方法：

- Vanilla linear；
- Simplex；
- SPR-RandomAxis；
- SPR-FixedBasis；
- GA-SPR-Local；
- GA-SPR-Expert；
- Balanced assignment control。

指标：LoadCV, max error, gap, tie rate, margin p05。

### E2 Assumption ladder

数据 regime：

1. Isotropic unstructured；
2. Isotropic clusterable；
3. Expert-aligned isotropic；
4. Low-margin / overlapping。

目的：明确哪些条件对 feature coherence 必要。

### E3 Expert-guided geometry after sign fix

重点：修复 SVD sign ambiguity 后测试 expert weights 是否提供有效 geometry。

需要：

- projective prototypes；
- prototype spread diagnostics；
- expert alignment / NMI / LoadCV。

### E4 Margin-aware update vs naive update

对比：

- Frozen GA-SPR；
- Naive SlowUpdate；
- Margin-aware update；
- Hysteresis update；
- Route-budget update。

指标：flip rate, margin p05, accepted updates, val loss。

### E5 Controlled training with true baselines

要求加入真正的：

- trainable linear top-1；
- trainable linear + load-balancing auxiliary loss；
- GA-SPR-init-linear + route-preservation regularizer。

### E6 Failure modes

测试：

- no latent structure；
- large atoms；
- random expert weights；
- high drift + low margin；
- calibration / holdout shift。

每个失败都要对应 violated assumption。

---

## 7. 给下一轮对话的当前状态

当前 V2.1 是 scaffold 状态：

- paper 已写；
- theory 已写；
- experiment protocols 已写；
- Codex tasks 已写；
- 没有结果；
- 不应在 paper 中写实验数字。

下一轮建议从以下问题开始：

1. 是否接受 V2.1 的三层 good dispatch 定义？
   ```text
   equal mass + feature coherence + preservation
   ```
2. 是否将 GA-SPR-Expert 作为主正方向？
3. 是否先让 Codex 实现 E1–E3，而不是直接跑训练？
4. 如何实现 projective expert prototypes？
5. 如何设计 margin-aware update？
6. 是否清理 V2.1 scaffold 中多余 marker 文件？

---

## 8. 当前最重要的研究判断

### 不要再说

> “谱均匀就能好地分发。”

### 应该说

> “谱归一化去除了各向异性，但 good dispatch 还需要 feature structure / expert alignment / margin preservation。”

### 当前主假设应为

```text
Globally isotropic but locally structured features
+ optional expert-weight alignment
+ low boundary mass
+ bounded drift
```

### 当前方法假设

```text
Quantiles solve equal mass.
Expert/local geometry solves coherence if structure exists.
Margins solve preservation if drift is bounded.
```

---

## 9. 推荐新对话开场提示

可以在新对话中直接粘贴：

```text
我们现在讨论 papers/spectral_partition_router_v2_1。
V1 解决 spherical + equal-measure prototype cells 的强特殊 case。
V2 用 recursive quantile routing 基本解决 equal-mass feature dispatch，但发现 equal mass 不等于 meaningful feature partition，也不保证 training preservation。
V2.1 已经创建 scaffold，目标是 equal mass + feature coherence + margin-based preservation。
请从 PROBLEM_STATEMENT.md 和 latex/paper.tex 开始，帮我审查 V2.1 的问题定义、理论严谨性、实验可执行性，并规划 Codex 实现 E1–E3。
```

---

## 10. 关键词表

| 术语 | 含义 |
|---|---|
| uniform feature dispatch | feature cells 概率质量相等：\(P(C_e)=1/E\) |
| non-cheating router | 不用 labels / task targets / current-batch counts，只用 feature stats 和可选 expert weights |
| SPR | Spectral Partition Routing，递归分位数路由 |
| GA-SPR | Geometry-Aware SPR，加入 local / expert geometry 和 margin preservation |
| equal mass | 每个 expert 接收等概率 feature mass |
| feature coherence | 路由与 latent feature structure 对齐 |
| preservation | 训练或 drift 后路由保持稳定 |
| margin p05 | route margin 的 5% 分位数，衡量低尾稳定性 |
| atom impossibility | 大质量 identical feature atom 使 deterministic exact equal dispatch 不可能 |
| projective prototype | \(P_e=v_ev_e^T\)，解决 SVD 符号歧义 |
| expert alignment | expert weight principal directions 与 feature geometry 相关 |

---

## 11. 最后提醒

- V2.1 是新研究主线，不是简单补实验。
- 后续任何 claim 都必须映射到三层目标之一：mass / coherence / preservation。
- 负结果很重要，尤其是：无结构 isotropic data、random expert weights、low-margin high-drift。
- 不要把 balanced assignment 当主方法。
- 不要把 current V2 E5 称为完整 MoE training dynamics，除非实现了 trainable router。
