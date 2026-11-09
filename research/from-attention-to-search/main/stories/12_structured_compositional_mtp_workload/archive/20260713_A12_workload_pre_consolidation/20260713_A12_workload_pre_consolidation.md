# From Distributed Evidence to Compositional Decisions

Archived pre-consolidation snapshot. Statements below describe the historical state at capture time and are not the current claim boundary.

## Status

- Document type: canonical prospective story for the A11 objective line.
- Chinese companion: `20260713_workload_pre_consolidation_cn.md`.
- Current stage: proposed `01-2` workload-modeling stage; pending model review before a formal anchor or protocol.
- Evidence boundary: A11_01--A11_20 remain valid controlled mechanism evidence, but no longer define the research mainline.
- A11_21 status: retained as one real-workload candidate, not the next automatic experiment.
- Repository naming: `01-2` is the conceptual stage name. If approved, the next new anchor keeps chronological repository numbering and starts at A11_22.

## 0. Terminology / Definitions

| Term | Plain meaning | Concrete object | Why it matters | What it cannot prove |
|---|---|---|---|---|
| next-token prediction (NTP) | predict only the immediately following token from a prefix state | $L_{NTP}(h_T)=\operatorname{CE}(q_1(h_T),Y_{T+1})$ | baseline objective | inability to learn long context |
| multi-token prediction (MTP) | predict several future offsets from the same prefix state | $L_K(h_T)=\sum_{j=1}^K\lambda_j\operatorname{CE}(q_j(h_T),Y_{T+j})$ | candidate earlier supervision path | that larger $K$ is better |
| distributed evidence | locally readable facts placed in different parts of a context | evidence spans $E_1,\ldots,E_m$ | the real input structure | that the final decision is compositional |
| composition graph | an operator-labeled tree or directed acyclic graph that combines local states | $G=(V,E,r)$ | specifies which facts must interact | that a model internally follows the graph |
| root decision | the final state produced by the graph | $Y^*=C_{\mathrm{root}}$ | the behavioral target | all downstream quality |
| retention span | distance from evidence to the decision boundary | $D$ tokens or graph edges | long-context axis | MTP prediction horizon |
| composition depth | longest leaf-to-root operator path | $d$ | computation axis | context length |
| decision-reveal latency | first output offset whose correct target depends on $Y^*$ | $\tau=\min\{j:I(Y^*;Y_{T+j}\mid W_T)>0\}$ | determines whether an MTP head directly covers the decision | composition difficulty |
| held-out compositional score | weakest model behavior required for a valid decision | $Q_{comp}=\min\{A_{root},S_{cf},S_{struct},C_{inv}\}$ | common method score | internal algorithm identity |
| compute to threshold | training compute needed to reach and sustain a target score | $C_\alpha=\inf\{c:Q_{comp}(c)\ge\alpha\}$ | primary MTP-versus-NTP efficiency metric | wall-clock portability across systems |

## 1. Abstract

The target workload is **long-context distributed-evidence composition**: each local fact is easy to recover, but no local fact or short chain is sufficient; a final action requires combining many facts through an explicit or latent relation structure.

The MTP question must therefore be stated on this workload rather than on a pre-given branch label:

> At matched total training compute, does MTP that covers the root-decision token learn held-out compositional decisions more efficiently than NTP, and is any gain caused by earlier root-decision supervision rather than extra loss, output serialization, retention distance, or memorization?

The current A11 results prove a narrower statement: a covered informative future target can directly force a current hidden state to encode a pre-given variable and can create positive local semantic-margin motion under controlled assumptions. They do not prove that the model learned the map $(Z_{1:m},G)\mapsto Y^*$, nor that the extra representation improves a real decision. Those results become mechanism lemmas used only after the workload and behavioral comparison pass.

The first decisive model is a depth-2, four-leaf symbolic composition tree with balanced quasigroup operators. It gives exact local insufficiency, exact counterfactual sensitivity, balanced labels, and a clean separation among composition depth $d$, retention span $D$, and decision-reveal latency $\tau$. No new Router or MTP method should be designed before this workload gate is accepted and tested.

## 2. Research Question

### Parent problem

What difficult workload should justify MTP, mixture-of-experts computation, or a learned Router?

### A11 `01-2` decision question

Holding context length, decision-reveal latency, model size, data, and total training compute fixed, does covering the root decision with MTP reduce the compute needed to learn **unseen compositions**, compared with NTP?

This question is deliberately about a task-level capability. Hidden-state information, gradient cosine, and private-head accuracy are mechanism diagnostics, not the decision metric.

## 3. Why This Question Is Confusing

1. **Distance is not composition.** A long `A -> B -> C -> ...` chain may consist only of easy local transitions. Increasing filler length changes retention span $D$, not composition depth $d$.
2. **A future variable is not a computed variable.** Replacing a branch label $Z$ by a symbol named $C$ does not show that the model learned $C=F_G(Z_{1:m})$.
3. **Target coverage is not task benefit.** MTP may make $Y^*$ readable at $h_T$ without improving the common autoregressive behavior.
4. **Output wording can manufacture an advantage.** If the answer token appears at offset one, NTP already receives direct supervision. If a generic phrase delays it, MTP may only be overcoming serialization latency.
5. **All-position NTP has an indirect path.** NTP predicts the decision token at a later state and updates shared parameters. The comparison is earlier direct supervision versus later indirect transfer, not “MTP learns, NTP cannot.”
6. **Extra targets add compute and gradient dose.** A fair claim needs compute matching, a loss-dose control, and an informative-offset mask.
7. **Better representation is not better reasoning.** Only held-out graph/assignment generalization and counterfactual behavior distinguish rule use from memorized labels.

## 4. Concrete Data / Training Layout

### 4.1 Real-world parent: distributed deployment authorization

Consider a repository-scale deployment decision. Evidence is spread across monitoring reports, schema checks, security policy, and rollback configuration.

| Local state | Evidence span | Value |
|---|---|---:|
| $Z_1$ | service health is within the release threshold | 1 |
| $Z_2$ | the schema change is backward compatible | 1 |
| $Z_3$ | the release is high risk | 1 |
| $Z_4$ | a verified rollback snapshot exists | 0 |

The policy graph is

$$
C_1=Z_1\land Z_2,
$$

$$
C_2=\neg Z_3\lor Z_4,
$$

$$
Y^*=C_1\land C_2.
$$

For this example, $C_1=1$, $C_2=0$, and $Y^*=0$: deployment must be denied. Each local statement is easy; the decision requires four facts and three relations. A real instance can be checked against a policy engine, type checker, build, or test suite rather than against a subjective rationale.

The context may serialize the evidence in a random order with unrelated reports between spans. The output may be:

```text
Review result : deployment DENIED
```

The location of `DENIED` must be measured under the actual tokenizer. It must not be assumed to occur at a convenient MTP offset.

### 4.2 Simplification chain

| Level | Retained | Removed | Question answered | Main validity risk |
|---|---|---|---|---|
| M4 real distributed decision | natural language/code, noisy evidence, implicit graph, executable outcome | nothing | does the phenomenon exist in a useful workload? | confounding world knowledge and ambiguous labels |
| M3 controlled text | paraphrases, distractors, evidence permutation, explicit rules | implicit world knowledge, unresolved labels | can a model extract and combine text evidence? | lexical/template shortcuts |
| M2 symbolic graph | leaf values, operator labels, variable trees | language and retrieval noise | can a model learn the composition rule? | memorized graph/tuple table |
| M1 minimal decisive model | four leaves, depth two, balanced non-associative operators, controlled $\tau$ | distance, language, large scale | does MTP improve composition learning under exact controls? | synthetic-to-real transfer |
| M0 existing A11 branch model | one pre-given variable and delayed target | the composition map itself | does a covered target directly shape $h_T$? | cannot answer the workload question |

The simplification is valid only if each lower level preserves the parent causal dependency while removing one confound. M0 is useful but too simple to stand as the research mainline.

### 4.3 Minimal numerical example

Let the state alphabet be $\mathcal A=\{0,1,2\}$. Use

$$
\phi_0(a,b)=a+b\pmod 3,
$$

$$
\phi_1(a,b)=a+2b\pmod 3,
$$

$$
\phi_2(a,b)=2a+b\pmod 3.
$$

For $(Z_1,Z_2,Z_3,Z_4)=(2,1,0,2)$,

$$
C_1=\phi_0(2,1)=0,
\qquad
C_2=\phi_1(0,2)=1,
$$

$$
Y^*=\phi_2(0,1)=1.
$$

A controlled atomic-token sequence is

```text
[Z1=2] ... [Z2=1] ... [Z3=0] ... [Z4=2]
[R12=phi0] [R34=phi1] [Rroot=phi2] [QUERY]
[P0] [P1] [S1]
```

At the `[QUERY]` boundary, $\tau=3$. NTP predicts shared `[P0]`; MTP with $K=3$ also predicts root code `[S1]`. The full benchmark should use several sampled non-associative quasigroup tables and reject operator sets with weak tree sensitivity; the affine example above is only a readable instance.

## 5. Physical Intuition

The hard object is a global sufficient state

$$
Y^*=F_G(Z_1,\ldots,Z_m)
$$

that cannot be obtained from a local fact. MTP does not create the composition rule. Its plausible role is narrower: when the immediate continuation after the evidence boundary is locally generic but a nearby future token reveals $Y^*$, MTP attaches the root-decision error to the earlier state $h_T$.

The proposed causal chain is

$$
\text{distributed facts}
\rightarrow
\text{correct composition}
\rightarrow
Y^*
\rightarrow
\text{covered future target}
\rightarrow
\text{earlier task-directed gradient}
\rightarrow
\text{lower compute to valid behavior}.
$$

Only the fourth-to-fifth link has controlled A11 support. The new line must test the first three and the final behavioral link.

## 6. Definitions And Metrics

### 6.1 Workload axes

Define

$$
\Omega=(m,d,R,D,\eta,\tau,\mathcal S),
$$

where $m$ is leaf count, $d$ is graph depth, $R$ is operator-family size, $D$ is evidence span, $\eta$ is distractor/language noise, $\tau$ is decision-reveal latency, and $\mathcal S$ specifies the generalization split.

These axes must be independently controllable. In particular, $d$, $D$, and $\tau$ may not be changed together in the first causal experiment.

### 6.2 Behavioral score

For held-out leaf assignments and held-out graph compositions, define:

- $A_{root}$: native root-decision accuracy;
- $S_{cf}$: correctness after changing exactly one causally necessary leaf;
- $S_{struct}$: correctness after changing an operator or tree edge while holding leaf text fixed;
- $C_{inv}$: consistency under evidence permutation and meaning-preserving serialization.

The common score is

$$
Q_{comp}=\min\{A_{root},S_{cf},S_{struct},C_{inv}\}.
$$

The minimum prevents ordinary accuracy from hiding a failed causal guard. It cannot prove the model literally executes the supplied tree.

### 6.3 Primary method metric

At matched total training FLOPs, define

$$
C_\alpha(o)=
\inf\left\{c:Q_{comp}^{(o)}(c)\ge\alpha
\text{ for a preregistered sustained window}\right\},
$$

for objective $o\in\{NTP,MTP\}$. The MTP efficiency advantage is

$$
\Delta C_\alpha=C_\alpha(NTP)-C_\alpha(MTP).
$$

Positive $\Delta C_\alpha$ means MTP needs less total compute. Backbone-update and data-token counts are secondary decomposition metrics, because MTP performs extra head computation.

## 7. Mathematical Model

### 7.1 Latent task

Let

$$
Z_i\overset{i.i.d.}{\sim}\operatorname{Unif}(\mathcal A_q),
\qquad i=1,\ldots,m.
$$

Let $G$ be an operator-labeled full binary tree. Leaves carry $C_i=Z_i$. Each internal node $v$ computes

$$
C_v=\phi_{r_v}(C_{l(v)},C_{r(v)}),
$$

and

$$
Y^*=C_{root}.
$$

Each $\phi_r$ is a quasigroup operation: fixing either input makes the map from the other input to the output a permutation. The minimal benchmark also requires nontrivial non-associativity and empirical tree-reparenting sensitivity.

### 7.2 Text realization

Each leaf is expressed by a local span

$$
E_i\sim P_i(\cdot\mid Z_i).
$$

The full context is

$$
X_{\le T}
=\operatorname{Serialize}(E_{1:m},G,\pi,D,\eta),
$$

where $\pi$ is evidence order. The evidence boundary $T$ occurs only after all required facts and rules are available.

### 7.3 Output realization

For controlled decision-reveal latency $\tau$,

$$
Y_{T+j}=A_j\quad(1\le j<\tau),
\qquad
Y_{T+\tau}=S_{Y^*},
$$

where the $A_j$ distribution is independent of $Y^*$ and $Y^*\mapsto S_{Y^*}$ is one-to-one.

At $T$,

$$
L_{NTP,T}=\operatorname{CE}(q_1(h_T),A_1),
$$

while MTP with $K\ge\tau$ includes

$$
\lambda_\tau\operatorname{CE}(q_\tau(h_T),S_{Y^*}).
$$

All-position NTP later predicts $S_{Y^*}$ from $h_{T+\tau-1}$. Thus the hypothesized advantage is earlier supervision of the fully informed boundary state, not exclusive access to the label.

## 8. Propositions And Proof State

### Proposition 1: exact missing-leaf insufficiency in M1

For a tree of quasigroup operators with independent uniform leaves, if any one leaf is unobserved, the root is uniform conditional on all observed leaves and $G$:

$$
H(Y^*\mid Z_S,G)=\log q
\quad\text{for every proper subset }S\subsetneq\{1,\ldots,m\}.
$$

**Proof.** Fix every leaf except one missing leaf $Z_i$. Along the unique path from $Z_i$ to the root, each parent is a permutation of the child on that path when the sibling is fixed. The composition of permutations is a permutation, so the root is a bijective function of uniform $Z_i$ and is therefore uniform. Averaging over any additional missing leaves preserves uniformity. Consequently, no proper subset improves on chance, while all leaves and $G$ determine the root exactly.

This establishes an exact composition requirement for M1. It does not establish that real AND/OR decisions have the same local-insufficiency property.

### Proposition 2: covered-root representation consequence

If $S_{Y^*}$ is a one-to-one code and

$$
\mathbb E[-\log q_\tau(S_{Y^*}\mid h_T)]\le\varepsilon,
$$

then

$$
I(h_T;Y^*)\ge H(Y^*)-\varepsilon.
$$

This is the existing A11 representation argument with the pre-given branch variable replaced by the computed root. It proves only a consequence of low covered-head loss. It does not prove that optimization reaches low loss or that the model generalizes the composition rule.

### Empirical proposition to decide

Under matched total compute and valid held-out compositions,

$$
K\ge\tau
\quad\Longrightarrow\quad
\Delta C_\alpha>0
$$

is an empirical hypothesis, not a theorem. It is supported as a composition-specific mechanism only if the gain disappears when the informative offset is masked, survives an equal-loss-dose control, and changes with $d$ rather than only with $D$ or output wording.

## 9. Mechanism Decomposition

| Gate | Question | Primary object | Current status |
|---|---|---|---|
| workload validity | are local facts easy but the root genuinely compositional? | oracle, missing-leaf, counterfactual, tree-sensitivity guards | proposed M1 model |
| evidence extraction | are $Z_i$ recovered from each $E_i$? | leaf accuracy | not yet tested in text |
| composition formation | does the model generalize $(Z_{1:m},G)\mapsto Y^*$? | $Q_{comp}$ | not established |
| target exposure | does $K$ cover the root-dependent output offset? | $K\ge\tau$ | controlled A11 mechanism established |
| parameter absorption | does the direct gradient survive sharing and background loss? | task-directed parameter velocity | locally supported, conditional |
| behavioral efficiency | does common native behavior improve per total compute? | $C_\alpha$ | not supported by A11_20 |

Method design begins only after a failed gate is localized. A method that improves a score without identifying which gate changed is engineering evidence, not the requested mechanism result.

## 10. Evidence From Existing Anchors

| Source | What it establishes | New role | What it does not establish |
|---|---|---|---|
| A11_01 | covered second target can separate a pre-given branch in $h_T$ | minimal target-exposure lemma | composition learning |
| A11_04--A11_10 | informative-horizon coverage and output-direction geometry control local semantic motion | mechanism diagnostics after a task effect exists | real task efficiency |
| A11_11--A11_12 | direct semantic motion can enter parameters but background terms can change the net sign | parameter-absorption decomposition | robust end behavior |
| A11_13 | a distant state can be made causally valid under paraphrase and counterfactual guards | construct-validity template | hierarchical composition |
| A11_14--A11_20 | private MTP learning and local margin effects do not reliably produce common behavioral advantage | decisive negative boundary | MTP is useless on compositional workloads |
| A11_21 | repository code offers a measurable real-workload candidate | possible M4 audit after 01-2 | that code is the unique or already valid workload |

## 11. Experiment Route

The route must move from simple to complex and stop whenever a gate fails:

```text
M1 exact symbolic workload validity
-> M1 compute-matched NTP/MTP comparison
-> d x D x tau causal separation
-> M2 variable graph and operator generalization
-> M3 controlled text extraction and paraphrase bridge
-> M4 real repository/deployment evidence and executable validation
-> capacity phase diagram
-> only then a targeted objective or architecture method
```

The first method comparison must include four causal roles, not a broad sweep:

1. NTP baseline;
2. MTP with $K\ge\tau$;
3. the same MTP objective with the root-informative offset masked;
4. an equal-loss-dose or informative-offset-only control.

These conditions distinguish future root supervision from extra compute, more gradient, and unrelated future targets. Exact seeds, thresholds, and configurations belong in a later approved protocol.

The comparison is decisive only through the following outcome map:

| Observed pattern | Interpretation | Research decision |
|---|---|---|
| covered MTP lowers $C_\alpha$, while masked MTP and equal-dose controls do not | earlier root-decision supervision is a supported cause in M1 | proceed to the $d\times D\times\tau$ separation |
| NTP and covered MTP have matched $C_\alpha$ with valid learning | the claimed MTP efficiency benefit is weakened in the minimal composition task | park method design; do not descend into gradient tuning |
| covered, masked, and equal-dose conditions all improve similarly | extra optimization dose or compute, not root information, explains the gain | revise the objective hypothesis |
| private-head or probe metrics improve but $Q_{comp}$ does not | representation changed without useful composition behavior | stop at a representation claim |
| neither objective learns valid held-out composition | the method comparison is insufficient because workload difficulty, capacity, or implementation failed first | localize that earlier gate before comparing objectives again |

## 12. Counterexamples And Rival Explanations

1. **Retention-only explanation:** MTP gain changes with $D$ but not $d$; then the result concerns memory, not composition.
2. **Serialization-only explanation:** gain appears only when a generic phrase delays the label; then the claim is earlier label exposure, not general reasoning.
3. **Extra-loss explanation:** masked or uninformative future targets give the same gain; then semantic coverage is not causal.
4. **Memorization explanation:** seen tuples pass but unseen graphs or one-leaf counterfactuals fail.
5. **Intermediate-label leakage:** providing $C_v$ targets changes the task into supervised reasoning traces. The first decisive comparison therefore exposes only the final root code.
6. **Capacity explanation:** small models may be unable to fit multiple objectives; large models may make NTP and MTP converge. Scale is a later axis, not an assumption.
7. **Synthetic-operator explanation:** quasigroup results may not transfer to AND/OR, causal, temporal, or exception rules. M1 earns only a clean mechanism claim.

## 13. Claim Boundary

### Can claim now

1. The advisor's target workload is better modeled as distributed evidence plus structured composition than as a single delayed variable.
2. $d$, $D$, and $\tau$ are distinct causal axes and must be independently controlled.
3. A quasigroup tree supplies an exact minimal construction in which every leaf is necessary and the root is balanced.
4. Existing A11 results explain one possible direct-supervision mechanism after a computed root exists.
5. Current evidence does not support a common behavioral MTP efficiency advantage.

### Cannot claim now

1. MTP is better than NTP on compositional workloads.
2. MTP directly solves long-context retention or hierarchical computation.
3. A hidden-state information bound proves held-out composition.
4. Code is already the decisive real workload.
5. MoE or a Router is needed before harmful operator interference and functional expert value are demonstrated.

## 14. Anchor Decomposition / Next Anchors

The conceptual `01-2` stage maps to chronological A11 anchors as follows:

| Proposed anchor | One decision | Primary metric | Opens only if |
|---|---|---|---|
| A11_22 compositional-workload validity | does M1 exactly realize local insufficiency, root sufficiency, counterfactual sensitivity, and tree sensitivity? | workload construct-validity gate | this story model is approved |
| A11_23 minimal objective comparison | does covered MTP reduce total compute to held-out composition threshold? | $C_\alpha$ | A11_22 passes and protocol is approved |
| A11_24 causal-axis separation | is any advantage caused by composition depth rather than distance or serialization? | preregistered $d\times D\times\tau$ interaction | A11_23 shows a nontrivial effect or ambiguity |
| A11_25 controlled-text bridge | does the result survive evidence extraction, paraphrase, order, and distractors? | text-layer $Q_{comp}$ | symbolic mechanism passes |
| A11_26 real workload audit | does the phenomenon occur in executable repository/deployment tasks? | eligible prevalence plus executable correctness | controlled text passes |
| A11_27 scale phase diagram | how does the advantage vary with capacity and data? | compute-normalized advantage across scale | a valid workload and stable base effect exist |

No formal A11_22 anchor or protocol is created by this story. The next artifact is created only after model review, following the anchor approval workflow.

## 15. Relation To MoE And Router Design

MTP and MoE address different candidate bottlenecks on the same workload:

- MTP asks whether the global decision state is supervised early enough.
- MoE asks whether heterogeneous composition operators should use conditional parameter subsets.
- A Router asks how to choose the parameter subset that has the best functional effect for the current computation.

MoE/Router work is premature until a dense model exhibits harmful cross-operator transfer at matched capacity. Gradient cosine alone is not enough. A functional interference measure is the increase in operator-$r'$ loss after an update for operator $r$:

$$
H_{r\rightarrow r'}
=L_{r'}(\theta-\eta g_r)-L_{r'}(\theta).
$$

Only persistent positive harm linked to worse $Q_{comp}$ justifies an oracle expert-separation test. Learned routing is judged by functional route regret,

$$
R_{route}
=\mathbb E\left[L_{e_\psi(x)}(x)-\min_e L_e(x)\right],
$$

not by balanced load or operator-label agreement alone. A joint MTP--Router anchor opens only after MTP has a task-level effect and oracle expert separation has functional value independently.

## 16. Next Decision

Approve, revise, or reject the `01-2` workload model as one unit:

> real parent = distributed deployment/repository decision; minimal core = depth-2 quasigroup composition tree; primary method conclusion = compute to sustained held-out compositional behavior.

Until that model is accepted, do not run A11_21, create A11_22, tune MTP, or connect A11 to MoE.

## Source Map

Advisor dialogue:

- `daily_research_reports/0710/0710_MTP_Router_对话校订稿.md`

Previous active story snapshot:

- `archive/20260711_A11_21_workload_grounded_reframe/20260711_A11_21_workload_grounded_reframe_cn.md`

Core anchors and evidence:

- `../../../../problem_anchors/11_long_horizon_mtp_objective/11_01_k2_branch_delayed_next_two_anchor.md`
- `../../../../problem_anchors/11_long_horizon_mtp_objective/11_13_downstream_semantic_state_validity_anchor.md`
- `../../../../problem_anchors/11_long_horizon_mtp_objective/11_20_end_to_end_bridge_conditioned_efficiency_anchor.md`
- `../../../../problem_anchors/11_long_horizon_mtp_objective/11_21_repository_code_semantic_latency_workload_anchor.md`
- `../../../../experiments/A11/A11_01_k2_branch_delayed_next_two/summary.md`
- `../../../../experiments/A11/A11_13_downstream_semantic_state_validity/summary.md`
- `../../../../experiments/A11/A11_20_end_to_end_bridge_conditioned_efficiency/summary.md`
