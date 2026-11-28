# Anchor: Router-to-representation gradient feedback

## 1. Problem Definition

Version clarification (2026-10-07 exposition edit): zero-aux descriptions refer to the original R1 condition. The final A3 amendment and Protocol A3 own the current training condition. Both A3 auxiliary paths are detached at r, leaving the LM feedback intervention unchanged. This distinguishes versions; it does not revise hypotheses, approval, the eight-section design or researcher judgment.

In a fixed-budget causal language model, does the direct LM gate-gradient returned to the shared backbone help or harm heldout prediction and functional expert differentiation? The researcher activated this independent temporary question and delegated design concretization, implementation, Smoke and submission in [the request](../../../handoff/researcher_request_cn.md). The root direction is better MoE learning allocation. Earlier fixed-action selection failed to beat a strong fixed common update; that does not test jointly learned experts. This experiment changes one backward edge while keeping the forward calculation unchanged at equal state. Its scope is one paired seed at a frozen token endpoint. Scientific mechanism judgment and a practical adoption threshold remain Unknown.

## 2. Physical Priors

Working hypothesis (AI proposal): a gate-gradient can help construct task-relevant differentiation or distort the shared representation. Chain-rule decomposition is mathematical, not empirical evidence for either direction. The credible alternatives are gradient magnitude/Adam preconditioning, unequal realized expert exposure and hardware arithmetic. None is assumed negligible.

## 3. Falsifiable Hypotheses

The open comparison allows either sign: coupled feedback may reduce heldout CE and increase sensitivity to causal, usage-preserving route reassignment; alternatively detached feedback may do so. A geometry change without better CE does not support utility. CE improvement without functional intervention support or with unresolved hardware/load explanation is bounded evidence, not a mechanism identification. The researcher's strongest-rival ranking remains Unknown; the registered alternatives are AI audit choices under delegated design.

## 4. Mathematical Model

At layer l, r is the attention output before residual addition; h is the normalized hidden state after that addition and is the expert input. Router logits are W r; p is their softmax over eight experts; K contains the top two. Selected weights retain their original probability mass. The shared expert S and routed experts E receive complete h. The layer contribution is

\[
m=S(h)+\sum_{i\in K}p_i(Wr)E_i(h).
\]

A uses live r; B substitutes stop-gradient(r) only inside W r. For the same state and sample, the forward function is identical. With auxiliary coefficient zero, B removes only the LM gate contribution to r; W, E, S, h and residual routes still receive their ordinary gradients. For a fixed differentiable routing branch, the difference in parameter gradients equals the upstream Jacobian transpose times the gate-path gradient, summed over intervened layers. Top-k boundary derivatives are not claimed. Hidden-state derivatives do not equal the next hidden-state displacement under AdamW. CE difference is defined as B minus A in nat per valid prediction token; positive favors A.

## 5. Computational Realization

Goal: distinguish backward feedback from forward changes. How: independently adapt the inspected 342M/12-layer native MoE scaffold, disable EMA and unrelated regularizers, intervene at all router inputs, load the same saved random initial state, use one data order and one global token batch across rank counts. Why: this tests the direct edge without freezing representation or expert learning. Local autograd checks isolate gate-only and expert-only paths and verify router/expert parameter gradients at a common state. A/B short windows run on each authorized Smoke hardware; their numerical spread remains a diagnostic.

Goal: assess utility and function before selecting stories from results. How: frozen document-level heldout CE and within-model causal route-bundle permutations with identical per-layer expert counts and gate-weight multisets; characterize geometry and finite updates separately. Why: descriptions of clusters/rank do not establish useful specialization. X-MoE's chain-rule and low-dimensional routing provide prior context, not a proof of total collapse or this detach intervention. DeepSeek-V3 §4.5.3 shows that batch-wise auxiliary balancing can match aux-free loss; the original R1 condition therefore kept aux=0; current A3 is specified below and does not compare balancing schemes. See [analysis Protocol](../../experiments/router_representation_gradient_feedback/analysis_protocol.md).

## 6. Minimal Falsification Tests

The primary falsifier is paired token-weighted heldout CE at the frozen endpoint with document-cluster bootstrap. An AI-proposed practical difference is 0.01 nat/token, reported separately from the zero-effect interval; researcher adoption threshold is Unknown. Supporting evidence requires a directional CE interval beyond that proposal, eligible engineering evidence and functional-route intervention consistent with differentiation. Reverse evidence weakens that direction; geometry alone, an interval spanning the relevant difference, missing endpoint or unresolved major rival gives INSUFFICIENT. Even support concerns only these trajectories and does not isolate hardware-free algorithm causation.

## 7. Current Evidence

New trajectories: NOT RUN at registration. The inspected scaffold and historical hardware receipts establish reusable engineering behavior only. Earlier fixed-library negative results do not settle this question. Smoke and local gradient checks will be recorded in Detailed, not promoted to scientific results.

## 8. Claim Boundary And Next Decision

This is an exploratory, single-seed, hardware-confounded comparison. It cannot establish universal representation collapse, all common-adaptation mechanisms, seed uncertainty or broadly improved MoE performance. The next researcher-owned decision is whether to retain, remove or further test direct feedback. Completion requires eligible aligned endpoint CE, functional tests and rival accounting; later inspect the existing jobs/checkpoints and execute the frozen analysis, without automatic retraining or additional submissions.


### Current design amendment A3 (2026-10-06)

The researcher explicitly selected a new common load-balancing condition and authorized fresh retraining with supervision. Protocol A3 now owns that exact execution condition. The original zero-aux design above remains historical. Both arms add coefficient0.01, layer-mean sequence-local balancing with the auxiliary reference detached in both; only the LM feedback edge differs. Same-state forward equality and the primary utility/function/geometry boundaries remain. No scientific closure or adoption follows from this design amendment.
