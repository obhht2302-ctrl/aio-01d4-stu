# curl-tui

`curl` 명령을 터미널 화면에서 간단히 실행하는 Textual 기반 TUI입니다.

## 실행

Python 3.10 이상과 시스템의 `curl`이 필요합니다.

```bash
cd curl-tui
python -m venv .venv
source .venv/bin/activate
pip install -e .
curl-tui
```

또는 uv를 사용한다면 다음처럼 실행할 수 있습니다.

```bash
uv run curl-tui
```

## 사용법

- URL을 입력하고 HTTP 메서드를 선택합니다.
- JSON 보내기를 켜면 `Content-Type: application/json`을 추가하고 본문 JSON을 검사합니다.
- 본문은 JSON이 아닐 때도 원문 그대로 전송할 수 있습니다.
- `Ctrl+Enter` 또는 **실행** 버튼으로 요청을 전송합니다. `Ctrl+Q`로 종료합니다.

응답 창에는 curl의 종료 상태, HTTP 상태 코드, 응답 본문 또는 오류 메시지가 표시됩니다.
