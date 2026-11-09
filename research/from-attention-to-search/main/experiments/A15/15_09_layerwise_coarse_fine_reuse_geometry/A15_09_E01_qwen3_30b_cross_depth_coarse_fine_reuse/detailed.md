---
experiment_id: A15_09_E01_qwen3_30b_cross_depth_coarse_fine_reuse
status: EVIDENCE_COMPLETE
completed: 2026-08-27
---

# Detailed Evidence: Qwen3-30B-A3B Cross-Depth Coarse--Fine Reuse

## 1. Frozen contract and provenance

- Model: `/data/share/Qwen3-30B-A3B`, 48 blocks, hidden width 2048, 128
  experts, top 8; inference only.
- Representation: final decision-token tensor received by each registered
  `block.mlp`, captured directly by a forward pre-hook.
- Blocks: 4, 12, 20, 28, 36, 44; one-based reporting.
- C4 primary source SHA-256:
  `4432e1493695542dd820c3e25483f81a31b10244bc1035c10ba1d15cd6b24f53`.
- C5 replication source SHA-256:
  `17619aa07e1b41f7d3ec36decf532f3a162240ca3f45e5925c574912a2d6e682`.
- Targets: mathematics and physics only.
- Fisher rank: 7; shared all-leaf Ledoit--Wolf within-class metric per
  panel/block/half.
- Nulls: 200 balanced template-cluster label permutations, seed 150901; 10,000
  Haar rank-seven pairs in dimension 2048, seed 150902.
- Protocol SHA-256 at completion:
  `18ba70cc8366fa201cd9b10368daf78b4c15d946779b0120acc646516ad4bc0a`.

The label-blind smoke used 16 rows from each panel. It captured a
\(6\times32\times2048\) tensor, had replay maximum absolute error 0.0, and read
no scientific metric.

## 2. Complete cell table

`Raw` is cross-half projector overlap, `C` is the empirical A/B
reproducibility reference, `A/C` is corrected overlap, and `Null50` is the
matched label-permutation median on the raw scale.

| Panel | Parent | Block | Raw | Null50 | C | A/C | \(R_C\) | \(R_F\) | Status |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| C4 | mathematics | 4 | 0.03294 | 0.04457 | 0.24403 | 0.13499 | 0.2258 | 0.2638 | Eligible |
| C4 | mathematics | 12 | 0.01416 | 0.03296 | 0.21475 | 0.06593 | 0.2013 | 0.2291 | Eligible |
| C4 | mathematics | 20 | 0.01318 | 0.03126 | 0.20903 | 0.06304 | 0.2175 | 0.2009 | Eligible |
| C4 | mathematics | 28 | 0.01507 | 0.03005 | 0.19490 | 0.07731 | 0.2138 | 0.1777 | Eligible |
| C4 | mathematics | 36 | 0.01218 | 0.02789 | 0.17730 | 0.06869 | 0.1981 | 0.1586 | Eligible |
| C4 | mathematics | 44 | 0.00942 | 0.01733 | 0.11140 | 0.08454 | 0.1024 | 0.1211 | Eligible |
| C4 | physics | 4 | 0.03257 | 0.03829 | 0.24084 | 0.13524 | 0.2258 | 0.2569 | Eligible |
| C4 | physics | 12 | 0.01798 | 0.02619 | 0.22153 | 0.08115 | 0.2013 | 0.2438 | Eligible |
| C4 | physics | 20 | 0.01664 | 0.02207 | 0.21298 | 0.07811 | 0.2175 | 0.2086 | Eligible |
| C4 | physics | 28 | 0.01611 | 0.01928 | 0.19437 | 0.08288 | 0.2138 | 0.1767 | Eligible |
| C4 | physics | 36 | 0.01474 | 0.01792 | 0.17094 | 0.08624 | 0.1981 | 0.1475 | Eligible |
| C4 | physics | 44 | 0.00649 | 0.01460 | 0.10884 | 0.05964 | 0.1024 | 0.1157 | Eligible |
| C5 | mathematics | 4 | 0.03858 | 0.04878 | 0.26697 | 0.14452 | 0.2565 | 0.2779 | Eligible |
| C5 | mathematics | 12 | 0.01690 | 0.03660 | 0.21813 | 0.07748 | 0.2019 | 0.2357 | Eligible |
| C5 | mathematics | 20 | 0.01538 | 0.03243 | 0.20432 | 0.07529 | 0.2110 | 0.1979 | Eligible |
| C5 | mathematics | 28 | 0.01572 | 0.02971 | 0.20558 | 0.07646 | 0.2124 | 0.1989 | Eligible |
| C5 | mathematics | 36 | 0.01409 | 0.02565 | 0.18358 | 0.07677 | 0.1998 | 0.1686 | Eligible |
| C5 | mathematics | 44 | 0.00796 | 0.01596 | 0.10766 | 0.07395 | 0.0957 | 0.1211 | Eligible |
| C5 | physics | 4 | 0.03669 | 0.04207 | 0.27062 | 0.13556 | 0.2565 | 0.2855 | Eligible |
| C5 | physics | 12 | 0.01781 | 0.02469 | 0.21901 | 0.08132 | 0.2019 | 0.2376 | Eligible |
| C5 | physics | 20 | 0.01775 | 0.02093 | 0.19827 | 0.08954 | 0.2110 | 0.1863 | Eligible |
| C5 | physics | 28 | 0.01574 | 0.01995 | 0.19514 | 0.08066 | 0.2124 | 0.1793 | Eligible |
| C5 | physics | 36 | 0.01645 | 0.01803 | 0.17617 | 0.09336 | 0.1998 | 0.1553 | Eligible |
| C5 | physics | 44 | 0.00703 | 0.01262 | 0.09778 | 0.07187 | 0.0957 | 0.0999 | Eligible |

All raw values are below their matched null median. Fifteen of 24 are below
the matched null 2.5th percentile. This is not a multiple-comparison global
test; it is the direct registered cell-level relationship to the null.

The Haar baseline has mean 0.0034173, median 0.0033703, and 95% interval
[0.0022091, 0.0048634]. Observed raw overlap exceeds the purely geometric Haar
scale but not the more relevant finite-sample label-permutation scale. The
common Fisher metric and finite panel geometry therefore matter materially;
Haar alone would overstate semantic reuse.

## 3. Registered cross-depth summaries

| Panel | Parent | Spearman \(\rho\) | Exact \(p\) | Shallow mean | Middle mean | Deep mean | Stage order | Middle extremum |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- | --- |
| C4 | mathematics | 0.029 | 1.000 | 0.10046 | 0.07017 | 0.07661 | shallow > deep > middle | minimum |
| C5 | mathematics | -0.771 | 0.103 | 0.11100 | 0.07588 | 0.07536 | shallow > middle > deep | none |
| C4 | physics | -0.486 | 0.356 | 0.10820 | 0.08050 | 0.07294 | shallow > middle > deep | none |
| C5 | physics | -0.600 | 0.242 | 0.10844 | 0.08510 | 0.08261 | shallow > middle > deep | none |

Cross-panel trajectory Spearman is 0.200 (exact \(p=0.714\)) for mathematics
and 0.771 (\(p=0.103\)) for physics. Mathematics does not replicate monotone
sign, full stage ordering, or middle-extremum type. Physics replicates negative
monotone sign and full stage ordering, but neither within-panel monotonicity
statistic is decisive and no non-monotone middle extremum exists.

## 4. Principal-angle evidence

The seven angle components are stored for every cell in `results.json` and
rendered in the heatmap. Across cells:

- best ordered component \(\cos^2\theta_1\): 0.0200--0.1093;
- top component share of total observed overlap: 30.2%--63.5%;
- top three share: 78.2%--93.7%;
- the seventh component rounds to zero throughout.

The heatmap supports the descriptive statement that the already-small overlap
is carried by a few ordered components, not uniform whole-space reuse. It does
not contain an angle-wise semantic-null verdict.

## 5. Execution and failure ledger

| Job | Resource | Outcome | Evidence role |
| --- | --- | --- | --- |
| `pt-q3jbbzgv` | 8x RTX 5090 SPOT | failed before persistent runtime log | execution-wrapper failure; no scientific output |
| `pt-fa73ufcc` | 4x RTX 5090 SPOT | runtime import passed, child lost exported path through a shell pipeline | diagnosed environment propagation; no scientific output |
| `pt-rdh3sq34` | 4x RTX 5090 SPOT | smoke and extraction passed; 24 cells computed; final JSON rejected one `numpy.bool_` | full evidence cache, record-layer failure only |
| `pt-diq3pdq9` | 4x RTX 5090 SPOT | `SUCCEEDED` | deterministic analysis resume, rendering, and completion audit |

The final successful job ran from 2026-08-27 16:58:43 UTC to 17:00:31 UTC.
The complete extraction was not repeated after the serialization repair.

## 6. Completion and visualization audit

- registered cells: 24;
- eligible cells: 24;
- invalid cells retained: 0;
- completion failures: 0;
- results SHA-256:
  `1bc024ee66a4955524d69de7ba3c85faf129c25a98a7659ce7ba72fe8da310a5`;
- all three figures were inspected at rendered resolution;
- corrected-trajectory and principal-angle figures retain their original
  0--1 scales and add numeric annotations rather than changing result-driven
  display thresholds.

## 7. Artifact map

### Curated artifacts

- [Summary](summary.md)
- [Protocol](protocol.md)
- [Raw-overlap figure](figures/figure1_raw_overlap_with_baselines.png)
- [Corrected trajectory](figures/figure2_corrected_overlap_trajectory.png)
- [Principal-angle heatmap](figures/figure3_principal_angle_cos2_heatmap.png)

### Worker evidence

Root:
`/data/250010109/MoE_Router/experiments/20260827_a15_09_e01_qwen3_30b_cross_depth_coarse_fine_reuse/runs/full-20260827T163900Z`

- `extraction/preflight.json`
- `extraction/smoke_receipt.json`
- `extraction/extraction_manifest.json`
- `analysis/results.json`
- `analysis/cells.csv`
- `analysis/null_ledger.json`
- `completion_audit.json`
- `logs/`

## 8. Interpretation boundary and next decision

The data disfavor a dominant shared-coarse coordinate account for conditional
fine discrimination. They are most compatible with a fine-residual geometry,
while providing only weak, parent-dependent descriptive support for a
layer-dependent account. Geometry alone cannot select a Router architecture.

The only next question is whether the coarse complement is functionally
sufficient and whether removing fine-specific residual directions is causally
harmful under frozen, cross-fitted evaluation. Router training remains outside
this result.
