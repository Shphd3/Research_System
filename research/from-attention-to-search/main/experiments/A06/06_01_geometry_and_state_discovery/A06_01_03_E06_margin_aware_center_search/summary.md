# Summary: A06_01_03_E06 Minimal-Prior M1/M2 Full Audit

Primary anchor:
`../../../../problem_anchors/06_geometry_proxy_preservation/06_01_geometry_and_state_discovery/06_01_geometry_and_state_discovery_anchor.md`

Protocol: `protocol.md`

## Purpose

Test whether the M2 continuous gradient-weighted sanity signal is stable across
8 controlled seeds under the minimal-prior rule: no feature labels, no position
labels, and no route-position prior during center selection.

## Exact Setup

Data is the A06 controlled no-position `C4_all_position_scope` bridge. Full
audit seeds are `20260623` to `20260630`. Each seed uses 12,288 calibration
sequences and 12,288 evaluation sequences. Conditions are raw all-token
k-means, route-only audit control, M1 static bootstrap margin, M2 continuous
gradient-weighted k-means, and M2 top-20% gradient-weighted k-means. M3 is not
run.

## Primary Metric

Held-out route-position `feature_NMI` decides whether frozen hidden-space
centers recover the controlled feature partition.

## Result

Full audit weakens the M2 continuous direction. The 2-seed sanity signal did
not hold at 8 seeds.

| Method | Mean `feature_NMI` | Min | Max | Mean max load | Mean active experts | Interpretation |
|---|---:|---:|---:|---:|---:|---|
| route-only control | 1.000 | 1.000 | 1.000 | 0.250 | 4.000 | positive control passes |
| raw all-token | 0.863 | 0.707 | 1.000 | 0.469 | 3.000 | stronger than expected baseline |
| M1 static bootstrap margin | 0.843 | 0.707 | 1.000 | 0.469 | 2.875 | does not beat raw |
| M2 continuous gradient weight | 0.784 | 0.621 | 1.000 | 0.530 | 2.750 | sanity signal not stable |
| M2 top-20% gradient weight | 0.756 | 0.637 | 0.866 | 0.606 | 2.625 | hard filtering remains weak |

Full table: `tables/full_method_aggregate.csv`.

## Interpretation

The positive control proves that feature centers remain discoverable when the
route pool is known. The failure is not task impossibility.

M2 continuous does not beat raw all-token or M1. It has some good seeds
(`1.000` on `20260627`, `0.866` on several seeds), but it fails badly on
`20260629` (`0.621`) and `20260628` (`0.637`). Its mean load is also worse than
raw all-token.

The shortcut guards do not show a simple position, slot, loss-bin, or
gradient-bin explanation. The more likely failure is that gradient-norm
weighting changes the all-token geometry, but not in a consistently
feature-controlling direction.

## Claim Boundary

Can claim: M1 and M2, as implemented here, do not provide a reliable
minimal-prior center-search method in the controlled bridge.

Cannot claim: no functional signal can ever work, no gradient method can work,
or real-DCLM preservation is impossible. This only falsifies the tested M1/M2
operationalizations.

## Next Decision

Do not proceed to preservation with M1/M2 centers. Next, analyze why raw
all-token becomes strong at full calibration size and whether the remaining
problem is sample size, center matching, or the absence of a true route-relevance
signal.
