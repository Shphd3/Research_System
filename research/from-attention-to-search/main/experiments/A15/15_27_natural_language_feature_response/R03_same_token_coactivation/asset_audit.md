# R03 assets: original same-token graph and matched CrossCoder

The exact original graph is available and matches the requested observation: binary activity of one shared CrossCoder z at the same token. Reuse it under identity **O**. New raw/corrected graphs and communities have separate identities R/C; neither is the E16 response-difference grouping G02/G04. This audit changes no old asset and performs no model forward.

## Matched primary assets

| Registered ID | Actual object / binding |
| --- | --- |
| `model_qwen3_0p6b_base` | `/data/share/Qwen3-0.6B-Base`; frozen pretrained Qwen3, 28 blocks, width 1024 |
| `tokenizer_qwen3_0p6b_base` | Parent-matched local tokenizer and recorded hashes |
| `crosscoder_qwen3_14layer_16384_bf16_a18_formal_14layer_batchtopk_a22_999997440_20261013` | Final A22 checkpoint, F16384, 999997440 positions, 244140 updates; no optimizer is loaded for this analysis |
| `dclm_crosscoder_direct_bins_1b_a15_20261013` | Original direct-bin source/index; VAL here is exposed review material, not sealed TEST |
| `representation_crosscoder_qwen3_final14_f16384_val10485760_phase1_20261013t173130z` | Complete same-token sparse-z cache, 10485760 rows, 640 CSR chunks |
| `analysis_crosscoder_feature_relation_phase1_20261013t173130z` | Original full counts, graph, geometry, splits and source/code identities |
| `data_same_token_coactivation_panel_r03_20261027` | New fixed 12-case/72-text panel, with six whole cases/36 inputs selected within the remaining budget; text SHA256 `57c1d0358b5128a116128f73514d6d855454bdb689e706c941ed76f6a27e01b9` |

Current strict access passed for the six reused primary IDs in [main input access](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R03_same_token_coactivation/audit/main_input_access.json). The newly registered panel also passed a current strict check by this document author. Separately, the original-graph audit checked seven IDs including the historical E17 cache, 17 small-source hashes and every cache chunk's recorded presence/size. It did not rehash all 16 GB. Selected chunks are fully hashed when read. Strict access is not tensor loadability, numerical qualification, independent-document evidence or scientific acceptance.

Model SHA256: `cd2a512003e2f9f3cd3c32a9c3573f820bb28c940f73c57b1ddaa983d9223eba`.

Dictionary SHA256: `09b432e98dd7426f9ea4170809d75068a2ada2ed38c1e97d3fa18e119cd79628`.

Those weight hashes were streamed in the preceding same-session R02 audit and are rechecked by the current runner before new inference. The final freeze receipt records current source hashes. Detailed original provenance is [original graph audit](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R03_same_token_coactivation/audit/original_graph_audit.md) and its structured JSON companion.

## Measurement interface and scale

At one token, take residual-post tensors from zero-based blocks 1,3,…,27 before final global norm. Normalize each with the saved TRAIN mean and vector RMS, yielding `[positions,14,1024]`. The encoder sums layer projections and shared bias, then applies ReLU. Base execution is BF16 SDPA; coder GEMMs are BF16 with FP32 state/scores. The saved strict TRAIN score gate is 0.051281172782182693, using z-preactivation times the sum of layer decoder norms; it is not per-token Top256. No normalization or threshold is refitted.

There is one shared z. Layer native contribution magnitude is z times TRAIN RMS times that layer's decoder norm. Center/decoder bias remain separate. The joined native contribution norm, raw activation and hook-normalized amount are distinct saved quantities. Layer decoder contributions do not become independent layer activations, semantic levels or evidence of information emerging from shallow to deep layers.

Reuse/adaptation: reuse exact checkpoint, normalizer, threshold, decoder and original cache/graph; adapt the existing native loader/extraction interface to bounded short inputs and a ledger; write only offline counting, randomization, graph grouping, controls and reporting code. No model, dictionary, expert or router is trained. E16 and CrossCoder feature numbers are not matched.

## Original graph retained

O has all 16384 nodes. Its D raw graph has 214711 edges; V rechecks those D edges and retains 206136. A→B requires nA,nB≥200, nAB≥20, P(B|A)≥0.8, P(A|B)≤0.5 and nB≥2nA. DeltaP/lift were saved as diagnostics, not original acceptance gates. Frequency doubles along every arrow, so the DAG is imposed by the rule. The reduced graph's longest outgoing path has maximum depth five; this is not semantic height. The old “composition list” is outgoing neighbors after reduction, not a graph-community algorithm or verified parent/child relation.

Complete D/V count matrices `(16384,16384)` int64, feature/block counts and old-edge block counts exist. The fixed 512-node R/C study uses exact cached rows. O's full graph and high-frequency nodes remain intact even if the random subgraph omits a global hub.

## Source-unit and precision limits

CSR fields are uint64 ptr, sorted uint16 IDs and positive FP32 z. Source indices recover exact token IDs, absolute offsets and context-relative positions. They do not recover original document IDs. The 10249 length-1024 contexts were split into within-bin D/V review blocks; near-duplicate/document independence is Unknown. First-eight token texts roundtrip exactly, but im_end separators are only a source-segment proxy, and punctuation rules can split abbreviations. No verified sentence/document resampling unit is available. Context intervals therefore stay descriptive; text-type labels are also missing.

Historical E17 is separate: E16 single-layer F30000 at layer27 MLP input, BF16 encoding and FP16 exported values after outlier filtering. Its native indices/parent/source mapping cannot be silently mixed with R02 FP32 or CrossCoder. Preserve its graph only as historical context.

## New-panel qualification remains pending

Old cached Base batches were 16×1024 and coder batches 1024 positions. The new controlled runner uses Base batch1, right padding to256 and coder batches1024. Shape changes require two original-cache replays, two identical replays, eight visible-prefix checks and reconstruction gates fixed by the [Protocol](protocol.md). The old cache and R02's different E16 failure establish neither success nor failure for this current interface. No new inference is asserted by this asset audit. Missing or failed dependent qualification is reported, not repaired by training or extra resources.
