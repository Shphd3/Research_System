派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/dataset_guide.md`。
[精确原始文件](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/dataset_guide.md)；研究修改仍回到原件。

---

# Dataset identity and reproducibility / 数据与可复算入口

The editable research owner is R17 in from-attention-to-search. Payloads remain at `/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02`. 本页只索引本轮确实读取／生成的对象，不代表新独立确认。问题与结论见[Summary](../../../../../../../../UNAVAILABLE.md)。

| Object / 对象 | Identity and actual scope | Saved source |
|---|---|---|
| Constructed panel / 构造面板 |384 rows;48 families;24/12/12 grouped split; SHA256 `dc2c3a58d056bdb20ffecbcbda57fa0b9afca1254e673b41e6271bf2263c5ace`;19 notation-corrected rows; exposed heldout | [full text, labels, token IDs](../../../../../../../../UNAVAILABLE.md) |
| Panel metadata |12 theorem groups split6/3/3;96 nonmatrix controls; coarse Unknown | [manifest](../../../../../../../../UNAVAILABLE.md) |
| Frozen model/dictionary/code |Qwen3-0.6B-Base official; A22 checkpoint000999997440;14 odd layers;16384 atoms | [hashes](../../../../../../../../UNAVAILABLE.md) |
| Responses |384 target positions; rawz/h/decoder/reconstruction/residual;48 cache batches | [raw cache](../../../../../../../../UNAVAILABLE.md) |
| Natural reference |R15 natural phenomena600 existing documents/76800 positions;300/150/150 | [source documents](../../../../../../../../UNAVAILABLE.md) |
| Natural response identity |Sparse fixed-thresholdz; current frequency metadata and original cache hashes | [frequency](../../../../../../../../UNAVAILABLE.md) · [cache hashes](../../../../../../../../UNAVAILABLE.md) |
| Candidates and state bins |Discovery-only candidates,8 C/8 F; H3fixed16; H4ten patterns from80 | [C/F](../../../../../../../../UNAVAILABLE.md) · [H4 freeze](../../../../../../../../UNAVAILABLE.md) |
| Predictions and fits |All splits/arms; coefficient, scaler, tuningC, failures retained | [H1](../../../../../../../../UNAVAILABLE.md) · [H2](../../../../../../../../UNAVAILABLE.md) · [H3](../../../../../../../../UNAVAILABLE.md) · [H4](../../../../../../../../UNAVAILABLE.md) |
| Blind visible prefixes |Automatic conservative labels;208 matched pairs+91 unmatched hits+150 independent document prefixes | [texts](../../../../../../../../UNAVAILABLE.md) · [labels](../../../../../../../../UNAVAILABLE.md) |
| Independent numerical verification |Loss and metric recomputation, H2serialized replay, group isolation, disjointmatching | [receipt](../../../../../../../../UNAVAILABLE.md) |
| Selected evidence |12 figures plus compact tables; copies are exact current output | [payload manifest](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/payload_manifest.json) |
| Old exposed versions |Before notation repair; before disjoint context matching | [versions](../../../../../../../../UNAVAILABLE.md) |

## Recompute / 复算

All analysis code lives at [shared/code](../../../../../../../../UNAVAILABLE.md). `runtime_cpu.sh` selects the established local tokenizer/transformers runtime, CPU2 threads and no CUDA. `forward.py` writes384 responses in fixed8×64 physical batches. `frequency.py` reconstructs the existing sparse natural reference. `analyze.py` fits H1–H3 and freezes H4; `h4.py` completes H4; `validate_and_diagnose.py` independently recomputes predictions/metrics and frozen same-support diagnostics; `figures.py` renders identified tables. `deliver_reports.py` places curated records, not model weights.

Exact reruns should use an isolated execution-root copy and retain the original source SHA, configuration,384 JSONL rows and splits. `prepare.py` intentionally refuses an existing frozen panel; `amend_panel.py` is a historical one-time correction, not a parameter sweep. Do not execute these destructively in the delivered root. The saved coefficient/scaler files allow reading current predictions without retraining. Random mean-loss arms average individual model losses; their saved mean probability is not an equivalent single-model loss.

Raw arrays, large prediction histories, checkpoints and private task histories are omitted from the portable reading copy. This checkout has selected results; it does not make omitted payloads downloadable. Local sync is not Git publication. Full execution logs remain under [evidence](../../../../../../../../UNAVAILABLE.md), and source meetings/attachments retain their original identity.


Selected portable metadata: [panel manifest](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/data_manifest.json) · [numerical verification](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/numeric_validation.json). 原始大载荷仍在执行侧。
