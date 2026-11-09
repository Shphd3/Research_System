---
anchor_id: 15_08_09_random_projection_router_preservation
status: SUCCESSOR_COMPUTATION_COMPLETE_AWAITING_HUMAN_H1_AND_JUDGMENT
parent_anchor: ../15_08_target_conditioned_layer_innovation_anchor.md
depends_on:
  - 15_08_07_semantic_conditioned_functional_subspace_anchor.md
protocol: ../../../../experiments/A15/15_08_target_conditioned_layer_innovation/A15_08_09_E02_qwen30b_all_layer_gain_and_preservation/protocol.md
predecessor_protocol: ../../../../experiments/A15/15_08_target_conditioned_layer_innovation/A15_08_09_E01_random_projection_router_preservation/protocol.md
created: 2026-08-24
updated: 2026-08-24
---

# A15_08_09: Random-Projection Preservation Of Full-Update Linear Structure

## 1. Problem Definition

For a frozen pretrained model and a registered decision token, let \(h_\ell\) be the residual stream entering block \(\ell\), \(a_\ell\) the attention output after its output projection and before residual addition, and \(N_\ell\) the block's post-attention RMSNorm. Define

\[
X_\ell=N_\ell(h_\ell),\qquad
Z_\ell=N_\ell(h_\ell+a_\ell),\qquad
U_\ell=Z_\ell-X_\ell,
\]

and the TRAIN-fitted linearly unpredictable update candidate

\[
R_{U,\ell}=U_\ell-(X_\ell\widehat B_\ell+\widehat b_\ell).
\]

The one decision question is:

> Does full-space \(R_U\) already contain stable positive-margin linear label structure, and, conditional on that gate, can an independent dense Gaussian projection preserve the frozen Router at \(m\ll d\)?

The task label is a controlled semantic class. It is a proxy used to test a linear decision geometry, not a model-native expert-utility target. “Router” below therefore means the registered linear probe only.

## 2. Physical Priors

1. A fixed common component cancels in pairwise differences and cannot by itself create class separation.
2. Bounded sample-specific perturbations can shrink a pre-existing gap but do not justify assuming a gap.
3. Dense Gaussian projections preserve finite sets of fixed vectors and inner products with high probability when \(m\) is large enough.
4. Projection after a failed full-space linear gate is logically irrelevant: a linear projection followed by a linear classifier is still a linear classifier in the original space.

## 3. Falsifiable Hypotheses

- **H0 — model-local layer localization:** on Qwen3-30B-A3B, at least one layer has positive simultaneous-interval lower bound for the DEV added-utility excess of \(R_U\) beyond same-layer \(X\), after duplicate-\(X\) and mismatched-\(R_U\) controls. Separately, a TRAIN/DEV-only rule freezes the layers used by H2/H3.
- **H1 — data validity:** the frozen 64-class taxonomy is expressed through split-isolated semantic seeds without direct labels, near duplicates, formula-instance overlap, or a near-saturating bag-of-words shortcut.
- **H2 — full-space accessibility:** the registered full-space L2 multinomial probe is stably above chance on same-template and unseen-template tests.
- **H3 — positive-margin admission:** on both tests, the 5th percentile true-label margin has a positive 95% lower confidence bound and balanced-accuracy lower bound at least 0.90. This is the hard gate.
- **H4 — conditional preservation:** only after H3 passes, some \(m\le d/8\) preserves the frozen Router under the registered NMR, accuracy-retention, and decision-agreement criteria.

Failure of H3 rejects this experiment's preservation premise for the registered object and probe; it does not prove that every linear subspace or nonlinear readout is uninformative.

## 4. Mathematical Model

For frozen full-space class scores

\[
s_k(r)=w_k^\top r+b_k,
\]

define the true-label margin

\[
\gamma_i^{\mathrm{full}}
=s_{y_i}(r_i)-\max_{k\ne y_i}s_k(r_i),\qquad
\Gamma_{0.05}^{\mathrm{full}}=Q_{0.05}(\gamma_i^{\mathrm{full}}).
\]

After H3, independently draw \(R\in\mathbb R^{m\times d}\) with \(R_{ab}\sim\mathcal N(0,1/m)\), set \(z_i=Rr_i\), and use the theorem-aligned frozen projected weights \(\widetilde w_k=Rw_k\) with the original bias. The primary preservation metric is

\[
\operatorname{NMR}(m,R)=
\frac{Q_{0.05}(\widetilde\gamma_i^{(m,R)})}
{\Gamma_{0.05}^{\mathrm{full}}},
\]

which is defined only when H3 has established a positive denominator. Accuracy retention is chance corrected:

\[
\operatorname{AR}(m,R)=
\frac{A_{m,R}-1/K}{A_{\mathrm{full}}-1/K}.
\]

Theory establishes only a sufficient finite-set preservation mechanism. It neither predicts the smallest empirical \(m\) tightly nor creates separability.

## 5. Computational Realization

- Frozen model: `/data/share/Qwen3-30B-A3B`, BF16, eval mode, no generation or parameter update.
- Layer localization: scan all 48 blocks. On TRAIN fit a ridge base score from \(X\) and an additive ridge correction from \(R_U\); on DEV compute cross-entropy reduction relative to duplicate-\(X\) and label-breaking mismatched-\(R_U\) controls with a simultaneous 95% lower interval. In parallel, compute the DEV 5th-percentile true-label margin of a standalone ridge readout from \(R_U\).
- Frozen layers: among positive-excess layers, choose the largest DEV standalone low-tail margin as primary; choose the best remaining layer at least four blocks away as replication. If no layer has positive excess, apply the same margin rule over all layers and label H0 `Fail`; this fallback cannot convert H0 to Pass. TEST is forbidden in localization.
- Data: the exact prior 8-by-8 taxonomy frozen by receipt; 300 rows per fine class, split 180/40/40/40 into TRAIN/DEV/same-template TEST/new-template TEST.
- Representation: the last token of the common `Answer:` suffix; TRAIN-fitted ridge residualizer, DEV-selected regularization, TRAIN-only standardization.
- Probe: one L2 multinomial-logistic family, five fixed seeds, DEV-selected regularization.
- Projection: \(m\in\{8,16,32,64,128,256,512,1024\}\) with \(m<d\), 30 independent Gaussian seeds per dimension, sampled only after the full-space Router is frozen.
- Execution: one reserved ACP worker with four 80-GB H100 GPUs; four replicated model processes shard the examples.

Random spectral-coordinate sampling and supervised functional rank are diagnostics. Spectral uniformity is not an assumption of the dense-Gaussian main claim.

## 6. Minimal Falsification Tests

1. **Layer-localization gate:** scan all 48 blocks using TRAIN/DEV only, publish the full added-utility curve and freeze primary/replication layers before TEST.
2. **Data/full-space gate:** retain the exact taxonomy, split, leakage, bag-of-words, review, identity, label-permutation, common-offset, replay, and \(U=Z-X\) guards; then evaluate H2/H3 on both TEST panels.
3. **Conditional projection gate:** if and only if the frozen primary layer passes H3, scan the frozen dimensions and report the smallest passing \(m_*\) or a registered Fail/Insufficient verdict.

## 7. Current Evidence

The final binding-controlled 19,200-row build passes every machine data guard and reduces the raw-text TEST-same/TEST-new bag-of-words baseline to 0.1270/0.1195. Independent human review of its 64-row pack remains unresolved, so overall H1 remains `Insufficient`.

E01 remains immutable evidence for historical blocks 24/28: both pass H2, fail H3, and make H4 ineligible. E02 removes the unsupported transfer of those layer numbers to Qwen3-30B-A3B by extracting all 48 blocks and selecting without TEST labels.

E02 H0 passes. Thirty-one of 48 blocks have a familywise simultaneous lower bound above zero for controlled incremental DEV utility of \(R_U\) beyond \(X\). Block 39 has the largest excess, 0.10994 nats/example with simultaneous interval [0.09872, 0.12080]. This establishes that \(R_U\) is not information-free.

The downstream selector freezes block 48 as the H3 primary because it has the least-negative standalone DEV low-tail margin among H0-admitted layers, and block 38 as the separated replication. Block 48 is H2 `Fail`, H3 `Fail`: TEST-same/new accuracy is 0.17125/0.12969 and margin \(Q_{.05}\) is -5.82955/-11.19046. Block 38 is H2 `Pass` but H3 `Fail`: accuracy 0.31016/0.23125 and margin -3.52356/-6.66276. All four margin intervals are wholly negative. Primary H4 is therefore `SKIPPED_H3_NOT_PASS`.

Exact enumeration of all 3,275,520 unordered pairs per TEST panel yields extreme \(D_{out}/D_{in}\) between 0.2027 and 0.3321 at the selected layers; robust ratios are 0.5315--0.7026. TRAIN-supervised orthogonal fine-label learning gives \(r_{90}=64\) at both blocks. Spectral-coordinate theorem bounds are 83,892/114,975 for blocks 48/38 and exceed the registered maximum 1,024. These diagnostics agree with the absent standalone routing geometry but cannot change H0--H4.

## 8. Claim Boundary And Next Decision

A positive result can establish only that an already-trained Qwen3-30B-A3B representation, at a registered layer and token on the registered distribution, exposes a stable linear semantic decision that an independent dense Gaussian map preserves for a fixed probe. It cannot establish expert utility, learned routing quality, causal specialization, nonlinear novelty, intrinsic semantic rank, or distribution-free preservation.

The bounded result is: \(R_U\) exposes controlled incremental information conditional on same-layer \(X\), but the selected standalone \(R_U\) spaces do not satisfy the stable positive-margin object required by the preservation theorem. E02 therefore does not test Gaussian preservation under a satisfied premise and does not prove that joint \((X,R_U)\), another learned linear representation, or a nonlinear Router is impossible.

The one proposed next decision is to open a representation-space-learning anchor, subject to human confirmation of the result wording and closure of the independent H1 review. Its minimal falsifier should compare a learned standalone routing representation with a joint \((X,R_U)\) baseline on genuinely held-out data and require a positive low-tail margin before any compression study. Do not reopen this preservation branch by changing layers, probes, thresholds, or the taxonomy.
