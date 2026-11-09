# Why frequency-based routing must cross three bridges

The purpose of this round is to determine whether organizing added computation by feature frequency improves answer prediction on inputs containing low-frequency features. It is not to make the feature-frequency curve resemble a theoretical distribution. The account below separates directly computable observations, mathematical identities, and learning hypotheses.

## 1. A membership list does not decompose the expert input

A feature is an indexed atom in the frozen CrossCoder dictionary. Its shared activation is jointly encoded from actual model blocks 2, 4, …, 28. The layer-28 decoder direction maps that same activation back into final-layer coordinates. This round therefore does not use an independent encoder fitted only to the final layer.

Frequency is the proportion of fixed TRAIN answer-prediction positions at which a feature has positive activation. Four frequency bands are defined first. The membership list of each band is then split equally between two experts to form organization T. Organization R randomly rearranges the same feature pool while preserving the exact sizes of all eight groups. Membership determines which scores receive a feature's contribution; it does not remove other components from the input.

Every called expert receives the complete final-layer representation. A token position can contain both low- and high-frequency features. Having one current token identity does not mean that the position contains only one kind of feature. Routing by feature frequency means using this mixed feature profile to decide which additional experts to call. It does not mean looking up a low-frequency token and sending it directly to a low-frequency expert.

## 2. High-frequency amplitude, the mean, and principal directions are different objects

For position \(t\) and feature \(i\), define the positive activation-amplitude proxy as the activation multiplied by the norm of its final-layer decoder vector in original coordinates:

$$
a_i(t)=z_i(t)\lVert d_{i,28}\rVert_2.
$$

Shares formed by summing these amplitudes within frequency bands are nonnegative. They are not an orthogonal energy decomposition. A vector decomposition must retain direction:

$$
v_b(t)=\sum_{i\in B_b}z_i(t)d_{i,28},\qquad
h_t=o+b_{\mathrm{dec}}+\sum_bv_b(t)+v_U(t)+\epsilon_t.
$$

Here, \(h_t\) is the actual layer-28 output before the final RMSNorm. The vector \(o\) is the offset used to restore original coordinates. The decoder bias \(b_{\mathrm{dec}}\) and reconstruction residual \(\epsilon_t\) are retained. Vectors from different bands can cancel. Squared norms contain cross terms, so normalized group norms cannot be called shares of actual information.

The earlier experiment asked which frequency-band vectors add to or cancel along the mean direction. PCA in this round asks which band vectors align with variation around the mean. These two questions can yield different signs without contradiction. Let \(P\) denote a projection fitted only to actual TRAIN representations \(h\) and then frozen. A tilde always denotes subtraction of the corresponding frozen TRAIN mean: the TRAIN mean of \(h\) for the actual representation, and the TRAIN mean of that band's vector for a band component. DEV is not recentered. Its coefficients therefore also contain mean shifts relative to TRAIN; they are not pure covariances recomputed around DEV's own mean:

$$
\beta_b(P)=\frac{\mathbb E\langle P\widetilde v_b,P\widetilde h\rangle}
{\mathbb E\lVert P\widetilde h\rVert_2^2}.
$$

The signed coefficients of the frequency bands, U, and the residual sum to 1. They can be negative and cannot be called mutually exclusive energy shares. PCA variance directions are also different from singular directions of a weight matrix. Neither can directly replace task gradients.

## 3. Reception opportunities are different from learning value

Let \(x_i\) indicate that feature \(i\) is active, and let \(I_e\) indicate that expert \(e\) is called. On exactly the same set of positions, define:

$$
p_i=P(x_i=1),\quad r_{i,e}=P(I_e=1\mid x_i=1),\quad
q_{i,e}=P(x_i=1\mid I_e=1),\quad \lambda_e=P(I_e=1),
$$

$$
p_i r_{i,e}=\lambda_e q_{i,e}.
$$

This is the same joint count conditioned in two ways. Reception \(r\) measures whether an active feature reaches an expert. Actual exposure frequency \(q\) measures how often the feature is active among the inputs received by that expert. With strict top-2 routing, expert loads sum to 2 rather than 1. A forced group-pair call rate of 100% follows directly from the routing rule; it is not evidence of function.

Why must learning still be tested? When the outputs of the two selected residual-branch experts each receive weight \(1/2\), the parameter gradient of an expert under fixed routing is:

$$
\nabla_{\theta_e}\mathcal L
=\mathbb E_t\left[\tfrac12 I_e(t)J_e(t)^\top g_t\right].
$$

Here, \(J_e\) is the Jacobian of the expert output with respect to its parameters, including the common input and output scales. The vector \(g_t\) is the loss gradient with respect to the hidden representation after the residual branch has been added. Occurrence counts account for only part of \(I_e\); inputs, prediction errors, downstream sensitivity, gradient directions, and optimization still affect learning. Improved reception, co-occurrence, and spectral shape therefore cannot replace held-out NLL.

## 4. This round tests one policy increment

All four arms use eight experts, call two per position, and share expert width and training budget. F freely selects two group-pairs. H always calls group-pair 4 and selects one other group-pair. Group-pair 4 is the high-frequency membership list only in T; in R it is a preassigned random counterpart. Each selected expert output receives weight \(1/2\), and the complete input \(h\) is unchanged.

On the same lowest-frequency B1 inputs, let \(L\) denote NLL averaged first within each feature's active positions and then equally across estimable features:

$$
\Delta_T=L(T_H)-L(T_F),\quad
\Delta_R=L(R_H)-L(R_F),\quad I=\Delta_T-\Delta_R.
$$

Both \(\Delta_T\) and \(I\) must be negative to meet the directional requirements that reserving the high-frequency call helps and that its increment exceeds that of reserving a general random group-pair. A negative \(I\) alone could merely mean that T is harmed less. This round does not change the Base model, directly train a common-semantic module, or compare top-1 with top-2 under equal computation.

## 5. Relation to existing methods

The [original CrossCoder account](https://transformer-circuits.pub/2024/crosscoders/index.html) distinguishes shared features with read/write connections across several layers from a single-layer SAE. This round preserves shared \(z\) as its object and uses the existing final-layer decoder for geometry. A shared feature ID is not treated as an independent measurement at every layer.

[Research on SAE scaling and evaluation](https://arxiv.org/abs/2406.04093) separates reconstruction, sparsity, and feature-quality evaluation. Accordingly, this round reports actual-hidden geometry, text support, and task loss together. Sparse activations alone are not treated as a complete discovery of natural concepts.

[Research on feature absorption](https://arxiv.org/abs/2409.14507) describes cases in which semantically related features in a sparse dictionary do not activate in every expected setting. This is one reason to retain counterexamples and missed-activation rates. It does not establish that the current CrossCoder exhibits the same absorption mechanism.

This account explains the frozen design. It introduces no new scientific threshold or experiment. Mechanism interpretation and the priority of subsequent work remain for discussion with the researcher.
