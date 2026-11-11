# R05: distillation and frozen student-atom routing

AI analysis; researcher judgment Unknown. All three new arms completed. A8 trains for 2000 updates from the shared initialization. A9 and A9d fork the complete native A0 state at update 1000 and add 1000 updates, replacing all eight layers or only layers 4–7. NLL is held-out negative log likelihood in nat, with lower values indicating better predictions. M measures actual hard Top-2 concentration in the same external teacher-atom coordinates; layers are averaged per atom before taking the atom median.

| arm     |      NLL |   M_median |
|:--------|---------:|-----------:|
| A5      | 4.039119 |   1.344968 |
| A0      | 4.083142 |   1.010460 |
| A1-deep | 4.085093 |   0.870829 |
| A9d     | 4.098041 |   1.026740 |
| A8      | 4.102006 |   1.113494 |
| A9      | 4.124848 |   0.967771 |
| A4      | 4.129442 |   0.810892 |
| A1      | 4.157604 |   0.585752 |
| A6      | 4.174997 |   0.924780 |
| A2      | 4.286028 |   0.256799 |

| pair   |   difference |   ci95_low |   ci95_high |
|:-------|-------------:|-----------:|------------:|
| A8-A0  |     0.018864 |   0.017118 |    0.020535 |
| A8-A5  |     0.062888 |   0.059057 |    0.066572 |
| A8-A4  |    -0.027435 |  -0.029164 |   -0.025726 |
| A9-A0  |     0.041705 |   0.039531 |    0.043695 |
| A9d-A0 |     0.014899 |   0.013455 |    0.016281 |
| A9-A9d |     0.026807 |   0.025567 |    0.028002 |

**None of the new arms beats native A0 at update 2000. A9d is better than A9 by 0.026807 nat, with a paired document interval [0.025567, 0.028002] for A9 minus A9d.** Frozen decisions are: P5 supported, P6 weakened, P7 insufficient because recovery is ongoing for both arms, P8 supported for both, and P9 supported. The last 250-update NLL drops, 0.085077 and 0.085756, exceed the preregistered 0.0817 threshold; this is why P7 is not classified as weakened.

Concentration changes relative to A0 are +10.20% for A8, −4.22% for A9 and +1.61% for A9d. The exact symmetric decomposition into conditional expert-slot distribution q and global load u is algebraic, not causal. Rounded mean M changes are approximately +0.139898 = +0.127172 +0.012726 for A8; −0.013685 = −0.038592 +0.024907 for A9; and +0.027357 = +0.024964 +0.002394 for A9d. These mean contributions do not decompose a difference of medians. The q term includes bias effects, and M ignores gate amplitudes.

Fixed-weight switching increases NLL by 1.105043 nat for A9 and 0.277600 for A9d. Atom-level Spearman correlations between route change and immediate loss increase are 0.487058 and 0.536567. Highest-quartile shock medians, 1.425312 and 0.411769, exceed lowest-quartile medians, 0.888983 and 0.203920. These meet P8, while gate changes, bias reset and routing changes remain joint interventions. A9 minus A9d estimates the conditional effect of adding early-layer interventions, rather than an additive independent layer contribution. Frozen dictionaries also drift: for example, A9 layer-0 normalized reconstruction error rises from 0.028965 to 0.278293, and A9d layer-4 error rises from 0.151707 to 0.458784.

The final interval's learned / forgotten / net-forgotten counts are 23765 / 240 / 456 for A8, 24291 / 164 / 293 for A9, and 24101 / 182 / 404 for A9d, among 29995 eligible atoms. Counts use at least 50 occurrences, BH q<0.05 and an absolute mean paired change of at least 0.01 nat. A8 history starts at update 250; self-routing histories start at the damaged post-switch update-1000 snapshot. From the common native update-1000 reference to each endpoint, learned / forgotten counts are 29125 / 226 for A9, 29262 / 205 for A9d, and 29281 / 212 for A0. Recovery below the old native-1000 level was observed for 29871 / 29915 atoms by update 2000, leaving 124 / 80 right-censored. Recovering an old baseline does not imply outperforming native update 2000. Atom tests remain descriptive because supports overlap and document dependence remains. A8 t50 has median 750, correlation −0.276977 with log frequency and −0.068577 with endpoint M; t50 is relative to improvement over updates 250–2000, rather than semantic knowledge acquisition.

AI interpretation: hard switching disrupts existing expert–input adaptation, especially when early layers are replaced. Training repairs much of this damage without overtaking native continuation. Gate 0.5, bias reset and dictionary drift remain credible competing explanations. An AI proposal, NOT RUN, is a fixed-weight late-layer selection-by-gate control before deciding the next main-model architecture. Architecture choice and new training remain for researcher discussion.

Only seed 17 was run. The 2000 paired resamples of 1871 documents measure evaluation sampling, not seed variance. A8 ran on four H100 GPUs; A9 and A9d ran on four RTX 5090 Reserved GPUs. Microbatch 16 with accumulation 2 changed to microbatch 8 with accumulation 4, preserving 262144 valid tokens per update and sample order. Read-only evaluation of identical native weights on the 5090 runtime changes aggregate NLL by +6.335e−6 / +3.396e−6 nat at updates 1000 / 2000. Minimum per-layer hard-set agreement is 99.5795% / 99.6124%; the 99th percentile of absolute position-loss changes is 0.0625 nat, so pointwise equivalence is not established. No native 5090 continuation was run, and hardware effects on training trajectories remain unresolved. The frozen primary baseline is unchanged. Evaluation uses FP32 weights with BF16 autocast and FP16 position-loss storage, rather than exclusively FP32 operators. Historical teacher BF16/FP32 Top-32 index overlap of 98.96% and exact-set agreement of 70.59% were not remeasured.

The diluted positive hint control remains below the 0.02 sensitivity threshold after four epochs (0.003803), while the full-hint control gives 1.016478. Detection power at the 0.04-nat scale therefore remains unestablished. The early A0@500 host's A5 hint gain is 0.000114, classified as not detected under the frozen rule, rather than an information upper bound. Five historical checkpoint-pair comparisons, or 55 overall and frequency-band intervals, remain BLOCKED because A0 position arrays and weights at 1250 / 1750 and A4 arrays and weights at 1500 were not retained. Aggregate curves and all primary endpoints are available. Missing intervals were neither imputed nor recovered by retraining old arms.

All requested tables, figures, recovery analyses, optional descriptive time-rescaling regressions, source identities and cost records are linked from the Chinese Detailed record. Job pt-kmzxmmyf SUCCEEDED and released its allocation. Each self-routing arm took about 77 minutes including initialization, evaluation and saving. The conservative total allocation across earlier H100 attempts and the 5090 run is 23.660797 GPU-hours, excluding queue time and counting MIG separately. Retained checkpoint families, dictionaries and actual evaluation caches are registered. The archive excludes model weights and position arrays. Researcher judgment remains Unknown.
