# A13_00_05_E01 Detailed Evidence

## 1. Exact Causal Contrast

The answer rule is \(Y=A\). Both objectives use the same targets at auxiliary
positions 0--3 and differ only at relay position 4:

```text
nuisance-aux: [x2 x3 x4 x5 B]
answer-aux:   [x2 x3 x4 x5 A]
```

\(A\) and \(B\) use the same 16 value tokens. Their per-token counts match exactly
in both train and evaluation splits: train counts are 12 or 13 for each value
under both targets; evaluation counts are 3 or 4 under both targets.

Both values are directly available to the relay. The task-level causal rule is

\[
Y(\operatorname{do}(A=a),\operatorname{do}(B=b))=a.
\]

## 2. Primary Effects

| Object | Mean | 95% paired bootstrap interval | Positive seeds |
| --- | ---: | ---: | ---: |
| \(R_{\mathrm{relay}}\) | 0.2315 nats | [0.1792, 0.2791] | 8/8 |
| \(R_{\mathrm{bypass}}\) | 0.0181 nats | [0.0029, 0.0359] | 6/8 |
| \(\Delta_R\) | 0.2134 nats | [0.1646, 0.2585] | 8/8 |

Every relay effect ranged from 0.0867 to 0.3347 nats. Every interaction ranged
from 0.0753 to 0.3060 nats. The conclusion is not controlled by one outlier.

## 3. Intuitive Learning-Time Result

| Path/objective | First-90% median step | Mean accuracy at step 100 | Mean accuracy at step 200 |
| --- | ---: | ---: | ---: |
| relay nuisance-\(B\) | 160 | 0.1635 | 0.9639 |
| relay answer-\(A\) | 60 | 0.9928 | 1.0000 |
| bypass nuisance-\(B\) | 60 | 1.0000 | 1.0000 |
| bypass answer-\(A\) | 50 | 1.0000 | 1.0000 |

## 4. Capability And Causal Use

Every objective/path cell reached final mean accuracy 1.0 with 8/8 seeds above
0.90. In both relay objectives, 8/8 models followed the label encoded by an
in-distribution different-label donor relay state with accuracy 1.0.

Therefore the primary interaction is not caused by an unlearnable control,
final capability mismatch, or a standard head that ignores the relay.

## 5. Gradient Diagnostics

At initialization, mean auxiliary shared-trunk gradient norms were 3.039 for
nuisance-\(B\) and 3.119 for answer-\(A\), a 2.6% difference. Mean answer/auxiliary
gradient cosines on the relay path were -0.0076 and -0.0044.

These diagnostics make a gross loss-scale explanation less likely, but they do
not prove that a particular parameter subspace or Jacobian path caused the
effect.

## 6. Split Association Boundary

The full generator samples \(A\) and \(B\) independently, but conditioning on the
held-out split creates observational association. The conclusion concerns the
known causal answer rule and matched target marginals, not zero mutual
information within the realized evaluation subset.

## 7. Artifact Map

- [Effects by seed](tables/effects_by_seed.csv)
- [Final metrics](tables/final_metrics.csv)
- [Relay intervention audit](tables/relay_patch_audit.csv)
- [Initial gradient diagnostics](tables/gradient_diagnostics.csv)
- [Learning curves](figures/objective_learning_curves.png)
- [Paired effect figure](figures/relay_interaction.png)
- Raw execution directory:
  `XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/outputs/a13_00_05_e01_task_relevant_target_full_20260716`

Runtime: 411.8 seconds on `cuda:1`.

## 8. Figure Contracts

### Learning-Curve Figure

- question: does answer-\(A\) supervision reduce ordinary-head loss earlier than
  nuisance-\(B\), and does the difference depend on relay necessity?
- metric/unit: standard-head answer NLL in nats per held-out example;
- data source: `trajectories.csv` from all eight paired seeds;
- aggregation: arithmetic mean at each registered 20-step checkpoint;
- axes/legend: optimization step on x, log-scaled NLL on y, bypass and relay
  panels, objective color in the legend;
- allowed conclusion: answer-aligned supervision learns faster and the gap is
  visually concentrated on the relay path;
- limitation: no seed uncertainty band, no final-task transfer, and spikes on
  the log scale are descriptive.

### Paired-Effect Figure

- question: are relay utility and its path interaction consistently positive
  across seeds?
- metric/unit: paired AULC differences in nats;
- data source: `effects_by_seed.csv`;
- aggregation: no cross-seed aggregation in plotted points;
- axes/legend: paired seed on x and utility on y;
- allowed conclusion: all relay and interaction signs are positive;
- limitation: the registered bootstrap intervals remain the inferential
  object, not visual line shape.

## 9. Claim Boundary

This establishes one controlled sufficient condition for earlier
task-relevant auxiliary supervision. It does not establish that the nuisance
control is a deployable MTP objective, that arbitrary future tokens help, or
that the condition transfers to code, language, long context, planning,
composition, or MoE.
