# A17_04_02: Shared versus mode-specific updates under a fixed budget

## 1. Problem Definition

Does assigning some trainable updates to visible modes improve joint old/new rule learning over sharing every update, at the same total trainable parameter budget, data exposure and executed matrix-computation budget? The parent problem asks when sharing helps and when differentiated processing is worth its cost. Reversed-only training destroyed an acquired old mapping, but joint supervision demonstrated that shared parameters can express both mappings. Neither observation measures the utility of parameter separation.

The researcher has adopted a comparison of fully shared, known-mode separate, and shared-base-plus-private-increment designs, and initially requested documents only. On2026-10-12 the researcher adopted this design and authorized implementation, Smoke and a one-seed acquisition pilot; the formal multi-seed comparison is held. This child inherits the parent's next comparison decision. Architecture and operational criteria below originated as AI proposals and are now adopted for the specified design; mechanism acceptance remains Unknown. The formal utility comparison remains **NOT RUN**. Engineering/acquisition facts are separately owned by the result records. A positive comparison motivates learned routing; no gain weakens separation at this allocation; failed learning qualification leaves utility unresolved. This is a conditional attention-update model, not a production feed-forward MoE comparison.

## 2. Physical Priors

**AI_PROPOSAL:** restricting which modes can change a parameter may protect conditional predictions while retaining some reusable learning. Conversely, reserving private capacity reduces the capacity available to each example, so separation may lose useful transfer. These are competing empirical possibilities. A fixed mode mask guarantees direct update isolation in the fully private arm; that architectural identity alone is not evidence of a practical benefit.

## 3. Falsifiable Hypotheses

Candidate H: with identical joint old/new supervision and fixed resources, a mode-specific allocation improves the weakest conditional rule accuracy by a practically meaningful amount while preserving competence in both modes. The strongest rival is that any gain comes from a smaller effective rank or changed optimization, rather than useful mode-dependent allocation. Equal-total-budget comparison removes extra storage as an explanation; smaller fully shared rank controls test the effective-capacity explanation. Factorization, optimization and allocation remain interacting causes, so support establishes allocation utility in this family, not an isolated biological or semantic mechanism.

## 4. Mathematical Model

Start from one acquired-old Qwen3-0.6B state and freeze its entire network. At its last attention layer, add trainable low-rank updates to query, key, value and output projections. For projection \(p\), input \(h\), visible mode \(m\), and frozen weight \(W_0^{(p)}\), define

\[
W^{(p)}(m)h=W_0^{(p)}h+B^{(p)}\operatorname{diag}(g_m)A^{(p)}h,
\qquad
J=\frac1{20}\sum_{i=1}^{20}-\log p(y_i\mid m_i,c_i,L_i).
\]

Here \(A^{(p)}\) has 16 rows, \(B^{(p)}\) has 16 columns, and \(g_m\) is a fixed binary mask. Each row/column pair is an engineering rank slot, not an identified functional direction. The gain is one for all conditions. Each batch contains ten old and ten reversed-new answer tokens. Mode one maps甲 to the first item and乙 to the last; mode two reverses the mapping. The label is a target, never an input. Routing may use only the visible mode, not the target or an experimental-world label.

Fully shared S16 activates all slots in both modes. Separate U8/8 assigns eight slots to each mode. Hybrid H8/4/4 activates eight shared slots and four private slots per mode. The original frozen backbone is shared in every arm; 'fully separate' refers only to new trainable increments. No orthogonality, semantic expert labels, learned router, or auxiliary loss is imposed.

## 5. Computational Realization

**Goal:** compare allocation without rewarding extra parameters or old supervision. **How:** use one factor-bank implementation and change only its masks. The four projection dimension sums total10,240 parameters per rank slot, giving163,840 trainable parameters in all three main arms. Their active parameters per example are163,840/81,920/122,880. Each arm computes dense rank16 products even for masked slots, matching executed matrix shapes. This deliberately tests quality under a common compute budget; it does not measure sparse speedups.

**Goal:** distinguish routing from rank restriction. **How:** include shared S8 and S12 controls, with81,920 and122,880 trainable parameters respectively, padded by frozen zero slots for dense rank16 execution. Compare U8/8 with S8 and H8/4/4 with S12 as supporting controls. These comparisons match active rank, not stored trainable parameters. No design simultaneously matches storage, active rank and genuine sparse compute across all three architectures without changing the question.

**Goal:** retain the shared-update connection. **How:** train all arms on exactly the same paired old/new batches from the same acquired-old state; report old/new CE, accuracy, correct-versus-opposite rule margin, candidate mass and within-candidate CE. A small optional same-state finite-step reader measures source-to-recipient loss changes. It explains immediate consequences but cannot replace the joint-training utility comparison. The precise candidate procedure and proposed settings are owned by the [E04 Protocol](../../../../experiments/A17/17_04_conditional_mapping_transfer/A17_04_E04_shared_routed_budget/protocol.md).

## 6. Minimal Falsification Tests

Define \(Q_{\min}\) as the minimum full-vocabulary accuracy over two modes, two commands and two unseen DEV panels. Each of the eight cells has200 answers. This avoids a high average hiding failure of one conditional rule. The **AI-proposed** fixed-budget endpoint is240 updates, or4,800 supervised answers.

Proposed support for a routed arm requires: every seed reaches \(Q_{\min}\ge95\%\); its paired mean gain over S16 is at least5 percentage points with positive gains in all three seeds; neither old nor new combined accuracy loses more than1 point; and the same improvement/non-regression test holds against its active-rank shared control. These thresholds make benefit substantial and require both tasks to work; they are reporting conventions, not a significance test. CE and margin show whether the benefit concerns rule selection and expose tradeoffs, rather than rescuing a failed primary comparison.

No qualifying gain, including a shared ceiling result, gives no support for separation at this budget. A routed-only failure weakens this allocation. If all designs fail learning qualification even at the planned terminal budget, or freeze/data/compute checks fail, architecture utility remains insufficient or the affected comparison is ineligible. Lower-rank shared controls matching the routed gains preserve the rank/optimization rival. Three seeds share one old acquisition; DEV is already exposed diagnostic data.

## 7. Current Evidence

The [parent R02 Summary](../../../../experiments/A17/17_04_conditional_mapping_transfer/A17_04_E01_consistent_reversed_mapping/rounds/R02_single_layer_adamw/summary.md) reports old accuracy0% after reversed-only continuation and near-perfect new learning. Joint supervision achieves mean old99.833% and new99.667%, establishing coexistence in one shared carrier with different supervision/exposure. This does not show that a routed design is better.

Parameter interventions show that Q/K/V/O changes affect predictions and interact. Spectral similarity did not identify a stable functional partition; the [R04 Summary](../../../../experiments/A17/17_04_conditional_mapping_transfer/A17_04_E01_consistent_reversed_mapping/rounds/R04_o_spectral_geometry/summary.md) preserves that descriptive boundary. Consequently this draft uses explicit allocation rather than treating SVD directions as experts. The number16 is a proposed capacity unit, not the previously measured top16 singular directions. This low-rank family has not yet been qualified. Formal E04 utility comparison: **NOT RUN**. The subsequently authorized Smoke and one-seed acquisition checks completed; [qualification Summary](../../../../experiments/A17/17_04_conditional_mapping_transfer/A17_04_E04_shared_routed_budget/summary.md) owns their facts. This availability does not accept a mechanism or close the sharing decision.

## 8. Claim Boundary And Next Decision

The possible bounded claim is that known-mode allocation is worth using for this reversed-mapping task at a specified budget. It cannot establish that experts are necessary, that private slots implement unique semantics, that shared slots contain common functions, that routing can be learned from unlabeled natural inputs, or that a feed-forward MoE will benefit. The smallest elegant implementation is a frozen shared base plus masked trainable increments; a trainable shared increment in the hybrid is distinct from the frozen base.

The next decision is whether actual Smoke and single-seed acquisition qualification warrant a formal multi-seed comparison. Current completion requires five qualified implementations, matched exposure and actual learning readouts, not a utility verdict. The Protocol now permits one reserved four-H100 engineering/acquisition job; no formal comparison submission or optional mechanism interventions are authorized. Resume the held formal decision only after reporting qualification. Parent mechanism acceptance and question closure remain Unknown.
