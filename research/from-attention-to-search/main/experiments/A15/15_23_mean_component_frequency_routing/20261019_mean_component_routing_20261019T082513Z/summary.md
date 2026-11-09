# Mean components and frequency routing: frozen analysis completed

The question was whether frequent CrossCoder features principally compose the true layer mean, and whether subtracting score means improves receipt of already present low-frequency features. The measurements distinguish representation means from score baselines; they do not establish expert learning or capacity gains.

A frozen Qwen3-0.6B Base and final joint-14-layer/F16384 CrossCoder were evaluated at block28 residual-post, before the original final RMSNorm. TRAIN has85,548 answer-prediction positions in1,024 dialogues; the previously exposed review has22,446 positions in256 dialogues. Four TRAIN-defined bands and their two relation subgroups remain fixed. All decomposition uses original hidden-state coordinates, including the preprocessing offset and decoder bias.

The highest-frequency band's signed projection on the TRAIN hidden-mean direction was−0.0931 on TRAIN and−0.0712 on review. The preprocessing offset contributed+1.4569 and the learned decoder bias−0.3362. These signed coefficients may be negative or exceed one: they are not energy shares. The proposed identification of frequent-feature contribution with the positive raw representation mean is not supported here. This does not imply frequent features are useless.

Review low-feature macro receipt was0% with raw R0,72.22% with ratio R1 (95% dialogue-bootstrap interval69.90–74.57%),17.58% with subtractive R2 (14.93–20.46%), and16.86% with both-stage R2b (14.07–19.63%). Of5,992 positions sent to the lowest band by R2,5,233 (87.33%) had no original activation in that band. Zero empty slots under R2b therefore cannot establish better target receipt. Each low-band feature had only1–17 TRAIN hits. Of1,694 low-band features,1,198 were observed on review and496 remainNA. Intervals use1,000 whole-dialogue resamples conditional on the frozen TRAIN definitions.

Target-layer-only centering and frozen re-encoding C left low-feature receipt at0%. Review per-coordinate MSE increased from33.59 to61.99 and mean activation count from304.69 to415.49. True final-layer h matched the original cache exactly at all107,994 positions; small BF16 gate differences are separately recorded. C remains confounded by changed encoder input distribution and degraded reconstruction.

AI proposal: retain only the R1 score hypothesis as a candidate for a separately authorized matched-budget learning comparison against R0. This is a next-decision proposal, not a learning verdict or training authorization. No expert, Base, or dictionary was trained; no external task was submitted and no commit/push was performed.

[Chinese summary](summary_cn.md) · [Detailed](detailed.md) · [Figures](figures_cn.md) · [Source tables](tables_index_cn.md).
