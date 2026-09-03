# Anchor Advisor-Style Alignment Audit

## Basis

Checked against the advisor-style research-exploration chain:

```text
conjecture -> physical priors -> mathematical model
-> implementation contract -> experiment
-> failure analysis / evidence interpretation -> updated conjecture
```

Current anchor:
`Projects/from-attention-to-search/main/problem_anchors/06_geometry_proxy_preservation/06_03_high_dimensional_gaussian_gate_norm_variation_anchor.md`

## Overall Judgment

The current anchor is mostly aligned with the advisor-style process. It starts
from a clear problem, names a physical prior, writes the minimal mathematical
model, maps the model to a concrete computational intervention, and updates
the claim boundary after the experiment.

The main remaining weakness is not structure. The weakness is transition:
the anchor now supports a clean gate-only mechanism claim, but the next
decision should more explicitly bridge from gate-only uniform inputs to real
hidden-state routing without jumping directly to a new gating method.

## Alignment Check

| Advisor-style requirement | Current anchor status | Comment |
|---|---|---|
| Problem first | aligned | The researcher judgment record and Problem Definition now state the parent problem before the experiment. |
| One decision question | aligned | The decision question is whether removing only row-norm variation reduces Gaussian true-cell imbalance. |
| Physical prior | aligned | $z_e=\rho_e u_e^\top x$ directly states why row norm can affect top-1 winning probability. |
| Mathematical model | aligned | The anchor has both row decomposition and observed-load decomposition. |
| Implementation contract | mostly aligned | The computational realization names inputs, variables, stages, and artifacts without becoming a runbook. |
| Minimal falsification | aligned | The norm-controlled paired comparison tests one model term: $\rho_e$. |
| Evidence updates conjecture | aligned | Current Evidence compresses 0620 evidence plus the new norm-control result. |
| Claim boundary | aligned | The anchor does not claim trained MoE collapse or semantic specialization. |
| Next uncertainty | partially aligned | The next decision is correct, but should be sharpened toward a real-hidden-state diagnostic before method design. |

## Main Narrative Strength

The anchor has a strong advisor-style causal chain:

```text
phenomenon:
  Gaussian top-1 gate has fixed load imbalance beyond sampling noise.

physical prior:
  dot-product score depends on direction and row norm.

model:
  w_e = rho_e u_e, z_e = rho_e u_e^T x.

intervention:
  keep u_e fixed, equalize rho_e.

result:
  Gaussian-scaled imbalance drops to normalized-direction level.

updated conjecture:
  row-norm variation is a separable initialization imbalance term.
```

This is the right kind of movement: it does not start from a method. It starts
from a mechanism question and tests one term in the model.

## Remaining Gaps

1. The parent problem still hints at a better initialization method. That is
   useful motivation, but the next research move should stay diagnostic until
   the real-hidden-state setting is checked.

2. The phrase `Gaussian prototype direction/cell imbalance` should remain
   carefully defined when speaking. It means imbalance from the geometry of
   normalized gate row directions, not semantic prototypes.

3. The current experiment assumes uniform high-dimensional inputs. Real router
   inputs may be anisotropic, centered around common directions, or changing
   during training. This can revive direction-geometry explanations even after
   row-norm variation is controlled.

4. The anchor does not yet separate these two real-setting questions:
   whether row-norm variation exists at initialization, and whether it remains
   important after hidden-state drift and training interactions begin.

## Recommended Next Directions

### 1. Real Hidden-State Norm-Controlled Replay

Question:
When router inputs are real hidden states rather than uniform random vectors,
how much early load imbalance remains after gate row norms are controlled?

Why this should be next:
It is the closest bridge from the current gate-only mechanism to the real MoE
failure mechanism. It keeps the same model term $\rho_e$ and tests whether the
gate-only result matters under the actual input distribution.

Expected comparison:

```text
standard init gate on real H
norm-controlled gate on real H
normalized-direction gate on real H
centered / whitened H diagnostic if needed
```

### 2. Hidden-State Geometry Versus Gate-Norm Decomposition

Question:
In trained or early-training hidden states, is load imbalance dominated by
gate row norm, hidden-state anisotropy, or direction-cell geometry under the
real input distribution?

Why this matters:
Uniform-input evidence is clean, but real hidden states may have common
components. If common-direction structure dominates, then row-norm control is
necessary but not sufficient.

Expected role:
Root-cause audit, not method construction.

### 3. Initialization Intervention Only After Diagnostic Transfer

Question:
If row-norm variation still contributes in the real hidden-state setting, does
row-normalized initialization reduce early load concentration without harming
the route-function learning objective?

Why this should wait:
This is method construction. It becomes justified only after the real-hidden
diagnostic shows that row-norm variation changes the current claim boundary or
next decision.

## Suggested Meeting Ask

Ask the advisor to confirm this route:

```text
gate-only decomposition is now closed enough;
next step should be real-hidden-state norm-control replay;
method design should wait until the mechanism survives the real input setting.
```
