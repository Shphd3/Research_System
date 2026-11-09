# Load Control, Gradient Interference, And Resolution

## 0. Definitions

- **Hard expert load:** the fraction of top-1 assignments received by each expert; the busiest-expert share is its maximum.
- **Switch load-balancing objective:** the differentiable auxiliary objective \(L_{LB}=E\sum_e f_e\bar p_e\), combining detached hard fractions \(f_e\) and mean soft Router probabilities \(\bar p_e\).
- **Gradient conflict:** opposite directions between the language-model (LM) and LB raw gradients on Gate or Router-upstream parameters, measured over the complete global batch.
- **Dynamic expert bias:** a non-gradient controller that adjusts expert-specific routing biases from observed hard load; it is a candidate intervention, not established evidence.

## 1. Abstract

A15 matched training exposed sharply different hard load between Vanilla-Full and Centered-Full. A migrated frozen counterfactual established that the true token-shared Router-input component immediately sustains current Vanilla collapse. A16 then discovered that the source runs recorded \(\lambda_{LB}=0.01\) but did not apply an effective LB gradient because the nested auxiliary tensor was detached by re-entrant activation checkpointing. A qualified counterfactual shadow audit therefore made LB truly differentiable at paired 50M, 6B, and 10B states. Centering reproducibly removed an early LB cost at 50M, but did not globally reduce held-out cost, Router-path conflict, or routed expert conflict across later states. The next problem is no longer “prove LB is uniformly harmful”; it is whether non-gradient dynamic expert bias can provide hard-load control more efficiently than effective differentiable LB in an already centered model.

## 2. Research Question

Can an MoE maintain operational expert load without slowing language-model learning or preventing useful expert differentiation? The completed local diagnostic asked whether centering reduces the one-step held-out cost and gradient opposition of effective Switch LB. Its global answer is no, with a reproducible early exception. The next local decision is whether dynamic expert bias outperforms effective LB and no added controller under matched Centered training.

## 3. Why The Previous Framing Was Insufficient

Equal LB coefficients do not imply equal hard routing. A large auxiliary value does not imply strong corrective force, a negative gradient cosine does not imply held-out harm, and a balanced Router does not imply useful specialization. These objects must be separated before selecting a repair.

## 4. Empirical Layout

The source system is the verified four-layer, hidden-768, eight-sparse-expert, top-1 DCLM MoE. A16_00_02 used paired Vanilla-Full and Centered-Full states for seeds 17/29 at 50M, 6B, and 10B; exact next DCLM batches; complete optimizer states; and 112 independent WoS validation documents. All 12 cells passed the execution guards.

## 5. Physical Intuition

A token-shared input component becomes an expert-specific constant logit offset after the linear Gate. It can coherently enlarge one expert's margin across many tokens. The Switch objective reacts through soft probabilities, whereas deployment uses hard top-1 winners. When margins saturate, the auxiliary penalty can remain large while its ability to change winners becomes stage- and layer-dependent. The central uncertainty is whether its remaining gradient is merely ineffective, beneficially regularizing, or actively opposing LM progress.

## 6. Decision Metrics

The primary metric is

\[
\Delta NLL_{LB,t}=NLL_{probe}(T_{AdamW}(s_t,g_{LM}+g_{LB}))-NLL_{probe}(T_{AdamW}(s_t,g_{LM})).
\]

It is measured in nat/token. Positive values mean that adding LB from the same optimizer state makes the next prediction step worse on independent text. It establishes an immediate quality cost, not a long-run training effect.

The mechanism metric is

\[
c_t=\frac{\langle g_{LM},g_{LB}\rangle}{\lVert g_{LM}\rVert\lVert g_{LB}\rVert+\epsilon}.
\]

Negative \(c_t\) means the two objectives locally oppose each other in a registered parameter group. It cannot by itself show harm. Hard-load benefit is measured by the paired change in busiest-expert share; negative change means better balance.

## 7. Minimal Mechanistic Model

The one-step update is not the raw gradient alone. AdamW transforms \(g_{LM}+g_{LB}\) using stored first and second moments, weight decay, learning rate, and scheduler state. A16 therefore compares complete shadow states rather than treating cosine as a surrogate for performance. Gate weights and Router-upstream parameters are decomposed separately; expert parameters have no direct LB gradient and enter only through later route feedback.

## 8. Theorem State

There is no theorem establishing that Switch LB generally harms MoE training. The verified propositions are narrower: mean removal immediately reduces frozen Vanilla concentration; centering removes a repeatable effective-LB cost at the 50M state; and the cost is not uniformly persistent across 6B/10B. The registered global lower-interference hypothesis failed.

## 9. Current Mechanism Chain

```text
shared Router-input component
-> expert-relative constant logit offset
-> coherent winner margins and hard concentration
-> effective soft LB has stage-dependent quality and hard-load effects
-> centering reduces the early cost but not all later conflict
-> compare non-gradient hard-load control against effective LB
```

## 10. Anchor Structure

- [A16_00 parent Anchor](../../problem_anchors/16_load_control_gradient_interference/16_00_switch_lb_gradient_conflict/16_00_switch_lb_gradient_conflict_anchor.md) owns the LM-versus-LB gradient and shadow-step decision.
- [A16_00_01 DC sustainer boundary](../../problem_anchors/16_load_control_gradient_interference/16_00_switch_lb_gradient_conflict/subanchors/16_00_01_dc_sustainer_boundary_anchor.md) owns the completed frozen counterfactual.
- Dynamic expert bias and matched long-run efficiency are downstream stages, not yet formal Anchors.

## 11. Evidence Chain

1. The A15 [10B online routing result](../../experiments/A15/15_06_online_spectral_routing_and_relay/A15_06_E01_10b_online_spectral_routing/summary.md) found that equal LB coefficients coexisted with sharply different hard expert use.
2. The migrated [DC sustainer audit](../../experiments/A16/A16_00_01_E01_dc_sustainer_audit/summary.md) returned `necessary_only`: Vanilla mean removal reduced registered deep-layer busiest share by 0.68678 [0.68435, 0.68922], above matched-random q95 0.18326; Centered add-back did not exceed random q95.
3. The source-training audit found the configured LB tensor was detached from backward, so coefficient equality was a config fact rather than an active-loss fact.
4. The completed [multistage audit](../../experiments/A16/A16_00_02_E01_multistage_gradient_pathway_audit/summary.md) found positive Centered mediation in both seeds at 50M, but only seed 29 passed the registered three-stage summary; shared-path and expert-conflict clauses failed.

## 12. Rival Explanations

- **Beneficial regularization:** LM and LB gradients oppose locally, but LB improves or preserves held-out NLL while balancing load.
- **Hard/soft mismatch:** LB changes soft probabilities without changing hard winners, so any NLL cost is ineffective interference rather than a necessary balance tradeoff.
- **Optimizer-history effect:** raw gradients appear benign, but AdamW moments transform them into a harmful applied update.
- **Route-feedback effect:** the one-step audit is benign, while long-run expert exposure creates the eventual slowdown.

## 13. Claim Boundary

Current evidence shows neither that all auxiliary balancing losses are harmful nor that dynamic expert bias is superior. The shadow audit is counterfactual at frozen states because the source runs did not receive effective LB. It cannot establish long-run effects or useful specialization. A16 remains separate from A15 spectral utility, A07 common/rare expert conflict, and A05 general top-1 collapse.

## 14. Method Landscape And Resolution Route

The Switch/GShard-style auxiliary objective is the common baseline. Loss-free balancing and DeepSeek-V3 motivate dynamic expert bias, which directly reacts to hard load without injecting a differentiable auxiliary term into LM parameters. BASE layers and Expert Choice change assignment semantics and are structural references rather than matched first repairs. Capacity limits, z-loss, noise, and drop controls remain stabilizers, not complete solutions to the current mechanism question.

The resolution route is:

```text
A16_00 completed stage-specific conflict / regularization / hard-load audit
-> compare Centered + dynamic bias / effective LB / no controller
-> matched same-token, same-FLOP, and wall-clock efficiency test
```

## 15. Relation To Other Lines

A15 owns spectral and Relay routing performance and continues independently. A05 owns general top-1 lock-in and common-offset failure mechanisms. A07 owns common/rare conflict inside expert learning. A16 uniquely owns LM-objective versus load-control interaction and the selection of a load-control remedy.

## 16. One Next Decision

The Vanilla/Centered multistage audit is complete. The single next decision is
whether Centered + dynamic expert bias preserves hard load and held-out NLL/FLOP
better than Centered + truly differentiable LB and Centered without an added
controller. The comparison must match two seeds, initialization, data order,
capacity, tokens, and compute; the current audit alone cannot approve a winner.

## Source Map

- [Switch Transformer](https://jmlr.org/papers/v23/21-0998.html)
- [Loss-Free Balancing](https://arxiv.org/abs/2408.15664)
- [DeepSeek-V3](https://arxiv.org/abs/2412.19437)
- [BASE Layers](https://proceedings.mlr.press/v139/lewis21a/lewis21a.pdf)
- [Expert Choice Routing](https://arxiv.org/abs/2202.09368)
- [A16 line index](../../problem_anchors/16_load_control_gradient_interference/README.md)
