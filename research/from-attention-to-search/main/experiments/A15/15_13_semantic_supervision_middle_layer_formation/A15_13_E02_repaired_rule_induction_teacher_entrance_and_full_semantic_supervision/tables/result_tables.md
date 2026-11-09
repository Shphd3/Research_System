# A15_13_E02 / E02-R Result Tables

Source aggregate: `/data/250010109/MoE_Router/experiments/20260830_a15_13_semantic_supervision_hierarchical_experts/runs/e02r-full-20260831T000800Z/stage2/results/aggregate.json`  
Aggregate SHA-256: `df507efaaab6f0e4773567ac47d4d55b68ccc5998dc0ae394b33efae3e11fb0f`

## Teacher Entrance

The entrance values below come from the immutable E02-R `teacher_gate.json`, which is the gate that authorized TEST unsealing and stage two.

| Teacher | Seed | DEV-ID answer accuracy | DEV-OOD answer accuracy | h3 parent balanced accuracy | Raw h2 conditional-fine q05 | Gate |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| Behavior-distilled, non-truth | 1701 | 0.999500 | 0.990250 | 0.987250 | -0.022320 | PASS |
| Behavior-distilled, non-truth | 2903 | 0.999500 | 0.973750 | 0.960500 | -0.032541 | PASS |
| Oracle coefficient control | 1701 | 0.998750 | 0.990625 | 0.988125 | -0.022320 | PASS, non-selectable |
| Oracle coefficient control | 2903 | 0.999375 | 0.976875 | 0.966000 | -0.117619 | PASS, non-selectable |

## Search-Label Entrance

| Seed | Paraphrase consistency | Bootstrap stability | Four leaf fractions | Post-freeze TEST-OOD leaf alignment | Entrance |
| ---: | ---: | ---: | --- | ---: | --- |
| 1701 | 0.981960 | 0.357330 | 0.2403 / 0.2724 / 0.2722 / 0.2151 | 0.2624 Hungarian accuracy; AMI 0.0011 | FAIL |
| 2903 | 0.984070 | 0.812511 | 0.2715 / 0.2468 / 0.2711 / 0.2106 | 0.2613 Hungarian accuracy; AMI 0.0003 | PASS |

The registered Search entrance requires both seeds to pass; its aggregate status is therefore `INSUFFICIENT`. The alignment values were computed only after the partition was frozen and did not select the partition.

## Registered Second-Stage Contrasts

The primary quantity is treatment minus control in the worse-parent TEST-OOD fifth-percentile normalized fine margin. Positive is better. The interval is a paired complete-paraphrase-group bootstrap with 2,000 draws and equal seed pooling.

| Link | Control -> treatment | Pooled delta | 95% interval | Seed 1701 | Seed 2903 | Language guard | Registered status |
| --- | --- | ---: | --- | ---: | ---: | --- | --- |
| Oracle semantic supervision | B1 -> O-F | -0.000046 | [-0.000333, 0.000171] | +0.000640 | -0.001227 | PASS | INSUFFICIENT |
| Search supervision | B1 -> S-F | +0.000488 | [+0.000247, +0.000704] | +0.000776 | +0.000721 | PASS | Geometrically stable positive; semantic interpretation ineligible because Search entrance failed |
| Oracle hierarchy | O-F -> O-HF | +0.001162 | [+0.000857, +0.001477] | +0.002382 | -0.000599 | PASS | INSUFFICIENT |
| Search hierarchy | S-F -> S-HF | +0.002245 | [+0.001916, +0.002584] | +0.003947 | -0.001231 | PASS | INSUFFICIENT |
| Oracle coarse-removal residual | O-HF -> O-HR | -0.000815 | [-0.001115, -0.000514] | +0.000926 | -0.003065 | PASS | INSUFFICIENT |
| Search coarse-removal residual | S-HF -> S-HR | +0.000002 | [-0.000105, +0.000105] | -0.000102 | +0.000208 | PASS | INSUFFICIENT |
| Oracle label specificity | O-S -> O-HR | -0.001004 | [-0.001420, -0.000614] | +0.001993 | -0.006047 | PASS | INSUFFICIENT |
| Search label specificity | S-S -> S-HR | +0.002042 | [+0.001762, +0.002256] | +0.003344 | -0.000098 | PASS | INSUFFICIENT |

## Absolute Primary Values By Condition

All values remain below zero, so no condition made the fifth-percentile difficult tail linearly separated under this metric.

| Condition | Label source | Architecture | Pooled primary q05 | Seed 1701 | Seed 2903 |
| --- | --- | --- | ---: | ---: | ---: |
| T0 | none | teacher | -0.039297 | -0.043021 | -0.033510 |
| B0 | none | dense | -0.039379 | -0.043168 | -0.033542 |
| B1 | none | flat | -0.039885 | -0.043788 | -0.034242 |
| O-F | Oracle | flat | -0.039931 | -0.043149 | -0.035469 |
| O-HF | Oracle | hierarchical full-state | -0.038770 | -0.040767 | -0.036069 |
| O-HR | Oracle | hierarchical residual Gate | -0.039585 | -0.039841 | -0.039134 |
| O-S | shuffled Oracle | hierarchical residual Gate | -0.038581 | -0.041834 | -0.033087 |
| S-F | Search | flat | -0.039397 | -0.043012 | -0.033521 |
| S-HF | Search | hierarchical full-state | -0.037153 | -0.039065 | -0.034752 |
| S-HR | Search | hierarchical residual Gate | -0.037150 | -0.039167 | -0.034544 |
| S-S | shuffled Search | hierarchical residual Gate | -0.039192 | -0.042512 | -0.034446 |
| L1-SEQ | Search | layer-one sequential extension | -0.038186 | -0.040290 | -0.035634 |
| L1-JOINT | Search | layer-one joint extension | -0.040548 | -0.043027 | -0.036536 |

