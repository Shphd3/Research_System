# The bridge from common structure to serial benefit

2026-10-03. This explains the [current Anchor](history/20261003_before_routing_refinement/reading/anchor.md); it is not a parallel design. The arguments are conditional derivations, not natural-text training results.

## A more precise question than whether serial is stronger

Let the common residual representation be h(z)=z+C(z), and let \(\mathcal F\) be the permitted expert function family. With C fixed, the parallel private contribution belongs to \(\mathcal F\); the serial contribution belongs to

\[
\mathcal F\circ h=\{E\circ h:E\in\mathcal F\}.
\]

The issue is whether composition with h leaves the permitted family unchanged. Preserving information does not guarantee that an expert with fixed size and depth can absorb h into its own parameters.

For h(z)=Az with invertible A and the full expert family of rank at most r without additional norm or sparsity restrictions, composing E with A preserves rank. Conversely, E=MA^{-1} represents any allowed parallel matrix M. The families are equal. This is the reason for the linear reparameterization result in the [second audit](/data/250010109/MoE_Router/experiments/20261003_common_specialized_capacity/notes/math_capacity_round2.md), not a theorem against every serial architecture.

## A nonlinear distinction with an invertible common map

Take a scalar input x≥0, C(x)=x² and E_b(u)=bu². The common residual h(x)=x+x² is strictly increasing, with derivative 1+2x>0, so it loses no input information on this interval. Parallel gives

\[
f_b^{\rm par}(x)=x+(1+b)x^2,
\]

whereas serial gives

\[
f_b^{\rm ser}(x)=x+x^2+b(x+x^2)^2
=x+(1+b)x^2+2bx^3+bx^4.
\]

For b≠0, the nonzero fourth-degree term cannot be represented by any parallel map x+ax²+cx² on an interval with nonempty interior: polynomial equality there requires equal coefficients. Serial nonlinear composition can therefore produce a function absent from the shallow parallel family even when the common map is invertible.

This also explains why effective depth remains a live rival. Repeated nonlinear composition creates the higher-degree term even for one task without any cross-task sharing. The example uses square nonlinearities, not SwiGLU, and is not a strict separation theorem for the actual fixed-width model. Its role is to locate the empirical question, not transfer polynomial degree claims to another activation.

## Equal representability does not make an update equally useful

Consider a complete scalar linear residual model with identity normalization: \(r=z=x\), \(C_\theta(x)=\theta x\), and \(E_d(u)=a_du\). The two computations are

\[
f_d^{\rm par}(x)=(1+\theta+a_d)x,\qquad
f_d^{\rm ser}(x)=(1+a_d)(1+\theta)x.
\]

For fixed \(\theta\) with \(1+\theta\ne0\), free \(a_d\) makes both families cover exactly the same scalar linear maps. Now hold the experts fixed and update only common parameters, asking whether representational equivalence ensures equal retention.

Take \(x=1\), \(\theta=0\), \(a_A=0\), \(a_B=-2\), and targets \(t_A=0\), \(t_B=-2\) under half squared error. Both architectures initially predict 1 for A and −1 for B; both losses equal 0.5. The common gradient from A equals 1 in each model. A step of size 0.1 gives \(\theta'=-0.1\) and reduces A's loss to 0.405 in both. Old task B differs:

| Architecture with B's expert fixed | Old output | New output | New loss |
|---|---:|---:|---:|
| Parallel | −1 | −1.1 | 0.405 |
| Serial | −1 | −0.9 | 0.605 |

At step size \(\eta\), B's loss changes are \(-\eta+\eta^2/2\) and \(+\eta+\eta^2/2\). For \(0<\eta<1\), the same common update helps the old task in parallel and hurts it in serial. All experts, including A, stay fixed; this step-size range keeps the common map invertible before and after the update.

Function preservation requires \(a_d^{\rm ser}=a_d^{\rm par}/(1+\theta)\), which depends on the common parameter. Fixed experts do not follow that mapping as common parameters change. Equal representational families therefore need not have equal cross-task functional trajectories; the actual \(\theta\) updates in this example are identical. Because source slope \(a_A=0\), its extra through-expert gradient is zero and E2 full/stopped directions would coincide. B differs through its sensitivity to common parameters. This is not a positive example of the E2 gradient-path mechanism. This uses identity normalization, linear experts, squared loss and common-only SGD; it does not predict the signs of SwiGLU/AdamW training. It is a linear-residual version of the [third audit's local counterexample](/data/250010109/MoE_Router/experiments/20261003_common_specialized_capacity/notes/gradient_coupling_round3.md), checked with [exact rational arithmetic](/data/250010109/MoE_Router/experiments/20261003_common_specialized_capacity/analysis/scalar_counterexample.json).

## Where shared knowledge enters the argument

If K tasks need the same h and differ only in b_d, storing h once avoids duplication. In this specific scalar parameterization with C_a(x)=ax² and a treated as an unknown learned coefficient rather than the preceding example's known constant1, shared serial uses 1+K coefficients; independent serial copies use 2K, saving K−1. This comparison requires a common a that serves all targets. It counts coefficients in a specified parameterization; it is not a minimum-storage or incompressibility bound.

It is a representation/storage result for a specified target family. It does not prove that an optimizer finds the common h or that task gradients agree on it. Binding a can be restrictive when tasks require different transforms, and updating a for one task changes every old task's expert input.

The evidence chain consequently has four separate obligations: useful reusable structure exists; the transformed input fits limited experts; training finds and retains a useful transform; and the through-expert gradient path improves a finite update. The present mathematical cases bound the first two, six-arm trajectories and C/trunk rollback examine the third, and the same-forward gradient-path diagnostic examines a bounded instance of the fourth.

An architecture comparison changes representations and the whole training process. A same-forward diagnostic holds the trained model's output fixed and isolates one local update path. Agreement could sharpen the explanation. Disagreement limits extrapolation between measurements and calls for checking state/layer selection, measurement scope, SGD versus AdamW, finite-sample uncertainty and other timescales. Neither substitutes for the other.

Representation, acquisition, retention and resource usefulness remain distinct. A valid link is progress, not proof that the entire chain is complete.


## Sharing can improve estimation without enlarging a function family

A second mechanism differs from storage compression. Let K fixed task means be \(\mu+\delta_d\), with zero mean task offsets and mean squared offset \(V_\delta\). Each task has n independent observations with independent zero-mean noise of variance \(\sigma^2\). Write the task sample mean as \(\bar y_d\), the grand mean as m, and fix the estimator

\[
\widehat\theta_d=m+\alpha(\bar y_d-m),\qquad 0\le\alpha\le1.
\]

Here \(\alpha\) is a prespecified shrinkage amount, not expert width or a serial gate. Averaging task-mean squared estimation error over repeated datasets gives

\[
R(\alpha)=(1-\alpha)^2V_\delta+\frac{\sigma^2}{Kn}
+\alpha^2\frac{\sigma^2}{n}\left(1-\frac1K\right).
\]

Complete sharing \(\alpha=0\) beats independent estimation \(\alpha=1\) exactly when \(V_\delta<\sigma^2(1-1/K)/n\): heterogeneity bias is smaller than the estimation variance saved by pooling. Mean improvement need not help every task. With K=4, n=10, noise variance 1 and mean squared task offset 0.025, mean-estimation MSE is 0.05 for full sharing, 0.10 for independent means and 0.04375 for oracle partial shrinkage. These are algebraic values under stated assumptions, not language-model measurements.

For fixed \(\alpha>0\), the possible prediction vectors still cover \(\mathbb R^K\). Lower error therefore does not establish a larger function family or fewer parameters. Only complete sharing restricts predictions to one common dimension. This benefit does not require serial nonlinear computation. More independent data changes the bias–variance tradeoff, while repeated language tokens cannot automatically count as independent samples. Connecting this stationary equal-n squared-loss pooling model to sequential NTP requires additional representation, curvature and dynamic arguments.

Even a more accurate common estimate need not improve every old task. With its residual fixed, current prediction error e and a common scalar shift \(\Delta\), squared error changes by \(2e\Delta+\Delta^2\). A residual may already compensate for error in the old common estimate. This motivates direct finite old-task evaluation rather than judging common estimation alone. The [fifth audit](/data/250010109/MoE_Router/experiments/20261003_common_specialized_capacity/notes/statistical_pooling_round5.md) gives the full derivation, unknown oracle quantities and degenerate cases.

## What the normalized-direction control compares

The same-forward probe must also distinguish gradients from normalized directions. Let the full gradient be \(g_f=g_d+g_p\) and the stopped gradient be \(g_d\). The displacements are \(-\epsilon g_f/\lVert g_f\rVert\) and \(-\epsilon g_d/\lVert g_d\rVert\). Their difference is not a fixed scaling of \(-\epsilon g_p\), because the direct term is rescaled too. On the source loss that generated \(g_f\), first-order changes are \(-\epsilon\lVert g_f\rVert\) and \(-\epsilon g_f^\top g_d/\lVert g_d\rVert\). Cauchy–Schwarz makes the former no larger than the latter. This ideal differentiable first-order fact does not determine finite BF16 responses or old-domain losses. Zero norms follow the registered degenerate-case rule.

## Functional matching beyond a generally stronger expert

Fix all final-checkpoint weights. Retain true domain d in the input and vary only the expert bank e used at every layer, obtaining the complete four-domain/four-expert loss matrix L. Columns within a domain use identical records. Let D be the mean diagonal, O the mean off-diagonal and G the mean of all16 cells. Define

\[
S=O-D,\qquad
I_{de}=L_{de}-\bar L_{d\cdot}-\bar L_{\cdot e}+G.
\]

For the complete uniformly weighted4×4 design, G=(D+3O)/4 and the mean diagonal of I is D−G, so

\[
S=-\frac43\operatorname{mean}_d I_{dd}.
\]

If L contains only additive domain difficulty a_d and general expert quality b_e, both I and S vanish. Positive S therefore indicates lower-loss assigned matching on average, not that every domain's own expert is best. Preserve the full matrix.

The matching can reflect co-adaptation with the current common/trunk state, order and optimization. It does not uniquely identify intrinsic semantic specialization or maximum capacity. Missing cells or unequal domain/expert weighting invalidate the simple cancellation identity; this round uses the complete balanced matrix.
