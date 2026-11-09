# Summary: A11_02_01_E01 K=2 Semantic Tangent-Kernel Transmission

Primary anchor: [11_02_01 reachability and background-sign subanchor](../../../../problem_anchors/11_informative_future_branch_mechanism/11_02_hidden_to_parameter_transmission/subanchors/11_02_01_reachability_and_background_sign_anchor.md)
Protocol: [protocol.md](protocol.md)
Detailed record: [detailed.md](detailed.md)

## Result Snapshot

**Verdict:** supported in the controlled reference-folded K=2 decision-only setting.

**What we established:** the K=2 direct semantic signal is locally reachable through the shared Transformer encoder parameters after freezing token embeddings and prediction heads. At the native Jacobian scale \(\alpha=1\), the direct parameter semantic velocity is positive in 5/5 seeds, and adding the shared H1 objective does not reverse it in any seed.

**What the experiment shows:** the reference intervention obeys the proved law: direct transmission scales as \(\alpha^2\), the H1 background term scales as \(\alpha\), and the native net-preservation ratio is reconstructed by kernel cosine and norm ratio. Actual one-step margin movement follows the linear prediction, and early training keeps the semantic-margin ordering \(\alpha=1>0.5>0\).

**What we do next:** move from decision-only transmission to all-position parameter decomposition. The next question is whether the same direct term can be separated from all-position indirect transfer and LM background losses.

## Purpose

A11_10 showed positive hidden-state semantic velocity but did not give a tight Transformer parameter-space certificate. A11_02_01_E01 tests the missing link:

\[
\text{direct semantic output direction } v
\rightarrow
J^\top v
\rightarrow
G_{\theta,total}
\rightarrow
\Delta M_2 .
\]

This is a root-cause audit, not a natural-language or sample-efficiency result.

## Terminology / Definitions

| Term | Plain meaning | Concrete object / computation | Unit or formula | Why it matters | Cannot prove |
| --- | --- | --- | --- | --- | --- |
| Semantic margin | whether each branch state moves toward its correct second-token output row | \(M_2=\frac1m v^\top H_\alpha(\theta)\) | scalar | tracks the K=2 semantic direction | downstream semantic usefulness |
| Parameter semantic velocity | first-order margin change under an SGD parameter update | \(G_{\theta,total}=-\langle\nabla_\theta M_2,\nabla_\theta L\rangle\) | margin per unit learning rate | primary decision metric | long-run convergence |
| Direct term | contribution from predicting \(Y_2=S_Z\) | \(G_{\theta,direct}\) | velocity | MTP-specific parameter signal | total training success |
| Background term | signed contribution from shared \(Y_1=A\) | \(G_{\theta,background}\) | velocity | detects help or cancellation from local loss | all-position background behavior |
| Kernel signal | parameter reachability of the semantic direction | \(v^\top\Theta v/m^2=\|\nabla_\theta M_2\|^2\) | velocity scale | tests whether encoder parameters can absorb the hidden signal | finite-step stability |
| Net-preservation ratio | direct signal retained after adding H1 | \(\rho_{\theta,net}=G_{\theta,total}/G_{\theta,direct}\) | unitless | reversal test | absolute learning speed |
| Kernel cosine | alignment of semantic and H1 directions after the encoder Jacobian | \(\chi_\Theta=\cos(J^\top v,J^\top c)\) | unitless | explains background sign | harm by itself |
| Kernel norm ratio | H1 parameter direction size relative to semantic direction | \(r_\Theta=\|J^\top c\|/\|J^\top v\|\) | unitless | explains background magnitude | long-run interference |
| Jacobian scale | controlled semantic sensitivity of the shared encoder | \(\alpha\in\{0,0.5,1\}\) in \(H_\alpha=\bar H_0+D_\alpha(H^{raw}-H_0^{raw})\) | intervention level | calibrates the theory | natural architecture variation |

## Exact Setup

**Research question:** in \(Y_1=A,\;Y_2=S_Z\), does the K=2 direct semantic signal survive shared-encoder parameterization after removing output-head and embedding lookup explanations?

**Data / model / objective:** four deterministic branches, one-layer causal Transformer, fixed token embeddings, fixed regular-simplex H1/H2 heads, full-batch SGD for 200 steps. Trainable parameters are attention, MLP, LayerNorm, and position parameters only.

**Conditions:** `shared_only_k1`; `direct_only_k2` with \(\alpha=0,0.5,1\); `full_k2` with \(\alpha=0,0.5,1\).

**Held fixed:** data, seeds, embeddings, heads, optimizer, checkpoints, and trainable parameter set.

**Changed variable:** semantic Jacobian scale \(\alpha\) and whether H1/H2 losses are active.

**Seeds / checkpoints:** seeds `971,972,973,974,975`; checkpoints `0,1,2,5,10,20,50,100,200`.

**Run:** remote 4-GPU job `pt-50l5l908`, run name `a11_11_k2_semantic_tangent_kernel_transmission_4gpu_20260710_124514`.

**Known limitation:** this is a reference-folded decision-only intervention. It validates local parameter transmission, not all-position LM training or natural-language MTP benefit.

## Primary Metric

The primary metric is:

\[
G_{\theta,total}
=G_{\theta,direct}+G_{\theta,background}.
\]

It decides this anchor because hidden-state theory is useful for parameter training only if \(J^\top v\) is nonzero and the shared objective does not reverse the direct semantic velocity.

## Result

| Check | Result | Interpretation |
| --- | ---: | --- |
| Calibration seeds | 5/5 pass | the reference intervention and autograd identities are valid |
| Direct native velocity at \(\alpha=1\) | mean \(0.056388\), min \(0.038651\) | shared encoder has resolved semantic reachability |
| Direct half-scale ratio | exactly \(0.25\) in 5/5 seeds | direct term follows \(\alpha^2\) |
| Background half-scale ratio | exactly \(0.50\) in 5/5 seeds | H1 background follows \(\alpha\) |
| Full-K2 native net velocity | mean \(0.059908\), min \(0.045335\) | shared H1 does not reverse net semantic velocity |
| Native \(\rho_{\theta,net}\) | mean \(1.089587\), min \(0.886259\) | background can help or mildly reduce, but remains positive |
| One-step sign match | 20/20 comparisons | finite update follows the predicted direction |
| One-step max relative error | \(0.033786\) | far below protocol threshold \(0.25\) |
| Early margin ordering | 10/10 seed-condition checks | \(\alpha=1>0.5>0\) for direct-only and full K2 |
| Local Y1 guard | 5/5 pass | full K2 does not harm final shared-token learning |

## Key Evidence

The native direct term is positive in every seed:

\[
G_{\theta,direct}(\alpha=1)\in[0.038651,0.081096].
\]

The background term is signed, not automatically harmful:

\[
G_{\theta,background}(\alpha=1)\in[-0.005970,0.014910].
\]

Even with the negative seed, the full-K2 total stays positive:

\[
G_{\theta,total}(\alpha=1)\in[0.045335,0.082070].
\]

The finite-step check passes because actual one-step \(\Delta M_2\) matches \(\eta G_{\theta,total}\) in sign and scale for both `direct_only_k2` and `full_k2` at \(\alpha=0.5,1\).

## Key Figure

### Figure: Tangent-kernel transmission and finite-step dynamics

![Tangent-kernel transmission and finite-step dynamics](figures/a11_11_transmission_and_dynamics.png)

**What this tests:** whether the proved reference law and the finite-step update are visible in the actual controlled Transformer run.

**Metric shown:** parameter semantic velocity, native velocity decomposition, predicted versus actual one-step margin change, and full-K2 semantic margin over training.

**How to read:** the upper-left panel should show direct \(\alpha^2\) scaling and background \(\alpha\) scaling; the upper-right panel shows direct/background/net velocity by seed at \(\alpha=1\); the lower-left panel checks \(\Delta M_2\approx\eta G_{\theta,total}\); the lower-right panel checks whether early training preserves \(\alpha=1>0.5>0\).

**Observed result:** all four panels match the expected pattern. One seed has negative background velocity, but its net velocity remains positive.

**Allowed claim:** in this controlled reference-folded K=2 setting, the direct semantic hidden-state signal is transmitted through shared encoder parameters and predicts one-step semantic margin movement.

**What this does not prove:** all-position training, natural-language sample efficiency, or larger-model behavior.

## Claim Boundary

**Can claim:** A11_02_01_E01 closes the local decision-only parameter-transmission prerequisite for the K=2 mechanism: \(J^\top v\) is nonzero, direct transmission has the predicted \(\alpha^2\) law, H1 background has the predicted \(\alpha\) law, and the native net velocity remains positive.

**Cannot claim:** MTP is better than NTP in natural language; all-position K=2 has the same clean decomposition; K larger is better; negative gradient cosine alone is harmful; local velocity equals sample efficiency.

## Next Decision

Create the next anchor for all-position parameter decomposition. The minimal target is to separate direct decision-prefix semantic velocity from all-position background and indirect-transfer terms under the same K=2 semantic tangent-kernel accounting.
