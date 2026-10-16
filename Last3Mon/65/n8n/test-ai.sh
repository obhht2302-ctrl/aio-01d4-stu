#!/bin/bash
for t in "VPN 접속이 계속 끊겨요" "비밀번호를 잊어버려서 로그인이 안 돼요" "점심 메뉴 추천해줘"; do
  curl -s -m 300 -w "  [%{time_total}s]\n" -X POST http://localhost:5678/webhook/ai-request \
    -H 'Content-Type: application/json' \
    -d "{\"user\":\"kim\",\"text\":\"$t\"}"
done
