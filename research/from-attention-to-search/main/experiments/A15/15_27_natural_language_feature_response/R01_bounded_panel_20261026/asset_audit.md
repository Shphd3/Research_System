# R01 existing-asset audit

The selected carrier is the original 28-layer Qwen3-0.6B official pretrained model and its existing E16 layer27 MLP-input SAE. All four required registered assets passed current strict access checks at 2026-10-26 10:40:13 UTC (18:40:13 Asia/Shanghai), effective UID 0. This audit selects one matching interface; it performs no model comparison.

| Asset | Existing object |
| --- | --- |
| `model_qwen3_0p6b_base_official_a5` | `/data/250010109/model_cache/Qwen3-0.6B-Base-official/model.safetensors` |
| `tokenizer_qwen3_0p6b_base_official_a5` | tokenizer files in the same official directory |
| `sae_qwen3_0p6b_e16_layer27_final_1b` | E16 run `full-20260903T150734Z/sae_full_final.pt` |
| `representation_qwen3_0p6b_e17_dclm_sparse_activation` | E17 DCLM TRAIN discovery arrays, 261,632 retained token positions |

## Exact measurement interface

The model has 28 blocks, hidden width 1,024 and intermediate MLP width 3,072. The hook is `model.model.layers[27].mlp.register_forward_pre_hook`, reading `args[0]`: actual MLP input after that block's post-attention normalization. It is neither the attention projection output nor an unnormalized residual. The single-layer SAE reads that 1,024-dimensional vector and returns 30,000 coordinates with ReLU and Top32. Its native `TopKSAE.from_pretrained` loader restores `format/config/state_dict/metadata`; the four FP32 state tensors are encoder weight `[30000,1024]`, encoder bias `[30000]`, decoder weight `[1024,30000]` and decoder bias `[1024]`.

No input unit normalization or decoder-bias subtraction precedes the encoder. Reconstruction is the sum of each activation times its decoder column, plus decoder bias. Contribution magnitude is activation times the actual saved decoder-column L2 norm, in native hook units. Keep absolute activation, raw contribution and any normalized quantity separately. Decoder magnitudes can cancel as vectors and are not causal or variance allocations.

The dictionary was trained on `dclm_pair_v1`, with the pretrained parent frozen and per-batch norm outliers above the 0.999 quantile removed. The new designed targets are not silently removed by that historical filter. The local model README describes 119 pretraining languages; English construction follows the dictionary's DCLM source rather than imposing Chinese text. The [machine audit](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/asset_audit.json) binds actual loaders and source paths.

## Identity and historical reconstruction

Freshly recomputed SHA256 values match the recorded identities:

| Object | SHA256 |
| --- | --- |
| Model weights | `cd2a512003e2f9f3cd3c32a9c3573f820bb28c940f73c57b1ddaa983d9223eba` |
| E16 dictionary | `e4e2049aced8ba9a3b043bbb2b3308b497b7ec22f107531e37197873ee545b65` |
| Model config | `504a6b58c4271583724e66584b6b7698aea18450209df6b2f7582df0e89cee59` |
| Tokenizer JSON | `c0382117ea329cdf097041132f6d735924b697924d6f6fc3945713e96ce87539` |

All tokenizer component and reference-array hashes remain in the machine audit. The original E16 [full summary](/data/250010109/MoE_Router/experiments/20260903_a15_13_e16_dclm_final_layer_sae/runs/full-20260903T150734Z/full_summary.json) reports validation normalized reconstruction MSE 0.0533820926, mean L0 32, and exact checkpoint reload difference 0.0. These historical measurements justify attempting R01 qualification; they do not qualify R01 text automatically.

## Independent reference frequency and its limit

Read only E17 `discovery_indices.npy` and `discovery_values.npy`. They contain 261,632×32 entries, all finite positive values. For each feature, frequency is positive-value hit count divided by 261,632. Mean activation is the corresponding activation sum divided by that denominator. This is a historical reference-corpus occurrence rate after its recorded norm filter. The current panel's hit rate is a separate statistic.

The source records the expected official parent path/config and exact SAE hash, but not the historical cache-producing backbone's weight digest. Freshly hashing today's parent does not repair this missing historical binding. Frequency-matched comparisons retain a conditional provenance limit. The E17 producer encoded with BF16 autocast; R01 uses the native FP32 encoder, so TopK near ties may differ and matching additionally depends on precision comparability. Historical NMSE never replaces local qualification. No new language-model forwards or reconstruction of that reference are authorized to conceal the gap. Existing E17 graph tables are selected-node outputs, not complete frequency statistics; deriving marginal counts from its saved discovery arrays is permitted offline work. E17 replication arrays and sealed TEST remain unread.

## Runtime reuse and pending qualification

Reuse existing `/root/anaconda3/envs/spectral-hier/bin/python` with `PYTHONPATH=/data/250010109/dependency_packages/hf_transformers_qwen3`. Imports verify Torch 2.5.1+cu121, Transformers 4.53.3, tokenizers 0.21.2 and safetensors 0.5.3. No package installation is required. The model uses native BF16 eval/no-grad SDPA; the SAE uses its saved FP32 tensors and native Top32 rule. Available existing execution surface is this container's H100 40 GB MIG, subject to actual runtime checks.

At the audit boundary there were zero model forwards, zero GPU model loads, one CPU-only dictionary payload inspection, and no training or TEST read. New-panel reconstruction, decoder-formula agreement and replay remain exact prespecified prerequisites in the [Protocol](protocol.md). Failure stops dependent hypotheses and does not trigger dictionary training or asset substitution.
