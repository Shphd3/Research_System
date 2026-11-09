---
experiment_id: A15_11_E03_counterfactual_utility_residual_tree
status: APPROVED_FOR_IMPLEMENTATION_SMOKE_FULL_RUN
created: 2026-08-29
primary_anchor: A15_11_gradient_consistent_hierarchical_routing
implementation_authorized: true
smoke_authorized: true
full_run_authorized: true
scientific_contract_frozen: true
scientific_body_frozen_at: 2026-08-29T16:35:39Z
resource_profile: 5090-8-spot
---

# Protocol: Counterfactual-Utility Supervision In A Frozen 1-to-2-to-4 Residual Expert Tree

## 0. Approval Snapshot

| Field | Frozen value |
| --- | --- |
| Authorization | the 2026-08-29 request delegates a readable Protocol and autonomous implementation, smoke, and full execution; post-result human judgment remains undelegated |
| Unique question | when a provided parent-first residual factorization is functionally correct, does counterfactual expert-utility supervision make the useful routing partition easier to learn and improve sample efficiency beyond a matched flat nonlinear MoE; and what exact structural obstruction explains failure when that factorization is wrong? |
| Advisor arm | one common rank-one expert, then two rank-one experts, then four rank-one experts; freeze every completed stage; train and route only on the unexplained function residual |
| AI audit | a matched \(2\times2\) crossing conditional tree versus flat nonlinear routing with task-only versus counterfactual-utility Router supervision |
| Primary metric | noise-free normalized mean-squared-error area under the learning curve versus cumulative examples |
| Seeds | `151130` through `151137`, paired across every condition and model |
| Resource | one SPOT worker exposing exactly eight RTX 5090 GPUs; one seed per process; H100 is forbidden |
| Cannot claim | autonomous semantic ontology discovery, a real-Qwen utility benefit, or a universal advantage of hierarchy |

This Protocol replaces no result. It is a new successor because the earlier E02
simultaneous two-bank design did not instantiate the advisor's progressive
\(1\rightarrow2\rightarrow4\) freeze-and-residual mechanism.

## 1. Objects And The Four Non-Equivalent Claims

- **Semantic variables:** balanced binary parent \(p\) and child \(b\).
- **Surface code:** \(q=pb\). The Router observes \(s=(p,q)\), never \(b\) or a
  route label.
- **Representation accessibility:** whether a registered linear readout can
  recover a named label from a named held-out representation.
- **Router accessibility:** whether the deployed Gate scores can rank the
  lower-loss action.
- **Counterfactual expert utility:** the loss improvement from replacing the
  current action by one equal-compute candidate for the same example and
  frozen ancestor state.
- **Functional gain:** lower held-out task error or less exposure to reach a
  fixed error.

Semantic readability, utility readability, native routing, and functional gain
are measured separately. In particular, \(b=pq\) is not globally affine-linearly
separable from \(s\), although it is linearly separable after conditioning on
\(p\) or on \(q\).

## 2. Generator And Exact Work/Fail Pair

Draw \(p,b\) independently and uniformly from \(\{-1,+1\}\), set \(q=pb\), draw
\(z\sim\mathcal N(0,I_8)\), and use \(s=(p,q)\). There is no observation noise:
the experiment isolates routing and rank rather than denoising. Construct
three canonical, doubly orthogonal rank-one matrices

\[
C=u_0v_0^\top,\qquad A=u_1v_1^\top,\qquad B=u_2v_2^\top
\]

as the first three diagonal coordinate projectors in
\(\mathbb R^{8\times8}\). Targets are

\[
\Theta^{work}_{p,b}=C+pA+bB,
\qquad
\Theta^{fail}_{p,b}=C+qA+bB,
\]

\[
y=\Theta z.
\]

Each training step draws 16 independent \(z\) blocks, crosses every block with
all four \((p,b)\) leaves, and then permutes the resulting 64 rows. The frozen
test bank uses the same complete-factorial construction. Thus the statistical
independence unit is a \(z\) block, not an individual row; every row still has
the registered standard-normal marginal, while finite-batch parent and child
averages cancel exactly. Each seed reuses exactly the same ordered
\((p,b,q,z)\) rows in work and fail. The implementation must verify before training that the two conditions
have the same four teacher matrices as a multiset under
\((p,b)\leftrightarrow(q,b)\), uniform leaf counts, zero Bayes noise, and mean
noise-free signal energy \(3\).

After removing \(C\), define

\[
\rho_g=
\frac{\mathbb E_g\|\mathbb E[\Theta-C\mid g]\|_F^2}
{\mathbb E\|\Theta-C\|_F^2}.
\]

The exact identities are

\[
(\rho_p^{work},\rho_q^{work})=(1/2,0),
\qquad
(\rho_p^{fail},\rho_q^{fail})=(0,1/2).
\]

They isolate functional grouping rather than frequency, entropy, label set,
noise, or teacher-function capacity.

## 3. Shared Progressive Expert System

Every model owns exactly seven trainable \(8\times8\) expert matrices organized
as one root, two level-one experts, and four level-two experts. Each matrix is
stored densely for a gauge-free audit. After every update, impose rank one and
ancestor orthogonality with an exact finite enumeration. For an unconstrained
candidate \(M\) and rank-one ancestors \(a_jb_j^\top\), the constraint

\[
\langle uv^\top,a_jb_j^\top\rangle_F
=(u^\top a_j)(v^\top b_j)=0
\]

means that each ancestor must be assigned either to the left constraint
\(u\perp a_j\) or to the right constraint \(v\perp b_j\). Enumerate all at most
\(2^m\) assignments, project \(M\) into the corresponding left and right
orthogonal complements, take that projected matrix's best rank-one singular-
value approximation, and retain the Frobenius-nearest feasible candidate with
deterministic lexicographic tie breaking. Here \(m\leq3\). A zero or numerically
infeasible candidate stops the cell. Normalized ancestor overlap must be at
most `1e-6`; this is checked rather than assumed. Inference activates exactly
one expert at each level and sums their outputs, so every model uses three
active rank-one operators.

Every newly active expert is constrained once before its first candidate
forward and again after every optimizer step. The ledger distinguishes this
stage-local step-zero feasibility projection from learned updates and records
pre/post overlap, pre/result numerical rank, feasible branch, and final guard.

Training is stagewise:

1. train the single common expert on \(y\) for 128 steps, then freeze it;
2. train two new experts for 128 steps on the function residual unexplained by
   the common expert, then freeze them and their Gate;
3. train four new experts for 128 steps on the residual unexplained by the
   frozen root and selected level-one expert.

For a new expert matrix \(W\), the constrained update is rank one and has at most
the registered normalized overlap with the frozen ancestor span. This makes
“remove common” a concrete function/gradient operation, not subtraction of the
common expert's output as a Router feature. The code records the selected
enumeration branch, pre/post overlap, numerical rank, and immutable
expert/Router freeze hashes. Any frozen parameter change is fatal.

All four models use the same complete-factorial batch of 64 rows from 16
independent \(z\) blocks, the same ordered rows, 128 steps per stage, the same
initial expert tensors, and no early stopping. Use Adam with betas
`(0.9,0.999)`, zero weight decay, expert learning rate `0.03`, Router learning
rate `0.01`, gradient-norm clip `5.0`, utility coefficient `1.0` for utility
arms and zero for task-only arms, and common load coefficient `0.01`. The
label-blind smoke uses only the non-registered seed `151129`, exercises all
eight work/fail-by-arm cells for two steps per stage on CPU, and persists only
guard booleans. It may establish numerical stability but may not persist or
select a scientific condition, registered seed, threshold, endpoint, NMSE,
utility metric, bootstrap result, or figure.

## 4. Matched \(2\times2\) Intervention

The only two axes are Router structure and Router supervision:

| Router structure | Task loss only | Counterfactual utility |
| --- | --- | --- |
| conditional \(1\rightarrow2\rightarrow4\) | `H_task` (advisor realization) | `H_util` (AI-audited utility realization) |
| flat nonlinear | `F_task` | `F_util` (necessary utility-control arm) |

All four instantiate the same Router MLP input width, hidden width, stage-one
two-way head, and stage-two four-way head. They share exact Router parameter
counts. `H_*` masks the stage-one input to \(p\) and, at stage two, selects only
the two children of the chosen \(p\) branch while reading \(q\). `F_*` reads the
full \(s\) and performs unrestricted two-way and four-way decisions. The
hierarchical arms therefore test a provided parent-first structural prior; they
do not claim to discover \(p\) without a prior.

All decisions use hard top one with the same straight-through estimator. At
training time every arm evaluates every same-level candidate expert for every
example, even when utility loss has zero weight. This matches candidate-forward
compute and produces a common diagnostic ledger.

For residual target \(r_i\) and candidate expert \(e\), define

\[
U_{ie}=\|r_i\|_2^2-\|r_i-W_ez_i\|_2^2,
\qquad
t_i=\arg\max_e U_{ie}.
\]

The target is stop-gradient. `H_util` and `F_util` add cross entropy between
the Gate and \(t_i\); `H_task` and `F_task` set that utility coefficient to zero
but still compute the same ledger. For every routed arm and every head with
\(K\) available candidates, let \(\bar p_e\) be candidate \(e\)'s mean softmax
probability in the batch and add the identical differentiable load penalty

\[
L_{bal}=K\sum_{e=1}^{K}(\bar p_e-1/K)^2
\]

with coefficient `0.01`. Utility is derived from \(y\) and is additional pseudo-
supervision; it must never be described as supervision-matched to task-only
routing.

## 5. Exact Capacity Claims And Falsifier

For the parent-first tree in work, the oracle decomposition is

\[
C\quad+\quad pA\quad+\quad bB,
\]

and has zero noise-free error. In fail, the level-one conditional mean given
\(p\) is zero. Each leaf then must represent

\[
qA+bB=b(pA+B),
\]

which has two equal nonzero singular values because \(A\) and \(B\) are doubly
orthogonal. By the Eckart--Young rank-one approximation theorem, at least one
unit of operator energy remains. Since total signal energy is three,

\[
NMSE_{H,fail}^{oracle}=1/3.
\]

Counterfactual utility cannot break this structural lower bound because
`H_util` retains the same \(p\)-first mask. A flat oracle can group by \(q\) first
in fail and attains zero error. Any trained hierarchical fail arm materially
below the registered \(1/3\) floor indicates rank, mask, or freeze leakage and
makes the run `Insufficient`.

## 6. Representation And Utility Audit

Before training, an exact linear-feasibility test must show that \(p\) and \(q\)
are globally linearly separable from \(s\), \(b=pq\) is not, and \(b\) is separable
inside each fixed \(p\) or \(q\) branch. These are finite-support identities, not
sample estimates.

At every registered evaluation step, separate representation potential from
native Gate use. For representation potential, generate two fixed, disjoint,
exact-balanced banks named `hidden_probe_calibration` and
`hidden_probe_test`; each contains 64 rows from 16 independent \(z\) blocks
crossed with all four leaves, uses `stage=0, step=0`, and is reused across
checkpoints for the same seed. Fit a closed-form one-versus-rest ridge readout
from Router hidden features plus an unpenalized intercept to the current
stop-gradient utility argmax. The objective is scaled by sample mean and uses
fixed \(\lambda=10^{-3}\) with no tuning. At hierarchical stage two, fit and
evaluate separately inside each deployed parent mask and macro-average the
branches. This probe is a diagnostic only and never enters the Section 8
verdict.

Record both the hidden probe and deployed Gate:

- hidden-probe balanced accuracy, negative log likelihood, normalized target-
  versus-best-wrong margin fifth percentile, and evaluated branch count;
- Gate balanced accuracy, negative log likelihood, and the same normalized
  margin fifth percentile for the current counterfactual-best candidate;
- chosen-expert regret \(\max_e U_{ie}-U_{i,\hat e}\), route agreement with the
  counterfactual-best candidate, effective expert count, load coefficient of
  variation, and per-expert load.

For balanced accuracy, macro-average recall over counterfactual target classes
present in the test bank. Stage zero has no Router, so Router-only fields are
explicitly null rather than assigned artificial perfect values. A positive
native Gate margin says that the utility decision is exposed to the deployed
linear readout at that checkpoint. Hidden-probe access without native Gate
access localizes an optimization/readout failure; failure of both localizes a
representation or input-information obstruction. Neither pattern by itself
establishes lower task loss; regret and held-out NMSE provide the separate
functional tests.

## 7. Metrics, Pairing, And Contrasts

On a frozen balanced noise-free test bank, define

\[
NMSE=\frac{\mathbb E\|\widehat y-\Theta z\|_2^2}
{\mathbb E\|\Theta z\|_2^2}.
\]

Evaluate after stage-local steps `1,2,4,8,16,32,64,128`. Integrate NMSE by
the trapezoid rule over log cumulative training examples and normalize by the
log range. Lower area under the learning curve (`AULC`) is better. The stage-two
endpoint NMSE is the fixed-budget performance metric.

For each condition, report paired whole-seed contrasts

\[
S_H=A(H_{task})-A(H_{util}),
\qquad
S_F=A(F_{task})-A(F_{util}),
\]

\[
A_T=A(F_{task})-A(H_{task}),
\qquad
A_U=A(F_{util})-A(H_{util}),
\qquad
X=S_H-S_F.
\]

Use all eight seeds and 10,000 paired whole-seed bootstrap draws with root seed
`151124`. Report the empirical seeds, medians, and percentile 95% intervals;
do not make a population-generalization claim from eight optimizer seeds.
For the mechanism gate, also register the paired whole-seed contrast

\[
M=AULC_{fail}(H_{task})-AULC_{work}(H_{task}),
\]

where a positive value means the advisor realization learns the aligned work
condition faster than the permutation-equivalent fail condition.

Also report unnormalized MSE, numerical rank, projection leakage, stored and
active expert parameters, Router parameters, training all-candidate expert-
forward FLOPs, inference expert-path FLOPs, step time, effective expert count,
and load coefficient of variation. The FLOP convention counts one multiply or
one add as one operation: a dense \(8\times8\) matrix-vector product costs 120
FLOPs. Thus the final three-expert path costs \(3\times120+16=376\) expert/output-
sum FLOPs per example. Router, loss, constraint projection, backward, optimizer,
and diagnostic hidden-probe work are excluded and named as exclusions; they
are identical or non-primary overhead rather than silently folded into the
expert-path count. Wall time is descriptive and never replaces cumulative
examples or FLOPs.

## 8. Admission, Verdict, And Failure Localization

The run is eligible only if generator identities hold within `1e-10`; exact
oracle NMSE is below `1e-10` for hierarchical work and flat work/fail; the
hierarchical fail oracle equals \(1/3\) within `1e-10`; every expert has numerical
rank at most one; ancestor projection leakage is below `1e-6`; freeze hashes,
paired streams, parameter counts, candidate-forward counts, and output schemas
match; and no seed is missing or replaced.
For the learned-model leakage guard, “materially below” the analytic fail floor
means endpoint NMSE below \(1/3-0.02\) in any hierarchical fail cell; the `0.02`
allowance is only a numerical/training-deviation guard and does not redefine
the analytic oracle value.

Verdicts are layered rather than collapsed:

1. **`MECHANISM_SUPPORTED`:** eligible `H_task` has an eight-seed median work
   endpoint NMSE at most `0.05`, an eight-seed median fail endpoint NMSE at
   least `0.25`, and a positive paired 95% lower bound for \(M\).
2. **`UTILITY_EFFECT_TREE` / `UTILITY_EFFECT_FLAT`:** in work, the
   corresponding \(S_H\) or \(S_F\) AULC lower bound is positive and the utility
   arm's eight-seed median endpoint NMSE is not worse than its task-only arm by
   more than `0.01`. This is a supervision result, not an architecture result.
3. **`HIERARCHY_GAIN_TASK` / `HIERARCHY_GAIN_UTILITY`:** in work, the
   corresponding \(A_T\) or \(A_U\) lower bound is positive, its median is at least
   five percent of the matched flat AULC, and the hierarchical endpoint is no
   worse. Only `HIERARCHY_GAIN_UTILITY` permits the phrase “tree bias adds value
   under the same utility supervision.”
4. **`GENERIC_NONLINEARITY_OR_UTILITY_SUFFICIENT`:** the mechanism gate passes
   and, under utility supervision in work, flat either beats the hierarchy
   (the \(A_U\) 95% upper bound is below zero) or is practically equivalent (the
   entire \(A_U\) 95% interval lies within plus or minus five percent of the
   eight-seed median flat AULC); in either case the flat median endpoint must
   be no worse than the hierarchical median endpoint by more than `0.01`.
   Retain the structural theorem and reject an empirical hierarchy advantage.
   Failure to establish `HIERARCHY_GAIN_UTILITY` alone is indeterminate and
   does not trigger this sufficiency verdict.
5. **`LEARNED_MECHANISM_FAIL`:** all exact guards pass but `H_task` does not
   realize the work/fail separation. Diagnose route optimization, expert
   estimation, or insufficient budget using oracle, regret, rank, and load
   ledgers.
6. Any identity, rank, mask, freeze, load, compute, numerical, or completion
   guard failure is **`Insufficient`**.

Neither a utility effect nor a tree-family alignment pattern may be promoted
to hierarchy gain without the matched `F_util` comparison. The outer machine
status is `LAYERED_VERDICTS_RECORDED` when guards pass and `Insufficient` when
they do not; it must not collapse the mechanism, utility, and architecture
fields into one favorable label.

## 9. Execution And Required Artifacts

The full run uses workspace `share-space`, AEC2
`computing-cluster-5090-01g`, one `n12lp.nn.i10a.8` SPOT worker, normal
priority, and eight processes. Preflight requires exactly eight visible RTX
5090 devices and rejects H100. Seeds are assigned by zero-based seed index
modulo eight. No local scientific GPU execution or H100 fallback is allowed.

Required artifacts are immutable generator and split manifests; matrices and
hashes; exact oracle/rank certificates; per-seed/per-step loss, route, utility,
margin, load, projection, parameter, and FLOP ledgers; paired bootstrap draws;
`results.json`; environment/code receipts; producer-local figures; and
`completion_audit.json`.

Figures must show: (1) the work/fail teacher decomposition and analytic floor;
(2) four-arm NMSE learning curves; (3) \(S_H,S_F,A_T,A_U\) paired contrasts;
and (4) representation margin, route regret, and oracle/learned failure
localization. Every figure states its question, metric/unit, source,
aggregation, allowed conclusion, and limitation.

## 10. Claim Boundary And Stop Rule

A positive result can establish only that a provided correct \(p\)-first
factorization and/or direct counterfactual-utility supervision improves a
controlled progressive rank-one MoE under matched candidate compute. The
permutation-equivalent fail can identify the bottom-level obstruction as a
wrong grouping that forces two orthogonal residual functions through one
rank-one leaf.

It cannot establish that natural-language semantics have this tree, that a
network will discover the tree without the provided structural cue, that hard
common-direction deletion is safe in non-orthogonal tasks, or that Qwen NLL
will improve. The run stops after the registered eight seeds and frozen
verdict. Any repair or hyperparameter change is a separately registered
successor.

## 11. Pre-Result Implementation Amendments

Between `2026-08-29T16:00:50Z` and `2026-08-29T16:35:39Z`, before any
scientific smoke or full result was accepted, implementation and diagnostic
details were made explicit without changing the question, scientific arms,
registered full-run seeds, thresholds, or primary comparison:

1. observation noise was fixed to zero and the three teacher operators were
   fixed to canonical doubly orthogonal coordinate projectors, so the analytic
   mechanism and \(1/3\) failure floor are exact rather than Monte Carlo claims;
2. optimizer, clipping, utility, and shared load-penalty coefficients were
   frozen as stated in Sections 3 and 4;
3. a one-step non-scientific implementation check showed that the provisional
   50-step alternating projection could stop above the registered `1e-6`
   overlap threshold. The tolerance was not relaxed. It was replaced by the
   finite left/right constraint enumeration in Section 3, which solves the
   rank-one ancestor-orthogonality constraint by checking all feasible
   branches and remains fail-closed under the original threshold.
4. the label-blind smoke was isolated to non-registered seed `151129`, and its
   persisted schema was restricted to numerical guard booleans rather than
   checkpoint results;
5. a fixed closed-form hidden-state ridge probe was added only to distinguish
   representation potential from native Gate use after failure. Its banks,
   regularization, conditional fitting rule, and non-decision role are frozen
   in Section 6;
6. parameter and FLOP ledgers were given the explicit dense-execution counting
   convention in Section 7, including the operations deliberately excluded;
7. an independent contract audit found that “flat matches” had not been
   operationalized. Section 8 therefore registered a two-sided five-percent
   AULC equivalence interval and endpoint guard before results, and prohibited
   collapsing the layered verdicts into the mechanism label.

No scientific condition, learning curve, endpoint, contrast, or seed result
was inspected when these amendments were frozen.
