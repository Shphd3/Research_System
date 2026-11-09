# Protocol: A06_01_05_E02 All-Position Initialization With MPI

Parent experiment:
`../../summary.md`

## Decision Question

Can MPI-c8 preserve or correct an all-position hidden-state initialization into
stable uniform feature specialization?

## Terms

| Term | Plain meaning | Concrete computation | Why it matters |
| --- | --- | --- | --- |
| All-position initialization | Router rows initialized from hidden states at every token position | K-means on all token hidden states after subtracting their mean | Tests a label-free source that does not know the route position |
| MPI-c8 | MPI router with scale constant \(C'=8\) | \(\hat r_e=8N^{-1/2}r_eW_eW_e^\top/\|r_eW_eW_e^\top\|\) | Strongest MPI variant in the base A06_01_05_E02 run |
| Feature NMI | Agreement between feature id and routed expert | NMI(feature, route) | Primary feature-separation metric |
| Margin p05 | Lower-tail route stability | 5th percentile of matched score minus strongest competitor | Decides whether routing is stable |

## Conditions

| Condition | Meaning |
| --- | --- |
| `vanilla` | Standard learned router |
| `allpos_centered_init` | All-position centered k-means router initialization with vanilla routing |
| `allpos_centered_mpi_c8` | Same all-position initialization, but effective router rows use MPI-c8 |
| `mpi_c8` | MPI-c8 from random router initialization |
| `route_centered_init` | Route-position centered k-means positive control |
| `oracle_centered_init` | Feature-label center upper bound |

## Setup

Same as A06_01_05_E02: uniform no-position slot bridge, four balanced features, slot
starts `2,10,18`, slot lengths `1,2,4,8`, one attention layer, one top-1 MoE
layer, `8` seeds, `160` train steps.

## Command

```bash
CUDA_VISIBLE_DEVICES=0,1 torchrun --standalone --nproc_per_node=2 \
  Projects/from-attention-to-search/main/experiments/A06/06_01_geometry_and_state_discovery/A06_01_05_E02_manifold_power_iteration/scripts/run_a06_26_mpi_uniform_feature_router.py \
  --run-stage full \
  --run-name a06_26_allpos_mpi_full_local2gpu_20260703 \
  --output-dir Projects/from-attention-to-search/main/experiments/A06/06_01_geometry_and_state_discovery/A06_01_05_E02_manifold_power_iteration/extensions/allpos_mpi \
  --methods "vanilla allpos_centered_init allpos_centered_mpi_c8 mpi_c8 route_centered_init oracle_centered_init"
```

## Decision Rule

The all-position + MPI condition is promoted only if it substantially improves
over all-position initialization and obtains positive margin p05. A small NMI
gain with negative margin is a failure to correct the initialization.

