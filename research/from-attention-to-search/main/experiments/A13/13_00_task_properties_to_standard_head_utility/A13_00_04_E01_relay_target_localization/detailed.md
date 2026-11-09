# A13_00_04_E01 Detailed Evidence

## 1. Causal Intervention

Both objectives used full Next-2 targets at auxiliary positions 0--3. Only the
relay-position target differed:

```text
background-MTP: [x2 x3 x4 x5 x5]
full-MTP:       [x2 x3 x4 x5 x6]
```

Here \(x_5=[ANSWER]\) and \(x_6=A\). Paths, tokens, labels, model, parameters,
loss weights, mini-batches, and all other auxiliary targets were matched.

## 2. Primary Effects

| Object | Mean | 95% paired bootstrap interval | Positive seeds |
| --- | ---: | ---: | ---: |
| \(D_{\mathrm{relay}}\) | 1.0343 nats | [0.4052, 2.0866] | 8/8 |
| \(D_{\mathrm{bypass}}\) | 0.1596 nats | [0.0831, 0.2446] | 8/8 |
| \(\Delta_D\) | 0.8747 nats | [0.2309, 1.8964] | 7/8 |

One interaction was negative (-0.2205); the other seven ranged from 0.2420 to
4.1686. The median interaction was approximately 0.519 nats, so the positive
decision is not solely an arithmetic sign caused by the largest seed, although
the mean magnitude is influenced by it.

## 3. Learning-Time Reading

| Path/objective | First-90% median step | Eligible crossings |
| --- | ---: | ---: |
| relay fixed-marker control | 340 | 7/8 |
| relay answer-aligned | 90 | 8/8 |
| bypass fixed-marker control | 130 | 8/8 |
| bypass answer-aligned | 70 | 8/8 |

The structural interaction is therefore visible in both the integrated NLL
metric and a plain threshold-time description.

## 4. Capability And Intervention Diagnostics

Final relay answer-aligned accuracy was 1.0 in 8/8 seeds. Fixed-marker mean
accuracy was 0.9567 but only 6/8 seeds met the registered 0.90 final threshold.
All capability-eligible models in both objectives had different-label donor
follow 1.0.

The performance estimand retained all paired seeds because the carrier was
validated before treatment. Causal-use sufficiency for the control arm remains
limited by only six eligible final models.

## 5. Artifact Map

- [Effects by seed](tables/effects_by_seed.csv)
- [Final metrics](tables/final_metrics.csv)
- [Relay intervention audit](tables/relay_patch_audit.csv)
- [Initial gradient diagnostics](tables/gradient_diagnostics.csv)
- [Learning curves](figures/objective_learning_curves.png)
- [Paired effect figure](figures/relay_interaction.png)
- Raw execution directory:
  `XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/outputs/a13_00_04_e01_relay_target_localization_full_20260716`

Runtime: 411.4 seconds on `cuda:0`.

## 6. Claim Boundary

The result establishes a one-position target intervention and a structural
necessity interaction. It does not distinguish answer alignment from generic
target variability; A13_00_05 owns that control.
