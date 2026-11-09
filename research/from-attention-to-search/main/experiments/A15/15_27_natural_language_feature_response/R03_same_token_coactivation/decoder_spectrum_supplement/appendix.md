# Measurements, qualification and traceability

The [old explanation](old_analysis_explained.md) was written before new geometry/PCA results. The machine specification and code-freeze receipts record fixed choices; no new Protocol or clustering was created. Existing replicated R-02 (12), C-02 (64), C-03 (72) remain unchanged; C03 is primary and alone passed the old all-member context-support requirement.

## Original-space decoder cosine

Use only zero-based block 27 residual-post/pre-final RMSNorm. Individually L2-normalize original decoder vectors, without centering, whitening or projection. The primary statistic is the mean signed cosine across all unordered member pairs; absolute cosine is descriptive.

| Fixed group | Size | Mean signed cosine | Null median | Null 95% reference interval | p | BH3 q | Forced members | Median overlap |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| R-02 | 12 | -0.00616272 | 0.00047391 | [-0.00971633, 0.00776459] | 0.936 | 0.9360 | 2 / 12 | 5 |
| C-02 | 64 | 0.00107145 | 0.00093015 | [-0.00031956, 0.00223004] | 0.421 | 0.6315 | 16 / 64 | 37 |
| C-03 | 72 | 0.00175863 | 0.00048521 | [-0.00071431, 0.00188661] | 0.042 | 0.1260 | 15 / 72 | 39 |

Each of 999 random groups preserves size and exact counts in joint strata of half-octave V-frequency and exact V-hit-context count. The pool contains 492 coordinates with positive D/V frequency from the frozen 512. Within-group sampling is without replacement, but original members may recur. Within-stratum frequency/count ratios are at most sqrt(2), not exact continuous-rate equality. C03 has 15 forced members and median overlap 39/72. This is a conditional finite-universe comparison. Upper-tail p uses the plus-one rule, followed by BH across 3 groups. The 95% null interval is a random-group reference interval, not a confidence interval from independent feature pairs. All 999 draws are valid. [Results](provenance/geometry_results.json), [pairs](tables/geometry_pairs.csv), [matching](tables/geometry_matching.csv).

Same-group f12277/f5409 cosine=.02624925; cross-group f12277/f1478=.05605357. The posthoc minimum within C03 is f14425/f16335=−.12916811 and maximum f14425/f14893=.39910665. These examples do not establish universal direction independence or absence of similar pairs.

## Reference spectrum and distinct quantities

Fit one FP64 empirical train-centered covariance/eigendecomposition on 130712 raw BF16 positions from 128 contexts, with dimension 1024, at block 27 residual-post. Eval has 65402 positions / 64 contexts; it does not refit the basis. Held-out variance is eval's own centered covariance projected on the frozen train axes; mean shift is separately saved. Frequency never orders PCs.

Head ranks 1–128, middle 449–576 and tail 897–1024 have 128 dimensions each; the remaining 640 are separate. Train variance fractions are 63.4844%/4.9592%/1.9093%/29.6470%; eval fractions 57.5425%/5.9435%/2.6869%/33.8271%. C03 mean unit-direction fractions are 18.8868%/12.9174%/5.1386%/63.0571%; activation-energy weighting gives 33.6129%/8.6802%/2.4666%/55.2403%. The dimension reference is 12.5% per 128-dimensional band, not a semantic random-subspace classification result.

Direction fractions sum squared projections of a unit decoder. Activation weights use existing graph-D mean(z²)×native decoder norm². They are sums of separate-feature squared contributions, excluding cross terms; neither full-h explained variance nor energy of a group-decoded sum. The raw-h reference lacks continuous z, so the graph-D activation-weight source is explicitly separate. Shared-z decoded layer contributions are not independent layer activations. [Features](tables/spectrum_features.csv), [groups](tables/spectrum_groups.csv), [eigenvalues](tables/spectrum_eigenvalues.csv).

Raw-cache bytes and producer/hook source chain are verified, with source files separate from graph VAL. However, the old producer did not independently verify/save the Base hash. Original document/near-duplicate independence is unknown, and the dictionary saw those TRAIN sources. The result remains BOUNDED_SOURCE_CHAIN_MATCH, not independently hash-proven historical model identity. Old group-conditioned eigenvalue-only spectra cannot substitute for this common basis. [Cache audit](cache_audit_cn.md).

## Same controlled panel

Reuse 36 old sequences and fixed groups/basis. Per-feature edit energy is (Δz×native_decoder_norm)²; it is not the old D-scaled RMS endpoint. f12277 head/middle/tail fractions are14.7222%/13.9393%/5.4800%; same-group f5409 has10.3981%/15.6139%/2.4848%. S01_far C03 edit-energy fractions are 42.6867% head and 1.4768% tail, reflecting multiple changing members.

Counterexample 1: only f5409 changes in S02, hence near/far spectral fractions are identical while amplitude differs; this follows algebraically from a fixed direction, not range specialization. Counterexample 2: R01_far original-layer semantic energy=.720640878 versus unrelated=.765826884. The old six-positive cases/q=.03125 belongs to a different D-scaled metric and cannot be inherited. Existing failed continuation preferences remain failures. [Aligned features](tables/panel_spectrum_features.csv), [groups](tables/panel_spectrum_groups.csv). Spectral rank does not establish distance dependence, actual model use or expertise.

## Semantic discrimination is NOT RUN

No qualified independent-label/matching-raw-h/discovery-heldout combination was found. Available raw h has next-token or group/winner labels; old independently sourced E18 labels lack matching residual-post h. Two R03 A_far hook files do not make a semantic heldout set. Classifier fits, spectral-band semantic scores and random-subspace classification controls are all 0 / NOT RUN. This is a missing dependency, not negative semantic evidence. [Label audit](semantic_audit_cn.md).

Completing this item requires matched block 27 raw h for verified labeled discovery/heldout prefixes: at least N_discovery+N_holdout new forwards, plus required qualification replays. A qualified sample scope/count is not fixed, so no total is invented. Remaining forwards are 0; no budget increase or new run occurs pending confirmation.

## Execution and checks

The existing Qwen3/A22 dictionary's freshly verified SHA is `09b432e98dd7426f9ea4170809d75068a2ada2ed38c1e97d3fa18e119cd79628`. Source hashes and outputs are in the [manifest](artifact_manifest.md). Geometry took 46.65 elapsed seconds on CPU, including 25.92 seconds of checkpoint hashing; covariance/PCA/projection took 5.91 elapsed seconds on CPU, using 8 CPU threads. New model forwards, model/dictionary training, clustering and classifier fits are 0; PCA statistical fits=1. Cumulative forwards remain 1500/1500. No sealed TEST or new allocation.

Checks cover known artificial covariance, orthonormal basis, projection partition, covariance/eigenvalue traces, fixed eval basis, exact random-group margins and native decoder scale. They validate implementation, not semantics. Two independent code reviews found no numerical correction required and explicitly retained the original-layer versus D-scaled distinction and eval variance versus mean-shift energy distinction. Old sources/groups/results remain unchanged; mechanism acceptance and closure are Unknown.

Coverage: old explanation DONE_VALID; cosine/null DONE_BOUNDED; reference spectrum/projections DONE_BOUNDED; near/far alignment DONE_DESCRIPTIVE; semantic classifier/random-subspace controls BLOCKED by missing matched semantic input and zero forward budget.
