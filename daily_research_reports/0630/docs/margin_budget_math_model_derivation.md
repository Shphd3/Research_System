# Mathematical Modeling Note: Margin-Budget Dynamics For Early-Training Preservation

**Status:** Draft v0.1 for review  
**Purpose:** Explain the mathematical model behind `A06_preservation_margin_budget` and how each experiment controls or measures each term.

---

## 1. Modeling Goal

The goal is to convert the qualitative preservation question:

> Why does a feature-to-expert routing partition survive or fail during early training?

into a quantitative geometric condition:

> Does the initial routing margin exceed the feature-center and router-boundary drift accumulated during training?

This document defines the mathematical objects, derives the margin dynamics, and maps each experimental audit to one term of the model.

---

## 2. Objects And Definitions

### 2.1 Hidden States

Let:

$$
h_i(t)\in\mathbb{R}^d
$$

be the hidden state of token/sample $i$ at training step $t$.

### 2.2 Fixed Feature / Proxy Label

Let:

$$
y_i\in F
$$

be the fixed feature/proxy label assigned to sample $i$. In synthetic settings this may be a true feature label. In real-DCLM proxy settings it may be a fixed cluster label.

This label is fixed for the audit. If labels are re-clustered at every checkpoint, the preservation question changes and becomes a tracking question, not assignment preservation.

### 2.3 Feature Center

For feature $f$, define:

$$
\mu_f(t)=\frac{1}{|I_f|}\sum_{i\in I_f}h_i(t),
\quad
I_f=\{i:y_i=f\}.
$$

This is the feature center.

### 2.4 Router Row

For expert $e$, define:

$$
w_e(t)\in\mathbb{R}^d.
$$

The top-1 router score is:

$$
z_e(h,t)=w_e(t)^\top h.
$$

The routed expert is:

$$
\hat e(h,t)=\arg\max_e w_e(t)^\top h.
$$

### 2.5 Initial Assignment

At step 0, each feature center is assigned to its winning expert:

$$
a(f)=\arg\max_e w_e(0)^\top \mu_f(0).
$$

This is the target assignment whose preservation we test.

### 2.6 Pairwise Router Gap

For a competing expert $e\neq a(f)$, define:

$$
u_{f,e}(t)=w_{a(f)}(t)-w_e(t).
$$

This vector defines the decision boundary between the assigned expert and competitor $e$.

### 2.7 Pairwise Margin

The center-level margin is:

$$
\gamma_{f,e}(t)=u_{f,e}(t)^\top\mu_f(t).
$$

If $\gamma_{f,e}(t)>0$, the feature center $\mu_f(t)$ scores higher for the original expert $a(f)$ than for competitor $e$.

For feature $f$ to preserve its center assignment:

$$
\gamma_{f,e}(t)>0,\quad \forall e\neq a(f).
$$

For all features to preserve center assignment:

$$
\Gamma(t)=\min_f\min_{e\neq a(f)}\gamma_{f,e}(t)>0.
$$

---

## 3. Derivation Of Margin Dynamics

### 3.1 Drift Definitions

Let:

$$
\Delta\mu_f(t)=\mu_f(t)-\mu_f(0),
$$

$$
\Delta u_{f,e}(t)=u_{f,e}(t)-u_{f,e}(0).
$$

Then:

$$
\mu_f(t)=\mu_f(0)+\Delta\mu_f(t),
$$

$$
u_{f,e}(t)=u_{f,e}(0)+\Delta u_{f,e}(t).
$$

### 3.2 Expanding The Margin

Start from:

$$
\gamma_{f,e}(t)=u_{f,e}(t)^\top\mu_f(t).
$$

Substitute the drift decompositions:

$$
\gamma_{f,e}(t)
=
\bigl(u_{f,e}(0)+\Delta u_{f,e}(t)\bigr)^\top
\bigl(\mu_f(0)+\Delta\mu_f(t)\bigr).
$$

Expand:

$$
\gamma_{f,e}(t)
=
u_{f,e}(0)^\top\mu_f(0)
+
\Delta u_{f,e}(t)^\top\mu_f(0)
+
u_{f,e}(0)^\top\Delta\mu_f(t)
+
\Delta u_{f,e}(t)^\top\Delta\mu_f(t).
$$

Since:

$$
\gamma_{f,e}(0)=u_{f,e}(0)^\top\mu_f(0),
$$

we get:

$$
\gamma_{f,e}(t)=
\gamma_{f,e}(0)
+
D^{\mathrm{router}}_{f,e}(t)
+
D^{\mathrm{feature}}_{f,e}(t)
+
D^{\mathrm{interaction}}_{f,e}(t),
$$

where:

$$
D^{\mathrm{router}}_{f,e}(t)
=
\Delta u_{f,e}(t)^\top\mu_f(0),
$$

$$
D^{\mathrm{feature}}_{f,e}(t)
=
u_{f,e}(0)^\top\Delta\mu_f(t),
$$

$$
D^{\mathrm{interaction}}_{f,e}(t)
=
\Delta u_{f,e}(t)^\top\Delta\mu_f(t).
$$

### 3.3 Meaning Of Each Term

| Term | Formula | Meaning |
|---|---|---|
| Initial margin | $\gamma_{f,e}(0)$ | Step-0 safety buffer |
| Router-boundary drift | $\Delta u^\top \mu_0$ | Router rows/decision boundaries move relative to original center |
| Feature-center drift | $u_0^\top\Delta\mu$ | Hidden feature center moves relative to original boundary |
| Interaction drift | $\Delta u^\top\Delta\mu$ | Router and feature center co-move in a coupled way |

A margin flips when:

$$
\gamma_{f,e}(t)<0.
$$

Equivalently:

$$
D^{\mathrm{router}}+
D^{\mathrm{feature}}+
D^{\mathrm{interaction}}
<
-\gamma_{f,e}(0).
$$

Thus, preservation failure can be read as:

> training-induced negative drift consumes the initial margin.

---

## 4. Margin Budget Bound

Using Cauchy-Schwarz:

$$
|D^{\mathrm{router}}|
=
|\Delta u^\top\mu_0|
\leq
\|\Delta u\|\|\mu_0\|,
$$

$$
|D^{\mathrm{feature}}|
=
|u_0^\top\Delta\mu|
\leq
\|u_0\|\|\Delta\mu\|,
$$

$$
|D^{\mathrm{interaction}}|
=
|\Delta u^\top\Delta\mu|
\leq
\|\Delta u\|\|\Delta\mu\|.
$$

Define the drift budget:

$$
B_{f,e}(t)
=
\|\Delta u_{f,e}(t)\|\|\mu_f(0)\|
+
\|u_{f,e}(0)\|\|\Delta\mu_f(t)\|
+
\|\Delta u_{f,e}(t)\|\|\Delta\mu_f(t)\|.
$$

Then:

$$
\gamma_{f,e}(t)
\geq
\gamma_{f,e}(0)-B_{f,e}(t).
$$

So a sufficient preservation condition is:

$$
\gamma_{f,e}(0)>B_{f,e}(t).
$$

This is sufficient but not necessary. Actual signs may cancel. Therefore both exact decomposition terms and norm-bound budget should be reported.

---

## 5. Cluster-Aware Extension

The center margin only guarantees the assignment of the center. Individual tokens may still cross boundaries.

Let:

$$
h_i(t)=\mu_f(t)+\epsilon_i(t).
$$

Then:

$$
u_{f,e}(t)^\top h_i(t)
=
u_{f,e}(t)^\top\mu_f(t)
+
u_{f,e}(t)^\top\epsilon_i(t)
=
\gamma_{f,e}(t)+u_{f,e}(t)^\top\epsilon_i(t).
$$

If:

$$
\|\epsilon_i(t)\|\leq \rho_f(t),
$$

then:

$$
u_{f,e}(t)^\top h_i(t)
\geq
\gamma_{f,e}(t)-\|u_{f,e}(t)\|\rho_f(t).
$$

Define robust cluster-aware margin:

$$
\tilde{\gamma}_{f,e}(t)=
\gamma_{f,e}(t)-\|u_{f,e}(t)\|\rho_f^{(q)}(t),
$$

where $\rho_f^{(q)}(t)$ is a high quantile radius, for example 90% or 95%.

If:

$$
\tilde{\gamma}_{f,e}(t)>0,
$$

then most samples in feature $f$ should remain on the original side of the boundary.

This extension distinguishes:

1. center assignment preserved but cluster spread grows;
2. center assignment fails;
3. cluster assignment fails before center assignment fails.

---

## 6. Common/Residual Decomposition

### 6.1 Feature Center Decomposition

Let:

$$
\mu_f(t)=c(t)+r_f(t),
$$

where:

$$
c(t)=\frac{1}{|F|}\sum_f \mu_f(t)
$$

is a common/dense component, and:

$$
r_f(t)=\mu_f(t)-c(t)
$$

is the feature residual.

### 6.2 Margin Decomposition

Then:

$$
\gamma_{f,e}(t)=u_{f,e}(t)^\top c(t)+u_{f,e}(t)^\top r_f(t).
$$

Define:

$$
C_{f,e}(t)=u_{f,e}(t)^\top c(t),
$$

$$
Q_{f,e}(t)=u_{f,e}(t)^\top r_f(t).
$$

So:

$$
\gamma_{f,e}(t)=C_{f,e}(t)+Q_{f,e}(t).
$$

### 6.3 Interpretation

- $C_{f,e}(t)$: common direction contribution.
- $Q_{f,e}(t)$: feature-residual contribution.

If router gaps $u_{f,e}(t)$ rotate toward common/dense directions, then $C_{f,e}(t)$ can dominate and feature residual separation can become irrelevant.

This gives a direct link to common-component / early-lock-in intuition:

> The feature signal may still exist in $r_f(t)$, but the router boundary no longer separates it.

### 6.4 Common-Driven Failure Signature

A common-driven failure should show:

1. increasing alignment of router gaps with $c(t)$;
2. decreasing or unstable residual term $Q_{f,e}(t)$;
3. increasing expert load concentration;
4. falling proxy-route NMI;
5. acceptable loss decrease, meaning training did not simply fail.

---

## 7. Rival Explanations And Their Signatures

### R1: Proxy Feature Instability

**Explanation:** The feature/proxy label itself is unstable; preservation fails because the object being preserved is not real or not stable.

**Signature:**

- low cluster stability across checkpoints;
- feature centers become unrecoverable;
- step-0 routing already weak or seed-unstable.

**Separated by:**

- checking cluster stability;
- checking step-0 proxy-route NMI;
- checking whether $\mu_f(t)$ remains distinguishable.

**If true:** margin model is not the first failure point.

---

### R2: Weak Linear Bridge

**Explanation:** The router was never truly aligned with the proxy partition.

**Signature:**

- low $\gamma(0)$;
- low step-0 NMI;
- unstable initial assignment.

**Separated by:**

- step-0 bridge audit;
- initial margin audit.

**If true:** preservation is premature; return to initialization.

---

### R3: Feature-Center Drift Dominates

**Explanation:** Hidden feature centers move away from their initial locations faster than the router can preserve assignment.

**Signature:**

$$
u_0^\top\Delta\mu
$$

is the dominant negative term in margin change.

**Separated by:**

- feature center drift audit;
- replaying fixed router on checkpoint hidden states;
- center-tracking oracle.

**If true:** next decision is whether tracking or representation stabilization is needed.

---

### R4: Router-Boundary Drift Dominates

**Explanation:** Router rows or decision boundaries move away from feature-residual directions, possibly toward common/dense directions.

**Signature:**

$$
\Delta u^\top\mu_0
$$

is the dominant negative term.

**Separated by:**

- router row drift audit;
- frozen hidden replay;
- common alignment audit.

**If true:** next decision is anti-lock-in or common-controlled routing.

---

### R5: Coupled Drift Dominates

**Explanation:** Neither hidden drift nor router drift alone explains failure; their interaction matters.

**Signature:**

$$
\Delta u^\top\Delta\mu
$$

is large and negative.

**Separated by:**

- joint trajectory analysis;
- comparing frozen-router, frozen-hidden replay, and ordinary training.

**If true:** next decision is to model co-adaptation dynamics, not one-sided drift.

---

### R6: Expert Feedback / Objective Incompatibility

**Explanation:** Even if margins are preserved geometrically, expert learning dynamics or the next-token objective makes the partition functionally unstable.

**Signature:**

- margins remain positive but NMI or functional utility still drops;
- loss improves only when partition breaks;
- positive preservation control hurts loss.

**Separated by:**

- LM loss guard;
- expert ablation utility;
- fixed-router / positive preservation control.

**If true:** preservation alone may be incompatible with objective or not useful.

---

### R7: Margin Is Correlational, Not Causal

**Explanation:** Large margin is only a marker of a better condition, not the cause of preservation.

**Signature:**

- natural seeds show correlation, but margin shrink/removal does not change NMI;
- interventions that change margin do not change preservation.

**Separated by:**

- controlled margin shrink/removal;
- matched-load and matched-loss comparisons.

**If true:** margin remains a diagnostic, not a mechanism.

---

## 8. How Experiments Control Each Quantity

### 8.1 Initial Margin Control

**Quantity:**

$$
\gamma_{f,e}(0)
$$

**How to vary:**

1. scale center-initialized router rows;
2. interpolate between center initialization and random initialization;
3. reduce pairwise separation among router rows;
4. reduce selected-gate confidence while preserving argmax where possible.

**Risk:** global row scaling changes softmax confidence and router gradients. It should be labeled diagnostic unless controlled.

---

### 8.2 Feature-Center Drift Control

**Quantity:**

$$
\Delta\mu_f(t)
$$

**How to measure:**

- compute $\mu_f(t)$ at checkpoints with fixed labels;
- compare $\|\Delta\mu_f(t)\|$;
- project $\Delta\mu_f(t)$ onto initial router gaps $u_{f,e}(0)$.

**How to control:**

1. freeze earlier layers or hidden generator if available;
2. replay checkpoint hidden states through fixed router;
3. compare controlled synthetic setting vs real-DCLM proxy setting;
4. center-tracking oracle.

---

### 8.3 Router-Boundary Drift Control

**Quantity:**

$$
\Delta u_{f,e}(t)
=
\Delta w_{a(f)}(t)-\Delta w_e(t)
$$

**How to measure:**

- router row norm drift;
- router gap norm drift;
- cosine between $u(t)$ and $u(0)$;
- projection onto $\mu_f(0)$, $c(0)$, and $r_f(0)$.

**How to control:**

1. freeze router;
2. slow router learning rate;
3. router regularization toward initial rows;
4. anti-lock-in window;
5. common-controlled router input.

---

### 8.4 Common-Direction Alignment Control

**Quantity:**

$$
u_{f,e}(t)^\top c(t)
$$

**How to measure:**

- common term $C_{f,e}(t)$;
- cosine between router gaps and common direction;
- common alignment gain from step 0 to step 5/10.

**How to control:**

1. router-input centering;
2. common-logit cancellation;
3. residual-only router diagnostic;
4. compare full hidden input vs common-controlled input.

---

### 8.5 Token-Level Robustness Control

**Quantity:**

$$
\tilde{\gamma}_{f,e}(t)
=
\gamma_{f,e}(t)-\|u_{f,e}(t)\|\rho_f(t)
$$

**How to measure:**

- within-feature radius;
- high-quantile distance to center;
- sign flip rate at token level;
- route purity within each feature.

**How to control:**

1. reduce hidden noise in synthetic setting;
2. compare center routing vs token routing;
3. measure whether cluster spread grows during training.

---

## 9. Metric Table

| Metric | Formula | Meaning | Main Use |
|---|---|---|---|
| Center margin | $\gamma_{f,e}(t)$ | Feature center assignment safety | Core preservation object |
| Min margin | $\Gamma(t)$ | Worst-case safety | Early warning |
| Drift budget | $B_{f,e}(t)$ | Upper bound on margin consumption | Sufficient condition |
| Consumption ratio | $R=B/(\gamma(0)+\varepsilon)$ | Whether margin budget is exhausted | Prediction of failure |
| Sign flip rate | $\Pr[\gamma<0]$ | Fraction of pairwise assignment reversals | Mechanism readout |
| Cluster-aware margin | $\tilde{\gamma}$ | Token-level robust margin | Explains NMI vs center margin gap |
| Router drift term | $\Delta u^\top\mu_0$ | Router-side failure | Lock-in diagnosis |
| Feature drift term | $u_0^\top\Delta\mu$ | Hidden-side failure | Tracking diagnosis |
| Interaction term | $\Delta u^\top\Delta\mu$ | Co-adaptation failure | Coupled dynamics |
| Common term | $u^\top c$ | Common/dense alignment | Common-component diagnosis |
| Residual term | $u^\top r_f$ | Feature-specific separation | Specialization diagnosis |
| proxy-route NMI | $\mathrm{NMI}(y_i,\hat e_i)$ | Route-label agreement | Primary outcome |
| LM loss | loss | Predictive guard | Prevent bad preservation |

---

## 10. Suggested Analysis Tables

### Table 1: Per-Condition Summary

| condition | seed | step | proxy_route_NMI | LM_loss | max_load | initial_min_margin | margin_consumption_q90 | sign_flip_rate |
|---|---:|---:|---:|---:|---:|---:|---:|---:|

### Table 2: Drift Attribution

| condition | seed | step | router_term_mean | feature_term_mean | interaction_term_mean | dominant_negative_term |
|---|---:|---:|---:|---:|---:|---|

### Table 3: Common/Residual Audit

| condition | seed | step | common_alignment_gain | residual_term_drop | NMI_drop | interpretation |
|---|---:|---:|---:|---:|---:|---|

### Table 4: Margin Intervention

| intervention | step0_assignment_ok | margin_change | NMI@5 | NMI@10 | loss_guard | interpretation |
|---|---|---:|---:|---:|---:|---|

---

## 11. Expected Plots

1. **NMI vs margin consumption ratio**  
   x-axis: $R(t)$, y-axis: proxy-route NMI.

2. **Margin trajectory**  
   $\Gamma(0), \Gamma(5), \Gamma(10)$.

3. **Drift attribution stacked bar**  
   router term, feature term, interaction term.

4. **Common vs residual term plot**  
   $u^\top c$ and $u^\top r_f$ over training.

5. **Sign flip heatmap**  
   feature $f$ by competitor expert $e$, colored by whether $\gamma_{f,e}$ flips.

---

## 12. How To Read Outcomes

### Outcome A: Margin Model Supported

Observed:

- initial margin predicts preservation;
- margin consumption predicts NMI drop;
- margin shrink reduces NMI;
- sign flips track NMI drop.

Interpretation:

```text
Preservation is at least partly governed by a margin budget.
```

Allowed next step:

```text
Test interventions that increase initial margin, reduce drift, or track moving centers.
```

---

### Outcome B: Router Drift Dominates

Observed:

- feature centers stable;
- router gaps rotate;
- common alignment increases;
- NMI drops.

Interpretation:

```text
Failure is router-side early lock-in or common-direction attraction.
```

Allowed next step:

```text
Test common-controlled router input, common-logit cancellation, router slow update, or anti-lock-in window.
```

---

### Outcome C: Feature Drift Dominates

Observed:

- router rows stable;
- feature centers move across decision boundaries;
- tracking oracle helps.

Interpretation:

```text
Failure is hidden-side feature-center drift.
```

Allowed next step:

```text
Test tracking or representation-stabilization mechanisms.
```

---

### Outcome D: Margin Not Predictive

Observed:

- no relation between margin metrics and NMI;
- margin intervention does not affect preservation.

Interpretation:

```text
Margin is not the right central mechanism.
```

Allowed next step:

```text
Park margin; inspect expert feedback, optimizer geometry, objective incompatibility, or metric definition.
```

---

### Outcome E: Preservation Hurts Loss

Observed:

- margin or tracking preserves NMI;
- LM loss worsens materially.

Interpretation:

```text
Preserving the partition may conflict with predictive learning.
```

Allowed next step:

```text
Do not claim method success. Move to utility/objective compatibility analysis.
```

---

## 13. Relation To The Current Research Line

This model does not replace the broader 05/06/07 chain. It sharpens level 3: preservation.

The route becomes:

```text
05 failure mechanism:
common component and early feedback can create wrong routing basins.

06 initialization:
feature/proxy centers can initialize step-0 routing.

06 preservation:
margin-budget model tests whether early training exhausts the assignment margin.

07 utility:
only after preservation succeeds should common/rare interference or expert utility be tested.
```

This prevents a common error:

```text
High step-0 NMI does not imply training preservation.
Preservation does not imply utility.
Utility must be tested after preservation.
```

---

## 14. Implementation Checklist For Codex

Before running code, require these fields:

```text
data:
model:
checkpoints:
fixed labels:
router row source:
initial assignment definition:
conditions:
primary metric:
secondary metrics:
known good case:
known bad case:
known confusing case:
success criterion:
failure criterion:
insufficient-evidence criterion:
claim boundary:
```

Codex should output:

```text
tables/margin_by_feature_expert.csv
tables/drift_decomposition.csv
tables/condition_summary.csv
figures/nmi_vs_margin_consumption.png
figures/margin_trajectory.png
figures/drift_attribution.png
summary.md
detailed.md
```

Do not allow Codex to add new claims beyond the approved protocol.

---

## 15. Review Questions

Before approving this model, check:

1. Is $a(f)$ fixed from step 0, or recomputed at each step?
2. Are feature/proxy labels fixed and meaningful enough for preservation?
3. Is the router row scale controlled, or does scaling change training dynamics?
4. Is cluster radius included when interpreting token-level NMI?
5. Are common/residual components defined consistently?
6. Does the model distinguish center assignment from token assignment?
7. Does the experiment include LM loss guard?
8. What result would falsify the margin-budget hypothesis?
9. What result would force us to abandon margin as central mechanism?
10. What exact next decision will the result change?
