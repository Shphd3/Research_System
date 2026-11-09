# Token rarity versus all four feature-frequency bands

[Chinese explanation and all numeric contrasts](README_cn.md).

This is a descriptive redraw of the existing Tulu SFT EVAL aggregates, not a new experiment. At positions whose current token ID occurred once in TRAIN, lowest-frequency feature contribution share averaged 0.2655%, versus 0.04731% for IDs with TRAIN counts >=5: a 5.612-fold ratio and a 0.2182 percentage-point difference. Ratios for bands 2/3/4 were 1.222/1.006/0.987. All original token bins are retained; empty G2 stays NA and TRAIN-unseen current tokens remain separate. Original position-weighted Spearman is 0.259 (existing dialogue-bootstrap interval [0.228,0.285]); token-ID-equal correlation is 0.124. No intervals were estimated for the new endpoint arithmetic.

Feature frequency, current-token frequency, contribution share and hit rate are different quantities. Contribution share is shared activation times final-layer decoder norm, summed within a band and divided by the full dictionary amplitude sum. It does not measure semantic information, gradient interference, learning value or capacity. The endpoint comparison is not strictly monotonic across intermediate bins and is not a controlled causal effect. Most positions have zero lowest-band share. EVAL is already exposed. No inference, training, cache scanning, bootstrap or group changes were performed.

Representation location: the complete block28 residual-post output before final RMSNorm. The CrossCoder code z is jointly encoded from blocks 2,4,...,28; the table uses only the final decoder norm to form contribution shares. The prior SFT branch trains experts after block28 and before the frozen final norm/head, supervising answer and EOS next-token targets.
