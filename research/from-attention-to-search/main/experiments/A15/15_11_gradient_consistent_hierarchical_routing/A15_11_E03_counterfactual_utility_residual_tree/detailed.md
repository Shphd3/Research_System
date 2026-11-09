---
experiment_id: A15_11_E03_counterfactual_utility_residual_tree
status: EVIDENCE_COMPLETE_AI_INTERPRETATION_AWAITING_HUMAN_CONFIRMATION
completed: 2026-08-29
---

# Detailed: Counterfactual-Utility Residual Tree

Primary Anchor: [A15_11 Anchor](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_11_gradient_consistent_hierarchical_routing/15_11_gradient_consistent_hierarchical_routing_anchor.md)
Frozen Protocol: [protocol.md](protocol.md), SHA-256
`cc1511b1766768ac01e0cbeedd41f828f790ca4979f413d6af32f8f5cda14144`
Summary: [summary.md](summary.md)

## 0. Quick Recap

- **Purpose:** separate a correct functional hierarchy, extra utility
  supervision, generic nonlinearity, and an incorrect first split.
- **Direct result:** the aligned task-only tree solves work and retains the
  fail floor; utility supervision does not help; flat nonlinear routing solves
  both work and fail.
- **Eligibility:** all 14 registered guards pass for 64 cells from eight paired
  seeds. Maximum normalized ancestor leakage is
  \(3.03\times10^{-8}<10^{-6}\).
- **Boundary:** this is an exact controlled mechanism result, not real-language
  model evidence.

## 1. Generator And Exact Theorem

Let \(p,b\) be independent balanced signs, let \(q=pb\), and give the Router
\(s=(p,q)\). For independent \(z\sim\mathcal N(0,I_8)\), the teacher output is
\(y=\Theta z\). Unit-Frobenius, mutually orthogonal rank-one matrices \(C,A,B\)
define

\[
\Theta^{work}_{p,b}=C+pA+bB,
\qquad
\Theta^{fail}_{p,b}=C+qA+bB.
\]

The two conditions contain the same four functions with the same frequency,
energy, and zero observation noise. Only their pairing with the named parent
\(p\) changes. A fixed \(p\)-first tree represents work exactly. In fail, each leaf
must approximate \(b(pA+B)\) with one rank-one matrix. The two nonzero singular
values are both one, so the Eckart--Young tail energy is one over total energy
three: exact oracle NMSE \(1/3\).

## 2. Architecture And Matched Grid

Every cell stores seven dense \(8\times8\) matrices constrained to numerical
rank at most one: one common expert, two level-one experts, and four leaves.
Training uses 128 steps at each stage. Completed experts and the level-one
Router are frozen. New experts fit only the function residual unexplained by
the frozen path. Inference activates one expert per level.

| | task-loss routing | task loss plus hard utility-target cross entropy |
| --- | --- | --- |
| fixed conditional tree | `H_task` | `H_util` |
| flat nonlinear Router | `F_task` | `F_util` |

All cells share expert and Router initialization, exact 64-row factorial
batches, row order, 384 optimizer steps, seven expert matrices, 550 stored
parameters, learning rates, load penalty, hard top-one estimation, and all-
candidate expert forwards. Each optimizer seed is an intact paired block.

The utility score for residual \(r_i\) is

\[
U_{ie}=\|r_i\|^2-\|r_i-W_ez_i\|^2.
\]

All arms execute the same candidate forwards; utility arms add unit-weight
cross entropy to the stop-gradient best candidate. Task-only arms record the
same utilities with zero auxiliary weight.

## 3. Metrics And Contrast Signs

The primary quantity is normalized noise-free NMSE area under the learning
curve over log cumulative examples (AULC); lower is better. Define

\[
S_H=H_{task}-H_{util},\quad
S_F=F_{task}-F_{util},\quad
A_T=F_{task}-H_{task},\quad
A_U=F_{util}-H_{util}.
\]

A positive \(S\) means utility supervision helps. A positive \(A\) means the tree
helps. Whole-seed paired median bootstrap uses 10,000 draws and seed 151124.
Endpoints, utility regret, route accuracy, normalized fifth-percentile margin,
load, rank, projection, freeze, and compute are secondary or guards.

## 4. Main Results

### 4.1 Eight-seed cell medians

| Condition | Variant | AULC | endpoint NMSE | route accuracy | utility-target BA | hidden-probe BA |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| work | `H_task` | 0.76185 | \(2.30\times10^{-5}\) | 1.000 | 1.000 | 1.000 |
| work | `H_util` | 0.79556 | 0.41693 | 0.805 | 0.625 | 0.625 |
| work | `F_task` | 0.76314 | \(1.98\times10^{-5}\) | 0.758 | 0.739 | 0.667 |
| work | `F_util` | 0.76401 | \(3.16\times10^{-5}\) | 1.000 | 1.000 | 1.000 |
| fail | `H_task` | 0.81733 | 0.33698 | 0.969 | 0.970 | 0.977 |
| fail | `H_util` | 0.81574 | 0.33417 | 1.000 | 1.000 | 0.984 |
| fail | `F_task` | 0.76288 | \(1.69\times10^{-5}\) | 0.789 | 0.735 | 0.667 |
| fail | `F_util` | 0.77053 | \(1.16\times10^{-4}\) | 1.000 | 1.000 | 1.000 |

### 4.2 Registered AULC contrasts

| Condition | Contrast | Median | paired 95% interval | Reading |
| --- | --- | ---: | ---: | --- |
| work | \(S_H\) | -0.03860 | [-0.06842, -0.00685] | utility tree worse |
| work | \(S_F\) | -0.00217 | [-0.00612, 0.00148] | no flat utility effect |
| work | \(A_T\) | -0.00072 | [-0.00334, 0.00258] | no task-only tree gain |
| work | \(A_U\) | -0.03279 | [-0.07027, -0.00334] | flat utility model better |
| work | interaction \(X\) | -0.03201 | [-0.06990, -0.00246] | utility effect depends adversely on tree |
| fail | \(A_T\) | -0.05336 | [-0.05853, -0.04955] | flat avoids wrong-tree floor |
| fail | \(A_U\) | -0.04512 | [-0.04926, -0.03292] | same under utility supervision |

The mechanism contrast
\(AULC_{fail}(H_{task})-AULC_{work}(H_{task})\) is 0.05406 with interval
[0.05220, 0.05537]. The work endpoint is below 0.05; the fail endpoint is above
0.25. The mechanism therefore passes without using a hierarchy-versus-flat
claim.

![NMSE learning curves](figures/nmse_learning_curves.png)

The first 128-step common stage is shared. At level one and the leaves, the
task-only aligned tree and both flat models converge to near zero. The utility
tree often locks into incomplete leaf coverage.

![Registered paired contrasts](figures/grid_contrasts.png)

Negative work \(S_H\) and \(A_U\) show that hard utility supervision does not
rescue or improve the hierarchy.

## 5. Failure Localization

### 5.1 Direct diagnostics

For aligned `H_task`, every seed ends with balanced leaf load, zero utility
regret, utility-target and hidden-probe balanced accuracy 1.0, and median native
and probe normalized fifth-percentile margins 0.547 and 0.545.

For aligned `H_util`:

- endpoint NMSE is near zero in only 1/8 seeds; the other seven end near 1/6 or
  2/3;
- the median minimum leaf load is zero;
- native-Gate and hidden-probe target balanced accuracy are both 0.625;
- their median normalized fifth-percentile margins are -0.478 and -0.586;
- endpoint utility regret has median 0.0500.

Because the frozen hidden-state ridge probe is no better than the native Gate,
the observed failure is not localized to a bad final linear output layer. The
utility target is not stably accessible from the Router representation.

### 5.2 AI causal hypothesis, not a registered result

Expanding the utility score gives

\[
U_{ie}=2r_i^\top W_ez_i-\|W_ez_i\|^2.
\]

At early steps, its argmax depends on the sampled \(z_i\), current residual, and
random evolving expert matrices. The hierarchical Router does not observe
\(z_i\): it observes only \(p\) at level one and \(q\) under a parent mask at level
two. Consequently, several rows with identical Router input can receive
different instantaneous best-expert labels. A stop-gradient hard-label loss
then rewards an accidental current winner, that winner receives more task
gradient, and the feedback can starve other experts. This explains the exact
combination of zero leaf load, negative margins, and poor probe readability.

This explanation is consistent with the evidence and follows from the object
definitions, but E03 did not intervene on target aggregation or Router
observability. It must remain an AI hypothesis until a successor compares the
instantaneous target with conditional expected utility under the same model.

## 6. Eligibility And Numerical Audit

All guard fields are true: exact generator and oracle, full 8×8 paired grid,
finite values, pretraining admission, paired initialization/data, cell schema,
rank, ancestor projection, freeze, and fail-floor non-leakage. The exact
failure floor is \(1/3\) with a 0.02 leakage-only allowance; no hierarchical fail
cell falls materially below it.

The finite projection evaluates every left/right ancestor-orthogonality branch
in float64 and stores the selected expert in FP32. The final registered
numerical-rank guard uses tolerance \(10^{-5}\) and returns rank one for all seven
experts in all 64 cells. The per-update ledger also recorded
`matrix_rank(tol=1e-8)` after FP32 storage; floating-point perturbations made
4,873 of 57,792 descriptive entries report rank 2--7 even though the producer
constructed a float64 outer product and the registered rank guard passed.

The first derived analysis mistakenly treated this stricter, unspecified
absolute-tolerance diagnostic as a second admission gate. Before reading
performance values, a red test reproduced the mismatch; the schema audit was
corrected to check the diagnostic's presence and dimension, while scientific
rank admission remained owned by the registered \(10^{-5}\) cell guard. The old
derived directory is preserved as `synthetic_ineligible_audit_v1`; raw seed
files, producer hashes, rank threshold, overlap threshold, and fail floor were
not modified. The corrected full suite has 118 passing tests.

## 7. Execution History

| Attempt | Run stamp / job | Outcome | Scientific status |
| --- | --- | --- | --- |
| 1 | `20260829T170740Z` / `pt-s3k4gytd` | base-image package audit stopped before inputs | no evidence |
| 2 | `20260829T171220Z` / `pt-gwwxjpyw` | nested thread-pool control deadlocked Qwen CPU cells | no E03 evidence |
| 3 | `20260829T172018Z` / `pt-3dndd5hl` | FP32 ancestor projection falsely found no feasible stage-two branch | no complete E03 grid |
| 4 | `20260829T180400Z` / `pt-0aopddjj` | all 64 E03 cells and artifacts landed; root CSV audit crashed afterward | canonical raw evidence |

Attempt 4 used exactly eight NVIDIA GeForce RTX 5090 GPUs, PyTorch
`2.8.0a0+5228986c39.nv25.06`, and Python 3.12.3. Its remote final job state is
`FAILED` only because the final root reader exceeded Python's default CSV field
limit. A test-first post-run reader repair and the rank-ledger schema correction
regenerated only derived analysis and completion receipts. The local root
completion audit now passes all 36 required artifacts. No H100 result is part
of this record.

Canonical worker evidence:
`/data/250010109/MoE_Router/experiments/20260829_a15_11_gradient_consistent_hierarchical_routing/runs/full-20260829T180400Z/`.

## 8. Visualization Audit

![Utility and representation diagnostics](figures/utility_diagnostics.png)

The side-by-side native Gate and frozen hidden probe are decision-explanatory
only. They do not enter a registered positive verdict. The box plots show seed
instability hidden by endpoint medians; this is why all eight seed values remain
in the raw ledger.

![Exact oracle and separability identities](figures/oracle_and_separability.png)

The deterministic bars verify work residual coherence 1/2, fail coherence
zero, work tree oracle zero, and fail tree floor 1/3. They certify the
generator, not learned optimization.

## 9. Knowledge Update And Boundary

**Direct evidence:** correct grouping is sufficient for the staged task-only
tree to realize the decomposed rank-one functions; wrong grouping is blocked
by rank, not optimization; flat nonlinearity removes that block; the registered
hard instantaneous utility supervision has no gain and destabilizes the
aligned tree.

**AI interpretation awaiting human confirmation:** expert utility must be
defined relative to the information available to the Router. A counterfactual
label that varies with hidden content omitted from the Router input is not a
learnable routing target merely because it is exactly computed.

**Cannot claim:** general harm from utility supervision, natural hierarchy
discovery, real-language-model efficiency, or safe common-subspace deletion.

## 10. Proposed Successor, Not Yet Approved

The smallest falsifier of the AI explanation keeps the same work generator,
experts, hierarchy, initialization, candidate compute, and task loss, and
changes only the auxiliary target:

\[
\bar U_e(r)=\mathbb E[U_e\mid r],
\]

where \(r\) is the exact Router-visible branch state. Compare no auxiliary loss,
instantaneous hard utility, and stop-gradient soft conditional-expected
utility. The primary criterion is recovery of the task-only tree's endpoint
without worse AULC, plus positive target margin and nonzero load for every
required function. This is an AI proposal; it is neither the current result nor
an approved Protocol.
