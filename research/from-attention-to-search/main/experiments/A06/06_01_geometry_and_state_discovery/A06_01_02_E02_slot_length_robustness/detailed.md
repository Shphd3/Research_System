# Detailed: A06_01_02_E02 Slot-Length Robustness Replay

Primary anchor:
`../../../../problem_anchors/06_geometry_proxy_preservation/06_01_geometry_and_state_discovery/06_01_geometry_and_state_discovery_anchor.md`

Protocol:
`protocol.md`

Summary:
`summary.md`

## 0. Quick Recap

Purpose:
Audit whether the A06_01_01_E05-A06_01_03_E01 initialized router-geometry sequence is stable when the one-token slot is replaced by repeated slots of length `2` and `4`.

Conclusion:
The sequence is stable. Longer repeated slots do not make simple label-free global common / residual controls recover the oracle feature partition.

Primary evidence:
`0/1008` A06_01_03_E01-style condition cells pass the label-free NMI gate. Oracle centroid routing remains perfect for all tested slot lengths. Common-centering and whitening continue to improve load without recovering feature_NMI.

## 1. Protocol Compliance Audit

Approved conditions match actual conditions:
Yes. The full run used `slot_token_len in {1,2,4}`, seeds `20260521..20260528`, depths `1,2,4`, and readouts `post_ln,pre_ln_replay`.

Primary metric exists:
Yes. `tables/a06_07_label_free.csv` and `tables/a06_07_aggregate.csv` include feature_NMI, NMI delta, oracle-gap fraction, and load \(L\).

Central figures/tables exist:
Yes. The experiment directory contains curated tables and five central figures.

Seeds/checkpoints recorded:
Yes. Step-0 only, eight seeds, three depths, two readouts, three slot lengths.

Known good reviewed:
Yes. The A06_01_02_E01-style oracle feature centroid reaches feature_NMI `1.0` and load `0.0` across slot lengths.

Known bad reviewed:
Yes. The A06_01_03_E01-style label-free global controls do not pass the NMI gate; whitening has low load but near-zero NMI.

Failure or insufficient evidence criteria applied:
Yes. No label-free condition reaches `+0.25` absolute NMI improvement and `50%` oracle-gap closure.

## 2. Setup

Data:
Synthetic sequence length `32`. Four pair ids. For each pair id, the generator repeats the same `SLOT_s` token for `slot_token_len` positions, then places `TARGET_s` immediately after the slot span. Background tokens are random and independent of pair id.

Route position:
`pair_start + slot_token_len - 1`.

Target position:
`pair_start + slot_token_len`.

Slot lengths:
`1,2,4`.

Model:
Initialized Transformer-MoE replay, four experts, no training.

Full run:

- seeds: `20260521..20260528`;
- depths: `1,2,4`;
- readouts: `post_ln`, `pre_ln_replay`;
- samples: 4096 per pair;
- calibration/evaluation: 2048 / 2048 per pair;
- run name: `a06_08_full_20260622_1`.

Smoke run:
`a06_08_smoke_20260622_1` completed before the full run with `slot_token_len in {1,4}`, two seeds, one layer, `post_ln`, and 512 samples per pair.

## 3. Commands

Smoke:

```bash
python scripts/run_a06_08_slot_length_robustness_replay.py \
  --config configs/a06_08_slot_length_robustness_replay.json \
  --run-name a06_08_smoke_20260622_1 \
  --run-stage smoke \
  --seeds 20260521,20260522 \
  --num-layers 1 \
  --slot-token-lens 1,4 \
  --router-input-norm post_ln \
  --device cuda
```

Full:

```bash
python scripts/run_a06_08_slot_length_robustness_replay.py \
  --config configs/a06_08_slot_length_robustness_replay.json \
  --run-name a06_08_full_20260622_1 \
  --run-stage full \
  --slot-token-lens 1,2,4 \
  --device cuda
```

## 4. Validity Audits

Data / route audit:
All `288` route audit rows are valid. The route position rule is `pair_start + slot_token_len - 1`; the target position rule is `pair_start + slot_token_len`.

Split audit:
All pair ids have exactly 2048 calibration samples and 2048 evaluation samples for every slot length, seed, depth, and readout.

Label leakage audit:
Label-free controls have zero pair-label control leakage. The oracle condition is explicitly marked non-label-free.

Primary pass audit:
`0/1008` A06_01_03_E01-style condition cells pass the label-free step-0 gate.

## 5. Full Evidence Tables

### A06_01_01_E05-Style Replay

Primary readout (`num_layers=1`, `post_ln`):

| Slot len | RR load \(L\) | NR load \(L\) | RC load \(L\) | NC load \(L\) |
| ---: | ---: | ---: | ---: | ---: |
| 1 | 0.5577 | 0.5577 | 0.2577 | 0.2408 |
| 2 | 0.5533 | 0.5538 | 0.2784 | 0.2688 |
| 4 | 0.5789 | 0.5805 | 0.2776 | 0.2723 |

Full sweep means:

| Slot len | RR load \(L\) | NR load \(L\) | RC load \(L\) | NC load \(L\) |
| ---: | ---: | ---: | ---: | ---: |
| 1 | 0.6873 | 0.6843 | 0.2820 | 0.2814 |
| 2 | 0.6915 | 0.6873 | 0.2953 | 0.2948 |
| 4 | 0.7032 | 0.7010 | 0.3001 | 0.2989 |

Interpretation:
Longer repeated slots do not make row-norm control important. Common-centering remains the only large load reduction.

### A06_01_01_E06-Style Residual Replay

Primary readout (`num_layers=1`, `post_ln`):

| Slot len | Centered replay \(L\) | Whitened replay \(L\) | Matched isotropic \(L\) |
| ---: | ---: | ---: | ---: |
| 1 | 0.2577 | 0.1071 | 0.0855 |
| 2 | 0.2784 | 0.0881 | 0.0858 |
| 4 | 0.2776 | 0.0829 | 0.0861 |

Full sweep means:

| Slot len | Centered replay \(L\) | Whitened replay \(L\) | Matched isotropic \(L\) |
| ---: | ---: | ---: | ---: |
| 1 | 0.2820 | 0.0804 | 0.0741 |
| 2 | 0.2953 | 0.0839 | 0.0736 |
| 4 | 0.3001 | 0.0743 | 0.0720 |

Interpretation:
Residual geometry remains. The centered residual load does not vanish as slot length grows.

### A06_01_02_E01-Style Oracle Reachability

Primary readout (`num_layers=1`, `post_ln`):

| Slot len | Random NMI | Raw centroid NMI | Common-centered centroid NMI | Whitened centroid NMI |
| ---: | ---: | ---: | ---: | ---: |
| 1 | 0.1981 | 1.0000 | 1.0000 | 1.0000 |
| 2 | 0.1913 | 1.0000 | 1.0000 | 1.0000 |
| 4 | 0.1894 | 1.0000 | 1.0000 | 1.0000 |

Full sweep means:

| Slot len | Random NMI | Raw centroid NMI | Common-centered centroid NMI | Whitened centroid NMI |
| ---: | ---: | ---: | ---: | ---: |
| 1 | 0.2299 | 1.0000 | 1.0000 | 1.0000 |
| 2 | 0.2342 | 1.0000 | 1.0000 | 1.0000 |
| 4 | 0.2400 | 1.0000 | 1.0000 | 1.0000 |

Oracle margins:
Common-centered centroid margin p05 increases slightly with slot length in the full sweep:

| Slot len | Common-centered centroid margin p05 |
| ---: | ---: |
| 1 | 3.9922 |
| 2 | 4.0432 |
| 4 | 4.0896 |

Interpretation:
Longer repeated slots slightly strengthen the oracle route margin, but this extra signal is not recovered by random-row label-free global controls.

### A06_01_03_E01-Style Label-Free Controls

Primary readout (`num_layers=1`, `post_ln`):

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

Full sweep means:

| Slot len | Condition | Feature NMI | Oracle-gap fraction | Load \(L\) |
| ---: | --- | ---: | ---: | ---: |
| 1 | baseline raw | 0.2299 | 0.0000 | 0.6910 |
| 1 | calibration mean | 0.2351 | 0.0052 | 0.2822 |
| 1 | heldout batch mean | 0.2358 | 0.0064 | 0.2823 |
| 1 | projection top-1 | 0.1621 | -0.0945 | 0.2829 |
| 1 | whitened residual | 0.0150 | -0.2944 | 0.0869 |
| 1 | oracle centroid | 1.0000 | 1.0000 | 0.0000 |
| 2 | baseline raw | 0.2342 | 0.0000 | 0.6915 |
| 2 | calibration mean | 0.2384 | 0.0039 | 0.2973 |
| 2 | heldout batch mean | 0.2393 | 0.0051 | 0.2923 |
| 2 | projection top-1 | 0.1651 | -0.0970 | 0.2922 |
| 2 | whitened residual | 0.0156 | -0.3011 | 0.0824 |
| 2 | oracle centroid | 1.0000 | 1.0000 | 0.0000 |
| 4 | baseline raw | 0.2400 | 0.0000 | 0.7031 |
| 4 | calibration mean | 0.2400 | -0.0028 | 0.2989 |
| 4 | heldout batch mean | 0.2402 | -0.0024 | 0.3006 |
| 4 | projection top-1 | 0.1680 | -0.1021 | 0.2888 |
| 4 | whitened residual | 0.0148 | -0.3127 | 0.0835 |
| 4 | oracle centroid | 1.0000 | 1.0000 | 0.0000 |

Interpretation:
Longer repeated slots do not increase label-free global-control NMI. The full-sweep calibration mean effect shrinks from a small positive gap at length 1 to approximately zero or negative at length 4.

## 6. Visualization Results

### A06_01_01_E05 Load By Slot Length

![A06_01_01_E05 load by slot length](figures/a06_04_load_by_slot_len.png)

Purpose:
Check whether A06_01_01_E05's common-component conclusion survives longer slots.

Setup:
Primary readout over slot lengths `1,2,4`, with RR / NR / RC / NC replay conditions.

How to read:
Lower load \(L\) means closer to uniform expert load. If row norm mattered, NR would drop below RR. If common mattered, RC / NC would drop below RR.

Observed result:
NR stays close to RR. RC and NC are consistently lower.

Take-home:
Common-centering remains the main tested load control.

Remaining uncertainty:
This only covers repeated slot tokens, not distributed slot codes.

### A06_01_01_E06 Residual By Slot Length

![A06_01_01_E06 residual by slot length](figures/a06_05_residual_by_slot_len.png)

Purpose:
Check whether residual geometry remains after common-centering for longer slots.

Setup:
Centered residual replay, centered whitened replay, and matched isotropic control.

How to read:
If residual load were only a short-slot artifact, centered replay should drop toward zero as slot length grows.

Observed result:
Centered residual replay remains around `0.26-0.28` in the primary readout. Whitening and matched isotropic controls remain lower.

Take-home:
Residual geometry remains active.

### A06_01_02_E01 NMI By Slot Length

![A06_01_02_E01 NMI by slot length](figures/a06_06_nmi_by_slot_len.png)

Purpose:
Check whether feature partition reachability changes with slot length.

Setup:
Random router and oracle centroid conditions.

How to read:
NMI near 1 means routed expert identity matches feature identity.

Observed result:
Oracle centroid conditions remain at NMI `1.0`.

Take-home:
The target partition exists across slot lengths.

### A06_01_03_E01 NMI By Slot Length

![A06_01_03_E01 NMI by slot length](figures/a06_07_nmi_by_slot_len.png)

Purpose:
Check whether simple label-free global controls recover feature routing when slots are longer.

Setup:
Baseline, mean-centering, projection, whitening, and oracle upper bound.

How to read:
Label-free controls should move upward toward oracle if they recover feature specialization.

Observed result:
Label-free controls remain near baseline or worse; only oracle reaches NMI `1.0`.

Take-home:
Longer repeated slots do not rescue simple label-free global controls.

### A06_01_03_E01 Load Versus Oracle Gap By Slot Length

![A06_01_03_E01 load versus oracle gap by slot length](figures/a06_07_load_gap_by_slot_len.png)

Purpose:
Separate load improvement from feature specialization.

Setup:
Load \(L\) for main label-free controls, plus oracle-gap fraction for calibration mean.

How to read:
Good load alone is not enough. A useful feature-specialization control must also close the oracle NMI gap.

Observed result:
Load improves strongly under centering and whitening, but oracle-gap fraction remains near zero.

Take-home:
Load balance remains a bad proxy for feature specialization.

## 7. Failure Interpretation

Observation:
Longer slots slightly increase oracle margins but do not improve label-free global-control NMI.

Interpretation:
Repeated slot length strengthens an oracle-readable feature direction, but global statistics such as mean, top-PC, and covariance do not discover the feature partition.

Observation:
Whitening consistently gives low load and near-zero feature_NMI.

Interpretation:
Covariance control can remove load anisotropy while scrambling or erasing feature-discriminative structure for random rows.

Observation:
Full-sweep baseline NMI slightly increases with slot length (`0.2299 -> 0.2342 -> 0.2400`), but the oracle gap remains almost entirely open.

Interpretation:
Longer repeated slots may make the feature signal a little more visible to random geometry, but not enough to change the method conclusion.

## 8. Artifact Map

Code workspace:
`Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/`

Runner:
`scripts/run_a06_08_slot_length_robustness_replay.py`

Config:
`configs/a06_08_slot_length_robustness_replay.json`

Raw result dir:
`results/a06_08_slot_length_robustness_replay/a06_08_full_20260622_1/`

Raw figure dir:
`figures/a06_08_slot_length_robustness_replay/a06_08_full_20260622_1/`

Curated project experiment dir:
`Projects/from-attention-to-search/main/experiments/A06/06_01_geometry_and_state_discovery/A06_01_02_E02_slot_length_robustness/`

Curated tables:

- `tables/a06_04_aggregate.csv`
- `tables/a06_04_replay.csv`
- `tables/a06_05_aggregate.csv`
- `tables/a06_05_residual.csv`
- `tables/a06_06_aggregate.csv`
- `tables/a06_06_oracle.csv`
- `tables/a06_07_aggregate.csv`
- `tables/a06_07_label_free.csv`
- `tables/data_audit.csv`
- `tables/route_audit.csv`
- `tables/split_audit.csv`
- `tables/label_leakage_audit.csv`
- `tables/projection_audit.csv`
- `tables/a06_05_whitening_audit.csv`
- `tables/a06_06_whitening_audit.csv`
- `tables/a06_07_whitening_audit.csv`

Curated figures:

- `figures/a06_04_load_by_slot_len.png`
- `figures/a06_05_residual_by_slot_len.png`
- `figures/a06_06_nmi_by_slot_len.png`
- `figures/a06_07_nmi_by_slot_len.png`
- `figures/a06_07_load_gap_by_slot_len.png`

Job id:
Local CUDA run, no ACP job id.

## 9. Claim Boundary

Can claim:
The A06_01_01_E05-A06_01_03_E01 initialized synthetic hidden-state replay conclusions are robust to repeated slot lengths `1,2,4`.

Cannot claim:
Real DCLM transfer, trained stability, distributed slot-code robustness, semantic specialization, expert utility, or failure of all label-free feature discovery methods.

## 10. Next Decision

Proceed to feature discovery or anti-lockin. Do not spend the next iteration on simple global common-centering, top-PC projection, or whitening as feature-specialization methods.
