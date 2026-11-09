# MTP Interference, Capacity, And Curriculum

Archived pre-consolidation snapshot. Statements below describe the historical state at capture time and are not the current claim boundary.

## Status

- English canonical story; Chinese companion: `20260713_mechanism_pre_consolidation_cn.md`.
- Current primary synthesis for the A11 line.
- The workload-first story remains background. The current route temporarily freezes workload expansion and asks why informative Next-2 supervision can harm or help the shared standard objective.

## 1. Research Question

The active question is not whether MTP is universally better than NTP. It is:

> When an informative second-future-token objective is added to the same shared model, what observable mechanism determines whether the standard autoregressive objective improves or deteriorates?

The candidate causal chain is:

$$
\text{task learned}
\rightarrow
\text{local gradient interaction}
\rightarrow
\text{task-related available capacity}
\rightarrow
\text{cross-position use}
\rightarrow
\text{standard-head performance}.
$$

Each arrow requires a separate anchor. Passing a representation probe or a local derivative cannot substitute for the final standard-head metric.

## 2. Definitions

| Object | Plain meaning | Operational definition | Boundary |
| --- | --- | --- | --- |
| controlled standard objective $L_N$ | the two-position loss both NTP and Next-2 must improve in this experiment | decision-format CE plus next-state answer CE | not all-token LM loss or a benchmark score |
| auxiliary objective $L_A$ | direct second-future answer supervision | answer CE read at the decision state | not evidence of later use |
| local interference | the extra standard-loss change caused by adding $g_A$ | paired cloned one-step updates | not full training |
| task calibration | evidence that the checkpoint learned composition | held-out answer accuracy at least `0.70` | does not identify why it learned |
| task-related capacity | independent directions available for standard and auxiliary functions | future effective-rank and safe-update metrics | not parameter count alone |
| curriculum mechanism | change caused by gradually increasing auxiliary weight | static versus dose-matched scheduled objective | not established by final score alone |

## 3. Core Mathematical Model

Let

$$
g_N=\nabla_\theta L_N,\qquad g_A=\nabla_\theta L_A.
$$

For paired updates,

$$
\theta_N'=\theta-\eta g_N,qquad
\theta_M'=\theta-\eta(g_N+\lambda g_A),
$$

and

$$
L_N(\theta_M')-L_N(\theta_N')
=-\eta\lambda\langle g_N,g_A\rangle+O(\eta^2).
$$

This equation predicts a local difference. It becomes a task-mechanism explanation only when the checkpoint has learned the held-out composition function.

If $L_N$ is twice differentiable, the explicit second-order expansion is

$$
\Delta_{obs}
=-\eta\lambda g_N^\top g_A
+\eta^2\lambda g_N^\top H_N g_A
+\frac{\eta^2\lambda^2}{2}g_A^\top H_N g_A
+O(\eta^3).
$$

A negative inner product therefore means the joint update leaves a higher $L_N$ than the paired NTP-only update; it does not imply an absolute loss increase relative to the original checkpoint.

The later low-rank model is valid only under a whitened linear shared representation, squared loss, and optimal linear readouts. If $T_N,T_A$ are task maps and representation rank is at most $r$, the selected subspace follows the top $r$ eigendirections of

$$
M_\lambda=T_N^\top T_N+\lambda T_A^\top T_A.
$$

Competition occurs only when auxiliary eigendirections enter the top-$r$ subspace and displace standard-task directions. This statement does not directly transfer to a Transformer.

Candidate Transformer diagnostics are local, task-conditioned quantities:

$$
r_{joint}=\frac{(\operatorname{tr}K)^2}{\operatorname{tr}(K^2)},
\quad K=J_{joint}J_{joint}^\top,
\qquad
S_{safe}=\frac{\|P_{\ker J_N}g_A\|^2}{\|g_A\|^2}.
$$

They require a numerical null-space threshold and sensitivity audit and cannot be called global model capacity.

Curriculum has a strict boundary: in a convex problem trained to the same global optimum under the same final objective, schedule order should not change the final solution. Any curriculum benefit must therefore come from finite budget, nonconvex path dependence, optimizer state, or representation locking, and must be tested under matched auxiliary-loss dose and update budget.

Neither effective rank nor curriculum is tested until a calibrated interference regime exists.

## 4. A11_22 Evidence

A11_22 used the exact two-permutation task $Y=\pi_2(\pi_1(A))$, a one-layer causal Transformer, five seeds, and paired finite differences over 1024 audit examples.

Under independent uniform permutations, $I(Y;\pi_1\mid A)=I(Y;\pi_2\mid A)=0$ while $I(Y;\pi_1,\pi_2\mid A)=\log 8$. This establishes joint necessity in the data distribution; it does not show that the model learned composition or that token distance alone is long-range semantics.

At relative step norm $10^{-5}$:

- prediction-observation slope: `1.0174`;
- Pearson correlation: `0.9990`;
- sign agreement: `1.0000`;
- median normalized residual: `0.1012`.

The numerical first-order law is therefore supported at a small step. However, validation answer accuracy is `0.125` in all five seeds, equal to chance. The formal verdict is insufficient evidence for learned-task interference.

The gradient sign is also not universal: four seeds show harmful auxiliary direction and one shows helpful direction. A theory must explain this state dependence rather than assume all MTP gradients conflict.

## 5. Updated Answers To The Core Questions

### Why can Next-2 make standard NTP worse?

Locally, a negative gradient inner product predicts a positive standard-loss difference relative to the paired NTP-only update. The equation is validated numerically, but its learned-task relevance is not yet established.

### Why might a larger model benefit?

The active hypothesis is that a larger model has higher task-conditioned local adjustable rank and a larger fraction of auxiliary gradient that does not perturb protected standard outputs to first order. Parameter count alone is not the mechanism, and no current evidence supports this yet.

### What is capacity?

Capacity will not be operationalized as parameter count alone. Candidate observables are joint task-Jacobian spectral participation ratio, intervention-response representation rank, and safe auxiliary-update fraction. Each is local to the task, data, checkpoint, and numerical threshold; none is a global capacity measure.

### Why might curriculum help?

The candidate mechanism is path dependence: first stabilize the standard subspace, then increase the auxiliary weight. In a sufficiently optimized convex problem, curriculum should not change the final solution. A valid neural test must match auxiliary-loss dose and update budget and show reduced early interference or subspace displacement, not merely a better final score. This remains untested.

### What is long-range semantic composition?

For this line, it is a task variable that depends on jointly necessary distant evidence, is invariant to nuisance changes, and changes under task-evidence intervention. The current synthetic instance is exact relation composition; natural-language validity remains outside the present claim.

## 6. Anchor Route And Gates

| Anchor | One decision | Status | Opening gate |
| --- | --- | --- | --- |
| A11_22 one-step interference | does the first-order term predict the paired standard-loss difference at a learned-task checkpoint? | numerical component supported; overall insufficient because calibration failed | complete a known-good task calibration |
| A11_23 calibration repair | can depth/time/width learn the original sequence task? | weakened: strongest train `0.1249`, validation `0.1211` | closed |
| A11_23b explicit binding | do role-specific pair tokens repair binding? | weakened: five-seed test `0.1274--0.1353` | closed |
| A11_24 task-rank competition | does explicit rank control the MTP standard-loss penalty? | supported: rank-1 gap `0.9084--1.0218`, rank-2 near zero | closed |
| A11_25 curriculum boundary | does dose-matched curriculum repair rank-1 deficiency? | weakened: Pareto pass `0/5` | closed |
| A11_26 scale / real transfer | is transfer to pretrained/real data justified? | parked: neural task gate failed | await neural bridge |
| A11_27 standard-head causal use | does informative Next-2 increase causal use by the common NTP head after capability is fixed? | design complete; protocol draft | approve protocol, then pass shared task gate |

“Complete the anchors in order” therefore means applying these gates. It does not mean fabricating later result records after an earlier validity guard fails.

Completion audit: A11_01--A11_20 have protocol, summary, and detailed records; A11_21 is parked; A11_22 is insufficient; A11_23/23b/24/25 are completed with the verdicts above; A11_26 is explicitly parked by its transfer gate; A11_27 is design-only and has no result. Router is outside the active MTP chain.

## 7. Claim Boundary

Current evidence supports a local first-order finite-difference law. It does not establish that MTP harms a learned composition function, that effective rank explains scale, that curriculum repairs capacity competition, or that the mechanism transfers to natural language.

## 8. Exactly One Next Decision

Stop tuning the small from-scratch sequence learner. Approve or revise A11_27. If approved, use its shared Qwen3-0.6B NTP calibration stage to pass the two-hop task gate before cloning NTP and informative Next-2. The first downstream question is standard-head causal use, not another private-head or probe result. Router and real transfer remain parked.

## Source Map

- Anchor: `../../../../problem_anchors/11_long_horizon_mtp_objective/11_22_one_step_ntp_interference_anchor.md`
- Protocol: `../../../../experiments/A11/A11_22_one_step_ntp_interference/protocol.md`
- Summary: `../../../../experiments/A11/A11_22_one_step_ntp_interference/summary.md`
- Detailed: `../../../../experiments/A11/A11_22_one_step_ntp_interference/detailed.md`
- Active anchor: `../../../../problem_anchors/11_long_horizon_mtp_objective/11_27_standard_head_causal_representation_use_anchor.md`
- Draft protocol: `../../../../experiments/A11/A11_27_standard_head_causal_representation_use/protocol.md`
