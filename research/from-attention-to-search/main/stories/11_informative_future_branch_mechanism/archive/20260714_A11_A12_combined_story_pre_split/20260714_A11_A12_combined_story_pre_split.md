# Multi-Token Prediction From Long-Horizon Representation To Causal Use

English canonical story. Chinese companion: [20260714_A11_A12_combined_story_pre_split_cn.md](20260714_A11_A12_combined_story_pre_split_cn.md).

## Abstract

This line asks one question: when does predicting more than the next token teach the current hidden state a task variable that the ordinary next-token predictor can actually use?

The established result is narrower than a general MTP advantage. When the prediction horizon first covers a future target that contains a new task variable, MTP adds a direct first-order update to the current hidden state. The update is controlled by the information content and centered output directions of the covered targets, not by horizon length alone. Controlled Transformer experiments show that this direction can reach shared parameters, but full language-model losses add signed interference. Later experiments show the central boundary: a useful direction at the current state can become adverse after the next-token state transition, so representation formation is not standard-head use.

To test use cleanly, the line adopts a minimal ordered-evidence workload. Two independent complete mapping tables determine an intermediate entity and then an answer. Either table alone is uninformative, while both tables jointly determine the answer. The workload is valid, but the tested from-scratch small Transformers did not learn it, so their gradients cannot adjudicate MTP use. A separate oracle linear experiment shows that insufficient representation rank can cause MTP to improve the future factor while harming the standard objective; increasing rank removes the tradeoff, and curriculum cannot repair missing structural rank. The only active decision is therefore to establish a shared task-capable checkpoint and test whether informative Next-2 increases task-specific causal control of the standard next-token head.

## 1. Terminology And Research Question

| Term | Plain meaning | Concrete object or computation | Why it matters | Cannot prove |
|---|---|---|---|---|
| next-token prediction, NTP | train each position to predict only the immediately following token | standard loss $L_N$ and ordinary output head $q_1$ | baseline objective and final comparison target | inability to learn distant variables |
| multi-token prediction, MTP | use one prefix state to predict several future positions | $L_N$ plus auxiliary future losses | creates earlier supervision paths | general downstream superiority |
| informative future target | a future label that depends on a task variable after local context is matched | branch-dependent $Y_{t+j}$ | identifies where extra signal begins | whether the signal is used |
| long-range compositional semantics | remote evidence remains necessary after the local window is known, and several pieces must be combined in order | $a\rightarrow b\rightarrow y$ with single-evidence controls | operationalizes the advisor's hard workload | all meanings of semantics |
| representation present | a held-out decoder can recover the task variable | probe on a hidden state | prerequisite | functional reliance |
| causal use | changing only the task-variable component changes the ordinary model answer as predicted | cross-fitted patch and matched random control | separates presence from use | real-world transfer |
| task-relevant rank | number of independent task directions a shared representation can carry | controlled encoder-rank intervention | structural capacity variable | parameter-count scaling |

The line's current question is not whether MTP is universally better. It is:

> Does informative future supervision create an earlier task variable, can shared model parameters preserve it to the answer position, and does the ordinary next-token head causally rely on it?

## 2. Why This Workload

The advisor's hard workload contains locally simple factors, distributed evidence, coupling, ordered combination, intermediate decisions, and a final outcome. The minimal model maps these requirements as follows:

| Workload property | Minimal object | Concrete meaning |
|---|---|---|
| distributed evidence | two tables separated in the context | the answer cannot be read from one local span |
| locally simple factors | one table lookup per step | each relation is easy in isolation |
| coupling | the first output becomes the second input | the two facts cannot be solved independently |
| order | apply table 1 before table 2 | reversing the order usually changes the answer |
| intermediate state | $B=\pi_1(A)$ | the model must know which row of table 2 to use |
| causal dependence | replacing either table changes the correct answer by rule | excludes answer-word correlation as the mechanism |

Let $\mathcal V$ contain $M$ entities. Independently sample two random permutations, which are complete one-to-one mapping tables:

$$
\pi_1,\pi_2:\mathcal V\rightarrow\mathcal V.
$$

For query entity $A$,

$$
B=\pi_1(A),
\qquad
Y=\pi_2(B).
$$

The first table determines which row to query; the second table determines the value in that row. Because both tables are complete permutations, every candidate answer appears exactly once. With independent uniform sampling,

$$
I(Y;\pi_1\mid A)=I(Y;\pi_2\mid A)=0,
$$

but

$$
I(Y;\pi_1,\pi_2\mid A)=H(Y\mid A)=\log M.
$$

This is the computational skeleton of multi-document question answering such as company to founder to birth country, knowledge-relation chaining, and cross-file code tracing. It deliberately removes natural-language relation extraction, ambiguity, and open-ended generation. Success can establish an ordered-composition mechanism, not automatic benchmark improvement.

The output interface is a decision marker, a branch-shared format token, and the answer entity. NTP predicts the answer after consuming the format token. Informative Next-2 additionally predicts the same answer directly from the earlier decision state. The final outcome is always the ordinary next-token head at the answer position.

## 3. Core Mechanism Theory

### 3.1 Direct current-state supervision

For task variable $Z=z$, let $\mathcal I_K$ be the informative positions covered by horizon $K$. The aggregate current-state direction is

$$
v_z^{(K)}=\sum_{j\in\mathcal I_K}\lambda_j(u_{j,z}-\bar u_j).
$$

This equation gives the first stable result of the line:

- before the first informative target, the direct task velocity is zero;
- covering that target turns the velocity on;
- adding an uninformative target gives no direct increment;
- adding another informative target helps or hurts according to output-direction alignment.

Thus the causal object is informative target coverage and direction geometry, not $K$ itself.

### 3.2 Shared-parameter transmission and interference

A hidden-state direction affects training only if shared parameters can realize it. Let $M$ be a task margin and partition the all-position loss:

$$
L^{all}=L_D+L_I+L_S+L_R.
$$

$L_D$ is the earlier MTP-specific path, $L_I$ is the later standard NTP semantic path, and the other terms are local and remaining background. Their same-checkpoint contributions are

$$
G_c=-\langle\nabla_\theta M,\nabla_\theta L_c\rangle.
$$

Controlled experiments show $G_D>0$ and $G_D>G_I$ across all confirmation seeds, but the background is signed and reverses the full net velocity in one seed. Direct supervision is therefore an available mechanism, not a guarantee of positive total training dynamics.

For one sufficiently small update, the auxiliary effect on the standard loss follows

$$
\Delta L_N\approx-\eta\lambda\langle g_N,g_A\rangle.
$$

This local identity predicts a paired finite difference but does not by itself explain the final trained solution.

### 3.3 Formation, transport, and use

The standard head predicts from a later state:

$$
h_{T+1}=F_\theta(h_T,e_{fmt}).
$$

A task direction useful at $h_T$ must survive this transition. Cross-position experiments show that changing output head leaves the sign almost unchanged, while moving from $h_T$ to $h_{T+1}$ reverses it. Intervening tokens modulate the geometry, but favorable local geometry does not reliably produce held-out behavioral gain.

The line therefore separates three claims:

1. **presence:** the variable is recoverable;
2. **transport:** the useful component survives to the answer state;
3. **causal use:** a task-specific intervention changes the standard answer and clean behavior benefits.

Only the third is the final functional claim.

### 3.4 Capacity and curriculum

An oracle linear model isolates structural capacity. The standard task requires two independent factors and MTP adds extra weight to one. A rank-one shared representation must trade them off; rank two can carry both. Experimentally, rank one improves the future factor but adds a large standard-loss penalty, while rank two removes the penalty to numerical zero.

This establishes a sufficient mechanism, not a Transformer scale law. Parameter count is only a proxy; the causal variable in the experiment is task-relevant rank.

A dose-matched NTP-to-MTP curriculum does not repair the rank-one tradeoff. This sharpens the curriculum theory: scheduling may help a nonconvex optimization path when capacity is sufficient, but it cannot create a structurally missing independent direction.

## 4. Six Stable Knowledge Updates

| Step | Decision answered | Result | Boundary earned |
|---|---|---|---|
| 1. Informative horizon | when does direct current-state supervision appear? | at informative target inclusion; direction alignment controls the increment | no parameter or downstream claim |
| 2. Parameter transmission | can shared parameters realize the direction? | yes under controlled Transformer interventions; background is signed | no natural-language efficiency claim |
| 3. Cross-position boundary | is current-state formation sufficient for standard-head behavior? | no; use can reverse after one state transition | no universal bridge law |
| 4. Workload and gate | is the ordered-composition task valid, and did the small learner learn it? | data model valid; tested from-scratch learners remained near chance | no NTP/MTP comparison on those checkpoints |
| 5. Capacity and curriculum | can missing rank cause the tradeoff, and can curriculum repair it? | rank is sufficient in the linear model; curriculum cannot repair missing rank | no neural scale law |
| 6. Causal use | does informative Next-2 increase standard-head causal reliance after capability exists? | not yet tested | only active decision |

The current split anchor chains are indexed by [A11](../../../../problem_anchors/11_informative_future_branch_mechanism/README.md) and [A12](../../../../problem_anchors/12_structured_compositional_mtp_workload/README.md).

## 5. Evidence Interpretation

The strongest direct-supervision evidence is the next-$K$ inclusion experiment: direct semantic velocity is zero before the informative position, positive when covered, unchanged by a shared target, amplified by aligned information, and weakened by conflicting information.

The strongest parameter evidence is the all-position decomposition: the earlier direct path is positive and larger than the later NTP semantic component in 5/5 seeds, while other losses make the full net effect nonuniform.

The strongest negative boundary is the cross-position audit: both output heads are useful at the current state in 5/5 seeds and adverse one token later in 5/5. The end-to-end proxy then fails to show a stable standard-head behavioral MTP advantage.

The compositional data audit is positive, but the model gate is negative: tested from-scratch models achieve approximately chance answer accuracy even after more depth, width, steps, and explicit row binding. This means the data are not invalid; it means those checkpoints cannot answer the MTP mechanism question.

The rank experiment gives controlled causality: at rank one, MTP improves the future factor in 5/5 seeds while increasing standard loss; at rank two the standard penalty disappears. The curriculum experiment excludes schedule order as a repair for this structural deficit.

## 6. Refined Theory And Scale Hypothesis

The line's reconciled model is

$$
\text{MTP net value}
=
\text{earlier informative supervision}
-
\text{objective interference}
-
\text{capacity competition}
-
\text{transport/use failure}.
$$

This makes a three-regime scale curve plausible but not established:

1. a low-capacity model may be harmed because competition and interference exceed the direct benefit;
2. an intermediate-capacity model may benefit because it can carry both directions while NTP has not yet learned the distant variable efficiently;
3. with enough model and data, NTP may learn the same variable through later ordinary supervision, so the MTP advantage may shrink.

The third regime is not inevitable. If workloads continually introduce new informative horizons or harder latent variables, MTP may retain an advantage. This remains a hypothesis until a task-capable, compute-matched neural comparison connects measured task rank and causal use to the performance gap.

## 7. Claim Boundary

### Established

- Informative future target coverage creates an earlier direct first-order task signal at the current state.
- Output-direction alignment determines how several informative targets combine.
- The direction can reach shared parameters under controlled assumptions, while all-position background is signed.
- Current-state formation is not sufficient for later standard-head behavior.
- Structural rank deficiency is a sufficient MTP/NTP tradeoff mechanism in the stated linear model.
- Curriculum cannot repair structurally missing rank in that model.

### Not established

- Informative Next-2 is causally used by the standard head on a learned composition task.
- Larger neural models benefit because they have higher task-relevant rank.
- Curriculum helps when neural capacity is sufficient but optimization is difficult.
- The mechanism transfers to multi-document QA, code repositories, or general language modeling.
- Router or MoE design follows from the present evidence.

## 8. Exactly One Next Decision

Use one shared pretrained or explicitly structured checkpoint that first passes the two-table capability gate. Then clone it into matched NTP and informative Next-2 conditions and measure task-specific counterfactual control of the same standard next-token head with cross-fitted task-subspace patches and matched random-subspace controls.

If the capability gate fails, stop. If the gate passes but causal control does not increase, the direct-supervision mechanism is present but functionally inert for this task. If causal control increases without clean-accuracy loss, the line earns its first standard-head utilization result; only then should scale, curriculum, or real-data transfer reopen.

## 9. Source Map

- [Informative-horizon inclusion](../../../../experiments/A11/A11_09_next_k_inclusion_law/summary.md)
- [Controlled parameter transmission](../../../../experiments/A11/A11_11_k2_semantic_tangent_kernel_transmission/summary.md)
- [All-position path decomposition](../../../../experiments/A11/A11_12_all_position_semantic_path_decomposition/summary.md)
- [Cross-position boundary](../../../../experiments/A11/A11_18_head_position_cross_kernel/summary.md)
- [End-to-end negative boundary](../../../../experiments/A11/A11_20_end_to_end_bridge_conditioned_efficiency/summary.md)
- [Local interference law and failed task guard](../../../../experiments/A12/A12_02_one_step_ntp_interference/summary.md)
- [From-scratch task-gate failure](../../../../experiments/A12/A12_03b_explicit_binding_calibration/summary.md)
- [Controlled rank mechanism](../../../../experiments/A12/A12_04_task_rank_competition/summary.md)
- [Curriculum boundary](../../../../experiments/A12/A12_05_curriculum_rank_boundary/summary.md)
- [Active causal-use anchor](../../../../problem_anchors/12_structured_compositional_mtp_workload/12_m03_standard_head_causal_use_anchor.md)
