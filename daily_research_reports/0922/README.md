# 0922 SAE shared-direction reuse cycle

The active Focus for this date is:

- `focus_sae_shared_direction_reuse.md`

This cycle belongs to the local project repository `Projects/from-attention-to-search/`.

## Canonical project-local placement

The approved question is a local clause of parent A15_17, so the formal design should be a **subanchor**, not a new sibling parent:

```text
Projects/from-attention-to-search/main/problem_anchors/
  15_spectral_representation_and_functional_routing/
    15_17_three_model_sae_representation_trajectory/
      subanchors/
        15_17_01_sae_shared_direction_reuse_anchor.md
```

Its first read-only mechanism audit should live at:

```text
Projects/from-attention-to-search/main/experiments/A15/
  15_17_three_model_sae_representation_trajectory/
    A15_17_01_E01_shared_direction_reuse_audit/
      protocol.md
      summary.md          # create only after an eligible result exists
      summary_cn.md       # create only after an eligible result exists
      detailed.md         # create when execution/analysis is actually recorded
      figures/
      tables/
```

## Repository boundary

The GitHub connector used on 2026-09-22 has write access to the root
`Shphd3/Research_System` repository, but `Projects/from-attention-to-search/`
is a separate local project repository and is not present in the root Git tree.
Therefore the root Focus and project registry can be committed here, while the
canonical subanchor and protocol must be created from the local project checkout
(or from a connector that has that project repository installed).

Do **not** place a duplicate Anchor or Protocol under this date directory or
under `sync/`; those are not the canonical owners.
