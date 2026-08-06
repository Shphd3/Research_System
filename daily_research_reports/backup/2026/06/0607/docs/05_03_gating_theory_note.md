# 05_03 Gating Theory Note: Why Uniform Features Can Still Collapse

> 目的：给 05_03 anchor 提供最小理论支架。重点不是证明 collapse 的唯一根因，而是把“uniform data”“random initialization”“common direction”“top-1 lock-in”“expert utility”这些概念拆开，使每个 claim 可被实验裁定。

---

## 0. Current Bottom Line

```text
Uniform feature frequency does not imply uniform routing.
```

更精确地说：

```text
P(feature) uniform 只说明数据计数均匀；
不说明 router input hidden states h_f 是 zero-mean / isotropic；
不说明 router scores z_{f,e}=w_e^T h_f+b_e 对所有 expert exchangeable；
不说明 NTP objective 会强制 feature-level split。
```

当前最安全的理论判断：

```text
collapse 可能来自三层机制的叠加：
1. step-0 random geometry / finite-feature imbalance；
2. hidden-state common component c 被某个 router vector 或 bias 捕获；
3. top-1 / expert-responsibility training 把 early advantage 放大成 lock-in。
```

因此“初始化问题”与“Common 方向问题”不是互斥二选一。更合理的问题是：

```text
common component 是否已经在 step 0 产生 shared logit offset？
这个 offset 是否超过 random finite-sample expectation？
training 是否通过 selected-expert / utility feedback 放大它？
```

---

## 1. Basic Router Geometry

设 routing hidden state 为：

\[
h_f \in \mathbb{R}^d, \quad f \in \{1,\dots,F\}
\]

router 有 \(E\) 个 expert row：

\[
w_e \in \mathbb{R}^d, \quad b_e \in \mathbb{R}
\]

linear gate logit：

\[
z_{f,e} = w_e^\top h_f + b_e
\]

hard top-1 routing：

\[
e^*(f)=\arg\max_e z_{f,e}
\]

soft routing：

\[
g_e(h_f)=\frac{\exp(z_{f,e}/\tau)}{\sum_k \exp(z_{f,k}/\tau)}
\]

---

## 2. Random Geometry Baseline: Uniform Data Does Not Guarantee One Expert Per Feature

If \(h_f\) and \(w_e\) are independent isotropic random vectors and no bias exists, then by exchangeability:

\[
P(e^*(f)=e)=\frac{1}{E}
\]

For \(F\) operational features, the load vector is approximately:

\[
(n_1,\dots,n_E) \sim \mathrm{Multinomial}\left(F; \frac{1}{E},\dots,\frac{1}{E}\right)
\]

So:

\[
\mathbb{E}[n_e] = \frac{F}{E}, \quad
\mathrm{Var}(n_e)=F\frac{1}{E}\left(1-\frac{1}{E}\right)
\]

Important implication:

```text
Even under perfectly uniform random geometry, feature-to-expert assignment is not guaranteed to be balanced for finite F.
```

Example for \(F=4, E=4\), if assignments are iid uniform:

```text
P(perfect 1-1 split) = 4! / 4^4 = 24/256 = 9.375%
P(all 4 features choose same expert) = 4 / 4^4 = 1.5625%
P(max load >= 3) = 20.3125%
```

So random geometry can create imbalance. But if final hard collapse occurs far more often than this baseline, or if step-0 margins grow systematically during training, pure finite-sample random assignment is insufficient.

---

## 3. Common Direction Model

Decompose each feature centroid into common and residual parts:

\[
h_f = c + u_f
\]

where:

\[
c = \frac{1}{F}\sum_f h_f, \quad
\frac{1}{F}\sum_f u_f = 0
\]

Then router logit becomes:

\[
z_{f,e}=w_e^\top c + w_e^\top u_f + b_e
\]

Define shared expert offset:

\[
\delta_e = w_e^\top c + b_e
\]

Then:

\[
z_{f,e}=\delta_e + w_e^\top u_f
\]

Interpretation:

```text
The common component c contributes the same expert-specific offset δ_e to every feature.
If one expert has a larger δ_e, it gains a global advantage across many or all features.
```

A sufficient condition for expert \(j\) to win feature \(f\) against expert \(k\):

\[
\delta_j-\delta_k > (w_k-w_j)^\top u_f
\]

If \(j\)'s common-offset gap dominates the residual feature-specific term for many \(f\), then many features route to the same expert even though feature frequencies are uniform.

### Consequence

```text
Common direction is not a high-frequency feature in the data-count sense.
It is a shared component in hidden-state geometry.
```

It can arise even under uniform feature counts if the sequence template, position, shared tokens, embedding mean, residual stream, LayerNorm affine parameters, target-prediction position, or learned task representation create a nonzero hidden-state mean.

---

## 4. Bias Is A Degenerate Common Direction

If router has bias:

\[
z_{f,e}=w_e^\top h_f+b_e
\]

then \(b_e\) acts as a constant expert-specific offset for every feature. This is equivalent to appending a constant dimension to all inputs:

\[
\tilde h_f = [h_f; 1], \quad \tilde w_e=[w_e; b_e]
\]

Thus a random router bias can create common expert preference even if \(h_f\) is centered.

Audit implication:

```text
Router bias must be explicitly checked.
If bias=True and initialized randomly or updated early, it can be a direct lock-in source.
```

---

## 5. Why Training Can Amplify A Small Early Advantage

### 5.1 Soft Mixture Derivation

For a feature \(i\), let expert \(e\)'s probability of the correct next token be:

\[
R_{i,e}=P_e(y_i|x_i)
\]

With soft gate \(g_e(x_i)\), the predictive probability is:

\[
P(y_i|x_i)=\sum_e g_e(x_i)R_{i,e}
\]

Loss:

\[
L_i=-\log\sum_e g_e(x_i)R_{i,e}
\]

Define expert posterior responsibility:

\[
\rho_{i,e}=\frac{g_e(x_i)R_{i,e}}{\sum_k g_k(x_i)R_{i,k}}
\]

Then for gate logit \(z_e\):

\[
\frac{\partial L_i}{\partial z_e}=g_e(x_i)-\rho_{i,e}
\]

Gradient descent therefore moves:

```text
g_e upward when expert e's posterior responsibility ρ_{i,e} exceeds its gate probability;
g_e downward when ρ_{i,e} is below its gate probability.
```

Short statement:

```text
The gate learns expert responsibility / utility, not feature identity by itself.
```

### 5.2 When Does This Produce Split?

If different features have different best experts:

\[
\arg\max_e R_{i,e}
\]

then gate can split features.

If the same expert has high responsibility for multiple features, then gate has a training signal to route those features to the same expert:

```text
feature difference does not force routing difference;
utility difference is what creates routing difference.
```

### 5.3 Hard Top-1 And Lock-In

With hard top-1, only selected expert \(e^*(f)\) processes the token. Depending on implementation:

```text
- selected expert receives more data and gradient;
- non-selected experts may receive no expert gradient for those tokens;
- selected expert can become better on the selected region;
- router/inhibition/auxiliary updates may further increase its score;
- margin grows, so later correction becomes harder.
```

This explains why a small step-0 geometry advantage can become high-margin collapse after training.

---

## 6. Initialization Versus Common Direction: Decision Logic

The correct decision should not be framed as:

```text
Is collapse caused by initialization OR common direction?
```

Better framing:

```text
Does random initialization alone predict the observed step-0 load concentration?
Does hidden common component create a shared score offset beyond random baseline?
Does training amplify that initial/common offset into final lock-in?
```

### Possible Outcomes

| Observation | Interpretation | Next Decision |
|---|---|---|
| data not uniform or order not random | code/data construction issue | fix data before mechanism claim |
| router bias / init not as assumed | initialization implementation issue | rerun with corrected init |
| step-0 load within random geometry baseline; final collapse high | training amplification / top-1 lock-in | test warmup / load balance / delayed hard top-1 |
| step-0 full routing concentrated; residual-only routing balanced | common component strong candidate | run common-direction residual routing |
| residual routing still collapses | not only global common component | test utility / capacity / init / anti-lockin |
| orthogonal / centered / zero-bias router init reduces collapse | initialization geometry matters | develop better init method |
| residual routing reduces collapse without hurting accuracy | common-direction shortcut causally supported | refine intervention and boundary |

---

## 7. Minimal Metrics For Theory-To-Experiment Mapping

### Data / Representation

```text
count uniformity: count(s), count(i), count(r), count(s,i)
order randomness: batch entropy, autocorrelation, order hash
common norm: ||mean_f h_f|| / mean_f ||h_f||
variance explained by common direction / first PC
```

### Router Geometry

```text
full load: argmax_e w_e^T h_f
residual load: argmax_e w_e^T (h_f - proj_c h_f)
common score: w_e^T c + b_e
router row norms and pairwise cosine
step-0 margin distribution
random geometry p-value for observed max load
```

### Training Amplification

```text
load entropy over steps 0 / 10 / 20 / 50 / final
top-1 margin over steps
fraction top1 equals final dominant expert
alignment between selected router vector and common direction
expert gradient norm by expert
expert vector movement from init
```

---

## 8. Claim Boundary

Can claim after current evidence:

```text
- Uniform feature frequency does not by itself rule out collapse.
- Step-0/early geometry can identify the eventual collapse expert in bad seeds.
- Training can amplify small early bias into high-margin lock-in.
- Common hidden direction is a strong candidate mechanism.
```

Cannot claim yet:

```text
- Common direction is the unique or sufficient cause.
- Initialization alone fully explains collapse.
- Inhibition is always harmful.
- Router-chosen expert is utility-wrong.
- The same conclusion holds for compositional, Zipf, full LM, or real data.
```

---

## 9. Recommended Theoretical Statement For The Anchor

```text
The central theoretical hypothesis is not that uniform data should always yield uniform routing.
Instead, under linear gating, routing depends on hidden-state geometry and expert responsibility.
If hidden states contain a shared component c, then a router row with large w_e^T c + b_e gains a feature-independent logit advantage.
Hard top-1 training can then amplify this shared advantage because the selected expert receives more tokens and becomes increasingly responsible for them.
Therefore the root cause must be decomposed into: data/representation common component, random initialization baseline, and training-amplified lock-in.
```
