# Layerwise head64 intervention

## 1. Problem Definition
Under the existing spectral position/semantic granularity owner, measure how replacing ONE Qwen3-0.6B-Base block residual-post by its own TRAIN mean plus first64 PCA components changes the final next-token prediction, across28 intervention layers. The researcher authorized this exact round in the current conversation. This measures intervention sensitivity, not intrinsic layer importance or a shallow/coarse to deep/fine order.

## 2. Physical Priors
Remaining blocks can transform or compensate a perturbation. Equal rank does not imply equal removed energy or intervention norm. Native middle-layer output-head reading may be mismatched.

## 3. Falsifiable Hypotheses
No depth order is assumed. Compare frozen original-top1 format/common-nonformat/other-nonformat groups across layers. Distinguishable depth patterns would establish bounded response differences; absent/uncertain patterns would not support such differences. Neither supports semantic hierarchy or stand-alone information sufficiency.

## 4. Mathematical Model
At layer L replace h by mu_L + Q_L Q_L^T(h-mu_L), then run the original remaining network and final norm/head. Q_L contains that layer's own TRAIN top64 vectors, or a fixed rank64 random basis; Q has zero columns for mean-only. All-prefix changes all valid preceding/current positions; target-only changes exactly the current position for one independently evaluated target. Primary outcome is equality of the final top1 ID to the no-intervention top1, first averaged within document/group and then over documents. It is not correctness. True successor NLL, full-distribution KL, retained centered energy and perturbation norm are distinct observations.

## 5. Computational Realization
Reuse R13's737 positions (700 natural/175documents and37/the) and tokenizer. Fit28 individual PCA references on the SAME60 R04 discovery documents and9600 positions. No evaluation PCA fitting. Cache untouched layer outputs once and continue only suffix blocks; qualify this mathematically equivalent computation with native-forward hook smoke. Per layer run head64, mean-only and3 fixed random64 subspaces in two separate scopes. Identity/full1024 are numerical guards. Legacy last-layer PCA is a separately named reference; middle raw/projected direct-head reading is diagnostic only.

## 6. Minimal Falsification Tests
Require checkpoint/token/prefix/shift/no-op equivalence and full-space reconstruction. Check same-rank random references, mean-only, energy and two intervention scopes. Report document bootstrap uncertainty, all failures and output-blind fixed examples. A failed identity/data interface makes dependent rows INVALID; wide/group-sparse intervals remain insufficient. A class-specific depth contrast is descriptive unless source/energy explanations are separately addressed.

## 7. Current Evidence
R13 final-layer head64 native decoding has already been measured; it cannot answer remaining-network compensation in earlier layers. R16 completed28layer independent fits,737positions and249843raw records. Natural-panel all-prefix vs target-only top1 preservation at layers1/7/14/21/28 is21.00/15.86/16.00/27.29/23.00% versus77.43/78.00/74.71/41.00/23.00%. Full-prefix depth response is nonmonotonic. All737native targeth/NLL reproduceR13exactly after correcting maximum-tie serialization; fixed categories unchanged. The original pre-run state wasNOT_RUN; [Summary](summary.md) owns actual measurements. See protocol.md and manifest.json for exact provenance; parent owner remains the sole mainline authority.

## 8. Claim Boundary And Next Decision
Exposed selected English panels, one frozen checkpoint and one reference cohort. No training, semantic hierarchy, causal feature mechanism or globally most-important layer claim. Researcher interpretation/acceptance remains Unknown. Deliver actual per-class layer curves and complete input/output cases for researcher reading before choosing another experiment.
