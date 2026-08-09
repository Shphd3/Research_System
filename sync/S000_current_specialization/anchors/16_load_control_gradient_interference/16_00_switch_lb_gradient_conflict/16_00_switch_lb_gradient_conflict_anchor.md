# A16_00 Switch Load-Balance Gradient Conflict

Thinking Card source: [16_00_switch_lb_gradient_conflict_thinking_card.md](16_00_switch_lb_gradient_conflict_thinking_card.md)

## 1. Problem Definition

The A16 line asks how to keep sparse-expert load operationally usable without slowing language-model learning or preventing expert differentiation. Existing evidence shows that a true token-shared Router-input component immediately sustains frozen Vanilla collapse, but it does not identify whether the differentiable load objective, the language-model objective, AdamW history, or hard-routing feedback formed that state.

The one decision question is: **from identical parameters, optimizer state, and global training batch during the first 100M tokens, does adding the Switch-style load-balancing gradient worsen the next-step held-out NLL while improving hard expert load, with negative raw LM/LB gradient cosine on the affected Router parameter groups?**

“Gradient conflict” here means opposition between the language-model (LM) and load-balancing (LB) objectives on shared Gate or upstream Router parameters. It is not the common/rare gradient conflict measured inside expert parameters by A07. Pass selects a non-gradient load controller as the first repair; Fail retains auxiliary LB or redirects to hard/soft control mismatch; invalid state pairing or incomplete global gradients is Insufficient.

## 2. Physical Priors

1. A differentiable auxiliary target can improve its own statistic while opposing descent of the primary target on shared parameters. This prior is false if the LB shadow update does not worsen independent LM NLL.
2. Negative raw-gradient cosine is mechanistic but not outcome evidence: intended regularization may oppose the current training gradient and still improve held-out NLL.
3. Load control is useful only when it changes hard expert usage. A quality cost without reduced hard concentration is ineffective interference, not a balance--quality trade-off.

## 3. Falsifiable Hypotheses

- **H1, harmful LB interference:** the LM-plus-LB shadow step has higher held-out NLL than the LM-only shadow step, reduces busiest-expert share, and has negative LM/LB global-batch gradient cosine in the Gate or Router-upstream groups.
- **Strongest rival, beneficial regularization:** raw gradients can oppose locally, but adding LB does not worsen held-out NLL and may improve it while balancing load.
- **Control-mismatch rival:** adding LB does not materially reduce hard concentration, so collapse reflects soft-probability versus hard top-1 mismatch, saturation, or path feedback rather than a price paid for successful balance.

Pass requires the H1 signature separately in both registered seeds. Fail means the held-out penalty is absent or the gradient mechanism is not opposed; an ineffective-control outcome redirects to a direct hard-load controller without calling LB gradient harmful. Opposite seed directions, non-identical shadow states, or missing full-batch gradients are Insufficient.

## 4. Mathematical Model

At training state $s_t$, let $g_{LM}$ be the raw language-model gradient and $g_{LB}=\lambda_{LB}\nabla L_{LB}$ the coefficient-scaled load gradient on one registered parameter group. Their global-batch cosine is

$$
c_t=\frac{\langle g_{LM},g_{LB}\rangle}
{\lVert g_{LM}\rVert\lVert g_{LB}\rVert+\epsilon}.
$$

$c_t<0$ means local objective opposition but cannot by itself prove harm. Let $T_{AdamW}(s,g)$ apply one shadow AdamW step from the complete same state $s$, including moments and scheduler. The primary metric is

$$
\Delta NLL_{LB,t}
=NLL_{probe}\!\left(T_{AdamW}(s_t,g_{LM}+g_{LB})\right)
-NLL_{probe}\!\left(T_{AdamW}(s_t,g_{LM})\right).
$$

It is measured in nat/token; positive values mean the current LB contribution worsens one-step prediction on independent text. The paired hard-load effect is $\Delta M_t=M_{LM+LB}-M_{LM}$, where $M$ is busiest-expert share and $\Delta M_t<0$ means better balance. These quantities establish an immediate optimization trade-off, not long-horizon causality or expert utility.

## 5. Computational Realization

Use the verified four-layer, hidden-size-768, eight-expert, top-1 DCLM MoE and its paired Vanilla-Full and Centered-Full conditions. At registered early states in two seeds, replay the identical global optimizer batch, including all gradient-accumulation microbatches and distributed reduction. Compute LM-only and LB-only raw gradients without advancing the data cursor or optimizer.

Clone the complete parameter, AdamW-moment, scheduler, RNG, and Router-buffer state. Apply an LM-only shadow step and an LM-plus-LB shadow step, then evaluate both on the same untouched probe documents and fixed load-guard tokens. Record cosine, norms, and applied-update alignment for each layer's Gate weights and Router-input upstream parameter group. Project Gate/upstream gradients onto the independently registered DC and centered-residual directions to connect with the completed DC audit. Expert parameters receive no direct LB gradient; any expert effect is a later routing-feedback question.

## 6. Minimal Falsification Tests

The decisive comparison is the paired shadow-step $\Delta NLL_{LB}$, aggregated over predeclared early states and probe documents but reported separately for seeds. The primary rule has no arbitrary practical margin: both seed-specific document-bootstrap 95% lower bounds must exceed zero. Mechanistic support additionally requires negative registered global-batch cosine in the same parameter groups and a paired reduction in busiest-expert share. Full-batch identity, exact state cloning, optimizer replay, probe isolation, deterministic Router buffers, and gradient reconstruction are hard guards.

Known-good cases include an artificial pair of opposing scalar objectives and an LB-only perturbation that reduces a constructed hard-load imbalance. Known-bad cases include identical objectives, zero LB coefficient, and permuted LB gradients. A negative cosine without positive $\Delta NLL_{LB}$ supports the regularization rival; positive $\Delta NLL_{LB}$ without load improvement supports ineffective interference. The test cannot identify the best long-run controller.

## 7. Current Evidence

All six relevant 30B training arms used the same Switch-style coefficient $\lambda_{LB}=0.01$, yet Vanilla-Full's deep layers approached single-expert routing around 50M--100M tokens while Centered-Full remained broadly used. This shows that a shared coefficient does not guarantee shared hard-load behavior.

The migrated frozen counterfactual returned `necessary_only`: subtracting the independently estimated true mean from Vanilla reduced registered deep-layer busiest-expert share by 0.68678 with paired 95% interval [0.68435, 0.68922], far above a matched-random q95 of 0.18326. Adding the saved center to independently trained Centered did not exceed its random control. The common component therefore immediately sustains current Vanilla collapse, but static add-back does not reconstruct the separately adapted training path. [The migrated subanchor](subanchors/16_00_01_dc_sustainer_boundary_anchor.md) and [result](/Projects/from-attention-to-search/main/experiments/A16/A16_00_01_E01_dc_sustainer_audit/summary.md) record this boundary.

The same audit found no universal “LB gradient is dead after collapse” rule: local softmax leverage varied across layers and checkpoints. Direct LM/LB global-batch gradients, applied AdamW updates, and shadow-step NLL have not yet been measured. A16_00 is therefore not yet experimentally adjudicated.

## 8. Claim Boundary And Next Decision

Supported: the DC component is a direction-specific immediate sustainer of frozen Vanilla collapse, and coefficient equality does not imply equivalent hard-load control. Unresolved: whether auxiliary LB imposes a held-out learning cost, acts as beneficial regularization, or simply lacks leverage over saturated hard routing.

This Anchor cannot claim that all auxiliary losses are harmful, that dynamic expert bias is already superior, that early one-step effects persist to long training, or that better balance creates useful expert specialization. Dynamic expert bias is the researcher-approved first intervention only if A16_00 supports harmful interference or hard/soft mismatch.

The researcher has approved the Vanilla-Full and Centered-Full early-gradient
and shadow-update experiment for Protocol, implementation, smoke, and direct
execution. Exactly one next decision now follows its eligible result: choose
dynamic expert bias, retained differentiable LB, or a hard/soft-control repair.
Completion requires both seeds and both model conditions to preserve identical
global batches and complete optimizer state and to reconstruct
$\Delta NLL_{LB}$, hard-load change, and batch-gradient cosine under the frozen
rule. Resume by freezing and executing that Protocol; do not start the
dynamic-bias long-training comparison first.
