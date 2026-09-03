# A11_22 Distributed-Evidence Composition Workload Anchor

Status: proposed anchor; approval-ready, not yet run.  
Parent line: `11_long_horizon_mtp_objective`.  
Daily source: `daily_research_reports/0712/docs/`.  
Benchmark anchor: LongBench multi-document QA, with 2WikiMultiHopQA as the trainable real-data source.

## 0. researcher judgment record

**Phenomenon:** A11 has established controlled informative-horizon representation and gradient mechanisms, but the downstream bridge failed to produce a stable common-H1 advantage. The failure is no longer productively addressed by bridge, weight, duration, or $K$ sweeps. The unresolved issue is whether the studied mechanism corresponds to a real difficult workload.

**Mechanism guess:** A useful long-context workload requires several individually insufficient pieces of evidence, correct evidence binding, a nontrivial composition operator, and preservation of the resulting task state to the answer position. MTP helps only when its additional future targets directly encode this task-relevant state and the useful gradient survives shared-parameter conflict and cross-position transmission.

**Key variables:** evidence state $E$; distractors $D$; query $Q$; operator tree $T_Q$; intermediate variables $Z_v$; answer $Y$; decision representation $H_T$; answer-position representation $H_A$; task score $Q_{\mathrm{comp}}$; task-gradient alignment $\Gamma_{\mathrm{task}}$; paired transfer score $T_{\mathrm{pair}}$.

**Causal relation:** If `MTP-info` adds a future target that encodes a necessary intermediate variable, it should improve task-relevant representation at the decision state. If that representation is causally used and preserved to the answer position, the same improvement should appear in both a controlled synthetic task and a real multi-document compositional QA task. Masking the informative future target should remove the gain.

**Primary observable:** paired mechanism-transfer score

$$
T_{\mathrm{pair}}
=
\min\left(
\Delta Q^{\mathrm{syn}},
\Delta Q^{\mathrm{real}}
\right),
$$

where each $\Delta Q$ compares `MTP-info` with the stronger of NTP and `MTP-mask`.

**Rival explanations:** synthetic lexical shortcuts; MTP receives more loss terms but no task-relevant signal; probe information is not causally used; the real task is solved by single-document retrieval; improvements come from local language-model fit; the structured serialization, rather than MTP, creates the effect; the small model is below the capability threshold.

**Decision:** Run one paired synthetic-real audit. Do not design a new Router unless the workload transfers and stable operator-conditioned interference is subsequently observed.

## 1. Decision Question

Does the proposed distributed-evidence composition model capture a real long-context workload strongly enough that the same task-relevant representation mechanism distinguishes informative MTP from NTP and masked-MTP on both controlled synthetic data and held-out real multi-document QA?

This is the only decision question.

## 2. Terminology / Definitions

| Term | Plain meaning | Concrete object | Formula / unit | Why it matters | Cannot prove |
|---|---|---|---|---|---|
| distributed evidence | necessary facts separated in context | $E_{1:m}$ placed in different passages | count and token distance | distinguishes composition from local lookup | semantic difficulty by itself |
| composition operator | rule combining evidence or intermediate states | relation composition, comparison, logic, or arithmetic | operator label $o$ | defines the required computation | that the model uses an explicit symbolic algorithm |
| operator tree | dependency structure from evidence to answer | $T_Q$ | depth $d$, node count | separates depth from distance | natural-language realism |
| decision representation | hidden state before structured reasoning/answer generation | $H_T$ | vector | location receiving direct future supervision | answer-position use |
| answer representation | hidden state at the actual answer token | $H_A$ | vector | tests cross-position preservation | how information was formed |
| local insufficiency | one evidence item is not enough | one-support controls | excess accuracy above chance | blocks retrieval shortcuts | full compositionality alone |
| task-relevant sufficiency | representation contains information needed for the answer | conditional-information or decoder criterion | $I(Y;E\mid H,Q)$ | formal target property | factor-wise binding |
| causal use | changing a task variable in the representation changes the output correctly | hidden-state patch/swap | consistency rate | guards probe-only claims | global mechanism uniqueness |
| `MTP-info` | MTP whose extra horizons encode necessary task variables at the decision state | structured future tokens with nonzero weights | objective condition | tests direct informative supervision | general pure-pretraining benefit |
| `MTP-mask` | same MTP architecture with task-informative decision-position horizons removed | zero mask on those terms | objective condition | isolates informative direct signal | perfect compute matching |
| $Q_{\mathrm{comp}}$ | guarded compositional task score | full accuracy plus anti-shortcut guards | 0 to 1 | main task-use metric | representation mechanism alone |
| $T_{\mathrm{pair}}$ | minimum informative-MTP gain across synthetic and real tasks | paired difference | accuracy points | rejects synthetic-only stories | universal benchmark transfer |
| $\Gamma_{\mathrm{task}}$ | alignment of extra MTP gradient with held-out task gradient | gradient inner product/cosine | scalar | tests useful versus conflicting signal | finite-step gain by itself |

## 3. Parent Problem And Current Evidence

### 3.1 What A11 already supports

Controlled A11 evidence supports:

1. direct informative future horizons can force or accelerate task-variable formation in a current hidden state;
2. larger $K$ is not the causal object; covered informative horizons and their readout geometry are;
3. extra MTP gradients can be useful at the current decision state but adverse after the intervening token/state transition;
4. local bridge-conditioned alignment did not yield a stable downstream efficiency advantage.

### 3.2 Why a new workload anchor is necessary

The mechanism phase is closed because further bridge, weight, duration, or horizon sweeps do not answer whether the target variable is part of a real difficult workload.

The current missing link is construct validity:

$$
\text{controlled semantic variable}
\stackrel{?}{\longrightarrow}
\text{real distributed-evidence compositional state}.
$$

A synthetic-only success cannot close this link.

## 4. One Core Mathematical Model

### 4.1 Data-generating model

Let

$$
E=(E_1,\ldots,E_m)\sim P_E,\qquad
D\sim P_D,\qquad
Q\sim P_Q.
$$

The context and answer are

$$
C=\operatorname{Serialize}(E,D),\qquad
Y=g_{T_Q}(E).
$$

Required assumptions:

$$
Y\perp D\mid E,Q,T_Q,
$$

$$
H(Y\mid E,Q,T_Q)=0
$$

for the controlled task, and every declared necessary evidence item passes a deletion test.

### 4.2 Task-relevant evidence equivalence class

Define

$$
E\sim E'
\iff
g_{T_Q}(E)=g_{T_Q}(E')
\quad
\forall Q\in\operatorname{supp}(Q).
$$

The model does not need to preserve all raw context. It needs to preserve $[E]$, the equivalence class relevant to the supported query family.

If the query family separates the equivalence classes and the model predicts the query answer with error at most $\epsilon$, the target theorem route is a Fano-style lower bound:

$$
I(H_T;[E])
\ge
H([E])
-h(\epsilon)
-\epsilon\log(|\mathcal E/{\sim}|-1).
$$

Status: theorem candidate. Finite-query separability and random-query sampling conditions remain to be written rigorously.

### 4.3 Intermediate variables

For every internal node $v$ of $T_Q$,

$$
Z_v=g_v(Z_{\mathrm{left}(v)},Z_{\mathrm{right}(v)}).
$$

The empirical mechanism audit tests whether $Z_v$ is recoverable and causally usable at $H_T$, then preserved to $H_A$.

### 4.4 Objective conditions

NTP:

$$
L_{\mathrm{NTP}}
=
\sum_t
\operatorname{CE}(q_1(\cdot\mid H_t),Y_{t+1}).
$$

Informative MTP:

$$
L_{\mathrm{MTP-info}}
=
\sum_t\sum_{j=1}^{K}
\lambda_j
\operatorname{CE}(q_j(\cdot\mid H_t),Y_{t+j}),
$$

with a declared nonempty information set at the decision position:

$$
\mathcal I_K(T)
=
\left\{
j:
I(Z;Y_{T+j}\mid Y_{T+1:T+j-1},H_T)>0
\right\}.
$$

Masked MTP uses the same architecture and data but removes the task-informative terms at $T$.

### 4.5 Net task-direction update

Define the extra MTP loss

$$
L_{\mathrm{extra}}
=
L_{\mathrm{MTP-info}}-L_{\mathrm{NTP}}
$$

on matched examples, and held-out task loss $L_{\mathrm{task}}$. The local alignment metric is

$$
\Gamma_{\mathrm{task}}
=
\left\langle
-\nabla_\theta L_{\mathrm{extra}},
-\nabla_\theta L_{\mathrm{task}}
\right\rangle.
$$

Positive $\Gamma_{\mathrm{task}}$ is a necessary local sign guard, not a downstream theorem.

## 5. Falsifiable Hypothesis

**H22:** In a workload satisfying local insufficiency, joint necessity, operator composition, and nuisance invariance, informative future supervision improves a task-relevant, causally used decision representation. This improvement transfers from the controlled synthetic task to held-out real multi-document compositional QA, whereas masking the informative future target removes the gain.

### Support

All must hold:

1. $T_{\mathrm{pair}}>0$ with a positive paired confidence lower bound;
2. `MTP-info` improves $Q_{\mathrm{comp}}$ over both NTP and `MTP-mask` on synthetic and real data;
3. evidence/intermediate-state causal-use metrics improve in the same direction;
4. decision-to-answer preservation improves or at least does not erase the decision-state gain;
5. shortcut and local-language guards pass.

### Falsify

Any one of the following is decisive against the current model:

1. the real task remains solvable from one support document or lexical cues;
2. `MTP-info` improves synthetic $Q_{\mathrm{comp}}$ but not real $Q_{\mathrm{comp}}$;
3. real accuracy improves while evidence/intermediate-state causal-use metrics do not;
4. `MTP-mask` reproduces the full gain;
5. the useful decision-state direction is systematically destroyed before the answer position.

### Insufficient evidence

1. the selected small model is near chance on the full real task;
2. synthetic or real data fail construct-validity guards;
3. causal patching is numerically unstable;
4. confidence intervals are too wide to determine the sign.

An insufficient result triggers dataset/model-capability repair, not a Router design.

## 6. Minimal Decisive Test

### 6.1 Conditions

Exactly three primary conditions:

| Condition | Objective | Decision-position informative horizons | Purpose |
|---|---|---|---|
| `NTP` | standard next-token loss | none beyond next token | baseline |
| `MTP-info` | matched next-$K$ loss | active | tests direct informative supervision |
| `MTP-mask` | same MTP architecture | informative decision terms masked | direct-signal control |

No $K$, bridge-token, loss-weight, or training-duration sweep.

### 6.2 Paired data

Synthetic side:

- two necessary evidence branches;
- one final composition operator;
- controlled $L,d,\tau$;
- matched distractors;
- exact single-evidence, local-window, binding, and lexical guards.

Real side:

- 2WikiMultiHopQA examples with complete support paths;
- original training split for training;
- held-out examples for evaluation;
- topic-matched distractors;
- one-support, support-deletion, support-order, and evidence-swap controls;
- LongBench-format evaluation;
- no LongBench v2 test use for training or tuning.

### 6.3 Primary model

Use one existing small pretrained backbone for all three conditions. The first choice is the existing A11 Qwen3-0.6B infrastructure because it has already passed a nontrivial held-out language capability gate.

Full-parameter training is primary. Parameter-efficient adaptation is exploratory and cannot substitute for a shared-parameter gradient claim.

### 6.4 Primary task score

Let $A_{\mathrm{full}}$ be full-evidence accuracy, $C_{\mathrm{swap}}$ be correct evidence-swap response, and

$$
\operatorname{ExcessAcc}_{\mathrm{one}}
=
\max\left(
0,
\frac{A_{\mathrm{one}}-A_{\mathrm{chance}}}
{1-A_{\mathrm{chance}}}
\right).
$$

Define

$$
Q_{\mathrm{comp}}
=
\min
\left(
A_{\mathrm{full}},
C_{\mathrm{swap}},
1-\operatorname{ExcessAcc}_{\mathrm{one}}
\right).
$$

For $x\in\{\mathrm{syn},\mathrm{real}\}$,

$$
\Delta Q^x
=
Q_{\mathrm{comp}}^x(\mathrm{MTP-info})
-
\max\left[
Q_{\mathrm{comp}}^x(\mathrm{NTP}),
Q_{\mathrm{comp}}^x(\mathrm{MTP-mask})
\right].
$$

Primary metric:

$$
T_{\mathrm{pair}}
=
\min(\Delta Q^{\mathrm{syn}},\Delta Q^{\mathrm{real}}).
$$

### 6.5 Mechanism guards

1. probe accuracy for necessary evidence and $Z_v$;
2. causal hidden-state patching for $Z_v$;
3. distractor-replacement invariance;
4. decision-to-answer task-direction preservation;
5. $\Gamma_{\mathrm{task}}$ sign and magnitude;
6. local next-token loss/accuracy.

## 7. Outcome Table

| Outcome | Interpretation | Next action |
|---|---|---|
| synthetic and real gains; mechanism guards pass | workload model and MTP mechanism transfer are supported | open a separate capacity/conflict anchor |
| synthetic gain only | controlled task is not a valid real-workload model | revise serialization, operators, or real-data mapping |
| real gain without mechanism gain | performance effect exists but current representation account is wrong | search for rival mechanism before method design |
| no gain; model passes capability gate | informative MTP does not help this workload under the tested setup | revise/reject MTP role; do not sweep $K$ |
| model fails capability gate | comparison is uninterpretable | change the primary small model or task difficulty |
| stable operator-conditioned conflict observed later | MoE may be justified | open MoE-necessity anchor |
| no stable operator-conditioned conflict | current workload does not justify a new Router | keep dense model; do not force specialization |

## 8. Claim Boundary And Only Next Decision

Can claim after support:

- the proposed workload is measurable in controlled and real data;
- informative MTP improves a causally used task representation under the tested structured training setup;
- the same directional mechanism transfers to a held-out real multi-document QA task.

Cannot claim:

- general MTP pretraining superiority;
- universal long-context compositionality;
- natural-language generation improvement outside the tested format;
- MoE necessity;
- semantic expert identity or Router utility.

**Only next decision:** approve, revise, or reject this A11_22 workload model and paired protocol. No Router method work begins before this decision and result.
