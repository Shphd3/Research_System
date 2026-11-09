# Detailed: A06_01_01_E06 Common-Centered Residual Geometry Diagnostic

Primary anchor:
`../../../../problem_anchors/06_geometry_proxy_preservation/06_01_geometry_and_state_discovery/06_01_geometry_and_state_discovery_anchor.md`

Protocol:
`protocol.md`

Summary:
`summary.md`

## 0. Quick Recap

Purpose:
Diagnose why initialized synthetic hidden-state routing remains load-imbalanced after hidden common-centering.

Hypothesis:
After \(h_i=c+r_i\), the residual replay \(w_e^\top r_i\) can remain imbalanced because \(r_i\) has non-isotropic covariance, non-isotropic router cells, context / position structure, or finite-sample noise.

Experiment logic:
Reuse A06_01_01_E05 hidden-state extraction and final-router rows. Replay common-centered residuals, whiten residual covariance, compare to matched isotropic residual samples, stratify by context / position, and run a sample-count guard.

Conclusion:
Residual covariance / structured residual geometry is supported. Finite-sample noise is weakened as the main explanation. Matched isotropic replay sets a smaller nonzero router-cell / sampling floor.

Evidence:
Primary setting (`num_layers=1`, `post_ln`) has `centered_replay L=0.2577`, `centered_whitened_replay L=0.1071`, and `matched_isotropic_replay_mean L=0.0874`. The sample-count guard stays near `0.2694 -> 0.2577` from 256 to 4096 samples per pair.

## 1. Anchor Link And Decision Point

Anchor decision question:
After hidden common-centering, what explains the remaining step-0 load imbalance: residual hidden anisotropy, router-direction cell geometry, random-context / position structure, or finite-sample noise?

Decision after this run:
Common-centering is not enough. Residual covariance / structured residual geometry must be carried as an active mechanism into A06_01_02_E01. A06_01_02_E01 should be an oracle feature-level initialization positive control, not a label-free method attempt yet.

## 2. Protocol Compliance Audit

approved conditions match actual conditions:
Yes. The run includes `centered_replay`, `centered_whitened_replay`, `matched_isotropic_replay`, `context_position_stratified_replay`, and `sample_count_guard`.

primary metric exists:
Yes. \(L=m\max_e |p_e-1/m|\) appears in `tables/aggregate_by_condition.csv`, `tables/sample_count_guard_aggregate.csv`, and stratified tables.

central figures/tables exist:
Yes. Central figures are copied under `figures/`. Central tables are copied under `tables/`.

seeds/checkpoints recorded:
Yes. Eight seeds `20260521` through `20260528`; initialization / step 0 only.

known good/bad/confusing cases reviewed:
Yes. A06_01_01_E05 centered replay scale is reproduced; finite-sample-only interpretation is weakened; whitening is treated as diagnostic, not a proposed router.

success/failure/insufficient-evidence criteria applied:
Yes. A named residual source is separated; finite-sample noise is weakened; claim remains synthetic initialized replay only.

## 3. Setup

Data:
Synthetic `(slot,target)` pairs, four pair ids, strictly uniform 4096 samples per pair. Pair start is randomized. Background tokens are random and independent of pair id. Route position is the last slot position.

Model:
Initialized Transformer-MoE replay surface reused from A06_01_01_E05. Four experts. Dot-product top-1 router. No training.

Readouts:
`post_ln` and `pre_ln_replay`.

Depths:
`num_layers in {1,2,4}`.

Execution:
Local CUDA full run in the active experiment workspace.

Run command:

```bash
python scripts/run_a06_05_common_centered_residual_geometry_diagnostic.py \
  --config configs/a06_05_common_centered_residual_geometry_diagnostic.json \
  --run-name a06_05_full_20260621_1 \
  --run-stage full \
  --device cuda
```

## 4. Conditions

`centered_replay`:
Replay scores \(w_e^\top(h_i-c)\).

`centered_whitened_replay`:
Whiten \(r_i=h_i-c\) by an empirical covariance inverse square root with `whitening_eps=1e-5`, then replay the same router rows.

`matched_isotropic_replay`:
Generate isotropic directions with the same dimension, sample count, and empirical residual-norm distribution; run eight replicates per seed / depth / readout.

`sample_count_guard`:
Balanced subsampling / bootstrap over the centered assignments at 256, 512, 1024, 2048, and 4096 samples per pair.

`context_position_stratified_replay`:
Compute centered replay load by pair start and pair id, with a sampled background-token context table for debugging.

## 5. Primary Evidence

Primary readout:
`num_layers=1`, `post_ln`.

| Condition | Mean \(L\) | Std | Min | Max | Interpretation |
| --- | ---: | ---: | ---: | ---: | --- |
| centered replay | 0.2577 | 0.0896 | 0.0779 | 0.3684 | residual load to explain |
| centered + whitened replay | 0.1071 | 0.0371 | 0.0347 | 0.1470 | covariance control removes much of the load |
| matched isotropic replay | 0.0874 | 0.0323 | 0.0243 | 0.1280 | router-cell / sample floor is lower than real residual |

Derived effects:

- whitening reduction: `0.1506` absolute \(L\), about `58.5%` of centered residual $L`;
- isotropic gap: `0.1703` absolute $L$, about `66.1%` lower than centered residual $L`;
- route agreement with centered replay: whitening `0.4890`, isotropic first replicate `0.2505`.

Interpretation:
Whitening changes assignments substantially and reduces load close to the matched isotropic floor. This supports residual covariance anisotropy / structured residual geometry as a main source.

## 6. Depth And Readout Guard

Aggregate \(L\) by depth and readout:

| Depth | Readout | Centered | Whitened | Isotropic | Whitened / Centered | Isotropic / Centered |
| ---: | --- | ---: | ---: | ---: | ---: | ---: |
| 1 | post_ln | 0.2577 | 0.1071 | 0.0874 | 0.415 | 0.339 |
| 1 | pre_ln_replay | 0.2491 | 0.1104 | 0.0878 | 0.443 | 0.352 |
| 2 | post_ln | 0.3463 | 0.0638 | 0.0652 | 0.184 | 0.188 |
| 2 | pre_ln_replay | 0.3440 | 0.0571 | 0.0660 | 0.166 | 0.192 |
| 4 | post_ln | 0.2469 | 0.0717 | 0.0702 | 0.291 | 0.284 |
| 4 | pre_ln_replay | 0.2480 | 0.0723 | 0.0703 | 0.291 | 0.283 |

Observation:
The reduction is present at every depth and both readouts.

Interpretation:
The residual geometry explanation is not an artifact of a single normalization readout or layer count.

## 7. Finite-Sample Guard

Primary sample-count guard (`num_layers=1`, `post_ln`):

| Samples per pair | Mean \(L\) | Min | Max |
| ---: | ---: | ---: | ---: |
| 256 | 0.2694 | 0.0313 | 0.4805 |
| 512 | 0.2636 | 0.0332 | 0.4629 |
| 1024 | 0.2621 | 0.0430 | 0.4141 |
| 2048 | 0.2586 | 0.0483 | 0.3975 |
| 4096 | 0.2577 | 0.0779 | 0.3684 |

Observation:
The mean \(L\) is stable as balanced samples per pair increase.

Interpretation:
Finite-sample noise is not the main explanation for the observed residual \(L\) at this scale.

Boundary:
This is a bootstrap / subsample guard on the full generated dataset. It does not replace an infinite-population estimate from newly generated larger synthetic data.

## 8. Context / Position Evidence

Position-conditioned centered replay (`post_ln`) shows high conditional load:

- layer 1 mean conditional \(L\): about `1.70`;
- layer 2 mean conditional \(L\): about `1.59`;
- layer 4 mean conditional \(L\): about `1.41`;
- mean sample count per pair-start stratum: about `528.5`.

Pair-id-conditioned centered replay also has high conditional load:

- layer 1 mean conditional \(L\): about `1.14`;
- layer 2 mean conditional \(L\): about `1.22`;
- layer 4 mean conditional \(L\): about `1.33`.

Interpretation:
The residual hidden distribution is strongly structured by position and pair id. Because pair ids are uniformly balanced, pair-conditioned structure does not automatically imply aggregate imbalance. Position-conditioned structure is a serious boundary for label-free controls because the router may read non-feature contextual geometry.

Boundary:
The conditional strata are smaller than the full aggregate; conditional \(L\) should not be read as the same metric scale as the full aggregate without the sample-count guard.

## 9. Whitening Audit

Whitening used `eps=1e-5` and empirical covariance from the centered residuals. The top eigenvalue ratios are large enough to make anisotropy plausible. In the primary setting, the top eigenvalue ratio is typically about `0.15` to `0.19`, and effective rank is around `10.8` to `13.3` for 128-dimensional states.

Some `post_ln` covariance matrices have near-zero minimum eigenvalues, so whitening should be interpreted as a diagnostic control rather than a production transformation. The same reduction pattern appears in `pre_ln_replay`, where the positive minimum eigenvalues are larger and the condition estimates are less extreme.

## 10. Visualization Results

### Primary Residual Controls

![Primary residual controls](figures/residual_load_by_condition.png)

Purpose:
Test whether residual covariance / real residual geometry explains centered replay load.

Setup:
Eight seeds, `num_layers=1`, `post_ln`.

How to read:
Lower \(L\) means closer to uniform expert load.

Observed result:
Whitening and matched isotropic controls both reduce \(L\) sharply relative to centered replay.

Take-home:
Residual covariance / structured residual geometry is supported.

Remaining uncertainty:
The figure does not separate all possible structured residual sources; it only shows that common-centering alone is not enough.

### Depth Guard

![Residual controls by depth](figures/residual_load_by_layer_post_ln.png)

Purpose:
Check whether the residual-control pattern survives depth changes.

Setup:
Eight seeds, `post_ln`, depths 1, 2, 4.

Observed result:
Centered replay stays higher than whitened and isotropic controls at all depths.

Take-home:
The mechanism is stable enough to carry forward.

Remaining uncertainty:
This is still initialized replay, not trained dynamics.

### Sample Count Guard

![Sample count guard](figures/sample_count_guard.png)

Purpose:
Test whether the residual load vanishes with more balanced samples.

Setup:
Balanced bootstrap / subsampling at 256 to 4096 samples per pair.

Observed result:
Mean \(L\) stays near `0.26`.

Take-home:
Finite-sample noise is weakened as the main explanation.

Remaining uncertainty:
The guard is based on the full generated dataset; it does not create a new larger population estimate.

### Position-Stratified Replay

![Position-stratified replay](figures/position_load_spread.png)

Purpose:
Test whether pair-start position changes centered residual assignments.

Setup:
Centered replay grouped by pair start for `num_layers=1`, `post_ln`.

Observed result:
Position-conditioned loads are high.

Take-home:
Position-conditioned residual structure is real and should be protected against in label-free controls.

Remaining uncertainty:
The figure does not prove position is the causal source of aggregate load imbalance.

## 11. Known Good / Known Bad / Known Confusing Cases

Known good:
The centered replay scale is comparable to A06_01_01_E05's residual common-centered result, so the A06_01_01_E05 object is reproduced.

Known bad avoided:
The result does not treat centered replay load as a method success. It decomposes the residual source.

Known confusing:
Whitening changes representation geometry and assignments. It is a diagnostic intervention, not a final router proposal.

## 12. Artifact Map

Code workspace:
`Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/`

Runner:
`scripts/run_a06_05_common_centered_residual_geometry_diagnostic.py`

Config:
`configs/a06_05_common_centered_residual_geometry_diagnostic.json`

Result dir:
`results/a06_05_common_centered_residual_geometry_diagnostic/a06_05_full_20260621_1/`

Figure dir:
`figures/a06_05_common_centered_residual_geometry_diagnostic/a06_05_full_20260621_1/`

Curated project experiment dir:
`Projects/from-attention-to-search/main/experiments/A06/06_01_geometry_and_state_discovery/A06_01_01_E06_centered_residual_geometry/`

Key tables:

- `tables/aggregate_by_condition.csv`
- `tables/sample_count_guard_aggregate.csv`
- `tables/context_position_load_aggregate.csv`
- `tables/whitening_audit.csv`
- `tables/state_audit.csv`
- `tables/router_audit.csv`
- `tables/replay_audit.csv`

Key figures:

- `figures/residual_load_by_condition.png`
- `figures/residual_load_by_layer_post_ln.png`
- `figures/sample_count_guard.png`
- `figures/position_load_spread.png`

Checkpoints / logs:
No checkpoints. Local CUDA run; no ACP job id.

## 13. Claim Boundary

Can claim:
In initialized synthetic hidden-state replay, after removing the hidden common component, residual covariance / structured residual geometry explains a substantial part of the remaining load imbalance. Finite-sample noise is not the main explanation at the tested sample scale.

Cannot claim:
No claim about trained collapse, real text, DCLM, semantic specialization, expert utility, or deployable label-free control.

## 14. Next Decision

Proceed to A06_01_02_E01 as an oracle feature-level initialization positive control. A06_01_02_E01 should ask whether feature-level initialization can overcome the residual covariance / structured residual load diagnosed here. If A06_01_02_E01 passes, A06_01_03_E01 can test whether a label-free common/residual control can approximate the oracle. If A06_01_02_E01 fails, A06_01_03_E01 should not be promoted as a method and should instead become a failure decomposition.
