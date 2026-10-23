#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
N8N_BASE_URL="${N8N_BASE_URL:-http://localhost:5678}"
WORKFLOW_FILE="${WORKFLOW_FILE:-${SCRIPT_DIR}/personal-inbox-organizer.workflow.json}"

if [[ -z "${N8N_API_KEY:-}" ]]; then
  echo "오류: N8N_API_KEY 환경 변수가 필요합니다." >&2
  echo "예: N8N_API_KEY=... ./push.sh" >&2
  exit 1
fi

if [[ ! -f "${WORKFLOW_FILE}" ]]; then
  echo "오류: 워크플로우 파일을 찾을 수 없습니다: ${WORKFLOW_FILE}" >&2
  exit 1
fi

python3 -m json.tool "${WORKFLOW_FILE}" >/dev/null

if [[ -n "${N8N_WORKFLOW_ID:-}" ]]; then
  METHOD="PUT"
  ENDPOINT="${N8N_BASE_URL%/}/api/v1/workflows/${N8N_WORKFLOW_ID}"
  echo "기존 워크플로우 ${N8N_WORKFLOW_ID} 업데이트 중..."
else
  METHOD="POST"
  ENDPOINT="${N8N_BASE_URL%/}/api/v1/workflows"
  echo "새 워크플로우 생성 중..."
fi

curl --fail-with-body --silent --show-error \
  --request "${METHOD}" \
  --url "${ENDPOINT}" \
  --header "X-N8N-API-KEY: ${N8N_API_KEY}" \
  --header "Content-Type: application/json" \
  --data-binary "@${WORKFLOW_FILE}"
echo

