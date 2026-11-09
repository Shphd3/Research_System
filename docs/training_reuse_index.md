# Model Training Reuse Index

> **2026-10-31 storage retirement:** The old decommon runs, training configs and launchers were removed at the researcher's request. Only reusable model/data/checkpoint source and evaluation tools remain at the original sibling paths. Old scientific records below resolve to a byte-preserving archive; historical approvals do not authorize new work. Actual spectral routing is in the separate early spectral execution packages, not the decommon source. [Cleanup receipt](/data/250010109/MoE_Router/storage_cleanup_receipts/20261031T033809Z_decommon_academic_order/completion.json).


Verified locally: 2026-09-12

Read this file before proposing a new model-training implementation or whenever
the researcher asks to reference or reuse previous training code. It is an
operational index, not a Protocol, execution approval, or scientific result.
Code, datasets, checkpoints, and raw runs remain in their original workspaces.

## Start Here

Read these four sources first:

1. [Source audit](../Projects/decommon-router-training/docs/source_audit.md) — what the clean trainer reused from the older project and where the historical runtime evidence lives.
2. [Training scaffold README](../Projects/decommon-router-training/README.md) — current code layout, supported training path, tests, and known retired configurations.
3. [Execution envelope](execution_envelope.md) — the current compute profile, image, runtime layer, and only supported submission entry point.
4. [Training observability contract](training_observability_contract.md) — required TensorBoard loss tags and the valid-token comparison coordinate.

Before writing code, state plainly which assets will be **reused**, **adapted**,
or **not reused**, and why.

## Reuse Priority

| Priority | Source | Reuse for | Boundary |
|---|---|---|---|
| 1 | `Projects/decommon-router-training/` | Data loading, distributed training, checkpoint/resume, provenance, health guards, launch structure | Best engineering reference. Its old production pairs are retired, and the whole directory is ignored by the root Git repository; verify that it exists in the current environment. |
| 2 | `/data/250010109/MoE_Router/` | Original Qwen3 MoE semantics and older training behavior | Execution workspace, not a current Git repository. Reuse selected code only after source inspection. |
| 3 | `/mnt/bucket/MoE_Router/experiments/active/exp_hierarchical/2026-05-05-real_dclm_qwen3_hier_moe/` | Actual historical configs, launcher, logs, and checkpoints from a stable training family | Mounted historical record. Runtime artifacts outrank its planning files, but its architecture and submission environment are old. |
| 4 | `Projects/decommon-router-evaluation/` | Held-out loss and downstream-evaluation pipeline | Evaluation only; it does not authorize or launch training. |

The 0912 draft under `daily_research_reports/0912/docs/code/` is a design
reference, not yet a runnable package: its imports expect missing `model/`,
`analysis/`, `data/`, and `utils/` package directories, and it has no complete
pretraining/resume loop.

### Current Dense LM / SAE execution package

The runnable adaptation now lives at
`/data/250010109/MoE_Router/experiments/20260912_dense_sae_pretraining`.
For this workstream, read its `README.md` and `docs/reuse_sources.json` before
returning to the historical sources. It reuses the clean data/checkpoint
framework and now implements an eight-layer Dense LM whose final-block
post-`norm2` MLP input is mediated by a width-30,000 Top-K SAE. LM loss traverses
the SAE; a separate detached reconstruction pass restricts reconstruction-loss
gradients to SAE parameters. The current source passed a bounded four-H100
Smoke under `runs/smoke_bottleneck8_4h100_202609121034/`. The researcher then
approved the separate exact 50B execution scope; its config and entrypoint are
`configs/full_4h100_sae30k_50b.json` and `scripts/run_full_4h100.sh`.
The flat draft above remains a design reference; it was not overwritten.

- [Execution record](../research/from-attention-to-search/main/experiments/A15/15_17_three_model_sae_representation_trajectory/supporting_records/sae_pretraining/dense_sae_30k/20260912/execution_record.md): completed four-H100 engineering check, preserved failure/repair and evidence boundary.
- [Code handoff](../research/from-attention-to-search/main/experiments/A15/15_17_three_model_sae_representation_trajectory/supporting_records/sae_pretraining/dense_sae_30k/20260912/code_handoff.md): actual file map, interfaces, confirmed external-process resume gaps and prioritized next audits.
- Execution `handoff/baseline_manifest.json`: code-only archive and per-file hashes;
  this execution workspace has no Git repository.

The completed 100-update bottleneck Smoke qualifies the current architecture's
GPU wiring but not 50B stability. External-process recovery is separately
qualified at one/two CPU ranks. Preserve both evidence scopes; a formal-run
startup observation is an operational check, not a long-run or scientific
result.

## Key Code Map

| Need | Preferred source |
|---|---|
| Training loop and distributed execution | `Projects/decommon-router-training/src/decommon_router/train.py` |
| Packed binary-token loader and sampler | `Projects/decommon-router-training/src/decommon_router/data.py` |
| Frozen data-view checks | `Projects/decommon-router-training/src/decommon_router/data_contract.py` |
| Atomic checkpoint and exact resume | `Projects/decommon-router-training/src/decommon_router/checkpoint.py` |
| Tokenizer identity | `Projects/decommon-router-training/src/decommon_router/tokenizer_contract.py` |
| Qwen3 model and MoE implementation | `Projects/decommon-router-training/src/decommon_router/model/qwen3.py` and `model/moe.py` |
| Parallel groups and expert synchronization | `Projects/decommon-router-training/src/decommon_router/model/parallel.py` |
| Original trainer | `/data/250010109/MoE_Router/train_qwen3_moe.py` |
| Original data utilities | `/data/250010109/MoE_Router/src/data_utils.py` |
| Original Qwen3 MoE model | `/data/250010109/MoE_Router/src/model/qwen3_moe/myqwen.py` |
| Downstream evaluator | `Projects/decommon-router-evaluation/src/decommon_eval/` |

For a new dense-model-plus-SAE experiment, prefer reusing the clean scaffold's
training, data, checkpoint, provenance, and monitoring components. Adapt the
model module deliberately; do not inherit the de-common intervention or MoE
architecture merely because they share a trainer.

## Training Data And Tokenizer

### DCLM training corpus

- Dataset: **DCLM-Baseline 1.0**, a public language-model pretraining corpus.
- Official dataset: <https://huggingface.co/datasets/mlfoundations/dclm-baseline-1.0>
- Official code and data instructions: <https://github.com/mlfoundations/dclm>
- Public dataset card: approximately 4T tokens and 3B documents; license
  `CC-BY-4.0`.
- Local pretokenized subset: 1 of the 10 global shards,
  `global-shard_01_of_10`.
- Local source directory:
  `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10`
- Local format: flat `uint32` token IDs in `*.bin` files.
- Verified local inventory: 2,420 files, 1,208,817,927,704 bytes, and
  302,204,481,926 token IDs.

### Frozen paired view

- Training view: `/data/250010109/training_data_views/dclm_pair_v1/train`
- Manifest: `/data/250010109/training_data_views/dclm_pair_v1/manifest.json`
- Manifest SHA-256:
  `8a91bdbb0eb537bd80612015b99f178ca1cbb54a2fa7cf8442ab1eae7f0a2f2d`
- Training inventory: 2,419 linked files and 302,089,493,820 token IDs.
- Validation file:
  `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_0_of_10_shard_00000001_processed.bin`
- Validation size: 114,988,106 token IDs.

This view was built for retired matched pairs. It is useful as a reproducible
data asset, but a new Protocol must explicitly decide whether its split and
ordering fit the new question.

### Additional DCLM holdout used by later audits

- Raw held-out source:
  `/mnt/bucket/109_cache_dir/hf_data/dclm_eval_holdout/global-shard_02_of_10/local-shard_0_of_10/shard_00000000_processed.jsonl.zst`
- SHA-256:
  `4c5ce60258943051758148653c448bb57724af7592cc9d3e9c053cc6f9e10323`

This is not automatically the default validation set for a new experiment.

### Tokenizer

- Local Qwen3 tokenizer/model directory: `/data/share/Qwen3-0.6B-Base`
- Official source: <https://huggingface.co/Qwen/Qwen3-0.6B-Base>
- Vocabulary size: 151,936.
- The clean trainer constructs the experimental model from its JSON config; it
  uses this directory to fingerprint and load the tokenizer. The directory also
  contains pretrained weights, which must not be loaded into a claimed
  random-initialization experiment.

## Historical Runs Worth Reading

### Clean four-H100 engineering acceptance

- Record:
  `Projects/decommon-router-training/results/implementation_smokes/20260724_remote_4gpu_idle_full_pipeline/summary_cn.md`
- Demonstrated: a 342,097,408-parameter, 12-layer, 8-expert top-2 model; native
  four-GPU data parallelism; 100 optimizer updates; checkpoint/resume; held-out
  loss; and downstream-evaluation wiring.
- Boundary: engineering acceptance only, not evidence that the de-common method
  works or that long training is stable.

### Older stable real-DCLM family

- Root:
  `/mnt/bucket/MoE_Router/experiments/active/exp_hierarchical/2026-05-05-real_dclm_qwen3_hier_moe/`
- Read actual `results/training/*/run_config.json`, the matching launcher, log,
  and checkpoint together.
- The actual runs used an approximately 441M-parameter, 8-layer, 16-path top-1
  Qwen3 MoE family on the same local DCLM shard. This is historical stability
  evidence, not an architecture-matched template for a new experiment.

## Do Not Reuse Blindly

- `configs/pairs/pair01` through `pair04` in the clean scaffold are retired;
  there is currently no production training command.
- Historical `docs/acp_run.md`, image URLs, quota choices, and direct `sco`
  commands are stale execution instructions. Always read
  [the execution envelope](execution_envelope.md) instead.
- The old planning `run_matrix.json` disagrees with actual runtime configs.
  Prefer run-local configs, logs, and checkpoint manifests.
- Do not treat the 0912 code bundle as runnable until its package layout and
  complete training/resume loop are repaired and checked.
- Reusing infrastructure does not authorize reusing a model architecture,
  dataset split, optimizer, scientific claim, or remote-run scope.

## AI Reminder Contract

When model training is proposed, or the researcher says “参考之前项目的代码”
or “尽量复用”:

1. Read this index and inspect the named source files themselves.
2. Verify that local and mounted paths still exist.
3. Tell the researcher what will be reused, adapted, and newly written.
4. Warn explicitly about retired configs, old submission commands, and any
   architecture or data mismatch.
5. Before execution, read the owning Anchor and Protocol, then resolve the
   current profile, image, runtime layer, and submission entry point from
   `docs/execution_envelope.md`.
6. Require the TensorBoard tags, valid-token counter, matched global batch, and
   token-aligned schedules defined in `docs/training_observability_contract.md`.
