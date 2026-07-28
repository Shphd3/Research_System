# Protocol: A06_02_01_E05 Margin-Basin Robust Initialization

## 0. Approval Snapshot

**Approval status:** approved by user in side conversation; execute now.

**Purpose:** test whether exact center initialization is required, or whether
any row initialization inside a positive-margin basin preserves routing.

**Primary anchor:** `../../../../problem_anchors/06_geometry_proxy_preservation/06_02_partition_preservation_dynamics/subanchors/06_02_01_finite_margin_basin_anchor.md`

**Anchor decision question:** is there a positive-margin basin around the
center row that preserves feature routing under early training?

**Anchor physical prior tested:** top-1 router regions are open sets, so small
row perturbations should preserve routing while positive margin remains.

**Anchor core model term tested:** minimum initial margin and matched-region
preserve fraction.

**Anchor falsifier:** small perturbations break preservation despite positive
initial margin, or preservation is unrelated to margin.

**Experiment role:** mechanism audit with method-facing implication.

**Primary metric from anchor:** final matched-region preserve fraction versus
minimum initial margin.

**Claim boundary from anchor:** controlled no-position bridge only.

**Minimal setup:** one-layer Transformer + top-1 MoE, 4 experts, no learned
absolute positional embedding, no B token, slot length 4, route on last slot
token, C0-C3, four seeds.

**Conditions to run:** pseudo center perturbation strengths
`0, 0.05, 0.1, 0.2, 0.35, 0.5, 0.7, 1.0`, plus oracle base guard.

**Pass:** nonzero perturbations preserve the original matched region whenever
initial margin remains positive.

**Fail:** preservation collapses under small positive-margin perturbations, or
negative-margin perturbations preserve equally well.

**Insufficient:** pseudo discovery or base preservation fails.

**Cannot claim:** real-DCLM behavior, semantic features, expert utility, or a
deployable label-free algorithm.

**Approval decision:** run the staged full experiment.

## 1. Anchor Alignment

This protocol directly tests whether the A06_02_01_E04 margin boundary implies a
basin of robust initialization around the center.

## 2. Tested Hypothesis

If a perturbation keeps initial margin positive, training should preserve the
original feature-to-expert region. If the perturbation removes margin, the
original region should fail or remap.

## 3. Rival Explanations

- Exact center direction is required.
- NMI stays high only because features remap to other experts.
- Random perturbation affects load but not feature regions.
- Training re-discovers the partition independent of initialization margin.

## 4. Data / Model / Algorithm / Objective

Same controlled no-position bridge as A06_02_01_E04. The target depends only on
feature identity. Feature, nuisance, and slot start are uniformly sampled.

## 5. Conditions, Seeds, And Checkpoints

Seeds: `20260623, 20260624, 20260625, 20260626`.

Cells: C0-C3.

Conditions:

- `oracle_rho0`
- `pseudo_rho0`
- `pseudo_rho0p05`
- `pseudo_rho0p1`
- `pseudo_rho0p2`
- `pseudo_rho0p35`
- `pseudo_rho0p5`
- `pseudo_rho0p7`
- `pseudo_rho1p0`

Checkpoints: step 0 and final step are sufficient for the primary judgment;
training still runs the same 1600-step objective.

## 6. Primary Metric

Final matched-region preserve fraction:

$$
P(T)=\frac{1}{F}\sum_f
\Pr_{h\in f}\left[\arg\max_e w_e(T)^\top h=e(f)\right].
$$

This is primary because it is identity-sensitive. NMI is secondary because it
does not care if all features move to different experts consistently.

## 7. Secondary Metrics

- initial matched-region preserve fraction;
- minimum initial margin;
- final minimum margin;
- feature NMI;
- max load;
- target accuracy and target loss.

## 8. Known Good / Known Bad / Known Confusing Cases

Known good: pseudo and oracle center initialization preserve C0-C3.

Known confusing: NMI can stay high even if the original expert identity is not
preserved.

## 9. Stage-Level Profiling Plan

| Stage | Question | Evidence | Rule |
|---|---|---|---|
| discovery | did pseudo centers recover route features? | pseudo NMI | must be high |
| step 0 | does perturbation stay in basin? | initial margin / preserve fraction | positive-margin candidates should preserve |
| final | does training keep basin assignments? | final preserve fraction | support if margin predicts preservation |

## 10. Algorithm Specification

1. Discover pseudo centers from route-position states.
2. Build the original pseudo center expert-feature matching.
3. Perturb rows by random-direction interpolation at each $\rho$.
4. Train for 1600 steps.
5. Measure initial and final margins, preserve fraction, NMI, load, and loss.

## 11. Success / Failure / Insufficient Evidence

Support: a broad perturbation interval keeps positive margin and high final
preserve fraction.

Failure: no basin exists, or margin does not predict preservation.

Insufficient: base pseudo center preservation fails.

## 12. What This Cannot Claim

No real-DCLM claim, no semantic expert claim, no utility claim.

## 13. Review Notes

Created after A06_02_01_E04 completed the controlled margin-crossing causal chain.
