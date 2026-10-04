# Mathematical analysis: natural continuations, native displacement and shared-update consequences

**The computational chain closes, but its parts answer different questions.** Natural text and the current model determine gradients. A source gradient determines another text's native displacement. The loss gradient and displacement determine local help or harm. SAE coordinates do not automatically replace that displacement. Natural-text measurements are in the [report](research_report.md).

[中文](mathematical_analysis_cn.md) · [Candidate Anchor](history/20261002_before_capacity_refinement/reading/anchor.md)

## 1. Define all objects in the same chain

Freeze one S7 checkpoint and change only the final attention output matrix \(W\). An event contains visible prefix \(x\) and actual next token \(y\).

| Object | Definition | Question answered |
| --- | --- | --- |
| \(c_x\in\mathbb R^{2048}\) | Input to the output projection | How does the prefix enter the shared matrix? |
| \(a_x=Wc_x\in\mathbb R^{1024}\) | Native attention output before residual addition | What does the SAE observe? |
| \(r_x\) | Pre-addition residual | What other context reaches the downstream map? |
| \(z_x=g(a_x,r_x)\) | Full-vocabulary logits | How does the output affect prediction? |
| \(p_x=\operatorname{softmax}(z_x)\) | Model probabilities | What does the model currently predict? |
| \(q_x=P_{\rm data}(Y\mid X=x)\) | Unknown natural continuation distribution | What can follow this prefix in the population? |
| \(\ell_{x,y}=-\log p_x(y)\) | Pure NTP loss, in nats | How much probability did the realized continuation receive? |

The distribution \(q_x\) is neither model-generated probability nor identifiable from a single continuation. We do not assume S7 satisfies \(p_x=q_x\). Every use of that equality below is an explicit theoretical condition.

## 2. How source learning moves another text's representation

Let \(J_x=\partial z_x/\partial a_x\), and let \(u_y\) be the true-target one-hot vector. The chain rule gives

\[
e_{x,y}=J_x^\top(p_x-u_y),\qquad
G_{x,y}=\nabla_W\ell_{x,y}=e_{x,y}c_x^\top.
\]

For two events,

\[
K_{ij}=\langle G_i,G_j\rangle_F=(c_i^\top c_j)(e_i^\top e_j).
\]

Input similarity supplies only one factor. The other depends on realized continuation, current prediction and downstream computation. Coactivation cannot determine its sign.

Average all valid source targets equally: \(M_A=N_A^{-1}\sum_{i\in A}G_i\). This is the mean of outer products, not the outer product of means. Under the ordinary SGD-form diagnostic change \(\Delta W_A=-\eta M_A\),

\[
\Delta a_{Aj}=\Delta W_Ac_j=-\eta M_Ac_j.
\]

This displacement is exact. The selected matrix does not change its own input or the pre-addition residual. Only positionwise MLP, normalization and vocabulary projection follow it, so native tail replay computes the finite matrix intervention. No SAE reconstruction replaces the forward pass. This diagnostic is not a replay of S7's AdamW training step or its SAE-augmented training objective.

Write \(v_{Aj}=-M_Ac_j\). Actual finite response is

\[
I_{Aj}(\eta)=\ell_j(a_j+\eta v_{Aj},r_j)-\ell_j(a_j,r_j).
\]

Positive is adverse, negative is helpful. A local expansion yields

\[
I_{Aj}(\eta)=\eta h_{Aj}+\frac{\eta^2}{2}v_{Aj}^\top H_{a,j}v_{Aj}+o(\eta^2),
\qquad h_{Aj}=e_j^\top v_{Aj}=-\langle G_j,M_A\rangle_F.
\]

The true-target Hessian is \(H_{a,j}\). Replacing actual \(I\) by \(\eta h\) requires a qualified local step and controlled remainder. An inner product between the same two population means is symmetric; directional finite responses can differ through curvature and source/readout sampling. Measure both directions without calling that inner product asymmetric.

## 3. Why the realized target strongly affects the sign

Treat the source update as an externally fixed intervention. If source sampling is also random, require the continuation to be independent of that sampling conditional on the prefix. Merely not directly using a readout label does not prove this independence. For a fixed prefix define

\[
t_A(x)=J_xM_Ac_x.
\]

Then the first-order loss response is

\[
h_A(x,y)=t_A(x)_y-p_x^\top t_A(x).
\]

Identical prefixes and SAE activations can therefore have opposite signs for different realized next tokens. A natural-language prior supplies conditional probabilities, not a requirement that every realized target have the same effect.

Taking expectation and variance under natural continuation gives

\[
\mathbb E[h_A\mid x,M_A]=t_A(x)^\top(q_x-p_x),
\]

\[
\operatorname{Var}(h_A\mid x,M_A)=t_A(x)^\top[\operatorname{Diag}(q_x)-q_xq_x^\top]t_A(x).
\]

Thus the mean depends on model/data mismatch, while realized targets introduce additional variation. An adverse single event does not by itself establish competing stable task demands. One continuation per prefix cannot identify these conditional moments.

If random sources and readout continuations remain dependent, replace \(q_x\) by \(P(Y\mid x,M_A)\). A calibrated binary logistic example shows why: with \(p=1/2\) and gradient \(G=p-y\), using the same event as source and readout gives \(M=G\) and \(h=-G^2=-1/4\), not zero. This is self-fitting an observed target, not evidence of generalizable mean demand. Separate source validation avoids mistaking that self-effect for generalization.

A minimal example has two equally likely targets and an already correct model distribution \((1/2, 1/2)\). A change that raises the first probability helps the first realized target and harms the second. It does not establish that two Experts are warranted: the outcome is unknown before prediction.

## 4. What Fisher connects, and what it does not

The model Fisher at the output is

\[
F_a(x)=J_x^\top[\operatorname{Diag}(p_x)-p_xp_x^\top]J_x.
\]

For a fixed direction \(v\),

\[
D_{\rm KL}(p_a\Vert p_{a+\eta v})=\frac{\eta^2}{2}v^\top F_a(x)v+o(\eta^2).
\]

This sensitivity relation needs no calibration assumption. Only under the additional condition \(p_x=q_x\) does the first-order conditional mean vanish and

\[
\operatorname{Var}(h_A\mid x,M_A)=v_A(x)^\top F_a(x)v_A(x).
\]

A direction can be sensitive and have large individual effects while having zero mean demand for change. Sensitivity has no help/conflict sign.

For any fixed finite change to model probabilities \(p_x'\),

\[
\mathbb E_{Y\sim q_x}[I_A\mid x,M_A]=D_{\rm KL}(q_x\Vert p_x')-D_{\rm KL}(q_x\Vert p_x).
\]

At \(q_x=p_x\), this is the nonnegative \(D_{\rm KL}(p_x\Vert p_x')\). This is a calibrated counterexample, not a claim that S7 is calibrated. An update from a sampled target can perturb an already appropriate distribution without establishing semantic conflict between domains.

Without calibration, the true-target gradient second moment is

\[
\mathbb E_{q_x}[ee^\top\mid x]
=J_x^\top\{\operatorname{Diag}(q_x)-q_xq_x^\top+(p_x-q_x)(p_x-q_x)^\top\}J_x.
\]

It generally differs from the model Fisher. So does the actual loss Hessian:

\[
H_{a,x,y}=F_a(x)+\sum_k(p_{x,k}-u_{y,k})\nabla_a^2z_{x,k}.
\]

At \(p=q\), target expectation removes the second term. Unverified calibration does not permit deleting it for current data. The distinction is consistent with the [empirical Fisher analysis](https://arxiv.org/abs/1905.12558).

## 5. Why second-order overlap is not a separation criterion

Vectorize \(W\) by columns into \(w\). Let a source estimate \(\widehat g_A\) have mean \(\mu_A\) and covariance \(\Sigma_A/m\). Let target population loss \(L_B\) have gradient \(\mu_B\) and Hessian \(H_B\). The quantity \(m\) counts the assumed independent sampling units; correlated tokens in one document cannot automatically be counted as independent units.

With an integrable controlled remainder and permission to exchange expectation and expansion,

\[
\mathbb E\{L_B(w-\eta\widehat g_A)-L_B(w)\}
=-\eta\mu_B^\top\mu_A
+\frac{\eta^2}{2}\left[\mu_A^\top H_B\mu_A+\frac1m\operatorname{tr}(H_B\Sigma_A)\right]+o(\eta^2).
\]

This separates mean direction, curvature and source sampling noise. Under additional calibration of both populations and independent-event sampling, \(\mu_A=\mu_B=0\), \(H_B=F_{W,B}\), and \(\Sigma_A=F_{W,A}\). The second-order cost is

\[
\frac{\eta^2}{2m}\operatorname{tr}(F_{W,B}F_{W,A})\ge0.
\]

In our input/output coordinates,

\[
\operatorname{tr}(F_{W,B}F_{W,A})
=\mathbb E_{x\sim A,\,x'\sim B}\left[(c_x^\top c_{x'})^2\operatorname{tr}\{F_a(x)F_a(x')\}\right].
\]

Input overlap and output-sensitivity overlap can therefore produce a second-order perturbation cost without first-order mean conflict. The calibration and sampling conditions are substantive, not measured natural mechanisms here.

This still does not imply separation helps. Consider identical local quadratic tasks at the same optimum with independent zero-mean gradient noise. A shared update averaging two batches of size \(m\) has covariance \(\Sigma/(2m)\); private parameters using \(m\) each have \(\Sigma/m\). Sharing reduces the noise consequence for each prediction. This is not yet a parameter-budget-matched experiment, but it refutes the sufficiency of “large Fisher overlap implies separation benefit.” That benefit requires a direct fair comparison.

### Why can parameter angle and response correlation differ?

For fixed readout events, write \(g_j=\operatorname{vec}(G_j)\), with mean \(\bar g\) and empirical covariance

\[
C_R=\frac1n\sum_j(g_j-\bar g)(g_j-\bar g)^\top.
\]

For source matrices \(U,V\), write \(u=\operatorname{vec}(U)\), \(v=\operatorname{vec}(V)\). Their first-order responses are \(-g_j^\top u\), \(-g_j^\top v\). Expanding the centered products gives

\[
\operatorname{Cov}_R(h_U,h_V)=u^\top C_Rv,\qquad
\operatorname{Corr}_R(h_U,h_V)=\frac{u^\top C_Rv}{\sqrt{(u^\top C_Ru)(v^\top C_Rv)}}.
\]

With nonzero denominators this is an exact finite-panel identity requiring no sampling-independence assumption. Low Euclidean matrix cosine can coexist with correlated responses because the readout covariance emphasizes some directions and ignores others. \(C_R\) is the centered empirical covariance of true-target gradients, not model Fisher. It need not be materialized: response vectors compute the same quantity. The identity is exact for derivatives only; actual finite correlation is measured separately. High correlation does not guarantee matching signs for every event.

## 6. SAE: static reconstruction, coordinate changes and native displacement

Freeze decoder \(D\), bias \(b\) and encoder. For native states \(a_0,a_1\), let actual codes be \(\alpha_0,\alpha_1\) and residuals \(\varepsilon_t=a_t-b-D\alpha_t\). Exactly,

\[
\Delta a=D\Delta\alpha+\Delta\varepsilon.
\]

Replacing native displacement by decoded coefficient differences requires a separate test of \(\Delta\varepsilon\). Small static residual does not guarantee it.

If the positive TopK support stays fixed at \(S\), with selected encoder rows \(E_S\), then within that coding region

\[
D\Delta\alpha=D_SE_S\Delta a,\qquad
\Delta\varepsilon=(I-D_SE_S)\Delta a.
\]

The map has rank at most K and is generally not an orthogonal projection. Accurate static states do not require that map to approximate the identity on update directions. A displacement outside the encoded local directions can have dynamic residual ratio near one.

At a support boundary, equal positive scores can belong to different decoder directions. Swapping them can make the reconstruction jump although the native state is continuous; the residual compensates. This coding jump is not an equally large model mechanism change.

A complete counterexample uses the three-dimensional identity decoder and Top2 positive scores, with \(a(t)=(A, 1+t, 1-t)\), \(0<\epsilon<1\) and \(A>1+\epsilon\). Static relative squared error becomes arbitrarily small as \(A\) grows. From \(t=-\epsilon\) to \(+\epsilon\), the last two atoms swap and

\[
\frac{\|\Delta a-D\Delta\alpha\|^2}{\|\Delta a\|^2}=\frac{(1-\epsilon)^2}{4\epsilon^2}.
\]

The dynamic ratio grows as the true movement shrinks. This proves absence of an automatic guarantee; natural data still require measurement. Today's audit retains all 30000 sparse endpoint coordinates and reports changed/stable support separately.

## 7. Fixed subspaces and finite effects without double counting

Orthonormalize selected decoder directions into \(Q\), and let \(P=QQ^\top\). This defines a native output subspace, not independent energies of nonorthogonal atoms. For \(u=\Delta a\), \(u_P=Pu\), \(u_R=(I-P)u\),

\[
e^\top u=e^\top u_P+e^\top u_R.
\]

First-order contributions add exactly; finite effects generally interact. Compute all three:

\[
I=L(a+u)-L(a),\quad I_P=L(a+u_P)-L(a),\quad I_R=L(a+u_R)-L(a).
\]

The removal comparison \(I-I_R\) need not equal \(I_P\). An explicitly symmetric two-part allocation is

\[
\phi_P=\tfrac12[I_P+(I-I_R)],\qquad
\phi_R=\tfrac12[I_R+(I-I_P)],\qquad
\phi_P+\phi_R=I.
\]

It averages adding a component first and last. It is a bookkeeping rule for specified interventions, not unique atom causation, isolated semantic function or separation utility. The matrices \(P\Delta W\) and \((I-P)\Delta W\) act identically across readout texts, giving a shared-parameter implementation rather than arbitrary per-example edits.

Another exact relation follows the native displacement path:

\[
I=\int_0^1\nabla_aL(a+tu)^\top u\,dt.
\]

One can split \(u_P,u_R\) along that fixed path, but the removal intervention takes a different path. Do not equate the attributions. [Integrated Gradients](https://proceedings.mlr.press/v70/sundararajan17a.html) supplies the path-attribution background; today's two-part allocation is calculated directly from the three native interventions above.

## 8. What would show additional representation information?

Let \(B\) be the pre-target baseline, \(Z\) the pre-update representation/code and \(H\) the scalar response for one fixed source; apply the identity separately to the four sources. Assume \(\mathbb E[H^2]<\infty\). For optimal squared-error predictors,

\[
R^*(B)-R^*(B,Z)=\mathbb E\left[\{\mathbb E(H\mid B,Z)-\mathbb E(H\mid B)\}^2\right]\ge0.
\]

Finite-sample ridge predictors are not Bayes predictors; negative measured Q does not prove no information. An SAE is a deterministic transformation of the native representation, so it cannot contain more information than the full native state. It may expose information more usefully to a particular readout or human description.

The actual target is allowed in an independent composition analysis but is unavailable before prediction. Its gain is not prospective Router performance. Residual error mixes unobserved target variation, readout limitations, sample size and source uncertainty; it is not automatically irreducible natural uncertainty.

The bounded outcome is a coherent procedure: seek repeatable response relations in pre-update representations; validate them with native displacement and actual loss; use SAE coordinates while retaining residuals and native controls. Long-term separation value remains a separate fair comparison.

## 9. Does source transfer also identify differences between sources?

Continuation, 2026-10-02. The following statements are algebraic. They do not assume an idealized generative model of natural text.

For one readout event, let \(H_A,H_B\) be the true responses to two fixed sources and \(P_A,P_B\) the predictions fitted for those sources. A response can be a derivative or an actual finite loss difference; one equation must use consistent labels and units. Define the mean, half difference, and corresponding predictions:

\[
H_+=\frac{H_A+H_B}{2},\quad H_-=\frac{H_B-H_A}{2},\qquad
P_+=\frac{P_A+P_B}{2},\quad P_-=\frac{P_B-P_A}{2}.
\]

Expectations below average over the same event distribution or empirical weights while fixing sources and predictors; they do not resample sources. Average prediction error within source and across sources obeys

\[
\frac{\mathbb E[(H_A-P_A)^2]+\mathbb E[(H_B-P_B)^2]}{2}
=\mathbb E[(H_+-P_+)^2]+\mathbb E[(H_--P_-)^2],
\]

\[
\frac{\mathbb E[(H_B-P_A)^2]+\mathbb E[(H_A-P_B)^2]}{2}
=\mathbb E[(H_+-P_+)^2]+\mathbb E[(H_-+P_-)^2].
\]

Subtracting gives the exact identity

\[
R_{\rm cross}-R_{\rm own}
=4\mathbb E[H_-P_-]
=\mathbb E[(H_B-H_A)(P_B-P_A)].
\]

These identities follow event by event. They require neither normality, calibration, statistical independence nor optimal prediction. Applying them separately to the lexical baseline and augmented model partitions their prediction-error improvement into mean and difference components. This accounting is not causal attribution to a semantic mechanism.

For a possibility example, take \(H_A=Z+\xi_A\) and \(H_B=Z+\xi_B\), with independent zero-mean variables of variances 1, 9 and 9. The baseline is constant and has no information about any of these variables; the augmented predictor observes \(Z\). Both optimal augmented predictors equal \(Z\), reducing own-source and cross-source error from 10 to 9. Yet \(H_B-H_A=\xi_B-\xi_A\) remains unpredictable from \(Z\). This mathematical example separates transferable gain from information about source differences; it is not an asserted S7 data-generating process.

With fixed features, preprocessing and regularization, this ridge predictor is linear in its training labels. A/B have equal size and partition the previous F-half0 source, so their average source matrix, derivative and prediction recover the earlier full-source quantities. Recovery checks implementation; it is not new independent evidence. For finite responses, \((I_A+I_B)/2\) is an arithmetic average of two interventions and generally differs from the finite response to the average matrix. The prediction-error identities still hold.

For a predictor trained on A and frozen on B, another exact decomposition is

\[
\mathbb E[(H_B-P_A)^2]
=\mathbb E[(H_A-P_A)^2]+\mathbb E[(H_B-H_A)^2]
+2\mathbb E[(H_A-P_A)(H_B-H_A)].
\]

The change in response can correlate with the old prediction error. An error increase is therefore not wholly attributable to failure of representation transfer. For any prediction \(P\) and response \(H\), with matched averaging weights,

\[
\operatorname{MSE}(P,H)
=(\mu_P-\mu_H)^2+(\sigma_P-\sigma_H)^2
+2\sigma_P\sigma_H(1-\rho_{P,H}).
\]

Variances use the population denominator. If either standard deviation is zero, covariance is zero and correlation is undefined. This describes offset, scale and association errors; it does not identify a representation's information deficit.

The current affine diagnostic fits \(H_B\approx\alpha+\beta H_A\) on F and applies the same map to every predictor. It uses the new source's F labels, so it is not raw transfer. Nor is it optimal calibration of each predictor. See the [source-transfer continuation](source_transfer_addendum.md) for the measurements and their boundaries.

## 10. Three distinct objects: domain averages, source replication and target-conditional means

### 10.1 Two different averages

A/B in §9 are two source samples **within each source domain**. Their average retains that domain's complete mean effect, including differences from other domains. It is not the four-domain common response. The earlier99.02% error accounting cannot show that between-domain differences disappear.

Index the response as \(H_{s,id}\), with source half \(s\in\{A,B\}\), source domain \(d\in\{1,2,3,4\}\), and recipient event \(i\). Use either \(\eta h\) or actual finite loss difference \(I\) consistently. Define

\[
g_{s,i}=\frac14\sum_dH_{s,id},\qquad
V_{s,id}=H_{s,id}-g_{s,i}.
\]

Here \(g_s\) is the current four-domain mean response and \(V_s\) its domain deviations. A domain contrast is \(H_{s,id}-H_{s,ie}=V_{s,id}-V_{s,ie}\). Fitting A responses and freezing the predictor on B's corresponding deviations tests between-domain readout under a replacement source sample. Six pairwise contrasts have only three linear degrees of freedom, not six independent replications.

### 10.2 Exact accounting versus an assumption-dependent interpretation

With fixed event weights \(w_i\ge0\), \(\sum_iw_i=1\), define \(\langle U,V\rangle=\frac14\sum_{i,d}w_iU_{id}V_{id}\). Direct expansion yields

\[
\frac{\|H_A\|^2+\|H_B\|^2}{2}
=\sum_iw_i g_{A,i}g_{B,i}
+\langle V_A,V_B\rangle
+\frac12\|H_A-H_B\|^2.
\]

The terms are cross-half inner products for the mean response and domain deviations, followed by source-half disagreement. This first supplies algebraic accounting for two fixed sources. The first two terms can be negative and must not be clipped into nonnegative population signal shares.

Only under additional assumptions—independent source samples with matched distribution, size and composition, fixed recipients, and \(H_s=\Theta+\varepsilon_s\) with zero-mean uncorrelated errors—do expected cross-half products recover population response energies and the final term estimate average single-source sampling-error energy. A/B here partition a fixed F-half0 pool and are dependent conditional on that finite pool. Population interpretation requires further sampling and document-dependence assumptions.

For finite responses, \(\Theta=\mathbb E_{\rm source}[I(\widehat M)]\), generally not \(I(\mathbb E_{\rm source}\widehat M)\). The nonlinear tail cannot pass through expectation.

Separate overall source strength from event variation by defining \(m_{s,d}=\sum_iw_iV_{s,id}\) and \(\widetilde V_{s,id}=V_{s,id}-m_{s,d}\). Then

\[
\langle V_A,V_B\rangle
=\frac14\sum_dm_{A,d}m_{B,d}
+\langle\widetilde V_A,\widetilde V_B\rangle.
\]

Thus repeatable overall source strength and repeatable variation with recipient text are distinct. Subtracting R means is descriptive here; it does not refit predictors on R.

### 10.3 Parameter geometry differs from recipient-response geometry

For first-order responses, define \(\Delta M_{s,d}=M_{s,d}-\frac14\sum_eM_{s,e}\), \(u_{s,d}=\operatorname{vec}(\Delta M_{s,d})\), and \(g_i^{W}=\operatorname{vec}(G_i)\). Then

\[
V_{s,id}=-\eta\langle G_i,\Delta M_{s,d}\rangle_F,
\qquad
\langle V_A,V_B\rangle
=\frac{\eta^2}{4}\sum_d u_{A,d}^\top K_R u_{B,d},
\quad K_R=\sum_iw_i g_i^{W}(g_i^{W})^\top.
\]

The formal September30 work used Euclidean parameter inner products, corresponding to identity weighting. Recipient responses use \(K_R\) weighting. Removing each source's R-response mean replaces this second moment by true-target gradient covariance. Weak Euclidean parameter replication therefore does not automatically imply unstable effects on all recipient texts. Nor is \(K_R\) automatically the model Fisher.

### 10.4 What the shared realized target contributes

Using \(t_{s,d}(x)=J_xM_{s,d}c_x\) from §3, let \(\tau_s=t_{s,d}-t_{s,e}\). The unit-step contrast is

\[
C_s(x,y)=\tau_s(x)_y-p_x^\top\tau_s(x).
\]

For fixed prefix and sources, averaging under the unknown natural continuation distribution gives

\[
\mathbb E_q[C_s\mid x]=\tau_s^\top(q_x-p_x),
\]

\[
\mathbb E_q[C_A C_B\mid x]
=\{\tau_A^\top(q_x-p_x)\}\{\tau_B^\top(q_x-p_x)\}
+\tau_A^\top[\operatorname{diag}(q_x)-q_xq_x^\top]\tau_B.
\]

The first term concerns prefix-conditional means; the second retains variation from the same realized target. Even under theoretical calibration \(q_x=p_x\), the first vanishes while the second can remain positive. Repeatability at a shared realized target is not advance predictability from the prefix. Domain centering does not automatically remove this target term.

We therefore distinguish response replication at realized targets, cross-half prediction without target features, and a target-informed composition diagnostic. The third is not prospective Router performance, the first does not establish stable mean harm, and the second alone does not establish long-term isolation utility.

### 10.5 What changes when events are averaged into a record?

Averaging a record's T true responses and predictions before computing squared error evaluates its mean effect. It differs from averaging squared event errors. With finite second moments,

\[
\operatorname{Var}\left(\frac1T\sum_tH_t\right)
=\frac1{T^2}\sum_{t,t'}\operatorname{Cov}(H_t,H_{t'}).
\]

The familiar \(1/T\) reduction needs additional independent, equal-variance conditions. Adjacent natural-text targets are dependent. Better performance of fixed predictors at record scale shows sensitivity to the evaluation object; it does not identify \(q_x\) or establish complete noise removal. See the [domain-response analysis](domain_response_structure.md) for new measurements.


The information horizon also matters. This16-event record mean aggregates16 sequential prefix predictions; later prefixes contain earlier realized targets. It is not a single forecast made at record start or position126. A separate strict-prefix check uses features no later than126 to forecast eight targets143…255. [Domain analysis§5](domain_response_structure.md) keeps these objects separate and does not interpret their numerical difference as a causal amount of denoising or leakage.

### 10.6 Amplitude along a common parameter axis

For nonzero \(\bar M_s=\frac14\sum_d M_{s,d}\), set \(\alpha_{s,d}=\langle M_{s,d},\bar M_s\rangle_F/\|\bar M_s\|_F^2\). Then \(\frac14\sum_d\alpha_{s,d}=1\), and \(M^\perp_{s,d}=M_{s,d}-\alpha_{s,d}\bar M_s\) is orthogonal to the common axis and averages to zero over domains. First-order responses \(H_{s,d}=\eta h_{s,d}\) satisfy

\[
Z_{s,d}=H_{s,d}-\alpha_{s,d}\bar H_s=-\eta\langle G,M^\perp_{s,d}\rangle_F.
\]

This is a linear transform defined by known sources. For A→B scoring, truth and all model predictions use the same evaluation-source \(\alpha_B\). R fits no coefficients, but the scoring operator changes with the evaluation source. This is neither a new finite intervention nor an unchanged transfer of every A-defined transform. Each half's common axis can differ, and parameter Euclidean orthogonality does not imply response orthogonality under \(K_R\). A retained cross-half inner-product ratio describes this transformation, not a unique shared-mechanism explanation fraction.

## 11. Seeing the entire current output need not reveal the update's input

This differs from §6's failure of SAE code differences to reconstruct a displacement. First suppose the native output \(a\) is observed perfectly, without SAE compression. If the input dimension of \(W\) exceeds its rank, some nonzero input directions are annihilated by the current matrix.

Let \(P_R\) project orthogonally onto the row space of \(W\) and \(P_N=I-P_R\) onto its kernel. For a column input,

\[
c=c_R+c_N,\qquad c_R=P_Rc,\quad c_N=P_Nc,
\qquad Wc_N=0,\quad a=Wc_R.
\]

The source matrix \(M\) can nevertheless induce

\[
\Delta a=-\eta Mc_R-\eta Mc_N,
\qquad h=h_R+h_N,
\quad h_R=-e^\top Mc_R,\quad h_N=-e^\top Mc_N.
\]

The current output does not directly retain \(c_N\), but the update matrix need not annihilate it. For an algebraic non-identification example, hold residual \(r\), target \(y\) and current output \(a\) fixed while replacing the input by \(c+u\), with \(Wu=0\). The downstream gradient \(e\) is unchanged, yet

\[
h(c+u)-h(c)=-e^\top Mu
\]

can be nonzero. Such a kernel direction exists for this fixed event if and only if \(P_NM^\top e\ne0\); a nonempty kernel alone does not guarantee a response change. Thus no function of \((a,r,y)\) alone identifies all such source responses in general. This example permits these input variations; it does not show that the actual data manifold contains matched pairs of this kind, or that \(c_N\) is statistically unpredictable from \(a\) on the actual distribution.

An SAE is a function of \(a\), so deterministic coding cannot generally supply the missing variable. This does not prevent an SAE from describing an output displacement: \(\Delta a\) still lies in output space, and distributional correlations may permit partial readout. Information in the current representation, the action of a source matrix and dynamic SAE fidelity are separate questions.

Orthogonal \(c_R,c_N\) do not imply orthogonal scalar responses \(h_R,h_N\). Correct energy accounting is

\[
\mathbb E[h^2]=\mathbb E[h_R^2]+\mathbb E[h_N^2]+2\mathbb E[h_Rh_N].
\]

The same holds for domain-centered responses. A/B repeatability additionally contains row–row, null–null, row–null and null–row terms. Individual squared or RMS ratios are not explained fractions. The present local diagnostic measures derivative channels only; it does not establish finite-intervention utility or an identified cause of readout failure.
