---
experiment_id: A15_11_E02_synthetic_parent_first_moe
status: SUPERSEDED_BEFORE_IMPLEMENTATION
created: 2026-08-29
primary_anchor: A15_11_gradient_consistent_hierarchical_routing
implementation_authorized: false
smoke_authorized: false
full_run_authorized: false
scientific_contract_frozen: true
scientific_body_frozen_at: 2026-08-29T14:55:25Z
resource_profile: h100-4-reserved
superseded_by: A15_11_E03_counterfactual_utility_residual_tree
---

# Protocol: Permutation-Equivalent Gradient-Consistency And Hierarchical MoE Test

## 0. Approval Snapshot

| Field | Frozen value |
| --- | --- |
| Status | `APPROVED_FOR_IMPLEMENTATION_SMOKE_FULL_RUN` |
| Authorization | the 2026-08-29 user request explicitly delegates readable formalization and requests autonomous execution on reserved 4×H100; post-result human knowledge wording is not delegated |
| Unique intervention | keep leaf frequency and the complete teacher-function multiset fixed; change only how those functions are paired with the named parent |
| Core stages | task-only representation formation; task-only compositional MoE utility |
| Primary metric | paired hierarchy-alignment interaction in log-exposure AULC of held-out functional NMSE |
| Decisive baseline | parameter-richer flat nonlinear GELU Router |
| Seeds | `151120` through `151139`, all paired across data and models |
| Resource | one worker exposing exactly four H100 GPUs; `seed_index mod 4` assigns work |
| Cannot claim | autonomous semantic discovery, universal neural-training necessity, natural-language hierarchy, or real-Qwen NLL gain |

The scientific contract is frozen before implementation. No result-dependent
learning-rate, step-budget, seed, model, condition, threshold, or metric change
may repair the primary run.

## 1. Terminology And Decision Chain

- **Parent $p$:** the externally named semantic grouping, one of four balanced
  values in $\mathbb Z_4$.
- **Child $c$:** one of four balanced values inside every parent.
- **Surface code $q$:** $q=(p+c)\bmod4$; neither another dataset nor a semantic
  parent.
- **Work:** the shared task operator is constant across children of the named
  parent.
- **Fail:** the exact same task operators are reassigned so that their mean
  cancels within the named parent.
- **Canonical operator:** the 512-dimensional vector whose inner product with
  content $z$ is the predicted response. It is the geometry object because a
  factorized hidden coordinate has an arbitrary invertible gauge.
- **Aligned hierarchy:** the structure whose first bank matches the current
  teacher's shared grouping: $H_p$ in work and $H_q$ in fail.

The tested chain is

$$
\text{cross-child gradient consistency}
\rightarrow\text{parent-readable task operator}
\rightarrow\text{matched conditional routing}
\rightarrow\text{held-out task gain}.
$$

Every arrow has a separate output and can fail without rewriting another.

## 2. Data Generator And Exact Invariants

Let $K=4$, $p,c\overset{ind}{\sim}\operatorname{Uniform}(\mathbb Z_4)$,
$q=(p+c)\bmod4$, and

$$
u(k)=(\cos(2\pi k/4),\sin(2\pi k/4))^\top.
$$

All Routers receive exactly

$$
s=[u(p);u(q)]\in\mathbb R^4.
$$

They never receive $c$, a leaf ID, or a semantic target. Let
$z\sim\mathcal N(0,I_{512})$. With root seed `151103`, generate two orthogonal
two-dimensional bases $U,V\in\mathbb R^{512\times2}$ by QR and fix

$$
A_k=\alpha Uu(k),\qquad B_k=\beta Vu(k).
$$

The main panel uses $\alpha=\beta=1$. The representation-only PCA companion
uses $\alpha=1,\beta=4$. Training observations add
$\epsilon\sim\mathcal N(0,0.05^2)$; primary held-out functional metrics score
the noise-free conditional mean and separately report noisy MSE.

Teacher operators are

$$
\theta^{work}_{p,c}=A_p+B_c,
\qquad
\theta^{fail}_{p,c}=A_q+B_c,
$$

and $y=\theta^\top z+\epsilon$. Because $(p,c)\leftrightarrow(q,c)$ is a
bijection, the run must verify before training that work and fail have the same
16 operators as a multiset, uniform leaf counts, signal variance
$\alpha^2+\beta^2$, Bayes noise, and per-sample supervision.

In canonical operator space define the zero-prediction functional gradient
$g_{p,c}=-\theta_{p,c}$ and

$$
\rho=\frac{\mathbb E_p\|\mathbb E_c g_{p,c}\|_2^2}
{\mathbb E_{p,c}\|g_{p,c}\|_2^2}.
$$

The generator must reproduce $\rho_{work}=1/2$ and $\rho_{fail}=0$ within
`1e-10` for the main panel. It also records the centered between-parent
gradient covariance, which is nonzero in work and zero in fail. Any failed
identity stops both stages.

## 3. Stage R: Task-Only Representation Formation

The encoder receives only an opaque 16-way one-hot leaf identifier. Training
code must not pass $p,c,q$, their embeddings, or any semantic auxiliary loss:

$$
h=Ee_{p,c}\in\mathbb R^4,
\qquad
\widehat y=z^\top V_dh.
$$

$E\in\mathbb R^{4\times16}$ and $V_d\in\mathbb R^{512\times4}$ are learned
from scalar task MSE. Initialize both with independent Normal$(0,0.02)$ values.
Train 1,024 steps, exact-balanced batch 64 (four samples per leaf), AdamW
learning rate `0.005`, betas `(0.9,0.999)`, weight decay `1e-4`, gradient clip
`1.0`, and the paired streams defined in Section 7. There is no early stopping.

Audit

$$
\widehat r_{p,c}=V_dEe_{p,c},
$$

not raw $h$. The transformation $E\mapsto TE$, $V_d\mapsto V_dT^{-1}$ leaves
the function unchanged, so raw-hidden PCA and raw variance are explicitly
forbidden as scientific evidence.

Required representation outputs are:

1. coefficient reconstruction NMSE over all 16 teacher operators;
2. exact-oracle multiclass hard-margin feasibility and distance of every
   parent convex hull to the origin;
3. learned-operator parent readout trained on child values `{0,2}` and tested
   on `{1,3}`, then reversed, using one fixed L2 multinomial logistic rule;
4. normalized low-tail parent margin from those out-of-child predictions;
5. parent-subspace energy in cumulative PCA dimensions for the $\beta=4$
   companion.

Stage-R admission requires the upper paired-seed 95% bound of coefficient NMSE
not exceed `0.02`; work cross-child parent balanced accuracy lower bound at
least `0.95`; fail upper bound at most `0.40` (chance `0.25`); exact work
hard-margin feasibility and exact fail shared-origin convex-hull intersection;
and companion work accuracy lower bound at least `0.95` while at least `0.90`
of the first-two-PC energy lies in the child $V$ subspace. A failure of these
manipulation/capability gates makes the whole experiment `Insufficient`.

## 4. Stage M: Common Expert Bank And Task-Only Routers

All models own the same eight learnable coefficient experts
$w^A_0,\ldots,w^A_3,w^B_0,\ldots,w^B_3\in\mathbb R^{512}$, initialized from
one paired Normal$(0,0.02)$ tensor per seed. Every example activates exactly
one expert in each bank and predicts the sum of their scalar responses. The
common expert parameter count is `4096`; active expert dot-product work is
exactly `2×512` multiplies per example.

Training is task MSE plus the same unlabeled Switch-style load-balancing loss
of weight `0.01` for each bank. Parent, child, leaf, route, and expert labels
are forbidden. A selected expert output is multiplied by its pre-renormalized
softmax probability so task gradients reach the selected Gate; top-1 indices
remain discrete. Test metrics report both this trained weighted output and the
hard unit-weight top-1 output, with the trained weighted output frozen as
primary.

### 4.1 Router variants

- **`H_p`:** root input is only $u(p)$. Normalize it and four learnable
  two-dimensional A prototypes; cosine scores use a learnable positive
  temperature. If root $i$ is selected, a learnable $T_i\in\mathbb R^{2\times2}$
  transforms $u(q)$. The selected-probability-weighted transform is compared
  to four normalized B prototypes with another learnable temperature.
- **`H_q`:** isomorphic to `H_p` with $p$ and $q$ exchanged. No parameter or
  optimizer setting differs.
- **`flat_linear`:** independent affine four-way Gates for A and B banks on
  the full four-dimensional $s$.
- **`xmoe_style`:** one learned $4\rightarrow3$ projection, L2-normalized
  projected tokens, two banks of four normalized three-dimensional
  prototypes, and one learned positive temperature per bank. “Style” is
  mandatory: this is not claimed to reproduce X-MoE training or discover
  semantics.
- **`flat_nonlinear`:** a shared `4→4` affine layer, GELU, and `4→8` affine
  output split into the two banks. Its roughly 60 Router parameters exceed the
  hierarchy's roughly 34 and make it the decisive generic-nonlinearity control.

No dummy parameters are allowed. The implementation records exact trainable
counts. Including common experts, maximum-minus-minimum total parameter count
must be below `1%`; analytic total forward FLOPs must differ by below `5%`.

## 5. Optimization, Pairing, And Budgets

Use exactly 20 seeds `151120..151139`. One `torchrun --nproc_per_node=4`
process receives seeds whose zero-based seed index modulo four equals its rank.
For a seed, generate immutable balanced train/evaluation streams first, then
run every model under work and fail. Identical architecture variants reuse the
same initial Router/expert tensors across work/fail; all variants reuse the
same expert base tensor and the same ordered data.

Functional training uses exact-balanced batch 64, 512 steps, AdamW learning
rate `0.003`, betas `(0.9,0.999)`, weight decay `1e-4`, gradient clip `1.0`, and
no scheduler or early stopping. Evaluate at steps
`1,2,4,8,16,32,64,128,256,512` on one frozen noise-free test bank containing
256 examples per leaf. Step 128 (8,192 training examples) is the registered
fixed-budget performance point; step 512 is a capability and convergence
diagnostic only.

All random streams are keyed by `(root_seed, seed, stage, purpose)` rather than
call order. Model execution order may not change generated data. No failed seed
may be deleted or replaced.

## 6. Metrics And Primary Analysis

For exact conditional-mean target $y^\star=\theta^\top z$, define

$$
NMSE=\frac{\mathbb E[(\widehat y-y^\star)^2]}{\alpha^2+\beta^2}.
$$

For each seed/model/condition, integrate NMSE by the trapezoid rule over log
cumulative training examples and divide by the total log range. This normalized
area under the learning curve is `AULC`; lower is better.

The primary alignment interaction is

$$
I=\frac12[(A_{H_q,work}-A_{H_p,work})+(A_{H_p,fail}-A_{H_q,fail})].
$$

Normalize its practical magnitude by the mean of `flat_nonlinear` work/fail
AULCs. Use 10,000 paired seed-bootstrap draws, root seed `151104`, always
resampling whole seed records and keeping every model/condition paired. Report
medians and percentile 95% intervals. There is no independent-run or
population-generalization claim.

Secondary outputs include step-128 and step-512 NMSE, noisy MSE, per-bank route
accuracy relative to the oracle decomposition, expert-load shares, effective
expert count, load CV, selected confidence, expert cosine recovery, parameter
counts, FLOPs, and wall time. Wall time is descriptive and never substitutes
for cumulative examples or active FLOPs.

## 7. Oracle Ceilings And Failure Localization

Before the learned comparison, compute and record:

1. **closed-form additive ceiling:** exact teacher reconstruction by the
   matching A/B operator bank;
2. **oracle route + learned experts:** train the same experts with true bank
   indices and no learned Router;
3. **learned route + true experts:** freeze the exact A/B operator bank and
   train each Router alone.

The exact ceiling must have noise-free NMSE below `1e-10`. The upper
paired-seed 95% bound of step-512 oracle-route/learned-expert NMSE must be at
most `0.02` in work and fail. Otherwise the model or budget lacks basic
capacity and the experiment is `Insufficient`.

At step 512, every primary comparison model must route at least `0.10` and at
most `0.40` of the balanced test rows to each expert in each bank, or its
common load guard fails. The analytic parameter/FLOP guards in Section 4 must
also pass.

## 8. Pass, Fail, And Insufficient

E02 is a scientific **Pass** only if all of the following hold:

1. Sections 2, 3, 4, and 7 invariants, representation admissions, oracle
   ceilings, load guards, parameter guards, and FLOP guards pass;
2. median $I$ divided by mean flat-nonlinear AULC is at least `0.05`, and the
   paired bootstrap lower 95% bound of $I$ is positive;
3. in work, `H_p` beats each of `H_q`, `xmoe_style`, and `flat_nonlinear` in
   both AULC and step-128 NMSE with positive paired lower bounds;
4. in fail, `H_q` beats each of `H_p`, `xmoe_style`, and `flat_nonlinear` under
   the same two tests;
5. the aligned hierarchy's step-512 median NMSE is at most `0.05` in both
   conditions.

If every admission and oracle guard passes but the upper 95% bound of $I$ is
non-positive, report `FAIL_NO_ALIGNMENT_EFFECT`. If alignment is positive and
the hierarchy beats flat-linear or X-MoE-style but does not beat
`flat_nonlinear`, report `FAIL_GENERIC_NONLINEARITY_SUFFICIENT`; this supports
nonlinearity, not a hierarchy-specific advantage. If the hierarchy and flat
nonlinear intervals overlap without either registered Fail condition, report
`Insufficient`, not a directional claim.

Any generator/representation/oracle/capacity/load/compute failure, missing
seed, numerical non-finiteness, or unregistered retry is `Insufficient`.

## 9. Bottom-Level Diagnosis Matrix

| Observed pattern | Frozen interpretation |
| --- | --- |
| work operator geometry forms but MoE does not improve | representation readability is not Router/expert utility |
| `H_p` and `H_q` both win in both conditions | regularization, parameterization, or implementation effect; not grouping alignment |
| hierarchy beats linear/X-MoE-style but ties flat nonlinear | an interaction/nonlinearity is needed; hierarchy adds no established value |
| flat controls differ materially between work and fail | violated permutation/data/init pairing; `Insufficient` |
| `H_p` wins work and `H_q` wins fail, but neither beats flat nonlinear | correct functional grouping matters inside the tree family, not beyond generic nonlinear routing |
| oracle route + learned experts is good; learned route + true experts is bad | Router optimization bottleneck |
| learned route + true experts is good; oracle route + learned experts is bad | expert estimation or sample-budget bottleneck |
| semantic route association is high but task NMSE is unchanged | semantics is accessible but not useful to the expert bank |

The fail condition's $H_q$ is a functional-grouping counterfactual. Its success
does not make $q$ a true semantic parent or show that natural-language
taxonomies should be shuffled.

## 10. Required Artifacts And Figure Contracts

Required machine artifacts are generator/operator manifests and hashes;
per-seed representation, learning-curve, route, load, oracle, parameter and
FLOP ledgers; bootstrap draws; `results.json`; environment and code receipts;
and a completion audit.

Required figures are:

1. canonical teacher and learned operator geometry for work/fail, including
   parent convex hulls and the $\beta=4$ PCA companion;
2. work/fail NMSE learning curves for all Router variants versus cumulative
   examples;
3. the paired alignment-interaction and aligned-versus-flat contrasts;
4. a failure-localization panel comparing the three oracle ceilings.

Each rendered figure must state the question, metric/formula, unit,
aggregation, exact data source, axes/legend, allowed conclusion, and
limitation. A visual cannot override the registered machine verdict.

## 11. Claim Boundary And Stop Rule

A Pass would establish that, in this fixed four-parent linear-teacher system,
permutation-equivalent tasks with coherent parent gradients form different
parent geometry and that a provided correct grouping prior improves sparse
compositional routing beyond a parameter-richer generic nonlinear Router. It
would not establish that the network autonomously discovered the parent, that
gradient consistency is universally necessary, or that Qwen/real-language
training benefits.

A Fail retains the exact lower-level result: frequency and teacher-function
multisets were insufficient to determine parent geometry, and/or generic
nonlinearity was sufficient for function. The run stops after the frozen
diagnosis; no post hoc sweep, new baseline, changed supervision, or extra seed
may rescue it.

## 12. Pre-Run Supersession Ledger

At `2026-08-29T15:45:00Z`, before implementation or any scientific run, this
Protocol was made non-executable. An audit against the 2026-08-24 advisor
meeting established that its simultaneous two-bank `H_p/H_q` construction is
not the requested progressive $1\rightarrow2\rightarrow4$ mechanism: it has no
stagewise freeze, no ancestor function/gradient residualization, and no
counterfactual expert-utility supervision. Stage R and Stage M also use
different representation inputs, so their outputs cannot support the claimed
representation-to-routing mediation chain.

The frozen body above is retained as provenance and is not silently rewritten.
The scientifically different successor is
`A15_11_E03_counterfactual_utility_residual_tree`. The user's resource boundary
also forbids the H100 profile recorded by this superseded draft. E02 must never
be submitted or cited as executed evidence.
