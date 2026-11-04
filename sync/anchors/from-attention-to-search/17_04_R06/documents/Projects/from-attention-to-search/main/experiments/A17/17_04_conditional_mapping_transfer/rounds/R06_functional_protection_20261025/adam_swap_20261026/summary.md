派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A17/17_04_conditional_mapping_transfer/rounds/R06_functional_protection_20261025/adam_swap_20261026/summary.md`。
[精确原始文件](../../../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A17/17_04_conditional_mapping_transfer/rounds/R06_functional_protection_20261025/adam_swap_20261026/summary.md)；研究修改仍回到原件。

---

# R06 step120 parameter × Adam-moment exchange

**Bounded result:** accumulated Adam state contributes to the local old-task disadvantage, with parameter-dependent effects. This is not a causal decomposition of the full training history.

A17 contains two compatible, mode-conditioned list rules. At the saved step120 of U/F 1:9 continuations (seeds29/43/71), we crossed U/F parameters with U/F named Adam first/second moments. Every cell used three prespecified TRAIN batches independently from step120:36new+4activeold,72slots,denominator72; one ordinary Adam update, no F projection. We evaluated64fixed old DEV and64paired new DEV items before/after. Three continuation orders share one old model.

| Parameter source | Adam moment source | Old one-step CE change | New one-step CE change |
|---|---|---:|---:|
| U | U | -0.037998 | -0.000494 |
| U | F | +0.020924 | -0.022451 |
| F | U | -0.052743 | -0.006555 |
| F | F | +0.077850 | -0.011939 |

Table: equal mean of9seed-batch contexts; CE change is after−before in nats/answer, negative is favorable. No confidence intervals implied.

At fixed F parameters, replacing F moments with U moments improves old CE change in9/9contexts (mean0.130592), although2updates still increase old CE. New CE change worsens in6/9 (mean0.005384 cost), improves in3/9. At U parameters, F rather than U moments worsens old CE change8/9 but improves new CE9/9. At fixed U moments, the F−U parameter effect has5favorable/4unfavorable old outcomes; at F moments,2/7. Old interaction differences are positive for all batches of seeds29/71 and negative for all batches of43. A universal additive attribution is unsupported.

All6native first batches exactly reproduced the previous unprojected d4 CE readouts before hybrids. Full name mapping is reconstructed from verified frozen producer code and actual parameter object identities because original optimizer metadata lacks explicit parameter names. We exchanged only exp_avg/exp_avg_sq, retainingstep120/settings, verifying shape/name/group/moment hashes. Same-parameter/batch raw gradients and clipping coefficients match across moment donors. No-op CE span0; all contrasts exceed prespecified numerical precision bounds, which are not statistical significance.

Completed36independent temporary steps,10320/12000sequence forwards, all6original checkpoint hashes unchanged. No TEST, F projection, full continuation, new allocation or candidate checkpoint save. Main new DEV64 is a locked extension using old DEV pairs; previous new TRAIN36 remains replay-only. Parameter/moment hybrid states may not occur naturally in training; one-step effects do not establish long-term cause or benefit. First versus second moments and direction versus scale contributions remain unresolved. AI suggestion only: separate first/second-moment exchange at the same states/batches; not executed.

[Chinese one-page](one_page_cn.md), [all-seed/all-batch appendix](appendix_cn.md), [frozen protocol](protocol.md), [figure](figures_cn.md).
