#!/usr/bin/env bash
# ACP submission entry point for Research_System.
#
# Every value below comes from docs/execution_envelope.md through
# `./researchctl envelope`. Nothing in this file restates a profile tuple, an
# image URL, or a mount.
#
# Usage:
#   JOB_NAME=my-smoke REMOTE_CMD='nvidia-smi' \
#     bash templates/execution/acp_submit_template.sh
#
# The default is a dry run: it prints the resolved tuple and the exact command
# and creates nothing. A real submission needs every gate:
#
#   DRY_RUN=0 ALLOW_SUBMIT=1 PROTOCOL_APPROVED=1 \
#   [SMOKE_GATE_PASSED=1 for a full run] \
#   JOB_NAME=... REMOTE_CMD='...' RUN_ROOT=/path/to/run \
#     bash templates/execution/acp_submit_template.sh
#
# Optional inputs:
#   SCO_PROFILE   profile key; defaults to the envelope default
#   SCO_IMAGE     image key; defaults to the envelope default
#   REMOTE_DIR    absolute working directory inside the pod
#   RUN_ROOT      where the submission receipt is written
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${HERE}/../.." && pwd)"
cd "${REPO_ROOT}"

SCO_PROFILE="${SCO_PROFILE:-}"
SCO_IMAGE="${SCO_IMAGE:-}"
REMOTE_DIR="${REMOTE_DIR:-/data/250010109/Research_System}"
REMOTE_CMD="${REMOTE_CMD:-}"
JOB_NAME="${JOB_NAME:-}"
RUN_ROOT="${RUN_ROOT:-${REPO_ROOT}/acp_receipts}"
DRY_RUN="${DRY_RUN:-1}"
ALLOW_SUBMIT="${ALLOW_SUBMIT:-0}"
PROTOCOL_APPROVED="${PROTOCOL_APPROVED:-0}"
SMOKE_GATE_PASSED="${SMOKE_GATE_PASSED:-0}"

args=(envelope --format shell)
[[ -n "${SCO_PROFILE}" ]] && args+=(--profile "${SCO_PROFILE}")
[[ -n "${SCO_IMAGE}" ]] && args+=(--image "${SCO_IMAGE}")
eval "$("./researchctl" "${args[@]}")"
export RESOURCE_PROFILE PROFILE_STATUS EXECUTION_SURFACE WORKSPACE AEC2 WORKER_SPEC \
  WORKER_NODES WORKER_PROCESSES GPUS QUOTA_TYPE PRIORITY STORAGE_MOUNT GPU_USED \
  IMAGE_ID IMAGE_STATUS IMAGE_URL IMAGE_INTERPRETER IMAGE_TORCH IMAGE_CUDA \
  IMAGE_ACTIVATION SUBMISSION_ENTRY_POINT ENVELOPE JOB_NAME RUN_ROOT

echo "=== resolved execution tuple (from ${ENVELOPE}) ==="
printf '%-26s %s\n' \
  resource_profile "${RESOURCE_PROFILE} (${PROFILE_STATUS})" \
  execution_surface "${EXECUTION_SURFACE}" \
  workspace "${WORKSPACE}" \
  aec2 "${AEC2}" \
  worker_spec "${WORKER_SPEC}" \
  worker_nodes "${WORKER_NODES}" \
  worker_processes "${WORKER_PROCESSES}" \
  gpus "${GPUS}" \
  quota_type "${QUOTA_TYPE}" \
  priority "${PRIORITY}" \
  storage_mount "${STORAGE_MOUNT}" \
  gpu_used "${GPU_USED}" \
  image_id "${IMAGE_ID} (${IMAGE_STATUS})" \
  image_url "${IMAGE_URL}" \
  interpreter "${IMAGE_INTERPRETER}" \
  torch_cuda "${IMAGE_TORCH} / cuda ${IMAGE_CUDA}" \
  entry_point "${SUBMISSION_ENTRY_POINT}"

if [[ -z "${REMOTE_CMD}" ]]; then
  echo >&2
  echo "REMOTE_CMD is empty; nothing to submit." >&2
  exit 2
fi

POD_LOG_DIR="${POD_LOG_DIR:-${REMOTE_DIR}/acp_receipts/pod}"

# The platform does not retain a finished pod's stdout: `stream-logs` returns
# only the scheduling line. Every run therefore tees its output into the mounted
# storage, so the evidence outlives the pod.
COMMAND="set -euo pipefail; cd $(printf '%q' "${REMOTE_DIR}"); export RESOURCE_PROFILE=$(printf '%q' "${RESOURCE_PROFILE}"); export IMAGE_ID=$(printf '%q' "${IMAGE_ID}"); export IMAGE_URL=$(printf '%q' "${IMAGE_URL}"); mkdir -p $(printf '%q' "${POD_LOG_DIR}"); POD_LOG=$(printf '%q' "${POD_LOG_DIR}")/$(printf '%q' "${JOB_NAME}")-\$(date -u +%Y%m%dT%H%M%SZ).log; echo \"[env] profile=${RESOURCE_PROFILE} image=${IMAGE_ID} host=\$(hostname)\" | tee \"\$POD_LOG\"; { ${REMOTE_CMD} ; } 2>&1 | tee -a \"\$POD_LOG\"; echo \"[pod] full output: \$POD_LOG\""

echo
echo "=== remote command ==="
printf '%s\n' "${COMMAND}"

if [[ "${DRY_RUN}" != "0" ]]; then
  echo
  echo "[dry-run] nothing was submitted. Set DRY_RUN=0 with the remaining gates to submit."
  exit 0
fi

missing=()
[[ "${ALLOW_SUBMIT}" == "1" ]] || missing+=(ALLOW_SUBMIT=1)
[[ "${PROTOCOL_APPROVED}" == "1" ]] || missing+=(PROTOCOL_APPROVED=1)
[[ -n "${JOB_NAME}" ]] || missing+=("JOB_NAME=<name>")
if [[ "${JOB_NAME}" == *-full* ]]; then
  [[ "${SMOKE_GATE_PASSED}" == "1" ]] || missing+=(SMOKE_GATE_PASSED=1)
fi
if ((${#missing[@]})); then
  echo >&2
  echo "submission blocked; missing gates: ${missing[*]}" >&2
  exit 2
fi

if [[ -x "${SUBMISSION_ENTRY_POINT}" ]]; then
  read -r -a SCO_PREFIX <<< "bash ${SUBMISSION_ENTRY_POINT} acp"
elif command -v sco >/dev/null 2>&1; then
  SCO_PREFIX=(sco)
elif [[ -x /root/.sco/bin/sco ]]; then
  SCO_PREFIX=(/root/.sco/bin/sco)
else
  echo "no SCO entry point found; check ${ENVELOPE} section 2" >&2
  exit 2
fi

mkdir -p "${RUN_ROOT}"
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
RAW="${RUN_ROOT}/submit-${JOB_NAME}-${STAMP}.txt"
RECEIPT="${RUN_ROOT}/submit-${JOB_NAME}-${STAMP}.json"

set +e
"${SCO_PREFIX[@]}" jobs create \
  --workspace-name="${WORKSPACE}" \
  --aec2-name="${AEC2}" \
  --job-name="${JOB_NAME}" \
  --container-image-url="${IMAGE_URL}" \
  --training-framework=pytorch \
  --worker-nodes="${WORKER_NODES}" \
  --worker-spec="${WORKER_SPEC}" \
  --priority="${PRIORITY}" \
  --quota-type="${QUOTA_TYPE}" \
  --storage-mount="${STORAGE_MOUNT}" \
  --command="${COMMAND}" 2>&1 | tee "${RAW}"
STATUS="${PIPESTATUS[0]}"
set -e

python3 - "${RECEIPT}" "${RAW}" "${STATUS}" <<'PY'
import json, pathlib, sys, os, datetime
receipt_path, raw_path, status = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]), int(sys.argv[3])
fields = {k: os.environ.get(k, "") for k in (
    "RESOURCE_PROFILE", "EXECUTION_SURFACE", "WORKSPACE", "AEC2", "WORKER_SPEC",
    "WORKER_NODES", "WORKER_PROCESSES", "GPUS", "QUOTA_TYPE", "PRIORITY",
    "STORAGE_MOUNT", "GPU_USED", "IMAGE_ID", "IMAGE_URL", "IMAGE_INTERPRETER",
    "IMAGE_TORCH", "IMAGE_CUDA", "SUBMISSION_ENTRY_POINT", "ENVELOPE",
)}
raw = raw_path.read_text(encoding="utf-8", errors="replace") if raw_path.is_file() else ""
receipt = {
    "status": "SUBMITTED" if status == 0 else "CREATE_FAILED",
    "exit_code": status,
    "submitted_at": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "resolved_tuple": fields,
    "job_name": os.environ.get("JOB_NAME", ""),
    "raw_output_path": str(raw_path),
    "raw_output": raw[-4000:],
}
receipt_path.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(f"\nreceipt: {receipt_path}")
PY

echo
echo "next: ./researchctl check --repository   # then write the run receipt from templates/execution/run_receipt_template.md"
exit "${STATUS}"
