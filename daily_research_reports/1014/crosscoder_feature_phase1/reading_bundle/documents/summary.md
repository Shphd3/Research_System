# Feature relations and candidate learning objects: phase-one summary

## Purpose
Inspect whether joint feature relations persist across discovery/review subsets and provide readable candidate learning objects. Shared/separate learning effects remain untested.

## Model
Final frozen 14-selected-layer, F=16384 CrossCoder on frozen Qwen3-0.6B Base, using complete saved TRAIN threshold, normalization and original inference. Full 10,485,760-position window, 128-context blocks, seed 20261014: discovery 5,238,097 and review 5,247,663 positions. Complete sparse activations are saved; all 16,384 hit counts exactly match original final validation.

## Hypothesis
Common topic, lexical/format/context effects and high-frequency background remain candidate explanations. Composition lists are statistical proxies, not demonstrated causal components.

## Conclusion
214,711 discovery raw edges; 206,136 passed within-bin review (96.01%), 8,575 failed. The review-reduced graph has 146,947 edges. One search of 120,380,886 qualified pairs delivered four: 1/17 and 1/242 have discovery/review J=1/1; 0/3 and 0/4 have J=0/0. Review both-position counts are 2, 245, 0 and 7 respectively. Both high-J pairs share eight composition items, seven of which are Top10 frequency nodes (87.5%). Individual Top10 removals preserve these J values but cannot exclude joint background dominance. High composition-list overlap is distinct from direct pair coactivation and does not establish content similarity or learning benefit.

## Analysis
Review precedes exact transitive reduction; all four lists per formal pair are nonempty. Delivered 16 local graph facets, a 14-layer heatmap, candidate tables and 118 deduplicated per-pair text records with random/high labels. No both text exists for 0/3; only two positions exist for 1/17. Original-document and near-duplicate independence are UNKNOWN; VAL was previously exposed. Four pairs share two anchors, frequencies are unmatched, and they are not independent replications. Shared z makes layer-amplitude shares equal to decoder-norm shares, not causal contributions. Block28 FVE=86.4722%; replacement CE=+0.305962 nats. Next decision belongs to the researcher after text/background inspection; phase one stops without training or phase-two advancement.

Active analysis plus saved-count completion checks: 10.51 minutes, including the first failed 41.22-second attempt, below the 220-minute cap. Recorded peak disk 43.05 GiB and aggregate CPU RSS 11.41 GiB.

[Candidate metrics](../selected_tables/candidate_metrics.md), [texts](../selected_provenance/pair_examples.json), [figures](../figures_cn.md), [sensitivity](../selected_provenance/sensitivity.json), [full metrics](../selected_provenance/pair_metrics.json), [edge failures](../selected_provenance/edge_review_summary.json).
