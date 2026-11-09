# Summary: A06_01_06_E04 Iterative Reservoir Direction Discovery

Primary anchor:
`../../../../problem_anchors/06_geometry_proxy_preservation/06_01_geometry_and_state_discovery/06_01_geometry_and_state_discovery_anchor.md`

Protocol: `protocol.md`

## Purpose

Test whether freezing a learned direction and training on the residual
discovers the next nested direction.

## Exact Setup

Run: `a08_singular_preservation_full_20260628_2`.

Seeds: `20260628-20260635`, 8 seeds, local CUDA.

Main conditions: `one_stage_common`, `two_stage_A_then_B`,
`three_stage_A_B_C`, `shuffled_residual_guard`.

Debug conditions added after failure: `oracle_two_stage_A_then_B`,
`oracle_three_stage_A_B_C`.

## Primary Metric

Primary metric: next-level alignment, defined as target child-feature alignment
minus overlap with previously extracted directions.

This decides whether the loop discovers a new direction rather than repeating
the old common direction.

## Result

Judgment: failed for the proposed iterative mechanism.

Key numbers:

| Metric | Value |
| --- | ---: |
| stage 1 A alignment | `0.7819` |
| learned stage 2 next alignment | `-0.1928` |
| learned stage 3 next alignment | `-0.1023` |
| shuffled guard alignment | `0.0061` |
| oracle A residual stage 2 alignment | `0.0567` |
| oracle A/B residual stage 3 alignment | `0.2601` |

The learned loop does not discover `B` or `C`. Oracle residualization shows that
even perfect removal of `A` gives weak `B`, while perfect removal of `A/B`
allows some `C` signal.

## Key Figure

### Figure: Iterative Alignment

![Iterative alignment](figures/a08_04_iterative_alignment.png)

Anchor question: can residual reservoirs discover nested directions
sequentially?

Observed result: learned residual stages have negative next-level alignment.

Allowed claim: the simple iterative loop is not supported.

What this does not prove: that no better staged objective or residual method can
work.

## Claim Boundary

Can claim: one-step common direction discovery works.

Cannot claim: repeated residual extraction works or should be moved to real
DCLM.

## Next Decision

Park the iterative-loop method. For the 06 mainline, proceed only with real
convergence/preservation audits that do not rely on A06_01_06_E04.
