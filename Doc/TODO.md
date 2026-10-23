# 목적
- 간단한 url 호출을 위한 curl 기반의 도구

## 방법
- 파이썬 언어 사용
- textual 라이브러리 사용
- TUI가 입력 출력을 맡고 curl은 별도 실행하여 결과를 받아온다.

## 기본 화면
- URL 입력창
- HTTP Method 선택 버튼 (GET, POST, PUT, DELETE)
- JSON 보내기 여부 토글 버튼
- Body 입력창
- 실행 버튼 (터미널의 엔터키로 실행)
- 결과 출력창

## 기존 curl
``` bash
curl -X POST http://localhost:5678/webhook/66-agy \
  -H "Content-Type: application/json" \
  -d '{
    "title": "주간 팀 회의",
    "notes": "참석: 김민지, 이준호, 박서연. 1) 신규 고객 문의 응답 템플릿을 이준호가 금요일까지 정리한다. 2) 박서연은 다음 주 월요일까지 VPN 장애 보고서를 작성한다. 3) 서버 점검 일정은 김민지가 오늘 중 공지한다. 4) 회의실 예약 규칙 개선은 담당자를 다음 회의에서 정한다. 다음 회의는 10월 23일"
  }'