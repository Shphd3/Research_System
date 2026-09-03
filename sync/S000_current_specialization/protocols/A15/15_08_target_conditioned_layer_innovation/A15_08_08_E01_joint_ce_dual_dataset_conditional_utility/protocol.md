# A15_08_08_E01: Joint-CE dual-dataset conditional utility repair

Status: `APPROVED_FOR_IMPLEMENTATION_AND_RUN`

Approval source: the researcher explicitly approved simultaneous cross-entropy
training of the two branches on both frozen datasets on 2026-08-20.

Scope: this is a bounded measurement repair of the existing A15_08 functional
admission test. It does not replace the active A15_07 meeting-cycle question,
and it does not admit any subspace to a Router.

## 1. Question

After removing the sequential residual-fitting readout, does the paired update
$R_{U,\ell}$ reduce held-out within-parent or within-domain classification
cross-entropy beyond an exactly equivalent same-$X$ two-branch control?

## 2. Frozen evidence

No model extraction or residualizer is retrained.

- Synthetic taxonomy: the frozen Qwen3-8B caches from
  `20260816_a15_08_02_e01_layerwise_conditional_fine_added_accessibility`.
  There are 8 parent-conditioned 8-way tasks and independent TRAIN,
  DEVELOPMENT, and CONFIRMATION expressions.
- CLINC150: the frozen Qwen3-8B caches from
  `20260819_a15_08_07_e01_clinc150_layerwise_added_accessibility_and_pca`.
  There are 10 domain-conditioned 15-way tasks and independent TRAIN,
  VALIDATION, and TEST utterances.
- Eligible blocks are 2--36. Block 1 remains structurally ineligible.
- $X_\ell$ and $R_{U,\ell}$ keep their existing definitions and frozen
  residualizer states. Standardization is fitted on TRAIN only and reused on
  DEVELOPMENT and CONFIRMATION/TEST.

## 3. Joint readouts

For each block and each parent/domain, fit three multinomial linear-softmax
models directly with mean cross-entropy plus an L2 penalty. Each standardized
4096-dimensional feature block is divided by $\sqrt{4096}$ before fitting.

1. Old-state baseline:
   $$f_X(x)=b+xW.$$
2. Same-$X$ identity control:
   $$f_{XX}(x)=b+\frac{x}{\sqrt 2}W_1+\frac{x}{\sqrt 2}W_2.$$
   Joint L2 regularization makes its minimum-norm effective coefficient and
   objective exactly equal to $f_X$. It is therefore materialized from the
   selected $f_X$ coefficient as $W_1=W_2=W/\sqrt 2$, rather than being
   contaminated by a second finite-precision optimization. Any material
   prediction difference is an implementation failure.
3. Paired update model:
   $$f_{XR}(x,r)=b+xW_X+rW_R.$$
   It nests the old-state model at $W_R=0$.

All finite two-branch candidates are optimized jointly rather than fitting a
second correction to the first model's residual. First, DEVELOPMENT selects
the old-state penalty $\lambda_X$. The paired model then keeps that penalty on
$W_X$ and DEVELOPMENT selects a separate update penalty $\lambda_R$ from
`1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 1e-1, 1, 10`, plus an explicit
$\lambda_R=\infty$ candidate with $W_R=0$. Consequently, the augmented model
can exactly fall back to the old-state model instead of being forced to use a
noisy 4096-dimensional branch. TRAIN fits parameters, DEVELOPMENT selects the
penalties, and the sealed split is evaluated once. Optimization is
deterministic full-batch L-BFGS from zero initialization with explicit
convergence receipts.

## 4. Decisive estimand and controls

The primary per-record estimand is

$$
T_{\ell,i}=\operatorname{CE}_i(f_{XX})-
            \operatorname{CE}_i(f_{XR}).
$$

Positive values mean that the correctly paired $R_U$ branch predicts the fine
label better than an exactly equivalent same-$X$ two-branch model under the
same direct objective.

Required guards:

- identity: $f_X$ and $f_{XX}$ must agree numerically in held-out CE and
  accuracy; the absolute mean CE difference must be at most $10^{-4}$ and the
  maximum absolute per-row CE difference at most $10^{-3}$;
- pairedness diagnostic: keep the fitted $f_{XR}$ fixed and permute TEST /
  CONFIRMATION $R_U$ within its parent/domain for 64 seeds. Its benefit should
  collapse if the model uses sample-specific update information;
- convergence: every selected fit must be finite, its final first-order
  gradient norm must be reported, and the selected fit must have gradient norm
  at most $10^{-3}$.

## 5. Inference and decision

Use 2,000 class-stratified bootstrap draws shared across blocks. A single
max-absolute centered bootstrap critical value gives simultaneous 95%
intervals over blocks 2--36 within each dataset.

- `CONFIRMED_POSITIVE`: the simultaneous lower bound of $T_\ell$ is above 0,
  the same-$X$ identity guard passes, and the paired point estimate exceeds
  the 95th percentile of the permuted-pair diagnostic.
- `CONFIRMED_NONPOSITIVE`: the simultaneous upper bound is at most 0.
- otherwise: `UNRESOLVED`.

The two datasets are judged separately. Cross-dataset raw cross-entropy
magnitudes are not compared as if they had the same class count. This repair
can establish only conditional linear accessibility under a joint CE head; it
cannot establish model understanding, low-rank sufficiency, or Router utility.
