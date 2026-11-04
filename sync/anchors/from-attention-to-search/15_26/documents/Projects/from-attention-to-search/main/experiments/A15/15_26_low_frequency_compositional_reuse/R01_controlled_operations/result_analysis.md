派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_26_low_frequency_compositional_reuse/R01_controlled_operations/result_analysis.md`。
[精确原始文件](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_26_low_frequency_compositional_reuse/R01_controlled_operations/result_analysis.md)；研究修改仍回到原件。

---

# R01 result analysis

This record explains measured comparisons. Belief revision is a separate step. [Detailed](detailed.md) owns the full evidence chain.

## Atomic access

| Seed | Parent | Original atomic | Changed format | F0–F3 / G0–G3 | 95% each |
| --- | --- | --- | --- | --- | --- |
| 29 | P | 100.00% | 33.98% | 31.25%, 37.50%, 31.25%, 15.63%, 62.50%, 21.88%, 18.75%, 53.13% | False |
| 29 | C | 100.00% | 26.17% | 18.75%, 46.88%, 21.88%, 12.50%, 40.63%, 28.13%, 28.13%, 12.50% | False |
| 43 | P | 100.00% | 36.72% | 46.88%, 56.25%, 28.13%, 18.75%, 62.50%, 34.38%, 9.38%, 37.50% | False |
| 43 | C | 100.00% | 24.22% | 25.00%, 34.38%, 18.75%, 6.25%, 50.00%, 25.00%, 12.50%, 21.88% | False |
| 71 | P | 100.00% | 38.28% | 31.25%, 46.88%, 28.13%, 31.25%, 53.13%, 28.13%, 25.00%, 62.50% | False |
| 71 | C | 100.00% | 21.09% | 12.50%, 34.38%, 12.50%, 6.25%, 34.38%, 28.13%, 25.00%, 15.63% | False |

Original-format fitting and cross-format callable competence differ. Explicit two-call composition succeeds100%, demonstrating composition through the external interface for measured atomic maps. It does not demonstrate a single-forward internal interface: both calls/compute and intermediate access change.

## Learning help

| Seed | P TEST | B TEST | C TEST | P−B (pp) | P−C (pp) | VAL AUC P−B / P−C (pp) |
| --- | --- | --- | --- | --- | --- | --- |
| 29 | 4.17% | 3.13% | 4.17% | +1.04 | +0.00 | +1.09 / +1.76 |
| 43 | 3.13% | 4.17% | 1.04% | -1.04 | +2.08 | -2.20 / -0.17 |
| 71 | 4.17% | 2.08% | 1.04% | +2.08 | +3.13 | -1.44 / -0.89 |

The registered prediction requires at least5pp P advantage over both B/C, consistent direction across seeds, with VAL AUC reported. VAL AUC differences against both controls also vary in sign across seeds. [Paired intervals](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_26_low_frequency_compositional_reuse/R01_controlled_operations/tables/help.csv) remain conditional on this fixed task. P-U original-format atomic accuracy after composition is 8.98%, 6.64%, 10.94%, despite100% composition TRAIN. Composition training has no atomic rehearsal; lost behavior does not prove that all component computation vanished. Training fit cannot replace held-out accuracy. Failed atomic-format guards restrict interpretation as help from already callable components. C may induce negative transfer, so P−C alone is insufficient. Near1/32 accuracy is a descriptive reference, not proof of random guessing under unrestricted full-vocabulary output.

## Controlled exposure

| Seed | High−low same-pair exposure (pp) | 98.333% conditional interval (pp) |
| --- | --- | --- |
| 29 | -2.08 | [-7.29, +2.08] |
| 43 | +0.00 | [-5.21, +5.21] |
| 71 | -1.04 | [-4.17, +0.00] |

Positive differences mean the same pair performs better under high exposure; none reaches the registered positive5pp effect.5000 input-symbol-cluster bootstrap draws provide98.333% conditional primary intervals. Operation tables, split and parent trajectories are fixed; these intervals do not cover new task worlds. A reporting-time audit additionally finds skew/swap differences in74/128 F–input and84/128 G–intermediate cells, up to448 targets. Specific component-map practice is not held fixed. [Joint-exposure audit](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_26_low_frequency_compositional_reuse/R01_controlled_operations/provenance/joint_exposure_audit.json) narrows interpretation without changing frozen data. Weak composition competence prevents extending these effects to qualified reuse or general frequency claims.

## Freezing and capacity

| Seed | Exposure | F TRAIN | F TEST | J TEST | F−J (pp) | F atomic-format |
| --- | --- | --- | --- | --- | --- | --- |
| 29 | balanced | 18.13% | 2.08% | 6.25% | -4.17 | 8.98% |
| 29 | skew | 32.81% | 2.08% | 3.13% | -1.04 | 9.38% |
| 29 | swap | 28.13% | 6.25% | 1.04% | +5.21 | 7.42% |
| 43 | balanced | 19.69% | 2.08% | 2.08% | +0.00 | 12.11% |
| 43 | skew | 31.56% | 0.00% | 1.04% | -1.04 | 13.67% |
| 43 | swap | 25.94% | 5.21% | 1.04% | +4.17 | 8.98% |
| 71 | balanced | 20.00% | 2.08% | 4.17% | -2.08 | 9.38% |
| 71 | skew | 34.06% | 1.04% | 2.08% | -1.04 | 10.16% |
| 71 | swap | 28.75% | 4.17% | 3.13% | +1.04 | 10.94% |

F trains only a rank32 adapter; J adds the identical adapter and updates the final block. Training failure triggers the single prespecified capacity check:

| Case | TRAIN | TEST | Atomic-format |
| --- | --- | --- | --- |
| capacity128/P_29_balanced_F | 67.50% | 6.25% | 5.86% |
| capacity128/P_29_balanced_J | 100.00% | 4.17% | 4.30% |
| capacity128/P_43_balanced_F | 75.94% | 2.08% | 10.94% |
| capacity128/P_43_balanced_J | 100.00% | 2.08% | 4.30% |
| capacity128/P_71_balanced_F | 75.94% | 2.08% | 6.64% |
| capacity128/P_71_balanced_J | 100.00% | 3.13% | 4.30% |

Rank128 F TRAIN rises to67.50%/75.94%/75.94%, while TEST is6.25%/2.08%/2.08%: wider capacity improves fitting without qualifying generalization. Despite frozen parent weights, rank32 F original-format atomic accuracy falls to28.52%/35.16%/32.42%. An adapter changes the whole prediction path; fixed old weights do not guarantee retained behavior. Rank128 does not replace the primary results. Parent competence, interface, structure, capacity and learning route remain possible limitations. Small F/J differences do not establish2pp equivalence with96 TEST rows. [Freeze intervals](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_26_low_frequency_compositional_reuse/R01_controlled_operations/tables/freeze.csv).

## Revision and state tests

All18 edit/sham pairs are in [revisions.csv](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_26_low_frequency_compositional_reuse/R01_controlled_operations/tables/revisions.csv). Edits change F0 or G0 atomic labels with other-operation rehearsal, without composition teaching. Sham shares inputs/order and keeps old labels. Every baseline fails competence, so local effects or nulls cannot adjudicate functional reuse.

| Seed | Selected site/rank | Native TEST | Retained atomic | Directed new answer | Random range | No-op original | Eligible |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 29 | attention/8 | 4.17% | 6.25% | 1.04% | 1.04%–2.08% | 4.17% | False |
| 43 | attention/8 | 3.13% | 3.52% | 4.17% | 2.08%–3.13% | 3.13% | False |
| 71 | attention/8 | 4.17% | 3.91% | 3.13% | 2.08%–3.13% | 4.17% | False |

Donors/bases come from pre-composition atomic P. VAL selects attention rank8/16; TEST is locked. Same-intermediate, other surface, no-op, five equal-rank/equal-norm random directions, half dose, late-state and removal tests all execute. Late-state replacement may transport an answer and is diagnostic only. No-op fidelity is measurement quality, not a repair for failed native competence. Only final-block candidates are tested; earlier or distributed carriers remain unmeasured.

The measured failure is access/held-out composition in this setup. An eligible starting point for distinguishing internal reuse from whole-pair mapping learning was not obtained. See separate [causal conjectures](mechanism_conjectures.md) and [recognition update](recognition_update.md).
