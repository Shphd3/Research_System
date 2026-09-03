---
experiment_id: A15_11_E03H_counterfactual_utility_residual_tree_h100
status: APPROVED_FOR_IMPLEMENTATION_SMOKE_FULL_RUN
created: 2026-08-29
primary_anchor: A15_11_gradient_consistent_hierarchical_routing
implementation_authorized: true
smoke_authorized: true
full_run_authorized: true
scientific_contract_frozen: true
scientific_body_frozen_at: 2026-08-29T16:18:22Z
resource_profile: h100-4-reserved
---

# Protocol: Counterfactual-Utility Supervision In A Frozen 1-to-2-to-4 Residual Expert Tree

## 0. Approval Snapshot

| Field | Frozen value |
| --- | --- |
| Authorization | the 2026-08-29 request delegates a readable Protocol and autonomous implementation, smoke, and full execution; post-result human judgment remains undelegated |
| Unique question | when a provided parent-first residual factorization is functionally correct, does counterfactual expert-utility supervision make the useful routing partition easier to learn and improve sample efficiency beyond a matched flat nonlinear MoE; and what exact structural obstruction explains failure when that factorization is wrong? |
| Advisor arm | one common rank-one expert, then two rank-one experts, then four rank-one experts; freeze every completed stage; train and route only on the unexplained function residual |
| AI audit | a matched $2\times2$ crossing conditional tree versus flat nonlinear routing with task-only versus counterfactual-utility Router supervision |
| Primary metric | noise-free normalized mean-squared-error area under the learning curve versus cumulative examples |
| Seeds | `151130` through `151137`, paired across every condition and model |
| Resource | one reserved worker exposing exactly four H100 GPUs; two registered seeds per process by seed-index modulo four |
| Cannot claim | autonomous semantic ontology discovery, a real-Qwen utility benefit, or a universal advantage of hierarchy |

This Protocol replaces no result. It is a new successor because the earlier E02
simultaneous two-bank design did not instantiate the advisor's progressive
$1\rightarrow2\rightarrow4$ freeze-and-residual mechanism.

## 1. Objects And The Four Non-Equivalent Claims

- **Semantic variables:** balanced binary parent $p$ and child $b$.
- **Surface code:** $q=pb$. The Router observes $s=(p,q)$, never $b$ or a
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
are measured separately. In particular, $b=pq$ is not globally affine-linearly
separable from $s$, although it is linearly separable after conditioning on
$p$ or on $q$.

## 2. Generator And Exact Work/Fail Pair

Draw $p,b$ independently and uniformly from $\{-1,+1\}$, set $q=pb$, draw
$z\sim\mathcal N(0,I_8)$, and use $s=(p,q)$. There is no observation noise:
the experiment isolates routing and rank rather than denoising. Construct
three canonical, doubly orthogonal rank-one matrices

$$
C=u_0v_0^\top,\qquad A=u_1v_1^\top,\qquad B=u_2v_2^\top
$$

as the first three diagonal coordinate projectors in
$\mathbb R^{8\times8}$. Targets are

$$
\Theta^{work}_{p,b}=C+pA+bB,
\qquad
\Theta^{fail}_{p,b}=C+qA+bB,
$$

$$
y=\Theta z.
$$

Each training step draws 16 independent $z$ blocks, crosses every block with
all four $(p,b)$ leaves, and then permutes the resulting 64 rows. The frozen
test bank uses the same complete-factorial construction. Thus the statistical
independence unit is a $z$ block, not an individual row; every row still has
the registered standard-normal marginal, while finite-batch parent and child
averages cancel exactly. Each seed reuses exactly the same ordered
$(p,b,q,z)$ rows in work and fail. The implementation must verify before training that the two conditions
have the same four teacher matrices as a multiset under
$(p,b)\leftrightarrow(q,b)$, uniform leaf counts, zero Bayes noise, and mean
noise-free signal energy $3$.

After removing $C$, define

$$
\rho_g=
\frac{\mathbb E_g\|\mathbb E[\Theta-C\mid g]\|_F^2}
{\mathbb E\|\Theta-C\|_F^2}.
$$

The exact identities are

$$
(\rho_p^{work},\rho_q^{work})=(1/2,0),
\qquad
(\rho_p^{fail},\rho_q^{fail})=(0,1/2).
$$

They isolate functional grouping rather than frequency, entropy, label set,
noise, or teacher-function capacity.

## 3. Shared Progressive Expert System

Every model owns exactly seven trainable $8\times8$ expert matrices organized
as one root, two level-one experts, and four level-two experts. Each matrix is
stored densely for a gauge-free audit. After every update, impose rank one and
ancestor orthogonality with an exact finite enumeration. For an unconstrained
candidate $M$ and rank-one ancestors $a_jb_j^\top$, the constraint

$$
\langle uv^\top,a_jb_j^\top\rangle_F
=(u^\top a_j)(v^\top b_j)=0
$$

means that each ancestor must be assigned either to the left constraint
$u\perp a_j$ or to the right constraint $v\perp b_j$. Enumerate all at most
$2^m$ assignments, project $M$ into the corresponding left and right
orthogonal complements, take that projected matrix's best rank-one singular-
value approximation, and retain the Frobenius-nearest feasible candidate with
deterministic lexicographic tie breaking. Here $m\leq3$. The zero operator is
allowed as rank at most one—it is the exact stage-one conditional mean in the
fail construction—but any nonfinite value or absence of a feasible branch
stops the cell. Normalized ancestor overlap must be at
most `1e-6`; this is checked rather than assumed. Inference activates exactly
one expert at each level and sums their outputs, so every model uses three
active rank-one operators.

Training is stagewise:

1. train the single common expert on $y$ for 128 steps, then freeze it;
2. train two new experts for 128 steps on the function residual unexplained by
   the common expert, then freeze them and their Gate;
3. train four new experts for 128 steps on the residual unexplained by the
   frozen root and selected level-one expert.

For a new expert matrix $W$, the constrained update is rank one and has at most
the registered normalized overlap with the frozen ancestor span. This makes
“remove common” a concrete function/gradient operation, not subtraction of the
common expert's output as a Router feature. The code records the selected
enumeration branch, pre/post overlap, numerical rank, and immutable
expert/Router freeze hashes. Any frozen parameter change is fatal.

All four models use the same complete-factorial batch of 64 rows from 16
independent $z$ blocks, the same ordered rows, 128 steps per stage, the same
initial expert tensors, and no early stopping. Use Adam with betas
`(0.9,0.999)`, zero weight decay, expert learning rate `0.03`, Router learning
rate `0.01`, gradient-norm clip `5.0`, utility coefficient `1.0` for utility
arms and zero for task-only arms, and common load coefficient `0.01`. The
label-blind smoke may establish numerical stability but may not select a
scientific condition, seed, threshold, or reported checkpoint.

## 4. Matched $2\times2$ Intervention

The only two axes are Router structure and Router supervision:

| Router structure | Task loss only | Counterfactual utility |
| --- | --- | --- |
| conditional $1\rightarrow2\rightarrow4$ | `H_task` (advisor realization) | `H_util` (AI-audited utility realization) |
| flat nonlinear | `F_task` | `F_util` (necessary utility-control arm) |

All four instantiate the same Router MLP input width, hidden width, stage-one
two-way head, and stage-two four-way head. They share exact Router parameter
counts. `H_*` masks the stage-one input to $p$ and, at stage two, selects only
the two children of the chosen $p$ branch while reading $q$. `F_*` reads the
full $s$ and performs unrestricted two-way and four-way decisions. The
hierarchical arms therefore test a provided parent-first structural prior; they
do not claim to discover $p$ without a prior.

All decisions use hard top one with the same straight-through estimator. At
training time every arm evaluates every same-level candidate expert for every
example, even when utility loss has zero weight. This matches candidate-forward
compute and produces a common diagnostic ledger.

For residual target $r_i$ and candidate expert $e$, define

$$
U_{ie}=\|r_i\|_2^2-\|r_i-W_ez_i\|_2^2,
\qquad
t_i=\arg\max_e U_{ie}.
$$

The target is stop-gradient. `H_util` and `F_util` add cross entropy between
the Gate and $t_i$; `H_task` and `F_task` set that utility coefficient to zero
but still compute the same ledger. For every routed arm and every head with
$K$ available candidates, let $\bar p_e$ be candidate $e$'s mean softmax
probability in the batch and add the identical differentiable load penalty

$$
L_{bal}=K\sum_{e=1}^{K}(\bar p_e-1/K)^2
$$

with coefficient `0.01`. Utility is derived from $y$ and is additional pseudo-
supervision; it must never be described as supervision-matched to task-only
routing.

## 5. Exact Capacity Claims And Falsifier

For the parent-first tree in work, the oracle decomposition is

$$
C\quad+\quad pA\quad+\quad bB,
$$

and has zero noise-free error. In fail, the level-one conditional mean given
$p$ is zero. Each leaf then must represent

$$
qA+bB=b(pA+B),
$$

which has two equal nonzero singular values because $A$ and $B$ are doubly
orthogonal. By the Eckart--Young rank-one approximation theorem, at least one
unit of operator energy remains. Since total signal energy is three,

$$
NMSE_{H,fail}^{oracle}=1/3.
$$

Counterfactual utility cannot break this structural lower bound because
`H_util` retains the same $p$-first mask. A flat oracle can group by $q$ first
in fail and attains zero error. Any trained hierarchical fail arm materially
below the registered $1/3$ floor indicates rank, mask, or freeze leakage and
makes the run `Insufficient`.

## 6. Representation And Utility Audit

Before training, an exact linear-feasibility test must show that $p$ and $q$
are globally linearly separable from $s$, $b=pq$ is not, and $b$ is separable
inside each fixed $p$ or $q$ branch. These are finite-support identities, not
sample estimates.

At every registered evaluation step, record for the Router hidden state and
Gate logits:

- balanced accuracy and negative log likelihood for the current
  counterfactual-best candidate on a disjoint balanced test bank;
- the fifth percentile of the normalized correct-versus-best-wrong score
  margin;
- chosen-expert regret $\max_e U_{ie}-U_{i,\hat e}$;
- route agreement with the counterfactual-best candidate and per-expert load.

A positive margin says that the utility decision is exposed to the registered
linear Gate at that checkpoint. It does not by itself establish lower task
loss; regret and held-out NMSE provide the separate functional tests.

## 7. Metrics, Pairing, And Contrasts

On a frozen balanced noise-free test bank, define

$$
NMSE=\frac{\mathbb E\|\widehat y-\Theta z\|_2^2}
{\mathbb E\|\Theta z\|_2^2}.
$$

Evaluate after stage-local steps `1,2,4,8,16,32,64,128`. Integrate NMSE by
the trapezoid rule over log cumulative training examples and normalize by the
log range. Lower area under the learning curve (`AULC`) is better. The stage-two
endpoint NMSE is the fixed-budget performance metric.

For each condition, report paired whole-seed contrasts

$$
S_H=A(H_{task})-A(H_{util}),
\qquad
S_F=A(F_{task})-A(F_{util}),
$$

$$
A_T=A(F_{task})-A(H_{task}),
\qquad
A_U=A(F_{util})-A(H_{util}),
\qquad
X=S_H-S_F.
$$

Use all eight seeds and 10,000 paired whole-seed bootstrap draws with root seed
`151124`. Generate one global `10000 x 8` seed-index matrix and reuse it for
every condition, metric, grid contrast, and the fail-minus-work mechanism
contrast. Report the empirical seed values, medians, percentile 95% intervals,
and the index-matrix hash;
do not make a population-generalization claim from eight optimizer seeds.

Also report unnormalized MSE, numerical rank, projection leakage, stored and active
expert parameters, Router parameters, training all-candidate FLOPs, inference
FLOPs, step time, effective expert count, and load coefficient of variation.
Wall time is descriptive and never replaces cumulative examples or FLOPs.

## 8. Admission, Verdict, And Failure Localization

The run is eligible only if generator identities hold within `1e-10`; exact
oracle NMSE is below `1e-10` for hierarchical work and flat work/fail; the
hierarchical fail oracle equals $1/3$ within `1e-10`; every expert has numerical
rank at most one; ancestor projection leakage is below `1e-6`; freeze hashes,
paired streams, parameter counts, candidate-forward counts, and output schemas
match; and no seed is missing or replaced. The immutable manifest must equal
the frozen full configuration, and exactly four rank-completion receipts must
map the registered seeds by index modulo four and authenticate every seed file.
The learned hierarchical fail endpoint may be below the analytic $1/3$ floor
by at most `1e-4`, a float32 numerical tolerance fixed before the full run.
A valid load ledger has finite nonnegative shares summing to one, finite load
coefficient of variation, and an effective expert count in `[1,K]`; load
imbalance itself remains a diagnostic rather than an outcome threshold.

Verdicts are layered rather than collapsed:

1. **`MECHANISM_SUPPORTED`:** eligible `H_task` has work endpoint NMSE at
   most `0.05`, fail endpoint NMSE at least `0.25`, and a positive paired 95%
   lower bound for fail-minus-work AULC.
2. **`UTILITY_EFFECT_TREE` / `UTILITY_EFFECT_FLAT`:** the corresponding
   $S_H$ or $S_F$ AULC lower bound is positive without worse endpoint NMSE by
   more than `0.01`. Apply this rule separately to work and fail; the work
   verdict is the headline and fail is a structural diagnostic. Endpoint and
   AULC point estimates are medians over the eight paired seeds. This is a
   supervision result, not an architecture result.
3. **`HIERARCHY_GAIN_TASK` / `HIERARCHY_GAIN_UTILITY`:** in work, the
   corresponding $A_T$ or $A_U$ lower bound is positive, its median is at least
   five percent of the median matched flat AULC, and the median hierarchical
   endpoint is no worse than the median matched flat endpoint. Only
   `HIERARCHY_GAIN_UTILITY` permits the phrase “tree bias adds value
   under the same utility supervision.”
4. **`GENERIC_NONLINEARITY_OR_UTILITY_SUFFICIENT`:** the mechanism gate passes
   but flat matches or beats the hierarchy. Retain the structural theorem and
   reject an empirical hierarchy advantage.
5. **`LEARNED_MECHANISM_FAIL`:** all exact guards pass but `H_task` does not
   realize the work/fail separation. Diagnose route optimization, expert
   estimation, or insufficient budget using oracle, regret, rank, and load
   ledgers.
6. Any identity, rank, mask, freeze, load, compute, numerical, or completion
   guard failure is **`Insufficient`**.

Neither a utility effect nor a tree-family alignment pattern may be promoted
to hierarchy gain without the matched `F_util` comparison.

## 9. Execution And Required Artifacts

The full run uses workspace `share-space`, AEC2 cluster `share-cluster`, one
`n6ls.iu.i40.4` reserved worker, normal priority, and four processes. Preflight
requires exactly four visible H100 GPUs and rejects any automatic resource
fallback. Seeds are assigned by zero-based seed index modulo four, so every
process runs exactly two registered seeds. No local scientific GPU execution
is allowed.

Required artifacts are immutable generator and split manifests; matrices and
hashes; exact oracle/rank certificates; per-seed/per-step loss, route, utility,
margin, load, projection, parameter, and FLOP ledgers; paired bootstrap draws;
`results.json`; environment/code receipts; producer-local figures; and
`completion_audit.json`.

Figures must show: (1) the work/fail teacher decomposition and analytic floor;
(2) four-arm NMSE learning curves; (3) $S_H,S_F,A_T,A_U$ paired contrasts;
and (4) representation margin, route regret, and oracle/learned failure
localization. Every figure states its question, metric/unit, source,
aggregation, allowed conclusion, and limitation.

## 10. Claim Boundary And Stop Rule

A positive result can establish only that a provided correct $p$-first
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

## 11. Pre-Result Amendments And Resource Isolation

At `2026-08-29T16:00:50Z`, before any scientific smoke or full result was
accepted, three implementation details were made explicit without changing the
question, arms, seeds, thresholds, or primary comparison:

1. observation noise was fixed to zero and the three teacher operators were
   fixed to canonical doubly orthogonal coordinate projectors, so the analytic
   mechanism and $1/3$ failure floor are exact rather than Monte Carlo claims;
2. optimizer, clipping, utility, and shared load-penalty coefficients were
   frozen as stated in Sections 3 and 4;
3. a one-step non-scientific implementation check showed that the provisional
   50-step alternating projection could stop above the registered `1e-6`
   overlap threshold. The tolerance was not relaxed. It was replaced by the
   finite left/right constraint enumeration in Section 3, which solves the
   rank-one ancestor-orthogonality constraint by checking all feasible
   branches and remains fail-closed under the original threshold.
At `2026-08-29T16:12:35Z`, still before any full scientific execution, a
fourth implementation guard was frozen:

4. the bootstrap reuse rule, manifest/rank-receipt admission, load-ledger
   validity checks, and `1e-4` learned fail-floor numerical tolerance were
   frozen to remove implementation ambiguity; none changes a model, seed,
   metric, effect threshold, or scientific comparison.
5. rank is interpreted as at most one, so the exact zero stage-one operator in
   fail is valid; only nonfinite or infeasible constrained projections stop a
   cell. This resolves a wording contradiction without changing capacity.

No scientific condition, learning curve, endpoint, contrast, or seed result
was inspected when these amendments were frozen.

At `2026-08-29T16:04:00Z`, the current task's explicit reserved 4xH100
execution request was isolated under this new `E03H` identifier because the
shared E03 surface had concurrently been assigned an incompatible 8xRTX-5090
SPOT contract. E03H preserves the amended E03 scientific question, generator,
models, optimizer, seeds, thresholds, estimand, and claim boundary exactly.
Only the execution resource and deterministic sharding change: eight optimizer
seeds run as two seeds on each of four H100 processes instead of one seed on
each of eight RTX-5090 processes. The optimizer seed remains the independence
and bootstrap unit; no cross-rank aggregation enters training. Therefore this
resource isolation does not change a scientific observation or contrast.
