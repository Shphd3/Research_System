# Table Templates

Copy these tables into `paper.tex` after running E1--E5.

## Table E1: Uniform sphere routing

| Prototype / assignment | Load CV ↓ | Max/min load ↓ | KL-to-uniform ↓ | Max load error ↓ |
|---|---:|---:|---:|---:|
| Symmetric prototypes | TBD | TBD | TBD | TBD |
| Random prototypes | TBD | TBD | TBD | TBD |
| Clustered prototypes | TBD | TBD | TBD | TBD |
| Symmetric + balanced assignment | TBD | TBD | TBD | TBD |

Main reading: symmetric prototypes should route uniform sphere features nearly uniformly; clustered prototypes should not.

## Table E2: Geometry floor versus token sampling

| E | N | Init error | Sampling error | Total error |
|---:|---:|---:|---:|---:|
| 4 | 1e3 | TBD | TBD | TBD |
| 4 | 1e4 | TBD | TBD | TBD |
| 4 | 1e5 | TBD | TBD | TBD |
| 8 | 1e3 | TBD | TBD | TBD |
| 8 | 1e4 | TBD | TBD | TBD |
| 8 | 1e5 | TBD | TBD | TBD |

Main reading: sampling error decreases with N, while initialization error remains.

## Table E3: Expert spectral prototypes

| Prototype mode | Router | Alignment lambda ↑ | Load CV ↓ | Max/min load ↓ | KL ↓ |
|---|---|---:|---:|---:|---:|
| Symmetric | Exact SVD | TBD | TBD | TBD | TBD |
| Symmetric | MPI-1 | TBD | TBD | TBD | TBD |
| Symmetric | MPI-5 | TBD | TBD | TBD | TBD |
| Random | Exact SVD | TBD | TBD | TBD | TBD |
| Clustered | Exact SVD | TBD | TBD | TBD | TBD |
| Clustered | MPI-1 | TBD | TBD | TBD | TBD |

Main reading: MPI alignment is useful, but load uniformity also depends on prototype spread.

## Table E4: Balanced assignment cost

| Prototype mode | Assignment | Load CV ↓ | Max/min load ↓ | Mean selected score ↑ | Score drop vs top-1 ↓ |
|---|---|---:|---:|---:|---:|
| Symmetric | Top-1 | TBD | TBD | TBD | TBD |
| Symmetric | Balanced | TBD | TBD | TBD | TBD |
| Random | Top-1 | TBD | TBD | TBD | TBD |
| Random | Balanced | TBD | TBD | TBD | TBD |
| Clustered | Top-1 | TBD | TBD | TBD | TBD |
| Clustered | Balanced | TBD | TBD | TBD | TBD |

Main reading: balanced assignment enforces strict load uniformity and reveals its score cost.

## Table E5: Nonuniform spectrum and whitening

| Alpha | Preprocess | Condition number ↓ | Effective rank ↑ | Load CV ↓ | Max/min load ↓ |
|---:|---|---:|---:|---:|---:|
| 1 | Raw | TBD | TBD | TBD | TBD |
| 1 | Whitened | TBD | TBD | TBD | TBD |
| 2 | Raw | TBD | TBD | TBD | TBD |
| 2 | Whitened | TBD | TBD | TBD | TBD |
| 5 | Raw | TBD | TBD | TBD | TBD |
| 5 | Whitened | TBD | TBD | TBD | TBD |
| 10 | Raw | TBD | TBD | TBD | TBD |
| 10 | Whitened | TBD | TBD | TBD | TBD |
| 20 | Raw | TBD | TBD | TBD | TBD |
| 20 | Whitened | TBD | TBD | TBD | TBD |

Main reading: anisotropy violates the theorem assumptions; whitening should restore the controlled geometry.
