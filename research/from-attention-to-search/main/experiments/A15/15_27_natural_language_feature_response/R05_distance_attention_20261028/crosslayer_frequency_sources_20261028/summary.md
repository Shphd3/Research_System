# Actual cross-layer source contributions: question, answer, progress

Question: do far high-attention source positions allocate relatively more low-frequency member norm contribution to the last7 covered layers than near positions, beyond middle-attention distance changes? Native A22 joint shared z, all16384 coordinates, fixed DCLM frequency groups; no layer-independent activation.

Answer: estimates below are percentage points with paired document95%intervals. The first comparison is high far-minus-near deep-minus-shallow low norm share; the second subtracts its middle-attention counterpart. Read signed estimates with the pooled4-test BH values in the [primary table](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R05_distance_attention_20261028/crosslayer_frequency_sources_20261028/tables/primary4_tests.csv); positive estimates support the predicted direction, reliable negative estimates oppose it, zero-crossing intervals remain insufficient.

| Domain | High far-minus-near depth change (pp) | High minus middle depth contrast (pp) |
|---|---:|---:|
| math | +0.22 [-0.45, +0.93] | -0.00 [-0.44, +0.41] |
| biology | +0.21 [-0.49, +0.99] | +0.61 [+0.06, +1.19] |

Progress: complete applicable cache-only calculations, three primary figure types, full fixed-member/support tables, window32:192 sensitivity, original-model scale and other-stratum descriptive results. Primary support uses identical query/head intersections for near/far; five-bin figures use a separate five-bin intersection.20old heldout documents/domain, reused and repeatedly inspected; exploratory only. A is the zero-inclusive mean contribution per fixed member. B averages per-position group normsum/ALL-member normsum before head/query/document averaging. Contributions are linear L2norms, not squared powers. Fixed group sizes4469/4437/4451/3027. Native unit scaling cancels exactly in B.

No primary comparison passes pooled BH4. Low-frequency shares decline from shallow to deep averages: math near high8.32% to3.53%, far high7.75% to3.18%; biology near high8.29% to4.51%, far high7.99% to4.42%. Low-frequency member magnitudes nevertheless increase between these fixed depth halves; high-frequency magnitudes increase more. Greater low-frequency magnitude therefore does not imply a greater norm share. These observations do not identify a strong-Attention-specific allocation.

[Figure guide](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R05_distance_attention_20261028/crosslayer_frequency_sources_20261028/figures_cn.md) · [Detailed evidence](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R05_distance_attention_20261028/crosslayer_frequency_sources_20261028/detailed.md) · [Full data index](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R05_distance_attention_20261028/crosslayer_frequency_sources_20261028/data_index_cn.md).

No new model forward, fit, training, dictionary, candidate, task or resource. Source position, lexical and formatting composition remain observational rivals. No first formation, dynamic layer migration, independent layer activation, causal transmission, functional importance or explained variance follows. Human mechanism acceptance and next scientific decision remain Unknown.
