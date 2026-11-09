# Binary feature occurrence by token position

Question: where are the fixed DCLM frequency groups active in the existing math and biology texts?

A22 produces one shared activation vector from fourteen jointly encoded layers. There is one binary event, z > 0, per feature and token. Its fourteen decoder interfaces do not provide independent activation events, so this analysis cannot measure a layer-local activation trend.

We completed descriptive statistics for 40 original heldout documents (20 per domain), all 192 positions per document, and all 16,384 coordinates. Four fixed groups contain 4,469 low-, 4,437 middle-, 4,451 high-frequency and 3,027 reference-low-support members. No decoder norm or Attention probability enters the binary event.

| Domain and source | All active members | Active low members | Low count / fixed low group | Low share of active members |
|---|---:|---:|---:|---:|
| Math, near high | 307.16 | 5.96 | 0.133% | 1.92% |
| Math, far high | 294.66 | 6.20 | 0.139% | 2.06% |
| Biology, near high | 290.81 | 8.59 | 0.192% | 2.95% |
| Biology, far high | 284.45 | 8.41 | 0.188% | 2.90% |

These are original near/far common-support document means. Shares are computed at each position before averaging, not by dividing the displayed means. Full five-distance results, exact absolute positions, six fixed position bands, query positions, middle-Attention controls, all original strata and window sensitivities are retained. Complete per-feature counts and weighted source activation rates include zero coordinates.

Intervals are descriptive, pointwise 95% paired document bootstrap intervals (5,000 draws); conditions with fewer than ten documents have no interval. No new p-values were computed. The heldout documents have been repeatedly inspected, so this is exploratory. Absolute positions mix different token identities and contexts and do not identify semantic progression. No new model forward, training, dictionary, candidate or task was created. Human mechanism acceptance remains unknown.

[Chinese numeric report and figures](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R05_distance_attention_20261028/activation_occurrence_by_position_20261028/summary_cn.md) · [Evidence and data ledger](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R05_distance_attention_20261028/activation_occurrence_by_position_20261028/detailed_cn.md).
