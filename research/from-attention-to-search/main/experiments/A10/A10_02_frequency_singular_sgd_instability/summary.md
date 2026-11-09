# A10_02 Frequency-Singular SGD Instability Summary

## Conclusion

The controlled run does **not** support the full 0701 claim that high-learning-rate SGD shows a clean late instability event after common-feature learning and singular concentration. In the main local boundary run (`high_lr=0.9`), no condition met the instability-event rule.

It **does** support a narrower and useful mechanism update: before clean divergence, high-learning-rate SGD can produce rare-prefix suppression together with stronger output-head spectral concentration and lower extra-feature rank. In the same setting, output-row clipping, output-row normalization, and label smoothing recovered rare accuracy and reduced the collapse signature.

Therefore the current A10 update is:

**Frequency-shaped spectral amplification is a plausible mechanism for rare-feature suppression under high SGD learning rate, but this run is insufficient to claim that it is the causal origin of high-learning-rate SGD divergence.**

## Terminology / Definitions

| Term | Plain meaning | Concrete object / computation | Why it matters | Cannot prove |
| --- | --- | --- | --- | --- |
| Main local boundary run | The primary run used for the anchor decision | `high_lr=0.9`, seeds `0,1,2`, 240 steps | Tests the edge between stable learning and rare suppression | Does not test all LR values |
| Remote stress run | A submitted SCO run with a larger high LR | `high_lr=2.0`, job `pt-c6a1nhsr` | Shows what happens when LR is clearly too high | Not a clean late-instability causal chain |
| Rare-prefix suppression | Common targets are learned but rare extension targets are not | Rare accuracy stays low while common accuracy is high | The strongest observed failure mode in the main run | Not yet real-language rare semantics |
| Extra-feature rank collapse | Prefix-extension hidden differences use fewer independent directions | Mean `extra_erank` decreases | Tests whether later features collapse into fewer directions | Not a proof of semantic collapse |
| Top-subspace reuse | Extra-feature directions project more into top output-head singular modes | Mean `extra_top2_mass` increases | Links rare suppression to spectral geometry | Not causal without stronger intervention |

## Setup

Data:
Nested-prefix next-token task:

\[
A\to AB\to ABC\to ABCD\to ABCDE\to ABCDEF\to ABCDEFG.
\]

Model:
One-layer, one-head causal next-token model with hidden dimension 32.

Main local run:
3 seeds, 240 steps, batch size 192, eval size 2048, safe SGD LR 0.25, high SGD LR 0.9.

Conditions:
`adamw_ce`, `sgd_safe_ce`, `sgd_high_ce`, `sgd_high_row_clip`, `sgd_high_row_norm`, `sgd_high_label_smoothing`, and `sgd_high_spectral_clip`.

## Main Results

| condition | stable rate | final eval loss | common acc | rare acc | top-SV growth | top-2 energy | top-band grad mass | extra erank | extra top-2 mass |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `adamw_ce` | 1.00 | 0.0007 | 1.000 | 1.000 | 1.91 | 0.413 | 0.352 | 4.68 | 0.303 |
| `sgd_safe_ce` | 1.00 | 0.0019 | 1.000 | 1.000 | 1.96 | 0.422 | 0.240 | 4.45 | 0.344 |
| `sgd_high_ce` | 1.00 | 0.5818 | 0.895 | 0.434 | 3.68 | 0.662 | 0.556 | 2.46 | 0.472 |
| `sgd_high_row_clip` | 1.00 | 0.0004 | 1.000 | 1.000 | 2.42 | 0.448 | 0.213 | 4.47 | 0.258 |
| `sgd_high_row_norm` | 1.00 | 0.0004 | 1.000 | 1.000 | 2.82 | 0.505 | 0.255 | 4.45 | 0.244 |
| `sgd_high_label_smoothing` | 1.00 | 0.1603 | 1.000 | 1.000 | 2.36 | 0.475 | 0.350 | 4.34 | 0.280 |
| `sgd_high_spectral_clip` | 1.00 | 0.4769 | 0.895 | 0.667 | 2.96 | 0.562 | 0.347 | 3.19 | 0.317 |

Primary readout:
`sgd_high_ce` did not diverge, but it had much lower rare accuracy (`0.434`) than AdamW, safe SGD, row clipping, row normalization, and label smoothing (`1.000`). This rare failure coincided with higher top singular-value growth (`3.68`), higher top-2 spectral energy (`0.662`), higher top-band gradient mass (`0.556`), lower extra-feature effective rank (`2.46`), and higher extra top-2 mass (`0.472`).

## Hypothesis Decisions

**H1: Frequency-gradient link.** Partially supported. Early frequency-gradient Spearman correlation was positive for unmodified AdamW (`0.964`), high-LR SGD (`0.464`), label smoothing (`0.607`), and spectral clipping (`0.571`). Row clipping and row normalization intentionally alter row gradients, so their correlations are not evidence against H1.

**H2: Common-to-spectrum temporal order.** Supported in the controlled run. Common accuracy rose quickly, while high-LR SGD showed stronger singular growth and lower rare-feature rank than safe baselines.

**H3: Instability localization.** Insufficient in the main local run. There was no qualifying late instability event at `high_lr=0.9`. The remote stress run at `high_lr=2.0` produced early spectral explosions, but those failures were too early to establish the full temporal causal chain.

## Remote Stress Result

SCO job `pt-c6a1nhsr` succeeded. It reran the same script with default `high_lr=2.0`, which is a stress run rather than the calibrated boundary run.

Stress result:
`sgd_high_ce` had stable rate `0.000`, mean instability step `12.33`, top-SV growth `3248.10`, top-2 energy `0.996`, top-band gradient mass `0.945`, rare accuracy `0.000`.

Interpretation:
The stress run confirms that very high SGD learning rates can cause early spectral blow-up, but because it often fails before clean common/rare learning, it is not the main evidence for the 0701 causal chain.

## Figure Reading Path

![Temporal profile](figures/local_full/temporal_profile.png)

This figure tests temporal order. `sgd_high_ce` shows higher top singular values and poorer rare behavior than AdamW and safe SGD, while row/smoothing probes recover the rare path.

![Spectral localization](figures/local_full/spectral_localization.png)

This figure tests spectral and token-gradient concentration. `sgd_high_ce` maintains the highest top-band gradient mass among the main conditions; row clipping and row normalization reduce the concentration.

![Extra-feature geometry](figures/local_full/extra_feature_geometry.png)

This figure tests whether prefix extensions remain independent. `sgd_high_ce` lowers effective rank and increases top-2 mass, while stable controls keep extension directions higher-rank.

## Claim Boundary

Can claim:
In this controlled nested-prefix task, high-LR SGD can enter a rare-suppression regime associated with stronger output-head spectral concentration and extra-feature rank collapse. Output-row clipping, output-row normalization, and label smoothing are useful causal probes because they rescue the rare path in the boundary run.

Cannot claim:
This does not prove that high-learning-rate SGD divergence in real LMs is caused by frequency-driven singular amplification. It does not prove that Adam works because it removes common directions. It does not update the MoE routing-preservation mainline.

## Next Decision

Run a focused LR/noise boundary experiment: map the transition from stable full learning -> rare suppression -> early spectral divergence across learning rate, batch size, and label noise. This directly connects to the seminar question about full-batch/noiseless, full-batch/noisy, and mini-batch/noisy regimes.
