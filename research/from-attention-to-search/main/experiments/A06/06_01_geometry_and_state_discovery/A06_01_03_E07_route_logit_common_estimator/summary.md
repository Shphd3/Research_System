# Summary: A06_01_03_E07 Route-Logit Common Estimator Under Random-Init Training

Primary anchor:
`../../../../problem_anchors/06_geometry_proxy_preservation/06_01_geometry_and_state_discovery/06_01_geometry_and_state_discovery_anchor.md`

Protocol: `protocol.md`

## Purpose

This experiment tests whether a routing-aware common-direction estimator can
make feature centers easier to recover from all-position hidden states during
random-init training.

The decisive question is narrow: does subtracting directions selected by
route-logit influence improve held-out route-position feature NMI over raw
all-position clustering and over simple controls?

## Exact Setup

- Controlled no-position A06 bridge.
- One-layer Transformer + top-1 MoE.
- 4 features, 4 nuisances, 4 experts.
- Feature slot length 4.
- Slot starts move across positions `[2, 10, 18]`.
- Route/evaluation position is the last token of the feature slot.
- No learned absolute positional embedding.
- Equal-norm random router initialization.
- Full run: 8 seeds, checkpoints `0, 5, 10, 100, 1600`.
- Fitting pool: all-position hidden states; evaluation: held-out route-position
  hidden states.

## Primary Metric

Primary metric:

\[
\Delta \mathrm{feature\_NMI}
=
\mathrm{feature\_NMI}_{\mathrm{estimator}}
-
\mathrm{feature\_NMI}_{\mathrm{raw}}.
\]

This metric decides the anchor because the mechanism claim is feature recovery,
not load change. Load, nuisance NMI, and slot-start NMI are guards.

## Result

**Verdict: not supported.**

The route-logit common estimator does not recover feature residual geometry
better than the controls. Across 40 seed-checkpoint cases, route-logit
subtraction is slightly worse than raw all-position clustering on average:

| Estimator | Mean feature NMI | Min feature NMI | Mean delta NMI vs raw | Mean delta margin vs raw | NMI wins / 40 |
|---|---:|---:|---:|---:|---:|
| route-only control | 0.995 | 0.807 | +0.166 | +3.862 | 36 |
| mean subtraction | 0.883 | 0.637 | +0.054 | +0.419 | 16 |
| raw all-position | 0.829 | 0.637 | 0.000 | 0.000 | 0 |
| load-sensitive ablation | 0.831 | 0.628 | +0.002 | +0.006 | 12 |
| route-logit subtraction | 0.815 | 0.637 | -0.014 | -0.080 | 12 |
| random-direction subtraction | 0.810 | 0.000 | -0.020 | +0.084 | 11 |
| top-PC subtraction | 0.798 | 0.637 | -0.031 | -0.598 | 10 |

The positive control matters: route-only clustering is near perfect, so the
feature geometry is still present. The failure is specific to the proposed
all-position route-logit common estimator.

## Key Figures

### Figure: Feature NMI By Estimator

![Feature NMI by estimator](figures/feature_nmi_by_estimator.png)

Anchor question: does route-logit common subtraction reveal feature centers?

Protocol question: does route-logit subtraction beat raw, mean, top-PC, random,
and load-sensitive controls on held-out route-position feature NMI?

Metric shown: feature NMI after fitting centers on the selected hidden-state
population.

Metric definition: normalized mutual information between true feature id and
assigned expert id on held-out route-position states.

Data source: 8 seeds x 5 checkpoints.

What this figure decides: whether the main estimator has a stable feature
recovery advantage.

Observed result: route-logit subtraction does not beat raw all-position
clustering overall; mean subtraction is the strongest non-oracle condition,
especially late.

Allowed claim: this route-logit estimator is not a valid feature-recovery
method in the controlled no-position bridge.

What this figure does not prove: it does not show that feature centers are
absent, because route-only control remains high.

Anchor update implication: weaken H1 and park this estimator unless redesigned.

### Figure: Load Change Does Not Imply Feature Recovery

![Load change by estimator](figures/load_change_by_estimator.png)

Anchor question: is routing-common removal different from load-only repair?

Protocol question: do directions that strongly change expert load also improve
feature NMI?

Metric shown: L1 change in expert load after subtracting selected directions.

Metric definition: \(\sum_e |p_e^{\mathrm{before}}-p_e^{\mathrm{after}}|\) on the
all-position fitting pool.

Data source: same full run.

What this figure decides: whether the route-logit estimator is mostly a
load-sensitive operation.

Observed result: route-logit and load-sensitive ablation change load, but this
does not translate into stable feature NMI improvement.

Allowed claim: load-driving directions are not sufficient feature-recovery
directions.

What this figure does not prove: it does not rule out a better routing-aware
selector with a different objective.

Anchor update implication: H3 is supported.

### Figure: Margin By Estimator

![Margin by estimator](figures/margin_by_estimator.png)

Anchor question: does subtraction create a stronger linear routing surface for
features?

Protocol question: does route-logit subtraction improve route-position margin?

Metric shown: held-out route-position raw-input margin from centers used as
router rows.

Metric definition: top-1 logit minus second-largest logit, evaluated on
route-position states.

Data source: same full run.

What this figure decides: whether NMI changes are supported by a stronger
linear separation surface.

Observed result: route-logit subtraction has a mean margin delta of -0.080
relative to raw; mean subtraction has a positive delta of +0.419.

Allowed claim: the proposed estimator does not create a better feature-routing
margin.

What this figure does not prove: it does not prove mean subtraction is a final
method, because its NMI gain is modest and controlled-only.

Anchor update implication: route-logit common subtraction fails the primary
mechanism test.

## Interpretation

The route-logit score selects router-contrast directions: each of the four
router contrasts appears in the selected subspace in every seed-checkpoint
case. That is exactly why it can affect load. But those directions are too
close to the current random router geometry: they modify router bias without
reliably exposing the feature partition.

The clean guard result is important. Nuisance NMI is essentially zero and
slot-start NMI is near zero for the tested estimators, so the negative result
is not explained by an obvious nuisance or slot-start shortcut.

## Claim Boundary

Can claim:

- In the controlled no-position bridge, this route-logit common estimator does
  not recover feature residual centers better than raw or simple controls.
- Load-changing directions are not enough to recover feature routing.
- Feature geometry is still present, because route-only control remains high.

Cannot claim:

- Real-DCLM behavior.
- Semantic feature discovery.
- Expert utility.
- That all routing-aware estimators fail.
- That mean subtraction is a final solution.

## Next Decision

Do not continue this route-logit estimator as the main path. The natural next
step is to return to center selection that directly optimizes held-out
route-margin geometry without using feature labels or route-position labels,
or to redesign the estimator so router-contrast directions cannot win merely
by changing load.

