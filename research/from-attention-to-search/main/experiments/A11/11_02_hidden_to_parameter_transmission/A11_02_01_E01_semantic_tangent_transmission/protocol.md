# Protocol: A11_02_01_E01 K=2 Semantic Tangent-Kernel Transmission

## 0. Approval Snapshot

**Approval status:** approved for implementation and remote 4-GPU execution by the user on 2026-07-10.  
**Purpose:** determine whether the controlled K=2 hidden-state semantic signal is transmitted into shared Transformer encoder parameters with the tangent-kernel-predicted magnitude.  
**Primary anchor:** `../../../../problem_anchors/11_informative_future_branch_mechanism/11_02_hidden_to_parameter_transmission/subanchors/11_02_01_reachability_and_background_sign_anchor.md`.
**Decision question:** does the native shared-encoder Jacobian carry a numerically resolved direct semantic direction, and does the net velocity remain positive after adding the shared H1 objective?  
**Experiment role:** root-cause audit, not a method comparison.  
**Primary metric:**

\[
G_{\theta,total}
=G_{\theta,direct}+G_{\theta,background},
\]

together with the tangent-kernel prediction \(v^\top\Theta v/m^2\).  
**Minimal setup:** clean K=2 decision-only data, one-layer Transformer, frozen token embeddings and output heads, five seeds, and semantic-Jacobian scale \(\alpha\in\{0,0.5,1\}\).  
**Pass:** calibration identities pass; native \(G_{\theta,direct}\) exceeds the numerical floor; full K2 has positive net velocity in at least 4/5 seeds; actual one-step margin movement matches the linear prediction.  
**Fail:** hidden direct velocity is positive but the shared encoder has no resolved transmission, or the shared H1 background reverses the direct term.  
**Insufficient:** forward-equivalence, autograd, coverage, or numerical-floor guards fail, or the nonlinear remainder makes the one-step sign undecidable.  
**Cannot claim:** natural-language benefit, all-position sample efficiency, general K, LLM scaling, or MoE benefit.

## 1. Terminology / Definitions

| Term | Plain meaning | Formula / computation | Decision role | Cannot prove |
|---|---|---|---|---|
| parameter semantic velocity | first-order semantic-margin movement under an SGD parameter update | \(G_\theta=-\langle\nabla_\theta M,\nabla_\theta L\rangle\) | primary local mechanism | multi-step convergence |
| kernel signal | shared-encoder reachability along the semantic direction | \(S_\Theta=v^\top\Theta v/m^2=\|\nabla_\theta M\|^2\) | detects a parameter bottleneck | net progress with H1 |
| direct term | contribution from predicting \(Y_2=S_Z\) | \(G_{\theta,direct}\) | MTP-specific signal | total training result |
| background term | signed contribution from the shared \(Y_1=A\) objective | \(G_{\theta,background}\) | help or cancellation | all-position background |
| net-preservation ratio | fraction and sign of direct velocity retained after H1 | \(\rho_{\theta,net}=G_{\theta,total}/G_{\theta,direct}\) above the numerical floor | scale-free reversal test | absolute speed |
| kernel cosine | alignment after semantic and H1 directions pass through the encoder Jacobian | \(\chi_\Theta=\cos(J^\top v,J^\top c)\) | direction of background transfer | finite-step harm |
| kernel norm ratio | relative strength of the H1 parameter direction | \(r_\Theta=\|J^\top c\|/\|J^\top v\|\) | magnitude of cancellation | long-run optimization |
| Jacobian scale \(\alpha\) | keeps reference states fixed while scaling semantic Jacobian sensitivity | \(H_\alpha=\bar H_0+D_\alpha(H^{raw}-H_0^{raw})\) | causal calibration | natural architecture change |
| nonlinear remainder | actual one-step movement minus linear prediction | \(R=(\Delta M-\eta G_\theta)/\eta^2\) | one-step fidelity | long-run curvature bound |

## 2. Anchor Alignment

The anchor asks whether the objective-level K=2 semantic direction survives shared-encoder parameterization rather than moving a trainable branch-token embedding row or output head. The protocol freezes those trivial paths and measures only attention, MLP, LayerNorm, and position parameters.

The main falsifier is:

```text
positive hidden semantic velocity
but unresolved shared-encoder J^T v or nonpositive full-K2 net velocity.
```

## 3. Tested Hypotheses

### H1. Algebra and implementation calibration

At the common reference state:

\[
\frac{S_\Theta(0)}{S_\Theta(1)}\le10^{-6},
\qquad
0.225\le\frac{S_\Theta(0.5)}{S_\Theta(1)}\le0.275,
\]

and direct-only must satisfy:

\[
\frac{|G_{\theta,direct}-S_\Theta|}
{|S_\Theta|+10^{-12}}\le10^{-4}.
\]

If \(|\eta G_{\theta,background}(1)|\ge10^{-10}\), the background scaling guard is:

\[
0.45\le
\frac{G_{\theta,background}(0.5)}
{G_{\theta,background}(1)}
\le0.55.
\]

For every seed and \(\alpha\):

\[
G_{\theta,total}(\alpha)
=\alpha^2G_{\theta,direct}(1)
+\alpha G_{\theta,background}(1)
\]

must hold with absolute residual divided by the native reference scale
\(|G_{\theta,direct}(1)|+|G_{\theta,background}(1)|\) at most \(10^{-4}\).
The native scale is required because the \(\alpha=0\) prediction is exactly zero.
These are validity guards, not scientific evidence.

### H2. Native transmission and net preservation

At \(\alpha=1\), direct transmission is resolved only when:

\[
|\eta G_{\theta,direct}|\ge10^{-10}
\]

and \(G_{\theta,direct}>0\). Full K2 must satisfy in at least 4/5 seeds:

\[
G_{\theta,total}>0,
\qquad
\rho_{\theta,net}>0.
\]

The diagnostic reconstruction is:

\[
\rho_{\theta,net}=1+\chi_\Theta r_\Theta.
\]

### H3. One-step and early finite-step fidelity

For \(\alpha\in\{0.5,1\}\) with \(|\eta G_{\theta,total}|\ge10^{-10}\), at least 4/5 seeds must satisfy:

\[
\operatorname{sign}(\Delta M)
=\operatorname{sign}(G_{\theta,total}),
\]

\[
\frac{|\Delta M-\eta G_{\theta,total}|}
{\eta|G_{\theta,total}|+10^{-12}}
\le0.25.
\]

Direct-only early margin area and native H2 recovery should order as \(\alpha=1>0.5>0\). Full-K2 ordering is required only when its reference net velocity is positive. If one-step fidelity passes but the ordering disappears, the claim remains local.

For conditions that train H1, full K2 at \(\alpha=1\) must finish with Y1 accuracy at least `0.90` and no more than `0.05` below shared-only K1. Report Y1-loss area without using an arbitrary small-cost failure threshold.

## 4. Rival Explanations

1. **Output-head adaptation:** both heads are frozen and head drift must be zero.
2. **Embedding lookup:** all token embeddings are frozen and their gradients/updates must be zero.
3. **Unequal reference states:** exact branch states, logits, and losses must match across branches and \(\alpha\) within \(10^{-7}\) at step 0.
4. **Autograd error:** vector-Jacobian and gradient-norm kernel computations must agree.
5. **Shared target mislabeled as direct signal:** direct-only, shared-only, and full gradients are computed separately.
6. **No raw branch sensitivity:** raw branch states or their shared-encoder Jacobians must differ before folding, while folded states coincide.
7. **Parameter omission:** attention, MLP, LayerNorm, and position-group direct contributions must sum to the shared-encoder total.
8. **Immediate nonlinearity:** actual virtual updates at \(\eta\) and \(\eta/2\) are compared with the linear prediction.

The fixed-head orthogonality and common-state class-logit ranges must be at
most \(10^{-6}\); this is a head-construction guard separate from cross-condition
forward equality.

## 5. Data / Model / Algorithm / Objective

Data:

\[
Z\sim\operatorname{Unif}\{1,2,3,4\},
\]

\[
X_{\le T}=(\operatorname{BR}_Z,F_1,\ldots,F_{16},U_1,\ldots,U_4),
\]

\[
Y_1=A,
\qquad
Y_2=S_Z.
\]

There is exactly one deterministic prefix per branch. The full batch contains four examples. Seeds change model, frozen-head, and frozen-embedding initialization, not data.

The H2 diagnostic softmax has four semantic classes with fixed regular-simplex rows orthogonal to the common folded state. Define:

\[
v=(v_1,\ldots,v_m),
\qquad
v_z=u_{S_z}-\bar u_2.
\]

The fixed H1 head uses one target and three distractor rows forming a regular simplex in a branch-common subspace orthogonal to the H2 row span and the common state. Its hidden descent direction is identical across branches:

\[
c=(b,\ldots,b),
\qquad
v^\top c=0.
\]

Folded state:

\[
H_\alpha(\theta)
=\bar H_0+D_\alpha
\left(H^{raw}(\theta)-H_0^{raw}\right),
\qquad
D_\alpha=P_\perp+\alpha P_v.
\]

\(\alpha=1\) uses the native raw shared-encoder Jacobian but still uses the reference-centered forward state. This is a mechanism intervention, not natural Transformer training.

Model and optimization:

- one-layer causal Transformer, `d_model=64`, one attention head, dropout zero;
- float64 parameters and activations, because this experiment adjudicates
  \(10^{-4}\)-level Jacobian identities rather than mixed-precision throughput;
- frozen token embeddings and fixed H1/H2 heads;
- train shared attention, MLP, LayerNorm, and position parameters only;
- full-batch SGD, no weight decay, learning rate `0.003`;
- virtual half-step learning rate `0.0015`;
- 200 training steps.

Objectives:

- `shared_only_k1`: \(L_1=\operatorname{CE}(q_1,A)\);
- `direct_only_k2`: \(L_2=\operatorname{CE}(q_2,S_Z)\);
- `full_k2`: \(L_1+L_2\).

## 6. Conditions, Seeds, And Checkpoints

Seeds: `971,972,973,974,975`.

| Condition | \(\alpha\) | Role | Primary judgment |
|---|---:|---|---|
| `shared_only_k1` | 1 | no-direct guard | direct contribution absent; Y1 learns |
| `direct_only_k2` | 0 | semantic-null intervention | kernel and margin movement zero |
| `direct_only_k2` | 0.5 | quadratic calibration | direct ratio approximately 0.25 |
| `direct_only_k2` | 1 | native Jacobian transmission | resolved positive direct velocity |
| `full_k2` | 0, 0.5, 1 | background and finite-step audit | net sign and reconstruction |

Checkpoints: `0,1,2,5,10,20,50,100,200`. Seven conditions per seed give 35 training tasks. Virtual updates do not add training tasks.

## 7. Primary Metric

The decision order is:

1. reference forward equality and autograd identities;
2. quadratic direct and linear background scaling;
3. native \(G_{\theta,direct}\) magnitude and full-K2 \(G_{\theta,total}\) sign;
4. \(\rho_{\theta,net}=1+\chi_\Theta r_\Theta\) reconstruction;
5. one-step remainder and 200-step persistence.

## 8. Secondary Metrics

- hidden direct semantic velocity;
- \(\kappa_2=S_\Theta/\|v\|^2\);
- actual and predicted \(\Delta M\) at \(\eta\) and \(\eta/2\);
- native H2 accuracy, H2 target probability, semantic margin, branch-swap consistency;
- Y1 loss and accuracy;
- head drift, embedding update/gradient, kernel drift;
- attention, MLP, LayerNorm, and position contributions;
- early area under the semantic-margin and native-H2 curves;
- raw and folded exact branch-state separation.

A learned probe is not primary evidence because four deterministic prefixes do not provide an independent probe train/test problem.

## 9. Known Good / Known Bad / Known Confusing Cases

- Known good: direct-only \(\alpha=1\) should have positive hidden and parameter direct velocity.
- Known bad: at \(\alpha=0\), semantic margin is invariant for all parameter values under the intervention.
- Known confusing: full K2 may have positive direct but negative net velocity; this is an H2 result, not implementation failure.
- Known confusing: background scales as \(\alpha\) while direct scales as \(\alpha^2\), so full-K2 \(\alpha=0.5\) need not lie between the 0 and 1 learning curves.
- Known confusing: native H2 may remain below high accuracy at step 200 while local margin transmission is valid.

## 10. Stage-Level Profiling Plan

| Stage | Question | Pass | Artifact |
|---|---|---|---|
| static audit | are projectors, heads, and identities correct? | analytic and numerical guards pass | `static_audit.json` |
| CPU smoke | do seven conditions produce complete finite values? | all primary tables nonempty | `smoke_manifest.json` |
| single-GPU smoke | does CUDA autograd match CPU logic? | forward and kernel guards pass | `gpu_smoke.json` |
| remote 4-GPU | do all 35 tasks finish? | four shards, 5/5 seeds | `run_manifest.json` |
| aggregation | is the decision reproducible? | complete joins and coverage | `coverage_audit.csv` |

## 11. Algorithm Specification

Inputs are the four branch prefixes, fixed raw-reference states, common folded state, fixed H1/H2 heads, semantic direction \(v\), background direction \(c\), condition, and \(\alpha\). Compute folded states, losses, \(M_2\), shared-encoder parameter gradients, direct/background/net velocity, virtual updates, and curve metrics.

Required tables:

```text
kernel_scaling.csv
transmission_decomposition.csv
parameter_group_transmission.csv
finite_step_transmission.csv
curve_metrics.csv
fold_and_local_guard.csv
coverage_audit.csv
```

Tasks are assigned to four shards by stable `(seed, condition)` index. Each shard binds one GPU; aggregation runs only after all shards finish.

## 12. Success / Failure / Insufficient Evidence

**Success:** all H1 validity guards pass; native direct velocity exceeds the numerical floor; full-K2 native net velocity is positive in at least 4/5 seeds; one-step fidelity passes in at least 4/5 seeds; embedding/head and local-Y1 guards pass.  
**Partial success:** H1 and H2 pass but H3 fails, restricting the claim to local parameter transmission.  
**Mechanism failure:** calibration is valid but native \(\kappa_2\) is unresolved or background consistently reverses the direct term.  
**Invalid run:** forward equality, kernel identity, frozen-parameter, numerical, or coverage guards fail.

## 13. What This Cannot Claim

- MTP is better than NTP on natural language;
- decision-only SGD transfers automatically to all-position AdamW;
- K=2 transfers automatically to general K;
- local parameter velocity equals sample efficiency;
- MTP improves MoE routing or expert utility.
- the reference identities automatically transfer to float32/bfloat16 training.

## 14. Review Notes And Protocol Changes

The user authorized future formal-anchor iterations to proceed without separate approval. Before implementation, the review draft was tightened in four ways: deterministic per-branch prefixes remove a mean-fold/residual mismatch; fixed orthogonal H1/H2 heads isolate Jacobian-created background interaction; probe-only evidence was removed; and the exact direct-quadratic/background-linear/net-preservation law was added. No K, all-position, optimizer, scale, natural-language, or MoE sweep is included.
