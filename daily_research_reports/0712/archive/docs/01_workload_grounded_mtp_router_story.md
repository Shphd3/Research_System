# 01 Workload-Grounded MTP and Router Research Story

Status: daily research draft for 2026-07-12.  
Role: convert the 0710 advisor dialogue into one workload-first, falsifiable research route.  
Current verdict: do not add MTP horizon, bridge-token, loss-weight, or Router sweeps before validating a real workload model.

## 0. Executive conclusion

The research object is not “prove multi-token prediction is better than next-token prediction” or “design a better Router.” Both are methods.

The provisional workload is:

> **Distributed-evidence compositional decision making**: several necessary pieces of evidence are dispersed in a long context; no single piece determines the answer; the model must bind the evidence correctly, compose it through an operator-labeled structure, and preserve the resulting task state until the answer position.

The fixed research chain is:

$$
\text{real benchmark task}
\rightarrow
\text{minimal capability}
\rightarrow
\text{task generative model}
\rightarrow
\text{necessary representation property}
\rightarrow
\text{mechanism metric}
\rightarrow
\text{causal NTP/MTP comparison}
\rightarrow
\text{conditional MoE/Router design}
\rightarrow
\text{real-task validation}.
$$

Only one experiment is currently approved: a paired synthetic-real audit that asks whether the same representation mechanism explains both a controlled task and a real multi-document compositional QA task.

---

## 1. Five urgent questions

### Q1. What workload are we solving?

Define

$$
\mathcal W=(C,Q,T,Y),
$$

where $C$ contains necessary evidence $E_{1:m}$ and distractors $D$, $Q$ is a query, $T$ is an operator-labeled composition tree, and

$$
Y=g_T(E_1,\ldots,E_m;Q).
$$

A valid instance must satisfy:

1. local insufficiency;
2. joint necessity;
3. nontrivial composition;
4. nuisance invariance;
5. independently controllable evidence distance, composition depth, and decision-reveal latency.

This excludes single-needle retrieval and purely local deterministic chains.

### Q2. What capabilities does the workload require?

The model must:

1. retain distributed evidence;
2. bind entities, attributes, and conditions correctly;
3. form intermediate composition variables;
4. suppress irrelevant context;
5. transmit the task state to the answer position.

The target is not “more information” but:

$$
\boxed{\text{the right task information, with the right structure, used at the right position}.}
$$

### Q3. What representation properties are necessary?

Let $H$ be the decision-state representation.

Task-relevant sufficiency:

$$
I(Y;E_{1:m}\mid H,Q)\approx 0.
$$

Factor recoverability:

$$
I(H;E_i\mid Q)>0
$$

for necessary factors, guarded by causal patching because probe decodability alone does not prove use.

For every internal tree node $v$,

$$
Z_v=g_v(Z_{\mathrm{left}(v)},Z_{\mathrm{right}(v)}),
$$

the audit should test whether $Z_v$ emerges at the expected layer and position.

Task-relevant nuisance invariance requires:

$$
d(\Pi_{\mathrm{task}}H(E,D),\Pi_{\mathrm{task}}H(E,D'))
\ll
d(\Pi_{\mathrm{task}}H(E,D),\Pi_{\mathrm{task}}H(E',D)).
$$

### Q4. Why may MTP help or hurt?

For

$$
L_K=\sum_{j=1}^{K}\lambda_j
\operatorname{CE}(q_j(\cdot\mid H_t),Y_{t+j}),
$$

only future horizons carrying new task information provide direct task signal. Define

$$
\mathcal I_K=
\{j\le K:
I(Z;Y_{t+j}\mid Y_{t+1:t+j-1},H_t)>0
\}.
$$

The real net update is:

$$
\Delta M_{\mathrm{task}}
=
\eta G_{\mathrm{direct}}
+\eta G_{\mathrm{transfer}}
-\eta G_{\mathrm{conflict}}
-O(\eta^2B).
$$

Therefore, extra information in $H_t$ does not imply downstream gain. Capacity competition, readout misalignment, cross-position destruction, and irrelevant future targets can eliminate the benefit.

### Q5. What bottleneck could justify MoE and a Router?

Let $o$ denote a composition operator and

$$
g_o=\mathbb E[\nabla_\theta L\mid o].
$$

A sparse expert decomposition is justified only if operator-conditioned gradients show stable interference:

$$
\langle g_o,g_{o'}\rangle<0.
$$

The Router target should then approximate the required computation or conditional expert advantage:

$$
r(H_t)\approx
\text{required computation type or best expert advantage},
$$

not merely token frequency or surface semantics.

Required evidence includes route-operator alignment, measurable selected-expert advantage, causal expert swap/ablation effects, and gains not explained by load balance.

---

## 2. Theory route

### Layer 1: workload generative model

$$
C=\operatorname{Serialize}(E,D),\qquad
Y=g_{T_Q}(E),\qquad
Y\perp D\mid E,Q,T_Q.
$$

This layer defines what must be retained and computed.

### Layer 2: task-relevant representation necessity

Define

$$
E\sim E'
\iff
g_{T_Q}(E)=g_{T_Q}(E')
\quad
\forall Q\in\operatorname{supp}(Q).
$$

Let $[E]$ be the task-relevant evidence equivalence class. For a query family that separates these classes and prediction error at most $\epsilon$, a Fano-style candidate bound is

$$
I(H;[E])
\ge
H([E])-h(\epsilon)
-\epsilon\log(|\mathcal E/{\sim}|-1).
$$

The required representation is the task-relevant evidence class, not the raw context.

Open proof work:

1. finite-query separability;
2. random-query rather than all-query bounds;
3. the need for a query family when a single answer is many-to-one in the evidence.

### Layer 3: hierarchical intermediate-state formation

For each internal node,

$$
Z_v=g_v(Z_{\mathrm{left}(v)},Z_{\mathrm{right}(v)}).
$$

The current claim is diagnostic, not yet a theorem: evidence variables should emerge before lower-level intermediate variables, which should emerge before the root answer variable. Operator-label perturbation should destroy the corresponding hierarchy.

### Layer 4: task-relevant MTP optimization

Map the existing A11 informative-horizon theory to $[E]$ or $Z_v$. If future horizon $j$ encodes $Z_v$, define centered readout direction $a_{j,z}$. In the local fixed-head model,

$$
G_K=
\frac{1}{|\mathcal Z|^2}
\sum_z
\left\|
\sum_{j\in\mathcal I_K}a_{j,z}
\right\|^2.
$$

The missing bridge is whether this velocity lies in the real task-sufficient subspace, survives to the answer position, and reduces real task hitting time.

### Layer 5: capacity-conflict-catch-up scale model

A candidate scale law is

$$
\mathcal A(C,N)
=
S_{\mathrm{direct}}(C,N)
-
I_{\mathrm{conflict}}(C,N)
-
R_{\mathrm{NTP\ catchup}}(C,N).
$$

This yields the advisor's possible phase diagram:

- small capacity: MTP can be worse;
- intermediate capacity: direct supervision can dominate;
- large capacity/data: NTP catches up and the gap shrinks.

No scale sweep belongs to the current protocol.

### Layer 6: conditional MoE/Router theory

For operator probabilities $p_o$,

$$
\left\|\sum_o p_og_o\right\|^2
=
\sum_o p_o^2\|g_o\|^2
+
2\sum_{o<o'}p_op_{o'}\langle g_o,g_{o'}\rangle.
$$

If cross terms are stably negative, routing operators to disjoint expert parameters can remove those interference terms. A new Router is justified only after three prerequisites pass:

$$
\boxed{
\text{stable operator-conditioned conflict}
+
\text{identifiable computation state}
+
\text{conditional expert advantage}.
}
$$

---

## 3. Research order

### Current anchor: A11_22 workload-mechanism paired audit

Compare only:

1. NTP;
2. informative MTP (`MTP-info`);
3. MTP with task-informative future targets masked at the decision position (`MTP-mask`).

Use one primary small pretrained model, matched data, matched backbone update count, and a paired synthetic-real task.

### Only after A11_22 passes

1. capacity phase-diagram anchor;
2. MoE necessity anchor for operator-conditioned interference;
3. Router method anchor only after conditional expert advantage is established.

Do not currently run:

- larger-$K$ sweeps;
- bridge-token, loss-weight, or duration sweeps;
- synthetic-only downstream claims;
- probe-only mechanism claims;
- load-balance-only specialization claims.

---

## 4. Minimal paired experiment

### Benchmark anchor

Use the multi-document compositional QA workload. Train on the annotated reasoning-path data from 2WikiMultiHopQA and evaluate in the LongBench multi-document QA format. LongBench v2 is a later external transfer test and is not used for training or tuning.

### Synthetic side

Construct an operator-labeled evidence graph or shallow tree with:

- two necessary evidence branches;
- one final composition operator;
- matched distractor passages;
- separately controlled evidence distance $L$, composition depth $d$, and decision-reveal latency $\tau$;
- shortcut guards for single evidence, local window, and lexical cues.

### Real side

Use held-out 2WikiMultiHopQA examples with:

- complete support paths;
- topic-matched distractors;
- one-support, support-deletion, support-order, and evidence-swap controls;
- no training or tuning on LongBench v2 test examples.

### Core measurements

Task score:

$$
Q_{\mathrm{comp}}
=
\min
\left(
A_{\mathrm{full}},
C_{\mathrm{evidence\ swap}},
1-\operatorname{ExcessAcc}_{\mathrm{one\ support}}
\right).
$$

Representation measurements:

- evidence and intermediate-variable probes;
- causal hidden-state patching;
- distractor invariance;
- preservation from decision state to answer state.

Optimization alignment:

$$
\Gamma_{\mathrm{task}}
=
\left\langle
-\nabla_\theta L_{\mathrm{extra}},
-\nabla_\theta L_{\mathrm{heldout\ task}}
\right\rangle.
$$

For $x\in\{\mathrm{syn},\mathrm{real}\}$,

$$
\Delta Q^x
=
Q_{\mathrm{comp}}^x(\mathrm{MTP\mbox{-}info})
-
\max
\left[
Q_{\mathrm{comp}}^x(\mathrm{NTP}),
Q_{\mathrm{comp}}^x(\mathrm{MTP\mbox{-}mask})
\right].
$$

Primary paired transfer score:

$$
T_{\mathrm{pair}}
=
\min(\Delta Q^{\mathrm{syn}},\Delta Q^{\mathrm{real}}).
$$

Support requires:

1. $T_{\mathrm{pair}}>0$ with a positive paired confidence lower bound;
2. improved representation and causal-use metrics on both sides;
3. representation improvement preceding or accompanying task improvement;
4. no reproduction of the gain by `MTP-mask`;
5. no local language-modeling difference sufficient to explain the result.

Synthetic-only gain means the model does not transfer.  
Real-task gain without mechanism gain means the representation account is incomplete.  
No gain means revise the workload or informative-target definition before designing a Router.

---

## 5. Claim boundary

Can propose:

- distributed-evidence compositional decision making as a falsifiable long-context workload;
- the existing A11 theory as a local tool for informative future supervision;
- a paired synthetic-real audit for construct validity.

Cannot claim:

- universal MTP superiority;
- all long-context tasks require tree composition;
- probe decodability equals causal use;
- the workload already requires MoE;
- load balance or route clustering proves functional experts;
- small-model structured-supervision gains transfer to large-scale pure pretraining.

## 6. Only next decision

Accept, revise, or reject this workload statement:

> The minimal difficult long-context unit is retaining multiple necessary pieces of evidence under distractors, binding them correctly, composing them into an intermediate task state, and preserving that state until the answer position.

If accepted, execute the paired A11_22 protocol. If rejected, revise the workload model before any MTP or Router method work.
