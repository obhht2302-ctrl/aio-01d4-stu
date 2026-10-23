from __future__ import annotations

import asyncio
import json
import shutil
import subprocess
from dataclasses import dataclass

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal
from textual.widgets import Button, Footer, Header, Input, RadioButton, RadioSet, Static, Switch, TextArea


STATUS_MARKER = "__CURL_TUI_STATUS__:"


@dataclass
class CurlResult:
    """The useful parts of one curl invocation."""

    exit_code: int
    status: str
    body: str
    error: str


class CurlTui(App[None]):
    TITLE = "curl TUI"
    SUB_TITLE = "간단한 HTTP 요청 도구"

    CSS = """
    Screen { layout: vertical; }
    #request { height: auto; padding: 1 2; }
    #url { width: 1fr; }
    #methods { width: 1fr; height: 3; }
    #options { height: 4; align: left middle; }
    #json-switch { margin-left: 1; }
    #body { height: 12; margin-top: 1; }
    #run { width: 18; margin-top: 1; }
    #result-label { margin: 1 2 0 2; }
    #result { height: 1fr; margin: 0 2 1 2; padding: 1; border: round $accent; overflow: auto; }
    .label { width: 12; padding-top: 1; }
    """

    BINDINGS = [
        ("ctrl+enter", "run_request", "실행"),
        ("ctrl+q", "quit", "종료"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        with Container(id="request"):
            with Horizontal():
                yield Static("URL", classes="label")
                yield Input(placeholder="https://api.example.com/items", id="url")
            with Horizontal():
                yield Static("HTTP Method", classes="label")
                with RadioSet(id="methods"):
                    yield RadioButton("GET", value=True)
                    yield RadioButton("POST")
                    yield RadioButton("PUT")
                    yield RadioButton("DELETE")
            with Horizontal(id="options"):
                yield Static("JSON 보내기", classes="label")
                yield Switch(id="json-switch")
            yield TextArea(
                "",
                language="json",
                soft_wrap=True,
                show_line_numbers=True,
                id="body",
            )
            yield Button("실행", id="run", variant="primary")
        yield Static("결과", id="result-label")
        yield Static("요청을 입력한 뒤 Ctrl+Enter 또는 실행 버튼을 누르세요.", id="result")
        yield Footer()

    def on_mount(self) -> None:
        self.query_one("#url", Input).focus()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "run":
            self.action_run_request()

    def action_run_request(self) -> None:
        url = self.query_one("#url", Input).value.strip()
        body = self.query_one("#body", TextArea).text
        send_json = self.query_one("#json-switch", Switch).value
        result = self.query_one("#result", Static)

        if not url:
            result.update("오류: URL을 입력하세요.")
            self.query_one("#url", Input).focus()
            return
        if not url.startswith(("http://", "https://")):
            result.update("오류: URL은 http:// 또는 https://로 시작해야 합니다.")
            return
        if send_json and body.strip():
            try:
                json.loads(body)
            except json.JSONDecodeError as error:
                result.update(f"오류: 유효하지 않은 JSON입니다. (줄 {error.lineno}, 열 {error.colno})")
                return
        if shutil.which("curl") is None:
            result.update("오류: 시스템에서 curl 실행 파일을 찾을 수 없습니다.")
            return

        method = self._selected_method()
        result.update(f"{method} 요청을 보내는 중입니다…")
        self.run_worker(self._send_request(url, method, body, send_json), exclusive=True)

    def _selected_method(self) -> str:
        methods = self.query_one("#methods", RadioSet)
        selected = methods.pressed_button
        return str(selected.label) if selected else "GET"

    async def _send_request(self, url: str, method: str, body: str, send_json: bool) -> None:
        curl_result = await asyncio.to_thread(self._curl, url, method, body, send_json)
        self._show_result(curl_result)

    @staticmethod
    def _curl(url: str, method: str, body: str, send_json: bool) -> CurlResult:
        command = [
            "curl",
            "--silent",
            "--show-error",
            "--location",
            "--request",
            method,
            "--write-out",
            f"\\n{STATUS_MARKER}%{{http_code}}",
        ]
        if send_json:
            command.extend(["--header", "Content-Type: application/json"])
        if body:
            command.extend(["--data-raw", body])
        command.append(url)
        completed = subprocess.run(command, capture_output=True, text=True, check=False)
        response, marker, status = completed.stdout.rpartition(STATUS_MARKER)
        return CurlResult(
            exit_code=completed.returncode,
            status=status.strip() if marker else "알 수 없음",
            body=response.rstrip("\n") if marker else completed.stdout,
            error=completed.stderr.strip(),
        )

    def _show_result(self, response: CurlResult) -> None:
        header = f"curl 종료 코드: {response.exit_code} | HTTP 상태: {response.status}"
        parts = [header]
        if response.error:
            parts.extend(["\n오류", response.error])
        if response.body:
            parts.extend(["\n응답 본문", response.body])
        elif not response.error:
            parts.append("\n(응답 본문 없음)")
        self.query_one("#result", Static).update("\n".join(parts))


def main() -> None:
    CurlTui().run()


if __name__ == "__main__":
    main()
