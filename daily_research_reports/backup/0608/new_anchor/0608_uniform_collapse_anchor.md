---
parent_node: uniform_feature_moe_specialization
status: draft_for_audit_cycle
created: 2026-06-08
---

# Anchor: Why Uniform Features Still Collapse After Removing Position-Seeded Common Offset

## 0. Thinking Card

**Parent problem:**

Can a standard top-1 MoE router trained by next-token prediction form stable feature-level expert specialization, rather than merely forming route consistency caused by collapse or route/expert co-adaptation?

**Current subproblem:**

In a controlled uniform-feature synthetic setting, after removing the most obvious fixed-position source of common routing bias, the router is initially less collapsed but still collapses during training. We need to identify why stable slot/target-feature-to-expert specialization does not emerge.

**Core hypothesis:**

Uniform feature frequency is not sufficient for feature-level specialization. After position-seeded step-0 common offset is reduced, final collapse can still arise because top-1 routing amplifies early traffic asymmetries and because the task loss does not necessarily provide a feature-aligned utility gradient for the router. Slot/target information may be present in the hidden state, but present information is not the same as utility-aligned routing pressure.

**Minimal test:**

Use a no-position or randomized-position discriminative synthetic setting. First audit whether feature information is linearly available in routed hidden states. Then initialize routing with an explicit one-to-one feature-to-expert map and track route logits, gradients, expert utility, load, and route-feature NMI through training. Compare vanilla, forced feature initialization, frozen oracle feature router, random balanced router, and feature-init with anti-lock-in/inhibition.

**Current boundary:**

Current evidence supports common-offset as a strong explanation for original step-0 dominant expert, but does not explain final collapse by itself. The recent no-position observation suggests that position/common-offset can seed early imbalance, while training-time dynamics can still re-create collapse.

**Next decision:**

Decide whether the remaining collapse is primarily:

1. an implementation or metric artifact;
2. residual common/nuisance signal after position removal;
3. top-1 rich-get-richer lock-in;
4. absence of feature-aligned expert utility;
5. insufficient evidence.

---

## 1. Problem Definition

### Broader question

When does MoE route consistency mean feature-level specialization?

Route consistency alone is not enough. A router may consistently send similar examples to the same expert because of:

- frequency bias;
- common hidden-state offsets;
- random initialization geometry;
- early top-1 lock-in;
- expert utility co-adaptation;
- true feature-specific causal utility.

The broader problem is to distinguish true feature-level specialization from these confounds.

### Sharper question

In the uniform synthetic setting, after reducing fixed-position common offset, why does the router still fail to maintain feature-to-expert specialization?

The key empirical trigger is:

```text
No-position setting: step-0 routing is less/no collapsed, but during training routing still concentrates, often toward a small number of experts.
```

### Decision question

Does the remaining collapse happen because the router cannot see the slot/target feature, because the feature is visible but not useful for reducing loss, or because top-1 routing destabilizes an otherwise valid feature partition?

### Not in scope

This anchor does not yet claim a deployable MoE method for real language models. It also does not address Zipfian feature distributions except as a future stress test after the uniform baseline is understood.

### Operational definitions

**Feature:**

A latent factor `F` that defines an equivalence class of examples expected to require the same expert-relevant computation. In the current synthetic setting, candidate feature definitions include:

- `slot_id`
- `B/context id`
- `target id`
- `(slot_id, B/context id)`
- `(slot_id, target id)`
- `logical rule id`

The experiment must state which one is used.

**Feature-level specialization:**

A route/expert structure is feature-level specialized only if all three conditions hold:

1. route consistency with `F` is high;
2. the matched expert has higher causal utility for that feature than unmatched experts;
3. the specialization is stable under training and not merely a post-hoc consequence of route/expert co-adaptation.

**Collapse:**

A routing state where a small subset of experts receives a disproportionate fraction of routed tokens/features, measured by max load, entropy/Gini, and seed-level route heatmaps. Collapse can be step-0 geometric collapse or training-induced final collapse; these must be separated.

**Common component:**

For feature centroids `h_f`, define:

$$
\begin{aligned}
c &= E_f[h_f] \\
r_f &= h_f - c \\
h_f &= c + r_f
\end{aligned}
$$

`c` is feature-independent hidden-state structure. It can come from position, template tokens, layernorm/residual mean, attention aggregation, or other nuisance factors.

**Utility-aligned feature:**

A feature `F` is utility-aligned if assigning examples with that feature to a particular expert produces lower loss or higher accuracy than assigning them to other experts, measured by a feature-by-expert utility matrix.

---

## 2. Physical Priors

### P1. Slot/target features may be real but not automatically routing-relevant

A logical slot or target factor can contain unique information. However, the router uses the hidden state and receives gradients only through task loss and routing losses. Therefore:

`feature present in h` is not equivalent to `feature used by router`, and neither is equivalent to `feature causally useful for expert specialization`.

This prior is weakened if feature information is not decodable from hidden states, or if an oracle feature router gives no improvement over random/balanced routing.

### P2. Uniform frequency removes one bias but not all routing biases

Uniform feature counts remove frequency imbalance, but do not imply hidden states are zero-mean, isotropic, or feature-dominated. A linear router can still see:

- common hidden component;
- position/template signal;
- target-label difficulty;
- finite random initialization asymmetry;
- batch stochasticity;
- expert utility differences produced during training.

This prior is weakened if step-0 routing matches random baselines and remains balanced across seeds without special controls.

### P3. Top-1 routing has a rich-get-richer instability

With hard top-1 routing, an early winner receives more traffic, more expert updates, and stronger router feedback. This can create a self-reinforcing loop even when step-0 routing is not severely imbalanced.

This prior is weakened if early load does not predict later load, gradients do not concentrate on winning experts, and soft/anti-lock-in controls do not change final collapse.

### P4. Stable feature specialization requires either utility pressure or an inductive bias

If all experts are symmetric and the task can be solved by shared computation, the loss may not prefer the intended feature partition. A feature-to-expert map may need one of:

- capacity/interference pressure;
- feature-aligned initialization;
- feature-aware regularization;
- inhibition / anti-lock-in;
- oracle or supervised routing signal.

This prior is weakened if vanilla random routing reliably discovers the same feature partition across seeds.

---

## 3. Mechanistic Motivation

The previous mechanism explained original step-0 imbalance as common-offset seeded routing:

$$
z_{f,e} = w_e^T h_f = w_e^T c + w_e^T r_f
$$

where `w_e^T c` is feature-independent but expert-specific. This makes one expert attractive across many features before training.

The no-position observation changes the mechanism boundary. If step-0 is no longer collapsed, then position-seeded common offset is probably a major early source in the original baseline. However, collapse during training means there is another mechanism after step 0.

The current candidate mechanism is:

1. Step-0 common offset is reduced.
2. Early assignments still fluctuate because of finite random geometry, stochastic batches, or small feature margins.
3. Top-1 routing gives early winners more traffic and expert updates.
4. Experts become useful for the traffic they receive.
5. Router gradients reinforce these assignments.
6. Route and expert utility co-adapt.
7. Final routing concentrates even when initial routing was balanced.

This mechanism predicts that a forced feature-to-expert initialization may not survive unless the feature partition is either causally useful or protected by an anti-lock-in/inhibition mechanism.

---

## 4. Mathematical Model
### Objects

Let:

- `F`: intended feature key, e.g. slot, target, or `(slot, target)`;
- `N`: nuisance/context variable, e.g. `B`, template, position, or batch context;
- `Y`: target token or class;
- `h(x,t)`: hidden state at the routed logical token;
- `E`: set of experts;
- `w_e`: router row for expert `e`;
- `r(x)`: selected expert, $\arg\max_e w_e^T h(x,t)$;
- `L_e(x)`: loss if `x` is routed to expert `e`;
- `U(e,F)`: causal utility of expert `e` for feature `F`.

### Hidden decomposition

For each feature:

$$
h_f = E[h(x,t) | F=f]
$$

Decompose:

$$
\begin{aligned}
h_f &= c + u_f \\
c &= E_f[h_f] \\
u_f &= h_f - c
\end{aligned}
$$

A more complete decomposition allows nuisance terms:

$$
h(x,t) = c + u_F + v_N + \epsilon
$$

where:

- `c` is common across features;
- `u_F` is feature-specific information;
- `v_N` is nuisance information such as position/template/context;
- `epsilon` is within-feature noise.

### Router logits

For a linear bias-free router:

$$
\begin{aligned}
z_e(x) &= w_e^T h(x,t) \\
       &= w_e^T c + w_e^T u_F + w_e^T v_N + w_e^T \epsilon
\end{aligned}
$$

Define:

$$
\begin{aligned}
a_e &= w_e^T c \\
q_{F,e} &= w_e^T u_F \\
n_{N,e} &= w_e^T v_N
\end{aligned}
$$

Feature-level routing requires the feature term `q_{F,e}` to dominate the common and nuisance terms in the routing decision, or for the training objective to amplify `q_{F,e}` rather than `a_e` or `n_{N,e}`.

### Utility matrix

Define a feature-by-expert utility matrix:

$$
U(e,f) = - E[\ell(x; expert=e) | F=f]
$$

or relative utility:

$$
\Delta U(e,f) = E[\ell(x; baseline) - \ell(x; expert=e) | F=f]
$$

True feature specialization requires more than high NMI between route and feature. It requires:

$$
r(f) \approx \arg\max_e U(e,f)
$$

and the utility matrix should show stable feature-dependent structure rather than one or two experts being broadly useful for all features.

### Falsifier

The core hypothesis is weakened if:

1. no-position/random-position hidden states still contain a large common or nuisance component that fully predicts final routing;
2. feature information is not decodable from hidden states;
3. an oracle feature router gives no accuracy/loss or interference benefit;
4. forced feature-to-expert initialization collapses immediately even when frozen/oracle controls show no benefit;
5. training dynamics do not show any rich-get-richer or co-adaptation pattern.

---

## 5. Computational Realization

### 5.1 Workflow Interface

Input construction:

1. Sample feature `F` uniformly.
2. Sample nuisance/context `N` under a controlled distribution.
3. Construct the sequence with no fixed absolute-position shortcut, or with randomized logical slot position.
4. Route at the logical slot token, not at a fixed absolute index.
5. Predict target `Y` from the intended synthetic rule.

Model:

- Transformer or minimal sequence model with top-1 MoE router;
- fixed `num_experts`;
- router bias disabled unless explicitly tested;
- position embedding removed or randomized according to protocol.

Output observations:

- hidden feature separability;
- common/nuisance ratio;
- route-feature alignment;
- load distribution;
- expert utility matrix;
- logit and gradient decomposition over time.

### 5.2 Minimal computational tests

#### Test A: no-position/random-position collapse audit

Question:

After reducing fixed-position common offset, does collapse still emerge from training dynamics?

Use the multi-B discriminative setting, but ensure position is not fixed.

Primary metrics:

- `step0 max_load`;
- `final max_load`;
- load entropy;
- accuracy;
- route-feature NMI for the declared feature key;
- `common_ratio`;
- linear-probe feature accuracy;
- winner persistence.

#### Test B: feature availability vs router usage

Question:

Is slot/target feature information available in `h`, and does the router use it?

Metrics:

- linear probe for feature `F` from `h`;
- linear probe for target `Y` from `h`;
- `NMI(route, F)`;
- logit decomposition: common vs feature vs nuisance;
- router gradient projection onto feature directions `u_F`.

#### Test C: forced feature-to-expert initialization

Question:

If we start from the desired feature-to-expert map, does vanilla training preserve it, destroy it, or improve it?

Use the simplest one-B discriminative setting first, with randomized logical slot position.

Variants:

- vanilla random router;
- random balanced router;
- feature-to-expert initialized router, trainable;
- feature-to-expert initialized router, frozen/oracle;
- feature-to-expert initialized router + inhibition / anti-lock-in.

Metrics:

- initial and final route heatmap;
- feature assignment survival rate;
- time-to-first route flip;
- time-to-NMI-drop;
- assigned-expert logit margin;
- per-feature expert utility matrix;
- gradient projection along assigned feature directions;
- accuracy/loss.

---

## 6. Minimal Falsifiable Test

### Primary decisive experiment

Run forced feature-to-expert initialization in the no-position/random-position one-B discriminative setting.

### Required comparisons

- `V0`: vanilla random top-1 router;
- `V1`: random balanced init, trainable router;
- `V2`: feature-to-expert init, trainable router;
- `V3`: oracle/frozen feature router;
- `V4`: feature-to-expert init + inhibition or anti-lock-in.

### Decisive readout

For each seed, plot and save:

- route heatmap at step 0, early checkpoints, and final;
- `max_load` trajectory;
- route-feature NMI trajectory;
- accuracy/loss trajectory;
- logit decomposition trajectory;
- router gradient decomposition trajectory;
- expert utility matrix trajectory.

### Interpretation

**Supported: training lock-in / missing utility alignment** if:

- step-0 is balanced or feature-aligned;
- feature information is decodable from hidden states;
- vanilla or trainable feature-init collapses during training;
- frozen oracle feature router remains feature-aligned;
- utility matrix is not naturally feature-diagonal, or becomes diagonal only after forced routing;
- anti-lock-in/inhibition preserves feature assignment better than vanilla.

**Weakened: representation failure** if:

- feature information is not decodable from hidden states;
- forced/oracle router does not help;
- logit/gradient decomposition shows no stable feature signal.

**Redirected: residual nuisance/common cause** if:

- no-position/random-position still has a large common or nuisance component;
- common/nuisance logits still predict route concentration;
- removing the new nuisance source fixes both step-0 and final collapse.

---

## 7. Falsifiable Outcomes

### Outcome 1: Feature information exists, but vanilla router ignores or loses it

Evidence:

- linear probe decodes `F` from `h`;
- feature-init router starts with high `NMI(route,F)`;
- trainable feature-init loses NMI and load collapses;
- frozen oracle preserves NMI;
- anti-lock-in improves survival.

Interpretation:

The failure is not that the slot/target feature is absent. The failure is that vanilla top-1 routing lacks stable feature-aligned optimization pressure.

Boundary:

This does not yet prove a deployable method; it just identifies the failure mode.

### Outcome 2: Feature information is not available to the router

Evidence:

- linear probe cannot decode `F` from `h`;
- feature residual ratio is small;
- forced feature routing has weak or unstable margins;
- oracle feature router gives little benefit.

Interpretation:

The immediate bottleneck is representation, not gating. The model must expose the intended feature in the routed hidden state before router design can solve it.

### Outcome 3: Feature routing is stable only under frozen/oracle routing

Evidence:

- frozen oracle works;
- trainable feature-init drifts or collapses;
- utility co-adapts with traffic.

Interpretation:

The feature partition is viable, but top-1 training destabilizes it. This motivates anti-lock-in or feature-aware router objectives.

### Outcome 4: Feature routing is stable under trainable feature initialization

Evidence:

- feature-init trainable router preserves high `NMI(route,F)`;
- load remains balanced;
- accuracy remains high;
- utility matrix becomes feature-diagonal.

Interpretation:

Feature-to-expert specialization is possible in the uniform setting with the right initialization. Previous collapse was likely due to initial geometry and training path dependence.

Boundary:

This still does not prove vanilla random top-1 routing will discover the partition.

### Outcome 5: Inhibition preserves feature routing

Evidence:

- feature-init + inhibition preserves route-feature alignment better than feature-init alone;
- accuracy is not harmed;
- utility matrix shows feature-dependent benefit.

Interpretation:

Inhibition is a candidate stabilization mechanism.

Boundary:

If inhibition only balances load without utility diagonalization, it is not evidence for feature-level specialization.

---

## 8. Current Evidence

The current evidence from the previous audit supports:

1. No first-order data/init/router implementation bug was found in the original uniform baseline.
2. Original step-0 imbalance is strongly explained by hidden common component `c` inducing effective expert bias $w_e^T c$.
3. Logit-level common-offset cancellation improves early routing geometry and reduces hard collapse, but final max-load can remain high.
4. Common-aware initialization can fix step-0 bias, but final training outcomes are mixed.
5. Load-balance warmup is currently the strongest final-load control, but load balance is not feature specialization.
6. Post-training route-utility match can be high, so final routing should be interpreted as route/expert co-adaptation, not simply wrong routing.

The most recent no-position observation adds:

Removing position embedding appears to reduce or remove step-0 collapse, but collapse still appears during training, less severely, toward a small subset of experts.

Safe interpretation:

Position/common-offset is likely an early seed in the original setup. It is not a complete explanation for final collapse.

---

## 9. Claim Boundary And Next Decision

### Can claim now

- Uniform feature frequency does not guarantee feature-level routing.
- In the original uniform baseline, common-offset $w_e^T c$ is a strong mechanism-level explanation for step-0 dominant expert.
- The no-position observation suggests final collapse can emerge even when the original step-0 position-seeded bias is reduced.
- The next scientific bottleneck is to separate feature availability, feature utility, and top-1 training lock-in.

### Cannot claim yet

- Position embedding is the only cause of collapse.
- Common-offset fully explains final collapse.
- The current router has proven inability to use feature information before feature availability and utility are audited.
- Load balancing or inhibition already solves feature-level specialization.
- Uniform-setting results transfer to Zipfian features, full language modeling, or real representations.

### Next decision

Run the audit and forced-init trajectory experiments to decide:

Is the desired feature-to-expert partition visible, useful, and trainably stable?

Only after this decision should the project move from root-cause audit to method design.
