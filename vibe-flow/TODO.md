개인 인박스 정리기를 하는 n8n 워크플로우를 만들고 싶어

## 제한
    - 입력은 웹훅
    - 출력은 JSON 결과
    - 외부 시스템 연동은 없음 (필요하면 fake sub-workflow로)

## 방법
추천하는 개인 워크플로우 실제 예

지금까지 배운 내용을 개인 생활에 적용한다면 첫 프로젝트로는 **“개인 인박스 정리기”**가 적합합니다.

내가 떠오르는 내용을 한 번에 보내면 일정·할 일·지출·메모로 나누고, 실제 저장 전에는 반드시 확인을 받는 워크플로우입니다.

예를 들어 다음과 같이 입력합니다.

> 내일 오후 3시에 치과 예약. 오늘 교재비로 35,000원 썼어. 금요일까지 프로젝트 발표 자료 만들고, 멀티 에이전트와 라우터의 차이도 메모해 줘.

흐름은 다음과 같습니다.

This Mermaid diagram uses features the terminal renderer doesn't support.
flowchart LR
  W["개인 인박스<br/>message · user · timezone"] --> V{"입력 있음?"}
  V -->|아니오| E["400 반환"]
  V -->|예| S["AI: 항목 분리"]
  S --> P["JSON 파싱·날짜 검증"]
  P --> R{"종류별 라우팅"}
  R --> C["일정 후보"]
  R --> T["할 일 후보"]
  R --> X["지출 기록 후보"]
  R --> N["메모 후보"]
  R --> Q["정보 부족<br/>추가 질문"]
  C & T & X & N & Q --> M["결과 취합"]
  M --> A{"사용자 승인?"}
  A -->|아니오| D["초안만 반환"]
  A -->|예| SAVE["각 시스템에 저장"]
  SAVE --> O["처리 결과·실패 항목 반환"]

첫 응답은 바로 저장하지 않고 다음처럼 미리 보여줍니다.

{
  "status": "confirmation_required",
  "items": [
    {
      "type": "calendar",
      "title": "치과 예약",
      "starts_at": "2026-10-23T15:00:00+09:00"
    },
    {
      "type": "expense",
      "category": "교육",
      "amount": 35000,
      "description": "교재비"
    },
    {
      "type": "task",
      "title": "프로젝트 발표 자료 만들기",
      "due_date": "2026-10-23"
    },
    {
      "type": "note",
      "title": "멀티 에이전트와 라우터의 차이",
      "content": null,
      "needs_input": true
    }
  ]
}

## 환경
    - json 워크플로우 나온 결과를 n8n 서버에 push 하는 push.sh 생성
    - n8n 서버는 http://localhost:5678/
