# A14_02 Experiment Index

Primary anchor:
[A14_02 shared compositional rules and semantic-conditioned root rank](../../../problem_anchors/14_tree_low_rank_language_structure/14_02_relation_reuse_root_effective_rank/14_02_relation_reuse_root_effective_rank_anchor.md)

Chinese companion:
[A14_02 中文 anchor](../../../problem_anchors/14_tree_low_rank_language_structure/14_02_relation_reuse_root_effective_rank/14_02_relation_reuse_root_effective_rank_anchor_cn.md)

## Experiment Chain

| Experiment | Role | Status |
| --- | --- | --- |
| [A14_02_E01 shared rule versus lookup root rank](A14_02_E01_shared_rule_vs_lookup_root_rank/summary.md) ([中文](A14_02_E01_shared_rule_vs_lookup_root_rank/summary_cn.md)) | Root-cause and operationalization audit separating shared composition from exact frequency and lookup cardinality | Completed; formal verdict `insufficient` because both low-exposure primary conditions failed capability. Diverse contexts enabled capability, and lookup `K=1/4/16` gave functional ranks 10.2/11.0/12.8 among passing runs |
| [A14_02_E02 frequency--mapping rank separation](A14_02_E02_frequency_mapping_rank_separation/summary.md) ([中文](A14_02_E02_frequency_mapping_rank_separation/summary_cn.md)) | Isolate exact frequency inside one learned common mapping | Completed; 10/10 valid pairs, mean LowF-minus-HighF rank 0.2 directions, one-sided 95% upper bound 0.5 below the two-direction margin |
| [A14_02_E03 rare--common subspace reuse](A14_02_E03_rare_common_subspace_reuse/summary.md) ([中文](A14_02_E03_rare_common_subspace_reuse/summary_cn.md)) | Distinguish outside magnitude, old residual reuse, novelty, and exact endpoint function | Parked before full treatment; common AdamW step-space capture 0.478--0.631, 0/10 passed the 0.80 gate |
| [A14_02_E04 shared Jacobian/path image](A14_02_E04_shared_jacobian_path_image/summary.md) ([中文](A14_02_E04_shared_jacobian_path_image/summary_cn.md)) | Direct local H9 test at the trained checkpoint | Completed; local trained-task H9 supported in 5/5 seeds |
| [A14_02_E05 trajectory Jacobian closure](A14_02_E05_trajectory_jacobian_closure/summary.md) ([中文](A14_02_E05_trajectory_jacobian_closure/summary_cn.md)) | Test whether the actual eight-dimensional optimizer trajectory closes through the endpoint Jacobian image | Completed; closure refuted in 4/5 despite low-dimensional parameter and exact ROOT effects |
| [A14_02_E06 reference Jacobian versus secant](A14_02_E06_reference_jacobian_vs_secant/summary.md) ([中文](A14_02_E06_reference_jacobian_vs_secant/summary_cn.md)) | Separate reference H9 from finite-displacement H11 | Completed decisively; H11 refuted in 5/5, exact learned secant passed all eight-dimensional positive controls |

## Ownership Boundary

- A14_01/E08 owns the completed parameter--state bridge reconstruction.
- A14_02/E01 owns the matched shared-rule versus independent-lookup root-rank test.
- A14_02/E04--E06 own the H9/H11 bridge audit in the minimal trainable
  one-layer Transformer.
- Archived E02-v1 owns the failed strong component-recombination history under
  [`archive/e02_v1_component_recombination_capability/`](archive/e02_v1_component_recombination_capability/summary.md).
- Active E02 owns the exact-frequency non-inferiority result; active E03 owns
  the failed common-parameter-space operationalization and no rare treatment
  verdict.
- The current finite-training theory must use a secant/path-integrated image;
  a point Jacobian remains only a local bridge with a measured small remainder.
- Router and real-language transfer experiments are outside the current experiment.
