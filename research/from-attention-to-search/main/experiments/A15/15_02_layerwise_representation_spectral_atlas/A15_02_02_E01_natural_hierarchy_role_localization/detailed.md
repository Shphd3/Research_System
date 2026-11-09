---
experiment_id: A15_02_02_E01_natural_hierarchy_role_localization
status: completed
verdict: fail_universal_semantic_hierarchy_spectral_mapping
date: 2026-08-01
---

# Detailed evidence ledger

## 1. Decision question

Does semantic granularity in natural disciplinary hierarchies map reproducibly to covariance-rank bands in a current MoE Router input and in Qwen3-8B hidden states?

## 2. Corpus

- 32 triples spanning mathematics, physics, chemistry, biology, computer science, economics, medicine, linguistics, history, law, psychology, philosophy, engineering, astronomy, geology, ecology, statistics, AI, education, music, business, agriculture, political science, sociology, anthropology, public health, neuroscience, environmental science, materials science, architecture, geography, and literary studies.
- 12 calibration and 4 disjoint evaluation templates, balanced between child-first and parent-first orders.
- 384 calibration and 128 evaluation sentences (512 total).
- Each sentence labels root, mid-child, the same mid-parent, and leaf spans.
- Corpus SHA-256: `01f9d83a3aea5beb0ef80c52fcbd9cb95f3cd3906345d70715bee3db8706572a`.
- Full worker-owned corpus: `Projects/from-attention-to-search/XingyuD/MoE_Routing_Experiments/active/a15_02_02_natural_hierarchy_role_localization/data/hierarchy_corpus.json`.

Representative evaluation text:

> In an academic taxonomy, mathematics includes algebra as a major field, while algebra in turn includes linear algebra as a specialized field.

This is a controlled natural-language corpus built from real disciplinary taxonomies, not a sample of naturally occurring encyclopedia prose. That distinction is part of the claim boundary.

## 3. Models and representation surfaces

| Model | Frozen state | Layers | Width | Representation surface |
| --- | --- | ---: | ---: | --- |
| LB-80k MoE | checkpoint 80,000 | 1--12 | 768 | actual deployed linear-Gate input |
| Qwen3-8B | `/data/share/Qwen3-8B` | 1,5,9,14,18,23,27,32,36 | 4096 | post-attention, pre-MLP normalized hidden state |

Qwen3-8B is a dense reference model and has no MoE Router. Its result therefore supports or falsifies representation-level generality, not Gate behavior.

## 4. Data and interface gates

| Guard | LB-80k | Qwen3-8B |
| --- | ---: | ---: |
| calibration content tokens | 9,180 | 9,180 |
| evaluation occurrences | 512 | 512 |
| audited spans | 2,048 | 2,048 |
| span failures | 0 | 0 |
| maximum sequence length | 33 | 33 |
| child-first / parent-first evaluation records | 64 / 64 | 64 / 64 |

The two occurrences of each mid concept have identical token-id sequences within a sentence. Extraction hashes and tensor shapes are recorded in the worker manifests.

## 5. Spectral construction

For each model and layer, covariance is fit only on calibration content-token representations. Eigenvectors are sorted by decreasing eigenvalue. Fine bands F1--F12 each contain one twelfth of the rank; H=F1, M=F2--F5, and T=F6--F12. A separate 48-bin rank profile is used only for visualization.

The occurrence score is

\[
r_B(h)=\log\frac{\|U_B^\top(h-\mu)\|^2/\|h-\mu\|^2}{\sum_{i\in B}\lambda_i/\sum_i\lambda_i}.
\]

It measures relative spectral location, not task utility. The primary contrast is

\[
\Delta_B=r_B(\text{same mid as parent})-r_B(\text{same mid as child}).
\]

Inference uses 2,000 paired bootstrap draws over the 32 semantic chains and 256 random assignments of eigenvector ranks to bands.

## 6. Basis stability

Alternating-token calibration halves yield the following minimum H/M/T projector overlaps across layers:

| Model | H | M | T |
| --- | ---: | ---: | ---: |
| LB-80k | 0.843 | 0.898 | 0.955 |
| Qwen3-8B | 0.756 | 0.526 | 0.743 |

For reference, independent random subspace expectations are the rank fractions 0.083, 0.333, and 0.583. The fitted bands are therefore not random-half artifacts, although Qwen middle/tail bases are less stable than the MoE bases.

## 7. Descriptive root/leaf atlas

Both concept sets are absolutely head-dominated. At selected layers, H contains 70.6--76.6% of MoE activation energy and 64.5--92.9% of Qwen activation energy. Relative to calibration tokens, root concepts are less H-enriched and more M/T-enriched than leaf concepts in:

- LB-80k: H 10/12 layers, M 10/12, T 12/12;
- Qwen3-8B: H 9/9, M 9/9, T 9/9.

This is a descriptive concept-set result. Root and leaf phrases differ lexically and frequently differ in token count, so it is not the primary semantic-role test.

Figure contracts:

- [Rank-ordered projection profile](figures/rank_ordered_projection_profile.png): x is decreasing covariance rank in 48 equal-rank bins; y is percent centered activation energy; each line is chain-balanced root or leaf mean with a 95% chain bootstrap interval. It shows where energy lies but cannot isolate hierarchy from lexicon.
- [MoE atlas](figures/layer_granularity_spectral_atlas_lb80k.png) and [Qwen atlas](figures/layer_granularity_spectral_atlas_qwen3_8b.png): rows are model layers, columns are F1--F12, and color is chain-balanced log enrichment for root, leaf, or root-minus-leaf. They describe the layer × granularity × spectrum profile but do not establish causal semantic identity.
- [Rank-ordered enrichment profile](figures/rank_ordered_enrichment_profile.png): the same 48-bin x axis; y is log enrichment relative to calibration tokens. It separates absolute head dominance from group-specific relative enrichment.

## 8. Primary same-lexeme role result

There are 315 model-layer-band cells. The initial implementation treated same-sign child-first and parent-first effects as sufficient. Nineteen cells also excluded zero and exceeded the absolute q95 of the rank-assignment null. This was not sufficient to enforce the registered positional rival: several effects had very different magnitudes under the two orders.

Before the final claim, the guard was made explicit and fail-closed. A cell must now:

1. exclude zero under the chain bootstrap;
2. exceed the rank-assignment q95;
3. have the same sign and exceed the null in both orders;
4. have an order-interaction 95% interval that contains zero.

Only LB-80k layer 1 F7, F9, and F11 survive. Their parent-minus-child estimates are -0.247, -0.515, and -0.659. Qwen3-8B has no surviving cell. Since no corresponding effect replicates across models, the registered universal-mapping hypothesis fails.

The decisive Qwen layer-1 T candidate has child-first mean -0.833, parent-first mean -0.024, and order interaction interval [-0.885,-0.743]. Its apparent semantic effect is therefore dominated by causal left context or occurrence order.

The [same-concept heatmap](figures/same_concept_role_spectral_heatmap.png) marks pre-interaction candidates with `x` and strict single-model passes with `*`.

## 9. Failures and repairs

Three smoke failures were engineering-only and did not alter the scientific conditions:

1. the current MoE loader returned a `(model, config)` pair;
2. the MoE Gate input was flattened to `[batch × sequence, width]`;
3. bfloat16 tensors could not be hashed directly through NumPy.

The full analysis first failed after writing all raw CSVs because a plotting pivot omitted `depth_fraction`; finalization was rerun from those immutable CSVs without recomputing the model outputs. The final order-interaction guard implements the Protocol's pre-existing position rival; the original candidates remain preserved in `role_effect_candidate`.

## 10. Artifact map

- Approved Protocol: [protocol.md](protocol.md), [protocol_cn.md](protocol_cn.md)
- Chinese first reading path: [summary_cn.md](summary_cn.md)
- Main tables: [role contrast](tables/role_contrast_summary.csv), [layer atlas](tables/layer_granularity_spectral_atlas.csv), [48-bin profile](tables/rank_ordered_projection_profile.csv)
- Worker code and raw artifacts: `Projects/from-attention-to-search/XingyuD/MoE_Routing_Experiments/active/a15_02_02_natural_hierarchy_role_localization/`

## 11. Claim boundary and next decision

The experiment rejects a universal semantic-level-to-covariance-rank mapping under the present corpus and models. It does not show that hierarchy information is absent, that non-head bands are useless, or that a Router cannot learn a nonlinear hierarchy feature.

The sole next decision is whether to run an independent position-matched natural-relation corpus with the same target concept probed after the complete relation at an identical causal position.
