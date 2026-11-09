---
experiment_id: A15_02_02_E01_natural_hierarchy_role_localization
status: completed
verdict: fail_universal_semantic_hierarchy_spectral_mapping
date: 2026-08-01
---

# Spectral location of natural coarse and fine concept tokens

## Conclusion

The experiment does not establish a cross-model mapping from semantic hierarchy level to a fixed covariance-rank band. Coarse/root and fine/leaf concept sets have reproducibly different descriptive spectral profiles: both are dominated by covariance-head energy, while root tokens are relatively more enriched in middle/tail bands at most layers. However, the same-lexeme parent-versus-child contrast does not survive the occurrence-order guard in Qwen3-8B and does not replicate across models. Lexical composition, span length, and causal left context therefore remain stronger explanations than semantic hierarchy itself.

## Setup

The controlled natural-language corpus contains 32 three-level disciplinary chains, including `mathematics → algebra → linear algebra`, 12 calibration templates, and 4 held-out evaluation templates (512 sentences total). Each sentence labels root, mid-as-child, the same mid-as-parent, and leaf spans. Covariance bases are fit on 9,180 calibration content tokens. Evaluation uses 128 sentences and 512 labeled occurrences per model.

The frozen models are the 12-layer width-768 LB-80k MoE and local Qwen3-8B. The MoE surface is the actual linear-Gate input. Qwen3-8B provides a dense-model representation comparison using post-attention, pre-MLP normalized states at nine depths. No fine-tuning or continued training is performed.

## Metrics

- Projection-energy share is the percentage of centered activation energy in a rank interval.
- Log spectral enrichment compares that share with the covariance energy share of ordinary calibration tokens; 0 means baseline, \(+0.69\) is approximately 2x baseline.
- The primary contrast is the log-enrichment difference between the same mid concept used as a parent and as a child in one sentence.

## Result

Across selected depths, H (the top \(1/12\) of directions) contains 70.6--76.6% of MoE concept-token energy and 64.5--92.9% of Qwen concept-token energy. Root tokens are relatively less head-enriched and more middle/tail-enriched than leaf tokens in almost every observed layer, but this comparison does not control lexical identity.

Among 315 model-layer-band cells, 19 were candidates before the occurrence-order interaction guard. Only MoE layer 1 F7/F9/F11 survive the strict single-model guard; Qwen3-8B has no surviving cell and no effect replicates across models. The registered universal-mapping hypothesis therefore fails.

![Rank-ordered projection profile](figures/rank_ordered_projection_profile.png)

![Same-lexeme role contrast](figures/same_concept_role_spectral_heatmap.png)

## Boundary and next decision

The result describes concept-set energy profiles and rejects a universal semantic-level-to-covariance-rank mapping under this corpus. It does not show that hierarchy is absent from the representation, that Router uses these bands functionally, or that spectral routing improves training.

The sole next decision is whether to run an independently sourced, position-matched natural-relation corpus in which the same target concept is probed after a fully observed parent/child relation at an identical causal position.

See [the detailed evidence ledger](detailed.md) and the [Chinese summary](summary_cn.md).
