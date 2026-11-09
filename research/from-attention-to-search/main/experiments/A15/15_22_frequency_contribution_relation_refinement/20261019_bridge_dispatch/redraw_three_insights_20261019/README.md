# Three insights: four concise figures

[Chinese interpretation, observations, allowed conclusions and design implications](README_cn.md).

Figures 1/2/2b redraw the new cached analysis: TRAIN-defined four-band memberships versus EVAL mean final-decoder contribution share; held-out pair-weighted signed phi versus 20 frequency-matched random groupings; and separate split-half membership stability with actual two-group sizes. U remains outside the four positive-frequency bands but inside the contribution denominator. Singleton phi remains NA, not zero. Panel-specific phi scales and random min/max ranges are explicit.

Figure 3 shows only old Tulu SFT T_S1 epoch1, seeds 11/22: natural-region NLL minus zero-branch NLL, with the existing 1000-draw dialogue-bootstrap 95% descriptive intervals. Experts 1/3 improve in both seeds; expert 7 worsens in both; other intervals cross zero or differ by seed. Epoch 1 is posthoc, EVAL exposed, and there is no multiplicity-adjusted guarantee. This is not evidence that the new final-layer routing learns better, and does not replace the fixed epoch 3 result.

The redraw does not execute inference, training, coactivation counting or new resampling. No coactivation, activation-count or receipt statistic is interpreted as gradient interference, learning value or capacity. Existing files remain unchanged. Full copied numeric sources and provenance hashes are in tables/ and manifest.json. PNG/SVG/PDF are provided for every figure.

[Supplement: token rarity contrasted across all four feature bands](token_rarity_contrast/README.md). Existing EVAL aggregates only; no new experiment.
