# Long-Horizon Compositional Workloads: Task Properties, Credit Paths, and Standard-Head Use

Date: 2026-07-16

Status: AI theory-clarification draft; not the researcher's judgment, a formal
story, an anchor, or a Protocol.

Chinese companion:
[06_long_horizon_compositional_workload_theory_cn.md](06_long_horizon_compositional_workload_theory_cn.md)

## 1. One-Sentence Conclusion

> **The causal object is not token distance. A plausible MTP advantage requires
> causally necessary early evidence with no bypass, composition of multiple
> locally insufficient evidence items through a state relay, weak/noisy/
> conflicting later NTP credit under a fixed learner and budget, and an
> informative early MTP update that is transported and causally used by the
> standard next-token head.**

All-position NTP eventually supervises the answer token. MTP therefore cannot
be information-theoretically necessary from the data distribution alone. Its
possible necessity is a finite-optimization statement relative to a model,
initialization, budget, and interface.

## 2. Advisor Question Chain

The questions are ordered by causal dependence.

1. **What is the causal next-one/next-two difference?** The 0706 recording
   proposes a first-to-last dependence intuition. The 0713 guidance corrects
   the order: short tasks can also expose the objective difference, so the
   objective mechanism precedes the workload label. A11_01 supports only an
   inclusion law: a direct signal appears when the horizon first includes an
   informative target, and its sign depends on target-direction geometry.
2. **Why does formation not imply use?** A11_02 establishes shared-parameter
   reachability while showing signed all-position background. A11_03 finds
   exact source K/V perfectly readable under every condition but no registered
   informative-MTP readability increment and no stable strong standard-head
   use increment.
3. **Why might code/planning need the mechanism?** The advisor's decision-tree,
   deep-logic, and code-versus-text account is a hypothesis. A sharper
   candidate is deterministic delayed dependence, multi-evidence state
   composition, and relatively low-noise future-state supervision—not the
   `code` label. Tokenization, repetition, data quality, exact-match scoring,
   compute, and local templates remain rivals.
4. **How can separability reach MoE?** Two bridges remain unproved: MTP must
   form a task-necessary state that the standard head uses, and that state must
   predict held-out conditional expert utility. A06 retains the Router
   criterion; readability, anisotropy, clustering, and route NMI are not
   substitutes.

## 3. Operational Definition

Relative to local-window width $w$ and the standard next-token head, a
**functional long-horizon compositional workload** has early semantic evidence
farther than $w$ from the answer; matched counterfactual changes to that
evidence change the answer while the answer-local window stays fixed; at least
two individually insufficient evidence items must be composed through ordered
state updates; semantics-preserving paraphrases preserve the answer; and the
standard head fails when the intended relay is broken.

| Object | Computation | Logical role |
| --- | --- | --- |
| token distance | $D=\operatorname{pos}(Y)-\operatorname{pos}(E_0)$ | geometric descriptor only; neither sufficient nor necessary for the objective mechanism |
| local-window insufficiency | collision $W_w(x)=W_w(x')$ with $Y(x)\neq Y(x')$, or nonzero local Bayes risk | necessary for a nonlocal claim |
| delayed counterfactual dependence | $Y(do(E_0=e))\neq Y(do(E_0=e'))$ with other evidence fixed | necessary for early-evidence relevance |
| paraphrase invariance | $Y(\tau(E_0),E_{1:L})=Y(E_0,E_{1:L})$ for semantics-preserving $\tau$ | necessary guard for a semantic/generalization claim, not every distance claim |
| multi-evidence necessity | every single evidence view is insufficient, while the joint view identifies $Y$ | necessary for a compositional claim |
| state transport | matched state/relay intervention changes a later state or final correct-answer probability | necessary mechanism for early-state use |
| standard-head causal use | intended-relay intervention changes ordinary $q_1$ loss/output with bypasses controlled | necessary for a standard-head benefit claim |

An informative early MTP signal additionally requires a nuisance context
$B_t$ that excludes the studied evidence $E_j$ or latent variable $Z_j$, and

$$
I\!\left(
Z_j;X_{t+k}
\mid B_t,X_{t+1:t+k-1}
\right)>0.
$$

This condition is necessary for an information-specific direct signal at
$h_t$; it is not sufficient for transport or use. If $Z_j$ is a deterministic
function of the full prefix, conditioning on that full prefix would make the
mutual information zero by definition.

## 4. Minimal Model and Objectives

Let distributed evidence induce an ideal latent computation

$$
z_0=\phi(E_0),
\qquad
z_{j+1}=F_j(z_j,E_{j+1}),
\qquad
Y=G(z_L).
$$

The learned carrier is

$$
s_0=\operatorname{encode}_\theta(x_{\mathrm{early}}),
\qquad
s_{j+1}=f_{\theta,j}(s_j,x_j),
\qquad
p_\theta(Y)=q_1(s_L).
$$

For deterministic composition, require

$$
H(Y\mid W_w,E_i)>0\quad\text{for every single }E_i,
\qquad
H(Y\mid W_w,E_0,\ldots,E_L)=0,
$$

plus a matched counterfactual witness.

A minimal abstract carrier may draw update rules per sample:

$$
z_1=F_a(q),
\qquad
Y=G_b(z_1),
$$

with $a$ early, $b$ intermediate, and $q$ answer-local. Neither $(a,q)$ nor
$(b,q)$ suffices. Rules must recombine across samples so the task is not a
fixed-pair/table lookup. This is a mathematical shape, not an approved data
implementation.

Forbidden shortcuts include an answer or branch-label leak, bijection
completion after row deletion, a sufficient final local window, a fixed
pair/table lookup, an auxiliary-only solution unused by $q_1$, and
generator/position/length/frequency leakage.

The all-position objectives are

$$
\mathcal L_{\mathrm{NTP}}
=
\mathbb E\sum_{t=1}^{T-1}
\ell(q_1(h_t),X_{t+1}),
$$

$$
\mathcal L_{\mathrm{MTP},K}
=
\mathbb E\sum_{t=1}^{T-1}
\sum_{k=1}^{\min(K,T-t)}
\lambda_k\ell(q_k(h_t),X_{t+k}).
$$

For target $X_{t+k}$, define

$$
J_{t\rightarrow t+k-1}
=
\frac{\partial h_{t+k-1}}{\partial h_t}.
$$

The NTP later/indirect early-state credit is

$$
g^{\mathrm{NTP}}_{t,k}
=
J_{t\rightarrow t+k-1}^{\top}
\nabla_{h_{t+k-1}}
\ell(q_1(h_{t+k-1}),X_{t+k}),
$$

whereas the MTP direct credit is

$$
g^{\mathrm{MTP}}_{t,k}
=
\nabla_{h_t}\ell(q_k(h_t),X_{t+k}).
$$

The comparison concerns path length, Jacobian products, useful-direction SNR,
and interference. For a task direction $u$,

$$
\operatorname{SNR}_u(g)
=
\frac{\mathbb E\langle u,g\rangle}
{\sqrt{\operatorname{Var}(\langle u,g\rangle)+\epsilon}}.
$$

If $L\gg K$, MTP still does not directly predict the final answer from the
first state. It can only provide local lookahead credit at multiple
boundaries. A long-range advantage therefore requires those local credits to
teach a transportable state-update rule.

## 5. Bounded Theory

### Assumptions

NTP and MTP share data, backbone, and standard $q_1$ evaluation. The main NTP
coefficient is held fixed; information-specific claims ultimately require a
matched shared-aux contrast. Local derivatives and bounded Taylor remainders
exist. The task has the early-evidence, joint-composition, and intended-relay
properties above. Efficiency is defined under a fixed learner,
initialization, and compute/token budget, not at unconstrained Bayes optimum.

### Proposition 1: No distance-only information-theoretic necessity

If the model family represents the true next-token conditionals,
all-position NTP reaches the population cross-entropy optimum, and
$Y=X_T$ is identifiable from $X_{<T}$, then the standard NTP head at $T-1$
already achieves Bayes-optimal answer risk. MTP cannot lower that Bayes risk.

**Proof.** Cross-entropy is a strictly proper scoring rule. The $T-1$ NTP term
recovers $P(X_T\mid X_{<T})$ at the population optimum. No auxiliary objective
can outperform the true conditional distribution on the same standard-head
risk. $\square$

### Proposition 2: Sufficient condition for stronger early credit

Let $R_j(s_j)$ measure carrier-state error and
$u_j=\nabla_{s_j}R_j$. Assume the informative direct gradient $d_j$ has
$\mathbb E\langle u_j,d_j\rangle\geq\alpha>0$, the later target gradient norm
is at most $B$, each intermediate Jacobian has operator norm at most
$\rho<1$, other MTP horizons contribute at most $c$ total negative alignment,
and pulling the state gradient back to shared parameters is nonzero and does
not reverse the stated positive alignment. Then

$$
\left|
\mathbb E\langle u_j,g^{\mathrm{NTP}}_{j,k}\rangle
\right|
\leq
\|u_j\|B\rho^{k-1}.
$$

If

$$
\lambda_k\alpha-c>\|u_j\|B\rho^{k-1},
$$

the MTP increment supplies more carrier-aligned local drive than the later
NTP credit.

**Proof.** Apply Cauchy–Schwarz and submultiplicativity to the NTP path, then
subtract the worst registered auxiliary conflict from the direct alignment.
$\square$

This is a formation-credit result, not transport or use.

### Proposition 3: Local standard-head benefit

Let $R_{\mathrm{std}}$ be standard-head carrier risk,
$G_S$ matched shared-aux gradient, $G_I$ informative-MTP gradient, and
$\Delta g_{\mathrm{info}}=G_I-G_S$. Locally,

$$
R_{\mathrm{std}}(\theta-\eta G_I)
-
R_{\mathrm{std}}(\theta-\eta G_S)
$$

$$
=
-\eta\langle\nabla R_{\mathrm{std}},\Delta g_{\mathrm{info}}\rangle
+\frac{\eta^2}{2}
\left(
2G_S^\top H_{\mathrm{std}}\Delta g_{\mathrm{info}}
+
\Delta g_{\mathrm{info}}^\top H_{\mathrm{std}}\Delta g_{\mathrm{info}}
\right)
+O(\eta^3).
$$

A first-order information-specific benefit therefore requires

$$
\langle\nabla R_{\mathrm{std}},\Delta g_{\mathrm{info}}\rangle>0,
$$

and a finite step also requires the benefit to exceed curvature cost.

### Counterexamples

- **Equivalence:** if $h_{t+k-1}=h_t$, the heads are tied, and there are no
  background losses, early MTP and later NTP gradients are identical up to a
  scalar. Learning-rate rescaling makes the trajectories equivalent.
- **Conflict:** for
  $R_{\mathrm{std}}(\theta)=\frac12(\theta-1)^2$ and
  $L_{\mathrm{aux}}(\theta)=\frac12(\theta+1)^2$ at $\theta=0$, the two
  gradients oppose. A sufficiently large auxiliary weight makes MTP worsen
  standard-head risk.
- **Formation without use:** let $s_0=Z$ but
  $s_1=f(s_0,x_1)=0$. An auxiliary head perfectly decodes $Z$ from $s_0$,
  while the standard head is independent of it.
- **Long distance with bypass:** a final local token directly identifies
  $Y$, so early-state removal has no behavioral effect.

The candidate advantage vanishes when the future target contains no new
state information, the local window or bypass suffices, the NTP Jacobian path
is clean and identity-like, the direct gradient targets nuisance or conflicts,
the early state is not transported/used, the baseline is saturated, or both
objectives reach the same Bayes optimum.

### Claim Boundary

These results do not establish Transformer Jacobian contraction, a general
code-versus-language distinction, the mechanism behind any code benchmark,
larger-$K$ benefit, equivalence of readability and use, MoE expert utility, or
an impossibility result from A12 E04.

## 6. Carrier Validation Gate

A carrier is the joint object
`data distribution + learner scale + relay interface + evaluation head`.
Thresholds are intentionally not frozen in this theory draft.

Gates 1–4, 6, and 9 mainly audit the data/generator. Gates 5, 7, and 8 must be
audited jointly with the learner, checkpoint, and standard-head interface.
Passing only the dataset-side gates does not validate the carrier.

| Gate | Computation | Pass | Fail | Insufficient |
| --- | --- | --- | --- | --- |
| local-window insufficiency | $W_w$ collision pairs; local-only and full-evidence oracles | same local window supports different answers; local oracle below mastery; full oracle solves | local window identifies or solves the answer | weak oracle, partial collisions, or unfrozen $w$ |
| early counterfactual necessity | replace $E_0$ with all other variables fixed | answer changes reliably | answer stays fixed or intervention changes nuisances | unmatched intervention or unaudited generator |
| paraphrase invariance | semantics-preserving variants and template audit | answer preserved without template-label leakage | answer changes or surface form leaks label | semantic equivalence unverified |
| multi-evidence necessity | joint, single-view, deletion, and counterfactual oracles | joint solves; every single view is insufficient; necessary-evidence changes matter | one evidence/position/frequency solves | weak oracle or correlational check only |
| relay necessity for standard head | clean/ablate/patch ordinary-$q_1$ loss with self/positive controls | clean model solves; relay break causes failure; matched repair restores | ablation does not affect standard head | no base capability or invalid intervention |
| no answer bypass | generator proof, field enumeration, masked-view oracle, token search | no deterministic path outside intended evidence/relay | label, alias, local clue, or generator rule predicts answer | incomplete path enumeration |
| at least one NTP-capable scale | NTP-only multi-seed final-window learning curves | one scale stably learns without transient-only success | every scale stays at floor or is seed-unstable | inadequate budget, seeds, implementation, or threshold |
| unsaturated matched shared-aux | floor/ceiling distance and checkpoint dynamic range | capable baseline retains preregistered headroom | floor or ceiling removes meaningful contrast | selection and dynamic-range rules unfrozen |
| no fixed-table/elimination shortcut | held-out rule recombination and enumeration of consistent missing-evidence worlds | unseen recombination is required; missing evidence leaves at least two consistent worlds with different answers | lookup or unique-completion elimination solves | incomplete solver or reused train/test pairs |

These are serial validity gates. A `fail` or `insufficient` result blocks an
objective comparison.

Current evidence does not pass them: A11 has a direct branch bypass and
saturated source decoding/shared control; A12 E04 has no NTP-eligible scale and
its row-removal guard is invalidated by bijection completion.

## 7. Exactly One Next Decision

> **Freeze the operational long-horizon/compositional definition and the
> nine carrier-validity tests first. Existing evidence is not sufficient to
> enter an NTP/MTP Protocol.**

The human gate is the
researcher judgment record.
Before approval, do not create an anchor, Protocol, implementation, run, graph
or sync update, commit, or push.

## 8. Source Map

- [0706 MTP recording](../../0706/recordings/mtp.md)
- [0713 research guidance](../../0713/recordings/0713_科研指导_整理稿.md)
- [0713 advisor discussion](../../0713/recordings/0713_导师与学长讨论_整理稿.md)
- [A11 current story](../../../../../../Projects/from-attention-to-search/main/stories/11_informative_future_branch_mechanism/01_informative_future_branch_signal_and_use_boundary.md)
- [A11_01 inclusion law](../../../../../../Projects/from-attention-to-search/main/experiments/A11/11_01_informative_horizon_supervision/A11_01_01_E01_next_k_inclusion_law/summary.md)
- [A11_02 all-position path decomposition](../../../../../../Projects/from-attention-to-search/main/experiments/A11/11_02_hidden_to_parameter_transmission/A11_02_01_E02_all_position_path_decomposition/summary.md)
- [A11_03 K/V causal use](../../../../../../Projects/from-attention-to-search/main/experiments/A11/11_03_cross_position_standard_head_use_boundary/A11_03_02_E01_model_local_kv_causal_use/summary.md)
- [A11_03 source information](../../../../../../Projects/from-attention-to-search/main/experiments/A11/11_03_cross_position_standard_head_use_boundary/A11_03_02_E02_exact_source_kv_information_audit/summary.md)
- [A12 E04 carrier failure](../../../../../../Projects/from-attention-to-search/main/experiments/A12/12_0_short_range_single_vs_two_step_composition/A12_0_E04_balanced_per_sample_dual_map/summary.md)
