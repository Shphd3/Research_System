# A14_E01 Detailed Evidence

## Setup

- ambient width \(d=128\), target rank \(k=8\);
- balanced binary forest depth 6 with 512 roots and 32,768 leaves;
- average aggregation, so \(\|A\|_2=1/\sqrt2\);
- target gain \(g\in\{0.5,0.9,1.0,1.1,1.5\}\);
- leaf noise \(\sigma\in\{0,0.01,0.03,0.1\}\);
- innovation ratio \(\delta\in\{0,0.01,0.05,0.1\}\);
- ten noisy seeds plus nine exact conditions;
- double-precision spectral calculations on CUDA.

Execution command:

```bash
python scripts/run_theory_synthetic.py \
  --config configs/exp1_theory_synthetic.yaml \
  --output-dir outputs/A14_E01_full
```

All 16 current unit tests pass; E01 itself was executed after the original
eight theory/operator tests passed.

## Primary Evidence

| Quantity | Observed | Registered rule | Verdict |
| --- | ---: | ---: | --- |
| maximum normalized bound violation | \(2.92\times10^{-8}\) | \(\le10^{-5}\) | pass |
| maximum exact relative rank-\(k\) error | \(2.83\times10^{-8}\) | \(\le10^{-6}\) | pass |
| registered conditions | 809 | complete grid | complete |
| layer records | 5,663 | complete layers | complete |
| deterministic counterexample checks | 17/17 | all exact | pass |

The gain comparison also passed in every informative paired condition: root
absolute residual at \(g=1.5\) exceeded that at \(g=0.5\). Relative tail energy is
nearly gain-invariant in this construction because both signal and registered
relative innovation scale with the shared gain; the protocol does not claim
otherwise.

## Boundary-Case Evidence

| Removed or changed assumption | Observed consequence |
| --- | --- |
| shared operator replaced by node-specific maps | rank 1 became rank 64 |
| average replaced by sum | \(\|A\|_2\) doubled from \(0.7071\) to \(1.4142\) and propagated absolute residual doubled |
| one orthogonal direction added per layer | numerical and 95%-energy rank grew from 1 to 9 |
| one child reused by \(q\) parents | \(\|A\|_2=\sqrt q\) for \(q=1,2,4,8\) |

## Bound Usefulness

At the root, the median values were:

| Leaf noise | Median tail energy | Median \(B/\|H\|_F\) |
| ---: | ---: | ---: |
| 0 | 0.0074 | 0.501 |
| 0.01 | 0.0089 | 0.809 |
| 0.03 | 0.0204 | 1.417 |
| 0.10 | 0.1345 | 3.345 |

This is direct evidence for a boundary, not a theorem failure: the universal
triangle/spectral-norm bound becomes loose or vacuous once off-subspace energy
is appreciable.

## Artifact Map

- row-level metrics:
  [worker metrics](../../../../../../../XingyuD/Attention_Search_Experiments/active/tree_low_rank/outputs/A14_E01_full/metrics.parquet)
- machine summary:
  [worker summary](../../../../../../../XingyuD/Attention_Search_Experiments/active/tree_low_rank/outputs/A14_E01_full/summary.json)
- counterexamples:
  [worker table](../../../../../../../XingyuD/Attention_Search_Experiments/active/tree_low_rank/outputs/A14_E01_full/counterexamples.csv)
- local central figures: [bound trajectory](bound_vs_actual.png) and
  [tail-energy heatmap](root_tail_energy_heatmap.png).

## Visualization Audit

The trajectory figure uses median values over ten seeds at
\(\sigma=0.03,\delta=0.05\); solid and dashed lines are actual error and bound
for the same gain/color. The dotted line in the relative panel is
\(\sqrt{0.05}\). The heatmap uses median root tail energy; shared color limits
are used across all leaf-noise panels. Neither figure is used to replace the
registered row-level pass condition.

