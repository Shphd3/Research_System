# Mini Anchor: Margin-Budget Preservation for Feature-to-Expert Gating

**Status:** Draft v0.1 for review  
**Anchor family:** A06 preservation  
**Short name:** `A06_preservation_margin_budget`  
**Core decision:** Can early-training preservation be modeled as a margin-budget problem?

---

## 0. researcher judgment record

### Phenomenon

A feature-to-expert partition can be constructed at step 0 by using feature/proxy centers to initialize the router. However, after early training, the route assignment may degrade: route NMI drops, feature-to-expert specialization weakens, or routing collapses into a small set of experts.

### Mechanism Guess

The step-0 route assignment is preserved only if its initial routing margin is large enough to absorb the relative movement of:

1. **feature centers**: hidden-state cluster means during training;
2. **router rows**: expert scoring vectors during training;
3. **common/dense directions**: shared components that attract router decision regions.

### Key Variables

- **特征中心（feature center）**  
  $$
  \mu_f(t)=\mathbb{E}[h_i(t)\mid y_i=f]
  $$
  where $y_i=f$ is a fixed feature/proxy label.

- **路由行向量（router row）**  
  $$
  w_e(t)
  $$
  the linear scoring vector for expert $e$.

- **初始特征到专家指派（initial feature-to-expert assignment）**  
  $$
  a(f)=\arg\max_e w_e(0)^\top \mu_f(0)
  $$

- **成对边际（pairwise margin）**  
  $$
  \gamma_{f,e}(t)=\bigl(w_{a(f)}(t)-w_e(t)\bigr)^\top \mu_f(t),
  \quad e\neq a(f)
  $$

- **最小边际（minimum margin）**  
  $$
  \Gamma(t)=\min_f\min_{e\neq a(f)}\gamma_{f,e}(t)
  $$

- **保持性（preservation）**  
  Step-0 assignment remains valid at step $t$ if most $\gamma_{f,e}(t)$ remain positive and proxy-route NMI remains high.

### Causal Relation

If:

$$
\Gamma(0) > \text{training-induced drift budget},
$$

then feature-to-expert routing is expected to be preserved.

If:

$$
\Gamma(0) \leq \text{training-induced drift budget},
$$

then some margins flip sign, route assignments change, and proxy-route NMI drops.

### Observable Metrics

- initial minimum margin: $\Gamma(0)$
- feature center drift: $\|\mu_f(t)-\mu_f(0)\|$
- router gap drift: $\|u_{f,e}(t)-u_{f,e}(0)\|$, where $u_{f,e}=w_{a(f)}-w_e$
- margin consumption ratio: drift budget / initial margin
- sign flip rate: fraction of $\gamma_{f,e}(t)<0$
- proxy-route NMI at step 5/10
- LM loss guard

### Alternative Explanations

1. Proxy labels are unstable; preservation fails because the feature object itself is not stable.
2. Step-0 router bridge is weak; preservation fails because initialization never truly aligned.
3. Feature centers drift too much; preservation requires tracking hidden-state movement.
4. Router rows drift toward common/dense direction; preservation fails due to router-side early lock-in.
5. Expert feedback or optimizer geometry destroys assignment even when center/router drift is small.
6. Margin is only correlated with success, not causal.

### Decision Rule

This anchor is useful only if the margin-budget model changes the next decision:

- If margin consumption predicts NMI drop, prioritize anti-drift / anti-lock-in interventions.
- If margin consumption does not predict NMI drop, park margin as a secondary diagnostic and search for another preservation mechanism.

---

## 1. Problem Definition

### Parent Question

Can top-1 MoE gating form a stable, interpretable, and useful feature-level expert partition?

### Current Subquestion

Given a step-0 feature-to-expert partition produced by feature/proxy-center router initialization:

> Can the partition survive early training, and what determines whether it survives?

### Specific Question For This Anchor

> Is early-training preservation governed by a margin budget: the initial routing margin must exceed the feature-center and router-boundary drift accumulated during training?

### Why This Is Not Just A Debugging Question

A route NMI drop by itself says that specialization failed, but not why. This anchor attempts to turn preservation failure into a decomposable geometric condition:

$$
\text{preservation failure}
=
\text{initial margin exhausted by drift}.
$$

If valid, it gives a quantitative bridge from local diagnostics to a mechanism-level explanation.

---

## 2. Physical Priors

### Prior 1: Top-1 routing is decision-region assignment

For a dot-product router, expert $e$ wins for hidden state $h$ when:

$$
w_e(t)^\top h > w_j(t)^\top h,\quad \forall j\neq e.
$$

Thus the router partitions hidden-state space into decision regions. Collapse does not require hidden states to collapse; it is enough that router decision regions assign many hidden states to the same expert.

### Prior 2: Feature information and common information coexist

For a feature $f$, write its center as:

$$
\mu_f(t)=c(t)+r_f(t),
$$

where:

- $c(t)$ is a shared common/dense component;
- $r_f(t)$ is the feature-specific residual component.

A router can fail even if $r_f(t)$ still contains feature information, if the decision boundary becomes aligned with $c(t)$ rather than the residual directions.

### Prior 3: Training moves both hidden states and router rows

During training:

$$
\mu_f(t)=\mu_f(0)+\Delta\mu_f(t),
$$

$$
w_e(t)=w_e(0)+\Delta w_e(t).
$$

Therefore preservation is a coupled geometry problem. It depends not only on feature-center movement and not only on router-row movement, but on their relative effect on margins.

### Prior 4: Initial alignment is insufficient without margin

A step-0 assignment can be correct but fragile. If the score gap between the assigned expert and its competitors is small, a small movement in either hidden centers or router rows can flip the assignment.

---

## 3. Falsifiable Hypotheses

### H1: Margin-buffer hypothesis

Successful preservation requires initial margins to exceed the drift budget.

**Prediction:** successful seeds/conditions have lower margin consumption ratio:

$$
R(t)=\frac{\text{drift budget}(t)}{\Gamma(0)}.
$$

When $R(t)<1$, proxy-route NMI should be higher. When $R(t)>1$, sign flips and NMI drop should be more likely.

**Falsifier:** NMI collapses even when $R(t)\ll 1$, or NMI remains high even when $R(t)\gg 1$, across seeds/conditions.

---

### H2: Router-side early-lock-in hypothesis

Preservation fails because router decision boundaries drift toward common/dense directions rather than following feature residual directions.

**Prediction:** feature centers remain relatively stable, but router rows or pairwise gaps show increased alignment with the common direction $c(t)$. Sign flips are dominated by:

$$
\Delta u_{f,e}(t)^\top \mu_f(0),
$$

where:

$$
u_{f,e}(t)=w_{a(f)}(t)-w_e(t).
$$

**Falsifier:** router rows remain stable, common alignment does not increase, but NMI still collapses.

---

### H3: Feature-center drift hypothesis

Preservation fails because the feature centers themselves move away from the initial router assignment.

**Prediction:** sign flips are dominated by:

$$
u_{f,e}(0)^\top\Delta\mu_f(t).
$$

Successful conditions either show smaller $\|\Delta\mu_f(t)\|$ or use a tracking mechanism that updates router rows with the moving centers.

**Falsifier:** $\Delta\mu_f(t)$ is small and not aligned with margin reduction, yet NMI drops.

---

### H4: Margin intervention hypothesis

Artificially shrinking or removing the initial margin should lower preservation, even if step-0 assignment is initially unchanged.

**Prediction:** margin shrink/removal reduces proxy-route NMI at step 5/10 and increases sign flip rate.

**Falsifier:** margin shrink/removal does not affect NMI or sign flip rate after controlling for loss, load, and initialization assignment.

---

## 4. Mathematical Model

### 4.1 Initial Assignment

Let $F$ be the set of feature/proxy labels and $E$ be the set of experts.

For each feature $f$, define its step-0 assigned expert:

$$
a(f)=\arg\max_{e\in E} w_e(0)^\top \mu_f(0).
$$

This assignment is the target partition to preserve.

### 4.2 Pairwise Router Gap

For each competitor $e\neq a(f)$, define:

$$
u_{f,e}(t)=w_{a(f)}(t)-w_e(t).
$$

This is the pairwise decision-boundary vector between the assigned expert and a competitor.

### 4.3 Pairwise Margin

The center-level pairwise margin is:

$$
\gamma_{f,e}(t)=u_{f,e}(t)^\top \mu_f(t).
$$

If:

$$
\gamma_{f,e}(t)>0,\quad \forall e\neq a(f),
$$

then the feature center $\mu_f(t)$ is still assigned to the original expert $a(f)$.

The minimum center margin is:

$$
\Gamma_{\mathrm{center}}(t)=\min_f\min_{e\neq a(f)} \gamma_{f,e}(t).
$$

### 4.4 Cluster-Aware Margin

For individual hidden states:

$$
h_i(t)=\mu_f(t)+\epsilon_i(t),\quad y_i=f.
$$

Then:

$$
u_{f,e}(t)^\top h_i(t)
=
\gamma_{f,e}(t)+u_{f,e}(t)^\top\epsilon_i(t).
$$

If $\|\epsilon_i(t)\|\leq \rho_f(t)$, then:

$$
u_{f,e}(t)^\top h_i(t)
\geq
\gamma_{f,e}(t)-\|u_{f,e}(t)\|\rho_f(t).
$$

Define cluster-aware margin:

$$
\tilde{\gamma}_{f,e}(t)
=
\gamma_{f,e}(t)-\|u_{f,e}(t)\|\rho_f(t).
$$

A stronger sufficient condition for all tokens in feature $f$ to preserve assignment is:

$$
\tilde{\gamma}_{f,e}(t)>0,\quad \forall e\neq a(f).
$$

In practice, $\rho_f(t)$ should use a robust quantile radius rather than a max radius.

### 4.5 Margin Dynamics

Let:

$$
\Delta u_{f,e}(t)=u_{f,e}(t)-u_{f,e}(0),
$$

$$
\Delta\mu_f(t)=\mu_f(t)-\mu_f(0).
$$

Then:

$$
\gamma_{f,e}(t)
=
\bigl(u_{f,e}(0)+\Delta u_{f,e}(t)\bigr)^\top
\bigl(\mu_f(0)+\Delta\mu_f(t)\bigr).
$$

Expanding:

$$
\gamma_{f,e}(t)
=
\gamma_{f,e}(0)
+
\underbrace{\Delta u_{f,e}(t)^\top \mu_f(0)}_{\text{router-boundary drift}}
+
\underbrace{u_{f,e}(0)^\top \Delta\mu_f(t)}_{\text{feature-center drift}}
+
\underbrace{\Delta u_{f,e}(t)^\top \Delta\mu_f(t)}_{\text{interaction drift}}.
$$

This is the core decomposition of the anchor.

### 4.6 Sufficient Preservation Condition

Using Cauchy-Schwarz:

$$
|\Delta u^\top \mu_0|\leq \|\Delta u\|\|\mu_0\|,
$$

$$
|u_0^\top \Delta\mu|\leq \|u_0\|\|\Delta\mu\|,
$$

$$
|\Delta u^\top \Delta\mu|\leq \|\Delta u\|\|\Delta\mu\|.
$$

Therefore, a sufficient condition for center assignment preservation is:

$$
\gamma_{f,e}(0)
>
\|\Delta u_{f,e}(t)\|\|\mu_f(0)\|
+
\|u_{f,e}(0)\|\|\Delta\mu_f(t)\|
+
\|\Delta u_{f,e}(t)\|\|\Delta\mu_f(t)\|.
$$

For token-level preservation, include the cluster radius term:

$$
\gamma_{f,e}(0)
>
B_{f,e}(t)
+
\|u_{f,e}(t)\|\rho_f(t),
$$

where:

$$
B_{f,e}(t)
=
\|\Delta u_{f,e}(t)\|\|\mu_f(0)\|
+
\|u_{f,e}(0)\|\|\Delta\mu_f(t)\|
+
\|\Delta u_{f,e}(t)\|\|\Delta\mu_f(t)\|.
$$

### 4.7 Margin Consumption Ratio

Define:

$$
R_{f,e}(t)
=
\frac{B_{f,e}(t)}{\gamma_{f,e}(0)+\varepsilon}.
$$

Aggregate:

$$
R_{\max}(t)=\max_f\max_{e\neq a(f)}R_{f,e}(t),
$$

or use high quantiles for stability.

Prediction:

- $R(t)<1$: assignment should be more stable.
- $R(t)\approx 1$: boundary cases.
- $R(t)>1$: sign flips and NMI drop become likely.

### 4.8 Common/Residual Decomposition

Using:

$$
\mu_f(t)=c(t)+r_f(t),
$$

the pairwise margin becomes:

$$
\gamma_{f,e}(t)=u_{f,e}(t)^\top c(t)+u_{f,e}(t)^\top r_f(t).
$$

This separates:

- **common term**:
  $$
  C_{f,e}(t)=u_{f,e}(t)^\top c(t)
  $$
- **residual feature term**:
  $$
  R^{\mathrm{feat}}_{f,e}(t)=u_{f,e}(t)^\top r_f(t)
  $$

Preservation requires that the correct expert's residual advantage is not overwhelmed by common-driven router drift.

---

## 5. Computational Realization

### Input Objects

Required for each seed, condition, and checkpoint $t\in\{0,5,10\}$:

1. hidden states $h_i(t)$
2. fixed proxy/feature labels $y_i$
3. router rows $w_e(t)$
4. route assignments $\hat e_i(t)=\arg\max_e w_e(t)^\top h_i(t)$
5. training loss / LM loss
6. expert load

### Derived Objects

1. feature centers:
   $$
   \mu_f(t)=\mathrm{mean}_{i:y_i=f}h_i(t)
   $$

2. common center:
   $$
   c(t)=\mathrm{mean}_f\mu_f(t)
   $$
   or another pre-specified common direction.

3. residual centers:
   $$
   r_f(t)=\mu_f(t)-c(t)
   $$

4. initial assignment:
   $$
   a(f)=\arg\max_e w_e(0)^\top\mu_f(0)
   $$

5. pairwise margins:
   $$
   \gamma_{f,e}(t)
   $$

6. drift decomposition terms:
   - router-boundary drift
   - feature-center drift
   - interaction drift

7. margin consumption ratio:
   $$
   R_{f,e}(t)
   $$

8. sign flip rate:
   $$
   \mathrm{SFR}(t)=
   \frac{
   \#\{(f,e):\gamma_{f,e}(t)<0\}
   }{
   \#\{(f,e):e\neq a(f)\}
   }
   $$

9. proxy-route NMI:
   $$
   \mathrm{NMI}(y_i,\hat e_i(t))
   $$

### Primary Metric

$$
\mathrm{proxy\_route\_NMI}@\{5,10\}
$$

### Mechanism Metrics

- $\Gamma_{\mathrm{center}}(0)$
- $\Gamma_{\mathrm{center}}(t)$
- $R_{\max}(t)$ or high-quantile $R(t)$
- sign flip rate
- margin term attribution:
  - router-boundary drift contribution
  - feature-center drift contribution
  - interaction contribution
- common alignment gain:
  $$
  u_{f,e}(t)^\top c(t)-u_{f,e}(0)^\top c(0)
  $$

### Guard Metrics

- LM loss
- maximum expert load
- active experts
- step-0 assignment validity
- cluster radius / within-feature dispersion

---

## 6. Minimal Falsification Tests

### Test 1: Margin-Preservation Correlation

**Question:** Do larger initial margins predict better preservation?

**Setup:** Compare seeds/conditions with different initial margins.

**Primary readout:** correlation between initial minimum margin / margin consumption ratio and proxy-route NMI at step 5/10.

**Pass:** lower $R(t)$ predicts higher NMI and lower sign flip rate.

**Fail:** no relationship between margin consumption and preservation.

**Insufficient:** NMI changes but loss/load artifacts dominate.

---

### Test 2: Margin Shrink / Removal

**Question:** Is margin causally relevant, not just correlated?

**Setup:** Construct interventions that reduce initial margin while preserving as much of the initial assignment and architecture as possible.

Candidate interventions:

1. global router-row scaling diagnostic;
2. pairwise margin shrink perturbation;
3. reduced center-init strength;
4. temperature/softmax confidence control.

**Pass:** margin shrink causes lower step-5/10 NMI and higher sign flip rate.

**Fail:** margin shrink does not affect preservation.

**Caution:** global scaling changes softmax confidence and gradients; treat it as diagnostic unless controlled.

---

### Test 3: Drift Attribution

**Question:** Does failure come mainly from feature-center drift or router-boundary drift?

**Setup:** Compute:

$$
\Delta u^\top\mu_0,\quad u_0^\top\Delta\mu,\quad \Delta u^\top\Delta\mu.
$$

**Pass:** the dominant negative term identifies failure mode.

**Fail:** decomposition terms do not explain margin or NMI change.

**Interpretation:**

- router-boundary term dominates: router-side early lock-in;
- feature-center term dominates: hidden-state feature object drift;
- interaction dominates: coupled instability.

---

### Test 4: Common-Direction Audit

**Question:** Does router drift toward common/dense direction explain preservation failure?

**Setup:** Track common term:

$$
u_{f,e}(t)^\top c(t)
$$

and residual term:

$$
u_{f,e}(t)^\top r_f(t).
$$

**Pass:** failed seeds show increased common alignment and reduced residual separation.

**Fail:** common alignment does not change, yet margin is consumed.

---

### Test 5: Tracking Oracle / Slow Router Control

**Question:** Would tracking moving feature centers rescue preservation?

**Setup:** Compare ordinary training against:

1. frozen router;
2. slow-updated router;
3. EMA center-tracking router;
4. oracle center-tracking diagnostic.

**Pass:** tracking improves NMI without unacceptable loss degradation.

**Fail:** tracking does not help, suggesting feature partition may not be compatible with the objective or failure is expert-side.

---

## 7. Current Evidence To Attach

This anchor should attach the following evidence once available:

1. baseline feature-center initialization result;
2. step-0 NMI and load;
3. step-5/10 NMI and load;
4. margin shrink/removal table;
5. center drift table;
6. router drift table;
7. margin decomposition table;
8. NMI vs margin consumption plot;
9. LM loss guard table.

Current evidence status:

```text
Draft anchor only. Evidence tables must be attached before claim update.
```

---

## 8. Claim Boundary And Next Decision

### Allowed Claim If Supported

If the tests pass, we can claim:

```text
In the tested synthetic/proxy setting, early-training preservation is partly governed by a margin budget: initial feature-to-expert margins must exceed training-induced feature-center and router-boundary drift.
```

### Not Allowed

Even if supported, this anchor does not prove:

```text
1. real natural-language semantic experts exist;
2. MoE specialization is functionally useful;
3. margin control alone solves gating;
4. common-component control is a deployable architecture;
5. load balance implies specialization;
6. real-DCLM preservation has been solved.
```

### Next Decision

If margin-budget evidence passes:

```text
Test whether common-controlled router input, anti-lock-in training, or center-tracking expands the margin-safe region while preserving LM loss.
```

If margin-budget evidence fails:

```text
Park margin as a secondary diagnostic and decompose preservation failure into expert feedback, optimizer geometry, hidden-state feature instability, or objective incompatibility.
```
