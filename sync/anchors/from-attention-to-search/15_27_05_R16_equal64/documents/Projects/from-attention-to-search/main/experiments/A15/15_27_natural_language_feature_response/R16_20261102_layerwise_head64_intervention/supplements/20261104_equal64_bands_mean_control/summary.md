派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R16_20261102_layerwise_head64_intervention/supplements/20261104_equal64_bands_mean_control/summary.md`。
[精确原始文件](../../../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R16_20261102_layerwise_head64_intervention/supplements/20261104_equal64_bands_mean_control/summary.md)；研究修改仍回到原件。

---

# Equal-rank spectral bands and the reference mean

**Main update:** when every band contains 64 directions and the reference mean is restored, the leading 64 directions have the highest observed original-top-1 retention at all 28 layers in both intervention scopes. The earlier late-layer advantage of retaining the remaining 960 directions does not imply that one equally sized later band is better. These are exploratory observations and bounded AI interpretations, not an accepted semantic hierarchy.

## Purpose and measurement

Read the experiment through behavior and factor controls, layerwise representation organization, and native intervention quality. The model is the same frozen official Qwen3-0.6B Base, with 28 blocks and hidden dimension 1024. Each layer uses its exact original R16 TRAIN mean and PCA basis. There is no new fit or training. The main panel has 175 documents and 700 natural positions; the auxiliary panel has 37 positions after `the`. They are reported separately and contain 180 physical documents in total. Both panels were previously exposed.

The 16 disjoint bands are PC1–64, PC65–128, through PC961–1024. At one block output, compare mean + (h − mean)P with (h − mean)P. Then continue the unchanged remaining blocks, final RMSNorm, and output head. Target-only and whole-prefix interventions are separate. Omitting the mean removes a fixed vector and changes the model's operating state. Standard affine PCA reconstruction is correct; attributing all of its prediction support to the 64 varying coordinates would be incorrect.

## Decisive observations

For target-only head64, retention with/without the mean at layers 1, 14, 25, and 28 is 77.43/17.71%, 74.71/40.71%, 34.29/12.71%, and 23.00/4.29%. For the whole prefix, the corresponding values are 21.00/1.00%, 16.00/1.86%, 30.14/1.86%, and 23.00/4.29%. Without the mean, head64 also attains the highest target-only retention at all 28 layers. It attains the whole-prefix maximum at 24 layers; the other four maxima are only 0.14–1.29%. These are descriptive sample rankings, not simultaneous-confirmation winners.

At the final layer, head64 with the mean retains 23.00%, versus 6.71% for PC65–128: paired difference 16.29 percentage points [12.86, 19.71]. The head64 difference between mean restoration and omission is 18.71 points [15.43, 22.15]. Intervals use 2,000 document bootstrap draws and are pointwise 95% intervals. The entire 16-by-28 matrix and all frozen frequency groups remain available.

Full-dimensional mean removal retains 100% of centered variation but preserves only 16.00% of original top choices at layer 1 and 33.29% at layer 28. It is not identity. Final full-centered NLL is 6.5937 nat, exceeding affine head64's 5.9027 despite higher top-1 retention; the original model gives 2.3418. Fidelity and actual-target prediction differ. At the final layer, head64, PC65–128, PC449–512, and PC961–1024 retain 41.44%, 8.72%, 3.61%, and 1.86% of centered energy. Equal rank does not match energy.

Final-layer head64 retention by original-choice group, with/without the mean, is 38.27/5.56% for format, 30.32/4.50% for reference-common nonformat, and 2.00/5.07% for other nonformat. The last group improves by 3.07 points [0.40, 6.00] without the mean, despite lower overall retention. This is a frequency-group observation, not a semantic-granularity effect. Every later affine rank64 band retains 0% in the other-nonformat group, whereas the inherited remaining960 condition retains 27.60%. Additional rank and energy remain competing explanations.

## Fixed text and interpretation

Case 211 ends with `Even triangles, the simplest of`. The current token is number 145, zero-based 144, ID315 ` of`; the actual successor is ID68159 ` polygons`. The full model chooses `polygons` with 40.45%. At layer 14, the final 64 directions plus the mean give 29.02%; mean-only already gives 29.28%. A concrete word here cannot be located in the tail from this output alone. At the final layer, affine head64 chooses `the` with 58.37%, centered head64 chooses `triangles` with 81.16%, and the full centered vector chooses `polygons` with 99.83%. Complete visible inputs, exact IDs, probabilities, and contrary examples are preserved in the casebook.

Storage/use: head64 is the strongest single rank64 block in the primary matrix. More later directions collectively support some predictions that head64 cannot maintain. Assuming later computations are more complex, broader joint support is plausible; additional dimensions, energy, and decoder geometry remain rivals. No distributed-knowledge or functional-interaction mechanism has been identified.

Granularity: a later single rank64 band does not replace the head at deeper layers. General patterns can participate in complex predictions. Shared variance, token frequency, semantic specificity, and computational complexity remain different objects. No external coarse/fine hierarchy was tested.

Compensation: intact earlier positions and the remaining network can produce a concrete candidate even when the current state is replaced by the mean. Compensation, retrieval, and later formation cannot be distinguished here. Whole-prefix interventions also change more states, so the scope difference is not a compensation estimate.

The sole next judgment is how much of the collective remaining960 advantage reflects accumulated dimensions/energy versus a specific contextual distinction. It does not authorize another run. Scientific acceptance and closure remain Unknown.

## Evidence and execution

Figures 01–05, the complete matrix, casebook, Detailed, assets/data guide, and reproduction record own the evidence. There are 1,403,985 unique new position-condition records, no PCA refits, and no parameter updates. Main job pt-pi9i0qnx succeeded on two authorized RTX5090 Spot GPUs; the two shards took 738.03 and 754.30 evaluation seconds, with approximately 1.6 GB peak memory per device. Frozen failures and engineering amendments are retained. Amendment E2 separately repairs five auxiliary-only singleton documents, preserving the entire main panel and every original chunk. Final validation and completion records own the repair count and integrity status. No H100, training, commit, push, or publication.

Final verification: all737 original states/outputs and old head64 comparisons are exact after the5 singleton repairs; main retention and its intervals are exactly unchanged; other serialized statistics differ by at most3.64e-12 (CSV roundtrip precision).9,525 replacement-version records are retained separately. In the other-nonformat group, head64 target NLL rises8.3413→9.3466nat withoutmean despite higher top1retention, so this is not an overall quality improvement.
