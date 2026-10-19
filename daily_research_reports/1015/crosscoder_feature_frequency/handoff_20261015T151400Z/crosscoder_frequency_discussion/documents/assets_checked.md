# Feature frequency Protocol: current asset check

Date: 2026-10-15, Asia/Shanghai. Actor: Codex `/root/assets_inventory`.
[中文](assets_checked_cn.md).

**Recommended input: reuse the existing complete final 14-layer/F16384 sparse inference cache and its complete D/V joint-count matrices.** This recommendation identifies a practical input; it does not select a scientific conclusion or authorize analysis. Current local access and saved metadata were checked. No training, inference, feature statistics, plotting, checkpoint deserialization, or large checkpoint hashing was performed.

Current receipts: [strict access](../EXTERNAL_DEPENDENCIES.md#external-9a20216f413ae829), checked at 22:11:00 Asia/Shanghai, and [metadata/source check](../evidence/asset_metadata_20261015.json). The strict checker exited 0 for the seven selected assets. Access does not certify runtime loadability, payload hash integrity, independent documents, or scientific eligibility.

## 1. Objects and exact identities

The Base model has 28 blocks. The completed A22 CrossCoder observes only 14 predeclared blocks: zero-based `1,3,...,27`, or one-based `2,4,...,28`. Its dictionary has 16,384 features and hidden size 1,024. It uses block residual-post before the final global norm. The final and 0.5B states share this architecture; they are different learned dictionaries/states. Feature ID equality alone does not establish feature matching.

Execution root: `/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder`.

| Role | Exact registered asset ID | Current required address |
|---|---|---|
| Frozen Base | `model_qwen3_0p6b_base` | `/data/share/Qwen3-0.6B-Base` |
| Tokenizer | `tokenizer_qwen3_0p6b_base` | `/data/share/Qwen3-0.6B-Base` |
| Prepared TRAIN/VAL | `dclm_crosscoder_direct_bins_1b_a15_20261013` | execution root + `/data/direct_dclm_bins_a15` |
| A22 0.5B checkpoint | `crosscoder_qwen3_14layer_16384_bf16_a18_formal_14layer_batchtopk_a22_499998720_20261013` | execution root + `/runs/formal_14layer_batchtopk_a22/checkpoint_000499998720.pt` |
| A22 final checkpoint | `crosscoder_qwen3_14layer_16384_bf16_a18_formal_14layer_batchtopk_a22_999997440_20261013` | execution root + `/runs/formal_14layer_batchtopk_a22/checkpoint_000999997440.pt` |
| Complete final sparse cache | `representation_crosscoder_qwen3_final14_f16384_val10485760_phase1_20261013t173130z` | phase-one root + `/feature_cache` |
| Existing phase-one analysis | `analysis_crosscoder_feature_relation_phase1_20261013t173130z` | phase-one root |

Phase-one root is `/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/feature_relation_phase1/20261013T173130Z`.

The final checkpoint producer is `pt-2639gg8p`, with 999,997,440 paired position exposures. Its recorded SHA256 is `09b432e98dd7426f9ea4170809d75068a2ada2ed38c1e97d3fa18e119cd79628`; the prepared-data manifest SHA256 is `874794a8657f8982f7abb12ee517ec551fce840d9f20dfe103f48589a6779849`. These hashes were read from saved identity records, not recomputed over large payloads in this check. See the existing `input_identity.json`, `cache_binding.json`, and `feature_cache/manifest.json` under the phase-one root.

The cache root manifest has no embedded asset-ID field. Its catalog entry provides the stable ID; its checkpoint/data binding and four rank manifests provide the saved identity chain. All 640 chunk files currently exist, match their recorded byte sizes, and carry the same checkpoint/data/config binding. Fresh complete chunk hashes and array contents were **NOT_CHECKED**.

## 2. Saved inference and data contract

| Item | Saved contract or observation |
|---|---|
| Gated inference | Positive ReLU code retained only when its decoder-norm-weighted score is strictly greater than the saved TRAIN EMA cutoff |
| Cutoff | `0.051281172782182693`, frozen from complete saved TRAIN state |
| Other state | `k=256`; completed updates 244,140; TRAIN normalization calibration count 65,536 |
| Normalization | Frozen TRAIN mean-centered vector RMS, target norm 1 per observed layer |
| Precision | BF16 GEMMs/Base; FP32 CrossCoder state, scores and saved positive code values |
| Forward partition | Four original rank ranges; 16 whole 1,024-token contexts per Base forward; 1,024 eligible positions per CrossCoder batch; SDPA |
| Eligible positions | `N=10,485,760`; special IDs 151643–151656 excluded; each row is one eligible position, not 14 independent layer samples |
| Cache size | 2,669,034,642 saved nonzeros; mean gated L0 `254.538978767395`; 290 zero-hit features in this window, per existing manifest |
| Existing D/V split | 81 source-ordered blocks of at most 128 whole contexts; seed 20261014; tail retained; eligible-count balancing |
| Existing counts | `N_D=5,238,097`; `N_V=5,247,663`; 10,249 contexts total |
| Source | One VAL bin, `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_0_of_10_shard_00000001_processed.bin` |

The recorded source-bin SHA256 is `664d07bcb4db743ac9ec62a9c6e4df245f3fd4fde35b8536dece439fcaac9697`. Row identity is the global eligible-position index joined through fixed `index_val/records.npy`, `index_val/prefix.npy`, the source-bin identity, and excluded IDs. These are token/context identities. **Original document boundaries, URL identity, and original-document/near-duplicate independence remain `Unknown`.** The original prepared-data manifest says `activation_cache=NONE`; that describes preparation before phase one. It does not contradict the subsequently saved phase-one cache.

Both D and V have already been inspected in previous analyses. They can support a new, transparently exposed within-bin exploratory analysis. They cannot become untouched confirmation data by renaming or reshuffling. A document-independent confirmation branch requires an identity-preserving document mapping and separately qualified data/split; the current cache does not establish those prerequisites.

Existing `original_validation_replay_check.json` reports equality of all 16,384 marginal hit counts to the original final validation, with zero count differences. Rank receipts report exact original-forward agreement and unchanged buffers. These are saved engineering receipts, not fresh replay in this task.

## 3. What can be reused without inference

All paths below are relative to the phase-one root stated above. File headers and saved producer code were inspected without loading the large count arrays.

| Saved object | Shape / dtype / size | Permitted reuse and limit |
|---|---|---|
| `counts/total0.npy` | `(16384,16384)`, int64; 2,147,483,776 bytes | Exact full-F D joint-hit matrix; arbitrary pair lookup, including pairs absent from the old graph |
| `counts/total1.npy` | Same | Exact full-F V joint-hit matrix |
| `feature_frequency.npz:n` | `(2,16384)`, int64 | D/V marginal hits; saved side order 0=D, 1=V |
| `feature_frequency.npz:zsum` | `(2,16384)`, float64 | Saved marginal gated-amplitude sums |
| `feature_frequency.npz:block_n` | `(81,16384)`, int64 | Arbitrary feature marginal hits per existing block |
| `feature_frequency.npz:block_zsum` | Same, float64 | Marginal gated-amplitude sums per existing block |
| `block_edges/block_000.npy` through `block_080.npy` | Each `(214711,)`, uint32 | Joint counts only for the 214,711 old discovery edges, aligned to `graphs/raw_edges.npz`; not all new pairs |
| `feature_cache/rank0..3/*.npz` | 640 CSR chunks; 16,098,567,532 file bytes total | Per-position gated activations for future selected-pair block recomputation or matching context display, after approval |
| `decoder_geometry.npz` | Saved decoder norms, TRAIN RMS and mean | Existing geometry description; geometry does not determine frequency or establish semantic/causal dependence |

CSR keys are `ptr` (uint64 row offsets), `ids` (sorted uint16 feature IDs), and `z` (positive FP32 gated activations). Each ordinary chunk has 16,384 rows. The first chunk header has `ptr:(16385,)`, `ids:(4126432,)`, and `z:(4126432,)`; this is a format example, not an assumed constant nnz per chunk. The raw element-size formula is `8*(N+640)+6*nnz`; actual file bytes also include NPY/ZIP metadata.

The complete count matrices are suitable for memory-mapped row/pair access. Rebuilding all pair counts is unnecessary when the indicator, window, side labels, and input identities remain unchanged. The full unordered pair universe has `F*(F-1)/2=134,209,536` pairs; the old candidate-list Jaccard search used a different 120,380,886-pair eligible pool. Neither the old graph nor its selected pair pool should silently define the new Anchor's all-feature population.

Arbitrary new-pair block intervals cannot be recovered from `block_n` alone. The old per-block edge arrays cover only the old discovery edges. For any newly selected pair outside that set, future block joint counts require reading the existing sparse cache, or the Protocol must label this readout `NOT_RUN`. Existing token-level summaries do not supply independent-document uncertainty.

## 4. Existing graphs, figures, source code and provenance

The phase-one graph is a thresholded, directed statistical construction. Its `code_snapshot_v2/core.py:rule` requires both marginal supports ≥200, joint support ≥20, `P(u|A)≥0.8`, `P(A|u)≤0.5`, and `n_u≥2*n_A`. Transitive reduction then produces the graph used for candidate-list overlap. This construction embeds frequency direction and threshold choices. It is not a neutral measurement of every possible pair.

`figure_provenance.json` points to the reduced V graph, complete count matrices, saved frequencies, decoder contribution table and four chosen pairs. `code_snapshot_manifest_v2.json` pins the eight producing files in `code_snapshot_v2/`. Their current small-file hashes all match that manifest. The code is a source reference; executing `features.py` would load models/checkpoints and can generate/count features, so it is **not** an authorized action in this drafting task.

Expanded-figure execution root:
`/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/hierarchy_decoder_distribution/20261014T020014Z/expanded_graph_20261014T032050Z`.

Its `receipt.json` and `selection_rules_frozen.json` identify reuse of the saved reduced V graph, raw-edge support table, frequencies and saved geometry. The expanded view shows 320 selected nodes and all 1,250 saved direct edges induced by them; the complete qualified population has 15,537 nodes, with h0–h5 counts `20,8896,5347,1209,63,2`. Display counts are `20,80,80,75,63,2`. The figure retains full-graph h and uses fixed quotas and D-frequency rank strata. It is a selected display, not the full frequency distribution or a new model mechanism.

The producing display source is `code/draw_expanded_graph.py`, with subsequent layout/title revision scripts and receipts retained alongside it. The repository copy and reading guide are under [the existing expanded package](../EXTERNAL_DEPENDENCIES.md#external-ef7441eeae6b3414). Its identity records describe visualization-only reuse, not a fresh feature cache or independent confirmation dataset. No existing figures were regenerated or reinterpreted here.

## 5. 0.5B and the distinct full-28-layer run

The A22 14-layer 0.5B and final checkpoints are both currently accessible in the strict check. The inspected complete sparse cache is **final only**. A complete corresponding 0.5B sparse cache or feature-matching certificate was not found in the inspected phase-one/analysis navigation. Therefore 0.5B/final stability is not presently qualified by cache reuse or by equal feature IDs; it remains a separate proposed branch with explicit matching and input preparation.

The full-28-layer/F32768 A23 run is a distinct fresh run. It is not the A22 cache producer. Current local metadata proves this run has advanced in a retry, so `NOT_RUN` would be false. At the bounded local inspection, `recovery_20261015/a23/run_retry_01/current_progress.json` recorded step 8,700 and 35,635,200 position exposures. `latest_checkpoint.json` recorded an actual mutable save at 24,997,888 exposures, path ending `/latest.pt`, and `asset_id:null`.

The original A23 run directory and its named retry directory contained no 0.5B or final checkpoint at inspection. The inspected catalog likewise contained no A23 0.5B/final registered asset. This is a bounded absence-of-target-evidence statement, not a claim about all storage or the job's current platform state. No platform query, new connection, monitoring, registration or run operation was performed. A23 inputs must be checked afresh if the researcher later chooses them.

## 6. Historical resources and planning limits

Saved phase-one producer `pt-zwh6g95p` followed engineering repair of `pt-io5c5h2p`, on four H100 80GB GPUs. The successful terminal receipt records 629.63 active seconds; its resource receipt records peak aggregate RSS 12,248,944,640 bytes and peak added disk 46,226,108,170 bytes. Sparse-generation telemetry reports maximum sampled allocated GPU memory 5,181,352,448 bytes. This is a generation-stage observation, **not a verified full-job GPU peak**.

| Successful stage | Saved seconds |
|---|---:|
| Sparse feature encoding | 127.26 |
| Exact full-F counting | 87.51 |
| Merge | 121.54 |
| Raw edges / reduction | 2.39 / 2.64 |
| Pair selection | 39.66 |
| Sensitivity | 2.92 |
| Selected-edge block counts / summary | 29.18 / 12.63 |
| Inspection / delivery | 134.13 / 25.91 |

These stage values come from saved `events_75.jsonl` and do not account identically to the terminal active-compute counter; do not sum them into a new billed duration. The expanded display separately records 63.91 CPU wall seconds, peak RSS 1,217,056,768 bytes, zero GPU jobs and zero sparse-cache scans.

No new benchmark was run. Historical timing does not qualify a new null model, resampling strategy, or full population scan on another runtime. For the proposed cache-reuse path, pair totals can avoid model inference and GPU counting. New arbitrary-pair block counts may still read roughly 16.1GB of saved cache; exact elapsed time remains `Unknown` until the approved implementation and execution environment are fixed.

## 7. Gaps to retain in the Protocol

1. Document-independent confirmation: blocked on original-document/duplicate-group identity and separately qualified split; old D/V is exposed within-bin exploration.
2. 0.5B/final stability: matching certificate and matching inference cache are not established by this check; no comparison was run.
3. Arbitrary new-pair block joint counts: available only after selected sparse-cache reads, unless the pair occurs in the old 214,711-edge table.
4. Asset access is current; full cache rehash, full array verification, checkpoint loadability and measurement-quality approval remain `NOT_CHECKED` or `Unknown` as applicable.
5. No new analysis, training, launch, commit, push, publication, graph edit or scientific state transition is authorized by this inventory.
