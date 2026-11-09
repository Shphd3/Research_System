# Project Dataset Registry

[中文入口](README_cn.md)

## Find a dataset by task

- **First/last list rules; sequential forgetting and joint learning:** [A17_04 data guide](A17_04_list_rule_mapping/README.md) ([中文](A17_04_list_rule_mapping/README_cn.md)). The matching result is E01/R02; the guide distinguishes the mother release, acquisition diagnostics and existing joint/mode views.
- **Coarse/fine semantic separability:** the A15 registry below preserves the established text-bank and representation-view identities.

## A15 Semantic-Separability Dataset Registry

This registry identifies the text banks and representation views used by the
A15 coarse/fine semantic-separability experiments. It is a provenance index,
not a copy of raw datasets or activation arrays.

## Counting Contract

Count three different objects separately:

1. **Fact source**: the proposition atoms from which prompts are written.
2. **Text bank**: the frozen prompt rows and labels used by an experiment.
3. **Representation view**: activations extracted from one text bank with a
   specified model, layer set, token, and hook.

Re-extracting the same text with another model does not create a new text
bank. Changing templates without changing proposition atoms creates a new
expression bank, but not an independent fact source.

## Controlled Coarse/Fine Taxonomy

The shared ontology has eight parent domains and eight fine classes per
parent. The original source provides six proposition atoms for each of the 64
parent--fine cells, or 384 atoms in total.

| Stable ID | Native identity | Rows | Cell design | Fact/expression change | Eligibility |
|---|---|---:|---|---|---|
| `TAX-BASE512` | `semantic_dataset.json` | 512 | 8 parents x 8 fine classes x 4 templates x 2 disjoint three-fact bundles | original 384-atom source | historical source and provenance |
| `TAX-T` | `registered_taxonomy.json:split=train` | 640 | 10 rows/cell | three original atoms per row | fitting only |
| `TAX-D` | `registered_taxonomy.json:split=development` | 640 | 10 rows/cell | three original atoms per row; different expression families | selection only |
| `TAX-C1` | `registered_taxonomy.json:split=confirmation` | 640 | 10 rows/cell | three original atoms; fresh confirmation expressions | opened; replay/diagnostic only |
| `TAX-C2` | `CONFIRMATION-v2` | 640 | 10 rows/cell | 320 two-atom and 320 four-atom rows | opened; replay/diagnostic only |
| `TAX-C3` | `CONFIRMATION-v3` | 640 | 10 rows/cell | 320 two-atom and 320 four-atom rows; fact subsets disjoint from C2 | opened; replay/diagnostic only |
| `TAX-C4E` | `C4-expression` | 1,920 | 30 rows/cell | all six original atoms; new templates and orders | opened expression-shift panel |
| `TAX-C4A` | `C4-atom` | 1,920 | 30 rows/cell | six additional Wikipedia-derived atoms per cell | opened fact-shift diagnostic; masked prose has naturalness limitations |
| `TAX-C5E` | `C5-expression` | 1,920 | 30 rows/cell | all six original atoms; another disjoint expression bank | opened expression-shift panel |

The eight formal panels `TAX-T` through `TAX-C5E` contain 8,960 prompt rows.
Including `TAX-BASE512`, the historical text lineage contains 9,472 rows.
These rows derive from two fact sources: the original 384 atoms and the 384
additional Wikipedia atoms used only by `TAX-C4A`.

### Canonical source receipts

| Object | Canonical path | SHA-256 |
|---|---|---|
| Original facts and `TAX-BASE512` | `/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/MoE_Routing_Experiments/active/a15_01_05_e01_qwen3_coarse_fine_semantic_variance_atlas/data/semantic_dataset.json` | `60236fcd675c307a38f1b1ae7b8b7712fa325f437937b6f8febebdaca3ee6bb1` |
| `TAX-T`, `TAX-D`, `TAX-C1` | `/data/250010109/MoE_Router/experiments/20260816_a15_08_02_e01_layerwise_conditional_fine_added_accessibility/runs/a15-08-02-e01-20260816-full/data/registered_taxonomy.json` | `c8b06af09791b5d3b859af058eb9264a32a28e0198b2a3bdf1054c4cbdf5991e` |
| `TAX-C2` | `/data/250010109/MoE_Router/experiments/20260819_a15_08_06_e02_hierarchical_taxonomy_replication/data_v2/confirmation_v2.json` | `9d62f50a709f9483169953c27508a7a1d27c970a70de180af33ca2eda1bb3bd9` |
| `TAX-C3` | `/data/250010109/MoE_Router/experiments/20260819_a15_08_06_e03_aligned_hierarchical_taxonomy_replication/data_v3/confirmation_v3.json` | `34bce8fa15e623dc3690af50fb22f4f229c6133ed0ceb71f24f5bb430c39b0c4` |
| `TAX-C4E` | `/data/250010109/MoE_Router/experiments/20260820_a15_07_e01_dual_track_heldout_spectrum/data_v1/controlled_c4_expression.jsonl` | `4432e1493695542dd820c3e25483f81a31b10244bc1035c10ba1d15cd6b24f53` |
| `TAX-C4A` | `/data/250010109/MoE_Router/experiments/20260820_a15_07_e01_dual_track_heldout_spectrum/data_v1/controlled_c4_atom.jsonl` | `cab867c3394d047822b896f6339412aa4b9d2568474715fa3f624767429f8226` |
| `TAX-C5E` | `/data/250010109/MoE_Router/experiments/20260820_a15_07_e02_fixed_axis_low_rank_atlas/data_v1/controlled_c5_expression.jsonl` | `17619aa07e1b41f7d3ec36decf532f3a162240ca3f45e5925c574912a2d6e682` |

## Active Qwen3-30B Representation View

| Stable view ID | Text bank | Model and object | Shape | Path | Status |
|---|---|---|---|---|---|
| `REP-Q30-C4E-GATEIN-L04-12-20-28-36-44` | `TAX-C4E` | Qwen3-30B-A3B, actual MLP/gate input at the final `Classification:` token | `[6,1920,2048]` | `/data/250010109/MoE_Router/experiments/20260827_a15_09_e01_qwen3_30b_cross_depth_coarse_fine_reuse/runs/full-20260827T163900Z/extraction/c4_activations.npy` | retain, active |
| `REP-Q30-C5E-GATEIN-L04-12-20-28-36-44` | `TAX-C5E` | Qwen3-30B-A3B, actual MLP/gate input at the final `Classification:` token | `[6,1920,2048]` | `/data/250010109/MoE_Router/experiments/20260827_a15_09_e01_qwen3_30b_cross_depth_coarse_fine_reuse/runs/full-20260827T163900Z/extraction/c5_activations.npy` | retain, active |

The adjacent C4/C5 metadata, split manifest, extraction manifest, and completion
receipts are part of each view's identity and must remain with the arrays.

## Secondary Data Families

| Stable ID | Rows | Role | Boundary |
|---|---:|---|---|
| `NAT-CLINC150-IS` | 22,500 | 10 known domains x 15 intents; official 15,000/3,000/4,500 splits | imported natural corpus; not generated taxonomy text |
| `NAT-MASSIVE-ENUS-5X4` | 6,318 | five scenarios x four intents; 4,389/778/1,151 splits | imported natural subset; imbalanced cells |
| `BIND-TAX-V2` | 19,200 | eight-card target binding; 11,520/2,560/2,560/2,560 splits | predicts eight parent labels, not within-parent fine classes |

The planned hidden two-level four-leaf teacher dataset has no formal generated
rows yet and is therefore not registered as an existing dataset.

## Retention And Deletion Policy

- Retain every canonical text bank, its source receipt, builder/audit manifest,
  and all metadata required to map an activation row back to text and labels.
- Retain complete formal-run representation caches while they support a
  canonical result or active reanalysis that would otherwise require another
  model forward pass.
- Treat old Qwen3-8B formal caches as historical evidence, not active Qwen3-30B
  data. Do not silently mix their hidden widths, hooks, tokens, or layers.
- Delete byte-identical superseded bundles, explicitly invalid pre-audit
  bundles, empty/incomplete analysis directories, and smoke-only outputs after
  a complete formal counterpart exists.

## Cleanup Receipt: 2026-08-30

The following non-canonical objects were deleted after a read-only provenance
audit. Their exact paths were checked before deletion, and their absence was
verified afterwards. The operation reclaimed approximately 11 MB; the retained
canonical text banks and Qwen3-30B representation views were then re-hashed.

| Deleted target | Reason |
|---|---|
| `.../A15_08_06_E02.../data_v1` | superseded by `data_v2`; the C2 text hash is identical and `data_v2` is a strict artifact superset |
| `.../A15_08_06_E03.../data_v3_invalid_pre_audit` | explicitly invalid pre-audit construction; valid C3 is in `data_v3` |
| `.../full-20260827T163900Z/analysis_incomplete_1787849947` | incomplete analysis with a complete formal counterpart |
| `.../runs/spectral-band-20260828T042753Z` | empty failed output with a complete formal counterpart |
| `.../runs/template-band-stability-smoke-20260828T045823Z` | smoke-only output with a complete formal counterpart |
