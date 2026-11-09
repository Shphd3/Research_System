# Summary: A06_01_05_E02 All-Position Initialization With MPI

Protocol:
`protocol.md`

Parent experiment:
`../../summary.md`

## Result

MPI-c8 does not preserve or correct all-position initialization into stable
feature specialization. It gives only a small feature-NMI gain over vanilla
all-position initialization and makes the lower-tail margin substantially
worse.

| Method | Feature NMI | Margin p05 | Positive margin frac | Max load | Effective experts | Slot-start NMI |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| vanilla | 0.686 | -3.019 | 0.617 | 0.617 | 2.325 | 0.0005 |
| allpos_centered_init | 0.818 | -5.602 | 0.695 | 0.516 | 2.641 | 0.0007 |
| allpos_centered_mpi_c8 | 0.830 | -20.579 | 0.703 | 0.500 | 2.679 | 0.0006 |
| mpi_c8 | 0.832 | -15.258 | 0.711 | 0.500 | 2.708 | 0.0008 |
| route_centered_init | 0.979 | 1.953 | 0.961 | 0.289 | 3.817 | 0.0010 |
| oracle_centered_init | 1.000 | 3.190 | 1.000 | 0.250 | 4.000 | 0.0010 |

## Interpretation

All-position initialization already contains a partial feature signal
(`0.818` NMI), but its margin is negative (`-5.602`). MPI-c8 raises NMI only
to `0.830`, essentially matching random-init MPI-c8 (`0.832`), while pushing
margin p05 down to `-20.579`. This means MPI-c8 amplifies a sharp spectral
routing rule but does not repair the unstable all-position partition.

The route-centered control remains qualitatively different: it has much higher
NMI (`0.979`) and positive lower-tail margin (`1.953`). Therefore the missing
object is still route-relevant feature-center geometry with positive margin,
not stronger expert-spectral alignment alone.

## Figures

![Final feature NMI](figures/final_feature_nmi_by_method.png)

![Final margin p05](figures/final_margin_p05_by_method.png)

## Claim Boundary

Can claim: in this uniform no-position bridge, all-position initialization plus
MPI-c8 is not a stable feature-specialization method.

Cannot claim: MPI fails in the paper's large-model setting, or expert spectra
contain no feature information.

## Artifacts

- full run log:
  `logs/local/a06_26_allpos_mpi_full_local2gpu_20260703.log`
- final aggregate:
  `tables/condition_aggregate_final.csv`
- trajectory:
  `tables/condition_trajectory_aggregate.csv`
- diagnostics:
  `tables/diagnostics_aggregate.csv`

