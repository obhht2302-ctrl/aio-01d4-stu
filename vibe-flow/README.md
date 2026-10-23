# 개인 인박스 정리기

`SPEC.md`와 `TODO.md`의 원칙을 반영한 n8n 워크플로우입니다. 입력 검증과 승인 여부는 규칙으로 처리하고, 자연어 항목 분리는 자격 증명 없이 실행 가능한 `Code` 노드에 격리했습니다. 실제 외부 저장 대신 종류별 fake target에 저장한 결과를 반환합니다.

## 설치

API 키를 n8n의 **Settings → n8n API**에서 만든 뒤 실행합니다.

```bash
chmod +x push.sh
N8N_API_KEY='your-api-key' ./push.sh
```

이미 생성된 워크플로우를 업데이트할 때는 ID를 함께 지정합니다.

```bash
N8N_API_KEY='your-api-key' N8N_WORKFLOW_ID='workflow-id' ./push.sh
```

업로드 후 n8n 화면에서 워크플로우를 활성화해야 production webhook을 사용할 수 있습니다.

## 1단계: 미리보기

```bash
curl -sS http://localhost:5678/webhook/personal-inbox \
  -H 'Content-Type: application/json' \
  -d '{
    "message": "내일 오후 3시에 치과 예약. 오늘 교재비로 35,000원 썼어. 금요일까지 프로젝트 발표 자료 만들고, 멀티 에이전트와 라우터의 차이도 메모해 줘.",
    "user": "me",
    "timezone": "Asia/Seoul"
  }'
```

응답의 `status`는 `confirmation_required`이며, `items`와 확인 요청에 사용할 `request_id`를 포함합니다. 날짜나 종류가 불명확한 항목은 `needs_input: true`와 질문으로 표시됩니다.

## 2단계: 승인 또는 취소

사용자가 미리보기 항목을 검토하고 빠진 정보를 채운 뒤 같은 웹훅으로 전송합니다.

```json
{
  "action": "confirm",
  "request_id": "inbox_...",
  "items": [
    {
      "type": "calendar",
      "title": "치과 예약",
      "starts_at": "2026-10-23T15:00:00+09:00",
      "needs_input": false
    }
  ]
}
```

승인 가능한 종류는 `calendar`, `task`, `expense`, `note`입니다. 필수 정보가 없거나 `needs_input`이 남은 항목은 HTTP 400으로 거절되어 저장되지 않습니다. 취소는 다음처럼 보냅니다.

```json
{ "action": "cancel", "request_id": "inbox_..." }
```

## 교체 지점

- `Extract, Validate & Route Draft`: 현재 규칙 기반 한국어 분류기입니다. AI 모델을 사용할 때 이 노드만 Structured Output을 반환하는 AI 노드로 교체할 수 있습니다.
- `Fake Save by Route`: 현재 외부 변경 없이 `fake_calendar`, `fake_task_list`, `fake_expense_ledger`, `fake_notes` 결과를 만듭니다. 실제 연동 시 타입별 sub-workflow 호출로 교체합니다.
- Webhook 테스트 URL은 비활성 상태에서 `/webhook-test/personal-inbox`, 활성 상태에서 `/webhook/personal-inbox`입니다.
