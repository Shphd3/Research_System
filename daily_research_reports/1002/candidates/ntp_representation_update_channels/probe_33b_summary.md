# Exact-33B finite routing: matching information without benefit over the strong fixed action

2026-10-04. [中文](probe_33b_summary_cn.md) · [Detailed record](probe_33b_detailed.md) · [Stage report](sharing_routing_report.md). Execution and numerical analysis are complete; scientific judgment and the practical-effect threshold remain `Unknown`.

## Purpose

Test whether information available before the target converts differences between source updates into useful action selection, as a local fixed-state test within the broader question of learning acquisition and retention under finite resources.

## Hypothesis

Pre-target representations may reveal relative action utility and improve selection over a strong fixed action. The rival is that useful matching information exists, but a pooled common action is already better than the fitted policy.

## Analysis Method

- Freeze Dense, fresh S7 and SALL at exactly 33 billion training tokens. These are existing dense backbones with different SAE training histories; 33B is not parameter count, and no MoE is trained here.
- Construct two disjoint source banks, A/B. Each provides four domain-average gradients and one mean raw gradient. Normalize each of the five directions separately to 0.001 of the original matrix Frobenius norm, and measure actual finite CE through the native model tail.
- Fit the frozen ridge recipe and select the fixed action using 512 FIT records only. Evaluate 1024 DEV records with 16 positions each. Retain every registered family, A→B/B→A transfer direction and both action sets, with or without no-update. Dense omits SAE features.
- Compare against the FIT-fixed action, uniform allocation, and random allocation preserving the policy's **global** action frequencies. The latter does not control domain/category composition. Use 2000 category-stratified paired whole-record bootstrap draws. Intervals condition on checkpoints, source banks and fitted models, without multiplicity correction.

Record identities and exact token strings are disjoint; article, near-duplicate and pretraining overlap remain unknown. DEV is for exploratory method evaluation, not independent confirmation.

## Conclusion

1. **The policies exploit matching information but lose to the strong common action.** All 92 pooled cross-source conditions beat global-frequency random allocation and lose to the FIT-fixed action, with their pointwise conditional 95% intervals on the respective sides of zero. FIT selects the common action for both banks and action sets. The table shows point-estimate ranges over all conditions, in micro-nats per selected event; positive favors the policy. Ranges are not pooled confidence intervals.

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
