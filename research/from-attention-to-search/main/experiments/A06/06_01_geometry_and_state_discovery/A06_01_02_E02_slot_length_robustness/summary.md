# Summary: A06_01_02_E02 Slot-Length Robustness Replay

Primary anchor:
`../../../../problem_anchors/06_geometry_proxy_preservation/06_01_geometry_and_state_discovery/06_01_geometry_and_state_discovery_anchor.md`

Protocol:
`protocol.md`

## Purpose

A06_01_02_E02 tests whether the A06_01_01_E05-A06_01_03_E01 initialized router-geometry sequence was an artifact of using one-token slots.

The run repeats the A06_01_01_E05-A06_01_03_E01 step-0 replay logic with `slot_token_len in {1,2,4}`. For slot lengths above 1, the current generator repeats the same `SLOT_s` token and places `TARGET_s` immediately after the slot span. Routing is read at the last slot position.

## Exact Setup

- synthetic sequence length: `32`;
- four strictly uniform `(slot,target)` pair features;
- four experts;
- `slot_token_len in {1,2,4}`;
- route position: `pair_start + slot_token_len - 1`;
- target position: `pair_start + slot_token_len`;
- random background tokens independent of pair id;
- no training, step-0 replay only;
- seeds `20260521..20260528`;
- depths `num_layers in {1,2,4}`;
- readouts `post_ln` and `pre_ln_replay`;
- full samples: 4096 per pair;
- calibration/evaluation split: 2048 / 2048 per pair.

Validity audit:
All route-position rows are valid, all calibration/evaluation splits are balanced by pair id, and label-free controls have no pair-label leakage. A06_01_03_E01-style pass count is `0/1008` condition cells.

## Primary Metric

Primary metric:
held-out feature_NMI for A06_01_03_E01-style label-free controls.

Why it decides:
The question at risk is whether longer slots let simple label-free global controls recover the oracle feature partition. Load \(L\) can improve without feature specialization, so feature_NMI and oracle-gap fraction decide the claim boundary.

Label-free pass gate:
absolute NMI improvement at least `+0.25` over the same-slot baseline and at least `50%` oracle-gap closure.

## Result

The A06_01_01_E05-A06_01_03_E01 conclusion is robust to repeated slot lengths `2` and `4`.

Longer slots do not make simple label-free global controls recover feature-level routing. Common-centering still strongly improves load, residual geometry remains after centering, oracle centroids remain perfect, and A06_01_03_E01-style label-free controls still fail the feature_NMI gate.

Primary readout (`num_layers=1`, `post_ln`):

### A06_01_01_E05-Style Common / Norm Replay

| Slot len | RR load \(L\) | NR load \(L\) | RC load \(L\) | NC load \(L\) |
| ---: | ---: | ---: | ---: | ---: |
| 1 | 0.5577 | 0.5577 | 0.2577 | 0.2408 |
| 2 | 0.5533 | 0.5538 | 0.2784 | 0.2688 |
| 4 | 0.5789 | 0.5805 | 0.2776 | 0.2723 |

Interpretation:
Row-norm control remains ineffective. Common-centering remains the main load reduction for all slot lengths.

### A06_01_01_E06-Style Residual Replay

| Slot len | Centered replay \(L\) | Whitened replay \(L\) | Matched isotropic \(L\) |
| ---: | ---: | ---: | ---: |
| 1 | 0.2577 | 0.1071 | 0.0855 |
| 2 | 0.2784 | 0.0881 | 0.0858 |
| 4 | 0.2776 | 0.0829 | 0.0861 |

Interpretation:
Residual geometry remains after common-centering. Whitening and matched isotropic controls reduce the residual load floor for every slot length.

### A06_01_02_E01-Style Oracle Reachability

| Slot len | Random NMI | Raw centroid NMI | Common-centered centroid NMI | Whitened centroid NMI |
| ---: | ---: | ---: | ---: | ---: |
| 1 | 0.1981 | 1.0000 | 1.0000 | 1.0000 |
| 2 | 0.1913 | 1.0000 | 1.0000 | 1.0000 |
| 4 | 0.1894 | 1.0000 | 1.0000 | 1.0000 |

Interpretation:
The target feature partition remains perfectly reachable under oracle feature-centroid construction. Longer repeated slots slightly increase oracle margins, but not in a way that helps random-row label-free controls.

### A06_01_03_E01-Style Label-Free Controls

| Slot len | Condition | Feature NMI | Oracle-gap fraction | Load \(L\) |
| ---: | --- | ---: | ---: | ---: |
| 1 | baseline raw | 0.1981 | 0.0000 | 0.5655 |
| 1 | calibration mean | 0.2079 | 0.0107 | 0.2588 |
| 1 | heldout batch mean | 0.2091 | 0.0123 | 0.2567 |
| 1 | projection top-1 | 0.1324 | -0.0883 | 0.2907 |
| 1 | whitened residual | 0.0116 | -0.2541 | 0.1102 |
| 1 | oracle centroid | 1.0000 | 1.0000 | 0.0000 |
| 2 | baseline raw | 0.1913 | 0.0000 | 0.5579 |
| 2 | calibration mean | 0.2040 | 0.0146 | 0.2865 |
| 2 | heldout batch mean | 0.2059 | 0.0170 | 0.2756 |
| 2 | projection top-1 | 0.1297 | -0.0799 | 0.2922 |
| 2 | whitened residual | 0.0116 | -0.2386 | 0.0964 |
| 2 | oracle centroid | 1.0000 | 1.0000 | 0.0000 |
| 4 | baseline raw | 0.1894 | 0.0000 | 0.5767 |
| 4 | calibration mean | 0.2072 | 0.0199 | 0.2691 |
| 4 | heldout batch mean | 0.2081 | 0.0211 | 0.2762 |
| 4 | projection top-1 | 0.1296 | -0.0776 | 0.3003 |
| 4 | whitened residual | 0.0104 | -0.2357 | 0.0901 |
| 4 | oracle centroid | 1.0000 | 1.0000 | 0.0000 |

Interpretation:
Longer slots do not rescue simple label-free global controls. Calibration / heldout mean centering still improves load by a large amount, but closes only about `1-2%` of the oracle NMI gap. Whitening gives the best load but destroys feature_NMI.

## Key Figures

### Figure: A06_01_01_E05-Style Load By Slot Length

![A06_01_01_E05 load by slot length](figures/a06_04_load_by_slot_len.png)

What this tests:
Whether common-centering remains the main load reduction as slot length changes.

Observed result:
RR and NR remain high and close to each other. RC and NC remain much lower.

Allowed claim:
The A06_01_01_E05 common-component interpretation is stable under repeated slot lengths `1,2,4`.

What this does not prove:
It does not prove the same behavior for distributed multi-token slot codes or real text.

### Figure: A06_01_01_E06-Style Residual Load By Slot Length

![A06_01_01_E06 residual by slot length](figures/a06_05_residual_by_slot_len.png)

What this tests:
Whether common-centered residual geometry remains active when slots are longer.

Observed result:
Centered residual replay remains nonzero for all slot lengths. Whitening and matched isotropic controls reduce it.

Allowed claim:
A06_01_01_E06's residual-geometry boundary is stable under repeated slot lengths.

### Figure: A06_01_02_E01 Oracle Reachability By Slot Length

![A06_01_02_E01 NMI by slot length](figures/a06_06_nmi_by_slot_len.png)

What this tests:
Whether the target feature partition remains reachable for longer slots.

Observed result:
Oracle centroid conditions remain at feature_NMI `1.0` and load `0.0`.

Allowed claim:
The target partition remains available; label-free failures are not caused by missing feature signal.

### Figure: A06_01_03_E01 Label-Free NMI By Slot Length

![A06_01_03_E01 NMI by slot length](figures/a06_07_nmi_by_slot_len.png)

What this tests:
Whether longer slots let label-free global controls approach the oracle.

Observed result:
Only oracle reaches high NMI. Label-free conditions remain near baseline or worse.

Allowed claim:
A06_01_03_E01's negative result is not a one-token-slot artifact for repeated slots of length `2` or `4`.

### Figure: A06_01_03_E01 Load Versus Oracle Gap By Slot Length

![A06_01_03_E01 load versus oracle gap by slot length](figures/a06_07_load_gap_by_slot_len.png)

What this tests:
Whether load improvement becomes aligned with feature specialization for longer slots.

Observed result:
Load improves under common-centering and whitening, but oracle-gap fraction stays near zero or negative.

Allowed claim:
Load balance remains a misleading proxy for feature specialization.

## Claim Boundary

Can claim:

- A06_01_01_E05-A06_01_03_E01 conclusions are robust to repeated slot lengths `1,2,4` in the same initialized synthetic hidden-state replay surface.
- Longer repeated slots do not make simple label-free global common / residual controls recover the oracle feature partition.
- The next step can remain feature discovery or anti-lockin rather than load-only router repair.

Cannot claim:

- Real DCLM behavior.
- Training stability.
- Distributed long slot codes such as `S_{s,1},S_{s,2},...`.
- Semantic feature discovery.
- Expert utility.
- Failure of all label-free methods.

## Next Decision

Proceed to the next mainline iteration:

1. feature discovery before routing, using clustering / dictionary / contrastive / gradient proxy; or
2. anti-lockin after a good oracle or pseudo-oracle partition.

Do not promote simple global common-centering, projection, or whitening as a feature-specialization method.
