# Low-frequency contribution concentration and domain correspondence

Question: do fewer low-frequency members carry reconstruction contributions in later interfaces, and do the dominant members increasingly correspond to document domain?

We reused native A22 shared activations, all 4,469 fixed DCLM low-frequency members, fourteen decoder interfaces, and 40 heldout math/biology documents. Each member contributes z times its layer-specific decoder L2 norm. Shares are normalized within the low-frequency group. K80 counts the members needed to reach 80% of that contribution; effective membership is 1 / sum of squared shares. Zero low contribution is undefined, not zero members. All layers use the same eligible source pairs; tiny positive totals are retained.

| Domain/source | First seven mean K80 | Last seven mean K80 | Paired change and 95% document interval |
|---|---:|---:|---:|
| Math, near high | 3.206 | 3.317 | +0.110 [0.044, 0.177] |
| Math, far high | 3.437 | 3.588 | +0.151 [0.075, 0.224] |
| Biology, near high | 4.170 | 4.597 | +0.427 [0.341, 0.521] |
| Biology, far high | 4.144 | 4.448 | +0.305 [0.220, 0.394] |

These descriptive changes point toward slightly more required members, not fewer. Effective-membership changes point in the same direction, although the math near-high interval crosses zero. Actual amplitudes produce more concentration than setting the same active members to z=1, but the actual distribution does not become more concentrated in the predefined depth comparison. The reference retains context-selected active lists and is not a context-free null.

Strict same-token-ID matching across different documents retains 178 near-high and 264 far-high anchors. The last-seven minus first-seven change in within-domain minus cross-domain cosine is +0.0239 [-0.0074, 0.0929] and +0.0234 [-0.0108, 0.0628]. These intervals do not establish depth enhancement. Word-shape-only matching gives more positive descriptive changes, but different words remain confounded, and the decoder-only reference gives similar changes. This does not establish fine-grained semantic or functional specialization.

Original near/far common support of 4,842 query/head cells becomes 4,795 after whole-pair, all-layer eligibility; all forty documents remain. Window sensitivity retains 3,212 cells. Full share vectors, matched triples, totals, active counts, figures and numerical checks are saved. Frozen discovery-selected display columns are preserved; an explicitly post-hoc addendum shows the complete active-member union of the same eight example rows.

All intervals are exploratory, pointwise document bootstrap intervals. No new p-values, forwards, training, dictionaries, interventions, candidates, resources or tasks were added. Human scientific acceptance remains unknown. [Chinese summary](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R05_distance_attention_20261028/low_frequency_concentration_20261028/summary_cn.md) · [Full evidence and figures](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R05_distance_attention_20261028/low_frequency_concentration_20261028/detailed_cn.md) · [Display addendum](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R05_distance_attention_20261028/low_frequency_concentration_20261028/display_addendum_cn.md).
