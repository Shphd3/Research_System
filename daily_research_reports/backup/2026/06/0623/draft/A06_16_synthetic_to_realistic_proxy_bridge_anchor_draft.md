---
anchor_id: A06_16_synthetic_to_realistic_proxy_bridge
parent_node: rq.feature_specialization.initialization_geometry
status: draft_for_review
created: 2026-06-23
canonical_language: en
---

# A06_16 Synthetic-To-Realistic Proxy Bridge Anchor Draft

## 0. researcher judgment record

父问题：在 uniform feature 分布下，dot-product top-1 MoE 的初始化能否形成并保持 feature-level specialization。

当前子问题：A06_08/A06_09 在干净 synthetic setting 中成功，但 real-DCLM proxy routing 训练早期失败。下一步不应直接修 DCLM，而应先在可控 synthetic setting 中逐步削弱 feature proxy，判断 pseudo-center 初始化在哪个机制轴上失效。

当前判断：real-DCLM 失败是 observation，不是 physical prior。新的 physical prior 是：pseudo-center 初始化依赖两个条件——hidden residual 中有可恢复的 feature centers，并且训练早期梯度不会快速抹掉这些 centers 的 routing margin。

下一步决策：先做 controlled bridge：从 clean synthetic feature 走向 weaker / noisier proxy feature，再决定是否回到 DCLM preservation 或转向 anti-lockin。

---

## 1. Decision Card

**Question:**
Does the A06_08/A06_09 pseudo-center initialization remain valid when the clean synthetic feature proxy is weakened toward a more realistic setting?

**Physical prior:**
Feature-aligned initialization works only when residual hidden states contain recoverable feature centers and early training does not erase their routing margin.

**Minimal model:**
\[
h_i = c + \mu_{f_i} + \eta_i,
\qquad
w_e = \alpha \cdot \mathrm{normalize}(\hat\mu_e),
\qquad
z_{i,e}=w_e^\top(h_i-c).
\]

Here \(\mu_{f_i}\) is the feature-related residual center, and \(\eta_i\) is context / position / nuisance variation.

**Model terms being tested:**
1. recoverability of \(\mu_f\) from unlabeled residual hidden states;
2. nuisance scale \(\eta_i\) relative to feature separation;
3. early training drift of \(W_t\) and \(h_t\).

**Primary metric:**
feature_NMI / proxy_NMI, read with load imbalance \(L\), margin, and task accuracy.

**Falsifier:**
If pseudo-centers no longer recover feature_NMI under a mild weakening that oracle centers still solve, then current label-free discovery is not robust enough. If pseudo-centers recover step-0 routing but training destroys it, the next mechanism is preservation / anti-lockin, not discovery.

**Can claim if supported:**
Pseudo-center initialization survives a controlled move from clean synthetic feature to weaker synthetic proxy.

**Cannot claim:**
Real DCLM specialization, semantic feature discovery, expert utility, or final deployable gating.

---

## 2. Problem Definition

A06_08 showed that route-position residual k-means can recover clean four-feature centers without labels. A06_09 showed that those pseudo-centers preserve feature routing under the current route-position target prediction training.

The real-DCLM proxy line found a different outcome: proxy clusters can be measured, proxy centers can initialize routing, but ordinary DCLM training quickly destroys proxy routing.

The immediate problem is therefore not “how to fix DCLM router training.” The immediate problem is narrower:

**Which assumption between clean synthetic success and real-DCLM failure breaks first?**

This anchor tests that break point under controlled synthetic-to-realistic proxy shifts.

Not in scope:
real text claim, utility binding, full router method, or anti-lockin intervention as the main experiment.

---

## 3. Physical Priors

**P1: Feature discovery requires residual cluster structure.**

Meaning: after common-centering, samples with the same feature should form a recoverable cluster or center in route-position residual space.

Could be wrong if: oracle labels reveal a feature partition but label-free residual clustering cannot recover it even under mild nuisance variation.

**P2: Route-position discovery may be easier than all-position discovery.**

Meaning: the routed position may contain the cleanest feature signal. Clustering all hidden states may mix feature, position, and context factors.

Could be wrong if: all-position clustering recovers the same feature centers without degrading NMI or increasing nuisance alignment.

**P3: Training preservation depends on margin against nuisance drift.**

Meaning: pseudo-center routing survives if the feature margin remains larger than early changes in router rows and hidden states.

Could be wrong if: high step-0 NMI and margin still collapse immediately under ordinary training.

---

## 4. Mathematical Model
Hidden decomposition:

\[
h_i = c + r_i,
\qquad
r_i = \mu_{f_i} + \eta_i.
\]

Pseudo-center discovery:

\[
\hat\mu_1,\ldots,\hat\mu_K = \mathrm{Cluster}(r_i),
\qquad
w_e = \alpha\frac{\hat\mu_e}{\|\hat\mu_e\|}.
\]

Routing:

\[
a_i = \arg\max_e w_e^\top r_i.
\]

Training drift readout:

\[
z_{i,e}^{(t)} = W_e^{(t)\top} h_i^{(t)}.
\]

Key diagnostic quantities:

\[
\mathrm{feature\_NMI}(f_i,a_i),
\quad
L=m\max_e|p_e-1/m|,
\quad
\mathrm{margin}_i=z_{i,a_i}-\max_{j\ne a_i}z_{i,j}.
\]

---

## 5. Minimal Tests

### Test 1: Discovery scope guard

**Question:**
Is feature discovery specific to route-position hidden states, or can it survive all-position hidden-state clustering?

**Conditions:**
1. route-position residual clustering;
2. all-position residual clustering;
3. all-position clustering with route-position evaluation;
4. oracle feature centroid upper bound.

**Primary read:**
feature_NMI / proxy_NMI on held-out route-position samples.

**Decision:**
If all-position clustering fails while route-position clustering succeeds, the current method requires a defined route position and cannot yet be treated as general language feature discovery.

---

### Test 2: Controlled proxy weakening

**Question:**
How much nuisance variation can pseudo-center discovery tolerate before it loses the oracle partition?

**Weakening axes:**
1. add feature-irrelevant context variation;
2. add decoy tokens correlated with position but not feature;
3. reduce feature signal strength in hidden states;
4. allow multiple feature-like factors per sequence while keeping evaluation labels known.

**Controls:**
random router, calibration mean, residual k-means, spherical residual k-means, oracle centroid.

**Primary read:**
feature_NMI, load \(L\), margin, and nuisance NMI.

**Decision:**
If oracle still succeeds but pseudo discovery fails, the next problem is label-free discovery robustness. If both fail, the synthetic proxy no longer contains a recoverable feature partition.

---

### Test 3: Preservation only after discovery passes

**Question:**
If pseudo-centers recover step-0 routing under a weakened proxy, does training preserve it?

**Conditions:**
1. random Gaussian init;
2. equal-norm random init;
3. residual k-means pseudo init;
4. oracle centroid init.

**Primary read:**
feature_NMI trajectory, NMI drop, load \(L\), margin trajectory, target accuracy.

**Decision:**
If pseudo init starts high and collapses while oracle remains stable, pseudo-center quality is insufficient. If both pseudo and oracle collapse, training feedback / anti-lockin becomes the next mainline.

---

## 6. Evidence Boundary From Prior Work

Current supported facts:

1. Oracle feature centroids can produce perfect feature routing in the clean synthetic hidden-state setting.
2. Global common-centering / projection / whitening improves load but does not recover feature specialization.
3. Route-position residual k-means recovers pseudo-feature centers in the clean synthetic setting.
4. Pseudo-center initialization is preserved under the current route-position target prediction objective.
5. Real-DCLM proxy routing is measurable and linearly initializable, but ordinary DCLM training does not preserve it.

Interpretation:
The clean synthetic line is not complete enough to jump directly to DCLM method repair. The controlled bridge should identify which assumption breaks: discovery, route-position specificity, proxy noise, or training preservation.

---

## 7. Claim Boundary And Next Decision

**Can claim after this anchor only if supported:**
The pseudo-center initialization route survives a specific controlled weakening of the synthetic feature proxy.

**Cannot claim:**
Real-language semantic feature discovery, full next-token training stability, causal expert utility, or a final gating method.

**Next decision after results:**
- If discovery fails first: improve label-free feature discovery or redefine proxy.
- If preservation fails after discovery succeeds: move to training preservation / anti-lockin audit.
- If both discovery and preservation hold: proceed to a more realistic proxy or real-DCLM audit with a pre-defined proxy metric.
