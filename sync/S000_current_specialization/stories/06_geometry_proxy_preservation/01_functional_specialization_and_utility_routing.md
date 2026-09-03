# From Hidden Geometry To Utility-Grounded Expert Routing

Status: current primary synthesis for the A06 line.

Canonical language: English. Chinese companion:
`01_functional_specialization_and_utility_routing_cn.md`.

## 0. Terminology / Definitions

| Term | Plain meaning | Concrete object or computation | Why it matters | Cannot prove |
|---|---|---|---|---|
| Operational feature | A controlled or measured input condition used to stratify routing | synthetic feature id, stable proxy, or registered workload condition $z$ | Gives routing a falsifiable target | Natural semantic meaning |
| Route-relevant state | A hidden state population whose information is available at the routing decision | states selected at the routed position or by a registered selector | Prevents clustering the wrong population | Expert utility |
| Route margin | The useful expert's score lead over a competitor | $m_{z,a,b}=(w_a-w_b)^\top\mu_z$ | Local assignment buffer | Long-run safety without a tail audit |
| Proxy | A reproducible hidden-state partition without semantic or utility status | split-stable real-DCLM clusters | Bridges synthetic labels to real hidden geometry | A semantic feature or useful expert |
| Counterfactual expert utility | Loss difference obtained by forcing alternative experts on the same input | $L_{z,b}^{cf}-L_{z,a}^{cf}$ | Defines functional expert identity | That a learned Router captures it |
| Functional specialization | Different input conditions stably prefer different expert functions and routing captures value under cost | held-out utility gap, route regret, causal value, activated cost | Final target of A06 | NMI or balanced load alone |
| Selected-path blindness | The selected expert supplies the forward utility signal while unselected experts are not individually evaluated | wrong-rank weighted top-1 remains trapped | Locates a partial-feedback failure | Universal failure of every sparse Router |
| Challenger audition | Execute the incumbent and one additional expert to compare utility | top-1 plus one rotating challenger | Minimal counterfactual feedback tested here | End-to-end systems efficiency |
| Lower-tail certificate | Stop audition only when the weakest routed-population utility tail favors the incumbent | $Q_{0.10}(D)>0$ or lower-CVaR10 $>0$ | Protects minority wrong routes | Safety under joint training or real workloads |
| Oracle routing headroom | Loss reduction available from a held-out best-expert rule over native routing | $G_{oracle}=L_{native}-L_{oracle}$ | Decides whether a workload is worth routing | That the oracle is learnable |

Normalized mutual information (NMI) measures agreement between two
partitions. It can show alignment or collapse, but it cannot establish expert
function. All feature, proxy, and utility claims below retain their stated data
and model boundaries.

## 1. Abstract

A06 asks one complete question: how can a top-1 mixture-of-experts model bind
an input condition to an expert that is actually more useful for it? The line
began with hidden-state geometry and now ends at a real-workload gate.

The evidence establishes four stages. First, feature-level routing is
geometrically reachable, but only when router rows are built from a
route-relevant hidden-state population. Real-DCLM proxy clusters are stable and
linearly routable at step 0, yet ordinary full-sequence training rapidly
overwrites them. Second, preservation is governed locally by finite route
margin. Its motion depends on expert utility, signed background projection,
representation movement, router movement, and optimizer-transmitted step
scale; mean subtraction or spectral initialization alone does not solve this
problem. Third, correct conditional exposure creates held-out specialist
utility, proving that route identity and expert function are different
objects. Fourth, selected-only weighted top-1 can preserve a correct specialist
but cannot discover the same specialist from a wrong rank. One rotating
challenger supplies the missing counterfactual utility, and a per-token lower-
tail certificate safely switches back to top-1 in the frozen four-expert
system.

This is a controlled mechanism result, not yet an LLM Router. The first
registered real-code test now closes one local surface negatively: relevant
cross-file evidence changes final-layer expert counterfactual effects, but the
selected expert is not split stable and its absolute headroom over native
routing is below the registered threshold. The parent unfiltered-workload
question remains broader than this CrossCodeEval test. The next decision is
whether to test training-time selective sharing on one explicit real
rare/common workload, not whether to design another Router from the same
frozen last-layer pool.

## 2. Research Question

The line's research question is:

> Under approximately fixed activated compute, what information and training
> feedback are sufficient to bind different input conditions to experts that
> reduce their held-out loss?

The required contracts are ordered:

1. **Visibility:** the routed state contains the operational feature.
2. **Readability:** router rows can separate the relevant state populations.
3. **Preservation:** training does not irreversibly erase the assignment.
4. **Function:** the assigned expert is better on held-out examples.
5. **Capture:** the learned Router recovers part of the available expert value
   under activated-compute and communication cost.

A06 has controlled evidence through contract 4 and a frozen-system primitive
for contract 5. Its first registered real-code clause failed the joint
stability-and-positive-headroom gate; no pretrained-LLM Router target has been
established.

## 3. Why This Question Is Confusing

Four common substitutions are invalid:

- A cluster visible to an external method is not necessarily available to the
  Router at its decision position.
- High step-0 NMI can come entirely from initialization and says nothing about
  training feedback.
- High route NMI is unchanged by expert permutation and therefore cannot prove
  that the selected expert is useful.
- A large common component is not automatically harmful. Only its signed
  projection on a relevant route boundary consumes the corresponding margin.

The Router is also not a static classifier. Hidden representations, router
rows, expert functions, and optimizer state all evolve. A useful theory must
describe their coupled motion and the information hidden by sparse execution.

## 4. Concrete Data And Training Layout

The evidence uses five deliberately separated surfaces.

| Surface | Data and model | Decides | Does not decide |
|---|---|---|---|
| Initialized synthetic geometry | Four balanced slot/target features and a Transformer hidden-state replay | reachability, population selection, nuisance guards | training or utility |
| One-layer synthetic Transformer+MoE | No learned position embedding, full-sequence LM loss, controlled features and experts | margin dynamics, freezing interventions, utility formation, sparse feedback | natural semantics or scale |
| Real-DCLM proxy audit | Qwen-style top-1 MoE on packed DCLM tokens | proxy stability, step-0 routability, early overwrite | semantic expert identity |
| Dense-LLM representation audit | Qwen3-0.6B attention/residual states $X$, $A$, and $H=X+A$ | candidate representation-source priors | MoE gate causality or rare features |
| Frozen real-code expert audit | Qwen3-Coder-30B-A3B-Instruct on repository-disjoint CrossCodeEval pairs, with a matched final-layer slot swap | context-conditioned expert effects, split stability, and absolute headroom on the registered surface | unfiltered repository-wide headroom, learned routing, or other layers |

The key learned-specialist bridge contains four equally frequent context-
defined tasks. A sequence-start instruction selects a later modular next-token
target. The model has one causal-attention layer, four experts, no learned
positional embedding, and all next-token positions contribute to the language-
model loss. This surface exposes known task identity for evaluation while
allowing full-sequence background gradients.

## 5. Physical Intuition

The correct physical picture is a moving decision boundary on a moving and
anisotropic representation manifold.

```text
training objective
-> representation forms and drifts
-> expert functions acquire conditional utility
-> router receives selected-path feedback
-> optimizer transforms the raw gradient into actual motion
-> route margins cross, recover, or stabilize
```

Two distinct resources are required:

1. **Discriminative state:** hidden directions that distinguish which expert
   function would be useful.
2. **Counterfactual feedback:** evidence about an expert that is not currently
   selected.

Initialization can supply the first resource temporarily. Ordinary top-1
execution can withhold the second. This explains why a geometrically correct
start may be preserved while a wrong start cannot be corrected.

The attention/residual spectrum contributes only a representation prior.
Attention output $A$ has stronger within-sequence continuity and sequence-level
discrimination, while the strong spectrum of $H=X+A$ is dominated by inherited
residual $X$ after layer 1. $A$ is distributed across multiple $H$ bands and is
smaller in amplitude within each band. This does not imply that attention
context is a rare feature; it motivates measuring which source carries
expert-utility information before designing a gate.

## 6. Definitions And Decision Metrics

For workload condition $z$, let routed states have mean $\mu_z$ and covariance
$\Sigma_z$. Let $a(z)$ denote the useful expert and $b$ a competitor.

The center route margin is

$$
m_{z,a,b}=(w_a-w_b)^\top\mu_z.
$$

The low-tail token margin is the fifth percentile of the same score gap over
the routed population. It is the primary local preservation metric because it
detects thin boundaries hidden by a positive center mean.

The held-out counterfactual utility gap is

$$
G_z=\min_{b\ne a(z)}
\left[L_{z,b}^{cf}-L_{z,a(z)}^{cf}\right].
$$

The route regret of a learned Router is

$$
R_{route}=L_{learned}-L_{oracle}.
$$

The workload gate is oracle routing headroom:

$$
G_{oracle}=L_{native}-L_{held\text{-}out\ oracle}.
$$

NMI remains a geometry and identity guard. $G_z$, $R_{route}$, and
$G_{oracle}$ are the functional decision metrics.

## 7. Mathematical Model

### 7.1 Finite-step margin motion

For a fixed condition and expert pair,

$$
m_t=(w_{a,t}-w_{b,t})^\top\mu_{z,t}.
$$

Its exact one-step change is

$$
\begin{aligned}
\Delta m_t
&=(\Delta w_a-\Delta w_b)^\top\mu_{z,t} \\
&\quad +(w_{a,t}-w_{b,t})^\top\Delta\mu_z \\
&\quad +(\Delta w_a-\Delta w_b)^\top\Delta\mu_z.
\end{aligned}
$$

This identity separates router motion, representation motion, and interaction.
It is bookkeeping, not causal attribution; freeze or replay interventions are
required for causality.

### 7.2 Soft-router utility transmission

For

$$
p_e=\operatorname{softmax}(Wh/\tau)_e,
\qquad
\hat y=\sum_ep_eE_e(h),
$$

define expert advantage

$$
A_e=-\langle\nabla_{\hat y}\ell,E_e(h)-\hat y\rangle.
$$

With fixed hidden states, fixed experts, and SGD,

$$
\Delta w_e=\frac{\eta}{\tau}p_eA_eh.
$$

Thus geometry alone does not determine the update sign. The expert function
must have task advantage.

### 7.3 Weighted-top-1 information boundary

For selected expert $r$ and output $\hat y=p_rE_r(h)$,

$$
\Delta w_j
=\frac{\eta}{\tau}p_r(\mathbf 1[j=r]-p_j)B_rh,
\qquad
B_r=-\langle\nabla_{\hat y}\ell,E_r(h)\rangle.
$$

Unselected rows may move through probability competition, but their updates do
not contain their own $E_j(h)$. Selected-only top-1 can reject a poor incumbent
without directly identifying which unselected expert is best.

### 7.4 Functional Router objective

Given state $h$ and activated-compute budget $B$, the functional target is

$$
r^*(h)=\arg\min_{S:\lvert S\rvert\le B}
\mathbb E[\ell(F_S(h),y)\mid h]+\lambda C(S),
$$

where $C(S)$ includes activated computation and communication. A semantic
partition matters only when it predicts this conditional expert utility.

### 7.5 Tail-safe phase switch

For incumbent $e$, challenger $c$, and routed token state $h$, define

$$
D_{e,c}(h)=\ell(E_c(h)) - \ell(E_e(h)).
$$

Positive values favor the incumbent. The controlled stopping rule requires all
directed expert pairs to have positive lower-tail utility, using either
$Q_{0.10}(D)$ or

$$
\operatorname{CVaR}^{low}_{0.10}(D)
=\mathbb E[D\mid D\le Q_{0.10}(D)].
$$

## 8. Propositions And Proof State

| Statement | Status | Boundary |
|---|---|---|
| Positive pairwise center margin preserves the center's current assignment. | Algebraic proposition | Says nothing about future parameter motion or token tails. |
| The finite-step margin decomposition above is exact. | Algebraic identity | Does not assign causal ownership. |
| Soft-router row motion is proportional to probability, expert advantage, and hidden direction under the stated fixed-SGD assumptions. | Chain-rule identity | Does not directly cover top-1, AdamW, or joint training. |
| Weighted top-1 does not use each unselected expert's own output in the selected-path gradient. | Structural statement for the implemented objective | Other sparse estimators may add such information. |
| Lower-tail stopping is safe. | Empirical proposition in the frozen four-expert bridge | Not a theorem for joint training, many experts, or real text. |

## 9. Mechanism Decomposition

The full mechanism is best read as six causal questions:

1. **State selection:** did the construction observe states carrying the
   route-relevant variable?
2. **Initial geometry:** did router rows create positive low-tail margins?
3. **Utility formation:** did conditional exposure make expert functions
   measurably different?
4. **Credit transmission:** did the training objective send corrective pressure
   to the relevant boundary?
5. **Counterfactual coverage:** was any unselected useful expert evaluated?
6. **Phase control:** when is enough evidence available to stop exploration?

The line's main advance is moving the bottleneck through these questions rather
than continuing to tune one geometric initializer.

## 10. Evidence From Anchors

| Current parent anchor | What was established | Auditable local clauses |
|---|---|---|
| `06_00` specialization contract | Functional specialization requires held-out expert-function value; route purity and load are guards. | `06_00_01` operational failure evidence; `06_00_02` hierarchy/utility separation; `06_00_03` real-data definition guard. |
| `06_01` geometry and state discovery | Oracle route-position states make the partition reachable, but tested label-free state selectors fail and real proxies are overwritten by ordinary training. | `06_01_01`--`06_01_07`: nuisance geometry, reachability, state selection, proxy overwrite, selector audits, spectral audit, and static side theory. |
| `06_02` preservation dynamics | Finite low-tail margin is the local budget; utility, signed boundary pressure, representation, Router, and actual step jointly determine crossing and recovery. | `06_02_01` finite basin; `06_02_02` common/background controls; `06_02_03` local signed dynamics; `06_02_04` coupled dynamics. |
| `06_03` utility and sparse discovery | Correct exposure creates specialists; selected-only top-1 can remain trapped; one challenger and a lower-tail certificate repair the controlled failure. | `06_03_01` function formation; `06_03_02` selected-path blindness; `06_03_03` challenger discovery; `06_03_04` tail-safe switch. |
| `06_04` workload gate | Relevant context changes final-layer counterfactual expert effects, but the first registered CrossCodeEval surface fails split stability and positive absolute headroom. | `06_04_01` completed registered failure; the broader unfiltered-workload scope is not adjudicated |

The full anchor-level disposition is maintained in
`../../problem_anchors/06_geometry_proxy_preservation/research_map.md`.

## 11. Experiment Evidence

The most decision-bearing measurements are:

- Real-DCLM raw-center proxy-route NMI falls from `0.7549` at step 0 to
  `0.0410` at step 5 and `0.0131` at step 10.
- In the all-position population audit, route-only feature NMI is `1.000`,
  while all-position mean NMI is `0.797`.
- Correct specialist exposure creates a paired held-out utility-gap increase of
  `8.892` nats/task-token, with 95% confidence interval `[8.694, 9.142]`, while
  route NMI remains `1.0` in both correct and shuffled controls.
- Learned wrong-rank weighted top-1 corrects `0/128` cells at rank 2 and rank 4;
  soft utility coverage corrects `128/128` at both ranks.
- One-challenger full-LM routing corrects `128/128` rank-2 and `125/128`
  rank-4 cells; task-only pair routing corrects every cell.
- q10 and lower-CVaR10 each reach `128/128` correction and retention with zero
  premature stops, while saving median `51%` and `43%` of audition updates.
- On 128 held-out CrossCodeEval examples, relevant context beats an equally
  long nuisance context by `0.20370` nats per target token, but the selected
  expert is not calibration-split stable. The held-out interaction is
  `0.01163` with 95% CI `[0.00336, 0.02022]`, while relevant absolute headroom
  is only `0.00540` with 95% CI `[-0.00105, 0.01225]` and therefore fails.
- The external Attention-Mean report reduces measured expert switch rate from
  `81.84%` to `7.30%`, but test loss worsens from `3.1395` to `3.1920` and the
  eight-task macro average changes from `0.4812` to `0.4787`. This is evidence
  for route continuity and a lower communication-cost term, not functional
  specialization.
- The external Feature-Context-Frozen report has a one-run matched-parameter
  NLL change of `-0.00413` versus standard routing and a no-feature control
  that is `+0.00782` worse than the feature condition. Without shuffled
  ownership, forced-expert utility matrices, or multiple seeds, it remains a
  representation-input diagnostic rather than a specialization result.

The first six measurements support the controlled mechanism chain. The
CrossCodeEval measurement is a direct negative result for one real-code
surface. The two external reports are adjacent evidence about representation
input and systems cost; neither supplies the missing positive expert-utility
headroom.

## 12. Counterexamples And Rival Explanations

- **Load-only repair:** centering and projection can improve load without
  feature identity. Load is a guard, not the target.
- **All-position clustering:** stronger warmup geometry still mixes role-
  specific populations. Better clustering does not repair a wrong sample pool.
- **Spectral initialization:** expert SVD and MPI can improve NMI while leaving
  negative low-tail margin. Spectral structure is not sufficient.
- **Common subtraction:** mean-DNS and common estimators do not preserve the
  full-LM partition. Common energy is not the causal object.
- **Margin alone:** clean positive initialization can still erode under long
  mixed full-LM training. Margin is a state variable, not a self-preserving
  method.
- **Task credit alone:** removing background improves some rank-2 correction
  but does not remove selected-path blindness.
- **Mean utility stopping:** it detects the population-average transition but
  stops before minority routes are corrected.
- **Continuity as specialization:** a lower switch rate can reduce expert-load
  traffic while preserving or worsening task loss. It changes $C(S)$ in the
  functional objective but does not identify a useful expert.
- **Interaction as positive utility:** a positive context-expert interaction
  can arise because one candidate becomes more harmful. Absolute headroom and
  split stability are necessary guards.

## 13. Claim Boundary

**Established in controlled settings:**

- route-relevant hidden geometry can initialize feature-aligned routing;
- positive low-tail margin is the local preservation buffer;
- expert utility, signed background projection, representation motion, router
  motion, and step scale jointly determine margin dynamics;
- conditional exposure can create held-out specialist utility;
- selected-only weighted top-1 can fail to discover an unselected specialist;
- one challenger plus a lower-tail stopping certificate repairs that failure
  under frozen four-expert assumptions;
- on the registered CrossCodeEval final-layer surface, relevant context changes
  expert counterfactual effects, but context interaction alone is not positive
  specialization.

**Not established:**

- natural-language or code experts have stable semantic identities;
- a pretrained LLM has positive held-out oracle routing headroom;
- the controlled Router remains valid while experts and representations train;
- the method scales to many experts or improves wall-clock efficiency;
- attention context is a rare feature;
- multi-token prediction improves routing;
- the proposed functional Router is optimal.

## 14. Anchor Decomposition And Next Anchors

The current chain contains five parent anchors, `06_00`--`06_04`. Repeated
common subtraction, denoising, spectral initialization, fixed-expert recovery,
and synthetic stopping variants are local subanchor evidence rather than
independent decision steps. Parent `06_04` now contains one completed local
failure: the CrossCodeEval final-layer frozen pool does not expose a stable,
context-favored positive headroom target. This does not prove that all
unfiltered repository-code workloads or all layers lack headroom.

The line must not create a Router-capture anchor from this result. Its only
candidate next branch is a human-approved training-time selective-sharing test
that asks whether stable positive utility can be created on an explicit real
rare/common workload.

## 15. Relation To Mainline

A06 now owns three interfaces:

- A05 supplies failure priors such as early lock-in and shortcut routing.
- A06 establishes whether a feature-expert binding can be discovered,
  functionalized, corrected, and evaluated.
- A07 may ask whether the resulting partition reduces interference only after
  real utility and Router capture are established.

The A11 multi-token-prediction line remains independent. A bridge is justified
only if both lines pass their own workload-level gates and the same causal
variable determines future prediction and expert utility.

## 16. Next Decision

> Should A06 approve one training-time selective-sharing test on an explicit
> real rare/common workload after the frozen CrossCodeEval final-layer pool
> failed split stability and positive absolute headroom?

If no, close this branch at the current boundary. If yes, formalize one anchor
and protocol before any implementation; do not continue frozen-pool mining or
construct a Router from route continuity alone.

## Source Map

- Anchor map: `../../problem_anchors/06_geometry_proxy_preservation/research_map.md`
- Active parent anchor: `../../problem_anchors/06_geometry_proxy_preservation/06_04_real_workload_utility_headroom/06_04_real_workload_utility_headroom_anchor.md`
- Completed real-code subanchor: `../../problem_anchors/06_geometry_proxy_preservation/06_04_real_workload_utility_headroom/subanchors/06_04_01_context_conditioned_expert_utility_anchor.md`
- Real-code result: `../../experiments/A06/06_04_real_workload_utility_headroom/A06_04_01_E01_context_conditioned_expert_utility/summary.md`
- External source fragment: `anchor_threads/06_04/story_fragment.md`
- Utility formation: `../../experiments/A06/06_03_utility_binding_and_sparse_discovery/A06_03_01_E01_trainable_expert_utility/summary.md`
- Wrong-rank failure: `../../experiments/A06/06_03_utility_binding_and_sparse_discovery/A06_03_02_E01_wrong_rank_correction/summary.md`
- One-challenger discovery: `../../experiments/A06/06_03_utility_binding_and_sparse_discovery/A06_03_03_E01_rotating_challenger/summary.md`
- Tail-safe stopping: `../../experiments/A06/06_03_utility_binding_and_sparse_discovery/A06_03_04_E03_tail_safe_certificate/summary.md`
