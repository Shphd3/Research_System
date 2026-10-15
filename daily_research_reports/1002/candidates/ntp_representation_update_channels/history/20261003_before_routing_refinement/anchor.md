# Candidate Anchor: Shared computation and specialized learning under finite expert budgets

Updated: 2026-10-03. Temporary candidate; same evolving research question, not a new formal project or Focus. Researcher instruction: [authorization receipt](/data/250010109/MoE_Router/experiments/20261003_common_specialized_capacity/receipts/user_authorization.json). Prior design is preserved in [history](history/20261002_before_capacity_refinement/reading/anchor.md); prior results remain historical evidence, not results of this design.

## 1. Problem Definition

The researcher wants separated learning to increase useful learning capacity: small specialized experts should reuse common processing and approach the learning performance of a larger dense model. The current bounded question is whether an explicit common computation, followed by specialized processing, improves learning and retention across a fixed sequence of four natural-text domains at a specified parameter and token budget.

The object of study is a causal language model trained from random initialization. A known record domain selects one expert at each feed-forward layer. This is a mechanism condition with oracle routing; it does not solve learned routing. “Capacity” currently means a motivation, not a measured saturation limit. This round measures finite-budget loss and retention. It does not determine how many tasks can be stored before a specified acceptable-loss threshold is crossed.

States: `task_state=IN_PROGRESS`; `question_state=OPEN`; `design_state=FROZEN_WITH_PRE_RESULT_ANALYSIS_AMENDMENTS`; `result_state=NOT_RUN`. The explicit instruction delegates bounded implementation and experiment choices; it does not pre-confirm an interpretation or practical success threshold. Researcher-selected acceptable dense gap and saturation definition remain `Unknown`.

## 2. Physical Priors

NTP targets are available during training. Update allocation may use them; a pre-update representation predictor is not a prerequisite. Natural-text domains can share useful structure, but architectural sharing does not establish functional shared knowledge. A shared module can save repeated parameters and can also transmit drift to previously learned domains. Unselected experts must remain unchanged for that distinction to be meaningful.

Finite-data sharing may also reduce estimation variance through pooling without enlarging the function family; the [statistical toy model](capacity_mathematics.md) states exact conditions. It neither establishes the current NTP mechanism nor changes the experiment contract.

Published shared-expert evidence is conditional. [DeepSeekMoE](https://arxiv.org/html/2401.06066v1) reports benefits of shared-expert isolation in its evaluated settings; [OLMoE](https://arxiv.org/html/2409.02060v1), §4.1.3/Figure 6, reports a slightly worse shared-expert ablation under its matching scheme. Neither proves this sequential common-to-specialized mechanism. [Progressive Networks](https://arxiv.org/pdf/1606.04671) provides a precedent for old features feeding new computation while adding capacity; [PackNet](https://arxiv.org/pdf/1711.05769) motivates distinguishing reusable frozen knowledge from remaining finite capacity.

## 3. Falsifiable Hypotheses

H1, sharing: common_parallel can achieve comparable or lower finite-budget old/new-domain loss than private_active while using fewer total FFN parameters. Initial functions are matched by copying common channels into every private_active expert. A failure would be a consistent loss disadvantage or a trade-off explained by transferred harm rather than useful reuse.

H2, coupling: common_serial can improve the same loss/retention coordinates relative to common_parallel, with identical parameter counts and nominal FFN multiplies. This tests the whole computation change; it does not isolate semantic knowledge reuse from greater effective nonlinear depth or altered optimization.

H3, update transmission: after a new-domain phase, an old domain's expert is unchanged. Finite common/trunk interventions can separate contributions of the changed common FFNs and the remaining shared parameters to its loss change. Positive drift is not assumed; beneficial transfer and harmful transfer are both retained.

The strongest rivals are undertraining; extra parameters or compute; function/initialization differences; task-specific memorization; shared trunk drift; domain-order effects; and serial effective depth. Two seed/order blocks only test replication across those joint conditions, not independent seed and order effects.

## 4. Mathematical Model

Let r be the post-attention residual and z=RMSNorm(r). C is a shared SwiGLU and E_d is the expert selected by record domain d. Parallel returns r+C(z)+E_d(z). Serial returns r+C(z)+E_d(z+C(z)). The specialist receives their sum, not z and C(z) separately. This residual supplies a direct input path, but the resulting map need not be invertible or information-preserving.

For E experts, common width c and private width p, the FFN parameter counts, ignoring no terms within bias-free SwiGLU, are 3h(c+Ep) total and 3h(c+p) active per layer. private_active uses width c+p in each expert; private_total uses p+c/E. A private-only model cannot match both total and active FFN counts with fixed E and c>0. Dense references therefore include both active-matched and total-matched widths. Shared embedding/attention parameters are identical in all arms and are included in whole-model totals.

A linear illustrative model W_d=C+E_d admits shared storage savings only when useful reusable structure actually exists. Sequential residual composition is (I+E_d)(I+C)=I+C+E_d+E_d C. If I+C is invertible, E_d(I+C) can be absorbed into a rank-preserving private map. Thus linear serial composition need not expand the function class. The nonlinear network must earn any benefit empirically; channel widths are not asserted to equal semantic ranks.

For an old domain i, retain its unchanged E_i and compare old/new C and trunk T. Let L_ab=L(C_a,T_b,E_i), with 0 before and 1 after the current phase. Define

\[
\phi_C=\tfrac12[(L_{10}-L_{00})+(L_{11}-L_{01})],\qquad
\phi_T=\tfrac12[(L_{01}-L_{00})+(L_{11}-L_{10})].
\]

Then phi_C+phi_T=L_11-L_00. The interaction is L_11-L_10-L_01+L_00. Keep all four losses; the allocation is a symmetric finite decomposition, not a unique semantic cause or a reachable training path.

Further explanation: invertibility preserves information but does not ensure closure of a limited expert family under nonlinear composition. The [linear equivalence and nonlinear counterexample](capacity_mathematics.md) separate representation, learning, retention and gradient-path obligations.

## 5. Computational Realization

Use the six arms and exact data/budget in [Protocol](protocol.md). The model has eight layers, h=256, four query heads, two KV heads, tied vocabulary embeddings and an identical additive domain embedding in every arm, and no SAE or learned router. Widths c=256, p=384, E=4. A larger approximately 300M model remains an authorized option, not a committed parallel experiment.

Train four-domain mixed warmup for 512 updates, then four single-domain phases of 1024 updates each. Each update has 8192 valid prediction targets; the fixed endpoint is 37,748,736 exposures. Both seed/order blocks run all arms. The only training allocation is one 8×RTX5090 SPOT node, with one independent trajectory per GPU and queued conditions on freed GPUs.

## 6. Minimal Falsification Tests

One experiment family contains six conditions, two paired seed/order blocks, and a finite intervention analysis on its retained checkpoints. Primary comparisons are serial versus parallel, parallel versus private_active, and both common arms versus dense_total/dense_active and private_total on explicitly distinct resource coordinates.

Inspect the full domain-by-stage dev matrix, own-phase learning gains, subsequent forgetting, final macro dev loss, and final held-out test loss. Preserve per-domain outcomes so one domain's benefit cannot hide another's harm. Common/trunk rollback tests the transmission path when an old expert is frozen. Parameter/optimizer hashes verify that condition before interpreting the intervention.

Two further preregistered finite diagnostics address the same question: a same-forward intervention on the selected through-expert common-gradient path, and expert-bank swaps retaining true domain inputs. They test a local update path and current functional matching, not long-term capacity. Protocol section17 records these pre-result amendments.

## 7. Current Evidence

At this revision, this new training family is `NOT RUN`. [Earlier finite-update results](source_transfer_addendum_cn.md) establish only the behavior of their old model and panels. They do not validate common/shared expert capacity. Data preparation and independent selected-record checks have passed; implementation and exact-resource Smoke remain gates before training. Evidence locations are in [Protocol](protocol.md) and the [execution directory](/data/250010109/MoE_Router/experiments/20261003_common_specialized_capacity).

## 8. Claim Boundary And Next Decision

A lower loss at a fixed endpoint supports only a bounded performance comparison. A common rollback effect establishes sensitivity to those finite parameter changes, not that common features are universal knowledge. Four known domains with four experts do not exhaust expert slots. No final method endorsement, capacity saturation, learned routing success, or long-run transfer claim follows from this round.

The next evidence-driven decision is whether the observed gap is primarily acquisition, retention, or shared drift, and whether serial coupling changes it enough to motivate a depth-controlled or more-task/fewer-expert experiment. These are AI suggestions until the researcher selects the next scientific claim. Keep this work in the temporary bundle.
