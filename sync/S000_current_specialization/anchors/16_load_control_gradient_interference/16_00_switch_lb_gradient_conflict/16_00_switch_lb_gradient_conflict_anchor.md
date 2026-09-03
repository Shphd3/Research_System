# A16_00 Switch Load-Balance Gradient Conflict


## 1. Problem Definition

The A16 line asks how to keep sparse-expert load operationally usable without slowing language-model learning or preventing expert differentiation. Existing evidence shows that a true token-shared Router-input component immediately sustains frozen Vanilla collapse, but it does not identify whether the differentiable load objective, the language-model objective, AdamW history, or hard-routing feedback formed that state.

The one decision question is: **from identical parameters, optimizer state, and global training batch at registered early, middle, and late states, does adding the Switch-style load-balancing gradient worsen the next-step held-out NLL while improving hard expert load, and does running-centering reduce that cost together with conflict in the Router-source, Gate, and routed expert-update pathways?**

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

Use the verified four-layer, hidden-size-768, eight-expert, top-1 DCLM MoE and its paired Vanilla-Full and Centered-Full conditions. At registered 50M, 6B, and 10B states in two seeds, replay the identical global optimizer batch, including all gradient-accumulation microbatches and distributed reduction. Compute LM-only and LB-only raw gradients without advancing the data cursor or optimizer.

Clone the complete parameter, AdamW-moment, scheduler, RNG, and Router-buffer state. Apply an LM-only shadow step and an LM-plus-LB shadow step, then evaluate both on the same untouched probe documents and fixed load-guard tokens. Record cosine, norms, and applied-update alignment for each layer's Gate weights and actual pre-center Router-source tensors. On frozen domain-stratified Web of Science documents, measure language-model gradient conflict among document groups co-routed to each expert. Expert parameters receive no direct LB gradient; a nonzero direct derivative is an implementation failure, while the measured expert conflict is a routing-mediated effect.

## 6. Minimal Falsification Tests

The decisive comparison is the Centered mediation of paired shadow-step $\Delta NLL_{LB}$ over the predeclared 50M, 6B, and 10B states, with stages and seeds separately visible. The primary rule has no arbitrary practical margin: both seed-specific document-bootstrap 95% lower bounds of the frozen stage-median effect must exceed zero and at least two stages per seed must point in the same direction. Router-source/Gate conflict and routed WoS expert conflict receive separate typed verdicts. Full-batch identity, exact state cloning, optimizer replay, probe isolation, deterministic Router buffers, and gradient reconstruction are hard guards.

Known-good cases include an artificial pair of opposing scalar objectives and an LB-only perturbation that reduces a constructed hard-load imbalance. Known-bad cases include identical objectives, zero LB coefficient, and permuted LB gradients. A negative cosine without positive $\Delta NLL_{LB}$ supports the regularization rival; positive $\Delta NLL_{LB}$ without load improvement supports ineffective interference. The test cannot identify the best long-run controller.

## 7. Current Evidence

All six relevant 30B training arms used the same Switch-style coefficient $\lambda_{LB}=0.01$, yet Vanilla-Full's deep layers approached single-expert routing around 50M--100M tokens while Centered-Full remained broadly used. This shows that a shared coefficient does not guarantee shared hard-load behavior.

The migrated frozen counterfactual returned `necessary_only`: subtracting the independently estimated true mean from Vanilla reduced registered deep-layer busiest-expert share by 0.68678 with paired 95% interval [0.68435, 0.68922], far above a matched-random q95 of 0.18326. Adding the saved center to independently trained Centered did not exceed its random control. The common component therefore immediately sustains current Vanilla collapse, but static add-back does not reconstruct the separately adapted training path. [The migrated subanchor](subanchors/16_00_01_dc_sustainer_boundary_anchor.md) and [result](/Projects/from-attention-to-search/main/experiments/A16/A16_00_01_E01_dc_sustainer_audit/summary.md) record this boundary.

The completed 12-cell multistage audit rejects a global “centering reduces LB conflict everywhere” explanation. At 50M, Vanilla paid a reproducible +0.000845/+0.000617 nat/token effective-LB shadow cost while Centered was indistinguishable from zero; the paired Centered mediation was positive in both seeds. At 6B the mediation point estimates reversed, and at 10B only seed 29 was precise. Seed 17 failed the registered stage-median interval while seed 29 passed, so the two-seed outcome verdict is Fail. Shared Router-path and within-expert conflict clauses also failed. [Multistage result](/Projects/from-attention-to-search/main/experiments/A16/A16_00_02_E01_multistage_gradient_pathway_audit/summary.md).

The same implementation audit found that the source 30B trajectories did not actually receive the configured LB gradient: re-entrant activation checkpointing detached the nested auxiliary tensor. The valid A16 result is therefore an exact-state, truly differentiable counterfactual shadow step at frozen states. It cannot be used as evidence that the original trajectories were trained under effective LB.

## 8. Claim Boundary And Next Decision

Supported: the DC component immediately sustains frozen Vanilla collapse; centering removes a reproducible early-state differentiable-LB cost; and the LB effect is strongly stage-dependent. Rejected: centering does not globally reduce shared-path or routed-expert conflict across both seeds and all stages. The original long-run LB effect remains unresolved because the source runs did not apply an effective LB gradient.

This Anchor cannot claim that all auxiliary losses are harmful, that dynamic expert bias is already superior, that early one-step effects persist to long training, or that better balance creates useful expert specialization. Dynamic expert bias is the researcher-approved first intervention only if A16_00 supports harmful interference or hard/soft mismatch.

The multistage audit is complete. The single next decision is whether Centered +
dynamic expert bias can preserve usable hard load more efficiently than Centered +
truly differentiable LB and Centered without extra load control. The comparison must
match tokens, initialization, data order, capacity, and compute and report held-out
NLL/FLOP together with hard expert load. Do not interpret the completed one-step
audit as proof that dynamic bias is already superior.
