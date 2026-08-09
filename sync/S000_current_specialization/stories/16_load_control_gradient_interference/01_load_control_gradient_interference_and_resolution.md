# Load Control, Gradient Interference, And Resolution

## 0. Definitions

- **Hard expert load:** the fraction of top-1 assignments received by each expert; the busiest-expert share is its maximum.
- **Switch load-balancing objective:** the differentiable auxiliary objective $L_{LB}=E\sum_e f_e\bar p_e$, combining detached hard fractions $f_e$ and mean soft Router probabilities $\bar p_e$.
- **Gradient conflict:** opposite directions between the language-model (LM) and LB raw gradients on Gate or Router-upstream parameters, measured over the complete global batch.
- **Dynamic expert bias:** a non-gradient controller that adjusts expert-specific routing biases from observed hard load; it is a candidate intervention, not established evidence.

## 1. Abstract

A15 matched training exposed a load-control failure that is independent of covariance-band utility: every relevant arm used the same Switch coefficient $\lambda_{LB}=0.01$, yet Vanilla-Full collapsed in deep layers while Centered-Full remained broadly used. A migrated frozen counterfactual establishes that the true token-shared Router-input component immediately sustains current Vanilla collapse, but adding that component to an independently adapted Centered Router is not sufficient beyond random shifts. The unresolved A16 question is therefore whether the differentiable LB update pays a held-out LM cost while improving hard load, or whether it is beneficial regularization or simply ineffective against hard top-1 saturation. A16_00 uses held-out shadow-step NLL as the decision metric and global-batch raw-gradient cosine as the mechanism metric. Dynamic expert bias is the researcher-selected first intervention only after this audit identifies harmful interference or hard/soft control mismatch.

## 2. Research Question

Can an MoE maintain operational expert load without slowing language-model learning or preventing useful expert differentiation? The current local decision is narrower: from an identical early AdamW state and identical global batch, does adding the Switch LB gradient improve hard load but worsen one-step held-out NLL through opposing Router gradients?

## 3. Why The Previous Framing Was Insufficient

Equal LB coefficients do not imply equal hard routing. A large auxiliary value does not imply strong corrective force, a negative gradient cosine does not imply held-out harm, and a balanced Router does not imply useful specialization. These objects must be separated before selecting a repair.

## 4. Empirical Layout

The source system is the verified four-layer, hidden-768, eight-sparse-expert, top-1 DCLM MoE. A15 provides matched Vanilla-Full and Centered-Full training histories. The migrated A16_00_01 frozen audit uses immutable statistics and validation text. A16_00 will use two registered early states, the complete accumulated global batch, exact copies of parameters, AdamW moments, scheduler, RNG, Router buffers, and independent held-out probe documents.

## 5. Physical Intuition

A token-shared input component becomes an expert-specific constant logit offset after the linear Gate. It can coherently enlarge one expert's margin across many tokens. The Switch objective reacts through soft probabilities, whereas deployment uses hard top-1 winners. When margins saturate, the auxiliary penalty can remain large while its ability to change winners becomes stage- and layer-dependent. The central uncertainty is whether its remaining gradient is merely ineffective, beneficially regularizing, or actively opposing LM progress.

## 6. Decision Metrics

The primary metric is

$$
\Delta NLL_{LB,t}=NLL_{probe}(T_{AdamW}(s_t,g_{LM}+g_{LB}))-NLL_{probe}(T_{AdamW}(s_t,g_{LM})).
$$

It is measured in nat/token. Positive values mean that adding LB from the same optimizer state makes the next prediction step worse on independent text. It establishes an immediate quality cost, not a long-run training effect.

The mechanism metric is

$$
c_t=\frac{\langle g_{LM},g_{LB}\rangle}{\lVert g_{LM}\rVert\lVert g_{LB}\rVert+\epsilon}.
$$

Negative $c_t$ means the two objectives locally oppose each other in a registered parameter group. It cannot by itself show harm. Hard-load benefit is measured by the paired change in busiest-expert share; negative change means better balance.

## 7. Minimal Mechanistic Model

The one-step update is not the raw gradient alone. AdamW transforms $g_{LM}+g_{LB}$ using stored first and second moments, weight decay, learning rate, and scheduler state. A16 therefore compares complete shadow states rather than treating cosine as a surrogate for performance. Gate weights and Router-upstream parameters are decomposed separately; expert parameters have no direct LB gradient and enter only through later route feedback.

## 8. Theorem State

There is no theorem establishing that Switch LB generally harms MoE training. The verified local proposition is narrower: for the registered frozen Vanilla checkpoints, subtracting the independently estimated true mean causes a direction-specific reduction in deep-layer route concentration; the inverse Centered add-back is not direction-specific sufficiency. A16_00's gradient and shadow-update proposition is untested.

## 9. Current Mechanism Chain

```text
shared Router-input component
-> expert-relative constant logit offset
-> coherent winner margins and hard concentration
-> soft LB may have stage-dependent corrective leverage
-> unresolved LM/LB update interaction
-> mechanism-conditioned choice of load controller
```

## 10. Anchor Structure

- [A16_00 parent Anchor](/Projects/from-attention-to-search/main/problem_anchors/16_load_control_gradient_interference/16_00_switch_lb_gradient_conflict/16_00_switch_lb_gradient_conflict_anchor.md) owns the LM-versus-LB gradient and shadow-step decision.
- [A16_00_01 DC sustainer boundary](/Projects/from-attention-to-search/main/problem_anchors/16_load_control_gradient_interference/16_00_switch_lb_gradient_conflict/subanchors/16_00_01_dc_sustainer_boundary_anchor.md) owns the completed frozen counterfactual.
- Dynamic expert bias and matched long-run efficiency are downstream stages, not yet formal Anchors.

## 11. Evidence Chain

1. The A15 [10B online routing result](/Projects/from-attention-to-search/main/experiments/A15/15_06_online_spectral_routing_and_relay/A15_06_E01_10b_online_spectral_routing/summary.md) found that equal LB coefficients coexisted with sharply different hard expert use.
2. The migrated [DC sustainer audit](/Projects/from-attention-to-search/main/experiments/A16/A16_00_01_E01_dc_sustainer_audit/summary.md) returned `necessary_only`: Vanilla mean removal reduced registered deep-layer busiest share by 0.68678 [0.68435, 0.68922], above matched-random q95 0.18326; Centered add-back did not exceed random q95.
3. The same audit found heterogeneous local LB logit leverage rather than universal gradient death.
4. Complete-global-batch LM/LB gradients, applied AdamW effects, and held-out shadow-step NLL remain unmeasured.

## 12. Rival Explanations

- **Beneficial regularization:** LM and LB gradients oppose locally, but LB improves or preserves held-out NLL while balancing load.
- **Hard/soft mismatch:** LB changes soft probabilities without changing hard winners, so any NLL cost is ineffective interference rather than a necessary balance tradeoff.
- **Optimizer-history effect:** raw gradients appear benign, but AdamW moments transform them into a harmful applied update.
- **Route-feedback effect:** the one-step audit is benign, while long-run expert exposure creates the eventual slowdown.

## 13. Claim Boundary

Current evidence does not show that all auxiliary balancing losses are harmful, that dynamic expert bias is superior, that one-step effects persist to long training, or that balance creates functional specialization. A16 is about load-control interference; A15 continues independently, A07's common/rare expert-parameter conflict remains a distinct line, and A05 retains general top-1 collapse mechanisms.

## 14. Method Landscape And Resolution Route

The Switch/GShard-style auxiliary objective is the common baseline. Loss-free balancing and DeepSeek-V3 motivate dynamic expert bias, which directly reacts to hard load without injecting a differentiable auxiliary term into LM parameters. BASE layers and Expert Choice change assignment semantics and are structural references rather than matched first repairs. Capacity limits, z-loss, noise, and drop controls remain stabilizers, not complete solutions to the current mechanism question.

The resolution route is:

```text
A16_00 harmful-conflict / regularization / ineffective-control audit
-> if harmful conflict or hard/soft mismatch: dynamic expert bias comparison
-> if beneficial regularization: retain LB and study saturation/scale
-> matched same-token, same-FLOP, and wall-clock efficiency test
```

## 15. Relation To Other Lines

A15 owns spectral and Relay routing performance and continues independently. A05 owns general top-1 lock-in and common-offset failure mechanisms. A07 owns common/rare conflict inside expert learning. A16 uniquely owns LM-objective versus load-control interaction and the selection of a load-control remedy.

## 16. One Next Decision

The Vanilla/Centered A16_00 audit is approved for Protocol, implementation,
smoke, and direct execution. Its eligible result will decide whether the first
intervention is dynamic expert bias, retained differentiable LB, or a
hard/soft-control repair. Completion requires identical global batches and full
optimizer states across LM-only and LM+LB shadow branches, two registered
seeds, independent probe documents, reconstructable raw gradients, hard-load
changes, and shadow-step NLL. Do not start dynamic expert bias long training
before this result.

## Source Map

- [Switch Transformer](https://jmlr.org/papers/v23/21-0998.html)
- [Loss-Free Balancing](https://arxiv.org/abs/2408.15664)
- [DeepSeek-V3](https://arxiv.org/abs/2412.19437)
- [BASE Layers](https://proceedings.mlr.press/v139/lewis21a/lewis21a.pdf)
- [Expert Choice Routing](https://arxiv.org/abs/2202.09368)
- [A16 line index](/Projects/from-attention-to-search/main/problem_anchors/16_load_control_gradient_interference/README.md)
