# 02 MTP-Only Story: Long-Range Semantics, Capacity, and Curriculum

Status: 2026-07-12 story update draft.  
Scope: next-token prediction (NTP) versus multi-token prediction (MTP) only. MoE and Router are explicitly out of scope.  
Current verdict: theory should compress the chain from workload structure to representation demand, optimization interference, scale effects, and training interventions into a few observable variables that can be falsified quickly.

## 0. Core questions

This line now keeps only four questions:

1. What statistical structure defines the target long-range compositional workload?
2. Why can Next2 put more future information in the current hidden state while hurting main-head NTP?
3. Why can larger models benefit more from MTP, and how should capacity be measured beyond parameter count?
4. Why can an NTP-to-MTP curriculum repair low-capacity failure?

## 1. Role of theory

The theory has five jobs:

1. separate task difficulty, representation formation, objective-induced optimization, and actual downstream use;
2. replace vague words such as long-range semantics, capacity, and conflict with computable variables;
3. state the causal path from an extra future loss to the main autoregressive prediction;
4. generate counterfactual interventions;
5. decide whether to continue, revise the model, or stop.

The framework has four layers:

```text
task structure
-> representation requirement
-> NTP/future-target optimization
-> cross-position use by the main NTP head
```

A richer current hidden state is therefore not sufficient evidence of improved autoregressive performance.

## 2. Workload model

Let necessary evidence be $E=(E_1,\ldots,E_m)$, nuisance and surface form be $D,S$, evidence positions be $P$, query be $Q$, composition tree be $T$, intermediate variables be $Z_v$, and answer be $Y$.

$$
X=\operatorname{Render}(E,D,S,P),
$$

$$
Z_v=g_{o_v}(Z_{\mathrm{left}(v)},Z_{\mathrm{right}(v)}),
\qquad
Y=Z_{\mathrm{root}}.
$$

### Task semantic variable

A task semantic variable is invariant to paraphrase and nuisance changes but changes under task-relevant evidence interventions:

$$
Z(X(E,S),Q)=Z(X(E,S'),Q),
$$

$$
Z(X(E,S),Q)\neq Z(X(E',S),Q).
$$

### Long-range strength

For local window width $w$ at decision position $T$:

$$
L_w
=
\frac{
I(Y;X_{1:T-w}\mid X_{T-w+1:T},Q)
}{
H(Y\mid X_{T-w+1:T},Q)
}.
$$

This measures the fraction of remaining answer uncertainty that can only be resolved by far context. Distance alone is not a long-range definition.

### Compositional necessity

$$
\Sigma_m
=
I(Y;E_{1:m}\mid Q)
-
\max_{A\subsetneq[m]}I(Y;E_A\mid Q).
$$

Minimal operator depth:

$$
d_{\mathcal G}(g)
=
\min\{\operatorname{depth}(T):T\text{ uses }\mathcal G\text{ and }T(E)=Y\}.
$$

The workload coordinates are therefore:

$$
\omega=(D,L_w,\Sigma_m,d_{\mathcal G},\tau),
$$

where $\tau$ is the delay between task-state formation and answer use.

### Concrete generator

Sample two random permutations $r_1,r_2$ on an entity set:

$$
b=r_1(a),\qquad c=r_2(b).
$$

Render two necessary facts among matched distractors and use the target:

```text
<DECIDE> <FORMAT_B> c
```

At $h_T$, the next token depends on a local format variable, while the second future token depends on the far two-hop composition. The generator is constructed so that:

$$
I(c;E_1\mid Q)=I(c;E_2\mid Q)=0,
$$

$$
I(c;E_1,E_2\mid Q)=H(c\mid Q)=\log M.
$$

This is a genuine joint-necessity task rather than a local deterministic chain.

## 3. NTP versus Next2 measurements

Objectives:

$$
L_{\mathrm{NTP}}=L_1,
\qquad
L_{\mathrm{Next2}}=L_1+\lambda L_2.
$$

The final target is main-head answer accuracy after the intervening token:

$$
A_{\mathrm{main}}
=
\Pr[\arg\max q_1(\cdot\mid h_{T+1})=Y_2].
$$

Required mechanism measurements:

### Current-state task formation

$$
R_Z=\min(A_{\mathrm{probe}},C_{\mathrm{patch}}).
$$

### Gradient interference

$$
g_1=\nabla_\theta L_1,
\qquad
g_2=\nabla_\theta L_2,
$$

$$
c_{12}
=
\frac{\langle g_1,g_2\rangle}{\|g_1\|\|g_2\|}.
$$

The exact first-order relative penalty is:

$$
L_1(\theta-\eta(g_1+\lambda g_2))
-
L_1(\theta-\eta g_1)
=
-\eta\lambda\langle g_1,g_2\rangle+O(\eta^2).
$$

### Task-relevant capacity

Let local and compositional target subspaces have ranks $r_1,r_2$ and overlap $o$:

$$
r_{\mathrm{req}}=r_1+r_2-o.
$$

For the joint output Jacobian $J_{\mathrm{joint}}$ and NTK $K=J_{\mathrm{joint}}J_{\mathrm{joint}}^\top$:

$$
r_{\mathrm{NTK}}
=
\frac{(\operatorname{tr}K)^2}{\operatorname{tr}(K^2)}.
$$

After training, use the effective rank of the intervention-response matrix $M_H=[\Delta H_U,\Delta H_Z]$ as realized task representation rank $r_{\mathrm{rep}}$.

Capacity slack:

$$
s_{\mathrm{cap}}=r_{\mathrm{avail}}-r_{\mathrm{req}}.
$$

### Cross-position preservation

$$
\kappa_Z
=
\frac{
\|P_Z^{T+1}J_{T\to T+1}P_Z^T\|_F^2
}{
\operatorname{rank}(P_Z^T)
}.
$$

High current-state decodability with low $\kappa_Z$ predicts no stable main-head gain.

## 4. Why small-model Next2 can be worse

### First-order conflict

When $\langle g_1,g_2\rangle<0$, the future-target update slows or reverses progress on the main NTP objective.

### Reduced-rank competition

Use the linear bottleneck:

$$
x=(u,z),\qquad h=Wx,\qquad \operatorname{rank}(W)\le r,
$$

$$
Y_1=Au,\qquad Y_2=Bz.
$$

For whitened inputs and squared loss, the optimal shared representation selects the top $r$ eigendirections of:

$$
M_\lambda=A^\top A+\lambda B^\top B.
$$

If

$$
r\ge\operatorname{rank}(A)+\operatorname{rank}(B),
$$

both tasks can be represented. If the rank is smaller, sufficiently strong future-target eigenvalues displace NTP directions and increase NTP risk.

### Readout and transition mismatch

Even when $z$ is present in $h_T$, it does not help if it is destroyed or misaligned after the intervening token. The three mechanisms are therefore:

```text
representation competition
+ gradient interference
+ cross-position loss
```

## 5. Why larger models can benefit more

Parameter count is only a proxy. The structural variables are:

1. joint local fitting rank $r_{\mathrm{NTK}}$;
2. realized task rank $r_{\mathrm{rep}}$;
3. safe future-update fraction;
4. cross-position retention $\kappa_Z$;
5. gradient alignment $c_{12}$.

For calibration-set NTP Jacobian $J_1$:

$$
S_{\mathrm{safe}}
=
\frac{\|P_{\ker J_1}g_2\|^2}{\|g_2\|^2}.
$$

Candidate phase diagram:

```text
small capacity:
s_cap < 0, low S_safe, negative c12 -> MTP can be worse

intermediate capacity:
s_cap >= 0, higher S_safe, positive retention -> MTP can help

large capacity/data:
NTP eventually learns the same task state -> MTP advantage can shrink
```

The final convergence regime is an advisor hypothesis to test, not an established result.

## 6. Curriculum mechanism

Let:

$$
L(\theta,t)=L_1(\theta)+\lambda(t)L_2(\theta).
$$

Forward curriculum increases $\lambda(t)$ from 0 to 1. If $\theta^*(\lambda)$ is a smooth local optimum path with nonsingular Hessian:

$$
\frac{d\theta^*}{d\lambda}
=-H_\lambda^{-1}\nabla L_2(\theta^*(\lambda)).
$$

Small increments follow a continuation path instead of abruptly rotating the representation toward a difficult auxiliary target.

Mechanism prediction:

1. NTP first stabilizes local features and the state transition;
2. task-effective rank and safe directions increase;
3. adding $L_2$ later causes less negative gradient area and less NTP-subspace rotation.

The curriculum paper reports that forward curricula help 1.3B/3B models use MTP while retaining self-speculative decoding, whereas reverse curricula can improve main-head quality but largely lose the decoding benefit. The rank-conflict account above is our falsifiable explanation, not a theorem from that paper.

## 7. Falsifiable hypotheses

### H1 Workload validity

$$
L_w\ge0.9,
\qquad
\Sigma_2\ge0.9H(Y\mid Q),
$$

with local and single-evidence controls near chance.

### H2 One-step conflict law

$$
-\eta\lambda\langle g_1,g_2\rangle
$$

predicts the observed one-step NTP difference between joint and NTP-only updates.

### H3 Rank threshold

The MTP-NTP gap changes sign near:

$$
r_{\mathrm{avail}}\approx r_{\mathrm{req}},
$$

and task-effective rank predicts the sign better than parameter count.

### H4 Formation is not use

Higher $R_Z(h_T)$ without higher $\kappa_Z$ does not yield stable $A_{\mathrm{main}}$ gain.

### H5 Forward curriculum repairs low-capacity conflict

Relative to static Next2, forward curriculum reduces early negative gradient area and representation rotation, improving final main-head performance primarily in the low-capacity condition.

### H6 NTP catch-up

With sufficient capacity and training, NTP catches up in task-state recovery and final answer performance. This is parked beyond the first experiment.

## 8. Minimal experiment order

### Phase A: frozen/one-step pretrained-model audit — active priority

Use one small and one larger dense model from the same family. On 256 exact synthetic examples and 128 real two-hop relation-composition examples, compute:

$$
(c_{12},r_{\mathrm{NTK}},S_{\mathrm{safe}},R_Z,\kappa_Z)
$$

and compare their prediction with the observed NTP change after one NTP-only versus one joint update.

No full training is needed.

Decision:

> Can the proposed structural variables predict the actual one-step NTP effect, and does the larger model differ through rank, safe directions, and retention rather than parameter count alone?

Failure stops the training phase and forces a theory revision.

### Phase B: controlled low-rank short training — conditional

Create two explicit bottlenecks:

$$
r_{\mathrm{low}}<r_{\mathrm{req}},
\qquad
r_{\mathrm{high}}>r_{\mathrm{req}}.
$$

Compare only:

```text
NTP
static Next2
forward-curriculum Next2
```

No $K$, bridge-token, loss-weight, or duration sweep.

Target phase diagram:

```text
low rank: NTP > static Next2; curriculum repairs part of the gap
high rank: static Next2 no longer hurts and may reach the task threshold faster
```

### Phase C: minimal real-data return — conditional

Apply the same three objectives to a small pretrained model on a real two-hop subset with held-out paraphrase, evidence-swap, and answer evaluation. Synthetic-only success is not sufficient.

## 9. Meeting brief

Thirty-second script:

> We no longer ask whether MTP is generally better. We test three mechanisms: whether the joint task rank exceeds the model's available rank, whether the future-target gradient conflicts with NTP, and whether the semantic direction formed at the current state survives to the next state used by the main head. Long-range structure is defined by nonlocal information, joint evidence necessity, composition depth, and use delay. The first experiment trains nothing: on matched small and larger pretrained models, we measure gradient inner product, NTK effective rank, and cross-position retention, then validate them with one real update. Only after that do we compare static Next2 with curriculum Next2.

One-slide order:

1. observed scale/curriculum puzzle;
2. three variables: $r_{\mathrm{req}}$, $c_{12}$, $\kappa_Z$;
3. one equation:

   $$
   \Delta L_1^{\mathrm{joint}}-\Delta L_1^{\mathrm{NTP}}
   \approx-\eta\lambda\langle g_1,g_2\rangle;
   $$

4. one pretrained-model audit;
5. one decision: do the variables predict the actual NTP change?

## 10. Claim boundary

Can propose:

- an operational definition of long-range compositional workload;
- a reduced-rank mechanism for small-model MTP interference;
- a continuation-path mechanism for curriculum learning;
- a rapid pretrained-model audit.

Cannot claim:

- universal MTP superiority;
- effective rank alone is model capacity;
- probe decodability equals causal use;
- larger parameter count guarantees MTP gain;
- the curriculum mechanism is already proved;
- synthetic phase diagrams necessarily transfer to natural language.

## 11. Only next decision

Approve or revise Phase A, which jointly measures:

$$
(c_{12},r_{\mathrm{NTK}},S_{\mathrm{safe}},R_Z,\kappa_Z,\Delta L_1^{\mathrm{obs}})
$$

on matched synthetic and real two-hop examples. Do not start full MTP or curriculum training until these variables predict an actual update.
