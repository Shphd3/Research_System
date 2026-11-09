# Summary: A15_17_E02 Gradient, Parameter, And Local-Utility Follow-Up

Primary Anchor: [A15_17](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_17_three_model_sae_representation_trajectory/15_17_three_model_sae_representation_trajectory_anchor.md)  
Frozen Protocol: [protocol.md](protocol.md)  
Detailed record: [detailed.md](detailed.md)  
Execution receipt: [execution_receipt.md](execution_receipt.md)  
Result status / eligibility: Smoke, full run, and S6 synthesis `PASS`; evidence `ELIGIBLE`; scientific verdict `AI_DRAFT_NOT_SUPPORTED_AWAITING_HUMAN_CONFIRMATION`.

## 1. Purpose

Test whether a reconstruction gradient that reaches the M2 backbone and changes a real one-step update improves frozen held-out domain readability over an otherwise matched LM-only update, while completing the registered 15B and read-only measurement gaps.

## 2. Hypothesis

If the local reconstruction-to-backbone direction is useful, the 95% paired interval for \(\mathrm{CE}(U0)-\mathrm{CE}(U1)\) should lie above zero. The strongest rival is that the path is physically real but does not improve held-out readability under this 2,048-valid-token, one-step condition.

## 3. Analysis Method

- At M2 10B (primary) and 15B (separate sensitivity), restore the same checkpoint, AdamW, scheduler, and RNG state for four fixed N-fit batches, then take one U0 LM-only or U1 LM-plus-reconstruction step with the SAE frozen.
- Freeze readouts before updating and score P report; average within each batch direction, then use 5,000 family/class-stratified paired bootstrap draws. Positive values favor U1; 15B cannot rescue 10B.
- Separately audit B/W/F, physical parameter displacement, 30,000 same-ID decoder directions, and frozen M0/M1/M2 N-report NLL through 15B.

## 4. Conclusion

Verdict: `AI_DRAFT_NOT_SUPPORTED_AWAITING_HUMAN_CONFIRMATION`.

1. The one-step local experiment does not support U1 over U0. The 10B primary value is `−0.000622 nats`, 95% CI `[−0.001691, 0.000400]`, with 2/4 positive batch directions. The 15B sensitivity is `−0.000571`, 95% CI `[−0.001664, 0.000564]`, with 1/4 positive directions. Neither interval excludes zero; this is not evidence of equivalence or harm.
2. The reconstruction path is real but local-path existence is not local utility. At the h node, reconstruction/LM gradient-norm ratios are `8.27%--10.06%` at 10B and `3.45%--5.57%` at 15B; all eight G0 batches have exact zero reconstruction gradient outside registered positions, and all 16 G1 trials retain identical SAE state.
3. The E01 Fisher increase is not within-class tightening. For P actual input at 10B, M1−M0 raw B is `+83.18 [72.78, 98.87]`, W is `+120.59 [70.99, 152.69]`, and F is `+0.2777 [0.1309, 0.3722]`; at 15B all three remain positive. Both between- and within-class energy grow.

| Registered rule | Observed value | Guard / eligibility | Verdict | Evidence source |
|---|---|---|---|---|
| 10B primary interval above zero | `−0.000622 [−0.001691, 0.000400]` | 4/4 pairs; 5,000 draws | `NOT_SUPPORTED` | [primary table](tables/primary_local_utility.csv) |
| separate 15B sensitivity | `−0.000571 [−0.001664, 0.000564]` | no pooling or checkpoint selection | `NOT_SUPPORTED` | [primary table](tables/primary_local_utility.csv) |
| G0 support / finite guards | 8/8 pass; outside-position max exactly 0 | detached target and denominator | `PASS` | [G0 table](tables/g0_h_gradient.csv) |
| G1 completion / freeze guards | 16/16 updates; SAE unchanged 16/16 | fresh state per trial | `PASS` | [G1 table](tables/g1_trial_summary.csv) |
| full Reserved execution | `pt-d6swd6xd`, `SUCCEEDED` | fresh v2 root; four H100s visible | `PASS` | [execution receipt](execution_receipt.md) |

### Important Figure

![Primary local utility at 10B and 15B](figures/primary_local_utility.png)

How to read: positive values favor the reconstruction-gradient arm; both paired intervals cross zero.

### Claim Boundary

Can claim: the registered local path exists and changes a real backbone update, but no P-report benefit was detected in this one-step condition; registered 15B parameter, direction, representation-component, and NLL supplements are complete.

Cannot claim: long-run ineffectiveness or harm, U0/U1 equivalence, single-loss attribution of historical M2−M1 differences, stable semantic identity of SAE columns, preserved general capability, or easier formation from scratch.

### Next Step Analysis

**AI recommendation:** do not use historical displacement or this one-step gradient as evidence for easier formation from scratch. If that mechanism remains a priority, the only next decision is whether to authorize a separately frozen, matched-from-zero C/T design with fixed budget, seeds, held-out functional primary metric, and stopping rule. Stop if those matching conditions cannot be guaranteed.
