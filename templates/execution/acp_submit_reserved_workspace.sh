#!/usr/bin/env bash
# Select one user-authorized Reserved workspace, then reuse the canonical
# resolver, gate checks, durable pod logging and submission receipt template.
# Default: dry run. Required selector: RESERVED_WORKSPACE=share|p12.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
case "${RESERVED_WORKSPACE:-}" in
  share) SELECTED_PROFILE=h100-4-reserved ;;
  p12) SELECTED_PROFILE=p12-h100-4-reserved ;;
  *) echo "Set RESERVED_WORKSPACE=share or RESERVED_WORKSPACE=p12." >&2; exit 2 ;;
esac
if [[ -n "${SCO_PROFILE:-}" && "${SCO_PROFILE}" != "${SELECTED_PROFILE}" ]]; then
  echo "SCO_PROFILE conflicts with RESERVED_WORKSPACE; use one consistent selection." >&2
  exit 2
fi
export SCO_PROFILE="${SELECTED_PROFILE}"
export ACP_COMPAT_PORT=18087

if [[ "${DRY_RUN:-1}" == "0" ]]; then
  : "${REMOTE_DIR:?Set REMOTE_DIR to the task directory on mounted /data.}"
  : "${RUN_ROOT:?Set RUN_ROOT to the task receipt directory.}"
  : "${JOB_NAME:?Set a unique JOB_NAME.}"
  shopt -s nullglob
  receipts=("${RUN_ROOT}"/submit-"${JOB_NAME}"-*.json)
  if ((${#receipts[@]})); then
    echo "A receipt already exists for JOB_NAME in RUN_ROOT; inspect that job before retrying." >&2
    exit 2
  fi
  HELPER=/data/250010109/MoE_Router/experiments/20261108_p12_four_gpu_storage_smoke/agent_submission_guide/sco_workspace.py
  [[ -f "${HELPER}" ]] || { echo "Missing workspace compatibility helper: ${HELPER}" >&2; exit 2; }
  mkdir -p "${RUN_ROOT}"
  # Read-only access check also starts the corrected local compatibility bridge.
  python3 "${HELPER}" --workspace "${RESERVED_WORKSPACE}" jobs list \
    --user-name 250010109 --page-size 1 -o json \
    >"${RUN_ROOT}/workspace-access-check.txt"
fi

exec bash "${HERE}/acp_submit_template.sh"
