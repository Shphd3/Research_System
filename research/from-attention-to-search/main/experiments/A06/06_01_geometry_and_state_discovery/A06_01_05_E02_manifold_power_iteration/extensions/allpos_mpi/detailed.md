# Detailed: A06_01_05_E02 All-Position Initialization With MPI

Protocol:
`protocol.md`

Summary:
`summary.md`

## Conclusion

The all-position + MPI-c8 extension weakens the idea that MPI can correct a
wrong or mixed hidden-state population. Compared with `allpos_centered_init`,
`allpos_centered_mpi_c8` improves final feature NMI by only `0.012`
(`0.818` to `0.830`) and worsens margin p05 from `-5.602` to `-20.579`.

## Setup

The run uses the same A06_01_05_E02 data and model: uniform no-position slot bridge,
four features, four experts, one causal attention layer, one MoE layer, `8`
seeds, slot lengths `1,2,4,8`, and `160` train steps.

Run name:
`a06_26_allpos_mpi_full_local2gpu_20260703`

Completed cells:
`192` seed/slot/method cells.

## Final Results

| Method | Feature NMI | NMI std | Margin p05 | Positive margin frac | Max load | Effective experts | Slot-start NMI |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| vanilla | 0.686 | 0.288 | -3.019 | 0.617 | 0.617 | 2.325 | 0.0005 |
| allpos_centered_init | 0.818 | 0.107 | -5.602 | 0.695 | 0.516 | 2.641 | 0.0007 |
| allpos_centered_mpi_c8 | 0.830 | 0.089 | -20.579 | 0.703 | 0.500 | 2.679 | 0.0006 |
| mpi_c8 | 0.832 | 0.097 | -15.258 | 0.711 | 0.500 | 2.708 | 0.0008 |
| route_centered_init | 0.979 | 0.049 | 1.953 | 0.961 | 0.289 | 3.817 | 0.0010 |
| oracle_centered_init | 1.000 | 0.000 | 3.190 | 1.000 | 0.250 | 4.000 | 0.0010 |

## Trajectory

| Method | NMI@0 | NMI@10 | NMI@40 | NMI@80 | NMI@160 | margin p05@160 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| allpos_centered_init | 0.802 | 0.815 | 0.816 | 0.810 | 0.818 | -5.602 |
| allpos_centered_mpi_c8 | 0.794 | 0.830 | 0.830 | 0.830 | 0.830 | -20.579 |
| mpi_c8 | 0.676 | 0.738 | 0.804 | 0.832 | 0.832 | -15.258 |
| route_centered_init | 0.970 | 0.979 | 0.979 | 0.979 | 0.979 | 1.953 |

## Mechanism Reading

MPI-c8 increases router-SVD alignment and sharpens expert usage, but the
matched feature margins remain negative. The result is consistent with the
main A06_01_05_E02 mechanism: expert-spectral alignment provides a partial routing
bias, but it is not the same as a positive-margin feature partition.

The all-position pool still mixes route-relevant and non-route hidden states.
MPI operates after that source choice; it does not identify which hidden-state
population should define the router rows.

## Claim Boundary

This extension only audits all-position initialization plus MPI-c8 on the
uniform no-position slot bridge. It does not test common/rare imbalance, real
DCLM hidden states, larger MoE models, or the full paper training recipe.

