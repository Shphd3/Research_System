# Reuse audit sources: sentence-local feature persistence and relation

Processing agent: `/root/graph_cache`. Date: 2026-10-28 UTC. Scope: read-only feasibility and source audit; H1/H2 statistics NOT RUN; new model forwards/training/graph construction: 0.

## Current access and physical objects

Strict read access of the following eight IDs passed at 2026-10-28T05:30:33Z, UID 0. Receipt: [current receipt](input_access_20261028.json). This does not newly certify multi-GB model hashes, numerical equality, scientific independence or hypothesis support.

| Registered ID | Actual primary location |
| --- | --- |
| `model_qwen3_0p6b_base` | `/data/share/Qwen3-0.6B-Base` |
| `model_qwen3_0p6b_base_official_a5` | `/data/250010109/model_cache/Qwen3-0.6B-Base-official` |
| `tokenizer_qwen3_0p6b_base_official_a5` | `/data/250010109/model_cache/Qwen3-0.6B-Base-official` |
| `sae_qwen3_0p6b_e16_layer27_final_1b` | `/data/250010109/MoE_Router/experiments/20260903_a15_13_e16_dclm_final_layer_sae/runs/full-20260903T150734Z/sae_full_final.pt` |
| `crosscoder_qwen3_14layer_16384_bf16_a18_formal_14layer_batchtopk_a22_999997440_20261013` | `/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/runs/formal_14layer_batchtopk_a22/checkpoint_000999997440.pt` |
| `data_a15_27_r04_domain_native_dual_20261027` | `/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R04_domain_usage_20261027/data` |
| `analysis_a15_27_r04_native_sae_joint_cc_domain_20261027` | `/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R04_domain_usage_20261027` |
| `analysis_crosscoder_feature_relation_phase1_20261013t173130z` | `/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/feature_relation_phase1/20261013T173130Z` |

## Native interface and recorded identity

R04 producer: `/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R04_domain_usage_20261027/run_dual_forward.py`. Lines 19-21 assert model, A22 and E16 weight SHA256, respectively. Lines 28-35 bind the Base, SAE and CrossCoder loaders and saved TRAIN normalization; lines 47-49 capture SAE block27 MLP input and CC blocks1,3,...27 residual-post; lines 58-60 apply native SAE and CC encoders. Lines 73-79 serialize only z>0 into native per-token CSR.

| Object | Producer-asserted SHA256 |
| --- | --- |
| Qwen3 Base model.safetensors | `cd2a512003e2f9f3cd3c32a9c3573f820bb28c940f73c57b1ddaa983d9223eba` |
| Final A22 CrossCoder | `09b432e98dd7426f9ea4170809d75068a2ada2ed38c1e97d3fa18e119cd79628` |
| E16 SAE | `e4e2049aced8ba9a3b043bbb2b3308b497b7ec22f107531e37197873ee545b65` |

Old graph identity owner: `/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/feature_relation_phase1/20261013T173130Z/input_identity.json`; its exact paths/recorded hashes bind the same Base and A22. R04 `/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R04_domain_usage_20261027/forward/completed.json` records both branches qualified and 456 total original calls. These are producer provenance, not newly executed model loading. The current audit freshly read and validated every one of the 120 sparse files against its token IDs, bounds, finite positive values, and strictly sorted unique per-row IDs.

SAE is FP32 native ReLU Top32 at zero-based block27 MLP input, F30000. CC is native shared z from 14 odd-indexed residual-post hooks, F16384, BF16 GEMMs, saved TRAIN centering/vector RMS and score gate 0.051281172782182693. Shared z is not fourteen independently measured layer activations. Decoder-scaled contributions remain separate from z.

## Texts, split exposure and cache fields

Data: `/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R04_domain_usage_20261027/data/documents.jsonl`; 60 math and 60 biology documents, one 192-token excerpt each. Each domain has 30 discovery, 10 development and 20 heldout documents; all these splits already appeared in R04 analyses and R05 reuses. They are not new untouched confirmation data. There are 120 canonical document groups. Stored fields include original URL, WARC ID, source text hash, source line, source character boundaries, full prefix, token IDs, domain and split.

Per-token cache: `/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R04_domain_usage_20261027/forward/documents/<seq_id>.npz`: `token_ids`, `SAE_ptr`, `SAE_ids`, `SAE_z`, `CC_ptr`, `CC_ids`, `CC_z`, and reconstruction errors. The 120 files contain 23,040 positions. SAE L0 is always 32; CC L0 ranges 29–637 (mean 295.4366). Aggregate `documents_SAE.npz`/`documents_CC.npz` count only token positions 32:192, and cannot substitute for per-token arrays.

Sentence boundaries are not stored. A deterministic boundary rule and text-only audit are required before pair results are opened. Abbreviations, formula punctuation, headings and 192-token truncation must not be silently called complete sentences.

## Independent DCLM frequency bins

Existing function: `/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R05_distance_attention_20261028/analyze_A.py:60`, `groups(k)`, lines61-62. Equivalent bin export: `/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R05_distance_attention_20261028/analyze_B.py:55` through58. Inputs: `/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R04_domain_usage_20261027/forward/reference_SAE.npz` and `reference_CC.npz`; each has per-window `counts`, `n_positions`, `seq_id`, sums and decoder norms. Define hits by summing counts over windows; frequency=hits/65536. Eligible hits>=20, then cuts=np.quantile(freq[eligible],[1/3,2/3]); bins use strict `freq>cut`, so ties remain together. Less than20 hits is a separate low-support group, not the low-frequency group.

| Dictionary | Lower cut | Upper cut | Low / middle / high / low-support features |
| --- | --- | --- | --- |
| SAE | 0.0005950927734375 | 0.0012359619140625 | 5121 / 4800 / 4947 / 15132 |
| CC | 0.002593994140625 | 0.0134429931640625 | 4469 / 4437 / 4451 / 3027 |

Reference has256 windows and65,536 token positions. Existing grouping implementation: `/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R04_domain_usage_20261027/analyze_frozen.py:62` through68, `(urlsplit(url).hostname,urlsplit(url).path.rstrip("/"))`; this yields254 groups. Current text-only checks find zero research/reference intersections for canonical URL, WARC ID and source-text hash. This is observed source separation, not proof against all unknown near-duplicates.

## Exact old CC graph, direction and one-hop meaning

Graph: `/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/feature_relation_phase1/20261013T173130Z/graphs/raw_edges.npz`. Exact keys: `A`, `u`, `cD`, `cV`, `passV` (case-sensitive; not `pass_v`). Edge source is `A`, destination is `u`. Validation-passed raw graph selects `A[passV] -> u[passV]`;206,136 edges from214,711 discovery candidates.

Discovery rule: `/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/feature_relation_phase1/20261013T173130Z/code_snapshot_v2/core.py:66` through67. Review repeats the same rule at `graphs.py:51`; fields serialized at `graphs.py:54`; direction and probability diagnostics at `graphs.py:59` through60.

At one and the same token: nA,nB>=200, nAB>=20, P(B|A)>=0.8, P(A|B)<=0.5, nB>=2*nA. The graph is not a cross-token conditional-probability model. Reusing its edges across tokens creates the new H2 observable. DeltaP=P(B|A)-P(B) and lift=P(B|A)/P(B) are saved diagnostics, not edge acceptance conditions.

Fresh edge check: self-loops0, bidirectional edges0, frequency-doubling rule true on every reviewed edge. Positive frequency strictly increases along any arrow, so cycles are impossible by design. Maximum outgoing degree91; maximum incoming degree15,439. Degree control is necessary. No independent semantic hierarchy has been defined.

Raw versus reduced: `/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/feature_relation_phase1/20261013T173130Z/code_snapshot_v2/graphs.py:12` through39 implements exact transitive reduction; lines63-76 apply it separately to D and V. `graphs/reduced_V.json` has146,947 edges and keeps reachability, but removes raw direct edges that can be reached via longer paths. Therefore raw-one-hop and reduced-one-hop coverage are different estimands. Fix one before results; a suggested primary choice is the original V-passed raw edges because each retained arrow directly passed the registered probability conditions. This is an AI design suggestion, not a new user decision. Existing maximum depth5 means longest outgoing path to a sink and is not semantic height.

## Why historical SAE graph is not currently compatible

Historical E17 producer `/data/250010109/MoE_Router/experiments/20260904_a15_13_e17_sae_hierarchy/run_hierarchy.py:99` through107 explicitly captures raw hook, filters norm outliers, uses BF16 autocast, saves `topk_indices` and FP16 `topk_values`. `/data/250010109/MoE_Router/experiments/20260904_a15_13_e17_sae_hierarchy/hierarchy_core.py:33` through40 counts valid feature indices without testing the corresponding activation value. `build_postings`, lines44 onward, likewise uses indices. R04 uses FP32 native SAE and stores only `z>0` (`run_dual_forward.py:76`). Even equal dictionary IDs do not certify this observation-interface equivalence. Historical parent/source binding was also reported incomplete in the owning R03 original-graph audit.

Status: `INCOMPATIBLE_INTERFACE_UNQUALIFIED`. Preserve E17 as history; SAE H1 can use R04 native cache, while SAE H2 remains blocked. Do not relabel the old graph compatible or rebuild another graph under its name.

## Fresh hashes of bounded source artifacts

The following are freshly calculated in this audit. Weight hashes above are recorded producer assertions, not rehashed here.

| Source | SHA256 |
| --- | --- |
| `/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R04_domain_usage_20261027/run_dual_forward.py` | `4c7a84cd3e5b1a2b4cd161297d1e30cd5e987ad699d43ea8c4b6672d3455e1dd` |
| `/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R04_domain_usage_20261027/forward/completed.json` | `7301fef7557976a2ce3f22fe1618eee5c14695b4a3828b7cfa69c86af434a461` |
| `/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R04_domain_usage_20261027/data/documents.jsonl` | `32e1e8a2e661808bf34a0b3df6636dd30aea784375adebe225c47a392db4a943` |
| `/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R04_domain_usage_20261027/data/reference.jsonl` | `11c3d538a588983e9565ab003ed78a7369498e9e0838b6f090bbad4e337d95f3` |
| `/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R04_domain_usage_20261027/data/source_manifest.json` | `06bfa7533da913339a70a298dd677e7725e4a9f7692c5ff35c5e36547ae8f960` |
| `/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R04_domain_usage_20261027/forward/reference_SAE.npz` | `fd40470a61a20b211c9c6ce001746ba00ac831224ed95c46d7521bbe8db175f9` |
| `/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R04_domain_usage_20261027/forward/reference_CC.npz` | `f241f53e5b5f41048ca8cc3861fa6d829d2cf42794fb5ebf5b58fd704787868e` |
| `/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R05_distance_attention_20261028/analyze_A.py` | `45f1a230ec5dd81d149d548e666524ba3aaf54b3174a5a96ea394c52b32b266d` |
| `/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/feature_relation_phase1/20261013T173130Z/input_identity.json` | `cb5d65d45fcb345af207e767afbd429dcc45f71768e47a8139e280081cdd1113` |
| `/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/feature_relation_phase1/20261013T173130Z/graphs/raw_edges.npz` | `e017e5d43235f4ed74691e2afc4ca003387e1ac96dee76de1f635ecade5806e1` |
| `/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/feature_relation_phase1/20261013T173130Z/code_snapshot_v2/core.py` | `cca787eed861413a1f07573854a9b5f0a6e5a2fb7daa0c4dd6a98c24306b0a3f` |
| `/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/feature_relation_phase1/20261013T173130Z/code_snapshot_v2/graphs.py` | `c9aaa1c80e787c8c3cbd153554a85547fe887ee6773cb13778def363e5a48e26` |
| `/data/250010109/MoE_Router/experiments/20260904_a15_13_e17_sae_hierarchy/run_hierarchy.py` | `da510c564c83d75f6409698304b617aa1e612d2804ba79188ba941a5887cb760` |
| `/data/250010109/MoE_Router/experiments/20260904_a15_13_e17_sae_hierarchy/hierarchy_core.py` | `c1efab33c86d2fad263789c6e29c1288cf299f51200131c542fec388bdad9785` |

## 中文结论

两套原生活跃缓存齐全；当前工作可进入切句和统计合同设计。CrossCoder 旧图可绑定原生接口，箭头只表明同 token 的非对称共现规则；旧图偏向高频目标，最大入度15,439，不能称语义上下级。SAE 旧图接口尚未合格，H2 单独受阻。H1/H2 的新成对统计、显著性和示例结果均 NOT RUN。
