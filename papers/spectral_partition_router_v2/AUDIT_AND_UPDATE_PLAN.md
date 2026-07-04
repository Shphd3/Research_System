# Audit and Update Plan for Spectral Partition Router v2

## 0. Current audit status

This audit was performed on the files currently visible on the GitHub default branch under:

```text
papers/spectral_partition_router_v2/
```

Visible files include:

```text
latex/paper.tex
latex/references.bib
latex/math_commands.tex
exp/README.md
exp/EXPERIMENT_PLAN.md
exp/CODEX_TASKS.md
exp/TABLE_TEMPLATES.md
```

I do **not** currently see executable experiment scripts or result folders under `exp/`, such as:

```text
exp/src/spr.py
exp/run_static_dispatch.py
exp/results/
```

Therefore, this audit can verify the paper logic and planned experiment design, but it cannot yet verify actual numerical results or script-level implementation. If Codex has generated scripts/results locally, they need to be pushed before a code-and-result audit can be completed.

---

## 1. Updated understanding of the research problem

The v2 problem should not be stated as ordinary load balancing. It should be stated as **uniform feature dispatch**.

Given an unlabeled route-relevant feature distribution

\[
X \sim P, \qquad X\in\mathbb{R}^d,
\]

construct a deterministic router

\[
g:\mathbb{R}^d\rightarrow \{1,\ldots,E\}
\]

with induced feature cells

\[
C_e=\{x:g(x)=e\}
\]

such that

\[
P(C_e)=1/E,\qquad e=1,\ldots,E.
\]

This is a distribution-level feature-space partition target. It is not the same as forcing a finite batch to have exactly equal expert counts.

---

## 2. Relation to the advisor's meeting instruction

The meeting instruction was to close the simplest mathematical case first: assume the feature representation / spectral space is uniform, then give a self-contained theoretical solution and experiments. Nonuniform spectra and large singular values are later problems.

The v2 formulation is consistent with that spirit, but it makes the task more operational:

```text
Advisor-level prompt:
If feature/spectral space is uniform, finish the simplest mathematical case.

v2 operational definition:
Uniform feature dispatch means equal-probability feature-space cells, and SPR constructs such cells from unlabeled features.
```

This is a reasonable iteration because the original phrase "uniformly distribute features to experts" is underspecified. v2 supplies:

1. the target definition;
2. the non-cheating criterion;
3. the construction;
4. the evaluation metrics.

Important boundary: v2 is not a claim that real sequence hidden states are already uniform. It is a controlled construction for the uniform-feature setting.

---

## 3. What currently matches between theory and experiments

### 3.1 Theory target

The paper proves the following core statement:

1. A scalar quantile split can assign any requested probability mass to a child node.
2. A recursive tree that splits each node in proportion to child expert counts gives leaf cells of mass `1/E`.
3. Once calibrated, the router is a fixed feature-only function and is not batch-level capacity assignment.

### 3.2 Experiment target

The planned experiments correctly follow the theory in broad structure:

| Experiment | Theory / claim tested |
|---|---|
| Static equal-mass dispatch | Recursive quantile partition gives equal-mass cells |
| Spectrally flat but non-spherical features | Prototype routers can fail under covariance-flat data; quantile calibration should still dispatch uniformly |
| Expert-weight-guided partitioning | Expert weights guide geometry, while quantiles provide mass uniformity |
| Feature partition quality | Equal mass is not the same as meaningful feature partition |
| Controlled MoE training dynamics | Initialization and training preservation are different problems |

This high-level alignment is correct.

---

## 4. Main theory–experiment mismatch risks

### Risk 1: Continuous-CDF theorem vs discrete experimental data

The current theorem assumes the scalar projection

\[
T=q^\top X
\]

has a continuous CDF. Several planned experiments use discrete or atom-supported distributions, such as

\[
X\in\{\pm e_1,\ldots,\pm e_d\}.
\]

For discrete distributions, a deterministic threshold may not be able to split probability mass exactly if a large atom lies at the threshold. This does **not** invalidate SPR, but the paper and implementation must handle it explicitly.

Required fix:

- Add a discrete/empirical version of the theorem with a tie condition.
- State the impossibility boundary: if an identical feature atom has probability greater than `1/E`, no deterministic feature-only router can split it while routing identical features identically.
- For empirical experiments, use lexicographic multi-projection keys to break projection ties using feature values, not sample indices.

### Risk 2: Spectral uniformity is not required by quantile routing

Quantile routing can equalize probability mass for any stable distribution with a usable scalar key. Therefore, spectral uniformity is not a mathematical requirement for the equal-mass proof.

Correct framing:

```text
Spectral uniformity is the controlled representation setting and normalization target.
Quantile calibration is the equal-mass construction.
```

Do not claim:

```text
Spectral uniformity causes quantile routing to work.
```

Claim instead:

```text
In the spectrally uniform setting requested by the problem, SPR gives a non-cheating equal-mass router. The same quantile principle is more general, but here it is used to solve the uniform-feature case.
```

### Risk 3: Expert SVD sign ambiguity

For an expert matrix `W_e`, the principal singular direction is a line:

\[
\{v_e,-v_e\}.
\]

Exact SVD does not determine an intrinsic sign. If SPR-Expert averages signed vectors directly,

\[
\bar v_L-\bar v_R,
\]

then the split direction can change arbitrarily with SVD sign conventions.

Required fix:

Use one of the following:

1. **Router-row inherited sign** if the prototype comes from an actual router row or MPI update.
2. **Deterministic orientation rule**, e.g. flip each vector so its dot product with a fixed anchor is nonnegative.
3. **Projective prototype representation**, using rank-one projectors
   \[
   P_e=v_ev_e^\top
   \]
   and sign-invariant distances/grouping. For a split direction, use the leading eigenvector of
   \[
   \bar P_L-\bar P_R.
   \]

The third option is the cleanest when using exact SVD prototypes from expert weights alone.

### Risk 4: Calibration exactness vs holdout generalization

SPR may be exact on calibration data but not on holdout data. The paper should not report calibration balance alone.

Required metrics:

- calibration LoadCV;
- holdout LoadCV;
- calibration-to-holdout gap;
- distribution shift diagnostics;
- node sample counts.

### Risk 5: SPR-Fixed can balance mass but may not partition meaningful features

SPR-Fixed should be treated as the minimal construction, not the final answer. It may create long slab-like cells.

Therefore, feature partition quality metrics are essential:

- within-cell variance;
- route-feature NMI on evaluation-only synthetic labels;
- expert purity;
- margin lower tail.

### Risk 6: Training dynamics cannot be inferred from static dispatch

Static equal-mass cells do not imply training preservation. The training section correctly introduces margin and route flips, but experiments must report them.

Required training metrics:

- route flip rate;
- margin p05;
- route-feature NMI over time;
- expert usage over time;
- validation loss;
- representation drift.

---

## 5. Implementation audit checklist for Codex outputs

When scripts are available, audit the implementation against the following invariants.

### 5.1 SPR tree construction

- Thresholds must be computed **inside each node**, not globally.
- Split ratio must be
  \[
  |E_L|/|E_N|.
  \]
- For non-power-of-two expert counts, child expert counts must determine quantile ratios.
- Leaf count must equal expert count.
- Each leaf must map to exactly one expert.

### 5.2 Non-cheating rule

- Router fitting may use `X_cal` and expert weights.
- Router fitting must not use feature labels except in evaluation code.
- Prediction must call `tree.predict(X)` using stored thresholds only.
- Holdout predictions must not recompute quantiles.
- No current-batch balancing or post-hoc reassignment may occur in SPR methods.

### 5.3 Tie handling

- Do not split ties using sample index if the route must be feature-only.
- Use deterministic feature-derived tie keys, e.g. secondary projections.
- Report atom/tie rate.
- If exact deterministic splitting is impossible, report this as a limitation rather than silently forcing balance.

### 5.4 Expert-weight usage

- If using SVD directions, handle sign ambiguity.
- Report whether prototypes are oriented vectors or sign-invariant projective lines.
- Compute prototype spread before interpreting expert-guided results.
- Compare expert-prototype top-1 against SPR-Expert to show that quantiles, not prototype top-1 alone, provide mass uniformity.

### 5.5 Metrics

Every experiment should report at least:

```text
LoadCV
max_abs_usage_error
max_min_load_ratio
margin_p05
calibration_holdout_gap
```

Feature-quality experiments should also report:

```text
route_feature_NMI
feature_purity
within_cell_variance
```

Training experiments should also report:

```text
train_loss
val_loss
route_flip_rate
representation_drift
expert_specialization_score
```

---

## 6. Recommended next paper updates

### Update 1: Add discrete quantile theorem and tie boundary

Add a subsection after the continuous quantile theorem:

```text
Discrete features and ties.
```

State that exact equal mass requires either no atom crossing a target threshold, feature-derived tie refinement, stochastic routing, or accepting approximate mass.

### Update 2: Clarify spectral uniformity's role

Add one paragraph:

```text
SPR's equal-mass proof does not require spectral uniformity; quantile calibration is distributional. Spectral uniformity is the controlled representation setting and removes anisotropy as a confound.
```

### Update 3: Fix expert prototype sign ambiguity

Replace signed-vector averaging in SPR-Expert with either:

- oriented router-row prototypes; or
- projective prototypes `P_e=v_ev_e^T`.

### Update 4: Separate three claims

The paper should explicitly separate:

1. equal-mass feature dispatch;
2. meaningful feature partition;
3. training preservation.

Only the first is proven by construction. The second and third require experiments.

### Update 5: Require holdout results before claiming uniformity

Do not fill paper tables with calibration-only success. Uniform dispatch should be reported on both calibration and holdout.

---

## 7. Updated iteration objective

The next iteration should be:

```text
v2.1 objective:
Make SPR mathematically valid for both continuous and empirical/discrete feature distributions; implement and audit the router; then run static dispatch and expert-guided experiments before training dynamics.
```

Priority order:

1. Implement and test SPR tree correctly.
2. Run static dispatch on continuous Gaussian/spherical data.
3. Run discrete/axis data with explicit tie handling.
4. Run expert-weight-guided audit with sign-invariant prototypes.
5. Only then run controlled MoE training dynamics.

---

## 8. Current bottom line

The current v2 story is strong, but it is not ready to claim experimental validation until code and results are pushed. The main conceptual correction is not to abandon SPR, but to tighten it:

```text
Quantiles guarantee equal mass.
Split directions determine geometry.
Expert weights guide expert identity.
Ties and sign ambiguity must be handled explicitly.
Training preservation must be measured separately.
```
