# Detailed: A06_01_05_E02 MPI Uniform Feature Router

Primary anchor:
`../../../../problem_anchors/06_geometry_proxy_preservation/06_01_geometry_and_state_discovery/06_01_geometry_and_state_discovery_anchor.md`

Protocol:
`protocol.md`

Summary:
`summary.md`

## Conclusion

MPI is useful as a spectral-router baseline but not sufficient as the next
mainline method. The best MPI condition, `mpi_c8`, improves final feature NMI
from vanilla `0.686` to `0.832`, while route-position centers reach `0.979`.
The decisive failure is margin: `mpi_c8` has final margin p05 `-15.258`, while
route-centered initialization has `1.953` and oracle has `3.190`.

## Terminology / Definitions

| Term | Plain meaning | Concrete object / computation | Unit or formula | Why it matters | Cannot prove |
| --- | --- | --- | --- | --- | --- |
| Feature NMI | Feature-to-route agreement | NMI(feature id, expert assignment) | 0--1 | Primary specialization metric | Expert utility |
| Margin p05 | Weak-sample route stability | 5th percentile of matched expert score minus best competitor | Logit difference | Guards against thin route basins | Loss optimality |
| Positive margin fraction | Fraction of samples where matched expert beats competitors | Mean of margin > 0 | 0--1 | Shows how much of the dataset has stable assignment | Which feature is useful |
| Max load | Largest expert assignment fraction | \(\max_e P(route=e)\) | 0--1 | Detects expert concentration | Feature identity |
| Effective experts | Diversity of expert usage | \(1/\sum_e p_e^2\) | 1--4 | Distinguishes partial from full distribution | Correct feature grouping |
| Router-SVD alignment | Spectral mechanism check | Diagonal absolute cosine between effective router rows and expert top SVD rows | 0--1 | Confirms MPI follows expert spectra | Feature specialization |
| Slot-start NMI | Position leakage check | NMI(slot_start, route) | 0--1 | Ensures no slot-position shortcut dominates | All nuisance absence |

## Paper Method And Bridge Implementation

The Redesign MoE router paper proposes aligning each router row with the
corresponding expert principal direction through manifold power iteration and
then retraction. The paper code hint uses `R`, expert weights `wg`, a
normalization step, and a scale \(C=C'N^{-1/2}\). The public TorchTitan patch
implements the same core operation as router row times expert first-layer
transpose times expert first-layer matrix before normalization.

This experiment implements the corresponding bridge operation:

\[
\tilde r_e = r_eW_eW_e^\top,\qquad
\hat r_e=\frac{C'}{\sqrt{N}}\frac{\tilde r_e}{\|\tilde r_e\|_2},
\qquad
s_e(h)=h^\top\hat r_e.
\]

Here \(W_e\) is the first linear projection of expert \(e\) transposed into input
space. This is appropriate for the GLU-free expert used in the synthetic
bridge. It is not a claim that the full large-model code path from the paper
has been reproduced.

Source:
<https://arxiv.org/abs/2606.12397>

Public code source:
<https://github.com/ericshwu/Router-with-Manifold-Power-Iteration/blob/main/torchtitan-patches/ttp/models/aoe4.py>

## Data Construction

The experiment uses the same uniform no-position slot bridge as A06_01_05_E01.

| Field | Value |
| --- | --- |
| sequence length | `32` |
| neutral tokens | `0--31` |
| feature tokens | `32--35` |
| target tokens | `36--39` |
| features | four balanced feature ids, exactly `0.25` each |
| slot starts | `2,10,18`, balanced |
| slot lengths | `1,2,4,8` |
| route position | final token of repeated feature slot |
| supervised target | feature-specific target token immediately after slot |
| position embeddings | none |

Data audit passed. For both calibration and evaluation splits, every feature
fraction is exactly `0.2500` and every slot length has three slot-start values.

## Model And Training Setup

| Field | Value |
| --- | --- |
| model | one causal self-attention layer + one top-1 MoE layer |
| hidden size | `64` |
| attention heads | `4` |
| experts | `4` |
| expert hidden size | `128` |
| optimizer | AdamW |
| learning rate | `2e-3` |
| weight decay | `1e-4` |
| gradient clip | `1.0` |
| train steps | `160` |
| train batch size | `256` |
| calibration samples | `2048` |
| eval samples | `2048` |
| seeds | `0--7` |
| slot lengths | `1,2,4,8` |
| local GPUs | `2` |

## Conditions

| Condition | Definition | Purpose |
| --- | --- | --- |
| `vanilla` | Standard trainable router | Baseline |
| `retract_c1` | Normalize router rows with \(C'=1\), no MPI | Retraction-only ablation |
| `mpi_c1` | MPI, \(C'=1\) | Paper-style spectral router |
| `mpi_c2` | MPI, \(C'=2\) | Scale sweep |
| `mpi_c4` | MPI, \(C'=4\) | Scale sweep |
| `mpi_c8` | MPI, \(C'=8\) | Scale sweep |
| `static_svd_init` | Initialize router from expert top singular directions, then train vanilla router | Static spectral baseline |
| `route_centered_init` | K-means on route-position hidden states | Positive control |
| `oracle_centered_init` | Feature-label centers | Upper bound |

## Main Results

Final checkpoint, averaged over `8` seeds and `4` slot lengths:

| Method | Feature NMI | NMI std | Margin p05 | Positive margin frac | Max load | Effective experts | Slot-start NMI |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| vanilla | 0.686 | 0.288 | -3.019 | 0.617 | 0.617 | 2.325 | 0.0005 |
| retract_c1 | 0.673 | 0.283 | -2.170 | 0.594 | 0.609 | 2.255 | 0.0004 |
| static_svd_init | 0.815 | 0.089 | -5.154 | 0.672 | 0.484 | 2.591 | 0.0008 |
| mpi_c1 | 0.705 | 0.251 | -3.047 | 0.609 | 0.609 | 2.288 | 0.0006 |
| mpi_c2 | 0.728 | 0.251 | -5.325 | 0.625 | 0.562 | 2.386 | 0.0006 |
| mpi_c4 | 0.794 | 0.166 | -8.870 | 0.672 | 0.523 | 2.560 | 0.0007 |
| mpi_c8 | 0.832 | 0.097 | -15.258 | 0.711 | 0.500 | 2.708 | 0.0008 |
| route_centered_init | 0.979 | 0.049 | 1.953 | 0.961 | 0.289 | 3.817 | 0.0010 |
| oracle_centered_init | 1.000 | 0.000 | 3.190 | 1.000 | 0.250 | 4.000 | 0.0010 |

### Slot-Length Robustness

Final feature NMI by slot length:

| Method | Slot 1 | Slot 2 | Slot 4 | Slot 8 |
| --- | ---: | ---: | ---: | ---: |
| vanilla | 0.689 | 0.689 | 0.689 | 0.678 |
| retract_c1 | 0.669 | 0.669 | 0.669 | 0.686 |
| static_svd_init | 0.823 | 0.823 | 0.806 | 0.806 |
| mpi_c1 | 0.697 | 0.681 | 0.681 | 0.760 |
| mpi_c2 | 0.735 | 0.689 | 0.689 | 0.798 |
| mpi_c4 | 0.814 | 0.798 | 0.738 | 0.826 |
| mpi_c8 | 0.826 | 0.834 | 0.834 | 0.834 |
| route_centered_init | 1.000 | 0.967 | 0.967 | 0.983 |
| oracle_centered_init | 1.000 | 1.000 | 1.000 | 1.000 |

The conclusion is not driven by a single slot length. `mpi_c8` is consistently
better than vanilla, but it remains below the route-centered control.

### Training Trajectory

Feature NMI trajectory:

| Method | step 0 | step 10 | step 40 | step 80 | step 160 |
| --- | ---: | ---: | ---: | ---: | ---: |
| vanilla | 0.594 | 0.695 | 0.682 | 0.686 | 0.686 |
| retract_c1 | 0.588 | 0.674 | 0.669 | 0.673 | 0.673 |
| static_svd_init | 0.735 | 0.812 | 0.815 | 0.815 | 0.815 |
| mpi_c1 | 0.676 | 0.705 | 0.705 | 0.705 | 0.705 |
| mpi_c2 | 0.676 | 0.728 | 0.723 | 0.728 | 0.728 |
| mpi_c4 | 0.676 | 0.749 | 0.749 | 0.789 | 0.794 |
| mpi_c8 | 0.676 | 0.738 | 0.804 | 0.832 | 0.832 |
| route_centered_init | 0.970 | 0.979 | 0.979 | 0.979 | 0.979 |
| oracle_centered_init | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |

Margin p05 trajectory:

| Method | step 0 | step 10 | step 40 | step 80 | step 160 |
| --- | ---: | ---: | ---: | ---: | ---: |
| vanilla | -0.844 | -1.899 | -3.085 | -3.050 | -3.019 |
| retract_c1 | -0.717 | -1.590 | -2.260 | -2.189 | -2.170 |
| static_svd_init | -1.484 | -4.345 | -5.130 | -5.139 | -5.154 |
| mpi_c1 | -0.731 | -3.543 | -3.288 | -3.086 | -3.047 |
| mpi_c2 | -1.462 | -6.531 | -5.787 | -5.384 | -5.325 |
| mpi_c4 | -2.924 | -10.668 | -9.547 | -8.998 | -8.870 |
| mpi_c8 | -5.849 | -18.093 | -16.786 | -15.472 | -15.258 |
| route_centered_init | 7.811 | 6.790 | 1.014 | 1.641 | 1.953 |
| oracle_centered_init | 11.121 | 9.752 | 2.399 | 2.803 | 3.190 |

Interpretation: MPI-c8 accumulates NMI, but the lower-tail margin becomes more
negative. Higher \(C'\) sharpens partial routing but does not create a safe
basin.

## Diagnostic Results

Final diagnostic aggregate:

| Method | Router-SVD alignment | Feature-center best cosine | Row-pair abs cosine | Center margin p05 |
| --- | ---: | ---: | ---: | ---: |
| vanilla | 0.202 | 0.378 | 0.124 | -2.966 |
| retract_c1 | 0.208 | 0.377 | 0.139 | -2.123 |
| static_svd_init | 0.279 | 0.333 | 0.097 | -4.924 |
| mpi_c1 | 0.917 | 0.457 | 0.378 | -3.000 |
| mpi_c2 | 0.874 | 0.453 | 0.298 | -5.219 |
| mpi_c4 | 0.841 | 0.439 | 0.205 | -8.647 |
| mpi_c8 | 0.809 | 0.432 | 0.166 | -14.812 |
| route_centered_init | 0.672 | 0.490 | 0.359 | 2.169 |
| oracle_centered_init | 0.699 | 0.498 | 0.326 | 3.446 |

MPI strongly increases router-SVD alignment, confirming the implementation is
doing the intended spectral operation. This does not imply feature
specialization: center margins remain negative.

## Extension: All-Position Initialization With MPI

This extension asks whether MPI-c8 can preserve or correct all-position
initialization. It cannot. The all-position source already has partial feature
agreement, but it does not have positive margins; MPI-c8 sharpens routing
without fixing that source error.

| Method | Feature NMI | Margin p05 | Positive margin frac | Max load | Effective experts |
| --- | ---: | ---: | ---: | ---: | ---: |
| allpos_centered_init | 0.818 | -5.602 | 0.695 | 0.516 | 2.641 |
| allpos_centered_mpi_c8 | 0.830 | -20.579 | 0.703 | 0.500 | 2.679 |
| mpi_c8 | 0.832 | -15.258 | 0.711 | 0.500 | 2.708 |
| route_centered_init | 0.979 | 1.953 | 0.961 | 0.289 | 3.817 |

The full extension record is in
`extensions/allpos_mpi/summary.md` and
`extensions/allpos_mpi/detailed.md`.

## Visualization Results

### Figure: Final Feature NMI

![Final feature NMI by router method](figures/final_feature_nmi_by_method.png)

Purpose: compare final feature-to-expert separation across router methods.

How to read: higher is better; `1.0` means route assignments perfectly identify
feature ids up to expert permutation.

Observed result: `mpi_c8` is the best MPI setting (`0.832`) but remains below
`route_centered_init` (`0.979`) and `oracle_centered_init` (`1.000`).

Take-home: MPI improves feature agreement but does not close the route-control
gap.

Limitation: NMI does not measure margin thickness or expert utility.

### Figure: Final Margin Lower Tail

![Final margin p05 by router method](figures/final_margin_p05_by_method.png)

Purpose: test whether the weakest routed samples are inside a positive-margin
basin.

How to read: values above zero mean the matched expert beats the best
competitor for at least 95% of samples under the matched map.

Observed result: route-centered and oracle-centered controls are positive;
all MPI variants are negative, with larger \(C'\) producing more negative
lower-tail margins.

Take-home: MPI is not a stable specialization method in this setting.

Limitation: margin is measured under the current matched feature-to-expert map;
it does not prove long-run failure under every possible optimizer schedule.

### Figure: Feature NMI Trajectory

![Feature NMI trajectory by router method](figures/feature_nmi_trajectory_by_method.png)

Purpose: inspect whether MPI is only an initialization effect or improves
through training.

How to read: each line is an aggregate over seeds and slot lengths at a
checkpoint.

Observed result: `mpi_c8` rises from `0.676` to `0.832`, while route-centered
and oracle controls stay near the top.

Take-home: MPI can accumulate partial feature agreement, but the improvement
does not reach the positive controls.

Limitation: the plot does not show margin; use the margin trajectory for
stability.

### Figure: Router-SVD Alignment

![Router-SVD alignment by method](figures/router_svd_alignment_by_method.png)

Purpose: verify whether MPI actually aligns effective router rows with expert
top singular directions.

How to read: higher cosine means stronger alignment between effective router
rows and corresponding expert spectral directions.

Observed result: MPI variants have the highest alignment (`0.809--0.917`),
while vanilla and retraction-only are near `0.20`.

Take-home: the spectral operation is active; the negative result is not caused
by failing to align with expert spectra.

Limitation: expert spectral alignment is not itself a feature-specialization
metric.

## Artifact Map

| Artifact | Path |
| --- | --- |
| runner | `scripts/run_a06_26_mpi_uniform_feature_router.py` |
| run log | `logs/local/a06_26_mpi_full_local2gpu_20260703.log` |
| summary JSON | `summary.json` |
| data audit | `tables/data_audit.csv` |
| raw trajectory | `tables/training_trajectory.csv` |
| final aggregate | `tables/condition_aggregate_final.csv` |
| diagnostic aggregate | `tables/diagnostics_aggregate.csv` |
| diagnostic trajectory | `tables/diagnostics_trajectory_aggregate.csv` |
| final feature NMI figure | `figures/final_feature_nmi_by_method.png` |
| final margin figure | `figures/final_margin_p05_by_method.png` |
| final load figure | `figures/final_max_load_by_method.png` |
| feature NMI trajectory figure | `figures/feature_nmi_trajectory_by_method.png` |
| margin trajectory figure | `figures/margin_p05_trajectory_by_method.png` |
| router-SVD alignment figure | `figures/router_svd_alignment_by_method.png` |
| all-position MPI extension | `extensions/allpos_mpi/summary.md` |

## Claim Boundary

Can claim:

- MPI improves final feature NMI over vanilla on the uniform no-position slot
  bridge.
- Retraction alone is not sufficient.
- All-position initialization plus MPI-c8 does not correct the mixed
  hidden-state source into stable feature specialization.
- Expert-spectrum alignment and feature specialization are distinct; MPI gives
  high spectral alignment but negative feature margins.
- Slot-start leakage is not the observed cause.

Cannot claim:

- MPI fails in the Redesign paper setting;
- MPI cannot work with larger models, different experts, load-balancing loss,
  or paper-level training recipes;
- real-DCLM transfer;
- common/rare routing behavior;
- semantic expert utility.

## Updated Hypothesis

Before this run, a live hypothesis was that dynamic expert spectral alignment
could turn the partly useful expert-SVD source from A06_01_05_E01 into a method. The
updated hypothesis is narrower:

```text
expert spectra can provide a weak route-relevant bias,
but a successful feature-specialization method must still form
feature-center-aware hidden states and positive route margins.
```

The next mainline experiment should therefore not be a broader MPI scale sweep.
It should test whether nested / long-horizon supervision can create
route-relevant feature geometry that a router can use with a positive margin.
