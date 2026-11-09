# A14_E06 Detailed Evidence

## Question

Does E05's split contrast survive when each parent contributes both adjacent
wrong boundaries with exactly equal weight?

Only parents with an interior gold boundary were retained. For each parent,
the left and right alternatives were

\[
b^-=b^{gold}-1,
\qquad
b^+=b^{gold}+1.
\]

The parent and ordered token sequence were identical in all three conditions.
Gold, left-shift, and right-shift maps were fitted separately. The control row
error was the average of the two alternative row errors before sentence-level
bootstrap resampling.

## Setup And Guards

- same Penn Treebank 70%/15%/15% file split and model revisions as E05;
- 8,192 training leaves;
- 3,500/500/480 train/validation/test interior parents;
- independent final EOS readout;
- strict frozen-leaf-space ordered output bottleneck;
- BF16 forward, float64 analysis, 1,000 bootstrap replicates;
- ridge grid \(10^{-6}\) through \(10^5\);
- same-token, disjoint-file, sample-shape, and ridge-interior guards all pass.

Execution:

```bash
python scripts/run_two_sided_split_robustness.py \
  --config configs/exp6_two_sided_split_robustness.yaml \
  --output-dir outputs/A14_E06_full
```

All 20 project tests passed, including the two-sided token-reconstruction test.

## Registered Results

| Model | Checkpoint | leaf \(r_{0.05}/d\) | gold error | left error | right error | two-sided advantage [95% interval] |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| Qwen | pretrained | 23/896 (2.57%) | 0.5161 | 0.5100 | 0.5290 | +0.0064 [-0.0525, 0.0631] |
| Qwen | initialization | 634/896 (70.76%) | 0.5772 | 0.6669 | 0.5140 | +0.0224 [0.0170, 0.0281] |
| Pythia | pretrained | 345/1024 (33.69%) | 0.4525 | 0.4002 | 0.5047 | -0.00014 [-0.0210, 0.0208] |
| Pythia | initialization | 343/1024 (33.50%) | 0.2144 | 0.3333 | 0.2176 | +0.2216 [0.2031, 0.2386] |

The Pythia pretrained-minus-initialization increment is -0.2217. Thus its E05
training-emergence story reverses under a direction-balanced parent subset.

## Direction Components

| Model/checkpoint | gold versus left shift | gold versus right shift |
| --- | ---: | ---: |
| Qwen pretrained | -0.0121 | +0.0243 |
| Qwen initialization | +0.1345 | -0.1230 |
| Pythia pretrained | -0.1307 | +0.1034 |
| Pythia initialization | +0.3567 | +0.0147 |

Opposite signs within the same parent are the decisive observation. A gold
syntax explanation predicts a consistent gold preference; the observed pattern
is compatible with directional position, length, and architecture geometry.

## Stability Frontier

| Model/checkpoint | selected bound | minimum eligible bound | compatible points |
| --- | ---: | ---: | ---: |
| Qwen pretrained | 1.4090 | 1.3061 | 0 |
| Pythia pretrained | 2.2309 | 1.4535 | 0 |

No point reaches the non-vacuity threshold. E06 therefore confirms rather than
repairs the propagation-bound failure.

## Artifact Map

- [machine summary](../../../../../../../../XingyuD/Attention_Search_Experiments/active/tree_low_rank/outputs/A14_E06_full/summary.json)
- [condition table](condition_summary.csv)
- [ridge frontier](../../../../../../../../XingyuD/Attention_Search_Experiments/active/tree_low_rank/outputs/A14_E06_full/metrics.parquet)
- [test parent records](../../../../../../../../XingyuD/Attention_Search_Experiments/active/tree_low_rank/outputs/A14_E06_full/Qwen__Qwen2.5-0.5B/pretrained/test_parent_records.parquet)
- [run manifest](../../../../../../../../XingyuD/Attention_Search_Experiments/active/tree_low_rank/outputs/A14_E06_full/run_manifest.json)
- local central figure: [two-sided robustness](two_sided_split_robustness.png).

## Visualization Audit

The first panel shows all four model/checkpoint aggregates and the 5% line.
The second exposes left/right components rather than hiding cancellation. The
third shows every validation-eligible Qwen frontier point, all below 5% and to
the right of bound ratio one. The figure therefore supports the registered
insufficient/fail verdict rather than selecting favorable strata.

## Claim Boundary

E06 tests adjacent boundary perturbations in one English treebank and two small
decoder families. It does not rule out nonlinear, node-conditioned, or
task-dependent composition. It does rule out using E05's Pythia aggregate as
evidence for a direction-independent, model-general shared-linear mechanism.

