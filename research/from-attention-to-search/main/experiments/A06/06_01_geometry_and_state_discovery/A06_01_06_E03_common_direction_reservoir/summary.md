# Summary: A06_01_06_E03 Common Direction Split Reservoir

Primary anchor:
`../../../../problem_anchors/06_geometry_proxy_preservation/06_01_geometry_and_state_discovery/06_01_geometry_and_state_discovery_anchor.md`

Protocol: `protocol.md`

## Purpose

Test whether sending the converged common projection to a common branch and the
residual to a reservoir branch protects tail learning.

## Exact Setup

Run: `a08_singular_preservation_full_20260628_2`.

Seeds: `20260628-20260635`, 8 seeds, local CUDA.

Conditions: `ce_baseline`, `update_suppression_only`,
`common_residual_split`, `capacity_matched_random_split`, `oracle_split`.

## Primary Metric

Primary metric: tail loss improvement over CE, with capacity guard and
\(\alpha_{\mathrm{tail}}\) guard.

\(\alpha_{\mathrm{tail}}\) means the fraction of the tail update that lies in the
common direction. Lower is better only if tail loss also improves and the
capacity guard does not explain the improvement.

## Result

Judgment: insufficient / weakened for the proposed mechanism.

What moved: common/residual split improved tail loss and reduced
\(\alpha_{\mathrm{tail}}\).

What failed: the capacity-matched random split improved tail loss even more, so
the observed gain cannot be attributed to the common/residual mechanism.

Key numbers:

| Metric | Value |
| --- | ---: |
| CE tail loss | `0.4098` |
| common/residual tail loss | `0.3114` |
| common/residual tail improvement | `0.0984` |
| common/residual alpha reduction | `0.1558` |
| common/residual common-loss regression | `-0.0354` |
| capacity-random tail improvement | `0.1596` |

## Key Figure

### Figure: Split Results

![Split results](figures/a08_03_split_results.png)

Anchor question: does common/residual split protect tail learning because it
removes the common direction from the reservoir?

Observed result: the proposed split reduces alpha and helps tail loss, but a
random split helps tail loss more.

Allowed claim: forward splitting changes learning and can reduce measured
common-subspace tail updates.

What this does not prove: that the r1 common/residual mechanism caused the tail
loss improvement.

## Claim Boundary

Can claim: split-forward is an active intervention worth diagnosing.

Cannot claim: common/residual split is the mechanism or a validated method.

## Next Decision

Do not promote A06_01_06_E03 into the real-DCLM preservation method. Revise the method
or metric so it beats a capacity-matched random split.
