# Exact-33B finite routing: matching information without benefit over the strong fixed action

2026-10-04. [中文](probe_33b_summary_cn.md) · [Detailed record](probe_33b_detailed.md) · [Stage report](sharing_routing_report.md). Execution and numerical analysis are complete; scientific judgment and the practical-effect threshold remain `Unknown`.

## Purpose

Candidates here are increments of a frozen model's final projection matrix, called update “actions”: four raw domain mean gradients are scaled separately, and pooling them before scaling constructs the common update. They never change during evaluation, defining a frozen candidate library. FIT supplies fitting supervision and chooses one candidate for every DEV position, defining fixed selection; an input-dependent selector predicts and chooses per position. These are not trained experts.

Test whether information available before the target converts differences between source updates into useful action selection, as a local fixed-state test within the broader question of learning acquisition and retention under finite resources.

## Hypothesis

Pre-target representations may reveal relative action utility and improve selection over a strong fixed action. The rival is that useful matching information exists, but a pooled common action is already better than the fitted policy.

## Analysis Method

The manipulated objects are increments of the frozen language model's final attention output matrix \(W\), not five trained experts. Compute one raw mean gradient \(M_d\) per source domain and then their equal-weight mean \(M_{\rm common}\). Normalize each direction separately:

\[
\Delta W_a=-0.001\|W\|_F M_a/\|M_a\|_F.
\]

Both matrices have shape 1024×2048; the Frobenius norm is the square root of the sum of all squared entries. Equal parameter-increment norms do not imply equal activation displacements or losses on a recipient. The pooled direction constructs the **common update**, called `common action` in result fields. All candidates remain unchanged during evaluation: this is a **frozen candidate library**, a learning-status statement distinct from a selection rule.

FIT contains 512 fitting records: measured finite loss changes for each candidate supervise a ridge predictor of those changes from information available before the target. Only predictor coefficients are learned; the LM and increments remain unchanged. The selector takes the candidate with the lowest predicted cost at each position. Separately, FIT's measured mean costs choose one candidate for every position in 1024 DEV evaluation records: **fixed selection**. Here it chooses the common update, but “common” describes construction and “fixed” describes selection. Each DEV record contributes 16 positions; previously exposed DEV is exploratory. A/B are two source-record banks, each constructing the same five candidate types. A→B fits/selects from A and scores the corresponding B-bank candidate; A/B are not domains.

- Freeze Dense, fresh S7 and SALL at exactly 33 billion training tokens. These are existing dense backbones with different SAE training histories; 33B is not parameter count, and no MoE is trained here.
- Fit the frozen ridge recipe and select the fixed action using 512 FIT records only. Evaluate 1024 DEV records with 16 positions each. Retain every registered family, A→B/B→A transfer direction and both action sets, with or without no-update. Dense omits SAE features.
- Compare against the FIT-fixed action, uniform allocation, and random allocation preserving the policy's **global** action frequencies. The latter does not control domain/category composition. Use 2000 category-stratified paired whole-record bootstrap draws. Intervals condition on checkpoints, source banks and fitted models, without multiplicity correction.

Record identities and exact token strings are disjoint; article, near-duplicate and pretraining overlap remain unknown. DEV is for exploratory method evaluation, not independent confirmation.

The controls answer different questions. Globally usage-matched random allocation preserves the policy's candidate proportions while removing their correspondence with inputs; it tests matching but leaves domain/category composition uncontrolled. FIT-fixed selection asks whether input-dependent switching is worth adopting over one strong candidate everywhere. The zero update, \(\Delta W=0\), supplies the original-model reference and is selectable in a separate candidate set. Pre-target information includes only the currently visible prefix and its model state: the true next token supplies fitting supervision and retrospective scores, not DEV selection input.

## Conclusion

1. **Input-dependent switching lowers loss relative to usage-matched random allocation, but has higher loss than using the FIT-selected common update everywhere.** All 92 pooled cross-source conditions beat global-frequency random allocation and lose to the FIT-fixed action, with their pointwise conditional 95% intervals on the respective sides of zero. FIT selects the common action for both banks and action sets. The table shows point-estimate ranges over all conditions, in micro-nats per selected event; positive favors the policy. Ranges are not pooled confidence intervals.

   | Model | Conditions | Gain over FIT-fixed common | Gain over global-frequency random |
   |---|---:|---:|---:|
   | Dense | 28 | −504.84 to −198.21 | +133.49 to +386.63 |
   | fresh S7 | 32 | −807.31 to −345.56 | +240.43 to +759.55 |
   | SALL | 32 | −514.85 to −191.92 | +157.86 to +422.75 |

   The [complete 92-condition table](evidence/probe_33b_pooled_cross_source.csv) retains every interval. These are not 92 independent replications. None of the 368 individual-domain conditions has a positive fixed-baseline gain estimate either, although some intervals cross zero.

2. **Matching benefit and benefit from replacing the common action differ.** Gain over fixed equals gain over frequency-random allocation minus the excess loss of that random mixture over fixed. The matching gain is smaller than that excess loss in all 92 conditions. This is a post-hoc accounting identity, not a discovered training mechanism. [Check](evidence/probe_33b_gain_accounting.json)

3. **The negative utility result bounds these policies, not separate learning in general.** The common direction is constructed from the balanced pooled objective. Its advantage is not evidence of universal shared knowledge. A target-informed oracle is not an attainable pre-target selector, and differences between compressed and full-input ridge predictors do not establish information sufficiency or an SAE mechanism. Parameter tying, long-term acquisition and retention still require trajectory evidence.

![Two comparator gains for every cross-source condition](figures/probe_33b_fixed_vs_marginal.png)

Left: FIT-fixed common action; right: global-frequency random allocation. Rightward favors the policy, and axis ranges differ between models. Blue/orange distinguish transfer direction; circles/squares distinguish the action sets. Every left interval is negative and every right interval positive. This is not an architectural causal comparison.

The full matrix contains 920 DEV and 1840 descriptive source rows. A separately implemented calculation checked 235,980 means and interval endpoints, with maximum absolute discrepancy about 1.74×10⁻¹⁸. It imported no producer module, performed no refits and made no new LM forwards. [Audit](evidence/probe_33b_independent_audit.json). Numerical verification does not add independent data or confirmation status.

**AI recommendation:** preserve the negative fixed-bank utility result and complete the already designed shared/private training comparison, reading acquisition, retention and resources separately. New training submissions and scientific state changes retain their respective authorization boundaries.
