# R03文本清单与配对

全部12情境为人工自然语言构造/受控编辑，非未修改自然语料。72文本先冻结，S01–S03/R01–R03共36实际执行，其他36 NOT RUN。每案例A/B相关线索、U星期编辑×近远；A/B/U目标/长度/位置/末5token匹配。完整token、offset、线索与候选保留执行侧。

| Case | Target / ID / position | Near / far gap | Candidates | Actual status |
| --- | --- | --- | --- | --- |
|R01|was / 572 / 82|7 / 51| Nora,  Felix|MEASURED6versions|
|R02|was / 572 / 86|7 / 53| Iris,  Hugo|MEASURED6versions|
|R03|was / 572 / 86|7 / 55| Vera,  Max|MEASURED6versions|
|R04|was / 572 / 84|7 / 53| Liam,  Zoe|NOT RUN,budget|
|R05|was / 572 / 85|7 / 53| Ethan,  Maya|NOT RUN,budget|
|R06|was / 572 / 88|7 / 55| Caleb,  Leah|NOT RUN,budget|
|S01|crane / 72947 / 84|6 / 50| flies,  lifts|MEASURED6versions|
|S02|bat / 15743 / 84|6 / 52| flew,  shattered|MEASURED6versions|
|S03|spring / 10464 / 85|6 / 54| starts,  bends|MEASURED6versions|
|S04|seal / 25349 / 83|6 / 52| swims,  melts|NOT RUN,budget|
|S05|bark / 53742 / 83|6 / 52| peeled,  echoed|NOT RUN,budget|
|S06|mouse / 8644 / 86|6 / 54| runs,  clicks|NOT RUN,budget|

[All72texts/tokens/pairs](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R03_same_token_coactivation/panel/tokenized_sequences.jsonl) · [36measured-input manifest](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R03_same_token_coactivation/panel/sequences_for_forward.jsonl) · [Qualification](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R03_same_token_coactivation/panel/qualification.json) · [Pre-response exclusions](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R03_same_token_coactivation/panel/exclusions.json).

SHA256:`57c1d0358b5128a116128f73514d6d855454bdb689e706c941ed76f6a27e01b9`. Final distances exclude right-padding. Moving filler changes order/recency. Single-token continuation candidates are predeclared compatibility readouts,not automatic truth. Different registry IDs do not establish document/template independence.
