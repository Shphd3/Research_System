# Round 6 Final Summary

| Pair | Group A | Group B | Group C | deep agreement(B) | deep agreement(C) | length-vs-R corr |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| acp_lite_vs_hybrid | 0.246700 | 0.397900 | 0.355400 | 0.136649 | 0.129555 | 0.037604 |
| acp_lite_vs_quadratic_low_rank | 0.239600 | 0.416200 | 0.344200 | 0.072080 | 0.070275 | 0.062634 |

- In both pairs, Group B is larger than Group C. Second-order wins exist, but they are not the dominant divergence pattern on real WoS sentences.
- Length correlations are weak in both pairs, so the observed divergence is unlikely to be driven mainly by sentence length.
- Group C does not show a strong extra deep-layer agreement collapse relative to Group B, so routing disagreement appears broad rather than uniquely tied to second-order wins.
