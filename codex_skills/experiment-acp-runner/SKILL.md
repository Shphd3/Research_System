---
name: experiment-acp-runner
description: Use when turning a research experiment card into a runnable local or ACP/SCO cluster run, especially for from-attention-to-search attention-search experiments that require dry-run submission, GPU/image edits, run records, and mainline-safe result summaries.
metadata:
  short-description: Write experiment cards and ACP run commands
---

# Experiment ACP Runner

Use this when an experiment needs an ACP/SCO cluster command, debug-friendly run
logs, and a short mainline-safe result summary.

## Required Context

Before writing commands or conclusions:

1. Read the active project's `main/` files, especially `current_mainline.md`.
2. Read the relevant experiment folder under the active `main/experiments/`.
3. Read the experiment workspace `AGENTS.md` and the specific runbook/doc named by the user.
4. For current `from-attention-to-search/XingyuD` work, use:

```text
Projects/from-attention-to-search/XingyuD/main/
```

Do not update `Projects/from-attention-to-search/main/` unless the user
explicitly asks.

ACP defaults live in:

```text
Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/attention_search_hier_kv/docs/acp_run.md
Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/attention_search_hier_kv/configs/real_hierarchical_acp.yaml
```

## ACP Defaults

For the active attention-search ACP path, start from:

```bash
cd /data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/attention_search_hier_kv
export PATH=/root/.sco/bin:$PATH

export WORKSPACE_NAME=share-space
export CLUSTER_NAME=share-cluster
export WORKER_SPEC=n6ls.iu.i40.4
# For 4 GPUs or fewer, omit QUOTA_TYPE and omit --quota-type to use
# guaranteed/default resources. For jobs requesting more than 4 GPUs, use:
# export QUOTA_TYPE=spot
export IMAGE_URL=registry.cn-sh-01.sensecore.cn/ccr-zhicheng-03/shphd-lite3:container1-20260506075648
export MOUNT_SPEC=01995892-d478-76d8-aec7-13fd8284477e:/data
export CONDA_ENV=spectral-hier
export GPU_COUNT=4
export EXP_ROOT=$PWD
export DATASET_ROOT=/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10
export SEED=20260510
```

## Fields To Check

Image must use `image:container-or-tag` form. For example:

```bash
export IMAGE_URL=registry.cn-sh-01.sensecore.cn/ccr-zhicheng-03/shphd-lite3:container1-20260506075648
```

When changing image, replace the value after `IMAGE_URL=...`. Keep the `:`
container/tag part; do not submit a bare image path without it. If the image
should become the default, also update `configs/real_hierarchical_acp.yaml`.

GPU count is encoded in the last field of `WORKER_SPEC`. Example:

```bash
n6ls.iu.i40.4  # final .4 means 4 GPUs
```

When changing card count, keep all of these consistent:

```bash
export WORKER_SPEC=<worker_spec_ending_with_gpu_count>
export GPU_COUNT=<gpu_count>
export DEEPSPEED_NUM_GPUS=<gpu_count>
export JOB_NAME=<job-name-ending-with-${gpu_count}gpu>
```

Quota rule:

- For `GPU_COUNT <= 4`, do not set `export QUOTA_TYPE=spot` and do not pass
  `--quota-type=spot`; this uses guaranteed/default resources.
- For `GPU_COUNT > 4`, set `export QUOTA_TYPE=spot` and pass
  `--quota-type="${QUOTA_TYPE}"`.

The inherited real-small submit script is a 4-GPU path and sets
`CUDA_VISIBLE_DEVICES=0,1,2,3`. For non-4-GPU jobs, patch visible devices before
real submission.

Change data path:

```bash
export DATA_DIR=<mounted_dataset_path>
```

Use `/data` as the mounted storage root unless the project docs say otherwise.

## Dry Run / Submit

Start with a small complete smoke. It should exercise the full path end to end
but stay short: config load, data path, model init, one or a few train/eval
steps, log creation, and output path creation. Do not start a long run until the
smoke passes.

The real-small training wrapper is dry-run by default:

```bash
RUN_PROFILE=hier_moe_candidate \
RUN_NAME=real_small_hier_moe_4x4_6l_1b5ep_seed20260510 \
bash scripts/cluster/submit_real_small_train_acp.sh
```

Real submit requires an explicit guard:

```bash
ATTENTION_SEARCH_ALLOW_REAL_SUBMIT=1 \
RUN_PROFILE=dense_lm \
RUN_NAME=real_small_dense_lm_6l_1b5ep_seed20260510 \
JOB_NAME=ats-real-small-dense-6l-1b5ep-4gpu \
bash scripts/cluster/submit_real_small_train_acp.sh
```

Submit matched profiles with the same seed, token budget, data order, checkpoint
policy, and GPU count before comparing real-data results.

After real submission, supervise for about 20 minutes. During that window:

- stream ACP logs;
- confirm the expected startup signals appear;
- check `nvidia-smi` / memory log if available;
- stop or investigate on fail-fast signals;
- append job id, runtime log path, and first diagnosis to the submit log.

## Log For Debug

Every run must write a log record before or during submission:

```bash
mkdir -p logs/acp
RUN_RECORD="logs/acp/${RUN_NAME}_submit_$(date +%Y%m%d_%H%M%S).log"
{
  echo "time=$(date -Is)"
  echo "workspace=${WORKSPACE_NAME}"
  echo "cluster=${CLUSTER_NAME}"
  echo "worker_spec=${WORKER_SPEC}"
  echo "gpu_count=${GPU_COUNT:-${DEEPSPEED_NUM_GPUS:-unknown}}"
  echo "image_url=${IMAGE_URL}"
  echo "mount_spec=${MOUNT_SPEC}"
  echo "conda_env=${CONDA_ENV}"
  echo "run_profile=${RUN_PROFILE}"
  echo "run_name=${RUN_NAME}"
  echo "job_name=${JOB_NAME}"
  echo "seed=${SEED}"
  echo "command=${COMMAND:-see submit script output}"
} | tee -a "${RUN_RECORD}"
```

After `sco acp jobs create`, append the ACP job id and log stream command to the
same record. If the wrapper already creates `LOG_FILE` and `MEM_FILE`, include
both paths in this submit log.

## Monitoring

```bash
sco acp jobs list --workspace-name=${WORKSPACE_NAME:-share-space} --page-size=100 --user-name=250010109
sco acp jobs stream-logs <job_id> --workspace-name=${WORKSPACE_NAME:-share-space}
```

Fail-fast signals:

```text
CUDA out of memory
Traceback
NaN
RuntimeError
MISSING_SMALL_CONFIG
Missing DATA_DIR
```

Expected startup signals:

```text
RUN_PROFILE=
RUN_NAME=
Total Parameters
Total training tokens
Training Config
```

## Run Record

After completion, summarize only:

- card ID / hypothesis ID
- job id, submit log, runtime log, result/checkpoint path
- direct result, interpretation, limitation, next decision

Only promote a result to the active branch mainline, currently as
`Projects/from-attention-to-search/XingyuD/main/experiments/<experiment_id>/summary.md`
plus `detailed.md`, if it changes a hypothesis status, claim boundary,
experiment status, or next decision.

Do not claim indexed-KV quality from training loss, router accuracy, or ACP
success. Quality claims require post-training candidate retrieval plus exact QK
rerank attention evaluation.
