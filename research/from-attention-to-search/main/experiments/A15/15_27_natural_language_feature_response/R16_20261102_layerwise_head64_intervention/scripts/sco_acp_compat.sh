#!/usr/bin/env bash
set -euo pipefail

PACKAGE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
COMPONENT="${SCO_ACP_COMPONENT:-/root/.local/share/sco/store/acp/sco-acp}"
COMPAT_PORT="${ACP_COMPAT_PORT:-18082}"
COMPAT_LOG="${ACP_COMPAT_LOG:-/tmp/h768-l4-switch-5090-acp-compat.log}"
COMPAT_PID="${ACP_COMPAT_PID:-/tmp/h768-l4-switch-5090-acp-compat.pid}"

port_ready() {
  python - "${COMPAT_PORT}" <<'PY'
import socket
import sys

with socket.socket() as sock:
    sock.settimeout(0.2)
    raise SystemExit(0 if sock.connect_ex(("127.0.0.1", int(sys.argv[1]))) == 0 else 1)
PY
}

if ! port_ready; then
  ACP_COMPAT_PORT="${COMPAT_PORT}" nohup python -u \
    "${PACKAGE_ROOT}/scripts/acp_workspace_compat_proxy.py" \
    >"${COMPAT_LOG}" 2>&1 &
  echo "$!" >"${COMPAT_PID}"
  for _ in $(seq 1 50); do
    port_ready && break
    sleep 0.1
  done
fi
port_ready || { echo "ACP workspace compatibility bridge failed to start" >&2; exit 2; }

while IFS=' = ' read -r key value; do
  value="${value#\'}"
  value="${value%\'}"
  case "${key}" in
    access_key_id) export SCO_ACCESS_KEY_ID="${value}" ;;
    access_key_secret) export SCO_ACCESS_KEY_SECRET="${value}" ;;
  esac
done < "${SCO_PROFILE_PATH:-/root/.config/sco/profiles/default.toml}"

export SCO_ENVIRONMENT=cn
export SCO_ZONE=cn-sh-01g
export SCO_SUBSCRIPTION=default
export SCO_RESOURCE_GROUP=default
export SCO_BASE_URL_MANAGEMENT_CN_SH_01="http://127.0.0.1:${COMPAT_PORT}"
export SCO_BASE_URL_MANAGEMENT_CN_SH_01G="http://127.0.0.1:${COMPAT_PORT}"
export SCO_BASE_URL_SRM_CN_SH_01="http://127.0.0.1:${COMPAT_PORT}/rmh"
export SCO_BASE_URL_SRM_CN_SH_01G="http://127.0.0.1:${COMPAT_PORT}/rmh"
export SCO_BASE_URL_ACP_CN_SH_01=https://aec2.cn-sh-01.sensecoreapi.cn
export SCO_BASE_URL_ACP_CN_SH_01G=https://aec2.cn-sh-01.sensecoreapi.cn
export SCO_BASE_URL_MONITOR_CN_SH_01=https://monitor.sensecoreapi.cn/monitor/ts/data
export SCO_BASE_URL_MONITOR_CN_SH_01G=https://monitor.sensecoreapi.cn/monitor/ts/data

if [[ "${1:-}" == "acp" ]]; then
  shift
fi
exec "${COMPONENT}" "$@"
