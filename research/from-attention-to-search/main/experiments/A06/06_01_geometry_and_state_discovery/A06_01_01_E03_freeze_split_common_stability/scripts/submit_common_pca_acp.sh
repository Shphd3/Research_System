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
export RUN_NAME="${RUN_NAME:-a06_02_02_freeze_split_common_stability_4gpu_20260614_full01}"
export JOB_NAME="${JOB_NAME:-ats-a06-02-02-common-pca-4gpu-env}"
export EXP_DIR="${EXP_DIR:-/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A06/06_01_geometry_and_state_discovery/A06_01_01_E03_freeze_split_common_stability}"
export RUN_DIR="${RUN_DIR:-${EXP_DIR}/runs/freeze_split_common_stability/${RUN_NAME}}"
export FALLBACK_MODEL_ROOT="${FALLBACK_MODEL_ROOT:-/data/250010109/past_records/qwen_exp}"

SCO_WIDE_ARGS=()
[ -z "${SCO_SUBSCRIPTION:-}" ] || SCO_WIDE_ARGS+=("--subscription=${SCO_SUBSCRIPTION}")
[ -z "${SCO_RESOURCE_GROUP:-}" ] || SCO_WIDE_ARGS+=("--resource-group=${SCO_RESOURCE_GROUP}")
[ -z "${SCO_ZONE:-}" ] || SCO_WIDE_ARGS+=("--zone=${SCO_ZONE}")

SCO_CREATE_ARGS=()
[ -z "${QUOTA_TYPE:-}" ] || SCO_CREATE_ARGS+=("--quota-type=${QUOTA_TYPE}")

mkdir -p "${EXP_DIR}/logs/acp"
RUN_RECORD="${EXP_DIR}/logs/acp/${RUN_NAME}_common_pca_4gpu_env_submit_$(date +%Y%m%d_%H%M%S).log"
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
  echo "run_dir=${RUN_DIR}"
  echo "fallback_model_root=${FALLBACK_MODEL_ROOT}"
} | tee -a "${RUN_RECORD}"

COMMAND=$(cat <<EOF
set -euo pipefail
cd /data/250010109/Research_System
source /root/anaconda3/etc/profile.d/conda.sh || source /root/miniconda3/etc/profile.d/conda.sh || true
conda activate "${CONDA_ENV}" || true
export PYTHONUNBUFFERED=1
export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
export OMP_NUM_THREADS=4
export PYTHONPATH="${FALLBACK_MODEL_ROOT}:\${PYTHONPATH:-}"
test -f "${FALLBACK_MODEL_ROOT}/src/model/qwen3_moe/myqwen.py"
mkdir -p "${EXP_DIR}/logs/acp"
LOG_PATH="${EXP_DIR}/logs/acp/${RUN_NAME}_common_pca_4gpu_env_runtime_\$(date +%Y%m%d_%H%M%S).log"
echo "runtime_log=\${LOG_PATH}"
python "${EXP_DIR}/scripts/audit_common_batch_stability_pca.py" \
  --run-dir "${RUN_DIR}" \
  --steps 0 10 300 \
  --seeds 0 1 2 \
  --num-splits 8 \
  --seqs-per-split 1024 \
  --audit-batch-size 16 \
  --pca-k 1 4 8 \
  --disable-shared-expert \
  --device cuda:0 \
  >"\${LOG_PATH}" 2>&1
echo "completed runtime_log=\${LOG_PATH}"
EOF
)
export COMMAND
echo "command=${COMMAND}" >> "${RUN_RECORD}"

if [[ "${A06_02_02_ALLOW_REAL_SUBMIT:-0}" != "1" ]]; then
  echo "[dry-run] Set A06_02_02_ALLOW_REAL_SUBMIT=1 to submit ACP job." | tee -a "${RUN_RECORD}"
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
