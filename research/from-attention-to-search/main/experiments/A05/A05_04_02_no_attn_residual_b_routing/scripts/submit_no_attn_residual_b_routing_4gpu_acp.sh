#!/usr/bin/env bash
set -euo pipefail

cd /data/250010109/Research_System
export PATH=/root/.sco/bin:$PATH

export WORKSPACE_NAME="${WORKSPACE_NAME:-share-space}"
export CLUSTER_NAME="${CLUSTER_NAME:-share-cluster}"
export WORKER_SPEC="${WORKER_SPEC:-n6ls.iu.i40.4}"
export IMAGE_URL="${IMAGE_URL:-registry.cn-sh-01.sensecore.cn/ccr-zhicheng-03/shphd-private-lite:container1-20260523142552}"
export MOUNT_SPEC="${MOUNT_SPEC:-01995892-d478-76d8-aec7-13fd8284477e:/data}"
export CONDA_ENV="${CONDA_ENV:-spectral-hier}"
export JOB_PRIORITY="${JOB_PRIORITY:-normal}"
export RUN_NAME="${RUN_NAME:-no_attn_residual_b_routing_4gpu_20260610}"
export JOB_NAME="${JOB_NAME:-ats-no-attn-residual-b-routing-4gpu}"
export EXP_DIR="${EXP_DIR:-/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A05/A05_04_02_no_attn_residual_b_routing}"
export MAX_PARALLEL="${MAX_PARALLEL:-4}"
export TRAIN_STEPS="${TRAIN_STEPS:-1600}"
export TRAIN_REPEATS_PER_PAIR="${TRAIN_REPEATS_PER_PAIR:-500}"
export EVAL_REPEATS_PER_PAIR="${EVAL_REPEATS_PER_PAIR:-32}"
export BATCH_SIZE="${BATCH_SIZE:-384}"
export EVAL_BATCH_SIZE="${EVAL_BATCH_SIZE:-512}"

SCO_WIDE_ARGS=()
[ -z "${SCO_SUBSCRIPTION:-}" ] || SCO_WIDE_ARGS+=("--subscription=${SCO_SUBSCRIPTION}")
[ -z "${SCO_RESOURCE_GROUP:-}" ] || SCO_WIDE_ARGS+=("--resource-group=${SCO_RESOURCE_GROUP}")
[ -z "${SCO_ZONE:-}" ] || SCO_WIDE_ARGS+=("--zone=${SCO_ZONE}")

SCO_CREATE_ARGS=()
[ -z "${QUOTA_TYPE:-}" ] || SCO_CREATE_ARGS+=("--quota-type=${QUOTA_TYPE}")

mkdir -p "${EXP_DIR}/logs/acp"
RUN_RECORD="${EXP_DIR}/logs/acp/${RUN_NAME}_submit_$(date +%Y%m%d_%H%M%S).log"
{
  echo "time=$(date -Is)"
  echo "workspace=${WORKSPACE_NAME}"
  echo "cluster=${CLUSTER_NAME}"
  echo "worker_spec=${WORKER_SPEC}"
  echo "image_url=${IMAGE_URL}"
  echo "mount_spec=${MOUNT_SPEC}"
  echo "conda_env=${CONDA_ENV}"
  echo "run_name=${RUN_NAME}"
  echo "job_name=${JOB_NAME}"
  echo "exp_dir=${EXP_DIR}"
  echo "max_parallel=${MAX_PARALLEL}"
  echo "train_steps=${TRAIN_STEPS}"
  echo "train_repeats_per_pair=${TRAIN_REPEATS_PER_PAIR}"
  echo "eval_repeats_per_pair=${EVAL_REPEATS_PER_PAIR}"
  echo "batch_size=${BATCH_SIZE}"
  echo "eval_batch_size=${EVAL_BATCH_SIZE}"
} | tee -a "${RUN_RECORD}"

COMMAND=$(cat <<EOF
set -euo pipefail
export CONDA_ENV="${CONDA_ENV}"
export EXP_DIR="${EXP_DIR}"
export RUN_NAME="${RUN_NAME}"
cd /data/250010109/Research_System
source /root/anaconda3/etc/profile.d/conda.sh || source /root/miniconda3/etc/profile.d/conda.sh || true
conda activate "\${CONDA_ENV}" || true
export PYTHONUNBUFFERED=1
export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
mkdir -p "\${EXP_DIR}/logs/acp"
LOG_PATH="\${EXP_DIR}/logs/acp/\${RUN_NAME}_runtime_\$(date +%Y%m%d_%H%M%S).log"
echo "runtime_log=\${LOG_PATH}"
python "\${EXP_DIR}/scripts/run_no_attn_residual_b_routing.py" \
  --output-dir "\${EXP_DIR}" \
  --run-name "\${RUN_NAME}" \
  --run-stage full \
  --train-steps "${TRAIN_STEPS}" \
  --train-repeats-per-pair "${TRAIN_REPEATS_PER_PAIR}" \
  --eval-repeats-per-pair "${EVAL_REPEATS_PER_PAIR}" \
  --batch-size "${BATCH_SIZE}" \
  --eval-batch-size "${EVAL_BATCH_SIZE}" \
  --parallel \
  --max-parallel "${MAX_PARALLEL}" \
  >"\${LOG_PATH}" 2>&1
echo "completed runtime_log=\${LOG_PATH}"
EOF
)
export COMMAND
echo "command=${COMMAND}" >> "${RUN_RECORD}"

if [[ "${NO_ATTN_RESIDUAL_B_ALLOW_REAL_SUBMIT:-0}" != "1" ]]; then
  echo "[dry-run] Set NO_ATTN_RESIDUAL_B_ALLOW_REAL_SUBMIT=1 to submit ACP job." | tee -a "${RUN_RECORD}"
  exit 0
fi

sco acp jobs create \
  "${SCO_WIDE_ARGS[@]}" \
  "${SCO_CREATE_ARGS[@]}" \
  --workspace-name="${WORKSPACE_NAME}" \
  --aec2-name="${CLUSTER_NAME}" \
  --job-name="${JOB_NAME}" \
  --container-image-url="${IMAGE_URL}" \
  --training-framework=pytorch \
  --worker-nodes=1 \
  --worker-spec="${WORKER_SPEC}" \
  --priority="${JOB_PRIORITY}" \
  --storage-mount="${MOUNT_SPEC}" \
  --command="${COMMAND}" 2>&1 | tee -a "${RUN_RECORD}"
