# Sharing decisions and routing information: mathematical account

2026-10-03. These are conditional-model derivations, not natural-text training outcomes. [中文](sharing_routing_mathematics_cn.md); [empirical report](sharing_routing_report.md). Earlier results on expressivity, statistical pooling and serial dynamics remain in [capacity mathematics](capacity_mathematics.md). This note supplies the decision bridge.

## What determines sharing for the same learning step?

Let w be the current shared parameters, δ a fixed update, L_k a task loss with other computation fixed, and p_k nonnegative task weights. The new source A uses w+δ under both alternatives. Sharing exposes old receivers B to w+δ; separation creates a private copy from the same initial value and keeps old receivers at w. Then

\[
R_{\rm share}-R_{\rm separate}
=\sum_Bp_B[L_B(w+\delta)-L_B(w)].
\]

The source term cancels exactly. No convexity or gradient approximation is required. The displacement, source computation, old-task selection and other state must match. Different candidate updates generally do not preserve equal source learning. Copying cost, architectural changes and future adaptation require their own terms.

For δ=−ηG_A and twice differentiable L_B,

\[
L_B(w-\eta G_A)-L_B(w)
=-\eta\langle G_B,G_A\rangle
+\frac{\eta^2}{2}G_A^\top H_BG_A+o(\eta^2).
\]

G_k denotes the task-conditional gradient and H_B the receiver Hessian. Positive alignment is local. Set w=0, L_A=(w−1)²/2, L_B=(w−0.1)²/2 and η=0.5. Gradient cosine is1, source loss falls0.5→0.125, but receiver loss rises0.005→0.08. The exact quadratic term causes finite harm without contradicting infinitesimal positive alignment.

Optimizer normalization also matters. With Σp_k=1 and G=Σp_kG_k, shared SGD has first-order improvementη||G||². If every private block receives its conditional update−ηG_k, its first-order advantage is

\[
\eta\sum_kp_k\|G_k-G\|^2\ge0.
\]

If private blocks instead receive the gradient of the global weighted objective,−ηp_kG_k, sharing's first-order advantage is

\[
\eta\sum_{k\ne j}p_kp_j\langle G_k,G_j\rangle.
\]

These compare different displacements. Neither proves unconditional resource-matched superiority. AdamW preconditioning, momentum, decay and update frequency must appear in the actual δ. [Full proof and independent audit](/data/250010109/MoE_Router/experiments/20261003_sharing_routing/notes/sharing_math_audit_round1.md).

## Why realized harm can coexist with always sharing

Freeze the update and other computation. Let H be the pre-target state, Y the next token, and D(H,Y) the realized update-minus-no-update loss. A router sees only Z=φ(H), accepting with s(Z)∈{0,1}. For integrable losses,

\[
d(Z)=\mathbb E[D\mid Z],\qquad
\Delta R(s)=\mathbb E[s(Z)D]=\mathbb E[s(Z)d(Z)].
\]

Without extra cost or joint capacity constraints, the optimum accepts for d(Z)<0 and rejects for d(Z)>0. Deployable separation depends on the conditional mean, not realized signs alone. An observable incremental cost c(Z), weighted by λ, changes the threshold to d(Z)+λc(Z)<0. A fixed K-expert bank does not itself prevent eventwise choice; shared activation budgets or hard capacity can couple decisions.

Exact counterexample: identical observable inputs, Y∼Bernoulli(0.6), and a probability update 0.5→0.6. D(1)=−0.18232156 and D(0)=+0.22314355. Forty percent of events are harmed, yet mean D=−0.02013551 and always updating is the best causal action. The target-informed oracle updates only at Y=1 and attains −0.10939293; the extra gap comes from seeing the answer. [Numerical check](evidence/causal_sharing_toy_checks.json). This does not estimate target noise in the actual corpus.

## Lossless router compression and full expert inputs

H is the complete causal layer state. Freeze a finite expert/action bank, with F_e(H) the full prediction under action e. Each expert reads its complete prescribed interface: here the residual matrix reads c and the shared tail retains r, while F_e(H) denotes the complete composite computation. Define

\[
Q_e(H)=\mathbb E[\ell(Y,F_e(H))\mid H],\qquad Z=\phi(H).
\]

For integrable costs and unrestricted policies under each information set,

\[
R_H=\mathbb E\min_eQ_e(H),\qquad
R_Z=\mathbb E\min_e\mathbb E[Q_e(H)\mid Z]\ge R_H.
\]

For a measurable conditional minimizer a_Z(Z),

\[
R_Z-R_H=\mathbb E[Q_{a_Z(Z)}(H)-\min_eQ_e(H)].
\]

The integrand is nonnegative. Equality holds exactly when a Z-measurable selection remains optimal for almost every H. Ties require some optimal selection, not recovery of an arbitrarily prescribed tie-break. A stronger sufficient form is Q_e(H)=u(H)+v_e(Z): discarded information changes only a common offset. This theorem does not compare finite-sample estimation, router cost or joint expert retraining. Compression can help estimation or optimization without improving the unrestricted Bayes risk.

Decision and computation may require different information. Let H=(C,S), with S an equiprobable sign and independent C of mean0/variance1; let Y=SC. Frozen experts E_+=C and E_−=−C attain zero squared loss when a router observes only S. If the entire prediction instead depends only on S, any a(S) has E[(SC−a(S))²]=1+E[a(S)²]≥1. Compressing the decision does not require discarding C from the expert.

Target sufficiency also need not imply routing sufficiency. Let independent uniform C∈{−1,1}, S∈{0,1}, Y=C, E_1=C+S and E_2=C+1−S. Z=C determines the target but gives optimal squared routing risk1/2. Z=S is target-independent yet permits zero risk. Retraining both experts to outputC removes the selection problem: this is explicitly a fixed-bank result. [Proofs and primary sources](/data/250010109/MoE_Router/experiments/20261003_sharing_routing/notes/router_expert_information_round1.md).

## Prediction MSE and action utility

Let estimated conditional costs choose ahat, and let a* minimize the true conditional costs. If maximum action error at each input is at mostε(H),

\[
Q_{\widehat a}(H)-Q_{a^*}(H)\le2\epsilon(H).
\]

Decompose the difference into two estimation errors and one predicted-cost difference; the latter is nonpositive. For m fully covered actions, population conditional-risk MSE also yields the loose bound E[regret]≤2√(m MSE). A smaller bound does not order actual regret, and observed-label sample MSE is not automatically this conditional-risk MSE.

For true costs(0,0.1), prediction(1,1.1) has action-mean MSE1 but selects correctly. Prediction(0.1,0) has MSE0.01 but regret0.1. This applies to every feature family. The realized-label oracle is also distinct: generally E[min_e ℓ_e(H,Y)]≤E[min_e Q_e(H)].

## Why a=Wc may omit decision information

In this probe, c is the complete output-projection input, a=Wc, r the pre-Attention residual, and actiond evaluates the same tail at a+D_dc. Its conditional cost is Q_d(H)=E[ℓ(a+D_dc,r,Y)|H]. When derivatives and conditional expectation may be exchanged, the first-order contrast is

\[
Q_d(H)-Q_b(H)\simeq
\mathbb E[\nabla_a\ell(a,r,Y)\mid H]^\top(D_d-D_b)c.
\]

The gradient expectation uses the data conditional distribution, not model-sampled zero-mean scores. Displacement, baseline state, r and target conditionals jointly determine preference. Output reconstruction does not automatically recover these comparisons.

A fixed linear action D factors as Dc=B(Wc) for every c exactly when ker W⊆ker D, equivalently D=DW†W. Necessity follows from Wv=0⇒Dv=0; sufficiency follows because equal Wc then implies equal Dc. Substituting D_d−D_b gives a condition for recovering the displacement-vector difference, not a necessary condition for recovering its scalar loss contrast or a sufficient condition for full cost ordering.

The new panel therefore compares c, a, x=r+a, and (c,x). It tests their usefulness under specified finite-sample learners; PCA dimension, SAE sparsity or fullcx performance is not an information-sufficiency proof. [Operators and costs](/data/250010109/MoE_Router/experiments/20261003_sharing_routing/notes/decision_information_round2.md).

## Why the same full input can support different responsibilities

For differentiable weighted output o=Σ_e g_e(φ(h))E_e(h), let δ_o=∇_oℓ. With disjoint expert parameters θ_e and router parameters ψ, locally holding the active set fixed,

\[
\nabla_{\theta_e}\ell=g_eJ_{E_e,\theta_e}^{\top}\delta_o,
\qquad
\nabla_\psi\ell=\sum_e(\delta_o^\top E_e(h))\nabla_\psi g_e.
\]

Specialize the existing chain rule to a full softmax-weighted mixture. Let s_e be the logit and g_e=softmax(s)_e, holding h and expert outputs fixed when differentiating logits. Then

\[
\frac{\partial\ell}{\partial s_e}
=g_e\,\delta_o^T\bigl(E_e(h)-o\bigr).
\]

Substitute ∂g_j/∂s_e=g_j(1_{j=e}−g_e) into the chain rule. The router receives a task-gradient signal from an expert output relative to the mixture output; an expert receives weighted output error. Identical input h therefore need not mean identical responsibility. If all E_e(h) currently agree, this task-logit gradient is zero. That does not prove permanent MoE stalling: initialization, assignment, noise or auxiliary objectives can break symmetry. It only shows that present loss gradients do not automatically expose future specialization value. This identity is for the stated differentiable full-softmax mixture, not an unweighted hard top-1 or arbitrary TopK normalization.

Experts improve allocated computations; the router changes allocation weights. Equal input tensors do not imply equal roles. Sparse selection also changes sample exposure. Pure hard argmax supplies no ordinary index gradient, so its training mechanism must be specified. Zero gradient for an uncalled expert does not ensure unchanged parameters under every optimizer. Shared branches may also read full h: shared parameters do not imply domain-invariant activations.

A fixed linear projection and linear score can be folded into one gate. In contrast, selecting 64 SAE atoms does not remove the nonlinear width-30000 encoder and TopK cost. This round counts explicit operators without claiming deployment throughput. The [native computation audit](/data/250010109/MoE_Router/experiments/20261003_sharing_routing/notes/router_expert_information_round1.md) explains the cached full-input residual bridge.

## Why no present routing gain does not rule out useful learning allocation

Selection among frozen experts allocates current computation. Training allocation can also change future expert parameters. An exact counterexample separates these decisions.

Let the full input be a uniform sign \(S\in\{-1,+1\}\), the target be 1, and the two bias-free experts be \(E_e(S)=\theta_e S\), with half squared error and both parameters initially zero. Every action then costs 1/2, so no causal router has an initial advantage over a fixed expert. With strictly balanced updates and a fixed tie rule that always chooses expert 1, its population gradient equals \(\theta_1\); both parameters remain zero indefinitely.

Instead, a prescribed causal rule assigns the two signs to separate experts, each still receiving the complete input. Under conditional-mean gradients, with both groups updated once per round at learning rate \(\eta\),

\[
\theta_\pm(t)=\pm[1-(1-\eta)^t],\qquad
R_t=\tfrac12(1-\eta)^{2t}.
\]

Risk converges to zero for \(0<\eta<2\). Global-mean gradients include group frequency 1/2, requiring \(\eta/2\) in the recurrence. This analytical model uses prescribed routing, a restricted bias-free function class, symmetric initialization and a specific tie rule. A bias lets one expert solve the task, and other algorithms can break the stall. It establishes that **learning allocation can create useful differences absent from the initial expert bank**, not that standard MoE training discovers the allocation. Weak readout still limits the tested bank's current usefulness; this toy does not turn an ineffective selector into a success. [Full recurrence, conditions and independent review](/data/250010109/MoE_Router/experiments/20261003_sharing_routing/notes/learning_allocation_round4.md).

## Which gradient differences can guide learning allocation?

At common initialization w, let g(H,Y) be the per-example gradient, H the complete pre-target state, and Z=φ(H) a fixed finite partition. Define G=E[g], G_Z=E[g|Z], and m(H)=E[g|H], assuming finite second moments, interchange of derivatives and expectations, and sufficient smoothness. In this abstract model each expert still receives full H; this does not mean the measured residual matrix also reads r. Shared parameters update by −ηG; private copies use their conditional gradients −ηG_Z. Then

\[
R_{\rm shared}-R_{\rm private}
=\eta\,\mathbb E\|G_Z-G\|^2+O(\eta^2).
\]

Under equal conditional learning rates and free parameter copies, useful grouping retains observable differences in mean learning demand. This excludes estimation variance, storage and future adaptation; it does not establish unconditional private-expert superiority. If the population coefficient is zero, every group gradient equals G, making all actual updates and risks exactly equal, not merely equal to first order. Private gradients of a global-mean objective carry an additional p_z and give a different comparison.

Conditional expectations also give

\[
\mathbb E\|g-G\|^2
=\mathbb E\|m(H)-G\|^2+\mathbb E\|g-m(H)\|^2,
\]

\[
\mathbb E\|m(H)-G\|^2
=\mathbb E\|G_Z-G\|^2+\mathbb E\|m(H)-G_Z\|^2.
\]

The first identity separates mean gradient variation available from H from remaining target-conditional variation. The second separates retained and discarded mean variation under the partition. With constant H, uniform target Y in ±1, and squared loss at w=0, gradients equal −Y and have variance 1, yet every causal partition has G_Z=0. The same realized gradient histogram permits grouping information if H reveals Y in advance. Post-target gradient conflict alone cannot decide an architecture.

Richer nested causal information retains at least as much exact population conditional-mean variance under these premises. Finite fitting and finite steps do not inherit an unconditional monotonic guarantee. The current finite-action results do not estimate these population gradients. The [full derivation](/data/250010109/MoE_Router/experiments/20261003_sharing_routing/notes/conditional_gradient_allocation_round5.md) and [independent audit](/data/250010109/MoE_Router/experiments/20261003_sharing_routing/notes/conditional_gradient_math_audit.md) preserve optimizer conditions and counterexamples.

The underlying drafts received independent formula, numerical-counterexample and source checks. These are not rendered-math certification or new empirical discoveries. [Audit](/data/250010109/MoE_Router/experiments/20261003_sharing_routing/notes/decision_information_math_audit.md).


## Why predictable differences can still favor sharing

Round six adds finite samples to round five. Fix a finite causal partition Z, known probabilities p_z and positive integer counts n_z. Experts start at the same w and use the same independent gradient samples with the same positive conditional step eta. Sharing uses the p_z-weighted mean of group averages; private copies use individual averages. Evaluate fixed population risk, not the fitting batch. If group risks share the same quadratic curvature Q over every compared displacement, let mu_z be group gradient means, Sigma_z their single-sample covariances and mu=sum p_z mu_z. Then

\[
V=\sum_zp_z\|\mu_z-\mu\|^2,\qquad
V_Q=\sum_zp_z(\mu_z-\mu)^TQ(\mu_z-\mu),
\]

\[
N_Q=\sum_z\frac{p_z(1-p_z)}{n_z}\operatorname{tr}(Q\Sigma_z),\qquad
\mathbb E[R_{\rm shared}-R_{\rm private}]
=\eta V-\tfrac12\eta^2V_Q-\tfrac12\eta^2N_Q.
\]

For positive-semidefinite Q and independent group samples, V, V_Q and N_Q are nonnegative. Mean learning differences supply the opportunity; finite-step curvature and reduced statistical pooling subtract from it. This is not an NTP identity. Unequal group Hessians, correlated data, adaptive optimizers or partitions selected from the fitting samples change the contract. Parameter budgets remain unmatched; a suitably valued resource difference C_private−C_shared must also be subtracted.

For two equiprobable scalar groups with Q=1, mu_±=±d, variance sigma² and n independent observations per group, the difference is eta(1−eta/2)d²−eta²sigma²/(4n). With eta=1, d=1 and sigma=2:

| Samples per group n | Expected population risk, shared minus private | Conditional-model preference |
|---:|---:|---|
| 1 | −0.50 | Sharing |
| 2 | 0 | Equal |
| 4 | +0.25 | Private |

These are analytical half-squared-loss examples. Identical genuine group differences can favor different choices at different sample sizes; richer pre-target information does not guarantee a finite-sample benefit from splitting. Independent enumeration also finds that incorrectly evaluating the fitting batch at n=1 yields +1.5 instead of the true population −0.5. Fully correlated cross-group noise likewise invalidates the independence formula. These establish why conditions matter, not new LM findings.

[Full derivation](/data/250010109/MoE_Router/experiments/20261003_sharing_routing/notes/finite_sample_sharing_round6.md) · [Independent enumeration](evidence/finite_sample_sharing_checks.json). Current empirical work does not estimate these population means, covariances or curvatures and adopts no scientific threshold from them.
