# Dataset identity and reproducibility / 数据与可复算入口

The editable research owner is R17 in from-attention-to-search. Payloads remain at `/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02`. 本页只索引本轮确实读取／生成的对象，不代表新独立确认。问题与结论见[Summary](summary_cn.md)。

| Object / 对象 | Identity and actual scope | Saved source |
|---|---|---|
| Constructed panel / 构造面板 |384 rows;48 families;24/12/12 grouped split; SHA256 `dc2c3a58d056bdb20ffecbcbda57fa0b9afca1254e673b41e6271bf2263c5ace`;19 notation-corrected rows; exposed heldout | [full text, labels, token IDs](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/shared/panel.jsonl) |
| Panel metadata |12 theorem groups split6/3/3;96 nonmatrix controls; coarse Unknown | [manifest](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/shared/data_manifest.json) |
| Frozen model/dictionary/code |Qwen3-0.6B-Base official; A22 checkpoint000999997440;14 odd layers;16384 atoms | [hashes](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/shared/models/input_fingerprints.json) |
| Responses |384 target positions; rawz/h/decoder/reconstruction/residual;48 cache batches | [raw cache](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/shared/rawcache) |
| Natural reference |R15 natural phenomena600 existing documents/76800 positions;300/150/150 | [source documents](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R15_20261102_natural_phenomena_output_geometry_v1/data/documents.jsonl) |
| Natural response identity |Sparse fixed-thresholdz; current frequency metadata and original cache hashes | [frequency](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/shared/frequency/frequency_table.csv) · [cache hashes](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/shared/frequency/cache_fingerprints.json) |
| Candidates and state bins |Discovery-only candidates,8 C/8 F; H3fixed16; H4ten patterns from80 | [C/F](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/shared/config/candidates_frozen.json) · [H4 freeze](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/H4/results/configurations_frozen.json) |
| Predictions and fits |All splits/arms; coefficient, scaler, tuningC, failures retained | [H1](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/H1/results) · [H2](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/H2/results) · [H3](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/H3/results) · [H4](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/H4/results) |
| Blind visible prefixes |Automatic conservative labels;208 matched pairs+91 unmatched hits+150 independent document prefixes | [texts](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/H4/results/blind_texts.jsonl) · [labels](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/H4/results/semantic_labels.jsonl) |
| Independent numerical verification |Loss and metric recomputation, H2serialized replay, group isolation, disjointmatching | [receipt](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/evidence/final_numeric_validation.json) |
| Selected evidence |12 figures plus compact tables; copies are exact current output | [payload manifest](payload_manifest.json) |
| Old exposed versions |Before notation repair; before disjoint context matching | [versions](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/versions) |

## Recompute / 复算

All analysis code lives at [shared/code](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/shared/code). `runtime_cpu.sh` selects the established local tokenizer/transformers runtime, CPU2 threads and no CUDA. `forward.py` writes384 responses in fixed8×64 physical batches. `frequency.py` reconstructs the existing sparse natural reference. `analyze.py` fits H1–H3 and freezes H4; `h4.py` completes H4; `validate_and_diagnose.py` independently recomputes predictions/metrics and frozen same-support diagnostics; `figures.py` renders identified tables. `deliver_reports.py` places curated records, not model weights.

Exact reruns should use an isolated execution-root copy and retain the original source SHA, configuration,384 JSONL rows and splits. `prepare.py` intentionally refuses an existing frozen panel; `amend_panel.py` is a historical one-time correction, not a parameter sweep. Do not execute these destructively in the delivered root. The saved coefficient/scaler files allow reading current predictions without retraining. Random mean-loss arms average individual model losses; their saved mean probability is not an equivalent single-model loss.

Raw arrays, large prediction histories, checkpoints and private task histories are omitted from the portable reading copy. This checkout has selected results; it does not make omitted payloads downloadable. Local sync is not Git publication. Full execution logs remain under [evidence](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/evidence), and source meetings/attachments retain their original identity.


Selected portable metadata: [panel manifest](data_manifest.json) · [numerical verification](numeric_validation.json). 原始大载荷仍在执行侧。
