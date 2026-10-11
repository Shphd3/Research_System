# Original Qwen3-0.6B SAE and related assets

This is a reading guide to **26 newly registered entries**: 25 accessible
entries and one missing historical dataset. The sole address/identity register
is [catalog.json](catalog.json). Weights, adapters, data and arrays remain at
their original storage addresses. This inventory changes no research design.

[中文](qwen3_0p6b_sae_cn.md) · [Access procedure and lifecycle](README.md) ·
[Current Qwen access evidence](checks/2026-10-09_qwen3_available_assets.json) ·
[Whole-library snapshot including the missing source](checks/2026-10-09_access_v4.json)

## Select the model and tensor before selecting a SAE

The standalone SAE was trained while the original 28-layer Qwen backbone was
frozen. It reads the **actual input to the MLP at zero-based layer index 27
(the 28th and final layer)**, captured before
the MLP runs, after that layer's post-Attention normalization. The 1,024 input
coordinates are encoded into 30,000 feature coordinates; ReLU and Top-32 retain
up to 32 positive feature values per token. The decoder reconstructs the MLP
input. Its columns are normalized during training; the encoder does not first
normalize each input to unit length or subtract decoder bias.

| Asset family | Parent and exact readout | Reuse boundary |
|---|---|---|
| E16 standalone SAE | Official pretrained Qwen3-0.6B, 28 layers; zero-based index 27 MLP input, dimension 1024 | Independent `sae_full_final.pt` and milestone exports |
| Current fresh S7 SAE | From-scratch 8-layer S7; zero-based block index 7 (8th layer) Attention output after projection, before residual addition, dimension 1024 | Embedded in the matching model `state.pt` |
| SALL SAEs | Separate from-scratch SALL model; eight embedded SAEs | Use its own native model/config, not the E16 loader |
| A3 router experiment | Separate 12-layer, hidden-512 MoE | No SAE is present in its registered endpoint |

Matching input dimensions cannot align these features or make their loaders
interchangeable. For a fixed SAE applied to an adapted model, record both the
SAE's training parent and the actual model producing the new representations.

## Checkpoints and parent weights

| Registered ID | Actual saved address / object |
|---|---|
| `model_qwen3_0p6b_base_official_a5` | [Official model directory](/data/250010109/model_cache/Qwen3-0.6B-Base-official), the parent recorded by E16 and historical A5/A6 workflows |
| `tokenizer_qwen3_0p6b_base_official_a5` | Tokenizer in the same directory; registered separately |
| `checkpoint_family_qwen3_0p6b_e16_layer27_sae` | [E16 run](/data/250010109/MoE_Router/experiments/20260903_a15_13_e16_dclm_final_layer_sae/runs/full-20260903T150734Z), including two rotating recovery slots |
| `sae_qwen3_0p6b_e16_layer27_final_1b` | [sae_full_final.pt](/data/250010109/MoE_Router/experiments/20260903_a15_13_e16_dclm_final_layer_sae/runs/full-20260903T150734Z/sae_full_final.pt) |
| `sae_qwen3_0p6b_e16_layer27_step_24415` | [sae_step_24415.pt](/data/250010109/MoE_Router/experiments/20260903_a15_13_e16_dclm_final_layer_sae/runs/full-20260903T150734Z/checkpoints/sae_step_24415.pt): 100,003,840 observed raw tokens |
| `sae_qwen3_0p6b_e16_layer27_step_73243` | [sae_step_73243.pt](/data/250010109/MoE_Router/experiments/20260903_a15_13_e16_dclm_final_layer_sae/runs/full-20260903T150734Z/checkpoints/sae_step_73243.pt): 300,003,328 observed raw tokens |
| `sae_qwen3_0p6b_e16_layer27_step_244141` | [sae_step_244141.pt](/data/250010109/MoE_Router/experiments/20260903_a15_13_e16_dclm_final_layer_sae/runs/full-20260903T150734Z/checkpoints/sae_step_244141.pt): 1,000,001,536 observed raw tokens |

The final export is at step 244141. Here “1B” describes tokens observed by SAE
training, not model parameters or language-model training progress. Milestone
and final exports store SAE config/state/metadata without the optimizer. Recovery
slots use a separate optimizer-bearing format. Their mutable `latest.json` is
not a stable checkpoint identity and does not prove exact continuation.

The [original full summary](/data/250010109/MoE_Router/experiments/20260903_a15_13_e16_dclm_final_layer_sae/runs/full-20260903T150734Z/full_summary.json)
records final digest `e4e2049aced8ba9a3b043bbb2b3308b497b7ec22f107531e37197873ee545b65`
and an original reload difference of 0.0. This inventory does not recompute that
digest or repeat loading. The final and 1B milestone have different file sizes;
we make no claim that their tensors or bytes are identical. The native loader
is [sae_core.py](/data/250010109/MoE_Router/experiments/20260903_a15_13_e16_dclm_final_layer_sae/sae_core.py),
`TopKSAE.from_pretrained`, not S7's embedded-state loader.

The official `model_cache` parent and the previously registered `/data/share`
Qwen model remain separate identities. The catalog distinguishes manifest-recorded
weight digests from currently verified small config hashes. This does not repair
missing historical backbone identity evidence in old caches.

## Saved representations, data and training products

| IDs or family | Saved object and main limitation |
|---|---|
| `representation_qwen3_0p6b_e17_dclm_sparse_activation` | [E17 activation cache](/data/250010109/MoE_Router/experiments/20260904_a15_13_e17_sae_hierarchy/runs/full-20260904T023742Z/activation_cache): discovery 261632 and replication 261634 rows of 32 feature IDs/values; no explicit token/window/position IDs in merged arrays |
| `representation_qwen3_0p6b_e18_semantics_035600`, `_040500`, `_042013` | [E18 runs](/data/250010109/MoE_Router/experiments/20260904_a15_13_e18_dataset_conditioned_sae_semantics/runs): each has six sparse caches. The first lacks a completion summary. Latest m2d2_train has 196734 rows; earlier versions have 65576 |
| `data_qwen3_0p6b_e18_e14_eight_task_proxy` | [E14 processed.pt](/data/250010109/datasets/a15_e14_benchmark/processed.pt): eight-task proxy, including GSM8K; distinct from the later full eight-task cache |
| `data_qwen3_0p6b_e18_m2d2_seq256` | [M2D2 sequence-256 prepared data](/data/250010109/datasets/m2d2_wikipedia_3x3/processed/m2d2_3x3_seq256.pt): distinct from the later N8 panel |
| `adapter_family_qwen06b_flat_0907`, `_a5_0908`, `_a6_0908`, `_a6r1_0909` | 15 + 15 + 12 + 12 condition/seed groups, with actual final/update/recovery paths enumerated in the catalog; no frozen backbone weights inside |
| `router_family_qwen06b_a5_frozen`, `feature_groups_qwen06b_a5` | Nine fitted routers and the saved feature groups/graphs used by the historical workflow; these are separate from expert weights |
| `representation_qwen06b_flat_0907_discovery`, `_router`, `_development` | Three frozen-backbone caches with raw h, sparse SAE values and record/shard mapping. Original qualification was `CACHED_NOT_QUALIFIED`; registration does not promote it |
| `teacher_cache_qwen06b_a6_0908`, `_a6r1_0909` | Frozen SAE/GMM probability targets used to train the online router; not learned expert checkpoints |
| `analysis_qwen06b_sae_hierarchy_0909` | Derived graphs/feature maps/coactivation/task composition; conditional historical provenance remains incomplete |

E18's `window_ids` index a selected record/window list, not original global
dataset IDs; original token positions and raw h are not saved. The eight-task
data includes redistributed official-test-origin examples. Historical partitions
and a filename containing “confirmation” do not create an untouched new test set.

E17/E18 parent-model references route to the expected inputs. The earlier E18
035600 run has no readable completion summary, so its parent/SAE/tokenizer
identity remains source-inferred rather than verified for that run. The inspected
historical cache sources do not close the backbone weight digest; registering
today's model files cannot supply that missing historical identity. Data IDs in
these entries provide source navigation, not automatic runtime dependencies for
reading existing arrays.

The 0907 experts read the 3072-dimensional input to MLP down_proj while routers
read the 1024-dimensional MLP input. A5/A6/A6R1 experts and routers read that same
1024-dimensional MLP input. They include a shared expert plus Top-1 expert;
they differ from the current S7 Attention branch with no shared expert. A5's
frozen router weights coexist with an updated balancing bias; A6/A6R1 train
the router using fixed teachers. Exact routing/save/loader definitions are in
each catalog entry's inspected source references.

0907/A5 saves lack explicit RNG fields; A6/A6R1 include RNG. Optimizer presence
alone does not qualify exact resume, and this inventory tests no resume.

## Access and the remaining gap

At **2026-10-09 16:02:39, Asia/Shanghai, effective UID 0**, all 25 available new
entries passed registered access checks. They have not been fully loaded on CPU
or GPU. Checks read file headers/one byte and inspect paths; they do not rerun
analysis or recompute large-file digests.

`data_qwen3_0p6b_senior_exact_sft_legacy_missing` records the unavailable original
path `/mnt/workspace/zx_workspace/sae-guided-router/sft_mixture_6000_each_with_mmlu_bbh_mmlu_eval_aligned/train.parquet`.
The E18 record already marked it `NOT_RUN_MISSING_DATA`; the current path check
also fails. Other external mounts are unknown. The E14 proxy is separately
registered and cannot silently replace the missing original.

```sh
python tools/check_assets.py --strict \
  --asset model_qwen3_0p6b_base_official_a5 \
  --asset tokenizer_qwen3_0p6b_base_official_a5 \
  --asset sae_qwen3_0p6b_e16_layer27_final_1b \
  --asset dclm_pair_v1
```

Use only inputs needed by the authorized stage. Missing required assets follow
the lookup-before-pause procedure in [README](README.md). Actual future training
checkpoints and reusable analysis caches follow its registration lifecycle.
No other user's shared storage was exhaustively searched; this inventory makes
no claim that every historical Qwen SAE has been found.
